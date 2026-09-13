---
title: "Discovering new solutions to century-old problems in fluid dynamics"
source: https://deepmind.google/blog/discovering-new-solutions-to-century-old-problems-in-fluid-dynamics/
site: deepmind
date: 2025-09-18
authors: Yongji Wang, Sam Blackwell
crawled: 2026-09-13
---

Our new method could help mathematicians leverage AI techniques to tackle long-standing challenges in mathematics, physics and engineering.

For centuries, mathematicians have developed complex equations to describe the fundamental physics involved in fluid dynamics. These laws govern everything from the swirling vortex of a hurricane to airflow lifting an airplane’s wing.

Experts can carefully craft scenarios that make theory go against practice, leading to situations which could never physically happen. These situations, such as when quantities like velocity or pressure become infinite, are called ‘singularities’ or ‘blow ups’. They help mathematicians identify fundamental limitations in the equations of fluid dynamics, and help improve our understanding of how the physical world functions.

In a [new paper](https://arxiv.org/abs/2509.14185), we introduce an entirely new family of mathematical blow ups to some of the most complex equations that describe fluid motion. We’re publishing this work in collaboration with mathematicians and geophysicists from institutions including Brown University, New York University and Stanford University

Our approach presents a new way to leverage AI techniques to tackle longstanding challenges in mathematics, physics and engineering that demand unprecedented accuracy and interpretability.

## The importance of unstable singularities

Stability is a crucial aspect of singularity formation. A singularity is considered stable if it is robust to small changes. Conversely, an unstable singularity requires extremely precise conditions.

It’s expected that unstable singularities play a major role in foundational questions in fluid dynamics because mathematicians believe no stable singularities exist for the complex boundary-free 3D [Euler](https://en.wikipedia.org/wiki/Euler_equations_(fluid_dynamics)) and [Navier-Stokes](https://en.wikipedia.org/wiki/Navier%E2%80%93Stokes_equations) equations. Finding any singularity in the Navier-Stokes equations is one of the six famous [Millennium Prize Problems](https://www.claymath.org/millennium-problems/) that are still unsolved.

With our novel AI methods, we presented the first systematic discovery of new families of unstable singularities across three different fluid equations. We also observed a pattern emerging as the solutions become increasingly unstable. The number characterizing the speed of the blow up, lambda (λ), can be plotted against the order of instability, which is the number of unique ways the solution can deviate from the blow up. The pattern was visible in two of the equations studied, the Incompressible Porous Media (IPM) and Boussinesq equations. This suggests the existence of more unstable solutions, whose hypothesized lambda values lie along the same line.

![A line graph plotting "Inverse lambda value" on the y-axis against "Order of instability" from 0 to 4 on the x-axis, showing two upward-sloping, linear relationships: one solid blue line representing "IPM with boundary" and one dashed purple line representing "Boussinesq."](https://lh3.googleusercontent.com/VoRTLG1YRAcdn0K32JuI5Pp0VK--Rzk8MZILQkr3zrkWLMSbOscSFmJohznpHnlI6mQ4V450Ud7ZDmrrwrst7NfRRfR_mjGEmJa9f3vncd371xeFWjE=w1440)

Line chart with our results showing a surprisingly clear pattern in lambda (λ), a key parameter representing the speed of the blow up, as we found increasingly unstable solutions. This pattern was visible in both the Incompressible Porous Media (IPM) and Boussinesq equations.

We discovered these singularities by incorporating machine learning techniques such as second order optimizers for training neural networks. These methods allowed us to refine our accuracy to an unprecedented level. For reference, our largest errors addressed are equivalent to predicting the diameter of the Earth to within a few centimeters.

Here we show an example of the vorticity (Ω) field found for one of the equations studied. This is a measure of how much the fluid is spinning at each point.

![A three-dimensional plot of a vorticity (Ω) field shown on axes y₁ and y₂, displaying a smooth, curved surface transitioning from blue at its peak to purple at its lowest point.](https://lh3.googleusercontent.com/DwpT60RGTClvrbwFAZvO6umLh0LuVKLzKubY139lJOsFFpOqfFFsBCYCwmB50jVaBoiHwmlRjgD0AFFt_LkRyrjGQqVoqqPF3bF2wVpE36Vz21Lc=w1440)

Visualization of a three-dimensional representation and the two-dimensional vorticity (Ω) field found for one of the equations studied.

We also show a one-dimensional slice through the same field along an axis for all of the instabilities we discovered, showing the evolution of increasingly unstable singularities.

![A line graph plotting vorticity ($\Omega$) on the y-axis against the spatial coordinate $y^1$ on the x-axis, showing five curves representing different levels of instability: "Stable", "1st unstable", "2nd unstable", "3rd unstable", and "4th unstable". As the instability increases, the curves transition from a smooth, low-amplitude wave (stable) into increasingly sharp, high-amplitude peaks and troughs around $y^1 = -1$ and $y^1 = 1$.](https://lh3.googleusercontent.com/VF1U6W9G6b2lhxjLLEXv-XKHdSfAXctoufRyMiFGWKi84X9rNMyjK5I20DfRiAuqOpbBfa3PdPOfzfxdfBpemfUBJ3RaNA9KCpa7gv3mo-5gxDDDWQ=w1440)

Visualization of a three-dimensional representation and the two-dimensional vorticity (Ω) field found for one of the equations studied.

## Novel method navigates a vast landscape of singularities

Our approach is based on the use of Physics-Informed Neural Networks (PINNs). Unlike conventional neural networks that learn from vast datasets, we trained our models to match equations which model the laws of physics. The network's output is constantly checked against what the physical equations expect, and it learns by minimizing its ‘residual’, the amount by which its solution fails to satisfy the equations.

> By embedding mathematical insights and achieving extreme precision, we transformed PINNs into a discovery tool that finds elusive singularities.

Yongji Wang

first author of the study and Postdoctoral Researcher at NYU

Our use of PINNs goes beyond their typical role as general-purpose tools used for solving partial differential equations ([PDEs](https://en.wikipedia.org/wiki/Partial_differential_equation)). By embedding mathematical insights directly into the training, we were able to capture elusive solutions — such as unstable singularities — that have long-challenged conventional methods.

At the same time, we developed a high-precision framework that pushes PINNs to near-machine precision, enabling the level of accuracy required for rigorous computer-assisted proofs.

## A new era of computer-assisted mathematics

This breakthrough represents a new way of doing mathematical research, combining deep mathematical insights with cutting-edge AI. We’re excited for this work to help usher in a new era where long-standing challenges are tackled with AI and computer-assisted proofs.

**Learn more**

[Read our paper](https://arxiv.org/abs/2509.14185)

**Acknowledgements**

This work was a joint effort by: Yongji Wang, Mehdi Bennani, James Martens, Sébastien Racanière, Sam Blackwell, Alex Matthews, Stanislav Nikolov, Gonzalo Cao-Labora, Daniel S. Park, Martin Arjovsky, Daniel Worrall, Chongli Qin, Ferran Alet, Borislav Kozlovskii, Nenad Tomašev, Alex Davies and Pushmeet Kohli

Tristan Buckmaster, Bogdan Georgiev, Javier Gómez-Serrano, Ray Jiang and Ching-Yao Lai.
