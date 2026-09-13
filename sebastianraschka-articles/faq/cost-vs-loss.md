---
title: "Cost Functions vs. Loss Functions in Machine Learning"
source: https://sebastianraschka.com/faq/docs/cost-vs-loss.html
crawled: 2026-09-06
---

# Cost Functions vs. Loss Functions in Machine Learning

The terms *cost* and *loss* functions are synonymous (some people also call it error function). The more general scenario is to define an objective function first, which we want to optimize. This objective function could be to

- maximize the posterior probabilities (e.g., naive Bayes)
- maximize a fitness function (genetic programming)
- maximize the total reward/value function (reinforcement learning)
- maximize information gain/minimize child node impurities (CART decision tree classification)
- minimize a mean squared error cost (or loss) function (CART, decision tree regression, linear regression, adaptive linear neurons, …
- maximize log-likelihood or minimize cross-entropy loss (or cost) function
- minimize hinge loss (support vector machine)
  …
