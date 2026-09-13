---
title: "Simulating matter on the quantum scale with AI"
source: https://deepmind.google/blog/simulating-matter-on-the-quantum-scale-with-ai/
site: deepmind
date: 2021-12-09
authors: James Kirkpatrick, Aron Cohen, Alex Gaunt
crawled: 2026-09-13
---

Solving some of the major challenges of the 21st Century, such as producing clean electricity or developing high temperature superconductors, will require us to design new materials with specific properties. To do this on a computer requires the simulation of electrons, the subatomic particles that govern how atoms bond to form molecules and are also responsible for the flow of electricity in solids. Despite decades of effort and several significant advances, accurately modelling the quantum mechanical behaviour of electrons remains an open challenge. Now, in a [paper](https://www.science.org/stoken/author-tokens/ST-218/full) ([Open Access PDF](https://storage.googleapis.com/deepmind-media/papers/Data_Driven_Density_Functional_Design/data_driven_density_functional_design_unformatted.pdf)) published in Science, we propose DM21, a neural network achieving state of the art accuracy on large parts of chemistry. To accelerate scientific progress, we’re also open sourcing our [code](https://github.com/deepmind/deepmind-research/tree/master/density_functional_approximation_dm21) for anyone to use.

Nearly a century ago, Erwin Schrödinger proposed [his famous equation](https://www.nobelprize.org/prizes/physics/1933/schrodinger/facts/) governing the behaviour of quantum mechanical particles. Applying this equation to electrons in molecules is challenging because all electrons repel each other. This would seem to require tracking the probability of each electron’s position — a remarkably complex task for even a small number of electrons. One major breakthrough came in the 1960s, when Pierre Hohenberg and Walter Kohn realised that it is not necessary to track each electron individually. Instead, knowing the probability for any electron to be at each position (i.e., the electron density) is sufficient to exactly compute all interactions. Kohn received a [Nobel Prize in Chemistry](https://www.nobelprize.org/prizes/chemistry/1998/kohn/facts/) after proving this, thus founding Density Functional Theory (DFT).

Although DFT proves a mapping exists, for more than 50 years the exact nature of this mapping between electron density and interaction energy — the so-called density functional — has remained unknown and has to be approximated. Despite the fact that DFT intrinsically involves a level of approximation, it is the only practical method to study how and why matter behaves in a certain way at the microscopic level and has therefore become one of the most widely used techniques in all of science. Over the years, researchers have proposed many approximations to the exact functional with varying levels of accuracy. Despite their popularity, all of these approximations suffer from systematic errors because they fail to capture certain crucial mathematical properties of the exact functional.

By expressing the functional as a neural network and incorporating these exact properties into the training data, we learn functionals free from important systematic errors — resulting in a better description of a broad class of chemical reactions.

![A diagram showing the mapping of a 3D electron density of a molecule, through a Functional neural network represented by a central box, to map to a scalar value for energy.](https://lh3.googleusercontent.com/p5U1EZotSmzxsQTeE1_DP7hYDByTCTyYKDFJoavfQsaw36BjqPaXCog7n74YlbQpqTaZHPM3rEwauuoPgA_IJ4XO-3awxrXdReDx8py80lUmTGwbpw=w1440)

We specifically address two long-standing problems with traditional functionals:

- **The delocalization error**: In a DFT calculation, the functional determines the charge density of a molecule by finding the configuration of electrons which minimizes energy. Thus, errors in the functional can lead to errors in the calculated electron density. Most existing density functional approximations prefer electron densities that are unrealistically spread out over several atoms or molecules rather than being correctly localized around a single molecule or atom (see Fig 2).
- **Spin symmetry breaking**: When describing the breaking of chemical bonds, existing functionals tend to unrealistically prefer configurations in which a fundamental symmetry known as spin symmetry is broken. Since symmetries play a vital role in our understanding of physics and chemistry, this artificial symmetry breaking reveals a major deficiency in existing functionals.

In principle, any chemical-physical process that involves movement of charge is liable to suffer from delocalization error, and any process that involves the breaking of bonds is liable to suffer from spin-symmetry breaking. Movement of charge and bond breaking are core to many important technological applications, but these problems can also lead to massive qualitative failure of functionals to describe the simplest molecules, such as hydrogen. Since DFT is such a crucial technology it is important to design functionals that get this simple chemistry correct before asking them to explain vastly more complex molecular interactions, such as those that may occur in a battery or solar cell.

![A comparison of electron density simulations between the traditional B3LYP functional, which shows unrealistically smeared (delocalized) charge clouds across two molecules, and the DM21 neural network functional, which correctly models localized (not smeared) electron density.](https://lh3.googleusercontent.com/EEmwVCY4WA6uUGn9eUuvN4Onk8gChBl3-3Ah1xPZHfNLt8bxV96r3dPJxM8d1fwauuCVdLfeY5cov-9h2mk9sGtjMCivuf-Gvhodn1seFRs8vjL-Bg=w1440)

Fig 2 | Left: Traditional functional (B3LYP) predicts charge is smeared over two adjacent molecules. Right: Learned functional (DM21) correctly localises charge on one molecule.

These longstanding challenges are both related to how functionals behave when presented with a system that exhibits “fractional electron character.” By using a neural network to represent the functional and tailoring our training dataset to capture the fractional electron behaviour expected for the exact functional, we found that we could solve the problems of delocalization and spin symmetry-breaking. Our functional also showed itself to be highly accurate on broad, large-scale benchmarks, suggesting that this data-driven approach can capture aspects of the exact functional that have thus far been elusive.

For years, computer simulations have played a central role in modern engineering, making it possible to provide reliable answers to questions like “will this bridge stay up?” to “will this rocket make it into space?” As technology increasingly turns to the quantum scale to explore questions about materials, medicines, and catalysts, including those we’ve never seen or even imagined, deep learning shows promise to accurately simulate matter at this quantum mechanical level.

**Notes**

Read the Science paper [here](https://www.science.org/stoken/author-tokens/ST-218/full).

Open Access PDF of the paper [here](https://storage.googleapis.com/deepmind-media/papers/Data_Driven_Density_Functional_Design/data_driven_density_functional_design_unformatted.pdf).
