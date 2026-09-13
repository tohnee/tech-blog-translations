---
title: "Open-sourcing Psychlab"
source: https://deepmind.google/blog/open-sourcing-psychlab/
site: deepmind
date: 2018-01-26
authors: Joel Leibo
crawled: 2026-09-13
---

Consider the simple task of going shopping for your groceries. If you fail to pick-up an item that is on your list, what does it tell us about the functioning of your brain? It might indicate that you have difficulty shifting your attention from object to object while searching for the item on your list. It might indicate a difficulty with remembering the grocery list. Or it could it be something to do with executing both skills simultaneously.

![Cartoon illustration of supermarket shelves stocked with colorful groceries and price tags.](https://lh3.googleusercontent.com/OUNT_RkjJtzrsGCubJebiNItSX1f2_84kmW_ld9xWGAPVCbmbmpziQ72mIm2N9kOpHYoocnuGAntJzY-JHdigwSwRKkQDuhDb9EW2PkDgpqI17Pfcg=w1440)

What appears to be a single task actually depends on multiple cognitive abilities. We face a similar problem in AI research, where the complexity of a task can often make it difficult to tease apart the individual skills required for an agent to be successful. But understanding an agent’s specific cognitive skill set may prove useful for improving its overall performance.

To address this problem in humans, psychologists have spent the last 150 years designing rigorously controlled experiments aimed at isolating one specific cognitive faculty at a time. For example, they might analyse the supermarket scenario using two separate tests - a “visual search” test that requires the subject to locate a specific shape in a pattern could be used to probe attention, while they might ask a person to recall items from a studied list to test their memory.

We believe it is possible to use similar experimental methods to better understand the behaviours of artificial agents. That is why we developed Psychlab, a platform built on top of [DeepMind Lab](https://deepmind.com/blog/article/open-sourcing-deepmind-lab), which allows us to directly apply methods from fields like cognitive psychology to study behaviours of artificial agents in a controlled environment. Today, we are also open-sourcing this platform for others to use.

Psychlab recreates the set-up typically used in human psychology experiments inside the virtual DeepMind Lab environment. This usually consists of a participant sitting in front of a computer monitor using a mouse to respond to the onscreen task. Similarly, our environment allows a virtual subject to perform tasks on a virtual computer monitor, using the direction of its gaze to respond. This allows humans and artificial agents to both take the same tests, minimising experimental differences. It also makes it easier to connect with the existing literature in cognitive psychology and draw insights from it.

Along with the open-source release of Psychlab we have built a series of classic experimental tasks to run on the virtual computer monitor, and it has a flexible and easy-to-learn API, enabling others to build their own tasks.

- [Visual search](https://youtu.be/54AS3a6niPo)–tests ability to search an array of items for a target.
- [Continuous recognition](https://youtu.be/rPlARM2KCuM)–tests memory for a growing list of items.
- [Arbitrary visuomotor mapping](https://youtu.be/385WgV-7fbw)–tests recall of stimulus-response pairings.
- [Change detection](https://youtu.be/p10hRvFquqU)–tests ability to detect changes in an array of objects reappearing after a delay.
- [Visual acuity and contrast sensitivity](https://youtu.be/m194hJJWwZE)–tests ability to identify small and low-contrast stimuli.
- [Glass pattern detection](https://youtu.be/KG0pO3U_EH8)–tests global form perception.
- [Random dot motion discrimination](https://youtu.be/HuNMXq-AjjE)–tests ability to perceive coherent motion.
- [Multiple object tracking](https://youtu.be/G4X5yeGCcyM)–tests ability to track moving objects over time.

Each of these tasks have been validated to show that our human results mirror standard results in the cognitive psychology literature.

Take the ‘visual search’ task for example. The ability to locate an object among a complex array of stimuli, like one item on a supermarket shelf, has been studied as a way of understanding selective attention in humans.

When humans are given the task of searching `for a vertically oriented bar among horizontal bars’ and ‘searching for a pink bar among bars of other colours’ their reaction times don’t change according to the numbers of items on the screen. In other words, their reaction times are independent of 'set size'. However, when the task is to search for a pink bar among different shaped and different coloured bars, human reaction times increase by approximately 50ms with each additional bar. When humans did this task on Psychlab, we replicated this result.

![Three diagrams and line graphs comparing response times of humans (red) and artificial agents (blue) across three visual search tasks: "Orientation Search," "Colour Search," and "Conjunction Search." While artificial agents maintain a flat response time across all set sizes, human response times remain flat for orientation and colour searches but increase with set size during conjunction search.](https://lh3.googleusercontent.com/1AN2JnR2iRFdcICpdi1HUf6BLZp62cgkymf5zncus9KEdVjwuC2nKwpGHenAxt3rxRmhrivsIJQnPTzWOcr4LM40zpgdbrobfDHwGM-SOusagAyidg=w1440)

When we did the same test on a state-of-the-art artificial agent, we found that, while it could perform the task, it did not show the human pattern of reaction time results. It used the same amount of time to respond in all three cases. In humans, this data has suggested a difference between [parallel and serial attention](http://search.bwh.harvard.edu/new/pubs/FiveFactors_Wolfe-Horowitz_2017.pdf). Agents appear only to have parallel mechanisms. Identifying this difference between humans and our current artificial agents shows a path toward improving future agent designs.

Psychlab was designed as a tool for bridging between cognitive psychology, neuroscience, and AI. By open-sourcing it, we hope the wider research community will make use of it in their own research and help us shape it going forward.

**Notes**

[Read the paper](https://arxiv.org/abs/1801.08116).

[Download the code on GitHub](https://github.com/deepmind/lab/tree/master/game_scripts/levels/contributed/psychlab).
