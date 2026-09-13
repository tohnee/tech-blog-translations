---
title: "Gemini Robotics brings AI into the physical world"
source: https://deepmind.google/blog/gemini-robotics-brings-ai-into-the-physical-world/
site: deepmind
date: 2025-03-12
authors: Carolina Parada
crawled: 2026-09-13
---

Introducing Gemini Robotics, our Gemini 2.0-based model designed for robotics

At Google DeepMind, we've been making progress in how our Gemini models solve complex problems through multimodal reasoning across text, images, audio and video. So far however, those abilities have been largely confined to the digital realm. In order for AI to be useful and helpful to people in the physical realm, they have to demonstrate “embodied” reasoning — the humanlike ability to comprehend and react to the world around us— as well as safely take action to get things done.

Today, we are introducing two new AI models, based on Gemini 2.0, which lay the foundation for a new generation of helpful robots.

The first is Gemini Robotics, an advanced vision-language-action (VLA) model that was built on Gemini 2.0 with the addition of physical actions as a new output modality for the purpose of directly controlling robots. The second is Gemini Robotics-ER, a Gemini model with advanced spatial understanding, enabling roboticists to run their own programs using Gemini’s embodied reasoning (ER) abilities.

Both of these models enable a variety of robots to perform a wider range of real-world tasks than ever before. As part of our efforts, we’re partnering with Apptronik to build the next generation of humanoid robots with Gemini 2.0. We’re also working with a selected number of trusted testers to guide the future of Gemini Robotics-ER.

We look forward to exploring our models’ capabilities and continuing to develop them on the path to real-world applications.

