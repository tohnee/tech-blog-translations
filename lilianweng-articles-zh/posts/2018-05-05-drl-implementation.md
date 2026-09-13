---
title: "用 Tensorflow + OpenAI Gym 实现深度强化学习模型"
title_en: "Implementing Deep Reinforcement Learning Models with Tensorflow + OpenAI Gym"
source: https://lilianweng.github.io/posts/2018-05-05-drl-implementation/
crawled: 2026-09-08
translated: 2026-09-08
---

# 用 Tensorflow + OpenAI Gym 实现深度强化学习模型

> 原文：[Implementing Deep Reinforcement Learning Models with Tensorflow + OpenAI Gym](https://lilianweng.github.io/posts/2018-05-05-drl-implementation/) · Lilian Weng（翁荔）

> 让我们看看如何用代码实现一批经典的深度强化学习模型。

完整实现见 [lilianweng/deep-reinforcement-learning-gym](https://github.com/lilianweng/deep-reinforcement-learning-gym)。

在前两篇文章中，我介绍了许多深度强化学习模型的算法。现在是动手实践、看看如何在实战中实现这些模型的时候了。实现将基于 Tensorflow 和 OpenAI [gym](https://github.com/openai/gym) 环境构建。本教程的完整版代码见 [[lilian/deep-reinforcement-learning-gym]](https://github.com/lilianweng/deep-reinforcement-learning-gym)。

## 环境搭建

0) 确保你已安装 [Homebrew](https://docs.brew.sh/Installation)：
```bash
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

1) 我建议为你的开发创建一个 virtualenv。当你有多个依赖冲突的项目时（比如一个要求 Python 2.7，另一个只兼容 Python 3.5+），它能让生活轻松得多。
```bash
# Install python virtualenv
brew install pyenv-virtualenv
# Create a virtual environment of any name you like with Python 3.6.4 support
pyenv virtualenv 3.6.4 workspace
# Activate the virtualenv named "workspace"
pyenv activate workspace
```

*[\*] 下面每一次新安装，请确保你处于 virtualenv 之中。*

2) 按照[说明](https://github.com/openai/gym#installation)安装 OpenAI gym。最小化安装运行：
```bash
git clone https://github.com/openai/gym.git 
cd gym 
pip install -e .
```

如果你想玩 Atari 游戏或其他高级包，请继续安装几个系统包。
```bash
brew install cmake boost boost-python sdl2 swig wget
```

对于 Atari，进入 gym 目录并用 pip 安装。如果你在安装 ALE（arcade learning environment）时遇到麻烦，这篇[文章](http://alvinwan.com/installing-arcade-learning-environment-with-python3-on-macosx/)很有帮助。
```bash
pip install -e '.[atari]'
```

3) 最后克隆"playground"代码并安装依赖。
```bash
git clone git@github.com:lilianweng/deep-reinforcement-learning-gym.git
cd deep-reinforcement-learning-gym
pip install -e .  # install the "playground" project.
pip install -r requirements.txt  # install required packages.
```

## Gym 环境

[OpenAI Gym](https://gym.openai.com/) 工具包提供了一组物理仿真环境、游戏和机器人模拟器，供我们把玩并为其设计强化学习智能体。一个环境对象可以通过 `gym.make("{environment name}"` 初始化：
```python
import gym
env = gym.make("MsPacman-v0")
```

![Pacman](https://lilianweng.github.io/posts/2018-05-05-drl-implementation/pacman-original.gif)

环境的动作和观测格式分别由 `env.action_space` 和 `env.observation_space` 定义。

gym [空间](https://gym.openai.com/docs/#spaces)的类型：
- `gym.spaces.Discrete(n)`：0 到 n-1 的离散值。
- `gym.spaces.Box`：数值的多维向量，每一维的上下界由 `Box.low` 和 `Box.high` 定义。

我们通过两个主要的 API 调用与环境交互：

**`ob = env.reset()`**
- 将环境重置为原始设置。
- 返回初始观测。

**`ob_next, reward, done, info = env.step(action)`**
- 在环境中施加一个应与 `env.action_space` 兼容的动作。
- 返回新观测 `ob_next`（env.observation_space）、一个奖励（float）、一个 `done` 标志（bool）和其他元信息（dict）。若 `done=True`，情节结束，我们应重置环境重新开始。更多内容见[这里](https://gym.openai.com/docs/#observations)。

## 朴素 Q-Learning

[Q-learning](https://lilianweng.github.io/posts/2018-02-19-rl-overview/#q-learning-off-policy-td-control)（Watkins & Dayan, 1992）学习动作价值（"Q 值"）并按 [Bellman 方程](https://lilianweng.github.io/posts/2018-02-19-rl-overview/#bellman-equations)更新它。关键点在于：估计下一个动作是什么时，它不遵循当前策略，而是独立地采纳最佳 Q 值（红色部分）。

$$
Q(s, a) \leftarrow (1 - \alpha) Q(s, a) + \alpha (r + \gamma \color{red}{\max_{a' \in \mathcal{A}} Q(s', a')})
$$

在朴素实现中，所有 (s, a) 对的 Q 值可以简单地记录在一个 dict 里。暂不涉及任何复杂的机器学习模型。
```python
from collections import defaultdict
Q = defaultdict(float)
gamma = 0.99  # Discounting factor
alpha = 0.5  # soft update param

env = gym.make("CartPole-v0")
actions = range(env.action_space)

def update_Q(s, r, a, s_next, done):
    max_q_next = max([Q[s_next, a] for a in actions]) 
    # Do not include the next state's value if currently at the terminal state.
    Q[s, a] += alpha * (r + gamma * max_q_next * (1.0 - done) - Q[s, a])
```

大多数 gym 环境有多维连续的观测空间（`gym.spaces.Box`）。为了确保我们的 Q 字典不会因试图记住无限多的键而爆炸，我们应用一个 wrapper 来离散化观测。[wrappers](https://github.com/openai/gym/tree/master/gym/wrappers) 的概念非常强大，借助它我们能够定制环境的观测、动作、step 函数等。无论应用了多少个 wrapper，`env.unwrapped` 总能取回内部原始的环境对象。

```python
import gym

class DiscretizedObservationWrapper(gym.ObservationWrapper):
    """This wrapper converts a Box observation into a single integer.
    """
    def __init__(self, env, n_bins=10, low=None, high=None):
        super().__init__(env)
        assert isinstance(env.observation_space, Box)

        low = self.observation_space.low if low is None else low
        high = self.observation_space.high if high is None else high

        self.n_bins = n_bins
        self.val_bins = [np.linspace(l, h, n_bins + 1) for l, h in
                         zip(low.flatten(), high.flatten())]
        self.observation_space = Discrete(n_bins ** low.flatten().shape[0])

    def _convert_to_one_number(self, digits):
        return sum([d * ((self.n_bins + 1) ** i) for i, d in enumerate(digits)])

    def observation(self, observation):
        digits = [np.digitize([x], bins)[0]
                  for x, bins in zip(observation.flatten(), self.val_bins)]
        return self._convert_to_one_number(digits)


env = DiscretizedObservationWrapper(
    env, 
    n_bins=8, 
    low=[-2.4, -2.0, -0.42, -3.5], 
    high=[2.4, 2.0, 0.42, 3.5]
)
```

让我们接入与 gym 环境的交互，每产生一个新的转移就更新一次 Q 函数。选取动作时，我们用 ε-贪婪来强制探索。
```python
import gym
import numpy as np
n_steps = 100000
epsilon = 0.1  # 10% chances to apply a random action

def act(ob):
    if np.random.random() < epsilon:
        # action_space.sample() is a convenient function to get a random action
        # that is compatible with this given action space.
        return env.action_space.sample()

    # Pick the action with highest q value.
    qvals = {a: q[state, a] for a in actions}
    max_q = max(qvals.values())
    # In case multiple actions have the same maximum q value.
    actions_with_max_q = [a for a, q in qvals.items() if q == max_q]
    return np.random.choice(actions_with_max_q)

ob = env.reset()
rewards = []
reward = 0.0

for step in range(n_steps):
    a = act(ob)
    ob_next, r, done, _ = env.step(a)
    update_Q(ob, r, a, ob_next, done)
    reward += r
    if done:
        rewards.append(reward)
        reward = 0.0
        ob = env.reset()
    else:
        ob = ob_next
```
通常我们从较高的 `epsilon` 开始，在训练过程中逐渐降低，这称为"epsilon 退火"。`QLearningPolicy` 的完整代码见[这里](https://github.com/lilianweng/deep-reinforcement-learning-gym/blob/master/playground/policies/qlearning.py)。

## 深度 Q 网络

[深度 Q 网络](https://lilianweng.github.io/posts/2018-02-19-rl-overview/#deep-q-network)是一项开创性工作，使 Q-learning 在用非线性函数近似 Q 值时训练更稳定、数据效率更高。两个关键要素是经验回放和单独更新的目标网络。

主损失函数如下：

$$
\begin{aligned}
& Y(s, a, r, s') = r + \gamma \max_{a'} Q_{\theta^{-}}(s', a') \\
& \mathcal{L}(\theta) = \mathbb{E}_{(s, a, r, s') \sim U(D)} \Big[ \big( Y(s, a, r, s') - Q_\theta(s, a) \big)^2 \Big]
\end{aligned}
$$

Q 网络可以是多层全连接神经网络、卷积网络或循环网络，取决于具体问题。在 DQN 策略的[完整实现](https://github.com/lilianweng/deep-reinforcement-learning-gym/blob/master/playground/policies/dqn.py)中，它由 `model_type` 参数决定，取值为 ("dense", "conv", "lstm") 之一。

下面的例子中，我用一个两层稠密连接神经网络学习倒立摆平衡问题的 Q 值。
```python
import gym
env = gym.make('CartPole-v1')
# The observation space is `Box(4,)`, a 4-element vector.
observation_size = env.observation_space.shape[0]
```

我们有一个用于创建网络的辅助函数：
```python
import tensorflow as tf
def dense_nn(inputs, layers_sizes, scope_name):
    """Creates a densely connected multi-layer neural network.
    inputs: the input tensor
    layers_sizes (list<int>): defines the number of units in each layer. The output 
        layer has the size layers_sizes[-1].
    """
    with tf.variable_scope(scope_name):
        for i, size in enumerate(layers_sizes):
            inputs = tf.layers.dense(
                inputs,
                size,
                # Add relu activation only for internal layers.
                activation=tf.nn.relu if i < len(layers_sizes) - 1 else None,
                kernel_initializer=tf.contrib.layers.xavier_initializer(),
                name=scope_name + '_l' + str(i)
            )
    return inputs
```

Q 网络和目标网络用一批转移（state, action, reward, state_next, done_flag）更新。输入张量有：
```python
batch_size = 32  # A tunable hyperparameter.

states = tf.placeholder(tf.float32, shape=(batch_size, observation_size), name='state')
states_next = tf.placeholder(tf.float32, shape=(batch_size, observation_size), name='state_next')
actions = tf.placeholder(tf.int32, shape=(batch_size,), name='action')
rewards = tf.placeholder(tf.float32, shape=(batch_size,), name='reward')
done_flags = tf.placeholder(tf.float32, shape=(batch_size,), name='done')
```

我们有两个结构相同的网络。它们都以状态观测为输入、以所有动作上的 Q 值为输出，网络架构一致。
```python
q = dense(states, [32, 32, 2], name='Q_primary')
q_target = dense(states_next, [32, 32, 2], name='Q_target')
```

目标网络 "Q_target" 以 `states_next` 张量为输入，因为我们用它的预测在 Bellman 方程中选择最优的下一状态。
```python
# The prediction by the primary Q network for the actual actions.
action_one_hot = tf.one_hot(actions, act_size, 1.0, 0.0, name='action_one_hot')
pred = tf.reduce_sum(q * action_one_hot, reduction_indices=-1, name='q_acted')

# The optimization target defined by the Bellman equation and the target network.
max_q_next_by_target = tf.reduce_max(q_target, axis=-1)
y = rewards + (1. - done_flags) * gamma * max_q_next_by_target

# The loss measures the mean squared error between prediction and target.
loss = tf.reduce_mean(tf.square(pred - tf.stop_gradient(y)), name="loss_mse_train")
optimizer = tf.train.AdamOptimizer(0.001).minimize(loss, name="adam_optim")
```
注意目标 y 上的 [tf.stop_gradient()](https://www.tensorflow.org/api_docs/python/tf/stop_gradient)，因为在最小化损失的梯度更新期间目标网络应保持固定。

![DQN-tensorflow](https://lilianweng.github.io/posts/2018-05-05-drl-implementation/dqn-tensorboard-graph.png)

目标网络通过每 `C` 步把主 Q 网络的参数复制过来（"硬更新"）或向主网络做 Polyak 平均（"软更新"）来更新：
```python
# Get all the variables in the Q primary network.
q_vars = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope="Q_primary")
# Get all the variables in the Q target network.
q_target_vars = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope="Q_target")
assert len(q_vars) == len(q_target_vars)

def update_target_q_net_hard():
    # Hard update
    sess.run([v_t.assign(v) for v_t, v in zip(q_target_vars, q_vars)])

def update_target_q_net_soft(tau=0.05):
    # Soft update: polyak averaging.
    sess.run([v_t.assign(v_t * (1. - tau) + v * tau) for v_t, v in zip(q_target_vars, q_vars)])
```

### Double Q-Learning

观察 Q 值目标的标准形式 $$Y(s, a) = r + \gamma \max_{a' \in \mathcal{A}} Q_\theta (s', a')$$，很容易注意到：我们用 $$Q_\theta$$ 在状态 s' 选择最佳下一动作，然后又用同一个 $$Q_\theta$$ 预测的动作值。这种两步强化的流程可能导致对某个（已经）被高估的值进一步高估，进而导致训练不稳定。Double Q-learning（[Hasselt, 2010](http://papers.nips.cc/paper/3964-double-q-learning.pdf)）提出的解决方案是使用两个 Q 网络 $$Q_1$$ 和 $$Q_2$$ 来解耦动作选择与动作价值估计：更新 $$Q_1$$ 时由 $$Q_2$$ 决定最佳下一动作，反之亦然。

$$
Y_1(s, a, r, s') = r + \gamma Q_1 (s', \arg\max_{a' \in \mathcal{A}}Q_2(s', a'))\\
Y_2(s, a, r, s') = r + \gamma Q_2 (s', \arg\max_{a' \in \mathcal{A}}Q_1(s', a'))
$$

要把 double Q-learning 纳入 DQN，最小的修改（[Hasselt, Guez, & Silver, 2016](https://arxiv.org/pdf/1509.06461.pdf)）是用主 Q 网络选择动作，而动作价值由目标网络估计：

$$
Y(s, a, r, s') = r + \gamma Q_{\theta^{-}}(s', \arg\max_{a' \in \mathcal{A}} Q_\theta(s', a'))
$$

在代码中，我们增加一个新张量用于接收主 Q 网络选出的动作作为输入，并增加一个张量操作用于选出该动作。
```python
actions_next = tf.placeholder(tf.int32, shape=(None,), name='action_next')
actions_selected_by_q = tf.argmax(q, axis=-1, name='action_selected')
```

损失函数中的预测目标 y 变为：
```python
actions_next_flatten = actions_next + tf.range(0, batch_size) * q_target.shape[1]
max_q_next_target = tf.gather(tf.reshape(q_target, [-1]), actions_next_flatten)
y = rewards + (1. - done_flags) * gamma * max_q_next_by_target
```

这里我用 [tf.gather()](https://www.tensorflow.org/api_docs/python/tf/gather) 选取感兴趣的动作值。

![tf-gather](https://lilianweng.github.io/posts/2018-05-05-drl-implementation/tf_gather.png)

*（图片来源：[tf.gather() 文档](https://www.tensorflow.org/api_docs/python/tf/gather)）*

在情节回放期间，我们把下一状态的数据喂给 `actions_selected_by_q` 操作来计算 `actions_next`。
```python
# batch_data is a dict with keys, ‘s', ‘a', ‘r', ‘s_next' and ‘done', containing a batch of transitions.
actions_next = sess.run(actions_selected_by_q, {states: batch_data['s_next']})
```

### 对偶 Q 网络（Dueling Q-Network）

对偶 Q 网络（[Wang et al., 2016](https://arxiv.org/pdf/1511.06581.pdf)）配备了一种增强的网络架构：输出层分出两个头，一个预测状态价值 V，另一个预测[优势](https://lilianweng.github.io/posts/2018-02-19-rl-overview/#value-function) A。Q 值随后重构为 $$Q(s, a) = V(s) + A(s, a)$$。

$$
\begin{aligned}
A(s, a) &= Q(s, a) - V(s)\\
V(s) &= \sum_a Q(s, a) \pi(a \vert s) = \sum_a (V(s) + A(s, a)) \pi(a \vert s) = V(s) + \sum_a A(s, a)\pi(a \vert s)\\
\text{Thus, }& \sum_a A(s, a)\pi(a \vert s) = 0
\end{aligned}
$$

为确保估计的优势值加和为零，$$\sum_a A(s, a)\pi(a \vert s) = 0$$，我们从预测中扣除均值。

$$
Q(s, a) = V(s) + (A(s, a) - \frac{1}{|\mathcal{A}|} \sum_a A(s, a))
$$

代码修改非常直接：

```python
q_hidden = dense_nn(states, [32], name='Q_primary_hidden')
adv = dense_nn(q_hidden, [32, env.action_space.n], name='Q_primary_adv')
v = dense_nn(q_hidden, [32, 1], name='Q_primary_v')

# Average dueling
q = v + (adv - tf.reduce_mean(adv, reduction_indices=1, keepdims=True))
```

![dueling-q-network](https://lilianweng.github.io/posts/2018-05-05-drl-implementation/dueling-q-network.png)
*（图片来源：[Wang et al., 2016](https://arxiv.org/pdf/1511.06581.pdf)）*

完整流程请查看[代码](https://github.com/lilianweng/deep-reinforcement-learning-gym/blob/master/playground/policies/dqn.py)。

## 蒙特卡洛策略梯度

我在[上一篇文章](https://lilianweng.github.io/posts/2018-04-08-policy-gradient/)中回顾了许多流行的策略梯度方法。蒙特卡洛策略梯度，也称 [REINFORCE](https://lilianweng.github.io/posts/2018-04-08-policy-gradient/#reinforce)，是一种显式学习策略模型的经典同策略方法。它使用从完整的同策略轨迹估计的回报，用策略梯度更新策略参数。

回报在 rollout 期间计算，然后作为输入喂进 Tensorflow 计算图。

```python
# Inputs
states = tf.placeholder(tf.float32, shape=(None, obs_size), name='state')
actions = tf.placeholder(tf.int32, shape=(None,), name='action')
returns = tf.placeholder(tf.float32, shape=(None,), name='return')
```

构建策略网络。我们通过最小化损失函数 $$\mathcal{L} = - (G_t - V(s)) \log \pi(a \vert s)$$ 来更新策略参数。
[tf.nn.sparse_softmax_cross_entropy_with_logits()](https://www.tensorflow.org/api_docs/python/tf/nn/sparse_softmax_cross_entropy_with_logits) 要求输入原始 logits 而非 softmax 之后的概率，这就是策略网络顶部没有 softmax 层的原因。
```python
# Policy network
pi = dense_nn(states, [32, 32, env.action_space.n], name='pi_network')
sampled_actions = tf.squeeze(tf.multinomial(pi, 1))  # For sampling actions according to probabilities.

with tf.variable_scope('pi_optimize'):
    loss_pi = tf.reduce_mean(
        returns * tf.nn.sparse_softmax_cross_entropy_with_logits(
            logits=pi, labels=actions), name='loss_pi')
    optim_pi = tf.train.AdamOptimizer(0.001).minimize(loss_pi, name='adam_optim_pi')
```

在情节回放期间，回报按如下方式计算：
```python
# env = gym.make(...)
# gamma = 0.99
# sess = tf.Session(...)

def act(ob):
    return sess.run(sampled_actions, {states: [ob]})

for _ in range(n_episodes):
    ob = env.reset()
    done = False

    obs = []
    actions = []
    rewards = []
    returns = []

    while not done:
        a = act(ob)
        new_ob, r, done, info = env.step(a)

        obs.append(ob)
        actions.append(a)
        rewards.append(r)
        ob = new_ob

    # Estimate returns backwards.
    return_so_far = 0.0
    for r in rewards[::-1]:
        return_so_far = gamma * return_so_far + r
        returns.append(return_so_far)

    returns = returns[::-1]

    # Update the policy network with the data from one episode.
    sess.run([optim_pi], feed_dict={
        states: np.array(obs),
        actions: np.array(actions),
        returns: np.array(returns),
    })
```

REINFORCE 的完整实现见[这里](https://github.com/lilianweng/deep-reinforcement-learning-gym/blob/master/playground/policies/reinforce.py)。

## Actor-Critic

[actor-critic](https://lilianweng.github.io/posts/2018-04-08-policy-gradient/#actor-critic) 算法同时学习两个模型：学习最佳策略的 actor 和估计状态价值的 critic。

1. 初始化 actor 网络 $$\pi(a \vert s)$$ 和 critic $$V(s)$$。
2. 收集一个新转移 (s, a, r, s')：为当前状态 s 采样动作 $$a \sim \pi(a \vert s)$$，获得奖励 r 和下一状态 s'。
3. 在情节回放期间计算 TD 目标 $$G_t = r + \gamma V(s')$$ 和 TD 误差 $$\delta_t = r + \gamma V(s') - V(s)$$。
4. 通过最小化 critic 损失更新 critic 网络：$$L_c = (V(s) - G_t)$$。
5. 通过最小化 actor 损失更新 actor 网络：$$L_a = - \delta_t \log \pi(a \vert s)$$。
6. 设 s' = s，重复第 2-5 步。

总体上，实现看起来与 REINFORCE 相当相似，只是多了一个 critic 网络。完整实现见此。

```python
# Inputs
states = tf.placeholder(tf.float32, shape=(None, observation_size), name='state')
actions = tf.placeholder(tf.int32, shape=(None,), name='action')
td_targets = tf.placeholder(tf.float32, shape=(None,), name='td_target')

# Actor: action probabilities
actor = dense_nn(states, [32, 32, env.action_space.n], name='actor')

# Critic: action value (Q-value)
critic = dense_nn(states, [32, 32, 1], name='critic')

action_ohe = tf.one_hot(actions, act_size, 1.0, 0.0, name='action_one_hot')
pred_value = tf.reduce_sum(critic * action_ohe, reduction_indices=-1, name='q_acted')
td_errors = td_targets - tf.reshape(pred_value, [-1])

with tf.variable_scope('critic_train'):
    loss_c = tf.reduce_mean(tf.square(td_errors))
    optim_c = tf.train.AdamOptimizer(0.01).minimize(loss_c)

with tf.variable_scope('actor_train'):
    loss_a = tf.reduce_mean(
        tf.stop_gradient(td_errors) * tf.nn.sparse_softmax_cross_entropy_with_logits(
            logits=actor, labels=actions),
        name='loss_actor')
    optim_a = tf.train.AdamOptimizer(0.01).minimize(loss_a)

train_ops = [optim_c, optim_a]
```

tensorboard 计算图总是很有帮助：
![ac-tensorflow](https://lilianweng.github.io/posts/2018-05-05-drl-implementation/actor-critic-tensorboard-graph.png)

## 参考文献

[1] [Tensorflow API Docs](https://www.tensorflow.org/api_docs/)

[2] Christopher JCH Watkins, and Peter Dayan. ["Q-learning."](https://link.springer.com/content/pdf/10.1007/BF00992698.pdf) Machine learning 8.3-4 (1992): 279-292.

[3] Hado Van Hasselt, Arthur Guez, and David Silver. ["Deep Reinforcement Learning with Double Q-Learning."](https://arxiv.org/pdf/1509.06461.pdf) AAAI. Vol. 16. 2016.

[4] Hado van Hasselt. ["Double Q-learning."](http://papers.nips.cc/paper/3964-double-q-learning.pdf) NIPS,  23:2613–2621, 2010.

[5] Ziyu Wang, et al. [Dueling network architectures for deep reinforcement learning.](https://arxiv.org/pdf/1511.06581.pdf) ICML. 2016.
