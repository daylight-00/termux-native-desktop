# Active task: consolidate operations and historical surfaces

> Task ID: `operations-consolidation-and-historical-surface-cleanup`
>
> Expected state on completion: durable web-chat collaboration rules have one canonical operations surface; legacy session-process and handoff documents are clearly historical or replaced; and a new session can locate operational guidance without reading superseded lifecycle narratives.

## Objective

Consolidate the progress-independent collaboration, transport, execution-package, result-review, and optional checkpoint rules under `docs/operations/`, then reduce the remaining authority ambiguity in `docs/session-operations/` and `docs/handoff/`.

## Why now

The constitutional surface is compact and ADR 0005 now bounds assurance work. The largest remaining documentation overlap affecting every web-chat session is operational: current rules are split between `AGENTS.md`, the ChatGPT platform profile, and seven legacy `session-operations` documents that evolved from the former mandatory-handoff model.

This should be resolved before resuming the provider-authority workstream so future sessions inherit one stable execution contract.

## Current accepted decisions

- Project identity is canonical in `docs/constitution/PROJECT.md`.
- Engineering, evidence, promotion, and assurance principles are canonical in `docs/constitution/PRINCIPLES.md`.
- Agent/user authority is canonical in `AGENTS.md`.
- ADR 0005 is accepted: assurance is proportional to the claim, implementation class, changed boundary, and risk.
- New web-chat sessions start from a user-provided full Git bundle and `START_HERE.md`.
- Narrative handoffs are not current authority.
- The provider-authority workstream remains paused pending object/claim reclassification under ADR 0005.

## In scope

- Map overlap among `docs/operations/`, `docs/session-operations/`, the ChatGPT platform profile, and legacy handoff procedures.
- Define one canonical home for collaboration roles, Git/bundle transport, Drive exchange, runner/result lifecycle, troubleshooting, and optional incomplete-work checkpoints.
- Preserve reusable failure lessons while removing obsolete mandatory-handoff assumptions.
- Decide whether legacy files should become compact tombstones, move under history, or remain reference sources with explicit lifecycle labels.
- Keep the web-chat operational surface small enough for task-specific reading.
- Add mechanical checks preventing reintroduction of narrative handoff authority or unsupported tool capabilities.

## Out of scope

- Resuming SUP-02 or collecting provider evidence.
- Reclassifying the 28 provider roots under ADR 0005.
- Moving the numbered refactor corpus.
- Rewriting experiment reports.
- Device runtime, deployment, graphics, or application testing.
- Adopting Codex or Claude Code as the current execution environment.

## Required reading

- `docs/current/STATE.yaml`
- `docs/DOCUMENTATION_MODEL.md`
- `docs/operations/README.md`
- `docs/operations/platforms/chatgpt-web.md`
- `docs/session-operations/README.md`
- `docs/session-operations/COLLABORATION.md`
- `docs/session-operations/AGENT_EXECUTION.md`

Do not read dated handoffs or the full refactor corpus. Open another legacy operations file only to resolve a named overlap or preserve a reusable failure lesson.

## Known facts

- Accepted repository transitions update current state directly; normal session close produces no handoff.
- The user may create a full bundle directly from authoritative Termux `main` for the next session.
- GitHub connector raw-content actions are not a substitute for clone/object transport.
- Google Drive carries bundles, patches, runners, results, logs, and safety artifacts.
- New-chat local-path upload rewriting can be unavailable on the first assistant turn.
- Docker is unavailable and outside the project workflow.

## Pending external inputs

None. See [`PENDING_ARTIFACTS.yaml`](PENDING_ARTIFACTS.yaml).

## Next valid action

Build an overlap map for the current operations documents, then define the smallest canonical operations set before moving or tombstoning any legacy file.

## Stop conditions

Stop before implementation if:

- a reusable operational lesson would be lost;
- two documents would remain canonical for the same rule;
- the new surface assumes repository-local capabilities unavailable in web chat;
- a physical move lacks complete inbound-link migration and repository-wide link validation;
- the change reintroduces a required session-close handoff.

## Completion criteria

- Each durable collaboration/tool/exchange rule has one canonical home.
- Legacy session and handoff narratives are explicitly historical or replaced.
- The web-chat profile accurately distinguishes sandbox, Drive, GitHub connector, and user Termux authority.
- Optional checkpointing is defined only for valuable incomplete work.
- Default onboarding remains four files and history-free.
- The next active task can apply ADR 0005 to the paused provider claims without relying on chat memory.
