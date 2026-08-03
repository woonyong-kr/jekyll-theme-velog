#!/usr/bin/env python3
"""Validate a generated Jekyll site without third-party dependencies."""

from __future__ import annotations

import argparse
import json
import sys
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit


REQUIRED_FILES = ("index.html", "404.html", "feed.xml", "sitemap.xml", "posts.json")
PLACEHOLDERS = (
    "https://github.com/your-handle",
    "owner/repository",
    "REPOSITORY_NODE_ID",
    "CATEGORY_NODE_ID",
)
IGNORED_SCHEMES = {"data", "http", "https", "mailto", "tel", "javascript"}


class DocumentParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.main_count = 0
        self.references: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "main":
            self.main_count += 1

        attribute_name = "href" if tag in {"a", "link"} else "src" if tag in {"img", "script"} else ""
        if not attribute_name:
            return

        for name, value in attrs:
            if name == attribute_name and value:
                self.references.append((tag, value))


def normalize_baseurl(value: str) -> str:
    stripped = value.strip()
    if not stripped or stripped == "/":
        return ""
    return "/" + stripped.strip("/")


def resolve_target(site_dir: Path, source: Path, reference: str, baseurl: str) -> Path | None:
    parsed = urlsplit(reference)
    if parsed.scheme.lower() in IGNORED_SCHEMES or parsed.netloc or not parsed.path:
        return None

    decoded_path = unquote(parsed.path)
    if decoded_path.startswith("/"):
        if baseurl and decoded_path != baseurl and not decoded_path.startswith(baseurl + "/"):
            raise ValueError(f"root URL does not include configured baseurl: {reference}")
        relative_path = decoded_path[len(baseurl) :].lstrip("/") if baseurl else decoded_path.lstrip("/")
    else:
        relative_path = str(PurePosixPath(source.relative_to(site_dir).parent.as_posix()) / decoded_path)

    target = site_dir / relative_path
    if decoded_path.endswith("/") or not target.suffix:
        target = target / "index.html"
    return target.resolve()


def validate(site_dir: Path, baseurl: str) -> list[str]:
    errors: list[str] = []
    site_root = site_dir.resolve()

    for required in REQUIRED_FILES:
        if not (site_dir / required).is_file():
            errors.append(f"missing required output: {required}")

    posts_path = site_dir / "posts.json"
    if posts_path.is_file():
        try:
            payload = json.loads(posts_path.read_text(encoding="utf-8"))
            if not isinstance(payload.get("posts"), list):
                errors.append("posts.json must contain a posts array")
        except (json.JSONDecodeError, UnicodeDecodeError) as error:
            errors.append(f"invalid posts.json: {error}")

    for html_path in sorted(site_dir.rglob("*.html")):
        source = html_path.read_text(encoding="utf-8")
        parser = DocumentParser()
        parser.feed(source)

        if parser.main_count != 1:
            errors.append(f"{html_path.relative_to(site_dir)}: expected one <main>, found {parser.main_count}")

        for tag, reference in parser.references:
            for placeholder in PLACEHOLDERS:
                if placeholder in reference:
                    errors.append(
                        f"{html_path.relative_to(site_dir)}: unresolved placeholder in {tag}: {placeholder!r}"
                    )
            try:
                target = resolve_target(site_dir, html_path, reference, baseurl)
            except ValueError as error:
                errors.append(f"{html_path.relative_to(site_dir)}: {error}")
                continue

            if target is None:
                continue
            try:
                target.relative_to(site_root)
            except ValueError:
                errors.append(f"{html_path.relative_to(site_dir)}: {tag} escapes site root: {reference}")
                continue
            if not target.is_file():
                errors.append(f"{html_path.relative_to(site_dir)}: broken {tag} target: {reference}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("site_dir", type=Path)
    parser.add_argument("--baseurl", default="")
    args = parser.parse_args()

    if not args.site_dir.is_dir():
        print(f"site directory not found: {args.site_dir}", file=sys.stderr)
        return 2

    errors = validate(args.site_dir, normalize_baseurl(args.baseurl))
    if errors:
        print("Site verification failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    html_count = sum(1 for _ in args.site_dir.rglob("*.html"))
    print(f"Site verification passed: {html_count} HTML documents, required outputs and internal links")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
