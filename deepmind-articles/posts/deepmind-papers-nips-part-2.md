---
title: "DeepMind Papers @ NIPS (Part 2)"
source: https://deepmind.google/blog/deepmind-papers-nips-part-2/
site: deepmind
date: 2016-12-05
authors: 
crawled: 2026-09-13
---

*The second blog post in this series, sharing brief descriptions of the papers we are presenting at NIPS 2016 Conference in Barcelona.*

## Sequential Neural Models with Stochastic Layers

**Authors:** Marco Fraccaro, Søren Kaae Sønderby, Ulrich Paquet, Ole Winther

Much of our reasoning about the world is sequential, from listening to sounds and voices and music, to imagining our steps to reach a destination, to tracking a tennis ball through time. All these sequences have some amount of latent random structure in them. Two powerful and complementary models, recurrent neural networks (RNNs) and stochastic state space models (SSMs), are widely used to model sequential data like these. RNNs are excellent at capturing longer-term dependencies in data, while SSMs model uncertainty in the sequence's underlying latent random structure, and are great for tracking and control.

Is it possible to get the best of both worlds? In this paper we show how you can, by carefully layering deterministic (RNN) and stochastic (SSM) layers. We show how you can efficiently reason about a sequence’s present latent structure, given its past (filtering) and also its past and future (smoothing).

For further details and related work, please see the paper <https://arxiv.org/abs/1605.07571>

**Check it out at NIPS:**Tue Dec 6th 05:20 - 05:40 PM @ Area 1+2 (Oral) in Deep Learning
Tue Dec 6th 06:00 - 09:30 PM @ Area 5+6+7+8 #179

## Learning to learn by gradient descent gradient descent

**Authors:** Marcin Andrychowicz, Misha Denil, Sergio Gomez, Matthew Hoffman, David Pfau, Tom Schaul, Nando De Freitas

Optimization algorithms today are typically designed by hand; algorithm designers, thinking carefully about each problem, are able to design algorithms that exploit structure that they can characterize precisely. This design process mirrors the efforts of computer vision in the early 2000s to manually characterize and locate features like edges and corners in images with hand designed features. The biggest breakthrough of modern computer vision has been to instead learn these features directly from data, removing manual engineering from the loop. This paper shows how we can extend these techniques to algorithm design, learning not only features but also learning about the learning process itself.

We show how the design of an optimization algorithm can be cast as a learning problem, allowing the algorithm to learn to exploit structure in the problems of interest in an automatic way. Our learned algorithms outperform standard hand-designed competitors on the tasks for which they are trained, and also generalize well to new tasks with similar structure. We demonstrate this on a number of tasks, including neural network training, and styling images with neural art.

For further details and related work, please see the paper <https://arxiv.org/abs/1606.04474>

**Check it out at NIPS:**Tue Dec 6th 06:00 - 09:30 PM @ Area 5+6+7+8 #9
Thursday Dec 8th 02:00 - 9:30 PM @ Area 1+2 (Deep Learning Symposium - Poster)
Friday Dec 9th 08:00 AM - 06:30 PM @ Area 1 (DeepRL Workshop - Talk by Nando De Freitas)
Friday Dec 9th 08:00 AM - 06:30 PM @ Area 5+6 (Nonconvex Optimization for Machine Learning: Theory and Practice - Talk by Nando De Freitas)
Saturday Dec 10th 08:00 AM - 6:30 PM @ Area 2 (Optimizing the Optimizers - Talk by Matthew W. Hoffman)

## An Online Sequence-to-Sequence Model Using Partial Conditioning

**Authors:** Navdeep Jaitly, Quoc V. Le, Oriol Vinyals, Ilya Sutskever, David Sussillo, Samy Bengio

