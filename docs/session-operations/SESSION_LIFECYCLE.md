# Recurring session lifecycle

This is the closed-loop procedure for every successor session. It starts with one mandatory handoff `.tar.zst` and ends by producing the next handoff packages.

## State machine

```text
RECEIVE_HANDOFF
    -> VERIFY_HANDOFF
    -> UNDERSTAND_PRINCIPLES
    -> RESOLVE_PENDING_BOUNDARY
    -> SYNCHRONIZE_REPOSITORY
    -> READ_CONTROLLING_AUTHORITY
    -> EXECUTE_ONE_BOUNDED_PHASE
    -> VERIFY_RESULT
    -> UPDATE_DURABLE_RULES_IF_NEEDED
    -> PREPARE_NEXT_HANDOFF
    -> VERIFY_REMOTE_BACKUPS
```

Do not skip forward. In particular, no repository mutation is allowed before an explicitly pending result is resolved.

## 1. Receive and verify

The mandatory handoff package is the first input. Record its observed SHA-256, test zstd, reject unsafe archive members, extract into an isolated directory, then run its internal verification script and `MANIFEST.sha256`.

A pending result may be included as raw, quarantined bytes. Verifying its transfer and zstd stream does not accept its project meaning.

## 2. Understand the project before acting

Read:

```text
START_HERE.md
PROJECT_PRINCIPLES.md
current project-state summary
current dated handoff
```

The successor must be able to state:

```text
what the project is proving;
what the evidence-to-authority ladder is;
which Git/result coordinates are verified;
which artifact is still pending;
which claims remain prohibited;
what the first safe action is.
```

## 3. Resolve the pending boundary

Prefer the raw pending result included in the handoff package. Use the exact Drive ID only as a fallback or remote-identity check. Review structured status files first, confirm Git and remote state, and use a lightweight GitHub read before accepting the new boundary.

Update `handoff/CURRENT.md` only after this review.

## 4. Continue one bounded phase

Read only the controlling project documents named by the handoff. Author and test in a local worktree, generate one immutable patch, and send one self-contained wrapper package. The user executes one command and returns the final status block.

Retrieve and verify the result before authoring another phase.

## 5. Maintain the operating system of collaboration

When a reusable lesson is learned, update the relevant file under `session-operations/` during the same session and add one changelog entry. Project decisions remain in numbered project documents; transient state remains in the dated handoff.

## 6. Close and hand over

Read [`SESSION_CLOSE.md`](SESSION_CLOSE.md) and classify the boundary:

```text
latest result verified;
execution package not run;
result exists but review deferred;
no execution pending.
```

Create two or three packages according to that state. The mandatory package must allow the next session to repeat this lifecycle without relying on the old container or on immediate connector availability.

## Completion test

The cycle is complete only when:

```text
mandatory handoff uploaded and remotely reverified;
miscellaneous backup uploaded and remotely reverified;
execution package also uploaded when applicable;
exact filenames, Drive IDs, sizes and SHA-256 values recorded;
START_HERE names one unambiguous first action;
next session can begin from the mandatory zst alone.
```
