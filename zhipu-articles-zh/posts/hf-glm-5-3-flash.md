---
title: "GLM-5.3-Flash 模型卡"
source: https://huggingface.co/zai-org/GLM-5.3-Flash
crawled: 2026-09-22
title_en: "zai-org/GLM-5.3-Flash model card"
translated: 2026-09-22
---

---
language:
- en
- zh
library_name: transformers
license: mit
pipeline_tag: image-text-to-text
---

# GLM-5.3-Flash 模型卡

> 原文：[zai-org/GLM-5.3-Flash model card](https://huggingface.co/zai-org/GLM-5.3-Flash) · 智谱 Z.ai

<div align="center">
<img src=https://raw.githubusercontent.com/zai-org/GLM-5/refs/heads/main/resources/logo.svg width="15%"/>
</div>
<p align="center">
    👋 欢迎加入我们的 <a href="https://raw.githubusercontent.com/zai-org/GLM-5/refs/heads/main/resources/wechat.png" target="_blank">WeChat</a> 或 <a href="https://discord.gg/QR7SARHRxK" target="_blank">Discord</a> 社区。
    <br>
    📖 了解 GLM-5.3-Flash <a href="https://z.ai/blog/glm-5.3-flash" target="_blank">博客</a>与 GLM-5 <a href="https://arxiv.org/abs/2602.15763" target="_blank">技术报告</a>。
    <br>
    📍 在 <a href="https://docs.z.ai/guides/llm/glm-5.3-flash">Z.ai API 平台</a>使用 GLM-5.3-Flash API 服务。
</p>

## 简介

我们推出 GLM-5.3-Flash——GLM-5 系列中首个原生多模态模型。它拥有 320B 总参数和仅 18B 激活参数，以十分之一的价格在各项基准和真实工作负载上超越 GLM-5.2，同时在编码和智能体（agentic）基准上逼近 Claude Opus 4.8。

GLM-5.3-Flash 从一个全新训练的基座模型出发，其架构与训练方案围绕能力与效率重新设计。GLM 系列首次引入结合稀疏注意力与线性注意力的混合架构，在保持精确长上下文能力的同时大幅降低长上下文服务成本。模型还采用流形约束超连接（Manifold-Constrained Hyper-Connections，mHC）以进一步提升扩展效率。配合我们最新的 30T token 多模态预训练语料，这些改进使 GLM-5.3-Flash 能够以更少的算力交付更多智能。

![bench_53](https://raw.githubusercontent.com/zai-org/GLM-5/refs/heads/main/resources/bench_53.png)


## 本地部署 GLM-5.3-Flash

GLM-5.3-Flash 支持使用以下框架部署，欢迎试用：

- [SGLang](https://github.com/sgl-project/sglang) — 参见 [cookbook](https://cookbook.sglang.io/autoregressive/GLM/GLM-5.3-Flash)
- [vLLM](https://github.com/vllm-project/vllm) — 参见 [recipes](https://recipes.vllm.ai/zai-org/GLM-5.3-Flash)
- [TokenSpeed](https://github.com/lightseekorg/tokenspeed) — 参见[此处](https://lightseek.org/tokenspeed/recipes/models#glm-5-3-flash)
- [Transformers](https://github.com/huggingface/transformers) — 参见 [transformers 文档](https://github.com/huggingface/transformers/blob/main/docs/source/en/model_doc/glm5_next.md)
- [KTransformers](https://github.com/kvcache-ai/ktransformers) — 参见[教程](https://github.com/kvcache-ai/ktransformers/blob/main/doc/en/kt-kernel/GLM-5.3-Flash-Tutorial.md)
- [Unsloth](https://github.com/unslothai/unsloth) — 参见[指南](https://unsloth.ai/docs/models/glm-5.3)

### 注意

- GLM-5.3-Flash 支持通过 `reasoning_effort` 参数控制思考预算，该参数接受三个级别：`low`、`high` 和 `max`。未传入（或设为任何其他值）时默认为 `max`。要使用 `low` 或 `high`，需显式传入。复现基准测试和排行榜结果时，请保持默认的 `max`。
- 在 GLM-5.3-Flash 的聊天模板中，`clear_thinking` 未传入时默认为 `false`。对话场景下请显式传入 `clear_thinking=true`。

## 脚注

* **HLE w/ tools（完整集）**：我们使用 `temperature=1.0` 和 `top_p=0.95` 的采样参数进行评测，最大生成长度为 `163,840` 个 token。评测在最大上下文长度 `300,000` 个 token 下进行，并使用上下文管理策略。我们使用 GPT-5.6-luna（medium）作为判分模型。
* **NL2Repo**：我们在 1M 上下文下以 temperature=1.0、top_p=1.0 和 max_new_tokens=64k 评测 NL2Repo。为防止作弊，我们使用基于规则和基于 LLM 的判定来防止恶意行为（例如未经授权的 pip 或 curl 操作）。
* **DeepSWE**：我们使用 mini-swe-agent 评测框架运行 DeepSWE，参数为 `temperature=0.95`、`top_p=1.0`、`timeout=6h`，上下文为 400K。
* **Terminal-Bench 2.1**：我们在 Claude Code 2.1.207 中以 temperature=1.0、top_p=1、max_new_tokens=65536 和 6 小时超时进行评测。
* **Agent’s Last Exam**：
* **Toolathlon Verified**：我们通过官方评测服务获取所有结果，并报告 3 次独立运行的 pass@1 平均值。
* **AutomationBench**：我们在 AutomationBench **v1.0.6** 上评测，包含 [PR #13](https://github.com/zapier/AutomationBench/pull/13) 中引入的 `null` 类型处理问题修复。
* **GDPval-AA v2**：模型由 Artificial Analysis 评测。
* **BabyVision**：我们使用 temperature=1.0、top_p=0.95，以及 164K token 的最大上下文长度。我们将输入图像调整为短边至少 1.5K 像素，与其他基线保持一致。

## 引用

如果您在研究中发现 GLM-5.3-Flash 有用，请引用我们的技术报告：

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
