---
title: "Decoupled Neural Interfaces Using Synthetic Gradients"
source: https://deepmind.google/blog/decoupled-neural-interfaces-using-synthetic-gradients/
site: deepmind
date: 2016-08-29
authors: Max Jaderberg
crawled: 2026-09-13
---

This post introduces some of our latest research in progressing the capabilities and training procedures of neural networks called [Decoupled Neural Interfaces using Synthetic Gradients](https://arxiv.org/abs/1608.05343). This work gives us a way to allow neural networks to communicate, to learn to send messages between themselves, in a decoupled, scalable manner paving the way for multiple neural networks to communicate with each other or improving the long term temporal dependency of recurrent networks. This is achieved by using a model to approximate error gradients, rather than by computing error gradients explicitly with backpropagation. The rest of this post assumes some familiarity with neural networks and how to train them. If you’re new to this area we highly recommend [Nando de Freitas lecture series on Youtube](https://www.youtube.com/watch?v=PlhFWT7vAEw) on deep learning and neural networks.

## Neural networks and the problem of locking

If you consider any layer or module in a neural network, it can only be updated once all the subsequent modules of the network have been executed, and gradients have been backpropagated to it. For example look at this simple feed-forward network:

![Diagram of a simple feed-forward neural network with Layer 1, Layer 2, and Layer 3. Black arrows show the forward propagation of activations from the input to the loss, while green arrows show the backward propagation of error gradients back through every layer.](https://lh3.googleusercontent.com/gKMZKitakIj90Cl_p9pwClgZGr1TXsfkhcnjszz7v9SHLBP889DLNZ91Ao8sv5aI32CsPD5faULJgNBdEPRSKRO0gHEccS7qIwpsrqJwH1h96fmGKw=w1440)

Here, after Layer 1 has processed the input, it can only be updated after the output activations (black lines) have been propagated through the rest of the network, generated a loss, and the error gradients (green lines) backpropagated through every layer until Layer 1 is reached. This sequence of operations means that Layer 1 has to wait for the forwards and backwards computation of Layer 2 and Layer 3 before it can update. Layer 1 is locked, coupled, to the rest of the network.

Why is this a problem? Clearly for a simple feed-forward network as depicted we don’t need to worry about this issue. But consider a complex system of multiple networks, acting in multiple environments at asynchronous and irregular timescales.

Or a big distributed network spread over multiple machines. Sometimes requiring all modules in a network to wait for all other modules to execute and backpropagate gradients is overly time consuming or even intractable. If we decouple the interfaces - the connections - between modules, every module can be updated independently, and is not locked to the rest of the network.

So, how can one decouple neural interfaces - that is decouple the connections between network modules - and still allow the modules to learn to interact? In this paper, we remove the reliance on backpropagation to get error gradients, and instead learn a parametric model which predicts what the gradients will be based upon only local information. We call these predicted gradients synthetic gradients.

![Diagram of a synthetic gradient model represented by a pink and blue diamond. A dotted arrow from the bottom labeled "Activations" points into the diamond, and a blue arrow points up from the diamond labeled "Predicted gradient of the loss with respect to the input activations" beneath the header "Synthetic Gradient".](https://lh3.googleusercontent.com/7SXqEPfXP2m7h9v_yQNxU9tgkCPrpsRw8a6jk_MOLqvQU7nwiwJyRMPV59h7t4xiws91jZ7R2s7tjraro2I09yKv4wsnDOLvKM-7r4_T2h8jtDogSlE=w1440)

The synthetic gradient model takes in the activations from a module and produces what it predicts will be the error gradients - the gradient of the loss of the network with respect to the activations.

Going back to our simple feed-forward network example, if we have a synthetic gradient model we can do the following:

![Diagram of a feed-forward network with Layer 1, Layer 2, and Layer 3. Activations from the input pass to Layer 1, which has turned orange to indicate an update. A dotted black arrow branches from Layer 1 toward Layer 2 and a pink and blue diamond representing a synthetic gradient model. A blue arrow representing the synthetic gradient points from this diamond back to Layer 1 to update it before Layer 2 and Layer 3 have executed.](https://lh3.googleusercontent.com/4AODyPgWTg6IlgFMOPkIYTd5MhwOZKDCtCbW2W835YurHvjK7F2jJqnnDh9mEdUmVt6gui6EET2w46n7c9ed2JiXX7jbvdef-tKrrlijxT809NKY=w1440)

... and use the synthetic gradients (blue) to update Layer 1 before the rest of the network has even been executed.

The synthetic gradient model itself is trained to regress target gradients - these target gradients could be the true gradients backpropagated from the loss or other synthetic gradients which have been backpropagated from a further downstream synthetic gradient model.

![Diagram of a feed-forward network with Layer 1, Layer 2, and Layer 3. Input is passed to Layer 1, which has already been updated. Dotted black arrows branch from Layer 2 toward Layer 3 and a synthetic gradient model represented by a pink and blue diamond. A blue arrow representing the synthetic gradient points from this diamond back to Layer 2. Simultaneously, a green arrow representing the true gradient points backwards from Layer 2, compared against a blue dot representing the synthetic gradient, and is backpropagated to a second synthetic gradient model to update it.](https://lh3.googleusercontent.com/O8zXOyLBjsgMbL-EYBBAkWBc6eK-H_BrcwYjJzn7sjYkrfkjeBMmbvYwBhnIj4UJTkDKePVOxoGsOlEwYsT_eGXXcRDxC7FtRaW3XJXRY7prVMd87Q=w1440)

This mechanism is generic for a connection between any two modules, not just in a feed-forward network. The play-by-play working of this mechanism is shown below, where the change of colour of a module indicates an update to the weights of that module.

![Animated diagram illustrating the play-by-play execution of Decoupled Neural Interfaces (DNI) between two recurrent neural network cores, where synthetic gradients (represented by a diamond) are used to update preceding modules asynchronously.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/622277b1a1bf935c82935454_Decoupled20Neural20Interfaces20Using20Synthetic20.gif)

Using decoupled neural interfaces (DNI) therefore removes the locking of preceding modules to subsequent modules in a network. In experiments from the paper, we show we can train convolutional neural networks for [CIFAR-10](https://www.cs.toronto.edu/~kriz/cifar.html) image classification where every layer is decoupled using synthetic gradients to the same accuracy as using backpropagation. It’s important to recognise that DNI doesn’t magically allow networks to train without true gradient information. The true gradient information does percolate backwards through the network, but just slower and over many training iterations, through the losses of the synthetic gradient models. The synthetic gradient models approximate and smooth over the absence of true gradients.

A legitimate question at this point would be to ask how much computational complexity do these synthetic gradient models add - perhaps you would need a synthetic gradient model architecture that is as complex as the network itself. Quite surprisingly, the synthetic gradient models can be very simple. For feed-forward nets, we actually found out that even a single linear layer works well as a synthetic gradient model. Consequently it is both very easy to train and so produces synthetic gradients rapidly.

DNI can be applied to any generic neural network architecture, not just feed-forward networks. An interesting application is to recurrent neural networks (RNNs). An RNN has a recurrent core which is unrolled - repeatedly applied - to process sequential data. Ideally to train an RNN we would unroll the core over the whole sequence (which could be infinitely long), and use backpropagation through time (BPTT) to propagate error gradients backwards through the graph.

![Illustrative visualisation of a theoretical recurrent neural network processing sequential data.](https://lh3.googleusercontent.com/176LUr08t3brnefNEfe2y8AGSxueJzDMR9fD5hXMygWilzynofdFJ2Gu05Jq6fbQXUv_n2B3DWM4FOZ5n4gIW4jerr7zZ9fODnwAIDO2BuXEk1adwQE=w1440)

However in practice, we can only afford to unroll for a limited number of steps due to memory constraints and the need to actually compute an update to our core model frequently. This is called truncated backpropagation through time, and shown below for a truncation of three steps:

![Illustrative visualisation of a recurrent neural network processing sequential data. Every few steps, it does not backpropogate, due to memory constraints.](https://lh3.googleusercontent.com/m6Y_UtdxCXLQoISfhBrLA7zSVmQAZvuuF0RhEXmGTU6jzDwKdK9VVE47UwAmkVZ3SnRi6N291469Ji_RoQ92qdEQsSiWBU087ZvA6YX1SaL6P558-70=w1440)

The change in colour of the core illustrates an update to the core, that the weights have been updated. In this example, truncated BPTT seems to address some issues with training - we can now update our core weights every three steps and only need three cores in memory. However, the fact that there is no backpropagation of error gradients over more than three steps means that the update to the core will not be directly influenced by errors made more than two steps in the future. This limits the temporal dependency that the RNN can learn to model.

What if instead of doing no backpropagation between the boundary of BPTT we used DNI and produce synthetic gradients, which model what the error gradients of the future will be? We can incorporate a synthetic gradient model into the core so that at every time step, the RNN core produces not only the output but also the synthetic gradients. In this case, the synthetic gradients would be the predicted gradients of the all future losses with respect to the hidden state activation of the previous timestep. The synthetic gradients are only used at the boundaries of truncated BPTT where we would have had no gradients before.

![Diagram of a recurrent neural network using Decoupled Neural Interfaces, where synthetic gradients are generated at the boundaries of truncated backpropagation through time to enable efficient, long-term temporal dependency training.](https://lh3.googleusercontent.com/GXOXL6nSDB5Avf7Lozqg82VAtOHHpFyKewwxUwxPavL1pjZZisFY8ggUD2VQmfIHA7oextLHMDbo6lC6vqf6iDSLyJGJU8cz55RJb6HM4m7vbgrj=w1440)

This can be performed during training very efficiently - it merely requires us to keep an extra core in memory as illustrated below. Here a green dotted border indicates just computing gradients with respect to the input state, while a solid green border additionally computes gradients with respect to the core’s parameters.

By using DNI and synthetic gradients with an RNN, we are approximating doing backpropagation across an infinitely unrolled RNN. In practice, this results in RNNs which can model longer temporal dependencies. Here’s an example result showing this from the paper.

Penn Treebank test error during training (lower is better):

![A line graph plotting Penn Treebank test error, measured in BPC (bits-per-character), against Data Time during training. It compares standard truncated backpropagation models unrolled for 8, 20, and 40 steps (represented by dotted blue, red, and grey curves, respectively) with a DNI model unrolled for 8 steps (solid blue curve). The DNI T=8.0 model achieves a lower test error (1.34 BPC) significantly faster than the other configurations.](https://lh3.googleusercontent.com/kVnUvieA74S1cPmlcEnVIOQo-Zj4rvdy_rwGZdZTrBwUPqPHXueM4FjpQP-UDQazL2zv9a2KmgLEwCnUlIe-kfrZ-ki4zqGqkQVrON12Hreuafxf-Q=w1440)

This graph shows the application of an RNN trained on next character prediction on Penn Treebank, a language modelling problem. On the y-axis the bits-per-character (BPC) is given, where smaller is better. The x-axis is the number of characters seen by the model as training progresses. The dotted blue, red and grey lines are RNNs trained with truncated BPTT, unrolled for 8 steps, 20 steps and 40 steps - the higher the number of steps the RNN is unrolled before performing backpropagation through time, the better the model is, but the slower it trains. When DNI is used on the RNN unrolled 8 steps (solid blue line) the RNN is able to capture the long term dependency of the 40-step model, but is trained twice as fast (both in terms of data and wall clock time on a regular desktop machine with a single GPU).

To reiterate, adding synthetic gradient models allows us to decouple the updates between two parts of a network. DNI can also be applied on hierarchical RNN models - system of two (or more) RNNs running at different timescales. As we show in the [paper](https://arxiv.org/abs/1608.05343), DNI significantly improves the training speed of these models by enabling the update rate of higher level modules.

Hopefully from the explanations in this post, and a brief look at some of the experiments we report in the [paper](https://arxiv.org/abs/1608.05343) it is evident that it is possible to create decoupled neural interfaces. This is done by creating a synthetic gradient model which takes in local information and predicts what the error gradient will be. At a high level, this can be thought of as a communication protocol between two modules. One module sends a message (current activations), another one receives the message, and evaluates it using a model of utility (the synthetic gradient model). The model of utility allows the receiver to provide instant feedback (synthetic gradient) to the sender, rather than having to wait for the evaluation of the true utility of the message (via backpropagation). This framework can also be thought about from an error critic point of view [[Werbos](http://www.werbos.com/HICChapter13.pdf)] and is similar in flavour to using a critic in reinforcement learning [[Baxter](http://www.cis.upenn.edu/~mkearns/finread/BaxterWeaverBartlett.pdf)].

These decoupled neural interfaces allow distributed training of networks, enhance the temporal dependency learnt with RNNs, and speed up hierarchical RNN systems. We’re excited to explore what the future holds for DNI, as we think this is going to be an important basis for opening up more modular, decoupled, and asynchronous model architectures. Finally, there are lots more details, tricks, and full experiments which you can find in the paper [here](https://arxiv.org/abs/1608.05343).

Neural networks are the workhorse of many of the algorithms developed at DeepMind. For example, [AlphaGo](https://deepmind.com/research/case-studies/alphago-the-story-so-far) uses convolutional neural networks to evaluate board positions in the game of Go and [DQN](https://deepmind.com/research/publications/human-level-control-through-deep-reinforcement-learning/)and [Deep Reinforcement Learning algorithms](https://deepmind.com/blog/article/deep-reinforcement-learning) use neural networks to choose actions to play at super-human level on video games.
