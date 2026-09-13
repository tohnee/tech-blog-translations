---
title: "FACTS Benchmark Suite: Systematically evaluating the factuality of large language models"
source: https://deepmind.google/blog/facts-benchmark-suite-systematically-evaluating-the-factuality-of-large-language-models/
site: deepmind
date: 2025-12-09
authors: FACTS team
crawled: 2026-09-13
---

Large language models (LLMs) are increasingly becoming a primary source for information delivery across diverse use cases, so it’s important that their responses are factually accurate.

In order to continue improving their performance on this industry-wide challenge, we have to better understand the types of use cases where models struggle to provide an accurate response and better measure factuality performance in those areas.

## The FACTS Benchmark Suite

Today, we’re teaming up with Kaggle to introduce the [FACTS Benchmark Suite](https://www.kaggle.com/benchmarks/google/facts/leaderboard). It extends our previous work developing the [FACTS Grounding Benchmark](https://deepmind.google/blog/facts-grounding-a-new-benchmark-for-evaluating-the-factuality-of-large-language-models/), with three additional factuality benchmarks, including:

- A [**Parametric Benchmark**](https://www.kaggle.com/benchmarks/google/facts-parametric/leaderboard) that measures the model’s ability to access its internal knowledge accurately in factoid question use-cases.
- A [**Search Benchmark**](https://www.kaggle.com/benchmarks/google/facts-search/leaderboard) that tests a model’s ability to use Search as a tool to retrieve information and synthesize it correctly.
- A [**Multimodal Benchmark**](https://www.kaggle.com/benchmarks/google/facts-multimodal/leaderboard) that tests a model’s ability to answer prompts related to input images in a factually correct manner.

We are also updating the original FACTS grounding benchmark with [**Grounding Benchmark - v2**](https://www.kaggle.com/benchmarks/google/facts-grounding/leaderboard), an extended benchmark to test a model’s ability to provide answers grounded in the context of a given prompt.

Each benchmark was carefully curated to produce a total of 3,513 examples, which we are making publicly available today. Similar to our previous release, we are following standard industry practice and keeping an evaluation set held-out as a private set. The FACTS Benchmark Suite Score (or FACTS Score) is calculated as the average accuracy of both public and private sets across the four benchmarks. Kaggle will oversee the management of the FACTS Benchmark Suite. This includes owning the private held-out sets, testing the leading LLMs on the benchmarks, and hosting the results on a public leaderboard. More details about the FACTS evaluation methodology can be found in our [tech report](https://storage.googleapis.com/deepmind-media/FACTS/FACTS_benchmark_suite_paper.pdf).


### Parametric Benchmark

The FACTS Parametric benchmark assesses the ability of models to accurately answer factual questions, without the aid of external tools like web search. All the questions in the benchmark are “trivia style” questions driven by user interest that can be answered via Wikipedia (a standard source for LLM pretraining). The resulting benchmark consists of a 1052-item public set and a 1052-item private set.

![Distribution of context domain (left) and distribution of the answer type (right) as a percent of the total set of questions in the Parametric benchmark.](https://lh3.googleusercontent.com/3rWcOoUWW4R1fPg-rubQXK7EX_LWQb-OVdjx3h5GnDHOXMIxVTWmMimghase8GzR0ih7O1fQUPLnxTkRNchdIKfZuPscCBnH-746Biyqt9a77ImKBw=w1440)![Distribution of context domain (left) and distribution of the answer type (right) as a percent of the total set of questions in the Parametric benchmark.](https://lh3.googleusercontent.com/dfUZuvGKtW46CkqUiLvZWXBqBOGGy1lkw31AyOjVyNpuWSfO2TQxYn9w-9MEABCoHDbszZswKFTxJjoOUu8oN8IARlQs9MlLLCS3O38BahvnLB6f=w1440)

Distribution of context domain (left) and distribution of the answer type (right) as a percent of the total set of questions in the Parametric benchmark.

A typical prompt from the public set would require the model to answer a simple question on a niche topic, e.g., “Who played harmonica on ‘The Rockford Files’ theme song?”

### Search Benchmark

By contrast, the FACTS Search benchmark evaluates a model’s ability to use a web search tool for answering questions. This benchmark was designed to be challenging for LLMs even with access to the web, often requiring the retrieval of multiple facts sequentially to answer a single query. The same web search tool is being made available to all models, ensuring the model capabilities are tested in isolation without the confounding factor of custom web retrieval settings. FACTS Search consists of a 890-item public set and a 994-item private set.

![Distribution of context domain (left) and distribution of the task requested by the user (right) as a percent of the total set of prompts in the Search benchmark.](https://lh3.googleusercontent.com/TjFoip4LXatWLaEeubsWJGshovmVWoxGFRAzw6HT_BYUcICF8EMvvClM8oQsn_7e34tgILFoCSN9R_OVZozgC9UQN8shMli9Uey1xpB3hUGQGtZhhA=w1440)![Distribution of context domain (left) and distribution of the task requested by the user (right) as a percent of the total set of prompts in the Search benchmark.](https://lh3.googleusercontent.com/KLFNpI1mJYU0HcEgdo2b0kbB2F7WLxA2hCttyzfPLSzPh9gtlC7u6yBMJ-PRw0XSzgamzFuNAfnr5_2i-d1AEx7ap9VwcE5FnHghuQfVcjnbSIBAl6A=w1440)

Distribution of context domain (left) and distribution of the task requested by the user (right) as a percent of the total set of prompts in the Search benchmark.

The following example from the public set was included because it requires retrieving information from several web pages, “What is the sum of the birth years of the British boxer who defeated Vazik Kazarian at the 1960 Summer Olympics, the Moroccan boxer who also competed in the men’s light welterweight event at those same Olympics, and the Danish boxer who competed in both the 1960 and 1964 Summer Olympics?”

### Multimodal Benchmark

The FACTS Multimodal benchmark evaluates the ability of models to generate factually accurate text in response to image-based questions, which is a critical capability for modern multimodal systems.

This task requires the integration of visual grounding, i.e. its ability to accurately interpret and connect information from visual input, using its internal or “parametric” world knowledge. The evaluation framework is designed to ensure that a response is both correct and provides all necessary information to be complete. The benchmark consists of a 711-item public set and a 811-item private set.

![Distribution of image (left) and distribution of the question categories (right) as a part of the Multimodal benchmark](https://lh3.googleusercontent.com/o1Gr2jkpDQliiXsnwl50CttQy1VoPvIyaveYz0et8KU7zVzGp0Cv6Nmkuk92FZFTlwTym-xUnnaGGtQwKWWCqib3ryideKWR8btNhYxNr5hP2HVQ=w1440)![Distribution of image (left) and distribution of the question categories (right) as a part of the Multimodal benchmark](https://lh3.googleusercontent.com/HNnmCFScFhiOAv4B7M9C6U3CHFwgZ_D2WM_TPpk96oYBLFSTQe3kM2zaqBJ-boHLu20neyvhYbO6NwImqW6rAYUyepBgGsPToEZwPjXJQhU-2EOl=w1440)

Distribution of image (left) and distribution of the question categories (right) as a part of the Multimodal benchmark.

For example, the following image from the public set of the Multimodal benchmark appeared with the prompt: “What genus does this animal belong to?”

![Close-up photograph of a small, fuzzy brown moth or skipper butterfly with broad wings resting on a green leaf. The insect has large black eyes and antennae curved backward over its head.](https://lh3.googleusercontent.com/RaSYwSSlTwGVF3I3lfRKPSwC6PlsqzYRyF-SnebnRLFCuOxNOx6jY743QGT9WwM-Ze1gievuj6D60l82PulYNYjVMDct0OueMC1Oti5CmWbtCaL5Oy4=w1440)

An example of an image from the Multimodal benchmark (Photo credit: Image: Racta apella by desertnaturalist, CC BY 4.0)

## Results

We evaluated leading LLMs on the FACTS Benchmark Suite, which includes the updated FACTS Grounding v2.

The table below lists 15 leading models and their overall FACTS score (followed by the breakdown to the scores across the four individual benchmarks: Grounding, Multimodal, Parametric and Search).

![A table ranking 15 leading large language models by their overall FACTS Score and individual benchmark scores in Grounding, Multimodal, Parametric, and Search, with Gemini 3 Pro leading at a 68.8% FACTS Score.](https://lh3.googleusercontent.com/abbClpiLAte-Kdj4zLeSNbsAwctgypFDfsTK33u8zqWTq_XkHzgszrv051GBbZldBg_zQ5h8gopJUw_W8P4vyRgWDBaz73j2jaVJuqj0Mscl8toe=w1440)![A table ranking 15 leading large language models by their overall FACTS Score and individual benchmark scores in Grounding, Multimodal, Parametric, and Search, with Gemini 3 Pro leading at a 68.8% FACTS Score.](https://lh3.googleusercontent.com/iAa3uDNbaJxHRXomKm4RSdLPhscLpLpZ9YnhpOlB1PGoymYfdlciMbJDv_6NwiKXVRC7p_Jg0Jn23j9eYuP2MIcVpo1oAlx_T8SsPeYwMs_9cS5_=w1440)

Gemini 3 Pro leads in overall performance, with a FACTS Score of 68.8%. In particular, we saw significant improvements from Gemini 2.5 Pro to Gemini 3 Pro in Search & Parametric slices, where the error rate was reduced by 55% on FACTS Search and 35% for FACTS Parametric. FACTS Multimodal saw the lowest scores, generally. All evaluated models achieved an overall accuracy below 70%, leaving considerable headroom for future progress.

Beyond the FACTS Benchmark Suite, Gemini’s improvement in factuality is also reflected in another factuality benchmark, [SimpleQA Verified](https://www.kaggle.com/benchmarks/deepmind/simpleqa-verified), going from 54.5% accuracy on Gemini 2.5 Pro to 72.1% accuracy on Gemini 3 Pro. SimpleQA Verified tests LLMs’ parametric knowledge on short-form responses.

## Looking Ahead

While LLM factuality is still an area of ongoing research, the FACTS Benchmark Suite and Gemini 3 Pro results are representative of Google’s long-term commitment towards making information universally accessible and useful. We hope this work encourages deeper research into LLM factuality, leading to better and more accurate models and products for the people that rely on them.
