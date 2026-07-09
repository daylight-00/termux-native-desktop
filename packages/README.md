# Packages

`packages/` owns workstation-specific lifecycle definitions and integration for external software payloads.

A package answers:

> How is this external software acquired, built or adapted, installed, exposed, and validated on this workstation?

Current owners:

- `mesa-glibc/` — Mesa glibc build lifecycle and build environment.
- `vscode/` — official VS Code glibc application integration; currently the promoted launcher is present while full acquisition/adaptation definition remains to be promoted.
- `obsidian/` — Obsidian glibc application integration; currently package-owned launchers are present while the AppImage acquisition/adaptation procedure remains documented by its experiment.

Package directories do not imply that external payload trees belong in Git. Runtime payloads remain outside Git and are reconstructed or reacquired from tracked definitions and source identities.
