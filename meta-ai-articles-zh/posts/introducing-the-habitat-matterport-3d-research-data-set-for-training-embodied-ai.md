---
title: "推出 Habitat-Matterport 3D 研究数据集，用于训练具身 AI"
title_en: "Introducing the Habitat-Matterport 3D research data set for training embodied AI"
date: 2021-06-30
source: https://ai.facebook.com/blog/introducing-the-habitat-matterport-3d-research-data-set-for-training-embodied-ai
crawled: 2026-09-22
translated: 2026-09-22
---

# 推出 Habitat-Matterport 3D 研究数据集，用于训练具身 AI

> 原文：[Introducing the Habitat-Matterport 3D research data set for training embodied AI](https://ai.facebook.com/blog/introducing-the-habitat-matterport-3d-research-data-set-for-training-embodied-ai) · Meta AI（Wayback 存档）

计算机视觉与自然语言处理的 AI 模型通常用从互联网策展的文本、图像、音频和视频来训练。但具身 AI——对拥有物理或虚拟身体（机器人和第一人称个人助理）的智能系统的研究与开发——有着不同的需求。想象一下，你走到家用机器人面前问：「嘿，机器人，去看看我的笔记本电脑是不是在桌上，如果在就拿来给我好吗？」或者问运行在你 AR 眼镜上的 AI 助手：「嘿，我上次看见我的钥匙是在哪里？」这些任务要求 AI 像人一样理解物理世界并与之交互：从任意视角识别不同物体、区分台面与书桌等等。为了安全且大规模地开发这类机器人与第一人称个人助理，我们必须在仿真中用丰富、逼真的 3D 空间来训练它们。遗憾的是，这样的 3D 数据非常稀缺。2D 图像数据集多年来已增长到包含数十亿张图像，而 3D 空间数据集却只有几十栋建筑。因此，具身 AI 的进步受到掣肘。

今天，Facebook AI 与 Matterport 合作，发布一个采用 Matterport 开源许可证的数据集——有史以来最大的室内 3D 扫描数据集——以造福研究社区。Habitat-Matterport 3D 研究数据集（HM3D）包含 1,000 个与 Habitat 兼容的 3D 扫描，由精确按比例缩放的住宅空间（公寓、多户住宅、独栋住宅）以及商业空间（办公楼、零售店等）组成。我们相信 HM3D 将在推进具身 AI 研究中发挥重要作用。借助这一数据集，家用机器人、AI 助手等具身 AI 智能体可以接受训练，去理解真实世界环境的复杂性——识别物体、房间与空间，或学习如何导航和遵循指令——且训练场景彼此差异极大。要完成寻找放错位置的物体或取回实物这类复杂任务，具身 AI 智能体需要构建地图与情景记忆表示（以回忆它已观察过什么）、理解语音与音频线索，并且在需要上下楼梯时展现出精细的运动控制。

Facebook AI 与 Matterport 合作提供 Matterport 开源 HM3D 数据集的访问，出于双方对解决具身 AI 这一关键需求领域的共同兴趣：用数据激发更大的创新。Matterport 是空间数据公司，引领着建成世界的数字化转型，其一体化 3D 数据平台已将数百万物理空间转化为沉浸式数字孪生。AI Habitat 是 Facebook AI 最先进的开放仿真平台，用于面向多种任务训练具身智能体。凭借快于实时的速度，它让研究者可以轻松高效地进行大量重复试验。得益于与 Matterport 的合作，研究者现在能够获得训练机器人及其他智能系统所需的关键规模。未来，我们希望把数据集扩展到更多国家的扫描；为数据集增加语义标注，从而承担物体检索等高层理解任务；并研究动态变化的环境，让仿真不再是静态的，而是流动的。这将使仿真训练环境更贴近真实世界——在那里人与宠物自由走动，手机、钱包、鞋子这些日常物品一天之中并不总在同一个位置。

我们相信，具身 AI 的进步可以帮助开发者构建并训练具备深度情境理解能力的助理，让它们有能力在周围世界中导航。终有一天，具身智能体将解锁全新的体验，提升使用者的生活质量——无论他们身在何处、使用何种设备。HM3D 现已免费开放用于学术与非商业研究。在此获取：https://matterport.com/habitat-matterport-3d-research-dataset

我们要感谢 Aaron Gokaslan、Alexander William Clegg、Erik Wijmans、John Turner、Oleksandr Maksymets、Wojtek Galuba、Yili Zhao、Eric Undersander、Santhosh Kumar Ramakrishnan 和 Jitendra Malik 的贡献，以及 UT-Austin、西蒙弗雷泽大学和佐治亚理工的众多合作伙伴在构建 HM3D 过程中的帮助。

**作者**

- Dhruv Batra，研究科学家
- Andrew Westbury，研究项目经理
