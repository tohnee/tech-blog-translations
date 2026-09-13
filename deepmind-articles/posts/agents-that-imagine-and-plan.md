---
title: "Agents that imagine and plan"
source: https://deepmind.google/blog/agents-that-imagine-and-plan/
site: deepmind
date: 2017-07-20
authors: Razvan Pascanu, Theophane Weber, Peter Battaglia, David Reichert, Sébastien Racanière, Yazhe Li
crawled: 2026-09-13
---

Imagining the consequences of your actions before you take them is a powerful tool of human cognition. When placing a glass on the edge of a table, for example, we will likely pause to consider how stable it is and whether it might fall. On the basis of that imagined consequence we might readjust the glass to prevent it from falling and breaking. This form of deliberative reasoning is essentially ‘[imagination](http://www.gatsby.ucl.ac.uk/~demis/SceneConstruction(TICS07).pdf)’, it is a distinctly human ability and is a crucial tool in our everyday lives.

If our algorithms are to develop equally sophisticated behaviours, they too must have the capability to ‘imagine’ and reason about the future. Beyond that they must be able to construct a plan using this knowledge. We have seen some tremendous results in this area - particularly in programs like AlphaGo, which use an ‘internal model’ to analyse how actions lead to future outcomes in order to to reason and plan. These internal models work so well because environments like Go are ‘perfect’ - they have clearly defined rules which allow outcomes to be predicted very accurately in almost every circumstance. But the real world is complex, rules are not so clearly defined and unpredictable problems often arise. Even for the most intelligent agents, imagining in these complex environments is a long and costly process.

> Being able to deal with imperfect models and learning to adapt a planning strategy to current state are important research questions

In [two](https://arxiv.org/abs/1707.06170) [new](https://arxiv.org/abs/1707.06203) papers, we describe a new family of approaches for imagination-based planning. We also introduce architectures which provide new ways for agents to learn and construct plans to maximise the efficiency of a task. These architectures are efficient, robust to complex and imperfect models, and can adopt flexible strategies for exploiting their imagination.

## Imagination-augmented agents

The agents we introduce benefit from an ‘imagination encoder’- a neural network which learns to extract any information useful for the agent’s future decisions, but ignore that which is not relevant. These agents have a number of distinct features:

- they learn to interpret their internal simulations. This allows them to use models which coarsely capture the environmental dynamics, even when those dynamics are not perfect.
- they use their imagination efficiently. They do this by adapting the number of imagined trajectories to suit the problem. Efficiency is also enhanced by the encoder, which is able to extract additional information from imagination beyond rewards - these trajectories may contain useful clues even if they do not necessarily result in high reward.
- they can learn different strategies to construct plans. They do this by choosing between continuing a current imagined trajectory or restarting from scratch. Alternatively, they can use different imagination models, with different accuracies and computational costs. This offers them a broad spectrum of effective planning strategies, rather than being restricted to a one-size-fits-all approach which might limit adaptability in imperfect environments.

## Testing our architectures

We tested our proposed architectures on multiple tasks, including the puzzle game Sokoban and a spaceship navigation game. Both games require forward planning and reasoning, making them the perfect environment to test our agents' abilities.

- In Sokoban the agent has to push boxes onto targets. Because boxes can only be pushed, many moves are irreversible (for instance a box in a corner cannot be pulled out of it).
- In the spaceship task, the agent must stabilise a craft by activating its thrusters a fixed number of times. It must contend with the gravitational pull of several planets, making it a highly nonlinear complex continuous control task.

To limit trial-and-error for both tasks, each level is procedurally generated and the agent can only try it once; this encourages the agent to try different strategies 'in its head' before testing them in the real environment.

Above, an agent plays Sokoban from a pixel representation, not knowing the rules of the game. At specific points in time, we visualise the agent's imagination of five possible futures. Based on that information, the agent decides what action to take. The corresponding trajectory is highlighted.

![A screenshot from the spaceship navigation game, showing a small white circle representing the craft, a green square target, and several gray circular planets of varying sizes exerting gravitational pull on a dark background.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62265a873b6b1f2f52357fd8_Spaceship.gif)

An agent playing the spaceship task. The red lines indicate trajectories that are executed in the environment while blue and green depict imagined trajectories.

For both tasks, the imagination-augmented agents outperform the imagination-less baselines considerably: they learn with less experience and are able to deal with the imperfections in modelling the environment. Because agents are able to extract more knowledge from internal simulations they can solve tasks more with fewer imagination steps than conventional search methods, like the Monte Carlo tree search.

When we add an additional ‘manager’ component, which helps to construct a plan, the agent learns to solve tasks even more efficiently with fewer steps. In the spaceship task it can distinguish between situations where the gravitational pull of its environment is strong or weak, meaning different numbers of these imagination steps are required. When an agent is presented with multiple models of an environment, each varying in quality and cost-benefit, it learns to make a meaningful trade-off. Finally, if the computational cost of imagination increases with each action taken, the agent imagines the effect of multiple chained actions early, and relies on this plan later without invoking imagination again.

Being able to deal with imperfect models and learning to adapt a planning strategy to current state are important research questions. Our two new papers, alongside previous work by Hamrick et al. consider these questions. While model-based reinforcement learning and planning are active areas of research (papers by Silver et al.; Henaff et al.; and Kansky et al. are a just a few examples of related lines of enquiry), further analysis and consideration is required to provide scalable solutions to rich model-based agents that can use their imaginations to reason about - and plan - for the future.

**Notes**

Read paper: [Learning model-based planning from scratch](https://arxiv.org/abs/1707.06170) and [Imagination-Augmented Agents for Deep Reinforcement Learning](https://arxiv.org/abs/1707.06203)
