---
title: "LLMs From Scratch at 100,000 GitHub Stars"
source: https://sebastianraschka.com/blog/2026/llms-from-scratch-reaches-100000-github-stars.html
crawled: 2026-09-06
---

# LLMs From Scratch at 100,000 GitHub Stars

Just saw that the [LLMs-from-scratch repository](https://github.com/rasbt/LLMs-from-scratch) passed 100,000 stars on GitHub!

This is super cool and motivating. I am really happy to see that this open-source repo has helped so many people.

Thanks also to everyone who shared ideas and opened PRs with improvements!

Of course, I plan to keep adding new material, including new attention variants and architectures (while bigger projects like RL and Reasoning From Scratch live in their separate repositories).

I am also currently working on a larger applied custom “small” LLM project. It has been keeping me super busy this month, but I will share more on that soon in an upcoming Substack mega-article! It’s my longest one yet!

If you are new to it, some of the highlights in the repo include

1. Of course, the complete code path from [tokenization](https://github.com/rasbt/LLMs-from-scratch/blob/main/ch02/01_main-chapter-code/ch02.ipynb) and [attention](https://github.com/rasbt/LLMs-from-scratch/blob/main/ch03/01_main-chapter-code/ch03.ipynb) to [pretraining](https://github.com/rasbt/LLMs-from-scratch/blob/main/ch05/01_main-chapter-code/ch05.ipynb), [classification](https://github.com/rasbt/LLMs-from-scratch/blob/main/ch06/01_main-chapter-code/ch06.ipynb), and [instruction fine-tuning](https://github.com/rasbt/LLMs-from-scratch/blob/main/ch07/01_main-chapter-code/ch07.ipynb), etc. All of it FROM SCRATCH, of course! (RL lives in a companion repo.)
2. From-scratch implementations of [Llama](https://github.com/rasbt/LLMs-from-scratch/blob/main/ch05/07_gpt_to_llama/standalone-llama32.ipynb), [Qwen](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch05/11_qwen3), [Gemma](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch05/12_gemma3), and [Olmo](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch05/13_olmo3) (smaller variants that run locally and can be plugged into the training scripts).
3. From-scratch implementations of attention alternatives and other architecture components, such as [GQA](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04/04_gqa), [MLA](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04/05_mla), [sliding-window attention](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04/06_swa), [Gated DeltaNet](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04/08_deltanet), [DeepSeek Sparse Attention](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04/09_dsa), [cross-layer KV sharing](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04/10_kv-sharing), and [mixture-of-experts](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04/07_moe)
4. Materials on [KV caching](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04/03_kv-cache), [training performance](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch05/10_llm-training-speed), [memory-efficient weight loading](https://github.com/rasbt/LLMs-from-scratch/blob/main/ch05/08_memory_efficient_weight_loading/memory-efficient-state-dict.ipynb), [DPO](https://github.com/rasbt/LLMs-from-scratch/blob/main/ch07/04_preference-tuning-with-dpo/dpo-from-scratch.ipynb), [evaluation](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch07/03_model-evaluation), and [LoRA](https://github.com/rasbt/LLMs-from-scratch/blob/main/appendix-E/01_main-chapter-code/appendix-E.ipynb)

So, if you don’t have any weekend plans yet, happy tinkering!

[![Collage showing the LLMs-from-scratch GitHub repository at 101,000 stars and diagrams of attention mechanisms and memory benchmarks](https://sebastianraschka.com/images/blog/2026/llms-from-scratch-100k-stars/hero.webp)](https://substack.com/@rasbt/note/c-310007138)

[Figures from the LLMs-from-scratch repo](https://github.com/rasbt/LLMs-from-scratch).

Source: website version of my [Substack note](https://substack.com/@rasbt/note/c-310007138).
