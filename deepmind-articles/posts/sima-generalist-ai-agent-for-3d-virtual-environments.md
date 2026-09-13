---
title: "A generalist AI agent for 3D virtual environments"
source: https://deepmind.google/blog/sima-generalist-ai-agent-for-3d-virtual-environments/
site: deepmind
date: 2024-03-13
authors: SIMA team
crawled: 2026-09-13
---

We present new research on a Scalable Instructable Multiworld Agent (SIMA) that can follow natural-language instructions to carry out tasks in a variety of video game settings

Video games are a key proving ground for artificial intelligence (AI) systems. Like the real world, games are rich learning environments with responsive, real-time settings and ever-changing goals.

From our [early work with Atari games](https://www.nature.com/articles/nature14236/), through to our [AlphaStar](https://deepmind.google/discover/blog/alphastar-grandmaster-level-in-starcraft-ii-using-multi-agent-reinforcement-learning/) system that plays StarCraft II at human-grandmaster level, Google DeepMind has a long history in AI and games.

Today, we’re announcing a new milestone - shifting our focus from individual games towards a general, instructable game-playing AI agent.

In a new [technical report](https://arxiv.org/abs/2404.10179), we introduce SIMA, short for Scalable Instructable Multiworld Agent, a generalist AI agent for 3D virtual settings. We partnered with game developers to train SIMA on a variety of video games. This research marks the first time an agent has demonstrated it can understand a broad range of gaming worlds, and follow natural-language instructions to carry out tasks within them, as a human might.

This work isn't about achieving high game scores. Learning to play even one video game is a technical feat for an AI system, but learning to follow instructions in a variety of game settings could unlock more helpful AI agents for any environment. Our research shows how we can translate the capabilities of advanced AI models into useful, real-world actions through a language interface. We hope that SIMA and other agent research can use video games as sandboxes to better understand how AI systems may become more helpful.

## Learning from video games

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

We collaborated with eight game studios to train and test SIMA on nine different video games.

To expose SIMA to many environments, we’ve built a number of partnerships with game developers for our research. We collaborated with eight game studios to train and test SIMA on nine different video games, such as No Man’s Sky by Hello Games and Teardown by Tuxedo Labs. Each game in SIMA’s portfolio opens up a new interactive world, including a range of skills to learn, from simple navigation and menu use, to mining resources, flying a spaceship, or crafting a helmet.

We also used four research environments - including a new environment we built with [Unity](https://deepmind.google/blog/using-unity-to-help-solve-intelligence/) called the Construction Lab, where agents need to build sculptures from building blocks which test their object manipulation and intuitive understanding of the physical world.

By learning from different gaming worlds, SIMA captures how language ties in with game-play behavior. Our first approach was to record pairs of human players across the games in our portfolio, with one player watching and instructing the other. We also had players play freely, then rewatch what they did and record instructions that would have led to their game actions.

![A diagram detailing the workflow for training the SIMA agent, moving left to right from "Environments" (including commercial games like Valheim and Teardown, and research environments like Construction Lab) to "Data" (data collection from human players), then to "Agents" (training using pretrained models), and finally to "Evaluation" (human evaluation of the agent carrying out a text instruction in-game).](https://lh3.googleusercontent.com/-gxeUygwIrMQel1FzsNH1cyThJZ9Wd2ZzwId17pmFxl5qXsQzXd74ZYgf5pAHqoNODEnFOOz9LytpXAAlcbSqO6Oild5sMLOFUsakRd63eVTlrJIQQ=w1440)

SIMA comprises pre-trained vision models, and a main model that includes a memory and outputs keyboard and mouse actions.

## SIMA: a versatile AI agent

SIMA is an AI agent that can perceive and understand a variety of environments, then take actions to achieve an instructed goal. It comprises a model designed for precise image-language mapping and a video model that predicts what will happen next on-screen. We finetuned these models on training data specific to the 3D settings in the SIMA portfolio.

Our AI agent doesn’t need access to a game's source code, nor bespoke APIs. It requires just two inputs: the images on screen, and simple, natural-language instructions provided by the user. SIMA uses keyboard and mouse outputs to control the games’ central character to carry out these instructions. This simple interface is what humans use, meaning SIMA can potentially interact with any virtual environment.

The current version of SIMA is evaluated across 600 basic skills, spanning navigation (e.g. "turn left"), object interaction ("climb the ladder"), and menu use ("open the map"). We’ve trained SIMA to perform simple tasks that can be completed within about 10 seconds.

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

SIMA was evaluated across 600 basic skills, spanning navigation, object interaction, and menu use.

We want our future agents to tackle tasks that require high-level strategic planning and multiple sub-tasks to complete, such as “Find resources and build a camp”. This is an important goal for AI in general, because while Large Language Models have given rise to powerful systems that can capture knowledge about the world and generate plans, they currently lack the ability to take actions on our behalf.

## Generalizing across games and more

We show an agent trained on many games was better than an agent that learned how to play just one. In our evaluations, SIMA agents trained on a set of nine 3D games from our portfolio significantly outperformed all specialized agents trained solely on each individual one. What’s more, an agent trained in all but one game performed nearly as well on that unseen game as an agent trained specifically on it, on average. Importantly, this ability to function in brand new environments highlights SIMA’s ability to generalize beyond its training. This is a promising initial result, however more research is required for SIMA to perform at human levels in both seen and unseen games.

Our results also show that SIMA’s performance relies on language. In a control test where the agent was not given any language training or instructions, it behaves in an appropriate but aimless manner. For example, an agent may gather resources, a frequent behavior, rather than walking where it was instructed to go.

![A bar chart showing the relative performance (%) of SIMA agents compared to an environment-specialized baseline (100%). The "Trained on all environments" agent scores highest at around 165%. The agent "Facing unseen environment" performs nearly as well as the baseline at roughly 90%. The agent "Given no language" performs poorly, scoring just above 30%.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/Sima_Fig4.svg)

We evaluated SIMA’s ability to follow instructions to complete nearly 1500 unique in-game tasks, in part using human judges. As our baseline comparison, we use the performance of environment-specialized SIMA agents (trained and evaluated to follow instructions within a single environment). We compare this performance with three types of generalist SIMA agents, each trained across multiple environments.

## Advancing AI agent research

SIMA’s results show the potential to develop a new wave of generalist, language-driven AI agents. This is early-stage research and we look forward to further building on SIMA across more training environments and incorporating more capable models.

As we expose SIMA to more training worlds, the more generalizable and versatile we expect it to become. And with more advanced models, we hope to improve SIMA’s understanding and ability to act on higher-level language instructions to achieve more complex goals.

Ultimately, our research is building towards more general AI systems and agents that can understand and safely carry out a wide range of tasks in a way that is helpful to people online and in the real world.

**Learn more about SIMA**

[Read our technical report](https://arxiv.org/abs/2404.10179)

We would like to thank all the paper authors: Maria Abi Raad, Arun Ahuja, Catarina Barros, Frederic Besse, Andrew Bolt, Adrian Bolton, Bethanie Brownfield, Gavin Buttimore, Max Cant, Sarah Chakera, Stephanie Chan, Jeff Clune, Adrian Collister, Vikki Copeman, Alex Cullum, Ishita Dasgupta, Julia Di Trapani, Yani Donchev, Martin Engelcke, Ryan Faulkner, Frankie Garcia, Charles Gbadamosi, Zhitao Gong, Lucy Gonzales, Karol Gregor, Kshitij Gupta, Arne Olav Hallingstad, Tim Harley, Sam Haves, Felix Hill, Ed Hirst, Drew Hudson, Jony Hudson, Steph Hughes-Fitt, Danilo J. Rezende, Mimi Jasarevic, Laura Kampis, Rosemary Ke, Thomas Keck, Junkyung Kim, Oscar Knagg, Kavya Kopparapu, Andrew Lampinen, Rory Lawton, Shane Legg, Alexander Lerchner, Marjorie Limont, Yulan Liu, Maria Loks-Thompson, Joseph Marino, Kathryn Martin Cussons, Loic Matthey, Siobhan Mcloughlin, Piermaria Mendolicchio, Hamza Merzic, Anna Mitenkova, Alexandre Moufarek, Valeria Oliveira, Yanko Oliveira, Hannah Openshaw, Renke Pan, Aneesh Pappu, Alex Platonov, Ollie Purkiss, David Reichert, John Reid, Pierre Harvey Richemond, Tyson Roberts, Giles Ruscoe, Jaume Sanchez Elias, Tasha Sandars, Daniel P. Sawyer, Tim Scholtes, Guy Simmons, Daniel Slater, Hubert Soyer, Heiko Strathmann, Peter Stys, Allison Tam, Tayfun Terzi, Davide Vercelli, Bojan Vujatovic, Marcus Wainwright, Jane X. Wang, Zhengdong Wang, Daan Wierstra, Duncan Williams, Nathaniel Wong, Sarah York and Nick Young.

Special thanks to all of the game developers who partnered with us: Coffee Stain (Valheim, Satisfactory, Goat Simulator 3), Foulball Hangover (Hydroneer), Hello Games (No Man's Sky), Keen Software House (Space Engineers), RubberbandGames (Wobbly Life), Strange Loop Games (Eco) and Tuxedo Labs & Saber Interactive (Teardown).
