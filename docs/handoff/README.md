# Project-state handoffs

This directory owns session-transition records whose contents depend on the current project state. Durable collaboration, packaging and agent-execution rules live separately under [`../session-operations/`](../session-operations/README.md).

## Entry point

Read [`CURRENT.md`](CURRENT.md) first. It is a compact index, not a substitute for the dated handoff and authoritative project documents that it links.

```text
CURRENT.md
    -> active dated handoff
    -> STATUS.md and controlling numbered records
    -> exact pending packages or receipts
```

## Scope

A project-state handoff records only information that can change between sessions:

```text
repository, branch, last verified HEAD and tree;
current authority and claim boundaries;
accepted and rejected conclusions;
exact result/package names, hashes and Drive locators;
verified versus intentionally unverified artifacts;
allowed next action and stop lines;
links to the controlling project documents.
```

It must not duplicate the long-lived Git/Drive workflow, wrapper contract, connector limitations or general troubleshooting rules. Link to `../session-operations/` instead.

## Onboarding order

```text
1. obtain and verify the mandatory handoff .tar.zst;
2. read its START_HERE.md and `../PROJECT_PRINCIPLES.md`;
3. read this CURRENT.md and its active dated handoff;
4. inspect any explicitly pending result before repository mutation;
5. verify repository branch, HEAD, tree, tracked state and remote state;
6. read the authoritative project documents linked by the dated handoff;
7. continue only the explicitly allowed workstream.
```

## Maintenance

At every session close:

1. create a new dated handoff when the project state changed;
2. update `CURRENT.md` to point to it;
3. preserve older handoffs as historical evidence;
4. update `../session-operations/CHANGELOG.md` only when a durable operating rule changed.

The session-close procedure is defined in [`../session-operations/SESSION_CLOSE.md`](../session-operations/SESSION_CLOSE.md).
