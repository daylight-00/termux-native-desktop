# Session operations

This directory records durable collaboration and execution rules for recurring web-chat sessions. Current project state does **not** live here; it is owned by [`../current/`](../current/).

## Normal web-chat start

```text
1. receive a user-created full Git bundle from the authoritative Termux checkout;
2. verify and clone the bundle in the sandbox;
3. read ../../START_HERE.md;
4. read ../../AGENTS.md, ../current/BRIEF.md and ../current/ACTIVE_TASK.md;
5. read only the active task's required documents;
6. inspect any blocking artifact named in ../current/PENDING_ARTIFACTS.yaml;
7. begin the first valid action.
```

No narrative handoff is required. The repository commit, current-state documents and Git history must be sufficient to initialize the successor session.

## Durable operating documents

- [`SESSION_LIFECYCLE.md`](SESSION_LIFECYCLE.md) — bundle-native receive-to-accepted-transition lifecycle.
- [`COLLABORATION.md`](COLLABORATION.md) — user/agent roles, Drive exchange and connector boundaries.
- [`AGENT_EXECUTION.md`](AGENT_EXECUTION.md) — candidate, wrapper, testing and receipt-review discipline.
- [`SESSION_CLOSE.md`](SESSION_CLOSE.md) — clean session boundary and optional incomplete-work checkpoint procedure.
- [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md) — accumulated failure modes and proven mitigations.
- [`CHANGELOG.md`](CHANGELOG.md) — durable changes to these operating rules.

## Ownership boundary

```text
AGENTS.md and PROJECT_PRINCIPLES.md
    durable project and agent contract

docs/current/
    current semantic state, active task and pending artifacts

session-operations/
    progress-independent collaboration and execution method

refactor/, experiments/, Git history
    evidence and historical transactions

handoff/
    archived legacy session-transition records only
```

When a reusable operating lesson is learned, update the relevant file here during the same accepted repository transition. Do not wait for a session close and do not bury the lesson only in chat narrative.
