# Sebastian Raschka 技术文章中文翻译

> 共 116 篇（博客 80 + LLM 架构图解 31 + 旧技术专栏 5），全文翻译；2026-09-06 完成首批 110 篇，此后每日同步补译。
> 英文原文存档见 [sebastianraschka-articles/](../sebastianraschka-articles/)；翻译规范见 [TRANSLATION_GUIDE.md](../TRANSLATION_GUIDE.md)。
> 每篇头部含英文原标题与原文链接；代码块、图片链接、公式原样保留。

## LLM 架构图解（31 篇）

- [Artificial Analysis 智能指数（Intelligence Index）](llm-architecture-gallery/aa-intelligence-index.md)
- [LLM 架构画廊 - 激活参数百分比](llm-architecture-gallery/active-parameter-ratio.md)
- [逐层注意力预算](llm-architecture-gallery/attention-budgeting.md)
- [LLM 架构画廊 - 注意力机制分布](llm-architecture-gallery/attention-mechanism-distribution.md)
- [注意力残差（AttnRes）](llm-architecture-gallery/attention-residuals.md)
- [LLM 架构画廊更新日志](llm-architecture-gallery/changelog.md)
- [压缩卷积注意力](llm-architecture-gallery/compressed-convolutional-attention.md)
- [CSA 与 HCA](llm-architecture-gallery/csa-hca.md)
- [DeepSeek 稀疏注意力（DSA）](llm-architecture-gallery/deepseek-sparse-attention.md)
- [门控注意力（Gated Attention）](llm-architecture-gallery/gated-attention.md)
- [门控残差（GR）](llm-architecture-gallery/gated-residuals.md)
- [分组查询注意力（GQA）](llm-architecture-gallery/gqa.md)
- [混合注意力](llm-architecture-gallery/hybrid-attention.md)
- [IndexShare](llm-architecture-gallery/indexshare.md)
- [每 token KV 缓存（bf16）](llm-architecture-gallery/kv-cache-calculations.md)
- [跨层 KV 共享](llm-architecture-gallery/kv-sharing.md)
- [潜在 MoE](llm-architecture-gallery/latent-moe.md)
- [循环 Transformer（Looped Transformer）](llm-architecture-gallery/looped-depth-sharing.md)
- [LLM 内存计算器](llm-architecture-gallery/memory-calculator.md)
- [多头注意力（MHA）](llm-architecture-gallery/mha.md)
- [流形约束超连接](llm-architecture-gallery/mhc.md)
- [多头潜在注意力（MLA）](llm-architecture-gallery/mla.md)
- [专家混合（MoE）](llm-architecture-gallery/moe.md)
- [多 token 预测（MTP）](llm-architecture-gallery/mtp.md)
- [无位置嵌入（NoPE）](llm-architecture-gallery/nope.md)
- [逐层嵌入（PLE）](llm-architecture-gallery/per-layer-embeddings.md)
- [PolyNorm](llm-architecture-gallery/polynorm.md)
- [QK-Norm](llm-architecture-gallery/qk-norm.md)
- [Qwen 稀疏注意力](llm-architecture-gallery/qwen-sparse-attention.md)
- [短卷积（ShortConv）](llm-architecture-gallery/shortconv.md)
- [滑动窗口注意力（SWA）](llm-architecture-gallery/swa.md)

## Ahead of AI 专栏（Magazine，1 篇）

Substack 专栏译文，按发布年份存放；后续更新继续追加。

- [GPT-6 Astra、循环 Transformer 与隐藏推理](magazine/2026/gpt-6-astra-looped-transformers-and.md)

## 博客文章（79 篇）

### 2014（1 篇）

- [MusicMood](blog/2014/musicmood.md)

### 2015（2 篇）

- [Python、机器学习与语言之战](blog/2015/why-python.md)
- [《Python Machine Learning》写作记](blog/2015/writing-pymle.md)

### 2016（3 篇）

- [机器学习模型评估：第一部分](blog/2016/model-evaluation-selection-part1.md)
- [机器学习模型评估：第 2 部分](blog/2016/model-evaluation-selection-part2.md)
- [机器学习模型评估：第三部分](blog/2016/model-evaluation-selection-part3.md)

