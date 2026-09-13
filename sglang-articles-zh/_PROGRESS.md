# SGLang 技术博客翻译进度

规范：TRANSLATION_GUIDE.md + TRANSLATION_GUIDE_SGLANG.md
源：sglang-articles/<slug>.md → 译文：sglang-articles-zh/<slug>.md
frontmatter：title 换中文，新增 title_en + source（https://lmsys.org/blog/<slug>/）+ translated: 2026-09-12；author/date/previewImg 照抄；正文 `# 中文标题` + `> 原文：[EN](url) · LMSYS Blog · <作者>`。

语料：LMSYS 官方博客 markdown 源（lm-sys/lm-sys.github.io/blog/，SGLang 官方文档站的同步来源），2024-01→2026-09，SGLang 及其生态（slime/Miles/SGLang-Diffusion/Jax）共 96 篇。非技术内容（Arena/排行榜/Vicuna 等）已排除。

## 状态：✅ 全部完成（2026-09-12，96/96）

- [x] 2024-01-17-sglang

批次清单（每行一个子代理任务，串行派发）：

1. [x] 2026-08-28-infer-forge-loop-engineering
2. [x] 2025-05-05-large-scale-ep
3. [x] 2026-07-15-inkling-day0-support
4. [x] 2026-06-17-ling-2-6-tpu
5. [x] 2026-07-02-agent-assisted-sglang-development
6. [x] 2026-01-15-chunked-pipeline
7. [x] 2026-08-19-deepseek-v4-pro-engine-optimization-h20
8. [x] 2026-08-21-ling3-flash-spec-decode-blackwell
9. [x] 2026-07-27-kimi-k3-day0-support
10. [x] 2026-07-29-mxfp8-nvfp4-rl
11. [x] 2025-07-08-ome
12. [x] 2026-08-07-hpc-ops-sglang
13. [x] 2025-11-25-fp8-rl
14. [x] 2026-08-11-unified-radix-cache
15. [x] 2026-04-25-deepseek-v4
16. [x] 2026-08-17-advanced-cuda-graph
17. [x] 2026-06-04-higgs-audio-v3-tts
18. [x] 2026-06-26-waterfill-lplb
19. [x] 2026-08-18-miles-v0-1
20. [x] 2026-08-27-minimax-h3-h200
21. [x] 2026-08-04-specforge-v0-3
22. [x] 2026-01-26-int4-qat
23. [x] 2025-07-16-nvila
24. [x] 2025-09-26-sglang-ant-group
25. [x] 2026-05-28-mori
26. [x] 2025-07-14-intel-xeon-optimization
27. [x] 2026-08-20-miles-mooncake-rollout-data-transfer
28. [x] 2026-04-29-p2p-update
29. [x] 2026-05-13-no-token-left-behind
30. [x] 2026-07-13-glm52-optimization
31. [x] 2026-07-06-dspark-sglang, 2026-02-19-gb300-longctx
32. [x] 2026-06-17-moss-tts-local-v15, 2026-07-10-rocm-miles-dsv4
33. [x] 2026-02-11-Qwen-latency, 2025-09-22-sglang-deterministic
34. [x] 2026-08-21-sglang-fast-recovery, 2026-08-26-qwen-flash-next
35. [x] 2025-10-13-nvidia-dgx-spark, 2025-09-28-pdmux
36. [x] 2026-06-15-next-generation-speculative-decoding-dflash-v2, 2025-12-19-diffusion-llm
37. [x] 2025-12-23-spec-bundle-phase-1, 2026-08-12-qwen3-8-day0-support
38. [x] 2025-10-22-KTransformers, 2025-12-10-rfork
39. [x] 2025-09-21-petit-amdgpu, 2024-07-25-sglang-llama3
40. [x] 2026-06-04-nvidia-run-nemotron-3-ultra, 2026-03-17-rocm-miles-rl-amd
41. [x] 2026-09-10-deepseek-v41, 2026-08-05-glmImage-optimization
42. [x] 2026-08-11-nemotron-3-5-lightning, 2025-12-01-eagle3-vertex
43. [x] 2025-11-07-sglang-diffusion, 2025-09-25-gb200-part-2
44. [x] 2026-07-18-opd-support-in-miles, 2025-07-20-k2-large-scale-ep
45. [x] 2024-02-05-compressed-fsm, 2024-12-04-sglang-v0-4
46. [x] 2025-12-16-mimo-v2-flash, 2026-01-16-sglang-diffusion, 2026-01-12-epd
47. [x] 2026-07-31-cleaner-quantization-stack, 2025-07-17-mtp, 2025-09-10-sglang-hicache
48. [x] 2026-02-16-sglang-diffusion-advanced-optimizations, 2025-08-27-gpt-oss, 2026-03-25-eep-partial-failure-tolerance
49. [x] 2026-03-25-gtc2026, 2025-10-29-sglang-jax, 2025-12-17-minisgl
50. [x] 2026-06-27-netpreme-xmem, 2025-09-01-sglang-longcat-flash, 2025-07-25-spec-forge
51. [x] 2025-11-13-AutoRound, 2025-07-09-slime, 2025-08-28-gpt-oss-qat
52. [x] 2026-01-21-novita-glm4, 2024-09-04-sglang-v0-3, 2026-02-20-gb300-inferencex
53. [x] 2025-10-14-sa-inference-max, 2025-11-04-miminmax-m2, 2025-12-15-run-nvidia-nemotron-3-nano
54. [x] 2026-04-10-sglang-hisparse, 2025-06-16-gb200-part-1, 2026-03-11-run-nvidia-nemotron-3-super
55. [x] 2026-06-01-hetero-epd, 2025-12-02-modelopt-quantization, 2026-08-10-meta-muse-glimmer
56. [x] 2025-11-03-gpt-oss-on-nvidia-dgx-spark, 2025-11-19-miles, 2025-09-29-deepseek-V32
57. [x] 2025-07-31-glm4-5, 2026-07-30-sglang-google-tpu
