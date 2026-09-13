---
title: "Producing flexible behaviours in simulated environments"
source: https://deepmind.google/blog/producing-flexible-behaviours-in-simulated-environments/
site: deepmind
date: 2017-07-10
authors: Nicolas Heess, Josh Merel, Ziyu Wang
crawled: 2026-09-13
---

The agility and flexibility of a monkey swinging through the trees or a football player dodging opponents and scoring a goal can be breathtaking. Mastering this kind of sophisticated motor control is a hallmark of physical intelligence, and is a crucial part of AI research.

True motor intelligence requires learning how to control and coordinate a flexible body to solve tasks in a range of complex environments. Existing attempts to control physically simulated humanoid bodies come from diverse fields, including computer animation and biomechanics. A trend has been to use hand-crafted objectives, sometimes with motion capture data, to produce specific behaviors. However, this may require considerable engineering effort, and can result in restricted behaviours or behaviours that may be difficult to repurpose for new tasks.

In three new papers, we seek ways to produce flexible and natural behaviours that can be reused and adapted to solve tasks.

## Emergence of locomotion behaviours in rich environments

For some AI problems, such as playing Atari or Go, the goal is easy to define - it’s winning. But how do you describe the process for performing a backflip? Or even just a jump? The difficulty of accurately describing a complex behaviour is a common problem when teaching motor skills to an artificial system. In this work we explore how sophisticated behaviors can emerge from scratch from the body interacting with the environment using only simple high-level objectives, such as moving forward without falling. Specifically, we trained agents with a variety of simulated bodies to make progress across diverse terrains, which require jumping, turning and crouching. The results show our agents develop these complex skills without receiving specific instructions, an approach that can be applied to train our systems for multiple, distinct simulated bodies. The GIFs below show how this technique can lead to high quality movements and perseverance. They can be viewed in full [here](https://youtu.be/hx_bgoTF7bs).

![An orange, simplified humanoid figure leaps high in the air to jump over a wide gap in a simulated 3D environment.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/622655eb68abbee38e669eb2_A20simulated2027planar2720walker20makes20repeated.gif)

A simulated 'planar' walker makes repeated attempts to climb over a wall.

![An orange, four-legged simulated agent navigates across narrow, elevated platforms in a 3D environment.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/622656200aa988d46d909b6f_A20simulated2027ant2720walker20learns20the20preci.gif)

A simulated 'ant' walker learns the precise movements required to jump between planks.

![An orange, simplified humanoid figure leaps high in the air to jump over a wide gap in a simulated 3D environment.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62265611c0a057d54f0c6e31_unnamed-3.gif)

A simulated 'humanoid' walker learns to move forward in an unfamiliar terrain

## Learning human behaviours from motion capture by adversarial imitation

The emergent behaviour described above can be very robust, but because the movements must emerge from scratch, they often do not look human-like. In our second paper, we demonstrate how to train a policy network that imitates motion capture data of human behaviours to pre-learn certain skills, such as walking, getting up from the ground, running, and turning. Having produced behaviour that looks human-like, we can tune and repurpose those behaviours to solve other tasks, like climbing stairs and navigating walled corridors.

![A simulated humanoid figure walks with a natural, human-like gait on a blue-and-white checkered floor.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62265660284fd1853f765891_A20humanoid20walker20produces20human-like20walkin.gif)

A humanoid walker produces human-like walking behaviour.

![A simulated humanoid figure uses its arms to push itself off the ground and stand up on a blue-and-white checkered floor.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6226568168abbe472b66a4d5_A20simulated20humanoid20walker20falls20over20and2.gif)

A simulated humanoid walker falls over and gets back up.

## Robust imitation of diverse behaviours

The third paper proposes a neural network architecture, building on state-of-the-art generative models, that is capable of learning the relationships between different behaviours and imitating specific actions that it is shown. After training, our system can encode a single observed action and create a new novel movement based on that demonstration. It can also switch between different kinds of behaviours despite never having seen transitions between them, for example switching between walking styles.

![Three side-by-side simulated humanoid figures demonstrate different walking styles and postures on a checkered floor.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/622656f6284fd1d557765db0_Behaviours201.gif)

In the left and middle panels we show two demonstrated behaviours. In the right panel, our agent produces an unseen transition between those behaviours.

![Two side-by-side simulated simplified humanoid figures demonstrating different walking styles on a checkered floor.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/622657235460dd5f37e33ee2_Planar20Walking.gif)

In the left panel, the planar walker demonstrates a particular walking style. In the right panel, our agent imitates this walking style using a single policy network.

Achieving flexible and adaptive control of simulated bodies is a key element of AI research. Our work aims to develop flexible systems which learn and adapt skills to solve motor control tasks while reducing the manual engineering required to achieve this goal. Future work could extend these approaches to enable coordination of a greater range of behaviours in more complex situations.

**Notes**

[Emergence of locomotion behaviours in rich environments](https://arxiv.org/abs/1707.02286)

[Learning human behaviours from motion capture by adversarial imitation](https://arxiv.org/abs/1707.02201)

[Robust imitation of diverse behaviours](https://arxiv.org/abs/1707.02747)
