---
title: "YouTube：提升用户体验"
title_en: "YouTube: Enhancing the user experience"
source: https://deepmind.google/blog/youtube-enhancing-the-user-experience/
site: deepmind
date: 2023-06-16
crawled: 2026-09-13
translated: 2026-09-13
---

# YouTube：提升用户体验

> 原文：[YouTube: Enhancing the user experience](https://deepmind.google/blog/youtube-enhancing-the-user-experience/) · Google DeepMind

这一切的核心是用我们的技术和研究去丰富人们的生活。就像 YouTube——以及它「给每个人发声的机会，向他们展示世界」的使命。

我们与 YouTube 产品和工程团队的合作，帮助优化了决策流程，提高了安全性与用户参与度，并改善了各类用户的体验。

## 让 Shorts 更容易被搜索到

YouTube Shorts——时长不到一分钟的短视频——每天的观看量超过 500 亿次。

从新晋 K-pop 明星到本地美食指南，它们看起来快、做起来也快，而且人气节节攀升。但由于 Shorts 的制作只需几分钟，它们往往缺少能让人通过搜索轻松找到的描述和标题。因此我们引入了 [Flamingo——我们的视觉语言模型](https://deepmind.google/blog/tackling-multiple-tasks-with-a-single-visual-language-model/)来帮助生成描述。

Flamingo 分析视频的开头几帧，解释屏幕上正在呈现的内容（例如「一只狗头顶平衡着一摞饼干」）。它将这段文字作为元数据保存在 YouTube 中，创建更清晰的内容分类，并将用户搜索与更好的结果相匹配。

YouTube 正在 Shorts 上推广这项技术，所有新上传的视频都会自动生成视频描述。现在，观众可以找到并观看更多来自全球更多样化创作者的相关视频。

![一幅插图，展示 AI 模型如何分析 YouTube Shorts 的视频帧，以检测并标注关键元素（例如一只猫和一团毛线），从而为搜索结果生成准确的视频描述。](https://lh3.googleusercontent.com/7QpkLIoR_M-h45-VkFsYeCIpJ502_JkHZ0bnKDTo3LqVP9oO40hAalOvKZbn3YYEFnvf5jjMVo41OE00Ub-vwDwOtr9M0KJ1G7-Ab33COUCBU_mKPSM=w1440)

## 优化视频压缩

近年来视频爆发式增长，而互联网流量预计未来还会继续增长——视频压缩因此成为一个日益紧迫的问题。

我们与 YouTube 合作，测试了[我们的 AI 模型 MuZero](https://deepmind.google/research/alphazero-and-muzero/) 改进 VP9 编解码器的潜力——VP9 是一种帮助在互联网上压缩和传输视频的编码格式。随后，我们将 MuZero 应用于 YouTube 的部分实时流量。

在上线时，我们看到一组多样化的视频平均码率降低了 4%。码率有助于决定播放和存储视频所需的计算能力与带宽——影响着从加载时间到分辨率、缓冲和数据用量的一切。

通过改进 YouTube 上的 VP9 编解码器，我们帮助减少了互联网流量、数据用量以及视频加载所需的时间。通过优化视频压缩，全球数百万人得以用更少的数据观看更多视频。

![一幅插图，展示 AI 模型如何分析 YouTube 视频帧（例如一名足球运动员踢球的腿部动作）来标注内容、检测对广告主友好的元素（如鞋子或饮料），并将视频切分为章节。](https://lh3.googleusercontent.com/wNyjvvN6nsiPD643bhl-iXjPBg5htYbRJznFbridnisvKZhF38qeqvFOLkgxGvptkM1EdxtXrq-Cd6UJHkTlAAAZIuhu4uMXOt_FqNK7H3WR-ik3pyU=w1440)

## 保护品牌安全

自 2018 年以来，我们与 YouTube 的合作帮助创作者了解哪些视频可以赚取广告收入，并确保合适的广告出现在合适的位置。

我们与 YouTube 团队共同开发了标签质量模型（Label Quality Model，LQM），以更精确地标注视频，并与 YouTube 的广告主友好准则保持一致。它不仅提升了视频所投放广告的准确性，还有助于确保广告只出现在符合 YouTube 准则的内容旁边。

通过改进视频的识别与分类方式，我们增强了观众、创作者和广告主对平台的信任。

![一幅插图，展示 AI 模型如何分析 YouTube 视频帧（例如两人击掌）来把视频时间线切分为自动章节，并用剪刀图标标记切分点。](https://lh3.googleusercontent.com/xyDPiIVCicitVkZN4dgD2zZ6AqGpu2qD2OfYz39rgpBJtGSoKhi_Hs5ixBpg9FTYuUbJ-fpW7HuSjRdySPCZe_t23tAzrOUgnUYub8R2suQvnas1=w1440)

## 改进 AutoChapters

随着视频制作与观看方式的演变，创作者开始为视频添加章节。这让观众更容易找到自己想要的内容——但这个过程可能很慢。

我们与 YouTube 搜索团队合作开发了一个 AI 系统，通过自动处理视频文字稿、音频和视觉特征，为 YouTube 创作者建议章节切分和标题。借助 AutoChapters，观众寻找内容的时间更少，创作者为视频制作章节也更省时。

自该功能在 [2022 年 Google I/O 大会](https://www.youtube.com/watch?v=nP-nMZpLM1A&t=663s)上发布以来，自动生成的章节已应用于 YouTube 上数千万个视频（且数量还在增加）。

## 演进中的技术与产品

我们一直在寻找用 AI 研究改进 Alphabet 产品的方法。

我们与 YouTube 的合作已经给人们的生活带来了巨大影响——随着更多项目的推进，我们将继续改善用户的体验。
