# Bounded libXdamage provider authority for GTK 3.24.49 GDK X11

## Decision

```text
recipe candidate:     qualified Class B
producing record:     retained Class C
provider decision:    ACCEPTED_BOUNDED_PROVIDER
accepted member:      libXdamage.so.1.1.0
accepted SONAME:      libXdamage.so.1
accepted capability:  GTK 3.24.49 GDK X11 damage-extension linkage and damage-region support
composition:          not accepted
supplier publication: not accepted
target population:    not accepted
activation:           not accepted
```

The exact project-produced Termux glibc `libXdamage.so.1.1.0` candidate is accepted only as the selected GTK 3.24.49 GDK X11 `libXdamage.so.1` provider. The provider-selection claim is Class B under ADR 0005; the producing evidence remains Class C because no approved Termux glibc repository has published the package.

Canonical machine-readable record:

```text
experiments/glibc/selected-obsidian-provider-authority/review/
    libxdamage-bounded-provider-authority.tsv
```

## Exact provider identity

```text
candidate review:     LIBXDAMAGE-CANDIDATE-001
recipe base HEAD:     9bdd20c1d36524a0ab016d9b71c748b0cbb20a34
recipe candidate tree:46fe3064b0537aa7b4327d3cefc6891fa3b2cba5
recipe SHA-256:       40ed4b7d663d01efd3c61d961094ff63659be67917d977f0543d2449411eb0e1
contribution SHA-256: eee51ab2293bd63848a0ae9418dc7c0e402a107a9ee2e9eec48573134079b20f
package:               libxdamage-glibc 1.1.6 aarch64
package SHA-256:       09062711dd28f7268f3d7f75c85b3b42a55d3e6d70d1644a9853ee0b4c0e7890
member:                libXdamage.so.1.1.0
member SHA-256:        391916aff0965656e7b81ece7766e3b22068462867b1dd88a0a051b3db9c2d7c
SONAME:                libXdamage.so.1
machine:               AArch64
DT_RPATH:              absent
DT_RUNPATH:            absent
```

The package contains the exact SONAME alias `libXdamage.so.1 -> libXdamage.so.1.1.0`. The unversioned development alias, header, pkg-config metadata, license and documentation are outside this provider decision.

## Capability, necessity and consumer binding

Corrected official GTK 3.24.49 tag commit `198aeace1e9e119c77f4d669bd8efdf337828ad1` declares `xdamage` whenever the X11 backend is enabled, sets `HAVE_XDAMAGE`, includes it in the X11 package set and links `xdamage_dep` into the GDK X11 static backend. The selected GTK closure requires lookup identity `libXdamage.so.1`.

Source-coordinate correction `GTK3-SOURCE-COORDINATE-001` revalidates this relation against `meson.build` blob `08337ec70cf1c006720eb3ab78a8beac32c898f5` and `gdk/x11/meson.build` blob `754ae0a6158003385dc3cbfda2fa17c23eb5c347`.

The retained controlled probe establishes the bounded call and load surface:

```text
XDamageQueryExtension
XDamageCreate
XDamageSubtract
```

It links directly against the candidate, also resolves the three symbols with `dlopen`/`dlsym`, exits successfully and records zero live-prefix escapes. This proves the exact member supplies the selected GDK X11 damage-extension linkage and basic damage-region lifecycle surface. It does not claim complete GTK runtime function or display-server behavior.

## Exact dependency closure

```text
libXfixes.so.3          accepted exact provider
libX11.so.6             accepted exact base provider
libc.so.6               accepted base runtime
ld-linux-aarch64.so.1   accepted base loader
```

The controlled loader additionally resolved transitive `libxcb.so.1`, `libXau.so.6` and `libXdmcp.so.6` from the isolated accepted glibc prefix. This decision does not create or widen their authority.

The exact accepted libXfixes dependency remained unchanged:

```text
package SHA-256: 23fe7f6003d9607db6af5c31b995616270c319f2af11ddcd6292facd43b25b66
member SHA-256:  271e82cbc4aa3db8ff36ad44735552153b6fbaa787bf59b6ec0b20f63d0f386d
```

The exact accepted libX11 member remained `libX11.so.6.4.0` SHA-256 `1d28ce6412b7919e6ad7592d327e7ee5fdf72551868657b8d8eecc3f8ac69e04`.

## Conflict and exclusion result

```text
one exact project-produced Termux glibc dynamic candidate
ordinary Termux/bionic libXdamage 1.1.7 excluded as wrong ABI world
Debian libXdamage 1.1.6 retained as oracle identity only
approved-supplier package absence preserved; publication not inferred
no accepted concrete-member or SONAME-alias collision
headers, pkg-config metadata, docs and unversioned development alias excluded
```

The local candidate is authoritative only by its exact retained Class C production record and this bounded provider decision. It does not become an approved-supplier artifact.

## Update and rollback boundary

Re-review is mandatory if any of the following changes:

```text
source version or SHA-256
recipe base, candidate tree, recipe SHA-256 or contribution SHA-256
package or member SHA-256
machine, SONAME, alias target, DT_NEEDED, RPATH or RUNPATH
pinned GTK commit or X11 damage consumer binding
accepted libXfixes or libX11 identity
controlled loader/symbol result or candidate multiplicity/collision set
```

Before materialization, rollback is revocation of `LIBXDAMAGE-PROV-001` and restoration of the composition gap. Any future materialization must occur in a new immutable generation; runtime rollback is selector reversal to the prior immutable generation preserving its previous GTK X11 provider set.

## Explicitly prohibited inference

This decision does not establish:

```text
approved upstream or supplier publication
complete X11 or GTK provider composition
package-wide libXdamage development surfaces
target paths, alias creation or filesystem population
materialization, deployment or selected-generation activation
full display-server behavior or complete GTK functional acceptance
producing-build equivalence beyond the retained exact Class C record
```

The selected composition remains blocked by six identities. The next production lane is the atomic AT-SPI2/ATK 2.56.2 candidate family; its D-Bus and accessibility services remain disabled and unauthorized unless separately reviewed.
