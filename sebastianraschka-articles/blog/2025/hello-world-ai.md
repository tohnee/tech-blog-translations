---
title: "ML/AI Hello Worlds: From RF to RLVR"
source: https://sebastianraschka.com/blog/2025/hello-world-ai.html
crawled: 2026-09-06
---

# ML/AI Hello Worlds: From RF to RLVR

Two years ago, I [posted a list](https://x.com/rasbt/status/1740006870096433509?s=20) of “Hello World” examples for machine learning and AI on social. Here, the “Hello World” means beginner-friendly examples to showcase a method.

I set a biennial calendar alert to revisit and append to it. I was thinking pretty hard about what a 2025 example could look like. So, here is a short post with the updated list and some explanations for more context.

- 2013: RandomForestClassifier on Iris
- 2015: XGBoost on Titanic
- 2017: MLPs on MNIST
- 2019: AlexNet on CIFAR-10
- 2021: DistilBERT on IMDb movie reviews
- 2023: Llama 2 with [LoRA](https://sebastianraschka.com/glossary/#lora "LoRA (Low-Rank Adaptation)") on Alpaca 50k
- 2025: Qwen3 with [RLVR](https://sebastianraschka.com/glossary/#rlvr "RLVR (Reinforcement Learning with Verifiable Rewards)") on MATH-500

Let’s go through them one by one.

**2013: RandomForestClassifier on Iris**

Note that the methods in the list lag a few years behind. For instance, [random forests](https://link.springer.com/article/10.1023/A:1010933404324) were introduced in 2001. But based on what I remember from back then, they didn’t become super popular and mainstream until 2013ish, after they were added to [scikit-learn](https://scikit-learn.org/stable/) in 2012, which was the main machine learning library back then.

- [Code example](https://github.com/rasbt/python-machine-learning-book/blob/master/code/ch03/ch03.ipynb) from Python Machine Learning

![random forest decision region](https://sebastianraschka.com/images/blog/2025/hello-world-ai/1.webp)

Figure from my [2015 Python Machine Learning book](https://amzn.to/3KnXunE)

**2015: XGBoost on Titanic**

[XGBoost](https://github.com/dmlc/xgboost) was first released in 2014, and I remember that it became super popular in 2015 in the context of Kaggle competitions (and there was the popular [Titanic dataset competition](https://www.kaggle.com/competitions/titanic) everyone started with).

- [Code example](https://www.kaggle.com/code/wissams/titanic-competition-step-by-step-using-xgboost/) on Kaggle

![Titanic Kaggle screenshot](https://sebastianraschka.com/images/blog/2025/hello-world-ai/2.webp)

The popular [Titanic Kaggle competition](https://www.kaggle.com/competitions/titanic)

**2017: MLPs on MNIST**

Multilayer perceptrons (MLPs) have been around for a looong time. They became somewhat practical in the 1980s and 90s after the [1986 backpropagation paper](https://www.nature.com/articles/323533a0), but they weren’t super popular. I remember that the early 2010s were still dominated by random forests, support vector machines, and gradient boosting (specifically XGBoost). And in the meantime, non-neural network-based methods remained popular in computer vision. However, with the initial release of [TensorFlow](https://www.tensorflow.org) in 2015, and TensorFlow 1.0 in 2017, MLPs and neural networks in general really picked up steam around that time.

- [Code example](https://github.com/rasbt/deeplearning-models/blob/master/tensorflow1_ipynb/mlp/mlp-basic.ipynb) from my deep learning notebook collection

![backprop and MNIST](https://sebastianraschka.com/images/blog/2025/hello-world-ai/3.webp)

Figures from my [2015 Python Machine Learning book](https://amzn.to/3KnXunE)

**2019: AlexNet on CIFAR-10**

AlexNet should probably come earlier in this list, since it was introduced in 2012 via the [ImageNet Classification with Deep Convolutional Neural Networks](https://proceedings.neurips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf) paper. However, it also didn’t become super popular until PyTorch and TensorFlow 1.0 were released in 2017. Most people were still using Caffe at the time, but there was also a shift to TensorFlow for computer vision.

Still, since it required GPUs to do any meaningful work with convolutional neural networks, which CUDA and cuDNN made more accessible, I think that putting it after the “2017 MPLPs on MNIST” example seems fair. (Also, ImageNet was way too large and expensive for most people at the time, so [CIFAR-10 and CIFAR-100](https://www.cs.toronto.edu/~kriz/cifar.html) were popular beginner datasets.)

- [Code example](https://github.com/rasbt/deeplearning-models/blob/master/pytorch_ipynb/cnn/cnn-alexnet-cifar10.ipynb) from my deep learning notebook collection

![Alexnext architecture](https://sebastianraschka.com/images/blog/2025/hello-world-ai/4.webp)

AlexNet architecture from the [AlexNet paper](https://papers.nips.cc/paper_files/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html)

**2021: DistilBERT on IMDb movie reviews**

[DistilBERT](https://arxiv.org/abs/1910.01108) on the [IMDb movie reviews sentiment classification dataset](https://ai.stanford.edu/~amaas/data/sentiment/) gets us to the era where language models started to pick up steam. Sure, the Transformer architecture was introduced in 2017, BERT in 2018, and DistilBERT in 2019, but it still took a few years for it to become popular.

- [Code example](https://github.com/rasbt/deeplearning-models/blob/master/pytorch_ipynb/transformer/distilbert-hf-finetuning.ipynb) from my deep learning notebook collection

![Ways to pretrain an LLM classifier](https://sebastianraschka.com/images/blog/2025/hello-world-ai/5.webp)

Ways to finetune pretrained transformers like DistilBERT as a classifier (from my [Finetuning Large Language Models](https://magazine.sebastianraschka.com/p/finetuning-large-language-models) article)

**2023: Llama 2 with LoRA on Alpaca 50k**

2023 was the year after the launch of ChatGPT, and LLMs picked up steam very quickly. There was still a big barrier due to the cost of training or fine-tuning LLMs, but the combination of [LoRA](https://arxiv.org/abs/2106.09685), [Llama 1 and 2](https://arxiv.org/abs/2307.09288), and the [Alpaca dataset](https://crfm.stanford.edu/2023/03/13/alpaca.html) made LLMs suddenly much more accessible, and there was a huge boom in instruction fine-tuning.

- [Code example](https://gist.github.com/radekosmulski/c3cce1a52b52b9b2037e1941de5afa32) by Radek Osmulski on GitHub

![Llama 2 architecture versus GPT](https://sebastianraschka.com/images/blog/2025/hello-world-ai/6.webp)

Llama 2 architecture from my [GPT to Llama conversion guide](https://github.com/rasbt/LLMs-from-scratch/blob/main/ch05/07_gpt_to_llama)

**2025: Qwen3 with RLVR on MATH-500**

Now, this year is the year of reasoning models and [reinforcement learning with verifiable rewards](https://magazine.sebastianraschka.com/p/understanding-reasoning-llms) (RLVR), which was kick-started with some hype around the first [OpenAI o1 release](https://openai.com/index/learning-to-reason-with-llms/) in 2024, but then really picked up steam in January 2025 with the release of [DeepSeek R1](https://arxiv.org/abs/2501.12948).

This year, [Qwen3 models](https://huggingface.co/collections/Qwen/qwen3) have also become super popular, and they come in many sizes from 0.6B to 235B. However, training a [reasoning model](https://sebastianraschka.com/glossary/#reasoning-model "Reasoning Model") with RLVR is still not trivial, even for the smallest model on the training portion of the [MATH-500](https://huggingface.co/datasets/HuggingFaceH4/MATH-500) dataset (that’s essentially the topic of my [new book](https://mng.bz/Nwr7)).

However, proprietary API services exist to showcase to a beginner what RLVR is, so it may be a good “Hello World” example and intro to AI (before the beginners want to dive into further details.)

- [Code example](https://github.com/thinking-machines-lab/tinker-cookbook/tree/main/tinker_cookbook/recipes/math_rl) from the Tinker API Cookbook (I am not affiliated with this company but think this is a good, fast intro example); from-scratch implementation to be added soon in my [reasoning from scratch book](https://github.com/rasbt/reasoning-from-scratch).

![Reasoning model training](https://sebastianraschka.com/images/blog/2025/hello-world-ai/7.webp)

Figure from my [The State of Reinforcement Learning for LLM Reasoning](https://magazine.sebastianraschka.com/p/the-state-of-llm-reasoning-model-training) article.
