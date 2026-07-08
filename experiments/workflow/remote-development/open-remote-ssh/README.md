# Code OSS + Open Remote SSH

**Status:** unsuccessful in the tested configuration; failure stage isolated  
**Experiment date:** 2026-06-30  
**Provenance:** first-hand session report (`report.md`)

## Question

Can native Code OSS on Termux use `jeanp413.open-remote-ssh` to provide an SSH remote-development workflow while preserving an existing official `~/.vscode-server` installation on the remote host?

## Result

The extension reached remote execution and platform detection, but its generated installer selected a VSCodium REH download path that returned a deterministic 404 for the observed local version mapping.

The tested failure was therefore not a basic SSH-authentication or remote-shell failure. The report narrows it to the remote server download/version-selection path used by the tested Open Remote SSH extension build.

An extension upgrade and an explicitly compatible remote extension-host version were proposed next directions but were not validated in this experiment.

## Decision

Do not treat the tested Open Remote SSH configuration as a working replacement for the desired official VS Code remote workflow. Preserve the report because it identifies the actual installer stage and avoids destructive cleanup of the unrelated working `~/.vscode-server` tree.

See [`report.md`](report.md).
