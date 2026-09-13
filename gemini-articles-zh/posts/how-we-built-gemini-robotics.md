---
title: "我们如何构建全新的 Gemini Robotics 模型家族"
title_en: "How we built the new family of Gemini Robotics models"
source: https://blog.google/products-and-platforms/products/gemini/how-we-built-gemini-robotics/
site: gemini
date: 2025-04-01
crawled: 2026-09-13
translated: 2026-09-13
---

# 我们如何构建全新的 Gemini Robotics 模型家族

> 原文：[How we built the new family of Gemini Robotics models](https://blog.google/products-and-platforms/products/gemini/how-we-built-gemini-robotics/) · Google

在 Google DeepMind 准备[宣布](https://deepmind.google/discover/blog/gemini-robotics-brings-ai-into-the-physical-world/)专为机器人设计的新一代 Gemini 2.0 模型家族时，其机器人技术负责人 Carolina Parada 召集团队，对这些技术的能力进行了一次检验。

他们让一台双臂 ALOHA 机器人——一种由多关节、钳状手的灵活金属附肢组成、广泛应用于研究领域的机器人——执行它从未做过的任务，并使用它从未见过的物品。"我们做了各种随性的事情，比如把我的鞋放到桌上，让它把几支笔放进去，"Carolina 说。"机器人花了一点时间理解任务，然后就完成了。"

接下来，他们找到一个玩具篮球框和球，让机器人来一个"扣篮"。Carolina 看着它真的做到了，既骄傲又欣喜。

Carolina 说，亲眼见证这次扣篮是一个"哇"的时刻。

"我们之前训练过帮助机器人完成特定任务、理解自然语言的模型，但这次是一个质的飞跃，"Carolina 说。"这个机器人从未见过任何与篮球相关的东西，也没见过这个玩具。但它理解了某个复杂的概念——'把球扣进去'——并流畅地完成了动作。*而且是第一次尝试。*"

这台全能机器人由 [Gemini Robotics](https://deepmind.google/technologies/gemini-robotics/) 模型驱动，该模型属于面向机器人技术的新一代多模态模型家族。这些模型在 [Gemini 2.0](https://blog.google/technology/google-deepmind/google-gemini-ai-update-december-2024/) 的基础上，通过机器人专属数据的微调，为 Gemini 的文本、视频和音频等多模态输出增加了物理动作能力。"这一里程碑为下一代机器人技术奠定了基础，它们将能在广泛的应用中提供帮助，"Google CEO Sundar Pichai 在 [X 上宣布新模型时](https://x.com/sundarpichai/status/1899838913054744679)表示。

Gemini Robotics 模型高度灵巧、可交互且通用，这意味着它们可以驱动机器人对新物体、新环境和新指令做出反应，而无需进一步训练。考虑到团队的雄心，这一点非常实用。

"我们的使命是构建具身智能（embodied AI），打造能在真实世界帮助你处理日常任务的机器人，"Carolina 说。她对机器人技术的痴迷始于童年的科幻动画片，满怀着让家务自动化的梦想。"最终，机器人将成为我们与 AI 互动的又一个界面，就像我们的手机或电脑一样——是物理世界中的智能体。"

与人类一样，机器人要有效且安全地执行任务，需要两项主要能力：理解与决策的能力，以及采取行动的能力。Gemini Robotics-ER 是一个构建于 Gemini 2.0 Flash 之上的"具身推理"（embodied reasoning）模型，专注于前者：识别眼前的元素，界定它们的大小和位置，并预测移动它们所需的轨迹和抓握方式，随后生成代码来执行动作。我们目前正在向受信任的测试者和合作伙伴开放该模型。

Google DeepMind 同时还推出了 Gemini Robotics——其最先进的视觉-语言-动作（vision-language-action）模型，让机器人能够对场景进行推理、与用户交互并采取行动。至关重要的是，它在机器人学家一直颇为棘手的领域取得了重大进展：灵巧性。"对人类来说自然而然的事情，对机器人来说却很难，"Carolina 解释道。"灵巧性既需要空间推理，也需要复杂的物理操作。在各项测试中，Gemini Robotics 创造了灵巧性方面的新尖端水平，能以流畅的动作和出色的完成时间解决复杂的多步骤任务。"

Gemini Robotics-ER 在具身推理能力方面表现出色，包括检测物体、指向物体的部件、寻找对应点以及进行 3D 物体检测。

![这张拼贴图展示了上述能力的可视化效果。左上：2D 物体检测；右上：指向；左下：多视角对应；右下：3D 物体检测。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Robotics-Inline2.width-1200.format-webp.webp)

在 Gemini Robotics 的驱动下，机器人们已经制作过沙拉、打包过孩子的午餐、玩过井字棋等游戏，甚至折过一只折纸狐狸。

要训练出能完成多种不同类型任务的模型是一项挑战——这主要是因为它与业界的普遍做法背道而驰：通常的做法是针对*单一*任务反复训练模型，直到它能被解决。"相反，我们选择了广泛的任务学习，在数量庞大的任务上训练模型，"Carolina 说。"我们预期在积累一定的训练量之后会涌现出泛化能力，事实证明我们是对的。"

两款模型都能适配多种机器人本体（embodiment），包括面向学术研究的机器人（如双臂 ALOHA 机器），以及由我们的合作伙伴 Apptronik 开发的人形机器人 Apollo。

这些模型可以适配不同的机器人本体，能以不同的形态完成打包午餐盒或擦白板等任务。

![四张机器人执行动作的图片。左上，一个人形机器人在打包午餐；右上，一只小机械臂正从保鲜盒中拿起一颗甜豆；左下，两条大型白色机械臂在工作台上准备执行任务；右下，一只黑色钳状手拿着白板擦位于白板上方。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Robotics-Inline3.width-1200.format-webp.webp)

这种适应能力是通往未来的关键——在未来，机器人可能承担许多截然不同的角色。

"使用高度通用、能力强大的模型的机器人，其应用前景广阔而令人兴奋，"Carolina 说。"它们在那些环境复杂、精度要求高、空间并不适合人类停留的行业里会更有用武之地。它们也可以在以人为本的空间中提供帮助，比如家庭。这还需要几年时间，但这些模型正让我们朝那个方向迈近好几步。"

看来终于会有人在做家务时得到帮手了——虽然要等上一阵子。
