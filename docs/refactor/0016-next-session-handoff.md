# 0016 — Next Session Handoff

## Purpose

This document is the operational handoff for the next development session.

The next session should not resume from the last implementation idea by inertia. It should resume from the current architecture decision.

## Repository and branch context

Repository:

```text
daylight-00/termux-native-desktop
```

Active refactor branch:

```text
refactor/module-package-layout
```

The branch and `main` diverged from:

```text
3cf41d6fc47050b06e18e956a23cefe25e4fb82a
```

Important architecture foundation on `main`:

```text
docs/system-foundation/
```

Latest architectural direction on `main`:

```text
docs/system-foundation/11-architecture-reassessment-and-hard-refactor-decision.md
```

Latest branch-specific direction:

```text
docs/refactor/0015-architecture-reassessment-and-hard-refactor-direction.md
```

## Mandatory reading order

Read before proposing implementation:

```text
main:
    docs/system-foundation/01-essence.md
    docs/system-foundation/02-principles-and-invariants.md
    docs/system-foundation/03-system-model-v2.md
    docs/system-foundation/04-domain-capability-bridge-model.md
    docs/system-foundation/05-ideal-target-architecture.md
    docs/system-foundation/11-architecture-reassessment-and-hard-refactor-decision.md

refactor/module-package-layout:
    docs/refactor/0001-current-state-inventory.md
    docs/refactor/0002-ownership-map.md
    docs/refactor/0011-phase-b-runtime-deploy-passed.md
    docs/refactor/0012-post-refactor-vscode-libdbus-abi-regression.md
    docs/refactor/0013-vscode-libdbus-root-cause-confirmed.md
    docs/refactor/0014-robust-gl-update-and-farm-lifecycle.md
    docs/refactor/0015-architecture-reassessment-and-hard-refactor-direction.md
```

Read actual implementation objects too:

```text
modules/gl/README.md
modules/gl/overlay/home/gl/env
modules/gl/overlay/home/gl/bin/gl-run
modules/gl/overlay/home/gl/bin/gl-farm
modules/gl/tests/core-abi.sh
modules/gl/tests/farm-libdbus-relocation.sh
packages/vscode/
packages/obsidian/
packages/mesa-glibc/
tools/deploy
```

## Current architectural conclusion

The directory ownership refactor was valuable and remains accepted.

However:

```text
modules/gl
```

is not accepted as one final semantic object.

It still combines:

```text
world substrate/base policy
shared-library provider materialization
OpenGL/Zink capability composition
Vulkan provider selection
font/locale/TLS policies
URL-open bridge
build target toolchain
```

Do not add more lifecycle authority to this umbrella before semantic decomposition.

## Current implementation stop line

Do not implement yet:

```text
gl-sync
gl-status
gl-run auto-sync
pacman transaction hooks
single global compatibility fingerprint
generational broad-farm activation
new global gl environment policy
```

Allowed work:

```text
read-only inspection
identity capture
incident recovery
regression validation
semantic inventory
contract design
small discriminating experiments
```

## Immediate technical incident

Confirmed failure:

```text
Debian rootfs libdbus-1.so.3.38.3
    requires __vsyslog_chk@GLIBC_2.17

installed Termux glibc 2.43 libc.so.6
    does not export it
```

The failure reproduces independently of VS Code through relocation testing.

This means:

```text
core substrate broken
    +
farm rebuild
    =
still broken
```

First restore the substrate contract, then rerun:

```text
modules/gl/tests/core-abi.sh
modules/gl/tests/farm-libdbus-relocation.sh
VS Code real workload probe
```

Preserve evidence before changing unrelated runtime state.

## Primary next design task

The next architecture task is a semantic inventory of the current `gl` umbrella.

For every file, environment variable, helper, and path assumption, record:

```text
mechanism
semantic purpose
current owner
actual consumers
minimum valid scope
evidence
candidate semantic owner
migration/removal condition
```

Owner categories:

```text
world
provider
bridge
toolchain
application family
specific application
validation only
supply adapter
```

The inventory should answer, among others:

```text
DISPLAY
XDG_RUNTIME_DIR
TMPDIR
XDG_DATA_DIRS
FONTCONFIG_PATH
FONTCONFIG_FILE
LOCPATH
LC_ALL
GSETTINGS_BACKEND
NO_AT_BRIDGE
ELECTRON_DISABLE_SANDBOX
DBUS_* clearing
TLS certificate variables
VK_ICD_FILENAMES
VK_DRIVER_FILES
MESA_LOADER_DRIVER_OVERRIDE
xdg-open shim
glibc target wrappers
farm scan directories
denylist
basename collision policy
ldconfig coupling
```

Do not move files merely to make the tree aesthetically match the model. First resolve semantic ownership.

## Substrate authority task

Do not assume pacman is required.

Capture actual device facts:

```text
which package database owns the installed glibc substrate
how glibc is updated today
which files are package-owned
whether exact previous artifacts are available
whether rollback is actually possible
what install/config semantics a direct artifact model would need to preserve
```

Architecture requirement:

```text
world.glibc
    -> backend-neutral substrate source adapter
```

Possible backend implementations may include pacman, another existing package backend, exact verified artifacts, or a project build path if evidence justifies the maintenance cost.

Installing/switching a package manager merely for change hooks is not accepted.

## Shared-library architecture task

Do not assume the broad farm is the target.

Treat it as:

```text
research compatibility pool
control/reference environment
transitional baseline
```

Design one bounded selected-closure pilot:

```text
manifest/domain target
    -> static ELF dependency closure
    -> protected world-owned exclusion
    -> preserve app-local $ORIGIN locality
    -> dynamic runtime evidence enrichment
    -> materialize selected provider bytes
    -> provenance receipt
    -> candidate-specific validation
```

Do not migrate VS Code first unless a smaller bounded target cannot exercise the required mechanism.

## Candidate validation requirement

A candidate test must prove the candidate was actually selected.

Do not accept:

```text
candidate files exist
    -> therefore candidate validated
```

Require evidence of:

```text
actual mapped provider identity
actual loader resolution path
no silent substitution from active cache/path state
```

## Design philosophy

The project owner explicitly prefers:

```text
minimum manipulation
maximum effect
```

and is willing to hard-refactor or delete early objects when they constrain the correct architecture.

Therefore:

```text
working before
    !=
must preserve API

existing command
    !=
architectural object

package manager available
    !=
package manager justified

compatibility facade useful during migration
    !=
compatibility facade permanent
```

Preserve evidence and validated semantics. Remove structural debt early when the object model is wrong.

## Expected next-session output

The next session should ideally produce:

```text
1. verified incident-recovery state or precise blocker
2. semantic inventory table for current gl umbrella
3. proposed semantic ownership split
4. substrate-authority evidence from the real device
5. explicit decision criteria for provider-closure pilot target
6. updated docs before or together with structural changes
```

If implementation is attempted, it must be justified from those outputs rather than from the existence of old commands.

## Decision precedence

Use:

```text
system-foundation/11
    -> architectural rationale

refactor/0015
    -> branch implementation direction

this handoff
    -> next-session operational entrypoint
```

`0014` remains valuable for transactional principles but no longer defines the next implementation sequence.
