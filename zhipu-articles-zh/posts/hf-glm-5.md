---
title: "GLM-5 模型卡"
source: https://huggingface.co/zai-org/GLM-5
crawled: 2026-09-22
title_en: "zai-org/GLM-5 model card"
translated: 2026-09-22
---

---
language:
- en
- zh
library_name: transformers
license: mit
pipeline_tag: text-generation
---

# GLM-5 模型卡

> 原文：[zai-org/GLM-5 model card](https://huggingface.co/zai-org/GLM-5) · 智谱 Z.ai

<div align="center">
<img src=https://raw.githubusercontent.com/zai-org/GLM-5/refs/heads/main/resources/logo.svg width="15%"/>
</div>
<p align="center">
    👋 欢迎加入我们的 <a href="https://raw.githubusercontent.com/zai-org/GLM-5/refs/heads/main/resources/wechat.png" target="_blank">WeChat</a> 或 <a href="https://discord.gg/QR7SARHRxK" target="_blank">Discord</a> 社区。
    <br>
    📖 了解 GLM-5 <a href="https://z.ai/blog/glm-5" target="_blank">技术博客</a>。
    <br>
    📍 在 <a href="https://docs.z.ai/guides/llm/glm-5">Z.ai API 平台</a>使用 GLM-5 API 服务。
    <br>
    👉 一键直达 <a href="https://chat.z.ai">GLM-5</a>。
</p>

<p align="center">
    [<a href="https://huggingface.co/papers/2602.15763" target="_blank">论文</a>]
    [<a href="https://github.com/zai-org/GLM-5" target="_blank">GitHub</a>]
</p>

## 简介

我们发布 GLM-5，面向复杂系统工程与长时程智能体任务。扩展（Scaling）仍是提升通用人工智能（AGI）智能效率最重要的途径之一。与 GLM-4.5 相比，GLM-5 从 355B 参数（32B 激活）扩展到 744B 参数（40B 激活），预训练数据从 23T 增加到 28.5T token。GLM-5 还集成了 DeepSeek 稀疏注意力（DSA），在保持长上下文能力的同时大幅降低部署成本。

强化学习旨在弥合预训练模型中「胜任」与「卓越」之间的差距。然而，由于 RL 训练效率低下，将其大规模部署于 LLM 是一项挑战。为此，我们开发了 [slime](https://github.com/THUDM/slime)——一种新颖的**异步 RL 基础设施**，可大幅提升训练吞吐量和效率，实现更细粒度的后训练迭代。凭借预训练与后训练的双重进步，GLM-5 在广泛的学术基准上相较 GLM-4.7 取得显著提升，并在推理、编码和智能体任务上取得全球所有开源模型中的最佳表现，缩小了与前沿模型的差距。

## 基准测试

|                                  | GLM-5                  | GLM-4.7   | DeepSeek-V3.2 | Kimi K2.5 | Claude Opus 4.5 | Gemini 3 Pro | GPT-5.2 (xhigh) |
| -------------------------------- | ---------------------- | --------- | ------------- |-----------| --------------- | ------------ | --------------- |
| HLE                              | 30.5                   | 24.8      | 25.1          | 31.5      | 28.4            | 37.2         | 35.4            |
| HLE (w/ Tools)                   | 50.4                   | 42.8      | 40.8          | 51.8      | 43.4*           | 45.8*        | 45.5*           |
| AIME 2026 I                      | 92.7                   | 92.9      | 92.7          | 92.5      | 93.3            | 90.6         | -               |
| HMMT Nov. 2025                   | 96.9                   | 93.5      | 90.2          | 91.1      | 91.7            | 93.0         | 97.1            |
| IMOAnswerBench                   | 82.5                   | 82.0      | 78.3          | 81.8      | 78.5            | 83.3         | 86.3            |
| GPQA-Diamond                     | 86.0                   | 85.7      | 82.4          | 87.6      | 87.0            | 91.9         | 92.4            |
| SWE-bench Verified               | 77.8                   | 73.8      | 73.1          | 76.8      | 80.9            | 76.2         | 80.0            |
| SWE-bench Multilingual           | 73.3                   | 66.7      | 70.2          | 73.0      | 77.5            | 65.0         | 72.0            |
| Terminal-Bench 2.0 (Terminus 2)  | 56.2 / 60.7 † | 41.0      | 39.3          | 50.8      | 59.3            | 54.2         | 54.0            |
| Terminal-Bench 2.0 (Claude Code) | 56.2 / 61.1 †  | 32.8      | 46.4          | -         | 57.9            | -            | -               |
| CyberGym                         | 43.2                   | 23.5      | 17.3          | 41.3      | 50.6            | 39.9         | -               |
| BrowseComp                       | 62.0                   | 52.0      | 51.4          | 60.6      | 37.0            | 37.8         | -               |
| BrowseComp (w/ Context Manage)   | 75.9                   | 67.5      | 67.6          | 74.9      | 67.8            | 59.2         | 65.8            |
| BrowseComp-Zh                    | 72.7                   | 66.6      | 65.0          | 62.3      | 62.4            | 66.8         | 76.1            |
| τ²-Bench                         | 89.7                   | 87.4      | 85.3          | 80.2      | 91.6            | 90.7         | 85.5            |
| MCP-Atlas (Public Set)           | 67.8                   | 52.0      | 62.2          | 63.8      | 65.2            | 66.6         | 68.0            |
| Tool-Decathlon                   | 38.0                   | 23.8      | 35.2          | 27.8      | 43.5            | 36.4         | 46.3            |
| Vending Bench 2                  | $4,432.12              | $2,376.82 | $1,034.00     | $1,198.46 | $4,967.06       | $5,478.16    | $3,591.33       |

> *：指其在完整集上的得分。
>
> †：Terminal-Bench 2.0 的一个修复了部分模糊指令的验证版本。
更多评测细节见脚注。

### 脚注

* **Humanity’s Last Exam（HLE）及其他推理任务**：我们以最大生成长度 131,072 个 token 进行评测（`temperature=1.0, top_p=0.95, max_new_tokens=131072`）。默认报告纯文本子集；带 * 的结果来自完整集。我们使用 GPT-5.2（medium）作为判分模型。对于 HLE-with-tools，我们使用最大 202,752 token 的上下文长度。
* **SWE-bench 与 SWE-bench Multilingual**：我们使用 OpenHands 及定制指令提示词运行 SWE-bench 套件。设置：`temperature=0.7, top_p=0.95, max_new_tokens=16384`，200K 上下文窗口。
* **BrowserComp**：不使用上下文管理时，我们保留最近 5 轮的细节。使用上下文管理时，我们采用与 DeepSeek-v3.2 和 Kimi K2.5 相同的「全部丢弃」策略。
* **Terminal-Bench 2.0（Terminus 2）**：我们使用 Terminus 框架评测，参数为 `timeout=2h, temperature=0.7, top_p=1.0, max_new_tokens=8192`，128K 上下文窗口。资源限制上限为 16 CPU 和 32 GB 内存。
* **Terminal-Bench 2.0（Claude Code）**：我们在 Claude Code 2.1.14（思考模式、默认 effort）中以 `temperature=1.0, top_p=0.95, max_new_tokens=65536` 进行评测。由于生成速度原因，我们移除了墙上时钟时间限制，但保留每任务的 CPU 和内存约束。得分为 5 次运行的平均值。我们修复了 Claude Code 引入的环境问题，并同时在消除了模糊指令的 Terminal-Bench 2.0 验证版数据集上报告结果（参见：[https://huggingface.co/datasets/zai-org/terminal-bench-2-verified](https://huggingface.co/datasets/zai-org/terminal-bench-2-verified)）。
* **CyberGym**：我们在 Claude Code 2.1.18（思考模式、无网络工具）中以（`temperature=1.0, top_p=1.0, max_new_tokens=32000`）进行评测，每任务超时 250 分钟。结果为 1,507 项任务上的单次运行 Pass@1。
* **MCP-Atlas**：所有模型均在 500 任务的公开子集上以思考模式评测，每任务超时 10 分钟。我们使用 Gemini 3 Pro 作为判分模型。
* **τ²-bench**：我们在 Retail 和 Telecom 中加入了小幅提示词调整，以避免因用户过早终止交互而导致的失败。对于 Airline 领域，我们采用 Claude Opus 4.5 系统卡中提出的领域修复。
* **Vending Bench 2**：评测由 [Andon Labs](https://andonlabs.com/evals/vending-bench-2) 独立进行。


## 本地部署 GLM-5

### 准备环境

以下开源框架支持 GLM-5 的本地部署：

- [vLLM](https://github.com/vllm-project/vllm)（v0.19.0+）
- [SGLang](https://github.com/sgl-project/sglang)（v0.5.10+）
- [KTransformers](https://github.com/kvcache-ai/ktransformers)（v0.5.3+）
- [Transformers](https://github.com/huggingface/transformers)（v0.5.4+）
- [xLLM](https://github.com/jd-opensource/xllm)（v0.8.0+）

### 部署

+ vLLM

    ```shell
    vllm serve zai-org/GLM-5 \
         --tensor-parallel-size 8 \
         --gpu-memory-utilization 0.85 \
         --speculative-config.method mtp \
         --speculative-config.num_speculative_tokens 3 \
         --tool-call-parser glm47 \
         --reasoning-parser glm45 \
         --enable-auto-tool-choice \
         --served-model-name glm-5
    ```

    更多详情请查阅 [recipes](https://github.com/vllm-project/recipes/blob/main/GLM/GLM5.md)。

+ SGLang

    ```shell
    sglang serve \
      --model-path zai-org/GLM-5 \
      --tp-size 8 \
      --tool-call-parser glm47  \
      --reasoning-parser glm45 \
      --speculative-algorithm EAGLE \
      --speculative-num-steps 3 \
      --speculative-eagle-topk 1 \
      --speculative-num-draft-tokens 4 \
      --mem-fraction-static 0.85 \
      --served-model-name glm-5
    ```

    更多详情请查阅 [sglang cookbook](https://cookbook.sglang.io/autoregressive/GLM/GLM-5)。

+ xLLM 及其他昇腾 NPU 平台

    请查阅[此处](https://github.com/zai-org/GLM-5/blob/main/example/ascend.md)的部署指南。

+ KTransformers

    请查阅[此处](https://github.com/kvcache-ai/ktransformers/blob/main/doc/en/kt-kernel/GLM-5-Tutorial.md)的部署指南。

## 引用

如果您在研究中发现 GLM-5 有用，请引用我们的技术报告：

```bibtex
@misc{glm5team2026glm5vibecodingagentic,
      title={GLM-5: from Vibe Coding to Agentic Engineering},
      author={GLM-5-Team and : and Aohan Zeng and Xin Lv and Zhenyu Hou and Zhengxiao Du and Qinkai Zheng and Bin Chen and Da Yin and Chendi Ge and Chenghua Huang and Chengxing Xie and Chenzheng Zhu and Congfeng Yin and Cunxiang Wang and Gengzheng Pan and Hao Zeng and Haoke Zhang and Haoran Wang and Huilong Chen and Jiajie Zhang and Jian Jiao and Jiaqi Guo and Jingsen Wang and Jingzhao Du and Jinzhu Wu and Kedong Wang and Lei Li and Lin Fan and Lucen Zhong and Mingdao Liu and Mingming Zhao and Pengfan Du and Qian Dong and Rui Lu and Shuang-Li and Shulin Cao and Song Liu and Ting Jiang and Xiaodong Chen and Xiaohan Zhang and Xuancheng Huang and Xuezhen Dong and Yabo Xu and Yao Wei and Yifan An and Yilin Niu and Yitong Zhu and Yuanhao Wen and Yukuo Cen and Yushi Bai and Zhongpei Qiao and Zihan Wang and Zikang Wang and Zilin Zhu and Ziqiang Liu and Zixuan Li and Bojie Wang and Bosi Wen and Can Huang and Changpeng Cai and Chao Yu and Chen Li and Chengwei Hu and Chenhui Zhang and Dan Zhang and Daoyan Lin and Dayong Yang and Di Wang and Ding Ai and Erle Zhu and Fangzhou Yi and Feiyu Chen and Guohong Wen and Hailong Sun and Haisha Zhao and Haiyi Hu and Hanchen Zhang and Hanrui Liu and Hanyu Zhang and Hao Peng and Hao Tai and Haobo Zhang and He Liu and Hongwei Wang and Hongxi Yan and Hongyu Ge and Huan Liu and Huanpeng Chu and Jia'ni Zhao and Jiachen Wang and Jiajing Zhao and Jiamin Ren and Jiapeng Wang and Jiaxin Zhang and Jiayi Gui and Jiayue Zhao and Jijie Li and Jing An and Jing Li and Jingwei Yuan and Jinhua Du and Jinxin Liu and Junkai Zhi and Junwen Duan and Kaiyue Zhou and Kangjian Wei and Ke Wang and Keyun Luo and Laiqiang Zhang and Leigang Sha and Liang Xu and Lindong Wu and Lintao Ding and Lu Chen and Minghao Li and Nianyi Lin and Pan Ta and Qiang Zou and Rongjun Song and Ruiqi Yang and Shangqing Tu and Shangtong Yang and Shaoxiang Wu and Shengyan Zhang and Shijie Li and Shuang Li and Shuyi Fan and Wei Qin and Wei Tian and Weining Zhang and Wenbo Yu and Wenjie Liang and Xiang Kuang and Xiangmeng Cheng and Xiangyang Li and Xiaoquan Yan and Xiaowei Hu and Xiaoying Ling and Xing Fan and Xingye Xia and Xinyuan Zhang and Xinze Zhang and Xirui Pan and Xu Zou and Xunkai Zhang and Yadi Liu and Yandong Wu and Yanfu Li and Yidong Wang and Yifan Zhu and Yijun Tan and Yilin Zhou and Yiming Pan and Ying Zhang and Yinpei Su and Yipeng Geng and Yong Yan and Yonglin Tan and Yuean Bi and Yuhan Shen and Yuhao Yang and Yujiang Li and Yunan Liu and Yunqing Wang and Yuntao Li and Yurong Wu and Yutao Zhang and Yuxi Duan and Yuxuan Zhang and Zezhen Liu and Zhengtao Jiang and Zhenhe Yan and Zheyu Zhang and Zhixiang Wei and Zhuo Chen and Zhuoer Feng and Zijun Yao and Ziwei Chai and Ziyuan Wang and Zuzhou Zhang and Bin Xu and Minlie Huang and Hongning Wang and Juanzi Li and Yuxiao Dong and Jie Tang},
      year={2026},
      eprint={2602.15763},
      archivePrefix={arXiv},
      primaryClass={cs.LG},
      url={https://arxiv.org/abs/2602.15763},
}
```
