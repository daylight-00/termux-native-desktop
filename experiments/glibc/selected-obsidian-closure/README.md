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
PHASE_B6_CORRECTED_PASS
PHASE_B7_PASS
PHASE_B8_PASS
PHASE_B9_PASS
PHASE_B10_LAUNCHER_DIAGNOSTIC_CLOSED
PHASE_B10_SHORT_PATH_TOPOLOGY_PASS
PHASE_B10_SURVIVAL_GTK_PIXBUF_FAILURE
PIXBUF_ICON_MIME_SOURCE_INVENTORY_NEXT
```

The selected CPU generation is materialized and immutable but not activated.

## Authority

```text
docs/refactor/0106-selected-obsidian-phase-b9-generation-materialization-pass.md
docs/refactor/0107-selected-obsidian-phase-b10-first-run-launcher-environment-failure.md
docs/refactor/0108-selected-obsidian-phase-b10-second-run-short-lived-main-diagnostic.md
docs/refactor/0109-selected-obsidian-phase-b10-short-runtime-topology-pass-gtk-pixbuf-survival-failure.md
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

## Phase B10 diagnostic history

### Launcher-shell contamination

```text
application exec:
    not reached

cause:
    candidate LD_LIBRARY_PATH reached a bionic mkdir

correction:
    launcher shell LD_LIBRARY_PATH unset
    candidate loader injection final exec only
```

### Long runtime path

```text
explicit main:
    observed

renderer/zygote:
    not stabilized

runtime paths:
    170-179 characters

SingletonSocket:
    not created
```

### Short runtime path

Receipt:

```text
selected-obsidian-phase-b10-short-runtime-cpu-validation-20260712-012415
```

Archive SHA-256:

```text
529e42fbc338148f5adf36cbabc1c8a1ebc16e9408e5850dd56f5194ac92f9fe
```

Captured head:

```text
e9a44c7bcd52b35e433d9b9850469c9b1bb7db99
```

Runtime contract:

```text
runtime root length:
    48

TMPDIR length:
    52

XDG_CONFIG_HOME length:
    59

runtime snapshot:
    MATCH
```

Topology:

```text
topology.status:
    PASS

main:
    1

zygote:
    3

utility:
    1

renderer:
    1

GPU process:
    0

renderer --disable-gpu-compositing:
    present
```

The short path produced `SingletonLock`, `SingletonSocket`, `SingletonCookie`, and the Chromium scoped temporary directory. The long-path hypothesis is therefore supported for startup.

Survival:

```text
survival.status:
    FAIL main process exited

recorded survival samples with complete topology:
    28

approximate process lifetime:
    72 seconds
```

Fatal chain:

```text
hicolor icon theme not found
    -> GTK fallback image-missing.png
    -> GdkPixbuf: Unrecognized image file format
    -> gtkiconhelper assertion
    -> application bailout
```

`current` remained absent before and after. Maps acceptance was not reached because survival failed.

## Open architecture boundary

The generation contains:

```text
libgdk_pixbuf-2.0.so.0
libpng16.so.16
libjpeg.so.62
```

The accepted data manifest contains:

```text
4 selected fonts
1 generated GSettings aggregate
12 protected-world locale files
```

It does not contain an explicit contract for:

```text
gdk-pixbuf loader cache
gdk-pixbuf loader modules
icon-theme index/data
shared MIME database
```

This is a runtime data/plugin capability gap not established by the mapped-object closure.

## Next stage — read-only capability inventory

Recipe:

```text
recipe/inspect-gtk-pixbuf-runtime-capability.py
```

It consumes the completed Phase B9 receipt and the short-runtime B10 failure receipt.

It performs:

```text
B9/B10 receipt verification;
rootfs gdk-pixbuf loader-cache discovery;
loader-module discovery;
cache-reference parsing;
package/version/SHA-256 ownership capture;
icon-theme index inventory;
shared MIME database inventory;
B9 semantic-manifest gap comparison.
```

It does not:

```text
launch Obsidian;
modify the generation;
create current;
change the promoted launcher.
```

Expected next state:

```text
READY_FOR_CONTROLLED_PIXBUF_RUNTIME_DIAGNOSTIC
```

### Canonical command

```bash
cd "$HOME/projects/termux-native-desktop"

rm -rf \
  experiments/glibc/selected-obsidian-closure/recipe/__pycache__

git fetch origin
git merge --ff-only origin/docs/post-graphics-architecture-audit

B9_OUT="$PREFIX/tmp/selected-obsidian-closure/selected-obsidian-phase-b9-generation-publication-corrected-20260712-003136"
B10_OUT="$PREFIX/tmp/selected-obsidian-closure/selected-obsidian-phase-b10-short-runtime-cpu-validation-20260712-012415"

out="selected-obsidian-gtk-pixbuf-runtime-capability-inventory-$(date +%Y%m%d-%H%M%S)"
OUT="$PREFIX/tmp/selected-obsidian-closure/$out"

if B9_OUT="$B9_OUT" \
   B10_OUT="$B10_OUT" \
   OUT="$OUT" \
   python \
     experiments/glibc/selected-obsidian-closure/recipe/inspect-gtk-pixbuf-runtime-capability.py
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
  "$OUT/input-verification.tsv" \
  "$OUT/failure-evidence.tsv" \
  "$OUT/pixbuf-loader-cache.tsv" \
  "$OUT/pixbuf-cache-references.tsv" \
  "$OUT/pixbuf-loader-modules.tsv" \
  "$OUT/gtk-data-capability.tsv" \
  "$OUT/semantic-coverage-gaps.tsv" \
  "$OUT/claim-boundary.txt"
do
  [ -e "$f" ] || continue
  printf '\n===== %s =====\n' "$f"
  cat "$f"
done

tar czf ~/Downloads/$out.tgz $OUT
```

## Stop line

Do not:

```text
rerun Phase B1-B9;
rerun B10 blindly;
modify the immutable generation before inventory;
copy the whole rootfs icon/MIME tree;
add rootfs or broad-farm paths to an acceptance run;
create current;
change the promoted launcher;
follow archived SingletonSocket symlinks during extraction;
garbage-collect the generation or object store;
start PyMOL by extending the broad farm.
```
