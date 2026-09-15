---
title: "Claude Code 代码审查（Code Review）"
title_en: "Code Review for Claude Code"
source: https://claude.com/blog/code-review/
crawled: 2026-09-14
translated: 2026-09-14
---

# Claude Code 代码审查（Code Review）

> 原文：[Code Review for Claude Code](https://claude.com/blog/code-review/) · Claude 博客

今天，我们推出 Code Review：它会在每个 PR 上派出一支智能体团队，捕捉粗略浏览会漏掉的 bug——为深度而生，而非为速度。这就是我们在 Anthropic 内部几乎每个 PR 上都在运行的系统。现面向 Team 与 Enterprise 套餐开放研究预览（research preview）。

## **管理审查瓶颈**

过去一年，Anthropic 每位工程师的代码产出增长了 200%。代码审查成为了瓶颈，我们每周都从客户那里听到同样的反馈。他们告诉我们，开发者的精力已被摊薄，许多 PR 得到的只是粗略扫视，而非深度阅读。

我们需要一位在每个 PR 上都值得信赖的审查者。Code Review 就是成果：深度、多智能体的审查，能捕捉人类审查者自己也常常漏掉的 bug。相比我们现有的 [Claude Code GitHub Action](https://code.claude.com/docs/en/github-actions)，它是一个更彻底（也更昂贵）的选项，后者仍保持开源并继续可用。

我们在 Anthropic 几乎每个 PR 上都运行 Code Review。此前，16% 的 PR 会收到有实质内容的审查意见；现在这一比例是 54%。它不会批准 PR——那仍然是人类的决定——但它弥合了缺口，让审查者能够真正覆盖所有要发布的内容。

## **工作原理**

当 PR 被打开时，Code Review 会派出一支智能体团队。这些智能体并行查找 bug、验证 bug 以过滤误报，并按严重程度排序。结果以一条高信息量的总览评论落在 PR 上，外加针对具体 bug 的行内评论。

审查规模随 PR 而定。大型或复杂的改动会得到更多智能体和更深入的阅读；琐碎的改动只做轻量检查。根据我们的测试，平均一次审查耗时约 20 分钟。

## **Code Review 实战**

我们已在内部运行 Code Review 数月：在大型 PR（改动超过 1,000 行）上，84% 会产生发现，平均 7.5 个问题。在改动少于 50 行的小型 PR 上，这一比例降至 31%，平均 0.5 个问题。工程师们大体认同它揭示的内容：不到 1% 的发现被标记为不正确。

有一个案例：对某个生产服务的一行修改看起来很常规，属于通常会被快速批准的那种 diff。但 Code Review 将其标记为严重级别。这个改动会破坏该服务的身份验证——这是一种在 diff 中很容易被一眼读过去、但一经指出就显而易见的故障模式。它在合并之前被修复了，那位工程师事后表示，靠他自己本来是抓不到的。

早期接入的客户也看到了类似的模式。在 [TrueNAS 开源中间件的一次 ZFS 加密重构](https://github.com/truenas/middleware/pull/18291)中，Code Review 发现了相邻代码中一个早已存在的 bug：一个类型不匹配会在每次同步时悄悄清空加密密钥缓存。这是 PR 恰好触碰到的代码中的潜在问题，正是人类审查者浏览变更集时不会主动去查的那类东西。

## **成本与控制**

Code Review 为深度而优化，比 [Claude Code GitHub Action](https://code.claude.com/docs/en/github-actions) 这类更轻量的方案更贵。审查按 token 用量计费，平均每次约 15–25 美元，并随 PR 规模与复杂度伸缩。

管理员有多种控制支出与用量的方式：

- **组织月度上限**：定义所有审查合计的月度支出总额
- **仓库级控制**：只在你选择的仓库上启用审查
- **分析仪表板**：追踪已审查的 PR、采纳率与审查总成本

## **开始使用**

Code Review 现已作为研究预览（beta）面向 Team 与 Enterprise 套餐开放。

- **管理员**：在你的 [Claude Code 设置](http://claude.ai/admin-settings/claude-code)中启用 Code Review，安装 GitHub App，并选择要运行审查的仓库。
- **开发者**：启用后，审查会在新 PR 上自动运行。无需任何配置。

更多信息请[查阅文档](http://code.claude.com/docs/en/code-review)。

FAQ（常见问题）
