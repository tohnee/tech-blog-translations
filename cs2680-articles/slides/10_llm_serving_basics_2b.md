---
title: "10_llm_serving_basics_2b"
source: https://cs2680.seas.harvard.edu/slides/10_llm_serving_basics_2b.pdf
pages: 44
crawled: 2026-11-16
---

# 10_llm_serving_basics_2b

> PDF 讲义文本抽取：[10_llm_serving_basics_2b.pdf](https://cs2680.seas.harvard.edu/slides/10_llm_serving_basics_2b.pdf) · Harvard CS2680

Modern AI Systems: Agents 
and System Optimizations
Juncheng Yang
LLM Serving Basics II: Intro to GPUs 

2Harvard MaDSys    ·   course.agentic-system.org 2
Logistics
• Assignment 4 will go out today and due in two and half weeks
• Goal: reason about performance, bottlenecks and improve iteratively, how 
real-world workloads differ from synthetic benchmarks
• Write-up is important, you only need to write a small number of lines of code
• NO LATE DAY for leaderboard submission. DO NOT grab more than one GPU
• Hard if you have limited prior experience in systems programming
• Proposal due next Wednesday (Oct 28)
• No limit on format or page
• DO NOT upload AI-generated content

3Harvard MaDSys    ·   course.agentic-system.org 3
Plan for today
• Introduction to GPU for LLM serving[1]
• GPU basics
• GPU architecture
• GPU programming and recent kernel advances
[1] We will not go into details; the goal is to help you build intuition

Harvard MaDSys    ·   course.agentic-system.org 4
GPU Programming

5Harvard MaDSys    ·   course.agentic-system.org 5
GPU code runs asynchronously
Host: CPU + DRAM runs main() Device: GPU + HBM runs kernels
PCIe Gen5 x16
~64 GB/s, 75× below HBM
CPU thread
Copy engine
SMs
cudaMalloc memcpy H→D launch other CPU work memcpy back (waits)
copy a, b in copy c out
vec_add kernel runs
time
Launch is asynchronously
CPU does not wait for GPU kernel to finish. 
Errors surface late
A kernel fault shows up at the next sync call.
NVIDIA, CUDA C++ Programming Guide, 2024; PCI-SIG, PCIe 5.0, 2019

6Harvard MaDSys    ·   course.agentic-system.org 6
A kernel is written for one thread (SIMT)
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
Global index
Each thread finds its element from block 
and thread IDs.
4,096 blocks
1M ÷ 256 threads; the GPU spreads them 
over 132 SMs.
Pick block sizes in multiples of 32
128–256 threads is typical; warps come 
from the linear tid.
Qualifier Runs on Called from
__global__ device host
__device__ device device
__host__ __device__ both either

7Harvard MaDSys    ·   course.agentic-system.org 7
Each thread's IDs pick its array element
1 LAUNCH: 4,096 BLOCKS × 256 THREADS
Block 0
0 1 … 255
Block 1
0 1 … 255
Block 2
0 1 … 255
Block 4,095
0 1 … 255…
2 EACH THREAD COMPUTES ITS INDEX
i
513
element
=
=
blockIdx.x
2
which block
*
×
blockDim.x
256
block size
+
+
threadIdx.x
1
slot in block
3 …AND WRITES ITS OWN ELEMENT out[i]
0 1 … 255 256 257 … 511 512 513 … 767 …  1,048,575…
NVIDIA, CUDA C++ Programming Guide

8Harvard MaDSys    ·   course.agentic-system.org 8
Blocks run on SMs as warps of 32
SOFTWARE HARDWARE
Grid
all blocks of one kernel launch
Whole GPU
blocks spread over 132 SMs
Block
up to 1,024 threads, shared memory
One SM
stays there until it finishes
Warp
32 threads in lockstep
One partition
scheduler issues it each cycle
Thread
own registers, own index
One core (also called lane)
one of the warp's 32 SIMT lanes
NVIDIA, CUDA C++ Programming Guide, 2024

9Harvard MaDSys    ·   course.agentic-system.org 9
Graph compilers (torch.compile): code the 
model, the compiler writes the kernels
torch.compile
import torch
 
def block(x, w, b):
    h = x @ w + b
    return gelu(h) * 0.5
 
# capture the graph, fuse, generate kernels
fast = torch.compile(block,
                     mode="max-autotune")
y = fast(x, w, b)  # first call compiles
 
# JAX: jax.jit(block) lowers to XLA
You decide
The math, in ordinary PyTorch or 
JAX. No threads, tiles or memory.
The compiler decides
Which ops fuse, tile sizes, and the 
generated Triton or XLA kernels.
Stops working when
Control flow breaks the graph, or 
the slow op cannot be fused.
Ansel et al., PyT orch 2, ASPLOS 2024; OpenXLA documentation, 2026

10Harvard MaDSys    ·   course.agentic-system.org 10
Tile languages: describe the work of a whole 
block, not one thread
CUDA C++ Tile language
You write the work of one thread the work of one tile of data
Indexing blockIdx × blockDim + threadIdx program_id + a range over the tile
Memory staging, sync you stage tiles, call __syncthreads() the compiler stages and syncs
Tensor Cores warp-level MMA instructions one dot product on whole tiles
Tile languages in use
Triton
Python; NVIDIA and 
AMD GPUs
Pallas
JAX kernels for TPU 
and GPU
TileLang
Python DSL built on 
TVM
ThunderKittens
C++ tile templates
cuTile
NVIDIA's tile model in 
CUDA
Tillet et al., MAPL 2019; Spector et al., ThunderKittens, 2024; NVIDIA CUDA 13.1, 2025

11Harvard MaDSys    ·   course.agentic-system.org 11
Triton: each program handles one tile of data
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
One program per tile
A program = one CUDA thread 
block; it owns BLOCK 
elements.
Compiler does the rest
Coalescing, shared-memory 
staging and Tensor Core MMA 
via tl.dot.
Autotuning picks the tile
@triton.autotune tries BLOCK 
sizes and warp counts per 
shape.
Tillet, Kung & Cox, Triton, MAPL 2019
ADVANCED — skim, or read more on your own

12Harvard MaDSys    ·   course.agentic-system.org 12
TileLang: you place each tile in shared 
memory, the compiler maps threads
TileLang matmul
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
You decide
Tile shapes, shared vs. register 
storage, and stages (tiles 
loaded ahead).
TileLang decides
Thread mapping, copy 
instructions, swizzles and the 
MMA calls.
Use it for
GEMM and attention variants 
that need explicit staging.
Wang et al., TileLang, arXiv 2025
ADVANCED — skim, or read more on your own

13Harvard MaDSys    ·   course.agentic-system.org 13
CuTe, CUTLASS and ThunderKittens: you 
choose layouts, async copies and warp roles
CuTe layouts (CuTe DSL, Python)
# a layout maps a coordinate to an offset
row = cute.make_layout((8, 4), stride=(4, 1))
col = cute.make_layout((8, 4), stride=(1, 8))
 
# (i, j) -> i*4 + j  versus  i + j*8
 
# the same algebra describes:
#  thread -> data in a warp
#  swizzled shared-memory tiles
#  TMA boxes and MMA fragments
You decide
Layouts, TMA and async 
pipelines, and which warps load 
or compute.
The library gives
Tested building blocks for copies, 
MMAs and pipelines per GPU.
Use it for
The last stretch to peak on GEMM 
and attention.
ADVANCED — skim, or read more on your own

14Harvard MaDSys    ·   course.agentic-system.org 14
Different levels of abstractions
Level Reach for it when Cost
Graph compiler
torch.compile, XLA Default for the whole model Little say over the slow op
Tile language
Helion, Triton, Pallas One op is unfused or missing Hours; ports across GPUs
Explicit tiles
TileLang You need to control staging Days
Layouts, warp roles
CuTe, CUTLASS, ThunderKittens GEMM or attention must reach peak Weeks; per GPU generation
Threads
CUDA C++ Irregular work: sort, sparse, graphs Everything is on you
Course synthesis of the preceding slides
ADVANCED — skim, or read more on your own

16Harvard MaDSys    ·   course.agentic-system.org 16
Every GPU program compiles down to SASS
NVCC device
NVCC host
Load time The driver runs the SASS that matches the GPU, else JIT-compiles the PTX and caches it.
Triton
CUDA Tile
device code NVVM PTX ptxas SASS fatbinary fatbin: SASS + PTX
host code GCC / Clang / MSVC host object linker executable + fatbin
@triton.jit Triton IR TritonGPU IR LLVM IR LLVM PTX ptxas SASS
(cubin)
cuTile Python, C++ CUDA Tile IR tileiras SASS
source intermediate code virtual ISA machine code
tool
ADVANCED — skim, or read more on your own

Harvard MaDSys    ·   course.agentic-system.org 21
GPU efficiency and utilization

22Harvard MaDSys    ·   course.agentic-system.org 22
MFU in inference: model FLOPs utilization
Model FLOPs utilization
MFU = achieved model FLOP/s ÷ peak 
FLOP/s
Model FLOPs: ≈ 2N per generated token, 
forward pass only
Peak: the GPU’s dense Tensor Core rate
Llama 2 70B on 8 H100s
Model FLOPs per token
2 × 70B ≈ 140 GFLOP
Achieved per GPU
3,040 tok/s × 140 GFLOP ≈ 426 TFLOP/s
MFU
426 ÷ 1,979 TFLOP/s ≈ 22%
Rule of thumb
Training 35–45%; 
inference prefill 40–60%, decode 10–40%

23Harvard MaDSys    ·   course.agentic-system.org 23
Four reasons why MFU is low
Chowdhery et al., PaLM, JMLR 2023; Korthikanti et al., Activation Recomputation, MLSys 2023
Communication
tensor-, pipeline- and data-parallel transfers not 
hidden behind compute
Pipeline bubbles
stages sit idle while each batch fills and drains 
the pipeline
Memory-bound kernels
norms, softmax and the optimizer step run at 
bandwidth, not Tensor Core peak
Recomputation (training)
activation checkpointing reruns forward work 
that MFU does not count
MFU separates hardware capability from software maturity

24Harvard MaDSys    ·   course.agentic-system.org 24
MBU: decode efficiency is bytes moved per 
second, not FLOPs
Model bandwidth utilization
MBU = achieved bytes/s ÷ peak HBM 
bandwidth
Bytes per decode step: all weights plus 
the KV cache read
Llama 3 8B, BF16, batch 1, H200
16 GB read per token
At 200 tok/s: 3.2 TB/s ÷ 4.8 TB/s ≈ 67%
Rule of thumb: report MFU for prefill and 
training, MBU for decode
Other measures of a serving system
Tokens/s per GPU
Throughput at a stated latency target, e.g. p50 
time per output token
Energy per token
Joules = average board power ÷ tokens/s
Cost per million tokens
$ per GPU-hour ÷ (tokens/s × 3,600) × 10⁶
Databricks, LLM Inference Performance Engineering, 2023

25Harvard MaDSys    ·   course.agentic-system.org 25
Profile the timeline, then the kernel
Nsight Systems (nsys)
nsys profile -o run ./app
Shows: one timeline of CPU threads, CUDA API 
calls, copies, kernels and streams.
Finds: idle gaps, serialized streams and launch 
overhead.
Nsight Compute (ncu)
ncu --set full -k vec_add ./app
Shows: each kernel replayed for counters: 
speed of light, memory traffic, warp stalls, hot 
lines.
Finds: why one kernel is slow. Replay timings are 
for comparison only.
nsys: find the slow region ncu: explain one kernel change one thing measure again
NVIDIA, Nsight Systems and Nsight Compute documentation, 2026
Intuition: scan the whole body (timeline) to find where time goes, then zoom in (kernel) to see why

26Harvard MaDSys    ·   course.agentic-system.org 26
GPU utilization
Counter What it measures
nvidia-smi utilization Share of time at least one kernel is running
SM active Share of SM cycles with a warp resident
SM occupancy Resident warps ÷ max warps, all SMs
Tensor pipe active Share of cycles the Tensor Cores are busy
DRAM active Share of cycles HBM is moving data
dcgmi dmon -e 203,1002,1003,1004,1005   one column per counter above
NVIDIA, DCGM User Guide: profiling metrics, 2026

27Harvard MaDSys    ·   course.agentic-system.org 27
Reading the counters: find which unit is busy
1. Is the GPU busy?
nvidia-smi at 100%
2. Are the SMs busy?
SM active high
3. Which unit is busy?
DRAM vs Tensor pipe active
Yes Yes
No No
GPU idle between 
kernels
CPU launch overhead or 
data loading
Next: Nsight Systems 
timeline; CUDA graphs
Too few thread 
blocks
Work does not fill all the 
SMs
Next: larger batch, 
more blocks per kernel
DRAM active high
Memory-bound → judge by MBU
Tensor pipe active high
Compute-bound → judge by MFU
Both low
Latency-bound → Nsight Compute
NVIDIA, DCGM User Guide: profiling metrics, 2026

30Harvard MaDSys    ·   course.agentic-system.org 30
GPU efficiency: what to take away
1  MFU: achieved model FLOP/s ÷ dense peak; judge prefill and training by it.
2  Low MFU: communication, pipeline bubbles, memory-bound kernels and recomputation 
eat the peak.
3  MBU: achieved bytes/s ÷ peak HBM bandwidth; judge decode by it.
4  Counters: nvidia-smi at 100% only means a kernel is running; read SM, Tensor and DRAM 
activity.

Harvard MaDSys    ·   course.agentic-system.org 31
Recent Advances in GPU Kernel Optimizations

32Harvard MaDSys    ·   course.agentic-system.org 32
Kernels lose GPU time in three places
1  Inside a kernel
SM
MMA exp load
Lost time
Tensor Cores wait on 
loads, softmax and exp.
Advances
FlashAttention, warp 
specialization, 
FlashAttention-4
2  Across SMs
Lost time
SMs sit idle in uneven 
rounds and between 
kernel launches.
Advances
Persistent kernels, split-
KV, CUDA Graphs, PDL, 
megakernels
3  Across GPUs
GPU 0 GPU 1
Lost time
GPUs wait for each 
other’s data.
Advances
Fused collectives, MoE 
all-to-all overlap
Writing kernels
write test
Lost engineer time
Each new GPU needs 
new hand-tuned 
kernels.
Advances
Agents that write and 
test kernels

34Harvard MaDSys    ·   course.agentic-system.org 34
Kernel fusion
Vertical: chain the steps, horizontal: merge parallel ops
Vertical fusion
A producer feeds its consumer inside one kernel.
GEMM + bias GELU
one kernel: each result stays in registers
Saves: HBM round trips
Examples: GEMM epilogues, LayerNorm, softmax with mask
Horizontal fusion
Ops that share an input merge into one kernel.
x · W_q
x · W_k
x · W_v
x · [W_q  W_k  W_v]
one GEMM: x is read once, one launch
Saves: launches and repeated reads of x
Examples: QKV projection, FFN gate + up
Compilers do both: torch.compile fuses vertical chains into one Triton kernel; model code often fuses 
QKV and gate + up weights by hand (concatenating them).
Unfused read x write t read t write u read u write y 1.25 ms
Scale, add bias, ReLU as three kernels on 1 GB of FP32: every step goes through HBM
Fused read x write y 0.42 ms, 3× less HBM traffic

35Harvard MaDSys    ·   course.agentic-system.org 35
FlashAttention: compute attention tile by tile 
so S never reaches HBM
The problem
Standard attention writes the 
n × n score matrix S and its 
softmax P to HBM, then reads 
them back.
At 8K tokens that is 67M 
scores per head in every layer, 
all moved through HBM.
Dao et al., FlashAttention, NeurIPS 2022; Dao, FlashAttention-2, ICLR 2024
Solution
On chip: one block’s shared memory and registers
Q tile × K₁ V₁ K₂ V₂ K₃ V₃ …
S tile = Q·Kᵀ softmax · V
running max, sum O tile
Repeat for every K, V tile: S and P never leave the chip
HBM
read K, V once write O once

36Harvard MaDSys    ·   course.agentic-system.org 36
From FlashAttention to FlashAttention-4
FlashAttention
2022 · A100
Bottleneck
HBM traffic: the n × n 
score matrix is written 
and read back
Fix
Tile Q, K, V in shared 
memory; online softmax
2–4× faster attention; 
memory linear in length
FlashAttention-2
2023 · A100
Bottleneck
Low occupancy: one 
block per head, many 
non-matmul FLOPs
Fix
Split work across the 
sequence; fewer rescales
About 2× FA1; up to 
~70% of A100 peak
FlashAttention-3
2024 · H100
Bottleneck
T ensor Cores wait while 
warps load and compute 
softmax
Fix
TMA + warp 
specialization; overlap 
softmax with GEMM; FP8
About 75% of H100 peak 
in FP16
FlashAttention-4
2025 · B200
Bottleneck
T ensor Cores doubled, 
exp unit did not: softmax 
is the bottleneck
Fix
TMEM accumulators; part 
of exp on FMA units
Faster than cuDNN 
attention on B200
Dao et al. 2022; Dao 2023; Shah et al. 2024; Dao et al. 2025
ADVANCED — skim, or read more on your own

39Harvard MaDSys    ·   course.agentic-system.org 39
Persistent kernels: one thread block per SM 
works through many tiles
Problem
A matrix multiply is cut into 
160 output tiles, one thread 
block per tile. The GPU has 
132 SMs, so the blocks run in 
two rounds.
Round 2 has only 28 blocks: 
104 SMs wait. Each block 
also redoes its setup for one 
tile.
Solution
Takeaway: launch one block per SM and let it loop over tiles: no idle round, and setup runs once. 
CUTLASS and DeepGEMM do this.
Osama et al., Stream-K, PPoPP 2023; NVIDIA CUTLASS 3.x, 2024
Normal launch: one block per tile, run in rounds
Round 1: 132 blocks fill all 132 SMs
Round 2: 28 104 SMs idle
Persistent kernel: 132 blocks stay put and take tiles one by one
Compute
Write out
tile 0 math
write tile 0
tile 1 math
write tile 1
tile 2 math
write tile 2
Stream-K: cut tiles into smaller pieces so all SMs finish together
ADVANCED — skim, or read more on your own

40Harvard MaDSys    ·   course.agentic-system.org 40
Split-KV balances decode across SMs
Problem
Decode has one query token 
per request, so splitting only 
over batch × heads leaves 
SMs idle.
KV lengths differ by 100× 
across requests, and their 
pages sit scattered in HBM.
Solution
Takeaway: FlashInfer (MLSys 2025 Outstanding Paper) pairs block-sparse KV with JIT-specialized 
kernels and this scheduler; vLLM and SGLang use it.
Dao et al., Flash-Decoding, 2023; Y e et al., FlashInfer , MLSys 2025
KV pages per request
R1
R2
R3
Split-KV: 4 pages per SM
SM0
SM1
SM2
SM3
Merge partial (m, ℓ, O) per request, as in online softmax
Paged KV as block-sparse rows Fixed grid: CUDA Graph-safe
ADVANCED — skim, or read more on your own

41Harvard MaDSys    ·   course.agentic-system.org 41
CUDA Graphs: record the launches once, 
replay them with one call
Problem
Decoding one token runs 
dozens of small kernels.
Each launch costs a few µs 
of CPU and driver time, so 
the GPU waits between 
kernels.
Solution
Normal stream: one CPU launch per kernel
CPU
GPU
CUDA Graph: one call replays all of them
CPU
GPU
graph launch
no gaps, done sooner
cudaStreamBeginCapture(s, mode);   // record one step
  …launch the kernels…;  cudaStreamEndCapture(s, &g);
cudaGraphInstantiate(&e, g, 0);  cudaGraphLaunch(e, s);
NVIDIA CUDA Programming Guide, CUDA Graphs, 2025
Takeaway: capture a decode step once and replay it every token; vLLM and SGLang do this.
ADVANCED — skim, or read more on your own

42Harvard MaDSys    ·   course.agentic-system.org 42
Programmatic Dependent Launch (PDL) starts the 
next kernel early
Problem
In a stream, kernel B 
launches only after kernel A 
has fully drained and flushed 
memory.
Decode runs many µs-scale 
kernels per token, so launch 
latency, prologue and each 
kernel's tail add up.
Solution
Takeaway: PDL needs Hopper or newer (SM 9.0); it cuts per-kernel gaps in decode, and works inside 
CUDA Graphs.
NVIDIA CUDA Programming Guide §4.5, 2025
Default stream order
Kernel A gap prologue Kernel B
With PDL
Kernel A
prologue wait Kernel B
trigger sync
A: cudaTriggerProgrammaticLaunchCompletion();
B: cudaGridDependencySynchronize();
ADVANCED — skim, or read more on your own

43Harvard MaDSys    ·   course.agentic-system.org 43
A megakernel runs the model in one launch
Problem
Batch-1 decode of 
Llama-3.2-1B runs ~7 
kernels per layer × 16 layers 
for every token.
Each boundary drains the 
GPU before the next kernel 
loads weights; vLLM and 
SGLang use ~50% of H100 
bandwidth.
Solution
Takeaway: the Hazy Research megakernel reaches 78% of H100 bandwidth at batch 1, ~1.5× SGLang 
per-user throughput. Mirage MPK compiles such task graphs automatically.
Spector , Juravsky et al., Look Ma, No Bubbles!, Hazy Research 2025; Mirage MPK, 2025
Kernel per op: bubbles at every launch boundary
Norm QKV Attn O-proj FFN
Megakernel: next op’s weights load during the current op
Norm QKV Attn O-proj FFN
On-GPU 
interpreter
Per-SM instruction 
queue
Paged SMEM for 
weights
Global counters 
for dependencies
ADVANCED — skim, or read more on your own

44Harvard MaDSys    ·   course.agentic-system.org 44
Fused collectives hide TP communication
Problem
Tensor parallelism splits 
each layer across 8 GPUs, 
adding an AllGather before 
and a ReduceScatter after 
every sharded GEMM.
Run as separate kernels, the 
GEMM waits for the whole 
collective.
Solution
Takeaway: Flux overlaps up to 96% of the communication and runs up to 1.66× faster prefill and 1.30× 
faster decode than vLLM on 8 GPUs.
Chang et al., FLUX, arXiv:2406.06858, 2024
Separate kernels: GEMM, then ReduceScatter
GEMM (all tiles) ReduceScatter
Fused: each tile's epilogue writes to its owner GPU
Compute
NVLink
t0
t0
t1
t1
t2
t2
t3
t3
t4
t4
t5
t5
AllGather + GEMM: tiles start as their 
rows arrive
Peer writes via NVLink or NVSHMEM, 
no extra kernel
ADVANCED — skim, or read more on your own

45Harvard MaDSys    ·   course.agentic-system.org 45
MoE all-to-all hides behind compute
Problem
Each MoE layer sends every 
token to its top-8 experts on 
other GPUs, then gathers the 
outputs back.
Run back to back, dispatch 
and combine leave Tensor 
Cores idle, and NCCL 
kernels take SMs from 
compute.
Solution
Takeaway: DeepEP sustains ~153 GB/s dispatch over NVLink within a node and ~43 GB/s over RDMA 
across nodes, close to link peak.
DeepSeek-AI, DeepEP , 2025; DeepSeek-V3, arXiv:2412.19437
Serial: dispatch, experts, combine, then the next layer
Dispatch Expert GEMM Combine Attention
DeepEP: two micro-batches overlap
SMs
Network
Attn A Attn B Experts A Experts B
Dispatch A Dispatch B Combine A Combine B
Hook-based transfers run on the NIC and use no SMs
Dispatch in FP8 Combine in BF16 NVLink → RDMA forwarding
ADVANCED — skim, or read more on your own

46Harvard MaDSys    ·   course.agentic-system.org 46
Agents become the new compiler
Problem
Each GPU generation (TMA, 
TMEM, FP4) and each 
attention variant needs new 
hand-tuned kernels, and few 
engineers write them.
Generated kernels can look 
fast by passing a weak test 
or exploiting the harness.
Solution
Ouyang et al., KernelBench, 2025; AutoMegaKernel, arXiv:2606.09682, 2026
Agent writes kernel (CUDA, 
Triton, CuTe DSL) Compile (nvcc, ptxas errors)
Check vs PyTorch reference 
on many shapes
Profile: runtime, Nsight 
counters
feedback loop
fastp: share of tasks that are correct and more than p× faster than PyTorch. Static 
checks reject racy schedules.
ADVANCED — skim, or read more on your own

47Harvard MaDSys    ·   course.agentic-system.org 47
Kernel advances: what to take away
1  Inside a kernel: feed the Tensor Cores. Fuse epilogues, scale per block in FP8/FP4, split 
warps into producers and consumers, and move work off the slowest unit.
2  Across SMs and launches: remove idle time. Persistent CTAs and split-KV balance the 
SMs; PDL and megakernels close the gaps between kernels.
3  Across GPUs: hide communication. Fuse tensor-parallel collectives into GEMM tiles and 
overlap MoE all-to-all with expert compute.
4  Writing kernels: automate the search. Agents write and profile candidate kernels; 
correctness checks on many shapes decide which survive.

48Harvard MaDSys    ·   course.agentic-system.org 48
Challenges in AI hardware
Networking 9× slower off-node
KV-cache handoff, 32K-token Llama 3 70B prompt
Reliability 1 failure every 3 hours1
Causes of 419 interruptions, Llama 3 training
Power 8× a conventional rack
Power per rack2
Cooling and water
GB200 NVL72 racks require liquid cooling 2
700,000 L
freshwater to train 
GPT-33
4.2–6.6B
m³ withdrawn by AI, 
2027E3
1The Llama 3 Herd of Models   2NVIDIA HGX Platform: Data Center Physical Requirements Guide
3Making AI Less “Thirsty”
215 ms
24 ms
400G NIC
NVLink (H100)
8%
17%
30%
Network
HBM3 memory
GPU faults
120 kW
60 kW
15 kW
GB200 NVL72
HGX B200
Conventional

49Harvard MaDSys    ·   course.agentic-system.org 49
Next class

Harvard MaDSys    ·   course.agentic-system.org 50
Optional reading
Optimize GPU code

51Harvard MaDSys    ·   course.agentic-system.org 51
Optimizing GPU code: four goals that 
combine in one kernel
Move less data
Fewer bytes moved per result
e.g. Coalescing, tiling, fusion
Hide waiting time
Keep units busy while loads finish
e.g. Async copies, warp specialization
Expose more parallelism
Give every SM enough independent work
e.g. Split-K, independent accumulators
Use faster instructions
Same math on cheaper hardware paths
e.g. Tensor Cores, lower precision
They stack: a fast GEMM coalesces loads, double-buffers tiles and uses Tensor Cores.
NVIDIA, CUDA C++ Best Practices Guide; NVIDIA, CUTLASS documentation

52Harvard MaDSys    ·   course.agentic-system.org 52
Optimize memory traffic: move fewer bytes, 
reuse each one more
Technique Core idea Example
Memory coalescing Neighboring threads read contiguous 
addresses Thread i reads x[i], not x[32·i]
Shared-memory tiling Load a block once; cooperating threads 
reuse it
Matrix tiles reused across many 
outputs
Register tiling Each thread computes several outputs 
from registers Several accumulators per thread
Kernel fusion Consume intermediates at once, 
skipping the HBM round trip
Matmul + bias + activation in one 
kernel
Padding / swizzling Change shared-memory layout to avoid 
bank conflicts Transpose tile 32×32 → 32×33
Cache-aware ordering Schedule nearby blocks so they reuse 
cached data
Group output tiles that read the 
same inputs
NVIDIA, CUDA C++ Best Practices Guide; NVIDIA, CUDA C++ Programming Guide

53Harvard MaDSys    ·   course.agentic-system.org 53
Hide waiting and expose parallelism: keep 
every SM issuing work
Technique Core idea Example
Async copies + double 
buffering
Load the next tile while computing on 
the current one
Alternate two shared-memory 
buffers in a GEMM
Instruction-level 
parallelism
Independent instructions issue while 
earlier ones wait
Several accumulators, not one 
dependency chain
Warp specialization Different warps take different pipeline 
roles
Producer warps load; consumer 
warps run MMAs
Split-K / split reductions Spread a long reduction over more 
workers, then merge
Split a long KV sequence across 
blocks in decode
Warp-level 
communication
Exchange values register to register in 
a warp Shuffle-based warp sum or max
The cost: split-K adds a merge step; pipelining adds buffers and syncs.
NVIDIA, CUTLASS documentation; NVIDIA, CUDA C++ Programming Guide

54Harvard MaDSys    ·   course.agentic-system.org 54
Cheaper computation: run the same math on 
faster instructions
Technique Core idea Example
Tensor Core mapping Shape matrix ops into tiles and layouts 
the hardware supports
MMA instructions instead of scalar 
FMAs
Lower precision Fewer bytes stored and moved; faster 
math where supported
FP16/BF16 inputs, FP32 
accumulation
Unrolling + 
specialization
Fix structure at compile time; drop 
runtime work
Kernel built for one head dim or 
mask type
Less branch divergence Keep threads in a warp on the same 
path
Group tasks with similar control 
flow
Autotuning Measure variants for each workload 
shape
Search tile size, warp count, 
pipeline depth
Two separate choices: Tensor Cores need fitting shapes; precision must stay accurate.
NVIDIA, CUDA C++ Programming Guide; NVIDIA, CUTLASS documentation
