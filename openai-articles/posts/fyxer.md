---
title: "How Fyxer built an AI executive assistant people trust"
date: 2026-09-03
source: https://openai.com/index/fyxer/
crawled: 2026-09-18
category: research
---

# How Fyxer built an AI executive assistant people trust

For many professionals, work means keeping track of conversations and commitments across inboxes, meetings, messages, and apps. Without rock-solid context, those commitments can fall through the cracks, damaging projects and relationships.

Fyxer built an AI executive assistant that follows the thread as work moves across tools. It combines the latest OpenAI models with more than 500,000 hours of executive assistant workflows, dividing the work among dozens of specialized models that improve through real user feedback.

Email is one of the clearest places to see it in action. Two people can receive the same email and need completely different replies depending on the relationship, what has happened before, and what each person is trying to get done. That makes a seemingly simple task deceptively hard for AI.

“There’s something called Moravec’s paradox,” explains Fyxer Co-founder Archie Hollingsworth. “Things that humans find easy are hard for computers, and things that computers find easy are hard for humans.” Fyxer handles that complexity by learning how each user works, so it can respond like an assistant who already knows what matters.

Frontier OpenAI models support key parts of the experience, from understanding the email and finding the right context to generating the draft. Fyxer chose OpenAI because its models performed best on Fyxer’s internal benchmarks, offered strong fine-tuning capabilities for subjective tasks like tone and intent, and provided hands-on engineering support through whiteboarding sessions and technical collaboration.

> “We chose OpenAI because they have the best models, and they’ve given us real access and a close working relationship. I can drop a question in Slack and get an answer quickly, and when we face a problem, the team comes to our office and works through it with us. They show up.”

Fyxer’s approach offers three lessons for founders building highly contextual AI products:

## 1. Break email into smaller jobs

Fyxer built its system around 30–50 specialized models, each responsible for a narrow part of the email workflow. Instead of treating email as a single text-generation task, Fyxer breaks the problem into a system of predictions, like deciding whether a message requires a reply or drafting responses that match a user’s tone and context.

“Breaking the problem into many smaller models works much better than asking one model to write a good email,” Hollingsworth explains.

When a new email arrives, a reply decision model classifies the message: is this something that needs a response, a scheduling action, or simply information the user should see?

If a response is needed, additional models analyze the intent of the email and predict the likely outcome of the interaction. These models determine patterns such as whether the conversation is moving toward scheduling a meeting, resolving a request, or continuing a longer relationship thread.

Memory is one of the most important parts of the system. Fyxer needs to decide which details should persist across conversations and which should disappear after a single exchange. When a new email arrives, retrieval models compare it with stored interactions and surface the memories most relevant to that person and thread.

OpenAI models power steps across Fyxer’s system. “We use OpenAI models for everything from digesting the email, so we can understand what it is actually about, to pulling in and re-ranking the context we want to include, to the actual email generation,” Shantsila says.

## 2. Train on how great assistants actually work

Before launching its AI product, Fyxer spent years operating a human-powered executive assistant service. Over time, the team accumulated a dataset built from more than 500,000 hours of annotated executive workflows, capturing how real assistants manage professional communication.

Those examples gave Fyxer training data drawn from the job itself. They captured the small judgments behind a good response: when to answer quickly, when to wait, which earlier conversation matters, and how the same request can call for a different response from one person to another.

Fyxer uses supervised fine-tuning and Low-Rank Adaptation (LoRA) across its broader system to create task-specific model variants while controlling training cost. Early in the product’s development, the team used OpenAI’s fine-tuning platform for tasks that needed high accuracy. More recently, Fyxer worked with OpenAI’s managed fine-tuning team to put a new checkpoint into production.

> “OpenAI has been pivotal for us in helping us transfer the learning that we have about our customer and successfully incorporate it into how the models work.”

Before any model is deployed, Fyxer evaluates it on validation sets built around its own email tasks, including drafting, classification, and prioritization. The team weighs accuracy alongside response time and cost, since the best choice can vary by job.

## 3. Turn user feedback into a self-training loop

Once deployed, Fyxer’s system continues improving through real user feedback. When someone edits a draft before sending it, the difference between the original and final email shows which output they preferred.

Fyxer converts those comparisons into training data using Direct Preference Optimization (DPO). Instead of manually labeling every example, the model learns from pairs of outputs: the original draft and the user-edited version.

Every drafting change then goes through an A/B test. Fyxer ships the new version only when it produces a statistically significant improvement. Its user volume means the team can sometimes reach that threshold within a day.

Today, 53% of Fyxer’s AI-generated drafts are accepted as written. That means the system is correctly predicting intent and tone for a large share of real conversations. In 2025 alone, Fyxer grew from $1 million to $32 million in annual recurring revenue.

For Hollingsworth, the stronger signal is retention. Many Fyxer customers are not deeply technical, and for some, Fyxer is the first AI system they use every day.

> “Everyone talks about ARR, but I think retention is the real flex. Over 90% of our users are still paying at the 90-day mark with us, and still using us every day.”

## From drafts to a proactive assistant

Looking ahead, Fyxer is building a richer understanding of relationships, preferences, and ongoing work threads. Their assistant continues to evolve beyond drafting replies toward a broader AI assistant that can manage more of a user’s communication and coordination workload.

“Our vision is to get our customers doing as much of the work they absolutely love,” Hollingsworth says. “We want to get them to a place where they never have to open their computer and can trust Fyxer to manage all of that.”
