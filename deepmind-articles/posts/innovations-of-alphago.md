---
title: "Innovations of AlphaGo"
source: https://deepmind.google/blog/innovations-of-alphago/
site: deepmind
date: 2017-04-10
authors: Lucas Baker, Fan Hui
crawled: 2026-09-13
---

One of the great promises of AI is its potential to help us unearth new knowledge in complex domains. We’ve already seen exciting glimpses of this, when our algorithms found ways to dramatically improve energy use in [data centres](https://deepmind.com/blog/article/deepmind-ai-reduces-google-data-centre-cooling-bill-40) - as well as of course with our program AlphaGo.

Since its historic success in Seoul last March, AlphaGo has heralded a new era for the ancient game of Go. Thanks to AlphaGo's creative and intriguing revelations, players of all levels have been inspired to test out new moves and strategies of their own, often re-evaluating centuries of inherited knowledge in the process.

Ahead of ‘[The Future of Go Summit in Wuzhen](https://deepmind.com/blog/article/exploring-mysteries-alphago)’, we summarise some recent examples of AlphaGo’s strategic and tactical innovations, and the new insights they have revealed.

> AlphaGo’s game last year transformed the industry of Go and its players. The way AlphaGo showed its level was far above our expectations and brought many new elements to the game.

Shi Yue

9 Dan Professional, World Champion

> I believe players more or less have all been affected by Professor Alpha. AlphaGo’s play makes us feel more free and no move is impossible to play anymore. Now everyone is trying to play in a style that hasn’t been tried before.

Zhou Ruiyang

9 Dan Professional, World Champion

## AlphaGo Style

AlphaGo's greatest strength is not any one move or sequence, but rather the unique perspective that it brings to every game. While Go style is difficult to encapsulate, one could say that AlphaGo's strategy embodies a spirit of flexibility and open-mindedness: a lack of preconceptions that allows it to find the most effective line of play. As the following two games will show, this philosophy often leads AlphaGo to discover counterintuitive yet powerful moves.

Although Go is a game of territory, most decisive battles hinge on the balance of power between groups, and AlphaGo excels in shaping this balance. Specifically, AlphaGo makes masterful use of "influence," or the effect of existing stones on surrounding areas. Although influence cannot be measured exactly, AlphaGo's value network enables it to consider all stones on the board at once, endowing its judgment with subtlety and precision. These abilities let AlphaGo convert local regions of influence into coordinated global advantages.

In this game (Dia. 1), Black (AlphaGo) has little secure territory, while White has three corners, but Black's influence radiates across the entire board. In particular, while the marked exchange solidifies White, it also improves Black's potential. Go players usually shy from such exchanges, which pay a definite price for uncertain profit, but AlphaGo combines its sterling judgment with a keen sense of risk and reward to make such moves possible.

![Dia. 1: A Go board showing a game where Black (AlphaGo) focuses on global influence despite White securing three corners, highlighting a marked exchange on the upper-left (D15 and E15 marked with triangles) that solidifies White but improves Black's potential.](https://lh3.googleusercontent.com/CySlJDiynS2jQNkDtxUNKIyKnpWmu0yCzz0WOzbfyN9cgZho-9j6rwn0PPBL7rchh8DF3Am8VnVXN4oksX91Pmv4Rov323AwLL0JgqkwMggyDApoQw=w1440)

Dia. 1

However, the value of influence depends entirely on context, and AlphaGo relinquishes influence freely when it can be effectively mitigated. In the the game displayed in Dia. 2, one of the most surprising in its oeuvre, AlphaGo has just played an incredible six stones along the second line. Go players have a saying: on the fourth line there is influence, and on the third line there is territory, but on the second line there is only defeat. AlphaGo's play at first looks deserving of such censure, as these moves give White both strength and influence in exchange for Black's paltry 4 points of side territory. Most players, unwilling to bear the ignominy of playing the marked stones, would reject this line in an instant. Yet AlphaGo judges it worthwhile to keep White's stones separated, and in the following exchanges, slowly erodes White's influence from the top and bottom to secure a winning advantage.

![Dia. 2: A Go board showing Black (AlphaGo) playing six stones marked with triangles along the second line on the right side (S8 to S13) to separate White's stones, trading local territory for global strategic advantage.](https://lh3.googleusercontent.com/BC8pPC_yTm_hAA0Is-t1QMfeIfTPZBBEXG6xY7YlpHr03G5KlVz3sMt7Wox9UOMJMN4vWI6hCiByw_J7kufILhJXkggNsCW88KcuVUQwmqHYf5EtbA=w1440)

Dia. 2

## New Moves, New Patterns

AlphaGo has also played several opening novelties in its recent games, the most salient being the early 3-3 invasion and a new variation of the "Magic Sword". Each defies conventional theory, but proves sound on deeper inspection.

## The Early 3-3 Invasion

One of the most territorial joseki (corner sequences) in Go is the 3-3 point invasion, shown in Dia. 3.

![Dia. 3: A Go board showing the initial setup of a 3-3 point invasion in the bottom-left corner, with a black stone marked with a circle played at C3.](https://lh3.googleusercontent.com/3MIzG4StzP2b8FYY5jROQGXP0-4uFtWQ_CxLE_0-m0n8juAmO408YAQGVNPgVGpbp2LyoqZuwOT6iQ8SNbNEYU5vaep3zaa3qL0XuXeE8E2P323t=w1440)

Dia. 3

This invasion immediately secures the corner, but the textbook sequence shown in Dia. 4 has long been disparaged as unsuitable for the opening, as it gives too much influence.

![Dia. 4: A Go board showing the traditional, textbook sequence of a 3-3 point invasion in the bottom-left corner, with four stones at C2, D2, E2, and F3 marked with triangles to highlight the standard exchanges.](https://lh3.googleusercontent.com/-oavV6PUbglcM_AaalSqrX-UJuBGCUJPUJ1ccRsokkvPQdMOHtdBJhQVi7PTVlWJs7xk-VPtQuspC8xZb23YvFZF-4JmutoILct9cbyQFmQP-S1BYw=w1440)

Dia. 4

AlphaGo's innovation is to omit the marked exchanges, leaving the corner unsettled as shown in Dia. 5.

![Dia. 5: A Go board showing AlphaGo's innovative 3-3 point invasion in the bottom-left corner, omitting the traditional exchanges (leaving out C2, D2, E2, and F3) to keep the corner unsettled while gaining territory and ceding only moderate influence.](https://lh3.googleusercontent.com/zpSsg08VZI_iDmYHKeHN0zdz8fDOaUmdpVqk9POYOrqjU9LCFmJDNaKnyNZr-RgtslmSXD4k2NBFFM3eYtuBp_bNVhB4V477fYW-0bbTXC3vkyXI=w1440)

Dia. 5

Though slightly less secure, Black retains miai (options) to escape on the left or finish the joseki later, and has gained territory while ceding only moderate influence. This strategy has created a great stir among professionals, and at least one has already tried it in an official game (Dia. 6).

![Dia. 6: A Go board showing an official professional game where AlphaGo's innovative early 3-3 point invasion has been adopted, with the numbered stones displaying the sequence of play on the board.](https://lh3.googleusercontent.com/I13hJqHmORsronaIzO27dXWNtwg56EQXqEipCUjy_h1acTDStr7-Lwe7ku7ix31Enul6s7V6r0B30joTrjGTXwPAamiAxJTtPb3w58RH2fzb9YTuAQ=w1440)

Dia. 6

## The New Magic Sword

Originally trained on human data, AlphaGo knows modern joseki and usually plays accordingly. However, in the "Magic Sword," a famously complex joseki family named for the cursed sword of Muramasa, it diverges.

Starting from the position in Dia. 7, the usual result exchanges the corner for the side as shown in Dia. 8.

![Dia. 7: A Go board showing the starting position of the "Magic Sword" joseki family in the bottom-left corner, featuring a vertical wall of black and white stones alongside isolated stones placed across other areas of the board.](https://lh3.googleusercontent.com/iD13DSOjjz9tedk2BaMGfEe_8Kis8yG2Wci1EfFIArlntFDLhQiwyivtE8HZIv1agb2w44XbNZ_m0XgzdjstgDIz5dS6SxIi-5krwenT1l1L5O8vrw=w1440)

Dia. 7

![Dia. 8: A Go board showing the traditional sequence for the "Magic Sword" joseki, where the bottom-right corner is exchanged for the side with numbered stones illustrating the standard outcome.](https://lh3.googleusercontent.com/dF0VF0Au0Kd398prcyoLmJg9FCN3UPZQVBoGO7xMc6dRKBVdVNtXB6QO86kS5Gc2tyFE5IhOIVSRJIgkRGkmdV0yF0bmjm1Zio3JYTCBiqZKElRgYbc=w1440)

Dia. 8

However, AlphaGo often prefers to sacrifice outside access for territorial compensation (Dia. 9).

![Dia. 9: A Go board showing AlphaGo's alternative "Magic Sword" sequence in the bottom-right corner, where White sacrifices outside access for territorial compensation, with numbered stones (1 to 19) detailing the moves played.](https://lh3.googleusercontent.com/uCn19SkcM2gyKQEb3nKUYYWpTaEdYwSuGBg9Ms4aeQWZ40uH4-kH5sWwxbJFJP98LLGXfb800z4ZqteTj_BrsEL-IrB1dtjxtisY1KWcBG0tVxTd=w1440)

Dia. 9

Most Go players would not consider playing this variation, as it gives Black a powerful wall, but White's follow-up approach declares that Black's influence is not as valuable as it looks. If Black does not reinforce the wall, it may even become a target. Kim Jiseok, one of Korea's top professionals, recently played this line in a tournament game (Dia. 10), which he went on to win.

![Dia. 10: A Go board showing a tournament game played by Korean professional Kim Jiseok, who adopted AlphaGo's alternative "Magic Sword" sequence in the bottom-right corner, with numbered stones displaying the sequence of play on the board.](https://lh3.googleusercontent.com/i9PZqg2wDS8M-J1Vl7DhNPSgD1e6RhTwYmx1lkMHwwb5FSrVrSwMw5BzbjJRThuAZKJ9v_suiu6A7svr6-VzHGIZ-LH-qyiKgmAeA9OIjaXHG9CSsQ=w1440)

Dia. 10

## More to Come

AlphaGo's innovations show great potential for impact in the world of professional Go, and we hope to present many more opportunities for collaborative research at the upcoming Future of Go Summit in Wuzhen. We look forward with great excitement to AlphaGo and human professionals striving together to discover the true nature of Go.
