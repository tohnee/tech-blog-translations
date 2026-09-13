---
title: "从零实现 BPE 分词器"
title_en: "BPE Tokenizer From Scratch"
source: https://sebastianraschka.com/blog/2025/bpe-from-scratch.html
crawled: 2026-09-06
translated: 2026-09-06
---

# 从零实现 BPE 分词器

> 原文：[BPE Tokenizer From Scratch](https://sebastianraschka.com/blog/2025/bpe-from-scratch.html)

- 这是一个独立的 notebook，出于教学目的从零实现了流行的[字节对编码（BPE）](https://sebastianraschka.com/glossary/#bpe "Byte Pair Encoding (BPE)")分词算法，该算法被用于 GPT-2 到 GPT-4、Llama 3 等模型
- 关于分词目的的更多细节，请参阅[第 2 章](https://github.com/rasbt/LLMs-from-scratch/blob/main/ch02/01_main-chapter-code/ch02.ipynb)；这里的代码是讲解 BPE 算法的附加材料
- OpenAI 为训练最初的 GPT 模型而实现的原始 BPE 分词器可以在[这里](https://github.com/openai/gpt-2/blob/master/src/encoder.py)找到
- BPE 算法最早见于 1994 年 Philip Gage 的《[A New Algorithm for Data Compression](http://www.pennelynn.com/Documents/CUJ/HTML/94HTML/19940045.HTM)》
- 如今，包括 Llama 3 在内的大多数项目出于计算性能的考虑，都使用 OpenAI 的开源 [tiktoken 库](https://github.com/openai/tiktoken)；例如，它可以加载预训练的 GPT-2 和 GPT-4 分词器（Llama 3 模型训练时使用的也是 GPT-4 分词器）
- 上面提到的实现与我在本 notebook 中的实现之间的区别在于，我的实现还包含一个用于训练分词器的函数（出于教学目的）
- 还有一个支持训练的实现 [minBPE](https://github.com/karpathy/minbpe)，它可能性能更好（我这里的实现侧重于教学目的）；与 `minbpe` 不同的是，我的实现还额外支持加载 OpenAI 原始分词器的词表和 BPE"合并"规则（此外，Hugging Face 的 tokenizers 库也能训练和加载各种分词器；更多信息可参阅一位在尼泊尔语上训练了 BPE 分词器的读者写的[这份 GitHub 讨论](https://github.com/rasbt/LLMs-from-scratch/discussions/485)）

**代码**

独立的代码 notebook 可以在[这里](https://github.com/rasbt/LLMs-from-scratch/blob/main/ch02/05_bpe-from-scratch/bpe-from-scratch.ipynb)找到。

## 1. 字节对编码（BPE）背后的核心思想

- BPE 的核心思想是把文本转换为整数表示（token ID），用于 LLM 训练（参见[第 2 章](https://github.com/rasbt/LLMs-from-scratch/blob/main/ch02/01_main-chapter-code/ch02.ipynb)）

![展示字节对编码 token 合并过程的示意图](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/bpe-from-scratch/bpe-overview.webp)

### 1.1 比特与字节

- 在进入 BPE 算法之前，先介绍一下字节的概念
- 考虑把文本转换成字节数组（毕竟 BPE 是"字节"对编码）：

```python
text = "This is some text"
byte_ary = bytearray(text, "utf-8")
print(byte_ary)
```

```python
bytearray(b'This is some text')
```

- 当我们对 `bytearray` 对象调用 `list()` 时，每个字节都会被视为一个独立元素，得到的是一组与字节值对应的整数列表：

```python
ids = list(byte_ary)
print(ids)
```

```python
[84, 104, 105, 115, 32, 105, 115, 32, 115, 111, 109, 101, 32, 116, 101, 120, 116]
```

- 这确实是一种把文本转换为 LLM [嵌入层](https://sebastianraschka.com/glossary/#token-embeddings "Token Embeddings")所需的 token ID 表示的可行方式
- 然而，这种方法的缺点是它会为每个字符创建一个 ID（对一段短文本来说，ID 数量太多了！）
- 也就是说，对于一段 17 个字符的输入文本，我们必须使用 17 个 token ID 作为 LLM 的输入：

```python
print("Number of characters:", len(text))
print("Number of token IDs:", len(ids))
```

```python
Number of characters: 17
Number of token IDs: 17
```

- 如果你之前用过 LLM，可能知道 BPE 分词器有一个词表，其中为完整的单词或子词（而不是每个字符）分配 token ID
- 例如，GPT-2 分词器把同样的文本（"This is some text"）只分成 4 个 token，而不是 17 个：`1212, 318, 617, 2420`
- 你可以用交互式的 [tiktoken 应用](https://tiktokenizer.vercel.app/?model=gpt2)或 [tiktoken 库](https://github.com/openai/tiktoken)复核这一点：

![Tiktokenizer 应用截图，展示 GPT-2 的分词结果](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/bpe-from-scratch/tiktokenizer.webp)

```python
import tiktoken

gpt2_tokenizer = tiktoken.get_encoding("gpt2")
gpt2_tokenizer.encode("This is some text")
# prints [1212, 318, 617, 2420]
```

- 由于一个字节由 8 个比特组成，单个字节可以表示 2^8 = 256 种可能的取值，范围从 0 到 255
- 你可以执行代码 `bytearray(range(0, 257))` 来验证，它会警告你 `ValueError: byte must be in range(0, 256)`）
- BPE 分词器通常把这 256 个值用作最初的 256 个单字符 token；可以通过运行下面的代码直观验证：

```python
import tiktoken
gpt2_tokenizer = tiktoken.get_encoding("gpt2")

for i in range(300):
    decoded = gpt2_tokenizer.decode([i])
    print(f"{i}: {decoded}")
"""
prints:
0: !
1: "
2: #
...
255: �  # <---- single character tokens up to here
256:  t
257:  a
...
298: ent
299:  n
"""
```

- 注意，上面的条目 256 和 257 并不是单字符值，而是双字符值（一个空格加一个字母），这是原始 GPT-2 BPE 分词器的一个小瑕疵（这一点在 GPT-4 分词器中已得到改进）

### 1.2 构建词表

- BPE 分词算法的目标是构建一个由常见子词组成的词表，比如 `298: ent`（例如它出现在 *entangle, entertain, enter, entrance, entity, …* 等单词中），甚至完整的单词，例如

```python
318: is
617: some
1212: This
2420: text
```

- BPE 算法最早见于 1994 年 Philip Gage 的《[A New Algorithm for Data Compression](http://www.pennelynn.com/Documents/CUJ/HTML/94HTML/19940045.HTM)》
- 在进入实际的代码实现之前，先按下面几节所述，总结一下如今 LLM 分词器所采用的形式。

### 1.3 BPE 算法概要

**1. 找出高频词对**

- 每次迭代时，扫描文本，找出出现最频繁的字节对（或字符对）

**2. 替换并记录**

- 用一个新的占位 ID 替换该词对（一个尚未被占用的 ID，例如，如果我们从 0…255 开始，第一个占位 ID 就是 256）
- 把这个映射记录到查找表中
- 查找表的大小是一个超参数，也称为"[词表大小](https://sebastianraschka.com/glossary/#vocabulary-size "Vocabulary Size")"（对 GPT-2 而言是
  50,257）

**3. 重复直到不再有收益**

- 不断重复步骤 1 和 2，持续合并最高频的词对
- 当无法进一步压缩时停止（例如，没有任何词对出现超过一次）

**解压缩（解码）**

- 要还原原始文本，反向执行该过程，使用查找表把每个 ID 替换回它对应的词对

### 1.4 BPE 算法示例

#### 1.4.1 编码部分的具体示例（1.3 节中的步骤 1 和 2）

- 假设我们有文本（训练数据集）`the cat in the hat`，想以此为一个 BPE 分词器构建词表

**第 1 轮迭代**

1. 找出高频词对
   - 在这段文本中，"th" 出现了两次（位于开头，以及第二个 "e" 之前）
2. 替换并记录
   - 用一个尚未占用的新 token ID 替换 "th"，例如 256
   - 新文本为：`<256>e cat in <256>e hat`
   - 新词表为

```python
  0: ...
  ...
  256: "th"
```

**第 2 轮迭代**

1. **找出高频词对**
   - 在文本 `<256>e cat in <256>e hat` 中，词对 `<256>e` 出现了两次
2. **替换并记录**
   - 用一个尚未占用的新 token ID 替换 `<256>e`，例如 `257`。
   - 新文本为：

     ```python
     <257> cat in <257> hat
     ```
   - 更新后的词表为：

     ```python
     0: ...
     ...
     256: "th"
     257: "<256>e"
     ```

**第 3 轮迭代**

1. **找出高频词对**
   - 在文本 `<257> cat in <257> hat` 中，词对 `<257>`  出现了两次（一次在开头，一次在 "hat" 之前）。
2. **替换并记录**
   - 用一个尚未占用的新 token ID 替换 `<257>`，例如 `258`。
   - 新文本为：

     ```python
     <258>cat in <258>hat
     ```
   - 更新后的词表为：

     ```python
     0: ...
     ...
     256: "th"
     257: "<256>e"
     258: "<257> "
     ```

- 以此类推

#### 1.4.2 解码部分的具体示例（1.3 节中的步骤 3）

- 要还原原始文本，我们按引入顺序的逆序，把每个 token ID 替换回它对应的词对
- 从最终压缩后的文本开始：`<258>cat in <258>hat`
- 把 `<258>` 替换为 `<257>`：`<257> cat in <257> hat`
- 把 `<257>` 替换为 `<256>e`：`<256>e cat in <256>e hat`
- 把 `<256>` 替换为 "th"：`the cat in the hat`

### 2. 一个简单的 BPE 实现

- 下面用一个 Python 类实现了上述算法，它模仿了 `tiktoken` 的 Python 用户接口
- 注意，上面的编码部分描述的是通过 `train()` 完成的原始训练步骤；而 `encode()` 方法的工作方式与此类似（只不过由于要处理特殊 token，它看起来稍微复杂一些）：

1. 把输入文本拆分成单个字节
2. 只要相邻 token（词对）匹配已学习的 BPE 合并规则中的任意词对，就反复查找并替换（合并）（按"秩"从高到低，即按学习的先后顺序）
3. 持续合并，直到无法再应用任何合并
4. 最终的 token ID 列表就是编码输出

```python
from collections import Counter, deque
from functools import lru_cache
import json

class BPETokenizerSimple:
    def __init__(self):
        # Maps token_id to token_str (e.g., {11246: "some"})
        self.vocab = {}
        # Maps token_str to token_id (e.g., {"some": 11246})
        self.inverse_vocab = {}
        # Dictionary of BPE merges: {(token_id1, token_id2): merged_token_id}
        self.bpe_merges = {}

        # For the official OpenAI GPT-2 merges, use a rank dict:
        #  of form {(string_A, string_B): rank}, where lower rank = higher priority
        self.bpe_ranks = {}

    def train(self, text, vocab_size, allowed_special={"<|endoftext|>"}):
        """
        Train the BPE tokenizer from scratch.

        Args:
            text (str): The training text.
            vocab_size (int): The desired vocabulary size.
            allowed_special (set): A set of special tokens to include.
        """

        # Preprocess: Replace spaces with "Ġ"
        # Note that Ġ is a particularity of the GPT-2 BPE implementation
        # E.g., "Hello world" might be tokenized as ["Hello", "Ġworld"]
        # (GPT-4 BPE would tokenize it as ["Hello", " world"])
        processed_text = []
        for i, char in enumerate(text):
            if char == " " and i != 0:
                processed_text.append("Ġ")
            if char != " ":
                processed_text.append(char)
        processed_text = "".join(processed_text)

        # Initialize vocab with unique characters, including "Ġ" if present
        # Start with the first 256 ASCII characters
        unique_chars = [chr(i) for i in range(256)]
        unique_chars.extend(
            char for char in sorted(set(processed_text))
            if char not in unique_chars
        )
        if "Ġ" not in unique_chars:
            unique_chars.append("Ġ")

        self.vocab = {i: char for i, char in enumerate(unique_chars)}
        self.inverse_vocab = {char: i for i, char in self.vocab.items()}

        # Add allowed special tokens
        if allowed_special:
            for token in allowed_special:
                if token not in self.inverse_vocab:
                    new_id = len(self.vocab)
                    self.vocab[new_id] = token
                    self.inverse_vocab[token] = new_id

        # Tokenize the processed_text into token IDs
        token_ids = [self.inverse_vocab[char] for char in processed_text]

        # BPE steps 1-3: Repeatedly find and replace frequent pairs
        for new_id in range(len(self.vocab), vocab_size):
            pair_id = self.find_freq_pair(token_ids, mode="most")
            if pair_id is None:
                break
            token_ids = self.replace_pair(token_ids, pair_id, new_id)
            self.bpe_merges[pair_id] = new_id

        # Build the vocabulary with merged tokens
        for (p0, p1), new_id in self.bpe_merges.items():
            merged_token = self.vocab[p0] + self.vocab[p1]
            self.vocab[new_id] = merged_token
            self.inverse_vocab[merged_token] = new_id

    def load_vocab_and_merges_from_openai(self, vocab_path, bpe_merges_path):
        """
        Load pre-trained vocabulary and BPE merges from OpenAI's GPT-2 files.

        Args:
            vocab_path (str): Path to the vocab file (GPT-2 calls it 'encoder.json').
            bpe_merges_path (str): Path to the bpe_merges file  (GPT-2 calls it 'vocab.bpe').
        """
        # Load vocabulary
        with open(vocab_path, "r", encoding="utf-8") as file:
            loaded_vocab = json.load(file)
            # Convert loaded vocabulary to correct format
            self.vocab = {int(v): k for k, v in loaded_vocab.items()}
            self.inverse_vocab = {k: int(v) for k, v in loaded_vocab.items()}

        # Handle newline character without adding a new token
        if "\n" not in self.inverse_vocab:
            # Use an existing token ID as a placeholder for '\n'
            # Preferentially use "<|endoftext|>" if available
            fallback_token = next((token for token in ["<|endoftext|>", "Ġ", ""] if token in self.inverse_vocab), None)
            if fallback_token is not None:
                newline_token_id = self.inverse_vocab[fallback_token]
            else:
                # If no fallback token is available, raise an error
                raise KeyError("No suitable token found in vocabulary to map '\\n'.")

            self.inverse_vocab["\n"] = newline_token_id
            self.vocab[newline_token_id] = "\n"

        # Load GPT-2 merges and store them with an assigned "rank"
        self.bpe_ranks = {}  # reset ranks
        with open(bpe_merges_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
            if lines and lines[0].startswith("#"):
                lines = lines[1:]

            rank = 0
            for line in lines:
                pair = tuple(line.strip().split())
                if len(pair) == 2:
                    token1, token2 = pair
                    # If token1 or token2 not in vocab, skip
                    if token1 in self.inverse_vocab and token2 in self.inverse_vocab:
                        self.bpe_ranks[(token1, token2)] = rank
                        rank += 1
                    else:
                        print(f"Skipping pair {pair} as one token is not in the vocabulary.")

    def encode(self, text, allowed_special=None):
        """
        Encode the input text into a list of token IDs, with tiktoken-style handling of special tokens.
    
        Args:
            text (str): The input text to encode.
            allowed_special (set or None): Special tokens to allow passthrough. If None, special handling is disabled.
    
        Returns:
            List of token IDs.
        """
        import re
    
        token_ids = []
    
        # If special token handling is enabled
        if allowed_special is not None and len(allowed_special) > 0:
            # Build regex to match allowed special tokens
            special_pattern = (
                "(" + "|".join(re.escape(tok) for tok in sorted(allowed_special, key=len, reverse=True)) + ")"
            )
    
            last_index = 0
            for match in re.finditer(special_pattern, text):
                prefix = text[last_index:match.start()]
                token_ids.extend(self.encode(prefix, allowed_special=None))  # Encode prefix without special handling
    
                special_token = match.group(0)
                if special_token in self.inverse_vocab:
                    token_ids.append(self.inverse_vocab[special_token])
                else:
                    raise ValueError(f"Special token {special_token} not found in vocabulary.")
                last_index = match.end()
    
            text = text[last_index:]  # Remaining part to process normally
    
            # Check if any disallowed special tokens are in the remainder
            disallowed = [
                tok for tok in self.inverse_vocab
                if tok.startswith("<|") and tok.endswith("|>") and tok in text and tok not in allowed_special
            ]
            if disallowed:
                raise ValueError(f"Disallowed special tokens encountered in text: {disallowed}")
    
        # If no special tokens, or remaining text after special token split:
        tokens = []
        lines = text.split("\n")
        for i, line in enumerate(lines):
            if i > 0:
                tokens.append("\n")
            words = line.split()
            for j, word in enumerate(words):
                if j == 0 and i > 0:
                    tokens.append("Ġ" + word)
                elif j == 0:
                    tokens.append(word)
                else:
                    tokens.append("Ġ" + word)
    
        for token in tokens:
            if token in self.inverse_vocab:
                token_ids.append(self.inverse_vocab[token])
            else:
                token_ids.extend(self.tokenize_with_bpe(token))
    
        return token_ids

    def tokenize_with_bpe(self, token):
        """
        Tokenize a single token using BPE merges.

        Args:
            token (str): The token to tokenize.

        Returns:
            List[int]: The list of token IDs after applying BPE.
        """
        # Tokenize the token into individual characters (as initial token IDs)
        token_ids = [self.inverse_vocab.get(char, None) for char in token]
        if None in token_ids:
            missing_chars = [char for char, tid in zip(token, token_ids) if tid is None]
            raise ValueError(f"Characters not found in vocab: {missing_chars}")

        # If we haven't loaded OpenAI's GPT-2 merges, use my approach
        if not self.bpe_ranks:
            can_merge = True
            while can_merge and len(token_ids) > 1:
                can_merge = False
                new_tokens = []
                i = 0
                while i < len(token_ids) - 1:
                    pair = (token_ids[i], token_ids[i + 1])
                    if pair in self.bpe_merges:
                        merged_token_id = self.bpe_merges[pair]
                        new_tokens.append(merged_token_id)
                        # Uncomment for educational purposes:
                        # print(f"Merged pair {pair} -> {merged_token_id} ('{self.vocab[merged_token_id]}')")
                        i += 2  # Skip the next token as it's merged
                        can_merge = True
                    else:
                        new_tokens.append(token_ids[i])
                        i += 1
                if i < len(token_ids):
                    new_tokens.append(token_ids[i])
                token_ids = new_tokens
            return token_ids

        # Otherwise, do GPT-2-style merging with the ranks:
        # 1) Convert token_ids back to string "symbols" for each ID
        symbols = [self.vocab[id_num] for id_num in token_ids]

        # Repeatedly merge all occurrences of the lowest-rank pair
        while True:
            # Collect all adjacent pairs
            pairs = set(zip(symbols, symbols[1:]))
            if not pairs:
                break

            # Find the pair with the best (lowest) rank
            min_rank = float("inf")
            bigram = None
            for p in pairs:
                r = self.bpe_ranks.get(p, float("inf"))
                if r < min_rank:
                    min_rank = r
                    bigram = p

            # If no valid ranked pair is present, we're done
            if bigram is None or bigram not in self.bpe_ranks:
                break

            # Merge all occurrences of that pair
            first, second = bigram
            new_symbols = []
            i = 0
            while i < len(symbols):
                # If we see (first, second) at position i, merge them
                if i < len(symbols) - 1 and symbols[i] == first and symbols[i+1] == second:
                    new_symbols.append(first + second)  # merged symbol
                    i += 2
                else:
                    new_symbols.append(symbols[i])
                    i += 1
            symbols = new_symbols

            if len(symbols) == 1:
                break

        # Finally, convert merged symbols back to IDs
        merged_ids = [self.inverse_vocab[sym] for sym in symbols]
        return merged_ids

    def decode(self, token_ids):
        """
        Decode a list of token IDs back into a string.

        Args:
            token_ids (List[int]): The list of token IDs to decode.

        Returns:
            str: The decoded string.
        """
        decoded_string = ""
        for i, token_id in enumerate(token_ids):
            if token_id not in self.vocab:
                raise ValueError(f"Token ID {token_id} not found in vocab.")
            token = self.vocab[token_id]
            if token == "\n":
                if decoded_string and not decoded_string.endswith(" "):
                    decoded_string += " "  # Add space if not present before a newline
                decoded_string += token
            elif token.startswith("Ġ"):
                decoded_string += " " + token[1:]
            else:
                decoded_string += token
        return decoded_string

    def save_vocab_and_merges(self, vocab_path, bpe_merges_path):
        """
        Save the vocabulary and BPE merges to JSON files.

        Args:
            vocab_path (str): Path to save the vocabulary.
            bpe_merges_path (str): Path to save the BPE merges.
        """
        # Save vocabulary
        with open(vocab_path, "w", encoding="utf-8") as file:
            json.dump(self.vocab, file, ensure_ascii=False, indent=2)

        # Save BPE merges as a list of dictionaries
        with open(bpe_merges_path, "w", encoding="utf-8") as file:
            merges_list = [{"pair": list(pair), "new_id": new_id}
                           for pair, new_id in self.bpe_merges.items()]
            json.dump(merges_list, file, ensure_ascii=False, indent=2)

    def load_vocab_and_merges(self, vocab_path, bpe_merges_path):
        """
        Load the vocabulary and BPE merges from JSON files.

        Args:
            vocab_path (str): Path to the vocabulary file.
            bpe_merges_path (str): Path to the BPE merges file.
        """
        # Load vocabulary
        with open(vocab_path, "r", encoding="utf-8") as file:
            loaded_vocab = json.load(file)
            self.vocab = {int(k): v for k, v in loaded_vocab.items()}
            self.inverse_vocab = {v: int(k) for k, v in loaded_vocab.items()}

        # Load BPE merges
        with open(bpe_merges_path, "r", encoding="utf-8") as file:
            merges_list = json.load(file)
            for merge in merges_list:
                pair = tuple(merge["pair"])
                new_id = merge["new_id"]
                self.bpe_merges[pair] = new_id

    @lru_cache(maxsize=None)
    def get_special_token_id(self, token):
        return self.inverse_vocab.get(token, None)

    @staticmethod
    def find_freq_pair(token_ids, mode="most"):
        pairs = Counter(zip(token_ids, token_ids[1:]))

        if not pairs:
            return None

        if mode == "most":
            return max(pairs.items(), key=lambda x: x[1])[0]
        elif mode == "least":
            return min(pairs.items(), key=lambda x: x[1])[0]
        else:
            raise ValueError("Invalid mode. Choose 'most' or 'least'.")

    @staticmethod
    def replace_pair(token_ids, pair_id, new_id):
        dq = deque(token_ids)
        replaced = []

        while dq:
            current = dq.popleft()
            if dq and (current, dq[0]) == pair_id:
                replaced.append(new_id)
                # Remove the 2nd token of the pair, 1st was already removed
                dq.popleft()
            else:
                replaced.append(current)

        return replaced
```

- 上面的 `BPETokenizerSimple` 类包含大量代码，详细讨论超出了本 notebook 的范围，但下一节会简要概述其用法，帮助大家更好地理解这些类方法

### 3. BPE 实现演练

- 实践中，我强烈推荐使用 [tiktoken](https://github.com/openai/tiktoken)，因为我上面的实现侧重于可读性和教学目的，而非性能
- 不过，其用法与 tiktoken 大同小异，只是 tiktoken 没有训练方法
- 下面通过一些例子来看看我的 `BPETokenizerSimple` Python 代码是如何工作的（详细的代码讨论不在本 notebook 的范围之内）

#### 3.1 训练、编码与解码

- 首先，让我们取一段样例文本作为训练数据集：

```python
import os
import urllib.request

def download_file_if_absent(url, filename, search_dirs):
    for directory in search_dirs:
        file_path = os.path.join(directory, filename)
        if os.path.exists(file_path):
            print(f"{filename} already exists in {file_path}")
            return file_path

    target_path = os.path.join(search_dirs[0], filename)
    try:
        with urllib.request.urlopen(url) as response, open(target_path, "wb") as out_file:
            out_file.write(response.read())
        print(f"Downloaded {filename} to {target_path}")
    except Exception as e:
        print(f"Failed to download {filename}. Error: {e}")
    return target_path

verdict_path = download_file_if_absent(
    url=(
         "https://raw.githubusercontent.com/rasbt/"
         "LLMs-from-scratch/main/ch02/01_main-chapter-code/"
         "the-verdict.txt"
    ),
    filename="the-verdict.txt",
    search_dirs=["ch02/01_main-chapter-code/", "../01_main-chapter-code/", "."]
)

with open(verdict_path, "r", encoding="utf-8") as f: # added ../01_main-chapter-code/
    text = f.read()
```

```python
the-verdict.txt already exists in ../01_main-chapter-code/the-verdict.txt
```

- 接下来，初始化 BPE 分词器，并以 1,000 的词表大小进行训练
- 注意，由于前面讨论过的字节取值，词表大小默认已经是 256，所以我们只"学习"744 个词表条目（如果把 `<|endoftext|>` 特殊 token 和 `Ġ` 空格 token 考虑在内的话；严格来说，那是 742 个）
- 作为对比，GPT-2 的词表是 50,257 个 token，GPT-4 的词表是 100,256 个 token（tiktoken 中的 `cl100k_base`），GPT-4o 则使用 199,997 个 token（tiktoken 中的 `o200k_base`）；与上面这段简单的示例文本相比，它们的训练集都大得多

```python
tokenizer = BPETokenizerSimple()
tokenizer.train(text, vocab_size=1000, allowed_special={"<|endoftext|>"})
```

- 你可能想查看词表的内容（但注意这会创建一份很长的列表）

```python
# print(tokenizer.vocab)
print(len(tokenizer.vocab))
```

```python
1000
```

- 这个词表是通过 742 次合并创建的（`= 1000 - len(range(0, 256)) - len(special_tokens) - "Ġ" = 1000 - 256 - 1 - 1 = 742`）

```python
print(len(tokenizer.bpe_merges))
```

```python
742
```

- 这意味着前 256 个条目是单字符 token
- 接下来，让我们通过 `encode` 方法使用创建好的合并规则来编码一些文本：

```python
input_text = "Jack embraced beauty through art and life."
token_ids = tokenizer.encode(input_text)
print(token_ids)
```

```python
[424, 256, 654, 531, 302, 311, 256, 296, 97, 465, 121, 595, 841, 116, 287, 466, 256, 326, 972, 46]
```

```python
input_text = "Jack embraced beauty through art and life.<|endoftext|> "
token_ids = tokenizer.encode(input_text)
print(token_ids)
```

```python
[424, 256, 654, 531, 302, 311, 256, 296, 97, 465, 121, 595, 841, 116, 287, 466, 256, 326, 972, 46, 60, 124, 271, 683, 102, 116, 461, 116, 124, 62]
```

```python
input_text = "Jack embraced beauty through art and life.<|endoftext|> "
token_ids = tokenizer.encode(input_text, allowed_special={"<|endoftext|>"})
print(token_ids)
```

```python
[424, 256, 654, 531, 302, 311, 256, 296, 97, 465, 121, 595, 841, 116, 287, 466, 256, 326, 972, 46, 257]
```

```python
print("Number of characters:", len(input_text))
print("Number of token IDs:", len(token_ids))
```

```python
Number of characters: 56
Number of token IDs: 21
```

- 从上面的长度可以看出，一个 42 个字符的句子被编码成了 20 个 token ID，与基于字符字节的编码相比，输入长度大约缩短了一半
- 注意，`decode()` 方法使用的正是词表本身，它让我们能够把 token ID 映射回文本：

```python
print(token_ids)
```

```python
[424, 256, 654, 531, 302, 311, 256, 296, 97, 465, 121, 595, 841, 116, 287, 466, 256, 326, 972, 46, 257]
```

```python
print(tokenizer.decode(token_ids))
```

```python
Jack embraced beauty through art and life.<|endoftext|>
```

- 逐个遍历 token ID，可以让我们更清楚地了解 token ID 是如何通过词表被解码的：

```python
for token_id in token_ids:
    print(f"{token_id} -> {tokenizer.decode([token_id])}")
```

```python
424 -> Jack
256 ->  
654 -> em
531 -> br
302 -> ac
311 -> ed
256 ->  
296 -> be
97 -> a
465 -> ut
121 -> y
595 ->  through
841 ->  ar
116 -> t
287 ->  a
466 -> nd
256 ->  
326 -> li
972 -> fe
46 -> .
257 -> <|endoftext|>
```

- 可以看到，大多数 token ID 表示的是 2 字符子词；这是因为训练数据文本非常短，重复的单词不多，而且我们使用的词表大小相对较小
- 总结一下，调用 `decode(encode())` 应该能够还原任意输入文本：

```python
tokenizer.decode(
    tokenizer.encode("This is some text.")
)
```

```python
'This is some text.'
```

```python
tokenizer.decode(
    tokenizer.encode("This is some text with \n newline characters.")
)
```

```python
'This is some text with \n newline characters.'
```

#### 3.2 保存与加载分词器

- 接下来，看看如何保存训练好的分词器以便日后复用：

```python
# Save trained tokenizer
tokenizer.save_vocab_and_merges(vocab_path="vocab.json", bpe_merges_path="bpe_merges.txt")
```

```python
# Load tokenizer
tokenizer2 = BPETokenizerSimple()
tokenizer2.load_vocab_and_merges(vocab_path="vocab.json", bpe_merges_path="bpe_merges.txt")
```

- 加载后的分词器应该能产生与之前相同的结果：

```python
print(tokenizer2.decode(token_ids))
```

```python
Jack embraced beauty through art and life.<|endoftext|>
```

```python
tokenizer2.decode(
    tokenizer2.encode("This is some text with \n newline characters.")
)
```

```python
'This is some text with \n newline characters.'
```

#### 3.3 从 OpenAI 加载原始的 GPT-2 BPE 分词器

- 最后，让我们加载 OpenAI 的 GPT-2 分词器文件

```python
# Download files if not already present in this directory

# Define the directories to search and the files to download
search_directories = ["ch02/02_bonus_bytepair-encoder/gpt2_model/", "../02_bonus_bytepair-encoder/gpt2_model/", "."]

files_to_download = {
    "https://openaipublic.blob.core.windows.net/gpt-2/models/124M/vocab.bpe": "vocab.bpe",
    "https://openaipublic.blob.core.windows.net/gpt-2/models/124M/encoder.json": "encoder.json"
}

# Ensure directories exist and download files if needed
paths = {}
for url, filename in files_to_download.items():
    paths[filename] = download_file_if_absent(url, filename, search_directories)
```

```python
vocab.bpe already exists in ../02_bonus_bytepair-encoder/gpt2_model/vocab.bpe
encoder.json already exists in ../02_bonus_bytepair-encoder/gpt2_model/encoder.json
```

- 接下来，我们通过 `load_vocab_and_merges_from_openai` 方法加载这些文件：

```python
tokenizer_gpt2 = BPETokenizerSimple()
tokenizer_gpt2.load_vocab_and_merges_from_openai(
    vocab_path=paths["encoder.json"], bpe_merges_path=paths["vocab.bpe"]
)
```

- 词表大小应该是 `50257`，我们可以用下面的代码确认：

```python
len(tokenizer_gpt2.vocab)
```

```python
50257
```

- 现在我们就可以通过 `BPETokenizerSimple` 对象使用 GPT-2 分词器了：

```python
input_text = "This is some text"
token_ids = tokenizer_gpt2.encode(input_text)
print(token_ids)
```

```python
[1212, 318, 617, 2420]
```

```python
print(tokenizer_gpt2.decode(token_ids))
```

```python
This is some text
```

- 你可以用交互式的 [tiktoken 应用](https://tiktokenizer.vercel.app/?model=gpt2)或 [tiktoken 库](https://github.com/openai/tiktoken)复核它产生的是正确的 token：

![Tiktokenizer 应用截图，展示 GPT-2 的分词结果](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/bpe-from-scratch/tiktokenizer.webp)

```python
import tiktoken

gpt2_tokenizer = tiktoken.get_encoding("gpt2")
gpt2_tokenizer.encode("This is some text")
# prints [1212, 318, 617, 2420]
```

## 4. 结论

- 就是这些！这就是 BPE 的工作原理概貌：既包含用于创建新分词器的训练方法，也支持从 OpenAI 原始 GPT-2 模型加载 GPT-2 分词器的词表与合并规则
- 希望这个简短教程对学习有所帮助；如果你有任何问题，欢迎随时到[这里](https://github.com/rasbt/LLMs-from-scratch/discussions/categories/q-a)发起一个新的讨论

**代码**

独立的代码 notebook 可以在[这里](https://github.com/rasbt/LLMs-from-scratch/blob/main/ch02/05_bpe-from-scratch/bpe-from-scratch.ipynb)找到。
