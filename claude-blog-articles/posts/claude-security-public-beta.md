---
title: "Claude Security is now in public beta"
date: 2026-04-30
source: https://claude.com/resources/articles/claude-security-public-beta
crawled: 2026-11-17
---

# Claude Security is now in public beta

Claude Security is now in public beta for Claude Enterprise customers. Scan code for vulnerabilities and generate proposed fixes with Opus 4.7, on the Claude Platform, or through technology and services partners building with Claude.

‍

* Category[Product updates](/resources/product-updates)
* ProductClaude Security
* DateApril 30, 2026
* Reading time6 min
* ShareCopy link

*Editor's note: Mentions of Max in this post from before October 30, 2026 include what are now the Max and Ultra plans.*

Claude Security is now available in public beta to Claude Enterprise customers.

AI cybersecurity capabilities are advancing fast. Today’s models are already highly effective at finding flaws in software code; the next generation will be more capable still, and will be particularly effective at autonomously *exploiting* these flaws. Now is the time for organizations to act to improve their security, preparing for a world in which working software exploits are much easier to discover.

Recently, we made Claude Mythos Preview—which can match or surpass even elite human experts at both finding and exploiting software vulnerabilities—available to a number of partners as part of [Project Glasswing.](https://www.anthropic.com/glasswing)

But our cybersecurity efforts go beyond Glasswing: with Claude Security, a much wider set of organizations can put our most powerful generally-available model, Claude Opus 4.7, to work across their codebases. Opus 4.7 is among the strongest models available for finding and patching software vulnerabilities, and for discovering complex, context-dependent issues that might otherwise be missed.

Claude Security—previously known as Claude Code Security—has already been tested by hundreds of organizations of all sizes in limited research preview, helping teams scan their codebases for vulnerabilities and generate targeted patches. Their feedback has shaped today’s release, which makes Claude Security available to all Enterprise customers. It comes with scheduled and targeted scans, easier integration with audit systems, and improved tracking of triaged findings. No API integration or custom agent build is required: if your organization uses Claude, you can start scanning today.

Opus 4.7’s capabilities are also being brought to cyber defenders through Claude’s integration into software tools that many enterprises already use. Our technology partners, including [CrowdStrike](https://www.crowdstrike.com/en-us/press-releases/crowdstrike-puts-claude-opus-4-7-to-work-across-falcon-platform-project-quiltworks/), Microsoft Security, [Palo Alto Networks](https://www.paloaltonetworks.com/blog/2026/04/ai-driven-defense-anthropics-claude-opus/), [SentinelOne](https://www.sentinelone.com/press/sentinelone-unveils-wayfinder-ai/), [TrendAI](https://newsroom.trendmicro.com/2026-04-30-TrendAI-TM-and-Anthropic-Advance-AI-Powered-Vulnerability-Detection-and-Risk-Mitigation-with-Claude-Opus-4-7), and [Wiz](https://www.wiz.io/blog/red-agent-claude-opus) are embedding Opus 4.7 into their tools; in addition, services partners like Accenture, BCG, Deloitte, Infosys and PwC are now helping organizations deploy Claude-integrated security solutions.

We are entering a pivotal time for cybersecurity. AI is compressing the timeline between vulnerability discovery and exploitation. We believe the right response is to make sure defenders have access to frontier capabilities in the ways most accessible to them, through Claude directly and through our partners.

## **How Claude Security works**

[Claude Security](https://youtu.be/0SgCiUfoYo8) can be accessed directly from the Claude.ai sidebar, or at [claude.ai/security](http://claude.ai/security). To begin, select one of your repositories (or scope to a specific directory or branch), then start a scan.

While scanning, Claude reasons about code much like a security researcher. Rather than finding vulnerabilities by searching for known patterns, Claude seeks to understand how components interact across files and modules, traces data flows, and reads the source code.

Once complete, Claude provides a detailed explanation of each of its findings, including its confidence that the vulnerability is real, how severe it is, its likely impact, and how it can be reproduced. It also generates instructions for a targeted patch, which users can open in Claude Code on the Web to work through the fix in context.

## **What we've learned since our initial preview**

Over the past two months, we’ve refined Claude Security in line with what we learned from its use in production across hundreds of enterprises. Specifically, we’ve seen that:

**Detection quality is paramount.** Teams have told us that high-confidence findings are what really accelerate security work. Claude Security's multi-stage validation pipeline independently examines each finding before it reaches an analyst, which drives down false positives, and Claude attaches a confidence rating to every result. This means that the signal that reaches the team is worth acting on.

**Time from scan to fix is the metric that matters.** Early users pointed to this consistently, with several teams going from scan to applied patch in a single sitting, instead of days of back-and-forth between security and engineering teams.

**Teams want ongoing coverage, not one-off audits.** We've added the option to schedule scans, so teams can set a regular cadence around reviewing and acting on findings.

With this release, we've also added the ability to target a scan at a particular directory within a repository, dismiss findings with documented reasons (so that future reviewers can trust prior triage decisions), export findings as CSV or Markdown for existing tracking and audit systems, and send scan results to Slack, Jira, or other tools via webhooks.

Here, organizations who’ve used Claude Security describe their experience:

![Column logo](https://assets.claude.com/88207d00a1f7ad8c894ef632af39d9b11d1b655a.png)

> “Claude Security grasps the actual business logic behind our code. Our security team can now go from scan to fixes in a few clicks within our trusted tooling.”

Greg Janowiak, Information Security Officer

![Yuno](https://assets.claude.com/1be68cb8bfce1230ce4702dbc8a2ca987e93f243.svg)

> “The scan quality is why we're working to plug Claude Security directly into our vulnerability management program—so real issues reach engineering faster, with less triage overhead in between.”

Chiara La Valle, Head of Security

![Hebbia](https://assets.claude.com/a51bf0be0d5ebeb3530f010c18452357dde28d83.svg)

> “Given the increasing pace of vulnerability discovery, the strongest signal for us is how quickly a finding turns into a PR we can actually merge, not a ticket. We've used patches built with Claude Security to close real vulnerabilities in minutes, not days.”

Matt Aromatorio, Head of Security

![Doordash](https://assets.claude.com/23e9f66a28975a13266abe3f53567c17a5bdb888.svg)

> “We are adapting our proactive security efforts through our Anthropic partnership. Claude Security helps us accelerate how we generate and secure new code at the scale and speed of DoorDash— it surfaces deep vulnerabilities accurately, and pipes findings right into our workflows so engineers can act on them in context.”

Suha Can, Vice President and Chief Security Officer

![Snowflake](https://assets.claude.com/5137db8e735ff610a994507050d0a0cea7ce6fd0.svg)

> “Claude Security surfaced novel, high-quality findings during our early testing of the research preview that helped us identify and address potential security issues before they could affect our environment or our customers. We see strong potential as we expand its use.”

Krzysztof Katowicz-Kowalewski, Staff Product Security Engineer

![Column logo](https://assets.claude.com/88207d00a1f7ad8c894ef632af39d9b11d1b655a.png)

> “Claude Security grasps the actual business logic behind our code. Our security team can now go from scan to fixes in a few clicks within our trusted tooling.”

Greg Janowiak, Information Security Officer

![Yuno](https://assets.claude.com/1be68cb8bfce1230ce4702dbc8a2ca987e93f243.svg)

> “The scan quality is why we're working to plug Claude Security directly into our vulnerability management program—so real issues reach engineering faster, with less triage overhead in between.”

Chiara La Valle, Head of Security

![Hebbia](https://assets.claude.com/a51bf0be0d5ebeb3530f010c18452357dde28d83.svg)

> “Given the increasing pace of vulnerability discovery, the strongest signal for us is how quickly a finding turns into a PR we can actually merge, not a ticket. We've used patches built with Claude Security to close real vulnerabilities in minutes, not days.”

Matt Aromatorio, Head of Security

![Doordash](https://assets.claude.com/23e9f66a28975a13266abe3f53567c17a5bdb888.svg)

> “We are adapting our proactive security efforts through our Anthropic partnership. Claude Security helps us accelerate how we generate and secure new code at the scale and speed of DoorDash— it surfaces deep vulnerabilities accurately, and pipes findings right into our workflows so engineers can act on them in context.”

Suha Can, Vice President and Chief Security Officer

![Snowflake](https://assets.claude.com/5137db8e735ff610a994507050d0a0cea7ce6fd0.svg)

> “Claude Security surfaced novel, high-quality findings during our early testing of the research preview that helped us identify and address potential security issues before they could affect our environment or our customers. We see strong potential as we expand its use.”

Krzysztof Katowicz-Kowalewski, Staff Product Security Engineer

![Column logo](https://assets.claude.com/88207d00a1f7ad8c894ef632af39d9b11d1b655a.png)

> “Claude Security grasps the actual business logic behind our code. Our security team can now go from scan to fixes in a few clicks within our trusted tooling.”

Greg Janowiak, Information Security Officer

1/5

We're still in the early days of AI-powered security. As our models improve and as we learn from the teams using Claude Security in production, we'll continue to expand what these tools can do.

## **Meeting defenders where they work**

Claude Security is one part of our broader push to put frontier capabilities in defenders' hands. Much of its reach comes through the platforms and services partners teams rely on today.

[CrowdStrike](https://www.crowdstrike.com/en-us/press-releases/crowdstrike-puts-claude-opus-4-7-to-work-across-falcon-platform-project-quiltworks/), Microsoft Security, [Palo Alto Networks](https://www.paloaltonetworks.com/blog/2026/04/ai-driven-defense-anthropics-claude-opus/), [SentinelOne](https://www.sentinelone.com/press/sentinelone-unveils-wayfinder-ai/), [TrendAI](https://newsroom.trendmicro.com/2026-04-30-TrendAI-TM-and-Anthropic-Advance-AI-Powered-Vulnerability-Detection-and-Risk-Mitigation-with-Claude-Opus-4-7), and [Wiz](https://www.wiz.io/blog/red-agent-claude-opus) are integrating Opus 4.7’s capabilities into the security platforms that enterprises already run on today.  
  
Accenture, BCG, Deloitte, Infosys, and PwC are working alongside enterprise security organizations to deploy Claude-integrated security solutions for vulnerability management, secure code review, and incident response programs.

Together, this means organizations can adopt these capabilities through whichever path fits how they already operate: directly in Claude Security, embedded in a platform they trust, or with a services team guiding the rollout.

![](https://assets.claude.com/c1b1e2638fb40873dea79f8d6c747d49a8b9262c.png)

## **Getting started**

Claude Security is available in public beta starting today for Claude Enterprise customers. Access for Claude Team and Max customers is coming soon.

Admins can enable Claude Security in the [admin console](http://claude.ai/admin-settings/claude-code). For a full walkthrough, see our [Getting Started Guide](https://claude.com/resources/tutorials/getting-started-with-claude-security).

¹Claude Opus 4.7 uses new cyber safeguards that automatically detect and block requests that are suggestive of prohibited or high-risk cybersecurity uses. However, organizations conducting work that may trigger these safeguards can become a part of our [Cyber Verification Program](https://support.claude.com/en/articles/14604842-real-time-cyber-safeguards-on-claude), which is part of our effort to make frontier capabilities available to defenders while keeping them out of the wrong hands.

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
