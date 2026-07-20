"""
URL checker for Search SBS evaluations.

The checker verifies liveness, extracts page content, and writes durable
per-run evidence files for rating work. It uses a fast requests pass first,
then falls back to Playwright for pages that look blocked, JavaScript-heavy,
or too thin to grade confidently.
"""

from __future__ import annotations

import argparse
import io
import json
import os
import re
import shlex
import socket
import ssl
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import urlparse, quote_plus

# Every third-party import is optional. When one is missing the checker drops to
# a stdlib path instead of crashing, because the evaluation workflows treat
# running this script as a mandatory step.
try:
    import requests
    _HAS_REQUESTS = True
except ImportError:
    requests = None  # type: ignore[assignment]
    _HAS_REQUESTS = False

try:
    from curl_cffi.requests import Session as _CfSession
    _CURL_CFFI = True
except ImportError:
    _CfSession = None  # type: ignore[assignment,misc]
    _CURL_CFFI = False

try:
    from bs4 import BeautifulSoup
    _HAS_BS4 = True
except ImportError:
    BeautifulSoup = None  # type: ignore[assignment,misc]
    _HAS_BS4 = False

try:
    from pypdf import PdfReader
except Exception:  # pragma: no cover - optional at runtime
    PdfReader = None  # type: ignore[assignment]


def _missing_dependencies() -> list[str]:
    missing = []
    if not _HAS_REQUESTS:
        missing.append("requests")
    if not _HAS_BS4:
        missing.append("beautifulsoup4")
    if PdfReader is None:
        missing.append("pypdf")
    return missing


INSTALL_HINT = (
    f"{shlex.quote(sys.executable)} -m pip install requests beautifulsoup4 lxml pypdf curl_cffi"
)


def _degraded_mode_banner() -> str:
    """Explain reduced capability instead of failing, so a run still produces evidence."""
    missing = _missing_dependencies()
    if not missing:
        return ""
    core_missing = not (_HAS_REQUESTS and _HAS_BS4)
    if core_missing:
        lines = [
            "DEGRADED MODE - falling back to the Python standard library.",
            f"  Missing packages: {', '.join(missing)}",
            f"  Install for full extraction quality: {INSTALL_HINT}",
            "  Pages are still fetched and graded, but extraction is coarser and",
            "  low word counts are more likely, so expect more manual-review results.",
        ]
    else:
        lines = [
            f"Optional packages missing: {', '.join(missing)}.",
            "  PDF result pages cannot be read; everything else works normally.",
            f"  Install with: {INSTALL_HINT}",
        ]
    return "\n".join(lines)


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,application/pdf,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

STATUS_MEANING = {
    200: "OK - page responded",
    301: "Permanent redirect - check destination",
    302: "Temporary redirect - check destination",
    401: "Unauthorized - manual review, not automatic CU",
    403: "Forbidden - likely bot-blocking or access control",
    404: "Not found - likely Content Unavailable",
    405: "Method not allowed - manual review, not automatic CU",
    410: "Gone - likely Content Unavailable",
    451: "Unavailable for legal reasons - manual review",
    429: "Rate limited - retry or manual review",
    500: "Server error - likely Content Unavailable",
    502: "Bad gateway - retry or manual review",
    503: "Service unavailable - retry or manual review",
    504: "Gateway timeout - retry or manual review",
}

SCRIPT_DIR = Path(__file__).resolve().parent


def _default_output_base() -> Path:
    """Resolve where run evidence is written.

    The script ships inside the skills repo, but its output is task evidence,
    not source. Prefer the workspace TELUS-TASKS folder so runs never land in
    a git working tree; fall back to the current directory when it is absent.
    """
    for base in (Path.cwd(), *Path.cwd().parents):
        candidate = base / "TELUS-TASKS"
        if candidate.is_dir():
            return (candidate / "url_content").resolve()
    return (Path.cwd() / "url_content").resolve()
SUMMARY_CHARS = 1500
MIN_USEFUL_WORDS = 80
HIGH_CONFIDENCE_WORDS = 200
CU_RETRY_STATUS_CODES = {404, 410, 500}
MANUAL_REVIEW_STATUS_CODES = {401, 403, 405, 429, 451, 502, 503, 504}
# Transient statuses worth a backoff retry before reporting them.
TRANSIENT_STATUS_CODES = {429, 502, 503, 504}
CU_REFRESH_ATTEMPTS = 2
DEFAULT_REQUEST_WORKERS = 4
DEFAULT_TIMEOUT = 20
MAX_RETRY_DELAY = 10.0

# Domains that are open access; a login/paywall match on them is a false positive.
OPEN_ACCESS_DOMAINS = ("wikipedia.org", "wiktionary.org", "nih.gov")


def _retry_delay(response: Any, attempt: int) -> float:
    """Honor Retry-After when the server sends it, else back off exponentially."""
    header = ""
    try:
        header = (response.headers or {}).get("retry-after", "") or ""
    except Exception:
        header = ""
    if header:
        try:
            return min(float(header), MAX_RETRY_DELAY)
        except ValueError:
            pass
    return min(2.0 ** attempt, MAX_RETRY_DELAY)


def _domain_matches(domain: str, suffixes: tuple[str, ...]) -> bool:
    """Match a registrable suffix, so `nih.gov.example.com` does not pass as `nih.gov`."""
    domain = domain.lower().split(":")[0].rstrip(".")
    return any(domain == suffix or domain.endswith("." + suffix) for suffix in suffixes)

PAYWALL_PATTERNS = [
    r"subscribe to (read|continue|access)",
    r"subscription required",
    r"paywall",
    r"premium content",
    r"sign up to read",
    r"create (?:a )?free account",
    r"already a subscriber",
    r"unlock this (article|story)",
    r"members[- ]only",
    r"to continue reading",
]

LOGIN_WALL_PATTERNS = [
    r"log[ -]?in required",
    r"sign in to (continue|read|view|access)",
    r"sign up to (continue|read|view|access)",
    r"create (?:a )?(?:free )?account to (continue|read|view|access)",
    r"must log[ -]?in to view",
    r"log[ -]?in to read the rest",
    r"password required",
    r"already a subscriber",
]

