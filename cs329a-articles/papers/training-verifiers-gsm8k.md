---
title: "Training Verifiers to Solve Math Word Problems"
arxiv: 2110.14168
source: https://arxiv.org/abs/2110.14168
crawled: 2026-09-23
---

# Training Verifiers to Solve Math Word Problems

Karl Cobbe  
Vineet Kosaraju00footnotemark: 
0
  
Mohammad Bavarian  
Mark Chen  
Heewoo Jun  
Łukasz Kaiser  
Matthias Plappert  
Jerry Tworek  
Jacob Hilton  
Reiichiro Nakano  
Christopher Hesse  
John Schulman  
Note: Equal contribution. Correspondence to: Karl Cobbe <karl@openai.com>, Vineet Kosaraju <vineet@openai.com>
Affiliation: OpenAI

###### Abstract

State-of-the-art language models can match human performance on many tasks, but they still struggle to robustly perform multi-step mathematical reasoning. To diagnose the failures of current models and support research, we introduce GSM8K, a dataset of 8.5K high quality linguistically diverse grade school math word problems. We find that even the largest transformer models fail to achieve high test performance, despite the conceptual simplicity of this problem distribution. To increase performance, we propose training verifiers to judge the correctness of model completions. At test time, we generate many candidate solutions and select the one ranked highest by the verifier. We demonstrate that verification significantly improves performance on GSM8K, and we provide strong empirical evidence that verification scales more effectively with increased data than a finetuning baseline.

## 1 Introduction

