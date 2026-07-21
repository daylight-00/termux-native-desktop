# Bounded atomic AT-SPI2 core provider authority for GTK 3.24.49 accessibility linkage

## Decision

```text
atomic recipe candidate: qualified Class B
producing record:         retained Class C
provider decision:        ACCEPTED_BOUNDED_PROVIDER
accepted package:         at-spi2-core-glibc 2.56.2 aarch64
accepted members:         libatk-1.0.so.0.25611.1
                          libatk-bridge-2.0.so.0.0.0
                          libatspi.so.0.0.1
accepted capability:      selected GTK 3.24.49 in-process ATK accessible-object model and linked ATK-bridge/AT-SPI library boundary
composition:              not accepted
supplier publication:     not accepted
target population:        not accepted
service authority:        not accepted
activation:               not accepted
```

The exact project-produced Termux glibc three-member family is accepted only as one atomic provider for the selected GTK 3.24.49 accessibility **library-linkage** boundary. The decision covers GTK's ATK accessible-object model, GTK's linked `atk-bridge` boundary, and the bridge's direct AT-SPI library dependency. It does not authorize an accessibility bus, registry daemon, helper execution, active service metadata, accessibility enablement, or complete assistive-technology behavior.

The provider-selection claim is Class B under ADR 0005. The exact recipe and independently reproduced package/member record remain Class B and Class C evidence respectively because no approved Termux glibc supplier repository has published this package.

Canonical machine-readable record:

```text
experiments/glibc/selected-obsidian-provider-authority/review/
    at-spi2-core-bounded-provider-authority.tsv
```

## Exact atomic provider identity

```text
candidate review:       ATSPI2-CORE-CANDIDATE-001
provider review:        ATSPI2-CORE-PROV-001
source version:         2.56.2
source SHA-256:         e1b1c9836a8947852f7440c32e23179234c76bd98cd9cc4001f376405f8b783b
recipe base HEAD:       9bdd20c1d36524a0ab016d9b71c748b0cbb20a34
recipe candidate tree:  0f6e255985e5967fe793b8ee3e86f248a430513f
recipe SHA-256:         6f727204730b6b0a3496c169f635c5016903cb64b816b7c84ca91fcbc9d4e30d
contribution SHA-256:   26f6741fbb081c64bffb53d0a467564845df5ef5a0983b09f00e2e924bba6c50
result archive SHA-256: 461b24dac879ca71252c209f0013ff17cb8f8ed1a889a32f0376b87372f3d3a4
evidence freeze SHA-256:b516ed70c10b6bf91fac08e2a461dc55e9f2b5337a4dade5b995e96fa5b4b40d
package SHA-256:        9a1395e893448508cfb8fbdee8ef0dd8268b8d21e9ac7bbe792f163dce6c365a
machine:                 AArch64
DT_RPATH:                absent on all three members
DT_RUNPATH:              absent on all three members
```

Exact members and aliases:

```text
libatk-1.0.so.0.25611.1
  SHA-256: 55c9c8a3767258bcc1d25640223aa8638ca0fc1bf5a310c7c87de14ad66191d7
  SONAME:   libatk-1.0.so.0
  alias:    libatk-1.0.so.0 -> libatk-1.0.so.0.25611.1

libatk-bridge-2.0.so.0.0.0
  SHA-256: cce78fd50cb5b3a19bdc046112c75a2309ad5feda3183e62f538bc1177e72773
  SONAME:   libatk-bridge-2.0.so.0
  alias:    libatk-bridge-2.0.so.0 -> libatk-bridge-2.0.so.0.0.0

libatspi.so.0.0.1
  SHA-256: e94f2980cf8580634d7ab3c4f9ad2d8713880a1e3614001aed7a63ba6388c874
  SONAME:   libatspi.so.0
  alias:    libatspi.so.0 -> libatspi.so.0.0.1
```

The provider is atomic. No one- or two-member subset is accepted. The package's unversioned development aliases, headers, pkg-config files, documentation, helper programs, and disabled metadata remain package content outside this provider decision.

## Capability, necessity and consumer binding

GTK 3.24 exposes `GtkAccessible` as an `AtkObject`-derived base for widget accessibility implementations, and the GTK 3 accessibility contract links `atk-bridge` into GTK by default. The corrected official GTK 3.24.49 source coordinate is tag object `9003f198803b9b8b1d7def25a2359f8ebb4b25cf` peeled to commit `198aeace1e9e119c77f4d669bd8efdf337828ad1`. Source-coordinate correction `GTK3-SOURCE-COORDINATE-001` revalidates the relation against GTK blobs `08337ec70cf1c006720eb3ab78a8beac32c898f5`, `ea866d8231c2a5fa9b1972c4b11148c35cd228b8`, and `9c2229b3e886b3dd3c8f0c8855d484bdd9f936f1`.

The exact family satisfies three coupled linkage directions:

```text
GTK accessible objects -> libatk-1.0.so.0
GTK accessibility bridge -> libatk-bridge-2.0.so.0
libatk-bridge-2.0.so.0 -> libatk-1.0.so.0 + libatspi.so.0
```

