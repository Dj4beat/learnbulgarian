#!/usr/bin/env python3
"""Submit bg60day.com URLs to IndexNow.

Reads the public key from the site-root ``<key>.txt`` file and, by default,
URLs from ``sitemap.xml``. The command is a dry run until ``--send`` is
passed. Optional positional paths are submitted instead of the sitemap.

HTTP 200 and 202 are success. HTTP 403 and 422 print a warning (the key file
may not be reachable yet) and do not raise. Other failures print a warning
and return a non-zero status; callers that deploy the site must ignore that
status.

Usage:
    python tools/indexnow.py
    python tools/indexnow.py --send
    python tools/indexnow.py --send day01.html index.html
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

HOST = "bg60day.com"
ENDPOINT = "https://api.indexnow.org/indexnow"
SITEMAP_NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
MAX_URLS = 10_000
SUCCESS_CODES = {200, 202}
WARNING_CODES = {403, 422}

ROOT = Path(__file__).resolve().parent.parent


def find_key_file(root: Path | None = None) -> Path | None:
    """Return the single site-root IndexNow key file, or None."""
    root = root or ROOT
    matches: list[Path] = []
    for path in sorted(root.iterdir()):
        if not path.is_file():
            continue
        stem = path.stem
        if path.suffix != ".txt" or len(stem) != 32:
            continue
        if stem != stem.lower() or any(c not in "0123456789abcdef" for c in stem):
            continue
        if path.read_bytes() != stem.encode("ascii"):
            continue
        matches.append(path)
    if not matches:
        return None
    if len(matches) > 1:
        names = ", ".join(path.name for path in matches)
        print(f"warning: more than one IndexNow key file at the site root ({names})")
        return None
    return matches[0]


def read_key(root: Path | None = None) -> str:
    path = find_key_file(root)
    if path is None:
        raise FileNotFoundError(
            "IndexNow key file not found at the site root "
            "(expected one <32 lowercase hex>.txt whose contents are the key)"
        )
    return path.stem


def sitemap_urls(root: Path | None = None) -> list[str]:
    """Return ``<loc>`` values from sitemap.xml, in document order."""
    root = root or ROOT
    sitemap = root / "sitemap.xml"
    tree = ET.parse(sitemap)
    urls: list[str] = []
    for element in tree.findall(".//sm:loc", SITEMAP_NS):
        if element.text and element.text.strip():
            urls.append(element.text.strip())
    if not urls:
        for element in tree.iter():
            if element.tag.endswith("loc") and element.text and element.text.strip():
                urls.append(element.text.strip())
    return _dedupe(urls)


def paths_to_urls(paths: list[str]) -> list[str]:
    """Turn CLI paths into absolute bg60day.com URLs. Full URLs pass through."""
    urls: list[str] = []
    for raw in paths:
        text = raw.strip()
        if not text:
            continue
        if "://" in text:
            urls.append(text)
            continue
        rel = text.replace("\\", "/").lstrip("/")
        urls.append(f"https://{HOST}/{rel}")
    return _dedupe(urls)


def submit(
    urls: list[str] | None = None,
    *,
    send: bool = False,
    root: Path | None = None,
) -> int:
    """Submit ``urls`` (or the sitemap, when ``urls`` is None).

    Returns 0 for a dry run, a successful response, or a 403/422 warning.
    Returns 1 for other failures. Does not raise for HTTP or network errors.
    """
    root = root or ROOT
    try:
        key = read_key(root)
    except FileNotFoundError as exc:
        print(f"warning: {exc}")
        return 1

    if urls is None:
        try:
            urls = sitemap_urls(root)
        except (ET.ParseError, OSError) as exc:
            print(f"warning: could not read sitemap.xml ({exc})")
            return 1

    urls = _dedupe(urls)
    key_location = f"https://{HOST}/{key}.txt"
    if not urls:
        print("IndexNow: no URLs to submit")
        return 0

    if not send:
        print("IndexNow dry run (nothing sent)")
        print(f"host: {HOST}")
        print(f"keyLocation: {key_location}")
        print(f"urls: {len(urls)}")
        for url in urls:
            print(f"  {url}")
        print("Pass --send to submit these URLs.")
        return 0

    exit_code = 0
    for start in range(0, len(urls), MAX_URLS):
        batch = urls[start : start + MAX_URLS]
        payload = {
            "host": HOST,
            "key": key,
            "keyLocation": key_location,
            "urlList": batch,
        }
        status, body = _post_json(payload)
        if status in SUCCESS_CODES:
            print(f"IndexNow accepted {len(batch)} URL(s) (HTTP {status})")
            continue
        if status in WARNING_CODES:
            print(
                f"warning: IndexNow returned HTTP {status}; the key may not be "
                f"verified yet ({key_location}). {_short(body)}"
            )
            continue
        print(f"warning: IndexNow request failed (HTTP {status}). {_short(body)}")
        exit_code = 1
    return exit_code


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Submit bg60day.com URLs to IndexNow.")
    parser.add_argument(
        "--send",
        action="store_true",
        help="POST to IndexNow. Without this flag the command only prints the payload.",
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help="Optional site paths or absolute URLs. Omit to use sitemap.xml.",
    )
    args = parser.parse_args(argv)
    urls = paths_to_urls(args.paths) if args.paths else None
    return submit(urls, send=args.send)


def _post_json(payload: dict) -> tuple[int, str]:
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        ENDPOINT,
        data=data,
        method="POST",
        headers={"Content-Type": "application/json; charset=utf-8"},
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.status, response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode("utf-8", errors="replace")
    except urllib.error.URLError as exc:
        return 0, str(exc.reason)


def _dedupe(urls: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for url in urls:
        if url in seen:
            continue
        seen.add(url)
        ordered.append(url)
    return ordered


def _short(body: str, limit: int = 200) -> str:
    text = " ".join(body.split())
    if not text:
        return ""
    if len(text) > limit:
        text = text[:limit] + "..."
    return text


if __name__ == "__main__":
    sys.exit(main())
