#!/usr/bin/env python3
"""
Regression tests for maps_recon.py — pure logic, no network, runs in milliseconds.

    python3 telus-ai-skills/maps-search-evaluator/scripts/test_maps_recon.py

Every case here is a bug that actually shipped. Two of them were caught only
because a task happened to exercise them:

  * phase4 keyed on the *note text* rather than the data, so a later reword of
    that note silently disabled the whole rebrand check.
  * the viewport fallback measured every swept candidate instead of the RETURNED
    results, so it never fired and the second sweep got rate-limited into a
    silent Nominatim fallback.

Run this after any edit to maps_recon.py. It does not replace a live run; it
stops the logic from rotting between them.
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import maps_recon as m  # noqa: E402

FAILED: list[str] = []


def check(name: str, cond: bool, detail: str = "") -> None:
    if cond:
        print(f"  pass  {name}")
    else:
        FAILED.append(name)
        print(f"  FAIL  {name}  {detail}")


def page(d: Path, fname: str, url: str, status: str, automation: str,
         body: str, captcha: str = "False") -> Path:
    p = d / fname
    p.write_text(
        f"URL: {url}\nFinal URL: {url}\nStatus: {status}\nTitle: t\n"
        f"Captcha Detected: {captcha}\nBlock Detected: False\n"
        f"Automation Result: {automation}\n" + "=" * 80 + f"\n\n{body}\n",
        encoding="utf-8")
    return p


# --------------------------------------------------------------------------
# _read_page — "a file is not a fetch"
# --------------------------------------------------------------------------

def test_read_page(d: Path) -> None:
    print("\n_read_page")
    ok = m._read_page(page(d, "a.txt", "https://ok.test/", "200 - OK",
                           "accessible", "real extracted content here"))
    check("200 with body is usable", ok["usable"] and not ok["blocked"])

    wall = m._read_page(page(d, "b.txt", "https://yelp.test/", "403 - Forbidden",
                             "manual_review_needed", "Please enable JS", captcha="True"))
    check("403 bot wall is NOT usable", not wall["usable"] and wall["blocked"],
          "a captcha page still writes ~700 chars; non-empty is not evidence")

    empty = m._read_page(page(d, "c.txt", "https://js.test/", "200 - OK",
                              "manual_review_needed", "[No extractable content]"))
    check("200 with no extractable content is NOT usable", not empty["usable"])

    gone = m._read_page(page(d, "d.txt", "https://brand.test/store/1",
                             "404 - Not found", "likely_cu", "page not found"))
    check("404 is detected by code", gone["code"] == 404)


# --------------------------------------------------------------------------
# phase0 — location intent, the highest-leverage decision in the skill
# --------------------------------------------------------------------------

def test_phase0() -> None:
    print("\nphase0 — location intent")
    base = {"query": "coffee", "user": "40.0,-80.0", "viewport_age": "FRESH"}

    r = m.phase0({**base, "query": "coffee in Boise, ID",
                  "explicit_location": "Boise, ID", "intent_coords": "43.6,-116.2",
                  "user_in_viewport": True})
    check("explicit location wins over user AND viewport",
          r["columns_that_matter"] == "neither", r["columns_that_matter"])

    r = m.phase0({**base, "query": "coffee near me", "user_in_viewport": False})
    check("'near me' uses the user even on a FRESH viewport",
          r["intent"] == "user location")

    r = m.phase0({**base, "viewport_age": "STALE", "user_in_viewport": False})
    check("STALE viewport is ignored outright", r["intent"] == "user location")

    r = m.phase0({**base, "user_in_viewport": True})
    check("FRESH + user inside -> user location", r["intent"] == "user location")

    r = m.phase0({**base, "user_in_viewport": False, "viewport_coords": "41.0,-81.0"})
    check("FRESH + user outside -> viewport", r["intent"] == "the viewport")
    check("fallback is offered when intent is the viewport",
          r.get("viewport_fallback_available") is True)

    for label, task in [
        ("refuses when user_in_viewport is unknown", {**base, "user_in_viewport": None}),
        ("refuses explicit location without intent_coords",
         {**base, "explicit_location": "Boise, ID", "user_in_viewport": True}),
    ]:
        try:
            m.phase0(task)
            check(label, False, "did not refuse")
        except SystemExit as e:
            check(label, e.code == 2)


# --------------------------------------------------------------------------
# viewport fallback — must measure the RETURNED results, not swept candidates
# --------------------------------------------------------------------------

def test_viewport_fallback() -> None:
    print("\nviewport fallback arithmetic")
    vp, far, near = (28.0, -82.8), (37.2, -77.4), (28.05, -82.85)
    check("results 1000+ km from the viewport trigger the fallback",
          m._km(vp, far) > 25)
    check("results inside the viewport do NOT trigger it", m._km(vp, near) < 25)


# --------------------------------------------------------------------------
# phase4 — closure signals. False positives are worse than misses here:
# the checkbox gates all three data dimensions.
# --------------------------------------------------------------------------

def test_term_pattern() -> None:
    print("\n_term_pattern — sweep term collisions")
    import re as _re
    spa = m._term_pattern("spa")
    check("short term is boundary-anchored", spa != "spa", spa)
    check("anchored 'spa' still matches 'Season Spa'",
          bool(_re.search(spa, "Season Spa", _re.I)))
    for bad in ("Kate Spade New York", "Spanish Moss Drive"):
        check(f"anchored 'spa' does NOT match {bad!r}",
              not _re.search(spa, bad, _re.I),
              "bare 'spa' matched these and 504'd the server")

    mas = m._term_pattern("massage")
    check("long term stays unanchored", mas == "massage")
    check("unanchored 'massage' still matches plurals",
          bool(_re.search(mas, "Massages by Anna", _re.I)),
          "anchoring long terms would break plurals")

    check("quotes and backslashes are stripped",
          '"' not in m._term_pattern('sp"a') and "\\" not in m._term_pattern("sp\\a"))


def test_phase4(d: Path) -> None:
    print("\nphase4 — closure signals")

    successor = [{"n": 1, "name": "Beaunuts", "claimed": "404 N Sycamore St",
                  "reverse": "Comeback Burger & Fries, 404, North Sycamore Street, "
                             "Petersburg, Virginia"}]
    r = m.phase4([], {}, successor)
    check("successor tenant at the same number FIRES", len(r["closed_signals"]) == 1)

    bare = [{"n": 3, "name": "Cakes and Moore Bakery", "claimed": "2112 Boulevard",
             "reverse": "2112, Boulevard, Woodlawn, Colonial Heights, Virginia"}]
    check("bare address node does NOT fire",
          len(m.phase4([], {}, bare)["closed_signals"]) == 0,
          "a numeric first component is an address, not a business")

    itself = [{"n": 2, "name": "IHOP", "claimed": "2190 Walker Lake Rd",
               "reverse": "IHOP, 2190, Walker Lake Road, Ontario, Ohio"}]
    check("reverse naming the result itself does NOT fire",
          len(m.phase4([], {}, itself)["closed_signals"]) == 0)

    # Co-tenant: a different business at the address, but the result's own page
    # was read and names it. Angel Hands shares 550 S Watters Rd with BitBranding.
    cot = [{"n": 3, "name": "Angel Hands Massage", "claimed": "550 S Watters Rd",
            "reverse": "BitBranding, 550, South Watters Road, Allen, Texas"}]
    live = [page(d, "live.txt", "https://angelhands.test/", "200 - OK", "accessible",
                 "Angel Hands Massage — Swedish, Lomi Lomi, open daily 9-7")]
    check("co-tenant is SUPPRESSED when the result's own page was read",
          len(m.phase4(live, {}, cot)["closed_signals"]) == 0,
          "false closure gates 3 data dimensions — suppression matters more than firing")
    check("same co-tenant FIRES when nothing was read",
          len(m.phase4([], {}, cot)["closed_signals"]) == 1,
          "unread is not the same as alive")

    p404 = [page(d, "gone.txt", "https://brand.test/store/1535", "404 - Not found",
                 "likely_cu", "not found")]
    r = m.phase4(p404, {"https://brand.test/store/1535": "#3 Store"}, [])
    check("404 on the operator's own page FIRES", len(r["closed_signals"]) == 1)
    check("404 signal is attributed to its result",
          r["closed_signals"][0].get("owner") == "#3 Store")

    body = [page(d, "closed.txt", "https://x.test/", "200 - OK", "accessible",
                 "Yelpers report this location has closed. Find a similar spot.")]
    check("closure phrase in body FIRES", len(m.phase4(body, {}, [])["closed_signals"]) == 1)

    hours = [page(d, "hours.txt", "https://y.test/", "200 - OK", "accessible",
                  "Mon 9-5 Tue 9-5 Sun Closed")]
    check("'Closed' in an opening-hours table does NOT fire",
          len(m.phase4(hours, {}, [])["closed_signals"]) == 0,
          "bare 'closed' must never match")


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        d = Path(td)
        test_read_page(d)
        test_phase0()
        test_viewport_fallback()
        test_term_pattern()
        test_phase4(d)
    print(f"\n{'FAILED: ' + ', '.join(FAILED) if FAILED else 'all checks passed'}")
    return 1 if FAILED else 0


if __name__ == "__main__":
    sys.exit(main())
