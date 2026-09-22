---
title: "MiMo-VL Technical Report"
arxiv: 2506.03569
date: 2025-06-04
source: https://arxiv.org/abs/2506.03569
crawled: 2026-09-22
---

# MiMo-VL Technical Report

LLM-Core Xiaomi

###### Abstract

We open-source MiMo-VL-7B-SFT and MiMo-VL-7B-RL, two powerful vision-language models delivering state-of-the-art performance in both general visual understanding and multimodal reasoning.
MiMo-VL-7B-RL outperforms Qwen2.5-VL-7B on 35 out of 40 evaluated tasks, and scores 59.4 on OlympiadBench, surpassing models with up to 78B parameters.
For GUI grounding applications, it sets a new standard with 56.1 on OSWorld-G, even outperforming specialized models such as UI-TARS.
Our training combines four-stage pre-training (2.4 trillion tokens) with Mixed On-policy Reinforcement Learning (MORL) integrating diverse reward signals. We identify the importance of incorporating high-quality reasoning data with long Chain-of-Thought into pre-training stages, and the benefits of mixed RL despite challenges in simultaneous multi-domain optimization.
We also contribute a comprehensive evaluation suite covering 50+ tasks to promote reproducibility and advance the field.
The model checkpoints and full evaluation suite are available at <https://github.com/XiaomiMiMo/MiMo-VL>.

Figure 1: 
Benchmark performance of MiMo-VL-7B.

## 1 Introduction

