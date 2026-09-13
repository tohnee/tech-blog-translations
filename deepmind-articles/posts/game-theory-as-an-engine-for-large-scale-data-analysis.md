---
title: "Game theory as an engine for large-scale data analysis"
source: https://deepmind.google/blog/game-theory-as-an-engine-for-large-scale-data-analysis/
site: deepmind
date: 2021-05-06
authors: Brian McWilliams, Ian Gemp, Claire Vernade
crawled: 2026-09-13
---

EigenGame maps out a new approach to solve fundamental ML problems

Modern AI systems approach tasks like [recognising objects in images](https://papers.nips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html) and [predicting the 3D structure of proteins](https://deepmind.com/blog/article/alphafold-a-solution-to-a-50-year-old-grand-challenge-in-biology) as a diligent student would prepare for an exam. By training on many example problems, they minimise their mistakes over time until they achieve success. But this is a solitary endeavour and only one of the known forms of learning. Learning also takes place by interacting and playing with others. It’s rare that a single individual can solve extremely complex problems alone. By allowing problem solving to take on these game-like qualities, previous DeepMind efforts have trained AI agents to play [Capture the Flag](https://deepmind.com/blog/article/capture-the-flag-science) and achieve [Grandmaster level at Starcraft](https://deepmind.com/blog/article/alphastar-mastering-real-time-strategy-game-starcraft-ii). This made us wonder if such a perspective modeled on game theory could help solve other fundamental machine learning problems.

Today at [ICLR 2021](https://iclr.cc/) (the International Conference on Learning Representations), we presented “[EigenGame: PCA as a Nash Equilibrium](https://openreview.net/forum?id=NzTU59SYbNq),” which received an Outstanding Paper Award. Our research explored a new approach to an old problem: we reformulated principal component analysis (PCA), a type of [eigenvalue problem](https://en.wikipedia.org/wiki/Eigendecomposition_of_a_matrix), as a competitive multi-agent game we call EigenGame. PCA is typically formulated as an optimisation problem (or single-agent problem); however, we found that the multi-agent perspective allowed us to develop new insights and algorithms which make use of the latest computational resources. This enabled us to scale to massive data sets that previously would have been too computationally demanding, and offers an alternative approach for future exploration.

## PCA as a Nash equilibrium

First described in the early 1900s, [PCA](https://en.wikipedia.org/wiki/Principal_component_analysis) is a long-standing technique for making sense of the structure of high-dimensional data. This approach is now ubiquitous as a first step in the data-processing pipeline and makes it easy to cluster and visualise data. It can also be a useful tool for learning low-dimensional representations for regression and classification. More than a century later, there are still compelling reasons to study PCA.

Firstly, data was originally recorded by hand in paper notebooks, and now it is stored in data centres the size of warehouses. As a result, this familiar analysis has become a computational bottleneck. Researchers have explored [randomised algorithms](https://arxiv.org/abs/0909.4061) and other directions to improve how PCA scales, but we found that these approaches have difficulty scaling to massive datasets because they are unable to fully harness recent deep-learning-centric advances in computation — namely access to many parallel GPUs or TPUs.

Secondly, PCA shares a common solution with many important ML and engineering problems, namely the [singular value decomposition](https://en.wikipedia.org/wiki/Singular_value_decomposition) (SVD). By approaching the PCA problem in the right way, our insights and algorithms apply more broadly across the branches of the ML tree.

![An illustration of the "ML tree" with roots labeled "SVD" branching into a brain-shaped tree crown containing circles representing machine learning concepts: PCA, Least Squares, Spectral Clustering, PVF, LSI, and Sorting.](https://lh3.googleusercontent.com/P5RV6oEE0BzEroaVUYlFOUSgOzr3QLwOdHa77-BlYwkSubeILRTjhkIg1pdb6eVNs6O8v16qYKCdnTcIuTjMKPo_l6H3vbdgzu5E0bzN83SgULF4=w1440)

Figure 1. With SVD at its roots, the tree of knowledge encompasses many fundamental ideas in machine learning including PCA, Least Squares, Spectral Clustering, Proto Value Functions, Latent Semantic Indexing, and Sorting.

As with any board game, in order to reinvent PCA as a game we need a set of rules and objectives for players to follow. There are many possible ways to design such a game; however, important ideas come from PCA itself: the optimal solution consists of eigenvectors which capture the important variance in the data and are orthogonal to each other.

![An illustration representing PCA as a game, showing a scatter plot of data points with two orthogonal vector arrows, labeled "Player 1" (blue) aligned with the direction of maximum variance, and "Player 2" (pink) orthogonal to it.](https://lh3.googleusercontent.com/nMwA723PiBoJDNTjJ4erYB-IJmm58-grtE47prwxe4B-9rQxPdP9XicouqsQfmmD28M7kVExqP1K5pP0ettVoVdvBn25ECqpQb-qfwzSN7h5XndoDA=w1440)

Figure 2. Each player wants to align with a direction of maximum variance (larger data spread) but also remain perpendicular to players higher up in the hierarchy (all players with a lower number).

In EigenGame each player controls an eigenvector. Players increase their score by explaining variance within the data but are penalised if they’re too closely aligned to other players. We also establish a hierarchy: Player 1 only cares about maximising variance, whereas other players also have to worry about minimising their alignment with players above them in the hierarchy. This combination of rewards and penalties defines each player’s utility.

![An illustration showing the mathematical equation for utility in EigenGame, calculated as the variance term minus the sum of alignment terms. The variance term is illustrated with a scatter plot and a diagonal vector, while the alignment term is depicted with orthogonal red and blue vectors.](https://lh3.googleusercontent.com/8sy0BGzdnswoFSHFG9j1N9d9v5yIk5-D83zEXh5NcK7x4a5LgIEGYVRd-OuPrdbMyRJQB1-X5N7HLJaA4BGf7XZ-tJP-Ppfd4KmmBbvJZ0oIxaseTms=w1440)

Figure 3. Summarising the utility of each player above.

With appropriately designed **Var** and **Align** terms, we can show that:

- If all players play optimally, together they achieve the [Nash equilibrium](https://en.wikipedia.org/wiki/Nash_equilibrium) of the game, which is the PCA solution.
- This can be achieved if each player maximises their utility independently and simultaneously using gradient ascent.

![An illustration of 3D vectors converging on a sphere: on the left, the "True Eigenvectors" labeled V1 (blue), V2 (pink), and V3 (teal) are orthogonal; on the right, three corresponding paths of colored dots starting from open circles (Start) trace trajectories across a wireframe sphere to align with these true eigenvectors at arrowheads (Finish).](https://lh3.googleusercontent.com/TetiQUjXs4WHCllUvxk898iSHEzofUiKPrgS6cBRlKGr16F9DFtSt2m95tf_wvO73_U-wUAn1LK4mLe0LAnL_kw_RwytRVP7papsWTOKiu0oqIrnBg=w1440)

Figure 4. EigenGame guides each player along the unit sphere from the empty circles to the arrows in parallel. Blue is player 1. Red is player 2. Green is player 3.

This independence property of simultaneous ascent is particularly important because it allows for the computation to be distributed across dozens of Google Cloud TPUs, enabling both data- and model-parallelism. This makes it possible for our algorithm to adapt to truly large-scale data. EigenGame finds the principal components in a matter of hours for hundred-terabyte datasets comprising millions of features or billions of rows.

![An illustration comparing model-parallel data distribution: on the left, a 3x3 grid assigns different players (V1, V2, V3, VK-2, VK-1, VK) to single compute devices; on the right, players are distributed across larger pools of grouped devices to achieve greater scale.](https://lh3.googleusercontent.com/q-34Fz9ZOZ6stlScBEd1a12GLLv0MTBlNc8LwljNk7OMaZZKs6ZXlt7Jzt_c25aN5mauMH73dkle-uXyLKNpeEYTfaivJ_ai_bHkhlolQADkrzsTJw=w1440)

Figure 5. Each coloured square is a separate device. (L) Each player lives and computes updates on a single device. (R) Each player is copied to multiple devices and computes updates using independent batches of data; the different updates are then averaged to form a more robust update direction.

## Utilities, updates, and everything in between

By thinking about PCA from a multi-agent perspective, we were able to propose scalable algorithms and novel analyses. We also uncovered a surprising connection to [Hebbian Learning](https://en.wikipedia.org/wiki/Hebbian_theory) — or, how neurons adapt when learning. In EigenGame, each player maximising their utilities gives rise to update equations that are similar to [update rules](https://en.wikipedia.org/wiki/Generalized_Hebbian_algorithm) derived from Hebbian models of synaptic plasticity in the brain. Hebbian updates are known to converge to the PCA solution but are not derived as the gradient of any utility function. Game theory gives us a fresh lens to view Hebbian learning, and also suggests a continuum of approaches to machine learning problems.

On one end of the ML continuum is the well-developed path of proposing an objective function that can be optimised: Using the theory of convex and non-convex optimisation, researchers can reason about the global properties of the solution. On the other end, pure [connectionist](https://en.wikipedia.org/wiki/Connectionism) methods and update rules inspired by neuroscience are specified directly, but analysis of the entire system can be more difficult, often invoking the study of complicated [dynamical systems](https://en.wikipedia.org/wiki/Dynamical_system).

Game theoretic approaches like EigenGame sit somewhere in between. Player updates are not constrained to be the gradient of a function, only a best response to the current strategies of the other players. We’re free to design utilities and updates with desirable properties — for example, specifying updates which are unbiased or accelerated — while ensuring the Nash property still allows us to analyse the system as a whole.

![A gradient bar illustrating a continuum of machine learning approaches, from left to right: "Utility (Optimisation)", "Multiple Utilities (Multi-agent/Game Theory)" in the center, and "Utility-Free (Hebbian/Dynamical System)" on the right.](https://lh3.googleusercontent.com/t5DveiWbra5YVGYTotrspJD8jsXc7VyJ244iO8mb19E6N3Feman7vWdOoMkJ5B8o871wKwQwRTMmXEa15TROdgxhQZC3GKkvhAhHj9Hj0dhLRdBb=w1440)

Figure 6: Allowing multiple utilities bridges the gap between optimisation approaches and dynamical systems.

EigenGame represents a concrete example of designing the solution to a machine learning problem as the output of a large multi-agent system. More generally, designing machine learning problems as multi-agent games is a challenging mechanism design problem; however, researchers have already used the class of two-player, [zero-sum](https://en.wikipedia.org/wiki/Zero-sum_game) games to solve machine learning problems. Most notably, the success of [generative adversarial networks](https://papers.nips.cc/paper/2014/file/5ca3e9b122f61f8f06494c97b1afccf3-Paper.pdf) (GANs) as an approach to generative modelling has driven interest in the relationship between game theory and machine learning.

EigenGame moves beyond this to the more complex many-player, general-sum setting. This enables more obvious parallelism for greater scale and speed. It also presents a quantitative benchmark for the community to test novel multi-agent algorithms alongside richer domains, such as [Diplomacy](https://deepmind.com/research/publications/Learning-to-Play-No-Press-Diplomacy-with-Best-Response-Policy-Iteration) and [Soccer](https://deepmind.com/research/publications/emergent-coordination-through-competition).

We hope our blueprint for designing utilities and updates will encourage others to explore this direction for designing new algorithms, agents, and systems. We’re looking forward to seeing what other problems can be formulated as games and whether the insights we glean will further improve our understanding of the multi-agent nature of intelligence.

For more details see our paper [EigenGame: PCA as a Nash Equilibrium](https://openreview.net/forum?id=NzTU59SYbNq) and our follow-up work [EigenGame Unloaded: When playing games is better than optimising](https://arxiv.org/abs/2102.04152).

**Notes**

This blog post is based on joint work with Thore Graepel, a research group lead at DeepMind and Chair of Machine Learning at University College London.

We would like to thank Rob Fergus for their technical feedback on this post as well as Sean Carlson, Jon Fildes, Dominic Barlow, Mario Pinto, and Emma Yousif for pulling this all together.

Custom figures by Jim Kynvin and Adam Cain.
