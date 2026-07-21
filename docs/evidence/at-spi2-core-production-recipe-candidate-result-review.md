# AT-SPI2 core 2.56.2 production recipe candidate result review

## Decision

```text
atomic recipe candidate:       QUALIFIED_CLASS_B
local package/member family:   QUALIFIED_CLASS_C
provider authority here:       OPEN_BOUNDED_PROVIDER_AUTHORITY_REVIEW_REQUIRED
composition effect here:       NONE; THREE CANDIDATE-OPEN GAPS RETAINED
target/service activation:     BLOCKED
```

This review accepts the bounded producing record whose result archive has SHA-256 `461b24dac879ca71252c209f0013ff17cb8f8ed1a889a32f0376b87372f3d3a4` and whose separately frozen candidate-evidence archive has SHA-256 `b516ed70c10b6bf91fac08e2a461dc55e9f2b5337a4dade5b995e96fa5b4b40d`. The run did not install the package, mutate the package database, change the live glibc prefix or repository, populate a provider target, start D-Bus or accessibility services, deploy, or activate anything.

## Production recipe candidate

```text
base repository:       termux-pacman/glibc-packages
base HEAD:             9bdd20c1d36524a0ab016d9b71c748b0cbb20a34
base tree:             2d7f6903db6b3be40618b19414e455198978747b
candidate tree:        0f6e255985e5967fe793b8ee3e86f248a430513f
recipe path:           gpkg/at-spi2-core/build.sh
recipe SHA-256:        6f727204730b6b0a3496c169f635c5016903cb64b816b7c84ca91fcbc9d4e30d
contribution SHA-256:  26f6741fbb081c64bffb53d0a467564845df5ef5a0983b09f00e2e924bba6c50
claim class:           B, reference-adapted recipe semantics
```

The recipe pins official AT-SPI2 core 2.56.2 source SHA-256 `e1b1c9836a8947852f7440c32e23179234c76bd98cd9cc4001f376405f8b783b`, enables the selected X11/GIR surface, preserves all three selected SONAME families atomically, adds the exact `gcc-libs-glibc` runtime dependency implied by the pinned GNU `-fexceptions` policy, and relocates seven activation metadata files out of active lookup namespaces. Private dependency overlays, PRoot isolation, host-tool shims, GPG socket aliasing, venv/Meson shebang repairs, and evidence collection remain outside the contribution recipe.

## Exact reproduced package and member family

```text
package:          at-spi2-core-glibc 2.56.2 aarch64
package SHA-256:  9a1395e893448508cfb8fbdee8ef0dd8268b8d21e9ac7bbe792f163dce6c365a
files/symlinks:   88 / 7

libatk-1.0.so.0.25611.1
  SHA-256: 55c9c8a3767258bcc1d25640223aa8638ca0fc1bf5a310c7c87de14ad66191d7
  SONAME:   libatk-1.0.so.0

libatk-bridge-2.0.so.0.0.0
  SHA-256: cce78fd50cb5b3a19bdc046112c75a2309ad5feda3183e62f538bc1177e72773
  SONAME:   libatk-bridge-2.0.so.0

libatspi.so.0.0.1
  SHA-256: e94f2980cf8580634d7ab3c4f9ad2d8713880a1e3614001aed7a63ba6388c874
  SONAME:   libatspi.so.0

claim class: C, independently reproduced local bytes
```

All three members are AArch64, have exact bounded `DT_NEEDED` sets, and have no `DT_RPATH` or `DT_RUNPATH`. ATK and the bridge match the strict reference ABI. `libatspi.so.0` additionally binds only `libgcc_s.so.1` and the exact `_Unwind_Resume@GCC_3.0` and `__gcc_personality_v0@GCC_3.3.1` symbols required by the pinned GNU framework `-fexceptions` policy. The runtime provider is pinned to `gcc-libs-glibc 14.2.1-1`, package SHA-256 `919c2e80a629d674dd450b0a0edd11378284f1ed9d2a8fd3c9c91d7ac72f041f`, and `libgcc_s.so.1` payload SHA-256 `22d5db25fece632754f7a0fb1c6586eb6e93eab6a5866da487b86f115d4e389d`.

## GIR and service boundary

The package contains byte-exact qualified introspection artifacts:

```text
Atk-1.0.gir       a15e67a1f42f4720d0b1920cf0739cc0a73d94ae04bcc69d580fa51bc4b4d6d3
Atk-1.0.typelib   0454707e83528cc498020f85f77761b6c8b365c592988dd3c60b00f1f15c7fc7
Atspi-2.0.gir     f97c8d5b3ef16cb9489d1ff57f418887abae759c5903bde15510355d10874caf
Atspi-2.0.typelib 125a679a0123b025562346dcbfa9fdc0ed3208aeee388db2c26cab8a25c6069d
```

Exactly seven D-Bus, autostart, systemd, Xwayland, defaults, and GTK-module activation metadata files are retained under `share/termux-native-desktop/disabled/at-spi2-core/`; none remains in an active lookup path. The two helper executables are present but were not executed. The Debian control archive contains no maintainer scripts or triggers.

## Protected-state result

Pre/post package-database queries and status digest, live glibc regular-file and symlink surfaces, repository HEAD/tree, and repository cleanliness were identical. Controlled loader escape count and probe failures were zero.

## Disposition

The historical `OPEN_BLOCKED_NO_GLIBC_CANDIDATE` result remains valid discovery evidence for the earlier pinned package/repository boundary, but is superseded as the current candidate state. An exact atomic Class B recipe and exact Class C package/member family now exist.

This record does **not** grant provider authority. The next task is a separate bounded review of exact capability necessity, three-member atomicity, consumer binding, dependency closure, collision/exclusion state, service lifecycle, update, and rollback. The six selected composition gaps remain unresolved; the three AT-SPI2/ATK rows change only from no-candidate blockers to qualified-local-candidate/provider-authority-open rows.

## Explicitly prohibited inference

This review does not authorize approved-supplier publication, package installation, package-wide provider authority, D-Bus bus ownership, registry-daemon operation, accessibility enablement, active metadata restoration, target population, alias creation in a target, deployment, or activation.
