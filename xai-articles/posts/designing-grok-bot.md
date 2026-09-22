---
title: "Designing Grok Bot for a world of persistent agents"
date: 2026-09-03
source: https://x.ai/news/designing-grok-bot
crawled: 2026-09-22
---

[Back to news](/news)

Sep 3, 2026

# Designing Grok Bot for a world of persistent agents

How we designed Grok Bot for agents that persist beyond a single session — from a chat history to a Bot roster, presence, a computer of the Bot’s own, and work that starts without a prompt.

---

When we started designing Grok Bot, one of the central questions was how the interface should shape the relationship between user and agent. Most AI interfaces are organized around a chat session the user operates. Each session begins with setup, unfolds as the user looks on, and ends when the conversation stops.

We wanted to design for an agent that persists beyond any one session and can carry responsibility on its own. That meant reconsidering some of the basic objects and signals of the interface, including what belongs in the sidebar, how an agent shows progress, and when its work should become visible.

![](/_next/static/media/wallpaper-light-noon.27_hyf9uycov-.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)![](/_next/static/media/wallpaper-dark-night.2tq8j5y-604e-.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

Search

Kenny

7:34 PM

Need your yes on the Friday all-hands deck.

Justin

8 intros drafted — sitting in the CRM till you send.

Luke

7:34 PM

Inbox's at 3. Two need a reply today.

Website launch

11:18 AM

John: checkout's clean on staging, 3 bugs closed.

John

Yesterday

Repro'd the checkout crash. Write-up's in the ticket.

Keith

Acme's wobbling. Drafted a Thursday check-in.

Tyler

9:04 AM

14 receipts in. Still missing your Uber from Tuesday.

Manuel

2:20 PM

Launch post is live. First 200 impressions.

Jenny

Tuesday

3 places in SoMa. The Folsom 2bed is the one.

Chang

10:12 AM

Sourced 3. Skipped one already in your ATS.

Plugins

![](/_next/static/media/user-peng.3rw63gdxpcheg.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

Peng Zheng

Kenny

9:41 AM

Hey, what were the main takeaways from today’s design sync?

The team spent most of the session reviewing the new onboarding flow.

The biggest discussion was around the empty states. Sarah felt the current illustrations don’t match the new brand direction, and most of the room agreed. There was also a long back and forth about whether the progress indicator belongs in the header or the sidebar.

The overall mood was positive though. Most people think the flow is close to ready for a wider review.

Did anyone bring up the Q3 roadmap?

Yes, it came up twice. Marcus said the roadmap review is now expected in the first week of August, and Priya asked whether the onboarding work would land before or after that. No firm dates were settled in the meeting.

Message Kenny

![](/_next/static/media/wallpaper-gray.13vta0mrxymev.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)![](/_next/static/media/wallpaper-dark-night.2tq8j5y-604e-.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)![](/_next/static/media/dock-icons.0cwlcw-73qj01.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

Kenny’s screen

Routines

Morning briefing

Every day at 8:00 AM

Inbox cleanup

Weekdays at 6:00 PM

Weekly team update

Paused

## [Rethinking the primitives](#rethinking-the-primitives)

AI products have accumulated a large vocabulary in a short time. Chats, sessions, models, context windows, memories, system prompts, projects, skills, connectors, agents, tools, sandboxes, permissions, and automations all describe real parts of these systems.

But exposing each one as a separate product concept asks users to understand more than they need to. We started by asking which concepts a person actually needs in order to work with an agent.

We kept coming back to five:

1. **Bots** are persistent agents with their own identity, memory, runtime, and tools.
2. **Chats** are the conversational interface for working with a Bot.
3. **Prompts** give a Bot context or instructions. They can be used once, saved as Skills, or triggered automatically as Routines.
4. **Tools** let Bots access information and take action through software, APIs, connectors, the shell, or computer use.
5. **Artifacts** are the documents, designs, code, data, and other durable outputs that Bots create or modify.

Everything else could remain beneath the interface until the user had a reason to care about it. The next question was which of these five objects should organize the product.

## [From chat history to a Bot roster](#from-chat-history-to-a-bot-roster)

Chats are disposable. We start a conversation to solve a problem. It gets pushed down the sidebar. A week later, we start another one. You rarely go back beyond the most recent five.

That behavior is perfectly reasonable when the unit of interaction is a question. It becomes strange when the thing on the other side of the interaction is supposed to know you, remember previous work, and take responsibility over time.

So the main objects in Grok Bot are Bots, not conversations. A Bot has a name. It has an avatar and a title. It remembers its conversations with you. It has its own computer and tools. When you come back tomorrow, you are coming back to the same Bot.

Project Acme

Draft a follow-up to Acme after Friday’s call

Rewrite the pricing one-pager

What should I ask in the security review?

Build a champion map from my call notes

Practice the demo with hard objections

Compare these three competitor decks for me

Show more

Kenny

7:34 PM

Need your yes on the Friday all-hands deck.

Justin

8 intros drafted — sitting in the CRM till you send.

John

Yesterday

Repro'd the checkout crash. Write-up's in the ticket.

Keith

Acme's wobbling. Drafted a Thursday check-in.

## [Presence as interface](#presence-as-interface)

Once a Bot was something you maintain over time rather than a session you start, the way Bots appear in the product had to answer three questions at once:

1. Who is this?
2. What are they doing?
3. How much do I need to know?

### [Who is this](#who-is-this)

A roster only works if it can be scanned quickly. As the roster grows, we did not want people to have to read every name each time they opened the product. They should be able to recognize a Bot from its avatar almost peripherally.

![](/_next/static/media/initials-1.0yig-qj1joruk.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/initials-2.1txviuzdipoiw.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/initials-3.38z4vaotfsn1v.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/initials-4.01qrbimmhtavw.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/initials-5.3jwzv-u8m85v8.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/initials-6.19sekhuc8jakl.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/emoji-1.3h5blj8bz5-jf.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/emoji-2.39jbp_6rdd-5c.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/emoji-3.28sgvmrs9mln9.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/emoji-4.2avjpk08w6cek.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/emoji-5.01zc07ny7g1nn.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/emoji-6.09640mz61fg7f.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/agentb-1.3r4tz4_d9u_-z.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/agentb-2.3fmjch4q22wof.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/agentb-3.3riz-3zy_f268.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/agentb-4.2--kd8w9v-eaw.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/agentb-5.0d3thxc1-7umo.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/agentb-6.2hz5ggcwjuefo.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/base-1.13x8p2khem12n.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/base-2.0_m9l5xohcj95.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/base-3.35r25_i92f7lp.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/base-4.1p9fcypmuoe49.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/base-5.1fhzuvuy00j0n.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/base-6.3t9tmxu30heol.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/new3d-1.1zc81r05mlxf2.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/new3d-2.27lpziqdwd0j0.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/new3d-3.1u9ugv0y8018y.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/new3d-4.0o6i10hvi0pyz.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/new3d-5.0dfi-x29-s1jo.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/new3d-6.30xsvxdcjr7_i.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/blob-1.179mb5k-55q0s.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/blob-2.0f9k73iqne5ic.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/blob-3.3ccg438vd4bnj.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/blob-4.26votlluxpf3p.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/blob-5.3td20ca0sy08_.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/blob-6.24umj72ldwxsm.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/line-1.2vlri0g4yob5c.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/line-2.0k59bd-g6w77s.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/line-3.00_foixq2-eza.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/line-4.3na4nl1j5at_t.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/line-5.3rjal0p5m-286.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/line-6.2ehf_3xbvejl2.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/s32-1.2utembwuppxxx.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/s32-2.3iy5no1sbn35f.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/s32-3.0e7acsgpg5bqv.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/s32-4.21x56bl2zkenr.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/s32-5.10zlplp724o1m.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/s32-6.26kxeg4kxjnex.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/mix-1.11lta7nrjb9pn.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/mix-2.1tpo6-fp8vgup.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/mix-3.32f6whniadrub.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/mix-4.1pily-uyp88-h.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/mix-5.2sq51vj2aq2dn.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/mix-6.1e2kj0mwyz2mi.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/agenta-1.1iuswpcl3hq8o.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/agenta-2.346vsyk23d7i_.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/agenta-3.20lqy9orb-_2u.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/agenta-4.44r1bdv8r6u-c.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/agenta-5.3at_es63n-ehm.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/agenta-6.3m1estnwuqiu3.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

Bot avatar visual style explorations by Kenny Kuh and Peng Zheng

At the same time, we wanted to keep the avatars consistent enough to read as one system. We studied character systems across illustration, animation, games, and interface design, exploring everything from initials and emojis to pixel art, watercolor, claymorphism, Noritake-style line art, silhouettes, and identicons.

Most approaches solved one side of the problem better than the other. Watercolor and clay gave individual Bots plenty of character but carried too much detail at sidebar scale. Simpler systems sat more naturally in the interface, but often left the Bots looking interchangeable.

The system we landed on keeps the basic construction consistent, using simple shapes and expressive eyes, then introduces distinction through controlled variations and accessories. Each Bot remains recognizable at a glance without appearing to come from a different visual world.

### [What are they doing](#what-are-they-doing)

Once the avatar became the Bot’s identity, it was also the natural place to show state. A Bot may be idle, thinking, working, waiting, blocked, or done. We could have represented each state with a separate indicator, but that would have added another layer of UI for the user to interpret.

Instead, we explored how much of the lifecycle the avatar itself could carry.

At rest, the Bot is calm and slightly curious. When work arrives, it acknowledges the task. As work begins, it kicks into gear. Its motion changes again when it is waiting or needs help, then settles once the work is done. The avatar now shows what the Bot is doing as well as which Bot it is.

IdleWorkingWaitingBlockedThinkingDone

Avatar motion system by Benji Taylor

### [How much do I need to know](#how-much-do-i-need-to-know)

A related design question was how much of the Bot’s execution to show. One approach would have been the standard “three animated dots” but that would have been too little information, making it hard for users to tell whether the Bot was working or stuck.

Searching the web

- Environment ready 387ms
- Edited math.ts +14 −10
- Ran focused tests npm test
- Ran type-check npm run
- Thought briefly
- Searched code “toFixed”
- Read AGENTS.md
- Edited math.test.ts +6 −2
- Ran full suite 212 passed
- Committed fix: clamp NaN

- Environment ready 387ms
- Edited math.ts +14 −10
- Ran focused tests npm test
- Ran type-check npm run
- Thought briefly
- Searched code “toFixed”
- Read AGENTS.md
- Edited math.test.ts +6 −2
- Ran full suite 212 passed
- Committed fix: clamp NaN

We also tried showing a short written description of the Bot’s current action, but once people could see one step, they wanted to see the rest. User research showed us that they were asking for that detail mainly for reassurance that the Bot was still working and on the right track.

In the final design, the avatar’s motion provides the first bit of reassurance by showing that the Bot is active. If someone wants to check what it is doing, they can hover to see its current action.

## [Their computer, not yours](#their-computer-not-yours)

Each Bot has its own computer, which it can use to browse the web, work with files, and run software. This created another interface problem. How visible should that computer be and when should the user be able to control it?

We explored four arrangements:

- **Floating window:** kept the computer easy to reach but covered the conversation.
- **Side by side:** made the work continuously visible and encouraged users to watch it.
- **Modal:** made checking in easy but treated the Bot’s workspace as a temporary interruption.
- **Full screen:** gave the computer plenty of room but displaced the conversation entirely.

![](/_next/static/media/wallpaper-gray.13vta0mrxymev.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/wallpaper-gray.13vta0mrxymev.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/wallpaper-gray.13vta0mrxymev.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/wallpaper-gray.13vta0mrxymev.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

The more prominent we made the computer, the more the product encouraged users to supervise it. We decided it should remain the Bot’s workspace, with the interface providing different levels of access as the user needed them.

The final design has three levels, which allow the user to enter the Bot’s workspace without being drawn into operating it:

- **Status:** the title-bar icon turns purple while the computer is active.
- **Preview:** opening it reveals a pinned side panel where the user can follow the work without leaving the conversation.
- **Takeover:** when the Bot needs help, the user can open the computer full screen, take control, and then hand it back.

![](/_next/static/media/wallpaper-gray.13vta0mrxymev.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/wallpaper-gray.13vta0mrxymev.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

We also designed wallpapers that shift throughout the day, becoming lighter in the morning and darker at night. The detail gives the Bot’s computer its own sense of time and makes it feel separate from the user’s desktop.

![light day](/_next/static/media/wall-strip-1.3gno9o6tamsil.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)![light noon](/_next/static/media/wall-strip-2.06luvae_idfx_.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)![light night](/_next/static/media/wall-strip-3.170lw02z5ufzv.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)![dark day](/_next/static/media/wall-strip-4.31folbdvqalze.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)![dark noon](/_next/static/media/wall-strip-5.099mty7qqe_zp.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

Dynamic wallpaper by Kenny Kuh and Luke Barker.

It is closer to working with a coworker than operating a remote machine. You can tell that they are working, glance at their screen when you need context, and sit down when something requires your help.

## [The shape of information](#the-shape-of-information)

Early versions of Grok Bot responded to almost every request with prose. It described a five-day forecast instead of showing one and narrated a set of tasks instead of laying them out as a board. The user then had to restructure the answer. This led us to treat the form of a response as part of the answer.

To support this, we built inline cards and widgets into Grok Bot. A Bot can answer in prose when prose fits the information and use structured UI when it does not.

New email

Ready to send

Frompeng@grokbot.app

Tosarah@acme.com

SubjectMoving Friday’s design review to 2 PM

Hi Sarah,  
  
Could we move Friday’s design review from 11 AM to 2 PM? A client call came up and I don’t want to rush our discussion.  
  
Thanks,  
Peng

Send emailDiscard

Inline chat widgets by Peng Zheng

The same principle applies to actions. When a Bot creates a Routine, changes a setting, or messages another Bot, the event can appear directly in the transcript. The user can open it when there is more to inspect.

9:41 AM

Morning! Can you check in with everyone for me?

On it — pinging the team for status now

6 messages withKennyTylerandJenny

All on track: Kenny shipped the landing page, Tyler sent this month's invoices, and Jenny booked next week's interviews. No blockers.

Love it, can you do this every morning?

Created RoutineMorning Briefing

Done, your Morning Briefing will be here at 9:00 every day

The result is a heterogeneous transcript in which conversation, system events, interactive objects, and visualizations share one timeline.

## [Organizing intelligence](#organizing-intelligence)

Once people create several Bots, the product also has to organize how those Bots work together. We needed to decide which context should belong to each role, how Bots should share context when their work overlaps, and how to coordinate them without turning the user into a dispatcher.

We saw one answer emerge as people created more Bots. Some made a Chief of Staff Bot responsible for coordinating several specialists. They could give direction to one Bot instead of checking each one and routing every task themselves.

Giving Bots distinct roles also forced us to decide what each role should know. A legal Bot may need the history of an ongoing dispute, while a finance Bot may need years of financial records. Combining those histories into one large memory would make it harder to give each Bot the information relevant to its work.

Capabilities and context therefore follow different boundaries in Grok Bot. Tools and Skills live at the account level because many Bots may need to browse the web, work with documents, or send email. Memory and Routines belong to the Bot because they reflect what that particular role knows and does over time. Put another way, capabilities can be shared broadly while context remains with the role that needs it.

Some work crosses those role boundaries. Group chats provide shared context for a project or team while allowing each Bot to retain its specialized memory. A designer, engineer, PM, and data scientist can work in the same conversation, hand work to one another, and share what the project requires.

We considered adding dashboards, assignment boards, and explicit handoff controls to manage these groups. Each one gave the user more coordination work. Instead, coordinating Bots handle routine routing and bring the user in when a decision requires judgment.

## [Work that keeps moving](#work-that-keeps-moving)

Most agent sessions begin when a user sends a prompt. That leaves even a persistent Bot waiting for someone to activate it. Routines let users give a Bot a standing responsibility that runs on a schedule or in response to an event, such as watching an industry or preparing a briefing every morning. The user defines the work once, and the Routine activates the Bot when it needs to happen.

We initially treated Routines as secondary configuration. As they became more important to autonomous work, we moved them into the Bot’s main interface. The transcript shows what ran and gives the user a place to review the result or handle an exception.

Every day at 8:00 AM

On weekdays at 8:00 AM

Every Monday at 9:00 AM

Monthly on the 1st at 8:00 AM

Every 30 minutes

On weekdays · 9:00 AM

Issue created in grokbot

Issue any event in all projects

Incident triggered on grokbot

Incident any event on grokbot

PR opened in grokbot

PR merged in spacexai

PR closed in acme

New push to main

Checks fail on PRs in grokbot

Label bug added in grokbot

Comment containing /fix in ops

Review approved in grokbot

Thread resolved in grokbot

Workflow deploy.yml fails

When webhook receives a POST

New messages in #grokbot

Reaction :eyes: added in #ops

Channel created matching dev

New messages in #design

Issue created in Roadmap

Issue status → In Review in Core

At end of cycle for Team Core

Issue status → Done in Design

New messages in Design team

Channel created in Design team

This also changes the role of conversation. A prompt can start a session, but so can a schedule, an event, or another Bot. Over time, more work may begin without the user being present at all.

## [The disappearing interface](#the-disappearing-interface)

By the end of the project, much of the design work involved taking things away. We removed window and panel controls, computer-view options, and agent metadata. We also set practical limits of roughly 50 Bots per account and six per group chat. Each decision came back to the same question: Did this help someone delegate, or did it give them one more thing to manage?

The line between operating an AI and delegating to a coworker keeps moving as models improve. Grok Bot reflects where we think it sits today. Designing Grok Bot from its earliest explorations through launch has been about finding that line and helping the interface change with it. As agents take on more responsibility, the interface should ask less of the person.
