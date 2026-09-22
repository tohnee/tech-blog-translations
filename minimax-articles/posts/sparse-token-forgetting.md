---
title: "Why Can't the MiniMax LLM Say 'Ma Jiaqi'? Internal Investigation of Sparse Token Forgetting"
date: 2026-05-25
source: https://www.minimax.io/blog/sparse-token-forgetting
crawled: 2026-09-22
---

# Why Can't the MiniMax LLM Say "Ma Jiaqi"? Internal Investigation of Sparse Token Forgetting

2026-05-26

AILLMTokenizerResearch

## Background

The MiniMax M2 series has attracted widespread attention from the developer community. During extensive usage, many users discovered certain corner cases — among which "the model cannot say Ma Jiaqi (马嘉祺)" sparked considerable discussion on Xiaohongshu and Zhihu. We also noticed that many community developers conducted rigorous analysis and argumentation on this phenomenon, including tokenizer comparisons and sampling parameter tests.

![Community discussion about MiniMax LLM sparse token forgetting on social media](https://filecdn.minimax.chat/public/sparse-token-forgetting-community-discussion-1779698066579.jpg)

Community discussion about MiniMax LLM sparse token forgetting on social media

After internal reproduction, we found this was not an isolated case — besides "Ma Jiaqi (马嘉祺)", several other low-frequency tokens (such as "Wang Dan (王郸)") exhibited similar behavior. Community developers have provided valuable analysis, but were limited by resources and could not delve further into model training-level experimental validation. As the model developers, we believe the underlying causes and mechanisms deserve a systematic investigation, and we have the capacity to compare parameter changes across pretrain and SFT layers, analyze lm_head degradation patterns, quantify sparse token forgetting mechanisms, and validate repair strategies through training experiments.

This issue has been fully investigated internally and resolved in subsequent model updates. This investigation trail also helped us identify and fix another long-standing minor-language mixing problem. Here we present our internal investigation process and experimental results, hoping to provide more reference for community discussions.

## Hypothesis 1: Token Misalignment Between Training and Inference

![Tokenizer encoding test results for Ma Jiaqi](https://filecdn.minimax.chat/public/sparse-token-forgetting-tokenizer-test-1779698066579.png)

Tokenizer encoding test results for Ma Jiaqi

From this case, the model still possesses the relevant knowledge — it can answer basic information about Ma Jiaqi (such as his group affiliation and debut date), indicating that the corresponding semantic representations have not been lost. The issue is that during generation, the model cannot output the token "Jiaqi (嘉祺)". Therefore, we first investigated at the tokenizer level: checking the token IDs for model input and expected output to confirm whether there is any mismatch in the text-to-token conversion process.

Using the post-training tokenizer to encode "Ma Jiaqi (马嘉祺)", the results are as follows:

| Text | 马嘉祺 |
| --- | --- |
| Token IDs | [4143, 190467] |
| Tokens | ['马', '嘉祺'] |
| Decode Verification | 马嘉祺 |

Both encode and decode processes work correctly, but one noteworthy detail is that "Jiaqi (嘉祺)" is tokenized as a single independent token (id=190467). These two characters co-occur infrequently in everyday corpora, making their existence as a single token somewhat unexpected. This led to a hypothesis: could it be that different tokenizer strategies were used during pretraining versus post-training+serving? Specifically, perhaps during pretraining, "嘉祺" was actually split into two tokens ['嘉', '祺'], meaning the merged "嘉祺" token never received sufficient training. If the post-training and serving stages use the merged token, its generation probability would be very low (below 5%), and under a top-p = 0.95 sampling strategy, it would be masked and thus unable to be generated.

To verify this hypothesis, we examined the pretrained model's vocab embedding from both statistical distribution and semantic nearest-neighbor perspectives to confirm whether token 190467 ("嘉祺") was adequately trained during pretraining.

1. **Statistical Distribution Check:** Comparing the embed_tokens norm distribution across the full vocabulary, token 190467 ("嘉祺") falls within the normal distribution range, without the anomalously small values typically seen in untrained tokens, indicating that this token was adequately learned during pretraining.

![LM head weight analysis showing sparse token degradation](https://filecdn.minimax.chat/public/sparse-token-forgetting-lm-head-analysis-1779698066579.png)

LM head weight analysis showing sparse token degradation

1. **Semantic Nearest-Neighbor Verification:** Performing nearest-neighbor retrieval on the embedding of "嘉祺", the results include semantically highly relevant Chinese name tokens such as "Qianxi (千玺)" and "Yaxuan (亚轩)", indicating that the pretrained model had established reasonable semantic clustering for this token, and the tokenizer was aligned with model parameters during pretraining.

Top-10 tokens closest to the "嘉祺" token embedding:

| Rank | Token | Meaning |
| --- | --- | --- |
| 1 | 亚轩 | Personal name |
| 2 | 千玺 | Yi Yangqianxi (Jackson Yee) |
| 3 | 祺 | Sub-token of "嘉祺" |
| 4 | 耀文 | Personal name |
| 5 | 嘉 | Sub-token of "嘉祺" |
| 6-10 | 王一博/徐坤/太郎/肖战... | Celebrities / Personal names |

1. **Pretrain vs. Post-training Few-shot Comparison:** To further pinpoint the stage at which the problem emerged, we conducted few-shot tests on both the pretrained base model and the post-trained model. Using other celebrity names as examples, we guided the model to answer questions involving "Ma Jiaqi (马嘉祺)":

```
Q: Who is the leader of TFBOYS?
A: The leader of TFBOYS is Wang Junkai.

Q: Who is the vocalist of F.I.R.?
A: The vocalist of F.I.R. is Zhan Wenting (Faye).

Q: Who is the leader of TNT (Teens in Times)?
A:
```

- **Pretrained base model**: Successfully continued with "The leader of TNT (Teens in Times) is Ma Jiaqi (马嘉祺)"; the "嘉祺" token was generated normally.
- **Post-trained model**: The model still tended to avoid this token and could not output it normally.

Combining all three verifications, we can rule out the tokenizer misalignment hypothesis: token 190467 ("嘉祺") was adequately trained during pretraining with correct semantic representations. The root cause must lie in the post-training stage.

## Hypothesis 2: Post-training Data Distribution Issues

Since the problem originates in the post-training stage, a natural hypothesis is that the token "嘉祺" appeared too infrequently in post-training data, causing the model to gradually "forget" its ability to generate this token during SFT.

Statistical analysis of the post-training data revealed fewer than 5 samples containing "嘉祺", essentially confirming this hypothesis.

Of course, the most straightforward fix is to supplement the post-training data with relevant samples. But what we are more interested in is: what exactly changed inside the model? Are there intermediate metrics that can more precisely characterize this sparse token forgetting mechanism? Another intriguing question is: why does the model still recognize the "嘉祺" token — why did the lack of post-training data only cause it to lose generation capability while retaining comprehension?

## Exploring Intermediate Metrics

Since most of the model's capabilities (such as knowledge Q&A, instruction following, etc.) did not degrade after post-training, we can infer that representational changes in the Transformer's intermediate layers are unlikely to be the primary cause. A more reasonable direction is to examine the two ends of the model — the input-side vocab embedding and the output-side lm_head — as these two layers directly participate in token-level mapping and are most sensitive to sparse token effects.

### Vocab Embedding: Nearly Unchanged

Comparing the vocab embeddings before and after SFT, we found virtually no difference. This is consistent with expectations: on one hand, gradient norms attenuate layer by layer during backpropagation; on the other hand, for extremely low-frequency tokens, the embedding layer receives almost no effective gradient updates from the loss — only weight decay exerts a weak regularization effect. Therefore, it is reasonable that vocab embeddings remain stable before and after post-training.

![Repair results showing restored token generation capability](https://filecdn.minimax.chat/public/sparse-token-forgetting-repair-result-1779698066579.png)

Repair results showing restored token generation capability

*[Figure: embed_tokens L2 Diff (SFT - Pretrain) histogram, token 190467 annotated within normal distribution range]*

### lm_head: Significant Changes

Turning to the output-side lm_head, we found that the weight vector corresponding to "嘉祺" underwent significant drift during post-training, mainly manifested in two aspects:

1. **Drastic Drop in Cosine Similarity and Large Norm Changes:** Computing the cosine similarity of each token vector in the lm_head before and after SFT, token 190467 ("嘉祺") ranks among the highest in magnitude of change across the entire vocabulary, indicating that its output representation has been substantially rewritten. The L2 diff also changed significantly.
2. **Dramatic Shift in Nearest-Neighbor Semantic Structure:** Comparing the nearest neighbors of the "嘉祺" vector in lm_head provides a more intuitive view of this degradation.
3. During pretraining, its neighbors were primarily semantically related Chinese personal names — Yaxuan (亚轩), Qi (祺), Xiao Zhan (肖战), Ziyi (子怡), Tingfeng (霆锋), Jielun (杰伦), etc. Although some noise tokens were mixed in, the overall clustering structure was reasonable.
4. After SFT, the neighbor structure deteriorated significantly: while some names remained among the top ranks (亚轩, Baizhi (柏芝), Wuya (无崖), Qianxi (千玺)), a large number of special tokens and noise tokens flooded in — including `</minimax:tool_call>`, `<edit_file>`, `<file_content>`, `<delete_file>` and other tool-call-related markers, as well as encoding noise like `LENBQUMs`, `EFCFFF`, `flagathlete`. These special tokens with IDs above 200,000 became anomalously close to the "嘉祺" lm_head vector, indicating that the vector space in this region had been compressed and contaminated during post-training.

## Other Findings: Which Tokens Had the Largest lm_head Changes?

Since the root cause lies in lm_head changes, a natural follow-up question is: is this degradation limited to "嘉祺"? To investigate, we computed the L2 diff of lm_head vectors before and after SFT for the entire vocabulary, sorted by magnitude of change, and systematically examined the token categories with the largest changes:

### 1. Special Tokens

- `<fim_middle>` (#1, L2=0.87), `<fim_suffix>` (#2, L2=0.82), `<fim_prefix>` (#195), `<gh_stars>` (#169)
- These tokens serve specific functions during pretraining (e.g., FIM fill-in-the-middle) and barely appear in SFT data. Large lm_head adjustments are expected and reasonable.

### 2. Japanese Colloquial / Web Templates (Largest Category, ~40%+)

- がスタート, かもしれません, に息, を満喫, きちんと, そういった, ですと, などなど, といいでしょう, にチャレンジ, 参考にしてみてください, 気を付けて...
- A large number of common Japanese SEO/blog expressions that appear with some frequency in pretraining corpora but have extremely low representation in SFT conversational data, causing significant lm_head representational drift.

### 3. LaTeX / Web Metadata

- `makebox`, `mathbbm`, `boldmath`, `mathring`, `medskip`, `mathds`, `\footnotetext`, `{multiline}`, `{corollary}`, `{defn}`
- Academic paper formatting markers, rarely used in SFT conversational data.
- `Weblinks`, `DEFAULTSORT`, `accessdate`, `commonscat`, `Commonscat`, `Reflist`, `Webarchive`, `Listaref`, `Collegamenti`, `interprogetto`
- Wikipedia source template markers, similarly unique to pretraining formatted tokens.

### 4. Chinese SEO / Spam Text

- 传奇私服 (Legend Private Server) (#6), 无痛人流 (Painless Abortion) (#17), 外墙涂装 (Exterior Wall Coating) (#166)
- Typical SEO spam keywords learned from pretraining crawler data, completely absent during SFT.

Among these, the changes in special tokens and LaTeX/web metadata are reasonable — these tokens naturally have very different distributions between pretraining and post-training stages. However, the fact that Japanese colloquial tokens account for over 40% of the most changed category caught our attention.

Looking back at earlier user feedback, M2.5 occasionally mixed in other languages during Japanese conversations — a phenomenon previously categorized as "minor-language mixing" but whose root cause had never been clearly identified. Combined with this analysis, we discovered that the two problems may share the same mechanism: severely insufficient coverage of Japanese tokens in post-training data caused their lm_head representations to drift during SFT, becoming confused with tokens from other languages in the vector space. This could both cause Japanese tokens to be erroneously activated when they shouldn't (language mixing) and push out spatially adjacent low-frequency Chinese tokens (such as "嘉祺") from the normal generation probability range (token forgetting). This finding unified two seemingly independent problems under the same framework and provided a clearer direction for subsequent repair strategies.

## Conclusion

Based on the above analysis, the core cause of sparse token forgetting is fairly clear: uneven vocabulary coverage in post-training data causes low-frequency token lm_head representations to drift during SFT. Meanwhile, the sparse update characteristic of the input embedding layer means that only generation capability is lost while comprehension is preserved.

## Validation & Repair Experiments

To address this issue, we designed a set of repair experiments centered on improving vocabulary coverage.

### Vocabulary Coverage Synthetic Data

On top of the control group (standard SFT data), we mixed in additional synthetic repetition data covering the entire vocabulary, ensuring that every token is adequately trained as a generation target during post-training. The synthetic data was constructed as follows:

- The full vocabulary (200,064 tokens) was randomly partitioned into segments, each containing approximately 8,000 tokens
- Each token list was randomly shuffled to construct a conversation sample: the query is the shuffled token list plus the instruction "Please repeat the above content", and the answer is an exact copy
- A total of approximately 500 conversations were generated, ensuring each token appears as a target at least 20 times

The core idea behind this design is: through a simple repetition task, establish a "floor guarantee" for generation frequency across the entire vocabulary at minimal data construction cost, preventing any token from undergoing lm_head degradation due to complete absence during post-training.

### Evaluation Methods

To comprehensively assess the effect of vocabulary coverage data, we designed the following test categories, comparing the experimental group (+full vocabulary coverage data) against the baseline model:

1. **Minor-Language Confusion Rate Test** (core metric, 100 samples, temperature=1.0): Using Korean and Japanese prompts respectively, measuring the occurrence rate of non-target-language characters in outputs.
2. **Ma Jiaqi Case Qualitative Verification** (temperature=0): Including direct queries and guided queries.
3. **Group Chat Comparison Cases**: Reproducing known baseline failure cases previously discovered in internal group chats (such as "无痛人流→人流 (Painless Abortion → Abortion)", "据介绍→介绍 (According to → Introduction)", "地税→地利 (Land Tax → Advantage)" and other sparse token substitution phenomena), verifying whether the experimental group fixes them.
4. **lm_head High-Degradation Token Targeted Test**: Selecting tokens with the largest lm_head cosine similarity changes in the baseline (cos_sim < 0.65), constructing prompts to guide the model to generate answers containing those tokens, and checking whether they can be correctly output.

### Experimental Results

### Minor-Language Confusion Rate

| Test | Prompt | Detection Metric | Experimental | Baseline |
| --- | --- | --- | --- | --- |
| Korean→Chinese Confusion | 짧은 이야기를 작성해 주세요 | Chinese character occurrence rate | 38% (38/100) | 49% (49/100) |
| Japanese→Russian Confusion ① | 日本ではどのような時にお年玉を渡しますか? | Russian character occurrence rate | **1%** (1/100) | 47% (47/100) |
| Japanese→Russian Confusion ② | 富士山の山頂にある神社の名前は? | Russian character occurrence rate | **1%** (1/100) | 5% (5/100) |

Japanese→Russian confusion dropped dramatically from the baseline's 47%/5% to 1%, showing significant improvement. The Korean confusion rate (38%) was on par with the control baseline (30%), suggesting that the primary cause of Korean confusion may not be token embedding degradation but rather Chinese-Korean mixed samples in training data, requiring data cleaning and other approaches.

### Qualitative Verification (temperature=0)

**Ma Jiaqi Case:**

| Case | Prompt | Experimental | Baseline |
| --- | --- | --- | --- |
| Direct Query | Please introduce Ma Jiaqi | Correctly output full introduction | Correct |
| Guided Query | What is the name of TNT's leader? | Correctly answered "Ma Jiaqi (马嘉祺)" | Unable to output "嘉祺" |

**Known Group Chat Failure Cases:**

| Case | Prompt | Experimental | Baseline |
| --- | --- | --- | --- |
| 无痛人流→人流 | Repeat this word three times: 无痛人流 | Correctly output "无痛人流" ×3 | Output "人流 人流 人流", lost "无痛" |
| 据介绍→介绍 | Repeat this word three times: 据介绍 | Correctly output "据介绍" ×3 | Output "介绍介绍介绍", lost "据" |
| 地税→地利 | Repeat this word three times: 地税 | Correctly output "地税" ×3 | Output "地利 地利 地利", completely replaced with wrong word |

These three cases perfectly demonstrate the generation-side effects of lm_head embedding degradation: the model can understand the prompt semantics (knowing it should "repeat three times"), but because the corresponding token's lm_head vector has undergone directional drift, it gets replaced by semantically similar or nearest-neighbor incorrect tokens during generation. The experimental group completely fixed these issues through full vocabulary coverage data.

**lm_head High-Degradation Token Targeted Test (cos_sim < 0.65):**

| Case | Target Token (rank / cos_sim) | Experimental | Baseline |
| --- | --- | --- | --- |
| Japanese - きちんと | きちんと (rank 31 / 0.59) | Correct | Output "ちゃんと" as substitute |
| Japanese - それほど | それほど (rank 52 / 0.62) | Correct | Output "それだけ" as substitute |
| Japanese - 色々な | 色々な (rank 39 / 0.60) | Correct | Output garbled "(多様)" as substitute |
| Japanese - 相続税 | 相続税 (rank 70 / 0.63) | Correct | Answer mixed in Korean and Russian (minor-language confusion) |
| Japanese - 凄い | 凄い (rank 71 / 0.63) | Correct | Substituted with "可愛い" |

Overall qualitative verification pass rate: experimental group 13/16, baseline only 4/16 (excluding cases where both failed at the tokenizer level). Notably, in the "相続税" (inheritance tax) case, the baseline directly mixed in Korean and Russian text, perfectly validating the causal chain from embedding degradation to minor-language confusion.

### lm_head Cosine Similarity Quantitative Analysis

To quantitatively verify the effect of full vocabulary coverage data on preserving embedding direction, we compared the lm_head cosine similarity changes of the experimental group and baseline relative to the pretrained base model:

| Metric | Experimental | Baseline |
| --- | --- | --- |
| cos sim mean | **0.9992** | 0.9837 |
| cos sim min | **0.9711** | 0.3290 |
| Tokens with cos sim < 0.95 | **0** | 9,805 (4.9%) |
| Tokens with cos sim < 0.90 | **0** | 4,234 (2.1%) |

Further breakdown by language:

| Language | Token Count | Experimental Mean | Baseline Mean | Baseline < 0.95 |
| --- | --- | --- | --- | --- |
| Japanese | 8,787 | **0.9992** | 0.9502 | 2,607 (29.7%) |
| Korean | 3,919 | **0.9995** | 0.9812 | 131 (3.3%) |
| Arabic | 6,082 | **0.9995** | 0.9821 | 265 (4.4%) |
| Russian | 3,928 | **0.9995** | 0.9866 | 147 (3.7%) |
| Chinese | 38,900 | **0.9992** | 0.9859 | 1,498 (3.9%) |
| English/Latin | 133,798 | **0.9992** | 0.9856 | 4,731 (3.5%) |

The data shows: the experimental group maintained lm_head mean cosine similarity above 0.999 across all languages, with all 200K tokens having cos_sim above 0.97 — embedding direction almost perfectly preserved. In contrast, Japanese token degradation in the baseline was particularly severe — mean cos_sim of only 0.9502, with 29.7% of Japanese tokens falling below 0.95, highly consistent with the 47% Japanese→Russian confusion rate.

### Other Directions Worth Exploring

Besides vocabulary coverage synthetic data, several other strategies deserve further exploration:

- **Mixing in Pretraining Data:** Blending pretraining corpora into SFT data at a certain ratio, leveraging the natural vocabulary coverage breadth of pretraining data to mitigate sparse token degradation. This method has been shown in existing research to be effective in alleviating catastrophic forgetting, but the mixing ratio needs careful tuning to avoid impacting SFT's conversational capabilities.
- **Targeted Synthesis for Low-Frequency Tokens:** Identifying tokens with insufficient coverage in post-training data and constructing high-quality conversation samples containing these tokens. Compared to the full vocabulary coverage approach, this method requires less data and can maintain more precise semantics, but requires maintaining a token coverage monitoring mechanism.
- **Vocabulary Pruning + CPT:** Fundamentally removing extremely low-frequency tokens (such as SEO spam keywords) from the vocabulary in target scenarios, then performing Continual Pre-Training (CPT) after reducing vocabulary size to realign the embedding space. This approach involves larger modifications but can eliminate the sparse token problem at its source.

## Deeper Reflections

The aforementioned mitigation strategies all operate during the post-training phase and are essentially remedial measures applied after the fact. Tracing the problem further to its root, the sparse token degradation phenomenon actually reflects a mismatch between the tokenizer's vocabulary design and downstream use cases.

Current LLM tokenizers are typically constructed using algorithms such as BPE on large-scale pretraining corpora. Even when low-quality text has been filtered out during corpus curation, the resulting vocabulary inevitably contains many low-frequency tokens that only appear in specific domains or languages. While these tokens may acquire some degree of learned representations during pretraining, once the model enters the post-training phase, the significant distributional shift between SFT data and pretraining data causes substantial parameter drift for the corresponding sparse tokens — this is essentially a form of catastrophic forgetting induced by distribution shift.

During pretraining, the tokenizer's vocabulary construction should incorporate forward-looking considerations of the post-training data distribution. By adjusting vocabulary size or merge strategies, one can reduce sparse tokens that are unlikely to be activated in downstream scenarios, thereby achieving better alignment between vocabulary design and the actually deployed model. During post-training, the training data coverage strategy must address two dimensions simultaneously: first, ensuring sufficient coverage across different task types and domains from a business perspective; second, continuously monitoring from a low-level statistical perspective whether the generation probabilities of low-frequency tokens in the vocabulary exhibit abnormal decay.
