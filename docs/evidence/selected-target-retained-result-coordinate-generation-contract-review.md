# Retained supply-result coordinate and generation-root contract review

## Decision

```text
review:                         RETAINED-SUPPLY-COORDINATE-GENERATION-CONTRACT-001
decision:                       INTERVENTION_RETAINED_COORDINATE_PROGRESS_AND_GENERATION_CONTRACTS_DEFINED
concrete objects:               41
existing digest-bound inputs:   14
new legacy Drive coordinates:   24
missing result coordinates:      3
legacy result-index upgrades:   24
generation contracts defined:    7
population authorized:          NO
materializer design authorized: NO
byte acquisition authorized:    NO
```

The review closes Drive file identity and outer-SHA coordinates for twenty-four previously blocked concrete objects without accepting their legacy authority transaction archives as population-grade verification. Those archives report successful transactions but predate `result-index.sha256`; each remains blocked by `LEGACY-RESULT-INDEX-UPGRADE-OPEN`.

Fontconfig, HarfBuzz and libxkbcommon retain `RETAINED-RESULT-COORDINATE-OPEN`. Exact package, artifact, member and SONAME identities remain accepted, but no result archive coordinate was found in the bounded search. Absence does not authorize reproduction or acquisition.

## Generation-root contract

The proposed non-live base is:

```text
/data/data/com.termux/files/home/.local/state/termux-native-desktop/selected-provider-runtime
```

It is a contract only. This review creates no directory. The future layout separates content objects, transaction staging, immutable generations, receipts, locks and `current`/`previous` selectors under the same base. Every existing ancestor must be non-symlink, owner-controlled and outside the live glibc prefix, `$HOME/gl`, package databases and the repository.

Whole-generation publication requires same-filesystem staging, tree and parent fsync, one rename into `generations/<generation-id>`, explicit verification, and only then a temporary relative selector symlink renamed atomically. Rollback changes only the selector and never mutates an immutable generation.

The receipt contract binds the accepted composition and target policy to all 41 object hashes, 41 alias targets, ELF machine/SONAME/NEEDED/RPATH/RUNPATH checks, canonical-loader resolution and a hashed result index. Space/ownership preflight uses verified member sizes plus receipt overhead and a 100% margin with a 16 MiB floor; exact member-size census remains open.

Failure handling is transaction-ID scoped. A failed staging tree is preserved or quarantined with an idempotent failure receipt; cleanup may never touch package databases, the live glibc prefix, another generation or an unknown path.

## Remaining blockers

```text
3 retained result coordinates missing
24 legacy result indexes missing
41-member exact size census missing
```

The intervention therefore remains. No supply artifact is downloaded or extracted, no target path is created, and no materializer is designed or authorized.

## Next action

```text
close-three-missing-result-coordinates-upgrade-legacy-indexes-and-census-member-sizes
```
