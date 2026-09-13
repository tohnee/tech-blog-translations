---
title: "FermiNet: Quantum physics and chemistry from first principles"
source: https://deepmind.google/blog/ferminet-quantum-physics-and-chemistry-from-first-principles/
site: deepmind
date: 2024-08-22
authors: David Pfau, James Spencer
crawled: 2026-09-13
---

Note: This blog was first published on 19 October 2020. Following the publication of our breakthrough work on excited states in Science on 22 August 2024, we’ve made minor updates and [added a section below](#a-new-way-to-compute-excited-states) about this new phase of work.

Using deep learning to solve fundamental problems in computational quantum chemistry and explore how matter interacts with light

In an [article](https://journals.aps.org/prresearch/abstract/10.1103/PhysRevResearch.2.033429) published in Physical Review Research, we showed how deep learning can help solve the fundamental equations of quantum mechanics for real-world systems. Not only is this an important fundamental scientific question, but it also could lead to practical uses in the future, allowing researchers to prototype new materials and chemical syntheses using computer simulation before trying to make them in the lab.

Our neural network architecture, [FermiNet](https://journals.aps.org/prresearch/abstract/10.1103/PhysRevResearch.2.033429) (Fermionic Neural Network), is well-suited to modeling the quantum state of large collections of electrons, the fundamental building blocks of chemical bonds. We released the [code from this study](https://github.com/deepmind/ferminet) so computational physics and chemistry communities can build on our work and apply it to a wide range of problems.

FermiNet was the first demonstration of deep learning for computing the energy of atoms and molecules from first principles that was accurate enough to be useful, and [Psiformer](https://arxiv.org/abs/2211.13672), our novel architecture based on self-attention, remains the most accurate AI method to date.

We hope the tools and ideas developed in our artificial intelligence (AI) research can help solve fundamental scientific problems, and FermiNet joins our work on [protein folding](https://deepmind.com/blog/article/AlphaFold-Using-AI-for-scientific-discovery), [glassy dynamics](https://deepmind.com/blog/article/Towards-understanding-glasses-with-graph-neural-networks), [lattice quantum chromodynamics](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.125.121601) and many other projects in bringing that vision to life.

## A brief history of quantum mechanics

Mention “quantum mechanics” and you’re more likely to inspire confusion than anything else. The phrase conjures up images of [Schrödinger’s cat](https://en.wikipedia.org/wiki/Schr%C3%B6dinger%27s_cat), which can paradoxically be both alive and dead, and fundamental particles that are also, somehow, waves.

In quantum systems, a particle such as an electron doesn’t have an exact location, as it would in a classical description. Instead, its position is described by a probability cloud — it’s smeared out in all places it’s allowed to be. This counterintuitive state of affairs led Richard Feynman to declare: “If you think you understand quantum mechanics, you don’t understand quantum mechanics.”

Despite this spooky weirdness, the meat of the theory can be reduced down to just a few straightforward equations. The most famous of these, the Schrödinger equation, describes the behavior of particles at the quantum scale in the same way that [Newton’s laws of motion](https://en.wikipedia.org/wiki/Newton%27s_laws_of_motion) describe the behavior of objects at our more familiar human scale. While the interpretation of this equation can cause endless head-scratching, the math is much easier to work with, leading to the common exhortation from professors to “shut up and calculate” when pressed with thorny philosophical questions from students.

These equations are sufficient to describe the behavior of all the familiar matter we see around us at the level of atoms and nuclei. Their counterintuitive nature leads to all sorts of exotic phenomena: superconductors, superfluids, lasers and semiconductors are only possible because of quantum effects. But even the humble covalent bond — the basic building block of chemistry — is a consequence of the quantum interactions of electrons.

Once these rules were worked out in the 1920s, scientists realized that, for the first time, they had a detailed theory of how chemistry works. In principle, they could just set up these equations for different molecules, solve for the energy of the system, and figure out which molecules were stable and which reactions would happen spontaneously. But when they sat down to actually calculate the solutions to these equations, they found that they could do it exactly for the simplest atom (hydrogen) and virtually nothing else. Everything else was too complicated.

> The underlying physical laws necessary for the mathematical theory of a large part of physics and the whole of chemistry are thus completely known, and the difficulty is only that the exact application of these laws leads to equations much too complicated to be soluble. It therefore becomes desirable that approximate practical methods of applying quantum mechanics should be developed.

Paul Dirac

founder of quantum mechanics, 1929

Many took up Dirac’s charge, and soon physicists built mathematical techniques that could approximate the qualitative behavior of molecular bonds and other chemical phenomena. These methods started from an approximate description of how electrons behave that may be familiar from introductory chemistry.

In this description, each electron is assigned to a particular orbital, which gives the probability of a single electron being found at any point near an atomic nucleus. The shape of each orbital then depends on the average shape of all other orbitals. As this “mean field” description treats each electron as being assigned to just one orbital, it’s a very incomplete picture of how electrons actually behave. Nevertheless, it’s enough to estimate the total energy of a molecule with only about 0.5% error.

![Illustration of atomic orbitals. The surface denotes the area of high probability of finding an electron. In the blue region, the wavefunction is positive, while in the purple region it’s negative.](https://lh3.googleusercontent.com/zh6UjGY11wBi8jUrFGpUkxpjGkY5cYNZUmkASctsepaix-Z4N8u5dC5tdqlyt3SUzCkREYQMcfchLuprVIXEQUi0tJudr-MXILSpW4B8IsJC0bBn=w1440)

Illustration of atomic orbitals. The surface denotes the area of high probability of finding an electron. In the blue region, the wavefunction is positive, while in the purple region it’s negative.

Unfortunately, 0.5% error still isn’t enough to be useful to the working chemist. The energy in molecular bonds is just a tiny fraction of the total energy of a system, and correctly predicting whether a molecule is stable can often depend on just 0.001% of the total energy of a system, or about 0.2% of the remaining “correlation” energy.

For instance, while the total energy of the electrons in a [butadiene molecule](https://en.wikipedia.org/wiki/Butadiene) is almost 100,000 kilocalories per mole, the difference in energy between different possible shapes of the molecule is just 1 kilocalorie per mole. That means that if you want to correctly predict butadiene’s natural shape, then the same level of precision is needed as measuring the width of a football field down to the millimeter.

With the advent of digital computing after World War II, scientists developed a wide range of computational methods that went beyond this mean field description of electrons. While these methods come in a jumble of abbreviations, they all generally fall somewhere on an axis that trades off accuracy with efficiency. At one extreme are essentially exact methods that scale worse than exponentially with the number of electrons, making them impractical for all but the smallest molecules. At the other extreme are methods that scale linearly, but are not very accurate. These computational methods have had an enormous impact on the practice of chemistry — the [1998 Nobel Prize in chemistry](https://www.nobelprize.org/prizes/chemistry/1998/summary/) was awarded to the originators of many of these algorithms.

## Fermionic neural networks

Despite the breadth of existing computational quantum mechanical tools, we felt a new method was needed to address the problem of efficient representation. There’s a reason that the largest quantum chemical calculations only run into the tens of thousands of electrons for even the most approximate methods, while classical chemical calculation techniques like molecular dynamics can handle millions of atoms.

The state of a classical system can be described easily — we just have to track the position and momentum of each particle. Representing the state of a quantum system is far more challenging. A probability has to be assigned to every possible configuration of electron positions. This is encoded in the wavefunction, which assigns a positive or negative number to every configuration of electrons, and the wavefunction squared gives the probability of finding the system in that configuration.

The space of all possible configurations is enormous — if you tried to represent it as a grid with 100 points along each dimension, then the number of possible electron configurations for the silicon atom would be larger than the number of atoms in the universe. This is exactly where we thought deep neural networks could help.

In the last several years, there have been huge advances in representing complex, high-dimensional probability distributions with neural networks. We now know how to train these networks efficiently and scalably. We guessed that, given these networks have already proven their ability to fit high-dimensional functions in AI problems, maybe they could be used to represent quantum wavefunctions as well.

Researchers such as [Giuseppe Carleo, Matthias Troyer and others](https://science.sciencemag.org/content/355/6325/602.abstract) have shown how modern deep learning could be used for solving idealized quantum problems. We wanted to use deep neural networks to tackle more realistic problems in chemistry and condensed matter physics, and that meant including electrons in our calculations.

There is just one wrinkle when dealing with electrons. Electrons must obey the [Pauli exclusion principle](https://en.wikipedia.org/wiki/Pauli_exclusion_principle), which means that they can’t be in the same space at the same time. This is because electrons are a type of particle known as [fermions](https://en.wikipedia.org/wiki/Fermion), which include the building blocks of most matter: protons, neutrons, quarks, neutrinos, etc. Their wavefunction must be antisymmetric. If you swap the position of two electrons, the wavefunction gets multiplied by -1. That means that if two electrons are on top of each other, the wavefunction (and the probability of that configuration) will be zero.

This meant we had to develop a new type of neural network that was antisymmetric with respect to its inputs, which we called FermiNet. In most quantum chemistry methods, antisymmetry is introduced using a function called the determinant. The determinant of a matrix has the property that if you swap two rows, the output gets multiplied by -1, just like a wavefunction for fermions.

So, you can take a bunch of single-electron functions, evaluate them for every electron in your system, and pack all of the results into one matrix. The determinant of that matrix is then a properly antisymmetric wavefunction. The major limitation of this approach is that the resulting function — known as a [Slater determinant](https://en.wikipedia.org/wiki/Slater_determinant) — is not very general.

Wavefunctions of real systems are usually far more complicated. The typical way to improve on this is to take a large linear combination of Slater determinants — sometimes millions or more — and add some simple corrections based on pairs of electrons. Even then, this may not be enough to accurately compute energies.

![Animation of a Slater determinant. Each curve is a slice through one of the orbitals shown above. When electrons 1 and 2 swap positions, the rows of the Slater determinant swap, and the wavefunction is multiplied by -1. This guarantees that the Pauli exclusion principle is obeyed.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62275ec6f3af2be16725b398_Fig202.gif)

Animation of a Slater determinant. Each curve is a slice through one of the orbitals shown above. When electrons 1 and 2 swap positions, the rows of the Slater determinant swap, and the wavefunction is multiplied by -1. This guarantees that the Pauli exclusion principle is obeyed.

Deep neural networks can often be far more efficient at representing complex functions than linear combinations of basis functions. In FermiNet, this is achieved by making each function going into the determinant a function of all electrons (see footnote). This goes far beyond methods that just use one- and two-electron functions. FermiNet has a separate stream of information for each electron. Without any interaction between these streams, the network would be no more expressive than a conventional Slater determinant.

To go beyond this, we average together information from across all streams at each layer of the network, and pass this information to each stream at the next layer. That way, these streams have the right symmetry properties to create an antisymmetric function. This is similar to how [graph neural networks](https://deepmind.com/blog/article/traffic-prediction-with-advanced-graph-neural-networks) aggregate information at each layer.

Unlike the Slater determinants, FermiNets are [universal function approximators](https://arxiv.org/abs/2007.15298), at least in the limit where the neural network layers become wide enough. That means that, if we can train these networks correctly, they should be able to fit the nearly-exact solution to the Schrödinger equation.

![Animation of FermiNet. A single stream of the network (blue, purple or pink) functions very similarly to a conventional orbital. FermiNet introduces symmetric interactions between streams, making the wavefunction far more general and expressive. Just like a conventional Slater determinant, swapping two electron positions still leads to swapping two rows in the determinant, and multiplying the overall wavefunction by -1.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62275ef038d03f8c2771b096_Fig203.gif)

Animation of FermiNet. A single stream of the network (blue, purple or pink) functions very similarly to a conventional orbital. FermiNet introduces symmetric interactions between streams, making the wavefunction far more general and expressive. Just like a conventional Slater determinant, swapping two electron positions still leads to swapping two rows in the determinant, and multiplying the overall wavefunction by -1.

We fit FermiNet by minimizing the energy of the system. To do that exactly, we would need to evaluate the wavefunction at all possible configurations of electrons, so we have to do it approximately instead. We pick a random selection of electron configurations, evaluate the energy locally at each arrangement of electrons, add up the contributions from each arrangement and minimize this instead of the true energy. This is known as a [Monte Carlo method](https://en.wikipedia.org/wiki/Monte_Carlo_method), because it’s a bit like a gambler rolling dice over and over again. While it’s approximate, if we need to make it more accurate we can always roll the dice again.

Since the wavefunction squared gives the probability of observing an arrangement of particles in any location, it’s most convenient to generate samples from the wavefunction itself — essentially, simulating the act of observing the particles. While most neural networks are trained from some external data, in our case the inputs used to train the neural network are generated by the neural network itself. This means we don’t need any training data other than the positions of the atomic nuclei that the electrons are dancing around.

The basic idea, known as variational quantum Monte Carlo (or VMC for short), has been around since the ‘60s, and it’s generally considered a cheap but not very accurate way of computing the energy of a system. By replacing the simple wavefunctions based on Slater determinants with FermiNet, we’ve dramatically increased the accuracy of this approach on every system we looked at.

![Simulated electrons sampled from FermiNet move around the bicyclobutane molecule.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62275f06cc5567a588e39ae1_Fig204.gif)

Simulated electrons sampled from FermiNet move around the bicyclobutane molecule.

To make sure that FermiNet represents an advance in the state of the art, we started by investigating simple, well-studied systems, like atoms in the first row of the periodic table (hydrogen through neon). These are small systems — 10 electrons or fewer — and simple enough that they can be treated by the most accurate (but exponential scaling) methods.

FermiNet outperforms comparable VMC calculations by a wide margin — often cutting the error relative to the exponentially-scaling calculations by half or more. On larger systems, the exponentially-scaling methods become intractable, so instead we use the coupled cluster method as a baseline. This method works well on molecules in their stable configuration, but struggles when bonds get stretched or broken, which is critical for understanding chemical reactions. While it scales much better than exponentially, the particular coupled cluster method we used still scales as the number of electrons raised to the seventh power, so it can only be used for medium-sized molecules.

We applied FermiNet to progressively larger molecules, starting with lithium hydride and working our way up to bicyclobutane, the largest system we looked at, with 30 electrons. On the smallest molecules, FermiNet captured an astounding 99.8% of the difference between the coupled cluster energy and the energy you get from a single Slater determinant. On bicyclobutane, FermiNet still captured 97% or more of this correlation energy, a huge accomplishment for such a simple approach.

![Graphic depiction of the fraction of correlation energy that FermiNet captures on molecules. The purple bar indicates 99% of correlation energy. Left to right: lithium hydride, nitrogen, ethene, ozone, ethanol and bicyclobutane.](https://lh3.googleusercontent.com/iwsZ_N68iQPV5eSYalaPuFBV92Edq3IuhsMB2BsRUeY1VH7DX7PnFqNyRYdfmQzMvxMunHyOAz-J7LObJA8i-BDkMYhxq8eHIym3WW-eJxyzLi4nZH8=w1440)

Graphic depiction of the fraction of correlation energy that FermiNet captures on molecules. The purple bar indicates 99% of correlation energy. Left to right: lithium hydride, nitrogen, ethene, ozone, ethanol and bicyclobutane.

While coupled cluster methods work well for stable molecules, the real frontier in computational chemistry is in understanding how molecules stretch, twist and break. There, coupled cluster methods often struggle, so we have to compare against as many baselines as possible to make sure we get a consistent answer.

We looked at two benchmark stretched systems: the nitrogen molecule (N2) and the hydrogen chain with 10 atoms (H10). Nitrogen is an especially challenging molecular bond because each nitrogen atom contributes three electrons. The hydrogen chain, meanwhile, is of interest for [understanding how electrons behave in materials](https://www.simonsfoundation.org/2020/09/14/infinitely-long-chains-of-hydrogen-atoms-have-surprising-properties-including-a-metallic-phase/), for instance, predicting whether or not a material will conduct electricity.

On both systems, the coupled cluster methods did well at equilibrium, but had problems as the bonds were stretched. Conventional VMC calculations did poorly across the board but FermiNet was among the best methods investigated, no matter the bond length.

## A new way to compute excited states

In August 2024, we [published the next phase of this work](https://www.science.org/doi/abs/10.1126/science.adn0137) in Science. Our research proposes a solution to one of the most difficult challenges in computational quantum chemistry: understanding how molecules transition to and from excited states when stimulated.

FermiNet originally focused on the ground states of molecules, the lowest energy configuration of electrons around a given set of nuclei. But when molecules and materials are stimulated by a large amount of energy, like being exposed to light or high temperatures, the electrons might get kicked into a higher energy configuration — an excited state.

Excited states are fundamental for understanding how matter interacts with light. The exact amount of energy absorbed and released creates a unique fingerprint for different molecules and materials, which affects the performance of technologies ranging from solar panels and LEDs to semiconductors, photocatalysts and more. They also play a critical role in biological processes involving light, like photosynthesis and vision.

Accurately computing the energy of excited states is significantly more challenging than computing ground state energies. Even gold standard methods for ground state chemistry, like coupled cluster, have [shown errors](https://pubs.acs.org/doi/10.1021/acs.jctc.4c00410) on excited states that are dozens of times too large. While we wanted to extend our work on FermiNet to excited states, existing methods didn't work well enough for neural networks to compete with state-of-the-art approaches.

We developed a novel approach to computing excited states that’s more robust and general than prior methods. Our approach can be applied to any kind of mathematical model, including FermiNet and other neural networks. It works by finding the ground state of an expanded system with extra particles, so existing algorithms for optimization can be used with little modification.

We validated this work on a wide range of benchmarks, with [highly-promising results](https://www.science.org/doi/abs/10.1126/science.adn0137). On a small but complex molecule called the [carbon dimer](https://en.wikipedia.org/wiki/Diatomic_carbon), we achieved a mean absolute error (MAE) of 4 meV, which is five times closer to experimental results than prior gold standard methods reaching 20 meV. We also tested our method on some of the most challenging systems in computational chemistry, where two electrons are excited simultaneously, and found we were within around 0.1 eV of the most demanding, complex calculations done to date.

Today, we’re [open sourcing our latest work](https://zenodo.org/records/11937084), and hope the research community will build upon our methods to explore the unexpected ways matter interacts with light.

[Read our latest paper in Science](https://www.science.org/doi/abs/10.1126/science.adn0137)[Read our original paper](https://journals.aps.org/prresearch/abstract/10.1103/PhysRevResearch.2.033429)[Download the code](https://github.com/google-deepmind/ferminet)

**Acknowledgements**

Our new research on excited states was developed with Ingrid von Glehn, Halvard Sutterud and Simon Axelrod.

FermiNet was developed by David Pfau, James S. Spencer, Alexander G. D. G. Matthews and W. M. C. Foulkes.

With thanks to Jess Valdez and Arielle Bier for support on the blog, and Jim Kynvin, Adam Cain and Dominic Barlow for the figures.

**Footnotes**

FermiNet also has streams for every pair of electrons, and information from these streams is passed back to the single-electron streams. For simplicity, we chose not to visualize this in the blog post, but details can be found in the paper.
