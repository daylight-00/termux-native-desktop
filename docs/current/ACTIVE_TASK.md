
# Active task: consolidate the constitution and decide assurance depth

> Task ID: `constitution-consolidation-and-assurance-decision`
>
> Expected state on completion: the project has a compact, non-overlapping constitutional surface; the system-foundation lifecycle is explicit; and ADR 0005 is accepted, revised, rejected, or replaced through an explicit decision.

## Objective

Consolidate the durable project identity and invariant documents, then review the proposed proportional assurance-depth policy before any provider-authority evidence campaign resumes.

## Why now

The logical documentation authority model and question-based routers are in place. The remaining high-value overlap is concentrated among project context, project principles, the system-foundation series, and the agent contract. Leaving those as partially overlapping canonical sources would still force future agents to reconstruct precedence.

The paused provider-authority workstream also needs an explicit decision on assurance depth rather than another evidence-producing transaction by inertia.

## Current accepted decisions

- Web-chat sessions start from a user-provided full Git bundle and `START_HERE.md`.
- `docs/current/` owns current semantic state and the active task.
- `docs/DOCUMENTATION_MODEL.md` defines the logical authority and lifecycle classes.
- `docs/catalog.tsv` identifies canonical routers and key documents.
- Historical refactor and handoff records are excluded from default onboarding.
- `main` is the sole intended long-lived branch.
- Repository deployment is immutable and explicitly activated.
- Mesa mutable workspace and provider candidates are owned under XDG state.
- The provider-authority workstream remains paused at the 0165 no-response boundary.
- ADR 0005 is proposed, not accepted.

## In scope

- Map overlap among `PROJECT_CONTEXT.md`, `PROJECT_PRINCIPLES.md`, `AGENTS.md`, and system-foundation documents 01-05 and 11-12.
- Define the smallest compact constitutional surface that preserves project purpose, invariants, evidence philosophy, and agent authority.
- Classify system-foundation 06-10 as historical planning/assessment material without rewriting it.
- Review ADR 0005 class definitions, risk modifiers, stop rules, and provider-workstream consequences.
- Accept, revise, reject, or replace ADR 0005 explicitly.
- Prepare or implement bounded physical moves only with complete link migration and repository checks.
- Further reduce default and task-specific reading where consolidation makes that possible.

## Out of scope

- Rewriting numbered refactor records or experiment reports.
- Moving all architecture, operations, evidence, or history documents at once.
- Resuming SUP-02 acquisition or producing supplier responses.
- Accepting provider authority, composition, target population, or activation.
- Device runtime, graphics, or application testing.
- Adopting Codex or Claude Code as the current execution environment.

## Required reading

- `docs/current/STATE.yaml`
- `docs/DOCUMENTATION_MODEL.md`
- `docs/constitution/README.md`
- `docs/decisions/0005-proportional-assurance-depth.md`
- `docs/system-foundation/11-architecture-reassessment-and-hard-refactor-decision.md`
- `docs/system-foundation/12-document-consistency-audit-and-execution-order.md`

Do not read all foundation, refactor, or experiment records. Open an older source only to resolve a specific overlap or provenance question.

## Known facts

- Logical routing is complete without moving the historical corpus.
- The default onboarding set is four files, within the enforced line and word budget.
- System-foundation 01-05 are durable design sources; 06-10 describe an earlier assessment and plan; 11-12 reinterpret the series after later evidence.
- ADR 0005 currently has no authority effect.
- Full Git bundle transport gives the web-chat sandbox ordinary Git objects and a working tree.

## Pending external inputs

None. See [`PENDING_ARTIFACTS.yaml`](PENDING_ARTIFACTS.yaml).

## Next valid action

Review the proposed assurance classes and risk modifiers against the project’s reference-first philosophy, then produce an explicit constitutional target map showing which current sources remain canonical, which are consolidated, and which become historical design provenance.

## Stop conditions

Stop before implementation if:

- the constitutional target would erase important project motivation or evidence principles;
- ADR 0005 would silently accept or reject a provider rather than define evidence depth;
- a physical move lacks complete inbound-link migration and a repository-wide link check;
- the result creates two competing canonical copies;
- the required-reading set expands rather than contracts without a concrete reason.

## Completion criteria

- Project purpose, invariants, evidence philosophy, and agent authority each have one canonical home.
- System-foundation lifecycle and precedence are mechanically clear.
- ADR 0005 has an explicit final status and rationale.
- The provider-authority next action follows from the accepted policy rather than historical momentum.
- Default onboarding remains bounded and history-free.
- The next implementation phase is repository-owned and does not depend on chat memory.
