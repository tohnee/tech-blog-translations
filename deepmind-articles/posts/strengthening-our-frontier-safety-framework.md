---
title: "Strengthening our Frontier Safety Framework"
source: https://deepmind.google/blog/strengthening-our-frontier-safety-framework/
site: deepmind
date: 2025-09-22
authors: Four Flynn, Helen King, Anca Dragan
crawled: 2026-09-13
---

We’re expanding our risk domains and refining our risk assessment process.

**Updated April 17, 2026**

AI breakthroughs are transforming our everyday lives, from advancing mathematics, biology and astronomy to realizing the potential of personalized education. As we build increasingly powerful AI models, we’re committed to responsibly developing our technologies and taking an evidence-based approach to staying ahead of emerging risks.

Today, we’re publishing the third iteration of our Frontier Safety Framework (FSF) — our most comprehensive approach yet to identifying and mitigating severe risks from advanced AI models.

This update builds upon our ongoing collaborations with experts across industry, academia and government. We’ve also incorporated lessons learned from implementing previous versions and evolving best practices in frontier AI safety.


### Addressing the risks of harmful manipulation

With this update, we’re introducing a Critical Capability Level (CCL)\* focused on [harmful manipulation](https://deepmind.google/blog/protecting-people-from-harmful-manipulation/) — specifically, AI models with powerful manipulative capabilities that could be misused to systematically and substantially change beliefs and behaviors in identified high stakes contexts over the course of interactions with the model, reasonably resulting in additional expected harm at severe scale.

This addition builds on and operationalizes research we’ve done to identify and evaluate [mechanisms that drive manipulation from generative AI](https://arxiv.org/abs/2404.15058). Going forward, we'll continue to invest in this domain to better understand and measure the risks associated with harmful manipulation.

### Adapting our approach to misalignment risks

We’ve also expanded our Framework to address potential future scenarios where misaligned AI models might interfere with operators’ ability to direct, modify or shut down their operations.

While our previous version of the Framework included an exploratory approach centered on instrumental reasoning CCLs (i.e., warning levels specific to when an AI model starts to think deceptively), with this update we now provide further protocols for our machine learning research and development CCLs focused on models that could accelerate AI research and development to potentially destabilizing levels.

In addition to the misuse risks arising from these capabilities, there are also misalignment risks stemming from a model’s potential for undirected action at these capability levels, and the likely integration of such models into AI development and deployment processes.

To address risks posed by CCLs, we conduct safety case reviews prior to external launches when relevant CCLs are reached. This involves performing detailed analyses demonstrating how risks have been reduced to manageable levels. For advanced machine learning research and development CCLs, large-scale internal deployments can also pose risk, so we are now expanding this approach to include such deployments.

### Sharpening our risk assessment process

Our Framework is designed to address risks in proportion to their severity. We’ve sharpened our CCL definitions specifically to identify the critical threats that warrant the most rigorous governance and mitigation strategies. We continue to apply safety and security mitigations before specific CCL thresholds are reached and as part of our standard model development approach.

Lastly, in this update, we go into more detail about our risk assessment process. Building on our core early-warning evaluations, we describe how we conduct holistic assessments that include systematic risk identification, comprehensive analyses of model capabilities and explicit determinations of risk acceptability.

### FSF 3.1: Introducing tracked capability levels

As of April 17, 2026, we are adding Tracked Capability Levels (TCLs) in certain domains to our [Frontier Safety Framework](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/strengthening-our-frontier-safety-framework/frontier-safety-framework_3-1.pdf), introducing a new capability level to help us spot and evaluate potential less extreme risks sooner.

We've also provided more detail on our full risk management process, from initial identification to mitigation.

## Advancing our commitment to frontier safety

The Frontier Safety Framework represents our continued commitment to taking a scientific and evidence-based approach to tracking and staying ahead of AI risks as capabilities advance toward AGI. By expanding our risk domains and strengthening our risk assessment processes, we aim to ensure that transformative AI benefits humanity, while minimizing potential harms.

Our Framework will continue evolving based on new research, stakeholder input and lessons from implementation. We remain committed to working collaboratively across industry, academia and government.

The path to beneficial AGI requires not just technical breakthroughs, but also robust frameworks to mitigate risks along the way. We hope that our updated Frontier Safety Framework contributes meaningfully to this collective effort.

**Learn more**

[Read the latest Frontier Safety Framework](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/strengthening-our-frontier-safety-framework/frontier-safety-framework_3-1.pdf)

**Footnotes**

\*We built our Framework around capability thresholds called Critical Capability Levels (CCLs). These are capability levels at which, absent mitigation measures, frontier AI models or systems may pose heightened risk of severe harm.
