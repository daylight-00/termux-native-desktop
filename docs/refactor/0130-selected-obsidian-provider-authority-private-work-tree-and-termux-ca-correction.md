# 0130 — Selected Obsidian Provider-Authority Private Work Tree and Termux CA Correction

## Status

```text
source-recipe receipt:
    PASS / ACCEPTED

first bounded binary artifact execution:
    FAIL DURING HTTPS CERTIFICATE VERIFICATION

failure cause:
    Python TLS trust did not resolve the Termux CA bundle

Downloads workspace policy:
    WITHDRAWN

private experiment work-tree policy:
    ACTIVE
```

## Correction

The earlier collector design incorrectly extended the archive-delivery convention into a general workspace convention and placed source inputs, raw `.deb` artifacts, and receipt archives under `$HOME/Downloads`.

On this device `$HOME/Downloads` resolves into Android shared storage. That surface has ownership, Git `safe.directory`, filesystem, and application-boundary behavior that is irrelevant and harmful for internal project work.

The repository already defines the correct local workspace convention through `.gitignore`:

```text
experiments/**/work/
```

Provider-authority local state now defaults to:

```text
experiments/glibc/selected-obsidian-provider-authority/work/
    source/
        termux-pacman-glibc-packages/
    artifacts/
        n3-exact-debs/
    receipts/
        unpacked/
        *.tgz
    tmp/
```

This tree is:

```text
inside Termux private storage;
ignored by Git;
owned by the Termux application user;
separate from tracked recipes and documentation;
reusable across bounded collector retries.
```

## Binary collector correction

The bounded binary artifact runner now uses:

```text
ARTIFACT_DIR:
    <provider-authority>/work/artifacts/n3-exact-debs

OUT:
    <provider-authority>/work/receipts/unpacked/<transaction>

ARCHIVE:
    <provider-authority>/work/receipts/<transaction>.tgz
```

The accepted source receipt remains at its already validated `$PREFIX/tmp` location and does not need to be regenerated merely because the later workspace convention changed.

## TLS correction

The Python collector already supports an explicit `SSL_CERT_FILE`. The runner now defaults it to:

```text
$PREFIX/etc/tls/cert.pem
```

The path must resolve to a file. A package-managed symlink is accepted because Termux may expose its CA bundle that way.

The collector continues to require:

```text
HTTPS only;
approved Termux package hosts only;
approved redirects only;
exact indexed byte size;
exact indexed SHA-256;
three bounded attempts;
partial-file removal after failure.
```

TLS verification is not disabled.

## Source collector correction

Future source-recipe collection defaults to:

```text
SOURCE_REPO:
    <provider-authority>/work/source/termux-pacman-glibc-packages

transaction temp:
    <provider-authority>/work/tmp

OUT and TGZ:
    <provider-authority>/work/receipts
```

An explicitly overridden external shared-storage source remains supported through command-scoped `safe.directory` and bundle isolation, but shared storage is no longer the default architecture.

## Current rerun boundary

Do not rerun the accepted source-recipe collector. Pull the corrected branch and rerun only:

```text
run-n3-binary-artifact-comparison.sh
```

The first failed binary transaction did not install or execute a package and did not create an accepted artifact. Its failed evidence root may remain as historical failure evidence.

## Stop line

Do not:

```text
use Android Downloads as the default internal cache;
disable TLS certificate verification;
set a global CA or Git trust exception merely for this transaction;
install downloaded artifacts;
run maintainer scripts;
mutate generation or current state.
```
