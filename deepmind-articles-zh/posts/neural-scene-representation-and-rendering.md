---
title: "神经场景表示与渲染"
title_en: "Neural scene representation and rendering"
source: https://deepmind.google/blog/neural-scene-representation-and-rendering/
site: deepmind
date: 2018-06-14
crawled: 2026-09-13
translated: 2026-09-13
---

# 神经场景表示与渲染

> 原文：[Neural scene representation and rendering](https://deepmind.google/blog/neural-scene-representation-and-rendering/) · Google DeepMind

我们对视觉场景的理解远不止眼前所见：我们的大脑会调动先验知识进行推理，做出远远超越投射到视网膜上的光线模式的推断。例如，第一次走进一个房间时，你会立刻认出房内有哪些物品以及它们的位置。如果你看到一张桌子的三条腿，你会推断大概率还有第四条腿，只是被遮挡而看不见，并且形状和颜色与前三条相同。即便你看不到房间里的一切，你多半也能勾勒出它的布局，或想象出从另一个角度看它是什么样子。

这些视觉与认知任务对人类而言看似毫不费力，但对人工智能系统而言却是重大挑战。如今，最先进的视觉识别系统是使用由人工制作的大规模标注图像数据集训练的。获取这些数据既昂贵又耗时，需要人们对数据集中每个场景里的每个物体的方方面面进行标注。其结果是，往往只能捕捉到场景整体内容的一小部分，这限制了基于这些数据训练的人工视觉系统。随着我们开发在真实世界中运行的更复杂的机器，我们希望它们能充分理解自己的周围环境：最近的、可以坐下的表面在哪里？沙发是什么材料做的？哪个光源制造了这些影子？电灯开关可能在哪儿？

在这项[发表于《科学》（Science）](http://science.sciencemag.org/cgi/content/full/360/6394/1204?ijkey=kGcNflzOLiIKQ&keytype=ref&siteid=sci)的工作中（[开放获取版本](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/neural-scene-representation-and-rendering/Neural%20Scene%20Representation%20and%20Rendering%20-%20Related%20Work.pdf)），我们介绍了生成查询网络（Generative Query Network，GQN）——一个让机器仅凭自己在场景中移动时获得的数据就能学会感知周围环境的框架。与婴儿和动物十分相似，GQN 通过尝试理解它对周围世界的观察来学习。在此过程中，GQN 学到了合理场景及其几何特性，而无需任何人工对场景内容进行标注。

GQN 模型由两部分组成：一个表示网络和一个生成网络。表示网络将智能体的观察作为输入，产出一个描述底层场景的表示（一个向量）。然后，生成网络从一个此前未观察过的视角预测（「想象」）该场景。

表示网络并不知道生成网络将被要求预测哪些视角，因此它必须找到一种高效方式，尽可能准确地描述场景的真实布局。它通过在一个简洁的分布式表示中捕捉最重要的元素来实现这一点，例如物体的位置、颜色和房间布局。在训练期间，生成器学习环境中典型的物体、特征、关系和规律。这一共享的「概念」集合使表示网络能够以高度压缩、抽象的方式描述场景，把在必要处填充细节的工作留给生成网络。例如，表示网络会把「蓝色立方体」简洁地表示为少数几个数字，而生成网络则知道它从某个特定视角来看会呈现为什么样的像素。

我们在一个模拟 3D 世界的一系列程序化生成环境中对 GQN 进行了受控实验，其中包含多个位置、颜色、形状和纹理随机的物体，并带有随机化的光源和严重的遮挡。在这些环境中训练之后，我们使用 GQN 的表示网络为新的、此前未见过的场景构建表示。我们在实验中表明，GQN 展现出以下几项重要特性：

- GQN 的生成网络能够以惊人的精度从新的视角「想象」此前未见过的场景。在给定场景表示和新的相机视角时，它无需对透视、遮挡或光照规律做任何先验设定，就能生成清晰的图像。因此，这个生成网络是一个从数据中学习得到的近似[渲染器](https://en.wikipedia.org/wiki/Rendering_(computer_graphics))：

![两幅图像对比观察与神经渲染。「观察」部分是一个盒子内两个 3D 形状在单一视角下的静态图像；「神经渲染」部分是一段动态图像，从多个侧面和角度观看同一个盒子。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62268c802b032b4a45307265_GQN202.gif)

- GQN 的表示网络能够在没有任何物体级标注的情况下学会计数、定位和分类物体。尽管它的表示可以非常小，GQN 在查询视角处的预测却高度准确，与真值几乎难以区分。这意味着表示网络的感知是准确的，例如它能识别出构成下面场景中方块的精确构型：

![观察与神经渲染并排展示。「观察」部分是黑色背景上一个多彩 3D 形状的静态图像；「神经渲染」部分是同一个 3D 形状在空间中旋转的画面，让我们从每个角度看到它。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62268c9404f53c40276f787e_GQN203.gif)

- GQN 能够表示、度量和降低不确定性。即便场景内容并未完全可见，它也能在其对场景的信念中考虑不确定性，并且能够把场景的多个局部视图组合成一个连贯的整体。这一点由下图中它的第一人称视角与俯视预测展示。模型通过预测结果的变化性来表达其不确定性，随着它在迷宫中移动，不确定性逐渐降低（灰色圆锥表示观察位置，黄色圆锥表示查询位置）：

![在 3D 迷宫中移动时，有一系列静态观察。其下方是两段对应的视频，分别代表神经渲染与真值。一幅地图展示了视角在空间中移动的轨迹。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62268ca3933713959ce79a77_GQN201.gif)

- GQN 的表示支持鲁棒且数据高效的强化学习。在给定 GQN 紧凑表示的情况下，最先进的深度强化学习智能体相比无模型基线智能体，能够以更数据高效的方式学会完成任务，如下图所示。对这些智能体而言，生成网络中编码的信息可以被看作对环境的「先天的」知识：

![对比使用 GQN 表示与使用原始像素的强化学习智能体性能。左侧为观察、GQN 预测和真值的示例，显示一只机械臂与物体交互。两幅折线图绘制了固定相机与移动相机两种设置下 3,000 万个训练回合内奖励的变化，表明 GQN 表示（蓝线）比原始像素（橙线）更快地达到更高奖励，尤其是在移动相机条件下——此时原始像素完全无法学习。](https://lh3.googleusercontent.com/HwNXPghKHsh5IWswYCg7CARynSm7kt6hd5RX-bd1cmZrk0GNJGq1r2WuJkQsYmgN8JBlvFG6zYkHH2mbZhTEk73zO0bc2AG08vw84zSls7hfcANjkw=w1440)

使用 GQN，我们观察到策略学习的数据效率大幅提升：与使用原始像素的标准方法相比，仅用约四分之一的交互次数就达到了收敛水平的性能。

GQN 建立在多视图几何、生成建模、无监督学习和预测学习等领域近期大量相关工作之上，我们在[这里](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/neural-scene-representation-and-rendering/Neural%20Scene%20Representation%20and%20Rendering%20-%20Related%20Work.pdf)、《[Science 论文](http://science.sciencemag.org/cgi/content/full/360/6394/1204?ijkey=kGcNflzOLiIKQ&keytype=ref&siteid=sci)》和[开放获取版本](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/neural-scene-representation-and-rendering/Neural%20Scene%20Representation%20and%20Rendering%20-%20Related%20Work.pdf)中对此进行了讨论。它展示了一种学习物理场景紧凑、有根基表示的新颖方式。至关重要的是，所提出的方法不需要领域特定的工程，也不需要对场景内容进行耗时的标注，因此同一个模型可以应用于一系列不同的环境。它还学到了一个强大的神经渲染器，能够从新的视角生成场景的准确图像。

与更传统的计算机视觉技术相比，我们的方法仍有许多局限，而且目前只在合成场景上进行过训练。不过，随着新的数据来源变得可用以及我们硬件能力的进步，我们预计将能够研究把 GQN 框架应用于真实场景的高分辨率图像。在未来的工作中，探索 GQN 在场景理解更广泛方面的应用也将十分重要，例如通过跨越空间和时间进行查询来学习关于物理和运动的常识性概念，以及在虚拟现实和增强现实中的应用。

虽然在我们的方法准备好投入实际应用之前还有大量研究工作要做，但我们相信这项工作朝着完全自主的场景理解迈出了相当大的一步。

**附注**

观看视频请见[这里](https://youtu.be/G-kWNQJ4idw)。

在《[Science 论文](http://science.sciencemag.org/cgi/content/full/360/6394/1204?ijkey=kGcNflzOLiIKQ&keytype=ref&siteid=sci)》中进一步了解该方法。

下载《[Science 论文](http://science.sciencemag.org/content/sci/360/6394/1204.full.pdf?ijkey=kpkRRXA1ckHD6&keytype=ref&siteid=sci)》 [PDF]。

下载一份[开放获取版本](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/neural-scene-representation-and-rendering/Neural%20Scene%20Representation%20and%20Rendering%20-%20Related%20Work.pdf) [PDF]。

在[这里](https://github.com/deepmind/gqn-datasets)下载论文所用的数据集。

下载扩展的[相关工作列表](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/neural-scene-representation-and-rendering/Neural%20Scene%20Representation%20and%20Rendering%20-%20Related%20Work.pdf) [PDF]。

下载配套美术素材（[竖版](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/neural-scene-representation-and-rendering/Neural%20Scene%20Representation%20and%20Rendering.jpeg)或 [16:9](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/neural-scene-representation-and-rendering/Neural%20Scene%20Representation%20and%20Rendering%2016x9.jpeg)）。

这项工作由 S. M. Ali Eslami、Danilo J. Rezende、Frederic Besse、Fabio Viola、Ari S. Morcos、Marta Garnelo、Avraham Ruderman、Andrei A. Rusu、Ivo Danihelka、Karol Gregor、David P. Reichert、Lars Buesing、Theophane Weber、Oriol Vinyals、Dan Rosenbaum、Neil Rabinowitz、Helen King、Chloe Hillier、Matt Botvinick、Daan Wierstra、Koray Kavukcuoglu 和 Demis Hassabis 完成。
