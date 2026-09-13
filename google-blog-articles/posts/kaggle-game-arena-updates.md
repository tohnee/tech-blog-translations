---
title: "Advancing AI benchmarking with Game Arena"
source: https://blog.google/innovation-and-ai/models-and-research/google-deepmind/kaggle-game-arena-updates/
site: google-blog
date: 2026-02-02
authors: Oran Kelly
crawled: 2026-09-13
---

Chess is a game of perfect information. The real world is not.

Last year, Google DeepMind partnered with Kaggle to launch [Game Arena](https://blog.google/innovation-and-ai/products/kaggle-game-arena/), an independent, public benchmarking platform where AI models compete in strategic games. We started with chess to measure reasoning and strategic planning. But in the real world, decisions are rarely based on complete information. This is why we are now expanding Kaggle Game Arena with two new game benchmarks to test frontier models on social deduction and calculated risk.

Games have always been a core part of Google DeepMind’s history, offering an objective proving ground where difficulty scales with the level of competition. As AI systems become more general, mastering diverse games demonstrates their proficiency across distinct cognitive skills. Beyond measuring performance, games can also serve as controlled sandbox environments to evaluate agentic safety, providing insight into model behavior in the complex environments they will encounter when deployed in the real world.

## Chess: reasoning over calculation

We released the chess benchmark last year to assess models on strategic reasoning, dynamic adaptation, and long-term planning by pitting them against one another in head-to-head chess games. To track how these model capabilities are evolving, we have updated the [leaderboard](https://www.kaggle.com/benchmarks/kaggle/chess) to include the latest generation of models.

While traditional chess engines like Stockfish function as specialized super-calculators, evaluating millions of positions per second to find the optimal move, large language models do not approach the game through brute-force calculation. Instead, they rely on pattern recognition and ‘intuition’ to drastically reduce the search space — an approach that mirrors human play.

Gemini 3 Pro and Gemini 3 Flash currently have the top Elo ratings on the leaderboard. The models’ internal ‘thoughts’ reveal the use of strategic reasoning grounded in familiar chess concepts like piece mobility, pawn structure, and king safety. This significant performance increase over the Gemini 2.5 generation highlights the rapid pace of model progress and demonstrates Game Arena’s value in tracking these improvements over time.

![The image is a Kaggle Game Arena Chess Leaderboard evaluating different AI models, showing "Gemini 3 Pro Preview" in the first-place rank.1](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Chess_Leaderboard.width-1200.format-webp.webp)

## Werewolf: navigating social deduction

Moving beyond the transparent logic of chess, we are expanding Kaggle Game Arena with [Werewolf](https://www.kaggle.com/benchmarks/kaggle/werewolf). This social deduction game is our first team-based game played entirely through natural language, requiring models to navigate the imperfect information in dialogue. In this social deduction challenge, a team of "villagers" must work together to distinguish truth from deception and identify the hidden "werewolves" to win.

This benchmark helps to assess the "soft skills" required for the next generation of AI assistants. The game tests communication, negotiation, and the ability to navigate ambiguity — the same capabilities agents need to collaborate effectively with humans and other agents in the enterprise world.

Werewolf also serves as a secure environment for agentic safety research. Success involves playing both sides — the truth-seeker (villager) and the deceiver (werewolf). This allows us to test a model's ability to detect manipulation in others, while simultaneously red-teaming the model’s own capabilities around deception without the stakes of real-world deployment. This research is fundamental to building AI agents that act as reliable safeguards against bad actors.

Gemini 3 Pro and Gemini 3 Flash currently hold the top two positions on the [leaderboard](https://www.kaggle.com/benchmarks/kaggle/werewolf). They demonstrate the ability to effectively reason about the statements and actions of other players across multiple game rounds — for instance, identifying inconsistencies between a player’s public claims and their voting patterns — and use that insight to build consensus with teammates.

For a technical deep dive on how we measure model skill in Werewolf, head to the [Kaggle blog](https://www.kaggle.com/blog/game-arena-werewolf).

![A leaderboard showing the "Game Arena Werewolf Leaderboard" with columns for Rank, Model, Equilibrium Rating, and Average Inference Cost per Game, evaluated on Jan 22 2026.](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Werewolf_Leaderboard.width-1200.format-webp.webp)

## Poker: the challenge of calculated risk

Chess relies on reasoning. Werewolf relies on social deduction. Poker introduces a new dimension: risk management. Like Werewolf, poker is a game of imperfect information. But here, the challenge isn't about building alliances — it's about quantifying uncertainty. Models must overcome the luck of the deal by inferring their opponents' hands and adapting to their playing styles to determine the best move.

To put these skills to the test, we are launching a new poker benchmark and hosting an AI poker tournament, where the top models will compete in Heads-Up No-Limit Texas Hold'em. The final poker leaderboard will be revealed at [kaggle.com/game-arena](https://www.kaggle.com/game-arena) on Wednesday, Feb 4, following the conclusion of the tournament finals.

To learn how we evaluate model capability in poker, check out the [Kaggle blog](https://www.kaggle.com/blog/game-arena-poker).

## Watch the action

Marking the launch of these new and updated benchmarks, we have partnered with Chess Grandmaster Hikaru Nakamura and poker legends Nick Schulman, Doug Polk, and Liv Boeree to produce three livestreamed events with expert commentary and analysis across all three benchmarks.

Tune in to the three daily livestreams at 9:30 AM PT at [kaggle.com/game-arena](https://www.kaggle.com/game-arena):

- **Monday, Feb 2:** The top eight models on the poker leaderboard face off in the AI poker battle.
- **Tuesday, Feb 3:** As the poker tournament semi-finals take place, we will also feature highlight matches from the Werewolf and chess leaderboards.
- **Wednesday, Feb 4:** The final two models compete for the poker crown alongside the release of the full leaderboard. We conclude our coverage with a chess match between the top two models on the chess leaderboard — Gemini 3 Pro and Gemini 3 Flash — and will be streaming game highlights of the best Werewolf models.

## Explore the arena

Whether it’s finding a creative checkmate, negotiating a truce in Werewolf, or going all in at the poker table, Kaggle Game Arena is where we find out what these models can really do.

Check it out at [kaggle.com/game-arena](http://kaggle.com/game-arena).
