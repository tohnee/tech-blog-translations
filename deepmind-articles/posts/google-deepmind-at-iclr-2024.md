---
title: "Google DeepMind at ICLR 2024"
source: https://deepmind.google/blog/google-deepmind-at-iclr-2024/
site: deepmind
date: 2024-05-03
authors: 
crawled: 2026-09-13
---

Developing next-gen AI agents, exploring new modalities, and pioneering foundational learning

Next week, AI researchers from around the globe will converge at the 12th [International Conference on Learning Representations](https://iclr.cc/) (ICLR), set to take place May 7-11 in Vienna, Austria.

Raia Hadsell, Vice President of Research at Google DeepMind, will deliver a keynote reflecting on the last 20 years in the field, highlighting how lessons learned are shaping the future of AI for the benefit of humanity.

We’ll also offer live demonstrations showcasing how we bring our foundational research into reality, from the development of [Robotics Transformers](https://deepmind.google/discover/blog/shaping-the-future-of-advanced-robotics/) to the creation of toolkits and open-source models like [Gemma](https://blog.google/technology/developers/gemma-open-models/).

Teams from across Google DeepMind will present more than 70 papers this year. Some research highlights:

[Google Research at ICLR 2024](https://research.google/conferences-and-events/google-at-iclr-2024/)

## Problem-solving agents and human-inspired approaches

Large language models (LLMs) are already revolutionizing advanced AI tools, yet their full potential remains untapped. For instance, LLM-based AI agents capable of taking effective actions could transform digital assistants into more helpful and intuitive AI tools.

AI assistants that follow natural language instructions to carry out web-based tasks on people’s behalf would be a huge timesaver. In an oral presentation we introduce [WebAgent](https://openreview.net/pdf?id=9JQtrumvg8), an LLM-driven agent that learns from self-experience to navigate and manage complex tasks on real-world websites.

To further enhance the general usefulness of LLMs, we focused on boosting their problem-solving skills. We demonstrate how we achieved this by equipping an LLM-based system with a traditionally human approach: [producing and using “tools”](https://openreview.net/forum?id=qV83K9d5WB). Separately, we present a training technique that ensures language models produce more consistently [socially acceptable outputs. Our approach](https://openreview.net/forum?id=NddKiWtdUm) uses a sandbox rehearsal space that represents the [values of society](https://deepmind.google/discover/blog/the-ethics-of-advanced-ai-assistants/).

## Pushing boundaries in vision and coding

![A grid of animated video clips showing various camera angles of everyday objects, including a Go board, mugs, keys, food, and indoor scenes, illustrating the Dynamic Scene Transformer (DyST) model's ability to generate 3D video representations from different perspectives.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/Figure-1.gif)

Our Dynamic Scene Transformer (DyST) model leverages real-world single-camera videos to extract 3D representations of objects in the scene and their movements.

Until recently, large AI models mostly focused on text and images, laying the groundwork for large-scale pattern recognition and data interpretation. Now, the field is progressing beyond these static realms to embrace the dynamics of real-world visual environments. As computing advances across the board, it is increasingly important that its underlying code is generated and optimized with maximum efficiency.

When you watch a video on a flat screen, you intuitively grasp the three-dimensional nature of the scene. Machines, however, struggle to emulate this ability without explicit supervision. We showcase our [Dynamic Scene Transformer](https://openreview.net/forum?id=MnMWa94t12) (DyST) model, which leverages real-world single-camera videos to extract 3D representations of objects in the scene and their movements. What’s more, DyST also enables the generation of novel versions of the same video, with user control over camera angles and content.

Emulating human cognitive strategies also makes for better AI code generators. When programmers write complex code, they typically “decompose” the task into simpler subtasks. With [ExeDec](https://openreview.net/pdf?id=oTRwljRgiv), we introduce a novel code-generating approach that harnesses a decomposition approach to elevate AI systems’ programming and generalization performance.

In a parallel [spotlight paper](https://openreview.net/forum?id=ix7rLVHXyY&referrer=%5BAuthor%20Console%5D%28%2Fgroup%3Fid%3DICLR.cc%2F2024%2FConference%2FAuthors%23your-submissions) we explore the novel use of machine learning to not only generate code, but to optimize it, introducing a [dataset for the robust benchmarking of code performance](https://pie4perf.com/). Code optimization is challenging, requiring complex reasoning, and our dataset enables the exploration of a range of ML techniques. We demonstrate that the resulting learning strategies outperform human-crafted code optimizations.

![Side-by-side comparison of code optimization: the left side displays complex, original C++ source code, while the right side shows "Generated Code" boasting a speedup of 18.80x.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/Figure_2.gif)

ExeDec introduces a novel code-generating approach that harnesses a decomposition approach to elevate AI systems’ programming and generalization performance

## Advancing foundational learning

Our research teams are tackling the big questions of AI - from exploring the essence of machine cognition to understanding how advanced AI models generalize - while also working to overcome key theoretical challenges.

For both humans and machines, causal reasoning and the ability to predict events are closely related concepts. In a spotlight presentation, we explore how [reinforcement learning is affected by prediction-based training objectives](https://openreview.net/forum?id=agPpmEgf8C), and draw parallels to changes in brain activity also linked to prediction.

When AI agents are able to generalize well to new scenarios is it because they, like humans, have learned an underlying causal model of their world? This is a critical question in advanced AI. In an oral presentation, we reveal that such models [have indeed learned an approximate causal model](https://openreview.net/forum?id=pOoKI3ouv1) of the processes that resulted in their training data, and discuss the deep implications.

Another critical question in AI is trust, which in part depends on how accurately models can estimate the uncertainty of their outputs - a crucial factor for reliable decision-making. We've made [significant advances in uncertainty estimation within Bayesian deep learning](https://openreview.net/forum?id=Sx7BIiPzys), employing a simple and essentially cost-free method.

Finally, we explore game theory’s Nash equilibrium (NE) - a state in which no player benefits from changing their strategy if others maintain theirs. Beyond simple two-player games, even approximating a Nash equilibrium is computationally intractable, but in an oral presentation, we [reveal new state-of-the-art approaches](https://openreview.net/forum?id=cc8h3I3V4E) in negotiating deals from poker to auctions.

## Bringing together the AI community

We’re delighted to sponsor ICLR and support initiatives including [Queer in AI](https://www.queerinai.com/) and [Women In Machine Learning.](https://www.wiml.org/) Such partnerships not only bolster research collaborations but also foster a vibrant, diverse community in AI and machine learning.

If you’re at ICLR, be sure to visit our booth and our [Google Research](https://research.google/conferences-and-events/google-at-iclr-2024/) colleagues next door. Discover our pioneering research, meet our teams hosting workshops, and engage with our experts presenting throughout the conference. We look forward to connecting with you!
