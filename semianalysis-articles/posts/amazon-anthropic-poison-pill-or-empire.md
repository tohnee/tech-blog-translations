---
title: "Amazon Anthropic: Poison Pill or Empire Strikes Back"
subtitle: "Claude 3, Claude 4, Trainium2, Marvell, Alchip, Bedrock, Google Infrastructure"
date: 2023-10-02
source: https://newsletter.semianalysis.com/p/amazon-anthropic-poison-pill-or-empire
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
---

# Amazon Anthropic: Poison Pill or Empire Strikes Back

**Claude 3, Claude 4, Trainium2, Marvell, Alchip, Bedrock, Google Infrastructure**

> ⚠️ 付费订阅文章：以下正文为公开可见的预览部分，在付费墙处截断，并非全文。/ Paid post: only the publicly visible preview portion is archived; the body is truncated at the paywall.

Amazon and Anthropic signed a significant deal last week, so let’s break it down the alleged deal terms and see what it means for the future of AI infrastructure and services at Amazon as well as Anthropic’s Claude-3 and Claude-4 models.

Amazon is investing $1.25B in the form of a convertible note that would turn into stock when Anthropic raises more money. Amazon has the option for up to $4B down the road. These dollar values are pointless to discuss directly as they are likely cloud credits, and Amazon’s embedded margins could range widely. The actual money out the door for Amazon would be much lower with credits. Some say Amazon is giving dollars, but that doesn't make much sense to us. Anthropic is in the process of raising more cash from other sources currently. Despite the magnitude invested, [Amazon will not have direct control over Anthropic](https://www.anthropic.com/index/anthropic-amazon), or even a seat [on their 5-person LTBT](https://www.anthropic.com/index/the-long-term-benefit-trust).

There are a wide range of emotions and thoughts around the community on the Amazon x Anthropic collaboration, and ours is best encapsulated by this quote from one of our favorite poets.

> If you have one shot or one opportunity to seize everything you ever wanted in one moment, would you capture it or just let it slip.

It may feel very out of place to quote Eminem, but give us a moment and it will all make sense.