Vision-language models (VLMs) have emerged as the foundational backbone for multimodal AI systems, enabling autonomous agents to perceive the visual world, reason over multimodal content ([Yue et al., 2024b](#bib.bib69)), and interact with both digital ([Xie et al., 2024](#bib.bib62); [OpenAI, 2025](#bib.bib40)) and physical environments ([Zitkovich et al., 2023](#bib.bib76); [Black et al., 2024](#bib.bib4)).
The significance of these capabilities has motivated extensive exploration across multiple dimensions, including novel architectural designs ([Alayrac et al., 2022](#bib.bib1); [Team, 2024](#bib.bib52); [Ye et al., 2025](#bib.bib66)) and innovative training methodologies with optimized data recipes ([Karamcheti et al., 2024](#bib.bib21); [Dai et al., 2024](#bib.bib10)), leading to rapid progress in the field ([Liu et al., 2023](#bib.bib28); [Tong et al., 2024](#bib.bib53); [Bai et al., 2025a](#bib.bib2)).

In this report, we share our efforts to build a compact yet powerful VLM, MiMo-VL-7B. MiMo-VL-7B comprises three components: (1) a native-resolution Vision Transformer (ViT) encoder that preserves fine-grained visual details, (2) a Multi-Layer Perceptron (MLP) projector for efficient cross-modal alignment, and (3) our MiMo-7B ([Xiaomi, 2025](#bib.bib61)) language model, specifically optimized for complex reasoning tasks.

The development of MiMo-VL-7B involves two sequential training processes:
(1) A *four-stage pre-training phase*, which includes projector warmup, vision-language alignment, general multimodal pre-training, and long-context Supervised Fine-Tuning (SFT).
Throughout these stages, we curate high-quality datasets by strategically combining open-source collections with synthetic data generation techniques, consuming 2.4 trillion tokens, adjusting the dataset distribution in different stages to facilitate training. This phase yields the MiMo-VL-7B-SFT model.
(2) A subsequent *post-training phase*, where we introduce Mixed On-policy Reinforcement Learning (MORL), a novel framework that seamlessly integrates diverse reward signals spanning perception accuracy, visual grounding precision, logical reasoning capabilities, and human preferences.
We adopt the idea of GRPO ([Shao et al., 2024](#bib.bib50)) and enhance training stability by exclusively performing on-policy gradient updates during this stage. This phase yields the MiMo-VL-7B-RL model.

During this journey, we find:

(1) Incorporating high-quality, broad-coverage reasoning data from the pre-training stage is crucial for enhancing model performance. 
In the current era of “thinking” models, vast quantities of multimodal pre-training data are undergoing a significant re-evaluation. Traditional question-answering (QA) data, with its direct, short answers, often restricts models to superficial pattern matching and leads to overfitting.
In contrast, synthesized reasoning data with long Chain-of-Thought (CoT) enables learning of complex logical relationships and generalizable reasoning patterns, providing richer supervision signals that markedly improve both performance and training efficiency.
To leverage this advantage, we curate high-quality reasoning data by identifying diverse queries, employing large reasoning models to regenerate responses with long CoT, and applying rejection sampling to ensure quality.
Furthermore, rather than treating this as supplementary fine-tuning data, we incorporate substantial volumes of this synthetic reasoning data directly into the later pre-training stages, where extended training yields continued performance improvements without saturation.

(2) Mixed On-policy Reinforcement Learning further enhances model performance, while achieving stable simultaneous improvements remains challenging.
We apply RL across diverse capabilities, including reasoning, perception, grounding, and human preference alignment, spanning modalities including text, images, and videos.
While this hybrid training approach further unlocks the model’s potential, interference across data domains remains challenging.
Disparities in the growth trends of response length and task difficulty levels hinder stable, simultaneous improvements across all capabilities.

MiMo-VL-7B-RL delivers exceptional results across the full spectrum of multimodal capabilities.
(1) On fundamental visual perception tasks, it achieves state-of-the-art performance among open-source VLMs of comparable scale, scoring 66.7 on MMMU ([Yue et al., 2024b](#bib.bib69)) and outperforming Qwen2.5-VL-7B ([Bai et al., 2025a](#bib.bib2)) on 35 out of 40 evaluated tasks.
(2) For complex multimodal reasoning, MiMo-VL-7B-RL exhibits outstanding performance, scoring 59.4 on OlympiadBench ([He et al., 2024](#bib.bib17)) and surpassing models up to 72B parameters.
(3) In GUI grounding for agentic applications, our model sets a new standard by achieving a score of 54.7 on OSWorld-G ([Xie et al., 2025](#bib.bib63)), even exceeding specialized models like UI-TARS ([Qin et al., 2025b](#bib.bib46)).
(4) In terms of user experience and preference, MiMo-VL-7B-RL achieves the highest Elo rating among all open-source VLMs on our in-house user preference evaluation, performing competitively with proprietary models such as Claude 3.7 Sonnet.

These results validate our approach: by combining strong perception, sophisticated reasoning, and precise grounding capabilities through our MORL framework, MiMo-VL-7B-SFT and MiMo-VL-7B-RL establish new standards for open-source vision-language models.
To promote transparency and reproducibility, we also contribute a comprehensive evaluation suite covering 50+ tasks with complete prompts and protocols, enabling the community to build upon our work.

## 2 Pre-Training

In this section, we introduce the architecture design of our MiMo-VL-7B, followed by the data curation process and training recipes of pre-training stages.

### 2.1 Architecture

MiMo-VL-7B consists of three components: (1) a Vision Transformer (ViT) for encoding visual inputs such as images and videos; (2) a projector that maps the visual encodings into a latent space aligned with the Large Language Model (LLM); and (3) the LLM itself, which performs textual understanding and reasoning.
To support native resolution inputs, we adopt Qwen2.5-ViT ([Bai et al., 2025a](#bib.bib2)) as our visual encoder.
We initialize the LLM backbone with MiMo-7B-Base ([Xiaomi, 2025](#bib.bib61)) to leverage its strong reasoning capability, and utilize a randomly initialized Multi-Layer Perceptron (MLP) as the projector.
The overall architecture is illustrated in Figure [2](#S2.F2 "Figure 2 ‣ 2.1 Architecture ‣ 2 Pre-Training ‣ MiMo-VL Technical Report"), and the model configuration can be found in Appendix [B](#A2 "Appendix B Model Configuration of MiMo-VL-7B ‣ MiMo-VL Technical Report").

![Refer to caption](2506.03569v1/mimo_vl_arch.png)

Figure 2: Model architecture of MiMo-VL-7B.

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| Stages | Stage 1 | Stage 2 | Stage 3 | Stage 4 |
| Purpose | Projector | Vision-Language | Multimodal | Long-context |
| Warmup | Alignment | Pre-training | SFT |
| Dataset |  |  | + | + |
|  |  | Pure Text, | Long Pure Text, |
|  | + | OCR, Grounding, | Long Documents, |
| Image-Caption Pairs | Interleaved Data | QA, Video, GUI, | High-resolution Images, |
|  |  | Instruction Data, | Extended Videos, |
|  |  | Reasoning Data | Long Reasoning Data |
| Learning Rate | 1e-3 | 1e-4, 1e-5 | 1e-5 | 2.5e-5 |
| Training Tokens | 300B | 167B | 1.4T | 550B |
| Sequence Length | 8K | 8K | 8K | 32K |
| Trainable Components | Projector | ViT, Projector | All | All |

Table 1: Overview of MiMo-VL-7B training stages.

### 2.2 Pre-training Data

The MiMo-VL-7B pre-training dataset comprises 2.4 trillion tokens of high-quality, diverse multimodal data spanning images, videos, and text. This comprehensive dataset includes general image captions, interleaved data, Optical Character Recognition (OCR) data, grounding data, video content, GUI interactions, reasoning examples, and text-only sequences.

To ensure the quality of each data modality, we implement dedicated data curation pipelines tailored to the characteristics of each data type. Throughout the training process, we systematically adjust the proportions of different data modalities across various training stages to optimize both training efficiency and model stability. Additionally, we employ phash-based image deduplication to eliminate potential overlaps between our training datasets and evaluation benchmarks, thereby minimizing data contamination.

We detail the specific processing procedures for each data type in the following sections.

#### 2.2.1 Image Caption Data

The construction of our image caption dataset involves a multi-stage process designed to ensure high quality and distributional balance. We begin by aggregating a substantial volume of publicly available caption data from web sources. This initial corpus then undergoes a rigorous deduplication phase, employing image perceptual hashing (phash) in conjunction with text filtering, to yield a refined set of unique raw captions.

Subsequently, leveraging both the images and their original textual descriptions as priors, we utilize a specialized captioning model to re-caption the entire raw caption dataset. Following re-captioning, we apply filtering mechanisms to the generated captions based on linguistic consistency and repetition patterns to ensure the quality of the re-captioned text. To address inherent data imbalances, we adopt the methodology of MetaCLIP ([Xu et al., 2023](#bib.bib64)), which involves constructing novel bilingual (Chinese and English) metadata. This critical step serves to refine the caption distribution, thereby mitigating the over-representation of high-frequency entries and reducing dataset noise.

The culmination of this meticulous process is a balanced, high-quality, and diverse caption dataset. Crucially, we observe that this rich dataset significantly enhances model generalization and qualitative performance, offering advantages not always fully reflected in evaluations on existing, specialized benchmarks.

#### 2.2.2 Interleaved Data

We compile an extensive corpus of interleaved image-text data from diverse sources, including webpages, books, and academic papers. For content originating from books and papers, we employ advanced PDF parsing toolkits for content extraction and cleansing. The filtering process prioritizes and retains data types rich in world knowledge, such as textbooks, encyclopedias, manuals, guides, patents, and biographies. Within this interleaved dataset, textual segments are evaluated based on metrics including knowledge density and readability. For the visual components, we implement filters to exclude images of diminutive size, anomalous aspect ratios, unsafe content, and those with minimal visual information (e.g., decorative chapter headings and illustrations). Finally, image-text pairs are scored on relevance, complementarity, and the balance of information density, ensuring the retention of high-quality data. This curated dataset significantly augments the model’s knowledge repository, thereby establishing a robust foundation for its subsequent reasoning capabilities.

#### 2.2.3 OCR and Grounding Data

To enhance the model’s capabilities in OCR and object grounding, we compile an extensive corpus of OCR and grounding data from open-source datasets for pre-training.

For the OCR data, the images encompass a diverse textual content from documents, tables, general scenes, product packaging, and mathematical formulas. To increase learning difficulty, in addition to standard printed text, we specifically incorporate images containing handwritten script, typographically deformed text, and blurry/occluded text, thereby improving the model’s recognition performance and robustness. For a portion of this data, textual regions are annotated with bounding boxes, enabling the model to simultaneously predict these locations.

For the grounding data, our images feature scenarios with both single and multiple objects. We further improve the model’s capacity to comprehend complex referential intentions by employing intricate object expressions within localization prompts. In all scenarios involving localization, we use absolute coordinates for representation.

#### 2.2.4 Video Data

Our video dataset primarily draws from publicly available online videos, spanning a wide array of domains, genres, and durations. Based on the videos, we design a video re-captioning pipeline that produces dense, fine-grained event-level descriptions. Each caption is temporally grounded with precise start and end timestamps, enabling the model to develop general video perception with time-awareness. From the caption dataset, we further collect a subset with a balanced distribution of event durations for temporal grounding pretraining. We also curate video analysis data that summarize the global semantics of videos, such as narrative structures, stylistic elements, and implicit intentions. These analytical paragraphs enable the model to grasp in-depth comprehension of videos and extended world knowledge. To enhance the model’s conversational coherence, we collect diverse and challenging questions about videos and synthesize corresponding responses. We also incorporate open-source video captioning and conversation datasets to further enrich our video pretraining data.

#### 2.2.5 Graphical User Interface Data

To enhance the model’s capabilities in navigating Graphical User Interfaces (GUIs), we collect open-source pre-training data covering all sorts of platforms such as mobile, web, and desktop. A synthetic data engine is also devised to compensate for the limitations of open-source data and to strengthen specific aspects of the model’s capabilities. For example, we have constructed a vast amount of Chinese GUI data to enable the model to better handle Chinese GUI scenarios.

For GUI Grounding, we gather data for both element grounding and instruction grounding. Element grounding trains the model to precisely locate interface elements based on textual descriptions, establishing a robust perception of static user interfaces. Instruction grounding requires the model to identify target objects on screenshots according to user instructions, enhancing comprehension of GUI interaction logic. For this part, we additionally introduce a pre-training task that involves predicting intermediate actions based on before-and-after screenshots. Empirical evidence demonstrates that this approach significantly improves the model’s dynamic perception of GUI interfaces.

For GUI Action, we collect a large scale of long GUI action trajectories. To ensure consistency across different platforms, we unified actions from mobile, web, and desktop environments into a standardized action space. A detailed specification of this action space is provided in Appendix [D](#A4 "Appendix D GUI Action Space ‣ MiMo-VL Technical Report"). This harmonization prevents action conflicts while maintaining platform-specific functionality.

#### 2.2.6 Synthetic Reasoning Data

Our approach to generating synthetic reasoning data begins with the comprehensive curation of open-source questions. This diverse collection spans perceptual question answering, document question answering, video question answering, and visual reasoning tasks, supplemented by question-answer pairs derived from web content and literary works.

Following initial filtering of these source questions, we leverage a large reasoning model to produce answers that integrate explicit reasoning. A cornerstone of our methodology is rigorous, multi-stage quality control. Beyond verifying the factual correctness of answers, we apply strict filtering criteria to the reasoning processes themselves, evaluating clarity of thought, eliminating redundancy, and ensuring consistent formatting.

The resulting high-fidelity dataset plays a critical role in empowering our model. It facilitates the effective inheritance of strong reasoning abilities inherent in MiMo-7B-Base ([Xiaomi, 2025](#bib.bib61)), enabling their seamless transfer and adaptation to multimodal contexts. Consequently, this allows our model to exhibit powerful and versatile multimodal reasoning capabilities across a broad array of domains.

### 2.3 Pre-training Stages

Our model undergoes a four pre-training stages as illustrated in Table [1](#S2.T1 "Table 1 ‣ 2.1 Architecture ‣ 2 Pre-Training ‣ MiMo-VL Technical Report"):

Stage 1: We freeze the ViT and LLM components, and warm up the randomly initialized projector using image-caption pairs.
This ensures the projector learns to map visual concepts to the language model’s representation space effectively, providing informative gradient signals for subsequent training stages rather than noisy updates from a poorly aligned projector.

Stage 2: The ViT is then unfrozen, and interleaved data is introduced to further strengthen vision-language alignment. The inclusion of complex and diverse images within the interleaved data enhances the ViT’s performance and robustness.

Stage 3: In this stage, all parameters are trainable. We introduce a more diverse array of data and tasks, including OCR, grounding, video, and GUI data—accumulating to 1.4 trillion tokens—to bolster the model’s general multimodal capabilities. To ensure stable mid-stage evaluation monitoring, small quantities of QA, instruction-following, and reasoning data are incorporated. Furthermore, a limited amount of text-only data is utilized to preserve MiMo-7B-Base’s textual capability.

Stage 4: This stage is dedicated to enhancing the model’s adaptability to long-context inputs.
The training sequence length is extended from 8K to 32K tokens.
We introduce additional data types such as long pure text, high-resolution images, long documents, extended videos, and long reasoning data to augment its long-context processing capabilities.
As long-context packing significantly increases the effective batch size, the learning rate is adjusted from 1e-5 to 2.5e-5.
Relative to Stage 3, this stage features a markedly increased proportion of reasoning data, alongside the introduction of long-form reasoning patterns.

These four stages create a powerful model, MiMo-VL-7B-SFT. With particular emphasis on Stage 4, the model’s reasoning capabilities are fully realized, enabling it to address highly intricate STEM problems. This advanced reasoning aptitude also generalizes effectively to common perception tasks. Consequently, our model demonstrates exceptionally high performance across various downstream benchmarks.

## 3 Post-Training

Building upon the visual perception capabilities and multimodal reasoning established during pre-training, we conduct post-training to further enhance MiMo-VL-7B.
Our approach employs a novel Mixed On-policy Reinforcement Learning (MORL) framework that seamlessly integrates Reinforcement Learning with Verifiable Rewards (RLVR) ([Shao et al., 2024](#bib.bib50); [Lambert et al., 2025](#bib.bib24)) with Reinforcement Learning from Human Feedback (RLHF) ([Ouyang et al., 2022](#bib.bib41)) to improve MiMo-VL-7B on challenging reasoning tasks and alignment with human preferences.

### 3.1 Reinforcement Learning with Verifiable Rewards

RLVR relies exclusively on rule-based reward functions, enabling continuous model self-improvement. In the post-training of MiMo-VL-7B, we design multiple verifiable reasoning and perception tasks where final solutions can be precisely validated using predefined rules.

##### Visual Reasoning

Visual reasoning capabilities are fundamental for multimodal models to understand and solve complex problems that require both visual perception and logical thinking. To facilitate this capability, we compile diverse verifiable STEM questions from open-source communities and proprietary K-12 collections.
An LLM is prompted to filter proof-based problems and rewrite multiple-choice questions with numerical or symbolic answers into free-answer formats, alleviating potential reward hacking.
We further refine question quality through comprehensive model-based difficulty assessment, excluding questions that either cannot be solved by advanced VLMs or are too easy, with a MiMo-VL-7B rollout pass rate exceeding 90%.
Additionally, we remove questions solvable even without image inputs. After data cleaning and category balancing, we curate a visual reasoning dataset of 80K problems. For evaluation, we use the rule-based Math-Verify library to determine response correctness.11
1
<https://github.com/huggingface/Math-Verify>

##### Text Reasoning

Since most visual reasoning data is limited to K-12 level questions, the reasoning performance of RL-trained models could be constrained.
In contrast, text-only reasoning datasets include more challenging queries requiring college or competition-level intelligence.
To unleash the full reasoning potential of our model, we incorporate mathematical reasoning data from [Xiaomi (2025)](#bib.bib61). Rewards are computed using the same rule-based Math-Verify library to ensure consistent evaluation across both visual and textual reasoning tasks.

##### Image Grounding

Accurate spatial localization is essential for models to understand object relationships and spatial reasoning in images. We include both general and GUI grounding tasks in our RLVR framework to enhance MiMo-VL-7B’s grounding capability. For bounding box predictions, rewards are calculated using the Generalized Intersection over Union (GIoU) ([Rezatofighi et al., 2019](#bib.bib49)) between predicted and ground-truth boxes. For point-style outputs, rewards are determined by whether the predicted point falls within the ground-truth bounding box.

##### Visual Counting

Precise counting abilities are essential for quantitative visual understanding and mathematical reasoning in visual contexts ([Chen et al., 2025a](#bib.bib5)).
We enhance visual counting capabilities through RL training, where rewards are defined by the accuracy of the model’s counting predictions compared to ground-truth counts.

##### Temporal Video Grounding

Beyond static image understanding and reasoning, we extend our RLVR framework to dynamic video content to capture temporal dependencies. We incorporate temporal video grounding tasks that require the model to localize video segments corresponding to natural language queries ([Wang et al., 2025](#bib.bib56)). The model outputs timestamps in [mm:ss,mm:ss] format to indicate the start and end times of the target video segments. Rewards are computed as the Intersection over Union (IoU) between predicted and ground-truth temporal segments.

### 3.2 Reinforcement Learning from Human Feedback

To align model outputs with human preferences and mitigate undesirable behaviors, we employ Reinforcement Learning from Human Feedback (RLHF) as a complementary approach to our verifiable reward framework.

##### Query Collection

Query diversity is paramount to the success of RLHF. Our methodology commences with gathering multimodal and text-only queries from open-source instruction tuning datasets and in-house human-written sources. All collected queries, both text and multimodal, then undergo a dedicated screening process. To further enhance diversity, we employ techniques such as clustering queries based on their embeddings and analyzing the resultant patterns. Crucially, we balance the proportions of Chinese and English queries, as well as those targeting helpfulness and harmlessness, before curating the final query set. For each selected query, MiMo-VL-7B and multiple other top-performing VLMs are prompted to generate responses. These responses are subsequently pairwise ranked by an advanced VLM to construct the definitive dataset for reward model training. Notably, to mitigate potential reward hacking, this same query set is utilized for both reward model training and the RLHF process.

##### Reward Model

We develop two specialized reward models tailored to different input modalities, training them using the Bradley-Terry reward modeling objective ([Ouyang et al., 2022](#bib.bib41)).
The text-only reward model is initialized from MiMo-7B ([Xiaomi, 2025](#bib.bib61)) to leverage its strong language understanding capabilities, while the multimodal reward model builds upon MiMo-VL-7B to effectively process queries containing visual inputs. This dual-model approach ensures optimal performance across both textual and multimodal evaluation scenarios.

### 3.3 Mixed On-Policy Reinforcement Learning

In the post-training phase of MiMo-VL-7B, we implement Mixed On-policy Reinforcement Learning (MORL) to simultaneously optimize RLVR and RLHF objectives.
As illustrated in Figure [3](#S3.F3 "Figure 3 ‣ 3.3 Mixed On-Policy Reinforcement Learning ‣ 3 Post-Training ‣ MiMo-VL Technical Report"), we integrate rule-based and model-based rewards as unified services within the verl framework ([Sheng et al., 2024](#bib.bib51)), enhanced by the Seamless Rollout Engine ([Xiaomi, 2025](#bib.bib61)).

![Refer to caption](2506.03569v1/morl_pipeline.png)

Figure 3: Mixed On-policy Reinforcement Learning in post-training phase.

##### On-Policy RL Recipe

We adopt a fully on-policy variant of GRPO ([Shao et al., 2024](#bib.bib50)) as the RL algorithm, which demonstrates robust training stability and effective exploration capabilities ([Chen et al., 2025b](#bib.bib7)).
For each problem qq, the algorithm samples a group of responses {o1,o2,…,oG}\left\{o_{1},o_{2},...,o_{G}\right\} from the policy πθ\pi_{\theta}, and updates the policy by maximizing the following objective:

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝒥GRPO(θ)=𝔼q∼D,{oi}i=1G∼πθ(⋅|q)[1∑i=1G|oi|∑i=1G∑j=1|oi|Ai,j],\mathcal{J}_{\mathrm{GRPO}}\left(\theta\right)=\mathbb{E}_{q\sim D,\{o_{i}\}_{i=1}^{G}\sim\pi_{\theta}(\cdot|q)}\left[\frac{1}{\sum_{i=1}^{G}\left|o_{i}\right|}\sum_{i=1}^{G}\sum_{j=1}^{\left|o_{i}\right|}A_{i,j}\right], |  | (1) |

where Ai,jA_{i,j} is the advantage, which is computed by the rewards {r1,r2,…,rG}\left\{r_{1},r_{2},...,r_{G}\right\} of responses in the same group:

|  |  |  |  |
| --- | --- | --- | --- |
|  | Ai,j=ri−mean⁡({ri}i=1G)std⁡({ri}i=1G).A_{i,j}=\frac{r_{i}-\mathrm{mean}(\{r_{i}\}_{i=1}^{G})}{\mathrm{std}(\{r_{i}\}_{i=1}^{G})}. |  | (2) |

Compared to vanilla GRPO, this on-policy variant performs single-step policy updates following response rollout, eliminating the need for a clipped surrogate training objective.
Following [Xiaomi (2025)](#bib.bib61), we integrate several advancements, including removal of the KL loss, dynamic sampling, easy data filter, and re-sampling strategies, into our RL training recipe.

##### Reward-as-a-Service

The MORL process integrates tasks across reasoning, perception, grounding, multimodal RLHF, and text-only RLHF, each requiring distinct reward functions or dedicated reward models.
To provide a unified interface and near-zero latency reward computation, we introduce Reward-as-a-Service (RaaS).
A reward router dynamically selects the appropriate reward function based on the query’s task type.
To minimize latency, reward models are deployed as standalone services, ensuring scalable reward computation accessible via HTTP.
All rewards are normalized to the range [0,1][0,1].
No additional reward, such as format rewards, is incorporated in our training process.

## 4 Evaluation

We evaluate MiMo-VL-7B across 50 tasks to comprehensively assess its capabilities. Appendix [C](#A3 "Appendix C Evaluation Benchmarks ‣ MiMo-VL Technical Report") lists all the benchmarks adopted in our evaluation.
We also assess model performance with an in-house evaluation set.

|  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Benchmark | Metrics | MiMo-VL | MiMo-VL | Qwen2.5-VL | InternVL3 | Gemma-3 | GPT-4o | Claude 3.7 |
| 7B-SFT | 7B-RL | 7B | 8B | 27B-IT | Sonnet |
| General | | | | | | | | |
| MMMU†val{}_{\mathrm{val}}^{{\dagger}} | Acc. | 64.664.6 | 66.7 | 58.658.6 | 62.762.7 | 64.964.9 | 70.770.7 | 69.869.8* |
| MMMU-Prostandard | Acc. | 45.245.2 | 46.2 | 34.734.7* | 45.645.6* | 37.837.8* | 42.542.5* | 56.556.5* |
| MMMU-Provision | Acc. | 39.439.4 | 40.3 | 29.429.4* | 37.837.8* | 24.924.9* | 36.136.1* | 45.845.8* |
| MMBench-entest | Acc. | 84.5 | 84.484.4 | 83.583.5 | 83.483.4 | 81.681.6* | 84.684.6* | 84.884.8* |
| MMBench-cntest | Acc. | 81.981.9 | 82.082.0 | 83.4 | 82.282.2 | 82.482.4* | 84.584.5* | 83.783.7* |
| Mantis | Acc. | 78.8 | 78.378.3 | 74.774.7* | 72.872.8* | 70.070.0* | 75.675.6* | 75.175.1* |
| MME-RealWorlden | Acc. | 57.457.4 | 59.1 | 57.457.4 | 56.156.1* | 51.951.9* | 57.557.5* | 50.850.8* |
| MME-RealWorldcn | Acc. | 55.055.0 | 55.555.5 | 51.251.2* | 58.5* | 47.947.9* | 58.558.5* | 40.640.6* |
| AI2D | Acc. | 83.283.2 | 83.583.5 | 83.983.9 | 85.2 | 84.584.5 | 82.682.6* | 81.481.4* |
| BLINKval | Acc. | 62.5 | 62.462.4 | 56.456.4 | 55.555.5 | 53.353.3* | 60.060.0 | 62.362.3* |
| CV-Bench | Acc. | 81.881.8 | 82.3 | 75.475.4* | 81.081.0* | 70.470.4* | 76.076.0* | 75.475.4* |
| VibeEval† | GPT-Score | 47.247.2 | 54.7 | 47.747.7* | 43.643.6* | 44.044.0* | 64.764.7 | 39.039.0* |
| VL-RewardBench† | Macro Acc. | 61.961.9 | 62.7 | 47.347.3* | 49.749.7* | 51.951.9* | 62.462.4 | 67.467.4* |
| V* | Acc. | 80.680.6 | 81.7 | 73.873.8* | 72.872.8* | 50.850.8* | 73.973.9 | - |
| VLMs are Blind | Acc. | 78.078.0 | 79.4 | 37.437.4* | 36.836.8* | 18.618.6* | 49.849.8* | 72.172.1* |
| PixmoCount | Acc. | 79.4 | 79.4 | 60.760.7* | 62.062.0 | 48.648.6* | 54.454.4* | 53.553.5* |
| CountBench | Acc. | 87.087.0 | 90.4 | 74.174.1* | 80.080.0* | 77.277.2* | 85.785.7* | 90.290.2* |
| RefCOCOavgval{}_{\mathrm{val}}^{\mathrm{avg}} | Acc.@0.5 | 85.785.7 | 89.689.6 | 87.187.1 | 90.1 | - | - | - |
| Doc & OCR | | | | | | | | |
| ChartQA† | Acc. | 92.9 | 91.791.7 | 90.290.2* | 89.689.6* | 78.078.0 | 86.786.7 | 92.292.2* |
| CharXiv†RQ{}_{\mathrm{RQ}}^{{\dagger}} | Acc. | 54.454.4 | 56.5 | 42.542.5 | 37.637.6 | 29.229.2* | 52.052.0 | 63.063.0* |
| CharXiv†DQ{}_{\mathrm{DQ}}^{{\dagger}} | Acc. | 87.0 | 86.886.8 | 73.973.9 | 73.673.6 | 63.863.8* | 86.586.5 | 89.589.5* |
| DocVQA†val{}_{\mathrm{val}}^{{\dagger}} | Acc. | 95.295.2 | 95.7 | 95.595.5* | 89.489.4* | 86.686.6 | 93.093.0* | 94.194.1* |
| InfoVQA†val{}_{\mathrm{val}}^{{\dagger}} | Acc. | 87.287.2 | 88.0 | 81.481.4* | 70.770.7* | 70.670.6 | 82.182.1* | 65.565.5* |
| SEED-Bench-2-Plus | Acc. | 71.971.9 | 72.4 | 70.770.7 | 69.769.7 | 66.366.3* | 71.171.1* | 72.972.9* |
| OCRBench† | Acc. | 87.687.6 | 86.686.6 | 89.7* | 88.088.0 | 77.677.6* | 84.384.3* | 80.680.6* |
| GUI | | | | | | | | |
| VisualWebBenchavg | Acc. | 80.2 | 80.2 | 72.972.9* | 62.762.7 | 49.749.7* | 80.280.2 | 79.379.3* |
| WebSrcval | SQuAD F1 | 96.5 | 95.395.3 | 94.694.6* | 91.191.1 | 89.089.0* | 89.189.1* | 91.191.1* |
| ScreenSpot | Center Acc. | 87.3 | 87.287.2 | 84.784.7 | 79.579.5 | - | 18.318.3 | - |
| ScreenSpot-v2 | Center Acc. | 89.589.5 | 90.5 | 88.088.0 | 81.481.4 | - | 18.518.5 | - |
| ScreenSpot-Proavg | Center Acc. | 39.939.9 | 41.9 | 29.029.0 | - | - | - | - |
| OSWorld-Gno_refusal | Center Acc. | 54.754.7 | 56.1 | 37.537.5* | - | - | - | - |
| Video | | | | | | | | |
| Video-MMEw/o​sub.{}_{\mathrm{w/o\penalty\ sub.}} | Acc. | 66.966.9 | 67.4 | 65.165.1 | 66.366.3 | - | - | - |
| Video-MMMU | Acc. | 53.1 | 43.343.3 | 47.447.4 | 48.948.9* | - | - | - |
| EgoSchemaval | Acc. | 60.460.4 | 59.659.6 | 62.462.4* | 68.2* | - | - | - |
| Charades-STA | mIoU | 38.538.5 | 50.0 | 43.643.6 | 25.425.4 | - | - | - |
| Text | | | | | | | | |
| GPQA Diamond | Pass@1 | 56.356.3 | 58.3 | 30.330.3* | 33.533.5* | 40.940.9 | 50.650.6* | 66.066.0* |
| SuperGPQA | Pass@1 | 42.642.6 | 44.3 | 25.425.4* | 29.429.4* | 29.329.3* | 31.631.6* | 54.454.4* |
| DROP | 3-shot F1 | 82.782.7 | 85.1 | 67.667.6* | 77.577.5* | 72.272.2 | 81.581.5 | 87.287.2* |
| MMLU-Pro | EM | 59.859.8 | 64.8 | 48.748.7* | 58.358.3* | 45.345.3 | 69.169.1 | 81.081.0 |
| IF-Eval | Prompt Strict | 75.375.3 | 75.975.9 | 75.175.1* | 87.287.2* | 88.9 | 82.582.5 | 88.788.7* |

Table 2: 
Comparison of MiMo-VL-7B models with other models on diverse visual-language and text benchmarks.
Results marked with * are obtained using our evaluation framework. † indicates that evaluation is performed using GPT-4o. The best results among open-source models are bolded.

### 4.1 Evaluation Setting

For image understanding benchmarks, we set the max pixels for the input image to 4096 × 28 × 28 and the maximum generation tokens to 32,768, employing greedy search for decoding.
For video benchmarks, videos are sampled at 2 FPS, with a maximum of 256 frames and a total token limit of 16,384.
For text evaluation benchmarks, we set the max new tokens for generation as 32,768, temperature as 0.6 and top-p as 0.95.
We adapt the existing framework based on LMMs-Eval ([Zhang et al., 2024a](#bib.bib71)) to better accommodate long-CoT reasoning models.
We further optimize the evaluation logic for specific tasks to ensure better evaluation consistency.
To facilitate open research, we open-source our evaluation framework with all prompts used.22
2
<https://github.com/XiaomiMiMo/lmms-eval>

### 4.2 General Capabilities

Table [2](#S4.T2 "Table 2 ‣ 4 Evaluation ‣ MiMo-VL Technical Report") presents benchmark results assessing the general capabilities of VLMs. Our MiMo-VL-7B models demonstrate consistently leading performance across a diverse range of vision-language and text benchmarks, establishing new state-of-the-art results among open-source models and even surpassing proprietary counterparts.

Specifically, our MiMo-VL-7B models achieve state-of-the-art results among open-source models. MiMo-VL-7B-SFT and
(i) On general vision-language tasks, our models achieve exceptional performance that leads the open-source field. MiMo-VL-7B-SFT and MiMo-VL-7B-RL obtain 64.6% and 66.7% on MMMUval respectively, outperforming much larger models such as Gemma 3 27B. For document and chart understanding, MiMo-VL-7B-RL excels with a top open-source score of 56.5% on CharXivRQ, significantly exceeding Qwen2.5-VL (42.5%) by 14.0 points and InternVL3 (37.6%) by 18.9 points.
(ii) Our models demonstrate superior video understanding capabilities while maintaining strong textual performance.
MiMo-VL-SFT achieves a leading 53.1% on Video-MMMU, and MiMo-VL-RL obtains an impressive 50.0% mIoU on Charades-STA. (iii) Compared with MiMo-7B, our models maintain decent performance on text-only benchmarks.
(iv) Remarkably, our MoRL yields comprehensive improvements, with the most impressive gains observed on challenging benchmarks such as VibeEval and CountBench.

|  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Reasoning | Metrics | MiMo-VL | MiMo-VL | QVQ-72B | Qwen2.5-VL | Intern-VL3 | Qwen2.5 | GPT-4o | Gemini-2.5 |
| Benchmark | 7B-SFT | 7B-RL | Preview | 72B | 78B | 72B | Pro |
| Multi-modal | | | | | | | | | |
| OlympiadBench | Acc. | 59.4 | 59.4 | 20.420.4 | 37.237.2* | 12.312.3 | - | 25.925.9 | 69.869.8 |
| MathVision | Acc. | 57.957.9 | 60.4 | 35.935.9 | 38.138.1 | 43.243.2 | - | 31.231.2 | 69.169.1 |
| MathVerse†vision​_​only{}_{\mathrm{vision\_only}}^{{\dagger}} | Acc. | 67.167.1 | 71.5 | 45.145.1* | 57.657.6 | 51.051.0 | - | 49.949.9 | 76.776.7 |
| DynaMath | Worst-case Acc. | 46.9 | 45.945.9 | 30.730.7 | 38.138.1* | 35.135.1 | - | 48.548.5 | 56.356.3 |
| WeMath | Strict Score | 65.165.1 | 66.3 | 37.737.7* | 50.650.6* | 46.146.1 | - | 50.650.6 | 78.078.0 |
| LogicVista | Acc. | 61.261.2 | 61.4 | 53.853.8* | 57.157.1* | 55.955.9 | - | 64.464.4 | 73.873.8 |
| MathVista†mini{}_{\mathrm{mini}}^{{\dagger}} | Acc. | 81.8 | 81.581.5 | 71.471.4 | 74.874.8 | 72.272.2 | - | 63.863.8 | 80.980.9 |
| Text | | | | | | | | | |
| MATH500 | Pass@1 | 95.095.0 | 95.4 | 83.883.8* | 83.083.0 | 68.868.8* | 82.882.8* | 78.278.2* | 95.295.2 |
| AIME24 | Pass@1 | 66.466.4 | 67.5 | 25.225.2* | 16.716.7* | 12.212.2* | 19.419.4* | 10.910.9* | 92.092.0 |
| AIME25 | Pass@1 | 50.950.9 | 52.5 | 18.118.1* | 10.810.8* | 11.711.7* | 13.313.3* | 8.78.7* | 86.786.7 |

Table 3: 
Comparison of MiMo-VL-7B with other models on reasoning benchmarks.
Results marked with * are obtained using our evaluation framework. † indicates that evaluation is performed using GPT-4o. The best results among open-source models are bolded.

### 4.3 Reasoning Tasks

Table [3](#S4.T3 "Table 3 ‣ 4.2 General Capabilities ‣ 4 Evaluation ‣ MiMo-VL Technical Report") presents evaluation results for multimodal and text reasoning benchmarks.
In multimodal reasoning, both the SFT and RL models significantly outperform all compared open-source baselines across these benchmarks.
Notably, MiMo-VL-7B-SFT surpasses much larger models, including Qwen2.5-VL-72B and QVQ-72B-Preview.
The RL model further improves performance on most reasoning benchmarks.
For example, MiMo-VL-7B-RL boosts accuracy on MathVision from 57.9% to 60.4%.
MiMo-VL-7B models also exhibit impressive reasoning capabilities on pure text benchmarks, even outperforming Qwen2.5-72B.
These results demonstrate that our multimodal pre-training and post-training recipes effectively endow the model with exceptional visual capabilities and strong text intelligence.

### 4.4 GUI Tasks

Figure 4: GUI understanding and grounding results. MiMo-VL-7B-RL achieves comparable results with GUI specialized models.

In addition, we demonstrate that MiMo-VL-7B models possess exceptional GUI understanding and grounding capabilities.
In Table [2](#S4.T2 "Table 2 ‣ 4 Evaluation ‣ MiMo-VL Technical Report"), MiMo-VL-7B-RL outperforms all other general VLMs compared. In Figure [4](#S4.F4 "Figure 4 ‣ 4.4 GUI Tasks ‣ 4 Evaluation ‣ MiMo-VL Technical Report"), we further compare MiMo-VL-7B-RL with GUI-specialized models (UI-TARS-1.0 ([Qin et al., 2025a](#bib.bib45)), Aguvis ([Xu et al., 2024](#bib.bib65)), OS-Atlas ([Wu et al., 2024](#bib.bib59))) of similar size on GUI Understanding (WebSrc, VisualWebBench) and Grounding (Screenspot, Screenspot-v2, Screenspot-Pro, OSWorld-G) benchmarks. As a general-purpose VLM, MiMo-VL achieves comparable or even superior performance to GUI-specialized models, particularly on the more challenging Screenspot-Pro and OSWorld-G benchmarks.

Figure 5: Elo ratings comparison across VLMs. MiMo-VL-7B-RL achieves the highest rating among open-source models, approaching the performance of proprietary alternatives such as Claude 3.7 Sonnet.

Figure 6: MiMo-VL-7B-SFT training curves in Stage 4.

Figure 7: On-policy RL and vanilla GRPO shows contrasting scaling behavior: on-policy RL performance continuously improves with more data, while vanilla GRPO reaches a plateau around 20,000 samples.

### 4.5 Elo Rating

Inspired by ChatbotArena ([Zheng et al., 2023](#bib.bib74)), we construct a balanced bilingual (Chinese and English) in-house evaluation dataset comprising real user prompts. This approach assesses user preference beyond traditional benchmark scores, providing insights into practical model performance in real-world scenarios.

Following the methodology of ([Chou et al., 2024](#bib.bib9)), we conduct pairwise comparisons between MiMo-VL-7B and competing models, including leading proprietary models and open-source VLMs ranging from 7B to 72B parameters. We compute Elo ratings based on GPT-4o judgments with style-controlled evaluation protocols.
Our evaluation covers a diverse range of visual-linguistic tasks, including multimodal reasoning, image understanding, and GUI interaction scenarios, therefore serving as a good proxy of user preference.

As illustrated in Figure [5](#S4.F5 "Figure 5 ‣ 4.4 GUI Tasks ‣ 4 Evaluation ‣ MiMo-VL Technical Report"), MiMo-VL-7B-RL achieves the highest Elo rating among all evaluated open-source VLMs, ranking first across models spanning from 7B to 72B parameters. This demonstrates superior user experience across the evaluation set, with our model’s performance closely approaching that of proprietary models such as Claude 3.7 Sonnet.
Moreover, MORL brings a boost of 22+ points for the MiMo-VL-7B-SFT.
These results highlight the competitive capability of our models and validate the effectiveness of our training methodology.

## 5 Discussion

### 5.1 Boosting Reasoning Capability in Pre-training

Figure [6](#S4.F6 "Figure 6 ‣ 4.4 GUI Tasks ‣ 4 Evaluation ‣ MiMo-VL Technical Report") shows the performance of MiMo-VL-7B-SFT during Stage 4, its final pre-training phase. In this stage, substantial volumes of synthetic long-form reasoning data are incorporated, and model performance increases sharply, e.g., +9 on MMMU, +14 on OSWorld-G, and +16 on OlympiadBench. Notably, model performance continuously improves without saturation.
These improvements are attributed to an increased depth in the model’s reasoning. For instance, on MMMU, the model’s average number of response tokens grows from 680 to 2.5K per question after Stage 4, indicating a more detailed and profound level of reasoning when tackling problems.

### 5.2 On-Policy RL v.s. Vanilla GRPO

We explore the benefits of on-policy RL v.s. vanilla GRPO with text-only reasoning tasks.
As illustrated in Figure [7](#S4.F7 "Figure 7 ‣ 4.4 GUI Tasks ‣ 4 Evaluation ‣ MiMo-VL Technical Report"), the on-policy algorithm demonstrates a consistent positive correlation between training data volume and performance score. Its learning curve shows no signs of saturation within the observed training window, suggesting potential for further enhancement with additional computational resources and data.
Conversely, the vanilla GRPO algorithm initially exhibits higher sample efficiency, achieving robust performance early in training. This advantage, however, is transient. The algorithm’s performance generally saturates around 20,000 training samples, beyond which further training yields negligible improvements.

|  |
| --- |
| Refer to caption |
| Instruction: Convert it to a table. |
| MiMo-VL-7B-RL: |
| Refer to caption |
| Refer to caption |
| Instruction: Answer the question in image. |
| MiMo-VL-7B-RL: <think>...</think> To solve for the tension in the wire, we use the equilibrium of torques about the hinge point PP. For a beam in equilibrium, the sum of clockwise torques equals the sum of counterclockwise torques. Step 1: Identify Forces and Torques - Beam’s weight (425​N425\,\text{N}): Acts downward at the beam’s midpoint (since it is uniform). The beam’s length is 8.4​m8.4\,\text{m}, so the midpoint is 8.42=4.2​m\frac{8.4}{2}=4.2\,\text{m} from PP. - Block’s weight (720​N720\,\text{N}): Acts downward at 8.4​m8.4\,\text{m} from PP. - Tension in the wire (TT): Acts at 3.4​m3.4\,\text{m} from PP at an angle of 23∘23^{\circ} above the horizontal. Only the vertical component of tension (Tsin23∘T\sin 23^{\circ}) contributes to torque (the horizontal component acts along the beam, so its torque about PP is zero). Step 2: Calculate Torques Torque is defined as force×perpendicular distance from pivot\text{force}\times\text{perpendicular distance from pivot}. - Clockwise torques (from the beam and block weights): - Beam’s weight: 425​N×4.2​m=1785​N·m425\,\text{N}\times 4.2\,\text{m}=1785\,\text{N·m} - Block’s weight: 720​N×8.4​m=6048​N·m720\,\text{N}\times 8.4\,\text{m}=6048\,\text{N·m} - Total clockwise torque: 1785+6048=7833​N·m1785+6048=7833\,\text{N·m} - Counterclockwise torque (from tension’s vertical component): - Tension’s vertical component: Tsin23∘T\sin 23^{\circ} - Perpendicular distance from PP to the wire: 3.4​m3.4\,\text{m} - Torque from tension: Tsin23∘×3.4mT\sin 23^{\circ}\times 3.4\,\text{m} Step 3: Solve for Tension In equilibrium, clockwise torque = counterclockwise torque: Tsin23∘×3.4=7833T\sin 23^{\circ}\times 3.4=7833 Solve for TT: T=78333.4×sin⁡23∘T=\frac{7833}{3.4\times\sin 23^{\circ}} Using sin⁡23∘≈0.3907\sin 23^{\circ}\approx 0.3907: T=78333.4×0.3907≈78331.328≈5900​NT=\frac{7833}{3.4\times 0.3907}\approx\frac{7833}{1.328}\approx 5900\,\text{N} Final Answer The tension in the wire is approximately 𝟓𝟗𝟎𝟎​N\boldsymbol{5900\,\text{N}}. |

  

Figure 8: Examples of MiMo-VL-7B solving complicated problems.

### 5.3 Interference Between RL Tasks

While MORL training enhances performance on nearly all evaluated tasks, achieving stable and simultaneous improvements across diverse task domains remains a significant challenge.
During training, we observe that reasoning tasks exhibit disparities with visual perception and grounding tasks, such as visual grounding and counting, making it difficult to match the performance of standalone RL on individual tasks.

The potential cause lies in the opposing growth trends of response length: reasoning tasks encourage longer CoT during the RL process, whereas grounding and counting tasks lead to shrinking ones.
Disparities in task difficulty and the risk of reward hacking may also contribute to this interference.
We are actively investigating the underlying causes of this phenomenon and seeking solutions to achieve consistent and persistent growth across all tasks.

## 6 Case Study

![Refer to caption](2506.03569v1/gui_case.png)

Figure 9: A case demonstrating the agentic capabilities of our model. MiMo-VL-7B successfully navigates a website to add the Xiaomi SU7 to the wishlist, customizing both paint and interior options. All screenshots are of size 1886*1544 (width*height).

We present qualitative results in Figure [8](#S5.F8 "Figure 8 ‣ 5.2 On-Policy RL v.s. Vanilla GRPO ‣ 5 Discussion ‣ MiMo-VL Technical Report") and Appendix [E](#A5 "Appendix E More Qualitative Examples ‣ MiMo-VL Technical Report").
As depicted in the top example in Figure [8](#S5.F8 "Figure 8 ‣ 5.2 On-Policy RL v.s. Vanilla GRPO ‣ 5 Discussion ‣ MiMo-VL Technical Report"), our model showcases strong plot understanding capabilities, successfully converting an intricate plot into a well-structured markdown table.
Additionally, we highlight the models’ superior reasoning capabilities in STEM tasks.
In the examples shown in Figure [10](#A5.F10 "Figure 10 ‣ Appendix E More Qualitative Examples ‣ MiMo-VL Technical Report") and Figure [13](#A5.F13 "Figure 13 ‣ Appendix E More Qualitative Examples ‣ MiMo-VL Technical Report"), the model effectively addresses multiple STEM questions within a single response.
Furthermore, our model exhibits strong agentic capabilities.
As illustrated in Figure [9](#S6.F9 "Figure 9 ‣ 6 Case Study ‣ MiMo-VL Technical Report"), MiMo-VL-7B successfully navigates a website to add the Xiaomi SU7 to the wishlist, with customized paint and interior options.

## 7 Conclusions

In this report, we present our efforts in building MiMo-VL-7B models.
Leveraging curated high-quality pre-training datasets and our MORL framework, MiMo-VL-7B-SFT and MiMo-VL-7B-RL demonstrate state-of-the-art performance across evaluated benchmarks.
We share key observations from our development process: the consistent performance gains from incorporating reasoning data in later pre-training stages, the advantages of on-policy RL over vanilla GRPO, and the challenges of task interference when applying MORL across diverse capabilities.
Alongside the released model checkpoints, we open-source our comprehensive evaluation suite to promote transparency and reproducibility in multimodal research.
We hope our work advances the development of capable open-source vision-language models and provides valuable insights for the community.

## References

- Alayrac et al. (2022)

  J. Alayrac, J. Donahue, P. Luc, A. Miech, I. Barr, Y. Hasson, K. Lenc, A. Mensch, K. Millican, M. Reynolds, R. Ring, E. Rutherford, S. Cabi, T. Han, Z. Gong, S. Samangooei, M. Monteiro, J. L. Menick, S. Borgeaud, A. Brock, A. Nematzadeh, S. Sharifzadeh, M. Binkowski, R. Barreira, O. Vinyals, A. Zisserman, and K. Simonyan.
  Flamingo: a visual language model for few-shot learning.
  In *NeurIPS*, 2022.
- Bai et al. (2025a)

  S. Bai, K. Chen, X. Liu, J. Wang, W. Ge, S. Song, K. Dang, P. Wang, S. Wang, J. Tang, H. Zhong, Y. Zhu, M. Yang, Z. Li, J. Wan, P. Wang, W. Ding, Z. Fu, Y. Xu, J. Ye, X. Zhang, T. Xie, Z. Cheng, H. Zhang, Z. Yang, H. Xu, and J. Lin.
  Qwen2.5-vl technical report.
  *arXiv preprint arXiv:2502.13923*, 2025a.
- Bai et al. (2025b)

  S. Bai, K. Chen, X. Liu, J. Wang, W. Ge, S. Song, K. Dang, P. Wang, S. Wang, J. Tang, et al.
  Qwen2. 5-vl technical report.
  *arXiv preprint arXiv:2502.13923*, 2025b.
- Black et al. (2024)

  K. Black, N. Brown, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, L. Groom, K. Hausman, B. Ichter, S. Jakubczak, T. Jones, L. Ke, S. Levine, A. Li-Bell, M. Mothukuri, S. Nair, K. Pertsch, L. X. Shi, J. Tanner, Q. Vuong, A. Walling, H. Wang, and U. Zhilinsky.
  π\pi0: A vision-language-action flow model for general robot control.
  *ArXiv*, abs/2410.24164, 2024.
  URL <https://api.semanticscholar.org/CorpusID:273811174>.
- Chen et al. (2025a)

  L. Chen, L. Li, H. Zhao, Y. Song, and Vinci.
  R1-v: Reinforcing super generalization ability in vision-language models with less than $3.
  <https://github.com/Deep-Agent/R1-V>, 2025a.
  Accessed: 2025-02-02.
- Chen et al. (2021)

  X. Chen, Z. Zhao, L. Chen, D. Zhang, J. Ji, A. Luo, Y. Xiong, and K. Yu.
  Websrc: a dataset for web-based structural reading comprehension.
  *arXiv preprint arXiv:2101.09465*, 2021.
- Chen et al. (2025b)

  Y. Chen, Z. Yang, Z. Liu, C. Lee, P. Xu, M. Shoeybi, B. Catanzaro, and W. Ping.
  Acereason-nemotron: Advancing math and code reasoning through reinforcement learning.
  *arXiv preprint arXiv:2505.16400*, 2025b.
- Cheng et al. (2024)

  K. Cheng, Q. Sun, Y. Chu, F. Xu, Y. Li, J. Zhang, and Z. Wu.
  Seeclick: Harnessing gui grounding for advanced visual gui agents.
  *arXiv preprint arXiv:2401.10935*, 2024.
- Chou et al. (2024)

  C. Chou, L. Dunlap, K. Mashita, K. Mandal, T. Darrell, I. Stoica, J. Gonzalez, and W.-L. Chiang.
  Visionarena: 230k real world user-vlm conversations with preference labels.
  *ArXiv*, abs/2412.08687, 2024.
  URL <https://api.semanticscholar.org/CorpusID:274655992>.
- Dai et al. (2024)

  W. Dai, N. Lee, B. Wang, Z. Yang, Z. Liu, J. Barker, T. Rintamaki, M. Shoeybi, B. Catanzaro, and W. Ping.
  Nvlm: Open frontier-class multimodal llms.
  *arXiv preprint*, 2024.
- Deitke et al. (2024)

  M. Deitke, C. Clark, S. Lee, R. Tripathi, Y. Yang, J. S. Park, M. Salehi, N. Muennighoff, K. Lo, L. Soldaini, et al.
  Molmo and pixmo: Open weights and open data for state-of-the-art multimodal models.
  *ArXiv preprint*, abs/2409.17146, 2024.
- Du et al. (2025)

  X. Du, Y. Yao, K. Ma, B. Wang, T. Zheng, K. Zhu, M. Liu, Y. Liang, X. Jin, Z. Wei, et al.
  Supergpqa: Scaling llm evaluation across 285 graduate disciplines.
  *ArXiv preprint*, abs/2502.14739, 2025.
  URL <https://arxiv.org/abs/2502.14739>.
- Dua et al. (2019)

  D. Dua, Y. Wang, P. Dasigi, G. Stanovsky, S. Singh, and M. Gardner.
  DROP: A reading comprehension benchmark requiring discrete reasoning over paragraphs.
  In J. Burstein, C. Doran, and T. Solorio, editors, *Proceedings of the 2019 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long and Short Papers)*, pages 2368–2378, Minneapolis, Minnesota, 2019. Association for Computational Linguistics.
  [10.18653/v1/N19-1246](https://doi.org/10.18653/v1/N19-1246).
  URL <https://aclanthology.org/N19-1246>.
- Fu et al. (2024a)

  C. Fu, Y. Dai, Y. Luo, L. Li, S. Ren, R. Zhang, Z. Wang, C. Zhou, Y. Shen, M. Zhang, et al.
  Video-mme: The first-ever comprehensive evaluation benchmark of multi-modal llms in video analysis.
  *arXiv preprint arXiv:2405.21075*, 2024a.
- Fu et al. (2024b)

  X. Fu, Y. Hu, B. Li, Y. Feng, H. Wang, X. Lin, D. Roth, N. A. Smith, W.-C. Ma, and R. Krishna.
  Blink: Multimodal large language models can see but not perceive.
  In *European Conference on Computer Vision*, pages 148–166. Springer, 2024b.
- Gao et al. (2017)

  J. Gao, C. Sun, Z. Yang, and R. Nevatia.
  Tall: Temporal activity localization via language query.
  In *Proceedings of the IEEE international conference on computer vision*, pages 5267–5275, 2017.
- He et al. (2024)

  C. He, R. Luo, Y. Bai, S. Hu, Z. L. Thai, J. Shen, J. Hu, X. Han, Y. Huang, Y. Zhang, et al.
  Olympiadbench: A challenging benchmark for promoting agi with olympiad-level bilingual multimodal scientific problems.
  *arXiv preprint arXiv:2402.14008*, 2024.
- Hendrycks et al. (2021)

  D. Hendrycks, C. Burns, S. Kadavath, A. Arora, S. Basart, E. Tang, D. Song, and J. Steinhardt.
  Measuring mathematical problem solving with the math dataset.
  *ArXiv preprint*, abs/2103.03874, 2021.
  URL <https://arxiv.org/abs/2103.03874>.
- Hu et al. (2025)

  K. Hu, P. Wu, F. Pu, W. Xiao, Y. Zhang, X. Yue, B. Li, and Z. Liu.
  Video-mmmu: Evaluating knowledge acquisition from multi-discipline professional videos.
  *arXiv preprint arXiv:2501.13826*, 2025.
- Jiang et al. (2024)

  D. Jiang, X. He, H. Zeng, C. Wei, M. Ku, Q. Liu, and W. Chen.
  Mantis: Interleaved multi-image instruction tuning.
  *arXiv preprint arXiv:2405.01483*, 2024.
- Karamcheti et al. (2024)

  S. Karamcheti, S. Nair, A. Balakrishna, P. Liang, T. Kollar, and D. Sadigh.
  Prismatic vlms: Investigating the design space of visually-conditioned language models.
  In *ICML*, 2024.
- Kazemzadeh et al. (2014)

  S. Kazemzadeh, V. Ordonez, M. Matten, and T. Berg.
  Referitgame: Referring to objects in photographs of natural scenes.
  In *Proceedings of the 2014 conference on empirical methods in natural language processing (EMNLP)*, pages 787–798, 2014.
- Kembhavi et al. (2016)

  A. Kembhavi, M. Salvato, E. Kolve, M. Seo, H. Hajishirzi, and A. Farhadi.
  A diagram is worth a dozen images.
  In *Computer Vision–ECCV 2016: 14th European Conference, Amsterdam, The Netherlands, October 11–14, 2016, Proceedings, Part IV 14*, pages 235–251. Springer, 2016.
- Lambert et al. (2025)

  N. Lambert, J. Morrison, V. Pyatkin, S. Huang, H. Ivison, F. Brahman, L. J. V. Miranda, A. Liu, N. Dziri, S. Lyu, Y. Gu, S. Malik, V. Graf, J. D. Hwang, J. Yang, R. L. Bras, O. Tafjord, C. Wilhelm, L. Soldaini, N. A. Smith, Y. Wang, P. Dasigi, and H. Hajishirzi.
  Tulu 3: Pushing frontiers in open language model post-training, 2025.
  URL <https://arxiv.org/abs/2411.15124>.
- Li et al. (2024a)

  B. Li, Y. Ge, Y. Chen, Y. Ge, R. Zhang, and Y. Shan.
  Seed-bench-2-plus: Benchmarking multimodal large language models with text-rich visual comprehension.
  *arXiv preprint arXiv:2404.16790*, 2024a.
- Li et al. (2025)

  K. Li, Z. Meng, H. Lin, Z. Luo, Y. Tian, J. Ma, Z. Huang, and T.-S. Chua.
  Screenspot-pro: Gui grounding for professional high-resolution computer use.
  *arXiv preprint arXiv:2504.07981*, 2025.
- Li et al. (2024b)

  L. Li, Y. Wei, Z. Xie, X. Yang, Y. Song, P. Wang, C. An, T. Liu, S. Li, B. Y. Lin, L. Kong, and Q. Liu.
  Vlrewardbench: A challenging benchmark for vision-language generative reward models.
  *ArXiv*, abs/2411.17451, 2024b.
  URL <https://api.semanticscholar.org/CorpusID:274281459>.
- Liu et al. (2023)

  H. Liu, C. Li, Q. Wu, and Y. J. Lee.
  Visual instruction tuning.
  In *NeurIPS*, 2023.
- Liu et al. (2024a)

  J. Liu, Y. Song, B. Y. Lin, W. Lam, G. Neubig, Y. Li, and X. Yue.
  Visualwebbench: How far have multimodal llms evolved in web page understanding and grounding?
  *arXiv preprint arXiv:2404.05955*, 2024a.
- Liu et al. (2024b)

  Y. Liu, H. Duan, Y. Zhang, B. Li, S. Zhang, W. Zhao, Y. Yuan, J. Wang, C. He, Z. Liu, et al.
  Mmbench: Is your multi-modal model an all-around player?
  In *European conference on computer vision*, pages 216–233. Springer, 2024b.
- Liu et al. (2024c)

  Y. Liu, Z. Li, M. Huang, B. Yang, W. Yu, C. Li, X.-C. Yin, C.-L. Liu, L. Jin, and X. Bai.
  Ocrbench: on the hidden mystery of ocr in large multimodal models.
  *Science China Information Sciences*, 67(12):220102, 2024c.
- Lu et al. (2023)

  P. Lu, H. Bansal, T. Xia, J. Liu, C. Li, H. Hajishirzi, H. Cheng, K.-W. Chang, M. Galley, and J. Gao.
  Mathvista: Evaluating mathematical reasoning of foundation models in visual contexts.
  *arXiv preprint arXiv:2310.02255*, 2023.
- MAA (2024)

  MAA.
  American invitational mathematics examination - aime.
  In *American Invitational Mathematics Examination - AIME*, 2024.
  URL <https://maa.org/math-competitions/american-invitational-mathematics-examination-aime>.
- MAA (2025)

  MAA.
  American invitational mathematics examination - aime.
  In *American Invitational Mathematics Examination - AIME*, 2025.
  URL <https://maa.org/math-competitions/american-invitational-mathematics-examination-aime>.
- Mangalam et al. (2023)

  K. Mangalam, R. Akshulakov, and J. Malik.
  Egoschema: A diagnostic benchmark for very long-form video language understanding.
  *Advances in Neural Information Processing Systems*, 36:46212–46244, 2023.
- Masry et al. (2022)

  A. Masry, D. X. Long, J. Q. Tan, S. Joty, and E. Hoque.
  Chartqa: A benchmark for question answering about charts with visual and logical reasoning.
  *arXiv preprint arXiv:2203.10244*, 2022.
- Mathew et al. (2021)

  M. Mathew, D. Karatzas, and C. Jawahar.
  Docvqa: A dataset for vqa on document images.
  In *Proceedings of the IEEE/CVF winter conference on applications of computer vision*, pages 2200–2209, 2021.
- Mathew et al. (2022)

  M. Mathew, V. Bagal, R. Tito, D. Karatzas, E. Valveny, and C. Jawahar.
  Infographicvqa.
  In *Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision*, pages 1697–1706, 2022.
- Nagaraja et al. (2016)

  V. K. Nagaraja, V. I. Morariu, and L. S. Davis.
  Modeling context between objects for referring expression understanding.
  In *Computer Vision–ECCV 2016: 14th European Conference, Amsterdam, The Netherlands, October 11–14, 2016, Proceedings, Part IV 14*, pages 792–807. Springer, 2016.
- OpenAI (2025)

  OpenAI.
  Computer-using agent: Introducing a universal interface for ai to interact with the digital world.
  2025.
  URL <https://openai.com/index/computer-using-agent>.
- Ouyang et al. (2022)

  L. Ouyang, J. Wu, X. Jiang, D. Almeida, C. L. Wainwright, P. Mishkin, C. Zhang, S. Agarwal, K. Slama, A. Ray, J. Schulman, J. Hilton, F. Kelton, L. Miller, M. Simens, A. Askell, P. Welinder, P. F. Christiano, J. Leike, and R. Lowe.
  Training language models to follow instructions with human feedback.
  In *NeurIPS*, 2022.
- Padlewski et al. (2024)

  P. Padlewski, M. Bain, M. Henderson, Z. Zhu, N. Relan, H. Pham, D. Ong, K. Aleksiev, A. Ormazabal, S. Phua, et al.
  Vibe-eval: A hard evaluation suite for measuring progress of multimodal language models.
  *ArXiv preprint*, abs/2405.02287, 2024.
- Paiss et al. (2023)

  R. Paiss, A. Ephrat, O. Tov, S. Zada, I. Mosseri, M. Irani, and T. Dekel.
  Teaching clip to count to ten.
  In *Proceedings of the IEEE/CVF International Conference on Computer Vision*, pages 3170–3180, 2023.
- Qiao et al. (2024)

  R. Qiao, Q. Tan, G. Dong, M. Wu, C. Sun, X. Song, Z. GongQue, S. Lei, Z. Wei, M. Zhang, et al.
  We-math: Does your large multimodal model achieve human-like mathematical reasoning?
  *arXiv preprint arXiv:2407.01284*, 2024.
- Qin et al. (2025a)

  Y. Qin, Y. Ye, J. Fang, H. Wang, S. Liang, S. Tian, J. Zhang, J. Li, Y. Li, S. Huang, et al.
  Ui-tars: Pioneering automated gui interaction with native agents.
  *arXiv preprint arXiv:2501.12326*, 2025a.
- Qin et al. (2025b)

  Y. Qin, Y. Ye, J. Fang, H. Wang, S. Liang, S. Tian, J. Zhang, J. Li, Y. Li, S. Huang, et al.
  Ui-tars: Pioneering automated gui interaction with native agents.
  *arXiv preprint arXiv:2501.12326*, 2025b.
- Rahmanzadehgervi et al. (2025)

  P. Rahmanzadehgervi, L. Bolton, M. R. Taesiri, and A. T. Nguyen.
  Vision language models are blind: Failing to translate detailed visual features into words, 2025.
  URL <https://arxiv.org/abs/2407.06581>.
- Rein et al. (2024)

  D. Rein, B. L. Hou, A. C. Stickland, J. Petty, R. Y. Pang, J. Dirani, J. Michael, and S. R. Bowman.
  Gpqa: A graduate-level google-proof q&a benchmark.
  In *First Conference on Language Modeling*, 2024.
- Rezatofighi et al. (2019)

  H. Rezatofighi, N. Tsoi, J. Gwak, A. Sadeghian, I. Reid, and S. Savarese.
  Generalized intersection over union: A metric and a loss for bounding box regression.
  In *Proceedings of the IEEE/CVF conference on computer vision and pattern recognition*, pages 658–666, 2019.
- Shao et al. (2024)

  Z. Shao, P. Wang, Q. Zhu, R. Xu, J. Song, X. Bi, H. Zhang, M. Zhang, Y. Li, Y. Wu, et al.
  Deepseekmath: Pushing the limits of mathematical reasoning in open language models.
  *arXiv preprint arXiv:2402.03300*, 2024.
- Sheng et al. (2024)

  G. Sheng, C. Zhang, Z. Ye, X. Wu, W. Zhang, R. Zhang, Y. Peng, H. Lin, and C. Wu.
  Hybridflow: A flexible and efficient rlhf framework.
  *ArXiv preprint*, abs/2409.19256, 2024.
  URL <https://arxiv.org/abs/2409.19256>.
- Team (2024)

  C. Team.
  Chameleon: Mixed-modal early-fusion foundation models.
  *arXiv preprint arXiv:2405.09818*, 2024.
- Tong et al. (2024)

  P. Tong, E. Brown, P. Wu, S. Woo, A. J. V. IYER, S. C. Akula, S. Yang, J. Yang, M. Middepogu, Z. Wang, et al.
  Cambrian-1: A fully open, vision-centric exploration of multimodal llms.
  *Advances in Neural Information Processing Systems*, 37:87310–87356, 2024.
- Wang et al. (2024a)

  K. Wang, J. Pan, W. Shi, Z. Lu, H. Ren, A. Zhou, M. Zhan, and H. Li.
  Measuring multimodal mathematical reasoning with math-vision dataset.
  *Advances in Neural Information Processing Systems*, 37:95095–95169, 2024a.
- Wang et al. (2024b)

  Y. Wang, X. Ma, G. Zhang, Y. Ni, A. Chandra, S. Guo, W. Ren, A. Arulraj, X. He, Z. Jiang, T. Li, M. Ku, K. Wang, A. Zhuang, R. Fan, X. Yue, and W. Chen.
  Mmlu-pro: A more robust and challenging multi-task language understanding benchmark.
  In A. Globersons, L. Mackey, D. Belgrave, A. Fan, U. Paquet, J. M. Tomczak, and C. Zhang, editors, *Advances in Neural Information Processing Systems 38: Annual Conference on Neural Information Processing Systems 2024, NeurIPS 2024, Vancouver, BC, Canada, December 10 - 15, 2024*, 2024b.
  URL <http://papers.nips.cc/paper_files/paper/2024/hash/ad236edc564f3e3156e1b2feafb99a24-Abstract-Datasets_and_Benchmarks_Track.html>.
- Wang et al. (2025)

  Y. Wang, B. Xu, Z. Yue, Z. Xiao, Z. Wang, L. Zhang, D. Yang, W. Wang, and Q. Jin.
  Timezero: Temporal video grounding with reasoning-guided lvlm.
  *arXiv preprint arXiv:2503.13377*, 2025.
- Wang et al. (2024c)

  Z. Wang, M. Xia, L. He, H. Chen, Y. Liu, R. Zhu, K. Liang, X. Wu, H. Liu, S. Malladi, et al.
  Charxiv: Charting gaps in realistic chart understanding in multimodal llms.
  *Advances in Neural Information Processing Systems*, 37:113569–113697, 2024c.
- Wu and Xie (2023)

  P. Wu and S. Xie.
  V*: Guided visual search as a core mechanism in multimodal llms, 2023.
  URL <https://arxiv.org/abs/2312.14135>.
- Wu et al. (2024)

  Z. Wu, Z. Wu, F. Xu, Y. Wang, Q. Sun, C. Jia, K. Cheng, Z. Ding, L. Chen, P. P. Liang, et al.
  Os-atlas: A foundation action model for generalist gui agents.
  *arXiv preprint arXiv:2410.23218*, 2024.
- Xiao et al. (2024)

  Y. Xiao, E. Sun, T. Liu, and W. Wang.
  Logicvista: Multimodal llm logical reasoning benchmark in visual contexts.
  *arXiv preprint arXiv:2407.04973*, 2024.
- Xiaomi (2025)

  L.-C.-T. Xiaomi.
  Mimo: Unlocking the reasoning potential of language model–from pretraining to posttraining.
  *arXiv preprint arXiv:2505.07608*, 2025.
- Xie et al. (2024)

  T. Xie, D. Zhang, J. Chen, X. Li, S. Zhao, R. Cao, T. J. Hua, Z. Cheng, D. Shin, F. Lei, et al.
  Osworld: Benchmarking multimodal agents for open-ended tasks in real computer environments.
  *Advances in Neural Information Processing Systems*, 37:52040–52094, 2024.
- Xie et al. (2025)

  T. Xie, J. Deng, X. Li, J. Yang, H. Wu, J. Chen, W. Hu, X. Wang, Y. Xu, Z. Wang, Y. Xu, J. Wang, D. Sahoo, T. Yu, and C. Xiong.
  Scaling computer-use grounding via user interface decomposition and synthesis, 2025.
  URL <https://arxiv.org/abs/2505.13227>.
- Xu et al. (2023)

  H. Xu, S. Xie, X. E. Tan, P.-Y. Huang, R. Howes, V. Sharma, S.-W. Li, G. Ghosh, L. Zettlemoyer, and C. Feichtenhofer.
  Demystifying clip data.
  *arXiv preprint arXiv:2309.16671*, 2023.
- Xu et al. (2024)

  Y. Xu, Z. Wang, J. Wang, D. Lu, T. Xie, A. Saha, D. Sahoo, T. Yu, and C. Xiong.
  Aguvis: Unified pure vision agents for autonomous gui interaction.
  *arXiv preprint arXiv:2412.04454*, 2024.
- Ye et al. (2025)

  J. Ye, Z. Xie, L. Zheng, J. Gao, Z. Wu, X. Jiang, Z. Li, and L. Kong.
  Dream 7b, 2025.
  URL <https://hkunlp.github.io/blog/2025/dream>.
- Yu et al. (2016)

  L. Yu, P. Poirson, S. Yang, A. C. Berg, and T. L. Berg.
  Modeling context in referring expressions.
  In *Computer Vision–ECCV 2016: 14th European Conference, Amsterdam, The Netherlands, October 11-14, 2016, Proceedings, Part II 14*, pages 69–85. Springer, 2016.
- Yue et al. (2024a)

  X. Yue, Y. Ni, K. Zhang, T. Zheng, R. Liu, G. Zhang, S. Stevens, D. Jiang, W. Ren, Y. Sun, et al.
  Mmmu: A massive multi-discipline multimodal understanding and reasoning benchmark for expert agi.
  In *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition*, pages 9556–9567, 2024a.
- Yue et al. (2024b)

  X. Yue, Y. Ni, T. Zheng, K. Zhang, R. Liu, G. Zhang, S. Stevens, D. Jiang, W. Ren, Y. Sun, C. Wei, B. Yu, R. Yuan, R. Sun, M. Yin, B. Zheng, Z. Yang, Y. Liu, W. Huang, H. Sun, Y. Su, and W. Chen.
  MMMU: A massive multi-discipline multimodal understanding and reasoning benchmark for expert AGI.
  In *CVPR*, pages 9556–9567, 2024b.
- Yue et al. (2024c)

  X. Yue, T. Zheng, Y. Ni, Y. Wang, K. Zhang, S. Tong, Y. Sun, B. Yu, G. Zhang, H. Sun, et al.
  Mmmu-pro: A more robust multi-discipline multimodal understanding benchmark.
  *arXiv preprint arXiv:2409.02813*, 2024c.
- Zhang et al. (2024a)

  K. Zhang, B. Li, P. Zhang, F. Pu, J. A. Cahyono, K. Hu, S. Liu, Y. Zhang, J. Yang, C. Li, and Z. Liu.
  Lmms-eval: Reality check on the evaluation of large multimodal models, 2024a.
  URL <https://arxiv.org/abs/2407.12772>.
- Zhang et al. (2024b)

  R. Zhang, D. Jiang, Y. Zhang, H. Lin, Z. Guo, P. Qiu, A. Zhou, P. Lu, K.-W. Chang, P. Gao, et al.
  Mathverse: Does your multi-modal llm truly see the diagrams in visual math problems?
  *ArXiv preprint*, abs/2403.14624, 2024b.
- Zhang et al. (2024c)

  Y.-F. Zhang, H. Zhang, H. Tian, C. Fu, S. Zhang, J. Wu, F. Li, K. Wang, Q. Wen, Z. Zhang, et al.
  Mme-realworld: Could your multimodal llm challenge high-resolution real-world scenarios that are difficult for humans?
  *arXiv preprint arXiv:2408.13257*, 2024c.
- Zheng et al. (2023)

  L. Zheng, W. Chiang, Y. Sheng, S. Zhuang, Z. Wu, Y. Zhuang, Z. Lin, Z. Li, D. Li, E. P. Xing, H. Zhang, J. E. Gonzalez, and I. Stoica.
  Judging llm-as-a-judge with mt-bench and chatbot arena.
  In *NeurIPS*, 2023.
- Zhou et al. (2023)

  J. Zhou, T. Lu, S. Mishra, S. Brahma, S. Basu, Y. Luan, D. Zhou, and L. Hou.
  Instruction-following evaluation for large language models, 2023.
  URL <https://arxiv.org/abs/2311.07911>.
- Zitkovich et al. (2023)

  B. Zitkovich, T. Yu, S. Xu, P. Xu, T. Xiao, F. Xia, J. Wu, P. Wohlhart, S. Welker, A. Wahid, et al.
  Rt-2: Vision-language-action models transfer web knowledge to robotic control.
  In *Conference on Robot Learning*, pages 2165–2183. PMLR, 2023.
- Zou et al. (2024)

  C. Zou, X. Guo, R. Yang, J. Zhang, B. Hu, and H. Zhang.
  Dynamath: A dynamic visual benchmark for evaluating mathematical reasoning robustness of vision language models.
  *arXiv preprint arXiv:2411.00836*, 2024.

## Appendix A Contributions and Acknowledgments

We would like to express our sincere gratitude to all contributors for their invaluable support and efforts, including the Xiaomi LLM-Plus, Mify, MiChat and CloudML teams, as well as those not explicitly listed in this paper.
Authors within each role are listed in reverse order by their first names.

Core Contributors
  
 Zihao Yue
  
 Zhenru Lin
  
 Yifan Song
  
 Weikun Wang
  
 Shuhuai Ren
  
 Shuhao Gu
  
 Shicheng Li
  
 Peidian Li
  
 Liang Zhao
  
 Lei Li
  
 Kainan Bao
  
 Hao Tian
  
 Hailin Zhang
  
 Gang Wang
  
 Dawei Zhu
  
 Cici
  
 Chenhong He
  
 Bowen Ye
  
 Bowen Shen

Contributors
  
 Zihan Zhang
  
 Zihan Jiang
  
 Zhixian Zheng
  
 Zhichao Song
  
 Zhenbo Luo
  
 Yue Yu
  
 Yudong Wang
  
 Yuanyuan Tian
  
 Yu Tu
  
 Yihan Yan
  
 Yi Huang
  
 Xu Wang
  
 Xinzhe Xu
  
 Xingchen Song
  
 Xing Zhang
  
 Xing Yong
  
 Xin Zhang
  
 Xiangwei Deng
  
 Wenyu Yang
  
 Wenhan Ma
  
 Weiwei Lv
  
 Weiji Zhuang
  
 Wei Liu
  
 Sirui Deng
  
 Shuo Liu
  
 Shimao Chen
  
 Shihua Yu
  
 Shaohui Liu
  
 Shande Wang
  
 Rui Ma
  
 Qiantong Wang
  
 Peng Wang
  
 Nuo Chen
  
 Menghang Zhu
  
 Kangyang Zhou
  
 Kang Zhou
  
 Kai Fang
  
 Jun Shi
  
 Jinhao Dong
  
 Jiebao Xiao
  
 Jiaming Xu
  
 Huaqiu Liu
  
 Hongshen Xu
  
 Heng Qu
  
 Haochen Zhao
  
 Hanglong Lv
  
 Guoan Wang
  
 Duo Zhang
  
 Dong Zhang
  
 Di Zhang
  
 Chong Ma
  
 Chang Liu
  
 Can Cai
  
 Bingquan Xia

## Appendix B Model Configuration of MiMo-VL-7B

In Table [4](#A2.T4 "Table 4 ‣ Appendix B Model Configuration of MiMo-VL-7B ‣ MiMo-VL Technical Report"), the architecture and configuration of MiMo-VL-7B are detailed.

|  |  |  |
| --- | --- | --- |
|  | Vision Encoder | Language Model |
| # Layers | 32 | 36 |
| # Heads | 16 | 32 |
| Hidden Size | 1280 | 4096 |
| Intermediate Size | 3456 | 11008 |
| Position Embedding | 2D RoPE | MRoPE ([Bai et al., 2025b](#bib.bib3)) |
| Patch Size | 14 | - |

Table 4: Configuration of MiMo-VL-7B. We adopt Qwen2.5-ViT ([Bai et al., 2025a](#bib.bib2)) as our visual encoder to support native resolution inputs, and MiMo-7B-Base ([Xiaomi, 2025](#bib.bib61)) as our LLM backbone to leverage its strong reasoning capability. Compared to the LLM backbone of Qwen2.5-VL-7B ([Bai et al., 2025a](#bib.bib2)), our LLM differs in its number of layers (36 vs. 28), hidden size (4096 vs. 3584), and intermediate size (11008 vs. 18944).

## Appendix C Evaluation Benchmarks

We evaluate our models across 50 diverse tasks, including:

##### General Visual Understanding

AI2D ([Kembhavi et al., 2016](#bib.bib23)),
BLINK ([Fu et al., 2024b](#bib.bib15)).
CV-Bench ([Tong et al., 2024](#bib.bib53)),
MMMU ([Yue et al., 2024a](#bib.bib68)),
MMMU-Pro (Standard and Vision) ([Yue et al., 2024c](#bib.bib70)),
Mantis ([Jiang et al., 2024](#bib.bib20)),
MME-RealWorld (English and Chinese) ([Zhang et al., 2024c](#bib.bib73)),
MMBench (English and Chinese) ([Liu et al., 2024b](#bib.bib30)),
VibeEval ([Padlewski et al., 2024](#bib.bib42)),
VL-RewardBench ([Li et al., 2024b](#bib.bib27)),
V* ([Wu and Xie, 2023](#bib.bib58)),
and VLMs are Blind ([Rahmanzadehgervi et al., 2025](#bib.bib47)).

##### General Grounding and Counting

RefCOCO ([Yu et al., 2016](#bib.bib67); [Nagaraja et al., 2016](#bib.bib39); [Kazemzadeh et al., 2014](#bib.bib22)),
CountBench ([Paiss et al., 2023](#bib.bib43)), and
PixmoCount ([Deitke et al., 2024](#bib.bib11))

##### Document and Chart Understanding

ChartQA ([Masry et al., 2022](#bib.bib36)), InfographicVQA ([Mathew et al., 2022](#bib.bib38)), DocVQA ([Mathew et al., 2021](#bib.bib37)),
OCRBench ([Liu et al., 2024c](#bib.bib31)),
SEED-Bench-2-Plus ([Li et al., 2024a](#bib.bib25)),
and CharXiv (RQ/DQ) ([Wang et al., 2024c](#bib.bib57)).

##### Video Understanding and Localization

Video-MME ([Fu et al., 2024a](#bib.bib14)),
Video-MMMU ([Hu et al., 2025](#bib.bib19)),
EgoSchema ([Mangalam et al., 2023](#bib.bib35)),
and Charades-STA [Gao et al. (2017)](#bib.bib16).

##### GUI Understanding and Grounding

WebSrc ([Chen et al., 2021](#bib.bib6)), VisualWebBench ([Liu et al., 2024a](#bib.bib29)), ScreenSpot ([Cheng et al., 2024](#bib.bib8)),
ScreenSpot-V2 ([Wu et al., 2024](#bib.bib59)),
ScreenSpot-Pro ([Li et al., 2025](#bib.bib26)),
and OSWorld-G ([Xie et al., 2025](#bib.bib63)).

##### Text-only Benchmarks

GPQA ([Rein et al., 2024](#bib.bib48)), SuperGPQA ([Du et al., 2025](#bib.bib12)), DROP ([Dua et al., 2019](#bib.bib13)), MMLU-Pro ([Wang et al., 2024b](#bib.bib55)),
and IFEval ([Zhou et al., 2023](#bib.bib75)).

##### Multimodal Reasoning

OlympiadBench ([He et al., 2024](#bib.bib17)), MathVision ([Wang et al., 2024a](#bib.bib54)), MathVerse (Vision Only) ([Zhang et al., 2024b](#bib.bib72)), DynaMath ([Zou et al., 2024](#bib.bib77)), WeMath ([Qiao et al., 2024](#bib.bib44)), LogicVista ([Xiao et al., 2024](#bib.bib60)),
and MathVista ([Lu et al., 2023](#bib.bib32)).

##### Text Reasoning

MATH500 ([Hendrycks et al., 2021](#bib.bib18)), AIME 2024 ([MAA, 2024](#bib.bib33)), and AIME 2025 ([MAA, 2025](#bib.bib34)).

## Appendix D GUI Action Space

The syntax and definition for each action in the GUI action space are summarized in Table [5](#A4.T5 "Table 5 ‣ Appendix D GUI Action Space ‣ MiMo-VL Technical Report").

|  |  |
| --- | --- |
| click | Syntax: {"action":"click","start_point":[x,y],"text"(opt.):text} |
|  | Definition: Click at (x, y) on an element with the given text. |
| scroll | Syntax: {"action":"scroll","direction":dir,"scroll_distance"(opt.):dist} |
|  | Definition: Scroll in the given direction by a specified distance. |
|  | Notes: Scroll up/down → to see more below/above. The same logic applies horizontally. |
| input | Syntax: {"action":"input","text":text,"start_point"(opt.):[x,y]} |
|  | Definition: Type the specified text at coordinates (x, y). |
| drag | Syntax: {"action":"drag","start_point":[x1,y1],"end_point":[x2,y2]} |
|  | Definition: Drag from the start_point to the end_point. |
| open | Syntax: {"action":"open","app":app_name} |
|  | Definition: Open the specified application app_name. |
| press | Syntax: {"action":"press","keys":[key1,key2,...]} |
|  | Definition: Press the specified hotkeys ([key1, key2,...]). |
| finished | Syntax: {"action":"finished","status":status} |
|  | Definition: Mark the task as complete with a given status. |
| longpress | Syntax: {"action":"longpress","start_point":[x,y]} |
|  | Definition: Long press at coordinates (x,y). |
| hover | Syntax: {"action":"hover"} |
|  | Definition: Hover the mouse over a location. |
| select | Syntax: {"action":"select","text":text} |
|  | Definition: Select the specified text. |
| wait | Syntax: {"action":"wait"} |
|  | Definition: Pause for a brief moment. |
| appswitch | Syntax: {"action":"appswitch","app":app_name} |
|  | Definition: Switch to the specified application app_name. |

Table 5: Action Space Details. opt. denotes optional.

## Appendix E More Qualitative Examples

|  |
| --- |
| Input image:Refer to caption |
| Instruction: 完成该试卷    MiMo-VL-7B: <think>...</think> 第1题：集合的交集 集合 A={0,1,2,8}A=\{0,1,2,8\}，B={−1,1,6,8}B=\{-1,1,6,8\}，交集为同时属于两个集合的元素，即 A∩B={1,8}A\cap B=\{1,8\}。 第2题：复数的实部 设 z=x+y​iz=x+yi（x,yx,y 为实数），由 i⋅z=1+2​ii\cdot z=1+2i，即 i⁡(x+y​i)=−y+x​i=1+2​ii(x+yi)=-y+xi=1+2i。 分离实部和虚部：−y=1-y=1（实部），x=2x=2（虚部）。故 zz 的实部为 22。 第3题：茎叶图的平均数 茎叶图中，茎为十位，叶为个位。分数为 89,89,90,91,9189,89,90,91,91（共5个）。 平均数为 89+89+90+91+915=4505=90\frac{89+89+90+91+91}{5}=\frac{450}{5}=90。 第4题：伪代码的循环结果 初始化 I=1I=1，S=1S=1。循环条件 I<6I<6： - 第1次循环：I=1+2=3I=1+2=3，S=2×1=2S=2\times 1=2； - 第2次循环：I=3+2=5I=3+2=5，S=2×2=4S=2\times 2=4； - 第3次循环：I=5+2=7I=5+2=7（不满足 I<6I<6，退出循环）。 最终 S=8S=8。 第5题：函数的定义域 函数 f⁡(x)=log2⁡x−1f(x)=\sqrt{\log_{2}x-1} 需满足： 1. 二次根式内非负：log2⁡x−1≥0\log_{2}x-1\geq 0； 2. 对数有定义：x>0x>0。 由 log2⁡x≥1\log_{2}x\geq 1 得 x≥21=2x\geq 2^{1}=2，故定义域为 [2,+∞)[2,+\infty)。 第6题：组合的概率 2男3女中选2人，总选法 C52=10C_{5}^{2}=10；选中2女生的选法 C32=3C_{3}^{2}=3。 概率为 310\frac{3}{10}。 第7题：正弦函数的对称轴 函数 y=sin⁡(2​x+φ)y=\sin(2x+\varphi) 关于 x=π3x=\frac{\pi}{3} 对称，即 2⋅π3+φ=k​π+π22\cdot\frac{\pi}{3}+\varphi=k\pi+\frac{\pi}{2}（k∈ℤk\in\mathbb{Z}）。 取 k=0k=0，得 φ=−π6\varphi=-\frac{\pi}{6}（满足 −π2<φ<π2-\frac{\pi}{2}<\varphi<\frac{\pi}{2}）。 第8题：双曲线的离心率 双曲线 x2a2−y2b2=1\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1，右焦点 F⁡(c,0)F(c,0)（c=a2+b2c=\sqrt{a^{2}+b^{2}}），渐近线 b​x−a​y=0bx-ay=0。 焦点到渐近线的距离为 |b​c|a2+b2=b\frac{|bc|}{\sqrt{a^{2}+b^{2}}}=b，由题设 b=32​cb=\frac{\sqrt{3}}{2}c。 结合 c2=a2+b2c^{2}=a^{2}+b^{2}，得 a=c2a=\frac{c}{2}，离心率 e=ca=2e=\frac{c}{a}=2。 第9题：周期函数与复合函数 f⁡(x+4)=f⁡(x)f(x+4)=f(x) 说明周期为4。 - f⁡(15)=f⁡(15−4×3)=f⁡(3)=f⁡(−1)f(15)=f(15-4\times 3)=f(3)=f(-1)（3=−1+43=-1+4）； - x∈(−2,0]x\in(-2,0] 时，f⁡(−1)=|−1+12|=12f(-1)=|-1+\frac{1}{2}|=\frac{1}{2}； - f⁡(12)=cos⁡(π2⋅12)=cos⁡π4=22f(\frac{1}{2})=\cos\left(\frac{\pi}{2}\cdot\frac{1}{2}\right)=\cos\frac{\pi}{4}=\frac{\sqrt{2}}{2}（12∈(0,2]\frac{1}{2}\in(0,2]）。 第10题：多面体的体积 正方体棱长2，面中心坐标为 (±1,0,0),(0,±1,0),(0,0,±1)(\pm 1,0,0),(0,\pm 1,0),(0,0,\pm 1)，构成正八面体。 正八面体体积为两个四棱锥之和，底面正方形边长 2\sqrt{2}，高1，体积为 2×13×2×1=432\times\frac{1}{3}\times 2\times 1=\frac{4}{3}。 第11题：函数的极值与零点 函数 f⁡(x)=2​x3−a​x2+1f(x)=2x^{3}-ax^{2}+1 在 (0,+∞)(0,+\infty) 内有且只有一个零点，导数 f′​(x)=6​x2−2​a​xf^{\prime}(x)=6x^{2}-2ax，临界点 x=0x=0 和 x=a3x=\frac{a}{3}。 当 f⁡(a3)=0f(\frac{a}{3})=0 时（极小值为0，仅1个零点），解得 a=3a=3。 f⁡(x)f(x) 在 [−1,1][-1,1] 上，f⁡(0)=1f(0)=1（最大值），f⁡(−1)=−4f(-1)=-4（最小值），和为 1+(−4)=−31+(-4)=-3。 第12题：向量垂直的条件 设 A⁡(x,2​x)A(x,2x)，A​B=(5−x,−2​x)AB=(5-x,-2x)，圆心 C⁡(x+52,x)C\left(\frac{x+5}{2},x\right)，另一交点 D⁡(1,2)D(1,2)（由圆与直线交点唯一性得）。 向量 C​D→=(−x−32,2−x)\overrightarrow{CD}=\left(\frac{-x-3}{2},2-x\right)，由 A​B→⋅C​D→=0\overrightarrow{AB}\cdot\overrightarrow{CD}=0，解得 x=3x=3。 答案 1. {𝟏,𝟖}\boldsymbol{\{1,8\}} 2. 𝟐\boldsymbol{2} 3. 𝟗𝟎\boldsymbol{90} 4. 𝟖\boldsymbol{8} 5. [𝟐,+∞)\boldsymbol{[2,+\infty)} 6. 𝟑𝟏𝟎\boldsymbol{\frac{3}{10}} 7. −𝝅𝟔\boldsymbol{-\frac{\pi}{6}} 8. 𝟐\boldsymbol{2} 9. 𝟐𝟐\boldsymbol{\frac{\sqrt{2}}{2}} 10. 𝟒𝟑\boldsymbol{\frac{4}{3}} 11. −𝟑\boldsymbol{-3} 12. 𝟑\boldsymbol{3} |

Figure 10: Example of MiMo-VL-7B-RL answering all questions within a whole test paper.

|  |  |
| --- | --- |
| Refer to caption | Instruction: 这瓶可乐喝10罐会摄入多少克钠？ MiMo-VL-7B-RL: <think>...</think>要计算喝10罐可口可乐零度时摄入的钠量，需按以下步骤分析：  1.  步骤1：明确营养成分表信息 从图片中“营养成分表”可知：每100毫升该饮料中，钠的含量为 18毫克。 2.  步骤2：确定单罐饮料容量（行业常见规格） 可口可乐零度的罐装规格通常为 330毫升/罐（这是饮料行业的常见罐装容量，若实际容量不同需以产品标注为准，此处默认330ml）。 3.  步骤3：计算单罐钠含量 单罐（330ml）中钠的含量 = 每100ml钠含量 × 单罐容量 ÷ 100 即：18​毫克/100ml​×​330​ml​÷​100=59.4​毫克18\ \text{毫克/100ml}×330\ \text{ml}÷100=59.4\ \text{毫克} 4.  步骤4：计算10罐钠总量 10罐钠总量 = 单罐钠含量 × 10 即：59.4​毫克​×​10=594​毫克59.4\ \text{毫克}×10=594\ \text{毫克} 因此，喝10罐该款可口可乐零度，约摄入 594毫克 钠。 |
| Refer to caption | Instruction: 该发票缺失的税额应该是多少？ MiMo-VL-7B-RL: <think>...</think>要计算该发票的税额，需结合税率和价税合计金额来推导：  1.  步骤1：明确关键信息 - 发票税率：13%13\%（发票中“税率”栏显示） - 价税合计金额（大写）：壹拾壹万贰仟伍佰捌拾玖圆伍角贰分，对应小写为 112589.52元 2.  步骤2：税额的计算逻辑 发票税额 = 价税合计金额 × （1 - 税率）× 税率 （即：总价价税合计 = 不含税金额 + 税额 → 税额 = 价税合计 × 税率 ÷ (1 + 税率) ） 设不含税金额为 X\ X ，则： X+X​×​13%=112589.52X+X×13\%=112589.52 X​×​1.13=112589.52X×1.13=112589.52 X=112589.52​÷​1.13=99636.74X=112589.52÷1.13=99636.74 元【不含税金额】 税额 = 不含税金额 × 税率 = 99636.74 × 13% = 12952.78 元 |

Figure 11: Example of MiMo-VL-7B-RL solving complex OCR problems with reasoning.

|  |  |
| --- | --- |
| Refer to caption | Instruction: How many muffin in the image? MiMo-VL-7B-RL: <think>...</think> To determine the number of muffins in the image, we analyze the 3×4 grid (12 cells total) and count muffins row by row: - Top row (row 1): Columns 1 and 3 are muffins → 2 muffins. - Middle row (row 2): Columns 2 and 4 are muffins → 2 muffins. - Bottom row (row 3): Columns 1 and 3 are muffins → 2 muffins. Adding these, 2+2+2=62+2+2=6. There are 6 muffins in the image. |
| Refer to caption | Instruction: How many cats in the image? MiMo-VL-7B-RL: <think>...</think> To determine the number of cats in the image, we can observe and count: - There is a black cat lying on the floor. - There is a white and brown cat sitting behind the black cat. Thus, the number of cats in the image is 2. |
| Refer to caption | Instruction: How many dogs in the image? MiMo-VL-7B-RL: <think>...</think> To determine the number of dogs in the image, we analyze both the printed dogs on the blanket and the real dog in the foreground:  1.  Printed dogs on the blanket: The blanket features a grid of dog faces. Counting these, we see 3 rows with 4 dogs each, so 3×4=123\times 4=12 printed dogs. 2.  Real dog in the foreground: There is 1 real dog standing in front of the blanket. Adding these together, 12+1=1312+1=13. Thus, the total number of dogs in the image is 13. |

Figure 12: Example of MiMo-VL-7B-RL solving detailed perception problem.

|  |  |
| --- | --- |
| Refer to caption | Instruction: answer all the questions. MiMo-VL-7B-RL: <think>...</think>  1.  Problem 7 To find xx and yy, we analyze the two right triangles formed by the height:  - **Right triangle (30° angle)**: Hypotenuse = 44. The height hh (opposite 30°) is 44⋅sin⁡(30∘)=44⋅0.5=2244\cdot\sin(30^{\circ})=44\cdot 0.5=22. The base segment yy (adjacent to 30°) is 44⋅cos⁡(30∘)=44⋅32=22​344\cdot\cos(30^{\circ})=44\cdot\frac{\sqrt{3}}{2}=22\sqrt{3}.  - **Right triangle (45° angle)**: This is a 45-45-90 triangle, so legs are equal. The height h=22h=22, so the other leg (left base segment) is also 22. Hypotenuse xx (45-45-90 ratio: leg ⋅2\cdot\sqrt{2}) is 22​222\sqrt{2}. 2.  Problem 8 For a square with diagonal d=22d=22, the side length ss relates to the diagonal by d=s​2d=s\sqrt{2}. Solving for ss: s=d2=222=11​2s=\frac{d}{\sqrt{2}}=\frac{22}{\sqrt{2}}=11\sqrt{2} (rationalizing the denominator). 3.  Problem 9 A pentagon circumscribed about a circle (tangential pentagon) has the property that the sum of the lengths of all sides equals 2×2\times the sum of the tangent segments from each vertex. However, since the problem provides the side lengths Q​Z=10QZ=10, Y​X=9YX=9, X​W=13XW=13, U​W=16UW=16, S​U=17SU=17, and the pentagon is tangential, the perimeter is the sum of these sides (as they represent the sides of the pentagon).  Perimeter =10+9+13+16+17=65=10+9+13+16+17=65. 4.  Problem 10 S​R¯\overline{SR} is tangent to ⊙Q\odot Q at RR, so Q​R⟂S​RQR\perp SR (tangent is perpendicular to radius). Thus, △​Q​R​S\triangle QRS is a right triangle with Q​R=7QR=7 (radius) and Q​S=25QS=25 (hypotenuse). By the Pythagorean theorem: S​R=Q​S2−Q​R2=252−72=625−49=576=24SR=\sqrt{QS^{2}-QR^{2}}=\sqrt{25^{2}-7^{2}}=\sqrt{625-49}=\sqrt{576}=24 5.  Problem 11 A perpendicular from the circle’s center to a chord bisects the chord. The chord length is 16, so half the chord is 162=8\frac{16}{2}=8. The distance from the center to the chord is 6, forming a right triangle with legs 6 and 8, and hypotenuse xx (radius). By the Pythagorean theorem: x=62+82=36+64=100=10x=\sqrt{6^{2}+8^{2}}=\sqrt{36+64}=\sqrt{100}=10 6.  Problem 12 Since R,S,TR,S,T are collinear and SS is between RR and TT, R​S+S​T=R​TRS+ST=RT. Substitute R​S=2​w+1RS=2w+1, S​T=w−1ST=w-1, and R​T=18RT=18:    (2​w+1)+(w−1)=18(2w+1)+(w-1)=18 Simplify: 3​w=18⟹w=63w=18\implies w=6. Substitute w=6w=6 into R​SRS: R​S=2​(6)+1=13RS=2(6)+1=13 Final Answers 7. x=22​2x=22\sqrt{2}, y=22​3y=22\sqrt{3} 8. 11​211\sqrt{2} 9. 6565 10. 2424 11. 1010 12. w=6w=6, R​S¯=13\overline{RS}=13 |

Figure 13: Example of MiMo-VL-7B-RL solving multiple geometry problems.
