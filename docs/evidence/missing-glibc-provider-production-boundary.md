# Missing Termux glibc provider production boundary

## Decision

```text
decision state:                  ACCEPTED_PLANNING_ONLY
reviewed blocker families:       4
reviewed blocked identities:     7
provider authority effect:       NONE
composition effect:              NONE; REVIEWED_BLOCKED_INCOMPLETE retained
target/materialization effect:   NONE
first separately authorized lane: libXdamage recipe-contribution candidate preparation
```

Read-only package and recipe discovery is complete. The absence of approved Termux glibc packages is not solved by copying ordinary Termux/bionic bytes, Debian oracle bytes, Android platform libraries, or by treating source compatibility as produced-artifact authority. This decision selects bounded production lanes and evidence gates only. It does not build, package, publish, install, populate, deploy, mutate policy, start services, or activate a selected generation.

## Claim layering under ADR 0005

Every production lane has two distinct claims:

```text
recipe and platform adaptation contract
    -> Class B reference-adapted when official source is retained and deviations are narrow and explicit

locally produced package and ELF bytes
    -> Class C independently reproduced until an authoritative upstream glibc repository publishes and signs the exact package
```

If an accepted upstream Termux glibc repository later publishes the exact package from the reviewed contribution, consumption may be reassessed as Class A or Class B. A local Class C candidate never becomes reference-consumed merely because its recipe was proposed upstream. The selected runtime composition remains Class D and blocked until every provider is separately accepted.

## Version and identity policy

The current selected composition is version-locked. A candidate closes an existing row only when it preserves the selected source/member contract:

```text
libXdamage:  1.1.6 / libXdamage.so.1.1.0 / libXdamage.so.1
AT-SPI2:    2.56.2 / three selected ATK bridge, ATK and AT-SPI members
GTK 3:      3.24.49 / libgdk-3.so.0.2417.32 and libgtk-3.so.0.2417.32
libSELinux: 3.8.1 / libselinux.so.1
```

A newer upstream or ordinary Termux package is a reselection input, not a drop-in closure. It requires regenerating the selected identity set and repeating dependency, collision and consumer review.

## Family decisions

### 1. libXdamage — first admissible production lane

Preferred lane: contribute a pinned `gpkg/libxdamage` recipe to the approved Termux glibc recipe project, using upstream `libXdamage 1.1.6` and the retained source SHA-256 `52733c1f5262fca35f64e7d5060c6fcd81a880ba8e1e65c9621cf0727afb5d11`. The ordinary Termux 1.1.6 recipe is reference evidence for source and dependency semantics only.

The recipe/adaptation claim is Class B. Any locally built `.deb` and `libXdamage.so.1.1.0` are Class C until published by the approved supplier. This is the first production lane because it is a single leaf member with a small accepted closure: exact `libX11.so.6`, exact `libXfixes.so.3`, libc/loader, and build-only X.Org protocol data.

Required acceptance gates:

- exact source digest, recipe tree and complete adaptation diff;
- recorded toolchain, environment, producing invocation and package manifest;
- exact package/member digest, AArch64 machine, SONAME and alias chain;
- direct `DT_NEEDED` closure to accepted providers only;
- no RPATH/RUNPATH or cross-world path;
- bounded symbol/load test and GTK 3.24.49 GDK X11 consumer-binding review;
- package update, removal and rollback contract.

Rejected as durable lanes: copying the bionic or Debian ELF; creating a cross-world alias; retaining a project-only package indefinitely without first attempting the upstream recipe contribution. A temporary local Class C candidate is allowed only as evidence for the contribution.

### 2. AT-SPI2/ATK — deferred atomic contribution lane

Preferred lane: one pinned `at-spi2-core 2.56.2` glibc recipe contribution that produces the three selected libraries as an atomic family. The recipe/adaptation claim is Class B; locally produced archives and members are Class C. Splitting the three members across unrelated source or update lifecycles is rejected.

This lane follows libXdamage and must complete before GTK 3 core production. Its evidence minimum includes exact source digest and tag/commit, complete package file manifest, all three exact members and aliases, direct dependency closure, GTK accessibility binding, D-Bus service/helper file inventory, disabled-by-default service lifecycle, collision review, coordinated update and rollback. Library authority does not imply bus ownership, registry-daemon acceptance, accessibility enablement, schema installation or service activation.

Rejected lanes: bionic metapackage reuse, installed-byte copying, service startup as functional proof, or accepting only one or two members of the coupled family.

### 3. GTK 3 core — deferred atomic contribution lane

Preferred lane: one pinned GTK `3.24.49` glibc recipe contribution from exact upstream commit `7a7e86ecab67e7cf65f066dae2e02ae74d653ced`, producing `libgdk-3.so.0.2417.32` and `libgtk-3.so.0.2417.32` atomically. The recipe/configuration claim is Class B; locally produced package bytes are Class C.

This lane starts only after the required Xdamage and AT-SPI2/ATK provider decisions are available. Backend, accessibility, input, printing, portal, theme, settings, module and service choices must be explicit. A changed backend set is an adaptation and cannot be inferred from ordinary Termux GTK. Acceptance requires exact source/recipe/toolchain/output records, both member and alias identities, GTK-to-GDK direct binding, complete dependency closure, controlled load/init and minimal surface tests, collision review and coordinated update/rollback.

Rejected lanes: separately versioning GDK and GTK; copying bionic or Debian members; accepting successful application launch as package or backend authority; silently disabling or enabling optional backends.

### 4. libSELinux — production deferred pending necessity proof

Preferred disposition: do not produce a glibc libSELinux candidate until the exact selected consumer edge and required symbol/semantic surface are identified. If the dependency is removable by reselection or rebuilding the consumer without SELinux support, that narrower path is preferred.

Only after direct necessity is proven may a separate decision authorize a pinned `libselinux 3.8.1` recipe contribution based on authoritative SELinux userspace source and the exact selected Debian source lineage. The recipe/adaptation claim would be Class B; every locally produced member would remain Class C. The gate must include libsepol/PCRE2 closure, policy-store and filesystem-context assumptions, behavior when Android policy paths are absent, exact consumer calls, and proof that tests do not load policy, relabel filesystems, change enforcing state or mutate Android platform state.

Rejected lanes: Android `libandroid-selinux` substitution, `/system` library reuse, a cross-world alias, a custom compatibility shim, or broad SELinux functionality claims without consumer-bounded evidence. This family has no build authorization from this decision.

## Production order

```text
1. prepare exact libXdamage Class B recipe contribution and isolated Class C candidate evidence
2. prepare the atomic AT-SPI2/ATK recipe contribution and candidate family
3. prepare the atomic GTK 3 GDK/GTK recipe contribution and candidate pair
4. revisit libSELinux only after direct-consumer necessity and symbol semantics are proven
```

The order is an evidence and dependency order, not authority inheritance. Completion of one lane does not accept the next lane or the composition.

## Stop and reopening rules

Stop a lane when exact source lineage, adaptation necessity, dependency closure, license/distribution boundary, atomicity, functional validation or rollback cannot be bounded. Do not widen the collector or combine families merely to continue execution.

The first lane has now produced and separated an exact Class B recipe candidate and exact isolated Class C artifact candidate. The next task is `review-libxdamage-production-candidate-bounded-provider-authority`. It may decide bounded provider authority from the retained evidence. It may not publish a package repository, install the candidate, populate a target, deploy, or activate it.
