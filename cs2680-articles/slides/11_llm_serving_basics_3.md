---
title: "11_llm_serving_basics_3"
source: https://cs2680.seas.harvard.edu/slides/11_llm_serving_basics_3.pdf
pages: 59
crawled: 2026-11-16
---

# 11_llm_serving_basics_3

> PDF 讲义文本抽取：[11_llm_serving_basics_3.pdf](https://cs2680.seas.harvard.edu/slides/11_llm_serving_basics_3.pdf) · Harvard CS2680

Modern AI Systems: Agents 
and System Optimizations
Juncheng Yang
LLM Serving Basics III: scheduling, paging and parallelism 

2Harvard MaDSys    ·   course.agentic-system.org 2
Plan for today
• LLM serving performance evaluation
• Scheduling and resource management
• Parallelism

3Harvard MaDSys    ·   course.agentic-system.org 3
Logistics
• Assignment 4 due next Tuesday midnight
• Reading and tune engine flags
• Speculative decoding
• Agent-engine co-design
• Measurement / observation + reasoning in write -up and video
• what you saw, what you did, what changed and why, what is the trade-off
• more than one counter and metric when you measure
• Project proposal due last Wednesday

4Harvard MaDSys    ·   course.agentic-system.org 4
LLM serving is different from previous 
computing, e.g., web service, batch jobs
Web request runs to completion in about 5–50 ms
LLM request
prefill decode: one batched forward pass per token
Why spend several classes on LLM serving?
Huge compute
LLMs need GPUs and 
other accelerators
Paid on every token
each user request 
reruns the model
GPUs are costly
serving efficiency sets 
cost and speed

6Harvard MaDSys    ·   course.agentic-system.org 6
How LLM serving differs: inside a single request
Two phases, two 
bottlenecks
Web request one short, stateless call
LLM request Prefill: compute-bound Decode: memory-bound
Multi-GPU, multi-server 
compute and communicate
One request's forward pass
GPU 1 GPU 2 GPU 3 GPU 4
Soft, growing state Router
GPU 1: holds its KV cache
GPU 2: must rebuild it
Tokens = 
checkpoint to 
rebuild state

7Harvard MaDSys    ·   course.agentic-system.org 7
How LLM serving differs: across many requests
Unknown output length Prompt: known Output: unknown until stop token
Tokens as the unit of work
Admission Scheduling Routing Autoscaling
Rate limits Prices SLOs counted in tokens
10⁴–10⁶×
cost spread
Shifting bottlenecks
Batch size
small 
  large
Context length
short 
  long
Phase mix
prefill 
  decode
Agents and reasoning 
widen every gap
Turn 1 new
Turn 2 reused new
Turn 3 reused prefix new
≈90% prefix reuse
KV cache becomes a 
storage problem

8Harvard MaDSys    ·   course.agentic-system.org 8
LLM inference metrics and evaluation

9Harvard MaDSys    ·   course.agentic-system.org 9
The two phases of LLM serving: prefill and decode
Prefill Decode
Granularity All S prompt tokens at once 1 token / step
Dominant op Matrix–matrix GEMM GEMV / thin GEMM
Bottleneck Compute (FLOPs) Memory bandwidth
Latency driver TTFT TPOT × output length
Serving effect: one request mixes a compute-bound phase and a memory-bound phase
Evaluation

11Harvard MaDSys    ·   course.agentic-system.org 11
Serving metrics on one request’s timeline
TTFT TBT decode → one token per pass
queue prefill t1 t2 t3 t4 t5 t6
time →
TPOT = average of the 5 TBT gaps (t2…t6)
TBT is one gap, measured per token, so its P99 catches stalls.
TPOT averages every gap: (E2E − TTFT) ÷ (n − 1). A few long stalls barely move it.
E2E = TTFT + TPOT × (n − 1): arrival to last token (t6)
Throughput is tokens/s per GPU across all requests, maximized by large batches.
Goodput is throughput counting only requests that meet their TTFT and TPOT SLOs.
Evaluation

12Harvard MaDSys    ·   course.agentic-system.org 12
GPU throughput vs user throughput
GPU throughput
all tokens the server emits per 
second
User throughput
1 ÷ TPOT — what one reader feels
Batch 1 → 64
20× the GPU, but 3× slower per user
0
2K
4K
6K
0 25 50 75 100
Interactivity (TPS per user)
6K TPS/GPU
100 TPS/user
TPS per GPU
Evaluation

13Harvard MaDSys    ·   course.agentic-system.org 13
Pitfall 1: Short, transient runs
Example: 500 requests sent at once 
• Early ones pay for kernel 
compilation, lazy loading, GPU clock 
ramping, and cold prefix caches; 
• Late ones run in a shrinking batch. 
A whole-run average blends both.
What you should do: report steady state 
performance. 
Throughput in one run, K tokens/s
Illustrative; x-axis in seconds
5.0K
0K
2K
4K
6K
0 15 30 45 60
Warmup Drain
Measure here
Evaluation

14Harvard MaDSys    ·   course.agentic-system.org 14
Pitfall 2: Reporting misleading or opaque metrics
Requests differ in prompt length, output length and latency sensitivity, so one average 
can hide what a user sees.
Example: two responses, 100 tokens each, both streamed in 5 s
Smooth 50 ms
Stalled Stalled 4.5 s, no new tokens 50 ms
Mean TPOT
Same 50 ms TPOT, yet one user watches a frozen stream for 4.5 s.
Evaluation
Max TBT
50 ms
4,500 ms
0 s 5 s
What you should do: (1) show the full distribution; (2) report TTFT, TPOT, and throughput. 

15Harvard MaDSys    ·   course.agentic-system.org 15
Pitfall 3: Unrealistic workloads
Token content
Benchmark
Real
Draft tokens rarely get accepted
kq 7z ##vl 3x
Summarize this email
Length distribution
Benchmark
Real
One 320K prompt stalls a batch
320K
Request arrival
Benchmark
Real
Bursts push P99 TTFT way up
Prefix cache hits
Benchmark
Real
A shared prompt skips prefill
Evaluation
What you should do: replay real traces, with real lengths and arrival times.

16Harvard MaDSys    ·   course.agentic-system.org 16
Pitfall 4: Unfair comparison
Fix: tune every baseline on the same hardware, then switch each technique off to measure its 
impact.
Evaluation
Unequal resources or 
tuning
Ours: 8 GPUs
Baseline: 4 GPUs
Twice the GPUs can explain 
a 2× win
Untuned baselines
Default baseline
1.0×
Tuned baseline
1.6×
Ours, tuned
1.8×
Real gain over tuned:
1.8 ÷ 1.6 ≈ 1.1×
Not isolating the 
algorithm
Implementation Algorithm
70% of speedup 30%
Only 30% comes from the 
algorithm

22Harvard MaDSys    ·   course.agentic-system.org 22
Batching, scheduling, paging and caching
Batching
Request scheduling
Memory management
Prefix caching

23Harvard MaDSys    ·   course.agentic-system.org 23
Continuous batching and iteration-level scheduling
Static Batching
Client forms a batch
Runs the whole batch to 
completion
Client
Server
idle
idle
time
Dynamic Batching
Sends each request as it 
arrives
Wait and form a batch
Client
Server
wait
wait
wait
idle
idle
time
Continuous Batching
Sends each request as it 
arrives
Batch sequences together 
per token generation 
iteration
Client
Server
new
new
time
Batching

24Harvard MaDSys    ·   course.agentic-system.org 24
Ordinary batching breaks when requests differ in 
input length and KV history
Request Phase
Tokens this 
step
KV-cache 
length
A Prefill 128 0
B Decode 1 500
C Decode 1 1,000
Pad every input to 128 tokens
A 128 useful
B 127 padded
C 127 padded
Yu et al., OSDI 2022 (Orca)
Batching

25Harvard MaDSys    ·   course.agentic-system.org 25
Attention can't share one GEMM: each request reads 
its own KV cache, and the lengths differ
Batching
Linear layer: batched
Tokens Shared W Output
A A
B B
C C
× W =
Every token multiplies the same W, so one 
GEMM serves all requests
Attention: per request
Query Own KV cache, tokens
A × 300
B × 40
C × 120
No shared operand and ragged lengths, so 
each request runs its own attention
Orca's observation: not every Transformer operation needs the same batching strategy.
Yu et al., OSDI 2022 (Orca)

26Harvard MaDSys    ·   course.agentic-system.org 26
Selective batching: batch every linear layer, split only 
attention by request
Flatten Batched Per request Batched Batched
Input tokens
from all 
requests, one 
token-major 
matrix
QKV 
projections
one GEMM 
over all 
tokens
Attention A
own KV cache
Attention B
own KV cache
Attention C
own KV cache
Merge + 
output 
projection
one GEMM
MLP , 
LayerNorm, 
residual
batched over 
all tokens
Why it works: linear layers treat every token the same, so one GEMM serves all requests; only 
attention needs each request's own KV cache.
Yu et al., OSDI 2022 (Orca)
Batching

27Harvard MaDSys    ·   course.agentic-system.org 27
Request scheduling
FCFS/SJF · chunked prefill · disaggregation

28Harvard MaDSys    ·   course.agentic-system.org 28
Request scheduling: first-come, first-served (FCFS)
vLLM and SGLang default to FCFS
• Admits waiting requests in arrival order as KV-cache space frees up
• Simple and starvation-free, but one long request at the head delays all behind it
But how to mix the prefill of an incoming request vs ongoing decode?
Prefill immediately
Larger batches, but blocks all 
decoding requests
Wait until decode finishes
TPOT less affected, but long queueing 
for new requests
Scheduling
D D Prefill D D
Decodes stall here
D D D D D Prefill
New request waits

29Harvard MaDSys    ·   course.agentic-system.org 29
Prefill-first schedulers protect TTFT; decode-first 
schedulers protect TPOT
Prefill-first  SGLang
D D Prefill D D time →
+ TTFT: new prompts start at once
+ Throughput: batch refills every step
− TPOT: each arrival stalls all decodes
Decode-first  FasterTransformer
D D D D D Prefill time →
+ TPOT: steady token stream
− TTFT: new prompts wait for a drain
− Throughput: batch shrinks as requests end
Two ways to break the trade-off
Chunked prefill
Mix small prompt chunks into decode batches
Disaggregation
Run prefill and decode on separate GPUs
Framing from Agrawal et al., Sarathi-Serve, OSDI 2024
Scheduling

30Harvard MaDSys    ·   course.agentic-system.org 30
Chunked prefill aims to strike a balance
Box width = step time. D = decode-only step for 4 running requests.
No chunking D Prefill 2,048 tokens + 4 decodes · 92 ms D D
Running requests wait 92 ms for their next token
512-token 
chunks D Chunk 1
+ 4 decodes
Chunk 2
+ 4 decodes
Chunk 3
+ 4 decodes
Chunk 4
+ 4 decodes D D
Each step: 512 prompt tokens + 4 decodes, so a token every ~23 ms
A per-step token budget bounds iteration latency
This relies on mixed-batch kernels being as efficient as pure prefill or decode kernels. 
SGLang: prefill-prioritized (with decode protection --prefill-decode-interval N)
vLLM: decode-prioritized (with chunked prefill)
Agrawal et al., Sarathi-Serve, OSDI 2024; SGLang and vLLM scheduler docs
Scheduling
What is the downside of chunked prefill?

31Harvard MaDSys    ·   course.agentic-system.org 31
Chunked prefill needs more memory reads
2,048-token prompt, chunk size 512
Iter 1 chunk 1
Iter 2 cached KV chunk 2
Iter 3 cached KV cached KV chunk 3
Iter 4 cached KV cached KV cached KV chunk 4
Computed now Read from cache Not yet
Same total prefill FLOPs, spread over 4 shorter steps.
Cost: KV is re-read
Chunk k reads (k − 1) × 512 tokens
Agrawal et al., Sarathi (2023) and Sarathi-Serve (OSDI 2024); vLLM: enable_chunked_prefill
Chunk size trades decode latency against prefill efficiency
Scheduling

32Harvard MaDSys    ·   course.agentic-system.org 32
PD disaggregation separates prefill and decode
One request’s path
Prompt
arrives
Prefill pool
Runs the prompt,
emits token 1
KV cache
per request
Decode pool
Loads KV , then
decodes in big batches
Tokens
2 … n
Prefill pool
Compute-bound; sized and 
parallelized for TTFT
KV transfer
Prompt KV sent layer by layer 
over NVLink or RDMA
Decode pool
Memory-bound; large batches, 
sized for TPOT
DistServe (Zhong et al., OSDI 2024); Splitwise (Patel et al., ISCA 2024); Mooncake (Qin et al., FAST 2025)
Scheduling

33Harvard MaDSys    ·   course.agentic-system.org 33
Each pool gets its own parallelism and batch size, 
tuned to its own SLO
Configure each pool separately
Prefill pool Decode pool
Target TTFT SLO TPOT SLO
Batch one or a few prompts 100s of sequences
Parallelism more TP , less latency more replicas
Best GPU high FLOPS high HBM bandwidth
The costs: a KV transfer per request, a P:D ratio to tune, two or more instances.
Zhong et al., DistServe, OSDI 2024; Patel et al., Splitwise, ISCA 2024
Scheduling

34Harvard MaDSys    ·   course.agentic-system.org 34
PD disaggregation requires moving the KV cache 
between nodes
KV size: Llama-3.1-70B (GQA), FP16
2 (K, V) × 80 layers × 8 KV heads
× 128 dims × 2 bytes
= 320 KB per token
× 65,536 tokens = 20 GB
Its prefill ≈ 11.5 s
2 × 70B × 65,536 ÷ (4 × 200 TFLOPS)
Time to move 20 GB
Link Bandwidth Time
NVLink, H100 450 GB/s 44 ms
NVLink, A100 300 GB/s 67 ms
InfiniBand 400 Gb/s 50 GB/s 400 ms
PCIe 4.0 x16 32 GB/s 625 ms
Ethernet 100 Gb/s 12.5 GB/s 1.6 s
Even 400 ms is under 4% of the prefill.
Streaming per layer hides most of it: layer i’s KV ships while layer i+1 computes.
Scheduling

35Harvard MaDSys    ·   course.agentic-system.org 35
From FCFS to SJF: short requests should not wait 
behind long ones
Head-of-line blocking: a full batch, served in arrival order
GPU
batch full
R0 · long answer
1,000 output tokens
R1
20 tok
R2
20 tok
R3
20 tok
R4
20 tok
R1–R4 wait for all of R0's tokensQueue head on the left; arrival order R0 → R4
FCFS
Serve in arrival order. Default in vLLM and 
SGLang; one long job delays every request 
behind it.
SJF
Serve the shortest job first. Minimizes 
average waiting time, but needs each job’s 
size up front.
For LLMs, job size depends on output length, and it is unknown until decoding ends.
Scheduling

36Harvard MaDSys    ·   course.agentic-system.org 36
Shortest-job-first needs output lengths, so learn to 
rank them
Three requests arrive together; the GPU emits one token per second
FCFS R0 · 10 tokens R1 · 2 R2 avg 6.7 s/token
SJF R2 R1 · 2 R0 · 10 tokens avg 1.3 s/token
0 s 13 s
The catch: output length is unknown until decoding ends, so it must be predicted
Waiting prompts OPT-125M ranker 
scores each prompt
Queue sorted by 
predicted rank
vLLM batch takes the 
top each step
Rank instead of regress
Trained with a ranking loss; 
only relative order matters
Starvation guard
A request that waits too long 
is promoted
Fu et al., Efficient LLM Scheduling by Learning to Rank, NeurIPS 2024
ADVANCED — skim, or read more on your own
Scheduling

37Harvard MaDSys    ·   course.agentic-system.org 37
FastServe: token-level preemption with a skip-join 
multi-level queue
Skip-join by prompt length
A new job enters the highest queue 
whose quantum covers its prefill time
Wu et al., FastServe, NSDI 2026 (arXiv 2305.05920)
Q1 q
Q2 2q
Q3 4q
Q4 8q · lowest priority
Long prompt
prefill > 2q → Q3
Demotion
A job that uses up its quantum drops 
one queue
Promotion
Jobs that wait too long are promoted 
back up to prevent starvation
Why it works: long jobs sink and short jobs finish first, so it approximates SRPT (shortest remaining 
processing time first) without knowing job sizes
ADVANCED — skim, or read more on your own
Short prompt
prefill ≤ q → Q1
Scheduling
Bar length = time slice per turn →
↓ quantum used up: demote   ·   Q1 = highest priority

40Harvard MaDSys    ·   course.agentic-system.org 40
Check your understanding: request scheduling
Q1. P99 TBT spikes whenever a long prompt arrives. Which techniques can fix this?
Answer: Chunked prefill caps prompt tokens per step; PD disaggregation keeps prefill out of decode steps.
Q2. When is PD disaggregation not worth deploying?
Answer: Short prompts or small fleets: KV transfer, P:D tuning and extra instances cost more than the stalls.
Q3. SJF needs job sizes. Are there other methods to avoid it for agentic workloads? 
Answer: Use uncached prefill tokens as job size. 
Scheduling

41Harvard MaDSys    ·   course.agentic-system.org 41
Memory management
PagedAttention

43Harvard MaDSys    ·   course.agentic-system.org 43
Unknown output length forces KV reservation that 
wastes memory three ways
Llama-3.1-70B on two H200s, 282 GB of memory
Weights  141 GB · 50% KV cache  ~130 GB · 45% Act.
320 KB per token  ·  40 GB per request at the 128K-token limit  ·  ~3 such requests fill the KV budget
The cat sat on Hi all
Request A: reserved for its 128K-token max Request B
In use Reserved Internal External In use Res. Int. External
1  Reserved
Slots held for tokens not yet generated. Used 
later, but idle until then.
2  Internal fragmentation
Slots past the real end. The reply hits EOS before 
its maximum length.
Only 20–38% of KV memory held real tokens in Orca-style contiguous allocators.
Sources: Kwon et al., SOSP 2023, Fig. 2–3; Meta Llama 3.1 70B config, 2024; NVIDIA H200 datasheet
PagedAttention

44Harvard MaDSys    ·   course.agentic-system.org 44
Contiguous caches cannot be shared, so n samples 
store the same prompt n times
Parallel sampling, n = 3, contiguous slabs
Sample 1 Prompt KV , copy 1 Output 1
Sample 2 Prompt KV , copy 2 Output 2
Sample 3 Prompt KV , copy 3 Output 3
Parallel sampling: n replies to one 
prompt copy the prompt n times
Beam search: beams share the 
prompt and a prefix that shifts 
every step; a fork copies the whole 
slab
Shared system prompt: every 
user request repeats the same 
instructions
PagedAttention

45Harvard MaDSys    ·   course.agentic-system.org 45
PagedAttention manages the KV cache like OS paging
Request A: logical blocks Block table Physical KV blocks in GPU
One slot per token (OS: byte) physical # filled
0 The cat sat on 4 4
1 the mat and then 1 4
2 it slept 3 2
row = logical block
0 Hi all
1 the mat and then
2
3 it slept
4 The cat sat on
5
Demand paging
New block only when the last 
one fills
Shared pages, copy-on-write
Shared prompt blocks with 
reference counts
Swap to disk
Swap blocks to CPU memory
One level of indirection removes the need for contiguous memory .
Source: Kwon et al., PagedAttention and vLLM, SOSP 2023, Fig. 6. Blocks hold 16 tokens; 4 shown.
PagedAttention

46Harvard MaDSys    ·   course.agentic-system.org 46
Prefix cache

47Harvard MaDSys    ·   course.agentic-system.org 47
Prefix cache: reuse the KV of a prefix the server has 
already computed
Prefix cache
Three chat requests share one system prompt
Req 1 System prompt: prefill Q1
Req 2 System prompt: cache hit Q2
Req 3 System prompt: cache hit Q3
Prefill work, 1,000-token prompt + 50-token question
No cache: 3 × 1,050 = 3,150 tokens
Prefix cache: 1,050 + 50 + 50 = 1,150 tokens
Where shared prefixes come 
from
System prompts: every request 
repeats the same instructions
Multi-turn chat: each turn 
resends the history
Agents: each step resends tools 
and the trace so far
Exact match only: a token's KV depends on every token before it.

48Harvard MaDSys    ·   course.agentic-system.org 48
Block hashing: find cached KV blocks by a hash of 
the whole prefix
Source: vLLM documentation, Automatic Prefix Caching design, 2024
Prefix cache
One prompt, 4 tokens per block (vLLM uses 16)
You are a helpful
h0 = H(∅, B0)
Hit: block 7
assistant who
h1 = H(h0, B1)
Hit: block 2
answers in French
h2 = H(h1, B2)
Miss: compute
Each hash folds in its parent, so h2 considers all 12 tokens, not 
just the last 4.
Lookup: hash each full block of a 
new prompt; stop at the first miss
Sharing: a hit raises the block's 
reference count; nothing is 
copied
Eviction: unreferenced blocks 
stay cached until memory is 
needed, then go in LRU order
Granularity: a partly filled last 
block is never shared
A hash table on top of PagedAttention turns shared blocks into a cache.

49Harvard MaDSys    ·   course.agentic-system.org 49
SGLang RadixAttention: keep every request's KV in a 
radix tree and share its prefixes
Source: Zheng et al., SGLang, NeurIPS 2024, Sec. 3 and Fig. 3
Prefix cache
One tree holds the KV of every cached request
root
System prompt
Few-shot set
Chat A, turn 1
Chat B, turn 1
Query 1
Query 2
Query 3
Turn 2
LRU evicted
Arrive: match the longest prefix 
in the tree; prefill only the rest
Finish: insert the new tokens as a 
branch; the KV stays on the GPU
Evict: drop least-recently-used 
leaves no running request uses
Branches share their parent's KV , so a common prefix is stored once.

51Harvard MaDSys    ·   course.agentic-system.org 51
Check your understanding: prefix caching
Q1. Two prompts differ only at token 3 of 1,000. How much KV can they share?
Answer: Two tokens at most, and none with 16-token block hashing: each token's KV depends on all tokens before 
it.
Q2. Why does maximizing prefix-cache hits conflict with fair scheduling?
Answer: Serving the client with the hottest cache first can starve others.
Q3. A cached prefix ends mid-block. Which index can still reuse it: block hash or radix tree?
Answer: The radix tree, which matches at token granularity; block hashing reuses only full blocks.
Prefix cache

53Harvard MaDSys    ·   course.agentic-system.org 53
Parallelism: one model, many GPUs
Data parallelism (DP)
Tensor parallelism (TP)
Pipeline parallelism (PP)
Expert parallelism (EP)
Sequence parallelism (SP)

54Harvard MaDSys    ·   course.agentic-system.org 54
Why one GPU is not enough
• Weights alone outgrow a single GPU; KV 
cache competes for the same HBM
• One GPU's bandwidth caps decode 
speed
• Parallelism buys capacity and speed
a 70B model in bf16
weights 140 GB, one GPU holds 141 GB
shard it across 4 GPUs
GPU 0 GPU 1 GPU 2 GPU 3
35 GB of weights each, plus room for KV
Back-of-envelope
ttoken ≥ 2N ÷ BWHBM
70B bf16 on H200: 140 GB ÷ 4.8 TB/s ≈ 29 ms
Parallelism

55Harvard MaDSys    ·   course.agentic-system.org 55
Collectives: send/recv, broadcast, all-gather
Color = GPU that produced the data; 
number = slice; M = size of A, W, or 0–3
Before After
G0 G1 G2 G3 G0 G1 G2 G3
Send / recv
One GPU sends a buffer to one peer
Used by: PP stage hops, SP ring
A A A
Broadcast
One GPU copies its buffer to all
Used by: batch inputs to TP ranks
W W W W W
All-gather
Each adds a shard; all get the whole
Used by: TP outputs, SP K/V
0 1 2 3
0
1
2
3
0
1
2
3
0
1
2
3
0
1
2
3
Cost
per GPU
M
M
0.75 M
Parallelism

56Harvard MaDSys    ·   course.agentic-system.org 56
Collectives: reduce-scatter, all-reduce, all-to-all
Color = source GPU; number = slice
Gray Σ = sum over GPUs; M = all 4 slices
Before After
G0 G1 G2 G3 G0 G1 G2 G3
Reduce-scatter
Sum across GPUs; each keeps one slice
Used by: TP with sequence parallelism
0
1
2
3
0
1
2
3
0
1
2
3
0
1
2
3
Σ0 Σ1 Σ2 Σ3
All-reduce
Sum across GPUs; every GPU keeps all
= reduce-scatter + all-gather
Used by: TP after row-parallel layers
0
1
2
3
0
1
2
3
0
1
2
3
0
1
2
3
Σ0
Σ1
Σ2
Σ3
Σ0
Σ1
Σ2
Σ3
Σ0
Σ1
Σ2
Σ3
Σ0
Σ1
Σ2
Σ3
All-to-all
GPU i sends slice j to GPU j
Used by: EP token dispatch and combine
0
1
2
3
0
1
2
3
0
1
2
3
0
1
2
3
0
0
0
0
1
1
1
1
2
2
2
2
3
3
3
3
Cost
per GPU
0.75 M
1.5 M
0.75 M
Parallelism

57Harvard MaDSys    ·   course.agentic-system.org 57
Data parallelism: more replicas
• Every GPU holds the whole model
• Requests are split across replicas
• Scales throughput
• Each replica keeps its own scheduler 
and KV cache
incoming requests
router splits the stream
replica 0
full model + own KV
replica 1
full model + own KV
2× throughput, same max model size
Back-of-envelope
Throughput ≈ G × Θ₁
G replicas; memory per GPU stays 2N + KV
Comm: 0, replicas never talk
Matrix view
X₀ × W = Y₀ GPU 0 X₁ × W = Y₁ GPU 1
X₂ × W = Y₂ GPU 2 X₃ × W = Y₃ GPU 3
Same W on every GPU; the batch splits by rows
Parallelism

59Harvard MaDSys    ·   course.agentic-system.org 59
Tensor parallelism: split within a layer
• Each layer's matrices are sliced across 
GPUs
• Every GPU computes part of every layer
• An all-reduce joins the slices each 
block
• Needs NVLink-class bandwidth, so 
keep it inside one node
one transformer layer, four GPUs
shard 0 shard 1 shard 2 shard 3
all-reduce after every block
repeated for all L layers
more GPUs means more communication
Back-of-envelope
Weights per GPU = 2N ÷ G
70B at G = 4 GPUs → 35 GB each
Comm per GPU: 2 × 1.5 × 2bh bytes per layer
Parallelism

61Harvard MaDSys    ·   course.agentic-system.org 61
Column-parallel linear: split W by columns, so each 
GPU owns whole output columns
Each GPU holds a vertical slice of W and a full copy of X, so it computes its own output 
columns with no communication.
X
b × h, on all GPUs
× W₀ W₁ W₂ W₃
h × f/G each
= Y₀ Y₁ Y₂ Y₃
b × f/G each
GPU 0:  Y₀ = X · W₀
GPU 1:  Y₁ = X · W₁
GPU 2:  Y₂ = X · W₂
GPU 3:  Y₃ = X · W₃
b tokens, h hidden, f output width
Communication
None inside the layer. Add an all-gather only if the next step needs the full Y .
Shoeybi et al., Megatron-LM, arXiv 1909.08053, 2019
Parallelism

62Harvard MaDSys    ·   course.agentic-system.org 62
Row-parallel linear: split W by rows, so each GPU 
holds a partial sum to all-reduce
Each GPU holds a horizontal slice of W and the matching columns of X. Its product is full size 
but only part of the answer.
X₀ X₁ X₂ X₃
b × h/G each
×
W₀
W₁
W₂
W₃
h/G × h each
= Z₀ + Z₁ + Z₂ + Z₃
partial sums, b × h each
all-reduce
Z
Z = Σ Zᵢ
b tokens, h hidden size; GPU i computes Zᵢ = Xᵢ · Wᵢ
Communication
One all-reduce of the b × h output (2bh bytes in bf16); each GPU sends 2(G − 1)/G × 2bh = 3bh at G = 4
Shoeybi et al., Megatron-LM, arXiv 1909.08053, 2019
Parallelism

63Harvard MaDSys    ·   course.agentic-system.org 63
Megatron TP block: column-parallel then 
row-parallel, one all-reduce per block
The column-parallel layer's output shards are exactly the input the row-parallel layer needs, so 
GPUs only talk once, at the end.
MLP
X Up + gate
column-parallel
Activation
local, no comm
Down proj
row-parallel
All-reduce
sum partials
Attention
X Q, K, V proj
column, 1/G heads
Attention
local, per head
Output proj
row-parallel
All-reduce
sum partials
Shoeybi et al., Megatron-LM, arXiv 1909.08053, 2019
Parallelism

64Harvard MaDSys    ·   course.agentic-system.org 64
Pipeline parallelism: split the layers
• Layers are cut into consecutive stages
• Each GPU owns a contiguous block of 
layers
• Micro-batches keep every stage busy
• Tolerates slower links, so it can span 
nodes
80 layers cut into 4 stages
L1–20 L21–40 L41–60 L61–80
Back-of-envelope
Bubble = (G − 1) ÷ (m + G − 1)
G = GPUs (stages), m = micro-batches
G = 4: m = 4 → 43%, m = 16 → 16%
Comm: one send of 2bh bytes per stage hop
forward pass: 4 micro-batches, 4 stages
G0 1 2 3 4
G1 1 2 3 4
G2 1 2 3 4
G3 1 2 3 4
time steps 1–7 →
Grey = bubble: 12 of 28 slots idle = 3/7 ≈ 43%
Parallelism

66Harvard MaDSys    ·   course.agentic-system.org 66
Expert parallelism: split the experts
• An MoE layer holds many experts; each 
token uses a few
• Experts are spread across GPUs
• An all-to-all ships tokens to their experts
• Uneven routing leaves some GPUs idle
8 experts spread over 4 GPUs
GPU 0
E0 E1
GPU 1
E2 E3
GPU 2
E4 E5
GPU 3
E6 E7
Back-of-envelope
Load per GPU ≈ k × b ÷ G
top-2, 1,024 tokens, 4 GPUs → 512 each
Comm per GPU: 2 × 0.75 × 2kbh bytes per layer
t token t → E3 and E7 (k = 2)
1 Dispatch: send t to its k experts
2 Compute: each expert runs locally
3 Combine: send results back, sum
All GPUs do this at once: all-to-all
Parallelism

68Harvard MaDSys    ·   course.agentic-system.org 68
Context parallelism: split the tokens
• Long prompts overflow one GPU
• Each GPU holds a block of tokens
• Ring attention passes K/V blocks
• Helps prefill, not decode
a 128K-token prompt over 4 GPUs
GPU 0
0–32K
GPU 1
32–64K
GPU 2
64–96K
GPU 3
96–128K
passes K/V blocks to the next GPU
every query still sees every key
transfers overlap with attention compute
Back-of-envelope
Tokens per GPU = s ÷ G
128K-token prompt, G = 4 → 32K tokens each
Comm: G − 1 K/V block passes per layer
Parallelism

70Harvard MaDSys    ·   course.agentic-system.org 70
TP and EP move 240× more bytes per token than PP
Strategy Collective How often Bytes / token / GPU
Data none never 0
Tensor (G = 4) all-reduce 2 per layer 3.9 MB
Pipeline (G = 4) send / recv 1 per stage hop 16 KB
Expert (G = 4, top-2) all-to-all 2 per MoE layer ≈ 3.9 MB
70B-shape model: h = 8,192, 80 layers, bf16, decoding one token.
Ring all-reduce moves 2(G − 1)/G of the data; MoE in every layer, 3 of 4 experts remote.
Parallelism

71Harvard MaDSys    ·   course.agentic-system.org 71
TP and EP need NVLink
Link bandwidth per GPU, GB/s per direction
H100 SXM: NVLink 4 (900 GB/s bidirectional), PCIe Gen5 x16, InfiniBand NDR 400 Gb/s
Cost of one transfer
t = bytes ÷ BW + hops × latency
Tensor traffic, 3.9 MB/token/GPU
NVLink ≈ 9 µs; InfiniBand ≈ 78 µs, plus 
overhead
Rule of thumb
TP inside a node; PP across nodes
50 GB/s
64 GB/s
450 GB/s  
InfiniBand NDR
PCIe Gen5 x16
NVLink 4
Parallelism

73Harvard MaDSys    ·   course.agentic-system.org 73
Check your understanding: parallelism
Q1. A 70B bf16 model on one node of 4 H200s (140 GB each). Which split first, and why?
Answer: TP = 4 over NVLink or DP2 + TP2 depends on context size. 
Q2. You add a second node. What parallelism to use? 
Answer: PP across nodes: one 2h-byte hop per token, while TP all-reduces every layer , about 240× more traffic.
Q3. Why can DP attention + EP outperform TP on long context but underperform on short ones?
Answer: Long: TP replicates KV when KV heads < ranks, while DP supports larger batches. Short: all -to-all overhead 
dominates.
Parallelism

74Harvard MaDSys    ·   course.agentic-system.org 74
Parallelism: what to take away
Data parallelism scales throughput
G replicas serve G× the requests, but every 
replica must hold the whole model
Tensor parallelism cuts per-token 
latency
Each GPU reads 1/G of the weights, at the cost 
of all-reduces every layer; keep it inside an 
NVLink node
Pipeline and sequence parallelism 
add capacity
Pipelines span nodes with light traffic but add 
bubbles; sequence parallelism splits very long 
prompts
Expert parallelism serves MoE 
models
Experts spread across GPUs; all-to-all traffic 
and expert load imbalance are the costs
Parallelism

75Harvard MaDSys    ·   course.agentic-system.org 75
Next class: speculative decoding
Today in brief
Measurement: TTFT and TBT percentiles, goodput
Batching: continuous, selective
Scheduling: request scheduling, chunked prefill, disaggregation
Memory management: paged, shared KV cache
Parallelism: DP , TP , PP , EP , SP

76Harvard MaDSys    ·   course.agentic-system.org 76
Optional reading

77Harvard MaDSys    ·   course.agentic-system.org 77
Optional reading: the papers behind each section
Evaluation
Agrawal et al., On Evaluating Performance of LLM 
Inference Systems, arXiv 2025
Batching and scheduling
Yu et al., Orca, OSDI 2022
Agrawal et al., Sarathi-Serve, OSDI 2024
Sheng et al., Fairness in Serving LLMs, OSDI 2024
PD disaggregation
Zhong et al., DistServe, OSDI 2024
KV-cache memory
Kwon et al., PagedAttention and vLLM, SOSP 2023
Zheng et al., SGLang, NeurIPS 2024
Parallelism
Shoeybi et al., Megatron-LM, arXiv 2019
Korthikanti et al., Reducing Activation 
Recomputation, MLSys 2023
Thakur, Rabenseifner and Gropp, Collective 
Operations in MPICH, IJHPCA 2005
