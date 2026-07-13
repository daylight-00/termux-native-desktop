# Status

> **State:** generic build-attestation and adaptation review set DEFINED / BOUNDED; 16 evidence requirements, 28 pinned-root work units and 37 object work units are canonical, while evidence collection, all acceptance decisions and target population remain blocked
> **Updated:** 2026-07-13

## Current conclusions

- Existing prototype, ownership, ABI, graphics, selected-generation, passive-runtime, N2/N3, source-recipe, and exact binary-artifact evidence remain valid.
- The existing selected generation remains immutable and unactivated. `current` is absent and the promoted launcher is unchanged.
- Exact priority supply remains a strong bounded result: 28 exact indexed `.deb` artifacts, 6,887 compared members, and zero member mismatches.
- Package-wide runtime inference remains rejected.
- The 59 priority reviewed objects are a bounded subset of the 161 semantic-object denominator, not global authority completion.
- The 96 first-generation contents are correctly defined as 91 selected external ELF + 4 fonts + 1 generated schema aggregate. They are not application-local payload.
- Eleven application-local reference identities remain a distinct AppDir/`$ORIGIN` set.
- Application payload, application-local reference, GUI/CLI launcher supply, publication, supplement, and release-transition identities are now explicitly separated under the bounded `AUTH-010` contract.
- Exact artifact supply, semantic role, Termux/Android adaptation, candidate-source comparison, artifact-to-recipe binding, necessity, and provisional final provider are now independent states.
- Canonical provider-object rows total 60: 59 bounded reviewed objects plus optional `libtermux-exec.so`.
- Canonical provider-fragment pressure contains 63 reviewed memberships plus one optional non-denominator edge.
- The old six “profiles” are historical non-materializing lock files. Seven normalized provider fragments now express pressure only.
- `libxcb-render.so.0` and `libxcb-shm.so.0` remain in the base X11 fragment because passive evidence records mapped/direct base consumers. Graphics remains secondary narrative pressure only.
- X11/XCB classification is conservative: libxcb and libxshmfence have explicit Termux adaptation evidence; the other reviewed X11 objects remain platform-versus-generic provisional.
- `libcap.so.2` remains `PLATFORM_OR_GENERIC` provisional with exact supply accepted and conditional necessity.
- Canonical artifact aliases total 84: 40 SONAME runtime candidates, 41 linker/development aliases, 2 loader/entrypoint aliases, and 1 package-internal unresolved alias.
- The historical lock files contain 64 content edges + 92 alias edges = 156 rows. “93 required aliases” is withdrawn.
- Sixty-one non-priority selected/reference provider identities are mapped to graphics, printing, GTK/GUI, security, audio, device, or global generic authority issues.
- World-core ELF and glibc-coupled locale data remain separate semantic/lifecycle fragments despite sharing the same exact artifact.
- Exact artifact recognition does not close clean acquisition. Repository trust, key/signature policy, immutable retention/snapshot, future availability, source archive identity, and build attestation remain open.
- A twenty-field target-layout schema and invariants exist, but every target row remains unpopulated.
- The world/locale/loader lifecycle boundary is accepted without clean-reconstruction or composition claims.
- No named glibc NSS/gconv module occurs in the normalized 161-row selected/reference denominator; world internals remain demand-gated.
- The twelve accepted locale members remain glibc-coupled world data; `ld.so.conf` is composition-derived policy input and `ld.so.cache` is derived mutable state.
- Exact Obsidian payload acquisition identity and named supplement membership remain open; the exact current repository GUI/CLI launcher source identities are bounded and accepted.
- The 61 non-priority generic identities are now bounded as six capability review units: 60 Debian-rootfs oracle identities and one local graphics-experiment identity. Neither observed origin is clean supply or final provider authority.
- Shared generic ownership is the default review direction; protected-world, application-local and application-supplement ownership require explicit object-specific authority.
- A canonical 61-row exact-candidate search-token contract and read-only apt/source/cache collector are repository-ready and the bounded device receipt has been reviewed.
- The reviewed snapshot contains 37 direct apt+recipe family candidates, 13 indirect token-only rows and 11 identities with no retained candidate.
- Candidate family matches remain non-authoritative; `.deb` member binding, adaptation, necessity and final providers remain open.
- A bounded named comparison set now covers all 37 direct identities with 34 exact indexed runtime/split artifacts and 44 member-search edges; 14 static-only artifacts and one architecture-all development artifact are explicitly excluded from download scope.
- The comparison-set definition performed no download or extraction and accepted no authority decision.
- The recipe-binding/drift-target receipt verifies all 34 cached artifacts, 28 pinned recipe roots, 84 recipe files and 15 drift-target ELFs without package mutation or extraction.
- Review accepts 37 recipe-lineage candidates and 36 object/member candidate rows, but accepts zero build attestations, adaptations, filename-drift policies, final providers or target rows.
- A bounded review set now defines 16 evidence requirements across 28 pinned recipe roots and 37 object rows; 36 rows are evidence-collection eligible and `libjpeg.so.62` remains correction-blocked. No build attestation, adaptation, filename drift or provider authority is accepted.
- The next active task is bounded collection of build-attestation and adaptation evidence according to those root/object work units.

