# Documentation map

The repository separates current integrated knowledge from experiment provenance, foundational study material, and target-architecture reasoning.

## Start here

- `PROJECT_CONTEXT.md` — why the project exists and how the workstreams evolved.
- `architecture.md` — current whole-system model.
- `glibc-layer.md` — conventional Linux/glibc application layer: bootstrap, boundaries, onboarding, traps, maintenance.
- `gpu.md` — glibc Mesa/Turnip/Zink operational model and diagnostic history.
- `desktop-session.md` — Termux:X11 + XFCE two-world session contract.
- `timeline.md` — chronological navigation aid.
- `decisions/` — durable choices whose rationale should survive individual experiments.

## Foundational study and design

- `knowledge/` — progressive systems knowledge layer, from package management and bootstrapping through ELF, processes, filesystems, networking, GPU, build systems, and debugging.
- `system-foundation/` — project essence, architectural invariants, target system model, current-state assessment, refactoring strategy, and implementation/validation roadmap.

The two sets are intentionally different:

```text
knowledge/
    -> understand the mechanisms the project depends on

system-foundation/
    -> derive the project's identity and target architecture from those mechanisms
```

## Evidence relationship

Integrated guides summarize the current interpretation. Detailed first-hand session reports, reconstructed records, and raw traces remain under `../experiments/`.

```text
experiment report / evidence
        -> canonical experiment README
        -> STATUS working conclusion
        -> decision record, when durable
        -> contract and validation gate, when stable
        -> integrated guide / promoted runtime artifact
```
