---
title: "Looped Transformer"
source: https://sebastianraschka.com/llm-architecture-gallery/looped-depth-sharing/
crawled: 2026-09-06
---

# Looped Transformer

The main idea in a looped transformer is that it applies the same layers (i.e., the transformer block) several times. The looped transformer method is often also called recurrent depth or looped depth sharing. In a sense, it’s like a regular transformer, where the hidden states from one pass become the inputs to the next but some of the layers get reused.

We can think of this as a form of depth-wise weight tying. For instance, if we have a transformer with with `L` distinct blocks and `T` passes, we have:

```python
effective block applications = L × T
```

In a regular transformer, `T=1`, but in the looped transformer, that’s `T>1`.

With the additional number of layers that the hidden states pass through, the activation memory and KV-cache memory also grow with the number of passes, depending on the implementation. So, the looped depth, in a sense, changes the trade-off between parameter count and computation.

The basic idea goes back to the 2018 [Universal Transformers paper](https://arxiv.org/abs/1807.03819), in which the researchers combined a recurrent transition with adaptive halting at individual token positions. The later [Ouro paper](https://arxiv.org/abs/2510.25741) by ByteDance then explicitly places LoopLMs in this line of work. And modern looped transformers then reuse the same general depth-wise weight-sharing idea, but with different looping and exit mechanisms.

For instance, two 2025 papers also follow-up on the Universal Transformer. First, the [Recurrent Depth paper](https://arxiv.org/abs/2502.05171) explored scaling test-time computation by unrolling a recurrent block to additional depths. Then, [Mixture-of-Recursions paper](https://arxiv.org/abs/2507.10524) added token-level routing so that different token positions can receive different recursive depths. The aforementioned Ouro followed in October 2025, while another model, Nanbeige 4.2 (2026), simplifies the looped transformer idea by repeating the same 22-layer stack without specific routing or stopping strategies.

[Architecture gallery](https://sebastianraschka.com/llm-architecture-gallery/)
[Universal Transformers paper](https://arxiv.org/abs/1807.03819)
[Ouro paper](https://arxiv.org/abs/2510.25741)

![Nanbeige 4.2 architecture with a loop around the shared 22-layer transformer stack](https://sebastianraschka.com/llm-architecture-gallery/images/architectures/nanbeige-4-2-3b.webp)

**Figure 1.** Nanbeige 4.2 sends the hidden states through the same 22-layer stack twice. The green return path shows
the second pass through the shared weights.

What is shared

The transformer-layer weights are reused across passes

Effective depth

Nanbeige 4.2 reaches 44 block applications; Ouro-Thinking 2.6B reaches 192 at four passes

Example architectures

[Nanbeige 4.2 3B](https://sebastianraschka.com/llm-architecture-gallery/#card-nanbeige-4-2-3b) ·
[Ouro-Thinking 2.6B](https://sebastianraschka.com/llm-architecture-gallery/#card-ouro-thinking-2-6b)

## Two fixed passes in Nanbeige 4.2

[Nanbeige 4.2 3B](https://sebastianraschka.com/llm-architecture-gallery/#card-nanbeige-4-2-3b), shown in the figure above, is the newer but simpler looped transformer example in the gallery. Nanbeige sends the hidden states through the same 22-layer transformer stack twice. This gives 44 block applications from 22 distinct layers, with a fixed two-pass execution path.

Section 2.1 of the [Nanbeige 4.2 technical report](https://huggingface.co/Nanbeige/Nanbeige4.2-3B/blob/main/Nanbeige42_report.pdf) says that two passes gave the best trade-off and retained about 75% of the token efficiency of a standard architecture. The researchers tried adding additional passes, but they found that it provided little benefit in terms of modeling performance (or training loss) while making training slower and more expensive.

## Four passes and a learned exit gate in Ouro

The [Ouro paper](https://arxiv.org/abs/2510.25741) extends the same basic mechanism with a maximum recurrent depth of four and a learned exit gate, which makes it closer to the original Universal Transformers idea.

Concretely, the [Ouro-Thinking 2.6B](https://sebastianraschka.com/llm-architecture-gallery/#card-ouro-thinking-2-6b) example that is included in the gallery has 48 distinct transformer blocks. Its released configuration sets `total_ut_steps` to 4, giving one initial pass plus three repeats through the shared stack. That corresponds to an effective192 transformer-block applications.

The training objective evaluates the intermediate representation after every pass and learns a probability distribution over exits from steps 1 through 4. At inference time, the paper’s Q-exit rule selects the first step where the cumulative exit probability crosses a chosen threshold. A lower threshold favors earlier exits, while a threshold of 1 uses all four passes.

There is an implementation detail worth separating from the paper’s early-exit description. The released [Hugging Face implementation](https://huggingface.co/ByteDance/Ouro-2.6B-Thinking/blob/main/modeling_ouro.py), at this time of writing, has not implemented this exit gating (yet) and computes every configured pass first and stores the intermediate hidden states and gate scores. It then selects one of those representations or forms a weighted output. With the default `total_ut_steps: 4` and `early_exit_threshold: 1.0`, all four passes are computed and the fourth representation is selected. Reducing `total_ut_steps` lowers the executed depth. Changing only the threshold currently changes which already-computed representation supplies the output.

The [model card](https://huggingface.co/ByteDance/Ouro-2.6B-Thinking) lists 24 layers in its architecture table. However, the released [`config.json`](https://huggingface.co/ByteDance/Ouro-2.6B-Thinking/blob/main/config.json) sets `num_hidden_layers` to 48, and the implementation instantiates that 48-layer stack. The gallery therefore uses 48 distinct layers and 192 block applications for the four-pass configuration.

![Ouro-Thinking 2.6B architecture showing four passes through a shared 48-layer transformer stack and a learned exit gate](https://sebastianraschka.com/llm-architecture-gallery/images/architectures/ouro-2-6b.webp)

**Figure 2.** Ouro-Thinking 2.6B reuses its 48-layer stack four times in the released configuration. The green return path denotes the three repeated passes, and the gate scores the representation produced after each pass.

## Fixed loops versus token-level routing

The gallery examples apply recurrence at the whole-stack level. Nanbeige uses two passes for every token. Ouro trains an exit distribution over the representations produced by passes 1 through 4, although its released implementation computes all configured passes before selecting an output.

[Mixture-of-Recursions](https://arxiv.org/abs/2507.10524) uses a finer-grained approach. Its router assigns different recursion depths to individual token positions. Tokens that remain active continue through deeper recursions, while other tokens skip those computations. This also lets the model restrict attention computation and KV caching at deeper recursions to the active tokens. The potential compute and memory savings therefore come with additional routing and cache-management complexity.

I cover and explain more of this in the video linked below.

## Looped Transformers and the KV cache

The shared transformer weights do not guarantee a single shared KV cache. Ouro’s released implementation assigns a separate cache index to every layer-pass combination. With four passes, 48 layers, 16 KV heads, and a head dimension of 128, this comes to `1.5 MiB/token` in bf16. The full calculation is on the [KV-cache calculation page](https://sebastianraschka.com/llm-architecture-gallery/kv-cache-calculations/).

The Ouro paper reports that all four caches are needed during prompt prefilling. During autoregressive decoding, reusing only the final pass’s cache reduced memory by 4 times with little performance loss in the reported experiments. This cache-reuse optimization is an additional inference strategy. It is separate from sharing the transformer weights and is not the default behavior of the released Hugging Face implementation.

For a longer explanation of recurrent depth and looped transformers, see my video below.

Sources

[Dehghani et al. (2018), *Universal Transformers*](https://arxiv.org/abs/1807.03819)
[Geiping et al. (2025), *Scaling up Test-Time Compute with Latent Reasoning*](https://arxiv.org/abs/2502.05171)
[Bae et al. (2025), *Mixture-of-Recursions*](https://arxiv.org/abs/2507.10524)
[Zhu et al. (2025), *Scaling Latent Reasoning via Looped Language Models*](https://arxiv.org/abs/2510.25741)
[Nanbeige 4.2 technical report](https://huggingface.co/Nanbeige/Nanbeige4.2-3B/blob/main/Nanbeige42_report.pdf)
[Nanbeige 4.2 configuration](https://huggingface.co/Nanbeige/Nanbeige4.2-3B/blob/main/config.json)
[Ouro-2.6B-Thinking model card](https://huggingface.co/ByteDance/Ouro-2.6B-Thinking)
[Ouro-2.6B-Thinking configuration](https://huggingface.co/ByteDance/Ouro-2.6B-Thinking/blob/main/config.json)
[Ouro-2.6B-Thinking implementation](https://huggingface.co/ByteDance/Ouro-2.6B-Thinking/blob/main/modeling_ouro.py)
[KV cache / token gallery calculations](https://sebastianraschka.com/llm-architecture-gallery/kv-cache-calculations/)

[Back to architecture gallery](https://sebastianraschka.com/llm-architecture-gallery/)
