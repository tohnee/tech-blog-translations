---
title: "Genie 3：世界模型的新前沿"
title_en: "Genie 3: A new frontier for world models"
source: https://deepmind.google/blog/genie-3-a-new-frontier-for-world-models/
site: deepmind
date: 2025-08-05
crawled: 2026-09-13
translated: 2026-09-13
---

# Genie 3：世界模型的新前沿

> 原文：[Genie 3: A new frontier for world models](https://deepmind.google/blog/genie-3-a-new-frontier-for-world-models/) · Google DeepMind

今天我们宣布推出 Genie 3，一个能够生成前所未有的多样化交互环境的通用世界模型。

给定一个文本提示，Genie 3 可以生成能以每秒 24 帧实时导航的动态世界，在 720p 分辨率下保持数分钟的连贯性。

## 迈向世界模拟

在 Google DeepMind，十多年来我们一直在模拟环境研究领域开疆拓土：从训练智能体[掌握即时战略游戏](https://deepmind.google/discover/blog/alphastar-mastering-the-real-time-strategy-game-starcraft-ii/?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=&utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=)，到为[开放式学习](https://deepmind.google/discover/blog/generally-capable-agents-emerge-from-open-ended-play/?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=)和[机器人技术](https://deepmind.google/discover/blog/from-motor-control-to-embodied-intelligence/?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=)开发模拟环境。这些工作推动了我们世界模型的研发——世界模型是能够运用其对世界的理解来模拟世界某些方面的 AI 系统，使智能体既能预测环境将如何演化，也能预测自己的行动将如何影响环境。

世界模型也是通往 AGI 道路上的关键垫脚石，因为它让在无限丰富的模拟环境课程中训练 AI 智能体成为可能。去年，我们通过 [Genie 1](https://deepmind.google/research/publications/60474/?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=&utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=) 和 [Genie 2](https://deepmind.google/discover/blog/genie-2-a-large-scale-foundation-world-model/?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=&utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=) 推出了第一批基础世界模型，它们能为智能体生成新环境。我们还以 Veo 2 和 Veo 3 模型持续推动视频生成的技术水平，这些模型展现出对直觉物理的深刻理解。

上述每个模型都代表着世界模拟不同能力维度上的进展。Genie 3 是我们第一个支持实时交互的世界模型，同时相比 Genie 2 提升了连贯性与真实感。

![对比表格，详细展示 Genie 3 模型在控制、分辨率、交互延迟等关键领域相较 GameNGen、Genie 2 和 Veo 的进步。](https://lh3.googleusercontent.com/cZoNo9iSxNXrzUDTQUuy84upr6YnjHF1XaysuhkUG9X8LwCzKI3KX4scd0Y779NBBi7ffpkTbTaKqPZ_07Wto_0VaqjF8gmwNAwTSk3eLOtX8PCn=w1440)

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ 您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

Genie 3 可以在更长的时间范围内生成连贯且可交互的世界

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ 您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

- [能力](#capabilities)
- [具身智能体研究](#embodied-agent-research)
- [局限](#limitations)
- [责任](#responsibility)
- [下一步](#next-steps)

## Genie 3 的能力包括：

以下是从 Genie 3 实时交互中录制的画面。

### 建模世界的物理特性

体验水和光照等自然现象，以及复杂的环境交互。

第 1 页，共 5 页

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ 您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

**提示词：** 视频以第一人称视角展示某人在火山地带中部穿越崎岖地形的过程。这是一段从轮式机器人视角拍摄的真实世界视频，该机器人需要穿越一片地形。车辆配备了粗犷的越野轮胎，碾过焦黑的岩石发出咯吱声。摄像机是安装在车辆上的第一人称摄像头，你可以在画面底部看到前轮以及机器人的车身。远处可以看到火山冒出的烟雾和流淌的熔岩。看不到其他生命的迹象。智能体正在努力避开熔岩池和形状各异的岩石。天空是鲜艳的蓝色。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ 您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

**提示词：** 灯光节上的水上摩托

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ 您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

**提示词：** 在佛罗里达州的一条人行道上行走，一侧是双车道公路，另一侧是大海，飓风正在逼近，狂风大作，海浪不断泼溅到公路上。智能体左侧有一道栏杆，把它与大海隔开。公路沿着海岸延伸，前方可以看到一座短桥。海浪一波接一波地越过栏杆泼到路上。棕榈树在风中弯折。大雨倾盆，智能体穿着雨衣。真实世界，第一人称。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ 您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

**提示词：** 快速跟拍的真实世界视频，一只水母在深海黑暗中高速游动，穿梭于布满密集硫化物贻贝、其间有小巧白蟹爬行的峡谷之间。远处模糊的热液喷口从炽热的岩石构造中喷涌出翻滚的、富含矿物的鲜艳蓝色浓烟。非常昏暗的深海光线，颗粒物在浑浊的海水中漂浮。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ 您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

**提示词：** 一名直升机飞行员在海岸悬崖上空有一道小型瀑布的地方小心飞行。

### 模拟自然世界

生成充满生机的生态系统，从动物行为到繁复的植物世界。

第 1 页，共 4 页

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ 您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

**提示词：** 沿着冰川湖岸奔跑，探索森林中的岔路，跨越流淌的山间溪流。置身于美丽的雪峰与松林之间。丰富的野生动物让旅程充满乐趣。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ 您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

**提示词：** 真实世界跟拍镜头，在幽暗的深海中游动，两侧是深海峡谷，密集庞大的水母群游动，生物发光照明。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ 您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

**提示词：** 这是一个设计成日式禅意园林的自然真实世界景观。场景设定在清晨，天空晴朗。柔和温暖的阳光照亮园林，投下修长而轻柔的影子。地面铺满细腻的白沙，被耙出精致的漩涡纹样。园中有一方小小的静水池塘，粉色睡莲漂浮在水面。大小不一、表面光滑的灰色岩石散布在园林各处，有些岩石表面覆着绿色苔藓。关键景观包括一座叠石塔和一盏日式石灯笼。整个区域被背景处高大的竹篱笆围住。视觉风格为照片级写实，沙子、石头和繁茂绿植的纹理细节丰富。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ 您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

**提示词：** 环境是一片自然的真实世界景观，具体是一片茂密繁盛、色彩鲜艳的植物丛。叶片宽大、纹理深邃，呈现出从翡翠绿到青柠绿的一系列绿色色调，其间点缀着黄色和红色的痕迹，暗示着一个丰富健康的生态系统。抽象的斑驳光线从上方洒落，在叶片上形成流动的光影图案，凸显它们精巧的叶脉和多样的表面。氛围宁静而沉浸，让人仿佛置身于一个生机勃勃的自然世界。一些叶片表面可见细小的水珠，反射着环境光。背景是相似植物的柔和虚化，突出了前景元素。空气显得潮湿而静止。

### 建模动画与虚构世界

释放想象力，创造奇幻场景和富有表现力的动画角色。

第 1 页，共 4 页

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ 您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

**提示词：** 鲜艳的 3D 风格，一只可爱的毛茸茸生物在一个奇幻景观中蹦跳着跨越一座绚丽的彩虹桥。这只生物小而紧凑，毛色模仿日出的暖色调——橙色、黄色和粉色无缝交融。它最醒目的特征是一对竖起的大耳朵，形状像德国牧羊犬的耳朵，为其圆润的身形平添了一分俏皮的对比。当它用四条短短的腿在彩虹上奔跑时，毛发仿佛在波动流淌，更添灵动与活力。彩虹桥优雅地拱起在一片奇幻景观之上，或许还点缀着漂浮的岛屿、发光的植物和翻卷的云朵。光线明亮欢快，给这只生物和它的周围投下温暖的光晕。整体印象是喜悦、惊奇与无尽的活力，捕捉了这只生物爱玩的天性和它所栖息世界的魔幻本质。这幅画面唤起一种童趣般的奇思妙想，邀请观者想象这只迷人的生物在它的奇幻国度里将迎来怎样的冒险。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ 您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

**提示词：** 变成一只蜥蜴，折纸风格

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ 您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

**提示词：** 一个奇幻的广角镜头，捕捉到一片沐浴在暮光柔辉中的茂密魔法森林。玩家操控一只大型萤火虫，在参天巨树间飞行，树上鲜艳的枝叶在头顶织成浓密的林冠，滤过阳光，在林间地面上投下斑驳的影子。枝杈间坐落着几座迷人的树屋，每一座都亮着温暖宜人的灯光。树屋大小与设计各异，有的像奇幻城堡，有的像温馨小木屋。发光的窗户和小巧的阳台等细节为它们增添了魅力。一条蜿蜒的小径在灌木下若隐若现，引领观者的视线深入魔法森林。整个场景唤起惊奇、宁静与童年梦境的魔幻感。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ 您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

**提示词：** 一片宁静的爱尔兰风景，起伏的翡翠绿山丘、薄雾笼罩的湖泊和崎岖的山峦突然剧烈颤动——仿佛大地本身正在被撕裂。在超现实的混乱中，整片整片的土地被撕扯开来，以棱角分明、粗野主义风格的形态升上天空，岩石裸露的下侧如同原始破碎的土壤。湖泊被向上拽起，悬浮在空中，湖水倾泻而下形成巨大的瀑布，在下方大地上掀起一场迷雾与雨水交织的末日风暴。镜头拉远，展现出一幅全新的不可能地理——漂浮的山峦、倒转的悬崖、在半空中扭转的河流——仿佛重力本身都在弯折，把曾经宁静的乡野变成一座见证自然剧烈蜕变的粗野主义超现实纪念碑。

### 探索地点与历史场景

超越地理与时间的边界，探索各地与往昔时代。

第 1 页，共 5 页

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ 您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

**提示词：** 阿尔卑斯山的一处真实世界山地环境。景观以陡峭的岩石峭壁和布满松散碎石与碎屑的狭窄峡谷为特色。岩石以灰白色为主，崖面上附着斑驳的绿色植被。峡谷顶端豁然开朗，展现出茂密常绿森林和草甸的景致。整体主题是粗犷的自然之美与极端地形。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ 您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

**提示词：** 乘水上巴士游威尼斯。威尼斯的运河以精益求精的细节重现。水面有着真实的倒影和尾迹。建筑上斑驳的墙皮诉说着数百年的风霜。场景中还有其他贡多拉、水上出租车和驳船。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ 您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

**提示词：** 探索克里特岛的克诺索斯宫殿，如同它辉煌鼎盛时期的样子。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ 您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

**提示词：** 在伊利诺伊州欣斯代尔一个晴朗的日子里四处走走。真实世界。路边停着车。拍摄者站在人行道上，头顶有成群的鸟飞过。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ 您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

**提示词：** 一位骑行爱好者在印度悬崖边缘的一条窄路上骑行，即基拉尔-基什特瓦尔公路。真实世界，第一人称，只看得见握在车把上的双手。

### 推进实时能力的前沿

在 Genie 3 中实现高度的可控性和实时交互，需要重大的技术突破。在每一帧的自回归生成过程中，模型都必须考虑随着时间不断增长的先前生成轨迹。例如，如果用户在一分钟后重新造访某个位置，模型必须回溯一分钟前的相关信息。要实现实时交互，这一计算必须每秒多次进行，以响应不断到来的新用户输入。

### 长时间范围内的环境一致性

AI 生成的世界要让人身临其境，就必须在长时间范围内保持物理上的一致性。然而，以自回归方式生成环境通常比生成一段完整的视频在技术上更难，因为误差会随时间累积。尽管存在挑战，Genie 3 的环境仍能在数分钟内大体保持一致，其视觉记忆可以延伸到一分钟之前。

第 1 页，共 5 页

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ 您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

**提示词：** 第一人称运动相机视角，一名第一人称智能体正用滚筒刷粉刷一栋棕褐色的房子

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ 您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

**提示词：** 一条维多利亚风格的街道上有一栋灰色的房子。灰房子的入口处有一个被魔法火花环绕的传送门。传送门通向一片沙丘遍布的广袤沙漠，从外面可以看到那片沙漠。智能体可以走进传送门，被传送到沙漠中。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ 您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

**提示词：** 这是一个奇幻而妙趣横生的森林环境。光线明亮欢快，暗示着一个晴朗的日子，斑驳的光线透过茂密的、格外巨大的树叶林冠洒落。空气清澈而静止。地面是一层柔软的翠绿苔藓地毯，其间长着异常巨大、色彩鲜艳的红蓝色蘑菇，菌盖上点缀着白色斑点。蜿蜒的泥土小径被踩踏得结实而狭窄，在树皮光滑呈灰色的高大古树间穿行。森林中点缀着迷人的蘑菇形小屋，带有精巧的木门和微小的圆形窗户，每一座的设计和配色都独一无二，从鲜艳的红色到柔和的蓝绿色不等。各种小而友善的森林生灵，例如彩色的蝴蝶和鸣唱的小鸟，在枝叶间飞舞，为生动的氛围增色。众多奇特的巨型花卉以柔和与明亮的色调盛开，散发着柔和的光晕。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ 您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

**提示词：** 一只极其巨大的写实风格大猩猩，身披一件缀有华丽黄铜纽扣的翡翠红艳丽背心，头戴一顶精巧的羽饰双角帽，手里只挥舞着一把古典丝绸阳伞，穿行于一系列极度奢华、爬满苔藓的豪宅之间，宏伟的大理石建筑被蔓延的古玫瑰丛和攀爬的常春藤悄然环抱。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ 您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

**提示词：** 漫步在古代雅典，希腊建筑，大理石

![一段生成的古希腊神庙与遗迹在 0:00、0:20 和 0:40 的三帧视频画面，展示模型的视觉记忆和随时间推移的环境一致性。](https://lh3.googleusercontent.com/mqzat7VkvKPSmjGZJgfgeK10HHg0w_9_UktqhR_YrpPEhme5G2VJKCqFNasBu-wEmOS_vNbpbE0uRGVzFQUkUNJoHVcTDPmJre-jByG6gkGTHbDk=w1440)

*建筑左侧的树木在整个交互过程中保持一致，即使它们不断进入和离开视野。*

Genie 3 的一致性是一种涌现能力。其他方法如 NeRF 和高斯泼溅（Gaussian Splatting）也能提供一致的可导航 3D 环境，但依赖于显式 3D 表示的提供。相比之下，Genie 3 生成的世界要动态和丰富得多，因为它们是基于世界描述和用户的动作逐帧创建的。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ 您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

**提示词：** 第一人称视角无人机视频。在冰岛一条狭窄峡谷中高速飞入并沿峡谷飞行，谷底有一条河，岩石上覆着苔藓，黄金时刻，真实世界

### 可用提示词驱动的世界事件

除了导航输入之外，Genie 3 还支持一种更具表现力的基于文本的交互形式，我们称之为*可提示驱动的世界事件*（promptable world events）。

可提示驱动的世界事件让改变生成的世界成为可能，比如改变天气状况或引入新的物体和角色，在导航控制之上增强体验。

这种能力也拓宽了反事实或"如果……会怎样"场景的范围，供从经验中学习的智能体用来应对意外情况。

**选择一个世界场景。然后挑选一个事件，看 Genie 3 把它创造出来。**

## 为具身智能体研究注入动力

为了检验 Genie 3 生成的世界与未来智能体训练的兼容性，我们为近期版本的 [SIMA 智能体](https://deepmind.google/discover/blog/sima-generalist-ai-agent-for-3d-virtual-environments/?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=)——我们面向 3D 虚拟场景的通用智能体——生成了世界。在每个世界中，我们指示智能体去完成一组不同的目标，它通过向 Genie 3 发送导航动作来达成这些目标。与任何其他环境一样，Genie 3 并不知道智能体的目标，它只是根据智能体的动作来模拟未来。

**选择一个世界场景。然后挑选一个你想让智能体实现的目标，看它如何完成。**

由于 Genie 3 能够保持一致性，现在可以执行更长的动作序列，达成更复杂的目标。我们期待这项技术在我们迈向 AGI、智能体在世界上扮演更重要的角色的过程中发挥关键作用。

第 1 页，共 3 页

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ 您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ 您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ 您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

## 局限

虽然 Genie 3 拓展了世界模型所能达到的边界，但认清其当前的局限同样重要：

- **动作空间有限**。尽管可提示驱动的世界事件允许广泛的环境干预，但这些干预不一定由智能体本身执行。智能体可以直接执行的动作范围目前是受限的。
- **与其他智能体的交互与模拟**。在共享环境中准确建模多个独立智能体之间的复杂交互，仍然是一个进行中的研究挑战。
- **真实世界地点的准确呈现**。Genie 3 目前无法以完美的地理精度模拟真实世界的地点。
- **文字渲染**。清晰易读的文字通常只有在输入的世界描述中提供了文字时才能生成。
- **交互时长有限**。模型目前支持几分钟的连续交互，而非数小时的长时间使用。

## 责任

我们相信，基础性技术从一开始就需要对责任做出深刻承诺。Genie 3 的技术创新，尤其是其开放式与实时能力，为安全与责任带来了新的挑战。为了在最大化效益的同时应对这些独特的风险，我们与我们的负责任开发与创新团队紧密合作。

在 Google DeepMind，我们致力于以一种放大人类创造力、同时限制意外影响的方式来开发我们一流的模型。随着我们继续探索 Genie 的潜在应用，我们将以有限研究预览的形式发布 Genie 3，向一小批学者和创作者提供早期访问。这一方式使我们能够在探索这一新前沿、继续加深对风险及相应缓解措施的理解时，收集关键的反馈和跨学科视角。我们期待与社区进一步合作，以负责任的方式开发这项技术。

## 下一步

我们相信，Genie 3 是世界模型的一个重要时刻，世界模型将开始对 AI 研究和生成式媒体的许多领域产生影响。为此，我们正在探索未来如何让更多测试者使用 Genie 3。

Genie 3 可以为教育和培训创造新的机会，帮助学生学习和专家积累经验。它不仅能提供一个广阔的空间来训练机器人和自主系统等智能体，还能评估智能体的表现、探索它们的弱点。

在每一步，我们都在审视我们工作的影响，安全、负责任地为造福人类而开发它。

**请使用以下 BibTex 引用**

[下载 BibTeX](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/genie-3/genie3worldmodel2025.bib?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=)

## 致谢

Genie 3 的实现离不开以下核心研究与工程贡献：Phil Ball, Jakob Bauer, Frank Belletti, Bethanie Brownfield, Ariel Ephrat, Shlomi Fruchter, Agrim Gupta, Kristian Holsheimer, Aleks Holynski, Jiri Hron, Christos Kaplanis, Marjorie Limont, Matt McGill, Yanko Oliveira, Jack Parker-Holder, Frank Perbet, Guy Scully, Jeremy Shar, Stephen Spencer, Omer Tov, Ruben Villegas, Emma Wang 和 Jessica Yung。

我们感谢 Andrew Audibert, Cip Baetu, Jordi Berbel, David Bridson, Jake Bruce, Gavin Buttimore, Sarah Chakera, Bilva Chandra, Paul Collins, Alex Cullum, Bogdan Damoc, Vibha Dasagi, Maxime Gazeau, Charles Gbadamosi, Shan Han, Woohyun Han, Ed Hirst, Ashyana Kachra, Lucie Kerley, Kristian Kjems, Eva Knoepfel, Vika Koriakin, Jessica Lo, Cong Lu, Zeb Mehring, Alexandre Moufarek, Henna Nandwani, Valeria Oliveira, Fabio Pardo, Jane Park, Andrew Pierson, Ben Poole, Helen Ran, Nilesh Ray, Tim Salimans, Manuel Sanchez, Igor Saprykin, Amy Shen, Sailesh Sidhwani, Duncan Smith, Joe Stanton, Hamish Tomlinson, Dimple Vijaykumar, Luyu Wang, Piers Wingfield, Nat Wong, Keyang Xu, Christopher Yew, Nick Young 和 Vadim Zubov 在开发和打磨本项目关键组件方面无价的合作。

感谢 Tim Rocktäschel, Satinder Singh, Adrian Bolton, Inbar Mosseri, Aäron van den Oord, Douglas Eck, Dumitru Erhan, Raia Hadsell, Zoubin Gharamani, Koray Kavukcuoglu 和 Demis Hassabis（德米斯·哈萨比斯）在整个研究过程中富有洞见的指导与支持。

功能视频由 Suz Chambers, Matthew Carey, Alex Chen, Andrew Rhee, JR Schmidt, Scotch Johnson, Heysu Oh, Kaloyan Kolev, Arden Schager, Sam Lawton, Hana Tanimura, Zach Velasco, Ben Wiley 和 Dev Valladares 制作。其中包括由 Signe Nørly, Eleni Shaw, Andeep Toor, Gregory Shaw 和 Irina Blok 生成的样例。

我们感谢 Frederic Besse、Tim Harley 以及 SIMA 团队的其他成员提供其智能体近期版本的访问权限。

最后，我们感谢 Mohammad Babaeizadeh, Gabe Barth-Maron, Parker Beak, Jenny Brennan, Tim Brooks, Max Cant, Harris Chan, Jeff Clune, Kaspar Daugaard, Dumitru Erhan, Ashley Feden, Simon Green, Nik Hemmings, Michael Huber, Jony Hudson, Dirichi Ike-Njoku, Hernan Moraldo, Bonnie Li, Simon Osindero, Georg Ostrovski, Ryan Poplin, Alex Rizkowsky, Giles Ruscoe, Ana Salazar, Guy Simmons, Jeff Stanway, Metin Toksoz-Exley, Xinchen Yan, Petko Yotov, Mingda Zhang 和 Martin Zlocha 的洞见与支持。
