# Collaboration and exchange contract

## Roles

The agent performs the complex, context-heavy work. The user normally performs one bounded action in the authoritative Android/Termux environment and returns a compact status block.

```text
agent
    inspect canonical documents and evidence
    author and test repository changes in the sandbox
    create one self-contained execution package
    publish and verify the package
    retrieve and review returned result archives

user
    create and attach a full Git bundle when starting a new web session
    download and verify an execution package
    run one bounded wrapper in authoritative Termux
    return the final status block
```

Do not shift patch editing, command assembly, broad log analysis, or Git repair to the user unless the user's environment is the only place where the operation can occur.

## Repository transport

A new web-chat session normally receives a full Git bundle created directly from the user's clean authoritative Termux checkout. The bundle carries the repository, current-state documents, initialization protocol, and Git objects. No separate bootstrap repository or narrative handoff is required.

The agent verifies and materializes the attached bundle into a local sandbox checkout, checks out `main`, and follows `START_HERE.md`. Network-backed repository clone, pull, and push are performed only in the user's authoritative Termux checkout. A GitHub URL or repeated connector file reads are not object-based repository transport.

## Exchange channel

Canonical Drive root:

```text
ChatGPT-Agent-Exchange/termux-native-desktop/
```

Logical surfaces:

```text
agent-outbox/    agent -> user execution packages
user-results/    user -> agent results, receipts, and safety material
handoff/         historical archive only; not an onboarding channel
```

Google Drive is the primary exchange path after onboarding for execution packages, results, patches, bundles, logs, and safety artifacts. The agent attempts Drive first for every outbound artifact. If that attempt fails, the agent makes no second connector call, path rewrite, filename rewrite, ASCII-copy retry, or user-side upload attempt in the same delivery; it exposes the identical artifact through one user-visible sandbox link and stops. The next outbound artifact starts with Drive again. Concrete web-chat connector limitations are owned by [`platforms/chatgpt-web.md`](platforms/chatgpt-web.md).

## Artifact classes

### Execution package

One related exchange is delivered as exactly one raw `.tar.zst`, regardless of its internal file count, unless the artifacts are genuinely unrelated in purpose. The package contains:

```text
one exact repository patch or Git bundle;
one executable wrapper;
RUN.txt;
MANIFEST.sha256.
```

Use a Git bundle rather than a patch when ancestry or merge topology must be preserved. Do not use Base64 envelopes or split the wrapper, repository delta, and instructions into separate Drive items.

### Acquisition/analyzer package

When an exact external object or device-only fact is required but the web sandbox cannot acquire or inspect it, the agent prepares one read-only Termux wrapper rather than asking the user to improvise commands.

The wrapper pins the object coordinate and expected digest, downloads only into scratch space, performs the smallest named analysis, and emits one structured result `.tar.zst`. It does not install or activate the object unless that mutation is the explicit task.

```text
exact bytes needed by agent
    -> return verified bytes plus manifest

only metadata or ELF/package facts needed
    -> analyze on Termux and return compact TSV/JSON/status evidence
```

A sandbox DNS failure is not a reason to weaken identity checks or repeatedly try mirrors. It is a reason to move the network action to the authoritative user environment through a self-contained package.

### Result archive

The wrapper emits one result `.tar.zst` containing compact structured status, exact Git coordinates, bounded phase metadata, and detailed logs. The result is evidence for review; it is not accepted merely because upload succeeded.

### Repository safety bundle

A mutating transaction preserves a pre-transaction Git safety bundle. It is recovery material, not a current baseline after a successful push.

### Optional checkpoint

A checkpoint is allowed only for materially valuable incomplete sandbox work and is always non-authoritative. Its contract is defined in [`CHECKPOINTS.md`](CHECKPOINTS.md).

## User command and communication

The wrapper owns all feasible logic so the user command is minimized. The user's default download directory is `$HOME/Downloads`. When Drive publication succeeds, provide one copy-paste block that downloads to that directory, verifies, extracts, and invokes the wrapper:

```text
rclone copyto
sha256sum -c
tar --zstd -xf
one wrapper invocation
```

When the Drive connector fails and the artifact is exposed through a user-visible sandbox link, do not provide an alternate `rclone` upload/download route in that delivery. The wrapper ends with a compact block such as:

```text
===== final status =====
TRANSACTION_RC=...
PACKAGE_RC=...
REPOSITORY_RC=...
TEST_RC=...
PUSH_RC=...
VERIFY_RC=...
ARCHIVE_RC=...
UPLOAD_RC=...
NEW_HEAD=...
NEW_TREE=...
REMOTE_MAIN=...
RESULT_ARCHIVE=...
RESULT_SHA256=...
```

The user normally returns only this block. The agent retrieves the exact result archive and performs selective review before continuing.
