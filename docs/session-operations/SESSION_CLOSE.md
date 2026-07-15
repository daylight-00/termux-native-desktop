# Session boundary and optional checkpoint procedure

This document is read only when a session is ending. Normal accepted work does not require a narrative handoff.

## First decision

Classify the boundary:

```text
A. accepted state is committed, pushed, verified and reflected in docs/current/;
B. an issued execution package has not been run;
C. a result exists but semantic review is intentionally deferred;
D. valuable sandbox-only work is incomplete;
E. no project state changed.
```

## Clean boundary

For A or E:

- do not create or update `docs/handoff/CURRENT.md`;
- do not write a session narrative;
- confirm that `docs/current/` contains the active state and next action;
- report the authoritative repository HEAD/tree and any non-blocking external coordinates;
- end the session.

The user creates a fresh full bundle from authoritative Termux `main` when starting the next web-chat session.

## Pending execution or result

For B or C, the repository must already record the boundary in:

```text
docs/current/ACTIVE_TASK.md
docs/current/PENDING_ARTIFACTS.yaml
```

Record exact package/result name, digest, state and successor first action. A result whose review is deferred remains semantically unaccepted. Do not rely on chat text alone.

## Incomplete sandbox-only work

For D, prefer discarding reproducible scratch work and restarting from the last accepted `main`.

Create a checkpoint only when losing the work would impose material cost. A checkpoint must be explicitly non-authoritative and may contain:

```text
a Git bundle containing the accepted main and one namespaced checkpoint ref;
a patch for tracked uncommitted changes;
necessary bounded logs or generated inputs;
a short CHECKPOINT.md stating base HEAD/tree, scope, unverified assumptions and next action;
MANIFEST.sha256.
```

A successor must compare the checkpoint against accepted `main`; it must not treat checkpoint contents as accepted project state.

## Artifact validation

Any checkpoint archive must:

1. use safe relative paths;
2. reject unexpected links and special members;
3. use zstd rather than gzip;
4. include `MANIFEST.sha256`;
5. be verified locally before publication;
6. be labelled `checkpoint`, never `handoff` or `current`.

## Durable operating lessons

Update `session-operations/` only for reusable process rules. Update architecture, decisions, current state and evidence at the accepted transition where they change, not at the end of the chat.
