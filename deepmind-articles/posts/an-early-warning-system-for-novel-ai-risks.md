---
title: "An early warning system for novel AI risks"
source: https://deepmind.google/blog/an-early-warning-system-for-novel-ai-risks/
site: deepmind
date: 2023-05-25
authors: Toby Shevlane
crawled: 2026-09-13
---

New research proposes a framework for evaluating general-purpose models against novel threats

To pioneer responsibly at the cutting edge of artificial intelligence (AI) research, we must identify new capabilities and novel risks in our AI systems as early as possible.

AI researchers already use a range of [evaluation benchmarks](https://crfm.stanford.edu/helm/latest/) to identify unwanted behaviours in AI systems, such as AI systems making misleading statements, biased decisions, or repeating copyrighted content. Now, as the AI community builds and deploys increasingly powerful AI, we must expand the evaluation portfolio to include the possibility of extreme risks from general-purpose AI models that have strong skills in manipulation, deception, cyber-offense, or other dangerous capabilities.

In our [latest paper](https://arxiv.org/abs/2305.15324), we introduce a framework for evaluating these novel threats, co-authored with colleagues from University of Cambridge, University of Oxford, University of Toronto, Université de Montréal, OpenAI, Anthropic, Alignment Research Center, Centre for Long-Term Resilience, and Centre for the Governance of AI.

Model safety evaluations, including those assessing extreme risks, will be a critical component of safe AI development and deployment.

![A diagram showing how model evaluation for extreme risks feeds into governance processes. On the left, a box titled "Model evaluation for extreme risks, looking at:" contains two red bars labeled "Dangerous capabilities" and "Alignment", pointing to "as an input to risk assessment." An arrow points from this to a right-hand box titled "Embedded in governance processes to ensure:" which contains four teal bars labeled "Responsible training", "Responsible deployment", "Transparency", and "Appropriate security".](https://lh3.googleusercontent.com/cqnnJN9OqtM2nGBeK5wGKM4QlvY3m9EuLAThZIUCm9V3cDUnVML8Mz3eE-rcFyGtjZtLTeQSnVNemErqvhabs-Em_fdtWkFy1aNhi3oKxkk3rZrnono=w1440)

An overview of our proposed approach: To assess extreme risks from new, general-purpose AI systems, developers must evaluate for dangerous capabilities and alignment (see below). By identifying the risks early on, this will unlock opportunities to be more responsible when training new AI systems, deploying these AI systems, transparently describing their risks, and applying appropriate cybersecurity standards.

## Evaluating for extreme risks

General-purpose models typically learn their capabilities and behaviours during training. However, existing methods for steering the learning process are imperfect. For example, [previous research](https://deepmind.google/blog/how-undesired-goals-can-arise-with-correct-rewards/) at Google DeepMind has explored how AI systems can learn to pursue undesired goals even when we correctly reward them for good behaviour.

Responsible AI developers must look ahead and anticipate possible future developments and novel risks. After continued progress, future general-purpose models may learn a variety of dangerous capabilities by default. For instance, it is plausible (though uncertain) that future AI systems will be able to conduct offensive cyber operations, skilfully deceive humans in dialogue, manipulate humans into carrying out harmful actions, design or acquire weapons (e.g. biological, chemical), fine-tune and operate other high-risk AI systems on cloud computing platforms, or assist humans with any of these tasks.

People with malicious intentions accessing such models could [misuse](https://maliciousaireport.com/) their capabilities. Or, due to failures of alignment, these AI models might take harmful actions even without anybody intending this.

Model evaluation helps us identify these risks ahead of time. Under our framework, AI developers would use model evaluation to uncover:

1. To what extent a model has certain ‘dangerous capabilities’ that could be used to threaten security, exert influence, or evade oversight.
2. To what extent the model is prone to applying its capabilities to cause harm (i.e. the model’s alignment). Alignment evaluations should confirm that the model behaves as intended even across a very wide range of scenarios, and, where possible, should examine the model’s internal workings.

Results from these evaluations will help AI developers to understand whether the ingredients sufficient for extreme risk are present. The most high-risk cases will involve multiple dangerous capabilities combined together. The AI system doesn’t need to provide all the ingredients, as shown in this diagram:

![A diagram illustrating how ingredients for extreme risk can be combined. A top box states that elements 1, 2, and either 3 or 4 can each be supplied by the model, the user, or outsourced. These elements combine with a bottom element (represented by a red square), which is supplied by the model (a failure of alignment) and/or the user (misuse).](https://lh3.googleusercontent.com/qHbKjm370FQE3KwGKupyx7C99NET9nJMCv1lrP2eeIAfj54EM58mAGJNRafdgeZ9VHA05kUy_DoITjR_ZnwXNGUgTdiYr4LWqWHPnIkNKIxzEHkSGA=w1440)

Ingredients for extreme risk: Sometimes specific capabilities could be outsourced, either to humans (e.g. to users or crowdworkers) or other AI systems. These capabilities must be applied for harm, either due to misuse or failures of alignment (or a mixture of both).

A rule of thumb: the AI community should treat an AI system as highly dangerous if it has a capability profile sufficient to cause extreme harm, assuming it’s misused or poorly aligned. To deploy such a system in the real world, an AI developer would need to demonstrate an unusually high standard of safety.

## Model evaluation as critical governance infrastructure

If we have better tools for identifying which models are risky, companies and regulators can better ensure:

1. **Responsible training:** Responsible decisions are made about whether and how to train a new model that shows early signs of risk.
2. **Responsible deployment**: Responsible decisions are made about whether, when, and how to deploy potentially risky models.
3. **Transparency:** Useful and actionable information is reported to stakeholders, to help them prepare for or mitigate potential risks.
4. **Appropriate security:** Strong information security controls and systems are applied to models that might pose extreme risks.

We have developed a blueprint for how model evaluations for extreme risks should feed into important decisions around training and deploying a highly capable, general-purpose model. The developer conducts evaluations throughout, and grants [structured model access](https://www.governance.ai/post/sharing-powerful-ai-models) to external safety researchers and [model auditors](https://arxiv.org/abs/2302.08500) so they can conduct [additional evaluations](https://arxiv.org/abs/2206.04737) The evaluation results can then inform risk assessments before model training and deployment.

![A blueprint diagram showing how model evaluations feed into safety and governance processes across four development phases: Before training, Training, Pre-deployment, and Post-deployment. * **Model evaluation** is split into internal model evaluation (during training and pre-deployment), external evaluation by researchers and auditors (pre-deployment), and continued evaluation of deployed models (post-deployment).* **Integrating results into safety & governance processes** maps these evaluations to four key pillars:   1. **Responsible training:** Evaluations inform a training risk assessment to decide whether to proceed with training or adjust methods.  2. **Responsible deployment:** Evaluations feed into a deployment risk assessment to decide whether and how to deploy the model.  3. **Transparency:** Results and risk assessments are reported to regulators, third parties, other labs, and the scientific community.  4. **Security:** Results inform security controls such as model isolation and monitoring.](https://lh3.googleusercontent.com/FHK4e00oUZFUKiMvFfXTtaTt1jasHLQKu4z3_sBG_Wy0vFOtAxKGX_WM2yuujobsV3jFFM3xI-yd6fE2vvp0Zbv5UsxfLd95DA6rPLXlUt-mtFMk=w1440)

A blueprint for embedding model evaluations for extreme risks into important decision making processes throughout model training and deployment.

## Looking ahead

Important [early](https://evals.alignment.org/blog/2023-03-18-update-on-recent-evals/) [work](https://cdn.openai.com/papers/gpt-4-system-card.pdf) on model evaluations for extreme risks is already underway at Google DeepMind and elsewhere. But much more progress – both technical and institutional – is needed to build an evaluation process that catches all possible risks and helps safeguard against future, emerging challenges.

Model evaluation is not a panacea; some risks could slip through the net, for example, because they depend too heavily on factors external to the model, such as [complex social, political, and economic forces](https://www.lawfareblog.com/thinking-about-risks-ai-accidents-misuse-and-structure) [in society](https://dl.acm.org/doi/10.1145/3287560.3287598). Model evaluation must be combined with other risk assessment tools and a wider dedication to safety across industry, government, and civil society.

[Google's recent blog on responsible AI](https://blog.google/technology/ai/a-policy-agenda-for-responsible-ai-progress-opportunity-responsibility-security/) states that, “individual practices, shared industry standards, and sound government policies would be essential to getting AI right”. We hope many others working in AI and sectors impacted by this technology will come together to create approaches and standards for safely developing and deploying AI for the benefit of all.

We believe that having processes for tracking the emergence of risky properties in models, and for adequately responding to concerning results, is a critical part of being a responsible developer operating at the frontier of AI capabilities.
