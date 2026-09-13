---
title: "From motor control to embodied intelligence"
source: https://deepmind.google/blog/from-motor-control-to-embodied-intelligence/
site: deepmind
date: 2022-08-31
authors: Siqi Liu, Leonard Hasenclever, Steven Bohez, Guy Lever, Zhe Wang, Ali Eslami, Nicolas Heess
crawled: 2026-09-13
---

Using human and animal motions to teach robots to dribble a ball, and simulated humanoid characters to carry boxes and play football

![](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/630f66e86725db418b6d33f0_Football20blog201.gif)

Humanoid character learning to traverse an obstacle course through trial-and-error, which can lead to idiosyncratic solutions. Heess, et al. "Emergence of locomotion behaviours in rich environments" (2017).

Five years ago, we took on the challenge of teaching a fully articulated humanoid character to [traverse obstacle courses](https://youtu.be/hx_bgoTF7bs?t=88). This demonstrated what reinforcement learning (RL) can achieve through trial-and-error but also highlighted two challenges in solving embodied intelligence:

1. **Reusing previously learned behaviours:** A significant amount of data was needed for the agent to “get off the ground”. Without any initial knowledge of what force to apply to each of its joints, the agent started with random body twitching and quickly falling to the ground. This problem could be alleviated by reusing previously learned behaviours.
2. **Idiosyncratic behaviours:** When the agent finally learned to navigate obstacle courses, it did so with unnatural ([albeit amusing](https://www.youtube.com/watch?v=EI3gcbDUNiM&t=258s)) movement patterns that would be impractical for applications such as robotics.

Here, we describe a solution to both challenges called neural probabilistic motor primitives (NPMP), involving guided learning with movement patterns derived from humans and animals, and discuss how this approach is used in our [Humanoid Football paper,](https://www.science.org/doi/10.1126/scirobotics.abo0235) published today in Science Robotics.

We also discuss how this same approach enables humanoid full-body manipulation from vision, such as a humanoid carrying an object, and robotic control in the real-world, such as a robot dribbling a ball.

## Distilling data into controllable motor primitives using NPMP

An NPMP is a general-purpose motor control module that translates short-horizon motor intentions to low-level control signals, and it’s [trained offline](https://openreview.net/forum?id=BJl6TjRcY7) or [via RL](https://proceedings.mlr.press/v119/hasenclever20a.html) by imitating motion capture (MoCap) data, recorded with trackers on humans or animals performing motions of interest.

![An orange 3D humanoid character mimics the walking and turning movements of a semi-transparent gray character on a tiled blue surface.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/630f68789b57e07b40fcd865_Football20blog202.gif)

An agent learning to imitate a MoCap trajectory (shown in grey).

**The model has two parts:**

1. An encoder that takes a future trajectory and compresses it into a motor intention.
2. A low-level controller that produces the next action given the current state of the agent and this motor intention.

![Diagram illustrating NPMP Training on the left and its Reuse on the right. During NPMP Training, reference data informs the agent state and future trajectory, which passes through an encoder to generate motor intentions. These intentions, regularized by a prior, guide the low-level controller to perform actions. During Reuse, an RL environment provides task observations to a pink task policy, which directly outputs motor intentions to the reused low-level controller to perform task actions.](https://lh3.googleusercontent.com/BVUVxX__mBb14uR12QhmavzmOnnw1bVtMCKaDU1SAB2ECVN7AXB743XMEPQaeVPlG1ZQ91bQbRoVL0gaDfnW5jvvE9evXNN4ta7citvyT2lXVnrzPw=w1440)

Our NPMP model first distils reference data into a low-level controller (left). This low-level controller can then be used as a plug-and-play motor control module on a new task (right).

After training, the low-level controller can be reused to learn new tasks, where a high-level controller is optimised to output motor intentions directly. This enables efficient exploration – since coherent behaviours are produced, even with randomly sampled motor intentions – and constrains the final solution.

## Emergent team coordination in humanoid football

Football has been [a long-standing challenge](https://link.springer.com/chapter/10.1007/3-540-64473-3_46) for embodied intelligence research, requiring individual skills and coordinated team play. In our latest work, we used an NPMP as a prior to guide the learning of movement skills.

The result was a team of players which progressed from learning ball-chasing skills, to finally learning to coordinate. Previously, in a [study with simple embodiments](https://openreview.net/forum?id=BkG8sjR5Km), we had shown that coordinated behaviour can emerge in teams competing with each other. The NPMP allowed us to observe a similar effect but in a scenario that required significantly more advanced motor control.

![An orange 3D humanoid agent mimics the walking and turning movements of a semi-transparent gray motion capture character on a tiled blue surface.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/630f6d699c09633d3acf48f2_football20blog203.gif)

![Three-panel diagram showing a blue humanoid agent in a simulated football field. Panel one, labeled "Follow," shows the agent standing near a blue-to-red path. Panel two, labeled "Dribble," shows the agent moving next to a football. Panel three, labeled "Kick to target," shows the agent standing on a white line.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/630f6d7c7e2a3064bd727f40_football20blog204.gif)

Agents first mimic the movement of football players to learn an NPMP module (top). Using the NPMP, the agents then learn football-specific skills (bottom).

Our agents acquired skills including agile locomotion, passing, and division of labour as demonstrated by a range of statistics, including metrics used in [real-world sports analytics](https://www.researchgate.net/profile/William-Spearman/publication/327139841_Beyond_Expected_Goals/links/5b7c3023a6fdcc5f8b5932f7/Beyond-Expected-Goals.pdf). The players exhibit both agile high-frequency motor control and long-term decision-making that involves anticipation of teammates’ behaviours, leading to coordinated team play.

![Three simulated humanoid agents—one in a red jersey dribbling a soccer ball, and two in blue jerseys defending—playing on a green, striped digital soccer pitch with a goal in the background.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/630f6e29ba1f6d269aff7c2d_football20blog205.gif)

An agent learning to play football competitively using multi-agent RL.

## Whole-body manipulation and cognitive tasks using vision

Learning to interact with objects using the arms is another difficult control challenge. The NPMP can also enable this type of whole-body manipulation. With a small amount of MoCap data of interacting with boxes, we’re able to [train an agent to carry a box](https://www.youtube.com/watch?v=2rQAW-8gQQk) from one location to another, using egocentric vision and with only a sparse reward signal:

![An orange 3D humanoid character, surrounded by glowing green tracking markers, walks toward a gray box on a tiled blue floor, picks it up, and carries it away.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/630f6f62cacfa971dd2e681e_Football20blog206.gif)

![An orange 3D humanoid character, shown from both a first-person egocentric camera view on the left and a third-person view on the right, catches a ball thrown at it and throws it back on a blue tiled floor.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/630f6f73a8d8fad56ff930ae_Football20blog207.gif)

With a small amount of MoCap data (top), our NPMP approach can solve a box carrying task (bottom).

Similarly, we can teach the agent to catch and throw balls:

![An orange 3D humanoid character, shown from both a first-person egocentric camera view on the left and a third-person view on the right, catches a ball thrown at it and throws it back on a blue tiled floor.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/630f6fac40b994092e8e6e81_Football20blog208.gif)

Simulated humanoid catching and throwing a ball.

Using NPMP, we can also tackle [maze tasks involving locomotion, perception and memory](https://openreview.net/forum?id=BJfYvo09Y7):

![A three-panel demonstration of a humanoid character navigating a maze task. The left panel shows the first-person egocentric camera view, the middle panel displays a top-down schematic map of the red and blue maze with several rooms, and the right panel shows a third-person view of the orange humanoid running through the blue corridors.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/630f70036725db20fe779940_Football20blog209.gif)

Simulated humanoid collecting blue spheres in a maze.

## Safe and efficient control of real-world robots

The NPMP can also help to control real robots. Having well-regularised behaviour is critical for activities like walking over rough terrain or handling fragile objects. Jittery motions can damage the robot itself or its surroundings, or at least drain its battery. Therefore, significant effort is often invested into designing learning objectives that make a robot do what we want it to while behaving in a safe and efficient manner.

As an alternative, we investigated whether using [priors derived from biological motion](https://arxiv.org/abs/2203.17138) can give us well-regularised, natural-looking, and reusable movement skills for legged robots, such as walking, running, and turning that are suitable for deploying on real-world robots.

Starting with MoCap data from humans and dogs, we adapted the NPMP approach to train skills and controllers in simulation that can then be deployed on real humanoid (OP3) and quadruped (ANYmal B) robots, respectively. This allowed the robots to be steered around by a user via a joystick or dribble a ball to a target location in a natural-looking and robust way.

![A simulated stick-figure quadruped dog walks, trots, and turns on a dark, tiled blue surface, demonstrating natural-looking biological motion capture-derived movement skills.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/630f73af3cbb9ede40ae9f98_Football20blog2010.gif)

Locomotion skills for the ANYmal robot are learned by imitating dog MoCap.

![A small, dark humanoid robot walks stably and controllably on a blue mat inside a walled-in testing area.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/630f73ed0b5f123a00699490_Football20blog2011.gif)

![A four-legged quadruped robot dribbles an orange ball across a green turf field, successfully guiding it into a designated red circular target area.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/630f741e73d0d9437e370ec8_Football20blog2012.gif)

Locomotion skills can then be reused for controllable walking and ball dribbling.

## Benefits of using neural probabilistic motor primitives

In summary, we’ve used the NPMP skill model to learn complex tasks with humanoid characters in simulation and real-world robots. The NPMP packages low-level movement skills in a reusable fashion, making it easier to learn useful behaviours that would be difficult to discover by unstructured trial and error. Using motion capture as a source of prior information, it biases learning of motor control toward that of naturalistic movements.

The NPMP enables embodied agents to learn more quickly using RL; to learn more naturalistic behaviours; to learn more safe, efficient and stable behaviours suitable for real-world robotics; and to combine full-body motor control with longer horizon cognitive skills, such as teamwork and coordination.

Learn more about our work**:**

- See selected [research references](https://storage.googleapis.com/deepmind-media/From%20motor%20control%20to%20embodied%20intelligence/From%20motor%20control%20to%20embodied%20intelligence%20-%20selected%20references.pdf).
- Read [our paper](https://www.science.org/doi/10.1126/scirobotics.abo0235) on Humanoid Football in Science Robotics or watch the [summary video](https://www.youtube.com/watch?v=tWnGTtbOK7I).
- Read [our paper](https://dl.acm.org/doi/abs/10.1145/3386569.3392474) on humanoid whole-body control or watch the [summary video](https://www.youtube.com/watch?v=2rQAW-8gQQk).
- Read [our paper](https://arxiv.org/abs/2203.17138) on control of real-world robots or watch the [summary video](https://youtu.be/K77HS6uO5F8).
