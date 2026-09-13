---
title: "Desktop Extensions：为 Claude Desktop 带来一键安装 MCP 服务器"
title_en: "Desktop Extensions: One-click MCP server installation for Claude Desktop"
source: https://www.anthropic.com/engineering/desktop-extensions
published: 2025-06-26
crawled: 2026-09-11
translated: 2026-09-11
---

# Desktop Extensions：为 Claude Desktop 带来一键安装 MCP 服务器

> 原文：[Desktop Extensions: One-click MCP server installation for Claude Desktop](https://www.anthropic.com/engineering/desktop-extensions) · Anthropic Engineering Blog

- 文件扩展名更新

  2025 年 9 月 11 日

  Claude Desktop Extensions 现在使用 .mcpb（MCP Bundle）文件扩展名，取代 .dxt。现有的 .dxt 扩展将继续可用，但我们建议开发者今后的新扩展采用 .mcpb。所有功能保持不变——这纯粹是一次命名规范的更新。

—

去年我们发布模型上下文协议（Model Context Protocol，MCP）时，看到开发者构建了出色的本地服务器，让 Claude 能访问从文件系统到数据库的各种资源。但我们不断听到同样的反馈：安装太复杂了。用户需要安装开发者工具、手动编辑配置文件，还常常被依赖问题卡住。

今天，我们推出 Desktop Extensions——一种新的打包格式，让安装 MCP 服务器简单到点一下按钮。

### 解决 MCP 安装难题

本地 MCP 服务器为 Claude Desktop 用户解锁了强大的能力。它们可以与本地应用交互、访问私有数据、与开发工具集成——同时把数据留在用户自己的机器上。然而，当前的安装过程设置了不少障碍：

- **需要开发者工具**：用户必须安装 Node.js、Python 或其他运行时
- **手动配置**：每个服务器都要求编辑 JSON 配置文件
- **依赖管理**：用户必须自行解决包冲突和版本不匹配
- **没有发现机制**：寻找有用的 MCP 服务器只能靠在 GitHub 上搜索
- **更新复杂**：保持服务器最新意味着手动重装

这些摩擦点意味着 MCP 服务器尽管强大，对非技术用户来说基本不可及。

### Desktop Extensions 登场

Desktop Extensions（`.mcpb` 文件）通过把整个 MCP 服务器——连同全部依赖——打包成单个可安装文件，解决了这些问题。用户侧的变化如下：

**改进前：**

```
# Install Node.js first 
npm install -g @example/mcp-server 
# Edit ~/.claude/claude_desktop_config.json manually 
# Restart Claude Desktop 
# Hope it works
```

**改进后：**

1. 下载一个 `.mcpb` 文件
2. 双击用 Claude Desktop 打开
3. 点击「Install」

就这么简单。没有终端、没有配置文件、没有依赖冲突。

## 架构总览

一个 Desktop Extension 是一个 zip 压缩包，内含本地 MCP 服务器和一个 `manifest.json`——后者描述了 Claude Desktop 以及其他支持桌面扩展的应用需要知道的一切。

```
extension.mcpb (ZIP archive)
├── manifest.json         # Extension metadata and configuration
├── server/               # MCP server implementation
│   └── [server files]    
├── dependencies/         # All required packages/libraries
└── icon.png             # Optional: Extension icon

# Example: Node.js Extension
extension.mcpb
├── manifest.json         # Required: Extension metadata and configuration
├── server/               # Server files
│   └── index.js          # Main entry point
├── node_modules/         # Bundled dependencies
├── package.json          # Optional: NPM package definition
└── icon.png              # Optional: Extension icon

# Example: Python Extension
extension.mcpb (ZIP file)
├── manifest.json         # Required: Extension metadata and configuration
├── server/               # Server files
│   ├── main.py           # Main entry point
│   └── utils.py          # Additional modules
├── lib/                  # Bundled Python packages
├── requirements.txt      # Optional: Python dependencies list
└── icon.png              # Optional: Extension icon
```

Desktop Extension 中唯一必需的文件是 manifest.json。其余复杂度都由 Claude Desktop 处理：

- **内置运行时**：Claude Desktop 自带 Node.js，免除外置依赖
- **自动更新**：有新版本时扩展自动更新
- **安全存储密钥**：API 密钥等敏感配置存放在操作系统钥匙串中

清单（manifest）包含人类可读的信息（如名称、描述、作者）、功能声明（工具、提示）、用户配置和运行时要求。大多数字段都是可选的，所以最简版本相当短。不过在实践中，我们预计三种受支持的扩展类型（Node.js、Python 和经典二进制/可执行文件）都会包含文件：

```
{
  "mcpb_version": "0.1",                    // MCPB spec version this manifest conforms to
  "name": "my-extension",                   // Machine-readable name (used for CLI, APIs)
  "version": "1.0.0",                       // Semantic version of your extension
  "description": "A simple MCP extension",  // Brief description of what the extension does
  "author": {                               // Author information (required)
    "name": "Extension Author"              // Author's name (required field)
  },
  "server": {                               // Server configuration (required)
    "type": "node",                         // Server type: "node", "python", or "binary"
    "entry_point": "server/index.js",       // Path to the main server file
    "mcp_config": {                         // MCP server configuration
      "command": "node",                    // Command to run the server
      "args": [                             // Arguments passed to the command
        "${__dirname}/server/index.js"      // ${__dirname} is replaced with the extension's directory
      ]                              
    }
  }
}
```

[清单规范](https://github.com/anthropics/dxt/blob/main/MANIFEST.md)中有许多便利选项，旨在让本地 MCP 服务器的安装和配置更轻松。服务器配置对象的定义方式既为模板字面量形式的用户自定义配置留了空间，也支持平台特定的覆盖。扩展开发者可以详细定义想从用户那里收集哪些配置。

来看一个清单如何辅助配置的具体例子。下面的清单中，开发者声明用户需要提供 `api_key`。在用户提供该值之前，Claude 不会启用这个扩展；该值会被自动保存在操作系统的密钥库中，并在启动服务器时透明地把 `${user_config.api_key}` 替换为用户提供的值。类似地，`${__dirname}` 会被替换为扩展解包目录的完整路径。

```
{
  "mcpb_version": "0.1",
  "name": "my-extension",
  "version": "1.0.0",
  "description": "A simple MCP extension",
  "author": {
    "name": "Extension Author"
  },
  "server": {
    "type": "node",
    "entry_point": "server/index.js",
    "mcp_config": {
      "command": "node",
      "args": ["${__dirname}/server/index.js"],
      "env": {
        "API_KEY": "${user_config.api_key}"
      }
    }
  },
  "user_config": {
    "api_key": {
      "type": "string",
      "title": "API Key",
      "description": "Your API key for authentication",
      "sensitive": true,
      "required": true
    }
  }
}
```

一份包含大多数字段的可选值的完整 `manifest.json` 大致如下：

```
{
  "mcpb_version": "0.1",
  "name": "My MCP Extension",
  "display_name": "My Awesome MCP Extension",
  "version": "1.0.0",
  "description": "A brief description of what this extension does",
  "long_description": "A detailed description that can include multiple paragraphs explaining the extension's functionality, use cases, and features. It supports basic markdown.",
  "author": {
    "name": "Your Name",
    "email": "yourname@example.com",
    "url": "https://your-website.com"
  },
  "repository": {
    "type": "git",
    "url": "https://github.com/your-username/my-mcp-extension"
  },
  "homepage": "https://example.com/my-extension",
  "documentation": "https://docs.example.com/my-extension",
  "support": "https://github.com/your-username/my-extension/issues",
  "icon": "icon.png",
  "screenshots": [
    "assets/screenshots/screenshot1.png",
    "assets/screenshots/screenshot2.png"
  ],
  "server": {
    "type": "node",
    "entry_point": "server/index.js",
    "mcp_config": {
      "command": "node",
      "args": ["${__dirname}/server/index.js"],
      "env": {
        "ALLOWED_DIRECTORIES": "${user_config.allowed_directories}"
      }
    }
  },
  "tools": [
    {
      "name": "search_files",
      "description": "Search for files in a directory"
    }
  ],
  "prompts": [
    {
      "name": "poetry",
      "description": "Have the LLM write poetry",
      "arguments": ["topic"],
      "text": "Write a creative poem about the following topic: ${arguments.topic}"
    }
  ],
  "tools_generated": true,
  "keywords": ["api", "automation", "productivity"],
  "license": "MIT",
  "compatibility": {
    "claude_desktop": ">=1.0.0",
    "platforms": ["darwin", "win32", "linux"],
    "runtimes": {
      "node": ">=16.0.0"
    }
  },
  "user_config": {
    "allowed_directories": {
      "type": "directory",
      "title": "Allowed Directories",
      "description": "Directories the server can access",
      "multiple": true,
      "required": true,
      "default": ["${HOME}/Desktop"]
    },
    "api_key": {
      "type": "string",
      "title": "API Key",
      "description": "Your API key for authentication",
      "sensitive": true,
      "required": false
    },
    "max_file_size": {
      "type": "number",
      "title": "Maximum File Size (MB)",
      "description": "Maximum file size to process",
      "default": 10,
      "min": 1,
      "max": 100
    }
  }
}
```

要看一个扩展及其清单的实例，请参考 [MCPB 仓库中的示例](https://github.com/anthropics/dxt/tree/main/examples)。

`manifest.json` 中所有必填与可选字段的完整规范，见我们的[开源工具链](https://github.com/anthropics/dxt/blob/main/MANIFEST.md)。

### 构建你的第一个扩展

我们来走一遍把现有 MCP 服务器打包成 Desktop Extension 的过程。以一个简单的文件系统服务器为例。

#### 第 1 步：创建清单

首先为你的服务器初始化一个清单：

```
npx @anthropic-ai/mcpb init
```

这个交互式工具会询问关于你服务器的信息，并生成完整的 manifest.json。如果你想以最快速度拿到最基础的 manifest.json，可以带 `--yes` 参数运行该命令。

#### 第 2 步：处理用户配置

如果你的服务器需要用户输入（如 API 密钥或允许访问的目录），在清单中声明：

```
"user_config": {
  "allowed_directories": {
    "type": "directory",
    "title": "Allowed Directories",
    "description": "Directories the server can access",
    "multiple": true,
    "required": true,
    "default": ["${HOME}/Documents"]
  }
}
```

Claude Desktop 将会：

- 展示友好的配置界面
- 在启用扩展前校验输入
- 安全存储敏感值
- 按开发者的配置，把配置以参数或环境变量的形式传给你的服务器

下面的例子把用户配置作为环境变量传递，但也可以作为参数。

```
"server": {
   "type": "node",
   "entry_point": "server/index.js",
   "mcp_config": {
   "command": "node",
   "args": ["${__dirname}/server/index.js"],
   "env": {
      "ALLOWED_DIRECTORIES": "${user_config.allowed_directories}"
   }
   }
}
```

#### 第 3 步：打包扩展

把所有内容打包成一个 `.mcpb` 文件：

```
npx @anthropic-ai/mcpb pack
```

这条命令会：

1. 校验你的清单
2. 生成 `.mcpb` 压缩包

#### 第 4 步：本地测试

把你的 `.mcpb` 文件拖进 Claude Desktop 的设置窗口。你会看到：

- 关于你扩展的人类可读信息
- 所需的权限和配置
- 一个简单的「Install」按钮

### 高级特性

#### 跨平台支持

扩展可以适配不同的操作系统：

```
"server": {
  "type": "node",
  "entry_point": "server/index.js",
  "mcp_config": {
    "command": "node",
    "args": ["${__dirname}/server/index.js"],
    "platforms": {
      "win32": {
        "command": "node.exe",
        "env": {
          "TEMP_DIR": "${TEMP}"
        }
      },
      "darwin": {
        "env": {
          "TEMP_DIR": "${TMPDIR}"
        }
      }
    }
  }
}
```

#### 动态配置

用模板字面量表示运行时值：

- `${__dirname}`：扩展的安装目录
- `${user_config.key}`：用户提供的配置
- `${HOME}, ${TEMP}`：系统环境变量

#### 功能声明

帮用户预先了解扩展的能力：

```
"tools": [
  {
    "name": "read_file",
    "description": "Read contents of a file"
  }
],
"prompts": [
  {
    "name": "code_review",
    "description": "Review code for best practices",
    "arguments": ["file_path"]
  }
]
```

### 扩展目录

我们随发布上线了内置于 Claude Desktop 的精选扩展目录。用户可以浏览、搜索、一键安装——无需翻 GitHub、无需审查代码。

虽然我们预计 Desktop Extension 规范以及 macOS 和 Windows 版 Claude 中的实现都会随时间演进，但我们期待看到扩展被以各种富有创意的方式用来拓展 Claude 的能力。

提交你的扩展：

1. 确保它遵循提交表单中的准则
2. 在 Windows 和 macOS 上都做好测试
3. [提交你的扩展](https://docs.google.com/forms/d/14_Dmcig4z8NeRMB_e7TOyrKzuZ88-BLYdLvS6LPhiZU/edit)
4. 我们的团队会对质量与安全进行审查

### 构建开放生态

我们致力于维护 MCP 服务器周围的开放生态，并相信它被多个应用和服务普遍采纳的能力已经惠及社区。本着这一承诺，我们将开源 Desktop Extension 规范、工具链，以及 macOS 和 Windows 版 Claude 实现其自身 Desktop Extensions 支持所使用的 schema 和关键函数。我们希望 MCPB 格式不仅让本地 MCP 服务器对 Claude 更具可移植性，也能惠及其他 AI 桌面应用。

我们正在开源：

- 完整的 MCPB 规范
- 打包与校验工具
- 参考实现代码
- TypeScript 类型与 schema

这意味着：

- **对 MCP 服务器开发者**：一次打包，在任何支持 MCPB 的地方运行
- **对应用开发者**：无需从零构建即可添加扩展支持
- **对用户**：在所有支持 MCP 的应用中获得一致的体验

规范和工具链有意以 0.1 版本发布，因为我们期待与更广大的社区一起演进和改进这个格式。期待听到你的声音。

### 安全与企业考量

我们理解扩展会带来新的安全考量，对企业用户尤其如此。随 Desktop Extensions 预览版，我们内置了多项保障：

#### 对用户

- 敏感数据留在操作系统钥匙串中
- 自动更新
- 可审计已安装的扩展

#### 对企业

- 支持 Group Policy（Windows）和 MDM（macOS）
- 可预装经批准的扩展
- 可拉黑特定扩展或发布者
- 可完全禁用扩展目录
- 可部署私有扩展目录

关于如何在你的组织内管理扩展的更多信息，参见我们的[文档](https://support.anthropic.com/en/articles/10949351-getting-started-with-model-context-protocol-mcp-on-claude-for-desktop)。

### 上手指南

准备好构建你自己的扩展了吗？从这里开始：

**对 MCP 服务器开发者**：查阅我们的[开发者文档](https://github.com/anthropics/dxt)——或者在你的本地 MCP 服务器目录里直接运行以下命令动手开始：

```
npm install -g @anthropic-ai/mcpb
mcpb init
mcpb pack
```

**对 Claude Desktop 用户**：更新到最新版本，在设置中寻找 Extensions 区块。

**对企业**：查阅我们的企业文档了解部署选项。

### 用 Claude Code 构建扩展

在 Anthropic 内部，我们发现 Claude 只需极少的干预就能出色地构建扩展。如果你也想用 Claude Code，我们建议先简要说明你想让扩展做什么，然后在提示中附上以下上下文：

```
I want to build this as a Desktop Extension, abbreviated as "MCPB". Please follow these steps:

1. **Read the specifications thoroughly:**
   - https://github.com/anthropics/mcpb/blob/main/README.md - MCPB architecture overview, capabilities, and integration patterns
   - https://github.com/anthropics/mcpb/blob/main/MANIFEST.md - Complete extension manifest structure and field definitions
   - https://github.com/anthropics/mcpb/tree/main/examples - Reference implementations including a "Hello World" example

2. **Create a proper extension structure:**
   - Generate a valid manifest.json following the MANIFEST.md spec
   - Implement an MCP server using @modelcontextprotocol/sdk with proper tool definitions
   - Include proper error handling and timeout management

3. **Follow best development practices:**
   - Implement proper MCP protocol communication via stdio transport
   - Structure tools with clear schemas, validation, and consistent JSON responses
   - Make use of the fact that this extension will be running locally
   - Add appropriate logging and debugging capabilities
   - Include proper documentation and setup instructions

4. **Test considerations:**
   - Validate that all tool calls return properly structured responses
   - Verify manifest loads correctly and host integration works

Generate complete, production-ready code that can be immediately tested. Focus on defensive programming, clear error messages, and following the exact
MCPB specifications to ensure compatibility with the ecosystem.
```

### 结语

Desktop Extensions 代表了用户与本地 AI 工具交互方式的根本转变。通过消除安装摩擦，我们让强大的 MCP 服务器触手可及——面向所有人，而不仅仅是开发者。

在内部，我们正在用桌面扩展分享高度实验性的 MCP 服务器——有的有趣，有的实用。一个团队实验了把我们的模型直接连上一台 GameBoy 能走多远，类似我们的[「Claude 玩宝可梦」研究](https://www.anthropic.com/news/visible-extended-thinking)。我们用 Desktop Extensions 打包了一个扩展，启动流行的 [PyBoy](https://github.com/Baekalfen/PyBoy) GameBoy 模拟器并让 Claude 接管操控。我们相信，把模型能力连接到用户本地机器上已有的工具、数据和应用，存在着数不清的机会。

![A desktop showing the PyBoy MCP with Super Mario Land start screen](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2Fd48f3ea1218a4b90450b9ab8134fa0e24db5a167-720x542.png&w=1920&q=75)

我们迫不及待想看到你构建的东西。催生出数千个 MCP 服务器的同一份创造力，如今一键即可触达数百万用户。准备好分享你的 MCP 服务器了吗？[提交你的扩展接受评审](https://forms.gle/tyiAZvch1kDADKoP9)。

![Interlocking puzzle piece with complex geometric shape and detailed surface texture](https://www-cdn.anthropic.com/images/4zrzovbb/website/43abe7e54b56a891e74a8542944dfbd33f07f49c-1000x1000.svg)

### 想了解更多？

浏览我们的课程：<https://anthropic.skilljar.com/>
