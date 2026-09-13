---
title: "GPT 5.6 Configurations and Defaults"
source: https://sebastianraschka.com/blog/2026/gpt-5-6-configurations.html
crawled: 2026-09-06
---

# GPT 5.6 Configurations and Defaults

Yes, there are probably too many options to choose from in the GPT 5.6 release.

In the context of reasoning models, though, I find it interesting how these choices map onto training-time and [inference-time scaling](https://sebastianraschka.com/glossary/#inference-time-scaling "Inference-Time Scaling"). If we loosely map the options onto the classic o1 plots, Sol, Terra, and Luna stand in for three model sizes and training budgets along the training-compute axis. The effort settings then sit on the inference-time-compute axis.

![Annotated comparison mapping GPT 5.6 model choices to training-compute scaling and effort levels to inference-time scaling](https://sebastianraschka.com/images/blog/2026/gpt-5-6-configurations/hero.webp)

Figure 1. A loose mapping from OpenAI's classic [o1 scaling plots](https://openai.com/index/learning-to-reason-with-llms/) to the GPT 5.6 choices. The three model options represent different model sizes and training budgets, while the effort setting represents inference-time compute.

The full list has three model choices and six reasoning-effort levels (Light, Medium, High, Extra High, Max, and Ultra). Once Work versus Codex and Standard versus Fast are included, the full configuration matrix becomes

`Work/Codex × Sol/Terra/Luna × Light/Medium/High/Extra High/Max/Ultra × Standard/Fast`

That gives us `2 × 3 × 6 × 2 = 72` possible configurations.

So, what is a good default now? Luna with High effort? Sol with Light effort? Terra with Medium effort?

Sure, a performance-versus-cost chart can help identify the good bang-for-the-buck combinations. For instance, Luna with Extra High effort may be better and cheaper than Sol with Medium effort.

![Artificial Analysis Coding Agent Index scores plotted against API cost for GPT 5.6 and comparison models](https://sebastianraschka.com/images/blog/2026/gpt-5-6-configurations/coding-agent-index-cost.webp)

Figure 2. Artificial Analysis Coding Agent Index v1.1 scores plotted against API cost across GPT 5.6 and several comparison models. Figure based on [OpenAI's GPT 5.6 release post on X](https://x.com/OpenAI/status/2075271425548795909).

But yeah, 72 possible configurations leave us with a lot of choices 🤯.
