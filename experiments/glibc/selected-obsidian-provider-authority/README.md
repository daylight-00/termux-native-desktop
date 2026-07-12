# Selected Obsidian Provider-Authority Census

## Status

```text
N0_REPOSITORY_ONBOARDING_PASS
N1_CENSUS_SCHEMA_AND_EVIDENCE_PLAN_PASS
N2_READ_ONLY_PROVIDER_EVIDENCE_PENDING
N3_PROVISIONAL_AUTHORITY_CLASSIFICATION_PENDING
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
```

It is read-only until a later explicit record authorizes a bounded discriminator.

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

## Repository schema

```text
schema/
    census-columns.tsv
    capability-groups.tsv
```

`census-columns.tsv` defines the canonical capability/object row fields and controlled values.

`capability-groups.tsv` defines the initial capability-first grouping. Its classifications are pressure-only seeds, not final provider decisions.

## Required evidence priority

Use accepted evidence before designing new collection:

```text
B7 complete CPU manifest
    -> base selected/reference/data/cache/state row set

B1 locality and identities
    -> exact path/package/hash and $ORIGIN evidence

B2 static/runtime partition
    -> dependency edges, static closures, dynamic roots, data separation

B9 generation publication
    -> content-object and alias identities

passive B10 + map-selection diagnostic
    -> actual mapped identities and negative leakage boundaries

pixbuf inventory
    -> bounded cache/module/icon/MIME facts only
```

The current glibc-prefix package/object surface requires a new read-only inventory because the existing substrate-authority record establishes the APT/dpkg backend but does not semantically partition every relevant package and object.

## Planned N2 outputs

```text
selected-reference-object-seed.tsv
glibc-prefix-package-surface.tsv
provider-authority-census.tsv
unresolved-evidence-ledger.tsv
summary.tsv
claim-boundary.txt
next-state.txt
analysis.status
```

No output receipt exists yet.

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

## Read-only device inventory boundary

Permitted N2 collection may inspect:

```text
dpkg package identities and file ownership;
APT/dpkg metadata already installed;
regular-file hashes;
symlink text and resolved paths;
ELF headers, NEEDED, SONAME, RPATH/RUNPATH, Build ID;
selected/reference consumers and dependency edges;
existing receipt files and generation manifests.
```

It must not:

```text
install, remove, upgrade, or downgrade packages;
run package maintainer scripts;
mutate loader caches;
mutate the selected generation;
create or change current;
change promoted launchers;
copy candidate provider bytes;
clean prefix or rootfs paths;
reopen graphics gates.
```

## Row discipline

Capability rows answer responsibility and reference-authority questions.

Object rows answer identity, locality, provenance, ABI, dependency, and concrete source-candidate questions.

Rules:

```text
path identity != content identity;
package ownership != semantic authority;
loader selection != final authority;
capability membership may overlap;
one row retains one provisional primary class and update owner;
UNRESOLVED is preferred over path-first inference;
app-local $ORIGIN topology is first-class evidence;
data, generated data, mutable state, and cache remain separate.
```

## Bounded pixbuf relationship

The interactive Vault-open pixbuf discriminator is allowed only as a separate named diagnostic under the fixed boundaries in `0117` and `0118`.

Its result may add evidence to the census. It may not choose Debian, Termux-glibc, native, app-local, upstream, or project-built authority by itself.

## Stop line

Do not derive a successor manifest or generation from these schema files.

The next valid state is:

```text
READY_FOR_N2_READ_ONLY_PROVIDER_EVIDENCE
```
