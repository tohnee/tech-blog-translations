---
title: "inclusionAI/PolyOCR-Venus"
title_en: "inclusionAI/PolyOCR-Venus"
source: https://github.com/inclusionAI/PolyOCR-Venus/blob/main/README.md
crawled: 2026-10-15
translated: 2026-10-15
---

<p align="center">
  <img src="assets/antgroup-logo.png" width="28%" alt="Ant Group">
</p>

---

<p align="center">
  <a href="docs/PolyOCR-Venus.pdf">📄 技术报告</a> •
  <a href="#overview">✨ 概览</a> •
  <a href="#benchmark-results">📊 结果</a> •
  <a href="evaluation/ocrbench_v2/README.md">🛠️ 评估指南</a> •
  <a href="#citation">📚 引用</a>
</p>

<h2 align="center">
  PolyOCR-Venus：统一 OCR 基础模型<br>
  面向以文本为中心的视觉智能
</h2>

<p align="center"><b>蚂蚁集团 GuangJian 团队</b></p>

<p align="center">
  <img src="assets/benchmark-results.png" width="100%" alt="PolyOCR cross-benchmark comparison on OCRBench v2.1, CC-OCR, OmniDocBench v1.6, in-house KIE, and MDPBench">
</p>

*在 OCRBench v2.1、CC-OCR、OmniDocBench v1.6、内部 KIE 与 MDPBench 上的跨基准对比。OmniDocBench 采用 PolyOCR-9B 的版面引导流水线；MDPBench 采用 PolyOCR-2.7B。CC-OCR 不含多语言 OCR，截断的坐标轴已作标记。端到端分数与协议细节见[基准结果](#benchmark-results)。*

**PolyOCR-Venus** 将文本识别、定位、文档解析、信息抽取、多语言转换以及以 OCR 为中心的推理，统一进一个遵循指令的模型家族。

## 发布

- **2026-09-21：**技术报告与 OCRBench 评估代码已在本仓库提供，同时附有依赖文件与安装指南。

## 目录

- [概览](#overview)
- [能力](#capabilities)
- [训练框架](#training-framework)
- [基准结果](#benchmark-results)
- [评估](#evaluation)
- [引用](#citation)
- [致谢](#acknowledgments)
- [许可证](#license)

## 概览

PolyOCR 是基于 **Qwen3.5** 视觉-语言骨干构建的 **2B 与 9B** OCR 基础模型家族。统一的遵循指令接口支持一系列任务，从读取单个文本区域，到恢复文档结构、对视觉文本进行推理。

- **统一的 OCR 能力。**六大能力组覆盖文本感知、空间定位（grounding）、结构化理解、抽取、转换与推理，横跨场景、文档、表格、图表与示意图。
- **大规模 OCR 数据构建。**在精选 OCR 资源之外，辅以受控合成、模型辅助标注与质量校验，构成约 **6000 万条 SFT 实例**的语料。
- **能力引导的策略优化（CGPO）。**后训练将基于验证器的组相对策略优化（GRPO）与自适应的 on-policy 蒸馏相结合，依据教师模型的可靠性与师生能力差距来路由教师监督。

[技术报告](docs/PolyOCR-Venus.pdf)介绍了模型家族、数据构建、训练方法，以及在 OCRBench v2.1、CC-OCR 与 OmniDocBench v1.6 上的评估。当前提供的代码是 [OCRBench 评估模块](evaluation/ocrbench_v2/README.md)；模型权重、训练代码以及 CC-OCR/OmniDocBench 流水线未包含在本次发布中。

## 能力

| 能力 | 代表性任务 |
| --- | --- |
| 文本识别 | 场景文本、手写体、多语言 OCR、整页转录 |
| 文本定位与检出（spotting） | 检测、grounding、指代文本定位、区域识别、文本检出（text spotting） |
| 结构化文档理解 | 版面与阅读顺序、文档解析、表格、公式、图表 |
| 信息抽取与语义关系 | 实体抽取、关键信息抽取、键值关联、表单 |
| 视觉文本理解与转换 | 文档 VQA、图表/表格理解、分类、翻译 |
| 以 OCR 为中心的推理 | 计数、对可见数值做算术、空间推理、多步推断 |

## 训练框架

<p align="center">
  <img src="assets/train.png" width="100%" alt="PolyOCR training: three-phase curriculum SFT followed by CGPO combining GRPO and competence-routed on-policy distillation">
</p>

1. **课程式监督微调。**约 6000 万条实例被组织为三个阶段。课程逐步把重心从文本感知与文档结构转向 OCR 理解与推理，同时保留通用的多模态对齐数据。
2. **能力引导的后训练。**CGPO 使用验证器奖励来估计学生模型的能力，使用缓存的教师生成结果来估计教师模型的能力。一个经过校准的路由器控制每个样本的蒸馏权重；基于验证器的 GRPO 全程保持启用。两个模型规格在该阶段均使用 Qwen3.5-122B-A10B 作为教师。

数据引擎、路由公式与训练设置详见技术报告。

## 基准结果

下表展示技术报告中精选的**端到端**结果。每一列均为数值越高越好。

| 模型 | OCRBench v2.1 EN | OCRBench v2.1 ZH | CC-OCR | OmniDocBench v1.6 |
| --- | ---: | ---: | ---: | ---: |
| Qwen3.5-2B | 54.03 | 63.75 | 65.66 | 79.95 |
| Qwen3.5-9B | 66.64 | 71.88 | 71.44 | 89.49 |
| **PolyOCR-2B** | **72.33** | **71.32** | **80.53** | **88.12** |
| **PolyOCR-9B** | **80.42** | **78.87** | **82.43** | **91.57** |

**版面引导的文档解析。**在 PP-DocLayoutV3 提供版面区域与阅读顺序的情况下，PolyOCR-9B 解析裁切出的文本、公式与表格区域，并将结果组装为 Markdown。该流水线在 OmniDocBench v1.6 上达到 **95.48**，相比之下直接整页推理为 **91.57**。

**OCRBench 协议。**在本报告中，**OCRBench v2.1** 指我们对 OCRBench v2 的修订版：经审核与修正的参考标注，加上与任务对齐的评分流程。它保留了原始的任务覆盖范围。这些分数只能与使用相同修订标注与协议的结果进行比较；原始 OCRBench v2 分数不可直接比较。报告附录记录了全部改动。

## 评估

OCRBench 评估是 PolyOCR 项目的组成部分之一。实现代码组织在 [`evaluation/ocrbench_v2/`](evaluation/ocrbench_v2/README.md) 之下，包括：

- PolyOCR 两阶段推理配置：解析/识别关闭 thinking，问答/推理开启 thinking。
- 兼容 OpenAI 的 API 推理，支持可断点续跑与预测结果导出。
- OCR、VQA、文档/表格/公式解析、关键信息抽取、定位与检出（spotting）的评分，包括 TEDS 与 CDM。
- 翻译/问答评判、子集重评分、结果合并与依赖检查。

修订版数据集以 `evaluation/ocrbench_v2/data/ocrbench_v21.tsv` 的形式随仓库提供（10,000 个样本，内嵌 base64 图像；因约 1.4 GB 体积而以 Git LFS 存储）。要复现报告中的 **v2.1** 协议，请使用该数据集，并配合评估指南所述的相应评分/评判设置。模型权重与 API 凭证需另行提供。

### 安装

在装有 Python 3.11 或更新版本的 Linux 环境中，于仓库根目录下运行：

```bash
# Fetch the OCRBench v2.1 dataset (requires Git LFS)
git lfs install
git lfs pull

python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

| 依赖文件 | 用途 |
| --- | --- |
| [`requirements.txt`](requirements.txt) | 完整 OCRBench 评估环境的默认入口 |
| [`requirements_api.txt`](evaluation/ocrbench_v2/requirements_api.txt) | 仅独立 API 推理 |
| [`requirements_vllm.txt`](evaluation/ocrbench_v2/requirements_vllm.txt) | 本地 vLLM 推理与评估 |

完整评分还需要用于 CDM 的 TeX Live 组件，以及用于手写体指标的 NLTK 语料。数据准备、API 配置、推理、评分与依赖检查请遵循**[评估指南](evaluation/ocrbench_v2/README.md)**。

### 仓库结构

```text
PolyOCR-Venus/
├── README.md
├── requirements.txt
├── assets/                         # Project logos and report figures
├── docs/
│   └── PolyOCR-Venus.pdf
└── evaluation/
    └── ocrbench_v2/                 # Evaluation code, configs, scripts, and guide
```

## 引用

如果您在研究中使用了 PolyOCR 或其评估协议，请引用技术报告：

```bibtex
@article{team2026polyocr,
  title={PolyOCR-Venus: Unified OCR Foundation Models for Text-Centric Visual Intelligence},
  author={Team, GuangJian and Huang, Kaili and Zhang, Yongshuo and Fu, Bingtao and Jiang, Changjiang and Qu, Chenfan and Zhang, Chenfeng and Cui, Fangming and Zhang, Gaoyang and Xie, Jiangwei and others},
  journal={arXiv preprint arXiv:2609.37712},
  year={2026}
}
```

## 致谢

PolyOCR 构建在 Qwen3.5 之上，使用 OCRBench、CC-OCR 与 OmniDocBench 进行评估。随附的评估框架改编自 VLMEvalKit；其[上游文档](evaluation/ocrbench_v2/README.upstream.md)、[许可证](evaluation/ocrbench_v2/LICENSE)与[源码清单](evaluation/ocrbench_v2/SOURCE_MANIFEST.json)随代码一并保留。

## 许可证

本项目的开源代码以 **GPL-2.0** 许可证发布。**OCRBenchV2.1** 以 **MIT** 许可证发布。第三方组件保留其原始许可证；随附的 VLMEvalKit 框架以 Apache-2.0 许可（见[其许可证](evaluation/ocrbench_v2/LICENSE)）。
