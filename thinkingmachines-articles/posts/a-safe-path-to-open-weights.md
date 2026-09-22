---
title: "A Safe Path to Open Weights"
date: 2026-08-31
source: https://thinkingmachines.ai/blog/a-safe-path-to-open-weights/
crawled: 2026-09-22
---

> **Abstract:** Safe open-weight models are public goods, as they put AI development and safety work in many hands and make training choices inspectable. Open models also carry real misuse risks, and release is irreversible. To release safely, we must consider both the model and the ecosystem it enters. For the model, we conduct robust safety testing and research whether dangerous capabilities can be decoupled from general intelligence. For the ecosystem, we invest in its readiness through staged releases, supporting defenders, and collaboration with safety researchers. By iteratively choosing the most open option the evidence supports while building up the ecosystem's resilience, we can move toward openness safely.

The [mission](/blog/the-future-worth-building-is-human/) of Thinking Machines is to build AI that extends human will and judgment. In pursuit of that mission, we recently released [Inkling](/news/introducing-inkling/) and [Inkling-Small](/news/inkling-small/), two open-weight language models that anyone can own, run, and customize.

Strong open-weight models put AI development in many hands. We believe that this is a good thing: the knowledge of what AI should do lives with the people doing the work, so they should be able to shape their models directly. All models, including our own, carry the assumptions and biases of those who trained it; open weights make those choices inspectable and revisable. Without strong open models, training and deployment expertise risks becoming concentrated in a few labs, leaving everyone else less able to understand, adapt, or govern the technology.

## Open-weight models carry misuse risks

Once weights are public, anyone can use them, including bad actors. Cybersecurity shows what this means. In April 2026, Anthropic reported that Claude Mythos Preview found thousands of previously unknown vulnerabilities across every major operating system and browser and wrote working exploits without human guidance. Systems like this could substantially lower the time, cost, and expertise required for offensive cyber operations. Will our society be safer when open-weights models allow everyone to have superhuman cybersecurity skills?

There are genuine uncertainties around the net effect of open weights on security and the offense-defense balance. These models could find and patch vulnerabilities before offenders do when they’re in defenders’ hands, but the same capabilities could accelerate exploitations across large numbers of unpatched systems when they are in attackers’ hands. Similar tradeoffs exist in other dual-use domains like chemistry and biology.

Given these uncertainties, releasing weights indiscriminately is not a safe path forward.

## A safe path to open-weight models

Is there a safe path to open the weights of powerful models when the misuse risks are real? We think that a path exists, though we have not mapped all of it. The central idea is that safe release depends on the model and the ecosystem around it.

### Is the model safe?

Robust safety testing – an imperfect but essential proxy for real-world capability in dangerous domains – must be a necessary part of our model release process. What harmful tasks can it complete? How accessible is it? What happens if guardrails are removed?

More broadly, additional safety research is needed. For example, we are particularly interested in whether dangerous capabilities that depend on specialized knowledge can be reduced through pretraining data curation or post-training interventions. This remains an active research question rather than an established solution.

### Is the ecosystem ready?

Readiness means layered defense. The first layer is to enable individual organizations to patch their systems early or catch attacks in progress. Defensive research adds another layer, developing tools and techniques that let AI models themselves strengthen defenses at scale. These are just two of many layers. To prepare the ecosystem with layered defenses, we plan to collaborate with the safety community and provide access to capable models.

A tension here is that the ecosystem builds defenses by working with capable models, but every expansion of access also expands who can misuse them. To address this tension, we can carefully stage releases with options such as monitored API access, hosted fine-tuning, and vetting defenders. Considering the rapid speed of AI capability advancement, these stages also need to move quickly enough for defensive learning to remain relevant.

On a safe path to openness, each stage should widen access only when the evidence supports it. The path is therefore iterative: at each step, choose the most open option the evidence supports, and let each release inform the next. A model held back today can become less risky as the ecosystem changes, and new evidence might suggest that we can open its weights.

## How we assessed Inkling

Inkling and Inkling-Small are not the most capable models at the frontier. Our release decisions therefore primarily addressed whether releasing their weights would add material incremental risk beyond what existing open-weights models already pose. A finding that a model does not advance the dangerous-capability frontier is important but not sufficient. We also considered whether Inkling’s multimodality, capacity for customization, or accessibility could make harmful capability meaningfully easier to use.

