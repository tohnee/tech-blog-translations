---
title: "Going beyond average for reinforcement learning"
source: https://deepmind.google/blog/going-beyond-average-for-reinforcement-learning/
site: deepmind
date: 2017-07-24
authors: Marc Gendron-Bellemare, Will Dabney, Rémi Munos
crawled: 2026-09-13
---

Consider the commuter who toils backwards and forwards each day on a train. Most mornings, her train runs on time and she reaches her first meeting relaxed and ready. But she knows that once in awhile the unexpected happens: a mechanical problem, a signal failure, or even just a particularly rainy day. Invariably these hiccups disrupt her pattern, leaving her late and flustered.

Randomness is something we encounter everyday and has a profound effect on how we experience the world. The same is true in reinforcement learning (RL) applications, systems that learn by trial and error and are motivated by rewards. Typically, an RL algorithm predicts the average reward it receives from multiple attempts at a task, and uses this prediction to decide how to act. But random perturbations in the environment can alter its behaviour by changing the exact amount of reward the system receives.

In [a new paper](https://arxiv.org/abs/1707.06887), we show it is possible to model not only the average but also the full variation of this reward, what we call the value distribution. This results in RL systems that are more accurate and faster to train than previous models, and more importantly opens up the possibility of rethinking the whole of reinforcement learning.

Returning to the example of our commuter, let’s consider a journey composed of three segments of 5 minutes each, except that once a week the train breaks down, adding another 15 minutes to the trip. A simple calculation shows that the average commute time is **(3 x 5) + 15 / 5 = 18** minutes.

![An illustrative diagram displaying the potential delays during a train journey between four stations.](https://lh3.googleusercontent.com/7opHvNS3gWnDiSqPD34eC3U4OnsKEudCt4Rplf5EAVw1QOyEM10xxNwkkM8P311Fhnf_6ZtAhijIqt81ofQ99NIJ0RL-j_zqmHe-OZ2iArlF-I7q=w1440)

In reinforcement learning, we use Bellman's equation to predict this average commute time. Specifically, Bellman’s equation relates our current average prediction to the average prediction we make in the immediate future. From the first station, we predict an 18 minutes journey (the average total duration); from the second, we predict a 13 minutes journey (average duration minus the first segment’s length). Finally, assuming the train hasn’t yet broken down, from the third station we predict there are 8 minutes (13 - 5) left to our commute, until finally we arrive at our destination. Bellman’s equation makes each prediction sequentially, and updates these predictions on the basis of new information.

What's a little counterintuitive about Bellman’s equation is that we never actually observe these predicted averages: either the train takes 15 minutes (4 days out of 5), or it takes 30 minutes – never 18! From a purely mathematical standpoint, this isn’t a problem, because decision theory tells us we only need averages to make the best choice. As a result, this issue has been mostly ignored in practice. Yet, there is now plenty of [empirical](https://arxiv.org/abs/1512.04860) [evidence](https://arxiv.org/abs/1509.06461) that predicting averages is a complicated business.

> It’s already evident from our empirical results that the distributional perspective leads to better, more stable reinforcement learning

In [our new paper](https://arxiv.org/abs/1707.06887), we show that there is in fact a variant of Bellman's equation which predicts all possible outcomes, without averaging them. In our example, we maintain two predictions – a distribution – at each station: If the journey goes well, then the times are 15, 10, then 5 minutes, respectively; but if the train breaks down, then the times are 30, 25, and finally 20 minutes.

All of reinforcement learning can be reinterpreted under this new perspective, and its application is already leading to surprising new theoretical results. Predicting the distribution over outcomes also opens up all kinds of algorithmic possibilities, such as:

- **Disentangling the causes of randomness**: once we observe that commute times are bimodal, i.e. take on two possible values, we can act on this information, for example checking for train updates before leaving home;
- **Telling safe and risky choices apart**: when two choices have the same average outcome (e.g., walking or taking the train), [we may favour](http://www.mit.edu/~jnt/Papers/J145-13-mv-MDP.pdf) the one which varies the least (walking)..
- **Natural auxiliary predictions**: predicting a multitude of outcomes, such as the distribution of commute times, has [been shown](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.121.8707&rep=rep1&type=pdf) to [be beneficial](https://deepmind.com/blog/reinforcement-learning-unsupervised-auxiliary-tasks/) for training deep networks faster.

We took our new ideas and implemented them within the [Deep Q-Network agent](https://deepmind.com/research/dqn/), replacing its single average reward output with a distribution with 51 possible values. The only other change was a new learning rule, reflecting the transition from Bellman’s (average) equation to its distributional counterpart. Incredibly, it turns out going from averages to distributions was all we needed to surpass the performance of all other comparable approaches, and by a wide margin. The graph below shows how we get 75% of a trained Deep Q-Network’s performance in 25% of the time, and achieve significantly better human performance:

![A line graph plotting the number of Atari games won against training frames up to 200 million. The purple line labeled "C51 vs. DQN" rises rapidly to outperform DQN in over 50 games. The blue line labeled "C51 vs. HUMAN" rises steadily to surpass human performance in over 30 games. The orange line labeled "DQN vs. HUMAN" plateaus at around 18 games won.](https://lh3.googleusercontent.com/v2iMB2V1VBIb2dlKARw95QlwwwjZAGfgu_xY5snnQxJYkCADWdj3hV9nGVQwzdp8OnBJm2Qt8NDRj-26CI3rM1viq1ZNLwhFJPB33_B-c1NyVhT3lHQ=w1440)

One surprising result is that we observe some randomness in Atari 2600 games, even though Stella, the underlying game emulator, is itself fully predictable. This randomness arises in part because of what’s called partial observability: due to the internal programming of the emulator, our agents playing the game of Pong cannot predict the exact time at which their score increases. Visualising the agent’s prediction over successive frames (graphs below) we see two separate outcomes (low and high), reflecting the possible timings. Although this intrinsic randomness doesn’t directly impact performance, our results highlight the limits of our agents’ understanding.

![An gameplay screenshot of Pong shown alongside five consecutive probability distribution graphs from t=0 to t=4, illustrating a bimodal prediction of high and low returns over time.](https://lh3.googleusercontent.com/JmLdX2dUqp4X6oYfQS0YK6BIcylUjFlGMI8yWODiEi_YZUahZHYXzvM9Jh30e65tyEAHYB1QDlcs3FCTGpEtMbM4NOT0Y8K8cU7Wny2I7-rCGY2O5tw=w1440)

Randomness also occurs because the agent’s own behaviour is uncertain. In Space Invaders, our agent learns to predict the future probability that it might make a mistake and lose the game (zero reward).

![A recording of a game of Space Invaders being played by an AI agent. Next to the animation, a chart records the probability of success against each input. The agent learns from this probability to predict future behaviours that will be more successful.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62265c0345111906f5453238_Beyond20Average20for20RL204.gif)

Just like in our train journey example, it makes sense to keep separate predictions for these vastly different outcomes, rather than aggregate them into an unrealisable average. In fact, we think that our improved results are in great part due to the agent’s ability to model its own randomness.

It’s already evident from our empirical results that the distributional perspective leads to better, more stable reinforcement learning. With the possibility that every reinforcement learning concept could now want a distributional counterpart, it might just be the beginning for this approach.

**Notes**

This work was done by Marc G. Bellemare\*, Will Dabney\*, and Rémi Munos.

Read paper: [A Distributional Perspective on Reinforcement Learning](https://arxiv.org/abs/1707.06887)
