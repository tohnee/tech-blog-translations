---
title: "How evolutionary selection can train more capable self-driving cars"
source: https://deepmind.google/blog/how-evolutionary-selection-can-train-more-capable-self-driving-cars/
site: deepmind
date: 2019-07-25
authors: Yu-hsin Chen
crawled: 2026-09-13
---

Waymo’s self-driving vehicles employ neural networks to perform many driving tasks, from detecting objects and predicting how others will behave, to planning a car's next moves.

Training an individual neural net has traditionally required weeks of fine-tuning and experimentation, as well as enormous amounts of computational power. Now, Waymo, in a research collaboration with DeepMind, has taken inspiration from Darwin’s insights into evolution to make this training more effective and efficient.

## Training machine learning models from novice to expert

![](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62272b19b25343f06150fa63_Waymo2001.gif)

At a high level, neural nets learn through trial and error. A network is presented with a task, and is “graded” on whether it performs the task correctly or not. The network learns by continually attempting these tasks and adjusting itself based on its grades, such that it becomes more likely to perform correctly in the future.

A network’s performance depends heavily on its training regimen. For example, a researcher can tweak how much a network adjusts itself after each task–referred to as its learning rate. The higher the learning rate, the more dramatic the adjustments. The goal is to find a learning rate high enough that the network gets better after each iteration, but not so high that the network's performance fluctuates wildly.

