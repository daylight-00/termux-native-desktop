
# ADR 0005: Proportional assurance depth

- **Status:** proposed
- **Decision type:** evidence and promotion policy
- **Scope:** providers, adaptations, reproduced builds, custom compositions, and other promoted technical objects
- **No authority effect:** this proposal does not accept a provider, resume SUP-02, populate a target, or activate a successor

## Context

The provider-authority workstream expanded from exact identity and runtime closure into producing-build provenance, artifact/member binding, supplier requests, and custodian export protocols. Those steps were internally consistent with the then-current evidence ladder, but the project lacked a policy that bounded assurance depth according to the actual deviation and consequence of a path.

The project prefers upstream and reference implementations. It also sometimes adapts, reproduces, or invents components because Android/Termux is not a reference deployment environment. Treating every path as either “trust upstream completely” or “prove every possible provenance edge” is not practical.

The project needs an explicit decision surface before additional evidence production resumes.

## Proposed decision

Assurance depth is selected before evidence collection from two inputs:

```text
implementation class
    +
risk modifiers
```

Evidence must be sufficient for the declared class and risk. It must not expand automatically merely because another possible proof can be imagined.

### Implementation classes

#### A. Reference-consumed

An official or authoritative reference artifact is consumed without semantic modification on a compatible platform path.

Minimum assurance:

```text
exact artifact identity and source
compatibility/ABI boundary check
intended configuration and provider selection
bounded functional or runtime acceptance
rollback or replacement path
```

Producing-build reconstruction is not required by default when the authoritative supplier already owns that claim and no material mismatch is observed.

#### B. Reference-adapted

A reference artifact is used with a narrow adapter, patch, wrapper, policy override, path transformation, or platform-specific composition.

Minimum assurance:

```text
all reference-consumed checks
exact adaptation diff or contract
reason the adaptation is necessary
targeted tests for changed semantics
check that unchanged reference assumptions remain valid
```

Assurance focuses on the adaptation boundary rather than reproducing unrelated upstream proofs.

#### C. Independently reproduced

The project rebuilds or reconstructs a reference result from source, recipe, or a compatible producing process.

Minimum assurance:

```text
source and recipe identity
toolchain and build-environment identity at the needed granularity
recorded producing invocation and output manifest
expected ABI/member/SONAME contract
functional equivalence or justified divergence
```

Bit-for-bit reproduction is required only when it is part of the declared requirement or when opacity/consequence makes weaker equivalence insufficient.

#### D. Novel or custom

The project invents a provider, bridge, composition, policy, or lifecycle with no authoritative reference implementation for the exact target.

Minimum assurance:

```text
explicit requirements and non-goals
failure and threat model proportional to consequence
comparison baseline or control
multi-layer validation of the claimed behavior
observability and rollback
independent re-review before broad promotion when consequence is high
```

Novelty does not imply unlimited proof. It does require explicit ownership of the assumptions that a reference supplier would otherwise own.

### Risk modifiers

Increase assurance within a class when one or more of these are high:

```text
deviation from the reference path
supplier or artifact opacity
privilege or security impact
persistence and blast radius
ABI or data-corruption consequence
irreversibility
number and diversity of consumers
weak observability
lack of a replaceable fallback
```

Reduce additional proof when the path is low-impact, reversible, directly observable, narrowly scoped, and replaceable by an authoritative reference.

## Required review record

Before an evidence campaign or promotion, record:

```text
object being judged
implementation class
risk modifiers
minimum evidence set
explicitly excluded evidence
acceptance and stop conditions
rollback boundary
```

Missing required evidence may block promotion. It does not automatically authorize broader acquisition. Expanding the evidence set requires an explicit review explaining which risk or uncertainty changed.

## Relationship to the evidence ladder

The existing distinction remains valid:

```text
observation
candidate
identity/provenance binding
provider authority
composition
target population
activation
acceptance
```

This ADR changes how much evidence is required to move between states. It does not collapse the states or allow successful launch to imply provider authority.

## Application to the paused SUP-02 boundary

Before any SUP-02 response production resumes, classify each affected provider/object under this policy and decide whether exact custodian producing-build exports are:

```text
required for the declared assurance class;
replaceable by authoritative supplier identity plus bounded adaptation evidence;
required only for a smaller high-risk subset; or
no longer justified for the intended project claim.
```

Until this proposal is reviewed and accepted or replaced, the existing provider-authority boundary remains paused and no target population follows.

## Consequences if accepted

Positive:

- evidence work becomes bounded before collection starts;
- reference paths receive appropriate reliance instead of automatic re-prosecution;
- custom adaptations receive focused scrutiny at the changed boundary;
- high-risk novel paths still receive deeper validation;
- stop conditions become enforceable.

Costs:

- every promotion needs an explicit class and risk review;
- disagreements move to the assurance-selection decision rather than being hidden in evidence volume;
- existing provider records may need reclassification before work resumes.

## Alternatives

### Uniform maximum provenance

Rejected as a default proposal because it can consume unbounded effort without changing the practical claim.

### Trust any upstream or package-manager artifact

Rejected because Android/Termux adaptation, mixed ABI worlds, runtime-loaded members, and provider composition can invalidate reference assumptions.

### Case-by-case evidence without a shared policy

Rejected because it reproduces the current drift and makes successor sessions reconstruct the assurance rationale from history.