VISIT_LIMIT_PATTERNS = [
    r"you(?:'|’)ve reached your (?:free )?(?:article|visit|view) limit",
    r"you have reached your (?:free )?(?:article|visit|view) limit",
    r"monthly (?:article|visit|view) limit",
    r"free (?:article|visit|view)s? remaining",
    r"limit on (?:the )?number of visits",
    r"continue reading with a subscription",
]

CAPTCHA_PATTERNS = [
    r"\bcaptcha\b",
    r"are you a human",
    r"please verify",
    r"robot check",
    r"unusual traffic",
]

SECURITY_WARNING_PATTERNS = [
    r"your connection is not private",
    r"privacy error",
    r"security warning",
    r"\bnot secure\b",
    r"net::err_cert",
    r"ssl (?:certificate|error)",
    r"certificate (?:is )?(?:invalid|expired|not trusted|not secure)",
    r"this site can(?:not|'t) provide a secure connection",
]

# Matched against the fetch error only, never page text, so wording inside an
# article cannot masquerade as a TLS failure.
TLS_ERROR_PATTERNS = [
    r"ssl/security error",
    r"certificate_verify_failed",
    r"certificate verify failed",
    r"certificate has expired",
    r"self[- ]signed certificate",
    r"hostname mismatch",
    r"unable to get local issuer certificate",
    r"wrong version number",
]

BLOCK_PATTERNS = [
    r"access denied",
    r"checking your browser",
    r"cloudflare",
    r"enable javascript",
    r"forbidden",
    r"just a moment",
    r"not available in your region",
]


def _create_session():
    """Create an HTTP session, with browser TLS impersonation when curl_cffi is available."""
    if _CURL_CFFI and _CfSession is not None:
        return _CfSession(impersonate="chrome")
    if _HAS_REQUESTS:
        return requests.Session()
    return _UrllibSession()


@dataclass
class _Response:
    """Normalized response so the rest of the checker is client-agnostic."""

    status_code: int
    url: str
    headers: dict[str, str]
    content: bytes
    encoding: str = "utf-8"

    @property
    def text(self) -> str:
        return self.content.decode(self.encoding, errors="replace")


class FetchError(Exception):
    """Fetch failure already classified into a human-readable kind."""

    def __init__(self, kind: str, detail: str = ""):
        self.kind = kind
        self.detail = detail
        super().__init__(f"{kind}: {detail}" if detail else kind)


class _UrllibSession:
    """Minimal stdlib stand-in for requests.Session used when requests is absent."""

    def get(self, url: str, headers: dict[str, str], timeout: int, allow_redirects: bool = True):
        request = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                body = response.read()
                return _Response(
                    status_code=response.status,
                    url=response.geturl(),
                    headers={k.lower(): v for k, v in response.headers.items()},
                    content=body,
                    encoding=response.headers.get_content_charset() or "utf-8",
                )
        except urllib.error.HTTPError as exc:
            # An HTTP error status is a real response, not a transport failure.
            body = exc.read() if hasattr(exc, "read") else b""
            return _Response(
                status_code=exc.code,
                url=exc.url if hasattr(exc, "url") else url,
                headers={k.lower(): v for k, v in (exc.headers or {}).items()},
                content=body,
                encoding=(exc.headers.get_content_charset() if exc.headers else None) or "utf-8",
            )
        except urllib.error.URLError as exc:
            reason = exc.reason
            if isinstance(reason, ssl.SSLError):
                raise FetchError("SSL/security error", str(reason)) from exc
            if isinstance(reason, socket.timeout):
                raise FetchError("Timeout") from exc
            raise FetchError("Connection failed", str(reason)) from exc
        except socket.timeout as exc:
            raise FetchError("Timeout") from exc

    def close(self) -> None:
        return None

    def __enter__(self) -> "_UrllibSession":
        return self

    def __exit__(self, *args: Any) -> None:
        return None


def _classify_fetch_exception(exc: Exception) -> FetchError:
    """Map client-specific exceptions onto one vocabulary.

    curl_cffi and urllib do not raise requests' exception types, so without this
    their failures all collapse into an unclassified error string.
    """
    if isinstance(exc, FetchError):
        return exc
    text = str(exc)
    lowered = text.lower()
    if _HAS_REQUESTS:
        if isinstance(exc, requests.exceptions.SSLError):
            return FetchError("SSL/security error", text)
        if isinstance(exc, requests.exceptions.Timeout):
            return FetchError("Timeout")
        if isinstance(exc, requests.exceptions.ConnectionError):
            return FetchError("Connection failed", text)
    if isinstance(exc, ssl.SSLError):
        return FetchError("SSL/security error", text)
    if isinstance(exc, socket.timeout):
        return FetchError("Timeout")
    if "certificate" in lowered or "ssl" in lowered:
        return FetchError("SSL/security error", text)
    if "timed out" in lowered or "timeout" in lowered:
        return FetchError("Timeout")
    if "connection" in lowered or "resolve" in lowered or "dns" in lowered:
        return FetchError("Connection failed", text)
    return FetchError("Fetch failed", text)


