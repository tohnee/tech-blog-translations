---
title: "Building 3D deep learning models with PyTorch3D"
date: 2020-06-12
source: https://ai.facebook.com/blog/building-3d-deep-learning-models-with-pytorch3d
crawled: 2026-09-22
---

June 12, 2020 Share on Facebook Share on Twitter In the same way that Torchvision and Detectron2 offer highly optimized libraries for 2D computer vision, PyTorch3D offers capabilities that support 3D data. Our open source library for 3D deep learning includes support for easy batching of heterogeneous meshes and point clouds, optimized implementations of common 3D operators such as Chamfer Loss and Graph Conv, as well as a modular, differentiable renderer for point clouds and meshes. We’re already using PyTorch3D at Facebook for research projects such as Mesh R-CNN and SynSin . Since the initial release in February 2020, we’ve added new features, including point cloud rendering, point-to-mesh distances, fast KNN, normal estimation, and more. These operators all support batching, are optimized and differentiable, and are ready to plug into deep learning pipelines. Learn more about how it works in this video by PyTorch3D co-creator and software engineer Nikhila Ravi. Watch the video to learn more: Something Went Wrong We're having trouble playing this video. Learn more You can try the code and tutorials here. Read more about PyTorch3D here. Join our CVPR 2020 Tutorial on Visual Recognition for Images, Video, and 3D. Share on Facebook Share on Twitter
