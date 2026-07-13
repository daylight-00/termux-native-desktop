# 0141 — Selected Obsidian Non-Priority Generic Exact-Candidate Receipt Review

## Status

The bounded device receipt produced from the `0140` collector has been reviewed against exact retained apt artifact identities and the pinned `termux-pacman/glibc-packages` recipe tree.

Receipt identity:

```text
archive:
    termux-native-desktop-generic-exact-candidate-evidence-result-20260713T034510Z.tar.zst

SHA-256:
    361d2105c57c6ce3f446de16aedd966a55593fbba4e77d8a40e92b857ca02ea7

collector project HEAD:
    3b689cd7d5f1b46da61ac9b7587e434c6386b138

source checkout HEAD:
    fd2ae25e04f3ea26d6c7b4678020814889331d86

source checkout tree:
    e502a4c18ab9092ec119e3a498a0bf192ef60e6f
```

Verdict:

```text
receipt integrity and bounded collection:
    PASS

61-object review coverage:
    PASS

direct apt + pinned-recipe family candidates:
    37

indirect broad-token matches only:
    13

no retained candidate:
    11

object-to-artifact member binding:
    OPEN

semantic final provider authority:
    OPEN

ApplicationRuntimeComposition:
    NOT REACHED

target population, extraction, materialization and activation:
    BLOCKED
```

No package, recipe, artifact or object is accepted as a final provider by this review.

## Why the collector output required a second review

The collector intentionally used broad discovery tokens. That maximized recall but produced many edges where a token occurred only in a dependency, description, patch or unrelated recipe field.

For example:

```text
nss
    matched packages and recipes that merely mention NSS;
    no retained nss-glibc artifact or nss recipe family was present.

systemd
    matched dependency and compatibility references;
    no retained systemd/libsystemd direct family candidate was present.

atk / gtk / pixman / selinux
    produced indirect references that do not identify a direct provider family.
```

Therefore:

```text
search-token match
    != direct package or recipe family match

package or recipe family match
    != object member binding

object member binding
    != Termux/Android adaptation acceptance

adaptation acceptance
    != final provider authority
```

## Canonical family-name review contract

`review/generic-exact-candidate-review-rules.tsv` contains exactly 61 rows. Each row names only the package/recipe family roots that are sufficiently specific to rank a retained candidate for later comparison.

The review policy is fixed to:

```text
FAMILY_NAME_MATCH_ONLY_NOT_AUTHORITY
```

Package normalization removes only bounded packaging suffixes such as:

```text
-glibc
-glibc-static
-glibc-dev
-static
-dev
```

The reviewer does not infer family ownership from dependency text or descriptions.

Implementation:

```text
recipe/review-generic-exact-candidate-evidence.py
```

Canonical reviewed output:

```text
review/generic-exact-candidate-receipt-review.tsv
review/generic-exact-candidate-receipt-metadata.tsv
```

## Review states

```text
DIRECT_APT_AND_RECIPE_FAMILY_CANDIDATE
    exact retained apt package family and pinned recipe family both exist;
    still candidate-only.

DIRECT_APT_FAMILY_CANDIDATE
    exact retained apt package family exists without a direct pinned recipe family.

DIRECT_RECIPE_FAMILY_CANDIDATE
    exact pinned recipe family exists without a direct retained apt package family.

INDIRECT_TOKEN_ONLY
    collector found rows, but none belong to a declared direct family root.

NO_RETAINED_CANDIDATE
    retained apt and pinned recipe inputs contain no candidate row.
```

For this receipt:

```text
DIRECT_APT_AND_RECIPE_FAMILY_CANDIDATE: 37
DIRECT_APT_FAMILY_CANDIDATE:             0
DIRECT_RECIPE_FAMILY_CANDIDATE:          0
INDIRECT_TOKEN_ONLY:                    13
NO_RETAINED_CANDIDATE:                  11
```

## Direct-family candidate scope

The 37 direct-family rows include bounded candidate families such as:

```text
sqlite / libsqlite
Mesa and the Freedreno ICD family
libcairo
libcloudproviders
libdatrie
libepoxy
fontconfig
freetype
fribidi
glib
harfbuzz
libjpeg-turbo
libmount / util-linux
pango
libpng
libthai
Xcomposite, Xcursor, Xfixes, Xi and Xinerama
libxkbcommon
alsa-lib
gnutls / libgnutls
nettle / libnettle
p11-kit
libtasn1
dbus
```

This is a candidate comparison set, not a deployable provider set. Some rows retain more than one direct artifact or subpackage candidate and require exact member inventory before one artifact can be selected.

## Indirect-only and absent scope

Thirteen rows have only indirect matches. They include the NSS object family and several GTK/device/system objects whose broad tokens occurred in unrelated package or recipe metadata.

Eleven rows have no retained candidate:

```text
libnspr4.so
libplc4.so
libplds4.so
libatk-1.0.so.0
libatspi.so.0
libgdk_pixbuf-2.0.so.0
libgdk-3.so.0
libXdamage.so.1
libavahi-client.so.3
libavahi-common.so.3
libcups.so.2
```

Absence from this retained snapshot is not proof that no valid provider exists. It is evidence that the current apt index and pinned source tree cannot support an exact binding for those identities.

## Explicit non-claims

The review does not establish:

```text
that a direct-family artifact contains the requested SONAME or exact filename;
that the artifact bytes equal the Debian/rootfs oracle bytes;
that the pinned recipe built the indexed artifact;
that recipe patches provide the required Android adaptation;
that all direct-family rows are necessary together;
that indirect-only rows should be rejected globally;
that printing is required;
that any candidate may enter ApplicationRuntimeComposition;
that any target row may be populated.
```

No `.deb` was downloaded or extracted during this review.

## Validation

Repository validation now checks:

```text
61-row review-rule denominator and unique identities;
61-row reviewed-receipt denominator;
37 / 13 / 11 disposition cardinality;
receipt and output SHA-256 locks;
all rows remain OPEN_NO_DEB_EXTRACTION, UNRESOLVED and BLOCKED;
reviewer contains no package/network/source-fetch/deb-extraction operation;
synthetic direct, indirect and absent classification paths;
existing collector, generic-source, application and repository smoke regression.
```

## Ledger effect

`AUTH-009` remains:

```text
OPEN_OBJECT_SOURCE_BINDING
```

The gap is narrower:

```text
candidate discovery:
    COMPLETE FOR THE RETAINED SNAPSHOT

candidate quality review:
    COMPLETE / BOUNDED

exact object-to-artifact member binding:
    OPEN

adaptation and final provider authority:
    OPEN
```

## Next valid task

```text
DEFINE_NAMED_GENERIC_ARTIFACT_MEMBER_COMPARISON_SET
```

The next transaction may select only exact indexed artifacts belonging to the 37 direct-family rows and define a download-only/member-inventory contract. It must keep indirect-only and absent rows outside the comparison set, must not install packages, and must not populate or compose a runtime.
