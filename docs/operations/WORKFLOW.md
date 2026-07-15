# Bundle-native web-chat workflow

This is the closed-loop procedure for a web-chat agent operating from a user-supplied full Git bundle. It does not depend on a previous chat, a narrative handoff, an immediate connector read, or a GitHub clone.

## State machine

```text
RECEIVE_FULL_BUNDLE
    -> VERIFY_AND_CLONE
    -> READ_REPOSITORY_BOOTSTRAP
    -> PRODUCE_ONBOARDING_RECEIPT
    -> RESOLVE_BLOCKING_ARTIFACT
    -> EXECUTE_ONE_BOUNDED_PHASE
    -> VERIFY_RETURNED_RESULT
    -> UPDATE_CANONICAL_STATE
    -> ACCEPT_OR_RECORD_BLOCK
```

A clean accepted repository transition is its own continuation point.

## 1. Verify and clone

```text
verify the supplied checksum when present
git bundle verify
clone into an isolated sandbox directory
checkout main explicitly
record branch, HEAD, tree, and tracked status
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
applicable platform profile when platform behavior matters
```

Before changing the repository, produce the onboarding receipt required by `START_HERE.md`. It must identify the current phase, active task, stop conditions, user/agent authority boundary, unavailable environments, and first valid action.

History, experiment reports, and archived handoffs are opened only for a specific need named by the active task.

## 3. Resolve blocking external state

Read `docs/current/PENDING_ARTIFACTS.yaml`. When a blocking artifact exists:

1. retrieve the exact object;
2. verify digest, archive integrity, and safe members;
3. inspect structured status and Git coordinates;
4. accept, reject, or preserve the boundary in canonical current state;
5. do not author an unrelated dependent transition first.

An artifact mentioned only in old chat or historical prose is not automatically blocking.

When the exact artifact is blocking but the sandbox cannot fetch it because DNS, outbound access, connector contracts, or device-only tooling are unavailable, perform one bounded probe and switch authority. Create a self-contained acquisition/analyzer wrapper for user Termux; do not accumulate equivalent retries in the web session.

## 4. Execute one bounded phase

The active task owns scope, required reading, next valid action, stop conditions, and completion criteria.

The agent authors and tests in the sandbox and publishes one self-contained execution package. The user's Termux environment performs authoritative Git mutation, deployment, and device-only checks. Follow [`EXECUTION.md`](EXECUTION.md) for transaction and review rules.

Do not claim acceptance until the returned result is verified.

## 5. Persist state at transition time

When a transition is accepted, update the relevant canonical documents in the same repository change:

```text
docs/current/STATE.yaml
docs/current/BRIEF.md
docs/current/ACTIVE_TASK.md
docs/current/PENDING_ARTIFACTS.yaml when needed
relevant architecture, decision, operations, or evidence documents
```

Do not defer current-state maintenance to a later session-close summary.

## 6. Boundary

When authoritative `main` contains the accepted state and no unreviewed blocking artifact remains, there is no handoff action. The user may create a fresh full bundle from that checkout whenever another web session is needed.

Valuable incomplete sandbox-only work is handled only through the optional non-authoritative checkpoint rules in [`CHECKPOINTS.md`](CHECKPOINTS.md). Reproducible scratch work should normally be discarded and repeated from accepted `main`.

## Completion test

A bounded cycle is complete when:

```text
the returned result has been verified;
remote main and authoritative local main agree;
canonical current documents describe the accepted boundary;
no hidden chat-only next action remains;
the repository can initialize a new agent through START_HERE.md.
```
