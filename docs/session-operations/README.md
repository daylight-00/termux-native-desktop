# Session initialization

> **Process transition:** New sessions now start from a user-provided full Git bundle and repository-root `START_HERE.md`. The durable collaboration lessons in this directory remain applicable, but the mandatory narrative-handoff lifecycle described below is legacy process material pending synchronization.

This is the stable entry point for recurring ChatGPT session changes. It deliberately separates long-lived collaboration rules from the project state recorded under [`../handoff/`](../handoff/README.md).

## New-session boot order

```text
1. receive the mandatory handoff .tar.zst;
2. verify SHA-256, zstd integrity, member safety and MANIFEST.sha256;
3. read START_HERE.md inside the package;
4. read ../PROJECT_PRINCIPLES.md;
5. read ../handoff/CURRENT.md and its linked dated handoff;
6. inspect any pending result before writing the next repository change;
7. verify local and remote Git coordinates;
8. continue only the allowed project workstream.
```

The first document should remain short. Follow these links for details:

- [`../PROJECT_PRINCIPLES.md`](../PROJECT_PRINCIPLES.md) — project purpose, evidence ladder and authority philosophy.
- [`SESSION_LIFECYCLE.md`](SESSION_LIFECYCLE.md) — complete receive-to-next-handoff cycle.
- [`COLLABORATION.md`](COLLABORATION.md) — agent/user roles, Drive exchange and connector boundaries.
- [`AGENT_EXECUTION.md`](AGENT_EXECUTION.md) — patch, wrapper, testing and receipt-review discipline.
- [`SESSION_CLOSE.md`](SESSION_CLOSE.md) — automatic close procedure and the two/three-package rule.
- [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md) — accumulated failure modes and proven mitigations.
- [`CHANGELOG.md`](CHANGELOG.md) — durable rule changes learned across sessions.

## Ownership boundary

```text
PROJECT_PRINCIPLES.md = durable project philosophy and evidence rules
session-operations/   = process independent of project progress
handoff/              = project state at one session boundary
refactor/experiments/STATUS.md = actual project work and evidence
```

When a new operational lesson is learned, update the relevant file here during the same session. Do not wait until the next handoff and do not bury it in a numbered project record.
