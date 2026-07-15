# Operations documentation

This directory is the single current authority for progress-independent web-chat collaboration, repository transport, execution transactions, result review, optional checkpoints, and platform capability boundaries.

## Canonical documents

| Question | Read |
|---|---|
| Who does what, and how are artifacts exchanged? | [`COLLABORATION.md`](COLLABORATION.md) |
| How does one bundle-native work cycle proceed? | [`WORKFLOW.md`](WORKFLOW.md) |
| How are candidates, wrappers, tests, results, and acceptance handled? | [`EXECUTION.md`](EXECUTION.md) |
| What happens at a clean boundary or with valuable incomplete work? | [`CHECKPOINTS.md`](CHECKPOINTS.md) |
| What failures have known operational mitigations? | [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md) |
| What can the current web-chat sandbox and connectors actually do? | [`platforms/chatgpt-web.md`](platforms/chatgpt-web.md) |

These responsibilities must not be duplicated as current authority in another directory. The former `docs/session-operations/` surface is historical and is indexed under [`../history/session-operations-v1/`](../history/session-operations-v1/).

## Ownership boundary

```text
AGENTS.md
    agent/user authority and non-negotiable execution boundaries

docs/current/
    current semantic state, active task, and pending artifacts

docs/operations/
    durable collaboration and execution method

docs/architecture/ and docs/decisions/
    system contracts and accepted choices

docs/evidence/, experiments/, docs/refactor/, Git history
    observations, receipts, and historical transactions
```

Current project progress does not live here. Reusable operational lessons are updated here in the same accepted repository transition in which they are learned; they are not deferred to session close or hidden only in chat narrative.

Codex or Claude Code profiles may be added when those environments are actually adopted. They must reuse `AGENTS.md` and the platform-neutral documents in this directory rather than fork the project contract.
