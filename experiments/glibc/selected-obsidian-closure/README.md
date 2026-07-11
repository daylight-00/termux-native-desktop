# Selected Obsidian AppDir Closure Pilot

## Status

```text
ACTIVE_ARCHITECTURE_DISCRIMINATION
PARENT_QUESTION_NOT_CLOSED
PHASE_B1_PASS
PHASE_B2_PASS
PHASE_B3_CORRECTED_PASS
PHASE_B4_PASS
PHASE_B5_PASS_WITH_REVIEW
PHASE_B6_FIRST_RUN_DIAGNOSTIC_ONLY
PHASE_B6_CORRECTED_PASS
PHASE_B7_PASS
PHASE_B8_PASS
PHASE_B9_PASS
PHASE_B10_FIRST_RUN_LAUNCHER_DIAGNOSTIC
PHASE_B10_SECOND_RUN_SHORT_LIVED_MAIN_DIAGNOSTIC
PHASE_B10_SHORT_RUNTIME_PATH_DISCRIMINATOR_NEXT
```

The selected CPU generation is materialized and published but not activated.

## Authority

```text
docs/refactor/0092-post-graphics-closure-architecture-midpoint-audit.md
docs/refactor/0093-post-audit-direction-validator-lifecycle-and-selected-closure-reentry.md
docs/refactor/0094-selected-obsidian-phase-b1-retained-control-locality-pass.md
docs/refactor/0095-selected-obsidian-phase-b2-static-runtime-closure-pass.md
docs/refactor/0096-selected-obsidian-phase-b3-first-run-script-failure.md
docs/refactor/0097-selected-obsidian-phase-b3-capability-grouping-pass.md
docs/refactor/0098-selected-obsidian-phase-b4-entrypoint-static-matrix-pass.md
docs/refactor/0099-selected-obsidian-phase-b5-data-provenance-review.md
docs/refactor/0100-selected-obsidian-phase-b6-source-manifest-gap.md
docs/refactor/0101-selected-obsidian-phase-b6-corrected-schema-reproduction-pass.md
docs/refactor/0102-selected-obsidian-phase-b7-complete-cpu-manifest-pass.md
docs/refactor/0103-selected-obsidian-phase-b8-generation-layout-preflight-pass.md
docs/refactor/0104-selected-obsidian-phase-b9-first-run-hardlink-publication-failure.md
docs/refactor/0105-selected-obsidian-phase-b9-generation-directory-publication-failure.md
docs/refactor/0106-selected-obsidian-phase-b9-generation-materialization-pass.md
docs/refactor/0107-selected-obsidian-phase-b10-first-run-launcher-environment-failure.md
docs/refactor/0108-selected-obsidian-phase-b10-second-run-short-lived-main-diagnostic.md
```

## Closed generation boundary

```text
generation ID:
    obsidian-cpu-435ac66d15de2e9a3188

content objects:
    96

content bytes:
    70,897,301

generation aliases:
    175

staged/final validation:
    1851 / 1851 PASS

current:
    ABSENT
```

Immutable content:

```text
selected external static ELF              87
required NSS/security dynamic ELF          4
selected fonts                              4
generated GSettings aggregate               1
```

Referenced outside the generation:

```text
app-local ELF/data                         11
protected-world ELF/locale                 18
```

Excluded from CPU mode:

```text
Vulkan feature/provider ELF                11
mutable application state                  19
fontconfig cache                            4
Mesa cache                                  1
optional GPU device                         1
```

## Phase B10 validation target

Files:

```text
recipe/launch-obsidian-explicit-generation-cpu.sh
recipe/run-explicit-generation-cpu-validation.sh
recipe/analyze-explicit-generation-cpu.py
```

Loader and data contract:

```text
candidate loader injection:
    final Obsidian exec only

LD_LIBRARY_PATH:
    <generation>/lib:$PREFIX/glibc/lib

GSETTINGS_SCHEMA_DIR:
    <generation>/share/glib-2.0/schemas

font source:
    <generation>/share/fonts/selected

CPU flag:
    exact --disable-gpu

Vulkan/Mesa overrides:
    cleared

current:
    forbidden

broad farm:
    forbidden

rootfs providers:
    forbidden
```

Expected stable process topology:

```text
main:
    exactly 1

renderer:
    at least 1
    every renderer has --disable-gpu-compositing

zygote:
    at least 1

GPU process:
    0

survival:
    100 seconds
```

Expected immutable mapped identities:

```text
selected object-store identities           96
app-local identities                       11
protected-world identities                 18
                                          ---
total                                      125
```

## Phase B10 diagnostic history

### First run — launcher shell contamination

```text
receipt:
    selected-obsidian-phase-b10-explicit-generation-cpu-validation-20260712-005240

result:
    FAIL / capture

application exec:
    not reached

cause:
    candidate LD_LIBRARY_PATH exported in bionic launcher shell
    Termux mkdir attempted to resolve glibc libc.so
```

