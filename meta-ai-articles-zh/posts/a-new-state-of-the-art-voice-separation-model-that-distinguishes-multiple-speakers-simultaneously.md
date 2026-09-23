---
title: "可同时区分多个说话者的全新最先进语音分离模型"
title_en: "A new, state-of-the-art voice separation model that distinguishes multiple speakers simultaneously"
date: 2020-07-10
source: https://ai.facebook.com/blog/a-new-state-of-the-art-voice-separation-model-that-distinguishes-multiple-speakers-simultaneously
crawled: 2026-09-22
translated: 2026-09-22
---

# 可同时区分多个说话者的全新最先进语音分离模型

> 原文：[A new, state-of-the-art voice separation model that distinguishes multiple speakers simultaneously](https://ai.facebook.com/blog/a-new-state-of-the-art-voice-separation-model-that-distinguishes-multiple-speakers-simultaneously) · Meta AI（Wayback 存档）

**研究内容：**我们正在介绍一种新方法，可在单个麦克风上分离多达五个同时说话的声音。我们的方法在多个语音源分离基准上超越了此前最先进的性能，包括那些包含棘手噪声和混响的基准。使用 WSJ0-2mix 和 WSJ0-3mix 数据集，以及新创建的包含四个和五个同时说话者的变体，我们的模型在尺度不变 SI-SNR（信噪比，衡量分离质量的常用指标）上比当前最先进模型提升了超过 1.5 dB（分贝）。

为构建该模型，我们使用了一种直接作用于原始音频波形的新型循环神经网络架构。此前最佳的模型使用掩码（mask）和解码器来区分每个说话者的声音，这类模型在说话者数量较多或未知时性能会迅速退化。与标准语音分离系统一样，我们的模型需要预先知道说话者总数。但为了应对说话者数量未知的挑战，我们构建了一个能自动检测说话者数量并选择最相关模型的新系统。

**工作原理：**语音分离模型的主要目标是：给定一段混叠的语音信号输入，估计出各个输入源，并为每个说话者生成一路隔离的输出声道。我们的模型使用编码器网络将输入信号映射到潜在表示。我们采用由多个模块组成的语音分离网络，其输入是潜在表示，输出是每个说话者的估计信号。以往方法在执行分离时通常使用掩码，这在掩码未定义时会带来问题，且部分信号信息可能在处理中丢失。我们训练模型并通过置换不变训练（permutation invariant training）以多个损失函数直接优化 SI-SNR。我们在每个分离模块之后插入一个损失函数，进一步改善优化过程。最后，为确保每个说话者始终被映射到特定的输出声道，我们利用预训练的说话者识别模型加入了一个感知损失函数。

我们还构建了一个处理未知数量多说话者分离的新系统。做法是：分别训练用于分离两个、三个、四个和五个说话者的模型。我们先把输入混叠语音喂给为最多五个同时说话者设计的模型，让它检测当前存在多少个活跃（非静音）声道。然后，我们用按活跃说话者数量训练的模型重复同样的过程，检查是否所有输出声道都活跃。不断重复，直到所有声道都被激活，或找到目标说话者数量最少的模型。

**为什么重要：**从许多人的交谈中分离出单个声音的能力，可以改善和增强我们日常生活中广泛使用的各类应用，如语音消息、语音助手和视频工具，以及 AR/VR 创新。它还能改善助听器用户的音质，让人在派对、餐厅或大型视频通话等嘈杂喧闹的环境中更容易听清他人说话。除了分离不同人声，我们的新系统还可用于从混叠声音中分离其他类型的语音信号，例如背景噪声。这项工作也可应用于音乐录音，改进我们此前将不同乐器从单一音频文件中分离的工作。作为下一步，我们将继续改进模型的生成特性，直到它在真实世界条件下达到高性能。

阅读完整论文：Voice separation with an unknown number of multiple speakers

音频样本可在此处查看。
