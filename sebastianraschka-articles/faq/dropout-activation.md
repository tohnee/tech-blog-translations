---
title: "Is dropout applied before or after the non-linear activation function?"
source: https://sebastianraschka.com/faq/docs/dropout-activation.html
crawled: 2026-09-06
---

# Is dropout applied before or after the non-linear activation function?

Typically, dropout is applied after the non-linear activation function (a). However, when using rectified linear units (ReLUs), it might make sense to apply dropout before the non-linear activation (b) for reasons of computational efficiency depending on the particular code implementation.

> (a): Fully connected, linear activation -> ReLU -> Dropout -> …  
> (b): Fully connected, linear activation -> Dropout -> ReLU -> …

Why do (a) and (b) produce the same results in case of ReLU?. Let’s answer this question with a simple example starting with the following *logits* (outputs of the linear activation of the fully connected layer):

> `[-1, -2, -3, 4, 5, 6]`

Let’s walk through scenario (a), applying the ReLU activation first. The output of the non-linear ReLU functions are as follows:

> `[0, 0, 0, 4, 5, 6]`

Remember, the ReLU activation function is defined as \(f(x) = max(0, x)\); thus, all non-zero values will be changed to zeros. Now, applying dropout with a probability 0f 50%, let’s assume that the units being deactivated are units 2, 4, and 6:

> `[0*2, 0, 0*2, 0, 0*2, 0] = [0, 0, 0, 0, 10, 0]`

Note that in dropout, units are deactivated randomly by default. In the preceding example, we assumed that the 2nd, 4th, and 6th unit were deactivated during the training iteration. Also, because we applied dropout with 50% dropout probability, we scaled the remaining units by a factor of 2.

Now, let’s take a look at scenario (b). Again, we assume a 50% dropout rate and that units 2, 4, and 6 are deactivated:

> `[-1, -2, -3, 4, 5, 6] -> [-1*2, 0, -3*2, 0, 5*2, 0]`

Now, if we pass this array to the ReLU function, the resulting array will look exactly like the one in scenario (a):

> `[-2, 0, -6, 0, 10, 0] -> [0, 0, 0, 0, 10, 0]`
