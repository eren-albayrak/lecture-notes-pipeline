"""Source intake: extract scanned page images byte-for-byte and build the page inventory.

Step 1 of the numeric branch. The source PDF is never modified. Every physical page
gets a permanent ID (C-001, C-002, ...) that all later artefacts (transcriptions,
question register, audits, SymPy checks) refer to, so any line in the final book can
be traced back to one physical page.

Usage:
    python -I scripts/extract_source.py <source.pdf> <project_dir> [--prefix C]

Output:
    <project_dir>/source_pages/pNNN.<ext>   original embedded image bytes, unchanged
    <project_dir>/inventory/pages.csv       one row per page: ID, image hash, review status

Safety rules:
    * an existing inventory is never overwritten (it may already contain review notes);
    * if a previously extracted image differs from the PDF, the script stops;
    * each page must contain exactly one scan image, otherwise the script stops
      instead of guessing which image is the page.

Note: JPEG scans (the usual case) are written exactly as stored in the PDF. Images stored
with other filters are exported by PyMuPDF in a lossless format.

Requires: pymupdf.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import sys
from pathlib import Path

import pymupdf

FIELDS = [
    "pdf_page", "page_id", "source_image", "width_px", "height_px", "image_sha256",
    "handwritten_page_no", "topic", "question_ids", "transcription_status", "review_status", "notes",
]


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def extract(source: Path, project: Path, prefix: str = "C") -> list[dict]:
    pages_dir = project / "source_pages"
    manifest = project / "inventory" / "pages.csv"
    if manifest.exists():
        raise FileExistsError(f"refusing to overwrite a reviewed inventory: {manifest}")
    pages_dir.mkdir(parents=True, exist_ok=True)
    manifest.parent.mkdir(parents=True, exist_ok=True)

    print("source sha256:", sha256(source.read_bytes()))
    rows = []
    doc = pymupdf.open(source)
    for page_number, page in enumerate(doc, 1):
        images = page.get_images(full=True)
        if len(images) != 1:
            raise ValueError(f"page {page_number}: expected exactly one scan image, found {len(images)}")
        image = doc.extract_image(images[0][0])
        destination = pages_dir / f"p{page_number:03d}.{image['ext']}"
        data = image["image"]
        if destination.exists() and destination.read_bytes() != data:
            raise ValueError(f"existing extraction differs from source: {destination}")
        if not destination.exists():
            destination.write_bytes(data)
        rows.append({
            "pdf_page": page_number,
            "page_id": f"{prefix}-{page_number:03d}",
            "source_image": destination.relative_to(project).as_posix(),
            "width_px": image["width"],
            "height_px": image["height"],
            "image_sha256": sha256(data),
            "handwritten_page_no": "",
            "topic": "",
            "question_ids": "",
            "transcription_status": "TODO",
            "review_status": "TODO",
            "notes": "",
        })

    with manifest.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"{len(rows)} pages extracted and inventoried: {manifest}")
    return rows


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("source", type=Path, help="scanned lecture-note PDF (read only)")
    ap.add_argument("project", type=Path, help="project directory to write into")
    ap.add_argument("--prefix", default="C", help="page ID prefix (default: C)")
    args = ap.parse_args()
    extract(args.source, args.project, args.prefix)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
