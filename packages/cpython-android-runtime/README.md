# CPython Android runtime consumer package

This package records the consumer-side identity and validation contract for the custom Android CPython runtime produced by the companion `cpython-android-cli` project.

The runtime artifact is external payload state and is not tracked in Git.

Current accepted identity:

```text
artifact: cpython-3.14-aarch64-linux-android-for-uv.tar.gz
producer: daylight-00/cpython-android-cli
target:   aarch64-linux-android
Python:   3.14.6
SHA-256:  7083ad89661d73278c2165dfff7506a6de26c8ec9471d6621a5c06c3aa9a49be
loader:   /system/bin/linker64
install:  $HOME/opt/cpython-3.14/prefix
```

Ownership boundary:

```text
cpython-android-cli
    source + build + artifact production

termux-native-desktop
    artifact identity + receipt + installation + validation + workstation use

uv-base
    consumer of the installed interpreter
```

The 22 MiB archive observed under `$HOME/uv-base/` is misplaced input state. It should be moved out of the live uv project during the later device migration; this refactor does not delete it automatically.