### 2018（2 篇）

- [机器学习模型评估：第 4 部分](blog/2018/model-evaluation-selection-part4.md)
- [面向人脸图像的半对抗网络](blog/2018/semi-adversarial-nets-1.md)

### 2019（2 篇）

- [UW-Madison 学生项目展示](blog/2019/student-gallery-1.md)
- [第三版有什么新内容](blog/2019/whats-new-in-the-3rd-edition.md)

### 2020（4 篇）

- [《Architects of Intelligence》书评](blog/2020/book-review-1-architects-of-intelligence.md)
- [可解释机器学习](blog/2020/interpretable-ml-1.md)
- [机器学习与深度学习导论](blog/2020/intro-to-dl-ch01.md)
- [NumPy 与 Matplotlib 入门](blog/2020/numpy-intro.md)

### 2021（5 篇）

- [深度学习导论](blog/2021/dl-course.md)
- [机器学习视频课程](blog/2021/ml-course.md)
- [机器学习与深度学习数据集](blog/2021/ml-dl-datasets.md)
- [我如何保持项目井井有条](blog/2021/project-management.md)
- [《Deep Learning with PyTorch》书评](blog/2021/pytorch-deeplearning-review.md)

### 2022（11 篇）

- [Ahead of AI 创刊，接下来要做什么？](blog/2022/ahead-of-ai-and-whats-next.md)
- [Batch Size 取 2 的幂的迷思](blog/2022/batch-size-2.md)
- [机器学习分类器的置信区间](blog/2022/confidence-intervals-for-ml.md)
- [PyTorch DataPipes 与 DataLoader](blog/2022/datapipes.md)
- [表格数据的深度学习](blog/2022/deep-learning-for-tabular-data.md)
- [构建超分辨率 GAN](blog/2022/lightning-app-srgan-1.md)
- [深度学习模型服务化：Lightning + 云](blog/2022/lightning-app-srgan-2.md)
- [损失函数学习笔记](blog/2022/losses-learned-part1.md)
- [PyTorch 与 Scikit-Learn 新书发布](blog/2022/ml-pytorch-book.md)
- [在 M1 GPU 上运行 PyTorch](blog/2022/pytorch-m1-gpu.md)
- [TorchMetrics](blog/2022/torchmetrics.md)

### 2023（16 篇）

- [寻找准确的 AI 信息](blog/2023/chatgpt-dilemma.md)
- [PyTorch 图像数据增强方法](blog/2023/data-augmentation-pytorch.md)
- [检测 LLM 生成的内容](blog/2023/detect-ai.md)
- [使用 LoRA 对 Falcon LLM 进行微调](blog/2023/falcon-finetuning.md)
- [如何跟上 AI 研究与新闻的步伐](blog/2023/keeping-up-with-ai.md)
- [参数高效的 LLM 微调](blog/2023/llm-finetuning-llama-adapter.md)
- [使用 LoRA 微调大语言模型](blog/2023/llm-finetuning-lora.md)
- [大语言模型的混合精度技术](blog/2023/llm-mixed-precision-copy.md)
- [大语言模型阅读清单](blog/2023/llm-reading-list.md)
- [LLM Efficiency Challenge 2023 参赛指南](blog/2023/neurips2023-starter-guide.md)
- [2022 年机器学习与 AI 开源项目亮点](blog/2023/open-source-highlights-2022.md)
- [从数据集视角看大语言模型](blog/2023/optimizing-LLMs-dataset-perspective.md)
- [PyTorch 训练提速技巧](blog/2023/pytorch-faster.md)
- [PyTorch 大语言模型显存优化](blog/2023/pytorch-memory-optimization.md)
- [从零实现自注意力](blog/2023/self-attention-from-scratch.md)
- [在云端 GPU 上训练 XGBoost](blog/2023/xgboost-gpu.md)

### 2025（4 篇）

