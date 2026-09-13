---
title: "Introducing OpenAI Privacy Filter"
date: 2026-04-22
source: https://openai.com/index/introducing-openai-privacy-filter/
crawled: 2026-09-13
category: research
---

Today we’re releasing OpenAI Privacy Filter, an open-weight model for detecting and redacting personally identifiable information (PII) in text. This release is part of our broader effort to support a more resilient software ecosystem by providing developers practical infrastructure for building with AI safely, including [tools](https://openai.com/index/codex-security-now-in-research-preview/) and [models](https://openai.com/index/scaling-trusted-access-for-cyber-defense/) that make strong privacy and security protections easier to implement from the start.

Privacy Filter is a small model with frontier personal data detection capability. It is designed for high-throughput privacy workflows, and is able to perform context-aware detection of PII in unstructured text. It can run locally, which means that PII can be masked or redacted without leaving your machine. It processes long inputs efficiently, making redaction decisions in a quick, single pass.

At OpenAI, we use a fine-tuned version of Privacy Filter in our own privacy-preserving workflows. We developed Privacy Filter because we believe that with the latest AI capabilities, we could raise the standard for privacy beyond what was already on the market. The version of Privacy Filter we are releasing today achieves state-of-the-art performance on the PII-Masking-300k benchmark, when corrected for annotation issues we identified during evaluation.

With this release, developers can run Privacy Filter in their own environments, fine tune it to their own use cases, and build stronger privacy protections into training, indexing, logging, and review pipelines.

## A small model with frontier personal data detection capability

Privacy protection in modern AI systems depends on more than pattern matching. Traditional PII detection tools often rely on deterministic rules for formats like phone numbers and email addresses. They can work well for narrow cases, but they often miss more subtle personal information and struggle with context.

Privacy Filter is built with deeper language and context awareness for more nuanced performance. By combining strong language understanding with a privacy-specific labeling system, it can detect a wider range of PII in unstructured text, including cases where the right decision depends on context. It can better distinguish between information that should be preserved because it is public, and information that should be masked or redacted because it relates to a private individual.

The result is a model that is strong enough to deliver frontier-level privacy filtering performance. At the same time, the model is small enough to be run locally–meaning data that has yet to be filtered can remain on device, with less risk of exposure, rather than needing to be sent to a server for de-identification.

## Model overview

Privacy Filter is a bidirectional token-classification model with span decoding. It begins from an autoregressive pretrained checkpoint and is then adapted into a token classifier over a fixed taxonomy of privacy labels. Instead of generating text token by token, it labels an input sequence in one pass and then decodes coherent spans with a constrained Viterbi procedure.

This architecture gives Privacy Filter a few useful properties for production use:

- **Fast and efficient:** all tokens are labeled in a single forward pass.
- **Context aware:** the language prior enables PII spans to be detected based on surrounding context.
- **Long-context:** the released model supports up to 128,000 tokens of context.
- **Configurable:** developers can tune operating points to trade off recall and precision depending on their workflow.

The released model has 1.5B total parameters with 50M active parameters.

Privacy Filter predicts spans across eight categories:

- `private_person`
- `private_address`
- `private_email`
- `private_phone`
- `private_url`
- `private_date`
- `account_number`
- `secret`

The `account_number` category helps mask a wide variety of account numbers, including banking info like credit card numbers and bank account numbers, while `secret` helps mask things like passwords and API keys.

These labels are decoded with BIOES span tags, which helps produce cleaner and more coherent masking boundaries.

## Example input text

Subject: Q2 Planning Follow-Up

Hi Jordan,

Thanks again for meeting earlier today. I wanted to follow up with the revised timeline for the Q2 rollout and confirm that the product launch is scheduled for September 18, 2026. For reference, the project file is listed under 4829-1037-5581. If anything changes on your side, feel free to reply here at maya.chen@example.com or call me at +1 (415) 555-0124.

Best,

Maya Chen

## Text after masking personal identifiers

Subject: Q2 Planning Follow-Up

Hi `[PRIVATE_PERSON]`,

Thanks again for meeting earlier today. I wanted to follow up with the revised timeline for the Q2 rollout and confirm that the product launch is scheduled for `[PRIVATE_DATE]`. For reference, the project file is listed under `[ACCOUNT_NUMBER]`. If anything changes on your side, feel free to reply here at `[PRIVATE_EMAIL]` or call me at `[PRIVATE_PHONE]`.

Best,

**[PRIVATE_PERSON]**

## How we built it

We developed Privacy Filter in several stages.

First, we built a privacy taxonomy that defines the types of spans the model should detect. This includes personal identifiers, contact details, addresses, private dates, many different kinds of account numbers such as credit and banking information, and secrets such as API keys and passwords.

Second, we converted a pretrained language model into a bidirectional token classifier by replacing the language modeling head with a token-classification head and post-training it with a supervised classification objective.

Third, we trained on a mixture of publicly available and synthetic data designed to capture both realistic text and difficult privacy patterns. In parts of the public data where labels were incomplete, we used model-assisted annotation and review to improve coverage. We also generated synthetic examples to increase diversity across formats, contexts, and privacy subtypes.

At inference time, the model's token-level predictions are decoded into coherent spans using constrained sequence decoding. This approach preserves the broad language understanding of the pretrained model while specializing it for privacy detection.

## How Privacy Filter performs

We evaluated Privacy Filter on standard benchmarks and on additional synthetic and chat-style evaluations designed to test harder, more context-sensitive cases.

On the [PII-Masking-300k](https://huggingface.co/datasets/ai4privacy/pii-masking-300k) benchmark, Privacy Filter achieves an F1 score of 96% (94.04% precision and 98.04% recall). On a corrected version of the benchmark that accounts for dataset annotation issues identified during review, the F1 score is 97.43% (96.79% precision and 98.08% recall).

We also found that the model can be adapted efficiently. Fine-tuning on even a small amount of data quickly improves accuracy on domain-specific tasks, increasing F1 score from 54% to 96% and approaches saturation on the domain-adaption benchmark we evaluated.

Beyond benchmark performance, Privacy Filter is designed for practical privacy filtering in noisy, real-world text. That includes long documents, ambiguous references, mixed-format strings, and software-related secrets. The [model card](https://cdn.openai.com/pdf/c66281ed-b638-456a-8ce1-97e9f5264a90/OpenAI-Privacy-Filter-Model-Card.pdf)also reports targeted evaluation on secret detection in codebases and stress tests across multilingual, adversarial, and context-dependent examples.

## Limitations

Privacy Filter is not an anonymization tool, a compliance certification, or a substitute for policy review in high-stakes settings. It is one component in a broader privacy-by-design system.

Its behavior reflects the label taxonomy and decision boundaries it was trained on. Different organizations may want different detection or masking policies, and those policies may require in-domain evaluation or further fine-tuning. Performance may also vary across languages, scripts, naming conventions, and domains that differ from the training distribution.

Like all models, Privacy Filter can make mistakes. It can miss uncommon identifiers or ambiguous private references, and it can over- or under-redact entities when context is limited, especially in short sequences. In high-sensitivity domains such as legal, medical, and financial workflows, human review and domain-specific evaluation and fine-tuning remain important.

## Availability

We are releasing OpenAI Privacy Filter to support stronger privacy protections across the ecosystem.

The model is available today under the Apache 2.0 license on [Hugging Face](https://huggingface.co/openai/privacy-filter) and [Github](https://github.com/openai/privacy-filter). It is intended for experimentation, customization, and commercial deployment, and it can be fine-tuned for different data distributions and privacy policies.

Alongside the model, we are sharing documentation covering the model architecture, label taxonomy, decoding controls, intended use cases, evaluation setup, and known limitations, so teams can understand both what the model does well and where it should be used carefully.

## Looking ahead

Privacy protection for AI systems is an ongoing effort across research, product design, evaluation, and deployment.

Privacy Filter reflects one direction we believe is important: small, efficient models with frontier capability in narrowly defined tasks that matter for real-world AI systems. We are releasing it because we think privacy-preserving infrastructure should be easier to inspect, run, adapt, and improve.

Our goal is for models to learn about the world, not about private individuals. Privacy Filter helps make that possible.

We’re releasing this preview of Privacy Filter to receive feedback from the research and privacy community and iterate further on model performance.
