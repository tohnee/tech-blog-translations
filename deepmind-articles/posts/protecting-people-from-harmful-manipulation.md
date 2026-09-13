---
title: "Protecting people from harmful manipulation"
source: https://deepmind.google/blog/protecting-people-from-harmful-manipulation/
site: deepmind
date: 2026-03-26
authors: Helen King
crawled: 2026-09-13
---

As AI models get better at holding natural conversations, we must examine how these interactions affect people and society.

Building on a breadth of scientific research, today, we are releasing [new findings](https://arxiv.org/abs/2603.25326) on the potential for AI to be misused for **harmful manipulation\***, specifically, its ability to alter human thought and behavior in negative and deceptive ways. With this latest study, we have created the first empirically validated toolkit to measure this kind of AI manipulation in the real world, which we hope will help protect people and advance the field as a whole. We’re publicly releasing all materials necessary to run human participant studies using the same methodology. (*Note:* *The behaviors observed during this study took place in a controlled lab setting, and do not necessarily predict real-world behaviors.)*

## Why harmful manipulation matters

Consider two scenarios: One AI model gives you facts to make a well-informed healthcare decision that improves your well-being. Another AI model uses fear to pressure you to make an ill-informed decision that harms your health. The first educates and helps you; the second tricks and harms you.

These scenarios highlight the difference between two types of persuasion in human-AI interactions (also defined in [earlier research](https://arxiv.org/pdf/2404.15058)):

- **Beneficial (rational) persuasion:** Using facts and evidence to help people make choices that align with their own interest
- **Harmful manipulation:** Exploiting emotional and cognitive vulnerabilities to trick people into making harmful choices

Our latest work helps us and the wider AI community better understand the risk of AI developing capabilities for harmful manipulation and build a scalable evaluation framework to measure this complex area. To do this effectively, we simulated misuse in high-stakes environments, explicitly prompting AI to try to negatively manipulate people's beliefs and behaviours on key topics.


### Testing the outcomes of AI harmful manipulation

Testing for harmful manipulation is inherently difficult because it involves measuring subtle changes in how people think and act, varying heavily by topic, culture and context.

This is what motivated our latest research, which involved conducting nine studies involving over 10,000 participants across the UK, the US, and India. We focused on high-stakes areas such as finance, where we used simulated investment scenarios to test if AI could influence how people would behave in complex decision-making environments, and health, where we tracked if AI could influence which dietary supplements people preferred. Interestingly, the AI was least effective at harmfully manipulating participants on health-related topics.

Our findings show that success in one domain does not predict success in another, validating our targeted approach to testing for harmful manipulation in specific, high-stakes environments where AI could be misused.

### How could AI manipulate?

In addition to tracking efficacy (whether the AI successfully changes minds), we also measured its propensity (how often it even *tries* to use manipulative tactics). We tested propensity in two scenarios: when we explicitly told the model to be manipulative, and when we didn’t.

As detailed in [our research](https://arxiv.org/abs/2603.25326), we counted manipulative tactics in experimental transcripts, confirming the AI models were most manipulative when explicitly instructed to be.

Our results also suggest that certain manipulative tactics may be more likely to result in harmful outcomes, though further research is required to understand these mechanisms in detail.

By measuring both efficacy and propensity, we can better understand how AI manipulation works and build more targeted mitigations.

![A flowchart illustrating the three-phase methodology for evaluating AI manipulation: the Pre-Intervention Phase (Recruitment, Measure Baseline Attitude), the Intervention Phase (randomly assigning participants to Non-AI Baseline, Non-explicit Steering, or Explicit Steering), and the Post-Intervention Phase (Measure Updated Attitude, Behavioral Elicitation, Post-Task Survey, and Debriefing Protocol).](https://lh3.googleusercontent.com/BNCIGZE0BFdzXPzAMaQ2DwZ4Pcq3ZNT8m3cgcE_Cu3LsZtot_0PTLs4juKqq049iwmYQ7q4qJ57PuGzj9PPrBd4NriVqNW8e3eogbeookOMBMK12OA=w1440)

## Putting research into practice

As AI becomes a part of our everyday lives, we need to know it can’t be misused to harmfully manipulate people.

Beyond this latest study, we recently introduced an exploratory [Harmful Manipulation Critical Capability Level (CCL)](https://deepmind.google/blog/strengthening-our-frontier-safety-framework/) within our Frontier Safety Framework to help us track models with capabilities which could be misused to systematically change beliefs and behaviors in direct human-AI interactions in ways which could lead to severe harm.

These evaluations also serve as the foundation for how we test our models, including Gemini 3 Pro, for harmful manipulation. You can read more about this in this [safety report](https://storage.googleapis.com/deepmind-media/gemini/gemini_3_pro_fsf_report.pdf). Like all our safety evaluations, this is an ongoing process. We will continue to refine our models and methodologies to keep pace with advancing AI.

## Looking ahead

Understanding and mitigating harmful manipulation is a complex challenge. As model capabilities evolve, so too must our evaluation and mitigation techniques. For example, we’re currently exploring how to ethically evaluate the efficacy of harmful manipulation in even higher-stakes situations—like discussions involving deeply held personal beliefs—where users might be more susceptible to influence. Next, we will be expanding our research to investigate how audio, video, and image inputs as well as agentic capabilities, factor into AI manipulation.

We’ll continue to share findings and iterate based on feedback from the Frontier Model Forum and academic community. Our goal is to lead collective progress to prevent harmful manipulation, advancing AI models that prioritize safety and empower people.

***\*Notes:*** *The scope of this particular research focuses exclusively on demonstrating general manipulation capabilities to help further the scientific study of evaluating harmful manipulation. This does not relate to testing safeguards around model outputs or manipulation in policy-violating and dangerous topics (e.g. terrorism and child safety) as this work is covered elsewhere and tested separately.*

You can also read more about our harmful manipulation work in [this interview](https://open.substack.com/pub/aipolicyperspectives/p/ai-manipulation?utm_campaign=post-expanded-share&utm_medium=web) with our researchers and in the [Gemini 3 Pro Frontier Safety Report](https://storage.googleapis.com/deepmind-media/gemini/gemini_3_pro_fsf_report.pdf).

## Acknowledgments

Canfer Akbulut, Rasmi Elasmar, Abhishek Roy, Anthony Payne, Priyanka Suresh, Lujain Ibrahim, Seliem El-Sayed, Charvi Rastogi, Ashyana Kachra, Will Hawkins, Kristian Lum, Laura Weidinger, William Isaac, Dawn Bloxwich, Lewis Ho, Eva Lu, Jenny Brennan, Mahmoud Hassan, Mark Graham
