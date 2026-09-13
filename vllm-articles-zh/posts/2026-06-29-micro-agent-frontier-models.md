---
title: "Micro-Agent：在 Model API 内部以协作击败前沿模型"
title_en: "Micro-Agent: Beat Frontier Models with Collaboration inside Model API"
source: https://vllm.ai/blog/2026-06-29-micro-agent-frontier-models
crawled: 2026-09-12
translated: 2026-09-13
---

# Micro-Agent：在 Model API 内部以协作击败前沿模型

> 原文：[Micro-Agent: Beat Frontier Models with Collaboration inside Model API](https://vllm.ai/blog/2026-06-29-micro-agent-frontier-models) · vLLM 博客

作者：vLLM Semantic Router 团队

[#生态](https://vllm.ai/blog/tags/ecosystem)[#智能体路由](https://vllm.ai/blog/tags/agentic-routing)

所有人都在等待下一个前沿模型。

更有意思的层次，也许是它前面的那一层。

路由器正在成为 AI 推理的控制平面。它最初的角色很务实：把正确的请求路由到正确的模型。这本身已经很重要，因为生产环境的 AI 不再是单一模型的世界。

路由器可以决定一个请求何时值得用前沿模型、何时用开源或本地模型就足够，从而削减成本。它可以把敏感领域送往更严格的模型、更严格的过滤器或更强的审查路径，让安全策略变得可执行。它还可以协调云与边缘，把隐私或低延迟意图留在本地，把更难的工作升级到云端。

这些都是重要的工作。

但路由器的下一份工作更有意思：

> 路由器可以让模型变得更好。

不是靠改权重，也不是靠让每个应用都自建一套定制的智能体图，而是把一次模型 API 调用变成服务层内部一次有边界的协作。

![图 1：路由器正在从模型选择走向能力构建。](https://vllm.ai/blog-assets/figures/2026-06-29-micro-agent-frontier-models/router-capability-layer.png)

图 1：路由器正在从模型选择走向能力构建。

这就是 [Sakana Fugu](https://sakana.ai/fugu/) 引起如此大反响的原因：它把一个简单而有力的想法做成了商业产品——“模型”可以只是一个界面，界面背后可以是一个团队。围绕这一想法的研究，包括 [Fugu 技术报告](https://arxiv.org/abs/2606.21228)以及 [Conductor](https://arxiv.org/abs/2512.04388)、[Trinity](https://arxiv.org/abs/2512.04695) 等协作论文，为思考编排问题提供了有用的语言。

但 vLLM Semantic Router 的愿景不同之处在于抽象放在哪里。协作不应只存在于某一个商业端点或某一个应用专属的智能体图里，它应该成为一种开放的服务原语。

vLLM Semantic Router 把这个想法带进开放的服务层。用户仍然只调用一个模型：

```
{
  "model": "vllm-sr/auto",
  "messages": [{"role": "user", "content": "..."}]
}
```

在这个稳定的模型标识背后，路由器可以选择配方（recipe）、扇出到多个 worker、收集法定数量（quorum）、验证分歧、合成最终答案、修复输出契约，并返回一个正常的 OpenAI 兼容响应。

重点不是把复杂性暴露出来。

重点而是让协作用起来像一个模型。

## Looper 就是运行时

在 vLLM Semantic Router 中，looper 是有边界微智能体（micro-agent）的执行运行时。

请求以普通的 chat completion 形式进入路由器。路由器提取信号，把它们投影到任务形态或风险区间，匹配一个决策，然后选择一个算法。该算法可能是一条普通的单模型路由，也可能是一条 looper 路由。

目前主要的 looper 模式有：

- **Confidence（置信度）**：一个顺序升级循环。先尝试更便宜的候选，测量置信度，只有分数过低时才升级。
- **Ratings（评分）**：一个有界扇出循环。在硬性并发上限下运行多个候选，并用评分感知的权重进行聚合。
- **ReMoM**：重复的模型混合（mixture-of-model）推理。它扇出广度样本，等待足够多的成功响应，再运行最终合成轮。
- **Fusion（融合）**：小组评审-裁判-定稿模式。独立的模型响应成为裁判与定稿者的证据。
- **Workflows（工作流）**：微智能体工作流运行时。支持静态角色或动态规划器，执行有边界的 worker 步骤，并合成最终响应。

![图 2：Looper 算法在路由器内部运行，同时保持模型 API 表面不变。](https://vllm.ai/blog-assets/figures/2026-06-29-micro-agent-frontier-models/looper-micro-agents.png)

图 2：Looper 算法在路由器内部运行，同时保持模型 API 表面不变。

实现细节很重要。looper 不是“多问几个模型”的口号，而是一个带预算、拓扑、追踪和失败策略的小型运行时。

### Confidence：把升级只花在难题上

Confidence 是成本感知的循环。它从更小或更便宜的候选开始，然后评估答案是否足够自信、可以停下来了。置信度信号可以来自 token 级对数概率、logprob 差值（margin）、混合分数、自我验证，或 AutoMix 式的蕴含校验器（entailment verifier）。

分数过阈值，路由器立即返回；分数过低，路由就升级到下一个候选。关键不在于存在升级，而在于升级成为显式的路由策略：阈值、失败行为和停止条件都是可见、可调的。

![图 3：Confidence 把升级变成一种可度量的停止策略。](https://vllm.ai/blog-assets/figures/2026-06-29-micro-agent-frontier-models/confidence-loop.png)

图 3：Confidence 把升级变成一种可度量的停止策略。

### Ratings：硬性上限下的并行质量

Ratings 是受控的集成（ensemble）循环。它并行启动若干候选，但不超过配置的 `max_concurrent` 上限。这让它在“希望从多个模型视角受益，又不想让每个请求都变成无界扇出”时非常有用。

路由器收集成功响应，应用评分感知的聚合，并按路由策略处理失败。实践中，Ratings 适合 A/B 式评估、集成策略，以及运营者已有有意义的候选级质量信号的路由。

![图 4：Ratings 让多候选执行保持有界且评分感知。](https://vllm.ai/blog-assets/figures/2026-06-29-micro-agent-frontier-models/ratings-loop.png)

图 4：Ratings 让多候选执行保持有界且评分感知。

### ReMoM：有契约的广度

当任务推理方差大、且答案格式必须在协作中保持不变时，ReMoM 很有用。它扇出多个推理尝试，等待最少成功数（minimum-success quorum），然后让合成模型把证据合并成所需的输出契约。

如果合成失败但此前的 worker 已产出有效证据，路由不必坍缩成一个 API 错误：它可以回退到最好的有效证据，仍然返回正常响应。

![图 5：ReMoM 把广度、法定数、合成与回退当作服务时控制项。](https://vllm.ai/blog-assets/figures/2026-06-29-micro-agent-frontier-models/remom-loop.png)

图 5：ReMoM 把广度、法定数、合成与回退当作服务时控制项。

### Fusion：把分歧当作信号

Fusion 押的是另一个注：有时有用的不是平均答案，而是分歧的结构。独立的小组答案成为证据；裁判看到一致、矛盾与独特洞察；然后定稿者返回一个答案，追踪轨迹折叠在 API 之内。

这让 Fusion 在存在多条看似合理的竞争路径时特别有用：困难的多选推理、长篇专家判断，或单一自信回答可能很脆弱的精确答案任务。

![图 6：Fusion 不隐藏分歧，而是把分歧变成证据。](https://vllm.ai/blog-assets/figures/2026-06-29-micro-agent-frontier-models/fusion-loop.png)

图 6：Fusion 不隐藏分歧，而是把分歧变成证据。

### Workflows：预算之下的角色

Workflows 是最具智能体色彩的模式，也是最需要最严格边界的模式。规划器只能从允许的 worker 模型中选择；计划会被校验；步骤受最大步数、最大并行度、超时和错误策略约束；最终响应仍须满足输出契约。

对 SWE 式任务而言，这意味着路由器可以表达规划器、补丁器（patcher）、验证器和定稿器，而不必让应用自持一套定制的智能体栈。对生产服务来说，这个区别至关重要：循环很强大，但它仍由基础设施治理。

![图 7：Workflows 给路由器的是一个有边界的角色系统，而不是一个无界的自主智能体。](https://vllm.ai/blog-assets/figures/2026-06-29-micro-agent-frontier-models/workflows-loop.png)

图 7：Workflows 给路由器的是一个有边界的角色系统，而不是一个无界的自主智能体。

### Auto 配方：一个模型名，多种循环

对外表面仍是一个模型名：`vllm-sr/auto`。在内部，路由器可以用信号与投影为请求选择正确的循环。难度、风险、契约压力、延迟和成本不是 prompt 里的注释，而是可以选择 Confidence、Ratings、ReMoM、Fusion、Workflows 或回退路径的路由事实。

![图 8：Auto 配方让信号来选择协作模式，同时保持单一模型标识。](https://vllm.ai/blog-assets/figures/2026-06-29-micro-agent-frontier-models/auto-recipe-loop.png)

图 8：Auto 配方让信号来选择协作模式，同时保持单一模型标识。

这就是“智能体作为应用逻辑”与“微智能体作为服务运行时”的区别。路由器掌控预算、策略、拓扑、追踪和失败模式。

## 配方胜过单一万能循环

我们评测工作给出的最重要教训，不是某个算法总能赢。

恰恰相反：

> 最好的循环是与任务形状匹配的。

GPQA-Diamond 需要严格保留多选答案格式；LiveCodeBench 需要可运行代码和对隐藏测试的稳健性；Humanity's Last Exam 需要分歧消解和精确答案格式；SWE 式任务需要规划器、补丁器、验证器和定稿器。

因此 `vllm-sr/auto` 不应意味着“永远跑最大的循环”，而应意味着：选择适合这个任务的配方。

![图 9：信号与投影让路由器选择与基准测试形态匹配的协作模式。](https://vllm.ai/blog-assets/figures/2026-06-29-micro-agent-frontier-models/benchmark-shaped-recipes.png)

图 9：信号与投影让路由器选择与基准测试形态匹配的协作模式。

在我们的配方里，这一形状是显式的：

- GPQA-Diamond 把高难理科多选 prompt 路由到带严格 `ANSWER: X` 保留的 ReMoM 配方。
- LiveCodeBench 先寻找约束、起始代码、标准输入、浮点容差、超时风险和隐藏测试风险，再选择代码形态的循环。
- HLE 先检测形式化推理、分歧风险、长上下文和精确答案压力，再在更深的 ReMoM、更小的 Fusion 或回退路径之间做出选择。

这就是为什么路由器侧的协作不只是 prompt 工程。prompt 只是其中一部分，配方还定义模型池、模型角色、推理力度（reasoning effort）、并发度、法定数、超时、合成模型、回退策略、输出契约和可观测性标签。

## 记分卡是证明，不是全部

我们在三个困难基准上评估了当前的闭源模型配方。这些数字有用，因为它们表明这个想法不只是好看。

![图 10：VSR Closed 与 VSR Hybrid 在 LiveCodeBench、GPQA-Diamond 和 Humanity's Last Exam 上的记分卡视图。](https://vllm.ai/blog-assets/figures/2026-06-29-micro-agent-frontier-models/three-eval-scorecard.png)

图 10：VSR Closed 与 VSR Hybrid 在 LiveCodeBench、GPQA-Diamond 和 Humanity's Last Exam 上的记分卡视图。

> 在这张记分卡中，**VSR Closed** 表示配方只使用闭源模型后端；**VSR Hybrid** 表示配方混合使用开源与闭源模型，在配方需要更高风险的评判、修复、合成或回退时使用更强的闭源模型。

| 基准 | VSR 记分卡行 | 分数 | 参照行 |
| --- | --- | --- | --- |
| LiveCodeBench（2025 年 1 月–4 月） | VSR Closed | 92.6 | Fugu Ultra 92.0、Fugu 90.3、GPT-5.5 90.7、Opus 4.8 90.3 |
| GPQA-Diamond | VSR Closed | 96.0 | Fugu Ultra 95.5、Fugu 95.5、Gemini 3.1 Pro 94.3、GPT-5.5 93.6 |
| Humanity's Last Exam | VSR Closed | 50.0 | Fugu Ultra 50.0、Fugu 48.5、Gemini 3.1 Pro 45.0 |
| Humanity's Last Exam | VSR Hybrid | 47.1 | GLM-5.2 40.5、Qwen3.7 Max 41.4、GPT-5.5 41.4 |

这张记分卡需要仔细解读。它并不是主张每个请求都应始终使用所有闭源模型——那样的产品是错误的。

它的主张是：由路由器拥有的协作可以创造出比其底层单个调用更强的模型标识，在保持单一 API 表面的同时，胜过或追平前沿单模型基线。

这才是真正的产品形态：

- 用户看到一个模型名。
- 运营者控制配方。
- 系统可以在不改动客户端集成的情况下变强。
- 开源与闭源模型可以在同一个服务抽象下参与。

## 这对模型服务意味着什么

旧的服务栈是被动的：它接受一个模型名，把请求发给某个后端。

下一代服务栈是主动的，它会问：

- 我们对这个请求掌握哪些证据？
- 它落在什么质量、成本、延迟和安全区间？
- 一个模型够不够？
- 如果不够，应该运行什么协作模式？
- 必须保持哪种答案契约？
- 如果某个供应商慢了或错了，该怎么办？
- 如何在保留完整追踪的同时只暴露一个干净的响应？

这不是应用胶水代码，这是基础设施。

微智能体属于路由器，因为路由器已经拥有微智能体需要的东西：模型别名、供应商策略、凭据、成本元数据、信号、决策、重试、超时、追踪，以及 OpenAI 兼容的响应语义。

## 要点

“前沿模型”这个词开始有两层含义。

一个含义是检查点（checkpoint）。

另一个含义是系统边界。

最近的编排浪潮让这个方向清晰可见。vLLM Semantic Router 押注的是：这种能力应该在服务层可编程、可观测、开放。

下一场模型竞赛仍会是更好的模型之间的竞赛，但也将是更好的路由器之间的竞赛：知道何时省钱、何时执行安全、何时留在边缘、何时上云，以及何时把一个请求变成一支小型而守纪律的团队的路由器。

这就是 Model API 内部微智能体的承诺。

## 致谢

我们感谢来自 [MBZUAI](https://mbzuai.ac.ae/)、[McGill University](https://www.mcgill.ca/)、[Mila](https://mila.quebec/) 和 [Agentic Intelligence Lab](https://agentic-in.ai/) 的研究者，特别是 [Xue Liu 教授](https://www.linkedin.com/in/xueliu)与 [Bowei He 博士](https://www.linkedin.com/in/bowei-he-8a9450199/)，感谢他们在路由器侧模型协作方面的研究合作与讨论。

个人贡献者：[Huamin Chen](https://www.linkedin.com/in/huaminchen/)、[Yincheng Ren](https://www.linkedin.com/in/yincheng-ren/)。

我们还感谢 AMD 的 [Andy Luo](https://www.linkedin.com/in/andyluo77/) 和 [Haichen Zhang](https://www.linkedin.com/in/haichen-zhang-9010b6382/) 为 AMD GPU 评估提供的支持。
