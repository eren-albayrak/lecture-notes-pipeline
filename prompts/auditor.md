# Auditor brief (numeric branch)

The book has been compiled. Your job is an **independent error audit** of source pages `<slice>`
(10 pages). Compare each source page with the book line by line. **Do not edit any file.** A separate
fixer agent applies the changes, so every finding must carry an exact correction that can be applied as-is.

## Read first
- `RULES.md`, the layer/label glossary, and the compiler brief (how the book was produced).
- The comparison reports of the two readings for your slice. Do not trust them blindly: re-test any
  doubtful decision against the image.

## Checklist (per source page)
- **A. Fidelity.** Every line on lecturer pages and in steps labelled as the lecturer's matches the
  image (sign, exponent, index, coefficient, variable name, order). A lecturer error is kept with
  `[sic]` plus a separate AI correction. It is never fixed silently.
- **B. Completeness.** Every example, rule, warning, exercise and margin note appears somewhere.
  Question numbering has no gaps. The question register agrees with the book.
- **C. Mathematics.** AI solution steps are correct and follow from each other, and the result box is
  right. When in doubt, test with SymPy in your own scratch folder.
- **D. Layers.** No AI content is presented as the lecturer's, and labels are correct. A question
  without a source solution must not look like a lecturer solution.
- **E. Typesetting.** Overflow, broken maths, spelling, orphaned headings, unreadable fractions.
- **F. Open gates.** Re-examine each `[?]` / `Blocked` at high zoom. Propose a reasoned decision or
  state that it must stay open.

## Report
`audit/audit_<slice>.md`:
1. Summary: pages audited, findings by severity (Critical / Medium / Minor).
2. Findings table: `No · Severity · Source page · File:line · Finding · Evidence (what the image shows) · Fix (old text -> new text)`.
   - Critical: wrong maths, a line wrongly attributed to the lecturer, lost content, layer violation.
   - Medium: misleading wording, missing `[sic]` correction, register inconsistency, layout that hurts reading.
   - Minor: spelling, formatting.
3. Decisions on open gates.
4. Pages found clean, with one line on what was verified.

Do not invent findings. Mark uncertain ones as "suspected" and show the evidence. If there are no
findings, say so explicitly.

## Final reply (at most 15 lines)
Report path, counts by severity, the 3–5 most important findings.
