---
title: "LLM 架构画廊更新日志"
title_en: "LLM Architecture Gallery Changelog"
source: https://sebastianraschka.com/llm-architecture-gallery/changelog/
crawled: 2026-09-06
translated: 2026-09-06
---

# LLM 架构画廊更新日志

> 原文：[LLM Architecture Gallery Changelog](https://sebastianraschka.com/llm-architecture-gallery/changelog/)

[返回画廊](https://sebastianraschka.com/llm-architecture-gallery/)
[画廊更新日志 RSS 订阅](https://sebastianraschka.com/llm-architecture-gallery/rss.xml)

## 2026 年 9 月 5 日

**新增交互式模型内存计算器**

使用画廊中的模型数据分别估算权重内存与 KV 缓存内存，并提供上下文长度、批次大小以及权重与缓存各自精度的控制选项。

- [新增内存计算器，支持可分享的设置，并对 MoE、循环与滑动窗口架构给出明确的假设条件。](https://sebastianraschka.com/llm-architecture-gallery/memory-calculator/)
- [将每个模型卡片链接到其预选好的内存估算结果。](https://sebastianraschka.com/llm-architecture-gallery/)

## 2026 年 9 月 4 日

**修复对比链接与键盘导航**

重新加载后 Model B 的选择仍保留其位置；放大查看图片时键盘焦点保持在对话框内；在移动端上过长的公式可在页面内滚动。

- [对比链接中保留空的 Model A 与 Model B 槽位。](https://sebastianraschka.com/llm-architecture-gallery/#architecture-diff-tool)
- [改进放大图片预览中的键盘导航与焦点恢复。](https://sebastianraschka.com/llm-architecture-gallery/)
- [修正标题层级，并让长公式在窄屏上不溢出。](https://sebastianraschka.com/llm-architecture-gallery/gated-attention/)
- [减少首图与海报预览的下载，并将概念引用直接链接到对应的杂志文章。](https://sebastianraschka.com/llm-architecture-gallery/)

## 2026 年 9 月 3 日

**新增 Ouro-Thinking 2.6B**

新增字节跳动 Ouro-Thinking 2.6B 架构卡片，扩充了 Looped Transformer 讲解文章，并刷新了画廊的 KV 缓存与注意力汇总内容。

- [新增字节跳动 Ouro-Thinking 2.6B 架构卡片。](https://sebastianraschka.com/llm-architecture-gallery/#card-ouro-thinking-2-6b)
- [扩充 Looped Transformer 讲解文章，加入 Ouro 的四次执行、可学习的退出门、相关架构以及 KV 缓存行为。](https://sebastianraschka.com/llm-architecture-gallery/looped-depth-sharing/)

## 2026 年 9 月 2 日

**改进画廊主题控件与深色模式图形**

新增画廊主题选择器，并改进了架构卡片、模型对比与放大视图在深色模式下的渲染效果。

- [新增紧凑的浅色/深色选择器](https://sebastianraschka.com/llm-architecture-gallery/#architecture-gallery)
- [深色模式下反转架构图形的颜色，同时保持摄影类图片不变。](https://sebastianraschka.com/llm-architecture-gallery/)

## 2026 年 8 月 29 日

**新增 Qwen3.8-Flash-Next 与 Tencent Hy4-preview 架构**

新增 Qwen3.8-Flash-Next 与 Tencent Hy4-preview 架构卡片，以及 Qwen Sparse Attention 与 Gated Residuals 讲解文章，并刷新了画廊汇总表格。

- [新增 Qwen3.8-Flash-Next 125B-A6B 架构卡片。](https://sebastianraschka.com/llm-architecture-gallery/#card-qwen3-8-flash-next-125b-a6b)
- [新增 Tencent Hy4-preview 770B-A49B 架构卡片。](https://sebastianraschka.com/llm-architecture-gallery/#card-tencent-hy4-preview-770b-a49b)
- [新增 Qwen Sparse Attention 讲解文章，涵盖微块选择机制及其与 DeepSeek Sparse Attention 的区别。](https://sebastianraschka.com/llm-architecture-gallery/qwen-sparse-attention/)
- [新增 Gated Residuals 讲解文章，涵盖 GR Read、GR Write 及其与 mHC 的区别。](https://sebastianraschka.com/llm-architecture-gallery/gated-residuals/)

## 2026 年 8 月 27 日

**新增公司元数据、排序与画廊筛选**

为每个架构卡片添加公司信息，引入按发布日期、总参数量、架构家族与公司的筛选功能，并让画廊目录按字母顺序排列。

- [在每个模型卡片标题旁标注所属公司。](https://sebastianraschka.com/llm-architecture-gallery/)
- [在画廊控件中新增公司排序与公司名称搜索。](https://sebastianraschka.com/llm-architecture-gallery/#architecture-gallery)
- [在画廊控件中新增发布日期、总参数量、架构家族与公司筛选。](https://sebastianraschka.com/llm-architecture-gallery/#architecture-gallery)
- [画廊目录保持按字母顺序排列，不受所选卡片排序方式影响。](https://sebastianraschka.com/llm-architecture-gallery/#architecture-gallery)

## 2026 年 8 月 26 日

**新增 GLM-5.3-Flash 并更新海报下载**

新增 Z.ai GLM-5.3-Flash 架构卡片，刷新画廊汇总表格，并更新了海报下载信息。

- [新增 Z.ai GLM-5.3-Flash 架构卡片。](https://sebastianraschka.com/llm-architecture-gallery/#card-glm-5-3-flash)
- 更新支持专区，提供可直接打印的数字版下载，不再列出实体海报。

## 2026 年 8 月 24 日

**新增 Ornith 1.5**

新增 Ornith 1.5 35B-A3B 架构卡片，并刷新画廊汇总表格。

- [新增 Ornith 1.5 35B-A3B 架构卡片。](https://sebastianraschka.com/llm-architecture-gallery/#card-ornith-1-5-35b-a3b)

## 2026 年 8 月 23 日

**新增 Ling 3.0 Flash**

新增 InclusionAI Ling 3.0 Flash 架构卡片，并刷新画廊汇总表格。

- [新增 Ling 3.0 Flash 架构卡片。](https://sebastianraschka.com/llm-architecture-gallery/#card-ling-3-0-flash)

## 2026 年 8 月 15 日

**新增 Qwen3.8 27B**

新增 Qwen3.8 27B 架构卡片，并刷新注意力机制分布表。

- [新增 Qwen3.8 27B 架构卡片。](https://sebastianraschka.com/llm-architecture-gallery/#card-qwen3-8-27b)

## 2026 年 8 月 11 日

**新增 Nemotron 3.5 Lightning**

新增 NVIDIA Nemotron 3.5 Lightning 30B-A3B 架构卡片，并刷新画廊汇总表格。

- [新增 NVIDIA Nemotron 3.5 Lightning 30B-A3B 架构卡片。](https://sebastianraschka.com/llm-architecture-gallery/#card-nemotron-3-5-lightning-30b-a3b)

## 2026 年 8 月 10 日

**新增 Muse Glimmer 30B**

新增 Meta Muse Glimmer 30B 架构卡片，并刷新注意力机制分布表。

- [新增 Muse Glimmer 30B 架构卡片。](https://sebastianraschka.com/llm-architecture-gallery/#card-muse-glimmer-30b)

## 2026 年 7 月 27 日

**新增 Kimi K3**

新增 Moonshot AI Kimi K3 架构卡片，并刷新画廊汇总表格。

- [新增 Kimi K3 架构卡片。](https://sebastianraschka.com/llm-architecture-gallery/#card-kimi-k3)

## 2026 年 7 月 25 日

**重大更新：新增 Antares 1B、BTL-3、Laguna 2.1 模型、Motif 3 Beta、Nanbeige 4.2、Solar Open 2 与多篇讲解文章**

新增 Antares 1B、BTL-3、Laguna S 2.1、Laguna XS 2.1、Motif 3 Beta、Nanbeige 4.2 与 Solar Open 2 的架构卡片，以及 ShortConv、Looped Transformers、IndexShare 与 PolyNorm 的讲解文章。

- 新增 [Antares-1B](https://sebastianraschka.com/llm-architecture-gallery/#card-antares-1b)、[BTL-3 27B](https://sebastianraschka.com/llm-architecture-gallery/#card-btl-3-27b)、[Laguna S 2.1](https://sebastianraschka.com/llm-architecture-gallery/#card-laguna-s-2-1)、[Laguna XS 2.1](https://sebastianraschka.com/llm-architecture-gallery/#card-laguna-xs-2-1)、[Motif 3 Beta](https://sebastianraschka.com/llm-architecture-gallery/#card-motif-3-beta)、[Nanbeige 4.2 3B](https://sebastianraschka.com/llm-architecture-gallery/#card-nanbeige-4-2-3b) 与 [Solar Open 2](https://sebastianraschka.com/llm-architecture-gallery/#card-solar-open-2) 架构卡片。
- [新增 ShortConv 教程。](https://sebastianraschka.com/llm-architecture-gallery/shortconv/)
- [新增简短的 Looped Transformer 讲解文章。](https://sebastianraschka.com/llm-architecture-gallery/looped-depth-sharing/)

## 2026 年 7 月 16 日

**新增 Soofi S**

新增 Soofi S 30B-A3B 架构卡片。

- [新增 Soofi S 30B-A3B 架构卡片。](https://sebastianraschka.com/llm-architecture-gallery/#card-soofi-s-30b-a3b)

## 2026 年 7 月 15 日

**新增 Inkling**

新增 Thinking Machines Lab Inkling 975B 架构卡片。

- [新增 Thinking Machines Lab Inkling 975B 架构卡片。](https://sebastianraschka.com/llm-architecture-gallery/#card-inkling)

## 2026 年 6 月 18 日

**新增 GLM-5.2 并刷新 AA 数据**

新增 Z.ai GLM-5.2 架构卡片，并刷新 Artificial Analysis Intelligence Index 数据。

- [新增 Z.ai GLM-5.2 架构卡片。](https://sebastianraschka.com/llm-architecture-gallery/#card-glm-5-2)
- [为近期相关卡片新增 Artificial Analysis 链接，并刷新 AA Intelligence Index 数值。](https://sebastianraschka.com/llm-architecture-gallery/aa-intelligence-index/)

## 2026 年 6 月 16 日

**新增 VibeThinker-3B**

向画廊新增 WeiboAI VibeThinker-3B 架构卡片。

- [新增 WeiboAI VibeThinker-3B 架构卡片。](https://sebastianraschka.com/llm-architecture-gallery/#card-vibethinker-3b)

## 2026 年 6 月 13 日

**新增 Kimi K2.7 Code 与 MiniMax M3**

新增 Moonshot AI Kimi K2.7 Code 与 MiniMax M3 428B 架构卡片。

- [新增 Moonshot AI Kimi K2.7 Code 架构卡片。](https://sebastianraschka.com/llm-architecture-gallery/#card-kimi-k2-7-code)
- [新增 MiniMax M3 428B 架构卡片。](https://sebastianraschka.com/llm-architecture-gallery/#card-minimax-m3-428b)

## 2026 年 6 月 9 日

**新增 North Mini Code**

新增 Cohere North Mini Code 30B-A3B 架构卡片，并刷新画廊汇总表格。

- [新增 Cohere North Mini Code 30B-A3B 架构卡片。](https://sebastianraschka.com/llm-architecture-gallery/#card-north-mini-code-30b-a3b)

## 2026 年 6 月 4 日

**新增 Nemotron 3 Ultra**

新增 NVIDIA Nemotron 3 Ultra 550B-A55B 架构卡片，并刷新画廊汇总表格。

- [新增 NVIDIA Nemotron 3 Ultra 550B-A55B 架构卡片。](https://sebastianraschka.com/llm-architecture-gallery/#card-nemotron-3-ultra-550b-a55b)

## 2026 年 6 月 3 日

**新增 Gemma 4、Mellum2 与 LFM2.5 模型**

新增 Gemma 4 12B、JetBrains Mellum2 Thinking 12B-A2.5B 与 Liquid AI LFM2.5 架构卡片，并刷新画廊汇总表格。

- [新增 Gemma 4 12B Unified 架构卡片。](https://sebastianraschka.com/llm-architecture-gallery/#card-gemma-4-12b)
- [新增 JetBrains Mellum2 Thinking 12B-A2.5B 架构卡片。](https://sebastianraschka.com/llm-architecture-gallery/#card-jetbrains-mellum2-thinking-12b-a2-5b)
- [新增 Liquid AI LFM2.5 350M 架构卡片。](https://sebastianraschka.com/llm-architecture-gallery/#card-lfm2-5-350m)
- [新增 Liquid AI LFM2.5 1.2B 架构卡片。](https://sebastianraschka.com/llm-architecture-gallery/#card-lfm2-5-1-2b)
- [新增 Liquid AI LFM2.5 8B-A1B 架构卡片。](https://sebastianraschka.com/llm-architecture-gallery/#card-lfm2-5-8b-a1b)

## 2026 年 5 月 27 日

**关联 MiniMax M2 系列与 Laguna 技术报告**

为画廊中 MiniMax M2、M2.5、M2.7 与 Laguna XS.2 卡片添加技术报告链接。

- [在 MiniMax M2、M2.5 与 M2.7 卡片中添加 MiniMax-M2 系列技术报告链接。](https://sebastianraschka.com/llm-architecture-gallery/#card-minimax-m2-230b)
- [在 Laguna XS.2 卡片中添加 Laguna XS.2 技术报告链接。](https://sebastianraschka.com/llm-architecture-gallery/#card-laguna-xs-2)

## 2026 年 5 月 21 日

**修正 OLMo 2 架构图**

更新 OLMo 2 7B 画廊图形，更准确地展示注意力之后与前馈之后的 RMSNorm 位置。

- [替换 OLMo 2 7B 架构图并重新生成其画廊缩略图。](https://sebastianraschka.com/llm-architecture-gallery/#card-olmo-2-7b)

## 2026 年 5 月 20 日

**新增 Command A+**

新增 Cohere Command A+ 218B-A25B 架构卡片，并刷新激活参数占比与注意力机制分布表。

- [新增 Cohere Command A+ 218B-A25B 架构卡片。](https://sebastianraschka.com/llm-architecture-gallery/#card-command-a-218b-a25b)

## 2026 年 5 月 17 日

**新增 Gemma 4、Laguna、ZAYA1 与 DeepSeek V4 讲解文章**

为 Gemma 4 E2B 与 E4B 新增跨层 KV 共享与逐层嵌入讲解文章；新增 Laguna 注意力预算、ZAYA1 压缩卷积注意力以及 DeepSeek V4 mHC 与 CSA/HCA 讲解文章；并将近期架构卡片链接到 5 月 16 日的文章章节。

- 新增以下讲解文章：[跨层 KV 共享](https://sebastianraschka.com/llm-architecture-gallery/kv-sharing/)、[逐层嵌入](https://sebastianraschka.com/llm-architecture-gallery/per-layer-embeddings/)、[Laguna XS.2 注意力预算](https://sebastianraschka.com/llm-architecture-gallery/attention-budgeting/)、[ZAYA1-8B 压缩卷积注意力](https://sebastianraschka.com/llm-architecture-gallery/compressed-convolutional-attention/)、[DeepSeek V4 流形约束超连接](https://sebastianraschka.com/llm-architecture-gallery/mhc/) 与 [DeepSeek V4 CSA/HCA 压缩注意力](https://sebastianraschka.com/llm-architecture-gallery/csa-hca/)。
- [为 Gemma 4 E2B、Gemma 4 E4B、Laguna XS.2、ZAYA1-8B 与 DeepSeek V4 添加“查看文中章节”链接。](https://sebastianraschka.com/llm-architecture-gallery/#card-gemma-4-e2b)

## 2026 年 5 月 14 日

**新增 Xiaomi MiMo-V2.5-Pro**

新增 Xiaomi MiMo-V2.5-Pro 1.02T 架构卡片（并更新激活参数占比与注意力机制分布表）。

- [新增 Xiaomi MiMo-V2.5-Pro 1.02T 架构卡片（并更新激活参数占比与注意力机制分布表）。](https://sebastianraschka.com/llm-architecture-gallery/#card-xiaomi-mimo-v2-5-pro-1-02t)

## 2026 年 5 月 14 日

**新增激活参数占比元分析**

在架构卡片下方新增元分析区块，并链接到激活参数占比与注意力机制分布的独立表格。

- [新增面向稀疏 MoE 与混合模型的独立激活参数占比表。](https://sebastianraschka.com/llm-architecture-gallery/active-parameter-ratio/)
- [新增面向画廊可见卡片的独立注意力机制分布表。](https://sebastianraschka.com/llm-architecture-gallery/attention-mechanism-distribution/)

## 2026 年 5 月 12 日

**更新画廊元数据与性能**

恢复了缺失的架构卡片，修正画廊元数据，并通过生成缩略图、离屏渲染提示与更低开销的吸附控件降低卡片渲染成本。

- [从 GPT-2 XL 卡片中移除错误的 Gemma 4 Artificial Analysis 分数与来源链接。](https://sebastianraschka.com/llm-architecture-gallery/#card-gpt-2-xl-1-5b)
- [在 Arcee AI Trinity Large 卡片中添加有据可查的 Trinity Large Thinking Artificial Analysis 分数。](https://sebastianraschka.com/llm-architecture-gallery/#card-arcee-ai-trinity-large-400b)
- [修正 Qwen3.5 来源章节的锚文本与 URL。](https://sebastianraschka.com/llm-architecture-gallery/#card-qwen3-5-397b)
- [补齐缺失的 Llama 3.2 3B、Qwen3 0.6B 与 Qwen3 30B-A3B 图形卡片。](https://sebastianraschka.com/llm-architecture-gallery/#card-llama-3-2-3b)
- [为架构卡片添加较小的生成缩略图，同时保留全尺寸图片供放大查看。](https://sebastianraschka.com/llm-architecture-gallery/)
- [为画廊卡片添加离屏渲染提示。](https://sebastianraschka.com/llm-architecture-gallery/)
- [移除吸附式搜索与排序控件的背景模糊，以减少滚动开销。](https://sebastianraschka.com/llm-architecture-gallery/)

## 2026 年 5 月 10 日

**新增 5 月 10 日架构画廊更新**

向公开架构画廊新增 ZAYA1-8B 与 LongCat-Flash-Lite 68.5B-A3B。

- [新增 ZAYA1-8B 架构卡片。](https://sebastianraschka.com/llm-architecture-gallery/#card-zaya1-8b)
- [新增 LongCat-Flash-Lite 68.5B-A3B 架构卡片。](https://sebastianraschka.com/llm-architecture-gallery/#card-longcat-flash-lite-68-5b-a3b)
- 明确说明画廊聚焦纯文本 LLM 与语言模型骨干网络。

## 2026 年 5 月 3 日

**新增 5 月 3 日架构画廊更新**

向公开架构画廊新增 Laguna XS.2、Tencent Hy3-preview 295B-A21B、Granite 4.1 30B 以及 Multi-Token Prediction 讲解文章。

- [新增 Laguna XS.2 架构卡片。](https://sebastianraschka.com/llm-architecture-gallery/#card-laguna-xs-2)
- [新增 Tencent Hy3-preview 架构卡片。](https://sebastianraschka.com/llm-architecture-gallery/#card-tencent-hy3-preview-295b-a21b)
- [新增 Granite 4.1 30B 架构卡片。](https://sebastianraschka.com/llm-architecture-gallery/#card-granite-4-1-30b)
- [新增 Multi-Token Prediction 讲解文章。](https://sebastianraschka.com/llm-architecture-gallery/mtp/)

## 2026 年 5 月 1 日

**新增 5 月架构画廊更新**

向公开架构画廊新增 Xiaomi MiMo-V2.5 310B、MiniMax M2.7 230B 与 Ling 2.6 1T；新增 AA Index 分数排序，并刷新新收录模型的 AA 档案数据。

- [新增 Xiaomi MiMo-V2.5 310B 架构卡片。](https://sebastianraschka.com/llm-architecture-gallery/#card-xiaomi-mimo-v2-5-310b)
- [新增 MiniMax M2.7 230B 架构卡片。](https://sebastianraschka.com/llm-architecture-gallery/#card-minimax-m2-7-230b)
- [新增 Ling 2.6 1T 架构卡片。](https://sebastianraschka.com/llm-architecture-gallery/#card-ling-2-6-1t)
- 新增按 AA Index 分数排序的选项，将带数值 Artificial Analysis 分数的模型排在前面。

## 2026 年 4 月 26 日

**新增 4 月架构卡片**

向公开架构画廊新增 Kimi K2.6、Qwen3.6 35B-A3B、Qwen3.6 27B、DeepSeek V4-Pro 与 DeepSeek V4-Flash。mHC 与压缩注意力的细节将在稍后补充。

- [新增 Kimi K2.6 架构卡片。](https://sebastianraschka.com/llm-architecture-gallery/#card-kimi-k2-6)
- [新增 Qwen3.6 35B-A3B 架构卡片。](https://sebastianraschka.com/llm-architecture-gallery/#card-qwen3-6-35b-a3b)
- [新增 Qwen3.6 27B 架构卡片。](https://sebastianraschka.com/llm-architecture-gallery/#card-qwen3-6-27b)
- [新增 DeepSeek V4-Pro 架构卡片。](https://sebastianraschka.com/llm-architecture-gallery/#card-deepseek-v4-pro)
- [新增 DeepSeek V4-Flash 架构卡片。](https://sebastianraschka.com/llm-architecture-gallery/#card-deepseek-v4-flash)

## 2026 年 4 月 10 日

**从零实现 Gemma 4 E2B 与 E4B**

从零实现了 Gemma 4 E2B 与 E4B（链接见架构卡片）。

- [从零实现 Gemma 4 E2B 与 E4B（链接见架构卡片）。](https://sebastianraschka.com/llm-architecture-gallery/#card-gemma-4-e2b)

## 2026 年 4 月 9 日

**扩充 Gemma 4 画廊覆盖**

新增 Gemma 4 E2B 与 E4B 架构卡片，并补齐较大 Gemma 4 模型与 GLM-5.1 缺失的 AA Intelligence Index 数据。

- [新增 Gemma 4 E2B 架构卡片。](https://sebastianraschka.com/llm-architecture-gallery/#card-gemma-4-e2b)
- [新增 Gemma 4 E4B 架构卡片。](https://sebastianraschka.com/llm-architecture-gallery/#card-gemma-4-e4b)
- [为 Gemma 4 31B 添加 AA Intelligence Index 数据。](https://sebastianraschka.com/llm-architecture-gallery/#card-gemma-4-31b)
- [为 Gemma 4 26B-A4B 添加 AA Intelligence Index 数据。](https://sebastianraschka.com/llm-architecture-gallery/#card-gemma-4-26b-a4b)
- [为 GLM-5.1 添加 AA Intelligence Index 数据。](https://sebastianraschka.com/llm-architecture-gallery/#card-glm-5-1)

## 2026 年 4 月 7 日

**新增 GLM-5.1 架构卡片**

向公开架构画廊新增 GLM-5.1。

- [新增 GLM-5.1 架构卡片。](https://sebastianraschka.com/llm-architecture-gallery/#card-glm-5-1)

## 2026 年 4 月 4 日

**新增 GLM-4.5-Air 与 INTELLECT-3**

为 GLM-4.5-Air 与 INTELLECT-3 新增独立的技术报告卡片。

- [新增 GLM-4.5-Air 架构卡片。](https://sebastianraschka.com/llm-architecture-gallery/#card-glm-4-5-air)
- [新增 INTELLECT-3 架构卡片。](https://sebastianraschka.com/llm-architecture-gallery/#card-intellect-3)

## 2026 年 4 月 2 日

**新增 Gemma 4 架构卡片**

向画廊新增两张 Gemma 4 架构卡片。

- [新增 Gemma 4 31B 架构卡片。](https://sebastianraschka.com/llm-architecture-gallery/#card-gemma-4-31b)
- [新增 Gemma 4 26B-A4B 架构卡片。](https://sebastianraschka.com/llm-architecture-gallery/#card-gemma-4-26b-a4b)

## 2026 年 3 月 29 日

**新增数字版海报购买链接**

在现有 Redbubble 海报商品旁新增 Gumroad 选项。

- 在现有 Redbubble 实体海报选项旁新增 Gumroad 链接，用于购买可直接打印的数字版海报。

## 2026 年 3 月 27 日

**扩充画廊控件与基准测试元数据**

新增 Artificial Analysis Intelligence Index 数据，并提供更灵活的稠密卡片浏览方式。

- 在适用的模型上添加 Artificial Analysis Intelligence Index 分数。
- 为主卡片网格添加 Detailed / Compact（详细/紧凑）视图切换。
- 在紧凑视图中为每张卡片添加 Show details / Show less（展开详情/收起）切换。

## 2026 年 3 月 26 日

**新增架构对比与排序工具**

将画廊改造为更具交互性的对比工具，并扩充了多个卡片规格字段。

- 新增并排架构差异对比，提供 Model A / Model B 选择器以及每张卡片的对比操作。
- 新增 Sort by 控件，支持发布日期（从新到旧）、发布日期（从旧到新）、A-Z 与 Size 排序。
- 在适用的 MoE Scale 字段中添加激活参数百分比。
- 在规格速览中添加 KV 缓存/token（bf16）估算值。
- 在规格速览中添加 Layer mix 字段。

## 2026 年 3 月 25 日

**新增 Phi-4 架构卡片**

向公开画廊新增 Phi-4。

- [新增 Phi-4 架构卡片。](https://sebastianraschka.com/llm-architecture-gallery/#card-phi-4)

## 2026 年 3 月 20 日

**新增四张架构卡片**

新增 Nemotron 3 Nano 4B、Kimi K2.5、Mistral Small 4 与 xLSTM 7B。

- [新增 Nemotron 3 Nano 4B 架构卡片。](https://sebastianraschka.com/llm-architecture-gallery/#card-nemotron-3-nano-4b)
- [新增 Kimi K2.5 架构卡片。](https://sebastianraschka.com/llm-architecture-gallery/#card-kimi-k2-5)
- [新增 Mistral Small 4 架构卡片。](https://sebastianraschka.com/llm-architecture-gallery/#card-mistral-small-4)
- [新增 xLSTM 7B 架构卡片。](https://sebastianraschka.com/llm-architecture-gallery/#card-xlstm-7b)

## 2026 年 3 月 17 日

**新增许可证元数据**

在适用处添加许可证信息及许可证文件链接。

- 在适用处添加许可证信息及许可证文件链接。
