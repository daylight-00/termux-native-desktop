# 0138 — Selected Obsidian Application Payload, Launcher and Supplement Authority Boundary

## Status

Repository-side authority review completed at:

```text
branch:
    docs/post-graphics-architecture-audit

base HEAD:
    84d8d495e10521837a7d5bf4c3e4253eb221ed7f

base tree:
    f8df6be56720fc009785f301fc402a6fa45b71ab
```

Verdict:

```text
application identity-class separation:
    PASS

repository-owned launcher source supply:
    PASS / BOUNDED CURRENT EVIDENCE

historical promoted GUI launcher binding:
    PASS / EXACT UNCHANGED SOURCE BLOB

upstream payload exact supply identity:
    OPEN

application supplement membership:
    OPEN

application release update/rollback contract:
    BOUNDED / EXECUTION OPEN

ApplicationRuntimeComposition:
    NOT REACHED

target population, extraction, materialization and activation:
    BLOCKED
```

No device transaction was required. This record normalizes existing repository and accepted receipt evidence; it does not acquire, extract, patch, publish or launch an application payload.

## Authority and inputs

Controlling precedence remains:

```text
system-foundation constitutional documents
    -> 0116 provider-authority intervention
    -> 0115 and 0112 accepted oracle/runtime facts
    -> 0135 audit corrections
    -> 0136 normalized coverage/registry/alias/schema state
    -> 0137 world/locale/loader lifecycle boundary
    -> this application authority boundary
```

Primary evidence:

```text
experiments/glibc/obsidian-appimage/report.md
packages/obsidian/README.md
packages/obsidian/launcher/obsidian
packages/obsidian/launcher/obsidian-app
tools/deploy

docs/refactor/0083-expanded-graphics-policy-predeploy-and-live-installation-pass.md
docs/refactor/0089-current-obsidian-gpu-environment-and-primary-identity-pass.md
docs/refactor/0090-current-obsidian-cpu-policy-and-survival-pass.md
docs/refactor/0091-scoped-graphics-policy-promotion-closure.md
docs/refactor/0112-selected-obsidian-passive-map-selection-diagnostic-pass-and-contract-decision.md
docs/refactor/0135-selected-obsidian-provider-profile-lock-draft-architecture-audit.md
docs/refactor/0136-selected-obsidian-provider-authority-coverage-and-lock-semantics-normalization.md

experiments/glibc/selected-obsidian-provider-authority/review/
    authority-coverage-ledger/application-local.tsv
    authority-coverage-ledger/set-and-application-requirements.tsv
    application-authority-boundary.tsv
    unresolved-authority-ledger.tsv
```

## Decision 1 — five application identity concepts remain separate

The application authority model is:

```text
APPLICATION_PAYLOAD_IDENTITY
    exact upstream Obsidian/Electron release artifact and extracted payload lineage

APPLICATION_LOCAL_REFERENCE_IDENTITIES
    selected AppDir/$ORIGIN objects whose locality must remain payload-owned

APPLICATION_LAUNCHER_SUPPLY_IDENTITY
    repository-owned GUI and CLI launch-policy sources

APPLICATION_DOMAIN_SUPPLEMENT_IDENTITIES
    named application-domain additions accepted only after generic/shared ownership review

APPLICATION_RELEASE_TRANSACTION
    compatibility and rollback tuple across accepted payload, launchers and supplements
```

None of these identities may substitute for another.

In particular:

```text
96 first-generation contents
    != application payload

11 application-local reference identities
    != complete payload aggregate

repository launcher source
    != upstream payload supply

historically selected external provider
    != accepted application supplement

working promoted launcher
    != accepted ApplicationRuntimeComposition
```

## Decision 2 — payload evidence is version-bounded, not reconstructable supply authority

The AppImage onboarding report establishes:

```text
application:
    Obsidian 1.12.7

architecture:
    arm64

input format:
    Type-2-style AppImage with embedded SquashFS

behavioral result:
    extraction, adaptation, dependency verification, GUI startup, GPU validation,
    CLI integration and clean rebuild PASS
```

