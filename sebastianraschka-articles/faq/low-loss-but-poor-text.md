---
title: "Why can a model have low training loss but still generate poor text?"
source: https://sebastianraschka.com/faq/docs/low-loss-but-poor-text.html
crawled: 2026-09-06
---

# Why can a model have low training loss but still generate poor text?

A low training loss only says that the model predicts the training targets well under the loss calculation being used. Poor generated text can still come from overfitting, a bug in the training or generation pipeline, unsuitable decoding settings, or a mismatch between next-token likelihood and the behavior we want from a complete response.

I would debug these possibilities in that order rather than treating the loss and the generated samples as contradictory.

**First, check which loss is low.** Training loss can continue to fall while validation loss stays flat or rises. This is the familiar overfitting case. The model has learned the training sequences more closely without improving on unseen text. A held-out validation set drawn from the intended use case is therefore more informative than the final training loss.

The validation calculation should run with the same tokenizer and next-token targets used for training. The model should also be in evaluation mode so that dropout is disabled. In PyTorch, `torch.no_grad()` saves memory during this calculation, but it does not replace `model.eval()`.

![Training and validation curves help distinguish continued training-set improvement from generalization to unseen text](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch05_compressed/train-steps.webp)

**Next, verify that the loss is measuring the intended task.** For a token sequence `[t0, t1, t2, t3]`, the inputs should be `[t0, t1, t2]` and the targets `[t1, t2, t3]`. If the targets accidentally equal the inputs, the residual path can make token reconstruction much easier than next-token prediction. A missing [causal mask](https://sebastianraschka.com/faq/docs/causal-attention.html) can also let each position read future tokens, producing a low loss through target leakage.

A useful sanity check is the untrained baseline. With a vocabulary of size \(V\) and approximately uniform predictions, the expected cross-entropy is about \(\ln(V)\). For the GPT-2 vocabulary of 50,257 tokens, this is about 10.8. A randomly initialized model that starts with a surprisingly small loss deserves a closer look at the target shift, masking, padding, and loss reduction.

Padding can distort the result as well. Padded target positions should normally be ignored. I would inspect one batch by printing the input token IDs, shifted target IDs, decoded strings, and per-token losses. This small test catches many data-pipeline mistakes faster than another training run. The construction is shown in more detail in [How are input-target training examples constructed for LLM pretraining?](https://sebastianraschka.com/faq/docs/input-target-pretraining-examples.html).

**If training and validation loss look plausible, test the generation code.** Start with greedy decoding so the next token is simply the `argmax` of the final-position logits. Confirm that the code loads the intended checkpoint, uses its matching tokenizer, selects logits from the last context position, appends the chosen token ID, and stops at the correct end-of-text token. An instruct model also needs the chat template it saw during finetuning.

Tokenizer mismatches are especially destructive. The same integer ID can represent different text under two vocabularies. In that situation, the model may have a perfectly reasonable loss during training and still produce nonsense when decoded with another tokenizer.

![Autoregressive generation repeatedly selects a token from the final logits and appends it to the context](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch05_compressed/gpt-process.webp)

Once greedy generation works, sampling can be introduced again. A high temperature or a very broad candidate set may admit many unlikely tokens. A very low temperature or narrow top-k can make the output repetitive. Comparing greedy output with a few moderate settings helps separate a model problem from a decoding problem. See [How do temperature, top-k, and top-p sampling differ?](https://sebastianraschka.com/faq/docs/temperature-topk-topp-sampling.html) for the individual controls.

**Finally, a real objective mismatch can remain.** Cross-entropy averages next-token errors over many positions. It does not directly score factual accuracy, instruction following, or paragraph-level coherence. During training, each prediction receives the correct preceding tokens from the dataset. During generation, the model conditions on its own previous choices, so one poor choice can move the continuation into an unfamiliar context.

This explains why a model can achieve a credible validation loss yet produce text that is bland, repetitive, or unhelpful. Dataset quality and model size matter too. A small model can learn common local patterns in a narrow corpus without developing the capacity needed for a long, coherent response. A base model trained for continuation may also complete a prompt rather than follow it as an instruction.

For that reason, I would keep loss as a training diagnostic and evaluate generated samples separately. Fixed prompts, task-specific checks, and human review reveal failure modes that average token loss cannot capture. The related distinction between loss and perplexity is covered in [What is perplexity, and what does it actually tell us about an LLM?](https://sebastianraschka.com/faq/docs/perplexity-what-it-means.html).
