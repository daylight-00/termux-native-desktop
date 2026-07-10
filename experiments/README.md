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

The `README.md` is allowed to say that a historical `report.md` used an intermediate architecture later superseded by the project. The report itself is preserved rather than rewritten to make the final architecture appear inevitable.

Recommended README shape:

```text
Status / Dates / Provenance
Question
Baseline
Hypothesis
Procedure
Evidence
Result
Decision
Current interpretation / superseded details
```

Information flow:

```text
experiment
  -> evidence
  -> working conclusion (STATUS.md)
  -> durable decision (docs/decisions/)
  -> module / package / test / integrated guide
```

Provenance labels:

- **first-hand report** — a detailed record extracted from the session that performed the experiment.
- **first-hand summary** — concise record written from direct work/evidence, but no separate full report is preserved.
- **reconstructed** — assembled later from another record or summary.
- **stub** — timeline-level fact only; details intentionally not invented.

## Index

| track | experiment | status | provenance |
|---|---|---|---|
| desktop | `session-launch` | passed; launcher promoted | first-hand summary |
| glibc | `miniforge-conda` | passed | first-hand report |
| glibc | `rootfs-as-library-pool` | passed; layer foundation | first-hand summary |
| glibc | `vscode` | passed | first-hand report + current canonical summary |
| glibc | `obsidian-appimage` | passed | first-hand report |
| glibc | `selected-dbus-closure` | passed bounded selected-provider candidate | first-hand experiment |
| glibc | `selected-obsidian-closure` | active; semantic decomposition and graphics-policy A/B complete | first-hand experiment |
| glibc | `vulkan-policy-composition` | active; scoped producer/consumer validation stage | first-hand experiment |
| gpu | `chromium-bionic-gpu` | passed conventional GPU path | first-hand report |
| gpu | `mesa-glibc-26.0.6` | passed; historical control | first-hand report + later controls |
| gpu | `mesa-bionic-26.1.4` | passed; bionic daily-driver lineage | first-hand report + later validation |
| gpu | `mesa-26.1.4-present-sigbus` | passed investigation; fix adopted | first-hand summary + raw evidence + recipe |
| gpu | `glibc-cross-toolchain` | passed | first-hand summary |
| gpu | `zink-runtime-contract` | passed | first-hand summary |
| gpu | `vscode-angle-vulkan` | passed | first-hand report |
| gpu | `picom-glx` | abandoned | stub |
| gpu | `video-accel` | unresolved/abandoned paths | stub |
| gpu | `webgpu` | desired native adapter path unsuccessful | first-hand report |
| workflow | `remote-development/open-remote-ssh` | unsuccessful; deterministic download mismatch isolated | first-hand report |
| workflow | `remote-development/official-tunnels-from-code-oss` | unsuccessful; final negotiation rejection isolated | first-hand report |
| workflow | `python/uv-base` | passed | first-hand report |

A failed experiment is not a failed repository entry. When it isolates a boundary or eliminates a tempting but incorrect explanation, it should stay.
