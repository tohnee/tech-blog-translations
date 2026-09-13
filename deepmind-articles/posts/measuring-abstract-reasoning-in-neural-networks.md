---
title: "Measuring abstract reasoning in neural networks"
source: https://deepmind.google/blog/measuring-abstract-reasoning-in-neural-networks/
site: deepmind
date: 2018-07-11
authors: Adam Santoro, David Barrett, Ari Morcos, Timothy Lillicrap, Felix Hill
crawled: 2026-09-13
---

Neural network-based models continue to achieve impressive results on longstanding machine learning problems, but establishing their capacity to reason about abstract concepts has proven difficult. Building on previous efforts to solve this important feature of general-purpose learning systems, our [latest paper](http://proceedings.mlr.press/v80/santoro18a/santoro18a.pdf) sets out an approach for measuring abstract reasoning in learning machines, and reveals some important insights about the nature of generalisation itself.

To understand why abstract reasoning is critical for general intelligence, consider Archimedes’ famous “Eureka!” moment: by noticing that the volume of an object is equivalent to the volume of water that the object displaces, he understood volume at a conceptual level, and was therefore able to reason about the volume of other irregularly shaped objects.

We would like AI to have similar capabilities. While current systems can defeat world champions in complicated strategic games, they often struggle on other apparently simple tasks, especially when an abstract concept needs to be discovered and reapplied in a new setting. For example, if specifically trained to only count triangles, then even our best AI systems can still fail to count squares, or any other previously unencountered object.

To build better, more intelligent systems it is therefore important to understand the ways in which neural networks are currently able to process abstract concepts, and where they still need improvement. To begin doing this, we took inspiration from the methods used to measure abstract reasoning in human IQ tests.

## Creating an abstract reasoning dataset

Standard human IQ tests often require test-takers to interpret perceptually simple visual scenes by applying principles that they have learned through everyday experience. For example, human test-takers may have already learned about ‘progressions’ (the notion that some attribute can increase) by watching plants or buildings grow, by studying addition in a mathematics class, or by tracking a bank balance as interest accrues. They can then apply this notion in the puzzles to infer that the number of shapes, their sizes, or even the intensity of their colour will increase along a sequence.

We do not yet have the means to expose machine learning agents to a similar stream of ‘everyday experiences’, meaning we cannot easily measure their ability to transfer knowledge from the real world to visual reasoning tests. Nonetheless, we can create an experimental set-up that still puts human visual reasoning tests to good use. Rather than study knowledge transfer from everyday life to visual reasoning problems (as in human testing), we instead studied knowledge transfer from one controlled set of visual reasoning problems to another.

To achieve this, we built a generator for creating matrix problems, involving a set of abstract factors, including relations like ‘progression’ and attributes like ‘colour’ and ‘size’. While the question generator uses a small set of underlying factors, it can nonetheless create an enormous number of unique questions.

Next, we constrained the factors or combinations available to the generator to create different sets of problems for training and testing our models, to measure how well our models can generalise to held-out test sets. For instance, we created a training set of puzzles in which the progression relation is only encountered when applied to the colour of lines, and a test set when it is applied to the size of shapes. If a model performs well on this test set, it would provide evidence for an ability to infer and apply the abstract notion of progression, even in situations in which it had never previously seen a progression.

## Promising evidence of abstract reasoning

In the typical generalisation regime applied in machine learning evaluations, where training and test data are sampled from the same underlying distribution, all of the networks we tested exhibited good generalisation error, with some achieving impressive absolute performance at just above 75%. The best performing network explicitly computed relations between different image panels and evaluated the suitability of each potential answer in parallel. We call this architecture a Wild Relation Network (WReN).

When required to reason using attribute values ‘interpolated’ between previously seen attribute values, and also when applying known abstract relations in unfamiliar combinations, the models generalised notably well. However, the same network performed much worse in the ‘extrapolation’ regime, where attribute values in the test set did not lie within the same range as those seen during training. An example of this occurs for puzzles that contain dark coloured objects during training and light coloured objects during testing. Generalisation performance was also worse when the model was trained to apply a previously seen relation, such as a progression on the number of shapes, to a new attribute, such as size.

Finally, we observed improved generalisation performance when the model was trained to predict not only the correct answer, but also the ‘reason’ for the answer (i.e. the particular relations and attributes that should be considered to solve the puzzle). Interestingly, in the neutral split, the model’s accuracy was strongly correlated with its ability to infer the correct relation underlying the matrix: when the explanation was right, the model would choose the correct answer 87% of the time, but when its explanation was wrong this performance dropped to only 32%. This suggests that models which achieved better performance when they correctly inferred the abstract concepts underlying the task.

## A more nuanced approach to generalisation

Recent literature has focussed on the strengths and weaknesses of neural network-based approaches to machine learning problems, often based around their capacity or failure to generalise. Our results show that it might be unhelpful to draw universal conclusions about generalisation: the neural networks we tested performed well in certain regimes of generalisation and very poorly in others. Their success was determined by a range of factors, including the architecture of the model used and whether the model was trained to provide an interpretable “reason” for its answer choices. In almost all cases, the systems performed poorly when required to extrapolate to inputs beyond their experience, or to deal with entirely unfamiliar attributes; creating a clear focus for future work in this critical, and important area of research.

**Notes**

To encourage and support further research towards improved generalisation and abstract reasoning, we have made our dataset publicly available [here](https://github.com/deepmind/abstract-reasoning-matrices).

Download the paper [[PDF](http://proceedings.mlr.press/v80/santoro18a/santoro18a.pdf)] and supplementary material [[PDF](http://proceedings.mlr.press/v80/santoro18a/santoro18a-supp.pdf)].

**This work was done by David G. T. Barrett\*, Felix Hill\*, Adam Santoro\*, Ari Morcos and Timothy Lillicrap.**
