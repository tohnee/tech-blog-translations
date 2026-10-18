---
title: "面向数学家的终端基础与智能体工作流指南"
title_en: "A Guide to Basic Terminal Use and Agentic Workflows for Mathematicians"
source: https://srliu.com/blog/terminal-guide/
crawled: 2026-10-19
translated: 2026-10-19
---

> 原文：[A Guide to Basic Terminal Use and Agentic Workflows for Mathematicians](https://srliu.com/blog/terminal-guide/) · Stanford MATH 289

这篇简短的说明介绍基本的终端命令和简单的智能体工作流。这些技能是更高级、亲自动手使用 Rethlas 的基础。上一篇指南把几乎所有事情都外包给了 AI。这种方式虽然方便，却可能让你看不清正在发生什么，浪费 token，并且当你运行大量实验、或当 Codex 或 Claude Code 压缩（compact）其上下文时变得不可靠。它还可能让 Rethlas 更难按照你自己的工作流进行定制。

## 基本终端命令

我是终端的爱好者，所以我会克制住滔滔不绝的冲动。你可以轻松地从 ChatGPT 或其他在线资源学到更多终端知识，所以我只介绍本指南后面会用到的命令。

1. `ls`：列出当前目录下可见的文件和文件夹。有些文件可能是隐藏的；`ls -alh` 会把它们也列出来，并显示大小、所有者等详细信息。
2. `cd`：更改你的当前目录。这个命令本质上就是终端里的"打开一个文件夹"。用 `cd <subfolder>` 进入当前目录中的某个文件夹，用 `cd ..` 返回其上级目录。
3. 在 macOS 上，`open -e <filename.md>` 会在"文本编辑"（TextEdit）中打开该文件。在 macOS 或 Linux 上，如果安装了 Visual Studio Code，你可以用 `code <filename.md>` 在 VS Code 中打开文件。我个人最喜欢的编辑器是 Neovim——Vim 的一个现代分支，它是终端原生的。但那是另一个无底洞，所以我在这里就不再多说了。如果你好奇，可以看看 [kickstart.nvim](https://github.com/nvim-lua/kickstart.nvim)。
4. `touch <filename.md>`：创建一个名为 `filename.md` 的空 Markdown 文件（如果它尚不存在）。

### tmux

tmux 是一个实用的终端复用器（terminal multiplexer），让你在单个窗口内管理多个终端会话。它还有另一大好处：如果你不小心关闭了终端窗口，你的 tmux 会话会在后台继续运行。

在 macOS 上，运行 `brew install tmux` 安装 tmux。然后运行 `tmux` 创建并进入一个新会话。

下面是几个实用的 tmux 快捷键。默认情况下，每个快捷键都以前缀 `ctrl+b` 开头。

1. 创建新窗口：按 `ctrl+b`，松开两个键，然后按 `c`。
2. 切换窗口：按 `ctrl+b`，松开两个键，然后按 `n` 进入下一个窗口，或按 `p` 回到上一个窗口。
3. 重命名当前窗口：按 `ctrl+b`，松开两个键，按 `,`，输入新名称，然后按 `enter`。
4. 脱离（detach）当前会话：按 `ctrl+b`，松开两个键，然后按 `d`。
5. 重新接入（reattach）某个会话：在脱离会话或不小心关闭终端窗口之后，运行 `tmux attach`。

稍后当我们手动运行 Rethlas 时，你就会明白 tmux 为什么有用了。

### Git

另一个实用的工具是 Git，一个版本控制系统。Git 通过称为提交（commit）的快照来维护你的编辑历史，让你能够恢复较早的版本。这类似于 Overleaf 的历史记录功能。

1. `git clone <repository-url> <folder-name>` 把一个远程 Git 仓库复制到当前目录下一个名为 `<folder-name>` 的新文件夹中。前面你已经用过 `git clone https://github.com/frenzymath/Rethlas rethlas`。
2. `git add .` 暂存当前目录及其子目录中的所有更改，为下一次提交做准备。`git commit -m "a short message recording what changed"` 把这些已暂存的更改记录到仓库的历史中。
3. `git push` 把你的本地提交发送到对应的远程仓库。
4. `git pull` 从远程分支取回更改，并将其整合进你当前的本地分支。

为什么我要和你分享这些 Git 基础？因为它们让你可以在本地使用 Overleaf，并搭建一个简单的智能体工作流。

有些人只在 Overleaf 里写 LaTeX，但当网络连接中断时，访问可能受阻。而且与本地相比，你对语法高亮、快捷键绑定以及其他编辑器定制的掌控也更少。然而，纯本地的 LaTeX 工作流要求你自己维护备份，以防文件丢失或损坏；与他人协作或从多台设备访问项目也可能更困难。

Git 为这些取舍提供了一个优雅的解决方案。在 AI 智能体的时代，这种方法甚至更加有用。

### 通过 Git 使用 Overleaf

一句话概括：你可以把一个 Overleaf 项目当作一个远程 Git 仓库。在提交（commit）你的本地更改之后，运行 `git push` 把它们发送到 Overleaf。这些更改随后会在 Overleaf 上得到备份，并对你的协作者和其他设备可用。当 Overleaf 上有更改时，运行 `git pull` 来更新你的本地副本。你可以在本地用自己喜欢的编辑器（VS Code、Neovim 等）编译并查看 PDF。

登录你的 Overleaf 账户，打开 **Account Settings**（账户设置）。

![Overleaf 账户设置](https://srliu.com/upload/terminal-guide-settings.png)

找到 **Git Integration**（Git 集成）部分，生成一个新令牌（token），并妥善保存。请把这个令牌当作密码来对待：它可以对你的账户可用的每一个 Overleaf 项目进行 Git 访问身份验证。Overleaf 只显示一次完整令牌。如果你弄丢了，就删除它并重新生成一个。

![Overleaf Git Integration 令牌设置](https://srliu.com/upload/terminal-guide-token.jpg)

打开你的 Overleaf 项目，选择 **Integrations**（集成）。

![Overleaf Integrations 菜单](https://srliu.com/upload/terminal-guide-integrations.jpg)

选择 **Git**，然后复制显示出来的 `git clone` 命令和 URL。

![Overleaf git clone 命令](https://srliu.com/upload/terminal-guide-clone.jpg)

现在回到终端，用 `cd` 进入你想存放项目的目录，然后运行：

```
git clone <url> <paper-folder-name>
```

出现提示时，输入 `git` 作为用户名，并使用你的 Overleaf 身份验证令牌作为密码。

现在你可以在本地编辑论文了。要把你的更改发送到 Overleaf，运行：

```
git add .
git commit -m "Describe your changes"
git push
```

要用 Overleaf 上所做的更改更新你的本地文件夹，运行 `git pull`。

在 macOS 上，你可以使用 MacTeX 在本地编译 LaTeX。运行 `brew install --cask mactex` 来安装它。

安装完成后，重启终端，让 MacTeX 的命令行工具生效。

### 用 AI 编辑你的 LaTeX 文件

现在你可以在本地编辑你的 Overleaf 项目，并把更新推送回 Overleaf。在 2026 年之前，这个工作流已经提供了两大好处：

1. 你可以使用本地编译器和你自己偏好的编辑器定制，同时在 Overleaf 上保留一份便捷的备份并与他人协作。这对 Neovim 和 VS Code 用户尤其有用。
2. 在 Overleaf 维护期间或断网时，你仍然可以在本地继续工作。

现在又多了一个重大好处：你可以使用 Claude Code、Codex 和其他 AI 智能体来帮你编辑论文！

用 `cd` 进入你的 Overleaf 项目的本地克隆。

运行 `codex`。如果出现提示，请确认你信任当前文件夹。

然后你可以让 Codex：

1. 修复格式。例如："修复这篇 LaTeX 文档中所有超出页边距的文字"、"添加另一位作者"、"让 `main.tex` 改用 `jams.tex` 中的模板"，或"调整格式，使论文控制在 10 页以内"。
2. 改进语法和表达的精确性。例如："标出这篇文档中所有英语语法错误或不精确的表达，并和我逐一过一遍。给我上下文，提出修改建议，并在应用每处修改之前让我确认。"

除了这些常规任务之外，一个自然的问题随之而来：你能用 AI 智能体来做数学吗——比如提问"帮我证明 `main.tex` 里的引理 3.14"？遗憾的是，Codex 和 Claude Code 开箱即用的数学推理能力并不总是足够强，尽管它们已经相当能干。请、请务必诚实：不要使用本指南中的技术在作业上作弊。

但你已经了解 Rethlas 了，你也许想用它来证明你论文中的引理！我们将在以后的博客文章中更详细地讨论这一点。

如果你经常重复某些工作流——比如排版 LaTeX、检查语法或批改作业——你可能会想用 `SKILL.md` 指令创建技能（skills），让智能体更可靠地遵循这些工作流。这体现了 Rethlas 背后的原则之一：把数学研究工作流的基本要素提炼成可复用的技能。

---

## 评论
