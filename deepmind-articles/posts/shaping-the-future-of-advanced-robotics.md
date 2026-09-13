---
title: "Shaping the future of advanced robotics"
source: https://deepmind.google/blog/shaping-the-future-of-advanced-robotics/
site: deepmind
date: 2024-01-04
authors: Robotics team
crawled: 2026-09-13
---

Introducing AutoRT, SARA-RT and RT-Trajectory to improve real-world robot data collection, speed, and generalization

Picture a future in which a simple request to your personal helper robot - “tidy the house” or “cook us a delicious, healthy meal” - is all it takes to get those jobs done. These tasks, straightforward for humans, require a high-level understanding of the world for robots.

Today we’re announcing a suite of advances in robotics research that bring us a step closer to this future. AutoRT, SARA-RT, and RT-Trajectory build on our historic [Robotics Transformers](https://deepmind.google/discover/blog/rt-2-new-model-translates-vision-and-language-into-action/) work to help robots make decisions faster, and better understand and navigate their environments.

## AutoRT: Harnessing large models to better train robots

We introduce [AutoRT](https://auto-rt.github.io/), a system that harnesses the potential of large foundation models which is critical to creating robots that can understand practical human goals. By collecting more experiential training data – and more diverse data – AutoRT can help scale robotic learning to better train robots for the real world.

AutoRT combines large foundation models such as a Large Language Model (LLM) or Visual Language Model (VLM), and a robot control model (RT-1 or RT-2) to create a system that can deploy robots to gather training data in novel environments. AutoRT can simultaneously direct multiple robots, each equipped with a video camera and an end effector, to carry out diverse tasks in a range of settings. For each robot, the system uses a VLM to understand its environment and the objects within sight. Next, an LLM suggests a list of creative tasks that the robot could carry out, such as “Place the snack onto the countertop” and plays the role of decision-maker to select an appropriate task for the robot to carry out.

In extensive real-world evaluations over seven months, the system safely orchestrated as many as 20 robots simultaneously, and up to 52 unique robots in total, in a variety of office buildings, gathering a diverse dataset comprising 77,000 robotic trials across 6,650 unique tasks.

![A flowchart diagram illustrating the five-step process of AutoRT data collection: 1. Exploration (mapping the environment), 2. Task Generation (using a VLM to describe objects and an LLM to generate tasks like wiping the counter), 3. Filter Tasks (using an LLM to filter tasks based on feasibility and safety), 4. Data Collection (the robot executing the chosen task), and 5. Data Diversity Scoring (plotting the data on a scatter plot before repeating the process).](https://lh3.googleusercontent.com/WooC0XNhBLULqzULW_Bv7CS0DtTqdEmOV7u_GtY8OcIxRq5m19-m8_Y_YmtUxf5lfX5xg0hahuGexU8_tnXL78MGPfKMF4YLTEJ1kwg_xlDUCK-BxA=w1440)

(1) An autonomous wheeled robot finds a location with multiple objects. (2) A VLM describes the scene and objects to an LLM. (3) An LLM suggests diverse manipulation tasks for the robot and decides which tasks the robot could do unassisted, which would require remote control by a human, and which are impossible, before making a choice. (4) The chosen task is attempted, the experiential data collected, and the data scored for its diversity/novelty. Repeat.

## Layered safety protocols are critical

Before robots can be integrated into our everyday lives, they need to be developed responsibly with robust research demonstrating their real-world safety.

While AutoRT is a data-gathering system, it is also an early demonstration of autonomous robots for real-world use. It features safety guardrails, one of which is providing its LLM-based decision-maker with a Robot Constitution - a set of safety-focused prompts to abide by when selecting tasks for the robots. These rules are in part inspired by Isaac Asimov’s Three Laws of Robotics – first and foremost that a robot “may not injure a human being”. Further safety rules require that no robot attempts tasks involving humans, animals, sharp objects or electrical appliances.

But even if large models are prompted correctly with self-critiquing, this alone cannot guarantee safety. So the AutoRT system comprises layers of practical safety measures from classical robotics. For example, the collaborative robots are programmed to stop automatically if the force on its joints exceed a given threshold, and all active robots were kept in line-of-sight of a human supervisor with a physical deactivation switch.

## SARA-RT: Making Robotics Transformers leaner and faster

Our new system, [Self-Adaptive Robust Attention for Robotics Transformers](https://sites.google.com/corp/view/rtsara/) (SARA-RT), converts Robotics Transformer (RT) models into more efficient versions.

The RT neural network architecture developed by our team is used in the latest robotic control systems, including our state-of-the-art [RT-2 model](https://deepmind.google/discover/blog/rt-2-new-model-translates-vision-and-language-into-action/). The best SARA-RT-2 models were 10.6% more accurate and 14% faster than RT-2 models after being provided with a short history of images. We believe this is the first scalable attention mechanism to provide computational improvements with no quality loss.

While transformers are powerful, they can be limited by computational demands that slow their decision-making. Transformers critically rely on attention modules of quadratic complexity. That means if an RT model’s input doubles – by giving a robot additional or higher-resolution sensors, for example – the computational resources required to process that input rise by a factor of four, which can slow decision-making.

SARA-RT makes models more efficient using a novel method of model fine-tuning that we call “up-training”. Up-training converts the quadratic complexity to mere linear complexity, sharply reducing the computational requirements. This conversion not only increases the original model’s speed, but also preserves its quality.

We designed our system for usability and hope many researchers and practitioners will apply it, in robotics and beyond. Because SARA provides a universal recipe for speeding up Transformers, without need for computationally expensive pre-training, this approach has the potential to massively scale up use of Transformers technology. SARA-RT does not require any additional code as various open-sourced linear variants can be used.

When we applied SARA-RT to a state-of-the-art RT-2 model with billions of parameters, it resulted in faster decision-making and better performance on a wide range of robotic tasks.

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

SARA-RT-2 model for manipulation tasks. Robot’s actions are conditioned on images and text commands.

And with its robust theoretical grounding, SARA-RT can be applied to a wide variety of Transformer models. For example, applying SARA-RT to [Point Cloud Transformers](https://arxiv.org/abs/2012.09688) - used to process spatial data from robot depth cameras - more than doubled their speed.

## RT-Trajectory: Helping robots generalize

It may be intuitive for humans to understand how to wipe a table, but there are many possible ways a robot could translate an instruction into actual physical motions.

We developed a model called [RT-Trajectory](https://rt-trajectory.github.io/), which automatically adds visual outlines that describe robot motions in training videos. RT-Trajectory takes each video in a training dataset and overlays it with a 2D trajectory sketch of the robot arm’s gripper as it performs the task. These trajectories, in the form of RGB images, provide low-level, practical visual hints to the model as it learns its robot-control policies.

When tested on 41 tasks unseen in the training data, an arm controlled by RT-Trajectory more than doubled the performance of existing state-of-the-art RT models: it achieved a task success rate of 63%, compared with 29% for RT-2.

Traditionally, training a robotic arm relies on mapping abstract natural language (“wipe the table”) to specific movements (close gripper, move left, move right), making it hard for models to generalize to novel tasks. In contrast, an RT-Trajectory model enables RT models to understand "how to do" tasks by interpreting specific robot motions like those contained in videos or sketches.

The system is versatile: RT-Trajectory can also create trajectories by watching human demonstrations of desired tasks, and even accept hand-drawn sketches. And it can be readily adapted to different robot platforms.

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

Left: A robot, controlled by an RT model trained with a natural-language-only dataset, is stymied when given the novel task: “clean the table”. A robot controlled by RT-Trajectory, trained on the same dataset augmented by 2D trajectories, successfully plans and executes a wiping trajectory

Right: A trained RT-Trajectory model given a novel task (“clean the table”) can create 2D trajectories in a variety of ways, assisted by humans or on its own using a vision-language model.

RT-Trajectory makes use of the rich robotic-motion information that is present in all robot datasets, but currently under-utilized. RT-Trajectory not only represents another step along the road to building robots able to move with efficient accuracy in novel situations, but also unlocking knowledge from existing datasets.

## Building the foundations for next-generation robots

By building on the foundation of our state-of-the-art RT-1 and RT-2 models, each of these pieces help create ever more capable and helpful robots. We envision a future in which these models and systems can be integrated to create robots – with the motion generalization of RT-Trajectory, the efficiency of SARA-RT, and the large-scale data collection from models like AutoRT. We will continue to tackle challenges in robotics today and to adapt to the new capabilities and technologies of more advanced robotics.

**Learn more**

[AutoRT paper](https://auto-rt.github.io/static/pdf/AutoRT.pdf)[AutoRT GitHub](https://auto-rt.github.io/)[SARA-RT paper](https://arxiv.org/abs/2312.01990)[SARA-RT website](https://sites.google.com/corp/view/rtsara/)[RT-Trajectory paper](https://arxiv.org/abs/2311.01977)[RT-Trajectory GitHub](https://rt-trajectory.github.io/)[Access the Open X-Embodiment dataset](https://github.com/google-deepmind/open_x_embodiment)

**Additional notes**

We would like to thank Krzysztof Choromanski, Keerthana Gopalakrishnan, Alex Irpan, and Ted Xiao for their contributions to this blog.

We would also like to thank all of the contributing authors to the three papers.

AutoRT: Michael Ahn, Debidatta Dwibedi, Chelsea Finn, Montse Gonzalez Arenas, Keerthana Gopalakrishnan, Karol Hausman, Brian Ichter, Alex Irpan, Nikhil Joshi, Ryan Julian, Sean Kirmani, Isabel Leal, Edward Lee, Sergey Levine, Yao Lu, Sharath Maddineni, Kanishka Rao, Dorsa Sadigh, Pannag Sanketi, Pierre Sermanet, Quan Vuong, Stefan Welker, Fei Xia, Ted Xiao, Peng Xu, Steve Xu, Zhuo Xu

SARA-RT: Isabel Leal, Krzysztof Choromanski, Deepali Jain, Avinava Dubey, Jake Varley, Michael Ryoo, Yao Lu, Frederick Liu, Vikas Sindhwani, Quan Vuong, Tamas Sarlos, Ken Oslund, Karol Hausman, Kanishka Rao

RT-Trajectory: Jiayuan Gu, Sean Kirmani, Paul Wohlhart, Yao Lu, Montserrat Gonzalez Arenas, Kanishka Rao, Wenhao Yu, Chuyuan Fu, Keerthana Gopalakrishnan, Zhuo Xu, Priya Sundaresan, Peng Xu, Hao Su, Karol Hausman, Chelsea Finn, Quan Vuong, Ted Xiao

Finally, we would like to acknowledge Vincent Vanhoucke who supported the research conducted in these papers.
