# 0157 — Selected Obsidian generic build-attestation and adaptation gap-evidence supply batch SUP-01 response

## Status

```text
SUPPLY BATCH: SUP-01
REQUEST: SRQ-OJ-001
RESPONSE: PREPARED / BOUNDED / REVIEW REQUIRED
REQUIREMENT: OJ-001
PRIOR ORACLE CONCRETE IDENTITY: libjpeg.so.62.3.0
PROPOSED REQUIRED IDENTITY: libjpeg.so.62
REJECTED SUBSTITUTE: libjpeg.so.8
MATCHING SONAME-62 PROVIDER CANDIDATES BOUND: 0
CANDIDATE EVIDENCE PAYLOADS: 1
OBJECT CORRECTIONS ACCEPTED: 0
FINAL PROVIDER AUTHORITY: 0 ACCEPTED
TARGET POPULATION: BLOCKED
```

This transaction fulfills the isolated P0 `SUP-01` request by preparing one immutable-reference-backed candidate response. It corrects the requirement model from the Debian oracle's provider-versioned concrete filename `libjpeg.so.62.3.0` to the stable required ABI identity `libjpeg.so.62`.

The correction is not yet accepted. The response must pass the bounded acquirer and a separate receipt review.

## Authoritative basis

The upstream libjpeg-turbo 3.1.0 build definition establishes two distinct ABI modes:

```text
default / libjpeg v6b emulation:
    JPEG_LIB_VERSION=62
    default SOVERSION=62

WITH_JPEG8=ON:
    JPEG_LIB_VERSION=80
    default SOVERSION=8
    explicitly backward-incompatible with libjpeg v6b
```

The shared target uses `SO_MAJOR_VERSION` as its ELF `SOVERSION`. Therefore a `WITH_JPEG8=ON` build is not a filename variant of the v6b ABI; it is a different ABI family.

The pinned Termux-pacman recipe for the selected 3.1.0 lineage enables:

```text
-DWITH_JPEG8=ON
```

The selected candidate artifact accordingly contains:

```text
libjpeg.so
libjpeg.so.8
libjpeg.so.8.3.2
```

It does not contain `libjpeg.so.62` and cannot satisfy the requirement by aliasing or ABI-family inference.

The Debian oracle identity remains useful but is narrowed:

```text
libjpeg.so.62.3.0
    -> observed provider-versioned concrete member

libjpeg.so.62
    -> stable required SONAME identity
```

A future acceptable candidate must carry exact ELF `DT_SONAME=libjpeg.so.62`. Its concrete filename is provider/version-specific and is not fixed to `.62.3.0`.

## Canonical response package

```text
experiments/glibc/selected-obsidian-provider-authority/evidence-supply/responses/SUP-01/SRQ-OJ-001/
    acquisition-input/
        acquisition-input-manifest.tsv
        object-requirement-correction-review.tsv
    analysis.status
    claim-boundary.txt
    next-state.txt
    response-metadata.tsv
```

Canonical generator:

```text
recipe/prepare-generic-build-attestation-and-adaptation-gap-evidence-supply-batch-sup-01-response.py
```

The tracked response is deterministically regenerated and then passed through the existing `0154` acquirer. The acquirer must emit one candidate row while keeping object-correction acceptance, final-provider authority and target population at zero.

## Response boundary

The response proposes:

```text
required_identity = libjpeg.so.62
```

It explicitly rejects:

```text
libjpeg.so.8 substitution;
libjpeg.so.8.3.2 concrete-member substitution;
ABI-family similarity as requirement satisfaction;
Debian concrete filename .62.3.0 as permanent target identity;
provider authority from recipe or package origin alone.
```

## Shell-layout intervention incorporated

The failed original `0156` wrapper inherited terminal stdin while running an interactive shell smoke through a non-foreground `timeout` process group. Subsequent transaction wrappers invoke repository smoke tests using:

```bash
timeout --foreground --kill-after=10s <seconds> bash <test> </dev/null
```

This is an execution-harness safeguard only. It changes no repository policy or product semantics.

## Next state

```text
REVIEW_BOUNDED_GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_SUPPLY_BATCH_SUP_01_RESPONSE
```

## Stop line

Do not:

```text
accept the proposed correction without the separate response review;
treat libjpeg.so.8 as libjpeg.so.62;
create a compatibility symlink across the ABI families;
accept the current Termux artifact as a matching provider candidate;
fix the required concrete filename to libjpeg.so.62.3.0;
accept build attestation, adaptation, filename policy or final provider authority;
populate target rows;
materialize or activate a successor.
```
