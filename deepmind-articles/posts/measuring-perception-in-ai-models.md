---
title: "Measuring perception in AI models"
source: https://deepmind.google/blog/measuring-perception-in-ai-models/
site: deepmind
date: 2022-10-12
authors: Viorica Pătrăucean, Lucas Smaira, Ankush Gupta, Adrià Recasens Continente, Yi Yang, Mateusz Malinowski, Carl Doersch, Larisa Markeeva, Yury Sulsky, Dylan Banarse, Skanda Koppula, Tatiana Matejovicova, Antoine Miech, Alexandre Fréchette, Junlin Zhang, Hanna Klimczak-Plucińska, Stephanie Winkler, Yusuf Aytar, Raphael Koster, Simon Osindero, Dima Damen, Andrew Zisserman, João Carreira
crawled: 2026-09-13
---

New benchmark for evaluating multimodal systems based on real-world video, audio, and text data

From the [Turing test](https://en.wikipedia.org/wiki/Turing_test) to [ImageNet](https://www.image-net.org/), benchmarks have played an instrumental role in shaping artificial intelligence (AI) by helping define research goals and allowing researchers to measure progress towards those goals. Incredible breakthroughs in the past 10 years, such as [AlexNet](https://proceedings.neurips.cc/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf) in computer vision and [AlphaFold](https://www.deepmind.com/research/highlighted-research/alphafold) in protein folding, have been closely linked to using benchmark datasets, allowing researchers to rank model design and training choices, and iterate to improve their models. As we work towards the goal of building artificial general intelligence (AGI), developing robust and effective benchmarks that expand AI models’ capabilities is as important as developing the models themselves.

Perception – the process of experiencing the world through senses – is a significant part of intelligence. And building agents with human-level perceptual understanding of the world is a central but challenging task, which is becoming increasingly important in robotics, self-driving cars, personal assistants, medical imaging, and more. So today, we’re introducing the [Perception Test](https://storage.googleapis.com/dm-perception-test/perception_test_report.pdf), a multimodal benchmark using real-world videos to help evaluate the perception capabilities of a model.

## Developing a perception benchmark

Many perception-related benchmarks are currently being used across AI research, like [Kinetics](https://www.deepmind.com/open-source/kinetics) for video action recognition, [Audioset](https://research.google.com/audioset/) for audio event classification, [MOT](https://motchallenge.net/) for object tracking, or [VQA](https://visualqa.org/) for image question-answering. These benchmarks have led to amazing progress in how AI model architectures and training methods are built and developed, but each one only targets restricted aspects of perception: image benchmarks exclude temporal aspects; visual question-answering tends to focus on high-level semantic scene understanding; object tracking tasks generally capture lower-level appearance of individual objects, like colour or texture. And very few benchmarks define tasks over both audio and visual modalities.

Multimodal models, such as [Perceiver](https://deepmind.google/blog/building-architectures-that-can-handle-the-worlds-data/), [Flamingo](https://deepmind.google/blog/tackling-multiple-tasks-with-a-single-visual-language-model/), or [BEiT-3](https://arxiv.org/pdf/2208.10442.pdf), aim to be more general models of perception. But their evaluations were based on multiple specialised datasets because no dedicated benchmark was available. This process is slow, expensive, and provides incomplete coverage of general perception abilities like memory, making it difficult for researchers to compare methods.

To address many of these issues, we created a dataset of purposefully designed videos of real-world activities, labelled according to six different types of tasks:

1. **Object tracking:** a box is provided around an object early in the video, the model must return a full track throughout the whole video (including through occlusions).
2. **Point tracking:** a point is selected early on in the video, the model must track the point throughout the video (also through occlusions).
3. **Temporal action localisation:** the model must temporally localise and classify a predefined set of actions.
4. **Temporal sound localisation:** the model must temporally localise and classify a predefined set of sounds.
5. **Multiple-choice video question-answering:** textual questions about the video, each with three choices from which to select the answer.
6. **Grounded video question-answering:** textual questions about the video, the model needs to return one or more object tracks.

We took inspiration from the way children’s perception is assessed in developmental psychology, as well as from synthetic datasets like [CATER](https://rohitgirdhar.github.io/CATER/) and [CLEVRER](http://clevrer.csail.mit.edu/), and designed 37 video scripts, each with different variations to ensure a balanced dataset. Each variation was filmed by at least a dozen crowd-sourced participants (similar to previous work on [Charades](https://prior.allenai.org/projects/charades) and [Something-Something](https://developer.qualcomm.com/software/ai-datasets/something-something)), with a total of more than 100 participants, resulting in 11,609 videos, averaging 23 seconds long.

The videos show simple games or daily activities, which would allow us to define tasks that require the following skills to solve:

- **Knowledge of semantics:** testing aspects like task completion, recognition of objects, actions, or sounds.
- **Understanding of physics:** collisions, motion, occlusions, spatial relations.
- **Temporal reasoning or memory:** temporal ordering of events, counting over time, detecting changes in a scene.
- **Abstraction abilities:** shape matching, same/different notions, pattern detection.

Crowd-sourced participants labelled the videos with spatial and temporal annotations (object bounding box tracks, point tracks, action segments, sound segments). Our research team designed the questions per script type for the multiple-choice and grounded video-question answering tasks to ensure good diversity of skills tested, for example, questions that probe the ability to reason counterfactually or to provide explanations for a given situation. The corresponding answers for each video were again provided by crowd-sourced participants.

## Evaluating multimodal systems with the Perception Test

We assume that models have been pre-trained on external datasets and tasks. The Perception Test includes a small fine-tuning set (20%) that the model creators can optionally use to convey the nature of the tasks to the models. The remaining data (80%) consists of a public validation split and a held-out test split where performance can only be evaluated via our evaluation server.

Here we show a diagram of the evaluation setup: the inputs are a video and audio sequence, plus a task specification. The task can be in high-level text form for visual question answering or low-level input, like the coordinates of an object’s bounding box for the object tracking task.

![Flowchart of inputs and outputs of a model evaluated on our benchmark.](https://lh3.googleusercontent.com/ke9eHkI90XHD-N1MzaGyI6Wn61IBaYXSj8kH4ZvGZ_4_hO20lW_zlx_fkRwuV_lmQkb6y1iE_4rFMXeSOIR-wnlQLcrP9fLSnzcqAhf6oSBhfrRr1A=w1440)

The inputs (video, audio, task specification as text or other form) and outputs of a model evaluated on our benchmark.

The evaluation results are detailed across several dimensions, and we measure abilities across the six computational tasks. For the visual question-answering tasks we also provide a mapping of questions across types of situations shown in the videos and types of reasoning required to answer the questions for a more detailed analysis (see [our paper](https://storage.googleapis.com/dm-perception-test/perception_test_report.pdf) for more details). An ideal model would maximise the scores across all radar plots and all dimensions. This is a detailed assessment of the skills of a model, allowing us to narrow down areas of improvement.

![Three radar charts divided up into computational task, area, and reasoning type.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/634d53562d6ff7e92bbe527c_Perception_Fig_5_Amended.svg)

Multi-dimensional diagnostic report for a perception model by computational task, area, and reasoning type. Further diagnostics is possible into sub-areas like: motion, collisions, counting, action completion, and more.

Ensuring diversity of participants and scenes shown in the videos was a critical consideration when developing the benchmark. To do this, we selected participants from different countries of different ethnicities and genders and aimed to have diverse representation within each type of video script.

![World map with certain countries pinpointed to show geolocation of crowd-sourced participants involved in filming.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/63443fa08c26680347106a0a_Perception_Fig_1.svg)

Geolocation of crowd-sourced participants involved in filming.

## Learning more about the Perception Test

The Perception Test benchmark is publicly available [here](https://github.com/deepmind/perception_test/) and further details are available in [our paper](https://storage.googleapis.com/dm-perception-test/perception_test_report.pdf). A leaderboard and a challenge server will be available soon too.

On 23 October, 2022, we’re hosting a [workshop about general perception models](https://computerperception.github.io/) at the European Conference on Computer Vision in Tel Aviv ([ECCV 2022](https://eccv2022.ecva.net/)), where we will discuss our approach, and how to design and evaluate general perception models with other leading experts in the field.

We hope that the Perception Test will inspire and guide further research towards general perception models. Going forward, we hope to collaborate with the multimodal research community to introduce additional annotations, tasks, metrics, or even new languages to the benchmark.

Get in touch by emailing [perception-test@google.com](mailto:perception-test@google.com) if you're interested in contributing!
