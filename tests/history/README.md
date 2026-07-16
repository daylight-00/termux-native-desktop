# Historical repository tests

The `tests/history/` directory preserves stage-specific smoke tests whose intermediate semantic state has been superseded.

They are not part of current `tests/run-repository --docs`, `--fast`, or `--full` gates. To reproduce one, check out the historical commit at which its associated stage was current and run it there. Current aggregate authority is verified by the current checker set under `tests/repository/`.

See `docs/operations/TEST_AUTHORITY.md`.
