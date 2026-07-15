# Project constitution: engineering principles

> **Status:** canonical constitutional authority
>
> This document is the single current source for stable engineering, evidence, promotion, and assurance principles. Concrete architecture and current state remain in their own authority classes.

## 1. Native host authority

Android and Termux remain the host authority. Foreign runtime worlds are composed beside the host; they do not redefine it.

## 2. Process ABI purity

Every process must resolve a coherent loader, libc family, low-level runtime, and provider set. Bionic and glibc libraries must not contaminate each other merely because they share a filesystem or display service.

## 3. Explicit bridges

Cross-world interaction occurs through named contracts such as X11, URL opening, files, sockets, or other observable interfaces. A bridge does not imply shared runtime ownership.

## 4. Supply is not runtime authority

An artifact may come from a Termux package, Debian package, AppImage, Conda environment, wheel, source build, cache, or upstream archive. Supply origin does not by itself decide:

```text
semantic role
provider authority
runtime closure
target membership
activation
```

A warehouse or rootfs is useful research and supply state, not automatically a promoted runtime closure.

## 5. Deterministic provider selection

A capability must identify the provider actually selected by the consumer. File presence, package installation, family similarity, or successful startup alone is insufficient when selection matters.

## 6. Smallest valid policy scope

Policy belongs at the narrowest scope that owns the requirement:

```text
host
world
capability/provider
application family
application
single experiment
```

Do not promote a diagnostic override or application-specific workaround into global world policy without evidence that the broader scope is required.

## 7. Reference first; scrutinize the changed boundary

Prefer upstream, authoritative, or mainstream implementations. Reliance on an authoritative reference is a legitimate engineering input, not a defect that must always be re-proven.

When the project adapts a reference path, assurance concentrates on:

```text
the exact deviation
the integration assumptions it changes
the consequence of failure
```

Do not expand evidence collection merely because another proof could be imagined. The binding assurance policy is [`../decisions/0005-proportional-assurance-depth.md`](../decisions/0005-proportional-assurance-depth.md).

## 8. Evidence precedes promotion

Progress moves through distinct claim states:

```text
observation
    -> candidate
    -> identity / provenance appropriate to the claim
    -> provider authority
    -> composition
    -> target population
    -> activation
    -> acceptance
```

A later state is never inferred from an earlier one. Successful launch does not automatically establish provider authority, composition, or target membership.

## 9. Claims have explicit scopes

Every acceptance must state what it proves and what it does not prove. Exact identities are required at the boundary where authority matters, but the required identity depth follows the declared claim and assurance class.

Useful coordinates include, as applicable:

```text
Git commit and tree
artifact or archive digest
package/member path and ELF identity
adaptation diff or contract
producing invocation and manifest
result receipt and transaction state
runtime selection evidence
target row and activation generation
```

Not every claim requires every coordinate.

## 10. Bounded phases and fail-closed transitions

Each transaction has one declared purpose. A review does not silently collect evidence; collection does not silently accept it; provider acceptance does not silently compose or populate a target.

Unknown, absent, not-run, and blocked states remain explicit. Plausible inference is not a substitute for a missing gate.

## 11. Source and state have owners

Keep these categories distinct:

```text
tracked source and desired state
generated immutable releases
mutable workspaces and provider stores
application payloads and user data
cache and disposable scratch
historical evidence
```

A working checkout is authoring state, not live runtime authority.

## 12. Candidate, promotion, activation, and rollback are separate

Prepare and validate candidates before promotion. Activation must be explicit and reversible. Repository deployment rollback, provider rollback, application-state rollback, and user-data recovery are separate authority domains.

## 13. Preserve valid upstream locality

Keep application-local or supplier-local structure when it is a valid part of the reference contract. Do not centralize every library or configuration merely for visual uniformity.

## 14. Mechanism before automation

Understand the loader, ABI, bridge, provider, package, device, and policy mechanism before turning it into lifecycle automation. Automation may make a wrong model repeatable; it does not make the model correct.

## 15. Failures are architecture data

Negative results, mismatches, regressions, and rollback failures constrain the system model. Preserve them with enough context to distinguish mechanism, observation, hypothesis, and conclusion.

## 16. Reproducible accepted transitions

An accepted repository transition should be recoverable from:

```text
exact Git state
structured test and transaction status
result archive digest
claim boundary
next semantic state
```

Narrative handoffs are not authority. Current state is updated in the same accepted repository transition.

## 17. Constitutional change rule

A project-purpose or invariant change requires an explicit accepted decision or a clearly identified correction. Experiment reports, active-task summaries, and historical records cannot silently redefine the constitution.

## Review checklist

Before promoting a new technical object, ask:

1. Which world, domain, capability, provider, bridge, or supply role owns it?
2. Is it reference-consumed, reference-adapted, independently reproduced, or novel/custom?
3. What semantics differ from the authoritative reference?
4. What risk modifiers change the minimum evidence?
5. What exact claim is being accepted, and which later states remain open?
6. What selects the candidate at runtime?
7. What is the rollback boundary?
8. Which source, generated, mutable, and historical states own the result?