class _StdlibHTMLExtractor(HTMLParser):
    """Coarse text/metadata extraction for when BeautifulSoup is unavailable."""

    SKIP_TAGS = {"script", "style", "noscript", "template", "svg", "iframe",
                 "nav", "header", "footer", "aside", "menu", "form"}
    BLOCK_TAGS = {"p", "div", "br", "li", "tr", "section", "article",
                  "h1", "h2", "h3", "h4", "h5", "h6"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.meta_description = ""
        self.canonical_url = ""
        self.language = ""
        self.publication_date = ""
        self.headings: list[str] = []
        self._parts: list[str] = []
        self._skip_depth = 0
        self._in_title = False
        self._heading_tag = ""
        self._heading_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = {key.lower(): (value or "") for key, value in attrs}
        if tag == "html" and attributes.get("lang"):
            self.language = attributes["lang"].strip()
        if tag == "meta":
            name = attributes.get("name", "").lower()
            prop = attributes.get("property", "").lower()
            if name == "description" and not self.meta_description:
                self.meta_description = attributes.get("content", "").strip()
            if prop == "article:published_time" and not self.publication_date:
                self.publication_date = attributes.get("content", "").strip()
        if tag == "time" and attributes.get("datetime") and not self.publication_date:
            self.publication_date = attributes["datetime"].strip()
        if tag == "link" and "canonical" in attributes.get("rel", "").lower():
            self.canonical_url = attributes.get("href", "").strip()
        if tag in self.SKIP_TAGS:
            self._skip_depth += 1
            return
        if self._skip_depth:
            return
        if tag == "title":
            self._in_title = True
        if tag in {"h1", "h2", "h3"}:
            self._heading_tag = tag
            self._heading_parts = []
        if tag in self.BLOCK_TAGS:
            self._parts.append("\n")
        if tag == "li":
            self._parts.append("- ")

    def handle_endtag(self, tag: str) -> None:
        if tag in self.SKIP_TAGS:
            self._skip_depth = max(0, self._skip_depth - 1)
            return
        if self._skip_depth:
            return
        if tag == "title":
            self._in_title = False
        if tag == self._heading_tag:
            heading = re.sub(r"\s+", " ", "".join(self._heading_parts)).strip()
            if heading and len(self.headings) < 30:
                self.headings.append(heading)
            self._heading_tag = ""
            self._heading_parts = []
        if tag in self.BLOCK_TAGS:
            self._parts.append("\n")

    def handle_data(self, data: str) -> None:
        if self._skip_depth:
            return
        if self._in_title:
            self.title += data.strip() + " "
            return
        if self._heading_tag:
            self._heading_parts.append(data)
        self._parts.append(data)

    @property
    def text(self) -> str:
        return _clean_text(_dedupe_lines("".join(self._parts)))


def _extract_html_stdlib(html: str, final_url: str, status_code: int, content_type: str) -> ExtractedContent:
    parser = _StdlibHTMLExtractor()
    try:
        parser.feed(html)
        parser.close()
    except Exception:
        # A malformed document should still yield whatever was parsed so far.
        pass
    return ExtractedContent(
        method="stdlib",
        title=parser.title.strip(),
        meta_description=parser.meta_description,
        canonical_url=parser.canonical_url,
        language=parser.language,
        publication_date=parser.publication_date,
        headings=parser.headings,
        content=parser.text,
        content_type=content_type,
        status_code=status_code,
        final_url=final_url,
        content_length=len(html),
    )


def _wait_for_cloudflare(page, timeout_ms: int = 15000) -> None:
    """Wait for a Cloudflare 'Just a moment...' challenge to auto-resolve."""
    try:
        title = page.title()
        if "just a moment" in title.lower():
            page.wait_for_function(
                "() => !document.title.toLowerCase().includes('just a moment')",
                timeout=timeout_ms,
            )
    except Exception:
        pass


@dataclass
class ExtractedContent:
    method: str
    title: str = ""
    meta_description: str = ""
    canonical_url: str = ""
    language: str = ""
    publication_date: str = ""
    headings: list[str] = field(default_factory=list)
    content: str = ""
    content_type: str = ""
    status_code: int | None = None
    final_url: str = ""
    redirected: bool = False
    content_length: int = 0
    refresh_attempts: int = 0
    status_history: list[int | None] = field(default_factory=list)
    error: str = ""

    @property
    def word_count(self) -> int:
        return len(re.findall(r"\b\w+\b", self.content))


@dataclass
class RequestStage:
    index: int
    url: str
    extracted: ExtractedContent
    assessment: dict[str, Any]


def _sanitize_run_id(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_.-]+", "-", value.strip())
    cleaned = cleaned.strip("-._")
    return cleaned or datetime.now().strftime("%Y%m%d-%H%M%S")


def _make_run_dir(output_base: Path, run_id: str | None) -> Path:
    chosen_run_id = _sanitize_run_id(run_id) if run_id else datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_base / chosen_run_id
    if run_dir.exists():
        suffix = datetime.now().strftime("%f")
        run_dir = output_base / f"{chosen_run_id}-{suffix}"
    run_dir.mkdir(parents=True, exist_ok=False)
    return run_dir


def _clean_text(value: str) -> str:
    value = re.sub(r"\r\n?", "\n", value)
    value = re.sub(r"[ \t]+", " ", value)
    value = re.sub(r"\n{3,}", "\n\n", value)
    return value.strip()


def _dedupe_lines(text: str) -> str:
    seen: set[str] = set()
    lines: list[str] = []
    for raw in text.splitlines():
        line = raw.strip()
        if len(line) < 2:
            continue
        key = re.sub(r"\s+", " ", line).lower()
        if key in seen:
            continue
        seen.add(key)
        lines.append(line)
    return "\n".join(lines)


def _text_has_any(text: str, patterns: list[str]) -> bool:
    haystack = text.lower()
    return any(re.search(pattern, haystack, re.IGNORECASE) for pattern in patterns)


def _make_soup(html: str):
    """Parse with lxml when installed, else the stdlib parser bs4 ships with."""
    try:
        return BeautifulSoup(html, "lxml")
    except Exception:
        return BeautifulSoup(html, "html.parser")


def _extract_html(html: str, final_url: str, status_code: int, content_type: str) -> ExtractedContent:
    if not _HAS_BS4:
        return _extract_html_stdlib(html, final_url, status_code, content_type)

    soup = _make_soup(html)

    for tag in soup(["script", "style", "noscript", "template", "svg", "iframe"]):
        tag.decompose()

    # Remove common layout blocks, but keep body fallback for sites that put all
    # content in divs.
    for selector in ["nav", "header", "footer", "aside", "menu", "form", "[role='navigation']"]:
        for tag in soup.select(selector):
            tag.decompose()

    title = soup.title.get_text(" ", strip=True) if soup.title else ""
    meta_description = ""
    meta = soup.find("meta", attrs={"name": re.compile("^description$", re.I)})
    if meta and meta.get("content"):
        meta_description = str(meta["content"]).strip()

    canonical_url = ""
    canonical = soup.find("link", rel=lambda value: value and "canonical" in value)
    if canonical and canonical.get("href"):
        canonical_url = str(canonical["href"]).strip()

    language = ""
    if soup.html and soup.html.get("lang"):
        language = str(soup.html["lang"]).strip()

    publication_date = ""
    meta_pub = soup.find("meta", property="article:published_time")
    if meta_pub and meta_pub.get("content"):
        publication_date = str(meta_pub["content"]).strip()
    else:
        time_tag = soup.find("time", attrs={"datetime": True})
        if time_tag:
            publication_date = str(time_tag["datetime"]).strip()

    headings = [
        heading.get_text(" ", strip=True)
        for heading in soup.find_all(["h1", "h2", "h3"])
        if heading.get_text(" ", strip=True)
    ][:30]

    for br in soup.find_all("br"):
        br.replace_with("\n")
    for block in soup.find_all(["p", "div", "h1", "h2", "h3", "h4", "h5", "h6", "li"]):
        if block.string is None:
            block.append("\n")
    for li in soup.find_all("li"):
        li.insert_before("- ")

    candidates = []
    for selector in ["main", "article", "[role='main']", ".content", "#content", "body"]:
        candidates.extend(soup.select(selector))

    chunks: list[str] = []
    seen_nodes: set[int] = set()
    for node in candidates:
        node_id = id(node)
        if node_id in seen_nodes:
            continue
        seen_nodes.add(node_id)
        text = node.get_text("\n\n", strip=True)
        if text:
            chunks.append(text)

    content = _clean_text(_dedupe_lines("\n".join(chunks)))
    return ExtractedContent(
        method="requests",
        title=title,
        meta_description=meta_description,
        canonical_url=canonical_url,
        language=language,
        publication_date=publication_date,
        headings=headings,
        content=content,
        content_type=content_type,
        status_code=status_code,
        final_url=final_url,
        content_length=len(html),
    )


def _extract_pdf(data: bytes, final_url: str, status_code: int, content_type: str) -> ExtractedContent:
    if PdfReader is None:
        return ExtractedContent(
            method="requests-pdf",
            final_url=final_url,
            status_code=status_code,
            content_type=content_type,
            content_length=len(data),
            error="pypdf is not available",
        )

    try:
        reader = PdfReader(io.BytesIO(data))
        pages = []
        for page in reader.pages[:30]:
            pages.append(page.extract_text() or "")
        metadata = reader.metadata or {}
        title = str(metadata.get("/Title") or Path(urlparse(final_url).path).name or "PDF document")
        content = _clean_text("\n\n".join(pages))
        return ExtractedContent(
            method="requests-pdf",
            title=title,
            content=content,
            content_type=content_type,
            status_code=status_code,
            final_url=final_url,
            content_length=len(data),
        )
    except Exception as exc:
        return ExtractedContent(
            method="requests-pdf",
            final_url=final_url,
            status_code=status_code,
            content_type=content_type,
            content_length=len(data),
            error=f"PDF extraction failed: {exc}",
        )


def _is_pdf_response(url: str, content_type: str) -> bool:
    path = urlparse(url).path.lower()
    return "application/pdf" in content_type.lower() or path.endswith(".pdf")


def _requests_extract(url: str, session: Any, timeout: int = DEFAULT_TIMEOUT) -> ExtractedContent:
    method = "requests" if _HAS_REQUESTS or _CURL_CFFI else "stdlib"
    responses: list[Any] = []
    for attempt in range(CU_REFRESH_ATTEMPTS + 1):
        headers = dict(HEADERS)
        if attempt:
            headers["Cache-Control"] = "no-cache"
            headers["Pragma"] = "no-cache"
        try:
            response = session.get(url, headers=headers, timeout=timeout, allow_redirects=True)
        except Exception as exc:
            failure = _classify_fetch_exception(exc)
            detail = f"{failure.kind}: {failure.detail}" if failure.detail else failure.kind
            return ExtractedContent(method=method, final_url=url, error=detail)

        responses.append(response)
        status = response.status_code
        if status in TRANSIENT_STATUS_CODES and attempt < CU_REFRESH_ATTEMPTS:
            # Rate limiting and gateway errors often clear on a second try.
            time.sleep(_retry_delay(response, attempt))
            continue
        if status not in CU_RETRY_STATUS_CODES:
            break

    response = responses[-1]
    status_history = [item.status_code for item in responses]
    refresh_attempts = max(0, len(responses) - 1)

    content_type = response.headers.get("content-type", "")
    is_actual_pdf = response.content.lstrip().startswith(b"%PDF")
    if response.status_code == 200 and _is_pdf_response(response.url, content_type) and is_actual_pdf:
        extracted = _extract_pdf(response.content, response.url, response.status_code, content_type)
    elif response.status_code == 200:
        extracted = _extract_html(response.text, response.url, response.status_code, content_type)
    else:
        extracted = ExtractedContent(
            method="requests",
            title=_extract_error_title(response.text),
            content=_clean_text(response.text[:2000]),
            content_type=content_type,
            status_code=response.status_code,
            final_url=response.url,
            content_length=len(response.text),
        )

    extracted.redirected = response.url.rstrip("/") != url.rstrip("/")
    extracted.refresh_attempts = refresh_attempts
    extracted.status_history = status_history
    # Report the client that actually fetched the page, not the parser used.
    extracted.method = f"{method}-pdf" if extracted.method.endswith("-pdf") else method
    return extracted


def _extract_error_title(html: str) -> str:
    try:
        soup = BeautifulSoup(html, "lxml")
        return soup.title.get_text(" ", strip=True) if soup.title else ""
    except Exception:
        return ""


def _playwright_available() -> bool:
    try:
        import playwright.sync_api  # noqa: F401
        return True
    except Exception:
        return False


def _playwright_extract(url: str) -> ExtractedContent:
    try:
        from playwright.sync_api import sync_playwright
    except Exception as exc:
        return ExtractedContent(method="playwright", final_url=url, error=f"Playwright import failed: {exc}")

    try:
        from playwright_stealth import stealth_sync
        _stealth_available = True
    except ImportError:
        _stealth_available = False

    try:
        with sync_playwright() as playwright:
            browser = None
            context = None
            try:
                browser = playwright.chromium.launch(headless=True)
                context = browser.new_context(
                    user_agent=HEADERS["User-Agent"],
                    locale="en-US",
                    viewport={"width": 1365, "height": 900},
                )
                page = context.new_page()
                if _stealth_available:
                    stealth_sync(page)
                response = page.goto(url, wait_until="domcontentloaded", timeout=25000)
                _wait_for_cloudflare(page)
                try:
                    page.wait_for_load_state("networkidle", timeout=5000)
                except Exception:
                    pass

                title = page.title()
                
                # Strip headers/footers to avoid false positive login links
                page.evaluate(
                    """
                    () => {
                      const selectors = ["nav", "header", "footer", "aside", "menu", "form", "[role='navigation']"];
                      selectors.forEach(selector => {
                        document.querySelectorAll(selector).forEach(el => el.remove());
                      });
                    }
                    """
                )
                
                content = page.locator("body").inner_text(timeout=7000)
                metadata = page.evaluate(
                    """
                    () => {
                      const meta = document.querySelector('meta[name="description" i]');
                      const canonical = document.querySelector('link[rel~="canonical" i]');
                      const headings = Array.from(document.querySelectorAll('h1,h2,h3'))
                        .map((el) => el.innerText.trim())
                        .filter(Boolean)
                        .slice(0, 30);
                      const metaPub = document.querySelector('meta[property="article:published_time"]');
                      const timeTag = document.querySelector('time[datetime]');
                      const pubDate = (metaPub ? metaPub.getAttribute('content') : (timeTag ? timeTag.getAttribute('datetime') : '')) || '';
                      return {
                        metaDescription: meta ? meta.getAttribute('content') || '' : '',
                        canonicalUrl: canonical ? canonical.getAttribute('href') || '' : '',
                        language: document.documentElement ? document.documentElement.lang || '' : '',
                        publicationDate: pubDate,
                        headings
                      };
                    }
                    """
                )
                content_type = response.headers.get("content-type", "") if response else ""
                status_code = response.status if response else None
                final_url = page.url
            finally:
                if context:
                    context.close()
                if browser:
                    browser.close()

        return ExtractedContent(
            method="playwright",
            title=title,
            meta_description=metadata.get("metaDescription", ""),
            canonical_url=metadata.get("canonicalUrl", ""),
            language=metadata.get("language", ""),
            publication_date=metadata.get("publicationDate", ""),
            headings=metadata.get("headings", []),
            content=_clean_text(_dedupe_lines(content)),
            content_type=content_type,
            status_code=status_code,
            final_url=final_url,
            redirected=final_url.rstrip("/") != url.rstrip("/"),
            content_length=len(content),
        )
    except Exception as exc:
        return ExtractedContent(method="playwright", final_url=url, error=f"Playwright failed: {exc}")


def _assess(extracted: ExtractedContent) -> dict[str, Any]:
    combined = "\n".join(
        [
            extracted.title,
            extracted.meta_description,
            "\n".join(extracted.headings),
            extracted.content,
            extracted.error,
        ]
    )
    status = extracted.status_code
    captcha = _text_has_any(combined, CAPTCHA_PATTERNS)
    security_warning = _text_has_any(combined, SECURITY_WARNING_PATTERNS)
    if extracted.error and _text_has_any(
        extracted.error, SECURITY_WARNING_PATTERNS + TLS_ERROR_PATTERNS
    ):
        security_warning = True

    # A plain-HTTP page makes browsers show a "Not Secure" label, which the
    # guideline treats as CU/NS. That is an inference about what a browser would
    # display, not an observed warning, so it is tracked separately and always
    # needs manual confirmation rather than becoming an automatic high-confidence CU.
    # Scheme is a fact regardless of whether this particular fetch succeeded, so
    # it is not gated on status or error the way page-text signals are.
    insecure_http = extracted.final_url.lower().startswith("http://")
    visit_limit = _text_has_any(combined, VISIT_LIMIT_PATTERNS)
    login_wall = _text_has_any(combined, LOGIN_WALL_PATTERNS)
    paywall = _text_has_any(combined, PAYWALL_PATTERNS)
    blocked = _text_has_any(combined, BLOCK_PATTERNS)
    word_count = extracted.word_count
    manual_review_status = status in MANUAL_REVIEW_STATUS_CODES

    # Improvement: Clear login_wall flag if word count is sufficiently high
    if login_wall and word_count > 400:
        login_wall = False

    # Improvement: Whitelist globally open access domains
    domain = urlparse(extracted.final_url).netloc.lower()
    if _domain_matches(domain, OPEN_ACCESS_DOMAINS):
        login_wall = False
        paywall = False

    flag_cu = status in CU_RETRY_STATUS_CODES or security_warning or visit_limit
    weak_content = word_count < MIN_USEFUL_WORDS and not flag_cu
    manual_review_reasons: list[str] = []
    likely_cu_reasons: list[str] = []

    if status in CU_RETRY_STATUS_CODES:
        likely_cu_reasons.append(f"status_{status}")
    if security_warning:
        likely_cu_reasons.append("security_warning")
    if visit_limit:
        likely_cu_reasons.append("visit_limit")

    if insecure_http:
        manual_review_reasons.append("insecure_http")
    if extracted.error:
        manual_review_reasons.append("fetch_error")
    if manual_review_status:
        manual_review_reasons.append(f"status_{status}")
    if captcha:
        manual_review_reasons.append("captcha")
    if login_wall:
        manual_review_reasons.append("login_wall")
    if paywall:
        manual_review_reasons.append("paywall")
    if blocked:
        manual_review_reasons.append("blocked_or_bot_check")
    if weak_content:
        manual_review_reasons.append("weak_content")

    manual_review = bool(
        manual_review_reasons
        or security_warning
        or visit_limit
    )

    if flag_cu:
        automation_result = "likely_cu"
    elif manual_review:
        automation_result = "manual_review_needed"
    else:
        automation_result = "accessible"

    if flag_cu:
        confidence = "high"
    elif extracted.error or blocked or word_count < MIN_USEFUL_WORDS:
        confidence = "low"
    elif word_count < HIGH_CONFIDENCE_WORDS:
        confidence = "medium"
    else:
        confidence = "high"

    return {
        "word_count": word_count,
        "captcha_detected": captcha,
        "security_warning_detected": security_warning,
        "insecure_http": insecure_http,
        "visit_limit_detected": visit_limit,
        "login_wall_detected": login_wall,
        "paywall_detected": paywall,
        "block_detected": blocked,
        "weak_content": weak_content,
        "flag_cu_likely": flag_cu,
        "manual_review_required": manual_review,
        "automation_result": automation_result,
        "likely_cu_reasons": likely_cu_reasons,
        "manual_review_reasons": manual_review_reasons,
        "confidence": confidence,
    }


def _needs_playwright(extracted: ExtractedContent, assessment: dict[str, Any]) -> bool:
    if extracted.method == "requests-pdf":
        return False
    if extracted.status_code in (404, 410, 500):
        return False
    return bool(
        extracted.error
        or extracted.status_code in MANUAL_REVIEW_STATUS_CODES
        or assessment["captcha_detected"]
        or assessment["login_wall_detected"]
        or assessment["paywall_detected"]
        or assessment["visit_limit_detected"]
        or assessment["security_warning_detected"]
        or assessment["block_detected"]
        or assessment["weak_content"]
    )


def _safe_domain(url: str) -> str:
    domain = urlparse(url).netloc or "unknown-domain"
    domain = domain.replace("www.", "")
    return re.sub(r"[^\w.-]", "_", domain)


def _write_content_file(run_dir: Path, index: int, url: str, extracted: ExtractedContent, assessment: dict[str, Any]) -> Path:
    path = run_dir / f"{index:02d}_{_safe_domain(url)}.txt"
    lines = [
        f"URL: {url}",
        f"Final URL: {extracted.final_url or url}",
        f"Method: {extracted.method}",
        f"Status: {extracted.status_code if extracted.status_code is not None else 'unknown'}",
        f"Title: {extracted.title}",
        f"Meta Description: {extracted.meta_description}",
        f"Publication Date: {extracted.publication_date}",
        f"Canonical URL: {extracted.canonical_url}",
        f"Language: {extracted.language}",
        f"Content Type: {extracted.content_type}",
        f"Word Count: {assessment['word_count']}",
        f"Confidence: {assessment['confidence']}",
        f"Refresh Attempts: {extracted.refresh_attempts}",
        f"Status History: {', '.join(str(item) for item in extracted.status_history) if extracted.status_history else ''}",
        f"Captcha Detected: {assessment['captcha_detected']}",
        f"Security Warning Detected: {assessment['security_warning_detected']}",
        f"Insecure HTTP (browser shows Not Secure): {assessment['insecure_http']}",
        f"Visit Limit Detected: {assessment['visit_limit_detected']}",
        f"Login Wall Detected: {assessment['login_wall_detected']}",
        f"Paywall Detected: {assessment['paywall_detected']}",
        f"Block Detected: {assessment['block_detected']}",
        f"Manual Review Required: {assessment['manual_review_required']}",
        f"Likely CU: {assessment['flag_cu_likely']}",
        f"Automation Result: {assessment['automation_result']}",
        f"Likely CU Reasons: {', '.join(assessment['likely_cu_reasons'])}",
        f"Manual Review Reasons: {', '.join(assessment['manual_review_reasons'])}",
    ]
    if extracted.error:
        lines.append(f"Error: {extracted.error}")
    if extracted.headings:
        lines.append("Headings:")
        lines.extend(f"- {heading}" for heading in extracted.headings[:30])
    lines.extend(["=" * 80, "", extracted.content or "[No extractable content]"])
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def _requests_stage(index: int, url: str, timeout: int = DEFAULT_TIMEOUT) -> RequestStage:
    with _create_session() as session:
        extracted = _requests_extract(url, session, timeout=timeout)
    return RequestStage(index=index, url=url, extracted=extracted, assessment=_assess(extracted))


def _get_query_preview(content: str, query: str, summary_chars: int = 1500) -> str:
    if not query:
        return content[:summary_chars]
    
    query_terms = [t.lower() for t in re.findall(r"[A-Za-z0-9'-]+", query)]
    if not query_terms:
        return content[:summary_chars]
        
    lower_content = content.lower()
    best_idx = -1
    
    exact_idx = lower_content.find(query.lower())
    if exact_idx != -1:
        best_idx = exact_idx
    else:
        for term in query_terms:
            idx = lower_content.find(term)
            if idx != -1:
                if best_idx == -1 or idx < best_idx:
                    best_idx = idx
                    
    if best_idx == -1:
        return content[:summary_chars]
        
    start = max(0, best_idx - 150)
    if start > 0:
        space_idx = content.find(" ", start)
        if space_idx != -1 and space_idx < best_idx:
            start = space_idx + 1
            
    end = min(len(content), start + summary_chars)
    preview = content[start:end]
    return ("... " if start > 0 else "") + preview + (" ..." if end < len(content) else "")


def check_url(
    url: str,
    index: int,
    run_dir: Path,
    session: requests.Session | None = None,
    use_playwright: bool = True,
    first: ExtractedContent | None = None,
    assessment: dict[str, Any] | None = None,
    query: str = "",
) -> dict[str, Any]:
    owns_session = session is None
    if first is None or assessment is None:
        session = session or _create_session()
        try:
            first = _requests_extract(url, session)
            assessment = _assess(first)
        finally:
            if owns_session:
                session.close()

    used_fallback = False
    fallback_error = ""

    extracted = first
    # Only attempt the browser pass if Playwright is actually installed, so a
    # missing optional dependency never lands in the record as a page error.
    if use_playwright and _playwright_available() and _needs_playwright(first, assessment):
        fallback = _playwright_extract(url)
        fallback_assessment = _assess(fallback)
        used_fallback = True
        fallback_error = fallback.error

        first_words = assessment["word_count"]
        fallback_words = fallback_assessment["word_count"]
        fallback_is_better = (
            not fallback.error
            and not fallback_assessment["block_detected"]
            and not fallback_assessment["captcha_detected"]
            and not fallback_assessment["security_warning_detected"]
            and not fallback_assessment["visit_limit_detected"]
            and fallback_words >= max(first_words, MIN_USEFUL_WORDS)
        )
        if fallback_is_better:
            first_security_warning = assessment["security_warning_detected"]
            extracted = fallback
            assessment = fallback_assessment
            if first_security_warning and not assessment["security_warning_detected"]:
                # The fast pass hit a real TLS failure. A browser that renders the
                # page anyway does not disprove the bad certificate, and the user
                # would still meet the warning, so the finding has to survive.
                assessment["security_warning_detected"] = True
                if "security_warning" not in assessment["likely_cu_reasons"]:
                    assessment["likely_cu_reasons"].append("security_warning")
                assessment["flag_cu_likely"] = True
                assessment["automation_result"] = "likely_cu"
                assessment["confidence"] = "high"
        else:
            assessment["manual_review_required"] = True
            if fallback_error and not extracted.error:
                extracted.error = fallback_error

    content_file = _write_content_file(run_dir, index, url, extracted, assessment)
    status = extracted.status_code
    record: dict[str, Any] = {
        "index": index,
        "url": url,
        "domain": urlparse(url).netloc,
        "final_url": extracted.final_url or url,
        "redirected": extracted.redirected,
        "status_code": status,
        "status_meaning": STATUS_MEANING.get(status, "Unknown") if status else "Unknown",
        "title": extracted.title,
        "meta_description": extracted.meta_description,
        "canonical_url": extracted.canonical_url,
        "language": extracted.language,
        "content_type": extracted.content_type,
        "content_length": extracted.content_length,
        "refresh_attempts": extracted.refresh_attempts,
        "status_history": extracted.status_history,
        "word_count": assessment["word_count"],
        "extraction_method": extracted.method,
        "used_playwright_fallback": used_fallback,
        "confidence": assessment["confidence"],
        "captcha_detected": assessment["captcha_detected"],
        "security_warning_detected": assessment["security_warning_detected"],
        "insecure_http": assessment["insecure_http"],
        "visit_limit_detected": assessment["visit_limit_detected"],
        "login_wall_detected": assessment["login_wall_detected"],
        "paywall_detected": assessment["paywall_detected"],
        "block_detected": assessment["block_detected"],
        "weak_content": assessment["weak_content"],
        "flag_cu_likely": assessment["flag_cu_likely"],
        "manual_review_required": assessment["manual_review_required"],
        "automation_result": assessment["automation_result"],
        "likely_cu_reasons": assessment["likely_cu_reasons"],
        "manual_review_reasons": assessment["manual_review_reasons"],
        "error": extracted.error,
        "fallback_error": fallback_error,
        "content_file": str(content_file),
        "content_summary": _get_query_preview(extracted.content, query, SUMMARY_CHARS),
        "publication_date": extracted.publication_date,
    }
    return record


def _query_pattern(query: str) -> str:
    terms = re.findall(r"[A-Za-z0-9][A-Za-z0-9'-]{2,}", query)
    terms = [re.escape(term) for term in terms[:5]]
    return "|".join(terms) if terms else "your keyword"


def check_urls(
    urls: list[str],
    query: str = "",
    run_id: str | None = None,
    output_dir: str | None = None,
    use_playwright: bool = True,
    workers: int = DEFAULT_REQUEST_WORKERS,
    timeout: int = DEFAULT_TIMEOUT,
) -> Path:
    output_base = Path(output_dir).resolve() if output_dir else _default_output_base()
    run_dir = _make_run_dir(output_base, run_id)
    request_workers = max(1, min(workers, len(urls))) if urls else 1

    print("\n" + "=" * 80)
    print("URL VERIFICATION REPORT")
    print("=" * 80)
    banner = _degraded_mode_banner()
    if banner:
        print(banner)
        print()
    print(f"Run folder: {run_dir}")
    if query:
        print(f"Query: {query}")
        print(f"Google: https://www.google.com/search?q={quote_plus(query)}")
        print(f"Bing: https://www.bing.com/search?q={quote_plus(query)}")
    print(f"Request workers: {request_workers}")
    if use_playwright and _playwright_available():
        print("Playwright fallback: enabled, serial")
    elif use_playwright:
        print("Playwright fallback: unavailable (not installed) - blocked or JS-heavy pages stay manual review")
    else:
        print("Playwright fallback: disabled")
    print()

    request_stages: dict[int, RequestStage] = {}
    if request_workers == 1:
        for index, url in enumerate(urls, 1):
            request_stages[index] = _requests_stage(index, url, timeout)
    else:
        with ThreadPoolExecutor(max_workers=request_workers) as executor:
            futures = {
                executor.submit(_requests_stage, index, url, timeout): (index, url)
                for index, url in enumerate(urls, 1)
            }
            for future in as_completed(futures):
                index, url = futures[future]
                try:
                    request_stages[index] = future.result()
                except Exception as exc:
                    extracted = ExtractedContent(
                        method="requests",
                        final_url=url,
                        error=f"Request worker failed: {exc}",
                    )
                    request_stages[index] = RequestStage(
                        index=index,
                        url=url,
                        extracted=extracted,
                        assessment=_assess(extracted),
                    )

    records = []
    for index, url in enumerate(urls, 1):
        stage = request_stages[index]
        record = check_url(
            url,
            index,
            run_dir,
            session=None,
            use_playwright=use_playwright,
            first=stage.extracted,
            assessment=stage.assessment,
            query=query,
        )
        records.append(record)
        _print_record(record)

    _print_summary(records)

    report = {
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "query": query,
        "run_dir": str(run_dir),
        "playwright_fallback_enabled": use_playwright,
        "request_workers": request_workers,
        "timeout_seconds": timeout,
        # True only when the stdlib fallback was used for fetching/parsing.
        "degraded_mode": not (_HAS_REQUESTS and _HAS_BS4),
        "missing_dependencies": _missing_dependencies(),
        "urls": records,
    }
    report_path = run_dir / "report.json"
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    print("=" * 80)
    print(f"Report saved to: {report_path}")
    print(f"Full extracted content saved to: {run_dir}")
    print(f"Search content with: {_search_hint(run_dir, query)}")
    return run_dir


def _search_hint(run_dir: Path, query: str) -> str:
    """Give a search command the current shell can actually run."""
    pattern = _query_pattern(query)
    if os.name == "nt":
        return f'Select-String -Path "{run_dir}\\*.txt" -Pattern "{pattern}" -Context 2,2'
    return (
        f"grep -rEi -C 2 --include='*.txt' {shlex.quote(pattern)} {shlex.quote(str(run_dir))}"
    )


def _print_summary(records: list[dict[str, Any]]) -> None:
    buckets = {
        "accessible": [],
        "manual_review_needed": [],
        "likely_cu": [],
    }
    for record in records:
        buckets.setdefault(record["automation_result"], []).append(record)

    print("-" * 80)
    print("Automation summary")
    for label, heading in [
        ("accessible", "Accessible"),
        ("manual_review_needed", "Needs manual review"),
        ("likely_cu", "Likely CU"),
    ]:
        items = buckets.get(label, [])
        indexes = ", ".join(str(item["index"]) for item in items) or "none"
        print(f"    {heading}: {indexes}")

    if buckets.get("manual_review_needed"):
        print(
            "    Manual review means the checker could not confirm the page. "
            "Do not mark CU unless a browser/manual check also shows unavailable content."
        )
    print("-" * 80)


def _print_record(record: dict[str, Any]) -> None:
    status = record["status_code"] if record["status_code"] is not None else "unknown"
    print(f"[{record['index']}] {record['domain'] or 'unknown-domain'}")
    print(f"    URL: {record['url']}")
    print(f"    Status: {status} - {record['status_meaning']}")
    print(f"    Method: {record['extraction_method']}")
    if record["used_playwright_fallback"]:
        print("    Playwright fallback: used")
    if record["redirected"]:
        print(f"    Redirected to: {record['final_url']}")
    if record["title"]:
        print(f"    Title: {record['title']}")
    if record.get("publication_date"):
        print(f"    Publication Date: {record['publication_date']}")
    print(f"    Word Count: {record['word_count']} ({record['confidence']} confidence)")
    print(f"    Automation Result: {record['automation_result']}")
    if record["refresh_attempts"]:
        history = ", ".join(str(item) for item in record["status_history"])
        print(f"    Refresh/retry attempts: {record['refresh_attempts']} (status history: {history})")
    print(f"    Content file: {record['content_file']}")

    if record["security_warning_detected"]:
        print("    SECURITY WARNING DETECTED - guideline CU/NS if confirmed in browser")
    if record.get("insecure_http"):
        print(
            "    PLAIN HTTP - browsers label this 'Not Secure'. Confirm in a browser, "
            "then flag CU/NS per guideline. Not a CU on this signal alone."
        )
    if record["visit_limit_detected"]:
        print("    VISIT LIMIT DETECTED - guideline CU/NS if confirmed in browser")
    if record["captcha_detected"]:
        print("    CAPTCHA DETECTED - solve manually, then grade visible page")
    if record["login_wall_detected"]:
        print("    LOGIN WALL DETECTED - try to close/bypass manually; CU if content remains blocked")
    if record["paywall_detected"]:
        print("    PAYWALL DETECTED - verify access manually")
    if record["flag_cu_likely"]:
        reasons = ", ".join(record["likely_cu_reasons"]) or "guideline CU signal"
        print(f"    FLAG CU: likely ({reasons})")
    if record["manual_review_required"]:
        reasons = ", ".join(record["manual_review_reasons"]) or "automation could not confirm"
        print(f"    MANUAL REVIEW REQUIRED ({reasons}) - do not flag CU from automation alone")
    if record["error"]:
        print(f"    Error: {record['error']}")

    summary = record["content_summary"]
    if summary:
        print("    CONTENT PREVIEW:")
        preview = summary[:SUMMARY_CHARS]
        for line in preview.splitlines()[:10]:
            stripped = line.strip()
            if stripped:
                print(f"       {stripped}")
        if len(summary) >= SUMMARY_CHARS:
            print("       [TRUNCATED]")
    print()


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check URL liveness and extract page content for Search SBS evaluations.",
    )
    parser.add_argument("urls", nargs="*", help="URLs to verify.")
    parser.add_argument("--query", default="", help="Optional query text to store in report.json.")
    parser.add_argument("--run-id", default=None, help="Optional run folder name under the output directory.")
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Base directory for per-run output folders. Defaults to the workspace TELUS-TASKS/url_content.",
    )
    parser.add_argument(
        "--no-playwright",
        action="store_true",
        help="Disable automatic Playwright fallback for weak or blocked pages.",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=DEFAULT_REQUEST_WORKERS,
        help=(
            "Number of concurrent request workers for the fast extraction pass. "
            f"Playwright fallback stays serial. Default: {DEFAULT_REQUEST_WORKERS}."
        ),
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT,
        help=f"Per-request timeout in seconds. Default: {DEFAULT_TIMEOUT}.",
    )
    parser.add_argument(
        "--check-deps",
        action="store_true",
        help="Report which optional packages are installed, then exit.",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    args = parse_args(argv)

    if args.check_deps:
        for name, present in [
            ("requests", _HAS_REQUESTS),
            ("beautifulsoup4", _HAS_BS4),
            ("curl_cffi (bot-block evasion)", _CURL_CFFI),
            ("pypdf (PDF pages)", PdfReader is not None),
            ("playwright (JS-heavy pages)", _playwright_available()),
        ]:
            print(f"  {'OK      ' if present else 'MISSING '} {name}")
        if _missing_dependencies():
            print(f"\nInstall with: {INSTALL_HINT}")
        else:
            print("\nAll core dependencies present.")
        return 0

    if not args.urls:
        print(
            "Usage: python check_urls.py [--query QUERY] [--run-id RUN_ID] "
            "[--output-dir DIR] [--workers N] [--timeout S] <url1> <url2> ..."
        )
        print("No URLs provided. Pass URLs as arguments.")
        return 0

    duplicates = len(args.urls) - len(set(args.urls))
    if duplicates:
        print(
            f"Note: {duplicates} duplicate URL(s) passed. Each is still checked and "
            "numbered separately so positions line up with the result list."
        )

    check_urls(
        args.urls,
        query=args.query,
        run_id=args.run_id,
        output_dir=args.output_dir,
        use_playwright=not args.no_playwright,
        workers=args.workers,
        timeout=args.timeout,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
