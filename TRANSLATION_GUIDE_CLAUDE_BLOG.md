# 翻译规范（claude.com/blog 技术文章中文化）

本文件是 claude.com/blog（Claude 官方博客）技术文章翻译项目的规范。基础原则、输出格式、Claude Code 术语表与 [TRANSLATION_GUIDE_CLAUDECODE.md](TRANSLATION_GUIDE_CLAUDECODE.md) 完全一致（先读它），本文件只列差异与补充。

## 项目信息

- 范围：claude.com/blog 中筛选的 86 篇技术文章（清单 `claude-blog-articles/meta.json`；客户故事、产品发布、企业合规、活动类不收录）
- 英文存档：`claude-blog-articles/posts/<slug>.md`
- 输出目录：`claude-blog-articles-zh/posts/<slug>.md`（同名镜像）
- 进度索引：`claude-blog-articles-zh/README.md`

## 输出文件头格式

源文件 frontmatter：`title / date / source / crawled`。译文：

```markdown
---
title: "中文标题"
title_en: "Original English Title"
source: https://claude.com/blog/<slug>/
crawled: 2026-09-14
translated: 2026-09-14
---

# 中文标题

> 原文：[Original English Title](source URL) · Claude 博客

（正文译文……）
```

## 本项目补充约定

1. 本博客文章多含「引导句 + 解释」的营销化段落，仍按全文翻译处理，不删减；但站点导航、"Related content"、"Subscribe" 订阅框、页脚等抓取噪音跳过不译（正文段落必须全部翻译）。
2. 文中引用的 X/Twitter 链接、YouTube 链接 URL 保留，链接文字翻译。
3. 文末若有 "Continue reading" 相关文章推荐列表，属站点噪音，跳过。
4. 日期行（如 "April 30, 2026"）保留在正文开头，格式统一为「2026 年 4 月 30 日」。

## 补充术语（在 claudecode 术语表基础上）

| English | 中文 |
|---|---|
| Cowork | Cowork（不译） |
| Skills / Agent Skills | Skills / 智能体技能（Skills，全文可保留英文） |
| Claude Agent SDK | Claude Agent SDK（不译） |
| managed agents | 托管智能体 |
| routines | 例行任务（routines） |
| hooks | hooks（不译） |
| subagent | 子智能体 |
| prompt caching | 提示缓存（prompt caching） |
| context engineering | 上下文工程 |
| context compaction / compaction | 上下文压缩（compaction） |
| memory | 记忆 |
| connectors | 连接器 |
| computer use | 计算机使用（computer use） |
| tool use | 工具使用 |
| effort level | 努力等级（effort level） |
| loops | loops（Claude Code 功能名，不译） |
| dynamic workflows | 动态工作流 |
| verification loop | 验证回路 |
| apps gateway | 应用网关 |
| checkpoint | 检查点 |
| rate limit | 速率限制 |
| 1M context | 1M 上下文 |
| inference / inference stack | 推理 / 推理栈 |
| Trainium2 | Trainium2（不译） |
| distillation | 蒸馏 |

## 模型名

Claude、Opus 4.x、Sonnet 4.x、Haiku 4.x、Claude 2.1、Fable、Mythos 等一律保留官方写法，不译。
