#!/usr/bin/env python3
"""
Maps Search recon — one command that runs the whole evidence phase for a TELUS
Maps task and writes a bundle the rating must cite.

It exists because agents skip research steps when those steps are prose in a
reference file, and because ad-hoc follow-up commands are where ratings drift
between agents. Everything deterministic happens here, once, identically.

It does NOT modify the shared tools. check_urls.py and maps_distance.py are
driven by subprocess exactly as the Search SBS and Ads Relevance skills use
them, so nothing here can change their behaviour for other task types.

    python3 telus-ai-skills/maps-search-evaluator/scripts/maps_recon.py task.json

Phases: 0 location intent · 1 page fetches · 2 pin reverse-geocode + delta
        3 candidate sweep and ranking · 4 closure scan

Task file schema (see scripts/task.example.json):

    {
      "query": "Biggby Coffee",
      "viewport_age": "STALE",              # FRESH | STALE | MISSING
      "user": "44.7610473,-85.5889892",     # or null when not shown
      "user_in_viewport": false,            # from the Show All frame
      "explicit_location": null,            # e.g. "Elkton, MD" when the query names a place
      "intent_coords": null,                # required when explicit_location is set
      "viewport_coords": null,              # required when intent resolves to the viewport
      "candidate_terms": ["Biggby"],        # what to sweep for; [] to skip Phase 3
      "results": [
        {"n": 1, "name": "...", "address": "...", "coords": "lat,lng",
         "category": "...", "type": "BUSINESS",
         "url": "https://...",              # REQUIRED for BUSINESS results
         "url_unavailable": null}           # ...or a reason why there is none
      ]
    }

Exit codes: 0 recon complete, 2 refused (inputs missing), 1 unexpected error.
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
OVERPASS = "https://overpass-api.de/api/interpreter"
UA = "telus-maps-recon/3.0"
PAUSE = 1.1  # Nominatim asks for <=1 req/sec. Do not lower this.

# Hosts MEASURED to bot-wall every request, browser included. Calibrated by
# fetching a real page on each and checking what came back — not guessed.
#
#   walled : yelp 403 (403 even with headless Chromium + stealth), tripadvisor 403,
#            yellowpages 403, loc8nearme 403, doordash 403, opentable 403,
#            restaurantji 403, zmenu 403, allmenus geo-blocked, simon 307,
#            instagram 200 but 44 chars of JS shell
#   USABLE : mapquest 202/1.7kB, chamberofcommerce 200/2.8kB,
#            facebook 200/654B **but only via Playwright**
#
# Skipped here means "unfetchable by this script", NOT "worthless". These remain
# reachable via WebSearch and readable by a human, and they still COUNT toward a
# source-consensus threshold. Do not rate Can't Verify because the only sources
# were on this list.
WALLED = ("yelp.com", "tripadvisor.", "instagram.com", "zmenu.com",
          "allmenus.com", "restaurantji.com", "doordash.com", "grubhub.com",
          "opentable.com", "simon.com", "trulia.com", "yellowpages.com",
          "loc8nearme.com")

# Multi-word only. Bare "closed" matches every opening-hours table.
CLOSURE_PATTERNS = [
    r"permanently closed", r"closed permanently", r"location has closed",
    r"this location is closed", r"no longer in business",
    r"no longer at this location", r"has permanently closed",
    r"report(?:s|ed)? this location has closed",
]
TEMP_PATTERNS = [r"temporarily closed", r"closed for renovation", r"reopening soon"]


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------

def _get(url: str) -> object | None:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, ValueError, TimeoutError):
        return None


def _term_pattern(term: str) -> str:
    """Escape a sweep term, boundary-anchoring short ones.

    Overpass regex is substring and case-insensitive, so a 3-letter term collides
    badly: "spa" matched "Kate Spade" and "Spanish Moss Drive", and the bare query
    is broad enough to 504 the server outright. Overpass has no \\b, so anchor with
    a character class instead.

    Long terms stay unanchored on purpose — anchoring "massage" would stop it
    matching "Massages".
    """
    e = re.sub(r'["\\\\]', "", term)
    return f"(^|[^a-zA-Z]){e}($|[^a-zA-Z])" if len(e) <= 4 else e


def _overpass(terms: list[str], lat: float, lng: float, box: float) -> list[dict] | None:
    """One call for the whole candidate sweep.

    Measured against the Nominatim sweep it replaces: 1 call vs 4, ~1.8s vs
    ~3.6s, and 6 candidates vs 1 on the same bounding box. It also returns
    structured tags (name, addr:*, cuisine, brand, opening_hours) instead of a
    display string. Returns None on failure so the caller can fall back.
    """
    bbox = f"{lat - box},{lng - box},{lat + box},{lng + box}"
    clauses = []
    for t in terms:
        e = _term_pattern(t)
        clauses += [f'nwr["name"~"{e}",i]({bbox});',
                    f'nwr["cuisine"~"{e}",i]({bbox});',
                    f'nwr["shop"~"{e}",i]({bbox});',
                    f'nwr["amenity"~"{e}",i]({bbox});',
                    f'nwr["brand"~"{e}",i]({bbox});']
    q = f"[out:json][timeout:25];({''.join(clauses)});out tags center 200;"
    try:
        req = urllib.request.Request(OVERPASS, urllib.parse.urlencode({"data": q}).encode(),
                                     headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=60) as r:
            data = json.loads(r.read())
    except Exception:
        return None
    out = []
    for e in data.get("elements", []):
        c = e.get("center") or e
        if "lat" not in c:
            continue
        tg = e.get("tags", {})
        street = f"{tg.get('addr:housenumber','')} {tg.get('addr:street','')}".strip()
        out.append({"lat": c["lat"], "lon": c["lon"],
                    "name": tg.get("name") or tg.get("brand") or "unnamed",
                    "addr": street, "hours": tg.get("opening_hours", "")})
    return out


def _coords(value: str) -> tuple[float, float]:
    lat, lng = value.replace(" ", "").split(",")
    return float(lat), float(lng)


def _km(a: tuple[float, float], b: tuple[float, float]) -> float:
    import math
    r = 6371.0088
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
    code = int(re.match(r"(\d{3})", status).group(1)) if re.match(r"(\d{3})", status) else 0
    automation = field("Automation Result")
    blocked = (code in (401, 403, 407, 429)
               or automation in ("manual_review_needed", "likely_cu")
               or field("Captcha Detected") == "True"
               or field("Block Detected") == "True")
    return {"url": field("URL", path.name), "code": code, "automation": automation,
            "body": body, "usable": bool(body) and not blocked, "blocked": blocked}


def refuse(message: str) -> None:
    print(f"\nREFUSED: {message}\n", file=sys.stderr)
    print("Fill the missing field in the task file and re-run. Do not rate "
          "without a completed recon — see SKILL.md, Mandatory Recon Gate.",
          file=sys.stderr)
    sys.exit(2)


# --------------------------------------------------------------------------
# Phase 0 — location intent
# --------------------------------------------------------------------------

def phase0(task: dict) -> dict:
    query = (task.get("query") or "").strip()
    if not query:
        refuse("`query` is empty. Without the query nothing can be rated.")

    explicit = task.get("explicit_location")
    near_me = any(t in query.lower() for t in ("near me", "nearby", "nearest", "my location"))
    age = (task.get("viewport_age") or "MISSING").upper()
    inside = task.get("user_in_viewport")
    user = task.get("user")

    if explicit:
        intent = f"explicit location in query: {explicit}"
        basis = "Rule 1 — a stated place overrides user location AND viewport."
        columns = "neither"
        coords = task.get("intent_coords")
        if not coords:
            refuse("`explicit_location` is set, so `intent_coords` is required "
                   "(geocode the stated place) to rank candidates from it.")
    elif near_me:
        intent, basis, columns, coords = (
            "user location",
            "Rule 2 — 'near me' uses the user, ignoring the viewport even when FRESH.",
            "Distance to User", user)
        if not coords:
            refuse("Query says 'near me' but `user` coordinates are missing.")
    else:
        if age == "STALE":
            intent, basis, columns, coords = ("user location",
                                              "Rule 3 — a STALE viewport is ignored outright.",
                                              "Distance to User", user)
        elif age in ("FRESH", "MISSING"):
            if inside is None:
                refuse("`user_in_viewport` is null. This flips the rating and is "
                       "only readable from the Show All frame. Ask for Show All.")
            if inside:
                intent, basis, columns, coords = ("user location",
                                                  "Rule 3 — FRESH viewport, user inside.",
                                                  "Distance to User", user)
            else:
                intent, basis, columns, coords = ("the viewport",
                                                  "Rule 3 — FRESH viewport, user outside.",
                                                  "Distance to Viewport", task.get("viewport_coords"))
                if not coords:
                    refuse("Intent resolves to the viewport, so `viewport_coords` "
                           "is required to rank candidates from it.")
        else:
            refuse(f"Unrecognised viewport_age {age!r}. Use FRESH, STALE or MISSING.")
        if not coords:
            refuse("Location intent resolves to the user but `user` is missing.")

    return {"intent": intent, "basis": basis, "columns_that_matter": columns,
            "intent_coords": coords, "user_coords": user,
            "viewport_fallback_available": intent == "the viewport" and bool(user)}


# --------------------------------------------------------------------------
# Phase 1 — batched page fetches, one URL per business result
# --------------------------------------------------------------------------

def phase1(task: dict, run_id: str, fast: bool) -> tuple[dict, Path | None, list[Path]]:
    """Fetch the per-result pages.

    The browser fallback is ON by default. It was previously off for speed, on the
    assumption it could not rescue a blocked host. Measurement showed that is true
    only for the WALLED hosts, which are now filtered out before we fetch. What it
    DOES rescue is JS-rendered pages and Facebook, which returns nothing without it
    and is an OFFICIAL-tier source under the claimed-social-media rule.
    --fast skips it.
    """
    urls, missing = [], []
    for r in task["results"]:
        if (r.get("type") or "BUSINESS").upper() == "ADDRESS":
            continue
        if r.get("url"):
            urls.append(r["url"])
        elif not r.get("url_unavailable"):
            missing.append(f"#{r.get('n')} {r.get('name')}")
    if missing:
        refuse("These business results have no `url` and no `url_unavailable` reason: "
               + "; ".join(missing) + ".\nPhase 1 is per-result and not optional. A "
               "brand locator index does NOT stand in for a result's own listing — a "
               "chain drops a closed store silently, so absence there produces no signal. "
               "Give each result its own listing page (the operator's store page, or a "
               "listing site that shows a closure banner).")

    urls += list(task.get("extra_urls") or [])

    # Don't spend the fetch budget on hosts that always return a captcha page.
    # Across recent tasks these were ~75% of supplied URLs and 0% of usable reads.
    walled = [u for u in urls if any(w in u.lower() for w in WALLED)]
    urls = [u for u in urls if u not in walled]

    if not urls:
        return ({"ran": False, "skipped_walled": walled,
                 "note": ("every URL is on a known bot-walled host — nothing fetched. "
                          "Use WebSearch for these; a structured status in a search "
                          "result title is worth more than a captcha page."
                          if walled else
                          "no URLs at all — every result declared unavailable")},
                None, [])

    cmd = [sys.executable, str(TOOLS_DIR / "check_urls.py"),
           "--query", task.get("query", ""), "--run-id", run_id,
           "--output-dir", str(OUT_ROOT), "--workers", "8"]
    if fast:
        cmd += ["--no-playwright", "--timeout", "15"]
    proc = subprocess.run(cmd + urls, capture_output=True, text=True, check=False)

    # check_urls renames its folder when the target exists (run-id -> run-id-NNNNNN).
    run_dir = OUT_ROOT / run_id
    if not (run_dir / "report.json").exists():
        sib = sorted(OUT_ROOT.glob(f"{run_id}-*"), key=lambda p: p.stat().st_mtime)
        if sib:
            run_dir = sib[-1]

    pages = sorted(run_dir.glob("*.txt"))
    if not pages:
        return ({"ran": False, "urls": urls, "returncode": proc.returncode,
                 "note": "check_urls.py produced no page files — Phase 1 did NOT happen. "
                         "Do not cite any of these URLs.",
                 "stderr": (proc.stderr or "")[-600:]}, None, [])

    # A file is not a fetch. Verify each one actually carries readable text and
    # was not a bot wall.
    parsed = [_read_page(p) for p in pages]
    # A 404 is not an unchecked page — it is a finding, reported by Phase 4.
    unchecked = [f"{d['url']} (HTTP {d['code'] or '?'}"
                 + (", blocked" if d["blocked"] else ", empty") + ")"
                 for d in parsed if not d["usable"] and d["code"] != 404]
    return ({"ran": True, "urls": urls, "skipped_walled": walled,
             "pages": [p.name for p in pages],
             "unchecked": unchecked,
             "note": ("SOME URLS WERE NOT ACTUALLY READ — do not cite them"
                      if unchecked else "")}, run_dir, pages)


# --------------------------------------------------------------------------
# Phase 2 — reverse-geocode every pin, with the delta
# --------------------------------------------------------------------------

def phase2(results: list[dict]) -> list[dict]:
    out = []
    for r in results:
        row = {"n": r.get("n"), "name": r.get("name"), "claimed": r.get("address")}
        if not r.get("coords"):
            row.update(reverse=None,
                       note="NO PIN SHOWN — a missing pin is Wrong (rating-contract.md)")
            out.append(row)
            continue
        lat, lng = _coords(r["coords"])
        data = _get(f"{NOMINATIM}/reverse?lat={lat}&lon={lng}&format=json&zoom=18") or {}
        row["reverse"] = data.get("display_name")
        addr = data.get("address", {})
        row["postcode"] = addr.get("postcode")
        row["locality"] = addr.get("city") or addr.get("town") or addr.get("village")

        if data.get("lat") and data.get("lon"):
            row["delta_m"] = round(
                _km((lat, lng), (float(data["lat"]), float(data["lon"]))) * 1000)

        # Forward-geocode the CLAIMED address and measure the pin against it.
        # The reverse lookup only says what is nearest; this says whether the pin
        # is where the result claims to be, which is the actual pin question.
        # Without it, a pin resolving to a neighbouring door reads as "wrong unit"
        # when the two addresses may be 4 m apart in one building.
        if r.get("address"):
            time.sleep(PAUSE)
            fwd = _get(f"{NOMINATIM}/search?"
                       f"q={urllib.parse.quote(r['address'])}&format=json&limit=1")
            if fwd:
                a = (float(fwd[0]["lat"]), float(fwd[0]["lon"]))
                row["claimed_geocode"] = f"{a[0]},{a[1]}"
                row["pin_to_claimed_m"] = round(_km((lat, lng), a) * 1000)
            else:
                row["pin_to_claimed_m"] = None
                row["claimed_geocode"] = "claimed address did not geocode"

        name = (r.get("name") or "").lower().split()
        rev = (row["reverse"] or "").lower()
        if not row["reverse"]:
            row["note"] = "reverse lookup failed — judge the pin on the frame alone"
        elif name and name[0] in rev:
            row["note"] = "pin resolves to the result itself — corroborates Perfect"
        elif (row.get("pin_to_claimed_m") or 9999) <= 40:
            row["note"] = (f"reverse names a different feature, but the pin is only "
                           f"{row['pin_to_claimed_m']} m from the CLAIMED address — "
                           "consistent with one multi-tenant building. Do not read this "
                           "as the wrong unit")
        else:
            row["note"] = ("PIN RESOLVES TO A DIFFERENT FEATURE. Check whether they share "
                           "one building before concluding Next Door; there is no Next Door "
                           "inside a shared space")
        out.append(row)
        time.sleep(PAUSE)
    return out


# --------------------------------------------------------------------------
# Phase 3 — candidate set and ranking
# --------------------------------------------------------------------------

def phase3(task: dict, intent_coords: str, terms: list[str]) -> dict:
    ilat, ilng = _coords(intent_coords)
    wide = float(task.get("sweep_degrees") or 0.25)
    candidates: dict[tuple, dict] = {}
    source = "overpass"

    for row in (_overpass(terms, ilat, ilng, wide) or []):
        candidates[(round(float(row["lat"]), 5), round(float(row["lon"]), 5))] = row

    if not candidates:  # Overpass down or nothing tagged — fall back, don't fail.
        source = "nominatim (overpass returned nothing)"
        for box in ([0.05, wide] if wide > 0.05 else [wide]):
            view = f"{ilng - box},{ilat + box},{ilng + box},{ilat - box}"
            for term in terms:
                for row in (_get(f"{NOMINATIM}/search?q={urllib.parse.quote(term)}"
                                 f"&format=json&limit=40&viewbox={view}&bounded=1") or []):
                    key = (round(float(row["lat"]), 5), round(float(row["lon"]), 5))
                    candidates.setdefault(key, {"lat": row["lat"], "lon": row["lon"],
                                                "name": row["display_name"], "addr": "",
                                                "hours": ""})
                time.sleep(PAUSE)
            if len(candidates) >= 8:
                break

    pairs = [(f"RETURNED #{r.get('n')} {r.get('name')}", r["coords"])
             for r in task["results"] if r.get("coords")]
    for (lat, lng), c in candidates.items():
        label = c["name"].split(",")[0]
        if any(label.lower() in (r.get("name") or "").lower() for r in task["results"]):
            continue
        addr = f" ({c['addr']})" if c.get("addr") else ""
        pairs.append((f"not returned — {label}{addr}", f"{lat},{lng}"))
    if not pairs:
        return {"ranked": [], "candidates_found": 0, "source": source}

    tmp = Path("/tmp/_maps_recon_pairs.txt")
    tmp.write_text("\n".join(f"{l}: {intent_coords} {c}" for l, c in pairs), encoding="utf-8")
    proc = subprocess.run(
        [sys.executable, str(TOOLS_DIR / "maps_distance.py"),
         "--batch", str(tmp), "--format", "json"],
        capture_output=True, text=True, check=False)
    try:
        rows = [r for r in json.loads(proc.stdout) if r.get("status") == "ok"]
    except ValueError:
        return {"ranked": [], "candidates_found": len(candidates), "source": source,
                "error": proc.stderr.strip() or "maps_distance.py produced no JSON"}
    rows.sort(key=lambda r: r["km"])
    return {"ranked": rows, "candidates_found": len(candidates), "source": source}


# --------------------------------------------------------------------------
# Phase 4 — closure scan
# --------------------------------------------------------------------------

def phase4(pages: list[Path], result_urls: dict[str, str], pins: list[dict]) -> dict:
    hits, temp, scanned = [], [], []
    parsed = [_read_page(p) for p in pages]

    # Everything we actually READ. If a result's own name turns up in here, it is
    # still trading, so a different business at its address is a CO-TENANT, not a
    # successor. Suppressing that matters more than firing: the closure checkbox
    # gates all three data dimensions, so one false flag silently removes three
    # ratings. (Real case: Angel Hands Massage shares 550 S Watters Rd with
    # BitBranding in a mixed-use development.)
    corpus = " ".join(d["body"].lower() for d in parsed if d["usable"])

    # Cheapest closure signal there is, and it needs no fetch: the pin resolves to
    # a DIFFERENT named business at the SAME street number. That is what a rebrand
    # or a successor tenant looks like in the data.
    for row in pins:
        rev, claimed = row.get("reverse") or "", row.get("claimed") or ""
        m = re.match(r"\s*(\d+)", claimed)
        if not (m and rev):
            continue
        # Key off the DATA, never the note text. A previous version tested the
        # note for "DIFFERENT FEATURE"; a later change reworded that note and
        # silently disabled this check. A successor tenant sits at the same
        # address, so a short pin-to-address distance is the norm here, not a
        # reason to stay quiet.
        first = rev.split(",")[0].strip()
        if first.isdigit():          # bare address node, not a named business
            continue
        nm = (row.get("name") or "").lower().split()
        if nm and nm[0] in rev.lower():   # reverse names the result itself
            continue
        if (row.get("name") or "").lower() in corpus:   # its own listing is live
            continue
        if re.search(rf"\b{m.group(1)}\b", rev):
            hits.append({"url": "(pin reverse-geocode)",
                         "pattern": "different business at the same street number",
                         "owner": f"#{row['n']} {row['name']}",
                         "context": f"Pin resolves to “{rev}” — same street number as the "
                                    f"claimed address, different business. Check whether "
                                    f"{row['name']} still trades there or was replaced."})

    for p in pages:
        d = _read_page(p)
        url, owner = d["url"], result_urls.get(d["url"])

        # A 404 on the operator's own store page is the strongest closure signal
        # available, and it never appears in the body text. Chains delist a closed
        # store rather than announcing it.
        if d["code"] == 404:
            hits.append({"url": url, "pattern": "HTTP 404 on the result's own listing",
                         "owner": owner,
                         "context": "The operator's page for this store no longer exists. "
                                    "Chains delist closed stores silently — treat this as "
                                    "positive evidence of closure and confirm."})
            continue
        if not d["usable"]:
            continue

        scanned.append(url)
        low = d["body"].lower()
        for pat in CLOSURE_PATTERNS:
            m = re.search(pat, low)
            if m:
                s = max(0, m.start() - 90)
                hits.append({"url": url, "pattern": pat, "owner": owner,
                             "context": re.sub(r"\s+", " ", d["body"][s:m.end() + 90]).strip()})
                break
        for pat in TEMP_PATTERNS:
            if re.search(pat, low):
                temp.append({"url": url, "pattern": pat})
                break
    return {"scanned": scanned, "closed_signals": hits, "temporary_signals": temp}


# --------------------------------------------------------------------------
# report
# --------------------------------------------------------------------------

def write_report(run_dir: Path, run_id: str, task: dict, p0, p2, p3, p1, p4) -> Path:
    L = [f"# Maps recon — {run_id}", ""]

    if p4.get("closed_signals"):
        L += ["## ⚠ CLOSURE SIGNALS FOUND", "",
              "Research the real-world state before rating. A confirmed closure means the "
              "`Business/POI is closed or does not exist` checkbox and **only relevance "
              "stays rateable**.", ""]
        for h in p4["closed_signals"]:
            who = f"**{h['owner']}** via " if h.get("owner") else ""
            L += [f"- {who}{h['url']} — `{h['pattern']}`", f"  > …{h['context']}…"]
        L += [""]
    if p4.get("temporary_signals"):
        L += ["## Temporary-closure signals", "",
              "A temporary closure announced by the business counts as **open**, with no "
              "time limit.", ""]
        L += [f"- {h['url']} matched `{h['pattern']}`" for h in p4["temporary_signals"]] + [""]

    L += [f"**Query:** {task.get('query')}",
          f"**Viewport age:** {task.get('viewport_age')}  ",
          f"**User inside viewport:** {task.get('user_in_viewport')}", "",
          "## Phase 0 — location intent", "",
          f"- **Intent:** {p0['intent']}",
          f"- **Basis:** {p0['basis']}",
          f"- **Distance column that matters:** {p0['columns_that_matter']}", ""]
    if p0["columns_that_matter"] == "neither":
        L += ["> The query names its own location. Do NOT demote any result for "
              "distance to the user or the viewport.", ""]

    L += ["## Phase 2 — pin reverse-geocode", ""]
    for row in p2:
        L += [f"**#{row['n']} {row['name']}**",
              f"- claimed: {row['claimed']}",
              f"- pin resolves to: {row['reverse'] or 'NO RESULT'}"]
        if row.get("delta_m") is not None:
            L += [f"- pin sits **{row['delta_m']} m** from that feature"]
        if row.get("pin_to_claimed_m") is not None:
            L += [f"- pin sits **{row['pin_to_claimed_m']} m** from the claimed address"]
        elif row.get("claimed_geocode"):
            L += [f"- {row['claimed_geocode']}"]
        L += [f"- {row['note']}", ""]

    L += ["## Phase 3 — candidate ranking from the location intent", ""]
    if p3.get("ranked"):
        L += ["| Rank | Candidate | Distance | Returned? |", "|---|---|---|---|"]
        for i, r in enumerate(p3["ranked"], 1):
            ret = "**Yes**" if r["label"].startswith("RETURNED") else "No"
            lbl = r["label"].replace("RETURNED #", "#").replace("not returned — ", "")
            L += [f"| {i} | {lbl} | {r['km_text']} | {ret} |"]
        L += ["", f"_{p3['candidates_found']} candidates swept from OpenStreetMap. OSM chain "
                  "coverage is patchy — cross-check the brand's official locator before "
                  "concluding a location does not exist._", ""]
    else:
        L += ["_No ranking produced._ " + str(p3.get("error", "")), ""]

    L += ["## Phase 1 — page fetches", "", f"- ran: {p1['ran']}"]
    for k in ("note",):
        if p1.get(k):
            L += [f"- **{p1[k]}**"]
    if p1.get("urls"):
        L += [f"- fetched: {', '.join(p1['urls'])}"]
    if p1.get("unchecked"):
        L += ["- **NOT ACTUALLY READ (do not cite these):** " + ", ".join(p1["unchecked"])]
    L += ["", "## Phase 4 — closure scan", "",
          f"- pages scanned: {len(p4.get('scanned', []))}",
          f"- closure signals: {len(p4.get('closed_signals', []))}",
          f"- temporary-closure signals: {len(p4.get('temporary_signals', []))}",
          "", "A clean scan is **not** proof a business is open — it only means these "
          "pages did not say otherwise. Absence from a chain locator is a closure signal "
          "the scan cannot see.", "",
          "## What this recon did NOT establish", "",
          "- Rooftop vs parcel vs neighbour — decide on the supplied hybrid frame.",
          "- Whether a business meaningfully offers a queried product or service — "
          "read the MENU, not a directory description.",
          "- **Whether each returned result is trading**, beyond the scan above. Any "
          "result whose page produced no content is unchecked.",
          "- Whether an un-returned candidate is open — confirm before letting it "
          "demote anything.", ""]

    path = run_dir / "recon.md"
    path.write_text("\n".join(L), encoding="utf-8")
    return path


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Maps Search recon (Phases 0-4).")
    ap.add_argument("task", help="Path to the task JSON file.")
    ap.add_argument("--run-id", default=None)
    ap.add_argument("--fast", action="store_true",
                    help="Skip the browser fallback. Faster, but loses Facebook and "
                         "any JS-rendered official site.")
    args = ap.parse_args(argv)

    task = json.loads(Path(args.task).read_text(encoding="utf-8"))
    if not task.get("results"):
        refuse("`results` is empty. Nothing to research.")

    slug = "".join(c if c.isalnum() else "-" for c in (task.get("query") or "task").lower())[:32]
    run_id = args.run_id or f"maps-{slug.strip('-')}-{datetime.now():%Y%m%d-%H%M%S}"

    p0 = phase0(task)
    p1, run_dir, pages = phase1(task, run_id, args.fast)
    if run_dir is None:
        run_dir = OUT_ROOT / run_id
        run_dir.mkdir(parents=True, exist_ok=True)
    run_id = run_dir.name

    result_urls = {r["url"]: f"#{r['n']} {r['name']}"
                   for r in task["results"] if r.get("url")}
    p2 = phase2(task["results"])
    p4 = phase4(pages, result_urls, p2)
    terms = task.get("candidate_terms") or []
    # "If no results can be found in or near the viewport, use user location as
    # secondary intent" (user-intent.md). Decide this BEFORE sweeping — it is pure
    # arithmetic on coordinates already in hand, and sweeping twice gets the second
    # Overpass call rate-limited into a silent Nominatim fallback.
    if p0.get("viewport_fallback_available"):
        vp = _coords(p0["intent_coords"])
        d = [_km(vp, _coords(r["coords"])) for r in task["results"] if r.get("coords")]
        if d and min(d) > 25:
            p0["intent_coords"] = p0["user_coords"]
            p0["intent"] = ("the viewport — but NO result sits in or near it, so "
                            "user location becomes the secondary intent")
            p0["basis"] += (f" Fallback fired: nearest result is {min(d):.0f} km from "
                            "the viewport, so ranking is from the user.")
            p0["columns_that_matter"] = "Distance to User (via the secondary-intent fallback)"

    p3 = (phase3(task, p0["intent_coords"], terms) if terms
          else {"ranked": [], "candidates_found": 0, "error": "no candidate_terms given"})

    report = write_report(run_dir, run_id, task, p0, p2, p3, p1, p4)
    (run_dir / "recon.json").write_text(json.dumps(
        {"run_id": run_id, "phase0": p0, "phase1": p1, "phase2": p2,
         "phase3": p3, "phase4": p4}, indent=2), encoding="utf-8")

    print(f"\nRUN ID: {run_id}")
    print(f"REPORT: {report}\n")
    if p4["closed_signals"]:
        print(f"⚠  CLOSURE SIGNALS: {len(p4['closed_signals'])} — see the top of the report")
        for h in p4["closed_signals"]:
            who = f"{h['owner']} — " if h.get("owner") else ""
            print(f"     {who}{h['url']}  ({h['pattern']})")
    if p1.get("unchecked"):
        print(f"⚠  {len(p1['unchecked'])} URL(s) were NOT actually read — do not cite:")
        for u in p1["unchecked"]:
            print(f"     {u}")
    flagged = [r for r in p2 if "DIFFERENT FEATURE" in (r.get("note") or "")]
    if flagged:
        print(f"⚠  {len(flagged)} pin(s) resolve to a different feature:")
        for r in flagged:
            print(f"     #{r['n']} {r['name']} — {r.get('delta_m','?')} m from {r['reverse']}")
    print(f"\nLocation intent: {p0['intent']} ({p0['columns_that_matter']})")
    print(f"Pins: {len(p2)}   Candidates swept: {p3.get('candidates_found', 0)}   "
          f"Ranked: {len(p3.get('ranked', []))}   Pages scanned: {len(p4.get('scanned', []))}")
    print("\nQuote the RUN ID and the Phase 3 table in your output. "
          "A rating without them was not researched.\n")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except KeyboardInterrupt:
        sys.exit(130)
