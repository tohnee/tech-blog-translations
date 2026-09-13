---
title: "Research acceleration: The view inside OpenAI"
date: 2026-09-06
source: https://openai.com/index/research-acceleration-view-inside-openai/
crawled: 2026-09-13
category: research
---

For AGI to benefit all of humanity, we believe it must be democratically governed. This can only happen through an informed public debate about the capabilities, risks and safeguards of highly capable AI systems. People everywhere need to understand the likely future trajectory of frontier AI, so they can have a meaningful voice in how it develops.

Transparency about specific risks, incidents and safeguards is necessary, but not sufficient. We believe the public also needs to understand how the most capable systems are developing, and how they are driving research progress, inside of frontier labs.

We aim to safely build an automated AI researcher that can work under human supervision to further progress on deep learning and alignment, enabling iterative improvements. According to our measurements, we have now reached the goal, [announced](https://x.com/sama/status/1983584366547829073?lang=en) last fall, of having an automated research intern by September of this year. By “research intern,” we mean a system that can carry out well-defined research tasks under human direction, including tasks that would take a skilled researcher a few days. We are making strong progress toward creating an automated AI researcher by March of 2028.

Over the course of this year, OpenAI researchers’ daily work has changed substantially. Researchers are using coding agents throughout the day (often in concurrent sessions) and total usage is rapidly increasing, outpacing growth among other OpenAI teams. Researchers are contributing code faster and running more experiments. The ways researchers use agents are changing, too: agents are handling increasingly complex tasks, and succeeding at them more often. AI research is a complex process with many potential bottlenecks, so the overall pace of progress likely won’t keep pace with these specific metrics. But on the whole, these findings are consistent with the broader impression many of us have internally that agentic tools are meaningfully accelerating research progress. People still set our research priorities, judge which ideas and results to pursue, and decide whether to scale, pause, or deploy systems.

If it is done responsibly, we believe automated AI research will yield models that directly enhance human welfare and advance OpenAI’s mission. It can bring down the cost of advanced intelligence so that people worldwide can benefit. We are pursuing this work in part because automated research could help us solve alignment and build defenses against increasingly capable AI. An automated AI researcher can also be an automated safety or alignment researcher. More capable, aligned systems could help secure critical infrastructure, defend against dangerous AI agents, and develop new protective measures.

These are reasons to develop useful automated research capabilities, but they do not mean that rapid RSI is necessarily an outcome we should pursue. Whether and how to proceed must depend on our ability to preserve human control and on informed democratic choices about the benefits and risks.

We do not yet know how to safely get all the way to aligned, full RSI. We are working to scale alignment and safety measures alongside capabilities. But we cannot assume that progress in alignment and safety will keep pace, and more capable systems can become harder to monitor. Careful alignment and safety work is at the center of this effort, and it starts with measuring and mitigating the safety problems we see today in agentic coding systems. Whenever we find that proceeding would pose an unacceptable safety risk, we will respond appropriately including by slowing or stopping our development or deployment of systems we find ourselves unable to sufficiently safeguard.

After the recent Hugging Face incident, we [put this commitment into action](https://openai.com/index/pacing-model-development-cyber-capabilities/), pausing reinforcement learning (RL) training on our latest models intended for deployment while we further hardened and red-teamed our research environments and expanded coverage of our monitoring systems. This did not halt all research: some workloads resumed under stronger controls, while others remained paused. We have raised our safety and alignment standards and moved safety work deeper into the model lifecycle, requiring stronger evidence of aligned behavior throughout all of training.

Today we are providing a detailed snapshot of how agentic systems have contributed to our progress toward RSI in recent months. Agentic systems are new and rapidly changing, and our measurement efforts are still preliminary. By sharing these early results and the methods behind them, we aim to inform the public, encourage a norm of public disclosure, and help the field move toward shared standards of measurement.

Ultimately, as we wrote in our [frontier policy blueprint](https://openai.com/index/frontier-safety-blueprint/), we believe that we and other companies should be required to publicly track our progress toward RSI. Even without such a requirement, we plan to continue being transparent about our RSI progress. We will evolve our transparency approach as our measurement techniques and understanding improve, while balancing the need to protect security and proprietary information.

## 1. Coding agents are reshaping daily work for OpenAI researchers

At the start of this year, the median researcher ranked by agent usage at OpenAI was using coding agents only in modest amounts. By mid-August, the median researcher was integrating agents daily into their work, using more than $600 per day of inference at API prices. The 90th percentile user in our research organization now uses more than $7,000 of tokens per day.

Before June 2026, total agent runtime across the research organization was still below that of total human labor. That has since changed. In terms of a standard 8 hour workday, as of mid-August, in total, the research organization uses 3.1 agent-workdays of effort for every workday of human labor.

Another way of looking at this is to understand how many researchers use highly concurrent workflows (e.g., running 4 or more agents simultaneously). As shown below, this number is increasing. These figures include the daily peaks of both agents started directly by the user and subagents created downstream from those the user launched directly.

## 2. Researchers are writing more code and running more experiments

Much of AI research can be seen as a labor-intensive process with the goal of integrating a new improvement to model intelligence or performance into one of our core models. The process depends on many steps, and capabilities advance when all the steps go right together: Researchers have to design new improvements, write evaluations to judge model performance, write infrastructure to test these improvements at scale, catch bugs as well as unsafe or misaligned behavior during training, and integrate winning ideas into a core training run. A failure at any part of the research process can constrain the entire loop.

Writing code and running experiments are two major activities that researchers do as part of their work, and we see evidence that these processes are accelerating.

These data points are relatively easy to measure, but can be hard to interpret. As automation progresses, the tasks which are *least* automatable will take on a larger share of researcher effort and will become the important bottlenecks to future progress. Compute is another gating factor for progress, and may become more important over time as other bottlenecks diminish.

Through 2026, the number of experiments per active experimenter has increased, with August 2026 being an all-time high since tracking began in Jan 2025. This is correlated with increased Codex adoption, though we note that our available compute has also grown significantly since 2025.

## 3. The work researchers use agents for is changing

Both qualitative impressions and internal data indicate that the mix of tasks researchers delegate to coding agents is changing, with delegation of higher level and longer-horizon tasks becoming more common over time.

To get a clearer picture of this trend, we analyzed recent usage in the research organization using a [recently published taxonomy](https://epoch.ai/gradient-updates/toward-an-onet-for-ai-rnd) of the different kinds of work that are part of the AI R&D lifecycle, developed by Epoch AI. This taxonomy, inspired by the longstanding O *NET system for classifying all kinds of work, is specifically tailored to frontier AI R&D, and breaks the process down into six main phases:

1. Decide: what to work on, what to continue, where to allocate
2. Design: research ideas and engineering specs
3. Build: code and datasets
4. Run: training/eval runs, hardware, serving
5. Analyze: experiments, models, deployment, external work
6. Communicate: findings, feedback, status, decisions

Below, we classify coding agent tokens under this taxonomy.

We see that all categories of research activities have increased between January and August 2026. In January, the dominant category was research and infrastructure code. This category has expanded, but we also see notable increases in additional categories, especially technical help and monitoring runs. High-level planning still remains a minimal fraction of agent output tokens.

Anecdotally, colleagues report that coding agents excel at troubleshooting internal research infrastructure, which addresses one meaningful bottleneck to research progress. Multiple teams which previously held office hours to help researchers troubleshoot their experiments have noted declining attendance in 2026, and one has stopped holding sessions entirely, to focus on making other system improvements instead.

Here, we plot the number of top-level posts per day to one of the main internal channels where researchers seek technical support from other teams. To our knowledge, the channel’s decrease in activity has not been offset by queries shifting to another technical support channel run by humans. The decline in traffic aligns with this broader shift.

We can also study whether coding agents are succeeding at the tasks researchers request. Using an agentic classifier, we find that from January to July, success rates generally increased across several difficulty buckets (proxied as the estimated time a human would take to complete the task) on tasks we can find a ground truth outcome for. However, agents still require significant human steering to be successful, especially as task complexity rises. In the last 6 months, over half of successful 4-8 hour tasks involved 1 or more interventions.

Success rates on researcher tasks have increased over time. Graph excludes classifications where the outcome was uncertain and points with <50 sessions or <50 unique users.

Task success and intervention rate from Jan to July, broken out by time horizon. Excludes classifications where the outcome was uncertain.

## 4. Pacing model development

Progress toward more capable systems for safe and beneficial AGI will also depend on the safeguards needed for such work. Our assessment of the needed safeguards may change as we learn more about the risks.

[As we have described,](https://openai.com/index/pacing-model-development-cyber-capabilities/) we have recently updated our standards for monitoring, alignment, and security. Here, we show how recent restrictions have affected one aspect of research activity.

*The majority of Astra compute shown here between July 20 and August 6 was intended to test the implementation of safety and security improvements.

On July 20, following the discovery that agents had compromised our research infrastructure, we temporarily shut down the container service used for training, and then restored it with significant additional restrictions.

This led to a sharp decline in RL training compute while teams reconfigured their workflows to operate within the hardened research environment. The plot above includes the two week pause in reinforcement learning on our latest models intended for deployment. Astra-class RL experiments between July 20 and August 6 include a majority of runs (by GPU allocation) intended to test the implementation of safety and security improvements.

On August 7, preliminary evidence that Astra [may have critical cyber capabilities](https://openai.com/index/responding-next-frontier-critical-cyber-capabilities/) under our [Preparedness Framework](https://cdn.openai.com/pdf/18a02b5d-6b67-4cec-ab64-68cdfbddebcd/preparedness-framework-v2.pdf) led to additional model-specific security restrictions which required the Astra model to be run in higher security research environments. In the following week, Astra-class GPU allocation fell a further 59.2 percent, but allocation to other model classes rose 17.2 percent. That increase offset about 85 percent of the Astra-class decline, leaving total allocation in the analyzed RL workloads largely unchanged. This pattern is consistent with substitution of some training and experimentation to non-Astra models while work involving Astra was restricted, and comports with anecdotal reports of researchers finding other uses for compute that could no longer be leveraged for workloads covered by the new constraints.

This data provides a useful signal for ongoing conversations about training and safety: When new controls are introduced, compute remains valuable and flexible, and will naturally be channeled into alternative uses within the research enterprise. Longer term, discussions about the pace of AI progress should also extend to the question of how compute that is subject to new or proposed controls can best be used.

## 5. The path ahead

Making and understanding progress toward aligned RSI is important for our mission. We will continue to refine our methods, report on our evolving understanding, and work toward an informed public debate and meaningful democratic governance of frontier systems.

## Appendix: Our methods for this post

Agent-powered AI research is still new, and we are still learning how to measure it. Some indicators, such as the amount of code our research teams generate, are relatively easy to gather, but hard to interpret because their relationship to research progress is uncertain. Metrics that focus more directly on research progress—such as how often agents succeed at the tasks researchers give them—could be more useful, but are complex to develop and validate. Furthering the difficulty, the tools and systems researchers rely on are evolving rapidly. Deepening our understanding of research acceleration is a significant focus area across OpenAI.

Across these analyses, unless otherwise noted:

- “Researcher” is a broad term for any member of our research organization, including some who build research infrastructure, manage research projects, or otherwise support the enterprise.
- Metrics of coding agent use cover most, but not all, usage given rapid evolution in the tools and systems researchers rely on.
