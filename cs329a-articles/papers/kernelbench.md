---
title: "KernelBench: Can LLMs Write Efficient GPU Kernels?"
arxiv: 2502.10517
source: https://arxiv.org/abs/2502.10517
crawled: 2026-09-23
---

# KernelBench: Can LLMs Write Efficient GPU Kernels? ††footnotetext: *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu

Anne Ouyang
Affiliation: Stanford University
  
Simon Guo
Affiliation: Stanford University
  
Simran Arora
Affiliation: Stanford University
  
Alex L. Zhang
Affiliation: Princeton University
  
William Hu
Affiliation: Stanford University
  
Christopher Ré
Affiliation: Stanford University
  
Azalia Mirhoseini
Affiliation: Stanford University

###### Abstract

Efficient GPU kernels are crucial for building performant machine learning architectures, but writing them is a time-consuming challenge that requires significant expertise; therefore, we explore using language models (LMs) to automate kernel generation. We introduce KernelBench, an open-source framework for evaluating LMs’ ability to write fast and correct kernels on a suite of 250 carefully selected PyTorch ML workloads. KernelBench represents a real-world engineering environment and making progress on the introduced benchmark directly translates to faster practical kernels. We introduce a new evaluation metric fastp\text{fast}_{p}, which measures the percentage of generated kernels that are functionally correct and offer a speedup greater than an adjustable threshold pp over baseline. Our experiments across various state-of-the-art models and test-time methods show that frontier reasoning models perform the best out of the box but still fall short overall, matching the PyTorch baseline in less than 20% of the cases. While we show that results can improve by leveraging execution and profiling feedback during iterative refinement, KernelBench remains a challenging benchmark, with its difficulty increasing as we raise speedup threshold pp.

## 1 Introduction

