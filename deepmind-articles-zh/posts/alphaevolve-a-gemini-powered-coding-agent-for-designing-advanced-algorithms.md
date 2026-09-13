---
title: "AlphaEvolve：一个由 Gemini 驱动、用于设计先进算法的编码智能体"
title_en: "AlphaEvolve: A Gemini-powered coding agent for designing advanced algorithms"
source: https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/
site: deepmind
date: 2025-05-14
crawled: 2026-09-13
translated: 2026-09-13
---

# AlphaEvolve：一个由 Gemini 驱动、用于设计先进算法的编码智能体

> 原文：[AlphaEvolve: A Gemini-powered coding agent for designing advanced algorithms](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/) · Google DeepMind

新 AI 智能体将大语言模型的创造力与自动评估器相结合，为数学和计算的实际应用演化算法

大语言模型（LLM）用途极为广泛。它们可以总结文档、生成代码，甚至头脑风暴出新点子。如今，我们把这些能力扩展到了数学和现代计算中基础且极其复杂的问题上。

今天，我们宣布推出 [AlphaEvolve](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/AlphaEvolve.pdf?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=)——一个由大语言模型驱动的演化式编码智能体，用于通用算法发现与优化。AlphaEvolve 将我们的 [Gemini 模型](https://deepmind.google/technologies/gemini/?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=)的创造性问题求解能力与验证答案的自动评估器相结合，并利用演化框架在最有前景的想法上不断改进。

AlphaEvolve 提升了 Google 数据中心、芯片设计和 AI 训练流程的效率——其中包括训练 AlphaEvolve 自身底层的大语言模型。它还帮助设计出更快的矩阵乘法算法，并为开放数学问题找到了新的解法，展现出在众多领域应用的巨大前景。

## 用大语言模型设计更好的算法

2023 年，我们首次展示大语言模型能够生成以计算机代码编写的函数，在一个开放科学问题上帮助[发现新的、可证明正确的知识](https://deepmind.google/discover/blog/funsearch-making-new-discoveries-in-mathematical-sciences-using-large-language-models/?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=)。AlphaEvolve 是一个能够超越单一函数发现的智能体：它可以演化整个代码库，开发复杂得多的算法。

AlphaEvolve 利用了最先进大语言模型的组合：我们最快、最高效的模型 [Gemini Flash](https://deepmind.google/technologies/gemini/flash/?_gl=1*7wovog*_up*MQ..*_ga*ODcyNjk2MzY0LjE3NDYxODE1OTY.*_ga_LS8HVHCNQ0*MTc0NjE4MTU5NS4xLjAuMTc0NjE4MTU5OS4wLjAuMA..&utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=) 最大化所探索想法的广度，而我们最强大的模型 [Gemini Pro](https://deepmind.google/technologies/gemini/pro/?_gl=1*5ncg4r*_up*MQ..*_ga*ODcyNjk2MzY0LjE3NDYxODE1OTY.*_ga_LS8HVHCNQ0*MTc0NjE4MTU5NS4xLjAuMTc0NjE4MTU5OS4wLjAuMA..&utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=) 则凭借富有洞见的建议提供关键的深度。两个模型共同提出以代码实现算法解决方案的计算机程序。

![示意图展示提示词采样器（prompt sampler）如何首先为语言模型组装一个提示词，语言模型随后生成新的程序。](https://lh3.googleusercontent.com/mUd0dQneyWkX6ohzKGk0dE4-vJaSgvgYGPFjWC2krhVWILtIiMFkSxz8OWA3ug17ZzUd61rKPuHFWafiuVJ2j9IVFzHSlklrd5ykNk3t_AZno9gXBfU=w1440)

示意图展示提示词采样器如何首先为语言模型组装一个提示词，语言模型随后生成新的程序。这些程序由评估器进行评估并存入程序数据库。该数据库实现了一个演化算法，决定哪些程序将被用于未来的提示词。

AlphaEvolve 使用自动化评估指标对提出的程序进行验证、运行和打分。这些指标为每个解的准确性和质量提供了客观、可量化的评估。这使得 AlphaEvolve 在那些进展可以被清晰、系统地度量的广泛领域中格外有用，比如数学和计算机科学。

### 优化我们的计算生态系统

过去一年，我们把 AlphaEvolve 发现的算法部署到了 Google 的计算生态系统中，包括我们的数据中心、硬件和软件。这些改进的影响在我们的 AI 与计算基础设施中被成倍放大，为所有用户构建一个更强大、更可持续的数字生态系统。

![示意图展示 AlphaEvolve 如何帮助 Google 交付一个更高效的数字生态系统，涵盖从数据中心调度、硬件设计到 AI 模型训练。](https://lh3.googleusercontent.com/1JID6zu5b-zdhv7d9QFqMQa-i6iODWRIc7oBEuRshiQV3T6lZK9NIL0CjpAbvz7NfMBBazNeG0iFCTJA2ZLFY9rZGiciQC__ebpo3DJQhUAUmaODGg=w1440)

示意图展示 AlphaEvolve 如何帮助 Google 交付一个更高效的数字生态系统，涵盖从数据中心调度、硬件设计到 AI 模型训练。

### 改进数据中心调度

AlphaEvolve 发现了一个简单却极为有效的启发式方法，帮助 [Borg](https://research.google/pubs/large-scale-cluster-management-at-google-with-borg/?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=) 更高效地编排 Google 庞大的数据中心。这一方案已在生产环境中运行一年有余，平均可持续回收 Google 全球算力资源的 0.7%。这一持续的效率提升意味着，在任何时刻，同样的算力占用可以完成更多任务。AlphaEvolve 的解决方案不仅带来出色性能，还具备人类可读代码的重大运维优势：可解释、可调试、可预测且易于部署。

### 协助硬件设计

AlphaEvolve 提出了一个 [Verilog](https://en.wikipedia.org/wiki/Verilog) 重写方案，移除了一个用于矩阵乘法、经过高度优化的关键算术电路中不必要的位。至关重要的是，该提案必须通过稳健的验证方法，确认修改后的电路保持功能正确。这一提案已被集成进即将推出的[张量处理单元](https://cloud.google.com/tpu?hl=en&utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=)（TPU）——Google 的定制 AI 加速器。通过以芯片设计师的标准语言提出修改建议，AlphaEvolve 促进了 AI 与硬件工程师之间的协作方式，加速未来专用芯片的设计。

### 增强 AI 训练与推理

AlphaEvolve 正在加速 AI 性能和研究速度。通过找到更聪明的方式把大型矩阵乘法运算拆分为更易处理的子问题，它将 Gemini 架构中的这一关键[内核](https://docs.jax.dev/en/latest/pallas/index.html)加速了 23%，使 Gemini 的训练时间缩短了 1%。由于开发生成式 AI 模型需要大量计算资源，每一分效率提升都意味着可观的节约。除了性能收益之外，AlphaEvolve 还大幅减少了内核优化所需的工程时间——从专家数周的工作量缩短到数天的自动化实验——让研究人员能够更快地创新。

AlphaEvolve 还能优化低层 GPU 指令。这个极其复杂的领域通常已被编译器深度优化，人类工程师一般不会直接修改它。AlphaEvolve 在基于 [Transformer](https://en.wikipedia.org/wiki/Transformer_%28deep_learning_architecture%29) 的 AI 模型中，为 [FlashAttention](https://arxiv.org/abs/2205.14135) 内核实现取得了高达 32.5% 的加速。这类优化帮助专家精确定位性能瓶颈，并轻松把改进纳入他们的代码库，提升生产力，并在未来节省算力与能源。

### 推进数学与算法发现的前沿

AlphaEvolve 还能为复杂数学问题提出新方法。在只提供一个计算机程序的最小代码骨架的条件下，AlphaEvolve 设计出了一种新颖的[基于梯度的优化](https://www.sciencedirect.com/topics/engineering/gradient-based-algorithm)流程的多个组件，为矩阵乘法——计算机科学中的一个基本问题——发现了多个新算法。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![你的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

AlphaEvolve 为发现更快的矩阵乘法算法所提出的一组修改列表。在这个例子中，AlphaEvolve 对多个组件提出了大量修改，包括优化器与权重初始化、损失函数以及超参数扫描。这些修改绝非平凡，在演化过程中需要 15 次变异。

AlphaEvolve 的流程找到了一个使用 48 次标量乘法来计算 4x4 复数值矩阵乘法的算法，改进了[ Strassen 1969 年的算法](https://en.wikipedia.org/wiki/Strassen_algorithm)——此前已知是该设定下的最优解。这一发现显著超越了我们之前的专门研究矩阵乘法算法的工作 [AlphaTensor](https://deepmind.google/discover/blog/discovering-novel-algorithms-with-alphatensor/?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=)——对于 4x4 矩阵，AlphaTensor 仅在二进制运算下找到了改进。

为了考察 AlphaEvolve 的广度，我们将该系统应用于数学分析、几何、组合和数论中的 50 多个开放问题。系统的灵活性让我们能在数小时内完成大多数实验的搭建。据我们所知，在约 75% 的案例中，它重新发现了最先进的解法。

而在 20% 的案例中，AlphaEvolve 改进了此前已知的最佳解法，在相应的开放问题上取得了进展。例如，它推进了[吻数问题（kissing number problem）](https://en.wikipedia.org/wiki/Kissing_number)。这个几何挑战[已经吸引数学家超过 300 年](https://plus.maths.org/content/newton-and-kissing-problem)，关注的是与一个公共单位球相接触的互不重叠球体的最大数量。AlphaEvolve 发现了一个由 593 个外部球构成的构型，在 11 维中建立了新的下界。

### 前进之路

AlphaEvolve 展示了从为特定领域发现算法到为广泛的现实挑战开发更复杂算法的演进。我们预期 AlphaEvolve 将随大语言模型能力的提升继续改进，尤其是在它们[编程能力更强](https://developers.googleblog.com/en/gemini-2-5-pro-io-improved-coding-performance/?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=)的情况下。

与 [People + AI Research 团队](https://pair.withgoogle.com/?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=)一起，我们一直在构建一个友好的用户界面来与 AlphaEvolve 交互。我们正在为选定的学术用户规划一个 Early Access Program（抢先体验计划），同时也在探索让 AlphaEvolve 更广泛开放的可能性。如需登记兴趣，请填写[这份表单](https://forms.gle/WyqAoh1ixdfq6tgN8?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=)。

虽然 AlphaEvolve 目前被应用于数学和计算领域，但它的通用性质意味着它可以应用于任何解法可以被描述为算法且能被自动验证的问题。我们相信，AlphaEvolve 有望在更多领域带来变革，如材料科学、药物发现、可持续发展以及更广泛的技术与商业应用。

[阅读我们白皮书中的更多细节](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/AlphaEvolve.pdf?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=)[登记使用 AlphaEvolve 的兴趣](https://forms.gle/WyqAoh1ixdfq6tgN8?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=)[在我们的 Google Colab 中查看 AlphaEvolve 的数学结果](https://colab.research.google.com/github/google-deepmind/alphaevolve_results/blob/master/mathematical_results.ipynb?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=)

**致谢**

AlphaEvolve 由 Matej Balog、Alexander Novikov、Ngân Vũ、Marvin Eisenberger、Emilien Dupont、Po-Sen Huang、Adam Zsolt Wagner、Sergey Shirobokov、Borislav Kozlovskii、Francisco J. R. Ruiz、Abbas Mehrabian、M. Pawan Kumar、Abigail See、Swarat Chaudhuri、George Holland、Alex Davies、Sebastian Nowozin 和 Pushmeet Kohli 开发。这项研究是我们「用 AI 进行算法发现」计划的一部分。

我们诚挚感谢以下人士的贡献、建议与支持：Jean-Baptiste Alayrac、Ankit Anand、Natasha Antropova、Giorgio Arena、Mohammadamin Barekatain、Johannes Bausch、Henning Becker、Daniel Belov、Alexander Belyaev、Sebastian Bodenstein、Sebastian Borgeaud、Calin Cascaval、Indranil Chakraborty、Benjamin Chetioui、Justin Chiu、Christopher Clark、Marco Cornero、Jeff Dean、Gaurav Dhiman、Yanislav Donchev、Srikanth Dwarakanath、Jordan Ellenberg、Alhussein Fawzi、Michael Figurnov、Aaron Gentleman、Bogdan Georgiev、Sergio Guadarrama、Demis Hassabis（德米斯·哈萨比斯）、Patrick Heisel、Chase Hensel、Koray Kavukcuoglu、Sultan Kenjeyev、Aliia Khasanova、Sridhar Lakshmanamurthy、Sergei Lebedev、Dmitry Lepikhin、Daniel Mankowitz、Andrea Michi、Kieran Milan、Vinod Nair、Robert O'Callahan、Cosmin Paduraru、Stig Petersen、Federico Piccinini、Parthasarathy Ranganatha、Bernardino Romera-Paredes、Georges Rotival、Kirk Sanders、Javier Gomez Serrano、Oleg Shyshkov、Timur Sitdikov、Tammo Spalink、Kerry Takenaka、Richard Tanburn、Terence Tao、Amin Vahdat、JD Velasquez、Dimitrios Vytiniotis、Julian Walker 和 Pengming Wang。更多细节请参阅我们的白皮书。

我们感谢 Armin Senoner、Juanita Bawagan、Jane Park、Arielle Bier 和 Molly Beck 对本文的反馈以及对本次发布工作的帮助；感谢 William Hood、Irina Andronic、Victoria Johnston、Lucas Dixon、Adam Connors 和 Jimbo Wilson 为插图与图表提供的帮助。
