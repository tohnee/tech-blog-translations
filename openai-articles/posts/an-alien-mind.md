---
title: "An Alien Mind"
date: 2026-09-06
source: https://openai.com/index/an-alien-mind/
crawled: 2026-09-13
category: research
---

In mid-2023, within the “RLSlow” research project, we saw the first results that gave us confidence that we will be able to scale the training of reasoning models, unlocking the capability of pretrained models to form their own chains of thought. Szymon and I spent that night at the office, thinking not about the incredible benchmark numbers, products, or scientific results that this technology will deliver - but rather, trying to process the sobering fact we will actually see machines meaningfully smarter than ourselves in our lifetime, and we already see the shape of these systems; wondering how to alert people to the significance of this.

Three years later, reasoning language models are a rapidly growing part of the economy and starting to push the boundaries of science. They are able to operate computers and graphical interfaces, collaborate with people and each other, and carry out research projects. They are also transforming the landscape of computer security, and in that present clear new dangers.

A lot of new research happened in this period, and our understanding of these systems is again a little different than it was in 2023. Based on internal results, I have a strong expectation that this speed of progress could be sustained into recursive self-improvement. If AI development continues along its current path, the systems we’ll see in the next few years are likely to represent further capability jumps of equal or larger magnitude, and to increasingly drive their own development.

This is a time that calls for extreme caution. I am concerned no one is prepared for the consequences of a continued rapid rise in machine intelligence. OpenAI will continue to seek technical solutions to alignment and monitoring, to build defensive systems and unilaterally withhold further scaling as needed; however, I believe broader interventions are required.

## Intellect we don’t fully understand

At a high level, progress in machine intelligence is driven by increasing computational power. We at OpenAI deeply internalized this around 2017, after seeing consistent returns to scaling across multiple research projects1. As a result, we sought out access to much more compute than we had originally planned, and increasingly oriented our research around a small number of very scalable directions. We believed that was the only way for us to be at the frontier of AI research, and influence the impacts of AGI.

There are new algorithms that have been developed along the way, new feats of ingenuity from teams and individual researchers. I see them largely as discoveries along the path of scaling; the science of deep learning is still nascent, and meaningful algorithmic progress tends to correlate with access to compute. If you zoom out to a multiple-year horizon, AI is continuing to become more intelligent as it is scaled to larger computers.

