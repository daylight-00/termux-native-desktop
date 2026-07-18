# libSELinux provider evidence blocker

## Decision

```text
selected identity:       libselinux.so.1
required SONAME:         libselinux.so.1
provider authority:      OPEN_BLOCKED_NO_GLIBC_CANDIDATE
composition effect:      NONE; the selected identity remains a gap
target/policy/activation: BLOCKED
```

The read-only acquisition result is retained by SHA-256
`319fa617ab9a419118c52a7f72e9e93b535e96821f0e1de71f7e1502f07ac770`.
The probe did not install, remove, or upgrade packages; mutate the repository; load SELinux policy; change enforcing state; relabel a filesystem; populate a provider target; deploy; or activate any runtime.

## What the approved indexes established

The bounded candidate-name set was:

```text
libselinux
libselinux-glibc
libselinux1
libselinux1-glibc
selinux-glibc
```

No approved Termux glibc coordinate was returned for any candidate. The only SELinux package observed was installed ordinary Termux/bionic `libandroid-selinux` version `14.0.0.11-1`, selected from `termux-main`, with filename `pool/main/liba/libandroid-selinux/libandroid-selinux_14.0.0.11-1_aarch64.deb` and dependency `pcre2`. It is the Android fork of libSELinux and belongs to a different ABI and package world. It does not provide an approved Termux glibc artifact, exact glibc member, or authority for the selected Debian `libselinux.so.1` identity.

## Recipe provenance boundary

At pinned glibc recipe commit `9bdd20c1d36524a0ab016d9b71c748b0cbb20a34`, exact-path checks for `gpkg/libselinux/build.sh`, `gpkg/libselinux1/build.sh`, `gpkg/selinux/build.sh`, and `gpkg/libsepol/build.sh` found no libSELinux-producing root. The approved glibc recipe boundary therefore contains no candidate that can be bound to the selected identity.

This finding is narrower than an upstream-source or ABI impossibility claim. It does not claim that libSELinux cannot be built for the Termux glibc world or that the Android fork is defective. It records only that the currently approved package and pinned-recipe sources contain no candidate that ADR 0005 permits this project to accept.

## Android platform boundary

Android platform `libselinux.so` observations and the installed bionic `libandroid-selinux` package are retained only as boundary evidence. Their process-context, policy-store, labeling, filesystem-context, service, and bionic-linkage behavior cannot be silently substituted for the selected glibc runtime identity. No policy loading, enforcing change, relabeling, Android platform mutation, or cross-world alias is authorized.

## Composition consequence

This completes read-only candidate discovery for all seven unresolved selected identities. Every remaining gap is now a reviewed `BLOCKED_NO_TERMUX_GLIBC_PROVIDER_CANDIDATE` row:

```text
libXdamage.so.1
libatk-bridge-2.0.so.0
libatk-1.0.so.0
libatspi.so.0
libgdk-3.so.0
libgtk-3.so.0
libselinux.so.1
```

The composition decision remains `REVIEWED_BLOCKED_INCOMPLETE`. No target manifest, population, materialization, deployment, policy mutation, service activation, or selected-generation activation is allowed.

## Stop condition and reopening gate

ADR 0005 requires this tranche to stop without authority. Reopening requires an exact approved Termux glibc archive or a separately authorized project-produced candidate, package and member digest, exact `libselinux.so.1` ELF and alias identity, pinned source/recipe and production record at the applicable implementation class, runtime dependency closure, selected-consumer binding, Android/Termux policy and labeling boundary, collision review, update boundary, and rollback boundary.

Bionic package availability, Android platform bytes, Debian oracle identity, source-level ABI expectations, or upstream release metadata are not interchangeable with that evidence.

The next task is non-mutating definition of the missing glibc provider production boundary across the four blocker families. It authorizes planning only, not a build.
