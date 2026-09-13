---
title: "Google DeepMind at NeurIPS 2023"
source: https://deepmind.google/blog/google-deepmind-at-neurips-2023/
site: deepmind
date: 2023-12-08
authors: 
crawled: 2026-09-13
---

Towards more multimodal, robust, and general AI systems

Next week marks the start of the 37th annual conference on Neural Information Processing Systems (NeurIPS),the largest artificial intelligence (AI) conference in the world. [NeurIPS 2023](https://nips.cc/) will be taking place December 10-16 in New Orleans, USA.

Teams from across Google DeepMind are presenting more than 180 papers at the main conference and workshops.

We’ll be showcasing demos of our cutting edge AI models for [global weather forecasting](https://deepmind.google/discover/blog/graphcast-ai-model-for-faster-and-more-accurate-global-weather-forecasting/), [materials discovery](https://deepmind.google/discover/blog/millions-of-new-materials-discovered-with-deep-learning), and [watermarking AI-generated content](https://deepmind.google/discover/blog/identifying-ai-generated-images-with-synthid/). There will also be an opportunity to hear from the team behind [Gemini, our largest and most capable AI mode](https://deepmind.google/technologies/gemini/#introduction)l.

Here’s a look at some of our research highlights:

[Google DeepMind at NeurIPS 2023 schedule](https://deepmind.events/events/neurips-2023/resources)[Google at NeurIPS 2023 blog](https://blog.research.google/2023/12/google-at-neurips-2023.html)

## Multimodality: language, video, action

![A grid of photos of actions: light switches, robotic arms cleaning and blocks on a table.](https://lh3.googleusercontent.com/HYY6sjOk71mM7Qhh8EVzlVDdnsSzPdkCeUD0wzEE9KYC68UN9qL50izYPqdjMEEolE4ETIBDTLYn55AE9h-p_YMi6bh0d45fZ7GLBX-QyFGbSD6z=w1440)

UniSim is a universal simulator of real-world interactions.

Generative AI models can create paintings, compose music, and write stories. But however capable these models may be in one medium, most struggle to transfer those skills to another. We delve into how generative abilities could help to learn across modalities. In a spotlight presentation, we show that [diffusion models can be used to classify images](https://openreview.net/pdf?id=fxNQJVMwK2) with no additional training required. Diffusion models like Imagen classify images in a more human-like way than other models, relying on shapes rather than textures. What’s more, we show how just [predicting captions from images can improve computer-vision learning](https://openreview.net/pdf?id=A7feCufBhL). Our approach surpassed current methods on vision and language tasks, and showed more potential to scale.

More multimodal models could give way to more useful digital and robot assistants to help people in their everyday lives. In a spotlight poster, we[create agents that could interact with the digital world like humans do](https://openreview.net/pdf?id=3PjCt4kmRx) — through screenshots, and keyboard and mouse actions. Separately, we show that by [leveraging video generation, including subtitles and closed captioning, models can transfer knowledge](https://openreview.net/pdf?id=bo8q5MRcwy) by predicting video plans for real robot actions.

One of the next milestones could be to generate realistic experience in response to actions carried out by humans, robots, and other types of interactive agents. We’ll be showcasing a demo of [UniSim](https://universal-simulator.github.io/unisim/), our universal simulator of real-world interactions. This type of technology could have applications across industries from video games and film, to training agents for the real world.

## Building safe and understandable AI

![Colorful blocks with a blanket to catch them below.](https://lh3.googleusercontent.com/CQHfz0ozRHIIEp-2Bkyl4naTv1wZX5CISfedfMoE5I7QGsrLNH_4QC78bT75gqfwQnF363E_IaHf8GY1_u51iOpBnt8vhhMVbNUOYkhe9tFwtd26IA=w1440)

An artist’s illustration of artificial intelligence (AI). This image depicts AI safety research. It was created by artist Khyati Trehan as part of the Visualising AI project launched by Google DeepMind.

When developing and deploying large models, privacy needs to be embedded at every step of the way.

In a paper recognized with the [NeurIPS best paper award](https://blog.neurips.cc/2023/12/11/announcing-the-neurips-2023-paper-awards/), our researchers demonstrate how to evaluate privacy-preserving [training with a technique that is efficient](https://openreview.net/pdf?id=q15zG9CHi8) enough for real-world use. For training, our teams are studying how to measure if [language models are memorizing data](https://openreview.net/pdf?id=67o9UQgTD0) – in order to protect private and sensitive material. In another oral presentation, our scientists investigate the [limitations of training through “student” and “teacher” models](https://openreview.net/pdf?id=a2Yg9Za6Rb) that have different levels of access and vulnerability if attacked.

Large Language Models can generate impressive answers, but are prone to “hallucinations”, text that seems correct but is made up. Our researchers raise the question of whether a method to find a fact stored location (localization) can enable editing the fact. Surprisingly, they found that[localization of a fact and editing the location does not edit the fact](https://openreview.net/pdf?id=EldbUlZtbd), hinting at the complexity of understanding and controlling stored information in LLMs. With [Tracr, we propose a novel way of evaluating interpretability](https://openreview.net/pdf?id=tbbId8u7nP) methods by translating human-readable programs into transformer models. We’ve [open sourced a version of Tracr](https://github.com/google-deepmind/tracr) to help serve as a ground-truth for evaluating interpretability methods.

## Emergent abilities

![An abstract, multi-level architectural illustration featuring stairs, columns, and platforms adorned with green moss and hanging vines, representing the conceptual structure of emergent abilities in AI.](https://lh3.googleusercontent.com/g2HYzBSuD-1M8R6_8ZCfXm_shrnh8yExnxBplKVmykYdmYTF_C5bPXlzBGOx0MK_qZ5SQWiVNA4cGA9SAdYiMa0th8civEWSv-8TPkxfl0nk6WcX3w=w1440)

An artist’s illustration of artificial intelligence (AI). This image imagines Artificial General Intelligence (AGI). It was created by Novoto Studio as part of the Visualising AI project launched by Google DeepMind.

As large models become more capable, our research is pushing the limits of new abilities to develop more general AI systems.

While language models are used for general tasks, they lack the necessary exploratory and contextual understanding to solve more complex problems. We introduce the [Tree of Thoughts, a new framework for language model inference](https://openreview.net/pdf?id=5Xc1ecxO1h) to help models explore and reason over a wide range of possible solutions. By organizing the reasoning and planning as a tree instead of the commonly used flat chain-of-thoughts, we demonstrate that a language model is able to solve complex tasks like “game 24” much more accurately.

To help people solve problems and find what they’re looking for, AI models need to process billions of unique values efficiently. With [Feature Multiplexing, one single representation space is used for many different features](https://openreview.net/pdf?id=hJzEoQHfCe), allowing large embedding models (LEMs) to scale to products for billions of users.

Finally, with DoReMi we show how using AI to automate the [mixture of training data types can significantly speed up language model training](https://openreview.net/pdf?id=lXuByUeHhd) and improve performance on new and unseen tasks.

## Fostering a global AI community

We’re proud to sponsor NeurIPS, and support workshops led by [LatinX in AI](https://www.latinxinai.org/), [QueerInAI](https://www.queerinai.com/), and [Women In ML](https://wimlworkshop.org/), helping foster research collaborations and developing a diverse AI and machine learning community. This year, NeurIPS will have a creative track featuring our Visualising AI project, which commissions artists to create more diverse and accessible representations of AI.

If you’re attending NeurIPS, come by our booth to learn more about our cutting-edge research and meet our teams hosting workshops and presenting across the conference.

**Learn more**

[Google DeepMind at NeurIPS 2023 schedule](https://deepmind.events/events/neurips-2023/resources)[Google at NeurIPS 2023 blog](https://blog.research.google/2023/12/google-at-neurips-2023.html)
