---
title: "Our new Quantum Virtual Machine will accelerate research and help people learn quantum computing"
source: https://blog.google/innovation-and-ai/technology/research/our-new-quantum-virtual-machine-will-accelerate-research-and-help-people-learn-quantum-computing/
site: google-blog
date: 2022-07-19
authors: Catherine Vollgraff Heidweiller
crawled: 2026-09-13
---

Several decades ago, quantum computers were only a concept — a distant idea discussed mostly in lecture halls. Flash forward to today, and the race is on to build fault-tolerant quantum computers and discover new algorithms to apply them in useful ways.

For all the aspirations of quantum computing, the reality is that unlocking its potential to solve real-world problems is as challenging as building the quantum computers themselves. This got us thinking…how can we empower more people to join us on the quest to discover quantum algorithms and applications? Can we make prototyping quantum algorithms for near term quantum computers free of cost and easy to get started with so that people can focus on the challenge at hand? Can we provide people with the tools they need to equip themselves with the quantum programming skills required for application development?

At Google Quantum AI, we have a long history of making tools we build for our own research available to the public free of cost. Today we are adding the [Quantum Virtual Machine](http://quantumai.google/quantum-virtual-machine) to the list. The Quantum Virtual Machine (QVM) emulates the experience and results of programming one of the quantum computers in our lab, from circuit validation to processor infidelity. We feed measurements from our Sycamore processors, such as qubit decay, dephasing, gate and readout errors into the QVM and combine these with the qubit connectivity of the device to simulate quantum processor-like output, using our physics research team’s models. You can see comparisons between results obtained from experiments on a Sycamore chip and the QVM [on this site](https://arxiv.org/abs/2111.02396).

The Quantum Virtual Machine can be deployed instantly [from a Colab notebook](http://quantumai.google/quantum-virtual-machine) and is available free of cost. You do not have to wait in a queue to get your program’s results and can iterate on results quickly. This, combined with processor-like output makes the QVM a great tool for prototyping, testing and optimizing your quantum circuit for near term quantum hardware. Users can currently emulate two of our processors: Weber and Rainbow. Weber is the Sycamore processor that was used in [our beyond-classical experiments published in Nature in 2019](https://www.nature.com/articles/s41586-019-1666-5). Rainbow was used in [our experiments demonstrating the variational quantum eigensolver on quantum chemistry problems published in Science](https://www.science.org/doi/10.1126/science.abb9811).

Once you have deployed your Quantum Virtual Machine, you can run your quantum program on a grid of virtual qubits. If you require more qubits than can be simulated through Colab, the QVM can be supercharged with additional high-performance compute of your choice. [This workflow](https://quantumai.google/qsim/tutorials/multinode) helps you set up a simulation on multiple parallel compute nodes with Google Cloud. To build your quantum program, you can use Cirq 1.0, the [newly released](https://opensource.googleblog.com/2022/07/Cirq-Turns-1.0.html) version of our open-source quantum programming framework.

We hope that you will find the Quantum Virtual Machine useful while exploring quantum computing, whether for research or education. For educators and their students, the QVM makes it possible to complete coursework and projects on a top quality processor, without running into the long and unpredictable queues that are common in the industry. We have also created supporting documentation that exposes several of the features of the QVM and Cirq 1.0 to enable students to onboard quickly.

With every major improvement in quantum hardware, the need to discover useful applications and to develop the global quantum workforce of the future grows. Join us on our quest to push the boundaries of innovation in quantum algorithms using the Quantum Virtual Machine. Get started at [quantumai.google/software](http://quantumai.google/software).
