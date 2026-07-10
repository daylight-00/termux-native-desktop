# System Foundation and Target Architecture

> **Status:** design foundation and target model, not a declaration that the repository already implements every element described here.
>
> **Refactoring note:** another development session may be actively refactoring the repository. This set therefore defines stable reasoning, boundaries, target contracts, and migration order. It intentionally avoids assuming that every current path or file layout will remain unchanged.
>
> **Precedence note:** `11-architecture-reassessment-and-hard-refactor-decision.md` is the latest architectural reasoning and decision authority. `12-document-consistency-audit-and-execution-order.md` is the current cross-document consistency index and execution-order guide. Where earlier migration documents can be read as requiring preservation of current command names, compatibility facades, the broad farm, or the `gl` umbrella object, documents 11 and 12 take precedence. Preserve validated semantics and evidence, not accidental object identity.

This documentation set starts above individual implementations. It asks:

> What is the project fundamentally building, which constraints are essential, what system model follows from those constraints, what would an ideal implementation look like, and how should the current system evolve toward it without destroying validated behavior?

The project was discovered bottom-up. A practical need led to experiments; experiments exposed ABI boundaries, loader behavior, path assumptions, display transport, GPU provider selection, and evidence requirements. That discovery process was necessary. The next stage is to synthesize those findings into architecture.

The intended relationship is:

```text
discovery loop
need -> obstacle -> hypothesis -> experiment -> evidence -> conclusion
                                      |
                                      v
synthesis loop
mission -> invariant -> architecture -> contract -> implementation -> validation
                                      ^
                                      |
                              new evidence refines model
```

Neither pure bottom-up accumulation nor pure top-down design is sufficient. The architecture must constrain implementation, while experiments remain able to correct the architecture.

## Reading order

1. [`01-essence.md`](01-essence.md) — the project’s abstract identity, mission, boundaries, and non-goals.
2. [`02-principles-and-invariants.md`](02-principles-and-invariants.md) — the proposed constitutional rules that implementation must preserve.
3. [`03-system-model-v2.md`](03-system-model-v2.md) — a six-plane model separating host, bridges, capabilities, application domains, supply/build, and knowledge/control.
4. [`04-domain-capability-bridge-model.md`](04-domain-capability-bridge-model.md) — a reusable object model for applications such as VS Code, Obsidian, and PyMOL.
5. [`05-ideal-target-architecture.md`](05-ideal-target-architecture.md) — the concrete target state: ownership, runtime materialization, manifests, providers, launch composition, and promotion.
6. [`06-current-state-assessment.md`](06-current-state-assessment.md) — comparison of the original pre-refactor repository/runtime model with the target.
7. [`07-gap-analysis-and-refactoring-strategy.md`](07-gap-analysis-and-refactoring-strategy.md) — original migration strategy centered on validation and gradual responsibility transfer.
8. [`08-implementation-roadmap.md`](08-implementation-roadmap.md) — phased implementation order and concrete deliverables as originally proposed.
9. [`09-validation-promotion-and-evidence.md`](09-validation-promotion-and-evidence.md) — validation gates, promotion rules, evidence quality, and rollback.
10. [`10-open-design-questions.md`](10-open-design-questions.md) — decisions intentionally left open until further evidence exists.
11. [`11-architecture-reassessment-and-hard-refactor-decision.md`](11-architecture-reassessment-and-hard-refactor-decision.md) — reconciliation with the refactor branch and ABI incident; supersession rules, `gl` object critique, farm lifecycle judgment, substrate authority, and hard-refactor sequence.
12. [`12-document-consistency-audit-and-execution-order.md`](12-document-consistency-audit-and-execution-order.md) — document authority map, resolved apparent contradictions, settled/open decision matrix, implementation stop line, and current execution order.
13. [`REFERENCES.md`](REFERENCES.md) — project-local and external references.

## Document evolution and precedence

The documents are intentionally historical as well as normative. Earlier files capture the strongest model available when they were written; later evidence may refine them.

Use this rule:

```text
stable invariant
    -> keep unless strong evidence changes the project definition

current-state observation
    -> interpret in its recorded repository/runtime context

migration tactic
    -> may be superseded when a better object model is established

implementation decision
    -> replaceable
```

In particular:

```text
preserve validated semantics
preserve evidence
preserve rollback ability

!=

preserve gl-run
preserve gl-farm
preserve ~/gl/env as a monolith
preserve modules/gl as one semantic owner
preserve one package-manager integration
```

When deciding what to do next:

```text
11
    -> why the direction changed and what the architecture decides

12
    -> how all documents fit together and what the current execution order is
```

## Relationship to existing repository documents

This set has a different responsibility from existing guides:

```text
PROJECT_CONTEXT.md
    -> why the project exists and how it evolved

architecture.md
    -> current integrated system model

glibc-layer.md / gpu.md / desktop-session.md
    -> current operational contracts

experiments/
    -> first-hand provenance and investigations

system-foundation/
    -> abstract identity, invariants, target architecture,
       reassessment, consistency audit, and migration model
```

The target architecture should not rewrite historical experiment reports to pretend the final model existed from the beginning. It should consume their evidence and make future changes more coherent.

## Core thesis

The project is best understood as:

> **A heterogeneous userspace composition system for a non-root Android workstation: it keeps the Android/Termux host native, constructs coherent foreign application runtime domains beside it, connects worlds through explicit bridges, provides hardware and desktop capabilities through ABI-appropriate providers, and promotes only experimentally validated contracts into the live system.**

The latest architectural rationale is in document 11; the current cross-document interpretation and execution order are in document 12.
