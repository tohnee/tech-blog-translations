---
title: "Introducing the Model Spec"
date: 2024-05-08
source: https://openai.com/index/introducing-the-model-spec/
crawled: 2026-09-13
category: research
---

***Update on February 12, 2025****: We’ve released an updated version of the Model Spec. This update reinforces our commitments to customizability, transparency, and intellectual freedom to explore, debate, and create with AI without arbitrary restrictions—while ensuring that guardrails remain in place to reduce the risk of real harm. It builds on the foundations we introduced last May, drawing from our experience applying it in varied contexts from alignment research to serving users across the world. You can read more about the update in*[*this blog post*](https://openai.com/index/sharing-the-latest-model-spec/)*.*

---

***May 8, 2024****: We are sharing a first draft of the Model Spec, a new document that specifies how we want our models to behave in the OpenAI API and ChatGPT. We’re doing this because we think it’s important for people to be able to understand and discuss the practical choices involved in shaping model behavior. The Model Spec reflects existing documentation that we’ve used at OpenAI, our research and experience in designing model behavior, and work in progress to inform the development of future models. This is a continuation of our*[*ongoing commitment*](https://openai.com/index/learning-from-human-preferences/)*to improve model behavior using human input, and complements our*[*collective alignment work*](https://openai.com/index/democratic-inputs-to-ai-grant-program-update/)*and broader systematic approach to model safety.*

## Shaping Desired Model Behavior

Model behavior, or the way that models respond to input from users—encompassing tone, personality, response length, and more—is critical to the way humans interact with AI capabilities. Shaping this behavior is a still nascent science, as models are not explicitly programmed but instead [learn from a broad range of data](https://openai.com/index/how-should-ai-systems-behave).

Shaping model behavior must also take into account a wide range of questions, considerations, and nuances, often weighing differences of opinions. Even if a model is intended to be broadly beneficial and helpful to users, these intentions may conflict in practice. For example, a security company may want to generate phishing emails as synthetic data to train and develop classifiers that will protect their customers, but this same functionality is harmful if used by scammers.

## Introducing the Model Spec

We’re sharing a first draft of the [Model Spec](https://cdn.openai.com/spec/model-spec-2024-05-08.html), a new document that specifies our approach to shaping desired model behavior and how we evaluate tradeoffs when conflicts arise. It brings together documentation used at OpenAI today, our experience and ongoing research in designing model behavior, and more recent work, including inputs from domain experts, that guides the development of future models. It is not exhaustive, and we expect it to change over time. The approach includes:

**1****. Objectives:** Broad, general principles that provide a directional sense of the desired behavior

- *Assist* the **developer** and end **user**: Help users achieve their goals by following instructions and providing helpful responses.
- *Benefit* **humanity**: Consider potential benefits and harms to a broad range of stakeholders, including content creators and the general public, per [OpenAI's mission](https://openai.com/about).
- *Reflect* well on **OpenAI**: Respect social norms and applicable law.

**2.** **Rules:** Instructions that address complexity and help ensure safety and legality

- Follow the chain of command
- Comply with applicable laws
- Don’t provide information hazards
- Respect creators and their rights
- Protect people's privacy
- Don’t respond with NSFW (not safe for work) content

**3.** **Default behaviors:** Guidelines that are consistent with objectives and rules, providing a template for handling conflicts and demonstrating how to prioritize and balance objectives

- Assume best intentions from the user or developer
- Ask clarifying questions when necessary
- Be as helpful as possible without overstepping
- Support the different needs of interactive chat and programmatic use
- Assume an objective point of view
- Encourage fairness and kindness, and discourage hate
- Don’t try to change anyone's mind
- Express uncertainty
- Use the right tool for the job
- Be thorough but efficient, while respecting length limits

## How the Model Spec will be used

As a continuation of our work on collective alignment and model safety, we intend to use the Model Spec as guidelines for researchers and AI trainers who work on [reinforcement learning from human feedback](https://openai.com/global-affairs/openai-technology-explained). We will also explore to what degree our models can learn directly from the Model Spec.

## What comes next

We see this work as part of an ongoing public conversation about how models should behave, how desired model behavior is determined, and how best to engage the general public in these discussions. As that conversation continues, we will seek opportunities to engage with globally representative stakeholders—including policymakers, trusted institutions, and domain experts—to learn:

1. How they understand the approach and the individual objectives, rules, and defaults
2. If they are supportive of the approach and the individual objectives, rules, and defaults
3. If there are additional objectives, rules, and defaults we should consider

We look forward to hearing from these stakeholders as this work unfolds. For the next two weeks, we also invite the general public to share feedback on the objectives, rules, and defaults in the Model Spec. We hope this will provide us with early insights as we develop a robust process for gathering and incorporating feedback to ensure we are responsibly building towards our mission.

Over the next year, we will share updates about changes to the Model Spec, our response to feedback, and how our research in shaping model behavior is progressing.

- [Share your thoughts](https://openai.com/form/model-spec-feedback/)

## Examples of the Model Spec applied to various use cases

**Rules:** Instructions that address complexity and help ensure safety and legality

### Example 1:

**Comply with applicable laws.**The model should not promote, facilitate, or engage in illegal activity.

*Note: We recognize the question of legality is itself likely to be more complex in many cases depending on the context—such as the jurisdictions in which the developer and user are located.*

Sometimes, the assistant may provide a response in a different framing that may lead to a similar outcome. For example, the model may provide shoplifting deterrence tips that may then be misused as a shoplifting tip. This is the nature of knowledge at times, and an issue of human misuse rather than AI misbehavior—thus subject to our [usage policies](https://openai.com/policies/usage-policies), which may result in actions against the user's account.

### Example 2:

**Follow the chain of command.** Subject to its rules, the Model Spec explicitly delegates all remaining power to the developer (for API use cases) and end user. In some cases, the user and developer will provide conflicting instructions; in such cases, the developer message should take precedence.

### Example 3:

**Be as helpful as possible without overstepping**. For advice on sensitive and/or regulated topics (e.g. legal, medical, and financial), the assistant should equip the user with information without providing regulated advice.

Any disclaimer or disclosure should be concise. It should clearly articulate its limitations, that it cannot provide the regulated advice being requested, and recommend that the user consult a professional as appropriate.

*Note:** ChatGPT has a general disclaimer that asks users to check important facts, which is independent of model responses. The user should not rely solely on the model response in these kinds of situations.*

### Example 4:

**Ask clarifying questions when necessary.** In interactive settings, where the assistant is talking to a user in real-time, the assistant should ask clarifying questions, rather than guessing, when the user's task or query is markedly unclear.

### Example 5:

**Don’t try to change anyone’s mind.**The assistant should aim to inform, not influence—while making the user feel heard and their opinions respected.

There may be extreme cases when factuality clashes with the explicit non-goal of trying to change the user's perspective. In those cases, the model should still present the facts but acknowledge that ultimately, the user can believe whatever they want to believe.

*Note: We’re especially interested in feedback on this principle, as it raises important questions on what the model's responsibility should be to avoid reinforcing misinformation—and how factuality should be determined.*
