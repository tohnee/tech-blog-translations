---
title: "Google DeepMind at NeurIPS 2024"
source: https://deepmind.google/blog/google-deepmind-at-neurips-2024/
site: deepmind
date: 2024-12-05
authors: 
crawled: 2026-09-13
---

Advancing adaptive AI agents, empowering 3D scene creation, and innovating LLM training for a smarter, safer future

Next week, AI researchers worldwide will gather for the [38th Annual Conference on Neural Information Processing Systems](https://neurips.cc/) (NeurIPS), taking place December 10-15 in Vancouver,

Two papers led by Google DeepMind researchers will be recognized with [Test of Time](https://blog.neurips.cc/2024/11/27/announcing-the-neurips-2024-test-of-time-paper-awards/) awards for their “undeniable influence” on the field. Ilya Sutskever will present on [Sequence to Sequence Learning with Neural Networks](https://arxiv.org/abs/1409.3215) which was co-authored with Google DeepMind VP of Drastic Research, Oriol Vinyals, and Distinguished Scientist Quoc V. Le. Google DeepMind Scientists Ian Goodfellow and David Warde-Farley will present on [Generative Adversarial Nets](https://arxiv.org/abs/1406.2661).

We’ll also show how we translate our foundational research into real-world applications, with live demonstrations including [Gemma Scope](https://deepmind.google/discover/blog/gemma-scope-helping-the-safety-community-shed-light-on-the-inner-workings-of-language-models/), [AI for music generation](https://deepmind.google/discover/blog/new-generative-ai-tools-open-the-doors-of-music-creation/), [weather forecasting](https://deepmind.google/research/publications/24820/) and more.

Teams across Google DeepMind will present more than 100 new papers on topics ranging from AI agents and generative media to innovative learning approaches.

[Google Research at NeurIPS 2024 schedule](https://research.google/conferences-and-events/google-at-neurips-2024/)

## Building adaptive, smart, and safe AI Agents

LLM-based AI agents are showing promise in carrying out digital tasks via natural language commands. Yet their success depends on precise interaction with complex user interfaces, which requires extensive training data. With [AndroidControl](https://neurips.cc/virtual/2024/poster/97433), we share the most diverse control dataset to date, with over 15,000 human-collected demos across more than 800 apps. AI agents trained using this dataset showed significant performance gains which we hope helps advance research into more general AI agents.

For AI agents to generalize across tasks, they need to learn from each experience they encounter. We present a method for [in-context abstraction learning](https://neurips.cc/virtual/2024/poster/96600) that helps agents grasp key task patterns and relationships from imperfect demos and natural language feedback, enhancing their performance and adaptability.

![A first-person view of a person cooking at a stove, with various objects in the kitchen numbered for dataset demonstration.](https://lh3.googleusercontent.com/hYU1cKrYubfWtrnBJfHtPSCuvL0ivAGVV7f3ZbZM10v9tHrr-DUUhjzyZeGihb4-2aIaNlVtNeddEvRK2rz9WJtgR41FAGNTQkjlCcyXZSaP2dxYhQ=w1440)

A frame from a video demonstration of someone making a sauce, with individual elements identified and numbered. ICAL is able to extract the important aspects of the process

Developing agentic AI that works to fulfill users’ goals can help make the technology more useful, but alignment is critical when developing AI that acts on our behalf. To that end, we propose a theoretical method to [measure an AI system’s goal-directedness](https://neurips.cc/virtual/2024/poster/93645), and also show how a [model’s perception of its user can influence its safety filters](https://neurips.cc/virtual/2024/poster/94269). Together, these insights underscore the importance of robust safeguards to prevent unintended or unsafe behaviors, ensuring that AI agents’ actions remain aligned with safe, intended uses.

## Advancing 3D scene creation and simulation

As demand for high-quality 3D content grows across industries like gaming and visual effects, creating lifelike 3D scenes remains costly and time-intensive. Our recent work introduces novel 3D generation, simulation, and control approaches, streamlining content creation for faster, more flexible workflows.

Producing high-quality, realistic 3D assets and scenes often requires capturing and modeling thousands of 2D photos. We showcase [CAT3D](https://neurips.cc/virtual/2024/poster/95046), a system that can create 3D content in as little as a minute, from any number of images — even just one image, or a text prompt. CAT3D accomplishes this with a multi-view diffusion model that generates additional consistent 2D images from many different viewpoints, and uses those generated images as input for traditional 3D modelling techniques. Results surpass previous methods in both speed and quality.

![A diagram demonstrating the CAT3D system creating 3D content from various inputs: a text prompt of a robot cat (left), a single photo of a dog in a car (center), and three photos of a Lego bonsai tree from different angles (right). Blue arrows point down from these inputs to show the generated 3D models and multiple viewpoint renders.](https://lh3.googleusercontent.com/GY3_w3clElUUoznz1JSljAUCVXe-sx0XkAPh9vBrmnmDQqd74MZpsGDv1Au45MOUmvoJjeSGpuYdnrFDtQVUTCBgPQVlUaQPozUNZRF01AXFtsgggg=w1440)

CAT3D enables 3D scene creation from any number of generated or real images.

Left to right: Text-to-image-to-3D, a real photo to 3D, several photos to 3D.

Simulating scenes with many rigid objects, like a cluttered tabletop or tumbling Lego bricks, also remains computationally intensive. To overcome this roadblock, we present [a new technique called SDF-Sim](https://neurips.cc/virtual/2024/poster/95252) that represents object shapes in a scalable way, speeding up collision detection and enabling efficient simulation of large, complex scenes.

![A complex simulation of hundreds of shoes falling and colliding, accurately modelled using SDF-Sim](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/pile_of_shoes.gif)

A complex simulation of shoes falling and colliding, accurately modelled using SDF-Sim

AI image generators based on diffusion models struggle to control the 3D position and orientation of multiple objects. Our solution, [Neural Assets](https://neural-assets.github.io/), introduces object-specific representations that capture both appearance and 3D pose, learned through training on dynamic video data. Neural Assets enables users to move, rotate, or swap objects across scenes—a useful tool for animation, gaming, and virtual reality.

![A series of images demonstrating the Neural Assets technique across six columns: "Original Image", "Translate Obj.", "Rotate Obj.", "Rescale Obj.", "Replace Obj.", and "Replace Bg." The top row applies these edits to a purple shoe outlined in a green 3D bounding box, while the bottom row applies them to cars on a city street.](https://lh3.googleusercontent.com/SdRwaLJ5jFNJAir4vEjMouPGAwPFi_1rBRdluqmSXxKoEh4ZsuFf3ciZqv8ak_9uJCReH0_MrgLCTxqF2fi6I9PNNLhzXheYXyqc_eXQm72CrKub=w1440)

Given a source image and object 3D bounding boxes, we can translate, rotate, and rescale the object, or transfer objects or backgrounds between images

## Improving how LLMs learn and respond

We’re also advancing how LLMs train, learn, and respond to users, improving performance and efficiency on several fronts.

With larger context windows, LLMs can now learn from potentially thousands of examples at once — known as many-shot in-context learning (ICL). This process boosts model performance on tasks like math, translation, and reasoning, but often requires high-quality, human-generated data. To make training more cost-effective, we explore [methods to adapt many-shot ICL](https://neurips.cc/virtual/2024/poster/96277) that reduce reliance on manually curated data. There is so much data available for training language models, the main constraint for teams building them becomes the available compute. We [address an important question](https://arxiv.org/pdf/2405.15074): with a fixed compute budget, how do you choose the right model size to achieve the best results?

Another innovative approach, which we call [Time-Reversed Language Models](https://neurips.cc/virtual/2024/poster/93684) (TRLM), explores pretraining and finetuning an LLM to work in reverse. When given traditional LLM responses as input, a TRLM generates queries that might have produced those responses. When paired with a traditional LLM, this method not only helps ensure responses follow user instructions better, but also improves the generation of citations for summarized text, and enhances safety filters against harmful content.

Curating high-quality data is vital for training large AI models, but manual curation is difficult at scale. To address this, our [Joint Example Selection](https://neurips.cc/virtual/2024/poster/97437) (JEST) algorithm optimizes training by identifying the most learnable data within larger batches, enabling up to 13× fewer training rounds and 10× less computation, outperforming state-of-the-art multimodal pretraining baselines.

Planning tasks are another challenge for AI, particularly in stochastic environments, where outcomes are influenced by randomness or uncertainty. Researchers use various inference types for planning, but there’s no consistent approach. We demonstrate that [planning itself can be viewed as a distinct type of probabilistic inference](https://neurips.cc/virtual/2024/poster/95030) and propose a framework for ranking different inference techniques based on their planning effectiveness.

## Bringing together the global AI community

We’re proud to be a Diamond Sponsor of the conference, and support [Women in Machine Learning](https://docs.google.com/document/d/1Yi_76ABz08xzF5On0h_vdob1wAl8LAAB4CvwfwJcjY8/edit?tab=t.0), [LatinX in AI](https://www.latinxinai.org/) and [Black in AI](https://www.blackinai.org/) in building communities around the world working in AI, machine learning and data science.

If you’re at NeurIPs this year, swing by the Google DeepMind and [Google Research](https://research.google/conferences-and-events/google-at-neurips-2024/) booths to explore cutting-edge research in demos, workshops and more throughout the conference.
