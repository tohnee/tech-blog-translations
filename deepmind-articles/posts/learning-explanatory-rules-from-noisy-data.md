---
title: "Learning explanatory rules from noisy data"
source: https://deepmind.google/blog/learning-explanatory-rules-from-noisy-data/
site: deepmind
date: 2018-01-29
authors: Richard Evans, Edward Grefenstette
crawled: 2026-09-13
---

Suppose you are playing football. The ball arrives at your feet, and you decide to pass it to the unmarked striker. What seems like one simple action requires two different kinds of thought.

First, you recognise that there is a football at your feet. This recognition requires intuitive perceptual thinking - you cannot easily articulate how you come to know that there is a ball at your feet, you just see that it is there. Second, you decide to pass the ball to a particular striker. This decision requires conceptual thinking. Your decision is tied to a justification - the reason you passed the ball to the striker is because she was unmarked.

The distinction is interesting to us because these two types of thinking correspond to two different approaches to machine learning: deep learning and [symbolic program synthesis](http://www.inductive-programming.org/intro.html). Deep learning concentrates on intuitive perceptual thinking whereas symbolic program synthesis focuses on conceptual, rule-based thinking. Each system has different merits - deep learning systems are robust to noisy data but are difficult to interpret and require large amounts of data to train, whereas symbolic systems are much easier to interpret and require less training data but struggle with noisy data. While human cognition [seamlessly combines](https://davidbarber.github.io/blog/2017/11/07/Learning-From-Scratch-by-Thinking-Fast-and-Slow-with-Deep-Learning-and-Tree-Search/) these two distinct ways of thinking, it is much less clear whether or how it is possible to replicate this in a single AI system.

Our new paper, [recently published in JAIR](https://www.jair.org/index.php/jair), demonstrates it is possible for systems to combine intuitive perceptual with conceptual interpretable reasoning. The system we describe, ∂ILP, is robust to noise, data-efficient, and produces interpretable rules.

![A comparison table showing that Deep Learning is robust to noise and can learn from non-symbolic data but is not data efficient or interpretable. Conversely, Symbolic Program Synthesis is not robust to noise or able to learn from non-symbolic data but is data efficient and interpretable. In contrast to both, the proposed system, ∂ILP, successfully meets all four of these criteria.](https://lh3.googleusercontent.com/W4Jgfh694UAVnMCdIxxNr0oTgJB4qNhQbrm9JD5MrnKg-_b_G1CUBIDkXl2ZwqbIIbUZu4RPuWLFO5OWYk_Rf8PBg0Vzdrj8J-fUyqGhNua1lIux2Q=w1440)

We demonstrate how ∂ILP works with an induction task. It is given a pair of images representing numbers, and has to output a label (0 or 1) indicating whether the number of the left image is less than the number of the right image. Solving this problem involves both kinds of thinking: you need intuitive perceptual thinking to recognise the image as a representation of a particular digit, and you need conceptual thinking to understand the less-than relation in its full generality.

![An illustration of the less-than induction task, displaying pairs of handwritten digit images compared with a less-than sign and labeled with "TRUE" or "FALSE" based on whether the left digit is less than the right digit.](https://lh3.googleusercontent.com/X_kfXD_VMZVmHbQNxxtS3Bm2O_HUpjohSQvlE9k0LTZWwIafaQXYPZ_1MV6kCKc0NKt4Z8glfsHtmYLWJv8WV0_Bwc4BhHdM4Dy4Geq2vg4piT47=w1440)

An example induction task

If you give a standard deep learning model (such as a convolutional neural network with an MLP) sufficient training data, it is able to learn to solve this task effectively. Once it has been trained, you can give it a new pair of images it has never seen before, and it will classify correctly. However, it will only generalise correctly if you give it multiple examples of every pair of digits. The model is good at visual generalisation: generalising to new images, assuming it has seen every pair of digits in the test set (see the green box below). But it is not capable of symbolic generalisation: generalising to a new pair of digits it has not seen before (see the blue box below). Researchers like [Gary Marcus](https://arxiv.org/abs/1801.00631) and [Joel Grus](https://joelgrus.com/2016/05/23/fizz-buzz-in-tensorflow/) have pointed this out in recent, thought-provoking articles.

![Diagram illustrating the difference between visual and symbolic generalisation. The training block shows observed digit pairs "4 < 5" and "5 < 6" alongside unobserved "4 < 6". During testing, "Visual Generalisation" points to a green box containing "New digits, known relations" ("4 < 5" and "5 < 6"), while "Symbolic Generalisation" points to a blue box containing unseen relations "Not observed during training" ("4 < 6").](https://lh3.googleusercontent.com/DI_hrSF5nDVhoeok1eOhiOY6Bda7exdLMeRnwgwpgyeFX5BvYZAJcRvUq9dAEH4-sIGmUbbtnQ997IWkicDfp0DqfOGveXzqwjCV4kiJv6bIxgtluQ=w1440)

∂ILP differs from standard neural nets because it is able to generalise symbolically, and it differs from standard symbolic programs because it is able to generalise visually. It learns explicit programs from examples that are readable, interpretable, and verifiable. ∂ILP is given a partial set of examples (the desired results) and produces a program that satisfies them. It searches through the space of programs using gradient descent. If the outputs of the program conflict with the desired outputs from the reference data, the system revises the program to better match the data.

![A flowchart illustrating the ∂ILP training process. It shows Desired Results feeding as inputs into an Explicit Program block containing code for "lessThan", "foo", and "bar" functions. The program predicts outputs to a Predicted Results block, which are validated against the Desired Results. A training loop continuously revises the Explicit Program based on these predicted results.](https://lh3.googleusercontent.com/po1ukeb5r66BRIkEz9luHxQ0_kp25k-M29dU3lukLctKdCT2vdRgNRbkfiTr6OyUHO8pwADegqP9GDjo3mmM8uAkvDWB8Qw4rgPvn9qygWWkfPnvNA=w1440)

This figure demonstrates the ∂ILP training loop

Our system, ∂ILP, is able to generalise symbolically. Once it has seen enough examples of x < y, y < z, x < z, it will consider the possibility that the < relation is transitive. Once it has realised this general rule, it can apply it to a new pair of numbers it has never seen before.

![A line graph plotting test error against the proportion of unseen pairs during training, comparing a standard deep learning "baseline" (blue line) with "∂ILP" (green line). As the proportion of unseen pairs increases from 0.0 to 0.9, the test error for the baseline rises sharply to over 0.40, while ∂ILP maintains a much lower test error, demonstrating its ability to generalize symbolically to unseen data.](https://lh3.googleusercontent.com/75244dLexhVjIalezJdZzl66It7Qnfr2SzQRZz5JCeO7W_HBgSCKZJJGH3bpwTHuBT2Mv7Rhpn1UoEX4mhb06e0tANixuVNeLVZUf4IXkGD1jDE2kDk=w1440)

Our less-than experiment is summarised above: the standard deep neural network (the blue curve) is unable to generalise correctly to unseen pairs of digits. By contrast, ∂ILP (the green line) is still able to achieve a low test error when it has only seen 40% of the pairs of digits; this shows it is capable of symbolic generalisation.

We believe that our system goes some way to answering the question of whether achieving symbolic generalisation in deep neural networks is possible. In future work, we plan to integrate ∂ILP-like systems into reinforcement learning agents and larger deep learning modules. In doing so, we hope to impart our systems with the ability to reason as well as to react.

**Notes**

Read the paper [here](https://www.jair.org/index.php/jair).
