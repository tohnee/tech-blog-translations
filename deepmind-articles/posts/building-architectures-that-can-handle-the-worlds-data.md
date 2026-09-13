---
title: "Building architectures that can handle the world’s data"
source: https://deepmind.google/blog/building-architectures-that-can-handle-the-worlds-data/
site: deepmind
date: 2021-08-03
authors: Drew Jaegle, João Carreira, Carl Doersch, David Ding, Catalin Ionescu
crawled: 2026-09-13
---

Perceiver and Perceiver IO work as multi-purpose tools for AI

Most architectures used by AI systems today are specialists. A 2D residual network may be a good choice for processing images, but at best it’s a loose fit for other kinds of data — such as the Lidar signals used in self-driving cars or the torques used in robotics. What’s more, standard architectures are often designed with only one task in mind, often leading engineers to bend over backwards to reshape, distort, or otherwise modify their inputs and outputs in hopes that a standard architecture can learn to handle their problem correctly. Dealing with more than one kind of data, like the sounds and images that make up videos, is even more complicated and usually involves complex, hand-tuned systems built from many different parts, even for simple tasks. As part of DeepMind's mission of solving intelligence to advance science and humanity, we want to build systems that can solve problems that use many types of inputs and outputs, so we began to explore a more general and versatile architecture that can handle all types of data.

![Diagram of the Perceiver IO architecture showing the flow from Input Array through Encode, Process, and Decode blocks to the final Output Array, utilizing a Latent Array and Output Query Array.](https://lh3.googleusercontent.com/KcLLFZfiq3COmFqB6qd__g_YOdmKQ-qvCmKmRlo2FnYuUpuC0Jbi_t3hrSApqScKKjSvQLD7EH82RrsOXfvkMqUesXWF_jON_FyXc8fRktnX70KbDQ=w1440)

Figure 1. The Perceiver IO architecture maps input arrays to output arrays by means of a small latent array, which lets it scale gracefully even for very large inputs and outputs. Perceiver IO uses a global attention mechanism that generalizes across many different kinds of data.

In a paper presented at [ICML 2021](https://icml.cc/) (the International Conference on Machine Learning) and [published as a preprint on arXiv](https://arxiv.org/abs/2103.03206), we introduced the Perceiver, a general-purpose architecture that can process data including images, point clouds, audio, video, and their combinations. While the Perceiver could handle many varieties of input data, it was limited to tasks with simple outputs, like classification. A [new preprint on arXiv](https://arxiv.org/abs/2107.14795) describes Perceiver IO, a more general version of the Perceiver architecture. Perceiver IO can produce a wide variety of outputs from many different inputs, making it applicable to real-world domains like language, vision, and multimodal understanding as well as challenging games like StarCraft II. To help researchers and the machine learning community at large, we’ve now [open sourced the code](https://github.com/deepmind/deepmind-research/tree/master/perceiver).

![Diagram showing text analysis examples categorized by "Local," "Periodic," and "Syntactic elements," illustrating how different words and punctuation marks in a joke about a bear are highlighted to demonstrate the model's attention patterns.](https://lh3.googleusercontent.com/IgHvJn3pfIBpwwOwyar4dt4CTibzoLHEiBygEJ79F2bmVTakSB5VLKNE9Wj9DQvDy15OdoH2XQT96LBecuvPksYmifvahUsUxF9AhUwYQrapxmpQ=w1440)

Figure 2. Perceiver IO processes language by first choosing which characters to attend to. The model learns to use several different strategies: some parts of the network attend to specific places in the input, while others attend to specific characters like punctuation marks.

Perceivers build on the [Transformer](https://en.wikipedia.org/wiki/Transformer_(machine_learning_model)), an architecture that uses an operation called “attention” to map inputs into outputs. By comparing all elements of the input, Transformers process inputs based on their relationships with each other and the task. Attention is simple and widely applicable, but Transformers use attention in a way that can quickly become expensive as the number of inputs grows. This means Transformers work well for inputs with at most a few thousand elements, but common forms of data like images, videos, and books can easily contain millions of elements. With the original Perceiver, we solved a major problem for a generalist architecture: scaling the Transformer’s attention operation to very large inputs without introducing domain-specific assumptions. The Perceiver does this by using attention to first encode the inputs into a small latent array. This latent array can then be processed further at a cost independent of the input’s size, enabling the Perceiver’s memory and computational needs to grow gracefully as the input grows larger, even for especially deep models.

![An animated split-screen comparison: the top panel shows workers in real life moving sugar cane stalks on a conveyor belt, and the bottom panel shows the Perceiver IO model's optical flow visualization tracking the motion of those same elements using a rainbow of colors to represent the movement direction of each point in the frame.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/fig_3a.gif)

![An animated split-screen comparison: the top panel shows a woman walking through a flock of scattering pigeons in a public square, and the bottom panel shows the Perceiver IO model's optical flow visualization tracking the motion of the woman and each flying bird using a vibrant array of colors to represent their movement direction.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/fig_3b.gif)

![An animated split-screen comparison: the top panel shows a group of dancers in traditional attire performing a ceremony in front of a temple, and the bottom panel shows the Perceiver IO model's optical flow visualization tracking the motion of each dancer using a vibrant array of colors to represent their movement direction.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/fig_3c.gif)

![A diagram of colorful arrows pointing outward from a central point, forming a circular color wheel that represents the mapping of motion direction to color in optical flow visualization.](https://lh3.googleusercontent.com/vct_DvboFWGKkNH8DDC38drvFect9ZFV-ikay93ChPTURa0_4hBI_4XSwNiUGtNFXnxpUAWlhFOfiJka0JOXe9W6SYYEbcLpCL5as_dwa7VftxbxWiY=w1440)

Figure 3. Perceiver IO produces state-of-the-art results on the challenging task of optical flow estimation, or tracking the motion of all pixels in an image. The colour of each pixel shows the direction and speed of motion estimated by Perceiver IO, as indicated in the legend above.

This “graceful growth” allows the Perceiver to achieve an unprecedented level of generality — it’s competitive with domain-specific models on benchmarks based on images, 3D point clouds, and audio and images together. But because the original Perceiver produced only one output per input, it wasn’t as versatile as researchers needed. Perceiver IO fixes this problem by using attention not only to encode to a latent array but also to decode from it, which gives the network great flexibility. Perceiver IO now scales to large and diverse inputs and outputs, and can even deal with many tasks or types of data at once. This opens the door for all sorts of applications, like understanding the meaning of a text from each of its characters, tracking the movement of all points in an image, processing the sound, images, and labels that make up a video, and even playing games, all while using a single architecture that’s simpler than the alternatives.

Original

Perceiver IO

Original

Perceiver IO

Original

Perceiver IO

In our experiments, we’ve seen Perceiver IO work across a wide range of benchmark domains — such as language, vision, multimodal data, and games — to provide an off-the-shelf way to handle many kinds of data. We hope [our latest preprint](https://arxiv.org/abs/2107.14795) and the code [available on Github](https://github.com/deepmind/deepmind-research/tree/master/perceiver) help researchers and practitioners tackle problems without needing to invest the time and effort to build custom solutions using specialised systems. As we continue to learn from exploring new kinds of data, we look forward to further improving upon this general-purpose architecture and making it faster and easier to solve problems throughout science and machine learning.
