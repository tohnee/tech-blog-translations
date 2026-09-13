---
title: "Prefrontal cortex as a meta-reinforcement learning system"
source: https://deepmind.google/blog/prefrontal-cortex-as-a-meta-reinforcement-learning-system/
site: deepmind
date: 2018-05-14
authors: Jane Wang, Zeb Kurth-Nelson, Matt Botvinick
crawled: 2026-09-13
---

Recently, AI systems have mastered a range of video-games such as Atari classics Breakout and Pong. But as impressive as this performance is, AI still relies on the equivalent of thousands of hours of gameplay to reach and surpass the performance of human video game players. In contrast, we can usually grasp the basics of a video game we have never played before in a matter of minutes.

The question of why the brain is able to do so much more with so much less has given rise to the theory of meta-learning, or ‘learning to learn’. It is thought that we learn on two timescales — in the short term we focus on learning about specific examples while over longer timescales we learn the abstract skills or rules required to complete a task. It is this combination that is thought to help us learn efficiently and apply that knowledge rapidly and flexibly on new tasks. Recreating this meta-learning structure in AI systems — called meta-reinforcement learning — has proven very fruitful in facilitating fast, one-shot, learning in our agents (see [our paper](https://arxiv.org/abs/1611.05763) and closely related [work](https://arxiv.org/abs/1611.02779) from OpenAI). However, the specific mechanisms that allow this process to take place in the brain are still largely unexplained in neuroscience.

In [our new paper](https://www.nature.com/articles/s41593-018-0147-8) in Nature Neuroscience (Download a [PDF here](https://www.biorxiv.org/content/early/2018/04/06/295964)), we use the meta-reinforcement learning framework developed in AI research to investigate the role of dopamine in the brain in helping us to learn. Dopamine—commonly known as the brain’s pleasure signal—has often been thought of as analogous to the reward prediction error signal used in AI reinforcement learning algorithms. These systems learn to act by trial and error guided by the reward. We propose that dopamine’s role goes beyond just using reward to learn the value of past actions and that it plays an integral role, specifically within the prefrontal cortex area, in allowing us to learn efficiently, rapidly and flexibly on new tasks.

We tested our theory by virtually recreating six meta-learning experiments from the field of neuroscience—each requiring an agent to perform tasks that use the same underlying principles (or set of skills) but that vary in some dimension. We trained a recurrent neural network (representing the prefrontal cortex) using standard deep reinforcement learning techniques (representing the role of dopamine) and then compared the activity dynamics of the recurrent network with real data taken from previous findings in neuroscience experiments. Recurrent networks are a good proxy for meta-learning because they are able to internalise past actions and observations and then draw on those experiences while training on a variety of tasks.

One experiment we recreated is known as the Harlow Experiment, a psychology test from the 1940s used to explore the concept of meta-learning. In the original test, a group of monkeys were shown two unfamiliar objects to select from, only one of which gave them a food reward. They were shown these two objects six times, each time the left-right placement was randomised so the monkey had to learn which object gave a food reward. They were then shown two brand new objects, again only one would result in a food reward. Over the course of this training, the monkey developed a strategy to select the reward associated-object: it learnt to select randomly the first time, and then based on the reward feedback to choose the particular object, rather than the left or right position, from then on. The experiment shows that monkeys could internalise the underlying principles of the task and learn an abstract rule structure — in effect, learning to learn.

When we simulated a very similar test using a [virtual computer screen](https://deepmind.com/blog/article/open-sourcing-psychlab) and randomly selected images, we found that our ‘meta-RL agent’ appeared to learn in a manner analogous to the animals in the Harlow Experiment, even when presented with entirely new images never seen before.

![An animated GIF showing a virtual simulation of the Harlow Experiment on a computer screen, where an AI agent chooses between two images to receive a reward.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62268a061ec09bdecce13dbd_MetaRL.gif)

In our virtual recreation of the Harlow Experiment, the agent must shift its gaze towards the object it thinks is associated with a reward.

In fact, we found that the meta-RL agent could learn to quickly adapt in a wide domain of tasks with different rules and structures. And because the network learned how to adapt to a variety of tasks, it also learned general principles about how to learn efficiently.

Importantly, we saw that the majority of learning took place in the recurrent network, which supports our proposal that dopamine plays a more integral role in the meta-learning process than previously thought. Dopamine is traditionally understood to strengthen synaptic links in the prefrontal system, reinforcing particular behaviours. In AI, this means the dopamine-like reward signal adjusts the artificial synaptic weights in a neural network as it learns the right way to solve a task. However, in our experiments the weights of the neural network were frozen, meaning they couldn’t be adjusted during the learning process, yet, the meta-RL agent was still able to solve and adapt to new tasks. This shows us that dopamine-like reward isn't only used to adjust weights, but it also conveys and encodes important information about abstract task and rule structure, allowing faster adaptation to new tasks.

Neuroscientists have long observed similar patterns of neural activations in the prefrontal cortex, which is quick to adapt and flexible, but have struggled to find an adequate explanation for why that’s the case. The idea that the prefrontal cortex isn’t relying on slow synaptic weight changes to learn rule structures, but is using abstract model-based information directly encoded in dopamine, offers a more satisfactory reason for its versatility.

In demonstrating that the key ingredients thought to give rise to meta-reinforcement learning in AI also exist in the brain, we’ve posed a theory that not only fits with what is known about both dopamine and prefrontal cortex but that also explains a range of mysterious findings from neuroscience and psychology. In particular, the theory sheds new light on how structured, model-based learning emerges in the brain, why dopamine itself contains model-based information, and how neurons in the prefrontal cortex become tuned to learning-related signals. Leveraging insights from AI which can be applied to explain findings in neuroscience and psychology highlights the value each field can offer the other. Going forward, we anticipate that much benefit can be gained in the reverse direction, by taking guidance from specific organisation of brain circuits in designing new models for learning in reinforcement learning agents.

**Notes**

Download the Nature Neuroscience paper [here](https://www.nature.com/articles/s41593-018-0147-8).

Download an Open Access version of the paper [here](https://www.biorxiv.org/content/early/2018/04/06/295964).

This work was completed by Jane X. Wang, Zeb Kurth-Nelson, Dharshan Kumaran, Dhruva Tirumala, Hubert Soyer, Joel Z. Leibo, Demis Hassabis and Matthew Botvinick.
