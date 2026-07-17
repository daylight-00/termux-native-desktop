# libxkbcommon bounded provider authority and filename continuity

## Decision

The exact Termux glibc member `libxkbcommon.so.0.8.0` is accepted only as the XKB context, keymap, keyboard-state, modifier, and keysym translation provider used by the selected GTK 3.24.49 Wayland keymap path.

```text
root review:       generic-root-review:778b62f6da21fd02f1bb
recipe root:       gpkg/libxkbcommon
recipe tree:       5fda5da07e6b38230082785d352adc4e6fb9c4da
build script blob: cc2f8554e83ee435400d0e5231f3870b8316fc91
artifact:          libxkbcommon-glibc 1.8.0
artifact SHA-256:  e58eca6f9c0e0d068d80dabd3b289d6b1b4cdaa25fc91053d21392ecfbf54f97
selected row:      selected:0eab80f8c75b58f5c92a
selected label:    libxkbcommon.so.0.0.0
member:            libxkbcommon.so.0.8.0
member SHA-256:    fee84d5d95a085a94d300186040a54b9844a491b599b1156867624af6b4e8ba9
SONAME:            libxkbcommon.so.0
```

## Class B boundary

The recipe's custom `termux_step_configure()` delegates exactly to `termux_step_configure_meson`. It adds no package-specific argument, patch, generated-data transform, install rewrite, or runtime-object semantic change. The custom-hook token therefore remains Class B evidence requiring review, but its bounded effect is standard Meson delegation only.

The decision must be re-reviewed if the recipe tree, build-script blob, delegation body, artifact identity, member digest, or SONAME changes.

## Concrete filename continuity

The selected `libxkbcommon.so.0.0.0` label is a reference concrete filename, not target-path authority. Earlier libxkbcommon 1.x source used `version: '0.0.0'`. Upstream 1.8.0 deliberately changed the concrete filename policy to `0.<minor>.<micro>`, producing `libxkbcommon.so.0.8.0`, while retaining SONAME `libxkbcommon.so.0` to avoid an unnecessary ABI-family bump.

The retained artifact contains the runtime alias:

```text
libxkbcommon.so.0 -> libxkbcommon.so.0.8.0
```

This exact alias-to-member pair satisfies the selected SONAME identity. It does not authorize creation of the older `0.0.0` filename or the unversioned development alias.

## Consumer binding

GTK 3.24.49's Wayland backend links its keymap sources with the `xkbcommon` dependency. `gdk/wayland/gdkkeys-wayland.c` directly creates and manages XKB contexts, keymaps, and states and uses XKB APIs for modifier and keysym translation. This closes the bounded library consumer binding without a device probe.

The authority covers the exact shared library API provider only. XKB configuration data, data-path policy, and complete keyboard functionality remain separate composition and target-population concerns.

## Conflict and exclusions

The retained evidence exposes one exact dynamic Termux glibc candidate with matching SONAME and a matching SONAME alias. No accepted member or alias collision exists.

This decision does not accept `libxkbcommon-x11`, `libxkbregistry`, XCB or Wayland sibling capabilities, `xkeyboard-config` data, tools, headers, pkg-config files, static libraries, unversioned development aliases, Debian/oracle bytes, package-wide authority, complete input composition, target paths, population, materialization, deployment, or activation.

## Update and rollback

Re-review the artifact version and digest, exact member and SONAME, recipe tree and custom delegation body, upstream concrete-version policy, GTK tag and direct API surface, and candidate multiplicity on change.

Before materialization, rollback is revocation of this provider and composition row. After a future materialization, reverse the selector to the prior immutable generation; do not mutate the active generation or rewrite the alias in place.

## Composition effect

```text
accepted bounded provider roots overall: 23
accepted roots inside 28-root inventory: 18
open roots inside inventory:             10
accepted exact members:                  30
included members:                        29
deferred members:                         1
unresolved selected identities:          13
composition: REVIEWED_BLOCKED_INCOMPLETE
target manifest allowed: NO
activation: BLOCKED
```
