---
title: "Game-theory insights into asymmetric multi-agent games"
source: https://deepmind.google/blog/game-theory-insights-into-asymmetric-multi-agent-games/
site: deepmind
date: 2018-01-17
authors: Karl Tuyls, Marc Lanctot, Julien Perolat
crawled: 2026-09-13
---

As AI systems start to play an increasing role in the real world it is important to understand how different systems will interact with one another.

In our [latest paper](https://www.nature.com/articles/s41598-018-19194-4), published in the journal [Scientific Reports](https://www.nature.com/srep/), we use a branch of [game theory](https://en.wikipedia.org/wiki/Game_theory) to shed light on this problem. In particular, we examine how two intelligent systems behave and respond in a particular type of situation known as an [asymmetric game](https://en.wikipedia.org/wiki/Game_theory#Symmetric_/_Asymmetric), which include Leduc poker and various board games such as [Scotland Yard](https://en.wikipedia.org/wiki/Scotland_Yard_(board_game)). Asymmetric games also naturally model certain real-world scenarios such as automated auctions where buyers and sellers operate with different motivations. Our results give us new insights into these situations and reveal a surprisingly simple way to analyse them. While our interest is in how this theory applies to the interaction of multiple AI systems, we believe the results could also be of use in economics, evolutionary biology and empirical game theory among others.

> The method proves to be mathematically simple, allowing a rapid and straightforward analysis of asymmetric games

Game theory is a field of mathematics that is used to analyse the strategies used by decision makers in competitive situations. It can apply to humans, animals, and computers in various situations but is commonly used in AI research to study “multi-agent” environments where there is more than one system, for example several household robots cooperating to clean the house. Traditionally, the evolutionary dynamics of multi-agent systems have been analysed using simple, [symmetric games](https://en.wikipedia.org/wiki/Symmetric_game), such as the classic [Prisoner’s Dilemma](https://en.wikipedia.org/wiki/Prisoner%27s_dilemma), where each player has access to the same set of actions. Although these games can provide useful insights into how multi-agent systems work and tell us how to achieve a desirable outcome for all players - known as the Nash equilibrium - they cannot model all situations.

Our new technique allows us to quickly and easily identify the strategies used to find the Nash equilibrium in more complex asymmetric games - characterised as games where each player has different strategies, goals and rewards. These games - and the new technique we use to understand them - can be illustrated using an example from ‘Battle of the Sexes’, a coordination game commonly used in game theory research.

Here, two players have to coordinate a night out to either the opera or the movies. One of the players has a slight preference for the opera and one of them has a slight preference for the movies. The game is asymmetric because, while both players have access to the same options, the corresponding rewards for each are different based on the players preferences. In order to maintain their friendship - or equilibrium - the players should choose the same activity (hence the zero payoff for separate activities).

![A payoff matrix for the asymmetric "Battle of the Sexes" coordination game, showing payoffs of (3,2) for Opera-Opera, (2,3) for Movie-Movie, and (0,0) for mismatched choices.](https://lh3.googleusercontent.com/jwWLgsEQbbwBGt8lEf-LMFAMblkrcQJxmFwXWsqj0lFzMK9NzD01bNaRAc4XMz6A7MIDfaZ06hRtrnGq_DHu0nHi7hx6-ayDpX7KGqSU3O2G6Ffu=w1440)

This game has three equilibria: (i) both players deciding to go to the opera, (ii) both deciding to go to the movies, and (iii) a final, mixed option, where each player will opt for their preferred option three fifths of the time. This last option, which is said to be “unstable”, can be rapidly uncovered using our method by simplifying - or decomposing - the asymmetric game into its symmetric counterparts. These counterpart games essentially considers the reward table of each player as a separate symmetric 2-player game with equilibrium points that coincide with the original asymmetric game.

In the plot below, the Nash equilibrium is plotted for the two, simple counterparts allowing us to quickly identify the optimal strategy in the asymmetrical game (a). The reverse can also be done, using the asymmetrical game to identify the equilibrium in its symmetrical counterparts.

![Three directional field plots illustrating the decomposition of the asymmetric "Battle of the Sexes" game (a) into its two symmetric counterparts, Game 1 (b) and Game 2 (c), to identify equilibrium points.](https://lh3.googleusercontent.com/anzpnloh49usEKec3qmq5mYd1VUSLvR9_ERNXkvvee7XRzjJF7IDtgnhL8DU3itLD8y998c0hyFMYkMMmgI3uRZSe7BWzCq32ElmeVEbzT2pphf_rQ8=w1440)

The red dot represents the Nash equilibrium. For the asymmetric game (a), this can easily be derived from the plots of the two symmetric counterparts (b) and (c). In all plots, the x-axis corresponds to the probability with which player 1 chooses opera, and the y-axis corresponds to the probability with which the 2nd player chooses opera.

This method can also be applied to other games, including Leduc poker, which is described in detail in the paper. In all of these situations, the method proves to be mathematically simple, allowing a rapid and straightforward analysis of asymmetric games that we hope will also help our understanding of various dynamic systems, including multi-agent environments.

Read the original Scientific Reports paper [here](https://www.nature.com/articles/s41598-018-19194-4).

Read the follow-up AAMAS paper [here](https://arxiv.org/abs/1803.06376).

The Scientific Reports paper is authored by Karl Tuyls, Julien Perolat, Marc Lanctot, Georg Ostrovski, Rahul Savani, Joel Leibo, Toby Ord, Thore Graepel and Shane Legg. The AAMAS paper is authored by Karl Tuyls, Julien Perolat, Marc Lanctot, Joel Leibo and Thore Graepel.

UPDATE 20/03/18

Our [latest paper](https://arxiv.org/abs/1803.06376), forthcoming at the Autonomous Agents and Multi-Agent Systems conference (AAMAS), builds on the Scientific Reports paper outlined above. [A Generalised Method for Empirical Game Theoretic Analysis](https://arxiv.org/abs/1803.06376) introduces a general method to perform empirical analysis of multi-agent interactions, both in symmetric and asymmetric games. The method allows to understand how multi-agent strategies interact, what the attractors are and what the basins of attraction look like, giving an intuitive understanding for the strength of the involved strategies. Furthermore, it explains how many data samples to consider in order to guarantee that the equilibria of the approximating game are sufficiently reliable. We apply the method to several domains, including AlphaGo, Colonel Blotto and Leduc poker.
