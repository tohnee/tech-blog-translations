---
title: "Temperature, top-k, and top-p sampling"
source: https://sebastianraschka.com/faq/docs/temperature-topk-topp-sampling.html
crawled: 2026-09-06
---

# Temperature, top-k, and top-p sampling

Temperature, top-k, and top-p control different parts of next-token sampling. Temperature changes the relative probabilities of all tokens. Top-k restricts sampling to a fixed number of candidates. Top-p restricts it to an adaptive number of candidates whose probabilities add up to a chosen threshold.

These operations happen after the model has produced its next-token logits. They change how one token is selected from those scores. The model’s weights and learned knowledge stay unchanged.

![A GPT model produces next-token probabilities over its vocabulary. Decoding converts this distribution into one selected token.](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch05_compressed/proba-index.webp)

## Temperature rescales the logits

Suppose the model assigns logit \(z\_i\) to token \(i\). With a positive temperature \(T\), the sampling probability is

\[p\_i(T) = \frac{\exp(z\_i / T)}{\sum\_j \exp(z\_j / T)}, \qquad T > 0.\]

A temperature of 1 leaves the softmax distribution unchanged. A value between 0 and 1 sharpens it, giving more probability to the strongest candidates. A value above 1 flattens it and gives weaker candidates a better chance.

For any positive temperature, dividing every logit by the same value does not change their ranking. The most likely token remains the most likely token. What changes are the probability ratios between tokens.

`temperature = 0` deserves a qualification. Zero is undefined in the formula because it would require division by zero. Many generation APIs interpret zero as a request for greedy decoding, which selects the largest logit without sampling. This is an implementation convention rather than temperature scaling. As \(T\) approaches zero from above, the distribution approaches an argmax distribution.

## Top-k keeps a fixed number of candidates

Top-k keeps the \(k\) tokens with the largest scores, removes every other token from consideration, and renormalizes the remaining probabilities before sampling.

![Top-k sampling retains the highest-scoring candidates, renormalizes their probabilities, and samples one token.](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch05_compressed/topk.webp)

With `top_k = 1`, only the largest-logit token remains, so the selected token is the same as under greedy decoding. A value at least as large as the vocabulary size has no filtering effect.

This fixed size does not suit every distribution equally well. When one token dominates, keeping 50 candidates may admit a long tail of weak options. When the distribution is flatter, keeping only 5 may remove several plausible continuations.

## Top-p keeps an adaptive probability mass

Top-p, or **nucleus sampling**, first sorts tokens from highest to lowest probability. It then keeps the smallest prefix whose cumulative probability reaches or exceeds \(p\). The retained probabilities are renormalized before one token is sampled.

The candidate count can therefore change at every generation step. A peaked distribution may reach `top_p = 0.9` with two tokens. A flatter distribution may need dozens or hundreds. Setting `top_p = 1` normally disables this filtering.

Nucleus sampling was introduced by Holtzman and colleagues in [The Curious Case of Neural Text Degeneration](https://arxiv.org/abs/1904.09751). Its adaptive cutoff was designed to exclude the unreliable tail without imposing one fixed candidate count on every distribution.

The three controls can be summarized as follows.

| Control | What it changes | Candidate set |
| --- | --- | --- |
| Temperature | Relative probability ratios | All tokens remain eligible unless another filter is applied |
| Top-k | Rank cutoff | Up to \(k\) tokens after any other masks |
| Top-p | Cumulative probability cutoff | Varies with the distribution at each step |

## A small probability example

Assume the next-token probabilities for five tokens are

\[[0.50,\ 0.25,\ 0.15,\ 0.07,\ 0.03].\]

With `top_k = 3`, the last two candidates are removed. The first three probabilities sum to 0.90, so renormalization gives approximately

\[[0.556,\ 0.278,\ 0.167].\]

With `top_p = 0.80`, the first two tokens are insufficient because their cumulative probability is 0.75. Including the third raises it to 0.90, so top-p retains the same three tokens in this particular step. If the leading token had probability 0.88, the same top-p setting could retain only that token.

Temperature modifies the probabilities before such a cutoff is computed. Applying \(T=0.5\) to the original distribution is equivalent to squaring the probabilities and renormalizing them. The result is approximately

\[[0.734,\ 0.183,\ 0.066,\ 0.014,\ 0.003].\]

The ranking is unchanged, but the first token now receives substantially more of the probability mass.

## How the settings interact

A common decoding sequence is to rescale the logits with temperature, apply top-k or top-p filtering, renormalize the retained scores, and sample one token. The exact order can differ across libraries, especially when repetition penalties and both truncation methods are enabled.

Applying temperature before top-p matters because temperature changes the cumulative probabilities and can therefore change the size of the nucleus. Positive temperature does not change which tokens belong to the top-k set because their rank stays the same. When top-k and top-p are used together, the final pool is typically restricted by both rules.

![After decoding selects one token, autoregressive generation appends it to the context and repeats the process.](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch05_compressed/proba-to-text.webp)

For debugging, greedy decoding is a useful baseline because it removes sampling randomness. For open-ended generation, a moderate temperature combined with top-p or top-k can allow several plausible continuations while excluding weak ones. The best values depend on the checkpoint and task, so I would begin with the model’s published generation configuration rather than reuse one setting across all models.

Their direct effect is on output diversity. They cannot add factual knowledge or reasoning ability. A higher temperature can expose more alternatives, but it can also increase errors. A narrow candidate set can make output more stable, but it can also reinforce repetition. The related FAQ on [repetition loops](https://sebastianraschka.com/faq/docs/repetition-loops-generation.html) covers that failure mode, while the [autoregressive generation overview](https://sebastianraschka.com/faq/docs/autoregressive-text-generation.html) shows where decoding fits into the full token loop.
