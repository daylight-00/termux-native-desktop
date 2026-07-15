# Active task: consolidate documentation authority and structure

> Task ID: `documentation-structure-consolidation`
>
> Expected state on completion: the repository has an agreed durable/current/history documentation model, a bounded default onboarding set and an explicit decision surface for proportional assurance depth.

## Objective

Design and implement the next bounded documentation reorganization so project philosophy, current state, architecture, operating rules, decisions, evidence and history have unambiguous authority and routing.

## Why now

Bundle-native onboarding and current-authority synchronization are complete. The remaining documents are still numerous and partly overlapping. Without a deliberate authority model, later agents may load superseded foundation assessments or reconstruct the project from transaction history instead of current contracts.

The paused provider-authority workstream also exposed a missing policy: how much assurance is justified when following a reference path versus adapting, independently reproducing or inventing a provider.

## Current accepted decisions

- Web-chat sessions start from a user-provided full Git bundle and `START_HERE.md`.
- `docs/current/` owns current semantic state and the active task.
- Narrative handoffs are historical evidence only.
- `main` is the sole intended long-lived branch.
- Repository deployment is immutable and explicitly activated.
- Mesa mutable workspace and provider candidates are owned under XDG state.
- The provider-authority workstream remains paused at the 0165 no-response boundary.

## In scope

- Define a concise documentation authority model covering constitution, current state, architecture, operations, decisions, evidence, history and knowledge.
- Decide whether physical moves are needed or whether indexes/status metadata are sufficient.
- Consolidate overlapping project-essence and system-foundation material without losing provenance.
- Add status metadata or indexes for accepted, superseded and historical decisions/documents.
- Define a bounded default onboarding reading set and context-budget expectations.
- Draft the proportional assurance-depth policy and its relation to reference, adapted, reproduced and novel paths.
- Add machine-checkable rules that prevent current and historical authority from being mixed again.

## Out of scope

- Rewriting 0001–0165 transaction records.
- Moving every experiment report in one transaction.
- Resuming SUP-02 evidence acquisition or producing supplier responses.
- Device runtime, graphics or application testing.
- Provider target population, extraction or selected-generation activation.
- Adopting Codex or Claude Code as the current execution environment.

## Required reading

- `docs/current/BRIEF.md`
- `docs/current/STATE.yaml`
- `AGENTS.md`
- `docs/INDEX.md`
- `docs/PROJECT_CONTEXT.md`
- `docs/PROJECT_PRINCIPLES.md`
- `docs/system-foundation/README.md`
- `docs/system-foundation/11-architecture-reassessment-and-hard-refactor-decision.md`
- `docs/system-foundation/12-document-consistency-audit-and-execution-order.md`
- `docs/architecture.md`
- `docs/decisions/README.md`
- `docs/session-operations/README.md`

Do not read all numbered refactor records or experiment reports. Open a specific historical source only to resolve a concrete provenance question encountered during consolidation.

## Known facts

- Current-facing branch, deployment, local-layout and session-operation documents have been synchronized.
- Historical documents intentionally retain old paths and old branch names where they describe past facts.
- The document corpus is large enough that default onboarding must be routed rather than exhaustive.
- Full Git bundle transport gives the web-chat sandbox ordinary Git objects and a working tree; GitHub raw-content reconstruction is unnecessary and undesirable.

## Pending external inputs

None. See [`PENDING_ARTIFACTS.yaml`](PENDING_ARTIFACTS.yaml).

## Next valid action

Produce a proposed documentation authority matrix and target tree, map every existing document class into it, and identify the smallest first physical reorganization that improves routing without breaking historical links unnecessarily.

## Stop conditions

Stop before implementation if:

- the proposal requires destructive rewriting of evidence history;
- a move would create more broken links than the routing benefit justifies without an automated migration plan;
- the assurance policy would silently accept or reject provider authority rather than defining evidence depth;
- the initial onboarding set exceeds its intended bounded context without a clear justification.

## Completion criteria

- Every document class has one explicit authority and lifecycle role.
- Current, superseded and historical material are mechanically distinguishable.
- A new web-chat agent can find needed documents by question without scanning the corpus.
- The default onboarding set remains small and excludes unrelated history.
- Assurance depth has an explicit draft decision surface tied to deviation and risk.
- The next implementation phase is repository-owned and does not depend on chat memory.
