# Active task: review libSELinux direct-consumer necessity and security boundary

> Task ID: `review-libselinux-direct-consumer-necessity-and-security-boundary`
>
> Expected state on completion: the exact selected consumer edge to `libselinux.so.1`, required symbols, and SELinux policy/filesystem-context semantics are either bounded sufficiently for a separate future candidate-authorization decision or the dependency is removed/reselected. **This task grants no build authorization.**

## Objective

Determine why the selected runtime requires `libselinux.so.1`, which exact ELF directly declares it, which imported symbols are actually used, and whether the dependency can be eliminated without changing the selected application contract. Bound all security-sensitive behavior before any production lane is considered.

## Why now

The exact GTK 3.24.49 atomic `libgdk-3.so.0`/`libgtk-3.so.0` pair now has bounded provider authority. The selected composition has one unresolved identity, `libselinux.so.1`. Target-manifest generation, population, deployment, and activation remain blocked.

## In scope

- identify every exact selected direct consumer of `libselinux.so.1`;
- record exact `DT_NEEDED`, imported symbol, call-site, package/source and configuration evidence;
- distinguish essential runtime behavior from optional SELinux feature linkage;
- review libsepol, PCRE2, policy-store, file-context, labeling and Android policy-path assumptions;
- prefer dependency elimination or consumer reselection when compatible with the selected contract;
- define the minimum evidence required for a separate high-risk Class B recipe/Class C candidate authorization, if necessity is proven.

## Out of scope

Building or acquiring libSELinux, using Android or bionic SELinux libraries, creating cross-world aliases or shims, loading policy, relabeling files, changing enforcing state, touching Android policy stores, package installation, target population, deployment, service activation, or selected-generation activation.

## Required reading

- `docs/evidence/libselinux-provider-evidence-blocker.md`
- `docs/evidence/missing-glibc-provider-production-boundary.md`
- `docs/evidence/selected-obsidian-provider-composition-review.md`
- `docs/evidence/gtk3-core-bounded-provider-authority.md`
- `docs/decisions/0005-proportional-assurance-depth.md`

## Pending external inputs

None. This task uses the retained selected/runtime evidence and repository/source metadata only. Any later candidate production requires a separate authorization decision.

## Completion criteria

A machine-readable and narrative review records exact direct consumers, required symbols, source/configuration cause, removal/reselection feasibility, security semantics, prohibited operations, dependency closure, and a decision of either `DEPENDENCY_ELIMINATION_OR_RESELECTION` or `SEPARATE_HIGH_RISK_CANDIDATE_AUTHORIZATION_REVIEW_REQUIRED`. Neither outcome itself authorizes a build.

## Stop conditions

Stop if consumer identity or symbol use cannot be made exact, if validation would require policy mutation or Android platform state access, or if the review begins to infer glibc compatibility from bionic/Android libraries.

## Next valid action

Perform a read-only direct-consumer and imported-symbol census for `libselinux.so.1`. Do not build, install, alias, load policy, relabel, populate a target, deploy, or activate.
