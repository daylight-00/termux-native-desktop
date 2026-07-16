# GDK Pixbuf exact util-linux provider authority

The official Termux `libmount-glibc` and `libblkid-glibc` pair is accepted only as the exact transitive runtime required by the already accepted GDK Pixbuf 2.42.12 fixed JPEG/PNG file and memory decode scope.

```text
result archive SHA-256: a18426371acf0339731464eea4a6fd1f8c745cc09154629b69e34d1063073c13
recipe tree:              e91a0c476ef4355dbfff46e2bcab23d0085ddd01
decision:                 ACCEPTED_BOUNDED_PROVIDER
```

| Package | Artifact SHA-256 | Exact member | Member SHA-256 | SONAME |
|---|---|---|---|---|
| `libmount-glibc 2.40.2-1` | `9004e88a9f43b2d5cf74fd8921e4b74146e3ced64c4f94490cc52d9b138b011a` | `libmount.so.1.1.0` | `6864b9050ddd5884642c98ea4df07e3ceaf78727324d6e9068d1866594ece1c2` | `libmount.so.1` |
| `libblkid-glibc 2.40.2-1` | `b6692956495dfd59ce70a854db5af86bae5f63791440e2cc5f21c26194b965fe` | `libblkid.so.1.1.0` | `21d47963d42a5b1c4008c88a311c17142f57ee2f19cd30770f0befa364908fb3` | `libblkid.so.1` |

The signed `termux-glibc` index selected both artifacts. `libmount` needs `libblkid.so.1`; both exact members have no RPATH or RUNPATH. The exact nine-object runtime map included GDK Pixbuf, four GLib members, libmount, libblkid, libpng and libjpeg, and all four JPEG/PNG file/memory cells passed.

The same-version `libblkid` package container showed metadata drift during acquisition history, while the exact runtime member digest remained identical to prior evidence. Runtime member identity, not stale package-container metadata, is the bounded provider coordinate.

The pinned recipe is Class B: it redirects filesystem and device paths into Termux/Android coordinates, selects a bounded Meson feature set, and splits libmount/libblkid into subpackages. This review accepts only the two shared members and their SONAME aliases. All other util-linux libraries, tools, executables, headers, static objects and development surfaces are excluded.

## Authority effect

```text
accepted bounded provider roots overall: 12
accepted root claims inside the 28-root inventory: 11
accepted exact members: 18
included composition members: 17
deferred members: 1
unresolved selected identities: 20
composition: REVIEWED_BLOCKED_INCOMPLETE
target manifest allowed: NO
activation: BLOCKED
```

Provider acceptance does not imply complete composition, target membership, materialization, deployment or activation.
