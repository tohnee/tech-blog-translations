---
title: "MuZero: Mastering Go, chess, shogi and Atari without rules"
source: https://deepmind.google/blog/muzero-mastering-go-chess-shogi-and-atari-without-rules/
site: deepmind
date: 2020-12-23
authors: Julian Schrittwieser, Ioannis Antonoglou, Thomas Hubert, Karen Simonyan, Laurent Sifre, Simon Schmitt, Arthur Guez, Edward Lockhart, Demis Hassabis, Thore Graepel, Timothy Lillicrap, David Silver
crawled: 2026-09-13
---

In 2016, we introduced [AlphaGo](https://deepmind.com/research/case-studies/alphago-the-story-so-far), the first artificial intelligence (AI) program to defeat humans at the ancient game of Go. Two years later, its successor - [AlphaZero](https://deepmind.com/blog/article/alphazero-shedding-new-light-grand-games-chess-shogi-and-go) - learned from scratch to master Go, chess and shogi. Now, [in a paper in the journal Nature](https://rdcu.be/ccErB), we describe MuZero, a significant step forward in the pursuit of general-purpose algorithms. MuZero masters Go, chess, shogi and Atari without needing to be told the rules, thanks to its ability to plan winning strategies in unknown environments.

For many years, researchers have sought methods that can both learn a model that explains their environment, and can then use that model to plan the best course of action. Until now, most approaches have struggled to plan effectively in domains, such as Atari, where the rules or dynamics are typically unknown and complex.

MuZero, first introduced in a [preliminary paper in 2019](https://deepmind.com/research/publications/Mastering-Atari-Go-Chess-and-Shogi-by-Planning-with-a-Learned-Model), solves this problem by learning a model that focuses only on the most important aspects of the environment for planning. By combining this model with AlphaZero’s powerful lookahead tree search, MuZero set a new state of the art result on the Atari benchmark, while simultaneously matching the performance of AlphaZero in the classic planning challenges of Go, chess and shogi. In doing so, MuZero demonstrates a significant leap forward in the capabilities of reinforcement learning algorithms.

![A comparison chart showing the evolution of DeepMind's algorithms from AlphaGo to MuZero. As the algorithms progress, the number of domains they master increases from only Go to Go, chess, shogi, and Atari, while the required prior knowledge decreases from human data, domain knowledge, and known rules down to none of these inputs for MuZero.](https://lh3.googleusercontent.com/Gy24iLqDpKl4TyH4BcMCFNOkiDlMRg6PbclXrOqhp6stgd8dQZHTabSqonlYa5UOZcv0EcGPhVS0DQK5ZEkFNHkJUom24m1__jIlRvXqkmaTCUOb=w1440)

## Generalising to unknown models

The ability to plan is an important part of human intelligence, allowing us to solve problems and make decisions about the future. For example, if we see dark clouds forming, we might predict it will rain and decide to take an umbrella with us before we venture out. Humans learn this ability quickly and can generalise to new scenarios, a trait we would also like our algorithms to have.

Researchers have tried to tackle this major challenge in AI by using two main approaches: lookahead search or model-based planning.

Systems that use lookahead search, such as AlphaZero, have achieved remarkable success in classic games such as checkers, chess and poker, but rely on being given knowledge of their environment’s dynamics, such as the rules of the game or an accurate simulator. This makes it difficult to apply them to messy real world problems, which are typically complex and hard to distill into simple rules.

Model-based systems aim to address this issue by learning an accurate model of an environment’s dynamics, and then using it to plan. However, the complexity of modelling every aspect of an environment has meant these algorithms are unable to compete in visually rich domains, such as Atari. Until now, the best results on Atari are from model-free systems, such as [DQN](https://www.nature.com/articles/nature14236), [R2D2](https://openreview.net/forum?id=r1lyTjAqYX) and [Agent57](https://arxiv.org/abs/2003.13350). As the name suggests, model-free algorithms do not use a learned model and instead estimate what is the best action to take next.

MuZero uses a different approach to overcome the limitations of previous approaches. Instead of trying to model the entire environment, MuZero just models aspects that are important to the agent’s decision-making process. After all, knowing an umbrella will keep you dry is more useful to know than modelling the pattern of raindrops in the air.

Specifically, MuZero models three elements of the environment that are critical to planning:

- The **value:** how good is the current position?
- The **policy:** which action is the best to take?
- The **reward:** how good was the last action?

These are all learned using a deep neural network and are all that is needed for MuZero to understand what happens when it takes a certain action and to plan accordingly.

![Illustration of how Monte Carlo Tree Search can be used to plan with the MuZero neural networks. Starting at the current position in the game (schematic Go board at the top of the animation), MuZero uses the representation function (h) to map from the observation to an embedding used by the neural network (s0). Using the dynamics function (g) and the prediction function (f), MuZero can then consider possible future sequences of actions (a), and choose the best action.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62277f565ad61d23ae431c30_Fig202.gif)

Illustration of how Monte Carlo Tree Search can be used to plan with the MuZero neural networks. Starting at the current position in the game (schematic Go board at the top of the animation), MuZero uses the representation function (h) to map from the observation to an embedding used by the neural network (s0). Using the dynamics function (g) and the prediction function (f), MuZero can then consider possible future sequences of actions (a), and choose the best action.

![MuZero uses the experience it collects when interacting with the environment to train its neural network. This experience includes both observations and rewards from the environment, as well as the results of searches performed when deciding on the best action.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62277f63a12b691d3d67ff4a_Fig203.gif)

MuZero uses the experience it collects when interacting with the environment to train its neural network. This experience includes both observations and rewards from the environment, as well as the results of searches performed when deciding on the best action.

![During training, the model is unrolled alongside the collected experience, at each step predicting the previously saved information: the value function v predicts the sum of observed rewards (u), the policy estimate (p) predicts the previous search outcome (π), the reward estimate r predicts the last observed reward (u).](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62277f797f22435437106707_Fig204.gif)

During training, the model is unrolled alongside the collected experience, at each step predicting the previously saved information: the value function v predicts the sum of observed rewards (u), the policy estimate (p) predicts the previous search outcome (π), the reward estimate r predicts the last observed reward (u).

This approach comes with another major benefit: MuZero can repeatedly use its learned model to improve its planning, rather than collecting new data from the environment. For example, in tests on the Atari suite, this variant - known as MuZero Reanalyze - used the learned model 90% of the time to re-plan what should have been done in past episodes.

## MuZero performance

We chose four different domains to test MuZeros capabilities. Go, chess and shogi were used to assess its performance on challenging planning problems, while we used the Atari suite as a benchmark for more visually complex problems. In all cases, MuZero set a new state of the art for reinforcement learning algorithms, outperforming all prior algorithms on the Atari suite and matching the superhuman performance of AlphaZero on Go, chess and shogi.

![A comparison table showing MuZero and MuZero Reanalyse outperforming prior RL algorithms like Ape-X, R2D2, IMPALA, Rainbow, UNREAL, and LASER in median and mean score percentages across Atari games, using fewer environment frames.](https://lh3.googleusercontent.com/AswLdUjq0IW4v9UJBJePKFfLO92wZG9KAiZehkr6lSN620UKt-zDpdMpKRwOH2caQngbJiNyE3MPWvod32xxPByjYRrkQMOFZFwrCfPgDfi3DRWZoQ=w1440)

Performance on the Atari suite using either 200M or 20B frames per training run. MuZero achieves a new state of the art in both settings. All scores are normalised to the performance of human testers (100%), with the best results for each setting highlighted in bold.

We also tested how well MuZero can plan with its learned model in more detail. We started with the classic precision planning challenge in Go, where a single move can mean the difference between winning and losing. To confirm the intuition that planning more should lead to better results, we measured how much stronger a fully trained version of MuZero can become when given more time to plan for each move (see left hand graph below). The results showed that playing strength increases by more than 1000 Elo (a measure of a player's relative skill) as we increase the time per move from one-tenth of a second to 50 seconds. This is similar to the difference between a strong amateur player and the strongest professional player.

![Two line graphs showing MuZero performance. Left graph (A) shows playing strength in Elo increasing by over 1000 Elo as search time per move increases from 0.1 to 50 seconds, with similar curves for the Learned Model and Real Simulator. Right graph (D) shows playing strength over millions of training steps on Ms. Pac-Man, with performance improving faster and reaching higher levels as the number of simulations per move increases from 5 to 50.](https://lh3.googleusercontent.com/BDp81lIpTe9oiPsPi3BGoP8fngCD7r8f8ETxB7vBm0BGGWg2F6D6v0et_t6STiVfXn5B8F8_sm2ic395zw8qrW1YwQlRpybkTZEnog4wRVZTJikjwo0=w1440)

Left: Playing strength in Go increases significantly as the time available to plan each move increases. Note how MuZero's scaling almost perfectly matches that of AlphaZero, which has access to a perfect simulator. Right: The score in the Atari game Ms Pac-Man also increases with the amount of planning per move during training. Each plot shows a different training run where MuZero was allowed to consider a different number of simulations per move.

To test whether planning also brings benefits throughout training, we ran a set of experiments on the Atari game Ms Pac-Man (right hand graph above) using separate trained instances of MuZero. Each one was allowed to consider a different number of planning simulations per move, ranging from five to 50. The results confirmed that increasing the amount of planning for each move allows MuZero to both learn faster and achieve better final performance.

Interestingly, when MuZero was only allowed to consider six or seven simulations per move - a number too small to cover all the available actions in Ms Pac-Man - it still achieved good performance. This suggests MuZero is able to generalise between actions and situations, and does not need to exhaustively search all possibilities to learn effectively.

## New horizons

MuZero’s ability to both learn a model of its environment and use it to successfully plan demonstrates a significant advance in reinforcement learning and the pursuit of general purpose algorithms. Its predecessor, AlphaZero, has already been applied to a range of complex problems in [chemistry](https://www.nature.com/articles/nature25978?proof=t), [quantum physics](https://www.nature.com/articles/s41534-019-0241-0) and beyond. The ideas behind MuZero's powerful learning and planning algorithms may pave the way towards tackling new challenges in robotics, industrial systems and other messy real-world environments where the “rules of the game” are not known.

**Related links:**

- MuZero: [Nature Paper](https://rdcu.be/ccErB)
- MuZero talks: [NeurIPS](https://www.youtube.com/watch?v=vt5jOSy7cz8&t=2s) (9 mins, Dec 2019), [ICAPS](https://www.youtube.com/watch?v=L0A86LmH7Yw) (30 mins, Oct 2020)
- MuZero: [Preprint](https://arxiv.org/abs/1911.08265) | [NeurIPS 2019 poster](https://storage.googleapis.com/deepmind-media/research/muzero_poster_neurips_2019.pdf)
- AlphaGo: [Blog](https://ai.googleblog.com/2016/01/alphago-mastering-ancient-game-of-go.html) | [Paper](https://www.nature.com/articles/nature16961)

**Notes**

Design by Adam Cain, Jim Kynvin and Aleksandrs Polozuns
