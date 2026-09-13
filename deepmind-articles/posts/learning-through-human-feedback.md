---
title: "Learning through human feedback"
source: https://deepmind.google/blog/learning-through-human-feedback/
site: deepmind
date: 2017-06-12
authors: Jan Leike, Miljan Martic, Shane Legg
crawled: 2026-09-13
---

We believe that Artificial Intelligence will be one of the most important and widely beneficial scientific advances ever made, helping humanity tackle some of its greatest challenges, from climate change to delivering advanced healthcare. But for AI to deliver on this promise, we know that the technology [must be built in a responsible manner](https://ai.googleblog.com/2016/06/bringing-precision-to-ai-safety.html) and that we must consider all potential challenges and risks.

That is why DeepMind co-founded initiatives like the [Partnership on AI to Benefit People and Society](https://www.partnershiponai.org/)and why we have a team dedicated to technical AI Safety. Research in this field needs to be open and collaborative to ensure that best practices are adopted as widely as possible, which is why we are also collaborating with [OpenAI](https://openai.com/) on [research in technical AI Safety](https://openai.com/blog/deep-reinforcement-learning-from-human-preferences/).

One of the central questions in this field is how we allow humans to tell a system what we want it to do and - importantly - what we don’t want it to do. This is increasingly important as the problems we tackle with machine learning grow more complex and are applied in the real world.

The [first results](https://arxiv.org/abs/1706.03741) from our collaboration demonstrate one method to address this, by allowing humans with no technical experience to teach a reinforcement learning (RL) system - an AI that learns by trial and error - a complex goal. This removes the need for the human to specify a goal for the algorithm in advance. This is an important step because getting the goal even a bit wrong could lead to undesirable or even dangerous behaviour. In some cases, as little as 30 minutes of feedback from a non-expert is enough to train our system, including teaching it entirely new complex behaviours, such as how to make a simulated robot do backflips.

![An AI-controlled model performs a backflip.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/622378d1616ef655e7c8590d_unnamed-2_1.gif)

It took around 900 pieces of feedback from a human to teach this algorithm to backflip

The system - described [in our paper Deep Reinforcement Learning from Human Preferences](https://arxiv.org/abs/1706.03741) - departs from classic RL systems by training the agent from a neural network known as the ‘reward predictor’, rather than rewards it collects as it explores an environment.

It consists of three processes running in parallel:

1. A reinforcement learning agent explores and interacts with its environment, such as an Atari game.
2. Periodically, a pair of 1-2 second clips of its behaviour is sent to a human operator, who is asked to select which one best shows steps towards fulfilling the desired goal.
3. The human’s choice is used to train a reward predictor, which in turn trains the agent. Over time, the agent learns to maximise the reward from the predictor and improve its behaviour in line with the human’s preferences.

![A diagram of the reinforcement learning process with human feedback. An RL algorithm interacts with an environment via action and observation (step 1). A human operator provides feedback to a reward predictor (step 2), which then sends a predicted reward back to the RL algorithm (step 3).](https://lh3.googleusercontent.com/KJJQZzwUEjjKAJXIuBFmS5NTJyj0jNy2o2OzIbNPhmKn8vabt_p8zwuXMNukS5PyiIr-mOstZyT1JlK57Kyw1bxjkifDL15XMRm7bFATCVaBPhAIFQ=w1440)

The system separates learning the goal from learning the behaviour to achieve it

This iterative approach to learning means that a human can spot and correct any undesired behaviours, a crucial part of any safety system. The design also does not put an onerous burden on the human operator, who only has to review around 0.1% of the agent’s behaviour to get it to to do what they want. However, this can mean reviewing several hundred to several thousand pairs of clips, something that will need to be reduced to make it applicable to real world problems.

![Side-by-side comparison interface showing two clips of the Atari game Q*bert, labeled "Left" and "Right," with interactive buttons below for a human operator to evaluate which agent's behavior is better, with options "Left is better," "Right is better," "It's a tie," and "Can't tell."](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6223794abf2cca4c6a9dc751_unnamed.gif)

Human operators have to choose between two clips. In this example, for the Atari game Qbert, the right hand clip shows the better - point scoring - behaviour

In the Atari game Enduro, which involves steering a car to overtake a line of others and is very difficult to learn by the trial and error techniques of a traditional RL network, human feedback eventually allowed our system to achieve superhuman results. In other games and simulated robotics tasks, it performed comparably to a standard RL set-up, while in a couple of games like Qbert and Breakout it failed to work at all.

But the ultimate purpose of a system like this is to allow humans to specify a goal for the agent, even if it is not present in the environment. To test this, we taught agents various novel behaviours such as performing a backflip, walking on one leg or learning to driving alongside another car in Enduro, rather than overtake to maximise the game score.

![A recording of the agent playing the video game Enduro.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62237af8d24c681a8e67e81e_unnamed-3.gif)

The normal aim of Enduro is to pass as many cars as possible. But using our system, we can train the agent to pursue a different goal, such as driving alongside other vehicles

Although these tests showed some positive results, others showed its limitations. In particular, our set-up was susceptible to reward hacking - or gaming its reward function - if human feedback was discontinued early in the training. In this scenario, the agent continues to explore its environment, meaning the reward predictor is forced to estimate rewards for situations it has received no feedback on. This can lead it to overpredict the reward, incentivising the agent to learn the wrong - often strange - behaviours. An example can be seen in the video below, where the agent has found that hitting the ball back and forth is a better strategy than winning or losing a point.

![A recording of the agent playing the video game Pong against itself.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62237b1eede3d70a945ba522_unnamed-4.gif)

The agent has hacked its reward function and has decided that hitting the ball back and forth is better than winning or losing a point

Understanding flaws like these is crucial to ensure we avoid failures and build AI systems that behave as intended.

There is still more work to be done to test and enhance this system, but already it shows a number of critical first steps in producing systems that can be taught by non-expert users, are economical with the amount of feedback they need, and can be scaled to a variety of problems.

Other areas of exploration could include reducing the amount of human feedback needed or giving humans the ability to give feedback through a natural language interface. This would mark a step-change in creating a system that can easily learn from the complexity of human behaviour, and a crucial step towards creating AI that works with and for all of humanity.

**Notes**

This research was done as part of an ongoing collaboration between Jan Leike, Miljan Martic, and Shane Legg at DeepMind and Paul Christiano, Dario Amodei, and Tom Brown at OpenAI.

Read the [full paper](https://arxiv.org/abs/1706.03741)

Read [the blog from OpenAI](https://openai.com/blog/deep-reinforcement-learning-from-human-preferences/)

Read ‘[Concrete Problems in AI Safety](https://arxiv.org/abs/1606.06565)’ for more background on the topic
