---
title: "Introducing the Gemini 2.5 Computer Use model"
source: https://blog.google/innovation-and-ai/models-and-research/google-deepmind/gemini-computer-use-model/
site: google-blog
date: 2025-10-07
authors: Google DeepMind
crawled: 2026-09-13
---

Earlier this year, we [mentioned](https://www.youtube.com/live/o8NiE3XMPrM?si=9uCZ5JXT0xtGyr1H&t=874) that we're bringing computer use capabilities to developers via the Gemini API. Today, we are releasing the [Gemini 2.5 Computer Use model](http://ai.google.dev/gemini-api/docs/computer-use), our new specialized model built on Gemini 2.5 Pro’s visual understanding and reasoning capabilities that powers agents capable of interacting with user interfaces (UIs). It outperforms leading alternatives on multiple web and mobile control benchmarks, all with lower latency. Developers can access these capabilities via the Gemini API in [Google AI Studio](http://ai.google.dev/gemini-api/docs/computer-use) and [Vertex AI](https://cloud.google.com/vertex-ai/generative-ai/docs/computer-use).

While AI models can interface with software through structured APIs, many digital tasks still require direct interaction with graphical user interfaces, for example, filling and submitting forms. To complete these tasks, agents must navigate web pages and applications just as humans do: by clicking, typing and scrolling. The ability to natively fill out forms, manipulate interactive elements like dropdowns and filters, and operate behind logins is a crucial next step in building powerful, general-purpose agents.

## How it works

The model’s core capabilities are exposed through the new `computer\_use` tool in the Gemini API and should be operated within a loop. Inputs to the tool are the user request, screenshot of the environment, and a history of recent actions. The input can also specify whether to exclude functions from the [full list of supported UI actions](http://ai.google.dev/gemini-api/docs/computer-use#supported-actions) or specify additional custom functions to include.

Gemini 2.5 Computer Use Model flow

![Diagram of AI agent loop: Initial task leads to a screenshot/context, which is sent to the Model, which returns a response to the computer environment to execute an action.](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/CTU-Diagram-RD4-V01.width-1200.format-webp.webp)

The model then analyzes these inputs and generates a response, typically a function call representing one of the UI actions such as clicking or typing. This response may also contain a request for an end user confirmation, which is required for certain actions such as making a purchase. The client-side code then executes the received action.

After the action is executed, a new screenshot of the GUI and the current URL are sent back to the Computer Use model as a function response restarting the loop. This iterative process continues until the task is complete, an error occurs or the interaction is terminated by a safety response or user decision.

The Gemini 2.5 Computer Use model is primarily optimized for web browsers, but also demonstrates strong promise for mobile UI control tasks. It is not yet optimized for desktop OS-level control.

Check out a few demos below to see the model in action (shown here at 3X speed).

**Prompt:** “From <https://tinyurl.com/pet-care-signup>, get all details for any pet with a California residency and add them as a guest in my spa CRM at <https://pet-luxe-spa.web.app/>. Then, set up a follow up visit appointment with the specialist Anima Lavar for October 10th anytime after 8am. The reason for the visit is the same as their requested treatment.”

**Prompt: “**My art club brainstormed tasks ahead of our fair. The board is chaotic and I need your help organizing the tasks into some categories I created. Go to [sticky-note-jam.web.app](http://sticky-note-jam.web.app) and ensure notes are clearly in the right sections. Drag them there if not.”

## How it performs

The Gemini 2.5 Computer Use model demonstrates strong performance on multiple web and mobile control benchmarks. The table below includes results from self-reported numbers, evaluations run by Browserbase and evaluations we ran ourselves. Evaluation details are available in the [Gemini 2.5 Computer Use evaluation info](https://storage.googleapis.com/deepmind-media/gemini/computer_use_eval_additional_info.pdf) and in [Browserbase’s blog post](https://www.browserbase.com/blog/evaluating-browser-agents). Unless otherwise indicated, scores shown are for computer use tools exposed via API.

Gemini 2.5 Computer Use outperforms leading alternatives on multiple benchmarks

![Benchmark performance table: Gemini 2.5 Computer Use leads in Online-Mind2Web, WebVoyager, and AndroidWorld benchmarks.](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/CTU-Benchmark_Chart-RD5_V01.width-1200.format-webp.webp)

The model offers leading quality for browser control at the lowest latency, as measured by performance on the Browserbase harness for Online-Mind2Web.

Gemini 2.5 Computer Use delivers high accuracy while maintaining low latency

![Latency vs. Quality scatterplot: Gemini 2.5 Computer Use is lowest in latency and highest in accuracy (70%+ accuracy, ∼225 sec latency).](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/CTU-Scatterplot-RD7.width-1200.format-webp.webp)

## How we approached safety

We believe that the only way to build agents that will benefit everyone is to be responsible from the start. AI agents that control computers introduce unique risks, including intentional misuse by users, unexpected model behavior, and prompt injections and scams in the web environment. Thus, it is critical to implement safety guardrails with care.

We have trained safety features directly into the model to address these three key risks (described in the [Gemini 2.5 Computer Use System Card](https://storage.googleapis.com/deepmind-media/Model-Cards/Gemini-2-5-Computer-Use-Model-Card.pdf)).

Further, we also provide developers with safety controls, which empower developers to prevent the model from auto-completing potentially high-risk or harmful actions. Examples of these actions include harming a system's integrity, compromising security, bypassing CAPTCHAs, or controlling medical devices. The controls:

- **Per-step safety service:** An out-of-model, inference-time safety service that assesses each action the model proposes before it’s executed.
- **System instructions:** Developers can further specify that the agent either refuses or asks for user confirmation before it takes specific kinds of high-stakes actions. (Example in [documentation](https://ai.google.dev/gemini-api/docs/computer-use#safety-security)).

Additional recommendations for developers on safety measures and best practices can be found in our [documentation](https://ai.google.dev/gemini-api/docs/computer-use#safety-best-practices). While these safeguards are designed to reduce risk, we urge all developers to thoroughly test their systems before launch.

## How early testers have used it

Google teams have already deployed the model to production for use cases including UI testing, which can make software development signficantly faster. Versions of this model have also been powering [Project Mariner](https://deepmind.google/models/project-mariner/), the [Firebase Testing Agent](https://firebase.blog/posts/2025/04/app-testing-agent/), and some agentic capabilities in [AI Mode in Search](https://blog.google/products/search/ai-mode-agentic-personalized/).

Users from our early access program have also been testing the model to power personal assistants, workflow automation, and UI testing, and have seen strong results. In their own words:

## How to get started

Starting today, the model is available in public preview, accessible via the Gemini API on Google AI Studio and Vertex AI.

- **Try it now:** In a demo environment hosted by [Browserbase](http://gemini.browserbase.com/).
- **Start building**: Dive into our [reference](https://github.com/google/computer-use-preview) and [documentation](http://ai.google.dev/gemini-api/docs/computer-use) (see [Vertex AI docs for enterprise use](https://cloud.google.com/vertex-ai/generative-ai/docs/computer-use)) to learn how to build your own agent loop locally with Playwright or in a cloud VM with Browserbase.
- **Join the community:** We’re excited to see what you build. Share feedback and help guide our roadmap in our [Developer Forum](https://discuss.ai.google.dev/c/gemini-api/4).
