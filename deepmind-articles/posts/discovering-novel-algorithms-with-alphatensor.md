---
title: "Discovering novel algorithms with AlphaTensor"
source: https://deepmind.google/blog/discovering-novel-algorithms-with-alphatensor/
site: deepmind
date: 2022-10-05
authors: Alhussein Fawzi, Matej Balog, Bernardino Romera-Paredes, Demis Hassabis, Pushmeet Kohli
crawled: 2026-09-13
---

First extension of AlphaZero to mathematics unlocks new possibilities for research

Algorithms have helped mathematicians perform fundamental operations for thousands of years. The ancient Egyptians created an algorithm to multiply two numbers without requiring a multiplication table, and Greek mathematician Euclid described an algorithm to compute the greatest common divisor, which is still in use today.

During the Islamic Golden Age, Persian mathematician [Muhammad ibn Musa al-Khwarizmi](https://en.wikipedia.org/wiki/Muhammad_ibn_Musa_al-Khwarizmi) designed new algorithms to solve linear and quadratic equations. In fact, al-Khwarizmi’s name, translated into Latin as Algoritmi, led to the term algorithm. But, despite the familiarity with algorithms today – used throughout society from classroom algebra to cutting edge scientific research – the process of discovering new algorithms is incredibly difficult, and an example of the amazing reasoning abilities of the human mind.

In our [paper](https://www.nature.com/articles/s41586-022-05172-4), published today in Nature, we introduce AlphaTensor, the first artificial intelligence (AI) system for discovering novel, efficient, and provably correct algorithms for fundamental tasks such as matrix multiplication. This sheds light on a 50-year-old open question in mathematics about finding the fastest way to multiply two matrices.

This paper is a stepping stone in DeepMind’s mission to advance science and unlock the most fundamental problems using AI. Our system, AlphaTensor, builds upon AlphaZero, an agent that has shown superhuman performance on board games, like chess, Go and shogi, and this work shows the journey of AlphaZero from playing games to tackling unsolved mathematical problems for the first time.

## Matrix multiplication

Matrix multiplication is one of the simplest operations in algebra, commonly taught in high school maths classes. But outside the classroom, this humble mathematical operation has enormous influence in the contemporary digital world and is ubiquitous in modern computing.

![A diagram illustrating matrix multiplication of two 3x3 matrices, highlighting the dot product of a row in the first matrix and a column in the second matrix to compute a single entry in the resulting matrix.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/633c31b866f7323281c5adaf_633c1c9aaaf084ffbeed2333_MM_Fig1.svg)

Example of the process of multiplying two 3x3 matrices.

This operation is used for processing images on smartphones, recognising speech commands, generating graphics for computer games, running simulations to predict the weather, compressing data and videos for sharing on the internet, and so much more. Companies around the world spend large amounts of time and money developing computing hardware to efficiently multiply matrices. So, even minor improvements to the efficiency of matrix multiplication can have a widespread impact.

For centuries, mathematicians believed that the standard matrix multiplication algorithm was the best one could achieve in terms of efficiency. But in 1969, German mathematician Volker Strassen [shocked the mathematical community](https://link.springer.com/article/10.1007/BF02165411) by showing that better algorithms do exist.

![A side-by-side comparison illustrating how to multiply two 2x2 matrices using the standard algorithm, which requires 8 multiplications (h1 through h8), versus Strassen's algorithm, which reduces the process to 7 multiplications (h1 through h7) by ingeniously combining the matrix entries.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/633c31b82381e038cc3a90ea_633c1d0f5ed3f701034748c5_MM_Fig2.svg)

Standard algorithm compared to Strassen’s algorithm, which uses one less scalar multiplication (7 instead of 8) for multiplying 2x2 matrices. Multiplications matter much more than additions for overall efficiency.

Through studying very small matrices (size 2x2), he discovered an ingenious way of combining the entries of the matrices to yield a faster algorithm. Despite decades of research following Strassen’s breakthrough, larger versions of this problem have remained unsolved – to the extent that it’s not known how efficiently it’s possible to multiply two matrices that are as small as 3x3.

In our paper, we explored how modern AI techniques could advance the automatic discovery of new matrix multiplication algorithms. Building on the progress of human intuition, AlphaTensor discovered algorithms that are more efficient than the state of the art for many matrix sizes. Our AI-designed algorithms outperform human-designed ones, which is a major step forward in the field of algorithmic discovery.

## The process and progress of automating algorithmic discovery

First, we converted the problem of finding efficient algorithms for matrix multiplication into a single-player game. In this game, the board is a three-dimensional tensor (array of numbers), capturing how far from correct the current algorithm is. Through a set of allowed moves, corresponding to algorithm instructions, the player attempts to modify the tensor and zero out its entries. When the player manages to do so, this results in a provably correct matrix multiplication algorithm for any pair of matrices, and its efficiency is captured by the number of steps taken to zero out the tensor.

This game is incredibly challenging – the number of possible algorithms to consider is much greater than the number of atoms in the universe, even for small cases of matrix multiplication. Compared to the game of Go, which remained [a challenge for AI for decades](https://www.deepmind.com/research/highlighted-research/alphago), the number of possible moves at each step of our game is 30 orders of magnitude larger (above 1033 for one of the settings we consider).

Essentially, to play this game well, one needs to identify the tiniest of needles in a gigantic haystack of possibilities. To tackle the challenges of this domain, which significantly departs from traditional games, we developed multiple crucial components including a novel neural network architecture that incorporates problem-specific inductive biases, a procedure to generate useful synthetic data, and a recipe to leverage symmetries of the problem.

We then trained an AlphaTensor agent using reinforcement learning to play the game, starting without any knowledge about existing matrix multiplication algorithms. Through learning, AlphaTensor gradually improves over time, re-discovering historical fast matrix multiplication algorithms such as Strassen’s, eventually surpassing the realm of human intuition and discovering algorithms faster than previously known.

![Diagram showing the step-by-step reinforcement learning loop of AlphaTensor, where the agent modifies a three-dimensional tensor grid representing the current algorithm state to discover new algorithms.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/633c31b879d44219c89ee786_633c1dbed481f1536ecc0ad1_MM_Fig3.svg)

Single-player game played by AlphaTensor, where the goal is to find a correct matrix multiplication algorithm. The state of the game is a cubic array of numbers (shown as grey for 0, blue for 1, and green for -1), representing the remaining work to be done.

For example, if the traditional algorithm taught in school multiplies a 4x5 by 5x5 matrix using 100 multiplications, and this number was reduced to 80 with human ingenuity, AlphaTensor has found algorithms that do the same operation using just 76 multiplications.

![A diagram illustrating AlphaTensor's 76-step algorithm for multiplying a 4x5 matrix by a 5x5 matrix, listing the formulas for factors h1 through h76 and the resulting entries of matrix C.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/633c31b8194b542332281409_633c1e36d481f1811ccc110b_MM_Fig4.svg)

Algorithm discovered by AlphaTensor using 76 multiplications, an improvement over state-of-the-art algorithms.

Beyond this example, AlphaTensor’s algorithm improves on Strassen’s two-level algorithm in a finite field for the first time since its discovery 50 years ago. These algorithms for multiplying small matrices can be used as primitives to multiply much larger matrices of arbitrary size.

Moreover, AlphaTensor also discovers a diverse set of algorithms with state-of-the-art complexity – up to thousands of matrix multiplication algorithms for each size, showing that the space of matrix multiplication algorithms is richer than previously thought.

Algorithms in this rich space have different mathematical and practical properties. Leveraging this diversity, we adapted AlphaTensor to specifically find algorithms that are fast on a given hardware, such as Nvidia V100 GPU, and Google TPU v2. These algorithms multiply large matrices 10-20% faster than the commonly used algorithms on the same hardware, which showcases AlphaTensor’s flexibility in optimising arbitrary objectives.

![A flowchart illustrating how AlphaTensor designs new tailored algorithms. An initial "Problem specification" representing matrix multiplication leads to the "AlphaTensor" system. A bidirectional arrow shows AlphaTensor has "Black box access to hardware" (illustrated by a GPU icon). This process results in a "New tailored algorithm" shown as a blue grid.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/633c31b82381e06d7f3a90e9_633c1e777cc74cc57c3960c3_MM_V4.svg)

AlphaTensor with an objective corresponding to the runtime of the algorithm. When a correct matrix multiplication algorithm is discovered, it's benchmarked on the target hardware, which is then fed back to AlphaTensor, in order to learn more efficient algorithms on the target hardware.

## Exploring the impact on future research and applications

From a mathematical standpoint, our results can guide further research in complexity theory, which aims to determine the fastest algorithms for solving computational problems. By exploring the space of possible algorithms in a more effective way than previous approaches, AlphaTensor helps advance our understanding of the richness of matrix multiplication algorithms. Understanding this space may unlock new results for helping determine the asymptotic complexity of matrix multiplication, [one of the most fundamental open problems in computer science](https://www.cambridge.org/core/books/geometry-and-complexity-theory/15E3ABA3FF14E1054574663F60250D80#fndtn-information).

Because matrix multiplication is a core component in many computational tasks, spanning computer graphics, digital communications, neural network training, and scientific computing, AlphaTensor-discovered algorithms could make computations in these fields significantly more efficient. AlphaTensor’s flexibility to consider any kind of objective could also spur new applications for designing algorithms that optimise metrics such as energy usage and numerical stability, helping prevent small rounding errors from snowballing as an algorithm works.

While we focused here on the particular problem of matrix multiplication, we hope that our paper will inspire others in using AI to guide algorithmic discovery for other fundamental computational tasks. Our research also shows that AlphaZero is a powerful algorithm that can be extended well beyond the domain of traditional games to help solve open problems in mathematics. Building upon our research, we hope to spur on a greater body of work – applying AI to help society solve some of the most important challenges in mathematics and across the sciences.

You can find more information in [AlphaTensor's GitHub repository](https://github.com/deepmind/alphatensor).

**Acknowledgements**

Francisco R. Ruiz, Thomas Hubert, Alexander Novikov, Alex Gaunt for feedback on the blog post. Sean Carlson, Arielle Bier, Gabriella Pearl, Katie McAtackney, Max Barnett for their help with text and figures. This work was done by a team with contributions from Alhussein Fawzi, Matej Balog, Aja Huang, Thomas Hubert, Bernardino Romera-Paredes, Mohammadamin Barekatain, Francisco Ruiz, Alexander Novikov, Julian Schrittwieser, Grzegorz Swirszcz, David Silver, Demis Hassabis, and Pushmeet Kohli.
