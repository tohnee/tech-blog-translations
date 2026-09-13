---
title: "Intuitive physics learning in a deep-learning model inspired by developmental psychology"
source: https://deepmind.google/blog/intuitive-physics-learning-in-a-deep-learning-model-inspired-by-developmental-psychology/
site: deepmind
date: 2022-07-11
authors: Luis Perez, Ari Weinstein, Peter Battaglia, Matt Botvinick
crawled: 2026-09-13
---

Understanding the physical world is a critical skill that most people deploy effortlessly. However, this still poses a challenge to artificial intelligence; if we’re to deploy safe and helpful systems in the real world, we want these models to share our intuitive sense of physics. But before we can build those models, there is another challenge: How will we measure the ability of these models to understand the physical world? That is, what does it mean to understand the physical world and how can we quantify it?

Luckily for us, developmental psychologists have spent decades studying what infants know about the physical world. Along the way, they've carved the nebulous notion of physical knowledge into a concrete set of physical concepts. And, they've developed the violation-of-expectation (VoE) paradigm for testing those concepts in infants.

In our paper published today in Nature Human Behavior, we extended their work and open-sourced the [Physical Concepts dataset](https://github.com/deepmind/physical_concepts). This synthetic video dataset ports the VoE paradigm to assess five physical concepts: solidity, object persistence, continuity, “unchangeableness'', and directional inertia.

With a benchmark for physical knowledge in hand, we turned to the task of building a model capable of learning about the physical world. Again, we looked to developmental psychologists for inspiration. Researchers not only catalogued what infants know about the physical world, they also posited the mechanisms that could enable this behaviour. Despite variability, these accounts have a central role for the notion of breaking up the physical world into a set of objects which evolve through time.

Inspired by this work, we built a system that we nickname PLATO (Physics Learning through Auto-encoding and Tracking Objects). PLATO represents and reasons about the world as a set of objects. It makes predictions about where objects will be in the future based on where they've been in the past and what other objects they're interacting with.

After training PLATO on videos of simple physical interactions, we found that PLATO passed the tests in our Physical Concepts dataset. Furthermore, we trained "flat" models that were as big (or even bigger) than PLATO but did not use object-based representations. When we tested those models, we found they didn't pass all of our tests. This suggests that objects are helpful for learning intuitive physics, supporting hypotheses from the developmental literature.

We also wanted to determine how much experience was needed to develop this capacity. Evidence for physical knowledge has been shown in infants as young as two and a half months of age. How does PLATO fare in comparison? By varying the amount of training data used by PLATO, we found that PLATO could learn our physical concepts with as little as 28 hours of visual experience. The limited and synthetic nature of our dataset means we cannot make a like-for-like comparison between the amount of visual experiences received by infants and PLATO. However, this result suggests that intuitive physics can be learned with relatively little experience if supported via an inductive bias for representing the world as objects.

Finally, we wanted to test PLATO's ability to generalise. In the Physical Concepts dataset, all of the objects in our test set are also present in the training set. What if we tested PLATO with objects it had never seen before? To do this, we leveraged a subset of another synthetic [dataset](http://physadept.csail.mit.edu/) developed by researchers at MIT. This dataset also probes physical knowledge, albeit with different visual appearances and a set of objects that PLATO has never seen before. PLATO passed, without any re-training, despite being tested on entirely new stimuli.

We hope this dataset can provide researchers with a more specific understanding of their model’s abilities to understand the physical world. In the future, this can be expanded to test more aspects of intuitive physics by increasing the list of physical concepts tested, and using richer visual stimuli including new object shapes or even real-world videos.
