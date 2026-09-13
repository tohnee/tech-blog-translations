---
title: "Multi-Token Prediction (MTP)"
source: https://sebastianraschka.com/llm-architecture-gallery/mtp/
crawled: 2026-09-06
---

# Multi-Token Prediction (MTP)

Multi-token prediction (MTP) changes how many targets a language model learns from at each sequence position. With ordinary next-token training, the hidden state at position `t` is used to predict token `t+1`. MTP adds losses for later tokens such as `t+2` and `t+3` through auxiliary prediction heads or shallow MTP modules.

The main decoder remains causal. It cannot inspect future tokens when generating text, and it can still run one token at a time. The extra path has a second possible use, though. Some inference engines keep it as a small internal draft model for speculative decoding.

I usually check both parts when a model card mentions MTP. How many extra prediction depths were trained? And does the serving stack actually use them at inference time?

[Architecture gallery](https://sebastianraschka.com/llm-architecture-gallery/)
[MTP paper](https://arxiv.org/abs/2404.19737)

![Comparison between next-token prediction and multi-token prediction](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/mtp-next-token-vs-multi-token.webp)

Figure 1. MTP supplies several future-token targets at each training position. The lower row still generates one
token per step because the extra heads do not have to be used during inference. (Original source
[*A Dream of Spring for Open-Weight LLMs*](https://magazine.sebastianraschka.com/p/a-dream-of-spring-for-open-weight)).

Training change

Each sequence position contributes losses for more than one future-token offset

Inference option

The auxiliary path can draft several candidate tokens for the main model to verify together

Example architectures

[DeepSeek V3](https://sebastianraschka.com/llm-architecture-gallery/#card-deepseek-v3),
[Qwen3-Next 80B-A3B](https://sebastianraschka.com/llm-architecture-gallery/#card-qwen3-next-80b-a3b),
[Step 3.5 Flash 196B](https://sebastianraschka.com/llm-architecture-gallery/#card-step-3-5-flash-196b),
[Nemotron 3 Super 120B-A12B](https://sebastianraschka.com/llm-architecture-gallery/#card-nemotron-3-super-120b-a12b),
[Nemotron 3.5 Lightning 30B-A3B](https://sebastianraschka.com/llm-architecture-gallery/#card-nemotron-3-5-lightning-30b-a3b), and
[Tencent Hy4-preview](https://sebastianraschka.com/llm-architecture-gallery/#card-tencent-hy4-preview-770b-a49b)

## One hidden state, several targets

The [original MTP paper](https://arxiv.org/abs/2404.19737) uses a shared transformer trunk and one output head for each future-token offset. All heads read the trunk representation at position `t`. One predicts `t+1`, another predicts `t+2`, and so forth. These heads contain transformer layers and share the final unembedding matrix, so they are more than separate linear classifiers. For its matched experiments, the paper removed one trunk layer per added head to keep the total parameter count equal.

A common modern notation uses `D` extra prediction depths in addition to the regular next-token objective. Their losses are averaged and added with a weight \(\lambda\).

\[\mathcal{L} = \mathcal{L}\_{\mathrm{next}} +
\frac{\lambda}{D}\sum\_{k=1}^{D}\mathcal{L}\_{\mathrm{MTP}}^{(k)}.\]

This provides several supervised signals for the same prefix. The original study found that predicting four future tokens worked best across its MBPP and HumanEval settings at 7B scale, while six led on APPS. Four is therefore a result from that code-training ablation, not a fixed MTP rule.

There is also a naming wrinkle. The paper’s `n=4` means four predictions in total, including the usual next token. A production label such as MTP-1 normally means one *additional* prediction depth. In that convention, the model learns two targets per position.

## DeepSeek keeps a causal chain

[DeepSeek V3](https://arxiv.org/abs/2412.19437) uses MTP-1 and changes the head design. Its extra module combines the main decoder’s hidden state with the embedding of the next ground-truth token during training. After normalization and a projection, a transformer block predicts the following token. With multiple modules, this procedure continues sequentially, one future offset at a time.

This arrangement preserves the causal relation between the predicted tokens. It also differs from the independent parallel heads in the original paper. DeepSeek shares the token embedding and output head with the main model, while each prediction depth has its own projection and transformer block.

The DeepSeek report treats MTP primarily as an auxiliary training objective. The module can be discarded for ordinary autoregressive inference, leaving the main decoder’s inference cost unchanged. The same module can instead be repurposed for speculative decoding.

## Using MTP as an internal draft model

Speculative decoding turns the auxiliary path into a proposer. It drafts a short continuation, and the main model checks those candidate tokens in one forward pass. Accepted tokens advance generation together. Once a candidate is rejected, the remaining draft is discarded and a new round begins.

The speedup depends heavily on draft cost and acceptance rate. [Qwen3-Next](https://huggingface.co/Qwen/Qwen3-Next-80B-A3B-Instruct) trains its MTP path for multi-step inference and provides dedicated settings for SGLang and vLLM. Its model card also notes that MTP is not generally available through Hugging Face Transformers. Loading the checkpoint by itself does not activate the faster decoding path.

The labels still don’t describe the whole design. Step 3.5 Flash uses three additional modules during training and inference, calling the setup MTP-3. [Nemotron 3 Super](https://research.nvidia.com/labs/nemotron/files/NVIDIA-Nemotron-3-Super-Technical-Report.pdf) trains two MTP layers with shared weights. It can apply that shared module recursively to draft more than two tokens, which is meant to reduce the mismatch between fixed-offset training and longer autoregressive drafts.

MTP can therefore remain a training-only objective or become part of the inference system. Reported throughput gains include the serving engine, batch size, hardware, draft length, and acceptance behavior. They should not be read as a speedup supplied by the training loss alone.

Sources

[Gloeckle et al. (2024), *Better & Faster Large Language Models via Multi-token Prediction*](https://arxiv.org/abs/2404.19737)
[DeepSeek V3 technical report](https://arxiv.org/abs/2412.19437)
[Qwen3-Next model card](https://huggingface.co/Qwen/Qwen3-Next-80B-A3B-Instruct)
[Step 3.5 Flash technical report](https://arxiv.org/abs/2602.10604)
[Nemotron 3 Super technical report](https://research.nvidia.com/labs/nemotron/files/NVIDIA-Nemotron-3-Super-Technical-Report.pdf)
[A Dream of Spring for Open-Weight LLMs](https://magazine.sebastianraschka.com/p/a-dream-of-spring-for-open-weight)
[The Big LLM Architecture Comparison](https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison)

[Back to architecture gallery](https://sebastianraschka.com/llm-architecture-gallery/)
