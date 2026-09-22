---
title: "GLM-5.3 模型卡"
source: https://huggingface.co/zai-org/GLM-5.3
crawled: 2026-09-22
title_en: "zai-org/GLM-5.3 model card"
translated: 2026-09-22
---

---
language:
- en
- zh
library_name: transformers
license: other
license_name: glm-5.3
pipeline_tag: text-generation
---

# GLM-5.3 模型卡

> 原文：[zai-org/GLM-5.3 model card](https://huggingface.co/zai-org/GLM-5.3) · 智谱 Z.ai

GLM-5.3 与 GLM-5.2 使用相同的基座模型——所有提升都来自后训练。与 GLM-5.2 相比，它在复杂编码和长时程任务上明显更强：

+ 更强的编码能力：GLM-5.3 是目前编码能力最强的开放权重模型，在我们内部的 Z.ai Code Bench 上较 GLM-5.2 提升 50%。它还在 Terminal Bench 3.0、Agents' Last Exam 等公开基准上取得了开源 SOTA。
+ 涌现的网络安全能力：随着后训练规模的扩大，网络安全（cyber）能力的发展速度超出了我们的预期。GLM-5.3 在 CyberGym 漏洞发现上达到业界最先进水平，且越靠近漏洞利用链的后端环节提升越大——在漏洞利用（exploitation）基准上的成绩是 GLM-5.2 的两倍以上。

![bench_53](https://raw.githubusercontent.com/zai-org/GLM-5/refs/heads/main/resources/bench_53_2.png)

## 基准测试

| 基准测试                    | GLM-5.3   | GLM-5.2 | Kimi K3  | DeepSeek-V4 Pro-0813 | Qwen3.8-Max | Opus 4.8 | Fable 5 (w/ fallback) | GPT-5.6 Sol   |
|------------------------------|-----------|---------|----------|----------------------|-------------|----------|-----------------------|---------------|
| Terminal Bench 2.1           | 88.2      | 81.0    | 88.3     | 87.9                 | 86.6        | 85.0     | 88.0                  | **88.8**      |
| Terminal Bench 3.0           | 28.3      | 4.6     | 17.4     | –                    | –           | 21.1     | 33.7                  | **34.6**      |
| DeepSWE (v1.1)               | 66.9      | 46.2    | 67.5     | 62.7                 | 56.6        | 58.0     | 69.7                  | **72.7**      |
| NL2Repo                      | 58.0      | 48.9    | 58.0     | 61.1                 | 55.9        | **69.7** | –                     | –             |
| ProgramBench (Almost Solved) | 19.0      | 9.5     | 17.5     | –                    | 10.5        | 15.5     | **33.0**              | 23.0          |
| FrontierSWE                  | 78.1      | 67.5    | –        | –                    | –           | 66.5     | **88.2**              | –             |
| SWE-Marathon (v1.1)          | 42.5      | 19.4    | 48.1     | –                    | –           | **48.8** | 33.1                  | 42.5          |
| PostTrainBench               | 39.8      | 31.7    | 32.0     | –                    | –           | 32.9     | **41.8**              | 36.2          |
| CyberGym                     | **84.5**  | 77.2    | 80.0     | 83.3                 | 78.5        | 78.1     | 83.8                  | 83.6          |
| ExploitGym (2h / 6h)         | 105 / 130 | 29 / 39 | 36 / 70  | –                    | 14 / 26     | 80 / 120 | 181 / 247             | **216 / 293** |
| ExploitBench                 | 54.4      | 24.4    | 32.2     | –                    | 28.8        | 40.0     | **78.0**              | 76.5          |
| Toolathlon Verified          | 73.0      | 59.9    | **76.5** | 74.1                 | 72.5        | 76.2     | 74.7                  | 74.9          |
| AutomationBench (v1.0.6)     | **48.2**  | 26.2    | 46.7     | 43.2                 | 39.8        | 41.0     | 46.2                  | 45.8          |
| Agents' Last Exam (ALE-CLI)  | 28.5      | 23.8    | 27.6     | 25.7                 | 27.0        | 25.7     | 23.8                  | **28.6**      |
| HLE w/ Tools                 | 62.5      | 54.7    | 59.8     | 60.0                 | 56.2        | 57.9     | 63.9                  | **64.5**      |
| GDPval-AA v2                 | **1769**  | 1508    | 1682     | 1590                 | 1739        | 1588     | 1743                  | 1730          |

### 本地部署 GLM-5.3

GLM-5.3 支持使用以下框架部署，欢迎试用：

- [SGLang](https://github.com/sgl-project/sglang) — 参见 [cookbook](https://cookbook.sglang.io/autoregressive/GLM/GLM-5.3)
- [vLLM](https://github.com/vllm-project/vllm) — 参见 [recipes](https://recipes.vllm.ai/zai-org/GLM-5.3)
- [TokenSpeed](https://github.com/lightseekorg/tokenspeed) — 参见[此处](https://lightseek.org/tokenspeed/recipes/models#glm-5-3)
- [Transformers](https://github.com/huggingface/transformers) — 参见 [transformers 文档](https://github.com/huggingface/transformers/blob/main/docs/source/en/model_doc/glm_moe_dsa.md)
- [KTransformers](https://github.com/kvcache-ai/ktransformers) — 参见[教程](https://github.com/kvcache-ai/ktransformers/blob/main/doc/en/kt-kernel/GLM-5.2-Tutorial.md)
- [Unsloth](https://github.com/unslothai/unsloth) — 参见[指南](https://unsloth.ai/docs/models/GLM-5.3)
- 若在 `Ascend NPU` 平台上部署，支持 vLLM-Ascend、xLLM 和 SGLang 等推理框架——参见[此处](https://github.com/zai-org/GLM-5/blob/main/example/ascend.md)。

### 注意

- GLM-5.3 支持通过 `reasoning_effort` 参数控制思考预算，该参数接受三个级别：`low`、`high` 和 `max`。未传入（或设为任何其他值）时默认为 `max`。要使用 `low` 或 `high`，需显式传入。复现基准测试和排行榜结果时，请保持默认的 `max`。
- 在 GLM-5.3 的聊天模板中，`clear_thinking` 未传入时默认为 `false`。对话场景下请显式传入 `clear_thinking=true`。

## 脚注

- **HLE w/ tools**：我们使用 `temperature=1.0` 和 `top_p=0.95` 的采样参数进行评测，最大生成长度为 `163,840` 个 token。评测在最大上下文长度 `300,000` 个 token 下进行，并使用上下文管理策略。我们使用 GPT-5.6-luna（medium）作为判分模型。
- **NL2Repo**：我们在 1M 上下文下以 `temperature=1.0`、`top_p=1.0` 和 `max_new_tokens=64k` 评测 NL2Repo。为防止作弊，我们使用基于规则和基于 LLM 的判定来防止恶意行为（例如未经授权的 pip 或 curl 操作）。
- **DeepSWE**：我们使用 mini-swe-agent 评测框架运行 DeepSWE，参数为 `temperature=0.95`、`top_p=1.0`、`timeout=6h`，上下文为 400K。
- **Terminal-Bench 2.1**：我们在 Claude Code 2.1.207 中以 `temperature=1.0`、`top_p=1`、`max_new_tokens=65536` 和 6 小时超时进行评测。
- **Terminal-Bench 3.0**：我们使用 Claude Code 2.1.207 评测框架（reasoning effort=max、400K 上下文、128K 最大输出）评测 Terminal-Bench-3 任务，报告每项任务三次 rollout 的 avg@3。每次 rollout 都在基于任务官方镜像构建的隔离容器中运行，上限为 600 个智能体回合和 10 小时超时。工具搜索（Tool Search）被禁用，每个智能体产出的工件由任务官方的独立验证器评分。
- **Agent's Last Exam (CLI)**：我们使用官方评测协议和 Claude Code 评测框架（reasoning effort=max、1M 上下文、64K 最大输出）评测 ALE。全部 105 项任务分别在隔离的 Docker 容器中运行，使用其任务卡（Task Card）中声明的资源。默认超时为 4 小时，任务特定的限制优先（最长 8 小时）。工具搜索被禁用，结果由官方 ALE 评测器评分。
- **Toolathlon Verified**：我们通过官方评测服务获取所有结果，并报告 3 次独立运行的 pass@1 平均值。
- **AutomationBench**：我们在 AutomationBench **v1.0.6** 上评测，包含 [PR #13](https://github.com/zapier/AutomationBench/pull/13) 中引入的 `null` 类型处理问题修复。
- **GDPval-AA v2**：模型由 Artificial Analysis 评测。
- **CyberGym**：我们在 Claude Code 2.1.207 中评测 GLM-5.3（max reasoning effort、无网络工具，`temperature=1.0`、`top_p=1.0`、`max_new_tokens=128000`）。所有评测均不设任务超时限制，结果为 1,507 项任务上的单次运行 Pass@1。为模拟真实使用场景，我们将智能体置于任务容器内。我们还移除了所有 Git 相关信息，并施加域名白名单（仅允许 pypi.org、deb.debian.org 等安装基础工具所需的关键域名），以防止智能体作弊。
- **ExploitGym**：我们在 Claude Code 2.1.207 中评测 GLM-5.3、Kimi-K3 和 Qwen3.8 Max（max reasoning effort、无网络工具，`temperature=1.0`、`top_p=1.0`、`max_new_tokens=128000`）。所报告的结果是 869 项任务在两种超时预算（2 小时和 6 小时）下的单次运行 Pass@1，其计算方式为：按各模型每秒 token 速率对 API 推理时间进行折算（各模型 TPS 来自 Artificial Analysis；即我们以 115 TPS 折算 GLM-5.3 的结果、以 40 TPS 折算 Kimi K3 的结果、以 47 TPS 折算 Qwen3.8 Max 的结果），再加上非 API 开销。我们同样施加域名白名单（仅允许 pypi.org、deb.debian.org 等安装基础工具所需的关键域名），以防止智能体作弊。
- **ExploitBench**：我们在 Claude Code 2.1.207 中评测 GLM-5.3（max reasoning effort、无网络工具，`temperature=1.0`、`top_p=1.0`、`max_new_tokens=128000`）。遵循官方评测设置，我们将智能体与环境之间的最大交互轮数限制为 300，并计算 3 次修订在全部 41 项任务上的平均覆盖率得分。任务的覆盖率结果由所有修订中达成的能力取并集确定，再对结果取平均得到平均分。我们同样施加域名白名单（仅允许 pypi.org、deb.debian.org 等安装基础工具所需的关键域名），以防止智能体作弊。
- **FrontierSWE**：该评测由 [Proximal](https://www.proximal.ai/) 使用 1M 上下文长度、max effort 级别和 128K 最大输出 token 完成。支配度（Dominance）得分截至 2026/08/14。
- **PostTrainBench**：我们使用 Claude Code 2.1.207 评测 GLM-5.3，max effort 级别、`temperature = 1.0`、`top_p = 1.0`、`max_new_tokens = 128000`、1M token 上下文窗口。我们报告 3 次运行的加权平均值。未能产生得分的运行回退到官方零样本基座模型基线得分。对于旨在防止使用第三方 API 的检查，我们移除了原先基于模式匹配的检查，因为当通过 OpenAI SDK 访问本地 vLLM 端点时它会产生误报；取而代之，我们使用一个 LLM 智能体来检查解决方案是否使用了外部 API。
- **SWE-Marathon**：我们使用 Claude Code 2.1.207 评测 GLM-5.3，max effort 级别、`temperature = 1.0`、`top_p = 0.95`、`max_new_tokens = 128000`、1M token 上下文窗口。对于 `strip-clone`，原有的反作弊检查使用了过于宽泛的导入检测，可能拒绝合法实现；我们移除了受影响的检查，改为进行基于 LLM 的审查以避免误报。对于 `parameter-golf` 和 `trimul-cuda`，NVIDIA wheel 的变更导致 Docker 镜像构建失败，因此我们添加了 `--extra-index-url https://pypi.org/simple` 以恢复成功构建。

## 引用

如果您在研究中发现 GLM-5.3 有用，请引用我们的技术报告：

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
