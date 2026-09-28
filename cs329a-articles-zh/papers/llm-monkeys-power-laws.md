---
title: "大语言模型猴子从何获得（超）能力？（缩放定律）"
title_en: "How Do Large Language Monkeys Get Their Power (Laws)?"
arxiv: 2502.17578
source: https://arxiv.org/abs/2502.17578
crawled: 2026-09-23
translated: 2026-09-23
---

# 大语言模型猴子从何获得（超）能力？（缩放定律）

> 原文：[How Do Large Language Monkeys Get Their Power (Laws)?](https://arxiv.org/abs/2502.17578) · Stanford CS329A 指定阅读

Rylan Schaeffer¹、Joshua Kazdan²、John Hughes³⁴、Jordan Juravsky¹、Sara Price⁴、Aengus Lynch⁴⁵、Erik Jones⁶、Robert Kirk⁵、Azalia Mirhoseini¹、Sanmi Koyejo¹

###### 摘要

近来横跨数学问题求解、证明助手编程与多模态越狱的研究记录了一个引人注目的发现：当（多模态）语言模型以每题多次尝试的方式处理一组任务——只要任意一次尝试正确即算成功——那么平均成功率的负对数随尝试次数呈幂律缩放。在本工作中，我们指出了一个表面上的悖论：一个简单的数学计算预言，在每道题上，失败率应随尝试次数指数下降。我们在经验上证实了这一预言，由此引出一个问题：聚合层面的多项式缩放从何而来？随后我们回答了这一问题：只要单次尝试成功概率的分布是重尾的——即一小部分成功率极低的任务合起来把聚合成功趋势扭曲成幂律——逐题的指数缩放就可以与聚合的多项式缩放相容，即便每道题自身都在按指数缩放。我们进一步证明，这一分布视角能解释先前观察到的对幂律缩放的偏离，并提供了一种预测幂律指数的简单方法，其相对误差低约一个数量级，等价地，所需推理计算少约 $2\text{--}4$ 个数量级。总体而言，本工作有助于更好地理解神经语言模型性能如何随推理计算的扩展而改进，并推动（多模态）语言模型缩放可预测评估的发展。

## 1 引言

大型神经语言模型的缩放行为令工程师、科学家和整个社会既惊讶又着迷（Hestness et al., 2017；Kaplan et al., 2020；Brown et al., 2020a；Hoffmann et al., 2022；Ganguli et al., 2022；Sorscher et al., 2022；Wei et al., 2022b；Schaeffer et al., 2023；OpenAI et al., 2024），并塑造了工程界、经济界和政府对前沿 AI 系统的兴趣（Bommasani et al., 2021；Eloundou et al., 2023；Anderljung et al., 2023；Wang et al., 2023；Reuel et al., 2024；Besiroglu et al., 2024a；Maslej et al., 2024）。相关文献的更详尽阐述请见相关工作（第 6 节）。

图 1：语言模型重复采样中的幂律缩放。上：Brown et al. (2024) 发现求解数学问题的负对数平均通过率 $-\log(\operatorname{pass_{\mathcal{D}}@k})$ 随每题独立尝试次数 $k$ 多项式（即幂律）缩放。下：Hughes et al. (2024) 在对多模态语言模型做越狱时类似地发现，负对数平均攻击成功率 $-\log(\operatorname{ASR_{\mathcal{D}}@k})$ 随每个提示的越狱尝试次数多项式缩放。这样的幂律缩放应当被预期吗？大语言模型猴子究竟从何处获得它们的（缩放）能力？

图 2：示意图：通过重复采样扩展推理计算时幂律的来源。$-\log(\operatorname{pass_{\mathcal{D}}@k})$ 随每题尝试次数 $k$ 呈幂律缩放（左）。这来自两个因素的组合：(1) 对每道题，$-\log(\operatorname{pass_{i}@k})$ 随 $k$ 指数缩放（中）；(2) 单次尝试成功率 $\operatorname{pass_{i}@1}$（在数据集的题目上）的分布本身在小值一侧具有幂律左尾（右）。

其中一个重获关注的方向是推理时计算扩展，即在推理时可控地增加计算以提升模型表现，例如 Pachocki et al. (2024)。在这一方向上，近期研究发现语言模型的成功率随完成任务的独立尝试次数可预测地缩放。具体而言，在一篇题为「Large Language Monkeys: Scaling Inference Compute with Repeated Sampling」的论文中，Brown et al. (2024) 研究了每题采样 $k$ 次独立尝试时，语言模型在数学问题求解与编程题上的表现如何变化。第 $i$ 道题上的表现用（对尝试取期望的）期望成功率度量（Kulal et al., 2019；Chen et al., 2021），定义为：

$$
\operatorname{pass_{i}@k}\;\defeq\;\mathbb{E}_{k\text{ 次尝试}}\Big[\mathbb{I}[\text{对第 }i\text{ 道题的任意一次尝试成功}]\Big]. \tag{1}
$$

使用 Chen et al. (2021) 的无偏且数值稳定的估计器（细节见附录 B），Brown et al. (2024) 发现对 $P$ 道题取平均的负对数成功率随每题独立尝试次数 $k$ 以幂律下降：

$$
-\log\Bigg(\frac{1}{P}\sum_{i=1}^{P}\operatorname{pass_{i}@k}\Bigg)\approx ak^{-b}, \tag{2}
$$

其中 $a,b>0$ 是模型特定且基准特定的常数（图 1 上）。不久之后，在通过文本、图像与音频攻击对多模态语言模型越狱这一独立话题上，Hughes et al. (2024) 的独立工作研究了每个有害提示做 $k$ 次独立尝试时的越狱成功率。表现用 $k$ 次尝试的攻击成功率（ASR）度量：

$$
\operatorname{ASR_{i}@k}\;\defeq\;\mathbb{E}_{k\text{ 次尝试}}\Big[\mathbb{I}[\text{对第 }i\text{ 个提示的任意一次攻击成功}]\Big]. \tag{3}
$$

这一「Best-of-N 越狱」攻击类似地发现，对 $P$ 个提示取平均的负对数攻击成功率随每个提示的越狱尝试次数 $k$ 以幂律下降：

$$
-\log\Bigg(\frac{1}{P}\sum_{i=1}^{P}\operatorname{ASR_{i}@k}\Bigg)\approx ak^{-b}, \tag{4}
$$

其中 $a,b>0$ 是模型特定且模态特定的常数（图 1 下）。两篇论文的具体系数见附录 C。作为术语上的小问题，两篇论文都用「覆盖率」（coverage，即每题 $k$ 次尝试后可被求解的问题比例）来表述结果，但正如 Brown et al. (2024) 指出的，覆盖率等价于平均成功率（附录 D）；我们更偏好后一种表述，因为它避免了「每道题在 $k$ 次尝试后要么被解出、要么没被解出」的二元含义。

## 2 幂律缩放应当被预期吗？

我们应当预期大语言模型猴子拥有这样的（缩放）能力吗？也就是说，平均成功率的负对数应当随独立尝试次数 $k$ 多项式缩放吗？正如我们接下来从数学上解释并在经验上证明的，这种随 $k$ 的多项式缩放或许出人意料，因为对任何单个问题，$k$ 处的负对数成功率应随 $k$ 指数下降；直觉在于：除非所有尝试都失败，否则 $\operatorname{pass_{i}@k}$ 就是 1，而由于各次尝试相互独立，全部失败的概率随尝试次数指数地 unlikely。

图 3：逐题表现随每题尝试次数 $k$ 指数缩放。上：Pythia 语言模型在 MATH 的 128 道题上，第 $i$ 道题的表现以 $-\log(\operatorname{pass_{i}@k})$ 度量。下：前沿 AI 模型在 HarmBench 越狱提示上，第 $i$ 个提示的表现以 $-\log(\operatorname{ASR_{i}@k})$ 度量。在两种设置中，每道题上负对数逐题成功率都随独立尝试次数 $k$ 指数下降。然而负对数平均成功率随 $k$ 呈幂律下降（黑色）。

数学上，在任意给定的一次尝试中，模型以概率 $\operatorname{pass_{i}@1}$ 解出第 $i$ 道题。回顾 $\operatorname{pass_{i}@k}$ 定义为：若 $k$ 次尝试中任意一次成功则为 1，否则为 0。由期望的线性性与 $k$ 次尝试的独立性，可以把 $\operatorname{pass_{i}@k}$ 改写为：

$$
\operatorname{pass_{i}@k}=\mathbb{E}_{k\text{ 次尝试}}\Big[1-\mathbb{I}[k\text{ 次尝试全部失败}]\Big] \tag{5}
$$

$$
=1-\prod_{j=1}^{k}\mathbb{E}_{1\text{ 次尝试}}\Big[\mathbb{I}[\text{第 }j\text{ 次尝试失败}]\Big]. \tag{6}
$$

第 $j$ 次尝试失败的概率等于一减第 $j$ 次尝试成功的概率。由于每次尝试是成功概率为 $\operatorname{pass_{i}@1}$ 的独立同分布试验，我们得到

$$
\operatorname{pass_{i}@k}=1-(1-\operatorname{pass_{i}@1})^{k}. \tag{7}
$$

当 $k$ 很大时，$(1-\operatorname{pass_{i}@1})^{k}$ 会很小。回顾 $\log(1+x)$ 在 $x$ 小时的泰勒级数展开 $\sum_{i=1}^{\infty}(-1)^{i-1}x^{i}/i\approx x$，我们有：

$$
-\log(\operatorname{pass_{i}@k})=-\log\Big(1-(1-\operatorname{pass@1})^{k}\Big) \tag{8}
$$

$$
\approx(1-\operatorname{pass_{i}@1})^{k}. \tag{9}
$$

图 4：单次尝试成功率分布具有类似幂律的左尾。Pythia 语言模型在 128 道 MATH 题上（上）与前沿 AI 系统在 159 个 HarmBench 提示上（下）的 $\operatorname{pass_{i}@1}$ 与 $\operatorname{ASR_{i}@1}$（在题目/提示上）的分布展现出类似幂律的尾部，可被缩放的 Beta-Binomial 分布很好拟合（黑色虚线），这些分布产生聚合幂律缩放。注意 Llama 3 8B 指令微调（IT）不具备幂律尾，这解释了该模型在 Best-of-N 越狱下未呈现聚合幂律缩放（第 4 节）。

因此，对任何单个问题，我们应当预期负对数期望（对尝试取期望的）成功率随 $k$ 指数下降，而不是随 $k$ 多项式下降。

为确认这一论断，我们绘制了模型在每道题上的表现缩放——以 $-\log(\operatorname{pass_{i}@k})$ 或 $-\log(\operatorname{ASR_{i}@k})$ 度量——随独立尝试次数 $k$ 的变化。我们具体使用了 Brown et al. (2024) 的 Pythia 语言模型家族（Biderman et al., 2023）求解 MATH（Hendrycks et al., 2021）128 道数学题的数据，以及 Hughes et al. (2024) 对前沿 AI 系统——Claude、GPT4（OpenAI et al., 2024）、Gemini（Team et al., 2024a；Team et al., 2024b）与 Llama 3 8B 指令微调（IT）（Grattafiori et al., 2024）——在 HarmBench（Mazeika et al., 2024）的 159 个提示上越狱的数据。对每一道数学题与每一个越狱提示，我们发现负对数期望（对尝试取期望的）成功率确实如预期那样随 $k$ 指数下降（图 3），包括在未呈现聚合幂律的 Llama 3 8B IT 上（图 1）。

## 3 逐题单次尝试成功率的分布造就幂律缩放

负对数逐题成功率的指数缩放如何产生负对数平均成功率的多项式缩放？这一问题的答案必然藏在基准题目上单次尝试（即 $k=1$）成功率分布 $\mathcal{D}$ 之中，因为该分布的密度 $p_{\mathcal{D}}(\operatorname{pass_{i}@1})$ 通过聚合成功率 $\operatorname{pass_{\mathcal{D}}@k}$ 的定义把逐题缩放行为与聚合缩放行为联系起来：

$$
\operatorname{pass_{\mathcal{D}}@k}\;\defeq\;\mathbb{E}_{\operatorname{pass_{i}@1}\sim\mathcal{D}}\Big[\operatorname{pass_{i}@k}(\operatorname{pass_{i}@1})\Big] \tag{10}
$$

$$
=1-\int_{0}^{1}(1-\operatorname{pass_{i}@1})^{k}\,p_{\mathcal{D}}(\operatorname{pass_{i}@1})\,\operatorname{d\,pass_{i}@1}.
$$

基于「幂律可以源自适当加权的指数函数之和」这一已知结果（附录 E.1），我们首先考虑单次尝试成功概率的一些简单分布，问哪些能在 $-\log(\operatorname{pass_{\mathcal{D}}@k})$ 与 $k$ 之间产生幂律缩放，以及分布的哪些性质决定了缩放指数。在附录 E.3-E.8 中，我们推导出若干简单分布以不同指数产生幂律缩放，而另一些则不会：

$$
-\log\big(\operatorname{pass_{\mathrm{Uniform}(0,\,\beta\leq 1)}}@k\big)\propto k^{-1}.
$$

$$
-\log\big(\operatorname{pass_{\operatorname{Beta(\alpha,\beta)}}@k}\big)\propto k^{-\alpha}.
$$

$$
-\log\big(\operatorname{pass_{\operatorname{Kumaraswamy(\alpha,\,\beta)}}@k}\big)\propto k^{-\alpha}.
$$

$$
-\log\big(\operatorname{pass_{\operatorname{ContinuousBernoulli(\lambda<1/2)}}@k}\big)\propto k^{-1}.
$$

$$
-\log\big(\operatorname{pass_{\operatorname{Reciprocal}(0<\alpha<\beta<1)}}@k\big)\propto\frac{(1-\alpha)^{k}}{k}.
$$

为检验这一理解，我们考察了 Brown et al. (2024) 与 Hughes et al. (2024) 的数据的逐题单次尝试成功率分布是否匹配这些简单分布之一（图 4）。我们发现这些分布确实能被带尺度参数 $c$ 的三参数 $\operatorname{Kumaraswamy}(\alpha,\beta,a=0,c)$ 分布很好拟合（图 4，黑色虚线）；我们发现尺度参数对获得良好拟合至关重要，因为标准的二参数 Kumaraswamy 分布支撑在 $(0,1)$ 上，而大多数单次尝试成功率分布的最大值更小，例如 $0.01$ 或 $0.1$。

更一般地，是哪些分布性质造就了这样的幂律缩放并设定了具体的幂律指数？正如我们即将展示的，负对数平均成功率将随 $k$ 以指数 $b$ 呈幂律缩放，当且仅当单次尝试成功概率（在题目上）的分布自身在 $0$ 附近表现得像指数为 $b-1$ 的幂律：

###### 定理 3.1（单次尝试成功率分布中幂律左尾的充分性）

设 $\mathcal{D}$ 为 $[0,1]$ 上的概率分布，PDF 为 $p_{\mathcal{D}}(\operatorname{pass_{i}@1})$。假设存在常数 $b>0$、$C>0$、$\theta>0$ 与 $\delta>0$，使得对所有 $0<\operatorname{pass_{i}@1}<\delta$，有

$$
p_{\mathcal{D}}(\operatorname{pass_{i}@1})\;=\;C\cdot(\operatorname{pass_{i}@1})^{b-1}\;+\;O\bigl((\operatorname{pass_{i}@1})^{b-1+\theta}\bigr).
$$

那么，对大的 $k$，

$$
-\log\big(\operatorname{pass_{\mathcal{D}}@k}\big)\;\sim\;C\,\Gamma(b)\;k^{-b}.
$$

###### 定理 3.2（单次尝试成功率分布中幂律左尾的必要性）

设 $\mathcal{D}$ 为 $\operatorname{pass_{i}@1}\in[0,1]$ 上的分布，PDF 为 $p_{\mathcal{D}}(\operatorname{pass_{i}@1})$。假设存在常数 $b>0$ 与 $A>0$，使得对大的 $k$，

$$
-\log\big(\operatorname{pass_{\mathcal{D}}@k}\big)\sim A\,k^{-b}.
$$

那么，在温和的正则性假设下，概率密度必须满足

$$
p_{\mathcal{D}}(\operatorname{pass_{i}@1})\;\sim\;\frac{A}{\Gamma(b)}\,(\operatorname{pass_{i}@1})^{b-1}\quad\text{当 }\operatorname{pass_{i}@1}\to 0^{+}.
$$

我们在图 2 中示意性地展示了这一联系。证明见附录 E 与 E.9。这些结果阐明：每当 $-\log(\operatorname{pass_{\mathcal{D}}@k})$ 呈现随 $k$、指数为 $b$ 的幂律衰减时，单次尝试成功率（在题目上）的分布*必然*在 $\operatorname{pass_{i}@1}=0$ 附近具有「多项式权重」，即 $p_{\mathcal{D}}(p)=\Theta(p^{\,b-1})$。

为提供直觉：我们知道每道题都正在被模型指数级快速地解出（等价地，每个提示都正在以指数速度越狱该模型）。若纵观基准中的所有题目，一些题的 $\operatorname{pass_{i}@1}$ 极小，以至于很多很多次尝试后仍未被解出。这些「极小 $\operatorname{pass_{i}@1}$」的问题在大的 $k$ 处是否仍然重要，取决于这样的问题*有多少*。在 $0$ 附近的多项式密度以恰到好处的方式「堆积」了足够多的困难问题，使得即便其中每个问题都在被指数级快速解出，*聚合*的成功率（在题目上）仍只以 $k$ 的幂律速率下降。一个更简洁的数学概括是：对复合二项分布而言，下尾概率控制了边缘生存函数的上尾。

## 4 缺乏分布结构解释了对幂律缩放的偏离

![Refer to caption](2502.17578v1/figures/92_schematic_distributional_fitting_attempt2/distributional_fitting_schematic.png)

图 5：示意图：通过重复采样扩展推理计算的幂律参数的两种估计器。(A) 两种估计器都从为每个提示生成大量样本开始，然后计算每个提示的成功次数。在标准最小二乘幂律参数估计器（上）中，(B) 在多个 $k$ 值处为每道题估计 $\operatorname{pass_{i}@k}$，然后 (C) 在题目上取平均并在 log-log 空间用线性回归拟合。在分布幂律参数估计器（下）中，(D) 对 $\operatorname{pass_{i}@1}$ 的估计拟合一个分布 $\mathcal{D}$，然后 (E) 用单次尝试成功概率分布模拟任意 $k$ 值处的 $\operatorname{pass_{\mathcal{D}}@k}$，以在 log-log 空间做线性回归。

值得注意的是，先前的论文观察到并非每个模型在每个设置下都呈现幂律缩放。举一个例子，Hughes et al. (2024) 观察到在对 Meta 的 Llama 3 8B 指令微调（IT）模型（Grattafiori et al., 2024）越狱时，$-\log(\operatorname{ASR_{\mathcal{D}}@k})$ 的下降快于任何幂律（图 1），也就是说 $\operatorname{ASR_{\mathcal{D}}@k}$ 的上升远快于其他前沿 AI 系统。基于我们的数学洞察与经验性的逐题单次尝试攻击成功率（图 4），我们可以理解其中的原因：Llama 3 8B IT 在允许的采样预算内每个提示都能被成功越狱，因此不具备产生聚合幂律缩放所必需的重左尾。

图 6：比较幂律指数的估计器。我们比较 $-\log(\operatorname{pass_{\mathcal{D}}@k})\approx ak^{-b}$ 中幂律指数 $b$ 的两种估计器：(1) log-log 空间中 $k$ 与 $-\log(\operatorname{pass_{\mathcal{D}}@k})$ 之间的标准最小二乘估计器；(2) 假设缩放 Kumaraswamy-Binomial 分布的 $\operatorname{pass_{i}@1}$ 分布估计器。用全部可用数据拟合两种估计器，我们发现最小二乘估计（纵轴）与分布导出估计（横轴）在 MATH 上的 Pythia 模型（左）与 HarmBench 上的前沿 AI 系统（右）上都相互吻合。关于两种估计器为何对 Large Language Monkeys 的匹配比对 Best-of-N Jailbreaking 更紧密，见附录 A。

图 7：通过回测比较幂律指数的两种估计器。在已知真实幂律 $a\,k^{-b}$ 的合成数据上，我们通过回测（对题目数量与每题样本数量做子采样）比较最小二乘与分布估计器以相对误差 $|\hat{b}-b|/b$ 度量恢复缩放指数 $b$ 的能力。我们发现分布估计器取得显著更好的样本效率。

## 5 一种预测幂律缩放的新型分布估计器

$-\log(\operatorname{pass_{\mathcal{D}}@k})$ 的缩放与分布 $p_{\mathcal{D}}(\operatorname{pass_{i}@1})$ 左尾之间这一联系的一个自然推论是：单次尝试成功率的分布可用来预测幂律缩放是否会出现，以及若出现，幂律的截距与指数是什么。为此，可以先拟合分布 $\hat{p}_{\mathcal{D}}(\operatorname{pass_{i}@1})$，再用以下关系模拟 $\operatorname{pass_{\mathcal{D}}@k}$ 将如何随 $k$ 缩放（图 5）：

$$
\widehat{\operatorname{pass_{\mathcal{D}}@k}}\defeq
$$

$$
1-\int_{0}^{1}(1-\operatorname{pass_{i}@1})^{k}\,\hat{p}_{\mathcal{D}}(\operatorname{pass_{i}@1})\,\operatorname{d\,pass_{i}@1}. \tag{11}
$$

为在经验上检验这一论断，我们把标准最小二乘回归估计器（在 log-log 空间）（Hoffmann et al., 2022；Caballero et al., 2022；Besiroglu et al., 2024b）与一个分布估计器做了比较。为引出我们的分布估计器，需要先解释一个关键障碍以及分布估计器如何克服它。这一障碍是：存在一些题目或提示，其单次尝试成功概率 $\operatorname{pass_{i}@1}$ 落在 $(0,1/\text{样本数})$ 之间，以致由于有限采样我们缺乏测量它们所需的分辨率。虽然我们不知道落在这个区间内的题目的真实单次尝试成功概率，但我们知道有多少题目落入这个左尾桶，并且可以拟合一个分布的参数，使该分布在区间 $(0,1/\text{样本数})$ 内的概率质量与该尾桶中题目的经验比例相匹配。因此，我们的分布估计器的做法是：先选择一个分布（例如缩放的三参数 Beta 分布），按采样分辨率 $1/\text{样本数}$ 对分布做离散化，然后在离散化分布的概率质量函数下做极大似然估计。

我们用两种不同方式测试了这一分布估计器。第一，聚焦 Large Language Monkeys，我们使用全部题目、每题全部样本的可用真实数据，比较标准最小二乘回归估计器与分布估计器。我们发现两种估计器高度吻合（图 6），让我们感到在大的采样预算下两种估计器给出相当一致的估计。

第二，分布估计器还有另一个好处：它直接给出 $a\,k^{-b}$ 中幂律指数 $b$ 的估计。估计幂律指数尤其有价值，因为指数决定了成功率如何随推理计算的增加而改进。为测试分布估计器与最小二乘估计器在恢复真实渐近幂律指数上的表现，我们生成了合成数据以便掌握真实幂律指数的真值，然后通过以更少题目与每题更少样本对数据做子采样，回测两种缩放估计器恢复真实指数的能力（Alabdulmohsin et al., 2022a；Owen, 2024）。我们发现分布估计器取得显著更好的样本效率，相对误差 $\defeq|\hat{b}-b|/b$ 比最小二乘估计器约低一个数量级（图 7），等价地，所需推理计算少约 $2\text{--}4$ 个数量级。分布估计器即便在分布失配下也表现良好。

## 6 相关工作

深度神经网络缩放定律的研究有着丰富的历史，横跨理论基础、经验验证与多样化应用。最早的探索在简单机器学习设置中发现了幂律缩放（Barkai et al., 1993；Mhaskar, 1996；Pinkus, 1999）。然而，缩放定律的现代纪元始于神经语言模型的开创性研究（Hestness et al., 2017；Kaplan et al., 2020；Brown et al., 2020b），催生了多个方向上的大量研究。

缩放定律的理论理解已显著推进（Spigler et al., 2020；Bousquet et al., 2020；Hutter, 2021；Sharma & Kaplan, 2022；Maloney et al., 2022；Roberts et al., 2022；Bahri et al., 2024；Michaud et al., 2024；Paquette et al., 2024；Atanasov et al., 2024；Bordelon et al., 2024a；Bordelon et al., 2024b；Lin et al., 2024；Brill, 2024），并有全面的经验研究作为补充（Rosenfeld et al., 2020；Henighan et al., 2020；Gordon et al., 2021；Tay et al., 2021；Ghorbani et al., 2021；Tay et al., 2022b；Zhai et al., 2022；Alabdulmohsin et al., 2022b；Dehghani et al., 2023；Bachmann et al., 2023）。在语言模型的语境下，研究者已探索了诸多方面的缩放行为：上下文长度（Xiong et al., 2023）、上下文学习（Chan et al., 2022；Agarwal et al., 2024；Arora et al., 2024）、词表规模（Tao et al., 2024）以及越狱尝试（Anil et al., 2024；Hughes et al., 2024）。研究还考察了微调中的缩放动力学（Kalajdzievski, 2024；Zhang et al., 2024）、迁移学习（Hernandez et al., 2021）以及重复数据的影响（Hernandez et al., 2022；Muennighoff et al., 2023）。架构层面的考量也被广泛研究，包括网络设计（Tay et al., 2022a；Clark et al., 2022）、嵌套模型（Kudugunta et al., 2023）、剪枝策略（Rosenfeld et al., 2021）与精度需求（Dettmers & Zettlemoyer, 2023；Kumar et al., 2024；Sun et al., 2025）。研究还涉及多模态扩展（Aghajanyan et al., 2023；Cherti et al., 2023）与推理优化（Sardana et al., 2023；Brown et al., 2024；Snell et al., 2024a；Wu et al., 2024；Chen et al., 2024）。该领域已扩展到众多领域，包括强化学习（单智能体（Jones, 2021；Hilton et al., 2023；Neumann & Gros, 2024）与多智能体（Neumann & Gros, 2022））、图网络（Liu et al., 2024）、扩散模型（Mei et al., 2024；Liang et al., 2024）与联想记忆模型（Romani et al., 2013；Cabannes et al., 2024；Schaeffer et al., 2024c）。近期工作探索了诸如逆缩放（McKenzie et al., 2024）、独特的函数形式（Caballero et al., 2022）、跨模型家族的缩放模式（Ruan et al., 2024；Polo et al., 2024）以及下游能力（Srivastava et al., 2023；Wei et al., 2022a；Hu et al., 2024；Schaeffer et al., 2024b；Snell et al., 2024b；Wu & Lo, 2024）等涌现现象。研究者还研究了关键挑战，包括数据污染（Schaeffer, 2023；Jiang et al., 2024；Dominguez-Olmedo et al., 2024）、模型-数据反馈循环（Dohmatob et al., 2024；Gerstgrasser et al., 2024；Kazdan et al., 2024）与过训练效应（Gao et al., 2023；Gadre et al., 2024）。其他贡献还包括稀疏自编码器（Gao et al., 2024）、生物学合理的反向传播（Filipovich et al., 2022）与视觉自监督学习（Schaeffer et al., 2024a）方面的研究。近期努力还聚焦于调和缩放行为中的表面矛盾（Besiroglu et al., 2024b；Porian et al., 2024）。

## 7 讨论与未来方向

本工作推进了我们对语言模型性能如何、以及为何随重复采样带来的额外推理计算而改进的数学理解。通过为这些经验观察到的幂律建立严格的理论基础，我们的工作为从业者提供了在扩展推理计算时理解与预测模型表现的有原则的方式。我们发展的分布视角解释了先前令人困惑的对幂律缩放的偏离，并使缩放参数的估计更高效。

两个相关的问题是：这种单次尝试成功率中的分布结构*为何*存在，以及是否应当预期这种结构出现在未来的基准中。我们推测至少有两个原因：(1) 基准设计，即基准被有意地构造为题目难度有分布、既不太容易也不太难；(2) 选择偏差，即幂律缩放等更有趣的模式更可能获得研究界更多的兴趣。

尽管聚焦于扩展推理计算，我们论文的贡献还包括对缩放预训练计算中一个开放问题的新假设：神经缩放定律为什么是幂律？正如 $-\log(\operatorname{pass_{\mathcal{D}}@k})$ 的缩放行为只在大的 $k$ 处才变得清晰，预训练交叉熵随预训练计算 $C$ 的缩放行为也可能如此。具体而言，假设预训练交叉熵 $\mathcal{L}$ 作为预训练计算 $C$ 的函数是许多以不同速率衰减的函数之和：

$$
\mathcal{L}(C)=\omega\Big(\frac{1}{C^{\alpha}}\Big)+\frac{A}{C^{\alpha}}+o\Big(\frac{1}{C^{\alpha}}\Big),
$$

其中 $\alpha$ 是最小的（正）多项式指数，$\omega(1/C^{\alpha})$ 表示衰减慢于任何多项式的函数。起初，在小的 $C$ 处，主导项可能不明确，但随着预训练计算扩展 8-10 个数量级，首阶项占据主导，一个近似的幂律便浮现出来：

$$
\mathcal{L}(C)\approx\text{const}+\frac{A}{C^{\alpha}}+0\quad\text{当}\quad C\rightarrow\infty.
$$

因此，幂律关系可能只对足够大的预训练计算 $C$ 才合理，这反过来可能需要剔除预训练计算最低的模型才能获得好的预测，这为一项普遍的经验实践提供了正当性（Kaplan et al., 2020）。我们把可能隐藏在 $\omega(1/C^{\alpha})$ 与 $o(1/C^{\alpha})$ 中的函数称为神经缩放定律的「暗物质」。

## 致谢

为盲审已隐去。

## 影响声明

我们的发现对大型语言模型的部署具有重要实际意义，因为它们可以帮助组织更准确地预测计算需求，并在模型规模、推理成本与性能目标之间做出知情的权衡。我们发展的数学框架还有可能从语言模型泛化到出现类似缩放现象的其他领域。虽然本工作主要是理论性的，但我们承认语言模型能力的进步可能带来广泛的社会影响。我们希望对这些基本缩放行为的更好理解能帮助研究界开发出更高效、更可靠的 AI 系统。

## 参考文献

- Agarwal et al. (2024)

  Agarwal, R., Singh, A., Zhang, L. M., Bohnet, B., Rosias, L., Chan, S. C., Zhang, B., Anand, A., Abbas, Z., Nova, A., Co-Reyes, J. D., Chu, E., Behbahani, F., Faust, A., and Larochelle, H.
  Many-shot in-context learning.
  In *The Thirty-eighth Annual Conference on Neural Information Processing Systems*, 2024.
  URL <https://openreview.net/forum?id=AB6XpMzvqH>.
- Aghajanyan et al. (2023)

  Aghajanyan, A., Yu, L., Conneau, A., Hsu, W.-N., Hambardzumyan, K., Zhang, S., Roller, S., Goyal, N., Levy, O., and Zettlemoyer, L.
  Scaling laws for generative mixed-modal language models.
  In *International Conference on Machine Learning*, pp. 265–279. PMLR, 2023.
- Alabdulmohsin et al. (2022a)

  Alabdulmohsin, I., Neyshabur, B., and Zhai, X.
  Revisiting neural scaling laws in language and vision, 2022a.
  URL <https://arxiv.org/abs/2209.06640>.
- Alabdulmohsin et al. (2022b)

  Alabdulmohsin, I. M., Neyshabur, B., and Zhai, X.
  Revisiting neural scaling laws in language and vision.
  *Advances in Neural Information Processing Systems*, 35:22300–22312, 2022b.
- Anderljung et al. (2023)

  Anderljung, M., Barnhart, J., Korinek, A., Leung, J., O’Keefe, C., Whittlestone, J., Avin, S., Brundage, M., Bullock, J., Cass-Beggs, D., Chang, B., Collins, T., Fist, T., Hadfield, G., Hayes, A., Ho, L., Hooker, S., Horvitz, E., Kolt, N., Schuett, J., Shavit, Y., Siddarth, D., Trager, R., and Wolf, K.
  Frontier ai regulation: Managing emerging risks to public safety, 2023.
  URL <https://arxiv.org/abs/2307.03718>.
- Anil et al. (2024)

  Anil, C., DURMUS, E., Rimsky, N., Sharma, M., Benton, J., Kundu, S., Batson, J., Tong, M., Mu, J., Ford, D. J., Mosconi, F., Agrawal, R., Schaeffer, R., Bashkansky, N., Svenningsen, S., Lambert, M., Radhakrishnan, A., Denison, C., Hubinger, E. J., Bai, Y., Bricken, T., Maxwell, T., Schiefer, N., Sully, J., Tamkin, A., Lanham, T., Nguyen, K., Korbak, T., Kaplan, J., Ganguli, D., Bowman, S. R., Perez, E., Grosse, R. B., and Duvenaud, D.
  Many-shot jailbreaking.
  In *The Thirty-eighth Annual Conference on Neural Information Processing Systems*, 2024.
  URL <https://openreview.net/forum?id=cw5mgd71jW>.
- Arora et al. (2024)

  Arora, A., Jurafsky, D., Potts, C., and Goodman, N. D.
  Bayesian scaling laws for in-context learning, 2024.
  URL <https://arxiv.org/abs/2410.16531>.
- Atanasov et al. (2024)

  Atanasov, A., Zavatone-Veth, J. A., and Pehlevan, C.
  Scaling and renormalization in high-dimensional regression.
  *arXiv preprint arXiv:2405.00592*, 2024.
- Bachmann et al. (2023)

  Bachmann, G., Anagnostidis, S., and Hofmann, T.
  Scaling mlps: A tale of inductive bias, 2023.
  URL <https://arxiv.org/abs/2306.13575>.
- Bahri et al. (2024)

  Bahri, Y., Dyer, E., Kaplan, J., Lee, J., and Sharma, U.
  Explaining neural scaling laws.
  *Proceedings of the National Academy of Sciences*, 121(27):e2311878121, 2024.
- Barkai et al. (1993)

  Barkai, N., Seung, H. S., and Sompolinsky, H.
  Scaling laws in learning of classification tasks.
  *Physical review letters*, 70(20):3167, 1993.
- Besiroglu et al. (2024a)

  Besiroglu, T., Emery-Xu, N., and Thompson, N.
  Economic impacts of ai-augmented r&d.
  *Research Policy*, 53(7):105037, 2024a.
- Besiroglu et al. (2024b)

  Besiroglu, T., Erdil, E., Barnett, M., and You, J.
  Chinchilla scaling: A replication attempt, 2024b.
  URL <https://arxiv.org/abs/2404.10102>.
- Biderman et al. (2023)

  Biderman, S., Schoelkopf, H., Anthony, Q. G., Bradley, H., O’Brien, K., Hallahan, E., Khan, M. A., Purohit, S., Prashanth, U. S., Raff, E., et al.
  Pythia: A suite for analyzing large language models across training and scaling.
  In *International Conference on Machine Learning*, pp. 2397–2430. PMLR, 2023.
- Bochud & Challet (2006)

  Bochud, T. and Challet, D.
  Optimal approximations of power-laws with exponentials, 2006.
  URL <https://arxiv.org/abs/physics/0605149>.
- Bommasani et al. (2021)

  Bommasani, R., Hudson, D. A., Adeli, E., Altman, R., Arora, S., von Arx, S., Bernstein, M. S., Bohg, J., Bosselut, A., Brunskill, E., et al.
  On the opportunities and risks of foundation models.
  *arXiv preprint arXiv:2108.07258*, 2021.
- Bordelon et al. (2024a)

  Bordelon, B., Atanasov, A., and Pehlevan, C.
  A dynamical model of neural scaling laws.
  *arXiv preprint arXiv:2402.01092*, 2024a.
- Bordelon et al. (2024b)

  Bordelon, B., Atanasov, A., and Pehlevan, C.
  How feature learning can improve neural scaling laws.
  *arXiv preprint arXiv:2409.17858*, 2024b.
- Bousquet et al. (2020)

  Bousquet, O., Hanneke, S., Moran, S., van Handel, R., and Yehudayoff, A.
  A theory of universal learning, 2020.
  URL <https://arxiv.org/abs/2011.04483>.
- Brill (2024)

  Brill, A.
  Neural scaling laws rooted in the data distribution.
  *arXiv preprint arXiv:2412.07942*, 2024.
- Brown et al. (2024)

  Brown, B., Juravsky, J., Ehrlich, R., Clark, R., Le, Q. V., Ré, C., and Mirhoseini, A.
  Large language monkeys: Scaling inference compute with repeated sampling, 2024.
  URL <https://arxiv.org/abs/2407.21787>.
- Brown et al. (2020a)

  Brown, T., Mann, B., Ryder, N., Subbiah, M., Kaplan, J. D., Dhariwal, P., Neelakantan, A., Shyam, P., Sastry, G., Askell, A., et al.
  Language models are few-shot learners.
  *Advances in neural information processing systems*, 33:1877–1901, 2020a.
- Brown et al. (2020b)

  Brown, T. B., Mann, B., Ryder, N., Subbiah, M., Kaplan, J., Dhariwal, P., Neelakantan, A., Shyam, P., Sastry, G., Askell, A., Agarwal, S., Herbert-Voss, A., Krueger, G., Henighan, T., Child, R., Ramesh, A., Ziegler, D. M., Wu, J., Winter, C., Hesse, C., Chen, M., Sigler, E., Litwin, M., Gray, S., Chess, B., Clark, J., Berner, C., McCandlish, S., Radford, A., Sutskever, I., and Amodei, D.
  Language models are few-shot learners, 2020b.
  URL <https://arxiv.org/abs/2005.14165>.
- Caballero et al. (2022)

  Caballero, E., Gupta, K., Rish, I., and Krueger, D.
  Broken neural scaling laws.
  *arXiv preprint arXiv:2210.14891*, 2022.
- Cabannes et al. (2024)

  Cabannes, V., Dohmatob, E., and Bietti, A.
  Scaling laws for associative memories, 2024.
  URL <https://arxiv.org/abs/2310.02984>.
- Chan et al. (2022)

  Chan, S., Santoro, A., Lampinen, A., Wang, J., Singh, A., Richemond, P., McClelland, J., and Hill, F.
  Data distributional properties drive emergent in-context learning in transformers.
  In Koyejo, S., Mohamed, S., Agarwal, A., Belgrave, D., Cho, K., and Oh, A. (eds.), *Advances in Neural Information Processing Systems*, volume 35, pp. 18878–18891. Curran Associates, Inc., 2022.
  URL <https://proceedings.neurips.cc/paper_files/paper/2022/file/77c6ccacfd9962e2307fc64680fc5ace-Paper-Conference.pdf>.
- Chen et al. (2021)

  Chen, M., Tworek, J., Jun, H., Yuan, Q., de Oliveira Pinto, H. P., Kaplan, J., Edwards, H., Burda, Y., Joseph, N., Brockman, G., Ray, A., Puri, R., Krueger, G., Petrov, M., Khlaaf, H., Sastry, G., Mishkin, P., Chan, B., Gray, S., Ryder, N., Pavlov, M., Power, A., Kaiser, L., Bavarian, M., Winter, C., Tillet, P., Such, F. P., Cummings, D., Plappert, M., Chantzis, F., Barnes, E., Herbert-Voss, A., Guss, W. H., Nichol, A., Paino, A., Tezak, N., Tang, J., Babuschkin, I., Balaji, S., Jain, S., Saunders, W., Hesse, C., Carr, A. N., Leike, J., Achiam, J., Misra, V., Morikawa, E., Radford, A., Knight, M., Brundage, M., Murati, M., Mayer, K., Welinder, P., McGrew, B., Amodei, D., McCandlish, S., Sutskever, I., and Zaremba, W.
  Evaluating large language models trained on code, 2021.
  URL <https://arxiv.org/abs/2107.03374>.
- Chen et al. (2024)

  Chen, Y., Pan, X., Li, Y., Ding, B., and Zhou, J.
  A simple and provable scaling law for the test-time compute of large language models, 2024.
  URL <https://arxiv.org/abs/2411.19477>.
- Cherti et al. (2023)

  Cherti, M., Beaumont, R., Wightman, R., Wortsman, M., Ilharco, G., Gordon, C., Schuhmann, C., Schmidt, L., and Jitsev, J.
  Reproducible scaling laws for contrastive language-image learning.
  In *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition*, pp. 2818–2829, 2023.
- Clark et al. (2022)

  Clark, A., de Las Casas, D., Guy, A., Mensch, A., Paganini, M., Hoffmann, J., Damoc, B., Hechtman, B., Cai, T., Borgeaud, S., et al.
  Unified scaling laws for routed language models.
  In *International conference on machine learning*, pp. 4057–4086. PMLR, 2022.
- Dehghani et al. (2023)

  Dehghani, M., Djolonga, J., Mustafa, B., Padlewski, P., Heek, J., Gilmer, J., Steiner, A. P., Caron, M., Geirhos, R., Alabdulmohsin, I., et al.
  Scaling vision transformers to 22 billion parameters.
  In *International Conference on Machine Learning*, pp. 7480–7512. PMLR, 2023.
- Dettmers & Zettlemoyer (2023)

  Dettmers, T. and Zettlemoyer, L.
  The case for 4-bit precision: k-bit inference scaling laws.
  In *International Conference on Machine Learning*, pp. 7750–7774. PMLR, 2023.
- Dohmatob et al. (2024)

  Dohmatob, E., Feng, Y., Yang, P., Charton, F., and Kempe, J.
  A tale of tails: Model collapse as a change of scaling laws, 2024.
  URL <https://arxiv.org/abs/2402.07043>.
- Dominguez-Olmedo et al. (2024)

  Dominguez-Olmedo, R., Dorner, F. E., and Hardt, M.
  Training on the test task confounds evaluation and emergence, 2024.
  URL <https://arxiv.org/abs/2407.07890>.
- Elkies (2016)

  Elkies, N. D.
  Is there a way to express an power law decay as a series of exponentials?
  MathOverflow, 2016.
  URL <https://mathoverflow.net/q/251661>.
  URL:https://mathoverflow.net/q/251661 (version: 2016-10-08).
- Eloundou et al. (2023)

  Eloundou, T., Manning, S., Mishkin, P., and Rock, D.
  Gpts are gpts: An early look at the labor market impact potential of large language models, 2023.
  URL <https://arxiv.org/abs/2303.10130>.
- Filipovich et al. (2022)

  Filipovich, M. J., Cappelli, A., Hesslow, D., and Launay, J.
  Scaling laws beyond backpropagation, 2022.
  URL <https://arxiv.org/abs/2210.14593>.
- Gadre et al. (2024)

  Gadre, S. Y., Smyrnis, G., Shankar, V., Gururangan, S., Wortsman, M., Shao, R., Mercat, J., Fang, A., Li, J., Keh, S., et al.
  Language models scale reliably with over-training and on downstream tasks.
  *arXiv preprint arXiv:2403.08540*, 2024.
- Ganguli et al. (2022)

  Ganguli, D., Hernandez, D., Lovitt, L., Askell, A., Bai, Y., Chen, A., Conerly, T., Dassarma, N., Drain, D., Elhage, N., et al.
  Predictability and surprise in large generative models.
  In *2022 ACM Conference on Fairness, Accountability, and Transparency*, pp. 1747–1764, 2022.
- Gao et al. (2023)

  Gao, L., Schulman, J., and Hilton, J.
  Scaling laws for reward model overoptimization.
  In Krause, A., Brunskill, E., Cho, K., Engelhardt, B., Sabato, S., and Scarlett, J. (eds.), *Proceedings of the 40th International Conference on Machine Learning*, volume 202 of *Proceedings of Machine Learning Research*, pp. 10835–10866. PMLR, 23–29 Jul 2023.
  URL <https://proceedings.mlr.press/v202/gao23h.html>.
- Gao et al. (2024)

  Gao, L., la Tour, T. D., Tillman, H., Goh, G., Troll, R., Radford, A., Sutskever, I., Leike, J., and Wu, J.
  Scaling and evaluating sparse autoencoders.
  *arXiv preprint arXiv:2406.04093*, 2024.
- Gerstgrasser et al. (2024)

  Gerstgrasser, M., Schaeffer, R., Dey, A., Rafailov, R., Sleight, H., Hughes, J., Korbak, T., Agrawal, R., Pai, D., Gromov, A., Roberts, D. A., Yang, D., Donoho, D. L., and Koyejo, S.
  Is model collapse inevitable? breaking the curse of recursion by accumulating real and synthetic data, 2024.
  URL <https://arxiv.org/abs/2404.01413>.
- Ghorbani et al. (2021)

  Ghorbani, B., Firat, O., Freitag, M., Bapna, A., Krikun, M., Garcia, X., Chelba, C., and Cherry, C.
  Scaling laws for neural machine translation.
  In *International Conference on Learning Representations*, 2021.
- Gordon et al. (2021)

  Gordon, M. A., Duh, K., and Kaplan, J.
  Data and parameter scaling laws for neural machine translation.
  In Moens, M.-F., Huang, X., Specia, L., and Yih, S. W.-t. (eds.), *Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing*, pp. 5915–5922, Online and Punta Cana, Dominican Republic, November 2021. Association for Computational Linguistics.
  doi: 10.18653/v1/2021.emnlp-main.478.
  URL <https://aclanthology.org/2021.emnlp-main.478>.
- Grattafiori et al. (2024)

  Grattafiori, A., Dubey, A., Jauhri, A., Pandey, A., Kadian, A., Al-Dahle, A., Letman, A., Mathur, A., Schelten, A., Vaughan, A., Yang, A., Fan, A., Goyal, A., Hartshorn, A., Yang, A., Mitra, A., Sravankumar, A., Korenev, A., Hinsvark, A., Rao, A., Zhang, A., Rodriguez, A., Gregerson, A., Spataru, A., Roziere, B., Biron, B., Tang, B., Chern, B., Caucheteux, C., Nayak, C., Bi, C., Marra, C., McConnell, C., Keller, C., Touret, C., Wu, C., Wong, C., Ferrer, C. C., Nikolaidis, C., Allonsius, D., Song, D., Pintz, D., Livshits, D., Wyatt, D., Esiobu, D., Choudhary, D., Mahajan, D., Garcia-Olano, D., Perino, D., Hupkes, D., Lakomkin, E., AlBadawy, E., Lobanova, E., Dinan, E., Smith, E. M., Radenovic, F., Guzmán, F., Zhang, F., Synnaeve, G., Lee, G., Anderson, G. L., Thattai, G., Nail, G., Mialon, G., Pang, G., Cucurell, G., Nguyen, H., Korevaar, H., Xu, H., Touvron, H., Zarov, I., Ibarra, I. A., Kloumann, I., Misra, I., Evtimov, I., Zhang, J., Copet, J., Lee, J., Geffert, J., Vranes, J., Park, J., Mahadeokar, J.,
  Shah, J., van der Linde, J., Billock, J., Hong, J., Lee, J., Fu, J., Chi, J., Huang, J., Liu, J., Wang, J., Yu, J., Bitton, J., Spisak, J., Park, J., Rocca, J., Johnstun, J., Saxe, J., Jia, J., Alwala, K. V., Prasad, K., Upasani, K., Plawiak, K., Li, K., Heafield, K., Stone, K., El-Arini, K., Iyer, K., Malik, K., Chiu, K., Bhalla, K., Lakhotia, K., Rantala-Yeary, L., van der Maaten, L., Chen, L., Tan, L., Jenkins, L., Martin, L., Madaan, L., Malo, L., Blecher, L., Landzaat, L., de Oliveira, L., Muzzi, M., Pasupuleti, M., Singh, M., Paluri, M., Kardas, M., Tsimpoukelli, M., Oldham, M., Rita, M., Pavlova, M., Kambadur, M., Lewis, M., Si, M., Singh, M. K., Hassan, M., Goyal, N., Torabi, N., Bashlykov, N., Bogoychev, N., Chatterji, N., Zhang, N., Duchenne, O., Çelebi, O., Alrassy, P., Zhang, P., Li, P., Vasic, P., Weng, P., Bhargava, P., Dubal, P., Krishnan, P., Koura, P. S., Xu, P., He, Q., Dong, Q., Srinivasan, R., Ganapathy, R., Calderer, R., Cabral, R. S., Stojnic, R., Raileanu, R., Maheswari, R., Girdhar,
  R., Patel, R., Sauvestre, R., Polidoro, R., Sumbaly, R., Taylor, R., Silva, R., Hou, R., Wang, R., Hosseini, S., Chennabasappa, S., Singh, S., Bell, S., Kim, S. S., Edunov, S., Nie, S., Narang, S., Raparthy, S., Shen, S., Wan, S., Bhosale, S., Zhang, S., Vandenhende, S., Batra, S., Whitman, S., Sootla, S., Collot, S., Gururangan, S., Borodinsky, S., Herman, T., Fowler, T., Sheasha, T., Georgiou, T., Scialom, T., Speckbacher, T., Mihaylov, T., Xiao, T., Karn, U., Goswami, V., Gupta, V., Ramanathan, V., Kerkez, V., Gonguet, V., Do, V., Vogeti, V., Albiero, V., Petrovic, V., Chu, W., Xiong, W., Fu, W., Meers, W., Martinet, X., Wang, X., Wang, X., Tan, X. E., Xia, X., Xie, X., Jia, X., Wang, X., Goldschlag, Y., Gaur, Y., Babaei, Y., Wen, Y., Song, Y., Zhang, Y., Li, Y., Mao, Y., Coudert, Z. D., Yan, Z., Chen, Z., Papakipos, Z., Singh, A., Srivastava, A., Jain, A., Kelsey, A., Shajnfeld, A., Gangidi, A., Victoria, A., Goldstand, A., Menon, A., Sharma, A., Boesenberg, A., Baevski, A., Feinstein, A., Kallet, A.,
  Sangani, A., Teo, A., Yunus, A., Lupu, A., Alvarado, A., Caples, A., Gu, A., Ho, A., Poulton, A., Ryan, A., Ramchandani, A., Dong, A., Franco, A., Goyal, A., Saraf, A., Chowdhury, A., Gabriel, A., Bharambe, A., Eisenman, A., Yazdan, A., James, B., Maurer, B., Leonhardi, B., Huang, B., Loyd, B., Paola, B. D., Paranjape, B., Liu, B., Wu, B., Ni, B., Hancock, B., Wasti, B., Spence, B., Stojkovic, B., Gamido, B., Montalvo, B., Parker, C., Burton, C., Mejia, C., Liu, C., Wang, C., Kim, C., Zhou, C., Hu, C., Chu, C.-H., Cai, C., Tindal, C., Feichtenhofer, C., Gao, C., Civin, D., Beaty, D., Kreymer, D., Li, D., Adkins, D., Xu, D., Testuggine, D., David, D., Parikh, D., Liskovich, D., Foss, D., Wang, D., Le, D., Holland, D., Dowling, E., Jamil, E., Montgomery, E., Presani, E., Hahn, E., Wood, E., Le, E.-T., Brinkman, E., Arcaute, E., Dunbar, E., Smothers, E., Sun, F., Kreuk, F., Tian, F., Kokkinos, F., Ozgenel, F., Caggioni, F., Kanayet, F., Seide, F., Florez, G. M., Schwarz, G., Badeer, G., Swee, G., Halpern, G.,
  Herman, G., Sizov, G., Guangyi, Zhang, Lakshminarayanan, G., Inan, H., Shojanazeri, H., Zou, H., Wang, H., Zha, H., Habeeb, H., Rudolph, H., Suk, H., Aspegren, H., Goldman, H., Zhan, H., Damlaj, I., Molybog, I., Tufanov, I., Leontiadis, I., Veliche, I.-E., Gat, I., Weissman, J., Geboski, J., Kohli, J., Lam, J., Asher, J., Gaya, J.-B., Marcus, J., Tang, J., Chan, J., Zhen, J., Reizenstein, J., Teboul, J., Zhong, J., Jin, J., Yang, J., Cummings, J., Carvill, J., Shepard, J., McPhie, J., Torres, J., Ginsburg, J., Wang, J., Wu, K., U, K. H., Saxena, K., Khandelwal, K., Zand, K., Matosich, K., Veeraraghavan, K., Michelena, K., Li, K., Jagadeesh, K., Huang, K., Chawla, K., Huang, K., Chen, L., Garg, L., A, L., Silva, L., Bell, L., Zhang, L., Guo, L., Yu, L., Moshkovich, L., Wehrstedt, L., Khabsa, M., Avalani, M., Bhatt, M., Mankus, M., Hasson, M., Lennie, M., Reso, M., Groshev, M., Naumov, M., Lathi, M., Keneally, M., Liu, M., Seltzer, M. L., Valko, M., Restrepo, M., Patel, M., Vyatskov, M., Samvelyan, M., Clark,
  M., Macey, M., Wang, M., Hermoso, M. J., Metanat, M., Rastegari, M., Bansal, M., Santhanam, N., Parks, N., White, N., Bawa, N., Singhal, N., Egebo, N., Usunier, N., Mehta, N., Laptev, N. P., Dong, N., Cheng, N., Chernoguz, O., Hart, O., Salpekar, O., Kalinli, O., Kent, P., Parekh, P., Saab, P., Balaji, P., Rittner, P., Bontrager, P., Roux, P., Dollar, P., Zvyagina, P., Ratanchandani, P., Yuvraj, P., Liang, Q., Alao, R., Rodriguez, R., Ayub, R., Murthy, R., Nayani, R., Mitra, R., Parthasarathy, R., Li, R., Hogan, R., Battey, R., Wang, R., Howes, R., Rinott, R., Mehta, S., Siby, S., Bondu, S. J., Datta, S., Chugh, S., Hunt, S., Dhillon, S., Sidorov, S., Pan, S., Mahajan, S., Verma, S., Yamamoto, S., Ramaswamy, S., Lindsay, S., Lindsay, S., Feng, S., Lin, S., Zha, S. C., Patil, S., Shankar, S., Zhang, S., Zhang, S., Wang, S., Agarwal, S., Sajuyigbe, S., Chintala, S., Max, S., Chen, S., Kehoe, S., Satterfield, S., Govindaprasad, S., Gupta, S., Deng, S., Cho, S., Virk, S., Subramanian, S., Choudhury, S.,
  Goldman, S., Remez, T., Glaser, T., Best, T., Koehler, T., Robinson, T., Li, T., Zhang, T., Matthews, T., Chou, T., Shaked, T., Vontimitta, V., Ajayi, V., Montanez, V., Mohan, V., Kumar, V. S., Mangla, V., Ionescu, V., Poenaru, V., Mihailescu, V. T., Ivanov, V., Li, W., Wang, W., Jiang, W., Bouaziz, W., Constable, W., Tang, X., Wu, X., Wang, X., Wu, X., Gao, X., Kleinman, Y., Chen, Y., Hu, Y., Jia, Y., Qi, Y., Li, Y., Zhang, Y., Zhang, Y., Adi, Y., Nam, Y., Yu, Wang, Zhao, Y., Hao, Y., Qian, Y., Li, Y., He, Y., Rait, Z., DeVito, Z., Rosnbrick, Z., Wen, Z., Yang, Z., Zhao, Z., and Ma, Z.
  The llama 3 herd of models, 2024.
  URL <https://arxiv.org/abs/2407.21783>.
- Hendrycks et al. (2021)

  Hendrycks, D., Burns, C., Kadavath, S., Arora, A., Basart, S., Tang, E., Song, D., and Steinhardt, J.
  Measuring mathematical problem solving with the math dataset.
  In *Thirty-fifth Conference on Neural Information Processing Systems Datasets and Benchmarks Track (Round 2)*, 2021.
- Henighan et al. (2020)

  Henighan, T., Kaplan, J., Katz, M., Chen, M., Hesse, C., Jackson, J., Jun, H., Brown, T. B., Dhariwal, P., Gray, S., et al.
  Scaling laws for autoregressive generative modeling.
  *arXiv preprint arXiv:2010.14701*, 2020.
- Hernandez et al. (2021)

  Hernandez, D., Kaplan, J., Henighan, T., and McCandlish, S.
  Scaling laws for transfer, 2021.
  URL <https://arxiv.org/abs/2102.01293>.
- Hernandez et al. (2022)

  Hernandez, D., Brown, T., Conerly, T., DasSarma, N., Drain, D., El-Showk, S., Elhage, N., Hatfield-Dodds, Z., Henighan, T., Hume, T., et al.
  Scaling laws and interpretability of learning from repeated data.
  *arXiv preprint arXiv:2205.10487*, 2022.
- Hestness et al. (2017)

  Hestness, J., Narang, S., Ardalani, N., Diamos, G., Jun, H., Kianinejad, H., Patwary, M., Ali, M., Yang, Y., and Zhou, Y.
  Deep learning scaling is predictable, empirically.
  *arXiv preprint arXiv:1712.00409*, 2017.
- Hilton et al. (2023)

  Hilton, J., Tang, J., and Schulman, J.
  Scaling laws for single-agent reinforcement learning, 2023.
  URL <https://arxiv.org/abs/2301.13442>.
- Hoffmann et al. (2022)

  Hoffmann, J., Borgeaud, S., Mensch, A., Buchatskaya, E., Cai, T., Rutherford, E., de Las Casas, D., Hendricks, L. A., Welbl, J., Clark, A., Hennigan, T., Noland, E., Millican, K., van den Driessche, G., Damoc, B., Guy, A., Osindero, S., Simonyan, K., Elsen, E., Rae, J. W., Vinyals, O., and Sifre, L.
  Training compute-optimal large language models, 2022.
  URL <https://arxiv.org/abs/2203.15556>.
- Hu et al. (2024)

  Hu, S., Liu, X., Han, X., Zhang, X., He, C., Zhao, W., Lin, Y., Ding, N., Ou, Z., Zeng, G., Liu, Z., and Sun, M.
  Predicting emergent abilities with infinite resolution evaluation, 2024.
  URL <https://arxiv.org/abs/2310.03262>.
- Hughes et al. (2024)

  Hughes, J., Price, S., Lynch, A., Schaeffer, R., Barez, F., Koyejo, S., Sleight, H., Jones, E., Perez, E., and Sharma, M.
  Best-of-n jailbreaking, 2024.
  URL <https://arxiv.org/abs/2412.03556>.
- Hutter (2021)

  Hutter, M.
  Learning curve theory, 2021.
  URL <https://arxiv.org/abs/2102.04074>.
- Jiang et al. (2024)

  Jiang, M., Liu, K. Z., Zhong, M., Schaeffer, R., Ouyang, S., Han, J., and Koyejo, S.
  Investigating data contamination for pre-training language models, 2024.
  URL <https://arxiv.org/abs/2401.06059>.
- Jones (2021)

  Jones, A. L.
  Scaling scaling laws with board games.
  *arXiv preprint arXiv:2104.03113*, 2021.
- Kalajdzievski (2024)

  Kalajdzievski, D.
  Scaling laws for forgetting when fine-tuning large language models, 2024.
  URL <https://arxiv.org/abs/2401.05605>.
- Kaplan et al. (2020)

  Kaplan, J., McCandlish, S., Henighan, T., Brown, T. B., Chess, B., Child, R., Gray, S., Radford, A., Wu, J., and Amodei, D.
  Scaling laws for neural language models, 2020.
  URL <https://arxiv.org/abs/2001.08361>.
- Kazdan et al. (2024)

  Kazdan, J., Schaeffer, R., Dey, A., Gerstgrasser, M., Rafailov, R., Donoho, D. L., and Koyejo, S.
  Collapse or thrive? perils and promises of synthetic data in a self-generating world, 2024.
  URL <https://arxiv.org/abs/2410.16713>.
- Kudugunta et al. (2023)

  Kudugunta, S., Kusupati, A., Dettmers, T., Chen, K., Dhillon, I., Tsvetkov, Y., Hajishirzi, H., Kakade, S., Farhadi, A., Jain, P., et al.
  Matformer: Nested transformer for elastic inference.
  *arXiv preprint arXiv:2310.07707*, 2023.
- Kulal et al. (2019)

  Kulal, S., Pasupat, P., Chandra, K., Lee, M., Padon, O., Aiken, A., and Liang, P. S.
  Spoc: Search-based pseudocode to code.
  *Advances in Neural Information Processing Systems*, 32, 2019.
- Kumar et al. (2024)

  Kumar, T., Ankner, Z., Spector, B. F., Bordelon, B., Muennighoff, N., Paul, M., Pehlevan, C., Ré, C., and Raghunathan, A.
  Scaling laws for precision.
  *arXiv preprint arXiv:2411.04330*, 2024.
- Liang et al. (2024)

  Liang, Z., He, H., Yang, C., and Dai, B.
  Scaling laws for diffusion transformers, 2024.
  URL <https://arxiv.org/abs/2410.08184>.
- Lin et al. (2024)

  Lin, L., Wu, J., Kakade, S. M., Bartlett, P. L., and Lee, J. D.
  Scaling laws in linear regression: Compute, parameters, and data.
  *arXiv preprint arXiv:2406.08466*, 2024.
- Liu et al. (2024)

  Liu, J., Mao, H., Chen, Z., Zhao, T., Shah, N., and Tang, J.
  Towards neural scaling laws on graphs, 2024.
  URL <https://arxiv.org/abs/2402.02054>.
- Maloney et al. (2022)

  Maloney, A., Roberts, D. A., and Sully, J.
  A solvable model of neural scaling laws.
  *arXiv preprint arXiv:2210.16859*, 2022.
- Maslej et al. (2024)

  Maslej, N., Fattorini, L., Perrault, R., Parli, V., Reuel, A., Brynjolfsson, E., Etchemendy, J., Ligett, K., Lyons, T., Manyika, J., Niebles, J. C., Shoham, Y., Wald, R., and Clark, J.
  Artificial intelligence index report 2024, 2024.
  URL <https://arxiv.org/abs/2405.19522>.
- Mazeika et al. (2024)

  Mazeika, M., Phan, L., Yin, X., Zou, A., Wang, Z., Mu, N., Sakhaee, E., Li, N., Basart, S., Li, B., Forsyth, D., and Hendrycks, D.
  Harmbench: A standardized evaluation framework for automated red teaming and robust refusal, 2024.
  URL <https://arxiv.org/abs/2402.04249>.
- McKenzie et al. (2024)

  McKenzie, I. R., Lyzhov, A., Pieler, M., Parrish, A., Mueller, A., Prabhu, A., McLean, E., Kirtland, A., Ross, A., Liu, A., Gritsevskiy, A., Wurgaft, D., Kauffman, D., Recchia, G., Liu, J., Cavanagh, J., Weiss, M., Huang, S., Droid, T. F., Tseng, T., Korbak, T., Shen, X., Zhang, Y., Zhou, Z., Kim, N., Bowman, S. R., and Perez, E.
  Inverse scaling: When bigger isn’t better, 2024.
  URL <https://arxiv.org/abs/2306.09479>.
- Mei et al. (2024)

  Mei, K., Tu, Z., Delbracio, M., Talebi, H., Patel, V. M., and Milanfar, P.
  Bigger is not always better: Scaling properties of latent diffusion models, 2024.
  URL <https://arxiv.org/abs/2404.01367>.
- Mhaskar (1996)

  Mhaskar, H. N.
  Neural networks for optimal approximation of smooth and analytic functions.
  *Neural computation*, 8(1):164–177, 1996.
- Michaud et al. (2024)

  Michaud, E., Liu, Z., Girit, U., and Tegmark, M.
  The quantization model of neural scaling.
  *Advances in Neural Information Processing Systems*, 36, 2024.
- mpmath development team (2023)

  mpmath development team, T.
  *mpmath: a Python library for arbitrary-precision floating-point arithmetic (version 1.3.0)*, 2023.
  http://mpmath.org/.
- Muennighoff et al. (2023)

  Muennighoff, N., Rush, A., Barak, B., Le Scao, T., Tazi, N., Piktus, A., Pyysalo, S., Wolf, T., and Raffel, C. A.
  Scaling data-constrained language models.
  *Advances in Neural Information Processing Systems*, 36:50358–50376, 2023.
- Neumann & Gros (2022)

  Neumann, O. and Gros, C.
  Scaling laws for a multi-agent reinforcement learning model.
  *arXiv preprint arXiv:2210.00849*, 2022.
- Neumann & Gros (2024)

  Neumann, O. and Gros, C.
  Alphazero neural scaling and zipf’s law: a tale of board games and power laws, 2024.
  URL <https://arxiv.org/abs/2412.11979>.
- OpenAI et al. (2024)

  OpenAI, Achiam, J., Adler, S., Agarwal, S., Ahmad, L., Akkaya, I., Aleman, F. L., Almeida, D., Altenschmidt, J., Altman, S., Anadkat, S., Avila, R., Babuschkin, I., Balaji, S., Balcom, V., Baltescu, P., Bao, H., Bavarian, M., Belgum, J., Bello, I., Berdine, J., Bernadett-Shapiro, G., Berner, C., Bogdonoff, L., Boiko, O., Boyd, M., Brakman, A.-L., Brockman, G., Brooks, T., Brundage, M., Button, K., Cai, T., Campbell, R., Cann, A., Carey, B., Carlson, C., Carmichael, R., Chan, B., Chang, C., Chantzis, F., Chen, D., Chen, S., Chen, R., Chen, J., Chen, M., Chess, B., Cho, C., Chu, C., Chung, H. W., Cummings, D., Currier, J., Dai, Y., Decareaux, C., Degry, T., Deutsch, N., Deville, D., Dhar, A., Dohan, D., Dowling, S., Dunning, S., Ecoffet, A., Eleti, A., Eloundou, T., Farhi, D., Fedus, L., Felix, N., Fishman, S. P., Forte, J., Fulford, I., Gao, L., Georges, E., Gibson, C., Goel, V., Gogineni, T., Goh, G., Gontijo-Lopes, R., Gordon, J., Grafstein, M., Gray, S., Greene, R., Gross, J., Gu, S. S., Guo, Y., Hallacy,
  C., Han, J., Harris, J., He, Y., Heaton, M., Heidecke, J., Hesse, C., Hickey, A., Hickey, W., Hoeschele, P., Houghton, B., Hsu, K., Hu, S., Hu, X., Huizinga, J., Jain, S., Jain, S., Jang, J., Jiang, A., Jiang, R., Jin, H., Jin, D., Jomoto, S., Jonn, B., Jun, H., Kaftan, T., Łukasz Kaiser, Kamali, A., Kanitscheider, I., Keskar, N. S., Khan, T., Kilpatrick, L., Kim, J. W., Kim, C., Kim, Y., Kirchner, J. H., Kiros, J., Knight, M., Kokotajlo, D., Łukasz Kondraciuk, Kondrich, A., Konstantinidis, A., Kosic, K., Krueger, G., Kuo, V., Lampe, M., Lan, I., Lee, T., Leike, J., Leung, J., Levy, D., Li, C. M., Lim, R., Lin, M., Lin, S., Litwin, M., Lopez, T., Lowe, R., Lue, P., Makanju, A., Malfacini, K., Manning, S., Markov, T., Markovski, Y., Martin, B., Mayer, K., Mayne, A., McGrew, B., McKinney, S. M., McLeavey, C., McMillan, P., McNeil, J., Medina, D., Mehta, A., Menick, J., Metz, L., Mishchenko, A., Mishkin, P., Monaco, V., Morikawa, E., Mossing, D., Mu, T., Murati, M., Murk, O., Mély, D., Nair, A., Nakano, R.,
  Nayak, R., Neelakantan, A., Ngo, R., Noh, H., Ouyang, L., O’Keefe, C., Pachocki, J., Paino, A., Palermo, J., Pantuliano, A., Parascandolo, G., Parish, J., Parparita, E., Passos, A., Pavlov, M., Peng, A., Perelman, A., de Avila Belbute Peres, F., Petrov, M., de Oliveira Pinto, H. P., Michael, Pokorny, Pokrass, M., Pong, V. H., Powell, T., Power, A., Power, B., Proehl, E., Puri, R., Radford, A., Rae, J., Ramesh, A., Raymond, C., Real, F., Rimbach, K., Ross, C., Rotsted, B., Roussez, H., Ryder, N., Saltarelli, M., Sanders, T., Santurkar, S., Sastry, G., Schmidt, H., Schnurr, D., Schulman, J., Selsam, D., Sheppard, K., Sherbakov, T., Shieh, J., Shoker, S., Shyam, P., Sidor, S., Sigler, E., Simens, M., Sitkin, J., Slama, K., Sohl, I., Sokolowsky, B., Song, Y., Staudacher, N., Such, F. P., Summers, N., Sutskever, I., Tang, J., Tezak, N., Thompson, M. B., Tillet, P., Tootoonchian, A., Tseng, E., Tuggle, P., Turley, N., Tworek, J., Uribe, J. F. C., Vallone, A., Vijayvergiya, A., Voss, C., Wainwright, C., Wang,
  J. J., Wang, A., Wang, B., Ward, J., Wei, J., Weinmann, C., Welihinda, A., Welinder, P., Weng, J., Weng, L., Wiethoff, M., Willner, D., Winter, C., Wolrich, S., Wong, H., Workman, L., Wu, S., Wu, J., Wu, M., Xiao, K., Xu, T., Yoo, S., Yu, K., Yuan, Q., Zaremba, W., Zellers, R., Zhang, C., Zhang, M., Zhao, S., Zheng, T., Zhuang, J., Zhuk, W., and Zoph, B.
  Gpt-4 technical report, 2024.
  URL <https://arxiv.org/abs/2303.08774>.
- Owen (2024)

  Owen, D.
  How predictable is language model benchmark performance?, 2024.
- Pachocki et al. (2024)

  Pachocki, J., Tworek, J., Fedus, L., Kaiser, L., Chen, M., Sidor, S., and Zaremba, W.
  Learning to reason with LLMs.
  Technical report, OpenAI, September 2024.
  URL <https://openai.com/index/learning-to-reason-with-llms>.
  Contributors include the o1 Contributions team, Core Contributors, and multiple research and safety teams.
- Paquette et al. (2024)

  Paquette, E., Paquette, C., Xiao, L., and Pennington, J.
  4+ 3 phases of compute-optimal neural scaling laws.
  *arXiv preprint arXiv:2405.15074*, 2024.
- Pinkus (1999)

  Pinkus, A.
  Approximation theory of the mlp model in neural networks.
  *Acta numerica*, 8:143–195, 1999.
- Polo et al. (2024)

  Polo, F. M., Somerstep, S., Choshen, L., Sun, Y., and Yurochkin, M.
  Sloth: scaling laws for llm skills to predict multi-benchmark performance across families, 2024.
  URL <https://arxiv.org/abs/2412.06540>.
- Porian et al. (2024)

  Porian, T., Wortsman, M., Jitsev, J., Schmidt, L., and Carmon, Y.
  Resolving discrepancies in compute-optimal scaling of language models, 2024.
  URL <https://arxiv.org/abs/2406.19146>.
- Reuel et al. (2024)

  Reuel, A., Bucknall, B., Casper, S., Fist, T., Soder, L., Aarne, O., Hammond, L., Ibrahim, L., Chan, A., Wills, P., Anderljung, M., Garfinkel, B., Heim, L., Trask, A., Mukobi, G., Schaeffer, R., Baker, M., Hooker, S., Solaiman, I., Luccioni, A. S., Rajkumar, N., Moës, N., Ladish, J., Guha, N., Newman, J., Bengio, Y., South, T., Pentland, A., Koyejo, S., Kochenderfer, M. J., and Trager, R.
  Open problems in technical ai governance, 2024.
  URL <https://arxiv.org/abs/2407.14981>.
- Roberts et al. (2022)

  Roberts, D. A., Yaida, S., and Hanin, B.
  *The principles of deep learning theory*, volume 46.
  Cambridge University Press Cambridge, MA, USA, 2022.
- Romani et al. (2013)

  Romani, S., Pinkoviezky, I., Rubin, A., and Tsodyks, M.
  Scaling laws of associative memory retrieval.
  *Neural computation*, 25(10):2523–2544, 2013.
- Rosenfeld et al. (2020)

  Rosenfeld, J. S., Rosenfeld, A., Belinkov, Y., and Shavit, N.
  A constructive prediction of the generalization error across scales.
  In *International Conference on Learning Representations*, 2020.
- Rosenfeld et al. (2021)

  Rosenfeld, J. S., Frankle, J., Carbin, M., and Shavit, N.
  On the predictability of pruning across scales.
  In Meila, M. and Zhang, T. (eds.), *Proceedings of the 38th International Conference on Machine Learning*, volume 139 of *Proceedings of Machine Learning Research*, pp. 9075–9083. PMLR, 18–24 Jul 2021.
  URL <https://proceedings.mlr.press/v139/rosenfeld21a.html>.
- Ruan et al. (2024)

  Ruan, Y., Maddison, C. J., and Hashimoto, T.
  Observational scaling laws and the predictability of language model performance, 2024.
  URL <https://arxiv.org/abs/2405.10938>.
- Sardana et al. (2023)

  Sardana, N., Portes, J., Doubov, S., and Frankle, J.
  Beyond chinchilla-optimal: Accounting for inference in language model scaling laws.
  In *Forty-first International Conference on Machine Learning*, 2023.
- Schaeffer (2023)

  Schaeffer, R.
  Pretraining on the test set is all you need, 2023.
  URL <https://arxiv.org/abs/2309.08632>.
- Schaeffer et al. (2023)

  Schaeffer, R., Miranda, B., and Koyejo, S.
  Are emergent abilities of large language models a mirage?
  In Oh, A., Naumann, T., Globerson, A., Saenko, K., Hardt, M., and Levine, S. (eds.), *Advances in Neural Information Processing Systems*, volume 36, pp. 55565–55581. Curran Associates, Inc., 2023.
  URL <https://proceedings.neurips.cc/paper_files/paper/2023/file/adc98a266f45005c403b8311ca7e8bd7-Paper-Conference.pdf>.
- Schaeffer et al. (2024a)

  Schaeffer, R., Lecomte, V., Pai, D. B., Carranza, A., Isik, B., Unell, A., Khona, M., Yerxa, T., LeCun, Y., Chung, S., Gromov, A., Shwartz-Ziv, R., and Koyejo, S.
  Towards an improved understanding and utilization of maximum manifold capacity representations, 2024a.
  URL <https://arxiv.org/abs/2406.09366>.
- Schaeffer et al. (2024b)

  Schaeffer, R., Schoelkopf, H., Miranda, B., Mukobi, G., Madan, V., Ibrahim, A., Bradley, H., Biderman, S., and Koyejo, S.
  Why has predicting downstream capabilities of frontier ai models with scale remained elusive?, 2024b.
  URL <https://arxiv.org/abs/2406.04391>.
- Schaeffer et al. (2024c)

  Schaeffer, R., Zahedi, N., Khona, M., Pai, D., Truong, S., Du, Y., Ostrow, M., Chandra, S., Carranza, A., Fiete, I. R., Gromov, A., and Koyejo, S.
  Bridging associative memory and probabilistic modeling, 2024c.
  URL <https://arxiv.org/abs/2402.10202>.
- Sharma & Kaplan (2022)

  Sharma, U. and Kaplan, J.
  Scaling laws from the data manifold dimension.
  *Journal of Machine Learning Research*, 23(9):1–34, 2022.
- Snell et al. (2024a)

  Snell, C., Lee, J., Xu, K., and Kumar, A.
  Scaling llm test-time compute optimally can be more effective than scaling model parameters.
  *arXiv preprint arXiv:2408.03314*, 2024a.
- Snell et al. (2024b)

  Snell, C., Wallace, E., Klein, D., and Levine, S.
  Predicting emergent capabilities by finetuning, 2024b.
  URL <https://arxiv.org/abs/2411.16035>.
- Sorscher et al. (2022)

  Sorscher, B., Geirhos, R., Shekhar, S., Ganguli, S., and Morcos, A.
  Beyond neural scaling laws: beating power law scaling via data pruning.
  *Advances in Neural Information Processing Systems*, 35:19523–19536, 2022.
- Spigler et al. (2020)

  Spigler, S., Geiger, M., and Wyart, M.
  Asymptotic learning curves of kernel methods: empirical data versus teacher–student paradigm.
  *Journal of Statistical Mechanics: Theory and Experiment*, 2020(12):124001, December 2020.
  ISSN 1742-5468.
  doi: 10.1088/1742-5468/abc61d.
  URL <http://dx.doi.org/10.1088/1742-5468/abc61d>.
- Srivastava et al. (2023)

  Srivastava, A., Rastogi, A., Rao, A., Shoeb, A. A. M., Abid, A., Fisch, A., Brown, A. R., Santoro, A., Gupta, A., Garriga-Alonso, A., Kluska, A., Lewkowycz, A., Agarwal, A., Power, A., Ray, A., Warstadt, A., Kocurek, A. W., Safaya, A., Tazarv, A., Xiang, A., Parrish, A., Nie, A., Hussain, A., Askell, A., Dsouza, A., Slone, A., Rahane, A., Iyer, A. S., Andreassen, A., Madotto, A., Santilli, A., Stuhlmüller, A., Dai, A., La, A., Lampinen, A., Zou, A., Jiang, A., Chen, A., Vuong, A., Gupta, A., Gottardi, A., Norelli, A., Venkatesh, A., Gholamidavoodi, A., Tabassum, A., Menezes, A., Kirubarajan, A., Mullokandov, A., Sabharwal, A., Herrick, A., Efrat, A., Erdem, A., Karakaş, A., Roberts, B. R., Loe, B. S., Zoph, B., Bojanowski, B., Özyurt, B., Hedayatnia, B., Neyshabur, B., Inden, B., Stein, B., Ekmekci, B., Lin, B. Y., Howald, B., Orinion, B., Diao, C., Dour, C., Stinson, C., Argueta, C., Ramírez, C. F., Singh, C., Rathkopf, C., Meng, C., Baral, C., Wu, C., Callison-Burch, C., Waites, C., Voigt, C., Manning,
  C. D., Potts, C., Ramirez, C., Rivera, C. E., Siro, C., Raffel, C., Ashcraft, C., Garbacea, C., Sileo, D., Garrette, D., Hendrycks, D., Kilman, D., Roth, D., Freeman, D., Khashabi, D., Levy, D., González, D. M., Perszyk, D., Hernandez, D., Chen, D., Ippolito, D., Gilboa, D., Dohan, D., Drakard, D., Jurgens, D., Datta, D., Ganguli, D., Emelin, D., Kleyko, D., Yuret, D., Chen, D., Tam, D., Hupkes, D., Misra, D., Buzan, D., Mollo, D. C., Yang, D., Lee, D.-H., Schrader, D., Shutova, E., Cubuk, E. D., Segal, E., Hagerman, E., Barnes, E., Donoway, E., Pavlick, E., Rodola, E., Lam, E., Chu, E., Tang, E., Erdem, E., Chang, E., Chi, E. A., Dyer, E., Jerzak, E., Kim, E., Manyasi, E. E., Zheltonozhskii, E., Xia, F., Siar, F., Martínez-Plumed, F., Happé, F., Chollet, F., Rong, F., Mishra, G., Winata, G. I., de Melo, G., Kruszewski, G., Parascandolo, G., Mariani, G., Wang, G., Jaimovitch-López, G., Betz, G., Gur-Ari, G., Galijasevic, H., Kim, H., Rashkin, H., Hajishirzi, H., Mehta, H., Bogar, H., Shevlin, H.,
  Schütze, H., Yakura, H., Zhang, H., Wong, H. M., Ng, I., Noble, I., Jumelet, J., Geissinger, J., Kernion, J., Hilton, J., Lee, J., Fisac, J. F., Simon, J. B., Koppel, J., Zheng, J., Zou, J., Kocoń, J., Thompson, J., Wingfield, J., Kaplan, J., Radom, J., Sohl-Dickstein, J., Phang, J., Wei, J., Yosinski, J., Novikova, J., Bosscher, J., Marsh, J., Kim, J., Taal, J., Engel, J., Alabi, J., Xu, J., Song, J., Tang, J., Waweru, J., Burden, J., Miller, J., Balis, J. U., Batchelder, J., Berant, J., Frohberg, J., Rozen, J., Hernandez-Orallo, J., Boudeman, J., Guerr, J., Jones, J., Tenenbaum, J. B., Rule, J. S., Chua, J., Kanclerz, K., Livescu, K., Krauth, K., Gopalakrishnan, K., Ignatyeva, K., Markert, K., Dhole, K. D., Gimpel, K., Omondi, K., Mathewson, K., Chiafullo, K., Shkaruta, K., Shridhar, K., McDonell, K., Richardson, K., Reynolds, L., Gao, L., Zhang, L., Dugan, L., Qin, L., Contreras-Ochando, L., Morency, L.-P., Moschella, L., Lam, L., Noble, L., Schmidt, L., He, L., Colón, L. O., Metz, L., Şenel, L. K.,
  Bosma, M., Sap, M., ter Hoeve, M., Farooqi, M., Faruqui, M., Mazeika, M., Baturan, M., Marelli, M., Maru, M., Quintana, M. J. R., Tolkiehn, M., Giulianelli, M., Lewis, M., Potthast, M., Leavitt, M. L., Hagen, M., Schubert, M., Baitemirova, M. O., Arnaud, M., McElrath, M., Yee, M. A., Cohen, M., Gu, M., Ivanitskiy, M., Starritt, M., Strube, M., Swędrowski, M., Bevilacqua, M., Yasunaga, M., Kale, M., Cain, M., Xu, M., Suzgun, M., Walker, M., Tiwari, M., Bansal, M., Aminnaseri, M., Geva, M., Gheini, M., T, M. V., Peng, N., Chi, N. A., Lee, N., Krakover, N. G.-A., Cameron, N., Roberts, N., Doiron, N., Martinez, N., Nangia, N., Deckers, N., Muennighoff, N., Keskar, N. S., Iyer, N. S., Constant, N., Fiedel, N., Wen, N., Zhang, O., Agha, O., Elbaghdadi, O., Levy, O., Evans, O., Casares, P. A. M., Doshi, P., Fung, P., Liang, P. P., Vicol, P., Alipoormolabashi, P., Liao, P., Liang, P., Chang, P., Eckersley, P., Htut, P. M., Hwang, P., Miłkowski, P., Patil, P., Pezeshkpour, P., Oli, P., Mei, Q., Lyu, Q., Chen, Q.,
  Banjade, R., Rudolph, R. E., Gabriel, R., Habacker, R., Risco, R., Millière, R., Garg, R., Barnes, R., Saurous, R. A., Arakawa, R., Raymaekers, R., Frank, R., Sikand, R., Novak, R., Sitelew, R., LeBras, R., Liu, R., Jacobs, R., Zhang, R., Salakhutdinov, R., Chi, R., Lee, R., Stovall, R., Teehan, R., Yang, R., Singh, S., Mohammad, S. M., Anand, S., Dillavou, S., Shleifer, S., Wiseman, S., Gruetter, S., Bowman, S. R., Schoenholz, S. S., Han, S., Kwatra, S., Rous, S. A., Ghazarian, S., Ghosh, S., Casey, S., Bischoff, S., Gehrmann, S., Schuster, S., Sadeghi, S., Hamdan, S., Zhou, S., Srivastava, S., Shi, S., Singh, S., Asaadi, S., Gu, S. S., Pachchigar, S., Toshniwal, S., Upadhyay, S., Shyamolima, Debnath, Shakeri, S., Thormeyer, S., Melzi, S., Reddy, S., Makini, S. P., Lee, S.-H., Torene, S., Hatwar, S., Dehaene, S., Divic, S., Ermon, S., Biderman, S., Lin, S., Prasad, S., Piantadosi, S. T., Shieber, S. M., Misherghi, S., Kiritchenko, S., Mishra, S., Linzen, T., Schuster, T., Li, T., Yu, T., Ali, T.,
  Hashimoto, T., Wu, T.-L., Desbordes, T., Rothschild, T., Phan, T., Wang, T., Nkinyili, T., Schick, T., Kornev, T., Tunduny, T., Gerstenberg, T., Chang, T., Neeraj, T., Khot, T., Shultz, T., Shaham, U., Misra, V., Demberg, V., Nyamai, V., Raunak, V., Ramasesh, V., Prabhu, V. U., Padmakumar, V., Srikumar, V., Fedus, W., Saunders, W., Zhang, W., Vossen, W., Ren, X., Tong, X., Zhao, X., Wu, X., Shen, X., Yaghoobzadeh, Y., Lakretz, Y., Song, Y., Bahri, Y., Choi, Y., Yang, Y., Hao, Y., Chen, Y., Belinkov, Y., Hou, Y., Hou, Y., Bai, Y., Seid, Z., Zhao, Z., Wang, Z., Wang, Z. J., Wang, Z., and Wu, Z.
  Beyond the imitation game: Quantifying and extrapolating the capabilities of language models, 2023.
  URL <https://arxiv.org/abs/2206.04615>.
- Sun et al. (2025)

  Sun, X., Li, S., Xie, R., Han, W., Wu, K., Yang, Z., Li, Y., Wang, A., Li, S., Xue, J., Cheng, Y., Tao, Y., Kang, Z., Xu, C., Wang, D., and Jiang, J.
  Scaling laws for floating point quantization training, 2025.
  URL <https://arxiv.org/abs/2501.02423>.
- Tao et al. (2024)

  Tao, C., Liu, Q., Dou, L., Muennighoff, N., Wan, Z., Luo, P., Lin, M., and Wong, N.
  Scaling laws with vocabulary: Larger models deserve larger vocabularies.
  *arXiv preprint arXiv:2407.13623*, 2024.
- Tay et al. (2021)

  Tay, Y., Dehghani, M., Rao, J., Fedus, W., Abnar, S., Chung, H. W., Narang, S., Yogatama, D., Vaswani, A., and Metzler, D.
  Scale efficiently: Insights from pre-training and fine-tuning transformers.
  *arXiv preprint arXiv:2109.10686*, 2021.
- Tay et al. (2022a)

  Tay, Y., Dehghani, M., Abnar, S., Chung, H. W., Fedus, W., Rao, J., Narang, S., Tran, V. Q., Yogatama, D., and Metzler, D.
  Scaling laws vs model architectures: How does inductive bias influence scaling?
  In *The 2023 Conference on Empirical Methods in Natural Language Processing*, 2022a.
- Tay et al. (2022b)

  Tay, Y., Wei, J., Chung, H. W., Tran, V. Q., So, D. R., Shakeri, S., Garcia, X., Zheng, H. S., Rao, J., Chowdhery, A., Zhou, D., Metzler, D., Petrov, S., Houlsby, N., Le, Q. V., and Dehghani, M.
  Transcending scaling laws with 0.1
  URL <https://arxiv.org/abs/2210.11399>.
- Team et al. (2024a)

  Team, G., Anil, R., Borgeaud, S., Alayrac, J.-B., Yu, J., Soricut, R., Schalkwyk, J., Dai, A. M., Hauth, A., Millican, K., Silver, D., Johnson, M., Antonoglou, I., Schrittwieser, J., Glaese, A., Chen, J., Pitler, E., Lillicrap, T., Lazaridou, A., Firat, O., Molloy, J., Isard, M., Barham, P. R., Hennigan, T., Lee, B., Viola, F., Reynolds, M., Xu, Y., Doherty, R., Collins, E., Meyer, C., Rutherford, E., Moreira, E., Ayoub, K., Goel, M., Krawczyk, J., Du, C., Chi, E., Cheng, H.-T., Ni, E., Shah, P., Kane, P., Chan, B., Faruqui, M., Severyn, A., Lin, H., Li, Y., Cheng, Y., Ittycheriah, A., Mahdieh, M., Chen, M., Sun, P., Tran, D., Bagri, S., Lakshminarayanan, B., Liu, J., Orban, A., Güra, F., Zhou, H., Song, X., Boffy, A., Ganapathy, H., Zheng, S., Choe, H., Ágoston Weisz, Zhu, T., Lu, Y., Gopal, S., Kahn, J., Kula, M., Pitman, J., Shah, R., Taropa, E., Merey, M. A., Baeuml, M., Chen, Z., Shafey, L. E., Zhang, Y., Sercinoglu, O., Tucker, G., Piqueras, E., Krikun, M., Barr, I., Savinov, N., Danihelka, I.,
  Roelofs, B., White, A., Andreassen, A., von Glehn, T., Yagati, L., Kazemi, M., Gonzalez, L., Khalman, M., Sygnowski, J., Frechette, A., Smith, C., Culp, L., Proleev, L., Luan, Y., Chen, X., Lottes, J., Schucher, N., Lebron, F., Rrustemi, A., Clay, N., Crone, P., Kocisky, T., Zhao, J., Perz, B., Yu, D., Howard, H., Bloniarz, A., Rae, J. W., Lu, H., Sifre, L., Maggioni, M., Alcober, F., Garrette, D., Barnes, M., Thakoor, S., Austin, J., Barth-Maron, G., Wong, W., Joshi, R., Chaabouni, R., Fatiha, D., Ahuja, A., Tomar, G. S., Senter, E., Chadwick, M., Kornakov, I., Attaluri, N., Iturrate, I., Liu, R., Li, Y., Cogan, S., Chen, J., Jia, C., Gu, C., Zhang, Q., Grimstad, J., Hartman, A. J., Garcia, X., Pillai, T. S., Devlin, J., Laskin, M., de Las Casas, D., Valter, D., Tao, C., Blanco, L., Badia, A. P., Reitter, D., Chen, M., Brennan, J., Rivera, C., Brin, S., Iqbal, S., Surita, G., Labanowski, J., Rao, A., Winkler, S., Parisotto, E., Gu, Y., Olszewska, K., Addanki, R., Miech, A., Louis, A., Teplyashin, D.,
  Brown, G., Catt, E., Balaguer, J., Xiang, J., Wang, P., Ashwood, Z., Briukhov, A., Webson, A., Ganapathy, S., Sanghavi, S., Kannan, A., Chang, M.-W., Stjerngren, A., Djolonga, J., Sun, Y., Bapna, A., Aitchison, M., Pejman, P., Michalewski, H., Yu, T., Wang, C., Love, J., Ahn, J., Bloxwich, D., Han, K., Humphreys, P., Sellam, T., Bradbury, J., Godbole, V., Samangooei, S., Damoc, B., Kaskasoli, A., Arnold, S. M. R., Vasudevan, V., Agrawal, S., Riesa, J., Lepikhin, D., Tanburn, R., Srinivasan, S., Lim, H., Hodkinson, S., Shyam, P., Ferret, J., Hand, S., Garg, A., Paine, T. L., Li, J., Li, Y., Giang, M., Neitz, A., Abbas, Z., York, S., Reid, M., Cole, E., Chowdhery, A., Das, D., Rogozińska, D., Nikolaev, V., Sprechmann, P., Nado, Z., Zilka, L., Prost, F., He, L., Monteiro, M., Mishra, G., Welty, C., Newlan, J., Jia, D., Allamanis, M., Hu, C. H., de Liedekerke, R., Gilmer, J., Saroufim, C., Rijhwani, S., Hou, S., Shrivastava, D., Baddepudi, A., Goldin, A., Ozturel, A., Cassirer, A., Xu, Y., Sohn, D., Sachan,
  D., Amplayo, R. K., Swanson, C., Petrova, D., Narayan, S., Guez, A., Brahma, S., Landon, J., Patel, M., Zhao, R., Villela, K., Wang, L., Jia, W., Rahtz, M., Giménez, M., Yeung, L., Keeling, J., Georgiev, P., Mincu, D., Wu, B., Haykal, S., Saputro, R., Vodrahalli, K., Qin, J., Cankara, Z., Sharma, A., Fernando, N., Hawkins, W., Neyshabur, B., Kim, S., Hutter, A., Agrawal, P., Castro-Ros, A., van den Driessche, G., Wang, T., Yang, F., yiin Chang, S., Komarek, P., McIlroy, R., Lučić, M., Zhang, G., Farhan, W., Sharman, M., Natsev, P., Michel, P., Bansal, Y., Qiao, S., Cao, K., Shakeri, S., Butterfield, C., Chung, J., Rubenstein, P. K., Agrawal, S., Mensch, A., Soparkar, K., Lenc, K., Chung, T., Pope, A., Maggiore, L., Kay, J., Jhakra, P., Wang, S., Maynez, J., Phuong, M., Tobin, T., Tacchetti, A., Trebacz, M., Robinson, K., Katariya, Y., Riedel, S., Bailey, P., Xiao, K., Ghelani, N., Aroyo, L., Slone, A., Houlsby, N., Xiong, X., Yang, Z., Gribovskaya, E., Adler, J., Wirth, M., Lee, L., Li, M., Kagohara, T.,
  Pavagadhi, J., Bridgers, S., Bortsova, A., Ghemawat, S., Ahmed, Z., Liu, T., Powell, R., Bolina, V., Iinuma, M., Zablotskaia, P., Besley, J., Chung, D.-W., Dozat, T., Comanescu, R., Si, X., Greer, J., Su, G., Polacek, M., Kaufman, R. L., Tokumine, S., Hu, H., Buchatskaya, E., Miao, Y., Elhawaty, M., Siddhant, A., Tomasev, N., Xing, J., Greer, C., Miller, H., Ashraf, S., Roy, A., Zhang, Z., Ma, A., Filos, A., Besta, M., Blevins, R., Klimenko, T., Yeh, C.-K., Changpinyo, S., Mu, J., Chang, O., Pajarskas, M., Muir, C., Cohen, V., Lan, C. L., Haridasan, K., Marathe, A., Hansen, S., Douglas, S., Samuel, R., Wang, M., Austin, S., Lan, C., Jiang, J., Chiu, J., Lorenzo, J. A., Sjösund, L. L., Cevey, S., Gleicher, Z., Avrahami, T., Boral, A., Srinivasan, H., Selo, V., May, R., Aisopos, K., Hussenot, L., Soares, L. B., Baumli, K., Chang, M. B., Recasens, A., Caine, B., Pritzel, A., Pavetic, F., Pardo, F., Gergely, A., Frye, J., Ramasesh, V., Horgan, D., Badola, K., Kassner, N., Roy, S., Dyer, E., Campos, V. C.,
  Tomala, A., Tang, Y., Badawy, D. E., White, E., Mustafa, B., Lang, O., Jindal, A., Vikram, S., Gong, Z., Caelles, S., Hemsley, R., Thornton, G., Feng, F., Stokowiec, W., Zheng, C., Thacker, P., Çağlar Ünlü, Zhang, Z., Saleh, M., Svensson, J., Bileschi, M., Patil, P., Anand, A., Ring, R., Tsihlas, K., Vezer, A., Selvi, M., Shevlane, T., Rodriguez, M., Kwiatkowski, T., Daruki, S., Rong, K., Dafoe, A., FitzGerald, N., Gu-Lemberg, K., Khan, M., Hendricks, L. A., Pellat, M., Feinberg, V., Cobon-Kerr, J., Sainath, T., Rauh, M., Hashemi, S. H., Ives, R., Hasson, Y., Noland, E., Cao, Y., Byrd, N., Hou, L., Wang, Q., Sottiaux, T., Paganini, M., Lespiau, J.-B., Moufarek, A., Hassan, S., Shivakumar, K., van Amersfoort, J., Mandhane, A., Joshi, P., Goyal, A., Tung, M., Brock, A., Sheahan, H., Misra, V., Li, C., Rakićević, N., Dehghani, M., Liu, F., Mittal, S., Oh, J., Noury, S., Sezener, E., Huot, F., Lamm, M., Cao, N. D., Chen, C., Mudgal, S., Stella, R., Brooks, K., Vasudevan, G., Liu, C., Chain, M., Melinkeri,
  N., Cohen, A., Wang, V., Seymore, K., Zubkov, S., Goel, R., Yue, S., Krishnakumaran, S., Albert, B., Hurley, N., Sano, M., Mohananey, A., Joughin, J., Filonov, E., Kepa, T., Eldawy, Y., Lim, J., Rishi, R., Badiezadegan, S., Bos, T., Chang, J., Jain, S., Padmanabhan, S. G. S., Puttagunta, S., Krishna, K., Baker, L., Kalb, N., Bedapudi, V., Kurzrok, A., Lei, S., Yu, A., Litvin, O., Zhou, X., Wu, Z., Sobell, S., Siciliano, A., Papir, A., Neale, R., Bragagnolo, J., Toor, T., Chen, T., Anklin, V., Wang, F., Feng, R., Gholami, M., Ling, K., Liu, L., Walter, J., Moghaddam, H., Kishore, A., Adamek, J., Mercado, T., Mallinson, J., Wandekar, S., Cagle, S., Ofek, E., Garrido, G., Lombriser, C., Mukha, M., Sun, B., Mohammad, H. R., Matak, J., Qian, Y., Peswani, V., Janus, P., Yuan, Q., Schelin, L., David, O., Garg, A., He, Y., Duzhyi, O., Älgmyr, A., Lottaz, T., Li, Q., Yadav, V., Xu, L., Chinien, A., Shivanna, R., Chuklin, A., Li, J., Spadine, C., Wolfe, T., Mohamed, K., Das, S., Dai, Z., He, K., von Dincklage, D.,
  Upadhyay, S., Maurya, A., Chi, L., Krause, S., Salama, K., Rabinovitch, P. G., M, P. K. R., Selvan, A., Dektiarev, M., Ghiasi, G., Guven, E., Gupta, H., Liu, B., Sharma, D., Shtacher, I. H., Paul, S., Akerlund, O., Aubet, F.-X., Huang, T., Zhu, C., Zhu, E., Teixeira, E., Fritze, M., Bertolini, F., Marinescu, L.-E., Bölle, M., Paulus, D., Gupta, K., Latkar, T., Chang, M., Sanders, J., Wilson, R., Wu, X., Tan, Y.-X., Thiet, L. N., Doshi, T., Lall, S., Mishra, S., Chen, W., Luong, T., Benjamin, S., Lee, J., Andrejczuk, E., Rabiej, D., Ranjan, V., Styrc, K., Yin, P., Simon, J., Harriott, M. R., Bansal, M., Robsky, A., Bacon, G., Greene, D., Mirylenka, D., Zhou, C., Sarvana, O., Goyal, A., Andermatt, S., Siegler, P., Horn, B., Israel, A., Pongetti, F., Chen, C.-W. L., Selvatici, M., Silva, P., Wang, K., Tolins, J., Guu, K., Yogev, R., Cai, X., Agostini, A., Shah, M., Nguyen, H., Donnaile, N. O., Pereira, S., Friso, L., Stambler, A., Kurzrok, A., Kuang, C., Romanikhin, Y., Geller, M., Yan, Z., Jang, K., Lee,
  C.-C., Fica, W., Malmi, E., Tan, Q., Banica, D., Balle, D., Pham, R., Huang, Y., Avram, D., Shi, H., Singh, J., Hidey, C., Ahuja, N., Saxena, P., Dooley, D., Potharaju, S. P., O’Neill, E., Gokulchandran, A., Foley, R., Zhao, K., Dusenberry, M., Liu, Y., Mehta, P., Kotikalapudi, R., Safranek-Shrader, C., Goodman, A., Kessinger, J., Globen, E., Kolhar, P., Gorgolewski, C., Ibrahim, A., Song, Y., Eichenbaum, A., Brovelli, T., Potluri, S., Lahoti, P., Baetu, C., Ghorbani, A., Chen, C., Crawford, A., Pal, S., Sridhar, M., Gurita, P., Mujika, A., Petrovski, I., Cedoz, P.-L., Li, C., Chen, S., Santo, N. D., Goyal, S., Punjabi, J., Kappaganthu, K., Kwak, C., LV, P., Velury, S., Choudhury, H., Hall, J., Shah, P., Figueira, R., Thomas, M., Lu, M., Zhou, T., Kumar, C., Jurdi, T., Chikkerur, S., Ma, Y., Yu, A., Kwak, S., Ähdel, V., Rajayogam, S., Choma, T., Liu, F., Barua, A., Ji, C., Park, J. H., Hellendoorn, V., Bailey, A., Bilal, T., Zhou, H., Khatir, M., Sutton, C., Rzadkowski, W., Macintosh, F., Shagin, K.,
  Medina, P., Liang, C., Zhou, J., Shah, P., Bi, Y., Dankovics, A., Banga, S., Lehmann, S., Bredesen, M., Lin, Z., Hoffmann, J. E., Lai, J., Chung, R., Yang, K., Balani, N., Bražinskas, A., Sozanschi, A., Hayes, M., Alcalde, H. F., Makarov, P., Chen, W., Stella, A., Snijders, L., Mandl, M., Kärrman, A., Nowak, P., Wu, X., Dyck, A., Vaidyanathan, K., R, R., Mallet, J., Rudominer, M., Johnston, E., Mittal, S., Udathu, A., Christensen, J., Verma, V., Irving, Z., Santucci, A., Elsayed, G., Davoodi, E., Georgiev, M., Tenney, I., Hua, N., Cideron, G., Leurent, E., Alnahlawi, M., Georgescu, I., Wei, N., Zheng, I., Scandinaro, D., Jiang, H., Snoek, J., Sundararajan, M., Wang, X., Ontiveros, Z., Karo, I., Cole, J., Rajashekhar, V., Tumeh, L., Ben-David, E., Jain, R., Uesato, J., Datta, R., Bunyan, O., Wu, S., Zhang, J., Stanczyk, P., Zhang, Y., Steiner, D., Naskar, S., Azzam, M., Johnson, M., Paszke, A., Chiu, C.-C., Elias, J. S., Mohiuddin, A., Muhammad, F., Miao, J., Lee, A., Vieillard, N., Park, J., Zhang, J.,
  Stanway, J., Garmon, D., Karmarkar, A., Dong, Z., Lee, J., Kumar, A., Zhou, L., Evens, J., Isaac, W., Irving, G., Loper, E., Fink, M., Arkatkar, I., Chen, N., Shafran, I., Petrychenko, I., Chen, Z., Jia, J., Levskaya, A., Zhu, Z., Grabowski, P., Mao, Y., Magni, A., Yao, K., Snaider, J., Casagrande, N., Palmer, E., Suganthan, P., Castaño, A., Giannoumis, I., Kim, W., Rybiński, M., Sreevatsa, A., Prendki, J., Soergel, D., Goedeckemeyer, A., Gierke, W., Jafari, M., Gaba, M., Wiesner, J., Wright, D. G., Wei, Y., Vashisht, H., Kulizhskaya, Y., Hoover, J., Le, M., Li, L., Iwuanyanwu, C., Liu, L., Ramirez, K., Khorlin, A., Cui, A., LIN, T., Wu, M., Aguilar, R., Pallo, K., Chakladar, A., Perng, G., Abellan, E. A., Zhang, M., Dasgupta, I., Kushman, N., Penchev, I., Repina, A., Wu, X., van der Weide, T., Ponnapalli, P., Kaplan, C., Simsa, J., Li, S., Dousse, O., Yang, F., Piper, J., Ie, N., Pasumarthi, R., Lintz, N., Vijayakumar, A., Andor, D., Valenzuela, P., Lui, M., Paduraru, C., Peng, D., Lee, K., Zhang, S.,
  Greene, S., Nguyen, D. D., Kurylowicz, P., Hardin, C., Dixon, L., Janzer, L., Choo, K., Feng, Z., Zhang, B., Singhal, A., Du, D., McKinnon, D., Antropova, N., Bolukbasi, T., Keller, O., Reid, D., Finchelstein, D., Raad, M. A., Crocker, R., Hawkins, P., Dadashi, R., Gaffney, C., Franko, K., Bulanova, A., Leblond, R., Chung, S., Askham, H., Cobo, L. C., Xu, K., Fischer, F., Xu, J., Sorokin, C., Alberti, C., Lin, C.-C., Evans, C., Dimitriev, A., Forbes, H., Banarse, D., Tung, Z., Omernick, M., Bishop, C., Sterneck, R., Jain, R., Xia, J., Amid, E., Piccinno, F., Wang, X., Banzal, P., Mankowitz, D. J., Polozov, A., Krakovna, V., Brown, S., Bateni, M., Duan, D., Firoiu, V., Thotakuri, M., Natan, T., Geist, M., tan Girgin, S., Li, H., Ye, J., Roval, O., Tojo, R., Kwong, M., Lee-Thorp, J., Yew, C., Sinopalnikov, D., Ramos, S., Mellor, J., Sharma, A., Wu, K., Miller, D., Sonnerat, N., Vnukov, D., Greig, R., Beattie, J., Caveness, E., Bai, L., Eisenschlos, J., Korchemniy, A., Tsai, T., Jasarevic, M., Kong, W., Dao,
  P., Zheng, Z., Liu, F., Yang, F., Zhu, R., Teh, T. H., Sanmiya, J., Gladchenko, E., Trdin, N., Toyama, D., Rosen, E., Tavakkol, S., Xue, L., Elkind, C., Woodman, O., Carpenter, J., Papamakarios, G., Kemp, R., Kafle, S., Grunina, T., Sinha, R., Talbert, A., Wu, D., Owusu-Afriyie, D., Du, C., Thornton, C., Pont-Tuset, J., Narayana, P., Li, J., Fatehi, S., Wieting, J., Ajmeri, O., Uria, B., Ko, Y., Knight, L., Héliou, A., Niu, N., Gu, S., Pang, C., Li, Y., Levine, N., Stolovich, A., Santamaria-Fernandez, R., Goenka, S., Yustalim, W., Strudel, R., Elqursh, A., Deck, C., Lee, H., Li, Z., Levin, K., Hoffmann, R., Holtmann-Rice, D., Bachem, O., Arora, S., Koh, C., Yeganeh, S. H., Põder, S., Tariq, M., Sun, Y., Ionita, L., Seyedhosseini, M., Tafti, P., Liu, Z., Gulati, A., Liu, J., Ye, X., Chrzaszcz, B., Wang, L., Sethi, N., Li, T., Brown, B., Singh, S., Fan, W., Parisi, A., Stanton, J., Koverkathu, V., Choquette-Choo, C. A., Li, Y., Lu, T., Ittycheriah, A., Shroff, P., Varadarajan, M., Bahargam, S., Willoughby,
  R., Gaddy, D., Desjardins, G., Cornero, M., Robenek, B., Mittal, B., Albrecht, B., Shenoy, A., Moiseev, F., Jacobsson, H., Ghaffarkhah, A., Rivière, M., Walton, A., Crepy, C., Parrish, A., Zhou, Z., Farabet, C., Radebaugh, C., Srinivasan, P., van der Salm, C., Fidjeland, A., Scellato, S., Latorre-Chimoto, E., Klimczak-Plucińska, H., Bridson, D., de Cesare, D., Hudson, T., Mendolicchio, P., Walker, L., Morris, A., Mauger, M., Guseynov, A., Reid, A., Odoom, S., Loher, L., Cotruta, V., Yenugula, M., Grewe, D., Petrushkina, A., Duerig, T., Sanchez, A., Yadlowsky, S., Shen, A., Globerson, A., Webb, L., Dua, S., Li, D., Bhupatiraju, S., Hurt, D., Qureshi, H., Agarwal, A., Shani, T., Eyal, M., Khare, A., Belle, S. R., Wang, L., Tekur, C., Kale, M. S., Wei, J., Sang, R., Saeta, B., Liechty, T., Sun, Y., Zhao, Y., Lee, S., Nayak, P., Fritz, D., Vuyyuru, M. R., Aslanides, J., Vyas, N., Wicke, M., Ma, X., Eltyshev, E., Martin, N., Cate, H., Manyika, J., Amiri, K., Kim, Y., Xiong, X., Kang, K., Luisier, F.,
  Tripuraneni, N., Madras, D., Guo, M., Waters, A., Wang, O., Ainslie, J., Baldridge, J., Zhang, H., Pruthi, G., Bauer, J., Yang, F., Mansour, R., Gelman, J., Xu, Y., Polovets, G., Liu, J., Cai, H., Chen, W., Sheng, X., Xue, E., Ozair, S., Angermueller, C., Li, X., Sinha, A., Wang, W., Wiesinger, J., Koukoumidis, E., Tian, Y., Iyer, A., Gurumurthy, M., Goldenson, M., Shah, P., Blake, M., Yu, H., Urbanowicz, A., Palomaki, J., Fernando, C., Durden, K., Mehta, H., Momchev, N., Rahimtoroghi, E., Georgaki, M., Raul, A., Ruder, S., Redshaw, M., Lee, J., Zhou, D., Jalan, K., Li, D., Hechtman, B., Schuh, P., Nasr, M., Milan, K., Mikulik, V., Franco, J., Green, T., Nguyen, N., Kelley, J., Mahendru, A., Hu, A., Howland, J., Vargas, B., Hui, J., Bansal, K., Rao, V., Ghiya, R., Wang, E., Ye, K., Sarr, J. M., Preston, M. M., Elish, M., Li, S., Kaku, A., Gupta, J., Pasupat, I., Juan, D.-C., Someswar, M., M., T., Chen, X., Amini, A., Fabrikant, A., Chu, E., Dong, X., Muthal, A., Buthpitiya, S., Jauhari, S., Hua, N.,
  Khandelwal, U., Hitron, A., Ren, J., Rinaldi, L., Drath, S., Dabush, A., Jiang, N.-J., Godhia, H., Sachs, U., Chen, A., Fan, Y., Taitelbaum, H., Noga, H., Dai, Z., Wang, J., Liang, C., Hamer, J., Ferng, C.-S., Elkind, C., Atias, A., Lee, P., Listík, V., Carlen, M., van de Kerkhof, J., Pikus, M., Zaher, K., Müller, P., Zykova, S., Stefanec, R., Gatsko, V., Hirnschall, C., Sethi, A., Xu, X. F., Ahuja, C., Tsai, B., Stefanoiu, A., Feng, B., Dhandhania, K., Katyal, M., Gupta, A., Parulekar, A., Pitta, D., Zhao, J., Bhatia, V., Bhavnani, Y., Alhadlaq, O., Li, X., Danenberg, P., Tu, D., Pine, A., Filippova, V., Ghosh, A., Limonchik, B., Urala, B., Lanka, C. K., Clive, D., Sun, Y., Li, E., Wu, H., Hongtongsak, K., Li, I., Thakkar, K., Omarov, K., Majmundar, K., Alverson, M., Kucharski, M., Patel, M., Jain, M., Zabelin, M., Pelagatti, P., Kohli, R., Kumar, S., Kim, J., Sankar, S., Shah, V., Ramachandruni, L., Zeng, X., Bariach, B., Weidinger, L., Vu, T., Andreev, A., He, A., Hui, K., Kashem, S., Subramanya, A.,
  Hsiao, S., Hassabis, D., Kavukcuoglu, K., Sadovsky, A., Le, Q., Strohman, T., Wu, Y., Petrov, S., Dean, J., and Vinyals, O.
  Gemini: A family of highly capable multimodal models, 2024a.
  URL <https://arxiv.org/abs/2312.11805>.
- Team et al. (2024b)

  Team, G., Georgiev, P., Lei, V. I., Burnell, R., Bai, L., Gulati, A., Tanzer, G., Vincent, D., Pan, Z., Wang, S., Mariooryad, S., Ding, Y., Geng, X., Alcober, F., Frostig, R., Omernick, M., Walker, L., Paduraru, C., Sorokin, C., Tacchetti, A., Gaffney, C., Daruki, S., Sercinoglu, O., Gleicher, Z., Love, J., Voigtlaender, P., Jain, R., Surita, G., Mohamed, K., Blevins, R., Ahn, J., Zhu, T., Kawintiranon, K., Firat, O., Gu, Y., Zhang, Y., Rahtz, M., Faruqui, M., Clay, N., Gilmer, J., Co-Reyes, J., Penchev, I., Zhu, R., Morioka, N., Hui, K., Haridasan, K., Campos, V., Mahdieh, M., Guo, M., Hassan, S., Kilgour, K., Vezer, A., Cheng, H.-T., de Liedekerke, R., Goyal, S., Barham, P., Strouse, D., Noury, S., Adler, J., Sundararajan, M., Vikram, S., Lepikhin, D., Paganini, M., Garcia, X., Yang, F., Valter, D., Trebacz, M., Vodrahalli, K., Asawaroengchai, C., Ring, R., Kalb, N., Soares, L. B., Brahma, S., Steiner, D., Yu, T., Mentzer, F., He, A., Gonzalez, L., Xu, B., Kaufman, R. L., Shafey, L. E., Oh, J., Hennigan,
  T., van den Driessche, G., Odoom, S., Lucic, M., Roelofs, B., Lall, S., Marathe, A., Chan, B., Ontanon, S., He, L., Teplyashin, D., Lai, J., Crone, P., Damoc, B., Ho, L., Riedel, S., Lenc, K., Yeh, C.-K., Chowdhery, A., Xu, Y., Kazemi, M., Amid, E., Petrushkina, A., Swersky, K., Khodaei, A., Chen, G., Larkin, C., Pinto, M., Yan, G., Badia, A. P., Patil, P., Hansen, S., Orr, D., Arnold, S. M. R., Grimstad, J., Dai, A., Douglas, S., Sinha, R., Yadav, V., Chen, X., Gribovskaya, E., Austin, J., Zhao, J., Patel, K., Komarek, P., Austin, S., Borgeaud, S., Friso, L., Goyal, A., Caine, B., Cao, K., Chung, D.-W., Lamm, M., Barth-Maron, G., Kagohara, T., Olszewska, K., Chen, M., Shivakumar, K., Agarwal, R., Godhia, H., Rajwar, R., Snaider, J., Dotiwalla, X., Liu, Y., Barua, A., Ungureanu, V., Zhang, Y., Batsaikhan, B.-O., Wirth, M., Qin, J., Danihelka, I., Doshi, T., Chadwick, M., Chen, J., Jain, S., Le, Q., Kar, A., Gurumurthy, M., Li, C., Sang, R., Liu, F., Lamprou, L., Munoz, R., Lintz, N., Mehta, H., Howard, H.,
  Reynolds, M., Aroyo, L., Wang, Q., Blanco, L., Cassirer, A., Griffith, J., Das, D., Lee, S., Sygnowski, J., Fisher, Z., Besley, J., Powell, R., Ahmed, Z., Paulus, D., Reitter, D., Borsos, Z., Joshi, R., Pope, A., Hand, S., Selo, V., Jain, V., Sethi, N., Goel, M., Makino, T., May, R., Yang, Z., Schalkwyk, J., Butterfield, C., Hauth, A., Goldin, A., Hawkins, W., Senter, E., Brin, S., Woodman, O., Ritter, M., Noland, E., Giang, M., Bolina, V., Lee, L., Blyth, T., Mackinnon, I., Reid, M., Sarvana, O., Silver, D., Chen, A., Wang, L., Maggiore, L., Chang, O., Attaluri, N., Thornton, G., Chiu, C.-C., Bunyan, O., Levine, N., Chung, T., Eltyshev, E., Si, X., Lillicrap, T., Brady, D., Aggarwal, V., Wu, B., Xu, Y., McIlroy, R., Badola, K., Sandhu, P., Moreira, E., Stokowiec, W., Hemsley, R., Li, D., Tudor, A., Shyam, P., Rahimtoroghi, E., Haykal, S., Sprechmann, P., Zhou, X., Mincu, D., Li, Y., Addanki, R., Krishna, K., Wu, X., Frechette, A., Eyal, M., Dafoe, A., Lacey, D., Whang, J., Avrahami, T., Zhang, Y., Taropa,
  E., Lin, H., Toyama, D., Rutherford, E., Sano, M., Choe, H., Tomala, A., Safranek-Shrader, C., Kassner, N., Pajarskas, M., Harvey, M., Sechrist, S., Fortunato, M., Lyu, C., Elsayed, G., Kuang, C., Lottes, J., Chu, E., Jia, C., Chen, C.-W., Humphreys, P., Baumli, K., Tao, C., Samuel, R., dos Santos, C. N., Andreassen, A., Rakićević, N., Grewe, D., Kumar, A., Winkler, S., Caton, J., Brock, A., Dalmia, S., Sheahan, H., Barr, I., Miao, Y., Natsev, P., Devlin, J., Behbahani, F., Prost, F., Sun, Y., Myaskovsky, A., Pillai, T. S., Hurt, D., Lazaridou, A., Xiong, X., Zheng, C., Pardo, F., Li, X., Horgan, D., Stanton, J., Ambar, M., Xia, F., Lince, A., Wang, M., Mustafa, B., Webson, A., Lee, H., Anil, R., Wicke, M., Dozat, T., Sinha, A., Piqueras, E., Dabir, E., Upadhyay, S., Boral, A., Hendricks, L. A., Fry, C., Djolonga, J., Su, Y., Walker, J., Labanowski, J., Huang, R., Misra, V., Chen, J., Skerry-Ryan, R., Singh, A., Rijhwani, S., Yu, D., Castro-Ros, A., Changpinyo, B., Datta, R., Bagri, S., Hrafnkelsson,
  A. M., Maggioni, M., Zheng, D., Sulsky, Y., Hou, S., Paine, T. L., Yang, A., Riesa, J., Rogozinska, D., Marcus, D., Badawy, D. E., Zhang, Q., Wang, L., Miller, H., Greer, J., Sjos, L. L., Nova, A., Zen, H., Chaabouni, R., Rosca, M., Jiang, J., Chen, C., Liu, R., Sainath, T., Krikun, M., Polozov, A., Lespiau, J.-B., Newlan, J., Cankara, Z., Kwak, S., Xu, Y., Chen, P., Coenen, A., Meyer, C., Tsihlas, K., Ma, A., Gottweis, J., Xing, J., Gu, C., Miao, J., Frank, C., Cankara, Z., Ganapathy, S., Dasgupta, I., Hughes-Fitt, S., Chen, H., Reid, D., Rong, K., Fan, H., van Amersfoort, J., Zhuang, V., Cohen, A., Gu, S. S., Mohananey, A., Ilic, A., Tobin, T., Wieting, J., Bortsova, A., Thacker, P., Wang, E., Caveness, E., Chiu, J., Sezener, E., Kaskasoli, A., Baker, S., Millican, K., Elhawaty, M., Aisopos, K., Lebsack, C., Byrd, N., Dai, H., Jia, W., Wiethoff, M., Davoodi, E., Weston, A., Yagati, L., Ahuja, A., Gao, I., Pundak, G., Zhang, S., Azzam, M., Sim, K. C., Caelles, S., Keeling, J., Sharma, A., Swing, A., Li,
  Y., Liu, C., Bostock, C. G., Bansal, Y., Nado, Z., Anand, A., Lipschultz, J., Karmarkar, A., Proleev, L., Ittycheriah, A., Yeganeh, S. H., Polovets, G., Faust, A., Sun, J., Rrustemi, A., Li, P., Shivanna, R., Liu, J., Welty, C., Lebron, F., Baddepudi, A., Krause, S., Parisotto, E., Soricut, R., Xu, Z., Bloxwich, D., Johnson, M., Neyshabur, B., Mao-Jones, J., Wang, R., Ramasesh, V., Abbas, Z., Guez, A., Segal, C., Nguyen, D. D., Svensson, J., Hou, L., York, S., Milan, K., Bridgers, S., Gworek, W., Tagliasacchi, M., Lee-Thorp, J., Chang, M., Guseynov, A., Hartman, A. J., Kwong, M., Zhao, R., Kashem, S., Cole, E., Miech, A., Tanburn, R., Phuong, M., Pavetic, F., Cevey, S., Comanescu, R., Ives, R., Yang, S., Du, C., Li, B., Zhang, Z., Iinuma, M., Hu, C. H., Roy, A., Bijwadia, S., Zhu, Z., Martins, D., Saputro, R., Gergely, A., Zheng, S., Jia, D., Antonoglou, I., Sadovsky, A., Gu, S., Bi, Y., Andreev, A., Samangooei, S., Khan, M., Kocisky, T., Filos, A., Kumar, C., Bishop, C., Yu, A., Hodkinson, S., Mittal, S.,
  Shah, P., Moufarek, A., Cheng, Y., Bloniarz, A., Lee, J., Pejman, P., Michel, P., Spencer, S., Feinberg, V., Xiong, X., Savinov, N., Smith, C., Shakeri, S., Tran, D., Chesus, M., Bohnet, B., Tucker, G., von Glehn, T., Muir, C., Mao, Y., Kazawa, H., Slone, A., Soparkar, K., Shrivastava, D., Cobon-Kerr, J., Sharman, M., Pavagadhi, J., Araya, C., Misiunas, K., Ghelani, N., Laskin, M., Barker, D., Li, Q., Briukhov, A., Houlsby, N., Glaese, M., Lakshminarayanan, B., Schucher, N., Tang, Y., Collins, E., Lim, H., Feng, F., Recasens, A., Lai, G., Magni, A., Cao, N. D., Siddhant, A., Ashwood, Z., Orbay, J., Dehghani, M., Brennan, J., He, Y., Xu, K., Gao, Y., Saroufim, C., Molloy, J., Wu, X., Arnold, S., Chang, S., Schrittwieser, J., Buchatskaya, E., Radpour, S., Polacek, M., Giordano, S., Bapna, A., Tokumine, S., Hellendoorn, V., Sottiaux, T., Cogan, S., Severyn, A., Saleh, M., Thakoor, S., Shefey, L., Qiao, S., Gaba, M., yiin Chang, S., Swanson, C., Zhang, B., Lee, B., Rubenstein, P. K., Song, G., Kwiatkowski, T.,
  Koop, A., Kannan, A., Kao, D., Schuh, P., Stjerngren, A., Ghiasi, G., Gibson, G., Vilnis, L., Yuan, Y., Ferreira, F. T., Kamath, A., Klimenko, T., Franko, K., Xiao, K., Bhattacharya, I., Patel, M., Wang, R., Morris, A., Strudel, R., Sharma, V., Choy, P., Hashemi, S. H., Landon, J., Finkelstein, M., Jhakra, P., Frye, J., Barnes, M., Mauger, M., Daun, D., Baatarsukh, K., Tung, M., Farhan, W., Michalewski, H., Viola, F., de Chaumont Quitry, F., Lan, C. L., Hudson, T., Wang, Q., Fischer, F., Zheng, I., White, E., Dragan, A., baptiste Alayrac, J., Ni, E., Pritzel, A., Iwanicki, A., Isard, M., Bulanova, A., Zilka, L., Dyer, E., Sachan, D., Srinivasan, S., Muckenhirn, H., Cai, H., Mandhane, A., Tariq, M., Rae, J. W., Wang, G., Ayoub, K., FitzGerald, N., Zhao, Y., Han, W., Alberti, C., Garrette, D., Krishnakumar, K., Gimenez, M., Levskaya, A., Sohn, D., Matak, J., Iturrate, I., Chang, M. B., Xiang, J., Cao, Y., Ranka, N., Brown, G., Hutter, A., Mirrokni, V., Chen, N., Yao, K., Egyed, Z., Galilee, F., Liechty, T.,
  Kallakuri, P., Palmer, E., Ghemawat, S., Liu, J., Tao, D., Thornton, C., Green, T., Jasarevic, M., Lin, S., Cotruta, V., Tan, Y.-X., Fiedel, N., Yu, H., Chi, E., Neitz, A., Heitkaemper, J., Sinha, A., Zhou, D., Sun, Y., Kaed, C., Hulse, B., Mishra, S., Georgaki, M., Kudugunta, S., Farabet, C., Shafran, I., Vlasic, D., Tsitsulin, A., Ananthanarayanan, R., Carin, A., Su, G., Sun, P., V, S., Carvajal, G., Broder, J., Comsa, I., Repina, A., Wong, W., Chen, W. W., Hawkins, P., Filonov, E., Loher, L., Hirnschall, C., Wang, W., Ye, J., Burns, A., Cate, H., Wright, D. G., Piccinini, F., Zhang, L., Lin, C.-C., Gog, I., Kulizhskaya, Y., Sreevatsa, A., Song, S., Cobo, L. C., Iyer, A., Tekur, C., Garrido, G., Xiao, Z., Kemp, R., Zheng, H. S., Li, H., Agarwal, A., Ngani, C., Goshvadi, K., Santamaria-Fernandez, R., Fica, W., Chen, X., Gorgolewski, C., Sun, S., Garg, R., Ye, X., Eslami, S. M. A., Hua, N., Simon, J., Joshi, P., Kim, Y., Tenney, I., Potluri, S., Thiet, L. N., Yuan, Q., Luisier, F., Chronopoulou, A.,
  Scellato, S., Srinivasan, P., Chen, M., Koverkathu, V., Dalibard, V., Xu, Y., Saeta, B., Anderson, K., Sellam, T., Fernando, N., Huot, F., Jung, J., Varadarajan, M., Quinn, M., Raul, A., Le, M., Habalov, R., Clark, J., Jalan, K., Bullard, K., Singhal, A., Luong, T., Wang, B., Rajayogam, S., Eisenschlos, J., Jia, J., Finchelstein, D., Yakubovich, A., Balle, D., Fink, M., Agarwal, S., Li, J., Dvijotham, D., Pal, S., Kang, K., Konzelmann, J., Beattie, J., Dousse, O., Wu, D., Crocker, R., Elkind, C., Jonnalagadda, S. R., Lee, J., Holtmann-Rice, D., Kallarackal, K., Liu, R., Vnukov, D., Vats, N., Invernizzi, L., Jafari, M., Zhou, H., Taylor, L., Prendki, J., Wu, M., Eccles, T., Liu, T., Kopparapu, K., Beaufays, F., Angermueller, C., Marzoca, A., Sarcar, S., Dib, H., Stanway, J., Perbet, F., Trdin, N., Sterneck, R., Khorlin, A., Li, D., Wu, X., Goenka, S., Madras, D., Goldshtein, S., Gierke, W., Zhou, T., Liu, Y., Liang, Y., White, A., Li, Y., Singh, S., Bahargam, S., Epstein, M., Basu, S., Lao, L., Ozturel, A.,
  Crous, C., Zhai, A., Lu, H., Tung, Z., Gaur, N., Walton, A., Dixon, L., Zhang, M., Globerson, A., Uy, G., Bolt, A., Wiles, O., Nasr, M., Shumailov, I., Selvi, M., Piccinno, F., Aguilar, R., McCarthy, S., Khalman, M., Shukla, M., Galic, V., Carpenter, J., Villela, K., Zhang, H., Richardson, H., Martens, J., Bosnjak, M., Belle, S. R., Seibert, J., Alnahlawi, M., McWilliams, B., Singh, S., Louis, A., Ding, W., Popovici, D., Simicich, L., Knight, L., Mehta, P., Gupta, N., Shi, C., Fatehi, S., Mitrovic, J., Grills, A., Pagadora, J., Munkhdalai, T., Petrova, D., Eisenbud, D., Zhang, Z., Yates, D., Mittal, B., Tripuraneni, N., Assael, Y., Brovelli, T., Jain, P., Velimirovic, M., Akbulut, C., Mu, J., Macherey, W., Kumar, R., Xu, J., Qureshi, H., Comanici, G., Wiesner, J., Gong, Z., Ruddock, A., Bauer, M., Felt, N., GP, A., Arnab, A., Zelle, D., Rothfuss, J., Rosgen, B., Shenoy, A., Seybold, B., Li, X., Mudigonda, J., Erdogan, G., Xia, J., Simsa, J., Michi, A., Yao, Y., Yew, C., Kan, S., Caswell, I., Radebaugh, C.,
  Elisseeff, A., Valenzuela, P., McKinney, K., Paterson, K., Cui, A., Latorre-Chimoto, E., Kim, S., Zeng, W., Durden, K., Ponnapalli, P., Sosea, T., Choquette-Choo, C. A., Manyika, J., Robenek, B., Vashisht, H., Pereira, S., Lam, H., Velic, M., Owusu-Afriyie, D., Lee, K., Bolukbasi, T., Parrish, A., Lu, S., Park, J., Venkatraman, B., Talbert, A., Rosique, L., Cheng, Y., Sozanschi, A., Paszke, A., Kumar, P., Austin, J., Li, L., Salama, K., Perz, B., Kim, W., Dukkipati, N., Baryshnikov, A., Kaplanis, C., Sheng, X., Chervonyi, Y., Unlu, C., de Las Casas, D., Askham, H., Tunyasuvunakool, K., Gimeno, F., Poder, S., Kwak, C., Miecnikowski, M., Mirrokni, V., Dimitriev, A., Parisi, A., Liu, D., Tsai, T., Shevlane, T., Kouridi, C., Garmon, D., Goedeckemeyer, A., Brown, A. R., Vijayakumar, A., Elqursh, A., Jazayeri, S., Huang, J., Carthy, S. M., Hoover, J., Kim, L., Kumar, S., Chen, W., Biles, C., Bingham, G., Rosen, E., Wang, L., Tan, Q., Engel, D., Pongetti, F., de Cesare, D., Hwang, D., Yu, L., Pullman, J.,
  Narayanan, S., Levin, K., Gopal, S., Li, M., Aharoni, A., Trinh, T., Lo, J., Casagrande, N., Vij, R., Matthey, L., Ramadhana, B., Matthews, A., Carey, C., Johnson, M., Goranova, K., Shah, R., Ashraf, S., Dasgupta, K., Larsen, R., Wang, Y., Vuyyuru, M. R., Jiang, C., Ijazi, J., Osawa, K., Smith, C., Boppana, R. S., Bilal, T., Koizumi, Y., Xu, Y., Altun, Y., Shabat, N., Bariach, B., Korchemniy, A., Choo, K., Ronneberger, O., Iwuanyanwu, C., Zhao, S., Soergel, D., Hsieh, C.-J., Cai, I., Iqbal, S., Sundermeyer, M., Chen, Z., Bursztein, E., Malaviya, C., Biadsy, F., Shroff, P., Dhillon, I., Latkar, T., Dyer, C., Forbes, H., Nicosia, M., Nikolaev, V., Greene, S., Georgiev, M., Wang, P., Martin, N., Sedghi, H., Zhang, J., Banzal, P., Fritz, D., Rao, V., Wang, X., Zhang, J., Patraucean, V., Du, D., Mordatch, I., Jurin, I., Liu, L., Dubey, A., Mohan, A., Nowakowski, J., Ion, V.-D., Wei, N., Tojo, R., Raad, M. A., Hudson, D. A., Keshava, V., Agrawal, S., Ramirez, K., Wu, Z., Nguyen, H., Liu, J., Sewak, M., Petrini,
  B., Choi, D., Philips, I., Wang, Z., Bica, I., Garg, A., Wilkiewicz, J., Agrawal, P., Li, X., Guo, D., Xue, E., Shaik, N., Leach, A., Khan, S. M., Wiesinger, J., Jerome, S., Chakladar, A., Wang, A. W., Ornduff, T., Abu, F., Ghaffarkhah, A., Wainwright, M., Cortes, M., Liu, F., Maynez, J., Terzis, A., Samangouei, P., Mansour, R., Kepa, T., Aubet, F.-X., Algymr, A., Banica, D., Weisz, A., Orban, A., Senges, A., Andrejczuk, E., Geller, M., Santo, N. D., Anklin, V., Merey, M. A., Baeuml, M., Strohman, T., Bai, J., Petrov, S., Wu, Y., Hassabis, D., Kavukcuoglu, K., Dean, J., and Vinyals, O.
  Gemini 1.5: Unlocking multimodal understanding across millions of tokens of context, 2024b.
  URL <https://arxiv.org/abs/2403.05530>.
- Wang et al. (2023)

  Wang, H., Fu, T., Du, Y., Gao, W., Huang, K., Liu, Z., Chandak, P., Liu, S., Van Katwyk, P., Deac, A., et al.
  Scientific discovery in the age of artificial intelligence.
  *Nature*, 620(7972):47–60, 2023.
- Wei et al. (2022a)

  Wei, J., Tay, Y., Bommasani, R., Raffel, C., Zoph, B., Borgeaud, S., Yogatama, D., Bosma, M., Zhou, D., Metzler, D., Chi, E. H., Hashimoto, T., Vinyals, O., Liang, P., Dean, J., and Fedus, W.
  Emergent abilities of large language models, 2022a.
  URL <https://arxiv.org/abs/2206.07682>.
- Wei et al. (2022b)

  Wei, J., Tay, Y., Bommasani, R., Raffel, C., Zoph, B., Borgeaud, S., Yogatama, D., Bosma, M., Zhou, D., Metzler, D., et al.
  Emergent abilities of large language models.
  *arXiv preprint arXiv:2206.07682*, 2022b.
- Wu & Lo (2024)

  Wu, T.-Y. and Lo, P.-Y.
  U-shaped and inverted-u scaling behind emergent abilities of large language models, 2024.
  URL <https://arxiv.org/abs/2410.01692>.
- Wu et al. (2024)

  Wu, Y., Sun, Z., Li, S., Welleck, S., and Yang, Y.
  Inference scaling laws: An empirical analysis of compute-optimal inference for problem-solving with language models, 2024.
  URL <https://arxiv.org/abs/2408.00724>.
- Xiong et al. (2023)

  Xiong, W., Liu, J., Molybog, I., Zhang, H., Bhargava, P., Hou, R., Martin, L., Rungta, R., Sankararaman, K. A., Oguz, B., Khabsa, M., Fang, H., Mehdad, Y., Narang, S., Malik, K., Fan, A., Bhosale, S., Edunov, S., Lewis, M., Wang, S., and Ma, H.
  Effective long-context scaling of foundation models, 2023.
  URL <https://arxiv.org/abs/2309.16039>.
- Zhai et al. (2022)

  Zhai, X., Kolesnikov, A., Houlsby, N., and Beyer, L.
  Scaling vision transformers.
  In *Proceedings of the IEEE/CVF conference on computer vision and pattern recognition*, pp. 12104–12113, 2022.
- Zhang et al. (2024)

  Zhang, B., Liu, Z., Cherry, C., and Firat, O.
  When scaling meets llm finetuning: The effect of data, model and finetuning method, 2024.
  URL <https://arxiv.org/abs/2402.17193>.
## 附录 A 对 Large Language Monkeys 与 Best-of-N Jailbreaking 采样数据方式的澄清

在本稿件中，我们使用了「独立尝试」的措辞，这并不完全正确。在本附录节中，我们澄清为何选择这一术语、我们相信这一不精确可能对结果造成的影响，以及如何相应地修正论文。

Large Language Monkeys（Brown et al., 2024）确实为每道题独立抽取了 10,000 次尝试，但 Best-of-N Jailbreaking（Hughes et al., 2024）的采样方式略有不同：对每个问题，越狱尝试一直抽取到要么获得一次成功越狱、要么达到 10,000 次尝试的上限为止。样本还是以大小为 60 的迷你批次抽取的，这使得样本的（非）独立性有些微妙。

我们省略这一细节，是因为它只是对论文主要故事的二阶修正，而几乎没有提供额外的洞见。我们的两个定理都没有改变，正文的所有图也没有改变。我们怀疑，正是这一略有不同的采样流程解释了为什么在图 6 中，Best-of-N Jailbreaking 的最小二乘幂律估计器与分布幂律估计器之间估计出的幂律指数比 Large Language Monkeys 更显著地偏离恒等线。一个自然的修正方式是使用 beta-负二项分布而非 beta-二项分布，并对最大尝试次数做一次额外修正。更多信息见附录 H。

## 附录 B 用 Chen et al. (2021) 的估计器估计成功率

在本稿件中，我们把 $\operatorname{pass_{i}@k}$ 与 $\operatorname{ASR_{i}@k}$ 定义为：

$$
\operatorname{pass_{i}@k}\defeq\mathop{\mathbb{E}}_{k\text{ 次尝试}}\big[\mathbb{I}[\text{模型的至少 1 次尝试解出第 }i\text{ 道题}]\big]
$$

$$
\operatorname{ASR_{i}@k}\defeq\mathop{\mathbb{E}}_{k\text{ 次尝试}}\big[\mathbb{I}[\text{至少 1 次尝试在第 }i\text{ 个提示上越狱该模型}]\big]
$$

在本稿件中，为估计 $\operatorname{pass_{i}@k}$ 与 $\operatorname{ASR@k}$，我们使用了 Chen et al. (2021) 引入的无偏且低方差估计器：对第 $i$ 道题，我们每题采样 $n\gg k$ 次尝试，统计成功尝试的次数 $c$，然后扫描 $k$ 以计算不同 $k$ 值下 $\operatorname{pass_{i}@k}$ 的估计：

$$
\widehat{\operatorname{pass_{i}@k}}=1-\frac{\binom{n-c}{k}}{\binom{n}{k}} \tag{12}
$$

两点说明：第一，此处使用的 $n$ 与第 1 节中基准的题目数量无关；第二，我们的记号与 Chen et al. (2021) 略有不同，但思想一致。该估计器的一个数值稳定的 Python 实现见图 8：

```python
def estimate_success_rate_at_k_per_problem(n: int, c: int, k: int) -> float:
    """
    :param n: number of total attempts on this problem.
    :param c: number of correct attempts on this problem.
    :param k: k in pass_i@$k$.
    """
    if n - c < k: return 1.0
    return 1.0 - np.prod(1.0 - k / np.arange(n - c + 1, n + 1))
```

图 8：Chen et al. (2021) 引入的 $\operatorname{pass_{i}@k}$ 的数值稳定无偏估计器。

重申 Chen et al. (2021) 指出的一点：把 $\operatorname{pass_{i}@k}$ 估计为 $1-(1-\widehat{\operatorname{pass_{i}@1}})^{k}$ 是有偏的（图 9）。

图 9：$\operatorname{pass_{i}@k}$ 估计器的偏差。数值模拟表明，把 $\operatorname{pass_{i}@k}$ 估计为 $1-(1-\widehat{\operatorname{pass_{i}@1}})^{k}$ 是有偏的，而 Chen et al. (2021) 的估计器则无偏。无偏性的数学证明见原论文。

## 附录 C 对 Large Language Monkeys 与 Best-of-N Jailbreaking 拟合幂律

我们对 Large Language Monkeys（Brown et al., 2024）与 Best-of-N Jailbreaking（Hughes et al., 2024）的数据子集拟合幂律，具体为 MATH 基准（Hendrycks et al., 2021）上的 Pythia 语言模型（Biderman et al., 2023），以及 HarmBench 越狱基准（Mazeika et al., 2024）上的前沿 AI 模型——Claude、GPT4（OpenAI et al., 2024）、Gemini（Team et al., 2024a；Team et al., 2024b）与 Llama 3（Grattafiori et al., 2024）。我们在表 1 与表 2 中分别给出函数形式与拟合参数。为拟合参数，对 Large Language Monkeys，我们简单地最小化真实与预测的 $-\log(\operatorname{pass_{\mathcal{D}}@k})$ 之间的平方误差；对 Best-of-N Jailbreaking，我们类似地最小化真实与预测的 $-\log(\operatorname{ASR_{\mathcal{D}}@k})$ 之间的平方误差。

注：Llama 3 8B IT 在 Best-of-N Jailbreaking 下不呈现幂律缩放（见图 1 下）。

| 模型 | 基准 | $a$ | $b$ |
| --- | --- | --- | --- |
| Pythia 70M | MATH | 8.026 | 0.194 |
| Pythia 160M | MATH | 6.591 | 0.280 |
| Pythia 410M | MATH | 5.524 | 0.286 |
| Pythia 1B | MATH | 5.452 | 0.315 |
| Pythia 2.8B | MATH | 4.104 | 0.336 |
| Pythia 6.9B | MATH | 4.255 | 0.348 |
| Pythia 12B | MATH | 4.113 | 0.370 |

表 1：Large Language Monkeys（Brown et al., 2024）在 MATH（Hendrycks et al., 2021）128 道数学题上拟合的幂律参数。
函数形式：$-\log(\operatorname{pass_{\mathcal{D}}@k})=a\,k^{-b}$。

| 模型 | 模态 | $a$ | $b$ |
| --- | --- | --- | --- |
| Claude 3.5 Opus | 文本 | 2.630 | 0.448 |
| Claude 3.5 Sonnet | 文本 | 3.436 | 0.312 |
| GPT4o | 文本 | 3.639 | 0.395 |
| GPT4o Mini | 文本 | 3.637 | 0.492 |
| Gemini 1.5 Flash | 文本 | 6.158 | 0.303 |
| Gemini 1.5 Pro | 文本 | 6.296 | 0.256 |
| Llama 3 8B IT | 文本 | – | – |

表 2：Best-of-N Jailbreaking（Hughes et al., 2024）在 HarmBench（Mazeika et al., 2024）文本越狱提示上拟合的幂律参数。
函数形式：$-\log(\operatorname{ASR_{\mathcal{D}}@k})=a\,k^{-b}$。
注：Llama 3 8B 指令微调（IT）不呈现幂律缩放。

## 附录 D 覆盖率与平均成功率的数学等价性

Brown et al. (2024) 与 Hughes et al. (2024) 用「覆盖率」（定义为可被求解的问题比例或能越狱模型的提示比例）来表述研究，但正如 Brown et al. (2024) 所评注且我们在此推导的，覆盖率在数学上等价于平均的 $\operatorname{pass_{i}@k}$（等价地 $\operatorname{ASR@k}$），依据是三个简单的概率学基元：(1) 期望的线性性；(2) 某事件指示随机变量的期望即该事件的概率；(3) $\operatorname{pass_{i}@k}$ 的定义：

$$
\mathbb{E}_{\begin{subarray}{c}\text{提示}\\ \text{尝试}\end{subarray}}\Big[\operatorname{Coverage}\Big]\defeq\mathbb{E}_{\begin{subarray}{c}\text{题目}\\ \text{尝试}\end{subarray}}\Big[k\text{ 次尝试后被解出的题目比例}\Big]
$$

$$
=\mathbb{E}_{\text{题目}}\Bigg[\mathbb{E}_{\text{尝试}|\text{题目}}\Big[\mathbb{I}\big[k\text{ 次尝试后题目被解出}\big]\Big]\Bigg]
$$

$$
=\mathbb{E}_{\text{题目}}\Bigg[\operatorname{pass_{problem}@k}\Bigg]
$$

$$
=\operatorname{pass_{\mathcal{D}}@k}
$$

在我们的工作中，我们更偏好「成功率」而非「覆盖率」的措辞，因为成功率避免了覆盖率那种「每个问题/提示要么被解出、要么未被解出」的二元含义。

## 附录 E 由指数函数上的概率分布产生聚合幂律

### E.1 预备知识：由加权指数函数产生幂律

一个已知结果是，幂律可以从适当加权的指数函数之和产生，例如（Bochud & Challet, 2006；Elkies, 2016；Bousquet et al., 2020）。举一个带简短证明的具体例子：

$$
x^{-r}=\frac{1}{\Gamma(r)}\int_{0}^{\infty}p^{r-1}\,e^{-px}\,dp, \tag{13}
$$

其中 $\Gamma(r)\defeq\int_{0}^{\infty}s^{r-1}\,e^{-s}\,ds$ 是 Gamma 函数。证明通过换元 $u\defeq p\,x$：

$$
\frac{1}{\Gamma(r)}\int_{0}^{\infty}p^{r-1}\,e^{-px}\,dp
=\frac{1}{\Gamma(r)}\int_{0}^{\infty}(u/x)^{r-1}\,e^{-u}\,\frac{du}{x} \tag{14}
$$

$$
=\frac{1}{\Gamma(r)}\,x^{-r}\,\int_{0}^{\infty}u^{r-1}\,e^{-u}\,du \tag{15}
$$

$$
=\frac{1}{\Gamma(r)}\,x^{-r}\,\Gamma(r) \tag{16}
$$

$$
=x^{-r} \tag{17}
$$

在我们的具体语境中，我们关心的是从基准数据分布采样的题目上期望成功率随 $k$ 的缩放：

$$
\operatorname{pass_{\mathcal{D}}@k}\defeq\mathbb{E}_{\operatorname{pass_{i}@1}\sim\mathcal{D}}\Big[\operatorname{pass_{i}@k}\Big] \tag{18}
$$

（基准中题目上）$\operatorname{pass_{i}@k}$ 得分的分布，能产生随尝试次数 $k$ 的幂律缩放：

$$
-\log\Bigg(\frac{1}{n}\sum_{i=1}^{n}\operatorname{pass_{i}@k}\Bigg)\approx ak^{-b}. \tag{19}
$$

其中常数 $a,b>0$。

### E.2 狄拉克分布：$\operatorname{pass_{i}@1}\sim\delta(p),\,p\in(0,1)$

先从一个负面结果开始：我们将证明并非所有逐题成功概率 $\operatorname{pass_{i}@1}$ 的分布都产生聚合幂律缩放。假设模型在基准各题上的 $\operatorname{pass_{i}@1}$ 概率都恰好是 $p\in(0,1)$。为简洁起见，令 $p_{i}\defeq\operatorname{pass_{i}@1}$。那么聚合成功率为：

$$
\mathbb{E}_{p_{i}\sim\delta(p)}[\operatorname{pass_{i}@k}]
=1-\mathbb{E}_{p_{i}}[(1-p_{i})^{k}] \tag{20}
$$

$$
=\int_{0}^{1}\delta(p)\,(1-p_{i})^{k}\,dp_{i} \tag{21}
$$

$$
=(1-p)^{k}. \tag{22}
$$

回顾 $\log(\cdot)$ 在 $x$ 小处的展开 $-\log(1-x)=x+O(x^{2})$，在我们的情形中得到：

$$
-\log\Big(1-\mathbb{E}_{p_{i}\sim\delta(p)}[\operatorname{pass@k}]\Big)=(1-p)^{k}+O((1-p)^{2k})=(1-p)^{k}+o((1-p)^{k}). \tag{23}
$$

因此，在大的 $k$ 区间，我们发现负对数聚合成功率呈现我们直觉上预期的随 $k$ 的指数缩放。

### E.3 均匀分布：$\operatorname{pass_{i}@1}\sim\mathrm{Uniform}(\alpha,\beta)$

假设 $\operatorname{pass_{i}@1}$ 概率服从均匀分布 $\mathrm{Uniform}(\alpha,\beta)$，其中 $0\leq\alpha<\beta\leq 1$。$k$ 次尝试后的聚合成功率定义为：

$$
\operatorname{pass_{\mathrm{Uniform}(\alpha,\beta)}}@k\defeq 1-\mathbb{E}\bigl[(1-p)^{k}\bigr].
$$

若 $p\sim\mathrm{Uniform}(\alpha,\beta)$，则 $(1-p)^{k}$ 的期望为：

$$
\mathbb{E}\bigl[(1-p)^{k}\bigr]\;=\;\frac{1}{\beta-\alpha}\int_{\alpha}^{\beta}(1-p)^{k}\,\mathrm{d}p.
$$

计算该积分得：

$$
\mathbb{E}\bigl[(1-p)^{k}\bigr]\;=\;\frac{(1-\alpha)^{k+1}-(1-\beta)^{k+1}}{(\beta-\alpha)\cdot(k+1)}.
$$

于是聚合成功率变为：

$$
\operatorname{pass_{\mathrm{Uniform}(\alpha,\beta)}}@k\;=\;1\;-\;\frac{(1-\alpha)^{k+1}-(1-\beta)^{k+1}}{(\beta-\alpha)\cdot(k+1)}.
$$

#### 情形 A：$\alpha>0$

若 $\alpha>0$，则 $(1-\alpha)$ 与 $(1-\beta)$ 都严格小于 $1$。当 $k\to\infty$ 时，$(1-\alpha)^{k+1}$ 与 $(1-\beta)^{k+1}$ 指数衰减。因此：

$$
\mathbb{E}\bigl[(1-p)^{k}\bigr]\sim\frac{(1-\alpha)^{k+1}}{(\beta-\alpha)\cdot(k+1)},
$$

且 $\operatorname{pass_{\mathrm{Uniform}(\alpha,\beta)}}@k$ 以指数速度趋近 $1$：

$$
\operatorname{pass_{\mathrm{Uniform}(\alpha,\beta)}}@k\sim 1-\frac{(1-\alpha)^{k+1}}{(\beta-\alpha)\cdot(k+1)}.
$$

因此聚合成功率的负对数指数衰减：

$$
-\log\bigl(\operatorname{pass_{\mathrm{Uniform}(\alpha,\beta)}}@k\bigr)\sim e^{-\Omega(k)}.
$$

#### 情形 B：$\alpha=0$

当 $\alpha=0$ 时，均匀分布落在 $[0,\beta]$ 上。此时：

$$
\mathbb{E}\bigl[(1-p)^{k}\bigr]\;=\;\frac{1}{\beta}\cdot\frac{1-(1-\beta)^{k+1}}{k+1}.
$$

对大的 $k$，$(1-\beta)^{k+1}$ 变得指数级小，且：

$$
\mathbb{E}\bigl[(1-p)^{k}\bigr]\sim\frac{1}{\beta}\cdot\frac{1}{k+1}.
$$

聚合成功率则为：

$$
\operatorname{pass_{\mathrm{Uniform}(0,\beta)}}@k\sim 1-\frac{1}{\beta\cdot k}.
$$

其负对数呈现幂律缩放：

$$
-\log\bigl(\operatorname{pass_{\mathrm{Uniform}(0,\beta)}}@k\bigr)\sim\frac{1}{\beta}\cdot\frac{1}{k}.
$$

#### 特殊情形：$\mathrm{Uniform}(0,1)$

若 $\beta=1$，分布为 $[0,1]$ 上的均匀分布。此时：

$$
\mathbb{E}\bigl[(1-p)^{k}\bigr]\;=\;\frac{1}{k+1},
$$

成功率变为：

$$
\operatorname{pass_{\mathrm{Uniform}(0,1)}}@k\;=\;1-\frac{1}{k+1}.
$$

对大的 $k$：

$$
-\log\bigl(\operatorname{pass_{\mathrm{Uniform}(0,1)}}@k\bigr)\sim\frac{1}{k}.
$$

### E.4 二参数 Beta 分布：$\operatorname{pass_{i}@1}\sim\operatorname{Beta}(\alpha,\beta)$

假设模型在基准各题上的 $\operatorname{pass_{i}@1}$ 概率服从 Beta 分布：

$$
\operatorname{pass_{i}@1}\sim\operatorname{Beta}(\alpha,\beta)
$$

该分布在支撑 $x\in(0,1)$ 上的概率密度函数为：

$$
f(x;\alpha,\beta)\defeq\frac{1}{B(\alpha,\beta)}\,x^{\alpha-1}\,(1-x)^{\beta-1}, \tag{24}
$$

其中 $\alpha>0,\beta>0$，$B(\cdot,\cdot)$ 是 Beta 函数。为简洁起见，令 $p_{i}\defeq\operatorname{pass_{i}@1}$。在我们假设的 Beta 分布下：

$$
\operatorname{pass_{\operatorname{Beta(\alpha,\beta)}}@k}
\defeq 1-\mathbb{E}_{p_{i}\sim\operatorname{Beta(\alpha,\beta)}}[(1-p_{i})^{k}] \tag{25}
$$

$$
=1-\int_{0}^{1}\frac{p_{i}^{\alpha-1}(1-p_{i})^{\beta-1}}{B(\alpha,\beta)}\;(1-p_{i})^{k}\;dp_{i} \tag{26}
$$

$$
=1-\frac{\Gamma(\alpha+\beta)}{\Gamma(\alpha)\Gamma(\beta)}\frac{\Gamma(\alpha)\Gamma(\beta+k)}{\Gamma(\alpha+\beta+k)} \tag{27}
$$

其中 $\Gamma(\cdot)$ 仍是 Gamma 函数。$\Gamma(\alpha)$ 项相消，而 Gamma 函数在大的 $k$ 下的一个标准渐近结果告诉我们：

$$
\frac{\Gamma(\beta+k)}{\Gamma(\alpha+\beta+k)}\sim k^{-\alpha}, \tag{28}
$$

于是：

$$
\frac{\Gamma(\alpha+\beta)}{\Gamma(\beta)}\frac{\Gamma(\beta+k)}{\Gamma(\alpha+\beta+k)}\sim\frac{\Gamma(\alpha+\beta)}{\Gamma(\beta)}k^{-\alpha}. \tag{29}
$$

再次回顾 $\log(\cdot)$ 在 $x$ 小处的展开 $-\log(1-x)=x+O(x^{2})$，在我们的情形中得到：

$$
-\log\Big(\operatorname{pass_{\mathcal{D}}@k}\Big)=\frac{\Gamma(\alpha+\beta)}{\Gamma(\beta)}k^{-\alpha}+O(k^{-2\alpha})=\frac{\Gamma(\alpha+\beta)}{\Gamma(\beta)}k^{-\alpha}+o(k^{-\alpha}). \tag{30}
$$

由这一最终结果可见，在 Beta 分布下且在大的 $k$ 区间，负对数聚合成功率呈现随 $k$、指数为 $\alpha$ 的多项式（幂律）缩放。

### E.5 Kumaraswamy 分布：$\operatorname{pass_{i}@1}\sim\operatorname{Kumaraswamy}(\alpha,\beta)$

接下来，假设模型的 $\operatorname{pass_{i}@1}$ 概率服从 Kumaraswamy 分布。该分布在支撑 $x\in(0,1)$ 上的概率密度函数为：

$$
f(x;\alpha,\beta)\defeq\alpha\,\beta\,x^{\alpha-1}\,(1-x^{\alpha})^{\beta-1} \tag{31}
$$

同样为简洁起见，令 $p_{i}\defeq\operatorname{pass_{i}@1}$。在我们假设的 Kumaraswamy 分布下：

$$
\operatorname{pass_{\operatorname{Kumaraswamy(\alpha,\beta)}}@k}
\defeq 1-\mathbb{E}_{p_{i}\sim\operatorname{Kumaraswamy}(\alpha,\beta)}[(1-p_{i})^{k}] \tag{32}
$$

$$
=1-\int_{0}^{1}(1-p)^{k}\cdot\alpha\,\beta\,p^{\alpha-1}\,(1-p^{\alpha})^{\beta-1}dp. \tag{33}
$$

定义积分

$$
I_{k}\defeq\mathbb{E}\bigl((1-p)^{k}\bigr)=\int_{0}^{1}(1-x)^{k}\,\alpha\,\beta\;x^{\alpha-1}\;\bigl(1-x^{\alpha}\bigr)^{\beta-1}\;\mathrm{d}x. \tag{34}
$$

我们旨在分析大的 $k$ 下的 $I_{k}$。注意 $(1-x)^{k}$ 除非 $x$ 非常接近 0，否则在 $k$ 上指数级小。因此直觉上，$I_{k}$ 的主要贡献来自 $x\in[0,\,O(1/k)]$。

#### 步骤 1：把积分拆成两部分。

固定常数 $c>0$。写

$$
I_{k}\;=\;\int_{0}^{c/k}[\cdots]\,\mathrm{d}x\;+\;\int_{c/k}^{1}[\cdots]\,\mathrm{d}x\;\;\defeq\;\;I_{k,\mathrm{left}}\;+\;I_{k,\mathrm{right}},
$$

其中 $[\cdots]$ 表示同一被积函数。在区域 $x\in[c/k,1]$ 上，我们有 $(1-x)^{k}\leq e^{-k\,x}\leq e^{-c}$。因此 $I_{k,\mathrm{right}}=O\bigl(e^{-c}\bigr)$。由于 $c$ 可以任意大，$I_{k,\mathrm{right}}$ 相对 $1/k$ 的任何多项式都可以忽略。

#### 步骤 2：在小 $x$ 区域近似被积函数。

在 $[0,c/k]$ 上，我们用近似 $\log(1-x)=-x+O(x^{2})$。于是

$$
(1-x)^{k}=\exp\big(k\log(1-x)\big)=\exp\big(-k\,x+O(k\,x^{2})\big).
$$

由于 $x\leq c/k$ 蕴含 $k\,x^{2}\leq c^{2}/k=O(1/k)$，且 $\exp(\epsilon)=1+O(\epsilon)$，我们得到

$$
(1-x)^{k}=\exp(-k\,x)\exp(O(1/k))=\exp(-k\,x)\,\big(1+O\bigl(\tfrac{1}{k}\bigr)\big).
$$

进一步，由 $(1-y)^{m}=1-my+O(y^{2})$，对小 $x$

$$
(1-x^{\alpha})^{\beta-1}=1-(\beta-1)x^{\alpha}+O(x^{2\alpha})=1+O\bigl(x^{\alpha}\bigr).
$$

在区域 $x\leq c/k$ 内，该误差为 $O\bigl(k^{-\alpha}\bigr)$。因此，在小 $x$ 区域内，被积函数

$$
(1-x)^{k}\;\alpha\,\beta\;x^{\alpha-1}\;\bigl(1-x^{\alpha}\bigr)^{\beta-1}
$$

可以近似为

$$
\alpha\,\beta\;x^{\alpha-1}\;e^{-k\,x}\;+\;O\Bigl(k^{-\alpha}\,x^{\alpha-1}\,e^{-k\,x}\Bigr).
$$

于是

$$
I_{k,\mathrm{left}}\;=\;\int_{0}^{c/k}\alpha\,\beta\;x^{\alpha-1}\,e^{-k\,x}\;\mathrm{d}x\;+\;O\Bigl(k^{-\alpha}\int_{0}^{c/k}x^{\alpha-1}\,e^{-k\,x}\,\mathrm{d}x\Bigr)\;+\;O\bigl(e^{-c}\bigr).
$$

#### 步骤 3：换元 $u\defeq k\,x$。

为处理 $\int_{0}^{c/k}x^{\alpha-1}e^{-k\,x}\,\mathrm{d}x$，我们换元 $u=k\,x$。则 $x=u/k$，$\mathrm{d}x=\mathrm{d}u/k$，上限 $x=c/k$ 变为 $u=c$。于是，

$$
\int_{0}^{c/k}x^{\alpha-1}\,e^{-k\,x}\,\mathrm{d}x
=\;\int_{0}^{c}\Bigl(\tfrac{u}{k}\Bigr)^{\alpha-1}\,e^{-\,u}\;\frac{\mathrm{d}u}{k}
$$

$$
=\;k^{-\alpha}\int_{0}^{c}u^{\alpha-1}\,e^{-\,u}\;\mathrm{d}u.
$$

当 $c\to\infty$ 时，$\int_{0}^{c}u^{\alpha-1}e^{-\,u}\,\mathrm{d}u\to\Gamma(\alpha)$，且对有限的 $c$ 余项为 $O\bigl(e^{-\,c}\bigr)$。因此，

$$
\int_{0}^{1}x^{\alpha-1}\,e^{-k\,x}\,\mathrm{d}x=k^{-\alpha}\,\Gamma(\alpha)\;+\;O\bigl(k^{-\alpha}\,e^{-\,c}\bigr),
$$

把常数 $c$ 吸收进大 $O$ 记号得

$$
\int_{0}^{1}x^{\alpha-1}\,e^{-k\,x}\,\mathrm{d}x=k^{-\alpha}\,\Gamma(\alpha)\;+\;O\bigl(k^{-\alpha-\epsilon}\bigr)\quad\text{对某个 }\epsilon>0.
$$

乘上因子 $\alpha\,\beta$，我们推得

$$
I_{k}\;=\;\alpha\,\beta\,\Gamma(\alpha)\,k^{-\alpha}\;+\;O\bigl(k^{-\alpha-\epsilon}\bigr).
$$

#### 步骤 4：成功率的最终结论。

回顾 $\operatorname{pass_{\mathrm{Kumaraswamy}(\alpha,\beta)}@k}=1-I_{k}$。于是

$$
\operatorname{pass_{\mathrm{Kumaraswamy}(\alpha,\beta)}@k}\;=\;1\;-\;\alpha\,\beta\,\Gamma(\alpha)\,k^{-\alpha}\;+\;O\bigl(k^{-\alpha-\epsilon}\bigr).
$$

由于它趋于 1，其负对数由 $\alpha\,\beta\,\Gamma(\alpha)\,k^{-\alpha}$ 的量级决定。利用展开 $-\log(1-y)=y+O(y^{2})$（当 $y\to 0$），我们得到

$$
-\log\Big(\operatorname{pass_{\mathrm{Kumaraswamy}(\alpha,\beta)}@k}\Big)\;=\;\alpha\,\beta\,\Gamma(\alpha)\;k^{-\alpha}\;+\;o\bigl(k^{-\alpha}\bigr).
$$

这恰是负对数成功率以指数为 $\alpha$ 的多项式（幂律）衰减。

### E.6 连续伯努利分布：$\operatorname{pass_{i}@1}\sim\operatorname{ContinuousBernoulli}(\lambda)$

接下来，假设模型的 $\operatorname{pass_{i}@1}$ 概率服从连续伯努利分布。该分布在支撑 $x\in[0,1]$ 上的概率密度函数为：

$$
f(x;\lambda)
\defeq C(\lambda)\lambda^{x}(1-\lambda)^{1-x} \tag{35}
$$

$$
C(\lambda)
\defeq\begin{cases}2&\text{若 }\lambda=1/2\\ \frac{2\tanh^{-1}{(1-2\lambda)}}{1-2\lambda}&\text{否则}\end{cases}. \tag{36}
$$

该密度可以等价地改写为更便于我们目的的形式：

$$
f(x;\lambda)=C(\lambda)\lambda^{x}(1-\lambda)(1-\lambda)^{-x}=C(\lambda)(1-\lambda)\Big(\frac{\lambda}{1-\lambda}\Big)^{x} \tag{37}
$$

由于我们的数据中单次成功概率很低，我们将考虑小 $\lambda<1/2$ 的情形。我们遵循与 Kumaraswamy 分布相同的路线。

#### 步骤 1：写出聚合通过率。

聚合通过率定义为：

$$
\operatorname{pass_{ContinuousBernoulli(\lambda)}@k}=1-I_{k},\quad\text{其中}\quad I_{k}\defeq\int_{0}^{1}(1-p)^{k}\,f(p;\lambda)\,dp.
$$

代入密度 $f(p;\lambda)$，得：

$$
I_{k}=\int_{0}^{1}(1-p)^{k}\,C(\lambda)\,\lambda^{p}\,(1-\lambda)^{1-p}\,dp.
$$

#### 步骤 2：用指数形式化简。

利用指数改写：

$$
\lambda^{p}\,(1-\lambda)^{1-p}=(1-\lambda)\exp\Bigl(p\log\bigl(\tfrac{\lambda}{1-\lambda}\bigr)\Bigr),
$$

积分变为：

$$
I_{k}=C(\lambda)\,(1-\lambda)\int_{0}^{1}(1-p)^{k}\exp\Bigl(p\log\bigl(\tfrac{\lambda}{1-\lambda}\bigr)\Bigr)\,dp.
$$

#### 步骤 3：小 $p$ 区域的主导性。

对大的 $k$，$(1-p)^{k}$ 除非 $p$ 接近 0，否则指数衰减。于是积分的主要贡献来自区域 $p\in[0,c/k]$，其中 $c>0$ 是常数。分解积分：

$$
I_{k}=\int_{0}^{c/k}[\cdots]\,dp+\int_{c/k}^{1}[\cdots]\,dp\defeq I_{k,\mathrm{left}}+I_{k,\mathrm{right}}.
$$

在区域 $p\in[c/k,1]$ 上，我们有 $(1-p)^{k}\leq e^{-kp}\leq e^{-c}$，故 $I_{k,\mathrm{right}}=O(e^{-c})$，相对 $1/k$ 可忽略。于是我们聚焦于 $I_{k,\mathrm{left}}$：

$$
I_{k,\mathrm{left}}=C(\lambda)\,(1-\lambda)\int_{0}^{c/k}(1-p)^{k}\exp\Bigl(p\log\bigl(\tfrac{\lambda}{1-\lambda}\bigr)\Bigr)\,dp.
$$

#### 步骤 4：近似被积函数。

对 $p\in[0,c/k]$，使用与 Kumaraswamy 推导中相同的近似：

$$
(1-p)^{k}=e^{-kp}\,\bigl(1+O(p)\bigr),\quad\exp\Bigl(p\log\bigl(\tfrac{\lambda}{1-\lambda}\bigr)\Bigr)=1+O(p).
$$

于是被积函数变为：

$$
(1-p)^{k}\exp\Bigl(p\log\bigl(\tfrac{\lambda}{1-\lambda}\bigr)\Bigr)=e^{-kp}\,\bigl(1+O(p)\bigr).
$$

#### 步骤 5：换元。

令 $u\defeq kp$，则 $p=u/k$、$dp=du/k$。积分变为：

$$
I_{k,\mathrm{left}}=C(\lambda)\,(1-\lambda)\int_{0}^{c}e^{-u}\,\bigl(1+O(u/k)\bigr)\,\frac{du}{k}.
$$

拆分积分：

$$
I_{k,\mathrm{left}}=\frac{C(\lambda)\,(1-\lambda)}{k}\int_{0}^{c}e^{-u}\,du+O\Bigl(\frac{1}{k^{2}}\Bigr).
$$

当 $c\to\infty$ 时，$\int_{0}^{c}e^{-u}\,du\to 1$。于是：

$$
I_{k,\mathrm{left}}=\frac{C(\lambda)\,(1-\lambda)}{k}+O\Bigl(\frac{1}{k^{2}}\Bigr).
$$

由于 $I_{k,\mathrm{right}}=O(e^{-c})$ 可忽略，我们有：

$$
I_{k}=\frac{C(\lambda)\,(1-\lambda)}{k}+O\Bigl(\frac{1}{k^{2}}\Bigr).
$$

#### 步骤 7：成功率的最终结论。

回顾：

$$
\operatorname{pass_{ContinuousBernoulli(\lambda)}@k}=1-I_{k}.
$$

对大的 $k$，这蕴含：

$$
\operatorname{pass_{ContinuousBernoulli(\lambda)}@k}=1-\frac{C(\lambda)\,(1-\lambda)}{k}+O\Bigl(\frac{1}{k^{2}}\Bigr).
$$

利用小 $y$ 下的展开 $-\log(1-y)=y+O(y^{2})$，我们得到：

$$
-\log\bigl(\operatorname{pass_{ContinuousBernoulli(\lambda)}@k}\bigr)=C(\lambda)\,(1-\lambda)k^{-1}+o(k^{-1}).
$$

这恰是负对数成功率以指数为 $1$（即 $k^{-1}$）的多项式（幂律）衰减。

顺带一提，回顾 $\tanh^{-1}(x)=\frac{1}{2}\log\big(\frac{1+x}{1-x}\big)$，归一化常数 $C(\lambda)$ 可改写为：

$$
C(\lambda)=\frac{2}{1-2\lambda}\frac{1}{2}\log\Bigg(\frac{1+(1-2\lambda)}{1-(1-2\lambda)}\Bigg)=\frac{1}{1-2\lambda}\log\Big(\frac{1-\lambda}{\lambda}\Big). \tag{38}
$$

因此对小 $\lambda$，注意 $C(\lambda)\approx\log(1/\lambda)=-\log(\lambda)$。当 $k\ll-\log(\lambda)$ 时，$1/k$ 公式有效。然而在 $k\approx-\log(\lambda)$ 附近，主导项 $-\log(\lambda)/k$ 变成 1 的量级；而当 $k\gg-\log(\lambda)$ 时，成功率已非常接近 1。因此我们看到，若 $\lambda$ 非常小，则在 $k\approx-\log(\lambda)$ 附近存在一个软截断尺度。

### E.7 任意在 0 处密度为正常数的连续分布：$p(\operatorname{pass_{i}@1})=c>0$

假设 $\operatorname{pass_{i}@1}$ 上的分布连续且在 $0$ 附近具有恒定的非零密度：

$$
f(0)=c>0 \tag{39}
$$

由于密度在 $0$ 处连续且 $f(0)=c>0$，存在某个 $\delta>0$ 使得：

$$
f(p)=c+O(p)\quad\quad\text{对所有 }p\in[0,\delta]. \tag{40}
$$

由于大的 $k$ 下小的 $\operatorname{pass_{i}@1}$ 区域占主导，与 Kumaraswamy 论证及连续伯努利论证类似的论证给出随 $k$、指数为 $1$ 的幂律缩放：

$$
-\log\Big(\operatorname{pass_{\mathcal{D}}@k}\Big)=c\,k^{-1}+o(k^{-1}). \tag{41}
$$

这一结果与连续伯努利的情形一致，其中 $c$ 由 $f_{\operatorname{ContinuousBernoulli(\lambda)}}(0;\lambda)=C(\lambda)(1-\lambda)$ 给出（$\lambda<1/2$）。该结果揭示了连续伯努利只是一个更大族中的一个实例：任何在 $\operatorname{pass_{i}@1}=0$ 处具有非零常数密度的连续分布都将以指数 $1$ 呈幂律缩放。

### E.8 倒数分布：$\operatorname{pass_{i}@1}\sim\operatorname{Reciprocal}(a,b)$

接下来，假设模型的 $\operatorname{pass_{i}@1}\sim\operatorname{Reciprocal(a,b)}$ 分布，$0<a<b<1$。该分布在支撑 $x\in[a,b]$ 上的概率密度函数为：

$$
f(x;a,b)=\frac{1}{(\log(b)-\log(a))\,x} \tag{42}
$$

与其他分布一样，$k$ 次尝试后的聚合成功率为：

$$
\operatorname{pass_{\mathrm{Reciprocal}(a,b)}@k}\;=\;\mathbb{E}\bigl[\operatorname{pass_{i}@k}\bigr]\;=\;1\;-\;I_{k},\quad\text{其中}\quad I_{k}\;\defeq\;\int_{x=a}^{b}(1-x)^{k}\,\frac{1}{(\log b-\log a)\,x}\,\mathrm{d}x.
$$

我们旨在证明 $I_{k}$ 的量级为 $\frac{(1-a)^{k}}{k}$。积分的主要贡献来自 $x=a$ 附近，因为 $(1-x)^{k}$ 随 $x$ 远离 $a$ 迅速衰减。

步骤 1：换元。定义 $y\defeq x-a$，于是定义域 $x\in[a,b]$ 变为 $y\in[0,b-a]$。则

$$
(1-x)^{k}\;=\;\bigl((1-a)-y\bigr)^{k},
$$

且

$$
I_{k}\;=\;\frac{1}{\log(b/a)}\int_{y=0}^{\,b-a}\bigl((1-a)-y\bigr)^{k}\;\frac{1}{a+y}\,\mathrm{d}y.
$$

步骤 2：在 $y=0$ 附近展开。对小 $y$，写 $(1-a)-y=(1-a)\bigl(1-\tfrac{y}{1-a}\bigr)$；于是

$$
\log\bigl((1-a)-y\bigr)\;=\;\log(1-a)\;+\;\log\Bigl(1-\tfrac{y}{\,1-a\,}\Bigr).
$$

对小 $z$ 用 $\log(1-z)=-z+O(z^{2})$，得

$$
\log\bigl((1-a)-y\bigr)\;=\;\log(1-a)\;-\;\frac{y}{1-a}\;+\;O\bigl(\tfrac{y^{2}}{(1-a)^{2}}\bigr),
$$

于是

$$
(1-a-y)^{k}\;=\;\exp\Bigl(k\,\log(1-a)\;-\;k\,\tfrac{y}{\,1-a\,}\;+\;O\bigl(\tfrac{k\,y^{2}}{(1-a)^{2}}\bigr)\Bigr).
$$

特别地，对直到 $c/k$ 的 $y$，项 $k\,y^{2}=O(1)$ 保持有界，故

$$
(1-a-y)^{k}\;=\;(1-a)^{k}\,\exp\Bigl(-\tfrac{k\,y}{\,1-a\,}\Bigr)\bigl[\,1+O\bigl(\tfrac{1}{k}\bigr)\bigr].
$$

步骤 3：积分由 $y\in[0,O(\tfrac{1}{k})]$ 主导。对大的 $k$，$\exp\bigl(-\tfrac{k\,y}{\,1-a\,}\bigr)$ 一旦 $y$ 超过 $\tfrac{1-a}{k}$ 的某个倍数就迅速衰减。因此从 $y=c_{0}/k$ 到 $b-a$ 的积分在 $k$ 上指数级小。在 $[0,c_{0}/k]$ 上，我们还有 $(a+y)^{-1}=\frac{1}{a}+O\bigl(\tfrac{1}{k}\bigr)$。于是

$$
I_{k}\;=\;\frac{1}{\log(b/a)}\int_{y=0}^{c_{0}/k}(1-a-y)^{k}\;\frac{1}{a+y}\,\mathrm{d}y\;+\;\text{（指数级小的尾部）}.
$$

把步骤 2 的近似代入被积函数：

$$
(1-a-y)^{k}\,\frac{1}{a+y}\;=\;(1-a)^{k}\,\exp\Bigl(-\tfrac{k\,y}{\,1-a\,}\Bigr)\;\Bigl[\tfrac{1}{a}+O\bigl(\tfrac{1}{k}\bigr)\Bigr].
$$

步骤 4：换元 $u=\frac{k\,y}{1-a}$。则 $y=\frac{(1-a)\,u}{k}$、$\mathrm{d}y=\frac{1-a}{k}\,\mathrm{d}u$。上限 $y=c_{0}/k$ 对应 $u=c_{0}\,\bigl(\tfrac{1-a}{1}\bigr)$，故

$$
\int_{y=0}^{c_{0}/k}\exp\Bigl(-\tfrac{k\,y}{\,1-a\,}\Bigr)\,\mathrm{d}y\;=\;\int_{u=0}^{c_{0}\,(1-a)}e^{-u}\;\frac{1-a}{k}\,\mathrm{d}u.
$$

令 $c_{0}\to\infty$ 只给尾部贡献一个 $e^{-c_{0}(1-a)}$ 因子，它趋于零。故

$$
\int_{y=0}^{\infty}\exp\Bigl(-\tfrac{k\,y}{\,1-a\,}\Bigr)\,\mathrm{d}y\;=\;\frac{1-a}{\,k\,}\int_{u=0}^{\infty}e^{-u}\,\mathrm{d}u\;=\;\frac{1-a}{k}.
$$

把所有因子放在一起，

$$
I_{k}\;=\;\frac{1}{\log(b/a)}\;(1-a)^{k}\;\Bigl[\tfrac{1}{a}+O\bigl(\tfrac{1}{k}\bigr)\Bigr]\;\frac{1-a}{k}\;+\;\text{（在 }k\text{ 上指数级小）}.
$$

于是用大 Theta 形式，

$$
I_{k}\;=\;\Theta\Bigl(\tfrac{(1-a)^{k}}{k}\Bigr).
$$

结论。由于 $\operatorname{pass_{\mathrm{Reciprocal}(a,b)}@k}=1-I_{k}$，我们得到

$$
\operatorname{pass_{\mathrm{Reciprocal}(a,b)}@k}\;=\;1\;-\;\Theta\Bigl(\tfrac{(1-a)^{k}}{k}\Bigr).
$$

进而，利用小 $y$ 下的 $-\log(1-y)=y+O(y^{2})$，可得

$$
-\log\Bigl(\operatorname{pass_{\mathrm{Reciprocal}(a,b)}@k}\Bigr)\;=\;\Theta\Bigl(\tfrac{(1-a)^{k}}{k}\Bigr).
$$

因此负对数聚合成功率在 $k$ 上*指数级快速*收敛到 $1$，这不是 $k$ 的幂律。

### 聚合成功率负对数幂律缩放的充分条件

###### 定理 E.1.

设 $\mathcal{D}$ 为 $[0,1]$ 上的概率分布，PDF 为 $f(p)$。假设存在常数 $b>0$、$C>0$、$\theta>0$ 与 $\delta>0$，使得对所有 $0<p<\delta$，有

$$
f(p)\;=\;C\,p^{\,b-1}\;+\;O\bigl(p^{\,b-1+\theta}\bigr).
$$

那么，对大的 $k$，

$$
1\;-\;\operatorname{pass_{\mathcal{D}}@k}\;=\;C\,\Gamma(b)\,k^{-b}\;+\;O\bigl(k^{-b-\min(\,1,\theta)}\bigr),
$$

这蕴含

$$
-\log\Bigl(\operatorname{pass_{\mathcal{D}}@k}\Bigr)\;=\;C\,\Gamma(b)\,k^{-b}\;+\;o\bigl(k^{-b}\bigr).
$$

等价地（含首常数），

$$
-\log\bigl(\operatorname{pass_{\mathcal{D}}@k}\bigr)\;\sim\;C\,\Gamma(b)\;k^{-b}.
$$

###### 证明.

步骤 1. 分解关键积分。定义

$$
I_{k}\;\defeq\;1\;-\;\operatorname{pass_{\mathcal{D}}@k}\;=\;\int_{0}^{1}(1-p)^{k}\,f(p)\,\mathrm{d}p.
$$

对正常数 $c>0$，拆分 $I_{k}$：

$$
I_{k}\;=\;\int_{\,0}^{\,c/k}(1-p)^{k}\,f(p)\,\mathrm{d}p\;\;+\;\;\int_{\,c/k}^{\,1}(1-p)^{k}\,f(p)\,\mathrm{d}p\;\;\defeq\;\;I_{k,\mathrm{left}}\;+\;I_{k,\mathrm{right}}.
$$

#### 右尾界（$I_{k,\mathrm{right}}$）。

对 $p\geq c/k$，注意 $(1-p)^{k}\leq e^{-k\,p}\leq e^{-c}$。故

$$
I_{k,\mathrm{right}}\;=\;\int_{c/k}^{1}(1-p)^{k}\,f(p)\,\mathrm{d}p\;\leq\;e^{-c}\,\int_{0}^{1}f(p)\,\mathrm{d}p\;=\;e^{-c}.
$$

由于 $c$ 可以任意大，$e^{-c}$ 可以被压到 $1/k$ 的*任何*幂以下。于是 $I_{k,\mathrm{right}}=o\bigl(k^{-\alpha}\bigr)$（对任何 $\alpha>0$）。因此我们可以聚焦于

$$
I_{k,\mathrm{left}}\;=\;\int_{\,0}^{\,c/k}(1-p)^{k}\,f(p)\,\mathrm{d}p,
$$

因为已知 $I_{k,\mathrm{right}}$ 在多项式型估计中可忽略。

步骤 2. 利用 $f(p)$ 在 $p=0$ 附近的假设行为。由假设，对直到某个 $\delta>0$ 的 $p$，

$$
f(p)\;=\;C\,p^{\,b-1}+O\bigl(p^{\,b-1+\theta}\bigr).
$$

取 $c/k<\delta$，于是左积分中的 $p\leq c/k<\delta$。则

$$
I_{k,\mathrm{left}}\;=\;\int_{\,0}^{\,c/k}(1-p)^{k}\Bigl[\,C\,p^{\,b-1}+O\bigl(p^{\,b-1+\theta}\bigr)\Bigr]\,\mathrm{d}p.
$$

拆成主项与误差项：

$$
I_{k,\mathrm{left}}\;=\;C\,\int_{\,0}^{\,c/k}(1-p)^{k}\,p^{\,b-1}\,\mathrm{d}p\;+\;\int_{\,0}^{\,c/k}(1-p)^{k}\,O\bigl(p^{\,b-1+\theta}\bigr)\,\mathrm{d}p.
$$

分别记这两项为 $T_{\mathrm{main}}$ 与 $T_{\mathrm{err}}$。

步骤 3. 用 $e^{-kp}$ 近似 $(1-p)^{k}$ 并控制误差。对 $[0,c/k]$ 中的 $p$，展开 $\log(1-p)=-p+O(p^{2})$。于是

$$
(1-p)^{k}\;=\;\exp\bigl(k\log(1-p)\bigr)\;=\;e^{-k\,p}\,\exp\bigl(O(k\,p^{2})\bigr)\;=\;e^{-k\,p}\,\bigl[\,1+O(k\,p^{2})\bigr].
$$

由于 $p\leq c/k$，得 $k\,p^{2}\leq c^{2}/k$，对大的 $k$ 有界。从而，

$$
(1-p)^{k}=e^{-k\,p}+O\bigl(k\,p^{2}\,e^{-k\,p}\bigr).
$$

我们将在 $T_{\mathrm{main}}$ 与 $T_{\mathrm{err}}$ 中都使用它。

步骤 4. 主项 $T_{\mathrm{main}}$。

$$
T_{\mathrm{main}}\;=\;C\int_{\,0}^{\,c/k}(1-p)^{k}\,p^{\,b-1}\,\mathrm{d}p.
$$

代入 $(1-p)^{k}=e^{-k\,p}+O\bigl(k\,p^{2}\,e^{-k\,p}\bigr)$，

$$
T_{\mathrm{main}}\;=\;C\int_{\,0}^{\,c/k}e^{-k\,p}\,p^{\,b-1}\,\mathrm{d}p\;+\;C\int_{\,0}^{\,c/k}O\bigl(k\,p^{\,b+1}\,e^{-k\,p}\bigr)\,\mathrm{d}p.
$$

记这两个积分为 $T_{1}$ 与 $T_{2}$。

#### $T_{1}$ 项。

$$
T_{1}=C\int_{\,0}^{\,c/k}p^{\,b-1}\,e^{-k\,p}\,\mathrm{d}p.
$$

做换元 $u\defeq k\,p$。则 $p=u/k$，$\mathrm{d}p=\mathrm{d}u/k$，且 $p^{\,b-1}=k^{-b+1}\,u^{\,b-1}$。上限 $p=c/k$ 变为 $u=c$。于是

$$
T_{1}=C\int_{\,0}^{\,c}\bigl(\tfrac{u}{k}\bigr)^{b-1}\,e^{-u}\,\tfrac{\mathrm{d}u}{k}=C\,k^{-b}\int_{\,0}^{\,c}u^{\,b-1}\,e^{-u}\,\mathrm{d}u.
$$

当 $c\to\infty$ 时，$\int_{0}^{c}u^{\,b-1}e^{-u}\,\mathrm{d}u\to\Gamma(b)$。故

$$
T_{1}=C\,k^{-b}\Bigl(\Gamma(b)-R_{c}\Bigr),\quad\text{其中 }|R_{c}|=O\bigl(e^{-c}\bigr).
$$

通过在 $k\to\infty$ 之后取大的 $c$，我们得出

$$
T_{1}=C\,\Gamma(b)\,k^{-b}+o\bigl(k^{-b}\bigr).
$$

#### $T_{2}$ 项。

$$
T_{2}=C\int_{\,0}^{\,c/k}O\bigl(k\,p^{\,b+1}\,e^{-k\,p}\bigr)\,\mathrm{d}p.
$$

在积分内部，$k\,p^{\,b+1}\,e^{-k\,p}$ 是主要因子。再次代入 $u\defeq k\,p$，

$$
p^{\,b+1}=\bigl(\tfrac{u}{k}\bigr)^{b+1}=k^{-b-1}\,u^{\,b+1}.
$$

于是

$$
T_{2}=C\,O(1)\,\int_{\,0}^{\,c/k}k\,p^{\,b+1}\,e^{-k\,p}\,\mathrm{d}p=O(k)\,\int_{\,0}^{\,c/k}p^{\,b+1}e^{-k\,p}\,\mathrm{d}p.
$$

代入 $u=k\,p$ 与 $\mathrm{d}p=\mathrm{d}u/k$。则

$$
T_{2}=O(k)\,\int_{\,0}^{\,c}\bigl(\tfrac{u}{k}\bigr)^{b+1}e^{-u}\,\tfrac{\mathrm{d}u}{\,k\,}=O(k)\,k^{-b-2}\int_{\,0}^{\,c}u^{\,b+1}\,e^{-u}\,\mathrm{d}u=O\bigl(k^{-b-1}\bigr).
$$

于是 $T_{2}$ 的阶严格小于 $k^{-b}$。

合并 $T_{1}$ 与 $T_{2}$：

$$
T_{\mathrm{main}}=C\,\Gamma(b)\,k^{-b}+O\bigl(k^{-b-1}\bigr).
$$

步骤 5. 误差项 $T_{\mathrm{err}}$。回顾

$$
T_{\mathrm{err}}=\int_{\,0}^{\,c/k}(1-p)^{k}\,O\bigl(p^{\,b-1+\theta}\bigr)\,\mathrm{d}p.
$$

完全相同的代入 $(1-p)^{k}=e^{-kp}+O(k\,p^{2}\,e^{-k\,p})$ 加上 $u=k\,p$ 表明

$$
T_{\mathrm{err}}=O\Bigl(\int_{\,0}^{\,c/k}p^{\,b-1+\theta}\,e^{-k\,p}\,\mathrm{d}p\Bigr)\;+\;O\Bigl(\int_{\,0}^{\,c/k}k\,p^{\,b+1+\theta}\,e^{-k\,p}\,\mathrm{d}p\Bigr).
$$

换元 $u=k\,p$ 时，若乘以 $k$，$p$ 的指数每次增加 $+1$，故每一项的阶为 $k^{-b-\theta}$ 或更小。具体地，

$$
\int_{0}^{c/k}p^{\,b-1+\theta}\,e^{-k\,p}\,\mathrm{d}p=k^{-b-\theta}\,\int_{0}^{c}u^{\,b-1+\theta}\,e^{-u}\,\mathrm{d}u=O\bigl(k^{-b-\theta}\bigr),
$$

第二项类似且更小。故

$$
T_{\mathrm{err}}=O\bigl(k^{-b-\theta}\bigr).
$$

步骤 6. 综合起来。总结：

$$
I_{k,\mathrm{left}}=T_{\mathrm{main}}+T_{\mathrm{err}}=C\,\Gamma(b)\,k^{-b}\;+\;O\bigl(k^{-b-1}\bigr)\;+\;O\bigl(k^{-b-\theta}\bigr).
$$

于是

$$
I_{k,\mathrm{left}}=C\,\Gamma(b)\,k^{-b}\;+\;O\bigl(k^{-b-\min(1,\theta)}\bigr).
$$

回顾尾部部分 $I_{k,\mathrm{right}}=e^{-c}=o\bigl(k^{-\alpha}\bigr)$（对任何 $\alpha$），我们得到

$$
I_{k}=I_{k,\mathrm{left}}+I_{k,\mathrm{right}}=C\,\Gamma(b)\,k^{-b}\;+\;O\bigl(k^{-b-\min(1,\theta)}\bigr).
$$

于是

$$
1-\operatorname{pass_{\mathcal{D}}@k}=I_{k}\;\;\sim\;\;C\,\Gamma(b)\,k^{-b}.
$$

#### 最终的负对数论证。

由于

$$
\operatorname{pass_{\mathcal{D}}@k}=1-I_{k}=1-\bigl(C\,\Gamma(b)\,k^{-b}+O\bigl(k^{-b-\min(1,\theta)}\bigr)\bigr),
$$

对大的 $k$ 它非常接近 1。则

$$
-\log\Bigl(\operatorname{pass_{\mathcal{D}}@k}\Bigr)=-\log\Bigl(1-C\,\Gamma(b)\,k^{-b}+\cdots\Bigr).
$$

利用当 $x\to 0$ 时的展开 $-\log(1-x)=x+O(x^{2})$，此处 $x=C\,\Gamma(b)\,k^{-b}$，我们得到

$$
-\log\Bigl(\operatorname{pass_{\mathcal{D}}@k}\Bigr)=C\,\Gamma(b)\,k^{-b}+o\bigl(k^{-b}\bigr).
$$

用包含首系数的「$\sim$」记号：

$$
-\log\Bigl(\operatorname{pass_{\mathcal{D}}@k}\Bigr)\;\sim\;C\,\Gamma(b)\;k^{-b}.
$$

证毕。∎

### E.9 由 $\operatorname{pass_{i}@1}$ 的分布导出幂律缩放的必要条件

###### 定理 E.2.

设 $\mathcal{D}$ 为 $[0,1]$ 上的概率分布，PDF $f(p)$ 在 $p=0$ 附近满足以下正则性：

- 在 $p=0$ 处没有点质量。即 $\int_{0}^{1}f(p)\,\mathrm{d}p=1$，且 $f$ 是 $(0,1]$ 上真正的 PDF。
- 在 $p=0$ 附近连续且非负。存在 $\delta>0$ 使 $f$ 在 $[0,\delta]$ 上连续，且没有破坏可积性的病态振荡或奇点。

定义 $k$ 次尝试下的聚合成功率：

$$
\operatorname{pass_{\mathcal{D}}@k}\;\defeq\;\int_{0}^{1}\Bigl[\,1-(1-p)^{k}\Bigr]\,f(p)\,\mathrm{d}p
$$

以及相关量

$$
I_{k}\;\;\defeq\;\;\int_{0}^{1}(1-p)^{k}\,f(p)\,\mathrm{d}p\;=\;1-\operatorname{pass_{\mathcal{D}}@k}.
$$

假设存在常数 $A>0$ 与 $b>0$，使得对大的 $k$：

$$
-\log\bigl(\operatorname{pass_{\mathcal{D}}@k}\bigr)\;\;\sim\;\;A\,k^{-b}
$$

那么

$$
I_{k}\;=\;A\,k^{-b}+o\bigl(k^{-b}\bigr),
$$

且在上述温和正则性假设下，

$$
f(p)\;\;\sim\;\;\frac{A}{\,\Gamma(b)\,}\;p^{\,b-1}\quad\text{当 }p\to 0^{+}.
$$

###### 证明.

步骤 1. 把 $I_{k}$ 与 $-\log(\operatorname{pass_{\mathcal{D}}@k})$ 联系起来。由定义，

$$
\operatorname{pass_{\mathcal{D}}@k}\;=\;1-I_{k},\quad I_{k}\;=\;\int_{0}^{1}(1-p)^{k}\,f(p)\,\mathrm{d}p.
$$

由于

$$
-\log\Bigl(\operatorname{pass_{\mathcal{D}}@k}\Bigr)\;\;\sim\;\;A\,k^{-b},
$$

对大的 $k$，我们有

$$
\operatorname{pass_{\mathcal{D}}@k}\;=\;\exp\bigl(-A\,k^{-b}\,(1+o(1))\bigr).
$$

当 $x$ 小时，$\exp(-x)=1-x+O(x^{2})$。于是

$$
I_{k}\;=\;1-\operatorname{pass_{\mathcal{D}}@k}\;=\;A\,k^{-b}+o\bigl(k^{-b}\bigr).
$$

故

$$
I_{k}\;\;\sim\;\;A\,k^{-b}.
$$

步骤 2. 限制到 $p=0$ 附近的小区间。由于 $(1-p)^{k}$ 在 $p$ 达到 $1/k$ 量级或更大后指数衰减，我们拆分：

$$
I_{k}\;\defeq\;\int_{0}^{1}(1-p)^{k}\,f(p)\,\mathrm{d}p\;=\;\int_{0}^{c/k}(1-p)^{k}\,f(p)\,\mathrm{d}p\;+\;\int_{c/k}^{1}(1-p)^{k}\,f(p)\,\mathrm{d}p\;\defeq\;I_{k,\mathrm{left}}+I_{k,\mathrm{right}},
$$

其中 $c$ 为某个正常数。在区域 $p\geq c/k$ 上，$(1-p)^{k}\leq e^{-k\,p}\leq e^{-c}$，故

$$
I_{k,\mathrm{right}}\;\leq\;e^{-c}\;\int_{0}^{1}f(p)\,\mathrm{d}p\;=\;e^{-c}.
$$

由于 $c>0$ 可以取大，$e^{-c}$ 可以被压到 $1/k$ 的任何固定幂之下。于是对 $\Theta(k^{-b})$ 行为，主要贡献来自 $[0,c/k]$。因此

$$
I_{k}\;=\;I_{k,\mathrm{left}}\;+\;o\bigl(k^{-m}\bigr)\;\;\text{对每个 }m>0
$$

步骤 3. 换元并控制 $(1-p)^{k}$ 与 $e^{-kp}$ 之比。

(a) 与 $e^{-kp}$ 的比。对 $p\in\bigl[0,\tfrac{c}{k}\bigr]$，定义比值

$$
R_{k}(p)\;\;\defeq\;\;\frac{(1-p)^{k}}{\,e^{-k\,p}\,}.
$$

我们将证明对大的 $k$，$R_{k}(p)$ 在 $p\in[0,c/k]$ 上一致地接近 $1$。事实上，

$$
(1-p)^{k}\;=\;\exp\Bigl[k\,\log(1-p)\Bigr],\quad\log(1-p)\;=\;-\,p\;-\;\frac{p^{2}}{2}\;-\;\frac{p^{3}}{3}\;-\;\dots\,.
$$

于是

$$
\log(1-p)+p\;=\;-\frac{p^{2}}{2}\;-\;\frac{p^{3}}{3}\;-\;\dots\;\;=\;\;O\bigl(p^{2}\bigr)\quad\text{当 }p\to 0.
$$

乘以 $k$，得

$$
k\,\bigl[\log(1-p)+p\bigr]\;=\;O\bigl(k\,p^{2}\bigr).
$$

由于 $0\leq p\leq\tfrac{c}{k}$ 蕴含 $k\,p^{2}\leq\tfrac{c^{2}}{k}$，它随 $k\to\infty$ 而 $\to 0$，可得

$$
k\,\log(1-p)\;=\;-k\,p+O\bigl(\tfrac{1}{k}\bigr).
$$

取指数：

$$
(1-p)^{k}\;=\;e^{-\,k\,p}\,\exp\Bigl(O\bigl(\tfrac{1}{k}\bigr)\Bigr)\;=\;e^{-\,k\,p}\Bigl[\,1+O\bigl(\tfrac{1}{k}\bigr)\Bigr].
$$

于是

$$
R_{k}(p)\;=\;\frac{(1-p)^{k}}{\,e^{-k\,p}\,}\;=\;1+O\bigl(\tfrac{1}{k}\bigr),
$$

且 $O(\tfrac{1}{k})$ 界对所有 $p\in[0,c/k]$ 一致。换言之，存在某个常数 $M>0$（与 $k$ 无关）使得

$$
\bigl|R_{k}(p)-1\bigr|\;\leq\;\frac{M}{k}\quad\text{对所有 }p\in\Bigl[0,\frac{c}{k}\Bigr].
$$

(b) 用 $R_{k}(p)$ 表示积分。于是在 $[0,c/k]$ 上，

$$
(1-p)^{k}\,f(p)\;=\;e^{-k\,p}\,R_{k}(p)\,f(p).
$$

于是

$$
I_{k,\mathrm{left}}\;=\;\int_{0}^{c/k}e^{-k\,p}\,f(p)\,R_{k}(p)\,\mathrm{d}p.
$$

定义 $\Delta_{k}(p)\defeq R_{k}(p)-1$，它满足 $|\Delta_{k}(p)|\leq M/k$。则

$$
I_{k,\mathrm{left}}=\int_{0}^{c/k}e^{-k\,p}\,f(p)\,\mathrm{d}p\;\;+\;\;\int_{0}^{c/k}e^{-k\,p}\,f(p)\,\Delta_{k}(p)\,\mathrm{d}p. \tag{43}
$$

步骤 4. 换元 $u=k\,p$ 并导出 $f(p)\sim p^{\,b-1}$。

(a) 主部。聚焦于式 (43) 的第一项：

$$
\int_{0}^{c/k}e^{-k\,p}\,f(p)\,\mathrm{d}p.
$$

代入 $u\defeq k\,p$，则 $p=\tfrac{u}{k}$、$\mathrm{d}p=\tfrac{1}{k}\,\mathrm{d}u$。上限 $p=\tfrac{c}{k}$ 变为 $u=c$。于是

$$
\int_{0}^{c/k}e^{-k\,p}\,f(p)\,\mathrm{d}p=\int_{0}^{c}e^{-u}\,f\Bigl(\frac{u}{k}\Bigr)\,\frac{\mathrm{d}u}{\,k\,}.
$$

于是

$$
\int_{0}^{c/k}e^{-k\,p}\,f(p)\,\mathrm{d}p=\frac{1}{k}\,\int_{0}^{c}e^{-u}\,f\Bigl(\frac{u}{k}\Bigr)\,\mathrm{d}u.
$$

(b) 误差部分。式 (43) 的第二项中 $\Delta_{k}(p)=R_{k}(p)-1$ 满足 $|\Delta_{k}(p)|\leq\frac{M}{k}$。故

$$
\left|\int_{0}^{c/k}e^{-k\,p}\,f(p)\,\Delta_{k}(p)\,\mathrm{d}p\right|\;\leq\;\frac{M}{\,k\,}\,\int_{0}^{c/k}e^{-k\,p}\,f(p)\,\mathrm{d}p.
$$

而积分 $\int_{0}^{c/k}e^{-k\,p}\,f(p)\,\mathrm{d}p$ 正是我们刚才考虑的主部。于是误差被 $\frac{M}{k}$ 乘以一个将被证明是 $\Theta(k^{-b})$ 的项所界。因此只要不是 $b<1$ 的情形误差就是次主导的——而即便是那种情形，我们也能系统地跟踪它。

综合两项，我们得到

$$
I_{k,\mathrm{left}}\;=\;\frac{1}{k}\int_{0}^{c}e^{-u}\,f\Bigl(\frac{u}{k}\Bigr)\,\mathrm{d}u\;+\;O\bigl(\tfrac{1}{k}\cdot\text{（主积分）}\bigr). \tag{44}
$$

(c) 匹配 $\Theta(k^{-b})$。由于 $I_{k}=I_{k,\mathrm{left}}+I_{k,\mathrm{right}}$ 且 $I_{k,\mathrm{right}}$ 可忽略，我们有

$$
I_{k}\;=\;\frac{1}{k}\int_{0}^{c}e^{-u}\,f\Bigl(\tfrac{u}{k}\Bigr)\,\mathrm{d}u\;+\;\text{（小修正）}.
$$

但由假设 $I_{k}\sim\alpha\,k^{-b}$。于是

$$
k\cdot I_{k}\;=\;\int_{0}^{c}e^{-u}\,f\Bigl(\tfrac{u}{k}\Bigr)\,\mathrm{d}u\;+\;\text{（更小的项）}\;\;\sim\;\;\alpha\,k^{1-b}. \tag{45}
$$

因此表达式

$$
\int_{0}^{c}e^{-u}\,f\Bigl(\tfrac{u}{k}\Bigr)\,\mathrm{d}u
$$

对大的 $k$ 必须是 $\Theta\bigl(k^{\,1-b}\bigr)$。由于 $0\leq u\leq c$ 时 $\tfrac{u}{k}$ 很小，我们实际上是在 $0$ 附近采样 $f$。要使积分产生 $k^{\,1-b}$，我们推得

$$
f\Bigl(\tfrac{u}{k}\Bigr)\;\;=\;\;\Theta\Bigl(\Bigl(\tfrac{u}{k}\Bigr)^{b-1}\Bigr),
$$

即 $f$ 在 $p=0$ 附近必须表现得像 $p^{\,b-1}$。改写前面的常数，可得

$$
f\Bigl(\tfrac{u}{k}\Bigr)\;=\;\Bigl(\tfrac{u}{k}\Bigr)^{b-1}\,\bigl[\text{某个正常数}\bigr].
$$

（然后我们通过精确匹配积分，把该常数识别为 $\frac{\alpha}{\Gamma(b)}$，与前面的论证一样。）

步骤 5. 结论。我们已证明在 $p\in[0,c/k]$ 上，

$$
(1-p)^{k}=e^{-k\,p}\,\bigl[\,1+O(\tfrac{1}{k})\bigr],
$$

并且积分后，$I_{k}$ 所需的 $k^{-b}$ 形式迫使

$$
f(p)\;=\;\frac{A}{\Gamma(b)}\,p^{\,b-1}\;+\;o\bigl(p^{\,b-1}\bigr),\quad\text{当 }p\to 0^{+}.
$$

这完成了必要性证明。∎

注（温和正则性）。若 $f$ 在 $0$ 附近有奇怪的振荡或不可积的奇点，积分 $\int_{0}^{1}(1-p)^{k}\,f(p)\,\mathrm{d}p$ 可能不会产生干净的 $k^{-b}$。通常我们施加单调性或至少在 $p=0$ 附近的连续性、$p=0$ 处无原子，以及当 $b>1$ 时 $f(0)=0$ 或当 $b=1$ 时 $f(0)>0$ 等。这些假设排除了病态行为，并保证 $f(p)$ 的局部形状产生干净的幂律。

## 附录 F 缩放 Beta-Binomial 分布的极大似然估计

为建模 $\operatorname{pass_{i}@1}$ 的分布，我们可以对缩放的三参数 Beta-Binomial 分布做极大似然估计。我们选择它，是因为对第 $i$ 道题的每次尝试是以成功概率 $\operatorname{pass_{i}@1}$ 的独立同分布伯努利随机变量；而引入尺度参数是因为最大的 $\operatorname{pass_{i}@1}$ 值通常比 1.0（未缩放 Beta 分布支撑的最大值）小 1-2 个数量级。

更详细地，作为背景，四参数 Beta 分布的 PDF 为

$$
p_{Y}(y;\alpha,\beta,a,c)\defeq\frac{(y-a)^{\alpha-1}(c-y)^{\beta-1}}{(c-a)^{\alpha+\beta-1}\operatorname{B}(\alpha,\beta)}, \tag{46}
$$

其中 $\operatorname{B}(\cdot,\cdot)$ 是 Beta 函数。若最小值 $a$ 固定为 $0$ 且最大值 $c$ 约束为 $a<c<1$，则缩放的三参数 Beta 分布简化为：

$$
f_{P}(p;\alpha,\beta,a=0,c)=\frac{p^{\alpha-1}(c-p)^{\beta-1}}{c^{\alpha+\beta-1}\operatorname{B}(\alpha,\beta)}. \tag{47}
$$

我们要基于这一缩放 Beta 分布的三参数 Beta-Binomial 分布的 PMF。对 $n$ 次采样、$x$ 次成功，PMF 为：

$$
P(X=x;\alpha,\beta,c,n)
\defeq\int_{0}^{c}\binom{n}{x}\,p^{x}\,(1-p)^{n-x}\,f_{P}(p;\alpha,\beta,a=0,c)\,dp \tag{48}
$$

$$
=\binom{n}{x}\frac{1}{c^{\alpha+\beta-1}\operatorname{B}(\alpha,\beta)}\int_{0}^{c}p^{x+\alpha-1}\,(1-p)^{n-x}\,(c-p)^{\beta-1}\,dp. \tag{49}
$$

利用换元 $p\defeq c\,z$，该 PMF 可改写为

$$
P(X=x;\alpha,\beta,c,n)
=\binom{n}{x}\frac{c^{x}}{\operatorname{B}(\alpha,\beta)}\int_{0}^{1}z^{x+\alpha-1}\,(1-z)^{\beta-1}\,(1-cz)^{n-x}\,dz \tag{50}
$$

$$
=\binom{n}{x}\;\frac{c^{x}\mathrm{B}\bigl(x+\alpha,\;\beta\bigr)}{\mathrm{B}(\alpha,\beta)}\;{}_{2}F_{1}\Bigl(-(n-x),\;x+\alpha;\;x+\alpha+\beta;\;c\Bigr), \tag{51}
$$

其中 ${}_{2}F_{1}(\cdot,\cdot;\cdot;\cdot)$ 是（高斯）超几何函数。

## 附录 G 缩放 Kumaraswamy-Binomial 分布的极大似然估计

为建模 $\operatorname{pass_{i}@1}$ 的分布，我们可以对缩放的三参数 Kumaraswamy-Binomial 分布做极大似然估计。我们选择它，是因为对第 $i$ 道题的每次尝试是以成功概率 $\operatorname{pass_{i}@1}$ 的独立同分布 Kumaraswamy 随机变量；而引入尺度参数是因为最大的 $\operatorname{pass_{i}@1}$ 值通常比 1.0（未缩放 Beta 分布支撑的最大值）小 1-2 个数量级。

更详细地，缩放的三参数 Kumaraswamy 分布简化为：

$$
f_{P}(p;\alpha,\beta,a=0,c)=\frac{\alpha\beta}{c^{\alpha}}\,p^{\alpha-1}\,(1-(p/c)^{\alpha})^{\beta-1}, \tag{52}
$$

支撑为 $(0,c)$。重标度的 Kumaraswamy-Binomial 分布则有 PMF：

$$
P(X=x;\alpha,\beta,c,n)=\binom{n}{x}\;\frac{\alpha\,\beta}{c^{\alpha}}\int_{0}^{c}p^{\,x+\alpha-1}\,(1-p)^{n-x}\,\Bigl(1-\bigl(\tfrac{p}{c}\bigr)^{\alpha}\Bigr)^{\beta-1}\,dp. \tag{53}
$$

可以做换元 $p\defeq cz$，但化简后得到的是超几何函数之和，几乎不增加概念上的清晰度，因此我们借助 Python 的 mpmath 库（mpmath development team, 2023）做数值积分。

## 附录 H 缩放 Beta-负二项分布的极大似然估计

为建模 $\operatorname{pass_{i}@1}$ 的分布，我们可以对缩放的三参数 Beta-负二项分布做极大似然估计。回顾缩放的三参数 Beta 分布为：

$$
f_{P}(p;\alpha,\beta,a=0,c)=\frac{p^{\alpha-1}(c-p)^{\beta-1}}{c^{\alpha+\beta-1}\operatorname{B}(\alpha,\beta)}. \tag{54}
$$

我们要基于这一缩放 Beta 分布的三参数 Beta-负二项分布的 PMF。对 $r$ 次期望成功，先抽得 $x$ 次失败的 PMF 为：

$$
P(X=x;\alpha,\beta,c,r)
=\;\int_{0}^{c}\underbrace{\binom{x+r-1}{x}\,p^{r}\,(1-p)^{x}}_{\text{NegBin}(r,p)}\;\;\underbrace{\frac{p^{\alpha-1}\,(c-p)^{\beta-1}}{\,c^{\alpha+\beta-1}\,\mathrm{B}(\alpha,\beta)\,}}_{\text{缩放 Beta PDF}}\;dp \tag{55}
$$

$$
=\;\binom{x+r-1}{x}\;\frac{1}{c^{\alpha+\beta-1}\,\mathrm{B}(\alpha,\beta)}\int_{0}^{c}p^{\,r+\alpha-1}\,\bigl(1-p\bigr)^{x}\,\bigl(c-p\bigr)^{\beta-1}\;dp. \tag{56}
$$

接着，代入 $p=c\,z\Longrightarrow dp=c\,dz$，把定义域 $[0,c]$ 重标度为 $[0,1]$。在此变换下：

$$
p^{\,r+\alpha-1}\;=\;(c\,z)^{\,r+\alpha-1}\;=\;c^{\,r+\alpha-1}\;z^{\,r+\alpha-1},
$$

$$
(c-p)^{\beta-1}\;=\;\bigl(c-c\,z\bigr)^{\beta-1}\;=\;\bigl(c(1-z)\bigr)^{\beta-1}\;=\;c^{\,\beta-1}\,(1-z)^{\beta-1},
$$

$$
(1-p)^{x}\;=\;\bigl(1-c\,z\bigr)^{x}.
$$

把这些代入被积函数：

$$
p^{\,r+\alpha-1}\,\bigl(1-p\bigr)^{x}\,\bigl(c-p\bigr)^{\beta-1}\,dp=\;\Bigl(c^{\,r+\alpha-1}\,z^{\,r+\alpha-1}\Bigr)\;\Bigl(\bigl(1-cz\bigr)^{x}\Bigr)\;\Bigl(c^{\,\beta-1}\,(1-z)^{\beta-1}\Bigr)\;\bigl(c\,dz\bigr).
$$

把 $c$ 的常数因子提出来：

$$
=\;c^{\,r+\alpha-1}\;c^{\,\beta-1}\;c\;\;z^{\,r+\alpha-1}\,(1-cz)^{x}\,(1-z)^{\beta-1}\;dz.
$$

由于 $c^{\,r+\alpha-1}\cdot c^{\,\beta-1}\cdot c\;=\;c^{\,r+\alpha+\beta-1}$，我们得到

$$
p^{\,r+\alpha-1}\,(1-p)^{x}\,(c-p)^{\beta-1}\,dp\;=\;c^{\,r+\alpha+\beta-1}\,\,z^{\,r+\alpha-1}\,(1-z)^{\beta-1}\,(1-cz)^{x}\;\,dz.
$$

代回 $P(X=x;\alpha,\beta,c,r)$ 并化简：

$$
P(X=x;\alpha,\beta,c,r)=\;\binom{x+r-1}{x}\;\frac{c^{r}}{\mathrm{B}(\alpha,\beta)}\;\;\int_{0}^{1}z^{\,r+\alpha-1}\,(1-z)^{\beta-1}\,\bigl(1-c\,z\bigr)^{x}\,dz. \tag{57}
$$

我们可以用（高斯）超几何函数 ${}_{2}F_{1}(\cdot,\cdot;\cdot;\cdot)$ 重新表达：

$$
P(X=x;\alpha,\beta,c,r)\;=\;\binom{x+r-1}{x}\;\frac{c^{r}\,\mathrm{B}\bigl(r+\alpha,\;\beta\bigr)}{\mathrm{B}\bigl(\alpha,\;\beta\bigr)}\;\;{}_{2}F_{1}\!\Bigl(-x,\;r+\alpha;\;r+\alpha+\beta;\;c\Bigr). \tag{58}
$$
