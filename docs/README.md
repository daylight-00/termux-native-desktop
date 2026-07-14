# Documentation map

The repository separates current integrated knowledge from experiment provenance and from session-level operating rules.

## Start here

- [`PROJECT_PRINCIPLES.md`](PROJECT_PRINCIPLES.md) — project purpose, evidence ladder and authority philosophy.
- [`session-operations/README.md`](session-operations/README.md) — new-session initialization and durable collaboration rules.
- [`handoff/CURRENT.md`](handoff/CURRENT.md) — compact pointer to the current project-state handoff.
- `PROJECT_CONTEXT.md` — why the project exists and how the workstreams evolved.
- `architecture.md` — current whole-system model.
- `glibc-layer.md` — conventional Linux/glibc application layer: bootstrap, boundaries, onboarding, traps, maintenance.
- `gpu.md` — glibc Mesa/Turnip/Zink operational model and diagnostic history.
- `desktop-session.md` — Termux:X11 + XFCE two-world session contract.
- `timeline.md` — chronological navigation aid.
- `decisions/` — durable choices whose rationale should survive individual experiments.

## Documentation ownership

```text
PROJECT_PRINCIPLES.md
    durable project philosophy and evidence/authority rules

session-operations/
    durable agent/user collaboration, packaging and transition rules

handoff/
    current and historical project-state transition records

refactor/ and experiments/
    project decisions, implementations, receipts and provenance
```

Do not copy durable collaboration rules into every dated handoff. A dated handoff links to `session-operations/` and records only the project-specific state that can change between sessions.

## Evidence relationship

Integrated guides summarize the current interpretation. Detailed first-hand session reports, reconstructed records, and raw traces remain under `../experiments/`.

```text
experiment report / evidence
        -> canonical experiment README
        -> STATUS working conclusion
        -> decision record, when durable
        -> integrated guide / promoted artifact
```

## Constitutional foundation

- [`knowledge/README.md`](knowledge/README.md) — systems-study map and references.
- [`system-foundation/README.md`](system-foundation/README.md) — project essence, invariants, target model and execution precedence.
- [`decisions/0004-single-main-and-immutable-release-deployment.md`](decisions/0004-single-main-and-immutable-release-deployment.md) — canonical branch and deployment authority.
