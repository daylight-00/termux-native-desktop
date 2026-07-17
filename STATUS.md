# Status

bundle-native documentation and operations control planes active; ADR 0005 claim classification complete; exact FreeType and bounded compression closure accepted for Pango/GTK font processing; selected-provider composition incomplete with 14 gaps; libxkbcommon review active
> **Updated:** 2026-07-17

## Repository and deployment consolidation

- `main` is the sole intended long-lived branch.
- The system-foundation history and the active implementation/evidence history are integrated by a history-preserving merge.
- Topic branches are deleted only after their tips are verified as ancestors of the pushed `main`.
- Direct checkout-to-live symlinks are superseded by immutable materialized repository releases and a stable atomic `current` pointer.
- `tools/deploy --profile workstation|full` owns managed public leaves; external payloads, selected generations, provider installs, build trees and user state remain outside this cleanup transaction.
- The provider-authority corpus is classified under ADR 0005: 89 separated claims and 28 historical SUP-02 requests reclassified as 14 narrowed, 7 replaced and 7 unnecessary. Seventeen root provider claims inside the 28-root inventory are accepted: four X.Org roots for bounded selected GTK X11 scope, libtasn1 for bounded external GnuTLS 3.8.9 ASN.1/security scope, libepoxy for bounded GTK 3.24.49 X11 GLX dispatch, the exact three-member Pango 1.54.0 family for bounded GTK text scope, the project-built libjpeg.so.62 provider for GdkPixbuf JPEG decoding, exact GLib/libpng providers, the exact util-linux libmount/libblkid pair, exact libXcursor, and exact libthai/libdatrie for Pango 1.54.0 Thai breaking, exact libcloudproviders for GTK 3.24.49 PlacesSidebar cloud-account integration, exact FriBidi for Pango 1.54.0 core Unicode bidirectional processing, and exact FreeType for bounded Pango/GTK font processing. The project-built GdkPixbuf root plus exact transitive libiconv, brotli, libbz2, and zlib provider roots are accepted separately outside that inventory. No complete composition, target row or activation is accepted.
- OJ-001 produced a corrected exact scratch-built `libjpeg.so.62.4.0` AArch64 candidate with SHA-256 `a537840ef9da6135cb3284bc3b3e0d1fb4f624180a416c2a3964b94714eb7fe5`, `DT_SONAME=libjpeg.so.62`, expected symbol versions and no `DT_RPATH`/`DT_RUNPATH`. The loader-isolated six-cell matrix passed completely: candidate and Debian oracle direct `djpeg` controls produced the same output digest, and candidate/oracle GdkPixbuf file and memory paths all reached completion with exact mapped-provider proof. The exact project candidate now has bounded provider authority for selected GdkPixbuf 2.42.12 JPEG file and memory decode only; composition, target population and activation remain open.
- The selected-provider composition review now records 29 exact accepted members, includes 28 in the selected GTK/transitive scope, defers libtasn1 until a GnuTLS/security profile is selected, finds zero accepted-member SONAME or alias collisions, and identifies 14 unresolved selected GTK identities. The exact `libXcursor.so.1.0.2` member is accepted only for GTK 3.24.49 X11 cursor theme/image/surface handling. The Class D composition decision remains `REVIEWED_BLOCKED_INCOMPLETE`; target-manifest generation, population and activation remain blocked while the next exact libxkbcommon provider and filename-continuity tranche is reviewed.
- The official-source GdkPixbuf 2.42.12 scratch build produced exact `libgdk_pixbuf-2.0.so.0.4200.12` SHA-256 `0c1404c...`, removed its build-tree search path, and passed JPEG/PNG file and memory decoding. Exact Termux GLib 2.82.2-2 four-member and libpng 1.6.47 shared-library providers are accepted only for that fixed JPEG/PNG file and memory scope. The official exact libmount/libblkid pair mapped successfully and the four-cell matrix passed, so those two members now have bounded transitive provider authority; tracked repository state and live glibc/provider paths were unchanged.

See `docs/decisions/0004-single-main-and-immutable-release-deployment.md`.

## Documentation and web-session control plane

