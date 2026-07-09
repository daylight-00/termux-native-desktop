# Shell module

The shell module owns the personal interactive Bash bootstrap and generic shell behavior.

It does not own capability-specific policy. The gl and uv-base modules contribute their own shell fragments under `~/.config/bash/conf.d/`, while the shell module owns the final cross-capability PATH ordering policy.

Live composition:

```text
$HOME/.bashrc
    -> generic shell files
    -> conf.d/40-gl.sh
    -> conf.d/60-uv-base.sh
    -> conf.d/99-path-policy.sh
```

The legacy Conda line that sourced `~/miniforge3/etc/profile.d/conda.sh` is intentionally not preserved: live inspection established that `~/miniforge3` is absent and `conda` is not on PATH. Future glibc Conda integration belongs to the gl execution domain and must be reintroduced explicitly from its validated prefix/runtime boundary rather than by reviving the stale native-shell line.