![](https://substack-post-media.s3.amazonaws.com/public/images/2d1cfc38-96ff-41a3-9b6e-cb8e18918ce4_1024x1024.jpeg)
*Made with DALL-E 3, isn’t it so cute!*

Amazon’s business has not seen the boom in generative AI this year for multiple reasons. Amazon lacks direct access to enterprise/consumer data and usage to directly roll out AI services themselves. Despite reorganizing Alexa teams + other AI teams across the organization, the internal Titan model development has been going poorly. Their CodeWhisperer model also gets demolished by new startups who have existed less than a year, let alone by the models of major competitors.

Lack of direct access/sales is not a big deal because Amazon’s entire business model revolves around being a Switzerland of sorts. The more worrisome aspect is with their infrastructure. Nitro, Elastic Fabric Adapter, Trainium, and Inferentia2, are **currently** poorly adapted for LLM. Their database moat is not that relevant for AI because storage costs and egress costs are irrelevant compared to the compute costs of AI, meaning multi-cloud strategies are not at any disadvantage and lock-in is low. Lastly, Amazon is getting really poor allocations from Nvidia, well below their current cloud market share. We went over all of this in detail over 6 months ago, [here](https://www.semianalysis.com/p/amazons-cloud-crisis-how-aws-will).

All of these factors have directly translated to Amazon losing market share in cloud and generally in computing. This is worrisome as Amazon is the largest datacenter deployer and operator in the world, with more storage and compute resources than any other firm.

Our data shows that both Microsoft and Google’s 2024 spending plans on AI Infrastructure would have them deploying far more compute than Amazon. This is logical as both have huge ambitions for deploying LLMs into every facet of their products. Amazon, who is at the whim of their customers, has generally had slower adoption plans relative to these tech giants. Furthermore, due to allocation/cost issues, many customers have gone to other services or clouds for more accessible and cheaper AI compute. If the difference in spend and deployment between Microsoft/Google and Amazon continues sustainably, Amazon will have smaller datacenter footprint in just a few years.

The match of Anthropic and Amazon is sort of perfect on the surface. Amazon needs frontier model capabilities, and this is how the empire strikes back. Anthropic, with Claude 2, has the 2nd best publicly accessible model after OpenAI’s GPT-4. Amazon gets direct access to Claude 2 for serving customers and can also offer fine tuning services. Future models will also be available to Amazon. Amazon also stated they will be leveraging these models for drug discovery and many other aspects of healthcare, [further strengthening their Amazon HealthOmics platform](https://www.semianalysis.com/i/137441303/aws-health-omics-as-a-template-for-nvidia).

On Anthropic’s side of the fence, while on the surface, it seems they get to stick to their core beliefs of AI safety without signing control away to Amazon, in reality, the deal represents Anthropic effectively betting it all. We hear there are pretty meaty IP transfers with regards to giving away certain current and upcoming models to Amazon. Allegedly Amazon can build pretty much anything they’d like to leveraging Anthropic’s technology.

Furthermore, we hear the deal has certain clawback provisions, meaning Anthropic has to make Amazon their investment back within a couple of years. These are just rumors, but Amazon’s products that leverage Anthropic’s IP would have some kickback that helps satisfy this. We have no idea what that kickback percentage could be, but hypothetically, it’s easy to imagine that for every $1B of revenue from Anthropic based models in AWS, served by Amazon to their customers, maybe only $100M is attributed back to Anthropic paying Amazon back.

On the surface is similar to the Microsoft OpenAI deal structure, but there are some major differences. For one, OpenAI and Microsoft terms are less opaque with [Microsoft receiving 75% of OpenAI’s profits until they are paid back on their investment, then 49% of the firms equity with profit caps](https://www.cnbc.com/2023/01/10/microsoft-to-invest-10-billion-in-chatgpt-creator-openai-report-says.html). OpenAI also seems to have more ability to control their own destiny due to the fact that they have direct access to enterprises and consumers via the app, website, and hugely successful APIs.

In the case of Anthropic, we struggle to see how this same control over how most deploy their Claude models can be established. Even though Anthropic offers a direct site and API, Amazon will be able deploying their models likely at the same time as Anthropic. Even in the case of OpenAI, DALL-E 3 and GPT-4 vision were both accessible through Microsoft’s Bing before they were for most ChatGPT paid subscribers.

Despite this front-running, because OpenAI has already built direct customer access, their customer retention for direct usage is very high and still growing. Likewise, Amazon will be deploying foundation model and fine-tuning APIs directly just like Microsoft is, but Anthropic may not have that same customer retention/share. This means Anthropic could be ceding a lot more economics than first meets the eye.

While this may sound like a poison pill on the surface, ultimately, the deal greatly accelerates Anthropic’s ability to build foundation models and potentially keep up with Google and OpenAI in the race to “AGI”. Anthropic’s biggest difficulty going forward was acquiring enough compute resources to not fall behind OpenAI and Google Deepmind. Anthropic clearly will do anything to not let their opportunity at greatness slip.

> If you have one shot or one opportunity to seize everything you ever wanted in one moment, would you capture it or just let it slip.

Google’s obvious advantage is that they are the only firm who wholly owns and controls their AI research organization. Furthermore, they are the [only firm with great in-house chips](https://www.semianalysis.com/p/google-ai-infrastructure-supremacy). Both Microsoft and Amazon are arms lengths partners with OpenAI/Anthropic. Furthermore, their upcoming in-house chips, Athena and Tranium2 still lag behind significantly.

Google will have multiple very large clusters across their infrastructure for training and by far the lowest cost per inference, but this won’t automatically grant them the keys to the kingdom. [If the battle is just access to compute resources, Google would crush both OpenAI and Anthropic](https://www.semianalysis.com/p/google-gemini-eats-the-world-gemini).

Being “GPU-rich” alone does not mean the battle is over. [Google will have multiple different clusters larger than their competitors](https://www.semianalysis.com/p/broadcoms-google-tpu-revenue-explosion), so they can afford to make mistakes with pretraining and trying more differing architectures. What OpenAI and Anthropic lack in compute, they have to make up in research efficiency, focus, and execution.

This necessity and the smaller teams will have to drive innovation. Even when compared to OpenAI, Anthropic is significantly behind in raw total compute resources, yet their ambitions are similar. We are hopeful to see if Anthropic can keep up. Right now Claude-2 offers a sweet spot on model quality vs cost, being much cheaper than GPT-4, but with 4-turbo being released in the short term, Anthropic will have to have another ace up their sleeve.

Below we will briefly touch on the following topics:

Google’s investment in Anthropic, speculating a bit about Anthropic’s Claude-3 and Claude-4 infrastructure with some bounding boxes around the potential size of these models, and the sizing of Amazon’s Trainium1/Inferentia2 + Tranium2/Inferentia3 deployments

[Get 20% off a group subscription](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)
