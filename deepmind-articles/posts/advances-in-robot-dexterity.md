---
title: "Our latest advances in robot dexterity"
source: https://deepmind.google/blog/advances-in-robot-dexterity/
site: deepmind
date: 2024-09-12
authors: Robotics team
crawled: 2026-09-13
---

Two new AI systems, ALOHA Unleashed and DemoStart, help robots learn to perform complex tasks that require dexterous movement

People perform many tasks on a daily basis, like tying shoelaces or tightening a screw. But for robots, learning these highly-dexterous tasks is incredibly difficult to get right. To make robots more useful in people’s lives, they need to get better at making contact with physical objects in dynamic environments.

Today, we introduce two new papers featuring our latest artificial intelligence (AI) advances in robot dexterity research: [ALOHA Unleashed](https://aloha-unleashed.github.io/assets/aloha_unleashed.pdf) which helps robots learn to perform complex and novel two-armed manipulation tasks; and [DemoStart](https://arxiv.org/abs/2409.06613) which uses simulations to improve real-world performance on a multi-fingered robotic hand.

By helping robots learn from human demonstrations and translate images to action, these systems are paving the way for robots that can perform a wide variety of helpful tasks.

## Improving imitation learning with two robotic arms

Until now, most advanced AI robots have only been able to pick up and place objects using a single arm. In [our new paper](https://aloha-unleashed.github.io/assets/aloha_unleashed.pdf), we present ALOHA Unleashed, which achieves a high level of dexterity in bi-arm manipulation. With this new method, our robot learned to tie a shoelace, hang a shirt, repair another robot, insert a gear and even clean a kitchen.

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

Example of a bi-arm robot straightening shoe laces and tying them into a bow.

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

Example of a bi-arm robot laying out a polo shirt on a table, putting it on a clothes hanger and then hanging it on a rack.

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

Example of a bi-arm robot repairing another robot.

The ALOHA Unleashed method builds on our [ALOHA 2](https://aloha-2.github.io/) platform that was based on the original [ALOHA](https://tonyzhaozh.github.io/aloha/) (a low-cost open-source hardware system for bimanual teleoperation) from [Stanford University](https://irislab.stanford.edu/).

ALOHA 2 is significantly more dexterous than prior systems because it has two hands that can be easily teleoperated for training and data collection purposes, and it allows robots to learn how to perform new tasks with fewer demonstrations.

We’ve also improved upon the robotic hardware’s ergonomics and enhanced the learning process in our latest system. First, we collected demonstration data by remotely operating the robot’s behavior, performing difficult tasks like tying shoelaces and hanging t-shirts. Next, we applied a diffusion method, predicting robot actions from random noise, similar to how our [Imagen](https://deepmind.google/technologies/imagen-3/) model generates images. This helps the robot learn from the data, so it can perform the same tasks on its own.

## Learning robotic behaviors from few simulated demonstrations

Controlling a dexterous, robotic hand is a complex task, which becomes even more complex with every additional finger, joint and sensor. In another [new paper](https://arxiv.org/abs/2409.06613), we present DemoStart, which uses a reinforcement learning algorithm to help robots acquire dexterous behaviors in simulation. These learned behaviors are especially useful for complex embodiments, like multi-fingered hands.

DemoStart first learns from easy states, and over time, starts learning from more difficult states until it masters a task to the best of its ability. It requires 100x fewer simulated demonstrations to learn how to solve a task in simulation than what’s usually needed when learning from real world examples for the same purpose.

The robot achieved a success rate of over 98% on a number of different tasks in simulation, including reorienting cubes with a certain color showing, tightening a nut and bolt, and tidying up tools. In the real-world setup, it achieved a 97% success rate on cube reorientation and lifting, and 64% at a plug-socket insertion task that required high-finger coordination and precision.

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

Example of a robotic arm learning to successfully insert a yellow connector in simulation (left) and in a real-world setup (right).

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

Example of a robotic arm learning to tighten a bolt on a screw in simulation.

We developed DemoStart with [MuJoCo](https://mujoco.org/), our open-source physics simulator. After mastering a range of tasks in simulation and using standard techniques to reduce the sim-to-real gap, like domain randomization, our approach was able to transfer nearly zero-shot to the physical world.

Robotic learning in simulation can reduce the cost and time needed to run actual, physical experiments. But it’s difficult to design these simulations, and moreover, they don’t always translate successfully back into real-world performance. By combining reinforcement learning with learning from a few demonstrations, DemoStart’s progressive learning automatically generates a curriculum that bridges the sim-to-real gap, making it easier to transfer knowledge from a simulation into a physical robot, and reducing the cost and time needed for running physical experiments.

To enable more advanced robot learning through intensive experimentation, we tested this new approach on a three-fingered robotic hand, called [DEX-EE](https://www.shadowrobot.com/dex-ee/), which was developed in collaboration with [Shadow Robot](https://www.shadowrobot.com/).

![A close-up shot of the DEX-EE three-fingered robotic hand with articulated, multi-jointed black fingers, shown against a plain white background.](https://lh3.googleusercontent.com/uuY20ESjCaU6ldnvE53s9PX5q4GovZlFSwsO900w6SOBiEQBQPX4hS9NFpO4AQkGzh0HboLmPKu6XpeF63G2z4xj34fGreyQwaFRtTWXtTFuySi2=w1440)

Image of the DEX-EE dexterous robotic hand, developed by Shadow Robot, in collaboration with the Google DeepMind robotics team (Credit: Shadow Robot).

## The future of robot dexterity

Robotics is a unique area of AI research that shows how well our approaches work in the real world. For example, a large language model could tell you how to tighten a bolt or tie your shoes, but even if it was embodied in a robot, it wouldn’t be able to perform those tasks itself.

One day, AI robots will help people with all kinds of tasks at home, in the workplace and more. Dexterity research, including the efficient and general learning approaches we’ve described today, will help make that future possible.

We still have a long way to go before robots can grasp and handle objects with the ease and precision of people, but we’re making significant progress, and each groundbreaking innovation is another step in the right direction.

[Read our ALOHA Unleashed paper](https://aloha-unleashed.github.io/assets/aloha_unleashed.pdf)[Read our DemoStart paper](https://arxiv.org/abs/2409.06613)[Learn more about ALOHA 2](https://aloha-2.github.io/)

**Acknowledgements**

The authors of DemoStart: Maria Bauza, Jose Enrique Chen, Valentin Dalibard, Nimrod Gileadi, Roland Hafner, Antoine Laurens, Murilo F. Martins, Joss Moore, Rugile Pevceviciute, Dushyant Rao, Martina Zambelli, Martin Riedmiller, Jon Scholz, Konstantinos Bousmalis, Francesco Nori, Nicolas Heess.

The authors of Aloha Unleashed: Tony Z. Zhao, Jonathan Tompson, Danny Driess, Pete Florence, Kamyar Ghasemipour, Chelsea Finn, Ayzaan Wahid.
