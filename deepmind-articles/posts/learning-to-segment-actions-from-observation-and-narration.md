---
title: "Learning to Segment Actions from Observation and Narration"
source: https://deepmind.google/blog/learning-to-segment-actions-from-observation-and-narration/
site: deepmind
date: 2020-05-07
authors: Daniel Fried, Jean-Baptiste Alayrac, Phil Blunsom, Chris Dyer, Stephen Clark, Aida Nematzadeh
crawled: 2026-09-13
---

Complex tasks that people carry out in the world, for example making pancakes, have multiple action steps (e.g., pouring the mixture, flipping the pancake, removing the pancake), and are structured. When we observe people carrying out tasks, we recognize where the action steps begin and end (pouring the mixture now, flipping the pancake later), and distinguish the important steps from the insignificant ones. Identifying important action steps and associating them with intervals of time is known as action segmentation, and is a crucial process for human cognition and planning. When people, and in particular, children, learn to segment actions, they rely on a number of cues, including descriptions narrated by the person carrying out the task (“now I’ll stir everything”..) and structural regularities in the task (mixing ingredients typically happens after adding the ingredients).

![Three lines; the first shows a written narration for making pancakes, underneath there's the video stills of the process, and below that there is the corresponding action segments.](https://lh3.googleusercontent.com/4XtdkmxuiWF_cDr3hGNHDqMwCDjD9lYBPwapAlosFoVyZkoKcNZCfBN8IXcP1bJURoZ3AICl-bEDviCgDqTZg8am---JsE_f30BgxjeERo5tz2Gh6Q=w1440)

In this work, inspired by how people learn to segment actions, we examine how effective language descriptions and task regularities are in improving systems for action segmentation. Action segmentation is an important first step for processing and cataloguing video: knowing which actions are occurring, and when, makes it easier to search for relevant videos and parts of video from a large, web-scale collection. However, standard, supervised, machine learning methods for predicting action segments in videos would require videos to be annotated with the action segments that occur in them. Since these annotations would be expensive and difficult to collect, we are interested in weakly-supervised action segmentation: training without annotated action segments.

We focus on a challenging dataset of instructional videos taken from YouTube [CrossTask, Zhukov et al. 2019], involving everyday household tasks such as cooking and assembling furniture. While these videos are naturally-occurring, they consist of tasks that have some structural regularities across videos, and have language descriptions (transcriptions of the person’s narration), which both provide a noisy source of weak supervision. We develop a flexible unsupervised model for action segmentation that can be trained without action labels, and can optionally use this weak supervision from the task regularities and language descriptions. Our model, and models from past work, both benefit substantially from both of these sources of supervision, even on top of rich features from state-of-the-art neural action and object classifiers. We also find that generative models of the video features typically have better performance than discriminative models on the segmentation task.

Our findings suggest that using language to guide action segmentation is a promising direction for future work, when annotations for the action segments are not available.
