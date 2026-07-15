# ADR 0005: Risk-proportional assurance at changed boundaries

- **Status:** accepted
- **Accepted:** 2026-07-15
- **Decision type:** evidence and promotion policy
- **Scope:** providers, artifacts, adaptations, reproduced builds, custom compositions, and other promoted technical objects
- **No direct promotion effect:** this decision does not accept a provider, resume an acquisition batch by itself, populate a target, or activate a successor

## Context

The provider-authority workstream expanded from runtime identity and closure into producing-build provenance, artifact/member binding, supplier requests, and custodian export protocols. Those steps were internally consistent with an unbounded reading of the evidence ladder, but the project had no policy for deciding how much evidence a specific claim actually required.

The project is reference-first. It consumes authoritative upstream and distribution artifacts where practical, adapts them where Android/Termux requires a narrow deviation, reproduces some components, and invents a smaller number of custom compositions. Treating every path as either “trust everything” or “re-prove the complete supply chain” is neither sound nor practical.

## Decision

Assurance is selected **before** evidence collection from:

```text
claim being made
    + implementation class
    + risk modifiers
```

Evidence must be sufficient for the declared claim, class, and consequence. It must not expand automatically merely because another possible proof can be imagined.

The project reviews the boundary it owns:

```text
authoritative supplier claim
    + project transfer/integration
    + any project deviation
    + runtime selection and consequence
```

It does not routinely re-prosecute an authoritative supplier's unchanged producing history unless the project claim, observed mismatch, opacity, or risk requires it.

## Implementation classes

### A. Reference-consumed

An official or authoritative reference artifact is consumed without semantic modification on a compatible path.

Minimum assurance:

```text
authoritative source and exact consumed artifact identity
compatibility and ABI boundary check
intended configuration/provider selection
bounded functional or runtime acceptance
replacement or rollback path
```

Not required by default:

```text
supplier producing-build reconstruction
independent bit-for-bit reproduction
unrelated dependency-family provenance
custodian export beyond the supplier's declared artifact boundary
```

Those items require an explicit escalation trigger.

### B. Reference-adapted

A reference artifact is used with a narrow patch, wrapper, path transformation, policy override, ABI adaptation, or platform-specific composition.

Minimum assurance:

```text
all applicable reference-consumed checks
exact adaptation diff or contract
reason the adaptation is necessary
targeted tests for changed semantics
checks for reference assumptions touched by the adaptation
```

The unchanged supplier boundary remains relied upon unless evidence shows that the adaptation invalidates it.

### C. Independently reproduced

The project rebuilds or reconstructs a reference result and claims ownership of the produced artifact or equivalence.

Minimum assurance:

```text
source and recipe identity
toolchain/build-environment identity at claim-relevant granularity
recorded producing invocation and output manifest
expected ABI/member/SONAME contract
functional equivalence or justified divergence
```

Bit-for-bit reproduction is required only when it is an explicit requirement or weaker equivalence cannot bound the relevant risk.

### D. Novel or custom

The project invents a provider, bridge, composition, policy, or lifecycle for which no authoritative reference exists for the exact target.

Minimum assurance:

```text
explicit requirements and non-goals
failure/threat model proportional to consequence
comparison baseline or control
multi-layer validation of the claimed behavior
observability and rollback
independent re-review before broad high-consequence promotion
```

Novelty requires ownership of assumptions; it does not authorize unlimited proof.

## Classification rules

- Classify the **claim**, not merely the file or package. One object may be reference-consumed for artifact identity and reference-adapted for runtime composition.
- A wrapper that only selects an unchanged provider does not automatically make the provider independently reproduced.
- A semantic patch, ABI transformation, or changed producing process moves the affected claim to B or C.
- A project-authored composition with reference components can be D for the composition while its components remain A or B.
- Select the narrowest class that honestly covers the claimed boundary.

## Risk modifiers

Increase assurance within a class when one or more are high:

```text
deviation from the reference path
supplier or artifact opacity
privilege or security impact
persistence and blast radius
ABI, memory-safety, or data-corruption consequence
irreversibility
number and diversity of consumers
weak observability
absence of a replaceable fallback
```

Reduce additional proof when the path is low-impact, reversible, directly observable, narrowly scoped, and replaceable by an authoritative reference.

Risk modifiers do not silently change the claim. If deeper evidence implies a different claim or implementation class, reclassify explicitly.

## Required assurance record

Before an evidence campaign or promotion, record:

```text
object and exact claim
implementation class
supplier/reference boundary relied upon
project-owned deviation
material risk modifiers
minimum evidence set
explicitly excluded evidence
acceptance and stop conditions
runtime-selection proof when applicable
rollback boundary
```

Missing required evidence may block the claim. It does not authorize a broader collector. Expanding the evidence set requires a recorded trigger: changed claim, newly observed mismatch, reclassification, or changed risk.

## Relationship to the evidence ladder

The evidence/promotion states remain distinct:

```text
observation
candidate
identity/provenance appropriate to the claim
provider authority
composition
target population
activation
acceptance
```

This decision bounds the evidence needed to move between states. It does not collapse states or allow successful launch to imply provider authority.

## Application to the paused SUP-02 boundary

The previous SUP-02 process sought exact custodian producing-build invocation, environment, and output manifests for 28 roots as a default next step.

That blanket requirement is no longer the default policy.

Before any supplier-response or acquisition work resumes, each affected claim must be reclassified:

```text
reference-consumed claims
    -> authoritative package/artifact identity plus integration evidence may suffice

reference-adapted claims
    -> focus on the exact Termux/Android adaptation and affected assumptions

independently reproduced claims
    -> producing-build evidence remains required at claim-relevant depth

novel/custom composition claims
    -> validate the project-owned composition and consequence
```

Exact custodian exports remain required only for claims classified C, or for a smaller A/B subset with an explicit escalation trigger. Existing requests and receipts remain historical evidence; they do not compel continuation.

Provider authority, composition, target population, and activation remain open until the reclassification and required evidence reviews are completed.

## Consequences

Positive:

- evidence work is bounded before collection;
- authoritative references receive deliberate reliance instead of automatic re-prosecution;
- project deviations receive focused scrutiny;
- high-risk reproduced or novel paths still receive deeper validation;
- stop conditions and excluded evidence become enforceable;
- successor sessions can understand why a proof was or was not required.

Costs:

- each promoted claim needs a short assurance record;
- existing provider records require reclassification before work resumes;
- disagreement moves to claim/class/risk selection rather than being hidden in evidence volume.

## Rejected alternatives

### Uniform maximum provenance

Rejected as a default because it can consume unbounded effort without changing the practical claim.

### Trust any upstream or package-manager artifact without integration checks

Rejected because Android/Termux adaptation, mixed ABI worlds, runtime-loaded members, and provider selection can invalidate reference assumptions.

### Case-by-case evidence without a shared policy

Rejected because it recreates evidence drift and forces each successor session to reconstruct the rationale from history.
