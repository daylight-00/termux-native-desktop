# 0007 — Third Device Preflight: Deploy Return Status

## Context

After syncing commit `eafc651`, the real device reran repository smoke tests and migration dry-runs.

Observed results:

```text
shell layout smoke test: PASS
adopt user env smoke test: PASS
uv-base definition validation: PASS
cpython artifact validation: PASS
cpython runtime validation: PASS
```

`deploy-smoke.sh` printed no PASS line, while both adoption and deployment dry-runs completed successfully.

No live mutation had occurred.

## Root cause

The dry-run simulation patch added this as the final command in `ensure_dir()`:

```bash
[ "$DRY_RUN" -eq 1 ] && mark_planned_dir "$dst"
```

In dry-run mode the command returns zero.

In real deployment mode the left-hand test returns status 1, so the function itself returns status 1. Because `tools/deploy` runs with `set -e`, the first real-mode call to `ensure_dir` terminates deployment.

This explains the exact symptom:

```text
dry-run: succeeds
real deploy smoke: exits before PASS
```

The failure was a shell function return-status bug introduced by the dry-run simulation patch.

## Fix

Replace the status-bearing AND-list with an explicit conditional and explicit success return:

```bash
if [ "$DRY_RUN" -eq 1 ]; then
    mark_planned_dir "$dst"
fi
return 0
```

## Test hardening

The deployment smoke test previously used bare `[ ... ]` assertions under `set -e`. A failed assertion could therefore terminate silently without identifying which contract failed.

The test now:

- captures dry-run output and prints it on failure;
- captures real deployment output and prints it on failure;
- uses labeled assertion helpers;
- reports the exact missing or incorrect live path;
- prints PASS only after all postconditions are verified.

## Safety conclusion

The staged migration process prevented the return-status bug from reaching the live device:

```text
repository change
    -> device smoke test
    -> dry-run review
    -> bug found
    -> no apply performed
```

This finding reinforces the rule that both dry-run and real-mode temporary-home tests are required before running the actual live deployment tool.

## Required revalidation

After syncing the fix commit:

```bash
bash tests/repository/deploy-smoke.sh
bash tests/repository/shell-layout-smoke.sh
bash tests/repository/adopt-user-env-smoke.sh

./tools/adopt-user-env --dry-run
./tools/deploy --dry-run
```

Expected repository-level results:

```text
deploy smoke test: PASS
shell layout smoke test: PASS
adopt user env smoke test: PASS
```

Only after all three tests pass and both dry-runs are reviewed should live adoption begin.
