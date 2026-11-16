---
title: "Your next sales teammate should be a Grok Bot"
date: 2026-10-27
source: https://x.ai/news/grok-bot-sales
crawled: 2026-11-16
---

[Back to news](/news)Oct 27, 2026

# Your next sales teammate should be a Grok Bot

By Iris Wang, Joe Robertson, Micheal Sihavong, and Palmi Angelova

The SpaceXSI Sales team built Team Bots for prospecting, quoting, and deal review so every rep works from the same up-to-date expertise.

[Download for macOS](https://api2.cursor.sh/updates/download/stable/darwin-arm64/grok-bot-bd824e1890d8b96f)[Contact sales](https://cursor.com/contact-sales?product=grok-bot)

When the SpaceXSI Sales team first adopted [Grok Bot](/bot), individual reps built their own Bots to research accounts, prepare for meetings, and manage their pipelines. This presented an opportunity to bring together the best of what everyone was building and make it available to the whole team.

We began creating Team Bots, each specializing in a role that already exists in our Sales organization. The people who know each job best help build and maintain the Bot, so everyone benefits from their expertise and works from the same up-to-date business knowledge. And as we improve a Bot, everyone who uses it benefits, without having to update their own setup.

We've started with three Team Bots, each responsible for a different part of the deal cycle.

* **Account Intel Bot** helps reps identify prospects, prepare for customer conversations, and keep Salesforce up to date.
* **Quote Bot** generates pricing proposals and prepares order forms using CPQ tools.
* **Deal Bot** helps our Deal Desk team review non-standard terms and approve deals.

Each brings its own expertise to the process, allowing us to delegate larger parts of the deal cycle while keeping people focused on customers and the decisions that need their judgment.

![How the SpaceXSI Sales team uses Team Bots to automate the deal cycle: Account Intel Bot handles account research and follow-up, Quote Bot prepares pricing and order forms, and Deal Bot reviews special terms and approvals](https://media.x.ai/cdn-cgi/image/fit=scale-down,onerror=redirect,f=auto/v1/website/sales-bot-diagram-light-6-b66d2e51.png)

![How the SpaceXSI Sales team uses Team Bots to automate the deal cycle: Account Intel Bot handles account research and follow-up, Quote Bot prepares pricing and order forms, and Deal Bot reviews special terms and approvals](https://media.x.ai/cdn-cgi/image/fit=scale-down,onerror=redirect,f=auto/v1/website/sales-bot-diagram-dark-6-5f6bb3a4.png)

## [How we think about Team Bots](#how-we-think-about-team-bots)

Team Bots are a new way to organize work around superintelligence. They take on defined roles that serve entire teams, which requires careful decisions about what they know, what they can do, and when people need to step in.

Each Team Bot needs to understand the systems it operates and the business rules it follows. We give them this knowledge through shared skills and connections to our internal sources of truth, keeping everyone on the same up-to-date rules. When a process changes or we find a better way to perform a task, we can update the Team Bot once for everyone.

Team Bots also need limits on what they can do. They act with each user's permissions, with additional restrictions on sensitive actions. We've built rate limits to prevent unintended changes at scale and reserved certain actions for specialist Team Bots. A sales rep, for example, cannot use Quote Bot to approve their own discount.

We also set boundaries on when Team Bots can act independently. For now, we require human review whenever we can't clearly define the criteria for a decision, or when a Team Bot prepares customer-facing communications. As we measure the quality of their work and gain confidence in their decisions, we expect to give our Team Bots more responsibility.

## [Account Intel Bot handles sales prep and follow-up](#account-intel-bot-handles-sales-prep-and-follow-up)

Our Account Intel Bot helps sales reps identify promising accounts, prepare for meetings, and manage their pipelines. Every rep has a private conversation with the same Team Bot, which draws on shared company knowledge and works with each rep's permissions.

Our GTM engineering team started by having Grok Bot analyze Salesforce activity logs to identify the most valuable work to automate. That showed us that reps were spending a lot of time updating opportunities after customer calls. We gave Account Intel the tools to make those updates and taught it the business rules for when and how to do so.

Proactivity is another principle we think is important for Team Bots. Account Intel can prepare a briefing based on account history before a customer meeting. Afterward, it can read the Gong transcript, identify and make the necessary Salesforce updates, and draft a follow-up email for the rep to review.

Reps can schedule these workflows to run automatically, so much of the preparation and follow-up happens without a separate request.

![Account Intel Bot summarizing next steps from a customer conversation and updating the Salesforce opportunity and account plan](https://media.x.ai/cdn-cgi/image/fit=scale-down,onerror=redirect,f=auto/v1/website/account-intel-01f2079e.png)

## [Quote Bot generates quotes and order forms](#quote-bot-generates-quotes-and-order-forms)

Once a rep is ready to discuss pricing with a customer, a Team Bot we call Quote Bot takes over.

A rep can ask Quote Bot to prepare several proposals with different products and discounts. Quote Bot inputs the quotes in Salesforce and presents them side by side in the Grok Bot app, so the rep can compare options before choosing one without having to go into the CPQ tool.

Quote Bot also manages the steps required to turn a quote into an order form. It submits quotes for approval, tracks their status, and routes exceptions to Deal Bot (more on this below). Once a quote is approved, Quote Bot can generate the order form in Ironclad, download the executable contract, and draft an email for the rep to send to the customer. The rep can complete much of this process in one conversation, rather than moving between systems and waiting for updates from other teams.

We built Quote Bot to handle this work without giving up control over important decisions. Before changing anything in Salesforce, it shows the rep a preview and asks for confirmation. It also operates with the rep's own permissions, so approvals and exceptions that require Deal Desk authority stay with Deal Desk.

![Quote Bot presenting three side-by-side Salesforce quote options for the same account](https://media.x.ai/cdn-cgi/image/fit=scale-down,onerror=redirect,f=auto/v1/website/grokbot_messagebuilder_wallpaper_2816x1832-e13f59e2.png)

## [Deal Bot reviews non-standard terms and approvals](#deal-bot-reviews-non-standard-terms-and-approvals)

When a quote requires special pricing or non-standard contract terms, Quote Bot hands the work to Deal Bot. This Team Bot supports our Deal Desk team, which reviews exceptions and decides what deal economics and risks the business is willing to accept.

Deal Bot checks requests against our approved policies and contract language, then prepares the changes needed to move the deal forward. It can also monitor and triage Slack requests submitted by reps, route requests to the right cross-functional owner or approver, and check whether Legal has already drafted similar terms.

![Deal Bot and Quote Bot coordinating an order-form revision in Slack after marketing language is removed](https://media.x.ai/cdn-cgi/image/fit=scale-down,onerror=redirect,f=auto/v1/website/slack-deal-2-1-f55e022f.png)

Deal Bot has permissions that sales reps don't, allowing it to make changes to quotes that require Deal Desk authority. For decisions that require human judgment, it prepares a recommendation and asks a Deal Desk specialist to approve it before proceeding. Deal Bot handles much of the routine processing, leaving the Deal Desk team to make the decisions that require commercial expertise and human judgment.

![Deal Bot asking a Deal Desk specialist to approve adding already-cleared legal language to a quote's special terms](https://media.x.ai/cdn-cgi/image/fit=scale-down,onerror=redirect,f=auto/v1/website/slack-dealbot-2-1-6035cfbe.png)

Every Salesforce approval processed by Deal Bot is stamped in the system with the decision, the rationale, and the DRI whom Deal Bot was supporting, to ensure accountability, traceability, and compliance within company policies.

## [Building toward a team of AI coworkers](#building-toward-a-team-of-ai-coworkers)

The three Bots we've described are part of a growing team. We've also built Team Bots like Competitive Intel Bot, which keeps our competitive intelligence current and helps reps prepare for competitive conversations, and Sales Training Bot, which supports employee onboarding and skill development. Across Sales, people are also building and using many more individual Bots for their own work.

We're still early in building out this system. Over time, we expect Team Bots to take on more responsibilities and coordinate more of their work with one another. Our goal is a sales organization where people can focus on customers while specialized Team Bots, built and maintained by the people who know each job best, take ownership of much of the work that supports them.

## Try Grok Bot today

[Download for macOS](https://api2.cursor.sh/updates/download/stable/darwin-arm64/grok-bot-bd824e1890d8b96f)[Contact sales](https://cursor.com/contact-sales?product=grok-bot)
