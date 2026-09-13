---
title: "The hippocampus as a predictive map"
source: https://deepmind.google/blog/the-hippocampus-as-a-predictive-map/
site: deepmind
date: 2017-10-02
authors: Kimberly Stachenfeld, Matt Botvinick, Samuel Gershman
crawled: 2026-09-13
---

Think about how you choose a route to work, where to move house, or even which move to make in a game like Go. All of these scenarios require you to estimate the likely future reward of your decision. This is tricky because the number of possible scenarios explodes as one peers farther and farther into the future. Understanding how we do this is a major research question in neuroscience, while building systems that can effectively predict rewards is a major focus in AI research.

In our new paper, [in Nature Neuroscience](https://www.nature.com/articles/nn.4650), we apply a neuroscience lens to a longstanding mathematical theory from machine learning to provide new insights into the nature of learning and memory. Specifically, we propose that the area of the brain known as the hippocampus offers a unique solution to this problem by compactly summarising future events using what we call a “predictive map.”

The hippocampus has traditionally been thought to only represent an animal’s current state, particularly in spatial tasks, such as navigating a maze. This view gained significant traction with the [discovery of “place cells” in the rodent hippocampus](http://www.cognitivemap.net/), which fire selectively when the animal is in specific locations. While this theory accounts for many neurophysiological findings, it does not fully explain why the hippocampus is also involved in other functions, such as memory, relational reasoning, and decision making.

![Two panels illustrating the firing activity of a hippocampal place cell in a 1-meter square arena. The left panel shows a colored heat map of firing frequency with a central peak reaching 8 Hz in red. The right panel shows the animal's trajectory in black with red dots marking the locations where the cell fired, clustered heavily in the center.](https://lh3.googleusercontent.com/but-B69WWVhome4KSxiun4rJipXyyDcgIjuqlHYMvtuHoYXno2dFkVJFUBm7NtRNTs1oMvFK0fU-m2vol6aR170jnZk21sLFy3zwgK8oXaMx1wbloA=w1440)

The activity of a single place cell recorded from the hippocampus of a rat as it explores a square room. On the left, the average activity or “firing rate” of the neuron is shown at each location in space. On the right, the black lines denote the places the rat visited, and the red dots mark the animal’s position each time a cell become active, or “fired.” As is typical of a place cell, this cell tends to fire only when near its preferred location in the upper right corner of the room. Credit: Royal Society (2013)

Our new theory thinks about navigation as part of the more general problem of computing plans that maximise future reward. Our insights were derived from reinforcement learning, the subdiscipline of AI research that focuses on systems that learn by trial and error. The key computational idea we drew on is that to estimate future reward, an agent must first estimate how much immediate reward it expects to receive in each state, and then weight this expected reward by how often it expects to visit that state in the future. By summing up this weighted reward across all possible states, the agent obtains an estimate of future reward.

Similarly, we argue that the hippocampus represents every situation - or state - in terms of the future states which it predicts. For example, if you are leaving work (your current state) your hippocampus might represent this by predicting that you will likely soon be on your commute, picking up your kids from school or, more distantly, at home. By representing each current state in terms of its anticipated successor states, the hippocampus conveys a compact summary of future events, known formally as the “[successor representation](https://www.google.com/url?q=http://www.gatsby.ucl.ac.uk/~dayan/papers/d93b.pdf&sa=D&ust=1506953602671000&usg=AFQjCNE8xj7DAxuDaaDRy8IZL07XlS6_4Q)”. We suggest that this specific form of predictive map allows the brain to adapt rapidly in environments with changing rewards, but without having to run expensive simulations of the future.

![A motion-blurred, overhead view of hands playing a piano, symbolizing the rapid sequence of actions and future states involved in planning and decision-making.](https://lh3.googleusercontent.com/2lgbgWfMimAl3CF09tfLzHFO_S5qYzgufGjo9h4bo68tL4aXFZnlnFXmguPkjoUIrEx_m_gzAqP2zNSJXzQqpPgQprjU1hTTC_gZNbS8-BglX5Ks=w1440)

A pianist’s successor representation of state would simultaneously represent the chords currently being played as well as statistics about which notes are upcoming. Credit: Shutterstock

This approach combines the strengths of two algorithms that are already well known in reinforcement learning and are also believed to exist in humans and rodents. “Model-based” algorithms learn models of the environment that can then be simulated to produce estimates of future reward, while “model-free” algorithms learn future reward estimates directly from experience in the environment. Model-based algorithms are flexible but computationally expensive, while model-free algorithms are computationally cheap but inflexible.

The algorithm that inspired our theory combines some of the flexibility of model-based algorithms with the efficiency of model-free algorithms. Because the calculation is a simple weighted sum, it is computationally efficient, much like a model-free algorithm. At the same time, by separating reward expectations and state expectations (the predictive map), it can rapidly adapt to changes in reward by simply updating the reward expectations while leaving the state expectations intact ([see our recent paper for further detail](https://www.nature.com/articles/s41562-017-0180-8)).

In future work, we plan to test the theory further. Since the predictive map theory can be translated into a [neural network architecture](https://arxiv.org/abs/1606.02396), we want to explore the extent to which this learning strategy can promote flexible, rapid planning in silico.

More generally, a major future task will be to look at how the brain integrates different types of learning. While we posed this model as an alternative to model-based and model-free learning in the brain, [a more realistic view](http://gershmanlab.webfactional.com/pubs/KoolCushmanGershman_CompCoop.pdf) is that many types of learning are simultaneously coordinated by the brain during learning and planning. Understanding how these learning algorithms are combined is an important step towards understanding human and animal brains, and could provide key insights for designing equally complex, multifaceted AI.

**Notes**

Read paper: [The hippocampus as a predictive map](https://www.nature.com/articles/nn.4650)
