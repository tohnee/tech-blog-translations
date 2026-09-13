---
title: "GPT‑5.2 derives a new result in theoretical physics"
date: 2026-02-13
source: https://openai.com/index/new-result-theoretical-physics/
crawled: 2026-09-13
category: research
---

We’ve published a new preprint showing that a type of particle interaction many physicists expected would not occur can in fact arise under specific conditions. The work focuses on gluons, the particles that carry the strong nuclear force. The [preprint](https://arxiv.org/abs/2602.12176) is available on arXiv and is being submitted for publication. In the meantime, we welcome feedback from the community.

The preprint, titled “*Single-minus gluon tree amplitudes are nonzero*,” is authored by Alfredo Guevara (Institute for Advanced Study), Alex Lupsasca (Vanderbilt University and OpenAI), David Skinner (University of Cambridge), and Andrew Strominger (Harvard University), and Kevin Weil (OpenAI) on behalf of OpenAI.

The preprint studies a central concept in particle physics called a scattering amplitude. A scattering amplitude is the quantity physicists use to compute the probability that particles interact in a particular way. For gluons, the particles that carry the strong nuclear force, many amplitudes take unexpectedly simple forms “at tree level” (meaning calculations that keep only the simplest diagrams with no quantum loops). These simplifications have repeatedly revealed deeper structure in quantum field theory, the framework that provides a description of physics that unifies special relativity with quantum mechanics.

One case, however, has generally been treated as absent (having zero amplitude). When one gluon has negative helicity (meaning one of the two possible spin orientations a massless particle can have) and the remaining n−1 n-1 n−1 gluons have positive helicity, standard textbook arguments suggest that the corresponding tree-level amplitude must be zero. As a result, this configuration has largely been set aside.

The preprint shows that this conclusion is too strong. The standard argument assumes generic particle momenta, meaning the directions and energies are not in any special alignment. We identify a specific and precisely defined slice of momentum space where that reasoning no longer applies, known as the half-collinear regime. Half-collinear here means the gluon momenta obey a special alignment condition that is not typical, but is mathematically well-defined and consistent. On this slice, the amplitude does not vanish, and we compute it in a special kinematic regime. This result opens the door to many new questions that will be the subject of subsequent investigations. Important extensions include the computation of the analogous amplitudes for gravitons (the particles that mediate the gravitational force).

A central aspect of the work concerns methodology. The final formula, Eq. (39) in the preprint, was first conjectured by GPT‑5.2 Pro. The human authors worked out the amplitudes for integer n n n up to n=6 n=6 n=6 by hand, obtaining very complicated expressions shown in Eqs. (29)--(32), which correspond to a “Feynman diagram expansion” whose complexity grows superexponentially in n. GPT‑5.2 Pro was able to greatly reduce the complexity of these expressions, providing the much simpler forms in Eqs. (35)--(38). From these base cases, it was then able to spot a pattern and posit a formula valid for all n n n.

An internal scaffolded version of GPT‑5.2 then spent roughly 12 hours reasoning through the problem, coming up with the same formula and producing a formal proof of its validity. The equation was subsequently verified analytically to solve the Berends-Giele recursion relation, a standard step-by-step method for building multi-particle tree amplitudes from smaller building blocks. It was also checked against the soft theorem, which constrains how amplitudes behave when a particle becomes soft.

With the help of GPT‑5.2, these amplitudes have already been extended from gluons to gravitons, and other generalizations are also on their way. These AI-assisted results, and many others, will be reported on elsewhere.

*“The physics of these highly degenerate scattering processes has been something I’ve been curious about since I first ran into them about fifteen years ago, so it is exciting to see the strikingly simple expressions in this paper.*

*It happens frequently in this part of physics that expressions for some physical observables, calculated using textbook methods, look terribly complicated, but turn out to be very simple. This is important because often simple formulas send us on a journey towards uncovering and understanding deep new structures, opening up new worlds of ideas where, amongst other things, the simplicity seen in the starting point is made obvious.*

*To me, “finding a simple formula” has always been fiddly, and also something that I have long felt might be automatable by computers. It looks like across a number of domains we are beginning to see this happen; the example in this paper seems especially well-suited to exploit the power of modern AI tools. I am looking forward to seeing this trend continue towards a general purpose “simple formula pattern recognition” tool in the near future.”*

—Nima Arkani-Hamed, Professor of Physics, Institute for Advanced Study, specializing in theoretical high-energy physics

*“I am already thinking about this preprint’s implications for aspects of my group’s research program. This is clearly journal-level research advancing the frontiers of theoretical physics, and its novelty will inspire future developments and subsequent publications. This preprint felt like a glimpse into the future of AI-assisted science, with physicists working hand-in-hand with AI to generate and validate new insights. There is no question that dialogue between physicists and LLMs can generate fundamentally new knowledge. By coupling GPT‑5.2 with human domain experts, the paper provides a template for validating LLM-driven insights and satisfies what we expect from rigorous scientific inquiry.”*

—Nathaniel Craig, Professor of Physics at the University of California, Santa Barbara (UCSB), specializing in high-energy physics, particle phenomenology, and cosmology
