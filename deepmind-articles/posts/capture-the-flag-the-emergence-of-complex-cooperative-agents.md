---
title: "Capture the Flag: the emergence of complex cooperative agents"
source: https://deepmind.google/blog/capture-the-flag-the-emergence-of-complex-cooperative-agents/
site: deepmind
date: 2019-05-30
authors: Max Jaderberg, Wojciech Marian Czarnecki, Iain Dunning, Thore Graepel, Luke Marris
crawled: 2026-09-13
---

Mastering the strategy, tactical understanding, and team play involved in multiplayer video games represents a critical challenge for AI research.

In our latest paper, [now published in the journal Science](http://science.sciencemag.org/cgi/content/full/364/6443/859?ijkey=rZC5DWj2KbwNk&keytype=ref&siteid=sci), we present new developments in reinforcement learning, resulting in human-level performance in Quake III Arena Capture the Flag. This is a complex, multi-agent environment and one of the canonical 3D first-person multiplayer games. The agents successfully cooperate with both artificial and human teammates, and demonstrate high performance even when trained with reaction times comparable to human players. Furthermore, we show how these methods have managed to scale beyond research Capture the Flag environments to the full game of Quake III Arena.

![Side-by-side gameplay footage from a first-person perspective showing two different procedural environments in a modified version of Quake III Arena Capture the Flag, with one on the left featuring blocky urban structures and the other on the right set in a desert landscape with trees and cacti.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/622724d86793159dd36203c6_CTF2001.gif)

Agents playing Capture the Flag, presented from the first-person perspective of one of the red players in an indoor environment (left) and outdoor environment (right).

![Side-by-side gameplay footage from a first-person perspective showing two different procedural environments in a modified version of Quake III Arena Capture the Flag, with one on the left featuring blocky urban structures and the other on the right set in a brick castle.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62272519604e646b14f736d4_CTF2002.gif)

Agents playing two other Quake III Arena multiplayer game modes on full-scale tournament maps: Harvester on the Future Crossings map (left) and One Flag Capture the Flag on the Ironwood map (right), with all the pickups and gadgets of the full game.

Billions of people inhabit the planet, each with their own individual goals and actions, but still capable of coming together through teams, organisations and societies in impressive displays of collective intelligence. This is a setting we call multi-agent learning: many individual agents must act independently, yet learn to interact and cooperate with other agents. This is an immensely difficult problem - because with co-adapting agents the world is constantly changing.

To investigate this problem, we look at 3D first-person multiplayer video games. These games represent the most popular genre of video game, and have captured the imagination of millions of gamers because of their immersive game play, as well as the challenges they pose in terms of strategy, tactics, hand-eye coordination, and team play. The challenge for our agents is to learn directly from raw pixels to produce actions. This complexity makes first-person multiplayer games a fruitful and active area of research within the AI community.

The game we focused on in this work is Quake III Arena (which we aesthetically modified, though all game mechanics remain the same). Quake III Arena has laid the foundations for many modern first-person video games, and has attracted a long-standing competitive e-sports scene. We train agents that learn and act as individuals, but which must be able to play on teams with and against any other agents, artificial or human.

The rules of CTF are simple, but the dynamics are complex. Two teams of individual players compete on a given map with the goal of capturing the opponent team’s flag while protecting their own. To gain tactical advantage they can tag the opponent team members to send them back to their spawn points. The team with the most flag captures after five minutes wins.

From a multi-agent perspective, CTF requires players to both successfully cooperate with their teammates as well as compete with the opposing team, while remaining robust to any playing style they might encounter.

To make things even more interesting, we consider a variant of CTF in which the map layout changes from match to match. As a consequence, our agents are forced to acquire general strategies rather than memorising the map layout. Additionally, to level the playing field, our learning agents experience the world of CTF in a similar way to humans: they observe a stream of pixel images and issue actions through an emulated game controller.

Our agents must learn from scratch how to see, act, cooperate, and compete in unseen environments, all from a single reinforcement signal per match: whether their team won or not. This is a challenging learning problem, and its solution is based on three general ideas for reinforcement learning:

- Rather than training a single agent, we **train a population of agents**, which learn by playing with each other, providing a diversity of teammates and opponents.
- Each agent in the population **learns its own internal reward signal**, which allows agents to generate their own internal goals, such as capturing a flag. A **two-tier optimisation process** optimises agents’ internal rewards directly for winning, and uses reinforcement learning on the internal rewards to learn the agents’ policies.
- Agents **operate at two timescales**, fast and slow, which improves their ability to use memory and generate consistent action sequences.

![Architecture diagram of the FTW agent, showing how game observations, points, and winning signals feed into fast and slow recurrent neural networks to optimize internal rewards, policy, and actions.](https://lh3.googleusercontent.com/5PHNViS_pfp2_Hi4IknNq1CXEVZZVM9GUqLWBwK7Eghos_rROM9YOPnPGl6biUFFmsV1ZyeuEHmSth-3m1Sp6FSNqBwHCK5WKfLR9wCMV6-hguVX=w1440)

A schematic of the For The Win (FTW) agent architecture. The agent combines recurrent neural networks (RNNs) on fast and slow timescales, includes a shared memory module, and learns a conversion from game points to internal reward.

The resulting agent, dubbed the For The Win (FTW) agent, learns to play CTF to a very high standard. Crucially, the learned agent policies are robust to the size of the maps, the number of teammates, and the other players on their team. Below, you can explore some games on both the outdoor procedural environments, where FTW agents play against each other, as well as games in which humans and agents play together on indoor procedural environments.

We ran a tournament including 40 human players, in which humans and agents are randomly matched up in games - both as opponents and as teammates.

![Several human players sitting at desks with computer monitors playing a multiplayer video game.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6227269607daf72e1b316f54_CTF2004.gif)

An early test tournament with humans playing CTF with and against trained agents and other humans.

The FTW agents learn to become much stronger than the strong baseline methods, and exceed the win-rate of the human players. In fact, in a survey among participants they were rated more collaborative than human participants.

![Line graph showing Agent Elo rating over 450K training games played. The FTW agent (blue line) rises steadily, surpassing the Average Human baseline at around 100K games and the Strong Human baseline at around 180K games, reaching nearly 1600 Elo. The Self-play + RS agent (red line) peaks below the Strong Human level, while the Self-play agent (dark grey line) remains near the Random agent baseline of 500 Elo.](https://lh3.googleusercontent.com/qlB3GyTaGuLxfVhFICNcr8MwIB6fyOCgodqYFShtiu2A4u0RatfTLI6KAKfYHUh1AeXjViRcRecwF2boCzTX8NdgJ3BJb9P7ao9LHICD8CPGYNYP9ZQ=w1440)

The performance of our agents during training. Our new agent, the FTW agent, obtains a much higher Elo rating - which corresponds to the probability of winning - than the human players and baseline methods of Self-play + RS and Self-play.

Going beyond mere performance evaluation, it is important to understand the emergent complexity in the behaviours and internal representations of these agents.

To understand how agents represent game state, we look at activation patterns of the agents’ neural networks plotted on a plane. Dots in the figure below represent situations during play with close by dots representing similar activation patterns. These dots are coloured according to the high-level CTF game state in which the agent finds itself: In which room is the agent? What is the status of the flags? What teammates and opponents can be seen? We observe clusters of the same colour, indicating that the agent represents similar high-level game states in a similar manner.

![Diagram of the agent's neural representations, showing how single neuron selectivity (such as for "agent flag taken" or "agent is respawning") maps to basic Capture the Flag situations, which then combine to form distinct color-coded clusters in a large t-SNE embedding of the overall agent state.](https://lh3.googleusercontent.com/zVf8uFhVFoqtxF4TliLjQj3uw0pTOrGAuDraseBOx0ITJK0Uq6xVW5SG109ZglCHksD7O3e9RfLeRyvtI7fbab8QH2t0jgOfQdBTYgzLcgMixWpm=w1440)

A look into how our agents represent the game world. In the plot above, neural activation patterns at a given time are plotted according to how similar they are to one another: the closer two points are in space, the more similar their activation patterns. They’re then coloured according to the game situation at that time - same colour, same situation. We see that these neural activation patterns are organised, and form clusters of colour, indicating that agents are representing meaningful aspects of gameplay in a stereotyped, organised fashion. The trained agents even exhibit some artificial neurons which code directly for particular situations.

The agents are never told anything about the rules of the game, yet learn about fundamental game concepts and effectively develop an intuition for CTF. In fact, we can find particular neurons that code directly for some of the most important game states, such as a neuron that activates when the agent’s flag is taken, or a neuron that activates when an agent’s teammate is holding a flag. The paper provides further analysis covering the agents’ use of memory and visual attention.

## Human Comparable Agents

How did our agents perform as well as they did? First, we noticed that the agents had very fast reaction times and were very accurate taggers, which might explain their performance (tagging is a tactical action that sends opponents back to their starting point). Humans are comparatively slow to process and act on sensory input, due to our slower biological signalling. [Here’s an example of a reaction time test you can try yourself](https://faculty.washington.edu/chudler/java/redgreen.html). Thus, our agents’ superior performance might be a result of their faster visual processing and motor control. However, by artificially reducing this accuracy and reaction time, we saw that this was only one factor in their success. In a further study, we trained agents which have an inbuilt delay of a quarter of a second (267 ms) – that is, agents have a 267ms lag before observing the world – comparable with reported reaction times of human video game players. These response-delayed agents still outperformed human participants, with strong humans only winning 21% of the time.

![A data table and bar chart showing results for agents with a 267ms response delay. The top table shows human win rates against these delayed agents: 30% for exploitability testers, 21% for strong human players, and 12% for intermediate human players. Below, a bar chart compares the average number of game events—capturing, picking up, and recovering flags, as well as tagging opponents—for average humans, strong humans, delayed agent teammates, and delayed agent opponents, showing that delayed agents consistently perform more flag-related actions than human players.](https://lh3.googleusercontent.com/46bqyRgJjBFhp44RnTHdcl9H728CDe-KAOkezbZzF_uXyDfmZq2QnIZxUjmyy5QVu2fJsCNcDloBkB_tMeHVJb9sEcHbr5yC-t91FDGqB_jlc63TAQ=w1440)

The win rates of human players against response-delayed agents are low, indicating that even with human-comparable reaction delays, agents outperform human players. In addition, looking at the average number of game events by humans and response-delayed agents, we see comparable numbers of tagging events, showing that these agents do not have an advantage over humans in this respect.

Through unsupervised learning we established the prototypical behaviours of agents and humans to discover that agents in fact learn human-like behaviours, such as following teammates and camping in the opponent’s base.

![Three automatically discovered behaviours: home base defence, opponent base camping, and teammate following.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/622726eac975f27c5d7cd03c_CTF2008.gif)

Three examples of the automatically discovered behaviours that the trained agents exhibit.

These behaviours emerge in the course of training, through reinforcement learning and population-level evolution, with behaviours - such as teammate following - falling out of favour as agents learn to cooperate in a more complementary manner.

The training progression of a population of FTW agents. Top left: the 30 agents’ Elo ratings as they train and evolve from each other. Top right: the genetic tree of these evolution events. The lower graph shows the progression of knowledge, some of the internal rewards, and behaviour probability throughout the training of the agents.

## Going Further

While this paper focuses on Capture the Flag, the research contributions are general and we are excited to see how others build upon our techniques in different complex environments. Since initially publishing these results, we have found success in extending these methods to the full game of Quake III Arena, which includes professionally played maps, more multiplayer game modes in addition to Capture the Flag, and more gadgets and pickups. Initial results indicate that agents can play multiple game modes and multiple maps competitively, and are starting to challenge the skills of our human researchers in test matches. Indeed, ideas introduced in this work, such as population based multi-agent RL, form a foundation of the [AlphaStar agent in our work on StarCraft II](https://deepmind.com/blog/alphastar-mastering-real-time-strategy-game-starcraft-ii/).

In general, this work highlights the potential of multi-agent training to advance the development of artificial intelligence: exploiting the natural curriculum provided by multi-agent training, and forcing the development of robust agents that can even team up with humans.

**Notes**

For more details, please see the [paper](http://science.sciencemag.org/cgi/content/full/364/6443/859?ijkey=rZC5DWj2KbwNk&keytype=ref&siteid=sci) ([PDF](https://science.sciencemag.org/content/sci/364/6443/859.full.pdf?ijkey=rZC5DWj2KbwNk&keytype=ref&siteid=sci)) and the [full supplementary video](https://youtu.be/dltN4MxV1RI).

This work was done by Max Jaderberg, Wojciech M. Czarnecki, Iain Dunning, Luke Marris, Brendan Tracey, Guy Lever, Antonio Garcia Castaneda, Charles Beattie, Neil Rabinowitz, Ari Morcos, Avraham Ruderman, Nicolas Sonnerat, Tim Green, Louise Deason, Joel Z. Leibo, David Silver, Demis Hassabis, Koray Kavukcuoglu, and Thore Graepel.

Visualisations were created by Adam Cain, Damien Boudot, Doug Fritz, Jaume Sanchez Elias, Paul Lewis, Max Jaderberg, Wojciech M. Czarnecki, and Luke Marris.

We would like to thank Patrick Howard and Dan “Scancode” Gold for allowing us to use the Quake III Arena maps they designed.

Updated 30/5/19. Read about our new work below, in “Human Comparable Agents” and “Going Further”.
