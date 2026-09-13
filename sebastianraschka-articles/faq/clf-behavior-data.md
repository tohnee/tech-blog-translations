---
title: "Toy Datasets for Visualizing Classifier Behavior"
source: https://sebastianraschka.com/faq/docs/clf-behavior-data.html
crawled: 2026-09-06
---

# Toy Datasets for Visualizing Classifier Behavior

The visualization part is a bit tricky since we as humans are limited to 1-3 D graphics. However, I’d still say Iris is one of the most useful toy datasets for looking at classifier behavior (see image below).

![](https://sebastianraschka.com/images/faq/clf-behavior-data/iris.png)

(I’ve implemented this simple function here if you are interested: [mlxtend plot\_decision\_regions](https://rasbt.github.io/mlxtend/user_guide/plotting/plot_decision_regions/).)
Other than that, I think that synthetic datasets like “XOR,” “half-moons,” or concentric circles would be good candidates for evaluating classifier on non-linear problems:

---

![](https://sebastianraschka.com/images/faq/clf-behavior-data/xor.png)

---

![](https://sebastianraschka.com/images/faq/clf-behavior-data/moons.png)

---

![](https://sebastianraschka.com/images/faq/clf-behavior-data/circles.png)
