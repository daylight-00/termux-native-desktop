# Active task: produce the GdkPixbuf 2.42.12 provider candidate

> Task ID: `produce-gdkpixbuf-2-42-12-provider-candidate`
>
> Expected state on completion: one exact scratch-built `libgdk_pixbuf-2.0.so.0.4200.12` candidate is bound to official source, the five acquired GLib/libpng candidates and the accepted project `libjpeg.so.62`; loader-isolated JPEG and PNG file/memory evidence is returned. No provider authority, target population or activation occurs automatically.

## Objective

Produce the missing sixth member of the GdkPixbuf core provider tranche without selecting Debian oracle bytes.

## Why now

The composition review is blocked by 27 identities, and this six-member image-core tranche is the smallest coherent closure unit. The first acquisition bound five exact Termux candidates and proved that no pinned Termux GdkPixbuf package or recipe exists. A project-produced upstream candidate is therefore the only bounded next step that does not select Debian oracle bytes.

## In scope

- Verify and unpack official GdkPixbuf 2.42.12 source.
- Build one exact scratch candidate with the pinned GLib/libpng artifacts and accepted libjpeg provider.
- Record source, toolchain, build, ELF, dependency and mapped-object coordinates.
- Run JPEG and PNG file and memory decode controls.
- Return explicit blockers if tools or dependency closure are insufficient.

## Established inputs

```text
GdkPixbuf source version: 2.42.12
expected member:          libgdk_pixbuf-2.0.so.0.4200.12
expected SONAME:          libgdk_pixbuf-2.0.so.0
official source SHA-256:  b9505b3445b9a7e48ced34760c3bcb73e966df3ac94c95a148cb669ab748e3c7

exact GLib artifact:      glib-glibc 2.82.2-2 / d91fe120...
exact libpng artifact:    libpng-glibc 1.6.47 / b283540...
accepted libjpeg member:  libjpeg.so.62.4.0 / a537840...
```

The acquisition review is in [`../evidence/gdkpixbuf-core-provider-acquisition-result-review.md`](../evidence/gdkpixbuf-core-provider-acquisition-result-review.md).

## Build boundary

- Build only in `$HOME/.cache` scratch space.
- Use the existing Termux glibc compiler wrappers.
- Create a disposable build-tools venv from `packages/gdkpixbuf-glibc/build-env/pyproject.toml` and `uv.lock` with `uv sync --locked --no-python-downloads`; run Meson from that venv.
- Use the existing native Termux `ninja`; do not install or vendor a PyPI Ninja/CMake executable.
- Extract exact GLib/libpng artifacts into a scratch prefix; do not install them.
- Use the accepted project `libjpeg.so.62.4.0` candidate and exact libjpeg-turbo 3.1.0 headers.
- Build PNG and JPEG loaders into the GdkPixbuf shared library.
- Disable TIFF, GIF, other loaders, introspection, tests, installed tests, documentation, man pages and GIO sniffing.
- Require no `DT_RPATH` or `DT_RUNPATH`.

## Required evidence

- official source archive and checksum identity;
- exact build command, cross file and tool versions;
- candidate SHA-256, ELF class, machine, SONAME and `DT_NEEDED`;
- exact mapping of candidate GdkPixbuf, four GLib members, libpng and libjpeg;
- fixed JPEG and PNG decode through file and memory APIs;
- unchanged repository HEAD/tree/tracked status and unchanged live provider/deployment paths;
- result archive and upload digest.

## Required reading

- `docs/current/STATE.yaml`
- `docs/constitution/PRINCIPLES.md`
- `docs/decisions/0005-proportional-assurance-depth.md`
- `docs/evidence/gdkpixbuf-core-provider-acquisition-result-review.md`
- `packages/gdkpixbuf-glibc/README.md`
- `docs/evidence/selected-obsidian-provider-composition-review.md`
- `docs/evidence/libjpeg-so-62-loader-isolated-provider-authority.md`
- `experiments/glibc/selected-obsidian-provider-authority/review/gdkpixbuf-core-provider-acquisition-result-review.tsv`

## Pending external inputs

None. The official source archive is acquired by the bounded runner; exact GLib, libpng and libjpeg bytes are embedded in the runner.

## Next valid action

Execute the single self-extracting scratch-build runner and return its one final-status block.

## Out of scope

- Installing source or candidate bytes.
- Using Debian GdkPixbuf bytes as target authority.
- Accepting the six-member tranche before result review.
- Generating a target manifest.
- Population, deployment, selector mutation or activation.

## Stop conditions

Stop if official source identity cannot be verified, required build tools are unavailable, the object links to `libjpeg.so.8`, any expected candidate maps from the live prefix instead of scratch, an RPATH/RUNPATH remains, or protected tracked/live state changes.

## Completion criteria

- exact GdkPixbuf candidate produced or explicit build blocker returned;
- six candidate identities and mappings visible;
- JPEG and PNG file/memory matrix complete;
- no live or target mutation;
- provider authority remains a later repository decision.
