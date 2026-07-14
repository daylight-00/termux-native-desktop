# Agent execution method

## Authoring sequence

```text
1. establish the exact verified repository HEAD, tree and branch;
2. inspect only the controlling project documents and receipts;
3. author changes in a local Git worktree;
4. run syntax, canonical generation, negative and regression tests;
5. generate one patch with an exact expected path set, or a Git bundle when preserving merge ancestry is part of the requested result;
6. construct and simulate one wrapper;
7. package as one .tar.zst and verify it before upload;
8. fetch the uploaded object and verify it again.
```

Do not claim that a repository change is applied merely because a patch or package was prepared. Distinguish `prepared`, `executed`, `result received`, `result verified` and `accepted` states.

## Wrapper contract

Every mutating wrapper should:

- pin the base HEAD and tree;
- require the intended branch and a clean tracked worktree;
- record unrelated untracked paths and avoid deleting them;
- fetch and verify the remote branch before applying the patch;
- verify the patch checksum and exact changed-path set;
- run `git diff --check` and bounded tests;
- use canonical author, committer and signoff:
  `daylight-00 <hwjang00@snu.ac.kr>`;
- commit only after all gates pass;
- re-check the remote immediately before push;
- push from the user environment;
- verify the remote after push;
- create and upload a result archive on both success and failure;
- restore the base HEAD and expected paths when failure occurs before a successful push;
- never attempt rollback after a confirmed successful push.

A shell test must use a real timeout and closed stdin:

```bash
timeout --foreground --kill-after=10s <seconds> bash <script> </dev/null
```

Under `set -u`, declare local variables separately from command substitutions. Avoid forms such as `local name=$(...)` when later arguments in the same declaration depend on `name`.

## Result archive contract

Prefer small structured files over raw logs:

```text
transaction-status.txt
final-git-state.txt
remote-state.txt
phase summary or metadata
next-state.txt
git-status-porcelain.txt
commit.txt
```

Retain full logs in the archive, but inspect them only through targeted `grep`, `tail` or exact file selection after a failure.

## Result review order

```text
1. locate the exact user-results item;
2. fetch raw bytes;
3. verify the user-reported SHA-256;
4. test zstd integrity;
5. reject unsafe paths, links or special members;
6. inspect transaction-status.txt;
7. inspect final-git-state.txt and remote-state.txt;
8. inspect phase metadata and next-state.txt;
9. verify clean tracked state and canonical commit identity;
10. use a lightweight GitHub read to confirm the commit and branch;
11. only then author the next phase.
```

Tree hashes are the cross-session content invariant. Record both commit and tree because commit metadata can differ even when the repository content is identical.

## Scope discipline

A review, collector or request-definition phase must not silently perform acquisition, installation, extraction, runtime mutation, provider promotion or target population. Preserve the explicit claim boundary of the controlling project document.
