# Collaboration and exchange contract

## Roles

The agent should perform the complex work. The user should normally perform one bounded local execution and return the final status.

```text
agent
    inspect evidence
    author and test repository changes locally
    create one patch and one self-contained wrapper
    package and upload one .tar.zst
    verify returned result archives

user
    download with rclone
    verify the published package SHA-256
    extract and run one wrapper
    return the final status block
```

Do not shift patch editing, command assembly, log analysis or Git repair to the user unless the user's environment is the only place where the operation can occur.

## New-session repository transport

The normal new-session input is a full Git bundle created directly by the user from the authoritative Termux checkout and attached to the web chat. The bundle contains the repository, its documentation control plane and Git objects; no separate narrative handoff or bootstrap repository is required.

The agent verifies and clones the bundle, then follows `START_HERE.md`. Google Drive remains the normal channel for execution packages, results, safety material and optional bundle/patch exchange after onboarding.

## Exchange locations

Canonical Drive root:

```text
ChatGPT-Agent-Exchange/termux-native-desktop/
```

Logical surfaces:

```text
agent-outbox/    agent -> user execution packages
user-results/    user -> agent result archives and transaction safety material
handoff/         legacy archive only; not an active onboarding channel
```

Current folder IDs may be recorded in the dated handoff package. Logical paths are the durable contract.

## Package rule

One related exchange is one raw `.tar.zst`.

An execution package contains:

```text
one repository patch, or one Git bundle when ancestry/merge topology must be preserved;
one executable wrapper;
RUN.txt;
MANIFEST.sha256.
```

Do not use Base64 envelopes. Do not split the patch or bundle, wrapper and instructions into separate Drive items. Do not add a separate `.sha256` file unless an external tool specifically requires it; the published checksum and internal manifest are sufficient.

The user command should be one copy-paste block using `rclone copyto`, `sha256sum -c`, `tar --zstd -xf` and the package wrapper.

## Connector boundaries

### Google Drive

- Only local files located anywhere under `/mnt/data` are eligible for local-path upload rewriting. They do not need to be directly inside `/mnt/data`.
- In a new chat, local-path rewriting is blocked during the first assistant turn. Do not retry the same upload in that turn; use the full bundle already supplied by the user or expose the local artifact for a later turn.
- Binary filename search can be unreliable. Prefer exact folder listing and exact file IDs.
- After upload, fetch the remote item again and verify byte identity, SHA-256, zstd integrity and the internal manifest.
- If a valid raw upload is rejected because of a path or filename handling issue, copy the exact bytes to a short ASCII path under `/mnt/data`, upload with the intended destination filename, then verify the fetched bytes. The workaround must not change the artifact.

### GitHub

Use the GitHub connector for lightweight reads such as commit metadata, branch comparison and small file lookup. Use local Git for authoring, patch application, commit creation, push, bundles and history-sensitive work. The user environment is the authority for the actual guarded push.

### rclone

The user environment is expected to have the configured `gdrive:` remote. The agent container may not have `rclone`; a local stub is acceptable only for wrapper simulation and must never be presented as production evidence.

## Communication

The wrapper must end with a compact block:

```text
===== final status =====
TRANSACTION_RC=...
ARCHIVE_RC=...
UPLOAD_RC=...
RESULT_ARCHIVE=...
RESULT_SHA256=...
TARGET_TREE=...
NEW_HEAD=...
```

The user normally returns only this block. The agent retrieves the exact result archive from Drive and performs selective inspection.
