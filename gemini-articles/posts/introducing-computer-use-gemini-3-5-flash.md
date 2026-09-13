---
title: "Introducing computer use in Gemini 3.5 Flash"
source: https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-computer-use-gemini-3-5-flash/
site: gemini
date: 2026-06-24
authors: Mateo Quiros
crawled: 2026-09-13
---

Computer use is now a built-in tool supported in Gemini 3.5 Flash, delivering our best performance yet for agentic computer use tasks. Previously only available as a standalone [Gemini 2.5 computer use model,](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/gemini-computer-use-model/) computer use is now integrated natively in the main Gemini Flash model. Gemini already excels at function calling and using built-in tools like Search and Maps grounding. With built-in computer use capability, developers can now use 3.5 Flash to reliably build custom agents that can see, reason and take action across browser, mobile and desktop environments. This unlocks improved performance for long-horizon and enterprise automation tasks like continuous software testing and knowledge work across professional applications.

![Gemini 3.5 benchmarks](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-5__benchmark-OSWorld-Ve.width-1200.format-webp.webp)

Developers and enterprises can start using computer use in 3.5 Flash via the [Gemini API](https://ai.google.dev/gemini-api/docs/computer-use) and [Gemini Enterprise Agent Platform](https://console.cloud.google.com/projectselector2/agent-platform/overview?pli=1&supportedpurview=project).

3.5 Flash uses computer use to analyse the Gemini app and return a categorized list of features.

3.5 Flash with computer use audits its own documentation for accessibility issues.

## Making computer use safe in 3.5 Flash

To mitigate some of the prompt injection risks for agents operating in live environments, we use targeted adversarial training for computer use in Gemini 3.5 Flash. We’re also releasing two optional enterprise safeguard systems that enable enterprises to:

- Require explicit user confirmation for sensitive or irreversible actions.
- Automatically stop tasks if an indirect prompt injection is identified.

Taking a “defense-in-depth” approach, we encourage developers to combine these features with secure sandboxing, human-in-the-loop verification and strict access controls. Additional information on safety measures can be found in our [best practices](https://ai.google.dev/gemini-api/docs/computer-use#safety-best-practices) documentation.

We are already seeing customers drive value with computer use. Here’s what some of them have to say:

![Quote from Migual Gonzalez Fernandez, Browserbase](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Gemini_3.5_Flash_BrowserBase_v2.width-100.format-webp.webp)

![Quote from Magnus Muller, CEO, Browser Use](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Gemini_3.5_Flash_Browser_Use_1.width-100.format-webp.webp)

![quote from Alvin Stanescu, Senior Director - UIPath](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Gemini_3.5_Flash_UiPath_v3.width-100.format-webp.webp)

To start building with computer use today:

- **Try it now**: Test the capabilities in a [demo environment hosted by Browserbase.](http://gemini.browserbase.com/)
- **Start building**: Dive into our [reference implementation](https://github.com/google-gemini/computer-use-preview) and documentation via [Gemini API](https://ai.google.dev/gemini-api/docs/interactions/computer-use) and [Gemini Enterprise Agent Platform](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/computer-use).
