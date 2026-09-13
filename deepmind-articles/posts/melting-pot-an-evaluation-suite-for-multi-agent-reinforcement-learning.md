---
title: "Melting Pot: an evaluation suite for multi-agent reinforcement learning"
source: https://deepmind.google/blog/melting-pot-an-evaluation-suite-for-multi-agent-reinforcement-learning/
site: deepmind
date: 2021-07-14
authors: Joel Leibo, Edgar Duéñez-Guzmán, Alexander Vezhnevets, John Agapiou, Peter Sunehag, Raphael Koster, Jayd Matyas, Charlie Beattie, Igor Mordatch, Thore Graepel
crawled: 2026-09-13
---

Technology deployed in the real world inevitably faces unforeseen challenges. These challenges arise because the environment where the technology was developed differs from the environment where it will be deployed. When a technology transfers successfully we say it generalises. In a multi-agent system, such as autonomous vehicle technology, there are two possible sources of generalisation difficulty: (1) physical-environment variation such as changes in weather or lighting, and (2) social-environment variation: changes in the behaviour of other interacting individuals. Handling social-environment variation is at least as important as handling physical-environment variation, however it has been much less studied.

As an example of a social environment, consider how self-driving cars interact on the road with other cars. Each car has an incentive to transport its own passenger as quickly as possible. However, this competition can lead to poor coordination (road congestion) that negatively affects everyone. If cars work cooperatively, more passengers might get to their destination more quickly. This conflict is called a social dilemma.

However, not all interactions are social dilemmas. For instance, there are synergistic interactions in open-source software, there are zero-sum interactions in sports, and coordination problems are at the core of supply chains. Navigating each of these situations requires a very different approach.

Multi-agent reinforcement learning provides tools that allow us to explore how artificial agents may interact with one another and with unfamiliar individuals (such as human users). This class of algorithms is expected to perform better when tested for their social generalisation abilities than others. However, until now, there has been no systematic evaluation benchmark for assessing this.

![Diagram illustrating the Melting Pot evaluation process: agents are trained on a MARL "substrate" consisting of familiar blue circle agents, and then evaluated on novel "test scenarios" (zero shot transfer) where they must interact in different proportions with unfamiliar red diamond agents.](https://lh3.googleusercontent.com/EG-5AeaSc16rfhRTx0PBuzB4K5vRj1_5wmdUTWdwJLTt90Kb1iw7EmQWudLCB3ZmZbHgmq3f4h12PGnSLpzTcmjpw3QC6XujYIqiF-bAKmoX3Tbp6dc=w1440)

Blue: focal populations of trained agents, Red: background population of pre-trained bots

Here we introduce Melting Pot, a scalable evaluation suite for multi-agent reinforcement learning. Melting Pot assesses generalization to novel social situations involving both familiar and unfamiliar individuals, and has been designed to test a broad range of social interactions such as: cooperation, competition, deception, reciprocation, trust, stubbornness and so on. Melting Pot offers researchers a set of 21 MARL “substrates” (multi-agent games) on which to train agents, and over 85 unique test scenarios on which to evaluate these trained agents. The performance of agents on these held-out test scenarios quantifies whether agents:

- Perform well across a range of social situations where individuals are interdependent,
- Interact effectively with unfamiliar individuals not seen during training,
- Pass a universalisation test: answering positively to the question "what if everyone behaved like that?''

The resulting score can then be used to rank different multi-agent RL algorithms by their ability to generalise to novel social situations.

![A matrix table mapping 21 different MARL "Substrates" (such as Capture the Flag and Clean Up) against various "Properties of game" and "Properties of potential solutions" (such as symmetric roles, temporal coordination, reciprocity, and trust) to show how each game is categorized.](https://lh3.googleusercontent.com/AtZHNXW6fNLGXBFEKoUnvturb_ay6pmefHTsU3Em5difedVaQT1le8X9Ftgf31v7avCla9WrzdmQooZq0M2FcNf97yaiJE09NXQ_sLYCehrr-MH0=w1440)

We hope Melting Pot will become a standard benchmark for multi-agent reinforcement learning. We plan to maintain it, and will be extending it in the coming years to cover more social interactions and generalisation scenarios.

Learn more from our [GitHub page](https://github.com/deepmind/meltingpot).
