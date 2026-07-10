# 15. Kernel, Scheduler, Drivers, and the GPU Stack

The project eventually reaches hardware, but not by letting applications talk to hardware arbitrarily. The kernel mediates CPU scheduling, memory, devices, synchronization, and protection.

## 15.1 What the kernel owns

A useful high-level model:

```text
userspace processes
    -> syscalls / UAPI
    -> kernel
        ├── scheduler
        ├── virtual memory
        ├── filesystems
        ├── networking
        ├── IPC primitives
        ├── security enforcement
        └── device drivers
    -> hardware
```

The kernel is not the distribution. Debian, Termux, bionic, and glibc userspaces can all interact with one Linux-derived kernel through compatible interfaces.

## 15.2 Scheduler

The scheduler decides which runnable tasks execute on which CPUs.

A simplified state picture:

```text
running
runnable
sleeping / waiting
stopped
exited/zombie state handling
```

A thread blocked on I/O does not need to consume CPU while waiting. The scheduler can run other tasks.

## 15.3 Context switch

A context switch means execution moves from one task context to another.

Conceptually:

```text
save enough state of task A
    -> choose task B
    -> restore task B state
    -> resume B
```

Costs include more than register save/restore. Cache locality, translation state, and scheduling overhead can matter.

A syscall entry is not automatically a context switch between tasks; the same thread can enter and leave kernel mode without another task running.

## 15.4 Interrupts and asynchronous events

A syscall is an intentional userspace request. A hardware interrupt is an asynchronous event from hardware or platform machinery.

Conceptually:

```text
GPU finishes work
    -> interrupt/completion path
    -> kernel driver updates state
    -> fence/event becomes signaled
    -> waiting task can wake
```

This connects device work, kernel event handling, and scheduler wakeups.

## 15.5 Drivers

A driver connects kernel subsystems to device-specific interfaces and behavior.

Userspace may interact through:

```text
device node
fd
ioctl
mmap
poll/read/write
```

A driver often acts as a resource manager and security boundary, not just a thin command forwarder.

## 15.6 `ioctl`

`ioctl` provides device/subsystem-specific operations associated with a file descriptor.

Conceptually:

```text
fd + command + structured argument
    -> kernel driver/subsystem operation
```

GPU stacks use rich ioctl/UAPI interfaces for objects such as:

```text
contexts
buffer allocation/import
virtual address management
command submission
synchronization
querying capabilities
```

The exact interface is driver/platform specific.

## 15.7 Userspace GPU driver versus kernel driver

A modern graphics stack spans both.

```text
application
    -> Vulkan/OpenGL API
    -> userspace driver
        shader compilation
        API validation/state tracking
        command construction
        resource management logic
    -> kernel UAPI
        memory objects
        submission
        synchronization
        scheduling/security
    -> GPU hardware
```

Mesa Turnip is a userspace Vulkan driver. KGSL is part of the Android/Qualcomm-oriented kernel graphics interface path used on the target.

## 15.8 Command submission

A simplified GPU workflow:

```text
application records API work
    -> userspace driver builds GPU commands
    -> buffers/resources referenced
    -> kernel submission request
    -> GPU scheduler/device executes
    -> completion/fence signal
```

The CPU can continue while GPU work is queued, so GPU failures and synchronization bugs can be temporally separated from the API call that initiated work.

## 15.9 CPU virtual address versus GPU virtual address

The CPU process and GPU can have different virtual-address spaces and translation arrangements.

Conceptually:

```text
CPU VA
    -> CPU page tables/MMU
    -> physical/system memory

GPU VA
    -> GPU/IOMMU translation
    -> device-visible memory mapping
```

Do not assume that an address used in GPU command context is directly meaningful as a CPU process virtual address.

## 15.10 DMA and IOMMU

DMA allows devices to transfer data without the CPU manually copying each byte.

An IOMMU can provide device address translation and isolation.

Conceptually:

```text
device-visible address
    -> IOMMU translation
    -> physical memory
```

This is part of why GPU buffer management involves explicit mapping/import/export contracts.

## 15.11 dma-buf

The Linux dma-buf framework supports sharing buffer objects across devices/subsystems using file-descriptor-based handles and synchronization conventions.

A conceptual path:

```text
producer creates buffer
    -> export fd
    -> consumer imports fd
    -> both refer to shared underlying buffer object
    -> synchronization controls safe access
```

