# Blind solver brief (verbal branch)

Answer every question in `parts/<part>_blind.json` **with your own knowledge**. The file does not
contain the source answer key or the explanations, on purpose: your answers are used to test the key
independently. Do not read the key from anywhere else (full data files, other agents' outputs). If you
do, independence is lost and the result is discarded.

## Known source defects (flag them, do not repair them)
- Matching sets: a question with empty options shares the list of the nearest preceding question
  that has options. Answer against that list and record its ID in `list_source`.
- A question's own options may be missing because the visible list belongs to another set. Record
  this in `structure`, give `answer: null`, and write the correct answer as free text.
- Two options merged on one line. Record this in `structure` and read the letters accordingly.

## Output
Write only `results/<part>_solver.json`, with one item per question:

```json
{"id": "S.3", "answer": "C", "answer_text": "...", "confidence": "certain|likely|unsure",
 "reason": "one sentence", "list_source": null, "structure": ""}
```

- Use `certain` only for facts stated plainly in standard references. An honest `unsure` is worth
  more than a wrong `certain`.
- After writing, reload the file and check that the item count equals the number of questions.

## Final reply
Question count, number of structural defects found, number of `unsure` answers.
