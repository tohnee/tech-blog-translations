---
title: "DeepMind’s latest research at ICLR 2022"
source: https://deepmind.google/blog/deepminds-latest-research-at-iclr-2022/
site: deepmind
date: 2022-04-25
authors: 
crawled: 2026-09-13
---

Working toward greater generalisability in artificial intelligence

Today, conference season is kicking off with The Tenth International Conference on Learning Representations ([ICLR 2022](https://iclr.cc/)), running virtually from 25-29 April, 2022. Participants from around the world are gathering to share their cutting-edge work in representational learning, from advancing the state of the art in artificial intelligence to data science, machine vision, robotics, and more.

On the first day of the conference, Pushmeet Kohli, our head of AI for Science and Robust and Verified AI teams, is delivering a talk on how AI can dramatically improve solutions to a wide range of scientific problems, from genomics and structural biology to quantum chemistry and even pure mathematics.

Beyond supporting the event as sponsors and regular workshop organisers, our research teams are presenting 29 papers, including 10 collaborations this year. Here’s a brief glimpse into our upcoming oral, spotlight, and poster presentations:

## Optimising learning

A number of key papers focus on the critical ways we’re making the learning process of our AI systems more efficient. This ranges from increasing performance, advancing few shot learning, and creating data efficient systems that reduce computational costs.

In [“Bootstrapped meta-learning”](https://openreview.net/forum?id=b-ny3x071E5), an [ICLR 2022 Outstanding Paper Award](https://blog.iclr.cc/2022/04/20/announcing-the-iclr-2022-outstanding-paper-award-recipients/) winner, we propose an algorithm that enables an agent to learn how to learn by teaching itself. We also present a [policy improvement algorithm](https://openreview.net/forum?id=bERaNdoegnO) that redesigns [AlphaZero](https://deepmind.google/blog/alphazero-shedding-new-light-on-chess-shogi-and-go/) – our system that taught itself from scratch to master chess, shogi, and Go – to continue improving even when training with a small number of simulations; a [regulariser that mitigates the risk of capacity loss](https://openreview.net/forum?id=ZkC8wKoLbQ7) in a broad range of RL agents and environments; and an improved [architecture to efficiently train attentional models](https://openreview.net/forum?id=sRZ3GhmegS).

## Exploration

Curiosity is a key part of human learning, helping to advance knowledge and skill. Similarly, exploration mechanisms allow AI agents to go beyond preexisting knowledge and discover the unknown or try something new.

Advancing the question “[When should agents explore?](https://openreview.net/forum?id=dEwfxt14bca)”, we investigate when agents should switch into exploration mode, at what timescales it makes sense to switch, and which signals best determine how long and frequent exploration periods should be. In another paper, we introduce an “[information gain exploration bonus](https://openreview.net/forum?id=cU8rknuhxc)” that allows agents to break out of the limitations of intrinsic rewards in RL to be able to learn more skills.

## Robust AI

To deploy ML models in the real world, they must be effective when shifting between training, testing, and across new datasets. Understanding the causal mechanisms is essential, allowing some systems to adapt, while others struggle to face new challenges.

Expanding the research into these mechanisms, we present an experimental framework that enables a fine-grained [analysis of robustness to distribution shifts](https://openreview.net/forum?id=Dl4LetuLdyK). Robustness also helps protect against adversarial harms, whether unintended or targeted. In the case of image corruptions, we propose a technique that theoretically [optimises the parameters of image-to-image models](https://openreview.net/forum?id=jJOjjiZHy3h) to decrease the effects of blurring, fog, and other common issues.

## Emergent communication

In addition to helping ML researchers understand how agents evolve their own communication to complete tasks, AI agents have the potential to reveal insights into linguistic behaviours within populations, which could lead to more interactive and useful AI.

Working with researchers at Inria, Google Research, and Meta AI, we connect the role of diversity within human populations on shaping language to [partially solve an apparent contradiction](https://openreview.net/forum?id=5Qkd7-bZfI) in computer simulations with neural agents. Then, because building better representations of language in AI is so vital to understanding emergent communication, we also investigate the [importance of scaling up](https://openreview.net/forum?id=AUGBfDIV9rL) the dataset, task complexity, and population size as independent aspects. Moreover, we also studied the [tradeoffs of expressivity, complexity, and unpredictability](https://openreview.net/forum?id=WxuE_JWxjkW) in games where multiple agents communicate to achieve a single goal.

See the full range of our work at ICLR 2022 [here](https://deepmind.events/events/iclr-2022).
