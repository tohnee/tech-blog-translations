---
title: "Is Curiosity All You Need? On the Utility of Emergent Behaviours from Curious Exploration"
source: https://deepmind.google/blog/is-curiosity-all-you-need-on-the-utility-of-emergent-behaviours-from-curious-exploration/
site: deepmind
date: 2021-09-17
authors: Oliver Groth, Markus Wulfmeier, Giulia Vezzani, Vibhavari Dasagi, Tim Hertweck, Roland Hafner, Nicolas Heess, Martin Riedmiller
crawled: 2026-09-13
---

During purely curious exploration, the JACO arm discovers how to pick up cubes, moves them around the workspace and even explores whether they can be balanced on their edges.

Curious exploration enables OP3 to walk upright, balance on one foot, sit down and even catch itself safely when leaping backwards - all without a specific target task to optimise for.

Intrinsic motivation [1, 2] can be a powerful concept to endow an agent with a mechanism to continuously explore its environment in the absence of task information. One common way to implement intrinsic motivation is via curiosity learning [3, 4]. With this method, a predictive model about the environment's response to an agent's actions is trained alongside the agent's policy. This model can also be called a world model. When an action is taken, the world model makes a prediction about the agent's next observation. This prediction is then compared to the true observation made by the agent. Crucially, the reward given to the agent for taking this action is scaled by the error it made when predicting the next observation. This way, the agent is rewarded for taking actions whose outcomes are not yet well predictable. Simultaneously, the world model is updated to better predict the outcome of said action.

This mechanism has been applied successfully in on-policy settings, e.g. to beat 2D computer games in an unsupervised way [4] or to train a general policy which is easily adaptable to concrete downstream tasks [5]. However, we believe that the true strength of curiosity learning lies in the diverse behaviour which emerges during the curious exploration process: As the curiosity objective changes, so does the resulting behaviour of the agent thereby discovering many complex policies which could be utilised later on, if they were retained and not overwritten.

