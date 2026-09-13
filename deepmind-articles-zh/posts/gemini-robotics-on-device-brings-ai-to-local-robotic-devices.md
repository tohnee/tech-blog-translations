---
title: "Gemini Robotics On-Device 把 AI 带到本地机器人设备"
title_en: "Gemini Robotics On-Device brings AI to local robotic devices"
source: https://deepmind.google/blog/gemini-robotics-on-device-brings-ai-to-local-robotic-devices/
site: deepmind
date: 2025-06-24
crawled: 2026-09-13
translated: 2026-09-13
---

# Gemini Robotics On-Device 把 AI 带到本地机器人设备

> 原文：[Gemini Robotics On-Device brings AI to local robotic devices](https://deepmind.google/blog/gemini-robotics-on-device-brings-ai-to-local-robotic-devices/) · Google DeepMind

我们正在推出一个高效的端侧机器人模型，具备通用灵巧性与快速任务适配能力。

今年 3 月，我们推出了 [Gemini Robotics](https://deepmind.google/discover/blog/gemini-robotics-brings-ai-into-the-physical-world/)——我们最先进的 VLA（视觉-语言-动作）模型，把 Gemini 2.0 的多模态推理和真实世界理解能力带入物理世界。

今天，我们推出 Gemini Robotics On-Device，这是我们经过优化、可在机器人设备上本地运行的最强大 VLA 模型。Gemini Robotics On-Device 展现出强大的通用灵巧性与任务泛化能力，并且针对在机器人本体上高效运行进行了优化。

由于模型独立于数据网络运行，它非常适合对延迟敏感的应用，并能在间歇性或零连接的环境中保证稳健性。

我们同时发布 [Gemini Robotics SDK](https://github.com/google-deepmind/gemini-robotics-sdk)，帮助开发者轻松评估 Gemini Robotics On-Device 在他们的任务与环境中的表现、在我们的 [MuJoCo](https://github.com/google-deepmind/aloha_sim) 物理模拟器中测试我们的模型，并快速将其适配到新领域——只需 50 到 100 个示范即可。开发者可以注册我们的可信测试者计划来获取 SDK。

## 模型能力与性能

Gemini Robotics On-Device 是一个面向双臂机器人的机器人基础模型，其工程设计力求占用最少的计算资源。它建立在 Gemini Robotics 的任务泛化与灵巧性能力之上，并且：

- 为灵巧操作的快速实验而设计。
- 可通过微调适配新任务以提升性能。
- 经优化可在本地以低延迟推理运行。

Gemini Robotics On-Device 在广泛的测试场景中实现了强大的视觉、语义与行为泛化，能遵循自然语言指令，并完成高度灵巧的任务，如拉开背包拉链或折叠衣物——这一切都直接在机器人上运行。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![你的浏览器不支持视频标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

在我们的评测中，我们的端侧模型在完全本地运行的情况下展现出强大的泛化性能。

![一张标题为「跨 9 项任务的泛化基准测试结果」（Generalization Benchmark results across 9 tasks）的柱状图，对比三个模型——Gemini Robotics（蓝色）、Previous Best On-Device（青色）和 Gemini Robotics On-Device（紫色）——在视觉、语义和动作泛化上的成功率。在这三项基准上，Gemini Robotics 成功率最高（介于 0.6 到 0.75），Gemini Robotics On-Device 紧随其后（约在 0.52 到 0.74 之间），而 Previous Best On-Device 模型表现明显偏低（介于 0.11 到 0.36）。](https://lh3.googleusercontent.com/I6Zopg7Y_-VweSLsrzuRFGXeuIvUAJPXwEnxvnFyGjqWl65K3luU2WFHyGEu4xvC-QWB7jW62FM5j_oKk6pvZB7X6QXsKKdYehyJZYoKmHem7MAJ35U=w1440)

图表评估 Gemini Robotics On-Device 的泛化性能，并与我们的旗舰模型 Gemini Robotics 及此前最佳的端侧模型对比。

在更具挑战性的分布外任务和复杂的多步骤指令上，Gemini Robotics On-Device 也优于其他端侧方案。对于追求业界领先结果、又不受端侧限制约束的开发者，我们还提供 Gemini Robotics 模型。

![一张标题为「指令遵循基准测试衡量可控性」（Instruction Following Benchmark measuring steerability）的柱状图，对比三个模型在「简单」和「困难」任务上的成功率。在这两个类别中，Gemini Robotics（蓝色）成功率最高，Gemini Robotics On-Device（紫色）次之，Previous Best On-Device 模型（青色）表现最低。](https://lh3.googleusercontent.com/SVQOj7ZJccb_C3l3VQ6aoXprwYDyozOFLTswucWr92L5e9vexhETlk4Oib6tym_v6IdhvpVzrmTVIlR2KHBohma7LtQ-kxTzZkYnmVkXoNb5bajn=w1440)

图表评估 Gemini Robotics On-Device 的指令遵循性能，并与我们的旗舰模型 Gemini Robotics 及此前最佳的端侧模型对比。

欲了解更多评测内容，请阅读我们的 [Gemini Robotics 技术报告](https://arxiv.org/pdf/2503.20020)。

## 可适配新任务，跨本体泛化

Gemini Robotics On-Device 是我们首个开放微调的 VLA 模型。虽然许多任务开箱即用，开发者也可以选择适配模型，以在其应用中取得更好的性能。我们的模型只需 50 到 100 个示范就能快速适配新任务——这表明这个端侧模型能将其基础知识很好地泛化到新任务上。

这里我们展示 Gemini Robotics On-Device 在涉及向新模型微调的任务上，如何超越当前最佳的端侧 VLA。我们在七项难度各异的灵巧操作任务上测试了该模型，包括拉上饭盒拉链、画一张卡片和倾倒沙拉酱。

![一张标题为「快速适配」（Fast Adaptation）的柱状图，对比三个模型在「快速适配任务的平均成功率」。Gemini Robotics（蓝色）成功率最高，为 0.8；Gemini Robotics On-Device（紫色）约为 0.68；Previous Best On-Device 模型（青色）约为 0.53。](https://lh3.googleusercontent.com/4YSKJSyeJJsQHU8Tz0jpkDloDAkF7Yb7mtcy8ECn5qC4nBFY9_75DSs1-qr-XNRGZvAvFZ2NaJ5LABD16QBZrPPufZt3oyTxWWKGh0M7im9uFt6edQ=w1440)

图表展示 Gemini Robotics On-Device 在少于 100 个样本下的任务适配性能。

我们进一步把 Gemini Robotics On-Device 模型适配到不同的机器人本体。虽然我们只用 [ALOHA 机器人](https://aloha-2.github.io/)训练了模型，但我们成功把它进一步适配到双臂 [Franka FR3 机器人](https://franka.de/franka-research-3)和 Apptronik 的 [Apollo 人形机器人](https://apptronik.com/apollo)上。

在双臂 Franka 上，模型执行通用的指令遵循任务，包括处理此前未见过的物体和场景，完成折叠连衣裙等灵巧任务，或执行需要精确与灵巧的[工业皮带装配任务](https://www.nist.gov/el/intelligent-systems-division-73500/robotic-grasping-and-manipulation-assembly/assembly)。

在 Apollo 人形机器人上，我们把模型适配到了一个差异显著的本体。这个相同的通用模型能够以通用的方式遵循自然语言指令并操作不同物体，包括此前未见过的物体。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![你的浏览器不支持视频标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

## 负责任的开发与安全

我们按照 [AI 原则](https://ai.google/principles/?utm_source=&utm_medium=&utm_campaign=&utm_content=)开发所有 Gemini Robotics 模型，并采用横跨语义安全与物理安全的[整体性安全方法](https://sites.google.com/corp/view/safe-robots)。

在实践中，我们通过 [Live API](https://ai.google.dev/gemini-api/docs/live?utm_source=&utm_medium=&utm_campaign=&utm_content=) 捕捉语义与内容安全，并将我们的模型与低层安全关键控制器对接以执行动作。我们建议在我们最新开发的[语义安全基准](https://asimov-benchmark.github.io/)上评估端到端系统，并在所有层级开展[红队测试演练](https://predictive-red-team.github.io/)，以暴露模型的安全漏洞。

我们的负责任开发与创新（ReDI）团队持续分析所有 Gemini Robotics 模型的现实世界影响并提供建议，寻找最大化其社会影响、最小化风险的途径。随后，我们的责任与安全委员会（RSC）审查这些评估，提供反馈并融入模型开发，以进一步最大化收益、最小化风险。

为了更深入地了解 Gemini Robotics On-Device 的使用方式与安全画像，并收集反馈，我们首先面向一个精选的可信测试者小组发布。

## 加速机器人技术的创新

Gemini Robotics On-Device 标志着让强大机器人模型更易获取、更易适配的一步——我们的端侧方案将帮助机器人社区应对重要的延迟与连接挑战。

Gemini Robotics SDK 将让开发者把模型适配到各自的具体需求，从而进一步加速创新。通过我们的[可信测试者计划](https://docs.google.com/forms/d/1sM5GqcVMWv-KmKY3TOMpVtQ-lDFeAftQ-d9xQn92jCE/edit?ts=67cef986)注册以获取模型与 SDK 访问权限。

我们期待看到机器人社区用这些新工具创造出什么，同时我们将继续探索把 AI 带入物理世界的未来。

[注册我们的可信测试者计划](https://docs.google.com/forms/d/1sM5GqcVMWv-KmKY3TOMpVtQ-lDFeAftQ-d9xQn92jCE/edit?ts=67cef986&utm_source=&utm_medium=&utm_campaign=&utm_content=)[阅读 Gemini Robotics 技术报告](https://arxiv.org/pdf/2503.20020)[在模拟中测试 ALOHA 机器人](https://github.com/google-deepmind/aloha_sim)

**致谢**

我们诚挚感谢以下人士的贡献、建议与支持：Abbas Abdolmaleki、Saminda Abeyruwan、Joshua Ainslie、Jean-Baptiste Alayrac、Montserrat Gonzalez Arenas、Travis Armstrong、Maria Attarian、Ashwin Balakrishna、Yanan Bao、Clara Barbu、Catarina Barros、Robert Baruch、Nathan Batchelor、Maria Bauza、Lucas Beyer、Jeff Bingham、Michael Bloesch、Michiel Blokzijl、Steven Bohez、Konstantinos Bousmalis、Demetra Brady、Philemon Brakel、Anthony Brohan、Thomas Buschmann、Arunkumar Byravan、Kendra Byrne、Serkan Cabi、Ken Caluwaerts、Federico Casarini、Christine Chan、Oscar Chang、Jose Enrique Chen、Xi Chen、Huizhong Chen、Hao-Tien Lewis Chiang、Krzysztof Choromanski、Adrian Collister、Kieran Connell、David D'Ambrosio、Sudeep Dasari、Todor Davchev、Coline Devin、Norman Di Palo、Tianli Ding、Adil Dostmohamed、Anca Dragan、Yilun Du、Debidatta Dwibedi、Michael Elabd、Tom Erez、Claudio Fantacci、Cody Fong、Erik Frey、Chuyuan Fu、Frankie Garcia、Ashley Gibb、Marissa Giustina、Keerthana Gopalakrishnan、Laura Graesser、Simon Green、Oliver Groth、Roland Hafner、Leonard Hasenclever、Sam Haves、Nicolas Heess、Brandon Hernaez、Tim Hertweck、Alexander Herzog、R. Alex Hofer、Sandy H Huang、Jan Humplik、Atil Iscen、Mithun George Jacob、Deepali Jain、Sally Jesmonth、Ryan Julian、Dmitry Kalashnikov、M. Emre Karagozler、Stefani Karp、Chase Kew、Jerad Kirkland、Sean Kirmani、Yuheng Kuang、Thomas Lampe、Antoine Laurens、Isabel Leal、Alex X. Lee、Tsang-Wei Edward Lee、Jennie Lees、Jacky Liang、Yixin Lin、Li-Heng Lin、Caden Lu、Sharath Maddineni、Anirudha Majumdar、Kevis-Kokitsi Maninis、Siobhan Mcloughlin、Assaf Hurwitz Michaely、Joss Moore、Robert Moreno、Thomas Mulc、Michael Neunert、Francesco Nori、Dave Orr、Carolina Parada、Emilio Parisotto、Peter Pastor、André Susano Pinto、Acorn Pooley、Grace Popple、Thomas Power、Alessio Quaglino、Haroon Qureshi、Kanishka Rao、Dushyant Rao、Krista Reymann、Martin Riedmiller、Francesco Romano、Keran Rong、Dorsa Sadigh、Stefano Saliceti、Daniel Salz、Pannag Sanketi、Mili Sanwalka、Kevin Sayed、Pierre Sermanet、Dhruv Shah、Mohit Sharma、Kathryn Shea、Mohit Shridhar、Charles Shu、Laurent Simon、Vikas Sindhwani、Sumeet Singh、Radu Soricut、Andreas Steiner、Rachel Sterneck、Ian Storz、Razvan Surdulescu、Ben Swanson、Mitri Syriani、Jie Tan、Yuval Tassa、Alan Thompson、Dhruva Tirumala、Jonathan Tompson、Karen Truong、Jake Varley、Siddharth Verma、Grace Vesom、Giulia Vezzani、Oriol Vinyals、Ayzaan Wahid、Zhicheng Wang、Xiaohan Wang、Stefan Welker、Paul Wohlhart、Chengda Wu、Markus Wulfmeier、Fei Xia、Ted Xiao、Annie Xie、Jinyu Xie、Peng Xu、Sichun Xu、Ying Xu、Zhuo Xu、Yuxiang Yang、KongQun Yang、Rui Yao、Sergey Yaroshenko、Matt Young、Wenhao Yu、Wentao Yuan、Martina Zambelli、Xiaohua Zhai、Jingwei Zhang、Tingnan Zhang、Allan Zhou、Yuxiang Zhou、Guangyao (Stannis) Zhou、Howard Zhou。

我们还要感谢为本项目执行数据收集和机器人评测的运营与支持人员。
