---
title: "Tackling multiple tasks with a single visual language model"
source: https://deepmind.google/blog/tackling-multiple-tasks-with-a-single-visual-language-model/
site: deepmind
date: 2022-04-28
authors: Jean-Baptiste Alayrac, Jeff Donahue, Pauline Luc, Antoine Miech
crawled: 2026-09-13
---

One key aspect of intelligence is the ability to quickly learn how to perform a new task when given a brief instruction. For instance, a child may recognise real animals at the zoo after seeing a few pictures of the animals in a book, despite differences between the two. But for a typical visual model to learn a new task, it must be trained on tens of thousands of examples specifically labelled for that task. If the goal is to count and identify animals in an image, as in “three zebras”, one would have to collect thousands of images and annotate each image with their quantity and species. This process is inefficient, expensive, and resource-intensive, requiring large amounts of annotated data and the need to train a new model each time it’s confronted with a new task. As part of DeepMind’s mission to solve intelligence, we’ve explored whether an alternative model could make this process easier and more efficient, given only limited task-specific information.

Today, in the preprint of our [paper](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/tackling-multiple-tasks-with-a-single-visual-language-model/flamingo.pdf), we introduce Flamingo, a single visual language model (VLM) that sets a new state of the art in few-shot learning on a wide range of open-ended multimodal tasks. This means Flamingo can tackle a number of difficult problems with just a handful of task-specific examples (in a “few shots”), without any additional training required. Flamingo’s simple interface makes this possible, taking as input a prompt consisting of interleaved images, videos, and text and then output associated language.

Similar to the behaviour of large language models (LLMs), which can address a language task by processing examples of the task in their text prompt, Flamingo’s visual and text interface can steer the model towards solving a multimodal task. Given a few example pairs of visual inputs and expected text responses composed in Flamingo’s prompt, the model can be asked a question with a new image or video, and then generate an answer.

On the 16 tasks we studied, Flamingo beats all previous few-shot learning approaches when given as few as four examples per task. In several cases, the same Flamingo model outperforms methods that are fine-tuned and optimised for each task independently and use multiple orders of magnitude more task-specific data. This should allow non-expert people to quickly and easily use accurate visual language models on new tasks at hand.

![A bar chart showing Flamingo 32-shot performance relative to state-of-the-art (SOTA) across 16 tasks, with three diagrams on the right illustrating input-output examples for the HatefulMemes, VizWiz, and VATEX tasks.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/626a705661073c5f801de094_Fig_02.svg)

Figure 2. **Left:** Few-shot performance of the Flamingo across 16 different multimodal tasks against task specific state-of-the-art performance. **Right:** Examples of expected inputs and outputs for three of our 16 benchmarks.

In practice, Flamingo fuses large language models with powerful visual representations – each separately pre-trained and frozen – by adding novel architectural components in between. Then it is trained on a mixture of complementary large-scale multimodal data coming only from the web, without using any data annotated for machine learning purposes. Following this method, we start from [Chinchilla](https://deepmind.google/blog/an-empirical-analysis-of-compute-optimal-large-language-model-training/), our recently introduced compute-optimal 70B parameter language model, to train our final Flamingo model, an 80B parameter VLM. After this training is done, Flamingo can be directly adapted to vision tasks via simple few-shot learning without any additional task-specific tuning.

We also tested the model’s qualitative capabilities beyond our current benchmarks. As part of this process, we compared our model's performance when captioning images related to gender and skin colour, and ran our model's generated captions through Google's Perspective API, which evaluates toxicity of text. While the initial results are positive, more research towards evaluating ethical risks in multimodal systems is crucial and we urge people to evaluate and consider these issues carefully before thinking of deploying such systems in the real world.

Multimodal capabilities are essential for important AI applications, such as [aiding the visually impaired](https://vizwiz.org/tasks-and-datasets/vqa/) with everyday visual challenges or [improving the identification of hateful content](https://ai.facebook.com/blog/hateful-memes-challenge-and-data-set/) on the web. Flamingo makes it possible to efficiently adapt to these examples and other tasks on-the-fly without modifying the model. Interestingly, the model demonstrates out-of-the-box multimodal dialogue capabilities, as seen here.

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

Figure 3a - Flamingo can engage in multimodal dialogue out of the box, seen here discussing an unlikely "soup monster" image generated by OpenAI's DALL·E 2

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

Figure 3b - Passing and identifying the famous Stroop test.

Flamingo is an effective and efficient general-purpose family of models that can be applied to image and video understanding tasks with minimal task-specific examples. Models like Flamingo hold great promise to benefit society in practical ways and we’re continuing to improve their flexibility and capabilities so they can be safely deployed for everyone's benefit. Flamingo’s abilities pave the way towards rich interactions with learned visual language models that can enable better interpretability and exciting new applications, like a visual assistant which helps people in everyday life – and we’re delighted by the results so far.

**Notes**

This project was enabled by the contributions of the entire Flamingo team: Iain Barr, Yana Hasson, Karel Lenc, Arthur Mensch, Katie Millican, Malcolm Reynolds, Roman Ring, Eliza Rutherford, Serkan Cabi, Tengda Han, Zhitao Gong, Sina Samangooei, Marianne Monteiro, Jacob Menick, Sebastian Borgeaud, Andrew Brock, Aida Nematzadeh, Sahand Sharifzadeh, Mikolaj Binkowski, Ricardo Barreira, Oriol Vinyals, Andrew Zisserman, and Karen Simonyan. We would also like to thank the blog post contributors: Aliya Ahmad, Dominic Barlow, Arielle Bier, Matt Botvinick, Jordan Hoffmann, Max Barnett, Gaby Pearl, and Emma Yousif.
