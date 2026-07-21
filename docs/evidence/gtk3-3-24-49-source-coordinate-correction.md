# GTK 3.24.49 source-coordinate correction

## Decision

```text
previous project-selected commit: 7a7e86ecab67e7cf65f066dae2e02ae74d653ced
official tag object:             9003f198803b9b8b1d7def25a2359f8ebb4b25cf
official tag commit:             198aeace1e9e119c77f4d669bd8efdf337828ad1
official source archive SHA-256: a2958d82986c81794e953a3762335fa7c78948706d23cced421f7245ca544cbc
source archive/tag tree:          byte-manifest equivalent
source-coordinate decision:       CORRECTED_TO_OFFICIAL_TAG_COMMIT
authority widening:               NONE
repository build/install effect:  NONE
```

The previous project-selected commit was not the GTK 3.24.49 release commit. It is superseded for every current GTK 3.24.49 source, consumer-binding, recipe and update/rollback statement by the peeled commit of the official `3.24.49` tag.

The authoritative read-only probe result has SHA-256 `782136c4f95bf4cd56dc0b9861743a4e8eb12ebd07227062ed4552b6719ab250`. It fetched tag object `9003f198803b9b8b1d7def25a2359f8ebb4b25cf`, peeled it to commit `198aeace1e9e119c77f4d669bd8efdf337828ad1`, downloaded the official GitLab archive, verified SHA-256 `a2958d82986c81794e953a3762335fa7c78948706d23cced421f7245ca544cbc`, and established byte-manifest equivalence between the archive and `git archive` of the tag commit. The probe also verified ordinary Termux recipe commit `01dfe9d72748ba6f15960ac3d0928e4f0e1c28cf`, glibc recipe base `9bdd20c1d36524a0ab016d9b71c748b0cbb20a34`, framework commit `ec0fa2fe2f0176266928c180ee9382224e94c22f`, the local glibc index, and package/live-prefix/repository invariance.

## Consumer-binding revalidation

The official tag commit preserves the previously accepted bounded consumer relations:

- `meson.build` blob `08337ec70cf1c006720eb3ab78a8beac32c898f5` declares optional `xdamage`, includes it in the X11 package set when found, sets `HAVE_XDAMAGE`, and declares required `atk-bridge-2.0` for X11.
- `gdk/x11/meson.build` blob `754ae0a6158003385dc3cbfda2fa17c23eb5c347` includes `xdamage_dep` in the GDK X11 backend dependency set.
- `gtk/meson.build` blob `ea866d8231c2a5fa9b1972c4b11148c35cd228b8` links GTK to GDK and includes `atkbridge_dep` in the GTK dependency set.
- `gtk/gtkaccessible.h` blob `9c2229b3e886b3dd3c8f0c8855d484bdd9f936f1` defines `GtkAccessible` with `AtkObject` as its parent.

Therefore `LIBXDAMAGE-PROV-001` and `ATSPI2-CORE-PROV-001` retain their existing exact bounded scopes. This correction does not add providers, members, claims, composition authority, service authority, target population, or activation.

## Recipe-shape result

The probe found 19 Meson options, six backend/print option rows, 1,061 module/schema/theme/settings/printing/portal/accessibility/service-related source paths, and four ordinary-recipe dependency tokens without a direct current index/recipe-root match. Those four tokens are not all runtime ELF blockers: project-produced `libxdamage` is already a bounded provider, while `gtk-update-icon-cache`, `shared-mime-info`, and `liblzma` require explicit package/data/tool treatment in the production recipe design.

## Next boundary

The next valid action is to design the exact GTK 3.24.49 glibc production recipe and isolated build around commit `198aeace1e9e119c77f4d669bd8efdf337828ad1` and archive SHA-256 `a2958d82986c81794e953a3762335fa7c78948706d23cced421f7245ca544cbc`. The design must explicitly choose X11/Wayland/Broadway and print backend states, bind project-produced libXdamage and AT-SPI2 records, separate runtime libraries from data/build tools, retain the GDK/GTK pair atomically, and keep modules, schemas, settings, themes, printing, portal and service activation outside candidate qualification unless separately reviewed.

## Prohibited inference

This correction does not qualify a recipe or package, grant GTK provider authority, accept one member independently, authorize publication or installation, restore schemas or modules to active paths, start display/D-Bus/accessibility/portal/printing services, populate a target, deploy, or activate a selected generation.