## Current authority

```text
main/docs/system-foundation/01-essence.md
main/docs/system-foundation/02-principles-and-invariants.md
main/docs/system-foundation/03-system-model-v2.md
main/docs/system-foundation/05-ideal-target-architecture.md
main/docs/system-foundation/11-architecture-reassessment-and-hard-refactor-decision.md
main/docs/system-foundation/12-document-consistency-audit-and-execution-order.md

docs/refactor/0112-selected-obsidian-passive-map-selection-diagnostic-pass-and-contract-decision.md
docs/refactor/0115-proot-oracle-supply-and-baseline-model.md
docs/refactor/0116-end-to-end-architecture-audit-and-provider-authority-intervention.md
docs/refactor/0133-selected-obsidian-priority-provider-authority-review.md
docs/refactor/0134-selected-obsidian-provider-profile-locked-member-draft.md
docs/refactor/0135-selected-obsidian-provider-profile-lock-draft-architecture-audit.md
docs/refactor/0136-selected-obsidian-provider-authority-coverage-and-lock-semantics-normalization.md
docs/refactor/0137-selected-obsidian-world-internals-locale-and-loader-lifecycle-boundary.md
docs/refactor/0138-selected-obsidian-application-payload-launcher-and-supplement-authority-boundary.md
docs/refactor/0139-selected-obsidian-non-priority-generic-source-authority-boundary.md
docs/refactor/0140-selected-obsidian-non-priority-generic-exact-candidate-evidence-collector.md
docs/refactor/0141-selected-obsidian-non-priority-generic-exact-candidate-receipt-review.md
docs/refactor/0142-selected-obsidian-non-priority-generic-artifact-member-comparison-set.md
docs/refactor/0143-selected-obsidian-non-priority-generic-artifact-member-inventory-collector.md
docs/refactor/0144-selected-obsidian-non-priority-generic-artifact-member-inventory-receipt-review.md
docs/refactor/0145-selected-obsidian-generic-recipe-binding-and-drift-target-elf-review.md
docs/refactor/0146-selected-obsidian-generic-recipe-binding-and-drift-target-elf-receipt-review.md
docs/refactor/0147-selected-obsidian-generic-build-attestation-and-adaptation-review-set.md
```

`0116` remains the controlling intervention. `0135` supplies the correction requirements. `0136` records P0-P6 normalization. `0137` accepts the non-materializing world/locale/loader lifecycle boundary. `0138` accepts the non-materializing application identity/launcher lifecycle boundary while keeping exact payload supply, supplement membership, composition and population open. `0139` bounds non-priority generic capability/source classes. `0140` defines the canonical 61-row candidate-search contract and a non-mutating retained-evidence collector. `0141` reviews the exact receipt into direct-family, indirect-only and absent classes while accepting no provider authority. `0142` defines the exact 34-artifact/44-edge member-inventory comparison set and explicit static/development exclusions without downloading or extracting artifacts. `0143` implements bounded exact-artifact acquisition and stream-only member inventory. `0144` reviews the exact device receipt into 21 exact member+SONAME observations, 15 expected-SONAME-alias concrete-filename drifts, and one expected-alias absence while accepting no provider authority. `0145` defines a cache-only collector that verifies 37 pinned recipe family/version/tree candidates and stream-inspects the 15 drift-target ELFs while keeping build attestation and adaptation acceptance open. `0146` reviews the resulting receipt as 37 lineage candidates, 21 exact-member candidates, 15 SONAME-confirmed drift-target candidates and one unsatisfied `libjpeg.so.62` row; it accepts no build attestation, adaptation, filename-drift policy, final provider or target population. `0147` defines 16 explicit evidence requirements and deterministic work units for 28 roots/37 objects while keeping every acceptance and target row open.