- A new web-chat session receives a user-created full Git bundle from authoritative Termux `main`, clones it in the sandbox and starts at `START_HERE.md`.
- `docs/current/` owns compact current state, the active task and pending external artifacts.
- Narrative handoffs and numbered refactor records are historical evidence, not default onboarding authority.
- The GitHub connector is limited to lightweight remote inspection; user Termux local Git/`gh` is authoritative for remote mutation.
- Repository state transitions update canonical current documents when accepted rather than deferring maintenance to session close.
- `docs/operations/` is the single current authority for collaboration, bundle transport, execution, result review, optional checkpoints, troubleshooting, and platform capability boundaries.
- The former `docs/session-operations/` surface and narrative handoffs are historical only.
- Docker is outside the available and intended workflow.
- Google Drive is the primary outbound exchange path. A runtime-initialization first-upload file-reference block falls back to a user-visible file only for that delivery; the next outbound upload attempts Drive first again.

## Local-layout consolidation

- The historical `$HOME/gl/.git` repository authority is retired and preserved in safety artifacts.
- Mesa mutable source/build state lives under `${XDG_STATE_HOME:-$HOME/.local/state}/termux-native-desktop/workspaces/mesa/`.
- Mesa provider candidates and the canonical provider `current` pointer live under `${XDG_STATE_HOME:-$HOME/.local/state}/termux-native-desktop/providers/mesa/`.
- Legacy `$HOME/gl/build` and `$HOME/gl/opt` paths remain compatibility symlinks only.
- Application bodies, selected generations, user data and provider contents were preserved.

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
- A bounded review set defines 16 evidence requirements across 28 pinned recipe roots and 37 object rows; 36 rows are evidence-collection eligible and `libjpeg.so.62` remains correction-blocked.
- The production receipt reverified 34 artifacts, inventoried 84 recipe files and 74 bounded script signals, recorded 37 root/object links, and confirmed 21 exact-member plus 15 alias-target output observations without package mutation, extraction or network acquisition.
- Receipt review accepts six local evidence dimensions only as bounded review inputs and confirms ten external, semantic, continuity-policy, consumer-binding or object-correction gaps. Build attestations, adaptations, filename drifts, final providers and target rows accepted remain zero.
- Six deterministic closure lanes now map all 16 requirements: object correction, digest-bound provenance, output-to-build linkage, adaptation semantic review, consumer binding, and successor/rollback continuity policy.
- The 28 pinned roots and 37 named objects now have explicit requirement dependencies and completion gates; no new evidence or authority was accepted.
- A bounded gap-closure collector enforces a strict manifest for optional candidate evidence and emits one collection state for every requirement, lane, root, and object.
- The production collector run found no candidate-evidence root and correctly emitted zero candidate files, six local-foundation-only requirements and ten explicit unavailable gaps.
- Receipt review confirms all six lanes, sixteen requirements, twenty-eight roots and thirty-seven objects remain incomplete, with zero build-attestation, adaptation, filename-drift, object-correction, provider or target acceptance.
- Ten source contracts now distinguish authoritative references, immutable/signed build provenance, independent reproduction, output manifests, pinned upstream baselines, semantic reviews, consumer/loader evidence and continuity policies.
- All 16 requirements now have deterministic acquisition modes, manifest scopes, deliverable contracts and integrity bindings; 28 root rows contain 303 requirement edges and 37 object rows contain 414 requirement edges.
- This transaction acquired zero candidate files and accepted no correction, build attestation, adaptation, filename drift, provider or target row.
- A bounded input-only acquirer now rejects unmanifested or contract-mismatched files and emits a deterministic strict-manifest evidence root with post-copy digest verification.
- Missing acquisition input is recorded as six local-foundation-only requirements plus ten explicit unavailable direct gaps; it is neither failure nor closure.
- The production acquirer receipt contains zero candidates, six local-foundation-only requirements and ten explicit unavailable direct gaps; all six lanes, twenty-eight roots and thirty-seven objects remain open.
- Receipt review confirms the strict evidence manifest is header-only and every build-attestation, adaptation, filename-drift, correction, provider and target counter remains zero.
- Six bounded supply batches now assign all sixteen requirements to explicit supplier roles, transport boundaries, deliverables and response paths.
- Fourteen dependency components are explicit; `CF-002`, `CF-003` and `CF-004` form the sole cyclic component and require fixed-point iteration rather than a false linear order.
- The first active response batch is `SUP-01` for the isolated P0 `OJ-001` authoritative libjpeg requirement correction.
- The bounded `SUP-01` response corrects the requirement model from provider-versioned concrete filename `libjpeg.so.62.3.0` to stable SONAME `libjpeg.so.62`.
- Upstream defines `WITH_JPEG8=ON` as backward-incompatible with the v6b ABI and maps it to SOVERSION 8; the selected Termux `libjpeg.so.8` family is therefore rejected as a substitute.
- The `SUP-01` response review accepts the requirement correction from provider-versioned concrete filename `libjpeg.so.62.3.0` to stable SONAME `libjpeg.so.62`.
- `OJ-001` is closed by required-identity correction under its disjunctive completion gate; the selected `WITH_JPEG8=ON` artifact remains a rejected SONAME-8 family and no matching SONAME-62 provider is bound.
- Accepted object-requirement corrections now total one; build attestations, adaptations, filename-drift policies, final providers and target rows accepted remain zero.
- The next active batch is `SUP-02` for digest-bound producing-build invocation, immutable environment and output linkage covering `BA-001`, `BA-002` and `BA-003`.
- A bounded SUP-02 locator now checks explicit custodian-export roots for `build-invocation-record.json`, `build-environment-record.json` and `build-output-manifest.tsv` across all 28 roots.
- GitHub repository, workflow and release metadata are retained only as locator surfaces; zero build attestations, providers or target rows are accepted.
- The production SUP-02 locator receipt contains zero complete exports, zero partial exports, twenty-eight absent exports and zero record files.
- Receipt review accepts that absence only as explicit gap evidence: `BA-001`, `BA-002` and `BA-003` remain open and no producing-build provenance is inferred.
- Repeating the same empty locator is rejected; the next transaction defines exact per-root custodian export requests for one-build invocation, environment and output linkage.
- The SUP-02 custodian-export request set now defines 28 exact root requests and 84 record contracts: one invocation, one immutable environment and one output manifest per root, all cross-linked by one build-run identity.
- The 28 exact requests are now repository-published with 84 issued record contracts; all remain `NOT_ACKNOWLEDGED`, responses and build-attestation acceptance remain zero, and publication does not imply custodian receipt.
- A strict SUP-02 response acquirer now verifies exact request/root/recipe coordinates, manifest-to-file equality, three mandatory records, record digests and one-build cross-record identity before emitting candidate review input.
- Absent response drops are explicit non-failures; malformed, partial, unknown, unmanifested or cross-build responses are rejected, and acquisition accepts no build attestation, provider or target row.
- The production response-acquisition receipt records an absent input root, zero complete candidate responses, twenty-eight explicit no-response states and zero verified response records.
- Receipt review accepts only that no response was staged at the bounded surface; all requests remain unacknowledged and repeating the same empty acquisition is non-progress.
- A strict custodian-side producer now executes the actual build command only after exact request and recipe-tree verification, captures bounded invocation, input, environment, toolchain and package-member records, and emits an `0163`-compatible candidate response.
- Producer implementation is not request execution: canonical responses, acknowledgements, build-attestation acceptance, provider decisions and target population remain zero.
- The ADR 0005 classification now separates 28 artifact-identity claims, 28 adaptation claims, 28 provider-authority claims, OJ-001, conditional build provenance, composition, target population and activation into 89 rows.
- Class distribution is 36 A, 49 B, 1 conditional C and 3 D; the Class C producing-build claim is deferred because no root is currently classified as independently reproduced.
- All 28 SUP-02 requests remain historical: 14 are narrowed to claim-specific escalation only, 7 are replaced by reference/artifact/semantic integration evidence, and 7 are unnecessary at the current boundary. Zero requests are required now.
- All seven no-token roots have completed exact pinned-recipe semantic review as Class A and bounded provider review. Four X.Org roots cover selected GTK 3.24.49 X11 features, `libtasn1` covers external GnuTLS 3.8.9 ASN.1/security, `libepoxy` covers GTK X11 GLX dispatch, and the exact Pango 1.54.0 three-member family covers selected GTK text/FreeType/Fontconfig/Cairo capability. Pango CF-001–CF-004 define SONAME alias necessity, bounded successor selection, immutable update review and atomic family rollback. Complete composition, target population and activation remain blocked.
- The OJ-001 provider-candidate review found no exact repository SONAME-62 artifact, keeps the SONAME-8 family rejected, and requires a scratch-built libjpeg-turbo 3.1.0 v6b compatibility candidate with expected member `libjpeg.so.62.4.0`; no provider or target authority is accepted.

