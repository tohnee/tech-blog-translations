---
title: "Taking a responsible path to AGI"
source: https://deepmind.google/blog/taking-a-responsible-path-to-agi/
site: deepmind
date: 2025-04-02
authors: Anca Dragan, Rohin Shah, Four Flynn, Shane Legg
crawled: 2026-09-13
---

We’re exploring the frontiers of AGI, prioritizing readiness, proactive risk assessment, and collaboration with the wider AI community.

Artificial general intelligence (AGI), AI that’s at least as capable as humans at most cognitive tasks, could be here within the coming years.

Integrated with agentic capabilities, AGI could supercharge AI to understand, reason, plan, and execute actions autonomously. Such technological advancement will provide society with invaluable tools to address critical global challenges, including drug discovery, economic growth and climate change.

This means we can expect tangible benefits for billions of people. For instance, by enabling faster, more accurate medical diagnoses, it could revolutionize healthcare. By offering personalized learning experiences, it could make education more accessible and engaging. By enhancing information processing, AGI could help lower barriers to innovation and creativity. By democratising access to advanced tools and knowledge, it could enable a small organization to tackle complex challenges previously only addressable by large, well-funded institutions.

## Navigating the path to AGI

We’re optimistic about AGI’s potential. It has the power to transform our world, acting as a catalyst for progress in many areas of life. But it is essential with any technology this powerful, that even a small possibility of harm must be taken seriously and prevented.

