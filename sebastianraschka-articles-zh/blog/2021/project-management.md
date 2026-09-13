---
title: "我如何保持项目井井有条"
title_en: "How I Keep My Projects Organized"
source: https://sebastianraschka.com/blog/2021/project-management.html
crawled: 2026-09-06
translated: 2026-09-06
---

# 我如何保持项目井井有条

> 原文：[How I Keep My Projects Organized](https://sebastianraschka.com/blog/2021/project-management.html)

---

## 动机

自从 2008 年开始本科学习以来，我就一直痴迷于效率技巧、笔记方案和待办清单管理。这些年里，我尝试过许许多多的工作流和数百种（大多为数字化的）工具，来让我的生活、项目和笔记保持有序。

我偶尔会和朋友、同事交流想法，也应要求在 Twitter 上谈过几次我的工作流。在今天这场 2021 年版的讨论之后，我觉得写一篇快速、非正式的博客文章是合理的——这样更好读，下次再有人问起时也有个可以快速查阅的参考 :)。

[![示意图](https://sebastianraschka.com/images/blog/2021/project-management/twitter.webp)](https://twitter.com/rasbt/status/1345874138754375680)

总体而言，我的方法灵感来自 David Allen 的 [Getting Things Done](https://gettingthingsdone.com)。它也基本上是一套数字化的工作流，辅以一些纸笔元素。在用专门工具和其他工作流做了多年实验之后，我已经在几乎未做改动的情况下使用这套方法约四年了，它对我很有效。

就个人而言，我的理念是避免订阅制，避免把你锁死在特定服务或生态系统中（这些服务几年后可能就不复存在）的专门工具。另外，由于我使用两台电脑，我的数据需要跨设备同步。还有一个要求是一切都应当便于备份。

请注意，这篇非正式的文章主要是为"问过我的人"提供一个更详细的版本。如果你已经有一套好用的系统，我建议你坚持用下去。坚持一套系统可能是最重要的效率建议，因为寻找那个（并不存在的）完美工具或完美工作流会浪费大量时间。

## 项目文件夹

本质上，我的项目管理围绕一个所谓的"`project-data`"文件夹展开，里面存放我所有正在进行的项目，也就是我当前正在做的项目。每个项目在 `project-data` 文件夹里有一个独立的文件夹，并带有类别前缀，例如：

- `admin__`：各种行政事务（比如我的网站，还有推荐信等）；
- `paper__`：我正在写的论文；
- `grant__`：我正在准备的基金申请；
- `learn__`：我目前正在学习的内容（书籍或在线课程）；
- `maybe__`：那些可能有趣但当前属于干扰的项目，或者我想先记在脑子里、以后再回头处理的事情；
- …
- `talk__`：我即将做的报告；
- `trips__`：即将出行的旅行相关资料；
- `write__`：非研究论文的写作项目（书籍、书籍章节或博客文章）。

![示意图](https://sebastianraschka.com/images/blog/2021/project-management/project-data-1.webp)

每个文件夹里放着与项目相关的文件，因项目而异。比如要读的论文、会议笔记、收据、图片和网页链接。例如，如果某个项目需要用 Overleaf 协作写作，我会在主文件夹里放一个指向 Overleaf 项目的链接。此外，每个这样的文件夹都有一份项目待办清单，用来管理该项目的待办事项。我在这些文件里写上截止日期，并把它们加进日历（包括提醒）。

![示意图](https://sebastianraschka.com/images/blog/2021/project-management/project-contents.webp)

有时我用纯文本文件做待办清单；有时用 Markdown 文件或 Pages 文档——如果其中要放 LaTeX 公式，或者想拖放图片和截图。现在我也常用 OneNote 页面，因为它有很方便的复选框，可以轻松重新排序，然后我会在文件夹里放一个指向该 OneNote 页面的链接（一个缺点是备份可能成问题——备份的事后面再谈）。总的来说，我用最适合做该项目待办清单的工具。

![示意图](https://sebastianraschka.com/images/blog/2021/project-management/one-note.webp)

关于我如何使用这些待办清单，稍后会在"每周回顾"和"每日待办清单与时间块"两节中详细说明。

## 项目归档

除了前面提到的 `project-data` 文件夹，我还保留一个 `project-archive` 文件夹（最早可以追溯到 2011 年我的本科毕业论文），存放已完成的项目。

![示意图](https://sebastianraschka.com/images/blog/2021/project-management/project-archive-old.webp)

项目完成后，我会检查 `project-data` 里对应的项目文件夹，确保所有相关文件都在我的电脑上。例如，如果项目待办清单在 OneNote 上，我会把它导出为 PDF；如果我用 Overleaf 做协作写作项目，我会下载 LaTeX 源文件。然后，我给项目文件夹加上完成的年份和月份前缀，并移动到我的 `project-archive` 文件夹。

![示意图](https://sebastianraschka.com/images/blog/2021/project-management/project-archive.webp)

## 每周回顾

每周我都会回顾我的活跃项目。通常我会在周日晚花大约 30-60 分钟做这件事；有时会推到周一早上第一件事来做。回顾时，我会过一遍 `project-data` 里的项目文件夹，重点关注各项目的待办清单。我勾掉上一周完成的事项，偶尔也会重新整理项目。基于这些待办清单，我会汇总出一份本周待办清单，列出我想要/需要完成的事项。

![示意图](https://sebastianraschka.com/images/blog/2021/project-management/weekly-todo.webp)

虽然一周之内我也会查阅各项目的待办文件，但这份每周待办清单才是我当周的主清单。我通常用它来制定每日待办清单，并配合时间块（time blocking）方法，下一节会解释。

通常我会把每周待办清单打印出来，方便随手涂写（用笔划掉事项有种说不出的满足感），也方便在清单底部追加新的待办事项。除非是紧急事项，我尽量把这些新加的待办放到最后处理。

## 每日待办清单与时间块

每天晚上，我会看着日历和每周待办清单来规划第二天的工作。如果我没记错的话，我的时间块方法灵感来自 Cal Newport 的 [Deep Habits: The Importance of Planning Every Minute of Your Work Day](https://www.calnewport.com/blog/2013/12/21/deep-habits-the-importance-of-planning-every-minute-of-your-work-day/)。

我会用一张散页纸（之后会收集起来扫描存档），画出当天的会议和我想做的事情。很多时候我并不会严格照着执行，有时甚至会取消某些条目，因为其他事情耗时更久，或者冒出了急事。不过，有个计划的好处在于，它让我大致知道一天能做多少事，也帮助我把预期控制在合理范围内。

![示意图](https://sebastianraschka.com/images/blog/2021/project-management/daily.webp)

## 跨设备同步项目数据

我希望所有项目在我的（两台）电脑上都能访问。（在疫情前这更重要——那时我经常在校内办公室和家里之间切换，还经常出差。）为此我使用 Microsoft OneDrive，不过其他云同步服务大概也同样好用。

![示意图](https://sebastianraschka.com/images/blog/2021/project-management/onedrive.webp)

我的主力电脑上有全部项目数据的离线副本。对于存储较小的笔记本，我可以通过"Files On-Demand"选项按需下载数据。我不在 iPhone、iPad 这类移动设备上工作——前者我只用来导航、双重认证和基本的电话功能，后者只用来教学。不过我猜这种云同步方式同样支持在移动设备上工作（比如通过 OneDrive 应用）。

## 备份

我发现，把活跃和归档项目放在文件夹结构里，让定期备份的实施变得相对简单。我用了（可能过多的）多种备份方案来保证冗余。除了把项目数据放在云端，我在 macOS 上用 Time Machine 把电脑备份到物理硬盘，并用 [Arq](https://www.arqbackup.com) 通过另一家云服务商创建带时间戳的额外备份。另外，从去年开始，我会把活跃和归档项目复制到一张 SD 卡上，存放在安全的地方。

![示意图](https://sebastianraschka.com/images/blog/2021/project-management/sd-card.webp)

关于做好备份，我的建议是把假想情景过一遍：

- 我的公寓/房子被水淹或烧毁；
- 我的电脑被偷或损毁；
- 我的办公室被水淹或烧毁。
- 如果云服务商 X 不可靠、擅自使用我的数据会怎样。

如果上面列出的每一种情景你都有恢复数据的方案，那大概就没什么问题了。

## 长期笔记

至于长期保存笔记（比如论文里一些普遍有趣的小知识），我用基于 [DokuWiki](https://www.dokuwiki.org/dokuwiki) 的个人 wiki。如果你的个人网站已经有 web 服务器，这种方式免费且经过验证——我认为 DokuWiki 短期内不会过时。

![示意图](https://sebastianraschka.com/images/blog/2021/project-management/wiki.webp)

## 结语

请注意，上面概述的工作流是对我特别有效的一套，但你的体验可能不同。我特别喜欢的一点是，它允许并支持：

- 离线工作（有时我喜欢关掉网络来提升专注力）；
- 跨设备轻松且可选的同步（因为我有多台电脑）；
- 轻松备份（图个安心）。

此外：

- 没有强生态系统锁定（未来切换工具甚至操作系统都不是问题）；
- 基本免费 :)；
- 而且我仍然可以为每个项目使用特定的工具，同时保持组织与归档的简单直接。

总的来说，我认为高效的关键之一在于找到一套对你来说相对有效的方法并坚持下去，避免因不断更换工具、寻找"更好的方案"而焦虑。当然，每 5-10 年左右重新审视一次自己的方法也不算坏事 :)。