![](https://lh3.googleusercontent.com/rQvqvsZb5dMgbR9LFKeMlUcaOWY0NTEd2d8-d_xeO6A84MXiluORxTIxLkUZ98O_Tit52oew2lZgbaatVNGrU92gaSMCH1Q7nFuVd_f4LMtLYkgxFg=w1440-h810-n-nu)

A summary of our efforts

## Gemini Robotics: Our most advanced vision-language-action model

To be useful and helpful to people, AI models for robotics need three principal qualities: they have to be general, meaning they’re able to adapt to different situations; they have to be interactive, meaning they can understand and respond quickly to instructions or changes in their environment; and they have to be dexterous, meaning they can do the kinds of things people generally can do with their hands and fingers, like carefully manipulate objects.

While our previous work demonstrated progress in these areas, Gemini Robotics represents a substantial step in performance on all three axes, getting us closer to truly general purpose robots.

### Generality

Gemini Robotics leverages Gemini's world understanding to generalize to novel situations and solve a wide variety of tasks out of the box, including tasks it has never seen before in training. Gemini Robotics is also adept at dealing with new objects, diverse instructions, and new environments. In [our tech report](https://arxiv.org/abs/2503.20020), we show that on average, Gemini Robotics more than doubles performance on a comprehensive generalization benchmark compared to other state-of-the-art vision-language-action models.

![](https://lh3.googleusercontent.com/n2By6bFHJPOFYCYpbrfUzdO2K09uqSRcamcYJ1qu-lh2S8L8_oYermL5qjOsQBJwATKBkhLyLatmXNgHM4KRhCQeclf2mH-1eBu0t5M_UEXA84zNAw=w1440-h810-n-nu)

A demonstration of Gemini Robotics’s world understanding.

### Interactivity

To operate in our dynamic, physical world, robots must be able to seamlessly interact with people and their surrounding environment, and adapt to changes on the fly.

Because it’s built on a foundation of Gemini 2.0, Gemini Robotics is intuitively interactive. It taps into Gemini’s advanced language understanding capabilities and can understand and respond to commands phrased in everyday, conversational language and in different languages.

It can understand and respond to a much broader set of natural language instructions than our previous models, adapting its behavior to your input. It also continuously monitors its surroundings, detects changes to its environment or instructions, and adjusts its actions accordingly. This kind of control, or “steerability,” can better help people collaborate with robot assistants in a range of settings, from home to the workplace.

![](https://lh3.googleusercontent.com/-TSwa6jvlFbAbtIoHIfDfrXEpZACC-ROkVz0SKXm-Lc4uldO33XbQiWiX_SOwKegzbpZn4IkrFdmCjXZNw1oNtkeRHh4iiqOgfCPki99jJ9bgJ8k7w=w1440-h810-n-nu)

If an object slips from its grasp, or someone moves an item around, Gemini Robotics quickly replans and carries on — a crucial ability for robots in the real world, where surprises are the norm.

### Dexterity

The third key pillar for building a helpful robot is acting with [dexterity](https://deepmind.google/discover/blog/advances-in-robot-dexterity/?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=). Many everyday tasks that humans perform effortlessly require surprisingly fine motor skills and are still too difficult for robots. By contrast, Gemini Robotics can tackle extremely complex, multi-step tasks that require precise manipulation such as origami folding or packing a snack into a Ziploc bag.

![](https://lh3.googleusercontent.com/x8ppIjczt6xr0H5ficw-WvO7vEy8O9rn15SgsYNN0-BmZoXBIqn3Mhu8F-BacgdMKsjMbAXtv8p4b9bEhyXHpxflICKPSOc5CGBIvvXqefCV31bbrA=w1440-h810-n-nu)

Gemini Robotics displays advanced levels of dexterity

### Multiple embodiments

Finally, because robots come in all shapes and sizes, Gemini Robotics was also designed to easily adapt to different robot types. We trained the model primarily on data from the bi-arm robotic platform, [ALOHA 2](https://aloha-2.github.io/), but we also demonstrated that it could control a bi-arm platform, based on the Franka arms used in many academic labs. Gemini Robotics can even be specialized for more complex embodiments, such as the humanoid Apollo robot developed by Apptronik, with the goal of completing real world tasks.

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

Gemini Robotics works on different kinds of robots

## Enhancing Gemini’s world understanding

Alongside Gemini Robotics, we’re introducing an advanced vision-language model called Gemini Robotics-ER (short for ‘“embodied reasoning”). This model enhances Gemini’s understanding of the world in ways necessary for robotics, focusing especially on spatial reasoning, and allows roboticists to connect it with their existing low level controllers.

Gemini Robotics-ER improves Gemini 2.0’s existing abilities like pointing and 3D detection by a large margin. Combining spatial reasoning and Gemini’s coding abilities, Gemini Robotics-ER can instantiate entirely new capabilities on the fly. For example, when shown a coffee mug, the model can intuit an appropriate two-finger grasp for picking it up by the handle and a safe trajectory for approaching it.

Gemini Robotics-ER can perform all the steps necessary to control a robot right out of the box, including perception, state estimation, spatial understanding, planning and code generation. In such an end-to-end setting the model achieves a 2x-3x success rate compared to Gemini 2.0. And where code generation is not sufficient, Gemini Robotics-ER can even tap into the power of in-context learning, following the patterns of a handful of human demonstrations to provide a solution.

![Gemini Robotics-ER excels at embodied reasoning capabilities including detecting objects and pointing at object parts, finding corresponding points and detecting objects in 3D. This is a collage of visualizations showcasing these capabilities. Top left: 2D object detection, top right: pointing, bottom left: multi-view correspondence, bottom right: 3d object detection.](https://lh3.googleusercontent.com/DM4OXpSjM_WxgFGTlzilbnx9iyBvWCEKTh6xza2uZa4MGfwJ38kyoWYRM8HpyZGLZP_czByK-74rYs3h9osaHU-i5JBvzLDHAZd3fvvCH7phDvuB1Q=w1440)

Gemini Robotics-ER excels at embodied reasoning capabilities including detecting objects and pointing at object parts, finding corresponding points and detecting objects in 3D.

## Responsibly advancing AI and robotics

As we explore the continuing potential of AI and robotics, we’re taking a layered, [holistic](https://sites.google.com/corp/view/safe-robots?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=) approach to addressing safety in our research, from low-level motor control to high-level semantic understanding.

The physical safety of robots and the people around them is a longstanding, foundational concern in the science of robotics. That's why roboticists have classic safety measures such as avoiding collisions, limiting the magnitude of contact forces, and ensuring the dynamic stability of mobile robots. Gemini Robotics-ER can be interfaced with these ‘low-level’ safety-critical controllers, specific to each particular embodiment. Building on Gemini’s core safety features, we enable Gemini Robotics-ER models to understand whether or not a potential action is safe to perform in a given context, and to generate appropriate responses.

To advance robotics safety research across academia and industry, we are also releasing a new dataset to evaluate and improve semantic safety in embodied AI and robotics. In previous work, we showed how a [Robot Constitution](https://deepmind.google/discover/blog/shaping-the-future-of-advanced-robotics/?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=) inspired by Isaac Asimov’s Three Laws of Robotics could help prompt an LLM to select safer tasks for robots. We have since developed a framework to automatically generate data-driven constitutions - rules expressed directly in natural language – to steer a robot’s behavior. This framework would allow people to create, modify and apply constitutions to develop robots that are safer and more aligned with human values. Finally, the [new ASIMOV dataset](https://asimov-benchmark.github.io/) will help researchers to rigorously measure the safety implications of robotic actions in real-world scenarios.

To further assess the societal implications of our work, we collaborate with experts in our Responsible Development and Innovation team and as well as our Responsibility and Safety Council, an internal review group committed to ensure we develop AI applications responsibly. We also consult with external specialists on particular challenges and opportunities presented by embodied AI in robotics applications.

In addition to our partnership with Apptronik, our Gemini Robotics-ER model is also available to trusted testers including Agile Robots, Agility Robots, Boston Dynamics, and Enchanted Tools. We look forward to exploring our models’ capabilities and continuing to develop AI for the next generation of more helpful robots.

[Read our paper](https://arxiv.org/abs/2503.20020)

**Acknowledgements**

This work was developed by the Gemini Robotics team. For a full list of authors and acknowledgements please view [our technical report](https://arxiv.org/abs/2503.20020).
