# Constitutional documentation

This directory is the compact current authority for project identity and stable engineering philosophy.

## Canonical surface

| Question | Canonical document |
|---|---|
| What is the project building, where is its boundary, and what is it not? | [`PROJECT.md`](PROJECT.md) |
| Which engineering, evidence, promotion, and assurance principles are invariant? | [`PRINCIPLES.md`](PRINCIPLES.md) |
| What may agents and users do, and which environment is authoritative? | [`../../AGENTS.md`](../../AGENTS.md) |
| Which durable choices are accepted, proposed, superseded, or rejected? | [`../decisions/README.md`](../decisions/README.md) |

These documents have non-overlapping ownership:

```text
PROJECT.md
    -> identity, purpose, boundary, quality goals, non-goals

PRINCIPLES.md
    -> engineering invariants, evidence states, promotion and assurance

AGENTS.md
    -> agent/user authority, context, transport and execution discipline
```

## Design provenance

The following remain valuable but are not competing current authority:

- [`../PROJECT_CONTEXT.md`](../PROJECT_CONTEXT.md) — historical motivation and early project evolution.
- [`../PROJECT_PRINCIPLES.md`](../PROJECT_PRINCIPLES.md) — earlier evidence doctrine before proportional assurance was adopted.
- [`../system-foundation/`](../system-foundation/README.md) — detailed top-down design, assessment, roadmap, validation, reassessment, and consistency provenance.

Open those sources only for a named provenance or design question. Current architectural realization is routed through [`../architecture/README.md`](../architecture/README.md).

## Constitutional change

A change to project identity or an invariant requires an accepted decision or an explicit correction. Current-task prose, experiments, receipts, and historical records cannot silently modify this surface.
