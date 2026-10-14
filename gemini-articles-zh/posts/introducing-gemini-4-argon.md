---
title: "Gemini 4 Argon：为攻克你最棘手的难题而生"
title_en: "Gemini 4 Argon: Built to solve your hardest problems"
source: https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-argon/
site: gemini
date: 2026-10-13
crawled: 2026-10-15
translated: 2026-10-15
---

# Gemini 4 Argon：为攻克你最棘手的难题而生

> 原文：[Gemini 4 Argon: Built to solve your hardest problems](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-argon/) · Google

[Gemini 4 Argon](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-argon/) 今天起向全球开放：开发者和企业可通过 [AI Studio](https://ai.google.dev/aistudio) 和 Gemini 平台使用 API；[Google AI Ultra 订阅用户](https://one.google.com/about/google-ai-plans/)可在 [Google Antigravity](https://antigravity.google/) 中使用；Google AI Ultra 和 Pro 订阅用户则可在 [Gemini 应用](http://gemini.google/)以及 [Search 中的 AI Mode](http://aimode.google/) 中使用。

Argon 擅长在编程、金融、法律、网络安全和科学等领域完成复杂真实世界任务中的深度工作。凭借在多步骤任务上的深度与精准，Argon 在[各领域基准测试](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-argon/#workingharder)中超越了其他前沿模型，并在 [Vals Index](https://www.vals.ai/benchmarks/vals_index) 上排名第一——该指数衡量模型在金融、编程、法律与税务等关键经济部门的表现。

模型今日以[入门价格](https://aistudio.google.com/docs/pricing) [1](#footnote-1) 上线：每百万输入 token 2 美元、每百万输出 token 10 美元（缓存输入 token 减免 95%）。

Google 内部团队、各企业以及研究社区已经在用 Argon 在各个领域取得显著成效：

- 解决大规模代码库重构与优化等重大工程问题
- 优化法律、金融、科学等领域的业务工作流
- 发现并修补关键的网络安全漏洞
- 在量子计算、核聚变和生命科学领域实现新的突破

## 攻克复杂工程任务

在 Google，我们一直把 Argon 用在最难的工程问题上。过去几周，软件工程师们以前所未有的速度交付着高质量代码。Antigravity 中的 Argon 帮助团队将智能体化代码提交量提高了 35% 以上，同时把代码回滚率降低了近三分之一。

- **梳理 Chrome 浏览器功能代码：**Argon 帮助 Chrome 团队把核心网页处理逻辑从 Chromium 4000 万行代码库中一个约 600 万行的浏览器功能遗留目录中剥离出来。[通过一次接入多条干净的代码变更](https://issues.chromium.org/issues/540709814)，Argon 帮助团队完成了一场横跨数百个文件的架构重构，把数月的工作压缩到数周内完成。对于 Chrome 全球数十亿用户而言，这将让网页无需重新加载即可在标签页、侧边栏和浮动窗口之间流畅移动，消除一整类浏览器崩溃。

- **数小时内优化生产级 Python 代码库：**Google 的开源项目 [Agent Development Kit](https://github.com/google/adk-python)（ADK）是支撑企业智能体的框架，Antigravity 中的 Argon 正在帮助其背后的团队进一步推进性能工程。团队把他们的 [.agents/skills](https://github.com/google/adk-python/tree/main/.agents/skills) 规则手册和一段话的目标交给 Argon：在不破坏现有应用的前提下消除框架开销。Argon 连夜自主工作，找出了多项优化，[现已在 google/adk-python 上线](https://github.com/google/adk-python/commit/1754b3eeb6cdb2c16e3b30619a12066623df132e)：长会话中内存会话准备时间减少 40%，冷启动导入速度提升 21%。详情可阅读[这篇工程深度解析](https://developers.googleblog.com/optimizing-a-200000-line-python-codebase-overnight-with-gemini-4-argon)。
- **量子化学开源软件包优化：**xTB（Semiempirical Extended Tight-Binding，半经验扩展紧束缚方法）是分子量子化学领域被引用最多的开源软件包之一。科学家用它来预测分子的三维形状，并筛选大量药物与材料候选。借助 Antigravity 中的 Argon，我们的研究人员让 xTB 预测分子结构的速度最高提升 2.3 倍，构象搜索速度提升 1.8 倍。相关改动已贡献到 [GitHub 上的官方 xTB 仓库](https://github.com/grimme-lab/xtb/pulls?q=is%3Apr+author%3Ag8j39+%28created%3A%3E2026-10-05+created%3A%3C2026-10-10%29)。
- **让我们的开放模型 Gemma 快了近三倍：**借助 Argon，我们仅用几天就实现了在 A100 上通过 vLLM 获得 2.85 倍端到端推理加速（Gemma 4 E2B 的吞吐量从约 37,900 token/秒提升至超过 108,000 token/秒），且 token 完全一致、零质量损失——这一过程通常需要数月。具体改动可查看[上游 pull request](https://github.com/vllm-project/vllm/pulls?q=is%3Apr+author%3Alucianommartins+%28created%3A%3E2026-10-05+created%3A%3C2026-10-10%29)（从注意力调优到投机解码的各类优化）。
- **呈现复杂 3D 可视化：**与之前的 Gemini 模型相比，Argon 在空间推理、数学精度和可视化编程方面带来重大提升。通过在 Antigravity 中使用 /goal 之类的斜杠命令，并提示配合自定义技能的多智能体循环，Google 员工正在用 Argon 以原生代码快速构建复杂 3D 可视化、高保真游戏和交互式动画的原型，并可直接在浏览器中渲染。

Argon 在 Antigravity 中通过多智能体视觉评审循环打造了一座细节极其丰富的宝塔模型。模型在 Blender 中自主雕琢出一座包含多栋建筑的寺庙建筑群，具备照片级真实的建筑、植被与光照。

在 Antigravity 中，Argon 通过多智能体循环把一张真实书桌的照片变成了可玩的迷你赛车游戏。桌面物品、房间和赛道使用 Blender MCP 建模并做碰撞检测，用 Nano Banana 制作贴图，并在 Three.js 中接入物理效果、自定义着色器以及来自 Gemini Omni Flash 的汽车引擎音效。在 Google AI Studio 中[立即试用](https://aistudio.google.com/apps/bundled/desk-racer?showAssistant=true&showPreview=true&fullscreenApplet=true)。

Antigravity 中的 Argon 编写 Python 脚本，借助多智能体视觉评审循环，以程序化方式雕琢、绑定骨骼、制作动画并烘焙 PBR 材质，构建出一款复杂 3D 游戏，随后在 Three.js 中接入 GLSL 着色器、碎裂物理效果和单机 AI，将其适配到网页端。在 Google AI Studio 中[立即试用](https://aistudio.google.com/apps/bundled/wizard-chess-3d?showAssistant=true&showPreview=true&fullscreenApplet=true)。

Argon 在零外部依赖、100% 纯 Python 的条件下，自行编写了 3D 光线追踪引擎，并配上自定义视频工具和音频混音器，从零开始构建并记录一座阳光洒落的图书馆，用 Gemini 3.8 TTS 配音和 Lyria 3.5 的音乐制作、旁白并剪辑了这段视频。[查看源代码](https://github.com/google-gemini/gemini-4-demo-vanilla-3D)。

在 Antigravity 中，Argon 从一张 Nano Banana 图像出发，在自主循环中驱动 Blender MCP，对齐相机网格、雕琢哥特式建筑、布置随音频律动的灯光，最终生成一个完整的 3D 场景。

## 变革关键业务与专业工作流

Argon 融合了前沿推理、深度视觉感知、更广的领域知识和更强的写作能力，覆盖法律、金融、科学和编程，助力高风险专业工作流。它的表达清晰、让你随时知情，对风格指令的遵循优于以往任何一款 Gemini 模型。Argon 回答问题更直接、更少含糊其辞，不作不必要的重复，并在整篇回复中避免陈词滥调。

参与我们早期访问计划的企业客户和初创公司已经在 Argon 身上收获了出色成果。

凭借先进的推理与多模态能力，同时保持严格的锚定（grounding），Argon 在深度多模态文档理解、纵向数据分析和交互式分析沙箱方面表现出色。

看看 Argon 如何综合约 50 GB 的机载激光雷达扫描数据、GIS 房间矢量数据、美国国会图书馆 CAD 图纸和国家公园管理局（NPS）档案，重建查科峡谷（Chaco Canyon）的 3D 模型，把零散的考古记录变成可探索的数字遗产站点。在 Google AI Studio 中[立即试用](https://aistudio.google.com/apps/bundled/chaco-canyon-3d?showPreview=true&showAssistant=true&fullscreenApplet=true)。

在 Gemini 应用中，Argon 接手一个满是项目背景资料的非结构化文件夹，用自定义技能将其整理成一份给客户的清晰提案演示文稿，随后起草并把它通过邮件发给客户，还通过定时任务为今后所有新进客户请求创建了自动化工作流。

看看 Argon 如何把 3 个开源仓库的数据整合成一个医学学习工具：在 3D 人体探索中，你可以层层剥开解剖结构、查看临床元数据，并触发生物力学演示。

在 Gemini macOS 应用中，Argon 借助 Antigravity 用 Nano Banana 为沙发新腿部生成设计迭代，然后为其中一款生成可 3D 打印的文件。从一张标有尺寸的草图和沙发照片出发，Argon 按正确尺寸建模，使其恰好适配这张沙发。

在 Isomorphic Labs，团队正把 Argon 当作合作伙伴，加速药物发现与设计研究工作流。Argon 能够快速综合复杂 PDF 和专利以提取关键信息，把通常需要数周的过程缩短到几个小时。

## 与研究者和领域专家一起加速真实世界影响

研究者、工程师和安全专家已经在用 Argon 推进网络防御、科学、数学和机器人技术的边界。它帮助网络防御者和研究者检验假设、自主审计关键代码库和形式化证明，并捕捉隐蔽的零日漏洞与逻辑缺陷。

### 把最先进的网络能力带给更多受信任的防御者

从今天起，我们开始向数百个新的 [Fairwind Program](https://deepmind.google/fairwind-program/) 合作伙伴扩展访问。

[Wiz](https://www.wiz.io/) 已经在其「[Scan for Good](https://www.wiz.io/blog/scan-for-good-critical-ai-exposures)」计划中使用 Argon——该计划免费为公共利益保护关键基础设施。借助模型的早期访问，Wiz 已在多个高风险领域展示了 Argon 的真实世界影响：

- **保护敏感政府数据：**作为一项长期网络韧性计划的一部分，Argon 与一家联邦机构合作，帮助主动识别并修复了一个可能暴露敏感数据和政府基础设施的缺口。这项工作帮助防止了安全部门关键开发细节的泄露，以及对专用模型的未授权访问。
- **保护关键医疗基础设施：**Wiz 还用 Argon 保护重要的医疗基础设施。通过串联多个复杂漏洞，模型帮助团队发现并快速修复了一个公开文件下载绕过漏洞——该漏洞暴露了主密钥并授予管理员访问权限。Argon 不止于发现漏洞，更主动守护了数十万条私人患者记录。

### 解锁新的科学突破

Argon 已经在整个科学界产生真实世界影响——助力多个领域的科学家和专家实现全新发现。

- **量子计算：**Argon 正在帮助我们的研究人员在量子纠错和算法设计两方面加速进展。为了让错误解码器能实时跟上量子硬件，Argon 把我们的机器学习量子纠错解码器 [AlphaQubit](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/alphaqubit-quantum-error-correction/) 的内部版本翻译成单一的高度优化硬件内核——推理吞吐量接近翻倍，使我们既能部署更大、能力更强的模型、扩展到更大的量子设备，又继续满足严格的实时性阈值。Argon 还在降低量子子程序的时空开销。以 arcsin（近期量子模拟算法的一个基础构件）为例，由 Argon 编写并经 Lean 形式化验证的实现，相比已发表的量子 CORDIC 基线，将时空开销降低超过 100 倍，这是迈向优化量子电路标准库的一步。
- **核聚变：**仿星器（stellarator）是极其复杂的机器，是无尽清洁聚变能源的主要候选方案之一，但优化其三维磁场以难度著称。自 1967 年以来，一个名为「Grad 猜想」的长期假设认为不可能为这些磁场找到精确的数学解，直到近期反例被发现，其中包括马里兰大学的 Matt Landreman 教授的成果。如今，Google 的一支团队与 Landreman 教授一起发现了[一类更广泛的 Grad 猜想反例](https://arxiv.org/abs/2610.07304)。这些新解为聚变界提供了可靠的基准来测试他们的仿星器模拟代码，而模拟代码正是未来设计的宝贵工具。
- **罕见病研究：**Gamow Labs 的研究人员用 Argon 分析患有罕见发育性肺病的新生儿的去标识化基因组。在一个案例中，Argon 精准定位了一个常规软件多年都未能发现的染色体重排，并解释了它为何一直未被检出。在基于真实临床和实验数据构建的 Gamow Labs 私有评测中，Argon 在 [RareBench](https://gamowlabs.com/benchmarks)（罕见病诊断辅助 57%）和 [LabBench](https://gamowlabs.com/benchmarks)（湿实验室推理 52.2%）上均排名第一。这些进展意味着面临罕见病困扰的家庭能更快获得诊断。详情参见[博客](https://gamowlabs.com/bringing-expert-genome-interpretation-to-every-nicu) [2](#footnote-2)。
- **酶设计：**设计具有精确反应性的酶出了名地慢，通常需要数月的定制模型调优和候选筛选。丝氨酸酯酶（serine esterase）是一类能切断目标分子上酯键的酶，广泛用于回收，以及制药、生物燃料和洗涤剂的制造。我们的科学家与 Argon 合作设计丝氨酸酯酶，针对基准分子 4MU-乙酸酯（4MU-acetate）——它的酯键一旦断裂就会在紫外光下发光。Argon 在数小时内完成了相关数据的汇集、模型调优，并确定了多个受生物化学启发的过滤条件，最终得到五个全新的设计。随后的实验室测试证实这些设计均具有稳健的催化活性。如此快速、便捷地成功生成酶，展示了酶工程在生物制造、绿色化学和药物开发等领域快速加速的潜力。

为进一步加快研究步伐，我们将向 10,000 名科学家免费提供 6 个月 Google Antigravity 最高用量档位的访问（滚动接入），以资格、容量和遴选为准。申请[现已开放](https://forms.gle/WvmBbPvRbpKG1BPn9)。

### 加速机器人技术发展

通过融合先进的视觉-语义推理、深入的物理理解和自主代码生成，Argon 在机器人技术栈各环节解锁了新的工作流，并加速迈向物理 AGI。这一能力跃升体现在 Argon 在[具身推理（ERQA）基准](https://github.com/embodiedreasoning/ERQA)上的表现——该基准测试模型在 3D 环境中理解和解决物理、空间问题的能力。仅凭纯推理，Argon 便以 87% 的得分超越所有其他前沿模型。

为了展示这些能力的实际效果，我们测试了 Argon 仅靠观察学习分布外物理技能的能力。在内部测试中，Argon 观看了一段人类玩 cornhole（沙包投掷游戏）的原始视频，映射环境的空间坐标，计算所需的全身关节运动，然后自主编写了仿真代码。迁移到 [Apptronik](https://apptronik.com/) 的 Apollo 人形机器人上后，机器人在真实世界测试中连续快速投中七球。

这条「视频到仿真再到现实」（Video-to-Sim-to-Real）流水线把数周的人工仿真建模压缩到几个小时，把普通视频变成机器人技术可扩展、无限的训练场。更多关于它如何加速机器人开发的信息，请参见[我们的开发者博客](https://developers.googleblog.com/gemini-4-argon-for-robotics)。

## 以负责任且安全的方式开发 Argon

安全是 Google 模型开发的根基。由于 Argon 能力极强，我们与多家第三方合作伙伴协作，对模型的部分能力与防护措施进行了测量。Gemini 4 Argon 代表了我们迄今最全面的安全防护体系：

- **防滥用与越狱防御：**帮助防御者修补医院软件或加速生物工程的编程与科学能力，同样需要针对恶意行为者的强有力防护。依照我们的前沿安全框架，我们评估了 Argon 在多个领域的增强能力，并部署了结合越狱抵抗、监测和执行的多层防御体系。这大幅提升了我们的鲁棒性——例如，外部生物红队测试仅能解锁我们测试的生物子任务中不到 1%。此外，面对危险请求——从编写漏洞利用代码到协助获取危险生物材料——Argon 在拒绝有害请求方面显著优于我们以往的模型。在一个旨在对模型进行压力测试的对抗性集合上，违规率下降近一半，同样显著优于以往的 Gemini 模型。
- **智能体对齐与实时监测：**随着智能体作为问题解决者的能力越来越强，我们必须确保它们在遇到障碍（如权限错误或测试失败）时，不会为了急于完成任务而采取未经授权的捷径。
  - 首先，我们训练 Argon 尊重系统边界、诚实报告负面结果，并在采取不可逆步骤前暂停等待人工确认。在模型没有克制动机的编程基准上，Gemini 4 Argon 的走捷径尝试降至仅 2%，是我们以往 Gemini 模型中的最佳表现。
  - 其次，作为纵深防御的一层，我们构建了自动化失对齐监测器，读取智能体的逐步推理和行动，实时捕捉并阻断非预期的绕行操作。我们在内部部署、能力评测和强化学习训练运行中都使用了这一监测器——同时严格避免在训练中惩罚模型的想法，使其推理保持透明、可监测。
- **提示词注入抵抗：**当智能体浏览网页、阅读邮件或检查代码时，可能遇到旨在劫持其任务的隐藏恶意指令。通过对抗训练和自动化红队测试，Argon 在 Gray Swan 间接提示词注入（IPI）基准上领先，把 15 次自适应攻击尝试的攻击成功率降至 0.7%。

更多信息请参见 [Gemini 4 Argon 模型卡](https://storage.googleapis.com/deepmind-media/Model-Cards/Gemini-4-Argon-Model-Card.pdf)。

## 今天就开始使用

Argon 能更久、更努力地解决高度复杂的科学、编程和智能体问题。这得益于通过 Gemini API 提供的行业领先的 1M 统一输入输出 token 上限。请阅读面向[开发者](https://aistudio.google.com/docs/long-decode)和[企业](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/guides/gemini-4-argon#long-decodes)的文档，了解新的续写协议（continuation protocol），并根据需求完成相应配置。Argon 今天起向全球推送：

- **开发者：**可在 AI Studio 和 Android Studio 中使用 Gemini API 付费档进行构建；如果你是 Google AI Ultra 订阅用户，还可以在 Google Antigravity 和 AI Studio 中试用。
- **企业：**可在 Gemini 商业版、API 以及 Google Antigravity 中试用。
- **日常用户：**如果你是 Google AI Ultra 或 Pro 订阅用户，从今天起即可在 Gemini 应用和 Search 中的 AI Mode 里试用。
- **科学家与研究者：**申请有机会免费获得 6 个月 Google Antigravity 最高用量档位的访问（滚动接入），以资格、容量和遴选为准。申请[现已开放](https://forms.gle/WvmBbPvRbpKG1BPn9)。
- **网络安全防御者：**申请加入 [Fairwind Program](https://deepmind.google/fairwind-program/)，即可滚动获得不带网络安全护栏的 Argon 访问权限。

Gemini 4 Argon 只是开始。我们期待把 Gemini 4 家族的其他成员带给大家。
