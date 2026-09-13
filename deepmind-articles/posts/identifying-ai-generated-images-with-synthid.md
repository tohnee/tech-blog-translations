---
title: "Identifying AI-generated images with SynthID"
source: https://deepmind.google/blog/identifying-ai-generated-images-with-synthid/
site: deepmind
date: 2023-08-29
authors: Sven Gowal, Pushmeet Kohli
crawled: 2026-09-13
---

New tool helps watermark and identify synthetic images created by Imagen

AI-generated images are becoming more popular every day. But how can we better identify them, especially when they look so realistic?

Today, in partnership with [Google Cloud](https://cloud.google.com/blog/products/ai-machine-learning/vertex-ai-next-2023-announcements), we’re launching a beta version of [SynthID](https://deepmind.google/blog/in-conversation-with-ai-building-better-language-models/), a tool for watermarking and identifying AI-generated images. This technology embeds a digital watermark directly into the pixels of an image, making it imperceptible to the human eye, but detectable for identification.

SynthID is being released to a limited number of [Vertex AI](https://cloud.google.com/vertex-ai) customers using [Imagen](https://cloud.google.com/vertex-ai/docs/generative-ai/image/overview), one of our latest text-to-image models that uses input text to create photorealistic images.

![](https://lh3.googleusercontent.com/WeBR_JIbLo0Sd1tKfJkPTW9EzO44KJHqsVfPtH09b3W1qWRyEjrV7iLXkqRCjTE8z0X_jC8vOL2KB-ux2AjWe2aLfBmEb8lYaX6BQSkFLDsaimrFUdo=w1440-h810-n-nu)

Generative AI technologies are rapidly evolving, and computer generated imagery, also known as ‘synthetic imagery’, is becoming harder to distinguish from those that have not been created by an AI system.

While generative AI can unlock huge creative potential, it also presents new risks, like enabling creators to spread false information — both intentionally or unintentionally. Being able to identify AI-generated content is critical to empowering people with knowledge of when they’re interacting with generated media, and for helping prevent the spread of misinformation.

We’re committed to connecting people with high-quality information, and upholding trust between creators and users across society. Part of this responsibility is giving users more advanced tools for identifying AI-generated images so their images — and even some edited versions — can be identified at a later date.

![A gif rotating four different AI-generated images. The images are split by a vertical line down the middle. The left-hand side shows the watermarked version, the right side is the non-watermarked version. There's no obvious difference between the two. The four images show: an illustrated bear walking past a cabin, a photo-realistic cow standing on a grassy hill with a mountain behind it, a close-up black-and-white photograph of an armadillo, and an illustrated flamingo drinking from a lake.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/64e8abbb424b8a7e3b88b707_64e7629196215db21326c003_synthid_watermark_lo.gif)

SynthID generates an imperceptible digital watermark for AI-generated images.

Google Cloud is the first cloud provider to offer a tool for creating AI-generated images responsibly and identifying them with confidence. This technology is grounded in our approach to developing and deploying responsible AI, and was developed by Google DeepMind and refined in partnership with Google Research.

SynthID isn’t foolproof against extreme image manipulations, but it does provide a promising technical approach for empowering people and organisations to work with AI-generated content responsibly. This tool could also evolve alongside other AI models and modalities beyond imagery such as audio, video, and text.

## New type of watermark for AI images

Watermarks are designs that can be layered on images to identify them. From physical imprints on paper to translucent text and symbols seen on digital photos today, they’ve evolved throughout history.

Traditional watermarks aren’t sufficient for identifying AI-generated images because they’re often applied like a stamp on an image and can easily be edited out. For example, discrete watermarks found in the corner of an image can be cropped out with basic editing techniques.

Finding the right balance between imperceptibility and robustness to image manipulations is difficult. Highly visible watermarks, often added as a layer with a name or logo across the top of an image, also present aesthetic challenges for creative or commercial purposes. Likewise, some previously developed imperceptible watermarks can be lost through simple editing techniques like resizing.

![An eight-panel grid showing different modified versions of a purple butterfly image, demonstrating variations like blur, grayscale, blue tint, rotation, color filters, noise, and brightness adjustments.](https://lh3.googleusercontent.com/6J5kRoU6TtjW7_CWcaVJj_lwK9TsnnSB1K2_okt11aKPmQl9iCGituySYuGvvUVbqdt_3jy03r1L1s9FxKy98WW3o89vGQKU9YRbhTTZFgLxkuPp=w1440)

The watermark is detectable even after modifications like adding filters, changing colours and brightness.

We designed SynthID so it doesn't compromise image quality, and allows the watermark to remain detectable, even after modifications like adding filters, changing colours, and saving with various lossy compression schemes — most commonly used for JPEGs.

SynthID uses two deep learning models — for watermarking and identifying — that have been trained together on a diverse set of images. The combined model is optimised on a range of objectives, including correctly identifying watermarked content and improving imperceptibility by visually aligning the watermark to the original content.

## Robust and scalable approach

SynthID allows Vertex AI customers to create AI-generated images responsibly and to identify them with confidence. While this technology isn’t perfect, our internal testing shows that it’s accurate against many common image manipulations.

SynthID's combined approach:

- **Watermarking**: SynthID can add an imperceptible watermark to synthetic images produced by Imagen.
- **Identification**: By scanning an image for its digital watermark, SynthID can assess the likelihood of an image being created by Imagen.

![A table of text showing the symbols to indicate identification confidence levels. A green tick saying "Digital watermark detected" means that the image is likely generated by Imagen. A grey cross saying "Digital watermark not detected" means that the image is unlikely to be generated by Imagen. A yellow triangle containing an exclamation mark saying "Digital watermark possibly detected" means this image could be generated, treat with caution.](https://lh3.googleusercontent.com/RcNmIRkeMo3OZBjK_X1Htx2KspARIV86qcwKkArLdXgZvnTiy0SQugW8loRb--PbGoMO-yhSxcOZlo-qRiYx2SSlVh4bXr2iG6LRpvLnGh37LfNouOk=w1440)

SynthID can help assess how likely it is that an image was created by Imagen.

This tool provides three confidence levels for interpreting the results of watermark identification. If a digital watermark is detected, part of the image is likely generated by Imagen.

SynthID contributes to the broad suite of approaches for identifying digital content. One of the most widely used methods of identifying content is through metadata, which provides information such as who created it and when. This information is stored with the image file. Digital signatures added to metadata can then show if an image has been changed.

When the metadata information is intact, users can easily identify an image. However, metadata can be manually removed or even lost when files are edited. Since SynthID’s watermark is embedded in the pixels of an image, it’s compatible with other image identification approaches that are based on metadata, and remains detectable even when metadata is lost.

## What’s next?

To build AI-generated content responsibly, [we’re committed to developing safe, secure, and trustworthy approaches](https://www.whitehouse.gov/wp-content/uploads/2023/07/Ensuring-Safe-Secure-and-Trustworthy-AI.pdf) at every step of the way — from image generation and identification to media literacy and information security.

These approaches need to be robust and adaptable as generative models advance and expand to other mediums. We hope our SynthID technology can work together with a broad range of solutions for creators and users across society, and we’re continuing to evolve SynthID by gathering feedback from users, enhancing its capabilities, and exploring new features.

SynthID could be expanded for use across other AI models and we’re excited about the potential of integrating it into more Google products and making it available to third parties in the near future — empowering people and organisations to responsibly work with AI-generated content.

Note: The model used for producing synthetic images in this blog may be different from the model used on Imagen and Vertex AI.

[Read the Google Cloud announcement](https://cloud.google.com/blog/products/ai-machine-learning/vertex-ai-next-2023-announcements)

**Acknowledgements**

This project was led by Sven Gowal and Pushmeet Kohli, with key research and engineering contributions from (listed alphabetically): Rudy Bunel, Jamie Hayes, Sylvestre-Alvise Rebuffi, Florian Stimberg, David Stutz, and Meghana Thotakuri.

Thanks to Nidhi Vyas and Zahra Ahmed for driving product delivery; Chris Gamble for helping initiate the project; Ian Goodfellow, Chris Bregler and Oriol Vinyals for their advice. Other contributors include Paul Bernard, Miklos Horvath, Simon Rosen, Olivia Wiles, and Jessica Yung. Thanks also to many others who contributed across Google DeepMind and Google, including our partners at Google Research and Google Cloud.

![AI-generated image of a metallic butterfly resting on a leaf](https://lh3.googleusercontent.com/ZS-zI46bM9R9lgYgMJfofqMF4KsacJmxHaAywxl3aKlzUOw4kbdMpaHwk4EiCPbchTLF05ShML4DEVFLT-9ev3dTBTK0EbyXncnpJOzQQ-FCZQ2LcA=w1440)

Watermarked image of a metallic butterfly with prismatic patterns on its wings
