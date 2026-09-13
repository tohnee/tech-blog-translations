---
title: "An empirical analysis of compute-optimal large language model training"
source: https://deepmind.google/blog/an-empirical-analysis-of-compute-optimal-large-language-model-training/
site: deepmind
date: 2022-04-12
authors: Jordan Hoffmann, Sebastian Borgeaud, Arthur Mensch, Laurent Sifre
crawled: 2026-09-13
---

In the last few years, a focus in language modelling has been on improving performance through increasing the number of parameters in transformer-based models. This approach has led to impressive results and state-of-the-art performance across many natural language processing tasks.

We also pursued this line of research at DeepMind and recently showcased [Gopher](https://arxiv.org/abs/2112.11446), a 280-billion parameter model that established leading performance on a wide range of tasks including language modelling, reading comprehension, and question answering. Since then, an even larger model named [Megatron-Turing NLG](https://arxiv.org/abs/2201.11990) has been published with 530 billion parameters.

Due to the substantial cost of training these large models, it is paramount to estimate the best possible training setup to avoid wasting resources. In particular, the training compute cost for transformers is determined by two factors: the model size and the number of training tokens.

The current generation of large language models has allocated increased computational resources to increasing the parameter count of large models and keeping the training data size fixed at around 300 billion tokens. In this work, we empirically investigate the optimal tradeoff between increasing model size and the amount of training data with increasing computational resources. Specifically, we ask the question: “What is the optimal model size and number of training tokens for a given compute budget?” To answer this question, we train models of various sizes and with various numbers of tokens, and estimate this trade-off empirically.
Our main finding is that the current large language models are far too large for their compute budget and are not being trained on enough data. In fact, we find that for the number of training FLOPs used to train Gopher, a 4x smaller model trained on 4x more data would have been preferable.

![A log-log plot comparing large language models on parameters vs. training tokens, showing a solid line for "Our estimated compute-optimal scaling" with marked FLOPs. Over-parameterized models like Megatron-Turing NLG (530B), Gopher (280B), and GPT-3 (170B) sit well above the line, while the compute-optimal Chinchilla (70B) model lies directly on it.](https://lh3.googleusercontent.com/iPsfVUThNKaxHiz8VbAG4dnKxFVopLZHQ_7rV54wVuEh_jLDTKLn2yUAXXQHQYSFsH3wbnha-SffP9ssoc6sSBYRMN7nwGbkwygRH32qQ9ZqG9q-3vk=w1440)

**Figure 1:** Based on our approach, we show our projections of the optimal number of training tokens and parameters. We show points representing the training setup of three different established large language models along with our new model, Chinchilla.

We [test our data scaling hypothesis](https://arxiv.org/abs/2203.15556) by training Chinchilla, a 70-billion parameter model trained for 1.3 trillion tokens. While the training compute cost for Chinchilla and Gopher are the same, we find that it outperforms Gopher and other large language models on nearly every measured task, despite having 70 billion parameters compared to Gopher’s 280 billion.

![A bar chart comparing the accuracy percentage of Chinchilla (70B), Gopher (280B), GPT-3 (175B), and Megatron-Turing NLG (530B) across various natural language processing benchmarks (MMLU, TriviaQA, LAMBADA, HellaSwag, PIQA, WinoGrande, and BoolQ). The chart shows that Chinchilla consistently outperforms the larger models on nearly every task.](https://lh3.googleusercontent.com/tD2PbVfdzGYr-2Ip6KNKrOmOYaaJ2HYilB-G9RJeszjYOvI5d_uiGt8j0MDxN-66UJzIkH4_Kdd05buxgzoehSjngWxbdwAUQu5MBsi2QumQW538_A=w1440)

**Figure 2:** For various common benchmarks that include Question Answering (TriviaQA), CommonSense (HellaSwag, PIQA, Winogrande, and BoolQ), Reading Comprehension (LAMBADA), and the large Multi-task Language Understanding (MMLU) general knowledge benchmark, we compare the performance of Gopher, Chinchilla, GPT-3, and Megatron-Turing NLG.

After the release of Chinchilla, a model named [PaLM](https://research.google/blog/pathways-language-model-palm-scaling-to-540-billion-parameters-for-breakthrough-performance/) was released with 540 billion parameters and trained on 768 billion tokens. This model was trained with approximately 5x the compute budget of Chinchilla and outperformed Chinchilla on a range of tasks. While the training corpus is different, our methods do predict that such a model trained on our data would outperform Chinchilla despite not being compute-optimal. Given the PaLM compute budget, we predict a 140-billion-parameter model trained on 3 trillion tokens to be optimal and more efficient for inference.

An additional benefit of smaller, more performant models is that the inference time and memory costs are reduced making querying the models both faster and possible on less hardware. In practice, while the training FLOPs between Gopher and Chinchilla are the same, the cost of using Chinchilla is substantially smaller, in addition to it performing better. Further simple optimisations may be possible that are able to continue to provide large gains.
