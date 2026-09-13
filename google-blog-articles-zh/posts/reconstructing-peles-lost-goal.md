---
title: "复原贝利「失传」的进球"
title_en: "Reconstructing Pelé’s “lost” goal"
source: https://blog.google/innovation-and-ai/models-and-research/google-deepmind/reconstructing-peles-lost-goal/
site: google-blog
date: 2026-07-14
crawled: 2026-09-13
translated: 2026-09-13
---

# 复原贝利「失传」的进球

> 原文：[Reconstructing Pelé’s “lost” goal](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/reconstructing-peles-lost-goal/) · Google

1959 年 8 月 2 日，球王贝利（Pelé）踢进了他职业生涯中最漂亮的一粒进球：连续三次「挑球过人」（sombrero），先后越过防守队员和门将，皮球全程没有落地。但这一瞬间从未被影像记录下来。

六十多年来，这粒传奇的「Javari 街进球」（Gol da Rua Javari）只存在于亲历球迷的记忆中。如今，我们与贝利的家人、历史学者、体育记者和足球名宿合作，运用 Google DeepMind 技术复原了这段足球历史。这项作品是在 NR Sports 领导下、与负责保存、保护和拓展贝利遗产的平台 Pelé Brand 全面合作完成的。

「Javari 街进球」的复原成果以一部迷你纪录片的形式呈现，片中收录了对历史学者、记者、贝利的家人、目击者和足球名宿的采访——正是与他们一起，我们讲述了足球史上这个不可思议瞬间的故事。

「他若看到这一切发生，一定会无比自豪。他总说，这粒进球没能被记录下来实在太遗憾了。所以，能借助这些技术重历那个瞬间，实在令人惊叹。」——Flávia Kurtz，贝利之女

![贝利与其女儿自豪地望着他的黑白合成照片](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Pele_Keyword_047.width-1200.format-webp.webp)

## 拼合一段传奇

为了把历史还原得分毫不差，巴西历史学者 Anita Lucchesi 和她的团队收集了近 2,000 份历史资料——从建筑图纸到家庭相册。他们采访了目击者、记者和 Mooca 社区，借助球场的缩比模型、档案照片和示意图，帮助亲见那粒进球的人们凭记忆将其重新拼合起来。

为精准复原这粒进球，团队收集了超过 3,600 张历史图片。

![那粒著名进球的黑白照片](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Pele_Keyword_002.width-100.format-webp.webp)

1959 年 8 月 2 日拍摄的「Javari 街进球」历史照片。

![一位历史学者对着镜头讲话的彩色照片](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Pele_Keyword_003.width-100.format-webp.webp)

Anita Lucchesi，UERJ & Arka 历史学者

![关于那粒著名进球的旧历史资料](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Pele_Keyword_004.width-100.format-webp.webp)

档案碎片：报纸、地图、图纸与家庭相册

![人们在巴西踢足球的黑白照片](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Pele_Keyword_005.width-100.format-webp.webp)

圣保罗 Mooca 街区「Javari 街球场」（Estádio da Rua Javari）的历史照片。

![巴西足球队队员的黑白照片](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Pele_Keyword_007.width-100.format-webp.webp)

Juventus 队队员与工作人员在 Javari 街球场。

![手指着一本书中照片的手](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Pele_Keyword_008.width-100.format-webp.webp)

1959 年 Juventus 队合影

![写着「Gooool」的旧报纸剪报和进球示意图](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Pele_Keyword_010.width-100.format-webp.webp)

比赛的报纸报道与进球示意图

## 从球场到像素

复原这粒进球需要将实景拍摄与我们最先进的 AI 模型相结合：Veo、Gemini Omni 和 Nano Banana Pro。

首先，我们的摄制组在 Javari 街球场的草皮上实景拍摄，使用沉重的皮质足球和符合当年样式的球衣。这一实体基础随后被输入我们的模型，开启数字化转换。我们聚焦于三项核心技术实验：

- **角色替换：** 将贝利的形象和他经典的 10 号球衣精准映射到现代特技替身球员身上。
- **环境重塑：** 将现代球场转换为与那一天的阴天天气和建筑样式相符的样子。
- **氛围生成：** 呈现当时在球场观赛的球迷和在家中收听广播直播的观众各自如何体验那个时刻。

![原版球鞋与数字化复刻的并排对比图](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Pele_Keyword_034.width-100.format-webp.webp)

贝利 1959 年的原版球鞋。档案照片与实物藏品是所有 AI 生成场景的基础，确保全片的历史准确性。

![原版照片与数字化复刻的并排对比图](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Pele_Keyword_028.width-100.format-webp.webp)

Raphael Herrera，1959 年 Javari 球场摄影师

![两位老人与他们年轻时的数字化复刻形象的并排对比图](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Pele_Keyword_030.width-100.format-webp.webp)

Angelo Agarelli 与 Vicente Romano Netto，Juventus 球迷、Javari 进球的目击者。

![人群照片与数字化复刻的并排对比图](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Pele_Keyword_033.width-100.format-webp.webp)

Juventus 比赛期间座无虚席的 Javari 球场

## 在照片级写实与表演控制之间取得平衡

虽然生成式模型擅长照片级写实，但像贝利这样的传奇球员极限的身体动作编排带来了独特挑战。为解决这一问题，我们使用了 Performance Control——一种基于 Veo 3 的方法，从现代特技球员身上提取精确的 3D 几何与运动数据来驱动视频生成。结合使用 Nano Banana Pro 和 Gemini Omni 的互补工作流，我们生成了最终视频，将球场建筑、场地状况、贝利的形象与动态比赛无缝融为一体。

从原始实景视频（左上）开始，我们把场景拆分成彼此独立、可分别编辑的图层：捕捉运动员精确的 3D 动作（右上），把他们从景物中分离出来（左下），并生成不含他们的干净背景（右下）。这让我们可以独立修改球员与环境。

![笔记本电脑上显示动画不同阶段的图像](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Pele_Keyword_035_1.width-100.format-webp.webp)

为简化剪辑、特效（VFX）与视频生成流程，Gemini Omni 与 Veo 将演员素材分离、提取背景，并生成表示球员运动的 3D 蓝色网格。

Performance Control 可从输入视频创建可编辑的 3D 蓝色网格渲染，并能借助参考图像进行修改。

## 打造混合后期制作管线

为了完成最终的精修，我们构建了一条将 AI 生成与传统视觉特效（VFX）相结合的混合管线。借助定制的内部工具，我们用 Gemini Omni 和 Nano Banana Pro 进一步打磨 AI 生成的镜头，并依据档案影像确保每个细节准确无误。随后工作流转入传统 VFX，完成足球合成、胶片颗粒融合和严格的色彩平衡等任务。为让生成画面尽可能贴近那个年代，我们把数字输出经胶片记录机（filmout）转印，捕捉 1950 年代电影独特的质感与观感。

## 让不可见变为可见

任何东西都无法替代亲临现场的球迷的体验，但我们希望这个项目能为足球史上一个标志性瞬间注入新的生命。

这粒进球的复原作品如今正在桑托斯的贝利博物馆（Pelé Museum）骄傲展出。

贝利博物馆（Museu Pelé），巴西圣保罗州桑托斯

![博物馆里身穿贝利球衣的孩子的照片](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Pele_Keyword_038.width-1200.format-webp.webp)
