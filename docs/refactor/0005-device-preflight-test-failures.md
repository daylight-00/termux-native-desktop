# 0005 — Device Preflight Test Failures

## Context

The first repository-level test run on the real Termux device was executed after syncing `refactor/module-package-layout` at commit `b34daf1`.

Observed output:

```text
deploy smoke test: PASS

shell layout smoke test:
    no PASS output

adoption smoke test:
    refusing to adopt modified file: <temporary-home>/.bashrc
    expected: 3c7b8682c4debff14f68fa2a239635aed7d13ec6c11918ddee8f59040245a7cf
    actual:   e317117629f67eaf80fc659cd932ceea7a39c06225c416f769876a04679b0916
```

The live system was not modified. The failures occurred entirely inside temporary test homes.

## Failure 1 — adoption fixture hash mismatch

### Cause

`tests/repository/adopt-user-env-smoke.sh` attempted to reproduce the captured legacy `.bashrc`, but its embedded fixture omitted two comment lines that exist in the actual device file:

```text
# gl layer commands first; upstream per-user tools second.
# Ensure gl wrappers take precedence over upstream registered binaries.
```

Because the adoption tool correctly validates exact SHA-256 identity before replacing personal files, the incomplete fixture was rejected.

This was a test-fixture defect, not an adoption-tool defect.

### Fix

- restore the exact two comment lines so the fixture reproduces the captured device file byte-for-byte;
- add an explicit fixture SHA-256 assertion before invoking the adoption tool.

The fixture must now equal:

```text
3c7b8682c4debff14f68fa2a239635aed7d13ec6c11918ddee8f59040245a7cf
```

Any future fixture drift fails immediately with a dedicated diagnostic rather than surfacing indirectly as an adoption refusal.

## Failure 2 — shell-layout test inherited legacy `VIRTUAL_ENV`

### Cause

The current device shell was started under the pre-refactor `.bashrc`, which sources the legacy `.uvrc` and exports:

```text
VIRTUAL_ENV=.venv
```

`tests/repository/shell-layout-smoke.sh` started a child interactive shell but inherited the parent process environment. The test then checked that the promoted shell configuration does not create a global `VIRTUAL_ENV`.

Because inherited environment and configuration-produced environment were not distinguished, the test failed before printing `PASS`.

This was a test-isolation defect, not evidence that the promoted shell module exports `VIRTUAL_ENV`.

### Fix

- explicitly `unset VIRTUAL_ENV` inside the child shell before sourcing the candidate `.bashrc`;
- preserve the assertion that `VIRTUAL_ENV` remains unset after configuration load;
- capture stderr and print it when the child shell fails, avoiding a blank failure section.

## Patch

Commit:

```text
70cfed632895eadd7467d5ee5a25863fe03827b9
    test: fix device shell and adoption fixtures
```

## Required revalidation

After fast-forwarding the local branch, rerun:

```bash
git fetch origin
git merge --ff-only origin/refactor/module-package-layout

bash tests/repository/deploy-smoke.sh
bash tests/repository/shell-layout-smoke.sh
bash tests/repository/adopt-user-env-smoke.sh
```

Expected result:

```text
deploy smoke test: PASS
shell layout smoke test: PASS
adopt user env smoke test: PASS
```

Only after these pass should the device identity checks and migration dry-runs continue.
