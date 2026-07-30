# Selected-provider local-supply live-authority transaction exact input-set collection boundary acceptance

## Decision

`SELECTED-PROVIDER-LOCAL-SUPPLY-LIVE-AUTHORITY-TRANSACTION-EXACT-INPUT-SET-COLLECTION-ACCEPT-001` accepts the exact six-artifact collection/sealing candidate as `ACCEPTED_BOUNDED_NON_EXECUTING_EXACT_INPUT_SET_COLLECTION_SEALING_AUTHORITY`.

The acceptance closes `SELECTED-PROVIDER-LOCAL-SUPPLY-LIVE-AUTHORITY-TRANSACTION-EXACT-INPUT-SET-COLLECTION-ACCEPTANCE-OPEN`. The accepted implementation remains non-executing until an explicit transaction envelope supplies every required input path and binding.

## Frozen artifacts

| Artifact | SHA-256 |
| --- | --- |
| collection implementation | `bcbd471b781a9843ba50da269c9686d928a638ede3f440bac5eda9b57bc58b3c` |
| isolated fixture plan | `f983c10db472d2aa2dd969e1366b147b421498386416353bf1840e17e1439496` |
| negative cases | `74a1168fbf1e3346b99366bb34564fa09a5d5186bfd61f29dce82af6d804bf95` |
| input coverage | `d5ce14debc372cb8fc2049d869ff3be1bfeb60c25e828a9875a95e17906e855c` |
| isolated success | `b9c844973f7203cb74e106da0ec6e6889a0898304bf2944b822127d5c196edd7` |
| metadata | `e24f13b2faab9098a2314aea4e6062161ba131b4124ebb3ccd281e7a28e86ec9` |

## Accepted behavior

The accepted boundary covers twenty explicit input contracts, one isolated success and twenty fail-closed cases. The success fixture performs five canonical authority-document reads, forty-one provider-coordinate `lstat` calls, one replay-registry `lstat`, two repository metadata captures, one remote capture, one executor identity capture and two isolated envelope writes.

Selected-provider content opens and reads remain zero. Provider bytes remain zero. Project replay opens, reads and writes remain zero. The collection implementation does not invoke the accepted orchestration or synthetic oracles.

## Owner accounting

One owner-authorized non-executing collection, sealing and review transaction exists. Acceptance does not consume it.

```text
accepted: 1
consumed: 0
remaining: 1
```

## Inputs still absent

The owner authorization token, canonical forty-one-row coordinate receipt, revocation document, trusted-time evidence, execution authorization, project replay-registry baseline and exact selected-provider coordinate paths remain unsupplied and unauthorized. Acceptance may not infer or generate them.

## Current authority

```text
live documents:             0
execution authorizations:   0
project replay writes:      0
selected-provider opens:    0
selected-provider reads:    0
provider bytes:             0
local-supply maps:          0
live authority:             0
```

## Next boundary

The next valid action is `prepare-and-review-one-non-executing-selected-provider-local-supply-live-authority-transaction-exact-input-set-collection-envelope`. Envelope preparation must remain explicit-input-only and must not consume the owner transaction, open provider content, access project replay contents or arm an execution gate.

Any source digest, input mapping, metadata capture, envelope serialization, owner accounting or authority change requires a new collection review.
