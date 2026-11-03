# Agent briefs

Generic English versions of the briefs that drive the sub-agents (Claude Code) in the pipeline.
The production briefs are in Turkish and contain project paths. These keep the structure and the
rules, with paths replaced by placeholders such as `<project>` and `<slice>`.

Every brief follows the same skeleton: goal, what to read first, ordered steps, files the agent may
write, files it must not touch, report format, and a cap on the length of the final reply.

| Brief | Branch | Role |
|---|---|---|
| [`reader.md`](reader.md) | numeric | One of two independent readers of a page group |
| [`auditor.md`](auditor.md) | numeric | Independent audit of a 10-page slice; writes a report only |
| [`blind-solver.md`](blind-solver.md) | verbal | Answers questions without seeing the source key |
| [`referee.md`](referee.md) | verbal | Decides disputed answers; the only role allowed to change one |
