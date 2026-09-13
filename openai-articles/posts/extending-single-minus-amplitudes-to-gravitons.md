---
title: "Extending single-minus amplitudes to gravitons"
date: 2026-03-04
source: https://openai.com/index/extending-single-minus-amplitudes-to-gravitons/
crawled: 2026-09-13
category: research
---

We’ve published a new preprint studying scattering amplitudes in quantum gravity, extending [recent results obtained for gluons](https://openai.com/index/new-result-theoretical-physics/) to the gravitational setting. The work shows that a class of graviton interactions long assumed to vanish can in fact arise under well-defined kinematic conditions. The preprint is available [here](https://cdn.openai.com/pdf/graviton.pdf). We welcome feedback from the community.

The paper, “Single-minus graviton tree amplitudes are nonzero,” is authored by Alfredo Guevara (Institute for Advanced Study), Alexandru Lupsasca (Vanderbilt University and OpenAI), David Skinner (University of Cambridge), Andrew Strominger (Harvard University), and Kevin Weil (OpenAI) on behalf of OpenAI.

## Understanding single-minus amplitudes in gravity

Scattering amplitudes are mathematical quantities physicists use to calculate the probability that particles interact in particular ways. Rather than tracking every intermediate step of a collision through many diagrams, amplitudes encode the final observable outcomes in a compact form. Over the past several decades, researchers have found that amplitudes often display unexpected simplicity, revealing hidden mathematical structure not obvious from traditional calculations.

The new preprint studies gravitons, quantum particles associated with gravity in quantum field theory. In particular, the authors analyze a configuration known as a single-minus amplitude, meaning that one particle has negative helicity while the remaining particles have positive helicity. Helicity describes the orientation of a particle’s spin relative to its direction of motion and plays an important role in determining how interactions occur. Standard textbook arguments suggest that these amplitudes should vanish at the simplest level of approximation, called tree level, where only the most direct interaction diagrams are considered and quantum loop effects are ignored.

The preprint shows that this conclusion depends on assuming generic particle motion. When particle momenta satisfy a special alignment known as the half-collinear regime, the usual argument no longer applies. In this regime, the amplitudes do not vanish but instead exist as well-defined mathematical distributions supported on a restricted region of momentum space. The authors derive explicit formulas describing these interactions and show that they follow from symmetry principles and recursion relations that build complex interactions from simpler ones.

This result is a small step towards the solution of the central problem of reconciling quantum mechanics with Einstein’s theory of general relativity. The single minus amplitudes realize an infinite dimensional “w-(1+∞)” symmetry. This powerful symmetry was discovered by Penrose a half century ago in the context of classical gravity and is expected by many to play a central role in quantizing the gravitational field. The new preprint shows how, in the simplest possible context, this symmetry acts on gravitons, the elementary quantum bits of the gravitational field.

## Methodology and verification

Although gravity and gauge theory share deep conceptual relationships, their calculations differ substantially in practice. The earlier gluon result demonstrated that a previously neglected helicity configuration could produce nonzero amplitudes under special conditions. After that work was completed, the gluon paper was provided to GPT‑5.2 Pro as context. Using it as a reference point, the model was asked to construct the corresponding amplitudes in quantum gravity, an extension which would have taken human authors considerable time to derive. GPT‑5.2 Pro not only solved this problem using a beautiful and surprising technique (the directed matrix-tree theorem), it also produced an excellent preliminary draft of the paper. You can find a transcript of this initial exchange [here](https://cdn.openai.com/pdf/gluon-to-graviton-paper.pdf).

The derivation combines several established tools in amplitude theory, including recursion relations that iteratively construct many-particle interactions from smaller building blocks and symmetry constraints that restrict the allowed form of the result. The final formulas were verified analytically and checked for consistency with known physical limits. After further interaction with GPT‑5.2 Pro, the amplitudes were also found to be consistent with an infinite-dimensional symmetry first studied in connection with gravity by Roger Penrose.

An important observation emerging from this and related projects concerns the pace of discovery. For this project, much of the time elapsed from the previous gluon result was spent confirming derivations, checking consistency, and preparing formal write-ups rather than generating initial conjectures. This sequence of results represents a significant shift, with verification and exposition representing the dominant share of effort.

The transition from gluons to gravitons illustrates how mathematical insight can transfer across neighboring areas of theoretical physics. While the two theories describe different fundamental forces, they share structural features that allow ideas developed in one setting to inform the other. Providing the gluon result as an anchor enabled exploration of this connection, leading to a gravitational construction that was subsequently proven using standard analytic methods.

## What’s next

Further extensions of these results are currently under investigation. Together with the earlier gluon work, this preprint contributes to an ongoing effort to understand how AI-assisted reasoning can participate in theoretical research while maintaining conventional standards of mathematical verification and scientific rigor.