The exact bridge directly requires both accepted sibling SONAMEs. Its AT-SPI linkage includes the bounded library calls `atspi_dbus_connection_setup_with_g_main`, `atspi_dbus_server_setup_with_g_main`, `atspi_get_a11y_bus`, `atspi_is_initialized`, and `atspi_set_main_context`. The bridge exports `atk_bridge_adaptor_init` and `atk_bridge_adaptor_cleanup`. The ATK member supplies the accessible-object and toolkit interfaces consumed by GTK and the bridge, including `atk_object_get_type`, `atk_implementor_ref_accessible`, `atk_get_root`, `atk_get_toolkit_name`, and `atk_get_toolkit_version`.

Controlled loading, ELF inspection, exact ABI comparison, and GIR/typelib validation establish the three library identities with zero live-prefix escapes. They do not establish that a bus exists, that a registry daemon is running, that assistive technologies can connect, or that an application has enabled accessibility.

## Exact dependency closure

```text
libatk-1.0.so.0:
  libglib-2.0.so.0
  libgobject-2.0.so.0
  libc.so.6
  ld-linux-aarch64.so.1

libatk-bridge-2.0.so.0:
  atomic sibling libatk-1.0.so.0
  atomic sibling libatspi.so.0
  libdbus-1.so.3
  libglib-2.0.so.0
  libgobject-2.0.so.0
  libc.so.6
  ld-linux-aarch64.so.1

libatspi.so.0:
  libX11.so.6
  libXi.so.6
  libdbus-1.so.3
  libgio-2.0.so.0
  libglib-2.0.so.0
  libgobject-2.0.so.0
  libgcc_s.so.1
  libc.so.6
  ld-linux-aarch64.so.1
```

The exact `libgcc_s.so.1` dependency is bounded to `gcc-libs-glibc 14.2.1-1`, package SHA-256 `919c2e80a629d674dd450b0a0edd11378284f1ed9d2a8fd3c9c91d7ac72f041f`, payload SHA-256 `22d5db25fece632754f7a0fb1c6586eb6e93eab6a5866da487b86f115d4e389d`, and the exact `_Unwind_Resume@GCC_3.0` and `__gcc_personality_v0@GCC_3.3.1` relation produced by the pinned GNU `-fexceptions` framework policy. This decision consumes existing bounded dependency authority and does not widen those dependencies.

## GIR and service boundary

The package contains the exact qualified introspection artifacts:

```text
Atk-1.0.gir       a15e67a1f42f4720d0b1920cf0739cc0a73d94ae04bcc69d580fa51bc4b4d6d3
Atk-1.0.typelib   0454707e83528cc498020f85f77761b6c8b365c592988dd3c60b00f1f15c7fc7
Atspi-2.0.gir     f97c8d5b3ef16cb9489d1ff57f418887abae759c5903bde15510355d10874caf
Atspi-2.0.typelib 125a679a0123b025562346dcbfa9fdc0ed3208aeee388db2c26cab8a25c6069d
```

They are retained as part of the atomic update and rollback boundary but do not create language-binding, service, or activation authority beyond the accepted library scope.

Exactly seven D-Bus, autostart, systemd, Xwayland, defaults, and GTK-module metadata files remain under `share/termux-native-desktop/disabled/at-spi2-core/`. No active lookup-path copy is accepted. The `at-spi-bus-launcher` and `at-spi2-registryd` helpers remain non-executed package content. The package has no maintainer scripts or triggers.

## Conflict and exclusion result

```text
one exact project-produced Termux glibc atomic package candidate
ordinary Termux/bionic AT-SPI2 and ATK packages excluded as the wrong ABI world
Debian 2.56.2 oracle members excluded as provider bytes
approved-supplier package absence preserved; publication not inferred
older split glibc ATK/AT-SPI package lifecycle rejected by Breaks/Replaces boundary
partial one- or two-member acceptance rejected
no accepted concrete-member or SONAME-alias collision
active activation metadata, service ownership and helper execution excluded
headers, pkg-config files, unversioned development aliases and package-wide surfaces excluded
```

## Update and rollback boundary

Re-review is mandatory if any of the following changes:

```text
source version or source SHA-256
recipe base, candidate tree, recipe SHA-256 or contribution SHA-256
package SHA-256, package lifecycle fields or any member SHA-256
machine, SONAME, alias target, DT_NEEDED, RPATH, RUNPATH or GCC runtime symbols
pinned GTK commit or GTK ATK/atk-bridge consumer binding
any accepted direct dependency identity or authority
any GIR/typelib SHA-256 or shared-library binding
seven-file disabled metadata inventory, active metadata count or helper inventory
candidate multiplicity, collision set, atomicity, update or rollback behavior
```

Before materialization, rollback is revocation of `ATSPI2-CORE-PROV-001` and restoration of the three composition gaps. Any future materialization must place the whole family, its exact aliases and GIR/typelib artifacts into one immutable generation while retaining activation metadata disabled. Runtime rollback is selector reversal to the prior immutable generation. Partial member rollback is prohibited.

## Explicitly prohibited inference

This decision does not establish:

```text
approved upstream or supplier publication
complete GTK or application provider composition
package-wide ATK or AT-SPI development surfaces
D-Bus bus ownership, accessibility-bus availability or registry-daemon authority
helper execution, active metadata restoration or accessibility enablement
screen-reader, automation or complete assistive-technology behavior
target paths, target population, materialization, deployment or activation
producing-build equivalence beyond the retained exact Class C record
```

The selected composition remains blocked by the GTK 3 GDK/GTK pair and `libselinux.so.1`. The next production lane is the atomic GTK 3.24.49 core candidate; this decision does not grant authority to that pair.
