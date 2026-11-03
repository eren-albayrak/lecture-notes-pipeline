"""Typesetting QA for a compiled book: margin overflow, near-empty pages, mark count, broken links.

Usage:
    python -I scripts/pdf_qa.py <book.pdf> [<book.pdf> ...] [--mark TEXT]

Checks per PDF:
    overflow    text span starting left of 20 mm or ending right of (width - 14 mm),
                with 1 pt tolerance for justified hyphenation;
    near-empty  4 or fewer text lines and no image (appendix pages that reproduce
                original scans contain an image and are skipped);
    mark        with --mark, every page must carry the faint build mark;
    links       every internal link must point to an existing page;
    outline     number of PDF bookmarks (for navigation review).

Exit status is 1 if any PDF has overflow, near-empty pages, missing marks or broken links.

Requires: pymupdf.
"""

from __future__ import annotations

import argparse
import sys

import pymupdf

MM = 72 / 25.4


def scan(path: str, mark: str | None) -> int:
    doc = pymupdf.open(path)
    overflow, empty, unmarked, broken = [], [], [], 0
    for i, page in enumerate(doc):
        width = page.rect.width
        for block in page.get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                for span in line["spans"]:
                    if not span["text"].strip():
                        continue
                    x0, _, x1, _ = span["bbox"]
                    if x0 < 20 * MM - 1 or x1 > width - 14 * MM + 1:
                        overflow.append((i + 1, round(x0 / MM, 1), round(x1 / MM, 1), span["text"][:40]))
        text = page.get_text()
        lines = [t for t in text.splitlines() if t.strip()]
        if len(lines) <= 4 and not page.get_images():
            empty.append(i + 1)
        if mark and mark not in text:
            unmarked.append(i + 1)
        for link in page.get_links():
            if link["kind"] == pymupdf.LINK_GOTO and not (0 <= link.get("page", -1) < doc.page_count):
                broken += 1

    print(f"{path}: {doc.page_count} pages | overflow {len(overflow)} | near-empty {len(empty)}"
          f" | unmarked {len(unmarked) if mark else 'n/a'} | broken links {broken} | bookmarks {len(doc.get_toc())}")
    for item in overflow[:30]:
        print("  OVERFLOW", item)
    if empty:
        print("  NEAR-EMPTY pages", empty[:30])
    if unmarked:
        print("  UNMARKED pages", unmarked[:30])
    return int(bool(overflow or empty or unmarked or broken))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("pdfs", nargs="+")
    ap.add_argument("--mark", help="text that must appear on every page")
    args = ap.parse_args()
    return max(scan(p, args.mark) for p in args.pdfs)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
