# Clean boundaries and optional checkpoints

Normal accepted work requires no narrative handoff and no session-close artifact.

## Boundary classification

```text
A. accepted state is committed, pushed, verified, and reflected in docs/current/;
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
- report authoritative HEAD/tree and any non-blocking external coordinates;
- end the session.

The user creates a fresh full bundle from authoritative Termux `main` when starting another web-chat session.

## Pending execution or result

For B or C, the repository must already record the boundary in:

```text
docs/current/ACTIVE_TASK.md
docs/current/PENDING_ARTIFACTS.yaml
```

Record the exact artifact name, digest, lifecycle state, and first valid action. A deferred result remains semantically unaccepted. Chat text alone is not durable state.

## Incomplete sandbox-only work

For D, prefer discarding reproducible scratch work and restarting from accepted `main`.

Create a checkpoint only when loss would impose material cost. It may contain:

```text
a Git bundle with accepted main and one namespaced checkpoint ref;
a patch for tracked uncommitted changes;
necessary bounded logs or generated inputs;
a short CHECKPOINT.md stating base HEAD/tree, scope, unverified assumptions, and next action;
MANIFEST.sha256.
```

A checkpoint is explicitly non-authoritative. A successor compares it against accepted `main` and must not treat its content as accepted state.

## Checkpoint validation

A checkpoint archive must:

1. use safe relative paths;
2. reject unexpected links and special members;
3. use zstd rather than gzip;
4. include `MANIFEST.sha256`;
5. be verified locally before publication;
6. be labelled `checkpoint`, never `handoff` or `current`.
