---
title: "DeepMind Papers @ NIPS (Part 3)"
source: https://deepmind.google/blog/deepmind-papers-nips-part-3/
site: deepmind
date: 2016-12-07
authors: 
crawled: 2026-09-13
---

## Scaling Memory-Augmented Neural Networks with Sparse Reads and Writes

**Authors:** J Rae, JJ Hunt, T Harley, I Danihelka, A Senior, G Wayne, A Graves, T Lillicrap

We can recall vast numbers of memories, making connections between superficially unrelated events. As you read a novel, you’ll likely remember quite precisely the last few things you’ve read, but also plot summaries, connections and character traits from far back in the novel.

Many machine learning models of memory, such as Long Short Term Memory, struggle at these sort of tasks. The computational cost of these models scales quadratically with the number of memories they can store so they are quite limited in how many memories they can have. More recently, memory augmented neural networks such as the Differentiable Neural Computer or Memory Networks, have shown promising results by adding memory separate from the computation and solving tasks such as reading short stories and answering questions [e.g. Babi].

However, while these new architectures show promising results on small tasks, they use ``soft-attention’’ for accessing their memories, meaning that at every timestep they touch every word in memory. So while they can scale to short stories, they’re a long way from reading novels.

In this work, we develop a set of techniques to use sparse approximations of such models to dramatically improve their scalability. In these sparse models only a tiny subset of the memory is touched at each timestep. Importantly, we show we can do this without harming the ability of the models to learn. This means that the sparse memory augmented neural networks are able to solve the same kind of tasks but require 1000s of times less resources, and look like a promising technique, with further refinement, for reading novels.

For further details and related work, please see the paper: <https://arxiv.org/abs/1610.09027>

**Check it out at NIPS:**Wed Dec 7th 06:00 - 09:30 PM @ Area 5+6+7+8 #17

## Attend, Infer, Repeat- Fast Scene Understanding with Generative Models

**Authors:** S. M. Ali Eslami, Nicolas Heess, Theophane Weber, Yuval Tassa, David Szepesvari, Koray Kavukcuoglu, Geoffrey Hinton

