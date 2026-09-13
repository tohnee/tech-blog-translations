---
title: "How Claude's Text Watermarking Works"
source: https://sebastianraschka.com/blog/2026/claude-text-watermarking.html
crawled: 2026-09-06
---

# How Claude's Text Watermarking Works

A short illustration of how Claude’s watermarking is supposed to work (based on my reading of [their released materials](https://www.anthropic.com/news/claude-text-watermark)).

In general, when we are generating tokens, there can be multiple high-scoring tokens at certain next-word positions. Usually, we sample with [top-k or top-p sampling](https://sebastianraschka.com/faq/docs/temperature-topk-topp-sampling.html) so the highest-scoring token is most often selected (if we repeat the sampling many times), but other tokens may be selected as well.

With watermarking, there is a key that influences which of the highest-scoring tokens to select. (Watermark key + recent token context → pseudorandom seed → pseudorandom scores for candidate tokens → sampling procedure biased toward candidates with favorable scores.)

Or, more concretely, the secret key and (a window of) previous token(s) influence the randomness here. Now, if we repeat this at many token positions, this creates the watermark, as it will be a pattern (statistical correlation) that is statistically unlikely to get otherwise (due to combinatorics).

![Diagram showing how a secret key and preceding tokens influence token sampling to create a statistically detectable text watermark](https://sebastianraschka.com/images/blog/2026/claude-watermarking-explained/claude-watermarking.webp)

Figure 1. Illustration of token sampling with and without watermarking, followed by an example of how repeated key-dependent token choices create a detectable pattern.

For more information about Claude's text watermarking, see my lengthier video below. The slide PDFs are available as [Claude text watermarking slides](https://sebastianraschka.com/pdf/slides/2026-08-18-claude-watermarking.pdf) and [From Conventional LLMs to Reasoning Models to Agents slides](https://sebastianraschka.com/pdf/slides/2026-08-llms-to-reasoning-to-agents.pdf).

Of course, this watermark can be removed by moderate to severe editing and rephrasing via a different, non-watermarking LLM. But this could potentially make the text worse, as it would require making several changes to the text where it swaps out words (since we don’t know the watermarked positions, a good de-watermarker would have to edit many positions).

One thing I am confused about: They basically say that they HAVE to do this for everyone due to EU regulation. Why? Sure, but this is an inference-time technique that doesn’t require retraining or training a separate model, so if they wanted, they could only do that for EU users?

**Edit**:

Someone pointed out to me:

> To answer your question about why this does not just apply to EU users:
>
> Anthropic is a provider and falls under EU AI Act because it offers Claude on the EU Market (Article 2) and its outputs may be based in the EU. That means duty to comply with transparency regulation (art 50) is on the provider. At the time of generation, Anthropic can’t know where the outputs will end up. The only reliable way to comply with the law is to mark text during generation, and to do it globally rather than segmenting by user or location.

My counter-argument was:

> In general though, I find this regulation very strict. E.g., I am thinking of a scenario where a pharmaceutical drug manufacturer can’t make and offer said pharmaceutical drug to patients in the US because someone could export it to the EU where it’s not approved yet. I.e., it shouldn’t the exporter be held liable rather than the manufacturer in this case?

Source: website version of my [Substack note](https://substack.com/@rasbt/note/c-315339554).
