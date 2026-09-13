---
title: "Perceiver AR: general-purpose, long-context autoregressive generation"
source: https://deepmind.google/blog/perceiver-ar-general-purpose-long-context-autoregressive-generation/
site: deepmind
date: 2022-07-16
authors: Curtis Hawthorne, Drew Jaegle, Cătălina Cangea, Sebastian Borgeaud, Charlie Nash, Mateusz Malinowski, Sander Dieleman, Oriol Vinyals, Matt Botvinick, Ian Simon, Hannah Sheahan, Neil Zeghidour, Jean-Baptiste Alayrac, João Carreira, Jesse Engel
crawled: 2026-09-13
---

Over the last few years, autoregressive Transformers have brought a steady stream of breakthroughs in generative modeling. These models generate each element of a sample – the pixels of an image, the characters of a text (typically in “token” chunks), the samples of an audio waveform, and so on – by predicting one element after the other. When predicting the next element, the model can look back at those that were created earlier.

However, each of a Transformer’s layers grows more expensive as more elements are used as input, and practitioners can only afford to train deep Transformers on sequences no more than about 2,048 elements in length. And so, most Transformer-based models ignore all elements beyond the most recent past (around 1,500 words or 1/6 of a small image) when making a prediction.

In contrast, our recently developed [Perceiver models](https://deepmind.google/blog/building-architectures-that-can-handle-the-worlds-data/) give excellent results on a variety of real-world tasks with up to around 100,000 elements. Perceivers use cross-attention to encode inputs into a latent space, decoupling the input’s compute requirements from model depth. Perceivers also spend a fixed cost, regardless of input size, at nearly every layer.

While latent-space encoding handles all elements in a single pass, autoregressive generation assumes processing happens one element at a time. To address this problem, Perceiver AR proposes a simple solution: align the latents one by one with the final elements of the input, and carefully mask the input so latents see only earlier elements.

![Diagram of the Perceiver AR architecture showing how a large set of inputs is mapped to a small number of latents using cross-attention with causal masking, followed by latent self-attention layers to predict target outputs.](https://lh3.googleusercontent.com/Ck0klfj8QgSgTWELIbAJuXqhVNaExAsUia6ysY8C9yj8-uV6nUaqwJ-YfwwWpoN47kP5huaYPqXToKS7pl7QgmB7Rp_7tZRFDsgNmciCDtN4AY7JMw=w1440)

Perceiver AR maps an input sequence (P e r c e i v e r A R) to a small latent space by cross-attention to produce one latent for each target token (3 latents shown, one for the targets A R <EOS>, for **E**nd **O**f **S**equence). These latents are then processed by a deep stack of self-attention layers. Perceiver AR can be trained for end-to-end autoregressive generation, all while making use of very long input sequences.

The result is an architecture (shown above) that attends to as much as 50x longer inputs as standard Transformers, while deploying as widely (and essentially as easily) as standard decoder-only Transformers.

![A scatter plot comparing training steps per second (y-axis) against context length (x-axis) for Perceiver AR (blue), Transformer-XL (orange), and standard Transformer (green). Perceiver AR scales to much longer context lengths (up to 65,536) while maintaining higher training speeds and deeper model layers (represented by circle size) compared to the other architectures.](https://lh3.googleusercontent.com/y8wMRp9d0-ADOts7ZXylO4Uzs83MNYBMPH3ZnnvdjnG5pvFOQc6C25d_gerF7iBx2rLPMzWEp1Tw5BRavbAYkcGV5rMj2DMAggIdXk44SkdlbaQuSg=w1440)

As context length or model size increases, the amount of compute needed to train a model grows. We can quantify the compute budget for different models by measuring their speed on real hardware (steps per second on TPUv3), as the input context length and model size increase. Unlike other generative models like Transformer or Transformer-XL, Perceiver AR decouples input context length from model depth, allowing us to easily deploy the deep models needed to model long sequences on current-generation TPUs or GPUs.

Perceiver AR scales considerably better with size than both standard Transformers and Transformer-XL models at a range of sequence lengths in real terms. This property allows us to build very effective long-context models. For example, we find that a 60-layer Perceiver AR with context length 8192 outperforms a 42-layer Transformer-XL on a book-length generation task, while running faster in real wall-clock terms.

On standard, long-context image (ImageNet 64x64), language (PG-19), and music (MAESTRO) generation benchmarks, Perceiver AR produces state-of-the-art results. Increasing input context by decoupling input size from compute budget leads to several intriguing results:

- Compute budget can be adapted at eval time, allowing us to spend less and smoothly degrade quality or to spend more for improved generation.
- A larger context allows Perceiver AR to outperform Transformer-XL, even when spending the same on compute. We find that greater context leads to improved model performance even at affordable scale (~1B parameters).
- Perceiver AR’s sample quality exhibits much less sensitivity to the order in which it generates elements. This makes Perceiver AR easy to apply to settings that don’t have a natural left-to-right ordering, such as data like images, with structure that spans more than one dimension.

Using a dataset of piano music, we trained Perceiver AR to generate new pieces of music from scratch. Because each new note is predicted based on the full sequence of notes that came before, Perceiver AR is able to produce pieces with a high level of melodic, harmonic, and rhythmic coherence:

Learn more about using Perceiver AR:

- Download the JAX code for training Perceiver AR [on Github](https://github.com/google-research/perceiver-ar)
- Read our paper on [arXiv](https://arxiv.org/abs/2202.07765)
- Check out our spotlight presentation at [ICML 2022](https://icml.cc/virtual/2022/spotlight/17886)

See the Google Magenta [blog post](https://magenta.tensorflow.org/perceiver-ar) with more music!
