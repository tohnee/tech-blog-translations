---
title: "Real-world challenges for AGI"
source: https://deepmind.google/blog/real-world-challenges-for-agi/
site: deepmind
date: 2021-11-02
authors: Koray Kavukcuoglu
crawled: 2026-09-13
---

**Note: This post is a summary of a talk given at CERN Sparks! Serendipity Forum in September 2021, which can be viewed** [**here**](https://www.youtube.com/watch?v=EKozG-B9mkI)**.**

When people picture a world with artificial general intelligence (AGI), robots are more likely to come to mind than enabling solutions to society’s most intractable problems. But I believe the latter is much closer to the truth. AI is already enabling huge leaps in tackling fundamental challenges: [from solving protein folding](https://deepmind.com/blog/article/putting-the-power-of-alphafold-into-the-worlds-hands) to [predicting accurate weather patterns](https://deepmind.com/blog/article/nowcasting), scientists are increasingly using AI to deduce the rules and principles that underpin highly complex real-world domains - ones they might never have discovered unaided.

Advances in AGI research will supercharge society’s ability to tackle and manage climate change - not least because of its urgency but also due to its complex and multifaceted nature.

## Taking control

Looking across the field of AI research today, there are two common categories of problems scientists are focused on: prediction and control. Prediction models try to learn about a domain (such as weather patterns) and understand how it might evolve, while control models prompt agents to take actions in that environment. Building a successful path to AGI requires understanding and developing algorithms in both spaces, accounting for all the variations that our natural and social environments throw at us, from how viruses mutate or how language may evolve in use and meaning over time to how to help produce energy from fusion power. Two real-world domains that scientists at DeepMind are contributing to tackle climate change while developing what’s required to build AGI are weather prediction and plasma control for fusion.

Weather patterns are almost impossible to precisely model - it’s an example of nature’s variations at its fullest. However, causes and effects can be inferred based on vast amounts of historical data. Transferring the same generative models that are used to generate images and video clips into learning weather patterns in collaboration with the [Met Office](https://www.metoffice.gov.uk/) (UK’s national meteorological service), scientists at DeepMind have developed systems that can take 20 minutes of weather data to generate multiple hypotheses for radar maps and [accurately predict heavy rainfall](https://deepmind.com/blog/article/nowcasting) in the next 90 minutes.

Critically, these models will help meteorologists provide forecasts that aid decision making for emergency services, energy management, and activation of flood warning systems - enabling better preparation for and responses to extreme weather events, which have become increasingly common around the world. Helping predict important weather events by forecasting accurate weather patterns is one example of how AI research can make a meaningful impact as it becomes more generally applicable and ‘intelligent’.

## Global challenges

Beyond responding to the effects of climate change, solving its sources is of equal if not greater importance. Fusion, a single source of energy that is clean, limitless, and self-sustaining, is elusive, yet remains one of the world’s most promising solutions - one that I believe requires developing a general algorithm that can solve many different components at once. Already we are seeing progress in one component, the extremely challenging problem of maintaining novel plasma shapes to enable better energy output and stability of the plasma for as long as possible.

By working with world-renowned experts at the [Swiss Plasma Center](https://www.epfl.ch/research/domains/swiss-plasma-center/) and [École polytechnique fédérale de Lausanne](https://www.epfl.ch/en/) (EPFL), we are able to go beyond today’s hand crafted models, applying deep reinforcement learning algorithms first developed for robotics to plasma control. The result is a controller that can successfully manipulate different plasma shapes and configurations at 10,000 interactions per second.

Without expert collaboration, AI researchers cannot make significant progress in real-world domains. Identifying the right paths forward in these fields requires partnerships across disciplines, leveraging a common scientific approach to develop and use AI to navigate complex questions at the heart of society’s most urgent needs. It’s why dreaming together with a diversity of natural and social scientists about what a world with AGI could look like is so critically important.

As we develop AGI, addressing global challenges such as climate change will not only make crucial and beneficial impacts that are urgent and necessary for our world, but also advance the science of AGI itself. Many other categories of AGI problems are yet to be solved - from causality, to learning efficiently and transfer - and as algorithms become more general, more real-world problems will be solved, gradually contributing to a system that one day will help solve everything else, too.
