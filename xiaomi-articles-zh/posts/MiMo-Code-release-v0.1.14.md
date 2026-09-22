---
title: "v0.1.14（MiMo-Code）"
title_en: "v0.1.14 (MiMo-Code)"
date: 2026-09-02
source: https://github.com/XiaomiMiMo/MiMo-Code/releases/tag/v0.1.14
crawled: 2026-09-22
translated: 2026-09-22
---

# MiMo-Code v0.1.14 发布说明

> 原文：[v0.1.14 (MiMo-Code)](https://github.com/XiaomiMiMo/MiMo-Code/releases/tag/v0.1.14) · 小米 MiMo

## 概要

中断或出错的回合仍可恢复：未完成的 assistant 消息会保留为候选，`/recover` 以 append-only 方式续跑，不改写历史。

会话标题可通过专用 API 生成（`POST /experimental/title` 与 `genTitle` helper）；首选模型不可用或返回无效结果时，会回退到 lite model。

TUI 语音输入升级为基于工具的 `voice_input` 协议：ASR 按光标/选区做 insert 或 set，发送始终由 send 字段显式触发；调用 schema 经过校验，模型可以稳定驱动。

本版本还包括：compaction 保留 summary 以及生成期间到达的 API 轮次，触发条件改为上下文窗口的固定 90%，重建后的 tail 收成活动日志；删除 `actor` spawn/run 中未实现的 resume 参数，把模型导向本来就能用的 `send`；子代理经 `exec` 使用 `actor` 时仅允许 `send`；嵌套 `exec` 调用会持久化且可在 TUI 回放；同会话子代理继承父级权限；会话 system prefix 冻结进快照以保持 prompt-cache 前缀稳定；可选的 `auto_worktree` 提示（默认关闭）；mate、pdf-official 中日文字体与 pptx-official 配图规则等 skill 更新；以及 provider/重试、MCP、compose-next 与构建相关修复。

---

## 新特性

- **tui:** 将语音输入升级为基于工具的 `voice_input` 协议（按光标/选区 insert/set、显式发送、schema 校验），作者 @yanyihan-xiaomi，见 #2308、#2309
- **session:** 将 compaction 呈现为 summary 加压缩时段的 tail；在上下文窗口的固定 90% 处触发；新增 `MIMOCODE_COMPACTION_MAX_CONTEXT` 环境变量默认值，作者 @MiMoHardFather，见 #2294、#2263、#2260
- **session:** 支持以 append-only 方式恢复被中断的回合（`/recover`、TUI 恢复操作）；出错的 assistant 消息保留为恢复候选，作者 @wqymi，见 #2205、#2279
- **session:** 将重建后的 tail 折叠为紧凑的活动日志，而非逐字回放工具结果，作者 @wqymi，见 #2275
- **session:** 将每个会话的 system prefix 冻结到持久快照中；把技能目录从用户消息移到 system 尾部；保持 prompt cache 前缀稳定，作者 @MiMoHardFather，见 #2289、#2287、#2258
- **sdk:** 暴露可靠的 `POST /experimental/title` / `genTitle`，带 lite-model 回退与写入保护，作者 @wqymi，见 #2228
- **actor:** 移除未实现的 spawn/run `actor_id` resume 参数；保留 `send` 作为唤醒并继续子代理的路径，作者 @yanyihan-xiaomi，见 #2262
- **actor:** 子代理经 `exec` 发起的 `actor` 调用仅允许 `send`，作者 @wqymi，见 #2217、#2223
- **exec:** 持久化可回放的嵌套工具部分（带版本的快照、TUI 渲染器、防抖），作者 @yanyihan-xiaomi，见 #2222
- **permission:** 同会话子代理继承父级授权（继承父级时回退到当前会话 id），作者 @wqymi，见 #2273
- **config:** 新增 `auto_worktree` 开关（默认关闭）；基于路径的每会话一次主 worktree 变更提示，作者 @wqymi，见 #2227、#2270、#2292
- **skill:** 新增用于创建桌面宠物的 `mate` 内置技能，作者 @oscar-cao7，见 #2225
- **skill:** pdf-official 中日韩字体协议（按操作系统的 TTF 字体梯度、CID STSong-Light 回退、绝不用 Helvetica），作者 @oscar-cao7，见 #2189
- **skill:** pptx-official 图片来源决策规则（绘制 / 引用 / 搜索 / 生成；受限的 `image_gen` 预算），作者 @oscar-cao7，见 #2265
- **provider:** 将小米 PTC 路由到 Responses 自定义 exec；在 GPT 工具过滤下保持 exec 网关可用，作者 @MiMoHardFather，见 #2203、#2183
- **tool-script:** 类型化的 `exec_command` 参数（`cmd`、`yield_time_ms`、`workdir`）；解析带 MCP 前缀的工具别名，作者 @MiMoHardFather，见 #2180、#2202

## 问题修复

- **provider:** 为大模型家族使用 128K 输出默认值；对齐大模型的输出与 compaction 预留，作者 @MiMoHardFather，见 #2181、#2182
- **provider:** 稳定 `defaultModel` 回退（配置 → 最近使用 → id 升序首个允许项；不按菜单优先级排序），作者 @wqymi，见 #2306
- **session:** 集中管理供应商重试协调（终态 vs 瞬时、Retry-After、产生副作用后不回放活跃步骤），作者 @wqymi，见 #2216
- **session:** 将 `replace-agent` 的基础覆盖限定在主/对等 actor，使子代理保留自己的 agent 提示词，作者 @MiMoHardFather，见 #2264
- **session:** 允许文件/搜索工具在工作区内使用相对路径，作者 @yanyihan-xiaomi，见 #2251
- **session:** 将文本部分的创建推迟到首个 delta（数据库中不再有空文本壳），作者 @wqymi，见 #2193
- **skill:** 用 glob 前缀匹配替换有缺陷的 skill-tools 过滤；移除 skill-search 提醒基础设施，作者 @MiMoHardFather，见 #2166、#2168
- **llm-server:** 公告 `Server.listen`，使 `mimo llm-server issue` 能解析出真实的 `base_url`；在服务停止时 publish/unpublish，作者 @wqymi，见 #2293
- **mcp:** 在 stdio 启动失败时记录本地启动退出码与 stderr 尾部，作者 @wqymi，见 #2269
- **mcp:** 在 OAuth 回调页面与 DCR 客户端注册中显示 MiMoCode 品牌信息，作者 @MiMoHardFather，见 #2301
- **compose-next:** 要求 spec 落到 worktree 中（流水线 `grill → workspace → spec → implement`），作者 @yanyihan-xiaomi，见 #2307
- **actor:** 按会话隔离 fork 上下文，避免重复的 actor id 跨会话冲突，作者 @wqymi，见 #2259
- **build:** 防止祖先目录 `node_modules` 中的 bun 劫持编译产物（固定版本检查 + `process.execPath`），作者 @MiMoHardFather，见 #2291
- **build-node:** 为 node 目标定义 `MIMOCODE_VERSION`，使嵌入式构建不再解压到 `builtin_skills/local/` 之下，作者 @yanyihan-xiaomi，见 #2297

## 重构

- **skill:** 将 `drive-mimo` 移到仓库范围（`.mimocode/skills/`），不再放在产品级内置包中，作者 @yanyihan-xiaomi，见 #2210
- **session:** 简化 harness 选择——显式 harness 标志是唯一事实来源；PTC 传输不再自动选择 GPT 工具集；`MIMOCODE_CODEX_MODE=false` 对每个模型强制使用默认 harness，作者 @MiMoHardFather，见 #2243、#2252、#2303
- **tool:** 移除独立的 `change_directory`；shell/code 模式命令要求使用绝对工作目录，作者 @yanyihan-xiaomi，见 #2239
- **prompt:** 将 Tools 一节重写为「使用你的工具」指南；指令文件默认开启并与动态 system prompt 标志解耦，作者 @MiMoHardFather，见 #2302、#2285

## 内部 / CI

- **session:** 为固定 90% 触发阈值重新调校自动溢出测试夹具，作者 @yanyihan-xiaomi，见 #2266
- **sdk:** 重新生成 openapi 与 js sdk 类型（投影 schema、harness 描述、compaction 字段文档），作者 @yanyihan-xiaomi，见 #2310
- **chore:** 版本号升至 0.1.14，作者 @yanyihan-xiaomi，见 #2311

**完整变更日志**: https://github.com/XiaomiMiMo/MiMo-Code/compare/v0.1.13...v0.1.14
