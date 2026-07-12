# Target Layout Schema Invariants

## Status

```text
schema definition:
    PASS

target row population:
    BLOCKED

extraction/materializer implementation:
    BLOCKED
```

This document defines invariants for a future `TargetLayout` layer. It does not define a target tree, populate a manifest, authorize extraction, or change any device/runtime state.

## Layer boundary

The architecture is split into distinct layers:

```text
SupplyArtifact
    exact acquisition and artifact recognition identity

ProviderObjectAuthority
    canonical content identity and separated authority states

ProviderFragmentMembership
    capability/profile pressure edges only

ApplicationRuntimeComposition
    final include/reference decisions and validation gates

TargetLayout
    target domain, relative path, node policy, ownership and lifecycle
```

No lower layer may silently populate a higher layer.

## Core invariants

### 1. Installed paths are evidence only

`historical_path` and `installed_source_path` prove prior observation or artifact equivalence. They cannot be copied into `target_relative_path` by convention.

### 2. Artifact paths are supply identity only

`source_artifact_member_path` identifies a member inside an exact artifact. Package prefixes and archive paths do not choose a future target domain or target path.

### 3. Artifact metadata is not target policy

Artifact mode, uid, gid and symlink metadata are recognition inputs. Target mode and ownership require explicit policy fields.

```text
artifact mode 0700
    != target mode authorization

artifact mode 0600
    != target readability policy

artifact symlink mode 0777
    != target alias requirement
```

### 4. Absolute and escaping target paths are forbidden

A populated `target_relative_path` must be normalized, relative, non-empty, and contain neither `..` traversal nor empty path components.

### 5. Semantic domains remain separate

At minimum:

```text
WORLD_CORE
WORLD_DATA
SHARED_PROVIDER
APPLICATION_LOCAL
APPLICATION_SUPPLEMENT
MUTABLE_STATE
GENERATED_CACHE
DEVICE_REFERENCE
```

Common supply from one `.deb` does not merge semantic lifecycle. In particular, glibc world-core ELF and glibc-coupled locale data remain distinct domains.

### 6. Fragment membership is not composition inclusion

A `provider-fragment-memberships.tsv` edge records bounded capability pressure. It does not establish installation inheritance, complete dependency closure, target inclusion, activation scope, or rollback scope.

### 7. Canonical objects and artifacts are deduplicated

One content SHA maps to one canonical provider object identity within the current registry. One artifact SHA maps to one supply artifact identity. Multiple fragment edges must not cause duplicate extraction or multiple update owners.

### 8. Alias inclusion is independently authorized

Only these alias classes may be considered for a future runtime composition:

```text
SONAME_RUNTIME_ALIAS
PROVEN_DLOPEN_RUNTIME_ALIAS
LOADER_OR_ENTRYPOINT_ALIAS
PACKAGE_INTERNAL_RELATIVE_ALIAS
```

`LINKER_DEVELOPMENT_ALIAS` is excluded from runtime target population and belongs only to a declared research/build profile. `UNRESOLVED_ALIAS` blocks alias population.

### 9. Final authority precedes population

A target row may be populated only when the owning object or application identity is `ACCEPTED_FINAL`, or when a bounded `REFERENCE_ONLY` relation is explicitly authorized.

The following states block population:

```text
UNRESOLVED
PROVISIONAL
CANDIDATE
CONDITIONAL_WITHOUT_COMPOSITION_DECISION
SOURCE_COMPARISON_OPEN_WHERE_FINAL_SOURCE_IS_REQUIRED
```

### 10. Unresolved issues remain machine-visible

Every populated or reviewed target row must carry `authority_issue_ids`. Any unresolved blocking issue keeps `population_state` below `AUTHORIZED`.

### 11. Mutable and generated state cannot enter immutable content

Mutable user/application state belongs to `MUTABLE_STATE`. Generated caches belong to `GENERATED_CACHE` with a declared generator and replacement policy. Neither may be hashed as immutable provider or application content merely because it existed in a prior run.

### 12. Collision handling is explicit

Silent last-writer-wins is forbidden. A path collision must resolve through one of:

```text
ERROR
SAME_CONTENT_DEDUP
DECLARED_OVERRIDE
EXTERNAL_REFERENCE
```

A declared override requires an authority record naming the winner and the validation consequence.

### 13. Update and rollback ownership are singular

Each populated object has one canonical `update_domain` and one `rollback_domain`. Shared fragment consumers do not create separate copies or owners.

World rollback remains distinct from provider/application generation rollback.

### 14. Supply recognition and clean acquisition remain distinct

An exact SHA, size, repository filename and member hash prove recognition. Clean acquisition additionally requires repository trust policy, retained artifact or immutable snapshot policy, signature/index verification, and future availability.

### 15. Application identity classes are not conflated

The future composition must distinguish:

```text
FIRST_GENERATION_CONTENT_IDENTITIES
APPLICATION_LOCAL_REFERENCE_IDENTITIES
APPLICATION_PAYLOAD_IDENTITY
APPLICATION_LAUNCHER_SUPPLY_IDENTITY
APPLICATION_DOMAIN_SUPPLEMENT_IDENTITIES
```

The 96 first-generation content identities are not the application-local payload.

## Current permitted state

During `NORMALIZE_PROVIDER_AUTHORITY_COVERAGE_AND_LOCK_SEMANTICS`, every target row remains:

```text
population_state:
    UNPOPULATED_SCHEMA_ONLY
```

No populated target manifest, extraction script, staging tree, generation, `current` pointer, launcher change, loader-state mutation, or package operation is authorized.
