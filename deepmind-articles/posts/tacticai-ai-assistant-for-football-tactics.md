---
title: "TacticAI: an AI assistant for football tactics"
source: https://deepmind.google/blog/tacticai-ai-assistant-for-football-tactics/
site: deepmind
date: 2024-03-19
authors: Zhe Wang, Petar Veličković
crawled: 2026-09-13
---

As part of our multi-year collaboration with Liverpool FC, we develop a full AI system that can advise coaches on corner kicks

'Corner taken quickly… Origi!'

Liverpool FC made a historic comeback in the 2019 UEFA Champions League semi-finals. One of the most iconic moments was a corner kick by Trent Alexander-Arnold that lined up Divock Origi to score what has gone down in history as [Liverpool FC’s greatest goal](https://www.liverpoolfc.com/news/first-team/454462-corner-taken-quickly-origi-voted-liverpool-s-greatest-ever-goal).

Corner kicks have high potential for goals, but devising a routine relies on a blend of human intuition and game design to identify patterns in rival teams and respond on-the-fly.

Today, in [Nature Communications](https://www.nature.com/articles/s41467-024-45965-x), we introduce TacticAI: an artificial intelligence (AI) system that can provide experts with tactical insights, particularly on corner kicks, through predictive and generative AI. Despite the limited availability of gold-standard data on corner kicks, TacticAI achieves state-of-the-art results by using a geometric deep learning approach to help create more generalizable models.

We developed and evaluated TacticAI together with experts from Liverpool Football Club as part of a multi-year research collaboration. TacticAI’s suggestions were preferred by human expert raters 90% of the time over tactical setups seen in practice.

TacticAI demonstrates the potential of assistive AI techniques to revolutionize sports for players, coaches, and fans. Sports like football are also a dynamic domain for developing AI, as they feature real-world, multi-agent interactions, with multimodal data. Advancing AI for sports could translate into many areas on and off the field – from computer games and [robotics](https://deepmind.google/blog/from-motor-control-to-embodied-intelligence/), to traffic coordination.

![A diagram illustrating how TacticAI addresses three core tactical questions through predictive models ("What will happen?"), embeddings/retrieval ("What happened?"), and guided generation ("How to make this happen?").](https://lh3.googleusercontent.com/S-Zqa29JwHj32RaAujqBAdPTIfDbxdr0Z4kiay85nqZRp2ULbiU9xSPAVq6TYYr83eNNwGQipwZuj4rBIhaFkLcqW41kN1zXkL6BxHLdtm3s3kNudXo=w1440)

TacticAI is a full AI system with combined predictive and generative models to analyze what happened in previous plays and how to to make adjustments towards making a particular outcome more likely.

## Developing a game plan with Liverpool FC

Five years ago, we began a multi-year collaboration with Liverpool FC to advance AI for sports analytics.

Our first paper, [Game Plan](https://deepmind.google/blog/advancing-sports-analytics-through-ai-research/), looked at why AI should be used in assisting football tactics, highlighting examples such as analyzing penalty kicks. In 2022, we developed [Graph Imputer](https://www.nature.com/articles/s41598-022-12547-0), which showed how AI can be used with a prototype of a predictive system for downstream tasks in football analytics. The system could predict the movements of players off-camera when no tracking data was available – otherwise, a club would need to send a scout to watch the game in person.

Now, we have developed TacticAI as a full AI system with combined predictive and generative models. Our system allows coaches to sample alternative player setups for each routine of interest, and then directly evaluate the possible outcomes of such alternatives.

TacticAI is built to address three core questions:

1. For a given corner kick tactical setup, what will happen? e.g., who is most likely to receive the ball, and will there be a shot attempt?
2. Once a setup has been played, can we understand what happened? e.g., have similar tactics worked well in the past?
3. How can we adjust the tactics to make a particular outcome happen? e.g., how should the defending players be repositioned to decrease the probability of shot attempts?

## Predicting corner kick outcomes with geometric deep learning

A corner kick is awarded when the ball passes over the byline, after touching a player of the defending team. Predicting the outcomes of corner kicks is complex, due to the randomness in gameplay from individual players and the dynamics between them. This is also challenging for AI to model because of the limited gold-standard corner kick data available – only about 10 corner kicks are played in each match in the Premier League every season.

![On the top is a football field with dots connecting to a network and arrows pointing to a new one. Below is a football field with arrows leading to four smaller fields which connected to a network of blue arrows.](https://lh3.googleusercontent.com/kLYJc6CiJFSnMUFwiy8pJ4PChxuU_iqpPFLjEt_teaqqaN-9cOeQ2iUfNnkTQ5XZs7zugryE80ggjqA55AIrbqJoyLwYmVHpcs54QxjjVybl2acjow=w1440)

(A) How corner kick situations are converted to a graph representation. Each player is treated as a node in a graph. A graph neural network operates over this graph updating each node’s representation using message passing.

(B) How TacticAI processes a given corner kick. All four possible combinations of reflections are applied to the corner, and fed to the core TacticAI model. They interact to compute the final player representations, which can be used to predict outcomes.

TacticAI successfully predicts corner kick play by applying a geometric deep learning approach. First, we directly model the implicit relations between players by representing corner kick setups as graphs, in which nodes represent players (with features like position, velocity, height, etc.) and edges represent relations between them. Then, we exploit an approximate symmetry of the football pitch. Our geometric architecture is a variant of the [Group Equivariant Convolutional Network](https://proceedings.mlr.press/v48/cohenc16.pdf) that generates all four possible reflections of a given situation (original, H-flipped, V-flipped, HV-flipped) and forces our predictions for receivers and shot attempts to be identical across all four of them. This approach reduces the search space of possible functions our neural network can represent to ones that respect the reflection symmetry — and yields more generalizable models, with less training data.

## Providing constructive suggestions to human experts

By harnessing its predictive and generative models, TacticAI can assist coaches by finding similar corner kicks, and testing different tactics.

Traditionally, to develop tactics and counter tactics, analysts would rewatch many videos of games to look for similar examples and study rival teams. TacticAI automatically computes the numerical representations of players, which allows experts to easily and efficiently look up relevant past routines. We further validated this intuitive observation through extensive qualitative studies with football experts, who found TacticAI’s top-1 retrievals were relevant 63% of the time, nearly double the 33% benchmark seen in approaches that suggest pairs based on directly analyzing player position similarity.

TacticAI’s generative model also allows human coaches to redesign corner kick tactics to optimize probabilities of certain outcomes, such as reducing the probability of a shot attempt for a defensive setup. TacticAI provides tactical recommendations which adjust positions of all the players on a particular team. From these proposed adjustments, coaches can identify important patterns, as well as key players for a tactic’s success or failure, more quickly.

![And image in four quadrants, in three are overhead views of football fields with blue and red circles. In one quadrant is a bar chart.](https://lh3.googleusercontent.com/K5unXt_sDNeeouaR2MLYxvEEuYiNEks8N75RGiSK5io8dizGeM_JZ5aMVTJp0qkrxtRVWyLV-kX9sj-4fJ5tVApw_9paE4R1BTpN-tMdfqsG1mGfdSY=w1440-h810-n-nu)

(A) An example of a corner kick where there was a shot attempt in reality.

(B) TacticAI can generate a counterfactual setting in which the shot probability has been reduced by adjusting the positioning and velocities of the defenders.

(C) The suggested defender positions result in reduced receiver probability for attacking players 2-4.

(D) The model is capable of generating multiple such scenarios and coaches can inspect the different options.

In our quantitative analysis, we showed TacticAI was accurate at predicting corner kick receivers and shot situations, and that player repositioning was similar to how real plays unfolded.We also evaluated these recommendations qualitatively in a blind case study where raters did not know which tactics were from real game play and which ones were TacticAI-generated. Human football experts from Liverpool FC found that our suggestions cannot be distinguished from real corners, and were favored over their original situations 90% of the time. This demonstrates TacticAI’s predictions are not only accurate, but useful and deployable.

![An image with four pairs of football fields. One has blue and red circles and the other highlight circles that have moved.](https://lh3.googleusercontent.com/Rg6Zmt1Ne-5AMKwwlrZVo0cOjojmBi2mXdQpJndpJmoDYzTegrBDBjAE9cd8tqbWtpdt4O-dB5xAsRpBt8EI5eZf-F4K63KZThcAlhoSq8tUvZvcRVE=w1440-h810-n-nu)

Examples of the strategic refinements that raters preferred to original plays, where TacticAI suggested:

(A) The recommendations of four players are more favorable by most raters.

(B) Defenders furthest away from the corner make improved covering runs

(C) Improved covering runs for a central group of defenders in the penalty box

(D) Substantially better tracking runs for two central defenders, along with a better positioning for two other defenders in the goal area.

## Advancing AI for sports

TacticAI is a full AI system that could give coaches instant, extensive, and accurate tactical insights – that are also practical on the field. With TacticAI, we have developed a capable AI assistant for football tactics and achieved a milestone in developing useful assistants in sports AI. We hope future research can help develop assistants that expand to more multimodal inputs outside of player data, and help experts in more ways.

We show how AI can be used in football, but football can also teach us a lot about AI. It’s a highly dynamic and challenging game to analyze, with many human factors from physique to psychology. It’s challenging even for experts like seasoned coaches to detect all the patterns. With TacticAI, we hope to take many lessons in developing broader assistive technologies that blend human expertise and AI analysis to help people in the real world.

**Learn more about TacticAI**

[Read our paper in Nature Communications](https://www.nature.com/articles/s41467-024-45965-x)

This project is a collaboration between the Google DeepMind team and Liverpool FC. The authors of TacticAI include: Zhe Wang, Petar Veličković, Daniel Hennes, Nenad Tomašev, Laurel Prince, Michael Kaisers, Yoram Bachrach, Romuald Elie, Li Kevin Wenliang, Federico Piccinini, William Spearman, Ian Graham, Jerome Connor, Yi Yang, Adrià Recasens, Mina Khan, Nathalie Beauguerlange, Pablo Sprechmann, Pol Moreno, Nicolas Heess, Michael Bowling, Demis Hassabis and Karl Tuyls.
