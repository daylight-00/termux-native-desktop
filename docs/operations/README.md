
# Operations documentation

This is the canonical router for progress-independent user/agent collaboration, repository transport, package exchange, testing, and platform behavior.

## Platform profile

- [`platforms/chatgpt-web.md`](platforms/chatgpt-web.md) — current web-chat sandbox, Git bundle transport, connector limits, Drive exchange, and Termux authority.

Codex or Claude Code profiles may be added when those environments are actually adopted. They must reuse `AGENTS.md` rather than fork the project contract.

## Durable collaboration and execution

- [`../session-operations/README.md`](../session-operations/README.md) — session-operation index.
- [`../session-operations/COLLABORATION.md`](../session-operations/COLLABORATION.md) — user/agent roles and Drive exchange.
- [`../session-operations/AGENT_EXECUTION.md`](../session-operations/AGENT_EXECUTION.md) — candidate, runner, result, and acceptance discipline.
- [`../session-operations/SESSION_LIFECYCLE.md`](../session-operations/SESSION_LIFECYCLE.md) — bundle-native receive-to-accepted-transition lifecycle.
- [`../session-operations/SESSION_CLOSE.md`](../session-operations/SESSION_CLOSE.md) — clean boundary and optional incomplete-work checkpoint.
- [`../session-operations/TROUBLESHOOTING.md`](../session-operations/TROUBLESHOOTING.md) — known operational failure modes.

Current project progress does not live in operations documents. It is owned by [`../current/`](../current/).
