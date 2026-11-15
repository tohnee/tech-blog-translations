---
title: "用 Jev 做实时决策：自演化，以及在 NVIDIA Blackwell 上 24 ms 的引擎"
title_en: "Real-Time Decisions with Jev: Self-Evolution and a 24 ms Engine on NVIDIA Blackwell"
date: 2026-10-05
source: https://haoailab.com/blogs/mcjev/
crawled: 2026-11-16
translated: 2026-11-16
---

# 用 Jev 做实时决策：自演化，以及在 NVIDIA Blackwell 上 24 ms 的引擎

> 原文：[Real-Time Decisions with Jev: Self-Evolution and a 24 ms Engine on NVIDIA Blackwell](https://haoailab.com/blogs/mcjev/) · Hao AI Lab @ UCSD

# 用 Jev 做实时决策：自演化，以及在 NVIDIA Blackwell 上 24 ms 的引擎

2026 年 10 月 5 日 · 18 分钟 · Minshen (Alex) Zhang、Junda Chen、Yuanbo Yang、Yuxuan Zhang、Yi Sun、Shaoxiong Duan、Lanxiang Hu、Jiaqi Leng、Yulun Wu、Will Lin、Hao Zhang

[![](https://img.shields.io/github/stars/alexzms/MCJev?style=social)](https://github.com/alexzms/MCJev)[![](https://img.shields.io/badge/🎮%20demo--green.svg?style=social)](https://mc.alexzms.com)[![X post](https://img.shields.io/badge/X-post-000000?style=social&logo=x)](https://x.com/haoailab/status/2104302648786919643?s=20)

**TL;DR**

* **我们做了什么。** MCJev：一个用 [Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev) 风格模型（[DJev](https://github.com/mmastrac/djev)）在单次前向计算中做出每一步决策的智能体，并在 Minecraft PvP 中与真人对抗测试。
* **在复杂任务上自演化，无需训练。** 借助一个 SOTA LLM 智能体和人工监督，我们从机器人自己的日志出发快速演化提示词。在不到两小时内，机器人从在满技能脚本对手面前输掉每一场基准对局，变成赢下每一场。
* **NVIDIA Blackwell 上每次决策 24 ms。** 我们的引擎 DJev-serve 比领先的推理引擎快 2.5 倍。
* **与真人、大规模测试。** 32 小时内 54 人在公开对局中打了 1,795 场，Jev 在 Block UHC 中胜率 70%。这是通往实时 AI 与物理 AI 的第一步。

我们与 NVIDIA 的 Pen Chung Li 在 MCJev 上紧密合作。MCJev 运行在 NVIDIA 提供的 **NVIDIA GB200 NVL72** 与 **B200** GPU 上。我们对其支持深表感谢。

## 问题：实时决策[#](#the-problem-real-time-decisions)

许多真实决策必须在世界持续变化的同时做出：在支付清算前将其标记出来、在别人看到之前拦下一条聊天消息、为一次客服来电做路由、决定一个游戏角色或一个机器人下一步做什么。它们本质上是同一件事：读懂局势，从一组固定的选项中挑一个，并在几十毫秒内完成，一天往往要做数百万次。一个先推理再回答的大模型对此太慢、每次决策也太贵；为任务训练的专用分类器很快，但任何变化都意味着新数据和新一轮训练。我们想要第三种选择：一个轻量、低延迟的决策模型，开箱即用，配上一套可以在数小时内迭代的 harness（图 1）。

![实时决策任务与 Minecraft PvP 测试](img/applications_v2.svg)

图 1. 许多实时决策任务共享同一个形状：局势进来，必须在几十毫秒内输出少数几个选项之一，而且规则经常变化。MCJev 在 Minecraft PvP 中检验这个形状：deadline 是 50 ms 的服务器 tick，规则是我们用一个 LLM 智能体演化的提示词，对手是一个会适应的真人。

[Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev) 风格的模型正好契合这个任务。它不做书写式的决策：它在一次前向计算中给每个选项打分，并返回它们的完整分布，因此每个答案都自带置信度：确定的选择直接执行，不确定的交给人类或更大的模型。一个先写思维链的智能体无法满足几十毫秒的预算：在每秒 200 token 的速度下，200 个推理 token 要花整整一秒。我们使用的 Jev 风格模型 DJev 也很轻：DiffusionGemma-26B-A4B 每个 token 只激活约 4B / 26B 参数，而在 DJev-serve 上一次决策约 24 ms，比人的反应速度大约快十倍（图 2）。

![这有多快](img/how_fast.png)

图 2. 真实对局中一次 Jev 决策（中位数）对比一个服务器 tick、人对视觉线索的反应，以及一个先推理再回答的 LLM（估算：每秒 200 token 下 200 个推理 token，未计入提示词处理）。

我们需要一个这样的测试：决策不能等，对手会适应，每次决策都被评分，而且我们仍然能便宜地大规模运行。Minecraft PvP 对抗真人就是这样的测试。服务器每秒 tick 20 次，人的反应约四分之一秒，所以一个需要一秒才能决策的智能体是靶子，不是对手。对局没有成本，一台服务器可同时跑几十场，每次决策连同结果都被记录，而对手是会学习智能体习惯的真人。主要模式 Block UHC 也不是单一选择，而是一个复杂任务：剑、弓、岩浆和方块，每一步都有十几种动作可选。游戏本身以及怎么玩，见[游玩](#play)。

## 它如何演化[#](#how-it-evolves)

Jev 的决策来自一个 harness：描述局势的提示词，以及提供给它的选项。Jev 的大部分提升来自 harness 而非模型，所以要演化的是 harness。训练会把每一次改动变成数天或数周的数据采集、训练和评测。我们改用另一种方式：在人工监督下用一个 SOTA LLM 智能体快速演化提示词——智能体阅读真实对局的日志并起草改动，我们决定保留什么（图 3）。

![反思循环](img/reflection_loop_master.svg)

图 3. 智能体反思。harness 写出提示词，Jev 去玩，每场对局都被观察，我们用 LLM 智能体根据所见演化提示词；机器人就地重新加载。负责打游戏的模型从不改变。

1. **提示词。** 每个 tick，机器人读取游戏状态，并用代码算出事实（距离、攻击范围、伤害、掩体）。harness 把它们写进约 1,760 token 的提示词，并且只提供此刻有意义的动作，每个动作都说明它会做什么。
2. **游玩与观察。** Jev 打真实对局。每场对局留下双方的录像，以及每次决策的日志：Jev 读到的提示词、DJev 在选项上的完整分布，以及随后发生了什么。
3. **演化提示词。** 我们和一个 SOTA LLM 智能体（Claude Opus 5.5 或 GPT-6 Astra）一起过日志。它找出 Jev 出错的地方（误判的一场战斗、没被提供的动作、问错时机的问题、本该成为反射动作的判断），起草新的提示词，并在需要时为机器人写新的反射动作；我们审阅每处改动并选择接下来打哪一版。
4. **重新加载。** 机器人就地加载新的 harness，无需重启、无需重训，然后循环再跑一遍。

![harness 版本随时间变化](img/harness_timeline_v2.png)

图 4. Block UHC harness 的演进（git 提交时间）。第一个小时内有八个版本；v10 是面向公众对战的版本，大约在 v1 之后九小时；下一版正在迭代中。

**它变好了吗？** Block UHC 足够复杂，以至于第一版 harness 是输的。我们用同一个脚本对手（一个满技能的战士机器人）做基准测试，每版三场：v1 输掉全部三场，v6 赢下两场，而 v9 在 v1 之后不到两小时赢下全部三场。面对真人，v10 随后在 870 场 Block UHC 中赢下 70%（[它表现如何](#how-it-performs)）。这个基准很小，而且并非一切都提升了：面对脚本弓箭手，v9 在 14 场中仍只赢 2 场。

**它花了多少成本。** v1 到 v8 用了 54 分钟，v10 出现在 v1 之后约九小时，智能体从第一行代码到公开发布大约一天（图 4）。每处改动都是一次文本编辑加一次重载：没有数据采集、没有标注、没有反向传播，全程使用同一个现成模型。这个循环里没有任何东西是游戏专用的：任何任务，只要一个 Jev 风格模型读取状态、从选项中挑选，并留下记录其选择结果的日志，都能以同样的方式迭代。我们正在迭代下一版，而它会很快：自服务器开放以来，循环里已经有了每一位与 Jev 对战过的玩家的对局和决策可以学习。

## 它如何工作[#](#how-it-works)

每个机器人都是一个决策头（deciding head）架在一个更快的执行器（actioner）之上（图 5）。**执行器**是一个 [mineflayer](https://github.com/PrismarineJS/mineflayer) 客户端，每个 50 ms 的 tick 读取游戏，并运行那些不能等待的反射动作：瞄准、躲箭、绝不走进岩浆。**决策头**是由 **DJev-serve** 提供服务的 [DJev](https://github.com/mmastrac/djev)，它把战斗读作文本并选择战术。这个切分是通用的：用快速代码处理不能等的事情，用模型做判断性决策，这与机器人学中“慢速策略驾驭快速底层控制器”是同一形状。

![MCJev 一览](img/mcjev_overview_v3.png)

图 5. MCJev 一览。执行器每个 tick 通过 mineflayer API 读取游戏，harness 把战斗写成文本，并留出一个被 mask 的答案槽；DJev 在一次前向计算中填上该槽，生成零个 token；该槽上的 logits 成为所提供动作上的分布，Jev 按下得分最高的一个（紫色循环，约 24 ms）。金色循环是反思：我们阅读 Jev 行为的日志，编辑 harness 并重载，从 v1 到 v10 约九小时、无需训练（它如何演化）。底部：真实对局中的一次决策（中位数），对比一个领先的推理引擎与 DJev-serve。

## 它跑得多快[#](#how-fast-it-runs)

实时决策有预算，路径上的每一部分都要计入：模型被如何提问、运行它的引擎，以及它周围的网络。

### 不解码就决策[#](#decide-without-decoding)

聊天模型通过书写来回答，一次一个 token；对于在十六个选项中做选择来说，这是浪费的工作。DJev 用另一种方式向扩散语言模型索取答案。DiffusionGemma 把一个因果**编码器**（把提示词读进 KV cache）与一个双向**解码器**配对，后者对一个“画布”去噪（我们服务 64 个 token 的画布）。一次 Jev 式读取会把答案骨架写进画布（`1: ▒`，每个问题一个槽），跑一次解码器前向，然后在每个槽上只保留该问题的候选 token（`A`、`B`……）并重新归一化（图 6）。这就是选项上的完整概率分布，且从未采样出任何 token。这就是 [DJev](https://github.com/mmastrac/djev) 的工作方式：[mmastrac](https://github.com/mmastrac) 为 DiffusionGemma 构建的 Jev 风格决策服务器，建立在他为 vLLM 添加的结构化读取之上（[#57250](https://github.com/vllm-project/vllm/pull/57250)、[#58216](https://github.com/vllm-project/vllm/pull/58216)）。

这样使用的 DiffusionGemma 非常擅长读局势并做选择（在我们的探针中，设备选择、从一张小图判断迷宫安全性和邮件分类都得了 0.95–1.0 分），但它不会替你做算术；harness 负责算数，把结论交给模型。

![DJev 如何读出一个决策](img/djev_readout.svg)

图 6. 一次决策。状态与问题进入提示词；画布承载留白的答案骨架；一次解码器前向把它填满；该槽上被限制在选项 token 内的 logits，就是 Jev 据以行动的分布。

### 推理引擎[#](#the-inference-engine)

**我们在 NVIDIA Blackwell 上的贡献：**

* **DJev-serve**：把一次 Jev 式读取作为从 CUDA graph 重放的单次前向，比领先的推理引擎快 2.5 倍：真实对局中每次决策约 24 ms，对比约 60 ms。
* **面向 DiffusionGemma 的 Blackwell kernel 选择**：滑动窗口层用 FlashAttention-2，全局层用调优的 Triton kernel，128 专家 MoE 用经 FlashInfer 的 CUTLASS grouped GEMM。
* **在 GB200 NVL72 与 B200 上的公共服务池**：八张 GB200 GPU 上约每秒 360 次决策，全天候运行。
* **全部开源**，NVFP4 是下一步。

服务同一个模型的三个阶段：

|  | 一次决策 | 变化 |
| --- | --- | --- |
| Hugging Face transformers | 174 ms | 第一个可用版本 |
| 带结构化读取的领先推理引擎（DJev） | ~60 ms | 去掉了生成循环，但仍是通用调度 |
| **DJev-serve** | **~24 ms** | 每次决策一次前向，捕获进 CUDA graph |

（174 ms：一张 NVIDIA GB200 上的第一个原型，一个短测试请求；它从未服务过真实对局。~60 与 ~24 ms：真实对局中的中位数（图 12）。在一个受控基准上，同一段录制请求、同一批权重、一张 NVIDIA B200，DJev-serve 同样是 2.5 倍更快。）

**时间花在哪了。** 第一个版本每次前向启动 **10,340 个 kernel**，大多是围绕 30 层的细小胶水操作，GPU 只有三分之一的时间真正忙碌；8 个请求合批后耗时几乎不比单个长。领先推理引擎上的 DJev 去掉了其中大部分，但仍把 prefill 和 denoise 当作两个调度步骤、按完整画布宽度运行。

**DJev-serve。** 我们通过 autoresearch 构建它：一个 AI 编程智能体跑了大部分的 profile、改动与基准循环，而我们选择下一步试什么并核对每一个数字。它保留 vLLM 的模型代码、分页 KV cache 与 attention kernel，去掉调度器，并且恰好用一次前向来完成同样的读取：

* **从 token id 到答案 log-prob 的单一 CUDA graph**，每个提示词长度桶一个；每次决策我们只填两个小索引缓冲区然后重放。
* **graph 内的前缀缓存**：每个请求复用它与近期提示词共享的最长块对齐前缀的 KV，前缀长度只是索引缓冲区里的数据。
* **25 个滑动窗口层用 FlashAttention-2**（在 Blackwell 上每层比 Triton attention kernel 快约 4 倍）；5 个全局层（head size 512）仍用调优的 Triton kernel。
* **MoE 用 NVIDIA kernel**，它占每次前向的最大份额（图 7）：经 FlashInfer 的 CUTLASS grouped GEMM，比 Triton MoE kernel 快 7%。

结果是真实对局中**每次决策约 24 ms**，从请求到答案，其中大部分是 GPU 前向本身，所以现在的瓶颈是 GPU。原始基准数字、版本与完整布局见 [serving/docs/PERFORMANCE.md](https://github.com/alexzms/MCJev/blob/main/serving/docs/PERFORMANCE.md)。

**NVFP4。** NVIDIA 发布了同一模型的 NVFP4 检查点 [nvidia/diffusiongemma-26B-A4B-it-NVFP4](https://huggingface.co/nvidia/diffusiongemma-26B-A4B-it-NVFP4)，采用 Blackwell 原生 4-bit 格式。在我们于 GB200 上的测试中，按我们的 batch size 它尚未比 BF16 更快（短读取上约慢 9%），但既然 GEMM 占每次前向的一半以上，把它引入 DJev-serve 的 graph 是我们的下一步；同时还有我们尚未做基准的 FlashAttention-4。

![GPU 时间分解](img/gpu_breakdown_v2.png)

图 7. 一次前向的 GPU 时间去向（前缀缓存之后的一个真实 MCJev step，kernel 时间取自 eager profile）：MoE 专家（128 个，每个 token 激活 8 个）占主导，其次是其它投影与 attention。

**一次决策的成本。** 大约**每次前向固定 6 ms**，加上**每 1,000 个不在前缀缓存中的 token 约 10.4 ms**，这使提示词设计变成一个系统问题：一个机器人约 1,760 token 的提示词里只有约 480 命中缓存，因为每一步都变化的那一行排在固定段落之前，而每个机器人的名字出现在第一句。harness 作者与服务工程师必须一起设计提示词。

**批处理**最多四个请求进一次前向，可带来 1.5 倍吞吐而不拖慢单个机器人，并把一张 GPU 从每秒 43 步提到 58–64 步。

![扩展与批处理](img/scaling_batching_v2.png)

图 8. 左：一次前向花费约 6 ms 外加每 1,000 个未缓存 token 约 10.4 ms。右：把请求批处理进一次前向。

### 服务许多个 Jev[#](#serving-many-jevs)

公共服务器需要同时服务许多 Jev；我们跑一个 24 个实例的池。每张 GPU 运行自己的一份 DJev-serve，前面是一个小的 **gateway**，它把每个请求发给健康且最少在途请求的引擎，如果某引擎在请求中途挂掉就换一个重试。在八张 NVIDIA GB200 GPU 上用真实决策对线上 gateway 做重放，8 条流达到每秒 324 次决策且延迟不升，而 24 条流满打满算在每秒 362 次饱和（图 9）。一个战斗中的 Jev 平均每秒约 6 次决策，所以 24 个只需约 140。

![Gateway 负载测试](img/gateway_load.png)

图 9. 用真实决策对 gateway 做闭环压测（8 张 GPU）：吞吐（柱）与延迟（线）。

网络也是预算的一部分。我们最早的智能体通过一条从笔记本连出的隧道访问模型：每次决策**约 330 ms**，大部分花在穿越互联网上。把智能体、然后连 Minecraft 服务器本身移到 GPU 集群上后，一次决策降到模型自身的延迟（图 10）。一个机器人同样面临选择：模型放在遥远的数据中心，还是放在执行器旁边；当循环很紧时，我们的数字是“把头留在身体旁边”的一个小数据点。

![网络路径](img/network_path_v2.png)

图 10. 从机器人视角看一次决策的端到端成本，随着各部分彼此靠近（真实对局中位数）。

## 它表现如何[#](#how-it-performs)

9 月 26 日我们以 v10 harness 向公众开放服务器。在最初约 32 小时（9 月 26 日 19:05 UTC 至 9 月 28 日 03:29 UTC），**54 人**在一对一模式中与 Jev 打了 **1,795 场**（按 Minecraft 账号计，含我们团队自己的账号）：

* 在 **Block UHC**（用剑、弓、岩浆和方块的完整战斗）中，**Jev 赢下 870 场的 70%**（图 11）。
* 在 **Sumo**（唯一动作是推）中，**人类赢下 925 场的 88%**。Jev 是远比相扑手优秀的决斗者，Sumo 场次是我们最清晰的待办清单。
* 整个发布期间，一次决策从请求到答案**约 24 ms**（图 12），快到 Jev 能在一场战斗的 4.4 秒里做出 131 次决策（图 13）。
* 每次决策都留下日志：仅我们主集群上就**超过 130,000 条**（含我们自己的测试对局），每条都包含 Jev 读到的状态、DJev 在选项上的完整分布，以及该动作的结果。这就是下一版要学习的数据。

![谁赢了](img/release_results.png)

图 11. 最初 32 小时内与 Jev 的一对一大厅对局，按模式划分。

![发布期间的延迟](img/latency_timeline_v2.png)

图 12. 发布期间 Jev 在真实对局中做出的每一次决策（文本 harness 的 94k 次决策，5 分钟中位数与 p90），从机器人视角的请求到答案：领先推理引擎上约 60 ms，切换到 DJev-serve 后约 24 ms。这些是不同小时、不同负载下的生产中位数，不是受控对比；在受控的同请求基准上，加速同样是 2.5 倍。

![一场真实对局](img/decisions_round_v2.png)

图 13. 一场真实对局的四秒钟：Jev2 在 4.4 秒内做出 131 次决策。每根柱是一次决策；高度是 DJev 给它所选动作的概率，颜色是动作。连续 0.99 的柱是坚定的承诺（这里是进入掩体）；更低、更多变的柱是接近的判断。

## 超越游戏[#](#beyond-the-game)

MCJev 是一个游戏，但它检验的约束不是：在世界持续运动、对手会适应的情况下，在几十毫秒内做决策。实时响应类任务都面临它——从在支付清算前标记支付，到在别人看到前拦下一条消息；物理 AI 也一样：一条从传送带上取件的机械臂不可能在决策时让传送带暂停。游戏既不是业务也不是机器人，我们还不知道这些结果能延伸多远，但其中一些经验也许可以：在一次前向中决策，把较慢的决策头架在快速执行器上，从 kernel 到网络全链路预算延迟，记录每次决策及其结果，并在人工监督下用 LLM 智能体在数小时内演化提示词。

接下来，我们想：

* **在日志上训练。** Jev 今天零训练游玩，而日志就是训练数据：先在赢的一方上做监督微调，然后用该场结果作为奖励做强化学习。每次决策都已保存 DJev 在选项上的完整分布，这让 RL 变得简单。
* **对不止一个对手演化。** 在多样化的对战套件上评判每个 harness 版本，并让使用不同 harness 与检查点的 Jev 全天候互相对战，用人类对局锚定评分。
* **跑得更快。** NVFP4 权重、更新的 attention kernel、以及在单卡上跨 Jev 批处理，把一次决策压到 20 ms 以下。
* **尝试物理任务。** 测试这些经验哪些在机器人上成立，例如在 [RoboDojo](https://robodojo-benchmark.com/) 这类操作基准上（其仿真任务运行在 NVIDIA Isaac Sim 上），以及决策头能缩小到什么程度以运行在机器人自身、比如 NVIDIA Jetson Thor 这样的计算机上。

## 游玩[#](#play)

Minecraft: Java Edition 1.9 或更新版本，付费游戏（服务器会校验账号，所以你需要一个拥有该游戏的 Microsoft 账号）：**多人游戏 → 添加服务器 → `mc.alexzms.com`**。在大厅里右键点击指南针选择模式，或者沿红毯跑到铁质踏板上。如果你赢了，你会出现在大厅的排行榜上。

* **Block UHC**：双方各得一把剑、一张弓、岩浆桶和水桶以及方块。60 秒时伤害翻倍，再过 30 秒两人都被丢到一个被岩浆环绕的小平台上。36 个竞技场并排运行。
* **Sumo**：单一平台、没有武器。把对方推下去。
* **2v2**：你和朋友对抗两个 Jev，它们共享所见。

最初 32 小时的一些记录：在 Block UHC 中最快击杀 Jev 用了 1.2 秒，人类获胜对局的中位时长为 21.5 秒。全部 1,757 场比赛都被录制，共 10.2 小时：双方每个 tick 与每次挥击、命中、箭矢、放置方块和死亡，压缩后 12.3 MB。

[![
](img/trailer_poster.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/mcjev--img--trailer.mp4)

图 14. 41 秒的真实对局：一个岩浆陷阱、半颗心时横穿岩浆、4 点生命时的翻盘。

[![](img/loop_counter_poster.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/mcjev--img--loop_counter.mp4)
[![](img/loop_neon_poster.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/mcjev--img--loop_neon.mp4)

图 15. 两场真实的 Block UHC，玩家视角（循环片段）。左：Jev 从掩体后作战，交换攻击并获胜。右：玩家围绕一根柱子倒岩浆；Jev 剑尖朝前穿过它，19.4 秒内获胜。

## 致谢[#](#acknowledgement)

我们特别感谢 **NVIDIA**，以及为这项工作提供硬件支持的每一个 NVIDIA 团队：MCJev 构建并运行在 NVIDIA **GB200 NVL72** 与 **B200** GPU 上；一个全天候与公众对战的 Jev 池，每个每几十毫秒就要一次决策，只有这样的硬件才有可能。感谢 NVIDIA 的 Pen Chung Li 在 MCJev 上的合作。感谢 TypeSafe AI——这项工作的想法与名字来自他们的 [Jev 与 System One 模型](https://typesafe.ai/blog/introducing-system-one-models-and-jev)；感谢 Google 以开放权重发布 DiffusionGemma；感谢 DJev-serve 所基于的 vLLM 项目；感谢 [mmastrac](https://github.com/mmastrac) 提供 [DJev](https://github.com/mmastrac/djev) 及其所依赖的 vLLM 结构化读取（[#57250](https://github.com/vllm-project/vllm/pull/57250)、[#58216](https://github.com/vllm-project/vllm/pull/58216)）；以及每一位登录并与 Jev 对战的人。

## 贡献者[#](#contributors)

[Minshen (Alex) Zhang](https://alexzms.github.io/)、[Junda Chen](https://github.com/GindaChen)、[Yuanbo Yang](https://freemty.github.io/)、[Yuxuan Zhang](https://yuxuandexter.github.io/)、[Yi Sun](https://www.linkedin.com/in/yi-sun-mlsys)、[Shaoxiong Duan](https://github.com/shaoxiongduan)、[Lanxiang Hu](https://snyhlxde1.github.io/)、[Jiaqi Leng](https://jacky-leng.github.io/)、[Yulun Wu](https://memset0.github.io)、[Will Lin](https://github.com/SolitaryThinker)、[Hao Zhang](https://haozhang.ai)

**引用我们：**

```
@misc{mcjev2026,
  title        = {Real-Time Decisions with {Jev}: Self-Evolution and a 24 ms Engine on {NVIDIA} {Blackwell}},
  author       = {Zhang, Minshen and Chen, Junda and Yang, Yuanbo and Zhang, Yuxuan and Sun, Yi and Duan, Shaoxiong and Hu, Lanxiang and Leng, Jiaqi and Wu, Yulun and Lin, Will and Zhang, Hao},
  year         = {2026},
  month        = oct,
  howpublished = {Hao AI Lab blog},
  url          = {https://haoailab.com/blogs/mcjev/}
}
```
