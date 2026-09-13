---
title: "Meet Willow, our state-of-the-art quantum chip"
source: https://blog.google/innovation-and-ai/technology/research/google-willow-quantum-chip/
site: google-blog
date: 2024-12-09
authors: Hartmut Neven
crawled: 2026-09-13
---

*Last updated: June 12, 2025*

Today I’m delighted to announce Willow, our latest quantum chip. Willow has state-of-the-art performance across a number of metrics, enabling two major achievements.

- The first is that Willow can reduce errors exponentially as we scale up using *more* qubits. This cracks a key challenge in quantum error correction that the field has pursued for almost 30 years.
- Second, Willow performed a standard benchmark computation in under five minutes that would take one of today’s [fastest supercomputers](https://www.olcf.ornl.gov/frontier/) 10 septillion (that is, 1025) years — a number that vastly exceeds the age of the Universe.

The Willow chip is a major step on a journey that began over 10 years ago. When I founded Google Quantum AI in 2012, the vision was to build a useful, large-scale quantum computer that could harness quantum mechanics — the “operating system” of nature to the extent we know it today — to benefit society by advancing scientific discovery, developing [helpful applications](https://quantumai.google/applications), and tackling some of society's greatest challenges. As part of Google Research, our team has charted a long-term [roadmap](https://quantumai.google/roadmap), and Willow moves us significantly along that path towards commercially relevant applications.

## Exponential quantum error correction — below threshold!

Errors are one of the greatest challenges in quantum computing, since qubits, the units of computation in quantum computers, have a tendency to rapidly exchange information with their environment, making it difficult to protect the information needed to complete a computation. Typically the more qubits you use, the more errors will occur, and the system becomes classical.

Today in [Nature](https://www.nature.com/articles/s41586-024-08449-y), we published results showing that [**the more qubits we use in Willow, the more we** ***reduce*** **errors**](https://research.google/blog/making-quantum-error-correction-work/)**, and the more quantum the system becomes**. We tested ever-larger arrays of physical qubits, scaling up from a grid of 3x3 encoded qubits, to a grid of 5x5, to a grid of 7x7 — and each time, using our latest advances in quantum error correction, we were able to cut the error rate in half. In other words, we achieved an exponential reduction in the error rate. This historic accomplishment is known in the field as “below threshold” — being able to drive errors down while scaling up the number of qubits. You must demonstrate being below threshold to show real progress on error correction, and this has been an outstanding challenge since [quantum error correction](https://journals.aps.org/pra/abstract/10.1103/PhysRevA.52.R2493) was introduced by Peter Shor in 1995.

There are other scientific “firsts” involved in this result as well. For example, it’s also one of the first compelling examples of real-time error correction on a superconducting quantum system — crucial for any useful computation, because if you can’t correct errors fast enough, they ruin your computation before it’s done. And it’s a "beyond breakeven" demonstration, where our arrays of qubits have longer lifetimes than the individual physical qubits do, an unfakable sign that error correction is improving the system overall.

As the first system below threshold, this is the most convincing prototype for a scalable logical qubit built to date. It’s a strong sign that useful, very large quantum computers can indeed be built. Willow brings us closer to running practical, commercially-relevant algorithms that can’t be replicated on conventional computers.

## 10 septillion years on one of today’s fastest supercomputers

As a measure of Willow’s performance, we used the [random circuit sampling (RCS) benchmark](https://research.google/blog/validating-random-circuit-sampling-as-a-benchmark-for-measuring-quantum-progress/). Pioneered by our team and now widely used as a standard in the field, RCS is the classically hardest benchmark that can be done on a quantum computer today. You can think of this as an entry point for quantum computing — it checks whether a quantum computer is doing something that couldn’t be done on a classical computer. Any team building a quantum computer should check first if it can beat classical computers on RCS; otherwise there is strong reason for skepticism that it can tackle more complex quantum tasks. We’ve consistently used this benchmark to assess progress from one generation of chip to the next — we reported Sycamore results in [October 2019](https://blog.google/technology/ai/what-our-quantum-computing-milestone-means/) and again recently in [October 2024](https://www.nature.com/articles/s41586-024-07998-6).

Willow’s performance on this benchmark is astonishing: It performed a computation in under five minutes that would take one of today’s [fastest supercomputers](https://www.olcf.ornl.gov/frontier/) 1025 or 10 septillion years. If you want to write it out, it’s 10,000,000,000,000,000,000,000,000 years. This mind-boggling number exceeds known timescales in physics and vastly exceeds the age of the universe. It lends credence to the notion that quantum computation occurs in many parallel universes, in line with the idea that we live in a multiverse, a [prediction](https://en.wikipedia.org/wiki/The_Fabric_of_Reality) first made by David Deutsch.

These latest results for Willow, as shown in the plot below, are our best so far, but we’ll continue to make progress.

Computational costs are heavily influenced by available memory. Our estimates therefore consider a range of scenarios, from an ideal situation with unlimited memory (▲) to a more practical, embarrassingly parallelizable implementation on GPUs (⬤).

![A chart comparing the performance of different quantum computing platforms, on the task of random circuit sampling (RCS).](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/image_8_dUczXnV.width-1200.format-webp.webp)

Our assessment of how Willow outpaces one of the world’s most powerful classical supercomputers, [Frontier](https://www.olcf.ornl.gov/frontier/), was based on conservative assumptions. For example, we assumed full access to secondary storage, i.e., hard drives, without any bandwidth overhead — a generous and unrealistic allowance for Frontier. Of course, as happened after we announced the first [beyond-classical computation in 2019](https://blog.google/technology/ai/what-our-quantum-computing-milestone-means/), we expect classical computers to keep improving on this benchmark, but the rapidly growing gap shows that quantum processors are peeling away at a double exponential rate and will continue to vastly outperform classical computers as we scale up.

## State-of-the-art performance

Willow was fabricated in our new, state-of-the-art fabrication facility in Santa Barbara — one of only a few facilities in the world built from the ground up for this purpose. System engineering is key when designing and fabricating quantum chips: All components of a chip, such as single and two-qubit gates, qubit reset, and readout, have to be simultaneously well engineered and integrated. If any component lags or if two components don't function well together, it drags down system performance. Therefore, maximizing system performance informs all aspects of our process, from chip architecture and fabrication to gate development and calibration. The achievements we report assess quantum computing systems holistically, not just one factor at a time.

We’re focusing on quality, not just quantity — because just producing larger numbers of qubits doesn’t help if they’re not high enough quality. With 105 qubits, Willow now has best-in-class performance across the two system benchmarks discussed above: quantum error correction and random circuit sampling. Such algorithmic benchmarks are the best way to measure overall chip performance. Other more specific performance metrics are also important; for example, our T1 times, which measure how long qubits can retain an excitation — the key quantum computational resource — are now approaching 100 µs (microseconds). This is an impressive ~5x improvement over our previous generation of chips. If you want to evaluate quantum hardware and compare across platforms, here is a table of key specifications:

Willow’s performance across a number of metrics.

![a table chart reading "Willow System Metrics" with columns showing details like number of qubits (105) and average connectivity (3.47)](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/KW_Fig3.width-1200.format-webp.webp)

## What’s next with Willow and beyond

The next challenge for the field is to demonstrate a first "useful, beyond-classical" computation on today's quantum chips that is relevant to a real-world application. We’re optimistic that the Willow generation of chips can help us achieve this goal. So far, there have been two separate types of experiments. On the one hand, we’ve run the RCS benchmark, which measures performance against classical computers but has no known real-world applications. On the other hand, we’ve done scientifically interesting simulations of quantum systems, which have led to new scientific discoveries but are still within the reach of classical computers. Our goal is to do both at the same time — to step into the realm of algorithms that are beyond the reach of classical computers **and** that are useful for real-world, commercially relevant problems.

Random circuit sampling (RCS), while extremely challenging for classical computers, has yet to demonstrate practical commercial applications.

![an illustrated chart reading "Random Circuit Sampling (RCS): in context](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/KW_Fig2.width-1200.format-webp.webp)

We invite researchers, engineers, and developers to join us on this journey by checking out our [open source software](https://quantumai.google/software) and educational resources, including our [new course on Coursera](https://coursera.org/learn/quantum-error-correction), where developers can learn the essentials of quantum error correction and help us create algorithms that can solve the problems of the future.

![an illustrated card reading "Our quantum computing roadmap" and a timeline showing 6 milestones from "Beyond classical" to "Large error-corrected quantum computer"](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/KW_Fig4.width-1200.format-webp.webp)

My colleagues sometimes ask me why I left the burgeoning field of AI to focus on quantum computing. My answer is that both will prove to be the most transformational technologies of our time, but advanced AI will significantly benefit from access to quantum computing. This is why I named our lab Quantum AI. Quantum algorithms have fundamental scaling laws on their side, as we’re seeing with RCS. There are similar scaling advantages for many foundational computational tasks that are essential for AI. So quantum computation will be indispensable for collecting training data that’s inaccessible to classical machines, training and optimizing certain learning architectures, and modeling systems where quantum effects are important. This includes helping us discover new medicines, designing more efficient batteries for electric cars, and accelerating progress in fusion and new energy alternatives. Many of these future game-changing applications won’t be feasible on classical computers; they’re waiting to be unlocked with quantum computing.