- [从零实现 BPE 分词器](blog/2025/bpe-from-scratch.md)
- [DGX Spark 本地 PyTorch 使用体验](blog/2025/dgx-impressions.md)
- [机器学习/AI 的 Hello World：从随机森林到 RLVR](blog/2025/hello-world-ai.md)
- [如何从技术书中获得最大收益](blog/2025/reading-books.md)

### 2026（30 篇）

- [20 万订阅者](blog/2026/ahead-of-ai-reached-200000-subscribers.md)
- [《AI Reasoning Models》课程上线](blog/2026/ai-reasoning-models-course.md)
- [《Build a Reasoning Model (From Scratch)》正式出版](blog/2026/build-a-reasoning-model-from-scratch-is-out.md)
- [《从零构建推理模型》现已登陆 Amazon](blog/2026/build-a-reasoning-model-from-scratch-on-amazon.md)
- [Claude 文本水印的工作原理](blog/2026/claude-text-watermarking.md)
- [从零实现 DeepSeek 稀疏注意力](blog/2026/deepseek-sparse-attention-from-scratch.md)
- [Gemma 4 架构与基准测试笔记](blog/2026/gemma-4-release-notes.md)
- [GLM-5.2 IndexShare 架构笔记](blog/2026/glm-5-2-indexshare.md)
- [GLM-5.3-Flash 架构笔记](blog/2026/glm-5-3-flash-architecture-notes.md)
- [GPT 5.6 的配置与默认选择](blog/2026/gpt-5-6-configurations.md)
- [Inkling 架构与基准测试笔记](blog/2026/inkling-architecture-benchmark-notes.md)
- [Kimi K3 架构笔记](blog/2026/kimi-k3-architecture-notes.md)
- [LLM Architecture Gallery 差异对比工具](blog/2026/llm-architecture-gallery-diff-tool.md)
- [走进 LLM Architecture Gallery](blog/2026/llm-architecture-gallery.md)
- [从零实现 LLM 架构（演讲）](blog/2026/llm-architectures-from-scratch-talk.md)
- [LLMs From Scratch 突破 100,000 GitHub Stars](blog/2026/llms-from-scratch-reaches-100000-github-stars.md)
- [本地开放权重 LLM 编程执行框架实测笔记](blog/2026/local-open-weight-llms-coding-harnesses.md)
- [MiniMax M2 技术报告笔记](blog/2026/minimax-m2-technical-report.md)
- [Muse Glimmer 30B 架构笔记](blog/2026/muse-glimmer-30b-architecture-notes.md)
- [Nemotron 3 Super 吞吐量笔记](blog/2026/nemotron-3-super-throughput.md)
- [Nemotron 3 Ultra 潜在 MoE 笔记](blog/2026/nemotron-3-ultra-latent-moe.md)
- [North Mini Code 编程智能体笔记](blog/2026/north-mini-code-agentic-coding.md)
- [六个值得关注的开放权重模型架构笔记](blog/2026/notable-open-weight-models-this-week.md)
- [OpenAI Astra 与循环 Transformer](blog/2026/openai-astra-looped-transformers.md)
- [推理模型新书读书会问答活动](blog/2026/reasoning-model-book-club-q-and-a.md)
- [推理模型一书清单 6.5 勘误](blog/2026/reasoning-model-listing-6-5-correction.md)
- [推理模型与代码环境搭建](blog/2026/reasoning-models-and-agents-from-scratch.md)
- [State of AI 2026 访谈](blog/2026/state-of-ai-interview.md)
- [使用本地编程智能体](blog/2026/using-local-coding-agents.md)
- [VibeThinker-3B 后训练笔记](blog/2026/vibethinker-3b-post-training.md)

## 旧技术专栏 articles（5 / 27 篇，持续补译中）

- [特征缩放与归一化](articles/2014_about_feature_scaling.md)
- [朴素贝叶斯与文本分类](articles/2014_naive_bayes_1.md)
- [监督机器学习基础](articles/2014_intro_supervised_learning.md)
- [RBF 核 PCA 与核技巧](articles/2014_kernel_pca.md)
- [主成分分析（PCA）：三步教程](articles/2015_pca_in_3_steps.md)
