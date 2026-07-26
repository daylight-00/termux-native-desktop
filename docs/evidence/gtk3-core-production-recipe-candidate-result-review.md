# GTK 3.24.49 atomic GDK/GTK production candidate result review

## Decision

```text
recipe candidate:        QUALIFIED_CLASS_B
local package/pair:      QUALIFIED_CLASS_C
subsequent disposition:  ACCEPTED_BOUNDED_PROVIDER by GTK3-CORE-PROV-001
composition effect:      two GTK core gaps closed; libselinux.so.1 remains
supplier publication:    not accepted
target/activation:       blocked
```

This review records exact result archive SHA-256 `ba0fa0e31cfea2a31f8065ecaccf998a49901c12aa5f62af978728ddd8f10b3a`. The result index, package database, live glibc prefix, tracked repository state, HEAD and tree all verified invariant. The run built in a private workspace and did not install, deploy, populate a target, start a display, restore caches or schemas, execute modules, or activate services.

## Source and production recipe

```text
GTK version:             3.24.49
official tag object:     9003f198803b9b8b1d7def25a2359f8ebb4b25cf
official tag commit:     198aeace1e9e119c77f4d669bd8efdf337828ad1
source archive SHA-256:  a2958d82986c81794e953a3762335fa7c78948706d23cced421f7245ca544cbc
recipe base HEAD:        9bdd20c1d36524a0ab016d9b71c748b0cbb20a34
recipe path:             gpkg/gtk3/build.sh
recipe SHA-256:          dd25427cfdbe418d5d9c6df182bab7f457fd8efd13931509a8d8e2053ffacf5e
contribution SHA-256:    b3b92eb0b5e4d57f7c63af4a1693fd48959ba06da0814823dda696ba9512e770
claim class:             B, reference-adapted production recipe
```

The production recipe contains source, dependency, backend, introspection and package-atomicity coordinates. Private dependency replay, private sysroots, compiler/loader environment launchers, poisoned-environment smokes, evidence reports and result archival remain in the qualification harness and are absent from the contribution patch.

## Configured backend boundary

```text
X11:                     enabled
Wayland:                 enabled
Broadway:                enabled
print backends:          file,lpr
introspection:           enabled
built-in input modules:  none
cloudproviders:          enabled
colord/tracker3:         disabled
profiler/tests/demos/examples/docs/man/installed tests: disabled
```

This records build configuration only. It does not authorize a display server, Broadway daemon, input-module execution, print job execution, schema installation, cache generation, D-Bus ownership, portal or accessibility service operation.

## Exact atomic package and members

```text
package:                 gtk3-glibc 3.24.49 aarch64
package SHA-256:         89dd7d0427932d85b439e18aa05021aca623ed876854a875837be87de1b90262
package members:         534
package symlinks:        6
normalized ELF files:    24
maintainer scripts:      absent

GDK member:              libgdk-3.so.0.2417.32
GDK SHA-256:             a237c3070ff1704f119cc318b6b837a9430a350648476123c1be75ba768d415d
GDK SONAME/alias:        libgdk-3.so.0 -> libgdk-3.so.0.2417.32

GTK member:              libgtk-3.so.0.2417.32
GTK SHA-256:             0404b91acdaa3a2558e3a11214918692f64d0ba3cebaae4722e3aa4a61f31bc6
GTK SONAME/alias:        libgtk-3.so.0 -> libgtk-3.so.0.2417.32

machine:                 AArch64
DT_RPATH/DT_RUNPATH:     absent for both
atomic relation:         libgtk-3.so.0 directly DT_NEEDED-binds libgdk-3.so.0
```

No one-member subset is qualified. Source, version, package lifecycle, aliases, review, update and rollback remain atomic.

## Introspection evidence

```text
Gdk-3.0.gir SHA-256:     8593a7727a9d3af3db5db9f55763fdde623a38697477516f0043c87f6b64b5c8
Gdk-3.0.typelib SHA-256: 11a398feef3b99b591efa220c360c448b914230df6fcd72561f16126bbc5385c
Gtk-3.0.gir SHA-256:     12d076f873ad36d1e815a34fdc92d36768184d925f306e24c4a05affbb897c91
Gtk-3.0.typelib SHA-256: ede3790ae71d482f2cade34a3095930791ca413c70748e1d7b6699e2058c5640
```

These bytes prove coherent namespace generation. They are retained review evidence, not accepted target membership or runtime registration authority.

## Loader and closure result

The display-free probe linked with the candidate GTK/GDK pair and existing private absolute Pango authority, then executed under the canonical Termux glibc loader. It returned:

```text
3.24.49 GdkDisplay
```

The loader mapped candidate GTK/GDK, private Pango, accepted exact dependencies and exact private `libjpeg.so.62`; it recorded no `$HOME/gl`, bionic, RPATH or RUNPATH escape. The exact private compatibility member remained `libjpeg.so.62.4.0` SHA-256 `a537840ef9da6135cb3284bc3b3e0d1fb4f624180a416c2a3964b94714eb7fe5`.

The result qualifies library linkage and a non-display GType/version surface. It does not establish complete widget rendering, display protocol behavior, theme/settings behavior, input method execution, accessibility operation, printing, portal behavior or application-level functional acceptance.

## Package-wide exclusion

The Debian candidate contains headers, pkg-config metadata, unversioned development aliases, GAIL, helper tools, `broadwayd`, shared input modules, file/LPR print backends, schemas, GIR/typelib and other data. They remain exact package inventory only. The bounded provider decision accepts only the two versioned runtime members and their SONAME aliases.

## Disposition

`OPEN_BLOCKED_NO_GLIBC_CANDIDATE` is superseded as the current GTK core production state. One exact Class B recipe and one exact Class C atomic local package now exist. `GTK3-CORE-PROV-001` separately accepts the two-member core provider within a bounded capability scope. Approved-supplier publication remains absent and unaccepted.