Finding the best training regimen (or “hyperparameter schedule”) is commonly achieved through an engineer’s experience and intuition, or through extensive searching. In random search, researchers apply many random hyperparameter schedules over multiple types of hyperparameters in order to train different networks independently and in parallel–after which it’s possible to settle on the best performing model. This [blog post](https://medium.com/waymo/automl-automating-the-design-of-machine-learning-models-for-autonomous-driving-141a5583ec2a) covers how Waymo engineers apply reinforcement learning to the search for better neural net architectures.

Because training numerous models in parallel is computationally expensive, researchers typically hand-tune random search by monitoring networks while they’re training, periodically culling the weakest performers and freeing resources to train new networks from scratch with new random hyperparameters. This type of manual tuning produces better results faster, but it’s labor intensive.

![](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62272b3e7a1ae0a1ba6bb46d_Waymo2002.gif)

## Training with evolutionary competition

To make this process more efficient, researchers at DeepMind devised a way to automatically determine good hyperparameter schedules based on evolutionary competition (called “Population Based Training” or PBT), which combines the advantages of [hand-tuning and random search](https://deepmind.com/blog/population-based-training-neural-networks/).

Like random search, PBT also starts with multiple networks initiated with random hyperparameters. Networks are evaluated periodically and compete with each other for “survival” in an evolutionary fashion. If a member of the population is underperforming, it’s replaced with the “progeny” of a better performing member. The progeny is a copy of the better performing member, with slightly mutated hyperparameters. PBT doesn’t require us to restart training from scratch, because each progeny inherits the full state of its parent network, and hyperparameters are updated actively throughout training, not at the end of training. Compared to random search, PBT spends more of its resources training with good hyperparameter values.

![An animated GIF depicting Population Based Training (PBT) for self-driving neural networks. Rows of icons representing different driving tasks (such as detecting pedestrians, bicycles, traffic lights, and cones) continually update, with lower-performing models flashing red and being replaced by higher-performing, mutated "progeny" models.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/622730f075887b5cfa3655e0_Waymo2003.gif)

How Population Based Training works: Inspired by evolutionary principles, Population Based Training (PBT) is a method first developed at DeepMind that helps discover effective and efficient training regimes for neural nets. PBT works by launching many hyperparameter searches at one time, with periodic “competitions” to compare models’ performances. Losing models are removed from the training pool, and training continues using only winning models, updated with slightly mutated hyperparameters. PBT is more efficient than traditional methods employed by researchers, such as random search, because each new neural net inherits the full state of its parent network and doesn’t need to restart training from the beginning. Also, hyperparameters aren’t static, but actively updated throughout training. Compared to random search, PBT spends more of its resources training with successful hyperparameter values.

## Evolution at Waymo

The first experiments that DeepMind and Waymo collaborated on involved training a network that generates boxes around pedestrians, bicyclists, and motorcyclists detected by our sensors–named a “region proposal network.” The aim was to investigate whether PBT could improve a neural net's ability to detect pedestrians along two measures: recall (the fraction of pedestrians identified by the neural net over total number of pedestrians in the scene) and precision (the fraction of detected pedestrians that are actually pedestrians, and not spurious “false positives”). Waymo’s vehicles detect these road users using multiple neural nets and other methods, but the goal of this experiment was to train this single neural net to maintain recall over 99%, while reducing false positives using population-based training.

We learned a lot from this experiment. Firstly, we discovered that we needed to create a realistic and robust evaluation for the networks so that we’d know if a neural net would truly perform better when deployed across a variety of situations in the real world. This evaluation formed the basis of the competition that PBT employs to pick one winning neural net over another. To ensure neural nets perform well generally, and don’t simply memorise answers to examples they've seen during training, our PBT competition evaluation uses a set of examples (the "validation set") that is different from those used in training (the "training set.") To verify final performance, we also use a third set of examples (the "evaluation set") that the neural nets have never seen in training or competition.

Secondly, we learned that we needed fast evaluation to support frequent evolutionary competition. Researchers seldom evaluate their models during training, and when they do, the evaluation is done infrequently. PBT required models be evaluated every 15 minutes. To achieve this, we took advantage of Google’s data centres to parallelise the evaluation across hundreds of distributed machines.

## The power of diversity in evolutionary competition

During these experiments, we noticed that one of PBT’s strengths–allocating more resources to the progeny of better performing networks–can also be a weakness, because PBT optimises for the present and fails to consider long-term outcomes. This can be a problem because it disadvantages late-bloomers, so neural nets with hyperparameters that perform better over the long term don’t have the chance to mature and succeed. One way to combat this is to increase population diversity, which can be achieved by simply training a larger population. If the population is large enough, there is a greater chance for networks with late-blooming hyperparameters to survive and catch up in later generations.

In these experiments, we were able to increase diversity by creating sub-populations called “niches,” where neural nets were only allowed to compete within their own sub-groups–similar to how species evolve when isolated on islands. We also tried to directly reward diversity through a technique called “fitness sharing,” where we measure the difference between members of the population and give more unique neural nets an edge in the competition. Greater diversity allows PBT to explore a larger hyperparameter space.

## Results

PBT enabled dramatic improvements in model performance. For the experiment above, our PBT models were able to achieve higher precision by reducing false positives by 24% compared to its hand-tuned equivalent, while maintaining a high recall rate. A chief advantage of evolutionary methods such as PBT is that they can optimise arbitrarily complex metrics. Traditionally, neural nets can only be trained using simple and smooth loss functions, which act as a proxy for what we really care about. PBT enabled us to go beyond the update rule used for training neural nets, and towards the more complex metrics optimising for features we care about, such as maximising precision under high recall rates.

PBT also saves time and resources. The hyperparameter schedule discovered with PBT-trained nets outperformed Waymo’s previous net with half the training time and resources. Overall, PBT uses half the computational resources used by random parallel search to efficiently discover better hyperparameter schedules. It also saves time for researchers–by incorporating PBT directly into Waymo’s technical infrastructure, researchers from across the company can apply this method with the click of a button, and spend less time tuning their learning rates. Since the completion of these experiments, PBT has been applied to many different Waymo models, and holds a lot of promise for helping to create more capable vehicles for the road.

**Notes**

Contributors: The work described here was a research collaboration between Yu-hsin Chen and Matthieu Devin of Waymo, and Ali Razavi, Ang Li, Sibon Li, Ola Spyra, Pramod Gupta and Oriol Vinyals of DeepMind. Advisors to the project include Max Jaderberg, Valentin Dalibard, Meire Fortunato and Jackson Broshear from DeepMind.
