# Selected target Pixman size, resource budget and intervention review

## Decision

```text
review id: PIXMAN-SIZE-RESOURCE-INTERVENTION-001
decision: INTERVENTION_CONDITIONALLY_LIFTED_FOR_READ_ONLY_MATERIALIZER_DESIGN_REVIEW_ONLY
exact member sizes: 41
open member sizes: 0
exact member bytes: 29,047,112
receipt prototype bytes: 44,332
receipt reservation: 1,048,576
final resource preflight: 59,142,800
population authorized: NO
```

The exact retained historical result `termux-native-desktop-cairo-pixman-prerequisite-evidence-v2-20260718T033508Z-results.tar.zst` has outer SHA-256 `3df4f72452b6fb36525ea651f58a0d9d0e551d6ab1f0076653588e767fb1ad9a`. Its regular tar member `./evidence/pixman/libpixman-1.so.0.46.4` is 460,920 bytes. The companion SHA evidence binds that member to `cab54c7f8e4c3a5c1980aa7564b9321114418f2d3c6fa37a3c0723f9f22e1eb2`. The embedded package size is not used as member size and no embedded provider byte is extracted by this review.

## Receipt reservation

`selected-target-verification-receipt-prototype.json` is canonical compact JSON generated from the accepted 41 object bindings, 41 aliases, target paths and GEN-005 verification fields. Its exact size is 44,332 bytes and SHA-256 is `b5e375cef8a47aac3fd298ef855ba0fd179942a005efc6a96817ab3bb9630b79`.

The reserved receipt overhead is deterministic:

```text
max(1,048,576, next_power_of_two(canonical_prototype_bytes))
= 1,048,576 bytes
```

Any future canonical receipt larger than this reservation must abort before generation publication. The reservation is not evidence that a receipt or generation already exists.

## Final resource budget

```text
41 exact members:                       29,047,112
100% member margin:                     29,047,112
verification receipt reservation:        1,048,576
final required free bytes:              59,142,800
minimum floor:                          16,777,216
```

The runtime preflight must require at least 59,142,800 free bytes and must still verify owner, mode, same-filesystem and non-symlink constraints. No statvfs or filesystem preflight is claimed by this review.

## Intervention decision

All ten prerequisites are satisfied at evidence or contract level for **read-only materializer design review only**. The intervention remains fully effective against byte acquisition, extraction, generation-root creation, target writes, population, publication, deployment and activation.

The next action is `design-read-only-selected-provider-materializer-and-runtime-preflight-contract`. It may specify algorithms, failure ordering and validation interfaces. It may not create the generation root, acquire provider bytes or execute a materializer.
