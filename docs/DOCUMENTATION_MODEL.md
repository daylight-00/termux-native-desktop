
# Documentation authority and lifecycle model

This document defines how the repository separates current state, durable contracts, architecture, operations, decisions, evidence, history, and reusable knowledge. It is the canonical answer to the question: **which document should an agent trust for which kind of claim?**

The repository is not a flat reading list. Different document classes answer different questions and have different lifecycles.

## Authority by question

There is no single total ordering that makes one document class universally superior to every other class. Route the question first.

| Question | Authority class | Canonical entry point |
|---|---|---|
| What is happening now and what should be done next? | current state | [`current/`](current/) |
| What is this project fundamentally building and what must remain invariant? | constitution | [`constitution/`](constitution/) |
| How is the current system composed and operated? | architecture | [`architecture/`](architecture/) |
| How do the user and agent collaborate and exchange work? | operations | [`operations/`](operations/) |
| Which durable choice was accepted, proposed, superseded, or rejected? | decisions | [`decisions/`](decisions/) |
| What was observed, tested, or produced? | evidence | [`evidence/`](evidence/) |
| What happened during an earlier transition? | history | [`history/`](history/) |
| How does the underlying Linux, Android, ABI, loader, GPU, or IPC mechanism work? | knowledge | [`knowledge/`](knowledge/) |

A current task may cite evidence or history, but evidence and history do not become current authority merely because they are detailed.

## Document classes

### Current state

`docs/current/` owns only rapidly changing semantic state:

```text
current project boundary
active task
pending external artifacts
machine-readable state
```

Exactly one active task is allowed. Current state must be updated in the same accepted repository transition that changes the project boundary. It must not depend on a future session-close narrative.

### Constitution

The constitutional class owns stable project identity and engineering invariants:

```text
project purpose and non-goals
host and ABI authority
reference-first and minimal-deviation policy
evidence and promotion principles
agent/user authority boundary
```

Constitutional changes require an explicit durable decision or a clearly recorded correction. They must not be introduced silently through an experiment report or active-task summary.

### Architecture

Architecture documents describe the current integrated system model and its durable component contracts. They may evolve more often than the constitution but must distinguish:

```text
current validated realization
active target architecture
historical or transitional implementation
```

A path or helper is not permanent architecture merely because it currently works.

### Operations

Operations documents own progress-independent collaboration, tooling, packaging, validation, and platform behavior. They must remain usable even when the active research topic changes.

### Decisions

Decision records use one of these lifecycle states:

```text
proposed
accepted
superseded
rejected
historical
```

Only `accepted` decisions are binding. A `proposed` record is a review surface, not permission to mutate runtime or accept authority. A superseded record remains evidence for why the project once acted differently.

### Evidence

Evidence includes experiment interpretations, detailed reports, raw captures, receipts, and transaction records. Evidence answers what was observed or produced. It does not automatically answer what should be promoted.

The experiment `README.md` is the current interpretation of that experiment. A detailed `report.md` remains first-hand provenance and may describe a later-superseded architecture.

### History

History preserves chronology and old session/refactor transitions. Historical documents are never default onboarding material. Open one only when the active task names a concrete reconstruction need.

### Knowledge

Knowledge documents explain reusable mechanisms and mental models. They may support reasoning but do not override current project state, accepted decisions, or project-specific evidence.

## Lifecycle statuses

The machine-readable catalog uses these statuses:

| Status | Meaning |
|---|---|
| `current` | canonical current or durable document |
| `accepted` | binding durable decision |
| `proposed` | explicit review surface, not yet binding |
| `superseded` | replaced for current use but retained as provenance |
| `historical` | chronology or past-state record |
| `evidence` | observation, receipt, or experiment record |
| `reference` | reusable background or external-facing index |
| `mixed` | index over children with different statuses |

Directories with many historical leaves do not need one catalog row per file. Their index assigns inherited classification to the contained records.

## Conflict handling

When documents appear to conflict:

1. identify the question class;
2. use the canonical entry point for that class;
3. check accepted decisions that explicitly govern the issue;
4. treat older assessments, reports, and handoffs as provenance;
5. record and repair the inconsistency rather than silently choosing the convenient document.

Current state cannot silently repeal a constitutional invariant or accepted decision. An accepted decision cannot rewrite an observed fact. Evidence can force a constitutional or architectural review, but the review must be explicit.

## Default onboarding budget

Default web-chat onboarding is intentionally bounded to:

```text
START_HERE.md
AGENTS.md
docs/current/BRIEF.md
docs/current/ACTIVE_TASK.md
```

The catalog marks these four documents with `default_onboarding=yes`.

Budget:

```text
maximum default-onboarding files: 4
maximum combined lines: 450
maximum combined words: 3500
historical files loaded by default: 0
```

The active task may add at most eight required-reading documents. It should select the smallest set that resolves the task. Platform profiles are loaded when the task reaches platform-specific repository transport, file exchange, or device execution, unless the active task explicitly requires one earlier.

## Physical reorganization rule

Logical authority is defined before files are moved. A physical move is justified only when it improves navigation or ownership enough to outweigh link churn.

Every move must:

```text
use git mv
update all live Markdown links in the same transition
preserve historical prose that accurately names an old path
keep evidence contents unchanged unless correcting a factual error
pass repository-wide link validation
avoid duplicate canonical copies or compatibility stubs unless a public path contract requires one
```

The first structure-consolidation phase therefore adds canonical routers and metadata without moving the large historical corpus. Later phases may consolidate constitutional and architectural source documents using this rule.

## Machine-readable catalog

[`catalog.tsv`](catalog.tsv) records the canonical routers and key authority documents. It is intentionally not a 284-file inventory. Large evidence and history trees inherit their class from their canonical directory index.

The catalog is validated by `tools/docs/check-document-model`.
