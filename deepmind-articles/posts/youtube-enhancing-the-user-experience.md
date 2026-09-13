---
title: "YouTube: Enhancing the user experience"
source: https://deepmind.google/blog/youtube-enhancing-the-user-experience/
site: deepmind
date: 2023-06-16
authors: 
crawled: 2026-09-13
---

It’s all about using our technology and research to help enrich people’s lives. Like YouTube — and its mission to give everyone a voice and show them the world.

Our work with YouTube’s product and engineering teams has helped optimize decision-making processes, increase safety and engagement, and enhance the experience for all kinds of users.

## Making Shorts more searchable

YouTube Shorts — short-form videos less than a minute long — are viewed more than 50 billion times a day.

Covering everything from emerging K-pop stars to local food guides, they’re quick to watch, quick to make — and getting more popular all the time. But because Shorts are created in just a few minutes, they often don’t include the descriptions and titles that make them easy to find through search. So we introduced [Flamingo, our visual language model](https://deepmind.google/blog/tackling-multiple-tasks-with-a-single-visual-language-model/) to help generate descriptions.

Flamingo analyzes the initial video frames, and explains what’s being shown on screen (e.g. “a dog balancing a stack of crackers on its head”). It saves this text as metadata in YouTube, creating clearer content categories and matching user searches to better results.

YouTube is rolling out this technology across Shorts, with auto-generated video descriptions on all new uploads. Now viewers can find and watch more relevant videos, from a more diverse range of global creators.

![An illustration showing how an AI model analyzes YouTube Shorts video frames to detect and label key elements, such as a cat and a ball of yarn, to generate accurate video descriptions for search results.](https://lh3.googleusercontent.com/7QpkLIoR_M-h45-VkFsYeCIpJ502_JkHZ0bnKDTo3LqVP9oO40hAalOvKZbn3YYEFnvf5jjMVo41OE00Ub-vwDwOtr9M0KJ1G7-Ab33COUCBU_mKPSM=w1440)

## Optimizing video compression

Video has exploded in recent years, and with internet traffic only expected to grow in the future — video compression is an increasingly pressing problem.

We worked with YouTube to test the potential of [our AI model, MuZero](https://deepmind.google/research/alphazero-and-muzero/) to improve the VP9 codec, a coding format that helps compress and transmit video over the internet. Then, we applied MuZero to some of YouTube’s live traffic.

At launch, we saw an average 4% bitrate reduction across a diverse set of videos. Bitrate helps determine the computing ability and bandwidth needed to play and store videos — impacting everything from loading time, to resolution, buffering, and data usage.

By improving the VP9 codec on YouTube, we’ve helped reduce internet traffic, data usage, and time needed for loading videos. And through optimizing video compression, millions of people around the world are able to watch more videos while using less data.

![An illustration showing how an AI model analyzes YouTube video frames—such as a soccer player's leg kicking a ball—to label content, detect advertiser-friendly elements like shoes or beverages, and segment the video into chapters.](https://lh3.googleusercontent.com/wNyjvvN6nsiPD643bhl-iXjPBg5htYbRJznFbridnisvKZhF38qeqvFOLkgxGvptkM1EdxtXrq-Cd6UJHkTlAAAZIuhu4uMXOt_FqNK7H3WR-ik3pyU=w1440)

## Protecting brand safety

Since 2018, our YouTube collaboration has helped educate creators on the kind of videos that can earn ad revenue, and make sure the right ads appear in the right place.

We developed a label quality model (LQM) with the YouTube team to label videos more precisely, and in-line with YouTube’s advertiser-friendly guidelines. As well as improving the accuracy of ads running on videos, it’s helping to ensure ads appear alongside content that follows YouTube’s guidelines.

By improving the way videos are identified and classified, we’ve enhanced trust in the platform for viewers, creators and advertisers alike.

![An illustration showing how an AI model analyzes YouTube video frames—such as two people high-fiving—to segment a video timeline into automated chapters using scissor icons to mark the breaks.](https://lh3.googleusercontent.com/xyDPiIVCicitVkZN4dgD2zZ6AqGpu2qD2OfYz39rgpBJtGSoKhi_Hs5ixBpg9FTYuUbJ-fpW7HuSjRdySPCZe_t23tAzrOUgnUYub8R2suQvnas1=w1440)

## Improving AutoChapters

As the way we make and watch video evolves, creators have started adding chapters to their videos. It makes it easier for their audience to find the content they want — but it can be a slow process.

We worked with the YouTube Search team to develop an AI system that suggests chapter segments and titles for YouTube creators, by automatically processing video transcripts, audio and visual features. With AutoChapters, viewers spend less time searching for content, and creators save time creating chapters for their videos.

Since the feature was introduced at [Google I/O in 2022](https://www.youtube.com/watch?v=nP-nMZpLM1A&t=663s), auto-generated chapters have been applied to tens of millions of videos (and counting) across YouTube.

## Evolving technologies and products

We’re continuously looking for ways to improve Alphabet products with our AI research.

Our collaboration with YouTube has already made a great impact on people’s lives — and with more projects underway, we're continuing to improve the experience for users.
