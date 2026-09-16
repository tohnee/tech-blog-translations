---
title: "GPT Model Training Competition Heats Up - Nvidia Has A Legitimate Challenger"
subtitle: "Cerebras Is Now Cost Competitive For Training GPT-like Large Language Models"
date: 2022-12-01
source: https://newsletter.semianalysis.com/p/gpt-model-training-competition-heats
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: everyone
paywalled: false
---

# GPT Model Training Competition Heats Up - Nvidia Has A Legitimate Challenger

**Cerebras Is Now Cost Competitive For Training GPT-like Large Language Models**

Unless you’ve been living under a rock, large language transformer models are clearly going to change the world. Don’t believe us? Check out [OpenAI’s Chat GPT.](https://openai.com/blog/chatgpt/) The capabilities are nuts, from [coding](https://twitter.com/jasondebolt/status/1598243854343606273?s=20&t=kasqfQ4tE4S4VI_b52LEDQ) to [quantum computing](https://twitter.com/quantumVerd/status/1598287336994967554?s=20&t=kasqfQ4tE4S4VI_b52LEDQ) to [search](https://twitter.com/jdjkelly/status/1598021488795586561?s=20&t=m1Ds3k7SZSPq6hIuEZyPRw) to [art](https://twitter.com/GuyP/status/1598020781065527296?s=20&t=m1Ds3k7SZSPq6hIuEZyPRw) to [creative writing](https://twitter.com/AndrewMayne/status/1598076165402419201?s=20&t=m1Ds3k7SZSPq6hIuEZyPRw) to [hacking](https://twitter.com/moyix/status/1598081204846489600?s=20&t=m1Ds3k7SZSPq6hIuEZyPRw) to [healthcare](https://twitter.com/RoxanaDaneshjou/status/1598170660186251264?s=20&t=m1Ds3k7SZSPq6hIuEZyPRw).

If you’ve followed our newsletter for a while, you know that we aren’t the best at grammar, but over the last few months, that’s changed. We even use semicolons in sentences! No, we didn’t hire an editor; we use a GPT-like model to grammar check and suggest rephrasing. Some firms have even disclosed that language models’ code generation capacities now contribute to as much as 25% of new additions to their codebases.

The tough pill to swallow with these large language models is the training cost. With large models such as OpenAI GPT3, Google Pathways, DeepMind Chinchilla, Nvidia Megatron, etc, a massive company with deep pockets funding the enormous compute bill. Since GPT3’s release, the conversation has revolved around a few metrics.

1. [How much bigger can we go in model size and datasets?](https://www.semianalysis.com/p/the-ai-brick-wall-a-practical-limit)
2. How much does it cost to train?
3. Is there anyone who can break the moat of Nvidia because their GPUs are so expensive?

For the answer to the first question, stay tuned because here at NeurIPS, we have seen and heard some crazy rumors about OpenAI’s GPT4 and future DeepMind models.

For the 2nd and 3rd questions, some firms are starting to break the moat. While most of the industry is using GPUs, both Google and their sister company DeepMind are using the in-house TPU for training large language models. Furthermore, Google TPU has a few external customers, namely Cohere. Cohere is building large language models which can be accessed via an API.

[Cerebras](https://www.cerebras.net/press-release/cerebras-unveils-andromeda-a-13.5-million-core-ai-supercomputer-that-delivers-near-perfect-linear-scaling-for-large-language-models), the company making chips the [size of entire wafers](https://www.semianalysis.com/p/cerebras-wafer-scale-hardware-crushes), released some very compelling benchmarks for GPT-style models running on their Andromeda system. Andromeda is a 16 CS-2 wafer-scale system with a combined 13.5 million AI cores fed by 284 64-core AMD EPYC Milan processors. These systems are linked together with their SwarmX fabric link, which provides more than 96.8 terabits of bandwidth.

This is the first time any vendor has ever released information that can be directly compared to Nvidia in the AI training battleground that matters, massive models. It’s very telling that Intel, AMD, Graphcore, SambaNova, etc, have training dedicated chips, but can’t show off their supposedly special hardware in large-scale clusters with large models.

We compared Cerebras’s results to those from [Mosaic ML](https://www.mosaicml.com/blog/gpt-3-quality-for-500k). Mosaic ML is a machine learning training orchestration platform. They are cloud and hardware agnostic, utilizing multiple public clouds, and their own internal datacenters to minimize training costs. Mosaic is a good basis for an optimized GPU stack that is also easy to use because the user doesn’t have to deal with many of the typical hardware-related and scaling issues.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/6b85936b-aaa5-4ca3-ad71-6b9057905f23_1685x438.png)

Cerebras and Nvidia are cost equivalent for training a large GPT style model!

Cerebras is behind Nvidia A100 GPUs on smaller GPT models, but they catch up as the model sizes increase.

Cerebras claims they will get a lot more efficient, especially with the addition of techniques like [unstructured sparsity](https://www.cerebras.net/blog/harnessing-the-power-of-sparsity-for-large-gpt-ai-models).

Mosaic ML also says they can do better now with some clever techniques that they have implemented on the backend. Mosaic’s current goal is to bring the cost to train a GPT 3 quality model from $450k to $100k. As Hopper begins to become available next year, it is likely that it brings significant cost improvements.

The other thing you may have noticed in the table is the days to train. While we did include this, we wouldn’t look too closely at it. Training time is a function of how large of a cluster of chips you can obtain. Scaling with GPUs and Cerebras Wafer Scale chips seems to be near perfect, ignoring the batch size issues. The first handful of results from Cerebras only uses 4 CS-2, with the largest using all 16 CS-2.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/cd750ee4-ce50-4c21-8fcc-5b65c08003a6_1366x617.png)

Cerebras also mentioned that long sequence lengths are "GPU impossible". That's simply not true. Multiple LLM companies and tech giants can do long sequence lengths with standard GPUs just fine, with very little effort.

Cerebras has signed deal with the $1.7B AI startup Jasper to provide compute, which is big news!

If you enjoyed reading, please share!

[Share](https://newsletter.semianalysis.com/p/gpt-model-training-competition-heats?utm_source=substack&utm_medium=email&utm_content=share&action=share)

[Get 20% off a group subscription](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)

[Give a gift subscription](https://newsletter.semianalysis.com/subscribe?&gift=true)
