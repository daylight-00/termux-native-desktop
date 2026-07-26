# Bounded atomic GTK 3.24.49 GDK/GTK core provider authority

## Decision

```text
recipe candidate:      qualified Class B
producing record:      retained Class C
provider decision:     ACCEPTED_BOUNDED_PROVIDER
accepted members:      libgdk-3.so.0.2417.32
                       libgtk-3.so.0.2417.32
accepted SONAMEs:      libgdk-3.so.0
                       libgtk-3.so.0
atomicity:             mandatory two-member source/package/update/rollback unit
composition:           not accepted; libselinux.so.1 remains unresolved
supplier publication:  not accepted
target population:     not accepted
activation:            not accepted
```

The exact project-produced Termux glibc pair is accepted only as the selected GTK 3.24.49 GDK display/input abstraction and GTK widget-toolkit core library provider. This is a Class B provider-selection decision under ADR 0005. The local production evidence remains Class C because no approved Termux glibc repository has published the package.

Canonical machine-readable records:

```text
experiments/glibc/selected-obsidian-provider-authority/review/
    gtk3-core-production-recipe-candidate-result-review.tsv
    gtk3-core-bounded-provider-authority.tsv
```

## Exact provider identity

```text
candidate review:       GTK3-CORE-CANDIDATE-001
provider review:        GTK3-CORE-PROV-001
source version:         3.24.49
tag object:             9003f198803b9b8b1d7def25a2359f8ebb4b25cf
tag commit:             198aeace1e9e119c77f4d669bd8efdf337828ad1
source archive SHA:     a2958d82986c81794e953a3762335fa7c78948706d23cced421f7245ca544cbc
recipe SHA:             dd25427cfdbe418d5d9c6df182bab7f457fd8efd13931509a8d8e2053ffacf5e
contribution SHA:       b3b92eb0b5e4d57f7c63af4a1693fd48959ba06da0814823dda696ba9512e770
package:                gtk3-glibc 3.24.49 aarch64
package SHA:            89dd7d0427932d85b439e18aa05021aca623ed876854a875837be87de1b90262
GDK member SHA:         a237c3070ff1704f119cc318b6b837a9430a350648476123c1be75ba768d415d
GTK member SHA:         0404b91acdaa3a2558e3a11214918692f64d0ba3cebaae4722e3aa4a61f31bc6
machine:                AArch64
RPATH/RUNPATH:          absent for both
```

The accepted aliases are exactly:

```text
libgdk-3.so.0 -> libgdk-3.so.0.2417.32
libgtk-3.so.0 -> libgtk-3.so.0.2417.32
```

Unversioned development aliases are excluded.

## Necessity, consumer binding and atomicity

The selected runtime ledger requires both SONAMEs. GTK directly DT_NEEDED-binds GDK, and both exact identities are generated from one official source, one configured build, one package and one rollback boundary. Partial GDK-only or GTK-only acceptance is prohibited.

The display-free direct-loader probe establishes exact version and GDK type loading without starting a display:

```text
3.24.49 GdkDisplay
```

The probe used the canonical Termux glibc loader and resolved candidate GTK/GDK, accepted private dependencies and exact private `libjpeg.so.62` with zero classical `$HOME/gl` or bionic mapping. This proves the bounded library-linkage and non-display type/version surface only.

## Backend and service boundary

The producing recipe enables X11, Wayland and Broadway, enables file/LPR print backend builds, and builds shared input modules and introspection. Those configuration facts are not service or execution authority.

This decision does not authorize:

```text
X11, Wayland or Broadway server startup
broadwayd execution
input-module loading or cache generation
print-backend loading or print execution
schema installation or compilation
theme/settings behavior
D-Bus, accessibility, portal or printing service activation
complete widget rendering or application behavior
```

## Dependency boundary

The exact GDK and GTK `DT_NEEDED` sets were reviewed atomically. They bind accepted project-produced libXdamage and AT-SPI2/ATK providers, accepted private Pango/Cairo/font/GdkPixbuf/GLib/epoxy/xkbcommon/X11 dependencies, and base Termux glibc runtime libraries. The exact `libjpeg.so.62.4.0` compatibility provider is retained only through the accepted GdkPixbuf JPEG scope. No dependency authority is widened by this decision.

## Introspection and package surface

Exact GDK/GTK GIR and typelib hashes are retained as coherence evidence. They are not accepted composition rows, target files or runtime registration surfaces. Headers, pkg-config metadata, GAIL, tools, demos, schemas, modules, print backends, data, documentation and all unversioned development aliases are outside this provider decision.

## Conflict and exclusion result

```text
one exact project-produced Termux glibc atomic package
ordinary Termux/X11 gtk3 bionic package excluded as wrong ABI world
Debian GTK bytes retained as reference/oracle only
approved-supplier publication absent and not inferred
no accepted member or SONAME-alias collision
partial pair acceptance prohibited
package-wide tools/modules/data/development surfaces excluded
```

## Update and rollback boundary

Re-review is mandatory if source tag/commit/archive, recipe base or content, contribution patch, package/member hashes, machine, SONAMEs, aliases, `DT_NEEDED`, RPATH/RUNPATH, backend matrix, GIR/typelib hashes, dependency authority, exact libjpeg62 closure, loader result, collision set, package atomicity or protected-state evidence changes.

Before materialization, rollback is revocation of `GTK3-CORE-PROV-001` and restoration of the two GTK composition gaps. Any future materialization must occur in a new immutable generation; runtime rollback is selector reversal to the prior generation and atomic removal of both members and aliases. Partial rollback is prohibited.

## Explicitly prohibited inference

This decision does not accept approved supplier publication, complete application composition, package-wide development or executable surfaces, target paths, population, materialization, deployment, persistent activation, display-server behavior, Broadway operation, module/cache/schema activation, accessibility, portal or printing services, or producing equivalence beyond the retained exact Class C record.

The selected composition remains blocked by one identity, `libselinux.so.1`. Its build remains unauthorized until direct-consumer necessity and security/policy semantics are separately bounded.
