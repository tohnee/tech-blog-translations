---
title: "Tips for getting the best image generation and editing in the Gemini app"
source: https://blog.google/products-and-platforms/products/gemini/image-generation-prompting-tips/
site: gemini
date: 2025-08-26
authors: Naina Raisinghani
crawled: 2026-09-13
---

Earlier today, we launched a state-of-the-art image generation and editing model, available in the [Gemini app](http://gemini.google.com), [AI Studio](http://aistudio.google.com/) and [Vertex AI](https://cloud.google.com/blog/products/ai-machine-learning/gemini-2-5-flash-image-on-vertex-ai). This update introduces significant advancements in character consistency; precise, conversational editing; and the ability to combine photos into a completely new creation. To help you get the most out of this update, here are some tips for writing more effective prompts for image generation and editing in Gemini.

## Key capabilities of image generation in Gemini

Before you dive in, it’s helpful to familiarize yourself with what’s been improved in Gemini, so you can consider which use cases to try with it:

1. **Consistent character design.** Preserve a character or object's appearance across multiple generations and edits.
2. **Creative composition.** Blend disparate elements, subjects and styles from multiple concepts into a single, unified image.
3. **Local edits.** Make precise edits to specific parts of an image using simple language.
4. **Design and appearance adaptation.** Apply a style, texture or design from one concept to another.
5. **Logic and reasoning.** Use real-world understanding to generate complex scenes or predict the next step in a sequence.

## 6 elements of constructing effective prompts

You can get great results with Gemini from simple one or two-sentence inputs. However, to achieve the best results and unlock more nuanced creative control, consider including the following elements in your prompt:

- **Subject:** Who or what is in the image? Be specific. (e.g., *a stoic robot barista with glowing blue optics*; *a fluffy calico cat wearing a tiny wizard hat*).
- **Composition:** How is the shot framed? (e.g., *extreme close-up*, *wide shot*, *low angle shot*, *portrait*).
- **Action:** What is happening? (e.g., *brewing a cup of coffee*, *casting a magical spell*, *mid-stride running through a field*).
- **Location:** Where does the scene take place? (e.g., *a futuristic cafe on Mars*, *a cluttered alchemist's library*, *a sun-drenched meadow at golden hour*).
- **Style:** What is the overall aesthetic? (e.g., *3D animation*, *film noir*, *watercolor painting*, *photorealistic*, *1990s product photography*).
- **Editing Instructions:** For modifying an existing image, be direct and specific. (e.g., *change the man's tie to green*, *remove the car in the background*).

## Prompting examples: A showcase of creative techniques

Different prompting strategies can unlock everything from photorealistic edits to fantastical new worlds. Here are five techniques to try, each with a key example.

### 1. Preserve characters’ appearances.

Gemini can maintain the likeness of a person or character across different poses, lighting and environments, and even apply the same character to new styles and surfaces. Here’s an example of how one character can be used across multiple prompts in the same session:

- **Prompt 1:** A whimsical illustration of a tiny, glowing mushroom sprite. The sprite has a large, bioluminescent mushroom cap for a hat, wide, curious eyes, and a body made of woven vines.
- **Prompt 2 (in the same conversation):** Now, show the same sprite riding on the back of a friendly, moss-covered snail through a sunny meadow full of colorful wildflowers.

![A side-by-side fantasy illustration shows a small pixie-like creature with a mushroom cap hat. On the left, it floats in a dark, misty forest. On the right, it rides a smiling snail through a sunlit field of wildflowers.](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/pixie.width-1200.format-webp.webp)

By establishing a clearly defined character with specific details in the first prompt, you can use follow-up prompts to place that *same character* in entirely new contexts. Here, Gemini preserves key features of the character like facial features, distinctive appearance and clothing.

### 2. Make targeted transformations with precision.

With updated image editing capabilities, you can make quick, highly precise edits to your photos. This is perfect for everything from product mockups to perfecting personal pictures. Here’s an example:

- **Prompt 1:** A high-quality photo of a modern, minimalist living room with a grey sofa, a light wood coffee table, and a large potted plant.
- **Prompt 2 (editing):** Change the sofa's color to a deep navy blue.
- **Prompt 3 (editing):** Now, add a stack of three books to the coffee table.

![Three side-by-side images of a living room demonstrate different interior design choices. The first photo features a gray sofa, the second shows a dark blue sofa, and the third shows the same blue sofa with a stack of books on the coffee table. The images are a comparison.](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/livingroom.width-1200.format-webp.webp)

This showcases Gemini’s strength in local edits. By using direct, conversational commands, you can modify specific elements within the image without needing complex software or re-generating the entire scene.

### 3. Blend concepts with creative composition.

Try fusing two or more ideas into a single, striking image. Prompt Gemini to create two images, and then combine their subjects and environments in imaginative ways:

- **Prompt 1:** Generate a photorealistic picture of an astronaut in a helmet and full suit.
- **Prompt 2:** A picture of an overgrown basketball court in the rainforest.
- **Prompt 3 (upload both and combine):** Show the astronaut dunking a basketball in this court.

![A three-panel sequence shows an astronaut in a spacesuit on Mars, an abandoned basketball court in a lush jungle, and the astronaut dunking a ball on that same court.](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/astronaut.width-1200.format-webp.webp)

### 4. Adapt and apply new styles.

Completely change the mood and aesthetic of an image by applying a new style, color palette or texture, all while keeping the original subject intact.

- **Prompt 1:** A photorealistic image of a classic motorcycle parked on a city street.
- **Prompt 2 (editing):** Apply the style of an architectural drawing to this image.

![A side-by-side comparison of a detailed photograph of a parked motorcycle and a black-and-white line drawing of the same scene.](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/bike.width-1200.format-webp.webp)

With “style transfer,” Gemini understands the core subject (the motorcycle) and its form, then re-renders it entirely in the requested artistic style. This can be used for design inspiration, artistic exploration, and more.

### 5. Use logic and reasoning for complex generation.

Give Gemini a simple concept and let its reasoning capabilities build out the details. This is useful for creating content that requires an understanding of real-world relationships or processes.

- **Prompt 1:** Generate an image of a person standing holding a 3 tiered cake.
- **Prompt 2 (in the same session):** Generate an image showing what would happen if they tripped.

![A two-panel image shows a chef holding a pristine three-tiered cake, followed by a second image of the same cake falling to pieces while the chef looks on in shock.](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/chef.width-1200.format-webp.webp)

The model can use its logic and reasoning capabilities to predict what comes next. It understands the context and physics of the first image — a person carefully balancing a cake — and can then simulate the plausible consequences of an action like tripping, resulting in a dynamic and context-aware new image.

## A note on current limitations

As we continue to develop and fine-tune our models, there are still areas in need of improvement:

- **Stylization:** While powerful, the model’s stylization can sometimes be inconsistent or produce unexpected results.
- **Text rendering:** The model may occasionally misspell words or struggle with complex typography.
- **Character features:** While the model excels at character consistency, it may not always get it right. We're working to make this consistency even more reliable.
- **Setting and maintaining aspect ratios:** The model struggles with maintaining aspect ratios — while you can prompt for desired dimensions, the output may not always support your requests.

We’re actively working to improve these areas and appreciate your creativity as we build the next generation of image tools together.

 The creative possibilities are ripe for your picking — we can’t wait to see what you come up with!

*With special thanks to the Greenfield team of senior staff generative engineers for their creative contributions.*
