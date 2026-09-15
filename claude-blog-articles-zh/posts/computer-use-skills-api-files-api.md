---
title: "用计算机使用、Skills API 与 Files API 构建生产级智能体"
title_en: "Build production agents with computer use, the Skills API, and the Files API"
source: https://claude.com/blog/computer-use-skills-api-files-api/
crawled: 2026-09-14
translated: 2026-09-14
---

# 用计算机使用、Skills API 与 Files API 构建生产级智能体

> 原文：[Build production agents with computer use, the Skills API, and the Files API](https://claude.com/blog/computer-use-skills-api-files-api/) · Claude 博客

今天，计算机使用（computer use）、Skills API 与 Files API 已在 Claude Platform 上正式发布。计算机使用还为在 Web 应用中工作的智能体新增了一个浏览器使用工具（browser use tool）。三者合力，让你能够构建这样的智能体：操作软件、运用你团队的专业知识，并返回完成的文件。

### **在 Claude Platform 上构建智能体**

**计算机使用**让你构建能操作自己看得见的软件的智能体。给它一张截图，智能体就会像坐在键盘前的人一样点击、输入、滚动。这让它可以在那些从未为自动化而设计的应用中工作。新的**浏览器使用工具（browser use tool）**把这一能力延伸到 Web。除了截图之外，智能体还能读取页面的结构，作用于某个具体的字段或按钮，而不是屏幕上的某个位置。

**Skills API** 与 **Files API** 让你把团队的专业知识与文档交给这位智能体。技能（skill）是一个由说明、脚本与模板组成的文件夹，Claude 只在任务需要时才加载它。通过 **Skills API**，你可以上传自己的技能并管理版本，然后把它们附加到任意请求上。它们运行在 Claude 的代码执行沙箱中，因此你无需托管任何东西。**Files API** 是智能体所读写文档的存储空间：把 PDF 或电子表格上传一次，在后续请求中按 ID 引用，而不必重复发送，最后下载智能体创建的文件。

假设你在构建一个理赔智能体。它从 Files API 读取受理单文档，遵循一个编码了团队申报流程的技能，用浏览器使用工具在保险公司的 Web 门户里完成提交，再把确认凭据保存为文件。代码执行与 Web 搜索（此前均已正式发布）也融入同一个回路。

### **正式发布带来了哪些新内容**

- **计算机使用：**更新后的计算机使用工具让 Claude 每一轮可以执行多个动作，而不是每次模型调用只执行一个，任务因此能用更少的调用、更少的时间完成。计算机使用现在也依据我们的 BAA（商业伙伴协议）支持受 HIPAA 监管的工作负载。
- **浏览器使用工具：**今天随计算机使用全新推出。它沿用同样的多动作轮次，并加入页面结构信息，智能体因此能比只靠像素更可靠地定位 Web 元素。
- **Skills API：**一个更简洁的 API，用于上传你自己的技能并管理版本。
- **Files API：**自动文件过期、5 倍的速率限制提升，以及每组织 1 TB 的存储空间。

「我们的智能体在没有 API 的医疗与保险系统内部工作。在新的计算机使用工具上，我们最长的理赔工作流从 32 分钟缩短到 13 分钟，我们测试的每一个工作流单任务成本下降约 30%，完成率达到 100%，而我们的提示没有做任何改动。」

「Skills API 为我们提供了一条直接的路径，把专门的文档创建能力内建到 Box Agent 中。对一家银行来说，一个技能捕获公司的授信方法论与获批的备忘录格式；Box Agent 将其应用于 Box 中已有的财务报表与交易文件，产出一份有据可查的授信备忘录，供分析师审阅。银行无需从零构建每一个智能体，就能获得面向复杂工作流的智能体。」

### **开始使用**

计算机使用工具、浏览器使用工具、Skills API 与 Files API 现已在 Claude Platform 上可用。Skills API 与 Files API 也可通过 Microsoft Foundry 使用；更新后的计算机使用与浏览器使用工具即将登陆 Google Cloud 的 Vertex AI。现有的 beta 集成在你迁移期间继续可用。请参阅[计算机使用](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)、[浏览器使用工具](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool)、[Skills API](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) 与 [Files API](https://platform.claude.com/docs/en/build-with-claude/files) 的文档以开始使用。

FAQ（常见问题）
