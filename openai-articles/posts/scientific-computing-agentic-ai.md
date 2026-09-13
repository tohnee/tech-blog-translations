---
title: "Scientific computing in the age of agentic AI"
date: 2026-07-28
source: https://openai.com/index/scientific-computing-agentic-ai/
crawled: 2026-09-13
category: research
---

Scientific computing is a core pillar of modern research across academia and industry. Yet the software needed to analyze scientific information has struggled to keep pace with the rapid rate of data generation. Many widely used research tools began as code accompanying a research paper, built by small academic teams with limited engineering experience and minimal time for packaging, testing, optimization, or long-term support. The result is scientific infrastructure that often depends on slow, fragile workflows requiring constant maintenance. These constraints impede the pace of discovery.

AI agents are beginning to change that equation. By lowering the costs of engineering work and taking on tedious implementation tasks, they can help researchers prototype ideas more quickly, pursue projects that were previously impractical, and more easily maintain software over the long term. As a result, scientific software becomes more efficient and better maintained, freeing researchers to spend more time on discovery.

We’re sharing an exploratory field report of eight agent-assisted scientific computing projects primarily in the life sciences; five using Codex alone, and three using a combination of Codex and Claude Code. The report brings together case studies written by the teams behind each project and identifies recurring themes. The projects range from routine maintenance and targeted optimization to large-scale language migrations and GPU-native redesigns. Contributors report that agents significantly accelerated software development and maintenance, in some cases helping small teams take on work that would otherwise have required far more time or specialized engineering support. But they also highlight the persistent challenge of establishing clear, long-term responsibility and stewardship of the resulting tools.

Contributors consistently describe a shift in the researchers’ role from implementation to verification and orchestration: specifying what to build, defining how to measure correctness, and deciding when a project is ready to ship. In this emerging model, the researchers remain in control of the scientific direction and quality bar, but with velocity uplift provided by agentic assistance

## Case studies

#### **Modernized a widely used library for parsing genomic data**

cyvcf2 is a Python library for reading and writing genomic variant files. GPT‑5.5 replaced the library’s legacy build and packaging system with a modern, unified process designed to make the library easier to install, test, and release.

> *With coding agents, it’s quite easy to go fast; for now, to go far in science, there’s still a need for expert guidance, understanding, taste, and care.*

—Brent Pedersen

## Recurring themes

Though the projects varied widely in scope, they demonstrated that coding agents are making engineering labor and expertise less of a constraint in scientific computing. Now, the bottleneck is validating an AI agent’s output, which still depends on human judgement.

Across case studies, agents handled specific, well-scoped requests effectively but could not reliably judge whether their work was scientifically valid or met expectations. Indeed, agents often expressed confidence even when their work contained clear errors. Human reviewers therefore needed to find reliable ways to validate the results. The strongest approaches used an external reference or measurable acceptance target such as exact output agreement, parity with an existing tool, appropriate statistical behavior, or answers established in advance using simulated data.

Another recurring theme was that the projects generally proceeded in stages using feedback-driven iterations rather than as one-shot approaches. Contributors broke down broad goals into smaller changes, then used intermediate benchmarks and test systems to evaluate and refine the agents’ work. Agents often produced initial implementations quickly, but resolving edge cases and subtle numerical differences took much longer. Completing the “last mile” of an implementation often took the most work.

Overall, these case studies suggest that agents are enabling researchers to spend less time on implementation and more time directing the scientific work. People define the goal, break down complex projects into manageable chunks, and judge whether results are scientifically valid. By easing longstanding engineering constraints, agents expand what researchers can build while freeing them to focus on the scientific questions and decisions that matter most.

## Long-term stewardship remains essential

The maintenance gap in research software has long slowed iteration and limited reproducibility and reliability. Published studies of “[research code](https://doi.org/10.1038/s41597-022-01143-6)” and [omics tools](https://doi.org/10.1371/journal.pbio.3000333) have found that published software often fails to properly install in a fresh computing setup or run as documented, forcing researchers to spend substantial time on configuration and debugging. Even routine improvements can save researchers time and reduce computing demands, while performance-based refactoring and rewrites can deliver larger gains.

But lower implementation costs also make it easier to produce many similar rewrites, fragmenting users and spreading the expert attention required to keep any one tool reliable. That makes long-term stewardship and attribution essential. Mature scientific software carries undocumented conventions, compatibility requirements, and user trust that translating the source code alone cannot reproduce.

The case studies illustrate several possible paths forward. Changes to MHCflurry and cyvcf2 were incorporated into their original upstream projects, while rustar-aligner moved under new community stewardship because the original project had been abandoned. Where coordination with existing maintainers is available, it should begin as early as possible. When a separate implementation is necessary, it needs a clear owner and a credible maintenance plan. Without that, today’s modern rewrite can become tomorrow’s abandoned code rather than reliable scientific infrastructure.

## Toward more durable scientific software

This field report is retrospective and exploratory, but the case studies point to a practical shift in how scientific software is developed. Coding agents such as Codex can significantly lower the cost of maintenance, migration, optimization, and new implementations. Their long-term scientific value still depends on human decisions around what to build, how to verify it, and who will maintain it. The deeper change is not simply that researchers can produce more software, but that they can focus more of their effort on defining, validating, and stewarding the tools.

These case studies show that agents can already accelerate the pace of iteration in scientific computing. As coding agents improve, researchers will be able to spend less time keeping analysis pipelines running and more time advancing their fields.
