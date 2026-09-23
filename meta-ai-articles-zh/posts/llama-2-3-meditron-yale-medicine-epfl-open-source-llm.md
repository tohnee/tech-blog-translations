---
title: "Meditron：基于 Meta Llama、特别适合低资源医疗场景的 LLM 套件"
title_en: "Meditron: An LLM suite especially suited for low-resource medical settings leveraging Meta Llama"
date: 2024-04-25
source: https://ai.meta.com/blog/llama-2-3-meditron-yale-medicine-epfl-open-source-llm
crawled: 2026-09-22
translated: 2026-09-22
---

# Meditron：基于 Meta Llama、特别适合低资源医疗场景的 LLM 套件

> 原文：[Meditron: An LLM suite especially suited for low-resource medical settings leveraging Meta Llama](https://ai.meta.com/blog/llama-2-3-meditron-yale-medicine-epfl-open-source-llm) · Meta AI（Wayback 存档）

在医学中，在正确的时间、正确的地点获取正确的信息可以决定一切——从决定采取预防措施，到在需要时求医、及时获得诊断、遵处方用药。Meditron 是一套专为医疗领域定制的开源大型多模态基础模型，旨在辅助临床决策与诊断。它构建于 Meta Llama 2 之上，用精心策展的高质量医疗数据源训练，并持续获得临床医生与人道主义响应专家的输入。EPFL 计算机与通信学院和耶鲁医学院的研究者联手开展该项目，并与红十字会国际委员会（ICRC）等人道组织紧密合作。Meditron 发布后头几个月下载量已超过 30,000 次，填补了低资源医疗场景创新的重要空白。而在上周 Meta Llama 3 发布后，团队在 24 小时内完成了新版 8B 模型的微调，推出 Llama-3[8B]-MeditronV1.0——在 MedQA、MedMCQA 等标准基准上，它超越了同参数量级的所有最先进开放模型。

「基础模型已经成为当代的智力与文化资产，」共同领导该项目的耶鲁教授 Mary-Anne Hartley 说，「应用于医疗领域时，它们有潜力提供挽救生命的建议与指导。然而，资源最匮乏的场景获益最大，却仍然代表性最低。」

像 Llama 这样的 LLM 可以把复杂信息压缩进一个易于使用的对话界面。Meditron 对 Llama 2 做了适配，确保其提供的信息更好地契合循证医疗、结合情境的建议以及专业标准。Meditron 套件有望满足多种场景的关键需求，包括需要快速准确医疗响应的紧急情况，以及协助医疗不足地区的医护工作者诊断和治疗患者。Hartley 说，希望通过完全开放访问、开源地发布它——从数据到权重，并附带清晰的上手文档——让资源受限场景也能开展创新，更好地确保代表性，并为医学知识创造公平的获取渠道。「低资源场景不应被迫『重新发明轮子』，才能让它们的人群与需求在这项关键技术中得到代表，」Hartley 说。

## 当资金是问题时，从小处着手、专注质量

资金对任何人都是挑战，对从事人道主义与低资源工作的团队尤其如此。Hartley 说，团队选择不商业化，以保持公正验证所需的中立性。为节约成本，实验先在较小的 Llama 2 7B 上进行，筛选出最优的预训练数据混合与参数，再扩展到 70B。这种保守的做法也是团队同时发布 7B 与 70B Meditron 模型的原因。Hartley 指出，Meditron 7B 虽然性能稍逊，但对建模实验的规模放大仍非常有用。多模态实现也遵循了类似路径。Meditron 7B 集成了图像解读，虽然前景极为可观（在医学图像解读上超越了 562B 的 Medpalm M），但在 70B 上会更好，值得投入，Hartley 说。

这种「质优于量」的取向也意味着，团队把大部分时间花在精心策展经过医学验证的文本文档上，这些文档代表了高资源与低资源场景下的循证指南。Hartley 说，持续预训练（continued pretraining）会更新模型的全部参数，而不只是针对微调的一部分，从而把 Llama 训练所用通用文本语料带来的污染与偏见风险降到最低，同时最大化医学知识的留存。由于在多 GPU、多节点集群上进行持续预训练技术难度极高，团队把 Llama 架构集成进了高性能分布式训练器 Megatron-LM。意识到许多其他人也可能遇到这个问题，他们确保开源了适配版 Megatron。

## 通过开放验证与评估检验 Meditron

Hartley 说，Meditron 工作到目前为止最激动人心的现实成果，是世界各地医疗专业人士与人道组织大规模报名参加 Meditron MOOVE（Massive Online Open Validation and Evaluation，大规模在线开放验证与评估）的兴趣。来自世界各地、尤其是低资源场景的医生向 Meditron 提出刁钻问题并严格评估其答案，以便团队据此调整模型。Hartley 表示，按照该领域的主流基准（如生物医学考试问答），Meditron 目前是医学领域表现最好的开源 LLM。团队之所以选择 MOOVE，是为了让社区意识到这些基准并不能完全代表真实的临床医学实践，以及低资源场景和人道响应中的挑战。「这些时间宝贵的专业人士在我们的开源社区志愿投入时间、独立验证 Meditron，正是对其价值的认可，」Hartley 说，「我们处在一个独特的位置，可以把所有这些反馈融入一个新模型。我们希望资助者能认识到投资我们这个学术开源计划的社会与商业价值。」

Hartley 说，开源技术在赋能创新方面有着经过时间检验的历史，而且关键在于让创新可公平获取。「我们不断听到低资源场景的研究者讲述 Meditron 如何助力了他们的研究，」她解释道，「开源并不新鲜，新鲜的这次贡献的规模与成本。我们需要更大胆地为这类努力寻求中立的慈善支持。」

分享你的 Llama 故事
