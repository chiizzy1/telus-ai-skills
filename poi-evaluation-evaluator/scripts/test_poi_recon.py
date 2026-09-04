#!/usr/bin/env python3
"""
Regression tests for poi_recon.py — pure logic, no network, runs in milliseconds.

    python3 telus-ai-skills/poi-evaluation-evaluator/scripts/test_poi_recon.py

Every case here encodes a rule the guideline states and a rater can get backwards.
Several are ported from the Maps recon tests because the underlying bug was in
shared logic that shipped once already:

  * a 403 bot wall still writes ~700 chars, so "body is non-empty" is not evidence
    the page was read
  * a purely numeric first component in a reverse geocode is an address node, not
    a successor tenant, and must not fire a closure signal
  * a co-tenant must be SUPPRESSED when the POI's own page was read — a false
    closure signal misdirects the State question, which gates Hours

Run this after any edit to poi_recon.py. It does not replace a live run; it stops
the logic from rotting between them.
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import poi_recon as p  # noqa: E402

FAILED: list[str] = []


def check(name: str, cond: bool, detail: str = "") -> None:
    if cond:
        print(f"  pass  {name}")
    else:
        FAILED.append(name)
        print(f"  FAIL  {name}  {detail}")


def page(d: Path, fname: str, url: str, status: str, automation: str,
         body: str, captcha: str = "False", final: str | None = None) -> Path:
    f = d / fname
    f.write_text(
        f"URL: {url}\nFinal URL: {final or url}\nStatus: {status}\nTitle: t\n"
        f"Captcha Detected: {captcha}\nBlock Detected: False\n"
        f"Automation Result: {automation}\n" + "=" * 80 + f"\n\n{body}\n",
        encoding="utf-8")
    return f


# --------------------------------------------------------------------------
# _read_page — "a file is not a fetch"
# --------------------------------------------------------------------------

def test_read_page(d: Path) -> None:
    print("\n_read_page")
    ok = p._read_page(page(d, "a.txt", "https://ok.test/", "200 - OK",
                           "accessible", "real extracted content here"))
    check("200 with body is usable", ok["usable"] and not ok["blocked"])

    wall = p._read_page(page(d, "b.txt", "https://yelp.test/", "403 - Forbidden",
                             "manual_review_needed", "Please enable JS", captcha="True"))
    check("403 bot wall is NOT usable", not wall["usable"] and wall["blocked"],
          "a captcha page still writes ~700 chars; non-empty is not evidence")

    empty = p._read_page(page(d, "c.txt", "https://js.test/", "200 - OK",
                              "manual_review_needed", "[No extractable content]"))
    check("200 with no extractable content is NOT usable", not empty["usable"])

    gone = p._read_page(page(d, "d.txt", "https://x.test/store/1",
                             "404 - Not found", "likely_cu", "page not found"))
    check("404 is detected by code", gone["code"] == 404)

    down = p._read_page(page(d, "e.txt", "https://y.test/", "503 - Unavailable",
                             "accessible", "maintenance"))
    check("503 is detected by code", down["code"] == 503)


# --------------------------------------------------------------------------
# phase0 — the input gate
# --------------------------------------------------------------------------

def test_phase0() -> None:
    print("\nphase0 — input gate")
    base = {"name": "Cafe", "address": "1 Main St", "coords": "40.0,-80.0"}

    r = p.phase0(base)
    check("a complete listing passes", r["name"] == "Cafe" and r["coords"] == "40.0,-80.0")
    check("no secondary components on a plain address", r["secondary_components"] == [])

    r = p.phase0({**base, "address": "937 Locklayer St, Suite #5, Nashville, TN"})
    check("a suite is detected as a secondary component",
          len(r["secondary_components"]) == 1,
          "§6.1 requires added components be verified before Address can be Correct")

    r = p.phase0({**base, "address": "2700 Alton Pkwy, Ste 121, Irvine, CA"})
    check("'Ste' is detected as well as 'Suite'", len(r["secondary_components"]) == 1)

    r = p.phase0({**base, "address": None, "address_absent": "no address shown"})
    check("a declared-absent address is allowed through", r["address"] is None)

    r = p.phase0(base)
    check("no listed url is flagged, not refused", r["no_listed_url"] is True)

    for label, task in [
        ("refuses on a missing name", {**base, "name": ""}),
        ("refuses on missing coordinates", {**base, "coords": ""}),
        ("refuses on unparseable coordinates", {**base, "coords": "not-a-pair"}),
        ("refuses on a missing address with no declared reason",
         {**base, "address": ""}),
    ]:
        try:
            p.phase0(task)
            check(label, False, "did not refuse")
        except SystemExit as e:
            check(label, e.code == 2)


# --------------------------------------------------------------------------
# distance — POI works at building scale
# --------------------------------------------------------------------------

def test_metres() -> None:
    print("\n_m — building-scale distance")
    a, b = (36.17169, -86.79583), (36.17169, -86.79483)
    d = p._m(a, b)
    check("returns metres, not kilometres", 80 < d < 95, f"got {d:.1f}")
    check("identical points are zero", p._m(a, a) < 0.001)
    # 2563 and 2565 of one building were 4 m apart on a live task and were read as
    # different features. Metres are the only unit that shows that.
    close = p._m((33.5, -117.2), (33.500036, -117.2))
    check("resolves a 4 m separation", 3 < close < 5, f"got {close:.1f}")


# --------------------------------------------------------------------------
# phase3 — State signals. False positives are worse than misses: the State
# question gates the Hours question entirely.
# --------------------------------------------------------------------------

def test_unit_stripping() -> None:
    """The suite token silently broke forward geocoding on the first live run.

    The pin-to-claimed-address distance is the most useful number in the report,
    and losing it produced a message blaming the street number instead."""
    print("\nUNIT_RE — the retry that rescues a geocode")
    addr = "937 Locklayer St, Suite #5, Nashville, TN 37208"
    import re as _re
    bare = _re.sub(r"\s*,\s*,", ",", p.UNIT_RE.sub("", addr)).strip(" ,")
    check("stripping the unit leaves a geocodable address",
          bare == "937 Locklayer St, Nashville, TN 37208", bare)

    addr2 = "2700 Alton Pkwy Ste 121, Irvine, CA"
    bare2 = _re.sub(r"\s+", " ", p.UNIT_RE.sub("", addr2)).strip(" ,")
    check("an inline unit strips without eating the street",
          bare2.startswith("2700 Alton Pkwy") and "121" not in bare2, bare2)

    plain = "1 Main St, Springfield, IL"
    check("an address with no unit is left alone",
          p.UNIT_RE.sub("", plain) == plain)


def test_phase3(d: Path) -> None:
    print("\nphase3 — State signals")
    p0 = {"name": "Beaunuts", "address": "404 N Sycamore St"}

    succ = {"reverse": "Comeback Burger & Fries, 404, North Sycamore Street, Petersburg"}
    check("successor tenant at the same number FIRES",
          len(p.phase3([], p0, succ)["signals"]) == 1)

    bare = {"reverse": "2112, Boulevard, Woodlawn, Colonial Heights, Virginia"}
    check("bare address node does NOT fire",
          len(p.phase3([], {"name": "Cakes and Moore", "address": "2112 Boulevard"},
                       bare)["signals"]) == 0,
          "a numeric first component is an address, not a business")

    itself = {"reverse": "IHOP, 2190, Walker Lake Road, Ontario, Ohio"}
    check("reverse naming the POI itself does NOT fire",
          len(p.phase3([], {"name": "IHOP", "address": "2190 Walker Lake Rd"},
                       itself)["signals"]) == 0)

    other_num = {"reverse": "Some Other Shop, 900, North Sycamore Street, Petersburg"}
    check("a business at a DIFFERENT number does NOT fire",
          len(p.phase3([], p0, other_num)["signals"]) == 0)

    live = [page(d, "live.txt", "https://beaunuts.test/", "200 - OK", "accessible",
                 "Beaunuts — doughnuts and coffee, open daily 7-3")]
    sig = p.phase3(live, p0, succ)["signals"]
    check("co-tenant is downgraded when the POI's own page was read",
          len(sig) == 1 and sig[0]["kind"] == "co-tenant",
          "a false permanent-closure signal would wrongly remove the Hours question")

    p404 = [page(d, "gone.txt", "https://brand.test/store/1535", "404 - Not found",
                 "likely_cu", "not found")]
    r = p.phase3(p404, {"name": "Store", "address": "1 Main St"}, {})
    check("404 on a listed page FIRES as permanent",
          len(r["signals"]) == 1 and r["signals"][0]["kind"] == "permanent")

    body = [page(d, "closed.txt", "https://z.test/", "200 - OK", "accessible",
                 "Yelpers report this location has closed. Find a similar spot.")]
    check("closure phrase in a body FIRES",
          len(p.phase3(body, {"name": "Z", "address": "1 A St"}, {})["signals"]) == 1)

    hours = [page(d, "hours.txt", "https://h.test/", "200 - OK", "accessible",
                  "Mon 9-5 Tue 9-5 Sun Closed")]
    check("'Closed' in an opening-hours table does NOT fire",
          len(p.phase3(hours, {"name": "H", "address": "1 A St"}, {})["signals"]) == 0,
          "bare 'closed' must never match")

    temp = [page(d, "temp.txt", "https://t.test/", "200 - OK", "accessible",
                 "We are temporarily closed for renovation and will reopen in May.")]
    sig = p.phase3(temp, {"name": "T", "address": "1 A St"}, {})["signals"]
    check("a temporary closure is typed as temporary, not permanent",
          len(sig) == 1 and sig[0]["kind"] == "temporary",
          "Temporarily Closed removes the Hours question; Permanently Closed does not")


# --------------------------------------------------------------------------
# phase4 — the per-dimension flags that encode the divergences from Maps
# --------------------------------------------------------------------------

def test_phase4(d: Path) -> None:
    print("\nphase4 — dimension flags")
    base = {"name": "X", "address": "1 Main St", "coords": "40.0,-80.0",
            "listed_url": None, "no_listed_url": True, "phone": None,
            "category": None, "hours_present": False, "secondary_components": []}

    r = p.phase4([], base, {})
    check("no listed URL prompts the OK Without / Missing distinction",
          any("OK Without only if" in f for f in r["flags"]))
    check("the location-specific-page question is always raised",
          any("LOCATION-SPECIFIC" in f for f in r["flags"]),
          "the URL band is conditional both ways and turns on this fact")

    gone = [page(d, "g.txt", "https://x.test/", "404 - Not found", "likely_cu", "nope")]
    r = p.phase4(gone, {**base, "listed_url": "https://x.test/", "no_listed_url": False}, {})
    check("404 on the listed URL pre-classifies as Incorrect",
          r["url_band_hint"] == "Incorrect",
          "§4.1: a permanent-access error is Incorrect, never Can't Verify")

    down = [page(d, "d503.txt", "https://y.test/", "503 - Unavailable", "accessible",
                 "maintenance")]
    r = p.phase4(down, {**base, "listed_url": "https://y.test/", "no_listed_url": False}, {})
    check("503 on the listed URL pre-classifies as Can't Verify",
          r["url_band_hint"] == "Can't Verify")

    r = p.phase4([], {**base, "listed_url": "https://www.facebook.com/thing",
                     "no_listed_url": False}, {})
    check("a social listed URL raises claimed-and-recent AND site-priority",
          any("12 months" in f and "official WEBSITE exists" in f for f in r["flags"]))

    r = p.phase4([], {**base, "secondary_components": ["Suite #5"]}, {})
    check("a secondary address component warns against Correct - Formatting Issue",
          any("superfluous but TRUE" in f for f in r["flags"]))

    r = p.phase4([], {**base, "category": "dining"}, {})
    check("a listed category raises Approximate",
          any("Approximate" in f for f in r["flags"]),
          "the divergence that produced a wrong answer on a live assessment")

    r = p.phase4([], {**base, "hours_present": True},
                 {"urls": ["https://www.yelp.com/biz/x"]})
    check("hours flag names the official-only rule",
          any("ONLY the official website" in f for f in r["flags"]))
    check("a barred host is named as unusable for Hours",
          any("may NOT be used for Hours" in f for f in r["flags"]),
          "§10.1.1 bars review sites and maps services even when the official site links there")

    redir = [page(d, "r.txt", "https://a.test/", "200 - OK", "accessible", "parked",
                  final="https://parking.example/")]
    r = p.phase4(redir, {**base, "listed_url": "https://a.test/", "no_listed_url": False}, {})
    check("a redirect away from the listed URL is flagged",
          any("redirects to" in f for f in r["flags"]))


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        d = Path(td)
        test_read_page(d)
        test_phase0()
        test_metres()
        test_unit_stripping()
        test_phase3(d)
        test_phase4(d)
    print(f"\n{'FAILED: ' + ', '.join(FAILED) if FAILED else 'all checks passed'}")
    return 1 if FAILED else 0


if __name__ == "__main__":
    sys.exit(main())
