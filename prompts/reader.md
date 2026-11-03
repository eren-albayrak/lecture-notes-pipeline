# Reader brief (numeric branch)

You are one of **two independent readers** of source pages `<from>`–`<to>`. Another agent reads the
same pages, and you must not open its output. A compiler agent resolves differences between the two
readings later by looking at the image.

## Read first
- `<project>/RULES.md` (wins on conflict) and the layer/label glossary.
- The `inventory/pages.csv` rows for your pages.

## Steps
1. For each page, open `source_pages/pNNN.jpg`. Crop and enlarge regions as needed and read them by eye.
   **OCR output is not allowed as a source**, not even as a draft.
2. Transcribe line by line, in source order. Keep the lecturer's notation, including mistakes.
   Mark a mistake with `[sic]` and leave it uncorrected.
3. If a symbol cannot be read, write `[?]` with a candidate reading, or `Blocked` if there is no
   candidate. Never infer from context.
4. List every example, exercise and boxed remark with its page ID, and whether the source shows a
   solution. This decides between the four-page cycle and "question only, AI solution".
5. Note page-order anomalies (handwritten page number vs PDF order) without reordering anything.

## You may write
`<scratch>/readings/reading<N>_<group>.md` only. Use your own scratch sub-folder for crops.

## Final reply (at most 10 lines)
Pages read, number of items found, number of `[?]` and `Blocked` marks, order anomalies.
