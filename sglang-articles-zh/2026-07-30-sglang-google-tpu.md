---
title: "RadixArk 携手 Google，将完整的 SGLang 特性带到 TPU"
title_en: "RadixArk Joins Forces with Google to Bring Full SGLang Features to TPUs"
author: "RadixArk & Google"
date: "July 30, 2026"
previewImg: /images/blog/2026-07-30-sglang-google-tpu/cover.png
type: news
excerpt: "RadixArk and Google Cloud are partnering to bring SGLang to TPUs, giving developers ultimate flexibility for running workloads on their choice of hardware."
source: https://lmsys.org/blog/2026-07-30-sglang-google-tpu/
translated: 2026-09-12
---

# RadixArk 携手 Google，将完整的 SGLang 特性带到 TPU

> 原文：[RadixArk Joins Forces with Google to Bring Full SGLang Features to TPUs](https://lmsys.org/blog/2026-07-30-sglang-google-tpu/) · LMSYS Blog · RadixArk & Google

RadixArk 与 Google Cloud 正在展开合作，将 [SGLang](https://github.com/sgl-project/sglang) 带到 TPU 上，让开发者能够以最大的灵活性在自己选择的硬件上运行工作负载。

SGLang 是一个为生产规模下高吞吐、低延迟而打造的开源推理框架。它拥有超过 30,000 个 GitHub star 和 1,700 多名贡献者，运行在全球数十万块 GPU 上，每天在生产环境中生成数万亿个 token。[RadixArk](https://www.radixark.com) 是 SGLang 项目的维护方。

目前，开发者已经可以通过 [SGL-JAX](https://github.com/sgl-project/sglang-jax) 在最新几代 TPU 上运行 SGLang，支持主流大语言模型与多模态模型家族，包括 Gemma、Qwen、DeepSeek、GLM、Mimo、Kimi、Ling、MiniMax 和 Grok，以及用于视频与图像生成的扩散模型，包括 Wan 和 Flux。今年晚些时候，RadixArk 还将推出 <span style="color: var(--orange);">SGL-torchtpu</span>，作为一个额外的 <span style="text-decoration: underline; text-decoration-color: var(--orange); text-decoration-thickness: 1.5px; text-underline-offset: 3px;">PyTorch 原生 TPU 后端</span>，具备即时执行（eager execution）、PyTorch 生态兼容性和 MPMD 支持等特性。它将让业界的任何 AI 研究员或工程师都能使用标准 PyTorch 工具链、通过 SGLang 在 Google TPU 上运行 LLM，并获得高性能、可扩展性与最先进的功能。这些功能包括：在多主机 TPU 上以完整规模运行领先的开源模型，且模型质量与已公布的基线持平；此外还支持多种并行方式（数据并行、张量并行、专家并行、上下文并行和流水线并行）、Radix Cache、HiCache、量化以及投机解码——这一切均由 RadixArk、Google 与 SGLang 社区共同构建的 TPU Pallas 算子（kernel）驱动。

今后，新的开源模型在 GPU 上可运行的当天即可在 TPU 上运行，且这一 Day 0 支持将延伸至每一代新的 TPU。

这些进展使 TPU 成为一条即插即用、高性价比的前沿推理路径。团队可以使用与 GPU 上完全相同的 SGLang API 和功能，并根据工作负载需求和性价比自由选择硬件。

<p style="margin: 2.6em 0; padding-left: 1.5em; border-left: 2px solid var(--orange); font-size: 1.125em; line-height: 1.6; font-style: normal;">“RadixArk 的使命是让每一位建设者都能使用开放且触手可及的前沿 AI 基础设施。SGLang 正是这一使命的体现，我们很高兴能与 Google Cloud 合作，把它的性能与灵活性带给 TPU 生态，”RadixArk CEO <strong>Ying Sheng</strong> 表示。</p>

<p style="margin: 2.6em 0; padding-left: 1.5em; border-left: 2px solid var(--orange); font-size: 1.125em; line-height: 1.6; font-style: normal;">“要真正加速前沿 AI 创新，开发者必须能够自由选择并使用性能、可靠性、可扩展性和成本表现更优的 AI 训练与推理服务平台，”Google 工程副总裁（Core ML/AI）<strong>Bill Jia</strong> 表示，“我们与 RadixArk 的合作是实现我们‘可编程异构’（programmable heterogeneity）愿景的关键一步——在这一愿景中，软件是开放的桥梁，而不是锁定机制。通过将 SGLang 的高吞吐推理服务框架带到 Google TPU 上，我们实际上为开发者免除了‘迁移税’，让他们能够使用完全相同的 SGLang 推理 API，在自选的硬件（如 GPU、TPU）与 AI 框架（如 PyTorch、JAX）上无缝运行生产工作负载。”</p>

<p style="margin-top: 2.4em;">由 RadixArk 与 SGLang 社区联手打造的 SGL-JAX 现已发布，访问地址：<a href="https://github.com/sgl-project/sglang-jax"><svg width="15" height="15" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true" style="vertical-align: -2px; margin-right: 5px;"><path d="M8 0c4.42 0 8 3.58 8 8a8.013 8.013 0 0 1-5.45 7.59c-.4.08-.55-.17-.55-.38 0-.27.01-1.13.01-2.2 0-.75-.25-1.23-.54-1.48 1.78-.2 3.65-.88 3.65-3.95 0-.88-.31-1.59-.82-2.15.08-.2.36-1.02-.08-2.12 0 0-.66-.21-2.17.82a7.6 7.6 0 0 0-2.04-.28c-.69 0-1.39.09-2.04.28-1.51-1.02-2.17-.82-2.17-.82-.44 1.1-.16 1.92-.08 2.12-.51.56-.82 1.28-.82 2.15 0 3.06 1.86 3.75 3.64 3.95-.23.2-.44.55-.51 1.07-.45.2-1.61.55-2.33-.66-.15-.24-.6-.83-1.23-.82-.67.01-.27.38.01.53.34.19.73.9.82 1.13.16.45.68 1.31 2.69.94 0 .67.01 1.3.01 1.49 0 .21-.15.45-.55.38A7.995 7.995 0 0 1 0 8c0-4.42 3.58-8 8-8Z"/></svg>github.com/sgl-project/sglang-jax</a>。</p>

<p>SGL 家族始终欢迎新的贡献者加入，与我们携手构建开放、高性能的推理服务引擎！</p>
