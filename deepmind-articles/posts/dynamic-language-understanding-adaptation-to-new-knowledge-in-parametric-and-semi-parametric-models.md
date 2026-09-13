---
title: "Dynamic language understanding: adaptation to new knowledge in parametric and semi-parametric models"
source: https://deepmind.google/blog/dynamic-language-understanding-adaptation-to-new-knowledge-in-parametric-and-semi-parametric-models/
site: deepmind
date: 2022-05-26
authors: Elena Gribovskaya, Angeliki Lazaridou, Tomáš Kočiský
crawled: 2026-09-13
---

Many recent successes in language models (LMs) have been achieved within a ‘static paradigm’, where the focus is on improving performance on the benchmarks that are created without considering the temporal aspect of data. For instance, answering questions on events that the model could learn about during training, or evaluating on text sub-sampled from the same period as the training data. However, our language and knowledge are dynamic and ever evolving. Therefore, to enable a more realistic evaluation of question-answering models for the next leap in performance, it’s essential to ensure they are flexible and robust when encountering new and unseen data.

![Timeline diagram illustrating the StreamingQA evaluation setup, showing a "Knowledge Corpus" spanning 2007 to 2020, followed by a quarterly evaluation ("Evaluate: future articles & questions") divided into Q1, Q2, Q3, and Q4 throughout 2020 and 2021.](https://lh3.googleusercontent.com/voWKunmt0yVRAbZOSo9eS_gr4fnWeqQ5KHc6pO76mnUmzhQ2sil5xEbl5CsWOkraROILnVP8iGw6wadVkcKQPb_zKOUoVa-atppgNJ67pCBmbAWHvCc=w1440)

Figure 1. We evaluate our models on unseen language and knowledge, seen here using questions about events in 2020, while the model has been trained on data up until the end of 2019.

In 2021, we released [Mind the Gap: Assessing Temporal Generalization in Neural Language Models](https://arxiv.org/abs/2102.01951) and the [dynamic language modelling benchmarks](https://github.com/deepmind/deepmind-research/tree/master/pitfalls_static_language_models) for WMT and arXiv to facilitate language model evaluation that take temporal dynamics into account. In this paper, we highlighted issues that current state-of-the-art large LMs face with temporal generalisation and found that knowledge-intensive tokens take a considerable performance hit.

Today, we’re releasing two papers and a new benchmark that further advance research on this topic. In [StreamingQA: A Benchmark for Adaptation to New Knowledge over Time in Question Answering Models](http://arxiv.org/abs/2205.11388), we study the downstream task of question-answering on our newly proposed benchmark, [StreamingQA](https://github.com/deepmind/streamingqa): we want to understand how parametric and retrieval-augmented, semi-parametric question-answering models adapt to new information, in order to answer questions about new events. In [Internet-augmented language models through few-shot prompting for open-domain question answering](https://arxiv.org/abs/2203.05115), we explore the power of combining a few-shot prompted large language model along with Google Search as a retrieval component. In doing so, we aim to improve the model's factuality, while making sure it has access to up-to-date information for answering a diverse set of questions.

## StreamingQA: A Benchmark for Adaptation to New Knowledge over Time in Question Answering Models

Knowledge and language understanding of models evaluated through question-answering (QA) has been commonly studied on static snapshots of knowledge, like Wikipedia. To study how semi-parametric QA models and their underlying parametric LMs adapt to evolving knowledge, we constructed the new large-scale benchmark, StreamingQA, with human-written and automatically generated questions asked on a given date, to be answered from 14 years of time-stamped news articles (see Figure 2). We show that parametric models can be updated without full retraining, while avoiding catastrophic forgetting. For semi-parametric models, adding new articles into the search space allows for rapid adaptation, however, models with an outdated underlying LM underperform those with a retrained LM.

![An example of the StreamingQA benchmark dataset showing a "Recent subset" question about net zero targets from February 2020, and a "Past subset" question about a 2016 Netflix series asked in April 2020.](https://lh3.googleusercontent.com/fKIKWzhgXEhCZIsP83_g9YdPWo5-ctX-HKzQRoNbx1Lj4fYDo2Hi6ZO1eF30VLgbBzAxun18567rkbaVh7OzahWn3WPLCbRQWc8GT2mL6MKIUv7sjA=w1440)

Figure 2. Example questions from the StreamingQA benchmark.

## Internet-augmented language models through few-shot prompting for open-domain question-answering

We’re aiming to capitalise on the unique few-shot capabilities offered by large-scale language models to overcome some of their challenges, with respect to grounding to factual and up-to-date information. Motivated by semi-parametric LMs, which ground their decisions in externally retrieved evidence, we use few-shot prompting to learn to condition LMs on information returned from the web using Google Search, a broad and constantly updated knowledge source. Our approach does not involve fine-tuning or learning additional parameters, thus making it applicable to virtually any language model. And indeed, we find that LMs conditioned on the web surpass the performance of closed-book models of similar, or even larger, model size in open-domain question-answering.
