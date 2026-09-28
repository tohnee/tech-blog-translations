---
title: "SPRINT: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models"
arxiv: 2506.05745
source: https://arxiv.org/abs/2506.05745
crawled: 2026-09-23
---

# Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models

Emil Biju
††thanks: Equal contribution.
Affiliation: Stanford University
Affiliation: Microsoft
  
Shayan Talaei11footnotemark: 
1
Affiliation: Stanford University
  
Zhemin Huang11footnotemark: 
1
Affiliation: Stanford University
  
Mohammadreza Pourreza
Affiliation: Google
  
Azalia Mirhoseini
††thanks: Equal senior authorship.
Affiliation: Stanford University
  
Amin Saberi22footnotemark: 
2
Email: [{emilbiju, stalaei, zheminh}@stanford.edupourreza@google.com, {azalia, saberi}@stanford.edu](mailto:)
Affiliation: Stanford University

###### Abstract

Large reasoning models (LRMs) excel at complex reasoning tasks but typically generate lengthy sequential chains-of-thought, resulting in long inference times before arriving at the final answer. To address this challenge, we introduce Sprint, a novel post-training and inference-time framework designed to enable LRMs to dynamically identify and exploit opportunities for parallelization during their reasoning process. Sprint incorporates an innovative data curation pipeline that reorganizes natural language reasoning trajectories into structured rounds of long-horizon planning and parallel execution. By fine-tuning LRMs on a small amount of such curated data, the models *learn* to dynamically identify independent subtasks within extended reasoning processes and effectively execute them in parallel. Through extensive evaluations, we demonstrate that models fine-tuned with the Sprint framework match the performance of reasoning models on complex domains such as mathematics while generating up to 39% fewer sequential tokens on problems requiring more than 8,000 output tokens. Finally, we observe consistent results transferred to two out-of-distribution tasks, namely GPQA and Countdown, with up to 45% and 65% reduction in average sequential tokens respectively for longer reasoning trajectories, while matching the performance of the fine-tuned reasoning model.

## 1 Introduction

