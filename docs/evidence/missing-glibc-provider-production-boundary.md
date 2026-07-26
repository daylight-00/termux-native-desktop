# Missing Termux glibc provider production boundary

## Decision

```text
planning decision:             ACCEPTED_PLANNING_ONLY
reviewed families:             4
completed production lanes:    libXdamage, atomic AT-SPI2/ATK, atomic GTK 3 core
remaining family:              libSELinux necessity review only
immediate build authorized:    NO
libSELinux build authorized:   NO
composition:                   ACCEPTED_BOUNDED_COMPLETE_SELECTED_PROVIDER_COMPOSITION
target/activation:             blocked
```

The absence of an approved package never authorizes copying bionic, Debian-oracle or Android platform bytes. Production recipes and local artifacts remain Class B and Class C claims respectively until separately reviewed.

## Completed lanes

1. Exact project-produced `libXdamage.so.1.1.0` has bounded GTK 3.24.49 GDK X11 damage-extension authority.
2. Exact atomic ATK/ATK-bridge/AT-SPI 2.56.2 family has bounded GTK accessibility library-linkage authority; service metadata and helpers remain inactive.
3. Exact atomic GTK 3.24.49 `libgdk-3.so.0.2417.32`/`libgtk-3.so.0.2417.32` pair has bounded core library authority. Package-wide development, executable, module, schema, print, display and service surfaces remain excluded.

Each lane retains exact source, recipe, producing, package/member, dependency, loader, update and rollback coordinates. Completion does not inherit authority to the next family or to composition/target/activation.

## Remaining libSELinux boundary

Do not produce a glibc `libselinux.so.1` candidate until exact direct consumers and imported symbols are identified and the feature cannot be removed or reselected. A separate necessity/security review must cover libsepol/PCRE2 closure, policy stores, filesystem contexts, absent Android policy paths, and proof that validation does not load policy, relabel filesystems, change enforcing state or mutate Android state.

Android `libandroid-selinux`, `/system` libraries, cross-world aliases and compatibility shims are rejected. The libSELinux lane was closed by dependency elimination through exact libmount consumer reselection. The bounded composition is now accepted by `SELECTED-COMPOSITION-ACCEPT-001`. The next task is `generate-and-review-non-mutating-selected-target-manifest`; it grants no target-population or activation authority.


## libSELinux lane disposition

The libSELinux production lane is closed without production. Exact consumer review selected `DEPENDENCY_ELIMINATION_OR_RESELECTION`: the accepted `gpkg/util-linux` libmount member removes the Debian oracle's optional SELinux linkage. `libselinux_build_authorized` remains `NO`. Android/bionic substitution, policy mutation, target population and activation remain prohibited.
