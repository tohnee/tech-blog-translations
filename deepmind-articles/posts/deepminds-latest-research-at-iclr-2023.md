---
title: "DeepMind’s latest research at ICLR 2023"
source: https://deepmind.google/blog/deepminds-latest-research-at-iclr-2023/
site: deepmind
date: 2023-04-27
authors: 
crawled: 2026-09-13
---

Research towards AI models that can generalise, scale, and accelerate science

Next week marks the start of the 11th [International Conference on Learning Representations](https://iclr.cc/) (ICLR), taking place 1-5 May in Kigali, Rwanda. This will be the first major artificial intelligence (AI) conference to be hosted in Africa and the first in-person event since the start of the pandemic.

Researchers from around the world will gather to share their cutting-edge work in deep learning spanning the fields of AI, statistics and data science, and applications including machine vision, gaming and robotics. We’re proud to support the conference as a Diamond sponsor and DEI champion.

Teams from across DeepMind are presenting 23 papers this year. Here are a few highlights:

## Open questions on the path to AGI

Recent progress has shown AI’s incredible performance in text and image, but more research is needed for systems to generalise across domains and scales. This will be a crucial step on the path to developing artificial general intelligence (AGI) as a transformative tool in our everyday lives.

We present a new approach where models [learn by solving two problems in one](https://openreview.net/pdf?id=hhvkdRdWt1F). By training models to look at a problem from two perspectives at the same time, they learn how to reason on tasks that require solving similar problems, which is beneficial for generalisation. We also explored the [capability of neural networks to generalise](https://openreview.net/pdf?id=WbxHAzkeQcn) by comparing them to the Chomsky hierarchy of languages. By rigorously testing 2200 models across 16 different tasks, we uncovered that certain models struggle to generalise, and found that augmenting them with external memory is crucial to improve performance.

Another challenge we tackle is how to [make progress on longer-term tasks at an expert-level](https://openreview.net/pdf?id=sKc6fgce1zs), where rewards are few and far between. We developed a new approach and open-source training data set to help models learn to explore in human-like ways over long time horizons.

## Innovative approaches

As we develop more advanced AI capabilities, we must ensure current methods work as intended and efficiently for the real world. For example, although language models can produce impressive answers, many cannot explain their responses. We introduce a [method for using language models to solve multi-step reasoning problems](https://openreview.net/pdf?id=3Pf3Wg6o-A4) by exploiting their underlying logical structure, providing explanations that can be understood and checked by humans. On the other hand, adversarial attacks are a way of probing the limits of AI models by pushing them to create wrong or harmful outputs. Training on adversarial examples makes models more robust to attacks, but can come at the cost of performance on 'regular' inputs. We show that by adding adapters, we can create [models that allow us to control this tradeoff](https://openreview.net/pdf?id=HPdxC1THU8T) on the fly.

Reinforcement learning (RL) has proved successful for a range of [real-world challenges](https://www.deepmind.com/blog-categories/applied), but RL algorithms are usually designed to do one task well and struggle to generalise to new ones. We propose [algorithm distillation](https://openreview.net/pdf?id=hy0a5MMPUv), a method that enables a single model to efficiently generalise to new tasks by training a transformer to imitate the learning histories of RL algorithms across diverse tasks. RL models also learn by trial and error which can be very data-intensive and time-consuming. It took nearly 80 billion frames of data for our model [Agent 57](https://deepmind.google/blog/agent57-outperforming-the-human-atari-benchmark/) to reach human-level performance across 57 Atari games. We share a new way to [train to this level using 200 times less experience](https://openreview.net/pdf?id=JtC6yOHRoJJ), vastly reducing computing and energy costs.

## AI for science

AI is a powerful tool for researchers to analyse vast amounts of complex data and understand the world around us. Several papers show how AI is accelerating scientific progress – and how science is advancing AI.

Predicting a molecule's properties from its 3D structure is critical for drug discovery. We present [a denoising method](https://openreview.net/pdf?id=tYIMtogyee) that achieves a new state-of-the-art in molecular property prediction, allows large-scale pre-training, and generalises across different biological datasets. We also introduce a new [transformer which can make more accurate quantum chemistry calculations](https://openreview.net/pdf?id=xveTeHVlF7j%E2%80%9D) using data on atomic positions alone.

Finally, with [FIGnet](https://openreview.net/pdf?id=J7Uh781A05p), we draw inspiration from physics to model collisions between complex shapes, like a teapot or a doughnut. This simulator could have applications across robotics, graphics and mechanical design.

See the full list of [DeepMind papers and schedule of events at ICLR 2023](https://deepmind.events/events/iclr-2023/resources).