This is accepted historical runtime evidence.

The repository does not currently retain an authority record containing all of:

```text
exact upstream release locator/channel
exact AppImage filename
size
SHA-256
signature or release-authenticity policy
immutable retained source artifact
exact extraction tool/version and offset receipt
complete extracted-tree manifest
exact adaptation receipt
```

Therefore:

```text
Obsidian 1.12.7 arm64 AppImage behavior:
    ACCEPTED / BOUNDED

APPLICATION_PAYLOAD_IDENTITY:
    OPEN EXACT SUPPLY
```

The historical clean rebuild proves repeatability from the retained device artifact at that time. It does not make the current repository capable of clean payload reconstruction.

## Decision 3 — eleven application-local identities are reference topology

The normalized denominator contains eleven application-local rows:

```text
chrome_100_percent.pak
chrome_200_percent.pak
icudtl.dat
en-US.pak
resources.pak
v8_context_snapshot.bin
libEGL.so
libGLESv2.so
libffmpeg.so
libvulkan.so.1
obsidian
```

Accepted claim:

```text
these objects belong to the observed AppDir/$ORIGIN application-local topology;
provider composition must preserve valid local selection and reject unauthorized shadowing.
```

Rejected claims:

```text
the eleven rows are the complete upstream payload;
the eleven rows define an acquisition artifact;
the eleven rows are members of the 96 first-generation contents;
the eleven rows may be copied into an external provider generation;
the eleven rows authorize target paths or payload materialization.
```

Every accepted payload release must regenerate its own exact local inventory and locality proof.

## Decision 4 — current launcher source supply is exact and bounded

At the reviewed base:

```text
CLI source:
    packages/obsidian/launcher/obsidian
    mode: 100755
    Git blob: 42f1c164f77804822f6773c34b232cc205c59fb3
    SHA-256: f9787804d6e17e1e53f7096890d352c05247cd902e73312797d27967516bc751

GUI source:
    packages/obsidian/launcher/obsidian-app
    mode: 100755
    Git blob: b3f131392f0aeed9ba9d45b9d13ec7531fe477c7
    SHA-256: 010de5793e9e28c77277f0801e10ae0841e60d7ff432770644e03b54f0a66aad

publication source:
    tools/deploy
    mode: 100755
    Git blob: 97b26780d3bb8fb71b190ca9e5e8144caa170661
    SHA-256: 1de55639dae1affe2b6447a3ef854f8e069c4a30a5c2e3769936d31c8877d297
```

The same launcher and deploy blobs occur at the canonical live-receipt commits:

```text
3384bf136f3f35f7ab1d86b2005c2e7559d7e298
    promoted Obsidian GPU receipt

5ab13fd6c2af5843abf7bbff3a8a26f46a8e84b5
    promoted Obsidian CPU receipt

07b2f9a6f8f985fb3f152abd77c0ad3f04237cc9
    post-graphics architecture midpoint
```

The receipts observed:

```text
$HOME/gl/bin/obsidian-app
    -> canonical checkout packages/obsidian/launcher/obsidian-app
```

and broader deployment evidence covered both public Obsidian launcher symlinks.

Accepted boundary:

```text
repository source identity:
    ACCEPTED

current GUI CPU/GPU launch-policy behavior:
    ACCEPTED / BOUNDED TO EXISTING PAYLOAD AND RECEIPTS

CLI wrapper source:
    ACCEPTED / USER-REGISTERED CLI BINDING CONDITIONAL

checkout-linked public symlink publication:
    ACCEPTED CURRENT IMPLEMENTATION ONLY
```

Still open:

```text
future non-checkout launcher publication identity;
atomic launcher update and rollback;
launcher compatibility across exact accepted payload releases;
final target domain/path and generation/current binding.
```

The current public paths are integration adapters, not permanent architecture identities.

## Decision 5 — supplement class accepted, membership remains open

`APPLICATION_DOMAIN_SUPPLEMENT_IDENTITIES` is a valid application authority class.

It may contain a bounded object only when evidence establishes:

