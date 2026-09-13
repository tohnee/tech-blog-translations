---
title: "How does autoregressive text generation work at inference time?"
source: https://sebastianraschka.com/faq/docs/autoregressive-text-generation.html
crawled: 2026-09-06
---

# How does autoregressive text generation work at inference time?

Autoregressive text generation means that an LLM generates one token, adds it to the input, and repeats the process. The tokens it generated during earlier rounds become part of the context for the next prediction. This is where the term *autoregressive* comes from.

I find it easiest to see the details by following a single generation step. Suppose we start with the prompt “Every effort moves you”. The tokenizer first turns the text into token IDs, and the model processes this sequence. The result is a set of vocabulary scores, or logits, for each input position.

![A GPT model produces vocabulary logits that are turned into a next-token choice](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch05_compressed/gpt-process.webp)

One detail in the figure above is easy to overlook. The model returns logits at every position, but the generation loop only needs the logits from the final position. These scores describe what may come after the complete prompt. Predictions at the other positions concern earlier parts of the input and are no longer needed here.

Choosing a token happens after the model call. We first convert the final logits into probabilities and then apply a decoding method.

- **Greedy decoding** chooses the highest-probability token.
- **Sampling** draws a token from the distribution. We can modify this distribution with settings such as temperature or restrict the draw to the top *k* candidates.

Let’s say the selected token is a comma. We append its token ID to the current sequence, so the next model call receives “Every effort moves you,” rather than the original prompt. It then produces the scores for the token after the comma. Each round extends the input by exactly one selected token.

![The predicted token ID is chosen from the vocabulary scores and appended to the sequence](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch05_compressed/proba-index.webp)

This also explains why generating a long answer takes many consecutive model steps. We cannot select token `t+1` before token `t` exists. During training, the complete text is available, and the model can compute the losses for many positions together. That type of parallelism is unavailable across future output tokens at inference time.

A **KV cache** avoids some repeated work by storing the attention keys and values for the tokens already processed. Even with this cache, the model still has to wait for the current token before it can generate the next one.

Finally, the loop needs a stopping rule. Generation usually ends for one of these reasons:

- the model emits a stop or end-of-text token
- it reaches a maximum number of new tokens
- an application-level stopping rule is triggered
