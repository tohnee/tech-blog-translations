---
title: "Inside the LLM Architecture Gallery"
source: https://sebastianraschka.com/blog/2026/llm-architecture-gallery.html
crawled: 2026-09-06
---

# Inside the LLM Architecture Gallery

I draw architecture diagrams whenever I work through a new model report. They help me answer concrete questions. How many layers use full attention? Where does mixture-of-experts routing happen? Does every layer add to the [KV cache](https://sebastianraschka.com/glossary/#kv-cache "KV Cache")?

The figures are useful inside their original articles, but they became hard to find once they were spread across many posts. I built the [LLM Architecture Gallery](https://sebastianraschka.com/llm-architecture-gallery/) to keep them in one place. It started with figures from [The Big LLM Architecture Comparison](https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison) and [A Dream of Spring for Open-Weight LLMs](https://magazine.sebastianraschka.com/p/a-dream-of-spring-for-open-weight). I have since added models from newer articles and standalone technical reports.

At the time of this update, the gallery contains 93 model cards from 42 source articles and reports. It covers familiar dense architectures such as GPT-2 and Llama 3, recent mixture-of-experts models such as DeepSeek V3 and Kimi K2, and hybrids that combine attention with recurrent or state-space layers.

[![LLM Architecture Gallery](https://sebastianraschka.com/llm-architecture-gallery/images/hero/architecture-gallery-hero.webp)](https://sebastianraschka.com/llm-architecture-gallery/)

A selection of the architecture diagrams collected in the gallery. Click the image to open the gallery.

## What each card contains

The diagram is the main part of each card. Clicking it opens the high-resolution version, which is usually easier to read than the thumbnail. The card also links back to the exact article section where I discussed the model.

The fact sheet underneath summarizes the details I tend to look up repeatedly. These include model scale, context length, [vocabulary size](https://sebastianraschka.com/glossary/#vocabulary-size "Vocabulary Size"), license, decoder type, attention mechanism, and the layer recipe. I also include a logical batch-size-1 bf16 estimate of the KV-cache growth per generated token when the public configuration provides enough information.

For models covered by Artificial Analysis, the card shows the AA Intelligence Index and its General, Scientific, Coding, and Agents profile. Missing data stays marked as `N/A`. I prefer that over filling a gap with an estimate from an unrelated source.

Most cards also include the public `config.json`, technical report, and a from-scratch implementation when one is available. This makes it possible to move from the simplified diagram to the underlying configuration without searching for the repository again.

## Comparing two architectures

Architecture changes are often easier to see in a direct comparison. The gallery’s [diff tool](https://sebastianraschka.com/llm-architecture-gallery/#architecture-diff-tool) lets you select two models and puts their diagrams and fact-sheet fields side by side.

DeepSeek V3 and DeepSeek V3.2 are a useful example. Their overall stacks look similar, while the attention field exposes the addition of [DeepSeek Sparse Attention](https://sebastianraschka.com/glossary/#deepseek-sparse-attention "DeepSeek Sparse Attention") in V3.2. The same view works well for comparing dense and MoE variants within one family, or for checking how the layer mix changed between releases. I wrote a separate [short note about the diff tool](https://sebastianraschka.com/blog/2026/llm-architecture-gallery-diff-tool.html) with a worked example.

## Following an unfamiliar term

The diagrams use many abbreviations because space is limited. If a card mentions GQA, MLA, sliding-window attention, NoPE, [KV sharing](https://sebastianraschka.com/glossary/#cross-layer-kv-sharing "Cross-Layer KV Sharing"), or another recurring mechanism, the related concept links lead to a short explainer. These pages focus on the mechanism itself and use individual models as examples.

The gallery also has two cross-model summaries. The [active-parameter ratio table](https://sebastianraschka.com/llm-architecture-gallery/active-parameter-ratio/) compares how much of each sparse model is used for a token. The [attention mechanism distribution](https://sebastianraschka.com/llm-architecture-gallery/attention-mechanism-distribution/) counts how often different attention designs and layer patterns appear across the gallery.

## Scope and corrections

I focus on text-only LLMs and the language-model backbones of multimodal systems. A card for a multimodal release therefore describes the text decoder rather than its vision or audio components. The diagrams are compact reading aids, so they leave out many training details and implementation choices that do not affect the high-level stack.

I update the gallery as new technical reports and configurations become available. There is a [changelog](https://sebastianraschka.com/llm-architecture-gallery/changelog/) and a dedicated [RSS feed](https://sebastianraschka.com/llm-architecture-gallery/rss.xml) for these updates. If you spot an incorrect field, a mislabeled block, or a broken source link, please use the issue link at the top of the [gallery](https://sebastianraschka.com/llm-architecture-gallery/).
