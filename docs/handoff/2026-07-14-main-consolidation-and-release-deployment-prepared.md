# Main consolidation and immutable release deployment prepared

## Prepared boundary

A history-preserving integration candidate combines:

```text
active implementation/evidence line:
    9d3b3ece936ca2ae106c6ac6d465f45bd9f91a0f

system-foundation line:
    b8858f44b159ca564ee3bab133085530a5bcb6e7
```

The candidate adds:

- `docs/knowledge/` and `docs/system-foundation/` to the canonical active tree;
- a one-long-lived-branch policy centered on `main`;
- manifest-driven immutable repository release deployment;
- `workstation` and `full` physical deployment profiles;
- stable `current` and `previous` deployment pointers;
- a canonical fast/full repository smoke runner.

## User-authoritative transaction

The Termux wrapper must:

1. verify exact local and remote coordinates;
2. create a local all-ref safety bundle;
3. fetch the agent integration bundle;
4. fast-forward local `main` to the integration candidate;
5. run repository gates;
6. push and verify `main`;
7. delete only merged remote topic branches;
8. migrate live managed leaves from checkout links to the immutable release pointer;
9. archive structured result evidence and upload it through the established Drive exchange.

No external application payload, selected provider generation, historical Mesa install or user profile is deleted by this transaction.

## Pending after success

- inspect and classify `$HOME/gl/.git` before retiring the duplicate repository authority;
- classify historical Mesa/build/provider directories before physical cleanup;
- revisit system-foundation, project philosophy and handoff/user-agent documentation as a separate discussion;
- reassess provider-authority assurance depth before continuing the full SUP-02 request set.
