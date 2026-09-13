---
title: "Understanding Agent Cooperation"
source: https://deepmind.google/blog/understanding-agent-cooperation/
site: deepmind
date: 2017-02-02
authors: Joel Leibo, Marc Lanctot, Thore Graepel, Vinicius Zambaldi, Janusz Marecki
crawled: 2026-09-13
---

We employ deep multi-agent reinforcement learning to model the emergence of cooperation. The new notion of sequential social dilemmas allows us to model how rational agents interact, and arrive at more or less cooperative behaviours depending on the nature of the environment and the agents’ cognitive capacity. The research may enable us to better understand and control the behaviour of complex multi-agent systems such as the economy, traffic, and environmental challenges.

Self-interested people often work together to achieve great things. Why should this be the case, when it is in their best interest to just care about their own wellbeing and disregard that of others?

The question of how and under what circumstances selfish agents cooperate is one of the fundamental question in the social sciences. One of the simplest and most elegant models to describe this phenomenon is the well-known game of [Prisoner’s Dilemma](https://en.wikipedia.org/wiki/Prisoner%27s_dilemma) from game theory.

Two suspects are arrested and put into solitary confinement. Without confessions the police do not have sufficient evidence to convict the two suspects on the main charge, but have good prospects to achieve one year prison sentences for both. In order to entice the prisoners to confess, they offer them simultaneously the following deal: If you testify against the other prisoner (“defect”) you will be released, but the other prisoner will serve three years in prison. If both prisoners testify against each other (“defect”), they will both serve two years.

It turns out, that [rational agents](https://en.wikipedia.org/wiki/Rational_agent) - in the sense of game theory - should always defect in this game, because no matter what the other prisoner chooses to do, they will be better off defecting. Yet, paradoxically, if both prisoners reason in this way, they will each have to serve two years in prison - one year more than if they had cooperated and remained silent. This paradox is what we refer to as a social dilemma.

Recent progress in artificial intelligence and specifically deep reinforcement learning provides us with the tools to look at the problem of social dilemmas through a new lens. Traditional game theorists model social dilemmas in terms of a simple binary choice between cooperate and defect for each agent. In real life, both cooperating and defecting may require complex behaviours, involving difficult sequences of actions that agents need to learn to execute. We refer to this new setting as sequential social dilemmas, and use artificial agents trained by deep multi-agent reinforcement learning to study it.

As an example, consider the following Gathering game: Two agents, Red and Blue, roam a shared world and collect apples to receive positive rewards. They may also direct a beam at the other agent, “tagging them”, to temporarily remove them from the game, but this action does not trigger a reward. A visualisation of agents playing the gathering game can be seen below.

We let the agents play this game many thousands of times and let them learn how to behave rationally using deep multi-agent reinforcement learning. Rather naturally, when there are enough apples in the environment, the agents learn to peacefully coexist and collect as many apples as they can. However, as the number of apples is reduced, the agents learn that it may be better for them to tag the other agent to give themselves time on their own to collect the scarce apples.

It turns out that this Gathering game shares many characteristics of the original Prisoner’s Dilemma, but allows us to study the more interesting case in which agents need to learn to implement their desired behaviour: Either to cooperate and collect apples, or to defect and try to tag the other agent.

In these sequential social dilemmas, we can now study what factors contribute to agents’ cooperation. For example, the following plot shows that in the Gathering game greater scarcity of apples leads to more “tagging” behaviour of agents. Furthermore, agents with the capacity to implement more complex strategies try to tag the other agent more frequently, i.e. behave less cooperatively - no matter how we vary the scarcity of apples.

![Two line graphs comparing the behavior of small networks (orange) and large networks (blue). The "Gathering" graph on the left shows that as scarcity increases, aggressiveness rises, with the large network consistently showing higher aggressiveness. The "Wolfpack" graph on the right shows that as group benefit increases, the lone-wolf capture rate decreases, with the large network cooperating more (lower lone-wolf capture rate) than the small network.](https://lh3.googleusercontent.com/HWhDR135jJAp9Oe_L_5XFXcRETIMUIHfGe8EPgZ_HCTl_5bMtoift1Wew4I-TTf44efcmIUSSbjS0tcy_7C-baGCWNowfQePTmAXarTzK5fPp5cXAag=w1440)

Interestingly, in another game called Wolfpack (see gameplay video below), which requires close coordination to successfully cooperate, we find that greater capacity to implement complex strategies leads to more cooperation between agents, the opposite of the finding with Gathering. So, depending on the situation, having a greater capacity to implement complex strategies may yield either more or less cooperation. The new framework of sequential social dilemmas allows us to take into account not only the outcome of the interaction (as in the Prisoner’s dilemma), but also the difficulty of learning to implement a given strategy.

In summary, we showed that we can apply the modern AI technique of deep multi-agent reinforcement learning to age-old questions in social science such as the mystery of the emergence of cooperation. We can think of the trained AI agents as an approximation to economics’ rational agent model [“homo economicus”](https://en.wikipedia.org/wiki/Homo_economicus). Hence, such models give us the unique ability to test policies and interventions into simulated systems of interacting agents - both human and artificial.

As a consequence, we may be able to better understand and control complex multi-agent systems such as the economy, traffic systems, or the ecological health of our planet - all of which depend on our continued cooperation.

**Notes**

Read the paper: [Multi-agent Reinforcement Learning in Sequential Social Dilemmas](https://storage.googleapis.com/deepmind-media/papers/multi-agent-rl-in-ssd.pdf)
