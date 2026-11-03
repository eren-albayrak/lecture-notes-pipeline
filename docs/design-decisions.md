# Design decisions

Short records of the main decisions: context, decision, consequence.

## 1. No OCR as a source

**Context.** OCR and LLM-based OCR on handwritten mathematics produce errors that look plausible, and
LLM tools tend to "correct" the writer's mistakes quietly. A quiet correction is worse than a visible
error, because the student cannot tell it happened.

**Decision.** OCR output never enters the book, not even as a draft. Each page is read by eye from
the image by two independent readers, and differences are decided against the image.

**Consequence.** Slower and more expensive per page, but every line can be defended by pointing at
the image.

## 2. Lecturer layer and AI layer are kept apart

**Context.** Students study for the lecturer's exam. They need to know exactly what the lecturer
wrote, and separately what was added to help them understand it.

**Decision.** Every sentence belongs to one layer (lecturer note, AI explanation, AI addition, AI
solution), and the layer name is printed as text. Solution steps carry their own labels. Lecturer
errors are kept with `[sic]` and corrected in a separate AI addition.

**Consequence.** The book can be checked line by line against the source, and AI mistakes cannot hide
behind the lecturer's authority.

## 3. Uncertainty is shown, never resolved by guessing

**Decision.** Unreadable spots become `[?]` (with a candidate reading) or `Blocked`. Open gates are
listed in every report and are not hidden by a "done" status.

## 4. Independence over agent count

**Context.** Several agents that see each other's output tend to agree with each other.

**Decision.** Checks are designed around information hiding: readers do not see each other, the blind
solver does not see the key, auditors cannot edit, fixers re-test findings. Agents own files; shared
files belong to the main session.

**Consequence.** Disagreement becomes a signal that routes work to a referee or to the main session.

## 5. Typst for typesetting

**Context.** The output is a long, maths-heavy, cross-linked book, rebuilt many times during audits.

**Decision.** Typst rather than LaTeX or a word processor.

**Reasons.**
- Fast incremental builds, so the full book can be rebuilt after every fix round.
- One scripting language for layout and logic: the four-page cycle, labels, bookmarks and the clickable
  question index are ordinary functions in [`templates/textbook.typ`](../templates/textbook.typ).
- `--input` switches build variants from the same source (for example the phone edition with lighter images).
- Readable error messages, so agents can fix their own compile errors.

**Known pitfalls, recorded in the rules.** `upper()` is not Turkish-aware (i -> İ needs a custom
function); visible page titles must not be headings, or the bookmark tree is reset; in maths mode
`xy` is one variable, so `x y` must be written.

## 6. SymPy gate with a self-test

**Decision.** Every "check your result" claim becomes an expression that must reduce to zero. The gate
first tries symbolic simplification and then seeded random numeric evaluation. A self-test feeds it
known-wrong claims and must reject all of them.

**Consequence.** "All checks passed" is only reported when the checker has shown it can fail. The gate
proves that solutions are correct, not that the transcription is faithful; that is the auditor's job.

## 7. Black-and-white academic layout

**Context.** Several layouts were tried and reviewed by the user. Coloured boxes and very airy layouts
were rejected. A layout that reads like a printed journal article was accepted.

**Decision.** Black and white, serif body, labels and thin rules instead of background colour. On
solution pages: maths first, little prose, no side-note column, large display fractions.

**Consequence.** Books print well on any printer and stay readable in grayscale. Accessibility does not
depend on colour.

## 8. Physical page IDs never change

**Decision.** `C-###` is the physical PDF page. Questions, audits and checks refer to it. Reordering
chapters never renumbers source pages.

**Consequence.** Audit reports and corrections stay valid across rebuilds.

## 9. Several editions from one source

**Decision.** Each course package has a full edition, a phone edition, an exam booklet and a reading
guide, all built from the same sources with build inputs.

**Consequence.** No edition drifts from the others; a fix lands in all of them on the next build.

## 10. The repository holds the system, not the content

**Decision.** Lecture notes, scans, produced books, exam questions and question-bank content are not
published here. They belong to their authors. Examples in this repository are synthetic.
