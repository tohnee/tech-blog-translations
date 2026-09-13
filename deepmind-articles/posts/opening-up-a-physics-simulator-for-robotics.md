---
title: "Opening up a physics simulator for robotics"
source: https://deepmind.google/blog/opening-up-a-physics-simulator-for-robotics/
site: deepmind
date: 2021-10-18
authors: Yuval Tassa, Saran Tunyasuvunakool, Nimrod Gileadi, Tom Erez, Andrea Huber
crawled: 2026-09-13
---

Advancing research everywhere with the acquisition of MuJoCo

When you walk, your feet make contact with the ground. When you write, your fingers make contact with the pen. Physical contacts are what makes interaction with the world possible. Yet, for such a common occurrence, contact is a surprisingly complex phenomenon. Taking place at microscopic scales at the interface of two bodies, contacts can be soft or stiff, bouncy or spongy, slippery or sticky. It’s no wonder our fingertips have [four different types](https://courses.lumenlearning.com/boundless-biology/chapter/somatosensation/) of touch-sensors. This subtle complexity makes simulating physical contact — a vital component of robotics research — a tricky task.

The rich-yet-efficient contact model of the [MuJoCo physics simulator](https://mujoco.org/) has made it a leading choice by robotics researchers and today, we're proud to announce that, as part of [DeepMind's mission](https://deepmind.com/about) of advancing science, we've acquired MuJoCo and are making it [freely available](https://mujoco.org/download) for everyone, to support research everywhere. Already widely used within the robotics community, including as the physics simulator of choice for DeepMind’s robotics team, MuJoCo features a rich contact model, powerful scene description language, and a well-designed API. Together with the community, we will continue to improve MuJoCo as open-source software under a permissive licence. As we work to prepare the codebase, we are making MuJoCo [freely available](https://mujoco.org/download) as a precompiled library.

A balanced model of contact. MuJoCo, which stands for **Mu**lti-**Jo**int Dynamics with **Co**ntact, hits a sweet spot with its contact model, which accurately and efficiently captures the salient features of contacting objects. Like other rigid-body simulators, it avoids the fine details of deformations at the contact site, and often runs much faster than real time. Unlike other simulators, MuJoCo resolves contact forces using the convex [Gauss Principle](https://en.wikipedia.org/wiki/Gauss%27s_principle_of_least_constraint). Convexity ensures unique solutions and well-defined inverse dynamics. The model is also flexible, providing multiple parameters which can be tuned to approximate a wide range of contact phenomena.

**Real:**

Complex contact-related phenomena like the flipping of a Tippe top emerge naturally in MuJoCo due to its accurate description of contacts.

**MuJoCo:**

Complex contact-related phenomena like the flipping of a Tippe top emerge naturally in MuJoCo due to its accurate description of contacts.

A [recent PNAS perspective](https://www.pnas.org/content/118/1/e1907856118) exploring the state of simulation in robotics identifies open source tools as critical for advancing research. The authors’ recommendations are to develop and validate open source simulation platforms as well as to establish open and community-curated libraries of validated models. In line with these aims, we’re committed to developing and maintaining MuJoCo as a free, open-source, community-driven project with best-in-class capabilities. We’re currently hard at work preparing MuJoCo for full open sourcing, and we encourage you to download the software from the [new homepage](http://mujoco.org/) and visit the [GitHub repository](https://github.com/deepmind/mujoco) if you'd like to contribute. [Email us](mailto:mujoco@deepmind.com) if you have any questions or suggestions, and if you're also excited to push the boundaries of realistic physics simulation, [we're hiring](https://deepmind.com/careers/jobs/3242004). We can’t promise we’ll be able to address everything right away, but we’re eager to work together to make MuJoCo the physics simulator we’ve all been waiting for.

**MuJoCo in DeepMind.** Our robotics team has been using MuJoCo as a simulation platform for various projects, mostly via our [dm\_control](https://github.com/deepmind/dm_control) Python stack. In the carousel below, we highlight a few examples to showcase what can be simulated in MuJoCo. Of course, these clips represent only a tiny fraction of the vast possibilities for how researchers might use the simulator. For higher quality versions of these clips, please click [here](https://www.youtube.com/playlist?list=PLstWnsTbb45eqXgVY2RhsFV6VeNsMFLS9).

**Real physics, no shortcuts.** Because many simulators were initially designed for purposes like gaming and cinema, they sometimes take shortcuts that prioritise stability over accuracy. For instance, they may ignore gyroscopic forces or directly modify velocities. This can be particularly harmful in the context of optimisation: as [first observed](https://doi.org/10.1145/192161.192167) by artist and researcher Karl Sims, an optimising agent can quickly discover and exploit these deviations from reality. In contrast, MuJoCo is a second-order continuous-time simulator, implementing the full Equations of Motion. Familiar yet non-trivial physical phenomena like [Newton’s Cradle](https://en.wikipedia.org/wiki/Newton%27s_cradle), as well as unintuitive ones like the [Dzhanibekov effect](https://en.wikipedia.org/wiki/Tennis_racket_theorem), emerge naturally. Ultimately, MuJoCo closely adheres to the equations that govern our world.

**Real:**

MuJoCo can accurately capture the impulse propagation in a Newton’s Cradle.

**MuJoCo:**

MuJoCo can accurately capture the impulse propagation in a Newton’s Cradle.

**Real (source: NASA):**

Gyroscopic forces due to angular momentum conservation cause this interesting effect, seen here in zero-gravity.

**MuJoCo:**

Gyroscopic forces due to angular momentum conservation cause this interesting effect, seen here in zero-gravity.

**Portable code, clean API.** MuJoCo’s core engine is written in pure C, which makes it easily portable to various architectures. The library produces deterministic results, with the scene description and simulation state fully encapsulated within two data structures. These constitute all the information needed to recreate a simulation, including results from intermediate stages, providing easy access to the internals. The library also provides fast and convenient computations of commonly used quantities, like kinematic Jacobians and inertia matrices.

**Powerful scene description.** The MJCF scene-description format uses cascading defaults — avoiding multiple repeated values ​​— and contains elements for real-world robotic components like equality constraints, motion-capture markers, tendons, actuators, and sensors. Our long-term roadmap includes standardising MJCF as an open format, to extend its usefulness beyond the MuJoCo ecosystem.

**Biomechanical simulation.** MuJoCo includes two powerful features that support musculoskeletal models of humans and animals. Spatial tendon routing, including wrapping around bones, means that applied forces can be distributed correctly to the joints, describing complicated effects like the variable [moment-arm](https://www.oxfordreference.com/view/10.1093/acref/9780198568506.001.0001/acref-9780198568506-e-4405) in the [knee enabled by the tibia](https://www.youtube.com/watch?v=wyiJw034ssA). MuJoCo’s muscle model captures the complexity of biological muscles, including activation states and force-length-velocity curves.

A simulated human leg swings around, driven by forces applied at the tendons. Note how the tibia slides along the femur. Based on Lai, Arnold & Wakeling (2017).

A [recent PNAS perspective](https://www.pnas.org/content/118/1/e1907856118) exploring the state of simulation in robotics identifies open source tools as critical for advancing research. The authors’ recommendations are to develop and validate open source simulation platforms as well as to establish open and community-curated libraries of validated models. In line with these aims, we’re committed to developing and maintaining MuJoCo as a free, open-source, community-driven project with best-in-class capabilities. We’re currently hard at work preparing MuJoCo for full open sourcing, and we encourage you to download the software from the [new homepage](http://mujoco.org/) and visit the [GitHub repository](https://github.com/deepmind/mujoco) if you'd like to contribute. Email us if you have any questions or suggestions, and if you're also excited to push the boundaries of realistic physics simulation, [we're hiring](https://deepmind.com/careers/jobs/3242004). We can’t promise we’ll be able to address everything right away, but we’re eager to work together to make MuJoCo the physics simulator we’ve all been waiting for.

**MuJoCo in DeepMind.** Our robotics team has been using MuJoCo as a simulation platform for various projects, mostly via our [dm\_control](https://github.com/deepmind/dm_control) Python stack. In the carousel below, we highlight a few examples to showcase what can be simulated in MuJoCo. Of course, these clips represent only a tiny fraction of the vast possibilities for how researchers might use the simulator. For higher quality versions of these clips, please click [here](https://www.youtube.com/playlist?list=PLstWnsTbb45eqXgVY2RhsFV6VeNsMFLS9).

![Simulated humanoid figures play football with two players on each team. There is a red team and a blue team. The red team successfully defends the blue team's attack and goes on to score a goal.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/mujoco_01.gif)

![A simulated dog-like figure runs across a flat surface. As it runs we get to glimpse an X-ray view of its animated skeleton, which is very detailed.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/mujoco_03.gif)

![A simulated humanoid figure holds a handstand. It is visibly struggling to hold the position, but it adjusts its posture so it does not fall.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/mujoco_04.gif)

![A simulated humanoid figure catches a ball thrown to it at various angles and speeds.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/mujoco_05.gif)

Like others in the community, our robotics team has used MuJoCo as a simulation platform for various projects. In the above montage, we highlight a few examples to showcase what this tool looks like in action. Of course, these video clips represent only a tiny fraction of the vast possibilities for how roboticists can use the simulator to advance their research.
