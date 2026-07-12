# 0128 — Selected Obsidian Provider-Authority Source Recipe Receipt PASS

## Status

```text
source-recipe evidence transaction:
    PASS / ACCEPTED

binary artifact acquisition:
    AUTHORIZED FOR BOUNDED PRIORITY SET ONLY

provider authority decisions:
    NOT ACCEPTED

successor composition/materialization/current activation:
    BLOCKED
```

The accepted receipt is:

```text
archive:
    selected-obsidian-provider-authority-n3-source-recipe-evidence-results-20260712-185001.tgz

SHA-256:
    c8160016267f3ff83b348146240f74f808ffbc93374a6f75988231ef22408cdb

captured branch:
    docs/post-graphics-architecture-audit

captured HEAD:
    5c11ec95f6e6529bbf03459a0515a88b5c685d18

analysis.status:
    PASS

next-state:
    READY_FOR_BOUNDED_BINARY_ARTIFACT_ACQUISITION_AND_RECIPE_REVIEW
```

## Archive integrity

Independent pre-extraction review established:

```text
members:
    183

regular files:
    151

directories:
    32

archive roots:
    1

absolute paths:
    0

parent traversal paths:
    0

symlinks, hardlinks, devices, FIFOs, sockets:
    0
```

The submitted SHA-256 matched independently.

## Preserved N3 input

All embedded corrected-N3 and APT-source inputs matched their recorded SHA-256 values.

The source receipt retained:

```text
corrected N3 HEAD:
    2d76d5b5253d10c415191b43f1427b64978695fb

installed package identities:
    86

selected-related packages:
    26

priority source/binary comparison packages:
    28

authority decisions accepted:
    0
```

## Source repository identity

The source input and isolated normalized checkout resolved to:

```text
repository:
    https://github.com/termux-pacman/glibc-packages.git

HEAD:
    fd2ae25e04f3ea26d6c7b4678020814889331d86

tree:
    e502a4c18ab9092ec119e3a498a0bf192ef60e6f

branch:
    main

shallow:
    false

worktree:
    CLEAN

fsck:
    PASS
```

Android shared-storage handling remained bounded:

```text
origin mode:
    ISOLATED_SHARED_STORAGE_SAFE_DIRECTORY_BUNDLE_CLONE

safe.directory scope:
    COMMAND_ONLY

transfer mode:
    LOCAL_GIT_BUNDLE_ALL_REFS

input Git configuration mutation:
    NO

input metadata mutation:
    NO

network source fetch:
    NO
```

The input HEAD and refs SHA-256 were unchanged before and after collection.

## Installed-state guard

The accepted package-state fingerprints remained exact and unchanged:

```text
dpkg status SHA-256:
    aba4d9e78f68bd0fe5d841b5d1422255ecca162621c85630137651122bcc8ee2

dpkg info metadata manifest:
    f1a32ecdf5cbe1999fbf4b2aeae28196e8a1ca215b17a4e2f4153578dce414e4
```

The transaction performed no package operation, package download, runtime launch, generation operation, `current` operation, or source fetch.

## Recipe-history result

For the 28 priority packages:

```text
package-to-recipe mappings found:
    28 / 28

installed versions found in recipe history:
    28 / 28

unique matching recipe tree:
    27

multiple matching recipe trees:
    1

recipe mapping/version not found:
    0

candidate commits:
    29

embedded recipe-file manifest rows:
    121
```

The embedded source material includes build recipes, subpackage recipes, patches, and auxiliary files. This is source evidence, not provider approval.

## Exact repository artifact metadata

The locally present APT state was read without `apt update`:

```text
APT source files:
    4

APT index files:
    10

Packages indexes:
    6 / PARSED

Release or InRelease records:
    4 / PARSED_FIELDS

parsed package records:
    4,914

installed packages with exact indexed version, filename, size, and SHA-256:
    86 / 86

cached .deb artifacts:
    0
```

All 86 exact records came from the configured Termux glibc repository index. An index record remains repository metadata until the referenced artifact bytes are independently acquired and verified.

## Important source findings

### glibc

```text
installed package:
    glibc 2.42 / hold ok installed

current source recipe:
    glibc 2.43

installed-version matching recipe trees:
    1

indexed 2.42 artifact SHA-256:
    59e47a50b77ba9c0c1cc7cd0dafbb1558528cb544a740858faad0263e8b9b27f
```

The current source HEAD is therefore not the installed glibc recipe version. Historical matching is required and was preserved.

### Termux/Android integration recipes

The receipt embeds explicit adaptation evidence for, among others:

```text
glibc Android/Termux patches and auxiliary syscall/shmem/path sources
termux-exec-glibc build recipe and termux-exec patch
glibc-runner scripts and shell environment
libxcb patch inputs
gcc-libs dynamic-linker and toolchain patches
util-linux/libblkid subpackage boundary
```

These files demonstrate candidate adaptation mechanisms. They do not by themselves prove minimum runtime membership or final authority.

### libwayland ambiguity

`libwayland-glibc 1.23.1` has two matching historical recipe trees:

```text
newer tree:
    fb5924ca0b3f42a87d0d865e11a8aa9f6163e5a2

older tree:
    d0c7dcd812e720f00a781c0410af150fbfffdae0
```

The build recipe, source URL, source SHA-256, `setdirs.patch`, and scanner-for-build patch are identical.

The older tree additionally contains:

```text
force-libm.patch
```

That patch links `wayland-scanner` with `libm`. The exact binary artifact may provide a semantic discriminator through its ELF `DT_NEEDED` set, but binary behavior alone is not complete build-provenance proof.

## Acceptance judgment

This receipt is accepted as evidence that:

```text
the corrected N3 priority set maps completely to source recipes;
historical installed-version recipe candidates are bounded;
exact current repository artifact identities are available for all installed packages;
Termux/Android-specific patch and auxiliary inputs are preserved for review;
the source and live package state remained unchanged.
```

It does not establish:

```text
which historical candidate tree built each installed artifact;
that an indexed artifact is byte-identical to installed files;
that current repository HEAD is final authority;
that package ownership equals semantic provider authority;
that glibc-runner or toolchain packages belong in the runtime profile;
that a successor may be materialized or activated.
```

## Next authorized transaction

The next transaction is limited to the 28 priority packages already present in the source comparison ledger.

```text
artifacts:
    28

indexed compressed bytes:
    42,864,296

operation:
    HTTPS download of exact indexed .deb files
    -> size/SHA-256/control identity verification
    -> non-executing control/data tar inventory
    -> live installed byte and symlink comparison
    -> ELF metadata capture

apt update:
    forbidden

package install/upgrade/remove:
    forbidden

maintainer-script execution:
    forbidden
```

The raw artifacts may be retained under `$HOME/Downloads` as evidence cache. Receipt archives remain metadata/manifests only unless separately authorized.

## Stop line

Do not:

```text
download packages outside the exact 28-row plan;
accept a redirect outside the approved Termux glibc artifact hosts;
use apt update, apt install, apt upgrade, apt remove, or dpkg installation;
execute preinst, postinst, prerm, postrm, triggers, or package payloads;
treat byte equality as semantic authority by itself;
mutate loader state, the selected generation, current, or promoted launchers;
start successor composition or activation.
```