AI relies on efficient GPU kernels to achieve high performance and cost and energy savings; however, developing kernels remains challenging.
There has been a Cambrian explosion of ML architectures [[33](#bib.bib33), [29](#bib.bib29), [7](#bib.bib7)], but their available implementations routinely underperform their peak potential. We are seeing a proliferation of AI hardware  [[24](#bib.bib24), [25](#bib.bib25), [26](#bib.bib26), [14](#bib.bib14), [11](#bib.bib11), [4](#bib.bib4), [10](#bib.bib10)], each with different specs and instruction sets, and porting algorithms across platforms is a pain point. A key example is the FlashAttention kernel [[8](#bib.bib8)], which is
crucial for running modern Transformer models –– the initial kernel released in 2022, five years after the Transformer was proposed; it took two more years from the release of NVIDIA Hopper GPUs to transfer the algorithm to the new hardware platform. We explore the question: Can language models help write correct and optimized kernels?

![Refer to caption](2502.10517v1/figures/KernelBench-Flow-HD.png)

Figure 1: KernelBench evaluates LMs’ ability to generate performant GPU Kernels. Overview of tasks in KernelBench: KernelBench tasks LMs with generating optimized CUDA kernels for a given target PyTorch model architecture and conducts automated evaluation

AI engineers use a rich set of information when developing kernels and it is not clear whether language models (LMs) can mimic the workflow. They use compiler feedback, profiling metrics, hardware-specific specs and instruction sets, and knowledge of hardware-efficiency techniques (e.g., tiling, fusion). They can use programming tools ranging from assembly (e.g., PTX as in  [DeepSeek-AI [9]](#bib.bib9)) to higher-level libraries (ThunderKittens [[32](#bib.bib32)], Triton [[36](#bib.bib36)]). Compared to existing LM code generation workloads [[43](#bib.bib43)], kernel writing requires a massive amount and diversity of information. We first design an environment that reflects the typical AI engineer’s workflow and supports providing LMs with this rich information. The environment should:

- •

  Automate the AI engineer’s workflow. The model should have full flexibility to decide which operators to optimize and how to optimize them.
- •

  Support a diverse set of AI algorithms, programming languages, and hardware platforms.
- •

  Make it easy to evaluate both performance and functional correctness of LM generations, ideally in a programmatic way. It should also capture profiling and execution information from generated kernels.

We introduce KernelBench to generate and evaluate kernels, which addresses the above considerations. KernelBench tests LM optimizations on three levels of AI workloads:

1. 1.

   Individual operations: We include various AI operators, including matrix multiplies, convolutions, activations, norms, and losses. While PyTorch already uses expert-optimized closed-source kernels, making this a potentially challenging baseline, it is valuable if LMs can generate open-source kernels for the operations.
2. 2.

   Sequence of operations: We provide problems that contain 3-6 individual operations together (e.g. a mainloop operator like matmul followed by pointwise operators like ReLU and Bias). This enables evaluating the models’ ability to fuse multiple operators.
3. 3.

   End-to-end architectures: We select architectures from popular AI repositories on Github including pytorch, huggingface/transformers, and huggingface/pytorch-image-models. These architectures contain many operations.

Mimicking an AI researcher’s workflow, the LM takes PyTorch reference code as input and outputs an optimized version of the code.
Similar to the human kernel development process, our environment enables the LM to iterate with compiler and profiler feedback to refine performance. The LM is free to use any programming language and decide both which parts of the PyTorch code to optimize, and how to optimize them. Our pipeline allows us to feed diverse information to the LMs, including hardware-specific information, example kernels, and compiler/profiler feedback.

We observe that frontier and open-source models perform poorly out-of-the-box on KernelBench, with OpenAI-o1 and DeepSeek-R1 matching the PyTorch Eager baseline on <20%<20\% of the tasks. These model-generated kernels greatly suffer from execution errors, functional correctness issues, and are unable to perform platform-specific optimizations. To identify areas for improvement, we conduct a series of experiments and analysis, and find that:

1. 1.

   Writing functionally correct kernels remains challenging for models: while models are able to fix execution failures through either reasoning or multiple attempts, they struggle to produce functionally correct code. Furthermore, we observe a trade-off between LMs attempting more complex optimizations / niche hardware instructions (e.g., tensor core wmma) and producing error-free kernels. We hypothesize this is due to CUDA being a low-resource language in open-source training data, only 0.073%0.073\% of popular code corpus The Stack v1.2 [[18](#bib.bib18), [16](#bib.bib16)].
2. 2.

   Models demonstrate potential to produce performant kernels via optimizations: We observe a few instances where LMs make algorithmic improvements – e.g., exploiting sparsity, operator fusion, and utilizing hardware features. We notice more of such instances when we explicitly condition the LM on hardware information (e.g., bandwidth and TFLOP specs) and demonstrations of hardware optimization techniques (e.g., tiling, fusion). While these capabilities remain nascent, LMs do demonstrate potential for generating performant kernels.
3. 3.

   Leveraging feedback is important for reducing execution errors and discovering faster solutions: By providing execution results and profiler feedback to the LM in context, the kernel quality significantly improves after multiple refinements from 12%12\%, 36%36\%, and 12%12\% in fast1\text{fast}_{1} to 43%43\%, 72%72\%, and 18%18\% respectively.

Our findings highlight the technical challenges we need to solve in order to adopt LMs for kernel writing. These include but are not limited to: how to improve LM performance in a low-resource data regime, and how to select from the rich set of information we can provide to models. To address these challenges, we contribute (1) an open-source framework to study LM kernel generation with a comprehensive suite of evaluation problems and (2) analysis of where current LMs stand and how to realize a future of efficient kernels generated by models.

## 2 Related Works

Kernel libraries and compilers. We evaluate existing approaches for kernel programming along the dimensions of automation, breadth, and performance. Mainstream kernel programming libraries like cuDNN  [[22](#bib.bib22)], CUTLASS [[23](#bib.bib23)], and Apple MLX [[1](#bib.bib1)] are hardware-specific and demand substantial engineering effort from human experts. Other libraries, like ThunderKittens [[32](#bib.bib32)] and Triton [[36](#bib.bib36)], successfully help AI researchers write a breadth of fast and correct kernels [[2](#bib.bib2), [45](#bib.bib45)], but still require human programming effort. Compiler-based tools, like torch.compile [[28](#bib.bib28)] and FlexAttention [[34](#bib.bib34)], automatically provide a narrow slice of optimizations. In contrast to these efforts, we ask if LMs can automatically generate performant kernels for a breadth of AI workloads.
  
  
LLMs for performance-optimized code generation. In the past year, there have been several efforts to build LMs that can automate algorithmic coding [[5](#bib.bib5), [31](#bib.bib31), [19](#bib.bib19)], resolving GitHub issues [[43](#bib.bib43), [44](#bib.bib44)], and domain-specific coding [[46](#bib.bib46), [17](#bib.bib17)]. While these works focus on producing correct and functional code, subsequent works have explored LMs’ ability to produce solutions with better algorithmic and asymptotic efficiency  [[21](#bib.bib21), [40](#bib.bib40)]. KernelBench focuses on wall-clock efficiency. LMs generate high-performance computing (HPC) code, which requires an understanding of the underlying hardware features and device instruction set, and common performance characteristics of parallel processors.

Existing works in the space of HPC code generation have evaluated LM performance on translating arbitrary code samples from C++ to CUDA [[35](#bib.bib35), [41](#bib.bib41)] or generating well-known, low-level kernels such as GEMMs [[38](#bib.bib38), [42](#bib.bib42)]. KernelBench instead curates a set of 250 diverse kernels from real-world, modern deep learning workloads, many of which do not have existing human-written implementations — in other words, solving KernelBench tasks are immediately beneficial for real deep learning workloads.

## 3 KernelBench: A Framework for AI Kernel Generation

KernelBench is a new framework for evaluating the ability of language models to generate performant kernels for a breadth of AI workloads. In this section, we describe the task format, contents, and evaluation metric.

### 3.1 KernelBench Task Format

KernelBench contains 250 tasks representing a range of AI workloads, and is easily extensible to new workloads. The end-to-end specification for a task is illustrated in [Figure 1](#S1.F1 "Figure 1 ‣ 1 Introduction ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu") and described below.
  
  
Task input: Given an AI workload, the input to the task is a reference implementation written in PyTorch. Mimicking an AI researcher’s workflow, the PyTorch code contains a class named Model derived from torch.nn.Module(), where the standard __init__ and forward() functions (and any helper functions) are populated with the AI workload’s PyTorch operations.

AI algorithms generally operate on large tensors of data. The optimal kernel for a workload depends on the size and data type (e.g., BF16, FP8) of the tensor. Therefore, each task additionally contains functions get_inputs() and get_init_inputs(), which specify the exact input tensors that the kernel needs to handle.
  
  
Task output: Given the input, the LM needs to output a new class named ModelNew derived from torch.nn.Module(), which contains custom optimizations. For example, the LM can incorporate in-line kernel calls during the forward() function using the CUDA-C extension in PyTorch.

In order to succeed, the LM needs to identify (1) which operations in the Model class would benefit most from optimizations, and (2) how to optimize those operations. The LM can use any hardware-efficiency techniques such as fusion and tiling or specialized instructions (e.g., tensor cores) and any programming library (e.g., PTX, CUDA, CUTLASS, Triton, ThunderKittens).

### 3.2 Task Selection

The 250 tasks in KernelBench are partitioned into three levels, based on the number of primitive operations, or PyTorch library functions, they contain:

- •

  Level 1 (100 tasks): Single primitive operation. This level includes the foundational building blocks of AI (e.g. convolutions, matrix-vector and matrix-matrix multiplications, losses, activations, and layer normalizations).

  Since PyTorch makes calls to several well-optimized and often closed-source kernels under-the-hood, it can be challenging for LMs to outperform the baseline for these primitive operations. However, if an LM succeeds, the open-source kernels could be an impactful alternative to the closed-source (e.g., CuBLAS [[27](#bib.bib27)]) kernels.
- •

  Level 2 (100 tasks): Operator sequences. This level includes AI workloads containing multiple primitive operations, which can be fused into a single kernel for improved performance (e.g., a combination of a convolution, ReLU, and bias).

  Since compiler-based tools such as the PyTorch compiler are effective at fusion, it can be challenging for LMs to outperform them. However, LMs may propose more complex algorithms compared to compiler rules.
- •

  Level 3 (50 tasks): Full ML architectures. This level includes architectures that power popular AI models, such as AlexNet and MiniGPT, collected from popular PyTorch repositories on GitHub.

  Given the scale of modern models, it is critical to use kernels when running training and inference. Unfortunately, it has been difficult for the AI community to generate performant kernels. For instance, it took 5 years from the release of the Transformer architecture [[39](#bib.bib39)] to obtain performant kernels [[8](#bib.bib8)], let alone today’s many new architectures. Peak performance kernels for these architectures require algorithmic modifications that are often beyond the scope of a compiler.

We reiterate that each task contains a meaningful set of AI primitive operations or architectures, such that LM success on the task can directly lead to real world impact.

### 3.3 Metric Design

We describe the evaluation approach for KernelBench and how we compare the success of different LMs.

##### Evaluation approach

KernelBench is an evaluation-only benchmark. We do not provide ground truth kernels for the tasks since we imagine users benchmarking on a variety of hardware platforms (including new platforms), input types, and workloads. However, by design, KernelBench is automatically verifiable. Given a task, we randomly generate input tensors of the prescribed shape and precision and collect the PyTorch Model output. We can evaluate whether LM generations are correct and fast as follows:

1. 1.

   Correctness
   We compare the Model output to the LM-generated ModelNew output.
   We evaluate on 5 random inputs per problem (detailed in Appendix [B](#A2 "Appendix B Evaluation Methodology and Baselines ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu")).
2. 2.

   Performance We compare the wall-clock execution time of Model against ModelNew using repeated trials to account for timing variations.

##### Comparing LMs on KernelBench

Some LMs may generate a small number of correct kernels that are very fast, while other LMs generate a large number of correct kernels that are quite slow. Here, we explain our proposed unified metric for ranking LM quality on KernelBench.

To capture both axes of correctness and performance, we introduce a new metric called fastp\text{fast}_{p}, which is defined as the fraction of tasks that are both correct and have a speedup (computed as the ratio of PyTorch wall-clock time to generated kernel time) greater than threshold pp. Formally:

|  |  |  |
| --- | --- | --- |
|  | fastp=1N∑i=1N𝟙(correcti∧{speedupi>p}),\displaystyle\text{fast}_{p}=\frac{1}{N}\sum_{i=1}^{N}\mathbbm{1}(\text{correct}_{i}\land\left\{\text{speedup}_{i}>p\right\}),\vskip-7.22743pt |  |

where fast0\text{fast}_{0} is equivalent to the LM’s correctness rate, as it measures the fraction of tasks for which the LM code is functionally correct regardless of its speed.

By adjusting the threshold parameter pp, we enable evaluation of kernel performance at different speedup thresholds and capture the speedup distributions. For our evaluations, we focus on p=1p=1 as a starting point, with the possibility of increasing pp as future methods for kernel generation improve. Additionally, using p<1p<1 for training is valuable, since PyTorch relies on complex optimized kernels, and matching even a fraction of their performance is still considered beneficial.

## 4 KernelBench Baseline Evaluation

In this section, we investigate how a range of LMs perform when evaluated off-the-shelf on KernelBench and explore their capabilities and failure modes.

### 4.1 One-shot Baseline

We evaluate LMs using a prompt that contains one example of a PyTorch Model input and ModelNew output, highlighting the task format. The example is simple, containing only an add operator
(See Appendix [C.1](#A3.SS1 "C.1 One-shot Baseline Prompt ‣ Appendix C Experiment Prompting Details ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu")). Given this in-context example and the PyTorch task Model to optimize, the LM generates ModelNew via greedy decoding. We profile the generated code on an NVIDIA L40S GPU, and measure the fastp\text{fast}_{p} metric across all problems. Table [3](#S4.F3 "Figure 3 ‣ 4.1 One-shot Baseline ‣ 4 KernelBench Baseline Evaluation ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu") shows that the LM-generated kernels achieves a speedup over PyTorch Eager in fewer than 20% of tasks on average.

|  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- |
| fast1\text{fast}_{1} over: | PyTorch Eager | | | torch.compile | | |
| KernelBench Level | 1 | 2 | 3 | 1 | 2 | 3 |
| GPT-4o | 4% | 5% | 0% | 18% | 4% | 4% |
| OpenAI o1 | 10% | 24% | 12% | 28% | 19% | 4% |
| DeepSeek V3 | 6% | 4% | 8% | 20% | 2% | 2% |
| DeepSeek R1 | 12% | 36% | 2% | 38% | 37% | 2% |
| Claude 3.5 Sonnet | 10% | 7% | 2% | 29% | 2% | 2% |
| Llama 3.1-70B Inst. | 3% | 0% | 0% | 11% | 0% | 0% |
| Llama 3.1-405B Inst. | 3% | 0% | 2% | 16% | 0% | 0% |

Figure 2: KernelBench is a challenging benchmark for current LMs. Here we present fast1\text{fast}_{1}, i.e. the percentage of problems where the model-generated kernel is faster than the PyTorch Eager and torch.compile baseline (default configuration) on NVIDIA L40S.

![Refer to caption](2502.10517v1/figures/error_breakdown.png)

Figure 3: We categorize failure modes of kernel code into execution failure and functional correctness. For the one-shot baseline, reasoning models generate fewer kernels with execution failures, but all models struggle similarly with functional correctness.

††footnotetext: The torch.compile baseline runtime is sometimes slower than Torch Eager – this is due to reproducible runtime overhead (not compile time) that could be significant for small kernels in Level 1. We focus on PyTorch Eager for the rest of our analysis, but we elaborate on other baselines in Appendix [B](#A2 "Appendix B Evaluation Methodology and Baselines ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu").

### 4.2 Correctness: Error Analysis

In Figure [3](#S4.F3 "Figure 3 ‣ 4.1 One-shot Baseline ‣ 4 KernelBench Baseline Evaluation ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu"), we analyze the failure modes of LMs across problems. It can be seen that a large proportion of model-generated kernels are incorrect. To better understand where model-generated kernels fail, we break down their correctness issues into execution failures (CUDA/nvcc / Python compile-time errors, CUDA memory violations, and runtime errors) and correctness errors (output tensor shape and value mismatches). We observe that the reasoning LMs (o1, R1) produce fewer incorrect solutions (<55%<55\%) than other models (>70%>70\%). However, we find this is mainly because they make fewer execution failures. All LMs struggle with functional correctness to a similar degree.

### 4.3 Performance: Speedup Distribution

A key point of interest is whether the functionally correct LM-generated kernels outperform the PyTorch baseline. Figure [4](#S4.F4 "Figure 4 ‣ 4.3 Performance: Speedup Distribution ‣ 4 KernelBench Baseline Evaluation ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu") shows the distribution of fastp\text{fast}_{p} as pp varies, indicating the percentage of kernels that are pp-times faster than the PyTorch Eager baseline (the top right of the plot is better). At p=1p=1, fewer than 15% of LM-generated kernels outperform PyTorch across all KernelBench levels. Reasoning-based LMs generally outperform the other LMs in providing speedups.

![Refer to caption](2502.10517v1/figures/greedy_fastp.png)

Figure 4: Most LM-generated kernels are slow. This figure shows the distribution of the fastp\text{fast}_{p} metric as the speedup threshold pp (over PyTorch baseline) increases. fast0\text{fast}_{0} represents the number of correct kernels regardless of speed, and fast1\text{fast}_{1} represents the number of correct kernels achieving at least >1×>1\times speedup over PyTorch. Increasing the threshold pp increases the difficulty.

### 4.4 Performance Variations across Hardware

Our one-shot baseline makes no assumptions about the underlying hardware, so a natural question is how our analysis of the LM-generated kernels generalizes across various GPU types. Table [13](#A7.T13 "Table 13 ‣ G.1 Evaluation across different hardware ‣ Appendix G Cross-Hardware Case Study ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu") and Figure [9](#A7.F9 "Figure 9 ‣ G.1 Evaluation across different hardware ‣ Appendix G Cross-Hardware Case Study ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu") show that kernels outperforming PyTorch Eager on NVIDIA L40S in Level 1 achieve similar speedups versus the baselines on other GPUs. However, on problems in Level 2, LMs exhibit larger variations in speedups across GPUs (Figure [10](#A7.F10 "Figure 10 ‣ G.1 Evaluation across different hardware ‣ Appendix G Cross-Hardware Case Study ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu")): DeepSeek R1-generated kernels achieve a fast1\text{fast}_{1} of 36% on NVIDIA L40S but 47% on NVIDIA A10G for Level 2. This suggests that one-shot LM-generated kernels may not generalize well across hardware.
To generate target-specific kernels, we explore in Section [5.2](#S5.SS2 "5.2 Case Study: Generating Hardware-Efficient Kernels via Hardware Knowledge ‣ 5 Analysis of Model Capabilities ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu") whether providing hardware-specific details in-context could help.

Our analysis reveals that the best models available today struggle to generate correct kernels that outperform the baseline PyTorch speeds. LM-generated kernels frequently fail due to simple compiler and run-time errors. Furthermore, it is difficult for LMs to write kernels that perform well across hardware platforms given simple instructions.

## 5 Analysis of Model Capabilities

In the last section, we found that KernelBench is a challenging benchmark for today’s models. In this section, we conduct case studies to explore opportunities for improvement in future models and AI systems.

### 5.1 Case Study: Leveraging the KernelBench Environment Feedback at Test-Time

As observed in Section [4.2](#S4.SS2 "4.2 Correctness: Error Analysis ‣ 4 KernelBench Baseline Evaluation ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu"), execution failures are the most frequent failure mode in LM-generated kernels. The environment provided by KernelBench allows us to collect rich signals, including compiler errors, correctness checks, and runtime profiling metrics, all of which can be fed back in to the LM to help it resolve kernel failures. To explore how well LMs can use this feedback, we evaluate and compare two baselines: (1) generating multiple parallel samples from the LM per KernelBench task and (2) sequentially generating kernels per KernelBench task by allowing the LM to iteratively refine using the execution feedback.

#### 5.1.1 Repeated Sampling

The KernelBench environment enables programmatic verification of LM-generated kernels,
allowing us to collect and evaluate multiple LM generations per task  [[3](#bib.bib3), [19](#bib.bib19), [12](#bib.bib12)]. We evaluate this repeated sampling approach using fastp​@​k\text{fast}_{p}@k, which measures the percentage of tasks where the model generated at least one functionally correct kernel that is pp times faster than PyTorch Eager when drawing kk samples.

Repeated sampling helps LMs discover more fast and correct solutions. Figure [5](#S5.F5.fig1 "Figure 5 ‣ 5.1.1 Repeated Sampling ‣ 5.1 Case Study: Leveraging the KernelBench Environment Feedback at Test-Time ‣ 5 Analysis of Model Capabilities ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu") shows that repeated sampling with high temperature improves fast1\text{fast}_{1} as kk increases across all three levels with both DeepSeek-V3 and Llama 3.1 70B. Notably, on Level 2, DeepSeek-V3 reaches a fast1\text{fast}_{1} of 37% with k=100k=100 samples, compared to just 4% in the one-shot baseline. Examining the samples, we find that high-temperature sampling helps explore the solution space, increasing the chances of generating error-free kernels with better optimizations. However, if a model has a very low inherent probability of solving a task, simply increasing the sampling budget has limited impact. For example, DeepSeek-V3 was never able to generate any correct solution for a group of 34 convolution variants in Level 1, even when attempting with 100 samples.

  

![Refer to caption](2502.10517v1/figures/monkey_fast1.png)

Figure 5: Repeated sampling helps discover more correct and performant kernels. As the number of repeated samples kk increases (up to 100), we observe that fast1\text{fast}_{1}@k improves for both DeepSeek-V3 and Llama 3.1-70B Instruct across all 3 KernelBench levels. We also observe a larger increase in correct solutions for Level 2 kernels.

#### 5.1.2 Iterative Refinement of Generations

The KernelBench environment is well-suited for collecting compiler feedback, execution errors, and timing analysis using tools like the PyTorch profiler as ground-truth signals. We investigate whether leveraging this feedback can help LMs to iteratively refine their generations.

![Refer to caption](2502.10517v1/figures/multi-turn-workflow.png)

Figure 6: The KernelBench framework enables models to receive and leverage feedback during iterative refinement. These ground-truth signals include NVCC compiler error messages, execution statistics (e.g. correctness checks and wall clock time), and the PyTorch profiler (operator timing breakdown).

We provide feedback to the model after each generation in a multi-turn process: after the initial generation, we provide the model with its previous generation GG, as well as compiler/execution feedback EE and/or profiler output PP over its current generation. We define each generation and subsequent feedback as a turn, and run this Iterative Refinement process over NN turns. For each turn, we measure fastp​@​N\text{fast}_{p}@N, which is the percentage of tasks where the model generated at least one functionally correct kernel that is pp times faster than PyTorch Eager by turn NN.

Leveraging execution feedback helps reduce errors and improves overall speedups over time. We examine the fast1\text{fast}_{1} behavior at turn N=10N=10 in Table [1](#S5.T1 "Table 1 ‣ 5.1.3 Comparing Repeated Sampling and Iterative Refinement ‣ 5.1 Case Study: Leveraging the KernelBench Environment Feedback at Test-Time ‣ 5 Analysis of Model Capabilities ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu") and find that iterative refinement consistently improves performance across models and levels of KernelBench. DeepSeek-R1 on Level 2 results in the most notable improvement, where the combination of execution feedback EE and profiler feedback PP boosts fast1\text{fast}_{1} from 36%36\% to 72%72\% (shown in Figure [7](#S5.F7.fig1 "Figure 7 ‣ 5.1.2 Iterative Refinement of Generations ‣ 5.1 Case Study: Leveraging the KernelBench Environment Feedback at Test-Time ‣ 5 Analysis of Model Capabilities ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu")).

Furthermore, by examining iterative refinement trajectories, we find that models self-correct more effectively with execution feedback EE, fixing issues especially related to execution errors. DeepSeek-R1 on Level 1 and 2 can generate a functional kernel on >90% of the tasks within 1010 turns of refinement (Table [8](#A5.T8 "Table 8 ‣ Appendix E Iterative Refinement on Correctness ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu")). However, the remaining incorrect kernels almost always fail due to functional incorrectness, likely because correctness feedback is less granular than execution failure messages. We include successful and failed examples of iterative refinement trajectories in Appendix [D.4](#A4.SS4 "D.4 Iterative Refinement Examples ‣ Appendix D Kernels of Interest ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu").

![Refer to caption](2502.10517v1/figures/multi-turn-trend-by-k.png)

Figure 7: Iterative refinement with execution feedback EE and profiling information PP enable models to improve kernel generations over turns, as shown in the fast1​@​N\text{fast}_{1}@N trajectory of DeepSeek-R1 on Level 2. The percentage of problems where the best generated kernel up to turn NN is correct and faster than PyTorch Eager consistently increases with the number of turns.

#### 5.1.3 Comparing Repeated Sampling and Iterative Refinement

|  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Method | Level 1 | | | Level 2 | | | Level 3 | | |
| Llama-3.1 | DeepSeek | Deepseek | Llama-3.1 | Deepseek | Deepseek | Llama-3.1 | Deepseek | Deepseek |
| 70B | V3 | R1 | 70B | V3 | R1 | 70B | V3 | R1 |
| Single Attempt (Baseline) | 3% | 6% | 12% | 0% | 4% | 36% | 0% | 8% | 2% |
| Repeated Sampling (@10) | 5% | 11% | N/A | 3% | 14% | N/A | 1% | 14% | N/A |
| Iterative Refinement w G | 9% | 9% | 18% | 0% | 7% | 44% | 0% | 14% | 4% |
| Iterative Refinement w G+E | 5% | 13% | 41% | 5% | 5% | 62% | 8% | 22% | 12% |
| Iterative Refinement w G+E+P | 7% | 19% | 43% | 4% | 6% | 72% | 2% | 14% | 18% |

Table 1: Both repeated sampling and iterative improvement enable models to generate more correct and fast kernels compared to baseline: Here we present the percentage of problems where the LM-generated kernel is correct and faster than baseline Torch Eager (Fast1\text{Fast}_{1} in %) for the two test-time methods, both with the same sample budget of 1010 calls. We further compare performance within iterative refinement achieved when leveraging previous Generation GG, Execution Result EE, and Timing Profiles PP. Note we do not repeatedly sample DeepSeek R1, as its API endpoint does not provide a temperature parameter.

In Table [1](#S5.T1 "Table 1 ‣ 5.1.3 Comparing Repeated Sampling and Iterative Refinement ‣ 5.1 Case Study: Leveraging the KernelBench Environment Feedback at Test-Time ‣ 5 Analysis of Model Capabilities ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu"), we compare repeated sampling and iterative refinement given a fixed budget of 1010 inference calls. Both methods provide meaningful improvements over the one-shot baseline, with iterative refinement being more effective in 5 of the 6 cases. However, ultimately we find that the effectiveness of the test-time methods is inherently dependent on the quality of the base model. For instance, with repeated sampling, DeepSeek-V3 consistently outperforms Llama-3.1 70B across all three levels. Similarly, with iterative refinement, DeepSeek-R1 consistently improves using feedback EE and PP, while DeepSeek-V3 and Llama-3.1 70B does not always benefit from having such information.

### 5.2 Case Study: Generating Hardware-Efficient Kernels via Hardware Knowledge

It is clear that LMs demonstrate limited success at generating hardware-efficient kernels. This is likely due to the scarcity of kernel code in the training data and the fact that the optimal kernel may need to change depending on the hardware platform-specific properties, as discussed in Section [4.4](#S4.SS4 "4.4 Performance Variations across Hardware ‣ 4 KernelBench Baseline Evaluation ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu"). In this case study, we explore providing 1) in-context examples of best-practices for kernel engineering and 2) in-context hardware specification details.

#### 5.2.1 Hardware-aware In-Context Examples

Well-written kernels often use techniques such as fusion, tiling, recompute, and asynchrony to maximize performance. We find that most of the one-shot generated kernels evaluated in [Section 4](#S4 "4 KernelBench Baseline Evaluation ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu") often do not use these techniques. Here, we explore whether providing explicit in-context examples that use these techniques can help the LMs improve their performance on KernelBench. Specifically, we include three in-context examples: GeLU [[13](#bib.bib13)] using operator fusion, matrix multiplication using tiling  [[20](#bib.bib20)], and a minimal Flash-Attention [[8](#bib.bib8), [15](#bib.bib15)] kernel that demonstrates shared memory I/O management.
  
  
In-context examples degrade the LM’s overall fast1\text{fast}_{1} score since LMs attempt more aggressive optimization strategies, but result in more execution failures. OpenAI o1’s generations are 25% longer on average using the few-shot examples, compared to the generations produced by [Section 4](#S4 "4 KernelBench Baseline Evaluation ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu") baseline. However, among the correct solutions, the LMs apply interesting optimizations: we find that on 77% of GEMM variants in KernelBench Level 1, o1 applies tiling and improves speed over the one-shot baseline (although remains slower than PyTorch Eager due to the lack of tensor core utilization). On Level 2, o1 applies aggressive shared memory I/O management on 11 problems, and is able to outperform PyTorch Eager (See Appendix [F](#A6 "Appendix F Few Shot Experiment ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu")).

#### 5.2.2 Specifying Hardware Information

As discussed in Section [4.4](#S4.SS4 "4.4 Performance Variations across Hardware ‣ 4 KernelBench Baseline Evaluation ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu"), kernel performance varies depending on the hardware platform. For instance, FlashAttention-2 [[6](#bib.bib6)] degrades 47% in hardware utilization going from the NVIDIA A100 to H100 GPU. FlashAttention-3 [[30](#bib.bib30)], an entirely different algorithm, was written for the H100. In this study, we explore whether LMs can use (1) hardware specifications such as the GPU type (H100, A100, etc.), memory sizes, bandwidths, TFLOPS and (2) hardware knowledge (e.g. definitions of threads, warps, thread-blocks, streaming multiprocessors) in-context to generate improved kernels (See Appendix [G](#A7 "Appendix G Cross-Hardware Case Study ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu") for more detail on the context).
  
  
Models rarely generate kernels that are optimized for the underlying hardware, highlighting room for improvement for future models. Certain generations of GPUs (e.g. H100) feature a variety of new hardware units and instructions from their predecessors. Providing hardware information does not significantly impact the outputs of Llama 3.1 70B or DeepSeek-V3.

Interestingly, we find that a subset of OpenAI o1 and DeepSeek-R1 generated kernels use hardware-specific instructions and optimizations. R1 attempts to generate warp matrix multiply-accumulate (wmma) instructions (Figure [11](#A7.F11 "Figure 11 ‣ G.2 Effect of Providing Hardware Information ‣ Appendix G Cross-Hardware Case Study ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu")) for approximately 50%50\% of the Level 1 matrix multiplication problems, although most fail to compile. Among the functionally correct generations, R1 and o1 produce 1-3 outliers per level that are ≥2×\geq 2\times faster than the [Section 4](#S4 "4 KernelBench Baseline Evaluation ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu") baselines. Overall, we find that LMs are better at adjusting their approaches when provided with few-shot examples in [Section 5.2.1](#S5.SS2.SSS1 "5.2.1 Hardware-aware In-Context Examples ‣ 5.2 Case Study: Generating Hardware-Efficient Kernels via Hardware Knowledge ‣ 5 Analysis of Model Capabilities ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu") than with hardware information.

## 6 Discussion

### 6.1 Deep Dive Into Interesting Kernels

Here, we discuss a few surprising LM-generated kernels that demonstrate significant speedups over the PyTorch baseline. See detailed examples in Appendix [D](#A4 "Appendix D Kernels of Interest ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu").
  
  
Operator fusion GPUs have small amounts of fast-access memory and large amounts of slow-access memory. Fusion can help reduce slow-access I/O costs by performing multiple operations on data that has been loaded into fast-access memory.
We find that LMs optimize the GELU (2.9x) and Softsign (1.3x) operators by fusing their computations into a single kernel. LMs generated a kernel that fuses multiple foundational operators – matrix multiplication with division, summation, and scaling – giving a 2.6x speedup. Overall, LMs leave many fusion opportunities on the table.
  
  
Memory hierarchy Effective kernels explicitly manage utilization of the limited amounts of shared and register memory. In the generated kernels, we found kernels that uses GPU shared memory – cosine similarity (2.8x) and triplet margin loss (2.0x) – to achieve speedups. We did not find successful usages of tensor core instructions, which are crucial for AI performance.
  
  
Algorithmic optimizations Kernels can require algorithmic modifications to better utilize the hardware features. We found one interesting generation for the problem of performing a multiplication between a dense and diagonal matrix, where the kernel scales each row (or column), rather than loading the zero-entries of the diagonal matrix, yielding a 13x speedup over PyTorch Eager.

### 6.2 Conclusion

Our contributions are: (1) We present KernelBench, a framework that lays the groundwork for LM-driven kernel optimization, and (2) We evaluate a diverse set of models and approaches, analyzing their strengths and limitations, and providing insights into opportunities for improvement.

Overall, while most benchmarks eventually saturate, KernelBench is designed to dynamically evolve as new AI workloads arise. Our fastp\text{fast}_{p} metric can be adapted over time to measure the speedup threshold (pp) over increasingly advanced baselines (i.e., beyond the PyTorch baseline used in our work). Since PyTorch is cross-hardware platform compatible, the PyTorch-based tasks in KernelBench tasks can be evaluated on every new hardware platform release.
Finally, unlike many benchmarks, success on KernelBench directly maps to production value and real-world impacts (lowering costs and reducing energy consumption at scale). These properties ensure that KernelBench will remain valuable in the ever-evolving AI landscape.

### 6.3 Opportunities for Future Work

We show that there is significant room for improvement on KernelBench given the currently available models.
First, future work can explore the development of advanced fine-tuning and reasoning techniques, including agentic workflows. Since CUDA is a low-resource language, it would be valuable for future work to open-source more high quality data. Second, LMs generate raw CUDA code in our experiments. However, future work can explore whether generating code using alternative programming abstractions (e.g., provided in ThunderKittens, CUTLASS, Triton, and others) can simplify the generation problem, for instance by making it easier for LMs to leverage tensor core instructions. Third, our evaluation has also been limited to GPUs so far and future work can expand to other hardware accelerators.

## Ethics Statement

Optimized GPU kernels can lead to significant energy savings in large-scale machine learning workloads, reducing both computational costs and environmental impact. By providing a framework for AI-assisted performance tuning, KernelBench contributes to more energy-efficient AI systems, aligning with global efforts to reduce the carbon footprint of computing infrastructure.

KernelBench does not involve human studies or collect user data, eliminating privacy concerns. It also avoids proprietary or private code, relying solely on publicly available Github repositories.

## Acknowledgements

We are grateful to Google DeepMind, Google, IBM, Stanford HAI, PrimeIntellect, and Modal for supporting this work. We thank Aaryan Singhal, AJ Root, Allen Nie, Anjiang Wei, Benjamin Spector, Bilal Khan, Bradley Brown, Dylan Patel, Genghan Zhang, Hieu Pham, Hugh Leather, John Yang, Jon Saad-Falcon, Jordan Juravsky, Marcel Rød, Mark Saroufim, Michael Zhang, Minkai Xu, Ryan Ehrlich, Sahan Paliskara, Sahil Jain, Shicheng (George) Liu, Simran Arora, Suhas Kotha, Vikram Sharma Mailthody, and Yangjun Ruan for insightful discussions and constructive feedback in shaping this work.

## References

- [1]

  Apple.
  Apple ml compute framework (mlx), 2020.
  URL <https://developer.apple.com/metal/>.
- [2]

  Simran Arora, Sabri Eyuboglu, Michael Zhang, Aman Timalsina, Silas Alberti, Dylan Zinsley, James Zou, Atri Rudra, and Christopher Ré.
  Simple linear attention language models balance the recall-throughput tradeoff.
  *International Conference on Machine Learning*, 2024.
- [3]

  Bradley Brown, Jordan Juravsky, Ryan Ehrlich, Ronald Clark, Quoc V. Le, Christopher Ré, and Azalia Mirhoseini.
  Large language monkeys: Scaling inference compute with repeated sampling, 2024.
  URL <https://arxiv.org/abs/2407.21787>.
- [4]

  Cerebras.
  Cerebras wafer-scale engine wse architecture.
  Online.
  <https://cerebras.ai/product-chip/>.
- [5]

  Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde de Oliveira Pinto, Jared Kaplan, Harri Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman, Alex Ray, Raul Puri, Gretchen Krueger, Michael Petrov, Heidy Khlaaf, Girish Sastry, Pamela Mishkin, Brooke Chan, Scott Gray, Nick Ryder, Mikhail Pavlov, Alethea Power, Lukasz Kaiser, Mohammad Bavarian, Clemens Winter, Philippe Tillet, Felipe Petroski Such, Dave Cummings, Matthias Plappert, Fotios Chantzis, Elizabeth Barnes, Ariel Herbert-Voss, William Hebgen Guss, Alex Nichol, Alex Paino, Nikolas Tezak, Jie Tang, Igor Babuschkin, Suchir Balaji, Shantanu Jain, William Saunders, Christopher Hesse, Andrew N. Carr, Jan Leike, Josh Achiam, Vedant Misra, Evan Morikawa, Alec Radford, Matthew Knight, Miles Brundage, Mira Murati, Katie Mayer, Peter Welinder, Bob McGrew, Dario Amodei, Sam McCandlish, Ilya Sutskever, and Wojciech Zaremba.
  Evaluating large language models trained on code, 2021.
  URL <https://arxiv.org/abs/2107.03374>.
- [6]

  Tri Dao.
  FlashAttention-2: Faster attention with better parallelism and work partitioning.
  *International Conference on Learning Representations*, 2024.
- [7]

  Tri Dao and Albert Gu.
  Transformers are ssms: Generalized models and efficient algorithms through structured state space duality.
  *International Conference on Machine Learning (ICML)*, 2024.
- [8]

  Tri Dao, Daniel Y. Fu, Stefano Ermon, Atri Rudra, and Christopher Ré.
  FlashAttention: Fast and memory-efficient exact attention with IO-awareness.
  In *Advances in Neural Information Processing Systems*, 2022.
- [9]

  DeepSeek-AI.
  Deepseek-v3 technical report, 2025.
  URL <https://github.com/deepseek-ai/DeepSeek-V3>.
- [10]

  Graphcore.
  Graphcore IPU architecture.
  Online.
  <https://www.graphcore.ai/products/ipu>.
- [11]

  Groq.
  Groq architecture.
  Online.
  <https://groq.com/>.
- [12]

  Dejan Grubisic, Chris Cummins, Volker Seeker, and Hugh Leather.
  Priority sampling of large language models for compilers, 2024.
  URL <https://arxiv.org/abs/2402.18734>.
- [13]

  Dan Hendrycks and Kevin Gimpel.
  Gaussian error linear units (gelus), 2023.
  URL <https://arxiv.org/abs/1606.08415>.
- [14]

  Norman P. Jouppi, George Kurian, Sheng Li, Peter Ma, Rahul Nagarajan, Lifeng Nai, Nishant Patil, Suvinay Subramanian, Andy Swing, Brian Towles, Cliff Young, Xiang Zhou, Zongwei Zhou, and David Patterson.
  Tpu v4: An optically reconfigurable supercomputer for machine learning with hardware support for embeddings, 2023.
  URL <https://arxiv.org/abs/2304.01433>.
- [15]

  Peter Kim.
  Flashattention minimal.
  Online, 2024.
  <https://github.com/tspeterkim/flash-attention-minimal>.
- [16]

  Denis Kocetkov, Raymond Li, Loubna Ben Allal, Jia Li, Chenghao Mou, Carlos Muñoz Ferrandis, Yacine Jernite, Margaret Mitchell, Sean Hughes, Thomas Wolf, Dzmitry Bahdanau, Leandro von Werra, and Harm de Vries.
  The stack: 3 tb of permissively licensed source code, 2022.
  URL <https://arxiv.org/abs/2211.15533>.
- [17]

  Yuhang Lai, Chengxi Li, Yiming Wang, Tianyi Zhang, Ruiqi Zhong, Luke Zettlemoyer, Scott Wen tau Yih, Daniel Fried, Sida Wang, and Tao Yu.
  Ds-1000: A natural and reliable benchmark for data science code generation, 2022.
  URL <https://arxiv.org/abs/2211.11501>.
- [18]

  Raymond Li, Loubna Ben Allal, Yangtian Zi, Niklas Muennighoff, Denis Kocetkov, Chenghao Mou, Marc Marone, Christopher Akiki, Jia Li, Jenny Chim, Qian Liu, Evgenii Zheltonozhskii, Terry Yue Zhuo, Thomas Wang, Olivier Dehaene, Mishig Davaadorj, Joel Lamy-Poirier, João Monteiro, Oleh Shliazhko, Nicolas Gontier, Nicholas Meade, Armel Zebaze, Ming-Ho Yee, Logesh Kumar Umapathi, Jian Zhu, Benjamin Lipkin, Muhtasham Oblokulov, Zhiruo Wang, Rudra Murthy, Jason Stillerman, Siva Sankalp Patel, Dmitry Abulkhanov, Marco Zocca, Manan Dey, Zhihan Zhang, Nour Fahmy, Urvashi Bhattacharyya, Wenhao Yu, Swayam Singh, Sasha Luccioni, Paulo Villegas, Maxim Kunakov, Fedor Zhdanov, Manuel Romero, Tony Lee, Nadav Timor, Jennifer Ding, Claire Schlesinger, Hailey Schoelkopf, Jan Ebert, Tri Dao, Mayank Mishra, Alex Gu, Jennifer Robinson, Carolyn Jane Anderson, Brendan Dolan-Gavitt, Danish Contractor, Siva Reddy, Daniel Fried, Dzmitry Bahdanau, Yacine Jernite, Carlos Muñoz Ferrandis, Sean Hughes, Thomas Wolf, Arjun Guha, Leandro von
  Werra, and Harm de Vries.
  Starcoder: may the source be with you!, 2023.
  URL <https://arxiv.org/abs/2305.06161>.
- [19]

  Yujia Li, David Choi, Junyoung Chung, Nate Kushman, Julian Schrittwieser, Rémi Leblond, Tom Eccles, James Keeling, Felix Gimeno, Agustin Dal Lago, Thomas Hubert, Peter Choy, Cyprien de Masson d’Autume, Igor Babuschkin, Xinyun Chen, Po-Sen Huang, Johannes Welbl, Sven Gowal, Alexey Cherepanov, James Molloy, Daniel J. Mankowitz, Esme Sutherland Robson, Pushmeet Kohli, Nando de Freitas, Koray Kavukcuoglu, and Oriol Vinyals.
  Competition-level code generation with alphacode.
  *Science*, 378(6624):1092–1097, December 2022.
  ISSN 1095-9203.
  doi: 10.1126/science.abq1158.
  URL <http://dx.doi.org/10.1126/science.abq1158>.
- [20]

  Christian J. Mills.
  Cuda mode notes - lecture 004.
  Online, 2024.
  <https://christianjmills.com/posts/cuda-mode-notes/lecture-004/>.
- [21]

  Daniel Nichols, Pranav Polasam, Harshitha Menon, Aniruddha Marathe, Todd Gamblin, and Abhinav Bhatele.
  Performance-aligned llms for generating fast code, 2024.
  URL <https://arxiv.org/abs/2404.18864>.
- [22]

  NVIDIA.
  cudnn: Gpu-accelerated library for deep neural networks, 2014.
  URL <https://developer.nvidia.com/cudnn>.
- [23]

  NVIDIA.
  Cuda templates for linear algebra subroutines, 2017a.
  URL <https://github.com/NVIDIA/cutlass>.
- [24]

  NVIDIA.
  Nvidia Tesla V100 GPU architecture, 2017b.
- [25]

  NVIDIA.
  Nvidia A100 tensor core GPU architecture, 2020.
- [26]

  NVIDIA.
  Nvidia H100 tensor core GPU architecture, 2022.
- [27]

  NVIDIA.
  cuBLAS, 2023.
  URL <https://docs.nvidia.com/cuda/cublas/>.
- [28]

  Adam Paszke, Sam Gross, Francisco Massa, Adam Lerer, James Bradbury, Gregory Chanan, Trevor Killeen, Zeming Lin, Natalia Gimelshein, Luca Antiga, Alban Desmaison, Andreas Köpf, Edward Yang, Zach DeVito, Martin Raison, Alykhan Tejani, Sasank Chilamkurthy, Benoit Steiner, Lu Fang, Junjie Bai, and Soumith Chintala.
  Pytorch: An imperative style, high-performance deep learning library, 2019.
  URL <https://arxiv.org/abs/1912.01703>.
- [29]

  Bo Peng, Eric Alcaide, Quentin Anthony, Alon Albalak, Samuel Arcadinho, Huanqi Cao, Xin Cheng, Michael Chung, Matteo Grella, Kranthi Kiran GV, Xuzheng He, Haowen Hou, Przemyslaw Kazienko, Jan Kocon, and Jiaming et al. Kong.
  Rwkv: Reinventing rnns for the transformer era.
  *Findings of the Association for Computational Linguistics: EMNLP 2023*, 2023.
- [30]

  Jay Shah, Ganesh Bikshandi, Ying Zhang, Vijay Thakkar, Pradeep Ramani, and Tri Dao.
  Flashattention-3: Fast and accurate attention with asynchrony and low-precision, 2024.
  URL <https://arxiv.org/abs/2407.08608>.
- [31]

  Quan Shi, Michael Tang, Karthik Narasimhan, and Shunyu Yao.
  Can language models solve olympiad programming?, 2024.
  URL <https://arxiv.org/abs/2404.10952>.
- [32]

  Benjamin Spector, Simran Arora, Aaryan Singhal, Daniel Fu, and Christopher Ré.
  Thunderkittens: Simple, fast, and adorable ai kernels.
  *International Conference on Learning Representations (ICLR)*, 2024.
- [33]

  Yi Tay, Mostafa Dehghani, Dara Bahri, and Donald Metzler.
  Efficient transformers: A survey.
  *ACM Computing Surveys*, 55(6):1–28, 2022.
- [34]

  Team PyTorch, Horace He, Driss Guessous, Yanbo Liang, and Joy Dong.
  FlexAttention: The flexibility of PyTorch with the performance of FlashAttention, 2024.
  URL <https://pytorch.org/blog/flexattention/>.
- [35]

  Ali TehraniJamsaz, Arijit Bhattacharjee, Le Chen, Nesreen K. Ahmed, Amir Yazdanbakhsh, and Ali Jannesari.
  Coderosetta: Pushing the boundaries of unsupervised code translation for parallel programming.
  In *The Thirty-eighth Annual Conference on Neural Information Processing Systems*, 2024.
  URL <https://openreview.net/forum?id=V6hrg4O9gg>.
- [36]

  Philippe Tillet, H. T. Kung, and David Cox.
  Triton: an intermediate language and compiler for tiled neural network computations.
  In *Proceedings of the 3rd ACM SIGPLAN International Workshop on Machine Learning and Programming Languages*, 2019.
- [37]

  Alan M. Turing.
  On computable numbers, with an application to the Entscheidungsproblem.
  *Proceedings of the London Mathematical Society*, 2(42):230–265, 1936.
  URL <http://www.cs.helsinki.fi/u/gionis/cc05/OnComputableNumbers.pdf>.
- [38]

  Pedro Valero-Lara, Alexis Huante, Mustafa Al Lail, William F. Godoy, Keita Teranishi, Prasanna Balaprakash, and Jeffrey S. Vetter.
  Comparing llama-2 and gpt-3 llms for hpc kernels generation, 2023.
  URL <https://arxiv.org/abs/2309.07103>.
- [39]

  Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N Gomez, Lukasz Kaiser, and Illia Polosukhin.
  Attention is all you need.
  *31st Conference on Neural Information Processing Systems (NIPS 2017)*, 2017.
- [40]

  Siddhant Waghjale, Vishruth Veerendranath, Zhiruo Wang, and Daniel Fried.
  ECCO: Can we improve model-generated code efficiency without sacrificing functional correctness?
  In Yaser Al-Onaizan, Mohit Bansal, and Yun-Nung Chen (eds.), *Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing*, pp. 15362–15376, Miami, Florida, USA, November 2024. Association for Computational Linguistics.
  doi: 10.18653/v1/2024.emnlp-main.859.
  URL <https://aclanthology.org/2024.emnlp-main.859/>.
- [41]

  Yuanbo Wen, Qi Guo, Qiang Fu, Xiaqing Li, Jianxing Xu, Yanlin Tang, Yongwei Zhao, Xing Hu, Zidong Du, Ling Li, Chao Wang, Xuehai Zhou, and Yunji Chen.
  BabelTower: Learning to auto-parallelized program translation.
  In Kamalika Chaudhuri, Stefanie Jegelka, Le Song, Csaba Szepesvari, Gang Niu, and Sivan Sabato (eds.), *Proceedings of the 39th International Conference on Machine Learning*, volume 162 of *Proceedings of Machine Learning Research*, pp. 23685–23700. PMLR, 17–23 Jul 2022.
  URL <https://proceedings.mlr.press/v162/wen22b.html>.
- [42]

  Hjalmar Wijk, Tao Lin, Joel Becker, Sami Jawhar, Neev Parikh, Thomas Broadley, Lawrence Chan, Michael Chen, Josh Clymer, Jai Dhyani, Elena Ericheva, Katharyn Garcia, Brian Goodrich, Nikola Jurkovic, Megan Kinniment, Aron Lajko, Seraphina Nix, Lucas Sato, William Saunders, Maksym Taran, Ben West, and Elizabeth Barnes.
  Re-bench: Evaluating frontier ai r&d capabilities of language model agents against human experts, 2024.
  URL <https://arxiv.org/abs/2411.15114>.
- [43]

  John Yang, Carlos E. Jimenez, Alexander Wettig, Kilian Lieret, Shunyu Yao, Karthik Narasimhan, and Ofir Press.
  Swe-agent: Agent-computer interfaces enable automated software engineering.
  *arXiv:2405.15793*, 2024a.
- [44]

  John Yang, Carlos E. Jimenez, Alex L. Zhang, Kilian Lieret, Joyce Yang, Xindi Wu, Ori Press, Niklas Muennighoff, Gabriel Synnaeve, Karthik R. Narasimhan, Diyi Yang, Sida I. Wang, and Ofir Press.
  Swe-bench multimodal: Do ai systems generalize to visual software domains?, 2024b.
  URL <https://arxiv.org/abs/2410.03859>.
- [45]

  Songlin Yang and Yu Zhang.
  Fla: A triton-based library for hardware-efficient implementations of linear attention mechanism, January 2024.
  URL <https://github.com/sustcsonglin/flash-linear-attention>.
- [46]

  Pengcheng Yin, Wen-Ding Li, Kefan Xiao, Abhishek Rao, Yeming Wen, Kensen Shi, Joshua Howland, Paige Bailey, Michele Catasta, Henryk Michalewski, Alex Polozov, and Charles Sutton.
  Natural language to code generation in interactive data science notebooks, 2022.
  URL <https://arxiv.org/abs/2212.09248>.

## Appendix A KernelBench Task Example

Here we provide an example task from KernelBench. Each task is wrapped in a class named Model. A task contains two key functions in the Model class, __init__ and forward; helper functions are included if necessary. We fix the shape of inputs and vary the numerical values through randomly generated tensors. We provide two functions, get_inputs and get_init_inputs, for generating random parameters for initializing the model and running a forward pass, respectively.
  
  
PyTorch Reference Architecture:

[⬇](data:text/plain;base64,aW1wb3J0IHRvcmNoCmltcG9ydCB0b3JjaC5ubiBhcyBubgoKY2xhc3MgTW9kZWwobm4uTW9kdWxlKToKICAgICIiIgogICAgU2ltcGxlIG1vZGVsIHRoYXQgcGVyZm9ybXMgYSBzaW5nbGUgbWF0cml4IG11bHRpcGxpY2F0aW9uIChDID0gQSAqIEIpIHdpdGggYSBsYXJnZSBLIGRpbWVuc2lvbgogICAgIiIiCiAgICBkZWYgX19pbml0X18oc2VsZik6CiAgICAgICAgc3VwZXIoTW9kZWwsIHNlbGYpLl9faW5pdF9fKCkKCiAgICBkZWYgZm9yd2FyZChzZWxmLCBBOiB0b3JjaC5UZW5zb3IsIEI6IHRvcmNoLlRlbnNvcikgLT4gdG9yY2guVGVuc29yOgogICAgICAgICIiIgogICAgICAgIFBlcmZvcm1zIG1hdHJpeCBtdWx0aXBsaWNhdGlvbiBvZiBBIGFuZCBCLgoKICAgICAgICBBcmdzOgogICAgICAgICAgICBBOiBJbnB1dCB0ZW5zb3Igb2Ygc2hhcGUgKE0sIEspCiAgICAgICAgICAgIEI6IElucHV0IHRlbnNvciBvZiBzaGFwZSAoSywgTikKCiAgICAgICAgUmV0dXJuczoKICAgICAgICAgICAgT3V0cHV0IHRlbnNvciBvZiBzaGFwZSAoTSwgTikKICAgICAgICAiIiIKICAgICAgICByZXR1cm4gdG9yY2gubWF0bXVsKEEsIEIpCgpNID0gMjU2Ck4gPSAyNTYKSyA9IDEzMTA3MgoKZGVmIGdldF9pbnB1dHMoKToKICAgIEEgPSB0b3JjaC5yYW5kbihNLCBLKQogICAgQiA9IHRvcmNoLnJhbmRuKEssIE4pCiAgICByZXR1cm4gW0EsIEJdCgpkZWYgZ2V0X2luaXRfaW5wdXRzKCk6CiAgICByZXR1cm4gW10gICMgTm8gc3BlY2lhbCBpbml0aWFsaXphdGlvbiBpbnB1dHMgbmVlZGVk)

1
import torch

2
import torch.nn as nn

3

4
class Model(nn.Module):

5
 """

6
 Simple model that performs a single matrix multiplication (C = A * B) with a large K dimension

7
 """

8
 def __init__(self):

9
 super(Model, self).__init__()

10

11
 def forward(self, A: torch.Tensor, B: torch.Tensor) -> torch.Tensor:

12
 """

13
 Performs matrix multiplication of A and B.

14

15
 Args:

16
 A: Input tensor of shape (M, K)

17
 B: Input tensor of shape (K, N)

18

19
 Returns:

20
 Output tensor of shape (M, N)

21
 """

22
 return torch.matmul(A, B)

23

24
M = 256

25
N = 256

26
K = 131072

27

28
def get_inputs():

29
 A = torch.randn(M, K)

30
 B = torch.randn(K, N)

31
 return [A, B]

32

33
def get_init_inputs():

34
 return [] # No special initialization inputs needed

We include an example output from a model below that attempts to optimize the task specification above. The model is not only responsible for generating the kernel code, but is also responsible for generating the peripheral code to integrate the kernel into the PyTorch framework. The evaluation framework will run the forward pass of the model as if it is a PyTorch operator, so a common approach is to inline the CUDA code.

[⬇](data:text/plain;base64,aW1wb3J0IHRvcmNoCmltcG9ydCB0b3JjaC5ubiBhcyBubgpmcm9tIHRvcmNoLnV0aWxzLmNwcF9leHRlbnNpb24gaW1wb3J0IGxvYWRfaW5saW5lCgojIERlZmluZSB0aGUgY3VzdG9tIENVREEga2VybmVsIGZvciBtYXRyaXggbXVsdGlwbGljYXRpb24KbWF0bXVsX3NvdXJjZSA9ICIiIgojaW5jbHVkZSA8dG9yY2gvZXh0ZW5zaW9uLmg+CiNpbmNsdWRlIDxjdWRhX3J1bnRpbWUuaD4KCl9fZ2xvYmFsX18gdm9pZCBtYXRtdWxfa2VybmVsKGNvbnN0IGZsb2F0KiBBLCBjb25zdCBmbG9hdCogQiwgZmxvYXQqIEMsIGludCBNLCBpbnQgTiwgaW50IEspIHsKICAgIGludCByb3cgPSBibG9ja0lkeC55ICogYmxvY2tEaW0ueSArIHRocmVhZElkeC55OwogICAgaW50IGNvbCA9IGJsb2NrSWR4LnggKiBibG9ja0RpbS54ICsgdGhyZWFkSWR4Lng7CgogICAgaWYgKHJvdyA8IE0gJiYgY29sIDwgTikgewogICAgICAgIGZsb2F0IHN1bSA9IDAuMGY7CiAgICAgICAgZm9yIChpbnQgayA9IDA7IGsgPCBLOyArK2spIHsKICAgICAgICAgICAgc3VtICs9IEFbcm93ICogSyArIGtdICogQltrICogTiArIGNvbF07CiAgICAgICAgfQogICAgICAgIENbcm93ICogTiArIGNvbF0gPSBzdW07CiAgICB9Cn0KCnRvcmNoOjpUZW5zb3IgbWF0bXVsX2N1ZGEodG9yY2g6OlRlbnNvciBBLCB0b3JjaDo6VGVuc29yIEIpIHsKICAgIGludCBNID0gQS5zaXplKDApOwogICAgaW50IE4gPSBCLnNpemUoMSk7CiAgICBpbnQgSyA9IEEuc2l6ZSgxKTsKCiAgICBhdXRvIEMgPSB0b3JjaDo6emVyb3Moe00sIE59LCBBLm9wdGlvbnMoKSk7CgogICAgZGltMyB0aHJlYWRzUGVyQmxvY2soMTYsIDE2KTsKICAgIGRpbTMgbnVtQmxvY2tzKChOICsgdGhyZWFkc1BlckJsb2NrLnggLSAxKSAvIHRocmVhZHNQZXJCbG9jay54LCAoTSArIHRocmVhZHNQZXJCbG9jay55IC0gMSkgLyB0aHJlYWRzUGVyQmxvY2sueSk7CgogICAgbWF0bXVsX2tlcm5lbDw8PG51bUJsb2NrcywgdGhyZWFkc1BlckJsb2NrPj4+KEEuZGF0YV9wdHI8ZmxvYXQ+KCksIEIuZGF0YV9wdHI8ZmxvYXQ+KCksIEMuZGF0YV9wdHI8ZmxvYXQ+KCksIE0sIE4sIEspOwoKICAgIHJldHVybiBDOwp9CiIiIgoKbWF0bXVsX2NwcF9zb3VyY2UgPSAoCiAgICAidG9yY2g6OlRlbnNvciBtYXRtdWxfY3VkYSh0b3JjaDo6VGVuc29yIEEsIHRvcmNoOjpUZW5zb3IgQik7IgopCgojIENvbXBpbGUgdGhlIGlubGluZSBDVURBIGNvZGUgZm9yIG1hdHJpeCBtdWx0aXBsaWNhdGlvbgptYXRtdWwgPSBsb2FkX2lubGluZSgKICAgIG5hbWU9Im1hdG11bCIsCiAgICBjcHBfc291cmNlcz1tYXRtdWxfY3BwX3NvdXJjZSwKICAgIGN1ZGFfc291cmNlcz1tYXRtdWxfc291cmNlLAogICAgZnVuY3Rpb25zPVsibWF0bXVsX2N1ZGEiXSwKICAgIHZlcmJvc2U9VHJ1ZSwKICAgIGV4dHJhX2NmbGFncz1bIiJdLAogICAgZXh0cmFfbGRmbGFncz1bIiJdLAopCgoKY2xhc3MgTW9kZWxOZXcobm4uTW9kdWxlKToKICAgIGRlZiBfX2luaXRfXyhzZWxmKToKICAgICAgICBzdXBlcihNb2RlbE5ldywgc2VsZikuX19pbml0X18oKQogICAgICAgIHNlbGYubWF0bXVsID0gbWF0bXVsCgogICAgZGVmIGZvcndhcmQoc2VsZiwgQTogdG9yY2guVGVuc29yLCBCOiB0b3JjaC5UZW5zb3IpIC0+IHRvcmNoLlRlbnNvcjoKICAgICAgICByZXR1cm4gc2VsZi5tYXRtdWwubWF0bXVsX2N1ZGEoQSwgQik=)

1
import torch

2
import torch.nn as nn

3
from torch.utils.cpp_extension import load_inline

4

5
# Define the custom CUDA kernel for matrix multiplication

6
matmul_source = """

7
#include <torch/extension.h>

8
#include <cuda_runtime.h>

9

10
__global__ void matmul_kernel(const float* A, const float* B, float* C, int M, int N, int K) {

11
 int row = blockIdx.y * blockDim.y + threadIdx.y;

12
 int col = blockIdx.x * blockDim.x + threadIdx.x;

13

14
 if (row < M && col < N) {

15
 float sum = 0.0f;

16
 for (int k = 0; k < K; ++k) {

17
 sum += A[row * K + k] * B[k * N + col];

18
 }

19
 C[row * N + col] = sum;

20
 }

21
}

22

23
torch::Tensor matmul_cuda(torch::Tensor A, torch::Tensor B) {

24
 int M = A.size(0);

25
 int N = B.size(1);

26
 int K = A.size(1);

27

28
 auto C = torch::zeros({M, N}, A.options());

29

30
 dim3 threadsPerBlock(16, 16);

31
 dim3 numBlocks((N + threadsPerBlock.x - 1) / threadsPerBlock.x, (M + threadsPerBlock.y - 1) / threadsPerBlock.y);

32

33
 matmul_kernel<<<numBlocks, threadsPerBlock>>>(A.data_ptr<float>(), B.data_ptr<float>(), C.data_ptr<float>(), M, N, K);

34

35
 return C;

36
}

37
"""

38

39
matmul_cpp_source = (

40
 "torch::Tensor matmul_cuda(torch::Tensor A, torch::Tensor B);"

41
)

42

43
# Compile the inline CUDA code for matrix multiplication

44
matmul = load_inline(

45
 name="matmul",

46
 cpp_sources=matmul_cpp_source,

47
 cuda_sources=matmul_source,

48
 functions=["matmul_cuda"],

49
 verbose=True,

50
 extra_cflags=[""],

51
 extra_ldflags=[""],

52
)

53

54

55
class ModelNew(nn.Module):

56
 def __init__(self):

57
 super(ModelNew, self).__init__()

58
 self.matmul = matmul

59

60
 def forward(self, A: torch.Tensor, B: torch.Tensor) -> torch.Tensor:

61
 return self.matmul.matmul_cuda(A, B)

## Appendix B Evaluation Methodology and Baselines

All evaluations are conducted on a bare-metal NVIDIA L40S GPU with Ada Lovelace architecture unless otherwise stated (such as the device generalization experiments in Section [4.4](#S4.SS4 "4.4 Performance Variations across Hardware ‣ 4 KernelBench Baseline Evaluation ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu") and the hardware case study in [5.2](#S5.SS2 "5.2 Case Study: Generating Hardware-Efficient Kernels via Hardware Knowledge ‣ 5 Analysis of Model Capabilities ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu")). The NVIDIA L40S has 48 GB of HBM memory and operates at 300W. Our environment uses Python 3.10, PyTorch 2.5.0+cu124, and CUDA 12.4, which is also where our PyTorch Eager and torch.compile baselines are derived from.

### B.1 Kernel Evaluation Setup

Recall the KernelBench task entails a PyTorch reference module Model as baseline, and model-generated PyTorch architecture ModelNew with custom inline CUDA kernel.
  
  
For correctness, we set num_correctness to 5, where we check equivalence of output between reference architecture Model and generated architecture with custom kernel ModelNew with 5 randomized inputs. We elaborate on our choice in Appendix [B.2](#A2.SS2 "B.2 Correctness Analysis Varying Number of Randomly Generated Inputs ‣ Appendix B Evaluation Methodology and Baselines ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu").
  
  
For performance, we measure the wall-clock execution time of nn.module.forward for both Model and ModelNew. We ensure only one kernel is being evaluated (no other CUDA process) on current GPU. We warm up for 3 iterations and then set num_profile to 100 times which measures the elapsed execution time signaled between CUDA events torch.cuda.Event. We take the mean of the 100 trials, and also note its max, min, and standard deviation. While the wall clock time might vary for every trial, we note our coefficient of variation (CV): std/mean\text{std}/\text{mean} is consistently <3%<3\%, we use the mean of both measured wall clock time for comparisons.

To compute the speedup of generated architecture over baseline architecture for individual problems, we use the mean for both speedup=TM​o​d​e​l/TM​o​d​e​l​N​e​w\text{speedup}=T_{Model}/T_{ModelNew}. For example, if TM​o​d​e​l=2T_{Model}=2 ms and TM​o​d​e​l​N​e​w=1T_{ModelNew}=1 ms, we have a 2x speedup with the newly generated kernel. We compare this speedup with our speedup threshold parameter pp (as explained in section [3.3](#S3.SS3 "3.3 Metric Design ‣ 3 KernelBench: A Framework for AI Kernel Generation ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu")) to compute fastp\text{fast}_{p} scores.

### B.2 Correctness Analysis Varying Number of Randomly Generated Inputs

Checking equivalence of programs in a formal sense is undecidable. ”The Halting Problem” [[37](#bib.bib37)] states that it is impossible to decide, in general, whether a given program will terminate for every possible input. This problem naturally extends to checking equivalence because in order to check whether two programs are equivalent, it is necessary to check their behavior for all inputs, including cases where one or both programs may not terminate. Since determining whether a program halts on a given input is undecidable (the Halting Problem), checking equivalence also becomes undecidable.

Approximate or heuristic methods are often used in practice for checking program equivalence. Random testing is the most common practical approach, where the program is run with sets of randomly chosen inputs, and their outputs are compared. Random testing is particularly effective for AI kernels, where control flow is simpler and the focus is primarily on numerical correctness. By using diverse inputs, it can uncover errors in computations or memory handling with high probability. Evaluating correctness more systematically, especially in the presence of subtle hardware-specific behavior, is an area for further exploration. Future work could investigate formal verification tools to provide stronger guarantees of equivalence.

We use five sets of random inputs for correctness, which is a good tradeoff between the ability to catch errors and efficiency. In an experiment with 100 generated kernels, the results were as follows: 50 kernels were correct (all 5/5 and 100/100), 19 had output value mismatches (19 0/5 and 0/100), 4 had output shape mismatches, 10 encountered runtime errors, and 17 had compilation errors. Notably, the 0/5 and 0/100 failures indicate that no partial correctness was observed.

### B.3 Distribution of Model Performance for One-Shot Baseline

Here we examine the quality of (functionally correct) kernel generations across a wide variety of models. Figure [8](#A2.F8 "Figure 8 ‣ B.3 Distribution of Model Performance for One-Shot Baseline ‣ Appendix B Evaluation Methodology and Baselines ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu") shows the distribution of speedups for various kernels across different levels and models. The median speedup for both Level 1 and Level 3 are less than 1, and the median speedup for Level 2 is only slightly above one. Level 1 has the most significant outliers, in one case showing a speedup greater than 10. We explored some of these outlier cases in greater detail in Section [6](#S6 "6 Discussion ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu").
  
  
Reasoning-optimized models (OpenAI-o1 and DeepSeek-R1) perform the best of out-of-the-box across all levels. These models demonstrate superior kernel generation capabilities, particularly excelling at Level 2 tasks (which mainly involve kernel fusion). In contrast, Llama 3.1 models (both 405B and 70B) perform poorly regardless of model size, suggesting that larger models do not necessarily guarantee better results for this task. DeepSeek-R1, while strong at Level 1 and 2, suffers significantly at Level 3, often generating incorrect kernels.

![Refer to caption](2502.10517v1/figures/greedy_speedup_box_whiskers.png)

Figure 8: A box and whisker plot of the speedup relative to Torch Eager of (correct) kernels generated by various models in the one-shot baseline setting. We also write the percentage of correctly generated kernels next to the model name. We observe that among most models, the median speedup for correctly generated kernels is below 1.

### B.4 PyTorch Baselines

PyTorch offers two common execution modes: Eager and torch.compile.
Aside from the results shown in Table [3](#S4.F3 "Figure 3 ‣ 4.1 One-shot Baseline ‣ 4 KernelBench Baseline Evaluation ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu"), all performance analysis is evaluated against PyTorch Eager.
  
  
PyTorch Eager is the default execution mode of PyTorch, which dynamically executes computation by invoking calls to highly optimized closed-source kernels.
  
  
PyTorch Compile or torch.compile uses rule-based heuristics over the underlying computation graph during an initial compilation phase and invokes various backends to perform optimizations like kernel fusion and graph transformations. In Table [3](#S4.F3 "Figure 3 ‣ 4.1 One-shot Baseline ‣ 4 KernelBench Baseline Evaluation ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu"), our performance baseline for torch.compile assumes the default configuration using PyTorch Inductor in default mode. Furthermore, we exclude the torch.compile compile time in our timing analysis, as we are only interested in the raw runtime behavior. torch.compile features multiple other backends and configurations, which we describe in Table [2](#A2.T2 "Table 2 ‣ B.4 PyTorch Baselines ‣ Appendix B Evaluation Methodology and Baselines ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu").

We observe that the torch.compile baseline runtime is generally faster on Level 2 and 3 of KernelBench reference problems compared to PyTorch Eager, mostly due to the availability of graph-level optimizations like operator fusion. However, on Level 1 problems, torch.compile can exhibit higher runtimes than PyTorch Eager, which can be attribute to empirically-reproducible runtime overhead for torch.compile (not compile time) that is significant for small kernels.

|  |  |  |  |
| --- | --- | --- | --- |
| Configuration | Backend | Mode | Description |
| PyTorch (Eager) | - | - | Standard PyTorch eager execution |
| Torch Compile | inductor | default | Default torch.compile behavior |
| Torch Compile | inductor | reduce-overhead | Optimized for reduced overhead |
| Torch Compile | inductor | max-autotune | Max autotuning enabled |
| Torch Compile | inductor | max-autotune-no-cudagraphs | Max autotuning without CUDA graphs |
| Torch Compile | cudagraphs | - | CUDA graphs with AOT Autograd |

Table 2: Configurations and modes for PyTorch execution and optimization backends.

Other torch.compile backends. In Table [3](#A2.T3 "Table 3 ‣ B.4 PyTorch Baselines ‣ Appendix B Evaluation Methodology and Baselines ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu"), we show more one-shot baseline results for fast1\text{fast}_{1} against some of the other torch.compile baselines. We note on some other configurations fast1\text{fast}_{1} drops especially for Level 2, as the torch.compile backends apply more aggressive optimization (at the cost of extra compile-time overhead, which we do not measure). Due to the variability of torch.compile across configurations, we focus our analysis on PyTorch Eager.

|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| fast1\text{fast}_{1} over: | torch.compile  default | | | cudagraphs | | | max-autotune | | | max-autotune  no-cudagraphs | | | reduce-overhead | | |
| KernelBench Level | 1 | 2 | 3 | 1 | 2 | 3 | 1 | 2 | 3 | 1 | 2 | 3 | 1 | 2 | 3 |
| Claude 3.5 Sonnet | 29% | 2% | 2% | 31% | 7% | 2% | 31% | 2% | 0% | 29% | 2% | 2% | 31% | 2% | 0% |
| DeepSeek V3 | 20% | 2% | 2% | 21% | 4% | 20% | 21% | 2% | 2% | 20% | 2% | 2% | 21% | 2% | 0% |
| DeepSeek R1 | 38% | 37% | 2% | 42% | 52% | 0% | 42% | 29% | 0% | 38% | 32% | 4% | 42% | 28% | 0% |
| GPT-4o | 18% | 4% | 4% | 22% | 6% | 6% | 21% | 4% | 2% | 18% | 3% | 4% | 21% | 4% | 0% |
| Llama 3.1-70B Inst. | 11% | 0% | 0% | 12% | 0% | 0% | 12% | 0% | 0% | 11% | 0% | 0% | 12% | 0% | 0% |
| Llama 3.1-405B Inst. | 16% | 0% | 0% | 16% | 0% | 4% | 16% | 0% | 0% | 16% | 0% | 0% | 16% | 0% | 0% |
| OpenAI O1 | 28% | 19% | 4% | 33% | 37% | 26% | 34% | 8% | 4% | 30% | 19% | 6% | 34% | 8% | 2% |

Table 3: We compare KernelBench torch.compile baseline runtime across various configurations, all measured on NVIDIA L40S, in addition to what is showed in Table [3](#S4.F3 "Figure 3 ‣ 4.1 One-shot Baseline ‣ 4 KernelBench Baseline Evaluation ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu").

## Appendix C Experiment Prompting Details

We provide details for the prompting strategies and associated sampling strategies used in Section [4](#S4 "4 KernelBench Baseline Evaluation ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu") and Section [5](#S5 "5 Analysis of Model Capabilities ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu").

### C.1 One-shot Baseline Prompt

For the one-shot baseline as shown in Section [4.1](#S4.SS1 "4.1 One-shot Baseline ‣ 4 KernelBench Baseline Evaluation ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu"), we want to examine each model’s out-of-the-box ability to generate kernels by providing the minimum set of information while ensuring the instructions and output format are clear. We query each model with the following prompt and a pair of in-context add examples (the PyTorch reference add and its CUDA kernel counterpart using inline compilation) to provide the output format. We sample the model with greedy decoding to ensure deterministic output, which is setting temperature=0\text{temperature}=0.

[⬇](data:text/plain;base64,WW91IHdyaXRlIGN1c3RvbSBDVURBIGtlcm5lbHMgdG8gcmVwbGFjZSB0aGUgcHl0b3JjaCBvcGVyYXRvcnMgaW4gdGhlIGdpdmVuIGFyY2hpdGVjdHVyZQp0byBnZXQgc3BlZWR1cHMuCgpZb3UgaGF2ZSBjb21wbGV0ZSBmcmVlZG9tIHRvIGNob29zZSB0aGUgc2V0IG9mIG9wZXJhdG9ycyB5b3Ugd2FudCB0byByZXBsYWNlLiBZb3UgbWF5Cm1ha2UgdGhlIGRlY2lzaW9uIHRvIHJlcGxhY2Ugc29tZSBvcGVyYXRvcnMgd2l0aCBjdXN0b20gQ1VEQSBrZXJuZWxzIGFuZCBsZWF2ZSBvdGhlcnMKdW5jaGFuZ2VkLiBZb3UgbWF5IHJlcGxhY2UgbXVsdGlwbGUgb3BlcmF0b3JzIHdpdGggY3VzdG9tIGltcGxlbWVudGF0aW9ucywgY29uc2lkZXIKb3BlcmF0b3IgZnVzaW9uIG9wcG9ydHVuaXRpZXMgKGNvbWJpbmluZyBtdWx0aXBsZSBvcGVyYXRvcnMgaW50byBhIHNpbmdsZSBrZXJuZWwsIGZvcgpleGFtcGxlLCBjb21iaW5pbmcgbWF0bXVsK3JlbHUpLCBvciBhbGdvcml0aG1pYyBjaGFuZ2VzIChzdWNoIGFzIG9ubGluZSBzb2Z0bWF4KS4gWW91IGFyZQpvbmx5IGxpbWl0ZWQgYnkgeW91ciBpbWFnaW5hdGlvbi4KCkhlcmVcJ3MgYW4gZXhhbXBsZSB0byBzaG93IHlvdSB0aGUgc3ludGF4IG9mIGlubGluZSBlbWJlZGRpbmcgY3VzdG9tIENVREEgb3BlcmF0b3JzIGluCnRvcmNoOiBUaGUgZXhhbXBsZSBnaXZlbiBhcmNoaXRlY3R1cmUgaXM6CmBgYAppbXBvcnQgdG9yY2gKaW1wb3J0IHRvcmNoLm5uIGFzIG5uCmltcG9ydCB0b3JjaC5ubi5mdW5jdGlvbmFsIGFzIEYKCgpjbGFzcyBNb2RlbChubi5Nb2R1bGUpOgogICAgZGVmIF9faW5pdF9fKHNlbGYpIC0+IE5vbmU6CiAgICAgICAgc3VwZXIoKS5fX2luaXRfXygpCgogICAgZGVmIGZvcndhcmQoc2VsZiwgYSwgYik6CiAgICAgICAgcmV0dXJuIGEgKyBiCgoKZGVmIGdldF9pbnB1dHMoKToKICAgICMgcmFuZG9tbHkgZ2VuZXJhdGUgaW5wdXQgdGVuc29ycyBiYXNlZCBvbiB0aGUgbW9kZWwgYXJjaGl0ZWN0dXJlCiAgICBhID0gdG9yY2gucmFuZG4oMSwgMTI4KS5jdWRhKCkKICAgIGIgPSB0b3JjaC5yYW5kbigxLCAxMjgpLmN1ZGEoKQogICAgcmV0dXJuIFthLCBiXQoKCmRlZiBnZXRfaW5pdF9pbnB1dHMoKToKICAgICMgcmFuZG9tbHkgZ2VuZXJhdGUgdGVuc29ycyByZXF1aXJlZCBmb3IgaW5pdGlhbGl6YXRpb24gYmFzZWQgb24gdGhlIG1vZGVsIGFyY2hpdGVjdHVyZQogICAgcmV0dXJuIFtdCmBgYAoKVGhlIGV4YW1wbGUgbmV3IGFyY2ggd2l0aCBjdXN0b20gQ1VEQSBrZXJuZWxzIGxvb2tzIGxpa2UgdGhpczoKYGBgCmltcG9ydCB0b3JjaAppbXBvcnQgdG9yY2gubm4gYXMgbm4KaW1wb3J0IHRvcmNoLm5uLmZ1bmN0aW9uYWwgYXMgRgpmcm9tIHRvcmNoLnV0aWxzLmNwcF9leHRlbnNpb24gaW1wb3J0IGxvYWRfaW5saW5lCgojIERlZmluZSB0aGUgY3VzdG9tIENVREEga2VybmVsIGZvciBlbGVtZW50LXdpc2UgYWRkaXRpb24KZWxlbWVudHdpc2VfYWRkX3NvdXJjZSA9ICIiIgojaW5jbHVkZSA8dG9yY2gvZXh0ZW5zaW9uLmg+CiNpbmNsdWRlIDxjdWRhX3J1bnRpbWUuaD4KCl9fZ2xvYmFsX18gdm9pZCBlbGVtZW50d2lzZV9hZGRfa2VybmVsKGNvbnN0IGZsb2F0KiBhLCBjb25zdCBmbG9hdCogYiwgZmxvYXQqIG91dCwgaW50IHNpemUpIHsKICAgIGludCBpZHggPSBibG9ja0lkeC54ICogYmxvY2tEaW0ueCArIHRocmVhZElkeC54OwogICAgaWYgKGlkeCA8IHNpemUpIHsKICAgICAgICBvdXRbaWR4XSA9IGFbaWR4XSArIGJbaWR4XTsKICAgIH0KfQoKdG9yY2g6OlRlbnNvciBlbGVtZW50d2lzZV9hZGRfY3VkYSh0b3JjaDo6VGVuc29yIGEsIHRvcmNoOjpUZW5zb3IgYikgewogICAgYXV0byBzaXplID0gYS5udW1lbCgpOwogICAgYXV0byBvdXQgPSB0b3JjaDo6emVyb3NfbGlrZShhKTsKCiAgICBjb25zdCBpbnQgYmxvY2tfc2l6ZSA9IDI1NjsKICAgIGNvbnN0IGludCBudW1fYmxvY2tzID0gKHNpemUgKyBibG9ja19zaXplIC0gMSkgLyBibG9ja19zaXplOwoKICAgIGVsZW1lbnR3aXNlX2FkZF9rZXJuZWw8PDxudW1fYmxvY2tzLCBibG9ja19zaXplPj4+KGEuZGF0YV9wdHI8ZmxvYXQ+KCksIGIuZGF0YV9wdHI8ZmxvYXQ+KCksIG91dC5kYXRhX3B0cjxmbG9hdD4oKSwgc2l6ZSk7CgogICAgcmV0dXJuIG91dDsKfQoiIiIKCmVsZW1lbnR3aXNlX2FkZF9jcHBfc291cmNlID0gInRvcmNoOjpUZW5zb3IgZWxlbWVudHdpc2VfYWRkX2N1ZGEodG9yY2g6OlRlbnNvciBhLCB0b3JjaDo6VGVuc29yIGIpOyIKCiMgQ29tcGlsZSB0aGUgaW5saW5lIENVREEgY29kZSBmb3IgZWxlbWVudC13aXNlIGFkZGl0aW9uCmVsZW1lbnR3aXNlX2FkZCA9IGxvYWRfaW5saW5lKAogICAgbmFtZT0nZWxlbWVudHdpc2VfYWRkJywKICAgIGNwcF9zb3VyY2VzPWVsZW1lbnR3aXNlX2FkZF9jcHBfc291cmNlLAogICAgY3VkYV9zb3VyY2VzPWVsZW1lbnR3aXNlX2FkZF9zb3VyY2UsCiAgICBmdW5jdGlvbnM9WydlbGVtZW50d2lzZV9hZGRfY3VkYSddLAogICAgdmVyYm9zZT1UcnVlLAogICAgZXh0cmFfY2ZsYWdzPVsnJ10sCiAgICBleHRyYV9sZGZsYWdzPVsnJ10KKQoKY2xhc3MgTW9kZWxOZXcobm4uTW9kdWxlKToKICAgIGRlZiBfX2luaXRfXyhzZWxmKSAtPiBOb25lOgogICAgICAgIHN1cGVyKCkuX19pbml0X18oKQogICAgICAgIHNlbGYuZWxlbWVudHdpc2VfYWRkID0gZWxlbWVudHdpc2VfYWRkCgogICAgZGVmIGZvcndhcmQoc2VsZiwgYSwgYik6CiAgICAgICAgcmV0dXJuIHNlbGYuZWxlbWVudHdpc2VfYWRkLmVsZW1lbnR3aXNlX2FkZF9jdWRhKGEsIGIpCmBgYAoKWW91IGFyZSBnaXZlbiB0aGUgZm9sbG93aW5nIGFyY2hpdGVjdHVyZToKCjxQeVRvcmNoIHJlZmVyZW5jZSBhcmNoaXRlY3R1cmUgZm9yIHNwZWNpZmljIEtlcm5lbEJlbmNoIFByb2JsZW0+CgpPcHRpbWl6ZSB0aGUgYXJjaGl0ZWN0dXJlIG5hbWVkIE1vZGVsIHdpdGggY3VzdG9tIENVREEgb3BlcmF0b3JzISBOYW1lIHlvdXIgb3B0aW1pemVkCm91dHB1dCBhcmNoaXRlY3R1cmUgTW9kZWxOZXcuIE91dHB1dCB0aGUgbmV3IGNvZGUgaW4gY29kZWJsb2Nrcy4gUGxlYXNlIGdlbmVyYXRlIHJlYWwKY29kZSwgTk9UIHBzZXVkb2NvZGUsIG1ha2Ugc3VyZSB0aGUgY29kZSBjb21waWxlcyBhbmQgaXMgZnVsbHkgZnVuY3Rpb25hbC4gSnVzdCBvdXRwdXQKdGhlIG5ldyBtb2RlbCBjb2RlLCBubyBvdGhlciB0ZXh0LCBhbmQgTk8gdGVzdGluZyBjb2RlIQ==)

1
You write custom CUDA kernels to replace the pytorch operators in the given architecture

2
to get speedups.

3

4
You have complete freedom to choose the set of operators you want to replace. You may

5
make the decision to replace some operators with custom CUDA kernels and leave others

6
unchanged. You may replace multiple operators with custom implementations, consider

7
operator fusion opportunities (combining multiple operators into a single kernel, for

8
example, combining matmul+relu), or algorithmic changes (such as online softmax). You are

9
only limited by your imagination.

10

11
Here\’s an example to show you the syntax of inline embedding custom CUDA operators in

12
torch: The example given architecture is:

13
‘‘‘

14
import torch

15
import torch.nn as nn

16
import torch.nn.functional as F

17

18

19
class Model(nn.Module):

20
 def __init__(self) -> None:

21
 super().__init__()

22

23
 def forward(self, a, b):

24
 return a + b

25

26

27
def get_inputs():

28
 # randomly generate input tensors based on the model architecture

29
 a = torch.randn(1, 128).cuda()

30
 b = torch.randn(1, 128).cuda()

31
 return [a, b]

32

33

34
def get_init_inputs():

35
 # randomly generate tensors required for initialization based on the model architecture

36
 return []

37
‘‘‘

38

39
The example new arch with custom CUDA kernels looks like this:

40
‘‘‘

41
import torch

42
import torch.nn as nn

43
import torch.nn.functional as F

44
from torch.utils.cpp_extension import load_inline

45

46
# Define the custom CUDA kernel for element-wise addition

47
elementwise_add_source = """

48
#include <torch/extension.h>

49
#include <cuda_runtime.h>

50

51
__global__ void elementwise_add_kernel(const float* a, const float* b, float* out, int size) {

52
 int idx = blockIdx.x * blockDim.x + threadIdx.x;

53
 if (idx < size) {

54
 out[idx] = a[idx] + b[idx];

55
 }

56
}

57

58
torch::Tensor elementwise_add_cuda(torch::Tensor a, torch::Tensor b) {

59
 auto size = a.numel();

60
 auto out = torch::zeros_like(a);

61

62
 const int block_size = 256;

63
 const int num_blocks = (size + block_size - 1) / block_size;

64

65
 elementwise_add_kernel<<<num_blocks, block_size>>>(a.data_ptr<float>(), b.data_ptr<float>(), out.data_ptr<float>(), size);

66

67
 return out;

68
}

69
"""

70

71
elementwise_add_cpp_source = "torch::Tensor elementwise_add_cuda(torch::Tensor a, torch::Tensor b);"

72

73
# Compile the inline CUDA code for element-wise addition

74
elementwise_add = load_inline(

75
 name=’elementwise_add’,

76
 cpp_sources=elementwise_add_cpp_source,

77
 cuda_sources=elementwise_add_source,

78
 functions=[’elementwise_add_cuda’],

79
 verbose=True,

80
 extra_cflags=[’’],

81
 extra_ldflags=[’’]

82
)

83

84
class ModelNew(nn.Module):

85
 def __init__(self) -> None:

86
 super().__init__()

87
 self.elementwise_add = elementwise_add

88

89
 def forward(self, a, b):

90
 return self.elementwise_add.elementwise_add_cuda(a, b)

91
‘‘‘

92

93
You are given the following architecture:

94

95
<PyTorch reference architecture for specific KernelBench Problem>

96

97
Optimize the architecture named Model with custom CUDA operators! Name your optimized

98
output architecture ModelNew. Output the new code in codeblocks. Please generate real

99
code, NOT pseudocode, make sure the code compiles and is fully functional. Just output

100
the new model code, no other text, and NO testing code!’

### C.2 Repeated Sampling Prompts

For repeated sampling, we use the same prompt that we used for the one-shot baseline in Appendix [C.1](#A3.SS1 "C.1 One-shot Baseline Prompt ‣ Appendix C Experiment Prompting Details ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu"). We used the same sampling temperature described in [[3](#bib.bib3)] as they allow sample diversity while ensuring quality. Specifically we use temperature=1.6\text{temperature}=1.6 for Deepseek-V3 and temperature=0.7\text{temperature}=0.7 for Llama 3.1-70B.

### C.3 Iterative Refinement Prompts

For iterative refinement, we start with the same initial prompt that we used for the one-shot baseline in Appendix [C.1](#A3.SS1 "C.1 One-shot Baseline Prompt ‣ Appendix C Experiment Prompting Details ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu"). A limitation of our experiments is that we sample with temperature=0=0 to focus on the effect of iterating based on feedback rather than introducing variability. On subsequent generations, we prompt the model with the following template depending on the feedback it expects:

[⬇](data:text/plain;base64,PEluaXRpYWwgcHJvbXB0IGZyb20gb25lLXNob3QgYmFzZWxpbmUgZm9yIHNwZWNpZmljIEtlcm5lbEJlbmNoIHByb2JsZW0uPgoKSGVyZSBpcyB5b3VyIGxhdGVzdCBnZW5lcmF0aW9uOgo8UHJldmlvdXNseSBnZW5lcmF0ZWQga2VybmVsIEc+CgpZb3VyIGdlbmVyYXRlZCBhcmNoaXRlY3R1cmUgTW9kZWxOZXcgYW5kIGtlcm5lbCB3YXMgZXZhbHVhdGVkIG9uIEdQVSBhbmQgY2hlY2tlZCBhZ2FpbnN0IHRoZSByZWZlcmVuY2UgYXJjaGl0ZWN0dXJlIE1vZGVsLgpIZXJlIGlzIHlvdXIgRXZhbHVhdGlvbiBSZXN1bHQ6Cgo8UmF3IENvbXBpbGVyIGFuZCBFeGVjdXRpb24gRmVlZGJhY2sgZnJvbSBzdGRvdXQ+Cgo8J2lmIGNvcnJlY3Q6Jz4KWW91ciBrZXJuZWwgZXhlY3V0ZWQgc3VjY2Vzc2Z1bGx5IGFuZCBwcm9kdWNlZCB0aGUgY29ycmVjdCBvdXRwdXQuCkhlcmUgaXMgeW91ciB3YWxsIGNsb2NrIHRpbWU6IHtydW50aW1lfSBtaWxsaXNlY29uZHMKCjxQcm9maWxlciBpbmZvcm1hdGlvbiBpZiB1c2VkIGFuZCBjb3JyZWN0Lj4KCk5hbWUgeW91ciBuZXcgaW1wcm92ZWQgb3V0cHV0IGFyY2hpdGVjdHVyZSBNb2RlbE5ldy4gT3V0cHV0IHRoZSBuZXcgY29kZSBpbiBjb2RlYmxvY2tzLiBQbGVhc2UgZ2VuZXJhdGUgcmVhbCBjb2RlLCBOT1QgcHNldWRvY29kZSwgbWFrZSBzdXJlIHRoZSBjb2RlIGNvbXBpbGVzIGFuZCBpcyBmdWxseSBmdW5jdGlvbmFsLiBKdXN0IG91dHB1dCB0aGUgbmV3IG1vZGVsIGNvZGUsIG5vIG90aGVyIHRleHQsIGFuZCBOTyB0ZXN0aW5nIGNvZGUh)

1
<Initial prompt from one-shot baseline for specific KernelBench problem.>

2

3
Here is your latest generation:

4
<Previously generated kernel G>

5

6
Your generated architecture ModelNew and kernel was evaluated on GPU and checked against the reference architecture Model.

7
Here is your Evaluation Result:

8

9
<Raw Compiler and Execution Feedback from stdout>

10

11
<’if correct:’>

12
Your kernel executed successfully and produced the correct output.

13
Here is your wall clock time: {runtime} milliseconds

14

15
<Profiler information if used and correct.>

16

17
Name your new improved output architecture ModelNew. Output the new code in codeblocks. Please generate real code, NOT pseudocode, make sure the code compiles and is fully functional. Just output the new model code, no other text, and NO testing code!

For the compiler and execution feedback, we handle timeouts and deadlocks explicitly with ”Your kernel execution timed out”, but do not provide any other information.

### C.4 Few-Shot in Context Prompts

For Few-Shot experiments as outlined in Section [5.2.1](#S5.SS2.SSS1 "5.2.1 Hardware-aware In-Context Examples ‣ 5.2 Case Study: Generating Hardware-Efficient Kernels via Hardware Knowledge ‣ 5 Analysis of Model Capabilities ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu"). We provide more details about the in-context example in Appendix [F](#A6 "Appendix F Few Shot Experiment ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu"). We sampled these experiments with temperature=0\text{temperature}=0.

[⬇](data:text/plain;base64,PEluaXRpYWwgVGFzayBwcm9tcHQgZnJvbSBvbmUtc2hvdCBiYXNlbGluZSBmb3IgSW5zdHJ1Y3Rpb24+CjxJbml0aWFsIHBhaXIgb2YgUmVmZXJlbmNlIFB5VG9yY2ggYW5kIENVREEga2VybmVsIGVxdWlhdmxlbnQgZm9yIGV4YW1wbGUgYWRkIGtlcm5lbCBmcm9tIG9uZS1zaG90IGJhc2VsaW5lIGZvciBJbnN0cnVjdGlvbj4KCkV4YW1wbGUgPGk+CkhlcmUgaXMgYW4gZXhhbXBsZSBhcmNoaXRlY3R1cmUKPFB5VG9yY2ggcmVmZXJlbmNlIGFyY2hpdGVjdHVyZSBmb3IgTm8uIGkgaW4tY29udGV4dCBleGFtcGxlPgoKSGVyZSBpcyBhbiBvcHRpbWl6ZWQgdmVyaXNvbiB3aXRoIGN1c3RvbSBDVURBIGtlcm5lbHM6CjxQeVRvcmNoIGFyY2hpdGVjdHVyZSB3aXRoIEN1c3RvbSBDVURBIEtlcm5lbCBmb3IgTm8uIGkgaW4tY29udGV4dCBleGFtcGxlPgoKLi4gdXAgdG8gbnVtYmVyIG9mIGluLWNvbnRleHQgc2FtcGxlIHRpbWVzCgoKVGFzazoKSGVyZSBpcyBhbiBleGFtcGxlIGFyY2hpdGVjdHVyZToKCjxQeVRvcmNoIHJlZmVyZW5jZSBhcmNoaXRlY3R1cmUgZm9yIHNwZWNpZmljIEtlcm5lbEJlbmNoIFByb2JsZW0+CgpOYW1lIHlvdXIgbmV3IGltcHJvdmVkIG91dHB1dCBhcmNoaXRlY3R1cmUgTW9kZWxOZXcuIE91dHB1dCB0aGUgbmV3IGNvZGUgaW4gY29kZWJsb2Nrcy4gUGxlYXNlIGdlbmVyYXRlIHJlYWwgY29kZSwgTk9UIHBzZXVkb2NvZGUsIG1ha2Ugc3VyZSB0aGUgY29kZSBjb21waWxlcyBhbmQgaXMgZnVsbHkgZnVuY3Rpb25hbC4gSnVzdCBvdXRwdXQgdGhlIG5ldyBtb2RlbCBjb2RlLCBubyBvdGhlciB0ZXh0LCBhbmQgTk8gdGVzdGluZyBjb2RlIQ==)

1
<Initial Task prompt from one-shot baseline for Instruction>

2
<Initial pair of Reference PyTorch and CUDA kernel equiavlent for example add kernel from one-shot baseline for Instruction>

3

4
Example <i>

5
Here is an example architecture

6
<PyTorch reference architecture for No. i in-context example>

7

8
Here is an optimized verison with custom CUDA kernels:

9
<PyTorch architecture with Custom CUDA Kernel for No. i in-context example>

10

11
.. up to number of in-context sample times

12

13

14
Task:

15
Here is an example architecture:

16

17
<PyTorch reference architecture for specific KernelBench Problem>

18

19
Name your new improved output architecture ModelNew. Output the new code in codeblocks. Please generate real code, NOT pseudocode, make sure the code compiles and is fully functional. Just output the new model code, no other text, and NO testing code!

### C.5 Hardware Case Study Prompts

Here we provide hardware information. This is used in Section [4.4](#S4.SS4 "4.4 Performance Variations across Hardware ‣ 4 KernelBench Baseline Evaluation ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu") and elaborated more in [G](#A7 "Appendix G Cross-Hardware Case Study ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu"), sampled with temperature=0\text{temperature}=0.

[⬇](data:text/plain;base64,PEluaXRpYWwgVGFzayBwcm9tcHQgZnJvbSBvbmUtc2hvdCBiYXNlbGluZSBmb3IgSW5zdHJ1Y3Rpb24+CjxJbml0aWFsIHBhaXIgb2YgUmVmZXJlbmNlIFB5VG9yY2ggYW5kIENVREEga2VybmVsIGVxdWlhdmxlbnQgZm9yIGV4YW1wbGUgYWRkIGtlcm5lbCBmcm9tIG9uZS1zaG90IGJhc2VsaW5lIGZvciBJbnN0cnVjdGlvbj4KCkhlcmUgaXMgc29tZSBpbmZvcm1hdGlvbiBhYm91dCB0aGUgdW5kZXJseWluZyBoYXJkd2FyZSB0aGF0IHlvdSBzaG91bGQga2VlcCBpbiBtaW5kLgoKVGhlIEdQVSB0aGF0IHdpbGwgcnVuIHRoZSBrZXJuZWwgaXMgTlZJRElBIDxHUFUgTkFNRT4uCgotIFdlIGhhdmUgPHg+IEdCIEdERFI2IHdpdGggRUNDIG9mIEdQVSBNZW1vcnkuCi0gV2UgaGF2ZSA8eD4gR0IvcyBvZiBNZW1vcnkgQmFuZHdpZHRoLgotIFdlIGhhdmUgPHg+IG9mIFJUIENvcmUgUGVyZm9ybWFuY2UgVEZMT1BTLgotIFdlIGhhdmUgPHg+IG9mIEZQMzIgVEZMT1BTLgotIFdlIGhhdmUgPHg+IG9mIFRGMzIgVGVuc29yIENvcmUgVEZMT1BTLgotIFdlIGhhdmUgPHg+IG9mIEZQMTYgVGVuc29yIENvcmUgVEZMT1BTLgotIFdlIGhhdmUgPHg+IG9mIEZQOCBUZW5zb3IgQ29yZSBURkxPUFMuCi0gV2UgaGF2ZSA8eD4gb2YgUGVhayBJTlQ4IFRlbnNvciBUT1BTLgotIFdlIGhhdmUgPHg+IG9mIFBlYWsgSU5UNCBUZW5zb3IgVE9QUy4KLSBXZSBoYXZlIDx4PiAzMi1iaXQgcmVnaXN0ZXJzIHBlciBTTSBvZiBSZWdpc3RlciBGaWxlIFNpemUuCi0gV2UgaGF2ZSA8eD4gb2YgTWF4aW11bSBudW1iZXIgb2YgcmVnaXN0ZXJzIHBlciB0aHJlYWQuCi0gV2UgaGF2ZSA8eD4gb2YgTWF4aW11bSBudW1iZXIgb2YgdGhyZWFkIGJsb2NrcyBwZXIgU00uCi0gV2UgaGF2ZSA8eD4gS0Igb2YgU2hhcmVkIG1lbW9yeSBjYXBhY2l0eSBwZXIgU00uCi0gV2UgaGF2ZSA8eD4gS0Igb2YgTWF4aW11bSBzaGFyZWQgbWVtb3J5IHBlciB0aHJlYWQgYmxvY2suCgoKCkhlcmUgYXJlIHNvbWUgY29uY2VwdHMgYWJvdXQgdGhlIEdQVSBhcmNoaXRlY3R1cmUgdGhhdCBjb3VsZCBiZSBoZWxwZnVsOgoKLSBUaHJlYWQ6IEEgdGhyZWFkIGlzIGEgc2luZ2xlIGV4ZWN1dGlvbiB1bml0IHRoYXQgY2FuIHJ1biBhIHNpbmdsZSBpbnN0cnVjdGlvbiBhdCBhIHRpbWUuCi0gVGhyZWFkIEJsb2NrOiBBIHRocmVhZCBibG9jayBpcyBhIGdyb3VwIG9mIHRocmVhZHMgdGhhdCBjYW4gY29vcGVyYXRlIHdpdGggZWFjaCBvdGhlci4KLSBTaGFyZWQgTWVtb3J5OiBTaGFyZWQgbWVtb3J5IGlzIGEgbWVtb3J5IHNwYWNlIHRoYXQgY2FuIGJlIGFjY2Vzc2VkIGJ5IGFsbCB0aHJlYWRzIGluIGEgdGhyZWFkIGJsb2NrLgotIFJlZ2lzdGVyOiBBIHJlZ2lzdGVyIGlzIGEgc21hbGwgbWVtb3J5IHNwYWNlIHRoYXQgY2FuIGJlIGFjY2Vzc2VkIGJ5IGEgc2luZ2xlIHRocmVhZC4KLSBNZW1vcnkgSGllcmFyY2h5OiBNZW1vcnkgaGllcmFyY2h5IGlzIGEgcHlyYW1pZCBvZiBtZW1vcnkgdHlwZXMgd2l0aCBkaWZmZXJlbnQgc3BlZWRzIGFuZCBzaXplcy4KLSBNZW1vcnkgQmFuZHdpZHRoOiBNZW1vcnkgYmFuZHdpZHRoIGlzIHRoZSByYXRlIGF0IHdoaWNoIGRhdGEgY2FuIGJlIHJlYWQgZnJvbSBvciBzdG9yZWQgaW50byBtZW1vcnkuCi0gQ2FjaGU6IENhY2hlIGlzIGEgc21hbGwgbWVtb3J5IHNwYWNlIHRoYXQgc3RvcmVzIGZyZXF1ZW50bHkgYWNjZXNzZWQgZGF0YS4KLSBIQk06IEhCTSBpcyBhIGhpZ2gtYmFuZHdpZHRoIG1lbW9yeSB0ZWNobm9sb2d5IHRoYXQgdXNlcyAzRC1zdGFja2VkIERSQU0uCgpIZXJlIGFyZSBzb21lIGJlc3QgcHJhY3RpY2VzIGZvciB3cml0aW5nIENVREEga2VybmVscyBvbiBHUFUKCi0gRmluZCB3YXlzIHRvIHBhcmFsbGVsaXplIHNlcXVlbnRpYWwgY29kZS4KLSBNaW5pbWl6ZSBkYXRhIHRyYW5zZmVycyBiZXR3ZWVuIHRoZSBob3N0IGFuZCB0aGUgZGV2aWNlLgotIEFkanVzdCBrZXJuZWwgbGF1bmNoIGNvbmZpZ3VyYXRpb24gdG8gbWF4aW1pemUgZGV2aWNlIHV0aWxpemF0aW9uLgotIEVuc3VyZSB0aGF0IGdsb2JhbCBtZW1vcnkgYWNjZXNzZXMgYXJlIGNvYWxlc2NlZC4KLSBNaW5pbWl6ZSByZWR1bmRhbnQgYWNjZXNzZXMgdG8gZ2xvYmFsIG1lbW9yeSB3aGVuZXZlciBwb3NzaWJsZS4KLSBBdm9pZCBsb25nIHNlcXVlbmNlcyBvZiBkaXZlcmdlZCBleGVjdXRpb24gYnkgdGhyZWFkcyB3aXRoaW4gdGhlIHNhbWUgd2FycC4KICAjV2UgYWRkZWQgdGhpcyB0byByZWZlcmVuY2UgdGhlIHNwZWNpZmljIEdQVSBhcmNoaXRlY3R1cmUKLSBVc2Ugc3BlY2lhbGl6ZWQgaW5zdHJ1Y3Rpb25zIGJhc2VkIG9uIHRoZSBzcGVjaWZpYyBHUFUgYXJjaGl0ZWN0dXJlCgpZb3UgYXJlIGdpdmVuIHRoZSBmb2xsb3dpbmcgYXJjaGl0ZWN0dXJlOgoKPFB5VG9yY2ggcmVmZXJlbmNlIGFyY2hpdGVjdHVyZSBmb3Igc3BlY2lmaWMgS2VybmVsQmVuY2ggUHJvYmxlbT4KCk5hbWUgeW91ciBuZXcgaW1wcm92ZWQgb3V0cHV0IGFyY2hpdGVjdHVyZSBNb2RlbE5ldy4gT3V0cHV0IHRoZSBuZXcgY29kZSBpbiBjb2RlYmxvY2tzLiBQbGVhc2UgZ2VuZXJhdGUgcmVhbCBjb2RlLCBOT1QgcHNldWRvY29kZSwgbWFrZSBzdXJlIHRoZSBjb2RlIGNvbXBpbGVzIGFuZCBpcyBmdWxseSBmdW5jdGlvbmFsLiBKdXN0IG91dHB1dCB0aGUgbmV3IG1vZGVsIGNvZGUsIG5vIG90aGVyIHRleHQsIGFuZCBOTyB0ZXN0aW5nIGNvZGUh)

1
<Initial Task prompt from one-shot baseline for Instruction>

2
<Initial pair of Reference PyTorch and CUDA kernel equiavlent for example add kernel from one-shot baseline for Instruction>

3

4
Here is some information about the underlying hardware that you should keep in mind.

5

6
The GPU that will run the kernel is NVIDIA <GPU NAME>.

7

8
- We have <x> GB GDDR6 with ECC of GPU Memory.

9
- We have <x> GB/s of Memory Bandwidth.

10
- We have <x> of RT Core Performance TFLOPS.

11
- We have <x> of FP32 TFLOPS.

12
- We have <x> of TF32 Tensor Core TFLOPS.

13
- We have <x> of FP16 Tensor Core TFLOPS.

14
- We have <x> of FP8 Tensor Core TFLOPS.

15
- We have <x> of Peak INT8 Tensor TOPS.

16
- We have <x> of Peak INT4 Tensor TOPS.

17
- We have <x> 32-bit registers per SM of Register File Size.

18
- We have <x> of Maximum number of registers per thread.

19
- We have <x> of Maximum number of thread blocks per SM.

20
- We have <x> KB of Shared memory capacity per SM.

21
- We have <x> KB of Maximum shared memory per thread block.

22

23

24

25
Here are some concepts about the GPU architecture that could be helpful:

26

27
- Thread: A thread is a single execution unit that can run a single instruction at a time.

28
- Thread Block: A thread block is a group of threads that can cooperate with each other.

29
- Shared Memory: Shared memory is a memory space that can be accessed by all threads in a thread block.

30
- Register: A register is a small memory space that can be accessed by a single thread.

31
- Memory Hierarchy: Memory hierarchy is a pyramid of memory types with different speeds and sizes.

32
- Memory Bandwidth: Memory bandwidth is the rate at which data can be read from or stored into memory.

33
- Cache: Cache is a small memory space that stores frequently accessed data.

34
- HBM: HBM is a high-bandwidth memory technology that uses 3D-stacked DRAM.

35

36
Here are some best practices for writing CUDA kernels on GPU

37

38
- Find ways to parallelize sequential code.

39
- Minimize data transfers between the host and the device.

40
- Adjust kernel launch configuration to maximize device utilization.

41
- Ensure that global memory accesses are coalesced.

42
- Minimize redundant accesses to global memory whenever possible.

43
- Avoid long sequences of diverged execution by threads within the same warp.

44
 #We added this to reference the specific GPU architecture

45
- Use specialized instructions based on the specific GPU architecture

46

47
You are given the following architecture:

48

49
<PyTorch reference architecture for specific KernelBench Problem>

50

51
Name your new improved output architecture ModelNew. Output the new code in codeblocks. Please generate real code, NOT pseudocode, make sure the code compiles and is fully functional. Just output the new model code, no other text, and NO testing code!

## Appendix D Kernels of Interest

In this section we provide examples of interesting or notable kernel generations. We first expand on the discussion in Section [6](#S6 "6 Discussion ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu"), where we defined the following categories of optimizations: algorithmic optimizations, operator fusion, and using hardware features.

### D.1 Algorithmic Optimizations

13x Speedup on Level 1 Problem 11 by Claude-3.5 Sonnet
  
The original torch operator is torch.diag(A) @ B, multiplying a diagonal matrix formed from the vector A with the matrix B. The model identifies an optimization in the special case of a diagonal matrix multiplication, where the diagonal matrix doesn’t need to be explicitly constructed. Instead, each element of the vector A is directly multiplied with the corresponding row in matrix B, significantly improving performance:

[⬇](data:text/plain;base64,X19nbG9iYWxfXyB2b2lkIGRpYWdfbWF0bXVsX2tlcm5lbCgKICAgIGNvbnN0IGZsb2F0KiBkaWFnLAogICAgY29uc3QgZmxvYXQqIG1hdCwKICAgIGZsb2F0KiBvdXQsCiAgICBjb25zdCBpbnQgTiwKICAgIGNvbnN0IGludCBNKSB7CgogICAgY29uc3QgaW50IHJvdyA9IGJsb2NrSWR4LnkgKiBibG9ja0RpbS55ICsgdGhyZWFkSWR4Lnk7CiAgICBjb25zdCBpbnQgY29sID0gYmxvY2tJZHgueCAqIGJsb2NrRGltLnggKyB0aHJlYWRJZHgueDsKCiAgICBpZiAocm93IDwgTiAmJiBjb2wgPCBNKSB7CiAgICAgICAgb3V0W3JvdyAqIE0gKyBjb2xdID0gZGlhZ1tyb3ddICogbWF0W3JvdyAqIE0gKyBjb2xdOwogICAgfQp9)

1
__global__ void diag_matmul_kernel(

2
 const float* diag,

3
 const float* mat,

4
 float* out,

5
 const int N,

6
 const int M) {

7

8
 const int row = blockIdx.y * blockDim.y + threadIdx.y;

9
 const int col = blockIdx.x * blockDim.x + threadIdx.x;

10

11
 if (row < N && col < M) {

12
 out[row * M + col] = diag[row] * mat[row * M + col];

13
 }

14
}

### D.2 Kernel Fusion

2.9x Speedup on Level 1 Problem 87 by DeepSeek-V3
  
GeLU reference in torch:

[⬇](data:text/plain;base64,MC41ICogeCAqICgxLjAgKyB0b3JjaC50YW5oKG1hdGguc3FydCgyLjAgLyBtYXRoLnBpKSAqICh4ICsgMC4wNDQ3MTUgKiB0b3JjaC5wb3coeCwgMy4wKSkpKQ==)

1
0.5 * x * (1.0 + torch.tanh(math.sqrt(2.0 / math.pi) * (x + 0.044715 * torch.pow(x, 3.0))))

Optimized version fuses in a single kernel. There is also a small constant folding optimization, instead of computing math.sqrt(2.0 / math.pi) repeatedly, the kernel uses the precomputed value 0.7978845608028654f:

[⬇](data:text/plain;base64,X19nbG9iYWxfXyB2b2lkIGdlbHVfa2VybmVsKGNvbnN0IGZsb2F0KiB4LCBmbG9hdCogb3V0LCBpbnQgc2l6ZSkgewogICAgaW50IGlkeCA9IGJsb2NrSWR4LnggKiBibG9ja0RpbS54ICsgdGhyZWFkSWR4Lng7CiAgICBpZiAoaWR4IDwgc2l6ZSkgewogICAgICAgIGZsb2F0IHhfdmFsID0geFtpZHhdOwogICAgICAgIGZsb2F0IGNkZiA9IDAuNWYgKiAoMS4wZiArIHRhbmhmKCgwLjc5Nzg4NDU2MDgwMjg2NTRmICogKHhfdmFsICsgMC4wNDQ3MTVmICogeF92YWwgKiB4X3ZhbCAqIHhfdmFsKSkpKTsKICAgICAgICBvdXRbaWR4XSA9IHhfdmFsICogY2RmOwogICAgfQp9)

1
__global__ void gelu_kernel(const float* x, float* out, int size) {

2
 int idx = blockIdx.x * blockDim.x + threadIdx.x;

3
 if (idx < size) {

4
 float x_val = x[idx];

5
 float cdf = 0.5f * (1.0f + tanhf((0.7978845608028654f * (x_val + 0.044715f * x_val * x_val * x_val))));

6
 out[idx] = x_val * cdf;

7
 }

8
}

1.3x Speedup on Level 1 Problem 29 by Claude-3.5 Sonnet
  
SoftSign reference in torch:

[⬇](data:text/plain;base64,eCAvICgxICsgdG9yY2guYWJzKHgpKQ==)

1
x / (1 + torch.abs(x))

Fused kernel:

[⬇](data:text/plain;base64,X19nbG9iYWxfXyB2b2lkIHNvZnRzaWduX2tlcm5lbChjb25zdCBmbG9hdCogaW5wdXQsIGZsb2F0KiBvdXRwdXQsIGludCBzaXplKSB7CiAgICBpbnQgaWR4ID0gYmxvY2tJZHgueCAqIGJsb2NrRGltLnggKyB0aHJlYWRJZHgueDsKICAgIGlmIChpZHggPCBzaXplKSB7CiAgICAgICAgZmxvYXQgeCA9IGlucHV0W2lkeF07CiAgICAgICAgZmxvYXQgYWJzX3ggPSBhYnMoeCk7CiAgICAgICAgb3V0cHV0W2lkeF0gPSB4IC8gKDEuMGYgKyBhYnNfeCk7CiAgICB9Cn0=)

1
__global__ void softsign_kernel(const float* input, float* output, int size) {

2
 int idx = blockIdx.x * blockDim.x + threadIdx.x;

3
 if (idx < size) {

4
 float x = input[idx];

5
 float abs_x = abs(x);

6
 output[idx] = x / (1.0f + abs_x);

7
 }

8
}

2.6x Speedup on Level 2 Problem 13 by Claude-3.5 Sonnet
  
Sequence of operators in torch:

[⬇](data:text/plain;base64,eCA9IHRvcmNoLm1hdG11bCh4LCBzZWxmLndlaWdodC5UKSAgIyBHZW1tCnggPSB4IC8gMiAgIyBEaXZpZGUKeCA9IHRvcmNoLnN1bSh4LCBkaW09MSwga2VlcGRpbT1UcnVlKSAjIFN1bQp4ID0geCAqIHNlbGYuc2NhbGluZ19mYWN0b3IgICMgU2NhbGluZw==)

1
x = torch.matmul(x, self.weight.T) # Gemm

2
x = x / 2 # Divide

3
x = torch.sum(x, dim=1, keepdim=True) # Sum

4
x = x * self.scaling_factor # Scaling

Fused kernel:

[⬇](data:text/plain;base64,X19nbG9iYWxfXyB2b2lkIGZ1c2VkX29wc19rZXJuZWwoCiAgICBjb25zdCBmbG9hdCogaW5wdXQsCiAgICBjb25zdCBmbG9hdCogd2VpZ2h0LAogICAgZmxvYXQqIG91dHB1dCwKICAgIGNvbnN0IGZsb2F0IHNjYWxpbmdfZmFjdG9yLAogICAgY29uc3QgaW50IGJhdGNoX3NpemUsCiAgICBjb25zdCBpbnQgaW5wdXRfc2l6ZSwKICAgIGNvbnN0IGludCBoaWRkZW5fc2l6ZQopIHsKICAgIC8vIEVhY2ggdGhyZWFkIGhhbmRsZXMgb25lIGVsZW1lbnQgaW4gdGhlIGJhdGNoCiAgICBjb25zdCBpbnQgYmF0Y2hfaWR4ID0gYmxvY2tJZHgueCAqIGJsb2NrRGltLnggKyB0aHJlYWRJZHgueDsKCiAgICBpZiAoYmF0Y2hfaWR4IDwgYmF0Y2hfc2l6ZSkgewogICAgICAgIGZsb2F0IHN1bSA9IDAuMGY7CgogICAgICAgIC8vIENvbXB1dGUgbWF0bXVsIGFuZCBkaXZpZGUgZm9yIHRoaXMgYmF0Y2ggZWxlbWVudAogICAgICAgIGZvcihpbnQgaCA9IDA7IGggPCBoaWRkZW5fc2l6ZTsgaCsrKSB7CiAgICAgICAgICAgIGZsb2F0IGVsZW0gPSAwLjBmOwogICAgICAgICAgICBmb3IoaW50IGkgPSAwOyBpIDwgaW5wdXRfc2l6ZTsgaSsrKSB7CiAgICAgICAgICAgICAgICBlbGVtICs9IGlucHV0W2JhdGNoX2lkeCAqIGlucHV0X3NpemUgKyBpXSAqCiAgICAgICAgICAgICAgICAgICAgICAgIHdlaWdodFtoICogaW5wdXRfc2l6ZSArIGldOwogICAgICAgICAgICB9CiAgICAgICAgICAgIC8vIERpdmlkZSBieSAyIGFzIHdlIGdvCiAgICAgICAgICAgIHN1bSArPSAoZWxlbSAvIDIuMGYpOwogICAgICAgIH0KCiAgICAgICAgLy8gU2NhbGUgYW5kIHN0b3JlIGZpbmFsIHJlc3VsdAogICAgICAgIG91dHB1dFtiYXRjaF9pZHhdID0gc3VtICogc2NhbGluZ19mYWN0b3I7CiAgICB9Cn0=)

1
__global__ void fused_ops_kernel(

2
 const float* input,

3
 const float* weight,

4
 float* output,

5
 const float scaling_factor,

6
 const int batch_size,

7
 const int input_size,

8
 const int hidden_size

9
) {

10
 // Each thread handles one element in the batch

11
 const int batch_idx = blockIdx.x * blockDim.x + threadIdx.x;

12

13
 if (batch_idx < batch_size) {

14
 float sum = 0.0f;

15

16
 // Compute matmul and divide for this batch element

17
 for(int h = 0; h < hidden_size; h++) {

18
 float elem = 0.0f;

19
 for(int i = 0; i < input_size; i++) {

20
 elem += input[batch_idx * input_size + i] *

21
 weight[h * input_size + i];

22
 }

23
 // Divide by 2 as we go

24
 sum += (elem / 2.0f);

25
 }

26

27
 // Scale and store final result

28
 output[batch_idx] = sum * scaling_factor;

29
 }

30
}

Despite this good example, overall Level 2 generated kernels show insufficient fusion. It is expected that most Level 2 problems can be expressed in a single fused kernel.
  
  
1.9x Speedup on Level 3 Problem 49 by OpenAI-o1
  
We have a hypothetical architecture of the attention mechanism where the softmax is replaced with a ReLU.

[⬇](data:text/plain;base64,ICAgIGF0dCA9IChxIEAgay50cmFuc3Bvc2UoLTIsIC0xKSkgKiAoMS4wIC8gbWF0aC5zcXJ0KGsuc2l6ZSgtMSkpKQogICAgYXR0ID0gYXR0Lm1hc2tlZF9maWxsKHNlbGYuYmlhc1s6LDosOlQsOlRdID09IDAsIGZsb2F0KCctaW5mJykpCiAgICBhdHQgPSBGLnJlbHUoYXR0KQ==)

1
 att = (q @ k.transpose(-2, -1)) * (1.0 / math.sqrt(k.size(-1)))

2
 att = att.masked_fill(self.bias[:,:,:T,:T] == 0, float(’-inf’))

3
 att = F.relu(att)

The model found an optimization that fuses the scaling, masked fill, and ReLU but not anything else, resulting in a modest improvement of 1.9x.

[⬇](data:text/plain;base64,X19nbG9iYWxfXyB2b2lkIGZ1c2VkX21hc2tlZF9maWxsX3NjYWxlX3JlbHVfa2VybmVsKAogICAgY29uc3QgZmxvYXQqIF9fcmVzdHJpY3RfXyBhdHQsCiAgICBjb25zdCBmbG9hdCogX19yZXN0cmljdF9fIGJpYXMsCiAgICBmbG9hdCogX19yZXN0cmljdF9fIG91dHB1dCwKICAgIGludCB0b3RhbF9lbGVtcywKICAgIGZsb2F0IHNjYWxlLAogICAgaW50IFQsCiAgICBmbG9hdCBuZWdhdGl2ZV9pbmZpbml0eQopIHsKICAgIGludCBpZHggPSBibG9ja0lkeC54ICogYmxvY2tEaW0ueCArIHRocmVhZElkeC54OwogICAgaWYgKGlkeCA8IHRvdGFsX2VsZW1zKSB7CiAgICAgICAgZmxvYXQgdmFsID0gYXR0W2lkeF0gKiBzY2FsZTsKICAgICAgICBpbnQgYmlhc19pZHggPSBpZHggJSAoVCAqIFQpOwogICAgICAgIGlmIChiaWFzW2JpYXNfaWR4XSA9PSAwLjBmKSB7CiAgICAgICAgICAgIHZhbCA9IG5lZ2F0aXZlX2luZmluaXR5OwogICAgICAgIH0KICAgICAgICBpZiAodmFsIDwgMC4wZikgewogICAgICAgICAgICB2YWwgPSAwLjBmOwogICAgICAgIH0KICAgICAgICBvdXRwdXRbaWR4XSA9IHZhbDsKICAgIH0KfQ==)

1
__global__ void fused_masked_fill_scale_relu_kernel(

2
 const float* __restrict__ att,

3
 const float* __restrict__ bias,

4
 float* __restrict__ output,

5
 int total_elems,

6
 float scale,

7
 int T,

8
 float negative_infinity

9
) {

10
 int idx = blockIdx.x * blockDim.x + threadIdx.x;

11
 if (idx < total_elems) {

12
 float val = att[idx] * scale;

13
 int bias_idx = idx % (T * T);

14
 if (bias[bias_idx] == 0.0f) {

15
 val = negative_infinity;

16
 }

17
 if (val < 0.0f) {

18
 val = 0.0f;

19
 }

20
 output[idx] = val;

21
 }

22
}

### D.3 Hardware Features

2.8x Speedup on Level 1 Problem 96 by OpenAI-o1
  
Torch reference for Cosine Similarity Loss

[⬇](data:text/plain;base64,Y29zaW5lX3NpbSA9IHRvcmNoLm5uLmZ1bmN0aW9uYWwuY29zaW5lX3NpbWlsYXJpdHkocHJlZGljdGlvbnMsIHRhcmdldHMsIGRpbT0xKQpyZXR1cm4gdG9yY2gubWVhbigxIC0gY29zaW5lX3NpbSk=)

1
cosine_sim = torch.nn.functional.cosine_similarity(predictions, targets, dim=1)

2
return torch.mean(1 - cosine_sim)

The generated kernel uses shared memory for reduce redundant global memory accesses, improving data locality and increasing overall performance. This is a moderately complicated kernel with synchronization points and reductions that would be tricky for humans to get right.

[⬇](data:text/plain;base64,X19nbG9iYWxfXyB2b2lkIGNvc2luZV9zaW1pbGFyaXR5X2xvc3Nfa2VybmVsKAogICAgY29uc3QgZmxvYXQqIF9fcmVzdHJpY3RfXyBwcmVkaWN0aW9ucywKICAgIGNvbnN0IGZsb2F0KiBfX3Jlc3RyaWN0X18gdGFyZ2V0cywKICAgIGZsb2F0KiBfX3Jlc3RyaWN0X18gbG9zc2VzLAogICAgY29uc3QgaW50IGJhdGNoX3NpemUsCiAgICBjb25zdCBpbnQgaW5wdXRfc2l6ZQopIHsKICAgIC8vIEVhY2ggYmxvY2sgaGFuZGxlcyBvbmUgc2FtcGxlIGluIHRoZSBiYXRjaAogICAgaW50IHNhbXBsZV9pZHggPSBibG9ja0lkeC54OwogICAgaWYgKHNhbXBsZV9pZHggPj0gYmF0Y2hfc2l6ZSkgcmV0dXJuOwoKICAgIC8vIFNoYXJlZCBtZW1vcnkgZm9yIHJlZHVjdGlvbnMKICAgIGV4dGVybiBfX3NoYXJlZF9fIGZsb2F0IHNkYXRhW107CgogICAgLy8gUG9pbnRlcnMgdG8gZGF0YSBmb3IgdGhpcyBzYW1wbGUKICAgIGNvbnN0IGZsb2F0KiBwcmVkID0gcHJlZGljdGlvbnMgKyBzYW1wbGVfaWR4ICogaW5wdXRfc2l6ZTsKICAgIGNvbnN0IGZsb2F0KiB0YXJnID0gdGFyZ2V0cyArIHNhbXBsZV9pZHggKiBpbnB1dF9zaXplOwoKICAgIC8vIEludGVybWVkaWF0ZSBzdW1zIGZvciBkb3QgcHJvZHVjdCBhbmQgbm9ybXMKICAgIGZsb2F0IHRocmVhZF9kb3QgPSAwLjBmOwogICAgZmxvYXQgdGhyZWFkX3ByZWRfbm9ybV9zcSA9IDAuMGY7CiAgICBmbG9hdCB0aHJlYWRfdGFyZ19ub3JtX3NxID0gMC4wZjsKCiAgICBmb3IgKGludCBpZHggPSB0aHJlYWRJZHgueDsgaWR4IDwgaW5wdXRfc2l6ZTsgaWR4ICs9IGJsb2NrRGltLngpIHsKICAgICAgICBmbG9hdCBwID0gcHJlZFtpZHhdOwogICAgICAgIGZsb2F0IHQgPSB0YXJnW2lkeF07CiAgICAgICAgdGhyZWFkX2RvdCArPSBwICogdDsKICAgICAgICB0aHJlYWRfcHJlZF9ub3JtX3NxICs9IHAgKiBwOwogICAgICAgIHRocmVhZF90YXJnX25vcm1fc3EgKz0gdCAqIHQ7CiAgICB9CgogICAgLy8gUmVkdWN0aW9uIGZvciBkb3QgcHJvZHVjdAogICAgc2RhdGFbdGhyZWFkSWR4LnhdID0gdGhyZWFkX2RvdDsKICAgIF9fc3luY3RocmVhZHMoKTsKICAgIGZvciAodW5zaWduZWQgaW50IHMgPSBibG9ja0RpbS54IC8gMjsgcyA+IDA7IHMgPj49IDEpIHsKICAgICAgICBpZiAodGhyZWFkSWR4LnggPCBzKSB7CiAgICAgICAgICAgIHNkYXRhW3RocmVhZElkeC54XSArPSBzZGF0YVt0aHJlYWRJZHgueCArIHNdOwogICAgICAgIH0KICAgICAgICBfX3N5bmN0aHJlYWRzKCk7CiAgICB9CiAgICBmbG9hdCBkb3RfcHJvZHVjdCA9IHNkYXRhWzBdOwoKICAgIC8vIFJlZHVjdGlvbiBmb3IgcHJlZF9ub3JtX3NxCiAgICBzZGF0YVt0aHJlYWRJZHgueF0gPSB0aHJlYWRfcHJlZF9ub3JtX3NxOwogICAgX19zeW5jdGhyZWFkcygpOwogICAgZm9yICh1bnNpZ25lZCBpbnQgcyA9IGJsb2NrRGltLnggLyAyOyBzID4gMDsgcyA+Pj0gMSkgewogICAgICAgIGlmICh0aHJlYWRJZHgueCA8IHMpIHsKICAgICAgICAgICAgc2RhdGFbdGhyZWFkSWR4LnhdICs9IHNkYXRhW3RocmVhZElkeC54ICsgc107CiAgICAgICAgfQogICAgICAgIF9fc3luY3RocmVhZHMoKTsKICAgIH0KICAgIGZsb2F0IG5vcm1fcHJlZCA9IHNxcnRmKHNkYXRhWzBdICsgMWUtOGYpOwoKICAgIC8vIFJlZHVjdGlvbiBmb3IgdGFyZ19ub3JtX3NxCiAgICBzZGF0YVt0aHJlYWRJZHgueF0gPSB0aHJlYWRfdGFyZ19ub3JtX3NxOwogICAgX19zeW5jdGhyZWFkcygpOwogICAgZm9yICh1bnNpZ25lZCBpbnQgcyA9IGJsb2NrRGltLnggLyAyOyBzID4gMDsgcyA+Pj0gMSkgewogICAgICAgIGlmICh0aHJlYWRJZHgueCA8IHMpIHsKICAgICAgICAgICAgc2RhdGFbdGhyZWFkSWR4LnhdICs9IHNkYXRhW3RocmVhZElkeC54ICsgc107CiAgICAgICAgfQogICAgICAgIF9fc3luY3RocmVhZHMoKTsKICAgIH0KICAgIGZsb2F0IG5vcm1fdGFyZyA9IHNxcnRmKHNkYXRhWzBdICsgMWUtOGYpOwoKICAgIGlmICh0aHJlYWRJZHgueCA9PSAwKSB7CiAgICAgICAgZmxvYXQgY29zaW5lX3NpbSA9IGRvdF9wcm9kdWN0IC8gKG5vcm1fcHJlZCAqIG5vcm1fdGFyZyArIDFlLThmKTsKICAgICAgICBsb3NzZXNbc2FtcGxlX2lkeF0gPSAxLjBmIC0gY29zaW5lX3NpbTsKICAgIH0KfQ==)

1
__global__ void cosine_similarity_loss_kernel(

2
 const float* __restrict__ predictions,

3
 const float* __restrict__ targets,

4
 float* __restrict__ losses,

5
 const int batch_size,

6
 const int input_size

7
) {

8
 // Each block handles one sample in the batch

9
 int sample_idx = blockIdx.x;

10
 if (sample_idx >= batch_size) return;

11

12
 // Shared memory for reductions

13
 extern __shared__ float sdata[];

14

15
 // Pointers to data for this sample

16
 const float* pred = predictions + sample_idx * input_size;

17
 const float* targ = targets + sample_idx * input_size;

18

19
 // Intermediate sums for dot product and norms

20
 float thread_dot = 0.0f;

21
 float thread_pred_norm_sq = 0.0f;

22
 float thread_targ_norm_sq = 0.0f;

23

24
 for (int idx = threadIdx.x; idx < input_size; idx += blockDim.x) {

25
 float p = pred[idx];

26
 float t = targ[idx];

27
 thread_dot += p * t;

28
 thread_pred_norm_sq += p * p;

29
 thread_targ_norm_sq += t * t;

30
 }

31

32
 // Reduction for dot product

33
 sdata[threadIdx.x] = thread_dot;

34
 __syncthreads();

35
 for (unsigned int s = blockDim.x / 2; s > 0; s >>= 1) {

36
 if (threadIdx.x < s) {

37
 sdata[threadIdx.x] += sdata[threadIdx.x + s];

38
 }

39
 __syncthreads();

40
 }

41
 float dot_product = sdata[0];

42

43
 // Reduction for pred_norm_sq

44
 sdata[threadIdx.x] = thread_pred_norm_sq;

45
 __syncthreads();

46
 for (unsigned int s = blockDim.x / 2; s > 0; s >>= 1) {

47
 if (threadIdx.x < s) {

48
 sdata[threadIdx.x] += sdata[threadIdx.x + s];

49
 }

50
 __syncthreads();

51
 }

52
 float norm_pred = sqrtf(sdata[0] + 1e-8f);

53

54
 // Reduction for targ_norm_sq

55
 sdata[threadIdx.x] = thread_targ_norm_sq;

56
 __syncthreads();

57
 for (unsigned int s = blockDim.x / 2; s > 0; s >>= 1) {

58
 if (threadIdx.x < s) {

59
 sdata[threadIdx.x] += sdata[threadIdx.x + s];

60
 }

61
 __syncthreads();

62
 }

63
 float norm_targ = sqrtf(sdata[0] + 1e-8f);

64

65
 if (threadIdx.x == 0) {

66
 float cosine_sim = dot_product / (norm_pred * norm_targ + 1e-8f);

67
 losses[sample_idx] = 1.0f - cosine_sim;

68
 }

69
}

1.9x Speedup on Level 1 Problem 98 by Deepseek-R1
  
Torch reference for Cosine Similarity Loss

[⬇](data:text/plain;base64,c2VsZi5sb3NzX2ZuID0gdG9yY2gubm4uVHJpcGxldE1hcmdpbkxvc3MobWFyZ2luPW1hcmdpbikKc2VsZi5sb3NzX2ZuKGFuY2hvciwgcG9zaXRpdmUsIG5lZ2F0aXZlKQ==)

1
self.loss_fn = torch.nn.TripletMarginLoss(margin=margin)

2
self.loss_fn(anchor, positive, negative)

Another example of a generated kernel using shared memory:

[⬇](data:text/plain;base64,X19nbG9iYWxfXyB2b2lkIHRyaXBsZXRfbWFyZ2luX2xvc3Nfa2VybmVsKAogICAgY29uc3QgZmxvYXQqIGFuY2hvciwKICAgIGNvbnN0IGZsb2F0KiBwb3NpdGl2ZSwKICAgIGNvbnN0IGZsb2F0KiBuZWdhdGl2ZSwKICAgIGZsb2F0KiBsb3NzZXMsCiAgICBmbG9hdCBtYXJnaW4sCiAgICBpbnQgZmVhdHVyZV9zaXplKQp7CiAgICBleHRlcm4gX19zaGFyZWRfXyBmbG9hdCBzaGFyZWRfc3Vtc1tdOwoKICAgIGludCBiYXRjaF9pZHggPSBibG9ja0lkeC54OwogICAgaW50IHRpZCA9IHRocmVhZElkeC54OwoKICAgIGludCBvZmZzZXQgPSBiYXRjaF9pZHggKiBmZWF0dXJlX3NpemU7CgogICAgY29uc3QgZmxvYXQqIGEgPSBhbmNob3IgKyBvZmZzZXQ7CiAgICBjb25zdCBmbG9hdCogcCA9IHBvc2l0aXZlICsgb2Zmc2V0OwogICAgY29uc3QgZmxvYXQqIG4gPSBuZWdhdGl2ZSArIG9mZnNldDsKCiAgICBmbG9hdCBhX3Bfc3VtID0gMC4wZjsKICAgIGZsb2F0IGFfbl9zdW0gPSAwLjBmOwoKICAgIGludCBzdHJpZGUgPSBibG9ja0RpbS54OwogICAgZm9yIChpbnQgaSA9IHRpZDsgaSA8IGZlYXR1cmVfc2l6ZTsgaSArPSBzdHJpZGUpIHsKICAgICAgICBmbG9hdCBkaWZmX2FwID0gYVtpXSAtIHBbaV07CiAgICAgICAgYV9wX3N1bSArPSBkaWZmX2FwICogZGlmZl9hcDsKICAgICAgICBmbG9hdCBkaWZmX2FuID0gYVtpXSAtIG5baV07CiAgICAgICAgYV9uX3N1bSArPSBkaWZmX2FuICogZGlmZl9hbjsKICAgIH0KCiAgICBzaGFyZWRfc3Vtc1t0aWRdID0gYV9wX3N1bTsKICAgIHNoYXJlZF9zdW1zW2Jsb2NrRGltLnggKyB0aWRdID0gYV9uX3N1bTsKCiAgICBfX3N5bmN0aHJlYWRzKCk7CgogICAgZm9yIChpbnQgcyA9IGJsb2NrRGltLnggLyAyOyBzID4gMDsgcyA+Pj0gMSkgewogICAgICAgIGlmICh0aWQgPCBzKSB7CiAgICAgICAgICAgIHNoYXJlZF9zdW1zW3RpZF0gKz0gc2hhcmVkX3N1bXNbdGlkICsgc107CiAgICAgICAgICAgIHNoYXJlZF9zdW1zW2Jsb2NrRGltLnggKyB0aWRdICs9IHNoYXJlZF9zdW1zW2Jsb2NrRGltLnggKyB0aWQgKyBzXTsKICAgICAgICB9CiAgICAgICAgX19zeW5jdGhyZWFkcygpOwogICAgfQoKICAgIGlmICh0aWQgPT0gMCkgewogICAgICAgIGZsb2F0IGRfYXAgPSBzcXJ0ZihzaGFyZWRfc3Vtc1swXSk7CiAgICAgICAgZmxvYXQgZF9hbiA9IHNxcnRmKHNoYXJlZF9zdW1zW2Jsb2NrRGltLnhdKTsKICAgICAgICBsb3NzZXNbYmF0Y2hfaWR4XSA9IGZtYXhmKGRfYXAgLSBkX2FuICsgbWFyZ2luLCAwLjBmKTsKICAgIH0KfQ==)

1
__global__ void triplet_margin_loss_kernel(

2
 const float* anchor,

3
 const float* positive,

4
 const float* negative,

5
 float* losses,

6
 float margin,

7
 int feature_size)

8
{

9
 extern __shared__ float shared_sums[];

10

11
 int batch_idx = blockIdx.x;

12
 int tid = threadIdx.x;

13

14
 int offset = batch_idx * feature_size;

15

16
 const float* a = anchor + offset;

17
 const float* p = positive + offset;

18
 const float* n = negative + offset;

19

20
 float a_p_sum = 0.0f;

21
 float a_n_sum = 0.0f;

22

23
 int stride = blockDim.x;

24
 for (int i = tid; i < feature_size; i += stride) {

25
 float diff_ap = a[i] - p[i];

26
 a_p_sum += diff_ap * diff_ap;

27
 float diff_an = a[i] - n[i];

28
 a_n_sum += diff_an * diff_an;

29
 }

30

31
 shared_sums[tid] = a_p_sum;

32
 shared_sums[blockDim.x + tid] = a_n_sum;

33

34
 __syncthreads();

35

36
 for (int s = blockDim.x / 2; s > 0; s >>= 1) {

37
 if (tid < s) {

38
 shared_sums[tid] += shared_sums[tid + s];

39
 shared_sums[blockDim.x + tid] += shared_sums[blockDim.x + tid + s];

40
 }

41
 __syncthreads();

42
 }

43

44
 if (tid == 0) {

45
 float d_ap = sqrtf(shared_sums[0]);

46
 float d_an = sqrtf(shared_sums[blockDim.x]);

47
 losses[batch_idx] = fmaxf(d_ap - d_an + margin, 0.0f);

48
 }

49
}

### D.4 Iterative Refinement Examples

#### D.4.1 Iteratively Trying new Optimizations

We provide an example of a kernel that iteratively improves on its existing generation. In the following example, the model attempts new optimizations incorrectly, fixes them, and continue to attempt new optimizations, improving its kernel to faster than the torch.compile baseline (1.341.34ms) but short of the Torch Eager baseline (0.470.47ms).
  
  
Level 1, Problem 63: 2D convolution with square input and square kernel. DeepSeek-R1 with Execution and Profile Feedback

|  |  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Turn # | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
| Compiles? | ✓\checkmark | ✗ | ✓\checkmark | ✗ | ✓\checkmark | ✓\checkmark | ✗ | ✓\checkmark | ✗ | ✓\checkmark |
| Correct? | ✓\checkmark | ✗ | ✓\checkmark | ✗ | ✓\checkmark | ✓\checkmark | ✗ | ✓\checkmark | ✗ | ✓\checkmark |
| Runtime (ms) | 9.1 | - | 1.57 | - | 1.83 | 1.43 | - | 1.13 | - | 1.46 |

Table 4: Iterative refinement trajectory of DeepSeek-R1 with execution feedback EE and profiler feedback PP on Problem 63, Level 1. Torch Eager baseline runs in 0.470.47ms and torch.compile runs in 1.341.34ms.

In this example, we see a 8×8\times speedup in average kernel runtime from its initial generation, where the model repeatedly (incorrectly) refines its kernel, fixes the compiler issues using feedback, then continues to attempt more optimizations. The first big jump in performance (Turn 1→Turn 3)(\text{Turn 1}\rightarrow\text{Turn 3}) occurs because the model decides to launch thread blocks along an output channel dimension, when it originally computed these elements sequentially. The model then attempts to use shared memory in Turn 5, and continues using it, along with texture cache memory with the __ldg instruction in Turns 7 and 8.

#### D.4.2 Leveraging Feedback to Correct Kernel Code

Level 2, Problem 73: 2D Convolution with a BatchNorm and a scale factor. DeepSeek-R1 with Execution Feedback

We provide an example of a kernel that the model struggles to generate correctly, and produces a correct kernel after iterative refinement using execution feedback.

|  |  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Turn # | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
| Compiles? | ✓\checkmark | ✓\checkmark | ✓\checkmark | ✓\checkmark | ✓\checkmark | ✓\checkmark | ✓\checkmark | ✓\checkmark | ✓\checkmark | ✓\checkmark |
| Correct? | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✓\checkmark |
| Runtime | - | - | - | - | - | - | - | - | - | 3.16 |

Table 5: Iterative refinement trajectory of DeepSeek-R1 with execution feedback EE on Problem 73, Level 2. Torch Eager baseline runs in 0.1050.105ms and torch.compile runs in 0.1560.156ms.

In the above example, the model continually produces either the wrong output tensor shape or the wrong values and iterates on its kernel using this feedback until the final turn, where it generates a functionally correct, albeit non-performant kernel. We provide another example below that explicitly leverages compiler feedback to fix compiler errors:
  
  
Level 2, Problem 23: 3D Convolution with a GroupNorm and return the mean across all but the batch dimension. DeepSeek-R1 with Execution Feedback

|  |  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Turn # | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
| Compiles? | ✓\checkmark | ✓\checkmark | ✓\checkmark | ✓\checkmark | ✗ | ✗ | ✓\checkmark | ✓\checkmark | ✗ | ✓\checkmark |
| Correct? | ✗ | ✗ | ✓\checkmark | ✓\checkmark | ✗ | ✗ | ✓\checkmark | ✓\checkmark | ✗ | ✗ |
| Runtime | - | - | 11.4 | 1.36 | - | - | 1.39 | 1.33 | - | - |

Table 6: Iterative refinement trajectory of DeepSeek-R1 with execution feedback EE on Problem 23, Level 2. Torch Eager baseline runs in 1.291.29ms and torch.compile runs in 0.7190.719ms.

In this example, the model attempts to use the CUB library, but incorrectly invokes function calls. The model is then able to correct these errors and write a slightly faster kernel in Turn 8 (see Table [6](#A4.T6 "Table 6 ‣ D.4.2 Leveraging Feedback to Correct Kernel Code ‣ D.4 Iterative Refinement Examples ‣ Appendix D Kernels of Interest ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu")).

#### D.4.3 Iterative Refinement Never Fixes the Error

Level 1, Problem 54: 3D Convolution square input and square kernel. DeepSeek-R1 with Execution and Profiler Feedback

|  |  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Turn # | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
| Compiles? | ✓\checkmark | ✓\checkmark | ✓\checkmark | ✓\checkmark | ✓\checkmark | ✓\checkmark | ✓\checkmark | ✓\checkmark | ✓\checkmark | ✓\checkmark |
| Correct? | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Runtime | - | - | - | - | - | - | - | - | - | - |

Table 7: Iterative refinement trajectory of DeepSeek-R1 with execution feedback EE and profiler feedback PP on Problem 54, Level 1. Torch Eager baseline runs in 4.474.47ms and torch.compile runs in 4.674.67ms.

This problem is particularly interesting because no model is able to consistently produce functional code for this kernel, even with different forms of feedback and profiling information. Interestingly, the example before is an arguably more difficult version of this kernel that fuses the 3D convolution with another operator, and the same model is able to generate functional code for this task. In the example above, the model consistently makes the same mistake and continually generates a functionally incorrect kernel with the same value errors.

## Appendix E Iterative Refinement on Correctness

Here we show that fast0\text{fast}_{0} across iterative refinement(Section [5.1.2](#S5.SS1.SSS2 "5.1.2 Iterative Refinement of Generations ‣ 5.1 Case Study: Leveraging the KernelBench Environment Feedback at Test-Time ‣ 5 Analysis of Model Capabilities ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu")) configurations at a turn budget of N=10N=10 compared to one-shot baseline (Section [4.1](#S4.SS1 "4.1 One-shot Baseline ‣ 4 KernelBench Baseline Evaluation ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu")). We find that models self-correct more effectively with execution feedback EE, fixing issues especially related to execution errors. Notably, DeepSeek-R1 on Level 1 and 2 can generate a functional kernel on >90% of the tasks given 1010 turns of iterative refinement. However, the remaining incorrect kernels almost always fail due to functional incorrectness, likely because correctness feedback is less granular than execution failure messages.

|  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Method | Level 1 | | | Level 2 | | | Level 3 | | |
| Llama-3.1 | DeepSeek | Deepseek | Llama-3.1 | Deepseek | Deepseek | Llama-3.1 | Deepseek | Deepseek |
| 70B | V3 | R1 | 70B | V3 | R1 | 70B | V3 | R1 |
| Single Attempt (Baseline) | 26% | 43% | 67% | 0% | 6% | 62% | 0% | 30% | 8% |
| Iterative Refinement (w G) | 27% | 48% | 72% | 2% | 7% | 67% | 0% | 36% | 14% |
| Iterative Refinement (w G+E) | 40% | 53% | 95% | 7% | 8% | 85% | 18% | 42% | 50% |
| Iterative Refinement (w G+E+P) | 36% | 50% | 95% | 7% | 9% | 92% | 8% | 44% | 42% |

Table 8: Leveraging execution feedback helps reduce errors: Here we present the percentage of problems where the LM-generated Kernel is correct for iterative refinement. We note leveraging execution feedback helps the model achieve better correctness fast0\text{fast}_{0}, which is the percentage of problems where the model has at least one correct generation up to turn N=10N=10. We note the various iterative refinement configurations, leveraging previous Generation GG, Execution Result EE, and Timing Profiles PP.

## Appendix F Few Shot Experiment

For this experiment, we provide in-context examples of optimization techniques such as fusion, tiling, recompute, and asynchrony to models during kernel generation. As described in Section [5.2.1](#S5.SS2.SSS1 "5.2.1 Hardware-aware In-Context Examples ‣ 5.2 Case Study: Generating Hardware-Efficient Kernels via Hardware Knowledge ‣ 5 Analysis of Model Capabilities ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu"), we provide three in-context examples: a fused GELU  [[13](#bib.bib13)], a tiled matrix multiplication  [[20](#bib.bib20)], and a minimal Flash-Attention  [[8](#bib.bib8), [15](#bib.bib15)] demonstrating effective shared memory I/O management. The prompt used for this experiment is described in Appendix [C.4](#A3.SS4 "C.4 Few-Shot in Context Prompts ‣ Appendix C Experiment Prompting Details ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu"). The speedup of these kernels were computed over PyTorch Eager. We compare the performance of these few-shot kernels over the one-shot baseline below.

|  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  | | Baseline | | | Few-Shot | | |
| Model | Level | fast1\text{fast}_{1} | fast0\text{fast}_{0} | Length (chars) | fast1\text{fast}_{1} | fast0\text{fast}_{0} | Length (chars) |
|  | 1 | 3% | 27% | 301018 | 6% | 27% | 360212 |
| Llama 3.1-70B | 2 | 0% | 0% | 646403 | 0% | 0% | 566668 |
|  | 3 | 0% | 0% | 404596 | 0% | 4% | 485332 |
|  | 1 | 10% | 55% | 343995 | 6% | 39% | 437768 |
| OpenAI o1 | 2 | 24% | 56% | 381474 | 16% | 39% | 432800 |
|  | 3 | 12% | 56% | 260273 | 8% | 22% | 364551 |

Table 9: Comparison of the Section [4.1](#S4.SS1 "4.1 One-shot Baseline ‣ 4 KernelBench Baseline Evaluation ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu") baseline and few-shot prompting performance across models. We examine the fast0\text{fast}_{0}, fast1\text{fast}_{1}, and cumulative character length of generated kernels per level.

77% of matrix multiplication problems in Level 1 achieves a speedup over the one-shot baseline through tiling. The runtime comparison for each GEMM variant is presented below.

|  |  |  |  |
| --- | --- | --- | --- |
| Problem Name | Baseline (ms) | Few-Shot (ms) | Ref Torch (ms) |
| 3D Tensor Matrix Multiplication | 20.9 | 7.71 | 1.45 |
| Matmul for Upper-Triangular Matrices | 14 | 5.39 | 2.98 |
| Matrix Scalar Multiplication | 1.19 | 0.811 | 0.822 |
| Standard Matrix Multiplication | 3.39 | 2.46 | 0.397 |
| Matmul with Transposed Both | 3.44 | 2.67 | 0.412 |
| Matmul with Transposed A | 3.61 | 2.99 | 0.384 |
| 4D Tensor Matrix Multiplication | 366 | 338 | 36 |
| Tall Skinny Matrix Multiplication | 3.39 | 3.59 | 1.9 |
| Matmul with Diagonal Matrices | 0.221 | 0.237 | 2.83 |

Table 10: Performance comparison of the Section [4.1](#S4.SS1 "4.1 One-shot Baseline ‣ 4 KernelBench Baseline Evaluation ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu") baseline and few-shot prompting in level 1 matrix multiplication problems.

Few-shot kernels generated for the following problems in level 2 outperformed PyTorch Eager through aggressive shared memory I/O management.

|  |  |  |  |
| --- | --- | --- | --- |
| Problem Name | Baseline (ms) | Few-Shot (ms) | Ref Torch (ms) |
| Conv2d InstanceNorm Divide | 0.514 | 0.0823 | 0.0898 |
| Gemm GroupNorm Swish Multiply Swish | 0.124 | 0.0542 | 0.0891 |
| Matmul Min Subtract | 0.0651 | 0.0342 | 0.0397 |
| Matmul GroupNorm LeakyReLU Sum | 0.0935 | 0.0504 | 0.072 |
| ConvTranspose3d Swish GroupNorm HardSwish | 33.3 | 29.6 | 35.2 |
| ConvTranspose2d Mish Add Hardtanh Scaling | 0.235 | 0.209 | 0.243 |
| ConvTranspose3d Add HardSwish | 15.6 | 14.1 | 22.2 |
| ConvTranspose2d Add Min GELU Multiply | 0.365 | 0.349 | 0.4 |
| ConvTranspose2d BiasAdd Clamp Scaling Clamp… | 0.3 | 0.31 | 0.368 |
| Conv2d GroupNorm Tanh HardSwish ResidualAdd… | 0.124 | 0.129 | 0.154 |
| Conv2d ReLU HardSwish | 0.0681 | 0.0711 | 0.0768 |

Table 11: Performance comparison of the Section [4.1](#S4.SS1 "4.1 One-shot Baseline ‣ 4 KernelBench Baseline Evaluation ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu") baseline and few-shot prompting in level 2 for problems whose few-shot kernels outperform PyTorch Eager.

## Appendix G Cross-Hardware Case Study

### G.1 Evaluation across different hardware

To evaluate how generated kernels fare across different hardware platforms, we utilize a number of different NVIDIA GPUs that span different micro-architectures and capabilities. The specific details for each is provided in Table [12](#A7.T12 "Table 12 ‣ G.1 Evaluation across different hardware ‣ Appendix G Cross-Hardware Case Study ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu").

|  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- |
| Provider | GPU Type | Memory | Power | Microarchitecture | FP16 TFLOPS | Memory Bandwidth |
| Baremetal | NVIDIA L40S | 48 GB | 300W | Ada | 362.05 | 864 GB/s |
| Baremetal | NVIDIA H100 | 80 GB | 700W | Hopper | 989.5 | 3350 GB/s |
| Serverless | NVIDIA L40S | 48 GB | 350W | Ada | 362.05 | 864 GB/s |
| Serverless | NVIDIA A100 | 42 GB | 400W | Ampere | 312 | 1935 GB/s |
| Serverless | NVIDIA L4 | 24 GB | 72W | Ada | 121 | 300 GB/s |
| Serverless | NVIDIA T4 | 16 GB | 70W | Turing | 65 | 300 GB/s |
| Serverless | NVIDIA A10G | 24 GB | 300W | Ampere | 125 | 600 GB/s |

Table 12: Specifications of different GPUs, including memory, power consumption, micro-architecture, FP16 TFLOPS, memory bandwidth, and their providers.

We ran the same set of kernels generated in Section [4.1](#S4.SS1 "4.1 One-shot Baseline ‣ 4 KernelBench Baseline Evaluation ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu") on a variety of hardware (as listed in Table [12](#A7.T12 "Table 12 ‣ G.1 Evaluation across different hardware ‣ Appendix G Cross-Hardware Case Study ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu")). We computed the fast1\text{fast}_{1} speedup against the PyTorch Eager baseline profiled on that particular hardware platform in Table [13](#A7.T13 "Table 13 ‣ G.1 Evaluation across different hardware ‣ Appendix G Cross-Hardware Case Study ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu").

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| Level | GPUs | Llama-3.1-70b-Inst | DeepSeek-V3 | DeepSeek-R1 |
| 1 | L40S | 3% | 6% | 12% |
| H100 | 2% | 7% | 16% |
| A100 | 3% | 7% | 16% |
| L4 | 2% | 4% | 15% |
| T4 | 3% | 7% | 22% |
| A10G | 2% | 7% | 12% |
| 2 | L40S | 0% | 4% | 36% |
| H100 | 0% | 4% | 42% |
| A100 | 0% | 4% | 38% |
| L4 | 0% | 4% | 36% |
| T4 | 0% | 4% | 46% |
| A10G | 0% | 4% | 47% |
| 3 | L40S | 0% | 8% | 2% |
| H100 | 0% | 10% | 2% |
| A100 | 0% | 8% | 2% |
| L4 | 0% | 6% | 2% |
| T4 | 0% | 10% | 2% |
| A10G | 0% | 10% | 0% |

Table 13: KernelBench result across multiple hardware types: Speedup (fast1\text{fast}_{1}) over Torch Eager comparison of GPUs across different models and levels. The kernels used across different GPUs are the same as the ones generated for Single Attempt without hardware/platform specific information.

Based on the increased variability in fast1\text{fast}_{1} score for DeepSeek R1 as described in Section [4.4](#S4.SS4 "4.4 Performance Variations across Hardware ‣ 4 KernelBench Baseline Evaluation ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu") and Table [13](#A7.T13 "Table 13 ‣ G.1 Evaluation across different hardware ‣ Appendix G Cross-Hardware Case Study ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu"), we plot the individual speedups for each problem (in Levels 1 and 2) across different GPUs. Speedup is computed against PyTorch Eager and there is a horizontal line at y=1.0y=1.0 to mark the cutoff for fast1\text{fast}_{1}.

![Refer to caption](2502.10517v1/figures/DeepSeekR1_Level1_HW.png)

Figure 9: Speedup comparison across different GPUs for DeepSeek R1 on Level 1 (log scale).

![Refer to caption](2502.10517v1/figures/DeepSeekR1_Level2_HW.png)

Figure 10: Speedup comparison across different GPUs for DeepSeek-R1 on Level 2 (log scale).

### G.2 Effect of Providing Hardware Information

We provided hardware-specific information such as the GPU’s micro-architecture, TFLOPS, and memory bandwidth (as shown in Table [12](#A7.T12 "Table 12 ‣ G.1 Evaluation across different hardware ‣ Appendix G Cross-Hardware Case Study ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu")) to models during kernel generation. These generations were then profiled on their respective hardware platforms. The speedup in terms of fast1\text{fast}_{1} over PyTorch Eager is provided below in Table [14](#A7.T14 "Table 14 ‣ G.2 Effect of Providing Hardware Information ‣ Appendix G Cross-Hardware Case Study ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu").

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| Level | GPUs | Llama-3.1-70b-Inst | DeepSeek-V3 | DeepSeek-R1 | OpenAI-o1 |
| 1 | L40S | 2% | 5% | 14% | 13% |
| H100 | 3% | 6% | 14% | 9% |
| A100 | 4% | 4% | 16% | 9% |
| 2 | L40S | 1% | 4% | 33% | 25% |
| H100 | 2% | 2% | 35% | 33% |
| A100 | 2% | 1% | 31% | 32% |
| 3 | L40S | 0% | 2% | 0% | 10% |
| H100 | 2% | 8% | 0% | 12% |
| A100 | 0% | 0% | 2% | 8% |

Table 14: Providing hardware specifications in context: Speedup (fast1\text{fast}_{1}) over Torch Eager comparison of GPUs across different models and levels.

As described in Section [5.2.2](#S5.SS2.SSS2 "5.2.2 Specifying Hardware Information ‣ 5.2 Case Study: Generating Hardware-Efficient Kernels via Hardware Knowledge ‣ 5 Analysis of Model Capabilities ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu"), DeepSeek-R1 begins to generate kernels with warp matrix multiply-accumulate (wmma) instructions. We show the generated kernel for Problem 1 Level 1 when provided with H100 specifications in context below.

[⬇](data:text/plain;base64,I2luY2x1ZGUgPHRvcmNoL2V4dGVuc2lvbi5oPgojaW5jbHVkZSA8Y3VkYV9mcDE2Lmg+CiNpbmNsdWRlIDxjdWRhX3J1bnRpbWUuaD4KI2luY2x1ZGUgPG1tYS5oPgoKdXNpbmcgbmFtZXNwYWNlIG52Y3VkYTsKCl9fZ2xvYmFsX18gdm9pZCBoZ2VtbV9rZXJuZWwoY29uc3QgaGFsZiogQSwgY29uc3QgaGFsZiogQiwgaGFsZiogQywgaW50IE4pIHsKICAgIGNvbnN0IGludCBXQVJQU19QRVJfQkxPQ0sgPSA4OwogICAgY29uc3QgaW50IFdNTUFfTSA9IDE2OwogICAgY29uc3QgaW50IFdNTUFfTiA9IDE2OwogICAgY29uc3QgaW50IFdNTUFfSyA9IDE2OwoKICAgIF9fc2hhcmVkX18gaGFsZiBBc2hhcmVkW1dBUlBTX1BFUl9CTE9DS11bV01NQV9NXVtXTU1BX0tdOwogICAgX19zaGFyZWRfXyBoYWxmIEJzaGFyZWRbV0FSUFNfUEVSX0JMT0NLXVtXTU1BX0tdW1dNTUFfTl07CgogICAgaW50IHdhcnBJZCA9IHRocmVhZElkeC54IC8gMzI7CiAgICBpbnQgbGFuZUlkID0gdGhyZWFkSWR4LnggJSAzMjsKCiAgICBpbnQgdGlsZU0gPSAoYmxvY2tJZHgueSAqIFdBUlBTX1BFUl9CTE9DSyArIHdhcnBJZCkgKiBXTU1BX007CiAgICBpbnQgdGlsZU4gPSBibG9ja0lkeC54ICogV01NQV9OOwoKICAgIHdtbWE6OmZyYWdtZW50PHdtbWE6Om1hdHJpeF9hLCBXTU1BX00sIFdNTUFfTiwgV01NQV9LLCBoYWxmLCB3bW1hOjpyb3dfbWFqb3I+IGFfZnJhZzsKICAgIHdtbWE6OmZyYWdtZW50PHdtbWE6Om1hdHJpeF9iLCBXTU1BX00sIFdNTUFfTiwgV01NQV9LLCBoYWxmLCB3bW1hOjpyb3dfbWFqb3I+IGJfZnJhZzsKICAgIHdtbWE6OmZyYWdtZW50PHdtbWE6OmFjY3VtdWxhdG9yLCBXTU1BX00sIFdNTUFfTiwgV01NQV9LLCBoYWxmPiBjX2ZyYWc7CiAgICB3bW1hOjpmaWxsX2ZyYWdtZW50KGNfZnJhZywgX19mbG9hdDJoYWxmKDAuMGYpKTsKCiAgICBmb3IgKGludCBrID0gMDsgayA8IE47IGsgKz0gV01NQV9LKSB7CiAgICAgICAgaW50IGxvYWRBaWR4ID0gbGFuZUlkICsgKHRpbGVNICsgKGxhbmVJZCAvIFdNTUFfSykpICogTiArIGsgKyAobGFuZUlkICUgV01NQV9LKTsKICAgICAgICBpbnQgbG9hZEJpZHggPSBsYW5lSWQgKyAoayArIChsYW5lSWQgLyBXTU1BX04pKSAqIE4gKyB0aWxlTiArIChsYW5lSWQgJSBXTU1BX04pOwoKICAgICAgICBpZiAodGlsZU0gKyAobGFuZUlkIC8gV01NQV9LKSA8IE4gJiYgayArIChsYW5lSWQgJSBXTU1BX0spIDwgTikKICAgICAgICAgICAgQXNoYXJlZFt3YXJwSWRdW2xhbmVJZCAvIFdNTUFfS11bbGFuZUlkICUgV01NQV9LXSA9IEFbbG9hZEFpZHhdOwogICAgICAgIGVsc2UKICAgICAgICAgICAgQXNoYXJlZFt3YXJwSWRdW2xhbmVJZCAvIFdNTUFfS11bbGFuZUlkICUgV01NQV9LXSA9IF9fZmxvYXQyaGFsZigwLjBmKTsKCiAgICAgICAgaWYgKGsgKyAobGFuZUlkIC8gV01NQV9OKSA8IE4gJiYgdGlsZU4gKyAobGFuZUlkICUgV01NQV9OKSA8IE4pCiAgICAgICAgICAgIEJzaGFyZWRbd2FycElkXVtsYW5lSWQgLyBXTU1BX05dW2xhbmVJZCAlIFdNTUFfTl0gPSBCW2xvYWRCaWR4XTsKICAgICAgICBlbHNlCiAgICAgICAgICAgIEJzaGFyZWRbd2FycElkXVtsYW5lSWQgLyBXTU1BX05dW2xhbmVJZCAlIFdNTUFfTl0gPSBfX2Zsb2F0MmhhbGYoMC4wZik7CgogICAgICAgIF9fc3luY3RocmVhZHMoKTsKCiAgICAgICAgd21tYTo6bG9hZF9tYXRyaXhfc3luYyhhX2ZyYWcsICZBc2hhcmVkW3dhcnBJZF1bMF1bMF0sIFdNTUFfSyk7CiAgICAgICAgd21tYTo6bG9hZF9tYXRyaXhfc3luYyhiX2ZyYWcsICZCc2hhcmVkW3dhcnBJZF1bMF1bMF0sIFdNTUFfTik7CiAgICAgICAgd21tYTo6bW1hX3N5bmMoY19mcmFnLCBhX2ZyYWcsIGJfZnJhZywgY19mcmFnKTsKCiAgICAgICAgX19zeW5jdGhyZWFkcygpOwogICAgfQoKICAgIGludCBzdG9yZUNpZHggPSAodGlsZU0gKyAobGFuZUlkIC8gV01NQV9OKSkgKiBOICsgdGlsZU4gKyAobGFuZUlkICUgV01NQV9OKTsKICAgIGlmICh0aWxlTSArIChsYW5lSWQgLyBXTU1BX04pIDwgTiAmJiB0aWxlTiArIChsYW5lSWQgJSBXTU1BX04pIDwgTikKICAgICAgICBDW3N0b3JlQ2lkeF0gPSBjX2ZyYWcueFtsYW5lSWRdOwp9Cgp0b3JjaDo6VGVuc29yIGhnZW1tX2N1ZGEodG9yY2g6OlRlbnNvciBBLCB0b3JjaDo6VGVuc29yIEIsIGludCBOKSB7CiAgICBhdXRvIEMgPSB0b3JjaDo6emVyb3Moe04sIE59LCBBLm9wdGlvbnMoKS5kdHlwZSh0b3JjaDo6a0Zsb2F0MTYpKTsKCiAgICBjb25zdCBpbnQgV0FSUFNfUEVSX0JMT0NLID0gODsKICAgIGRpbTMgZ3JpZCgoTiArIDE1KSAvIDE2LCAoTiArIDE1KSAvICgxNiAqIFdBUlBTX1BFUl9CTE9DSykpOwogICAgZGltMyBibG9jaygzMiAqIFdBUlBTX1BFUl9CTE9DSyk7CgogICAgaGdlbW1fa2VybmVsPDw8Z3JpZCwgYmxvY2s+Pj4oQS5kYXRhX3B0cjxoYWxmPigpLCBCLmRhdGFfcHRyPGhhbGY+KCksIEMuZGF0YV9wdHI8aGFsZj4oKSwgTik7CiAgICByZXR1cm4gQzsKfQ==)

1
#include <torch/extension.h>

2
#include <cuda_fp16.h>

3
#include <cuda_runtime.h>

4
#include <mma.h>

5

6
using namespace nvcuda;

7

8
__global__ void hgemm_kernel(const half* A, const half* B, half* C, int N) {

9
 const int WARPS_PER_BLOCK = 8;

10
 const int WMMA_M = 16;

11
 const int WMMA_N = 16;

12
 const int WMMA_K = 16;

13

14
 __shared__ half Ashared[WARPS_PER_BLOCK][WMMA_M][WMMA_K];

15
 __shared__ half Bshared[WARPS_PER_BLOCK][WMMA_K][WMMA_N];

16

17
 int warpId = threadIdx.x / 32;

18
 int laneId = threadIdx.x % 32;

19

20
 int tileM = (blockIdx.y * WARPS_PER_BLOCK + warpId) * WMMA_M;

21
 int tileN = blockIdx.x * WMMA_N;

22

23
 wmma::fragment<wmma::matrix_a, WMMA_M, WMMA_N, WMMA_K, half, wmma::row_major> a_frag;

24
 wmma::fragment<wmma::matrix_b, WMMA_M, WMMA_N, WMMA_K, half, wmma::row_major> b_frag;

25
 wmma::fragment<wmma::accumulator, WMMA_M, WMMA_N, WMMA_K, half> c_frag;

26
 wmma::fill_fragment(c_frag, __float2half(0.0f));

27

28
 for (int k = 0; k < N; k += WMMA_K) {

29
 int loadAidx = laneId + (tileM + (laneId / WMMA_K)) * N + k + (laneId % WMMA_K);

30
 int loadBidx = laneId + (k + (laneId / WMMA_N)) * N + tileN + (laneId % WMMA_N);

31

32
 if (tileM + (laneId / WMMA_K) < N && k + (laneId % WMMA_K) < N)

33
 Ashared[warpId][laneId / WMMA_K][laneId % WMMA_K] = A[loadAidx];

34
 else

35
 Ashared[warpId][laneId / WMMA_K][laneId % WMMA_K] = __float2half(0.0f);

36

37
 if (k + (laneId / WMMA_N) < N && tileN + (laneId % WMMA_N) < N)

38
 Bshared[warpId][laneId / WMMA_N][laneId % WMMA_N] = B[loadBidx];

39
 else

40
 Bshared[warpId][laneId / WMMA_N][laneId % WMMA_N] = __float2half(0.0f);

41

42
 __syncthreads();

43

44
 wmma::load_matrix_sync(a_frag, &Ashared[warpId][0][0], WMMA_K);

45
 wmma::load_matrix_sync(b_frag, &Bshared[warpId][0][0], WMMA_N);

46
 wmma::mma_sync(c_frag, a_frag, b_frag, c_frag);

47

48
 __syncthreads();

49
 }

50

51
 int storeCidx = (tileM + (laneId / WMMA_N)) * N + tileN + (laneId % WMMA_N);

52
 if (tileM + (laneId / WMMA_N) < N && tileN + (laneId % WMMA_N) < N)

53
 C[storeCidx] = c_frag.x[laneId];

54
}

55

56
torch::Tensor hgemm_cuda(torch::Tensor A, torch::Tensor B, int N) {

57
 auto C = torch::zeros({N, N}, A.options().dtype(torch::kFloat16));

58

59
 const int WARPS_PER_BLOCK = 8;

60
 dim3 grid((N + 15) / 16, (N + 15) / (16 * WARPS_PER_BLOCK));

61
 dim3 block(32 * WARPS_PER_BLOCK);

62

63
 hgemm_kernel<<<grid, block>>>(A.data_ptr<half>(), B.data_ptr<half>(), C.data_ptr<half>(), N);

64
 return C;

65
}

Figure 11: A CUDA kernel generated by DeepSeek-R1 for Level 1 Problem 1 when provided with hardware-specific information on the H100 GPU.

## Appendix H High-Throughput Evaluation System

### H.1 Single-shot Experiments: Batched Kernel Generation

Given the high volume of GPU kernels to evaluate, we build a fast and highly-parallelized evaluation system, where we separate into the kernel generation and evaluation process into 3 stages, as shown in Figure [12](#A8.F12 "Figure 12 ‣ H.1 Single-shot Experiments: Batched Kernel Generation ‣ Appendix H High-Throughput Evaluation System ‣ KernelBench: Can LLMs Write Efficient GPU Kernels? *Equal Contribution. Correspondence: aco@stanford.edu, simonguo@stanford.edu").

- •

  Inference: We query LMs in parallel and store the generated kernel.
- •

  CPU Pre-Compile: We compile the model-generated kernels with nvcc for a specified hardware into a binary, parallelized on CPUs and each kernel binary is saved to their individual specific directory for caching.
- •

  GPU Evaluation: With the kernel binary already built on CPU, we focus on evaluating multiple kernels in parallel across multiple GPU devices. However, to ensure accurate kernel timing, we only evaluate one kernel at time on one device.

![Refer to caption](2502.10517v1/figures/parallel-eval.png)

Figure 12: KernelBench provide a high throughput kernel generation and evaluation system. We parallelized generation, compilation, and evaluation of kernels across CPUs and GPUs.

### H.2 Iterative Refinement Experiments: GPU Orchestrator System

Based on the single-shot system, we also design a platform to handle multiple iterative refinement experiments at once. We treat each iterative refinement experiment as a finite state machine, where the states are LM-based kernel generation, pre-compilation, kernel execution, and profiling. The transitions are based on environment feedback, and can change based on different experiment setups.

Our system was run on a node with 88 available GPUs. Unlike the single-shot system, batching each generation and kernel execution is highly inefficient – thus, we design a pipelined, multiprocessing system with a GPU orchestrator with the following characteristics:

- •

  CPU Parallelism: The orchestrator spawns multiple independent processes that each handle an independent task in KernelBench. These processes run the multi-turn state machine logic for the iterative refinement experiments – only the kernel execution state requires acquiring a GPU.
- •

  Acquiring GPUs: The GPU orchestrator keeps a separate process running that handles which processes can acquire a GPU using semaphores. Processes can request a GPU from this process when it is ready to execute and evaluate kernel code. We try to minimize process control over a GPU to maximize resource throughput, given a system with a limited number of available GPUs.
- •

  Pre-compiling on the CPU: To avoid processes hogging GPU time, we pre-compile kernels with nvcc on the CPU for a specified hardware into a binary. We also did this same trick for the single-shot system, but for separate reasons.
- •

  Evaluating Kernels on the GPU: The only state where the finite state machine uses the GPU is for kernel execution and profiling. We found that waiting on GPUs is the primary bottleneck in the orchestrator, so we designed the orchestrator to maximize device occupancy.

The system generally supports overlapping the generation of kernel code and the execution of already-generated kernel code. There are also several unavoidable errors such as CUDA illegal memory accesses and deadlocks due to faulty kernel generations that the orchestrator solves by releasing and spawning new processes when encountered, and we wrote specifically handlers to ensure these errors are properly captured without crashing the orchestrator itself.

### H.3 UI: Visualizing Kernel Generation Trajectories

To qualitatively observe the generated and compare them across techniques, we design an interface to easily visualize them. We provide this as part of the KernelBench framework.

![Refer to caption](2502.10517v1/figures/kernel_inspect_interface.png)

Figure 13: We provide a visual interface for kernel inspection. This allows us to easily examine kernel content, its performance, and compare across various techniques and configurations.
