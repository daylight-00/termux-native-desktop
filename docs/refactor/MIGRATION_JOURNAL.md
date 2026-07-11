# Migration Journal

This journal records major migration state transitions. Detailed evidence and false-negative corrections remain in the numbered `docs/refactor/` records.

## 2026-07-09 — Refactor initialization

### Input state

- user local checkout clean: `## main...origin/main`;
- remote base commit: `3cf41d6fc47050b06e18e956a23cefe25e4fb82a`;
- refactor branch created: `refactor/module-package-layout`;
- container network `git clone` attempt failed because `github.com` DNS could not be resolved;
- authenticated GitHub connector selected for repository reads and writes;
- local working mirrors under `/mnt/data/` used for design material and generated evidence.

### Initial ownership decisions

- `startxfce-x11` -> desktop module;
- `gl/env`, `gl-run`, `gl-farm`, shim, glibc target wrappers -> transitional gl module grouping;
- VS Code and Obsidian launchers -> package owners;
- Mesa build definition -> Mesa package;
- Mesa bisect judges -> SIGBUS experiment recipe;
- deploy helper -> repository tool;
- no live build/install prefix cleanup in the ownership refactor.

The later architecture reassessment retains the ownership moves but rejects `modules/gl` as one final semantic object.

## 2026-07-09 — Ownership move preparation

- Mesa bisect judges moved to experiment ownership.
- VS Code and Obsidian launchers moved to package ownership.
- generic `gl/bin` initially retained only layer commands (`gl-run`, `gl-farm`).
- Mesa patch path retained compatibility with the existing live build tree.

## 2026-07-09 — Deploy rewrite and smoke validation

`tools/deploy` was designed to:

1. resolve repository root from tool location;
2. support `--dry-run`;
3. deploy module overlays as leaf symlinks;
4. convert legacy directory symlinks before leaf deployment;
5. refuse unmanaged real-file replacement;
6. install application launchers from package owners;
7. preserve Mesa live build compatibility paths;
8. remove only obsolete symlinks, never real directories.

A temporary-home smoke test found and corrected:

```text
Bash function variable leakage
legacy-view dry-run target handling
Mesa compatibility-path handling
```

Repository deploy smoke passed.

## 2026-07-09 — CPython, shell, and uv-base ownership

The CPython Android runtime was recorded as an external package consumer identity rather than committed as a runtime archive.

The shell and uv-base definitions were split into explicit owners.

Key decisions:

```text
system/infrastructure Python remains separate
uv-base owns personal Python definition
.venv is generated state
no global VIRTUAL_ENV export
stale Conda shell source removed from native shell model
```

Shell layout, adoption, and uv-base validation passed.

## 2026-07-09 — Connector write-order incidents and recovery

Several GitHub contents-API writes advanced the branch while separately created tree commits remained unattached.

Recovery policy:

```text
treat actual branch tip as authoritative
rebuild intended tree on that tip
never force-rewrite history
compare branch state after grouped phases
document incidents
```

## 2026-07-09 — Live ownership migration passed

The repository ownership migration was deployed to the real device.

Accepted results:

```text
module/package/tool owners installed
public launchers point to package owners
session source tracked under desktop module
shell and uv-base ownership adopted
repository relocated to $HOME/projects/termux-native-desktop
legacy checkout identity retired
```

The old statement that live migration had not run is superseded by `0011-phase-b-runtime-deploy-passed.md` and subsequent live receipts.

## 2026-07-10 — Post-refactor glibc ABI incident

VS Code failed after the refactor, but the failure was reduced independently to:

```text
Debian-derived libdbus
    requires __vsyslog_chk@GLIBC_2.17

installed Termux glibc 2.43
    does not export it
```

The incident proved:

```text
substrate/provider ABI compatibility is first-class;
farm regeneration cannot repair a broken substrate;
provider rollback != substrate rollback.
```

The concrete broad-farm/pacman-hook lifecycle plan in `0014` was paused pending top-down reassessment.

## 2026-07-10 — Architecture reassessment and semantic inventory

The project reconciled the ownership refactor with the system-foundation model.

Accepted direction:

