# Status

> **State:** selected-Obsidian priority provider-authority review PARTIAL PASS; exact provider-profile/member-lock draft PASS; base-profile gaps and target/extraction contract are next; materialization and activation remain blocked  
> **Updated:** 2026-07-12

## Working conclusions

- **The project remains architecturally on track.** Existing prototype, ownership, ABI, graphics, selected-generation, passive-runtime, N2, corrected N3, source-recipe, and exact binary-artifact evidence remain valid.
- **The existing selected generation remains immutable and unactivated.** `current` is absent and the promoted launcher is unchanged.
- **Priority provider authority is now object-scoped.** All 28 priority packages and all 59 priority selected/reference objects have dispositions; package membership is not runtime authority.
- **Twenty-nine reviewed objects are base-profile authorities.** Thirty are conditional graphics, GTK/font/device/Wayland, printing, or optional-platform objects.
- **Termux-adapted `glibc 2.42` is the accepted native world authority for the reviewed world set.** Clean reconstruction, update, rollback, loader-state ownership, runtime-internal modules, and 2.42→2.43 revalidation remain open.
- **Selected X11/XCB objects have object-scoped platform authority.** The whole package surfaces are not admitted.
- **`glibc-runner` is research/build/maintenance tooling and is rejected from the promoted runtime.**
- **`termux-exec-glibc` is an accepted optional platform provider, not proven minimum-runtime content.**
- **Exact binary supply identity remains established.** Twenty-eight exact indexed `.deb` artifacts totaling 42,864,296 bytes match the installed package-owned filesystem with zero member mismatches.
- **Provider profiles now have exact artifact-member locks.** Fifty-nine unique reviewed objects produce 63 profile content memberships, 93 required symlink aliases, 156 total member-lock rows, and 35 profile/package artifact locks.
- **Six profiles are defined:** selected world, base Obsidian X11, conditional Freedreno graphics, conditional GTK/font/device compatibility, conditional printing, and optional Termux exec integration.
- **All profile locks are non-materializing drafts.** Every member row is `DRAFT_LOCK_ONLY_BLOCKED`; every profile has `materialization_authorized=NO`.
- **`artifact_member_path` is immutable supply identity.** `installed_source_path` is historical evidence only and cannot define a future target path.
- **The base runtime is not complete.** It still lacks application-local composition, font authority, pixbuf/icon/MIME authority, loader-state lifecycle, complete world internals, and explicit conditional-profile choices.
- **Storage policy remains:** internal source/cache/unpacked/temp state uses Termux-private or ignored `work/`; only explicit handoff exports use `$HOME/Downloads`.

## Architecture authority

```text
main/docs/system-foundation/01-essence.md
main/docs/system-foundation/02-principles-and-invariants.md
main/docs/system-foundation/03-system-model-v2.md
main/docs/system-foundation/05-ideal-target-architecture.md
main/docs/system-foundation/11-architecture-reassessment-and-hard-refactor-decision.md
main/docs/system-foundation/12-document-consistency-audit-and-execution-order.md

docs/refactor/0112-selected-obsidian-passive-map-selection-diagnostic-pass-and-contract-decision.md
docs/refactor/0113-clean-state-minimum-condition-and-supply-authority-audit.md
docs/refactor/0114-debian-baseline-correction-native-font-pressure-and-auditor-boundary.md
docs/refactor/0115-proot-oracle-supply-and-baseline-model.md
docs/refactor/0116-end-to-end-architecture-audit-and-provider-authority-intervention.md
docs/refactor/0117-provider-authority-intervention-adoption-and-execution-order.md
docs/refactor/0118-selected-obsidian-provider-authority-census-schema-and-evidence-plan.md
docs/refactor/0119-selected-obsidian-provider-authority-n2-read-only-evidence-collector.md
docs/refactor/0120-selected-obsidian-provider-authority-n2-device-receipt-review.md
docs/refactor/0123-selected-obsidian-provider-authority-corrected-n3-receipt-pass-and-source-comparison-entry.md
docs/refactor/0128-selected-obsidian-provider-authority-source-recipe-receipt-pass.md
docs/refactor/0131-selected-obsidian-provider-authority-binary-artifact-receipt-pass.md
docs/refactor/0132-evidence-storage-and-android-downloads-handoff-boundary.md
docs/refactor/0133-selected-obsidian-priority-provider-authority-review.md
docs/refactor/0134-selected-obsidian-provider-profile-locked-member-draft.md
```

`0116` remains the end-to-end intervention authority. `0133` accepts object-scoped priority authority only; `0134` locks exact supply members without authorizing target layout or materialization.

## Accepted receipt identities

```text
corrected N3:
    4dd86c4af956b447ed1829d6b5d604f43d10a17e5b3dcb3ddff3e9b48c377a9c

source recipe:
    c8160016267f3ff83b348146240f74f808ffbc93374a6f75988231ef22408cdb

binary artifact:
    da16d49acf54cbc8b6824e3974f08fea9ad0d6daf91687f4666d6c48d0b7567f
```

## Current review products

```text
experiments/glibc/selected-obsidian-provider-authority/review/
    package-authority-t0.tsv
    package-authority-t1.tsv
    selected-object-authority-base.tsv
    selected-object-authority-conditional.tsv
    unresolved-authority-ledger.tsv

experiments/glibc/selected-obsidian-provider-authority/profiles/
    README.md
    provider-profile-definitions.tsv
    provider-profile-artifact-locks.tsv
    member-locks/*.tsv
```

## Open authority groups

```text
AUTH-001 world reconstruction/update/rollback
AUTH-002 termux-exec minimum-profile necessity
AUTH-003 GTK/font/device/Wayland provider composition
AUTH-004 printing capability/provider requirement
AUTH-005 graphics provider/update contract
AUTH-006 libwayland source-tree binding
AUTH-007 extraction and target-layout contract
AUTH-008 fonts, pixbuf/icons/MIME and loader-state authority
```

## Next valid state

```text
CLOSE_BASE_PROVIDER_PROFILE_GAPS_AND_DEFINE_EXTRACTION_TARGET_CONTRACT
```

Required repository-side work:

```text
define target-domain and target-path rules independently from installed paths;
close world runtime-internal and loader-state ownership;
incorporate the 96 application-local generation identities and application supply identity;
resolve font and pixbuf/icon/MIME authority;
choose inclusion policy for graphics, GTK/Wayland, printing, and optional exec profiles;
define exact-artifact extraction verification without package installation or maintainer scripts.
```

## Stop lines

Do not:

```text
materialize or activate a successor
create or modify current
install, remove, upgrade, or downgrade packages
run package maintainer scripts
mutate ld.so.conf or ld.so.cache
patch RPATH
copy package-wide surfaces from object-scoped authority
use installed absolute paths as target authority
promote conditional profiles into the base by availability
reopen closed graphics gates
```

## Evidence policy

Prototype validity, oracle validity, package-source provenance, exact binary supply identity, semantic provider authority, profile inclusion, target ownership, runtime composition, materialization, activation, rollback, and clean reconstruction are separate claims.
