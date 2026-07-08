# Session setup

The hardened `startxfce-x11` launcher is described by `experiments/desktop/session-launch/README.md`, but its canonical source file is not present in the current GitHub tree.

The live on-device copy or source-linked repository file must be recovered and reviewed before `setup/session/startxfce-x11` is committed. Do not reconstruct it from an old report: the experiment record documents several field-hardening changes that postdate earlier representative scripts.

`scripts/deploy-gl.sh` therefore treats this launcher as optional and will not replace a working local target with a dangling symlink.
