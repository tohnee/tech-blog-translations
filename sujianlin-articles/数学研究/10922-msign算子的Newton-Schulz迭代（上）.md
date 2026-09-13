---
title: "msign算子的Newton-Schulz迭代（上）"
date: "2025-05-11"
author: "苏剑林"
category: "数学研究"
tags: ["迭代", "近似", "优化器", "muon"]
url: "https://kexue.fm/archives/10922"
blog: "科学空间 | Scientific Spaces"
---

在之前的[《Muon优化器赏析：从向量到矩阵的本质跨越》](https://kexue.fm/archives/10592)、[《Muon续集：为什么我们选择尝试Muon？》](https://kexue.fm/archives/10739)等文章中，我们介绍了一个极具潜力、有望替代Adam的新兴优化器——“Muon”。随着相关研究的不断深入，Muon优化器受到的关注度也在日益增加。

了解过Muon的读者都知道，Muon的核心运算是$\newcommand{msign}{\mathop{\text{msign}}}\msign$算子，为其寻找更高效的计算方法是学术社区的一个持续目标。本文将总结一下它的最新进展。

## 写在前面
$\msign$的定义跟SVD密切相关。假设矩阵$\boldsymbol{M}\in\mathbb{R}^{n\times m}$，那么
\begin{equation}\boldsymbol{U},\boldsymbol{\Sigma},\boldsymbol{V}^{\top} = \text{SVD}(\boldsymbol{M}) \quad\Rightarrow\quad \msign(\boldsymbol{M}) = \boldsymbol{U}_{[:,:r]}\boldsymbol{V}_{[:,:r]}^{\top}\end{equation}
其中$\boldsymbol{U}\in\mathbb{R}^{n\times n},\boldsymbol{\Sigma}\in\mathbb{R}^{n\times m},\boldsymbol{V}\in\mathbb{R}^{m\times m}$，$r$是$\boldsymbol{M}$的秩。简单来说，$\msign$就是把矩阵的所有非零奇异值都变成1后所得的新矩阵。基于SVD，我们还可以证明
\begin{equation}\text{msign}(\boldsymbol{M}) = (\boldsymbol{M}\boldsymbol{M}^{\top})^{-1/2}\boldsymbol{M}= \boldsymbol{M}(\boldsymbol{M}^{\top}\boldsymbol{M})^{-1/2}\end{equation}
这里的$^{-1/2}$的矩阵的$-1/2$次幂。这个形式跟标量的$\mathop{\text{sign}}(x) = x / \sqrt{x^2}$很相似，所以笔者用了$\msign$这个名字。但要注意的是这跟维基的“[Matrix Sign](https://en.wikipedia.org/wiki/Matrix_sign_function)”不完全相同，维基的概念只适用于方阵，但当$\boldsymbol{M}$是对称矩阵时，两者是一致的。

当$m=n=r$时，$\text{msign}(\boldsymbol{M})$还有一个意义是“最优正交近似”：
\begin{equation}\text{msign}(\boldsymbol{M}) = \mathop{\text{argmin}}_{\boldsymbol{O}^{\top}\boldsymbol{O} = \boldsymbol{I}}\Vert \boldsymbol{M} - \boldsymbol{O}\Vert_F^2\end{equation}
证明过程可参考[《Muon优化器赏析：从向量到矩阵的本质跨越》](https://kexue.fm/archives/10592)。因为这个特性，$\msign$也被称为“对称正交化”，这个名字最早出自[《On the Nonorthogonality Problem》](https://www.sciencedirect.com/science/article/abs/pii/S0065327608603391)（参考维基百科的“[Orthogonalization](https://en.wikipedia.org/wiki/Orthogonalization)”条目）。

最后，在[《高阶MuP：更简明但更高明的谱条件缩放》](https://kexue.fm/archives/10795)中，$\msign$还被笔者视为“奇异值裁剪”的极限版本。

## 迭代计算
$\msign$由SVD定义，自然也可以直接用SVD来精确计算，然而精确的SVD计算复杂度比较高，所以实践中往往都是用“Newton-Schulz迭代”近似计算。

Newton-Schulz迭代是求矩阵函数的常用迭代算法，在$\msign$这里它的迭代格式是
\begin{equation}\boldsymbol{X}_0 = \frac{\boldsymbol{M}}{\Vert\boldsymbol{M}\Vert_F},\qquad \boldsymbol{X}_{t+1} = a\boldsymbol{X}_t + b\boldsymbol{X}_t(\boldsymbol{X}_t^{\top}\boldsymbol{X}_t) + c\boldsymbol{X}_t(\boldsymbol{X}_t^{\top}\boldsymbol{X}_t)^2+\cdots\end{equation}
其中$\Vert\boldsymbol{M}\Vert_F$是$\boldsymbol{M}$的$F$范数，即所有元素的平方和的平方根，$(a,b,c,\cdots)$是待定系数，实际计算中我们需要截断有限项，常见的是2项或者3项，即如下二选一：
\begin{gather}\boldsymbol{X}_{t+1} = a\boldsymbol{X}_t + b\boldsymbol{X}_t(\boldsymbol{X}_t^{\top}\boldsymbol{X}_t) \\[8pt]
\boldsymbol{X}_{t+1} = a\boldsymbol{X}_t + b\boldsymbol{X}_t(\boldsymbol{X}_t^{\top}\boldsymbol{X}_t) + c\boldsymbol{X}_t(\boldsymbol{X}_t^{\top}\boldsymbol{X}_t)^2\label{eq:power-5}\end{gather}
最后返回$T$步迭代后的$\boldsymbol{X}_T$作为$\msign(\boldsymbol{M})$的近似。这样一来，系数$(a,b,c)$和迭代步数$T$就构成了Newton-Schulz迭代的全部超参数，Muon作者[KellerJordan](https://github.com/KellerJordan/Muon)给出的参考选择是
\begin{equation}(a,b,c)=(3.4445, -4.7750, 2.0315),\qquad T = 5\end{equation}
接下来我们的主题就是理解它，然后尝试改进它。

## 参考实现
这里给出一个极简的参考实现：

```
def msign(x, steps=5, eps=1e-20):
    a, b, c, y = 3.4445, -4.7750, 2.0315, x.astype('bfloat16')
    y = y.mT if x.shape[-2] > x.shape[-1] else y
    y /= ((y**2).sum(axis=(-2, -1), keepdims=True) + eps)**0.5
    for _ in range(steps):
        y = a * y + (b * (y2 := y @ y.mT) + c * y2 @ y2) @ y
    return y.mT if x.shape[-2] > x.shape[-1] else y
```

这个实现已经包含了batch运行能力（只对最后两个dims做$\msign$），可以在Jax跑通；如果将`x.astype('bfloat16')`改为`x.to(torch.bfloat16)`可以在Torch跑通；直接将`x.astype('bfloat16')`改为`x`也可以在Numpy跑通。

## 原理分析
为了理解Newton-Schulz迭代的原理，我们的逐一分析它的步骤。首先是$\boldsymbol{X}_0 = \boldsymbol{M}/\Vert\boldsymbol{M}\Vert_F$，我们代入$\boldsymbol{M}$的SVD：
\begin{equation}\boldsymbol{X}_0 = \frac{\boldsymbol{M}}{\Vert\boldsymbol{M}\Vert_F} = \boldsymbol{U}_{[:,:r]}\left(\frac{\boldsymbol{\Sigma}_{[:r,:r]}}{\Vert\boldsymbol{M}\Vert_F}\right)\boldsymbol{V}_{[:,:r]}^{\top} = \boldsymbol{U}_{[:,:r]}\underbrace{\left(\frac{\boldsymbol{\Sigma}_{[:r,:r]}}{\Vert\boldsymbol{\Sigma}_{[:r,:r]}\Vert_F}\right)}_{\boldsymbol{S}_0}\boldsymbol{V}_{[:,:r]}^{\top}\end{equation}
最后一个等号，是因为$F$范数的平方，既等于全体分量的平方和，又等于全体奇异值的平方和。最后的结果表明$\boldsymbol{S}_0$是一个分量均在$[0,1]$内的对角阵，换言之$\boldsymbol{X}_0=\boldsymbol{U}_{[:,:r]}\boldsymbol{S}_0\boldsymbol{V}_{[:,:r]}^{\top}$的全体奇异值都不超过1，这就是第一步$\boldsymbol{X}_0 = \boldsymbol{M}/\Vert\boldsymbol{M}\Vert_F$的目的。

接着，我们代入$\boldsymbol{U}_{[:,:r]}\boldsymbol{S}_t\boldsymbol{V}_{[:,:r]}^{\top}$到式$\eqref{eq:power-5}$，将会得到
\begin{equation}\boldsymbol{X}_{t+1} = \boldsymbol{U}_{[:,:r]}\left(a\boldsymbol{S}_t + b\boldsymbol{S}_t^3 + c\boldsymbol{S}_t^5\right)\boldsymbol{V}_{[:,:r]}^{\top}\end{equation}
也就是说，迭代不改变左右的$\boldsymbol{U}_{[:,:r]}$和$\boldsymbol{V}_{[:,:r]}^{\top}$，本质上式对角阵的迭代
\begin{equation}\boldsymbol{S}_{t+1} = a\boldsymbol{S}_t + b\boldsymbol{S}_t^3 + c\boldsymbol{S}_t^5\end{equation}
然后对角阵的幂又等价于对角线元素各自取幂，所以这本质又等价于标量$x_t$的迭代
\begin{equation}x_{t+1} = a x_t + b x_t^3 + c x_t^5\end{equation}
由于$\boldsymbol{X}_0 = \boldsymbol{M}/\Vert\boldsymbol{M}\Vert_F$已经将奇异值都压缩在$(0,1]$内，所以我们希望从任意$x_0\in(0,1]$出发，经过$T$步迭代后，$x_T$能够尽可能接近于1，那么迭代$\eqref{eq:power-5}$就可以足够近似$\msign$。这样一来，我们将矩阵的迭代分析简化为标量的迭代分析，大大降低了分析难度。

## 优化求解
其实$a,b,c$的求解，我们在[《Muon优化器赏析：从向量到矩阵的本质跨越》](https://kexue.fm/archives/10592)首次介绍Muon时也简单讨论过，基本思路是将$a,b,c$视为优化参数，用$x_T$与$1$的差来构建Loss，然后用SGD来优化。

本文的思路大致相同，但稍作调整。很明显，优化结果将会依赖于奇异值分布，之前笔者的思路是用随机矩阵SVD来模拟真实奇异值分布，但SVD费时费力，并且结果还会依赖于矩阵的shape，现在看来没太大必要，我们改为在$[0,1]$内均匀取点，然后选择$|x_T-1|$最大的$k$个点来构建Loss，这样转化为一个$\min\text{-}\max$问题，尽可能减轻奇异值分布的影响：

```
import jax
import jax.numpy as jnp
from tqdm import tqdm

def loss(w, x, k=50):
    for a, b, c in [w] * iters:
        x = a * x + b * x**3 + c * x**5
    return jnp.abs(x - 1).sort()[-k:].mean()

@jax.jit
def grad(w, x, tol=0.1):
    G = lambda w, x: (g := jax.grad(loss)(w, x)) / jnp.fmax(jnp.linalg.norm(g), 1)
    return 0.6 * G(w, x) + 0.2 * (G(w + tol / 2, x) + G(w - tol / 2, x))

iters = 5
x = jnp.linspace(0, 1, 10001)[1:]
w = jnp.array([1.5, -0.5, 0])
m, v = jnp.zeros_like(w), jnp.zeros_like(w)
lr = 1e-3
pbar = tqdm(range(20000), ncols=0, desc='Adam')

for i in pbar:
    l, g = loss(w, x), grad(w, x)
    m = 0.9 * m + 0.1 * g
    v = 0.999 * v + 0.001 * g**2
    w = w - lr * m / jnp.sqrt(v + 1e-20)
    pbar.set_description(f'Loss: {l:.6f}, LR: {lr:.6f}')
    if i in [10000]:
        lr *= 0.1
```

此外，优化器也从SGD改为Adam，这比较容易控制参数的更新幅度，同时为了增强解的噪声抵御能力，我们给$a,b,c$加上一定扰动，然后将扰动后的梯度也混合进来。上述脚本的优化结果是：
\begin{equation}(a,b,c)=(3.3748, -4.6969, 2.1433)\end{equation}
可以看到跟KellerJordan解相差不远。进一步通过图像比较一下两者差异：

[![[0, 1]的近似效果](https://kexue.fm/usr/uploads/2025/05/812396616.png)](https://kexue.fm/usr/uploads/2025/05/812396616.png "点击查看原图")

[0, 1]的近似效果

[![[0, 0.01]的近似效果](https://kexue.fm/usr/uploads/2025/05/519231176.png)](https://kexue.fm/usr/uploads/2025/05/519231176.png "点击查看原图")

[0, 0.01]的近似效果

可以看到，全局来看，我们这里求出的解平均误差小一点，KellerJordan解的好处则是在$[0, 0.01]$区间内的斜率大一点，这意味着它对更小的奇异值会更有利。

## 初值分布
在进一步讨论之前，我们需要明确一个问题：我们究竟要关心多小的奇异值？这要回到$\boldsymbol{S}_0$的分布上。由于$\boldsymbol{S}_0$经过$F$范数归一化，所以$\mathop{\text{diag}}(\boldsymbol{S}_0)$实际上是一个$r$维单位向量。如果全体奇异值都相等，那么可以推出每个奇异值都是$1/\sqrt{r}$。

于是，根据鸽笼原理，我们得到非均匀的情况下必然存在少于$1/\sqrt{r}$的奇异值。保险起见，我们可以考虑一个倍数，比如10倍，这意味着我们至少要兼顾到$0.1/\sqrt{r}$大小的奇异值。实际情况中，一个矩阵严格低秩（即奇异值严格等于0）的概率是很小的，所以我们一般都是假设矩阵满秩，即$r = \min(n,m)$，因此至少要兼顾$0.1/\sqrt{\min(n,m)}$的奇异值。

考虑到现在最大的LLM，hidden_size已经来到了$8192\sim 100^2$这个级别，所以根据这个数值估计，一个通用的Muon优化器，它的$\msign$算法至少要兼顾到$0.001$大小的奇异值，即能够将$0.001$映射到接近于1的值，这样看来不管是KellerJordan解还是我们新求出的解，都差点意思。

注：关于初值分布的讨论，我们还可以参考[《Iterative Orthogonalization Scaling Laws》](https://papers.cool/arxiv/2505.04005)。

## 解开约束
这时候，推特上[@YouJiacheng](https://twitter.com/YouJiacheng/status/1893704552689303901)（Muon主要推动者之一）提出了一个非常机智的想法：每一步迭代我们可以使用不同的系数！也就是将迭代改为
\begin{equation}\boldsymbol{X}_{t+1} = a_{t+1}\boldsymbol{X}_t + b_{t+1}\boldsymbol{X}_t(\boldsymbol{X}_t^{\top}\boldsymbol{X}_t) + c_{t+1}\boldsymbol{X}_t(\boldsymbol{X}_t^{\top}\boldsymbol{X}_t)^2\end{equation}
这样改动的好处是当选定$T$后，总计算量完全不会有任何变化，但从拟合的角度看，原本只有$3$个训练参数，现在变成了$3T$个，拟合能力将会大大加强。他本人给出的参考结果是一个6步迭代：
\begin{array}{c|ccc}
\hline
t & a & b & c \\
\hline
\quad 1\quad & 3955/1024 & -8306/1024 & 5008/1024 \\
2 & 3735/1024 & -6681/1024 & 3463/1024 \\
3 & 3799/1024 & -6499/1024 & 3211/1024 \\
4 & 4019/1024 & -6385/1024 & 2906/1024 \\
5 & 2677/1024 & -3029/1024 & 1162/1024 \\
6 & 2172/1024 & -1833/1024 &  682/1024 \\
\hline
\end{array}
我们可以画出来对比一下：

[![[0, 1]的近似效果](https://kexue.fm/usr/uploads/2025/05/350533843.png)](https://kexue.fm/usr/uploads/2025/05/350533843.png "点击查看原图")

[0, 1]的近似效果

[![[0, 0.01]的近似效果](https://kexue.fm/usr/uploads/2025/05/3892110485.png)](https://kexue.fm/usr/uploads/2025/05/3892110485.png "点击查看原图")

[0, 0.01]的近似效果

公平起见，KellerJordan解和Ours解也都改为了$T=6$。可见，不管是从光滑程度还是整体近似程度来看，YouJiacheng解都有非常明显的提升，这充分体现了去掉参数共享后所释放的“完全体”威力。

## 自己试试
YouJiacheng解是怎么求出来的呢？作者在[这里](https://gist.github.com/YouJiacheng/393c90cbdc23b09d5688815ba382288b/5bff1f7781cf7d062a155eecd2f13075756482ae)分享了他的代码，思路也是用Adam来求解，但包含了很多不同的Loss，理解起来有点麻烦。事实上，用我们前面的脚本，配合他提供的初始化，可以得到同样好的结果：
\begin{array}{c|ccc}
\hline
t & a & b & c \\
\hline
\quad 1\quad & 4140/1024 & -7553/1024 & 3571/1024 \\
2 & 3892/1024 & -6637/1024 & 2973/1024 \\
3 & 3668/1024 & -6456/1024 & 3021/1024 \\
4 & 3248/1024 & -6211/1024 & 3292/1024 \\
5 & 2792/1024 & -5759/1024 & 3796/1024 \\
6 & 3176/1024 & -5507/1024 & 4048/1024 \\
\hline
\end{array}

参考代码：

```
import jax
import jax.numpy as jnp
from tqdm import tqdm

def loss(w, x, k=50):
    for a, b, c in w:
        x = a * x + b * x**3 + c * x**5
    return jnp.abs(x - 1).sort()[-k:].mean()

@jax.jit
def grad(w, x, tol=0.1):
    G = lambda w, x: (g := jax.grad(loss)(w, x)) / jnp.fmax(jnp.linalg.norm(g), 1)
    return 0.6 * G(w, x) + 0.2 * (G(w + tol / 2, x) + G(w - tol / 2, x))

iters = 6
x = jnp.linspace(0, 1, 10001)[1:]
w = jnp.array([[3.5, -6.04444444444, 2.84444444444]] * iters)
m, v = jnp.zeros_like(w), jnp.zeros_like(w)
lr = 1e-3
pbar = tqdm(range(20000), ncols=0, desc='Adam')

for i in pbar:
    l, g = loss(w, x), grad(w, x)
    m = 0.9 * m + 0.1 * g
    v = 0.999 * v + 0.001 * g**2
    w = w - lr * m / jnp.sqrt(v + 1e-20)
    pbar.set_description(f'Loss: {l:.6f}, LR: {lr:.6f}')
    if i in [10000]:
        lr *= 0.1
```

对比如下（标记为“Ours-X”）：

[![[0, 1]的近似效果](https://kexue.fm/usr/uploads/2025/05/518737221.png)](https://kexue.fm/usr/uploads/2025/05/518737221.png "点击查看原图")

[0, 1]的近似效果

[![[0, 0.01]的近似效果](https://kexue.fm/usr/uploads/2025/05/3430771328.png)](https://kexue.fm/usr/uploads/2025/05/3430771328.png "点击查看原图")

[0, 0.01]的近似效果

由图可见，相比YouJiacheng解，我们的结果振荡更多，但换来了$[0,0.001]$处更大的斜率。

## 其他解集
如果读者想要振荡更少的解，那么只需要调大$k$值，比如$k=200$的结果是：
\begin{array}{c|ccc}
\hline
t & a & b & c \\
\hline
\quad 1\quad & 4059/1024 & -7178/1024 & 3279/1024 \\
2 & 3809/1024 & -6501/1024 & 2925/1024 \\
3 & 3488/1024 & -6308/1024 & 3063/1024 \\
4 & 2924/1024 & -5982/1024 & 3514/1024 \\
5 & 2439/1024 & -5439/1024 & 4261/1024 \\
6 & 3148/1024 & -5464/1024 & 4095/1024 \\
\hline
\end{array}

这时候就跟YouJiacheng解相差无几了（Ours-X2）：

[![[0, 1]的近似效果](https://kexue.fm/usr/uploads/2025/05/1050151153.png)](https://kexue.fm/usr/uploads/2025/05/1050151153.png "点击查看原图")

[0, 1]的近似效果

[![[0, 0.01]的近似效果](https://kexue.fm/usr/uploads/2025/05/617077151.png)](https://kexue.fm/usr/uploads/2025/05/617077151.png "点击查看原图")

[0, 0.01]的近似效果

另外再给出一个5步的解，方便大家跟原始解对比：
\begin{array}{c|ccc}
\hline
t & a & b & c \\
\hline
\quad 1\quad & 4.6182 & -12.9582 & 9.3299 \\
2 & 3.8496 & -7.9585 & 4.3052 \\
3 & 3.5204 & -7.2918 & 4.0606 \\
4 & 3.2067 & -6.8243 & 4.2802 \\
5 & 3.2978 & -5.7848 & 3.8917 \\
\hline
\end{array}
效果图（Ours-X3）：

[![[0, 1]的近似效果](https://kexue.fm/usr/uploads/2025/05/2624824428.png)](https://kexue.fm/usr/uploads/2025/05/2624824428.png "点击查看原图")

[0, 1]的近似效果

[![[0, 0.01]的近似效果](https://kexue.fm/usr/uploads/2025/05/1368764254.png)](https://kexue.fm/usr/uploads/2025/05/1368764254.png "点击查看原图")

[0, 0.01]的近似效果

## 改良初值
至此，我们关于$a,b,c$的求解告一段落。总的来说，每一步使用不同的$a,b,c$，确实能大幅提高Newton-Schulz迭代的收敛性质，并且不增加任何计算成本，算得上免费午餐了。

除了优化Newton-Schulz迭代的系数外，还有其他思路可以改进迭代的收敛性质吗？还真有。[@johanwind](https://github.com/KellerJordan/modded-nanogpt/discussions/23#discussioncomment-11293594)、[@YouJiacheng](https://x.com/YouJiacheng/status/1866505635329978803)、[@ZhangRuichong](https://x.com/ZhangRuichong/status/1866496714733211809)等人发现，我们可以利用Newton-Schulz迭代的特点，近乎免费地提高初值的质量，从而提高收敛速度。[@leloykun](https://x.com/leloykun)则在[这里](https://github.com/KellerJordan/Muon/pull/14/files)给出了一个参考实现。

具体来说，目前改进Newton-Schulz迭代的主要努力都可以总结为“在保证收敛的前提下，尽可能地提高接近于零的奇异值的收敛速度”。如果我们能事先把这些接近于零的奇异值放大一点，那么在不改变迭代算法的前提下也能提高收敛速度。目前为了将奇异值压缩到$[0,1]$内，我们使用的是$F$范数归一化$\boldsymbol{M}/\Vert\boldsymbol{M}\Vert_F$，它将奇异值压缩成
\begin{equation}\sigma_i \quad\to\quad \frac{\sigma_i}{\Vert\boldsymbol{M}\Vert_F} = \frac{\sigma_i}{\sqrt{\sum\limits_{j=1}^r \sigma_i^2}} \in [0, 1]\end{equation}
这样做确实能达到目标，但也有压缩过度的问题，最紧凑的压缩方式应该是$\sigma_i\to \sigma_i/\sigma_1$，即谱归一化。问题是谱范数不如$F$范数容易计算，所以我们不得已选择了$F$范数。但是，我们有
\begin{equation}\sigma_1 \quad\leq\quad \underbrace{\sqrt[\uproot{10}8]{\sum_{j=1}^r \sigma_i^8}}_{\sqrt[4]{\Vert(\boldsymbol{M}^{\top}\boldsymbol{M})^2\Vert_F}}\quad\leq\quad \underbrace{\sqrt[\uproot{10}4]{\sum_{j=1}^r \sigma_i^4}}_{\sqrt{\Vert\boldsymbol{M}^{\top}\boldsymbol{M}\Vert_F}} \quad\leq\quad \underbrace{\sqrt{\sum_{j=1}^r \sigma_i^2}}_{\Vert\boldsymbol{M}\Vert_F} \end{equation}
这意味着用$\sqrt[4]{\Vert(\boldsymbol{M}^{\top}\boldsymbol{M})^2\Vert_F}$或$\sqrt{\Vert\boldsymbol{M}^{\top}\boldsymbol{M}\Vert_F}$作为归一化因子，理论上都比$\Vert\boldsymbol{M}\Vert_F$更好。非常巧妙的是，在Newton-Schulz迭代下，它们的计算是近乎免费的！为理解这一点，我们写出第一步迭代
\begin{equation}\boldsymbol{X}_0 = \frac{\boldsymbol{M}}{\Vert\boldsymbol{M}\Vert_F},\qquad \boldsymbol{X}_1 = a\boldsymbol{X}_0 + b\boldsymbol{X}_0(\boldsymbol{X}_0^{\top}\boldsymbol{X}_0) + c\boldsymbol{X}_0(\boldsymbol{X}_0^{\top}\boldsymbol{X}_0)^2\end{equation}
可以看到$\boldsymbol{X}_0^{\top}\boldsymbol{X}_0$和$(\boldsymbol{X}_0^{\top}\boldsymbol{X}_0)^2$是必然要算出来的，所以我们直接拿它们算$F$范数，然后重新归一化就行，参考代码：

```
def msign(x, steps=5, eps=1e-20):
    a, b, c, y = 3.4445, -4.7750, 2.0315, x.astype('bfloat16')
    y = y.mT if x.shape[0] > x.shape[1] else y
    y /= ((y**2).sum(axis=[-2, -1], keepdims=True) + eps)**0.5
    for i in range(steps):
        y4 = (y2 := y @ y.mT) @ y2
        if i == 0:
            n = ((y4**2).sum(axis=[-2, -1], keepdims=True) + eps)**0.125
            y, y2, y4 = y / n, y2 / n**2, y4 / n**4
        y = a * y + (b * y2 + c * y4) @ y
    return y.mT if x.shape[0] > x.shape[1] else y
```

实测结果，对于一个$100\times 100$的随机高斯矩阵，改进后的最小奇异值，大多数都在改进前的2倍以上，平均奇异值也更接近于1。不过，Muon作者也表示它可能会带来额外的不稳定性，因此还没有采纳到官方代码中。

## 文章小结
本文介绍了通过Newton-Schulz迭代来计算$\msign$的优化思路，所得结果相比Muon的官方解，能够明显提高迭代的收敛速度和效果。

最后需要指出的是，对于Muon来说，小规模的实验结果显示，$\msign$的计算精度跟模型的最终效果似乎没有必然联系，小模型下提高$\msign$的精度似乎只能在前期加速一点收敛速度，但最终结果并无变化。目前尚不清楚这个结论在更大规模的模型下是否成立。
