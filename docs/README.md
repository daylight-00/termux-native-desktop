
# Documentation map

The repository uses a question-routed authority model rather than a flat reading list.

## Initialization and current state

- [`DOCUMENTATION_MODEL.md`](DOCUMENTATION_MODEL.md) — authority, lifecycle, conflict, and context-budget rules.
- [`INDEX.md`](INDEX.md) — question-oriented router.
- [`catalog.tsv`](catalog.tsv) — machine-readable canonical catalog.
- [`current/`](current/) — current semantic state, active task, and pending external inputs.

## Authority classes

- [`constitution/`](constitution/) — project purpose, invariants, and durable philosophy.
- [`architecture/`](architecture/) — integrated system and component contracts.
- [`decisions/`](decisions/) — accepted, proposed, superseded, rejected, or historical decisions.
- [`evidence/`](evidence/) — experiments, receipts, and transaction evidence.
- [`history/`](history/) — chronology and legacy refactor routing.
- [`knowledge/`](knowledge/) — reusable systems-study material.

The large existing corpus has not been moved merely to match this logical tree. Routers assign authority to existing paths, and later physical moves must follow the migration rules in `DOCUMENTATION_MODEL.md`.

History is not read by default.
