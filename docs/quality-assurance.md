# Quality assurance

LLM output is treated as a draft that has to pass gates, not as an answer. Each gate targets a
specific way the pipeline can fail.

## Failure modes and the gate that catches each

| Failure mode | Why it happens | Gate |
|---|---|---|
| Misread symbol (sign, exponent, index) | Handwriting is ambiguous; a single reader is confident and wrong | Two independent readings, differences decided from the image |
| "Helpful" silent correction of the lecturer | OCR and LLM tools tend to normalise mistakes away | OCR banned as a source; `[sic]` + separate AI correction; auditor checks fidelity |
| Guessing an unreadable spot | Context makes a guess look plausible | `[?]` with candidate, or `Blocked`; open gates listed in every report |
| Wrong AI solution | Algebra slips, lost constants, sign errors | SymPy gate on every "check your result" claim, with a self-test |
| AI content presented as the lecturer's | Layers blur during editing | Layer labels in text; auditor checklist item "Layers" |
| Skipped example or exercise | Long sources, page-order anomalies | Question register; coverage counts (N/N pages, N/N questions) |
| Wrong answer key in a question bank | Errors in the source itself | Blind solver + auditor + referee |
| Shifted or copied explanations | Compiled sources sometimes attach one question's explanation to its neighbours | Auditor flags `explanation_status`; referee or editor replaces it with a labelled AI note |
| Stems or options edited in passing | Editing and re-typesetting | Fidelity gate (`fidelity_check.py`) |
| Wrong AI summary or key fact | Plausible but inverted statements | Independent audit of every AI-generated text |
| Layout defects | Long books, many authors | `pdf_qa.py`: overflow, near-empty pages, mark count, broken links |

## Independence

- The two readers of a page group do not see each other's files.
- The blind solver does not see the answer key. If it reads the key, the result is discarded.
- Auditors only write reports. They cannot edit the book, so a finding cannot be "fixed" by the agent
  that found it without a second look.
- Fixers re-test every finding against the image before applying it, so an auditor's mistake is not
  propagated.
- Each agent gets its own scratch folder. Shared scratch space caused agents to overwrite each
  other's crop files.

## Automated gates

| Script | Branch | Proves | Does not prove |
|---|---|---|---|
| [`extract_source.py`](../scripts/extract_source.py) | numeric | Page images are the original bytes; every page has a permanent ID | Anything about the content |
| [`verify_solutions.py`](../scripts/verify_solutions.py) | numeric | Each stated result satisfies its equation (symbolic, then seeded numeric) | That the transcription matches the handwriting |
| `verify_solutions.py --selftest` | numeric | The gate rejects known-wrong claims, so "all passed" is meaningful | — |
| [`pdf_qa.py`](../scripts/pdf_qa.py) | both | No overflow, no near-empty page, mark on every page, no broken internal link | Visual quality of maths |
| [`compare_answers.py`](../scripts/compare_answers.py) | verbal | Every question has three views; disagreements are routed to the referee | That the referee is right |
| [`fidelity_check.py`](../scripts/fidelity_check.py) | verbal | Stems/options unchanged; answers changed only with referee authorisation and a visible note | That explanations are correct |

What the scripts cannot prove is covered by the human-readable audit reports and the open-gates list.

## Done criteria

A chapter or book is **not** called done by the pipeline. It is reported as in progress until:

- page and question coverage is complete (N/N);
- the SymPy gate and its self-test pass, and the build has no errors;
- PDF QA reports overflow 0, near-empty 0, mark count = page count, broken links 0;
- every audit finding is either applied or recorded with a reason;
- open gates (`[?]`, `Blocked`) and kept source errors (`[sic]`) are listed in the report;
- **the user has reviewed it.** "Done" is a human decision.

## Audit severity

| Severity | Examples |
|---|---|
| Critical | Wrong mathematics; a line attributed to the lecturer that the lecturer did not write; lost content; layer violation |
| Medium | Misleading wording; missing `[sic]` correction; register inconsistency; layout that hurts reading |
| Minor | Spelling, formatting |

Every finding must include evidence (what the image shows) and an exact `old -> new` fix, so that a
different agent can apply it without re-interpreting it.

## Running the gates on the synthetic examples

```bash
python -I scripts/verify_solutions.py --checks-dir examples/numeric-branch/checks
python -I scripts/verify_solutions.py --selftest
python -I scripts/pdf_qa.py examples/numeric-branch/example.pdf --mark sample
python -I scripts/compare_answers.py examples/verbal-branch
python -I scripts/fidelity_check.py examples/verbal-branch
python -I scripts/fidelity_check.py examples/verbal-branch final_tampered.json   # must fail
```
