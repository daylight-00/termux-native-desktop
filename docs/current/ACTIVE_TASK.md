# Active task: define the missing glibc provider production boundary

> Task ID: `define-missing-glibc-provider-production-boundary`
>
> Expected state on completion: the four reviewed blocker families have one explicit, non-mutating production/remediation decision record that selects admissible supplier, package-contribution, or project-produced candidate lanes and the assurance class and evidence gates for each. No build, installation, target population, policy mutation, deployment, or activation occurs.

## Objective

Define the smallest coherent production boundary for the seven selected runtime identities that remain blocked because the approved Termux glibc package index and pinned recipe repository contain no candidate.

## Why now

Read-only discovery is complete. libXdamage, the coupled AT-SPI2/ATK family, the GTK 3 GDK/GTK core pair, and libSELinux all stopped at the same durable boundary: no approved glibc package coordinate and no pinned producing recipe root. Repeating package-name probes cannot close the composition.

## Blocker families

```text
Xdamage:       libXdamage.so.1
AT-SPI2/ATK:  libatk-bridge-2.0.so.0; libatk-1.0.so.0; libatspi.so.0
GTK 3 core:   libgdk-3.so.0; libgtk-3.so.0
SELinux:      libselinux.so.1
```

## In scope

- compare supplier addition, upstream contribution, pinned Termux glibc recipe contribution, and separately authorized project-produced candidate lanes;
- classify each proposed production claim under ADR 0005 as reference-adapted or independently reproduced;
- define exact source, version, recipe-tree, patch/configuration, toolchain, package, member, SONAME, alias, dependency, consumer, collision, update, rollback and functional gates;
- preserve atomic grouping for AT-SPI2/ATK and GTK/GDK;
- define ordering and prerequisite closure without executing a build;
- explicitly retain Android/bionic wrong-world exclusions and SELinux policy/labeling boundaries.

## Out of scope

Source checkout, compilation, package creation, repository publication, package-manager mutation, installation, target generation, materialization, policy loading, relabeling, service activation, deployment, or selected-generation activation.

## Required reading

- `docs/current/STATE.yaml`
- `docs/decisions/0005-proportional-assurance-depth.md`
- `docs/evidence/libxdamage-provider-evidence-blocker.md`
- `docs/evidence/at-spi2-core-provider-evidence-blocker.md`
- `docs/evidence/gtk3-core-provider-evidence-blocker.md`
- `docs/evidence/libselinux-provider-evidence-blocker.md`
- `docs/evidence/selected-obsidian-provider-composition-review.md`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-composition-gaps.tsv`

## Pending external inputs

None for the planning tranche. Exact upstream and distribution coordinates may be inspected read-only. Any artifact production or repository mutation requires a separate authorized transaction after the decision record is accepted.

## Stop conditions

Stop without a production recommendation for any family whose source lineage, adaptation necessity, dependency closure, runtime consequence, licensing/distribution boundary, or validation method cannot be bounded. Do not combine the four families into one build merely because they share the same missing-package disposition.

## Next valid action

Author a decision matrix for the four blocker families that selects a preferred production lane, implementation class, exact evidence minimum, atomicity, dependencies, exclusions, stop condition and reopening gate. Do not execute the selected lane in this task.

## Completion criteria

- Every blocker family has one preferred and at least one rejected or deferred production lane with rationale.
- Class B versus Class C ownership is explicit for each produced claim.
- Package/member/SONAME/alias/dependency/consumer/update/rollback and functional acceptance gates are explicit.
- No build, target, policy mutation, deployment, or activation occurs.
