---
title: "AlphaGo 的创新"
title_en: "Innovations of AlphaGo"
source: https://deepmind.google/blog/innovations-of-alphago/
site: deepmind
date: 2017-04-10
crawled: 2026-09-13
translated: 2026-09-13
---

# AlphaGo 的创新

> 原文：[Innovations of AlphaGo](https://deepmind.google/blog/innovations-of-alphago/) · Google DeepMind

AI 最伟大的承诺之一，是它有潜力帮助我们在复杂领域发掘新知识。我们已经看到了一些令人兴奋的苗头：我们的算法找到了大幅优化[数据中心](https://deepmind.com/blog/article/deepmind-ai-reduces-google-data-centre-cooling-bill-40)能源使用的办法——当然还有我们的程序 AlphaGo。

自去年 3 月在首尔取得历史性的胜利以来，AlphaGo 为古老的围棋开启了一个新纪元。多亏 AlphaGo 那些富有创造性、引人入胜的着法，各个水平的棋手都受到启发，去尝试属于自己的新手筋与新策略，并在此过程中常常重新审视沿袭数百年的既有知识。

在"[乌镇围棋未来峰会](https://deepmind.com/blog/article/exploring-mysteries-alphago)"召开之前，我们在这里总结 AlphaGo 近期在战略与战术上的一些创新，以及它们所揭示的新洞见。

> AlphaGo 去年的对局改变了围棋这个行业和棋手们。AlphaGo 展现出的水平远远超出我们的预期，为这项游戏带来了许多新的元素。

时越（Shi Yue）

职业九段，世界冠军

> 我认为棋手们或多或少都受到了"Alpha 老师"的影响。AlphaGo 的棋让我们感到更加自由，不再有任何一手棋是不可下的。现在每个人都在尝试以前从未尝试过的棋风。

周睿羊（Zhou Ruiyang）

职业九段，世界冠军

## AlphaGo 的棋风

AlphaGo 最大的长处并不在于某一步棋或某一个次序，而在于它为每一盘棋带来的独特视角。围棋的"棋风"很难一言以蔽之，但可以说 AlphaGo 的战略体现了一种灵活与开放的精神：它不带先入之见，因此能够找到最有效的行棋路线。正如下面两盘棋将要展示的，这种理念常常引导 AlphaGo 发现那些看似违反直觉、实则威力巨大的着法。

虽然围棋是争夺地域的游戏，但大多数决定性的战斗都取决于棋块之间力量的平衡，而 AlphaGo 恰恰擅长塑造这种平衡。具体来说，AlphaGo 极为精妙地运用"外势"（influence），即现有棋子对周边区域的影响。虽然外势无法被精确度量，但 AlphaGo 的价值网络让它能够同时顾及盘上所有棋子，赋予其判断细腻与精准。这些能力让 AlphaGo 能够把局部的外势转化为相互配合的全局优势。

在这盘棋（参考图 1）中，黑棋（AlphaGo）几乎没有确定的地域，而白棋已占三个角，但黑棋的外势辐射全盘。尤其是，图中标注的交换虽然巩固了白棋，但同时也提升了黑棋的潜力。围棋棋手通常对这类交换避之不及，因为它要用确定的代价去换取不确定的收益，而 AlphaGo 凭借其卓越的判断力与对风险收益的敏锐嗅觉，让这样的下法成为可能。

![参考图 1：一张围棋棋盘，展示了黑棋（AlphaGo）在白棋已占三个角的情况下仍专注于全局外势的对局，突出左上角（标注三角形的 D15 和 E15）的一处交换，该交换巩固了白棋但提升了黑棋的潜力。](https://lh3.googleusercontent.com/CySlJDiynS2jQNkDtxUNKIyKnpWmu0yCzz0WOzbfyN9cgZho-9j6rwn0PPBL7rchh8DF3Am8VnVXN4oksX91Pmv4Rov323AwLL0JgqkwMggyDApoQw=w1440)

参考图 1

然而，外势的价值完全取决于具体局面，当外势可以被有效化解时，AlphaGo 也会毫不吝惜地将其舍弃。在参考图 2 展示的这盘棋——它堪称 AlphaGo 全部对局中最令人惊讶的棋局之一——中，AlphaGo 刚刚在二路连下六子。围棋界有句老话：四线有外势，三线有实地，二路只有失败。AlphaGo 的下法乍看之下似乎正该受到这样的责难，因为这些棋给了白棋外势与厚势，换来的却只是黑棋边上可怜的 4 目地域。大多数棋手都不愿忍受下出这些标注棋子的耻辱，会立刻否定这条路线。然而 AlphaGo 判断，让白棋的棋子相互分离是值得的，并在随后的交换中，从上下两边慢慢侵蚀白棋的外势，最终确保了获胜的优势。

![参考图 2：一张围棋棋盘，展示黑棋（AlphaGo）在右边二路（S8 至 S13）连下六子（以三角形标注）以分割白棋的棋子，用局部地域换取全局战略优势。](https://lh3.googleusercontent.com/BC8pPC_yTm_hAA0Is-t1QMfeIfTPZBBEXG6xY7YlpHr03G5KlVz3sMt7Wox9UOMJMN4vWI6hCiByw_J7kufILhJXkggNsCW88KcuVUQwmqHYf5EtbA=w1440)

参考图 2

## 新手筋，新棋形

AlphaGo 在最近的棋局中还下出了几个开局的创新着法，其中最引人注目的是早期的点三三（3-3 入侵）以及"妖刀"定式的一个新变化。每一个都挑战了传统定式理论，但经过更深入的审视都被证明是成立的。

## 早期点三三

围棋中最重地域的定式（角部次序）之一就是三三点（3-3 点）入侵，如参考图 3 所示。

![参考图 3：一张围棋棋盘，展示左下角三三点入侵的初始局面，一颗以圆形标注的黑子下在 C3。](https://lh3.googleusercontent.com/3MIzG4StzP2b8FYY5jROQGXP0-4uFtWQ_CxLE_0-m0n8juAmO408YAQGVNPgVGpbp2LyoqZuwOT6iQ8SNbNEYU5vaep3zaa3qL0XuXeE8E2P323t=w1440)

参考图 3

这种入侵可以立即确保角地，但参考图 4 所示的教科书式次序长期以来被认为不适合用于开局，因为它让出的外势太多。

![参考图 4：一张围棋棋盘，展示左下角三三点入侵的传统教科书次序，C2、D2、E2 和 F3 的四颗棋子以三角形标注，以突出标准交换。](https://lh3.googleusercontent.com/-oavV6PUbglcM_AaalSqrX-UJuBGCUJPUJ1ccRsokkvPQdMOHtdBJhQVi7PTVlWJs7xk-VPtQuspC8xZb23YvFZF-4JmutoILct9cbyQFmQP-S1BYw=w1440)

参考图 4

AlphaGo 的创新在于省略了这些被标注的交换，让角地保持未定，如参考图 5 所示。

![参考图 5：一张围棋棋盘，展示 AlphaGo 在左下角创新的三三点入侵，省略了传统交换（略去 C2、D2、E2 和 F3），让角地保持未定，同时获得地域、只让出适度的外势。](https://lh3.googleusercontent.com/zpSsg08VZI_iDmYHKeHN0zdz8fDOaUmdpVqk9POYOrqjU9LCFmJDNaKnyNZr-RgtslmSXD4k2NBFFM3eYtuBp_bNVhB4V477fYW-0bbTXC3vkyXI=w1440)

参考图 5

虽然这样稍稍不够稳固，但黑棋保留着"见合"（miai，即等效可选点）：既可以在左边逃出，也可以稍后再完成定式，并且在只让出适度外势的同时获得了地域。这一策略在职业棋手中引起了巨大轰动，至少已有一位棋手在正式比赛中尝试了它（参考图 6）。

![参考图 6：一张围棋棋盘，展示一场职业正式比赛，其中采用了 AlphaGo 创新的早期三三点入侵，棋盘上以编号棋子显示行棋次序。](https://lh3.googleusercontent.com/I13hJqHmORsronaIzO27dXWNtwg56EQXqEipCUjy_h1acTDStr7-Lwe7ku7ix31Enul6s7V6r0B30joTrjGTXwPAamiAxJTtPb3w58RH2fzb9YTuAQ=w1440)

参考图 6

## 新"妖刀"

AlphaGo 最初是用人类棋谱训练的，因此熟悉现代定式，并且通常按定式行棋。然而，在"妖刀"——一个以村正妖刀命名的著名复杂定式家族——中，它选择了偏离。

从参考图 7 的局面出发，通常的结果是角地与边上的交换，如参考图 8 所示。

![参考图 7：一张围棋棋盘，展示左下角"妖刀"定式家族的起始局面，黑白棋子构成的竖直墙壁与散布在棋盘其他区域的孤立棋子。](https://lh3.googleusercontent.com/iD13DSOjjz9tedk2BaMGfEe_8Kis8yG2Wci1EfFIArlntFDLhQiwyivtE8HZIv1agb2w44XbNZ_m0XgzdjstgDIz5dS6SxIi-5krwenT1l1L5O8vrw=w1440)

参考图 7

![参考图 8：一张围棋棋盘，展示"妖刀"定式的传统次序，右下角与边上交换，编号棋子展示了标准的结果。](https://lh3.googleusercontent.com/dF0VF0Au0Kd398prcyoLmJg9FCN3UPZQVBoGO7xMc6dRKBVdVNtXB6QO86kS5Gc2tyFE5IhOIVSRJIgkRGkmdV0yF0bmjm1Zio3JYTCBiqZKElRgYbc=w1440)

参考图 8

然而，AlphaGo 往往更愿意舍弃向外的出路，以换取地域补偿（参考图 9）。

![参考图 9：一张围棋棋盘，展示 AlphaGo 在右下角的"妖刀"替代次序，白棋舍弃向外的出路以换取地域补偿，编号棋子（1 至 19）详细列出行棋次序。](https://lh3.googleusercontent.com/uCn19SkcM2gyKQEb3nKUYYWpTaEdYwSuGBg9Ms4aeQWZ40uH4-kH5sWwxbJFJP98LLGXfb800z4ZqteTj_BrsEL-IrB1dtjxtisY1KWcBG0tVxTd=w1440)

参考图 9

大多数围棋棋手都不会考虑下这个变化，因为它给了黑棋一道厚实的墙，但白棋后续的挂角表明，黑棋外势的价值并不像看上去那么大。如果黑棋不补强这道墙，它甚至可能成为被打入的目标。韩国顶尖职业棋手之一的金志锡（Kim Jiseok）最近就在一场比赛中下出了这条路线（参考图 10），并且最终赢下了那盘棋。

![参考图 10：一张围棋棋盘，展示韩国职业棋手金志锡的一场比赛，他在右下角采用了 AlphaGo 的"妖刀"替代次序，棋盘上以编号棋子显示行棋次序。](https://lh3.googleusercontent.com/i9PZqg2wDS8M-J1Vl7DhNPSgD1e6RhTwYmx1lkMHwwb5FSrVrSwMw5BzbjJRThuAZKJ9v_suiu6A7svr6-VzHGIZ-LH-qyiKgmAeA9OIjaXHG9CSsQ=w1440)

参考图 10

## 更多精彩还在后面

AlphaGo 的创新显示出在职业围棋界产生巨大影响的潜力，我们希望在即将于乌镇举行的围棋未来峰会上呈现更多合作研究的机会。我们满怀兴奋地期待 AlphaGo 与人类职业棋手一道努力，去发现围棋的真正本质。
