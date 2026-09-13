---
title: "Neural scene representation and rendering"
source: https://deepmind.google/blog/neural-scene-representation-and-rendering/
site: deepmind
date: 2018-06-14
authors: Ali Eslami, Danilo Jimenez Rezende
crawled: 2026-09-13
---

There is more than meets the eye when it comes to how we understand a visual scene: our brains draw on prior knowledge to reason and to make inferences that go far beyond the patterns of light that hit our retinas. For example, when entering a room for the first time, you instantly recognise the items it contains and where they are positioned. If you see three legs of a table, you will infer that there is probably a fourth leg with the same shape and colour hidden from view. Even if you can’t see everything in the room, you’ll likely be able to sketch its layout, or imagine what it looks like from another perspective.

These visual and cognitive tasks are seemingly effortless to humans, but they represent a significant challenge to our artificial systems. Today, state-of-the-art visual recognition systems are trained using large datasets of annotated images produced by humans. Acquiring this data is a costly and time-consuming process, requiring individuals to label every aspect of every object in each scene in the dataset. As a result, often only a small subset of a scene’s overall contents is captured, which limits the artificial vision systems trained on that data. As we develop more complex machines that operate in the real world, we want them to fully understand their surroundings: where is the nearest surface to sit on? What material is the sofa made of? Which light source is creating all the shadows? Where is the light switch likely to be?

