---
title: "让 Claude 在你的电脑上工作"
title_en: "Put Claude to work on your computer"
source: https://claude.com/blog/dispatch-and-computer-use/
crawled: 2026-09-14
translated: 2026-09-14
---

# 让 Claude 在你的电脑上工作

> 原文：[Put Claude to work on your computer](https://claude.com/blog/dispatch-and-computer-use/) · Claude 博客

在 Claude Cowork 与 Claude Code 中，你现在可以让 Claude 使用你的电脑来完成任务。当 Claude 无法访问所需的工具时，它会指向、点击并导航你屏幕上的内容，亲自把任务完成。它可以打开文件、使用浏览器、自动运行开发工具——无需任何设置。

这项功能现已面向 Claude Pro 与 Max 订阅者开放研究预览（research preview）。它与 [Dispatch](https://support.claude.com/en/articles/13947068-assign-tasks-to-claude-from-anywhere-in-cowork) 配合尤其出色——后者让你可以从手机上向 Claude 指派任务。

## Claude 如何使用你的电脑

Claude 会优先选用最精确的工具，从 Slack、Google Calendar 等服务的连接器（connector）开始。当没有可用的连接器时，Claude 可以直接控制你的浏览器、鼠标、键盘和屏幕来完成任务。它会按需滚动、点击打开、逐步探索，且始终会先征求你的明确许可。

我们在构建这项能力时加入了将风险降到最低的安全防护，包括针对提示注入（prompt injection）的防护。当 Claude 使用你的电脑时，我们的系统会自动扫描模型内部的激活值（activations），以检测此类活动。你也可以随时叫停 Claude，而且 Claude 在访问新应用之前总会先请求许可。

与 Claude 的编码或文本交互能力相比，计算机使用仍处于早期阶段。Claude 可能会出错，而且在我们持续改进安全防护的同时，威胁也在不断演变。我们建议从你信任的应用开始，不要处理敏感数据。正因如此，某些应用默认是禁用的。你可以[在这里](https://support.claude.com/en/articles/14128542)了解更多安全最佳实践。

## 从任何地方给 Claude 发消息

上周，我们发布了 [Dispatch](https://support.claude.com/en/articles/13947068-assign-tasks-to-claude-from-anywhere-in-cowork)：这是 Claude Cowork 中的一项新功能（现已登陆 Claude Code），让你可以在手机或桌面上与 Claude 保持一段连续不断的对话。你可以在手机上给 Claude 指派一个任务，把注意力转向别处，然后在电脑上打开已完成的工作。

有了 Dispatch，你可以让 Claude 每天早上自动查看你的邮件，或每周提取一些指标，也可以为一份报告或一个 pull request 拉起一个 Claude Cowork 或 Claude Code 会话。

Claude 全新的计算机使用能力让 Dispatch 更有帮助。现在，你不在时，Claude 可以代你使用你的电脑。例如，在你坐火车时创建一份晨间简报；在你的 IDE 里做修改、运行测试并提交 PR；或者让你的 3D 打印项目按最初的计划继续推进。

## 开始使用

Claude 在 Claude Cowork 与 Claude Code 中的计算机使用能力处于研究预览阶段。它不会总是完美运行：复杂任务有时需要再试一次，而且通过你的屏幕操作比使用直接集成更慢。我们选择早早分享它，是因为想了解它在哪里行得通、在哪里仍有不足——正如我们当初对待 Claude Cowork 一样。

它现已面向 Claude Pro 与 Claude Max 订阅者开放。计算机使用支持 macOS 与 Windows，你需要在桌面应用的设置中启用它。你还需要确保桌面应用处于唤醒且运行的状态。之后，你可以将其与移动应用配对，尝试从手机上交接一个任务。

FAQ（常见问题）
