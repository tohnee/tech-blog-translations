---
title: "机器学习/AI 的 Hello World：从随机森林到 RLVR"
title_en: "ML/AI Hello Worlds: From RF to RLVR"
source: https://sebastianraschka.com/blog/2025/hello-world-ai.html
crawled: 2026-09-06
translated: 2026-09-06
---

# 机器学习/AI 的 Hello World：从随机森林到 RLVR

> 原文：[ML/AI Hello Worlds: From RF to RLVR](https://sebastianraschka.com/blog/2025/hello-world-ai.html)

两年前，我在社交媒体上[发过一份](https://x.com/rasbt/status/1740006870096433509?s=20)机器学习和 AI 的"Hello World"示例清单。这里的"Hello World"指的是用来展示某种方法的入门友好示例。

我设了一个两年一次的日历提醒，用来回顾和补充这份清单。这次我认真想了很久，2025 年的例子会是什么样子。所以，这是一篇短文，附上更新后的清单和一些解释性背景。

- 2013：在 Iris 数据集上跑 RandomForestClassifier
- 2015：在 Titanic 数据集上跑 XGBoost
- 2017：在 MNIST 上跑 MLP
- 2019：在 CIFAR-10 上跑 AlexNet
- 2021：在 IMDb 影评上跑 DistilBERT
- 2023：Llama 2 配 [LoRA](https://sebastianraschka.com/glossary/#lora "LoRA (Low-Rank Adaptation)") 跑 Alpaca 50k
- 2025：Qwen3 配 [RLVR](https://sebastianraschka.com/glossary/#rlvr "RLVR (Reinforcement Learning with Verifiable Rewards)") 跑 MATH-500

让我们逐一来看。

**2013：Iris 数据集上的 RandomForestClassifier**

注意，清单中的方法都比当时的前沿滞后几年。例如，[随机森林](https://link.springer.com/article/10.1023/A:1010933404324)早在 2001 年就已提出。但根据我对当年的记忆，直到 2013 年前后——它们在 2012 年被加入当时最主要的机器学习库 [scikit-learn](https://scikit-learn.org/stable/) 之后——才真正变得流行和主流。

- 《Python Machine Learning》中的[代码示例](https://github.com/rasbt/python-machine-learning-book/blob/master/code/ch03/ch03.ipynb)

![random forest decision region](https://sebastianraschka.com/images/blog/2025/hello-world-ai/1.webp)

图出自我的 [2015 年《Python Machine Learning》一书](https://amzn.to/3KnXunE)

**2015：Titanic 数据集上的 XGBoost**

[XGBoost](https://github.com/dmlc/xgboost) 于 2014 年首次发布，我记得它在 2015 年随着 Kaggle 竞赛火了起来（还有那个人人入门都会先打的著名 [Titanic 数据集竞赛](https://www.kaggle.com/competitions/titanic)）。

- Kaggle 上的[代码示例](https://www.kaggle.com/code/wissams/titanic-competition-step-by-step-using-xgboost/)

![Titanic Kaggle screenshot](https://sebastianraschka.com/images/blog/2025/hello-world-ai/2.webp)

著名的 [Titanic Kaggle 竞赛](https://www.kaggle.com/competitions/titanic)

**2017：MNIST 上的 MLP**

多层感知机（MLP）已经存在非常非常久了。在 [1986 年的反向传播论文](https://www.nature.com/articles/323533a0)之后，它们在 20 世纪 80、90 年代变得勉强可用，但并不算流行。我记得 2010 年代早期仍是随机森林、支持向量机和梯度提升（尤其是 XGBoost）的天下。与此同时，计算机视觉领域里非神经网络方法也依然流行。不过，随着 [TensorFlow](https://www.tensorflow.org) 于 2015 年首次发布、2017 年发布 TensorFlow 1.0，MLP 和神经网络整体在那段时间真正开始提速发展。

- 我的深度学习 notebook 合集中的[代码示例](https://github.com/rasbt/deeplearning-models/blob/master/tensorflow1_ipynb/mlp/mlp-basic.ipynb)

![backprop and MNIST](https://sebastianraschka.com/images/blog/2025/hello-world-ai/3.webp)

图出自我的 [2015 年《Python Machine Learning》一书](https://amzn.to/3KnXunE)

**2019：CIFAR-10 上的 AlexNet**

AlexNet 或许在本清单中应该排得更靠前，因为它早在 2012 年就通过 [ImageNet Classification with Deep Convolutional Neural Networks](https://proceedings.neurips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf) 一文问世。不过，它同样直到 2017 年 PyTorch 和 TensorFlow 1.0 发布后才真正流行起来。当时大多数人还在用 Caffe，不过计算机视觉也开始向 TensorFlow 迁移。

话虽如此，由于卷积神经网络需要 GPU 才能做出有意义的工作——CUDA 和 cuDNN 让 GPU 变得更易用——我认为把它排在"2017 MNIST 上的 MLP"这个例子之后是合理的。（另外，ImageNet 对当时的大多数人来说太大太贵，所以 [CIFAR-10 和 CIFAR-100](https://www.cs.toronto.edu/~kriz/cifar.html) 是流行的入门数据集。）

- 我的深度学习 notebook 合集中的[代码示例](https://github.com/rasbt/deeplearning-models/blob/master/pytorch_ipynb/cnn/cnn-alexnet-cifar10.ipynb)

![Alexnext architecture](https://sebastianraschka.com/images/blog/2025/hello-world-ai/4.webp)

出自 [AlexNet 论文](https://papers.nips.cc/paper_files/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html)的 AlexNet 架构

**2021：IMDb 影评上的 DistilBERT**

在 [IMDb 影评情感分类数据集](https://ai.stanford.edu/~amaas/data/sentiment/)上跑 [DistilBERT](https://arxiv.org/abs/1910.01108)，我们就进入了语言模型开始加速发展的时代。诚然，Transformer 架构于 2017 年提出，BERT 是 2018 年，DistilBERT 是 2019 年，但它真正流行起来还是花了几年的时间。

- 我的深度学习 notebook 合集中的[代码示例](https://github.com/rasbt/deeplearning-models/blob/master/pytorch_ipynb/transformer/distilbert-hf-finetuning.ipynb)

![Ways to pretrain an LLM classifier](https://sebastianraschka.com/images/blog/2025/hello-world-ai/5.webp)

把 DistilBERT 这类预训练 Transformer 微调为分类器的各种方式（出自我的 [Finetuning Large Language Models](https://magazine.sebastianraschka.com/p/finetuning-large-language-models) 一文）

**2023：Llama 2 配 LoRA 跑 Alpaca 50k**

2023 年是 ChatGPT 发布后的第二年，LLM 迅速升温。训练或微调 LLM 的成本仍然是很大的门槛，但 [LoRA](https://arxiv.org/abs/2106.09685)、[Llama 1 和 2](https://arxiv.org/abs/2307.09288) 与 [Alpaca 数据集](https://crfm.stanford.edu/2023/03/13/alpaca.html)的组合让 LLM 突然变得平易近人得多，指令微调也随之迎来爆发。

- Radek Osmulski 在 GitHub 上的[代码示例](https://gist.github.com/radekosmulski/c3cce1a52b52b9b2037e1941de5afa32)

![Llama 2 architecture versus GPT](https://sebastianraschka.com/images/blog/2025/hello-world-ai/6.webp)

Llama 2 架构，出自我的 [GPT 到 Llama 转换指南](https://github.com/rasbt/LLMs-from-scratch/blob/main/ch05/07_gpt_to_llama)

**2025：Qwen3 配 RLVR 跑 MATH-500**

今年则是推理模型和[可验证奖励强化学习](https://magazine.sebastianraschka.com/p/understanding-reasoning-llms)（RLVR）之年——它在 2024 年随着首批 [OpenAI o1 发布](https://openai.com/index/learning-to-reason-with-llms/)引发的热潮起步，随后在 2025 年 1 月随着 [DeepSeek R1](https://arxiv.org/abs/2501.12948) 的发布真正升温。

今年，[Qwen3 系列模型](https://huggingface.co/collections/Qwen/qwen3)也变得非常流行，它们提供从 0.6B 到 235B 的多种规格。然而，用 RLVR 训练一个[推理模型](https://sebastianraschka.com/glossary/#reasoning-model "Reasoning Model")仍然不是件容易的事，即使对 [MATH-500](https://huggingface.co/datasets/HuggingFaceH4/MATH-500) 数据集训练部分中最小的模型也是如此（这基本上就是我[新书](https://mng.bz/Nwr7)的主题）。

不过，现在有一些专有 API 服务可以向初学者展示 RLVR 是什么，所以它可以作为一个不错的"Hello World"示例和 AI 入门（在初学者想深入了解更多细节之前）。

- 来自 Tinker API Cookbook 的[代码示例](https://github.com/thinking-machines-lab/tinker-cookbook/tree/main/tinker_cookbook/recipes/math_rl)（我与这家公司没有关系，但认为这是一个不错的快速入门示例）；从零实现将很快加入我的[从零构建推理模型之书](https://github.com/rasbt/reasoning-from-scratch)。

![Reasoning model training](https://sebastianraschka.com/images/blog/2025/hello-world-ai/7.webp)

图出自我的 [The State of Reinforcement Learning for LLM Reasoning](https://magazine.sebastianraschka.com/p/the-state-of-llm-reasoning-model-training) 一文。
