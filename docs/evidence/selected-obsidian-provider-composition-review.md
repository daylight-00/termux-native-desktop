# Selected Obsidian provider composition review

## Decision

```text
composition decision:             REVIEWED_BLOCKED_INCOMPLETE
accepted bounded provider roots:  29
accepted exact members:           37
included members:                 36
deferred members:                  1
selected GTK identity gaps:        6
target manifest allowed:          NO
activation allowed:               NO
```

The accepted-member table is generated at `selected-provider-composition-members.tsv`; remaining selected identities are generated at `selected-provider-composition-gaps.tsv`. The review is non-materializing and does not authorize target paths, aliases, copies, installation, deployment or activation.

## Latest bounded tranche

Exact project-produced `libXdamage.so.1.1.0` is included for the selected GTK 3.24.49 GDK X11 damage-extension linkage and recorded damage-region surface only. The selected runtime alias is `libXdamage.so.1 -> libXdamage.so.1.1.0`. The exact Class B recipe candidate remains separated from its private qualification harness, while the producing package/member record remains Class C because supplier publication is absent.

The decision accepts neither the unversioned development alias nor headers, pkg-config metadata, documentation, supplier publication, complete X11/GTK composition, target population or activation. Exact `libXfixes.so.3`, `libX11.so.6`, libc and the loader remain the bounded direct dependency closure.

## Remaining gaps

The coupled selected `libatk-bridge-2.0.so.0.0.0`, `libatk-1.0.so.0.25611.1`, and `libatspi.so.0.0.1` family remains `BLOCKED_NO_TERMUX_GLIBC_PROVIDER_CANDIDATE`. Only ordinary bionic package entries were observed and the pinned glibc recipe source has no producing root. This is not authority to copy bionic bytes or activate accessibility or D-Bus services.

The selected `libgdk-3.so.0.2417.32` and `libgtk-3.so.0.2417.32` pair remains `BLOCKED_NO_TERMUX_GLIBC_PROVIDER_CANDIDATE`. Ordinary bionic GTK does not authorize glibc provider bytes or infer backend, settings, theme, accessibility, input, printing or service behavior.

Selected `libselinux.so.1` remains `BLOCKED_NO_TERMUX_GLIBC_PROVIDER_CANDIDATE`. Android and ordinary Termux/bionic SELinux libraries are boundary evidence only and do not authorize a cross-world alias, policy loading, relabeling or glibc compatibility.

All six selected identities remain unresolved. The three AT-SPI2/ATK identities now have one exact qualified atomic local candidate family with provider authority still open; the GTK 3 core pair and libSELinux remain reviewed no-candidate blockers. The Class D composition remains incomplete and no target manifest is allowed.

## Production-boundary disposition and next tranche

The AT-SPI2/ATK production candidate lane is complete at the qualification layer only. The next tranche is `AT_SPI2_ATK_ATOMIC_BOUNDED_PROVIDER_AUTHORITY_REVIEW`: review the exact Class B recipe and coherent Class C three-member family for one narrowly bounded selected GTK accessibility capability, or retain a precise provider blocker. It does not authorize supplier publication, package installation, D-Bus activation, accessibility enablement, target population, deployment, or activation.
