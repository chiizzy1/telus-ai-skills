#!/usr/bin/env python3
"""
POI Evaluation recon — the mandatory gate before rating any dimension.

    python3 telus-ai-skills/poi-evaluation-evaluator/scripts/poi_recon.py task.json

Dedicated to POI Evaluation. It shares only `tools/check_urls.py` with the other
TELUS task types, and changes nothing there — Maps, SBS and Ads Relevance are
unaffected by edits to this file.

What it does, and does not do:

  Phase 0  input gate — refuses on a missing name, address or coordinates rather
           than letting you guess them
  Phase 1  one parallel fetch of the listed URL plus any candidate official pages
  Phase 2  pin geometry — reverse-geocode the pin, FORWARD-geocode the claimed
           address, and report the distance between them
  Phase 3  closure signals, from page bodies and from a successor tenant at the
           claimed street number
  Phase 4  per-dimension flags: URL band pre-classification, social-recency and
           hours-sourcing warnings, and extra address components to verify

It never assigns a rating. Every phase produces evidence and open questions; the
rating is yours, made against the guideline.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
TOOLS_DIR = SKILL_DIR.parent / "tools"
WORKSPACE = SKILL_DIR.parent.parent
OUT_ROOT = WORKSPACE / "TELUS-TASKS" / "url_content"

NOMINATIM = "https://nominatim.openstreetmap.org"
UA = "telus-poi-recon/1.0"
PAUSE = 1.1  # Nominatim asks for <=1 req/sec. Do not lower this.

# Measured on the Maps side by fetching a real page on each host. Skipped here
# means "unfetchable by this script", NOT "worthless" — these stay reachable via
# WebSearch and still count toward a source consensus. Never rate Can't Verify
# because the only sources were on this list.
WALLED = ("yelp.com", "tripadvisor.", "instagram.com", "zmenu.com",
          "allmenus.com", "restaurantji.com", "doordash.com", "grubhub.com",
          "opentable.com", "simon.com", "trulia.com", "yellowpages.com",
          "loc8nearme.com")

SOCIAL = ("facebook.com", "instagram.com", "x.com", "twitter.com", "linkedin.com",
          "tiktok.com", "vk.com", "weibo.com")

# Barred as a source for HOURS by §10.1.1, even where the official site links to
# them. Wider than WALLED: these are readable, they just may not be used.
HOURS_BARRED = ("yelp.com", "tripadvisor.", "google.com/maps", "maps.google",
                "bing.com/maps", "mapquest.com", "yellowpages.com", "foursquare.com",
                "opentable.com", "doordash.com", "grubhub.com", "seamless.com",
                "ubereats.com", "zomato.com", "here.com")

# Multi-word only. Bare "closed" matches every opening-hours table.
CLOSURE_PATTERNS = [
    r"permanently closed", r"closed permanently", r"location has closed",
    r"this location is closed", r"no longer in business",
    r"no longer at this location", r"has permanently closed",
    r"report(?:s|ed)? this location has closed",
]
TEMP_PATTERNS = [r"temporarily closed", r"closed for renovation", r"reopening soon",
                 r"closed for remodel", r"coming soon"]

# Secondary address components. Present in the listing but absent from official
# sources, these are what §6.1 says must be verified through an authoritative
# source before the address can be rated Correct.
UNIT_RE = re.compile(
    r"\b(?:ste|suite|unit|apt|apartment|#|fl|floor|bldg|building|rm|room)\b\.?\s*#?\s*[\w-]+",
    re.I)


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------

def _get(url: str) -> object | None:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return json.loads(r.read().decode("utf-8", "replace"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, OSError):
        return None


def _coords(value: str) -> tuple[float, float]:
    lat, lng = value.replace(" ", "").split(",")
    return float(lat), float(lng)


def _m(a: tuple[float, float], b: tuple[float, float]) -> float:
    """Metres. POI works at building scale, so kilometres would round away the answer."""
    import math
    r = 6371008.8
    p1, p2 = math.radians(a[0]), math.radians(b[0])
    dp, dl = p2 - p1, math.radians(b[1] - a[1])
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(h))


def _read_page(path: Path) -> dict:
    """Parse one check_urls .txt into url / status / automation verdict / body.

    `usable` is deliberately strict. A 403 bot wall still writes a few hundred
    characters, so "body is non-empty" is not evidence the page was read.
    """
    t = path.read_text(encoding="utf-8", errors="replace")

    def field(name, default=""):
        m = re.search(rf"^{name}:\s*(.*)$", t, re.M)
        return m.group(1).strip() if m else default

    parts = re.split(r"^={40,}$", t, maxsplit=1, flags=re.M)
    body = parts[1].strip() if len(parts) > 1 else ""
    if body.startswith("[No extractable content]"):
        body = ""

    status = field("Status")
    m = re.match(r"(\d{3})", status)
    code = int(m.group(1)) if m else 0
    automation = field("Automation Result")
    blocked = (code in (401, 403, 407, 429)
               or automation in ("manual_review_needed", "likely_cu")
               or field("Captcha Detected") == "True"
               or field("Block Detected") == "True")
    return {"url": field("URL", path.name), "final_url": field("Final URL"),
            "code": code, "automation": automation, "body": body,
            "usable": bool(body) and not blocked, "blocked": blocked}


def refuse(message: str) -> None:
    print(f"\nREFUSED: {message}\n", file=sys.stderr)
    print("Fill the missing field in the task file and re-run. Do not rate without a "
          "completed recon — see SKILL.md, Mandatory recon gate.", file=sys.stderr)
    sys.exit(2)


# --------------------------------------------------------------------------
# Phase 0 — input gate
# --------------------------------------------------------------------------

def phase0(task: dict) -> dict:
    name = (task.get("name") or "").strip()
    address = (task.get("address") or "").strip()
    coords = (task.get("coords") or "").strip()

    if not name:
        refuse("`name` is empty. The POI's listed name is the subject of the Name "
               "question and the anchor for every search. A page title is not a "
               "substitute for it.")
    if not coords:
        refuse("`coords` is empty. The Pin question cannot be answered without the "
               "listed coordinates, and estimating them from the address inverts the "
               "check — §7.1 requires the pin be rated independently of the address.")
    try:
        _coords(coords)
    except (ValueError, AttributeError):
        refuse(f"`coords` is not a 'lat,lng' pair: {coords!r}")

    if not address and not task.get("address_absent"):
        refuse("`address` is empty. If the listing genuinely shows no address, set "
               "`address_absent` to a reason — that distinction is the whole "
               "difference between OK Without and Missing.")

    units = UNIT_RE.findall(address) if address else []
    return {
        "name": name,
        "address": address or None,
        "address_absent": task.get("address_absent"),
        "coords": coords,
        "listed_url": task.get("url"),
        "no_listed_url": not task.get("url"),
        "phone": task.get("phone"),
        "category": task.get("category"),
        "hours_present": bool(task.get("hours")),
        "secondary_components": units,
        "note": ("Listing carries secondary address components "
                 f"({', '.join(units)}) — §6.1 requires these be verified through an "
                 "authoritative source if the official source does not show them."
                 if units else ""),
    }


# --------------------------------------------------------------------------
# Phase 1 — fetch the listed URL and any candidate official pages
# --------------------------------------------------------------------------

def phase1(task: dict, run_id: str, fast: bool) -> tuple[dict, Path | None, list[Path]]:
    urls = []
    if task.get("url"):
        urls.append(task["url"])
    urls += [u for u in (task.get("candidate_urls") or []) if u]
    seen, ordered = set(), []
    for u in urls:
        if u not in seen:
            seen.add(u)
            ordered.append(u)

    walled = [u for u in ordered if any(w in u.lower() for w in WALLED)]
    fetch = [u for u in ordered if u not in walled]

    if not fetch:
        return ({"ran": False, "skipped_walled": walled,
                 "note": ("every URL is on a known bot-walled host — nothing fetched. "
                          "Reach these through WebSearch; they still count as sources."
                          if walled else
                          "no URLs supplied. Before rating URL `OK Without`, search for "
                          "an official site and a claimed social page — OK Without "
                          "asserts none exists.")},
                None, [])

    cmd = [sys.executable, str(TOOLS_DIR / "check_urls.py"),
           "--query", task.get("name", ""), "--run-id", run_id,
           "--output-dir", str(OUT_ROOT), "--workers", "8"]
    if fast:
        cmd += ["--no-playwright", "--timeout", "15"]
    proc = subprocess.run(cmd + fetch, capture_output=True, text=True, check=False)

    # check_urls renames its folder when the target exists (run-id -> run-id-NNNNNN).
    run_dir = OUT_ROOT / run_id
    if not (run_dir / "report.json").exists():
        sib = sorted(OUT_ROOT.glob(f"{run_id}-*"), key=lambda p: p.stat().st_mtime)
        if sib:
            run_dir = sib[-1]

    pages = sorted(run_dir.glob("*.txt"))
    if not pages:
        return ({"ran": False, "urls": fetch, "returncode": proc.returncode,
                 "note": "check_urls.py produced no page files — Phase 1 did NOT happen. "
                         "Do not cite any of these URLs.",
                 "stderr": (proc.stderr or "")[-600:]}, None, [])

    parsed = [_read_page(p) for p in pages]
    unchecked = [f"{d['url']} (HTTP {d['code'] or '?'}"
                 + (", blocked" if d["blocked"] else ", empty") + ")"
                 for d in parsed if not d["usable"] and d["code"] not in (404, 410, 503)]
    return ({"ran": True, "urls": fetch, "skipped_walled": walled,
             "pages": [p.name for p in pages], "unchecked": unchecked,
             "note": ("SOME URLS WERE NOT ACTUALLY READ — do not cite them"
                      if unchecked else "")}, run_dir, pages)


# --------------------------------------------------------------------------
# Phase 2 — pin geometry
# --------------------------------------------------------------------------

def phase2(p0: dict) -> dict:
    """Reverse-geocode the pin AND forward-geocode the claimed address.

    Reverse alone answers "what is nearest the pin", which will happily name the
    neighbouring door — two unit numbers four metres apart in one building read
    as different features and are not. The pin-to-claimed-address distance is the
    question the Pin rating actually turns on.
    """
    out: dict = {"reverse": None, "forward": None, "delta_m": None, "notes": []}
    pin = _coords(p0["coords"])

    rev = _get(f"{NOMINATIM}/reverse?format=jsonv2&zoom=18&addressdetails=1"
               f"&lat={pin[0]}&lon={pin[1]}")
    if isinstance(rev, dict) and rev.get("display_name"):
        out["reverse"] = rev["display_name"]
        out["reverse_type"] = f"{rev.get('category','?')}/{rev.get('type','?')}"
    else:
        out["notes"].append("reverse geocode returned nothing — judge the pin from "
                            "imagery and the task's own map layers")

    if p0.get("address"):
        # Geocoders routinely choke on a secondary component ("Suite #5"), and a
        # silent failure here removes the single most useful number in the report.
        # Try the address as listed; on failure, retry with the unit stripped and
        # say which attempt succeeded — "the suite broke the lookup" and "the
        # street number does not exist" are different findings for §6.
        attempts = [(p0["address"], "as listed")]
        if p0.get("secondary_components"):
            bare = re.sub(r"\s*,\s*,", ",", UNIT_RE.sub("", p0["address"])).strip(" ,")
            if bare and bare != p0["address"]:
                attempts.append((bare, "with the secondary component removed"))

        for query, how in attempts:
            time.sleep(PAUSE)
            fwd = _get(f"{NOMINATIM}/search?format=jsonv2&limit=1&q="
                       + urllib.parse.quote(query))
            if isinstance(fwd, list) and fwd:
                fc = (float(fwd[0]["lat"]), float(fwd[0]["lon"]))
                out["forward"] = fwd[0].get("display_name")
                out["forward_coords"] = f"{fc[0]:.6f},{fc[1]:.6f}"
                out["forward_query"] = query
                out["delta_m"] = round(_m(pin, fc))
                if how != "as listed":
                    out["notes"].append(
                        f"the address geocoded only {how} — the geocoder could not "
                        "place the unit. That is a limit of the tool, NOT evidence "
                        "about the unit. Verify the secondary component against an "
                        "authoritative source (§6.1).")
                break
        else:
            out["notes"].append(
                "the claimed address did not forward-geocode, even with any secondary "
                "component removed. That is itself a finding for the Address question "
                "— check whether the street number exists (USPS or the local postal "
                "authority) before assuming a geocoder gap.")

    d = out["delta_m"]
    if d is not None:
        if d <= 30:
            out["notes"].append(f"pin sits {d} m from the claimed address — same "
                                "building at this scale. Confirm the rooftop from "
                                "imagery; do not infer Perfect from this number.")
        elif d <= 120:
            out["notes"].append(f"pin sits {d} m from the claimed address — could be "
                                "the same parcel, next door, or across a public road. "
                                "§7.3.2 boundaries decide it, not the distance.")
        else:
            out["notes"].append(f"pin sits {d} m from the claimed address — far enough "
                                "that Approximate is unlikely. Check whether the pin or "
                                "the address is the wrong one; they are rated "
                                "separately (§7.1).")
    out["reminder"] = ("Distance never decides a pin rating. Boundaries do: same "
                       "parcel, same side of street, same block. A pin outside the "
                       "Approximate area is Wrong, never Next Door (§7.3.2.1).")
    return out


# --------------------------------------------------------------------------
# Phase 3 — closure signals
# --------------------------------------------------------------------------

def phase3(pages: list[Path], p0: dict, p2: dict) -> dict:
    signals: list[dict] = []
    read_any = False

    for path in pages:
        d = _read_page(path)
        if d["code"] in (404, 410):
            signals.append({"kind": "permanent", "url": d["url"],
                            "pattern": f"HTTP {d['code']} on a listed page",
                            "why": "a 404 on the operator's own page is closure "
                                   "evidence; on the listed URL it is also an "
                                   "Incorrect URL under §4.1"})
            continue
        if not d["usable"]:
            continue
        read_any = True
        body = d["body"].lower()
        for pat in CLOSURE_PATTERNS:
            if re.search(pat, body):
                signals.append({"kind": "permanent", "url": d["url"], "pattern": pat})
                break
        for pat in TEMP_PATTERNS:
            if re.search(pat, body):
                signals.append({"kind": "temporary", "url": d["url"], "pattern": pat})
                break

    # Successor tenant: the reverse geocode names a business at the same street
    # number that is not this POI. A purely numeric first component is an address
    # node, not a business, and must not fire.
    rev = p2.get("reverse") or ""
    if rev and p0.get("address"):
        first = rev.split(",")[0].strip()
        num = re.match(r"\s*(\d+)", p0["address"])
        same_number = bool(num and re.search(rf"(^|\D){num.group(1)}(\D|$)", rev))
        looks_like_business = bool(first) and not first[:1].isdigit()
        names_itself = p0["name"].lower()[:12] in rev.lower()
        if same_number and looks_like_business and not names_itself:
            if read_any:
                signals.append({"kind": "co-tenant", "url": "(reverse geocode)",
                                "pattern": f"'{first}' at the same street number",
                                "why": "the POI's own page was read and did not say "
                                       "closed, so this is more likely a co-tenant "
                                       "than a successor — check street imagery"})
            else:
                signals.append({"kind": "permanent", "url": "(reverse geocode)",
                                "pattern": f"'{first}' occupies the same street number",
                                "why": "nothing was successfully read for this POI, so "
                                       "a different business at its number is a real "
                                       "successor-tenant signal"})

    return {"signals": signals, "pages_read": read_any,
            "reminder": ("A signal is a lead, not a State rating. Work §3.2.1.2.1 in "
                         "order: official sources, then authoritative/reliable, then "
                         "count recent written reviews. Closure BANNERS on review "
                         "sites are not allowed as evidence — only written reviews.")}


# --------------------------------------------------------------------------
# Phase 4 — per-dimension flags
# --------------------------------------------------------------------------

def phase4(pages: list[Path], p0: dict, p1: dict) -> dict:
    flags: list[str] = []
    url_band = None
    listed = (p0.get("listed_url") or "").lower()

    by_url = {d["url"]: d for d in (_read_page(p) for p in pages)}
    listed_page = next((d for u, d in by_url.items()
                        if p0.get("listed_url") and u.rstrip("/") == p0["listed_url"].rstrip("/")),
                       None)

    if p0["no_listed_url"]:
        flags.append("No URL in the listing. The answer is OK Without only if research "
                     "finds no official website AND no claimed social page updated in "
                     "the past 12 months; otherwise it is Missing (§4.1).")
    elif listed_page:
        c = listed_page["code"]
        if c in (404, 410):
            url_band = "Incorrect"
            flags.append(f"Listed URL returns HTTP {c}. §4.1 makes a permanent-access "
                         "error Incorrect — NOT Can't Verify.")
        elif c == 503:
            url_band = "Can't Verify"
            flags.append("Listed URL returns HTTP 503. §4.1 puts temporary downtime at "
                         "Can't Verify — this is the one band that means 'try later'.")
        elif listed_page["blocked"]:
            flags.append("Listed URL could not be read by this script (bot wall). That "
                         "is not a rating. Open it another way before deciding.")
        fin = (listed_page.get("final_url") or "").lower()
        if fin and fin.rstrip("/") != listed.rstrip("/"):
            flags.append(f"Listed URL redirects to {listed_page['final_url']} — check "
                         "whether that is a domain-parking or spam page (§4.1 "
                         "Incorrect) or a legitimate move.")

    if any(s in listed for s in SOCIAL):
        flags.append("Listed URL is a social media page. Two checks decide the band: "
                     "is it CLAIMED, and was it updated within the past 12 months? An "
                     "unmaintained claimed page is Incorrect, not Can't Verify. And if "
                     "an official WEBSITE exists, a correct social page is still "
                     "Incorrect (§4.1) — the site takes priority.")

    flags.append("URL band turns on a fact you must go and get: does a "
                 "LOCATION-SPECIFIC page exist? Homepage + location page exists = "
                 "Partially Correct. Homepage + no location pages = Correct (§4.1).")

    if p0["secondary_components"]:
        flags.append("Address carries "
                     f"{', '.join(p0['secondary_components'])}. If the official source "
                     "does not show it, verify through an authoritative source. "
                     "Unverifiable = Incorrect (Unit/Apt), not Correct - Formatting "
                     "Issue — that band is for material that is superfluous but TRUE.")

    if p0.get("category"):
        flags.append("Category: check the reference list even though one is listed "
                     "(§9.1.2 rule 5). Correct requires accuracy AND best fit — an "
                     "accurate but overly broad category is Approximate, a band Maps "
                     "does not have.")

    hours_sources = [u for u in (p1.get("urls") or []) + (p1.get("skipped_walled") or [])
                     if any(b in u.lower() for b in HOURS_BARRED)]
    if p0["hours_present"]:
        flags.append("Hours are listed. §10.1.1 allows ONLY the official website or "
                     "official social page — review sites, SERPs, street imagery and "
                     "maps services are barred even if the official site links to "
                     "them. Get the FULL WEEK, not the current-day default.")
    if hours_sources:
        flags.append("These fetched sources may NOT be used for Hours: "
                     + ", ".join(hours_sources))

    return {"url_band_hint": url_band, "flags": flags}


# --------------------------------------------------------------------------
# report
# --------------------------------------------------------------------------

def write_report(run_dir: Path, run_id: str, p0, p1, p2, p3, p4) -> Path:
    L = [f"# POI recon — {p0['name']}", "",
         f"RUN ID: `{run_id}`", f"Generated: {datetime.now():%Y-%m-%d %H:%M:%S}", "",
         "This is evidence, not ratings. Every band is yours to assign against the "
         "guideline.", ""]

    if p3["signals"]:
        L += ["## ⚠ State signals", ""]
        for s in p3["signals"]:
            L.append(f"- **{s['kind']}** — `{s['pattern']}` — {s['url']}")
            if s.get("why"):
                L.append(f"  - {s['why']}")
        L += ["", f"> {p3['reminder']}", ""]
    else:
        L += ["## State signals", "", "None detected.", "",
              f"> {p3['reminder']}", ""]

    L += ["## Listing", "",
          f"- **Name:** {p0['name']}",
          f"- **Address:** {p0['address'] or '(none listed)'}",
          f"- **Coordinates:** {p0['coords']}",
          f"- **URL:** {p0['listed_url'] or '(none listed)'}",
          f"- **Phone:** {p0['phone'] or '(none listed)'}",
          f"- **Category:** {p0['category'] or '(none listed)'}",
          f"- **Hours:** {'listed' if p0['hours_present'] else 'not listed'}", ""]

    L += ["## Pin geometry", ""]
    L.append(f"- Pin reverse-geocodes to: {p2['reverse'] or '(nothing returned)'}"
             + (f"  _[{p2['reverse_type']}]_" if p2.get("reverse_type") else ""))
    if p2.get("forward"):
        L.append(f"- Claimed address forward-geocodes to: {p2['forward']} "
                 f"(`{p2['forward_coords']}`)")
    if p2.get("delta_m") is not None:
        L.append(f"- **Pin is {p2['delta_m']} m from the claimed address.**")
    for n in p2["notes"]:
        L.append(f"- {n}")
    L += ["", f"> {p2['reminder']}", ""]

    L += ["## Pages", ""]
    if p1.get("ran"):
        L.append(f"Fetched {len(p1.get('pages', []))} page(s) into `{run_dir}`.")
        if p1.get("skipped_walled"):
            L += ["", "Skipped (bot-walled — reach these via WebSearch; they still "
                  "count as sources):"]
            L += [f"- {u}" for u in p1["skipped_walled"]]
        if p1.get("unchecked"):
            L += ["", "**NOT actually read — do not cite:**"]
            L += [f"- {u}" for u in p1["unchecked"]]
    else:
        L.append(p1.get("note", "Phase 1 did not run."))
    L.append("")

    L += ["## Open questions before you rate", ""]
    L += [f"- {f}" for f in p4["flags"]]
    if p4.get("url_band_hint"):
        L += ["", f"Pre-classified URL band from the HTTP status: "
                  f"**{p4['url_band_hint']}** — confirm against §4.1."]
    L += ["", "## Reminders", "",
          "- Read the saved page, not the status code.",
          "- A snippet is not proof. Cite nothing you did not open.",
          "- Batch your remaining lookups into one pass.",
          "- Hours: official website or official social page only.",
          "- Can't Verify means the evidence does not exist — not that a fetch failed.",
          ""]

    path = run_dir / "recon.md"
    path.write_text("\n".join(L), encoding="utf-8")
    return path


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="POI Evaluation recon (Phases 0-4).")
    ap.add_argument("task", help="Path to the task JSON file.")
    ap.add_argument("--run-id", default=None)
    ap.add_argument("--fast", action="store_true",
                    help="Skip the browser fallback. Faster, but loses Facebook and "
                         "any JS-rendered official site.")
    args = ap.parse_args(argv)

    task = json.loads(Path(args.task).read_text(encoding="utf-8"))

    p0 = phase0(task)
    slug = "".join(c if c.isalnum() else "-" for c in p0["name"].lower())[:32]
    run_id = args.run_id or f"poi-{slug.strip('-')}-{datetime.now():%Y%m%d-%H%M%S}"

    p1, run_dir, pages = phase1(task, run_id, args.fast)
    if run_dir is None:
        run_dir = OUT_ROOT / run_id
        run_dir.mkdir(parents=True, exist_ok=True)
    run_id = run_dir.name

    p2 = phase2(p0)
    p3 = phase3(pages, p0, p2)
    p4 = phase4(pages, p0, p1)

    report = write_report(run_dir, run_id, p0, p1, p2, p3, p4)
    (run_dir / "recon.json").write_text(json.dumps(
        {"run_id": run_id, "phase0": p0, "phase1": p1, "phase2": p2,
         "phase3": p3, "phase4": p4}, indent=2), encoding="utf-8")

    print(f"\nRUN ID: {run_id}")
    print(f"REPORT: {report}\n")
    if p3["signals"]:
        print(f"⚠  STATE SIGNALS: {len(p3['signals'])}")
        for s in p3["signals"]:
            print(f"     [{s['kind']}] {s['pattern']} — {s['url']}")
    if p1.get("unchecked"):
        print(f"⚠  {len(p1['unchecked'])} URL(s) were NOT actually read — do not cite:")
        for u in p1["unchecked"]:
            print(f"     {u}")
    if p2.get("delta_m") is not None:
        print(f"\nPin to claimed address: {p2['delta_m']} m")
    print(f"Open questions: {len(p4['flags'])} — read {report.name} before rating.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
