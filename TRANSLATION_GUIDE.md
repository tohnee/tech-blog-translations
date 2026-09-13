# 翻译规范（Sebastian Raschka 文章中文化）

本文件是所有翻译批次的统一规范。开始翻译前先读完本文件。

## 输出位置与文件头

- 输出目录：`/Users/tohnee/zcode/优秀文章和教程翻译/sebastianraschka-articles-zh/`
- 输出路径与源文件路径**逐级镜像**：`sebastianraschka-articles/blog/2023/x.md` → `sebastianraschka-articles-zh/blog/2023/x.md`
- 文件头 frontmatter 格式（保留 source 与 title_en，title 换成中文译名）：

```markdown
---
title: "中文标题"
title_en: "Original English Title"
source: <原文件的 source URL，保持不变>
crawled: 2026-09-06
translated: 2026-09-06
---

# 中文标题

> 原文：[Original English Title](source URL)

（正文译文……）
```

## 翻译原则

1. **全文翻译，不得缩写或跳过段落**。引言、脚注、结尾说明都要译。
2. **代码块原样保留**：fenced code block（``` 内）的代码、命令、输出一律不翻译、不改写（包括代码内英文注释——保留原样以免引入错误）。行内代码 `` `x` `` 同样保留。
3. **图片链接保留**：`![alt](url)` 的 URL 原样保留；alt 文本可译可留。图片下方的 caption 如有则翻译。
4. **Markdown 结构保持**：标题层级、列表、表格、引用块、粗斜体位置与原文一一对应。表格内容翻译，表头翻译。
5. **链接文本翻译，URL 不动**。站内相对链接（如 `/glossary/#mha`）原样保留。
6. 语气：技术博客风格，面向中文 AI 研究者/工程师，流畅自然，不要逐词直译腔；专有名词首次出现时可用「中文（English）」格式。

## 术语表（全文统一）

| English | 中文 |
|---|---|
| attention / self-attention | 注意力 / 自注意力 |
| multi-head attention (MHA) | 多头注意力（MHA） |
| grouped-query attention (GQA) | 分组查询注意力（GQA） |
| multi-head latent attention (MLA) | 多头潜在注意力（MLA） |
| sliding-window attention (SWA) | 滑动窗口注意力（SWA） |
| sparse attention | 稀疏注意力 |
| causal attention / causal mask | 因果注意力 / 因果掩码 |
| KV cache | KV 缓存 |
| token / embedding | token（不译）/ 嵌入 |
| vocabulary / tokenizer / BPE | 词表 / 分词器 / 字节对编码（BPE） |
| from scratch | 从零实现 |
| pretraining / finetuning | 预训练 / 微调 |
| instruction-finetuning | 指令微调 |
| mixture-of-experts (MoE) | 专家混合（MoE） |
| expert / routing / router | 专家 / 路由 / 路由器 |
| residual connection | 残差连接 |
| layer normalization / RMSNorm | 层归一化 / RMSNorm（不译） |
| positional embeddings | 位置嵌入 |
| RoPE (rotary position embedding) | 旋转位置嵌入（RoPE） |
| NoPE | NoPE（不译） |
| LoRA / DoRA | LoRA / DoRA（不译） |
| knowledge distillation | 知识蒸馏 |
| reinforcement learning (RL) | 强化学习（RL） |
| RLHF / RLVR | RLHF / RLVR（不译） |
| reasoning model | 推理模型 |
| inference-time scaling | 推理时扩展 |
| chain-of-thought (CoT) | 思维链（CoT） |
| test-time compute | 测试时计算 |
| open-weight model | 开放权重模型 |
| benchmark / leaderboard | 基准测试 / 排行榜 |
| throughput / latency | 吞吐量 / 延迟 |
| gradient accumulation | 梯度累积 |
| mixed precision | 混合精度 |
| learning rate / weight decay | 学习率 / 权重衰减 |
| overfitting / underfitting | 过拟合 / 欠拟合 |
| cross-validation | 交叉验证 |
| feature scaling | 特征缩放 |
| supervised / unsupervised learning | 监督学习 / 无监督学习 |
| deep neural network | 深度神经网络 |
| convolutional | 卷积 |
| kernel / weight | 核 / 权重 |
| logit / softmax | logit（不译）/ softmax（不译） |
| cross-entropy | 交叉熵 |
| loss function | 损失函数 |
| hyperparameter | 超参数 |
| checkpoint | 检查点 |
| context window / context length | 上下文窗口 / 上下文长度 |
| multimodal | 多模态 |
| diffusion model | 扩散模型 |
| agent / coding agent | 智能体 / 编程智能体 |
| harness | 执行框架（harness，首次出现标注英文） |
| gating / gate | 门控 / 门 |
| depth-wise / cross-layer | 逐深度 / 跨层 |
| short convolution (ShortConv) | 短卷积（ShortConv） |
| recurrent depth | 循环深度 |
| latent | 潜在 |
| fact sheet | 规格速览 |

人名、公司名、产品名（Kimi、GLM、DeepSeek、Qwen、Llama、PyTorch、NumPy 等）不翻译。
书名首次出现保留英文原名，可括注中文：《Build a Large Language Model (From Scratch)》（《从零构建大语言模型》）。
