---
title: "Simple Sensor Intentions for Exploration"
source: https://deepmind.google/blog/simple-sensor-intentions-for-exploration/
site: deepmind
date: 2020-05-12
authors: Tim Hertweck, Martin Riedmiller, Michael Bloesch, Jost Tobias Springenberg, Noah Siegel, Markus Wulfmeier, Roland Hafner, Nicolas Heess
crawled: 2026-09-13
---

![A moving image of four blocks. In the first one, a green box is picked up by a grabber. The next block is the same but with a black background. In the third and fourth blocks, it shows a moving green bar chart; on the x and y axis respectively. The image then zooms out to show the same four part situation in different colours.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6228c5d829a96fa1b5f53db5_Fig201.gif)

By simple color-masking, high-level image statistics can be derived. Rewarding an agent for deliberately changing these statistics, leads to diverse exploration and interesting behavior like, for example, grasping or lifting objects.

## Example Skills

Learned from scratch and from pixels and proprioception only. The external rewards are sparse and Simple Sensor Intentions (SSIs) are used as the only auxiliary tasks.

![Two videos side by side. On the left, a robot with an orange arm grabs multiple changing objects from a flat, grey surface. On the right, the same robot catches a yellow ball in a large cup.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6228c5ead7858131e4ad7dd2_Fig202.gif)

