# 5. Processes, Threads, Syscalls, File Descriptors, and Signals

A program file is passive. A process is an executing instance with state. This distinction is the center of runtime reasoning.

## 5.1 Program versus process

An executable file can exist on storage without running:

```text
ELF file
    -> bytes, metadata, machine code
```

When executed, the kernel and dynamic loader construct a process:

```text
process
├── virtual address space
├── threads
├── registers
├── file descriptor table
├── signal state
├── credentials
├── environment
└── memory mappings
```

One executable can produce many simultaneous processes, each with its own state.

## 5.2 `execve` replaces the process image

A shell does not “open” an executable as if it were a document. It resolves a command name, then ultimately requests execution.

A simplified path is:

```text
shell
    -> PATH lookup
    -> fork/spawn strategy
    -> execve(path, argv, envp)
    -> kernel reads executable format
    -> ELF interpreter involved when dynamic
    -> process image replaced
```

The process identity relationship is subtle: `execve` does not necessarily create a new PID. It replaces the current process image.

This is why launch scripts often end with:

```sh
exec application "$@"
```

The shell process is replaced by the application. Signal handling and process-tree behavior become cleaner than leaving an unnecessary wrapper shell waiting above the application.

## 5.3 Process versus thread

A process contains one or more threads of execution.

```text
Process
├── shared address space
├── shared file descriptor table semantics
├── shared loaded libraries
│
├── Thread A
│   ├── registers
│   └── stack
├── Thread B
│   ├── registers
│   └── stack
└── Thread C
    ├── registers
    └── stack
```

A crash signal is delivered in a process/thread context; identifying the correct process and thread is therefore essential.

For Chromium/Electron:

```text
application
├── browser/main process
├── renderer processes
├── GPU process
└── utility processes
```

Each process may itself have many threads. “VS Code crashed” is less precise than “the GPU child process terminated by SIGBUS in thread X.”

## 5.4 Syscalls: the userspace/kernel boundary

A syscall is a controlled request from userspace to the kernel.

Examples:

```text
openat
read
write
mmap
connect
ioctl
clone
execve
futex
```

A libc function is not synonymous with a syscall. For example:

```text
printf
    -> userspace formatting and buffering
    -> eventually write syscall(s)
```

or:

```text
malloc
    -> userspace allocator state
    -> may occasionally request memory via mmap/brk-like mechanisms
```

This distinction explains why `strace` sees kernel-boundary events, not every high-level library call.

## 5.5 Blocking and scheduler interaction

Suppose a thread calls `read()` and data is unavailable.

A simplified flow:

```text
thread running
    -> read syscall
    -> kernel determines it must wait
    -> thread sleeps/blocks
    -> scheduler runs another runnable task
    -> event completes
    -> blocked task becomes runnable
    -> scheduler eventually runs it again
```

A syscall entry is not automatically a context switch to another task. A context switch means the CPU stops executing one task context and resumes another.

## 5.6 File descriptors: process-local handles to kernel objects

A file descriptor is a small integer index in a process’s descriptor table.

Typical start:

```text
fd 0 -> stdin
fd 1 -> stdout
fd 2 -> stderr
```

Additional descriptors can refer to:

```text
regular file
pipe
Unix socket
TCP socket
device node
terminal/PTY
anonymous kernel object
```

The unifying pattern is:

```text
process fd number
    -> kernel file/open object
    -> subsystem-specific behavior
```

This is why `read(7, ...)` can mean reading a file, pipe, socket, terminal, or device depending on what fd 7 refers to.

## 5.7 Redirection and pipes are fd rewiring

Shell syntax:

```sh
producer | consumer
```

can be understood as:

```text
producer stdout fd 1
        -> pipe write end
        -> pipe read end
consumer stdin fd 0
```

Similarly:

```sh
command > log.txt
```

means the process starts with fd 1 bound to an open file rather than the terminal.

This low-level model makes shell composition much less mysterious.

## 5.8 FD inheritance and close-on-exec

Child processes can inherit open file descriptors. This is useful for pipes, sockets, and supervision, but accidental inheritance can leak resources or keep endpoints alive unexpectedly.

The close-on-exec concept marks a descriptor to be closed when a successful `exec` replaces the process image.

A launcher debugging problem may involve:

```text
wrong environment
wrong working directory
wrong PATH
missing interpreter
unexpected inherited fd
sandbox helper failure
```

`posix_spawn` or `exec` failures are therefore broader than “binary missing.”

## 5.9 Signals

Signals are asynchronous process-control and notification mechanisms.

Examples:

```text
SIGINT  -> interactive interrupt, often Ctrl+C
SIGTERM -> termination request
SIGKILL -> uncatchable forced termination
SIGCHLD -> child state changed
SIGSEGV -> invalid memory access class
SIGBUS  -> bus/mapping/alignment-related fault class
SIGABRT -> abort-style termination
```

A signal name is a classification, not necessarily the root cause.

```text
SIGABRT
    may mean
runtime detected heap corruption
assertion failure
application called abort
fatal library invariant
```

## 5.10 Process groups and Ctrl+C

A terminal typically has a foreground process group. Pressing Ctrl+C results in an interrupt signal being directed according to terminal job-control semantics.

This explains why wrappers that do not use `exec`, background processes, and detached daemons can react differently to terminal signals.

For launchers, using `exec` where appropriate helps keep the process tree and signal relationship straightforward.

## 5.11 Zombies

When a child exits, the kernel retains minimal termination information until the parent collects it with a wait-family operation.

A zombie is not a process still executing CPU instructions. It is an exited process whose termination status has not yet been reaped.

Conceptually:

```text
child exits
    -> kernel keeps exit status
    -> parent has not wait()ed yet
    -> zombie entry
    -> parent wait()
    -> final cleanup
```

## 5.12 `futex` and synchronization

Threads sharing memory need synchronization. A mutex implementation may perform uncontended operations mostly in userspace and use a `futex` syscall when sleeping/waking becomes necessary.

A simplified model:

```text
fast uncontended path
    -> atomic userspace state change

contended path
    -> futex wait
    -> kernel sleeps thread
    -> futex wake
```

This matters because a “hung” application may be blocked in a futex wait rather than consuming CPU.

## 5.13 Project application: process boundaries as architecture

A strong project rule is that each process should remain inside one coherent ABI world.

A safer cross-world pattern is:

```text
bionic process
    -> Unix socket / pipe / bytes / protocol
    -> glibc process
```

rather than:

```text
one process
├── bionic runtime objects
└── glibc runtime objects
```

The process boundary naturally isolates:

- virtual address spaces;
- allocator state;
- libc TLS and internal objects;
- dynamic-linker scopes;
- many runtime globals.

## 5.14 Useful inspection commands

```sh
# Process tree
ps -ef

# Threads for one process
ps -T -p "$PID"

# File descriptors
ls -l /proc/$PID/fd

# Environment
tr '\0' '\n' < /proc/$PID/environ

# Syscall trace
strace -f -o trace.log ./program
```

Questions:

1. Which exact process fails?
2. Does the process spawn helpers?
3. Which descriptors and sockets are open?
4. Where does the process block?

## References

- Linux man-pages project, `execve(2)`: <https://man7.org/linux/man-pages/man2/execve.2.html>
- Linux man-pages project, `signal(7)`: <https://man7.org/linux/man-pages/man7/signal.7.html>
- Linux man-pages project, `futex(2)`: <https://man7.org/linux/man-pages/man2/futex.2.html>
- Termux execution environment: <https://github.com/termux/termux-packages/wiki/Termux-execution-environment>
