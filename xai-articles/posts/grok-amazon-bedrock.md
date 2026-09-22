---
title: "Grok on Amazon Bedrock"
date: 2026-06-17
source: https://x.ai/news/grok-amazon-bedrock
crawled: 2026-09-22
---

[Back to news](/news)

Jun 17, 2026

# Grok on Amazon Bedrock

Grok models are now available via Amazon Bedrock.

---

Today, we’re excited to announce that Grok 4.3 is now generally available on Amazon Bedrock.

Grok 4.3 achieves the lowest hallucination rate among frontier models, offers 1-million-token context window, and supports configurable reasoning efforts (none, low, medium, high). Now, Amazon Bedrock users can leverage the model through Bedrock’s secure and reliable inference engine.

[![Grok on Amazon Bedrock](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fgrok-aws-bedrock.07e-o4tqulgz8.jpg&w=3840&q=75&dpl=4c9aa05fc3fc6095ad71eaad15cf086cb4a9f22e)](https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-xai-grok-4-3.html)

## [Leading Performance in Enterprise](#leading-performance-in-enterprise)

Grok 4.3 is one of the strongest models available today for building enterprise-ready AI agents:

- #1 on Artificial Analysis Omniscience benchmark*, achieving the lowest hallucination rate among frontier models.
- #1 on Artificial Analysis Tau2 Telecom benchmark*, which evaluates real-world tool-calling performance in customer support agent scenarios.
- #1 on Vals AI Case Law and Corporate Finance benchmarks, which measure Grok's capabilities in complex document understanding tasks.

** In comparison to major frontier labs*

## [Capabilities & Pricing](#capabilities--pricing)

Grok 4.3 sits on the Pareto frontier for intelligence versus cost, delivering 2-10x more intelligence per dollar than other frontier models.

- **Input**: $1.25 per 1 million tokens
- **Output**: $2.50 per 1 million tokens

It features a 1 million context window that handles extremely long documents and codebases with ease. Developers can also configure reasoning: Use `none` for maximum speed on simple requests, or `low` / `medium` / `high` to scale reasoning effort to the difficulty of the problem.

## [Build with Grok 4.3 on Amazon Bedrock](#build-with-grok-43-on-amazon-bedrock)

Grok 4.3 is now available to all developers in [supported AWS Regions](https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-xai-grok-4-3.html#model-card-xai-grok-4-3-programmatic-access).

Copy

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

To get started, please visit the [Grok on Amazon Bedrock documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-xai-grok-4-3.html#model-card-xai-grok-4-3-sample-code). We're excited to see what you build!
