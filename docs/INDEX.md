
# Documentation index

Use this page to route a question to the smallest authoritative document set. The authority and lifecycle rules are defined in [`DOCUMENTATION_MODEL.md`](DOCUMENTATION_MODEL.md); canonical metadata is in [`catalog.tsv`](catalog.tsv).

## Current work

| Question | Read |
|---|---|
| What is the project and where is it now? | [`current/BRIEF.md`](current/BRIEF.md) |
| What should the active agent do next? | [`current/ACTIVE_TASK.md`](current/ACTIVE_TASK.md) |
| What is the machine-readable semantic state? | [`current/STATE.yaml`](current/STATE.yaml) |
| Is an external result or package blocking progress? | [`current/PENDING_ARTIFACTS.yaml`](current/PENDING_ARTIFACTS.yaml) |

## Authority routers

| Question class | Router |
|---|---|
| Project identity, invariants, and durable philosophy | [`constitution/README.md`](constitution/README.md) |
| Current integrated system and component contracts | [`architecture/README.md`](architecture/README.md) |
| User/agent collaboration, tools, and platform behavior | [`operations/README.md`](operations/README.md) |
| Accepted, proposed, superseded, or historical choices | [`decisions/README.md`](decisions/README.md) |
| Experiments, receipts, and transaction evidence | [`evidence/README.md`](evidence/README.md) |
| Chronology and earlier state reconstruction | [`history/README.md`](history/README.md) |
| Reusable systems mechanisms and mental models | [`knowledge/README.md`](knowledge/README.md) |

## Component ownership

| Question | Read |
|---|---|
| Which project-authored modules own physical integration? | [`../modules/README.md`](../modules/README.md) |
| Which package owns an external payload or provider lifecycle? | [`../packages/README.md`](../packages/README.md) |
| Where is Mesa build/provider ownership documented? | [`../packages/mesa-glibc/README.md`](../packages/mesa-glibc/README.md) |

## Historical access rule

Historical evidence is not default onboarding material. A current task must name the specific record and the question being reconstructed. Do not scan `refactor/`, dated handoffs, or large experiment reports merely to become generally familiar with the project.
