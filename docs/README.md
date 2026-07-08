# Documentation map

The repository separates current integrated knowledge from experiment provenance.

## Start here

- `PROJECT_CONTEXT.md` — why the project exists and how the workstreams evolved.
- `architecture.md` — current whole-system model.
- `glibc-layer.md` — conventional Linux/glibc application layer: bootstrap, boundaries, onboarding, traps, maintenance.
- `gpu.md` — glibc Mesa/Turnip/Zink operational model and diagnostic history.
- `desktop-session.md` — Termux:X11 + XFCE two-world session contract.
- `timeline.md` — chronological navigation aid.
- `decisions/` — durable choices whose rationale should survive individual experiments.

## Evidence relationship

Integrated guides summarize the current interpretation. Detailed first-hand session reports, reconstructed records, and raw traces remain under `../experiments/`.

```text
experiment report / evidence
        -> canonical experiment README
        -> STATUS working conclusion
        -> decision record, when durable
        -> integrated guide / promoted artifact
```
