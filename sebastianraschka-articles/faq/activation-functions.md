---
title: "Activation Functions for Artificial Neural Networks"
source: https://sebastianraschka.com/faq/docs/activation-functions.html
crawled: 2026-09-06
---

# Activation Functions for Artificial Neural Networks

An activation function transforms a neuron’s weighted input, usually written as `z = wᵀx + b`, into its output. Nonlinear activations let a neural network learn nonlinear relationships. Without them, a sequence of fully connected linear layers would still reduce to a single linear transformation, with an added bias if the layers use biases.

The choice depends on where the function is used. Hidden layers need a useful gradient for training. At the output layer, the activation also determines the range of predictions. For example, a sigmoid maps a binary classification score into the interval between zero and one, while a linear output can represent any real-valued regression prediction.

## Common activation functions

Here, `exp` is the exponential function and `log` is the natural logarithm. The threshold values at zero are conventions; the table uses the definitions in the original chart below.

On narrow screens, scroll the table sideways to read all columns.

| Function | Formula | Typical use or limitation |
| --- | --- | --- |
| Unit step | `0` for `z < 0`, `0.5` at zero, `1` for `z > 0` | Threshold decisions in perceptron variants. Its derivative is zero away from the discontinuity, so it is unsuitable for ordinary backpropagation. |
| Sign | `-1` for `z < 0`, `0` at zero, `1` for `z > 0` | A threshold decision with signed outputs; it has the same gradient limitation as the step function. |
| Linear | `z` | Unrestricted regression outputs, including linear regression and Adaline. |
| Clipped linear | `min(1, max(0, z + 0.5))` | A bounded, piecewise linear response. The gradient is zero outside the linear region. |
| Logistic sigmoid | `1 / (1 + exp(-z))` | Binary classification probabilities and gates. Large positive or negative inputs produce small gradients. |
| Hyperbolic tangent | `(exp(z) - exp(-z)) / (exp(z) + exp(-z))` | Outputs between -1 and 1, including recurrent network states. It also saturates for large input magnitudes. |
| ReLU | `max(0, z)` | A common hidden-layer activation. Positive inputs retain a gradient of one; negative inputs have a gradient of zero. |
| Softplus | `log(1 + exp(z))` | A smooth alternative to ReLU that produces positive outputs. |

## Choosing an activation in practice

For a basic feedforward network, ReLU is a reasonable hidden-layer starting point. It is inexpensive, but a unit that receives only negative inputs can stop learning because its gradient is zero. The [ReLU derivative FAQ](https://sebastianraschka.com/faq/docs/relu-derivative.html) explains this behavior, including the convention used at zero.

For binary classification in PyTorch, pass the output logits directly to [`BCEWithLogitsLoss`](https://docs.pytorch.org/docs/stable/generated/torch.nn.BCEWithLogitsLoss.html). That loss combines sigmoid and binary cross-entropy in a numerically stable computation. Apply sigmoid separately when converting the logits to probabilities for prediction.

For multiclass classification with mutually exclusive classes, [softmax](https://sebastianraschka.com/faq/docs/softmax.html) converts the vector of scores into probabilities that sum to one. This differs from the elementwise functions in the table because each softmax output depends on all scores in the vector.

## Original visual reference

The 2016 chart below contains two errors. The tanh denominator should be `exp(z) + exp(-z)`, as shown in the table and the [PyTorch tanh definition](https://docs.pytorch.org/docs/stable/generated/torch.nn.Tanh.html). Also, the clipped linear function is not the standard SVM decision function; an SVM classifies using the sign of its decision score.

![Original 2016 activation-function chart; the tanh formula and SVM example are corrected in the text above](https://sebastianraschka.com/images/faq/activation-functions/activation-functions.png)
