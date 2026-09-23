---
title: "How we’ve advanced Smart Camera for new Portal video-calling devices"
date: 2019-03-15
source: https://ai.facebook.com/blog/smart-camera-portal-advances
crawled: 2026-09-22
---

With the launch of three new Portal models today, we’re sharing an overview of how we’ve advanced Smart Camera , the AI-powered system that intelligently frames the action during video calls. Smart Camera was built on Facebook AI’s groundbreaking Mask R-CNN framework for object instance segmentation and keypoint detection. We’ve made additional speed and precision improvements in the computer vision models that power Smart Camera. We’re now using Detectron2, the new, second-generation object detection platform created by Facebook AI, to train Smart Camera’s pose estimation models. Because Detectron2 was developed in PyTorch , our deep learning platform, it enables faster model iteration. In addition to these model improvements, we’ve built custom hardware integrations for object detection and enhancements like foveated processing, which focuses processing on specific regions of the camera sensor. This work has allowed us to bring the Portal experience to lower-power IoT chipsets. Click on the video above to learn more. Share on Facebook Share on Twitter
