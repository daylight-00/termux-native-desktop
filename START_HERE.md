# Start here

This repository is self-initializing. A web-chat agent should receive a full Git bundle from the user's authoritative Termux checkout, clone it into the session sandbox, and use this file as the first repository document.

## Required boot order

1. Confirm the checked-out branch, `HEAD`, tree, and tracked-worktree status.
2. Read [`AGENTS.md`](AGENTS.md).
3. Read [`docs/current/BRIEF.md`](docs/current/BRIEF.md).
4. Read [`docs/current/ACTIVE_TASK.md`](docs/current/ACTIVE_TASK.md).
5. Read only the documents listed under **Required reading** in the active task.
6. Read a platform profile only when the active task requires it or before platform-specific transport, file exchange, or device execution.
7. Use [`docs/DOCUMENTATION_MODEL.md`](docs/DOCUMENTATION_MODEL.md) and [`docs/INDEX.md`](docs/INDEX.md) only when deeper routing is needed.
8. Produce a compact onboarding receipt before proposing or executing project work.

Do not use a dated handoff, a numbered refactor record, or an old session narrative as current authority unless the active task names it as evidence or as a document being repaired.

## Platform profiles

- ChatGPT web: [`docs/operations/platforms/chatgpt-web.md`](docs/operations/platforms/chatgpt-web.md)
- Codex and other repository-native agents: follow `AGENTS.md`; a dedicated profile may be added when that environment is adopted.
- Claude Code: [`CLAUDE.md`](CLAUDE.md) points back to the same canonical contract.

## Onboarding receipt

Before work begins, state:

```text
branch / HEAD / tree
semantic state version
current project phase
active task
required documents loaded
historical documents loaded
user and agent authority boundary
available and unavailable execution environments
first valid action
```

## Context boundary

The default onboarding set is exactly this routing file plus the three files named in steps 2-4. Historical records are never loaded by default. The active task may name at most eight additional required-reading documents.