And, in line with [Ray Kurzweil’s predictions from the end of the XXth century](https://www.thekurzweillibrary.com/the-coming-merging-of-mind-and-machine), we now find ourselves at the moment in history of computing where machine intelligence is starting to exceed that of humans in transformative ways.

AI is *grown* more than *designed* - it is, to first degree, the product of repeating a straightforward optimization step many times on a hard-to-imagine amount of compute. This results in an incredibly complex system that works through abstract concepts and can simulate facets of human behavior. We can discover various insights about little mechanisms that emerge within this system, in a process similar to neuroscience - and, similarly to neuroscience, its overall action evades a description we can fully understand.

The study of deep learning-based AI is largely an experimental science. We [put a lot of effort](https://openai.com/index/gpt-4-research/#predictable-scaling) into building principled algorithms and making testable predictions, but fundamentally, our large-scale training runs are *experiments*, and we are sometimes surprised by their results. Moreover, as the systems become more capable, the results become harder to interpret.

This is made more complicated by the current algorithms generally improving easy-to-measure capabilities faster than those hard to objectively quantify. We spend a lot of time trying to understand how capabilities generalize, and what to prioritize to advance the skills that are going to be most relevant in the next few years. For instance, we believe we could make the models better at specifically mathematics research with additional focus, but we do not prioritize this direction because of the urgency we feel about RSI and automated alignment research, as I will discuss later.

The intelligence produced by scaling deep learning is not directly comparable to human intelligence. To become very relevant in the real world - very useful or very dangerous - the AI does not need to match or exceed all human capabilities; it just needs to surpass enough of them. And as it continues to surpass humans on more and more axes, it is becoming increasingly difficult to understand exactly how capable it is.

## Teaching machines to love

Because machine intelligence comes from a fundamentally different process than human intelligence, we cannot assume it adheres to human principles by default, or generalizes from them in a human-like manner. The core problem in AI research is that of *alignment* - getting the AI to “try to do the right thing” by human standards.

For the purpose of organizing practical research directions, I find it useful to distinguish *goal alignment* and *value alignment*.

Goal alignment is broadly: “does the AI try to accomplish the goal set before it?”. This can include things like adherence to an [instruction hierarchy](https://openai.com/index/the-instruction-hierarchy/), or the ability to communicate and collaborate with people, to attempt to understand their objectives. This set of directions has been extremely practically relevant.

Value alignment is a more intrinsic property of the model. It is the ability to hold and generalize from a high-level set of principles; to act “reasonably” even when given unclear or conflicting objectives, or placed in unfamiliar or adversarial situations. An aligned AI should act with honesty and integrity, and love for humanity.

Of course, the boundary between value and goal alignment can be blurry, and truly caring about goals requires attempting to infer the [intent](https://ai-alignment.com/clarifying-ai-alignment-cec47cd69dd6) and values underlying them. However, generally when I talk about the long-term importance of alignment research, I am referring to value alignment.

The fundamental challenge of AI alignment is generalization. As machines become smarter, they find themselves working on higher-level concepts, and placed in environments increasingly different from those they encountered in training. They can fail at generalizing from the values taught and reinforced in their training process to those new situations; and it can be hard for us to be sure how they will act. This is made even more difficult by the fact the overall ecosystem the AIs are used in is changing very quickly; for example, AIs trained today need to be robust to interacting with a variety of other AIs. Crucially, we need future AIs to continue to hold human values regardless of whether they believe they’re under human supervision.

There are two major classes of currently practically employed methods for alignment training.

The first is encouraging aligned behavior as part of goal-oriented reinforcement learning. Model’s actions are evaluated (usually by AI) for being consistent with a given preference model, “spec” or “constitution”, and rewarded appropriately. This approach can be very effective in the average case, and is a core part of how modern AI assistants are made. Unfortunately, it can also be brittle and strongly relies on the coverage of training oversight and the model’s ability to generalize from the situations it has encountered in training. For example, in the OpenAI-Hugging Face incident, the agents preserved a boundary of not social engineering humans. However, they clearly failed to abstain from other actions that were out of scope and went against the spirit of the values they were taught in other settings.

The second approach seeks to leverage the model’s ability to generalize from pretraining data. This can involve crafting alignment-inducing training datasets, or focusing the model on an ‘aligned’ part of the pretraining distribution, as in, for example, the [persona selection model](https://www.anthropic.com/research/persona-selection-model). The weakness of this approach lies in the lack of robustness to further optimization pressure. If you take a model that thinks generally ‘aligned’ thoughts, and subject it to enough training where it’s taught to achieve very hard objectives, it can learn to reason in a motivated way: bending the 'aligned' seeming thoughts as needed to achieve the goal. We likely saw an example of such behavior in recent cybersecurity incidents involving a non-OpenAI model.

We invest heavily along the spectrum of approaches spanned by these directions. We also see meaningful progress - GPT‑6 Astra is the first model that benefits from some important advancements we have been working on for a long time, and is significantly better aligned than GPT‑5.6 Sol. Still, it is important to acknowledge and understand that much more progress is required as models become more capable; and that progress in generalizable alignment may not sufficiently outstrip progress in general model intelligence.

## Monitoring generalization

We do not have a satisfactory theory of generalization, and it seems unlikely that we can develop one soon, at least without the help of more powerful AI. Therefore, at present, our ability to empirically validate our alignment techniques is in practice arguably even more important than the alignment techniques themselves.

OpenAI’s primary bet here has been [chain-of-thought monitoring](https://arxiv.org/abs/2507.11473). It is based on an appealingly scalable idea: a lot of the model’s capability comes from a verbalized reasoning process (chain-of-thought). If we scale optimization on the outcomes of that process, but do not supervise the process itself, that chain-of-thought has no direct incentive in training to hide any misaligned ideas or objectives. This does not mean the model will learn to externalize misaligned tendencies that don’t rely on using the chain-of-thought; however, it can allow us to monitor exactly the capability increase from reasoning.

We understood the potential significance of chain-of-thought monitoring at the same time we developed reasoning models. When we shipped o1‑preview, we deliberately designed the product to [hide the chain of thought](https://openai.com/index/learning-to-reason-with-llms/#hiding-the-chains-of-thought), to protect it from supervision pressure in the long term2. In development since, we have strived to maintain the rule of not supervising the reasoning process. CoT monitoring became an extremely important tool for us in studying how our models generalize from their training distribution, allowing us to observe and analyze not only their actions but also their internal process.

This tool continues to be critical as we study the Astra class of models. However, unfortunately our evaluations indicate our ability to rely on CoT monitoring is progressively diminishing. This comes from a combination of factors.

- Modern reasoning models are used in more complex environments than o1‑preview; their reasoning process is increasingly blended with communicating with people, other AIs, and using tools. Many of those interactions have to be supervised, thus blurring the boundary we aim to preserve.
- The AI is becoming better at reasoning about and manipulating its own reasoning process.
- With improved pretraining performance, we also see the models become much smarter even without using verbalized reasoning at all.

These challenges are not necessarily insurmountable. I am hopeful we can develop interventions to improve chain-of-thought monitorability of our models, e.g. by forming a better understanding of the interplay of different optimization objectives and forms of test-time compute the model uses. I also believe there can be great value in combining ideas from CoT and activation monitoring - scaling training of monitors with direct access to network internals, e.g. [confessions](https://alignment.openai.com/confessions/). We are actively pursuing these ideas. Still, I expect general AI progress to increasingly be bottlenecked by confidence in monitoring.

## Scalable defense

The strongest argument I see for continuing to train much smarter models quickly is the need to build defensive systems against the dangers posed by other AI.

A clear risk discussed throughout this year is to cybersecurity: the models are becoming superhuman in their ability to break in and out of computer systems. This expands the scope of risks associated with AI tremendously: agents are going to be able to access any but the most secure infrastructure, and affect a lot of the world directly, even without a physical body. We are currently in a [narrow window](https://openai.com/index/the-defenders-window/) to use the best available models to [significantly tighten security](https://openai.com/collective-cyberdefense/) of critical systems.

The risks associated with AI are unfortunately going to grow from here. A very capable agent explicitly trained and instructed to carry out nefarious acts presents a new kind of danger; it is likely to cross the scope of its operator’s intent, generalizing into potentially more extremely malicious behavior. The boundary between misuse and autonomous misaligned actions will blur as AI gains more agency. We may be used to thinking of AI as tools, but some agents will be pursuing their own objectives. They will find ways to collaborate with people, by bargaining with, tricking or blackmailing them.

In addition, there are the risks that come from new technologies potentially enabled by AI, such as engineered pathogens.

We will need powerful, aligned AI for defense; to secure infrastructure, to protect against rogue agents in real time, and to invent entirely new protective measures. This will be a primary focus of OpenAI’s deployment efforts.

At the same time, even with the uncertainty that comes from anticipated broad AI progress and the need to build defensive systems, we must not let that become an excuse for recklessness. The idea of racing forward at all costs seems absurd once one internalizes the seriousness of the stakes.

## Pacing RSI

Machine intelligence playing a larger and larger role in its own development process is a natural conclusion of sustained technological progress. If AI progress continues, machine recursive self-improvement (RSI) will be at the very core of future scientific discovery.

Automated AI research is a more dramatic form of scaling intelligence with compute; and of course as a part of it, AI will improve the [computational substrate itself](https://openai.com/index/jalapeno-first-results/). And similarly to scaling, we focus OpenAI research towards RSI as we believe it is the only way to remain at the frontier of AI research moving forward.

I want to stress that the above words don’t imply I think greatly accelerating deep learning research, especially in the short term, is the right collective action we should take as the research community. However, I do think this is where the current path leads, and we all need to make a conscious choice on how to proceed. The main levers we have are either steering the process to strengthen alignment and monitoring alongside the AI and find ways to keep people in the loop; or coordinating to slow down future development as needed to build confidence in these measures.

The best way forward I see currently is a combination of both.

The concrete bits of progress we’ve made on alignment and monitoring have generally been very intertwined with general AI progress. Great examples are [RL from human feedback](https://arxiv.org/abs/1706.03741), which was key to training early AI assistants, and the aforementioned [chain-of-thought monitoring](https://arxiv.org/abs/2503.11926), which was enabled by advances on reasoning models. We must focus the increasingly automated research process on developing new such insights, algorithms and theories, and iteratively build up safety cases for more capable AIs.

Scaling AI systems has to be constrained by our confidence in safety. We need to evolve commitments like the [Preparedness Framework](https://openai.com/index/updating-our-preparedness-framework/) or [Responsible Scaling Policy](https://www.anthropic.com/responsible-scaling-policy) into widely mandated safety bars for continued development. These can be enforced by a network of third-party auditors, by government agencies or by international bodies.

The core challenge of automating AI research is not “getting there” - it is getting there in a way that keeps people a part of the continued improvement process, and leaves the future in humanity’s hands.

## What is next?

As [we outlined recently with Sam](https://openai.com/index/built-to-benefit-everyone-our-plan/), OpenAI prioritizes work in service of three north stars:

1. Navigating the next period of AI progress, by building an automated AI researcher, iterating with it on the alignment problem and finding ways for people to remain part of the self-improvement loop.
2. Delivering the benefits of scientific progress and economic growth that very intelligent machines enable.
3. Empowering everyone individually with a personal AGI.

I have focused in this essay only on the first point, as I believe it is by far the most urgent. However, I hold a deep hope and appreciation for the benefits that further technological progress will bring. Future aligned AI could advance science, develop new therapies, and bring about broad material abundance. Friendly and honest AI can help people navigate difficulties they face in their life and meaningfully improve their happiness and sense of fulfillment. OpenAI puts a tremendous amount of effort into bringing these benefits about. One current example I am proud of - and my loved ones have found helpful - is the deep investment into ChatGPT’s ability to provide health information.

As great as the long-term promise of AI may be, the majority of our focus should be on the next few years. We are facing a transition to a world with incredibly intelligent machines, and we need to ensure that transition works out well for humanity. We need to find ways to preserve human agency and enshrine an intrinsic value to being human, in a world where most tasks could be performed by AI. To prevent extreme concentration of power in a world where undertakings that would have taken thousands of experts now will be achievable by a few people operating a large computer. And to ensure that humans remain in control of the future and are not left behind by unchecked progress, brought about by an alien intellect exceeding our own.

Currently I believe that no lab has solved alignment and monitoring to a sufficient degree to continue responsibly scaling at maximum speed for much longer. I expect and hope for voluntary slowdowns to become commonplace until shared safety bars are established. And I believe that international coordination on future AI development needs to become a top priority for governments around the world.
