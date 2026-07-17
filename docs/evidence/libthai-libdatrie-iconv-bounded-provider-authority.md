# Bounded libthai, libdatrie and libiconv authority for Pango Thai breaking

## Decision

```text
libthai.so.0.3.1:   ACCEPTED_BOUNDED_PROVIDER
libdatrie.so.1.4.0: ACCEPTED_BOUNDED_PROVIDER
libiconv.so.2.7.0:  ACCEPTED_BOUNDED_TRANSITIVE_PROVIDER
thbrk.tri:          ACCEPTED_BOUNDED_RUNTIME_DATA_CONTENT
libcharset.so.1.0.0: EXCLUDED_NOT_NEEDED_OR_MAPPED
composition:         not accepted
target population:   not accepted
activation:          not accepted
```

The signed `termux-glibc` artifacts are accepted only for Pango 1.54.0 Thai line and word breaking. The authoritative result archive is SHA-256 `7789ff1a039e3186b04014e4ddf6a7ba68d77fe31a2f1ef77273590aa97b8e1e`.

Canonical machine records:

```text
experiments/glibc/selected-obsidian-provider-authority/review/
    libthai-libdatrie-bounded-provider-authority.tsv
    libiconv-transitive-provider-authority.tsv
```

## Exact identities

| Role | Package | Exact member | Member SHA-256 | SONAME |
|---|---|---|---|---|
| selected Thai provider | `libthai-glibc 0.1.29` | `libthai.so.0.3.1` | `773a629e30546b57d650d9d991d18c64490ef5cf53062fec1e02c69ece66bf9c` | `libthai.so.0` |
| selected trie provider | `libdatrie-glibc 0.2.13` | `libdatrie.so.1.4.0` | `8052746b4003c367e811dc26686373455f687e11bf95cbbe8772a2069b86e7dd` | `libdatrie.so.1` |
| transitive conversion provider | `libiconv-glibc 1.18` | `libiconv.so.2.7.0` | `3d3edba1ecd510ddac243a3c9a5a08341219b62bc4c874241a134bc7d250f5be` | `libiconv.so.2` |
| runtime data | `libthai-glibc 0.1.29` | `share/libthai/thbrk.tri` | `d411879359c81553f3b508f7c27918f88ec2b42b8b249594af0de84e8a79dd25` | n/a |

The signed repository index matched all three artifact sizes and SHA-256 values. Exact recipe trees are `4943c66f...` for libthai, `d773dbb3...` for libdatrie and `aefe8f63...` for libiconv.

## Adaptation boundaries

`libthai` declares `BUILD_IN_SRC=true`. This selects the build directory but adds no package-specific source patch, hook, ABI change or Thai breaking algorithm change.

`libdatrie` also builds in source and adds `-liconv`. The exact ELF confirms the resulting `libiconv.so.2` dependency. No trie ABI or data-format change is introduced.

`libiconv` enables extra encodings and relocates the CLI and headers inside the Termux prefix. The accepted shared-library boundary is only `libiconv.so.2.7.0`; the executable, headers and `libcharset.so.1.0.0` are excluded. `libcharset` was neither an exact NEEDED edge nor a mapped object in the functional probe.

## Consumer, data and dependency binding

Pango 1.54.0 enables libthai when found and calls `th_brk_find_breaks()` for Thai text. The exact dependency chain is:

```text
Pango Thai break path
  -> libthai.so.0
       -> libdatrie.so.1
       -> libiconv.so.2
  -> thbrk.tri dictionary content
```

The device probe inhibited the staged objects' canonical Termux RPATH, rejected a missing dictionary, loaded the exact `thbrk.tri`, returned break positions `4`, `7` and `11`, and mapped exactly the staged libthai, libdatrie and libiconv members. Protected repository, glibc, provider and deployment state remained unchanged.

The dictionary **content** is accepted. Its future target path is not. Pango passes the default libthai dictionary selection path, so target population must later authorize either the compiled path or an explicit environment/layout policy without changing this provider decision.

## Conflict, update and rollback

There is one signed exact dynamic candidate for each accepted SONAME and no accepted member or alias collision. Re-review is mandatory if an artifact, member, SONAME, NEEDED edge, recipe tree, dictionary digest, Pango source/tag, break result or exact map changes.

Before materialization, rollback is revocation of these provider/data rows. After a future immutable materialization, rollback is selector reversal to the prior generation preserving its prior text stack.

## Prohibited inference

This decision does not accept package-wide surfaces, `libcharset`, the libiconv CLI or headers, the default dictionary target path, complete Pango/GTK composition, target population, deployment, activation or producing-build equivalence.