## Current authority

```text
main/docs/constitution/PROJECT.md
main/docs/constitution/PRINCIPLES.md
main/AGENTS.md

historical design provenance:
main/docs/system-foundation/README.md

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
docs/refactor/0148-selected-obsidian-generic-build-attestation-and-adaptation-evidence-collector.md
docs/refactor/0149-selected-obsidian-generic-build-attestation-and-adaptation-evidence-receipt-review.md
docs/refactor/0150-selected-obsidian-generic-build-attestation-and-adaptation-gap-closure-set.md
docs/refactor/0151-selected-obsidian-generic-build-attestation-and-adaptation-gap-closure-collector.md
docs/refactor/0152-selected-obsidian-generic-build-attestation-and-adaptation-gap-closure-receipt-review.md
docs/refactor/0153-selected-obsidian-generic-build-attestation-and-adaptation-gap-evidence-acquisition-set.md
docs/refactor/0154-selected-obsidian-generic-build-attestation-and-adaptation-gap-evidence-acquirer.md
docs/refactor/0155-selected-obsidian-generic-build-attestation-and-adaptation-gap-evidence-acquisition-receipt-review.md
docs/refactor/0156-selected-obsidian-generic-build-attestation-and-adaptation-gap-evidence-supply-request-set.md
docs/refactor/0157-selected-obsidian-generic-build-attestation-and-adaptation-gap-evidence-supply-batch-sup-01-response.md
docs/refactor/0158-selected-obsidian-generic-build-attestation-and-adaptation-gap-evidence-supply-batch-sup-01-response-review.md
docs/refactor/0159-selected-obsidian-generic-build-attestation-and-adaptation-gap-evidence-supply-batch-sup-02-provenance-locator.md
docs/refactor/0160-selected-obsidian-generic-build-attestation-and-adaptation-gap-evidence-supply-batch-sup-02-provenance-locator-receipt-review.md
docs/refactor/0161-selected-obsidian-generic-build-attestation-and-adaptation-gap-evidence-supply-batch-sup-02-custodian-export-request-set.md
docs/refactor/0162-selected-obsidian-generic-build-attestation-and-adaptation-gap-evidence-supply-batch-sup-02-custodian-export-request-issuance.md
docs/refactor/0163-selected-obsidian-generic-build-attestation-and-adaptation-gap-evidence-supply-batch-sup-02-custodian-export-response-acquirer.md
docs/refactor/0164-selected-obsidian-generic-build-attestation-and-adaptation-gap-evidence-supply-batch-sup-02-custodian-export-response-acquisition-receipt-review.md
docs/refactor/0165-selected-obsidian-generic-build-attestation-and-adaptation-gap-evidence-supply-batch-sup-02-custodian-export-response-producer.md
```