In recent years, large language models have demonstrated impressive skills across many diverse tasks ([Wang et al., 2019](#bib.bib26), [Brown et al., 2020](#bib.bib2)). [Kaplan et al. (2020)](#bib.bib9) describe the consistent benefits of increasing model size, characterizing scaling trends that hold across many orders of magnitude. However, even the largest models falter when required to perform multi-step mathematical reasoning ([Hendrycks et al., 2021](#bib.bib6)). Model samples frequently contain catastrophic mistakes, even after the model has been appropriately finetuned. Mathematical reasoning thus reveals a critical weakness in modern language models.

One significant challenge in mathematical reasoning is the high sensitivity to individual mistakes ([Shen et al., 2021a](#bib.bib21)). When generating a solution, autoregressive models have no mechanism to correct their own errors. Solutions that veer off-course quickly become unrecoverable. If we rely purely on generative methods and extrapolate from current trends, we will require an exorbitant parameter count to achieve even moderate performance on distributions as challenging as the MATH dataset ([Hendrycks et al., 2021](#bib.bib6)). This evidence strongly motivates the search for methods with more favorable scaling laws.

We propose training verifiers to evaluate the correctness of model generated solutions, similar to concurrent work by [Shen et al. (2021a)](#bib.bib21). At test time, we sample a fixed number of candidate solutions and select the solution ranked highest by the verifier. Verifiers benefit both from their inherent optionality and from verification being a simpler task than generation in general.

To facilitate research, we are releasing GSM8K, a dataset of 8.5K high quality problems at the grade school math level. We designed this dataset to have high linguistic diversity while relying on relatively simple grade school math concepts. State-of-the-art language models struggle to achieve high performance on this dataset, primarily due to the high diversity among problems. At the same time, GSM8K solutions depend only on elementary concepts, so achieving high test performance is a tractable goal.

![Refer to caption](2110.14168v2/figures/example_problems.png)

Figure 1: Three example problems from GSM8K. Calculation annotations are highlighted in red.

Our main contributions are as follows:

1. 1.

   We present a curated dataset of 8.5K grade school math questions and natural language solutions, useful for probing the informal reasoning ability of large language models.
2. 2.

   We show that, compared to a finetuning baseline, the use of verifiers results in approximately the same performance boost as a 30x model size increase, and that verifiers scale significantly better with increased data.
3. 3.

   We show that dropout acts as a strong regularizer, significantly improving performance for both finetuning and verification.

## 2 Dataset

GSM8K consists of 8.5K high quality grade school math problems created by human problem writers. We segmented these into 7.5K training problems and 1K test problems. These problems take between 2 and 8 steps to solve, and solutions primarily involve performing a sequence of elementary calculations using basic arithmetic operations (+−×÷+-\times\div) to reach the final answer. A bright middle school student should be able to solve every problem.

We created GSM8K based on the following design principles.

- •

  High Quality We avoid error-prone scraping procedures and instead rely on human workers to create problems. After performing extensive quality control based on workers’ answer agreement, we estimate that less than 2 percent of problems contain breaking errors.
- •

  High Diversity We strive for high diversity among problems. We actively avoid designing problems that are drawn from the same linguistic template or differ only in superficial details, an issue that is prevalent among many other datasets. By creating each individual problem to be relatively unique, held-out test performance becomes a far more relevant metric.
- •

  Moderate Difficulty We choose a problem distribution that is challenging for large state-of-the-art language models, without being completely intractable. GSM8K will help us better understand the data scaling trends of different models and methods in this difficulty sweet spot. Problems require no concepts beyond the level of early Algebra, and the vast majority of problems can be solved without explicitly defining a variable.
- •

  Natural Language Solutions We collect solutions in natural language rather than as pure math expressions. We believe this is the most generally useful data format, and we expect it to shed light on the properties of large language models’ internal monologues. We instructed problem writers to explain their work as much as possible, but we allowed them to write solutions in their own diverse linguistic styles.

The full GSM8K dataset can be found at <https://github.com/openai/grade-school-math>. Example problems are shown in [Figure 1](#S1.F1 "In 1 Introduction ‣ Training Verifiers to Solve Math Word Problems"), and we discuss additional dataset details in [Appendix A](#A1 "Appendix A Dataset Details ‣ Training Verifiers to Solve Math Word Problems").

## 3 Related Work

### 3.1 Related Datasets

Early math word problem datasets ([Kushman et al., 2014](#bib.bib11), [Roy and Roth, 2015](#bib.bib20)) are relatively small and are not well suited for testing the limits of modern language models. Dolphin18K ([Huang et al., 2016](#bib.bib7)) is a larger dataset containing 18K problems, but solutions are provided only in the form of equations or final answers. AQuA-RAT ([Ling et al., 2017](#bib.bib15)) contains 100K problems, but this dataset unfortunately suffers from both a high degree of problem templatization and poor quality control of the natural language solutions. MathQA is a recently released subset of AQuA-RAT focused on correcting these mistakes ([Amini et al., 2019](#bib.bib1)), but even the corrected dataset has data quality issues, with around 30% of the data having inconsistencies ([Miao et al., 2021](#bib.bib17)). Ape210K ([Zhao et al., 2020](#bib.bib29)) is the largest publicly available dataset, consisting of 210K Chinese elementary school-level math problems. However, due to the language barrier and the lack of natural language solutions, we’re unable to evaluate our methods on this dataset.

The recently developed ASDiv dataset ([Miao et al., 2021](#bib.bib17)), which contains 2.3K math word problems, addresses common flaws in prior datasets by ensuring problems have both high diversity and high quality. We share those design principles in the creation of GSM8K. However, we note that GSM8K is larger, provides natural language solutions, and consists of problems that on average require more steps to solve. The MATH dataset ([Hendrycks et al., 2021](#bib.bib6)) is larger and significantly more complex than GSM8K, but the high difficulty makes it challenging to accurately measure progress given the current capabilities of state-of-the-art language models.

Other recent reasoning-related datasets have focused on mathematical reasoning on symbolic math ([Lample and Charton, 2019](#bib.bib12)), reading comprehension (LogiQA) ([Liu et al., 2020](#bib.bib16)), and commonsense question answering (CommonsenseQA) ([Talmor et al., 2018](#bib.bib24)). Similar to CommonsenseQA, GSM8K includes questions that require basic background knowledge, like the number of days in a week. Similar to LogiQA, which requires a mix of reading comprehension and logical reasoning, GSM8K’s main difficulty lies in both properly interpreting a question and reasoning through the steps to solve it.

### 3.2 Related Methods

Previous work has attempted to solve classic math word problem benchmarks with recurrent seq2seq models ([Sutskever et al., 2014](#bib.bib23)) and closely related variants ([Wang et al., 2017](#bib.bib27), [Huang et al., 2018](#bib.bib8)). More recent work has improved performance by designing specialized encoder-decoder architectures ([Amini et al., 2019](#bib.bib1), [Chiang and Chen, 2018](#bib.bib5), [Xie and Sun, 2019](#bib.bib28), [Chen et al., 2020](#bib.bib3), [Li et al., 2020](#bib.bib13)), with the strongest results often relying on large pretrained encoders from the BERT family ([Chen et al., 2019](#bib.bib4), [Kim et al., 2020](#bib.bib10), [Liang et al., 2021](#bib.bib14)).

Other recent work has recommended additional pretraining tasks to further improve the math reasoning skills of large transformer-based models. [Hendrycks et al. (2021)](#bib.bib6) propose pretraining models on a new AMPS corpus, derived from Khan Academy problems and Mathematica scripts. Similarly, [Shen et al. (2021b)](#bib.bib22) propose a pretrained a corpus of pre-K to college level curricula extracted from the internet, and [Peng et al. (2021)](#bib.bib19) propose pretraining by predicting masked subexpressions from expression trees.

Similar to verification, other methods have finetuned a language model to select among many model completions. [Nichols et al. (2020)](#bib.bib18) proposed a sample-and-rank approach to improve the collaborative storytelling ability of large language models, with the training signal coming from the preferences of human workers. In concurrent work closely related to our own, [Shen et al. (2021a)](#bib.bib21) applied a similar approach to solving math word problems, jointly training a model to both generate and rank solutions. Our work shares many fundamental similarities with their approach, though we differ in several key respects. First, we focus attention on the space of natural language solutions, as this is a richer and more general solution format than pure mathematical expressions. Moreover, this choice enables our models to develop verbal analytical skills and to produce solutions that are more readily interpretable by humans. Second, we provide evidence that verifiers scale far more favorably with additional data than baseline methods. Finally, we use separate generator and verifier networks, in order to prevent the generator from overfitting.

## 4 Methods

Figure 2: Final test performance for various GPT-3 model sizes after finetuning on training sets of different sizes. Mean and standard deviation is shown across 3 runs.

We investigate two methods to solve problems in GSM8K: finetuning and verification. Finetuning, our baseline method, uses the same language modeling objective as the generative pretraining in GPT-3 ([Brown et al., 2020](#bib.bib2)). At test time, we judge performance by autoregressively sampling a single low temperature solution and checking whether the final answer is correct. In contrast, verification consists of sampling multiple high temperature solutions, assigning each solution a score, and outputting the highest ranked solution. Verifiers are trained to judge the correctness of solutions, with the training signal determined solely by whether or not the solution reached the correct final answer.

For both methods, we use models from the GPT-3 family as our initialization, primarily focusing on the 175B and 6B model sizes. The 175B model is the largest and produces the most impressive results, while the 6B model is significantly more convenient for research purposes. We discuss hyperparameter choices in [Appendix B](#A2 "Appendix B Hyperparameters ‣ Training Verifiers to Solve Math Word Problems").

Our models frequently fail to accurately perform calculations. Although larger models make fewer arithmetic mistakes than smaller models, this remains a common source of errors. To mitigate this issue, we train all models to use a calculator by injecting calculation annotations into the training set. At test time, a calculator will override sampling when the model chooses to use these annotations. Details can be found in [Appendix C](#A3 "Appendix C Calculator Annotations ‣ Training Verifiers to Solve Math Word Problems").

Figure 3: Test solve rate after finetuning a 6B model on the full GSM8K training set, when the model is allowed to make 1 guess (left) or 100 guesses (right).

### 4.1 Finetuning

We perform finetuning by updating model parameters to minimize the cross-entropy loss over all training tokens. [Figure 2](#S4.F2 "In 4 Methods ‣ Training Verifiers to Solve Math Word Problems") shows test performance after finetuning on training sets of varying sizes for 20 epochs. We visualize the same data both as a function of training set size and as a function of model size. Test performance is determined by a single low temperature (T=0T=0) sample for each test problem. Unsurprisingly, we see that the 175B model significantly outperforms the smaller models. Assuming a log-linear trend, we can naively extrapolate these results to estimate that a model with 101610^{16} parameters would be required to reach an 80%80\% solve rate, when using the full GSM8K training set. It is even harder to extrapolate along the data dimension, since performance does not appear to follow a log-linear trend. Nevertheless, it appears likely that the 175B model would require at least two additional orders of magnitude of training data to reach an 80%80\% solve rate.

In [Figure 3](#S4.F3 "In 4 Methods ‣ Training Verifiers to Solve Math Word Problems"), we show how 6B test performance varies over the course of 100 training epochs. We use test@N to denote the percentage of problems solved correctly at least once when allowing the model to make N separate guesses for each problem. We use a low temperature (T=0T=0) to generate test@1 samples and we use a higher temperature (T=0.7T=0.7) to generate test@100 samples. Both temperature values were chosen empirically to produce the best results. Test@1 performance improves approximately monotonically, even though we quickly begin overfitting on test loss. Unfortunately, test@100 performance degrades much more sharply than test@1 as we increase the number of epochs. This is to be expected: as the model repeatedly encounters the same data, it becomes increasingly uncalibrated and overconfident in its predictions. At test time, this overconfidence leads to poor coverage of the solution space, an effect which only becomes noticeable when we are considering multiple samples at test time.

Choosing a model with good coverage is critical to successfully train verifiers. Empirically, we see that test@100 performance peaks within the first few epochs. For this reason, we use models trained for 2 epochs to generate samples for training verifiers. We provide several example solutions from 6B and 175B models in [Appendix D](#A4 "Appendix D Example Model Solutions ‣ Training Verifiers to Solve Math Word Problems"). We also note that it is important to allow the model to generate the full natural language solution before outputting a final answer. If we instead finetune a 6B model to directly output the final answer without any intermediate steps, performance drops drastically from 20.6% to 5.2%.

Figure 4: A diagram of the verification training pipeline.

![Refer to caption](2110.14168v2/figures/verifier_diagram.png)

### 4.2 Verification

To improve upon the finetuning baseline, we train verifiers to judge the correctness of model-generated solutions and search against these verifiers at test time. Conditioned on the problem and a candidate solution, the verifier outputs the probability that the solution is correct. Training solutions are labeled as correct or incorrect based solely on whether they reach the correct final answer. In practice, some solutions will reach the correct final answer using flawed reasoning, leading to false positives.

As shown in [Figure 4](#S4.F4 "In 4.1 Finetuning ‣ 4 Methods ‣ Training Verifiers to Solve Math Word Problems"), we train the verifier as follows:

1. 1.

   Finetune a model (the “generator”) for 2 epochs on the training set.
2. 2.

   Sample 100 completions from the generator for each training problem and label each solution as correct or incorrect.
3. 3.

   Train a verifier for a single epoch on this dataset.

Training for 2 epochs is enough for the generator to learn basic skills in this domain. We choose not to train for longer, since the diversity of generated solutions begins to collapse after this point, as shown in [Figure 3](#S4.F3 "In 4 Methods ‣ Training Verifiers to Solve Math Word Problems"). We train separate generator and verifier models to limit the generator’s training and prevent overfitting, but in principle, it should be possible to combine these models. Unless otherwise specified, we use the same model size for the generator and the verifier. In addition to predicting solution correctness, we also train the verifier with the same language modeling objective as the generator. This serves as a valuable auxiliary objective for the verifier. We discuss additional verifier training details in [Appendix E](#A5 "Appendix E Verifier Details ‣ Training Verifiers to Solve Math Word Problems").

Figure 5: A comparison between finetuning and verification using 6B and 175B model sizes. Verification considers 100 solutions per problem. Mean and standard deviation is shown across 3 runs, except for 175B verification which shows only a single run.

At test time, we sample 100 completions to each test problem, rank them with the verifier, and then return the one with the highest verifier score. A comparison between verification and finetuning is shown in [Figure 5](#S4.F5 "In 4.2 Verification ‣ 4 Methods ‣ Training Verifiers to Solve Math Word Problems") for both the 6B and 175B model sizes. We find that it is not beneficial to use verification at low dataset sizes. We believe this is due to the pressure to overfit to the correct answer: with small datasets, overfitting to the correct answer happens faster than learning more generalizable properties of correct reasoning. However, once we use a sufficiently large dataset, we see a strong boost from verifiers. It’s interesting to note that the 175B verifiers “take off” earlier than the 6B verifiers, requiring fewer training problems to surpass the finetuning baseline. See [Appendix D](#A4 "Appendix D Example Model Solutions ‣ Training Verifiers to Solve Math Word Problems") for example solutions found by verifiers and [Appendix F](#A6 "Appendix F Verifier Visualization ‣ Training Verifiers to Solve Math Word Problems") for a visualization of verifier confidence.

(a) Comparison between a verifier trained to predict correctness after every token (token-level) and one trained to predict correctness after only the final token (solution-level)

(b) Comparison between a verifier trained jointly to predict correctness and perform language modeling (joint) and one trained only to predict correctness (verification-only)

(c) Performance when varying the size of the generator and the verifier in isolation. Increasing the size of the generator has a larger impact than increasing the size of the verifier.

Figure 6: Verification ablations

### 4.3 Verification Ablations

We can either train verifiers to make a single scalar prediction conditioned on the entire generated solution, or to make a scalar prediction after each token in the solution. By default, we choose the latter, training verifiers to make predictions after each token. This can be viewed as a token-level value function. We compare these two methods in [Figure 6(a)](#S4.F6.sf1 "In Figure 6 ‣ 4.2 Verification ‣ 4 Methods ‣ Training Verifiers to Solve Math Word Problems"), respectively labeled “solution-level” and “token-level”.

Predicting the value function at every token is a more challenging and noisier task than judging only the full completion. However, despite the initially slower training, the token-level verifier ultimately outperforms the solution-level verifier. Moreover, the token-level verifier is still improving late in training, whereas the solution-level verifier quickly shows signs of overfitting. We hypothesize that the full value function provides a useful auxiliary signal that encourages the model to judge the reasoning throughout solutions, rather than merely memorizing the correct final answer.

In [Figure 6(b)](#S4.F6.sf2 "In Figure 6 ‣ 4.2 Verification ‣ 4 Methods ‣ Training Verifiers to Solve Math Word Problems"), we ablate the objective used when training verifiers. As discussed in [Section 4.2](#S4.SS2 "4.2 Verification ‣ 4 Methods ‣ Training Verifiers to Solve Math Word Problems"), we can optionally include a language modeling objective alongside the verification objective. We compare using both objectives to using only the verification objective. Although both are reasonable choices, including the language modeling objective is a strict improvement. This makes intuitive sense: better understanding this language distribution should only aid the verifier in discriminating between samples.

In [Figure 6(c)](#S4.F6.sf3 "In Figure 6 ‣ 4.2 Verification ‣ 4 Methods ‣ Training Verifiers to Solve Math Word Problems"), we separately ablate the model size of the generator and the verifier. We find that using a large generator with a small verifier performs significantly better than using a small generator with a large verifier. Verification is still remarkably effective, even when the verifier is much smaller than the generator. This suggests that the verifier may often be relying on relatively coarse heuristics to discriminate between solutions from a given generator, rather than attempting a more thorough form of verification.

(a) 6B verification test performance when given varying numbers of completions per problem to rank.

(b) 6B verification test performance when varying the number of top ranked samples allowed to vote on the answer.

Figure 7: Performance as the amount of test time compute varies.

## 5 Additional Experiments

### 5.1 Test Time Compute

At test time, we can choose to generate arbitrarily many solutions to be judged by the verifier before selecting the highest ranked completion. [Figure 7(a)](#S4.F7.sf1 "In Figure 7 ‣ 4.3 Verification Ablations ‣ 4 Methods ‣ Training Verifiers to Solve Math Word Problems") shows how 6B verifier performance varies with the number of completions per test problem. At this scale, performance improves as we increase the number of completions up to 400. Beyond this point, performance start to decrease. This suggests that the benefits of search are eventually outweighed by the risk of finding adversarial solutions that fool the verifier. In general, we evaluate verifier test performance using 100 completions, since this captures most of the benefits of verification with a relatively modest compute cost.

To further increase performance, we can take a majority vote among the top verifier-ranked solutions instead of selecting only the single top solution. This voting process considers only the final answer reached by the individual solutions: the final answer selected is the one with the most votes. [Figure 7(b)](#S4.F7.sf2 "In Figure 7 ‣ 4.3 Verification Ablations ‣ 4 Methods ‣ Training Verifiers to Solve Math Word Problems") shows how performance varies as we allow a greater number of top samples to cast a vote. Unsurprisingly, when starting with a greater number of samples, we can afford to allow a greater number of samples to cast a vote. When we have only 100 samples, it is optimal to allow only the top 3-5 samples to cast a vote. When we have 3200 samples, it is approximately optimal to allow the top 30 to cast a vote.

### 5.2 Regularization

(a) Finetuning

(b) Solution-level verifiers

(c) Token-level verifiers

Figure 8: 6B finetuning and verification dropout ablations.

We find that both finetuning and verification strongly benefit from the use of dropout as a regularizer. Specifically, we apply residual dropout ([Vaswani et al., 2017](#bib.bib25)) along the residual paths of each layer in the network. We use 20% dropout for all dropout experiments, chosen based on the results of a hyperparameters sweep. We note that GPT-3 models are not pretrained with dropout. For experiments involving dropout, we therefore perform additional pretraining with dropout before subsequently finetuning the models. This mitigates the distribution shift the model experiences during finetuning.

We first investigate the effect of dropout on finetuning across various training set sizes. [Figure 8(a)](#S5.F8.sf1 "In Figure 8 ‣ 5.2 Regularization ‣ 5 Additional Experiments ‣ Training Verifiers to Solve Math Word Problems") shows that dropout leads to a significant improvement over baseline. We next investigate the effect of dropout on verifiers, considering both the solution-level and token-level variants. In [Figure 8(b)](#S5.F8.sf2 "In Figure 8 ‣ 5.2 Regularization ‣ 5 Additional Experiments ‣ Training Verifiers to Solve Math Word Problems"), we see that dropout significantly improves solution-level verifiers, mitigating the overfitting that occurs in the unregularized baseline. Notably, using dropout with solution-level verifiers reaches a similar level of performance as token-level verifiers. In [Figure 8(c)](#S5.F8.sf3 "In Figure 8 ‣ 5.2 Regularization ‣ 5 Additional Experiments ‣ Training Verifiers to Solve Math Word Problems"), we apply dropout to token-level verifiers. Since token-level verifiers are already less susceptible to overfitting, it is no surprise that the impact of dropout is less significant. Nevertheless, we do still see a slight gain from training token-level verifiers with dropout. Note that we increase the batch size for token-level verifiers by a factor of 4, to better handle the more difficult objective and the noise from dropout.

## 6 Conclusion

We have seen that verification provides a significant performance boost relative to a finetuning baseline. On the full dataset, 6B verification slightly outperforms a finetuned 175B model, thereby offering a boost approximately equivalent to a 30x model size increase. We have also seen that token-level verifiers are less prone to overfitting than solution-level verifiers, and that all methods benefit from regularization with residual dropout. We expect verification to scale well to problem distributions that require more complex mathematical reasoning, and we hope GSM8K supports the development of new methods that scale even better.

## Acknowledgements

We thank Dan Hendrycks, Leo Gao, Alec Radford, and Giambattista Parascandolo for their valuable feedback on this paper; Harri Edwards, Yura Burda, Michael Wu, and Nick Ryder for many insightful conversations; Michael Petrov, Alethea Power, and Jacob Jackson for their technical assistance; the OpenAI Supercomputing team for the infrastructure that made these experiments possible; and the team at Surge AI for performing the GSM8K data collection.

## References

- Amini et al. (2019)

  A. Amini, S. Gabriel, P. Lin, R. Koncel-Kedziorski, Y. Choi, and H. Hajishirzi.
  Mathqa: Towards interpretable math word problem solving with
  operation-based formalisms.
  *arXiv preprint arXiv:1905.13319*, 2019.
- Brown et al. (2020)

  T. B. Brown, B. Mann, N. Ryder, M. Subbiah, J. Kaplan, P. Dhariwal,
  A. Neelakantan, P. Shyam, G. Sastry, A. Askell, et al.
  Language models are few-shot learners.
  *arXiv preprint arXiv:2005.14165*, 2020.
- Chen et al. (2020)

  K. Chen, Q. Huang, H. Palangi, P. Smolensky, K. D. Forbus, and J. Gao.
  Mapping natural-language problems to formal-language solutions using
  structured neural representations.
  In *ICML*, 2020.
- Chen et al. (2019)

  X. Chen, C. Liang, A. W. Yu, D. Zhou, D. Song, and Q. V. Le.
  Neural symbolic reader: Scalable integration of distributed and
  symbolic representations for reading comprehension.
  In *International Conference on Learning Representations*, 2019.
- Chiang and Chen (2018)

  T.-R. Chiang and Y.-N. Chen.
  Semantically-aligned equation generation for solving and reasoning
  math word problems.
  *arXiv preprint arXiv:1811.00720*, 2018.
- Hendrycks et al. (2021)

  D. Hendrycks, C. Burns, S. Kadavath, A. Arora, S. Basart, E. Tang, D. Song, and
  J. Steinhardt.
  Measuring mathematical problem solving with the math dataset.
  *arXiv preprint arXiv:2103.03874*, 2021.
- Huang et al. (2016)

  D. Huang, S. Shi, C.-Y. Lin, J. Yin, and W.-Y. Ma.
  How well do computers solve math word problems? large-scale dataset
  construction and evaluation.
  In *Proceedings of the 54th Annual Meeting of the Association
  for Computational Linguistics (Volume 1: Long Papers)*, pages 887–896, 2016.
- Huang et al. (2018)

  D. Huang, J. Liu, C.-Y. Lin, and J. Yin.
  Neural math word problem solver with reinforcement learning.
  In *Proceedings of the 27th International Conference on
  Computational Linguistics*, pages 213–223, 2018.
- Kaplan et al. (2020)

  J. Kaplan, S. McCandlish, T. Henighan, T. B. Brown, B. Chess, R. Child,
  S. Gray, A. Radford, J. Wu, and D. Amodei.
  Scaling laws for neural language models.
  *arXiv preprint arXiv:2001.08361*, 2020.
- Kim et al. (2020)

  B. Kim, K. S. Ki, D. Lee, and G. Gweon.
  Point to the expression: Solving algebraic word problems using the
  expression-pointer transformer model.
  In *Proceedings of the 2020 Conference on Empirical Methods in
  Natural Language Processing (EMNLP)*, pages 3768–3779, 2020.
- Kushman et al. (2014)

  N. Kushman, Y. Artzi, L. Zettlemoyer, and R. Barzilay.
  Learning to automatically solve algebra word problems.
  In *Proceedings of the 52nd Annual Meeting of the Association
  for Computational Linguistics (Volume 1: Long Papers)*, pages 271–281, 2014.
- Lample and Charton (2019)

  G. Lample and F. Charton.
  Deep learning for symbolic mathematics.
  *arXiv preprint arXiv:1912.01412*, 2019.
- Li et al. (2020)

  S. Li, L. Wu, S. Feng, F. Xu, F. Xu, and S. Zhong.
  Graph-to-tree neural networks for learning structured input-output
  translation with applications to semantic parsing and math word problem.
  *EMNLP*, 2020.
- Liang et al. (2021)

  Z. Liang, J. Zhang, J. Shao, and X. Zhang.
  Mwp-bert: A strong baseline for math word problems, 07 2021.
- Ling et al. (2017)

  W. Ling, D. Yogatama, C. Dyer, and P. Blunsom.
  Program induction by rationale generation: Learning to solve and
  explain algebraic word problems.
  *arXiv preprint arXiv:1705.04146*, 2017.
- Liu et al. (2020)

  J. Liu, L. Cui, H. Liu, D. Huang, Y. Wang, and Y. Zhang.
  Logiqa: A challenge dataset for machine reading comprehension with
  logical reasoning.
  In *IJCAI*, 2020.
- Miao et al. (2021)

  S.-Y. Miao, C.-C. Liang, and K.-Y. Su.
  A diverse corpus for evaluating and developing english math word
  problem solvers.
  *arXiv preprint arXiv:2106.15772*, 2021.
- Nichols et al. (2020)

  E. Nichols, L. Gao, and R. Gomez.
  Collaborative storytelling with large-scale neural language models.
  *arXiv preprint arXiv:2011.10208*, 2020.
- Peng et al. (2021)

  S. Peng, K. Yuan, L. Gao, and Z. Tang.
  Mathbert: A pre-trained model for mathematical formula understanding.
  *ArXiv*, abs/2105.00377, 2021.
- Roy and Roth (2015)

  S. Roy and D. Roth.
  Solving general arithmetic word problems.
  In *Proceedings of the 2015 Conference on Empirical Methods in
  Natural Language Processing*, pages 1743–1752, Lisbon, Portugal, Sept. 2015.
  Association for Computational Linguistics.
  doi: 10.18653/v1/D15-1202.
  URL <https://aclanthology.org/D15-1202>.
- Shen et al. (2021a)

  J. Shen, Y. Yin, L. Li, L. Shang, X. Jiang, M. Zhang, and Q. Liu.
  Generate & rank: A multi-task framework for math word problems.
  *arXiv preprint arXiv:2109.03034*, 2021a.
- Shen et al. (2021b)

  J. T. Shen, M. Yamashita, E. Prihar, N. Heffernan, X. Wu, B. Graff, and D. Lee.
  Mathbert: A pre-trained language model for general nlp tasks in
  mathematics education, 08 2021b.
- Sutskever et al. (2014)

  I. Sutskever, O. Vinyals, and Q. V. Le.
  Sequence to sequence learning with neural networks.
  In *Advances in neural information processing systems*, pages
  3104–3112, 2014.
- Talmor et al. (2018)

  A. Talmor, J. Herzig, N. Lourie, and J. Berant.
  Commonsenseqa: A question answering challenge targeting commonsense
  knowledge.
  *arXiv preprint arXiv:1811.00937*, 2018.
- Vaswani et al. (2017)

  A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez,
  Ł. Kaiser, and I. Polosukhin.
  Attention is all you need.
  In *Advances in neural information processing systems*, pages
  5998–6008, 2017.
- Wang et al. (2019)

  A. Wang, Y. Pruksachatkun, N. Nangia, A. Singh, J. Michael, F. Hill, O. Levy,
  and S. R. Bowman.
  Superglue: A stickier benchmark for general-purpose language
  understanding systems.
  *arXiv preprint arXiv:1905.00537*, 2019.
- Wang et al. (2017)

  Y. Wang, X. Liu, and S. Shi.
  Deep neural solver for math word problems.
  In *Proceedings of the 2017 Conference on Empirical Methods in
  Natural Language Processing*, pages 845–854, Copenhagen, Denmark, Sept.
  2017. Association for Computational Linguistics.
  doi: 10.18653/v1/D17-1088.
  URL <https://aclanthology.org/D17-1088>.
- Xie and Sun (2019)

  Z. Xie and S. Sun.
  A goal-driven tree-structured neural model for math word problems.
  In *IJCAI*, 2019.
- Zhao et al. (2020)

  W. Zhao, M. Shang, Y. Liu, L. Wang, and J. Liu.
  Ape210k: A large-scale and template-rich dataset of math word
  problems.
  *arXiv preprint arXiv:2009.11506*, 2020.

## Appendix A Dataset Details

We initially collected a starting set of a thousand problems and natural language solutions by hiring freelance contractors on Upwork ([upwork.com](https://upwork.com)). We then worked with Surge AI ([surgehq.ai](https://surgehq.ai)), an NLP data labeling platform, to scale up our data collection. After collecting the full dataset, we asked workers to re-solve all problems, with no workers re-solving problems they originally wrote. We checked whether their final answers agreed with the original solutions, and any problems that produced disagreements were either repaired or discarded. We then performed another round of agreement checks on a smaller subset of problems, finding that 1.7% of problems still produce disagreements among contractors. We estimate this to be the fraction of problems that contain breaking errors or ambiguities. It is possible that a larger percentage of problems contain subtle errors.

To assist contractors with writing questions, we provided seed questions automatically generated from a few-shot prompted 175B GPT-3 model. Contractors were allowed to use those seed questions directly, to use them as inspiration and make modifications, or to come up with their own questions entirely. We instructed contractors to be as descriptive as possible in their solutions, and to not re-use problem settings or templates between different questions. To ensure contractors were not re-using problem templates, we computed pairwise similarity scores between problems and used this to provide feedback to contractors.

## Appendix B Hyperparameters

We include a table of important hyperparameters below. We performed sweeps of the learning rate and batch size by an order of magnitude in both directions from the values in the table and were unable to find any significant improvements. Other reasonable choices for both the verifier temperature (eg: 1.0 instead of 0.7) and objective (cross-entropy instead of mean squared error) also had negligible effect in our ablations.

|  |  |
| --- | --- |
| General Hyperparameters | Value |
| Batch Size | 3.2×1043.2\times 10^{4} tokens |
| Max Sample Length | 400 tokens |
| Tokenization | reversible_50000 |
| Optimizer | Adam, β1=0.9\beta_{1}=0.9, β2=0.95\beta_{2}=0.95 |
| Dropout | 0.00.0 |
| Learning Rate Schedule | Linear decay to 0 |
| Finetuning Hyperparameters | Value |
| Epochs | 20 |
| Sampling Temperature | 0 (argmax) |
| Base Learning Rate (α\alpha) | 1.6×10−51.6\times 10^{-5} (3B) |
|  | 1.2×10−51.2\times 10^{-5} (6B) |
|  | 1.0×10−51.0\times 10^{-5} (12B) |
|  | 6.0×10−66.0\times 10^{-6} (175B) |
| Learning Rate | 0.1×α0.1\times\alpha |
| Verification Hyperparameters | Value |
| Epochs | 2 for generator, 1 for verifier |
| Sampling Temperature | 0.70.7 |
| Learning Rate | 1.0×10−51.0\times 10^{-5} |
| Loss weight | 1.01.0 |
| Verifier loss | MSE |
| Completions per train problem | 100 |
| Completions per test problem | 100 |

Table 1: Hyperparameters used for all experiments, unless explicitly said otherwise. Notable exceptions include Figure [8(c)](#S5.F8.sf3 "Figure 8(c) ‣ Figure 8 ‣ 5.2 Regularization ‣ 5 Additional Experiments ‣ Training Verifiers to Solve Math Word Problems"), which uses 4x more tokens per batch and 300 completions at both training and test time. All dropout experiments in Figure [8](#S5.F8 "Figure 8 ‣ 5.2 Regularization ‣ 5 Additional Experiments ‣ Training Verifiers to Solve Math Word Problems") use 20% dropout. Figure [7(a)](#S4.F7.sf1 "Figure 7(a) ‣ Figure 7 ‣ 4.3 Verification Ablations ‣ 4 Methods ‣ Training Verifiers to Solve Math Word Problems") uses verifiers trained on 100 completions, but searching over more completions at test time.

## Appendix C Calculator Annotations

The calculator annotations were not provided by human contractors: they were generated by a combination of hard-coded logic and a finetuned language model. The logic for auto-generating calculator annotations is imperfect. It is highly unlikely to generate any incorrect annotations, but it is not uncommon for it to ignore some lines that could be annotated.

During training, there is no special distinction between the annotated tokens and the rest of the solution: they are all just tokens. During testing, we override model sampling when a well-formatted annotation exists, specifically overwriting the token(s) directly following “=” and within <<…>>.

To simulate the calculator, we simply use the python eval function to evaluate the tokens in the expression (Figure [9](#A3.F9 "Figure 9 ‣ Appendix C Calculator Annotations ‣ Training Verifiers to Solve Math Word Problems")). Evaluations that time out or throw an error result in the annotations being skipped and the model being sampled from as usual.

We note that the original version of our calculator, used for all results in this paper, had some minor implementation bugs. Our reported test performance is therefore a slight underestimate, though the magnitude of this discrepancy is less than 1% in most experiments. Fixing the calculator improves verification test performance by about 1% when using the full GSM8K training set.

Figure 9: A diagram of the calculator sampling procedure.

## Appendix D Example Model Solutions

We showcase a handful of samples comparing finetuning and verification at both 6B and 175B scale. Samples were slightly cherry-picked for diversity.

![[Uncaptioned image]](2110.14168v2/figures/example_solutions_1.png)

![[Uncaptioned image]](2110.14168v2/figures/example_solutions_3.png)

![[Uncaptioned image]](2110.14168v2/figures/example_solutions_2.png)

![[Uncaptioned image]](2110.14168v2/figures/example_solutions_4.png)

![[Uncaptioned image]](2110.14168v2/figures/example_solutions_5.png)

![[Uncaptioned image]](2110.14168v2/figures/example_solutions_8.png)

![[Uncaptioned image]](2110.14168v2/figures/example_solutions_7.png)

![[Uncaptioned image]](2110.14168v2/figures/example_solutions_6.png)

## Appendix E Verifier Details

As noted in section [4.2](#S4.SS2 "4.2 Verification ‣ 4 Methods ‣ Training Verifiers to Solve Math Word Problems"), we train verifiers with a joint objective where the model learns to label a model completion as correct or incorrect, in addition to the original language modeling objective. Architecturally, this means our verifiers are language models, with a small scalar head that outputs predictions on a per-token basis.

We implement this scalar head as a single bias parameter and single gain parameter that operate on the logits outputted by the language model’s final unembedding layer. Specifically, the bias and gain shift and scale the logit corresponding to a special token in the vocabulary. As such, the logits for other tokens can continue to represent the language modeling objective, while this special token is reserved for the verifier’s predictions.

We can choose to initialize the verifier from the same pretrained language model the generator was finetuned from, or from the generator itself. In our ablations the latter performed slightly better; we suspect this is because better understanding the language distribution that the generator learned should only aid the verifier in scoring samples from that distribution. Unless otherwise explicitly stated, we initialize our verifiers from their corresponding generators in all experiments.

When training verifiers with the joint objective, we use an equal mix of language data and verifier data. Because we sample 100 completions for each original training example to generate the verifier data, using an equal mix means we effectively upsample the original language data by a factor of 100. To form the joint objective, we simply add the verifier loss and language modeling loss unweighted, and define an epoch of this joint objective as having seen each verifier example once. With both objectives, we mask out tokens in the question and only train on tokens in the solutions, as visualized in Figure [12](#A5.F12 "Figure 12 ‣ Appendix E Verifier Details ‣ Training Verifiers to Solve Math Word Problems").

Figure 12: Visualization of the joint training objective. We mask out tokens in the question and only consider the loss corresponding to tokens in the solution.

## Appendix F Verifier Visualization

![Refer to caption](2110.14168v2/vf_viz_cherrypicked.png)

Figure 13: Five cherry-picked samples generated by a 175B finetuned model and scored by a 175B token-level verifier. A green background color indicates a high verifier score, and a red background color indicates a low one.

One benefit of the token-level verifiers is that these models become immediately interpretable: we can visualize the predicted value for each token and better understand how the verifier makes decisions on judging samples. Above we present a visualization of the predicted values for five different cherry-picked questions and model completions, verified by a 175B token-level verifier that was trained on the full training set.

In the visualization, the background color of the text corresponds to the verifier score for that token, where red is low value (predicted incorrect) and green is high value (predicted correct). The second column of the table summarizes the verifier’s prediction, and the third column indicates whether the generated model completion was actually correct or incorrect. Any disagreement between the second and third columns indicates that the verifier made an error.

The first row includes a true positive example, where the verifier correctly classifies the completion as correct. Note that the model is initially unsure about whether the solution is correct and gradually gains certainty as the solution progresses: this is likely a property of the verifier training procedure, where it trains on a large fraction of incorrect model-generated samples.

The second row contains a problem where the solution is correct, but the verifier has rated it as incorrect. This is potentially due to the ambiguity between the “4 times” and the “4 potatoes” in the problem description.

The third row consists of another false negative example. However, unlike the previous example, here the model completion contains some faulty reasoning. As such, even though the final answer in the model completion was correct, the natural language explanation was incorrect, and so the verifier correctly assigned a low score.

In the fourth row we see the verifier score a model completion that starts out correct, but where the verifier gradually becomes less confident in the solution as the solution progresses. After the solution makes a clear mistake (saying that $64 dollars were spent, instead of the 64+16+8=$8864+16+8=\$88), the verifier judges the solution as incorrect with a high degree of confidence.

The final row contains a false positive, where the model makes a mistake on the second step, where it subtracts 400 from the price of a diamond jewel instead of a gold one. Verifiers occasionally make mistakes with performing this variable binding of quantities to their relationships.

*
