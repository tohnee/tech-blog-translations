---
title: "Learning Robust Real-Time Cultural Transmission without Human Data"
source: https://deepmind.google/blog/learning-robust-real-time-cultural-transmission-without-human-data/
site: deepmind
date: 2022-03-03
authors: Cultural General Intelligence team
crawled: 2026-09-13
---

Over millennia, humankind has discovered, evolved, and accumulated a wealth of cultural knowledge, from navigation routes to mathematics and social norms to works of art. Cultural transmission, defined as efficiently passing information from one individual to another, is the inheritance process underlying this exponential increase in human capabilities.

Our agent, in blue, imitates and remembers the demonstration of both bots (left) and humans (right), in red.

For more videos of our agents in action, visit our [website](https://sites.google.com/view/dm-cgi).

In this work, we use deep reinforcement learning to generate artificial agents capable of test-time cultural transmission. Once trained, our agents can infer and recall navigational knowledge demonstrated by experts. This knowledge transfer happens in real time and generalises across a vast space of previously unseen tasks. For example, our agents can quickly learn new behaviours by observing a single human demonstration, without ever training on human data.

![Diagram illustrating the reinforcement learning environment, featuring details on procedurally generated 3D worlds, the red "Expert" and blue "MEDAL-ADR" agent players, available actions and sensors, and examples of complex navigation games.](https://lh3.googleusercontent.com/kMuCeakChRUqxlFuWtuXEwMZ4oqLxxjf9qK43ZPZme0MStAVHgebEptMvy4s36jN-wKdyzBIKuwKZjjb_1iaK0M7F-p14eOa1VQn_1XnwbjUaq1elw=w1440)

A summary of our reinforcement learning environment. The tasks are navigational representatives for a broad class of human skills, which require particular sequences of strategic decisions, such as cooking, wayfinding, and problem solving.

We train and test our agents in procedurally generated 3D worlds, containing colourful, spherical goals embedded in a noisy terrain full of obstacles. A player must navigate the goals in the correct order, which changes randomly on every episode. Since the order is impossible to guess, a naive exploration strategy incurs a large penalty. As a source of culturally transmitted information, we provide a privileged “bot” that always enters goals in the correct sequence.

![Line graph plotting cultural transmission against training time in hours, comparing the MEDAL agent (blue line) against ME-AL (orange dashed line) and Best seed (grey line). MEDAL shows higher cultural transmission performance over time than ME-AL.](https://lh3.googleusercontent.com/Bw02zYeKnwjZRkUXOJlX8rCwxlGXzJVHZbgST72X56JKBIYFIYkGRtZ89dTsMlzELELGV1u9OnqZaBtPvzaq_Cz8dzEGp3DxTi7_tcXzyOPTGZaohA=w1440)

![Line graph comparing the cultural transmission performance of different agent architectures over 250+ hours of training. The MEDAL-ADR agent (solid dark blue line) outperforms its ablation variants, MEDAL--DR (dashed purple line) and MEDAL---- (pink dash-dot line), while trailing just below the Best seed baseline (thin grey line).](https://lh3.googleusercontent.com/2JzDYGMIPOHUwH62XG9awAs5rkRBAtb8iC2hBarwS0OZ7FcnKT5n1JyiyJ4xBnAtqpdOaIPwABArXMfdh5UqWhscwoOresrR8_dAOiVfdBgIm1Ioqg=w1440)

Our MEDAL(-ADR) agent outperforms ablations on held-out tasks, in worlds without obstacles (top) and with obstacles (bottom).

Via ablations, we identify a minimal sufficient "starter kit" of training ingredients required for cultural transmission to emerge, dubbed MEDAL-ADR. These components include memory (M), expert dropout (ED), attentional bias towards the expert (AL), and automatic domain randomization (ADR). Our agent outperforms the ablations, including the state-of-the-art method (ME-AL), across a range of challenging held-out tasks. Cultural transmission generalises out of distribution surprisingly well, and the agent recalls demonstrations long after the expert has departed. Looking into the agent's brain, we find strikingly interpretable neurons responsible for encoding social information and goal states.

![Bar chart evaluating cultural transmission generalization, plotting normalized scores for 4-goal, 5-goal, and 6-goal game configurations across different numbers of path crossings. Solid blue bars represent in-distribution tasks (5-goals), and patterned blue bars represent out-of-distribution tasks (4-goals and 6-goals), with performance compared against baselines for perfect following (red dashed line at 1.0) and perfect remembering (blue dotted line at 2.0).](https://lh3.googleusercontent.com/6A8VBVW2-U3zlscxjOzlVBM8mrwCHvL1IYCbrEFaDWM_L5vUU-FJkBHJGnlyuISPpgmi_OKQ5Y9P5zW8Md5DeH2TR4egnqUGUMXq47PRfJnGa-typvI=w1440)

![Line graph showing agent neural activation over episode steps. In the first half, when the expert is present (dark blue dots), activation averages around 0.00. In the second half, when the expert is absent (orange dots), activation jumps higher and stabilizes around 0.15.](https://lh3.googleusercontent.com/ose4b2I2r9QyANTNZmxTPicVrWtFKDMHg93ceb2KsBjUvacPyzUQH9Mb2D25yfXaaIyhKtXzVc0tz1WAQ0kDPKSLZRbVBxDqNqh5Iuh7YlbabS1UD2E=w1440)

Our agent generalises outside the training distribution (top) and possesses individual neurons that encode social information (bottom).

In summary, we provide a procedure for training an agent capable of flexible, high-recall, real-time cultural transmission, without using human data in the training pipeline. This paves the way for cultural evolution as an algorithm for developing more generally intelligent artificial agents.

This authors' notes is based on joint work by the Cultural General Intelligence Team: Avishkar Bhoopchand, Bethanie Brownfield, Adrian Collister, Agustin Dal Lago, Ashley Edwards, Richard Everett, Alexandre Fréchette, Edward Hughes, Kory W. Mathewson, Piermaria Mendolicchio, Yanko Oliveira, Julia Pawar, Miruna Pîslar, Alex Platonov, Evan Senter, Sukhdeep Singh, Alexander Zacherl, and Lei M. Zhang.

Read the full paper [here](https://arxiv.org/abs/2203.00715).
