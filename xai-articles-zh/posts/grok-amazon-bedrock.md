---
title: "Grok 登陆 Amazon Bedrock"
title_en: "Grok on Amazon Bedrock"
date: 2026-06-17
source: https://x.ai/news/grok-amazon-bedrock
crawled: 2026-09-22
translated: 2026-09-22
---

# Grok 登陆 Amazon Bedrock

> 原文：[Grok on Amazon Bedrock](https://x.ai/news/grok-amazon-bedrock) · xAI

[返回新闻列表](/news)

2026 年 6 月 17 日

Grok 系列模型现已通过 Amazon Bedrock 提供。

---

今天，我们很高兴地宣布 Grok 4.3 现已在 Amazon Bedrock 上正式可用。

Grok 4.3 在前沿模型中拥有最低的幻觉率，提供 100 万 token 上下文窗口，并支持可配置的推理努力级别（none、low、medium、high）。现在，Amazon Bedrock 用户可以通过 Bedrock 安全可靠的推理引擎使用该模型。

[![Grok on Amazon Bedrock](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fgrok-aws-bedrock.07e-o4tqulgz8.jpg&w=3840&q=75&dpl=4c9aa05fc3fc6095ad71eaad15cf086cb4a9f22e)](https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-xai-grok-4-3.html)

## [企业级场景中的领先性能](#leading-performance-in-enterprise)

Grok 4.3 是当今构建企业级 AI 智能体的最强模型之一：

- 在 Artificial Analysis Omniscience 基准*上排名第一，在前沿模型中取得最低幻觉率。
- 在 Artificial Analysis Tau2 Telecom 基准*上排名第一，该基准评测客服智能体场景下的真实世界工具调用表现。
- 在 Vals AI 判例法（Case Law）与公司金融（Corporate Finance）基准上排名第一，衡量 Grok 在复杂文档理解任务中的能力。

** 与主要前沿实验室相比*

## [能力与定价](#capabilities--pricing)

Grok 4.3 位于智能与成本的帕累托前沿，每美元能交付的智能是其他前沿模型的 2-10 倍。

- **输入**：每 100 万 token 1.25 美元
- **输出**：每 100 万 token 2.50 美元

它配备 100 万 token 的上下文窗口，可以轻松处理超长文档和代码库。开发者还可以配置推理：简单请求用 `none` 获得最快速度，或用 `low` / `medium` / `high` 按问题难度调节推理投入。

## [在 Amazon Bedrock 上用 Grok 4.3 构建](#build-with-grok-43-on-amazon-bedrock)

Grok 4.3 现已面向[受支持 AWS 区域](https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-xai-grok-4-3.html#model-card-xai-grok-4-3-programmatic-access)的所有开发者开放。

复制

```
curl https://bedrock-mantle.us-west-2.api.aws/openai/v1/responses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $BEDROCK_API_KEY" \
  -d '{
    "model": "grok-4.3",
    "input": "What is the meaning of life?",
    "reasoning": {
        "effort": "low"
    },
    "include": ["reasoning.encrypted_content"]
  }'
```

bash

要开始使用，请访问 [Grok on Amazon Bedrock 文档](https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-xai-grok-4-3.html#model-card-xai-grok-4-3-sample-code)。我们期待看到你构建的作品！
