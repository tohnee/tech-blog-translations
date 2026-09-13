---
title: "D4RT: Teaching AI to see the world in four dimensions"
source: https://deepmind.google/blog/d4rt-teaching-ai-to-see-the-world-in-four-dimensions/
site: deepmind
date: 2026-01-22
authors: Guillaume Le Moing, Mehdi S. M. Sajjadi
crawled: 2026-09-13
---

Introducing D4RT, a unified AI model for 4D scene reconstruction and tracking across space and time.

Anytime we look at the world, we perform an extraordinary feat of memory and prediction. We see and understand things as they are at a given moment in time, as they were a moment ago, and how they are going to be in the moment to follow. Our mental model of the world maintains a persistent representation of reality and we use that model to draw intuitive conclusions about the causal relationship between the past, present and future.

To help machines see the world more like we do, we can equip them with cameras, but that only solves the problem of input. To make sense of this input, computers must solve a complex, inverse problem: taking a video — which is a sequence of flat 2D projections — and recovering or understanding the rich, volumetric 3D world, in motion.

Today, we are introducing [D4RT (Dynamic 4D Reconstruction and Tracking)](https://d4rt-paper.github.io/), a new AI model that unifies dynamic scene reconstruction into a single, efficient framework, bringing us closer to the next frontier of artificial intelligence: total perception of our dynamic reality.

## The Challenge of the Fourth Dimension

In order for it to understand a dynamic scene captured on a 2D video, an AI model must track every pixel of every object as it moves through the three dimensions of space and the fourth dimension of time. In addition, it must disentangle this motion from the motion of the camera, maintaining a coherent representation even when objects move behind one another or leave the frame entirely. Traditionally, capturing this level of geometry and motion from 2D videos requires computationally intensive processes or a patchwork of specialized AI models — some for depth, others for movement or camera angles — resulting in AI reconstructions that are slow and fragmented.

D4RT’s simplified architecture and novel query mechanism place it at the forefront of 4D reconstruction while being up to 300x more efficient than previous methods — fast enough for real-time applications in robotics, augmented reality, and more.

## How D4RT Works: A Query-Based Approach

D4RT operates as a unified encoder-decoder Transformer architecture. The encoder first processes the input video into a compressed representation of the scene’s geometry and motion. Unlike older systems that employed separate modules for different tasks, D4RT calculates only what it needs using a flexible querying mechanism centered around a single, fundamental question:

"Where is **a given pixel** from the video located **in 3D space** at an arbitrary **time**, as viewed from a **chosen camera**?"

Building on [our prior work](https://srt-paper.github.io/), a lightweight decoder then queries this representation to answer specific instances of the posed question. Because queries are independent, they can be processed in parallel on modern AI hardware. This makes D4RT extremely fast and scalable, whether it’s tracking just a few points or reconstructing an entire scene.

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

D4RT combines a powerful encoder that builds a rich, global understanding of the video, and a lightweight decoder that answers thousands of queries in parallel. By asking specific questions — identifying where a source pixel is located at a target time and camera view — the model efficiently solves diverse tasks like tracking, depth estimation, and pose estimation through a single, flexible interface.

## Capabilities: Fast, Accurate 4D Understanding

With this flexible formulation, a wide variety of 4D tasks can now be solved by the model, including:

- **Point Tracking**: By querying a pixel's location across different time steps, D4RT can predict its 3D trajectory. Importantly, an object need not be visible on other frames of the video for the model to make a prediction.
- **Point Cloud Reconstruction**: By freezing time and the camera viewpoint, D4RT can directly generate the complete 3D structure of a scene, eliminating extra steps such as separate camera estimation or per-video iterative optimization.
- **Camera Pose Estimation**: By generating and aligning 3D snapshots of a single moment from different viewpoints, D4RT can easily recover the camera's trajectory.

As detailed in the [underlying technical report](https://arxiv.org/abs/2512.08924), D4RT outperforms previous methods across a wide spectrum of 4D reconstruction tasks. Qualitative comparisons show that while other methods struggle with dynamic objects — often duplicating them or failing to reconstruct them entirely — D4RT maintains a solid, continuous understanding of the moving world.

Crucially, D4RT’s precision does not come at the expense of efficiency. In testing, it performed 18x to 300x faster than the previous state of the art. For example, D4RT processed a one-minute video in roughly five seconds on a single TPU chip. Previous state-of-the-art methods could take up to ten minutes for the same task — an improvement of 120x.

Slide 1 of 3

![A bar chart titled "Point Cloud Reconstruction on MPI Sintel" comparing 3D Fidelity (2 minus L1 error, higher is better) across six models. From lowest to highest performance, the scores are: MapAnything at 0.282, VGGT at 0.420, MegaSaM at 0.469, SpatialTrackerV2 at 0.625, π3 at 0.861, and D4RT leading with the highest score of 1.091, highlighted in a bright blue bar.](https://lh3.googleusercontent.com/XpEVj8v4dIrVaUtViFeyGyY4fyRUMnvpIcP9jheHwWS17VhKk5eGNoHWQNoXzRKIOxHxNj3kU0AlD-8kDE-gxHOeM_dwSa2CZbxTMWoQAtMUy0Mxcwc=w1440-h810-n-nu)![A bar chart titled "Point Cloud Reconstruction on MPI Sintel" comparing 3D Fidelity (2 minus L1 error, higher is better) across six models. From lowest to highest performance, the scores are: MapAnything at 0.282, VGGT at 0.420, MegaSaM at 0.469, SpatialTrackerV2 at 0.625, π3 at 0.861, and D4RT leading with the highest score of 1.091, highlighted in a bright blue bar.](https://lh3.googleusercontent.com/muuplDDRZOonBlJAm4pYP3QJhNlRXlGzFWoXsnpIAnpUgUoIl5_z4UacYi0f6NuejmFJ48m7PKHpHRn6-4ieX6-0KVsjNEJv6EhBuShwYE4HC5KrAAQ=w1440-h810-n-nu)

In evaluations on the MPI Sintel benchmark featuring complex synthetic scenes with fast motion blur and non-rigid deformation, D4RT demonstrates superior fidelity compared to recent strong baselines. This highlights the model’s ability to reconstruct geometry accurately even when objects or the camera move rapidly through the scene.

![A bar chart titled "Point Tracking on Aria Digital Twin" comparing 3D Fidelity (2 minus L1 error, higher is better) across four models. From lowest to highest performance, the scores are: St4RTrack at 1.161, CoTracker3 + VGGT at 1.264, SpatialTrackerV2 at 1.762, and D4RT leading with the highest score of 1.904, highlighted in a bright blue bar.](https://lh3.googleusercontent.com/g6EamdthyxHW3RAZn0ln9LwWVTDdIAb9-LFcTyzdqzG0Ya20gMb6txonCrAivra7zqo256Bj03-4YquLVONufp2sXLkMWO1EkEjoi24BCHJx-NtIM6k=w1440-h810-n-nu)![A bar chart titled "Point Tracking on Aria Digital Twin" comparing 3D Fidelity (2 minus L1 error, higher is better) across four models. From lowest to highest performance, the scores are: St4RTrack at 1.161, CoTracker3 + VGGT at 1.264, SpatialTrackerV2 at 1.762, and D4RT leading with the highest score of 1.904, highlighted in a bright blue bar.](https://lh3.googleusercontent.com/4-7pj8axU2Z9RTs7rcnVN4XJxcSS1x9QaM23ogfVlz0k3xwdms06i5ArIWC3FCANXRqfYy7fP-FbepGqTrwdXFw4rYdBGfuzVrcXs8P6mhcSUroPbg=w1440-h810-n-nu)

Using smart-glasses footage from the Aria Digital Twin dataset, D4RT achieves top-tier performance in 3D point tracking. This verifies the model's robust handling of complex ego-motion and occlusions in realistic household environments.

![A bar chart titled "Camera Pose Estimation on RE10k" comparing Pose AUC across five models. From lowest to highest performance, the scores are: VGGT at 0.702, MegaSaM at 0.710, SpatialTrackerV2 at 0.757, π3 at 0.787, and D4RT leading with the highest score of 0.835, highlighted in a bright blue bar.](https://lh3.googleusercontent.com/UoGso_JmalQ1HFec6Vw4LPY8qShLWVmaSUEDR3nAWca0VA8PVJpMr5olAYC7kw1KMKqtFTbmY7fCjnagrEqF1o02CEvtQhRSqR1ezeBeHwobSrrH=w1440-h810-n-nu)![A bar chart titled "Camera Pose Estimation on RE10k" comparing Pose AUC across five models. From lowest to highest performance, the scores are: VGGT at 0.702, MegaSaM at 0.710, SpatialTrackerV2 at 0.757, π3 at 0.787, and D4RT leading with the highest score of 0.835, highlighted in a bright blue bar.](https://lh3.googleusercontent.com/EtGSifMr1elbDT1MtcHCK1EDj6EMcFNqACQsrtWr5oisX4F0LcGqBxDmW1Ehtf-yfM6bhT63LGrIuNCVzR9dxt2vEHSECgXEiuTkUFjFdsFJdwxCHvY=w1440-h810-n-nu)

Evaluating camera pose estimation on the diverse indoor and outdoor scenes of the RE10k dataset, D4RT achieves the highest AUC score. This metric, which tracks how often the estimated pose falls within a range of strict accuracy thresholds, illustrates the model’s capacity to lock onto stable geometry without the need for costly test-time optimization.

## Downstream Applications

D4RT demonstrates that we don't need to choose between accuracy and efficiency in 4D reconstruction. Its flexible, query-based system can capture our dynamic world in real-time, paving the way for the next generation of spatial computing. This includes:

- **Robotics**: Robots need to navigate dynamic environments populated by moving people and objects. D4RT can provide the spatial awareness required for safe navigation and dextrous manipulation.
- **Augmented Reality (AR)**: For AR glasses to overlay digital objects onto the real world, they need an instant, low-latency understanding of a scene’s geometry. D4RT’s efficiency contributes to making on-device deployment a tangible reality.
- **World Models**: By effectively disentangling camera motion, object motion, and static geometry, D4RT brings us a step closer to AI that possesses a true “world model” of physical reality — a necessary step on the path to AGI.

We're continuing to explore the model’s capabilities and potential for applications across robotics, augmented reality, and beyond.

[Read our technical report](https://arxiv.org/abs/2512.08924)[Visit our project website](https://d4rt-paper.github.io/)
