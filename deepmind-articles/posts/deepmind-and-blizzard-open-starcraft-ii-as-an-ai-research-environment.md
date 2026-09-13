---
title: "DeepMind and Blizzard open StarCraft II as an AI research environment"
source: https://deepmind.google/blog/deepmind-and-blizzard-open-starcraft-ii-as-an-ai-research-environment/
site: deepmind
date: 2017-08-09
authors: Oriol Vinyals, Stephen Gaffney, Timo Ewalds
crawled: 2026-09-13
---

DeepMind's scientific mission is to push the boundaries of AI by developing systems that can learn to solve complex problems. To do this, we design agents and test their ability in a wide range of environments from the purpose-built [DeepMind Lab](https://arxiv.org/pdf/1612.03801.pdf) to established games, such as [Atari](https://github.com/mgbellemare/Arcade-Learning-Environment) and [Go](https://deepmind.com/research/case-studies/alphago-the-story-so-far).

Testing our agents in games that are not specifically designed for AI research, and where humans play well, is crucial to benchmark agent performance. That is why we, along with our [partner Blizzard Entertainment](https://starcraft2.com/en-us/), are excited to announce the release of SC2LE, a set of tools that we hope will accelerate AI research in the real-time strategy game StarCraft II. The SC2LE release includes:

- A [Machine Learning API](https://github.com/Blizzard/s2client-proto) developed by Blizzard that gives researchers and developers hooks into the game. This includes the release of tools for Linux for the first time.
- A [dataset of anonymised game replays](https://github.com/Blizzard/s2client-proto#replay-packs), which will increase from 65k to more than half a million in the coming weeks.
- An open source version of DeepMind’s toolset, [PySC2](https://github.com/deepmind/pysc2), to allow researchers to easily use Blizzard’s feature-layer API with their agents.
- A series of simple RL mini-games to allow researchers to test the performance of agents on specific tasks.
- A [joint paper](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/deepMind-and-blizzard-open-starcraft-ii-as-an-ai-research-environment/sc2le.pdf) that outlines the environment, and reports initial baseline results on the mini-games, supervised learning from replays, and the full 1v1 ladder game against the built-in AI.

![A futuristic control panel from StarCraft II featuring illuminated green holographic screens, buttons, and switches.](https://lh3.googleusercontent.com/5zO_kwU78AYi-WFYhkuHDAEe5PtFk8HyW6ERBaVuBePBTSU5Usw5zTRtGHeGn4-1JZfylEnMu1EhX_7wVbckP1jqKvBeX2zHpoA5o6_QXdS1bAAXKqM=w1440)

StarCraft II is a science-fiction based real-time strategy game, released in 2010

StarCraft and StarCraft II are among the biggest and most successful games of all time, with players competing in tournaments for more than 20 years. The original game is also already used by AI and ML researchers, who compete annually in the [AIIDE bot competition](http://www.cs.mun.ca/~dchurchill/starcraftaicomp/). Part of StarCraft’s longevity is down to the rich, multi-layered gameplay, which also makes it an ideal environment for AI research.

For example, while the objective of the game is to beat the opponent, the player must also carry out and balance a number of sub-goals, such as gathering resources or building structures. In addition, a game can take from a few minutes to one hour to complete, meaning actions taken early in the game may not pay-off for a long time. Finally, the map is only partially observed, meaning agents must use a combination of memory and planning to succeed.

The game also has other qualities that appeal to researchers, such as the large pool of avid players that compete online every day. This ensures that there is a large quantity of replay data to learn from - as well as a large quantity of extremely talented opponents for AI agents.

Even StarCraft’s action space presents a challenge with a choice of more than 300 basic actions that can be taken. Contrast this with Atari games, which only have about 10 (e.g. up, down, left, right etc). On top of this, actions in StarCraft are hierarchical, can be modified and augmented, with many of them requiring a point on the screen. Even assuming a small screen size of 84x84 there are roughly 100 million possible actions available.

![A StarCraft II gameplay visualization showing a small blue unit with a green health bar, with labeled sections below for Human Actions, Agent Actions, and Available Actions.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/622662820ee9d9abfa26f4e3_StarCraft2022002.gif)

Actions available to both humans and agents depend on the units selected

This release means researchers can now tackle some of these challenges using Blizzard’s own tools to build their own tasks and models.

Our [PySC2](https://github.com/deepmind/pysc2) environment wrapper helps by offering a flexible and easy-to-use interface for RL agents to play the game. In this initial release, we break the game down into “feature layers”, where elements of the game such as unit type, health and map visibility are isolated from each other, whilst preserving the core visual and spatial elements of the game.

The release also contains a series of ‘mini-games’ - an established technique for breaking down the game into manageable chunks that can be used to test agents on [specific](https://arxiv.org/abs/1703.10069)[tasks](https://arxiv.org/abs/1609.02993), such as moving the camera, [collecting mineral shards](https://youtu.be/6L448yg0Sm0) or selecting units. We hope that researchers can test their techniques on these as well as propose new mini-games for other researchers to compete and evaluate on.

Our initial investigations show that our agents perform well on these mini-games. But when it comes to the full game, even strong baseline agents, such as [A3C](https://arxiv.org/abs/1602.01783), cannot win a single game against even the easiest built-in AI. For instance, the following video shows an early-stage training agent (left) which fails to keep its workers mining, a task that humans find trivial. After training (right), the agents perform more meaningful actions, but if they are to be competitive, we will need further breakthroughs in deep RL and related areas.

One technique that we know allows our agents to learn stronger policies is imitation learning. This kind of training will soon be far easier thanks to Blizzard, which has committed to ongoing releases of hundreds of thousands of anonymised replays gathered from the StarCraft II ladder. These will not only allow researchers to train supervised agents to play the game, but also opens up other interesting areas of research such as sequence prediction and long-term memory.

Our hope is that the release of these new tools will build on the work that the AI community has already done in StarCraft, encouraging more DeepRL research and making it easier for researchers to focus on the frontiers of our field.

We look forward to seeing what the community discovers.

**Notes**

Read more on the [Blizzard blog](https://starcraft2.com/en-us/).

PySC2 is available from [DeepMind’s github page](https://github.com/deepmind/pysc2).

Blizzard’s StarCraft API is available [here](https://github.com/Blizzard/s2client-proto), with details on how to get the linux version, replays and other elements.

If you use our environment in your research, please cite [the release paper.](https://deepmind.com/research/publications/Starcraft-II-A-New-Challenge-for-Reinforcement-Learning)
