---
title: "Amazon Web Services Infrastructure Inefficiencies Cause Cuts To Twitch Driving Creators To Google’s YouTube"
subtitle: "Hyperscalers have different hardware software advantages"
date: 2022-10-05
source: https://newsletter.semianalysis.com/p/amazon-web-services-infrastructure
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: everyone
paywalled: false
---

# Amazon Web Services Infrastructure Inefficiencies Cause Cuts To Twitch Driving Creators To Google’s YouTube

**Hyperscalers have different hardware software advantages**

Amazon made major waves with recent announcements on their Twitch.tv video streaming platform by slashing payouts to creators from [70/30 revenue sharing to 50/50](https://blog.twitch.tv/en/2022/09/21/a-letter-from-twitch-president-dan-clancy-on-subscription-revenue-shares/). These cuts primarily target large content creators who are making more than $100,000 a year off the platform. In addition to capturing more of the revenue from their creators, Twitch is also [capping the stream quality of streams in certain geographies such as South Korea](https://blog.twitch.tv/ko-kr/2022/09/28/%ED%95%9C%EA%B5%AD-twitch-%EC%97%85%EB%8D%B0%EC%9D%B4%ED%8A%B8/), which has some of the best and lowest cost network infrastructure in the world. Shockingly, in both of these announcements, Twitch cited infrastructure costs as the limiting factor. Meanwhile, Google’s YouTube not only pays their creators a 70/30 revenue share, but they also deliver higher quality and bitrates up to 4k.

> Delivering high definition, low latency, always available live video to nearly every corner of the world is expensive. To bring it back around more directly to this blog’s topic: we can’t run this service unless you make money. That’s not a drawback; it’s by design.
>
> Dan Clancy, President of Twitch

Twitch’s most popular streamers have started [quite the backlash due to this move with multiple stating they will move to YouTube as a result](https://www.theverge.com/2022/9/26/23369070/twitch-revenue-split-70-30-streamers-reaction-amazon). There is a bit of a standoff here between these major content creators and Twitch. We won’t get into that as we aren’t media analysts, but we do want to talk a bit about why Amazon was forced into these drastic actions. Additionally, we want to explain why YouTube is able to profitably offer a higher 70/30 revenue split while also offering 4x the bitrate (amount of data per video stream).

To start off with, let’s discuss Amazon’s general video streaming infrastructure model. Streamers upload video to Twitch where the video gets transcoded into a variety of formats to be played across a wide range of devices that users consume Twitch content on.

Amazon dynamically choses transcode options based on its infrastructure capacity and viewership of the stream along with other factors. The largest streamers will have their stream transcoded to many varying quality options while low view count streamers often have a single quality preset option for viewers. While there is no public indication of how Amazon operates its content delivery network, we have heard they are using a variety of CPUs, GPUs, and FPGAs for their transcoding and AI inference for terms of service checks. They deliver these videos live and offer on-demand video for 7 to 60 days depending on the creator. After that time elapses, the video is deleted from the platform.

> Using the published rates from Amazon Web Services’ Interactive Video Service (IVS) — which is essentially Twitch video — live video costs for a 100 CCU streamer who streams 200 hours a month are more than $1000 per month. We don’t typically talk about this because, frankly, you shouldn’t have to think about it. We’d rather you focus on doing what you do best. But to fully answer the question of “why not 70/30,” ignoring the high cost of delivering the Twitch service would have meant giving you an incomplete answer.
>
> Dan Clancy, President of Twitch

Google and YouTube on the other hand have very different infrastructure and product offering model. They transcode all videos that they receive into many formats no matter what size the creator is. These transcoded videos have a natural language model auto-generate captions for every video, and they are never deleted. This on the surface sounds much more costly than what Amazon and Twitch are doing, but YouTube is both larger and more profitable than Amazon’s Twitch platform in the general video content delivery market. YouTube offers these services for its streaming business as well as standard on-demand videos.

We believe Google is able to keep costs down due to a superior service infrastructure. First off, Google has a [custom-designed transcoding chip](https://semianalysis.substack.com/p/google-new-custom-silicon-replaces). As we reported in the past, they are on the second generation of this chip, and [it allows them to reduce CPU footprint by the millions](https://semianalysis.substack.com/p/google-new-custom-silicon-replaces)! Due to having a custom ASIC that can transcode video at 40x lower cost than a CPU and 20x lower cost than a GPU, YouTube can always hit the most optimal point on the video quality versus bitrate (file size) curve while delivering a consistently better viewer experience. Twitch often compromises with respect to quality and viewer experience because they must rely on lower computationally intensive transcoding for their streams because of their video encoding infrastructure limitations. Google’s terms of service and captioning will is done on [2nd generation and beyond custom transcoding chips](https://semianalysis.substack.com/p/google-new-custom-silicon-replaces).

Given a certain bitrate, YouTube videos almost always outperform Twitch on video quality. This in turn means users will often request the YouTube content delivery network for a lower bitrate stream versus Twitch because it meets their subjective quality requirements. YouTube is able to save on north-south bandwidth out of the datacenter because they have more specialized ASIC compute. [As a reminder, north-south bandwidth is one of the highest expenses in a datacenter.](https://www.fabricatedknowledge.com/p/r2-what-it-means-to-be-1-less-than) Google’s YouTube being more efficient also makes their infrastructure greener and more environmentally sustainable versus Amazon’s Twitch.

Another aspect of the profitability difference between YouTube and Twitch, which likely factors into the feature differences and revenue share split, 70/30 vs. 50/50,  also boils down to the quality of YouTube’s ad serving and recommendation engines. Google’s deep learning recommendation systems (DLRS) trained on their in-house TPU AI silicon, are amongst the best in the industry. While Amazon has their own DLRS models, they don’t seem to achieve as accurate targeting as Google’s which impacts advertisement rates. In our view, this boils down more to AI superiority than silicon, but it is important to note how much more mature Google’s TPU is versus Amazon’s Trainium and Inferentia AI silicon. We believe Amazon is working on their own video transcoding ASIC, but Amazon could also turn [to NetInt, a 3rd party provider.](https://semianalysis.substack.com/p/meet-netint-the-startup-selling-to)

For the hyperscalers, hardware is an extension of their software. While Amazon is most definitely much more mature on their cloud service provider offering through AWS and custom silicon such as [in-house Nitro DPUs](https://semianalysis.substack.com/p/amazon-graviton-3-uses-chiplets-and) and [Graviton CPUs](https://semianalysis.substack.com/p/amazon-graviton-3-uses-chiplets-and), Google is clearly more advanced in AI and video content delivery networks. These different companies have grown out of different roots and so their hardware, software co-optimization will differ significantly. It’s interesting to see Google try to build out this suite of capabilities to compete better for their cloud offerings while Amazon is trying to catch up in video content delivery networks and search/recommendation AI’s for ad networks.

If you like what you’re reading, please share it!

[Share](https://newsletter.semianalysis.com/p/amazon-web-services-infrastructure?utm_source=substack&utm_medium=email&utm_content=share&action=share)

[Get 20% off a group subscription](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)