Scaling inference-time compute in large language models (LLMs) has consistently been shown to enhance reasoning accuracy. Existing methods broadly fall into two categories: sequential [Wei et al. (2023)](#bib.bib15) and parallel [Brown et al. (2024)](#bib.bib10). Sequential approaches, notably large reasoning models (LRMs) such as Deepseek-R1 [Guo et al. (2025)](#bib.bib2) and OpenAI o1 [OpenAI (2024)](#bib.bib1), have demonstrated remarkable successes in solving complex reasoning tasks, e.g., math and coding, but at the cost of generating very lengthy sequences of tokens. On the other hand, parallel methods, such as repeated sampling with self-consistency [Wang et al. ()](#bib.bib41) or best-of-N [Cobbe et al. (2021)](#bib.bib35); [Lightman et al. (2023b)](#bib.bib32) leverage multiple response generations to improve accuracy. However, these methods typically lack effective coordination and shared information across inference paths, leading to redundant computations and limited performance gains. Furthermore, structured parallel methods like Tree-of-Thoughts [Yao et al. (2023a)](#bib.bib7) and Graph-of-Thoughts [Besta et al. (2024)](#bib.bib8) require predefined, heuristics-driven search structures, inherently restricting flexibility and scalability across diverse tasks.

We propose Sprint11
1
The name Sprint is inspired by the agile development methodology, where a sprint involves a planning phase followed by parallel, incremental execution., a framework for post-training and inference of reasoning models that combines the advantages of sequential reasoning and parallel inference, while maintaining the flexibility required for general tasks. Instead of relying on manual structures, Sprint trains reasoning language models to dynamically identify and exploit parallelization opportunities during inference. This enables Sprint to achieve the high accuracy of reasoning models while significantly reducing the number of sequential tokens needed for solving complex reasoning tasks such as mathematics.

For the inference, Sprint introduces an orchestration of LRMs through two distinct roles: a planner and a pool of executors. At each step, the planner that has access to the cumulative context of the reasoning trajectory generates a set of independent plans, each explained via a natural language *<prompt>*. Subsequently, multiple executors concurrently carry out these plans. This interleaved planning-execution strategy accelerates the reasoning process by enabling simultaneous execution of lengthy tasks.

Although many off-the-shelf LRMs achieve high performance via sequential reasoning trajectories, they are not trained for effectively proposing parallelizable tasks. Recognizing that LRMs’ reasoning trajectories for a given query include steps such as reflection on their previous steps, decomposing tasks to subtasks, and trial-and-error exploration of alternative strategies, we question the necessity of strictly sequential reasoning. In practice, many reasoning steps are independent and thus can be executed in parallel; for instance, by simultaneously exploring multiple strategies or independently computing separate components of a complex problem. Building on these insights, we designed a data curation pipeline that carefully reorganizes natural language reasoning trajectories into structured plans and parallel executions, closely preserving the original data distribution. Finally, through supervised fine-tuning of the reasoning model on only 1700 such demonstrations, we unlock the model’s capability to dynamically recognize and exploit opportunities for parallel reasoning.

To evaluate the accuracy and efficacy of Sprint, we conducted experiments on MATH-500 [Lightman et al. (2023b)](#bib.bib32) for testing in-distribution, and two out-of-domain distribution benchmarks: GPQA-diamond [Rein et al. (2023)](#bib.bib16), and Countdown (Game of 24) [Yao et al. (2023a)](#bib.bib7). On MATH-500, Sprint improved the accuracy of the base reasoning model Deepseek-R1-distill-7B [Guo et al. (2025)](#bib.bib2) from 89.1% to 92.5%, outperforming the reasoning fine-tuned model (RFT) at 91%, while generating 440 fewer sequential tokens on average. On the problems requiring longer reasoning trajectories (more than 8000 tokens under the RFT model), Sprint achieves even greater savings, reducing sequential tokens by up to 39%. We also show that Sprint generalizes well to out-of-domain tasks, matching the performance of the reasoning fine-tuned model while significantly reducing token usage – by 53% on Countdown.

In summary, our work makes the following key contributions22
2
We open-source our code and datasets at this [repository](https://github.com/ShayanTalaei/SPRINT/tree/main).:

- •

  We propose Sprint, an innovative framework for accelerating the reasoning process of large reasoning models through rolling horizon parallel planning and execution.
- •

  We develop a novel data curation pipeline that carefully converts complex natural language reasoning trajectories into structured datasets for fine-tuning LRMs, featuring a multi-step process that includes step extraction, Directed Acyclic Graph (DAG) creation, packing, filtering, and reformatting.
- •

  We analyze the accuracy and the efficiency of Sprint on complex reasoning tasks in comparison to strong reasoning baselines. Our results show that Sprint can achieve higher accuracy compared to the reasoning distilled model, while generating up to 39% fewer sequential tokens on long reasoning trajectories.
- •

  We show consistent generalization performance of Sprint on two out-of-domain benchmarks, saving sequential tokens by about 45% on GPQA and 65% on Countdown respectively, while matching the performance of the reasoning finetuned model. These results highlight Sprint’s ability to effectively parallelize reasoning trajectories across diverse domains.

## 2 Related Work

Long Chains-of-Thought for Improved Reasoning.
Recent advancements have shown that generating extensive chains-of-thought [Wei et al. (2023)](#bib.bib15) significantly enhances the reasoning capabilities of large language models, particularly in tasks such as mathematical problem-solving and logical inference [Zhu et al. (2023)](#bib.bib43); [Zelikman et al. (2022)](#bib.bib42); [OpenAI (2024)](#bib.bib1); [Guo et al. (2025)](#bib.bib2). Despite their effectiveness, these methods inherently produce long sequential outputs, increasing latency and slowing inference speed. Sprint addresses this limitation by enabling models to dynamically parallelize independent reasoning steps, significantly reducing sequential generation and enhancing inference efficiency.

Structured Search and Multi-Agent Frameworks. Approaches like Tree-of-Thought [Yao et al. (2023a)](#bib.bib7), Graph-of-Thought [Besta et al. (2024)](#bib.bib8), Forest-of-Thought [Bi et al. (2025)](#bib.bib27), and Atom-of-Thought [Teng et al. (2025)](#bib.bib40), along with multi-agent interaction methods [Du et al. (2023)](#bib.bib36); [Kim et al. (2024)](#bib.bib37); [Zhuge et al. (2024)](#bib.bib44); [Saad-Falcon et al. (2024)](#bib.bib21), structure reasoning processes through fixed search patterns or predefined interaction protocols, often at the full-solution level. Sprint generalizes these frameworks by *training* models to autonomously allocate inference-time computation between serial and parallel tasks to solve sub-parts of one solution trajectory or explore alternative solutions.

Planning and Execution with Language Models. Integrating planning capabilities into language models has been explored through upfront decomposition of tasks into subtasks [Zhou et al. (2022)](#bib.bib4); [Valmeekam et al. (2023)](#bib.bib19); [Juneja et al. (2024)](#bib.bib9); [Prasad et al. (2024)](#bib.bib20) or iterative refinement based on intermediate feedback [Yao et al. (2023b)](#bib.bib5); [Shinn et al. (2023)](#bib.bib6). These approaches primarily rely on sequential execution without explicitly considering dynamic parallel planning. Sprint addresses this gap by enabling models to autonomously perform dynamic parallel planning, enhancing inference efficiency through concurrent execution.

Table 1: Comparison of inference-time scaling approaches. Methods are evaluated based on support for inference-time parallelism, adaptive search, model optimization, and the capability to handle multi-step sequential reasoning. Sprint uniquely addresses all criteria, enabling dynamic parallelism in general reasoning tasks that require interdependent sequential steps.

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| Method | Inference-Time  Parallelism | Adaptive  Search | Model  Optimization | Multi-Step  Reasoning |
| Tree-of-Thought (ToT) [Yao et al. (2023a)](#bib.bib7) | ✓ | ✗ | ✗ | ✗ |
| Graph-of-Thought (GoT) [Besta et al. (2024)](#bib.bib8) | ✓ | ✗ | ✗ | ✗ |
| Skeleton-of-Thought (SoT) [Ning et al. (2023)](#bib.bib39) | ✓ | ✓ | ✗ | ✗ |
| Repeated Sampling [Brown et al. (2024)](#bib.bib10); [Wang et al. ()](#bib.bib41); [Cobbe et al. (2021)](#bib.bib35) | ✓ | ✗ | ✗ | ✗ |
| Reasoning Models [Guo et al. (2025)](#bib.bib2); [OpenAI (2024)](#bib.bib1) | ✗ | ✓ | ✓ | ✓ |
| PASTA [Jin et al. (2025)](#bib.bib29) | ✓ | ✓ | ✓ | ✗ |
| Hogwild! Inference [Rodionov et al. (2025)](#bib.bib30) | ✓ | ✓ | ✗ | ✗ |
| Sprint (Ours) | ✓ | ✓ | ✓ | ✓ |

Parallelization in language model reasoning. Methods that leverage parallel inference paths, such as best-of-N sampling [Cobbe et al. (2021)](#bib.bib35); [Lightman et al. (2023b)](#bib.bib32) or self-consistency [Wang et al. ()](#bib.bib41), have shown performance improvements through generating multiple independent reasoning trajectories. However, these techniques typically lack effective coordination among parallel threads, resulting in redundancy and inefficient computation. To mitigate this issue, Skeleton-of-Thought (SoT)[Ning et al. (2023)](#bib.bib39) and APAR[Liu et al. (2024)](#bib.bib28) parallelize decoding by assuming semantic independence among subtasks, thus enabling separate processing of different response segments. Although these methods achieve faster inference, they exhibit suboptimal performance on tasks that inherently require sequential reasoning, such as mathematical problem-solving, where later steps depend on earlier computations.

Recently, three works, PASTA [Jin et al. (2025)](#bib.bib29), Hogwild! Inference [Rodionov et al. (2025)](#bib.bib30), and APR [Pan et al. (2025)](#bib.bib31) have investigated parallelization within a shared reasoning trajectory. PASTA teaches models to decompose a task into parallel subtasks and subsequently merges their full context back into a single main thread, but it does not optimize for reasoning tasks that require multi-step planning. Hogwild! Inference relies on parallel prompting for collaborative reasoning among multiple workers, without tuning the models to distribute tasks effectively. APR trains models to delegate subtasks to parallel child threads for synthetic countdown tasks, but its training data curation relies on a specialized symbolic solver, limiting its applicability to general reasoning tasks. Sprint extends this line of research by introducing a generalizable post-training framework that enables reasoning models to dynamically structure inference for general reasoning tasks.

In general, an effective reasoning system should support logical multi-step interdependencies (multi-step reasoning) to accurately handle tasks where later steps depend on earlier outcomes. It should dynamically adapt its search strategy (adaptive search) to address diverse problem structures. Optimizing model performance specifically for downstream tasks (model optimization) is often necessary to achieve efficient results. Finally, leveraging parallel execution (inference-time parallelism) is crucial to reducing latency by concurrently processing independent reasoning subtasks. Table [1](#S2.T1 "Table 1 ‣ 2 Related Work ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models") compares our method and existing inference-time scaling methods against these criteria.

## 3 Methodology

In this section, we outline the design and components of Sprint, which at a high level consists of an inference framework for reasoning models and a training protocol to teach them how to effectively identify and exploit parallelizable planning and execution during their reasoning processes.

### 3.1 Interleaved Planning and Parallel Execution at Inference Time

Figure 1: Overview of Sprint’s inference process: 1) The planner receives the cumulative context, including previous plans and execution results, and either proposes a new set of independent tasks or terminates the process by producing the final answer. 2) A pool of executors concurrently performs each task according to their prompts. 3) The execution outcomes are appended back into the cumulative context with corresponding tags, returning to step 1 for the next iteration.

Sprint’s inference comprises two main modules: a planner and a pool of executors, all powered by fine-tuned reasoning models. Inference begins when the planner receives the *input query*, followed by iterative rounds of planning and execution, called *stages*, until the planner decides to terminate the process by producing the final answer. As shown in Figure [1](#S3.F1 "Figure 1 ‣ 3.1 Interleaved Planning and Parallel Execution at Inference Time ‣ 3 Methodology ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models"), each inference stage includes the following three phases:

1. Planning. At stage ii, the planner receives the cumulative context of the reasoning trajectory, which includes the input query, previous plans, and the execution outputs from all the preceding stages (11 through i−1i-1). The planner then generates a plan for the current stage, enclosed within *<Plan_i>* tags. During this stage, the planner may generate intermediate reasoning tokens, benefiting from its reasoning capabilities. When the planner identifies a subtask suitable for delegation to an executor, it specifies this task within tags *<prompt_i.j>*. Upon closing each *</prompt_i.j>* tag, an executor initiates the corresponding task given the current cumulative context snapshot.

2. Parallel executions. Each executor independently and concurrently performs its assigned subtask by generating a chain-of-thought reasoning trajectory to accomplish the specific task. Executing these subtasks in parallel significantly reduces the total number of sequential tokens generated compared to processing them sequentially, greatly improving inference efficiency.

3. Syncing. Once all parallel executions are complete, the results from each executor are enclosed within tags *<execution_i.j>*, clearly indicating their corresponding tasks. These results are synced back into the cumulative context in the same order as their original prompt definitions. The updated context is then fed back to the planner, which either initiates the next stage or concludes the inference by outputting the final answer.

### 3.2 Training Reasoning Models for Sprint Framework

To effectively train reasoning models to identify and exploit parallelization opportunities during inference, we developed a data curation pipeline that transforms complete natural language reasoning trajectories into structured rounds of rolling-horizon planning and parallel execution. The pipeline extracts individual planning and execution steps, organizes them into dependency-based stages, and generates training examples that capture both sequential planning and parallel execution aspects. An overview of this pipeline is shown in Figure [2](#S3.F2 "Figure 2 ‣ 3.2 Training Reasoning Models for Sprint Framework ‣ 3 Methodology ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models"). Detailed prompts for each step in the pipeline are provided in Appendix [A](#A1 "Appendix A Implementation Details ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models").

![Refer to caption](2506.05745v2/SPRINT_Training_overview.png)

Figure 2: Overview of the Sprint training pipeline: (0) Starting from raw reasoning trajectories, (1) we first extract individual reasoning steps, identifying their planning and execution phases. Next, (2) we construct a DAG representing dependencies among these steps, and then (3) group steps into compact stages that can be executed in parallel. Finally, (4) after filtering and reformatting these structured stages into training samples, we perform supervised fine-tuning of a reasoning model to dynamically propose and execute parallelizable tasks.

1. Step extraction. Given a reasoning trajectory τ\tau, generated by DeepSeek-R1 [Guo et al. (2025)](#bib.bib2) in response to a query QQ, we decompose it into distinct steps S={S1,S2,…,Sn}S=\{S_{1},S_{2},\dots,S_{n}\} by prompting an LLM (in this case, GPT-4o) with specific instructions; refer to Appendix [A.2](#A1.SS2.SSS0.Px1 "Step Extraction. ‣ A.2 Dataset Curation ‣ Appendix A Implementation Details ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models"). Each step SiS_{i} is further decomposed into a planning phase (PiP_{i}), where R1 identifies tasks and strategies, and an execution phase (EiE_{i}), where these planned tasks are performed. Note that some steps may only involve planning without explicit execution; these are termed *plan-only steps*, and no executor instructions are generated for them.

To discourage trivial executor calls, we merge very short executions back into their planning phase, making them plan-only steps and encouraging the planner to handle simpler tasks independently.

2. DAG creation. Next, we identify dependencies among steps by prompting a smaller LLM (GPT-4o-mini) to determine which steps depend on others; for the instructions see [A.2](#A1.SS2.SSS0.Px2 "DAG Creation. ‣ A.2 Dataset Curation ‣ Appendix A Implementation Details ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models"). These dependencies are represented formally as:

|  |  |  |
| --- | --- | --- |
|  | D={(Si,Sj)∣Sj depends on Si,i<j,Si,Sj∈S}.D=\{(S_{i},S_{j})\mid S_{j}\text{ depends on }S_{i},i<j,S_{i},S_{j}\in S\}. |  |

This set of dependencies forms a Directed Acyclic Graph (DAG), denoted by G=(S,D)G=(S,D), where nodes represent individual steps and edges represent dependencies among them.

3. Packing. We group the steps into stages, each containing plans that can be generated simultaneously by the planner and executions that can be carried out concurrently by executors. While a naive approach would group steps solely based on their depth in the DAG, we further optimize the stage arrangement by observing that if the parent SpS_{p} of a node SiS_{i} is a plan-only step, SiS_{i} can safely be included in the same stage as SpS_{p}. This optimization ensures both context availability and enhanced parallelization efficiency. Further details on this adjustment are provided in Appendix [A.2](#A1.SS2 "A.2 Dataset Curation ‣ Appendix A Implementation Details ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models").

Formally, the stage number σ⁡(Si)\sigma(S_{i}) for each step Si=(Pi,Ei)S_{i}=(P_{i},E_{i}) is defined as:

|  |  |  |
| --- | --- | --- |
|  | σ⁡(Si)={1,if ​Si​ has no parentsmaxSp∈Parents​(Si)⁡(σ⁡(Sp)+𝟙​(Ep≠∅)),otherwise\displaystyle\sigma(S_{i})=\begin{cases}1,&\text{if }S_{i}\text{ has no parents}\\ \max\limits_{S_{p}\in\text{Parents}(S_{i})}\left(\sigma(S_{p})+\mathbb{1}(E_{p}\neq\emptyset)\right),&\text{otherwise}\end{cases} |  |

The set of steps at a given stage kk consists of all steps with stage number σ⁡(Si)=k\sigma(S_{i})=k, represented as:

|  |  |  |
| --- | --- | --- |
|  | ℒ(k)=Si∈S|σ⁡(Si)=k.\mathcal{L}^{(k)}={S_{i}\in S\mid\sigma(S_{i})=k}. |  |

Within each stage kk, the combined plan is created by concatenating the plans of all steps SiS_{i} in ℒ(k)\mathcal{L}^{(k)}, ordered according to their original sequence. The execution phase for stage kk includes execution components from all steps, excluding those that are plan-only:

|  |  |  |
| --- | --- | --- |
|  | 𝒫(k)=concat(Pi∣Si∈ℒ(k)),ℰ(k)={Ei∣Si∈ℒ(k),Ei≠∅},\displaystyle\mathcal{P}^{(k)}=\text{concat}(P_{i}\mid S_{i}\in\mathcal{L}^{(k)}),\quad\mathcal{E}^{(k)}=\{E_{i}\mid S_{i}\in\mathcal{L}^{(k)},E_{i}\neq\emptyset\}, |  |

where Ei=∅E_{i}=\emptyset indicates that SiS_{i} is a plan-only step.

4. Training the LRM.
To ensure that the model learns from trajectories with significant parallelization potential, we introduce a *parallelization ratio*, defined as (#​steps)/(#​stages)(\#\text{steps})/(\#\text{stages}), and discard trajectories with ratios below 1.5. The selected trajectories are reformatted into sequences of stage-wise plans and executions, enclosed within explicit tags (*<Plan_i>* and *<execution_i.j>*) in the order illustrated in Figure [3](#S3.F3 "Figure 3 ‣ 3.2 Training Reasoning Models for Sprint Framework ‣ 3 Methodology ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models"). Finally, we fine-tune the LRM on the reformatted thinking patterns. Through this process, the model learns to dynamically propose independent, parallelizable tasks based on previous sequences of plans and executions, and to execute each task following its corresponding prompt effectively.

Figure 3: Comparison of sequential tokens decoded during reasoning. Sequential reasoning models generate all the steps serially, resulting in long token sequences. Sprint’s fine-tuning data restructures these steps into stages, grouping parallelizable plans followed by their respective executions. This organization enables Sprint’s inference framework to execute these grouped steps in parallel, significantly reducing the number of sequential tokens.

Methodology Overview. Overall, as detailed in Section [3.2](#S3.SS2 "3.2 Training Reasoning Models for Sprint Framework ‣ 3 Methodology ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models"), Sprint trains reasoning models to propose parallelizable subtasks rather than generating their entire reasoning trajectories serially. During inference, as described in Section [3.1](#S3.SS1 "3.1 Interleaved Planning and Parallel Execution at Inference Time ‣ 3 Methodology ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models"), the trained model effectively manages long-term interdependencies while significantly reducing the number of sequential tokens generated. Figure [3](#S3.F3 "Figure 3 ‣ 3.2 Training Reasoning Models for Sprint Framework ‣ 3 Methodology ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models") illustrates this workflow, highlighting how Sprint reorganizes sequential reasoning traces into parallelizable stages during training and subsequently leverages this learned parallel structure for efficient, concurrent execution at inference time. For examples of Sprint’s reasoning versus serial reasoning trajectories, please refer to Appendix [B](#A2 "Appendix B Sample Demonstrations ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models").

## 4 Experiments

### 4.1 Experimental Setup

Datasets.
To train our models, we begin with 6,000 reasoning trajectories from DeepSeek-R1 [Guo et al. (2025)](#bib.bib2) generated on the training set of the MATH dataset [Hendrycks et al. (2021)](#bib.bib33), as released by [open-r1 (2025)](#bib.bib34). After filtering these trajectories for correctness of the final answers and processing them through our data curation pipeline (Section [3.2](#S3.SS2 "3.2 Training Reasoning Models for Sprint Framework ‣ 3 Methodology ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models")), we obtain a curated set of approximately 1,700 samples for training.

For evaluation, we primarily use the MATH-500 benchmark [Lightman et al. (2023a)](#bib.bib3), a widely recognized test set consisting of 500 mathematical reasoning problems. To further examine the generalization capabilities of Sprint to more challenging and out-of-distribution scenarios, we evaluate its performance against strong baseline models on two additional benchmarks. First, we evaluate on GPQA-diamond [Rein et al. (2023)](#bib.bib16), a dataset from entirely different scientific domains, including biology, physics, and chemistry, thus assessing cross-domain reasoning robustness. Moreover, following [Pan et al. (2025)](#bib.bib31); [Yao et al. (2023a)](#bib.bib7), we test Sprint on a subset of 1000 samples from Countdown [Yao et al. (2023a)](#bib.bib7), a synthetic numerical reasoning task in which models must derive a target number from four provided numbers using arithmetic operations (+,−,×,÷+,-,\times,\div).

Baselines.
We compare Sprint against several reasoning baselines employing both serial and parallel sampling strategies:

1. Base reasoning model (DeepSeek-R1-Distill-Qwen-7B) [Guo et al. (2025)](#bib.bib2): This model is a distillation of the main R1 reasoning model into Qwen-2.5-7B [Yang et al. (2024)](#bib.bib14), released by DeepSeek. We use this reasoning model both as a baseline for direct comparison and as the base model for our fine-tuning experiments.

2. Reasoning fine-tuned model (RFT): To control for the effect of the training data and compare against conventional distillation methods, we perform supervised fine-tuning of the DeepSeek-R1-Distill-Qwen-7B model using the same 1,700 R1 reasoning trajectories from MATH used to train Sprint. This model represents a standard continued distillation of Qwen-2.5-7B on R1 trajectories from the MATH dataset.

3. Skeleton-of-Thought (SoT) [Ning et al. (2023)](#bib.bib39): Given a query, SoT decomposes it into subtasks and executes them through parallel LLM calls within a single stage. Both the subtask generation and execution processes rely on out-of-the-box LLMs without any task-specific fine-tuning. We evaluate SoT using both the chat-instruct Qwen-2.5-7B model (referred to as SoT-chat) and the reasoning-focused DeepSeek-R1-Distill-Qwen-7B model (referred to as SoT-reasoning).

4. Repeated Sampling + Self-consistency [Brown et al. (2024)](#bib.bib10); [Wang et al. ()](#bib.bib41): We include repeated sampling combined with self-consistency aggregation as a baseline to evaluate whether a purely parallel sampling approach can achieve similar accuracy and efficiency compared to the interleaved planning and execution framework of Sprint.

Evaluation Metrics. We consider two metrics to evaluate the performance and efficiency of different approaches. First, we measure the accuracy of the final answer reached for the downstream task, computed as the percentage of the correctly answered queries by each method (see [A.4](#A1.SS4 "A.4 Evaluation ‣ Appendix A Implementation Details ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models") for details). Second, to evaluate the efficiency improvements in terms of the latency, we measure the number of sequential tokens generated by each method. In particular, for sequential reasoning baselines, it is exactly the number of output tokens. For Sprint, we calculate the sequential tokens as follows:

|  |  |  |
| --- | --- | --- |
|  | number of sequential tokens=∑i=1# stagesmaxk# prompts at stage ​i⁡(Pi.k+Ei.k),\text{number of sequential tokens}=\sum_{i=1}^{\text{\# stages}}\max_{k}^{\text{\# prompts at stage }i}(P_{i.k}+E_{i.k}), |  |

where Pi.kP_{i.k} and Ei.kE_{i.k} represent the number of sequential tokens generated by the planner until the end of kthk^{\text{th}} prompt and by an executor for the kthk^{\text{th}} execution at step ii respectively. Note that the ideal wall-clock time correlates with the number of sequential tokens generated by each method; however, accurately measuring this metric would require higher computational resources, which we discuss further in Section [5](#S5 "5 Limitations and Future work ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models").

### 4.2 Results

Figure 4: Pareto plot comparing accuracy (%) and sequential token counts generated by different methods on MATH-500. While Sprint achieves slightly higher accuracy compared to the RFT model, it generates 440 (∼15%\sim 15\%) fewer tokens on average.

Figure 5: Number of problems at each difficulty level in MATH-500 that pass each stage of interleaved planning before arriving at the final answer. The dashed line indicates the number of problems at each stage that exhibit parallelism (more than one plan).

|  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  | In-domain | | | Out-of-domain | | | |
|  | MATH-500 | | | Countdown | | GPQA-Diamond | |
| Method | Acc↑\uparrow | # Seq↓\downarrow | # Total↓\downarrow | Acc↑\uparrow | # Seq↓\downarrow | Acc↑\uparrow | # Seq↓\downarrow |
| Self-consistency | 80.5 | 590 | 11645 | 78.5 | 2845 | 45.4 | 4735 |
| SoT-chat | 47.3 | 256 | 1290 | 80.0 | 2367 | 49.4 | 3526 |
| SoT-reasoning | 90.8 | 3836 | 11538 | 82.4 | 5823 | 48.0 | 7560 |
| RFT | 91.0 | 2880 | 2880 | 84.9 | 4917 | 50.5 | 7103 |
| Sprint | 92.5 | 2440 | 3622 | 85.9 | 2284 | 51.0 | 6336 |

Table 2: Comparison of pass@1 accuracy and sequential token count across MATH-500, GPQA-Diamond, and Countdown tasks. While Sprint is only fine-tuned on math reasoning, Sprint demonstrates strong generalization capabilities on the out-of-domain tasks, Countdown and GPQA-Diamond. Sprint also reduces sequential token count through parallelized executions without a large increase in total token count.

Comparison to conventional distillation. Figure [4](#S4.F4 "Figure 4 ‣ 4.2 Results ‣ 4 Experiments ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models") shows the accuracy and average number of sequential tokens generated by different methods on the MATH-500 benchmark. We observe that fine-tuning our base model (R1-Distill-7B) on trajectories generated by DeepSeek-R1 improves the accuracy of both Sprint and RFT, albeit with an increase in their average sequential token counts. The accuracy gains are substantial, bringing both models close to the performance of the much larger R1-Distill-32B reasoning model. Notably, Sprint achieves a higher accuracy of 92.5%, which can be attributed to independent executions within each stage that prevent one result from influencing the others. Despite being fine-tuned on the same trajectories as RFT, reorganized in a plan–execution format, Sprint requires 440 (∼15%\sim 15\%) fewer sequential tokens due to parallelized executions. These results demonstrate that Sprint achieves the same level of reasoning accuracy as conventional distillation used in RFT while substantially reducing the sequential token count.

Effectiveness of interleaved planning.
The SoT-reasoning baseline underperforms Sprint in both accuracy and the number of sequential tokens. Since SoT only allows a single round of planning and uses a model without task-specific fine-tuning, it often generates mutually dependent subtasks. When the model executes them independently in parallel, it cannot use the result of one execution to inform another, resulting in redundant computations across subtasks and a total token count that is almost three times higher than Sprint (see Table [2](#S4.T2 "Table 2 ‣ 4.2 Results ‣ 4 Experiments ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models")). Similarly, repeated sampling with self-consistency generates multiple independent responses to the same query, leading to a high total token count. In contrast, Sprint uses interleaved planning and execution over multiple stages where the plan in each stage is generated based on the results of previous executions, allowing better coordination. Figure [5](#S4.F5 "Figure 5 ‣ 4.2 Results ‣ 4 Experiments ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models") illustrates patterns in Sprint’s interleaved planning. As expected, harder problems require more stages before reaching the final answer. Additionally, Sprint generates more plans in the earlier stages, as the model explores multiple strategies and identifies relevant subtasks, while later stages are more deterministic.

Reduction in sequential token count. We further examine the sequential token reduction achieved by Sprint relative to RFT in Figure [6](#S4.F6 "Figure 6 ‣ 4.2 Results ‣ 4 Experiments ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models"). For problems with short reasoning trajectories, the additional prompts and plan/execution tags introduce a small overhead, resulting in a 5% increase in sequential tokens. However, as problem difficulty increases and reasoning trajectories become longer, Sprint consistently reduces the sequential token count relative to the length of the RFT trajectory due to parallel executions. In particular, on problems where RFT requires more than 8,000 tokens on average, Sprint achieves a 39% reduction in sequential tokens.

Reduction in runtime. The savings in sequential tokens translate directly to lower latency. We estimate per-problem runtime by adding the time-to-first-token (TTFT) overhead incurred at the start of each plan/execution to the subsequent decoding time. In practice, decoding dominates; the prefilling (TTFT) cost is comparatively small. Under this estimate, Sprint outperforms RFT by 9% on MATH-500 (36.92s vs. 40.57s per problem) and by 38% on the subset with longer reasoning chains (74.47s vs. 120.54s). Because runtime scales primarily with the number of decoded tokens, Sprint’s advantage increases with trajectory length, yielding larger absolute and relative latency reductions on harder instances.

Generalization. To assess Sprint’s generalization capabilities to out-of-domain tasks, we report performance on Countdown and GPQA-Diamond in Table [2](#S4.T2 "Table 2 ‣ 4.2 Results ‣ 4 Experiments ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models"). Sprint leverages the highly parallelizable nature of the Countdown task to solve problems with much fewer sequential tokens (2284 tokens compared to 4917 tokens by RFT), demonstrating a 53.5% reduction. Notably, these parallelization opportunities are identified despite not being trained on trajectories from this task. Due to the benefits of independent exploration and interleaved planning, Sprint also beats all baseline methods to achieve an accuracy of 85.9%. Similarly, on the GPQA-Diamond dataset, Sprint achieves the highest accuracy (51.0%) while reducing sequential token count by 10.8% relative to RFT. Similar to MATH-500, we observe from Figure [6](#S4.F6 "Figure 6 ‣ 4.2 Results ‣ 4 Experiments ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models") that Sprint provides higher efficiency gains on problems with longer reasoning chains.

Figure 6: Sequential token reduction achieved by Sprint. The x-axis shows the number of sequential tokens generated by the RFT baseline model, and the y-axis indicates the average reduction in sequential tokens achieved by Sprint. As the baseline’s sequential requirements increase, Sprint finds greater opportunities for parallelization, yielding larger sequential token reductions.

## 5 Limitations and Future work

Hardware optimization for realized wall-clock time speed-up.
Sprint delivers clear efficiency gains, reducing sequential tokens and lowering our end-to-end runtime approximation, but fully realizing these benefits in wall-clock time requires hardware-aware optimizations. Previous works [Jin et al. (2025)](#bib.bib29); [Rodionov et al. (2025)](#bib.bib30); [Pan et al. (2025)](#bib.bib31) have indicated that sequential token counts are closely correlated with wall-clock latency. However, achieving the ideal latency improvements in practice requires optimized key-value caching mechanisms and high-bandwidth GPU interconnects, especially for long reasoning trajectories encountered in general tasks. Additionally, executing a large number of parallel tasks simultaneously necessitates a corresponding number of GPUs. Due to limited resources, we were unable to implement the optimal hardware-accelerated decoding for Sprint. Future work could explore implementing Sprint within optimized caching frameworks and scalable GPU architectures to fully realize practical wall-clock time efficiency gains offered by parallel decoding strategies.

Parallelizing tool-use in reasoning models.
In our current work, we primarily treat executions as sequences of tokens that models decode to accomplish tasks. However, from a planning perspective, these executions can alternatively be viewed as black-box modules that receive specific tasks and return corresponding execution results. Several prior works, such as ReAct [Yao et al. (2023b)](#bib.bib5), Self-Ask [Press et al. (2023)](#bib.bib26), Swirl [Goldie et al. (2025)](#bib.bib22), and others [Shi et al. (2025)](#bib.bib23); [Shen et al. (2023)](#bib.bib24); [Paranjape et al. (2023)](#bib.bib25), have introduced mechanisms enabling language models to integrate tool-use into their reasoning loops, iteratively planning, invoking external tools or APIs, and then continuing their reasoning based on the obtained results. Such reasoning-tool interaction trajectories could significantly benefit from parallelization, especially in scenarios where tool invocations dominate the decoding latency. Future work could extend Sprint’s data curation pipeline to accommodate these trajectories, training models to effectively invoke multiple tools or APIs concurrently within their reasoning processes.

Beyond Supervised Training. Through supervised fine-tuning (SFT) on curated data, our model learned how to define parallelizable plans, effectively reducing sequential token generation. However, the achievable parallelism is inherently limited by the quality of training data. Future work could explore latency-aware reinforcement learning (RL), using reward signals based on inference efficiency, allowing models to autonomously discover strategies that further enhance parallel reasoning beyond the constraints of demonstration data.

## 6 Conclusion

In this work, we presented Sprint, a framework for post-training reasoning language models that reorganizes their reasoning trajectories into a series of plans and parallelized executions. Additionally, Sprint introduces an inference mechanism that leverages the trained reasoning model to identify independent subtasks and execute them in parallel. This approach significantly reduces the number of sequential tokens while achieving comparable state-of-the-art performance to the reasoning fine-tuned (RFT) model. Notably, on problems requiring extensive reasoning trajectories, Sprint uncovers even greater parallelization potential, achieving sequential token reductions of 39%. Furthermore, we evaluated our model’s generalization on multiple out-of-domain tasks and consistently found that Sprint generates substantially fewer sequential tokens while maintaining performance on par with RFT. These results suggest that the Sprint training unlocks parallelized reasoning capabilities in the model across diverse domains with longer reasoning trajectories.

## 7 Acknowledgment

This work was supported in part by the Air Force Office of Scientific Research (AFOSR) under Grant FA9550-23-1-0251 and in part by the Office of Naval Research under Grant N00014-24-1-2164. We also thank Yuhao Ge at the University of Illinois Urbana-Champaign for his guidance on the model training process and computing requirements.

## References

- Besta et al. (2024)
  M. Besta, N. Blach, A. Kubicek, R. Gerstenberger, M. Podstawski, L. Gianinazzi, J. Gajda, T. Lehmann, H. Niewiadomski, P. Nyczyk, et al.
  Graph of thoughts: solving elaborate problems with large language models.
  In Proceedings of the AAAI Conference on Artificial Intelligence,
  Vol. 38, pp. 17682–17690.
  Cited by: [§1](#S1.p1.1 "1 Introduction ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models"),
  [Table 1](#S2.T1.6.1.3.1 "In 2 Related Work ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models"),
  [§2](#S2.p2.1 "2 Related Work ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models").
- Bi et al. (2025)
  Z. Bi, K. Han, C. Liu, Y. Tang, and Y. Wang
  Forest-of-thought: scaling test-time compute for enhancing llm reasoning.
  External Links: 2412.09078,
  [Link](https://arxiv.org/abs/2412.09078)
  Cited by: [§2](#S2.p2.1 "2 Related Work ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models").
- Brown et al. (2024)
  B. Brown, J. Juravsky, R. Ehrlich, R. Clark, Q. V. Le, C. Ré, and A. Mirhoseini
  Large language monkeys: scaling inference compute with repeated sampling.
  arXiv preprint arXiv:2407.21787.
  Cited by: [§1](#S1.p1.1 "1 Introduction ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models"),
  [Table 1](#S2.T1.6.1.5.1 "In 2 Related Work ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models"),
  [§4.1](#S4.SS1.p7.1 "4.1 Experimental Setup ‣ 4 Experiments ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models").
- Cobbe et al. (2021)
  K. Cobbe, V. Kosaraju, M. Bavarian, M. Chen, H. Jun, L. Kaiser, M. Plappert, J. Tworek, J. Hilton, R. Nakano, et al.
  Training verifiers to solve math word problems.
  arXiv preprint arXiv:2110.14168.
  Cited by: [§1](#S1.p1.1 "1 Introduction ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models"),
  [Table 1](#S2.T1.6.1.5.1 "In 2 Related Work ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models"),
  [§2](#S2.p4.1 "2 Related Work ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models").
- Dettmers et al. (2023)
  T. Dettmers, A. Pagnoni, A. Holtzman, and L. Zettlemoyer
  Qlora: efficient finetuning of quantized llms.
  Advances in neural information processing systems 36, pp. 10088–10115.
  Cited by: [§A.3](#A1.SS3.p1.1 "A.3 Fine-tuning ‣ Appendix A Implementation Details ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models").
- Du et al. (2023)
  Y. Du, S. Li, A. Torralba, J. B. Tenenbaum, and I. Mordatch
  Improving factuality and reasoning in language models through multiagent debate.
  In Forty-first International Conference on Machine Learning,
  Cited by: [§2](#S2.p2.1 "2 Related Work ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models").
- Goldie et al. (2025)
  A. Goldie, A. Mirhoseini, H. Zhou, I. Cai, and C. D. Manning
  Synthetic data generation & multi-step rl for reasoning & tool use.
  External Links: 2504.04736,
  [Link](https://arxiv.org/abs/2504.04736)
  Cited by: [§5](#S5.p2.1 "5 Limitations and Future work ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models").
- Guo et al. (2025)
  D. Guo, D. Yang, H. Zhang, J. Song, R. Zhang, R. Xu, Q. Zhu, S. Ma, P. Wang, X. Bi, et al.
  Deepseek-r1: incentivizing reasoning capability in llms via reinforcement learning.
  arXiv preprint arXiv:2501.12948.
  Cited by: [§A.1](#A1.SS1.SSS0.Px1.p1.1 "Inference from a sequential reasoning model. ‣ A.1 Inference ‣ Appendix A Implementation Details ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models"),
  [§1](#S1.p1.1 "1 Introduction ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models"),
  [§1](#S1.p5.1 "1 Introduction ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models"),
  [Table 1](#S2.T1.6.1.6.1 "In 2 Related Work ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models"),
  [§2](#S2.p1.1 "2 Related Work ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models"),
  [§3.2](#S3.SS2.p2.1 "3.2 Training Reasoning Models for Sprint Framework ‣ 3 Methodology ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models"),
  [§4.1](#S4.SS1.p1.1 "4.1 Experimental Setup ‣ 4 Experiments ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models"),
  [§4.1](#S4.SS1.p4.1 "4.1 Experimental Setup ‣ 4 Experiments ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models").
- Hendrycks et al. (2021)
  D. Hendrycks, C. Burns, S. Kadavath, A. Arora, S. Basart, E. Tang, D. Song, and J. Steinhardt
  Measuring mathematical problem solving with the math dataset.
  External Links: 2103.03874,
  [Link](https://arxiv.org/abs/2103.03874)
  Cited by: [§4.1](#S4.SS1.p1.1 "4.1 Experimental Setup ‣ 4 Experiments ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models").
- Hu et al. (2022)
  E. J. Hu, Y. Shen, P. Wallis, Z. Allen-Zhu, Y. Li, S. Wang, L. Wang, W. Chen, et al.
  Lora: low-rank adaptation of large language models..
  ICLR 1 (2), pp. 3.
  Cited by: [§A.3](#A1.SS3.p1.1 "A.3 Fine-tuning ‣ Appendix A Implementation Details ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models").
- Jin et al. (2025)
  T. Jin, E. Y. Cheng, Z. Ankner, N. Saunshi, B. M. Elias, A. Yazdanbakhsh, J. Ragan-Kelley, S. Subramanian, and M. Carbin
  Learning to keep a promise: scaling language model decoding parallelism with learned asynchronous decoding.
  External Links: 2502.11517,
  [Link](https://arxiv.org/abs/2502.11517)
  Cited by: [Table 1](#S2.T1.6.1.7.1 "In 2 Related Work ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models"),
  [§2](#S2.p5.1 "2 Related Work ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models"),
  [§5](#S5.p1.1 "5 Limitations and Future work ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models").
- Juneja et al. (2024)
  G. Juneja, S. Dutta, S. Chakrabarti, S. Manchanda, and T. Chakraborty
  Small language models fine-tuned to coordinate larger language models improve complex reasoning.
  External Links: 2310.18338,
  [Link](https://arxiv.org/abs/2310.18338)
  Cited by: [§2](#S2.p3.1 "2 Related Work ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models").
- Kim et al. (2024)
  S. Kim, S. Moon, R. Tabrizi, N. Lee, M. W. Mahoney, K. Keutzer, and A. Gholami
  An llm compiler for parallel function calling.
  In Forty-first International Conference on Machine Learning,
  Cited by: [§2](#S2.p2.1 "2 Related Work ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models").
- Kwon et al. (2023)
  W. Kwon, Z. Li, S. Zhuang, Y. Sheng, L. Zheng, C. H. Yu, J. Gonzalez, H. Zhang, and I. Stoica
  Efficient memory management for large language model serving with pagedattention.
  In Proceedings of the 29th Symposium on Operating Systems Principles,
  pp. 611–626.
  Cited by: [§A.4](#A1.SS4.p1.1 "A.4 Evaluation ‣ Appendix A Implementation Details ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models").
- Lightman et al. (2023a)
  H. Lightman, V. Kosaraju, Y. Burda, H. Edwards, B. Baker, T. Lee, J. Leike, J. Schulman, I. Sutskever, and K. Cobbe
  Let’s verify step by step.
  arXiv preprint arXiv:2305.20050.
  Cited by: [§4.1](#S4.SS1.p2.1 "4.1 Experimental Setup ‣ 4 Experiments ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models").
- Lightman et al. (2023b)
  H. Lightman, V. Kosaraju, Y. Burda, H. Edwards, B. Baker, T. Lee, J. Leike, J. Schulman, I. Sutskever, and K. Cobbe
  Let’s verify step by step.
  External Links: 2305.20050,
  [Link](https://arxiv.org/abs/2305.20050)
  Cited by: [§1](#S1.p1.1 "1 Introduction ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models"),
  [§1](#S1.p5.1 "1 Introduction ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models"),
  [§2](#S2.p4.1 "2 Related Work ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models").
- Liu et al. (2024)
  M. Liu, A. Zeng, B. Wang, P. Zhang, J. Tang, and Y. Dong
  APAR: llms can do auto-parallel auto-regressive decoding.
  External Links: 2401.06761,
  [Link](https://arxiv.org/abs/2401.06761)
  Cited by: [§2](#S2.p4.1 "2 Related Work ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models").
- Ning et al. (2023)
  X. Ning, Z. Lin, Z. Zhou, Z. Wang, H. Yang, and Y. Wang
  Skeleton-of-thought: prompting llms for efficient parallel generation.
  arXiv preprint arXiv:2307.15337.
  Cited by: [1st item](#A1.I10.i1.p1.1 "In A.5 Baselines ‣ Appendix A Implementation Details ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models"),
  [Table 1](#S2.T1.6.1.4.1 "In 2 Related Work ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models"),
  [§2](#S2.p4.1 "2 Related Work ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models"),
  [§4.1](#S4.SS1.p6.1 "4.1 Experimental Setup ‣ 4 Experiments ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models").
- open-r1 (2025)
  open-r1
  OpenThoughts-114k-math.
  External Links: [Link](https://huggingface.co/datasets/open-r1/OpenThoughts-114k-math)
  Cited by: [§4.1](#S4.SS1.p1.1 "4.1 Experimental Setup ‣ 4 Experiments ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models").
- OpenAI (2024)
  OpenAI
  Learning to reason with llms.
  External Links: [Link](https://openai.com/index/learning-to-reason-with-llms/)
  Cited by: [§1](#S1.p1.1 "1 Introduction ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models"),
  [Table 1](#S2.T1.6.1.6.1 "In 2 Related Work ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models"),
  [§2](#S2.p1.1 "2 Related Work ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models").
- Pan et al. (2025)
  J. Pan, X. Li, L. Lian, C. Snell, Y. Zhou, A. Yala, T. Darrell, K. Keutzer, and A. Suhr
  Learning adaptive parallel reasoning with language models.
  External Links: 2504.15466,
  [Link](https://arxiv.org/abs/2504.15466)
  Cited by: [§2](#S2.p5.1 "2 Related Work ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models"),
  [§4.1](#S4.SS1.p2.1 "4.1 Experimental Setup ‣ 4 Experiments ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models"),
  [§5](#S5.p1.1 "5 Limitations and Future work ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models").
- Paranjape et al. (2023)
  B. Paranjape, S. Lundberg, S. Singh, H. Hajishirzi, L. Zettlemoyer, and M. T. Ribeiro
  ART: automatic multi-step reasoning and tool-use for large language models.
  External Links: 2303.09014,
  [Link](https://arxiv.org/abs/2303.09014)
  Cited by: [§5](#S5.p2.1 "5 Limitations and Future work ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models").
- Prasad et al. (2024)
  A. Prasad, A. Koller, M. Hartmann, P. Clark, A. Sabharwal, M. Bansal, and T. Khot
  ADaPT: as-needed decomposition and planning with language models.
  External Links: 2311.05772,
  [Link](https://arxiv.org/abs/2311.05772)
  Cited by: [§2](#S2.p3.1 "2 Related Work ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models").
- Press et al. (2023)
  O. Press, M. Zhang, S. Min, L. Schmidt, N. A. Smith, and M. Lewis
  Measuring and narrowing the compositionality gap in language models.
  External Links: 2210.03350,
  [Link](https://arxiv.org/abs/2210.03350)
  Cited by: [§5](#S5.p2.1 "5 Limitations and Future work ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models").
- Rajbhandari et al. (2020)
  S. Rajbhandari, J. Rasley, O. Ruwase, and Y. He
  Zero: memory optimizations toward training trillion parameter models.
  In SC20: International Conference for High Performance Computing, Networking, Storage and Analysis,
  pp. 1–16.
  Cited by: [§A.3](#A1.SS3.p4.1 "A.3 Fine-tuning ‣ Appendix A Implementation Details ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models").
- Rasley et al. (2020)
  J. Rasley, S. Rajbhandari, O. Ruwase, and Y. He
  Deepspeed: system optimizations enable training deep learning models with over 100 billion parameters.
  In Proceedings of the 26th ACM SIGKDD international conference on knowledge discovery & data mining,
  pp. 3505–3506.
  Cited by: [§A.3](#A1.SS3.p4.1 "A.3 Fine-tuning ‣ Appendix A Implementation Details ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models").
- Rein et al. (2023)
  D. Rein, B. L. Hou, A. C. Stickland, J. Petty, R. Y. Pang, J. Dirani, J. Michael, and S. R. Bowman
  GPQA: a graduate-level google-proof q&a benchmark.
  External Links: 2311.12022,
  [Link](https://arxiv.org/abs/2311.12022)
  Cited by: [§1](#S1.p5.1 "1 Introduction ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models"),
  [§4.1](#S4.SS1.p2.1 "4.1 Experimental Setup ‣ 4 Experiments ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models").
- Rodionov et al. (2025)
  G. Rodionov, R. Garipov, A. Shutova, G. Yakushev, V. Egiazarian, A. Sinitsin, D. Kuznedelev, and D. Alistarh
  Hogwild! inference: parallel llm generation via concurrent attention.
  External Links: 2504.06261,
  [Link](https://arxiv.org/abs/2504.06261)
  Cited by: [Table 1](#S2.T1.6.1.8.1 "In 2 Related Work ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models"),
  [§2](#S2.p5.1 "2 Related Work ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models"),
  [§5](#S5.p1.1 "5 Limitations and Future work ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models").
- Saad-Falcon et al. (2024)
  J. Saad-Falcon, A. G. Lafuente, S. Natarajan, N. Maru, H. Todorov, E. Guha, E. K. Buchanan, M. Chen, N. Guha, C. Ré, and A. Mirhoseini
  Archon: an architecture search framework for inference-time techniques.
  External Links: 2409.15254,
  [Link](https://arxiv.org/abs/2409.15254)
  Cited by: [§2](#S2.p2.1 "2 Related Work ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models").
- Shen et al. (2023)
  Y. Shen, K. Song, X. Tan, D. Li, W. Lu, and Y. Zhuang
  HuggingGPT: solving ai tasks with chatgpt and its friends in hugging face.
  External Links: 2303.17580,
  [Link](https://arxiv.org/abs/2303.17580)
  Cited by: [§5](#S5.p2.1 "5 Limitations and Future work ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models").
- Shi et al. (2025)
  Z. Shi, S. Gao, L. Yan, Y. Feng, X. Chen, Z. Chen, D. Yin, S. Verberne, and Z. Ren
  Tool learning in the wild: empowering language models as automatic tool agents.
  External Links: 2405.16533,
  [Link](https://arxiv.org/abs/2405.16533)
  Cited by: [§5](#S5.p2.1 "5 Limitations and Future work ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models").
- Shinn et al. (2023)
  N. Shinn, F. Cassano, E. Berman, A. Gopinath, K. Narasimhan, and S. Yao
  Reflexion: language agents with verbal reinforcement learning.
  External Links: 2303.11366,
  [Link](https://arxiv.org/abs/2303.11366)
  Cited by: [§2](#S2.p3.1 "2 Related Work ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models").
- Teng et al. (2025)
  F. Teng, Z. Yu, Q. Shi, J. Zhang, C. Wu, and Y. Luo
  Atom of thoughts for markov llm test-time scaling.
  arXiv preprint arXiv:2502.12018.
  Cited by: [§2](#S2.p2.1 "2 Related Work ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models").
- Valmeekam et al. (2023)
  K. Valmeekam, S. Sreedharan, M. Marquez, A. Olmo, and S. Kambhampati
  On the planning abilities of large language models (a critical investigation with a proposed benchmark).
  External Links: 2302.06706,
  [Link](https://arxiv.org/abs/2302.06706)
  Cited by: [§2](#S2.p3.1 "2 Related Work ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models").
- [35]
  X. Wang, J. Wei, D. Schuurmans, Q. V. Le, E. H. Chi, S. Narang, A. Chowdhery, and D. Zhou
  Self-consistency improves chain of thought reasoning in language models.
  In The Eleventh International Conference on Learning Representations,
  Cited by: [§1](#S1.p1.1 "1 Introduction ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models"),
  [Table 1](#S2.T1.6.1.5.1 "In 2 Related Work ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models"),
  [§2](#S2.p4.1 "2 Related Work ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models"),
  [§4.1](#S4.SS1.p7.1 "4.1 Experimental Setup ‣ 4 Experiments ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models").
- Wei et al. (2023)
  J. Wei, X. Wang, D. Schuurmans, M. Bosma, B. Ichter, F. Xia, E. Chi, Q. Le, and D. Zhou
  Chain-of-thought prompting elicits reasoning in large language models.
  External Links: 2201.11903,
  [Link](https://arxiv.org/abs/2201.11903)
  Cited by: [§1](#S1.p1.1 "1 Introduction ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models"),
  [§2](#S2.p1.1 "2 Related Work ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models").
- Yang et al. (2024)
  A. Yang, B. Yang, B. Zhang, B. Hui, B. Zheng, B. Yu, C. Li, D. Liu, F. Huang, H. Wei, et al.
  Qwen2. 5 technical report.
  arXiv preprint arXiv:2412.15115.
  Cited by: [§4.1](#S4.SS1.p4.1 "4.1 Experimental Setup ‣ 4 Experiments ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models").
- Yao et al. (2023a)
  S. Yao, D. Yu, J. Zhao, I. Shafran, T. Griffiths, Y. Cao, and K. Narasimhan
  Tree of thoughts: deliberate problem solving with large language models.
  Advances in neural information processing systems 36, pp. 11809–11822.
  Cited by: [§1](#S1.p1.1 "1 Introduction ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models"),
  [§1](#S1.p5.1 "1 Introduction ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models"),
  [Table 1](#S2.T1.6.1.2.1 "In 2 Related Work ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models"),
  [§2](#S2.p2.1 "2 Related Work ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models"),
  [§4.1](#S4.SS1.p2.1 "4.1 Experimental Setup ‣ 4 Experiments ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models").
- Yao et al. (2023b)
  S. Yao, J. Zhao, D. Yu, N. Du, I. Shafran, K. Narasimhan, and Y. Cao
  React: synergizing reasoning and acting in language models.
  In International Conference on Learning Representations (ICLR),
  Cited by: [§2](#S2.p3.1 "2 Related Work ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models"),
  [§5](#S5.p2.1 "5 Limitations and Future work ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models").
- Zelikman et al. (2022)
  E. Zelikman, Y. Wu, J. Mu, and N. Goodman
  Star: bootstrapping reasoning with reasoning.
  Advances in Neural Information Processing Systems 35, pp. 15476–15488.
  Cited by: [§2](#S2.p1.1 "2 Related Work ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models").
- Zhao et al. (2024)
  Y. Zhao, J. Huang, J. Hu, X. Wang, Y. Mao, D. Zhang, Z. Jiang, Z. Wu, B. Ai, A. Wang, W. Zhou, and Y. Chen
  SWIFT:a scalable lightweight infrastructure for fine-tuning.
  External Links: 2408.05517,
  [Link](https://arxiv.org/abs/2408.05517)
  Cited by: [§A.3](#A1.SS3.p2.1 "A.3 Fine-tuning ‣ Appendix A Implementation Details ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models").
- Zhou et al. (2022)
  D. Zhou, N. Schärli, L. Hou, J. Wei, N. Scales, X. Wang, D. Schuurmans, C. Cui, O. Bousquet, Q. Le, et al.
  Least-to-most prompting enables complex reasoning in large language models.
  arXiv preprint arXiv:2205.10625.
  Cited by: [§2](#S2.p3.1 "2 Related Work ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models").
- Zhu et al. (2023)
  B. Zhu, H. Sharma, F. V. Frujeri, S. Dong, C. Zhu, M. I. Jordan, and J. Jiao
  Fine-tuning language models with advantage-induced policy alignment.
  arXiv preprint arXiv:2306.02231.
  Cited by: [§2](#S2.p1.1 "2 Related Work ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models").
- Zhuge et al. (2024)
  M. Zhuge, W. Wang, L. Kirsch, F. Faccio, D. Khizbullin, and J. Schmidhuber
  GPTSwarm: language agents as optimizable graphs.
  In Proceedings of the 41st International Conference on Machine Learning,
  Cited by: [§2](#S2.p2.1 "2 Related Work ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models").

## Appendix A Implementation Details

### A.1 Inference

#### Inference from a sequential reasoning model.

To generate responses from sequential reasoning models, such as DeepSeek-R1-Distill-7B and the RFT model, we use the prompt provided below. The same prompt was used for fine-tuning DeepSeek-R1-Distill-7B to derive the RFT model. During inference, the question is appended to the prompt and the model is called in the completions format. Following guidelines suggested by DeepSeek [[8](#bib.bib2)], we set the generation temperature to 0.6 to mitigate repetitive outputs. Additionally, we enforce a maximum token limit of 36,000 per response, truncating any outputs exceeding this threshold.

Sequential Reasoning Prompt

Your role as an assistant involves thoroughly exploring questions through a systematic long thinking process before providing the final precise and accurate solutions. This requires engaging in a comprehensive cycle of analysis, summarizing, exploration, reassessment, reflection, backtracking, and iteration to develop well-considered thinking process.
  
Please structure your response into two main sections: Thought and Solution.

•

In the Thought section, detail your reasoning process using the specified format: <think> {thought with steps separated with "\n \n"} </think> Each step should include detailed considerations such as analyzing questions, summarizing relevant findings, brainstorming new ideas, verifying the accuracy of the current steps, refining any errors, and revisiting previous steps.
•

In the Solution section, based on various attempts, explorations, and reflections from the Thought section, systematically present the final solution that you deem correct. The solution should remain a logical, accurate, concise expression style and detail necessary step needed to reach the conclusion.
Now, try to solve the following question through the above guidelines. Return your final response within \boxed{}.

#### SPRINT Inference.

During inference, we use the following prompt to guide the generation of plans and executions from the SPRINT model. Although the model is fine-tuned to produce an entire trajectory—including all plans and executions—in a single generation, we manage model invocations and output token handling to alternate between planner and executor roles effectively.

To restrict the model’s outputs to either a single plan or execution per invocation, we employ specific stop tokens. Generation is terminated once the model produces any of the following strings, indicating the completion of a plan or execution segment: {</Execution_, </Plan_, </Final_answer>, </execution_}.

When generating a plan for stage ii, we feed the prompt along with the input query and the cumulative context, which includes all preceding plans and executions, to the Sprint model. Conversely, to generate the execution corresponding to a particular prompt_i.j, we provide the model with the prompt, the input query, all previously generated plans and executions up to stage i−1i-1, and the text from plan ii until the end of prompt_i.j. This structured context management allows us to reuse the same prompt for both planning and execution tasks seamlessly.

The model is permitted a maximum of 12 stages to produce a final answer. To enforce this constraint, we append "<Final_answer>\n" at the end of the prompt when invoking the model at the 12th stage. Generated responses for each plan or execution are limited to 8,000 tokens, with any excess tokens truncated accordingly. This prompt is identical to that used during model fine-tuning.

SPRINT Prompt

You are an AI system that follows a systematic long thinking process to arrive at the precise and accurate answer to the below math question specified within <Question> and </Question> tags. The solution is generated over multiple phases, where each phase consists of a plan and an execution.
  

#### Planning.

At phase p, you must first create a plan within <Plan_p> and </Plan_p> tags by thinking out loud and planning the tasks that need to be executed next.

•

Your plan may involve detailed considerations such as analyzing the question, summarizing relevant findings, brainstorming new/alternative approaches, verifying the accuracy of the current steps, refining any errors, or revisiting previous steps.
•

Since you may think about multiple aspects of the problem within the same plan, you must insert a line break using "- - - - -" before you transition from one train of thought to another.
•

While generating the plan, if you identify a task that needs to be executed, you must create a prompt that clearly specifies the task within <prompt_p.k> and </prompt_p.k> tags where k starts from 1.
•

When planning within each phase, you must create prompts that can be run independent of the results from the other prompts, to achieve speedup through parallelization. You must also try to minimize the number of phases required further to arrive at the accurate final answer.

#### Execution.

After creating the plan, you must carry out the tasks identified in the plan sequentially within <Execution_p> and </Execution_p> tags. For the prompt labeled as prompt_p.k, the corresponding execution must be generated within <execution_p.k> and </execution_p.k> tags.
  

If the plans and execution results you receive are sufficient to generate the accurate final answer, you must respond with the final answer within <Final_answer> and </Final_answer> tags. The numerical answer must be within \boxed{}.

### A.2 Dataset Curation

#### Step Extraction.

For step extraction, we use the GPT-4o model with the temperature set to 0. The following prompt is used to extract steps from a reasoning trajectory generated by DeepSeek R1. In the prompt, we use the term "Component" to refer to the extracted steps to prevent the model from confusing it with the traditional use of the term "step" in a math solution which could be a single operation as opposed to a logical part of the solution. Components, as defined here, may involve tasks such as identifying subsequent actions, validating previous results, proposing alternative methods, or comparing solutions derived through different strategies. For each component, the model starts by thinking out loud about what needs to be done and then carries out the identified task. We refer to the first part as the plan and the second as the execution and extract them separately using this prompt.

The reasoning trajectory passed to the model as input is formatted by labeling each line/sentence with a unique line number and the model provides the range of line numbers for each plan and execution within a component. This minimizes the number of output tokens that have to be generated by the model, consequently reducing costs. The line numbers are later parsed from the response to infer the block of text that is relevant to each plan or execution.

Step Extraction Prompt

Given below is a math problem and a well-thought out solution to the problem generated by an AI model. The solution contains multiple components (progressing with next steps, verifying past steps, proposing alternative methods, comparing solutions across different methods, etc.). Within each component, there are three phases:

•

Planning: Here, the model first thinks out loud and plans what it needs to do.
•

Execution: Here,the model follows the plan and executes it.
•

Commenting: Here, the model comments on the execution results with phrases such as "Yes, that seems right", "Both methods lead to the same answer, etc.
Note that the verification of an execution should be considered as a separate component and not as the commenting phase of the same component.
  
I am building a new AI system to solve such math problems. This system will consist of two separate AI models – a planner and an executor.

•

Planner: The planner will receive all the components of the solution completed so far and will need to think aloud and generate a plan for the next component. Then, it needs to provide a prompt to the executor model to execute a specific task.
•

Executor: The executor will receive all the components of the solution completed so far, the plan for the next component generated by the planner, and the prompt generated by the planner. It will need to execute the specified task.
To train these two AI models, I must generate training data by breaking down the solution provided below into individual components. For each component, clearly provide the following details:

Required Response Format:
### Component X (Line Number Range)

•

Description: Brief explanation of what this component achieves.
•

Plan: Lines (minimal number of lines to describe the plan clearly).
•

Prompt: A precise, actionable instruction for the executor based explicitly on the above plan.
•

Execution: Lines (specific line numbers performing the planned task).
•

Comment: Lines (reflective comments or Lines not found if missing).

Important Notes:

•

The planning phase should only include a minimal number of lines required to specify what needs to be done. The remaining lines from the component where the model carries out the plan should be included in the execution phase.
•

There MUST be NO overlap between the line numbers of different components.
•

There MUST be NO overlap between the line numbers of the planning and execution phases of the same component.
•

All the lines in the solution should be covered by the components.
•

Use the line number mentioned at the start and end of each line to identify the line when specifying the line number range.
•

The prompt to the executor model must be a very specific instruction that the executor can follow to complete the required task. The executor must not perform more tasks than required. The prompt can refer to the plan for that component by saying "the above plan".
•

If the model does not comment on the execution results within a component, the corresponding bullet point can be written as Comment: Lines not found

#### DAG Creation.

For DAG creation, we use the GPT-4o-mini model with the temperature set to 0. The following prompt is used to infer the DAG in the form of a parent dictionary, where each key refers to a step extracted above and the corresponding values refer to the steps on which the key depends.

DAG Creation Prompt

Given below is a well-thought out solution to a math problem generated by an AI system. The system consists of a planner and an executor. The planner model thinks out loud and plans the next component of the problem solution. Then, it provides a prompt along with the plan to an executor model. The executor then follows the instructions in the prompt and uses context from the plan to carry out the given task.
The solution consists of multiple components, each containing the following:

•

Description: A brief description of what the component does.
•

Plan: The plan generated by the planner.
•

Prompt: Instructions generated by the planner enclosed within <prompt> tags.
•

Execution: Output provided by the executor.
Though the executions are run sequentially in this solution, some of the executions may be parallelized to improve speed. Identify and explain which components can run in parallel and determine the best way to parallelize them to maximize speed. Note that parallel runs should not have co-dependency.
  
The parallelization schedule can be represented as a directed acyclic graph (DAG) where the nodes are the component numbers. You need to represent the DAG as a parent dictionary where each node is a key and its value is a list of nodes that point to it, i.e., the nodes that must be executed immediately before it. For a key node, do not include any nodes in its value that can be run in parallel with it.
  
Format of parent dictionary:
  
Let us consider a simple example. Suppose that the following constraints hold:

•

Component 1 needs to be run before any other component
•

Components 2, 3, 4 can be run in parallel after 1
•

Component 5 which depends on the results of 2 and 3 can be run after 2 and 3
•

Component 6 which depends on the results of 4 and 5 can be run after 4 and 5
The parent dictionary for this example *MUST* be represented as a python dictionary as follows:

```
parent_dictionary = {
    1: [],
    2: [1],
    3: [1],
    4: [1],
    5: [2, 3],
    6: [4, 5]
}
```

Using the resulting DAG, we can reorganize the components into interleaved plans and executions to obtain a parallelizable reasoning trajectory. A simple strategy involves assigning components at the same DAG depth to the same planning-execution stage. However, further optimization can reduce the total number of stages required to reach the final answer.

#### Packing.

The objective of packing is to optimally assign stage numbers to each component. To achieve this, we apply the following greedy heuristics:

- •

  If a component’s execution consists of fewer than three lines, it is merged directly with its corresponding plan. This approach reduces overhead from additional prompt writing and executor invocation. Through fine-tuning on trajectories with merged short executions, the planner learns to carry out short or trivial executions on its own.
- •

  If a component CC depends on a plan-only component PP, then CC’s plan is independent of the execution results from PP’s stage. When all of CC’s parent components satisfy this condition, CC is merged into the same planning stage as PP by combining their respective plans.

As a result, we obtain optimal stage numbers for each component which can then be used for generating the fine-tuning trajectory.

### A.3 Fine-tuning

We conducted supervised fine-tuning (SFT) of our models by training on the reasoning trajectories. Initially, we experimented with more efficient fine-tuning techniques such as LoRA[[10](#bib.bib11)] and qLoRA [[5](#bib.bib12)]. However, since LoRA did not adequately enable the models to adhere to the desired response format, we proceed with full fine-tuning instead.

Fine-tuning was primarily executed on a single machine with eight NVIDIA A100 GPUs with 40 GB memory per GPU. We use the ms-swift framework [[41](#bib.bib13)], a fine-tuning toolkit provided by the Modelscope community.

Each model is fine-tuned for 5 epochs. Due to the long-context required for reasoning traces and the memory constraints, we use a batch size of 1 during the training. We use bfloat16 precision, an initial learning rate of 1×10−51\times 10^{-5}, and a weight decay factor of 1×10−41\times 10^{-4}. The learning rate scheduling consists of a linear warm-up phase during the first 5% of training steps, subsequently followed by linear decay to zero over the remaining training iterations. Model evaluation is conducted every 100 steps, and the best-performing model based on evaluation loss is retained.

To optimize memory usage during training, we integrate several efficiency strategies, notably the DeepSpeed ZeRO Redundancy Optimizer [[26](#bib.bib17), [25](#bib.bib18)] and 4-bit quantization. DeepSpeed’s ZeRO optimizer offers a set of memory-partitioning strategies that trade off memory savings against communication overhead. In many workloads, ZeRO Stage 1 or 2 strikes the best balance between memory efficiency and communication cost; however, since we need to train on long sequences, our per-GPU memory demands exceed what those stages can support. Therefore, we adopted ZeRO Stage 3 to train with extended context lengths without OOM errors.

### A.4 Evaluation

For model evaluation, we leverage vLLM [[14](#bib.bib38)] to serve our models. Specifically, each 7B-scale model (SPRINT, RFT, and DeepSeek-R1-Distill-7B) is deployed on a single NVIDIA A100 GPU with 40 GB of memory.

To enhance evaluation accuracy, we instruct the models to encapsulate their final answers within `\boxed{}`. For evaluations on the MATH-500 and Countdown tasks, we leverage the Math-Verify library alongside SymPy for equivalence checking, ensuring robustness against mathematically equivalent but differently expressed solutions. In the GPQA task, accuracy is determined by comparing explicitly generated option labels (e.g., A, B, C, D) directly with the corresponding ground-truth options.

Despite providing explicit formatting instructions, we occasional observe deviations by the models from the specified output format. For instance, during the Countdown task evaluation, the models occasionally produce outputs in unexpected formats (e.g., `\times`, ×\times), complicating the parsing procedure. To mitigate these issues, we incorporate the GPT-4o-mini model as an auxiliary evaluator to judge the generated answer against the ground truth.

### A.5 Baselines

Below we present the implementation details for the baselines used in our study:

- •

  SoT (Skeleton of Thought): For SoT-chat, we use the Qwen2.5-7B-Instruct model with the temperature set to 0.1. For SoT-reasoning, we use the DeepSeek-R1-Distill-Qwen-7B model with the temperature set to 0.6. We use the same prompts as reported in the original paper [[18](#bib.bib39)]. After the full solution is generated, we send it to GPT-4o-mini to extract the final answer for evaluation.
- •

  RFT (Reasoning Fine-tuned Model): This baseline was created by fine-tuning the DeepSeek model on sequential R1 trajectories. During inference, we set the temperature to 0.6 and employed the sequential reasoning prompt provided in Appendix [A.1](#A1.SS1 "A.1 Inference ‣ Appendix A Implementation Details ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models").
- •

  Parallel Sampling + Self-consistency: The Qwen2.5-7B-Instruct model was used with a temperature of 0.3, generating 20 independent samples per problem. The majority answer is considered as the predicted answer for the evaluation of this baseline.

## Appendix B Sample Demonstrations

### B.1 Demonstration of the Data Curation Pipeline

To illustrate our data curation pipeline, we examine a representative example from the MATH training dataset. Consider the following question:

Question: The vertex of the parabola described by the equation y=−3​x2−30​x−81y=-3x^{2}-30x-81 is (m,n)(m,n). What is nn?

Next, we provide the response generated by DeepSeek-R1 for this question with each logical component in a separate box. Note that the original response does not provide any separation among its logical components and the full text is generated as a single long trajectory.

Outline of DeepSeek-R1 response

Okay, so I need to find the vertex of the parabola given by the equation y=−3​x2−30​x−81y=-3x^{2}-30x-81, and specifically determine the nn-coordinate of the vertex, which is (m,n)(m,n). Hmm, let’s start by recalling how to find the vertex of a quadratic equation. I remember that quadratic equations are in the form y=a​x2+b​x+cy=ax^{2}+bx+c, and their graphs are parabolas. The vertex of a parabola can be found using the formula for the xx-coordinate, which is −b/(2a)-b/(2a). Then once we have the xx-coordinate, we can plug that back into the original equation to find the corresponding yy-coordinate, which would be nn in this case.
So let’s identify aa, bb, and cc from the given equation. Comparing y=−3​x2−30​x−81y=-3x^{2}-30x-81 with the standard form y=a​x2+b​x+cy=ax^{2}+bx+c, it looks like a=−3a=-3, b=−30b=-30, and c=−81c=-81.

Wait, is that right? Let me check again. The coefficient of x2x^{2} is −3-3, so a=−3a=-3. The coefficient of xx is −30-30, so b=−30b=-30. The constant term is −81-81, so c=−81c=-81. Okay, that seems correct.

Now, using the formula for the xx-coordinate of the vertex: m=−b/(2a)m=-b/(2a). Plugging in the values of aa and bb, we get m=−(−30)/(2∗(−3))m=-(-30)/(2*(-3)). Let’s compute that step by step. The numerator is −(−30)-(-30), which is positive 3030. The denominator is 22 times aa, which is 2∗(−3)=−62*(-3)=-6. So m=30/(−6)=−5m=30/(-6)=-5. Therefore, the xx-coordinate of the vertex is −5-5. That seems straightforward.

Now, to find the yy-coordinate nn, I need to substitute x=−5x=-5 into the original equation. Let’s do that. The original equation is y=−3​x2−30​x−81y=-3x^{2}-30x-81. Plugging in x=−5x=-5:
y=−3∗(−5)2−30∗(−5)−81y=-3*(-5)^{2}-30*(-5)-81. Let’s compute each term step by step. First, (−5)2(-5)^{2} is 2525, so −3∗25-3*25 is −75-75. Then, −30∗(−5)-30*(-5) is positive 150150. And the last term is −81-81. So adding them up: −75+150−81-75+150-81. Let’s calculate this.
First, −75+150=75-75+150=75. Then, 75−81=−675-81=-6. So n=−6n=-6. Therefore, the vertex is at (−5,−6)(-5,-6), so nn is −6-6.

Wait, let me double-check my calculations to make sure I didn’t make any arithmetic errors. Let’s redo the substitution.
Calculating yy when x=−5x=-5:
First term: −3∗(−5)2-3*(-5)^{2}. The exponent first: (−5)2=25(-5)^{2}=25. Then multiply by −3-3: −3∗25=−75-3*25=-75. Second term: −30∗(−5)-30*(-5). Multiply those: −30-30 times −5-5 is 150150. Third term is −81-81. So adding them: −75+150=75-75+150=75; 75−81=−675-81=-6. Yep, that’s correct.

Alternatively, maybe I can use another method to confirm. Sometimes, completing the square can be a good way to find the vertex. Let me try that. The given equation is y=−3​x2−30​x−81y=-3x^{2}-30x-81. To complete the square, first factor out the coefficient of x2x^{2} from the first two terms. So:
y=−3​(x2+10​x)−81y=-3(x^{2}+10x)-81. Wait, let’s check: −3​x2−30​x-3x^{2}-30x becomes −3​(x2+10​x)-3(x^{2}+10x). Yes, that’s correct because −3-3 times x2x^{2} is −3​x2-3x^{2} and −3-3 times 10​x10x is −30​x-30x. Then, we have the remaining constant term as −81-81.
Now, to complete the square inside the parentheses, we need to take half of the coefficient of xx, which is 1010, so half of 1010 is 55, and then square it: 52=255^{2}=25. So we add and subtract 2525 inside the parentheses to maintain equality. However, since we are adding 2525 inside the parentheses that’s multiplied by −3-3, we have to balance that by actually adding and subtracting −3∗25-3*25 to the entire equation. Wait, maybe I need to write it out more carefully.
So:
y=−3​(x2+10​x+25−25)−81y=-3(x^{2}+10x+25-25)-81
Wait, that is equivalent to:
y=−3​[(x2+10​x+25)−25]−81y=-3[(x^{2}+10x+25)-25]-81
Which simplifies to:
y=−3​(x+5)2+75−81y=-3(x+5)^{2}+75-81
Because (x2+10​x+25)(x^{2}+10x+25) is (x+5)2(x+5)^{2}, and then we have −3-3 times −25-25 which is +75+75. Then, subtract 8181. So:
y=−3​(x+5)2+75−81y=-3(x+5)^{2}+75-81
Then, combining the constants: 75−81=−675-81=-6. So the equation becomes:
y=−3​(x+5)2−6y=-3(x+5)^{2}-6
Which is in vertex form: y=a​(x−h)2+ky=a(x-h)^{2}+k, where the vertex is (h,k)(h,k). Wait, in this case, it’s (x+5)(x+5) which is the same as (x−(−5))(x-(-5)), so hh is −5-5 and kk is −6-6. Therefore, the vertex is at (−5,−6)(-5,-6), so nn is −6-6. That confirms the previous result.

Alternatively, maybe I can use calculus, taking the derivative and setting it to zero, but since this is a simple quadratic, that might be overkill. But for thoroughness, let’s try it. The derivative of yy with respect to xx is d​y/d​x=2∗(−3)​x+(−30)=−6​x−30dy/dx=2*(-3)x+(-30)=-6x-30. Setting this equal to zero for critical points: −6​x−30=0-6x-30=0. Solving for xx: −6​x=30⇒x=−5-6x=30\Rightarrow x=-5. Then substitute x=−5x=-5 into original equation, as before, gives y=−6y=-6. So again, same result.

Therefore, all three methods (vertex formula, completing the square, calculus) lead to the same answer: n=−6n=-6.

Is there any chance I made a mistake in the signs? Let me check again. The original equation is y=−3​x2−30​x−81y=-3x^{2}-30x-81. So a=−3a=-3, b=−30b=-30. Then the xx-coordinate of vertex is −b/(2a)=−(−30)/(2∗(−3))=30/−6=−5-b/(2a)=-(-30)/(2*(-3))=30/-6=-5. That’s correct. Then substituting x=−5x=-5 into the equation: y=−3∗(−5)2−30∗(−5)−81y=-3*(-5)^{2}-30*(-5)-81. Compute each term:
First term: −3∗(25)=−75-3*(25)=-75
Second term: −30∗(−5)=+150-30*(-5)=+150
Third term: −81-81
Total: −75+150=75-75+150=75; 75−81=−675-81=-6. Correct.
Completing the square also confirmed the same. Calculus as well. So multiple methods confirm that n=−6n=-6.
Therefore, I’m confident that the answer is n=−6n=-6.

Next, we demonstrate the output of step extraction. As explained in [A.2](#A1.SS2 "A.2 Dataset Curation ‣ Appendix A Implementation Details ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models"), the output from step extraction contains line numbers corresponding to each plan and execution within a component. In the sample below, we replace line numbers with the corresponding block of text from the reasoning trajectory for ease of understanding. For the sake of brevity, we only show the full details for a few components.

Formatted output of Step Extraction

### Component 1
  
Description: Planning how to find the vertex of the parabola.
  
Plan: Okay, so I need to find the vertex … Then once we have the xx-coordinate, we can plug that back into the original equation to find the corresponding yy-coordinate, which would be nn in this case.
  
Prompt: Identify the values of aa, bb, and cc from the given quadratic equation.
  
Execution: So let’s identify aa, bb, and cc … it looks like a=−3a=-3, b=−30b=-30, and c=−81c=-81.
Comment: No lines found
  
### Component 2
  
Description: Verifying the identified values of aa, bb, and cc.
  
…
  
### Component 3
  
Description: Calculating the xx-coordinate of the vertex using the vertex formula.
  
…
  
### Component 4
  
Description: Calculating the yy-coordinate of the vertex by substituting the xx-coordinate.
…
  
### Component 5
  
Description: Verifying the calculation of the yy-coordinate.
…
  
### Component 6
  
Description: Using the method of completing the square to find the vertex.
  
Plan: Alternatively, maybe I can use another method to confirm. Sometimes, completing the square can be a good way to find the vertex. Let me try that.
  
Prompt: Use the method of completing the square on the given equation to find the vertex.
  
Execution: The given equation is y=−3​x2−30​x−81y=-3x^{2}-30x-81. To complete the square, first factor out the coefficient of x2x^{2} … So the equation becomes: y=−3​(x+5)2−6y=-3(x+5)^{2}-6 which is in vertex form: y=a​(x−h)2+ky=a(x-h)^{2}+k, where the vertex is (h,k)(h,k) … Therefore, the vertex is at (−5,−6)(-5,-6), so nn is −6-6.
  
Comment: That confirms the previous result.
…
  
### Component 7
  
Description: Using calculus to find the vertex by taking the derivative and setting it to zero.
…
  
### Component 8
  
Description: Comparing results from different methods.
…
  
### Component 9
  
Description: Final verification of the solution and confirming results.
…

In Figure [7](#A2.F7 "Figure 7 ‣ B.1 Demonstration of the Data Curation Pipeline ‣ Appendix B Sample Demonstrations ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models"), we demonstrate the dependencies that are inferred from running DAG creation over the steps (a.k.a components) extracted above. The model has identified that Components 2, 3, 6, and 7 can run in parallel. This is because once the values of aa, bb, and cc are identified in Component 1, the verification of that calculation (Component 2) and the computation of the xx-coordinate (Component 3) are mutually independent. Besides, alternative approaches such as completing the square (Component 6) and using calculus (Component 7) are not dependent on components other than Component 1. Component 4 depends on Component 3 as the computation of the yy-coordinate depends on the value of the xx-coordinate identified in Component 3. Comparing the results of the three approaches (Component 8) depends on the results from Components 4, 6, and 7 while the final verification (Component 9) depends on Component 8. Hence, the DAG effectively models the dependencies among the components and identifies parallelization opportunities.

![Refer to caption](2506.05745v2/figures/dag_99.png)

Figure 7: Dependencies inferred from running DAG creation over the steps extracted from the example reasoning trajectory in Appendix [B.1](#A2.SS1 "B.1 Demonstration of the Data Curation Pipeline ‣ Appendix B Sample Demonstrations ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models")

As explained in Appendix [A.2](#A1.SS2 "A.2 Dataset Curation ‣ Appendix A Implementation Details ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models"), for components with short executions, we merge the executions with their plans. Hence, for the above problem, the executions of Components 2, 3, and 8 are merged with their plans. The trajectory containing plans and executions generated for the above problem following this modification is given below. Note that the plans are ordered based on the dependencies modeled in the DAG.

The sequential token count for the original response from R1 is measured as the total number of tokens in the response which is 1645. The trajectory sample below has a smaller sequential token count of 1445 due to the parallelized executions.

Trajectory sample for fine-tuning

<Plan_1>
  

Okay, so I need to find the vertex … it looks like a=−3a=-3, b=−30b=-30, and c=−81c=-81.
…
Wait, is that right? Let me check again … The constant term is −81-81, so c=−81c=-81.
…
Now, using the formula and plugging in the values of aa and bb… Let’s compute that step by step.
…
<prompt_1.1> Calculate the x-coordinate of the vertex </prompt_1.1>
Alternatively, maybe I can use another method to confirm. Sometimes, completing the square can be a good way to find the vertex.
<prompt_1.2> Use the method of completing the square on the given equation to find the vertex. </prompt_1.2>
  
Alternatively, maybe I can use calculus, taking the derivative … let’s try it.
<prompt_1.3> Use calculus to find the xx-coordinate </prompt_1.3>
  
</Plan_1>
  
<Execution_1>
  

<execution_1.1>
  
The numerator is −(−30)-(-30)… So m=30/(−6)=−5m=30/(-6)=-5. Therefore, the xx-coordinate of the vertex is −5-5.
</execution_1.1>
  
<execution_1.2>
  
The given equation is y=−3​x2−30​x−81y=-3x^{2}-30x-81. To complete the square, first factor out the coefficient of x2x^{2} … So the equation becomes: y=−3​(x+5)2−6y=-3(x+5)^{2}-6 which is in vertex form: y=a​(x−h)2+ky=a(x-h)^{2}+k, where the vertex is (h,k)(h,k) … Therefore, the vertex is at (−5,−6)(-5,-6), so nn is −6-6.
</execution_1.2>
  
<execution_1.3>
  
The derivative of yy with respect to xx is d​y/d​x=2∗(−3)​x+(−30)=−6​x−30dy/dx=2*(-3)x+(-30)=-6x-30. Setting this equal to zero for critical points … as before, gives y=−6y=-6.
</execution_1.3>
  
</Execution_1>
  
<Plan_2>
  

Now, to find the y-coordinate nn … , I need to substitute x=−5x=-5…
<prompt_2.1> Substitute x = -5 to find the y-coordinate of the vertex. </prompt_2.1>
  
</Plan_2>
  
<Execution_2>
  
<execution_2.1>
  
Plugging in x = -5:
…
So n=−6n=-6.
</execution_2.1>
  
</Execution_2>
  
<Plan_3>
  
Based on execution_2.1:
Wait, let me double-check my calculations …
<prompt_3.1> Redo the substitution of x=−5x=-5 into the original equation to verify. </prompt_3.1>
  
Based on execution_2.1, execution_1.2, execution_1.3:
Therefore, all three methods (vertex formula, completing the square, calculus) lead to the same answer: n=−6n=-6.
Let me check again.
<prompt_3.2> Recheck the calculations and confirm the results </prompt_3.2>
  
</Plan_3>
  
<Execution_3>
  

<execution_3.1>
  
Calculating yy when x=−5x=-5: First term: −3∗(−5)2-3*(-5)^{2} … So adding them: n=−75+150=75;75−81=−6n=-75+150=75;75-81=-6.
</execution_3.1>
  
<execution_3.2>
  
The original equation is … So multiple methods confirm that n=−6n=-6.
</execution_3.2>
  
</Execution_3>
  
<Final_answer>
  
Therefore, the value of nn is \\backslashboxed{−6-6}.
</Final_answer>

### B.2 Demonstration of Sprint execution versus sequential reasoning from RFT

Given below is an example of how Sprint responds to a question from the MATH-500 benchmark at inference time. The executions presented side-by-side are carried out in parallel using the inference strategy shown in Figure [3](#S3.F3 "Figure 3 ‣ 3.2 Training Reasoning Models for Sprint Framework ‣ 3 Methodology ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models").
  
Question: The binary number 10101001110210101001110_{2} is equal to what number in base eight?

Planning and parallel execution trajectory generated by Sprint

<Plan_1>
  

Okay, so I need to convert the binary number 10101001110210101001110_{2} to base eight. So, the plan is probably to group the binary digits into sets of three starting from the right and then convert each group to an octal digit.
Wait, but first, let me confirm: the binary number given is 10101001110. Let me count the digits.
Let’s see: 1010100111010101001110. That’s 11 binary digits. Since 8 is 232^{3}, each octal digit is three bits, so 11 bits would need to be grouped into 4 octal digits (since 4*3=12, which is more than 11) but we need to add a leading zero to make it 12 bits? Wait, no, actually, when converting from binary to octal, you start from the right and split into groups of three.
Right, so even if the total number of bits isn’t a multiple of three, you can add leading zeros to make it a multiple of three. Let me check.
<prompt_1.1> Verify the method of converting binary to octal by considering the binary number 1010100111010101001110. </prompt_1.1>
  
But let me think again. Let me confirm with another approach.
Alternatively, I could convert the binary number to decimal first and then to octal. Maybe that’s a good way to cross-verify.
<prompt_1.2> Consider converting the binary number to decimal first and then to octal as an alternative method. </prompt_1.2>
  
</Plan_1>
  
<Execution_1>
  

<execution_1.1>
  
The original number is 10101001110. Let’s write them out: positions from right to left (since we start grouping from the right). Wait, actually, when grouping, we start from the right, so the leftmost digit might need to be padded with zeros to make the total number of digits a multiple of three.
So the binary number has 11 digits. 11 divided by 3 is 3 with a remainder of 2. So, we need to add one leading zero to make it 12 digits. Wait, 3*4=12, so yes, adding one zero on the left. So the original binary is 10101001110. Adding a leading zero gives 010101001110.
</execution_1.1>

<execution_1.2>
  
Let’s see. The binary number is 10101001110. Let me write down the positions from right to left, starting at 0. Wait, actually, in computers, the rightmost bit is the least significant bit, which is position 0. So let’s list the bits:
Position: 10 9 8 7 6 5 4 3 2 1 0
Bit: 1 0 1 0 1 0 0 1 1 1 0
…
So:
Bit 10: 1 (2102^{10})
Bit 9: 0 (292^{9})
Bit 8: 1 (282^{8})
…
So the binary number is:
210+28+…​212^{10}+2^{8}+...2^{1}
…
…
Adding them all up: 1024 + 256 = 1280; 1280 + 64 = 1344; 1344 + 8 = 1352; 1352 + 4 = 1356; 1356 + 2 = 1358.
So the decimal equivalent is 1358.
</execution_1.2>
  

</Execution_1>
  
<Plan_2>
  
   
Based on execution_1.1:
Now, splitting into groups of three starting from the right:
<prompt_2.1> Split the 12-digit binary number into groups of three starting from the right and convert each group to octal. </prompt_2.1>
  
Based on execution_1.2:
Now, converting 1358 to octal. Let’s divide by 8:
<prompt_2.2> Convert the decimal number 1358 to octal using division by 8. </prompt_2.2>
  
</Plan_2>
  
<Execution_2>
  

<execution_2.1>
  
0 1 0 1 0 0 0 1 1 1 0
Wait, no, wait. Wait, the binary number after adding a leading zero is 010101001110. Now, group into 4 sets of three:
Group 1 (leftmost): 010, Group 2: 101, Group 3: 001, Group 4: 110.
Then convert each of these to octal digits.
Wait, octal digits go from 0 to 7, so each group of three bits represents 0-7. Let me recall the binary to octal mapping:
000 = 0, 001 = 1, 010 = 2, … So:
Group 1: 010 →\rightarrow 2
Group 2: 101 →\rightarrow 5
Group 3: 001 →\rightarrow 1
Group 4: 110 →\rightarrow 6
So putting them together: 2 5 1 6 →\rightarrow 251682516_{8}.
</execution_2.1>

<execution_2.2>
  
1358 ÷ 8 = 169 with remainder 6 (since 169*8 = 1352, 1358 - 1352 = 6)
169 ÷ 8 = 21 with remainder 1 (21*8 = 168, 169 - 168 = 1)
21 ÷ 8 = 2 with remainder 5 (2*8 = 16, 21 - 16 = 5)
2 ÷ 8 = 0 with remainder 2
So the remainders, from last to first, are 2, 5, 1, 6. Therefore, 1358 in octal is 251682516_{8}.
</execution_2.2>

</Execution_2>
  
<Plan_3>
  

Based on execution_2.1:
Wait, but let me check again. Let’s verify the grouping.
<prompt_3.1> Verify the grouping of the binary digits and the conversion to octal. </prompt_3.1>
  
Based on execution_2.2:
Therefore, the binary number 10101001110210101001110_{2} is equal to 251682516_{8}.
So both methods give the same result, which is reassuring.
<prompt_3.2> Reflect on the solution and confirm its correctness by comparing both conversion methods. </prompt_3.2>
  
</Plan_3>
  
<Execution_3>
  

<execution_3.1>
  
Original binary with leading zero: 010 101 001 110.
Group 1: 010 → 2
Group 2: 101 → 5
Group 3: 001 → 1
Group 4: 110 → 6
So octal number is 2 5 1 6 → 2516.
</execution_3.1>

<execution_3.2>
  
I think this confirms that the answer is correct.
But let me just go through the steps once more to be thorough.
Original binary: 10101001110
Convert to groups of three starting from the right. Since it’s 11 digits, add a leading zero to make it 12 digits: 010101001110.
Group into four parts: 010 101 001 110. Convert each:
010 = 2, 101 = 5, 001 = 1, 110 = 6
Combine: 2516. Yep.
Alternatively, converting to decimal via binary to decimal conversion:
101010011102=1∗21​0+0∗29+1∗28+0∗27+…+0∗20=1024+256+64+8+4+2=135810101001110_{2}=1*2^{1}0+0*2^{9}+1*2^{8}+0*2^{7}+...+0*2^{0}=1024+256+64+8+4+2=1358. Then 1358 divided by 8 gives 169*8=1352, remainder 6; 169 divided by 8 is 21*8=168,
…
So 2 5 1 6. So 2516. All checks out.
Therefore, the final answer is 2516 in octal. I think that’s solid. No mistakes detected in the process.
</execution_3.2>

</Execution_3>
  
<Final_answer>
  
This step-by-step conversion shows that the binary number 10101001110210101001110_{2} is equal to \\backslashboxed{251682516_{8}} in base eight.
</Final_answer>

The sequential token count of the above response from Sprint is 1463. For the same question, we present the sequential trajectory generated by the RFT model below. The sequential token count of this response is 1989 since all tokens are generated sequentially. This highlights the benefit of parallelizing executions using Sprint.

Sequential reasoning trajectory generated by the RFT model

Okay, so I need to convert the binary number 10101001110210101001110_{2} to base eight. Hmm, I remember that converting between binary and octal is done by grouping the binary digits into sets of three, starting from the right. Each group of three bits corresponds to a single octal digit. Let me think through the steps carefully.
  
First, let me write down the binary number: 1 0 1 0 1 0 0 1 1 1 01\ 0\ 1\ 0\ 1\ 0\ 0\ 1\ 1\ 1\ 0. Wait, let me count the digits. The original number is 1010100111010101001110, which has 1111 digits. Since octal groups are in threes, I need to split this into groups of three. But 1111 isn’t divisible by three. So, I should add leading zeros to make the total number of digits a multiple of three. Right, so 1111 divided by 33 is 33 with a remainder of 22. That means I need to add one leading zero to make it 1212 digits. So the new number becomes 0101010011102010101001110_{2}.
  
Now, let me split this into groups of three starting from the right. Let me write it out:
  
Group 11: 010010, Group 22: 101101, Group 33: 001001, Group 44: 110110
  
Wait, no. Wait, the leading zeros are added at the beginning, so the original number was 1010100111010101001110. Adding a leading zero makes it 010101001110010101001110. Now, splitting into groups of three from the right:
  
Starting from the end, the last three digits are 110110, then moving left, the next three are 001001, then 101101, then 010010. So the groups are 010010, 101101, 001001, 110110. Now, each of these binary groups needs to be converted to their octal equivalents.
  
Let me convert each group:
  
0102010_{2} is 22 in octal because 0×4+1×2+0×1=20\times 4+1\times 2+0\times 1=2.
  
1012101_{2} is 55 in octal because 1×4+0×2+1×1=51\times 4+0\times 2+1\times 1=5.
  
…
  
So putting those together in order from left to right, the octal digits are 22, 55, 11, 66. Therefore, the octal number should be 251682516_{8}. Wait, but let me verify this again to make sure I didn’t make a mistake in grouping or conversion.
  
Wait, when grouping from the right, the first group (rightmost) is 110110, then moving left, the next is 001001, then 101101, then 010010. So the groups are 010010, 101101, 001001, 110110. Converting each to octal:
  
0102=2010_{2}=2, 1012=5101_{2}=5, 0012=1001_{2}=1, 1102=6110_{2}=6. So the octal number is 2 5 1 62\ 5\ 1\ 6, which is 251682516_{8}. Let me check if this is correct by converting the original binary number to decimal and then converting that decimal number to octal to see if it matches.
  
First, converting 10101001110210101001110_{2} to decimal. Let’s write out the binary number with each digit’s place value:
  
From right to left, the positions are 00 to 1010. The digits are:
  
Position 1010: 11, Position 99: 00, Position 88: 11, …, Position 00: 00
  
Calculating the decimal value:
  
1×(210)+0×(29)+1×(28)+0×(27)+1×(26)+0×(25)+0×(24)+1×(23)+1×(22)+1×(21)+0×(20)1\times(2^{10})+0\times(2^{9})+1\times(2^{8})+0\times(2^{7})+1\times(2^{6})+0\times(2^{5})+0\times(2^{4})+1\times(2^{3})+1\times(2^{2})+1\times(2^{1})+0\times(2^{0})
Calculating each term:
  
210=10242^{10}=1024, 28=2562^{8}=256, 26=642^{6}=64, 23=82^{3}=8, 22=42^{2}=4, 21=22^{1}=2
  
Adding them up: 1024+256=12801024+256=1280; 1280+64=13441280+64=1344; 1344+8=13521344+8=1352; 1352+4=13561352+4=1356; 1356+2=13581356+2=1358.
  
So the decimal value is 13581358. Now, converting 13581358 to octal. Let’s divide 13581358 by 88 repeatedly.
  
1358÷8=1691358\div 8=169 with a remainder of 66.
  
169÷8=21169\div 8=21 with a remainder of 11.
  
21÷8=221\div 8=2 with a remainder of 55.
  
2÷8=02\div 8=0 with a remainder of 22.
  
Writing the remainders from last to first: 2 5 1 62\ 5\ 1\ 6. So 251682516_{8}. Which matches the previous result. Therefore, the conversion is correct.
  
But wait, let me check the grouping again. The original binary number was 1010100111010101001110. When adding a leading zero, it becomes 010101001110010101001110. Splitting into groups of three from the right:
  
Starting from the right:
  
111111 001001 101101 010010. Wait, that’s different. Wait, perhaps I made a mistake in grouping.
  
Wait, the original binary number is 1010100111010101001110. Let me write it as 10 101 001 11010\ 101\ 001\ 110. Wait, that’s not correct. Wait, the original number is 1111 digits. So when adding a leading zero, it becomes 1212 digits: 0 1 0 1 0 1 0 0 1 1 1 00\ 1\ 0\ 1\ 0\ 1\ 0\ 0\ 1\ 1\ 1\ 0. Then grouping from the right:
  
Group11: 0 1 00\ 1\ 0 (positions 11,10,911,10,9), Group22: 1 0 11\ 0\ 1 (positions 8,7,68,7,6), Group33: 0 0 10\ 0\ 1 (positions 5,4,35,4,3), Group44: 1 1 01\ 1\ 0 (positions 2,1,02,1,0)
  
Wait, but when grouping from the right, the rightmost group is the last three digits. So the original number is 010101001110010101001110. The rightmost three digits are 110110, then moving left, next three are 001001, then 101101, then 010010. So the groups are 010010, 101101, 001001, 110110. Which is the same as before. So converting each gives 2,5,1,62,5,1,6. So 251682516_{8}. Which is correct. So the answer is 251682516_{8}.
  
But wait, when I grouped the original number as 1010100111010101001110, which is 1111 digits, adding a leading zero makes it 010101001110010101001110, which is 1212 digits. So grouping into three from the right: 010010, 101101, 001001, 110110. So that’s correct.
  
Alternatively, another way to check is by converting each group as I did before. So yes, the answer is 25162516 in octal.
  
But let me just confirm once again by converting 251682516_{8} back to binary to see if it’s 10101001110210101001110_{2}.
  
25162516 in octal:
  
Each digit corresponds to three binary digits:
  
2→0102\rightarrow 010
5→1015\rightarrow 101
1→0011\rightarrow 001
6→1106\rightarrow 110
So putting them together: 010 101 001 110→010101001110010\ 101\ 001\ 110\rightarrow 010101001110, which is the original number. So that’s correct.
  
Therefore, the final answer is \boxed{25162516} in base eight.

### B.3 Demonstration of Sprint parallelism within a single solution method

The sample in Section [B.2](#A2.SS2 "B.2 Demonstration of Sprint execution versus sequential reasoning from RFT ‣ Appendix B Sample Demonstrations ‣ Sprint: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models") shows Sprint parallelizing alternative solution methods in stages 1 and 2. In the below example, we show that Sprint can also split a single solution method into subtasks, execute them in parallel, and aggregate the results later. Here, the planner splits the problem into calculating the vertical asymptote and re-evaluating the horizontal asymptote, as prompts 1.1 and 1.2 in parallel.

Question: The graph of 2​xx2−5​x−14\frac{2x}{x^{2}-5x-14} has vertical asymptotes x=ax=a and x=bx=b, and horizontal asymptote y=cy=c. Find a+b+ca+b+c.

Trajectory sample for parallelism within a single solution method

<Plan_1>
  

Determine the vertical and horizontal asymptotes of f(x)=\frac{2x}{x^2-5x-14}, then compute a+b+c.
<prompt_1.1> Identify the vertical asymptotes by finding the roots of the denominator. </prompt_1.1>
<prompt_1.2> Re-evaluate the horizontal asymptote using the degrees of the numerator and denominator. </prompt_1.2>
</Plan_1>
  
<Execution_1>
  

<execution_1.1>
  
Vertical asymptotes occur where the denominator is zero (provided the numerator isn’t zero). Factoring x^2-5x-14 = (x-7)(x+2) gives roots at x=7 and x=-2. Thus, a=7 and b=-2.
</execution_1.1>
  
<execution_1.2>
  
Since the numerator’s degree (1) is less than the denominator’s (2), the horizontal asymptote is y=0. Hence, c=0.
</execution_1.2>
  
</Execution_1>
  
Rest of the solution continues…

### B.4 Demonstration of Sprint execution on a non-STEM task

We use the below example to demonstrate that Sprint generalizes well to non-STEM tasks like creative writing, despite being different from tasks in the MATH dataset used for fine-tuning. When tasked with generating a brief movie scene description, the planner successfully devises three independent subtasks, each executed concurrently by separate executors. After three planning and execution rounds, these independently developed results were integrated into a coherent and unified narrative.

Trajectory sample for creative writing task

<Plan_1>
  

The user wants a 250-word scene set shortly after the Battle of King’s Landing.
<prompt_1.1> Identify the key elements and emotions for each perspective: Bran Stark’s visions, the noble’s skepticism, and the urchin’s admiration. </prompt_1.1>
</Plan_1>
  
<Execution_1>
  

<execution_1.1>
  
- Bran: He’s the one who saw the vision of the White City…
- Noble from the Vale: He’s skeptical…
- Urchin: This adds an unexpected element…
</execution_1.1>
  
</Execution_1>
  
<Plan_2>
  

Based on Execution 1.1:
Bran: His lines should include visions…
<prompt_2.1> Develop Bran Stark’s lines to describe the vision of the White City and the Iron Throne. </prompt_2.1>
  
<prompt_2.2> Develop the noble’s lines to express skepticism about Bran’s leadership and his brother’s choice. </prompt_2.2>
  
<prompt_2.3> Develop the urchin’s lines to show admiration for Bran and the vision, and the impact on his journey. </prompt_2.3>
  
</Plan_2>
  
<Execution_2>
  

<execution_2.1>
  
The urchin’s lines should be simple but full of wonder…
</execution_2.1>
  
<execution_2.2>
  
The urchin in the Red Keep adds a layer of innocence, contrasting with…
</execution_2.2>
  
<execution_2.3>
  
The streets below are in ruins, but the urchin’s eyes…
</execution_2.3>
  
</Execution_2>
  
<Plan_3>
  

Based on Executions 2.1–2.3:
<prompt_3.1> Ensure each character’s perspective is distinct and contributes to the overall mood. The scene should capture the transition from battle chaos to the realm of possibility of a new order. </prompt_3.1>
  
</Plan_3>
  
<Execution_3>
  

<execution_3.1>
  
The urchin’s admiration is genuine…
</execution_3.1>
  
</Execution_3>
  
<Final_answer>
  

The air was thick with the scent of incense and the faint hum of machinery. The throne loomed before Bran…
The council chambers were quiet, save for the faint murmur of leather on wood…
The Red Keep was alive with the promise of change … The White City was his home, and the Iron Throne was his throne.
</Final_answer>
