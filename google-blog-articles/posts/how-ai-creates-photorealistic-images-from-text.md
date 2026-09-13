---
title: "How AI creates photorealistic images from text"
source: https://blog.google/innovation-and-ai/technology/research/how-ai-creates-photorealistic-images-from-text/
site: google-blog
date: 2022-06-22
authors: Yonghui Wu
crawled: 2026-09-13
---

![Pictures of puppy in a nest emerging from a cracked egg. Photos overlooking a steampunk city with airships. Picture of two robots having a romantic evening at the movies.](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Final_Hero_Image_Imagen_Parti.width-1200.format-webp.webp)

Have you ever seen a puppy in a nest emerging from a cracked egg? What about a photo that’s overlooking a steampunk city with airships? Or a picture of two robots having a romantic evening at the movies? These might sound far-fetched, but a novel type of machine learning technology called text-to-image generation makes them possible. These models can generate high-quality, photorealistic images from a simple text prompt.

Within Google Research, our scientists and engineers have been exploring text-to-image generation using a variety of AI techniques. After a lot of testing we recently announced two new text-to-image models — [Imagen](https://imagen.research.google/) and [Parti](https://parti.research.google/). Both have the ability to generate photorealistic images but use different approaches. We want to share a little more about how these models work and their potential.

### How text-to-image models work

With text-to-image models, people provide a text description and the models produce images matching the description as closely as possible. This can be something as simple as “an apple” or “a cat sitting on a couch” to more complex details, interactions and descriptive indicators like “a cute sloth holding a small treasure chest. A bright golden glow is coming from the chest.”

![A picture of a cute sloth holding a small treasure chest. A bright golden glow is coming from the chest](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Sloth_Image.width-1200.format-webp.webp)

In the past few years, ML models have been trained on large image datasets with corresponding textual descriptions, resulting in higher quality images and a broader range of descriptions. This has sparked major breakthroughs in this area, including Open AI’s [DALL-E 2](https://openai.com/dall-e-2/).

### How Imagen and Parti work

Imagen and Parti build on previous models. Transformer models are able to process words in relationship to one another in a sentence. They are foundational to how we represent text in our text-to-image models. Both models also use a new [technique](https://openreview.net/forum?id=qw8AKxfYbI) that helps generate images that more closely match the text description. While Imagen and Parti use similar technology, they pursue different, but complementary strategies.

Imagen is a Diffusion model, which learns to convert a pattern of random dots to images. These images first start as low resolution and then progressively increase in resolution. Recently, Diffusion models have seen success in both [image](https://iterative-refinement.github.io/palette/) and [audio](https://wavegrad.github.io/) tasks like enhancing image resolution, recoloring black and white photos, editing regions of an image, uncropping images, and text-to-speech synthesis.

Parti’s approach first [converts](https://ai.googleblog.com/2022/05/vector-quantized-image-modeling-with.html) a collection of images into a sequence of code entries, similar to puzzle pieces. A given text prompt is then [translated](https://ai.googleblog.com/2017/08/transformer-novel-neural-network.html) into these code entries and a new image is created. This approach takes advantage of existing research and infrastructure for large language models such as [PaLM](https://ai.googleblog.com/2022/04/pathways-language-model-palm-scaling-to.html) and is critical for handling long, complex text prompts and producing high-quality images.

These models have many limitations. For example, neither can reliably produce specific counts of objects (e.g. “ten apples”), nor place them correctly based on specific spatial descriptions (e.g. “a red sphere to the left of a blue block with a yellow triangle on it”). Also, as prompts become more complex, the models begin to falter, either missing details or introducing details that were not provided in the prompt. These behaviors are a result of several shortcomings, including lack of explicit training material, limited data representation, and lack of 3D awareness. We hope to address these gaps through broader representations and more effective integration into the text-to-image generation process.

### Taking a responsible approach to Imagen and Parti

Text-to-image models are exciting tools for inspiration and creativity. They also come with risks related to disinformation, bias and safety. We’re having discussions around Responsible AI practices and the necessary steps to safely pursue this technology. As an initial step, we’re using easily identifiable watermarks to ensure people can always recognize an Imagen- or Parti-generated image. We’re also conducting experiments to better understand biases of the models, like how they represent people and cultures, while exploring possible mitigations. The [Imagen](https://arxiv.org/pdf/2205.11487.pdf) and [Parti](https://parti.research.google/paper) papers provide extensive discussion of these issues.

### What’s next for text-to-image models at Google

We will push on new ideas that combine the best of both models, and expand to related tasks such as adding the ability to interactively generate and edit images through text. We’re also continuing to conduct in-depth comparisons and evaluations to align with our [Responsible AI Principles](https://ai.google/principles/). Our goal is to bring user experiences based on these models to the world in a safe, responsible way that will inspire creativity.
