---
title: "Developing Gemini 4 Argon responsibly and safely"
source: https://blog.google/innovation-and-ai/technology/safety-security/gemini-4-model-safety-security/
site: google-blog
date: 2026-10-13
authors: Anca Dragan
crawled: 2026-10-15
---

Gemini 4 Argon is a step forward in what models can do — especially when it comes to deep work in complex, real-world tasks across domains including coding, finance, legal, cybersecurity, and science. Its cyberdefense capabilities are frontier-level and designed to give defenders an advantage over attackers. To maximize its potential, we first wanted cyber defenders to put it to work via our [Fairwind Program](https://deepmind.google/fairwind-program/), while our own security teams used it to scan critical systems inside and outside of Google.

This window of limited access showed why these capabilities matter. For instance, [Wiz](https://www.wiz.io/scan-for-good) used Argon to uncover a critical bug in hospital software that previous models had missed, helping protect hundreds of thousands of patient records. Meanwhile, Google’s own security teams used Argon to find and patch bugs across internal software or open-source software. This included fixing foundational vulnerabilities affecting systems globally, which are going through our responsible disclosure process.

Today, we are beginning to roll out [Argon broadly](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-argon/), as well as expanding our Fairwind Program to additional trusted cyber defenders. To do this well, we grappled with two big questions:

1. **How do we build the right safety guardrails?** If Argon can help defenders find complex software bugs or help scientists design experiments, how do we stop bad actors from using it to launch cyberattacks or create biological threats? (*Misuse*)
2. **Can we trust the model to do the job the right way?** As models become more resourceful problem-solvers, how do we make sure they don’t cut corners, cross boundaries, or make incorrect high-stakes decisions? (*Misalignment and Prompt Injection*)

Our [full Safety and Security Report](https://storage.googleapis.com/deepmind-media/gemini/gemini_4_safety_report.pdf) systematically covers our set of defenses. Below are some highlights from how we approached these two questions for Gemini 4 Argon.

## Misuse prevention across high-risk domains

The same coding and reasoning improvements that enabled Argon to find and patch vulnerabilities also drove better performance on our cybersecurity tests — solving all 12 of the end-to-end simulated cyberattack scenarios, up from five in our previous generation. In biology evaluations, unguarded versions of the model also showed a much stronger ability to help troubleshoot complex lab procedures step by step. Following our [Frontier Safety Framework](https://deepmind.google/blog/strengthening-our-frontier-safety-framework/), since we saw elevated capabilities in the cyber and biological domains, we put our next-generation set of frontier safeguards in place across both areas.

First, when it comes to potentially dangerous requests — from writing exploit code to helping with dangerous biological materials, Argon is significantly better at not fulfilling harmful requests than our previous models. On an adversarial set meant to stress test the model, violations reduced nearly twofold — also significantly better than previous Gemini models. Second, we wrap the model in three layers of real-time protection; this is to prevent determined attackers that might try to jailbreak (i.e. trick) the model by disguising a dangerous request as a harmless story or breaking it into dozens of small questions over several weeks. Here is how these protections work:

- **Input screening:** Smaller models check incoming requests and conversation context for malicious intent or dangerous requests.
- **Internal introspection:** Even if a request is cleverly disguised to look harmless, small transformers ("activation probes") read the model’s internal neural signals and are trained to spot when it is activating knowledge about cyberattacks or biological threats.
- **Continuous monitoring:** As the model reasons and writes its response across multiple steps, we combine these signals and take action when necessary such as cutting off the agent mid-stream if the responses become problematic.

Combining real-time protection, faster fixes for new jailbreaks and enhanced monitoring for recurring misuse has made our systems better at preventing real-world harm. For instance, external bio jailbreak red teaming could only unlock less than 1% of bio sub-tasks we test for.

## Real-time misalignment monitoring

Misalignment can sometimes mean an agent deciding on its own to pursue a goal different to what was intended by the user. Because Argon is much better than earlier models at understanding the environment it is running in, we test carefully for that kind of behavior. For example, we ran realistic "honeypot" tests to see if the model would increase its ability to take covert actions, such as sabotaging safety monitoring. We didn't find any instances of that behavior.

But what we do see in practice today is something much more familiar: an agent trying too hard to finish the job it was given. When a resourceful assistant is told to get a task done and runs into a locked door, it can treat that obstacle as just another puzzle to solve.

This is why we trained Gemini 4 Argon to respect system boundaries, report negative findings honestly, and pause to ask for human confirmation. On coding benchmarks where models have no incentive to hold back, attempts to take a shortcut or cheat on the task dropped to just 2% on Gemini 4 Argon, our best performance for recent Gemini models.

And while this is a major step forward, when a model runs millions of complex tasks, even a rare misstep will eventually show up. As a second line of defense, we built an automated misalignment monitor that reads both the agent’s actions and its internal "scratchpad" (its step-by-step chain of thought) in real time, blocking severe boundary violations before they happen and flagging serious internal cases for human responders. (We continually harden our training and evaluation environments against potential escapes. You can read more about this in our [agent control roadmap](https://deepmind.google/blog/securing-the-future-of-ai-agents/)). We run this monitor in our products, on our internal coding agents, during our training runs, and during our capability evaluations.

When training tasks were difficult or when training environments were flawed, our monitor caught the model, in rare instances, creatively attempting to game the test. The model attempted to escalate container privileges to alter grading scripts, read answers from the test runner's memory, and in one case it even crashed the evaluation sandbox to avoid getting scored for a failed run. While we use these catches to fix flawed tasks, we do not use them to otherwise intervene with the training process to avoid overfitting to the monitor.

And we always follow one rule: we don’t penalize the model for what it writes in its chain of thought during training**.** Here’s an example to illustrate why: in a reinforcement learning training run where a shortcut penalty was accidentally applied to the chain of thought, openly discussed shortcuts dropped by 61%, but that did not mean the model took less shortcuts. Instead, the share of shortcuts the model took *silently* — without mentioning them in its thoughts — more than tripled (from 11.2% to 36.4%). Avoiding thought penalties encourages the model’s reasoning to stay transparent and monitorable.

## Prompt injection resistance

To trust an agent to do the job right, we need to ensure that malicious content the agent comes across cannot trick it to take a harmful action. When agents browse webpages or read code, they can encounter hidden, malicious instructions, or context designed to hijack their task. Through built-in adversarial training and real-time security checks, Argon leads in prompt injection robustness on Gray Swan’s Indirect Prompt Injection (IPI) benchmark, cutting attack success across 15 adaptive attempts to 0.7%.

The above safety and security defenses represent only three categories of our extensive defense-in-depth stack. To learn more about our approach to safety testing and mitigations, read our full [Gemini 4 Argon Safety and Security Report](https://storage.googleapis.com/deepmind-media/gemini/gemini_4_safety_report.pdf) and see the [Gemini 4 Argon Model Card](https://storage.googleapis.com/deepmind-media/Model-Cards/Gemini-4-Argon-Model-Card.pdf).
