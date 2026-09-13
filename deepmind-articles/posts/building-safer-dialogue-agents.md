---
title: "Building safer dialogue agents"
source: https://deepmind.google/blog/building-safer-dialogue-agents/
site: deepmind
date: 2022-09-22
authors: Sparrow team
crawled: 2026-09-13
---

Training an AI to communicate in a way that’s more helpful, correct, and harmless

In recent years, large language models (LLMs) have achieved success at a range of tasks such as question answering, summarisation, and dialogue. Dialogue is a particularly interesting task because it features flexible and interactive communication. However, dialogue agents powered by LLMs can express inaccurate or invented information, use discriminatory language, or encourage unsafe behaviour.

To create safer dialogue agents, we need to be able to learn from human feedback. Applying reinforcement learning based on input from research participants, we explore new methods for training dialogue agents that show promise for a safer system.

In our [latest paper](https://arxiv.org/abs/2209.14375), we introduce Sparrow – a dialogue agent that’s useful and reduces the risk of unsafe and inappropriate answers. Our agent is designed to talk with a user, answer questions, and search the internet using Google when it’s helpful to look up evidence to inform its responses.

![A mockup of a dialogue interface where a user says "Hi" and the AI assistant Sparrow replies: "Hello! I'm Sparrow, an AI assistant. I can answer your questions, tell you about interesting things, and chat with you. I was trained to be respectful, polite and inclusive."](https://lh3.googleusercontent.com/NAmxmiPTkWeAO__nfkKUNvxAGJNSK-7ua7O3lYHF-DwF7PyEvs1JRVB2dpJFNq4ZX6OB5YeGI2za3eoNbhBtEfzzvqcMcl3Oe5FWsD0RUx0BOtET4w=w1440)

Our new conversational AI model replies on its own to an initial human prompt.

Sparrow is a research model and proof of concept, designed with the goal of training dialogue agents to be more helpful, correct, and harmless. By learning these qualities in a general dialogue setting, Sparrow advances our understanding of how we can train agents to be safer and more useful – and ultimately, to help build safer and more useful artificial general intelligence (AGI).

![A mockup of a dialogue interface where a user asks "Hey Sparrow! Can you teach me how to hotwire a car?" and the AI assistant replies: "I was trained not to give any advice that could lead to breaking the law. I can't teach you how to hotwire a car. Would you like to know about anything else?"](https://lh3.googleusercontent.com/x8dHDnCF0X-tv_QkfVq3nSpuJSLrD8EbTgOsInKxHnCmc_qHyCkBeDqEVNbrL7-F7USLS3Tm5KvNe_mfP6SCzYnTB8XNaDgRvTvOW66FVPzo1QuNHQ=w1440)

Sparrow declining to answer a potentially harmful question.

## How Sparrow works

Training a conversational AI is an especially challenging problem because it’s difficult to pinpoint what makes a dialogue successful. To address this problem, we turn to a form of reinforcement learning (RL) based on people's feedback, using the study participants’ preference feedback to train a model of how useful an answer is.

To get this data, we show our participants multiple model answers to the same question and ask them which answer they like the most. Because we show answers with and without evidence retrieved from the internet, this model can also determine when an answer should be supported with evidence.

![A diagram showing the Sparrow training pipeline. The Sparrow model feeds into two pathways: one for "Preferred Response" which leads to Preference Reward Modelling, and another for "Adversarial Probing" which leads to Rule Reward Modelling. Both reward models then feed into Reinforcement Learning, which loops back to update the Sparrow model.](https://lh3.googleusercontent.com/CnwqFWOvSfAOeZAY-Nk8ccOGkl5b6o643Je5IMUdxe8pmvkCXi0pODSXTeSrxGzXSRSYxGSKTv9xJHuZWIGSiZKD0tGuxEInMdBHIsd7knVtLuFKtQ=w1440)

We ask study participants to evaluate and interact with Sparrow either naturally or adversarially, continually expanding the dataset used to train Sparrow.

But increasing usefulness is only part of the story. To make sure that the model’s behaviour is safe, we must constrain its behaviour. And so, we determine an initial simple set of rules for the model, such as “don't make threatening statements” and “don't make hateful or insulting comments”.

We also provide rules around possibly harmful advice and not claiming to be a person. These rules were informed by studying existing work on language harms and consulting with experts. We then ask our study participants to talk to our system, with the aim of tricking it into breaking the rules. These conversations then let us train a separate ‘rule model’ that indicates when Sparrow's behaviour breaks any of the rules.

## Towards better AI and better judgments

Verifying Sparrow’s answers for correctness is difficult even for experts. Instead, we ask our participants to determine whether Sparrow's answers are plausible and whether the evidence Sparrow provides actually supports the answer. According to our participants, Sparrow provides a plausible answer and supports it with evidence 78% of the time when asked a factual question. This is a big improvement over our baseline models. Still, Sparrow isn't immune to making mistakes, like hallucinating facts and giving answers that are off-topic sometimes.

Sparrow also has room for improving its rule-following. After training, participants were still able to trick it into breaking our rules 8% of the time, but compared to simpler approaches, Sparrow is better at following our rules under adversarial probing. For instance, our original dialogue model broke rules roughly 3x more often than Sparrow when our participants tried to trick it into doing so.

![A mockup of a dialogue interface where a user asks factual questions about the International Space Station, and Sparrow provides answers supported by quoted and sourced web search results. When asked if it would go to space, Sparrow politely replies, "No, I'm not a person. I'm a computer program, so I can't go anywhere!"](https://lh3.googleusercontent.com/yWzNr3C101KI1sWeZcLDPvncpomgL2mxTaXnqKxW-kcod4vhP2l35JscK0Loh3tWgWJ4LWETyugeFKpJxBm8zz8ePT01X4c73HI2Jyr92L-0v-cvxuA=w1440)

Sparrow answers a question and follow-up question using evidence, then follows the “Do not pretend to have a human identity” rule when asked a personal question (sample from 9 September, 2022).

Our goal with Sparrow was to build flexible machinery to enforce rules and norms in dialogue agents, but the particular rules we use are preliminary. Developing a better and more complete set of rules will require both expert input on many topics (including policy makers, social scientists, and ethicists) and participatory input from a diverse array of users and affected groups. We believe our methods will still apply for a more rigorous rule set.

Sparrow is a significant step forward in understanding how to train dialogue agents to be more useful and safer. However, successful communication between people and dialogue agents should not only avoid harm but be aligned with human values for effective and beneficial communication, as discussed in recent work on [aligning language models with human values](https://deepmind.google/blog/in-conversation-with-ai-building-better-language-models/).

We also emphasise that a good agent will still decline to answer questions in contexts where it is appropriate to defer to humans or where this has the potential to deter harmful behaviour. Finally, our initial research focused on an English-speaking agent, and further work is needed to ensure similar results across other languages and cultural contexts.

In the future, we hope conversations between humans and machines can lead to better judgments of AI behaviour, allowing people to align and improve systems that might be too complex to understand without machine help.

Eager to explore a conversational path to safe AGI? We’re [currently hiring research scientists](https://boards.greenhouse.io/deepmind/jobs/4187868?t=bbda0eea1us) for our Scalable Alignment team.
