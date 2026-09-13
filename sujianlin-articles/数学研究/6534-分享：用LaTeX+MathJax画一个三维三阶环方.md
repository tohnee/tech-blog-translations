---
title: "分享：用LaTeX+MathJax画一个三维三阶环方"
date: "2019-03-28"
author: "苏剑林"
category: "数学研究"
tags: ["趣味", "幻方", "分享"]
url: "https://kexue.fm/archives/6534"
blog: "科学空间 | Scientific Spaces"
---

昨天看到数学研发论坛在讨论[三维三阶幻方](https://bbs.emath.ac.cn/thread-16090-1-1.html)，论坛里的各大牛都已经讨论得差不多了，我也没什么好插话的。然后突发奇想，能不能用纯LaTeX画出一个这样的立体幻方出来？

昨天下午折腾了好一会儿，最后只抛出了个半成品，然后经过论坛的mathe大佬继续完善后，终于成功地画出来了：
$$\begin{array}{ccccccccccc}
& & & & 4 & —& —& — & — & 25 & —& —& — & — & 11
\\
& & & \require{HTML} \style{display: inline-block; transform: rotate(45deg)}{|} &\require{HTML} \style{display: inline-block; opacity:0.5;}{\color{red}{\vdots}} & && &\require{HTML} \style{display: inline-block; transform: rotate(45deg)}{|} &\require{HTML} \style{display: inline-block; opacity:0.5;}{\color{red}{\vdots}} && &&\require{HTML} \style{display: inline-block; transform: rotate(45deg)}{|} &|
\\
& & 14 & — & — & —& — & 22 & — & — & — & —& 7 & & |
\\
& \require{HTML} \style{display: inline-block; transform: rotate(45deg)}{|} & \require{HTML} \style{display: inline-block; opacity:0.5;}{\color{red}{\vdots}}& &\require{HTML} \style{display: inline-block; opacity:0.5;}{\color{red}{\vdots}} & &\require{HTML} \style{display: inline-block; transform: rotate(45deg)}{|} & \require{HTML} \style{display: inline-block; opacity:0.5;}{\color{red}{\vdots}}& &  \require{HTML} \style{display: inline-block; opacity:0.5;}{\color{red}{\vdots}}&&\require{HTML} \style{display: inline-block; transform: rotate(45deg)}{|} & | & & | \\
24 & — & —& —& — & 1 &  —& —& — & — & 18 & & | &  & |\\
|& & \require{HTML} \style{display: inline-block; opacity:0.5;}{\color{red}{\vdots}} & &\color{red}{13} &| &  \require{HTML} \style{display: inline-block; opacity:0.5;}{\color{red}{\cdots}} & \require{HTML} \style{display: inline-block; opacity:0.5;}{\color{red}{\vdots}} &\require{HTML} \style{display: inline-block; opacity:0.5;}{\color{red}{\cdots}} &\color{red}{27} & |  & \require{HTML} \style{display: inline-block; opacity:0.5;}{\color{red}{\cdots}} & | &\require{HTML} \style{display: inline-block; opacity:0.5;}{\color{red}{\cdots}}&5\\
|& & \require{HTML} \style{display: inline-block; opacity:0.5;}{\color{red}{\vdots}} & \require{HTML} \style{display: inline-block; transform: rotate(45deg); opacity:0.5;}{\color{red}{\vdots}} &\require{HTML} \style{display: inline-block; opacity:0.5;}{\color{red}{\vdots}} & | &  & \require{HTML} \style{display: inline-block; opacity:0.5;}{\color{red}{\vdots}}  &\require{HTML} \style{display: inline-block; transform: rotate(45deg); opacity:0.5;}{\color{red}{\vdots}} &\require{HTML} \style{display: inline-block; opacity:0.5;}{\color{red}{\vdots}} &| & & |&\require{HTML} \style{display: inline-block; transform: rotate(45deg)}{|} &|\\
|& & \color{red}{8} & \require{HTML} \style{display: inline-block; opacity:0.5;}{\color{red}{\cdots}} & \require{HTML} \style{display: inline-block; opacity:0.5;}{\color{red}{\cdots}}& | &\require{HTML} \style{display: inline-block; opacity:0.5;}{\color{red}{\cdots}} & \color{red}{12} & \require{HTML} \style{display: inline-block; opacity:0.5;}{\color{red}{\cdots}} &\require{HTML} \style{display: inline-block; opacity:0.5;}{\color{red}{\cdots}}& | &\require{HTML} \style{display: inline-block; opacity:0.5;}{\color{red}{\cdots}}&22&&|\\
|&\require{HTML} \style{display: inline-block; transform: rotate(45deg); opacity:0.5;}{\color{red}{\vdots}} & \require{HTML} \style{display: inline-block; opacity:0.5;}{\color{red}{\vdots}} & & \require{HTML} \style{display: inline-block; opacity:0.5;}{\color{red}{\vdots}} & | &\require{HTML} \style{display: inline-block; transform: rotate(45deg); opacity:0.5;}{\color{red}{\vdots}} &\require{HTML} \style{display: inline-block; opacity:0.5;}{\color{red}{\vdots}} & & \require{HTML} \style{display: inline-block; opacity:0.5;}{\color{red}{\vdots}}& | &\require{HTML} \style{display: inline-block; transform: rotate(45deg)}{|}  & | &&|\\
15  & — & —& —& — & 3 & — & — & —& —& 21 &  & | & &|\\
|& & \require{HTML} \style{display: inline-block; opacity:0.5;}{\color{red}{\vdots}} &  & \color{red}{9}  &| &\require{HTML} \style{display: inline-block; opacity:0.5;}{\color{red}{\cdots}} &  \require{HTML} \style{display: inline-block; opacity:0.5;}{\color{red}{\vdots}} & \require{HTML} \style{display: inline-block; opacity:0.5;}{\color{red}{\cdots}} & \color{red}{26} &|&\require{HTML} \style{display: inline-block; opacity:0.5;}{\color{red}{\cdots}}&|&\require{HTML} \style{display: inline-block; opacity:0.5;}{\color{red}{\cdots}}&6\\
|& & \require{HTML} \style{display: inline-block; opacity:0.5;}{\color{red}{\vdots}}&\require{HTML} \style{display: inline-block; transform: rotate(45deg); opacity:0.5;}{\color{red}{\vdots}}  &  &|  &  &\require{HTML} \style{display: inline-block; opacity:0.5;}{\color{red}{\vdots}} &\require{HTML} \style{display: inline-block; transform: rotate(45deg); opacity:0.5;}{\color{red}{\vdots}}  &&|&&|&\style{display: inline-block; transform: rotate(45deg)}{|}\\
|& &\color{red}{16} & \require{HTML} \style{display: inline-block; opacity:0.5;}{\color{red}{\cdots}}  & \require{HTML} \style{display: inline-block; opacity:0.5;}{\color{red}{\cdots}} &|&\require{HTML} \style{display: inline-block; opacity:0.5;}{\color{red}{\cdots}}& \color{red}{8} &\require{HTML} \style{display: inline-block; opacity:0.5;}{\color{red}{\cdots}}&\require{HTML} \style{display: inline-block; opacity:0.5;}{\color{red}{\cdots}}& | &  \require{HTML} \style{display: inline-block; opacity:0.5;}{\color{red}{\cdots}}&17\\
|& \require{HTML} \style{display: inline-block; transform: rotate(45deg); opacity:0.5;}{\color{red}{\vdots}}& & &  &|&  \require{HTML} \style{display: inline-block; transform: rotate(45deg); opacity:0.5;}{\color{red}{\vdots}} &&&& | & \require{HTML} \style{display: inline-block; transform: rotate(45deg)}{|}\\
23 & — & — & — & — & 2  & — & — & — & — & 19\\
\end{array}$$

事实上代码里边还内嵌了一些HTML代码，所以不算是严格的纯LaTeX代码，应该说是LaTeX+MathJax的结合。
