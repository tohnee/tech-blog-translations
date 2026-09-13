---
title: "How evals drive the next chapter in AI for businesses"
date: 2025-11-19
source: https://openai.com/index/evals-drive-next-chapter-of-ai/
crawled: 2026-09-13
category: research
---

Over [one million businesses](https://openai.com/index/1-million-businesses-putting-ai-to-work/) around the world are leveraging AI to drive greater efficiency and value creation. But some organizations have struggled to get the results they are expecting. What is causing the gap?

At OpenAI we are leveraging AI internally to achieve our ambitious goals. One key set of tools we use are **evals**, methods to measure and improve the ability of an AI system to meet expectations.

Similar to product requirement documents, evals make fuzzy goals and abstract ideas specific and explicit. Using evals strategically can make a customer-facing product or internal tool more reliable at scale, decrease high-severity errors, protect against downside risk, and give an organization a measurable path to higher ROI.

At OpenAI, our models are our products, so our researchers use rigorous [**frontier evals**](https://evals.openai.com/) 1 to measure how well the models perform in different domains. While frontier evals help us ship better models faster, they cannot reveal all the nuances required to ensure the model will perform on a specific workflow in a specific business setting. That is why internal teams have also created dozens of **contextual evals** designed to assess performance within a specific product or internal workflow. It is also why business leaders should learn how to create contextual evals specific to their organization’s needs and operating environment.

This is a primer for business leaders looking to apply evals in their organizations. Contextual evals, each crafted for a specific organization’s workflow or product, are an active area of development and definitive processes have yet to emerge. As a result, this article provides a broad framework that we have seen work across many situations. We expect this field to evolve and for more frameworks to emerge that address specific business contexts and goals. For example, an excellent eval for a cutting-edge, AI-enabled consumer product might require a different process than an eval for an internal automation based around a standard operating procedure. We believe that the framework presented below will serve as a collection of best practices in both cases, and will be a useful guide as you build evals tailored to your organization’s needs.

## How evals work: Specify → Measure → Improve

### 1. Specify: Define what “great” means

Start with a small, empowered team that can write down the purpose of your AI system in plain terms, for example: “Convert qualified inbound emails into scheduled demos while staying on brand.”

This team should be a mix of individuals with technical and domain expertise (in the given example, you’d want sales experts on the team). They should be able to state the most important outcomes to measure, outline the workflow end-to-end, and identify each important decision point your AI system will encounter. For every step in that workflow, the team should define what success looks like and what to avoid. This process will create a mapping of dozens of example inputs (e.g. inbound emails) to the outputs they want the system to produce. The resulting **golden set** of examples should be a living, authoritative reference of your most skilled experts’ judgement and taste for what “great” looks like.

Do not get overwhelmed with a cold start or try to solve it all at once. The process is iterative and messy. Early prototyping can help immensely. Reviewing 50 to 100 outputs from an early version of the system will uncover how and when your system is failing. This “error analysis” will result in a taxonomy of different errors (and their frequencies) to track as your system improves.

This process is not purely technical—it’s cross-functional and centered on defining business goals and desired processes. Technical teams should not be asked in isolation to judge what best serves customers or the needs of other teams like product, sales, or HR. Consequently, domain experts, technical leads, and other key stakeholders should share ownership.

### 2. Measure: Test against real-world conditions

The next step is to measure. The goal of measurement is to reliably surface concrete examples of how and when the system is failing. To do that, create a dedicated test environment that closely mirrors real-world conditions—not just a demo or prompt playground. Evaluate performance against your golden set and error analysis under the same pressures and edge cases your system will actually face.

Rubrics can help bring concreteness to judging outputs from your system, but it is possible to over-emphasize superficial items at the expense of your overall goals. Further, some qualities are difficult or impossible to measure. In some cases, traditional business metrics will be important. In others, you’ll need to invent new metrics. Keep your subject matter experts in the loop throughout, and tightly align the process with your core objectives.

To actually test the system, use examples drawn from real-world situations whenever possible, and include or invent edge cases that are rare but costly if mishandled.

Some evals can be scaled through the use of an **LLM grader**, an AI model that grades outputs the same way an expert would; yet, it is still important to keep a human in the loop. Your domain expert needs to regularly audit LLM graders for accuracy and should also directly review logs of your system’s behavior.

Evals can help you decide when a system is ready to launch, but they do not stop at launch. You should continuously measure the quality of your system's real outputs generated from real inputs. As with any product, signals from your end-users (whether external or internal) are especially important and should be built into your eval.

### 3. Improve: Learn from errors

The last step is to set up a process for continuous improvement. Addressing problems uncovered by your eval can take on many forms: refining prompts, adjusting data access, updating the eval itself to better reflect your goals, and so forth. As you uncover new types of errors, add them to your error analysis and address them. Each iteration compounds upon the last: new criteria and clearer expectations of system behavior help reveal new edge cases and subtle, stubborn issues to correct.

To support this iteration, build a data flywheel. Log inputs, outputs, and outcomes; sample those logs on a schedule and automatically route ambiguous or costly cases to expert review. Add these expert judgements to your eval and error analysis, then use them to update prompts, tools, or models. Through this loop you will more clearly define your expectations for the system, align it tighter to those expectations, and identify additional relevant outputs and outcomes to track. Deploying this process at scale yields a large, differentiated, context-specific dataset that is hard to copy—a valuable asset your organization can leverage as you build the best product or process in your market.

While evals create a systematic way to improve your AI system, new failure modes can arise. In practice, as models, data, and business goals evolve, evals must also be continuously maintained, expanded, and stress-tested.

For external-facing deployments, evals do not replace more traditional A/B tests and product experimentation. They are complements to traditional experimentation that can help guide each other and provide visibility into how changes you make impact real-world performance.

## What evals mean for business leaders

Every major technology shift reshapes operational excellence and competitive advantage. Frameworks like OKRs and KPIs have helped organizations orient themselves around “measuring what matters” for their business in the age of big data analytics. Evals are the natural extension of measurement for the age of AI.

Working with probabilistic systems requires new kinds of measurement and deeper consideration of trade-offs. Leaders must decide when precision is essential, when they can be more flexible, and how to balance velocity and reliability.

Evals are difficult to implement for the same reason that building great products is difficult; they require rigor, vision, and taste. If done well, evals become unique differentiators. **In a world where information is freely available across the world and expertise is democratized, your advantage hinges on how well your systems can execute inside your context.** Robust evals create compounding advantages and institutional know-how as your systems improve.

At their core, evals are about a deep understanding of business context and objectives. If you cannot define what “great” means for your use case, you’re unlikely to achieve it. In this sense, evals highlight a key lesson of the AI era: management skills are AI skills. Clear goals, direct feedback, prudent judgment, and a clear understanding of your value proposition, strategy, and processes still matter, perhaps even more than ever.

As more best practices and frameworks emerge, we will be sharing them. In the meantime, we encourage you to experiment with evals and discover what processes work best for your needs. To get started, identify the problem to be solved and your domain expert, round up your small team, and, if you are building on our API, explore our [Platform Docs](https://platform.openai.com/docs/guides/evals?api-mode=responses).

Don’t hope for “great.” Specify it, measure it, and improve toward it.
