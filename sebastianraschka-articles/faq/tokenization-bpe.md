---
title: "Tokenization and byte pair encoding"
source: https://sebastianraschka.com/faq/docs/tokenization-bpe.html
crawled: 2026-09-06
---

# Tokenization and byte pair encoding

Tokenization converts text into a sequence of integer token IDs that an LLM can process. A subword method such as byte pair encoding (BPE) represents common text fragments with single IDs and less common text with several smaller pieces. This gives the tokenizer broad text coverage without requiring one vocabulary entry for every possible word.

The tokenizer sits outside the transformer. It encodes text before the model runs and decodes generated IDs back into text afterward.

![Tokenization splits input text into token pieces and maps each piece to an integer ID before the embedding lookup.](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/bpe-from-scratch/bpe-overview.webp)

## From text to token IDs

A tokenizer has a vocabulary that associates token pieces with integer IDs. For example, a tokenizer might encode `This is an example.` as five token IDs. The model uses those integers to select rows from its token-embedding matrix. The [embedding layer FAQ](https://sebastianraschka.com/faq/docs/embedding-linear-onehot.html) explains this lookup in more detail.

The integer values themselves have no numerical meaning. Token ID 500 is not inherently closer to token ID 501 than to token ID 20. Each ID is an index into the model’s learned embedding and output matrices.

This is also why a pretrained checkpoint must be used with its matching tokenizer. If another tokenizer assigns different text to ID 500, the model retrieves the wrong embedding row. Adding tokens requires resizing and training the corresponding model parameters.

## Why whole words and individual bytes are awkward

A word-level tokenizer can keep common words compact, but its vocabulary cannot contain every name, spelling variation, technical term, or new word. Text outside the vocabulary then collapses into an unknown token such as `[UNK]`, which discards the original spelling.

![A word-level vocabulary needs an unknown token when an input word has no matching entry.](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch02_compressed/09.webp)

At the other extreme, a tokenizer can represent text as individual characters or UTF-8 bytes. Coverage is excellent, but sequences become long. The string `This is some text` contains 17 bytes in UTF-8, whereas GPT-2’s BPE tokenizer represents it with 4 tokens. Longer sequences consume more context positions and increase the work done by the transformer.

Subword tokenization provides a middle ground. Frequent words and fragments receive compact representations. Rare strings remain representable as shorter pieces.

![A subword tokenizer preserves an unfamiliar word by splitting it into known pieces instead of replacing it with one unknown symbol.](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch02_compressed/11.webp)

## How BPE learns its vocabulary

Training a BPE tokenizer is separate from training the LLM. The tokenizer is usually fitted first and then held fixed while the model is pretrained.

A simplified BPE training procedure works as follows.

1. Represent the training corpus with an initial set of small symbols. A byte-level tokenizer begins with the 256 possible byte values.
2. Count adjacent symbol pairs across the corpus.
3. Replace the most frequent pair with a new symbol and record the merge.
4. Repeat the counting and merging until the chosen vocabulary size or another stopping condition is reached.

Consider the toy corpus `low lower lowest`. The adjacent pair `l` and `o` occurs three times, so a training run could merge it into `lo`. The pair `lo` and `w` would then occur three times and could become `low`. Later merges may create pieces such as `er` or `est`, depending on their frequencies and the tie-breaking rules.

The resulting vocabulary contains the original small symbols and the merged pieces. BPE does not know that `er` is sometimes an English suffix. It learned the piece from pair frequency. Token boundaries therefore do not have to match linguistic morphemes or words.

Real tokenizers add preprocessing details. They may normalize Unicode, use a regular expression to split the input into regions, preserve leading spaces as part of a token, or prevent merges across certain boundaries. These choices are part of the tokenizer and can change the final IDs even when the merge algorithm is called BPE.

My [BPE-from-scratch walkthrough](https://sebastianraschka.com/blog/2025/bpe-from-scratch.html) shows the training loop, merge table, and decoding procedure in Python.

## Encoding uses the learned merges

Once the tokenizer is trained, encoding new text does not count pairs again. It starts from the base symbols and applies the fixed learned merges according to their stored priority, often called the merge rank. Merging stops when no learned rule applies. The remaining pieces are looked up in the vocabulary to obtain token IDs.

This distinction matters because BPE training depends on corpus-wide frequencies, while encoding must be deterministic for one input string. The model and every application using it need to produce the same IDs from the same tokenizer configuration.

Decoding follows the reverse mapping. Each token ID resolves to its stored byte sequence, the sequences are concatenated, and the bytes are decoded as text. With byte-level BPE, a single token can contain only part of a multibyte Unicode character. Decoding the complete sequence is therefore safer than assuming every individual token is valid standalone text.

## Why byte-level BPE avoids unknown text

UTF-8 represents text with byte values from 0 through 255. A byte-level BPE vocabulary retains these base values and adds frequent merged byte sequences. Any input that can be represented as UTF-8 can therefore fall back to its individual bytes, even if none of its longer pieces appeared during tokenizer training.

This removes the ordinary out-of-vocabulary problem, but it does not make all text equally efficient. A tokenizer trained mostly on English may use many more tokens for another language. Code, whitespace, capitalization, and unusual Unicode characters can also change token counts substantially.

## Vocabulary size is a tradeoff

A smaller BPE vocabulary requires fewer rows in the embedding and output matrices, but it usually produces longer sequences. A larger vocabulary can encode common text with fewer tokens, while increasing those matrices and creating more token entries that need enough training examples.

The context limit is measured in tokens rather than words or characters. Two documents with the same character count can therefore occupy different amounts of the context window. Token counts should be measured with the exact tokenizer used by the checkpoint.

Special tokens require the same care. Beginning-of-sequence, end-of-sequence, padding, and chat-control tokens are reserved IDs with model-specific meanings. They are usually handled separately from ordinary BPE merges. Using the wrong end token or chat template can cause generation and stopping errors even when the regular text tokenization is correct.

Other common subword methods include WordPiece and Unigram tokenization. They make different choices about how the vocabulary is learned and how a string is segmented. The practical reason for using any of these approaches remains similar. They keep frequent text compact while retaining a path for encoding unfamiliar text.
