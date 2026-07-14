# 7. CPU Instructions, AArch64 Registers, Calling Conventions, and ABI

The CPU does not execute C, Python, ELF metadata, or shell scripts. It executes architecture-specific machine instructions. Higher layers arrange those instructions and the state they operate on.

## 7.1 ISA versus ABI

An instruction-set architecture (ISA) defines the machine-level instruction and register model.

Examples:

```text
AArch64
x86-64
RISC-V
```

An ABI defines how independently compiled components cooperate at binary level.

Examples of ABI concerns:

```text
argument registers
return-value registers
stack alignment
callee-saved registers
ELF conventions
symbol naming/versioning
object layout assumptions
syscall convention
```

Therefore:

```text
same ISA
    !=
same userspace ABI
```

Two files can both be AArch64 ELF binaries while one expects Android bionic and another expects a conventional glibc runtime.

## 7.2 Instructions and registers

A simple assembly-like example:

```asm
add x0, x0, x1
ret
```

Conceptually:

```text
x0 = x0 + x1
return to caller
```

Registers are small, fast CPU-visible storage locations. Memory is accessed through load/store instructions.

A useful mental model:

```text
memory
    -> load into register
    -> compute in registers
    -> store result to memory
```

AArch64 is a load/store architecture: arithmetic instructions generally operate on registers rather than arbitrary memory operands.

## 7.3 General-purpose registers

AAPCS64 defines roles for AArch64 registers in procedure calls. Important beginner-level roles include:

```text
x0-x7   argument/result registers
x19-x28 callee-saved general-purpose registers
x29      frame pointer role by convention
x30      link register (LR)
SP       stack pointer
```

The 32-bit `wN` names refer to the lower-width views associated with general-purpose register numbering.

The program counter is conceptually the current instruction address, but AArch64 does not treat PC as an ordinary general-purpose `xN` register.

## 7.4 Function arguments and return values

A simplified function:

```c
long add(long a, long b) {
    return a + b;
}
```

can conceptually map to:

```text
input a -> x0
input b -> x1
return  -> x0
```

and assembly resembling:

```asm
add x0, x0, x1
ret
```

Real compiler output depends on optimization, types, ABI details, and surrounding context.

## 7.5 `bl` and the link register

AArch64 function calls commonly use a branch-with-link instruction conceptually like:

```asm
bl function
```

The call transfers control and records a return address in the link register (`x30`/LR). A return instruction can use that saved return state.

Nested functions must preserve return information as needed, often saving state on the stack according to compiler-generated prologue/epilogue rules.

## 7.6 Stack frames

A common conceptual frame contains:

```text
local variables/spills
saved registers
saved frame pointer
saved return information
alignment padding
```

One common prologue shape may save `x29` and `x30`, establish a frame pointer, and allocate stack space. This is not a universal mandatory instruction sequence; optimization can omit frame pointers or organize frames differently.

The ABI defines the contract. The compiler chooses a valid implementation.

## 7.7 Caller-saved and callee-saved registers

Suppose function A calls function B.

For caller-saved registers, A must assume B may overwrite them and preserve values itself if needed.

For callee-saved registers, B must restore the required registers before returning if it uses them.

This contract allows separately compiled object files to call one another safely without knowing each other’s source code.

## 7.8 Calling convention is one part of ABI

ABI is broader than argument registers.

Consider a C struct crossing a library boundary:

```c
struct Record {
    int a;
    long b;
};
```

Both sides must agree on:

```text
integer widths
alignment
padding
offset of b
calling convention
ownership rules
```

A function name matching at link time does not prove semantic ABI compatibility.

## 7.9 Syscall ABI

Userspace normally calls libc wrappers, but at the lowest interface a syscall follows an architecture/kernel convention.

On Linux AArch64, the general conceptual shape is:

```text
syscall number in designated register
arguments in designated registers
svc instruction enters kernel
return value/error convention in register
```

The important project lesson is that libc API and kernel UAPI are separate contracts. A glibc process and bionic process can both reach the same kernel while exposing different userspace APIs and runtime assumptions.

## 7.10 Machine code, assembly, object file

The pipeline is:

```text
source language
    -> compiler IR and optimization
    -> target machine instructions
    -> assembler/object encoding
    -> relocatable object file
    -> linker
    -> ELF executable/shared object
```

Assembly is a human-readable representation of instructions. Machine code is the binary encoding the CPU executes.

## 7.11 Why external calls need relocations

When compiling one object file, the final address of an external function may be unknown.

```text
main.o
    needs foo

foo.o or libfoo.so
    defines foo
```

The object file therefore carries symbol and relocation information. The static linker and, for dynamic references, the runtime linker cooperate to establish actual addresses.

This is the machine-level foundation of GOT, PLT, dynamic symbols, and runtime relocation.

## 7.12 Endianness

A multi-byte value must be represented as an ordered sequence of bytes in memory. AArch64 Android devices used by this project operate in the common little-endian environment, visible in ELF descriptions such as “LSB.”

The practical lesson is not to memorize one byte pattern but to recognize that binary file formats, network protocols, and device interfaces define byte-order rules explicitly.

## 7.13 Alignment

Many data types and instructions have alignment preferences or requirements. ABI rules define expected alignment at interfaces such as the stack.

Do not reduce every SIGBUS to “unaligned access.” Alignment behavior depends on instruction type, mapping type, platform, and signal metadata. Crash analysis should inspect `si_code`, the fault address, the instruction, and the mapping.

## 7.14 Disassembly exercises

Pick a small binary:

```sh
BIN="$(command -v true)"

file "$BIN"
readelf -h "$BIN"
readelf -l "$BIN"
readelf -s "$BIN" | head
llvm-objdump -d "$BIN" | less
```

Questions:

1. Is the binary AArch64?
2. Which interpreter is encoded?
3. Where is the entry point?
4. Can you find branch-and-link instructions?
5. Which external symbols remain undefined for the dynamic linker?

## 7.15 Project connection: architecture match is only the first filter

An upstream package labeled `arm64` or `aarch64` answers:

```text
Can the CPU decode these instructions?
```

It does not answer:

```text
Can Android linker load it?
Does it expect glibc symbol versions?
Does it require filesystem paths absent in Termux?
Does its plugin system load coherent libraries?
Can its display and GPU protocols reach valid providers?
```

This is why `patchelf` can change interpreter/search metadata but cannot magically convert a glibc ABI binary into a bionic-native binary.

## References

- Arm AAPCS64 specification: <https://github.com/ARM-software/abi-aa/blob/main/aapcs64/aapcs64.rst>
- Arm ABI specifications repository: <https://github.com/ARM-software/abi-aa>
- Linux kernel arm64 documentation: <https://docs.kernel.org/arch/arm64/>
- LLVM documentation: <https://llvm.org/docs/>
