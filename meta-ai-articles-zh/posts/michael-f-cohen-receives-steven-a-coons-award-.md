---
title: "Michael F. Cohen 荣获 Steven A. Coons 奖"
title_en: "Michael F. Cohen receives Steven A. Coons Award"
date: 2019-05-24
source: https://ai.facebook.com/blog/michael-f-cohen-receives-steven-a-coons-award-
crawled: 2026-09-22
translated: 2026-09-22
---

# Michael F. Cohen 荣获 Steven A. Coons 奖

> 原文：[Michael F. Cohen receives Steven A. Coons Award](https://ai.facebook.com/blog/michael-f-cohen-receives-steven-a-coons-award-) · Meta AI（Wayback 存档）

Facebook 计算摄影总监 Michael F. Cohen 成为 2019 年度「Steven A. Coons 计算机图形学杰出创造性贡献奖」得主。该奖项由 ACM SIGGRAPH 每两年颁发给一位个人，以表彰其在计算机图形学与交互技术领域的杰出终身贡献。在 Facebook，Cohen 领导计算摄影方向的研究工作，聚焦 3D 照片等沉浸式媒体。他此前曾于 1998 年获得 SIGGRAPH 成就奖，并于 2007 年当选 ACM Fellow。

「Michael 毕生的工作涵盖了许多重要的计算机图形学领域，包括逼真渲染、模拟与编辑、光场渲染和计算摄影。」核心科技 AR/VR 工程总监 Amir Frenkel 说，「我们能与不止一位、而是两位 Steven Anson Coons 奖得主共事，实在幸运至极！」他指的正是 Cohen 和 Jessica Hodgins——后者领导 Facebook AI 位于匹兹堡的实验室，于 2017 年获得 Steven A. Coons 奖。

获奖公告全文如下。

## 2019 年 Steven A. Coons 奖：Michael F. Cohen

ACM SIGGRAPH 荣幸地将 2019 年度 Steven A. Coons 计算机图形学杰出创造性贡献奖授予 Michael F. Cohen。他之所以当选，不仅因为在众多研究领域的开创性工作——辐射度（radiosity）、动作模拟与编辑、光场渲染、抠图与合成、计算摄影等——还因为他对计算机图形学社区的长期服务。Cohen 正是这一奖项设立所要表彰的、对本领域终身贡献的典范。

Cohen 大量工作的共同点，是把艺术家的敏感与严谨的底层物理相结合，为用户提供一种指定艺术目标或约束的方式（往往是实时的），同时保持物理上的合理性。

Cohen 最早的主要研究贡献在逼真渲染领域，尤其是辐射度研究：使用有限元方法求解具有漫反射表面环境的渲染方程。他最重要的成果包括：用于计算存在遮挡情形下形状因子（form factor）的半立方体方法（hemicube，1985）；实验评估框架（1986）——最早定量比较真实图像与合成图像的研究之一；将辐射度扩展到非漫反射环境（1986）；光线追踪与辐射度的结合（1987）；渐进求精（progressive refinement，1988）——使交互式渲染成为可能；小波辐射度（wavelet radiosity，1993）——层次化方法的更一般框架；以及「辐射度优化」（radioptimization，1993）——一种基于用户指定目标反解光照参数的逆方法。这些工作最终汇集为 1993 年与 John Wallace 合著的教科书《Radiosity and Realistic Image Synthesis》。

在一个截然不同的研究领域，Cohen 在动作模拟与编辑方面也做出了重大贡献，最突出的包括：带运动学约束的动力学模拟（1987），首次允许动画师组合运动学与动力学规范；面向动画的交互式时空控制（1992），将基于物理的约束与用户自定义约束结合以控制运动；基于时空约束的动作过渡（1996），为人体等多自由度系统实现动作片段之间无缝且合理的过渡；动作插值（1998），一个对参数化动作进行实时插值的系统；以及艺术家导向的逆运动学（2001），允许用户以高帧率摆放关节角色，适用于游戏等实时应用。

此外，在他最具开创性、引用最多的工作中，Cohen 及其同事提出了 Lumigraph（1996）——一种捕获并表示合成或真实世界物体/场景完整外观（涵盖所有视点）的方法。这项工作与 Levoy 和 Hanrahan 的光场渲染（Light Field Rendering）论文同期，两篇论文在 SIGGRAPH '96 论文集中紧挨着发表（并同台报告）。在这项工作的基础上，Cohen 发表了多篇重要后续论文：基于视图的渲染（view-based rendering，1997），利用几何信息从稀疏图像集生成场景的新视图；以及非结构化 Lumigraph 渲染（2001），在单一框架下统一了光场和视点相关纹理映射方法。

在后续工作中，Cohen 显著推进了抠图与合成的技术水平，发表了以下论文：基于各向异性核均值漂移的图像与视频分割（2004）；视频抠图（video cutout，2004），在空间和时间上保持平滑；优化颜色采样（2005），通过分析前景与背景颜色样本的置信度改进了此前的图像抠图方法；以及软剪刀（soft scissors，2007）——首个高质量图像抠图与合成的交互式工具。

近年来，Cohen 将注意力转向计算摄影，发表了大量极具创造力的里程碑式论文：交互式数字照片拼贴（interactive digital photomontage，2004），以各种新颖方式组合照片的不同部分；闪光/无闪光图像对（2004），将开启与关闭闪光拍摄的照片结合，合成优于任一单独图像的更高质量结果；全景视频纹理（panoramic video textures，2005），把在动态场景上平移拍摄的视频转换为高分辨率的连续循环播放视频；基于注视的照片裁剪（2006）；多视点全景（multi-viewpoint panoramas，2006），用于拍摄并渲染非常长的场景；「瞬间相机」（Moment Camera，2007），概述捕获主观瞬间的一般原则；联合双边上采样（joint bilateral upsampling，2007），利用降采样图像实现快速图像增强；十亿像素图像（gigapixel images，2007），用普通相机加专用云台获取超高分辨率图像的手段；deep photo（2008），将随手拍摄的户外照片与现有数字地形数据结合加以增强的系统；图像去模糊（2010），用于消除相机抖动导致的模糊；GradientShop（2010），在单一优化框架下统一了以往的梯度域解决方案；以及 ShadowDraw（2011），一个为物体自由手绘提供引导的系统。

不仅如此，Cohen 的贡献远远超出了他本人的研究。Cohen 是 ACM SIGGRAPH 社区的长期志愿者。他十一次任职 SIGGRAPH 论文委员会，并于 1998 年担任 SIGGRAPH 论文主席。他还于 2013 至 2018 年担任 SIGGRAPH 奖项主席，并在 SIGGRAPH Asia 2018 上发表主题演讲。

Cohen 对艺术与工程的共同兴趣源自早年：他同时拥有艺术（贝洛伊特学院）与土木工程（罗格斯大学）两个本科学位。他于 1985 年在康奈尔大学获得计算机图形学硕士学位，并于 1992 年在犹他大学获得博士学位。Cohen 曾在学术界任职多年，先后执教于康奈尔大学和普林斯顿大学，1994 年加入微软研究院，在那里工作了 21 年。过去 25 年里，他还担任华盛顿大学的兼职教授。在这些岗位上，他指导了许多研究生，他们后来在学术界和业界担任重要职务。他目前领导 Facebook 的计算摄影团队，自 2015 年起在 Facebook 工作。
