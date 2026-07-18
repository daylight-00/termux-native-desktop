# Active task: prepare the libXdamage glibc recipe-contribution candidate

> Task ID: `prepare-libxdamage-glibc-recipe-contribution-candidate`
>
> Expected state on completion: an isolated Class C `libxdamage-glibc` candidate and a reviewable Class B `gpkg/libxdamage` recipe-contribution diff are captured with exact source, package, member, SONAME, alias, dependency, consumer and rollback evidence. No package repository publication, installation, target population, deployment or activation occurs.

## Objective

Execute the first lane selected by the accepted missing-provider production-boundary decision: reproduce exact upstream libXdamage 1.1.6 for the Termux glibc world and prepare a minimal upstream recipe contribution.

## Why now

All seven unresolved selected identities have completed read-only candidate discovery and are reviewed blockers. The accepted production-boundary decision selects libXdamage as the lowest-risk first lane because it is one exact leaf member with a small accepted dependency closure and a retained upstream source digest.

## Authoritative inputs

```text
source:          libXdamage 1.1.6
source SHA-256:  52733c1f5262fca35f64e7d5060c6fcd81a880ba8e1e65c9621cf0727afb5d11
expected member: libXdamage.so.1.1.0
expected SONAME: libXdamage.so.1
reference recipe: termux/termux-packages@552a825cc8433e3aced966ff4bf5c8ea9255ca7d:x11-packages/libxdamage/build.sh
candidate recipe destination: termux-pacman/glibc-packages:gpkg/libxdamage
```

## In scope

- verify exact source bytes and hash;
- derive the smallest glibc recipe from the authoritative upstream source and retained ordinary Termux dependency semantics;
- record every prefix, toolchain, configure, packaging or path adaptation;
- build only in an isolated cache/workspace;
- retain exact package, recipe diff, member, aliases, ELF metadata, `DT_NEEDED`, symbols and build logs;
- prove direct closure to accepted `libX11.so.6`, `libXfixes.so.3`, libc and loader providers;
- run bounded load/symbol and GTK 3.24.49 GDK X11 consumer-binding checks that do not require target population;
- define package removal and rollback.

## Out of scope

Publishing or pushing to the upstream recipe repository, installing or upgrading packages, changing configured repositories, copying bionic or Debian bytes, creating a cross-world alias, populating a selected target, deployment, activation or widening GTK authority.

## Required reading

- `docs/current/STATE.yaml`
- `docs/decisions/0005-proportional-assurance-depth.md`
- `docs/evidence/missing-glibc-provider-production-boundary.md`
- `docs/evidence/libxdamage-provider-evidence-blocker.md`
- `docs/evidence/selected-obsidian-provider-composition-review.md`

## Claim classes

- Recipe and Termux glibc adaptation: Class B reference-adapted.
- Locally produced `.deb` and ELF: Class C independently reproduced.
- Eventual approved-repository artifact: separate Class A/B review only after supplier publication.

## Pending external inputs

None for package authoring. Network-backed source and build-input acquisition occurs only in the user Termux runner. Upstream publication or contribution submission is a later, separately authorized action.

## Completion criteria

- Exact source hash and reference recipe coordinates are verified.
- One reviewable `gpkg/libxdamage` recipe diff is retained.
- One isolated `.deb` and exact `libXdamage.so.1.1.0` member are retained with hashes, AArch64, SONAME, alias and dependency evidence.
- Class B recipe/adaptation and Class C produced-artifact records are explicit.
- Bounded load/symbol and GTK GDK X11 consumer-binding checks are recorded.
- Repository state and configured package state remain unchanged; no installation, target, deployment or activation occurs.

## Stop conditions

Stop without a candidate when source identity, dependency closure, package layout, SONAME/alias contract, absence of RPATH/RUNPATH, consumer binding, license/distribution boundary or rollback cannot be made exact. Do not substitute version 1.1.7 or any bionic artifact for the selected 1.1.6 identity.

## Next valid action

Author a separate exact-base, non-installing Termux runner that acquires the pinned source and required build inputs, produces the isolated candidate and contribution evidence, archives the result, and leaves the repository and configured package state unchanged.
