---
title: "一个通用智能体"
title_en: "A Generalist Agent"
source: https://deepmind.google/blog/a-generalist-agent/
site: deepmind
date: 2022-05-12
crawled: 2026-09-13
translated: 2026-09-13
---

# 一个通用智能体

> 原文：[A Generalist Agent](https://deepmind.google/blog/a-generalist-agent/) · Google DeepMind

受大规模语言建模进展的启发，我们将类似的方法应用于在文本输出领域之外构建单一通用智能体。这个智能体被称为 Gato，它作为一个多模态、多任务、多具身的通用策略工作。同一个网络、同一套权重，可以玩 Atari 游戏、为图像写说明文字、聊天、用真实机械臂堆叠积木等等，并根据上下文决定输出文本、关节力矩、按键动作还是其他 token。

![中央蓝色图标标注为"Gato"，通过箭头连接到多样的多模态任务，包括 3D 环境、Atari 游戏、物理模拟、聊天机器人对话、图像说明文字生成和机械臂控制。](https://lh3.googleusercontent.com/T0NXTmIR8b3kxzy_7tmN4DgluPggtpEb6HP6Pq2pH9PvtE7wMgmkbuJQKDgIAgRlo5YiXkdkX55YMGI77kZ2aAFzgtlMm_Ov3-b9wABFatqBmfY9BA=w1440)

在 Gato 的训练阶段，来自不同任务和模态的数据被序列化为扁平的 token 序列，分批后由一个类似大语言模型的 transformer 神经网络处理。损失函数经过掩码处理，使 Gato 只对动作和文本目标进行预测。

![图示 Gato 模型的训练方式：多样的模态数据（Atari、文本、图像、本体感觉）被分词并排列成批量输入，由 Gato 网络处理，生成经过批量和掩码的移位目标用于优化。](https://lh3.googleusercontent.com/dELldQjUlVR_3wIjXUIaSISuvbCZTDQFraNENfkvTW5TsMznAU6l_VzLrVe4QclFyp06qaWeMVDrknN0bgWYOrGMNhDMGr_RK9ZUZFi7leIS7BQP=w1440)

部署 Gato 时，先对提示词（例如一段示范）进行分词，形成初始序列。接着，环境给出第一个观测，该观测同样被分词并追加到序列中。Gato 以自回归方式对动作向量进行采样，一次一个 token。

当构成动作向量的所有 token 都被采样完毕（由环境的动作规范决定）后，动作被解码并发送给环境，环境随即前进一步并给出新的观测。然后重复上述过程。模型在其 1024 个 token 的上下文窗口内始终能看到之前所有的观测和动作。

![图示 Gato 模型的部署方式：一个可选的固定提示词被分词，随后是与环境交互循环中的观测序列和自回归采样的动作。](https://lh3.googleusercontent.com/s-5aBCFsPzWWFDHiTRpBuuIDcOhyrS-HX0AxH2Jf0HmD5gheV8po4JS_YoT3iUkhKj9Ksh8X6bjw8xyY8NVGiM9h40GssG4Leo4gvQcuX2uDhtKbRQ=w1440)

Gato 在大量数据集上训练，这些数据既包含模拟环境和真实环境中的智能体经验，也包含多种自然语言和图像数据集。预训练 Gato 模型性能超过专家得分某一百分比的任务数量（按领域分组）如下图所示。

![堆叠面积图，按专家得分百分比展示 Gato 在各任务领域的表现。](https://lh3.googleusercontent.com/FcRbjUl-2s-MlpygxiWSrMKZNDvo8x7MIGlelYkB6IeMItwjLJvW03xs7w3LLDh0KvWG5CioRMNBbjM8XM2g9_Kp_H5p7X8ulzWK4_csO4czvQEgPg=w1440)

下面的图片还展示了具备相同权重的预训练 Gato 模型如何完成图像说明文字生成、交互式对话和机械臂控制等众多任务。

![十张配有说明文字的图片，展示预训练的 Gato 模型如何生成图像说明文字。](https://lh3.googleusercontent.com/m_EZIGaZ5a4nJEcmQkxXGow-KTh1iGv-VMdimwSYnVAHJimsqS5-KYW7v3qrzu78wznFAgylL5ExKAlsHh6nvuOAEy2h1vJoi024Q0PwCMy1znua=w1440)

![聊天机器人对话，展示具备相同权重的预训练 Gato 模型如何进行交互式对话。](https://lh3.googleusercontent.com/-4PURVjQgptdksFcPBUtyDYvlK1gvTZWm4MrAyVY04hxPFHYndT5kCh4F6hRHFAthAtCkOgqf3dsfUkiJw3FJx2eQzx4e84UUU3mpNAYKu1YHtm5QVI=w1440)

![绿色立方体、红色梯形和紫色 3D 八边形摆放在灰色地面上。该图像重复八次，展示一个黑色抓取器从上方拾起并放下每个物体。](https://lh3.googleusercontent.com/Vz2LuGHS5eXOgfMil_9h03VymgRDd9yFzD3SQH76ao0Uda3Ncn8W2HYSqD6QhBG-LV0kg3VdhShvsFQhmfVJ28ZnSSNXIl4GABiaNcKwRgoMQsZdVg=w1440)
