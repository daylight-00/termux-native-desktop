# 0110 — Selected Obsidian Pixbuf Inventory Pass and Interaction-Boundary Correction

## Status

The GTK pixbuf/icon/MIME source inventory passed. A direct operator observation also corrects the interpretation of the preceding short-runtime B10 receipt.

```text
inventory.status:
    PASS

inventory next state:
    READY_FOR_CONTROLLED_PIXBUF_RUNTIME_DIAGNOSTIC

short-runtime initial window:
    DISPLAYED SUCCESSFULLY

fatal trigger:
    OPERATOR CLICKED THE VAULT-OPEN CONTROL

passive idle survival:
    NOT MEASURED CLEANLY
```

The short-runtime receipt is therefore an interaction-triggered file-chooser failure receipt, not evidence that the initial Obsidian window spontaneously aborted after approximately 72 seconds.

## Operator-observation provenance

The following fact comes from direct operator observation rather than a machine-recorded input event:

```text
The Obsidian initial window appeared.
The operator clicked the control used to open a vault.
The GTK failure occurred after that click.
```

The capture receipt records the process topology and fatal GTK chain, but does not timestamp or encode the mouse click. The operator observation is retained as a separate evidence class and must not be represented as if it came from `/proc`, stderr, or the capture script.

## Corrected claim split

The previous single B10 survival claim must be divided.

### Passive initial-window claim

```text
launch explicit immutable generation;
form main/zygote/renderer CPU topology;
perform no GUI input;
survive 100 seconds;
capture maps;
verify the expected immutable identity set.
```

This claim remains open because the previous run was perturbed by operator input during the survival interval.

### Interactive vault-open claim

```text
launch explicit immutable generation;
click the vault-open control;
exercise GTK file chooser, icons, MIME data, and pixbuf loaders;
remain alive and usable.
```

The previous short-runtime receipt proves this interactive claim currently fails in GTK icon/pixbuf handling.

Passing the passive claim does not close the interactive claim. A usable Obsidian deployment requires both.

## Authoritative inventory receipt

Archive:

```text
selected-obsidian-gtk-pixbuf-runtime-capability-inventory-20260712-014314.tgz
```

Archive SHA-256:

```text
e9f5fc256dbbe74e6b060fb8ebfde8745959321d20a58f8d7bd4181d19be3be6
```

Captured repository state:

```text
branch:
    docs/post-graphics-architecture-audit

head:
    a1ba53e48146dc5eeb68901bea7725a2bfcbf56e
```

Archive structure:

```text
members:
    12

absolute paths:
    0

parent traversal:
    0

symlink/hardlink/device/special members:
    0
```

## Inventory result

```text
analysis.status:
    PASS

next-state:
    READY_FOR_CONTROLLED_PIXBUF_RUNTIME_DIAGNOSTIC

topology status inherited from B10:
    PASS

survival status inherited from B10:
    FAIL main process exited

GPU process observed:
    NO

current pointer changed:
    NO
```

The inherited survival result is now interpreted as interaction-triggered rather than passive.

## GdkPixbuf loader cache

One cache exists:

```text
$ROOTFS/usr/lib/aarch64-linux-gnu/gdk-pixbuf-2.0/2.10.0/loaders.cache
```

Identity:

```text
SHA-256:
    b1413b11f2a94c873d3f6825e897208b85986d818adad33ed017150580a9949d

package ownership:
    UNOWNED

referenced modules:
    12
```

The unowned status is expected for a generated cache file and is not a provenance failure by itself.

Every cache reference is written as an FHS absolute path:

```text
/usr/lib/aarch64-linux-gnu/gdk-pixbuf-2.0/2.10.0/loaders/<module>.so
```

Namespace result:

```text
written cache paths present in native namespace:
    0 / 12

rootfs-prefixed referenced modules present:
    12 / 12
```

