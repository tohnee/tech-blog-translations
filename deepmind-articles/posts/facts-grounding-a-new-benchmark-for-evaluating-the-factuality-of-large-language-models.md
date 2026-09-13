---
title: "FACTS Grounding: A new benchmark for evaluating the factuality of large language models"
source: https://deepmind.google/blog/facts-grounding-a-new-benchmark-for-evaluating-the-factuality-of-large-language-models/
site: deepmind
date: 2024-12-17
authors: FACTS team
crawled: 2026-09-13
---

Our comprehensive benchmark and online leaderboard offer a much-needed measure of how accurately LLMs ground their responses in provided source material and avoid hallucinations

Large language models (LLMs) are transforming how we access information, yet their grip on factual accuracy remains imperfect. They can “hallucinate” false information, particularly when given complex inputs. In turn, this can erode trust in LLMs and limit their applications in the real world.

Today, we’re introducing [FACTS Grounding](https://goo.gle/FACTS_paper), a comprehensive benchmark for evaluating the ability of LLMs to generate responses that are not only factually accurate with respect to given inputs, but also sufficiently detailed to provide satisfactory answers to user queries.

We hope our benchmark will spur industry-wide progress on factuality and grounding. To track progress, we’re also launching the [FACTS leaderboard on Kaggle](http://www.kaggle.com/facts-leaderboard). We’ve already tested leading LLMs using FACTS Grounding and have populated the initial leaderboard with their grounding scores. We will maintain and update the leaderboard as the field advances.

![A table showing the FACTS Grounding leaderboard ranking nine language models by their grounding scores, with gemini-2.0-flash-exp in first place at 83.6%, followed by other models from Google, Anthropic, and OpenAI.](https://lh3.googleusercontent.com/6RO_Jbetl7FvF3Exa2Sq-UXC9vQCCFqvZx0MpbgI_99N300B_sUW_Ri5BJtPxpMomEUBTn2O0KnuLFRgT-OJacfevPUSTFfHnIHMN5ZmLK9xRjYvUw=w1440)

Current leaderboard ranking

## FACTS Grounding dataset

To accurately evaluate the factuality and grounding of any given LLM, the FACTS Grounding dataset comprises 1,719 examples, each carefully crafted to require long-form responses grounded in the context document provided. Each example comprises a document, a system instruction requiring the LLM to exclusively reference the provided document, and an accompanying user request.

![A diagram illustrating a FACTS Grounding dataset example, showing a system instruction at the top requiring responses to rely solely on the provided prompt. Below, a context document about money-saving tips and a user request asking for tips are processed to generate a grounded response summarizing the tips.](https://lh3.googleusercontent.com/vQ3z6dE4DArP71eQM5m_rLzOYlj5JtEPAtNPjOqYjDDniDUyalQyqW0QWTsy-yT2v8-R9mHhYbp1l3wnNrydos7c4Ky6fFAwjY31VfLk6bFlkpF2uw=w1440)

An example from the FACTS Grounding dataset

All examples are divided into a "public" set (860) and a "private" (859) held out set. We are [releasing the public set](http://www.kaggle.com/datasets/deepmind/facts-grounding-examples) today so anyone can use it to evaluate an LLM. Of course, we know that issues of benchmark contamination and leaderboard hacking are important to protect against, so following standard industry practice, we are keeping the private evaluation set held out. The FACTS leaderboard scores are the average performance across both public and private sets.

To ensure a diversity of inputs, the FACTS Grounding examples include documents with a variety of lengths, up to a maximum of 32,000 tokens (roughly 20,000 words), covering domains such as finance, technology, retail, medicine, and law. The user requests are similarly wide ranging, including requests for summarization, Q&A generation, and rewriting tasks. We did not include any examples that could require creativity, mathematics, or complex reasoning – capabilities which might require the model to apply more advanced reasoning in addition to grounding.

![Two pie charts illustrating the FACTS Grounding dataset distribution. The left chart shows the "Domain distribution" across medical (29.0%), legal (22.3%), internet/technology (19.2%), financial (18.1%), and retail/product (11.4%). The right chart shows the "Task distribution," led by fact finding (31.6%) and find & summarize (29.7%), followed by smaller percentages for explanation/definition, concept comparison, pros & cons, and various summarization formats.](https://lh3.googleusercontent.com/zErrMWYZIvU9kSpVOzE2QnZhefVHi4kI3q-NN0Or8t173NbmE0upIDPSYKIhRWK2nnvrntjSN-KOpAPrtQiM6LVKtznXIK2L4J431IwnVksS72J8Ug=w1440)

Prompt distribution

## Collective judgement by leading LLMs

To succeed on a given example, an LLM must synthesize the complex information in the document and generate a long-form response that is both a comprehensive answer to the user request and fully attributable to that document.

FACTS Grounding evaluates model responses automatically using three frontier LLM judges — namely Gemini 1.5 Pro, GPT-4o, and Claude 3.5 Sonnet. We selected a combination of different judges to mitigate any potential bias of a judge giving higher scores to the responses produced by a member of its own model family. The automatic judge models were comprehensively evaluated against a held-out test set to find the best performing judging prompt templates and to verify agreement with human raters.

Each FACTS Grounding example is judged in two phases. First, responses are evaluated for eligibility, and disqualified if they don’t sufficiently address the user’s request. Second, responses are judged as factually accurate if they are fully grounded in information contained in the provided document, with no hallucinations.

With the eligibility and grounding accuracy of a given LLM response evaluated separately by multiple AI judge models, the results are then aggregated to determine if the LLM has dealt with the example successfully. The final score for the overall grounding task is the average of all judge models’ scores across all examples. Find more details of our FACTS Grounding evaluation methodology [in our paper](https://goo.gle/FACTS_paper).

![A flowchart illustrating the FACTS Grounding evaluation process. An example consisting of a system instruction, context document, and user prompt generates a response. This response is evaluated sequentially by a "Quality judge" and a "Grounding judge" using Claude 3.5 Sonnet, Gemini 1.5 Pro, and GPT-4o. If disqualified at the quality phase, it is marked as an "Ineligible response." Successfully evaluated responses are averaged across all judges and 1,719 examples to produce a final "Factuality score."](https://lh3.googleusercontent.com/wqLQZz-033f2ephaEcL2-z-Hxl8QnhFOlOiHDcZS4ZOa4BIfLUS-JSWvD-59AIDINkSc4NN59pslUD1lsUx6XGkDLU65j9xR5qqruZUOLdNtGKf4Qbw=w1440)

A factually correct response that fails to properly address the user’s request fails the benchmarking example. Here we see three instances of model responses that the automated LLM judges considered ineligible

## FACTS Grounding will continue to evolve

We are mindful that benchmarks can be quickly overtaken by progress, so this launch of our FACTS Grounding benchmark and leaderboard is just the beginning. Factuality and grounding are among the key factors that will shape the future success and usefulness of LLMs and broader AI systems, and we aim to grow and iterate FACTS Grounding as the field progresses, continually raising the bar.

We encourage the AI community to [engage with FACTS Grounding](http://www.kaggle.com/facts-leaderboard/discussion), evaluate their models on the open set of examples or to submit their models for evaluation. We believe that comprehensive benchmarking methods, coupled with continuous research and development will continue to improve AI systems.

**Acknowledgements**

FACTS is a collaboration between Google DeepMind and Google Research.
FACTS Grounding was led by: Alon Jacovi, Andrew Wang, Chris Alberti, Connie Tao, Dipanjan Das, Jon Lipovetz, Kate Olszewska, Lukas Haas, Michelle Liu, and Nate Keating.

We are also very grateful for contributions from: Adam Bloniarz, Carl Saroufim, Corey Fry, Dror Marcus, Doron Kukliansky, Gaurav Singh Tomar, James Swirhun, Jinwei Xing, Lily Wang, Madhu Gurumurthy, Michael Aaron, Moran Ambar, Rachana Fellinger, Rui Wang, Zizhao Zhang, and Sasha Goldshtein.

We would also like to thank Avinatan Hassidim, D. Sculley, Fernando Pereira, Koray Kavukcuoglu, Slav Petrov, Ya Xu, and Yossi Matias for their continued support.
