---
title: "Benchmarking the next generation of never-ending learners"
source: https://deepmind.google/blog/benchmarking-the-next-generation-of-never-ending-learners/
site: deepmind
date: 2022-11-22
authors: Marc’Aurelio Ranzato, Amal Rannen-Triki
crawled: 2026-09-13
---

Learning how to build upon knowledge by tapping 30 years of computer vision research

In just a few years, large-scale deep learning (DL) models have achieved unprecedented success in a variety of domains, from predicting protein structures to natural language processing and vision[1, 2, 3]. Machine learning engineers and researchers have delivered these successes for the most part thanks to powerful new hardware that has enabled their models to scale up and be trained with more data.

Scaling up has resulted in fantastic capabilities, but also means that DL models can be resource intensive. For example, when large models are deployed, whatever they have learned on one task is seldom harnessed to facilitate their learning of the next task. What’s more, once new data or more compute become available, large models are typically retrained from scratch – a costly, time-consuming process.

This raises the question of whether we could improve the trade-off between the efficiency and performance of these large models, making them faster and more sustainable while also preserving their outstanding capabilities. One answer to this is to encourage the development of models that accrue knowledge over time, and that can therefore better adapt more efficiently to new situations and novel tasks.

## Introducing NEVIS’22

Our new paper, [NEVIS’22: A Stream of 100 Tasks Sampled From 30 Years of Computer Vision Research](https://arxiv.org/abs/2211.11747), proposes a playground to study the question of efficient knowledge transfer in a controlled and reproducible setting. The Never-Ending Visual classification Stream (NEVIS’22) is a benchmark stream in addition to an evaluation protocol, a set of initial baselines, and an open-source codebase. This package provides an opportunity for researchers to explore how models can continually build on their knowledge to learn future tasks more efficiently.

NEVIS’22 is actually composed of 106 tasks extracted from publications randomly sampled from the online proceedings of major computer vision conferences over the past three decades. Each task is a supervised classification task, the best understood approach in machine learning. And crucially, the tasks are arranged chronologically, and so, become more challenging and expansive, providing increasing opportunities to transfer knowledge from a growing set of related tasks. The challenge is how to automatically transfer useful knowledge from one task to the next to achieve a better or more efficient performance.

Here are some images derived from datasets referenced in Appendix H of our paper:

NEVIS’22 is reproducible and sufficiently scaled to test state-of-the-art learning algorithms. The stream includes a rich diversity of tasks, from optical character recognition and texture analysis to crowd counting and scene recognition. The task-selection process, being randomly sampled, did not favour any particular approach, but merely reflects what the computer vision community has deemed interesting over time.

NEVIS’22 is not only about data, but also about the methodology used to train and evaluate learning models. We evaluate learners according to their ability to learn future tasks, as measured by their trade-off between error rate and compute (the latter measured by the number of floating-point operations). So, for example, achieving a lower error rate in NEVIS’22 is not sufficient if this comes at an unreasonable computational cost. Instead, we incentivise models to be both accurate and efficient.

## Initial lessons and open challenges

Our initial experiments show that the models that achieve a better trade-off are those that leverage the structure shared across tasks and employ some form of transfer learning. In particular, clever fine-tuning approaches can be rather competitive, even when combined with large pre-trained models. This latter finding highlights the possibility to further improve upon the general representations of large-scale models, opening up an entirely new avenue of research. We believe that NEVIS’22 presents an exciting new challenge for our community as we strive to develop more efficient and effective never-ending learning models.

Discover more about NEVIS’22 by reading [our paper](https://arxiv.org/abs/2211.11747) and downloading [our code](http://github.com/deepmind/dm_nevis).

**Notes**

References

[1] John M Jumper, Richard Evans, Alexander Pritzel, Tim Green, Michael Figurnov, Olaf Ron-neberger, Kathryn Tunyasuvunakool, Russ Bates, Augustin Zídek, Anna Potapenko, Alex Bridgland, Clemens Meyer, Simon A A Kohl, Andy Ballard, Andrew Cowie, Bernardino Romera-Paredes, Stanislav Nikolov, Rishub Jain, Jonas Adler, Trevor Back, Stig Petersen, David A. Reiman, Ellen Clancy, Michal Zielinski, Martin Steinegger, Michalina Pacholska, Tamas Berghammer, Sebastian Bodenstein, David Silver, Oriol Vinyals, Andrew W Senior, Koray Kavukcuoglu, Pushmeet Kohli & Demis Hassabis. Highly accurate protein structure prediction with AlphaFold. Nature, 596:583 – 589, 2021.

[2] Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, Sandhini Agarwal, Ariel Herbert-Voss, Gretchen Krueger, Tom Henighan, Rewon Child, AdityaRamesh, Daniel Ziegler, Jeffrey Wu, Clemens Winter, Chris Hesse, Mark Chen, EricSigler, Mateusz Litwin, Scott Gray, Benjamin Chess, Jack Clark, Christopher Berner, Sam McCandlish, Alec Radford, Ilya Sutskever, and Dario Amodei. Language models are few-shot learners. In H Larochelle, M Ranzato, R Hadsell, M F Balcan, and H Lin, editors, Advances in Neural Information Processing Systems, volume 33, pages 1877-1901. Curran Associates, Inc., 2020

[3] Jean-Baptiste Alayrac, Jeff Donahue, Pauline Luc, Antoine Miech, Iain Barr, Yana Hasson, Karel Lenc, Arthur Mensch, Katie Millican, Malcolm Reynolds, Roman Ring, Eliza Rutherford, Serkan Cabi, Tengda Han, Zhitao Gong, Sina Samangooei, Marianne Monteiro, Jacob Menick, Sebastian Borgeaud, Andrew Brock, Aida Nematzadeh, Sahand Sharifzadeh, Miko-laj Binkowski, Ricardo Barreira, Oriol Vinyals, Andrew Zisserman, and Karen Simonyan. Flamingo: a visual language model for few-shot learning, 2022.
