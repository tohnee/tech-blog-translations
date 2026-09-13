---
title: "What is perplexity, and what does it actually tell us about an LLM?"
source: https://sebastianraschka.com/faq/docs/perplexity-what-it-means.html
crawled: 2026-09-06
---

# What is perplexity, and what does it actually tell us about an LLM?

**Perplexity** measures how well a language model predicts the observed next tokens in a particular dataset. It is the exponential of the average cross-entropy loss. Lower values indicate that the model assigned more probability to the tokens that actually occurred.

For valid target positions (\mathcal{I}), the average next-token loss is

[
\mathcal{L}
= -\frac{1}{N}
\sum\_{i \in \mathcal{I}}
\log p\_\theta(x\_i \mid x\_{<i}),
]

where (N) is the number of included tokens. When the logarithm is natural, perplexity is

[
\operatorname{PPL} = \exp(\mathcal{L}).
]

With base-2 logarithms, the loss is measured in bits per token and perplexity is (2^\mathcal{L}). The numerical perplexity is unchanged as long as the logarithm and exponentiation use the same base.

The same quantity can be written as the geometric mean of the inverse probabilities assigned to the observed tokens:

[
\operatorname{PPL}
= \left(
\prod\_{i \in \mathcal{I}}
\frac{1}{p\_\theta(x\_i \mid x\_{<i})}
\right)^{1/N}.
]

This form gives perplexity a useful numerical interpretation. If a model assigned probability 0.25 to every correct next token, its average loss would be (-\log(0.25) = \log(4)), and its perplexity would be 4. A perfect predictor has perplexity 1. A model that predicts uniformly over a vocabulary of (V) tokens has perplexity (V). Perplexity itself is neither a probability nor a percentage.

The phrase “effective number of choices” is sometimes used for this interpretation. It should be treated as an intuition. A perplexity of 4 does not mean that every position had exactly four equally likely candidates. Real token distributions vary widely between positions.

![Perplexity exponentiates the same average cross-entropy loss used for next-token training.](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch05_compressed/cross-entropy.webp)

Perplexity is most useful for comparisons where the evaluation setup stays fixed. For example, it can help answer whether a later training checkpoint predicts a held-out corpus better, whether an architecture change improves language modeling under the same training recipe, or whether training has started to overfit.

The held-out dataset matters. Training perplexity can keep falling as a model memorizes its training examples. Validation perplexity measures generalization to unseen text from the chosen validation distribution, so it is usually the more informative number. A low value on news articles does not guarantee a low value on source code, medical text, or conversational data.

![Training and validation loss curves show whether token prediction improves on held-out data or only on the training set.](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch05_compressed/train-steps.webp)

Several evaluation details must also match:

- **Tokenizer.** Different tokenizers split the same text into different targets. Token-level perplexity values from two tokenizers are generally not directly comparable.
- **Corpus and preprocessing.** Document boundaries, normalization, end-of-text markers, and which text is included all affect the result.
- **Context policy.** Window length, stride, and whether context resets at document or chunk boundaries change how much preceding text the model can use.
- **Loss mask.** Padding and any intentionally excluded prompt positions should not contribute to either the total loss or the token count.
- **Model mode.** Dropout should be disabled, and perplexity should be computed from the model’s original next-token probabilities without sampling, top-k filtering, or temperature changes.

When tokenizers differ, bits per byte or bits per character can provide a more comparable normalization. The raw text encoding and preprocessing still have to match. For sliding-window evaluation, each target token should be counted once even if overlapping windows provide additional left context.

The [next-token-prediction FAQ](https://sebastianraschka.com/faq/docs/next-token-prediction.html) explains how the individual token losses are computed. Perplexity simply puts their average back onto a probability-like scale through exponentiation. Because the exponential function is monotonic, comparing perplexity is equivalent to comparing average cross-entropy when everything else is unchanged.

Perplexity does not directly measure factual accuracy, reasoning, instruction following, safety, or the quality of a complete generated response. A model can assign high likelihood to common text patterns while still producing an incorrect answer. Conversely, an instruction-tuned model can become more useful for chat without improving perplexity on an unrelated pretraining corpus.

Perplexity also hides variation inside the average. A few domains or token types can have very high losses while the overall number looks reasonable. Per-token losses and separate domain results help reveal these cases. The troubleshooting guide [Why can a model have low training loss but still generate poor text?](https://sebastianraschka.com/faq/docs/low-loss-but-poor-text.html) covers the corresponding gap between token-level optimization and generation quality.

I would therefore use perplexity as a controlled language-modeling metric. It is well suited to training curves and same-setup ablations. Broader model selection should pair it with task-specific checks and output evaluation, as described in [Why is evaluating LLM outputs difficult?](https://sebastianraschka.com/faq/docs/evaluating-llm-outputs.html)