`0116` remains the controlling intervention. `0135` supplies the correction requirements. `0136` records P0-P6 normalization. `0137` accepts the non-materializing world/locale/loader lifecycle boundary. `0138` accepts the non-materializing application identity/launcher lifecycle boundary while keeping exact payload supply, supplement membership, composition and population open. `0139` bounds non-priority generic capability/source classes. `0140` defines the canonical 61-row candidate-search contract and a non-mutating retained-evidence collector. `0141` reviews the exact receipt into direct-family, indirect-only and absent classes while accepting no provider authority. `0142` defines the exact 34-artifact/44-edge member-inventory comparison set and explicit static/development exclusions without downloading or extracting artifacts. `0143` implements bounded exact-artifact acquisition and stream-only member inventory. `0144` reviews the exact device receipt into 21 exact member+SONAME observations, 15 expected-SONAME-alias concrete-filename drifts, and one expected-alias absence while accepting no provider authority. `0145` defines a cache-only collector that verifies 37 pinned recipe family/version/tree candidates and stream-inspects the 15 drift-target ELFs while keeping build attestation and adaptation acceptance open. `0146` reviews the resulting receipt as 37 lineage candidates, 21 exact-member candidates, 15 SONAME-confirmed drift-target candidates and one unsatisfied `libjpeg.so.62` row; it accepts no build attestation, adaptation, filename-drift policy, final provider or target population. `0147` defines 16 explicit evidence requirements and deterministic work units for 28 roots/37 objects while keeping every acceptance and target row open. `0148` implements and runs bounded local evidence collection without build, package mutation, extraction or network acquisition. `0149` reviews the resulting receipt into six confirmed local review-input dimensions and ten explicit provenance/semantic/policy/correction gaps while accepting no authority or target population. `0150` maps those requirements into six ordered closure lanes. `0151` implements a strict-manifest, read-only collector that records verified candidate files or explicit unavailable gaps without accepting any closure or authority claim. `0152` reviews the production no-candidate receipt as six incomplete local foundations plus ten explicit gaps and accepts no closure, authority or target claim. `0153` defines ten source contracts and deterministic acquisition work units for all six lanes, sixteen requirements, twenty-eight roots and thirty-seven objects without acquiring evidence. `0154` implements a bounded input-only acquirer that validates exact source-contract modes, locator classes, scopes, units, digests and file-set equality before emitting an `0151`-compatible candidate evidence root with zero authority effect. `0155` reviews the production no-input receipt as zero candidates, six incomplete local foundations and ten explicit unavailable direct gaps, with every authority and target decision still open. `0156` defines six bounded supply batches, one exact request for each of the sixteen requirements, fourteen dependency components and exact request fan-out across twenty-eight root and thirty-seven object units without issuing a request or accepting evidence. `0157` prepares the isolated `SUP-01` authoritative correction response: stable required SONAME `libjpeg.so.62`, no `libjpeg.so.8` substitution, no matching provider candidate bound and no authority effect. `0158` reviews that response, accepts the narrow OJ-001 required-identity correction, keeps the SONAME-8 family rejected and advances to SUP-02 without accepting provider authority or target population. `0159` implements a bounded operator-local provenance locator for exact producing-build invocation, environment and output-manifest exports while treating GitHub metadata as locator-only. `0160` reviews the production locator receipt as twenty-eight absent custodian exports and zero records, preserves all three build-provenance requirements as open, and requires an exact custodian-export request set. `0161` defines that request set as twenty-eight root-scoped requests and eighty-four cross-linked record contracts without issuing a request or accepting evidence. `0162` publishes the exact request packets through the canonical repository transport, records twenty-eight issued-but-unacknowledged requests and preserves zero response, attestation, provider and target effects. `0163` implements the strict input-only response acquirer, validates complete three-record one-build bindings, records absent drops explicitly and emits candidate response input without acceptance effect. `0164` reviews the production zero-response receipt, confirms all twenty-eight requests remain outstanding, accepts no attestation or authority effect, and requires exact custodian response fulfillment before any further batch progression.

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
GENERIC_BUILD_ATTESTATION_ADAPTATION_EVIDENCE_COLLECTOR_PASS_BOUNDED
GENERIC_BUILD_ATTESTATION_ADAPTATION_EVIDENCE_RECEIPT_REVIEW_PASS_BOUNDED
GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_CLOSURE_SET_DEFINED_BOUNDED
GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_CLOSURE_COLLECTOR_IMPLEMENTED_BOUNDED
GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_CLOSURE_RECEIPT_REVIEW_PASS_BOUNDED
GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_ACQUISITION_SET_DEFINED_BOUNDED
GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_ACQUIRER_IMPLEMENTED_BOUNDED
GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_ACQUISITION_RECEIPT_REVIEW_PASS_BOUNDED
GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_SUPPLY_REQUEST_SET_DEFINED_BOUNDED
GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_SUPPLY_BATCH_SUP_01_RESPONSE_PREPARED_BOUNDED
GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_SUPPLY_BATCH_SUP_01_RESPONSE_REVIEW_PASS_BOUNDED
GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_SUPPLY_BATCH_SUP_02_PROVENANCE_LOCATOR_IMPLEMENTED_BOUNDED
GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_SUPPLY_BATCH_SUP_02_PROVENANCE_LOCATOR_RECEIPT_REVIEW_PASS_BOUNDED
GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_SUPPLY_BATCH_SUP_02_CUSTODIAN_EXPORT_REQUEST_SET_DEFINED_BOUNDED
GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_SUPPLY_BATCH_SUP_02_CUSTODIAN_EXPORT_REQUESTS_ISSUED_BOUNDED
GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_SUPPLY_BATCH_SUP_02_CUSTODIAN_EXPORT_RESPONSE_ACQUIRER_IMPLEMENTED_BOUNDED
GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_SUPPLY_BATCH_SUP_02_CUSTODIAN_EXPORT_RESPONSE_ACQUISITION_RECEIPT_REVIEW_PASS_BOUNDED
GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_SUPPLY_BATCH_SUP_02_CUSTODIAN_EXPORT_RESPONSE_PRODUCER_IMPLEMENTED_BOUNDED
OBJECT_REQUIREMENT_CORRECTION_OJ_001_ACCEPTED_STABLE_SONAME_LIBJPEG_SO_62
LIBJPEG_SO_62_RUNPATH_FREE_CANDIDATE_IDENTITY_ACCEPTED_CONSUMER_VALIDATION_REQUIRED
NO_TOKEN_RECIPE_SEMANTIC_REVIEW_CLASS_A_7
XORG_REFERENCE_CONSUMED_PROVIDER_AUTHORITY_ACCEPTED_BOUNDED_4
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
    generic-build-attestation-adaptation-evidence-receipt-review-rules.tsv
    generic-build-attestation-adaptation-evidence-receipt-review.tsv
    generic-build-attestation-adaptation-root-evidence-receipt-review.tsv
    generic-build-attestation-adaptation-object-evidence-receipt-review.tsv
    generic-build-attestation-adaptation-evidence-receipt-metadata.tsv
    generic-build-attestation-adaptation-gap-closure-lanes.tsv
    generic-build-attestation-adaptation-gap-closure-requirements.tsv
    generic-build-attestation-adaptation-root-gap-closure-set.tsv
    generic-build-attestation-adaptation-object-gap-closure-set.tsv
    generic-build-attestation-adaptation-gap-closure-set-metadata.tsv
    generic-build-attestation-adaptation-gap-closure-receipt-review-rules.tsv
    generic-build-attestation-adaptation-gap-closure-receipt-review.tsv
    generic-build-attestation-adaptation-gap-closure-lane-receipt-review.tsv
    generic-build-attestation-adaptation-root-gap-closure-receipt-review.tsv
    generic-build-attestation-adaptation-object-gap-closure-receipt-review.tsv
    generic-build-attestation-adaptation-gap-closure-receipt-review-metadata.tsv
    generic-build-attestation-adaptation-gap-evidence-source-contracts.tsv
    generic-build-attestation-adaptation-gap-evidence-acquisition-lanes.tsv
    generic-build-attestation-adaptation-gap-evidence-acquisition-requirements.tsv
    generic-build-attestation-adaptation-root-gap-evidence-acquisition-set.tsv
    generic-build-attestation-adaptation-object-gap-evidence-acquisition-set.tsv
    generic-build-attestation-adaptation-gap-evidence-acquisition-set-metadata.tsv
    generic-build-attestation-adaptation-gap-evidence-acquisition-receipt-review-rules.tsv
    generic-build-attestation-adaptation-gap-evidence-acquisition-receipt-review.tsv
    generic-build-attestation-adaptation-gap-evidence-acquisition-lane-receipt-review.tsv
    generic-build-attestation-adaptation-root-gap-evidence-acquisition-receipt-review.tsv
    generic-build-attestation-adaptation-object-gap-evidence-acquisition-receipt-review.tsv
    generic-build-attestation-adaptation-gap-evidence-acquisition-receipt-review-metadata.tsv
    generic-build-attestation-adaptation-gap-evidence-supply-batches.tsv
    generic-build-attestation-adaptation-gap-evidence-supply-requests.tsv
    generic-build-attestation-adaptation-root-gap-evidence-supply-request-set.tsv
    generic-build-attestation-adaptation-object-gap-evidence-supply-request-set.tsv
    generic-build-attestation-adaptation-gap-evidence-supply-request-set-metadata.tsv
    generic-build-attestation-adaptation-gap-evidence-supply-batch-sup-01-response-review-rules.tsv
    generic-build-attestation-adaptation-gap-evidence-supply-batch-sup-01-response-review.tsv
    generic-build-attestation-adaptation-gap-evidence-supply-batch-sup-01-object-review.tsv
    generic-build-attestation-adaptation-gap-evidence-supply-batch-sup-01-response-review-metadata.tsv
    generic-build-attestation-adaptation-gap-evidence-supply-batch-sup-02-custodian-export-response-acquisition-receipt-review-rules.tsv
    generic-build-attestation-adaptation-gap-evidence-supply-batch-sup-02-custodian-export-response-acquisition-receipt-review.tsv
    generic-build-attestation-adaptation-gap-evidence-supply-batch-sup-02-root-custodian-export-response-acquisition-receipt-review.tsv
    generic-build-attestation-adaptation-gap-evidence-supply-batch-sup-02-custodian-export-response-acquisition-receipt-review-metadata.tsv
    unresolved-authority-ledger.tsv