We tested Inkling and Inkling-Small in three ways: internal evaluations across a broad taxonomy of harms, external testing by four independent organizations, and a fine-tuning study to elicit worst-case capabilities. Based on the results of these evaluations, we concluded that releasing Inkling was not likely to add material risk beyond what existing open-weight models already pose.

**Internal safety evaluations.** Our internal evaluation suite spanned three tracks. The first targeted dangerous dual-use domains like CBRNchemical, biological, radiological, and nuclear and offensive cybersecurity, testing both what the model knows about these domains and whether it can operationalize that knowledge in realistic settings. The second was a broad misuse set covering direct requests for harmful content and behavior in agentic, tool-use settings. The third was our own multimodal content evaluation, which tests models on harmful prompts paired with benign look-alikes across 17 languages and text, image, and audio inputs. In each of these tracks, Inkling and Inkling-Small’s results were in line with other open-weight models.

**External red-teaming.** We worked with four external organizations, giving them early access to Inkling for pre-deployment testing in four areas:

- ***General misuse***: probing for policy violations against our model spec (Scale AI)
- ***Vulnerable-user interaction***: suicide, self-harm, eating disorders, and child safety (Handshake AI)
- ***CBRN and cybersecurity***: elicitation of dangerous dual-use capabilities (FAR.AI)
- ***Loss-of-control behaviors***: scheming, evaluation awareness, and sabotage (Apollo Research)

Across these areas, external testers did not identify capabilities that would meaningfully increase real-world risk beyond what is already achievable with existing open-weight models, or, where relevant, they did not find the safeguards of Inkling or Inkling Small to be meaningfully weaker than those of existing open-weight models.

**Adversarial fine-tuning.** Because open weights can be customized to strip a model of its safety training, refusal behavior cannot be treated as a durable safeguard for an open-weight release. To assess this, we fine-tuned variants of Inkling and Inkling-Small optimized to comply with, rather than refuse, harmful requests – and ran them against our dual-use evaluations. This tests whether the model raises new material risks if its safeguards are removed. In our experiments, it did not: the helpful-only variants did not provide new uplift on CBRN and cyber tasks, and remained comparable to existing open-weight models.

Taken together, neither model extends the dangerous-capability frontier. Neither meaningfully broadens access to it, as models of comparable or greater strength in these domains are already downloadable. Although refusals can be removed, doing so did not reveal substantially greater capability on these evaluations. Defenders, meanwhile, are already contending with models at or above this level. Based on these points, we concluded that releasing Inkling was not likely to add material risk beyond what existing open-weight models already pose.

As our models approach the capability frontier, the balance across capability, accessibility, safeguard removability, and ecosystem readiness will change. Our safety approach will need to change with it.

## Decoupling dangerous capabilities from general intelligence

