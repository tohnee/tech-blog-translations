---
title: "用 MCP 做代码执行：构建更高效的智能体"
title_en: "Code execution with MCP: Building more efficient agents"
source: https://www.anthropic.com/engineering/code-execution-with-mcp
published: 2025-11-04
crawled: 2026-09-11
translated: 2026-09-11
---

# 用 MCP 做代码执行：构建更高效的智能体

> 原文：[Code execution with MCP: Building more efficient agents](https://www.anthropic.com/engineering/code-execution-with-mcp) · Anthropic Engineering Blog

[模型上下文协议（Model Context Protocol，MCP）](https://modelcontextprotocol.io/)是把 AI 智能体连接到外部系统的开放标准。传统上，把智能体连接到工具和数据，需要为每一对组合写定制集成，造成碎片化和重复劳动，让真正互联的系统难以规模化。MCP 提供了一个通用协议——开发者只需在智能体中实现一次 MCP，即可解锁整个集成生态。

自 2024 年 11 月发布以来，MCP 的采用非常迅速：社区已构建了数千个 [MCP 服务器](https://github.com/modelcontextprotocol/servers)，[SDK](https://modelcontextprotocol.io/docs/sdk) 覆盖所有主流编程语言，业界已把 MCP 作为连接智能体与工具和数据的既成事实标准。

如今开发者日常构建的智能体已经能跨几十个 MCP 服务器、访问成百上千个工具。然而，随着接入工具数量增长，预先加载全部工具定义、并把中间结果经由上下文窗口传递，会拖慢智能体并推高成本。

本文将探讨代码执行如何让智能体更高效地与 MCP 服务器交互：处理更多工具，同时使用更少 token。

## **工具导致的 token 过度消耗让智能体效率下降**

随着 MCP 使用规模扩大，有两种常见模式会推高智能体的成本和延迟：

1. 工具定义撑爆上下文窗口；
2. 中间工具结果消耗额外 token。

### **1. 工具定义撑爆上下文窗口**

大多数 MCP 客户端把所有工具定义预先直接载入上下文，用直接工具调用语法暴露给模型。这些工具定义可能长这样：

```
gdrive.getDocument
     Description: Retrieves a document from Google Drive
     Parameters:
                documentId (required, string): The ID of the document to retrieve
                fields (optional, string): Specific fields to return
     Returns: Document object with title, body content, metadata, permissions, etc.
```

```
salesforce.updateRecord
    Description: Updates a record in Salesforce
    Parameters:
               objectType (required, string): Type of Salesforce object (Lead, Contact,      Account, etc.)
               recordId (required, string): The ID of the record to update
               data (required, object): Fields to update with their new values
     Returns: Updated record object with confirmation
```

工具描述占据更多上下文窗口空间，增加响应时间和成本。当智能体连接了数千个工具时，它在读取一个请求之前就要先处理数十万 token。

### **2. 中间工具结果消耗额外 token**

大多数 MCP 客户端允许模型直接调用 MCP 工具。例如，你可以对智能体说：「从 Google Drive 下载我的会议记录，并附到 Salesforce 线索上。」

模型会做类似这样的调用：

```
TOOL CALL: gdrive.getDocument(documentId: "abc123")
        → returns "Discussed Q4 goals...\n[full transcript text]"
           (loaded into model context)

TOOL CALL: salesforce.updateRecord(
			objectType: "SalesMeeting",
			recordId: "00Q5f000001abcXYZ",
  			data: { "Notes": "Discussed Q4 goals...\n[full transcript text written out]" }
		)
		(model needs to write entire transcript into context again)
```

每个中间结果都必须经过模型。在这个例子里，完整的通话记录流经模型两次。对一场 2 小时的销售会议来说，这可能意味着额外处理 50,000 个 token。更大的文档甚至可能超出上下文窗口上限，直接破坏工作流。

面对大文档或复杂数据结构，模型在工具调用之间复制数据时也更容易出错。

![Image of how the MCP client works with the MCP server and LLM.](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F9ecf165020005c09a22a9472cee6309555485619-1920x1080.png&w=3840&q=75)

MCP 客户端把工具定义载入模型的上下文窗口，并编排一个消息循环：每次工具调用与结果都要在操作之间流经模型。

## **用 MCP 做代码执行提升上下文效率**

随着代码执行环境在智能体中日益普遍，一个解决方案是把 MCP 服务器呈现为代码 API，而不是直接的工具调用。智能体随后可以编写代码与 MCP 服务器交互。这一方案同时应对了两个挑战：智能体可以只加载自己需要的工具，并在把结果传回模型之前先在执行环境中处理数据。

做法有很多。其一是从已连接的 MCP 服务器生成一棵包含全部可用工具的文件树。下面是一个 TypeScript 实现：

```
servers
├── google-drive
│   ├── getDocument.ts
│   ├── ... (other tools)
│   └── index.ts
├── salesforce
│   ├── updateRecord.ts
│   ├── ... (other tools)
│   └── index.ts
└── ... (other servers)
```

然后每个工具对应一个文件，类似：

```
// ./servers/google-drive/getDocument.ts
import { callMCPTool } from "../../../client.js";

interface GetDocumentInput {
  documentId: string;
}

interface GetDocumentResponse {
  content: string;
}

/* Read a document from Google Drive */
export async function getDocument(input: GetDocumentInput): Promise<GetDocumentResponse> {
  return callMCPTool<GetDocumentResponse>('google_drive__get_document', input);
}
```

上面 Google Drive 到 Salesforce 的例子就变成了这样的代码：

```
// Read transcript from Google Docs and add to Salesforce prospect
import * as gdrive from './servers/google-drive';
import * as salesforce from './servers/salesforce';

const transcript = (await gdrive.getDocument({ documentId: 'abc123' })).content;
await salesforce.updateRecord({
  objectType: 'SalesMeeting',
  recordId: '00Q5f000001abcXYZ',
  data: { Notes: transcript }
});
```

智能体通过探索文件系统来发现工具：列出 `./servers/` 目录找到可用的服务器（如 `google-drive` 和 `salesforce`），然后读取它需要的具体工具文件（如 `getDocument.ts` 和 `updateRecord.ts`）来理解每个工具的接口。这让智能体只为当前任务加载所需定义。token 用量从 150,000 降到 2,000——节省 98.7% 的时间和成本。

Cloudflare [发布了类似的发现](https://blog.cloudflare.com/code-mode/)，把用 MCP 做代码执行称为「Code Mode」。核心洞见相同：LLM 擅长写代码，开发者应当利用这一强项，构建与 MCP 服务器更高效交互的智能体。

## **用 MCP 做代码执行的收益**

用 MCP 做代码执行让智能体更高效地使用上下文：按需加载工具、在数据到达模型之前先行过滤、以及把复杂逻辑一步执行。这种做法还有安全与状态管理方面的好处。

### 渐进式披露

模型非常擅长浏览文件系统。把工具呈现为文件系统上的代码，模型就能按需读取工具定义，而不是预先全部读取。

另一种做法是在服务器上加一个 `search_tools` 工具来查找相关定义。例如，在使用上文假设的 Salesforce 服务器时，智能体搜索「salesforce」，只加载当前任务需要的工具。在 `search_tools` 工具中加入一个 detail level 参数，让智能体选择所需的详细程度（如仅名称、名称加描述、或含 schema 的完整定义），也有助于智能体节约上下文、高效找工具。

### 上下文高效的工具结果

处理大数据集时，智能体可以在代码中先过滤和转换结果再返回。设想取回一个 10,000 行的电子表格：

```
// Without code execution - all rows flow through context
TOOL CALL: gdrive.getSheet(sheetId: 'abc123')
        → returns 10,000 rows in context to filter manually

// With code execution - filter in the execution environment
const allRows = await gdrive.getSheet({ sheetId: 'abc123' });
const pendingOrders = allRows.filter(row => 
  row["Status"] === 'pending'
);
console.log(`Found ${pendingOrders.length} pending orders`);
console.log(pendingOrders.slice(0, 5)); // Only log first 5 for review
```

智能体看到的是 5 行，而不是 10,000 行。类似模式适用于聚合、跨多个数据源的 join、或提取特定字段——全都不会撑大上下文窗口。

#### **更强大且上下文高效的控制流**

循环、条件判断和错误处理可以用熟悉的代码模式完成，而不必串联单个工具调用。例如，如果你需要一条 Slack 部署通知，智能体可以写：

```
let found = false;
while (!found) {
  const messages = await slack.getChannelHistory({ channel: 'C123456' });
  found = messages.some(m => m.text.includes('deployment complete'));
  if (!found) await new Promise(r => setTimeout(r, 5000));
}
console.log('Deployment notification received');
```

这比在智能体循环中交替进行 MCP 工具调用和 sleep 命令高效得多。

此外，能够写出一棵待执行的条件树还能节省「首 token 延迟」：不必等模型逐个评估 if 语句，智能体可以让代码执行环境代劳。

### 保护隐私的操作

当智能体用 MCP 做代码执行时，中间结果默认留在执行环境内。这样，智能体只看到你显式打印或返回的内容——你不想与模型共享的数据可以流经你的工作流，而不进入模型的上下文。

对更敏感的工作负载，智能体 harness 可以自动对敏感数据做 token 化。例如，设想你需要把电子表格里的客户联系方式导入 Salesforce。智能体写道：

```
const sheet = await gdrive.getSheet({ sheetId: 'abc123' });
for (const row of sheet.rows) {
  await salesforce.updateRecord({
    objectType: 'Lead',
    recordId: row.salesforceId,
    data: { 
      Email: row.email,
      Phone: row.phone,
      Name: row.name
    }
  });
}
console.log(`Updated ${sheet.rows.length} leads`);
```

MCP 客户端拦截数据，在其到达模型之前对 PII 做 token 化：

```
// What the agent would see, if it logged the sheet.rows:
[
  { salesforceId: '00Q...', email: '[EMAIL_1]', phone: '[PHONE_1]', name: '[NAME_1]' },
  { salesforceId: '00Q...', email: '[EMAIL_2]', phone: '[PHONE_2]', name: '[NAME_2]' },
  ...
]
```

随后，当这些数据在另一次 MCP 工具调用中被共享时，MCP 客户端通过查找把它还原（untokenize）。真实的电子邮箱、电话号码和姓名从 Google Sheets 流向 Salesforce，但从不经过模型。这防止了智能体意外打印或处理敏感数据。你还可以用它定义确定性的安全规则，选择数据可以流向哪里、从哪里来。

### 状态持久化与技能

带文件系统访问的代码执行让智能体可以跨操作维持状态。智能体可以把中间结果写入文件，从而恢复工作、跟踪进度：

```
const leads = await salesforce.query({ 
  query: 'SELECT Id, Email FROM Lead LIMIT 1000' 
});
const csvData = leads.map(l => `${l.Id},${l.Email}`).join('\n');
await fs.writeFile('./workspace/leads.csv', csvData);

// Later execution picks up where it left off
const saved = await fs.readFile('./workspace/leads.csv', 'utf-8');
```

智能体还可以把自己的代码持久化为可复用函数。一旦智能体为某个任务写出了可用的代码，它就可以保存这份实现供未来使用：

```
// In ./skills/save-sheet-as-csv.ts
import * as gdrive from './servers/google-drive';
export async function saveSheetAsCsv(sheetId: string) {
  const data = await gdrive.getSheet({ sheetId });
  const csv = data.map(row => row.join(',')).join('\n');
  await fs.writeFile(`./workspace/sheet-${sheetId}.csv`, csv);
  return `./workspace/sheet-${sheetId}.csv`;
}

// Later, in any agent execution:
import { saveSheetAsCsv } from './skills/save-sheet-as-csv';
const csvPath = await saveSheetAsCsv('abc123');
```

这与[技能（Skills）](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)的概念紧密相关——为模型提升专门任务表现的可复用指令、脚本和资源文件夹。在这些已保存的函数上添加一个 SKILL.md 文件，就形成了一个模型可以引用和使用的结构化技能。假以时日，这让你的智能体积累起一个高层能力工具箱，演化出它最有效工作所需的脚手架。

注意，代码执行也引入了自身的复杂度。运行智能体生成的代码，需要一个带适当[沙箱机制](https://www.anthropic.com/engineering/claude-code-sandboxing)、资源限制和监控的安全执行环境。这些基础设施要求带来了直接工具调用所没有的运维开销和安全考量。代码执行的收益——更低的 token 成本、更低的延迟、更好的工具组合——应当与这些实现成本相权衡。

## **总结**

MCP 为智能体连接众多工具与系统提供了基础协议。然而一旦接入的服务器太多，工具定义和结果就会消耗过量 token，降低智能体效率。

尽管这里的许多问题看似新颖——上下文管理、工具组合、状态持久化——它们在软件工程中都有已知解法。代码执行把这些成熟的模式应用到智能体上，让它们用熟悉的编程结构与 MCP 服务器更高效地交互。如果你实现了这个方案，鼓励你把发现分享给 [MCP 社区](https://modelcontextprotocol.io/community/communication)。

### 致谢

*本文由 Adam Jones 和 Conor Kelly 撰写。感谢 Jeremy Fox、Jerome Swannack、Stuart Ritchie、Molly Vorwerck、Matt Samuels 和 Maggie Vo 对本文草稿的反馈。*
