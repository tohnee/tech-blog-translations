---
title: "Enabling Continual Learning in Neural Networks"
source: https://deepmind.google/blog/enabling-continual-learning-in-neural-networks/
site: deepmind
date: 2017-03-13
authors: James Kirkpatrick, Razvan Pascanu, Neil Rabinowitz, Joel Veness, Guillaume Desjardins, Andrei Rusu, Kieran Milan, John Quan, Tiago Ramalho, Agnieszka Grabska-Barwinska, Demis Hassabis, Dharshan Kumaran, Raia Hadsell, Claudia Clopath
crawled: 2026-09-13
---

Computer programs that learn to perform tasks also typically forget them very quickly. We show that the learning rule can be modified so that a program can remember old tasks when learning a new one. This is an important step towards more intelligent programs that are able to learn progressively and adaptively.

Deep neural networks are currently the most successful machine learning technique for solving a variety of tasks including language translation, image classification and image generation. However, they have typically been designed to learn multiple tasks only if the data is presented all at once. As a network trains on a particular task its parameters are adapted to solve the task. When a new task is introduced, new adaptations overwrite the knowledge that the neural network had previously acquired. This phenomenon is known in cognitive science as ‘catastrophic forgetting’, and is considered one of the fundamental limitations of neural networks.

By contrast, our brains work in a very different way. We are able to learn incrementally, acquiring skills one at a time and applying our previous knowledge when learning new tasks. As a starting point for our recent [PNAS paper](http://www.pnas.org/content/early/2017/03/13/1611835114.abstract), in which we propose an approach to overcome catastrophic forgetting in neural networks, we took inspiration from neuroscience-based theories about the consolidation of previously acquired skills and memories in mammalian and human brains.

Neuroscientists have distinguished two kinds of consolidation that occur in the brain: systems consolidation and synaptic consolidation. Systems consolidation is the process by which memories that have been acquired by the quick-learning parts of our brain are imprinted into the slow-learning parts. This imprinting is known to be mediated by conscious and unconscious recall - for instance, this can happen during dreaming. In the second mechanism, synaptic consolidation, connections between neurons are less likely to be overwritten if they have been important in previously learnt tasks. Our algorithm specifically takes inspiration from this mechanism to address the problem of catastrophic forgetting.

A neural network consists of several connections in much the same way as a brain. After learning a task, we compute how important each connection is to that task. When we learn a new task, each connection is protected from modification by an amount proportional to its importance to the old tasks. Thus it is possible to learn the new task without overwriting what has been learnt in the previous task and without incurring a significant computational cost. In mathematical terms, we can think of the protection we attach to each connection in a new task as being linked to the old protection value by a spring, whose stiffness is proportional to the connection’s importance. For this reason, we called our algorithm Elastic Weight Consolidation (EWC).

![An animated diagram illustrating Elastic Weight Consolidation (EWC) in a neural network learning Task A and Task B sequentially. Solid lines show important connection weights for Task A being protected and maintained while new connections are formed for Task B.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62229423100cfeaf511d88da_Enabling20Continual20Learning20in20Neural20Networ.gif)

Illustration of the learning process for two tasks using EWC

To test our algorithm, we exposed an agent to Atari games sequentially. Learning an individual game from the score alone is a challenging task, but learning multiple games sequentially is even more challenging as each game requires an individual strategy. As shown in the figure below, without EWC, the agent quickly forgets each game after it stops playing it (blue). This means that on average, the agent barely learns a single game. However, if we use EWC (brown and red), the agent does not forget as easily and can learn to play several games, one after the other.

![Line graph showing total normalized score over training time (million frames) for sequentially trained Atari games. The "no penalty" method (blue line) remains flat near 0, showing catastrophic forgetting. "EWC + task oracle" (brown) and "EWC + FMN" (red) show steadily increasing scores up to 500 million frames as more games are protected, shown in the step-graph below.](https://lh3.googleusercontent.com/z4f0nbMAdAzE2vIrftw2uq4_iJP-LCsg_Ks_xqWNnCvFssPjfDoKCBraMXsPxFcvR5WCcvXU4QTDYfGpZGGZ6AeQsMSQgIFgya2JPfxBc8zwgCsJP-c=w1440)

Today, computer programs cannot learn from data adaptively and in real time. However, we have shown that catastrophic forgetting is not an insurmountable challenge for neural networks. We hope that this research represents a step towards programs that can learn in a more flexible and efficient way.

Our research also progresses our understanding of how consolidation happens in the human brain. The neuroscientific theories that our work is based on, in fact, have mainly been proven in very simple examples. By showing that those same theories can be applied in a more realistic and complex machine learning context, we hope to give further weight to the idea that synaptic consolidation is key to retaining memories and know-how.

![An abstract illustration of a human brain containing a retro video game maze, symbolizing the intersection of neuroscience-inspired memory consolidation and continual machine learning in neural networks.](https://lh3.googleusercontent.com/RHT3VlM6p9C29oMKNfblDgBC30fvGBNNjwvJY3LPcNHRHm1RYApbhFrbNXAf9Tg4lNzI3sVC16TAG1scmY4N05yZC3T2KoNVVmR9SGMhBl28zsOzmw=w1440)

**Notes**

Read the paper: [Overcoming catastrophic forgetting in neural networks](https://www.pnas.org/doi/abs/10.1073/pnas.1611835114)
