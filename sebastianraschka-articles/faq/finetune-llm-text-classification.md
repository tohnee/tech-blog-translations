---
title: "How can a pretrained LLM be finetuned for text classification?"
source: https://sebastianraschka.com/faq/docs/finetune-llm-text-classification.html
crawled: 2026-09-06
---

# How can a pretrained LLM be finetuned for text classification?

A pretrained LLM can be adapted for text classification by keeping its transformer backbone and replacing the next-token output head with a small classifier. Chapter 6 of the repo uses spam detection as a concrete example.

The original language-model head maps each hidden vector to one logit for every token in the vocabulary. A classification head instead maps a hidden vector to \(C\) logits, where \(C\) is the number of classes. Binary spam detection therefore needs two output logits.

![A pretrained GPT backbone can be adapted by replacing the original output head](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch06_compressed/09.webp)

The classifier also needs one vector that represents the input sequence. For a causal GPT-style model, the hidden state at the final text token is a natural choice. That position can attend to every earlier token in the input, while an earlier position has seen only a shorter prefix.

Padding requires some care here. In a variable-length batch, the final array position may be a padding token. The classifier should select the last non-padding token for each example, or use another explicitly defined pooling rule.

![In a causal GPT model, the final token representation contains information from the full prefix](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch06_compressed/11.webp)

Training uses labeled texts and a loss such as cross-entropy. PyTorch’s `CrossEntropyLoss` receives the raw class logits and the integer class label. It applies the required log-softmax calculation internally, so the training code should not pass probabilities into this loss.

At inference time, `argmax` over the class logits selects the predicted label. Applying softmax first is useful when probabilities are needed for reporting or thresholding, although it does not change which class has the largest score.

![Class logits can be turned into class predictions with softmax and argmax](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch06_compressed/14.webp)

The amount of backbone adaptation is a separate decision. Training only the new head is inexpensive and treats the pretrained transformer as a fixed feature extractor. Full finetuning updates every layer and requires more memory. Chapter 6 uses a middle ground: it trains the new head and unfreezes the last transformer block plus the final normalization layer.

I would keep the train, validation, and test splits separate before finetuning. Accuracy is useful for balanced classes. For an imbalanced task such as rare-event detection, precision, recall, and F1 reveal errors that accuracy can hide. The decision threshold can be selected on the validation set and then held fixed for the test set.

This procedure produces a specialized predictor. A spam classifier maps text to a fixed label set and no longer uses its output head for general next-token generation. Instruction finetuning has a different goal and keeps the generative language-model interface.
