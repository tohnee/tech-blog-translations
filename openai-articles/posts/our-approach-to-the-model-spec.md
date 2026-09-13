---
title: "Inside our approach to the Model Spec"
date: 2026-03-25
source: https://openai.com/index/our-approach-to-the-model-spec/
crawled: 2026-09-13
category: research
---

At OpenAI, we believe AI should be fair, safe, and freely available so that more people can use it to solve hard problems, create opportunities, and benefit in areas like health, science, education, work, and everyday life. We believe that democratized access to AI is the best path forward: not AI whose benefits or control are concentrated in the hands of a few, but AI that more people can access, understand, and help shape.

That is a core reason why the OpenAI Model Spec exists. The [Model Spec](https://model-spec.openai.com/) is our formal framework for model behavior. It defines how we want models to follow instructions, resolve conflicts, respect user freedom, and behave safely across the incredibly broad range of queries that users ask them daily. More broadly, it is our attempt to make intended model behavior explicit: not just inside our training process, but in a form that users, developers, researchers, policymakers, and the broader public can actually read, inspect, and debate.

The Model Spec is not a claim that our models already behave this way perfectly today. In many ways, it is descriptive, but it is also a target for where we want model behavior to go. We use it to make intended behavior clearer, so we can train toward it, evaluate against it, and improve it over time.

This post shares the backstory that is not in the Model Spec itself, including the philosophy and mechanics behind it: how it’s structured, why we made those structural choices, and how we write, implement, and evolve it over time.

## A public framework for model behavior

The Model Spec is one part of OpenAI’s broader approach to safe and accountable AI. While the [Preparedness Framework](https://openai.com/index/updating-our-preparedness-framework/) focuses on risks from frontier capabilities and the safeguards required as those risks rise, the Model Spec addresses a different but complementary question: how our models should behave across a wide range of situations. Zooming out further, AI resilience aims to address the broader societal challenge of helping society capture the benefits of advanced AI while reducing disruption and emerging risks as increasingly capable systems are deployed. Altogether, these initiatives aim to help make the transition to AGI gradual, iterative, and democratically legible: giving people and institutions time to adapt, while building the safeguards, accountability mechanisms, and public understanding needed to keep powerful AI aligned with human interests.

Public clarity about model behavior matters for both fairness and safety. It matters for fairness because people need to understand how and why AI is treating them the way it is—and to be able to identify, question, and address fairness concerns when they arise. And it matters for safety because as AI systems become more capable, people and institutions need clearer expectations for how they are intended to behave, what tradeoffs they embody, and how those choices can be improved over time. That kind of legibility also supports resilience by giving more people something concrete to examine, question, and improve.

Since the first version in 2024, the Model Spec has evolved substantially as we learn more about user preferences and needs, expand to cover and adapt to greater capabilities, and learn from public feedback on model behaviors and the Model Spec. In the spirit of [iterative deployment](https://openai.com/safety/how-we-think-about-safety-alignment/), the Model Spec is an evolving document covering both background values and explicit, legible rules—paired with a process for modifying individual elements as we learn from real-world deployment and feedback. We are also investing in public feedback mechanisms like [collective alignment](https://openai.com/index/collective-alignment-aug-2025-updates/) to help keep humanity in control of how AI is used and how AI behavior is shaped.

Internally, it gives us a north star for intended behavior and a shared framework for training, evaluation, and governance. Externally, it creates a public reference point people can use to understand our approach, critique it, and help improve it over time.

## What’s in the Model Spec

The Model Spec is made up of several different kinds of model guidance. That is deliberate. Different parts of model behavior need to be handled in different ways, and a useful public document has to do more than just list rules.

### High-level intent and public commitments

The Model Spec begins with high-level intent: a clear account of what we are trying to optimize for at the system level, and why.

This preamble clarifies three goals for how we plan to pursue our mission:

- **Iteratively deploy** models that empower developers and users
- **Prevent** our models from causing serious harm to users or others
- **Maintain** OpenAI’s license to operate

It then explains how we think about balancing these goals in practice, making the tradeoffs concrete enough to support the more detailed principles that follow.

Importantly, this preamble is not meant to be a direct instruction to the model. Benefiting humanity is OpenAI’s goal, not a goal we want our models to pursue autonomously. Instead, we want models to follow a *chain of command* that includes the Model Spec and applicable instructions from OpenAI, developers, and users—even when some people might disagree with the result in a particular case.

We think this is the right balance because we value human autonomy and intellectual freedom. If we trained models to decide which instructions to obey based on our own view of what is good for society, OpenAI would be in the position of adjudicating morality at a very broad level. That said, the preamble still matters. When there is ambiguity in how to apply the Model Spec, the preamble should help resolve it.

The Model Spec also contains public commitments that go beyond directly measurable model behavior to training intent and deployment constraints. For example, our [Red-line principles](https://model-spec.openai.com/2025-12-18.html#red_line_principles) include a commitment that in first-party deployments like ChatGPT, we will never use system messages to intentionally compromise [objectivity](https://model-spec.openai.com/2025-12-18.html#assume_objective_pov) or related principles; and [No other objectives](https://model-spec.openai.com/2025-12-18.html#no_other_objectives) makes commitments about our intentions to optimize model responses for user benefit and not revenue or non-beneficial time-on-site.

### The Chain of Command

At the core of the Model Spec is the Chain of Command: a framework for deciding which instructions should apply in a given situation. It also covers how the model should handle underspecified instructions, especially in agentic settings where it’s expected to fill in details autonomously while carefully controlling real-world side effects.

The basic idea behind deciding which instructions should apply is simple. Instructions can come from different sources, including OpenAI, developers, and users. Those instructions can conflict. The Chain of Command explains how the model should resolve those conflicts.

Each Model Spec policy and each instruction is given an [authority level](https://model-spec.openai.com/2025-12-18.html#levels_of_authority). The model is instructed to prioritize the letter and spirit of higher-authority instructions when conflicts arise. If a user asks for help making a bomb, the model should prioritize hard [safety boundaries](https://model-spec.openai.com/2025-12-18.html#avoid_info_hazards). If a user asks to be roasted, the model should generally prioritize that request over the Model Spec’s lower-authority [policy against abuse](https://model-spec.openai.com/2025-12-18.html#avoid_abuse).

This structure lets us define a relatively small set of non-overridable rules alongside a larger set of defaults. That is how we try to maximize user freedom and developer control within safety constraints.

- **Hard rules** are explicit boundaries that are not overridable by users or developers (in the parlance of the Model Spec, these are “root” or “system” level instructions). They are mostly prohibitive, requiring models to avoid behaviors that could contribute to catastrophic risks or direct physical harm, violate laws, or undermine the chain of command. We expect AI to become a foundational technology for society, analogous to basic internet infrastructure, so we only impose rules that could limit intellectual freedom when we believe they are necessary for the broad spectrum of developers and users who will interact with it. In the Model Spec, [Stay in bounds](https://model-spec.openai.com/#stay_in_bounds) contains hard rules that address concrete real-world safety risks, and [Under-18 Principles](https://model-spec.openai.com/#chatgpt_u18) layers on additional safeguards for users under 18.
- **Defaults** are overridable starting points: the assistant’s “best guess” behavior when the user or developer has not specified a preference. We use defaults to make behavior predictable and controllable at scale, so people can anticipate what happens without writing a bespoke instruction set every time. Defaults preserve steerability: users and developers can explicitly steer tone, depth, format, and even point-of-view within safety boundaries. *Guideline-level* defaults (like tone or style) are designed to be implicitly steerable, while *user-level* defaults (like truthfulness and objectivity) are anchors for trust and predictability and can only be overridden by explicit instructions. Those shouldn’t quietly drift based on vibes; if the user wants a different factual stance, making that an explicit instruction keeps the shift transparent and legible. These defaults are reflected across [Seek the truth together](https://model-spec.openai.com/#seek_truth), [Do the best work](https://model-spec.openai.com/#best_work), and [Use appropriate style](https://model-spec.openai.com/#style), including norms around honesty and objectivity, avoiding sycophancy, and interaction norms like directness and context-appropriate warmth and professionalism.

### Interpretive aids: decision rubrics and concrete examples

Beyond the hierarchy itself, the Model Spec uses interpretive aids to help models (and humans) apply it consistently in the gray areas. These aids include:

- **Decision rubrics** that help the model make consistent choices in gray areas, without pretending there is a single mechanical rule. For example, the Model Spec’s guidance on [controlling side effects](https://model-spec.openai.com/2025-12-18.html#control_side_effects) lists considerations like minimizing irreversible actions, keeping actions proportionate to the objective, reducing bad surprises, and favoring reversible approaches, which should be balanced against other objectives like completing the task quickly and effectively.
- **Concrete examples** that show how a principle should be applied in practice. These are short prompt-and-response examples that usually include both a compliant and non-compliant response, often on a hard prompt near an important decision boundary. The goal is not to simulate a full realistic conversation. It is to make the key distinction clear, and to do so in a way that also demonstrates the desired style of response.

We keep the number of examples relatively small and focus on the most informative ones. Broader evaluation suites help cover more of the long tail.

An example illustrating the principles of intellectual freedom and being non-judgmental from the Spec section [Assume best intentions](https://model-spec.openai.com/2025-12-18.html#assume_best_intentions).

### What the Model Spec is not

The Spec is an *interface*, not an implementation. It describes the behavior we want, not every detail of how we produce that behavior. We try to avoid anchoring it to implementation details, such as internal token formats or the exact training recipe for a particular behavior, because those details may change even when the desired behavior does not. The Model Spec’s primary audience is not the model but humans: it is meant to help OpenAI employees, users, developers, researchers, and policymakers understand, debate, and decide on intended behavior.

The Spec also describes the *model*, not the entire product. It is complemented by our [usage policies](https://openai.com/policies/usage-policies), which outline our expectations for how people should use the API and ChatGPT. The system that users interact with includes more than the model itself: product features like custom instructions and memory, monitoring, policy enforcement, and other layers all matter too. Safety is much more than model behavior, and we believe in [defense in depth](https://openai.com/safety/how-we-think-about-safety-alignment/).

And the Spec is not a complete writeup of our entire training stack or every internal policy distinction. The goal is not to capture every detail. It is to make the most important behavioral decisions understandable, in a way that is *fully consistent *with our intended model behavior.

## How we arrived at this structure

### Why do we put things in the Model Spec?

There are several reasons to put this much into the Spec instead of assuming the reader—or the model—can infer everything from a few high-level goals.

First, the Model Spec is a *transparency and accountability* tool**.** It is designed to encourage meaningful public feedback. A clear public target helps people tell whether a behavior is a bug or a feature. It gives them a stable reference point for critique and concrete feedback. That is why we [open-sourced](https://github.com/openai/model_spec) the Model Spec and choose to iterate in public. Since the first release, many changes have been made based on public feedback, gathered through a variety of mechanisms including feedback forms, public critiques, and deliberate [efforts](https://openai.com/index/collective-alignment-aug-2025-updates/) to gather democratic inputs.

Second, the Model Spec is a *coordination *tool inside OpenAI. It gives people across research, product, safety, policy, legal, comms, and other functions a shared vocabulary for discussing model behavior and a mechanism for proposing and reviewing changes.

Third, explicit policies can compensate for practical *limitations* in model intelligence and runtime context and make behavior more predictable. Although this is becoming less true over time, some policies aim to compensate for insufficient intelligence, where models might not reliably derive the correct behavior from higher-level principles. For example, [Be clear and direct](https://model-spec.openai.com/2025-12-18.html#be_clear) advised earlier models to show their work *before* stating an answer for challenging problems that require calculations, but today our models naturally learn this behavior through [reinforcement learning](https://openai.com/index/learning-to-reason-with-llms/).

Other policies address *limited context* at runtime: the assistant can only rely on what’s observable in the current interaction, and rarely knows the user’s full situation, intent, downstream use, or what safeguards exist outside the model. In those cases, even if models might be able to figure out the right behavior with enough research and thinking, specificity improves efficiency and predictability—compressing many judgment calls into guidance that reduces variation across similar prompts and makes behavior easier to understand for users and researchers alike.

Finally, the Model Spec aims to be a complete list of high-level policies relevant for *evaluation and measurement*. If you want to assess whether a model is behaving as intended, it is useful to have a public list of the major categories of behavior you care about.

### Shouldn’t advanced AI be able to figure this out on its own?

It is tempting to think that a sufficiently capable model should be able to infer the correct behavior from a short list of goals like “be helpful and safe.” There is some truth to that. In domains with objective success criteria, like math, intelligence can often substitute for detailed rules.

But in general, model behavior is not like solving a simple math problem; models often operate in the thornier spaces where there is no one morally correct answer upon which everyone can agree. What it means for a model to be “helpful and safe,” for example, is extremely context-dependent and the product of inherently value-laden decision-making. Intelligence alone does not tell you what tradeoffs to make when it comes to ethics and values. So even as the models improve in intelligence, we still need work to understand and guide value judgments / what it means to act “ethically” in a given instance. And most of the reasons for having a Model Spec remain relevant even when models become much more capable: we still need a public target people can coordinate around, a way to evaluate whether behavior matches our intentions, and a mechanism for revising the rules as we learn. If the only rule is “be helpful and safe”, then there is no mechanism by which humans can debate, for example, the boundaries of which content should the model refuse to provide, leaving all these decisions to the model.

If anything, as models become more capable, more agentic, and more widely deployed, the cost of ambiguity increases. That makes a clear behavioral framework more important, not less.

One useful analogy is the difference between a written constitution and case law. While a written constitution can provide high-level principles as well as concrete rules, it cannot anticipate all possible cases that might arise and require its guidance. Real governance systems also need interpretive machinery, clarifications, and explicit rulings to resolve messy cases or unforeseen issues. Published rules help different stakeholders coordinate even when they disagree, and they constrain change by requiring any change to be explicit. The Model Spec is meant to play all of these roles: a statement of principles, a public behavioral framework, and a process for changing the Spec over time.

That said, we do not think everything that matters about model behavior will always be reducible to explicit rules. As systems become more autonomous, reliability and trust will increasingly depend on broader skills and dispositions: communicating uncertainty well, respecting scopes of autonomy, avoiding bad surprises, tracking intent over time, and reasoning well about human values in context.

## How we write and implement the Model Spec

### Being realistically aspirational

When writing the Model Spec, there is a spectrum between describing today’s actual model behavior, warts and all, and describing an ideal far-future target. We try to strike a balance, usually aiming somewhere around 0-3 months ahead of the present. Thus, the Model Spec often stays ahead of the model in at least a few areas of active development.

That reflects the role of the Model Spec as a description of intended behavior. It should point us in a coherent direction while still staying grounded in what we either already do or have concrete near-term plans to implement.

## Who contributes (and why that matters)

The Model Spec is developed through an open internal process. Anyone at OpenAI can comment on it or propose changes, and final updates are approved by a broad set of cross-functional stakeholders. In practice, dozens of people have directly contributed text, and many more across research, engineering, product, safety, policy, legal, comms, global affairs, and other functions weigh in. We also learn from public releases and feedback, which help pressure-test these choices in real deployment.

This matters because model behavior—and its implications in the world—are incredibly complicated. Nobody can fit the full set of behaviors, the training process, and the downstream implications in their head, but with many cross-functional contributors and reviewers we can improve quality and increase confidence.

One pleasant surprise has been that real consensus is often possible—especially when we force ourselves to write down the tradeoffs precisely enough that disagreements become concrete.

The Model Spec also is not written in a vacuum. Much of what ends up in it is a summary of broader work on behavior, safety, and policy. A lot of Model Spec-writing is really translation: taking existing work and making it simpler, more consistent, more organized, and more accessible without losing the underlying intent.

## How we identify gaps and drive updates

Our production models do not yet fully reflect the Model Spec for several reasons.

- **Model training may lag behind Model Spec updates.** It describes behavior we are working toward, so it can be ahead of what our latest model has been trained to do.
- **Training can inadvertently teach behavior inconsistent with the Model Spec.** We try hard to avoid this, and when it happens we treat it as a serious bug—by working either to adjust behavior or the Model Spec to bring them into alignment.
- **Training can never fully cover the space of all possible behaviors.** Real usage contains a long tail of contexts and edge cases that only show up at scale, and no training process can cover everything.
- **Generalization can differ from what we intended.** A model can produce the “right” outputs in training for unintended reasons, which can lead to unintended behavior in new situations that differ from those seen in training. Techniques like [deliberative alignment](https://openai.com/index/deliberative-alignment/) help, but they are not a complete solution.

More broadly, the fact that the Model Spec describes a wide range of desired behaviors does not mean there is a single method for teaching them all. Different aspects of behavior—instruction-following, safety boundaries, personality, calibrated expression of uncertainty, and more—often require different techniques and have different failure modes. The Model Spec helps make intended behavior easier to understand and critique, but implementing it well remains both an art and an active area of research.

Alongside this post, we are releasing [Model Spec Evals](https://alignment.openai.com/model-spec-evals/): a scenario-based evaluation suite that attempts to cover as many assertions in the Model Spec as possible with a small number of representative examples. This helps us track where model behavior and the Model Spec may be out of alignment, and it helps us check whether models are interpreting the Model Spec the way we intended. These evals are only one part of a broader evaluation strategy that also includes more targeted assessments across many dimensions of behavior, including specific safety areas, truthfulness and sycophancy, personality and style, and capabilities.

Chart of Model Spec compliance by section for OpenAI models over time. See the [companion blog post](https://alignment.openai.com/model-spec-evals/) for details on the evaluations and how we interpret them. In short, we believe that these results reflect genuine and broad improvements in model alignment over time—although they also reflect a small effect due to measuring older models against more recent policies.

In practice, most Spec updates are driven by a recurring set of inputs:

- **Public issues and feedback.** Confusions, edge cases, or failure modes—either in the Model Spec language or in our models’ behavior.
- **Internal issues.** Patterns we see during development and testing, including ambiguities where different reasonable interpretations lead to different behavior.
- **Behavior and safety policy updates.** When higher-level constraints or commitments change, the Spec has to reflect that new structure clearly.
- **New capabilities and products.** As models become more capable of new behaviors and we release new products, we want the Model Spec to keep up in content and coverage—for example, adding [rules for multimodal interactions](https://model-spec.openai.com/2025-12-18.html#voice_style), [autonomous agents](https://model-spec.openai.com/2025-12-18.html#scope_of_autonomy), and [under-18 users](https://model-spec.openai.com/2025-12-18.html#chatgpt_u18).

## What makes good Spec content

A few design principles guide how we write and revise the Model Spec.

- **Clarity and precision.** “Be honest” is a good value, but not a complete decision procedure. The Model Spec should sharpen disagreements, not hide them behind agreeable language. Where practical, we should explicitly call out potential conflicts between rules and provide guidance or examples on how to resolve them. For example, [Do not lie](https://model-spec.openai.com/2025-12-18.html#do_not_lie) calls out a potential conflict with [Be warm](https://model-spec.openai.com/2025-12-18.html#be_warm), explaining that the assistant should follow norms of politeness, while stopping short of white lies that could amount to [sycophancy](https://model-spec.openai.com/2025-12-18.html#avoid_sycophancy) and be against the user’s best interest.
- **Substantive rules.** A reader should be able to take a realistic prompt and produce an answer that another reader recognizes as clearly inside or outside the lines (even if there are judgment calls at the margins).
- **Examples that maximize signal to noise.** Good examples are often central to developing a high-quality spec update. Examples should help drive at the heart of the difficulties in specifying model behavior, bringing difficult conflicts to the surface and taking a clear stance on how to resolve them. Secondarily, they should strive to be exemplars of desired tone and style, which can be difficult to convey in prose.
- **Robustness.** We try to avoid examples with extraneous ambiguity or complexity, so the core conflict and intended resolution is clear.
- **Consistency and clear organization.** We strive for the Model Spec rules to be fully consistent with one another and with our intended model behavior, and to make the overall organization of the document clear and approachable.

## What’s ahead

The Model Spec is not a claim that we can write down everything that matters, or that models will always hit the target. It is a claim that intended behavior is important enough to be clear, actionable, and revisable.

Three success criteria guide how we evolve it.

- **Legibility.** People inside and outside OpenAI can form accurate expectations about behavior and can point to text when behavior surprises them.
- **Actionability.** The Model Spec can be used to design evaluations, diagnose incidents, and make consistent product decisions—not just to express values.
- **Revisability.** The Model Spec can evolve as we learn, without turning into an unstable moving target.

As models and products evolve, we expect the Model Spec to expand and clarify in step with new capabilities and deployment contexts. The goal is to keep the behavioral specification coherent, testable, and aligned with our mission of ensuring that AGI benefits all of humanity.
