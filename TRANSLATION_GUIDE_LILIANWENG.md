# 翻译规范（Lilian Weng 博客中文化）

本文件是翁荔博客翻译项目的统一规范，所有翻译批次开始前先读完。通用原则与 [TRANSLATION_GUIDE.md](TRANSLATION_GUIDE.md)（Raschka 项目）一致，本文件补充本项目特有的约定与术语表。

## 项目信息

- 英文存档：`lilianweng-articles/posts/<slug>.md`（52 篇）+ `lilianweng-articles/faq.md`
- 输出目录：`lilianweng-articles-zh/posts/<slug>.md`（与源文件同名镜像）
- 进度索引：`lilianweng-articles-zh/README.md`（每完成一篇更新）

## 输出文件头格式

```markdown
---
title: "中文标题"
title_en: "Original English Title"
source: <原文件 source URL，保持不变>
crawled: 2026-09-08
translated: <完成日期 YYYY-MM-DD>
---

# 中文标题

> 原文：[Original English Title](source URL) · Lilian Weng（翁荔）

（正文译文……）
```

## 翻译原则（在通用规范基础上补充）

1. **全文翻译，不得缩写或跳过**：包括开头的 `[Updated on ...]` 更新说明（译为「[更新于 ……]」，其中日期保留）、文末 Citation（BibTeX）代码块之前的 "Citation" 引言行、References 参考文献列表。
2. **BibTeX 引用块原样保留**（``` 包裹的 `@article{weng20xx...}` 代码块不翻译）。
3. **数学公式一律原样保留**：`$...$` 与 `$$...$$` 中的 LaTeX 一个字符都不改（包括 `\text{}` 内的英文说明文字——若要翻译 `\text{...}` 内的说明，只在确定不破坏渲染语义时进行；默认保留原文）。
4. **代码块原样保留**，代码内英文注释也保留。
5. **图片链接 URL 原样保留**，caption（图注、`*斜体 caption*`、`Fig. 1.` 行）翻译。
6. **脚注**：`[^1]` 引用标记位置保持，`[^1]: ...` 定义翻译。
7. **表格**：表头与单元格翻译；符号单元格（如 `$N$`、`—`）保留。
8. **人名处理**：以「外文姓（中文译名）」或直接保留外文姓，全文统一。常见人名：Lilian Weng（翁荔）、Geoffrey Hinton、Yoshua Bengio、Yann LeCun（杨立昆）、Richard Sutton、Jürgen Schmidhuber 等；论文作者引用格式（如 "Jacot et al. 2018"）中的姓不译。
9. **模型/系统/数据集名不翻译**：GPT、BERT、CLIP、ImageNet、Atari、MuJoCo、DQN、A3C、PPO、SAC 等。
10. **提示词模板**（如 HuggingGPT 的 `{{ Available Task List }}` 模板正文）保留英文原文，可加中文引导句。
11. 站内链接（`https://lilianweng.github.io/posts/...`）URL 不动，链接文字翻译。

## 术语表（全文统一）

### 通用深度学习

| English | 中文 |
|---|---|
| representation learning | 表征学习 |
| self-supervised learning | 自监督学习 |
| semi-supervised learning | 半监督学习 |
| contrastive learning | 对比学习 |
| active learning | 主动学习 |
| curriculum learning | 课程学习 |
| meta-learning | 元学习 |
| neural architecture search (NAS) | 神经架构搜索（NAS） |
| knowledge distillation | 知识蒸馏 |
| overfitting / generalization | 过拟合 / 泛化 |
| inductive bias | 归纳偏置 |
| embedding | 嵌入 |
| fine-tune / pretrain | 微调 / 预训练 |
| multimodal | 多模态 |
| hallucination | 幻觉 |
| scaling law | 标度律（scaling law） |
| emergent ability | 涌现能力 |

### 生成模型

| English | 中文 |
|---|---|
| generative model | 生成模型 |
| likelihood | 似然 |
| (log-)likelihood | （对数）似然 |
| evidence / marginal likelihood | 证据 / 边际似然 |
| ELBO (evidence lower bound) | 证据下界（ELBO） |
| variational inference | 变分推断 |
| posterior / prior | 后验 / 先验 |
| reparameterization trick | 重参数化技巧 |
| normalizing flow | 归一化流 |
| invertible / reversible | 可逆 |
| diffusion model | 扩散模型 |
| forward / reverse process | 前向 / 反向过程 |
| noise schedule | 噪声调度 |
| score function | 分数函数 |
| denoising | 去噪 |
| mode collapse | 模式坍塌 |
| vanilla | 朴素（如 vanilla GAN → 朴素 GAN） |
| WGAN (Wasserstein GAN) | WGAN（不译） |
| Lipschitz continuity | Lipschitz 连续性（利普希茨连续性） |
| Earth-Mover / Wasserstein distance | 推土机距离 / Wasserstein 距离 |
| VQ-VAE / PixelCNN / MADE | 不译 |
| latent variable | 潜变量 |
| tractable / intractable | 可解 / 不可解（tractable→可解析处理） |

### 强化学习

