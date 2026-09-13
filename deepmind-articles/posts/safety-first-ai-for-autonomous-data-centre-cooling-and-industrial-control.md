---
title: "Safety-first AI for autonomous data centre cooling and industrial control"
source: https://deepmind.google/blog/safety-first-ai-for-autonomous-data-centre-cooling-and-industrial-control/
site: deepmind
date: 2018-08-17
authors: Chris Gamble, Jim Gao
crawled: 2026-09-13
---

Many of society’s most pressing problems have grown increasingly complex, so the search for solutions can feel overwhelming. At DeepMind and Google, we believe that if we can use AI as a tool to discover new knowledge, solutions will be easier to reach.

In 2016, we jointly developed an [AI-powered recommendation system](https://deepmind.com/blog/article/deepmind-ai-reduces-google-data-centre-cooling-bill-40) to improve the energy efficiency of Google’s already highly-optimised data centres. Our thinking was simple: even minor improvements would provide significant energy savings and reduce CO2 emissions to help combat climate change.

Now we’re taking this system to the next level: instead of human-implemented recommendations, our AI system is directly controlling data centre cooling, while remaining under the expert supervision of our data centre operators. This first-of-its-kind cloud-based control system is now safely delivering energy savings in multiple Google data centres.

## How it works

Every five minutes, our cloud-based AI pulls a snapshot of the data centre cooling system from thousands of sensors and feeds it into our deep neural networks, which predict how different combinations of potential actions will affect future energy consumption. The AI system then identifies which actions will minimise the energy consumption while satisfying a robust set of safety constraints. Those actions are sent back to the data centre, where the actions are verified by the local control system and then implemented.

![Every five minutes, our cloud-based AI pulls a snapshot of the data centre cooling system as represented by thousands of physical sensors.](https://lh3.googleusercontent.com/0u87s3Hmu328SX5o5WysUdebSgB7O5VsLslrh4Y-5B7o9XEVRHydVwywUpGxZawCRaJR-0A5CfNADcBjQl8078ui4F4UF_af6YjYnIOiBPBCS8nSqus=w1440)

![The information is fed into our deep neural networks, which predict the future energy efficiency and temperature based on proposed actions.](https://lh3.googleusercontent.com/pJPaHFVd8tqwC3P04djE-pvBPwsu1YNOYOG_vj13IcNW6FtpDEin1zd3DvEFh3IOi-9cIbEihwf8N6sbUttpiLDWJBwurJCRFZclZ5ndMCRVsR4lcw=w1440)

![The AI selects actions that satisfy safety constraints and minimise future energy consumption.](https://lh3.googleusercontent.com/g-0Xb_Ky85xmxKNCqTI1YeMNydKIQ1deGvhm3WgDMfiaEcqBblMBXrND0qepkMZNfcKeZlLv_VzPrKTKMQQSoqZbwOhNZZJ8GR2mhicxEK4xDOd7Gg=w1440)

![Optimal actions are sent back to the data centre, where the local system verifies them against its own safety constraints before implementation.](https://lh3.googleusercontent.com/iN32ajXdFb8a4Q-Rj7efUkmLL27f0fgKA0xwzJbEQNfzC7zSzWbO4yzITRvEKdBqw6M8W_pSaoHcfDYRFEaakT0_Ss2fI_PfINNIrax1DrfogN8dyuQ=w1440)

The idea evolved out of feedback from our data centre operators who had been using our AI recommendation system. They told us that although the system had taught them some new best practices—such as spreading the cooling load across more, rather than less, equipment—implementing the recommendations required too much operator effort and supervision. Naturally, they wanted to know whether we could achieve similar energy savings without manual implementation.

We’re pleased to say the answer was yes!

## Designed for safety and reliability

Google's data centres contain thousands of servers that power popular services including Google Search, Gmail and YouTube. Ensuring that they run reliably and efficiently is mission-critical. We've designed our AI agents and the underlying control infrastructure from the ground up with safety and reliability in mind, and use eight different mechanisms to ensure the system will behave as intended at all times.

![An overhead view of a vast Google data centre filled with rows of servers and overhead cooling infrastructure.](https://lh3.googleusercontent.com/KnVOqqkDQFl8lhedIsVxOCoxHcA8mSxxwfvvjIeRcs1M5MPFLqDVFDOITFhDatN582sB5_0Iwy0m4eKaPxPSOtVMpBH2TCiOpkaslBhff1heeN65kA=w1440)

One simple method we’ve implemented is to estimate uncertainty. For every potential action—and there are billions—our AI agent calculates its confidence that this is a good action. Actions with low confidence are eliminated from consideration.

Another method is two-layer verification. Optimal actions computed by the AI are vetted against an internal list of safety constraints defined by our data centre operators. Once the instructions are sent from the cloud to the physical data centre, the local control system verifies the instructions against its own set of constraints. This redundant check ensures that the system remains within local constraints and operators retain full control of the operating boundaries.

Most importantly, our data centre operators are always in control and can choose to exit AI control mode at any time. In these scenarios, the control system will transfer seamlessly from AI control to the on-site rules and heuristics that define the automation industry today.

Find out about the other safety mechanisms we’ve developed, below:

![Continuous monitoring to ensure that the AI control system does not violate safety constraints. Automatic failover to a neutral state if the AI control system does violate the safety constraints. Smooth transfer during failovers to prevent sudden changes to the system. Two-layer verification of the AI actions before implementation. Constant communication between the cloud-based AI and the physical infrastructure. Uncertainty estimation to ensure we only implement high confidence actions.  Rules and heuristics as backup if we need to exit AI control mode.Human override is always available and will supersede any AI actions.](https://lh3.googleusercontent.com/H64NVqQM9X4R3x3vKz7k8gM-fK98hxJC6MP7zga9jA6dCN3qsS0reapSKxBwS8iIS8TSBYpS9gKjYmJX9ZG0l5isAB9Hpf3d_dWZBYeAydzq1zaRYg=w1440)

## Increasing energy savings over time

Whereas our original recommendation system had operators vetting and implementing actions, our new AI control system directly implements the actions. We’ve purposefully constrained the system’s optimisation boundaries to a narrower operating regime to prioritise safety and reliability, meaning there is a risk/reward trade off in terms of energy reductions.

Despite being in place for only a matter of months, the system is already delivering consistent energy savings of around 30 percent on average, with further expected improvements. That’s because these systems get better over time with more data, as the graph below demonstrates. Our optimisation boundaries will also be expanded as the technology matures, for even greater reductions.

![A dual-axis line graph plotting performance and training data metrics from September 2017 to July 2018. The left vertical axis measures "Improvement vs historical performance" from -35 to -5, while the right vertical axis measures "Number of training examples" from 0 to 90 million. A green line representing "Trailing twelve-month AI performance" steadily decreases from approximately -12 to -29 over the time period, shown with a light-green shaded variance band. Conversely, a blue line representing "Training data" shows a steady linear increase over the same period, rising from roughly 12 million to over 80 million training examples.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/622690d2f1f3943175d607a4_DC206.gif)

This graph plots AI performance over time relative to the historical baseline before AI control. Performance is measured by a common industry metric for cooling energy efficiency, kW/ton (or energy input per ton of cooling achieved). Over nine months, our AI control system performance increases from a 12 percent improvement (the initial launch of autonomous control) to around a 30 percent improvement.

Our direct AI control system is finding yet more novel ways to manage cooling that have surprised even the data centre operators. Dan Fuenffinger, one of Google’s data centre operators who has worked extensively alongside the system, remarked: "It was amazing to see the AI learn to take advantage of winter conditions and produce colder than normal water, which reduces the energy required for cooling within the data centre. Rules don’t get better over time, but AI does."

We’re excited that our direct AI control system is operating safely and dependably, while consistently delivering energy savings. However, data centres are just the beginning. In the long term, we think there's potential to apply this technology in other industrial settings, and help tackle climate change on an even grander scale.
