---
title: "Statistical Modeling vs. Machine Learning"
source: https://sebastianraschka.com/faq/docs/statistical-modeling-vs-machine-learning.html
crawled: 2026-09-06
---

# Statistical Modeling vs. Machine Learning

As a statistics professor who teaches machine learning classes, this is among the top questions
I get frequently asked by students. There are, of course, many ways to slice and dice it. In my
opinion, if I had to boil it down to a few single points, I would highlight the following:

- In statistical modeling we usually use parametric approaches (e.g., think of linear or logistic regression as the simplest examples of parametric models – we specify the number of parameters upfront), whereas in machine learning, we often use nonparametric approaches, which means that we don’t pre-specify the structure of the model (e.g., K-nearest neighbors, decision trees, kernel SVM, etc.)
- In most statistical models, we assume that features (predictors, covariates) are additive
- Using statistical models, we usually care a lot about uncertainty estimates (confidence intervals, hypothesis tests, etc.)
- When we are using machine learning models, we typically don’t make any substantial/particular assumptions like non-collinearity, normally distributed residuals, etc.
- The absolute predictive performance of ML models is usually better than for statistical models (although, they often don’t have the same level of interpretability as statistical models)

Two articles related to the topic I would recommend are:

- Breiman, L. (2001). [Statistical modeling: The two cultures](https://projecteuclid.org/euclid.ss/1009213726) (with comments and a rejoinder by the author). Statistical science, 16(3), 199-231.
- Carmichael, I., & Marron, J. S. (2018). [Data science vs. statistics: two cultures?](https://link.springer.com/article/10.1007/s42081-018-0009-3). Japanese Journal of Statistics and Data Science, 1(1), 117-138.
