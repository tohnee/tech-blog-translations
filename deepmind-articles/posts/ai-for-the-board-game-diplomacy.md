---
title: "AI for the board game Diplomacy"
source: https://deepmind.google/blog/ai-for-the-board-game-diplomacy/
site: deepmind
date: 2022-12-06
authors: Yoram Bachrach, János Kramár
crawled: 2026-09-13
---

Agents cooperate better by communicating and negotiating, and sanctioning broken promises helps keep them honest

Successful communication and cooperation have been crucial for helping societies advance throughout history. The closed environments of board games can serve as a sandbox for modelling and investigating interaction and communication – and we can learn a lot from playing them. In our recent paper, [published today in Nature Communications](https://www.nature.com/articles/s41467-022-34473-5), we show how artificial agents can use communication to better cooperate in the board game Diplomacy, a vibrant domain in artificial intelligence (AI) research, known for its focus on alliance building.

Diplomacy is challenging as it has simple rules but high emergent complexity due to the strong interdependencies between players and its immense action space. To help solve this challenge, we designed negotiation algorithms that allow agents to communicate and agree on joint plans, enabling them to overcome agents lacking this ability.

Cooperation is particularly challenging when we cannot rely on our peers to do what they promise. We use Diplomacy as a sandbox to explore what happens when agents may deviate from their past agreements. Our research illustrates the risks that emerge when complex agents are able to misrepresent their intentions or mislead others regarding their future plans, which leads to another big question: What are the conditions that promote trustworthy communication and teamwork?

We show that the strategy of sanctioning peers who break contracts dramatically reduces the advantages they can gain by abandoning their commitments, thereby fostering more honest communication.

## What is Diplomacy and why is it important?

Games such as [chess](https://en.wikipedia.org/wiki/Deep_Blue_(chess_computer)), [poker](https://en.wikipedia.org/wiki/Computer_poker_player), [Go](https://en.wikipedia.org/wiki/AlphaGo), and many [video games](https://en.wikipedia.org/wiki/AlphaStar_(software)) have always been fertile ground for AI research. [Diplomacy](https://en.wikipedia.org/wiki/Diplomacy_(game)) is a seven-player game of negotiation and alliance formation, played on an old map of Europe partitioned into provinces, where each player controls multiple units ([rules of Diplomacy](https://media.wizards.com/2015/downloads/ah/diplomacy_rules.pdf)). In the standard version of the game, called Press Diplomacy, each turn includes a negotiation phase, after which all players reveal their chosen moves simultaneously.

The heart of Diplomacy is the negotiation phase, where players try to agree on their next moves. For example, one unit may support another unit, allowing it to overcome resistance by other units, as illustrated here:

![Two maps of France side by side showing movement scenarios. On the left, two units, represented by a red soldier figure and arrow in Burgundy and a blue soldier figure and arrow in Gascony attempt to move into the Paris region. As the units have equal strength, neither succeeds.On the right, the red unit in Picardy supports the red unit in Burgundy, overpowering Gascony's blue unit and allowing the red unit into Burgundy.](https://lh3.googleusercontent.com/SeB3fQbZy8hYrqEo5Zm2TSAT6_d6NsV0YXC6bbtpL802esmYrTGRmFjyVP9AeIbi1aguiS4ASoSxcHcYyIKhTiEBhiYz14eJWCctiAogYkPYW77cqw=w1440)

**Two movement scenarios.**
**Left:** two units (a Red unit in Burgundy and a Blue unit in Gascony) attempt to move into Paris. As the units have equal strength, neither succeeds.
**Right:** the Red unit in Picardy supports the Red unit in Burgundy, overpowering Blue’s unit and allowing the Red unit into Burgundy.

Computational approaches to Diplomacy have been researched since the 1980s, many of which were explored on a simpler version of the game called No-Press Diplomacy, where strategic communication between players is not allowed. Researchers have also proposed [computer-friendly negotiation protocols](http://www.daide.org.uk/), sometimes called “Restricted-Press”.

## What did we study?

We use Diplomacy as an analog to real-world negotiation, providing methods for AI agents to coordinate their moves. We take [our non-communicating Diplomacy agents](https://www.deepmind.com/publications/learning-to-play-no-press-diplomacy-with-best-response-policy-iteration) and augment them to play Diplomacy with communication by giving them a protocol for negotiating contracts for a joint plan of action. We call these augmented agents Baseline Negotiators, and they are bound by their agreements.

![Two maps of France side by side illustrating diplomacy contracts. On the left, a restriction represented by a pink arrow with a cross through it blocks the red player from moving from Ruhr to Burgundy. While a pink arrow from a red player in Piedmont to Marseilles allows a move. The map on the right is the same, with an additional pink arrow between Brest and Gascony.](https://lh3.googleusercontent.com/g-1iYXu5iFalP5lRCKkoNi7lsW7PT31a8vOTaV-iajiV-7veK0qK6rrbA-tzflULaVmzDxiOvoK1RfbtUGiCLlJOIHTGhUHhSxsaywKLnkdHyD4f=w1440)

**Diplomacy contracts.**
**Left:** a restriction allowing only certain actions to be taken by the Red player (they are not allowed to move from Ruhr to Burgundy, and must move from Piedmont to Marseilles).
**Right:** A contract between the Red and Green players, which places restrictions on both sides.

We consider two protocols: the Mutual Proposal Protocol and the Propose-Choose Protocol, discussed in detail in [the full paper](https://www.nature.com/articles/s41467-022-34473-5). Our agents apply algorithms that identify mutually beneficial deals by simulating how the game might unfold under various contracts. We use the [Nash Bargaining Solution](https://en.wikipedia.org/wiki/Cooperative_bargaining#:~:text=Nash%20bargaining%20game,-John%20Forbes%20Nash&text=His%20solution%20is%20called%20the,and%20independence%20of%20irrelevant%20alternatives.) from [game theory](https://en.wikipedia.org/wiki/Game_theory) as a principled foundation for identifying high-quality agreements. The game may unfold in many ways depending on the actions of players, so our agents use Monte-Carlo simulations to see what might happen in the next turn.

![Map images of next state simulations under a given contract. On the left, there's a map of the current state. On the right, three smaller maps show multiple possible next states.](https://lh3.googleusercontent.com/aom4EV1Ay_Ibt4eYG_18K4AJhiq2kseick_zbz_SOch2F_cS1HG6FIZO_eC3MNblwUqn53GHuJyX08LHD4_wVToifsYmOqXMZmwJ3qiBpMT2due-=w1440)

Simulating next states given an agreed contract. Left: current state in a part of the board, including a contract agreed between the Red and Green players. Right: multiple possible next states.

Our experiments show that our negotiation mechanism allows Baseline Negotiators to significantly outperform baseline non-communicating agents.

![Two graphs showing Baseline Negotiators significantly outperforming non-communicating agents. The graph on the left is for The Mutual Proposal Protocol. On the right, it shows The Propose-Choose Protocol.](https://lh3.googleusercontent.com/4DPDARaNRFGuI2QMVIqO58kqihMRdaqxvBAG5s7qwR55aQAbsZkt761dAXcTdQRQpNpMlU846EDhT0SpwQQIu_dhKGFHM9Orhd5AC__bRjqlfuALhg=w1440)

Baseline Negotiators significantly outperform non-communicating agents. Left: The Mutual Proposal Protocol. Right: The Propose-Choose Protocol. “Negotiator advantage” is the ratio of win rates between the communicating agents and the non-communicating agents.

## Agents breaking agreements

In Diplomacy, agreements made during negotiation are not binding (communication is “[cheap talk'](https://en.wikipedia.org/wiki/Cheap_talk#:~:text=In%20game%20theory%2C%20cheap%20talk,the%20state%20of%20the%20world.)'). But what happens when agents who agree to a contract in one turn deviate from it the next? In many real-life settings people agree to act in a certain way, but fail to meet their commitments later on. To enable cooperation between AI agents, or between agents and humans, we must examine the potential pitfall of agents strategically breaking their agreements, and ways to remedy this problem. We used Diplomacy to study how the ability to abandon our commitments erodes trust and cooperation, and identify conditions that foster honest cooperation.

So we consider Deviator Agents, which overcome honest Baseline Negotiators by deviating from agreed contracts. Simple Deviators simply “forget” they agreed to a contract and move however they wish. Conditional Deviators are more sophisticated, and optimise their actions assuming that other players who accepted a contract will act in accordance with it.

![Digram showing all types of Communicating Agents in green boxes. Blue boxes shoot off some of these to represent specific agent algorithms.](https://lh3.googleusercontent.com/gLIpehcVdrgG6HqkIV5Sk7jMC6Nd8yMlyISOmOUr492GKWGDFe_7D4ZuBsgQc6blRVH0LJtzm3c9Y9STUA3IrW5EkbFs91OTory5EomPMhLEvdwul50=w1440)

All types of our Communicating Agents. Under the green grouping terms, each blue block represents a specific agent algorithm.

We show that Simple and Conditional Deviators significantly outperform Baseline Negotiators, the Conditional Deviators overwhelmingly so.

![Two graphs showing comparing Deviator Agents and Baseline Negotiator Agents. The left graph shows The Mutual Proposal Protocol. On the right is The Propose-Choose Protocol.](https://lh3.googleusercontent.com/Vg7_bhmDBR2G56_astmZZZY7SYFzKQelJvSxAb7-fotvGx7U4oGW6ExeuPOQSWfVEN7iNManFkMM4bEXRt-1H2jszoEcguL78ZvEAkzERGF4OT_NEg=w1440)

Deviator Agents versus Baseline Negotiator Agents. Left: The Mutual Proposal Protocol. Right: The Propose-Choose Protocol. “Deviator advantage” is the ratio of win rates between the Deviator Agents over the Baseline Negotiators.

## Encouraging agents to be honest

Next we tackle the deviation problem using Defensive Agents, which respond adversely to deviations. We investigate Binary Negotiators, who simply cut off communications with agents who break an agreement with them. But shunning is a mild reaction, so we also develop Sanctioning Agents, who don’t take betrayal lightly, but instead modify their goals to actively attempt to lower the deviator's value – an opponent with a grudge! We show that both types of Defensive Agents reduce the advantage of deviation, particularly Sanctioning Agents.

![Two graphs comparing Deviator Agents and Baseline Negotiator Agents. On the left, the graph shows The Mutual Proposal Protocol. On the right, the graph is for The Propose-Choose Protocol.](https://lh3.googleusercontent.com/45v1YOhCJl4-VQ_aTRdDif-ZPc57voNR8RXROpcI41rbPAAFoVN1i7K1gTdWUD97OY7rbbwsE70fhgg57IrfeWmv5raCuZz4PUmjIq76Ddn3TNuw5w=w1440)

Non-Deviator Agents (Baseline Negotiators, Binary Negotiators, and Sanctioning Agents) playing against Conditional Deviators. Left: Mutual Proposal Protocol. Right: Propose-Choose Protocol. “Deviator advantage” values lower than 1 indicate a Defensive Agent outperforms a Deviator Agent. A population of Binary Negotiators (blue) reduces the advantage of Deviators compared with a population of Baseline Negotiators (grey).

Finally, we introduce Learned Deviators, who adapt and optimise their behaviour against Sanctioning Agents over multiple games, trying to render the above defences less effective. A Learned Deviator will only break a contract when the immediate gains from deviation are high enough and the ability of the other agent to retaliate is low enough. In practice, Learned Deviators occasionally break contracts late in the game, and in doing so achieve a slight advantage over Sanctioning Agents. Nevertheless, such sanctions drive the Learned Deviator to honour more than 99.7% of its contracts.

We also examine possible learning dynamics of sanctioning and deviation: what happens when Sanctioning Agents may also deviate from contracts, and the potential incentive to stop sanctioning when this behaviour is costly. Such issues can gradually erode cooperation, so additional mechanisms such as repeating interaction across multiple games or using a trust and reputation systems may be needed.

Our paper leaves many questions open for future research: Is it possible to design more sophisticated protocols to encourage even more honest behaviour? How could one handle combining communication techniques and imperfect information? Finally, what other mechanisms could deter the breaking of agreements? Building fair, transparent and trustworthy AI systems is an extremely important topic, and it is a key part of DeepMind’s mission. Studying these questions in sandboxes like Diplomacy helps us to better understand tensions between cooperation and competition that might exist in the real world. Ultimately, we believe tackling these challenges allows us to better understand how to develop AI systems in line with society’s values and priorities.

Read our full paper [here](https://www.nature.com/articles/s41467-022-34473-5).

**Acknowledgements**

We would like to thank Will Hawkins, Aliya Ahmad, Dawn Bloxwich, Lila Ibrahim, Julia Pawar, Sukhdeep Singh, Tom Anthony, Kate Larson, Julien Perolat, Marc Lanctot, Edward Hughes, Richard Ives, Karl Tuyls, Satinder Singh and Koray Kavukcuoglu for their support and advice throughout the work.

**Full paper authors**

János Kramár, Tom Eccles, Ian Gemp, Andrea Tacchetti, Kevin R. McKee, Mateusz Malinowski, Thore Graepel, Yoram Bachrach.
