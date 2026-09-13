---
title: "VibeThinker-3B Post-Training Notes"
source: https://sebastianraschka.com/blog/2026/vibethinker-3b-post-training.html
crawled: 2026-09-06
---

# VibeThinker-3B Post-Training Notes

According to the reported benchmarks, [VibeThinker-3B](https://huggingface.co/WeiboAI/VibeThinker-3B) gets surprisingly close to much larger models on competition math and coding tasks. It reaches 94.3 on AIME 2026, 80.2 on LiveCodeBench v6, and 76.4 on IMO-AnswerBench. These are impressive numbers for a dense 3B-parameter model.

The architecture is the least surprising part. VibeThinker-3B starts from [Qwen2.5-Coder-3B](https://huggingface.co/Qwen/Qwen2.5-Coder-3B), and its [configuration](https://huggingface.co/WeiboAI/VibeThinker-3B/blob/main/config.json) retains the standard Qwen2-style decoder. It has 36 transformer blocks, a 2,048-dimensional embedding space, and an 11,008-dimensional feed-forward hidden layer. The attention layers use 16 query heads and 2 key-value heads, which gives an 8:1 grouped-query attention ratio. The configured [context length](https://sebastianraschka.com/glossary/#context-length "Context Length") is 131,072 tokens.

The interesting part is the post-training recipe described in the [technical report](https://arxiv.org/abs/2606.16140). It combines data synthesis, two [supervised finetuning](https://sebastianraschka.com/glossary/#instruction-finetuning "Instruction Finetuning (SFT)") stages, several reinforcement-learning stages, offline self-distillation, and a final instruction-tuning pass.

## Two supervised finetuning stages

The supervised data spans math, code, STEM, general chat, and instruction following. For math and code, the authors begin with problems that have checkable answers or executable tests. They expand these seed problems, sample several solutions from teacher models, and use majority voting to construct pseudo-labels. Multiple valid reasoning paths are kept for the same problem.

There is a substantial filtering step after synthesis. The pipeline removes repetitive generations and overlaps with evaluation sets, rejects poorly formed questions, checks final answers, and executes code in a sandbox. This part matters because [verifier](https://sebastianraschka.com/glossary/#verifier "Verifier")-driven RL is only as useful as the prompts and reward checks that feed it.

The first SFT stage trains on the full filtered mixture for broad coverage. The second stage uses a much narrower subset. The authors discard reasoning traces shorter than 5,000 tokens. They also run VibeThinker-1.5B eight times per problem and remove relatively easy questions with an error rate below 75%. In other words, the second stage concentrates on examples that are both long and difficult for the reference model.

Checkpoint selection is also unusual. Instead of choosing one checkpoint from validation loss, the authors measure Pass@K on domain-specific probe sets. They select checkpoints that produce a wider set of valid solutions for each domain and merge these specialist checkpoints at the parameter level.

## Reinforcement learning near the capability boundary

VibeThinker-3B uses MaxEnt-Guided Policy Optimization, or MGPO. It is a [GRPO](https://sebastianraschka.com/glossary/#grpo "GRPO (Group Relative Policy Optimization)")-style method carried over from the earlier VibeThinker-1.5B work.

The main idea is intuitive. Suppose the model samples several answers for one prompt. A prompt with almost no correct answers may be too hard to provide a useful learning signal. A prompt that is almost always solved has little left to teach. MGPO assigns more weight to prompts near 50% group accuracy, where successful and unsuccessful attempts coexist.

The RL data covers math, code, and STEM. Each domain uses a suitable verifier: final-answer checking for math, sandboxed tests for code, and answer or option matching for STEM. The stages run sequentially in the order math, code, and STEM. All three use on-policy sampling.

Another practical detail is the context window. The earlier 1.5B work expanded the context length over multiple stages. For this model, the authors found that early truncation damaged long reasoning traces and that the model did not fully recover later. They therefore ran RL directly with a single 64K-token context window.

The math stage ends with a Long2Short phase. Rewards among correct responses are adjusted slightly in favor of shorter solutions, while rewards for incorrect solutions stay unchanged. This encourages more concise reasoning after the accuracy-oriented stage has already learned to solve the problems.

## Distilling the RL checkpoints

Sequential domain training creates another issue. A later checkpoint can lose useful behavior from an earlier stage. The authors address this with offline self-[distillation](https://sebastianraschka.com/glossary/#distillation "Distillation"). They collect verified trajectories from the math, code, and STEM checkpoints, then finetune one student model on the filtered mixture.

Their filtering score favors a correct trace when the student still assigns it a relatively low likelihood. This is a sensible way to spend distillation capacity. A correct solution that the student already predicts easily contains less new information than one it has not absorbed yet.

The last step is instruction RL. Rule-based validators score prompts with explicit format, ordering, item-count, and keyword constraints. Rubric-based reward models handle more open-ended prompts. The reported 93.4 on IFEval suggests that the long reasoning pipeline did not erase instruction-following ability.

## How I read the [benchmark](https://sebastianraschka.com/glossary/#benchmark "Benchmark") results

The numbers are provider-reported and should be read with their evaluation protocol in mind. The authors use [temperature](https://sebastianraschka.com/glossary/#temperature "Temperature") 1.0 and average repeated samples: 64 generations for most math benchmarks, 8 for coding, and 16 for knowledge tasks. Scores for comparison models come from released reports, public leaderboards, or official evaluation records rather than one shared evaluation harness.

The higher scores labeled CLR use additional [test-time compute](https://sebastianraschka.com/glossary/#reasoning-model "Reasoning Model"). For each problem, Claim-Level Reliability Assessment generates 32 candidate trajectories, extracts five decision-relevant claims from each one, and asks the model to verify those claims. It then aggregates answers using the resulting reliability scores. For example, the reported AIME 2026 score rises from 94.3 to 97.1 with CLR. I would keep that result separate from the ordinary Pass@1 number.

There are also limits to the broad “frontier-level” description. VibeThinker-3B scores 70.2 on GPQA-Diamond, where several larger models in the report score above 80. The [model card](https://huggingface.co/WeiboAI/VibeThinker-3B) recommends the model for verifiable math, coding, and STEM tasks. It explicitly says that the model was not trained for [tool calling](https://sebastianraschka.com/glossary/#tool-use "Tool Use") or agentic programming.

Finally, the report does not disclose total GPU hours or a complete cost breakdown. It also does not provide controlled ablations for every pipeline stage. We can see the final outcome and understand the recipe, but we cannot assign a precise share of the gain to MGPO, Long2Short RL, self-distillation, or the synthetic data. The familiar Qwen2.5-Coder backbone still makes this a useful case study in how far careful post-training can push a small model on tasks with reliable verification.

[![VibeThinker-3B benchmark, architecture, and post-training overview](https://sebastianraschka.com/images/blog/2026/vibethinker-3b/hero.webp)](https://substack.com/@rasbt/note/c-277879621)

Figure 1: The left panel shows selected provider-reported math scores, including the extra CLR test-time scaling results. The upper-right panel summarizes the familiar Qwen2.5-Coder-style architecture. The lower panel traces the post-training stages from curriculum SFT through reasoning RL, offline self-distillation, and instruction RL.

Sources: expanded website version of my [Substack note](https://substack.com/@rasbt/note/c-277879621), based on the [VibeThinker-3B technical report](https://arxiv.org/abs/2606.16140), [model card](https://huggingface.co/WeiboAI/VibeThinker-3B), and [model configuration](https://huggingface.co/WeiboAI/VibeThinker-3B/blob/main/config.json).
