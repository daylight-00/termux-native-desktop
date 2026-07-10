# 16. Debugging, Performance Measurement, and Experiment Design

Systems work becomes reliable when observations are converted into evidence chains rather than anecdotes. A crash, slowdown, or workaround is the start of investigation, not the conclusion.

## 16.1 Crash analysis direction

Normal execution reasoning goes downward:

```text
source
    -> binary
    -> process
    -> instruction
    -> syscall/kernel/device
```

Crash analysis often goes backward:

```text
signal
    -> thread
    -> PC/register state
    -> mapped ELF object
    -> stack unwind
    -> source location
    -> memory mapping
    -> prior syscall/ioctl events
    -> root-cause hypothesis
```

## 16.2 Signal is classification, not cause

Examples:

```text
SIGSEGV
    -> invalid mapping or permission-related memory access class

SIGBUS
    -> bus/mapping/alignment/object-related fault class

SIGABRT
    -> explicit abort or runtime-detected fatal condition
```

Do not infer the precise mechanism from the signal name alone.

For memory faults, inspect:

```text
signal code
fault address
PC
instruction
register operands
mapping permissions/type
```

## 16.3 PC versus fault address

These are different.

```text
PC
    -> address of instruction being executed

fault address
    -> memory address the instruction tried to access
```

Example:

```asm
ldr x5, [x3, #16]
```

If `x3 == 0`, the instruction address may be in `libfoo.so`, while the fault address is near `0x10`.

## 16.4 Mapping the PC to an object

With ASLR:

```text
runtime PC
    -> find containing mapping
    -> identify ELF object
    -> compute/resolve object-relative location
    -> symbolize with exact matching binary/debug info
```

A raw absolute address from one run may not be meaningful in another run.

## 16.5 Backtrace and stack unwinding

A backtrace reconstructs the active caller chain:

```text
#0 current function
#1 caller
#2 caller's caller
...
```

It is not a complete historical trace of every function ever called.

Unwinding can use:

```text
frame-pointer chains
unwind metadata
ABI rules
debug information
```

Optimization can inline functions, remove frame pointers, perform tail calls, and reorder code, making source-level interpretation more complex.

## 16.6 DWARF and debug information

DWARF provides structured debugging information that can describe relationships among:

```text
machine addresses
source files and lines
function scopes
types
variables
inline calls
unwind information
```

Machine code alone does not inherently know that address `X` corresponds to `renderer.c:742`.

## 16.7 Debug symbols and exact build identity

A useful crash-analysis artifact set is:

```text
core dump
exact executable
exact loaded shared objects
matching debug information
matching source revision
build options/toolchain identity
```

Using “almost the same” library build can produce misleading symbols or line mappings.

Record checksums and source commits.

## 16.8 Core dump

A core dump is a snapshot-like artifact of process state at termination. It can preserve memory and register/thread information for offline analysis.

It is not a complete time-ordered syscall or instruction trace.

Therefore combine:

```text
core/GDB
    -> crash-time process state

strace
    -> syscall history

application logs
    -> semantic events

GPU/kernel diagnostics
    -> device-side evidence
```

## 16.9 GDB

GDB can inspect:

```text
registers
memory
threads
stack frames
symbols
breakpoints/watchpoints
live process or core file
```

Useful conceptual commands:

```gdb
bt
info threads
thread apply all bt
info registers
x/i $pc
x/16gx ADDRESS
```

The exact command set should be used with an understanding of the target architecture and symbol quality.

## 16.10 `addr2line`, `objdump`, `readelf`

Each answers a different question.

```text
readelf
    -> ELF metadata and structure

objdump / llvm-objdump
    -> disassembly and object inspection

addr2line
    -> binary address/offset to source location when debug info matches

GDB
    -> integrated execution-state analysis
```

## 16.11 `strace`

`strace` observes syscall-boundary behavior.

Useful for:

```text
missing paths
plugin discovery
socket connections
mmap creation
process spawning
ioctl sequence
permission failures
```

It does not show every userspace function call.

Combine loader diagnostics and `strace` when investigating dynamic-link behavior:

```text
loader says: searching libfoo
strace says: which exact paths were opened and failed
```

## 16.12 Mapping a GPU fault path

A strong evidence chain can be:

