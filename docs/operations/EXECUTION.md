# Agent execution and result-review method

## Authoring sequence

```text
1. establish the exact verified repository branch, HEAD, and tree;
2. inspect only the controlling documents and named evidence;
3. author changes in an isolated local worktree;
4. run syntax, canonical, negative, and regression tests;
5. create one exact patch, or a Git bundle when ancestry matters;
6. construct and simulate one wrapper;
7. package one .tar.zst and verify it before publication;
8. fetch the published object and verify byte identity again.
```

Distinguish these states:

```text
prepared
executed
result received
result verified
accepted
```

A prepared package is not an applied repository change.

## Mutating wrapper contract

Every mutating wrapper should contain all feasible acquisition, checksum, extraction, repository gating, test, commit, push, verification, archive, and upload logic so the user normally runs one command. It should:

- pin the expected base HEAD and tree;
- require the intended branch and a clean tracked worktree;
- preserve unrelated untracked paths;
- perform any network-backed repository fetch/pull only in the user's Termux checkout and verify the remote branch before mutation;
- verify the repository delta checksum and exact changed-path set;
- run `git diff --check` and bounded tests;
- use canonical author, committer, and signoff: `daylight-00 <hwjang00@snu.ac.kr>`;
- commit only after all pre-push gates pass;
- re-check the remote immediately before push;
- perform repository clone, pull, and push only from the user Termux environment;
- verify the remote after push;
- create and upload a result archive on success and failure;
- restore the pinned base only when failure occurs before a successful push;
- never attempt rollback after a confirmed successful push.

A shell test uses a real timeout and closed stdin:

```bash
timeout --foreground --kill-after=10s <seconds> bash <script> </dev/null
```

Under `set -u`, declare local variables separately from assignments and command substitutions.

## Result archive contract

Prefer small structured files over raw output:

```text
transaction-status.txt
final-git-state.txt
remote-state.txt
phase metadata or summary
next-state.txt
git-status-porcelain.txt
commit.txt
```

Retain detailed logs, but inspect them only with targeted `grep`, bounded `tail`, or exact member extraction after a structured failure signal.

Structured result members must match their declared format. A `.tsv` file contains real tab delimiters, not escaped `\t` text, and is parser-validated before archival. A formatting defect is recorded explicitly during result review even when independent evidence makes it non-blocking.

## Review order

```text
1. locate the exact user-results object;
2. fetch raw bytes;
3. verify the user-reported SHA-256;
4. test zstd integrity;
5. reject unsafe paths, links, or special members;
6. inspect transaction-status.txt;
7. inspect final-git-state.txt and remote-state.txt;
8. inspect bounded phase metadata and next-state.txt;
9. verify clean tracked state and canonical commit identity;
10. use a lightweight remote read when independent publication confirmation is useful;
11. only then author the next dependent phase.
```

Tree hashes are the cross-session content invariant. Record commit and tree because commit metadata can differ while content remains identical.

## Failure boundary

- Before push: restore the pinned base and only the expected changed paths.
- After a confirmed push: do not reset local or remote history merely because packaging, upload, or later verification failed. Report the pushed state and repair the later stage separately.
- If the remote moved: abort; never force the branch.

## Scope discipline

A review, collector, request-definition, or classification phase must not silently perform acquisition, installation, extraction, runtime mutation, provider promotion, or target population. Preserve the claim boundary of the active task and controlling decision.
