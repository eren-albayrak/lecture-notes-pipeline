# Referee brief (verbal branch)

Two agents answered each question independently: a **blind solver** that did not see the key, and
an **auditor** that saw everything. Your input `referee_<n>.json` holds the questions where the source
key, the solver and the auditor disagree, or where the options are broken in the source. Each item
includes the stem, the options, the source explanation, the previous question and, for matching sets,
the question that owns the shared list.

House rule: **stems and options are never changed.** An answer is changed only if it is clearly
wrong, and every intervention stays visible to the student as an "AI note".

## Decide each question
Solve it yourself first, then weigh both agents' reasons.

- `source_correct`: the key is right; the objection is wrong or only a nuance.
- `fix`: the key is clearly wrong and the correct answer is among the visible options. Use only when sure.
- `options_lost`: the question's own options are missing in the source, so the key letter is
  meaningless. Give `answer: null` and the correct answer as short text.
- `disputed`: more than one option is defensible, or the question is defective. The key stays;
  explain in the note.

## Output
Write only `results/referee_<n>_decision.json`:

```json
{"id": "S.3", "decision": "source_correct|fix|options_lost|disputed", "answer": "C or null",
 "answer_text": "", "note": "student-facing AI note, 1–2 sentences: what the source said and why"}
```

For `fix`, use the pattern "Source marked X; correct is Y, because ...".
After writing, reload the file and check the item count.

## Final reply
Distribution of decisions, and each `fix` on one line.
