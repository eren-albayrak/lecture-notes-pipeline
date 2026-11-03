# Synthetic example: numeric branch

**Everything here is synthetic.** No lecturer's notes were used.

## Input (imagined)

One handwritten page, `C-001`, showing a worked example of a first-order linear ODE,
`y' + 2y = 4`, solved by the lecturer with an integrating factor, followed by an exercise
`y' = x y` with no solution.

## What the pipeline produces from it

| Item | Treatment | Pages in `example.pdf` |
|---|---|---|
| Chapter opening | Learning goals, source-page note | 1 |
| `I.1`, solution visible in source | Four-page cycle: lecturer note -> AI explanation -> try it yourself -> step-by-step solution | 2–5 |
| `I.2`, question only | Try it yourself + solution with every step labelled `AI çözümü` | 6–7 |
| Self-check questions | Labelled as AI study questions | 7 |

Look for: the layer label at the top of every page, the per-step labels on solution pages
(`hoca hesabı` = lecturer's calculation, `AI tamamlaması` = AI completion), the source line in each
footer, the PDF bookmarks, and the faint page mark (`sample`) at the bottom centre.

## Files

| File | Purpose |
|---|---|
| `main.typ` | Book source, using `templates/textbook.typ` |
| `example.pdf` | Compiled output (Typst 0.15.1); page 5 is shown in the main README next to a synthetic scan ([`docs/img/`](../../docs/img/)) |
| `checks/checks_example.py` | SymPy plug-in: each "check your result" claim as an expression that must be zero |

## Run

From the repository root:

```bash
typst compile examples/numeric-branch/main.typ examples/numeric-branch/example.pdf --root .
python -I scripts/verify_solutions.py --checks-dir examples/numeric-branch/checks
python -I scripts/pdf_qa.py examples/numeric-branch/example.pdf --mark sample
```

Expected: `3/3 checks passed`; `overflow 0 | near-empty 0 | unmarked 0 | broken links 0`.
