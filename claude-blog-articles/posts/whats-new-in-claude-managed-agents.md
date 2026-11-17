---
title: "New in Claude Managed Agents: run agents on a schedule and store environment variables in vaults"
date: 2026-06-09
source: https://claude.com/resources/articles/whats-new-in-claude-managed-agents
crawled: 2026-11-17
---

# New in Claude Managed Agents: run agents on a schedule and store environment variables in vaults

* Category[Product updates](/resources/product-updates)
* ProductClaude Platform
* DateJune 9, 2026
* Reading time5 min
* ShareCopy link

Starting today, [Claude Managed Agents](https://claude.com/resources/articles/claude-managed-agents) can run on a schedule and securely access CLI tools and other authenticated services. Both features are now available in public beta on the Claude Platform.

## **Scheduled deployments: Run agents on a schedule**

Agents can now run on a schedule, completing routine work automatically. A [scheduled deployment](https://platform.claude.com/docs/en/managed-agents/scheduled-deployments) runs a Claude Managed Agent on a cron schedule. Each time the schedule fires, the agent starts a new session and completes its task, with no scheduler for you to build or host.

Use it for recurring work like a nightly data sync, a weekly compliance scan, or a daily digest. Once a deployment is live, you can pause, resume, or archive it at any time, or trigger additional runs on demand.

![](https://assets.claude.com/baff2128f2d026b8c6892798adfc4021170bce04.png)

Teams are already using scheduled deployments to automate recurring work:

* [Rakuten](https://claude.com/customers/rakuten-qa) uses scheduled deployments to analyze spreadsheet data and produce reports and decks on a weekly or monthly schedule. Teams also monitor production logs and metrics, allowing product managers to see application health without creating a dashboard.
* [Actively AI](https://actively.ai/) uses Managed Agents to power cross-account agentic search for sales teams. Scheduled deployments refresh answers regularly, simplifying their stack by replacing scheduling infrastructure the team initially built themselves.[‍](https://ando.so)
* [Ando](https://ando.so) uses scheduled deployments to keep hiring and sales teams moving. Agents autonomously watch channels for proposed next steps, follow up when they're due, and send meeting reminders.

## **Vaults: store environment variables to authenticate CLIs and other tools**

[Vaults](https://platform.claude.com/docs/en/managed-agents/vaults) securely store environment variables and credentials for Claude Managed Agents. At runtime, agents access secrets like API keys as environment variables, so they can authenticate CLI tools and other services without hardcoding credentials into prompts or code.

Agents [connect to external systems](https://claude.com/resources/articles/building-agents-that-reach-production-systems-with-mcp) through direct API calls, CLIs, and MCP. CLIs let agents drive existing command-line tools directly through a shell, making them a fast, lightweight integration path. Register an API key with an environment variable name and the domains it can reach, and the CLIs installed in an agent's sandbox can use it to make authenticated API calls.

The agent never sees your key because the sandbox only holds a placeholder. The real key is attached at the network boundary, and only on requests to domains you allow, so it only goes where you’ve approved. To change a key, update it in the vault, and running sessions will pick up the new value on their next call. Most CLIs that send their key in an HTTP request work this way, including the Browserbase, KERNEL, Notion, Ramp, and Sentry CLIs. [Browserbase](https://docs.browserbase.com/integrations/anthropic/managed-agents/quickstart) and [KERNEL](https://www.kernel.sh/docs/integrations/claude-managed-agents) give Managed Agents browser capabilities for the first time, so agents can navigate and interact with the web alongside their other tools.

![](https://assets.claude.com/e17afdf706d61056b4686ea4649ab1f0ee2e706e.png)

Teams are using environment variables in vaults to give agents secure access to authenticated tools:

* [Notion](https://claude.com/customers/notion-qa) uses environment variables in vaults to roll out its CLI alongside MCP tools, adding file-upload capabilities to its agents without API tokens ever being handed to the model.
* [Browserbase](https://www.browserbase.com/) built its public catalog of browser skills using the [browse CLI](https://www.npmjs.com/package/browse), authenticated through vaults. A scheduled deployment periodically validates the catalog to keep it accurate.
* [KERNEL](https://www.kernel.sh/docs/integrations/claude-managed-agents) uses environment variables in vaults to securely connect agents to the databases where it tracks usage and customer conversations. The agent flags usage surges as they happen, so the team can confirm with customers if the activity is intended.[‍](https://getmilana.ai/)
* [Milana](https://getmilana.ai/) uses environment variables in vaults to securely connect its AI product engineer to a customer's codebase. The agent finds and fixes bugs automatically, with large-scale data analysis running faster than before.

![Milana](https://assets.claude.com/df4ef0d4ea1d8d538cba548c2987c958ae613b87.svg)

> “With Claude Managed Agents, we grounded our agent on a customer's actual codebase. We found it easy to work with and got high-quality results almost instantly. The key unlock was environment variables in vaults, which let our agent invoke private APIs through a CLI without exposing credentials. Large-scale data analysis is now dramatically faster, and with outcomes we can ensure the quality of every output.”

Raghav Sethi, Co-founder & CTO

![BrowserBase](https://assets.claude.com/489e95f32195178dcffe6284f2d9135182747045.svg)

> “Environment variables in vaults enabled our engineering team to combine two major compute primitives: the agent and the browser. At Browserbase, we used Claude Managed Agents with the browse CLI to generate our public catalog of browser skills that help agents navigate the web, and scheduled deployments run periodic validation on our public catalog.”

Ziray Hao, Product Lead

![KERNEL](https://assets.claude.com/3380cafbe5974d507544a64329ae6eba4c3d9794.svg)

> “Usage on Kernel's browser infrastructure can surge quickly, often right after a customer deploys. With environment variables in vaults, our agent now connects directly to the databases where we track usage and customer conversations. It pulls 30 days of daily usage in seconds, flags surges as they happen, and helps our team confirm with customers that the activity is intended.”

Catherine Jue, Co-founder & CEO

![Notion](https://assets.claude.com/19e0cdfaef9d2980bddd19cd993076d62b46c0c7.svg)

> “Environment variables in vaults let us securely roll out the Notion CLI, meeting our security team’s strict guidelines by ensuring sensitive API tokens are never handed to agents. The CLI is complementary to MCP tools, enabling file-upload capabilities in Claude Managed Agents.”

Quan Nguyen, Public API Lead

![Rakuten](https://assets.claude.com/5463fa5a44d12868ceec5ae30bfc8c412cafdeae.svg)

> “Teams across Rakuten use scheduled deployments to analyze data in a spreadsheet and produce a report or deck on a weekly or monthly schedule. Our power users put it on production logs and metrics, so a product manager can see the health of their application without creating an analytics dashboard.”

Yusuke Kaji, General Manager of AI for Business

![Ando](https://assets.claude.com/9d0ae4950cad063b171ca1e5a983f38f34493562.svg)

> “Most of our users prefer to work with fewer agents rather than many. With scheduled deployments, they can bundle more capabilities into one autonomous agent. For example, an agent can watch multiple sales and hiring processes, check in with the right people for updates, and push next steps along.”

Sara Du, Founder

![Actively](https://assets.claude.com/af1bb9358ee0e5aac7291ad82c0287503c9b7b63.svg)

> “We built a cross-account agentic search system on Claude Managed Agents that lets sales teams ask things like which accounts to reach out to today. Since customers want those answers refreshed regularly, we replaced the scheduling infrastructure we'd built ourselves with scheduled deployments, which greatly simplified our stack and improved our product cycles.”

Mihir Garimella, Co-founder

![Milana](https://assets.claude.com/df4ef0d4ea1d8d538cba548c2987c958ae613b87.svg)

> “With Claude Managed Agents, we grounded our agent on a customer's actual codebase. We found it easy to work with and got high-quality results almost instantly. The key unlock was environment variables in vaults, which let our agent invoke private APIs through a CLI without exposing credentials. Large-scale data analysis is now dramatically faster, and with outcomes we can ensure the quality of every output.”

Raghav Sethi, Co-founder & CTO

![BrowserBase](https://assets.claude.com/489e95f32195178dcffe6284f2d9135182747045.svg)

> “Environment variables in vaults enabled our engineering team to combine two major compute primitives: the agent and the browser. At Browserbase, we used Claude Managed Agents with the browse CLI to generate our public catalog of browser skills that help agents navigate the web, and scheduled deployments run periodic validation on our public catalog.”

Ziray Hao, Product Lead

![KERNEL](https://assets.claude.com/3380cafbe5974d507544a64329ae6eba4c3d9794.svg)

> “Usage on Kernel's browser infrastructure can surge quickly, often right after a customer deploys. With environment variables in vaults, our agent now connects directly to the databases where we track usage and customer conversations. It pulls 30 days of daily usage in seconds, flags surges as they happen, and helps our team confirm with customers that the activity is intended.”

Catherine Jue, Co-founder & CEO

![Notion](https://assets.claude.com/19e0cdfaef9d2980bddd19cd993076d62b46c0c7.svg)

> “Environment variables in vaults let us securely roll out the Notion CLI, meeting our security team’s strict guidelines by ensuring sensitive API tokens are never handed to agents. The CLI is complementary to MCP tools, enabling file-upload capabilities in Claude Managed Agents.”

Quan Nguyen, Public API Lead

![Rakuten](https://assets.claude.com/5463fa5a44d12868ceec5ae30bfc8c412cafdeae.svg)

> “Teams across Rakuten use scheduled deployments to analyze data in a spreadsheet and produce a report or deck on a weekly or monthly schedule. Our power users put it on production logs and metrics, so a product manager can see the health of their application without creating an analytics dashboard.”

Yusuke Kaji, General Manager of AI for Business

![Ando](https://assets.claude.com/9d0ae4950cad063b171ca1e5a983f38f34493562.svg)

> “Most of our users prefer to work with fewer agents rather than many. With scheduled deployments, they can bundle more capabilities into one autonomous agent. For example, an agent can watch multiple sales and hiring processes, check in with the right people for updates, and push next steps along.”

Sara Du, Founder

1/7

## **Getting started**

Explore our [documentation](https://platform.claude.com/docs/en/managed-agents/overview) to learn more or visit the [Claude Console](https://platform.claude.com/) to deploy your first agent.

## Related articles

Explore more product news and best practices for teams building with Claude.

[ArticleNov 12, 2026

### Operate Claude Managed Agents inside your security perimeter

Introducing self-hosted Claude Managed Agents. Now you can run agents in your own environment, whether that’s in your own cloud or on-premise. You host the agents, credentials, and session history, and choose where requests to Claude are sent.

Claude PlatformClaude Managed Agents](/resources/articles/self-hosted-claude-managed-agents)[ArticleNov 12, 2026

### Introducing Claude for Manufacturing

A new plugin with 17 skills and four connectors helps manufacturers draft quotes, quality reports, and supplier requests from the systems they already run.](/resources/articles/claude-for-manufacturing)[ArticleNov 12, 2026

### Introducing Claude Meetings

Add Claude to your video call and get the work started while you talk](/resources/articles/claude-meetings)[ArticleNov 10, 2026

### Your apps can now open in Claude, and Claude can work in them

Our partners can now embed their apps directly in Claude, so you and Claude can work in the same tool, on the same screen, without switching tabs.

Claude appsMCP](/resources/articles/interactive-connectors-full-tool)
