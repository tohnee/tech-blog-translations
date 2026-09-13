---
title: "RoboCat: A self-improving robotic agent"
source: https://deepmind.google/blog/robocat-a-self-improving-robotic-agent/
site: deepmind
date: 2023-06-20
authors: RoboCat team
crawled: 2026-09-13
---

New foundation agent learns to operate different robotic arms, solves tasks from as few as 100 demonstrations, and improves from self-generated data.

Robots are quickly becoming part of our everyday lives, but they’re often only programmed to perform specific tasks well. While harnessing recent advances in AI could lead to robots that could help in many more ways, progress in building general-purpose robots is slower in part because of the time needed to collect real-world training data.

[Our latest paper](https://arxiv.org/abs/2306.11706) introduces a self-improving AI agent for robotics, RoboCat, that learns to perform a variety of tasks across different arms, and then self-generates new training data to improve its technique.

Previous research has explored how to develop [robots that can learn to multi-task at scale](https://ai.googleblog.com/2022/12/rt-1-robotics-transformer-for-real.html) and [combine the understanding of language models with the real-world capabilities](https://sites.research.google/palm-saycan) of a helper robot. RoboCat is the first agent to solve and adapt to multiple tasks and do so across different, real robots.

RoboCat learns much faster than other state-of-the-art models. It can pick up a new task with as few as 100 demonstrations because it draws from a large and diverse dataset. This capability will help accelerate robotics research, as it reduces the need for human-supervised training, and is an important step towards creating a general-purpose robot.

## How RoboCat improves itself

RoboCat is based on our multimodal model [Gato](https://deepmind.google/blog/a-generalist-agent/) (Spanish for “cat”), which can process language, images, and actions in both simulated and physical environments. We combined Gato’s architecture with a large training dataset of sequences of images and actions of various robot arms solving hundreds of different tasks.

After this first round of training, we launched RoboCat into a “self-improvement” training cycle with a set of previously unseen tasks. The learning of each new task followed five steps:

1. Collect 100-1000 demonstrations of a new task or robot, using a robotic arm controlled by a human.
2. Fine-tune RoboCat on this new task/arm, creating a specialised spin-off agent.
3. The spin-off agent practises on this new task/arm an average of 10,000 times, generating more training data.
4. Incorporate the demonstration data and self-generated data into RoboCat’s existing training dataset.
5. Train a new version of RoboCat on the new training dataset.

![A visual representation of the list of steps RoboCat takes to improve itself.](https://lh3.googleusercontent.com/fkvWSJIvd2LNhRFhQDeGcKTNNmsI__N2nU05Y876K0G2rGsYbm3-Mf9oiSy1rWROhygrPgMTGQfjJh1zo1N10-48B9YmRgu515zTNh2QSZmhlTGEE3I=w1440)

RoboCat’s training cycle, boosted by its ability to autonomously generate additional training data.

The combination of all this training means the latest RoboCat is based on a dataset of millions of trajectories, from both real and simulated robotic arms, including self-generated data. We used four different types of robots and many robotic arms to collect vision-based data representing the tasks RoboCat would be trained to perform.

![Three videos of RoboCat in real-world, simulated, and self-generated forms. The first video shows a real robotic arm picking up gears, the second is a simulated arm stacking blocks, and the third shows RoboCat using a robotic arm to pick up a cucumber.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6491af73bf4b23fea70312cf_6490352e82d96885abfec100_z9I3J43_HYsCvaW04QpU3Sfm.gif)

RoboCat learns from a diverse range of training data types and tasks: Videos of a real robotic arm picking up gears, a simulated arm stacking blocks and RoboCat using a robotic arm to pick up a cucumber.

## Learning to operate new robotic arms and solve more complex tasks

With RoboCat’s diverse training, it learned to operate different robotic arms within a few hours. While it had been trained on arms with two-pronged grippers, it was able to adapt to a more complex arm with a three-fingered gripper and twice as many controllable inputs.

![The image on the left shows a new robotic arm RoboCat learned to control. Next to it is a video of RoboCat using the arm to pick up gears.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6491af726c741ebb048f88ba_6491a345181cdaa42e86ec2f_Copy2520of2520Fig25204.gif)

**Left:** A new robotic arm RoboCat learned to control
**Right:** Video of RoboCat using the arm to pick up gears

After observing 1000 human-controlled demonstrations, collected in just hours, RoboCat could direct this new arm dexterously enough to pick up gears successfully 86% of the time. With the same level of demonstrations, it could adapt to solve tasks that combined precision and understanding, such as removing the correct fruit from a bowl and solving a shape-matching puzzle, which are necessary for more complex control.

![Two videos of RoboCat completing tasks. On the left, a robotic arm is doing a children's puzzle, placing wooden blocks into the correctly shaped hole. On the right, the robotic arm is picking a lemon out of a fruit bowl.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6491af73441ad51e4b9fc18c_6491a374441ad51e4b945df3_Copy2520of2520Fig2520525.gif)

Examples of tasks RoboCat can adapt to solving after 500-1000 demonstrations.

## The self-improving generalist

RoboCat has a virtuous cycle of training: the more new tasks it learns, the better it gets at learning additional new tasks. The initial version of RoboCat was successful just 36% of the time on previously unseen tasks, after learning from 500 demonstrations per task. But the latest RoboCat, which had trained on a greater diversity of tasks, more than doubled this success rate on the same tasks.

![A bar chart comparing RoboCat's success at new tasks, after 500 demos. The initial RoboCat has a 36% average success rate. The final RoboCat has a 74% average success rate.](https://lh3.googleusercontent.com/Okfaiq6fpxBb8wC7k_jyelj_3SID_e_rWrLmrrUsT8rsbSjyU78xKi5vRnfQcApxS7hXmK0uu5IaFi6qVkI98DouyKWpxMUF6v1DApRGDUD-DfYSCw=w1440)

The big difference in performance between the initial RoboCat (one round of training) compared with the final version (extensive and diverse training, including self-improvement) after both versions were fine-tuned on 500 demonstrations of previously unseen tasks.

These improvements were due to RoboCat's growing breadth of experience, similar to how people develop a more diverse range of skills as they deepen their learning in a given domain. RoboCat’s ability to independently learn skills and rapidly self-improve, especially when applied to different robotic devices, will help pave the way toward a new generation of more helpful, general-purpose robotic agents.

[Read our paper on arXiv](https://arxiv.org/abs/2306.11706)
