# libSELinux direct-consumer necessity and security-boundary review

## Decision

```text
review ID:                    LIBSELINUX-CONSUMER-NECESSITY-001
decision:                     DEPENDENCY_ELIMINATION_OR_RESELECTION
provider build authorized:    NO
active selected gaps:         0
composition acceptance:       NOT YET GRANTED
target manifest allowed:      NO
population / activation:      BLOCKED
```

The selected `libselinux.so.1` observation is eliminated from the active composition by exact consumer reselection. No libSELinux provider is required or authorized.

## Exact oracle edge

```text
consumer evidence row: selected:ff6dae6f57afefe0d2b1
consumer:              libmount.so.1.1.0
consumer SHA-256:       3e92bbc2903ed7b319ea68c1c53b468c066db854c5ca3178e1d6e868d4a52877
package:               libmount1:arm64 2.41-5
required identity:      libselinux.so.1
required row:           selected:7e82ba054b7d9f26f80e
```

This is an oracle feature choice, not a mandatory GTK/GdkPixbuf contract.

## Source/configuration cause

util-linux v2.41 compiles `libmount/src/hook_selinux.c` only under `HAVE_LIBSELINUX`. The hook calls `is_selinux_enabled`, `getfilecon_raw`, `freecon`, and `selinux_trans_to_raw_context`. It processes `context`, `fscontext`, `defcontext`, `rootcontext`, and `seclabel` mount options, including `rootcontext=@target`. This optional hook does not establish a selected GUI requirement to load policy, relabel files, change enforcing state, or access Android policy stores.

## Exact selected replacement

```text
provider review:       GDKPIXBUF-UTIL-LINUX-PROV-001
recipe root:           gpkg/util-linux
package:               libmount-glibc 2.40.2-1
package SHA-256:        9004e88a9f43b2d5cf74fd8921e4b74146e3ced64c4f94490cc52d9b138b011a
member:                libmount.so.1.1.0
member SHA-256:         6864b9050ddd5884642c98ea4df07e3ceaf78727324d6e9068d1866594ece1c2
SONAME:                libmount.so.1
DT_NEEDED:             libblkid.so.1; libc.so.6; ld-linux-aarch64.so.1
libSELinux DT_NEEDED:  absent
SELinux imports:       0
```

The exact package bytes recur in the v69 dependency closure and v101 completed GTK candidate. v101 completed configure, build, DESTDIR install, atomic pair verification, GIR/typelib verification, canonical-loader probing, and packaging without a libSELinux provider.

## Necessity conclusion

The selected application contract requires the `libmount.so.1` API used by GLib/GIO, not Debian's optional SELinux-enabled feature set. Reselecting the exact Termux-glibc provider preserves the SONAME/API edge while removing `libselinux.so.1` from `DT_NEEDED` and imported-symbol closure. The decision is `DEPENDENCY_ELIMINATION_OR_RESELECTION`.

## Security boundary

Building or acquiring libSELinux, substituting Android/bionic SELinux bytes, adding aliases or shims, loading policy, accessing Android policy stores, relabeling, changing enforcing state, installing packages, populating a target, deploying, and activating remain prohibited.

## Composition effect

The historical oracle identity remains in provenance ledgers but is no longer an active selected-provider gap. The reviewed provider set has zero unresolved selected identities. Composition acceptance remains a separate Class D decision, and target-manifest generation remains blocked.

## Next valid action

`generate-and-review-non-mutating-selected-target-manifest`