```text
SIGBUS
    -> fault address
    -> mapping range
    -> mapping created by mmap(fd 17, offset ...)
    -> fd 17 refers to device/buffer object
    -> preceding ioctl sequence differs from working run
```

This turns a generic crash label into a mechanism-oriented hypothesis.

## 16.13 Crash location versus bug origin

Memory corruption can be detected later than it is caused.

```text
function A corrupts heap
    -> time passes
    -> function B calls free
    -> allocator detects corruption
    -> abort
```

Backtrace points to detection, not necessarily origin.

Use watchpoints, sanitizers, narrower reproductions, and differential experiments when necessary.

## 16.14 Sanitizers

Compiler instrumentation tools can detect classes of bugs closer to their origin.

Examples:

```text
AddressSanitizer -> memory safety bug classes
UndefinedBehaviorSanitizer -> selected undefined behavior
ThreadSanitizer -> data-race detection
```

Instrumentation changes timing and memory layout. A non-reproduction under a sanitizer build does not automatically disprove a race or layout-sensitive bug.

## 16.15 Performance: latency versus throughput

### Latency

Time for one operation to complete.

### Throughput

Amount of work completed per unit time.

A system can improve throughput through concurrency while individual request latency worsens, or reduce latency without increasing total throughput.

Always identify which metric matters for the workload.

## 16.16 Wall, user, and system time

Conceptually:

```text
wall time
    -> elapsed real time

user CPU time
    -> CPU time executing userspace code

system CPU time
    -> CPU time executing kernel work on behalf of process
```

A process can have long wall time and low CPU time because it waits for:

```text
I/O
network
locks
GPU fences
child processes
```

## 16.17 Profiling and sampling

A sampling profiler periodically observes execution state.

Conceptually:

```text
10,000 stack samples
    -> aggregate where CPU time appears concentrated
```

This helps answer:

```text
Where is CPU time spent?
```

not necessarily:

```text
What exact chronological event sequence caused the bug?
```

`perf` and tracing tools answer different questions from GDB and `strace`.

## 16.18 Benchmark design for PRoot versus direct runtime

Do not measure one mixed workload and call the result “PRoot overhead.” Separate mechanisms.

Suggested matrix:

```text
CPU-only computation
process spawn/exec
small-file stat/open/read loops
directory traversal
large sequential reads
large sequential writes with defined sync policy
build workload
GUI interaction workload
```

Control:

```text
same binaries where meaningful
same input data
same cache state definition
same thermal/power state as far as practical
multiple repetitions
reported variance
```

The purpose is not to prove one architecture universally faster. It is to identify where mediation costs matter for actual workstation workloads.

## 16.19 Controlled experiment design

A disciplined loop:

```text
baseline
    -> hypothesis
    -> change one meaningful variable
    -> collect evidence
    -> compare with control
    -> update hypothesis
```

Avoid changing ten environment variables and five libraries before declaring victory.

A useful project record distinguishes:

```text
observation
interpretation
proven conclusion
open mechanism
```

## 16.20 Reproduction harness

Turn manual sequences into scripts before deep debugging.

A good harness records:

```text
command line
environment diff
binary checksums
source/build identity
stdout/stderr
process tree
maps
trace logs
result status
```

This makes A/B comparison possible.

## 16.21 Validation gates

A validation gate is a repeatable test for one contract claim.

Examples:

```text
world-purity gate
    -> no foreign ABI libraries mapped

X11 gate
    -> window client reaches Termux:X11

Vulkan gate
    -> intended ICD selected and Adreno enumerated

Zink gate
    -> OpenGL renderer reports Zink/Turnip path

VS Code GPU gate
    -> GPU process remains stable and renderer evidence matches claim
```

A screenshot can be evidence of visible output, but not of an uninstrumented zero-copy path or a specific hidden buffer mechanism.

## References

- GDB documentation: <https://sourceware.org/gdb/current/onlinedocs/gdb.html/>
- GNU Binutils documentation: <https://sourceware.org/binutils/docs/>
- DWARF standard: <https://dwarfstd.org/>
- Linux `perf` documentation: <https://perf.wiki.kernel.org/index.php/Main_Page>
- Linux kernel tracing documentation: <https://docs.kernel.org/trace/>
- Project evidence policy: [`../../../STATUS.md`](../../../STATUS.md)