Correction:

```text
launcher shell LD_LIBRARY_PATH:
    UNSET

candidate loader injection:
    EXEC_ENV_ONLY
```

### Second run — short-lived main

```text
receipt:
    selected-obsidian-phase-b10-explicit-generation-cpu-validation-corrected-20260712-010602

archive SHA-256:
    01c14177d9ed32bb9de294aef2ccc64dba3e2afbbd1e82ed53eb705526ff3575

captured head:
    d6be102385140c61f92f1ca41028c90cbc866233

result:
    FAIL / capture

explicit main observed:
    YES

stable renderer/zygote:
    NO

current before/after:
    ABSENT / ABSENT
```

Observed runtime artifacts:

```text
SingletonLock -> localhost-4594
one Chromium scoped temporary directory
no SingletonSocket
no SingletonCookie
```

Observed path lengths:

```text
XDG config application path:
    178

Chromium scoped temp path:
    179

XDG runtime directory:
    170
```

Stderr contained only inotify sysctl-access and missing system-D-Bus warnings. No fatal loader or missing-library message was present.

The long runtime/socket path is therefore the next highest-value discriminator, not yet a closed root cause.

## Short runtime-path correction

The runner now creates:

```text
$PREFIX/tmp/o10.XXXXXXXX
```

and uses the conventional sublayout:

```text
fontconfig/
xdg/config/
xdg/cache/
xdg/data/
xdg/state/
xdg/runtime/
tmp/
bin/
```

Required pre-launch gate:

```text
TMPDIR length <= 64
```

After capture:

```text
short live runtime root
    -> cp -a to $OUT/runtime-evidence
    -> diff -qr equality gate
    -> short live root removal
```

Receipt files:

```text
runtime-root-contract.tsv
runtime-snapshot.tsv
runtime-evidence/
runtime-cleanup.status
capture-exit-status.txt
```

The real capture return code is now preserved; the prior negation-status bug is removed.

## Canonical short-path B10 command

```bash
cd "$HOME/projects/termux-native-desktop"

rm -rf \
  experiments/glibc/selected-obsidian-closure/recipe/__pycache__

git fetch origin
git merge --ff-only origin/docs/post-graphics-architecture-audit

B9_OUT="$PREFIX/tmp/selected-obsidian-closure/selected-obsidian-phase-b9-generation-publication-corrected-20260712-003136"
out="selected-obsidian-phase-b10-short-runtime-cpu-validation-$(date +%Y%m%d-%H%M%S)"
OUT="$PREFIX/tmp/selected-obsidian-closure/$out"

if B9_OUT="$B9_OUT" \
   OUT="$OUT" \
   bash \
     experiments/glibc/selected-obsidian-closure/recipe/run-explicit-generation-cpu-validation.sh
then
  analysis_rc=0
else
  analysis_rc=$?
fi

printf '\n===== analysis exit status =====\n'
printf '%s\n' "$analysis_rc"

for f in \
  "$OUT/analysis.status" \
  "$OUT/failure-stage.txt" \
  "$OUT/next-state.txt" \
  "$OUT/summary.tsv" \
  "$OUT/runtime-root-contract.tsv" \
  "$OUT/runtime-snapshot.tsv" \
  "$OUT/runtime-cleanup.status" \
  "$OUT/capture-exit-status.txt" \
  "$OUT/runtime-contract.tsv" \
  "$OUT/launch-script-identity.tsv" \
  "$OUT/launch-contract/launch-environment.tsv" \
  "$OUT/launch-contract/argv.txt" \
  "$OUT/process-contract.tsv" \
  "$OUT/missing-expected-mapped-paths.tsv" \
  "$OUT/unexpected-mapped-paths.tsv" \
  "$OUT/mapped-identity-verification.tsv" \
  "$OUT/mapped-path-classification.tsv" \
  "$OUT/current-state-before.tsv" \
  "$OUT/current-state-after.tsv" \
  "$OUT/capture/class-counts.tsv" \
  "$OUT/capture/processes.tsv" \
  "$OUT/capture/last-processes.tsv" \
  "$OUT/capture/launch.stdout" \
  "$OUT/capture/launch.stderr" \
  "$OUT/claim-boundary.txt"
do
  [ -e "$f" ] || continue
  printf '\n===== %s =====\n' "$f"
  cat "$f"
done

tar czf ~/Downloads/$out.tgz $OUT
```

## Expected next state after PASS

```text
READY_FOR_ATOMIC_ACTIVATION_IMPLEMENTATION
```

## Stop line

Do not:

```text
rerun Phase B1-B9;
change generation content or loader order in the short-path test;
create current;
change the promoted launcher;
add broad-farm or rootfs paths;
include excluded graphics objects in CPU mode;
interpret the current path-length hypothesis as proven before rerun;
garbage-collect the generation or object store;
start PyMOL by extending the broad farm.
```
