---
title: "DeepMind papers at ICML 2018"
source: https://deepmind.google/blog/deepmind-papers-at-icml-2018/
site: deepmind
date: 2018-07-09
authors: 
crawled: 2026-09-13
---

The [2018 International Conference on Machine Learning](https://icml.cc/) will take place in Stockholm, Sweden from 10-15 July.

For those attending and planning the week ahead, we are sharing a schedule of DeepMind presentations at ICML (**you can download a pdf version** [**here**](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/deepmind-papers-at-icml-2018/ICML2018-DM-schedule.pdf)). We look forward to the many engaging discussions, ideas, and collaborations that are sure to arise from the conference!


### Efficient Neural Audio Synthesis

**Authors:** Nal Kalchbrenner, Erich Elsen, Karen Simonyan, Seb Nouri, Norman Casagrande, Edward Lockhart, Sander Dieleman, Aaron van den Oord, Koray Kavukcuoglu

Sequential models achieve state-of-the-art results in audio, visual and textual domains with respect to both estimating the data distribution and generating desired samples. Efficient sampling for this class of models at the cost of little to no loss in quality has however remained an elusive task. With a focus on text-to-speech synthesis, we show that compact recurrent architectures, a remarkably high degree of weight sparsification and a novel reordering of the variables greatly reduce sampling latency while maintaining high audio fidelity. We first describe a compact single-layer recurrent neural network, the WaveRNN, with a novel dual softmax layer that matches the quality of the state-of-the-art WaveNet model. Persistent GPU kernels for the WaveRNN are able to synthesize 24kHz 16-bit audio 4 times faster than real time. We then apply a weight sparsification technique to the model. We show that, given a constant number of weights, large sparse networks perform better than small dense networks. Using a large Sparse WaveRNN, we demonstrate the feasibility of real-time synthesis of high-fidelity audio on a low-power mobile phone CPU. We use a large Sparse WaveRNN to demonstrate the first instance of real-time synthesis of high-fidelity audio on low-resource mobile phone CPU. Finally, we introduce a novel reordering of the variables in the factorization of the joint distribution. The reordering makes it possible to trade vacuous dependencies on samples from the distant future for the ability to generate in batches. The Batch WaveRNN produces up to 16 samples per step maintaining high quality and enables audio synthesis that is up to 40 times faster than real time.

**Presentations:**

- 11:00 – 11:20 AM @ Victoria (Oral)
- 06:15 – 09:00 PM @ Hall B #105 (Poster)

### Learning to Search with MCTSnets

**Authors:** Arthur Guez\*, Theophane Weber\*, Ioannis Antonoglou, Karen Simonyan, Oriol Vinyals, Daan Wierstra, Remi Munos, David Silver

Planning problems are among the most important and well-studied problems in artificial intelligence. They are most typically solved by tree search algorithms that simulate ahead into the future, evaluate future states, and back-up those evaluations to the root of a search tree. Among these algorithms, Monte-Carlo tree search (MCTS) is one of the most general, powerful and widely used. A typical implementation of MCTS uses cleverly designed rules, optimised to the particular characteristics of the domain. These rules control where the simulation traverses, what to evaluate in the states that are reached, and how to back-up those evaluations. In this paper we instead learn where, what and how to search. Our architecture, which we call an MCTSnet, incorporates simulation-based search inside a neural network, by expanding, evaluating and backing-up a vector embedding. The parameters of the network are trained end-to-end using gradient-based optimisation. When applied to small searches in the well-known planning problem Sokoban, the learned search algorithm significantly outperformed MCTS baselines.

**Presentations:**

- 11:20 – 11:30 AM @ Victoria (Oral)
- 06:15 – 09:00 PM @ Hall B #92 (Poster)

### LeapsAndBounds: A Method for Approximately Optimal Algorithm Configuration

**Authors:** Gellert Weisz, Andras Gyorgy, and Csaba Szepesvari

We consider the problem of configuring general-purpose solvers to run efficiently on problem instances drawn from an unknown distribution. The goal of the configurator is to find a configuration that runs fast on average on most instances, and do so with the least amount of total work. It can run a chosen solver on a random instance until the solver finishes or a timeout is reached. We propose LEAPSANDBOUNDS, an algorithm that tests configurations on randomly selected problem instances for longer and longer time. We prove that the capped expected runtime of the configuration returned by LEAPSANDBOUNDS is close to the optimal expected runtime, while our algorithm’s running time is near-optimal. Our results show that LEAPSANDBOUNDS is more efficient than the recent algorithm of Kleinberg et al. (2017), which, to our knowledge, is the only other algorithm configuration method that claims to have non-trivial theoretical guarantees. Experimental results on configuring a public SAT solver on a public benchmark also stand witness to the superiority of our method.

**Presentations:**

- 11:30 – 11:40 AM @ A6 (Oral)
- 06:15 – 09:00 PM @ Hall B #165 (Poster)

### Implicit Quantile Networks for Distributional Reinforcement Learning

**Authors:** Will Dabney\*, Georg Ostrovski\*, David Silver, Remi Munos

In this work, we build on recent advances in distributional reinforcement learning to give a generally applicable, flexible, and state-of-the-art distributional variant of DQN. We achieve this by using quantile regression to approximate the full quantile function for the state-action return distribution. By reparameterizing a distribution over the sample space, this yields an implicitly defined return distribution and gives rise to a large class of risk-sensitive policies. We demonstrate improved performance on the 57 Atari 2600 games in the ALE, and use our algorithms implicitly defined distributions to study the effects of risk-sensitive policies in Atari games.

**Presentations:**

- 11:40 – 11:50 AM @ A1 (Oral)
- 06:15 – 09:00 PM @ Hall B #3 (Poster)

### Graph Networks as Learnable Physics Engines for Inference and Control

**Authors:** Alvaro Sanchez, Nicolas Heess, Jost Tobias Springenberg, Josh Merel, Martin Riedmiller, Raia Hadsell, Peter Battaglia

Understanding and interacting with everyday physical scenes requires rich knowledge about the structure of the world, represented either implicitly in a value or policy function, or explicitly in a transition model. Here we introduce a new class of learnable models—based on graph networks—which implement an inductive bias for object- and relation-centric representations of complex, dynamical systems. Our results show that as a forward model, our approach supports accurate predictions, and surprisingly strong and efficient generalization, across eight distinct physical systems which we varied parametrically and structurally. We also found that our inference model can perform system identification from real and simulated data. Our models are also differentiable, and support online planning via gradient based trajectory optimization, as well as offline policy optimization. Our framework offers new opportunities for harnessing and exploiting rich knowledge about the world, and takes a key step toward building machines with more human-like representations of the world.

**Presentations:**

- 11:50 AM – 12:00 PM @ Victoria (Oral)
- 06:15 – 09:00 PM @ Hall B #84 (Poster)

### More Robust Doubly Robust Off-policy Evaluation

**Authors:** Mehrdad Farajtabar, Yinlam Chow, and Mohammad Ghavamzadeh

We study the problem of off-policy evaluation (OPE) in reinforcement learning (RL), where the goal is to estimate the performance of a policy from the data generated by another policy(ies). In particular, we focus on the doubly robust (DR) estimators that consist of an importance sampling (IS) component and a performance model, and utilize the low (or zero) bias of IS and low variance of the model at the same time. Although the accuracy of the model has a huge impact on the overall performance of DR, most of the work on using the DR estimators in OPE has been focused on improving the IS part, and not much on how to learn the model. In this paper, we propose alternative DR estimators, called more robust doubly robust (MRDR), that learn the model parameter by minimizing the variance of the DR estimator. We first present a formulation for learning the DR model in RL. We then derive formulas for the variance of the DR estimator in both contextual bandits and RL, such that their gradients w.r.t. the model parameters can be estimated from the samples, and propose methods to efficiently minimize the variance. We prove that the MRDR estimators are strongly consistent and asymptotically optimal. Finally, we evaluate MRDR in bandits and RL benchmark problems, and compare its performance with the existing methods.

**Presentations:**

- 11:50 AM – 12:00 PM @ A1 (Oral)
- 06:15 – 09:00 PM @ Hall B #62 (Poster)

### Conditional Neural Processes

**Authors:** Marta Garnelo, Dan Rosenbaum, Christopher Maddison, Tiago Ramalho, David Saxton, Murray Shanahan, Yee Whye Teh, Danilo Rezende, S. M. Ali Eslami

Deep neural networks excel at function approximation, yet they are typically trained from scratch for each new function. On the other hand, Bayesian methods, such as Gaussian Processes (GPs), exploit prior knowledge to quickly infer the shape of a new function at test time. Yet GPs are computationally expensive, and it can be hard to design appropriate priors. In this paper we propose a family of neural models, Conditional Neural Processes (CNPs), that combine the benefits of both. CNPs are inspired by the flexibility of stochastic processes such as GPs, but are structured as neural networks and trained via gradient descent. CNPs make accurate predictions after observing only a handful of training data points, yet scale to complex functions and large datasets. We demonstrate the performance and versatility of the approach on a range of canonical machine learning tasks, including regression, classification and image completion.

**Presentations:**

- 02:10 – 02:20 PM @ Victoria (Oral)
- 06:15 – 09:00 PM @ Hall B #130 (Poster)

### Generative Temporal Models with Spatial Memory for Partially Observed Environments

**Authors:** Marco Fraccaro, Danilo Jimenez Rezende, Yori Zwols, Alexander Pritzel, S. M. Ali Eslami, Fabio Viola

In model-based reinforcement learning, generative and temporal models of environments can be leveraged to boost agent performance, either by tuning the agent’s representations during training or via use as part of an explicit planning mechanism. However, their application in practice has been limited to simplistic environments, due to the difficulty of training such models in larger, potentially partially-observed and 3D environments. In this work we introduce a novel action-conditioned generative model of such challenging environments. The model features a non-parametric spatial memory system in which we store learned, disentangled representations of the environment. Low-dimensional spatial updates are computed using a state-space model that makes use of knowledge on the prior dynamics of the moving agent, and high-dimensional visual observations are modelled with a Variational Auto-Encoder. The result is a scalable architecture capable of performing coherent predictions over hundreds of time steps across a range of partially observed 2D and 3D environments.

**Presentations:**

- 02:30 – 02:50 PM @ A7 (Oral)
- 06:15 – 09:00 PM @ Hall B #101 (Poster)

### Disentangling by Factorising

**Authors:** Hyunjik Kim, Andriy Mnih

We define and address the problem of unsupervised learning of disentangled representations on data generated from independent factors of variation. We propose FactorVAE, a method that disentangles by encouraging the distribution of rep-resentations to be factorial and hence independent across the dimensions. We show that it improves upon β-VAE by providing a better trade-off between disentanglement and reconstruction quality and being more robust to the number of training iterations. Moreover, we highlight the problems of a commonly used disentanglement metric and introduce a new metric that does not suffer from them.

**Presentations:**

- 02:50 – 03:00 PM @ A7 (Oral)
- 06:15 – 09:00 PM @ Hall B #90 (Poster)

### Learning by Playing – Solving Sparse Reward Tasks from Scratch

**Authors:** Martin Riedmiller, Roland Hafner, Thomas Lampe, Michael Neunert, Jonas Degrave, Tobias Springenberg

We propose Scheduled Auxiliary Control (SAC), a new learning paradigm in the context of Reinforcement Learning (RL) . SAC enables learning of complex behaviors – from scratch – in the presence of multiple sparse reward signals. To achieve this the agent is equipped with a set of general auxiliary tasks, that it attempts to learn simultaneously via off-policy RL. The key idea behind our method is that active (learned) scheduling and execution of auxiliary policies allows the agent to efficiently explore its environment – enabling it
to excel at sparse reward RL. Our experiments in several challenging robotic manipulation settings demonstrate the power of our approach.

Read more on the DeepMind [blog](https://deepmind.com/blog/learning-playing/).

**Presentations:**

- 04:20 – 04:40 PM @ A1 (Oral)
- 06:15 – 09:00 PM @ Hall B #41 (Poster)

### Fast Parametric Learning with Activation Memorization

**Authors:** Jack W Rae, Chris Dyer, Peter Dayan, Timothy P Lillicrap

Neural networks trained with backpropagation often struggle to identify classes that have been observed a small number of times. In applications where most class labels are rare, such as language modelling, this can become a performance bottleneck. One potential remedy is to augment the network with a fast-learning non-parametric model which attends over recent activations. We explore a simplified architecture where we treat a subset of the model parameters as fast memory stores. This can help retain information over longer time intervals than a traditional memory, and does not require additional space or compute. In the case of image classification, we display faster binding of novel classes on an Omniglot image curriculum task. We also show improved performance for word-based language models on news reports (GigaWord), books (Project Gutenberg) and Wikipedia articles (WikiText-103) — the latter achieving state-of-the-art perplexity.

**Presentations:**

- 04:40 – 04:50 PM @ Victoria (Oral)
- 06:15 – 09:00 PM @ Hall B #121 (Poster)

### Learning Implicit Generative Models with the Method of Learned Moments

**Authors:** Suman Ravuri, Shakir Mohamed, Mihaela Rosca, and Oriol Vinyals

We propose a method of moments (MoM) algorithm for training large-scale implicit generative models. Moment estimation in this setting encounters two problem: it is often difficult to define the millions of moments needed to learn the model parameters, and it is hard to determine which properties are useful when specifying moments. To address the first issue, we introduce a moment network, and define the moments as the gradient of the network’s output with respect to its parameters and the network’s hidden units. To tackle the second problem, we use asymptotic theory to highlight desiderata for moments – namely they should minimize the asymptotic variance of estimated model parameters – and introduce an objective to learn better moments. The sequence of objectives created by this Method of Learned Moments (MoLM) can train high-quality neural image samplers. On CIFAR-10, we demonstrate that MoLM-trained generators achieve significantly higher Inception Scores and lower Frechet Inception Distances than those trained with gradient penalty regularized adversarial objectives. These generators also achieve nearly perfect Multi-Scale Structural Similarity Scores on CelebA, and can create high-quality samples of resolutions up to 128×128.

**Presentations:**

- 04:40 – 04:50 PM @ A7 (Oral)
- 06:15 – 09:00 PM @ Hall B #112 (Poster)

### Automatic Goal Generation for Reinforcement Learning Agents

**Authors:** David Held, Xinyang Geng, Carlos Florensa, Pieter Abbeel

Reinforcement learning is a powerful technique to train an agent to perform a task. However, an agent that is trained using reinforcement learning is only capable of achieving the single task that is specified via its reward function. Such an approach does not scale well to settings in which an agent needs to perform a diverse set of tasks, such as navigating to varying positions in a room or moving objects to varying locations. Instead, we propose a method that allows an agent to automatically discover the range of tasks that it is capable of performing. We use a generator network to propose tasks for the agent to try to achieve, specified as goal states. The generator network is optimized using adversarial training to produce tasks that are always at the appropriate level of difficulty for the agent. Our method thus automatically produces a curriculum of tasks for the agent to learn. We show that, by using this framework, an agent can efficiently and automatically learn to perform a wide set of tasks without requiring any prior knowledge of its environment. Our method can also learn to achieve tasks with sparse rewards, which traditionally pose significant challenges.

**Presentations:**

- 04:40 – 04:50 PM @ A1 (Oral)
- 06:15 – 09:00 PM @ Hall B #135 (Poster)

### Machine Theory of Mind

**Authors:** Neil C. Rabinowitz, Frank Perbet, H. Francis Song, Chiyuan Zhang, S. M. Ali Eslami, Matthew Botvinick

Theory of mind (ToM) broadly refers to humans’ ability to represent the mental states of others, including their desires, beliefs, and intentions. We propose to train a machine to build such models too. We design a Theory of Mind neural network – a ToMnet – which uses meta-learning to build models of the agents it encounters. The ToMnet learns a strong prior model for agents’ future behaviour, and, using only a small number of behavioural observations, can bootstrap to richer predictions about agents’ characteristics and mental states. We apply the ToMnet to agents behaving in simple gridworld environments, showing that it learns to model random, algorithmic, and deep RL agents from varied populations, and that it passes classic ToM tasks such as the “Sally-Anne” test of recognising that others can hold false beliefs about the world.

**Presentations:**

- 05:00 – 05:20 PM @ A3 (Oral)
- 06:15 – 09:00 PM @ Hall B #208 (Poster)

### Path Consistency Learning in Tsallis Entropy Regularized MDPs

**Authors:** Ofir Nachum, Yinlam Chow, and Mohammad Ghavamzadeh

We study the sparse entropy-regularized reinforcement learning (ERL) problem in which the entropy term is a special form of the Tsallis entropy. The optimal policy of this formulation is sparse, i.e., at each state, it has non-zero probability for only a small number of actions. This addresses the main drawback of the standard Shannon entropy-regularized RL (soft ERL) formulation, in which the optimal policy is {\em softmax}, and thus, may assign a non-negligible probability mass to non-optimal actions. This problem is aggravated as the number of actions is increased. In this paper, we follow the work of Nachum et al. (2017) in the soft ERL setting, and propose a class of novel path consistency learning (PCL) algorithms, called sparse PCL, for the sparse ERL problem that can work with both on-policy and off-policy data. We first derive a sparse consistency equation that specifies a relationship between the optimal value function and policy of the sparse ERL along any system trajectory. Crucially, a weak form of the converse is also true, and we quantify the sub-optimality of a policy which satisfies sparse consistency, and show that as we increase the number of actions, this sub-optimality is better than that of the soft ERL optimal policy. We then use this result to derive the sparse PCL algorithms. We empirically compare sparse PCL with its soft counterpart, and show its advantage, especially in problems with a large number of actions.

**Presentations:**

- 05:20 – 05:40 PM @ A1 (Oral)
- 06:15 – 09:00 PM @ Hall B #172 (Poster)

### Transfer in Deep Reinforcement Learning Using Successor Features and Generalised Policy Improvement

**Authors:** Andre Barreto, Diana Borsa, John Quan, Tom Schaul, David Silver, Matteo Hessel, Daniel Makowitz, Augustin Zidek, Remi Munos

The ability to transfer skills across tasks has the potential to scale up reinforcement learning (RL) agents to environments currently out of reach. Recently, a framework based on two ideas, successor features (SFs) and generalised policy improvement (GPI), has been introduced as a principled way of transferring skills. In this paper we investigate the feasibility of combining SF&GPI with the representation power of deep learning. Since in deep RL we are interested in learning all the components of SF&GPI concurrently, the existing inter-dependencies between them can lead to instabilities. In this work we propose a solution for this problem that makes it possible to use SF & GPI online, at scale. In order to empirically verify this claim, we apply the proposed method to a complex 3D environment that requires hundreds of millions of transitions to be solved. We show that the transfer promoted by SF&GPI leads to reasonable policies on unseen tasks almost instantaneously. We also show how to build on the transferred policies to learn policies that are specialised to the new tasks, which can then be added to the agent’s set of skills to be used in the future.

**Presentations:**

- 05:20 – 05:40 PM @ A3 (Oral)
- 06:15 – 09:00 PM @ Hall B #163 (Poster)

### Been There, Done That: Meta-Learning with Episodic Recall

**Authors:** Samuel Ritter, Jane Wang, Sid Jayakumar, Zeb Kurth-Nelson, Charles Blundell, Razvan Pascanu, Matt Botvinick

Meta-learning agents have demonstrated the ability to rapidly explore and exploit new tasks sampled from the task distribution on which they were trained. However, when these agents encounter situations that they explored in the distant past, they are not able to remember the results of their past exploration. Thus, instead of immediately exploiting previously discovered solutions, they must again explore from scratch. In this work, we argue that the necessity to remember the results of past exploration is ubiquitous in naturalistic environments. We propose a formalism for modeling this kind of recurring environment structure, then develop a meta-learning architecture for solving such environments. This architecture melds the standard LSTM working memory with a differentiable neural episodic memory. We explore the capabilities of this episodic LSTM in four recurrent-state stochastic process environments: 1.) episodic contextual bandits, 2.) compositional contextual bandits, 3.) episodic two-step task, and 4.) contextual water-maze navigation.

