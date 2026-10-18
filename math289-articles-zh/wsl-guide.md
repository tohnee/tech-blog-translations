---
title: "Windows 用户 WSL 指南"
title_en: "WSL Guide for Windows Users"
source: https://web.stanford.edu/class/math289/wsl_guide.pdf
crawled: 2026-10-19
translated: 2026-10-19
---

> 原文：[WSL Guide for Windows Users](https://web.stanford.edu/class/math289/wsl_guide.pdf) · Stanford MATH 289

# 在 Windows 10 和 11 上安装 WSL

作者：Travor Liu（tzliu@stanford.edu） · 2026 年 9 月 23 日

在斯坦福 MATH 289 课程中，我们将使用编码智能体（coding agents）：帮助我们编写并执行代码的 AI 工具。这些智能体在类 Unix 环境（如 Linux 和 macOS）中通常比在 Windows 中工作得更好。因此，本课程倾向于使用类 Unix 环境。对于 Windows 用户来说，仍然可以在照常使用 Windows 的同时拥有一个 Linux 环境。在本指南中，我们将帮助你安装 Ubuntu——一个使用广泛、自带一系列实用程序的 Linux 版本。我们将通过适用于 Linux 的 Windows 子系统（Windows Subsystem for Linux，WSL）来运行 Ubuntu；WSL 是 Windows 的一项功能，让你无需替换 Windows 即可使用 Linux。

本指南适用于 Windows 10 和 Windows 11。大多数截图展示的是 Windows 10；Windows 11 的界面可能有所不同，相关的菜单差异在下文中有注明。

在本指南中，Windows+R 表示按住带有 Windows 徽标的键，按下 R，然后同时松开两个键。这会打开"运行"（Run）对话框，这是一种通过输入程序名称并按 Enter 来快速启动应用程序的方式。例如，在运行对话框中输入 `winver`（图 1）会打开一个显示你的 Windows 版本的窗口。

稍后，你将输入命令（command）：在 PowerShell 或 Ubuntu 终端中执行的指令。每一步都会指明应使用哪个应用程序。在该应用程序中键入或粘贴命令并按 Enter，然后等它执行完毕，再输入下一条。

> 图 1：已输入 `winver` 的"运行"对话框。来源：Southern Oregon University，https://support.sou.edu/kb/articles/how-to-check-your-version-of-windows-10

请按第 1 节到第 6 节的顺序操作：先检查你的电脑并启用 Windows 功能，然后学习如何使用 PowerShell、安装 Ubuntu、创建你的 Linux 账户，并验证安装。第 7 节介绍日常使用与维护。如果遇到问题，请查阅第 8 节；如有需要，第 9 节提供了另一种安装方法。咨询 AI 模型也能帮助你排查问题。

## 1 检查你的电脑

开始之前请先保存你的工作：你需要重启 Windows。你还需要互联网连接，以及一个拥有管理员权限（可安装软件）的 Windows 账户。

1. 检查 Windows 版本。按 Windows+R，输入 `winver`，然后按 Enter。在打开的窗口中，查看 Version 和 OS Build（图 2）。主要安装方法适用于 Windows 11，或版本号为 2004 及以上、内部版本号（build）为 19041 及以上的 Windows 10（https://learn.microsoft.com/en-us/windows/wsl/install）。检查完毕后关闭该窗口。如果你的 Windows 10 版本较旧，请在"设置">"更新和安全">"Windows 更新"下检查更新，或使用第 9 节中的可选手动安装说明。

   > 图 2：`winver` 中显示的 Windows 10 Home 22H2。来源：Sun City Texas Computer Club，第 9 页，https://www.sctexas.org/Files/Library/27409/SUNCITYCOMPUTERWINDOWSSIG11082022.PDF

2. 检查系统类型。打开开始菜单，然后进入"设置">"系统">"关于"。在"系统类型"（System type）下，确认是配有基于 x64 或基于 ARM 的处理器的 64 位操作系统（图 3）。

   > 图 3：设置中的"系统类型"。来源：Into Windows，https://www.intowindows.com/how-to-check-if-your-pc-is-running-32-bit-or-64-bit-windows-10/

3. 检查虚拟化（virtualization）。这是 WSL 2 需要的一项计算机功能。按 Ctrl+Shift+Esc 打开任务管理器。如有必要，先选择"更多详细信息"，然后进入"性能">"CPU"。查看 Virtualization（虚拟化）是否显示为"已启用"（图 4）。如果显示"已禁用"，请按照你的计算机制造商的说明，在 BIOS/UEFI 设置（计算机的启动设置）中启用虚拟化（https://learn.microsoft.com/en-us/windows/wsl/troubleshooting）。

   > 图 4：任务管理器中的虚拟化状态。来源：ASUS，https://www.asus.com/us/support/faq/1043181/

## 2 启用 Windows 功能

1. 按 Windows+R，输入 `optionalfeatures`，然后按 Enter。会打开一个名为"Windows 功能"的窗口。
2. 向下滚动，同时勾选"适用于 Linux 的 Windows 子系统"（Windows Subsystem for Linux）和"虚拟机平台"（Virtual Machine Platform）（图 5）。如果其中某一项已经被勾选，保持勾选即可。
3. 点击"确定"。如果 Windows 请求进行更改的权限，请予以批准。等待 Windows 完成。
4. 如果你在这一步勾选了任何一项，请在继续之前重启 Windows。先保存所有打开的文档。

   > 图 5：Windows 11 上的"Windows 功能"，两个必需项目已用框标出。来源：LogicMonitor，https://www.logicmonitor.com/blog/install-pietrasanta-traceroute-on-windows-11

## 3 使用 Windows PowerShell

Windows PowerShell 是一个你可以向 Windows 输入指令的应用程序。我们会确切地告诉你输入什么，以及是否需要管理员窗口——即有权更改计算机设置的窗口。图 6 显示了下文会用到的 Windows+X 菜单。

- 管理员窗口：按 Windows+X，在 Windows 10 上选择"Windows PowerShell (管理员)"（Windows PowerShell (Admin)），在 Windows 11 上选择"终端 (管理员)"（Terminal (Admin)），然后批准管理员提示。安装 WSL 时，或某个步骤要求管理员权限时，使用它。
- 普通窗口：按 Windows+X，在 Windows 10 上选择"Windows PowerShell"，在 Windows 11 上选择"终端"（Terminal）。检查安装或启动 Ubuntu 时，使用它。

  > 图 6：Windows+X 菜单。来源：WindowsLoop，https://windowsloop.com/how-to-run-powershell-as-administrator/

在 Windows 11 上，"终端"可能显示为"Windows 终端"（Windows Terminal）。它会打开一个带标签页的窗口；请使用 PowerShell 标签页。图 7 展示了经典窗口与 Windows 终端中的 PowerShell。如果 PowerShell 尚未打开，请从 + 按钮旁边的箭头菜单中选择"Windows PowerShell"。

> 图 7：经典窗口（左）与 Windows 终端（右）中的 PowerShell。来源：Packt，第 1 页，https://static.packt-cdn.com/downloads/9781800207561_ColorImages.pdf

如果找不到这些选项，请在开始菜单中搜索"Windows PowerShell"。单击该应用即为普通窗口；右键单击它并选择"以管理员身份运行"（Run as administrator）即为管理员窗口。

提示符（prompt）是计算机在准备好让你输入命令时显示的文本。PowerShell 提示符通常以 PS 开头，后面跟着当前的 Windows 文件夹。例如：

```
PS C:\Users\alice>
```

请在提示符之后输入命令；不要把提示符本身一起复制进去。在管理员窗口中，窗口标题通常包含"管理员"（Administrator）字样。

## 4 安装 WSL 和 Ubuntu

按照第 3 节的说明，使用管理员 PowerShell 窗口。逐字键入下面这一行，包括空格和连字符，然后按 Enter：

```
wsl --install -d Ubuntu
```

Windows 将下载并安装必要的软件。等待完成后重启 Windows。重新登录后，点击开始菜单，输入 Ubuntu，如果 Ubuntu 应用尚未自动打开，就点击它。首次启动可能需要几分钟。这种方法安装的是 WSL 2，即本指南所使用的版本（https://learn.microsoft.com/en-us/windows/wsl/install）。

如果想要另一个带图解的完整流程，请参阅 Microsoft 的 WSL 教程（https://code.visualstudio.com/docs/remote/wsl-tutorial）。该教程还涵盖了可选的 Visual Studio Code 设置；完整的 WSL 2 手动安装步骤请使用本指南的第 9 节。

## 5 Ubuntu 入门

本节请使用 Ubuntu 窗口。这个窗口被称为 Ubuntu 终端：它让你输入面向 Linux 的命令。你可以通过在开始菜单中选择 Ubuntu 来打开它（Windows 10 见图 8，Windows 11 见图 9）。

> 图 8：Windows 10 开始菜单中的 Ubuntu。来源：Config Server Firewall，https://www.configserverfirewall.com/ubuntu-linux/install-ubuntu-on-windows-10/

> 图 9：Windows 11 开始菜单搜索中的 Ubuntu。来源：It's FOSS，https://itsfoss.com/run-linux-apps-windows-wsl/

首次启动时，Ubuntu 会要求你选择用户名和密码。请使用简单的小写字母、不含空格的用户名，例如 `alice`。这个账户与你的 Windows 账户相互独立。请记住密码：安装或更新 Linux 软件时会用到它。

注 1. 输入密码时屏幕上不会显示任何内容，连圆点或星号都没有。这是正常现象。你可以用 Backspace 删除刚输入的最后一个字符。输入密码并按 Enter，然后在要求确认时再输入一遍。

例如，账户设置可能会显示如下提示。请选择你自己的用户名来代替 `alice`；密码输入始终保持不可见。

```
Enter new UNIX username: alice
New password:
Retype new password:
```

账户设置完成后，当 Ubuntu 准备好接收命令时，终端会显示一个提示符（图 10）。例如：

```
alice@DESKTOP:~$
```

这里，`alice` 是你的 Linux 用户名，`DESKTOP` 是你的计算机名称，`~` 表示你的主文件夹。你的名称可能与此不同。请在 `$` 之后输入命令；不要把提示符本身复制进去。命令执行完毕后，提示符会重新出现，你便可以输入下一条命令。

> 图 10：账户设置完成后的 Ubuntu 终端。来源：Microsoft，https://code.visualstudio.com/docs/remote/wsl-tutorial

下面三条命令分别显示你的用户名、你的 Ubuntu 发行版本，以及 Linux 内核版本（Linux 核心部分的版本）。下面的示例会话使用名为 `DESKTOP` 的计算机上的 `alice`。只需在 `$` 提示符之后输入命令；其余各行都是示例输出。你的用户名、计算机名、Ubuntu 版本和内核版本可能与此不同。`/etc/os-release` 的输出有所省略。

```
alice@DESKTOP:~$ whoami
alice
alice@DESKTOP:~$ cat /etc/os-release
PRETTY_NAME="Ubuntu 24.04.1 LTS"
NAME="Ubuntu"
VERSION_ID="24.04"
VERSION="24.04.1 LTS (Noble Numbat)"
ID=ubuntu
...
alice@DESKTOP:~$ uname -r
5.15.167.4-microsoft-standard-WSL2
```

逐条输入以下命令来更新 Ubuntu 的软件。等第一条执行完毕后，再输入第二条：

```
sudo apt update
sudo apt upgrade
```

单词 `sudo` 用于向 Ubuntu 请求更改已安装软件的权限。如果被询问，请输入你刚创建的 Linux 密码。第一条命令检查可用的更新；第二条安装它们。如果被问到 Do you want to continue? [Y/n]，请输入 `y` 并按 Enter。然后等待提示符重新出现。

注 2. Windows Update 不会更新 Ubuntu 内部的软件。

Microsoft 的图解设置指南涵盖了账户、更新和 Linux 文件（https://learn.microsoft.com/en-us/windows/wsl/setup/environment）。

## 6 验证你的安装

按照第 3 节的说明，打开一个普通 PowerShell 窗口。运行：

```
wsl --list --verbose
```

查看 NAME 为 Ubuntu 且 VERSION 列显示 2 的条目。例如：

```
NAME STATE VERSION
* Ubuntu Running 2
```

注 3. 显示 Stopped 也是正常的：它表示 Ubuntu 当前没有打开。VERSION 列应显示 2；这是 WSL 的版本，而不是 Ubuntu 的发行版本号。星号可以忽略。如果该列显示 1，请参阅第 8 节（https://learn.microsoft.com/en-us/windows/wsl/basic-commands）。

当 `wsl --list --verbose` 列出了 WSL 版本为 2 的 Ubuntu，并且第 5 节中的示例命令能在 Ubuntu 中正常运行时，安装即告完成。现在你可以关闭 PowerShell 窗口了。以后使用时，只需从开始菜单打开 Ubuntu；无需重复安装过程。

## 7 日常使用与维护

在 PowerShell 窗口中，运行 `wsl -d Ubuntu` 即可进入 Linux。在 Ubuntu 内部，运行 `exit` 即可返回。你也可以直接从开始菜单启动 Ubuntu。

使用 Linux 软件进行工作时，请把文件放在你的 Linux 主文件夹（home folder）中，也就是属于你的 Ubuntu 账户的个人文件夹。符号 `~` 表示这个文件夹。在 Ubuntu 中，以下命令会创建一个名为 `projects` 的文件夹、切换到该文件夹，并在 Windows 文件资源管理器中打开它：

```
mkdir -p ~/projects
cd ~/projects
explorer.exe .
```

注 4. 请保留 `explorer.exe .` 末尾的那个点：它表示"当前文件夹"。Windows 的 C 盘可以从 Linux 通过 `/mnt/c` 访问。文件存储指南见（https://learn.microsoft.com/en-us/windows/wsl/setup/environment）。

### 例行维护

PowerShell：使用以下命令更新 WSL 本身：

```
wsl --update
```

对 Linux 软件包，请继续在 Ubuntu 内部运行 `sudo apt update` 和 `sudo apt upgrade`。要重启 WSL，请先保存你的工作，然后在 PowerShell 窗口中运行以下命令：

```
wsl --shutdown
wsl -d Ubuntu
```

关机（shutdown）会停止所有正在运行的 WSL 发行版。在较旧的 WSL 安装上，一些较新的选项可能不存在；`wsl --help` 会列出你的安装所支持的选项。维护命令参见（https://learn.microsoft.com/en-us/windows/wsl/basic-commands）。

## 8 故障排除

如果出了问题，请在关闭窗口之前复制完整的错误信息，或者给它拍张照片。以下建议涵盖常见问题。

**Ubuntu 被列出但 VERSION 为 1。**
在普通 PowerShell 窗口中运行以下命令。如果这个 Ubuntu 安装中已包含你的工作成果，请先保存一份备份。如果 NAME 列显示的是其他名称，请把 Ubuntu 替换为该名称。

```
wsl --set-version Ubuntu 2
```

等待其完成后，再次运行 `wsl --list --verbose`。

**安装程序只打印帮助信息，或 Ubuntu 不在列表中。**
在 PowerShell 窗口中，先运行 `wsl --list --online`，再运行 `wsl --install -d Ubuntu`。启动一次 Ubuntu 以完成初始化。请使用你安装它时所用的同一个 Windows 账户。

**下载进度停留在 0.0%。**
在管理员 PowerShell 窗口中尝试 `wsl --install --web-download -d Ubuntu`。如果该选项不可用，请查阅 `wsl --help` 并使用手动备用方法。安装程序故障排除见（https://learn.microsoft.com/en-us/windows/wsl/install）。

**错误 0x80370102：虚拟机无法启动。**
重复第 1 节中的虚拟化检查和第 2 节中的复选框检查，然后重启 Windows。如果错误仍然存在，请在 Microsoft 的故障排除指南中查找该确切错误（https://learn.microsoft.com/en-us/windows/wsl/troubleshooting）。

**错误 0x8007019e：WSL 组件被禁用。**
回到第 2 节中的 Windows 功能检查，启用"适用于 Linux 的 Windows 子系统"，然后重启 Windows。

**WSL 2 报告内核缺失或过期。**
在 PowerShell 窗口中尝试 `wsl --update`。对于旧版手动安装，请安装第 9 节中对应的内核更新包。

更多帮助请参阅 Microsoft 的故障排除指南（https://learn.microsoft.com/en-us/windows/wsl/troubleshooting）。

## 9 替代安装方法（可选）

如果 Ubuntu 已经可以正常使用，请跳过本节。当第 4 节中的命令不可用时，这些较旧的安装步骤可能会有用。Microsoft 的手动指南列出了此方法支持的 Windows 版本，并提供相应的下载（https://learn.microsoft.com/en-us/windows/wsl/install-manual）。

在继续之前，请完成第 2 节中的 Windows 功能检查以及任何所需的重启。

1. 下载并运行 Microsoft 手动指南第 4 步中链接的 x64 或 ARM64 WSL 2 Linux 内核更新包。基于 x64 的处理器选择 x64，基于 ARM 的处理器选择 ARM64——依据是你在第 1 节中检查的"系统类型"。下载文件后，双击运行安装程序。
2. PowerShell：运行 `wsl --set-default-version 2`。
3. 从 Microsoft Store 安装 Ubuntu（图 11）并启动它。如果 Store 不可用，请使用手动指南中的发行版直接下载与软件包安装说明。

   > 图 11：Microsoft Store 中的 Ubuntu（外观可能有所不同）。来源：手动安装指南（https://learn.microsoft.com/en-us/windows/wsl/install-manual）

4. 完成第 5 节和第 6 节中的账户设置与安装验证。
