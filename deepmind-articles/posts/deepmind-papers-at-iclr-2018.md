---
title: "DeepMind papers at ICLR 2018"
source: https://deepmind.google/blog/deepmind-papers-at-iclr-2018/
site: deepmind
date: 2018-04-26
authors: 
crawled: 2026-09-13
---

**Between 30 April and 03 May, hundreds of researchers and engineers will gather in Vancouver, Canada, for the** [**Sixth International Conference on Learning Representations.**](https://iclr.cc/)

Here you can read details of all DeepMind’s accepted papers and find out where you can see the accompanying poster sessions and talks.


### Maximum a posteriori policy optimisation

**Authors:** Abbas Abdolmaleki, Jost Tobias Springenberg, Nicolas Heess, Yuval Tassa, Remi Munos

We introduce a new algorithm for reinforcement learning called Maximum a posteriori Policy Optimisation (MPO) based on coordinate ascent on a relative entropy objective. We show that several existing methods can directly be related to our derivation. We develop two off-policy algorithms and demonstrate that they are competitive with the state-of-the-art in deep reinforcement learning. In particular, for continuous control, our method outperforms existing methods with respect to sample efficiency, premature convergence and robustness to hyperparameter settings.

- Read the [paper](https://openreview.net/forum?id=S1ANxQW0b)
- Check out the poster at East Meeting level; 1,2,3 from 1100 to 1300

### Hierarchical representations for efficient architecture search

**Authors:** Hanxiao Liu (CMU), Karen Simonyan, Oriol Vinyals, Chrisantha Fernando, Koray Kavukcuoglu

We explore efficient neural architecture search methods and show that a simple yet powerful evolutionary algorithm can discover new architectures with excellent performance. Our approach combines a novel hierarchical genetic representation scheme that imitates the modularized design pattern commonly adopted by human experts, and an expressive search space that supports complex topologies. Our algorithm efficiently discovers architectures that outperform a large number of manually designed models for image classification, obtaining top-1 error of 3.6% on CIFAR-10 and 20.3% when transferred to ImageNet, which is competitive with the best existing neural architecture search approaches. We also present results using random search, achieving 0.3% less top-1 accuracy on CIFAR-10 and 0.1% less on ImageNet whilst reducing the search time from 36 hours down to 1 hour.

- Read the [paper](https://arxiv.org/abs/1711.00436)
- Check out the poster at East Meeting level; 1,2,3 from 1100 to 1300

### Learning an embedding space for transferable robot skills

**Authors:** Karol Hausman, Jost Tobias Springenberg, Ziyu Wang, Nicolas Heess, Martin Riedmiller

We present a method for reinforcement learning of closely related skills that are parameterized via a skill embedding space. We learn such skills by taking advantage of latent variables and exploiting a connection between reinforcement learning and variational inference.

The main contribution of our work is an entropy-regularized policy gradient formulation for hierarchical policies, and an associated, data-efficient and robust off-policy gradient algorithm based on stochastic value gradients. We demonstrate the effectiveness of our method on several simulated robotic manipulation tasks.

- Read the [paper](https://openreview.net/forum?id=rk07ZXZRb)
- Check out the poster at East Meeting level; 1,2,3 from 1100 to 1300

### Learning awareness models

**Authors:** Brandon Amos, Laurent Dinh, Serkan Cabi, Thomas Rothörl, Sergio Gómez Colmenarejo, Alistair M Muldal, Tom Erez, Yuval Tassa, Nando de Freitas, Misha Denil

We show that models trained to predict proprioceptive information about an agent's body come to represent objects in the external world. The models able to successfully predict sensor readings over 100 steps into the future and continue to represent the shape of external objects even after contact is lost. We show that active data collection by maximizing uncertainty over future sensor readings leads to models that show superior performance when used for control. We also collect data from a real robotic hand and show that the same models can be used to answer questions about the properties of objects in the real world.

- Read the [paper](https://openreview.net/forum?id=r1HhRfWRZ)
- Check out the poster at East Meeting level; 1,2,3 from 1100 to 1300

### Kronecker-factored curvature approximations for recurrent neural networks

**Authors:** James Martens, Jimmy Ba (Vector Institute), Matthew Johnson (Google)

Kronecker-factor Approximate Curvature (Martens & Grosse, 2015) (K-FAC) is a 2nd-order optimization method which has been shown to give state-of-the-art performance on large-scale neural network optimization tasks (Ba et al., 2017). It is based on an approximation to the Fisher information matrix (FIM) that makes assumptions about the particular structure of the network and the way it is parameterized. The original K-FAC method was applicable only to fully-connected networks, although it has been recently extended by Grosse & Martens (2016) to handle convolutional networks as well. In this work we extend the method to handle RNNs by introducing a novel approximation to the FIM for RNNs. This approximation works by modelling the covariance structure between the gradient contributions at different time-steps using a chain-structured linear Gaussian graphical model, summing the various cross-covariances, and computing the inverse in closed form. We demonstrate in experiments that our method significantly outperforms general purpose state-of-the-art optimizers like SGD with momentum and Adam on several challenging RNN training tasks.

- Read the [paper](https://openreview.net/forum?id=HyMTkQZAb¬eId=HkIsQkpSG)
- Check out the poster at East Meeting level; 1,2,3 from 1100 to 1300

### Distributed distributional deterministic policy gradients

**Authors:** Gabriel Barth-maron, Matthew Hoffman, David Budden, Will Dabney, Daniel Horgan, Dhruva Tirumala Bukkapatnam, Alistair M Muldal, Nicolas Heess, Timothy Lillicrap

This work adopts the very successful distributional perspective on reinforcement learning and adapts it to the continuous control setting. We combine this within a distributed framework for off-policy learning in order to develop what we call the Distributed Distributional Deep Deterministic Policy Gradient algorithm, D4PG. We also combine this technique with a number of additional, simple improvements such as the use of N-step returns and prioritized experience replay. Experimentally we examine the contribution of each of these individual components, and show how they interact, as well as their combined contributions. Our results show that across a wide variety of simple control tasks, difficult manipulation tasks, and a set of hard obstacle-based locomotion tasks the D4PG algorithm achieves state of the art performance.

- Read the [paper](https://openreview.net/forum?id=SyZipzbCb)
- Check out the poster at East Meeting level; 1,2,3 from 1630 to 1830

### The Kanerva Machine: A generative distributed memory

**Authors:** Yan Wu, Greg Wayne, Alex Graves, Timothy Lillicrap

We present an end-to-end trained memory system that quickly adapts to new data and generates samples like them. The memory is analytically tractable, which enables optimal on-line compression via a Bayesian update-rule. We formulate it as a hierarchical conditional generative model, where memory provides a rich data-dependent prior distribution. Consequently, the top-down memory and bottom-up perception are combined to produce the code representing an observation.

- Read the [paper](https://arxiv.org/abs/1804.01756)
- Check out the poster at East Meeting level; 1,2,3 from 1630 to 1830

### Memory-based parameter adaptation

**Authors:** Pablo Sprechmann, Siddhant Jayakumar, Jack Rae, Alexander Pritzel, Adria P Badia · Benigno Uria, Oriol Vinyals, Demis Hassabis, Razvan Pascanu, Charles Blundell

Humans and animals are able to incorporate new knowledge quickly from a few examples, continually throughout much of their lifetime. In contrast, neural network-based models rely on the data distribution being stationary and a gradual training procedure to obtain good generalisation. Drawing inspiration from the theory of complementary learning systems, we propose Memory-based Parameter Adaptation (MbPA), a method for augmenting neural networks with an episodic memory to allow for rapid acquisition of new knowledge while preserving the high performance and good generalisation of standard deep models. MbPA, stores examples in memory and then uses a context-based lookup to directly modify the weights of a neural network. It alleviates several shortcomings of neural networks, such as catastrophic forgetting, fast, stable acquisition of new knowledge, and fast learning during evaluation.

- Read the [paper](https://arxiv.org/abs/1802.10542)
- Check out the poster at East Meeting level; 1,2,3 from 1630 to 1830


### SCAN: Learning hierarchical compositional visual concepts

**Authors:** Irina Higgins, Nicolas Sonnerat, Loic Matthey, Arka Pal, Christopher P Burgess, Matko Bošnjak, Murray Shanahan, Matthew Botvinick, Alexander Lerchner

We propose a novel theoretical approach to address the problem of abstract compositionality - how can we learn a small number of grounded building blocks and use them to create a vast number of new abstract concepts on the fly? We present a new neural network architecture called the Symbol-Concept Association Network (SCAN), that can learn a grounded visual concept hierarchy, enabling it to imagine novel concepts guided by language instructions.

- Read [the blog in full.](https://deepmind.com/blog/article/imagine-creating-new-visual-concepts-recombining-familiar-ones)
- Read the [paper](https://arxiv.org/abs/1707.03389)
- Check out the poster at East Meeting level; 1,2,3 from 1100 to 1300

### Emergence of linguistic communication from referential games with symbolic and pixel input

**Authors:** Angeliki Lazaridou, Karl M Hermann, Karl Tuyls, Stephen Clark

The ability of algorithms to evolve or learn (compositional) communication protocols has traditionally been studied in the language evolution literature through the use of emergent communication tasks. Here we scale up this research by using contemporary deep learning methods and by training reinforcement-learning neural network agents on referential communication games. We extend previous work, in which agents were trained in symbolic environments, by developing agents which are able to learn from raw pixel data, a more challenging and realistic input representation. We find that the degree of structure found in the input data affects the nature of the emerged protocols, and thereby corroborate the hypothesis that structured compositional language is most likely to emerge when agents perceive the world as being structured.

- Read the [paper](https://openreview.net/pdf?id=HJGv1Z-AW)
- Check out the poster at East Meeting level; 1,2,3 from 1100 to 1300
- Attend the oral session on **Wednesday 02 May** in Exhibition Hall A from 1015 to 1030

### Many paths to equilibrium: GANs do not need to decrease a divergence at every step

**Authors:** William Fedus (Université de Montréal), Mihaela Rosca, Balaji Lakshminarayanan, Andrew Dai (Google), Shakir Mohamed, Ian Goodfellow (Google Brain)

The field of generative adversarial networks research has grown, fueled by the successes of their application in computer vision. In an attempt to solve training instability in generative adversarial networks, multiple theoretical justifications for training dynamics have been suggested and new training methods proposed. By focusing on the divergence minimization view of generative adversarial networks and regularizers such as gradient penalties, we empirically show that the success of some of these approaches cannot be solely explained by the accompanying underlying theory. This motivates the need for new theoretical framework that can encompass and explains the presented results.

- Read the [paper](https://arxiv.org/abs/1710.08446)
- Check out the poster at East Meeting level; 1,2,3 from 1630 to 1830

### Can neural networks understand logical entailment?

**Authors:** Richard Evans, David Saxton, David Amos, Pushmeet Kohli, Edward Grefenstette

We introduce a new dataset of logical entailments for the purpose of measuring models' ability to capture and exploit the structure of logical expressions against an entailment prediction task. We use this task to compare a series of architectures which are ubiquitous in the sequence-processing literature, in addition to a new model class–PossibleWorldNets–which computes entailment as a "convolution over possible worlds". Results show that convolutional networks present the wrong inductive bias for this class of problems relative to LSTM RNNs, tree-structured neural networks outperform LSTM RNNs due to their enhanced ability to exploit the syntax of logic, and PossibleWorldNets outperform all benchmarks.

- Read the [paper](https://openreview.net/forum?id=SkZxCk-0Z)
- Check out the poster at East Meeting level; 1,2,3 from 1630 to 1830

### Distributed prioritized experience replay

**Authors:** Daniel Horgan, John Quan, David Budden, Gabriel Barth-maron, Matteo Hessel, Hado van Hasselt, David Silver

We propose a distributed architecture for deep reinforcement learning at scale, that enables agents to learn effectively from orders of magnitude more data than previously possible. The algorithm decouples acting from learning: the actors interact with their own instances of the environment by selecting actions according to a shared neural network, and accumulate the resulting experience in a shared experience replay memory; the learner replays samples of experience and updates the neural network. The architecture relies on prioritized experience replay to focus only on the most significant data generated by the actors. Our architecture substantially improves the state of the art on the Arcade Learning Environment, achieving better final performance in a fraction of the wall-clock training time.

- Read the [paper](https://arxiv.org/abs/1803.00933)
- Check out the poster at East Meeting level; 1,2,3 from 1630 to 1830

### The Reactor: A fast and sample-efficient actor-critic agent for reinforcement learning

**Authors:** Audrunas Gruslys, Will Dabney, Mohammad Gheshlaghi Azar, Bilal Piot, Marc G Bellemare, Remi Munos

We propose multiple algorithmic and architectural improvements producing an agent with a higher sample-efficiency than Prioritized Dueling DQN and Categorical DQN, while giving better run-time performance than A3C. Distributional Retrace policy evaluation algorithm brings multi-step off-policy updates to the distributional reinforcement learning setting. Our approach can be used to convert several classes of multi-step policy evaluation algorithms into distributional ones. β-leave-one-out policy gradient algorithm uses action values as a baseline. A new prioritized replay algorithm exploits temporal locality for more efficient replay prioritization. Reactor reaches state-of-the-art performance after 200 million frames in less than a day.

- Read the [paper](https://arxiv.org/abs/1704.04651)
- Check out the poster at East Meeting level; 1,2,3 from 1630 to 1830

### Minimally Redundant Laplacian Eigenmaps

**Authors:** David Pfau, Christopher P Burgess

Spectral algorithms for learning low-dimensional data manifolds have largely been supplanted by deep learning methods in recent years. One reason is that classic spectral manifold learning methods often learn collapsed embeddings that do not fill the embedding space. We show that this is a natural consequence of data where different latent dimensions have dramatically different scaling in observation space. We present a simple extension of Laplacian Eigenmaps to fix this problem based on choosing embedding vectors which are both orthogonal and \textit{minimally redundant} to other dimensions of the embedding. In experiments on NORB and similarity-transformed faces we show that Minimally Redundant Laplacian Eigenmap (MR-LEM) significantly improves the quality of embedding vectors over Laplacian Eigenmaps, accurately recovers the latent topology of the data, and discovers many disentangled factors of variation of comparable quality to state-of-the-art deep learning methods.

- Read the [paper](https://iclr.cc/Conferences/2018/Schedule?showEvent=475)
- Check out the poster at East Meeting level; 1,2,3 from 1630 to 1830


### On the importance of single directions for generalization

**Authors:** Ari Morcos, David GT Barrett, Neil C Rabinowitz, Matthew Botvinick

Our investigation into the importance of single directions for generalisation...uses an approach inspired by decades of experimental neuroscience - exploring the impact of damage - to determine: how important are small groups of neurons in deep neural networks? Are more easily interpretable neurons also more important to the network’s computation? We measured the performance impact of damaging the network by deleting individual neurons as well as groups of neurons. Our experiments led to two surprising findings: 1. Although many previous studies have focused on understanding easily interpretable individual neurons (e.g. “cat neurons”, or neurons in the hidden layers of deep networks which are only active in response to images of cats), we found that these interpretable neurons are no more important than confusing neurons with difficult-to-interpret activity. 2. Networks which correctly classify unseen images are more resilient to neuron deletion than networks which can only classify images they have seen before. In other words, networks which generalise well are much less reliant on single directions than those which memorise.

- Read the [blog in full](https://deepmind.com/blog/article/understanding-deep-learning-through-neuron-deletion).
- Read the [paper](https://openreview.net/forum?id=r1iuQjxCZ¬eId=r1On1W5xf)
- Check out the poster at East Meeting level; 1,2,3 from 1100 to 1300

### Memory architectures in recurrent neural network language models

**Authors:** Dani Yogatama, Yishu Miao, Gábor Melis, Wang Ling, Adhiguna Kuncoro, Chris Dyer, Phil Blunsom

Generating fluent, grammatical language requires keeping track of what words have been generated in the past. In this paper, we compare three memory architectures (sequential, random access, and stack-based) and find that a stack-structured memory demonstrates the best performance in terms of held-out perplexity. To give the stack memory more power and better match the phenomena encountered in language, we introduce a generalization of existing differentiable stack memories enabling them to execute multiple pop operations at each timestep, which further improves performance. Finally, we show that our stack-augmented language model correctly learns to predict difficult long-range agreement patterns which are difficult for conventional LSTM language models.

- Read the [paper](https://openreview.net/forum?id=SkFqf0lAZ)
- Check out the poster at East Meeting level; 1,2,3 from 1100 to 1300

### Few-shot autoregressive density estimation: Towards learning to learn distributions

**Authors:** Scott Reed, Yutian Chen, Thomas Paine, Aaron van den Oord, S. M. Ali Eslami, Danilo J Rezende, Oriol Vinyals, Nando de Freitas

Current image density models require large amounts of data and computation time for training. In this paper, we show how 1) neural attention and 2) meta learning techniques can be used in combination with autoregressive models to enable effective few-shot density estimation. Our modified PixelCNNs result in state-of-the art few-shot density estimation on Omniglot. We visualize the learned attention policy and find that it learns intuitive algorithms for simple tasks such as image mirroring and digit drawing on Omniglot without supervision. Finally, we demonstrate few-shot image generation on the Stanford Online Products dataset.

- Read the [paper](https://arxiv.org/abs/1710.10304)
- Check out the poster at East Meeting level; 1,2,3 from 1100 to 1300

### On the state of the art of evaluation in neural language models

**Authors:** Gábor Melis, Chris Dyer, Phil Blunsom

Ongoing innovations in recurrent neural network architectures have provided a steady influx of apparently state-of-the-art results on language modelling benchmarks. However, these have been evaluated using differing code bases and limited computational resources, which represent uncontrolled sources of experimental variation. We reevaluate several popular architectures and regularisation methods with large-scale automatic black-box hyperparameter tuning and arrive at the somewhat surprising conclusion that standard LSTM architectures, when properly regularised, outperform more recent models. We establish a new state of the art on the Penn Treebank and Wikitext-2 corpora, as well as strong baselines on the Hutter Prize dataset.

- Read the [paper](https://arxiv.org/abs/1707.05589)
- Check out the poster at East Meeting level; 1,2,3 from 1100 to 1300

### Emergent communication through negotiation

**Authors:** Kris Cao, Angeliki Lazaridou, Marc Lanctot, Joel Z Leibo, Karl Tuyls, Stephen Clark

Multi-agent reinforcement learning offers a way to study how communication could emerge in communities of agents needing to solve specific problems. In this paper, we study the emergence of communication in the negotiation environment, a semi-cooperative model of agent interaction. We introduce two communication protocols – one grounded in the semantics of the game, and one which is a priori ungrounded and is a form of cheap talk. We show that self-interested agents can use the pre-grounded communication channel to negotiate fairly, but are unable to effectively use the ungrounded channel. However, prosocial agents do learn to use cheap talk to find an optimal negotiating strategy, suggesting that cooperation is necessary for language to emerge. We also study communication behaviour in a setting where one agent interacts with agents in a community with different levels of prosociality and show how agent identifiability can aid negotiation.

- Read the [paper](https://openreview.net/forum?id=Hk6WhagRW)
- Check out the poster at East Meeting level; 1,2,3 from 1630 to 1830


### Compositional obverter communication learning from raw visual input

**Authors:** Edward Choi, Angeliki Lazaridou, Nando de Freitas

One of the distinguishing aspects of human language is its compositionality, which allows us to describe complex environments with limited vocabulary. Previously, it has been shown that neural network agents can learn to communicate in a highly structured, possibly compositional language based on disentangled input (e.g. hand-engineered features). Humans, however, do not learn to communicate based on well-summarized features. In this work, we train neural agents to simultaneously develop visual perception from raw image pixels, and learn to communicate with a sequence of discrete symbols. The agents play an image description game where the image contains factors such as colors and shapes. We train the agents using the obverter technique where an agent introspects to generate messages that maximize its own understanding. Through qualitative analysis, visualization and a zero-shot test, we show that the agents can develop, out of raw image pixels, a language with compositional properties, given a proper pressure from the environment.

- Read the [paper](https://arxiv.org/abs/1804.02341)
- Check out the poster at East Meeting level; 1,2,3 from 1100 to 1300

### Noisy networks for exploration

**Authors:** Meire Fortunato, Mohammad Gheshlaghi Azar, Bilal Piot, Jacob Menick, Matteo Hessel, Ian Osband, Alex Graves, Volodymyr Mnih, Remi Munos, Demis Hassabis, Olivier Pietquin, Charles Blundell, Shane Legg

We introduce NoisyNet, a deep reinforcement learning agent with parametric noise added to its weights, and show that the induced stochasticity of the agent's policy can be used to aid efficient exploration. The parameters of the noise are learned with gradient descent along with the remaining network weights. NoisyNet is straightforward to implement and adds little computational overhead. We find that replacing the conventional exploration heuristics for A3C, DQN and dueling agents (entropy reward and ε-greedy respectively) with NoisyNet yields substantially higher scores for a wide range of Atari games, in some cases advancing the agent from sub to super-human performance.

- Read the [paper](https://arxiv.org/abs/1706.10295)
- Check out the poster at East Meeting level; 1,2,3 from 1630 to 1830
