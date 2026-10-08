---
title: "GPT-6 and Intelligent UI for everyone"
date: 2026-10-07
source: https://openai.com/index/gpt-6-for-everyone/
crawled: 2026-10-08
category: research
---

# GPT‑6 and Intelligent UI for everyone

Last month we introduced the first GPT‑6 models for paid customers and today we're bringing that next generation of intelligence to more people with a new GPT‑6 model built for more than 1.2 billion people who use ChatGPT each week.

GPT‑6 in ChatGPT introduces Intelligent UI, a new capability that allows ChatGPT to answer quickly with fully interactive user interfaces that make everyday answers more visual, make learning complex topics easier and that can quickly create a tool to solve a task right in the moment.

### 7‑Speed Bicycle

### 7‑Speed Bicycle

### 7‑Speed Bicycle

### 7‑Speed Bicycle

## Introducing Intelligent UI

We’ve trained GPT‑6 to compose responses using text, visuals and interactive elements, choosing how they fit together based on your question. With Intelligent UI, responses can include graphics, tappable buttons, forms, charts, and interactive experiences you can use directly in your conversation.

The format depends on what you’re asking. A comparison might work best side by side. An explanation might be easier to understand through an interactive diagram. And when a simple text answer is the most useful response, ChatGPT can give you that.

### More visual responses to everyday questions

ChatGPT can make a plan easier to follow by showing how it fits together. The timing for a Sunday roast can sit alongside the recipe, or the stops on a road trip can appear on a map, with notes on what’s worth a detour.

### Learn complex topics more easily

Visual and interactive explanations let you explore how something works, change an input to see what happens, or work through a problem step by step.

### Create interactive experiences just by asking

You can also ask ChatGPT to create a tool for the task at hand, such as a calculator to explore how savings could grow, a bill splitter for dinner with friends, or a game you can play in the conversation.

## How Intelligent UI works

With Intelligent UI, we gave GPT‑6 the freedom to create the most useful interface for each question, while keeping the experience fast and familiar across web and mobile.

We built a library of native, streamable components, along with a compiler that processes the interface as the model generates it. The library gives each response a familiar design foundation while leaving the model room to decide how the pieces fit together. The compiler allows the interface to appear progressively as the model generates it, without waiting for the entire response to be complete.

We expanded our training methods to help the model make thoughtful decisions about content, layout, visuals, and interaction. This included evaluating the interfaces it creates for clarity, usefulness, and completeness. GPT‑6 learned to use the component library and make good design decisions, including how to organize information clearly, when to use interactivity, and when a simple text response is enough.

There's still work ahead to improve the model's design judgment and expand what it can create, but Intelligent UI marks a significant shift in how people interact with ChatGPT. Instead of fitting every question into the same conversational format, ChatGPT can combine UI, data, and actions to create entirely new ways for people to explore, understand, and interact with information.

## Frontier Intelligence – delivered more quickly

With GPT‑6, we’re also making it possible for ChatGPT to begin answering while it continues to think.

**GPT‑5.6 Instant**

**GPT‑6 Instant**

With the introduction of reasoning models, users could get help with much harder problems, but had to wait for the model to finish thinking before getting an answer. Now, ChatGPT can interleave thinking with answering. We trained it to take into account the user’s waiting time and progressively compose an answer using its knowledge and findings up to that point. It learned to build answers across multiple partial responses, each adding useful information without unnecessary filler, while keeping the full answer as cohesive and factual as one written all at once.

In an internal evaluation of high-value, everyday agentic tasks, GPT‑6 Extra High is able to begin answering in the same amount of time as GPT‑5.6 Medium while achieving a better overall score than GPT‑5.6 Extra High.

For questions that need web search, GPT‑6 Instant starts answering 44% sooner, on average, than GPT‑5.6 Instant.

GPT‑6 also improves the quality of answers that require web search. It makes better decisions about when to look something up and more reliably finds information that supports its answer. In an internal evaluation of difficult problems, GPT‑6 correctly addressed the key aspect of the user’s question more often than GPT‑5.6.

## Deploying GPT‑6 safely

As we bring more intelligent AI to more people, we work to improve how it recognizes real-world risks, how honestly it responds, and how well it respects the limits that people set. GPT‑6 makes progress in each of these areas, building on several of Astra’s safety advances to better resist attempts to bypass its safety training, follow safeguards, and be clearer about what it can and can’t do relative to GPT‑5.6 Sol. We updated its safety training based on lessons from real-world use to strengthen protections against high-risk misuse involving cyberattacks, biological threats, and violence. In adversarial testing, GPT‑6 showed stronger resistance to attempts to bypass its safety training, particularly attacks that adapt across multiple turns. GPT‑6 is also trained to respond safely in higher-risk scenarios while avoiding unnecessary refusals of harmless requests. This includes using conversation history and relevant context to recognize risks that may not be apparent from a single prompt.

We ran alignment evaluations throughout training, assessing honesty and responses to safety restrictions. GPT‑6 is better at recognizing and communicating the limits of its own capabilities, including when it lacks the information or tools needed to answer. More detail on the results and our review is available in the [**system card**⁠(opens in a new window)](https://deploymentsafety.openai.com/gpt-6-october).

## Availability

GPT‑6 with Intelligent UI starts rolling out globally to ChatGPT Plus, Pro, Business and Enterprise tiers today in the Chat tab. Starting tomorrow, the rollout expands to Free and Go tiers. Enterprise availability depends on workplace admin settings.

GPT‑6 in ChatGPT is powered by GPT‑6 Sol for Plus, Pro, Business, and Enterprise tiers, and GPT‑6 Luna for Free and Go tiers. Both are tuned for everyday conversation.

This update applies to the Chat experience in ChatGPT. The models powering Work and Codex are not changing as part of this release.

## What comes next

Our mission is to deliver the benefits of artificial general intelligence safely to all of humanity. GPT‑6 brings our latest advances in intelligence to the more than 1.2 billion people who use ChatGPT every week.

Intelligent UI is a step toward a ChatGPT that can shape an interface around what you’re trying to do.

Over time, we want ChatGPT to create more of the interfaces people need for everyday tasks. You should be able to describe what you want to accomplish and work with an experience built around it.

For decades, people have had to learn how to use software, navigating fixed interfaces designed around particular tasks. We believe the future will be different. Instead of people adapting to software, software will adapt to people.

## Author
