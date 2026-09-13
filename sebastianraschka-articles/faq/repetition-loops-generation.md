---
title: "Why LLMs get stuck in repetition loops"
source: https://sebastianraschka.com/faq/docs/repetition-loops-generation.html
crawled: 2026-09-06
---

# Why LLMs get stuck in repetition loops

LLMs can get stuck in repetition loops because every generated token becomes part of the context for the next prediction. Once a phrase is repeated, the new context may assign even more probability to another copy. Greedy or highly constrained decoding then keeps selecting the same local continuation.

Suppose a model generates “The main reason is” twice. Its next-token distribution now conditions on a prefix that already contains this repeated structure. If the highest-probability continuation completes the phrase again, the sequence enters a self-reinforcing region. The decoding loop chooses one token at a time and does not run an explicit paragraph-level repetition check.

![Autoregressive generation feeds every selected token back into the context, allowing a repeated pattern to reinforce its own continuation.](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch05_compressed/gpt-process.webp)

Repetition has several possible sources, and they require different fixes.

**Decoding can expose a concentrated distribution.** Greedy decoding always selects the largest logit. A very low temperature sharpens the distribution, while a small top-k or restrictive top-p cutoff removes alternatives. These settings can make an existing repetitive mode deterministic.

Increasing randomness is not a universal fix. A moderate temperature or wider candidate set may let generation leave the loop. Excessive randomness can move the text into a low-probability context and create a different kind of degeneration. The [temperature, top-k, and top-p FAQ](https://sebastianraschka.com/faq/docs/temperature-topk-topp-sampling.html) explains how these controls reshape token selection.

![Decoding chooses one token from the current probability distribution, and that choice changes every distribution that follows.](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch05_compressed/proba-to-text.webp)

**The model or data can favor repetitive text.** A small or undertrained model may rely heavily on short local patterns. Overfitting can make it reproduce repeated passages from a narrow dataset. Duplicate finetuning records, templated synthetic responses, and many examples with the same headings or transition phrases can also raise the probability of those patterns.

Training and generation expose the model to different prefixes. During teacher-forced training, the next prediction receives the actual preceding tokens from the dataset. During generation, it receives the model’s own earlier choices. One weak choice can move the sequence into a context that rarely appeared in training. This mismatch is often called **exposure bias**.

**The prompt or chat template can create the loop.** A prompt ending with an unfinished list may encourage the model to keep adding similarly shaped items. Repeated instructions can be echoed. For an instruct checkpoint, a missing assistant-start marker or wrong end-of-turn token can make the model generate both sides of a conversation indefinitely. The intended [chat template](https://sebastianraschka.com/faq/docs/why-prompt-templates-matter.html) should be applied before changing sampling settings.

**Generation code can duplicate or misread the context.** Each decoding step should select from the logits at the final position and append exactly one new token ID. A loop can appear if code appends the complete decoded response again, feeds the original prompt without the latest token, selects logits from the wrong position, or combines a KV cache with incorrect position IDs or attention masks.

The tokenizer and checkpoint must match as well. The model should run in evaluation mode so dropout is disabled. When the context reaches its maximum length, the truncation policy should preserve the intended recent history and any instructions that must remain visible.

**Stopping logic can turn repetition into an apparently infinite run.** The generator should stop when it emits the checkpoint’s end-of-sequence or end-of-turn token. It also needs a maximum-new-token limit as a safety bound. Application stop strings may span multiple token IDs, so checking only the latest token can miss them.

I would debug a repetition loop in this order:

1. Run greedy decoding with the correct checkpoint, tokenizer, chat template, and model evaluation mode.
2. Log the generated token IDs and verify that each step appends one token, reads the final logits, and advances cache positions correctly.
3. Confirm the end token, stop strings, and maximum-new-token limit.
4. Compare greedy output with a moderate temperature and a reasonable top-k or top-p setting.
5. Test several prompts and inspect validation loss, duplicated training records, and repetitive response templates.

Greedy decoding is useful for debugging because it is deterministic. If an implementation produces different greedy output from the same input and checkpoint, there may be nondeterministic kernels or hidden state outside the shown loop. If greedy repeats while moderate sampling usually escapes, the decoding distribution is likely part of the problem. If every decoding method repeats on many prompts, the checkpoint, data, or template deserves closer inspection.

Anti-repetition controls can help once the basic loop is correct. A **repetition penalty** reduces the probability of token IDs that already appeared. A **presence penalty** penalizes a previously used token once, while a **frequency penalty** grows with its count. A **no-repeat n-gram rule** blocks any next token that would recreate an earlier n-gram.

These controls need conservative settings. Natural language legitimately repeats names, function identifiers, punctuation, and common words. Strong penalties can damage code, quoted text, factual names such as “New York,” or structured output with recurring field names. An n-gram rule can stop exact copying while leaving semantic repetition untouched.

Prompting can also help when it defines a finite structure, such as a requested number of items or an explicit ending condition. For a recurring production failure, better finetuning examples and preference data may improve the response distribution more reliably than an aggressive decoding penalty.

The general [autoregressive-generation FAQ](https://sebastianraschka.com/faq/docs/autoregressive-text-generation.html) shows the complete token loop. If repetition accompanies suspiciously low training loss or broadly poor text, the [training and generation troubleshooting guide](https://sebastianraschka.com/faq/docs/low-loss-but-poor-text.html) covers target leakage, tokenizer mismatches, and overfitting.
