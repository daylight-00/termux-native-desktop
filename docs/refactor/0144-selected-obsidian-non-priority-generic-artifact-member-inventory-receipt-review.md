# 0144 — Selected Obsidian non-priority generic artifact member-inventory receipt review

## Status

```text
PASS / BOUNDED RECEIPT REVIEW
FINAL PROVIDER AUTHORITY OPEN
TARGET POPULATION BLOCKED
```

This record reviews the device receipt produced by the bounded collector defined in `0143`. It does not widen the collector boundary and does not accept any artifact, recipe, package or object as a final provider.

## Source receipt

```text
archive:
    termux-native-desktop-generic-artifact-member-inventory-recovery-result-20260713T054649Z.tar.zst

archive SHA-256:
    e42db95f816700d1cf80cae7b747e876f831924c5f3df7f416c22243b0e83274

source repository HEAD:
    69f6fb137cc43e42135dbc655a8e172e5a0ac7d4

source repository tree:
    4ae2bf1359eb8b5673686d53f7c17e7e92a0d38f
```

Receipt integrity and bounded execution:

```text
exact artifacts planned and verified:
    34 / 34

verified compressed bytes:
    51,771,348

named identity-to-artifact edges:
    44

review identities:
    37

package transaction:
    NO

maintainer-script execution:
    NO

filesystem payload extraction:
    NO

dpkg status and retained apt-list mutation:
    NONE

authority decisions accepted:
    0

target rows populated:
    0
```

## Canonical review products

```text
review/generic-artifact-member-inventory-review-rules.tsv
review/generic-artifact-member-inventory-receipt-review.tsv
review/generic-artifact-member-inventory-receipt-metadata.tsv
recipe/review-generic-artifact-member-inventory.py
tests/repository/generic-artifact-member-inventory-receipt-review-smoke.sh
```

The rules explicitly state the expected SONAME alias for each of the 37 direct-family identities. The reviewer consumes the 44-edge named observation receipt and the data-member inventory, but it never executes an artifact or installs/extracts payloads.

## Review classes

### Exact concrete member and expected ELF SONAME observed — 21

The receipt contains one exact concrete basename, a regular member SHA-256, and a parsed ELF `DT_SONAME` equal to the expected alias.

```text
libVkLayer_MESA_device_select.so
libasound.so.2.0.0
libepoxy.so.0.0.0
libvulkan_freedreno.so
libnettle.so.8.10
libXinerama.so.1.0.0
libXcomposite.so.1.0.0
libdatrie.so.1.4.0
libfribidi.so.0.4.0
libfreetype.so.6.20.2
libhogweed.so.6.10
libXfixes.so.3.1.0
libgnutls.so.30.40.3
libtasn1.so.6.6.4
libgbm.so.1.0.0
libXi.so.6.1.0
libcloudproviders.so.0.3.6
libXcursor.so.1.0.2
libp11-kit.so.0.4.1
libthai.so.0.3.1
libmount.so.1.1.0
```

Review state:

```text
EXACT_CONCRETE_MEMBER_AND_EXPECTED_SONAME_OBSERVED
```

This is strong candidate object/member evidence. It is not artifact-to-recipe binding, Android adaptation acceptance, necessity, final provider authority or composition acceptance.

### Expected SONAME alias symlink present; concrete filename drift — 15

The exact first-generation concrete filename is absent, but the artifact contains the expected SONAME-named symlink and a unique regular target with a different concrete filename.

