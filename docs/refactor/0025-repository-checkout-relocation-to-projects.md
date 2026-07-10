# 0025 — Repository Checkout Relocation to `~/projects`

## Status

The canonical live-device checkout location is changed from:

```text
$HOME/termux-native-desktop
```

to:

```text
$HOME/projects/termux-native-desktop
```

This is an operator/workspace topology decision, not a change to the repository's semantic identity.

## Rationale

The home root should not accumulate project source trees alongside runtime state and application payloads.

The intended separation is:

```text
$HOME/projects/
    source checkouts and active project work

$HOME/gl/
    current foreign-world runtime/provider state and compatibility surfaces

$HOME/opt/
    installed project-managed runtime prefixes

$HOME/.local/state/
    durable local state, receipts, recovery artifacts, adoption backups

$PREFIX/
    Termux-managed substrate and native package state
```

The repository checkout path must not become architectural object identity.

## Invariant

```text
repository source root is movable
    +
live managed symlinks may point into the current checkout
    +
relocation is repaired by explicit adoption/deploy relink
    +
old checkout path is not preserved as a compatibility symlink
```

The last rule matters. Leaving:

```text
$HOME/termux-native-desktop -> $HOME/projects/termux-native-desktop
```

would hide stale path assumptions and preserve accidental object identity.

## Current implementation behavior

### `tools/deploy`

`tools/deploy` derives repository root from its own location and updates managed leaf symlinks with `ln -sfn`.

Therefore runtime-facing module links, package entrypoints, and Mesa maintenance compatibility links can be safely rebound after repository relocation.

### `tools/adopt-user-env`

Before this decision, hash-guarded adopted top-level links such as:

```text
$HOME/.bashrc
$HOME/uv-base/pyproject.toml
$HOME/uv-base/uv.lock
```

could not be rebound after checkout relocation because a stale/broken symlink would fall into regular-file verification.

The adoption tool is now relocation-aware for exactly the known legacy checkout root:

```text
$HOME/termux-native-desktop
```

It accepts and rewrites only managed links whose raw target exactly matches the legacy root plus the expected repository-relative source path.

Unknown symlinks are still rejected.

## Migration procedure

### Preconditions

```text
branch synced at old checkout
working tree clean
no active write operation using the old checkout path
VS Code window for the old workspace closed before move
```

### Move

```bash
OLD="$HOME/termux-native-desktop"
NEW="$HOME/projects/termux-native-desktop"

mkdir -p "$HOME/projects"
test -d "$OLD"
test ! -e "$NEW"

cd "$HOME"
mv "$OLD" "$NEW"
cd "$NEW"
```

### Rebind adopted user environment

```bash
tools/adopt-user-env --dry-run
tools/adopt-user-env --apply
```

The apply run must:

```text
relink known stale adopted top-level links
refresh shell config leaf links
leave adoption backups unchanged
leave uv-base .venv unchanged
leave CPython prefix/artifact state unchanged
```

### Rebind runtime-facing deployment links

```bash
tools/deploy --dry-run
tools/deploy
```

The apply run must update managed leaf symlinks to the new checkout root without rebuilding runtime payloads or provider state.

## Validation

### Repository identity

```bash
pwd
git status --short --branch
git rev-parse --show-toplevel
```

Expected top level:

```text
$HOME/projects/termux-native-desktop
```

### Adopted links

```bash
readlink -f "$HOME/.bashrc"
readlink -f "$HOME/uv-base/pyproject.toml"
readlink -f "$HOME/uv-base/uv.lock"
```

All must resolve under the new checkout root.

### Managed runtime links

Inspect representative links:

```bash
readlink -f "$HOME/.local/bin/code"
readlink -f "$HOME/gl/bin/gl-run"
readlink -f "$HOME/gl/toolchain/glibc-gcc"
readlink -f "$HOME/gl/build/build-mesa.sh"
```

All repository-owned sources must resolve under the new checkout root.

### No stale legacy checkout targets

```bash
OLD="$HOME/termux-native-desktop"

{
    [ -L "$HOME/.bashrc" ] && printf '%s\n' "$HOME/.bashrc"
    find \
        "$HOME/.config/bash" \
        "$HOME/uv-base" \
        "$HOME/.local/bin" \
        "$HOME/gl/bin" \
        "$HOME/gl/shims" \
        "$HOME/gl/toolchain" \
        "$HOME/gl/build" \
        -type l \
        -lname "$OLD/*" \
        -print
} | while IFS= read -r link; do
    [ -n "$link" ] || continue
    target=$(readlink "$link")
    case "$target" in
        "$OLD"/*) printf 'STALE\t%s\t%s\n' "$link" "$target" ;;
    esac
done
```

Expected output:

```text
<empty>
```

### Runtime regression checks

After relocation:

```text
core ABI gate
libdbus relocation gate
VS Code CLI gate
```

must remain valid before continuing the selected-closure pilot.

## Historical evidence policy

Historical records that truthfully captured the old checkout path are not rewritten.

For example, prior evidence may contain:

```text
$HOME/termux-native-desktop
```

as the real path at the time of observation.

Only current operational instructions and current-state documentation use:

```text
$HOME/projects/termux-native-desktop
```

This preserves provenance rather than making the final layout appear inevitable.

## Selected-closure pilot impact

The active pilot scripts derive their experiment directory from script location and do not require the checkout to remain at the old home-root path.

The existing probe binary under:

```text
experiments/glibc/selected-dbus-closure/work/
```

moves with the checkout.

The first control evidence under `$PREFIX/tmp` remains valid historical evidence and is not moved.

Because the first static discovery run terminated before complete traversal, the static stage must be rerun after the checkout move with the corrected discovery harness.
