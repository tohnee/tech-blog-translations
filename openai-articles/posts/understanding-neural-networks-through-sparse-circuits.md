---
title: "Understanding neural networks through sparse circuits"
date: 2025-11-13
source: https://openai.com/index/understanding-neural-networks-through-sparse-circuits/
crawled: 2026-09-13
category: research
---

Neural networks power today’s most capable AI systems, but they remain difficult to understand. We don’t write these models with explicit, step-by-step instructions. Instead, they learn by adjusting billions of internal connections, or “weights,” until they master a task. We design the rules of training, but not the specific behaviors that emerge, and the result is a dense web of connections that no human can easily decipher.

## How we view interpretability

As AI systems become more capable and have real-world impact on decisions in science, education, and healthcare, understanding how they work is essential. **Interpretability** refers to methods that help us understand why a model produced a given output. There are many ways we might achieve this.

For example, reasoning models are incentivized to explain their work on the way to a final answer. **Chain of thought interpretability** leverages these explanations to monitor the model’s behavior. This is immediately useful: current reasoning models’ chains of thought seem to be informative with respect to concerning behaviors like deception. However, fully relying on this property is a brittle strategy, and this may break down over time.

On the other hand, **mechanistic interpretability**, which is the focus of this work, seeks to completely reverse engineer a model’s computations. It has so far been less immediately useful, but in principle, could offer a more complete explanation of the model’s behavior. By seeking to explain model behavior at the most granular level, mechanistic interpretability can make fewer assumptions and give us more confidence. But the path from low-level details to explanations of complex behaviors is much longer and more difficult.

Interpretability supports several key goals, for example enabling better oversight and providing early warning signs of unsafe or strategically misaligned behavior. It also complements our other safety efforts, such as scalable oversight, adversarial training, and red-teaming.

In this work, we show that we can often train models in ways that make them easier to interpret. We see our work as a promising complement to post-hoc analysis of dense networks.

This is a very ambitious bet; there is a long path from our work to fully understanding the complex behaviors of our most powerful models. Still, for simple behaviors, we find that sparse models trained with our method contain small, disentangled circuits that are both understandable and sufficient to perform the behavior. This suggests there may be a tractable path toward training larger systems whose mechanisms we can understand.

## A new approach: learning sparse models

Previous mechanistic interpretability work has started from dense, tangled networks, and tried to untangle them. In these networks, each individual neuron is connected to thousands of other neurons. Most neurons seem to perform many distinct functions, making it seemingly impossible to understand.

But what if we trained untangled neural networks, with many more neurons, but where each neuron has only a few dozen connections? Then maybe the resulting network will be simpler, and easier to understand. This is the central research bet of our work.

With this principle in mind, we trained language models with a very similar architecture to existing language models like GPT‑2, with one small modification: we force the vast majority of the model’s weights to be zeros. This constrained the model to use only very few of the possible connections between its neurons. This is a simple change which we argue substantially disentangles the model’s internal computations.

In normal dense neural networks, each neuron is connected to every neuron in the next layer. In our sparse models, each neuron only connects to a few neurons in the next layer. We hope that this makes the neurons, and the network as a whole, easier to understand.

## Evaluating interpretability

We wish to measure the extent to which our sparse models’ computations are disentangled. We considered various simple model behaviors, and checked whether we could isolate the parts of the model responsible for each behavior—which we term circuits.

We hand-curated a suite of simple algorithmic tasks. For each, we pruned the model down to the smallest circuit that can still perform the task, and examined how simple that circuit is. (For details, see our [paper](https://arxiv.org/abs/2511.13653).) We found that by training bigger and sparser models, we could produce increasingly capable models with increasingly simple circuits.

We plot interpretability versus capability across models (lower-left is better). For a fixed sparse model size, increasing sparsity—setting more weights to zero—reduces capability but increases interpretability. Scaling up model size shifts this frontier outward, suggesting we can build larger models that are both capable and interpretable.

To make this concrete, consider a task where a model trained on Python code has to complete a string with the correct type of quote. In Python, ‘hello’ must end with a single quote, and “hello” must end with a double quote. The model can solve this by remembering which quote type opened the string and reproducing it at the end.

Our most interpretable models appear to contain disentangled circuits which implement exactly that algorithm.

Example circuit in a sparse transformer that predicts whether to end a string in a single or double quote. This circuit uses just five residual channels (vertical gray lines), two MLP neurons in layer 0, and one attention query-key channel and one value channel in layer 10. The model (1) encodes single quotes in one residual channel and double quotes in another; (2) uses an MLP layer to convert this into one channel that detects any quote and another that classifies between single and double quotes; (3) uses an attention operation to ignore intervening tokens, find the previous quote, and copy its type to the final token; and (4) predicts the matching closing quote.

In our definition, the exact connections shown above are sufficient to perform the task—if we remove the rest of the model, this small circuit still works. They are also necessary–deleting these few edges causes the model to fail.

We also looked at some more complicated behaviors. Our circuits for these behaviors (for example variable binding shown below) are harder to explain completely. Even then, we can still achieve relatively simple partial explanations which are predictive of model behavior.

Another example circuit, in less detail. To determine the type of a variable called `current`, one attention operation copies the variable name into the `set()` token when it’s defined, and another later operation copies the type from the `set()` token into a subsequent use of the variable, allowing the model to infer the correct next token.

## The road ahead

This work is an early step toward a larger goal: making model computations easier to understand. But, there’s still a long way to go. Our sparse models are much smaller than frontier models, and large parts of their computation remain uninterpreted.

Next, we hope to scale our techniques to larger models, and to explain more of the models’ behavior. By enumerating circuit motifs underlying more complex reasoning in capable sparse models, we could develop an understanding that helps us better target investigations of frontier models.

To overcome the inefficiency of training sparse models, we see two paths forward. One is to extract sparse circuits from existing dense models, rather than training sparse models from scratch. Dense models are fundamentally more efficient to deploy than sparse models. The other path is to develop more efficient techniques to train models for interpretability, which might be easier to put in production.

Note that our findings here are no guarantee that this approach will extend to more capable systems, but these early results are promising. Our aim is to gradually expand how much of a model we can reliably interpret, and to build tools that make future systems easier to analyze, debug, and evaluate.
