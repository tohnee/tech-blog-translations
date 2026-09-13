---
title: "Population based training of neural networks"
source: https://deepmind.google/blog/population-based-training-of-neural-networks/
site: deepmind
date: 2017-11-27
authors: Max Jaderberg
crawled: 2026-09-13
---

Neural networks have shown great success in everything from playing Go and Atari games to image recognition and language translation. But often overlooked is that the success of a neural network at a particular application is often determined by a series of choices made at the start of the research, including what type of network to use and the data and method used to train it. Currently, these choices - known as hyperparameters - are chosen through experience, random search or a computationally intensive search processes.

In our [most recent paper](https://arxiv.org/abs/1711.09846), we introduce a new method for training neural networks which allows an experimenter to quickly choose the best set of hyperparameters and model for the task. This technique - known as Population Based Training (PBT) - trains and optimises a series of networks at the same time, allowing the optimal set-up to be quickly found. Crucially, this adds no computational overhead, can be done as quickly as traditional techniques and is easy to integrate into existing machine learning pipelines.

The technique is a hybrid of the two most commonly used methods for hyperparameter optimisation: random search and hand-tuning. In random search, a population of neural networks are trained independently in parallel and at the end of training the highest performing model is selected. Typically, this means that a small fraction of the population will be trained with good hyperparameters, but many more will be trained with bad ones, wasting computer resources.

![Diagram showing three separate, independent parallel training runs where fixed hyperparameters influence each model's sequential training progress and final performance over time.](https://lh3.googleusercontent.com/n8IJcqZq44hIxXNPS5X5mh3XLwyP18Q_WHZ7iHWhw1u9pWbIwiFBVtl5vQvs3ut1WMLa40RdH6mFx8q-4UlX7X7T9dZLk75svweGbtJ8yPXbHyfUfg=w1440)

Random search of hyperparameters, where many hyperparameters are tried in parallel, but independently. Some hyperparameters will lead to models with good performance, but others will not

With hand tuning, researchers must guess at the best hyperparameters, train their models using them, and then evaluate the performance. This is done over and over, until the researcher is happy with the performance of the network. Although this can result in better performance, the downside is that this takes a long time, sometimes taking weeks or even months to find the perfect set-up. And while there are ways of automating this process - such as Bayesian optimisation - it still takes a long time and requires many sequential training runs to find the best hyperparameters.

![Diagram showing the sequential process of Population Based Training, where a model's hyperparameters and parameters are periodically evaluated, with poorly performing models copying parameters from better ones and exploring new hyperparameters over time.](https://lh3.googleusercontent.com/2w0BX5atTa8QeO3UMI_YnmUERKWEsSyM1AWuaGOq34zbZEwFWpd_PUhO6v-kqmYL-EvihLvzLdQTCacadJBoLlGIlwXiWDEbPGpI7LiUJQAwZqbxXdE=w1440)

Methods like hand tuning and Bayesian Optimisation make changes to the hyperparameters by observing many training runs sequentially, making these methods slow

PBT - like random search - starts by training many neural networks in parallel with random hyperparameters. But instead of the networks training independently, it uses information from the rest of the population to refine the hyperparameters and direct computational resources to models which show promise. This takes its inspiration from genetic algorithms where each member of the population, known as a worker, can exploit information from the remainder of the population. For example, a worker might copy the model parameters from a better performing worker. It can also explore new hyperparameters by changing the current values randomly.
As the training of the population of neural networks progresses, this process of exploiting and exploring is performed periodically, ensuring that all the workers in the population have a good base level of performance and also that new hyperparameters are consistently explored. This means that PBT can quickly exploit good hyperparameters, can dedicate more training time to promising models and, crucially, can adapt the hyperparameter values throughout training, leading to automatic learning of the best configurations.

![Diagram showing the sequential process of Population Based Training, where a model's hyperparameters and parameters are periodically evaluated, with poorly performing models copying parameters from better ones (exploit) and exploring new hyperparameters (explore) over time.](https://lh3.googleusercontent.com/1GRFJPRkeWtdSv5qwjD3GCdaz7f-tOn3OPRlEfy-f6UFQq21JPhntOFFQygaD_SOtj3kPg_nRCRSLX20ILUOeW-SNucc5w-bKCcctIm2n8U3iJwCsA=w1440)

Population Based Training of neural networks starts like random search, but allows workers to exploit the partial results of other workers and explore new hyperparameters as training progresses

Our experiments show that PBT is very effective across a whole host of tasks and domains. For example, we rigorously tested the algorithm on a suite of challenging reinforcement learning problems with state-of-the-art methods on DeepMind Lab, Atari, and StarCraft II. In all cases, PBT stabilised training, quickly found good hyperparameters, and delivered results that were beyond state-of-the-art baselines.

![Five bar charts comparing the performance of standard baselines (grey bars) against Population Based Training (blue segments) across different tasks: DM Lab (UNREAL vs PBT: 0.93 to 1.06), Atari (FuN vs PBT: 1.47 to 1.81), StarCraft II (A3C vs PBT: 0.36 to 0.39), Machine Translation (Transformer BLEU score: 22.30 to 22.65), and GAN (DCGAN Inception score: 6.45 to 6.89). PBT consistently improves performance across all tasks.](https://lh3.googleusercontent.com/EybG_XFyyq3Z_iCavC6IHKnQeRiOPPAwAK2jemU82uqs-aruFYty83jqXcTv9ImhXdy7UOcW7llX1cKC1VDarkdmqP5Eo5rbsopidEWpF3F13N3H4g=w1440)

We have also found PBT to be effective for training Generative Adversarial Network (GAN), which are notoriously difficult to tune. Specifically, we used the PBT framework to maximise the Inception Score - a measure of visual fidelity - resulting in a significant improvement from 6.45 to 6.9.

We have also applied it to one of Google’s state-of-the-art machine translation neural networks, which are usually trained with carefully hand tuned hyperparameter schedules that take months to perfect. With PBT we automatically found hyperparameter schedules that match and even exceed existing performance, but without any tuning and in the same time it normally takes to do a single training run.

![An animated visualization comparing the Population Based Training (PBT) process for GAN population development (left, measured by Inception Score) and FuN population development (right, measured by Cumulative Expected Reward). Both panels show a branching tree of training runs, illustrating how poorly performing models are pruned and replaced by copying (exploit) and mutating (explore) the hyperparameters of better-performing runs over time, leading to overall performance improvement.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/622672bd27482f02e110af3b_PBT205.gif)

The evolution of the population during training of GANs on CIFAR-10 and Feudal Networks (FuN) on Ms Pacman. Pink dots represent initial agents, blue ones the final ones.

We believe this is only the beginning for the technique. At DeepMind, we have also found PBT is particularly useful for training new algorithms and neural network architectures that introduce new hyperparameters. As we continue to refine the process, it offers up the possibility of finding and developing ever more sophisticated and powerful neural network models.

**Notes**

Read the [full paper](https://arxiv.org/abs/1711.09846).

This work was done by Max Jaderberg, Valentin Dalibard, Simon Osindero, Wojciech M. Czarnecki, Jeff Donahue, Ali Razavi, Oriol Vinyals, Tim Green, Iain Dunning, Karen Simonyan, Chrisantha Fernando and Koray Kavukcuoglu.
