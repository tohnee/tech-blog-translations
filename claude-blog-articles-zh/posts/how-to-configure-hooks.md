---
title: "Claude Code 高级用户定制：如何配置 hooks"
title_en: "Claude Code power user customization: How to configure hooks"
source: https://claude.com/blog/how-to-configure-hooks/
crawled: 2026-09-14
translated: 2026-09-14
---

# Claude Code 高级用户定制：如何配置 hooks

> 原文：[Claude Code power user customization: How to configure hooks](https://claude.com/blog/how-to-configure-hooks/) · Claude 博客

即便是顺畅的 [Claude Code](https://www.claude.com/product/claude-code) 工作流，随着时间推移也会积累摩擦点。每次 Claude 写文件，[Prettier](https://prettier.io/) 都需要手动运行。每次它运行 npm test，都会出现同样的权限提示。每次会话开始，都要把同样的项目样板上下文粘贴进第一条消息。

好消息是：[Hooks](https://code.claude.com/docs/en/hooks-guide) 可以消除这些摩擦点。它们就像你可以配置的触发器，在特定动作之前或之后触发，让你能够把自定义逻辑、脚本和命令直接注入 Claude 的操作过程。

本文面向已经熟悉 Claude Code 基础的开发者，介绍高级配置。读完本文，你将了解八种 hook 类型、各自的使用时机、如何配置它们，以及出问题时如何调试。

让我们开始吧。

## **什么是 hook？**

hook 是你创建的自定义 shell 命令，当 Claude Code 会话中发生特定事件时自动执行，例如 Claude 即将写一个文件时，或你提交一条提示时。你可以把 hooks 用于非常广泛的用途：在动作执行之前拦截、注入智能体上下文、自动化批准，或在操作发生之前阻止它们。

hooks 在你的 settings 文件中配置，使用包含事件名称、匹配器（matcher，用于过滤哪些工具触发 hook）和要运行的命令的 JSON 结构。它们以你的用户权限在本地环境中执行，通过 stdin 接收触发事件的相关信息，并通过退出码和 stdout 传回结果。这让你无需修改工具本身，就能精确控制 Claude Code 的行为。

## **为什么要在 Claude Code 中使用 hooks？**

hooks 解决三类问题。

第一，**它们消除重复的手动步骤**。不必在每次文件改动后手动运行格式化工具，一个 PostToolUse hook 会自动处理。不必第一百次批准 npm test，一个 PermissionRequest hook 会自动放行。

第二，**hooks 自动执行项目专属规则**。你可以在危险命令执行前阻止它，在写入前校验文件路径，或确保命名约定得到遵守。这些防护栏（guardrail）每次都会运行，而不是只在你想起来检查时才运行。

第三，**hooks 无需人工投入即可注入动态上下文。**一个 SessionStart hook 可以把当前的 git 状态和 TODO 列表喂给 Claude。一个 UserPromptSubmit hook 可以把你的 sprint 优先级附加到每个请求上。Claude 始终掌握最新情况，而你不必反复重述。

## **Claude Code 的 hook 类型及使用时机**

Claude Code 提供八种 hook 事件，覆盖会话的完整生命周期：从启动，到工具执行，再到结束。每种 hook 在特定时刻触发，让你精确控制自动化在何时运行。选对 hook 取决于你想完成什么。

**Hooks 一览**

如果不需要图注，可以删除这一行

| Hook | 触发时机 | 常见用途 |
|---|---|---|
| PreToolUse | 工具执行之前 | 阻止危险命令、校验文件路径、自动批准安全操作 |
| PermissionRequest | 权限对话框出现之前 | 自动批准测试命令、阻止访问敏感文件 |
| PostToolUse | 工具完成之后 | 运行格式化工具、触发 linter、记录文件变更 |
| PreCompact | 上下文压缩之前 | 备份对话记录、保留重要决策 |
| SessionStart | 会话开始或恢复时 | 注入 git 状态、加载 TODO 列表、设置环境上下文 |
| Stop | Claude 完成回复时 | 验证任务完成、运行测试、生成摘要 |
| SubagentStop | 子智能体完成时 | 校验子智能体输出、触发后续动作 |
| UserPromptSubmit | 你提交提示时 | 注入 sprint 上下文、校验请求、添加动态上下文 |

### **PreToolUse**

这是最常用的 hook，在 Claude 选定要用的工具之后、工具真正执行之前触发。你的脚本可以检查计划中的动作，然后批准、阻止、请求用户确认或修改参数，还可以用匹配器过滤哪些工具触发这个 hook。

这个 PreToolUse hook 示例会在文件写入执行之前对其进行评估。Claude 会根据指定的标准审查计划中的动作，并可以依据提示逻辑批准、阻止或标记疑虑。

```
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/validate-file-path.sh"
          }
        ]
      }
    ]
  }
}
```

何时使用 PreToolUse：

- 阻止 rm -rf 或强制推送（force push）等危险的 Bash 命令
- 自动批准安全、重复的操作，减少提示疲劳
- 在写入前校验文件路径，防止意外覆盖
- 修改工具输入，注入项目专属默认值

### **PermissionRequest**

当 Claude 正常情况下会显示权限对话框时，这个 hook 触发。它拦截在你看到确认提示之前的那个时刻，让你的脚本决定是允许、拒绝，还是仍然询问用户。

```
{
  "hooks": {
    "PermissionRequest": [
      {
        "matcher": "Bash(npm test*)",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/validate-test-command.sh"
          }
        ]
      }
    ]
  }
}
```

这个示例自动批准任何以 npm test 开头的 Bash 命令。匹配器模式可以包含参数，实现更精细的控制。

何时使用 PermissionRequest：

- 自动批准你在一次会话中要运行几十遍的测试命令
- 阻止对生产配置文件的写访问
- 允许对特定目录的读取操作而不弹提示
- 拒绝任何匹配危险模式的命令

### **PostToolUse**

在工具成功完成后立即触发。你的脚本会收到关于发生了什么的信息，包括工具输出；可用匹配器过滤哪些工具触发它。

这个 PostToolUse 示例会对 Claude 写入或编辑的任何文件运行 Prettier。匹配器中的竖线语法表示它对 Write 和 Edit 两种工具都触发。

```
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "prettier --write \"$CLAUDE_TOOL_INPUT_FILE_PATH\""
          }
        ]
      }
    ]
  }
}
```

何时使用 PostToolUse：

- 每次文件写入后运行 Prettier、Black 或 gofmt，强制统一格式
- 把所有文件修改记录到审计日志
- 在代码变更后触发 linter 并显示警告
- 特定操作完成时发送通知

### **PreCompact**

在 Claude 压缩（compact）对话上下文以腾出空间之前触发。压缩会对对话中较旧的部分做摘要，这意味着一些细节会丢失。这个 hook 让你有机会在这些信息丢失之前把它们保存下来。

这个 PreCompact 示例会在自动压缩前备份对话记录。匹配器可以是 "auto" 或 "manual"，这样你可以区分自动压缩和用户触发的压缩事件。

```
{
  "hooks": {
    "PreCompact": [
      {
        "matcher": "auto",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/backup-transcript.sh"
          }
        ]
      }
    ]
  }
}
```

何时使用 PreCompact：

- 在摘要生成之前，把完整对话记录备份到文件
- 提取并保存重要决策或代码片段
- 记录会话里程碑，便于事后回顾

### **SessionStart**

在 Claude Code 开始新会话或恢复既有会话时触发。你的脚本输出的任何内容都会被加入对话上下文，因此 Claude 一开始就带着这些信息。

```
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "git status --short && echo '---' && cat TODO.md"
          }
        ]
      }
    ]
  }
}
```

每次会话开始时，Claude 都知道你当前的 git 状态和 TODO 列表。stdout 会自动成为上下文。

何时使用 SessionStart：

- 把你当前的 git 分支和最近提交喂给 Claude
- 加载 TODO 列表或 sprint backlog 的内容
- 注入特定环境的配置细节

### **Stop**

在 Claude 完成回复、正要等待你的下一个输入时触发。你的脚本可以检查 Claude 产出的内容，判断任务是否真正完成。

脚本可以返回带 "continue": true 的 JSON，让 Claude 继续工作，这对多步骤工作流很有用：

```
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Review whether the task is complete. If all requirements are met, respond with 'complete'. If work remains, respond with 'continue' and specify what still needs to be done."
          }
        ]
      }
    ]
  }
}
```

何时使用 Stop：

- 强制 Claude 持续工作，直到检查清单上的所有条目都完成
- 在判定任务完成之前，验证测试是否通过
- 在会话结束时触发摘要生成
- 在停止前确认生成的代码可以编译

### **SubagentStop**

每当通过 Task 工具创建的子智能体（subagent）完成时，这个 hook 触发。工作方式与 Stop 相同，但专门在子智能体（而非主智能体）完成其动作时触发。SubagentStop 的配置与 Stop hook 结构一致：

```
{
  "hooks": {
    "SubagentStop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Evaluate the subagent's output. Verify the task was completed correctly and the results meet quality standards. If the output is satisfactory, respond with 'accept'. If issues exist, respond with 'reject' and explain what needs to be fixed."
          }
        ]
      }
          ]
  }
}

```

何时使用 SubagentStop：

- 校验子智能体的输出是否达到质量标准
- 根据子智能体的结果触发后续动作
- 记录子智能体的活动，便于调试或审计

### **UserPromptSubmit**

在你提交提示时、Claude 处理它之前触发。你的脚本通过 stdout 输出的任何内容都会随你的提示一起加入 Claude 的上下文，这使得 UserPromptSubmit 非常适合动态注入 Claude 应当考虑的信息。

在这个示例中，每次你提交提示，Claude 都会收到你的 sprint 上下文文件的内容。这让 Claude 始终了解当前优先级，而无需你反复重述。

```
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "cat ./current-sprint-context.md"
          }
        ]
      }
    ]
  }
}
```

何时使用 UserPromptSubmit：

- 每条提示都注入当前的 sprint 上下文或项目优先级
- 在提示到达 Claude 之前进行校验
- 根据内容阻止特定类型的请求
- 添加动态上下文，例如最近的错误日志或测试结果

## **配置与文件位置**

hooks 存放在三个层级的 JSON settings 文件中。项目级 hooks 放在仓库内的 .claude/settings.json 中，可以与团队共享。用户级 hooks 放在 ~/.claude/settings.json 中，对你所有项目生效。本地项目级 hooks 放在 .claude/settings.local.json 中，用于你不想提交的个人配置。

项目级设置优先于用户级设置。此外还有面向组织管控的企业托管策略设置。完整细节请参阅 Claude Code 的 settings 说明。

**Pro tip：**这也是你可以为 Claude 的动作设置细粒度权限的同一个文件，支持项目级、用户级或本地级。例如，你可以显式允许 Claude 读取某个目录下的所有文件，省去每次批准的麻烦；或者阻止对敏感文件的任何修改。

## **匹配器语法**

匹配器（matcher）是你过滤哪些工具可以触发 hook 的方式。它们只适用于 PreToolUse、PostToolUse 和 PermissionRequest 这三种 hook。

简单字符串匹配的行为正如你所预期："Write" 只匹配 Write 工具。

例如：

```
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "your-command-here"
          }
        ]
      }
    ]
  }
}
```

竖线语法让你匹配多个工具："Write|Edit" 对两者都触发；而通配符匹配一切："*" 或空字符串匹配所有工具。

**注意：**匹配器区分大小写，所以 "bash" 不会匹配到 Bash 工具。

要更精细的控制，可以使用参数模式，如 "Bash(npm test*)"，匹配特定的命令参数。MCP 工具模式遵循 "mcp__memory__.*" 格式，用于 Model Context Protocol 工具。

## **输入、输出与结构化响应**

### **hooks 接收什么**

所有 hook 都会通过 stdin 接收包含会话信息和事件特定数据的 JSON。常见字段包括：session_id、transcript_path、cwd、permission_mode 和 hook_event_name。

此外，与工具相关的 hook 还会收到 tool_name 和 tool_input。这些数据让你的脚本能够基于充分的信息决定如何响应。

### **hooks 如何响应**

退出码决定基本结果。退出码 0 表示成功，stdout 要么作为 JSON 处理，要么加入上下文。退出码 2 表示阻断性错误：stderr 成为错误消息，动作被阻止。

其他退出码表示非阻断性错误，stderr 会在详细（verbose）模式下显示。

除退出码之外，hook 还可以返回结构化 JSON 以获得更多控制。字段包括：decision（approve、block、allow 或 deny）、reason（展示给 Claude 的解释）、continue（用于 Stop hook 强制继续）和 updatedInput（在执行前修改工具参数）。

## **环境与执行**

hooks 可以访问环境变量，包括：CLAUDE_PROJECT_DIR（项目根路径）、CLAUDE_CODE_REMOTE（在 web 环境中为 true）和 CLAUDE_ENV_FILE（供 SessionStart hook 持久化变量）。你 shell 中的标准环境变量同样可以访问。

另外值得注意的是：hooks 默认有 60 秒超时，可按 hook 单独配置。当多个 hook 匹配同一事件时，它们并行运行。相同的命令会自动去重。

## **安全注意事项**

hooks 会以你的用户权限执行任意 shell 命令。Claude Code 内置了一道保障：对 hook 配置文件的直接修改，需要在 /hooks 菜单中经过审查才能生效。这可以防止恶意代码悄悄向你的配置中添加 hooks。

不过，一旦你配置并批准了 hooks，它们就会以你的权限级别执行。

**Pro tip：**在任何环境中运行命令之前，请先评估风险。如果你打算用 hooks 运行命令，请考虑以下良好实践：校验并清洗来自 stdin 的输入、给 shell 变量加引号以防注入、为脚本使用绝对路径，以及避免处理 .env 或凭据这类敏感文件。

## **调试与测试**

Claude Code 会把所有内容记录到 transcript 文件中，无需任何设置就能看到工具调用和响应。每个 hook 都会收到一个 transcript_path 字段，指向一个包含完整会话历史的 JSONL 文件。你可以用一个 SessionStart hook 来记录每个 transcript 的位置：

```
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '\"Session: \" + .transcript_path' >> ~/.claude/sessions.log"
          }
        ]
      }
    ]
  }
}
```

然后 tail 这个 transcript，实时观察 Claude 的工作：`tail -f /path/to/transcript.jsonl | jq` 。

### **针对 hook 的调试**

要针对 hook 本身调试，请为你的 hook 脚本添加日志。transcript 文件会显示 Claude 做了什么，但不会显示你的 hook 为何做出了批准或阻止某个动作的决定。

稍加努力，你可以添加一个小的 bash 脚本，包裹你的工具并记录额外信息。例如 log-wrapper.sh：

```
#!/bin/bash
LOG=~/.claude/hooks.log
INPUT=$(cat)

TOOL=$(echo "$INPUT" |
 jq -r '.tool_name // "n/a"')
EVENT=$(echo "$INPUT" | jq -r '.hook_event_name // "n/a"')

echo "=== $(date) | $EVENT | $TOOL ===" >> "$LOG"

echo "$INPUT" | "$1"
CODE=$?

echo "Exit: $CODE" >> "$LOG"
exit $CODE
```

这个小小的包裹脚本把 stdin 捕获到一个变量，记录时间戳和工具名，然后把输入传给你的实际工具。

写好 log-wrapper.sh 之后，在 hook 中把它前置到工具调用上：

```
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "log-wrapper.sh your-tool-command.py"
          }
        ]
      }
    ]
  }
}
```

**Pro tip：**更多调试技巧，请查阅 Claude Code 调试文档。

## **构建你自己的 hooks**

从一个简单的 hook 开始，解决你工作流中一个真实的摩擦点。PostToolUse 格式化 hook 是很好的第一选择，因为反馈立竿见影、清晰可见。跑通之后，再根据你学到的东西逐步扩展。

完整的参考文档（包括所有可用字段和高级模式），请参阅官方 hooks 文档。

hooks 让你按照自己的工作流来塑造 Claude Code，而不是让自己的工作流去适应工具。在配置 hooks 上的投入，每一次会话都会获得回报。

*今天就开始用 hooks 定制你的 [Claude Code](https://www.claude.com/product/claude-code) 工作流吧。*

FAQ（常见问题）
