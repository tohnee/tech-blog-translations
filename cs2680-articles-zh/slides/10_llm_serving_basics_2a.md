---
title: "第 10 讲（上）：LLM 服务基础（二）——GPU 入门"
title_en: "LLM Serving Basics II: Intro to GPUs"
source: https://cs2680.seas.harvard.edu/slides/10_llm_serving_basics_2a.pdf
pages: 41
crawled: 2026-11-16
translated: 2026-11-16
---

# 第 10 讲（上）：LLM 服务基础（二）——GPU 入门

> PDF 讲义文本抽取：[10_llm_serving_basics_2a.pdf](https://cs2680.seas.harvard.edu/slides/10_llm_serving_basics_2a.pdf) · Harvard CS2680

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

**GPU 基础**

关于 GPU 你必须知道的一切

## 第 5 页

**GPU 形态**

消费级 · 台式机中的 PCIe 卡｜数据中心 · 服务器中的 8-GPU 板

## 第 6 页

（空白页）

## 第 7 页

**GPU 是一台吞吐机器**

CPU · 为单线程优化

control, OoO, branch predict / ALUs / L1/L2（×4）

共享 L3 缓存

内存：少量 DDR 通道

GPU · 为整个芯片优化

图中画出 132 个 SM 中的 32 个

L2 缓存

内存控制器

内存：HBM 堆栈，数千位宽

图例：控制与推测｜算术单元｜寄存器｜私有缓存｜共享缓存

跑车：2 名乘客，最快到达｜公交车队：更慢，但能运送数千人

## 第 8 页

**GPU 用少量快核换数千个简单核**

| | 64 核服务器 CPU | NVIDIA H200 SXM |
| --- | --- | --- |
| 并行单元 | 64 核 | 132 个 SM，16,896 个 FP32 核 |
| 在飞线程 | 128 | 270,336（每 SM 2,048） |
| 内存带宽 | 约 0.46 TB/s（DDR5） | 4.8 TB/s（HBM3e） |
| 峰值稠密算力 | 约 5 TFLOPs FP32 | 989 TFLOPs BF16 |
| 隐藏延迟的方式 | 缓存、乱序核 | 切换到就绪的 warp |

发生缓存缺失时，CPU 线程继续向前跑，直到乱序窗口填满，然后停顿。GPU 则切换到另一个就绪的 warp。

为什么适合 LLM：每个 token 都在相同权重上并行执行相同的矩阵乘。

## 第 9 页

**切换 warp 隐藏内存延迟**

warp 发射指令｜warp 等待内存｜时间 →

Warp 0：等待内存　等待内存　等待内存

Warp 1：等待内存　等待内存

Warp 2：等待内存　等待内存

Warp 3：等待内存　等待内存

数学单元：W0 W1 W2 W3　W0 W1 W2 W3　W0 W1 W2 W3

为什么有效：一个 warp 等待时，另一个发射，数学单元因此保持忙碌。

A100/H200/B200：每个 warp 调度器（每个 SM 中有 4 个）管理最多 16 个 warp，因此每个 SM 有 64 个常驻 warp。

## 第 10 页

**SIMT：单指令、多线程**

一个线程的程序：

```
i = threadIdx.x
y[i] = a*x[i] + b
```

标量代码，只写一次

32 个线程：一个 warp = 一个块中的线程 0–31

1 次取指 · 1 次译码 · 1 次调度决策

lane 0 … lane 31

执行 lane：自己的寄存器

为什么高效：一条 warp 指令完成 32 条标量指令的工作。

控制只付一次代价，由 32 个 lane 共享，就像 CPU 上的 SIMD 向量指令。

## 第 11 页

**分支发散**

指令（一个 warp）：

```
int i = threadIdx.x;
bool p = (i % 4 == 0);
if (p) a = f(x[i]);
else a = g(x[i]);
y[i] = a;
```

diverged（发散）／reconverged（重汇合）

lane 0 … lane 31｜active mask

0xFFFFFFFF

0xFFFFFFFF

0x11111111

0xEEEEEEEE

0xFFFFFFFF

lane 运行｜lane 被掩掉，空闲

代价：warp 轮流执行两条路径；f 用到 32 个 lane 中的 8 个，g 用到 24 个。

## 第 12 页

**GPU 背后的权衡**

| GPU 放弃 | 换来 |
| --- | --- |
| 单线程速度。频率适中、无推测执行：串行代码慢得多。 | 面积和功耗给到数千个算术单元。 |
| 并行必须显式表达。约 27 万线程才能填满 132 个 SM；小任务会让芯片空闲。 | 用切换 warp 隐藏延迟，而不是靠缓存和推测。 |
| 控制流是共享的。线程以 32 个为一组运行；分支发散损失吞吐。 | 一次指令取指和译码驱动 32 个核。 |
| 每线程的片上内存很小。满占用时每线程约 240 字节。 | 每个线程的状态都常驻，所以 warp 切换是免费的。 |

## 第 13 页

**三项规格决定每块 GPU 的上限**

峰值 BF16 算力

A100　312 TFLOP/s

H200　989 TFLOP/s

B200　2,250 TFLOP/s

Rubin　≈ 4,000 TFLOP/s

决定数学运算跑多快

内存容量

A100　80 GB HBM2e

H200　141 GB HBM3e

B200　180 GB HBM3e

Rubin　288 GB HBM4

决定能放下多少权重和 KV 缓存条目

内存带宽

A100　2.0 TB/s

H200　4.8 TB/s

B200　8 TB/s

Rubin　≈ 22 TB/s

决定权重和 KV 缓存读得多快

直觉：算力是引擎，带宽是油路，容量是油箱

## 第 14 页

**只有当每读入一个字节都喂给足够 FLOPs 时，算力才能达到峰值**

解码，批 1：每 token 3.3 ms

HBM 读取 16 GB 权重

Tensor Core 有 99.5% 的时间空闲

预填充，2,048 token：每个提示 33 ms

权重加载完后 HBM 读取空闲

Tensor Core 33 TFLOP，接近峰值忙碌

解码：计算在等——每个权重只用一次，所以 0.016 ms 的数学要等 3.3 ms 的读取。

预填充：计算很忙——每个权重喂给 2,048 个 token，所以读取早早完成，数学决定节奏。

Kernel 时间 ≈ max(字节 ÷ 带宽, FLOPs ÷ 峰值)。

## 第 15 页

**roofline 模型显示 kernel 受内存还是计算限制**

拐点左侧：内存受限：速度 = 带宽 × 算术强度

拐点右侧：计算受限：速度 = 峰值 FLOP/s

拐点 = 峰值 FLOP/s ÷ 带宽

可达 FLOP/s｜内存受限｜计算受限｜decode｜prefill

算术强度（FLOPs / byte）

H200 拐点 ≈ 206

Williams, Waterman & Patterson, Roofline, CACM 2009

算术强度 = 执行的 FLOPs ÷ 移入或移出 HBM 的字节

## 第 16 页

**常见的算术强度**

方阵 GEMM，N × N：每个元素复用约 N 次。强度 = 2N³ ÷ 3N²b = 2N/(3b)

解码注意力，n × d：每个 KV 条目每个头只用一次。强度 = 4nd ÷ 2ndb = 2/b

GEMV（解码），N × N：每个权重只用一次。强度 = 2N² ÷ (N² + 2N)b ≈ 2/b

向量加法，长度 N：每移动 3 个元素做 1 FLOP。强度 = N ÷ 3Nb = 1/(3b)

强度 = FLOPs ÷ 字节（每个元素 b 字节）

## 第 17 页

**批处理对解码有帮助吗？**

按批大小 n 的算术强度，FLOP/B，BF16

256：Weights

206：拐点

1：Attention

0、100、200、300

1 2 4 8 16 32 64 128 256

批处理把权重 GEMV 推向拐点，但解码注意力仍停留在 2/b

KV ×＝　W ×＝

## 第 18 页

**上下文长度对解码有帮助吗？**

Meta, The Llama 3 Herd of Models, 2024; NVIDIA H200 datasheet, 2024

按上下文长度统计的每解码步 HBM 读取字节，Llama 3 8B，批 16，BF16

权重：固定 16.1 GB，任意 L 下每步读一次

KV 缓存：128 KiB/token，随批 × L 增长

步 ≈ 字节 ÷ 4.8 TB/s：1K 时 3.8 ms，32K 时 17.7 ms

18.2 GB　24.7 GB　33.3 GB　50.5 GB　84.8 GB

1K　4K　8K　16K　32K

权重｜KV 缓存

## 第 19 页

**批 1 解码时 H200 有多忙？**

已知条件

峰值算力：989 TFLOP/s（BF16，稠密）

HBM 带宽：4.8 TB/s

批 1 解码：一个 GEMV，每读一字节权重约做 1 FLOP

你估计的峰值算力占比

A　≈ 50%　　B　≈ 10%

C　≈ 2%　　D　< 1%

然后：你会改什么来提升它？

## 第 20 页

**在 H200 的 roofline 上，批 1 解码只跑到峰值算力的 0.5%**

0.1 / 1 / 10 / 100 / 1,000 / 10,000

TFLOP/s（对数轴）

算术强度（FLOP/B，对数轴）

解码受带宽限制：批 1 GEMV 约 1 FLOP/B，只达到 989 TFLOP/s 中的约 5。

提高算术强度：增大批、量化、减少 KV 流量。

预填充受计算限制：大 GEMM 位于平坦的屋顶上；只有更快的数学或更少的 FLOPs 有帮助。

图中标注：向量加法、GEMV 批 1、GQA 解码、GEMV 批 32、GEMM N = 8192

计算屋顶 989 TFLOP/s

内存屋顶 4.8 TB/s × 强度

拐点 ≈ 206 FLOP/B

## 第 21 页

**趋势：更低精度把拐点推向右**

拐点 = 稠密峰值 ÷ HBM 带宽，FLOP/B

| GPU | HBM | FP32 | BF16 | FP8 | FP4 |
| --- | --- | --- | --- | --- | --- |
| A100 SXM | 2.04 TB/s | 9.6 | 153 | – | – |
| H100 SXM5 | 3.35 TB/s | 20 | 295 | 591 | – |
| H200 | 4.8 TB/s | 14 | 206 | 412 | – |
| B200 HGX | 8 TB/s | 9.4 | 281 | 563 | 1,125 |
| MI355X | 8 TB/s | – | 315 | 629 | 1,259 |
| Rubin（初步） | 22 TB/s | – | 182 | 795 | 1,591 |

FP4 把拐点推向右：Rubin 的稠密 NVFP4 需要约 1,600 FLOP/byte 才算计算受限

计算增长超过带宽：从 A100 到 Rubin，BF16 增长约 13×，带宽增长约 9×，因此 kernel 越来越受带宽限制。

## 第 22 页

**GPU 基础：要点**

1. 吞吐机器：GPU 用快速的单线程换数千个并行核。
2. 三项限制：峰值算力、HBM 带宽和内存容量约束每个 kernel。
3. roofline：拐点（H200 上 206 FLOP/B）区分内存受限与计算受限 kernel。
4. 解码：批处理把权重读取推向拐点；KV 缓存读取仍受内存限制。
5. 趋势：新 GPU 把拐点右移；越来越多 kernel 受带宽限制。

## 第 23 页

**GPU 架构**

## 第 24 页

**H200 示意图**

132 个 SM 共享一个 50 MB L2 缓存和 141 GB HBM3e

SM SM SM SM SM SM SM SM SM SM SM

SM SM SM SM SM SM SM SM SM SM SM

L2 缓存 · 50 MB · 被所有 SM 共享

SM SM SM SM SM SM SM SM SM SM SM

SM SM SM SM SM SM SM SM SM SM SM

die 上共有 132 个 SM（图中画出 44 个）；每个有自己的寄存器和 256 KB SRAM

HBM3e 24 GB ×6

HBM3e：6 个堆栈 × 24 GB，141 GB 可用，4.8 TB/s。NVLink：到其他 GPU 900 GB/s。

NVIDIA, Hopper Architecture whitepaper, 2022; H200 datasheet, 2024

## 第 25 页

**每个 SM 分成四个分区，每个分区每周期发射一条 warp 指令**

分区 1：warp 调度器｜寄存器 64 KB｜32 个 FP32 核｜Tensor Core

分区 2：warp 调度器｜寄存器 64 KB｜32 个 FP32 核｜Tensor Core

分区 3：warp 调度器｜寄存器 64 KB｜32 个 FP32 核｜Tensor Core

分区 4：warp 调度器｜寄存器 64 KB｜32 个 FP32 核｜Tensor Core

L1 / 共享内存 · 256 KB

Warp = 32 个线程：一条指令同时在全部 32 个线程上运行（SIMT）。

最多 64 个 warp：2,048 个常驻线程；调度器每周期挑一个就绪 warp。

Tensor Core：每条指令执行一个小矩阵乘加。

NVIDIA, Hopper Architecture whitepaper, 2022

## 第 26 页

**LLM 的数学主要是矩阵乘，Tensor Core 加速它**

一条 warp 指令：D = A × B + C

A 16×16，B 16×8，C 16×8，D 16×8

× + =

矩阵乘占 LLM FLOPs 的 99% 以上

Softmax 和 norm 使用 FP32 核。

一条 mma = 2,048 次乘加

每条指令是一个 FMA 的 64× 工作量。

H200 SXM 的峰值稠密 TFLOP/s

989　BF16 Tensor

495　TF32 Tensor

134　FP16 标量

67　FP32 标量

NVIDIA, PTX ISA (mma); H200 datasheet, 2024; Dally et al., IEEE Micro, 2021

## 第 27 页

**Tensor Core 为什么快**

专门的算术单元：专用乘加数据通路并行处理整个矩阵 tile。

每个 FLOP 更少指令：一条 MMA 指令覆盖许多乘加，摊薄译码、调度和操作数处理的开销。

高效的操作数复用：A 的每个值喂给多个输出列；B 的每个值喂给多个输出行。

更低精度算术：FP16、BF16 和 FP8 提升吞吐并缩小操作数，通常配合更高精度的累加。

NVIDIA, Hopper Architecture whitepaper, 2022

## 第 28 页

**内存层次**

| 层级 · H200 容量 | 延迟 · Hopper | 带宽 |
| --- | --- | --- |
| 寄存器（每 SM 256 KB） | 在流水线内，每条指令都读 | 每核每时钟 3 个操作数 |
| 共享内存 / L1（每 SM 256 KB 池） | 约 30 周期（L1 命中 40） | 每 SM 128 B/clk，132 个 SM 合计约 33 TB/s |
| L2 缓存（50 MB） | 约 250 周期 | 约 6 KB/clk，Hopper 上约 12 TB/s |
| HBM3e（6 堆栈共 141 GB） | 约 500 周期 | 4.8 TB/s |
| 主机内存与对等 GPU（CPU DRAM，经 NVLink 访问其他 GPU） | 微秒级 | 经 NVLink 或 PCIe 双向 450 GB/s；NVLink 4；PCIe 5.0 约 64 GB/s |

H200 SXM

Luo et al., Dissecting the NVIDIA Hopper Architecture, 2024

## 第 29 页

**内存是一根 250 ns 的管道：带宽取决于里面有多少字节**

Little 定律：带宽 = 在飞字节 ÷ 延迟

（图中标注：= 512 B）

朴素 kernel：每 SM 4 KB 在飞 = 32 warp × 32 线程 × 一次 4 B 加载

每 SM 2.2 TB/s

45% 峰值

满管：每 SM 9 KB 在飞 = 4.8 TB/s × 250 ns ÷ 132 个 SM

每 SM 4.8 TB/s

100% 峰值

管道长度 = 延迟：从发出加载到数据到达 250 ns

硬件固定了管道的长度，所以提升带宽的唯一办法是让管道里保持更多字节。

增加在飞字节的方法

- 使用 16 字节向量加载
- 每线程发出四个独立加载
- 使用批量异步拷贝（TMA）

A Proof for the Queuing Formula: L = λW; NVIDIA H200

## 第 30 页

**在飞字节：每一代 GPU 都需要更多才能达到峰值带宽**

| | H200 · Hopper | B200 · Blackwell | Rubin |
| --- | --- | --- | --- |
| SM 数 | 132 | 148 | 224 |
| HBM | 141 GB HBM3e | 180 GB HBM3e | 288 GB HBM4 |
| HBM 带宽 | 4.8 TB/s | 8 TB/s | 22 TB/s |
| 在飞字节（GPU） | 1.2 MB | 2.0 MB | 5.5 MB |
| 在飞字节（每 SM） | 9 KB | 14 KB | 25 KB |
| 新数据通路特性 | TMA、cluster | TMEM、2-SM MMA | Inline TMA descriptors |

NVIDIA, Hopper and Blackwell whitepapers; Vera Rubin, GTC 2025

## 第 31 页

**Hopper 让每条指令承载更多在飞字节**

| 特性 | 它做什么 | 效果 |
| --- | --- | --- |
| 合并访问（Coalescing） | 32 个线程读连续 4 字节字，合并成一个 128 B 请求 | 更少、更满的内存请求 |
| 16 字节向量加载 | 一条 warp 指令移动 512 B 而不是 128 B | 每条指令 4× 字节 |
| cp.async（Ampere+） | 把全局内存拷入共享内存，不经寄存器中转 | 寄存器空出来做更多加载 |
| TMA（Hopper） | 一个线程发出批量 tile 拷贝；硬件生成地址 | 一条指令就有数千字节在飞 |
| TMA multicast | 一次 L2 读取落到一个 cluster 中每个 SM 的共享内存 | 每 SM 更少的 L2 流量 |

ADVANCED —— 可略读，或自行深入阅读

## 第 32 页

**Hopper 的 TMA 用一条指令拷贝整个 tile**

TMA：一个线程，一个 tile

全局内存（HBM）→ TMA 引擎→共享内存 tile，例如 128 × 64

一个线程启动整个拷贝

寄存器保持空闲，一条指令让数十 KB 在飞

Cluster multicast：一次读取，多个 SM

L2：一次读取

SM 0　拷贝

SM 1　拷贝

SM 2　拷贝

SM 3　拷贝

一个 cluster 中最多 8 个线程块共享一次 L2 读取，因此 L2 流量下降

ADVANCED —— 可略读，或自行深入阅读

## 第 33 页

**Blackwell 把结果移入张量内存，并让两个 SM 合作一次乘法**

TMEM：结果离开寄存器

Hopper：共享内存｜Tensor Core｜寄存器保存结果

Blackwell：共享内存｜Tensor Core｜TMEM 256 KB 保存结果

寄存器被释放，以维持更多在飞加载

2-SM MMA：两个 SM，一次乘法

一次矩阵乘，两倍 tile

SM 0：加载共享 tile 的一半

SM 1：加载共享 tile 的另一半

每个 SM 只取两个 SM 都需要的一半 tile

ADVANCED —— 可略读，或自行深入阅读

NVIDIA, Blackwell Architecture whitepaper, 2024

## 第 34 页

**从一块 GPU 到多块：scale-up 与 scale-out**

8-GPU 节点（HGX H200）

GPU｜NVSwitch｜GPU｜GPU｜NVSwitch｜GPU｜GPU｜NVSwitch｜GPU｜GPU｜NVSwitch｜GPU

8 个 400 Gb/s NIC 接到 scale-out 网络

NVL72 机架（GB200）

4 GPU + 2 CPU｜NVLink switch｜4 GPU + 2 CPU

4 GPU + 2 CPU｜NVLink switch｜4 GPU + 2 CPU

4 GPU + 2 CPU｜NVLink switch｜4 GPU + 2 CPU

4 GPU + 2 CPU｜NVLink switch｜4 GPU + 2 CPU

⋮　⋮　× 9 行　⋮

NVIDIA, HGX H200 and GB200 NVL72 specifications, 2024

HBM 4.8 TB/s｜NVLink 900 GB/s｜RDMA 50 GB/s

HBM 8 TB/s｜NVLink 1.8 TB/s｜RDMA 100 GB/s

## 第 35 页

**NVIDIA GPU 二十年**

| 架构 | 对程序员而言改变了什么 |
| --- | --- |
| Tesla　2006 · G80 | 统一着色器；CUDA、线程块、共享内存 |
| Fermi　2010 · C2050 | 真正的 L1/L2 缓存、ECC、统一地址空间、快速 FP64 |
| Kepler　2012 · K20X | warp shuffle、动态并行、Hyper-Q 工作队列 |
| Maxwell　2014 · M40 | SM 分成四个分区；每瓦性能大幅提升 |
| Pascal　2016 · P100 | HBM2、NVLink、按页错误的统一内存、2× FP16 |
| Volta　2017 · V100 | Tensor Core、独立线程调度、统一 L1/共享内存 |

| 架构 | 对程序员而言改变了什么 |
| --- | --- |
| Turing　2018 · T4 | INT8 和 INT4 Tensor Core、光线追踪核 |
| Ampere　2020 · A100 | TF32、BF16、2:4 稀疏、cp.async、MIG、40 MB L2 |
| Hopper　2022 · H100 | FP8、TMA、cluster 与 DSMEM、wgmma、机密计算 |
| Blackwell　2024 · B200 | 双 die、FP6/FP4 与块缩放、TMEM、tcgen05、NVL72 |
| Blackwell Ultra　2025 · B300 | 288 GB HBM3e、15 PF 稠密 NVFP4、更快的 exp、大幅缩减的 FP64 |
| Rubin　2026 · NVL72 | HBM4、NVLink 6、更大的 TMEM 和共享内存（初步） |

ADVANCED —— 可略读，或自行深入阅读

2006–17：图形 → 通用计算｜2018–26：计算 → 低精度 AI 引擎

计算跑得比内存快，G80 → B300：峰值数学约 43,000×，带宽约 90×

GeForce 8 系列；Blackwell Ultra

## 第 36 页

**下一讲**

- 学生分享
- GPU 编程与性能优化
- LLM 服务（三）：批处理、分页与并行

## 第 37 页

**延伸阅读**

## 第 38 页

**AMD Instinct MI355X：一个 chiplet GPU，每个封装有更多 HBM**

与 NVIDIA GPU 的不同之处

- 一个封装上有 8 个计算 die，软件看来是一块 GPU
- 256 MB Infinity Cache 位于 HBM 之前
- 64 线程的 wavefront，而不是 32 线程的 warp

如何编程

- ROCm 和 HIP：CUDA 风格的 C++；hipify 可转换 CUDA 源码
- PyTorch、vLLM 和 SGLang 可运行在 ROCm 上
- 自定义 kernel 用 Triton 或 Composable Kernel

5.0 PF　稠密 FP8（B200：4.5 PF）

288 GB　HBM3E（B200：180 GB）

8 TB/s　HBM 带宽（B200：8 TB/s）

8 GPUs　scale-up 域（GB200 NVL72：72）

AMD, Instinct MI355X datasheet and CDNA 4 whitepaper, 2025

## 第 39 页

**Google TPU Ironwood：串联成 3D torus 的脉动阵列**

Google Cloud, TPU7x (Ironwood) documentation, 2026; Jouppi et al., ISCA 2023

如何编程

- JAX 或 PyTorch/XLA
- XLA 把矩阵乘切 tile 映射到阵列上
- 自定义 kernel 用 Pallas

4.6 PF　稠密 FP8 · B200 4.5

192 GB　HBM3E · B200 180

7.4 TB/s　HBM · B200 8

9,216 chips　3D torus · NVL72 72

SIMT lane

寄存器堆

FMA FMA FMA FMA

每条指令从寄存器堆读取操作数（灰色），并把结果（蓝色）写回

脉动阵列（权重驻留）

w00 w01 w02

w10 w11 w12

w20 w21 w22

每个权重留在自己的单元中

激活从左侧进入

部分和向下流动，并从底部离开

## 第 40 页

**Amazon Trainium3：带软件管理 SRAM 的脉动引擎**

与 NVIDIA GPU 的不同之处

- 8 个 NeuronCore，每个都有独立的 Tensor（脉动）、Vector 和 Scalar 引擎
- 每核 32 MB SRAM，由 DMA 引擎填充；没有硬件缓存
- 收益来自 MXFP8 和 MXFP4；每核的 BF16 与 Trainium2 相同

如何编程

- Neuron SDK 编译 PyTorch 和 JAX 计算图
- NKI（Neuron Kernel Interface）：用 Python 写 kernel，显式在 HBM 与 SRAM 之间搬运 tile
- 没有 CUDA；kernel 面向引擎，而不是线程

2.5 PF　稠密 MXFP8（B200：4.5 PF FP8）

144 GB　HBM3E（B200：180 GB）

4.9 TB/s　HBM 带宽（B200：8 TB/s）

144 chips　scale-up 域（GB200 NVL72：72）

AWS, Trainium3 Architecture Guide for NKI, 2025; AWS Trainium product page, 2025

## 第 41 页

**其他加速器：用片上 SRAM 取代 HBM**

| 芯片 | 片上 SRAM | 片外内存 | 权衡 |
| --- | --- | --- | --- |
| Cerebras WSE-3 | 44 GB | 无 | 整个晶圆是一块芯片；更大的模型要流式加载权重 |
| Groq LPU | 230 MB | 无 | 8 bit 的 70B 模型约需 300 块芯片 |
| Microsoft Maia 200 | 272 MB | 216 GB HBM3e | SRAM 存热数据；仅在 Azure 内可用 |

Cerebras, WSE-3 datasheet, 2024; Groq, LPU architecture, 2024; Microsoft, Maia 200, 2026
