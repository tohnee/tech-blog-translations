---
title: "When to Use Poisson vs. Ordinal Regression"
source: https://sebastianraschka.com/faq/docs/poisson-ordinal.html
crawled: 2026-09-06
---

# When to Use Poisson vs. Ordinal Regression

Usually, we use Poisson regression is for when the target variable represents count data (positive integers). As an example of count data, consider the number of colds contracted on an airplane or the number of guests visiting a restaurant on a given day.

Ordinal data is a subcategory of categorical data where the categories have a natural order, for example, 3 > 2 > 1. Ordinal data is often represented as positive integers and may look similar to count data. For example, consider the star rating on Amazon (1 star, 2 stars, 3 stars, etc.). However, ordinal regression does not make any assumptions about the distance between the ordered categories. As another example of ordinal data, consider disease severity, *severe > moderate > mild > none*. While we typically map the disease severity variable to an integer representation (4 > 3 > 2 > 1), there is no assumption that the distance between 4 and 3 (severe and moderate) is the same as the distance between 2 and 1 (mild and none).

In short, we use Poisson regression for count data. We use ordinal regression when we know that certain outcomes are “higher” or “lower” than others, but we are not sure how much or if it even matters.

---

**This is an abbreviated answer and excerpt from my book [Machine Learning Q and AI](https://leanpub.com/machine-learning-q-and-ai/), which contains a more verbose version with additional illustrations.**
