# 0014 — Robust gl Update and Farm Lifecycle

## Goal

Keep the workstation close to latest package versions without making every glibc or Debian provider update an untracked compatibility gamble.

The design principle is:

```text
core runtime update
    -> detect identity change
    -> validate core ABI
    -> detect provider-set change
    -> generate candidate farm
    -> validate candidate closure
    -> activate atomically
    -> run post-activation workload probes
```

A farm rebuild is cheap enough to perform whenever the compatibility state changes, but rebuilding alone is not sufficient. A broken core ABI cannot be repaired by relinking the same provider libraries, as demonstrated by the missing `__vsyslog_chk@GLIBC_2.17` incident.

## Current weakness

The current `gl-farm` implementation:

```text
rm -rf $HOME/gl/lib
mkdir $HOME/gl/lib
link current Debian rootfs .so files directly into it
run denylist contamination check
run glibc ldconfig
```

This is destructive and in-place. If generation or validation fails midway, the active farm has already been replaced.

The active compatibility state also has no explicit receipt tying it to:

- the installed glibc package/binary identity;
- the Debian provider package set;
- the farm generator/denylist version.

## Proposed state model

Treat the farm as a materialized compatibility view, not mutable primary state.

```text
$HOME/gl/
├── lib -> farms/current/lib
├── farms/
│   ├── generations/
│   │   ├── <fingerprint-A>/
│   │   │   ├── lib/
│   │   │   ├── receipt.env
│   │   │   ├── provider-packages.tsv
│   │   │   └── validation/
│   │   └── <fingerprint-B>/
│   ├── current -> generations/<fingerprint-B>
│   └── previous -> generations/<fingerprint-A>
└── state/
    ├── observed.fingerprint
    ├── active.fingerprint
    └── dirty
```

Exact path names are implementation details; the important contract is immutable generations plus an atomic active selector.

## Fingerprint inputs

The compatibility fingerprint should include three domains.

### 1. Core identity

At minimum:

```text
glibc package version
libc.so.6 Build ID
hash of exported dynamic symbol/version table
```

The package version alone is insufficient because rebuilt packages can preserve the same version while changing binary ABI.

### 2. Debian provider identity

A conservative first implementation may hash the complete sorted output of:

```text
dpkg-query -W package/version set
```

This can rebuild the farm after an unrelated Debian package update, but the farm operation is cheap and the conservative false-positive is preferable to a missed provider ABI transition.

A later optimization may fingerprint only packages owning `.so` files reachable by the farm.

### 3. Generator identity

Include:

```text
gl-farm generator source hash
denylist hash
validation policy version
```

Changing filtering or validation semantics must invalidate the previous generation.

## Update detection

Use two mechanisms together.

### A. ALPM hook for core updates

A pacman/libalpm PostTransaction hook may trigger on package `glibc` and mark the gl state dirty. The hook should be small and deterministic.

It should not rebuild the complete farm inside the package transaction path.

Recommended action:

```text
glibc transaction completes
    -> mark core state dirty
    -> run quick core ABI gate
    -> print actionable failure if ABI contract is broken
```

The hook executable should live at a stable prefix path, not depend on interactive-shell PATH or shell functions.

### B. Lazy fingerprint check for Debian provider drift

Debian updates do not pass through pacman, so a pacman hook cannot detect them.

Before a gl workload starts, `gl-run` should perform a cheap state check:

```text
current fingerprint == active fingerprint
    yes -> run workload immediately
    no  -> invoke gl-sync --if-dirty or refuse with a clear remediation command
```

Because the expensive validation runs only after fingerprint changes, normal launches remain fast.

## Recommended default policy

For this workstation, prefer:

```text
GL_AUTO_SYNC=1
```

semantics:

```text
clean state
    -> launch immediately

dirty provider/core identity
    -> run transactional gl-sync
    -> launch only if sync succeeds

broken core ABI
    -> fail before touching current farm
```

This matches a latest-first maintenance preference while preserving a validated previous generation.

An opt-out mode should exist for debugging:

```text
GL_AUTO_SYNC=0
```

which reports dirty state and requires an explicit `gl-sync`.

## Transactional gl-sync

Recommended phases:

```text
0. acquire lock
1. capture current core/provider/generator identities
2. compute fingerprint
3. if already active and clean: exit 0
4. run core ABI gates
5. generate candidate farm under a new immutable generation directory
6. run contamination checks
7. run candidate relocation/workload closure tests
8. record receipt and validation evidence
9. atomically switch current generation
10. refresh ld cache
11. run post-switch gates
12. on failure: restore previous selector and ld cache
13. mark active fingerprint and clear dirty state
14. retain at least one previous validated generation
```

Critical invariant:

> Do not delete or mutate the active farm before the candidate has passed pre-activation validation.

## Validation policy

Use layered gates rather than one monolithic test.

### Tier 0 — core ABI

Examples:

```text
modules/gl/tests/core-abi.sh
```

This catches failures that no farm rebuild can repair.

### Tier 1 — compatibility provider relocation

Examples:

```text
modules/gl/tests/farm-libdbus-relocation.sh
```

Extend this list with a small manifest of critical provider libraries such as D-Bus, systemd, GTK-related roots, and other libraries known to sit on common Electron/desktop paths.

### Tier 2 — registered workload closure

Maintain a bounded manifest of workload entry points:

```text
VS Code executable
Obsidian executable
glxinfo or selected GL/Vulkan utility
other promoted glibc apps
```

Run loader/relocation probes against these entry points after a compatibility-state change.

### Tier 3 — real workload probes

After structural gates pass:

```text
code --version
obsidian-app --version or controlled startup probe
gl-run glxinfo -B
```

GUI launch/session restart remains a higher-cost validation step.

## Why unconditional farm rebuild alone is insufficient

The current incident proves:

```text
core libc missing required symbol
    +
rebuilding farm from the same Debian libdbus
    =
exact same failure
```

Therefore:

```text
rebuild-on-update
```

is useful but incomplete.

The correct policy is:

```text
validate core
    -> rebuild candidate farm
    -> validate closure
    -> activate
```

## Package rollback readiness

A latest-first policy still benefits from keeping at least one previous package artifact or equivalent rollback source.

Before implementing automatic recovery, first inspect the real pacman `CacheDir` configuration rather than assuming the default path.

If no persistent cache exists, configure one or create a package-receipt policy that preserves at least the previous validated glibc package artifact. Automatic rollback should only use a package artifact that has already passed the workstation ABI gates.

## Recommended commands and ownership

Future gl module interface:

```text
gl-status
    print core/provider/generator identities
    print clean/dirty/broken state

gl-sync
    build and validate a new generation transactionally

gl-run
    cheap fingerprint check
    optional auto-sync if dirty
    then execute workload

gl-farm
    low-level candidate generator only
    no longer mutates the active farm directly
```

Ownership:

```text
modules/gl/
    state model
    fingerprints
    generator
    validator
    activation/rollback
    pacman hook integration

packages/*
    workload-specific probes and expected entry points
```

## Implementation order

1. preserve the current broken state and repair the upstream glibc export issue;
2. verify `core-abi.sh`, `farm-libdbus-relocation.sh`, and VS Code workload probes;
3. inspect real pacman CacheDir and hook paths;
4. refactor `gl-farm` into candidate generation without active mutation;
5. add fingerprint/receipt generation;
6. add `gl-sync` transaction orchestration;
7. add lazy dirty-state check to `gl-run`;
8. add a minimal PostTransaction glibc hook that marks state dirty and runs only quick core validation;
9. test rollback by intentionally failing a candidate generation in a temporary farm root;
10. only then enable latest-first auto-sync behavior by default.
