# 0137 — Selected Obsidian World Internals, Locale and Loader Lifecycle Boundary

## Status

```text
repository-side authority boundary:
    PASS

AUTH-001 world reconstruction/lifecycle:
    OPEN / NARROWED

AUTH-008 locale and loader-state portion:
    BOUNDED / OTHER DATA CAPABILITIES OPEN

ApplicationRuntimeComposition:
    NOT REACHED

target population, extraction, materialization and activation:
    BLOCKED

device transaction:
    NOT REQUIRED
```

This record completes the first repository-side item under the `0136` next-state order by explicitly bounding world internals, locale policy and loader-state lifecycle. It does not claim clean reconstruction, select a successor glibc version, define loader-policy contents, populate target rows or authorize a package/device transaction.

## Authority and inputs

Read under:

```text
docs/refactor/0112-selected-obsidian-passive-map-selection-diagnostic-pass-and-contract-decision.md
docs/refactor/0115-proot-oracle-supply-and-baseline-model.md
docs/refactor/0116-end-to-end-architecture-audit-and-provider-authority-intervention.md
docs/refactor/0133-selected-obsidian-priority-provider-authority-review.md
docs/refactor/0134-selected-obsidian-provider-profile-locked-member-draft.md
docs/refactor/0135-selected-obsidian-provider-profile-lock-draft-architecture-audit.md
docs/refactor/0136-selected-obsidian-provider-authority-coverage-and-lock-semantics-normalization.md
```

Evidence used:

```text
exact glibc 2.42 artifact:
    artifact:59e47a50b77ba9c0c1cc7cd0
    SHA-256 59e47a50b77ba9c0c1cc7cd0dafbb1558528cb544a740858faad0263e8b9b27f

reviewed world-core objects:
    6

accepted glibc-coupled locale members:
    12

normalized selected/reference authority denominator:
    161 rows

named glibc NSS/gconv module rows in that denominator:
    0

observed unowned loader state:
    ld.so.conf  82 bytes     SHA-256 01f5b20f777259a788b98cb522a34b7e0edd62f4babdce43a518be1672365512
    ld.so.cache 44,684 bytes SHA-256 91b45aec95233536c439ed87e11ee3e8fe2a3afc7a747fe998c6df434329f2aa
```

The canonical boundary table is:

```text
experiments/glibc/selected-obsidian-provider-authority/review/
    world-lifecycle-authority-boundary.tsv
```

## Decision 1 — supply artifact and runtime authority remain separate

The exact `glibc 2.42` artifact is accepted as the current Termux/Android world supply and as the bounded clean-reconstruction input. Its exact repository metadata, artifact identity and installed-member equivalence are strong evidence.

That artifact-wide supply result does not make every package member runtime content.

```text
exact glibc artifact supply
    != complete runtime-world manifest

all artifact members equal live installation
    != all members required by declared applications
```

The six reviewed loader/core objects remain accepted current world authority for the bounded selected/reference graph. Headers, static/start files, build metadata, administration tools and unobserved runtime internals do not inherit application-runtime inclusion.

## Decision 2 — NSS, gconv and other internals are demand-gated

No named glibc NSS or gconv module occurs in the normalized 161-row selected/reference authority denominator.

This absence is not a universal proof that the modules are unnecessary. It is sufficient to reject package-inertia inclusion in the current authority phase.

A world-internal module becomes eligible for authority review only after a named discriminator records:

```text
exact module identity;
exact declared application or launcher consumer;
observed load or failing capability transition;
semantic reason for the module;
exact supply/source identity;
world-version coupling;
validation and rollback gate.
```

Electron's NSS/security libraries remain `AUTH-009` generic capability providers. They must not be confused with glibc NSS service modules.

No device collector is requested now. A bounded read-only collector is permitted only if a concrete application or launcher decision cannot be resolved from existing evidence.

## Decision 3 — locale is world-coupled data, not application payload

The twelve accepted `en_US.utf8` members retain the Phase B5 policy:

```text
semantic owner:
    WORLD_LOCALE_DATA

current behavior:
    reference glibc-coupled prefix data

application-generation behavior:
    do not copy locale bytes
```

World core and locale data share the current exact artifact but remain separate semantic, validation and rollback-trigger domains.

This means:

```text
one atomic artifact transaction
    + separate world-core gate
    + separate locale gate
```

A locale failure may require world rollback. Because the current supply is one exact artifact, rollback reverts the shared artifact atomically rather than mixing locale data from one world version with core ELF from another.

The accepted set is not a universal future locale policy. Additional language coverage requires a declared application/user requirement and a separate authority decision.

