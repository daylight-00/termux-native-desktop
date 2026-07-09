# Repository Refactor Work Log

This directory is the low-level source of truth for the repository refactor from the legacy `setup/` layout to capability modules, external software package definitions, stable experiment provenance, and explicit deployment tooling.

## Working rule

Every structural change must be recorded here before or at the same time as the repository change. Session context is not authoritative.

## Documents

- `0001-current-state-inventory.md` — observed repository and live-system state before migration.
- `0002-ownership-map.md` — old path, new owner, new path, live target, and migration method.
- `0003-migration-plan.md` — ordered repository and live migration procedure.
- `MIGRATION_JOURNAL.md` — chronological execution log with commands, commit IDs, validation, and deviations.
- `repo-path-map.tsv` — machine-readable path mapping for moved tracked files.

## Refactor branch

`refactor/module-package-layout`

Base commit:

`3cf41d6fc47050b06e18e956a23cefe25e4fb82a`

## Environment limitation

The execution container cannot resolve `github.com`, so a normal network `git clone` is not possible inside this runtime. Repository reads and writes are performed through the authenticated GitHub connector. A local working mirror under `/mnt/data/tnd-refactor` stores the design documents, path maps, generated migration material, and validation records used to construct connector-backed Git commits.
