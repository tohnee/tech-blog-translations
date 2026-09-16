---
title: "DeepSeek Debrief: >128 Days Later "
subtitle: "Traffic and User Zombification, GPU Rich Western Neoclouds, Token Economics (Tokenomics) Sets the Competitive Landscape "
date: 2025-07-03
source: https://newsletter.semianalysis.com/p/deepseek-debrief-128-days-later
crawled: 2026-09-15
authors: ["Wei Zhou", "AJ", "Dylan Patel"]
tags: ["LLMs", "Tokenomics", "Inference"]
audience: only_paid
paywalled: true
---

# DeepSeek Debrief: >128 Days Later 

**Traffic and User Zombification, GPU Rich Western Neoclouds, Token Economics (Tokenomics) Sets the Competitive Landscape **

> ⚠️ 付费订阅文章：以下正文为公开可见的预览部分，在付费墙处截断，并非全文。/ Paid post: only the publicly visible preview portion is archived; the body is truncated at the paywall.

SemiAnalysis is hiring an analyst in New York City for Core Research, our world class research product for the finance industry. [Please apply here](https://app.dover.com/apply/SemiAnalysis/6ec0e8df-3da0-469c-9422-0c8d5dd624a7/?rs=76643084)

It’s been a bit over 150 days since the launch of the Chinese LLM DeepSeek R1 shook stock markets and the Western AI world. R1 was the first model to be publicly released that matched OpenAI’s reasoning behavior. However, much of this was overshadowed by the fear that DeepSeek (and China) would commoditize AI models given the [extremely low price](https://api-docs.deepseek.com/quick_start/pricing) of $0.55 input/$2.19 output, undercutting the then SOTA model o1 by 90%+ on output token pricing. Reasoning model prices have dropped significantly since, with OpenAI recently dropping their flagship model price by 80%.

![](https://substack-post-media.s3.amazonaws.com/public/images/9908f718-4a2e-4bcf-bf37-d3a068f0ccbc_1157x623.png)
*Source: SemiAnalysis, Company prices*

 R1 got an update as DeepSeek continued to scale RL after release. This resulted in the model improving in many domains, particularly coding. This continuous development and improvement is a hallmark of the new paradigm we previously covered.

Today we look at DeepSeek’s impact on the AI model race and the state of AI market share.

### A Boom and... Bust?

Consumer app traffic to DeepSeek spiked following release, resulting in a sharp increase in market share. Because Chinese usage is poorly tracked and Western labs are blocked in China, the numbers below understate DeepSeek’s total reach. However the explosive growth has not kept pace with other AI apps and DeepSeek market share has since declined.

![](https://substack-post-media.s3.amazonaws.com/public/images/347d92fd-80bf-460c-9e72-698e245a1606_1230x736.png)
*Source: SemiAnalysis, SensorTower*

For web browser traffic, the data is even more grim with DeepSeek traffic down in absolute terms since release. The other leading AI model providers have all seen impressive growth in users over the same time frame.

![](https://substack-post-media.s3.amazonaws.com/public/images/9946944b-b37c-4bc7-b255-afe3822a29f0_1656x798.png)
*Source: SemiAnalysis, SimilarWeb*

The poor user momentum for DeepSeek-hosted models stands in sharp contrast to third party hosted instances of DeepSeek. Aggregate usage of  R1 and V3 on third party hosts continues to grow rapidly, up nearly 20x since R1 first released.

![](https://substack-post-media.s3.amazonaws.com/public/images/ef102cb8-67dc-4bb1-8ca3-ce6cc59620c1_1099x598.png)
*Source: SemiAnalysis, OpenRouter*

Digging deeper into the data, by splitting out the DeepSeek tokens into just those hosted by the company itself, we can see that DeepSeek’s share of total tokens continues to fall every month.

![](https://substack-post-media.s3.amazonaws.com/public/images/78132000-3afb-4a11-800e-3337f4a82c09_1044x589.png)
*Source: SemiAnalysis, OpenRouter*

So why are users shifting away from DeepSeek’s own web app and API service in favor of other open source providers despite the rising popularity of DeepSeek’s models and the apparently very cheap price?

The answer lies in tokenomics and the myriad of tradeoffs between the KPIs for serving a model. These tradeoffs mean a model’s price per token is an OUTPUT of these KPI decisions which can be tuned based on the model providers’ hardware and model setup.

### Tokenomics Basics

Tokens are the fundamental building blocks of AI models. AI models can learn through reading the internet in token form and produce output in the form of text, audio, image, or action tokens. A token is just a bite-sized chunk of text (like “fan”, “tas”, “tic”) that a large language model counts and processes instead of whole words or letters.

When Jensen talks about datacenters becoming AI factories, the input and output of these factories are tokens. Much like a physical factory, AI factories make money with a P x Q equation: P is the price per token and Q is the quantity of input and output tokens.

Unlike a normal factory, the token price is a variable that model providers can *solve for* based on the other attributes of the model. We list the key KPIs below

1. **Latency or Time-to-First-Token**: how long a model takes to generate a token. This is also known as ‘time to first token’ or approximately how long it takes the model to complete the prefill stage (ie encoding input tokens into the KVCache) and start producing the first token in the decode stage.

2. **Interactivity**: how fast each token is produced, oftentimes measured in tokens per second per user. Some providers also talk about the inverse of interactivity which is the average time between each output token (time per output token or TPOT). Human reading speed is 3-5 words per second but most model providers have settled on output speeds of around 20-60 tokens per second.

3. **Context Window**: how many tokens can be held in the ‘short term memory’ of the model before earlier tokens are evicted and the model ‘forgets’ the older parts of the conversation. Different use cases require different context windows. Large document and code base analysis benefit from larger context windows that allow the model to coherently reason over data.

For any given model, you can manipulate these 3 KPIs to produce effectively any price per token. Therefore it is not always productive or practical to discuss tokens on purely price per million-token ($/Mtok) as this ignores the nature of the workload and requirements of the token user.

### DeepSeek Trade-Offs

Now let’s look at the tokenomics of how DeepSeek serves its R1 model to understand why they have been losing market share on their own model.

![](https://substack-post-media.s3.amazonaws.com/public/images/bb15c40e-0472-44f1-8759-371f04698860_1385x809.png)
*Source: https://openrouter.ai/ accessed in May 2025. Blended $/Mtok calcuated with 3:1 input:output ratio*

Plotting Latency against Price, we can see that DeepSeek’s own service is no longer the cheapest for its latency. In fact, a big reason why DeepSeek is able to price their product so cheaply is because they force users to wait many seconds before the model responds with the first token. This compares to some other providers offering it for the same price but delaying responses by much less time. Token consumers can pay $2-4 for nearly no latency with providers like Parasail or Friendli. Microsoft Azure offers the service for 2.5x more than DeepSeek but with 25s less latency. Since we pulled this data, the situation has become even more grim for DeepSeek as almost all R1 0528 instances are now hosted with [sub-5 second latencies](https://openrouter.ai/deepseek/deepseek-r1-0528).

![](https://substack-post-media.s3.amazonaws.com/public/images/f34f16fa-64b4-4d59-9274-1a7930329bfc_1385x810.png)
*Source: https://openrouter.ai/ accessed in May 2025. Blended $/Mtok calcuated with 3:1 input:output ratio, bubble size represents context window size*

Using the same plot but adding bubble size for the context window, we can see another tradeoff that DeepSeek runs to deliver a very cheap model with limited inference compute resources. They run a 64K context window which is one of the smallest of the major model providers. Smaller context windows limit use cases like coding which require a model to coherently remember a large amount of tokens across a code base to reason across. At the same price you can get >2.5x the context size with providers like Lambda and Nebius in the above chart.

![](https://substack-post-media.s3.amazonaws.com/public/images/ede5f394-a33a-4129-8b82-643800be96b1_907x614.png)
*Source: SemiAnalysis benchmarks*

Digging into hardware, we can see with the above [benchmarking of AMD and NVDA](https://semianalysis.com/2025/05/23/amd-vs-nvidia-inference-benchmark-who-wins-performance-cost-per-million-tokens/) chips on DeepSeek V3 how providers solve for $/Mtok: by batching more users simultaneously on a single GPU or cluster of GPUs, the model provider can INCREASE the total wait experienced by the end user with higher latency and slower interactivity (measured by the x-axis in Median End to End Latency per User) to DECREASE the total cost per token. Higher batch sizes and slower interactivity will reduce the cost per token at the expense of a much worse user experience.

To be clear, this is an active decision by DeepSeek. They are not interested in making money off users or in serving them lots of tokens via a chat app or an API service. The company is singularly focused on reaching AGI and is not interested in end user experience.

Batching at extremely high rates allows them to use the minimal amount of compute possible for inference and external usage. This keeps the maximal amount of compute internal for research and development purposes. [As we have previously discussed](https://semianalysis.com/2025/06/08/scaling-reinforcement-learning-environments-reward-hacking-agents-scaling-data/#rl-is-an-inference-game-but-china-lacks-the-chips), export controls have limited the Chinese ecosystem’s capability in serving models. As such, for DeepSeek, it makes sense to open source. Whatever compute they have is kept internal, while other clouds can host their model so they can win mind share and global adoption. While the export controls have greatly limited China’s capability in inferencing models at scale, we do not believe it has equally hindered their ability to train a useful model as evidenced by recent releasees from [Tencent](https://github.com/Tencent-Hunyuan/Hunyuan-A13B), [Alibaba](https://qwenlm.github.io/blog/qwen3/), [Baidu,](https://ernie.baidu.com/blog/posts/ernie4.5/) and even [Rednote](https://github.com/rednote-hilab/dots.llm1).

### Anthropic is More Like DeepSeek than They’d like to Admit

In the world of AI, the only thing that matters is compute. Like DeepSeek, Anthropic is compute constrained. Anthropic has focused their product development on code and have seen strong adoption among coding applications like Cursor. We think that Cursor usage is the ultimate eval as it represents what users care about most: **cost** and **experience**. Anthropic has ranked first for over a year now, which is decades in the AI industry.

Having noticed the success of token consumers like Cursor, the company launched Claude Code, a coding tool built into the terminal. Claude Code usage has skyrocketed, leaving OpenAI’s codex in the dust.

Google, in response, also released their own tool: Gemini CLI. While it is a similar coding tool to Claude Code, Google uses their compute advantage with TPUs to offer unbelievably large request limits at no cost to users.

![](https://substack-post-media.s3.amazonaws.com/public/images/c41d41f8-18c0-4abd-ab31-894c98a5a0ef_1403x737.png)
*Source: Google*

Claude Code, for all of its wonderful performance and design, is **expensive.** In many ways, the success of Anthropic’s models in code has placed significant stress on the company. **They are squeezed tight on compute.**

This is most evident in Claude 4 Sonnet’s output speed on the API. Since the launch of Claude 4 Sonnet, the speed has decreased by 40% to just above 45 tokens per second. The reason for this is not unlike DeepSeek’s – to manage all the incoming requests with the available compute, they have to batch at higher rates. Coding usage also tends to skew towards larger token count conversations which worsens the crunch on compute resources compared to lower token count casual chat applications. Regardless, comparable models like o3 and Gemini 2.5 Pro run at significantly faster speeds, reflecting the much larger compute resources at OpenAI and Google.

![](https://substack-post-media.s3.amazonaws.com/public/images/b89ab9f0-6877-4763-b4ec-2992efcb6d94_1718x1005.png)
*Source: SemiAnalysis, Artificial Analysis*

Anthropic is focused on acquiring more compute, striking a major deal with Amazon which we have covered before.

Anthropic is getting more than half a million Trainium chips, which they will then be used for both inference and training. This relationship is still a work-in-progress as, despite popular opinion, Claude 4 was not pretrained on AWS Trainium. It was trained on GPUs and TPUs.

Anthropic also turned to their other major investor Google of compute. Anthropic rents significant amounts of compute from GCP, specifically TPUs. Following this success, Google Cloud is expanding their offerings to other AI companies, striking a deal with OpenAI. Unlike previous reporting, Google is only renting GPUs to OpenAI – not TPUs.

### Speed Can be Compensated for

Claude’s speed is indicative of their compute constraints, but generally Anthropic’s UX is better than DeepSeek. First, the speed, despite being low, is faster than DeepSeek’s 25 tokens per second. Second, Anthropic models require significantly less tokens than other models to answer a question. This means that despite the speed, users experience a significantly lower end-to-end response time.

While this can depend on workload, Gemini 2.5 Pro and DeepSeek R1-0528 are more than 3 times as wordy as Claude. Gemini 2.5 Pro, Grok 3, and DeepSeek R1 used significantly more tokens to run Artificial Analysis’ intelligence index, which aggregates several varied benchmark scores together. Indeed, Claude has the lowest amount of total output tokens for leading reasoning models and showed an impressive improvement over Claude 3.7 Sonnet.

This aspect of tokenomics shows that there are many dimensions on which providers are working to improve models. It is not just more intelligence, but more intelligence **per token produced.**

![](https://substack-post-media.s3.amazonaws.com/public/images/ffa08b1a-03d2-4148-9f7e-c3304a806fec_2560x1245.png)
*Source: Artificial Analysis Intelligence Index, SemiAnalysis*

### Rise of the Inference Clouds

With the meteoric rise of Cursor, Windsurf, Replit, Perplexity, and other “GPT Wrappers” or AI token-powered apps hitting mainstream recognition, we are seeing more and more companies emulate Anthropic’s focus on selling tokens as a service, rather than bundled as a monthly subscription like ChatGPT.

Next, we will explore what is next for DeepSeek and address rumors of a delayed R2.
