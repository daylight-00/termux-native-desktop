# GDK Pixbuf reference dependency provider authority

## Decision

The exact Termux reference artifacts collected for GLib `2.82.2-2` and libpng `1.6.47` are accepted as bounded providers for the already accepted project-built GDK Pixbuf `2.42.12` fixed JPEG/PNG file and memory decode scope.

```text
GLib four-member family: ACCEPTED_BOUNDED_PROVIDER
libpng shared member:    ACCEPTED_BOUNDED_PROVIDER
libmount official pair: OPEN_EXACT_RUNTIME_BINDING_REQUIRED
libblkid official pair: OPEN_EXACT_RUNTIME_BINDING_REQUIRED
```

This is a provider review, not target population or activation.

## GLib family

Accepted exact members:

| Member | SHA-256 | SONAME |
|---|---|---|
| `libglib-2.0.so.0.8200.2` | `e0504b50e14870623e10490d76b78c7a8d0037a54fe354429e2e3b5ac07ae0d5` | `libglib-2.0.so.0` |
| `libgobject-2.0.so.0.8200.2` | `de13928664709a9cecd61f50dcc4d2294d0c2ff91f147d0827d209cd03af45a6` | `libgobject-2.0.so.0` |
| `libgmodule-2.0.so.0.8200.2` | `feaad9c286e9a1af3cff94a78924f543bc0f4d7f8dfc05c9ec13eb1c3d8764bf` | `libgmodule-2.0.so.0` |
| `libgio-2.0.so.0.8200.2` | `aa9fa8876fac7334570273064be05c3e65ba0f16d30a77a5929f48b12bfe64b3` | `libgio-2.0.so.0` |

The pinned recipe is Class B. Its patches redirect machine ID, settings, resolver, XDG, locale, spawn shell/PATH, temporary directory, OS-release and data paths into the Termux prefixes and disable the pidfd feature probe. Configure and package hooks change runtime directory, debug/documentation/introspection/man-page selection and package lifecycle behavior. These changes are bounded Android/Termux integration adaptations; they do not change the four accepted SONAMEs.

The accepted GDK Pixbuf result maps all four exact members and passes JPEG file, JPEG memory, PNG file and PNG memory cells. Concrete Debian `2.84.4` suffixes are oracle labels only and are not target filenames.

Excluded GLib surfaces include `libgirepository`, `libgthread`, executables, static libraries, development aliases and broader GIO service behavior.

## libpng

Accepted exact member:

| Member | SHA-256 | SONAME |
|---|---|---|
| `libpng16.so.16.47.0` | `00c9fd06c139699552c086b60d116a01d067ceddddb29c56600bf9fd3bae746f` | `libpng16.so.16` |

The package recipe uses the pinned upstream `1.6.47` shared-library build. Its package-specific post-install step builds `png2pnm` and `pnm2png`; those utilities and the unversioned development alias are excluded. The exact shared member is mapped in the accepted GDK Pixbuf result and both PNG cells pass. The Debian `1.6.48` concrete suffix is not a target path requirement.

## Transitive util-linux boundary

`libgio-2.0.so.0.8200.2` directly needs `libmount.so.1`, and libmount needs `libblkid.so.1`. The successful scratch build mapped scratch util-linux bytes, not the official exact package candidates already recorded by the repository.

| Dependency | Official exact member SHA-256 | Scratch mapped SHA-256 | Decision |
|---|---|---|---|
| `libmount.so.1.1.0` | `6864b9050ddd5884642c98ea4df07e3ceaf78727324d6e9068d1866594ece1c2` | `951a7e682476045acaa598eb05e2b79adc5f800b6fc34133eac49f797b064b40` | open |
| `libblkid.so.1.1.0` | `21d47963d42a5b1c4008c88a311c17142f57ee2f19cd30770f0befa364908fb3` | `bd63dcc600487615ee6256b9cfe4d474ebc76899c911f8134d66765810e7db51` | open |

The differing digests prohibit inferring official provider authority from the successful scratch run. The next minimum action is a read-only Termux acquisition/analyzer transaction that verifies the official pair, reviews the pinned util-linux adaptation boundary, reruns the fixed GDK Pixbuf matrix and proves exact `/proc/self/maps` binding.

## Authority effect

After this decision:

```text
accepted provider roots overall: 11
accepted root claims in the 28-root inventory: 10
accepted exact members: 16
included selected members: 15
deferred members: 1
unresolved selected identities: 21
composition: REVIEWED_BLOCKED_INCOMPLETE
target manifest allowed: NO
activation: BLOCKED
```

No provider bytes are installed or copied by this review.

## Canonical data

- [`gdkpixbuf-reference-dependency-provider-authority.tsv`](../../experiments/glibc/selected-obsidian-provider-authority/review/gdkpixbuf-reference-dependency-provider-authority.tsv)
- [`gdkpixbuf-util-linux-transitive-provider-disposition.tsv`](../../experiments/glibc/selected-obsidian-provider-authority/review/gdkpixbuf-util-linux-transitive-provider-disposition.tsv)