**Presentations:**

- 05:40 – 05:50 PM @ A3 (Oral)
- 06:15 – 09:00 PM @ Hall B #209 (Poster)

### Adversarial Risk and the Dangers of Evaluating Against Weak Attacks

**Authors:** Jonathan Uesato, Brendan O'Donoghue, Aaron van den Oord, and Pushmeet Kohli.

This paper investigates recently proposed approaches for defending against adversarial examples and evaluating adversarial robustness. The existence of adversarial examples in trained neural networks reflects the fact that expected risk alone does not capture the model’s performance against worst-case inputs. We motivate the use of advKarol Hausmaersarial risk as an objective, although it can not easily be computed exactly. We then frame commonly used attacks and evaluation metrics as defining a tractable surrogate objective to the true adversarial risk. This suggests that models may be obscured to adversaries, by optimizing this surrogate rather than the true adversarial risk. We demonstrate that this is a significant problem in practice by repurposing gradient-free optimization techniques into adversarial attacks, which we use to decrease the accuracy of several recently proposed defenses to near zero. Our hope is that
our formulations and results will help researchers to develop more powerful defenses.

**Presentations:**

- 05:50 – 06:00 PM @ A7 (Oral)
- 06:15 – 09:00 PM @ Hall B #132 (Poster)

## Thursday 12th July

