---
title: "Our Quantum Echoes algorithm is a big step toward real-world applications for quantum computing"
source: https://blog.google/innovation-and-ai/technology/research/quantum-echoes-willow-verifiable-quantum-advantage/
site: google-blog
date: 2025-10-22
authors: Hartmut Neven
crawled: 2026-09-13
---

**Editor’s note:** *Today, we’re announcing research that shows — for the first time in history — that a quantum computer can successfully run a verifiable algorithm on hardware, surpassing even the fastest classical supercomputers (13,000x faster). It can compute the structure of a molecule, and paves a path towards real-world applications. Today’s advance builds on decades of work, and six years of major breakthroughs. Back in 2019, we* [*demonstrated*](https://blog.google/technology/ai/what-our-quantum-computing-milestone-means/) *that a quantum computer could solve a problem that would take the fastest classical supercomputer thousands of years. Then, late last year (2024), our new* [*Willow quantum chip*](https://blog.google/technology/research/google-willow-quantum-chip/) *showed how to dramatically suppress errors, solving a major issue that challenged scientists for nearly 30 years. Today’s breakthrough moves us much closer to quantum computers that can drive major discoveries in areas like medicine and materials science.*

Imagine you’re trying to find a lost ship at the bottom of the ocean. Sonar technology might give you a blurry shape and tell you, "There's a shipwreck down there." But what if you could not only find the ship but also read the nameplate on its hull?

That's the kind of unprecedented precision we've just achieved with our Willow quantum chip. Today, we’re announcing a major algorithmic breakthrough that marks a significant step towards a first real-world application. Just [published in Nature](https://www.nature.com/articles/s41586-025-09526-6), we have demonstrated the [first-ever verifiable quantum advantage](https://research.google/blog/a-verifiable-quantum-advantage/) running the out-of-order time correlator (OTOC) algorithm, which we call Quantum Echoes.

![a picture of Sundar Pichai standing next to a quantum computer](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/QuantumSundar_Inline.width-1200.format-webp.webp)

Quantum Echoes can be useful in learning the structure of systems in nature, from molecules to magnets to black holes, and we’ve demonstrated it runs 13,000 times faster on Willow than the best classical algorithm on one of the world’s fastest supercomputers.

In a separate, proof-of-principle experiment [*Quantum computation of molecular geometry via many-body nuclear spin echoes*](https://quantumai.google/static/site-assets/downloads/quantum-computation-molecular-geometry-via-nuclear-spin-echoes.pdf) (to be posted on arXiv later today), we showed how our new technique — a “molecular ruler” — can measure longer distances than today’s methods, using data from Nuclear Magnetic Resonance (NMR) to gain more information about chemical structure.

### The Quantum Echoes algorithm, a verifiable quantum advantage

This is the first time in history that any quantum computer has successfully run a verifiable algorithm that surpasses the ability of supercomputers. Quantum verifiability means the result can be repeated on our quantum computer — or any other of the same caliber — to get the same answer, confirming the result. This repeatable, beyond-classical computation is the basis for scalable verification, bringing quantum computers closer to becoming tools for practical applications.

Our new technique works like a highly advanced echo. We send a carefully crafted signal into our quantum system (qubits on Willow chip), perturb one qubit, then precisely reverse the signal’s evolution to listen for the "echo" that comes back.

This quantum echo is special because it gets amplified by constructive interference — a phenomenon where quantum waves add up to become stronger. This makes our measurement incredibly sensitive.

This diagram shows the four-step process for creating a quantum echo on our 105-qubit array: run operations forward, perturb one qubit, run operations backward, and measure the result. The signal's overlap reveals how a disturbance spreads across the Willow chip.

This implementation of the Quantum Echoes algorithm is enabled by the advances in [quantum hardware](https://blog.google/technology/research/quantum-hardware-verifiable-advantage/) of our Willow chip. Last year, Willow proved its power with our Random Circuit Sampling benchmark, a test designed to measure maximum quantum state complexity. The Quantum Echoes algorithm represents a new class of challenge because it models a physical experiment. This means this algorithm tests not only for complexity, but also for precision in the final calculation. This is why we call it “quantum verifiable,” meaning the result can be cross-benchmarked and verified by another quantum computer of similar quality. To deliver both precision and complexity, the hardware must have two key traits: extremely low error rates and high-speed operations.

![Hand in a white glove holding a square electronic sensor or microchip. White logos for Willow and a stylized geometric shape are overlaid on the image.](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/WillowChip_4k_Render_02.width-1200.format-webp.webp)

### Towards real world application

Quantum computers will be instrumental in modeling quantum mechanical phenomena, such as the interactions of atoms and particles and the structure (or shape) of molecules. One of the tools scientists use to understand chemical structure is Nuclear Magnetic Resonance (NMR), the same science behind MRI technology. NMR acts as a molecular microscope, powerful enough to let us see the relative position of atoms, which helps us understand a molecule’s structure. Modeling molecules’ shape and dynamics is foundational in chemistry, biology and materials science, and advances that help us do this better underpin progress in fields ranging from biotechnology to solar energy to nuclear fusion.

In a [proof-of-principle experiment](https://quantumai.google/static/site-assets/downloads/quantum-computation-molecular-geometry-via-nuclear-spin-echoes.pdf) in partnership with The University of California, Berkeley, we ran the Quantum Echoes algorithm on our Willow chip to study two molecules, one with 15 atoms and another with 28 atoms, to verify this approach. The results on our quantum computer matched those of traditional NMR, and revealed information not usually available from NMR, which is a crucial validation of our approach.

Just as the telescope and the microscope opened up new, unseen worlds, this experiment is a step toward a ‘quantum-scope’ capable of measuring previously unobservable natural phenomena. Quantum computing-enhanced NMR could become a powerful tool in drug discovery, helping determine how potential medicines bind to their targets, or in materials science for characterizing the molecular structure of new materials like polymers, battery components or even the materials that comprise our quantum bits (qubits).

### What’s next

This demonstration of the first-ever verifiable quantum advantage with our Quantum Echoes algorithm marks a significant step toward the first real-world applications of quantum computing.

As we scale up towards a full-scale, error-corrected quantum computer, we expect many more such useful real-world applications to be invented. Now, we’re focused on achieving Milestone 3 on our [quantum hardware roadmap](https://quantumai.google/roadmap), a long-lived logical qubit.
