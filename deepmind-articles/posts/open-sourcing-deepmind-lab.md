---
title: "Open-sourcing DeepMind Lab"
source: https://deepmind.google/blog/open-sourcing-deepmind-lab/
site: deepmind
date: 2016-12-03
authors: Charlie Beattie, Joel Leibo, Stig Petersen, Shane Legg
crawled: 2026-09-13
---

DeepMind's scientific mission is to push the boundaries of AI, developing systems that can learn to solve any complex problem without needing to be taught how. To achieve this, we work from the premise that AI needs to be general. Agents should operate across a wide range of tasks and be able to automatically adapt to changing circumstances. That is, they should not be pre-programmed, but rather, able to learn automatically from their raw inputs and reward signals from the environment. There are two parts to this research program: (1) designing ever-more intelligent agents capable of more-and-more sophisticated cognitive skills, and (2) building increasingly complex environments where agents can be trained and evaluated.

The development of innovative agents goes hand in hand with the careful design and implementation of rationally selected, flexible and well-maintained environments. To that end, we at DeepMind have invested considerable effort toward building rich simulated environments to serve as “laboratories” for AI research. Now we are open-sourcing our flagship platform, DeepMind Lab, so the broader research community can make use of it.

DeepMind Lab is a fully 3D game-like platform tailored for agent-based AI research. It is observed from a first-person viewpoint, through the eyes of the simulated agent. Scenes are rendered with rich science fiction-style visuals. The available actions allow agents to look around and move in 3D. The agent’s “body” is a floating orb. It levitates and moves by activating thrusters opposite its desired direction of movement, and it has a camera that moves around the main sphere as a ball-in-socket joint tracking the rotational look actions. Example tasks include collecting fruit, navigating in mazes, traversing dangerous passages while avoiding falling off cliffs, bouncing through space using launch pads to move between platforms, playing laser tag, and quickly learning and remembering random procedurally generated environments. An illustration of how agents in DeepMind Lab perceive and interact with the world can be seen below:

![Diagram showing DeepMind Lab agent's Observations (receiving raw pixel inputs and rewards like a green apple) and Actions (movement controls including jump, crouch, forward/back, strafe, and rotation).](https://lh3.googleusercontent.com/PS3Srq6kyMb_ILjWpEIjcJL9ygms26l_zRf2BzsRzAYQje1NQmmyKtoOv4LgcDp1cCWC1-HWcN-EXn4yLflGA7Qr57S3DurUxEbV5ZFep0gdeNIhdS0=w1440)

At each moment in time, agents observe the world as an image, in pixels, rendered from their own first-person perspective. They also may receive a reward (or punishment!) signal. The agent can activate its thrusters to move in 3D and can also rotate its viewpoint along both horizontal and vertical axes.

Artificial general intelligence research in DeepMind Lab emphasizes navigation, memory, 3D vision from a first person viewpoint, motor control, planning, strategy, time, and fully autonomous agents that must learn for themselves what tasks to perform by exploring their environment. All these factors make learning difficult. Each are considered frontier research questions in their own right. Putting them all together in one platform, as we have, represents a significant new challenge for the field.

DeepMind Lab is highly customisable and extendable. New levels can be authored with off-the-shelf editor tools. In addition, DeepMind Lab includes an interface for programmatic level-creation. Levels can be customised with gameplay logic, item pickups, custom observations, level restarts, reward schemes, in-game messages and more. The interface can be used to create levels in which novel map layouts are generated on the fly while an agent trains. These features are useful in, for example, testing how an agent copes with unfamiliar environments. Users will be able to add custom levels to the platform via GitHub. The assets will be hosted on GitHub alongside all the code, maps and level scripts. Our hope is that the community will help us shape and develop the platform going forward.

DeepMind Lab has been used internally at DeepMind for some time ([example](https://deepmind.com/blog/article/reinforcement-learning-unsupervised-auxiliary-tasks)). We believe it has already had a significant impact on our thinking concerning numerous aspects of intelligence, both natural and artificial. However, our efforts so far have only barely scratched the surface of what is possible in DeepMind Lab. There are opportunities for significant contributions still to be made in a number of mostly still untouched research domains now available through DeepMind Lab, such as navigation, memory and exploration.

As well as facilitating agent evaluation, there are compelling reasons to think that it may be fundamentally easier to develop intelligence in a 3D world, observed from a first-person viewpoint, like DeepMind Lab. After all, the only known examples of general-purpose intelligence in the natural world arose from a combination of evolution, development, and learning, grounded in physics and the sensory apparatus of animals. It is possible that a large fraction of animal and human intelligence is a direct consequence of the richness of our environment, and unlikely to arise without it. Consider the alternative: if you or I had grown up in a world that looked like Space Invaders or Pac-Man, it doesn’t seem likely we would have achieved much general intelligence!

**Notes**

Read the [full paper here](https://arxiv.org/abs/1612.03801)
Access DeepMind's GitHub repository [here](https://github.com/deepmind/lab).
