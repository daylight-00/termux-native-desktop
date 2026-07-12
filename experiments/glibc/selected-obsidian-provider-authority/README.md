# Selected Obsidian Provider-Authority Census

## Status

```text
N0_REPOSITORY_ONBOARDING_PASS
N1_CENSUS_SCHEMA_AND_EVIDENCE_PLAN_PASS
N2_READ_ONLY_PROVIDER_EVIDENCE_PASS
N3_NORMALIZED_PROVISIONAL_AUTHORITY_CLASSIFICATION_READY
PROVIDER_AUTHORITY_INTERVENTION_ACTIVE
SUCCESSOR_MANIFEST_BLOCKED
SUCCESSOR_MATERIALIZATION_BLOCKED
CURRENT_ACTIVATION_BLOCKED
```

This workstream implements the provider-authority census required by:

```text
docs/refactor/0116-end-to-end-architecture-audit-and-provider-authority-intervention.md
docs/refactor/0117-provider-authority-intervention-adoption-and-execution-order.md
docs/refactor/0118-selected-obsidian-provider-authority-census-schema-and-evidence-plan.md
docs/refactor/0119-selected-obsidian-provider-authority-n2-read-only-evidence-collector.md
docs/refactor/0120-selected-obsidian-provider-authority-n2-device-receipt-review.md
```

## Accepted N2 receipt

```text
archive:
    selected-obsidian-provider-authority-n2-read-only-evidence-results-20260712-155013.tgz

SHA-256:
    e1eec5b68286cd6f888241afb50d9eabe00a8765269ecf20eb57bc0d7fe270d0

captured HEAD:
    b8a7ba253053c9355ce53fb3db92ae905f4855b9

analysis.status:
    PASS

next-state:
    READY_FOR_N3_PROVISIONAL_AUTHORITY_CLASSIFICATION
```

Independent review accepted:

```text
28 embedded input identities
96 immutable generation identities
161 selected/reference rows
20 pixbuf/icon/MIME supplemental rows
27,279 current glibc-prefix paths
86 package identities
958 prefix ELF objects
2 unowned loader-state paths
zero current or dpkg-state change
```

N2 is closed. No provider authority was accepted by N2.

## Purpose

The first selected Obsidian generation proved that an immutable selected composition can run passively outside PRoot.

It did not prove that every selected/reference object comes from the correct final authority.

This workstream separates:

```text
current path and provenance
historical selected-generation disposition
semantic capability responsibility
candidate source authorities
runtime/research profile
update and revalidation ownership
provisional final authority
missing discriminating evidence
```

## Repository layout

```text
schema/
    census-columns.tsv
    capability-groups.tsv

recipe/
    collect-read-only-provider-evidence.py
    run-n2-read-only-provider-evidence.sh
```

`census-columns.tsv` defines the canonical capability/object fields.

`capability-groups.tsv` defines pressure-only capability seeds. It does not choose providers.

## N2 outputs

```text
selected-reference-object-seed.tsv
supplemental-capability-evidence.tsv
glibc-prefix-package-surface.tsv
package-control-surface.tsv
glibc-prefix-package-summary.tsv
provider-authority-census.tsv
unresolved-evidence-ledger.tsv
summary.tsv
claim-boundary.txt
next-state.txt
analysis.status
```

The raw provider-authority census contains 26,419 OPEN/UNRESOLVED rows. Of those, 26,213 are `unassigned.prefix-surface` members.

## N3 normalization boundary

N3 must not classify every raw prefix path independently.

Required normalized decision surface:

```text
selected/reference rows:
    161

pixbuf/icon/MIME rows:
    20

prefix ELF rows:
    958

unowned loader-state rows:
    2

package aggregate rows:
    86

remaining non-runtime package files:
    aggregated by package and semantic path class
```

The 27,279-path raw table remains immutable evidence for drill-down.

## Semantic classes

```text
WORLD_CORE_SUBSTRATE
PLATFORM_INTEGRATION_PROVIDER
GENERIC_SHARED_CAPABILITY_PROVIDER
APPLICATION_LOCAL
APPLICATION_DOMAIN_SUPPLEMENT
DATA_CAPABILITY_PROVIDER
TOOLCHAIN_ONLY
ORACLE_ONLY
MUTABLE_OR_CACHE
UNRESOLVED
```

Historical classes such as `WORLD_SUBSTRATE_ELF`, `PROVIDER_PREFIX_ELF`, and `PROVIDER_ROOTFS_ELF` remain evidence fields. They do not directly populate the new semantic class.

## Read-only boundary

Permitted work may inspect:

```text
dpkg package identities and file ownership
existing package metadata
regular-file hashes
symlink text and resolved paths
ELF headers, NEEDED, SONAME, RPATH/RUNPATH, Build ID
selected/reference consumers and dependency edges
existing receipt files and generation manifests
```

It must not:

```text
install, remove, upgrade, or downgrade packages
run package maintainer scripts
mutate loader caches
mutate the selected generation
create or change current
change promoted launchers
copy candidate provider bytes
clean prefix or rootfs paths
reopen graphics gates
```

## Archive policy

Unpacked receipt roots remain under:

```text
$PREFIX/tmp/selected-obsidian-provider-authority
```

TGZ archives default to:

```text
$HOME/Downloads
```

The N2 wrapper accepts `DOWNLOADS_DIR` only when an alternate operator-controlled Downloads directory is required.

## Row discipline

```text
path identity != content identity
package ownership != semantic authority
loader selection != final authority
capability membership may overlap
UNRESOLVED is preferred over path-first inference
app-local $ORIGIN topology is first-class evidence
data, generated data, mutable state, and caches remain separate
```

## Bounded pixbuf relationship

The interactive Vault-open pixbuf discriminator remains allowed only as a separate named diagnostic under the fixed boundaries in `0117`, `0118`, and `0120`.

Its result may add evidence. It may not choose final source authority by itself.

## Next valid state

```text
BUILD_NORMALIZED_N3_DECISION_SURFACE
```

Do not derive a successor manifest or generation from the raw census.
