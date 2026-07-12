# Selected Obsidian Provider-Authority Census

## Status

```text
N0_REPOSITORY_ONBOARDING_PASS
N1_CENSUS_SCHEMA_AND_EVIDENCE_PLAN_PASS
N2_READ_ONLY_PROVIDER_EVIDENCE_PASS
N3_CORRECTED_NORMALIZED_CLASSIFICATION_PASS
N3_SOURCE_RECIPE_EVIDENCE_PASS
N3_BINARY_ARTIFACT_COMPARISON_PASS
PRIORITY_PROVIDER_AUTHORITY_REVIEW_PARTIAL_PASS
PROVIDER_PROFILE_LOCK_DRAFT_PASS
SUCCESSOR_MANIFEST_BLOCKED
SUCCESSOR_MATERIALIZATION_BLOCKED
CURRENT_ACTIVATION_BLOCKED
```

This workstream implements the provider-authority intervention required by `docs/refactor/0116-end-to-end-architecture-audit-and-provider-authority-intervention.md`.

## Closed evidence transactions

```text
N2 read-only evidence:
    e1eec5b68286cd6f888241afb50d9eabe00a8765269ecf20eb57bc0d7fe270d0

corrected N3 normalization:
    4dd86c4af956b447ed1829d6b5d604f43d10a17e5b3dcb3ddff3e9b48c377a9c

source-recipe evidence:
    c8160016267f3ff83b348146240f74f808ffbc93374a6f75988231ef22408cdb

exact binary-artifact comparison:
    da16d49acf54cbc8b6824e3974f08fea9ad0d6daf91687f4666d6c48d0b7567f
```

The binary receipt established exact indexed `.deb` supply identity for 28 priority package identities and byte-for-byte equivalence for all 6,887 artifact data members, including 462 ELF objects. Supply identity is not package-wide runtime authority.

## Priority authority review

```text
priority package dispositions:
    28 / 28

selected/reference object dispositions:
    59 / 59

base object authorities:
    29

conditional object authorities:
    30

unresolved authority groups:
    8
```

Accepted decisions include:

```text
Termux-adapted glibc 2.42:
    reviewed native world authority

selected X11/XCB SONAMEs:
    object-scoped platform authority

exact selected generic-library objects:
    object-scoped authority inside named profiles

glibc-runner:
    research/build/maintenance only; rejected runtime

termux-exec-glibc:
    optional platform provider; minimum-runtime inclusion unproven

package-wide runtime inference:
    rejected
```

Review files:

```text
review/
    package-authority-t0.tsv
    package-authority-t1.tsv
    selected-object-authority-base.tsv
    selected-object-authority-conditional.tsv
    unresolved-authority-ledger.tsv
```

See `docs/refactor/0133-selected-obsidian-priority-provider-authority-review.md`.

## Provider-profile lock draft

All reviewed objects are assigned to exact, non-materializing provider profiles.

```text
unique reviewed objects:
    59

profile content memberships:
    63

required symlink aliases:
    93

total locked rows:
    156

profile/package artifact locks:
    35

profiles:
    6
```

Profiles:

```text
world-substrate-selected
base-obsidian-x11-provider
graphics-freedreno-provider
gtk-font-device-compat-provider
printing-provider
optional-termux-exec-provider
```

Profile files:

```text
profiles/
    README.md
    provider-profile-definitions.tsv
    provider-profile-artifact-locks.tsv

    member-locks/
        world-substrate-selected.tsv
        base-obsidian-x11-provider.tsv
        graphics-freedreno-provider.tsv
        gtk-font-device-compat-provider.tsv
        printing-provider.tsv
        optional-termux-exec-provider.tsv
```

Every content row binds an exact accepted artifact SHA-256, exact `.deb` member path, content SHA-256, mode, size, authority state, source-recipe state, and update domain. Every alias row binds an exact artifact symlink and literal target.

```text
materialization_state:
    DRAFT_LOCK_ONLY_BLOCKED

materialization_authorized:
    NO
```

See `docs/refactor/0134-selected-obsidian-provider-profile-locked-member-draft.md`.

## Path boundary

```text
artifact_member_path:
    immutable supply identity inside the accepted artifact

installed_source_path:
    historical evidence path that proved live equivalence

future target path:
    unresolved and must be explicitly owned
```

Installed `$PREFIX/glibc` paths do not become successor target authority by inclusion in a ledger.

## Repository layout

```text
schema/
    census-columns.tsv
    capability-groups.tsv

recipe/
    N2, normalized N3, source-recipe and binary-artifact collectors/runners

review/
    package and object authority ledgers

profiles/
    profile definitions, artifact locks and exact member locks

work/                       # ignored by Git
    source/
    artifacts/
    receipts/unpacked/
    tmp/
```

## Storage boundary

```text
work/ and other Termux-private paths:
    source repositories
    raw artifacts and caches
    unpacked receipts
    temporary transaction state

$HOME/Downloads:
    final handoff archives and explicitly requested exports only
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

## Current incompleteness

The locked profile draft is not a complete runtime. It still excludes or leaves unresolved:

```text
complete glibc runtime-internal modules and loader state
world clean reconstruction/update/rollback
96 application-local generation identities
application payload and launcher supply identity
fonts
pixbuf modules and cache
icons and MIME data
D-Bus and other external capability ownership
final graphics overlay inclusion
GTK/Wayland, printing and optional exec policy
future target-domain and target-path mapping
```

## Claim discipline

```text
path identity != content identity
package ownership != semantic authority
exact artifact identity != runtime necessity
profile membership != materialization authorization
installed source path != future target authority
working runtime != final provider choice
application-local $ORIGIN topology remains first-class evidence
```

## Next valid state

```text
CLOSE_BASE_PROVIDER_PROFILE_GAPS_AND_DEFINE_EXTRACTION_TARGET_CONTRACT
```

This next stage remains repository-side design and analysis. A device transaction is not required until a specific unresolved claim needs new evidence or an explicitly bounded non-mutating validation is designed.

## Stop line

Do not:

```text
install, remove, upgrade, or downgrade packages
run package maintainer scripts
extract or copy profile members into a target
materialize a successor generation
create or change current
change promoted launchers
mutate loader state
patch RPATH
promote conditional profiles by availability
reopen closed graphics gates
```
