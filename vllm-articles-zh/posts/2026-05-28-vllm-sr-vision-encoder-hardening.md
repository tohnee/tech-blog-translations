---
title: "从文本到多模态路由：加固 vLLM 语义路由器中的视觉信号"
title_en: "From Text to Multimodal Routing: Hardening Vision Signals in vLLM Semantic Router"
source: https://vllm.ai/blog/2026-05-28-vllm-sr-vision-encoder-hardening
crawled: 2026-09-12
translated: 2026-09-13
---

# 从文本到多模态路由：加固 vLLM 语义路由器中的视觉信号

> 原文：[From Text to Multimodal Routing: Hardening Vision Signals in vLLM Semantic Router](https://vllm.ai/blog/2026-05-28-vllm-sr-vision-encoder-hardening) · vLLM 博客

作者：David Shrader、Huamin Chen、Xunzhuo Liu、Bowei He 以及 vLLM Semantic Router 团队

[#生态](https://vllm.ai/blog/tags/ecosystem)[#性能](https://vllm.ai/blog/tags/performance)

大多数路由系统从一个提示（prompt）出发，然后选择一个模型端点。vLLM Semantic Router（VSR）押注的是另一条路径：在请求到达服务模型之前，系统应当提取信号、把这些信号组合成决策，并让所选路径可观测、可审计、可编程。

这一理念始于文本。Iris 引入了信号-决策（Signal-Decision）架构，让 VSR 超越固定的领域分类器，进入一个更丰富的系统：意图、关键词、嵌入、安全、PII、语义缓存和插件都可以参与路由。Athena 把同样的理念再向前推进：Semantic Router 不仅仅是 vLLM 前面的一个快速分类器，更是面向模型混合（mixture-of-models）与智能体部署的系统级智能层。

![](https://vllm.ai/blog-assets/figures/2026-05-28-vllm-sr-vision-encoder-hardening/hero.png)

下一个边界是多模态路由。一旦图像、截图、扫描件或文档页面进入请求，路由器就不再只是对一条提示进行推理，而是对请求证据进行推理。图像可能正是让请求变得临床、受监管、安全敏感、超出领域、或值得路由到更强视觉语言模型的那部分。只看文本的路由器，路由的是一个不完整的请求。

本文讲的就是跨越这条边界。关键的一步并不是简单地加一个图像编码器，而是把视觉证据转化为可信赖的 VSR 信号，使其能与文本信号在同一个决策织体（decision fabric）中组合。

下面的加固故事解释了为什么这个区别很重要。一条围绕 `multi-modal-embed-small` 的已部署多模态路径看起来是“自信地错了”。第一眼看上去的解释显而易见：也许是紧凑型视觉编码器不够强。而实际找到的问题对生产系统更有价值、也更重要：VSR 所用的 Rust/Candle 路径与同一模型的 PyTorch 参考路径并不一致。

## 多模态路由不是图像分类

纯文本路由所处理的已经远不止主题匹配。在信号-决策模型中，信号是独立的观察，决策按优先级和布尔逻辑组合这些观察，插件或模型引用定义接下来该发生什么。正是这种分离让 VSR 能够表达“安全敏感的代码审查要用更强的推理模型并开启越狱检查”这样的策略，而不是“计算机科学就发给编码模型”。

多模态路由保持同样的形态，只是把分析单元从一条文本提示变成完整请求。文本可能很笼统，而图像才携带决定性证据：

| 请求证据 | 纯文本路由器看到的 | 多模态路由器应看到的 |
| --- | --- | --- |
| “总结这个” + 护照图像 | 泛泛的摘要任务 | 证件类文件、PII 风险、受限制的处理方式 |
| “这显示的是什么？” + 胸部 X 光片 | 模糊的视觉问题 | 临床图像、医疗领域策略、能力足够的 VLM 目标 |
| “找出 bug” + 代码截图 | 编码请求 | 代码产物、可能的密钥泄露、安全审查路径 |
| 医疗提示 + 无关的汽车图像 | 医疗文本 | 超出领域的视觉证据、澄清或拒绝路径 |

创新不在于 VSR 能计算图像嵌入，而在于图像嵌入成为与文本意图、PII、越狱、领域、语义相似度、插件和模型选择同处一个织体的类型化信号。换句话说，多模态支持让 VSR 从提示级路由走向请求级策略。

![](https://vllm.ai/blog-assets/figures/2026-05-28-vllm-sr-vision-encoder-hardening/policy-layer.png)

这也是信号正确性成为控制面要求的原因。如果一个文本信号错了，策略可能路由到错误的模型或跳过错误的插件。而如果视觉信号是负相关的，问题更严重：路由器可能在自信地做出错误决策的同时，仍然为这个错误决策留下一条干净、可复现的审计轨迹。

因此，与参考实现的一致性（reference parity）不只是模型质量层面的卫生问题。对 VSR 而言，它是控制面的不变量。部署中的信号路径必须与参考模型路径含义相同，否则决策层组合的就是错误的证据。

## 当视觉信号自信地错着时

最初的症状并不是小幅的准确率下降。在一个覆盖 3 个行业领域、21 个候选标签的 11 张图像探针测试中，线上部署的 `multi-modal-embed-small`（mmes）路径在 11 张图像中的 9 张上把错误的领域排在最高位。医疗 X 光片对半导体候选的打分比对医疗候选更接近。证件类文档也没有稳定地落在证件锚点附近。

这是 82% 的反转率。信号是负相关的，而不仅仅是有噪声。

![](https://vllm.ai/blog-assets/figures/2026-05-28-vllm-sr-vision-encoder-hardening/inversion-heatmap.png)

对路由器来说，这种失败模式比基准测试分数更重要。弱分类器通常产生的是不确定性；方向反转的分类器产生的则是朝错误方向的自信。在多模态策略层中，这可能比完全没有图像信号还要糟。

暴露这一问题的是围绕 `multi-modal-embed-small` 的图像模态路由工作，包括 [vllm-project/semantic-router PR #1881](https://github.com/vllm-project/semantic-router/pull/1881) 中引入的 E2E 路由配置。一旦真实图像流经 Candle 绑定路径，差距就显现出来。

## 一个诱人的解释：升级编码器

第一个假设很自然：也许是紧凑型编码器对路由任务来说不够强。同一时期，团队正在探索 SigLIP2 系列以及更大的 `multi-modal-embed-large`（mmEL）方向。这让升级编码器看起来像是显而易见的修复方案。

我们直接验证了这一假设：

- SigLIP2-base 在同样的 21 候选探针上得分 10/10。
- 通过 Hugging Face Transformers 运行的 SigLIP-base 同样得分 10/10。
- 视觉塔基于 SigLIP2 的 mmEL 得分 10/10。
- 直接通过 PyTorch 参考路径加载的 mmes 模型卡同样得分 10/10。

![](https://vllm.ai/blog-assets/figures/2026-05-28-vllm-sr-vision-encoder-hardening/encoder-eliminated.png)

这一结果改变了调查的走向。编码器家族并不是根本问题。即便是被认为“有问题”的 mmes 模型，通过参考路径加载时行为也是正确的。

追查编码器的过程中仍有有价值的收获。更大的 SigLIP2-so400m 变体在这个探针中表现出更强的分布外拒绝能力，比更小的变体更激进地压制了一张意外混入的汽车发动机图像。当内存余量允许更大的视觉塔时，这一点可能对未来的防御性路由有用。但它并不是线上信号反转背后的 bug。

## 改变调查方向的参考路径检查

决定性的测试很简单：用两条路径在同一个护照测试样本上运行同一个 mmes 模型，比较嵌入行为。

PyTorch 参考路径针对相关护照锚点返回的余弦相似度为 **0.7204**。而部署的 Candle 绑定路径在同一图像、同一概念流程上返回 **0.1576**。在同一个模型和同一个测试样本上，这是 5-8x 的量级差距。

![](https://vllm.ai/blog-assets/figures/2026-05-28-vllm-sr-vision-encoder-hardening/diagnostic-gap.png)

到这一步，调查不再是模型选择问题。真正有用的问题变成：生产路径在哪里偏离了参考路径？

教训很直接：对多模态路由来说，参考路径对比应该是第一个诊断手段，而不是最后一个。当生产嵌入路径行为异常时，先与模型卡的参考加载器对比，再下结论说模型本身太弱。

这在 VSR 中尤其重要，因为嵌入不仅是检索原语，还可能成为策略证据。如果这份证据与参考模型方向相反，那么每个下游层都可能在逻辑上正确、而在实际运行中错误。

## 真正坏掉的是什么

偏差来自 Candle 路径中的实现细节，而不是模型权重。三项修复把问题隔离到了具体的层次。

第一，池化头是错的。`candle-binding/src/model_architectures/embedding/multimodal_embedding.rs` 中的 `SigLIPVisionEncoder::forward` 实际上在做 BERT 风格的 mean + Linear + tanh 池化，而 SigLIP 使用的是注意力探针（attentional probe）池化头。[PR #1927](https://github.com/vllm-project/semantic-router/pull/1927) 在 Candle 绑定中复刻了 SigLIP 的多头注意力池化行为。

第二，图像归一化路径不完整。Go 图像加载器产出的是 `[0, 1]` 区间的 CHW float32 像素，而 SigLIP 期望的是等价于 `(x - 0.5) / 0.5` 的逐通道归一化。[PR #1928](https://github.com/vllm-project/semantic-router/pull/1928) 在 Rust 编码器路径中应用了这一归一化。

第三，在池化和归一化修复之后，预处理仍带有残余偏差。旧的 Go 侧缩放路径使用 4-tap 双线性实现，而 PyTorch 参考路径通过 `SiglipProcessor` 使用 PIL 风格的图像预处理。[PR #1943](https://github.com/vllm-project/semantic-router/pull/1943) 把图像解码、缩放和 CHW float32 转换移入 Rust，使用 `image` crate 的 Catmull-Rom 滤波来逼近 PIL 的 bicubic + 抗锯齿行为。

![](https://vllm.ai/blog-assets/figures/2026-05-28-vllm-sr-vision-encoder-hardening/hardening-arc.png)

这类 bug 在跨语言服务栈中很容易被漏掉。Go 层、Rust FFI 层、Candle 模型实现和 PyTorch 参考实现可以各自看起来都合理，但端到端却产生破坏路由的不一致。

## 验证状态

下列数字来自 [#1927](https://github.com/vllm-project/semantic-router/pull/1927)、[#1928](https://github.com/vllm-project/semantic-router/pull/1928) 和 [#1943](https://github.com/vllm-project/semantic-router/pull/1943) 的 PR 分支栈测量结果。它们作为所提议加固路径的验证轨迹收录。在三个 PR 全部合并之前，这些数字应被理解为分支栈验证结果，而非已发布的生产行为。

在标准护照测试样本（`inrule_identifier_passport.jpg`）上进行的三向量隔离实验，将模型前向偏差与预处理偏差分离开来：

| 对比 | 余弦相似度 | 最大绝对差 | 隔离的对象 |
| --- | --- | --- | --- |
| Python vs Candle-PIL | **0.999989** | 0.000911 | 仅模型前向 |
| Candle-PIL vs Candle-Go | **0.999916** | 0.001992 | 仅预处理 |
| Python vs Candle-Go | **0.999902** | 0.002120 | 完整分支栈流水线 |

第一行说明 Rust 模型前向路径可以做到与 PyTorch 参考实现只差 fp32 级别的噪声。前两项修复后残余的偏差存在于预处理中，这正是把预处理跨 FFI 边界移动之所以重要的原因。

在覆盖证件、环境、代码、对抗与分布外样本的 20 张图像语料上，分支栈的测量结果为：

- 余弦相似度：最小 **0.999557**，平均 **0.999919**，最大 **0.999978**
- **20 / 20 张图像相对 PyTorch 参考实现的余弦相似度 >= 0.999**
- 修复前，标准测试样本上的预处理余弦相似度为 **0.990145**

![](https://vllm.ai/blog-assets/figures/2026-05-28-vllm-sr-vision-encoder-hardening/corpus-alignment.png)

重要的不只是最终的余弦数值，而是隔离方法：把生产路径与参考路径对比，把模型前向偏差与预处理偏差分离，然后让生产路径在测试与服务中使用相同的预处理语义。

## 这为 VSR 解锁了什么

一旦视觉路径变得可信，VSR 就可以把图像当作一等证据，而不是旁路元数据。这一解锁的意义大于“把图像请求路由给图像模型”：它让文本与图像证据进入同一个信号-决策织体：

| 组合信号模式 | 示例决策 |
| --- | --- |
| 临床文本 + 临床图像 + PHI/PII 信号 | 路由到受保护的医疗 VLM 路径，并启用隐私插件 |
| 笼统文本 + 证件图像 | 在模型调用之前阻断、脱敏，或路由到身份证件处理策略 |
| 代码/安全提示 + 代码截图 | 路由到安全专用模型，并对原始请求保持越狱检查 |
| 领域内文本 + 领域外图像 | 请求澄清或拒绝该图像证据，而不是强行产生一条错误路由 |

这是 Iris 与 Athena 方向的自然延续。Iris 让路由决策可组合；Athena 通过加入更强的模型栈、模型选择、记忆、回放和更丰富的信号处理，让路由器更具策略性。多模态路由把同一套架构从纯语言控制扩展到请求级控制。

与这项工作相关的公开演示是 [shrader.dev](https://shrader.dev)。它目前展示的是策略模式的文本路由版本：领域相关性检查、隐私敏感路由，以及模型调用之前的阻断结果。这个演示很重要，因为它展示了加入图像之前的策略形态。

![](https://vllm.ai/blog-assets/figures/2026-05-28-vllm-sr-vision-encoder-hardening/cyclotron-demo.png)

文本路由路径还展示了一个对多模态生产环境很重要的性能特性：分类器信号可以通过 `runSignalDispatchers` 并发运行，因此墙上时钟延迟由最慢的已启用分类器决定，而不是所有分类器之和。在一个代表性追踪中，完整的分类决策在 CPU 上约 1.3 秒完成。

![](https://vllm.ai/blog-assets/figures/2026-05-28-vllm-sr-vision-encoder-hardening/parallel-dispatch.png)

多模态版本并不是另一条独立的产品路径，而是同一个策略引擎加上更大的证据面。图像与文本信号应当通过同一套路由语义进行提取、验证、组合、回放和审计。

这就是加固工作重要的原因。如果 VSR 要基于视觉证据进行路由，视觉信号路径就必须可靠到“无聊”的程度：它必须与参考模型一致，能经受跨语言服务边界的考验，并在策略变得更富有表现力时保持可测试。

## 接下来是什么

眼下的工作是合并并评审这些加固 PR，并在多模态路由演进过程中持续让验证语料参与其中。更大的方向是让以参考实现为驱动的检查成为 VSR 多模态服务故事的常规部分。

由此往下，下一步是架构层面的：

- 把图像派生信号暴露在与文本派生信号相同的决策层中；
- 让多模态决策在回放、指标和调试工具中保持可见；
- 让模型选择同时感知策略适配性与模态能力；
- 对 PII、越狱等安全关键信号保留高保真检查；
- 把同一织体扩展到智能体工作流，让工具调用、记忆写入和模型调用都经由同一个决策层路由。

文本路由是第一个控制面，多模态路由是下一个。目标不是在路由器旁边再造一个一次性的视觉分类器，而是让请求中每个有意义的部分都能被同一个可编程的路由大脑使用。

![](https://vllm.ai/blog-assets/figures/2026-05-28-vllm-sr-vision-encoder-hardening/next-steps.png)

入门资源：

- 项目仓库：[vllm-project/semantic-router](https://github.com/vllm-project/semantic-router)
- 在线演示：[shrader.dev](https://shrader.dev)

## 致谢

感谢 Huamin Chen 提供的 mmEL 线索——它帮助打破了“升级编码器”这一误诊，感谢维护者对 [#1927](https://github.com/vllm-project/semantic-router/pull/1927)、[#1928](https://github.com/vllm-project/semantic-router/pull/1928) 和 [#1943](https://github.com/vllm-project/semantic-router/pull/1943) 的评审，以及撰写本文的邀请。也感谢更广泛的维护者团队在这一弧线所嵌入的多模态分类器工作、`multi-modal-embed-small` 模型卡，以及这一切所依赖的 Candle 绑定集成。