In this work, [published in Science](http://science.sciencemag.org/cgi/content/full/360/6394/1204?ijkey=kGcNflzOLiIKQ&keytype=ref&siteid=sci) ([Open Access version](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/neural-scene-representation-and-rendering/Neural%20Scene%20Representation%20and%20Rendering%20-%20Related%20Work.pdf)), we introduce the Generative Query Network (GQN), a framework within which machines learn to perceive their surroundings by training only on data obtained by themselves as they move around scenes. Much like infants and animals, the GQN learns by trying to make sense of its observations of the world around it. In doing so, the GQN learns about plausible scenes and their geometrical properties, without any human labelling of the contents of scenes.

The GQN model is composed of two parts: a representation network and a generation network. The representation network takes the agent's observations as its input and produces a representation (a vector) which describes the underlying scene. The generation network then predicts (‘imagines’) the scene from a previously unobserved viewpoint.

The representation network does not know which viewpoints the generation network will be asked to predict, so it must find an efficient way of describing the true layout of the scene as accurately as possible. It does this by capturing the most important elements, such as object positions, colours and the room layout, in a concise distributed representation. During training, the generator learns about typical objects, features, relationships and regularities in the environment. This shared set of ‘concepts’ enables the representation network to describe the scene in a highly compressed, abstract manner, leaving it to the generation network to fill in the details where necessary. For instance, the representation network will succinctly represent ‘blue cube’ as a small set of numbers and the generation network will know how that manifests itself as pixels from a particular viewpoint.

We performed controlled experiments on the GQN in a collection of procedurally-generated environments in a simulated 3D world, containing multiple objects in random positions, colours, shapes and textures, with randomised light sources and heavy occlusion. After training on these environments, we used GQN’s representation network to form representations of new, previously unobserved scenes. We showed in our experiments that the GQN exhibits several important properties:

- The GQN’s generation network can ‘imagine’ previously unobserved scenes from new viewpoints with remarkable precision. When given a scene representation and new camera viewpoints, it generates sharp images without any prior specification of the laws of perspective, occlusion, or lighting. The generation network is therefore an approximate [renderer](https://en.wikipedia.org/wiki/Rendering_(computer_graphics)) that is learned from data:

![Two images compare observation with neural rendering. To represent observation there is a static image of a two 3D shapes inside a box from a single viewpoint. For neural rendering there is a moving image, seeing that same box from multiple sides and angles.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62268c802b032b4a45307265_GQN202.gif)

- The GQN’s representation network can learn to count, localise and classify objects without any object-level labels. Even though its representation can be very small, the GQN’s predictions at query viewpoints are highly accurate and almost indistinguishable from ground-truth. This implies that the representation network perceives accurately, for instance identifying the precise configuration of blocks that make up the scenes below:

![Observation and neural rendering are shown side by side. For observation there's a static image of a multicoloured 3D shape on a black background. For neural rendering that same 3D shape spins around in the space, so we see it from every angle.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62268c9404f53c40276f787e_GQN203.gif)

- The GQN can represent, measure and reduce uncertainty. It is capable of accounting for uncertainty in its beliefs about a scene even when its contents are not fully visible, and it can combine multiple partial views of a scene to form a coherent whole. This is shown by its first-person and top-down predictions in the figure below. The model expresses its uncertainty through the variability of its predictions, which gradually reduces as it moves around the maze (grey cones indicate observation locations, yellow cone indicates query location):

![Moving around a 3D maze, there is a series of static observations. Below that are two matching videos representing neural rendering and ground truth. A map shows how the viewpoint is  moving around the space.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62268ca3933713959ce79a77_GQN201.gif)

- The GQN’s representation allows for robust, data-efficient reinforcement learning. When given GQN’s compact representations, state-of-the-art deep reinforcement learning agents learn to complete tasks in a more data-efficient manner compared to model-free baseline agents, as shown in the figure below. To these agents, the information encoded in the generation network can be seen to be ‘innate’ knowledge of the environment:

![A comparison of reinforcement learning agent performance using GQN representation versus raw pixels. On the left, examples of observation, GQN prediction, and ground truth show a robotic arm interacting with objects. Two line graphs plot reward over 30 million training epochs for a fixed camera and a moving camera setup, demonstrating that GQN representation (blue lines) achieves higher rewards much faster than raw pixels (orange lines), especially in the moving camera condition where raw pixels fail to learn.](https://lh3.googleusercontent.com/HwNXPghKHsh5IWswYCg7CARynSm7kt6hd5RX-bd1cmZrk0GNJGq1r2WuJkQsYmgN8JBlvFG6zYkHH2mbZhTEk73zO0bc2AG08vw84zSls7hfcANjkw=w1440)

Using GQN we observe substantially more data-efficient policy learning, obtaining convergence-level performance with approximately 4 times fewer interactions than a standard method using raw pixels.

GQN builds upon a large literature of recent related work in multi-view geometry, generative modelling, unsupervised learning and predictive learning, which we discuss [here](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/neural-scene-representation-and-rendering/Neural%20Scene%20Representation%20and%20Rendering%20-%20Related%20Work.pdf), in the [Science paper](http://science.sciencemag.org/cgi/content/full/360/6394/1204?ijkey=kGcNflzOLiIKQ&keytype=ref&siteid=sci) and the [Open Access version](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/neural-scene-representation-and-rendering/Neural%20Scene%20Representation%20and%20Rendering%20-%20Related%20Work.pdf). It illustrates a novel way to learn compact, grounded representations of physical scenes. Crucially, the proposed approach does not require domain-specific engineering or time-consuming labelling of the contents of scenes, allowing the same model to be applied to a range of different environments. It also learns a powerful neural renderer that is capable of producing accurate images of scenes from new viewpoints.

Our method still has many limitations when compared to more traditional computer vision techniques, and has currently only been trained to work on synthetic scenes. However, as new sources of data become available and advances are made in our hardware capabilities, we expect to be able to investigate the application of the GQN framework to higher resolution images of real scenes. In future work, it will also be important to explore the application of GQNs to broader aspects of scene understanding, for example by querying across space and time to learn a common sense notion of physics and movement, as well as applications in virtual and augmented reality.

While there is still much more research to be done before our approach is ready to be deployed in practice, we believe this work is a sizeable step towards fully autonomous scene understanding.

**Notes**

Watch the video [here](https://youtu.be/G-kWNQJ4idw).

Read more about the method in [the Science paper](http://science.sciencemag.org/cgi/content/full/360/6394/1204?ijkey=kGcNflzOLiIKQ&keytype=ref&siteid=sci).

Download the [Science paper](http://science.sciencemag.org/content/sci/360/6394/1204.full.pdf?ijkey=kpkRRXA1ckHD6&keytype=ref&siteid=sci) [PDF].

Download an [Open Access version](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/neural-scene-representation-and-rendering/Neural%20Scene%20Representation%20and%20Rendering%20-%20Related%20Work.pdf) [PDF].

Download the datasets used in the paper [here](https://github.com/deepmind/gqn-datasets).

Download an extended [list of related work](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/neural-scene-representation-and-rendering/Neural%20Scene%20Representation%20and%20Rendering%20-%20Related%20Work.pdf) [PDF].

Download the accompanying artwork ([portrait](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/neural-scene-representation-and-rendering/Neural%20Scene%20Representation%20and%20Rendering.jpeg) or [16:9](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/neural-scene-representation-and-rendering/Neural%20Scene%20Representation%20and%20Rendering%2016x9.jpeg)).

This work was done by S. M. Ali Eslami, Danilo J. Rezende, Frederic Besse, Fabio Viola, Ari S. Morcos, Marta Garnelo, Avraham Ruderman, Andrei A. Rusu, Ivo Danihelka, Karol Gregor, David P. Reichert, Lars Buesing, Theophane Weber, Oriol Vinyals, Dan Rosenbaum, Neil Rabinowitz, Helen King, Chloe Hillier, Matt Botvinick, Daan Wierstra, Koray Kavukcuoglu and Demis Hassabis.
