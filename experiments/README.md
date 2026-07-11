# Experiments

`experiments/` is the living workbench of the project.

## Record contract

Each experiment has one current interpretation and may have deeper provenance:

```text
experiment/
├── README.md     # concise canonical record: current interpretation
├── report.md     # detailed session-derived report, when available
├── evidence/     # raw traces, logs, tables, captures worth preserving
├── recipe/       # experiment-specific reproduction material, when useful
└── work/         # local scratch space; ignored
```

The canonical `README.md` may state that a detailed report or recipe used an intermediate architecture later superseded by evidence. Historical reports are preserved rather than rewritten to make the final model appear inevitable.

Recommended README shape:

```text
Status / dates / provenance
Question
Baseline
Hypothesis
Procedure
Evidence
Result
Decision
Current interpretation / superseded details
Revalidation or stop line
```

Information flow:

```text
experiment
  -> evidence
  -> interpretation correction
  -> working conclusion (STATUS.md)
  -> durable contract/decision
  -> active gate or historical diagnostic classification
  -> module / package / integrated guide
```

## Tool lifecycle after experiment closure

Recipe files are not automatically permanent tests.

Classify them as:

```text
ACTIVE_CONTRACT_GATE
CANONICAL_EVIDENCE_HELPER
HISTORICAL_DIAGNOSTIC
SUPERSEDED_FALSE_NEGATIVE_MODEL
```

Minimum manipulation requires keeping only the necessary active gate surface while preserving evidence and history.

## Provenance labels

- **first-hand report** — detailed record from the session that performed the experiment.
- **first-hand summary** — concise record written from direct work/evidence without a separate full report.
- **reconstructed** — assembled later from another preserved record.
- **stub** — timeline-level fact only; details intentionally not invented.

## Index

| track | experiment | current status | provenance |
|---|---|---|---|
| desktop | `session-launch` | passed; launcher promoted | first-hand summary |
| glibc | `miniforge-conda` | passed | first-hand report |
| glibc | `rootfs-as-library-pool` | passed current compatibility baseline; not final provider architecture | first-hand summary |
| glibc | `vscode` | passed current GPU/CPU application branches | first-hand report + canonical summaries |
| glibc | `obsidian-appimage` | passed current extracted payload onboarding | first-hand report |
| glibc | `selected-dbus-closure` | passed bounded selected-provider candidate | first-hand experiment |
| glibc | `selected-obsidian-closure` | active/incomplete; graphics sub-question closed, selected candidate/locality equivalence open | first-hand experiment |
| glibc | `vulkan-policy-composition` | closed scoped transaction; trigger-based revalidation only | first-hand experiment + closure records |
| gpu | `chromium-bionic-gpu` | passed conventional GPU path | first-hand report |
| gpu | `mesa-glibc-26.0.6` | passed; historical control | first-hand report + later controls |
| gpu | `mesa-bionic-26.1.4` | passed; bionic daily-driver lineage | first-hand report + later validation |
| gpu | `mesa-26.1.4-present-sigbus` | investigation closed; practical fix adopted; low-level mechanism open | first-hand summary + raw evidence + recipe |
| gpu | `glibc-cross-toolchain` | passed | first-hand summary |
| gpu | `zink-runtime-contract` | passed current composition | first-hand summary |
| gpu | `vscode-angle-vulkan` | passed selected Turnip/Adreno path | first-hand report |
| gpu | `picom-glx` | abandoned | stub |
| gpu | `video-accel` | unresolved/abandoned paths | stub |
| gpu | `webgpu` | desired native adapter path unsuccessful | first-hand report |
| workflow | `remote-development/open-remote-ssh` | unsuccessful; deterministic download mismatch isolated | first-hand report |
| workflow | `remote-development/official-tunnels-from-code-oss` | unsuccessful; final negotiation rejection isolated | first-hand report |
| workflow | `python/uv-base` | passed | first-hand report |

## Current architecture-sensitive experiments

### Selected Obsidian closure

This is the active parent architecture-discrimination pilot.

It must either:

```text
complete locality-preserving candidate materialization/equivalence
```

or:

```text
terminate explicitly with remaining unanswered questions documented
```

before PyMOL is allowed to inherit a provider/application closure model.

### Vulkan policy composition

This experiment is closed.

Do not expand it for unrelated application, WebGPU, video, zero-copy, or PyMOL work.

Canonical closure:

```text
docs/refactor/0091-scoped-graphics-policy-promotion-closure.md
```

Post-closure audit:

```text
docs/refactor/0092-post-graphics-closure-architecture-midpoint-audit.md
```

A failed experiment is not a failed repository entry. When it isolates a boundary, corrects an observability model, or eliminates a tempting explanation, it remains part of the knowledge/control plane.