![Diagram of an online sequence-to-sequence model using partial conditioning, showing the interaction between the encoder and transducer layers.](https://lh3.googleusercontent.com/DMg4X_XVZv27ROfuZgBMZmflL2zjsJl7Ip8O751YeBJR5V1_VUbp4c44JjQnCWIAYCosfLYQ0XLaZgLByMNucXzgHul7E5_R09swlzAS0fAEJNqpY1M=w1440)

Models which map from a sequence of observations to another sequence (sequence-to-sequence) have become extremely popular in the last two years due to their generality, achieving state-of-the-art results in a variety of tasks such as translation, captioning, or parsing. The main drawback of these models is that they need to read in the whole sequence of inputs “x” before starting producing the resulting output sequence “y”. In our paper we circumvent these limitations by allowing the model to emit output symbols before the whole input sequence has been read. Although this introduces some independence assumptions, making online decisions in certain domains such as speech recognition or machine translation makes these models much more desirable.

For further details and related work, please see the paper<http://papers.nips.cc/paper/6594-an-online-sequence-to-sequence-model-using-partial-conditioning.pdf>

**Check it out at NIPS:**Tue Dec 6th 06:00 - 09:30 PM @ Area 5+6+7+8 #53

## Memory-Efficient Backpropagation through time

**Authors:** Audrunas Gruslys, Remi Munos, Ivo Danihelka, Marc Lanctot, Alex Graves

Many state of art results were achieved by training large recurrent models over long sequences of input data. Training recurrent networks is not an easy task for many reasons. One of complications is a large memory consumption of the standard backpropagation through time (BPTT) algorithm, as it requires memorizing all or almost all past neuron activations. It is especially easy to run out of expensive GPU memory when training convolutional RNNs, and memory constraints often lead to unwanted compromises in network size. A common solution used to alleviate this problem is to memorize only some of intermediate neuron activations and recompute others on demand. While there were many heuristics that trade off memory and computation, most of them are adapted for certain edge cases and are suboptimal. We viewed the problem as a dynamic programming problem which allowed us to find a class of provably optimal strategies subject to memory constraints. For sequences of length 1000, our algorithm saves 95% of memory usage while using only one third more time per learning step than the standard BPTT.

For further details and related work, please see the paper [https://papers.nips.cc/paper/6220-memory-efficient-backpropagation-through-time.pdf](https://arxiv.org/abs/1606.03401)

**Check it out at NIPS:**Tue Dec 6th 06:00 - 09:30 PM @ Area 5+6+7+8 #64

## Towards Conceptual Compression

**Authors:** Karol Gregor, Frederic Besse, Danilo Rezende, Ivo Danihelka, Daan Wierstra

Discovering high level abstract representations is one of the primary goals of unsupervised learning. We approach this problem by designing an architecture that transforms the information stored in pixels into an ordered sequence of information carrying representations. Training results in an emergent order, where early representations carry information about the more global & conceptual aspects of the image, while the latter representations correspond to the details. The model is a fully convolutional, sequential variational autoencoder inspired by DRAW. The architecture is simple and homogeneous and therefore does not require many design choices.

The resulting information transformation can be used for lossy compression, by transmitting only the early set of representations (the number of which is given by the desired compression level) and generating the remaining ones as well as the image using the generative model. If the ordering of information that the model discovers correlates strongly with the ordering of information by importance as judged by humans, then the algorithm will transmit what humans consider to be the most important. If the generation of the remaining variables results in a high quality image, this method should lead to high quality lossy compression. Because both humans and unsupervised algorithms try to understand data and because both use deep networks to do so, there is a good reason to believe that this approach will work. We demonstrate that this is indeed the case and the current model already results in performance that compares favorably to that of JPEG and JPEG 2000. As generative models are progressively getting better, these results demonstrate the potential of this method for building future compression algorithms.

For further details and related work, please see the paper <http://papers.nips.cc/paper/6542-towards-conceptual-compression.pdf>

**Check it out at NIPS:**Tue Dec 6th 06:00 - 09:30 PM @ Area 5+6+7+8 #77

## Unsupervised Learning of 3D Structure from Images

**Authors:** Danilo Rezende, Ali Eslami, Shakir Mohamed, Peter Battaglia, Max Jaderberg, Nicolas Heess

![Architecture diagram of an unsupervised 3D structure learning model, showing the flow from training inputs through an inference network and a 3D structure model to a learned or specified renderer.](https://lh3.googleusercontent.com/mtak3QbTGXQ04Bo94QuVIIBJsX1VmYak1k7QDw14g0J4nlmrswYukcuCyveOhD5lxDvapLojjhRcG5wdbhpcw4EHgrO1dBqDqpZCV7mQn3v3laOe1g=w1440)

Imagine looking at a photograph of a chair. The image you see will be a complex function of the attributes and positions of the camera, the lights and, of course of the shape of the chair. Importantly, due to self-occlusion you never see the full chair, so there is an infinite number chair-like objects that would be consistent with what you see. Nevertheless, when asked how to imagine the chair's shape from a different point of view you will probably be able to do so quite accurately. Key to this ability is not just an implicit understanding of perspective, occlusion and the image formation process, but critically your prior knowledge of what a plausible chair ought to look like, which allows you to “fill in” the missing parts.

In this paper we study models that are able to perform similar types of reasoning. Specifically, we formulate generative models which can learn about the statistical regularities of the three-dimensional shape of objects. The resulting prior over shapes produces high-quality samples, and allows us to formulate challenging ill-posed problems such as that of recovering plausible 3D structures given a 2D image as probabilistic inference, accurately capturing the multi-modality of the posterior. This inference can be achieved rapidly with a single forward-pass through a neural network and we show how both the models and inference networks can be trained end-to-end directly from 2D images without any use of ground-truth 3D labels, therefore demonstrating for the first time the feasibility of learning to infer 3D representations of the world in a purely unsupervised manner.

For further details and related work, please see the paper <https://arxiv.org/abs/1607.00662> and our video: <https://www.youtube.com/watch?v=stvDAGQwL5c>

**Check it out at NIPS:**Wed Dec 7th 06:00 - 09:30 PM @ Area 5+6+7+8 #2
