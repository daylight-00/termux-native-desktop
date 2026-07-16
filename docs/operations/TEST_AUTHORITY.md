# Test authority model

Repository tests have the same authority-lifecycle problem as documentation: an observation from an earlier transition must not silently become the owner of current semantic state.

## Current gates

A current gate may verify one of two things:

1. an immutable evidence or component contract that remains true independently of the active task; or
2. the latest aggregate current authority, owned by a dedicated current-state checker.

Reusable component checks must not pin:

```text
current active-task ID
exact semantic state version
whole-project accepted/open counts
next review tranche
an intermediate disposition that a later accepted transition superseded
```

Those fields belong to aggregate current checkers such as `check-current-authority`, `check-provider-claim-classification`, `check-selected-provider-composition-review`, and the checker for the latest accepted transition.

## Historical stage smoke tests

A smoke test that proves an intermediate state transition is preserved under `tests/history/` after that transition is superseded. It remains provenance for the historical commit where it was current, but it is excluded from `--docs`, `--fast`, and current `--full` gates.

Historical stage tests are not rewritten to pretend that their intermediate conclusion is still current. Their immutable receipt and result evidence remain available through Git history and the evidence documents they originally validated.

## Promotion rule

When a new accepted transition supersedes an intermediate test:

1. add or update a final aggregate/current checker;
2. move the superseded stage smoke under `tests/history/`;
3. remove active-task, state-version, global-count, and next-tranche coupling from reusable component checkers;
4. keep the current suite bounded to live invariants;
5. record the lifecycle change in the same repository transition.

## Negative testing

Current negative smokes should mutate the specific authority they own—for example a provider decision, digest, collision count, or prohibited inference. They should not use an obsolete active-task string merely as a proxy for correctness.