```text
preserve validated semantics and evidence
not command names, facades, or umbrella objects

modules/gl
    = transitional physical deployment grouping
    != final semantic owner

broad farm
    = research/control/compatibility mechanism
    != established production target

package manager
    = supply backend implementation
    != architecture authority
```

The real device established APT/dpkg as the current glibc substrate backend.

## 2026-07-10 — glibc 2.42 recovery and containment

Exact glibc 2.42 artifact recovery was simulated, then applied through the package-managed path.

The tested VS Code workload recovered through:

```text
core ABI gate
provider relocation gate
CLI GPU/CPU checks
real GUI validation
```

The package remains held at 2.42 as temporary containment.

A corrected current/newer substrate lifecycle remains open.

## 2026-07-10 — First selected-provider closure passed

The bounded D-Bus pilot produced a materialized candidate containing:

```text
libdbus
libsystemd
libcap
```

The pilot proved:

```text
static/runtime selected-set agreement
actual candidate-owned provider bytes
provenance receipt
candidate-specific actual-selection proof
protected substrate boundary
zero broad-farm/rootfs provider leakage
```

It did not prove one world-global shared-provider object.

## 2026-07-10 to 2026-07-11 — Obsidian application-domain pilot

Obsidian was selected as the second closure pilot to test:

```text
real Electron multiprocess composition
application-local $ORIGIN locality
world/prefix/rootfs provider boundaries
font/locale/schema data
candidate workload equivalence
```

Control capture, provenance enrichment, semantic classification, and graphics provider decomposition advanced.

The parent pilot remains incomplete:

```text
locality-shadowing:
    OPEN

non-graphics static/runtime closure agreement:
    OPEN

candidate materialization/equivalence:
    NOT COMPLETED
```

## 2026-07-11 — Scoped graphics-policy architecture discrimination

The project separated:

```text
world-boundary sanitation
Vulkan provider selection
OpenGL bridge selection
application feature mode
consumer-specific suitability
selected-device evidence
application-state authority
```

Key results:

```text
standalone Zink explicit Turnip:
    PASS

standalone Zink implicit/default:
    llvmpipe discovered, CPU device rejected

standalone Zink implicit/software intent:
    PASS

Electron explicit provider:
    Turnip / Adreno 730

Electron implicit provider control:
    LVP / llvmpipe primary device
```

This established that provider policy and device intent are separate and consumer-aware.

## 2026-07-11 — Scoped graphics-policy promotion closed

The promoted transaction passed:

```text
expanded source/pre-deploy
expanded live installation
current OpenGL/Zink renderer
VS Code GPU
VS Code CPU
Obsidian GPU
Obsidian CPU
```

Canonical closure:

```text
docs/refactor/0091-scoped-graphics-policy-promotion-closure.md
```

Accepted semantic contract:

```text
glibc boundary removes inherited bionic graphics policy
baseline selects no provider/bridge
hardware provider is explicit and consumer-scoped
OpenGL consumer owns Zink bridge
Electron domain owns GPU/CPU feature mode
validation owns isolated application state
selected GPU requires correlated evidence
revalidation is trigger-based
```

The closure validates semantics, not permanent adapter/path identity.

## 2026-07-11 — Post-closure architecture midpoint audit

Audit:

```text
docs/refactor/0092-post-graphics-closure-architecture-midpoint-audit.md
```

The audit confirms the project is on track but identifies remaining top-down pressure:

```text
resume or terminate selected Obsidian closure
separate semantic invariants from current adapters
split remaining gl umbrella responsibilities
move high-risk Electron/security policy out of world baseline when validated
define atomic activation before another multi-file migration
define glibc substrate upgrade/recovery lifecycle
synchronize canonical documentation
classify active versus historical validators
use PyMOL only after reusable objects are decided
```

## Current migration state

```text
ownership migration:
    DEPLOYED

ABI incident recovery:
    CLOSED FOR TESTED WORKLOAD

D-Bus selected-provider pilot:
    PASS

Obsidian selected application-domain closure:
    ACTIVE / INCOMPLETE

scoped graphics-policy promotion:
    CLOSED

atomic activation:
    OPEN

glibc newer-substrate lifecycle:
    OPEN

PyMOL runtime pilot:
    DEFERRED
```
