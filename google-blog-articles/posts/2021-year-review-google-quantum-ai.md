---
title: "2021 Year in Review: Google Quantum AI"
source: https://blog.google/innovation-and-ai/technology/research/2021-year-review-google-quantum-ai/
site: google-blog
date: 2021-12-30
authors: Emily Mount
crawled: 2026-09-13
---

Google’s Quantum AI team has had a productive 2021. Despite ongoing global challenges, we’ve made significant progress in our effort to build a fully error-corrected quantum computer, working towards our next hardware milestone of building an error-corrected quantum bit (qubit) prototype. At the same time, we have continued our commitment to realizing the potential of quantum computers in various applications. That's why we [published results](https://quantumai.google/research) in top journals, collaborated with researchers across academia and industry, and expanded our [team](https://quantumai.google/team) to bring on new talent and expertise.

### An update on hardware

The Quantum AI team is determined to build an error-corrected quantum computer within the next decade, and to simultaneously use what we learn along the way to deliver helpful—and even transformational—quantum computing applications. This [long-term commitment](https://www.wsj.com/articles/google-aims-for-commercial-grade-quantum-computer-by-2029-11621359156) is expanded broadly into three key questions for our quantum hardware:

1. Can we demonstrate that quantum computers can outperform the classical supercomputers of today in a specific task? We [demonstrated beyond-classical computation in 2019](https://www.nature.com/articles/s41586-019-1666-5).
2. Can we build a prototype of an error-corrected qubit? In order to use quantum computers to their full potential, we will need to realize quantum error correction to overcome the noise that is present during our computations. As a key step in this direction, we aim to realize the primitives of quantum error correction by redundantly encoding quantum information across several physical qubits, demonstrating that such redundancy leads to an improvement over using individual physical qubits. This is our current target.
3. Can we build a logical qubit which does not have errors for an arbitrarily long time? Logical qubits encode information redundantly across several physical qubits, and are able to reduce the impact of noise on the overall quantum computation. Putting together a few thousand logical qubits would allow us to realize the full potential of quantum computers for various applications.

An [interactive map of our journey to build an error-corrected quantum computer](https://quantumai.google/learn/map)

![An  interactive map of our journey to build an error-corrected quantum computer.](https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/Scroll_Journey_02.gif)

### Progress toward building an error-corrected qubit prototype

The distance between the noisy quantum computers of today and the fully error-corrected quantum computers of the future is vast. In 2021, we made significant progress in closing this gap by working toward building a prototype logical qubit whose errors are smaller than those of the physical qubits on our chips.

This work requires improvements across the entire quantum computing stack. We have made chips with better qubits, improved the methods that we use to package these chips to better connect them with our control electronics, and developed [techniques to calibrate large chips with several dozens of qubits simultaneously](https://quantumai.google/cirq/tutorials/google/floquet_calibration_example).

These improvements culminated in two key results. First, we are now able to [reset our qubits with high fidelity](https://www.nature.com/articles/s41467-021-21982-y), allowing us to reuse qubits in quantum computations. Second, we have realized mid-circuit measurement that allows us to keep track of computation within quantum circuits. Together, the high-fidelity resets and mid-circuit measurements were used in our recent demonstration of [exponential suppression of bit and phase flip errors](https://www.nature.com/articles/s41586-021-03588-y) using repetition codes, resulting in 100x suppression of these errors as the size of the code grows from 5 to 21 qubits.

[Suppression of logical errors as the number of qubits in the repetition code is increased](https://www.nature.com/articles/s41586-021-03588-y). As we increase the code size from 5 to 21 qubits, we see 100x reduction in logical. Image acknowledgement: Kevin Satzinger/Google Quantum AI

![Chart chronicling repetition code](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Fig_Abe_EOY_blog_2021.width-1200.format-webp.webp)

Repetition codes, an error correction tool, enable us to trade-off between resources (more qubits) and performance (lower error) which will be central in guiding our hardware research and development going forward. This year we showed how [error decreases as we increase the number of included qubits for a 1-dimensional code](https://www.nature.com/articles/s41586-021-03588-y). We are currently running experiments to extend these results to two-dimensional surface codes which will correct errors more comprehensively.

### Applications of quantum computation

In addition to building quantum hardware, our team is also looking for clear margins of quantum advantage in real world applications. With our collaborators in academia and industry, we are exploring fields where quantum computers can provide significant speedups, with realistic expectations that [error-corrected quantum computers will likely require better than quadratic speedups for meaningful improvements](https://journals.aps.org/prxquantum/abstract/10.1103/PRXQuantum.2.010103).

As always, our collaborations with academic and industry partners were invaluable in 2021. One notable collaboration with Caltech showed that, under certain conditions, [quantum machines can learn about physical systems from exponentially fewer experiments](https://scirate.com/arxiv/2112.00778) than what is conventionally required. This novel method was validated experimentally using 40 qubits and 1300 quantum operations, demonstrating a substantial quantum advantage even with the noisy quantum processors we have today. This paves the way to more innovation in quantum machine learning and quantum sensing, with potential near-term use cases.

In collaboration with researchers at Columbia University, we [combined one of the most powerful techniques for chemical simulation, Quantum Monte Carlo, with quantum computation](https://arxiv.org/abs/2106.16235). This approach surpasses previous methods as a promising quantum approach to ground state many-electron calculations, which are critical in creating new materials and understanding their chemical properties. When we run a component of this technique on a real quantum computer, we are able to double the size of prior calculations without sacrificing accuracy of the measurements, even in the presence of noise on a device with up to 16 qubits. The resilience of this method to noise is an indication of its potential for scalability even on today’s quantum computers.

We continue to study how quantum computers can be used to simulate quantum physical phenomena—as was most recently reflected in our experimental [observation of a time crystal on a quantum processor](https://www.nature.com/articles/s41586-021-04257-w) ([Ask a Techspert: What exactly is a time crystal?](https://blog.google/inside-google/googlers/ask-techspert-what-exactly-time-crystal/)). This was a great moment for theorists, who’ve pondered the possibility of time crystals for nearly a century. In other work, we also explored the emergence of quantum chaotic dynamics by experimentally [measuring out-of-time-ordered correlations on one of our quantum computers](https://www.science.org/doi/10.1126/science.abg5029), which was done jointly with collaborators at the NASA Ames Research Center; and experimentally [measuring the entanglement entropy of the ground state of the Toric code Hamiltonian](https://www.science.org/doi/10.1126/science.abi8378) by creating its eigenstates using shallow quantum circuits with collaborators at the Technical University of Munich.

Our collaborators contributed to, and even inspired, some of our most impactful research in 2021. Quantum AI remains committed to discovering and realizing meaningful quantum applications in collaboration with scientists and researchers from across the world in 2022 and beyond as we continue our focus on machine learning, chemistry, and many-body quantum physics.

You can find a list of all our publications [here](https://quantumai.google/research/publications).

### Continuing investment in the quantum computing ecosystem

This year, at Google’s annual developer conference, Google I/O, we [reaffirmed](https://blog.google/technology/ai/unveiling-our-new-quantum-ai-campus/) our commitment to the roadmap and investments required to make a useful quantum computer within the decade. While we were busy growing in Santa Barbara, we also continue to support the enablement of researchers in the quantum community through our open source software. Our quantum programming framework, [Cirq](https://github.com/quantumlib/cirq), continues to improve with contributions from the community. 2021 also saw the release of specialized tools in collaboration with partners in the ecosystem. Two examples of these are:

- The release of a [new Fermionic Quantum Simulator](https://opensource.googleblog.com/2021/11/Efficient%20emulation%20of%20quantum%20circuits%20for%20chemistry.html) for quantum chemistry applications in collaboration with QSimulate, taking advantage of the symmetry in quantum chemistry problems to provide efficient simulations.
- A significant [upgrade to qsim](https://opensource.googleblog.com/2021/11/Upgrading%20qsim%20Google%20Quantum%20AIs%20Open%20Source%20Quantum%20Simulator%20.html) which allows for simulation of noisy quantum circuits on high performance processors such as GPUs via Google Cloud, and [qsim integration with NVIDIA’s cuQuantum SDK](https://opensource.googleblog.com/2021/11/qsim%20integrates%20with%20NVIDIA%20cuQuantum%20SDK%20to%20accelerate%20quantum%20circuit%20simulations%20on%20NVIDIA%20GPUs.html) to enable qsim users to make the most of NVIDIA GPUs when developing quantum algorithms and applications.

We also released an open-source tool called [stim](https://github.com/quantumlib/stim), which provides a [10000x speedup when simulating error correction circuits](https://quantum-journal.org/papers/q-2021-07-06-497/).

You can access our portfolio of open-source software [here](https://quantumai.google/software).

### Looking toward 2022

Resident quantum scientist [Qubit the Dog](https://blog.google/technology/ai/qubit-dog-big-questions-quantum-computing/) taking part in a holiday sing-along led by team members Jimmy Chen and Ofer Naaman.

![Resident quantum scientist Qubit the Dog taking part in a holiday sing-along.](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/IMG-1324.width-1200.format-webp.webp)

Through teamwork, collaboration, and some innovative science, we are excited about the progress that we have seen in 2021. We have big expectations for 2022 as we focus on progressing through our hardware milestones, the discovery of new quantum algorithms, and the realization of quantum applications on the quantum processors of today. To tackle our difficult mission, we are [growing our team](https://quantumai.google/team/careers), building on our existing [network of collaborators](https://quantumai.google/research/outreach), and expanding our [Santa Barbara campus](https://quantumai.google/hardware/our-lab). Together with the broader quantum community, we are excited to see the progress that quantum computing makes in 2022 and beyond.
