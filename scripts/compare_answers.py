"""Verbal branch: three-way answer comparison (source key / blind solver / auditor) -> referee queue.

The blind solver never sees the source answer key; the auditor sees everything.
A question goes to the referee if the three views disagree, if the auditor flags the
explanation as shifted/missing/wrong, or if either agent reports low confidence.
Only the referee may change an answer (enforced later by fidelity_check.py).

Usage:
    python -I scripts/compare_answers.py <work_dir>

Input (in <work_dir>):
    source.json   {"questions": [{"id", "stem", "options": [{"letter", "text"}], "answer", "explanation"}]}
    solver.json   [{"id", "answer", "confidence": "certain|likely|unsure", "reason"}]
    auditor.json  [{"id", "correct_answer", "key_correct", "explanation_status": "ok|shifted|missing|wrong",
                    "confidence", "reason"}]
Output (in <work_dir>):
    comparison.json      every question with the three views and the reasons it was flagged
    referee_queue.json   flagged questions only, with stem/options/explanation for the referee

Exit status is 1 if a solver or auditor result is missing for any question.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def compare(work: Path) -> int:
    source = {q["id"]: q for q in load(work / "source.json")["questions"]}
    solver = {r["id"]: r for r in load(work / "solver.json")}
    auditor = {r["id"]: r for r in load(work / "auditor.json")}

    missing = [i for i in source if i not in solver or i not in auditor]
    if missing:
        print("MISSING results for:", missing)

    rows, queue, counts = [], [], Counter()
    for qid, q in source.items():
        s, a = solver.get(qid, {}), auditor.get(qid, {})
        key, blind, audit = q["answer"], s.get("answer"), a.get("correct_answer")
        agree = blind == key and audit == key and a.get("key_correct", True)
        expl = a.get("explanation_status", "?")
        reasons = []
        if not agree:
            reasons.append(f"answer: source {key}, blind {blind}, auditor {audit}")
        if expl in ("shifted", "missing", "wrong"):
            reasons.append(f"explanation {expl}")
        if "unsure" in (s.get("confidence"), a.get("confidence")):
            reasons.append("low confidence")
        counts["agree" if agree else "disagree"] += 1
        counts[f"explanation_{expl}"] += 1
        row = {"id": qid, "source": key, "blind": blind, "blind_reason": s.get("reason"),
               "auditor": audit, "auditor_reason": a.get("reason"), "reasons": reasons}
        rows.append(row)
        if reasons:
            queue.append({**row, "stem": q["stem"], "options": q["options"], "source_explanation": q["explanation"]})

    (work / "comparison.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    (work / "referee_queue.json").write_text(json.dumps(queue, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"questions {len(source)} | " + " | ".join(f"{k} {v}" for k, v in sorted(counts.items())))
    print(f"sent to referee: {len(queue)} -> {[r['id'] for r in queue]}")
    return int(bool(missing))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sys.exit(compare(Path(sys.argv[1])))