The exact Android graphics stack can include platform-specific allocation and synchronization layers in addition to standard Linux mechanisms.

## 15.12 Synchronization and fences

GPU and display pipelines are asynchronous. A fence represents completion/synchronization state.

A conceptual error class:

```text
buffer rendered
    -> presentation consumer reads before completion
    -> or producer reuses buffer too early
    -> corruption/fault/hang
```

Correct buffer lifetime and synchronization are as important as successful allocation.

## 15.13 Mesa, Turnip, Vulkan loader, and ICD

A simplified glibc Vulkan path in this project:

```text
application
    -> Vulkan loader
    -> ICD metadata selects driver
    -> Turnip userspace driver
    -> KGSL UAPI
    -> Adreno GPU
```

The ICD JSON/loader configuration is runtime metadata. If a glibc application accidentally default-scans a bionic ICD and loads an incompatible `.so`, the failure is a cross-ABI provider-selection problem.

This is why deterministic ICD pinning is part of the runtime contract.

## 15.14 Zink

Zink is a Mesa Gallium driver that implements OpenGL over Vulkan.

Project path:

```text
OpenGL application
    -> Zink
    -> Vulkan
    -> Turnip
    -> KGSL
    -> Adreno
```

This allows glibc OpenGL consumers to use the validated Vulkan driver path without requiring a separate classic OpenGL hardware driver path.

## 15.15 ANGLE Vulkan

Chromium/Electron can use ANGLE as a translation layer, with Vulkan as its backend.

Conceptual project path:

```text
Chromium/Electron graphics API usage
    -> ANGLE
    -> Vulkan
    -> Turnip
    -> KGSL
    -> Adreno
```

This is a different consumer path from Zink even though both eventually reach Vulkan/Turnip.

## 15.16 Rendering versus presentation

A GPU can be detected and rendering commands can succeed while the display/presentation path fails.

```text
GPU enumeration
    -> device creation
    -> command execution
    -> render target produced
    -> WSI/buffer sharing
    -> presentation
    -> X11/display integration
```

A failure at the final presentation stage does not negate earlier GPU success, and earlier GPU success does not prove presentation correctness.

## 15.17 WSI

Window System Integration connects Vulkan rendering with a windowing/display system.

Conceptually:

```text
Vulkan rendering
    -> swapchain images
    -> synchronization
    -> X11/window-system integration
    -> presentation
```

A SIGBUS occurring at first X11 presentation belongs to a narrower region of the pipeline than “Vulkan does not work.”

## 15.18 The Mesa 26.1.x lesson

The project observed a split:

```text
kgsl-only investigated configuration
    -> GPU enumeration possible
    -> first X11 presentation failure with SIGBUS

msm,kgsl build policy
    -> validated working dependency/runtime shape
```

The disciplined conclusion is:

```text
validated practical build policy
    !=
proven low-level crash mechanism
```

That distinction is a model for evidence quality across the project.

## 15.19 Android versus desktop DRM/KMS assumptions

Linux graphics tutorials often assume a conventional desktop DRM/KMS stack. Android devices can use different display allocation/composition paths and vendor/kernel interfaces.

Therefore porting a userspace graphics stack requires examining:

```text
kernel device interface
buffer allocation/import/export
synchronization
window-system integration
Android display bridge
permissions/security policy
```

Do not infer platform compatibility from CPU architecture or generic “Linux” support alone.

## 15.20 GPU debugging ladder

For a failure:

```text
1. Which process failed?
2. Can Vulkan loader find the intended ICD?
3. Which driver .so is actually mapped?
4. Can physical devices enumerate?
5. Can device creation succeed?
6. Can a headless/compute/render test submit work?
7. Does WSI surface creation work?
8. Does swapchain creation work?
9. Does first presentation work?
10. What mmap/ioctl/fence events differ from a working control?
```

This ladder prevents “GPU works/does not work” from hiding the actual failure stage.

## References

- Linux kernel GPU documentation: <https://docs.kernel.org/gpu/>
- Linux kernel dma-buf documentation: <https://docs.kernel.org/driver-api/dma-buf.html>
- Mesa documentation: <https://docs.mesa3d.org/>
- Mesa Turnip source tree: <https://gitlab.freedesktop.org/mesa/mesa/-/tree/main/src/freedreno/vulkan>
- Vulkan specification: <https://registry.khronos.org/vulkan/specs/latest/html/vkspec.html>
- Project GPU guide: [`../../gpu.md`](../../gpu.md)
