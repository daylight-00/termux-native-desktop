# Documentation map

The repository separates current semantic authority, durable architecture and operations, experiment provenance, and historical transition evidence.

## Start here

- [`../START_HERE.md`](../START_HERE.md) — repository initialization and required reading order.
- [`../AGENTS.md`](../AGENTS.md) — durable project-agent contract.
- [`INDEX.md`](INDEX.md) — question-oriented document router.
- [`current/BRIEF.md`](current/BRIEF.md) — compact current project boundary.
- [`current/ACTIVE_TASK.md`](current/ACTIVE_TASK.md) — current bounded task, required reading, stop conditions, and next valid action.
- [`current/STATE.yaml`](current/STATE.yaml) — machine-readable semantic state.
- [`current/PENDING_ARTIFACTS.yaml`](current/PENDING_ARTIFACTS.yaml) — external inputs that may block progress.

A new agent should not begin from `handoff/CURRENT.md`. Dated handoffs are historical transition evidence and remain available only for reconstruction.

## Durable project knowledge

- [`PROJECT_CONTEXT.md`](PROJECT_CONTEXT.md) — why the project exists and how the workstreams evolved.
- [`PROJECT_PRINCIPLES.md`](PROJECT_PRINCIPLES.md) — evidence, authority, and project philosophy.
- [`system-foundation/README.md`](system-foundation/README.md) — top-down essence, invariants, target model, and execution precedence.
- [`architecture.md`](architecture.md) — integrated whole-system model.
- [`glibc-layer.md`](glibc-layer.md) — glibc application-world boundaries and operations.
- [`gpu.md`](gpu.md) — graphics composition and evidence contract.
- [`desktop-session.md`](desktop-session.md) — Termux:X11 and XFCE session contract.
- [`decisions/`](decisions/) — durable accepted, superseded, or historical decisions.

## Agent and collaboration operations

- [`operations/platforms/chatgpt-web.md`](operations/platforms/chatgpt-web.md) — web-chat bundle transport, connector limits, and execution authority.
- [`session-operations/COLLABORATION.md`](session-operations/COLLABORATION.md) — durable user/agent exchange contract.
- [`session-operations/AGENT_EXECUTION.md`](session-operations/AGENT_EXECUTION.md) — candidate, wrapper, and result-review discipline.
- [`session-operations/TROUBLESHOOTING.md`](session-operations/TROUBLESHOOTING.md) — accumulated operational failure modes.

The old mandatory narrative-handoff lifecycle is retired. Reusable operating lessons remain valid while current-state ownership moves to `current/`.

## Evidence and history

- [`../experiments/README.md`](../experiments/README.md) — experiment interpretation and provenance contract.
- [`refactor/README.md`](refactor/README.md) — transaction-level work-log index and evidence precedence.
- [`handoff/README.md`](handoff/README.md) — historical session-transition records.
- [`timeline.md`](timeline.md) — chronological navigation.
- [`knowledge/README.md`](knowledge/README.md) — reusable systems-study map.

```text
current/ and accepted decisions
    current semantic authority

integrated architecture and operations
    durable interpretation and procedure

experiments and numbered refactor records
    evidence and transaction history

handoff/
    historical session-boundary evidence only
```
