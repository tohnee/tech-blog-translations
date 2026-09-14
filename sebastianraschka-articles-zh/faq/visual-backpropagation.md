---
title: "神经网络反向传播的直观图解"
title_en: "A Visual Explanation of Backpropagation in Neural Networks"
source: https://sebastianraschka.com/faq/docs/visual-backpropagation.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 神经网络反向传播的直观图解

假设我们非常喜欢登山，而且这次为了增加一点额外的挑战，我们蒙住了眼睛，这样我们就看不见自己身在何处，也不知道什么时候完成了"目标"——也就是登顶。

由于无法预先看清路径，我们只能凭直觉行动：假设山顶是整座山"最高"的点，我们认为最陡峭的路径能最高效地把我们带到山顶。
我们通过迭代式地在四周"摸索"并朝着最陡上升的方向迈出一步来应对这个挑战——不妨称之为"梯度上升"。但如果我们到达了一个再也无法继续上升的地方呢？也就是说，每个方向都是向下的？此时，我们可能已经登上了山顶，但也可能只是走到了一块较小的平台……我们无从得知。

从本质上说，这只是梯度上升优化的一种类比（基本上就是通过梯度下降最小化代价函数的对应操作）。不过，这并不是反向传播所特有的内容，而只是最小化凸代价函数（如果只存在全局最小值）或非凸代价函数（它存在局部最小值，就像那些让我们误以为已登顶的"平台"）的一种方式。借助一点视觉辅助，我们可以把一个只有一个参数的非凸代价函数（蓝球表示我们当前所在的位置）画成下面这样：

![](https://sebastianraschka.com/images/faq/visual-backpropagation/nonconvex-cost.png)

而反向传播，只是把代价"反向传播"穿过多个"层级"（或称层）。例如，对于一个多层感知机，我们可以把前向传播（把输入信号传入网络，同时乘以相应的权重以计算输出）画成下面这样：

![](https://sebastianraschka.com/images/faq/visual-backpropagation/forward-propagation.png)

而在反向传播中，我们"只需"把误差反向传播回去（即我们通过比较计算得到的输出与已知的正确目标输出所算出的"代价"，随后用它来更新模型参数）：

![](https://sebastianraschka.com/images/faq/visual-backpropagation/backpropagation.png)

虽然离上次学微积分先修课可能已经过去很久了，但这一切本质上都基于我们对嵌套函数所使用的简单链式法则：

![](https://sebastianraschka.com/images/faq/visual-backpropagation/chain_rule_1.png)

![](https://sebastianraschka.com/images/faq/visual-backpropagation/chain_rule_2.png)

与其"手动"做这些，我们可以使用计算工具（称为"自动微分"），而反向传播基本上就是这种自动微分的"反向"（reverse）模式。为什么是反向而不是正向？因为计算上更便宜！如果我们按正向来做，就得对每一层依次做大矩阵与大矩阵相乘，直到在输出层用一个向量去乘一个大矩阵。但如果反过来，也就是先做矩阵乘向量，我们会得到另一个向量，依此类推。所以我想说，反向传播的美妙之处在于：我们做的是更高效的矩阵-向量乘法，而不是矩阵-矩阵乘法。
