"""
Straight-line distance helper for TELUS Maps Search evaluations.

Maps relevance demotions turn on how far a result sits from the user or the
viewport edge, and eyeballing that from coordinates invites arithmetic slips.
This computes the great-circle distance deterministically so the number in an
evaluation note is one you can defend.

It informs a rating. It never decides one: distance is only one input, and
density of real-world candidates sets the scale for what counts as far.

No network access, no dependencies beyond the standard library.

    python3 maps_distance.py 37.3861,-122.0839 37.4419,-122.1430
    python3 maps_distance.py --label "user->result 1" 40.7580,-73.9855 40.6892,-74.0445
    python3 maps_distance.py --batch pairs.txt
    python3 maps_distance.py --format json 51.5007,-0.1246 48.8584,2.2945

Batch input is one pair per line, optionally prefixed with a label and a colon:

    user->Starbucks A: 37.3861,-122.0839 37.4419,-122.1430
    37.3861,-122.0839 37.3900,-122.0800
"""

from __future__ import annotations

import argparse
import json
import math
import sys

# Mean Earth radius (IUGG). Great-circle distance on a sphere of this radius is
# within ~0.3% of the true ellipsoidal distance, which is far tighter than any
# threshold the Maps rubric asks you to judge.
#
# Verified against independent implementations and closed-form values:
#   1 deg longitude at equator  111.195 km  (= 2*pi*R/360, exact)
#   equator -> north pole     10007.557 km  (quarter meridian, exact)
#   Big Ben -> Eiffel Tower     340.539 km  (spherical law of cosines: 340.539;
#                                            Vincenty ellipsoidal: 340.895, +0.10%)
#   JFK -> LAX                 3974.342 km
EARTH_RADIUS_KM = 6371.0088
KM_PER_MILE = 1.609344

LAT_RANGE = (-90.0, 90.0)
LNG_RANGE = (-180.0, 180.0)


class CoordinateError(ValueError):
    """Raised when a coordinate string is missing, malformed, or out of range."""


def parse_coordinate(raw: str) -> tuple[float, float]:
    """Parse a "lat,lng" string into a validated (lat, lng) pair."""
    if raw is None:
        raise CoordinateError("coordinate is missing")

    text = raw.strip().strip("()[]")
    if not text:
        raise CoordinateError("coordinate is empty")

    # Accept "lat,lng", "lat, lng", and whitespace-separated forms.
    parts = [p for p in text.replace(",", " ").split() if p]
    if len(parts) != 2:
        raise CoordinateError(
            f"expected 'lat,lng' with exactly two values, got {raw!r}"
        )

    try:
        lat, lng = float(parts[0]), float(parts[1])
    except ValueError:
        raise CoordinateError(f"non-numeric coordinate: {raw!r}") from None

    if not math.isfinite(lat) or not math.isfinite(lng):
        raise CoordinateError(f"coordinate is not a finite number: {raw!r}")
    if not LAT_RANGE[0] <= lat <= LAT_RANGE[1]:
        raise CoordinateError(f"latitude {lat} is outside {LAT_RANGE}")
    if not LNG_RANGE[0] <= lng <= LNG_RANGE[1]:
        raise CoordinateError(f"longitude {lng} is outside {LNG_RANGE}")

    return lat, lng


def haversine_km(start: tuple[float, float], end: tuple[float, float]) -> float:
    """Great-circle distance in kilometres between two validated coordinates."""
    lat1, lng1 = math.radians(start[0]), math.radians(start[1])
    lat2, lng2 = math.radians(end[0]), math.radians(end[1])

    dlat = lat2 - lat1
    dlng = lng2 - lng1

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlng / 2) ** 2
    return 2 * EARTH_RADIUS_KM * math.asin(math.sqrt(min(1.0, a)))


def format_distance(km: float) -> tuple[str, str]:
    """Render km and miles at a precision that matches the scale being judged."""
    miles = km / KM_PER_MILE
    if km < 1:
        return f"{km * 1000:.0f} m", f"{miles * 5280:.0f} ft"
    if km < 100:
        return f"{km:.2f} km", f"{miles:.2f} mi"
    return f"{km:,.1f} km", f"{miles:,.1f} mi"


