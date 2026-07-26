# Selected Obsidian provider composition boundary acceptance

## Decision

```text
review id:                     SELECTED-COMPOSITION-ACCEPT-001
decision:                      ACCEPTED_BOUNDED_COMPLETE_SELECTED_PROVIDER_COMPOSITION
accepted provider roots:       31
accepted decision rows:        42
included current-scope rows:   41
deferred rows:                  1
active selected gaps:           0
SONAME collisions:              0
alias collisions:               0
target manifest generated:     NO
target population authorized:  NO
activation authorized:         NO
```

The exact zero-gap provider composition boundary is accepted as a Class D project-owned decision. The accepted boundary is the exact v103 review set: 42 provider decision rows, of which 41 are included for the current selected GTK/transitive runtime scope and exact `libtasn1.so.6.6.4` remains profile-deferred. The acceptance freezes the reviewed member, exclusion, alias, collision, capability, update and rollback decisions; it does not create target paths or copy files.

## Frozen review inputs

```text
selected-provider-composition-members.tsv SHA-256:
ce60f71248db0568f52a1230b086f6af272555fff6187a3ca1a76c83014e2e70

selected-provider-composition-gaps.tsv SHA-256:
14568107bbe4f28f101a31488b93db1920365c1893edc6d47d4d6530aff86673

selected-provider-composition-metadata.tsv pre-acceptance SHA-256:
14e340dbd8f5d1ec4f72e0ccf287810d02a60486cb50e78fcb13987035251dde
```

The gap table contains only its header. The member table contains 42 unique SONAMEs and 42 unique SONAME-alias basenames. The accepted inclusion/exclusion split is 41/1.

## Ordering and alias boundary

The deterministic composition-row order is accepted only as review ordering. It is not filesystem copy order, dynamic-loader search order, package installation order, or activation order. Exact SONAME alias identities are accepted as composition decisions, but no target pathname or symlink is created by this transaction.

The Pango three-member family, Cairo two-member family, AT-SPI2/ATK three-member family, and GDK/GTK two-member family remain atomic. Partial family updates or rollback are prohibited.

## Deferred member

`libtasn1.so.6.6.4 -> libtasn1.so.6` remains an accepted bounded provider outside the current selected GTK runtime membership. It may enter a later target only after a GnuTLS security or printing profile decision. This acceptance does not silently include it.

## Exclusions

The following remain excluded: package-wide development surfaces, unversioned development aliases, tools, modules, schemas, print backends, services, data, GIR/typelib target membership, deferred libtasn1 current-profile membership, display execution, target paths, population, materialization, deployment and activation.

## Update and rollback

Any member SHA, version, SONAME, alias, inclusion state, capability boundary, atomic-family relation, provider decision or dependency change requires a new Class D composition review. Before target-manifest generation the decision may be revoked directly. After any future materialization, rollback must select a prior immutable whole-composition generation while preserving atomic families.

## Next action

```text
generate-and-review-non-mutating-selected-target-manifest
```

That next transaction may calculate target rows and collisions only. It may not copy, install, populate, deploy or activate anything.
