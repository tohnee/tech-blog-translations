---
title: "Google DeepMind’s latest research at ICML 2023"
source: https://deepmind.google/blog/google-deepmind-research-at-icml-2023/
site: deepmind
date: 2023-07-20
authors: 
crawled: 2026-09-13
---

Exploring AI safety, adaptability, and efficiency for the real world

Next week marks the start of the 40th [International Conference on Machine Learning](https://icml.cc/) (ICML 2023), taking place 23-29 July in Honolulu, Hawai'i.

ICML brings together the artificial intelligence (AI) community to share new ideas, tools, and datasets, and make connections to advance the field. From computer vision to robotics, researchers from around the world will be presenting their latest advances.

Our director for science, technology & society, Shakir Mohamed, will give a [talk on machine learning with social purpose](https://icml.cc/virtual/2023/invited-talk/21547), tackling challenges from healthcare and climate, taking a sociotechnical view, and strengthening global communities.

We’re proud to support the conference as a Platinum Sponsor and to continue working together with our long-term partners [LatinX in AI](https://www.latinxinai.org/), [Queer in AI](https://www.queerinai.com/), and [Women in Machine Learning](https://wimlworkshop.org/).

At the conference, we’re also showcasing demos on [AlphaFold](https://www.deepmind.com/research/highlighted-research/alphafold), our advances in [fusion science](https://deepmind.google/blog/accelerating-fusion-science-through-learned-plasma-control/), and new models like [PaLM-E](https://ai.googleblog.com/2023/03/palm-e-embodied-multimodal-language.html) for robotics and [Phenaki](https://sites.research.google/phenaki/) for generating video from text.

Google DeepMind researchers are presenting more than 80 new papers at ICML this year. As many papers were submitted before [Google Brain and DeepMind joined forces](https://deepmind.google/blog/announcing-google-deepmind/), papers initially submitted under a Google Brain affiliation will be included in a [Google Research blog](https://ai.googleblog.com/2023/07/google-at-icml-2023.html), while this blog features papers submitted under a DeepMind affiliation.

[View the full ICML 2023 schedule](https://deepmind.events/events/icml-2023)

## AI in the (simulated) world

The success of AI that can read, write, and create is underpinned by foundation models – AI systems trained on vast datasets that can learn to perform many tasks. Our latest research explores how we can translate these efforts into the real world, and lays the groundwork for more generally capable and embodied AI agents that can better understand the dynamics of the world, opening up new possibilities for more useful AI tools.

In an oral presentation, we introduce [AdA](https://arxiv.org/abs/2301.07608), an AI agent that can adapt to solve new problems in a simulated environment, like humans do. In minutes, AdA can take on challenging tasks: combining objects in novel ways, navigating unseen terrains, and cooperating with other players

Likewise, we show how we could use [vision-language models to help train embodied agents](https://arxiv.org/abs/2301.12507) – for example, by telling a robot what it’s doing.

## The future of reinforcement learning

To develop responsible and trustworthy AI, we have to understand the goals at the heart of these systems. In reinforcement learning, one way this can be defined is through reward.

In an oral presentation, we aim to [settle the reward hypothesis](https://arxiv.org/abs/2212.10420#:~:text=The%20reward%20hypothesis%20posits%20that,to%20fully%20settle%20this%20hypothesis.) first posited by Richard Sutton stating that all goals can be thought of as maximising expected cumulative reward. We explain the precise conditions under which it holds, and clarify the kinds of objectives that can – and cannot – be captured by reward in a general form of the reinforcement learning problem.

When deploying AI systems, they need to be robust enough for the real-world. We look at how to better [train reinforcement learning algorithms within constraints](https://arxiv.org/abs/2302.01275), as AI tools often have to be limited for safety and efficiency.

In our research, which was recognised with an [ICML 2023 Outstanding Paper Award](https://icml.cc/Conferences/2023/Awards), we explore how we can teach models complex long-term strategy under uncertainty with [imperfect information games](https://arxiv.org/abs/2212.12567). We share how models can play to win two-player games even without knowing the other player's position and possible moves.

## Challenges at the frontier of AI

Humans can easily learn, adapt, and understand the world around us. Developing advanced AI systems that can generalise in human-like ways will help to create AI tools we can use in our everyday lives and to tackle new challenges.

One way that AI adapts is by quickly changing its predictions in response to new information. In an oral presentation, we look at [plasticity in neural networks](https://arxiv.org/abs/2303.01486#:~:text=We%20find%20that%20loss%20of,units%20or%20divergent%20gradient%20norms.) and how it can be lost over the course of training – and ways to prevent loss.

We also present research that could help explain the type of in-context learning that emerges in large language models by studying [neural networks meta-trained on data](https://arxiv.org/abs/2302.03067) sources whose statistics change spontaneously, such as in natural language prediction.

In an oral presentation, we introduce a new family of recurrent neural networks [(RNNs) that perform better on long-term reasoning tasks](https://arxiv.org/abs/2303.06349) to unlock the promise of these models for the future.

Finally, in ‘[quantile credit assignment](https://openreview.net/pdf?id=4yoLVter71)’ we propose an approach to disentangle luck from skill. By establishing a clearer relationship between actions, outcomes, and external factors, AI can better understand complex, real-world environments.