## Accepted states

```text
PRIORITY_PROVIDER_EVIDENCE_PASS_BOUNDED
EXACT_ARTIFACT_MEMBER_SUPPLY_STRONG_PASS
PACKAGE_WIDE_RUNTIME_REJECTION_PASS
GLOBAL_IDENTITY_COVERAGE_NORMALIZATION_PASS
CANONICAL_SUPPLY_OBJECT_FRAGMENT_REGISTRY_PASS
ARTIFACT_ALIAS_CLASSIFICATION_PASS
TARGET_LAYOUT_SCHEMA_ONLY_PASS
WORLD_LOCALE_LOADER_LIFECYCLE_BOUNDARY_PASS
APPLICATION_PAYLOAD_LAUNCHER_SUPPLEMENT_BOUNDARY_PASS_BOUNDED
NON_PRIORITY_GENERIC_SOURCE_CLASS_BOUNDARY_PASS_BOUNDED
GENERIC_EXACT_CANDIDATE_COLLECTOR_READY
GENERIC_EXACT_CANDIDATE_RECEIPT_REVIEW_PASS_BOUNDED
GENERIC_ARTIFACT_MEMBER_COMPARISON_SET_DEFINED_BOUNDED
GENERIC_ARTIFACT_MEMBER_INVENTORY_COLLECTOR_PASS_BOUNDED
GENERIC_ARTIFACT_MEMBER_INVENTORY_RECEIPT_REVIEW_PASS_BOUNDED
GENERIC_RECIPE_BINDING_AND_DRIFT_TARGET_ELF_COLLECTOR_PASS_BOUNDED
GENERIC_RECIPE_BINDING_AND_DRIFT_TARGET_ELF_RECEIPT_REVIEW_PASS_BOUNDED
GENERIC_BUILD_ATTESTATION_ADAPTATION_REVIEW_SET_DEFINED_BOUNDED
SEMANTIC_FINAL_PROVIDER_AUTHORITY_OPEN
APPLICATION_RUNTIME_COMPOSITION_NOT_REACHED
TARGET_LAYOUT_POPULATION_BLOCKED
EXTRACTION_MATERIALIZER_BLOCKED
SUCCESSOR_MATERIALIZATION_BLOCKED
CURRENT_ACTIVATION_BLOCKED
```

## Normalized products

```text
experiments/glibc/selected-obsidian-provider-authority/review/
    authority-coverage-ledger.tsv
    authority-coverage-ledger/*.tsv
    non-priority-generic-authority-ledger.tsv
    non-priority-generic-authority-ledger/*.tsv
    normalization-codebook.tsv
    world-lifecycle-authority-boundary.tsv
    application-authority-boundary.tsv
    generic-source-authority-boundary.tsv
    generic-exact-candidate-search-tokens.tsv
    generic-exact-candidate-review-rules.tsv
    generic-exact-candidate-receipt-review.tsv
    generic-exact-candidate-receipt-metadata.tsv
    generic-artifact-member-comparison-artifacts.tsv
    generic-artifact-member-comparison-edges.tsv
    generic-artifact-member-comparison-exclusions.tsv
    generic-artifact-member-comparison-metadata.tsv
    generic-artifact-member-inventory-review-rules.tsv
    generic-artifact-member-inventory-receipt-review.tsv
    generic-artifact-member-inventory-receipt-metadata.tsv
    generic-recipe-binding-and-drift-target-rules.tsv
    generic-recipe-binding-and-drift-target-metadata.tsv
    generic-recipe-binding-and-drift-target-receipt-review-rules.tsv
    generic-recipe-binding-and-drift-target-receipt-review.tsv
    generic-recipe-binding-and-drift-target-receipt-metadata.tsv
    generic-build-attestation-adaptation-review-requirements.tsv
    generic-build-attestation-adaptation-root-review-set.tsv
    generic-build-attestation-adaptation-object-review-set.tsv
    generic-build-attestation-adaptation-review-set-metadata.tsv
    unresolved-authority-ledger.tsv

experiments/glibc/selected-obsidian-provider-authority/profiles/
    supply-repository-metadata-registry.tsv
    supply-artifact-registry.tsv
    provider-object-registry.tsv
    provider-object-registry/*.tsv
    provider-fragment-registry.tsv
    provider-fragment-memberships.tsv
    runtime-alias-authority.tsv
    runtime-alias-authority/*.tsv
    target-layout-schema.tsv
    target-layout-invariants.md
```

