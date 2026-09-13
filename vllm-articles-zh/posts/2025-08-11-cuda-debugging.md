---
title: "CUDA Core Dump：调试内存访问问题及其他问题的有效工具"
title_en: "CUDA Core Dump: An Effective Tool to Debug Memory Access Issues and Beyond"
source: https://vllm.ai/blog/2025-08-11-cuda-debugging
crawled: 2026-09-12
translated: 2026-09-13
---

# CUDA Core Dump：调试内存访问问题及其他问题的有效工具

> 原文：[CUDA Core Dump: An Effective Tool to Debug Memory Access Issues and Beyond](https://vllm.ai/blog/2025-08-11-cuda-debugging) · vLLM 博客

作者：Kaichao You

[#开发者](https://vllm.ai/blog/tags/developer)

TL;DR：如果你遇到 `an illegal memory access was encountered` 错误，可以启用 CUDA core dump 来调试该问题。只需设置以下环境变量并重新运行程序以收集 coredump 文件，然后就可以使用 `cuda-gdb` 来调试该问题。

```
CUDA_ENABLE_COREDUMP_ON_EXCEPTION=1 \
CUDA_COREDUMP_SHOW_PROGRESS=1 \
CUDA_COREDUMP_GENERATION_FLAGS='skip_nonrelocated_elf_images,skip_global_memory,skip_shared_memory,skip_local_memory,skip_constbank_memory' \
CUDA_COREDUMP_FILE="/tmp/cuda_coredump_%h.%p.%t"
```

# 简介

你是否有过这样的经历：正在开发 CUDA 内核，而测试时经常遇到非法内存访问（illegal memory access，简称 IMA），却不知道该如何调试？在开发 vLLM——一个高性能 LLM 推理引擎——的过程中，我们一再体会到这种痛苦。

如果你正是遇到过这个问题的开发者之一，那么这篇博客就是为你准备的！我们将揭示我们使用的一些高级调试技巧，它们可以帮助用户调试 vLLM 中的复杂问题，例如 IMA。

例如，下面是一个来自 PyTorch 的错误：

```
RuntimeError: CUDA error: an illegal memory access was encountered
CUDA kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
For debugging consider passing CUDA_LAUNCH_BLOCKING=1
Compile with `TORCH_USE_CUDA_DSA` to enable device-side assertions.
```

这里的难点在于：CUDA kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.（CUDA 内核错误可能在另一个 API 调用处被异步报告，因此下面的堆栈跟踪可能不正确。）根据我们的经验，这类异常的 Python 堆栈跟踪基本上**总是不正确的，而且几乎没有价值**。为了解决这个问题，错误信息建议在运行代码时添加 `CUDA_LAUNCH_BLOCKING=1`。然而，这仍然存在两个问题：

1. 很多人使用 `kernel<<<>>>` 语法启动 CUDA 内核时，没有对内核启动状态做错误检查，例如这段[代码](https://github.com/pytorch/pytorch/blob/5e320eea665f773b78f6d3bfdbb1898b8e09e051/aten/src/ATen/native/cuda/SortStable.cu#L117)。在这种情况下，即使设置了 `CUDA_LAUNCH_BLOCKING=1`，也无法定位出错的内核。
2. 如果非法内存访问发生在 CUDA Graph 内的某个内核中，那么即使设置了 `CUDA_LAUNCH_BLOCKING=1`，我们也只能看到启动 CUDA Graph 时出现了问题，但仍无法精确定位出错的内核。

要准确定位这类问题，我们需要在非法内存访问发生的那一刻立即做出反应。当然，这不是用户能够直接做到的——必须由 CUDA 驱动本身提供支持。

[CUDA core dump 功能](https://docs.nvidia.com/cuda/cuda-gdb/index.html#gpu-core-dump-support)正是为此目的而设计的。它允许 CUDA 驱动在非法内存访问发生时转储（dump）GPU 状态，以便用户事后分析 GPU 状态，找出是哪个内核导致的问题以及非法内存访问的具体内容。

# 什么是 Core Dump？

GPU 本质上是一个大规模并行处理器，它的许多概念都可以在 CPU 中找到对应物。

[core dump（核心转储）](https://en.wikipedia.org/wiki/Core_dump)是由 CPU 和操作系统共同提供的功能。当程序在执行过程中崩溃时，操作系统可以记录程序的内存数据、运行状态等信息，供后续分析和调试使用。程序崩溃是一个硬件层面的概念。当 CPU 在执行某些指令时遇到错误，它会进入 `trap` 状态。此时，操作系统接管程序并执行相应的异常处理流程（默认情况下只是终止程序，但可以配置选项来生成 core dump 供分析。例如，`ulimit -c 1` 可以启用 core dump 生成，`echo "core.%e.%p" > /proc/sys/kernel/core_pattern` 可以指定 core dump 文件的路径）。

类推到 GPU 上，core dump 功能需要 GPU 硬件与 GPU 驱动协作。当 GPU 上的线程在执行过程中崩溃时，GPU 硬件需要触发异常并传递给 GPU 驱动，由驱动立即处理该异常。不过，根据[论坛讨论](https://forums.developer.nvidia.com/t/difference-in-error-handling-between-driver-api-and-runtime-api/336389)，GPU 驱动处理异常的默认行为是将当前 CUDA 上下文标记为不可用，而不是终止程序。

# 如何启用 CUDA Core Dump

启用 CUDA core dump 非常简单，只需设置 `CUDA_ENABLE_COREDUMP_ON_EXCEPTION=1` 环境变量即可。不过，为了获得更顺畅的体验，你还应该额外设置几个环境变量：

1. 默认情况下，CUDA core dump 会把 coredump 文件保存在当前目录，并且不打印文件路径。你可以启用 `CUDA_COREDUMP_SHOW_PROGRESS=1` 环境变量来显示 coredump 过程的进度和细节。最重要的是，它会在该过程完成后显示 coredump 文件的路径，便于后续的调试与分析。
2. 很多任务运行在容器中，任务失败时容器会被销毁，导致 coredump 文件无法保留。在这种情况下，你可以使用 `CUDA_COREDUMP_FILE` 环境变量为 coredump 文件指定一个文件路径模板。例如，你可以把 coredump 文件存放到持久化存储目录：`CUDA_COREDUMP_FILE="/persistent_dir/cuda_coredump_%h.%p.%t"`，其中 `%h` 是主机名，`%p` 是进程 ID，`%t` 是 coredump 的时间戳。
3. 默认情况下，coredump 过程会保存整个 GPU 上下文。对于像大模型推理这样几乎占用全部 GPU 内存的程序来说，完整的 coredump 并不现实（数百 GiB 的数据）。你可以使用 `CUDA_COREDUMP_GENERATION_FLAGS='skip_nonrelocated_elf_images,skip_global_memory,skip_shared_memory,skip_local_memory,skip_constbank_memory'` 环境变量来跳过保存 GPU 内存、共享内存和本地内存，从而减小 coredump 文件的体积。文档中没有提到 `skip_constbank_memory` 标志，但它实际上是被 CUDA core dump 功能支持的，[当大量 GPU 线程同时报错时](https://forums.developer.nvidia.com/t/cuda-core-dump-does-not-work-properly-when-many-device-assert-happens/342410)有时必须要用到它。

文档还提到，在 `CUDA_COREDUMP_GENERATION_FLAGS` 中加入 `skip_abort` 可以防止 CPU 进程在 coredump 完成后中止。这使得 CPU 进程可以补充自己的错误跟踪信息，提供更多调试信息。然而实验表明，该功能存在一个明显的 [bug](https://forums.developer.nvidia.com/t/cuda-core-dump-with-skip-abort-will-ignore-an-illegal-memory-access-error/341802/3)，可能导致 GPU 上的非法内存访问错误被忽略。在这种情况下，后续代码可能会继续正常运行，但程序的内存数据可能已经损坏。这对训练任务是不可接受的，对推理任务也不理想。因此这个功能总体上不可靠，不推荐使用。

此外，文档指出，启用 `CUDA_ENABLE_COREDUMP_ON_EXCEPTION=1` 不仅会启用 CUDA core dump，默认情况下还会生成 CPU coredump。但在实践中，我们发现 CPU coredump 包含的有用信息很少，而且难以分析。

如果你想要实时的数据用于调试，还可以启用 `CUDA_DEVICE_WAITS_ON_EXCEPTION=1` 环境变量。它不使用 CUDA core dump，而是在异常发生时立即停止 GPU 执行并挂起，等待用户附加调试器（如 cuda-gdb）来检查 GPU 状态，此时完整的 GPU 内存仍然完好。不过这种方式自动化程度较低，需要更多的人工干预。

总结一下，使用 CUDA core dump 功能时，推荐使用以下环境变量组合：

`CUDA_ENABLE_COREDUMP_ON_EXCEPTION=1 CUDA_COREDUMP_SHOW_PROGRESS=1 CUDA_COREDUMP_GENERATION_FLAGS='skip_nonrelocated_elf_images,skip_global_memory,skip_shared_memory,skip_local_memory,skip_constbank_memory' CUDA_COREDUMP_FILE="/persistent_dir/cuda_coredump_%h.%p.%t"`

# CUDA Core Dump 使用示例

让我们用一些代码来验证 CUDA core dump 的效果。

## 调试不当的内核启动

```
// test.cu
#include <cuda_runtime.h>
#include <stdio.h>
#include <stdlib.h>

// CUDA error checking macro
#define cuda_check(call) do { \
    cudaError_t err = call; \
    if (err != cudaSuccess) { \
        printf("CUDA Error at %s:%d - %s: %s\n", __FILE__, __LINE__, #call, cudaGetErrorString(err)); \
        exit(EXIT_FAILURE); \
    } \
} while(0)

// Kernel with illegal memory access - accesses memory beyond allocated bounds
__global__ void illegalMemoryAccessKernel(int* data, int size) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;

    // This will cause illegal memory access - accessing beyond allocated memory
    // We allocate 'size' elements but access up to size * 2
    if (idx < size * 2) {  // Access twice the allocated size
        for (int i = 0; i < 10000; i++) {
            data[idx - 1000000000 + i] = idx;   // This will cause illegal access for idx == 0
        }
    }
}

// Simple kernel with no errors
__global__ void normalKernel(int* data, int size) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;


    if (idx < size) {
        data[idx] = idx;
    }
}

int main() {
    printf("CUDA Illegal Memory Access Test\n");
    printf("===============================\n\n");

    int size = 100;
    int* h_data = (int*)malloc(size * sizeof(int));
    int* d_data;

    // Initialize host memory
    for (int i = 0; i < size; i++) {
        h_data[i] = 0;
    }

    // Allocate device memory
    cuda_check(cudaMalloc(&d_data, (unsigned long long)(size) * sizeof(int)));
    cuda_check(cudaMemcpy(d_data, h_data, size * sizeof(int), cudaMemcpyHostToDevice));

    // Launch kernel with illegal memory access
    int blockSize = 256;
    int numBlocks = (size + blockSize - 1) / blockSize;

    printf("Launching kernel with out-of-bounds access...\n");
    illegalMemoryAccessKernel<<<numBlocks, blockSize>>>(d_data, size);

    normalKernel<<<numBlocks, blockSize>>>(d_data, size);

    cuda_check(cudaMemcpy(h_data, d_data, size * sizeof(int), cudaMemcpyDeviceToHost));
    for (int i = 0; i < 5; i++) {
        printf("%d ", h_data[i]);
    }
    printf("\n");

    // Synchronize to catch any runtime errors
    cuda_check(cudaDeviceSynchronize());

    printf("Test completed.\n");

    // Cleanup
    cuda_check(cudaFree(d_data));
    free(h_data);

    return 0;
}
```

这段代码连续启动两个内核（`illegalMemoryAccessKernel` 和 `normalKernel`）。在执行过程中，你会遇到这样的错误信息：`CUDA Error at test.cu:62 - cudaMemcpy(h_data, d_data, size * sizeof(int), cudaMemcpyDeviceToHost): an illegal memory access was encountered`，而且错误只能在 `cudaMemcpy` 的返回值中被检测到。即使设置 `CUDA_LAUNCH_BLOCKING=1`，也无法识别导致错误的具体内核。

加上 CUDA core dump 相关的环境变量后，我们可以观察到：

```
[06:43:15.209195] coredump: Detected an exception of type CUDBG_EXCEPTION_WARP_ILLEGAL_ADDRESS (14)
[06:43:15.209202] coredump:   - Device: 0
[06:43:15.209206] coredump:   - SM: 124
[06:43:15.209208] coredump:   - Warp: 0
[06:43:15.209210] coredump:   - PC 0x7462c3bac310
[06:43:15.209477] coredump: Stack trace (lane masks: active 0xFFFFFFFF, valid 0xFFFFFFFF):
[06:43:15.209486] coredump:   #0	0x7462c3bac620	_Z25illegalMemoryAccessKernelPii

[00:40:46.806153] coredump: Writing ELF file to /tmp/cuda_coredump_xxx.1799919.1754898045

[1]    1799919 IOT instruction (core dumped)  CUDA_ENABLE_COREDUMP_ON_EXCEPTION=1 CUDA_COREDUMP_SHOW_PROGRESS=1 = = ./test3
```

GPU 线程触发非法内存访问后，CPU 立即生成一个 coredump 文件，然后触发 CPU 异常，直接终止程序。此时，我们得到了一个 coredump 文件 `/tmp/cuda_coredump_xxx.1799919.1754898045`。我们可以用 `cuda-gdb` 打开它（命令：`target cudacore /path/to/coredump_file`，其中 `cudacore` 指 CUDA 上的 coredump）：

```
$ cuda-gdb
(cuda-gdb) target cudacore /tmp/cuda_coredump_xxx.1799919.1754898045
Opening GPU coredump: /tmp/cuda_coredump_xxx.1799919.1754898045

CUDA Exception: Warp Illegal Address
The exception was triggered at PC 0x7f31abb9f6d0  illegalMemoryAccessKernel(int*, int)
[Current focus set to CUDA kernel 0, grid 1, block (0,0,0), thread (0,0,0), device 0, sm 124, warp 0, lane 0]
#0  0x00007f31abb9f6e0 in illegalMemoryAccessKernel(int*, int)<<<(1,1,1),(256,1,1)>>> ()
```

我们可以清楚地看到，异常是由 `illegalMemoryAccessKernel` 在 `kernel 0, grid 1, block (0,0,0), thread (0,0,0), device 0, sm 124, warp 0, lane 0` 处引起的。

## 调试 CUDA Graph 中的内核异常

下面是一个更复杂的例子：一个会触发非法内存访问的内核被插入到了 CUDA Graph 中：

```
# core_dump.py
import torch
import torch.nn as nn

from dataclasses import dataclass

@dataclass
class CupyWrapper:
    data_ptr: int
    size_in_bytes: int

    @property
    def __cuda_array_interface__(self):
        return {
            "shape": (self.size_in_bytes,),
            "typestr": '|u1',
            "data": (self.data_ptr, False),
            "version": 3,
        }

def from_buffer(data_ptr: int, size_in_bytes: int) -> torch.Tensor:
    out = torch.as_tensor(CupyWrapper(data_ptr, size_in_bytes))
    assert data_ptr == out.data_ptr(), "not zero-copy convert, something must be wrong!"
    return out


class NeuralNetwork(nn.Module):
    def __init__(self):
        super(NeuralNetwork, self).__init__()
        # First layer: [B, 10] -> [B, 20] with ReLU activation
        self.layer1 = nn.Linear(10, 20)
        self.relu = nn.ReLU()
        # Second layer: [B, 20] -> [B, 30]
        self.layer2 = nn.Linear(20, 30)
        self.num_called = 0

    def forward(self, x):
        # Input shape: [B, 10]
        x = self.layer1(x)  # [B, 20]
        x = self.relu(x)    # [B, 20] with ReLU activation
        self.num_called += 1
        if self.num_called > 1:
            y = from_buffer(x.data_ptr(), x.numel() * 1024 * 1024)
            # will trigger illegal memory access
            y.fill_(1)
        x = self.layer2(x)  # [B, 30]
        return x


# Example usage
if __name__ == "__main__":
    # Check if CUDA is available
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")

    # Create the model and move to CUDA
    model = NeuralNetwork().to(device)

    # Create sample input with batch size B=4 and move to CUDA
    batch_size = 4
    input_tensor = torch.randn(batch_size, 10).to(device)

    print(f"Input shape: {input_tensor.shape}")
    print(f"Input device: {input_tensor.device}")

    # Forward pass
    with torch.no_grad():
        # warmup
        output = model(input_tensor)
        # capture graph
        g = torch.cuda.CUDAGraph()
        with torch.cuda.graph(g):
            output = model(input_tensor)
        # replay graph
        g.replay()

    print(f"Output shape: {output.shape}")
    print(f"Output device: {output.device}")

    print(f"Output: {output.sum()}")

    # Print model summary
    print("\nModel architecture:")
    print(model)

    # Print number of parameters
    total_params = sum(p.numel() for p in model.parameters())
    print(f"\nTotal parameters: {total_params}")

    # Verify model is on CUDA
    print(f"Model device: {next(model.parameters()).device}")
```

直接执行会得到如下错误：

```
Using device: cuda
Input shape: torch.Size([4, 10])
Input device: cuda:0
Output shape: torch.Size([4, 30])
Output device: cuda:0
Traceback (most recent call last):
  File "core_dump.py", line 76, in <module>
    print(f"Output: {output.sum()}")
RuntimeError: CUDA error: an illegal memory access was encountered
CUDA kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
For debugging consider passing CUDA_LAUNCH_BLOCKING=1
Compile with `TORCH_USE_CUDA_DSA` to enable device-side assertions.
```

错误直到 `output.sum()` 触发设备同步后才被打印出来，从而暴露了非法内存访问。但由于 CUDA 内核是异步执行的，我们并不知道是哪个内核导致了非法内存访问。

添加 `CUDA_LAUNCH_BLOCKING=1` 后，错误信息变成了：

```
Using device: cuda
Input shape: torch.Size([4, 10])
Input device: cuda:0
Traceback (most recent call last):
  File "core_dump.py", line 71, in <module>
    g.replay()
  File "/uv_envs/py310/lib/python3.10/site-packages/torch/cuda/graphs.py", line 88, in replay
    super().replay()
RuntimeError: CUDA error: an illegal memory access was encountered
Compile with `TORCH_USE_CUDA_DSA` to enable device-side assertions.
```

可以推断出异常发生在 CUDA Graph 内的某个内核中。然而，常规方法最多只能提供这些信息。

加上环境变量 `CUDA_ENABLE_COREDUMP_ON_EXCEPTION=1 CUDA_COREDUMP_SHOW_PROGRESS=1 CUDA_COREDUMP_GENERATION_FLAGS='skip_nonrelocated_elf_images,skip_global_memory,skip_shared_memory,skip_local_memory,skip_constbank_memory' CUDA_COREDUMP_FILE="/tmp/cuda_coredump_%h.%p.%t"` 后，我们可以清楚地定位导致错误的内核：

```
(cuda-gdb) target cudacore /tmp/cuda_coredump_flow-matic.1929094.1754901120
Opening GPU coredump: /tmp/cuda_coredump_flow-matic.1929094.1754901120

CUDA Exception: Warp Illegal Address
The exception was triggered at PC 0x7fc2afba5e30  void at::native::vectorized_elementwise_kernel<4, at::native::FillFunctor<unsigned char>, std::array<char*, 1ul> >(int, at::native::FillFunctor<unsigned char>, std::array<char*, 1ul>)
[Current focus set to CUDA kernel 0, grid 9, block (17454,0,0), thread (0,0,0), device 0, sm 0, warp 1, lane 0]
#0  0x00007fc2afba5e70 in void at::native::vectorized_elementwise_kernel<4, at::native::FillFunctor<unsigned char>, std::array<char*, 1ul> >(int, at::native::FillFunctor<unsigned char>, std::array<char*, 1ul>)<<<(40960,1,1),(128,1,1)>>> ()
```

显然，这是一个 `fill` 函数，而且 `40960` 的网格大小非常大。借助这些信息，我们可以轻松定位到 `y = from_buffer(x.data_ptr(), x.numel() * 1024 * 1024); y.fill_(1);` 这两行——它们把 `x` 的长度强行扩大了一百万倍，然后用 1 全部填满，从而触发了 `illegal memory access` 异常。

在某些 GPU 上，这行代码可能导致的是 `invalid argument` 错误而不是 `illegal memory access`，因为网格大小超过了上限。在这种情况下，CUDA core dump 功能无法被触发，你需要把扩容系数 `1024 * 1024` 调小一些，以避免超出网格大小限制。

# 局限性与注意事项

1. 从理论上讲，CUDA core dump 应该能够捕获 GPU 上某个特定线程引发的各种异常。然而在实践中，在某些 GPU 和驱动版本上，诸如 `operation not supported on global/shared address space` 之类的异常可能无法触发 CUDA core dump。所幸 `illegal memory access` 通常能够可靠地触发 CUDA core dump，这可以满足大多数调试需求。
2. 对于与硬件相关的错误，例如 `Invalid access of peer GPU memory over nvlink or a hardware error`，它们并非由某个特定线程引起，无法归因于某个具体的 GPU 线程。因此，这类问题不会触发 CUDA core dump。
3. 由驱动 API 使用不当引起的错误被认为是[非粘性错误（non-sticky errors）](https://forums.developer.nvidia.com/t/difference-in-error-handling-between-driver-api-and-runtime-api/336389)，与 GPU 本身无关。这类错误在驱动 API 层面报告，不会触发 CUDA core dump。一个常见的例子是 `cudaMalloc` 期间的内存不足（out-of-memory）错误，它不会产生 CUDA core dump。
4. 对于涉及多 GPU 通信的分布式程序，通常会使用内存映射把其他 GPU 的内存映射到当前 GPU。如果另一个 GPU 上的程序退出，被映射的内存就会失效，访问它会触发 `illegal memory access`。但这不属于典型的 `illegal memory access` 问题。这类问题在分布式程序的关闭过程中很常见：如果关闭时 GPU 之间仍在通信，关闭的先后顺序可能导致部分 GPU 报出 `illegal memory access`。对此类程序使用 CUDA core dump 时，要注意区分这些误报。
5. 启用 CUDA core dump 确实会对 CUDA 内核带来一些性能影响（因为它需要在 GPU 线程退出时检查错误并归因）。因此，不建议在生产环境中启用 CUDA core dump。建议只有在能够可靠复现 `illegal memory access` 等错误之后，才为调试目的启用它。
6. 为了从 CUDA core dump 中获得最大收益，建议在编译 vLLM 时带上调试符号，或者至少在编译时嵌入行号信息。遗憾的是，由于二进制体积限制，vLLM 的默认构建不包含这些信息。要享受这一好处，用户需要[从源码编译 vLLM](https://docs.vllm.ai/en/latest/getting_started/installation/gpu.html#full-build-with-compilation)，并设置环境变量 `export NVCC_PREPEND_FLAGS='-lineinfo'` 或 `export NVCC_PREPEND_FLAGS='-G'`。建议从 `-lineinfo` 开始，只有当 `-lineinfo` 不够用时再切换到 `-G`。有了丰富的调试信息，CUDA core dump 就能回溯到引发异常的确切代码行。

# 结论

这篇博客分析了 CUDA core dump 的原理与使用场景。这种调试方法对内核启动不当、CUDA Graph 内的内核异常等问题都很有效，是调试 `illegal memory access` 问题及其他问题的有力工具。

举个例子，我们最近用这项技术调试了 vLLM 中一个复杂的 `illegal memory access` 问题，详情见[这个 PR](https://github.com/vllm-project/vllm/pull/22593)。大致情况是：我们为 MRope 添加了一个 [triton kernel](https://github.com/vllm-project/vllm/pull/22375)，但该内核隐含 `head_size==rotary_dim`（即完整 Rope）的假设。当 `head_size!=rotary_dim`（即部分 Rope）时，内核会触发 `illegal memory access`，而新的 [GLM-4.5V](https://huggingface.co/zai-org/GLM-4.5V) 模型正是这种情况。如果没有 CUDA core dump，错误会被报告为 `Failed: Cuda error /workspace/csrc/custom_all_reduce.cuh:453 'an illegal memory access was encountered'`，非常具有误导性。有了 CUDA core dump，我们可以轻松把错误定位到 MRope 内核，然后修复它。注意，这个例子是由 CUDA 内核参数配置错误引起的，找到导致问题的内核就足以完成调试。对于更复杂的 `illegal memory access` 问题，我们仍需要隔离内核，在最小示例（而非端到端示例）中复现问题，然后使用 [Compute Sanitizer](https://docs.nvidia.com/compute-sanitizer/ComputeSanitizer/index.html#memcheck-tool) 等更专业的工具进一步排查。

vLLM 项目致力于为所有人提供简单、快速、低成本的 LLM 服务，而易用的调试也是其中重要的一环。未来我们将继续分享更多调试技巧，共同建设强大的 LLM 推理生态。想分享你与 vLLM 的故事或用法，请在[博客仓库](https://github.com/vllm-project/vllm-project.github.io)提交 PR。

# 致谢

我们感谢 NVIDIA 的 Ze Long、Vikram Sharma Mailthody、Jeremy Iverson 和 Sandarbh Jain 提供的有益讨论。感谢 Red Hat 的 Lucas Wilkinson 帮助润色本文草稿。
