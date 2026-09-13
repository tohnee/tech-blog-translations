---
title: "Our vision for building a universal AI assistant"
source: https://blog.google/innovation-and-ai/models-and-research/google-deepmind/gemini-universal-ai-assistant/
site: google-blog
date: 2025-05-20
authors: Demis Hassabis
crawled: 2026-09-13
---

Over the last decade, we’ve laid a lot of the foundations for the modern AI era, from pioneering the [Transformer](https://research.google/blog/transformer-a-novel-neural-network-architecture-for-language-understanding/) architecture on which all large language models are based, to developing agent systems that can learn and plan like [AlphaGo](https://deepmind.google/research/breakthroughs/alphago/) and [AlphaZero](https://deepmind.google/research/breakthroughs/alphazero-and-muzero/?_gl=1*1pz0hjt*_up*MQ..*_ga*MTU3NjU3MjE3OC4xNzQ3MzA4NjIy*_ga_LS8HVHCNQ0*czE3NDczMDg2MjEkbzEkZzAkdDE3NDczMDkwMTIkajAkbDAkaDA.).

We’ve applied these techniques to make breakthroughs in [quantum computing](https://blog.google/technology/google-deepmind/alphaqubit-quantum-error-correction/), [mathematics](https://deepmind.google/discover/blog/ai-solves-imo-problems-at-silver-medal-level/?_gl=1*1bl3hx2*_up*MQ..*_ga*MTU3NjU3MjE3OC4xNzQ3MzA4NjIy*_ga_LS8HVHCNQ0*czE3NDczMDg2MjEkbzEkZzAkdDE3NDczMDkzMzYkajAkbDAkaDA.), [life sciences](https://deepmind.google/discover/blog/alphaproteo-generates-novel-proteins-for-biology-and-health-research/?_gl=1*1dmnab3*_up*MQ..*_ga*MTU3NjU3MjE3OC4xNzQ3MzA4NjIy*_ga_LS8HVHCNQ0*czE3NDczMDg2MjEkbzEkZzAkdDE3NDczMDk0NjEkajAkbDAkaDA.) and [algorithmic discovery](https://deepmind.google/discover/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/?_gl=1*16es8jk*_up*MQ..*_ga*MTU3NjU3MjE3OC4xNzQ3MzA4NjIy*_ga_LS8HVHCNQ0*czE3NDczMDg2MjEkbzEkZzAkdDE3NDczMDkzMzQkajAkbDAkaDA.). And we continue to double down on the breadth and depth of our fundamental research, working to invent the next big breakthroughs necessary for artificial general intelligence (AGI).

This is why we’re working to extend our best multimodal foundation model, Gemini 2.5 Pro, to become a “world model” that can make plans and imagine new experiences by understanding and simulating aspects of the world, just as the brain does.

We’ve been taking strides in this direction for a while, from our pioneering work training agents to master complex games like [Go](https://deepmind.google/research/breakthroughs/alphago/) and [StarCraft](https://deepmind.google/discover/blog/alphastar-mastering-the-real-time-strategy-game-starcraft-ii/), to building [Genie 2](https://deepmind.google/discover/blog/genie-2-a-large-scale-foundation-world-model/), which is capable of generating 3D simulated environments that you can interact with, from a single image prompt.

Already, we can see evidence of these capabilities emerging in Gemini’s ability to use world knowledge and reasoning to represent and [simulate natural environments](https://www.youtube.com/watch?v=zvouDoWL6fk), [Veo](https://deepmind.google/technologies/veo/veo-2/?_gl=1*69oxzg*_up*MQ..*_ga*MTU3NjU3MjE3OC4xNzQ3MzA4NjIy*_ga_LS8HVHCNQ0*czE3NDczMTg1MzMkbzMkZzAkdDE3NDczMTg1MzMkajAkbDAkaDA.)’s deep understanding of intuitive physics, and the way [Gemini Robotics](https://deepmind.google/technologies/gemini-robotics/?_gl=1*6jv8a4*_up*MQ..*_ga*MTU3NjU3MjE3OC4xNzQ3MzA4NjIy*_ga_LS8HVHCNQ0*czE3NDczMTg1MzMkbzMkZzAkdDE3NDczMTg3ODAkajAkbDAkaDA.) teaches robots to grasp, follow instructions and adjust on the fly.

Making Gemini a world model is a critical step in developing a new, more general and more useful kind of AI — a universal AI assistant. This is an AI that’s intelligent, understands the context you are in, and that can plan and take action on your behalf, across any device.

## Bringing Project Astra’s live capabilities into our products

Our ultimate vision is to transform the [Gemini app](https://blog.google/products/gemini/gemini%E2%80%93app-updates-io-2025) into a universal AI assistant that will perform everyday tasks for us, take care of our mundane admin and surface delightful new recommendations — making us more productive and enriching our lives.

This starts with the capabilities we first explored last year in our research prototype [Project Astra](https://deepmind.google/technologies/project-astra/?_gl=1*1ueecac*_up*MQ..*_ga*MjU3NzU4MzA2LjE3NDU4NTM0ODU.*_ga_LS8HVHCNQ0*MTc0NTg1MzQ4Mi4xLjAuMTc0NTg1MzQ4OS4wLjAuMA..), such as video understanding, screen sharing and memory.

Over the past year, we’ve been integrating capabilities like these into [Gemini Live](https://gemini.google/overview/gemini-live/?hl=en) for more people to experience today. We continue to relentlessly improve and explore new innovations at the frontier. For example, we upgraded voice output to be more natural with native audio, we’ve improved memory and added computer control.

We’re now gathering feedback about these capabilities from trusted testers and are working to bring them to [Gemini Live](https://gemini.google/overview/gemini-live/?hl=en), to new experiences in [Search](https://blog.google/products/search/google-search-ai-mode-update/), the [Live API](https://ai.google.dev/gemini-api/docs/live) for developers and new form factors, like glasses.

Through every step of this process, safety and responsibility are central to our work. We recently conducted a large research project, exploring the [ethical issues surrounding advanced AI assistants](https://deepmind.google/discover/blog/the-ethics-of-advanced-ai-assistants/), and this work continues to inform our research, development and deployment.

## Building AI that can multitask for you

We’ve also been exploring how agentic capabilities can help people multitask, with [Project Mariner](https://deepmind.google/project-mariner). This is a research prototype that explores the future of human-agent interaction, starting with browsers.

Since launching Project Mariner [last December](https://blog.google/technology/google-deepmind/google-gemini-ai-update-december-2024/#project-mariner), we’ve been working closely with a group of trusted testers to gather feedback and improve its experimental capabilities.

Project Mariner now includes a system of agents that can complete up to ten different tasks at a time. These agents can help you look up information, make bookings, buy things, do research and more — all at the same time.

The updated Project Mariner is available to [Google AI Ultra](https://blog.google/products-and-platforms/products/google-one/google-ai-ultra/) subscribers in the U.S. We're bringing its computer use capabilities into the [Gemini API](https://ai.google.dev/), and we’re planning to bring more of its capabilities to Google products throughout the year. Read more about our agentic capabilities in [Search](https://blog.google/products/search/google-search-ai-mode-update) and the [Gemini app](https://blog.google/products/gemini/gemini%E2%80%93app-updates-io-2025).

With this, and all our groundbreaking work, we’re building AI that’s more personal, proactive and powerful, enriching our lives, advancing the pace of scientific progress and ushering in a new golden age of discovery and wonder.
