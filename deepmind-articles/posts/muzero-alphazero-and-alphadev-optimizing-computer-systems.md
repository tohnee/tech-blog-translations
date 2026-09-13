---
title: "MuZero, AlphaZero, and AlphaDev: Optimizing computer systems"
source: https://deepmind.google/blog/muzero-alphazero-and-alphadev-optimizing-computer-systems/
site: deepmind
date: 2023-06-12
authors: 
crawled: 2026-09-13
---

As part of our aim to build increasingly capable and general artificial intelligence (AI) systems, we’re working to create AI tools with a broader understanding of the world. This can allow useful knowledge to be transferred between many different types of tasks.

Using reinforcement learning, our AI systems AlphaZero and MuZero have achieved superhuman performance playing games. Since then, we’ve expanded their capabilities to help design better computer chips, alongside optimizing data centers and video compression. And our specialized version of AlphaZero, called AlphaDev, has also discovered new algorithms for accelerating software at the foundations of our digital society.

Early results have shown the transformative potential of more general-purpose AI tools. Here, we explain how these advances are shaping the future of computing — and already helping billions of people and the planet.

![](https://lh3.googleusercontent.com/dzUtBJ3epFNS_8F38J-3fuK-mwCLWNNMbXjjxTCHUHbgOllAqj5npzEv9NHHyYGjPsYoldmvxxWNbdLAyKXKEeFyJZ_ZHC2wuEZJ_G1pq2bApFnDCQ=w1440-h810-n-nu)

## Designing better computer chips

Specialized hardware is essential to making sure today's AI systems are resource-efficient for users at scale. But designing and producing new computer chips can take years of work.

Our researchers have developed an AI-based approach to design more powerful and efficient circuits. By treating a circuit like a neural network, we found a way to accelerate chip design and take performance to new heights.

Neural networks are often designed to take user inputs and generate outputs, like images, text, or video. Inside the neural network, edges connect to nodes in a graph-like structure.

To create a circuit design, our team proposed circuit neural networks’, a new type of neural network which turns edges into wires and nodes into logic gates, and learns how to connect them together.

![Diagram of a circuit neural network, showing how binary circuit inputs pass through three hidden layers of logic gates connected by a dense web of dashed lines to produce circuit outputs.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/64be3d05d906a15808441b38_64b659c99dad7b8061b8a6f8_CHIP-_FIGX-5-01_goqZXL2.gif)

Animated illustration of a circuit neural network learning a circuit design. It determines which edges (wires) connect to which nodes (logic gates) to improve the overall circuit design.

We optimized the learned circuit for computational speed, energy efficiency, and size, while maintaining its functionality. Using 'simulated annealing', a classical search technique that looks one step into the future, we also tested different options to find its optimal configuration.

With this technique, we won the [IWLS 2023 Programming Contest](https://www.iwls.org/contest/) — with the best solution on 82% of circuit design problems in the competition.

Our team also used AlphaZero, which can look many steps into the future, to improve the circuit design by treating the challenge like a game to solve.

So far, our research combining circuit neural networks with the reward function of reinforcement learning has shown very promising results for building even more advanced computer chips.

![An isometric vector illustration mapping out Google DeepMind’s AI systems—AlphaZero, MuZero, and AlphaDev—as interconnected, colorful paths of a computer board game, featuring elements like chess pieces, video frames, computer chips, and game controllers.](https://lh3.googleusercontent.com/kYbwB0FNBt9SlVGZ7OKUAKbz0Lms1tOlEjDuowkDzkKkId8rgUyvJlYUSHT4XwIvxrx_bniAmO3oWgeavhEQqKqfwnCGfMrAPuILMZEAkN0TCJlC=w1440)

## Optimising data centre resources

Data centers manage everything from delivering search results to processing datasets. Like a game of multi-dimensional Tetris, a system called [Borg](https://storage.googleapis.com/pub-tools-public-publication-data/pdf/43438.pdf) manages and optimizes workloads within Google’s vast data centers.

To schedule tasks, Borg relies on manually-coded rules. But at Google’s scale, manually-coded rules can’t cover the variety of ever-changing workload distributions. So they are designed as one size to best fit all .

This is where machine learning technologies like AlphaZero are especially helpful: they are able to work at scale, automatically creating individual rules that are optimally tailored for the various workload distributions.

During its training, AlphaZero learned to recognise patterns in tasks coming into the data centers, and also learned to predict the best ways to manage capacity and make decisions with the best long-term outcomes.

When we applied AlphaZero to Borg in experimental trials, we found we could reduce the proportion of underused hardware in the data center by up to 19%.

![An isometric vector illustration side-by-side comparison of data center optimization, featuring a clean, empty blue wireframe cube labeled "Optimised" next to an identical wireframe cube labeled "Unoptimised" that is cluttered with various colorful, disorganized 3D blocks.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/64807c135294d98635791646_6464c6b5be889dc90e670f40_Figure202.gif)

An animated visualization of neat, optimized data storage, versus messy and unoptimized storage.

## Compressing video efficiently

Video streaming makes up the majority of internet traffic. So finding ways to make streaming more efficient, however big or small, will have a huge impact on the millions of people watching videos every day.

We worked with YouTube to compress and transmit video using MuZero’s problem-solving abilities. [By reducing the bitrate by 4%, MuZero enhanced the overall YouTube experience](https://www.deepmind.com/blog/muzeros-first-step-from-research-into-the-real-world) — without compromising on visual quality.

We initially applied MuZero to optimize the compression of each individual video frame. Now, we’ve expanded this work to help make decisions on how frames are grouped and referenced during encoding, leading to more bitrate savings.

Results from these first two steps show great promise of MuZero’s potential to become a more generalized tool, helping find optimal solutions across the entire video compression process.

![An abstract white line diagram showing a sequence of steps where video frames are grouped and compressed, illustrating MuZero’s video compression process.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/64807c135294d9863579165c_6464ba81cad8de9f10319887_Copy20of20Figure1.gif)

A visualization demonstrating how MuZero compresses video files. It defines groups of pictures with visual similarities for compression. A single keyframe is compressed. MuZero then compresses other frames, using the keyframe as a reference. The process repeats for the rest of the video, until compression is complete.

## Discovering faster algorithms

[AlphaDev](https://www.deepmind.com/blog/alphadev-discovers-faster-sorting-algorithms), a version of AlphaZero, made a novel breakthrough in computer science, when it discovered faster sorting and hashing algorithms. These fundamental processes are used trillions of times a day to sort, store, and retrieve data.

**AlphaDev’s sorting algorithms**

Sorting algorithms help digital devices process and display information, from ranking online search results and social posts, to user recommendations.

AlphaDev discovered an algorithm that increases efficiency for sorting short sequences of elements by 70% and by about 1.7% for sequences containing more than 250,000 elements, compared to the algorithms in the C++ library. That means results generated from user queries can be sorted much faster. When used at scale, this saves huge amounts of time and energy.

**AlphaDev’s hashing algorithms**

Hashing algorithms are often used for data storage and retrieval, like in a customer database. They typically use a key (e.g. user name “Jane Doe”) to generate a unique hash, which corresponds to the data values that need retrieving (e.g. “order number 164335-87”).

Like a librarian who uses a classification system to quickly find a specific book, with a hashing system, the computer already knows what it’s looking for and where to find it. When applied to the 9-16 bytes range of hashing functions in data centers, AlphaDev’s algorithm improved the efficiency by 30%.

**The impact of these algorithms**

We added the sorting algorithms to the [LLVM standard C++ library](https://reviews.llvm.org/D118029) — replacing sub-routines that have been used for over a decade. And contributed AlphaDev’s hashing algorithms to the [abseil library](https://abseil.io/docs/cpp/guides/hash).

Since then, millions of developers and companies have started using them across industries as diverse as cloud computing, online shopping, and supply chain management.

![An isometric vector illustration in shades of green, purple, and black, depicting a central computing cube connected via a winding circuit-board-like track to four glass spheres, each representing areas of technological optimization: a house, an autonomous vehicle, a lightning bolt for energy, and a heart with an EKG line.](https://lh3.googleusercontent.com/SOV2QO8AGpIp8ph-GvybvqXj6HF1IIhHEcu68BMD6zCub9YGMkJxG6pdTvQDbl0r4zMfbFXRo9S_18XabydvzkTimT8Q8xaKW3dYu883_9ru6m8Upg=w1440)

## General-purpose tools to power our digital future

Our AI tools are already saving billions of people time and energy. This is just the start. We envision a future where general-purpose AI tools can help optimize the global computing ecosystem.

We’re not there yet — we still need faster, more efficient, and sustainable digital infrastructure.

Many more theoretical and technological breakthroughs are needed to create fully generalized AI tools. But the potential of these tools — across technology, science, and medicine — makes us excited about what's on the horizon.

**Learn more about AlphaDev**

[Read paper](https://www.nature.com/articles/s41586-023-06004-9)
