---
title: "把挂起与复杂的 GPU 内核追查到源代码"
title_en: "Tracing Hanging and Complicated GPU Kernels Down To The Source Code"
source: https://vllm.ai/blog/2025-12-03-improved-cuda-debugging
crawled: 2026-09-12
translated: 2026-09-13
---

# 把挂起与复杂的 GPU 内核追查到源代码

> 原文：[Tracing Hanging and Complicated GPU Kernels Down To The Source Code](https://vllm.ai/blog/2025-12-03-improved-cuda-debugging) · vLLM 博客

Kaichao You（vLLM）

[#开发者](https://vllm.ai/blog/tags/developer)

几个月前，我们发布了一篇博客文章 [CUDA Core Dump：调试内存访问错误及其他问题的高效工具](https://blog.vllm.ai/2025/08/11/cuda-debugging.html)，介绍了一种调试 CUDA 内核非法内存访问问题的强大技术。这是 GPU 内核调试的一个重要里程碑，它使开发者能够准确定位导致失败的内核。在此之前，由于 GPU 执行的异步特性，找出问题内核几乎不可能，错误信息也常常具有误导性。

随着 CUDA core dump 技术的采用不断增长，开发者表达了对更细粒度信息的需求——具体来说，就是触发问题的那行源代码。在这篇博文中，我们先介绍如何识别挂起的内核，然后演示如何把问题内核追查回其源代码。

## 如何找到挂起的内核

GPU 的算力一直在指数级增长，但内存带宽未能同步跟上。这种失衡导致了日益复杂的内存访问模式。近年来，旗舰数据中心 GPU 引入了异步内存访问模式，实现高性能内核时需要精细的同步机制。这些同步机制容易出现竞态条件和死锁，在复杂的代码库中尤其如此。

当 GPU 内核挂起时，程序通常会冻结或失去响应——即使按 Ctrl-C 也无法停止。最直接的解决办法是杀掉进程，但这种方式无法提供任何根因信息。开发者只能盲目猜测，对代码改动做二分排查，反复运行测试，直到找到问题。

> **注意：** 为什么 CUDA 内核挂起时按 Ctrl-C 无法停止进程？按 Ctrl-C 会向进程发送 SIGINT 信号。如果进程正在运行 Python 代码，SIGINT 信号会被 Python 解释器捕获，转换为一个 KeyboardInterrupt 异常，并把该异常排队，等进程回到运行 Python 代码的状态时再处理。但如果进程正在运行 CUDA 内核并等待 GPU 完成，它实际上是在等待底层 CUDA API 返回，此时没有任何 Python 代码在运行，因此 KeyboardInterrupt 异常无法被抛出。在下面的 `conditional_hang.py` 例子中，如果你想通过 Ctrl-C 终止进程，需要在脚本开头加上 `import signal; signal.signal(signal.SIGINT, signal.SIG_DFL)`，让 Python 解释器不捕获 SIGINT 信号，这样 Ctrl-C 才能成功终止进程。缺点是当 Python 解释器被 Ctrl-C 停止时，将无法显示错误堆栈。

幸运的是，有一种更好的办法。CUDA 驱动包含一个名为 `user induced GPU core dump generation` 的特性：驱动会在操作系统中打开管道（pipe），允许用户通过向管道写入来触发 core dump。触发后，CUDA 驱动会把 GPU 状态转储到 core dump 文件中，让我们能够检查 GPU 内部正在发生什么，最重要的是，识别出哪个 GPU 内核正在挂起。

考虑一个条件挂起内核的简单示例：

```
# save as conditional_hang.py

import triton
import triton.language as tl
import torch


@triton.jit
def conditional_hang_kernel(x_ptr,
                            flag,          # int32 scalar
                            n_elements,    # int32 scalar
                            BLOCK_SIZE: tl.constexpr):
    pid = tl.program_id(0)
    offs = pid * BLOCK_SIZE + tl.arange(0, BLOCK_SIZE)
    mask = offs < n_elements

    # Load values
    x = tl.load(x_ptr + offs, mask=mask, other=0)

    # If flag == 1: do a normal "+1" update
    if flag == 1:
        x = x + 1
        tl.store(x_ptr + offs, x, mask=mask)
    else:
        # Else: non-terminating loop, no break.
        # The loop condition depends on `flag`, which is invariant,
        # so this is effectively an infinite loop when flag == 0.
        while flag == 0:
            # do something trivial so the loop isn't optimized away
            x = x + 1
            tl.store(x_ptr + offs, x, mask=mask)


x = torch.ones(16, dtype=torch.float32, device="cuda")
n_elements = x.numel()
BLOCK_SIZE = 16


# 1) Normal behavior: increment by 1
conditional_hang_kernel[(1,)](
   x,
   flag=1,
   n_elements=n_elements,
   BLOCK_SIZE=BLOCK_SIZE,
)
print("After flag=1:", x)  # should be all 2s


# 2) Hanging behavior: this will spin forever
conditional_hang_kernel[(1,)](
   x,
   flag=0,
   n_elements=n_elements,
   BLOCK_SIZE=BLOCK_SIZE,
)

# this print will hang, because printing x will synchronize the device,
# and the kernel will never finish.

print("After flag=0:", x)

# the following line will never be reached

x = x + 2

torch.cuda.synchronize()
```

执行这段代码会无限期挂起。要调试这个问题，我们可以启用 user-induced GPU core dump 生成：

```
CUDA_ENABLE_USER_TRIGGERED_COREDUMP=1 \
CUDA_COREDUMP_PIPE="/tmp/cuda_coredump_pipe_%h.%p.%t" \
CUDA_ENABLE_COREDUMP_ON_EXCEPTION=1 \
CUDA_COREDUMP_SHOW_PROGRESS=1 \
CUDA_COREDUMP_GENERATION_FLAGS='skip_nonrelocated_elf_images,skip_global_memory,skip_shared_memory,skip_local_memory,skip_constbank_memory' \
CUDA_COREDUMP_FILE="/tmp/cuda_coredump_%h.%p.%t" \
python conditional_hang.py
```

在代码无限运行时，我们可以通过向管道写入来触发 CUDA core dump：

```
dd if=/dev/zero bs=1M count=1 > /tmp/cuda_coredump_pipe_hostname.3000837.1764236276
```

我们向管道写入 1MB 的零来触发 CUDA core dump。注意，简单的 `echo` 命令可能因管道缓冲而无法生效。

触发 core dump 后，运行 `python conditional_hang.py` 的原始终端会显示 core dump 进度：

```
[01:39:15.256278] coredump: Writing ELF file to /tmp/cuda_coredump_hostname.3000837.1764236276
[01:39:15.256350] coredump: Writing out global memory (0 bytes)
[01:39:15.256354] coredump: Writing out device table
[01:39:15.292027] coredump: Writing out metadata
[01:39:15.292039] coredump: Finalizing
[01:39:15.292124] coredump: Writing done
[01:39:15.292128] coredump: All done (took 00s)
```

然后我们可以用 `cuda-gdb` 打开 core dump 文件，确切看到内核挂在哪里：

```
Opening GPU coredump: /tmp/cuda_coredump_hostname.3000837.1764236276
[Current focus set to CUDA kernel 0, grid 53, block (0,0,0), thread (0,0,0), device 0, sm 124, warp 0, lane 0]
#0  0x00007f2e6fbff300 in conditional_hang_kernel<<<(1,1,1),(128,1,1)>>> () at conditional_hang.py:31
31                  tl.store(x_ptr + offs, x, mask=mask)
```

这种方法不仅让我们识别出挂起的内核（`conditional_hang_kernel`），还能精确定位它挂起的那一行代码。相比之前连问题内核都无法识别、更遑论找出导致挂起的具体行的情况，这是一个重大改进。

一个小的麻烦是，core dump 管道的路径是由 CUDA 驱动动态生成的，很难定位。我们可以通过 `CUDA_COREDUMP_PIPE` 环境变量为 core dump 管道指定一个模板路径来解决这个问题，这样通过检查进程的文件描述符就能轻松找到它：

```
$ ls /proc/3037675/fd/ -alth | grep /tmp/cuda_coredump_pipe_
lr-x------ 1 user user 64 Nov 27 01:50 98 -> /tmp/cuda_coredump_pipe_hostname.3037675.1764237014
```

## 如何把复杂内核追查回源代码

在上一篇博客中，我们提到用 `export NVCC_PREPEND_FLAGS='-lineinfo'` 环境变量编译可以把行信息嵌入编译后的二进制文件，让我们能够追查导致问题的确切代码行。在讨论并调试了若干真实问题之后，我们发现 `cuda-gdb` 显示行信息的默认方式并不完善：

1. 对于某些复杂内核，即使行信息已嵌入编译后的二进制文件，`cuda-gdb` 也找不到导致问题的正确代码行。
2. 即使 `cuda-gdb` 能找到正确的代码行，它也只显示编译器内联后的最后一行，这可能并不是真正导致问题的那一行。由于 C++ 代码大量依赖内联来消除运行时函数调用开销，我们需要完整的内联栈才能理解问题。

让我们用一个具体例子来说明。下面的 Python 脚本演示了一个非法内存访问问题：

```
# save as illegal_memory_access.py

from dataclasses import dataclass
import torch

@dataclass
class TensorWrapper:
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


def from_buffer(data_ptr: int, size_in_bytes: int, device: str, dtype: torch.dtype) -> torch.Tensor:
    return torch.as_tensor(TensorWrapper(data_ptr, size_in_bytes), device=device).view(dtype)

data = from_buffer(123456, 1024, device="cuda:0", dtype=torch.uint8)

index = torch.ones(10, device="cuda", dtype=torch.int32) + 100
print(data[index])
```

用 PyTorch >= 2.9.0 运行这段代码（具体来说，确保它包含[这个提交](https://github.com/pytorch/pytorch/commit/dae7710bf2561e9e8a8dc76fd30c68e25bd755b8)；否则你会看到类似 `RuntimeError: The specified pointer resides on host memory and is not registered with any CUDA device.` 的错误）。这将触发一个非法内存访问错误。

首先，让我们在启用 CUDA core dump 的情况下运行代码：

```
CUDA_ENABLE_COREDUMP_ON_EXCEPTION=1 \
CUDA_COREDUMP_SHOW_PROGRESS=1 \
CUDA_COREDUMP_GENERATION_FLAGS='skip_nonrelocated_elf_images,skip_global_memory,skip_shared_memory,skip_local_memory,skip_constbank_memory' \
CUDA_COREDUMP_FILE="/tmp/cuda_coredump_%h.%p.%t" \
python illegal_memory_access.py
```

core dump 进度会明确指出导致问题的内核：

```
_ZN2at6native24index_elementwise_kernelILi128ELi4EZNS0_16gpu_index_kernelIZNS0_17index_kernel_implINS0_10OpaqueTypeILi1EEEEEvRNS_18TensorIteratorBaseEN3c108ArrayRefIlEESA_EUlPcPKclE_EEvS7_SA_SA_RKT_bEUliE_EEvlT1_
```

从内核名称可以看出，问题是由 PyTorch 的 `index_elementwise_kernel` 引起的。要定位导致问题的确切代码行，我们需要用 `export NVCC_PREPEND_FLAGS='-lineinfo'` 环境变量从源码构建 PyTorch，然后再次运行代码。

当编译后的 GPU 内核嵌入了行信息时，我们可以用 `cuda-gdb` 打开 core dump 文件，确切看到是哪一行代码导致了问题：

```
(cuda-gdb) target cudacore /tmp/cuda_coredump_flow-matic.3756036.1764250282
Opening GPU coredump: /tmp/cuda_coredump_flow-matic.3756036.1764250282
[Current focus set to CUDA kernel 0, grid 4, block (0,0,0), thread (0,0,0), device 0, sm 124, warp 3, lane 0]

CUDA Exception: Warp Illegal Address
The exception was triggered at PC 0x7ff533bb91d0  ...
#0  void at::native::index_elementwise_kernel<128, 4, at::native::gpu_index_kernel<at::native::index_kernel_impl<at::native::OpaqueType<1> >(at
::TensorIteratorBase&, c10::ArrayRef<long>, c10::ArrayRef<long>)::{lambda(char*, char const*, long)#1}>(at::TensorIteratorBase&, c10::ArrayRef<
long>, c10::ArrayRef<long>, at::native::index_kernel_impl<at::native::OpaqueType<1> >(at::TensorIteratorBase&, c10::ArrayRef<long>, c10::ArrayR
ef<long>)::{lambda(char*, char const*, long)#1} const&, bool)::{lambda(int)#1}>(long, at::native::gpu_index_kernel<at::native::index_kernel_imp
l<at::native::OpaqueType<1> >(at::TensorIteratorBase&, c10::ArrayRef<long>, c10::ArrayRef<long>)::{lambda(char*, char const*, long)#1}>(at::Ten
sorIteratorBase&, c10::ArrayRef<long>, c10::ArrayRef<long>, at::native::index_kernel_impl<at::native::OpaqueType<1> >(at::TensorIteratorBase&,
c10::ArrayRef<long>, c10::ArrayRef<long>)::{lambda(char*, char const*, long)#1} const&, bool)::{lambda(int)#1})<<<(1,1,1),(128,1,1)>>> ()
    at /data/youkaichao/pytorch/aten/src/ATen/native/cuda/IndexKernel.cu:203 in _ZZN2at6native17index_kernel_implINS0_10OpaqueTypeILi1EEEEEvRNS
_18TensorIteratorBaseEN3c108ArrayRefIlEES8_ENKUlPcPKclE_clES9_SB_l inlined from IndexKernel.cu:118
203         *reinterpret_cast<scalar_t*>(out_data) = *reinterpret_cast<const scalar_t*>(in_data + offset);
```

接下来，在 `cuda-gdb` 中，我们可以用 `info symbol $errorpc` 获取关于出错位置的更多信息：

```
(cuda-gdb) info symbol $errorpc
void at::native::index_elementwise_kernel<128, 4, at::native::gpu_index_kernel<at::native::index_kernel_impl<at::native::OpaqueType<1> >(at::TensorIteratorBase&, c10::ArrayRef<long>, c10::ArrayRef<long>)::{lambda(char*, char const*, long)#1}>(at::TensorIteratorBase&, c10::ArrayRef<long>, c10::ArrayRef<long>, at::native::index_kernel_impl<at::native::OpaqueType<1> >(at::TensorIteratorBase&, c10::ArrayRef<long>, c10::ArrayRef<long>)::{lambda(char*, char const*, long)#1} const&, bool)::{lambda(int)#1}>(long, at::native::gpu_index_kernel<at::native::index_kernel_impl<at::native::OpaqueType<1> >(at::TensorIteratorBase&, c10::ArrayRef<long>, c10::ArrayRef<long>)::{lambda(char*, char const*, long)#1}>(at::TensorIteratorBase&, c10::ArrayRef<long>, c10::ArrayRef<long>, at::native::index_kernel_impl<at::native::OpaqueType<1> >(at::TensorIteratorBase&, c10::ArrayRef<long>, c10::ArrayRef<long>)::{lambda(char*, char const*, long)#1} const&, bool)::{lambda(int)#1}) + 11472 in section .text._ZN2at6native24index_elementwise_kernelILi128ELi4EZNS0_16gpu_index_kernelIZNS0_17index_kernel_implINS0_10OpaqueTypeILi1EEEEEvRNS_18TensorIteratorBaseEN3c108ArrayRefIlEESA_EUlPcPKclE_EEvS7_SA_SA_RKT_bEUliE_EEvlT1_ of /tmp/cuda-dbg/2123124/session1/elf.21407f80.24fe2940.o.4gyLzn
```

这提供了关于出错位置的更多信息。`cuda-gdb` 会解包编译后的二进制文件，`/tmp/cuda-dbg/2123124/session1/elf.21407f80.24fe2940.o.4gyLzn` 是一个包含 `index_elementwise_kernel` 的 cubin 文件。错误发生在 cubin 文件中的 `0x7ff533bb91d0` 位置。我们可以用 `nvdisasm` 反汇编 cubin 文件，确切看到是哪一行代码导致了问题：

```
$ nvdisasm -ndf -c -gi /tmp/cuda-dbg/2123124/session1/elf.21407f80.24fe2940.o.4gyLzn > output.txt
$ grep -C20 7ff533bb91d0 output.txt
...
        /*7ff533bb9190*/                   IMAD.IADD R19, R23, 0x1, R3 ;
.L_x_27840:
	//## File "/data/youkaichao/pytorch/aten/src/ATen/native/cuda/IndexKernel.cu", line 203 inlined at "/data/youkaichao/pytorch/aten/src/ATen/native/cuda/IndexKernel.cu", line 118
	//## File "/data/youkaichao/pytorch/aten/src/ATen/native/cuda/IndexKernel.cu", line 118 inlined at "/data/youkaichao/pytorch/aten/src/ATen/native/cuda/IndexKernel.cu", line 37
	//## File "/data/youkaichao/pytorch/aten/src/ATen/native/cuda/IndexKernel.cu", line 37
        /*7ff533bb91a0*/                   ULDC.64 UR4, c[0x0][0x480] ;
        /*7ff533bb91b0*/                   IADD3 R2, P0, P1, R22, UR4, R2 ;
        /*7ff533bb91c0*/                   IADD3.X R3, R19, UR5, RZ, P0, P1 ;
        /*7ff533bb91d0*/                   LDG.E.U8 R3, desc[UR36][R2.64] ;
...
```

现在我们可以看到导致问题的代码的完整内联栈。默认情况下，`cuda-gdb` 只显示最后一次内联展开。

对这些命令的简要说明：

- `-ndf`：反汇编后禁用数据流分析器。
- `-c`：只打印代码段。
- `-gi`：用从 .debug\_line 节获取的源码行信息（以及函数内联信息，如存在）注释反汇编结果。
- `-C20`：`grep` 的参数，显示找到的程序计数器地址 `7ff533bb91d0` 前后各 20 行上下文。

如果 cubin 文件中包含多个具有相同程序计数器地址的内核（即 `grep` 显示多个匹配），我们需要进一步过滤信息：

```
$ cuobjdump -elf /tmp/cuda-dbg/2123124/session1/elf.21407f80.24fe2940.o.4gyLzn > elf.txt
$ cat elf.txt | grep ".text._ZN2at6native24index_elementwise_kernelILi128ELi4EZNS0_16gpu_index_kernelIZNS0_17index_kernel_implINS0_10OpaqueTypeILi1EEEEEvRNS_18TensorIteratorBaseEN3c108ArrayRefIlEESA_EUlPcPKclE_EEvS7_SA_SA_RKT_bEUliE_EEvlT1_" | grep PROGBITS

  1ac 1b83f80   b200  0 80                     PROGBITS        6    3      26a .text._ZN2at6native24index_elementwise_kernelILi128ELi4EZNS0_16gpu_index_kernelIZNS0_17index_kernel_implINS0_10OpaqueTypeILi1EEEEEvRNS_18TensorIteratorBaseEN3c108ArrayRefIlEESA_EUlPcPKclE_EEvS7_SA_SA_RKT_bEUliE_EEvlT1_

$ nvdisasm -ndf -c -gi -fun 0x26a /tmp/cuda-dbg/2123124/session1/elf.21407f80.24fe2940.o.4gyLzn > output.txt
$ grep -C20 7ff533bb91d0 output.txt
...
        /*7ff533bb9190*/                   IMAD.IADD R19, R23, 0x1, R3 ;
.L_x_27840:
	//## File "/data/youkaichao/pytorch/aten/src/ATen/native/cuda/IndexKernel.cu", line 203 inlined at "/data/youkaichao/pytorch/aten/src/ATen/native/cuda/IndexKernel.cu", line 118
	//## File "/data/youkaichao/pytorch/aten/src/ATen/native/cuda/IndexKernel.cu", line 118 inlined at "/data/youkaichao/pytorch/aten/src/ATen/native/cuda/IndexKernel.cu", line 37
	//## File "/data/youkaichao/pytorch/aten/src/ATen/native/cuda/IndexKernel.cu", line 37
        /*7ff533bb91a0*/                   ULDC.64 UR4, c[0x0][0x480] ;
        /*7ff533bb91b0*/                   IADD3 R2, P0, P1, R22, UR4, R2 ;
        /*7ff533bb91c0*/                   IADD3.X R3, R19, UR5, RZ, P0, P1 ;
        /*7ff533bb91d0*/                   LDG.E.U8 R3, desc[UR36][R2.64] ;
...
```

主要区别是通过搜索该函数的 ELF 段，从 `cuobjdump` 获取 CUDA 函数索引（即 `-fun` 参数），在本例中为 `26a`。

注意，这是一个用于演示该技术的简化例子。真实世界的内核可能复杂得多。例如，下面是一个复杂的内联情形：

```
	//## File "/data/youkaichao/data/vllm_flash_attn/csrc/cutlass/include/cute/arch/copy_sm90.hpp", line 93 inlined at "/data/youkaichao/data/vllm_flash_attn/csrc/cutlass/include/cute/arch/util.hpp", line 158
	//## File "/data/youkaichao/data/vllm_flash_attn/csrc/cutlass/include/cute/arch/util.hpp", line 158 inlined at "/data/youkaichao/data/vllm_flash_attn/csrc/cutlass/include/cute/arch/util.hpp", line 185
	//## File "/data/youkaichao/data/vllm_flash_attn/csrc/cutlass/include/cute/arch/util.hpp", line 185 inlined at "/data/youkaichao/data/vllm_flash_attn/csrc/cutlass/include/cute/atom/copy_traits.hpp", line 133
	//## File "/data/youkaichao/data/vllm_flash_attn/csrc/cutlass/include/cute/atom/copy_traits.hpp", line 133 inlined at "/data/youkaichao/data/vllm_flash_attn/csrc/cutlass/include/cute/atom/copy_atom.hpp", line 103
	//## File "/data/youkaichao/data/vllm_flash_attn/csrc/cutlass/include/cute/atom/copy_atom.hpp", line 103 inlined at "/data/youkaichao/data/vllm_flash_attn/csrc/cutlass/include/cute/atom/copy_atom.hpp", line 124
	//## File "/data/youkaichao/data/vllm_flash_attn/csrc/cutlass/include/cute/atom/copy_atom.hpp", line 124 inlined at "/data/youkaichao/data/vllm_flash_attn/csrc/cutlass/include/cute/algorithm/copy.hpp", line 211
	//## File "/data/youkaichao/data/vllm_flash_attn/csrc/cutlass/include/cute/algorithm/copy.hpp", line 211 inlined at "/data/youkaichao/data/vllm_flash_attn/csrc/cutlass/include/cute/algorithm/copy.hpp", line 412
	//## File "/data/youkaichao/data/vllm_flash_attn/csrc/cutlass/include/cute/algorithm/copy.hpp", line 412 inlined at "/data/youkaichao/data/vllm_flash_attn/hopper/epilogue_fwd.hpp", line 265
	//## File "/data/youkaichao/data/vllm_flash_attn/hopper/epilogue_fwd.hpp", line 265 inlined at "/data/youkaichao/data/vllm_flash_attn/hopper/flash_fwd_kernel_sm90.h", line 454
	//## File "/data/youkaichao/data/vllm_flash_attn/hopper/flash_fwd_kernel_sm90.h", line 454 inlined at "/data/youkaichao/data/vllm_flash_attn/hopper/utils.h", line 41
	//## File "/data/youkaichao/data/vllm_flash_attn/hopper/utils.h", line 41 inlined at "/data/youkaichao/data/vllm_flash_attn/csrc/cutlass/include/cutlass/device_kernel.h", line 122
	//## File "/data/youkaichao/data/vllm_flash_attn/csrc/cutlass/include/cutlass/device_kernel.h", line 122
        /*7eebf5e9eb80*/                   STSM.16.M88.4 [R13], R4 ;
        /*7eebf5e9eb90*/                   MOV R34, R26 ;
```

在这个例子里，出问题的代码是：

![](https://vllm.ai/blog-assets/figures/2025-improved-cuda-debugging/poisoned_code.png)
注意力内核中的一行有问题的代码。

有问题的源代码调用了一些 CUTLASS 函数，而包含它的函数本身又被上层调用者内联。在这种情况下，`cuda-gdb` 无法正确关联到该行。实际上，它在出错位置附近不显示任何行信息。即使它显示了正确的行，也只是最后一个内联帧，即 `File "/data/youkaichao/data/vllm_flash_attn/csrc/cutlass/include/cute/arch/copy_sm90.hpp", line 93 inlined at "/data/youkaichao/data/vllm_flash_attn/csrc/cutlass/include/cute/arch/util.hpp", line 158`——这是 CUTLASS 函数内部的一次内联展开，对调试底层问题仍然没有帮助。

借助上述方法，我们可以还原源代码的完整内联链，并逐一仔细检查每一帧，找出应对错误负责的那一行。

**警告：** 要最大限度发挥 CUDA core dump 的作用，行信息至关重要。建议用 `export NVCC_PREPEND_FLAGS='-lineinfo'` 环境变量进行编译，因为它对所有被编译的内核透明生效，无需修改编译脚本。但这种透明性也意味着：如果你使用了 `ccache` 之类的编译缓存机制，它可能会忽略该标志，直接复用之前编译的结果而不进行真正的编译。从源码编译时，请确保禁用编译缓存机制。如果你使用即时（JIT）编译，请查阅你的即时编译工具的文档，了解如何添加行信息。

## 结论

这篇博文介绍了两种 CUDA 内核的高级调试技术。第一种利用用户触发的 core dump 识别挂起的内核，第二种利用嵌入编译二进制中的行信息把复杂内核追查回源代码。这些技术是调试 CUDA 内核复杂问题的有力工具，尤其是非法内存访问问题。最近，我们把两者结合使用，成功调试了 [CUTLASS MLA 注意力后端中一个难以复现且棘手的挂起问题](https://github.com/vllm-project/vllm/pull/26026)——它实际上源于上游的 CUTLASS 代码示例，并已在 [v4.3.0](https://github.com/NVIDIA/cutlass/commit/b1d6e2c9b334dfa811e4183dfbd02419249e4b52) 中修复。

vLLM 项目旨在为每个人提供简单、快速、可负担的 LLM 服务，而易用的调试是这一使命的重要方面。未来我们将继续分享更多调试技巧与技术，共同构建强大的 LLM 推理生态。想分享你与 vLLM 的故事或使用经验，请向[博客仓库](https://github.com/vllm-project/vllm-project.github.io)提交 PR。

# 致谢

我们感谢 NVIDIA 的 Ze Long 和 Sandarbh Jain 提供的有益讨论。Moonshot AI 的 Chao Hong 帮助提供了 motivating example。Red Hat 的 Lucas Wilkinson 帮助润色了草稿。
