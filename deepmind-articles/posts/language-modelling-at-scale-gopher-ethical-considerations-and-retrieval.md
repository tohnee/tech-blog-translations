---
title: "Language modelling at scale: Gopher, ethical considerations, and retrieval"
source: https://deepmind.google/blog/language-modelling-at-scale-gopher-ethical-considerations-and-retrieval/
site: deepmind
date: 2021-12-08
authors: Jack Rae, Geoffrey Irving, Laura Weidinger
crawled: 2026-09-13
---

Language, and its role in demonstrating and facilitating comprehension - or intelligence - is a fundamental part of being human. It gives people the ability to communicate thoughts and concepts, express ideas, create memories, and build mutual understanding. These are foundational parts of social intelligence. It’s why our teams at DeepMind study aspects of language processing and communication, both in artificial agents and in humans.

As part of a broader portfolio of AI research, we believe the development and study of more powerful language models – systems that predict and generate text – have tremendous potential for building advanced AI systems that can be used safely and efficiently to summarise information, provide expert advice and follow instructions via natural language. Developing beneficial language models requires research into their potential impacts, including the risks they pose. This includes collaboration between experts from varied backgrounds to thoughtfully anticipate and address the challenges that training algorithms on existing datasets can create.

Today we are releasing three papers on language models that reflect this interdisciplinary approach. They include a detailed study of [a 280 billion parameter transformer language model called Gopher](https://arxiv.org/abs/2112.11446), [a study of ethical and social risks associated with large language models](https://arxiv.org/abs/2112.04359), and [a paper investigating a new architecture with better training efficiency.](https://arxiv.org/abs/2112.04426)

## Gopher - A 280 billion parameter language model

In the quest to explore language models and develop new ones, we trained a series of transformer language models of different sizes, ranging from 44 million parameters to 280 billion parameters (the largest model we named Gopher).

Our research investigated the strengths and weaknesses of those different-sized models, highlighting areas where increasing the scale of a model continues to boost performance – for example, in areas like reading comprehension, fact-checking, and the identification of toxic language. We also surface results where model scale does not significantly improve results — for instance, in logical reasoning and common-sense tasks.

![A bar chart comparing accuracy percentages across fields like Humanities, Social sciences, Medicine, General knowledge, Science/technology, and Maths for GPT-3, UnifiedQA, Gopher, and Human expert, showing Gopher consistently outperforming other models but trailing behind human expert levels.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6224d01f62cce9f8638e7d78_Fig201.svg)

Performance on the Massive Multitask Language Understanding (MMLU) benchmark broken down by category. Gopher improves upon prior work across several categories.

In our research, we found the capabilities of Gopher exceed existing language models for a number of key tasks. This includes the Massive Multitask Language Understanding (MMLU) benchmark, where Gopher demonstrates a significant advancement towards human expert performance over prior work.

As well as quantitative evaluation of Gopher, we also explored the model through direct interaction. Among our key findings was that, when Gopher is prompted towards a dialogue interaction (like in a chat), the model can sometimes provide surprising coherence.

![A screenshot of a dialogue between a User and Gopher discussing cell biology and prokaryotes, where Gopher successfully provides accurate facts, definitions, examples, and a Wikipedia link about E. coli.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6224d04aacea2444a5eeef02_Fig202.svg)

Here Gopher can discuss cell biology and provide a correct citation despite no specific dialogue fine-tuning. However our research also detailed several failure modes that persist across model sizes, amongst them a tendency for repetition, the reflection of stereotypical biases, and the confident propagation of incorrect information.

![A screenshot of a text-based dialogue illustrating a failure mode where Gopher confidently provides incorrect answers to questions about the 2021 Women's US Open winner, French-speaking territories in South America, and Euler's identity, while denying any uncertainty about its responses.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6224d058786212486e2a4f1b_Fig203.svg)

This type of analysis is important, because understanding and documenting failure modes gives us an insight into how large language models could lead to downstream harms, and shows us where mitigation efforts in research should focus to address those issues.

## Ethical and social risks from Large Language Models

In our second paper, we anticipate possible ethical and social risks from language models, and create a comprehensive classification of these risks and failure modes, building on prior research in this area [[Bommasani et al 2021](https://arxiv.org/abs/2108.07258), [Bender et al 2021](https://dl.acm.org/doi/abs/10.1145/3442188.3445922), [Patterson et al 2021](https://arxiv.org/abs/2104.10350)]. This systematic overview is an essential step towards understanding these risks and mitigating potential harm. We present a taxonomy of the risks related to language models, categorised into six thematic areas, and elaborate on 21 risks in-depth.

Taking a broad view of different risk areas is essential: as we show in the paper, an overly narrow focus on a single risk in isolation can make other problems worse. The taxonomy we present serves as a foundation for experts and wider public discourse to build a shared overview of ethical and social considerations on language models, make responsible decisions, and exchange approaches to dealing with the identified risks.

![An infographic displaying six thematic risk areas for large language models, each featuring a blue icon, a bold title, and a brief description: - **Discrimination, exclusion and toxicity**: Harms from discriminatory and exclusionary speech.- **Information hazards**: Harms from leaking or inferring true sensitive information.- **Misinformation harms**: Harms from producing false or misleading information.- **Malicious uses**: Harms from actors intentionally using models to cause harm.- **Human-computer interaction harms**: Harms from users overly trusting the model or treating it as human-like.- **Automation, access and environmental harms**: Harms from environmental or downstream economic impacts.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6224d06f425601d8baac2b6b_Fig204.svg)

Our research finds that two areas in particular require further work. First, current benchmarking tools are insufficient for assessing some important risks, for example, when language models output misinformation and people trust this information to be true. Assessing risks like these requires more scrutiny of human-computer-interaction with language models. In our paper we list several risks that similarly require novel or more interdisciplinary analysis tools. Second, more work is needed on risk mitigations. For example, language models are known to reproduce harmful social stereotypes, but research on this problem is still in early stages, as a [recent DeepMind paper](https://deepmind.com/research/publications/2021/Challenges-in-Detoxifying-Language-Models) showed.

## Efficient Training with Internet-Scale Retrieval

Our final paper builds on the foundations of Gopher and our taxonomy of ethical and social risk by proposing an improved language model architecture that reduces the energy cost of training and makes it easier to trace model outputs to sources within the training corpus.

The Retrieval-Enhanced Transformer (RETRO) is pre-trained with an Internet-scale retrieval mechanism. Inspired by how the brain relies on dedicated memory mechanisms when learning, RETRO efficiently queries for passages of text to improve its predictions. By comparing generated texts to the passages RETRO relied upon for generation, we can interpret why the model makes certain predictions and where they came from. We also see how the model obtains comparable performance to a regular Transformer with an order of magnitude fewer parameters, and obtains state-of-the-art performance on several language modeling benchmarks.

![A block diagram illustrating the Retrieval-Enhanced Transformer (RETRO) architecture, showing how an input sequence queries a retrieval database to extract neighbor passages, which are encoded and integrated via cross-attention layers to produce an output sequence.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6224d07ff43a03f5048d6d4e_Fig205.svg)

## Going forward

These papers offer a foundation for DeepMind’s language research going forward, particularly in areas that will have a bearing on how these models are evaluated and deployed. Addressing these areas will be critical for ensuring safe interactions with AI agents – from people telling agents what they want to agents explaining their actions to people. Research in the broader community on using communication for safety includes [natural language explanations](https://arxiv.org/abs/1812.01193), [using communication to reduce uncertainty](https://en.wikipedia.org/wiki/Human_Compatible), and using language to unpack complex decisions into pieces such as [amplification](https://arxiv.org/abs/1810.08575), [debate](https://arxiv.org/abs/1805.00899), and [recursive reward modeling](https://arxiv.org/abs/1811.07871) -- all critical areas of exploration.

As we continue our research on language models, DeepMind will remain cautious and thoughtful. This requires stepping back to assess the situation we find ourselves in, mapping out potential risks, and researching mitigations. We will strive to be transparent and open about the limitations of our models and will work to mitigate identified risks. At each step, we draw on the breadth of expertise from our multidisciplinary teams, including from our Language, Deep Learning, Ethics, and Safety teams. This approach is key to creating large language models that serve society, furthering our mission of solving intelligence to advance science and benefit humanity.
