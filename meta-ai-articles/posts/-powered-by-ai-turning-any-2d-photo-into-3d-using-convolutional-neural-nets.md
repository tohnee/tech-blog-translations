---
title: "-powered-by-ai-turning-any-2d-photo-into-3d-using-convolutional-neural-nets"
date: 2020-02-28
source: https://ai.facebook.com/blog/-powered-by-ai-turning-any-2d-photo-into-3d-using-convolutional-neural-nets
crawled: 2026-09-22
---

Our [3D Photos feature](https://www.facebook.com/help/414295416095269) on Facebook launched in 2018 as a new, immersive format for sharing pictures with friends and family. The feature has relied on the dual-lens “portrait mode” capabilities available only in new, higher-end smartphones, however. So it hasn’t been available on typical mobile devices, which have only a single, rear-facing camera. To bring this new visual format to more people, we have used state-of-the-art machine learning techniques to produce 3D photos from virtually any standard 2D picture. This system infers the 3D structure of any image, whether it is a new shot just taken on an Android or iOS device with a standard single camera, or a decades-old image recently uploaded to a phone or laptop.

This advance makes 3D photo technology easily accessible for the first time to the many millions of people who use single-lens camera phones or tablets. It also allows everyone to experience decades-old family photos and other treasured images in a new way, by converting them to 3D. People with state-of-the-art dual-camera devices can benefit, too, since they can now use their single, front-facing camera to take 3D selfies. Anyone with an iPhone 7 or higher, or a recent midrange or better Android device, can now try these options in the Facebook app.

![](https://static.xx.fbcdn.net/rsrc.php/v3/y4/r/-PAXP-deijE.gif)

Something Went Wrong

We're having trouble playing this video.

[Learn More](https://www.facebook.com/help/396404120401278/list)

This animation shows how the the depth of different areas of a 2D picture is estimated in order to create a 3D image.

Building this enhanced 3D Photos technique required overcoming a variety of technical challenges, such as training a model that correctly infers 3D positions of an extremely wide variety of subject matter and optimizing the system so that it works on-device on typical mobile processors in a fraction of a second. To overcome these challenges, we trained a convolutional neural network (CNN) on millions of pairs of public 3D images and their accompanying depth maps, and leveraged a variety of mobile-optimization techniques previously developed by Facebook AI, such as [FBNet](https://ai.facebook.com/blog/differentiable-neural-architecture-search-for-accurate-efficient-cnns/) and [ChamNet](https://ai.facebook.com/blog/platform-aware-ai-to-design-neural-networks/). (We’ve also discussed our recent [related research on 3D understanding here](https://ai.facebook.com/blog/pushing-state-of-the-art-in-3d-content-understanding/)).

Now that this feature is available to everyone who uses Facebook, we are sharing details of how we built it.

![](https://static.xx.fbcdn.net/rsrc.php/v3/y4/r/-PAXP-deijE.gif)

Something Went Wrong

We're having trouble playing this video.

[Learn More](https://www.facebook.com/help/396404120401278/list)

The original photo of the puppy was taken with a single-lens camera and did not contain any depth map data. Our system converted it into the 3D image shown here.

## Delivering highly efficient performance on mobile devices

Given a standard RGB image, the 3D Photos CNN can estimate a distance from the camera for each pixel. We accomplished this through four means:

- A network architecture built with a set of parameterizable, mobile-optimized neural building blocks.
- Automated architecture search to find an effective configuration of these blocks, enabling the system to perform the task in under a second on a wide range of devices.
- Quantization-aware training to leverage high-performance INT8 quantization on mobile while minimizing potential quality degradation from the quantization process.
- Large amounts of training data derived from public 3D photos.

## Neural building blocks

Our architecture uses building blocks inspired by [FBNet](https://l.facebook.com/l.php?u=https%3A%2F%2Fresearch.fb.com%2Fpublications%2Ffbnet-hardware-aware-efficient-convnet-design-via-differentiable-neural-architecture-search%2F&h=AT0xnZEZj9joq4tfeR9LAa3iMXM2IEI6mabKtHioDh8yGhXlmvGpAgxkLM_pt1-AE9TYJ0dN6f_gMyqt4yUy7UzPzQe6OUV5yRW0n3wK9yhR-bZ9_Sj-2nxYeaN7umiix83AUHEs-sb5pQhj), a framework to optimize ConvNet architectures for mobile and other resource-constrained devices. A building block consists of point-wise convolution, optional upsampling, K x K depthwise convolution, and an additional point-wise convolution. We implement a U-net style architecture that has been modified to place FBNet building blocks along the skip connection. The U-net encoder and decoder each contain five stages, each corresponding to a different spatial resolution.

![](https://static.xx.fbcdn.net/rsrc.php/v3/y4/r/-PAXP-deijE.gif)

Something Went Wrong

We're having trouble playing this video.

[Learn More](https://www.facebook.com/help/396404120401278/list)

Overview of our network architecture. Our network architecture is a U-net with additional macro-level building blocks placed along the skip connections.

## Automated architecture search

In order to find an effective architecture configuration, we automated the search process using [ChamNet](https://l.facebook.com/l.php?u=https%3A%2F%2Fresearch.fb.com%2Fpublications%2Fchamnet-towards-efficient-network-design-through-platform-aware-model-adaptation%2F&h=AT2oa7UsOPhibXtzPW6sjjdTS1Jz8ciG0bbHIKxGT1QyolF0L8C4w9fjbOOiZ1AhMtF7HZuQFdipRGeRhVcNIU6LW8qUK7qdiADFgQ_rB6mzeQKDzSvO7RHUEyL77XZQZ80IYhTdPVeBE0UT), an algorithm developed by Facebook AI. The ChamNet algorithm iteratively samples points from the search space to train an accuracy predictor. This accuracy predictor is used to accelerate a genetic search to find a model that maximizes predicted accuracy while satisfying specified resource constraints. In this setting, we used a search space that varies the channel expansion factor and number of output channels per block, resulting in 3.4x1022 possible architectures. We then completed the search in approximately three days using 800 Tesla V100 GPUs, setting and then adjusting a FLOP constraint on the model architecture in order to achieve different operating points.

## Quantization-aware training

By default, our model is trained using single-precision floating point weights and activations, but we found significant advantages to quantizing both weights and activations to be only 8 bits. In particular, int8 weights require only a quarter of the storage required of float32 weights, thereby reducing the number of bytes that must be transferred to the device on first use.

![](https://static.xx.fbcdn.net/rsrc.php/v3/y4/r/-PAXP-deijE.gif)

Something Went Wrong

We're having trouble playing this video.

[Learn More](https://www.facebook.com/help/396404120401278/list)

Each of these images started as a regular 2D image and was transformed to 3D with our depth estimation neural network.

Int8-based operators also have much higher throughput compared with their float32 counterparts, thanks to well-tuned libraries such as Facebook AI’s [QNNPACK](https://ai.facebook.com/blog/qnnpack-open-source-library-for-optimized-mobile-deep-learning/), which has been integrated into PyTorch. We used quantization-aware training (QAT) to avoid an unacceptable drop in quality due to quantization. [QAT, which is now available as part of PyTorch](https://l.facebook.com/l.php?u=https%3A%2F%2Fpytorch.org%2Fdocs%2Fstable%2Fquantization.html&h=AT0m-NwEMaaNkzGG80kOXnL9RrSdeIKxN9gdMKg1MdZ1O0WBHUGgu6L15M9py904MGaZCJkVV-FDH87KxYzoeXVDnwghb4eJjUiA--No_NnrhfLGPDLN06WNUugZudHh6quluLPUCav7atea), simulates quantization during training and supports back propagation, thereby eliminating the gap between training and production performance.

![](https://static.xx.fbcdn.net/rsrc.php/v3/y4/r/-PAXP-deijE.gif)

Something Went Wrong

We're having trouble playing this video.

[Learn More](https://www.facebook.com/help/396404120401278/list)

Our neural network works on a variety of content, including paintings and images of complex scenes. (Trevi Fountain photo taken by Livioandronic2013 and shared under a https://creativecommons.org/licenses/by-sa/4.0/ license.)

## Finding new ways to create 3D experiences

In addition to refining and improving our depth estimation algorithm, we’re working toward enabling high-quality depth estimation for videos taken with mobile devices. Videos pose a noteworthy challenge, since each frame depth must be consistent with the next. But it is also an opportunity to improve performance, since multiple observations of the same objects can provide additional signal for highly accurate depth estimations. Video-length depth estimation will open up a variety of innovative content creation tools to our users. As we continue to improve the performance of our neural network, we will also explore leveraging depth estimation, surface normal estimation, and spatial reasoning in real-time applications such as augmented reality.

Beyond these potential new experiences, this work will help us better understand the content of 2D images more generally. Improved understanding of 3D scenes could also help robots navigate and interact with the physical world. We hope that by sharing details about our 3D Photos system, we will help the AI community make progress in these areas and create new experiences that leverage advanced 3D understanding.

## Written by

Kevin Matzen

Research Scientist

Matthew Yu

Software Engineer

Jonathan Lehman

Software Engineer

Peizhao Zhang

Research Scientist

Jan-Michael Frahm

Research Scientist Manager

Peter Vajda

Research Scientist Manager

Johannes Kopf

Research Scientist Manager

Matt Uyttendaele

Engineering Director

## Related posts

[Introducing PyTorch3D: An open-source library for 3D deep learning](https://ai.facebook.com/blog/-introducing-pytorch3d-an-open-source-library-for-3d-deep-learning/)

February 06, 2020

[Pushing the state of the art in 3D content understanding](https://ai.facebook.com/blog/pushing-state-of-the-art-in-3d-content-understanding/)

October 29, 2019

[A new dense, sliding-window technique for instance segmentation](https://ai.facebook.com/blog/a-new-dense-sliding-window-technique-for-instance-segmentation/)

October 28, 2019

## Related Tags

[ML Applications](https://ai.facebook.com/blog/results/ml-applications/)

[Computer Vision](https://ai.facebook.com/blog/results/computer-vision/)

[Research](https://ai.facebook.com/blog/results/research/)
