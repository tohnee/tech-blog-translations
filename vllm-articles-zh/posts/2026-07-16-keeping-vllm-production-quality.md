---
title: "守护 vLLM 的生产质量：深入 CI、基准测试与发布流程"
title_en: "Keeping vLLM Production Quality: A Look Inside CI, Benchmarking, and the Release Process"
source: https://vllm.ai/blog/2026-07-16-keeping-vllm-production-quality
crawled: 2026-09-12
translated: 2026-09-13
---

# 守护 vLLM 的生产质量：深入 CI、基准测试与发布流程

> 原文：[Keeping vLLM Production Quality: A Look Inside CI, Benchmarking, and the Release Process](https://vllm.ai/blog/2026-07-16-keeping-vllm-production-quality) · vLLM 博客

作者：Kevin Luu（Inferact）

[#CI](https://vllm.ai/blog/tags/ci)[#性能](https://vllm.ai/blog/tags/performance)[#评估](https://vllm.ai/blog/tags/evaluation)[#发布](https://vllm.ai/blog/tags/release)

![vLLM 的 pull request 依次通过 CI、性能与精度评估以及发布关卡](https://vllm.ai/blog-assets/figures/2026-07-16-keeping-vllm-production-quality/00-production-quality-hero-airport.png)

vLLM 的 pull request 依次通过 CI、性能与精度评估以及发布关卡

## 引言

vLLM 是使用最广泛的开源 LLM 推理引擎：GitHub star 数超过 86K，每月 pip 安装量超过 560 万，每月镜像拉取量超过 250 万，支持 1000 多种模型架构和 600 多种加速器类型。

支持如此多的模型和加速器一直是 vLLM 最大的优势之一，也正是让稳定性难以维持的原因。

2026 年 6 月，vLLM 向 main 分支合并了 1,918 个提交——平均每天 64 个，与 PyTorch、Kubernetes 等其他大型开源项目相当。同期，我们的 CI 运行了 1300 万个任务分钟，峰值时有 1400 个并发 runner。

测试 vLLM——尤其是以这样的节奏——每天都在变得更难。一个在 H100 上毫无问题的改动，可能在 AMD 上无法编译、在 B200 上吞吐量下降，或者在某个后端上让模型输出产生刚好会有影响的偏移。让 vLLM 值得使用的整个能力面，正是我们必须在每个提交上守住的阵地。

在这篇文章中，我想分享我们如何在这样的节奏下保持 vLLM 发布的稳定：哪些做法有效、我们学到了什么、还有哪些不足。内容主要涵盖高层流程而非技术细节，那些留待另一篇文章。

在 vLLM 中，从 pull request 到新版本发布的旅程要经过三层：

- **CI** —— 我们如何在每个 PR 上抓住那些"响亮地坏掉"的问题
- **性能基准测试与精度评估** —— 我们如何抓住 CI 覆盖不到的"悄悄坏掉"的问题
- **发布流程** —— 我们如何评估信号、做出决断，然后把构建产物安全地交付给用户。

## 第一层：CI

### 对代码库每个组件进行充分的单元测试

每个 PR 都从轻量级的 GitHub Actions 检查开始——lint、格式化等类似的防护栏。当 committer 认为该 PR 可以合并时，更重的单元测试就会在我们的 CI 平台 Buildkite 上开始运行。

![vLLM 的 CI 流程：从 GitHub Actions 检查到动态选定的 Buildkite 任务](https://vllm.ai/blog-assets/figures/2026-07-16-keeping-vllm-production-quality/01-ci-pipeline-and-selected-jobs.png)

vLLM 的 CI 流程：从 GitHub Actions 检查到动态选定的 Buildkite 任务

Buildkite 动态组装每个 PR 的测试流水线：一个引导步骤读取任务定义、检查 diff，然后只调度相关的组。只改文档的话，可能只有寥寥几个任务。碰了几个重要内核？系好安全带，100 多个任务即将并行启动。

vLLM CI 套件总共运行 37 个测试组、266 个任务，覆盖每一个主要组件和特性——从各类内核到投机解码再到 LoRA。测试组从几个任务到几十个不等，许多测试会同时锻炼多个组件。以下是其中一部分：

![vLLM CI 测试组与示例任务](https://vllm.ai/blog-assets/figures/2026-07-16-keeping-vllm-production-quality/02-ci-test-groups-266-jobs.png)

vLLM CI 测试组与示例任务

### 确保测试环境一致

**只有每次都以相同方式运行的测试才有意义。** 我们通常看到两类漂移从中作梗：环境在不同 CI runner 之间可能不同，依赖也可能随时间在暗地里变化。共享的容器镜像解决前者，锁定的依赖图解决后者。

**所有机器用同一个容器镜像。** 当 266 个任务分散到几十种机器类型上时，得到不稳定、不可信结果的最快方式，就是让每个任务自己搭一个略有差异的环境。为了避免这一点，我们的大多数任务都运行在同一个容器镜像内——它在一次运行开始时构建一次，然后到处复用。我们的 Dockerfile 分阶段构建，每一层都在下一层之上叠加。

![vLLM CI 与发布共用的容器构建阶段](https://vllm.ai/blog-assets/figures/2026-07-16-keeping-vllm-production-quality/03-container-build-stages.png)

vLLM CI 与发布共用的容器构建阶段

`base` 阶段提供 CUDA 工具链；`build` 阶段在其上编译 wheel 包；`runtime` 阶段安装这些 wheel 及其运行时依赖。

从这里开始构建分叉：一个镜像加入服务入口，成为发布镜像；另一个独立的 `test` 镜像加入测试依赖，成为 CI 任务拉取的镜像。这种共同的血缘让我们测试的东西贴近我们发布的东西。

对使用共享镜像的任务来说，B200 上的内核测试与 L4 上的入口点测试拉取的是同一个容器镜像，逐字节一致，只是运行在不同硬件上。构建一次就消除了一个主要的差异来源：失败来自各任务环境搭建漂移的可能性大大降低。

**每次运行用相同版本。** 依赖会随时间漂移——这是我们吃过苦头才学到的另一半。

未锁定的依赖会让失败难以追查：同一个测试周一通过、周三崩溃。你把期间的每一条代码改动都读了一遍，没有一条看起来相关。几个小时后才恍然大悟——FlashInfer 周三发了新版本，构建悄悄把它拉了进来。而且 FlashInfer 从来不是孤例：nixl、transformers 以及它们的传递依赖都用同样的方式咬过我们——每一次不打招呼的升级都是打破 CI 的新机会，而原因埋在依赖层次之下。

因此 vLLM CI 锁定依赖。我们对顶层依赖运行 `pip-compile`，生成锁定每一个包（包括传递依赖）的 lock 文件。

![顶层依赖被编译成完全锁定的包依赖图](https://vllm.ai/blog-assets/figures/2026-07-16-keeping-vllm-production-quality/04-pip-compiled-dependency-graph.png)

顶层依赖被编译成完全锁定的包依赖图

我们定期更新锁文件，并且每次都运行完整的 CI 套件。自从开始锁定完整的依赖图以来，依赖导致的破坏不再是反复发作的头痛。

### 在异构、多供应商的机群上扩展 CI 算力

每个任务都会被推送到 Buildkite 上的一个 runner 队列——即具有特定硬件配置的一池机器。例如，`gpu_1` 队列由带 L4 GPU 的单台 VM 支撑；`b200` 队列由内含 B200 的 Kubernetes 集群支撑。当某个 runner 空闲时，它认领队列中的下一个任务，运行它，并把结果报告给 Buildkite。

截至本文撰写时，vLLM CI 拥有 58 个 runner 队列，覆盖种类繁多的加速器，这些硬件由多个合作组织提供。

![vLLM CI 跨加速器厂商与硬件类型的 runner 队列](https://vllm.ai/blog-assets/figures/2026-07-16-keeping-vllm-production-quality/05-accelerator-runner-fleet.png)

vLLM CI 跨加速器厂商与硬件类型的 runner 队列

我们在算力上的花费是有限的。即使负担得起，自己管理所有这些机器也是一件相当艰难的工作。能有如此多样化的 CI 覆盖，完全得益于众多优秀伙伴的慷慨支持与协作。

不过，集成是个大挑战。每个伙伴的需求都不同：有的直接把所有东西的访问权交给我们，有的倾向于自己管理硬件，有的有非常严格的安全护栏。

**那么，我们是如何把它们全部接入同一条 CI 流水线的？**

这就是 **Buildkite agent** 的用武之地。它运行在供应商的环境内部，通过 HTTPS 向外连接 Buildkite 来领取工作。由于 Buildkite 不需要主动连接 agent，供应商不必开放入站端口、配置 VPN，也不必让我们访问其网络。

agent 接受任务后，运行命令、回传日志流，并报告最终退出状态。持久型 agent 随后继续等待更多工作，而临时型 agent 在完成任务后退出。

运行该 agent 不止一种方式，供应商可以按自己的环境任选。

最简单的是独立机器——比如我们的 8xA100 机器或 Arm 服务器。供应商安装 agent，把它指向一个 runner 队列，它就会永远运行这个循环。

![独立 Buildkite agent 轮询 runner 队列并报告结果](https://vllm.ai/blog-assets/figures/2026-07-16-keeping-vllm-production-quality/06-standalone-buildkite-agent-flow.png)

独立 Buildkite agent 轮询 runner 队列并报告结果

对 Kubernetes 集群中的机器，同样的模型可以通过 [Buildkite Agent Stack for Kubernetes](https://github.com/buildkite/agent-stack-k8s) 实现。控制器把每个匹配的任务变成一个带单个 Pod 的 Kubernetes Job，由它运行测试并回报。我们总是推荐这种方式，因为它扩展性很好：不需要在每个节点上安装 Buildkite agent，只需把它们加入集群。

![Buildkite Agent Stack for Kubernetes 为每个 CI 任务创建一个 pod](https://vllm.ai/blog-assets/figures/2026-07-16-keeping-vllm-production-quality/07-kubernetes-buildkite-agent-flow.png)

Buildkite Agent Stack for Kubernetes 为每个 CI 任务创建一个 pod

无论哪种方式，接入在我们这边都很简单：我们创建一个队列、提供一个 token，供应商自己启动 agent。我们不需要访问机器。正是这一点让 vLLM 能在我们永远买不起的更多硬件上测试——**一套每年价值数百万美元的捐赠机群。**

### 硬件利用率也是挑战

需求很多而算力有硬上限，所以我们必须确保一点不浪费。

**用 MIG 把大 GPU 切片**

![8 张 H200 GPU 被划分为 56 个 Multi-Instance GPU 切片](https://vllm.ai/blog-assets/figures/2026-07-16-keeping-vllm-production-quality/08-h200-mig-slices.png)

8 张 H200 GPU 被划分为 56 个 Multi-Instance GPU 切片

大多数 CI 任务用较小的模型运行，需要的资源远少于一整张 GPU。NVIDIA 的 Multi-Instance GPU（MIG）让我们把一张卡切成多个隔离的切片——一张 H200 变成 7 个 18 GB 的分区——意味着同一时间 7 个任务可以共享一张 GPU。我们算了一笔账，发现在很多情况下，把大 GPU 切片比为了同样工作量去租用小 GPU 便宜得多！

**从零自动扩缩，每台机器一个任务**

对按小时租用的机器来说，开着机闲置就是白白烧钱。所以这些队列各自自动扩缩：有任务等待时启动更多机器，没有任务可跑时缩到零。每台机器领取一个任务，在容器中运行，然后关机。附带的好处是测试也更干净：每个任务拿到的是一台全新的机器，过去运行留下的任何东西都不会捣乱。

**能复用的就不要重建**

CI 中最慢、最重复、最昂贵的部分是：

1. 构建整条 CI 流水线使用的标准 Docker 镜像

   1. 编译 CUDA 内核
   2. 安装全部依赖
2. 从 Hugging Face 下载模型权重。

所以我们尽量避免：

- **Docker 层**：我们使用 registry 缓存，复用已缓存的层而不是重建。依赖也包括在内。
- **构建机预热缓存 AMI**：我们有一个每晚运行的任务，构建构建机所用的 AMI，其中已拉取最新层，让构建机的起点尽可能接近 main。
- **编译器缓存**：我们使用 **sccache**，把编译好的 C++/CUDA 输出缓存到 S3 桶中，跨构建复用。每台构建机都可以读取这个桶，但只有用于 main 分支的构建机可以写入。
- **模型权重**：我们测试的模型非常庞大，所以对每个集群，我们把它们一次性下载到共享存储，每个任务都从那里读取，而不是每次都拉取几个 GB。

### 让 CI 健康状况可见

每天数百次 CI 运行、每次跨不同硬件运行数百个任务，我们还需要知道系统本身是否健康。

某个队列悄悄积压到数小时等待。某个测试开始每 20 次运行失败一次。某个任务比上个月慢了 10 分钟。这些都不容易追踪。

我们从 PyTorch 的好朋友们打造的出色的 PyTorch CI HUD（[hud.pytorch.org](https://hud.pytorch.org/)）中获得灵感，在 [ci.vllm.ai](https://ci.vllm.ai) 建了自己的一个。

每 15 分钟，我们 Buildkite 流水线的数据就会汇入 Databricks 和 ClickHouse。

有了全部可用数据和对仪表盘的完全控制，我们在构建可观测性栈上有了极大的灵活性。回答下面这些典型问题变得容易多了：

CI 健康信号

01 / 共 04

问题

#### main 分支现在健康吗？

![显示 main 分支健康状况的 CI 仪表盘](https://vllm.ai/blog-assets/figures/2026-07-16-keeping-vllm-production-quality/08-main-branch-health.png)

仪表盘告诉我们什么

过去 3 天：不健康。而且任务为什么要跑 10 个小时！？

这些只是我们仪表盘能力的几个例子。现代编码智能体让这类工具的开发出人意料地容易上手，即使没有深厚的前端专长也是如此。

### 自动化故障检测与响应

仪表盘帮我们看到问题。下一步是缩短从发现到诊断的时间，这里当然要用上强大的 AI 智能体。

每天晚上，一个 CI 分析机器人会运行完整套件，并与前一晚的运行结果对比。如果有新失败的项，它会读取错误日志、对失败分类，并逐个排查中间的提交来找出元凶。然后它会把报告发到 Slack，并附上一个准备好的自动回滚 PR 供维护者审阅合并。这大约相当于每天 1.5 个自动回滚 PR，其中约 70% 的情况能正确识别出失败与元凶提交——因此值班评审通常是从一个正确的诊断出发，而不是面对空白页。

这个机器人已经成为快速发现破坏的关键，与之并行的还有社区在问题出现时即刻修复的努力——向每一位提供帮助的人致敬，尤其是 Red Hat 的值班轮换团队！

![CI 分析机器人报告回归并建议回滚](https://vllm.ai/blog-assets/figures/2026-07-16-keeping-vllm-production-quality/12-ci-analyzer-bot.png)

CI 分析机器人报告回归并建议回滚

### 绿色对勾无法告诉我们的事

把以上一切合在一起，就是让我们敢于信任 PR 上的绿色对勾的原因：广泛的单元测试覆盖，在由大量不同加速器组成的机群上运行，环境一致，并且监控完善。当 CI 通过时，我们确信合并风险已显著降低。

但 CI 不能说明全部。一个改动可以通过所有测试，却仍然让模型变慢或输出错误。为了让 CI 保持快速且成本可控，我们会跳过许多 e2e 测试，更重要的是，不会去精细模拟 vLLM 用户每天经历的一切。这正是下一层的用途。

## 第二层：性能基准测试与精度评估

5 月，我们发布了 `v0.20.0`，几天之内就不得不打出两个紧急补丁 `v0.20.1` 和 `v0.20.2`。两个问题溜了过去：一个在 `gpt-oss` 于 Blackwell 上跨多 GPU 切分（张量并行 > 1）时使其崩溃，另一个让 `DeepSeek V4` 在 GB200 上的吞吐量大幅下滑。

当时我们还没有基准测试流水线；没有任何东西在发布前于该硬件上端到端运行这些模型，确认它们仍能正常工作且跑得快。于是两个问题都顺利越过 CI，到达了用户手中。

性能回归很少导致崩溃。服务器能启动、请求能成功；用户只是每秒拿到的 token 变少，或者等待首 token 的时间变长。精度回归则悄无声息：模型返回了有效响应，但答案是错的。

我们意识到端到端运行模型、配合性能基准与精度检查是多么重要，因此投入了大量时间构建这一层。

它现在为我们的发布流程提供了大量信号，并且已经抓住过数次重大回归。我们建成的这套系统，本可以在 v0.20.0 发布之前就抓住那些问题。

### 每晚运行模型与加速器的组合矩阵

我们的流水线维护在 <https://github.com/vllm-project/perf-eval>。每个配置文件描述一个工作负载：如何启动 vLLM 服务器、使用哪些参数、服务哪个模型、用哪种加速器、运行哪些任务。

每个工作负载通常运行三类任务：

- 性能基准——测量 TTFT（首 token 延迟）、TPOT（每输出 token 时间）等许多指标——使用 `vllm-bench`
- 数学与推理基准（GSM8K、GPQA、AIME）上的模型精度，使用 `lm-eval`
- 通过 Berkeley 函数调用排行榜（BFCL）测量的函数调用精度

![每晚运行的 vLLM 工作负载：执行性能、精度与函数调用评估](https://vllm.ai/blog-assets/figures/2026-07-16-keeping-vllm-production-quality/14-nightly-perf-eval-workload.png)

每晚运行的 vLLM 工作负载：执行性能、精度与函数调用评估

每晚以及针对每个发布候选版本，我们都会在 H200、B200、MI300X 和 MI355X 上，对选定的模型——DeepSeek V4 Pro/Flash、gpt-oss、Kimi K2.5、MiniMax M2.5 与 M3、Qwen3.5、GLM 5.1、Gemma 4、Nemotron 3 Super——运行完整套件。目前总共有 17 组"模型-硬件"配方，而且清单还在不断增加。我们计划很快加入 GB200/GB300、PD 分离部署以及更多模型的支持。

### 它始终够快吗？

每次运行结束后，结果都会汇入我们的数据库。还记得前文的 CI 仪表盘吗？它也有性能结果！

我们把每晚的数字变成图表，让回归随着时间推移容易察觉。

例如，这是我们[性能仪表盘](https://ci.vllm.ai/perf)的一个视图：

![gpt-oss 120B 在 H200 上的性能历史](https://vllm.ai/blog-assets/figures/2026-07-16-keeping-vllm-production-quality/14-performance-trends.svg)

gpt-oss 120B 在 H200 上的性能历史

*gpt-oss 120B 在 H200 上（张量并行度 8）的性能历史，按并发度拆分。*

[对比视图](https://ci.vllm.ai/compare)让我们把两个 vLLM 镜像面对面比较——例如发布候选版对上一个正式版。

![在性能仪表盘中对比两个 vLLM 镜像](https://vllm.ai/blog-assets/figures/2026-07-16-keeping-vllm-production-quality/15-compare-view.png)

在性能仪表盘中对比两个 vLLM 镜像

### 它始终正确吗？

如果你的 vLLM 实例快得飞起，但输出一塌糊涂，那速度毫无价值。除了性能之外，我们还要确保模型的答案依然站得住。

[评估仪表盘](https://ci.vllm.ai/eval)存储汇总分数与误差条，并允许我们打开一次运行，检查底层问题、参考答案、原始响应、抽取出的答案以及正确性判定。这种样本级证据远比从一个汇总数字调试有用得多。

![检查一个错误的评估样本](https://vllm.ai/blog-assets/figures/2026-07-16-keeping-vllm-production-quality/16-accuracy-sample-debugging.svg)

检查一个错误的评估样本

*一个出错的 GSM8K 样本展示了确切的问题、期望答案、模型响应与抽取结果。*

## 第三层：发布流程

### 快节奏发布

自 2025 年 11 月以来，我们一直保持 vLLM 两周一发的节奏。与我们规模相当的项目中，很多发布要慢得多。我们坚持这一节奏的原因：

- **改动快速到达用户手中。** 新版本永远不会落后 main 太多。
- **可预测。** 用户和下游项目可以围绕稳定的日程做规划，而不必猜测下一次发布何时落地。
- **特性管理和回归追踪更容易。** 需要二分定位的是 500 个提交而不是几千个。
- **截止期压力更小。** 贡献者不必赶在"火车发车"前匆忙塞进自己的改动，两周后搭下一班就好。
- **Cherry-pick 保持干净。** 几天前的修复通常是一次简单的摘取，而不是合并冲突的烂摊子。

每隔一周的周一，我们启动发布周。流程如下：

![vLLM 发布候选版本的测试与发布循环](https://vllm.ai/blog-assets/figures/2026-07-16-keeping-vllm-production-quality/18-release-candidate-loop.png)

vLLM 发布候选版本的测试与发布循环

### 从最安全的提交开始

周一，发布管理员查看 `main` 分支最近几次完整 CI 运行，选出"最绿"的提交。这样发布分支在加入任何发布专属改动之前，就拿到了最健康的可用起点。

我们就在那个提交上切出 `releases/vX.Y.Z` 分支，并宣布该分支与发布窗口。

### 对每个发布候选版本进行重量级测试

从切分支到周三，我们审阅 cherry-pick 请求，把它们分批摘入发布分支，并打上标签作为下一个发布候选版本。

每个候选版本都要通过同样的三道关卡：

- 完整 CI 套件
- 性能基准套件
- 模型精度评估套件

每个结果都与一个发布候选版本绑定。当后续候选版本改变了 CI 健康度、性能或评估质量时，我们可以追查是哪个候选版本引入了差异：它们之间只隔着几十个提交。

cherry-pick 窗口在周三关闭。此后只能 cherry-pick 修复发布候选版本上既有问题的改动，随后打上新的候选版本标签、再过一遍三道关卡，直到某个候选版本达标。

### 标准面前不打折扣

只有三道关卡全部通过，候选版本才算合格。

有时一周结束时没有任何合格的候选版本，这也没关系。我们尽力按时发布，但绝不会为了赶时间而在标准上妥协。我们对待新版本的态度就像 Rockstar 对待 GTA 6：好了才算好。不过我们不会花十年……

### 为每个平台交付

一旦候选版本合格，我们就以该提交为起点，开始为不同硬件平台和 CUDA 版本构建全部产物，确保每个人都能原生使用 vLLM。而且在任何东西发布之前，我们会对构建产物本身做冒烟测试。

截至本文撰写时，我们每次发布都交付：

- **7 个 Python wheel 包**：

  - CUDA 12.9 x86\_64/arm64
  - CUDA 13.0 x86\_64/arm64
  - CPU x86\_64/arm64
  - ROCm
- **11 个 Docker 镜像**：

  - CUDA 12.9，x86\_64/arm64，Ubuntu 22.04/24.04
  - CUDA 13.0，x86\_64/arm64，Ubuntu 22.04/24.04
  - ROCm
  - CPU x86\_64/arm64

## 下一步计划

我夸了很多我们建成的东西——但说实话，路线图上仍有很多事要做。其中几个大项：

- **自动测试选择。** 目前我们依据一份手工维护的映射来决定每个 PR 运行哪些测试，而它过时得很快。我们希望这一过程自动化，正在尝试几个方向：基于 LLM 的选择、静态分析、动态分析，以及给源码路径打标签以匹配测试。
- **更快的信号时间。** CI 平均要 1–2 小时才能给出结论；我们希望压到 30 分钟以内。
- **更轻量的单元测试。** 我们的许多"单元"测试实际上会启动一个完整的 vLLM 服务器并向它发送真实请求，这大大拖慢了 CI。
- **更好的退出码处理。** 一些任务失败时仍会返回错误的退出码，例如把基础设施问题报告成测试失败，导致失败分类和告警/重试都很困难。
- **更快的 flaky 测试检测与隔离。** 我们有不少不稳定的测试——来自基础设施、上游包，或者纯粹写得不够安全的测试——我们希望自动发现并隔离它们。
- **基础设施问题自动检测。** 快速发现一台坏机器，并在它连累一堆任务失败之前自动将其移出 CI 机群。
- **更好的告警。** 我们对 runner 队列拥塞和回归已有一些基础告警。但越多越好：CI runner 磁盘压力过高、任务突然以远超平常的速度失败、依赖安装损坏等等。
- **代码覆盖率报告。** 我们的覆盖很广，但还不能确信代码库的每个角落都真正被执行到。

做 CI 其实比大多数人想象的有趣得多。这篇文章只讲了保持 vLLM 发布稳定的高层流程；还有许多有趣的技术细节我没能覆盖——也许留到另一篇文章 :)

如果这些问题听起来正是你感兴趣的那种乐趣，或者你认为我们哪里做得不对，欢迎来 vLLM Slack 的 `#sig-ci` 频道打个招呼。如果你想全职做这些事，Inferact 正在[招聘](https://jobs.ashbyhq.com/Inferact/3dee433c-7121-458c-8408-c193b6326ffb)~！

## 致谢

这一切都不是一个人的努力。vLLM CI 由整个社区共同构建和维系。

我深深感谢一路以来帮助过 CI 的每一个人（按字母顺序列出）：

- **Amazon**：Junpu Fan、Liangfu Chen、Omri Shiv
- **AMD**：Alexei Ivanov、Andreas Karatzas、Kenny Roche、Micah Williamson
- **Arm**：Fadi Arafeh、Ioana Ghiban
- **EmbeddedLLM**：Tun Jian Tan
- **Google**：Brittany Rockwell、Jincheng Chen、Ming Huang、Qiliang Cui、Yarong Mu、Yiwei Wang
- **HuggingFace**：Harry Mellor
- **Inferact**：Harry Chen、Jiangyun Zhu、Kaichao You、Nick Hill、Roger Wang、Simon Mo、Zhewen Li
- **Intel**：Chendi Xue、Jiang Li、Kunshang Ji、Wenjun Liu
- **Meta**：Andrey Talman、Charlotte Qi、Eli Uriegas、Huamin Li、Huy Do、Orion Reblitz-Richardson、Reza Barazesh
- **NVIDIA**：Alec Flowers、Benjamin Chislett、Mathew Wicks、Pen Chung Li、Stefano Castagnetta、Vadim Gimpelson、Xin Li
- **Red Hat**：Andy Linfoot、Avinash Singh、Doug Smith、Edward Quarm、Flora Feng、Lucas Wilkinson、Luka Govedic、Matt Bonanni、Michael Goin、Nicolo Lucchesi、Robert Shaw、Russell Bryant、Tarun Kumar、Tyler Michael Smith、Wentao Ye
- **Reflection AI**：Amr Mahdi（贡献完成于其在 Meta 任职期间）
- **独立贡献者**：Cyrus Leung（DarkLight1337）、Yuqi Wang（noooop）、haosdent、Mohammad Angkad

以及了不起的合作伙伴：

- **AWS、Crusoe、LambdaLabs、Nebius、NVIDIA、Roblox、RunPod** 以算力额度赞助我们
- **Buildkite** 让我们在其平台上免费运行 CI <3

最后，感谢两位导师，我在 Anyscale（Ray）期间从他们身上学到了很多 CI 知识：**Lonnie Liu**（现就职于 OpenAI）和 **Cuong Nguyen**（现就职于 NVIDIA）。
