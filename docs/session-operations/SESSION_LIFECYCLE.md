# Recurring web-chat session lifecycle

This is the closed-loop procedure for a web-chat agent that receives a full Git bundle. It does not depend on a previous chat, a narrative handoff, an immediate connector read, or a repository clone from GitHub.

## State machine

```text
RECEIVE_FULL_BUNDLE
    -> VERIFY_AND_CLONE
    -> READ_START_HERE
    -> CONFIRM_CURRENT_STATE
    -> RESOLVE_BLOCKING_ARTIFACT
    -> EXECUTE_ONE_BOUNDED_PHASE
    -> VERIFY_RESULT
    -> UPDATE_CANONICAL_STATE
    -> ACCEPT_OR_RECORD_BLOCK
```

A clean accepted transition is its own continuation point. The user can create the next full bundle directly from authoritative Termux `main` whenever a new session is needed.

## 1. Receive, verify and clone

The normal first input is a user-created full Git bundle.

```text
verify the supplied checksum when present
run git bundle verify from a temporary repository context
clone into an isolated sandbox directory
checkout main explicitly
record branch, HEAD, tree and tracked status
```

Do not reconstruct the repository through repeated raw GitHub connector reads.

## 2. Initialize from repository authority

Read in this order:

```text
START_HERE.md
AGENTS.md
docs/current/BRIEF.md
docs/current/ACTIVE_TASK.md
active-task required reading
applicable platform profile
```

The agent must be able to state the current phase, active task, stop conditions, user/agent authority boundary, unavailable environments and first valid action before changing the repository.

Historical numbered records, experiment reports and archived handoffs are loaded only when the active task names a specific need.

## 3. Resolve blocking external state

Read `docs/current/PENDING_ARTIFACTS.yaml`.

When a blocking result exists:

1. retrieve the exact artifact;
2. verify its reported digest and archive integrity;
3. inspect structured status and Git coordinates;
4. accept, reject or preserve the boundary in canonical current state;
5. do not author the next unrelated repository transition first.

A result mentioned only in old chat or an archived handoff is not automatically blocking.

## 4. Execute one bounded phase

The active task defines scope, required reading, next valid action, stop conditions and completion criteria.

The agent authors and tests in the sandbox, creates one self-contained execution package, and gives the user one bounded command. The user's Termux environment performs authoritative Git mutation, deployment and device-only checks.

Retrieve and review the returned result before claiming acceptance or beginning another dependent phase.

## 5. Persist state at transition time

When a transition is accepted, update in the same repository change:

```text
docs/current/STATE.yaml
docs/current/BRIEF.md
docs/current/ACTIVE_TASK.md
docs/current/PENDING_ARTIFACTS.yaml when needed
relevant durable architecture/operations documents
```

Do not defer this work to a future session-close summary.

## 6. Session boundary

When authoritative `main` already contains the accepted state and there is no unreviewed blocking artifact, no handoff artifact is required.

If valuable work exists only in the sandbox and cannot be accepted before the session ends, follow [`SESSION_CLOSE.md`](SESSION_CLOSE.md) to create an explicitly non-authoritative checkpoint. The next session otherwise starts from the latest accepted full bundle and repeats only unfinished work.

## Completion test

A bounded cycle is complete when:

```text
the returned result has been verified;
remote main and local authoritative main agree;
canonical current-state documents describe the accepted boundary;
no hidden chat-only next action remains;
the repository can initialize a new agent through START_HERE.md.
```
