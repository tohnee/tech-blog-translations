---
title: "Random Forest Feature Sampling at Each Tree or Node"
source: https://sebastianraschka.com/faq/docs/random-forest-feature-subsets.html
crawled: 2026-09-06
---

# Random Forest Feature Sampling at Each Tree or Node

That’s a good question, since the earlier random decision forests by Tin Kam Ho used the “random subspace method,” where each tree got a random subset of features.

> “Our method relies on an autonomous, pseudo-random procedure to select a small number of dimensions from a given feature space …”

- Ho, Tin Kam. “The random subspace method for constructing decision forests.” IEEE transactions on pattern analysis and machine intelligence 20.8 (1998): 832-844.

However, a few years later, Leo Breiman described the procedure of selecting different subsets of features for each node (while a tree was given the full set of features) — Leo Breiman’s formulation has become the “trademark” random forest algorithm that we typically refer to these days when we speak of “random forest”

> “… random forest with random features is formed by selecting at random, at each node, a small group of input variables to split on.”

- Breiman, Leo. “Random Forests” Machine learning 45.1 (2001): 5-32.

To answer your question: Each tree gets the full set of features, but at each node, only a random subset of features is considered.
