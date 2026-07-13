# 0143 — Selected Obsidian Non-Priority Generic Artifact Member-Inventory Collector

## Status

A bounded download-only collector is implemented for the exact comparison set defined by 0142.

```text
canonical artifacts permitted:
    34

canonical identity-to-artifact edges:
    44

maximum compressed bytes:
    51,771,348

package installation:
    FORBIDDEN

maintainer-script execution:
    FORBIDDEN

filesystem payload extraction/materialization:
    FORBIDDEN

control/data archive stream inventory:
    IMPLEMENTED

authority decisions accepted by implementation:
    0

target rows populated:
    0
```

Verdict:

```text
collector implementation:
    READY / BOUNDED

exact device receipt:
    NOT YET REVIEWED BY THIS REPOSITORY TRANSACTION

object-to-artifact member binding:
    OPEN

artifact-to-recipe build binding:
    OPEN

Termux/Android adaptation acceptance:
    OPEN

final provider authority:
    OPEN

ApplicationRuntimeComposition:
    NOT REACHED

target population, materialization and activation:
    BLOCKED
```

`AUTH-009` remains `OPEN_OBJECT_SOURCE_BINDING`.

## Canonical inputs

The collector accepts only the exact products defined by 0142:

```text
review/generic-artifact-member-comparison-artifacts.tsv
review/generic-artifact-member-comparison-edges.tsv
review/generic-artifact-member-comparison-metadata.tsv
profiles/supply-repository-metadata-registry.tsv
```

Before acquisition it verifies:

```text
artifact-set SHA-256;
edge-set SHA-256;
34-artifact cardinality;
44-edge cardinality;
51,771,348-byte ceiling;
repository metadata identity and base URI;
exact repository-relative path, package, version, architecture, size and SHA-256;
zero accepted authority decisions and zero populated targets in the input contract.
```

Only HTTPS URLs on the approved Termux package hosts are accepted in production. Redirect destinations are checked against the same host/scheme policy.

## Acquisition and private cache

Artifacts are stored only under the experiment-private work tree:

```text
experiments/glibc/selected-obsidian-provider-authority/work/
    artifacts/generic-artifact-member-inventory/
```

Existing cache entries are reused only when they are regular non-symlink files whose exact size and SHA-256 match the canonical artifact row.

A missing artifact is downloaded to an exclusive partial file, bounded by the exact expected size, SHA-256 verified, fsynced and atomically renamed into the private cache.

The collector does not call `apt`, `pkg`, `dpkg -i`, repository-index update commands or any package transaction command.

## Archive inspection boundary

The collector uses read-only `dpkg-deb` operations:

```text
dpkg-deb -W
    exact Package / Version / Architecture control identity

dpkg-deb --ctrl-tarfile
    control archive member metadata stream

dpkg-deb --fsys-tarfile
    data archive member metadata stream
```

The tar streams are iterated without creating an extraction directory and without writing package members into the filesystem.

For exact named search members only, regular-file bytes may be read into bounded memory to inspect the ELF header and dynamic string table for an observed `DT_SONAME`. Symlink and hardlink members are recorded as metadata only.

This is archive-stream observation, not runtime materialization.

## Receipt products

A successful collector receipt contains:

```text
analysis.status
claim-boundary.txt
next-state.txt
summary.tsv
input-verification.tsv
download-plan.tsv
downloaded-artifacts.tsv
artifact-control-fields.tsv
artifact-control-member-inventory.tsv
artifact-data-member-inventory.tsv
named-member-observations.tsv
```

The named observation states are:

```text
UNIQUE_EXACT_BASENAME_MEMBER_OBSERVED
MULTIPLE_EXACT_BASENAME_MEMBERS_OBSERVED
NO_EXACT_BASENAME_MEMBER_OBSERVED
```

Observed paths, member types, exact named-member SHA-256 values and ELF SONAME values are evidence for later review. The collector itself labels every observation:

```text
object_member_binding_state:
    OBSERVED_CANDIDATE_NOT_AUTHORITY_ACCEPTED

artifact_to_recipe_binding_state:
    OPEN

termux_android_adaptation_state:
    OPEN

final_provider_state:
    UNRESOLVED

target_population_state:
    BLOCKED
```

## Mutation guards

The collector snapshots and verifies that the following remain unchanged during the transaction:

```text
repository HEAD and tree;
tracked repository status;
dpkg status file;
apt-list metadata/content manifest.
```

The only expected persistent mutation is creation or verified reuse of exact `.deb` files in the private artifact cache and creation of the evidence receipt.

It performs no runtime launch, build, source fetch, generation/current mutation, launcher/loader mutation or RPATH change.

## Validation

Repository smoke validation covers:

```text
canonical 34/44/51,771,348 comparison-set lock;
production host and path validation;
exact size/SHA/control verification;
stream-only control/data inventory;
exact basename found, symlink and missing-member observations;
in-memory ELF SONAME observation;
package/dpkg/apt state preservation;
private cache reuse with the network server stopped;
zero authority acceptance and zero target population;
absence of install/materializer commands.
```

The synthetic end-to-end test builds two `.deb` files, serves them from a loopback HTTP server under explicit test mode, verifies the first download run, stops the server and verifies a cache-only second run.

## Claim boundary

This stage establishes only that the repository has a bounded mechanism capable of:

```text
acquiring the exact 34-artifact set;
verifying each artifact identity;
listing control and data archive members without installation;
recording exact-basename, named-member SHA-256 and ELF SONAME observations;
proving package-manager and repository-state preservation;
producing a reviewable immutable receipt.
```

It does not establish:

```text
that a basename observation is final semantic object ownership;
that a SONAME observation proves ABI compatibility or necessity;
that artifact bytes were built from the pinned recipe tree;
that recipe patches provide the required Android adaptation;
that any candidate belongs in the final runtime composition;
that artifact member path, mode, uid, gid or link target is target policy;
that any target may be populated or materialized.
```

## Next valid task

```text
RUN_BOUNDED_GENERIC_ARTIFACT_MEMBER_INVENTORY_COLLECTOR
```

After a device receipt is returned, the next repository task is:

```text
REVIEW_GENERIC_ARTIFACT_MEMBER_INVENTORY_RECEIPT
```

Do not promote member observations into authority until the exact receipt has been independently reviewed against the canonical 34-artifact/44-edge contract.