![A diagram illustrating the Attend, Infer, Repeat (AIR) architecture, which sequentially processes an input image "x" through recurrent hidden states to generate latent variables for object presence, identity, and location (z_pres, z_what, z_where). On the right, a 3D scene of a table with a pot, cup, and plate is reconstructed by a decoder based on these inference steps.](https://lh3.googleusercontent.com/Px1VyeY825a1HxUMkVyZlcXNi-vP6UO3X17up88phd2O4VDFf5G_KaLuc6pBllVXUcYjiy_9YmY5uFH6dxlSN9ouaL2-LP7VCkDn99VJOAf-U4nLzpA=w1440)

Consider the task of clearing a table after dinner. To plan your actions you will need to determine which objects are present, what classes they belong to and where each one is located on the table. In other words, for many interactions with the real world the perception problem goes far beyond just image classification. We would like to build intelligent systems that learn to parse the image of a scene into objects that are arranged in space, have visual and physical properties, and are in functional relationships with each other. And we would like to do so with as little supervision as possible.

Starting from this notion our paper presents a framework for efficient inference in structured, generative image models that explicitly reason about objects. We achieve this by performing probabilistic inference using a recurrent neural network that attends to scene elements and processes them one at a time. Crucially, the model itself learns to choose the appropriate number of inference steps.

We use this scheme to learn to perform inference in partially specified 2D models (variable-sized variational auto-encoders) and fully specified 3D models (probabilistic renderers). We show that such models learn to identify multiple objects - counting, locating and classifying the elements of a scene - without any supervision, e.g., decomposing 3D images with various numbers of objects in a single forward pass of a neural network.

For further details and related work, please see the paper <https://arxiv.org/abs/1603.08575>

**Check it out at NIPS:**Wed Dec 7th 06:00 - 09:30 PM @ Area 5+6+7+8 #2

## Unifying Count-Based Exploration and Intrinsic Motivation

**Authors:** Marc G. Bellemare, Sriram Srinivasan, Georg Ostrovski, Tom Schaul, David Saxton, Remi Munos

While we've successfully trained agents to super-human performance on many Atari 2600 games, some games remain elusively difficult. One of our favourite "hard" games is Montezuma's Revenge. Montezuma's Revenge is famous for its hostile, unforgiving environment, where the agent must navigate a maze of rooms filled with traps. Each level has 24 rooms, is shaped like a pyramid, and looks like this:

![A pyramid-shaped map of the 24 rooms in Montezuma's Revenge, showing a screenshot of the game's starting room at the top (room 1), with the other rooms represented as numbered white squares.](https://lh3.googleusercontent.com/iwjydWMaeAxyPLGS51TShnk73MYx7_sNf_Z2oWyvuVQtu8HdGcr57q4EhE9T0JFI4-qm3UYCYzK4EyYYHYKFPmv9z_77l2VVopQ8ZVMtiw5h5alM=w1440)

Until now, most published agents failed to even make their way out of the first room.

Many of these hard RL problems share one thing in common: rewards are few and far between. In reinforcement learning, exploration is the process by which an agent comes to understand its environment and discover where the reward is. Most practical RL applications still rely on crude algorithms, like epsilon-greedy (once in awhile, choose a random action), because more theoretically-motivated approaches don't scale. But epsilon-greedy is quite data inefficient, and often can't even get off the ground.

In this paper we show that it's possible to use simple density models (assigning probabilities to states) to "count" the number of times we've visited a particular state. We call the output of our algorithm a pseudo-count. Pseudo-counts give us a handle on uncertainty: how confident are we that we've explored this part of the game? As a result, we were able to progress significantly further in Montezuma's Revenge. The standard DQN algorithm gets less than 100 points per play, on average; in comparison, we get 3439. To give you a sense of the difference, compare the rooms visited by both methods (white = unexplored):

![A comparison of exploration in Montezuma's Revenge: "No bonus" (top) shows only two explored rooms with the rest blank white squares, while "With bonus" (bottom) shows 15 rooms successfully explored and filled with game screenshots.](https://lh3.googleusercontent.com/5po5MrSHfpafMNQ28XzCWuo3hI--wD7_iLAJvjmsR4OZr62aNDIQVCv4PEb7tPDbwnjPRJAkBVjITLOvCt_nd-S-NikDOdfV5DVUP-ddQTexFuoWzQ=w1440)

All in all, our agent navigates through 15 rooms, compared to DQN's two. See also the video of [our agent playing Montezuma's Revenge](https://youtu.be/0yI2wJ6F8r0).

Our approach is inspired by White's 1959 idea of intrinsic motivation: that intelligent agents act first to understand their environment (See also the more recent work by Oudeyer; Barto; and Schmidhuber). What's exciting is that by playing to satisfy their curiosity, rather than to immediately win, our agents eventually come to surpass their peers.

For further details and related work, please see [the paper](https://papers.nips.cc/paper/6383-unifying-count-based-exploration-and-intrinsic-motivation.pdf).

**Check it out at NIPS:**Wednesday Dec 7th, 6PM — 9:30PM @ Area 5+6+7+8 Poster #71

## Learning values across many orders of magnitude

**Authors:** H van Hasselt, A Guez, M Hessel, V Mnih, D Silver

Sometimes we want to learn a function for which we don’t know the scale beforehand, or where the scale can change over time. For instance, this happens in value-based reinforcement learning when our policy improves over time. Initially, values might be small because our policy is not yet great, but later they increase repeatedly and unpredictably. This is a problem for many (deep) learning algorithms, because they were often not developed with such cases in mind and can then be slow or unstable.

A concrete motivation is that the [DQN](https://deepmind.com/research/publications/human-level-control-through-deep-reinforcement-learning/) algorithm successfully learned to play many Atari games, but clipped all non-zero rewards to -1 and 1. This makes learning easier, because it changes the behaviour. For instance, eating a ghost (actual reward 100+) in Ms. Pac-Man then seems to give the same reward as eating a pellet (actual reward 10).

We propose to instead adaptively normalize the targets we present to the deep neural network. To get a feel for the effectiveness of this method, we can look at the resulting magnitude (of the l2-norm) of the gradients during learning across 57 different Atari games:

![A line chart plotting gradient norm (log scale) against frames (in millions) for three different training configurations across Atari games: unclipped (red), clipped (blue), and Pop-Art (green). The unclipped gradients vary widely over six orders of magnitude, clipped gradients span about four orders of magnitude, and Pop-Art gradients are the most stable, spanning only two orders of magnitude between 1 and 100.](https://lh3.googleusercontent.com/wl5szX96XjEdaeDJedFAm2AvhaYI6bs30GfwaME3E1AaFB15y-salxTt_q8CSTbkA9zSWCDKIv99wwbbjy_0GxVUid1CH-p1ZvvGtyVukO-1os1C=w1440)

[Double DQN](https://hadovanhasselt.com/2015/12/10/deep-reinforcement-learning-with-double-q-learning-2/) is shown with unclipped rewards on the left, with the clipped rewards in the middle, and with Pop-Art is on the right. Pop-Art results in much more consistent gradients, whose magnitudes fall into a much narrower, and therefore more predictable, range. The unclipped version is much more erratic – note the log scale on the y-axis. Pop-Art even has better-normalized gradients than the clipped variant, without qualitatively changing the task as the clipping does. For some games, the resulting performance is much better than previous state of the art.

Pop-Art is not specific to DQN, Atari, or reinforcement learning. It can be useful whenever a function must be learned with unknown magnitude, or where the scale changes over time. Additionally, it can be useful when learning about multiple signals at the same time, for instance when these signals have different units and/or modalities. Normalizing per output can then help disentangle the magnitude from the importance of a signal.

For further details and related work, please see the paper [here](https://arxiv.org/abs/1602.07714) and an accompanying video [here](https://youtu.be/68LfBLPLySg).

**Check it out at NIPS:**Wednesday, December 7th, 6PM — 9:30PM @ Area 5+6+7+8 #81
