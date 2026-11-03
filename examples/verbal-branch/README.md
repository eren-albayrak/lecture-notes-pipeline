# Synthetic example: verbal branch

**Everything here is synthetic.** The four questions are trivial calculus items written for this
example. No real question bank content is included.

Two defects are planted in `source.json`:

- `S.3` has a wrong answer key (D instead of C);
- `S.4` has a shifted explanation (copied from `S.2`).

## Flow

| File | Produced by | Content |
|---|---|---|
| `source.json` | intake | Questions exactly as in the source, with key and explanation |
| `solver.json` | blind solver | Answers given without seeing the key |
| `auditor.json` | auditor | Saw everything; judges the key and the explanation |
| `comparison.json`, `referee_queue.json` | `compare_answers.py` | Three-way comparison; flagged items for the referee |
| `referee.json` | referee | `fix` for S.3, `source_correct` for S.4 (explanation replaced) |
| `final.json` | assembly | S.3 answer changed with a visible AI note; S.4 explanation replaced and labelled AI |
| `final_tampered.json` | negative test | An answer changed without the referee, and a stem edited |

## Run

From the repository root:

```bash
python -I scripts/compare_answers.py examples/verbal-branch
# questions 4 | agree 3 | disagree 1 | explanation_ok 3 | explanation_shifted 1
# sent to referee: 2 -> ['S.3', 'S.4']

python -I scripts/fidelity_check.py examples/verbal-branch
# questions 4 | answers changed 1 | fidelity errors 0

python -I scripts/fidelity_check.py examples/verbal-branch final_tampered.json
# FIDELITY S.1: answer changed without referee authorisation (None)
# FIDELITY S.1: answer changed but no AI note is shown
# FIDELITY S.2: stem changed
# exit status 1
```