experiments/glibc/selected-obsidian-provider-authority/evidence-supply/requests/SUP-02/custodian-export/
    custodian-export-request-issuance.tsv
    custodian-export-record-contract-issuance.tsv
    custodian-export-request-issuance-metadata.tsv

experiments/glibc/selected-obsidian-provider-authority/evidence-supply/responses/SUP-01/SRQ-OJ-001/
    acquisition-input/acquisition-input-manifest.tsv
    acquisition-input/object-requirement-correction-review.tsv
    response-metadata.tsv

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
AUTH-009 non-priority generic capabilities; OJ-001 required identity, exact runpath-free candidate identity and bounded GdkPixbuf JPEG provider authority are resolved, the 89-row ADR 0005 claim inventory is complete, all 28 SUP-02 requests are historical with zero currently required, seven no-token recipes are Class A, and nine exact providers have bounded authority while composition and remaining provider claims stay open
AUTH-010 exact application payload supply, named supplement membership and release execution; launcher source boundary bounded
```

## Bounded libepoxy provider authority

The exact `libepoxy.so.0.0.0` member is accepted only for the GTK 3.24.49 X11 GLX dispatch capability. X11 and GLX are required and bound; EGL is explicitly not claimed. The supplier build framework remains a relied-upon boundary because the supplier pipeline fetched a floating `termux-packages` master. This decision authorizes no composition, target membership, materialization, or activation.

## Bounded Pango provider authority and filename continuity

The exact Pango 1.54.0 `libpango-1.0.so.0.5400.0`, `libpangoft2-1.0.so.0.5400.0`, and `libpangocairo-1.0.so.0.5400.0` members are accepted as one bounded provider family for selected GTK 3.24.49 text, FreeType/Fontconfig and Cairo capability. The three observed SONAME aliases match the three ELF SONAMEs. The Debian/oracle `5600.3` labels are reference filenames from a different release and are not target-path authority.

CF-001 through CF-004 require SONAME alias continuity, accept the exact 1.54.0 family as the bounded successor, require a new immutable review on update, and roll back all three objects and aliases atomically. No alias is created and no target path, composition, materialization or activation is accepted.

## Web-chat capability fallback contract

Known sandbox, connector, network, filesystem, timeout, context, and device-authority limits are recorded in `docs/operations/platforms/chatgpt-web.md` and the machine-readable `chatgpt-web-limitations.tsv`. The operational rule is one representative probe followed by the registered practical fallback; repeated equivalent attempts are prohibited. Exact bytes blocked by web DNS/egress move to a self-contained user-Termux acquisition/analyzer transaction.

## Next valid state

```text
RERUN_LIBJPEG_SO_62_GDKPIXBUF_WITH_LOADER_ISOLATION
```

Active task:

```text
RERUN_LIBJPEG_SO_62_GDKPIXBUF_WITH_LOADER_ISOLATION
```

Required order:

```text
1. preserve the 89-row claim inventory and the separation between identity, adaptation, provider, composition, target and activation;
2. retain the seven Class A recipe decisions and seven bounded provider rows without broadening their scope;
3. compare the authoritative `libjpeg.so.62` requirement with exact eligible Termux candidates and reject silent SONAME-8 substitution;
4. use one bounded Termux acquisition/analyzer wrapper only if exact repository bytes or ELF identity are unavailable in the web runtime;
5. keep broader reference-adapted provider review and complete composition outside this correction tranche;
6. do not issue SUP-02 without a recorded Class C reclassification or escalation trigger;
7. do not treat a bounded provider or requirement-correction decision as complete application composition, target membership or activation.
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
create or modify the selected-generation current pointer;
mutate the promoted launcher or loader state;
patch RPATH;
reopen closed graphics gates.
```

## Evidence policy

Prototype validity, oracle validity, exact supply identity, semantic role, platform adaptation, candidate-source comparison, artifact-to-recipe binding, profile necessity, alias necessity, application composition, target ownership, materialization, activation, rollback, and clean reconstruction are separate claims.
