---
title: "Our quantum hardware: the engine for verifiable quantum advantage"
source: https://blog.google/innovation-and-ai/technology/research/quantum-hardware-verifiable-advantage/
site: google-blog
date: 2025-10-22
authors: Yu Chen
crawled: 2026-09-13
---

Today, powered by our high-performance quantum chip, [Willow](https://blog.google/technology/research/google-willow-quantum-chip/), we have achieved the [first-ever demonstration of verifiable quantum advantage](https://blog.google/technology/research/quantum-echoes-willow-verifiable-quantum-advantage/). This milestone is a critical step toward realizing useful quantum computation, a feat made possible by the precision and speed engineered into our quantum hardware systems.

### Willow: engineering best-in-class performance

Willow, our state-of-the-art quantum chip, is built from superconducting quantum circuits. This field of research began with the groundbreaking discovery of the macroscopic quantum effect in 1985, an achievement that earned John Clarke, Michel Devoret, and John Martinis the status of 2025 Physics Nobel Laureates. Utilizing these circuits, superconducting qubits function as macroscopic "artificial atoms." Over the past 40 years, driven by the mature integrated circuit fabrication and active research in both academia and industry, these qubits have demonstrated an excellent balance of performance and scalability. This makes them a leading platform for building a fault-tolerant quantum computer.

Building on the foundation of this leading platform, we set out to demonstrate its power in a complex, practical application, to take quantum computing closer to delivering real-world benefits for people. To reveal hidden information about the inner dynamics of quantum systems, such as molecules, we successfully executed the Quantum Echoes algorithm. This algorithm relies on reversing the flow of quantum data in the quantum computers, which in turn places strong demands on Willow's performance at the system scale. It requires running the Willow chip with a large set of quantum gates and a high volume of quantum measurements — two key elements required to distill useful signals from background noise.

The current-generation Willow chip, benefiting from continuous post-release improvements, delivers best-in-class performance at scale. Across its entire 105-qubit array, it features fidelities of 99.97% for single-qubit gates, 99.88% for entangling gates, and 99.5% for readout, all operating at an unmatched speed of tens to hundreds of nanoseconds.

![Dark rectangular microchip resting on a reflective wafer substrate labeled "Quantum AI" and "Willow." The substrate displays fine etched traces and patterns.](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/QuantumWIllow_Chip.width-1200.format-webp.webp)

These high-precision quantum gates enabled us to perform the highly complex Quantum Echoes algorithms, involving large-scale quantum interferences and entanglement. It concretely placed our results in a regime beyond the capabilities of classical computers.

Furthermore, this precision is matched by the fact that our system can perform millions of Quantum Echoes measurements in just tens of seconds. This speed was instrumental in enabling a staggering one trillion measurements over the course of this project—a significant portion of *all* measurements ever performed on *all* quantum computers combined. This solidifies our work as one of the most complex experiments in the history of quantum computing.

![Intricate, multi-tiered gold and brass structure of a quantum computer cryostat, connected by hundreds of dense, wavy black coaxial cables.](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/QuantumComputer.width-1200.format-webp.webp)

### The road to fault tolerance: our strategic roadmap

Since its inception, we have been fully committed to the Google Quantum AI Roadmap toward building a fault-tolerant quantum computer. We have demonstrated progress with completion of the first two milestones: beyond-classical quantum computation in 2019 and a quantum error correction prototype in 2023. With the release of Willow in 2024, we further progressed along our roadmap by demonstrating below-threshold quantum error correction, towards Milestone 3.

![Infographic timeline of a quantum computing roadmap, showing six milestones from physical quantum chips to a large error-corrected quantum computer.](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/QuantumWillow_Roadmap.width-1200.format-webp.webp)

Today’s demonstration of verifiable quantum advantage marks another crucial step forward. It not only highlights our persistent efforts in exploring useful quantum applications, but also strengthens our confidence in using superconducting qubits for large-scale, complex quantum computation.

As we march toward our next milestone — a long-lived logical qubit — we are fully aware of the numerous challenges ahead. Reaching our ultimate goal will require orders-of-magnitude improvement in system performance and scale, with millions of components to be developed and matured. Despite these hurdles, we remain committed to navigating this path forward.
