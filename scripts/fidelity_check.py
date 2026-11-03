"""Verbal branch fidelity gate: the final book may not silently change the source.

Rules checked for every question in final.json against source.json:
    1. the stem is identical to the source (whitespace-insensitive);
    2. the options are identical to the source (letters and text);
    3. the answer differs from the source only if the referee decided "fix" or
       "options_lost" for that question, and the final item carries a visible AI note.
Question counts must match. Any violation is printed and the exit status is 1.

Usage:
    python -I scripts/fidelity_check.py <work_dir> [final_file]   (default final_file: final.json)

Input (in <work_dir>): source.json, final.json (same schema, plus "answer_note"),
                       referee.json [{"id", "decision", "answer", "note"}]
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

AUTHORISED = {"fix", "options_lost"}


def norm(text: str) -> str:
    return re.sub(r"\s+", "", text)


def options_text(q: dict) -> str:
    return norm("".join(o["letter"] + o["text"] for o in q["options"]))


def check(work: Path, final_name: str = "final.json") -> int:
    load = lambda name: json.loads((work / name).read_text(encoding="utf-8"))  # noqa: E731
    source = {q["id"]: q for q in load("source.json")["questions"]}
    final = load(final_name)["questions"]
    referee = {r["id"]: r for r in load("referee.json")}

    errors = []
    if len(final) != len(source):
        errors.append(f"question count: source {len(source)}, final {len(final)}")
    for q in final:
        s = source.get(q["id"])
        if s is None:
            errors.append(f"{q['id']}: not in source")
            continue
        if norm(q["stem"]) != norm(s["stem"]):
            errors.append(f"{q['id']}: stem changed")
        if options_text(q) != options_text(s):
            errors.append(f"{q['id']}: options changed")
        if q["answer"] != s["answer"]:
            decision = referee.get(q["id"], {}).get("decision")
            if decision not in AUTHORISED:
                errors.append(f"{q['id']}: answer changed without referee authorisation ({decision})")
            if not q.get("answer_note"):
                errors.append(f"{q['id']}: answer changed but no AI note is shown")

    changed = sum(1 for q in final if source.get(q["id"], {}).get("answer") != q["answer"])
    for e in errors:
        print("FIDELITY", e)
    print(f"questions {len(final)} | answers changed {changed} | fidelity errors {len(errors)}")
    return int(bool(errors))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) not in (2, 3):
        sys.exit(__doc__)
    sys.exit(check(Path(sys.argv[1]), *sys.argv[2:]))