## Decision 4 — `ld.so.conf` is policy input, not captured authority

The observed `ld.so.conf` is unowned live state. Its path, bytes and hash are evidence, not target policy.

Accepted class:

```text
semantic class:
    LOADER_POLICY_INPUT

lifecycle owner:
    WORLD_LOADER_POLICY

content state:
    UNDEFINED UNTIL ApplicationRuntimeComposition IS ACCEPTED
```

Future policy content may be derived only from accepted world/platform/generic/application authorities and explicit search-order/collision invariants.

The current live file must not be copied by inertia. This record defines no target path, mode, owner, search directory or alias.

## Decision 5 — `ld.so.cache` is derived mutable state

The observed `ld.so.cache` is not a supply artifact, provider object or rollback authority.

Accepted class:

```text
semantic class:
    DERIVED_LOADER_CACHE

lifecycle owner:
    WORLD_LOADER_CACHE

composition role:
    derived after composition; never an input to composition
```

After an `ApplicationRuntimeComposition` is accepted, a future world transaction must regenerate the cache with an explicitly accepted loader-cache generator coupled to the accepted world—normally that world's `ldconfig`, if separately accepted—and validate that cache entries resolve only accepted runtime providers and accepted runtime aliases.

This is a lifecycle rule, not permission to run `ldconfig` now. No loader state is mutated by this transaction.

## Decision 6 — world update and rollback gate

A future `2.42 -> 2.43` or other world transition is one atomic supply transaction with independent acceptance gates:

```text
1. repository trust, exact artifact identity and retained rollback artifact;
2. source/recipe and artifact-to-build evidence;
3. loader/core object identity and behavior;
4. named NSS/gconv/runtime-internal demand closure;
5. locale identity, compatibility and declared coverage;
6. loader-policy derivation from accepted composition;
7. loader-cache regeneration and accepted-entry validation;
8. declared application smoke/survival validation;
9. previous-world rollback validation.
```

World rollback is independent of application-generation rollback. During the current authority phase it must not mutate `current`, the promoted launcher or the existing immutable generation.

## Ledger effect

`AUTH-001` remains `OPEN_CONTRACT`, but its unresolved surface is narrowed to:

```text
clean acquisition trust and immutable retention;
artifact-to-build attestation;
complete clean-world reconstruction mechanism;
exact NSS/gconv/runtime-internal set if named demand appears;
successor-version evidence and execution validation.
```

The locale and loader-state portion of `AUTH-008` is bounded:

```text
locale:
    glibc-coupled world data; reference, do not copy

ld.so.conf:
    composition-derived policy input; live hash is evidence only

ld.so.cache:
    derived mutable cache; regenerate only after composition acceptance
```

`AUTH-008` remains open for fonts, pixbuf, icons, MIME and generated-schema authority.

## Next valid repository task

The umbrella state remains:

```text
CLOSE_GLOBAL_WORLD_APPLICATION_GENERIC_AND_DATA_AUTHORITY_GAPS
```

The next active task is now:

```text
ESTABLISH_OBSIDIAN_ELECTRON_PAYLOAD_LAUNCHER_AND_SUPPLEMENT_AUTHORITY
```

This task must keep separate:

```text
FIRST_GENERATION_CONTENT_IDENTITIES
APPLICATION_LOCAL_REFERENCE_IDENTITIES
APPLICATION_PAYLOAD_IDENTITY
APPLICATION_LAUNCHER_SUPPLY_IDENTITY
APPLICATION_DOMAIN_SUPPLEMENT_IDENTITIES
```

## Claim boundary

This transaction accepts:

```text
world artifact supply versus runtime authority separation;
demand-gated world-internal module policy;
glibc-coupled locale reference policy;
separate core/locale validation domains inside one atomic artifact transaction;
loader-policy input lifecycle class;
derived loader-cache lifecycle class;
future world update/rollback gate structure.
```

It does not accept:

```text
complete clean reconstruction;
any specific NSS/gconv module;
future locale expansion;
loader-policy contents;
loader-cache contents or generator invocation;
ApplicationRuntimeComposition;
target paths, modes, owners or aliases;
extraction, materialization or activation.
```

## Stop line

Do not:

```text
treat the exact glibc artifact as a deployable application runtime profile;
include NSS/gconv modules by package inertia;
confuse Electron NSS libraries with glibc NSS service modules;
copy locale bytes into an application generation;
copy the observed ld.so.conf as target policy;
copy the observed ld.so.cache as authoritative state;
run ldconfig or mutate loader state;
populate target rows;
write extraction/materializer code;
install, remove, upgrade or downgrade packages;
mutate current, launcher, generation or RPATH.
```
