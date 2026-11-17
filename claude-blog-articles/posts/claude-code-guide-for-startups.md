---
title: "The Claude Code guide for startups"
date: 2026-08-20
author: Michael Segner
source: https://claude.com/resources/articles/claude-code-guide-for-startups
crawled: 2026-11-17
---

# The Claude Code guide for startups

How fast-growing startups use Claude Code to ship—five operating principles drawn from interviews with more than a dozen companies.

* Category[Best practices](/resources/best-practices), [Perspectives](/resources/perspectives)
* ProductClaude Code
* AuthorMichael Segner
* DateAugust 20, 2026
* Reading time16 min
* ShareCopy link

Prefer a PDF?

This guide is also available for download — the same five rules, founder insights, and checklist, laid out for reading offline or sharing with your team.

[Download the PDF](https://assets.claude.com/054519a5658ddeee3cf9791eda1a36f4455ad842.pdf)

## AI natives working at the frontier

If you want to take a peek at the future of work, ask startups how they are operating today. So we did.

We spoke with more than a dozen fast-growing startups about how they use agentic coding tools to build products and scale their companies. These startups are changing the rules of who gets to build, what gets scrapped, and how to create a flywheel between how you build and what you build.

And they are shipping like organizations ten times their size.

![ClickHouse](https://assets.claude.com/002d4e2a6b94d0409b6dd64c8e91ac1e1fac0bd8.svg)

30%

more features shipped

![Omni](https://assets.claude.com/ade4bc4e76a4151d0e0ba0e7c78fa7eaf24f39c3.svg)

2–3x

engineering productivity

![Clay](https://assets.claude.com/267a4deeacbde106146d26ffa4ef2b08fbb3cb4f.svg)

100%

of bug triage automated

![Artemis](https://assets.claude.com/4c49849997fa71df9c3086ce4dc48ed96d44abfd.svg)

6,000+

PRs a week

In this guide, we'll dive into the unique deployments of these organizations to learn the rules they follow to ship fast and maintain their competitive advantage.

In doing so we'll also start to glean an answer to the question: what would it look like if an organization built their product development lifecycle with Claude Code from the ground up?

### Featuring founder insights from

* [![Artemis](https://assets.claude.com/4c49849997fa71df9c3086ce4dc48ed96d44abfd.svg)](https://artemissecurity.com/)
* [![Cainex](https://assets.claude.com/f56808d1860fc6dec47de96660f570d6fc9b468f.svg)](https://www.cainex.com/)
* [![Clay](https://assets.claude.com/267a4deeacbde106146d26ffa4ef2b08fbb3cb4f.svg)](https://www.clay.com/)
* [![ClickHouse](https://assets.claude.com/002d4e2a6b94d0409b6dd64c8e91ac1e1fac0bd8.svg)](https://clickhouse.com/)
* [![Commure](https://assets.claude.com/e054a5fc14658f016836f9897a3c9035c0d7b30d.svg)](https://www.commure.com/)
* [![Crosby](https://assets.claude.com/9815d36508ab5cbef0ba2782bc26371f19356894.svg)](https://crosby.ai/)
* [![Emergent](https://assets.claude.com/3ecc6fb3c36328f216239a92947c6a75e5dd54d9.svg)](https://emergent.sh/)
* [![Harvey](https://assets.claude.com/9447073367b83132335cb2c191c36bef275f48e6.svg)](https://www.harvey.ai/)
* [![Heidi](https://assets.claude.com/18cd69d52e1475b87358e17bd02b9f79d5049bc5.svg)](https://www.heidihealth.com/)
* [![Higgsfield](https://assets.claude.com/bf441d6847e786ea78a00e4361f0478a2ee260e7.svg)](https://higgsfield.ai/)
* [![Omni](https://assets.claude.com/ade4bc4e76a4151d0e0ba0e7c78fa7eaf24f39c3.svg)](https://omni.co/)
* [![Parahelp](https://assets.claude.com/8d2694cc4ea70bbae09ecf919b6b7fc81ec50df7.svg)](https://www.parahelp.com/)
* [![Translucent](https://assets.claude.com/414fb7868ededc0a2f895e1583fdff9578381784.svg)](https://www.translucent.co/)
* [![Zingage](https://assets.claude.com/7a6b9b092d1ec61d938402cc6744e4d94ed2564a.svg)](https://zingage.com/)

Tip

Only interested in the practical next steps? We've put a [checklist at the end of this guide](#checklist) that consolidates the key technical tips contained in each chapter.

## 01 Everyone ships

Agentic coding lowers the barrier to entry, so the person who understands the problem can ship the first version of the fix.

Agentic coding lowers the barrier to entry for non-technical employees to build products. With Claude Code, you can create functional features without being fluent in a coding language or how to use an IDE.

![](https://assets.claude.com/777148b01c9c3f7be3cf75bf029bf0a1daf0876b.jpg?w=168&q=75&fm=webp&fit=max)
> "Not only were engineers shipping much more, but non-technical people (like me) were also suddenly shipping UI changes and other product improvements."

[Mads Lunau Liechti](https://www.linkedin.com/in/mads-lunau-liechti/), co-founder, [Parahelp](https://www.parahelp.com/)

For startup founders this has obvious advantages. For one, they don't have the headcount of their larger competitors so it's "all hands on deck." But it's not just raw capacity that founders are after–these non-technical members of the team bring domain expertise as well.

![](https://assets.claude.com/e03dea8351fda949e3c950e1f42c4e79bb65c21c.jpg?w=168&q=75&fm=webp&fit=max)
> "Claude Code changed what it meant to be a lawyer at Crosby. The lawyers have the best product insights, because they are the users. It's been amazing to watch them cook."

[Ryan Daniels](https://www.linkedin.com/in/crosbyryan/), co-founder and CEO, [Crosby](https://crosby.ai/)

We heard the same thing from Dr. Thomas Kelly, co-founder and CEO of Heidi.

![](https://assets.claude.com/10bc73da91563f63ea78792df45b4c23b83aec0d.jpg?w=168&q=75&fm=webp&fit=max)
> "For us, Claude Code solved the broken telephone problem. The way a new idea used to move through a team was the person with the idea tells a PM, who tells a designer, who then tells an engineer… and inevitably the essence of the idea gets lost in that chain. By the time something shipped, it often didn't resemble what the person had in mind. And it took weeks. Claude Code collapses that chain. The person who actually understands the problem can ship a PR bringing in designers and engineers for the parts where their expertise matters."

[Dr. Thomas Kelly](https://www.linkedin.com/in/tomkeykong/), co-founder and CEO, [Heidi](https://www.heidihealth.com/)

Saying "everyone ships" makes for a great LinkedIn post, but how does that work in reality? Is the marketing team approving pull requests? Is the legal team working through the intricacies of bisecting flaky tests?

The answer we got is that there is still a division of labor. Marketers still focus on marketing and developers still focus on developing. But the all important first step of getting an idea to working prototype, of going from 0 to 1, is open to everyone.

We also saw the most effective startups create mechanisms to make these contributions systemic rather than leaving it to chance or individual ambition.

### Create connections

It's one thing to create expectations for employees to use AI, it's another to give them access to Claude Code and the tools they need.

![](https://assets.claude.com/f7c8dc8ab99a4876f637ab9d4a56c05db52bc8d7.jpg?w=168&q=75&fm=webp&fit=max)
> "We're actually not running away from [having non-technical employees contribute], we're going towards it. Our take is every role is becoming an engineering role because you can build software for it… so we hire people who are tinkerers, who are interested in building"

[Kareem Amin](https://www.linkedin.com/in/kareemamin/), co-founder and CEO, [Clay](https://www.clay.com/)

At Crosby, the team didn't bring lawyers to Claude Code, they brought Claude Code to the lawyers by connecting it to the tools and operating systems they were familiar with and worked in every day.

Tip

Claude can't understand what it can't see. One of the most effective ways to extend Claude's value is to connect it to sources of truth and the tools your team uses every day.

[MCP](https://code.claude.com/docs/en/mcp) is an open source standard for AI-tool integrations that give Claude Code access to your tools, databases, and APIs. Explore adding these connections whenever your team finds itself copying and pasting information from a tool into Claude.

Connecting via CLI can be more token-efficient when a mature command-line tool already exists (`gh`, `kubectl`, `bq`, `psql`) and you want Claude working against the same ground truth your engineers do.

![](https://assets.claude.com/e0d8cf3d206d25734edd01413cc3516d4d66e38c.png)

MCP Connector Directory in Claude Code desktop.

### Standup showcases

At some point, ideas need to be given the opportunity to be prioritized so that organizational resources can help bring them to market. That road is clear for product managers—it's their job after all—but not as clear for non-technical employees.

Clay creates quarterly reviews where prototypes are considered and can enter the formal roadmap. This is how a go-to-market team member at Clay built an autonomous agent that visits your websites, fills out your lead-capture forms, times how long it takes to respond, rates the experience, and generates a performance report.

Omni has a dedicated Slack channel for Claude generated prototypes with contributions from everyone including senior technical staff. They also practice the corollary of "everyone ships," which is "everyone talks with customers."

![](https://assets.claude.com/fee2f7e667afc975c0a300f48a1f5c6a6e9986a8.jpg?w=168&q=75&fm=webp&fit=max)
> Even though engineers don't naturally gravitate toward customer calls, Omni deliberately puts them in front of customers because it closes the feedback loop faster.

[Chris Merrick](https://www.linkedin.com/in/merrickchristopher/), co-founder and CTO, [Omni](https://omni.co/)

### Share skills

The line between "everyone ships" and "piecemeal" can be a thin one. Feature prototypes, whoever they come from, still need to be integrated into a product that feels like a cohesive whole. This is where skills, reusable instruction files that encode your team's standards and context, can help ensure development stays aligned even as the process becomes increasingly democratized.

"Anyone on the team can draft product components, marketing collateral or deck material from Claude Code using our design system as reference. AI that touches the product must clear a much higher bar, which Claude Code helps us meet with more precision," said Dr. Thomas Kelly, Heidi.

They can also get new developers and non-technical employees onboarded and up and running quickly.

![](https://assets.claude.com/0eb2fe5da7332af61215ca4ae5320f375ef72928.png?w=168&q=75&fm=webp&fit=max)
> "...we also have a GitHub repo of Claude Code skills which works as a shared knowledge base to quickly bootstrap a Claude Code session with known Emergent details like database [and data warehouse] location, some schema [information], overall company context….instead of trying to be perfect here, it is ok to live with slightly outdated context files as long as the agent can quickly verify and course correct."

[Mukund Jha](https://www.linkedin.com/in/mukund-jha-a1596413/), co-founder and CEO, [Emergent](https://emergent.sh/)

![](https://assets.claude.com/7e5acf1e961c4204e46a47a0bd19450fe9f0e58e.jpg?w=168&q=75&fm=webp&fit=max)
> "Our engineers use Claude Code to spin up an in-house marketplace of specialized internal agents, organized by role, so engineering, delivery, and sales each get tools built for how they actually work."

[Jack O'Hara](https://www.linkedin.com/in/jack-o-hara-/), founder and CEO, [Translucent](https://www.translucent.co/)

Tip

Skills [can be shared across the company using a directory](https://code.claude.com/docs/en/plugin-marketplaces) so one employee's best practice can be instantly transferred to another. Use `CLAUDE.md` files in each subdirectory of your repo for coding conventions specific to that subdirectory that apply every time. Use skills for on-demand procedural workflows. For more information, read: [Steering Claude Code: when to use CLAUDE.md, skills, hooks, and subagents](/resources/articles/steering-claude-code-skills-hooks-rules-subagents-and-more).

## 02 Automate the tedium

Agents own the mechanical 80% of the lifecycle so engineers spend their time on the cases that actually need judgment.

All companies have sought to gain efficiencies through technology since the dawn of the industrial revolution, but these startups separated themselves by the speed and depth of their adoption.

These founders believe AI is an essential component of their mission. Many are explicit that agents own the mechanical 80% so engineers spend their time on the cases that actually need judgment.

![](https://assets.claude.com/b0484f07fb5d387c4006d3a9cf0614b525a69689.png?w=168&q=75&fm=webp&fit=max)
> "Everyone's racing to build AI products. Far fewer are rebuilding how their company actually runs. The second one is the bigger unlock. Artemis Security runs as an AI-native company, not a company that happens to use AI. This supercharges our velocity and allows us to help customers stop attacks at machine speed."

[Shachar Hirshberg](https://www.linkedin.com/in/shachar-hirshberg/), co-founder and CEO, [Artemis Security](https://artemissecurity.com/)

Specifically, we saw AI more tightly integrated across their SDLC stages than others as well as more purpose built agents designed to take recurring tasks end-to-end. Let's look at a couple examples of both.

### AI-native SDLCs

Many of these featured startups have implemented means of accelerating their teams' onboarding into their agentic coding processes. For example, at Emergent, Mukund told us, "on day one, a new hire bootstraps their entire dev setup by pointing Claude at the right markdown file. If Claude hits anything broken or out of date during onboarding, it updates that file."

Tip

[Code Review](https://code.claude.com/docs/en/code-review) is a managed multi-agent service in Claude Code. It runs an automated review pass on PRs in the repos you enable. You can manually fix the finding and push, or close the loop by commenting `@Claude` on the finding (if you've set up and configured GitHub Actions).

![](https://assets.claude.com/34bded07fcea3eac15f98f353ee808974a44b101.png)

Code Review tags each finding with a severity level.

These engineers need to be onboarded quickly because these teams ship fast.

![](https://assets.claude.com/9a5f813e3ee4e8e2d591259a52dae3505693ee77.png?w=168&q=75&fm=webp&fit=max)
> "Engineers here are orchestrating agent fleets, shipping fixes to production data problems the same day they're found, and running multiple PRs in flight simultaneously. One engineer ran a ~13-ticket initiative with Claude subagents in parallel, each owning a ticket and its PR."

[Tanay Tandon](https://www.linkedin.com/in/tanaytandon/), CEO and founder, [Commure](https://www.commure.com/)

At these organizations, Claude Code not only helps generate code, but reviews it too. "We run automated code reviews against our vetted technical and compliance frameworks, flagging critical issues and routing suggested changes to the right reviewers before anything ships," said Dr. Kelly of Heidi.

Some of these organizations have also built custom agents for code review, testing, and CI. These startups have placed considerable attention on [building loops](https://claude.com/resources/articles/getting-started-with-loops) vs just deploying code.

"My favorite [agent] is the "Translucent code reviewer," which fans out across a change, reviews it from multiple angles, and synthesizes the results the way one of our senior engineers would but faster than any one person could," said Translucent founder Jack.

Clay "...built an agent that handles…bug triage, from first pass to suggesting code changes for fixes," said Kareem.

Tip

For the last several months [Claude Tag](https://claude.com/product/tag) has been the on-call first responder for CI/CD failures at Anthropic. Claude authored the first situation report in every recent incident that had one, typically publishing its first analysis within 15 minutes.

[Claude Tag has its own service account](/resources/articles/agent-identity-access-model) and access to the tools an Anthropic CI engineer needs such as Datadog or Grafana. Standing instructions are in markdown files as skills, committed in a GitHub repository. This way multiple teammates can iterate on them and we can manage changes just like we do code.

![](https://assets.claude.com/f60bcb14cf717c2d43f5ff9ba5eab9861b91d831.png)

Claude Tag picks up an on-call thread in Slack and reports progress in-channel.

![](https://assets.claude.com/f9f778a29e7d934084fa793c629068373feb51c1.jpg?w=168&q=75&fm=webp&fit=max)
> This was most pronounced at [ClickHouse](https://clickhouse.com/), where **co-founder and CTO Alexey Milovidov reported** the database company had turned nearly every SDLC stage into an autonomous loop. Two purpose-built agents designed to fix flaky tests and find missing test coverage are now the #2 and #3 contributors to the ClickHouse repo. A separate family of agents handles operations, and the team uses Claude Code to build and iterate on those agents themselves.

### Accelerating processes with agents

Another consistent pattern was that these startups were not only using agentic loops in Claude Code to accelerate their development efforts, but they were also creating agents to accelerate recurring and often tedious processes.

This was often routine work so that more attention could be focused on their competitive advantage, customer relationships, and on top-line growth. One of the most common processes we saw accelerated by Claude was self-service data analytics.

Nearly every one of these companies had some process in place so they could make quick decisions with fresh data, including unstructured data, that fuels the pivoting so essential in the life of a startup.

For example, Clay built an internal analytics agent and Heidi uses Claude Code to categorize customer and clinician feedback alongside usage data to surface signals that matter for product insights.

Both ClickHouse and Omni ship products that package this type of AI data analysis within them, all powered by Claude.

Other examples include summarizing thousands of legal documents with subagents (Crosby), sweeping claims data to flag anomalies across sites (Commure), and continuously mining hospital financial data for warning signs no analyst team could catch in time (Translucent).

Tip

[Dynamic workflows](https://claude.dev/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code/) can be used to fan multiple subagents to analyze large amounts of data in parallel or to conduct an adversarial review of another agent's work. When using a model like Claude Opus or Claude Fable say "fan out multiple subagents," or "use a workflow."

![](https://assets.claude.com/a6ae82f87e4ab07588d0f70e4c528365080cdb14.png)

## 03 Trust, but verify

You can't automate a process unless you have a reliable means of monitoring and verifying the outcome.

This rule is the necessary corollary to Rule 2: Automate the tedium. You can't automate a process, unless you have a reliable means of monitoring and verifying the outcome.

![](https://assets.claude.com/9696a56eaa29376c23109fc6a50dccf00577519b.jpg?w=168&q=75&fm=webp&fit=max)
> Artemis Security co-founder Dan Shiebler said their increased deployment speed only works…"because we've invested deeply in testing infrastructure, codebase organization, and team knowledge systems that let agents ship end to end. This is the flywheel we've built with Claude: structure your codebase, knowledge base, and team the right way, and every contribution compounds."

[Dan Shiebler](https://www.linkedin.com/in/dan-shiebler-10219b42/), co-founder, [Artemis Security](https://artemissecurity.com/)

![](https://assets.claude.com/56a82bd3edaf8003b57812e5a1b37c6753b7e938.jpg?w=168&q=75&fm=webp&fit=max)
> "Early on we gave Claude full autonomy and it did what AI does. It shipped plausible code fast. The problem was it drifted from our architecture in ways that looked right but weren't. So we…wrote down every invariant. How we frame problems. What has to be true no matter what. How to prove something works instead of trusting a confident answer. 567 lines of how this team thinks."

[Victor Hunt](https://www.linkedin.com/in/victor-c-hunt), co-founder and CEO, [Zingage](https://zingage.com/)

Tip

Put what can't change in `CLAUDE.md` at the root of your repo. Claude reads it at the start of every session, so your architecture rules, security boundaries, and non-negotiables travel with every session.

To be clear, none of these startups are having agents merge to main and hoping for the best. Many of them operate in highly regulated industries and require strong governance frameworks. Cainex is a particularly illustrative example of combining agents with deterministic checks to read medical records and generate codes that direct hospital billing.

![](https://assets.claude.com/6ee9006723da038933b4e3e4a6c6e2fa8b4b2f69.jpg?w=168&q=75&fm=webp&fit=max)
> "In medical coding, a wrong code isn't a typo. It's a billing and compliance event. That one fact governs how we build."

[Uriah Israel](https://www.linkedin.com/in/uriah-israel/), co-founder and CTO, [Cainex](https://www.cainex.com/)

"Here's the loop Claude Code runs for us. We process a batch with an agent, and our auditors review the output in an internal app. They don't just see the codes. They see the model's reasoning, and they comment on both….Everything is versioned and auditable," he said.

"Then Claude Code takes over. It reads the original predictions, along with every correction and comment, straight from the database. Each correction is tagged by the kind of code involved, so Claude Code knows whether it's looking at a diagnosis issue, a procedure issue, or another category, and it can go straight to the guidance that governs that specific kind of coding.

From there, it finds the part of the agent's instructions that produced the mistake and revises it, or writes new guidance when the case is genuinely new. Every change is made against a versioned set of instructions and tested against the records that failed. The rule we enforce: fix the principle, not the example," he continued.

"Then the back-test. A record can have more than one acceptable coding, so it's not a string match. The check combines semantic matching against our accepted sets with a judge that asks, 'Is this a real error or just a different valid path,' and Claude Code adds its own comparisons on top.

It runs the candidate change across a golden set plus random samples and surfaces any regressions before anything ships. What comes back is a short list: suggested edits, the records it couldn't resolve, and the questions it wants answered. Engineers spend their time on genuinely hard cases rather than the mechanical 80%," he said.

There are many generalized takeaways that founders can glean from this healthcare billing specific workflow.

For example, Cainex uses subject matter experts to routinely review and guide Claude's reasoning, and ensure that guidance becomes part of a self-improvement loop. However, those experts aren't there to fix example by example, their guidance is used as part of a self-improvement loop. As Uriah puts it "fix the principle, not the example."

Tip

Loops are agents that repeat cycles of work until a stop condition is met. They can be effective ways to use Claude Code for more autonomous or long-horizon work. [You can use skills to define what criteria the agent needs to meet](/resources/articles/building-verification-loops-in-claude-code-with-skills) (the more clearly defined the better) and have the agent iterate until it reaches its goal.

For example, many organizations create flaky test agents, or loops, because the stop condition is clear and self-contained: the agent can verify its own fix by rerunning the test until it passes.

![](https://assets.claude.com/0c0fab39c03f3bef320d3a017d73ecd8592dd7b6.png)

Loops repeat cycles of work until a stop condition is met.

The other takeaway is the diligence placed on maintaining a strong evaluation "golden set," or group of verified question answer pairs the team uses to verify the agent's accuracy. Every startup should maintain multiple sets of evals for their key use cases, and update them regularly, so they can prevent drift and evaluate future models.

![](https://assets.claude.com/cda18e355fb29a209fbb90b45a6455cb68e4e64a.jpg?w=168&q=75&fm=webp&fit=max)
> "[Claude Code has] also transformed how we manage model velocity. New video and image models arrive constantly. Each requires new skills, evaluations, routing logic, and production testing before deployment. Claude Code has compressed that cycle from days to hours, allowing us to identify issues in production and deploy fixes in the same session….When you're competing against companies with 10x the headcount, that kind of leverage changes everything."

[Alex Mashrabov](https://www.linkedin.com/in/amashrabov), co-founder and CEO, [Higgsfield](https://higgsfield.ai/)

Tip

When teams first start building agents, they can get surprisingly far through a combination of manual testing, dogfooding, and intuition. The breaking point often comes when users report the agent feels worse after changes, and the team is "flying blind" with no way to verify except to guess and check. Teams can't distinguish real regressions from noise, automatically test changes against hundreds of scenarios before shipping, or measure improvements. For more information read: [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents).

The final point Uriah makes is that this process can take some work. "It didn't start this clean. Our first version overfitted. It would 'fix' things by encoding the specific case, and we were accumulating patches instead of getting smarter. We changed the approach to force general principles and to cap how many specifics can enter a change at all."

Tip

AI agents are not deterministic, but a lot of highly regulated work requires processes to be done the same way every time. Claude Code has features that can help combine frontier intelligence with deterministic processes.

[Hooks](https://code.claude.com/docs/en/hooks) are user-defined commands that fire at fixed points in Claude Code's lifecycle and can serve as hard gates. They execute every time regardless of what the model decides. For example they can be used to block a write that fails a lint, require a test pass before commit, or strip secrets before anything leaves the sandbox.

[Dynamic workflows](https://code.claude.com/docs/en/workflows#orchestrate-subagents-at-scale-with-dynamic-workflows) orchestrate subagents with deterministic sequencing, separate context windows, and focused goals. `/goal` is helpful for long complex tasks where Claude may prematurely call the job done, prefer its own findings when reviewing, and drift from its original goals.

## 04 Build for rebuilding

Model capability keeps shifting underneath these teams, so very little is treated as permanent.

Many of these AI-native startups are in a state of constant reinvention.

AI is often at the heart of what they are building as well as how they are building it. Since model capability continuously evolves, groundbreaking features and critical scaffolding were discarded the minute they became sunk costs. Many of these organizations saw this constant rebuilding as part of their competitive advantage.

"What we do at Clay is you build it and then you build it again and then you build it again. And then the fourth time you build it, you know everything that's needed and you get it right. And so we don't necessarily throw away things. We just rebuild it: and this time with more clarity," said Kareem.

"A rebuild isn't done when the new path ships. It's done when the old path is gone. Teardown always lost the prioritization fight before: it's tedious and it ships no features," said Commure co-founder Tanay. "Now one of Commure's engineers just invokes a Claude skill to the tune of 'for every feature flag already released to everyone, open a PR removing it and the associated code,' then the engineer reviews what comes back. Migrations that used to eat a lot of dev cycles are now a plan and a fan out, done in a couple of hours."

Tip

Use [git worktrees](https://code.claude.com/docs/en/worktrees) to run a rebuild in an isolated copy of the repo while the current version stays untouched. Claude Code can spin one up for you — you get v2 running next to v1, run your evals against both, and only merge when the new one wins. This is what makes "build it four times" cheap.

![](https://assets.claude.com/b3a73f9f5fc3c905cb94c25e5c5643a9bf87638d.png)

One repository, one object store — three checkouts you can work in simultaneously, each on its own branch.

Each linked worktree is an ordinary directory with its own checked-out branch; all three share the single .git object store inside acme-web.

Kareem also described part of Clay's moat as the ability to constantly rebuild, evolve, and create self-improvement loops.

"I think the moat for any company right now is that it needs to be self-improving. So Clay is a self-learning revenue engine. So the more you use this, the more we know who your best customers are, what should you say, what's worked, what hasn't and that's changing over time," he said. "The race is really, whoever can get to the distribution fastest… so you can help each [customer] so that you can self-improve."

At a [May 2026 Code with Claude event](https://www.youtube.com/live/OFDm3T7pVlc?si=Z_RENcJSqm8H79aj), Niko Grupen, Harvey's Head of Applied AI, spoke about how each new wave of model capabilities — emergent reasoning, agentic automation, planning and orchestration — required a full re-architecture of the platform.

![](https://assets.claude.com/75801fece65e4c2852f8dc9a24862591f645bae2.png?w=168&q=75&fm=webp&fit=max)
> "If you asked me six months ago what our architecture looks like, I'd give a fundamentally different answer from what it looks like today. If we hadn't been willing to say 'Hey, we need to scrap this and go agent native' we simply could not have these capabilities in our platform right now."

[Niko Grupen](https://www.linkedin.com/in/nikogrupen), Head of Applied AI, [Harvey](https://www.harvey.ai/)

Tip

For non-trivial rewrites, start Claude Code in [plan mode](https://code.claude.com/docs/en/permission-modes#analyze-before-you-edit-with-plan-mode) (`--plan` or hit Shift+Tab). Claude will explore the codebase and propose the rebuild approach before writing any code — you approve or redirect. It's the cheapest place to catch a rebuild that's about to drift from your architecture.

## 05 Prototype, dogfood, productionize

Building with AI helps these startups create disruptive products with AI — the flywheel at the heart of their process.

Many of these startups have a key flywheel at the heart of their development process. Building with AI helps them create disruptive products with AI.

When developers advance their agentic coding practices, they have a stronger grasp on the model's capabilities and insights into how harness design evolves at the frontier. They can then use this inspiration in their own agents and products.

"We took inspiration from [Anthropic's] file vs embedding approach, which emboldened us to keep things simple in our own product. We avoided a lot of complexity that would have come from a RAG pipeline," said Chris, Omni. "We also saw how Claude Code's harness was enabling users to do things in parallel and adapted some of those concepts into our own UI."

It also helps them stay attuned to their own product performance.

"Because our app builder also uses Anthropic models behind the scenes, if we ever see a behavior on our product… we can quickly debug locally via Claude Code to tell whether it's model behavior or a harness issue. This has tremendously helped improve our triage cycles," said Mukund, Emergent.

The pattern we heard repeatedly was build an internal agent with Claude Code, use internally (dogfood), and depending on the response, promote to a customer facing product often using the Claude API, SDK, or Claude Managed Agents.

"We built our own AI agents [in our product] that teams interact with directly, including an agent in the SQL console and an AI SRE. We use Claude Code to build and iterate on these agents themselves. The tooling that powers our customers' AI experiences is, in part, built with AI," said Alexey, ClickHouse.

## The Checklist

This guide covered a lot of ground. Here are the key tips consolidated on one page:

Chapter 1: Everyone ships

Claude can't understand what it can't see. Connect it to sources of truth and the tools your team uses every day via [MCP](https://code.claude.com/docs/en/mcp) or CLI.

Create a [company plugin marketplace](https://code.claude.com/docs/en/plugin-marketplaces) so one employee's best practice can be instantly transferred to another via a skill. Use CLAUDE.md files in each subdirectory of your repo for coding conventions specific to that subdirectory that apply every time. Use skills for on-demand procedural workflows.

Chapter 2: Automate Tedium

Set up [Code Review](https://code.claude.com/docs/en/code-review) (research preview) on a repo for an automated review pass on PRs.

Make [Claude Tag](https://claude.com/product/tag) (public beta) part of your CI/CD on-call response and bug triage.

[Dynamic workflows](https://code.claude.com/docs/en/workflows#orchestrate-subagents-at-scale-with-dynamic-workflows) can be used to fan multiple subagents to analyze large amounts of data in parallel or to conduct an adversarial review of another agent's work.

Chapter 3: Trust, but verify

Put what can't change in CLAUDE.md at the root of your repo.

Use [loops](https://code.claude.com/docs/en/workflows), agents that repeat cycles of work until a stop condition is met, for more autonomous or long-horizon work.

Establish a process for [creating and maintaining agent evaluations](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents).

[Hooks](https://code.claude.com/docs/en/hooks) are user-defined commands that fire at fixed points in Claude Code's lifecycle and can serve as hard gates. Use these when components of the work need to be deterministic.

Chapter 4: Build for rebuilding

Use [git worktrees](https://code.claude.com/docs/en/worktrees) to run a rebuild in an isolated copy of the repo while the current version stays untouched. This is what makes "build it four times" cheap.

For non-trivial rewrites, start Claude Code in [plan mode](https://code.claude.com/docs/en/permission-modes#analyze-before-you-edit-with-plan-mode) (/plan or hit Shift+Tab). Claude will explore the codebase and propose the rebuild approach before writing any code — you approve or redirect. It's the cheapest place to catch a rebuild that's about to drift from your architecture.

## Startups on the frontier build at the frontier

These insights come from your peers building at the frontier and we hope you found them practical and actionable. The Claude startup community is a constant source of inspiration, best practices, and advice. You can join this community by:

* [Subscribing to the Startup Newsletter and joining the startup program](https://claude.com/programs/startups).
* [Bookmarking upcoming Claude Code webinars](https://academy.claude.com/code/webinars).
* [Attending an event near you](https://luma.com/claudecommunity)
* Contributing on [Reddit](https://www.reddit.com/r/ClaudeAI/) and [Discord](https://discord.com/invite/6PPFFzqPDZ).
* Early-stage companies can also apply to the [Claude for Startups program](https://claude.com/programs/startups) for credits and support. [Read what the program now includes](/resources/articles/were-expanding-the-claude-startups-program-to-help-founders-build)

## Related articles

Explore more product news and best practices for teams building with Claude.

[ArticleNov 13, 2026

### Building always-on agents

Always-on agents run indefinitely, deciding how and when to act across many sessions. This guide walks through their core primitives and how they fit together.

Claude Platform](/resources/articles/building-always-on-agents)[ArticleNov 13, 2026

### The Claude Tag guide for startups

How leading startups use Claude Tag to ship faster and scale operations

Claude Tag](/resources/articles/claude-tag-guide-for-startups)[ArticleNov 10, 2026

### How Curative is building a national provider network with agents on Claude

Curative’s deal-making agent negotiates 2,000+ provider contracts a week.

Claude PlatformClaude Code](/resources/articles/how-curative-is-building-a-national-provider-network-with-agents-on-claude)[ArticleNov 9, 2026

### Safely scaling multi-agent teams with Claude Fable 5.2

How a team of 1,000 agents running an early version of Claude Fable 5.2 reproduced a formal proof of Fermat's Last Theorem with general tools, a shared database, and layered safety controls.

(opens in new tab)](https://claude.dev/blog/safely-scaling-multi-agent-teams-with-fable-5-2/)