Large registries use hash-locked root indexes and partitions. The historical `profiles/member-locks/*.tsv` files are bounded supply evidence only and are not materializer inputs.

## Open authority groups

```text
AUTH-001 world clean reconstruction, acquisition, named internals and successor validation
AUTH-002 optional Termux exec necessity
AUTH-003 GTK/GLib/font/device/Wayland provider composition
AUTH-004 printing capability/provider
AUTH-005 graphics/X11/XCB provider composition
AUTH-006 libwayland artifact-to-recipe binding
AUTH-007 supply/alias/target population contract
AUTH-008 remaining data capabilities; locale/loader lifecycle bounded
AUTH-009 non-priority generic capabilities; bounded local evidence collector implemented for 16 requirements and 28-root/37-object work units; external build provenance, semantic/policy review, libjpeg.so.62 correction and all acceptance/final binding decisions remain open
AUTH-010 exact application payload supply, named supplement membership and release execution; launcher source boundary bounded
```

## Next valid state

```text
CLOSE_GLOBAL_WORLD_APPLICATION_GENERIC_AND_DATA_AUTHORITY_GAPS
```

Active repository task:

```text
RUN_BOUNDED_GENERIC_BUILD_ATTESTATION_AND_ADAPTATION_EVIDENCE_COLLECTOR
```

Repository-side order:

```text
1. world runtime internals, locale and loader-state lifecycle boundary: PASS / remaining evidence explicit;
2. application identity/launcher lifecycle boundary: PASS / exact payload supply and named supplement membership OPEN;
3. non-priority generic capability/source-class boundary: PASS / 16-requirement, 28-root and 37-object review set DEFINED; bounded local evidence collector IMPLEMENTED, with production receipt collection NEXT and libjpeg.so.62 correction still blocked;
4. decide graphics, GTK/Wayland, printing and optional-exec composition policy only after owning candidate sets are explicit;
5. close font, pixbuf, icon, MIME and generated-schema authority;
6. define an ApplicationRuntimeComposition only after owning authorities are accepted;
7. populate target-layout rows only after composition acceptance;
8. perform an intervention-lift audit before any extraction/materializer implementation.
```

## Stop lines

Do not:

```text
treat 59/59 as global authority completion;
call the 96 first-generation contents application-local payload;
treat exact Termux supply as automatic final generic/platform authority;
consume provider fragments or historical member locks as deployable profiles;
populate target paths, modes, owners or aliases;
copy linker/development aliases into a runtime target;
treat artifact path/mode/uid/gid as target policy;
write an extraction or materializer script;
install, remove, upgrade or downgrade packages;
run package maintainer scripts;
materialize or activate a successor;
create or modify current;
mutate the promoted launcher or loader state;
patch RPATH;
reopen closed graphics gates.
```

## Evidence policy

Prototype validity, oracle validity, exact supply identity, semantic role, platform adaptation, candidate-source comparison, artifact-to-recipe binding, profile necessity, alias necessity, application composition, target ownership, materialization, activation, rollback, and clean reconstruction are separate claims.