```text
libxkbcommon.so.0.0.0
    libxkbcommon.so.0 -> libxkbcommon.so.0.8.0

libgobject-2.0.so.0.8400.4
    libgobject-2.0.so.0 -> libgobject-2.0.so.0.8200.2

libpango-1.0.so.0.5600.3
    libpango-1.0.so.0 -> libpango-1.0.so.0.5400.0

libfontconfig.so.1.12.1
    libfontconfig.so.1 -> libfontconfig.so.1.14.0

libpng16.so.16.48.0
    libpng16.so.16 -> libpng16.so.16.47.0

libdbus-1.so.3.38.3
    libdbus-1.so.3 -> libdbus-1.so.3.37.0

libcairo.so.2.11804.4
    libcairo.so.2 -> libcairo.so.2.11802.2

libgio-2.0.so.0.8400.4
    libgio-2.0.so.0 -> libgio-2.0.so.0.8200.2

libgmodule-2.0.so.0.8400.4
    libgmodule-2.0.so.0 -> libgmodule-2.0.so.0.8200.2

libsqlite3.so.0.8.6
    libsqlite3.so.0 -> libsqlite3.so.3.49.1

libpangoft2-1.0.so.0.5600.3
    libpangoft2-1.0.so.0 -> libpangoft2-1.0.so.0.5400.0

libharfbuzz.so.0.61020.0
    libharfbuzz.so.0 -> libharfbuzz.so.0.61010.0

libpangocairo-1.0.so.0.5600.3
    libpangocairo-1.0.so.0 -> libpangocairo-1.0.so.0.5400.0

libglib-2.0.so.0.8400.4
    libglib-2.0.so.0 -> libglib-2.0.so.0.8200.2

libcairo-gobject.so.2.11804.4
    libcairo-gobject.so.2 -> libcairo-gobject.so.2.11802.2
```

Review state:

```text
EXPECTED_SONAME_ALIAS_SYMLINK_PRESENT_CONCRETE_FILENAME_DRIFT
```

The collector parsed ELF metadata only for exact named regular members. Therefore, the symlink target's ELF SONAME and regular-member SHA-256 are not yet accepted by this review.

The `libsqlite3.so.0` alias is present. The concrete target name `libsqlite3.so.3.49.1` alone is not sufficient to classify an ABI-major mismatch. A bounded target-ELF review is required before making that claim.

### Expected SONAME alias absent — 1

```text
expected identity:
    libjpeg.so.62.3.0

expected SONAME alias:
    libjpeg.so.62

observed family members:
    libjpeg.so
    libjpeg.so.8
    libjpeg.so.8.3.2
```

Review state:

```text
EXPECTED_SONAME_ALIAS_NOT_OBSERVED_DIFFERENT_FAMILY_MEMBERS_PRESENT
```

The current `libjpeg-turbo-glibc` artifact is not evidence for the expected `libjpeg.so.62` object. This row requires source correction or an alternative exact artifact candidate; it is not eligible for provider acceptance from this receipt.

## Claim boundary

```text
exact artifact identity
    != artifact-to-recipe build binding

exact concrete member and expected ELF SONAME observation
    != Termux/Android adaptation acceptance

expected SONAME alias symlink
    != verified ELF SONAME of the symlink target

filename drift
    != automatic compatibility or incompatibility

candidate object/member evidence
    != necessity, final provider authority or runtime composition
```

All 37 rows remain:

```text
artifact-to-recipe binding:
    OPEN

Termux/Android adaptation:
    OPEN

final provider:
    UNRESOLVED

target population:
    BLOCKED
```

## Next bounded work

```text
DEFINE_BOUNDED_GENERIC_RECIPE_BINDING_AND_DRIFT_TARGET_ELF_REVIEW
```

Required order:

1. For the 21 exact rows, seek repository/build evidence that binds each exact artifact to its pinned recipe source and records adaptation deltas.
2. For the 15 alias-drift rows, extend read-only inspection only enough to hash and parse the unique regular symlink target from the already verified artifact cache; do not extract to a filesystem tree.
3. For `libjpeg.so.62`, search for a correct exact candidate rather than treating the observed `.so.8` family as compatible.
4. Keep the 13 indirect-only and 11 retained-gap rows outside this 37-row receipt review.
5. Do not accept coherent capability sets, final providers, composition or target population until recipe binding and adaptation review close.

## Stop line

Do not:

```text
treat 21 exact observations as final provider acceptance;
treat a SONAME alias symlink as proof of its target ELF SONAME;
classify sqlite ABI compatibility from the concrete target filename alone;
treat libjpeg.so.8 as a substitute for libjpeg.so.62;
install packages or execute maintainer scripts;
extract payloads into a filesystem tree;
populate target paths, aliases, modes or owners;
write or run a materializer;
modify generation/current, launcher, loader state or RPATH.
```
