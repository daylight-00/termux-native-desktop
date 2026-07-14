# Operational troubleshooting

## Drive and connector bottlenecks

| Symptom | Proven response |
|---|---|
| Binary file is not found by Drive search | List the exact canonical folder and select by full filename and creation time. |
| Fetched binary appears as a local `.bin` | Treat it as raw bytes; verify the expected SHA-256 and zstd stream before extraction. |
| Local upload path is rejected | Confirm the file is anywhere under `/mnt/data`; paths outside that subtree cannot be rewritten. |
| Upload fails on the first assistant turn of a new chat | Do not retry in that turn. Start from the user-supplied handoff artifact and upload later. |
| Valid archive is rejected because of filename/path handling | Copy identical bytes to a short ASCII path under `/mnt/data`, set the intended Drive filename explicitly, and verify the fetched bytes. |
| Upload reports success but trust is uncertain | Fetch the Drive item by exact ID and compare SHA-256, size, zstd and internal manifest. |

## Wrapper failures

| Symptom | Proven response |
|---|---|
| `unbound variable` under `set -u` in a helper | Separate `local` declarations from assignments and command substitutions. |
| Wrapper appears stuck | Inspect process state and `transaction.log`; do not infer from intended behavior. |
| Test can inherit interactive stdin | Run through `timeout --foreground --kill-after=10s ... </dev/null`. |
| A smoke test copies `.git` from a linked worktree and unexpectedly mutates the candidate checkout | Never copy a linked-worktree `.git` control file into a fixture. Create an independent local fixture with `git clone --no-hardlinks` instead. |
| Failure after patch application | Reset to pinned base HEAD and clean only the expected new paths; preserve unrelated untracked files. |
| Remote moved during execution | Abort before push. Never force the branch. |
| Push succeeded but a later packaging step failed | Do not reset the repository or remote; report the pushed state and package failure separately. |

## Inspection and output volume

Start with structured status files. Do not read entire raw logs unless a structured file indicates failure. For large failures use exact `grep`, bounded `tail` and targeted member extraction.

Terminal output should show transaction stages and the final status, while detailed tests remain in the result archive.

## Repository recovery

Prefer the user's live local repository plus remote verification. A Git bundle is required when refs or history diverge, a rewrite occurred, or the authoring baseline cannot be trusted. A stale bundle remains useful as recovery material only when paired with exact later patches and an explicit warning that it is not the current baseline.

## GitHub connector reads

| Symptom | Proven response |
|---|---|
| Exact branch search returns no result for a known slash-containing branch | Read a known file with the branch as `ref`, then use commit-to-branch comparison. Treat the comparison result, not search recall, as the branch identity check. |
| Container Git cannot resolve the remote host | Keep authoring and publication separate. Use the GitHub connector for current remote reads and a verified bundle only as local recovery material; never present a stale bundle as the current baseline. |
