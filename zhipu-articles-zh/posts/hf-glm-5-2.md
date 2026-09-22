---
title: "GLM-5.2 模型卡"
source: https://huggingface.co/zai-org/GLM-5.2
crawled: 2026-09-22
title_en: "zai-org/GLM-5.2 model card"
translated: 2026-09-22
---

---
language:
- en
- zh
library_name: transformers
license: mit
pipeline_tag: text-generation
new_version: zai-org/GLM-5.3-BF16
---

# GLM-5.2 模型卡

> 原文：[zai-org/GLM-5.2 model card](https://huggingface.co/zai-org/GLM-5.2) · 智谱 Z.ai

<div align="center">
<img src=https://raw.githubusercontent.com/zai-org/GLM-5/refs/heads/main/resources/logo.svg width="15%"/>
</div>
<p align="center">
    👋 欢迎加入我们的 <a href="https://raw.githubusercontent.com/zai-org/GLM-5/refs/heads/main/resources/wechat.png" target="_blank">WeChat</a> 或 <a href="https://discord.gg/QR7SARHRxK" target="_blank">Discord</a> 社区。
    <br>
    📖 了解 GLM-5.2 <a href="https://z.ai/blog/glm-5.2" target="_blank">博客</a>与 GLM-5 <a href="https://arxiv.org/abs/2602.15763" target="_blank">技术报告</a>。
    <br>
    📍 在 <a href="https://docs.z.ai/guides/llm/glm-5.2">Z.ai API 平台</a>使用 GLM-5.2 API 服务。
    <br>
    🔜 在<a href="https://chat.z.ai">此处</a>体验 GLM-5.2。
</p>

<p align="center">
    [<a href="https://huggingface.co/papers/2602.15763" target="_blank">论文</a>]
    [<a href="https://github.com/zai-org/GLM-5" target="_blank">GitHub</a>]
</p>

## 简介

我们推出 GLM-5.2——我们面向长时程任务的最新旗舰模型。相较前代 GLM-5.1，它在长时程任务能力上实现了重大飞跃，并首次在**坚实的 1M token 上下文**上交付这种能力。GLM-5.2 的新能力包括：
- **坚实的 1M 上下文**：稳固的 1M token 上下文，可稳定支撑长时程工作
- **支持灵活思考力度的先进编码**：更强的编码能力，提供多个思考力度级别以平衡性能与延迟
- **改进的架构**：我们提出 [IndexShare](https://arxiv.org/abs/2603.12201)，在每四个稀疏注意力层之间复用同一个索引器，在 1M 上下文长度下将每 token FLOPs 降低 2.9 倍。我们还改进了 GLM-5.2 用于投机解码的 MTP 层，将接受长度最多提升 20%
- **纯粹开放**：MIT 开源许可证——无地域限制，技术访问无国界

![bench_52](https://raw.githubusercontent.com/zai-org/GLM-5/refs/heads/main/resources/bench_52.png)

## 基准测试

|基准测试|GLM-5.2|GLM-5.1|Qwen3.7-Max|MiniMax M3|DeepSeek-V4-Pro|Claude Opus 4.8|GPT-5.5|Gemini 3.1 Pro|
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
|推理|||||||||||
|HLE|40.5|31|41.4|37|37.7|49.8*|41.4*|45|
|HLE (w/ Tools)|54.7|52.3|53.5|-|48.2|57.9*|52.2*|51.4*|
|CritPt|20.9|4.6|13.4|3.7|12.9|20.9|27.1|17.7|
|AIME 2026|99.2|95.3|97|-|94.6|95.7|98.3|98.2|
|HMMT Nov. 2025|94.4|94|95|84.4|94.4|96.5|96.5|94.8|
|HMMT Feb. 2026|92.5|82.6|97.1|84.4|95.2|96.7|96.7|87.3|
|IMOAnswerBench|91.0|83.8|90|-|89.8|83.5|-|81|
|GPQA-Diamond|91.2|86.2|90|93|90.1|93.6|93.6|94.3|
|编码|||||||||||
|SWE-bench Pro|62.1|58.4|60.6|59|55.4|69.2|58.6|54.2|
|NL2Repo|48.9|42.7|47.2|42.1|35.5|69.7|50.7|33.4|
|DeepSWE|46.2|18|18|20|8|58|70|10|
|ProgramBench|63.7|50.9|-|-|47.8|71.9|70.8|39.5|
|Terminal Bench 2.1 (Terminus-2)|81.0|63.5|75|65|64| 85|84|74|
|Terminal Bench 2.1 (Best Reported Harness)|82.7|69|-|-|-|78.9|83.4|70.7|
|FrontierSWE (Dominance)|74.4|30.5|-|-|29.0|75.1|72.6|39.6|
|PostTrainBench|34.3|20.1|-|-|-|37.2|28.4|21.6|
|SWE-Marathon|13.0|1.0|-|-|-|26.0|12.0|4.0|
|智能体|||||||||||
|MCP-Atlas (Public Set)|76.8|71.8|76.4|74.2|73.6|77.8|75.3|69.2|
|Tool-Decathlon|48.2|40.7|-|-|52.8|59.9|55.6|48.8|

## 本地部署 GLM-5.2

GLM-5.2 支持使用以下框架部署，欢迎试用：

- [SGLang](https://github.com/sgl-project/sglang)（v0.5.13.post1+）— 参见 [cookbook](https://cookbook.sglang.io/autoregressive/GLM/GLM-5.2)
- [vLLM](https://github.com/vllm-project/vllm)（v0.23.0+）— 参见 [recipes](https://recipes.vllm.ai/zai-org/GLM-5.2)
- [Transformers](https://github.com/huggingface/transformers)（v0.5.12+）— 参见 [transformers 文档](https://github.com/huggingface/transformers/blob/main/docs/source/en/model_doc/glm_moe_dsa.md)
- [KTransformers](https://github.com/kvcache-ai/ktransformers)（v0.5.12+）— 参见[教程](https://github.com/kvcache-ai/ktransformers/blob/main/doc/en/kt-kernel/GLM-5.2-Tutorial.md)
- [Unsloth](https://github.com/unslothai/unsloth)（v0.1.47-beta+）— 参见[指南](https://unsloth.ai/docs/models/glm-5.2)
- 若在 `Ascend NPU` 平台上部署，支持 vLLM-Ascend、xLLM 和 SGLang 等推理框架——参见[此处](github.com/zai-org/GLM-5/blob/main/example/ascend.md)。

## 脚注

* **Humanity’s Last Exam（HLE）及其他推理任务**：我们使用 `temperature=1.0`、`top_p=0.95` 的采样参数进行评测。评测的最大生成长度为 `163,840` 个 token。默认报告纯文本子集；带 * 的结果来自完整集。对于 AIME、HMMT 和 IMOAnswerBench，我们使用以下系统提示词评测每道题：`Your response should be in the following format:\nExplanation: {your explanation for your final answer}\nExact Answer: {your succinct, final answer}\nConfidence: {your confidence score between 0% and 100% for your answer}.` 我们使用 GPT-5.5（medium）作为判分模型。对于 HLE-with-tools，我们使用最大 300,000 token 的上下文长度，不使用上下文管理策略。
* **SWE-Bench Pro**：我们使用 OpenHands 及定制指令提示词运行 SWE-Bench Pro 套件。设置：`temperature=1`、`top_p=1`、`max_new_tokens=32k`，400K 上下文窗口。
* **NL2Repo**：我们在 400k 上下文下以 `temperature=1.0`、`top_p=1.0` 和 `max_new_tokens=48k` 评测 NL2Repo。为防止作弊，我们使用基于规则和基于 LLM 的判定来防止恶意行为（例如未经授权的 pip 或 curl 操作）。
* **DeepSWE**：我们使用官方 pier 评测框架和 mini-swe-agent 评测框架（`temperature=1.0`、`top_p=1.0`、`timeout=2h`、400K 上下文）运行 DeepSWE。每项任务在 2 CPU、8 GB 内存、无网络访问的隔离容器中求解。
* **ProgramBench**：我们使用 Claude-Code 2.1.156 评测 ProgramBench（200 个实例），参数为 `temperature=1.0, top_p=1.0, max_tokens=64000, max_turns=2000, sample_timeout=6h, reasoning_effort=max`，400K 上下文窗口。每个实例在（4 CPU、8 GB 内存）沙箱中运行，且禁用网络访问。
* **Terminal-Bench 2.1（Terminus 2）**：我们使用 Terminus-2 框架评测 Terminal-Bench 2.1，参数为 `parser=json`、`timeout=4h`、`temperature=1.0`、`top_p=1.0`、`max_new_tokens=48k`、`max_episodes=500`，256K 上下文窗口。资源限制上限为 4 CPU 和 8 GB 内存。
* **Terminal-Bench 2.1（Claude Code）**：我们在 Claude Code 2.1.167 中以 `temperature=1.0, top_p=0.95, max_new_tokens=131072` 进行评测。我们通过透明代理将 max_new_tokens 覆写为 128k，绕过 64k 的 CLI 上限，以恢复 `CLAUDE_CODE_MAX_OUTPUT_TOKENS` 的可配置性。我们移除了墙上时钟时间限制，但保留每任务的 CPU 和内存约束。得分为 5 次运行的平均值。
* **MCP-Atlas**：所有模型均在 500 任务的公开子集上以思考模式评测，每任务超时 10 分钟。我们使用 Gemini-3.0-Pro 作为判分模型。
* **Tool-Decathlon**：我们使用官方评测服务，并将 max_token 设为 128K。
* **FrontierSWE**：该评测由 [Proximal](https://www.proximal.ai) 使用 1M 上下文长度、max effort 级别和 128K 最大输出 token 完成。支配度得分截至 2026/06/16。
* **PostTrainBench**：该评测由 [PostTrainBench](https://posttrainbench.com) 使用 1M 上下文长度、max effort 级别和 128K 最大输出 token 完成。
* **SWE-Marathon**：该评测由 [Abundant AI](https://www.abundant.ai) 使用 1M 上下文长度、max effort 级别和 128K 最大输出 token 完成。

## 引用

如果您在研究中发现 GLM-5.2 有用，请引用我们的技术报告：

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
