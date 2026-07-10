# 0020 — glibc 2.42 → 2.43 Binary ABI Regression

## Status

This document records the decisive non-installing A/B comparison between the repository-addressable `glibc=2.42` artifact and the active device `glibc=2.43` substrate.

The comparison was performed without modifying installed package state.

## 1. Exact artifact acquisition

The device downloaded the exact previous version from the configured Termux glibc APT repository:

```text
package: glibc
version: 2.42
architecture: aarch64
artifact:
    glibc_2.42_aarch64.deb
sha256:
    59e47a50b77ba9c0c1cc7cd0dafbb1558528cb544a740858faad0263e8b9b27f
```

Package metadata:

```text
Package: glibc
Version: 2.42
Architecture: aarch64
Depends: linux-api-headers-glibc
```

The artifact was extracted into a temporary directory with `dpkg-deb -x`. It was not installed.

## 2. Binary identities

### glibc 2.42 artifact libc

```text
Build ID:
    0b0a4cdb97355daecdb91d2915f61215924104c8

SHA-256:
    665384fb6018e1a41ce21e542c6e7b4ee67850ec7292ce90329623b25a673834
```

### active glibc 2.43 libc

```text
Build ID:
    44a096e6462274ee2203500197c7aa1adf5ef9a5

SHA-256:
    e9e6d07732a00aa3c56ca8ca0a3ec9cf4a6c310ea3cad5ba5638f2cb21ac9d56
```

The binaries are concretely distinct and their identities are recorded.

## 3. Fortified syslog ABI comparison

### glibc 2.42 binary

Observed dynamic exports:

```text
syslog@@GLIBC_2.17
__vsyslog_chk@@GLIBC_2.17
__syslog_chk@@GLIBC_2.17
vsyslog@@GLIBC_2.17
```

Exact target result:

```text
__vsyslog_chk@GLIBC_2.17: PRESENT
```

### glibc 2.43 binary

Observed dynamic exports:

```text
syslog@@GLIBC_2.17
__syslog_chk@@GLIBC_2.17
vsyslog@@GLIBC_2.17
```

Missing exact target:

```text
__vsyslog_chk@GLIBC_2.17: ABSENT
```

## 4. Incident classification

The evidence now supports the stronger binary-level conclusion:

> The repository artifact currently addressable as glibc 2.42 exports `__vsyslog_chk@@GLIBC_2.17`, while the installed glibc 2.43 binary does not. The active device incident is therefore a concrete 2.42 → 2.43 binary ABI regression for this required symbol.

This statement is intentionally about binary artifacts, not inferred source intent.

## 5. Relationship to earlier source analysis

Earlier source inspection found that the custom Termux syslog implementation shape already existed in the glibc 2.42 source snapshot, while the installed 2.43 binary lacked the export.

The A/B binary comparison resolves the practical ambiguity:

```text
source-level implementation pattern:
    suspicious in both snapshots examined

actual binary ABI:
    2.42 artifact exports required symbol
    2.43 active binary does not
```

These facts are not contradictory.

Possible explanations for why binary behavior differs despite similar source shape include build-system, symbol-versioning, alias-generation, long-double compatibility, or other integration differences. The incident recovery does not require identifying that build-level mechanism before choosing a validated recovery path.

## 6. Recovery consequence

A rollback candidate now exists with direct ABI evidence:

```text
glibc 2.42 artifact
    exact version
    exact SHA-256 recorded
    exact libc Build ID recorded
    required export present
```

However, this does not yet prove that installing `glibc=2.42` is transactionally safe on the current package set.

The next step is an APT simulation, not an immediate downgrade.

Required check:

```text
apt-get --simulate install glibc=2.42
```

Capture:

```text
all Inst/Conf/Remv operations
dependency conflicts
whether linux-api-headers-glibc must change
whether any other glibc-family packages are changed/removed
whether APT reports broken dependencies
```

## 7. Recovery decision gate

### Candidate rollback is acceptable only if

```text
APT simulation is bounded and understood
no unrelated destructive removals are required
current dependent package set remains satisfiable
post-install validation plan is ready
exact 2.42 artifact identity is preserved in evidence
```

### Required post-change gates

If rollback is selected after simulation review:

```text
1. dpkg reports glibc 2.42 installed
2. active libc Build ID matches expected 2.42 identity
3. core ABI regression gate PASS
4. farm libdbus relocation gate PASS
5. VS Code CLI workload probe PASS
6. real GUI workload validation PASS when appropriate
7. recovery transaction and identities recorded
```

## 8. Architecture implications

This incident strengthens several current architecture rules.

### Package version is not sufficient identity

The project must preserve binary identity where substrate correctness matters:

```text
package version
+
content hash
+
ELF Build ID
+
critical ABI gates
```

### Provider rebuild cannot repair substrate ABI regression

The libdbus failure was reproduced independently of VS Code and cannot be repaired by rebuilding the same broad farm against a substrate missing the required symbol.

### Substrate recovery remains separate from provider architecture work

Do not use this rollback experiment to introduce:

```text
gl-sync
global compatibility fingerprinting
farm lifecycle redesign
application launcher redesign
selected-closure pilot implementation
```

First restore and validate substrate/provider compatibility. Then continue the semantic hard-refactor sequence.

## 9. Current incident state

The device remains:

```text
BLOCKED_SUBSTRATE
```

but the recovery decision space is now narrowed to:

```text
Option A:
    validated bounded rollback to exact glibc 2.42

Option B:
    corrected current/newer glibc package preserving latest-first preference
```

The immediate next action is transaction simulation and review, not active mutation.
