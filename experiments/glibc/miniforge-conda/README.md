# Miniforge / Conda on the native glibc runtime

**Status:** passed  
**Provenance:** first-hand session report (`report.md`)

## Question

Can an ordinary Linux aarch64 Miniforge/Conda stack run from native Termux as glibc processes, without using PRoot as the runtime, and execute real compiled packages?

## Hypothesis

If the bootstrap and installed prefixes are adapted at the ELF/runtime boundary, Conda can remain a conventional Linux package ecosystem while execution stays native to the Termux host.

## Procedure

The experiment adapted the official Miniforge installer and runtime prefixes rather than replacing Conda internals:

1. identify the Termux glibc loader and runtime paths;
2. patch the bootstrap execution path and installed ELF interpreters/RPATH as required;
3. clear incompatible Termux preload/library-path inheritance at glibc process entry;
4. keep the Conda package cache pristine and patch installed prefixes/environments instead;
5. validate Conda, Mamba, environment creation, Python, native modules, and NumPy.

## Evidence

The preserved report records successful:

- Miniforge installation;
- Conda and Mamba execution;
- creation of a Python 3.11 environment;
- imports of native-library-using standard modules;
- NumPy 2.4.6 execution with the expected array result.

It also records concrete failure signatures around linker scripts, Termux preload injection, and Conda package-cache integrity checks.

## Result

Passed. A practical compiled-package ecosystem can exist in the glibc world without making PRoot the application runtime.

## Decision

Keep Conda/Miniforge as an available glibc workload and package ecosystem. The result is also the baseline for the planned PyMOL experiment.

The earlier `conda-pilot` stub has been replaced by this canonical record because the first-hand report preserves the actual experiment in much greater detail.

See [`report.md`](report.md) for the full session-derived report.
