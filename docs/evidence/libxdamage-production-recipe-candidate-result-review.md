# libXdamage production recipe candidate result review

## Decision

```text
recipe candidate:       QUALIFIED_CLASS_B
local package/member:   QUALIFIED_CLASS_C
provider authority here: OPEN_REVIEW_REQUIRED AT QUALIFICATION TIME
subsequent disposition: ACCEPTED_BOUNDED_PROVIDER by LIBXDAMAGE-PROV-001
composition effect here: NONE AT QUALIFICATION TIME
target/activation:      BLOCKED
```

This review records the bounded Termux run whose result archive has SHA-256 `462b613a0d6a2c2e2eefdff6742fd16014311f87606916ab0982220998612f6c` and the separately frozen candidate-evidence archive SHA-256 `f1ee7e091d29783de294d7bd44116e8f13413bbf4ef7a0045ef0307927f8b126`. The run did not install a package, mutate the package database, change the live glibc prefix, populate a target, deploy or activate anything.

## Production recipe candidate

```text
base repository:       termux-pacman/glibc-packages
base HEAD:             9bdd20c1d36524a0ab016d9b71c748b0cbb20a34
candidate tree:        46fe3064b0537aa7b4327d3cefc6891fa3b2cba5
recipe path:           gpkg/libxdamage/build.sh
recipe SHA-256:        40ed4b7d663d01efd3c61d961094ff63659be67917d977f0543d2449411eb0e1
contribution SHA-256:  eee51ab2293bd63848a0ae9418dc7c0e402a107a9ee2e9eec48573134079b20f
contribution surface:  one new 11-line metadata recipe
claim class:           B, reference-adapted recipe semantics
```

The recipe contains only upstream source, license, version, digest and glibc dependency coordinates. The exact dependency overlay, scoped PRoot installation isolation, `CONFIG_SHELL` selection and restricted host-tool shims belong to the private evidence harness and are absent from the contribution patch.

## Exact reproduced artifact

```text
package:          libxdamage-glibc 1.1.6 aarch64
package SHA-256:  09062711dd28f7268f3d7f75c85b3b42a55d3e6d70d1644a9853ee0b4c0e7890
member:           libXdamage.so.1.1.0
member SHA-256:   391916aff0965656e7b81ece7766e3b22068462867b1dd88a0a051b3db9c2d7c
SONAME:           libXdamage.so.1
machine:          AArch64
DT_RPATH:         absent
DT_RUNPATH:       absent
DT_NEEDED:        libXfixes.so.3;libX11.so.6;libc.so.6;ld-linux-aarch64.so.1
claim class:      C, independently reproduced local bytes
```

The exact package and member hashes were reproduced after production-recipe/harness separation. The controlled loader reported zero live-prefix escapes, the symbol probe returned zero, and GTK 3.24.49 GDK X11 source binding was retained.

## Dependency and protected-state result

The accepted exact `libxfixes-glibc` package and member remained unchanged:

```text
package SHA-256: 23fe7f6003d9607db6af5c31b995616270c319f2af11ddcd6292facd43b25b66
member SHA-256:  271e82cbc4aa3db8ff36ad44735552153b6fbaa787bf59b6ec0b20f63d0f386d
```

Pre/post package-database state, live glibc regular-file surface and live glibc symlink surface were identical. Canonical prefix strings were retained while physical install writes were redirected only inside the bounded build subprocess.

## Disposition

The historical `OPEN_BLOCKED_NO_GLIBC_CANDIDATE` discovery result is superseded as the current libXdamage production state: an exact Class B recipe candidate and exact Class C package/member candidate now exist. It remains valid historical evidence that no approved supplier package or recipe root existed at the earlier pinned discovery boundary.

Provider authority was not granted by this qualification record. The subsequent canonical decision `LIBXDAMAGE-PROV-001`, documented in `libxdamage-bounded-provider-authority.md`, accepts the exact local Class C member only for the bounded GTK 3.24.49 GDK X11 damage-extension capability. The producing record remains Class C and approved-repository publication remains unaccepted.

## Explicitly prohibited inference

This qualification review alone does not accept the candidate as a provider. The later bounded provider decision does not authorize upstream submission or supplier publication, installation, target paths, alias creation in a target, generation population, deployment or activation.
