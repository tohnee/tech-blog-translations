---
title: "Google I/O 2025: From research to reality"
source: https://blog.google/innovation-and-ai/technology/ai/io-2025-keynote/
site: google-blog
date: 2025-05-20
authors: Sundar Pichai
crawled: 2026-09-13
---

*Editor’s note: Below is an edited transcript of Google CEO Sundar Pichai’s remarks at Google I/O 2025, adapted to include more of what was announced on stage. See all the announcements in our* [*collection*](https://blog.google/technology/developers/google-io-2025-collection)*.*

Normally, you wouldn’t have heard much from us in the weeks leading up to I/O, because we’d be saving up our best models for the stage. But in our Gemini era, we’re just as likely to [ship our most intelligent model](https://blog.google/technology/google-deepmind/gemini-model-thinking-updates-march-2025/) on a Tuesday in March, or [announce a really cool breakthrough like AlphaEvolve](https://deepmind.google/discover/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/) a week before.

We want to get our best models into your hands and our products ASAP. And so we’re shipping faster than ever.

![Diagram called "Shipping at a relentless pace" showing a timeline of Google AI development](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/IO25_Shipping.width-1200.format-webp.webp)

## Relentless model progress

I’m particularly excited about the rapid model progress. Elo scores, a measure of progress, are up more than 300 points since our first-generation Gemini Pro model. Today, Gemini 2.5 Pro sweeps the LMArena leaderboard in all categories.

Model progress is enabled by our world-leading infrastructure. Our seventh-generation TPU, [Ironwood](https://blog.google/products/google-cloud/ironwood-tpu-age-of-inference/), is the first designed specifically to power thinking and inferential AI workloads at scale. It delivers 10 times the performance over the previous generation, and packs an incredible 42.5 exaflops compute per pod — just amazing.

Our infrastructure strength, down to the TPU, is what helps us deliver dramatically faster models, even as model prices are coming down significantly. Over and over, we've been able to deliver the best models at the most effective price point. Not only is Google leading the Pareto Frontier, we’ve fundamentally shifted the frontier itself.

![Chart showing the Pareto frontier of low cost AI models](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/0520_ParetoFrontier.width-1200.format-webp.webp)

## The world is adopting AI

More intelligence is available, for everyone, everywhere. And the world is responding, adopting AI faster than ever before. Some important markers of progress:

- This time last year, we were processing 9.7 trillion tokens a month across our products and APIs. Now, we’re processing over 480 trillion — that’s 50 times more.
- Over 7 million developers are building with Gemini, five times more than this time last year, and Gemini usage on Vertex AI is up 40 times.
- The Gemini app now has over 400 million monthly active users. We are seeing strong growth and engagement particularly with the 2.5 series of models. For those using 2.5 Pro in the Gemini app, usage has gone up 45%.

## From research to reality

What all this progress means is that we’re in a new phase of the AI platform shift. Where decades of research are now becoming reality for people, businesses and communities all over the world.

### Project Starline → Google Beam + speech translation

We [debuted Project Starline](https://blog.google/technology/research/project-starline/), our breakthrough 3D video technology, at I/O a few years back. The goal was to create a feeling of being in the same room as someone, even if you were far apart.

We’ve continued to make technical advances. Today we’re ready to introduce the next chapter: [Google Beam](http://blog.google/outreach-initiatives/research/project-starline-google-beam-update), a new AI-first video communications platform. Beam uses a new state-of-the-art video model to transform 2D video streams into a realistic 3D experience, using an array of six cameras and AI to merge video streams together and render you on a 3D lightfield display. It has near perfect head tracking, down to the millimeter, and at 60 frames per second, all in real-time. The result is a much more natural and deeply immersive conversational experience. In collaboration with HP, the first Google Beam devices will be available for early customers later this year.

![Google Beam setup](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/SP_MM_Beam_v91.width-1200.format-webp.webp)

Over the years, we’ve also been creating much more immersive experiences in Google Meet. That includes technology that’s helping people break down language barriers with [speech translation, coming to Google Meet](https://workspace.google.com/blog/product-announcements/new-ways-to-do-your-best-work). In near real time, it can match the speaker’s voice and tone, and even their expressions — bringing us closer to natural and free-flowing conversation across languages. Translation in English and Spanish is rolling out to Google AI Pro and Ultra subscribers in beta, with more languages coming in the next few weeks. This will come to Workspace business customers for early testing this year.

### Project Astra → Gemini Live

Another exciting research project first seen at I/O was [Project Astra](https://blog.google/technology/google-deepmind/google-gemini-ai-update-december-2024/#project-astra), which explores the future capabilities of a universal AI assistant capable of understanding the world around you. [Gemini Live](https://blog.google/technology/google-deepmind/gemini-universal-ai-assistant) now incorporates Project Astra's camera and screen-sharing capabilities. People are using it in interesting ways, from interview preparation to marathon training. This feature is already available to all Android users and rolling out to iOS users starting today.

We’re also bringing capabilities like these to products like [Search](https://blog.google/products/search/google-search-ai-mode-update).

### Project Mariner → Agent Mode

We think of agents as systems that combine the intelligence of advanced AI models with access to tools, so they can take actions on your behalf and under your control.

Our early research prototype, Project Mariner, is an early step forward in agents with computer-use capabilities to interact with the web and get stuff done for you. We released it as an early research prototype in December, and we’ve made a lot of progress since with new multitasking capabilities — and a method called “teach and repeat,” where you can show it a task once and it learns plans for similar tasks in the future. We're bringing Project Mariner’s computer use capabilities to developers via the Gemini API. Trusted testers like Automation Anywhere and UiPath are already starting to build with it, and it will be available more broadly this summer.

Computer use is part of a broader set of tools we’ll need to build for an agent ecosystem to flourish.

Like our open Agent2Agent Protocol, so that agents can talk to each other, or the Model Context Protocol introduced by Anthropic, so agents can access other services. And today, we're excited to announce that our Gemini API and SDK are now compatible with MCP tools.

We’re also starting to bring agentic capabilities to Chrome, Search and in the Gemini app. For example, a new Agent Mode in the [Gemini app](https://blog.google/products/gemini/gemini-app-updates-io-2025) will help you get even more done. If you’re apartment hunting, it will help find listings that match your criteria on websites like Zillow, adjust filters and use MCP to access the listings and even schedule a tour for you. An experimental version of Agent Mode in the Gemini app will be coming soon to subscribers. And it’s great for companies like Zillow, bringing in new customers and improving conversion rates.

This is a new and emerging area, and we’re excited to explore how best to bring the benefits of agents to users and the ecosystem more broadly.

## The power of personalization

The best way we can bring research into reality is to make it really useful — in your own reality. That’s where personalization will be really powerful. We are working to bring this to life with something we call personal context. With your permission, Gemini models can use relevant personal context across your Google apps in a way that is private, transparent and fully under your control.

One example of this is our new [personalized Smart Replies in Gmail](https://workspace.google.com/blog/product-announcements/new-ways-to-do-your-best-work). If your friend emails you for advice about a road trip that you’ve done in the past, Gemini can do the work of searching your past emails and files in Google Drive, such as itineraries you created in Google Docs, to suggest a response with specific details that are on point. It will match your typical greeting and capture your tone, style and even favorite word choices, all to generate a reply that’s more relevant and sounds authentically like you. Personalized Smart Replies will be available for subscribers later this year. And you can imagine how helpful personal context will be across Search, Gemini and more.

## AI Mode in Search

Our Gemini models are helping to make Google Search more intelligent, agentic and personalized.

Since launching last year, AI Overviews have scaled to over 1.5 billion users and are now in 200 countries and territories. As people use AI Overviews, we see they’re happier with their results, and they search more often. In our biggest markets like the U.S. and India, AI Overviews are driving over 10% growth in the types of queries that show them, and this growth increases over time.

It’s one of the most successful launches in Search in the past decade.

For those who want an end-to-end AI Search experience, [we’re introducing an all-new AI Mode](https://blog.google/products/search/google-search-ai-mode-update). It’s a total reimagining of Search. With more advanced reasoning, you can ask AI Mode longer and more complex queries. In fact, early testers have been asking queries that are two to three times the length of traditional searches, and you can go further with follow-up questions. All of this is available as a new tab right in Search.

I’ve been using it a lot, and it’s completely changed how I use Search. And I’m excited to share that AI Mode is coming to everyone in the U.S., starting today. With our latest Gemini models our AI responses are at the quality and accuracy you've come to expect from Search, and are the fastest in the industry. And starting this week, Gemini 2.5, is coming to Search in the U.S., as well.

## Advancing our most intelligent model: Gemini 2.5

Our powerful and most efficient workhorse model, Gemini 2.5 Flash, has been incredibly popular with developers who love its speed and low cost. And the new 2.5 Flash is better in nearly every dimension — improving across key benchmarks for reasoning, multimodality, code and long context. It’s second only to 2.5 Pro on the LMArena leaderboard.

We’re making 2.5 Pro even better by introducing an enhanced reasoning mode we’re calling Deep Think. It uses our latest cutting-edge research in thinking and reasoning, including parallel thinking techniques.

## A more personal, proactive and powerful Gemini app

We're making [Deep Research](https://gemini.google/overview/deep-research/?hl=en) more personal, allowing you to upload your own files and soon connect to Google Drive and Gmail, enhancing its ability to generate custom research reports. We're also integrating it with [Canvas](https://gemini.google/overview/canvas/?hl=en), enabling the creation of dynamic infographics, quizzes and even podcasts in numerous languages with a single click. Beyond this, we're seeing exciting adoption of vibe coding with Canvas, empowering more people to build functional apps simply by chatting with Gemini.

And for Gemini Live, a feature that has truly resonated with users, we're making camera and screen sharing capabilities freely available to everyone, including iOS users, and will soon connect it to your favorite Google apps for [more seamless assistance](https://www.youtube.com/watch?v=GaCKzEBT5mY).

## Advancements in our generative media models

We’re introducing our latest state-of-the-art video model, Veo 3, which now has native audio generation. We’re also introducing Imagen 4, our latest and most capable image generation model. Both are available in the Gemini app — opening up a whole new world for creativity.

We’re bringing those possibilities to filmmakers with a new tool called [Flow](https://blog.google/technology/ai/google-flow-veo-ai-filmmaking-tool/). You can create cinematic clips, and extend a short clip into a longer scene.

## An opportunity to improve lives

The opportunity with AI is truly as big as it gets. And it will be up to this wave of developers, technology builders and problem solvers to make sure its benefits reach as many people as possible. And it’s especially inspiring to think about the research we’re working on today that will become the foundation of tomorrow’s reality, from robotics to quantum, AlphaFold and Waymo.

This opportunity to improve lives is not something I take for granted. And a recent experience brought that home for me. I was in San Francisco with my parents. The first thing they wanted to do was ride in a Waymo, which I’m learning is becoming one of the city’s top tourist attractions. I had taken Waymos before, but my father, who is in his 80s, was totally amazed; I saw the progress in a whole new light.

It was a reminder of the incredible power of technology to inspire, to awe and to move us forward. And I can’t wait to see the amazing things we’ll build together next.
