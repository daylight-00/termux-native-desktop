# Operational troubleshooting

## Capability-failure triage

Use the limitation IDs in [`platforms/chatgpt-web-limitations.tsv`](platforms/chatgpt-web-limitations.tsv).

```text
one representative probe
    -> environmental/tool-contract failure confirmed
    -> stop equivalent retries
    -> preserve exact coordinates and error
    -> use the registered fallback authority
```

Do not turn an unavailable web capability into repeated trial-and-error. The active task should continue through a bundle, connector exact-read, user-Termux acquisition/analyzer wrapper, device runner, or later-turn Drive transfer as appropriate.

| Symptom | Do not | Proven response |
|---|---|---|
| DNS resolution or outbound download fails while exact dependency/source bytes are required | Keep trying mirrors, proxy tricks, package managers, or versions; disable digest checks | Generate one Termux acquisition/analyzer wrapper with exact URL and SHA-256. Return verified bytes when agent-side analysis is required, otherwise return compact package/ELF metadata. |
| GitHub code search misses a file or ref already known to exist | Infer absence or rebuild the repository from search snippets | Fetch the exact path at the exact ref, compare commits, or use the user's Git object database/full bundle. |
| A required fact is Android-, loader-, package-, GPU-, filesystem-, or runtime-specific | Treat synthetic sandbox behavior as authoritative | Generate the smallest bounded Termux runner and review its result archive. |
| A combined test call is terminated by an outer execution limit | Blindly rerun the full suite | Inspect logs and process state, then split the same test set into independent bounded calls or poll a persistent shell session. |

## Drive and connector bottlenecks

| Symptom | Proven response |
|---|---|
| Binary file is not found by Drive search | List the exact canonical folder and select by full filename and creation time. |
| Fetched binary appears as a local `.bin` | Treat it as raw bytes; verify the expected SHA-256 and zstd stream before extraction. |
| Local upload path is rejected | Confirm the file is anywhere under `/mnt/data`; paths outside that subtree cannot be rewritten. |
| The first upload after runtime initialization or reset blocks local-path-to-file-reference rewriting, including in an existing chat | Keep Drive as the primary path, do not repeat the blocked call for the current delivery, expose identical bytes through a user-visible sandbox link, then attempt Drive first again on the next outbound upload if the runtime persists. |
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
