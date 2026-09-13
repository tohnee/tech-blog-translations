---
title: "Learning by playing"
source: https://deepmind.google/blog/learning-by-playing/
site: deepmind
date: 2018-02-28
authors: Martin Riedmiller, Roland Hafner
crawled: 2026-09-13
---

Getting children (and adults) to tidy up after themselves can be a challenge, but we face an even greater challenge trying to get our AI agents to do the same. Success depends on the mastery of several core visuo-motor skills: approaching an object, grasping and lifting it, opening a box and putting things inside of it. To make matters more complicated, these skills must be applied in the right sequence.

Control tasks, like tidying up a table or stacking objects, require an agent to determine how, when and where to coordinate the nine joints of its simulated arms and fingers to move correctly and achieve its objective. The sheer number of possible combinations of movements at any given time, along with the need to carry out a long sequence of correct actions constitute a serious exploration problem—making this a particularly interesting area for reinforcement learning research.

Techniques like reward shaping, apprenticeship learning or learning from demonstrations can help with the exploration problem. However, these methods rely on a considerable amount of knowledge about the task—the problem of learning complex control problems from scratch with minimal prior knowledge is still an open challenge.

Our [new paper](https://arxiv.org/abs/1802.10567) proposes a new learning paradigm called ‘Scheduled Auxiliary Control (SAC-X)’ which seeks to overcome this exploration issue. SAC-X is based on the idea that to learn complex tasks from scratch, an agent has to learn to explore and master a set of basic skills first. Just as a baby must develop coordination and balance before she crawls or walks—providing an agent with internal (auxiliary) goals corresponding to simple skills increases the chance it can understand and perform more complicated tasks.

![An animated sequence showing a simulated robotic arm practicing manipulation tasks by interacting with a red and a green block on a tabletop.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62267c4938ec8f7177c7d560_Learning20by20playing.gif)

We demonstrate the SAC-X approach on several simulated and real robot tasks using a variety of tasks including stacking problems with different objects and ‘tidying up a playground’, which involves moving objects into a box. The auxiliary tasks we define follow a general principle: they encourage the agent to explore its sensor space. For example, activating a touch sensor in its fingers, sensing a force in its wrist, maximising a joint angle in its proprioceptive sensors or forcing a movement of an object in its visual camera sensors. Each task is associated with a simple reward of one if the goal is achieved, and zero otherwise.

![An animated sequence showing a simulated robotic arm practicing manipulation tasks by interacting with a red and a green block on a tabletop.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62267d28f70ee120ddd63bbb_unnamed_1.gif)

The first thing the agent learns is to activate its touch sensors in the fingers and to move both objects.

![An animated sequence showing a simulated robotic arm practicing manipulation tasks by interacting with a red and a green block on a tabletop.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62267d46801fc6e300b17d42_unnamed-2.gif)

The simulated agent eventually masters the complex task of ‘stacking’ objects.

Our agent can then decide by itself about its current ‘intention’, i.e. which goal to pursue next. This might be an auxiliary task or an externally defined target task. Crucially, the agent can detect and learn from reward signals for all other tasks that it is not currently following by making extensive use of replay-based off-policy learning. For example, when picking up or moving an object the agent might incidentally stack it, leading to the observation of rewards for ‘stacking’. Because a sequence of simple tasks can lead to the observation of a rare external reward, the ability to schedule intentions is crucial. It can create a personalised learning curriculum based on all the tangential knowledge it has collected. This turns out to be an effective way to exploit knowledge in such a large domain, and is particularly useful when there are only few external reward signals available. Our agent decides which intention to follow via a scheduling module. The scheduler is improved during training via a meta-learning algorithm that attempts to maximise progress on the main task, which results in significantly improved data-efficiency.

![An animated sequence showing a simulated robotic arm practicing manipulation tasks by interacting with a red and a green block on a tabletop.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62267d63b8f50b29f6390f4c_unnamed.gif)

After exploring a number of internal auxiliary tasks, the agent learns how to stack and tidy the objects away.

Our evaluations show that SAC-X is able to solve all the tasks we set it from scratch—using the same underlying set of auxiliary tasks. Excitingly, SAC-X is also able to successfully learn a pick-up and a placing task from scratch directly on a real robot arm in our lab. In the past this has been particularly challenging because learning on robots in a real-world setup requires data-efficiency, so a popular approach is to pre-train an agent in simulation and then transfer the agent to the real robot arm.

![An animated sequence showing a real robotic arm practicing a pick-up and placing task with a green block on a tabletop.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62267da9ac18bf6f60653b58_unnamed-3.gif)

On the real robot arm, SAC-X learns how to lift and move the green cube from scratch, never having seen the task before.

We consider SAC-X as an important step towards learning control tasks from scratch, when only the overall goal is specified. SAC-X allows you to define auxiliary tasks arbitrarily: they can be based on general insights (like deliberately activating sensors as suggested here), but could ultimately incorporate any task a researcher thinks is important. In that respect, SAC-X is a general RL method that is broadly applicable in general sparse reinforcement learning settings beyond control and robotics.

**Notes**

Read the paper [here](https://arxiv.org/abs/1802.10567).

This work was completed by Martin Riedmiller, Roland Hafner, Thomas Lampe, Michael Neunert, Jonas Degrave, Tom Van de Wiele, Volodymyr Mnih, Nicolas Heess and Tobias Springenberg.
