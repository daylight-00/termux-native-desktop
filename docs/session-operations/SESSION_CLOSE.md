# Session-close and successor handoff procedure

This file is the standing instruction for a future request such as "close the session and prepare the handoff." The user should not need to restate the full procedure.

## First decision

Determine the boundary state:

```text
A. latest user result verified;
B. execution package not run;
C. result exists but review is intentionally deferred;
D. no execution is pending.
```

When the user explicitly defers result review, do not inspect or interpret that result. Record its exact Drive locator as pending and make verification the successor's first project action.

## Separate durable process from project state

At close:

- update `session-operations/` only for new durable collaboration or execution lessons;
- create or refresh a dated file under `handoff/` for the current project state;
- keep the handoff concise and link to controlling numbered documents;
- do not duplicate the full collaboration contract in the dated handoff.

## Backup classes

### 1. Execution package

The normal agent-to-user package containing the next patch and wrapper. Store in `agent-outbox/`.

### 2. Mandatory handoff package

The successor session must receive this first. It contains:

```text
START_HERE.md;
verified baseline and exact pending-state summary;
Drive locators and checksums;
links or copies of the controlling project documents;
repository continuation patch or recovery material when needed;
current project principles and session-operations documents or their refactor patch;
raw pending result bytes when available, explicitly quarantined and semantically unverified;
verification script;
MANIFEST.sha256.
```

It must be sufficient to decide the first safe action without relying on the previous container.

### 3. Miscellaneous backup package

This protects useful but nonessential state:

```text
older execution packages and receipts;
full or recovery Git bundles;
authoring worktrees or patches;
select logs and inventories;
container-local material not required for immediate onboarding.
```

Label stale or partial repository recovery material explicitly. The successor must not mistake it for the current verified baseline.

## Two-package versus three-package close

Produce three packages when a fresh execution package is also being handed to the user:

```text
execution package
mandatory handoff package
miscellaneous backup package
```

Produce only two packages when the execution was not performed or when result review is intentionally deferred:

```text
mandatory handoff package
miscellaneous backup package
```

In the two-package case, the mandatory handoff package records the existing execution/result artifact rather than creating another user action.

## Mandatory handoff layout

```text
<name>/
  START_HERE.md
  project/
    PROJECT_PRINCIPLES.md
  state/
    PROJECT_STATE.md
    PENDING_ARTIFACTS.md
    VERIFIED_BASELINE.txt
    DRIVE_COORDINATES.txt
  pending-results/
    <exact pending result>.tar.zst when available
  repository/
    continuation.patch
    APPLY_AFTER_REVIEW.md
  operations/
    session-operations documents or patch
  tools/
    verify-handoff.sh
  MANIFEST.sha256
```

The first page should state only the verified baseline, pending artifact, first action and links to deeper material.

## Close validation

Before upload:

1. ensure all package members use relative safe paths;
2. reject symlinks and special files unless explicitly required;
3. generate `MANIFEST.sha256` after all contents are final;
4. create with zstd, not gzip;
5. verify SHA-256, `zstd -t`, tar member safety and manifest;
6. upload raw bytes to the handoff folder;
7. fetch every uploaded package and verify it again;
8. report exact filenames, Drive IDs, sizes and SHA-256 values.

## Successor responsibilities

The successor must:

1. verify the mandatory handoff package before trusting it;
2. inspect the explicitly pending result first;
3. compare the user's local branch, remote branch and recorded baseline;
4. update `handoff/CURRENT.md` after resolving the pending boundary;
5. continue the project only after the first result review is complete.
