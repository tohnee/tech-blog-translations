---
title: "Gemma Scope: helping the safety community shed light on the inner workings of language models"
source: https://deepmind.google/blog/gemma-scope-helping-the-safety-community-shed-light-on-the-inner-workings-of-language-models/
site: deepmind
date: 2024-07-31
authors: Language Model Interpretability team
crawled: 2026-09-13
---

Announcing a comprehensive, open suite of sparse autoencoders for language model interpretability.

To create an artificial intelligence (AI) language model, researchers build a system that learns from vast amounts of data without human guidance. As a result, the inner workings of language models are often a mystery, even to the researchers who train them. Mechanistic interpretability is a research field focused on deciphering these inner workings. Researchers in this field use sparse autoencoders as a kind of ‘microscope’ that lets them see inside a language model, and get a better sense of how it works.

Today, [we’re announcing Gemma Scope](https://developers.googleblog.com/en/smaller-safer-more-transparent-advancing-responsible-ai-with-gemma/), a new set of tools to help researchers understand the inner workings of Gemma 2, our lightweight family of open models. Gemma Scope is a collection of hundreds of freely available, open sparse autoencoders (SAEs) for [Gemma 2 9B](https://huggingface.co/google/gemma-2-9b) and [Gemma 2 2B](https://huggingface.co/google/gemma-2-2b). We're also open sourcing [Mishax](https://github.com/google-deepmind/mishax), a tool we built that enabled much of the interpretability work behind Gemma Scope.

We hope today’s release enables more ambitious interpretability research. Further research has the potential to help the field build more robust systems, develop better safeguards against model hallucinations, and protect against risks from autonomous AI agents like deception or manipulation.

[Try our interactive Gemma Scope demo](https://www.neuronpedia.org/gemma-scope), courtesy of Neuronpedia.

## Interpreting what happens inside a language model

When you ask a language model a question, it turns your text input into a series of ‘activations’. These activations map the relationships between the words you’ve entered, helping the model make connections between different words, which it uses to write an answer.

As the model processes text input, activations at different layers in the model’s neural network represent multiple increasingly advanced concepts, known as ‘features’.

For example, a model’s early layers might learn to [recall facts](https://arxiv.org/abs/2202.05262) like that [Michael Jordan plays basketball](https://www.alignmentforum.org/posts/iGuwZTHWb6DFY3sKB/fact-finding-attempting-to-reverse-engineer-factual-recall), while later layers may recognize more complex concepts like [the factuality of the text](https://arxiv.org/abs/2310.06824).

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

A stylised representation of using a sparse autoencoder to interpret a model’s activations as it recalls the fact that the City of Light is Paris. We see that French-related concepts are present, while unrelated ones are not.

However, interpretability researchers face a key problem: the model’s activations are a mixture of many different features. In the early days of mechanistic interpretability, researchers hoped that features in a neural network’s activations would line up with individual neurons, i.e., nodes of information. But unfortunately, in practice, neurons are active for many unrelated features. This means that there is no obvious way to tell which features are part of the activation.

**This is where sparse autoencoders come in.**

A given activation will only be a mixture of a small number of features, even though the language model is likely capable of detecting millions or even billions of them – i.e., the model uses features sparsely. For example, a language model will consider relativity when responding to an inquiry about Einstein and consider eggs when writing about omelettes, but probably won’t consider relativity when writing about omelettes.

Sparse autoencoders leverage this fact to discover a set of possible features, and break down each activation into a small number of them. Researchers hope that the best way for the sparse autoencoder to accomplish this task is to find the actual underlying features that the language model uses.

Importantly, at no point in this process do we - the researchers - tell the sparse autoencoder which features to look for. As a result, we are able to discover rich structures that we did not predict. However, because we don’t immediately know the meaning of the discovered features, we look for [meaningful patterns](https://transformer-circuits.pub/2023/monosemantic-features/index.html) in examples of text where the sparse autoencoder says the feature ‘fires’.

Here’s an example in which the tokens where the feature fires are highlighted in gradients of blue according to their strength:

![An illustrative diagram titled "The Idiom Feature" showcasing how a sparse autoencoder detects idiom-related features across various sentences. Individual tokens are highlighted in gradients of blue according to their activation strength, including words like "hot" in "hot cakes," "Croesus" in "rich like Croesus," "socks" in "knock their socks off," and "nail" in "hit the nail on the head."](https://lh3.googleusercontent.com/SgZETU9GmYp3bu_qHnh-aySzh5ItRdvkrWdsPlwqjutxKlW0VbQrStFsH_WO2MlrVpnD4iZ__Kj7w1agoFO20NiIHh-IGZh_TZLjmIkjbjCt9pkffQ=w1440)

Example activations for a feature found by our sparse autoencoders. Each bubble is a token (word or word fragment), and the variable blue color illustrates how strongly the feature is present. In this case, the feature is apparently related to idioms.

## What makes Gemma Scope unique

Prior research with sparse autoencoders has mainly focused on investigating the inner workings of [tiny models](https://arxiv.org/abs/2403.19647) or [a single layer in larger models](https://transformer-circuits.pub/2024/scaling-monosemanticity/index.html). But more ambitious interpretability research involves decoding layered, complex algorithms in larger models.

We trained sparse autoencoders at every layer and sublayer output of [Gemma 2 2B](https://huggingface.co/google/gemma-2-2bb) and [9B](https://huggingface.co/google/gemma-2-9b) to build Gemma Scope, producing more than 400 sparse autoencoders with more than 30 million learned features in total (though many features likely overlap). This tool will enable researchers to study how features evolve throughout the model and interact and compose to make more complex features.

Gemma Scope is also trained with our new, state-of-the-art [JumpReLU SAE architecture](https://arxiv.org/abs/2407.14435). The original sparse autoencoder architecture struggled to balance the twin goals of detecting which features are present, and estimating their strength. The JumpReLU architecture makes it easier to strike this balance appropriately, significantly reducing error.

Training so many sparse autoencoders was a significant engineering challenge, requiring a lot of computing power. We used about 15% of the training compute of Gemma 2 9B (excluding compute for generating distillation labels), saved about 20 Pebibytes (PiB) of activations to disk (about as much as [a million copies of English Wikipedia](https://dumps.wikimedia.org/enwiki/20240720/)), and produced hundreds of billions of sparse autoencoder parameters in total.

## Pushing the field forward

In releasing Gemma Scope, we hope to make Gemma 2 the best model family for open mechanistic interpretability research and to accelerate the community’s work in this field.

So far, the interpretability community has made great progress in understanding small models with sparse autoencoders and developing relevant techniques, like [causal](https://arxiv.org/abs/2004.12265) [interventions](https://proceedings.neurips.cc/paper_files/paper/2021/file/4f5c422f4d49a5a807eda27434231040-Paper.pdf), [automatic](https://arxiv.org/abs/2304.14997) [circuit](https://arxiv.org/abs/2403.19647) [analysis](https://arxiv.org/abs/2403.00745), [feature interpretation](https://openaipublic.blob.core.windows.net/neuron-explainer/paper/index.html), and [evaluating](https://arxiv.org/abs/2406.04093) [sparse autoencoders](https://transformer-circuits.pub/2023/monosemantic-features/index.html). With Gemma Scope, we hope to see the community scale these techniques to modern models, analyze more complex capabilities like chain-of-thought, and find real-world applications of interpretability such as tackling problems like hallucinations and jailbreaks that only arise with larger models.

[Read the Gemma Scope technical report](https://storage.googleapis.com/gemma-scope/gemma-scope-report.pdf)[See our interactive demo, courtesy of Neuronpedia](https://www.neuronpedia.org/gemma-scope)[Try our Gemma Scope coding tutorial](https://colab.research.google.com/drive/17dQFYUYnuKnP6OwQPH9v_GSYUW5aj-Rp?usp=sharing)[Download Gemma Scope](https://huggingface.co/google/gemma-scope)[Check out Mishax](https://github.com/google-deepmind/mishax)

**Acknowledgements**

Gemma Scope was a collective effort of Tom Lieberum, Sen Rajamanoharan, Arthur Conmy, Lewis Smith, Nic Sonnerat, Vikrant Varma, Janos Kramar and Neel Nanda, advised by Rohin Shah and Anca Dragan. We would like to especially thank Johnny Lin, Joseph Bloom and Curt Tigges at Neuronpedia for their assistance with the interactive demo. We are grateful for the help and contributions from Phoebe Kirk, Andrew Forbes, Arielle Bier, Aliya Ahmad, Yotam Doron, Tris Warkentin, Ludovic Peran, Kat Black, Anand Rao, Meg Risdal, Samuel Albanie, Dave Orr, Matt Miller, Alex Turner, Tobi Ijitoye, Shruti Sheth, Jeremy Sie, Tobi Ijitoye, Alex Tomala, Javier Ferrando, Oscar Obeso, Kathleen Kenealy, Joe Fernandez, Omar Sanseviero and Glenn Cameron.
