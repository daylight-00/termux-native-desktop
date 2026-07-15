# libtasn1 reference-consumed provider-authority decision

## Status

```text
reviewed roots:                1
accepted bounded providers:    1
rejected providers:            0
open explicit gaps:            0
composition effect:            NONE
target population effect:      NONE
activation effect:             NONE
```

This record decides provider authority for the exact Class A root:

```text
gpkg/libtasn1
```

The decision is governed by [ADR 0005](../decisions/0005-proportional-assurance-depth.md). The canonical machine-readable result is:

```text
experiments/glibc/selected-obsidian-provider-authority/review/
    libtasn1-reference-consumed-provider-authority.tsv
```

Authority is limited to one exact Termux glibc artifact, one exact regular ELF member, its observed `DT_SONAME`, and the exact external-libTASN1 capability selected by the bounded GnuTLS 3.8.9 security consumer.

## Exact provider and consumer

### Provider

```text
artifact:  libtasn1-glibc 4.20.0
artifact SHA-256:
           51ed5e4d2e3fcd5ed96630635edf75ed6f50ecd4bafdcbed478bbd3822f6864b
member:    libtasn1.so.6.6.4
member SHA-256:
           a66b335b8311c8006067a4b1df490a3ed4fbd68e9d9dd71eedc79e3c46838c0f
SONAME:    libtasn1.so.6
recipe:    gpkg/libtasn1
recipe tree:
           3601f2ed3c9fd4d03c20c0d854d7b3aa05628482
```

### Bounded consumer

```text
artifact:  libgnutls-glibc 3.8.9
artifact SHA-256:
           e072748f2ddba21f0193604132d578c406267931692c0291f1a87da1899980da
member:    libgnutls.so.30.40.3
member SHA-256:
           53fb8f500bbc0c3e900fc26701ef58641ad018993682dba3fff76525e7923244
SONAME:    libgnutls.so.30
recipe:    gpkg/libgnutls
recipe tree:
           8851cd93d2e7c823b86e3940d7b61fd1965594e6
```

The consumer itself remains a separate open adaptation and provider-authority claim. It is named here only to bound the accepted libtasn1 capability.

## Capability necessity

GnuTLS 3.8.9 defines `LIBTASN1_MINIMUM=4.9`. Its configuration selects the system libtasn1 by default and permits the included `minitasn1` fallback only through the explicit `--with-included-libtasn1` mode.

The pinned Termux `gpkg/libgnutls` recipe:

```text
depends on libtasn1-glibc
does not pass --with-included-libtasn1
```

Therefore the selected external GnuTLS build contract requires a compatible `libtasn1` provider. This is a semantic requirement for the GnuTLS ASN.1, X.509, PKCS and related TLS/security implementation, not package-presence inference.

Authoritative contract locators:

```text
termux-pacman/glibc-packages@9bdd20c1d36524a0ab016d9b71c748b0cbb20a34
    gpkg/libgnutls/build.sh

gnutls/gnutls@3.8.9
    m4/hooks.m4
    lib/Makefile.am
```

`m4/hooks.m4` requires external libtasn1 when the included fallback is not selected. `lib/Makefile.am` adds `$(LIBTASN1_LIBS)` to `libgnutls` in that mode.

## Consumer-binding result

The binding is accepted without a new device observation because the following independent coordinates agree:

1. exact GnuTLS 3.8.9 upstream configuration and link contract;
2. exact pinned Termux GnuTLS recipe dependency and absence of the included-fallback option;
3. exact Termux GnuTLS and libtasn1 artifact/member/SONAME identities;
4. the existing selected security/printing closure containing `libgnutls.so.30` and `libtasn1.so.6`.

A future binary `DT_NEEDED` re-observation is an escalation action if any exact artifact, recipe, included/external mode, SONAME, or consumer-binding coordinate changes. It is not required to re-prosecute the unchanged reference contract in this review.

## Conflict and exclusion result

```text
one exact dynamic Termux glibc libtasn1 candidate
libtasn1-glibc-static excluded from dynamic provider authority
Debian-rootfs libtasn1 bytes retained as oracle/reference only
GnuTLS included minitasn1 fallback not selected
no concrete-filename drift
observed SONAME equals required lookup name
```

The Debian oracle build has the same ABI-family role but different distribution bytes and is not selected as target authority. The project is constructing a coherent Termux glibc provider generation.

## Decision

```text
decision:
    ACCEPTED_BOUNDED_PROVIDER

scope:
    exact libtasn1.so.6.6.4 member
    observed SONAME libtasn1.so.6
    selected external GnuTLS 3.8.9 ASN.1/security capability

remaining provider gap:
    NONE_FOR_BOUNDED_PROVIDER_AUTHORITY
```

This decision does not accept the GnuTLS recipe adaptation or GnuTLS provider authority. It also does not claim complete security composition.

## Update and rollback boundary

Re-review is mandatory if any of the following changes:

```text
libtasn1 artifact version or SHA-256
libtasn1 member SHA-256 or SONAME
libtasn1 recipe tree
GnuTLS artifact/member identity
GnuTLS recipe tree or external-versus-included libtasn1 mode
consumer-binding contract
dynamic candidate or conflict set
```

This transaction performs no runtime mutation. Before materialization, rollback is revocation of this row. A future materializer must place the provider only in a new immutable generation. Runtime rollback must reverse the selector to the previous immutable generation and preserve the previously accepted GnuTLS/libtasn1 security pair.

## Explicitly prohibited inference

This decision does not establish:

```text
GnuTLS adaptation acceptance
GnuTLS provider authority
complete TLS/security composition
complete application runtime composition
target membership or target paths
materialization readiness
selected-generation activation readiness
```

`libepoxy`, Pango drift/provider authority, and all explicit-delta roots remain separate decisions.
