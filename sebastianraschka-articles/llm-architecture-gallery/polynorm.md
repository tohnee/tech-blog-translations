---
title: "PolyNorm"
source: https://sebastianraschka.com/llm-architecture-gallery/polynorm/
crawled: 2026-09-06
---

# PolyNorm

PolyNorm is a trainable activation that mixes separately normalized linear, quadratic, and cubic transformations of the same preactivation. In [Motif 3 Beta](https://sebastianraschka.com/llm-architecture-gallery/#card-motif-3-beta), it replaces the SiLU part of the usual SwiGLU-style feed-forward module.

[Architecture gallery](https://sebastianraschka.com/llm-architecture-gallery/)
[PolyCom paper](https://arxiv.org/abs/2411.03884)
[PolyCom code](https://github.com/BryceZhuo/PolyCom)
[Motif 3 Beta model](https://huggingface.co/Motif-Technologies/Motif-3-Beta)

![SwiGLU applies a fixed SiLU activation to its gate projection, while PolyNorm learns a mixture of separately RMS-normalized linear, quadratic, and cubic terms](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/polynorm-gated-ffn.webp)

SwiGLU uses a fixed SiLU function on the gate branch. PolyNorm learns three mixture
coefficients and a bias while keeping the surrounding projection matrices unchanged.

## How we got from GELU to PolyNorm

Early GPT architectures used GELU. Why now use Swish over GELU? Swish (also referred to as sigmoid linear unit or SiLU) is considered computationally slightly cheaper, and in my opinion, that is all there is to it. I consider the reported performance differences between the two functions too small to generalize. They are probably within standard error, and your mileage will vary based on hyperparameter sensitivity.

Activation functions used to be a hot topic of debate until the deep learning community largely settled on ReLU more than a decade ago. Since then, researchers have proposed and tried many ReLU-like variants with smoother curves, and GELU and Swish are the ones that stuck.

Early GPT architectures used GELU, which is defined as `0.5x * [1 + erf(x / sqrt(2))]`. Here, `erf` (short for error function) is the integral of a Gaussian and it is computed using polynomial approximations of the Gaussian integral, which makes it more computationally expensive than simpler functions like the sigmoid used in Swish, where Swish is simply `x * sigmoid(x)`.

In practice, Swish is computationally slightly cheaper than GELU, and that’s probably the main reason it replaced GELU in most newer models. I would not choose between them based on small modeling differences alone. I’d say these gains are often within standard error, and the winner will depend heavily on hyperparameter tuning.

Swish is used in most architectures today. However, GELU is not entirely forgotten; for example, Google’s Gemma models still use GELU.

What’s more notable, though, is that the feed forward module (a small multi-layer perceptron) is replaced by a gated “GLU” counterpart, where GLU stands for gated linear unit and was proposed in a [2020 paper](https://arxiv.org/abs/2002.05202). Concretely, the two fully connected layers are replaced by three fully connected layers.

At first glance, it may appear that the GEGLU/SwiGLU variants may be better than the regular feed forward layers because there are simply more parameters due to the extra layer. But this is deceiving because in practice, the `W` and `V` weight layers in SwiGLU/GEGLU are usually chosen to be half the size each of the `W_1` layer in a traditional feed forward layer.

SwiGLU applies SiLU to the gate branch. PolyNorm replaces this fixed function with a learned mixture while leaving the gate, up, and down projection sizes unchanged. Let `g = W_gate h` and `u = W_up h`. A SwiGLU-style module computes

```python
output = W_down(SiLU(g) ⊙ u)
```

Motif changes only the activation on the gate branch:

```python
output = W_down(s · PolyNorm(g) ⊙ u)
```

## The normalized polynomial

PolyNorm first forms `x`, `x²`, and `x³` and RMS-normalizes each one separately:

```python
norm(z) = z / sqrt(mean(z²) + ε)
```

It then mixes three normalized powers:

```python
PolyNorm(x) = a₃ · norm(x³) + a₂ · norm(x²) + a₁ · norm(x) + b
```

Three learned coefficients mix these terms, and a learned bias shifts the result. Separate normalization matters because it prevents the larger raw scale of the cubic term from deciding its importance.

Motif applies a sigmoid to the coefficient parameters, clamps the bias to plus or minus 0.5, and scales the activation by 0.5. These stabilization choices belong to the Motif implementation rather than the general PolyNorm definition.

## Grouped PolyNorm in Motif 3 Beta

Motif 3 Beta has 384 routed experts and selects eight for each token. Each routed expert gets its own three PolyNorm coefficients and bias. This adds 1,536 scalars per MoE layer, which is tiny compared with the projection matrices. The released activation package provides a grouped CUDA operation for the expert-specific computation.

![Motif 3 Beta architecture diagram showing Grouped PolyNorm inside its mixture-of-experts feed-forward module](https://sebastianraschka.com/llm-architecture-gallery/images/architectures/motif-3-beta.webp)

Motif 3 Beta applies separate Grouped PolyNorm parameters in each selected expert before the
gating multiplication.

## Evidence and costs

The [PolyCom paper](https://arxiv.org/abs/2411.03884) tested dense 1B and sparse 7B-A1B models. Its polynomial activations improved validation loss and perplexity over the tested fixed activations. Third- and fourth-order variants converged similarly, making the cubic form the cheaper practical choice.

The extra parameters are negligible, but the elementwise work is not free. PolyNorm computes three powers and three RMS normalizations. It does not reduce the large matrix multiplications in an MoE layer, so efficient use benefits from a fused kernel.

Sources

[Polynomial Composition Activations paper](https://arxiv.org/abs/2411.03884)
[PolyCom reference code](https://github.com/BryceZhuo/PolyCom)
[Motif model implementation](https://huggingface.co/Motif-Technologies/Motif-3-Beta/blob/main/modeling_motif.py)
[Motif model configuration](https://huggingface.co/Motif-Technologies/Motif-3-Beta/blob/main/config.json)
[Motif activation kernels](https://huggingface.co/Motif-Technologies/activation)

[Back to architecture gallery](https://sebastianraschka.com/llm-architecture-gallery/)
