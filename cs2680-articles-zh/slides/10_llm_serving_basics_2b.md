---
title: "第 10 讲（下）：LLM 服务基础（二）——GPU 编程、效率与 kernel 优化"
title_en: "LLM Serving Basics II: Intro to GPUs"
source: https://cs2680.seas.harvard.edu/slides/10_llm_serving_basics_2b.pdf
pages: 44
crawled: 2026-11-16
translated: 2026-11-16
---

# 第 10 讲（下）：LLM 服务基础（二）——GPU 编程、效率与 kernel 优化

> PDF 讲义文本抽取：[10_llm_serving_basics_2b.pdf](https://cs2680.seas.harvard.edu/slides/10_llm_serving_basics_2b.pdf) · Harvard CS2680

## 第 1 页

**现代 AI 系统：智能体与系统优化**

Juncheng Yang

LLM 服务基础（二）：GPU 入门

## 第 2 页

**事务**

- 作业 4 今天发布，两周半后截止
- 目标：推理性能与瓶颈，并迭代改进；理解真实工作负载与合成基准的差异
- 书面报告很重要，你只需要写少量代码
- 排行榜提交没有迟交日。不要占用超过一块 GPU
- 如果你之前系统编程经验有限，这个作业会比较难
- 项目提案下周三（10 月 28 日）截止
- 格式和页数不限
- 不要上传 AI 生成的内容

## 第 3 页

**今日安排**

- LLM 服务的 GPU 入门[1]
  - GPU 基础
  - GPU 架构
  - GPU 编程与近期 kernel 进展

[1] 我们不会深入细节；目标是帮助你建立直觉

## 第 4 页

**GPU 编程**

## 第 5 页

**GPU 代码异步执行**

主机：CPU + DRAM，运行 main()｜设备：GPU + HBM，运行 kernel

PCIe Gen5 x16：约 64 GB/s，只有 HBM 的约 1/75

CPU 线程｜拷贝引擎｜SM

cudaMalloc　memcpy H→D　启动 kernel　CPU 做其他工作　memcpy 回（等待）

拷贝 a、b 进｜拷贝 c 出

vec_add kernel 运行

时间 →

启动是异步的

CPU 不会等待 GPU kernel 结束。

错误很晚才暴露

kernel 故障要到下一次同步调用才显现。

NVIDIA, CUDA C++ Programming Guide, 2024; PCI-SIG, PCIe 5.0, 2019

## 第 6 页

**kernel 是按一个线程来写的（SIMT）**

```cuda
// one thread computes one output element
__global__ void add(float* x, float* y,
                    float* out, int n) {
  int i = blockIdx.x * blockDim.x + threadIdx.x;
  if (i < n) out[i] = x[i] + y[i];
}
// launch: n = 1M elements
int threads = 256;
int blocks  = (n + threads - 1) / threads;
add<<<blocks, threads>>>(x, y, out, n);
```

全局索引：每个线程通过 block 和 thread ID 找到自己的元素。

4,096 个块：1M ÷ 256 个线程；GPU 把它们分散到 132 个 SM 上。

块大小取 32 的倍数：通常 128–256 个线程；warp 由线性 tid 推出。

| 限定符 | 运行在 | 从何处调用 |
| --- | --- | --- |
| `__global__` | 设备 | 主机 |
| `__device__` | 设备 | 设备 |
| `__host__ __device__` | 两者 | 任意 |

## 第 7 页

**每个线程用它的 ID 选出数组元素**

1. 启动：4,096 个块 × 256 个线程

Block 0：0 1 … 255

Block 1：0 1 … 255

Block 2：0 1 … 255

Block 4,095：0 1 … 255

…

2. 每个线程计算自己的索引

i = blockIdx.x × blockDim.x + threadIdx.x

513 = 2（哪个块）× 256（块大小）+ 1（块内槽位）

3. ……并写入自己的元素 out[i]

0 1 … 255　256 257 … 511　512 513 … 767　…　1,048,575

NVIDIA, CUDA C++ Programming Guide

## 第 8 页

**块以 32 个线程的 warp 形式在 SM 上运行**

| 软件 | 硬件 |
| --- | --- |
| Grid：一次 kernel 启动的所有块 | 整个 GPU：块分散到 132 个 SM |
| Block：最多 1,024 个线程，带共享内存 | 一个 SM：驻留到完成为止 |
| Warp：32 个线程锁步执行 | 一个分区：调度器每周期发射它 |
| Thread：自己的寄存器、自己的索引 | 一个核（也叫 lane）：warp 的 32 个 SIMT lane 之一 |

NVIDIA, CUDA C++ Programming Guide, 2024

## 第 9 页

**图编译器（torch.compile）：你写模型，编译器写 kernel**

torch.compile

```python
import torch

def block(x, w, b):
    h = x @ w + b
    return gelu(h) * 0.5

# capture the graph, fuse, generate kernels
fast = torch.compile(block,
                     mode="max-autotune")
y = fast(x, w, b)  # first call compiles

# JAX: jax.jit(block) lowers to XLA
```

你决定：数学本身，用普通 PyTorch 或 JAX 写。不涉及线程、tile 或内存。

编译器决定：哪些算子融合、tile 大小，以及生成的 Triton 或 XLA kernel。

什么时候失效：控制流破坏计算图，或慢算子无法融合。

Ansel et al., PyTorch 2, ASPLOS 2024; OpenXLA documentation, 2026

## 第 10 页

**Tile 语言：描述整个块的工作，而不是一个线程的工作**

| | CUDA C++ | Tile 语言 |
| --- | --- | --- |
| 你写的是 | 一个线程的工作 | 一个数据 tile 的工作 |
| 索引 | blockIdx × blockDim + threadIdx | program_id + 对 tile 取范围 |
| 内存暂存、同步 | 你自己暂存 tile、调用 `__syncthreads()` | 编译器负责暂存并同步 |
| Tensor Core | warp 级 MMA 指令 | 对整个 tile 做一次点积 |

使用中的 tile 语言

Triton：Python；NVIDIA 和 AMD GPU

Pallas：面向 TPU 和 GPU 的 JAX kernel

TileLang：构建在 TVM 上的 Python DSL

ThunderKittens：C++ tile 模板

cuTile：NVIDIA 在 CUDA 中的 tile 模型

Tillet et al., MAPL 2019; Spector et al., ThunderKittens, 2024; NVIDIA CUDA 13.1, 2025

## 第 11 页

**Triton：每个 program 处理一个数据 tile**

```python
# each program handles one BLOCK
@triton.jit
def add(x, y, out, n, BLOCK: tl.constexpr):
    pid = tl.program_id(0)
    offs = pid * BLOCK + tl.arange(0, BLOCK)
    mask = offs < n
    a = tl.load(x + offs, mask=mask)
    b = tl.load(y + offs, mask=mask)
    tl.store(out + offs, a + b, mask=mask)
# launch: one program per tile
grid = (triton.cdiv(n, 1024),)
add[grid](x, y, out, n, BLOCK=1024)
```

每个 tile 一个 program：一个 program = 一个 CUDA 线程块；它拥有 BLOCK 个元素。

其余交给编译器：合并访问、共享内存暂存，以及通过 `tl.dot` 使用 Tensor Core MMA。

自动调优选 tile：`@triton.autotune` 针对每种形状尝试不同的 BLOCK 大小和 warp 数。

Tillet, Kung & Cox, Triton, MAPL 2019

ADVANCED —— 可略读，或自行深入阅读

## 第 12 页

**TileLang：你把每个 tile 放进共享内存，编译器映射线程**

TileLang 矩阵乘：

```python
@T.prim_func
def mm(A, B, C):
  with T.Kernel(N // bn, M // bm,
                threads=128) as (bx, by):
    As = T.alloc_shared((bm, bk), "float16")
    Bs = T.alloc_shared((bk, bn), "float16")
    Cl = T.alloc_fragment((bm, bn), "float")
    T.clear(Cl)
    for k in T.Pipelined(K // bk, num_stages=3):
      T.copy(A[by * bm, k * bk], As)
      T.copy(B[k * bk, bx * bn], Bs)
      T.gemm(As, Bs, Cl)
    T.copy(Cl, C[by * bm, bx * bn])
```

你决定：tile 形状、放共享内存还是寄存器，以及阶段数（提前加载几个 tile）。

TileLang 决定：线程映射、拷贝指令、swizzle 以及 MMA 调用。

适用场景：需要显式暂存的 GEMM 和注意力变体。

Wang et al., TileLang, arXiv 2025

ADVANCED —— 可略读，或自行深入阅读

## 第 13 页

**CuTe、CUTLASS 和 ThunderKittens：你选择布局、异步拷贝和 warp 角色**

CuTe 布局（CuTe DSL，Python）

```python
# a layout maps a coordinate to an offset
row = cute.make_layout((8, 4), stride=(4, 1))
col = cute.make_layout((8, 4), stride=(1, 8))

# (i, j) -> i*4 + j  versus  i + j*8

# the same algebra describes:
#  thread -> data in a warp
#  swizzled shared-memory tiles
#  TMA boxes and MMA fragments
```

你决定：布局、TMA 和异步流水线，以及哪些 warp 负责加载、哪些负责计算。

库提供：针对每种 GPU 经过测试的拷贝、MMA 和流水线构件。

适用场景：让 GEMM 和注意力冲击峰值的最后一程。

ADVANCED —— 可略读，或自行深入阅读

## 第 14 页

**不同的抽象层级**

| 层级 | 何时使用 | 成本 |
| --- | --- | --- |
| 图编译器（torch.compile、XLA） | 整个模型的默认选择 | 对慢算子几乎无法干预 |
| Tile 语言（Helion、Triton、Pallas） | 某个算子未融合或缺失 | 数小时；跨 GPU 移植 |
| 显式 tile（TileLang） | 需要控制暂存 | 数天 |
| 布局、warp 角色（CuTe、CUTLASS、ThunderKittens） | GEMM 或注意力必须达到峰值 | 数周；每代 GPU 重做 |
| 线程（CUDA C++） | 不规则工作：排序、稀疏、图 | 一切都得自己来 |

本课程对前述幻灯片的综合

ADVANCED —— 可略读，或自行深入阅读

## 第 15 页

**每个 GPU 程序最终都编译成 SASS**

NVCC device｜NVCC host

加载时：驱动运行与 GPU 匹配的 SASS，否则即时编译 PTX 并缓存。

Triton｜CUDA Tile

设备代码：NVVM → PTX → ptxas → SASS → fatbinary（fatbin：SASS + PTX）

主机代码：GCC / Clang / MSVC → 主机目标文件 → 链接器 → 可执行文件 + fatbin

`@triton.jit` → Triton IR → TritonGPU IR → LLVM IR → LLVM PTX → ptxas → SASS（cubin）

cuTile：Python、C++ → CUDA Tile IR → tileiras → SASS

源码｜中间代码｜虚拟 ISA｜机器码

工具

ADVANCED —— 可略读，或自行深入阅读

## 第 16 页

**GPU 效率与利用率**

## 第 17 页

**推理中的 MFU：模型 FLOPs 利用率**

模型 FLOPs 利用率

MFU = 实际达到的模型 FLOP/s ÷ 峰值 FLOP/s

模型 FLOPs：每个生成的 token 约 2N，仅前向

峰值：GPU 的稠密 Tensor Core 速率

Llama 2 70B 在 8 张 H100 上

每 token 的模型 FLOPs：2 × 70B ≈ 140 GFLOP

每 GPU 实际达到：3,040 tok/s × 140 GFLOP ≈ 426 TFLOP/s

MFU：426 ÷ 1,979 TFLOP/s ≈ 22%

经验法则：训练 35–45%；推理预填充 40–60%，解码 10–40%

## 第 18 页

**MFU 偏低的四个原因**

Chowdhery et al., PaLM, JMLR 2023; Korthikanti et al., Activation Recomputation, MLSys 2023

通信：张量并行、流水并行和数据并行的传输没有藏在计算后面

流水线气泡：每个批填充和排空流水线时，各阶段空闲

内存受限 kernel：norm、softmax 和优化器步骤以带宽速度运行，而非 Tensor Core 峰值

重计算（训练）：激活检查点重跑前向工作，而 MFU 不计这部分

MFU 把硬件能力和软件成熟度分开衡量

## 第 19 页

**MBU：解码效率看每秒移动的字节，而不是 FLOPs**

模型带宽利用率

MBU = 实际达到的字节/s ÷ 峰值 HBM 带宽

每解码步字节：全部权重加上读取的 KV 缓存

Llama 3 8B，BF16，批 1，H200：每 token 读取 16 GB

在 200 tok/s 下：3.2 TB/s ÷ 4.8 TB/s ≈ 67%

经验法则：预填充和训练报告 MFU，解码报告 MBU

服务系统的其他度量

每 GPU tokens/s：在给定延迟目标下的吞吐，例如每输出 token 的 p50 时间

每 token 能耗：焦耳 = 平均板卡功耗 ÷ tokens/s

每百万 token 成本：$ 每 GPU-小时 ÷ (tokens/s × 3,600) × 10⁶

Databricks, LLM Inference Performance Engineering, 2023

## 第 20 页

**先剖析时间线，再剖析 kernel**

Nsight Systems（nsys）

```
nsys profile -o run ./app
```

显示：CPU 线程、CUDA API 调用、拷贝、kernel 和流的一条时间线。

发现：空闲间隙、串行化的流和启动开销。

Nsight Compute（ncu）

```
ncu --set full -k vec_add ./app
```

显示：每个 kernel 被重放以采集计数器：speed of light、内存流量、warp 停顿、热点行。

发现：某个 kernel 为什么慢。重放时间仅用于对比。

nsys：找到慢的区域｜ncu：解释一个 kernel｜一次只改一件事，再测一次

NVIDIA, Nsight Systems and Nsight Compute documentation, 2026

直觉：先扫全身（时间线）找时间花在哪里，再放大（kernel）看为什么

## 第 21 页

**GPU 利用率**

| 计数器 | 它度量什么 |
| --- | --- |
| nvidia-smi utilization | 至少有一个 kernel 在运行的时间占比 |
| SM active | 有 warp 常驻的 SM 周期占比 |
| SM occupancy | 常驻 warp ÷ 最大 warp，所有 SM 合计 |
| Tensor pipe active | Tensor Core 忙碌的周期占比 |
| DRAM active | HBM 正在搬运数据的周期占比 |

```
dcgmi dmon -e 203,1002,1003,1004,1005
```

每个计数器一列

NVIDIA, DCGM User Guide: profiling metrics, 2026

## 第 22 页

**读计数器：找出哪个单元在忙**

1. GPU 忙吗？nvidia-smi 达到 100%

是 → 2. SM 忙吗？SM active 高

否 → GPU 在 kernel 之间空闲：CPU 启动开销或数据加载。下一步：Nsight Systems 时间线；CUDA Graph

是 → 3. 哪个单元忙？比较 DRAM 与 Tensor pipe active

否 → 线程块太少：工作填不满所有 SM。下一步：更大的批，每个 kernel 更多块

DRAM active 高 → 内存受限 → 用 MBU 判断

Tensor pipe active 高 → 计算受限 → 用 MFU 判断

两者都低 → 延迟受限 → 用 Nsight Compute

NVIDIA, DCGM User Guide: profiling metrics, 2026

## 第 23 页

**GPU 效率：要点**

1. MFU：实际达到的模型 FLOP/s ÷ 稠密峰值；用它判断预填充和训练。
2. MFU 偏低：通信、流水线气泡、内存受限 kernel 和重计算都在吃掉峰值。
3. MBU：实际达到的字节/s ÷ 峰值 HBM 带宽；用它判断解码。
4. 计数器：nvidia-smi 100% 只说明有 kernel 在跑；要读 SM、Tensor 和 DRAM 活动。

## 第 24 页

**GPU kernel 优化的近期进展**

## 第 25 页

**Kernel 在三个地方损失 GPU 时间**

1. kernel 内部

SM：MMA　exp　load

损失的时间：Tensor Core 在等加载、softmax 和 exp。

进展：FlashAttention、warp 特化、FlashAttention-4

2. 跨 SM

损失的时间：SM 在不均匀的轮次之间和 kernel 启动之间空闲。

进展：持久化 kernel、Split-KV、CUDA Graph、PDL、megakernel

3. 跨 GPU

GPU 0｜GPU 1

损失的时间：GPU 互相等待对方的数据。

进展：融合集合通信、MoE all-to-all 重叠

编写 kernel

写测试

损失的工程师时间：每一代新 GPU 都需要新的手工调优 kernel。

进展：自动编写和测试 kernel 的智能体

## 第 26 页

**Kernel 融合**

纵向：把步骤串起来；横向：合并并行算子

纵向融合

生产者在一个 kernel 内直接喂给消费者。

GEMM + bias GELU

一个 kernel：每个结果都留在寄存器里

省掉：HBM 往返

例子：GEMM epilogue、LayerNorm、带 mask 的 softmax

横向融合

共享输入的算子合并进一个 kernel。

x · W_q

x · W_k

x · W_v

→ x · [W_q　W_k　W_v]

一个 GEMM：x 只读一次，只启动一次

省掉：启动开销和重复读取 x

例子：QKV 投影、FFN 的 gate + up

编译器两者都做：torch.compile 把纵向链融合成一个 Triton kernel；模型代码常常手工（拼接权重）融合 QKV 和 gate + up。

未融合：读 x 写 t，读 t 写 u，读 u 写 y —— 1.25 ms

把 Scale、加 bias、ReLU 作为三个 kernel 作用在 1 GB FP32 上：每一步都经过 HBM

融合：读 x 写 y —— 0.42 ms，HBM 流量降至约 1/3

## 第 27 页

**FlashAttention：逐 tile 计算注意力，让 S 从不进入 HBM**

问题

标准注意力把 n × n 的分数矩阵 S 及其 softmax P 写到 HBM，再读回来。

在 8K token 时，每一层每个头就是 6,700 万个分数，全部要经过 HBM 搬运。

Dao et al., FlashAttention, NeurIPS 2022; Dao, FlashAttention-2, ICLR 2024

解法

片上：一个块的共享内存和寄存器

Q tile × K₁ V₁　K₂ V₂　K₃ V₃ …

S tile = Q·Kᵀ　softmax · V

running max、sum　O tile

对每个 K、V tile 重复：S 和 P 从不离开芯片

HBM：K、V 读一次，O 写一次

## 第 28 页

**从 FlashAttention 到 FlashAttention-4**

FlashAttention（2022 · A100）

瓶颈：HBM 流量：n × n 分数矩阵要写出再读回

修复：Q、K、V 在共享内存中分 tile；在线 softmax

结果：注意力快 2–4×；内存随长度线性增长

FlashAttention-2（2023 · A100）

瓶颈：占用率低：每个头一个块，大量非矩阵乘 FLOPs

修复：把工作沿序列切分；减少重缩放

结果：约为 FA1 的 2×；最高约 A100 峰值的 70%

FlashAttention-3（2024 · H100）

瓶颈：Tensor Core 在等待 warp 加载和计算 softmax

修复：TMA + warp 特化；softmax 与 GEMM 重叠；FP8

结果：FP16 下约为 H100 峰值的 75%

FlashAttention-4（2025 · B200）

瓶颈：Tensor Core 翻倍，exp 单元没有：softmax 成了瓶颈

修复：TMEM 累加器；部分 exp 放到 FMA 单元

结果：在 B200 上比 cuDNN 注意力更快

Dao et al. 2022; Dao 2023; Shah et al. 2024; Dao et al. 2025

ADVANCED —— 可略读，或自行深入阅读

## 第 29 页

**持久化 kernel：每个 SM 一个线程块，循环处理许多 tile**

问题

一次矩阵乘被切成 160 个输出 tile，每个 tile 一个线程块。GPU 有 132 个 SM，所以这些块要跑两轮。

第二轮只有 28 个块：104 个 SM 在等。每个块还要为单个 tile 重做一次初始化。

解法

要点：每个 SM 只启动一个块，让它循环处理 tile：没有空闲轮次，初始化只做一次。CUTLASS 和 DeepGEMM 都这么做。

Osama et al., Stream-K, PPoPP 2023; NVIDIA CUTLASS 3.x, 2024

正常启动：每个 tile 一个块，分轮运行

第 1 轮：132 个块填满 132 个 SM

第 2 轮：28 个块，104 个 SM 空闲

持久化 kernel：132 个块原地不动，逐个领取 tile

Compute｜Write out

tile 0 math → write tile 0

tile 1 math → write tile 1

tile 2 math → write tile 2

Stream-K：把 tile 切成更小的片，让所有 SM 一起完成

ADVANCED —— 可略读，或自行深入阅读

## 第 30 页

**Split-KV 在 SM 之间均衡解码**

问题

解码每个请求只有一个查询 token，所以只在批 × 头上切分会让 SM 空闲。

不同请求的 KV 长度相差 100×，而且它们的页分散在 HBM 中。

解法

要点：FlashInfer（MLSys 2025 杰出论文）把块稀疏 KV 与 JIT 特化 kernel 及该调度器结合；vLLM 和 SGLang 都在使用。

Dao et al., Flash-Decoding, 2023; Ye et al., FlashInfer, MLSys 2025

每个请求的 KV 页：R1、R2、R3

Split-KV：每 SM 4 页

SM0｜SM1｜SM2｜SM3

按请求合并部分结果 (m, ℓ, O)，与在线 softmax 同理

分页 KV 作为块稀疏行｜固定网格：对 CUDA Graph 安全

ADVANCED —— 可略读，或自行深入阅读

## 第 31 页

**CUDA Graph：只记录一次启动，之后用一次调用重放**

问题

解码一个 token 要运行几十个小 kernel。

每次启动花费几微秒的 CPU 和驱动时间，GPU 因此在 kernel 之间等待。

解法

普通流：每个 kernel 一次 CPU 启动

CPU｜GPU

CUDA Graph：一次调用重放全部

CPU｜GPU

graph launch

没有间隙，更早完成

```cuda
cudaStreamBeginCapture(s, mode);   // record one step
  …launch the kernels…;  cudaStreamEndCapture(s, &g);
cudaGraphInstantiate(&e, g, 0);  cudaGraphLaunch(e, s);
```

NVIDIA CUDA Programming Guide, CUDA Graphs, 2025

要点：捕获一次解码步，之后每个 token 重放一次；vLLM 和 SGLang 都这么做。

ADVANCED —— 可略读，或自行深入阅读

## 第 32 页

**Programmatic Dependent Launch（PDL）提前启动下一个 kernel**

问题

在一个流中，kernel B 只有在 kernel A 完全排空并刷新内存后才启动。

解码每 token 要运行许多微秒级 kernel，因此启动延迟、序言和每个 kernel 的尾部累加起来。

解法

要点：PDL 需要 Hopper 或更新架构（SM 9.0）；它削减解码中 kernel 之间的间隙，并且可以在 CUDA Graph 内工作。

NVIDIA CUDA Programming Guide §4.5, 2025

默认流顺序：Kernel A → 间隙 → 序言 → Kernel B

使用 PDL：Kernel A → 序言等待 → Kernel B（trigger / sync）

```cuda
A: cudaTriggerProgrammaticLaunchCompletion();
B: cudaGridDependencySynchronize();
```

ADVANCED —— 可略读，或自行深入阅读

## 第 33 页

**Megakernel 在一次启动中跑完整个模型**

问题

Llama-3.2-1B 的批 1 解码对每个 token 要运行约 7 个 kernel/层 × 16 层。

每个边界都要排空 GPU，下一个 kernel 才能加载权重；vLLM 和 SGLang 只用到 H100 带宽的约 50%。

解法

要点：Hazy Research 的 megakernel 在批 1 下达到 H100 带宽的 78%，每用户吞吐约为 SGLang 的 1.5×。Mirage MPK 可以自动编译这类任务图。

Spector, Juravsky et al., Look Ma, No Bubbles!, Hazy Research 2025; Mirage MPK, 2025

每个算子一个 kernel：每个启动边界都有气泡

Norm｜QKV｜Attn｜O-proj｜FFN

Megakernel：当前算子执行时加载下一个算子的权重

Norm｜QKV｜Attn｜O-proj｜FFN

GPU 上的解释器

每 SM 指令队列

权重用分页 SMEM

依赖关系用全局计数器

ADVANCED —— 可略读，或自行深入阅读

## 第 34 页

**融合集合通信隐藏 TP 通信**

问题

张量并行把每一层切到 8 块 GPU 上，在每个分片 GEMM 之前加一个 AllGather、之后加一个 ReduceScatter。

作为独立 kernel 运行时，GEMM 要等整个集合通信完成。

解法

要点：Flux 重叠了最多 96% 的通信，在 8 块 GPU 上预填充比 vLLM 快最多 1.66×，解码快 1.30×。

Chang et al., FLUX, arXiv:2406.06858, 2024

分离 kernel：先 GEMM，再 ReduceScatter

GEMM（所有 tile）→ ReduceScatter

融合：每个 tile 的 epilogue 直接写到拥有它的 GPU

Compute｜NVLink

t0 t0 t1 t1 t2 t2 t3 t3 t4 t4 t5 t5

AllGather + GEMM：tile 在对应行到达时就开始

通过对等写入（NVLink 或 NVSHMEM），不需要额外 kernel

ADVANCED —— 可略读，或自行深入阅读

## 第 35 页

**MoE all-to-all 藏在计算后面**

问题

每个 MoE 层把每个 token 发到其他 GPU 上它的 top-8 专家，然后把输出收回来。

背靠背运行时，dispatch 和 combine 会让 Tensor Core 空闲，且 NCCL kernel 会占用本应用于计算的 SM。

解法

要点：DeepEP 在节点内通过 NVLink 维持约 153 GB/s 的 dispatch，跨节点通过 RDMA 约 43 GB/s，接近链路峰值。

DeepSeek-AI, DeepEP, 2025; DeepSeek-V3, arXiv:2412.19437

串行：dispatch、专家、combine，然后下一层

Dispatch → Expert GEMM → Combine → Attention

DeepEP：两个微批重叠

SM｜网络

Attn A｜Attn B｜Experts A｜Experts B

Dispatch A｜Dispatch B｜Combine A｜Combine B

基于 hook 的传输运行在 NIC 上，不占用 SM

Dispatch 用 FP8｜Combine 用 BF16｜NVLink → RDMA 转发

ADVANCED —— 可略读，或自行深入阅读

## 第 36 页

**智能体成为新的编译器**

问题

每一代 GPU（TMA、TMEM、FP4）和每种注意力变体都需要新的手工调优 kernel，而会写的人很少。

生成的 kernel 可能通过弱测试或利用测试框架，显得很快。

解法

Ouyang et al., KernelBench, 2025; AutoMegaKernel, arXiv:2606.09682, 2026

智能体编写 kernel（CUDA、Triton、CuTe DSL）→ 编译（nvcc、ptxas 报错）→ 在多种形状上与 PyTorch 参考实现比对 → 剖析：运行时、Nsight 计数器

反馈回路

fastp：既正确、又比 PyTorch 快 p 倍以上的任务占比。静态检查会拒绝有竞态的调度。

ADVANCED —— 可略读，或自行深入阅读

## 第 37 页

**Kernel 进展：要点**

1. kernel 内部：喂饱 Tensor Core。融合 epilogue、按块做 FP8/FP4 缩放、把 warp 分成生产者和消费者，并把工作从最慢的单元移走。
2. 跨 SM 与跨启动：消除空闲时间。持久化 CTA 和 Split-KV 均衡 SM；PDL 和 megakernel 弥合 kernel 之间的间隙。
3. 跨 GPU：隐藏通信。把张量并行集合通信融进 GEMM tile，并让 MoE all-to-all 与专家计算重叠。
4. 编写 kernel：自动化搜索。智能体编写并剖析候选 kernel；多形状的正确性检查决定哪些能留下。

## 第 38 页

**AI 硬件的挑战**

网络：节点外慢 9×

KV 缓存交接，32K token 的 Llama 3 70B 提示

215 ms｜24 ms

400G NIC｜NVLink（H100）

可靠性：每 3 小时一次故障¹

Llama 3 训练 419 次中断的成因

8%｜17%｜30%

网络｜HBM3 内存｜GPU 故障

功耗：常规机架的 8×

每机架功耗²

120 kW｜60 kW｜15 kW

GB200 NVL72｜HGX B200｜常规

冷却与水

GB200 NVL72 机架需要液冷²

700,000 L：训练 GPT-3 所需淡水³

4.2–6.6B m³：预计 2027 年 AI 取水量³

¹The Llama 3 Herd of Models　²NVIDIA HGX Platform: Data Center Physical Requirements Guide

³Making AI Less “Thirsty”

## 第 39 页

**下一讲**

## 第 40 页

**延伸阅读**

优化 GPU 代码

## 第 41 页

**优化 GPU 代码：四个目标，在一个 kernel 中组合使用**

少搬数据：每个结果移动更少字节。例如合并访问、tiling、融合

隐藏等待时间：加载完成前让单元保持忙碌。例如异步拷贝、warp 特化

暴露更多并行：给每个 SM 足够多的独立工作。例如 Split-K、独立累加器

使用更快的指令：同样的数学走更便宜的硬件路径。例如 Tensor Core、更低精度

它们可以叠加：一个快速 GEMM 会合并加载、双缓冲 tile 并使用 Tensor Core。

NVIDIA, CUDA C++ Best Practices Guide; NVIDIA, CUTLASS documentation

## 第 42 页

**优化内存流量：少搬字节，每个字节多复用**

| 技术 | 核心思想 | 示例 |
| --- | --- | --- |
| 内存合并 | 相邻线程读连续地址 | 线程 i 读 x[i]，而不是 x[32·i] |
| 共享内存 tiling | 一块只加载一次；协作线程复用它 | 矩阵 tile 被多个输出复用 |
| 寄存器 tiling | 每个线程从寄存器算出多个输出 | 每线程多个累加器 |
| Kernel 融合 | 立即消费中间结果，跳过 HBM 往返 | Matmul + bias + 激活在一个 kernel 中 |
| Padding / swizzling | 改变共享内存布局以避免 bank 冲突 | 转置 tile 32×32 → 32×33 |
| 缓存感知排序 | 调度相邻块，让它们复用缓存数据 | 把读相同输入的输出 tile 分到一组 |

NVIDIA, CUDA C++ Best Practices Guide; NVIDIA, CUDA C++ Programming Guide

## 第 43 页

**隐藏等待并暴露并行：让每个 SM 持续发射工作**

| 技术 | 核心思想 | 示例 |
| --- | --- | --- |
| 异步拷贝 + 双缓冲 | 计算当前 tile 时加载下一个 | 在 GEMM 中交替使用两个共享内存缓冲 |
| 指令级并行 | 独立指令在更早指令等待时发射 | 多个累加器，而不是一条依赖链 |
| Warp 特化 | 不同 warp 承担流水线的不同角色 | 生产者 warp 加载；消费者 warp 跑 MMA |
| Split-K / 分裂归约 | 把长归约分散给更多工作者，再合并 | 解码中把长 KV 序列切到多个块 |
| Warp 级通信 | 在 warp 内寄存器到寄存器交换值 | 基于 shuffle 的 warp 求和或求最大值 |

代价：Split-K 多一个合并步骤；流水化增加缓冲和同步。

NVIDIA, CUTLASS documentation; NVIDIA, CUDA C++ Programming Guide

## 第 44 页

**更便宜的计算：让同样的数学跑在更快的指令上**

| 技术 | 核心思想 | 示例 |
| --- | --- | --- |
| Tensor Core 映射 | 把矩阵运算塑造成硬件支持的 tile 和布局 | 用 MMA 指令代替标量 FMA |
| 更低精度 | 存储和移动的字节更少；在支持处数学更快 | FP16/BF16 输入，FP32 累加 |
| 展开 + 特化 | 编译期固定结构；去掉运行时工作 | 针对一种 head 维度或 mask 类型构建 kernel |
| 更少分支发散 | 让 warp 内线程走同一条路径 | 把控制流相似的任务分到一组 |
| 自动调优 | 针对每种工作负载形状测量变体 | 搜索 tile 大小、warp 数、流水线深度 |

两个独立的选择：Tensor Core 需要合适的形状；精度必须保持准确。

NVIDIA, CUDA C++ Programming Guide; NVIDIA, CUTLASS documentation