```text
a named Obsidian/Electron capability and consumer;
exact object/source/supply identity;
why application-domain ownership is preferable to a generic shared authority;
necessity for the accepted payload/launcher contract;
update and rollback coupling;
no collision with application-local or protected-world ownership.
```

The following shortcuts are rejected:

```text
historically selected object
    -> application supplement

fallback app.obsidian.supplement classifier seed
    -> final semantic authority

first-generation membership
    -> application composition inclusion

working broad-farm runtime
    -> final application supplement set
```

No supplement member is accepted for composition by this record.

## Decision 6 — application release transitions are compatibility transactions

Payload, GUI launcher, CLI launcher, publication mechanism and supplements remain separate lifecycle domains.

A future accepted application release must nevertheless validate one compatible tuple:

```text
exact payload supply and extracted-tree lineage
+ compatible repository launcher sources
+ accepted named supplement set
+ accepted provider/world composition references
+ declared CPU/GPU and application-state gates
+ verified previous-release rollback candidate
```

Receipt-local test configuration and normal user data remain separate mutable application state. They are not immutable payload bytes, supplements or rollback authority.

This lifecycle contract does not define the tuple yet and does not authorize activation.

## Ledger effect

`application-authority-boundary.tsv` now records seven non-materializing application contracts:

```text
APP-001 exact payload boundary
APP-002 application-local reference topology
APP-003 GUI launcher supply
APP-004 CLI launcher supply
APP-005 current publication mechanism
APP-006 supplement identity-class boundary
APP-007 application release transition
```

`AUTH-010` becomes:

```text
OPEN_CONTRACT
```

Accepted:

```text
identity classes are separated;
historical payload version/architecture/input format and behavior are bounded;
eleven application-local roles are bounded reference topology;
current repository GUI/CLI launcher sources are exact;
historical promoted GUI binding is tied to the unchanged exact source blob;
current checkout-symlink publication is bounded as implementation only;
supplement class and release lifecycle rules are defined.
```

Open:

```text
exact upstream payload supply/acquisition/retention;
complete extracted-tree and adaptation receipt;
named supplement membership and candidate-source authority;
future launcher publication and atomic update/rollback;
accepted payload/launcher/supplement composition tuple;
executed application release rollback.
```

## Next valid repository task

```text
CLOSE_EXACT_OBSIDIAN_PAYLOAD_SUPPLY_AND_NAMED_SUPPLEMENT_MEMBERSHIP
```

Proceed repository-side in this order:

```text
1. seek existing evidence for the exact retained Obsidian 1.12.7 AppImage filename,
   size, SHA-256, release locator and extraction/adaptation receipt;
2. if unavailable, define one bounded read-only payload-identity collector without
   downloading, extracting, patching or launching anything;
3. enumerate only named supplement candidates and compare each against generic
   owning authorities before accepting application-domain membership;
4. keep ApplicationRuntimeComposition and all target rows blocked.
```

## Claim boundary

This record proves:

```text
application authority identity classes are explicit and non-interchangeable;
the current repository launcher source identities are exact;
accepted live GUI launcher receipts bind to the same unchanged GUI source blob;
the historical payload claim is correctly bounded below exact supply identity;
supplement membership cannot be inferred from selected or fallback classification;
application release update/rollback gates are defined without activation.
```

It does not prove:

```text
clean reconstruction of the Obsidian payload;
current retention of the original AppImage;
complete payload tree identity;
any final supplement member;
final generic/platform provider choice;
ApplicationRuntimeComposition;
target paths, modes, owners or aliases;
materialization, activation or rollback execution.
```

## Stop line

Do not:

```text
call Obsidian 1.12.7 an exact payload supply without filename/size/hash/release identity;
call the eleven application-local rows the complete payload;
call the 96 first-generation contents application payload;
classify all selected external objects as Obsidian supplements;
copy application-local objects into a provider generation;
turn public checkout symlinks into target-layout policy;
populate target rows;
write acquisition, extraction, adaptation or materializer code;
download, extract or patch an AppImage;
mutate packages, launcher, RPATH, generation, current or loader state;
materialize or activate a successor.
```