[In this paper](https://arxiv.org/abs/2109.08603), we make two contributions to study curiosity learning and harness its emergent behaviour: First, we introduce SelMo, an off-policy realisation of a self-motivated, curiosity-based method for exploration. We show that using SelMo, meaningful and diverse behaviour emerges solely based on the optimisation of the curiosity objective in simulated manipulation and locomotion domains. Second, we propose to extend the focus in the application of curiosity learning towards the identification and retention of emerging intermediate behaviours. We support this conjecture with an experiment which reloads self-discovered behaviours as pretrained, auxiliary skills in a hierarchical reinforcement learning setup.

![Diagram illustrating the SelMo off-policy curiosity-learning loop. Raw trajectories from an actor interacting with the environment are stored in a replay buffer to train a dynamics world model. These trajectories are then labeled with curiosity rewards based on prediction error and sent to a second replay buffer to perform off-policy reinforcement learning, improving the actor policy.](https://lh3.googleusercontent.com/AQyewboCUZANdrGw8av-m8_t383c5UnlE-qxKJ7vtDmEI_ay4ecapvG-kH_-u9pbzNz5Srw7suXoL-fJ1FI-qcOYNLDj-iZsyjUSvDjJapahvJcRFw=w1440)

The control flow of the SelMo method: The agent (actor) collects trajectories in the environment using its current policy and stores them in the model replay buffer on the left. The connected world model samples uniformly that buffer and updates its parameters for forward prediction using stochastic gradient descent (SGD). The sampled trajectories are assigned curiosity rewards scaled by their respective prediction error under the current world model. The labeled trajectories are then passed on to the policy replay buffer on the right. Maximum a posteriori policy optimisation (MPO) [6] is used to fit Q-function and policy based on samples from the policy replay. The resulting, updated policy is then synced back into the actor.

We run SelMo in two simulated continuous control robotic domains: On a 6-DoF JACO arm with a three-fingered gripper and on a 20-DoF humanoid robot, the OP3. The respective platforms present challenging learning environments for object manipulation and locomotion, respectively. While only optimising for curiosity, we observe that complex human-interpretable behaviour emerges over the course of the training runs. For instance, JACO learns to pick up and move cubes without any supervision or the OP3 learns to balance on a single foot or sit down safely without falling over.

![A timeline showing the progression of behaviors discovered by a robotic arm during curious exploration over 100,000 episodes: pushing objects up slanted walls, lifting cubes, moving cubes longer distances, balancing cubes on edges, and picking up two cubes at once.](https://lh3.googleusercontent.com/vwaSmf-bz-LN6MtrUVeGFGaXZvNou8z9mhcfZ_T22CcRu4slQ3T1eCVBnI0nZJlu51hOHIrrm7y53KscLBAlZpD5rpUAkHQAYupjYSzv1jSo3yfzp8Q=w1440)

![A timeline showing the progression of behaviors discovered by a humanoid robot (OP3) during curious exploration over 100,000 episodes: raising arms, balancing on a single foot, sitting down, catching itself after leaping backwards, and stretching with bent knees.](https://lh3.googleusercontent.com/_f_eFZZmrG4nPN-ep2_6yVrEylKQXvQe0sNtlaif8b6FvokP8X1XCkSD2zwsUB6JCCx0EkO2VmgBZBCl64Epvg3_kKmoMJjrpOEN8iCIu9tlPrkLIGY=w1440)

Example training timelines for JACO and the OP3. While optimising for the curiosity objective, complex, meaningful behaviour emerges in both manipulation and locomotion settings. The full videos can be found at the top of this page.

However, the impressive behaviours observed during curious exploration have one crucial drawback: They are not persistent as they keep changing with the curiosity reward function. As the agent keeps repeating a certain behaviour, e.g. JACO lifting the red cube, the curiosity rewards accumulated by this policy are diminishing. Consequently, this leads to the learning of a modified policy which acquires higher curiosity rewards again, e.g. moving the cube outside the workspace or even attending to the other cube. But this new behaviour overwrites the old one. However, we believe that retaining the emergent behaviours from curious exploration equips the agent with a valuable skill set to learn new tasks more quickly. In order to investigate this conjecture, we set up an experiment to probe the utility of the self-discovered skills.

![A line graph titled "Accumulated lift_red reward over time" comparing four reinforcement learning setups (RHPO - early, RHPO - mid, RHPO - late, and SAC-X) over 60,000 training episodes, showing that using intermediate, mid-exploration auxiliary skills (RHPO - mid) leads to the fastest learning progress.](https://lh3.googleusercontent.com/5SNjJb2rU-f9Ut9YPCgMkqx-_nWUbqOrXGa1jwYQjj9oXUK8YxT8Uo4GUPQMLDbY7u7yrty3YkzFKGE-4ANbBwfVEJV9cd9fwRoa1mPvdRhoEf-yCA=w1440)

We treat randomly sampled snapshots from different phases of the curious exploration as auxiliary skills in a modular learning framework [7] and measure how quickly a new target skill can be learned by using those auxiliaries. In the case of the JACO arm, we set the target task to be "lift the red cube" and use five randomly sampled self-discovered behaviours as auxiliaries. We compare the learning of this downstream task to an SAC-X baseline [8] which uses a curriculum of reward functions to reward reaching and moving the red cube which ultimately facilitates to learn lifting as well. We find that even this simple setup for skill-reuse already speeds up the learning progress of the downstream task commensurate with a hand designed reward curriculum. The results suggest that the automatic identification and retention of useful emerging behaviour from curious exploration is a fruitful avenue of future investigation in unsupervised reinforcement learning.

**References**

[1] Oudeyer, Pierre-Yves, Frdric Kaplan, and Verena V. Hafner. "Intrinsic motivation systems for autonomous mental development." IEEE transactions on evolutionary computation 11.2 (2007): 265-286.

[2] Schmidhuber, Jürgen. "Formal theory of creativity, fun, and intrinsic motivation (1990–2010)." IEEE Transactions on Autonomous Mental Development 2.3 (2010): 230-247.

[3] Schmidhuber, Jürgen. "A possibility for implementing curiosity and boredom in model-building neural controllers." Proc. of the international conference on simulation of adaptive behavior: From animals to animats. 1991.

[4] Pathak, Deepak, et al. "Curiosity-driven exploration by self-supervised prediction." International conference on machine learning. PMLR, 2017.

[5] Sekar, Ramanan, et al. "Planning to explore via self-supervised world models." International Conference on Machine Learning. PMLR, 2020.

[6] Abdolmaleki, Abbas, et al. "Maximum a posteriori policy optimisation." arXiv preprint arXiv:1806.06920 (2018).

[7] Wulfmeier, Markus, et al. "Compositional transfer in hierarchical reinforcement learning." arXiv preprint arXiv:1906.11228 (2019).

[8] Riedmiller, Martin, et al. "Learning by playing solving sparse reward tasks from scratch." International Conference on Machine Learning. PMLR, 2018.

[9] Riedmiller, Martin, et al. "Collect & Infer" arXiv preprint arXiv:2108.10273 (2021).
