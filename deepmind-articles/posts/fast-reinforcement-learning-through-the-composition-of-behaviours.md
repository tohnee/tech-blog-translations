---
title: "Fast reinforcement learning through the composition of behaviours"
source: https://deepmind.google/blog/fast-reinforcement-learning-through-the-composition-of-behaviours/
site: deepmind
date: 2020-10-12
authors: André Barreto, Shaobo Hou, Diana Borsa, David Silver, Doina Precup
crawled: 2026-09-13
---

## The compositional nature of intelligence

Imagine if you had to learn how to chop, peel and stir all over again every time you wanted to learn a new recipe. In many machine learning systems, agents often have to learn entirely from scratch when faced with new challenges. It’s clear, however, that people learn more efficiently than this: they can combine abilities previously learned. In the same way that a finite dictionary of words can be reassembled into sentences of near infinite meanings, people repurpose and re-combine skills they already possess in order to tackle novel challenges.

In nature, learning arises as an animal explores and interacts with its environment in order to gather food and other rewards. This is the paradigm captured by [reinforcement learning](http://incompleteideas.net/book/the-book-2nd.html) (RL): interactions with the environment reinforce or inhibit particular patterns of behavior depending on the resulting reward (or penalty). Recently, the combination of RL with [deep learning](https://www.nature.com/articles/nature14539) has led to impressive results, such as agents that can learn how to play boardgames like [Go](https://deepmind.com/blog/article/alphazero-shedding-new-light-grand-games-chess-shogi-and-go) and [chess](https://arxiv.org/abs/1911.08265), the full spectrum of [Atari](https://deepmind.com/blog/article/Agent57-Outperforming-the-human-Atari-benchmark) games, as well as more modern, difficult video games like [Dota](https://openai.com/projects/five/) and [StarCraft II](https://deepmind.com/blog/article/alphastar-mastering-real-time-strategy-game-starcraft-ii).

A major limitation in RL is that current methods require vast amounts of training experience. For example, in order to learn how to play a single Atari game, an RL agent typically consumes an amount of data corresponding to several weeks of uninterrupted playing. A [study](http://gershmanlab.webfactional.com/pubs/Tsividis17.pdf) led by researchers at MIT and Harvard indicated that in some cases, humans are able to reach the same performance level in just fifteen minutes of play.

One possible reason for this discrepancy is that, unlike humans, RL agents usually learn a new task from scratch. We would like our agents to leverage knowledge acquired in previous tasks to learn a new task more quickly, in the same way that a cook will have an easier time learning a new recipe than someone who has never prepared a dish before. In [an article](https://www.pnas.org/content/early/2020/08/13/1907370117) recently published in the Proceedings of the National Academy of Sciences (PNAS), we describe a framework aimed at endowing our RL agents with this ability.

## Two ways of representing the world

To illustrate our approach, we will explore an example of an activity that is (or at least used to be) an everyday routine: the commute to work. Imagine the following scenario: an agent must commute every day from its home to its office, and it always gets a coffee on the way. There are two cafes between the agent's house and the office: one has great coffee but is on a longer path, and the other one has decent coffee but a shorter commute (Figure 1). Depending on how much the agent values the quality of the coffee versus how much of a rush it is in on a given day, it may choose one of two routes (the yellow and blue paths on the map shown in Figure 1).

![An illustrative map showing three routes from "Home" to "Office": a blue path passing through "Cafe A" (3-star coffee, 5-star food), a yellow path passing through "Cafe B" (5-star coffee, 3-star food), and an orange path that goes from "Home" through "Park" to "Cafe A," then connects to "Cafe B" before reaching the "Office."](https://lh3.googleusercontent.com/94uCFjigjYHUt5vLxw50vU2PvgaflGrkHyiiMz57I4f7QjTcr8xs9EEM2o6RiVQDsa2qthy_cDg1cLJtsLr75gtztHsf9dOq6_AfB0PoxP3Ks3oUDw=w1440)

Figure 1: A map of an illustrative work commute.

Traditionally, RL algorithms fall into two broad categories: [model-based and model-free agents](https://www.jair.org/index.php/jair/article/view/10166) (Figures 2 & 3). A model-based agent (Figure 2) builds a representation of many aspects of the environment. An agent of this type might know how the different locations are connected, the quality of the coffee in each cafe, and anything else that is considered relevant. A model-free agent (Figure 3) has a much more compact representation of its environment. For instance, a value-based model-free agent would have a single number associated with each possible route leaving its home; this is the expected "value" of each route, reflecting a specific weighing of coffee quality vs. commute length. Take the blue path shown in Figure 1 as an example. Say this path has length 4, and the coffee the agent gets by following it is rated 3 stars. If the agent cares about the commute distance 50% more than it cares about the quality of the coffee, the value of this path will be (-1.5 x 4) + (1 x 3) = -3 (we use a negative weight associated with the distance to indicate that longer commutes are undesirable).

![A blue hexagonal infographic mapping out a network of routes from "Home" to "Office." The map includes "Park," "Cafe A," and "Cafe B" as intermediate nodes, with numerical labels for distance along the paths, and callouts showing coffee and food values for each cafe.](https://lh3.googleusercontent.com/qu0UEh4uIwg-ufTtF4lam_l4wVLiKDub_Bq8qQa8z9lm8ngx-VPB319EcfE4QUQtaQagFpmcXPd-QX-zuPV1nwKSXoDNl4Y58skD77GMx1CdaoJG_Q=w1440)

Figure 2: How a model-based agent represents the world. Only details relevant to the agent are captured in the representation (compare with Figure 1). Still, the representation is considerably more complex than the one used by a model-free agent (compare with Figure 3).

![A blue hexagonal infographic illustrating how an agent using successor features represents its environment, showing decision nodes for Home, Cafe A, Cafe B, and Park, with associated transition options and their expected values.](https://lh3.googleusercontent.com/w0i8pXBuiAKDBVRROPhu8wU-TM7ZKILG1epkbluglispHzhQ1WIUoc236rsB8INECUUDd9ruysT7reRcrAGAWH5gQQ-hy5q2TRSElLum2-NJfFERkA=w1440)

Figure 3: How a value-based model-free agent represents the world. For each location the agent has one number associated with each possible course of action; this number is the “value” of each alternative available to the agent. When in a given location, the agent checks the values available and makes a decision based on this information only (as illustrated in the right figure for the location “home”). In contrast with the model-based representation, the information is stored in a non-spatial way, that is, there are no connections between locations (compare with Figure 2).

We can interpret the relative weighting of the coffee quality versus the commute distance as the agent’s preferences. For any fixed set of preferences, a model-free and a model-based agent would choose the same route. Why then have a more complicated representation of the world, like the one used by a model-based agent, if the end result is the same? Why learn so much about the environment if the agent ends up sipping the same coffee?

Preferences can change day to day: an agent might take into account how hungry it is, or whether it’s running late to a meeting, in planning its route to the office. One way for a model-free agent to handle this is to learn the best route associated with every possible set of preferences. This is not ideal because learning every possible combination of preferences will take a long time. It is also impossible to learn a route associated with every possible set of preferences if there are infinitely many of them.

In contrast, a model-based agent can adapt to any set of preferences, without any learning, by "imagining" all possible routes and asking how well they would fulfill its current mindset. However, this approach also has drawbacks. Firstly, ”mentally” generating and evaluating all possible trajectories can be computationally demanding. Secondly, building a model of the entire world can be very difficult in complex environments.

Model-free agents learn faster but are brittle to change. Model-based agents are flexible but can be slow to learn. Is there an intermediate solution?

## Successor features: a middle ground

A recent [study](https://www.nature.com/articles/s41562-017-0180-8) in behavioural science and neuroscience suggests that in certain situations, humans and animals make decisions based on an algorithmic model that is a compromise between the model-free and model-based approaches ([here](https://deepmind.com/blog/article/hippocampus-predictive-map) and [here](https://papers.nips.cc/paper/9522-a-neurally-plausible-model-learns-successor-representations-in-partially-observable-environments.pdf)). The hypothesis is that, like model-free agents, humans also compute the value of alternative strategies in the form of a number. But, instead of summarising a single quantity, humans summarise many different quantities describing the world around them, reminiscent of model-based agents.

It’s possible to endow an RL agent with the same ability. In our example, such an agent would have, for each route, a number representing the expected quality of coffee and a number representing the distance to the office. It could also have numbers associated with things the agent is not deliberately trying to optimise but are nevertheless available to it for future reference (for example, the quality of the food in each cafe). The aspects of the world the agent cares about and keeps track of are sometimes referred to as “features”. Because of that, this representation of the world is called successor features (previously termed the “successor representation” in its [original incarnation](https://www.mitpressjournals.org/doi/abs/10.1162/neco.1993.5.4.613?journalCode=neco)).

Successor features can be thought of as a middle ground between the model-free and model-based representations. Like the latter, successor features summarise many different quantities, capturing the world beyond a single value. However, like in the model-free representation, the quantities the agent keeps track of are simple statistics summarising the features it cares about. In this way, successor features are like an “unpacked” version of the model-free agent. Figure 4 illustrates how an agent using successor features would see our example environment.

![A blue hexagonal infographic illustrating how an agent using successor features represents its environment, showing decision nodes for Home, Cafe A, Cafe B, and Park, with associated transition options and their expected values.](https://lh3.googleusercontent.com/XT3mqYTbd-7Epb1-Zf62a3ekWpXckzpULmkEbagd_A9hKhrSHebMcDyduCaeiSPVVdl-6n_5ia_YjontOdjE-TkC9AVVRTUwAMqEolwlfPlkIll0=w1440)

Figure 4: Representing the world using successor features. This is similar to how a model-free agent represents the world, but, instead of one number associated with each path, the agent has several numbers (in this case, coffee, food and distance). That is, at the location “home”, the agent would have nine, rather than three, numbers to weigh according to its preferences at the moment (compare with Figure 3).

## Using successor features: composing novel plans from a dictionary of policies

Successor features are a useful representation because they allow for a route to be evaluated under different sets of preferences. Let’s use the blue route in Figure 1 as an example again. Using successor features, the agent would have three numbers associated with this path: its length (4), the quality of the coffee (3) and the quality of the food (5). If the agent already ate breakfast it will probably not care much about the food; also, if it is late, it might care about the commute distance more than the quality of the coffee --say, 50% more, as before. In this scenario the value of the blue path would be (-1.5 x 4) + (1 x 3) + (0 x 5) = -3, as in the example given above. But now, on a day when the agent is hungry, and thus cares about the food as much as it cares about the coffee, it can immediately update the value of this route to (-1.5 x 4) + (1 x 3) + (1 x 5) = 2. Using the same strategy, the agent can evaluate any route according to any set of preferences.

In our example, the agent is choosing between routes. More generally, the agent will be searching for a policy: a prescription of what to do in every possible situation. Policies and routes are closely related: in our example, a policy that chooses to take the road to cafe A from home and then chooses the road to the office from cafe A would traverse the blue path. So, in this case, we can talk about policies and routes interchangeably (this would not be true if there were some randomness in the environment, but we will leave this detail aside). We discussed how successor features allow a route (or policy) to be evaluated under different sets of preferences. We call this process generalised policy evaluation, or GPE.

Why is GPE useful? Suppose the agent has a dictionary of policies (for example, known routes to the office). Given a set of preferences, the agent can use GPE to immediately evaluate how well each policy in the dictionary would perform under those preferences. Now the really interesting part: based on this quick evaluation of known policies, the agent can create entirely new policies on the fly. The way it does it is simple: every time the agent has to make a decision, it asks the following question: “if I were to make this decision and then follow the policy with the maximum value thereafter, which decision would lead to the maximum overall value?” Surprisingly, if the agent picks the decision leading to the maximum overall value in each situation, it ends up with a policy that is often better than the individual policies used to create it.

This process of “stitching together” a set of policies to create a better policy is called generalised policy improvement, or GPI. Figure 5 illustrates how GPI works using our running example.

![An infographic composed of three side-by-side hexagonal maps illustrating how Generalized Policy Improvement (GPI) works. In the left map, a robot agent at "Home" evaluates known paths to "Park," "Cafe A," and "Cafe B." In the middle map, the agent selects the path to "Cafe A" as the best next decision. In the right map, the agent moves from "Cafe A" to "Cafe B" to construct an optimized route.](https://lh3.googleusercontent.com/wyxmoz4HoOvkQgEyCvCX0v7gy9Dh6-1BakfugJqLKE4wQx9ft5gYS5Qm2wK8xnxuew4sZsiKleARczC_oRdDRifZiFBxzHRFMoTNeD5nM8xAnPkuURs=w1440)

Figure 5: How GPI works. In this example the agent cares about the commute distance 50% more than it cares about coffee and food quality. The best thing to do in this case is to visit cafe A, then visit cafe B, and finally go to the office. The agent knows three policies associated with the blue, yellow, and orange paths (see Figure 1). Each policy traverses a different path, but none of them coincides with the desired route. Using GPE, the agent evaluates the three policies according to its current set of preferences (that is, weights -1.5, 1, and 1 associated with distance, coffee and food, respectively). Based on this evaluation, the agent asks the following question at home: “if I were to follow one of the three policies all the way to the office, which one would be best?” Since the answer to this question is the blue policy, the agent follows it. However, instead of commiting to the blue policy all the way, when the agent arrives at cafe A it asks the same question again. Now, instead of the blue path, the agent follows the orange one. By repeating this process the agent ends up following the best path to the office to satisfy its preferences, even though none of its known policies would do so on their own.

The performance of a policy created through GPI will depend on how many policies the agent knows. For instance, in our running example, as long as the agent knows the blue and yellow paths, it will find the best route for any preferences over coffee quality and commute length. But the GPI policy will not always find the best route. In Figure 1, the agent would never visit cafe A and then cafe B if it did not already know a policy that connected them in this way (like the orange route in the figure).

### A simple example to show GPE and GPI in action

To illustrate the benefits of GPE and GPI, we now give a glimpse of one of the experiments from our recent publication (see [paper](https://www.pnas.org/content/early/2020/08/13/1907370117) for full details). The experiment uses a simple environment that represents in an abstract way the type of problem in which our approach can be useful. As shown in Figure 6, the environment is a 10 x 10 grid with 10 objects spread across it. The agent only gets a non-zero reward if it picks up an object, in which case another object pops up in a random location. The reward associated with an object depends on its type. Object types are meant to represent concrete or abstract concepts; to connect with our running example, we will consider that each object is either “coffee” or “food” (these are the features the agent keeps track of).

![A 10x10 grid-world map showing three highlighted paths starting from a robot icon: a red path heading to coffee icons, a blue path heading to food icons, and a gray path heading to coffee icons while avoiding food.](https://lh3.googleusercontent.com/239JaXxj4NoXrxIkNFdnP7JnvAKoDwkf_hzUxifhTa89gpY5CZU7gMuVUEfgGeM2zGV0b0MGcL6rRBmVeAT_cHBMZqFoH5AtjhE_DST2lPS_zKCCVQ=w1440)

Figure 6: Simple environment to illustrate the usefulness of GPE and GPI. The agent moves around using the four directional actions (“up”, “down”, “left” and “right”) and receives a non-zero reward when it picks up an object. The reward associated with an object is defined by its type (“coffee” or “food”).

Clearly, the best strategy for the agent depends on its current preferences over coffee or food. For example, in Figure 6, an agent that only cares about coffee may follow the path in red, while an agent focused exclusively on food would follow the blue path. We can also imagine intermediate situations in which the agent wants coffee and food with different weights, including the case in which the agent wants to avoid one of them. For example, if the agent wants coffee but really does not want food, the gray path in Figure 6 may be a better alternative to the red one.

The challenge in this problem is to quickly adapt to a new set of preferences (or a “task”). In our experiments we showed how one can do so using GPE and GPI. Our agent learned two policies: one that seeks coffee and one that seeks food. We then tested how well the policy computed by GPE and GPI performed on tasks associated with different preferences. In figure 7 we compare our method with a model-free agent on the task whose goal is to seek coffee while avoiding food. Observe how the agent using GPE and GPI instantaneously synthesises a reasonable policy, even though it never learned how to deliberately avoid objects. Of course, the policy computed by GPE and GPI can be used as an initial solution to be later refined through learning, which means that it would match the final performance of a model-free agent but would probably get there faster.

![A line graph comparing the average sum of rewards over time for a model-free agent (Q-learning) and a GPE-GPI agent. The model-free agent, represented by a dashed pink line, starts with a very low reward that slowly rises over time in an S-curve, eventually surpassing the GPE-GPI agent. The GPE-GPI agent, shown as a solid blue horizontal line, achieves a high, stable average sum of rewards instantaneously with no learning curve.](https://lh3.googleusercontent.com/9RzYF1zQ4CcCP5PWSuO8aZEf_StLX_xpDnScuG8jQZfd9-zkfN8aKxZyfpGmJXU1cgXYUhn17iGwU6LKN1_FSDKNbtQ4KQ2N9SBz4o9do9BXD1fqcQ=w1440)

Figure 7: A GPE-GPI agent learns to perform well given much less training data than a model-free method (Q-learning). Here the task is to seek coffee while avoiding food. The GPE-GPI agent learned two policies, one that seeks coffee and one that seeks food. It manages to avoid food even though it has never been trained to avoid an object. Shadowed regions are one standard deviation over 100 runs.

Figure 7 shows the performance of GPE and GPI on one specific task. We have also tested the same agent across many other tasks. Figure 8 shows what happens with the performance of the model-free and GPE-GPI agents when we change the relative importance of coffee and food. Note that, while the model-free agent has to learn each task separately, from scratch, the GPE-GPI agent only learns two policies and then quickly adapts to all of the tasks.

![A bar chart comparing the performance of a GPE-GPI agent across different tasks against a model-free agent. Blue vertical bars represent the average sum of rewards achieved by the GPE-GPI agent across various combinations of preferences, which range from "Avoid coffee" to "Seek coffee" and "Seek food" to "Avoid food." A dashed purple line at the top of the chart represents the high, stable benchmark performance of a model-free agent (Q-learning) that had to solve each task individually.](https://lh3.googleusercontent.com/MMP1FmfHjpbRJDHLBLw4tWNE0MXpzhBPT05I64xu1stjT-Y9Hb6rhkhKkSjuwxwjOEIJIJ2-8RpjnZmi-T_K3PUFFwWxserYP88--_Z6LIBwryDv0g=w1440)

Figure 8: Performance of the GPE-GPI agent over different tasks. Each bar corresponds to a task induced by a set of preferences over coffee and food. The colour gradients under the graph represent the sets of preferences: blue indicates positive weight, white indicates zero weight, and red indicates negative weight. So, for example, at the extremes of the graph we have tasks in which the goal is essentially to avoid one type of object while ignoring the other, while at the centre the task is to seek both types of objects with equal impetus. Error bars are one standard deviation over 10 runs.

The experiments above used a simple environment designed to exhibit the properties needed by GPE and GPI without unnecessary confounding factors. But GPE and GPI have also been applied at scale. For example, in previous papers ([here](http://proceedings.mlr.press/v80/barreto18a/barreto18a.pdf) and [here](https://openreview.net/pdf?id=S1VWjiRcKX)) we showed how the same strategy also works when we replace a grid world with a three dimensional environment in which the agent receives observations from a first-person perspective (see illustrative videos [here](https://www.youtube.com/watch?v=-dTnqfwTRMI&feature=youtu.be) and [here](https://www.youtube.com/watch?v=0afwHJofbB0&feature=youtu.be)). We have also used GPE and GPI to allow a four-legged simulated robot to navigate along any direction after having learned how to do so along three directions only (see paper [here](https://papers.nips.cc/paper/9463-the-option-keyboard-combining-skills-in-reinforcement-learning) and video [here](https://www.youtube.com/watch?v=39Ye8cMyelQ&feature=youtu.be)).

## GPE and GPI in context

The work on GPE and GPI is at the intersection of two separate branches of research related to these operations individually. The first, related to GPE, is the work on the successor representation, initiated with Dayan’s [seminal paper](https://www.mitpressjournals.org/doi/abs/10.1162/neco.1993.5.4.613?journalCode=neco) from 1993. Dayan’s paper inaugurated a line of work in neuroscience that is very active to this day (see further reading: "The successor representation in neuroscience"). Recently, the successor representation reemerged in the context of RL (links [here](https://papers.nips.cc/paper/6994-successor-features-for-transfer-in-reinforcement-learning) and [here](https://arxiv.org/abs/1606.02396)), where it is also referred to as “successor features”, and became an active line of research there as well (see further reading: "GPE, successor features, and related approaches"). Successor features are also closely related to [general value functions](https://www.cs.swarthmore.edu/~meeden/DevelopmentalRobotics/horde1.pdf), a concept based on Sutton et al.’s hypothesis that relevant knowledge can be expressed in the form of many predictions about the world (also discussed [here](https://link.springer.com/chapter/10.1007/978-3-642-33093-3_30)). The definition of successor features has independently emerged in [other contexts](https://ai.stanford.edu/~ang/papers/icml04-apprentice.pdf) within RL, and is also related to more [recent approaches](http://proceedings.mlr.press/v37/schaul15.pdf) normally associated with deep RL.

The second branch of research at the origins of GPE and GPI, related to the latter, is concerned with composing behaviours to create new behaviours. The idea of a decentralised controller that executes sub-controllers has come up multiple times over the years (e.g., [Brooks, 1986](https://ieeexplore.ieee.org/document/1087032)), and its implementation using value functions can be traced back to at least as far as 1997, with [Humphrys’](https://www.computing.dcu.ie/~humphrys/PhD/index.html) and [Karlsson’s](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.37.8338&rep=rep1&type=pdf) PhD theses. GPI is also closely related to hierarchical RL, whose foundations were laid down in the 1990's and early 2000’s in the works by [Dayan and Hinton](https://papers.nips.cc/paper/714-feudal-reinforcement-learning), [Parr and Russell](https://papers.nips.cc/paper/1384-reinforcement-learning-with-hierarchies-of-machines), [Sutton, Precup and Singh](https://www.sciencedirect.com/science/article/pii/S0004370299000521), and [Dietterich](https://jair.org/index.php/jair/article/view/10266). Both the composition of behaviours and hierarchical RL are today dynamic areas of research (see further reading: "GPI, hierarchical RL, and related approaches").

[Mehta et al.](http://homes.sice.indiana.edu/natarasr/Papers/var-reward.pdf) were probably the first ones to jointly use GPE and GPI, although in the scenario they considered GPI reduces to a single choice at the outset (that is, there is no “stitching” of policies). The version of GPE and GPI discussed in this blog post was first [proposed](https://arxiv.org/abs/1606.05312) in 2016 as a mechanism to promote [transfer learning](https://www.jmlr.org/papers/volume10/taylor09a/taylor09a.pdf). Transfer in RL dates back to [Singh’s work](https://link.springer.com/article/10.1007/BF00992700) in 1992 and has recently experienced a [resurgence](https://arxiv.org/abs/2009.07888) in the context of deep RL, where it continues to be an active area of research (see further reading: "GPE + GPI, transfer learning, and related approaches").

See more information about these works below, where we also provide a list of suggestions for further readings.

## A compositional approach to reinforcement learning

In summary, a model-free agent cannot easily adapt to new situations, for example to accommodate sets of preferences it has not experienced before. A model-based agent can adapt to any new situation, but in order to do so it first has to learn a model of the entire world. An agent based on GPE and GPI offers an intermediate solution: although the model of the world it learns is considerably smaller than that of a model-based agent, it can quickly adapt to certain situations, often with good performance.

We discussed specific instantiations of GPE and GPI, but these are in fact more general concepts. At an abstract level, an agent using GPE and GPI proceeds in two steps. First, when faced with a new task, it asks: “How well would solutions to known tasks perform on this new task?” This is GPE. Then, based on this evaluation, the agent combines the previous solutions to construct a solution for the new task --that is, it performs GPI. The specific mechanics behind GPE and GPI are less important than the principle itself, and finding alternative ways to carry out these operations may be an exciting research direction. Interestingly, a new [study](https://www.biorxiv.org/content/10.1101/815332v1) in behavioural sciences provides preliminary evidence that humans make decisions in multitask scenarios following a principle that closely resembles GPE and GPI.

The fast adaptation provided by GPE and GPI is promising for building faster learning RL agents. More generally, it suggests a new approach to learning flexible solutions to problems. Instead of tackling a problem as a single, monolithic, task, an agent can break it down into smaller, more manageable, sub-tasks. The solutions of the sub-tasks can then be reused and recombined to solve the overall task faster. This results in a compositional approach to RL that may lead to more scalable agents. At the very least, these agents will not be late because of a cup of coffee.

Read the paper, as first published in PNAS, [here](https://www.pnas.org/content/early/2020/08/13/1907370117).

With thanks to Jim Kynvin, Adam Cain and Dominic Barlow for the figures, Kimberly Stachenfeld for the pointers to the neuroscience literature, and Kelly Clancy for the help with the text.

**Further reading**

GPE, successor features, and related approaches

[Improving Generalisation for Temporal Difference Learning: The Successor Representation.](http://www.gatsby.ucl.ac.uk/~dayan/papers/d93b.pdf) Peter Dayan. Neural Computation, 1993.

[Apprenticeship Learning Via Inverse Reinforcement Learning.](https://ai.stanford.edu/~ang/papers/icml04-apprentice.pdf) Pieter Abbeel and Andrew Y. Ng. Proceedings of the International Conference on Machine learning (ICML), 2004.

[Horde: A Scalable Real-time Architecture for Learning Knowledge from Unsupervised Sensorimotor Interaction.](https://www.cs.swarthmore.edu/~meeden/DevelopmentalRobotics/horde1.pdf) Richard S. Sutton, Joseph Modayil, Michael Delp, Thomas Degris, Patrick M. Pilarski, Adam White. Proceedings of the International Conference on Autonomous Agents and Multiagent Systems (AAMAS), 2011.

[Multi-timescale Nexting in a Reinforcement Learning Robot.](https://link.springer.com/chapter/10.1007/978-3-642-33093-3_30) Joseph Modayil, Adam White, Richard S. Sutton. From Animals to Animats, 2012.

[Universal Value Function Approximators.](http://proceedings.mlr.press/v37/schaul15.pdf) Tom Schaul, Dan Horgan, Karol Gregor, David Silver. Proceedings of the International Conference on Machine learning (ICML), 2015.

[Deep Successor Reinforcement Learning.](https://arxiv.org/abs/1606.02396) Tejas D. Kulkarni, Ardavan Saeedi, Simanta Gautam, Samuel J. Gershman. arXiv, 2017.

[Visual Semantic Planning Using Deep Successor Representations.](https://openaccess.thecvf.com/content_ICCV_2017/papers/Zhu_Visual_Semantic_Planning_ICCV_2017_paper.pdf) Yuke Zhu, Daniel Gordon, Eric Kolve, Dieter Fox, Li Fei-Fei, Abhinav Gupta, Roozbeh Mottaghi, Ali Farhadi. Proceedings of the IEEE International Conference on Computer Vision (ICCV), 2017.

[Deep Reinforcement Learning with Successor Features for Navigation Across Similar Environments.](https://ieeexplore.ieee.org/abstract/document/8206049/authors#authors) Jingwei Zhang, Jost Tobias Springenberg, Joschka Boedecker, Wolfram Burgard. IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), 2017.

[Universal Successor Representations for Transfer Reinforcement Learning.](https://arxiv.org/abs/1804.03758) Chen Ma, Junfeng Wen, Yoshua Bengio. arXiv, 2018.

[Eigenoption Discovery through the Deep Successor Representation.](https://openreview.net/pdf?id=Bk8ZcAxR-) Marlos C. Machado, Clemens Rosenbaum, Xiaoxiao Guo, Miao Liu, Gerald Tesauro, Murray Campbell. International Conference on Learning Representations (ICLR), 2018.

[Successor Options: An Option Discovery Framework for Reinforcement Learning.](https://www.ijcai.org/Proceedings/2019/0458.pdf) Rahul Ramesh, Manan Tomar, Balaraman Ravindran. Proceedings of the International Joint Conference on Artificial Intelligence (IJCAI), 2019.

[Successor Uncertainties: Exploration and Uncertainty in Temporal Difference Learning.](https://papers.nips.cc/paper/8700-successor-uncertainties-exploration-and-uncertainty-in-temporal-difference-learning.pdf) David Janz, Jiri Hron, Przemysław Mazur, Katja Hofmann, José Miguel Hernández-Lobato, Sebastian Tschiatschek. Advances in Neural Information Processing Systems (NeurIPS), 2019.

[Successor Features Combine Elements of Model-Free and Model-based Reinforcement Learning.](https://arxiv.org/abs/1901.11437) Lucas Lehnert, Michael L. Littman. arXiv, 2019.

[Count-Based Exploration with the Successor Representation.](https://aaai.org/ojs/index.php/AAAI/article/view/5955) Marlos C. Machado, Marc G. Bellemare, Michael Bowling. Proceedings of the AAAI Conference on Artificial Intelligence (AAAI), 2020.

GPI, hierarchical RL, and related approaches

[A Robust Layered Control System for a Mobile Robot.](https://ieeexplore.ieee.org/document/1087032) R. Brooks. IEEE Journal on Robotics and Automation, 1986.

[Feudal Reinforcement Learning.](https://papers.nips.cc/paper/714-feudal-reinforcement-learning) Peter Dayan and Geoffrey E. Hinton. Advances in Neural Information Processing Systems (NIPS), 1992.

[Action Selection Methods Using Reinforcement Learning.](https://www.computing.dcu.ie/~humphrys/PhD/index.html) Mark Humphrys. PhD thesis, University of Cambridge, Cambridge, UK, 1997.

[Learning to Solve Multiple Goals.](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.37.8338&rep=rep1&type=pdf) Jonas Karlsson. PhD thesis, University of Rochester, Rochester, New York, 1997.

[Reinforcement Learning with Hierarchies of Machines.](https://papers.nips.cc/paper/1384-reinforcement-learning-with-hierarchies-of-machines) Ronald Parr and Stuart J. Russell. Advances in Neural Information Processing Systems (NIPS), 1997.

[Between MDPs and Semi-MDPs: A Framework for Temporal Abstraction in Reinforcement Learning.](https://www.sciencedirect.com/science/article/pii/S0004370299000521) Richard S.Sutton, DoinaPrecup, Satinder Singh. Artificial Intelligence, 1999.

[Hierarchical Reinforcement Learning with the MAXQ Value Function Decomposition.](https://jair.org/index.php/jair/article/view/10266) T. G. Dietterich. Journal of Artificial Intelligence Research, 2000.

[Multiple-Goal Reinforcement Learning with Modular Sarsa(O).](https://www.ijcai.org/Proceedings/03/Papers/233.pdf) Nathan Sprague and Dana Ballard. Proceedings of the International Joint Conference on Artificial Intelligence (IJCAI), 2003.

[Q-decomposition for Reinforcement Learning Agents.](https://people.eecs.berkeley.edu/~russell/papers/ml03-qdecomp.pdf) Stuart J. Russell and Andrew Zimdars. Proceedings of the International Conference on Machine Learning (ICML), 2003.

[Compositionality of Optimal Control Laws.](https://papers.nips.cc/paper/3842-compositionality-of-optimal-control-laws) E. Todorov. Advances in Neural Information Processing Systems (NIPS), 2009.

[Linear Bellman combination for control of character animation.](https://homes.cs.washington.edu/~jovan/papers/dasilva-2009-lbc.pdf) M. da Silva, F. Durand, and J. Popovic. ACM Transactions on Graphics, 2009.

[Hierarchy Through Composition with Multitask LMDPS.](http://proceedings.mlr.press/v70/saxe17a.html) A. M. Saxe, A. C. Earle, and B. Rosman. Proceedings of the International Conference on Machine Learning (ICML), 2017.

[Hybrid Reward Architecture for Reinforcement Learning.](https://papers.nips.cc/paper/7123-hybrid-reward-architecture-for-reinforcement-learning) Harm van Seijen, Mehdi Fatemi, Joshua Romoff, Romain Laroche, Tavian Barnes, and Jeffrey Tsang. Advances in Neural Information Processing Systems (NIPS), 2017.

[Feudal Networks for Hierarchical Reinforcement Learning.](https://arxiv.org/abs/1703.01161) Alexander Sasha Vezhnevets, Simon Osindero, Tom Schaul, Nicolas Heess, Max Jaderberg, David Silver, Koray Kavukcuoglu. Proceedings of the International Conference on Machine Learning (ICML), 2017.

[Composable Deep Reinforcement Learning for Robotic Manipulation.](https://arxiv.org/abs/1803.06773) T. Haarnoja, V. Pong, A. Zhou, M. Dalal, P. Abbeel, and S. Levine. IEEE International Conference on Robotics and Automation (ICRA), 2018.

[Composing Value Functions in Reinforcement Learning.](http://proceedings.mlr.press/v97/van-niekerk19a.html) Benjamin Van Niekerk, Steven James, Adam Earle, Benjamin Rosman. Proceedings of the International Conference on Machine Learning (ICML), 2019.

[Planning in Hierarchical Reinforcement Learning: Guarantees for Using Local Policies.](http://proceedings.mlr.press/v117/zahavy20a.html) Tom Zahavy, Avinatan Hasidim, Haim Kaplan, Yishay Mansour. International Conference on Algorithmic Learning Theory (ALT), 2020.

GPE + GPI, transfer learning, and related approaches

[Transfer of Learning by Composing Solutions of Elemental Sequential Tasks.](https://link.springer.com/article/10.1007/BF00992700) Satinder Singh. Machine Learning, 1992.

[Transfer Learning for Reinforcement Learning Domains: A Survey.](https://www.jmlr.org/papers/volume10/taylor09a/taylor09a.pdf) Matthew E. Taylor and Peter Stone. Journal of Machine Learning Research, 2009.

[Transfer in Variable-Reward Hierarchical Reinforcement Learning.](http://homes.sice.indiana.edu/natarasr/Papers/var-reward.pdf) Neville Mehta, Sriraam Natarajan, Prasad Tadepalli, Alan Fern. Machine Learning, 2008.

[Learning and Transfer of Modulated Locomotor Controllers.](https://arxiv.org/abs/1610.05182) Nicolas Heess, Greg Wayne, Yuval Tassa, Timothy Lillicrap, Martin Riedmiller, David Silver. arXiv, 2016.

[Learning to Reinforcement Learn.](https://arxiv.org/abs/1611.05763) Jane X. Wang, Zeb Kurth-Nelson, Dhruva Tirumala, Hubert Soyer, Joel Z. Leibo, Remi Munos, Charles Blundell, Dharshan Kumaran, Matt Botvinick. arXiv, 2016.

[RL2: Fast Reinforcement Learning via Slow Reinforcement Learning.](https://arxiv.org/abs/1611.02779) Yan Duan, John Schulman, Xi Chen, Peter L. Bartlett, Ilya Sutskever, Pieter Abbeel. arXiv, 2016.

[Model-Agnostic Meta-Learning for Fast Adaptation of Deep Networks.](https://dl.acm.org/doi/10.5555/3305381.3305498) Chelsea Finn, Pieter Abbeel, Sergey Levine. Proceedings of the International Conference on Machine Learning (ICML), 2017.

[Successor Features for Transfer in Reinforcement Learning.](https://papers.nips.cc/paper/6994-successor-features-for-transfer-in-reinforcement-learning) André Barreto, Will Dabney, Rémi Munos, Jonathan J. Hunt, Tom Schaul, Hado van Hasselt, David Silver. Advances in Neural Information Processing Systems (NIPS), 2017.

[Transfer in Deep Reinforcement Learning Using Successor Features and Generalised Policy Improvement.](https://arxiv.org/pdf/1901.10964) André Barreto, Diana Borsa, John Quan, Tom Schaul, David Silver, Matteo Hessel, Daniel Mankowitz, Augustin Žídek, Rémi Munos. Proceedings of the International Conference on Machine Learning (ICML), 2018.

[Composing Entropic Policies Using Divergence Correction.](http://proceedings.mlr.press/v97/hunt19a/hunt19a.pdf) Jonathan Hunt, André Barreto, Timothy Lillicrap, Nicolas Heess. Proceedings of the International Conference on Machine Learning (ICML), 2019.

[Universal Successor Features Approximators.](https://arxiv.org/pdf/1812.07626) Diana Borsa, André Barreto, John Quan, Daniel Mankowitz, Rémi Munos, Hado van Hasselt, David Silver, Tom Schaul. International Conference on Learning Representations (ICLR), 2019.

[The Option Keyboard: Combining Skills in Reinforcement Learning.](https://papers.nips.cc/paper/9463-the-option-keyboard-combining-skills-in-reinforcement-learning) André Barreto, Diana Borsa, Shaobo Hou, Gheorghe Comanici, Eser Aygün, Philippe Hamel, Daniel Toyama, Jonathan J. Hunt, Shibl Mourad, David Silver, Doina Precup. Advances in Neural Information Processing Systems (NeurIPS), 2019.

[Transfer Learning in Deep Reinforcement Learning: A Survey.](https://arxiv.org/abs/2009.07888) Zhuangdi Zhu, Kaixiang Lin, Jiayu Zhou, arXiv, 2020.

[Fast Task Inference with Variational Intrinsic Successor Features.](https://openreview.net/pdf?id=BJeAHkrYDS) Steven Hansen, Will Dabney, André Barreto, Tom Van de Wiele, David Warde-Farley, Volodymyr Mnih. International Conference on Learning Representations (ICLR), 2020.

[Fast Reinforcement Learning with Generalized Policy Updates.](https://www.pnas.org/content/early/2020/08/13/1907370117) André Barreto, Shaobo Hou, Diana Borsa, David Silver, Doina Precup. Proceedings of the National Academy of Sciences, 2020.

The successor representation in neuroscience

[The Hippocampus as a Predictive Map.](https://www.nature.com/articles/nn.4650) Kimberly Stachenfeld, Matthew Botvinick, Samuel Gershman. Nature Neuroscience, 2017.

[The Successor Representation in Human Reinforcement Learning.](https://www.nature.com/articles/s41562-017-0180-8) I. Momennejad, E. M. Russek, J. H. Cheong, M. M. Botvinick, N. D. Daw, S. J. Gershman. Nature Human Behaviour, 2017.

[Predictive Representations Can Link Model-Based Reinforcement Learning to Model-Free Mechanisms.](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1005768) E. Russek, I. Momennejad, M. M. Botvinick, S. J. Gershman, N. D. Daw. PLOS Computational Biology, 2017.

[The Successor Representation: Its Computational Logic and Neural Substrates.](https://www.jneurosci.org/content/38/33/7193.short) Samuel J. Gershman. Journal of Neuroscience, 2018.

[Better Transfer Learning with Inferred Successor Maps.](https://papers.nips.cc/paper/9104-better-transfer-learning-with-inferred-successor-maps.pdf) Tamas J. Madarasz, Timothy E. Behrens. Advances in Neural Information Processing Systems (NeurIPS), 2019.

[Multi-Task Reinforcement Learning in Humans.](https://www.biorxiv.org/content/10.1101/815332v1.full.pdf) Momchil S. Tomov, Eric Schulz, and Samuel J. Gershman. bioRxiv, 2019.

[A neurally plausible model learns successor representations in partially observable environments.](https://papers.nips.cc/paper/9522-a-neurally-plausible-model-learns-successor-representations-in-partially-observable-environments) Eszter Vertes, Maneesh Sahani. Advances in Neural Information Processing Systems (NeurIPS), 2019.

[Neurobiological Successor Features for Spatial Navigation.](https://onlinelibrary.wiley.com/doi/abs/10.1002/hipo.23246) William de Cothi, Caswell Barry. Hippocampus, 2020.

[Linear Reinforcement Learning: Flexible Reuse of Computation in Planning, Grid Fields, and Cognitive Control.](https://www.biorxiv.org/content/10.1101/856849v3) Payam Piray, Nathaniel D. Daw. bioRxiv, 2020.
