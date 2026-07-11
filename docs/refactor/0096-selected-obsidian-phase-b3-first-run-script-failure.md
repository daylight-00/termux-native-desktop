# 0096 — Selected Obsidian Phase B3 First-Run Script Failure

## Status

The first Phase B3 archive is invalid as a capability-grouping receipt.

It is preserved as a source-script failure, not an evidence or architecture failure.

```text
phase:
    selected Obsidian Phase B3 capability grouping

result:
    INCOMPLETE
    INVALID_FOR_CAPABILITY_OWNERSHIP_DECISION

runtime launch:
    NO

promoted runtime mutation:
    NO
```

## Failed archive

```text
selected-obsidian-phase-b3-capability-grouping-20260711-203153.tgz
```

SHA-256:

```text
33382473aa1a42b48840e6033cbc71f55bdc59d7c6d8b956720c98a93b40d8fb
```

Captured repository state:

```text
branch:
    docs/post-graphics-architecture-audit

head:
    f01545da948354e3b8d0590fc0566ffb46811264
```

## Archive inspection

The archive contained 18 members under one relative Termux path.

It contained no:

```text
absolute archive path
parent traversal
symlink
device node
special member
```

All eight Phase B2 inputs were present and copied into the B3 output:

```text
analysis.status
summary.tsv
resolved-edges.tsv
candidate-elf-partition.tsv
mapped-only-dynamic.tsv
data-capabilities.tsv
input/elf-objects.tsv
input/process-semantic-usage.tsv
```

`input-verification.tsv` marked every input `PASS`.

## Failure signature

The output stopped after creating headers for:

```text
dynamic-root-candidates.tsv
dynamic-root-closure.tsv
dynamic-root-members.tsv
```

All three files contained only their header row.

The archive did not contain:

```text
analysis.status
next-state.txt
summary.tsv
failure-stage.txt
shared-dynamic-support.tsv
entrypoint-direct-providers.tsv
partition-package-summary.tsv
data-capability-summary.tsv
suggested-dynamic-family-summary.tsv
claim-boundary.txt
```

Therefore the script aborted during the first dynamic-root derivation before a receipt was finalized.

## Root cause

The original function used one `local` command for both argument assignment and associative-array lookups:

```bash
suggest_family() {
    local path=$1 semantic=${SEMANTIC_BY_PATH[$path]} package=${PACKAGE_BY_PATH[$path]}
    ...
}
```

In Bash, expansions in a `local` command occur before those assignments become visible to the same command.

After the preceding `while read ... path` loop reached EOF, the outer `path` variable was empty. Under:

```bash
set -u
```

this caused an empty associative-array subscript / unbound lookup while evaluating:

```bash
${SEMANTIC_BY_PATH[$path]}
```

The root argument had not yet become the local `path` value for that expansion.

The failure is deterministic source behavior and is unrelated to the Phase B2 graph contents.

## Correction

Corrected form:

```bash
suggest_family() {
    local object_path semantic package
    object_path=$1
    semantic=${SEMANTIC_BY_PATH[$object_path]:-}
    package=${PACKAGE_BY_PATH[$object_path]:-}
    ...
}
```

The correction separates declaration, argument assignment, and associative-array lookup.

Corrected commit:

```text
590c66d5ebb07aee6af2037d8482ac709c17cfd5
```

## Failure receipt hardening

The corrected recipe also adds stage-aware error handling.

Unexpected failures now write:

```text
analysis.status=FAIL
failure-stage.txt=<current analysis stage>
```

Known input/status/root-count failures also write an explicit failure stage.

On success:

```text
analysis.status=PASS
failure-stage.txt absent
```

This prevents another partial directory from appearing receipt-like without an explicit final state.

## Source-level replay

The corrected script was replayed locally against the exact B2 files embedded in the failed B3 archive.

The replay completed with:

```text
mapped_only_objects:
    15

dynamic_discovery_roots:
    5

unclassified_dynamic_roots:
    0

shared_dynamic_support_objects:
    1

entrypoint_direct_providers:
    34

data_capability_objects:
    17

runtime_launch_performed:
    NO

promoted_runtime_mutated:
    NO
```

This is a source-level regression check, not an authoritative Termux receipt. A fresh Phase B3 read-only run is still required.

## Evidence consequence

The failed archive proves only:

```text
Phase B2 inputs were available;
the original B3 script reached dynamic-root derivation;
the original B3 implementation then aborted.
```

It does not prove:

```text
dynamic root count;
family classification;
shared support count;
entrypoint direct provider count;
capability ownership readiness.
```

Phase B1 and Phase B2 remain valid and do not need to be rerun.

## Next action

```text
sync corrected commit;
run only Phase B3 again;
use a fresh stage-specific OUT directory;
archive the fresh output;
do not reuse or overwrite the failed evidence root.
```

## Stop line

Do not:

```text
promote the first B3 archive;
interpret empty dynamic-root tables as zero roots;
rerun Phase B1 or Phase B2;
rerun Obsidian or any graphics workload;
merge failed and corrected B3 files into one receipt;
reuse the failed OUT directory.
```
