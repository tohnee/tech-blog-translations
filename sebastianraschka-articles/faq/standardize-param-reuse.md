---
title: "Why Test Data Must Use Training-Set Scaling Parameters"
source: https://sebastianraschka.com/faq/docs/standardize-param-reuse.html
crawled: 2026-09-06
---

# Why Test Data Must Use Training-Set Scaling Parameters

Let me give you an example to this very common question to show why we don’t want to standardize new (or test) data “from scratch.”

Let’s assume we have a simple training set consisting of 3 samples with 1 feature (let’s call this feature “length”):

- train\_1: 10 cm -> class\_2
- train\_2: 20 cm -> class\_2
- train\_3: 30 cm -> class\_1

mean: 20, std.: 8.2

After standardization, the transformed feature values are

- train\_std\_1: -1.21 -> class\_2
- train\_std\_2: 0 -> class\_2
- train\_std\_3: 1.21 -> class\_1

Next, let’s assume our model has learned to classify samples with a standardized length value < 0.6 as class\_2 (class\_1 otherwise). So far so good. Now, let’s say we have 3 unlabeled data points that we want to classify:

- new\_4: 5 cm -> class ?
- new\_5: 6 cm -> class ?
- new\_6: 7 cm -> class ?

If we look at the “unstandardized “length” values in our training dataset, it is intuitive to say that all of these samples are likely belonging to class\_2. However, if we standardize these by re-computing standard deviation and and mean you would get similar values as before in the training set and your classifier would (probably incorrectly) classify samples 4 and 5 as class 2.

- new\_std\_4: -1.21 -> class 2
- new\_std\_5: 0 -> class 2
- new\_std\_6: 1.21 -> class 1

However, if we use the training mean of 20 cm and the rounded standard deviation of 8.2 cm, we compute `(length - 20) / 8.2` and get:

- new\_4: -1.83 -> class 2
- new\_5: -1.71 -> class 2
- new\_6: -1.59 -> class 2

The values 5 cm, 6 cm, and 7 cm are much lower than anything we have seen in the training set previously. Thus, it only makes sense that the standardized features of the “new samples” are much lower than every standardized feature in the training set.
