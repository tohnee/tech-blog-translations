---
title: "Deriving Gradient Descent for Linear Regression and Adaline"
source: https://sebastianraschka.com/faq/docs/linear-gradient-derivative.html
crawled: 2026-09-06
---

# Deriving Gradient Descent for Linear Regression and Adaline

Linear Regression and Adaptive Linear Neurons (Adalines) are closely related to each other. In fact, the Adaline algorithm is a identical to linear regression except for a threshold function ![](https://sebastianraschka.com/images/faq/linear-gradient-derivative/1.png) that converts the continuous output into a categorical class label

![](https://sebastianraschka.com/images/faq/linear-gradient-derivative/2.png)

where $z$ is the net input, which is computed as the sum of the input features **x** multiplied by the model weights **w**:

![](https://sebastianraschka.com/images/faq/linear-gradient-derivative/3.png)

(Note that ![](https://sebastianraschka.com/images/faq/linear-gradient-derivative/4.png) refers to the bias unit so that ![](https://sebastianraschka.com/images/faq/linear-gradient-derivative/5.png).)

In the case of linear regression and Adaline, the activation function ![](https://sebastianraschka.com/images/faq/linear-gradient-derivative/6.png) is simply the identity function so that ![](https://sebastianraschka.com/images/faq/linear-gradient-derivative/7.png).

![](https://sebastianraschka.com/images/faq/linear-gradient-derivative/regression-vs-adaline.png)

Now, in order to learn the optimal model weights **w**, we need to define a cost function that we can optimize. Here, our cost function ![](https://sebastianraschka.com/images/faq/linear-gradient-derivative/8.png) is the sum of squared errors (SSE), which we multiply by ![](https://sebastianraschka.com/images/faq/linear-gradient-derivative/9.png) to make the derivation easier:

![](https://sebastianraschka.com/images/faq/linear-gradient-derivative/10.png)

where ![](https://sebastianraschka.com/images/faq/linear-gradient-derivative/11.png) is the label or target label of the *i*th training point ![](https://sebastianraschka.com/images/faq/linear-gradient-derivative/12.png).

(Note that the SSE cost function is convex and therefore differentiable.)

In simple words, we can summarize the gradient descent learning as follows:

1. Initialize the weights to 0 or small random numbers.
2. For *k* epochs (passes over the training set)
   1. For each training sample ![](https://sebastianraschka.com/images/faq/linear-gradient-derivative/12.png)
      - Compute the predicted output value ![](https://sebastianraschka.com/images/faq/linear-gradient-derivative/13.png)
      - Compare ![](https://sebastianraschka.com/images/faq/linear-gradient-derivative/13.png) to the actual output ![](https://sebastianraschka.com/images/faq/linear-gradient-derivative/14.png) and Compute the “weight update” value
      - Update the “weight update” value
   2. Update the weight coefficients by the accumulated “weight update” values

Which we can translate into a more mathematical notation:

1. Initialize the weights to 0 or small random numbers.
2. For *k* epochs
   1. For each training sample ![](https://sebastianraschka.com/images/faq/linear-gradient-derivative/12.png)
      - ![](https://sebastianraschka.com/images/faq/linear-gradient-derivative/15.png)
      - ![](https://sebastianraschka.com/images/faq/linear-gradient-derivative/16.png) (where *η* is the learning rate);
      - ![](https://sebastianraschka.com/images/faq/linear-gradient-derivative/17.png)
   2. ![](https://sebastianraschka.com/images/faq/linear-gradient-derivative/18.png)

Performing this global weight update

![](https://sebastianraschka.com/images/faq/linear-gradient-derivative/18.png),

can be understood as “updating the model weights by taking an opposite step towards the cost gradient scaled by the learning rate *η*”

![](https://sebastianraschka.com/images/faq/linear-gradient-derivative/19.png)

where the partial derivative with respect to each ![](https://sebastianraschka.com/images/faq/linear-gradient-derivative/21.png) can be written as

![](https://sebastianraschka.com/images/faq/linear-gradient-derivative/20.png)

To summarize: in order to use gradient descent to learn the model coefficients, we simply update the weights **w** by taking a step into the opposite direction of the gradient for each pass over the training set – that’s basically it. But how do we get to the equation

![](https://sebastianraschka.com/images/faq/linear-gradient-derivative/22.png)

Let’s walk through the derivation step by step.

![](https://sebastianraschka.com/images/faq/linear-gradient-derivative/23.png)
