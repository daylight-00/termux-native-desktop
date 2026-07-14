# Documentation index

Use this page to route a question to the smallest authoritative document set. Do not treat the repository as a flat reading list.

## Current work

| Question | Read |
|---|---|
| What is the project and where is it now? | [`current/BRIEF.md`](current/BRIEF.md) |
| What should the active agent do next? | [`current/ACTIVE_TASK.md`](current/ACTIVE_TASK.md) |
| What is the machine-readable semantic state? | [`current/STATE.yaml`](current/STATE.yaml) |
| Is an external result or package blocking progress? | [`current/PENDING_ARTIFACTS.yaml`](current/PENDING_ARTIFACTS.yaml) |

## Project purpose and durable principles

| Question | Read |
|---|---|
| Why does the project exist? | [`PROJECT_CONTEXT.md`](PROJECT_CONTEXT.md) |
| What evidence and authority rules govern it? | [`PROJECT_PRINCIPLES.md`](PROJECT_PRINCIPLES.md) |
| What is the top-down system model? | [`system-foundation/README.md`](system-foundation/README.md) |
| Which durable choices have been accepted? | [`decisions/`](decisions/) |

## Current architecture and operations

| Question | Read |
|---|---|
| How is the whole system currently composed? | [`architecture.md`](architecture.md) |
| How is the glibc application world operated? | [`glibc-layer.md`](glibc-layer.md) |
| How is graphics composition validated? | [`gpu.md`](gpu.md) |
| How does the Termux:X11 desktop session work? | [`desktop-session.md`](desktop-session.md) |
| How does a web-chat session obtain and modify the repository? | [`operations/platforms/chatgpt-web.md`](operations/platforms/chatgpt-web.md) |
| What are the durable user/agent exchange rules? | [`session-operations/COLLABORATION.md`](session-operations/COLLABORATION.md) |
| How are candidates and result archives constructed and reviewed? | [`session-operations/AGENT_EXECUTION.md`](session-operations/AGENT_EXECUTION.md) |

## Component ownership

| Question | Read |
|---|---|
| Which project-authored modules own physical integration? | [`../modules/README.md`](../modules/README.md) |
| Which package owns an external payload or provider lifecycle? | [`../packages/README.md`](../packages/README.md) |
| Where is Mesa build/provider ownership documented? | [`../packages/mesa-glibc/README.md`](../packages/mesa-glibc/README.md) |

## Evidence and historical reconstruction

| Need | Read |
|---|---|
| Current interpretation of an experiment | The experiment's `README.md` under [`../experiments/`](../experiments/) |
| Detailed first-hand report or raw evidence | The named experiment's report/evidence directory |
| Transaction-level provider/refactor history | [`refactor/README.md`](refactor/README.md), then the specific numbered record |
| Old session transition context | [`handoff/README.md`](handoff/README.md), historical use only |
| Chronological navigation | [`timeline.md`](timeline.md) |

Historical evidence is not default onboarding material. A current task should name the specific record needed and explain why.

## Systems knowledge

For reusable Linux, Android, ELF, ABI, filesystem, IPC, GPU, and experiment-design background, use [`knowledge/README.md`](knowledge/README.md). Knowledge chapters explain mechanisms; they do not override project current state.
