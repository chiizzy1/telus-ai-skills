"""
App Store metadata fetcher for Search Ads Relevance evaluations.

Pulls the five fields that skill requires for its research table (App Name,
Developer, Category, Rating, Review Count) straight from the structured data
Apple embeds in each listing, so the numbers do not have to be read out of page
prose where a rating and a review count are easy to confuse.

Takes App Store URLs or bare numeric app IDs and prints a ready-to-paste table.
It writes nothing to disk.

    python3 fetch_app_meta.py 284876795 6480136315
    python3 fetch_app_meta.py --storefront gb https://apps.apple.com/gb/app/id284876795
    python3 fetch_app_meta.py --format json 284876795
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.request
from typing import Any

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
)
DEFAULT_STOREFRONT = "us"
DEFAULT_TIMEOUT = 20

# Apple throttles back-to-back listing requests, so batches pace themselves.
RETRY_STATUS_CODES = {429, 503}
RETRY_ATTEMPTS = 4
RETRY_BASE_DELAY = 2.0
MAX_RETRY_DELAY = 15.0
REQUEST_SPACING = 1.0

# Apple tags the listing's structured data with this id; the looser pattern is a
# fallback for when the markup shifts.
LD_JSON_TAGGED = re.compile(
    r'<script id=["\']?software-application["\']?[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
    re.DOTALL | re.IGNORECASE,
)
LD_JSON_ANY = re.compile(
    r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
    re.DOTALL | re.IGNORECASE,
)
APP_ID = re.compile(r"id(\d{6,})")


def resolve_url(value: str, storefront: str) -> str:
    """Accept a full listing URL or a bare app id."""
    value = value.strip()
    if value.startswith("http://") or value.startswith("https://"):
        return value
    match = APP_ID.search(value) or re.fullmatch(r"\d{6,}", value)
    app_id = match.group(1) if match and match.groups() else value
    return f"https://itunes.apple.com/{storefront}/app/id{app_id}"


def format_review_count(count: Any) -> str:
    """Match the skill's rule: 4.7K for thousands, 1.2M for millions, raw under 1000."""
    if not isinstance(count, int):
        return str(count) if count else ""
    if count >= 1_000_000:
        return f"{count / 1_000_000:.1f}M"
    if count >= 1_000:
        return f"{count / 1_000:.1f}K"
    return str(count)


def parse_listing(html: str) -> dict[str, Any] | None:
    for pattern in (LD_JSON_TAGGED, LD_JSON_ANY):
        for raw in pattern.findall(html):
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                continue
            if isinstance(data, list):
                data = next(
                    (d for d in data if isinstance(d, dict) and d.get("name")), None
                )
            if isinstance(data, dict) and data.get("name"):
                return data
    return None


def fetch(url: str, timeout: int) -> dict[str, Any]:
    record: dict[str, Any] = {"url": url, "error": ""}
    html = ""
    # Apple rate-limits back-to-back listing requests, so a batch needs retries.
    for attempt in range(RETRY_ATTEMPTS):
        try:
            request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(request, timeout=timeout) as response:
                html = response.read().decode("utf-8", errors="replace")
            record["error"] = ""
            break
        except urllib.error.HTTPError as exc:
            record["error"] = f"HTTP {exc.code}"
            if exc.code not in RETRY_STATUS_CODES or attempt == RETRY_ATTEMPTS - 1:
                return record
            retry_after = (exc.headers or {}).get("Retry-After", "")
            try:
                delay = min(float(retry_after), MAX_RETRY_DELAY)
            except (TypeError, ValueError):
                delay = min(RETRY_BASE_DELAY * (2 ** attempt), MAX_RETRY_DELAY)
            time.sleep(delay)
        except Exception as exc:  # network, DNS, TLS, timeout
            record["error"] = str(exc)
            return record

    if record["error"] or not html:
        return record

    data = parse_listing(html)
    if data is None:
        record["error"] = "listing data not found in page"
        return record

    rating = data.get("aggregateRating") or {}
    record.update(
        {
            "name": data.get("name", "N/A"),
            "developer": (data.get("author") or {}).get("name", "N/A"),
            "category": data.get("applicationCategory", "N/A"),
            "rating": rating.get("ratingValue", ""),
            "review_count": rating.get("reviewCount", ""),
        }
    )
    return record


def rating_cell(record: dict[str, Any]) -> str:
    """Render as the skill's table expects: 4.8★, 477.3K."""
    rating = record.get("rating")
    reviews = format_review_count(record.get("review_count"))
    if rating in ("", None):
        return "No rating"
    cell = f"{rating}★"
    return f"{cell}, {reviews}" if reviews else cell


def print_table(records: list[dict[str, Any]]) -> None:
    print("| # | App | Developer | Category |")
    print("| :--- | :--- | :--- | :--- |")
    for index, record in enumerate(records, 1):
        if record["error"]:
            print(f"| {index} | **Fetch failed** | | {record['error']} |")
            continue
        print(
            f"| {index} | **{record['name']}** | {record['developer']} | "
            f"{record['category']} ({rating_cell(record)}) |"
        )
    failures = [r for r in records if r["error"]]
    if failures:
        print()
        print("Could not fetch:")
        for record in failures:
            print(f"- {record['url']}: {record['error']}")
        print(
            "Verify these listings with your URL-fetch tool before rating. "
            "Do not report a field you did not actually read."
        )


def print_lines(records: list[dict[str, Any]]) -> None:
    for record in records:
        if record["error"]:
            print(f"Error fetching {record['url']}: {record['error']}")
        else:
            print(
                f"{record['name']} | {record['developer']} | "
                f"{record['category']} ({rating_cell(record)})"
            )


def main(argv: list[str]) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(
        description="Fetch App Store metadata for Search Ads Relevance research."
    )
    parser.add_argument("apps", nargs="*", help="App Store URLs or bare numeric app IDs.")
    parser.add_argument(
        "--storefront",
        default=DEFAULT_STOREFRONT,
        help=f"Two-letter storefront for bare IDs, matching the task locale. Default: {DEFAULT_STOREFRONT}.",
    )
    parser.add_argument(
        "--format",
        choices=["table", "line", "json"],
        default="table",
        help="table: the skill's research table (default). line: one row per app. json: raw fields.",
    )
    parser.add_argument(
        "--timeout", type=int, default=DEFAULT_TIMEOUT, help=f"Seconds per request. Default: {DEFAULT_TIMEOUT}."
    )
    args = parser.parse_args(argv)

    if not args.apps:
        print("Usage: python3 fetch_app_meta.py [--storefront xx] [--format table|line|json] <url-or-id> ...")
        print("No apps provided. Pass App Store URLs or numeric app IDs as arguments.")
        return 0

    records = []
    for position, app in enumerate(args.apps):
        if position:
            time.sleep(REQUEST_SPACING)
        records.append(fetch(resolve_url(app, args.storefront), args.timeout))

    if args.format == "json":
        print(json.dumps(records, indent=2, ensure_ascii=False))
    elif args.format == "line":
        print_lines(records)
    else:
        print_table(records)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