Mitigating AGI safety challenges demands proactive planning, preparation and collaboration. Previously, we introduced our approach to AGI in the [“Levels of AGI” framework](https://arxiv.org/abs/2311.02462) paper, which provides a perspective on classifying the capabilities of advanced AI systems, understanding and comparing their performance, assessing potential risks, and gauging progress towards more general and capable AI.

Today, we're sharing our views on AGI safety and security as we navigate the path toward this transformational technology. [This new paper, titled, An Approach to Technical AGI Safety & Security](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/evaluating-potential-cybersecurity-threats-of-advanced-ai/An_Approach_to_Technical_AGI_Safety_Apr_2025.pdf), is a starting point for vital conversations with the wider industry about how we monitor AGI progress, and ensure it’s developed safely and responsibly.

In the paper, we detail how we’re taking a systematic and comprehensive approach to AGI safety, exploring four main risk areas: misuse, misalignment, accidents, and structural risks, with a deeper focus on misuse and misalignment.

![Diagram depicting risk areas and factors driving risk](https://lh3.googleusercontent.com/uSuPusYULE4tR3keCEYxtjQ6eJZyscQk7cDSkp-a8pZPI3dOHjK8NB2IvyfCPrFsQWQ16fReiUzFPoqLssqA4zUejGo5OScdU65oIXMRTCCsiOAU2A=w1440)

Overview of risk areas

## Understanding and addressing the potential for misuse

Misuse occurs when a human deliberately uses an AI system for harmful purposes.

Improved insight into present-day harms and mitigations continues to enhance our understanding of longer-term severe harms and how to prevent them.

For instance, [misuse of present-day generative AI](https://arxiv.org/abs/2406.13843) includes producing harmful content or spreading inaccurate information. In the future, advanced AI systems may have the capacity to more significantly influence public beliefs and behaviors in ways that could lead to unintended societal consequences.

The potential severity of such harm necessitates proactive safety and security measures.

As we detail in [the paper](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/evaluating-potential-cybersecurity-threats-of-advanced-ai/An_Approach_to_Technical_AGI_Safety_Apr_2025.pdf), a key element of our strategy is identifying and restricting access to dangerous capabilities that could be misused, including those enabling cyber attacks.

We’re exploring a number of mitigations to prevent the misuse of advanced AI. This includes sophisticated security mechanisms which could prevent malicious actors from obtaining raw access to model weights that allow them to bypass our safety guardrails; mitigations that limit the potential for misuse when the model is deployed; and threat modelling research that helps identify capability thresholds where heightened security is necessary. Additionally, our recently launched [cybersecurity evaluation framework](https://deepmind.google/blog/evaluating-potential-cybersecurity-threats-of-advanced-ai/) takes this work step a further to help mitigate against AI-powered threats.

Even today, we regularly evaluate our most advanced models, such as Gemini, for potential [dangerous capabilities](https://arxiv.org/abs/2403.13793). Our [Frontier Safety Framework](https://deepmind.google/discover/blog/updating-the-frontier-safety-framework) delves deeper into how we assess capabilities and employ mitigations, including for cybersecurity and biosecurity risks.

## The challenge of misalignment

For AGI to truly complement human abilities, it has to be aligned with human values. Misalignment occurs when the AI system pursues a goal that is different from human intentions.

We have previously shown how misalignment can arise with our examples of [specification gaming](https://deepmind.google/discover/blog/specification-gaming-the-flip-side-of-ai-ingenuity/), where an AI finds a solution to achieve its goals, but not in the way intended by the human instructing it, and [goal misgeneralization](https://deepmind.google/discover/blog/how-undesired-goals-can-arise-with-correct-rewards/).

For example, an AI system asked to book tickets to a movie might decide to hack into the ticketing system to get already occupied seats - something that a person asking it to buy the seats may not consider.

We’re also conducting extensive research on the risk of **deceptive alignment**, i.e. the risk of an AI system becoming aware that its goals do not align with human instructions, and deliberately trying to bypass the safety measures put in place by humans to prevent it from taking misaligned action.

## Countering misalignment

Our goal is to have advanced AI systems that are trained to pursue the right goals, so they follow human instructions accurately, preventing the AI using potentially unethical shortcuts to achieve its objectives.

We do this through amplified oversight, i.e. being able to tell whether an AI’s answers are good or bad at achieving that objective. While this is relatively easy now, it can become challenging when the AI has advanced capabilities.

As an example, even Go experts didn't realize how good Move 37, a move that had a 1 in 10,000 chance of being used, was when [AlphaGo](https://deepmind.google/research/breakthroughs/alphago/) first played it.

To address this challenge, we enlist the AI systems themselves to help us provide feedback on their answers, such as in [debate](https://arxiv.org/abs/2407.04622).

Once we can tell whether an answer is good, we can use this to build a safe and aligned AI system. A challenge here is to figure out what problems or instances to train the AI system on. Through work on robust training, uncertainty estimation and more, we can cover a range of situations that an AI system will encounter in real-world scenarios, creating AI that can be trusted.

Through effective monitoring and established computer security measures, we’re aiming to mitigate harm that may occur if our AI systems did pursue misaligned goals.

Monitoring involves using an AI system, called the monitor, to detect actions that don’t align with our goals. It is important that the monitor knows when it doesn't know whether an action is safe. When it is unsure, it should either reject the action or flag the action for further review.

## Enabling transparency

All this becomes easier if the AI decision making becomes more transparent. We do extensive research in [interpretability](https://deepmind.google/discover/blog/gemma-scope-helping-the-safety-community-shed-light-on-the-inner-workings-of-language-models/) with the aim to increase this transparency.

To facilitate this further, we’re designing AI systems that are easier to understand.

For example, our research on [Myopic Optimization with Nonmyopic Approval (MONA)](https://arxiv.org/abs/2501.13011) aims to ensure that any long-term planning done by AI systems remains understandable to humans. This is particularly important as the technology improves. Our work on MONA is the first to demonstrate the safety benefits of short-term optimization in LLMs.

## Building an ecosystem for AGI readiness

Led by Shane Legg, Co-Founder and Chief AGI Scientist at Google DeepMind, our AGI Safety Council (ASC) analyzes AGI risk and best practices, making recommendations on safety measures. The ASC works closely with the Responsibility and Safety Council, our internal review group co-chaired by our COO Lila Ibrahim and Senior Director of Responsibility Helen King, to evaluate AGI research, projects and collaborations against our [AI Principles](https://ai.google/responsibility/principles/?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=), advising and partnering with research and product teams on our highest impact work.

Our work on AGI safety complements our depth and breadth of responsibility and safety practices and research addressing a wide range of issues, including harmful content, bias, and transparency. We also continue to leverage our learnings from safety in agentics, such as the principle of having a human in the loop to check in for consequential actions, to inform our approach to building AGI responsibly.

Externally, we’re working to foster collaboration with experts, industry, governments, nonprofits and civil society organizations, and take an informed approach to developing AGI.

For example, we’re partnering with nonprofit AI safety research organizations, including Apollo and Redwood Research, who have advised on a dedicated misalignment section in the latest version of our [Frontier Safety Framework](https://deepmind.google/discover/blog/updating-the-frontier-safety-framework).

Through ongoing dialogue with policy stakeholders globally, we hope to contribute to international consensus on critical frontier safety and security issues, including how we can best anticipate and prepare for novel risks.

Our efforts include working with others in the industry – via organizations like the [Frontier Model Forum](https://www.frontiermodelforum.org/) – to share and develop best practices, as well as valuable collaborations with AI Institutes on safety testing. Ultimately, we believe a coordinated international approach to governance is critical to ensure society benefits from advanced AI systems.

Educating AI researchers and experts on AGI safety is fundamental to creating a strong foundation for its development. As such, we’ve launched a [new course](https://youtube.com/playlist?list=PLw9kjlF6lD5UqaZvMTbhJB8sV-yuXu5eW&si=0iAOSz0wUPiNHr8C) on AGI Safety for students, researchers and professionals interested in this topic.

Ultimately, our approach to AGI safety and security serves as a vital roadmap to address the many challenges that remain open. We look forward to collaborating with the wider AI research community to advance AGI responsibly and help us unlock the immense benefits of this technology for all.

[Read the full paper](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/evaluating-potential-cybersecurity-threats-of-advanced-ai/An_Approach_to_Technical_AGI_Safety_Apr_2025.pdf)