[**Learning to Coordinate with Coordination Graphs in Repeated Single-Stage Multi-Agent Decision Problems**](http://proceedings.mlr.press/v80/bargiacchi18a/bargiacchi18a.pdf)

**Authors:** Eugenio Bargiacchi (Vrije Universiteit Brussel), Timothy Verstraeten (Vrije Universiteit Brussel), Diederik Roijers (Vrije Universiteit Brussel / Vrije Universiteit Amsterdam), Ann Nowé (Vrije Universiteit Brussel), Hado van Hasselt

Learning to coordinate between multiple agents is an important problem in many reinforcement learning problems. Key to learning to coordinate is exploiting loose couplings, i.e., conditional independences between agents. In this paper we study learning in repeated fully cooperative games, multi-agent multi-armed bandits (MAMABs), in which the expected rewards can be expressed as a coordination graph. We propose multi-agent upper confidence exploration (MAUCE), a new algorithm for MAMABs that exploits loose couplings, which enables us to prove a regret bound that is logarithmic in the number of arm pulls and only linear in the number of agents. We empirically compare MAUCE to sparse cooperative Q-learning, and a state-of-the-art combinatorial bandit approach, and show that it performs much better on a variety of settings, including learning control policies for wind farms.

**Presentations:**

- 11:00 – 11:10 AM @ A3 (Oral)
- 06:15 – 09:00 PM @ Hall B #126 (Poster)

### Bandits with Delayed, Aggregated Anonymous Feedback

**Authors:** Ciara Pike-Burke, Shipra Agrawal, Csaba Szepesvari, Steffen Grunewalder

We study a variant of the stochastic K-armed bandit problem, which we call "bandits with delayed, aggregated anonymous feedback". In this problem, when the player pulls an arm, a reward is generated, however it is not immediately observed. Instead, at the end of each round the player observes only the sum of a number of previously generated rewards which happen to arrive in the given round. The rewards are stochastically delayed and due to the aggregated nature of the observations, the information of which arm led to a particular reward is lost. The question is what is the cost of the information loss due to this delayed, aggregated anonymous feedback? Previous works have studied bandits with stochastic, non-anonymous delays and found that the regret increases only by an additive factor relating to the expected delay. In this paper, we show that this additive regret increase can be maintained in the harder delayed, aggregated anonymous feedback setting when the expected delay (or a bound on it) is known. We provide an algorithm that matches the worst case regret of the non-anonymous problem exactly when the delays are bounded, and up to logarithmic factors or an additive variance term for unbounded delays.

**Presentations:**

- 02:50 – 03:10 PM @ A5 (Oral)
- 06:15 – 09:00 PM @ Hall B #123 (Poster)

### The Mechanics of n-Player Differentiable Games

**Best Paper Runner Up**

**Authors:** David Balduzzi, Sébastien Racaniere, James Martens, Jakob Foerster, Karl Tuyls, Thore Graepel

The cornerstone underpinning deep learning is the guarantee that gradient descent on an objective converges to local minima. Unfortunately, this guarantee fails in settings, such as generative adversarial nets, where there are multiple interacting losses. The behavior of gradient-based methods in games is not well understood – and is becoming increasingly important as adversarial and multi-objective architectures proliferate. In this paper, we develop new techniques to understand and control the dynamics in general games. The key result is to decompose the second-order dynamics into two components. The first is related to potential games, which reduce to gradient descent on an implicit function; the second relates to Hamiltonian games, a new class of games that obey a conservation law, akin to conservation laws in classical mechanical systems. The decomposition motivates Symplectic Gradient Adjustment (SGA), a new algorithm for finding stable fixed points in general games. Basic experiments show SGA is competitive with recently proposed algorithms for finding local Nash equilibria in GANs – whilst at the same time being applicable to – and having guarantees in – much more general games.

**Presentations:**

- 04:00 – 04:20 PM @ A7 (Oral)
- 06:15 – 09:00 PM @ Hall B #201 (Poster)

### LaVAN: Localized and Visible Adversarial Noise

**Authors**: Danny Karmon (Bar Ilan University), Daniel Zoran, Yoav Goldberg (Bar Ilan University)

Most works on adversarial examples for deep-learning based image classifiers use noise that, while small, covers the entire image. We explore the case where the noise is allowed to be visible but confined to a small, localized patch of the image, without covering any of the main object(s) in the image. We show that it is possible to generate localized adversarial noises that cover only 2% of the pixels in the image, none of them over the main object, and that are transferable across images and locations, and successfully fool a state-of-the-art Inception v3 model with very high success rates.

**Presentations:**

- 04:50 – 05:00 PM @ A7 (Oral)
- 06:15 – 09:00 PM @ Hall B #116 (Poster)

### Synthesizing Programs for Images using Reinforced Adversarial Learning

**Authors:** Yaroslav Ganin, Tejas Kulkarni, Igor Babuschkin, S.M. Ali Eslami, Oriol Vinyals

Advances in deep generative networks have led to impressive results in recent years. Nevertheless, such models can often waste their capacity on the minutiae of datasets, presumably due to weak inductive biases in their decoders. This is where graphics engines may come in handy since they abstract away low-level details and represent images as high-level programs. Current methods that combine deep learning and renderers are limited by hand-crafted likelihood or distance functions, a need for large amounts of supervision, or difficulties in scaling their inference algorithms to richer datasets. To mitigate these issues, we present SPIRAL, an adversarially trained agent that generates a program which is executed by a graphics engine to interpret and sample images. The goal of this agent is to fool a discriminator network that distinguishes between real and rendered data, trained with a distributed reinforcement learning setup without any supervision. A surprising finding is that using the discriminator's output as a reward signal is the key to allow the agent to make meaningful progress at matching the desired output rendering. To the best of our knowledge, this is the first demonstration of an end-to-end, unsupervised and adversarial inverse graphics agent on challenging real world (MNIST, Omniglot, CelebA) and synthetic 3D datasets.

**Presentations:**

- 05:00 – 05:20 PM @ A7 (Oral)
- 06:15 – 09:00 PM @ Hall B #84 (Poster)

### Measuring abstract reasoning in neural networks

**Authors:** David Barrett\*, Felix Hill\*, Adam Santoro\*, Ari Morcos, Tim Lillicrap

Whether neural networks can learn abstract reasoning or whether they merely rely on superficial statistics is a topic of recent debate. Here, we propose a dataset and challenge designed to probe abstract reasoning, inspired by a well-known human IQ test. To succeed at this challenge, models must cope with various generalisation ‘regimes’ in which the training and test data differ in clearly defined ways. We show that popular models such as ResNets perform poorly, even when the training and test sets differ only minimally, and we present a novel architecture, with a structure designed to encourage reasoning, that does significantly better. When we vary the way in which the test questions and training data differ, we find that our model is notably proficient at certain forms of generalisation, but notably weak at others. We further show that the model’s ability to generalise improves markedly if it is trained to predict symbolic explanations for its answers. Altogether, we introduce and explore ways to both measure and induce stronger abstract reasoning in neural networks. Our freely-available dataset should motivate further progress in this direction.

**Presentations:**

- 05:20 – 05:40 PM @ K1 (Oral)
- 06:15 – 09:00 PM @ Hall B #110 (Poster)

Read more on the DeepMind [blog](https://deepmind.com/blog/article/measuring-abstract-reasoning).


### Scalable Distributed Deep-RL with Importance Weighted Actor-Learner Architectures

**Authors:** Lasse Espeholt, Hubert Soyer, Remi Munos, Karen Simonyan, Volodymir Mnih, Tom Ward, Yotam Doron, Vlad Firoiu, Tim Harley, Iain Dunning, Shane Legg, Koray Kavukcuoglu

In this work we aim to solve a large collection of tasks using a single reinforcement learning agent with a single set of parameters. A key challenge is to handle the increased amount of data and extended training time. We have developed a new distributed agent IMPALA (Importance Weighted Actor-Learner Architecture) that not only uses resources more efficiently in single-machine training but also scales to thousands of machines without sacrificing data efficiency or resource utilisation. We achieve stable learning at high throughput by combining decoupled acting and learning with a novel off-policy correction method called
V-trace. We demonstrate the effectiveness of IMPALA for multi-task reinforcement learning on DMLab-30 (a set of 30 tasks from the DeepMind Lab environment (Beattie et al., 2016)) and Atari-57 (all available Atari games in Arcade Learning Environment (Bellemare et al., 2013a)). Our results show that IMPALA is able to achieve better performance than previous agents with less data, and crucially exhibits positive transfer between tasks as a result of its multi-task approach.

Read more on the DeepMind [blog](https://deepmind.com/blog/impala-scalable-distributed-deeprl-dmlab-30/), and see our open-source implementation on [GitHub](https://github.com/deepmind/scalable_agent).

**Presentations:**

- 09:50 – 10:10 AM @ A1 (Oral)
- 06:15 – 09:00 PM @ Hall B #176 (Poster)

### Mix & Match - Agent Curricula for Reinforcement Learning

**Authors:** Wojtek Czarnecki\*, Siddhant Jayakumar\*, Max Jaderberg, Leonard Hasenclever, Yee Whye Teh, Nicolas Heess, Simon Osindero, Razvan Pascanu

We introduce Mix & Match (M&M) – a training framework designed to facilitate rapid and effective learning in RL agents, especially those that would be too slow or too challenging to train otherwise. The key innovation is a procedure that allows us to automatically form a curriculum over agents. Through such a curriculum we can progressively train more complex agents by, effectively, bootstrapping from solutions found by simpler agents. In contradistinction to typical curriculum learning approaches, we do not gradually modify the tasks or environments presented, but instead use a process to gradually alter how the policy is represented internally. We show the broad applicability of our method by demonstrating significant performance gains in three different experimental setups: (1) We train an agent able to control more than 700 actions in a challenging 3D first-person task; using our method to progress through an action-space curriculum we achieve both faster training and better final performance than one obtains using traditional methods. (2) We further show that M&M can be used successfully to progress through a curriculum of architectural variants defining an agents internal state. (3) Finally, we illustrate how a variant of our method can be used to improve agent performance in a multitask setting.

**Presentations:**

- 10:10 – 10:20 AM @ A1 (Oral)
- 06:15 – 09:00 PM @ Hall B #13 (Poster)

### Parallel WaveNet: fast high-Fidelity Speech Synthesis

**Authors:** Aaron van den Oord, Yazhe Li, Igor Babuschkin, Karen Simonyan, Oriol Vinyals, Koray Kavukcuoglu

The recently-developed WaveNet architecture is the current state of the art in realistic speech synthesis, consistently rated as more natural sounding for many different languages than any previous system. However, because WaveNet relies on sequential generation of one audio sample at a time, it is poorly suited to today’s massively parallel computers, and therefore hard to deploy in a real-time production setting. This paper introduces Probability Density Distillation, a new method for training a parallel feed-forward network from a trained WaveNet with no significant difference in quality. The resulting system is capable of generating high-fidelity speech samples at more than 20 times faster than real-time, and is deployed online by Google Assistant, including serving multiple English and Japanese voices.

**Presentations:**

- 04:00 – 04:20 PM @ A7 (Oral)
- 06:15 – 09:00 PM @ Hall B #25 (Poster)

Read more on the DeepMind [blog](https://deepmind.com/blog/learning-playing/).

### Progress & Compress: A scalable framework for continual learning

**Authors:** Jonathan Schwarz, Jelena Luketina, Wojciech M. Czarnecki, Agnieszka Grabska-Barwinska, Yee Whye Teh, Razvan Pascanu\* Raia Hadsell\*

We introduce a conceptually simple and scalable framework for continual learning domains where tasks are learned sequentially. Our method is constant in the number of parameters and is designed to preserve performance on previously encountered tasks while accelerating learning progress on subsequent problems. This is achieved through

training two neural networks: A knowledge base, capable of solving previously encountered problems, which is connected to an active column that is employed to efficiently learn the current task. After learning a new task, the active column is distilled into the knowledge base, taking care to protect any previously learnt tasks. This cycle of active learning (progression) followed by consolidation (compression) requires no architecture growth, no access to or storing of previous data or tasks, and no task-specific parameters. Thus, it is a learning process that may be sustained over a lifetime of tasks while supporting forward transfer and minimising forgetting. We demonstrate the progress & compress approach on sequential classification of handwritten alphabets as well as two reinforcement learning domains: Atari games and 3D maze navigation.

**Presentations:**

- 04:00 – 04:20 PM @ Victoria (Oral)
- 06:15 – 09:00 PM @ Hall B #168 (Poster)

### Autoregressive Quantile Networks for Generative Modeling

**Authors:** Georg Ostrovski\*, Will Dabney\*, Remi Munos

We introduce autoregressive implicit quantile networks (AIQN), a fundamentally different approach to generative modeling than those commonly used, that implicitly captures the distribution using quantile regression. AIQN is able to achieve superior perceptual quality and improvements in evaluation metrics, without incurring a loss of sample diversity. The method can be applied to many existing models and architectures. In this work we extend the PixelCNN model with AIQN and demonstrate results on CIFAR-10 and ImageNet using Inception scores, FID, non-cherry-picked samples, and inpainting results. We consistently observe that AIQN yields a highly stable algorithm that improves perceptual quality while maintaining a highly diverse distribution.

**Presentations:**

- 04:20 – 04:40 PM @ A7 (Oral)
- 06:15 – 09:00 PM @ Hall B #110 (Poster)

### The Uncertainty Bellman Equation and Exploration

**Authors:** Brendan O'Donoghue, Ian Osband, Remi Munos, Volodymyr Mnih

We consider the exploration/exploitation problem in reinforcement learning. For exploitation, it is well known that the Bellman equation connects the value at any time-step to the expected value at subsequent time-steps. In this paper we consider a similar \textit{uncertainty} Bellman equation (UBE), which connects the uncertainty at any time-step to the expected uncertainties at subsequent time-steps, thereby extending the potential exploratory benefit of a policy beyond individual time-steps. We prove that the unique fixed point of the UBE yields an upper bound on the variance of the posterior distribution of the Q-values induced by any policy. This bound can be much tighter than traditional count-based bonuses that compound standard deviation rather than variance. Importantly, and unlike several existing approaches to optimism, this method scales naturally to large systems with complex generalization. Substituting our UBE-exploration strategy for ε-greedy improves DQN performance on 51 out of 57 games in the Atari suite.

**Presentations:**

- 05:50 – 06:00 PM @ A1 (Oral)
- 06:15 – 09:00 PM @ Hall B #14 (Poster)

### Crowdsourcing with Sparsely Interacting Workers

**Authors:** Yao Ma (Boston University), Alexander Olshevsky (Boston University), Csaba Szepesvari, Venkatesh Saligrama (Boston University)

We consider estimation of worker skills from worker-task interaction data (with unknown labels) for the single-coin crowd-sourcing binary classification model in symmetric noise. We define the (worker) interaction graph whose nodes are workers and an edge between two nodes indicates whether or not the two workers participated in a common task. We show that skills are asymptotically identifiable if and only if an appropriate limiting version of the interaction graph is irreducible and has odd-cycles. We then formulate a weighted rank-one optimization problem to estimate skills based on observations on an irreducible, aperiodic interaction graph. We propose a gradient descent scheme and show that for such interaction graphs estimates converge asymptotically to the global minimum. We characterize noise robustness of the gradient scheme in terms of spectral properties of signless Laplacians of the interaction graph. We then demonstrate that a plug-in estimator based on the estimated skills achieves state-of-art performance on a number of real-world datasets. Our results have implications for rank-one matrix completion problem in that gradient descent can provably recover W×W rank-one matrices based on W+1 off-diagonal observations of a connected graph with a single odd-cycle.

**Presentations:**

- 05:50 – 06:00 PM @ K11 (Oral)
- 06:15 – 09:00 PM @ Hall B #77 (Poster)