Therefore the retained cache cannot be used unchanged outside PRoot/chroot. Any native diagnostic must create a receipt-local relocated cache with exact native absolute paths. Blindly setting `GDK_PIXBUF_MODULE_FILE` to the rootfs cache would preserve broken `/usr/...` references.

## Loader modules

Discovered modules:

```text
count:
    12

libgdk-pixbuf-2.0-0:arm64 2.42.12+dfsg-4+deb13u1:
    ani
    bmp
    gif
    icns
    ico
    pnm
    qtif
    tga
    tiff
    xbm
    xpm

librsvg2-common:arm64 2.60.0+dfsg-1:
    svg
```

Every module has a captured SHA-256 and byte size in `pixbuf-loader-modules.tsv`.

The inventory does not identify an external PNG module. It therefore does not yet prove whether the fatal embedded PNG fallback requires a relocated module cache, a library build-time loader registration path, icon data that avoids fallback, or a combination.

## GTK data inventory

Icon-theme indexes:

```text
Adwaita/index.theme
    package: adwaita-icon-theme 48.1-1

hicolor/index.theme
    package: hicolor-icon-theme 0.18-2
```

Shared MIME database files:

```text
aliases
globs
globs2
mime.cache
subclasses
```

The selected MIME files and generated loader cache were reported as unowned by the simple dpkg list lookup. This is expected for generated/maintainer-script products but requires a later generation contract based on source/package and reproduction, not merely copied generated bytes.

## Semantic-manifest gap

Discovered paths absent from the B9 semantic manifest:

```text
loader cache:
    1

loader modules:
    12

icon-theme indexes:
    2

MIME database files:
    5

combined:
    20
```

All twenty are absent. This confirms a real coverage gap in the prior maps-plus-selected-data model.

It does not mean all twenty must enter the final immutable generation.

## Direction decision

The next execution order is:

```text
1. Passive no-input B10
    establish initial-window 100-second survival and maps without user interaction

2. Controlled vault-open diagnostic
    use a receipt-local relocated pixbuf loader cache
    intentionally reference exact rootfs loader modules
    record rootfs-provider mappings as diagnostic-only

3. If loader-cache-only still fails
    add exact icon-theme data as a separate discriminator

4. Define the minimum reproducible data/plugin capability

5. Create a new generation
    never mutate the published B9 generation in place

6. Re-run passive and interactive acceptance
```

## Passive wrapper

A dedicated wrapper records the operator contract:

```text
recipe/run-passive-explicit-generation-cpu-validation.sh
```

Receipt contract:

```text
mode:
    PASSIVE_NO_GUI_INPUT

operator action:
    OBSERVE_ONLY

forbidden action:
    DO_NOT_CLICK_OPEN_VAULT_OR_ANY_GUI_CONTROL

interactive file chooser capability:
    OUT_OF_SCOPE
```

The wrapper cannot technically prove absence of human input. The operator must follow the displayed instruction, and that compliance remains operator evidence.

## Claim boundary

This inventory and correction prove:

```text
the initial short-runtime window appeared;
the prior fatal event followed a vault-open click;
the required CPU topology formed before the click-triggered failure;
one loader cache references twelve modules at unusable native `/usr/...` paths;
the exact rootfs-prefixed modules all exist;
twenty pixbuf/icon/MIME capability paths were absent from the B9 manifest;
the immutable generation and current pointer were not mutated.
```

They do not prove:

```text
passive 100-second survival;
exact 125-object passive maps acceptance;
which minimum pixbuf/icon/MIME subset is required;
a relocated cache fixes the vault-open path;
interactive Obsidian usability;
activation readiness.
```

## Stop line

Do not:

```text
describe the short-runtime failure as spontaneous idle abort;
merge passive and interactive claims;
mutate the existing immutable generation;
copy all twenty discovered paths into the generation;
use the rootfs loaders.cache unchanged;
claim operator input timing as machine-captured evidence;
create current;
change the promoted launcher.
```