| English | 中文 |
|---|---|
| agent / environment | 智能体 / 环境 |
| policy | 策略 |
| reward | 奖励 |
| return | 回报 |
| value function / state-value / action-value | 价值函数 / 状态价值 / 动作价值 |
| Q-learning / Q function | Q-learning（不译）/ Q 函数 |
| Bellman equation | Bellman 方程（贝尔曼方程） |
| Markov decision process (MDP) | 马尔可夫决策过程（MDP） |
| Markov chain | 马尔可夫链 |
| discount factor | 折扣因子 |
| exploration / exploitation | 探索 / 利用 |
| multi-armed bandit | 多臂老虎机 |
| regret | 遗憾（regret，bandit 语境） |
| policy gradient | 策略梯度 |
| actor-critic | actor-critic（不译，或 演员-评论家） |
| on-policy / off-policy | 同策略 / 离策略（on-policy/off-policy） |
| model-based / model-free | 基于模型 / 无模型 |
| replay buffer / experience replay | 经验回放缓冲区 / 经验回放 |
| deterministic policy | 确定性策略 |
| entropy regularization | 熵正则化 |
| advantage function | 优势函数 |
| trust region / TRPO / PPO | 信赖域 / TRPO（不译）/ PPO（不译） |
| curriculum for RL | 强化学习中的课程（学习） |
| reward hacking | 奖励作弊（reward hacking） |
| reward model | 奖励模型 |
| RLHF (RL from human feedback) | 基于人类反馈的强化学习（RLHF） |
| evolution strategies (ES) | 进化策略（ES） |
| genetic algorithm | 遗传算法 |
| simulated annealing | 模拟退火 |
| CMA-ES | CMA-ES（不译） |
| sim2real | sim2real（仿真到现实，不译） |
| domain randomization | 域随机化 |
| meta-RL | 元强化学习 |
| exploration strategy | 探索策略 |
| intrinsic reward / motivation | 内在奖励 / 内在动机 |
| curiosity | 好奇心 |
| count-based exploration | 基于计数的探索 |
| episodic memory | 情景记忆 |

### NLP / LLM

| English | 中文 |
|---|---|
| language model (LM) | 语言模型 |
| autoregressive | 自回归 |
| masked language model | 掩码语言模型 |
| token / tokenizer | token（不译）/ 分词器 |
| prompt / prompt engineering | 提示 / 提示工程 |
| in-context learning | 上下文学习（in-context learning） |
| zero-shot / few-shot | 零样本 / 少样本 |
| chain-of-thought (CoT) | 思维链（CoT） |
| instruction tuning | 指令微调 |
| alignment | 对齐 |
| steerability / controllable generation | 可操控性 / 可控生成 |
| toxicity | 毒性 |
| decoding strategy | 解码策略 |
| beam search | 束搜索 |
| sampling temperature | 采样温度 |
| nucleus sampling (top-p) | 核采样（top-p） |
| retrieval / retriever | 检索 / 检索器 |
| open-domain question answering (ODQA) | 开放域问答（ODQA） |
| reader | 阅读器（ODQA 语境） |
| hallucination (extrinsic) | （事实性/外在）幻觉 |
| adversarial attack | 对抗攻击 |
| jailbreak | 越狱（jailbreak） |
| prompt injection | 提示注入 |
| fine-tuning attack / backdoor | 微调攻击 / 后门 |
| benchmark | 基准测试 |
| inference optimization | 推理优化 |
| quantization | 量化 |
| KV cache | KV 缓存 |
| speculative decoding | 投机解码 |
| mixture-of-experts (MoE) | 专家混合（MoE） |
| long context | 长上下文 |
| agent / LLM agent | 智能体 / LLM 智能体 |
| tool use | 工具使用 |
| planning / subgoal decomposition | 规划 / 子目标分解 |
| reflection | 反思 |
| short-term / long-term memory | 短期 / 长期记忆 |
| task decomposition | 任务分解 |
| ReAct | ReAct（不译） |
| self-refine / self-criticism | 自我改进 / 自我批评 |
| reward hacking | 奖励作弊 |
| recursive self-improvement (RSI) | 递归自我改进（RSI） |
| harness | 执行框架（harness） |
| test-time / inference-time compute | 测试时 / 推理时计算 |
| reasoning | 推理 |
| human data / human feedback | 人类数据 / 人类反馈 |
| data quality / label quality | 数据质量 / 标注质量 |
| inter-annotator agreement | 标注者间一致性 |

### 数学与优化

| English | 中文 |
|---|---|
| objective function | 目标函数 |
| loss | 损失 |
| gradient descent / stochastic | 梯度下降 / 随机（梯度下降） |
| backpropagation | 反向传播 |
| convex / non-convex | 凸 / 非凸 |
| stationary point | 驻点 |
| saddle point | 鞍点 |
| Taylor expansion | 泰勒展开 |
| central limit theorem | 中心极限定理 |
| Gaussian process | 高斯过程 |
| kernel (method) | 核（方法） |
| neural tangent kernel (NTK) | 神经正切核（NTK） |
| Jacobian / Hessian | 雅可比矩阵 / 海森矩阵 |
| distribution (probability) | 分布 |
| stochastic differential equation | 随机微分方程 |
| ordinary differential equation (ODE) | 常微分方程（ODE） |
| score matching | 分数匹配 |
| maximum likelihood estimation | 极大似然估计 |
| cross-entropy | 交叉熵 |
| bias-variance tradeoff | 偏差-方差权衡 |

### 计算机视觉

| English | 中文 |
|---|---|
| object detection | 目标检测 |
| bounding box | 边界框 |
| region proposal | 候选区域 |
| selective search | 选择性搜索 |
| non-max suppression (NMS) | 非极大值抑制（NMS） |
| feature pyramid | 特征金字塔 |
| anchor | 锚框 |
| segmentation | 分割 |
| gradient vector / histogram (HOG) | 梯度向量 / 梯度直方图（HOG） |
| receptive field | 感受野 |
| sliding window | 滑动窗口 |
| IoU (intersection over union) | 交并比（IoU） |
| mAP (mean average precision) | 平均精度均值（mAP） |

其余术语以 [TRANSLATION_GUIDE.md](TRANSLATION_GUIDE.md) 总表为准；两表冲突时以本文件为准。首次出现的重要术语采用「中文（English）」标注。
