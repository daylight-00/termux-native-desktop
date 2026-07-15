# Operational troubleshooting

## Drive and connector bottlenecks

| Symptom | Proven response |
|---|---|
| Binary file is not found by Drive search | List the exact canonical folder and select by full filename and creation time. |
| Fetched binary appears as a local `.bin` | Treat it as raw bytes; verify the expected SHA-256 and zstd stream before extraction. |
| Local upload path is rejected | Confirm the file is anywhere under `/mnt/data`; paths outside that subtree cannot be rewritten. |
| Upload fails on the first assistant turn of a new chat | Do not retry in that turn. Continue from the user-supplied full bundle and publish on a later turn. |
| Valid archive is rejected because of filename/path handling | Copy identical bytes to a short ASCII path under `/mnt/data`, set the intended Drive filename explicitly, and verify fetched bytes. |
| Upload reports success but trust is uncertain | Fetch by exact file ID and compare size, SHA-256, zstd integrity, and internal manifest. |

## Wrapper and test failures

| Symptom | Proven response |
|---|---|
| `unbound variable` under `set -u` | Separate declarations from assignments and command substitutions. |
| Wrapper appears stuck | Inspect process state and `transaction.log`; do not infer from intended behavior. |
| Test can inherit interactive stdin | Run through `timeout --foreground --kill-after=10s ... </dev/null`. |
| A smoke test copies a linked-worktree `.git` control file and mutates the candidate checkout | Create an independent fixture with `git clone --no-hardlinks`; never copy the control file. |
| One smoke test removes a shared parent temporary directory | Give every test an independent child root and remove only that child. |
| Link validation flags ignored upstream source snapshots | Scope project-document validation to Git-tracked Markdown or explicitly exclude experiment `work/source/` inputs. |
| `mv -Tf` fails when replacing a symlink whose target resolves to a directory | Remove the old selector and create the final symlink directly; validate the raw link target. |
| Failure occurs before push | Reset to the pinned base and clean only expected paths; preserve unrelated untracked files. |
| Remote moved during execution | Abort before push. Never force the branch. |
| Push succeeded but packaging or upload later failed | Do not reset repository or remote; preserve the pushed state and repair the later stage separately. |

## Inspection and output volume

Start with structured status files. Do not read entire raw logs unless a structured file indicates failure. Use exact `grep`, bounded `tail`, and targeted member extraction.

Terminal output should show transaction stages and the final status block; detailed test output belongs in the result archive.

## Repository recovery

Prefer the user's live authoritative repository plus remote confirmation. Use a Git bundle when refs or history diverge, a rewrite occurred, or the authoring baseline cannot be trusted. A stale bundle is recovery material only when paired with exact later deltas and an explicit warning that it is not current.

## GitHub connector reads

| Symptom | Proven response |
|---|---|
| Exact branch search misses a known slash-containing ref | Read a known file with the branch as `ref`, then compare commit and branch; trust the comparison rather than search recall. |
| Sandbox Git cannot resolve the remote host | Keep authoring and publication separate. Use connector-backed remote inspection and a verified bundle for local objects; never present stale recovery material as current. |
