---
title: "The road to useful quantum computing applications"
source: https://blog.google/innovation-and-ai/technology/research/useful-quantum-computing-applications/
site: google-blog
date: 2025-11-13
authors: Ryan Babbush
crawled: 2026-09-13
---

Sometimes, history happens all at once. A few short years can usher in decades of progress and innovation. We’re now seeing that with quantum computing. [Forty years of research](https://blog.google/technology/research/quantum-hardware-verifiable-advantage/), work and investment are converging, and the grand challenge of building large-scale, capable quantum computers is within humanity's reach.

The quantum computing community has made remarkable progress on hardware, and our high-performance Willow chip is leading the charge. We’re now focused on achieving our [next milestone](https://quantumai.google/roadmap), a long-lived logical qubit, which will enable more powerful and stable quantum computers. While challenges remain, there’s growing confidence at Google and across the community that no insurmountable obstacles exist on the road ahead.

However, a critical question remains: *what will we actually do with the full power of a fault-tolerant quantum computer?*

To map the journey from an idea to a deployed, real-world tool, our team developed a five-stage framework, published in our paper, “[The Grand Challenge of Quantum Applications](http://arxiv.org/abs/2511.09124).” Today, we are sharing these five stages and evaluating where some of the most promising applications currently stand in the process.

### The five stages building from idea to impact

![Six-stage flow diagram for quantum application development (0-V), showing a Stage II-IV benchmark bypass.](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/stages_highres_1.width-1200.format-webp.webp)

The wide-ranging research required to uncover useful quantum computing applications can be divided into five main stages, and an idea typically passes through all of them on the way to real-world impact.

**Stage I - Discovery:** A new abstract quantum algorithm — like [Simon’s algorithm](https://en.wikipedia.org/wiki/Simon%27s_problem) for finding hidden patterns, [Grover's algorithm](https://en.wikipedia.org/wiki/Grover%27s_algorithm) for unstructured search or the [quantum phase estimation algorithm](https://en.wikipedia.org/wiki/Quantum_phase_estimation_algorithm) — is discovered and analyzed. These algorithms may theoretically tackle problems faster than classical methods, and deliver foundational results in a given field, but their direct practical utility is often uncertain or limited at this early stage. This work is frequently built upon the most basic, fundamental research into quantum computation's features and limits (Stage 0).

**Stage II - Finding the right problem instances:** This stage focuses on finding and characterizing concrete, verifiable problem instances where a quantum algorithm demonstrates a true advantage over all known classical methods. For example, addressing an abstract Stage I problem like “finding a molecule's lowest energy state” requires identifying specific molecules (the "problem instances") for which a quantum computer will provide an advantage. This can be challenging because often many instances of real-world problems are solvable by classical computers. The quantum advantage may only be guaranteed in the most complex cases, and classically hard instances can be difficult to identify. The quantum algorithm must successfully compete against a vast array of constantly improving classical approaches to pass this stage.

**Stage III - Establishing real-world advantage:** This is the "so what?" stage. Having characterized problem instances that we can solve better than classical, this stage asks whether those instances connect to *specific, real-world* use cases. For example, how does simulating particular molecules we know to be challenging classically (the Stage II “problem instances”) create value for drug discovery? The first common issue at this stage is that the devil is in the details, and it is often challenging to find real world use cases that fit the criteria for quantum advantage identified in Stage II. There is also a knowledge gap for both quantum and application area experts. For example, quantum algorithmists often don't know the fine details of an application area like battery chemistry, and battery engineers don't know the fine print of quantum algorithms.

**Stage IV - Engineering for use:** Once we have a real-world problem instance with quantum advantage, we need to understand how much it will actually cost computationally. This stage is where we do practical optimization, multiple layers of compilation and resource estimation for a specific use case. Key questions here include: how many qubits and gates? How long will the algorithm need to run? For fault-tolerant quantum computing use cases (i.e. cases that use quantum error correction) Stage IV also involves mapping how this error correction will be implemented.

Over the last decade, Stage IV research has reduced the estimated resources required to solve problems like factoring integers (left) and simulating molecules (right) by many orders of magnitude

![Double scatter plot showing Physical Qubits decreasing ($10^9$ to $10^6$) and FeMoco Toffoli Gates decreasing ($10^{11}$ to $10^9/10^8$) from 2010 to 2025.](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/RoadtoQuantum_Graphs.width-1200.format-webp.webp)

**Stage V - Application deployment:** The final leg of the journey. The proven quantum solution is deployed and used in a practical, real-world workflow where it provides an advantage over all classical alternatives. This stage lies in the future. Due to the still-early state of hardware development, no end-to-end quantum application has yet been implemented in hardware with a conclusive advantage on a problem of real-world consequence.

### Where do some of today’s most promising applications stand?

Our framework shows where three potential applications stand on their respective journeys.

![Title: Quantum simulation (Stages III & IV). Text details research progress, including reduced computational resources for quantum chemistry and fusion reactor modeling (Stage IV), and the development of open-source tools like Qualtran and the Quantum Echoes algorithm.](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/QuantumCarousel1_v2.width-100.format-webp.webp)

For details, see our Stage III research on [industrial quantum simulation](https://research.google/blog/developing-industrial-use-cases-for-physical-simulation-on-future-error-corrected-quantum-computers/) and [Quantum Echoes](https://blog.google/technology/research/quantum-echoes-willow-verifiable-quantum-advantage/) for [measuring molecules](https://arxiv.org/abs/2510.19550); our Stage IV papers on [quantum chemistry](https://journals.aps.org/prx/abstract/10.1103/pb2g-j9cw), [fusion reactors](https://www.pnas.org/doi/10.1073/pnas.2317772121), and [physics simulations](https://journals.aps.org/prx/abstract/10.1103/pb2g-j9cw); and the [Qualtran software library](https://quantumai.google/qualtran).

![Slide titled "Cryptanalysis (Stage IV)" with a blue vertical bar and an orange circle graphic. Text discusses Shor's quantum algorithm breaking current public-key cryptography and the focus on Stage IV for the transition to post-quantum cryptography.](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/QuantumCarousel2_v2.width-100.format-webp.webp)

For details, see our [security blog](https://security.googleblog.com/2025/05/tracking-cost-of-quantum-factori.html) and [accompanying paper](https://arxiv.org/abs/2505.15917) on factoring large integers using a quantum computer.

![Presentation slide titled "Optimization & Machine Learning (Stages I & II)." The accompanying text details work on a new quantum algorithm and decoded quantum interferometry (DQI), reporting Stage II and Stage IV results, and finding that quantum advantage requires less than a million physical qubits.](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/QuantumCarousel3_v2.width-100.format-webp.webp)

For details, see our recent papers on [optimization](https://journals.aps.org/prx/abstract/10.1103/PhysRevX.15.021077) and [machine learning](https://arxiv.org/abs/2509.09033), and our [Stage II](https://www.nature.com/articles/s41586-025-09527-5) and [Stage IV](https://arxiv.org/abs/2510.10967) work on [DQI](https://research.google/blog/a-new-quantum-toolkit-for-optimization/).

### Next steps and the work ahead

Our framework helps us see that while the community has made impressive progress on new algorithms and resource estimates, there are real bottlenecks in identifying the right problem instances and finding real-world advantage. We highlight two of the calls to action from our paper, to help humanity reach the full potential of quantum computing applications.

- **Adopt an algorithm-first approach:** Instead of starting with a vague business problem, which has had limited historical success, we should focus on getting algorithms to a level of proven advantage (clearing Stage II) and *then* actively search for a real-world application (Stage III). In addition, a useful solution should be verifiable to lead to a practical application. Our Quantum Echoes experiment is the first example of an algorithm run on a quantum computer with verifiable quantum advantage.
- **Bridge the knowledge gap:** We need to cultivate more cross-disciplinary experts and teams who can speak both quantum and a specific domain language (e.g., chemistry, finance, materials science). We are optimistic that AI could be a powerful tool for bridging this Stage III-related gap, by scanning vast amounts of scientific literature to find connections between abstract quantum problems and practical industry challenges.

Governments and other research funders can play a key role in addressing gaps by targeting programs and funding to Stage II and III applications development.

Building a fault-tolerant quantum computer is a grand challenge of hardware. Using it is a grand challenge of applications — and our five-stage framework offers the community a clearer way to see the road we're on and the challenges ahead, as we work toward quantum computing that delivers real-world benefits.

Read the full details in our perspective paper, "[The Grand Challenge of Quantum Applications](http://arxiv.org/abs/2511.09124)."
