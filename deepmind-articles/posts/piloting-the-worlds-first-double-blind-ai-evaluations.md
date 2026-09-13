---
title: "Piloting the world's first double-blind AI evaluations"
source: https://deepmind.google/blog/piloting-the-worlds-first-double-blind-ai-evaluations/
site: deepmind
date: 2026-08-27
authors: William Isaac, Sol Messing, Kristian Lum
crawled: 2026-09-13
---

Building trust in proprietary model benchmarks using cryptographically secure environments

Imagine a student is set to take a high-stakes exam. If they accidentally peek at the test questions in advance, achieving a perfect score is influenced by this knowledge, making it a meaningless accomplishment. To truly measure what they know, they must have no visibility of the test questions until it's time to take the exam. That is the exact challenge the industry faces when evaluating advanced AI models. If a model has already seen the test questions - a problem known as benchmark contamination - the results can only be trusted to an extent.

Today, we’re introducing the **world’s first double-blind evaluation of a proprietary, frontier class AI model,** which keeps external evaluations confined to a cryptographic “box” where they can’t be used by models later to optimize performance ahead of testing. We're partnering with the Singapore AI Safety Institute, OpenMined, AVERI, and [MLCommons](https://mlcommons.org/2026/08/double-blind-reliability-evaluation/), to test a Gemini Flash Lite model against confidential benchmarks in a [privacy-preserving environment](https://cloud.google.com/blog/products/identity-security/verifiable-trust-in-the-ai-era-whats-new-in-confidential-computing), increasing evaluation integrity.

At Google, we assess our AI systems using a broad spectrum of evaluations throughout model development and deployment, but we don’t rely on internal testing alone. To identify potential blindspots, we work with a diverse group of external partners, including specialized research labs, civil society and national AI Safety and Security Institutes (AISIs), using their unique expertise to stress-test our models.

As AI models become more capable, ensuring the model has not seen the test questions or prompts in advance is critical, as this can skew the results. Policymakers, researchers, and enterprises need to trust that AI benchmarks accurately reflect a model's true capabilities and safety, but if models are able to “peek” at the evaluation questions in advance, it can artificially inflate scores and undermine this trust.

Although zero-logging protocols and rigorous contractual safeguards have long kept external test prompts confidential, incorporating technical and cryptographic safeguards marks a major step forward in secure model evaluation.

## How double-blind evaluations work

![An architectural diagram illustrating a 7-step secure evaluation workflow between an "AI Owner" and an "Evaluator" using a secure "GPU Enclave."](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/QIliP0rsPdITCeVJ/Double_blind_evals_diagram.svg)![An architectural diagram illustrating a 7-step secure evaluation workflow between an "AI Owner" and an "Evaluator" using a secure "GPU Enclave."](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/QIliP0rsPdITCeVJ/Double_blind_evals_diagram_dark.svg)

Historically, high-stakes external evaluations required a tradeoff. Either evaluators handed over their testing prompts (risking the model provider seeing the test questions in advance), or the model provider handed over their model weights (risking their intellectual property).

Double-blind evaluations eliminate this compromise. By using Confidential Space within Google Cloud’s [Confidential Computing](https://cloud.google.com/security/products/confidential-computing) portfolio, we can cryptographically verify that both the external evaluation data and the proprietary model remain private to their respective owners. The evaluator cannot see the Gemini model weights, and Google cannot see the evaluator’s test prompts.

## A novel approach to building trust in model evaluations

This cryptographic evidence helps prevent benchmark contamination and protects sensitive data. As models become more capable this becomes particularly important for highly sensitive evaluations, such as those used for cybersecurity or by government bodies. Double-blind evaluations unlock the ability for independent organizations to rigorously test advanced models without compromising data sovereignty or security.

We hope this pilot establishes a new frontier for model oversight, helping the broader industry build safer, more reliable, and widely trusted AI systems. To learn more about our methodology and findings, read our [technical report](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/piloting-the-worlds-first-double-blind-ai-evaluations/double-blind-evaluations-technical-report.pdf).