def measure(start_raw: str, end_raw: str, label: str | None = None) -> dict:
    """Measure one pair, returning a result dict that always reports its status."""
    entry: dict = {"label": label, "start": start_raw, "end": end_raw}
    try:
        start = parse_coordinate(start_raw)
        end = parse_coordinate(end_raw)
    except CoordinateError as exc:
        entry.update(status="error", error=str(exc))
        return entry

    km = haversine_km(start, end)
    km_text, mi_text = format_distance(km)
    entry.update(
        status="ok",
        start_lat=start[0], start_lng=start[1],
        end_lat=end[0], end_lng=end[1],
        km=round(km, 6),
        miles=round(km / KM_PER_MILE, 6),
        km_text=km_text,
        miles_text=mi_text,
    )
    return entry


def parse_batch_line(line: str) -> tuple[str | None, str, str] | None:
    """Parse one batch line into (label, start, end). Returns None for blanks."""
    text = line.strip()
    if not text or text.startswith("#"):
        return None

    label = None
    # A label is everything before a colon that is not part of a coordinate.
    if ":" in text:
        head, _, tail = text.partition(":")
        if tail.strip():
            label, text = head.strip(), tail.strip()

    parts = text.split()
    if len(parts) == 4:  # "lat lng lat lng" with space separators
        return label, f"{parts[0]},{parts[1]}", f"{parts[2]},{parts[3]}"
    if len(parts) == 2:
        return label, parts[0], parts[1]
    raise CoordinateError(f"cannot read a coordinate pair from: {line.strip()!r}")


def render_text(results: list[dict]) -> str:
    lines = []
    for r in results:
        name = r["label"] or f"{r['start']} -> {r['end']}"
        if r["status"] == "error":
            lines.append(f"{name}: UNABLE TO MEASURE - {r['error']}")
        else:
            lines.append(f"{name}: {r['km_text']} ({r['miles_text']})")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Straight-line distance between coordinates, for Maps evaluation notes.",
        epilog="Distance informs a relevance demotion; it never decides one.",
    )
    parser.add_argument("coords", nargs="*", help="Two coordinates: 'lat,lng' 'lat,lng'.")
    parser.add_argument("--label", help="Name for this measurement in the output.")
    parser.add_argument(
        "--batch",
        help="File of pairs, one per line, optionally 'label: lat,lng lat,lng'. Use - for stdin.",
    )
    parser.add_argument(
        "--format", choices=("text", "json"), default="text",
        help="Output format (default: text).",
    )
    args = parser.parse_args(argv)

    results: list[dict] = []
    exit_code = 0

    if args.batch:
        stream = sys.stdin if args.batch == "-" else open(args.batch, encoding="utf-8")
        try:
            for lineno, line in enumerate(stream, 1):
                try:
                    parsed = parse_batch_line(line)
                except CoordinateError as exc:
                    results.append({
                        "label": f"line {lineno}", "start": None, "end": None,
                        "status": "error", "error": str(exc),
                    })
                    exit_code = 1
                    continue
                if parsed is None:
                    continue
                label, start, end = parsed
                entry = measure(start, end, label or f"line {lineno}")
                if entry["status"] == "error":
                    exit_code = 1
                results.append(entry)
        finally:
            if stream is not sys.stdin:
                stream.close()
    else:
        if len(args.coords) == 4:  # tolerate space-separated "lat lng lat lng"
            args.coords = [
                f"{args.coords[0]},{args.coords[1]}",
                f"{args.coords[2]},{args.coords[3]}",
            ]
        if len(args.coords) != 2:
            parser.error("provide exactly two coordinates, or use --batch")
        entry = measure(args.coords[0], args.coords[1], args.label)
        if entry["status"] == "error":
            exit_code = 1
        results.append(entry)

    if args.format == "json":
        print(json.dumps(results, indent=2))
    else:
        print(render_text(results))

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