A common assumption holds that dangerous capabilities emerge without explicit training and correlate strongly with general intelligence. As a result, cyber-range results[How fast is autonomous AI cyber capability advancing?](https://www.aisi.gov.uk/blog/how-fast-is-autonomous-ai-cyber-capability-advancing) (AI Security Institute, 2025) are often treated as just another capabilities benchmark to optimize – some researchers go so far as to celebrate gains as milestones.

However, we hypothesize that not all dangerous capability automatically emerges without training on it. In biology, for instance, a meaningful share of the knowledge rests on specific empirical findings, like protocols, conditions, reagents, and results, that a model acquires from particular documents in its pretraining corpus rather than inferring through general reasoning. As a result, such knowledge can potentially be withheld at training time without disturbing ordinary use. Recent work shows early promise: document-level filtering of CBRN-related content from pretraining reduces performance on harmful-capability evaluations while leaving unrelated capabilities intact.[Deep Ignorance: Filtering Pretraining Data Builds Tamper-Resistant Safeguards into Open-Weight LLMs](https://arxiv.org/abs/2508.06601) (O’Brien et al, 2025); Chen et al., 2025

This is still an open research question. General reasoning may transfer sufficiently well to let a capable model re-derive what was filtered, and the line between dangerous and ordinary technical knowledge and capability may be too blurry to cut cleanly. However, the early evidence is enough that we think the distinction is worth pushing on.

## Supporting the safety ecosystem with staged releases

Another way to make an open-weight release safer is to make the ecosystem in which it lands safer. Expanding access in stages lets society build up its defenses as it goes: a release can begin with inference API access for a limited population, widen to monitored general availability, and eventually reach open weights.

Fine-tuning APIs like Tinker add a stage between inference access and open weights. They allow providers to host weights without releasing them, while still letting users fine-tune with their own data, loss functions, and training loops. That control still captures most of the benefits of openness, and it raises the misuse ceiling above what an inference API alone allows.[Model Tampering Attacks Enable More Rigorous Evaluations of LLM Capabilities](https://arxiv.org/abs/2502.05209) (Che et al, 2025) However, the risks stay below releasing weights: the provider can monitor usage, maintain guardrails, and revoke access.

Each stage does specific work:

- ***Give defenders early inference access,*** so they can find weaknesses, patch systems, and anticipate future misuse. Anthropic’s Project GlassWing did this with Claude Mythos Preview by providing early access to a small group of trusted organizations to allow them to prepare defenses before the model reached the public. This mirrors responsible disclosure in security, where vendors get a private window to ship patches before a flaw goes public.
- ***Give vetted defenders fine-tuning access*** so they can build and strengthen the layers that detect and block risks. The winning DARPA AI Cyber Challenge team fine-tuned a model to find and fix software vulnerabilities; OpenAI’s gpt-oss-safeguard models are fine-tuned from open gpt-oss weights into policy-guided safety classifiers. Both are defensive layers built by fine-tuning—and accessible fine-tuning is what lets defenders everywhere build their own.
- ***Give vetted safety researchers white-box access*** to encourage novel safety work. We understand how shallow refusal safeguards are — bypassable through adversarial token-level optimization[Universal and Transferable Adversarial Attacks on Aligned Language Models](https://arxiv.org/abs/2307.15043) (Zou et al, 2023), removable via a single direction in activation space[Refusal in Language Models Is Mediated by a Single Direction](https://arxiv.org/abs/2406.11717) (Arditi et al, 2024), and concentrated in just the first few output tokens [Safety Alignment Should Be Made More Than Just a Few Tokens Deep](https://arxiv.org/abs/2406.05946) (Qi et al, 2024) — only because researchers could study open weights directly. Fine-tuning also lets us study the true capability ceilings of models in dangerous domains.[Estimating Worst-Case Frontier Risks of Open-Weight LLMs](https://arxiv.org/abs/2508.03153) (Wallace et al, 2025) Similar to crash testing for cars, white-box testing lets us study model failure modes in-depth, under controlled conditions, to prevent real-world harm.
- ***Give the public monitored access before opening fully,*** so we can assess misuse patterns that may appear once controls come off, and support the ecosystem to prepare in advance.

These stages are not a fixed sequence that automatically ends with releasing the model’s weights. Instead, we think of them as a way to gather evidence and build resilience while moving towards greater openness. Progression should depend on what we learn about the model and whether the surrounding ecosystem is ready.

This post offers a high-level framework, not a complete release standard. Important questions remain: what evidence should justify moving from one stage to the next, how uncertainty should affect that decision, what changes in capability or accessibility should pause progression, and how ecosystem readiness should be measured. We plan to publish a more detailed framework covering evaluations, access criteria, and stop conditions as we learn from Inkling and future models.

## Building the safety ecosystem together

This safe path to open models only works if the ecosystem’s defenses improve as quickly as the models do. We will do our part: deciding carefully what to release, and researching how to decouple intelligence from dangerous capability.

However, most of the work above happens outside our lab, and much of what this post describes builds on other people’s work: for example, data filtering (Anthropic, EleutherAI, and the UK AI Security Institute), our external pre-deployment safety testers (Scale AI, Apollo Research, Handshake AI, and FAR.AI), the framework for fine-tuning safety (OpenAI), and countless others working on cyber-defense. No lab builds this path alone. Each new defense lets us open models that were previously too risky to release. This takes many more hands than ours alone, and we want to support that work broadly.

We will shortly launch Tinker safety grants: funding for the community to strengthen the ecosystem’s defenses. If you do safety research, our Tinker platform makes it easy to study fine-tuning and its risks, so give it a go. If you defend systems, we want to give you a head start. If you evaluate models, we want you to scrutinize ours. And if you want to do this from the inside, join our safety team—[we’re hiring](/#join-us)!
