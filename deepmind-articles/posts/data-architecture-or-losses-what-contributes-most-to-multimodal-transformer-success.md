---
title: "Data, Architecture, or Losses: What Contributes Most to Multimodal Transformer Success?"
source: https://deepmind.google/blog/data-architecture-or-losses-what-contributes-most-to-multimodal-transformer-success/
site: deepmind
date: 2021-02-02
authors: Aida Nematzadeh, Lisa Anne Hendricks, Jean-Baptiste Alayrac, Rosalia Schneider, John Mellor
crawled: 2026-09-13
---

The ability to ground language to vision is a fundamental aspect of real-world AI systems; it is useful across a range of tasks (e.g., visual question answering) and applications (e.g., generating descriptions for visually impaired). Multimodal models (pre-trained on image-language pairs) aim to address this grounding problem. A recent family of models, multimodal transformers (e.g., Lu et al., 2019; Chen et al., 2020; Tan and Bansal, 2019; Li et al., 2020), have achieved state-of-the-art performance in a range of multimodal benchmarks, suggesting that the joint-encoder transformer architecture is better suited for capturing the alignment between image-language pairs than previous approaches (such as dual encoders).

![Diagram comparing Dual Encoders, which use separate image and language encoders with an image-language matching loss, and Joint Encoders (Multimodal Transformers), which process both image patches and text tokens within a single unified transformer using image modelling, language modelling, and matching losses.](https://lh3.googleusercontent.com/gEZUcDKk0hxz89Ks7KY2-puji53klG42-XFvkY4E7hpyvO0NGmZmcS3buCcSl0Creo1RrNoTw9BaGXtTvCZU2Zh9_ggiJv7nAZb1xKAuCPtMFeph=w1440)

In particular, compared to the dual-encoder architecture where there is no cross-talk between the modalities, multimodal transformers (joint encoders) are more sample efficient. In the plot below, we see that, when tested on zero-shot image retrieval, an existing multimodal transformer (UNITER) performs similar to a large-scale dual encoder (CLIP) which is trained on 100 times more data.

![A scatter plot comparing zero-shot image retrieval performance (R@1) against the number of pretraining images. It shows that given the same training data size, a Multimodal Transformer (MMT) outperforms a Dual Encoder (BOW-DE). Meanwhile, the Multimodal Transformer (UNITER) achieves the same performance as a Dual Encoder (CLIP) while requiring significantly fewer training images.](https://lh3.googleusercontent.com/XoD7vsvUuc1uG8yBOln2ITw0xAjYAwwA9XeAb9uJI1xS3syVuQl7n0JSGdBb6kKvPtxCKK5P7qao-mraqHDfiePUByMEe1kuDNSgyEFUFfyvGta-rw=w1440)

BOW-DE: Miech & Alayrac et al. Arxiv 2021, MMT: Hendricks et al. TACL 2021, UNITER: Chen et al. ECCV 2020, CLIP: Radford et al. Arxiv 2021, ALIGN: Jia et al. Arxiv 2021

In this work, we examine what aspects of multimodal transformers – attention, losses, and pretraining data – are important in their success at multimodal pretraining. We find that Multimodal attention, where both language and image transformers attend to each other, is crucial for these models’ success. Models with other types of attention (even with more depth or parameters) fail to achieve comparable results to shallower and smaller models with multimodal attention. Moreover, comparable results can be achieved without the image (masked region modelling) loss originally proposed for multimodal transformers. This suggests that our current models are not tapping into the useful signal in the image modality, presumably because of the image loss formulation.

We also study different properties of multimodal datasets such as their size and the degree to which the language describes its corresponding image (noisiness). We find that a dataset’s size does not always predict multimodal transformers’ performance; its noise level and language similarity to the evaluation task are both important contributing factors. These suggest curating less noisy image–text datasets to be important despite the current trend of harvesting noisy datasets from the web.

Overall, our analysis shows that multimodal transformers are stronger than dual encoder architecture (given the same amount of pretraining data), mainly due to the cross-talk through multimodal attention. However, there are still many open problems when designing multimodal models, including better losses for the image modality and robustness to dataset noise.
