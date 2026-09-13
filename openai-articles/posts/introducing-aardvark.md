---
title: "Introducing Aardvark: OpenAI’s agentic security researcher"
date: 2025-10-30
source: https://openai.com/index/introducing-aardvark/
crawled: 2026-09-13
category: research
---

***March 6, 2026 Update:****Aardvark is now Codex Security, and is available as a research preview.*

*Aardvark is now built directly into Codex as Codex Security, and is rolling out to ChatGPT Enterprise, Business, and Edu customers via Codex web with free usage for the next month. Please see our blog*[*here.*](https://openai.com/index/codex-security-now-in-research-preview/)

Today, we’re announcing Aardvark, an agentic security researcher powered by GPT‑5.

Software security is one of the most critical—and challenging—frontiers in technology. Each year, tens of thousands of new vulnerabilities are discovered across enterprise and open-source codebases. Defenders face the daunting tasks of finding and patching vulnerabilities before their adversaries do. At OpenAI, we are working to tip that balance in favor of defenders.

Aardvark represents a breakthrough in AI and security research: an autonomous agent that can help developers and security teams discover and fix security vulnerabilities at scale. Aardvark is now available in private beta to validate and refine its capabilities in the field.

## How Aardvark works

Aardvark continuously analyzes source code repositories to identify vulnerabilities, assess exploitability, prioritize severity, and propose targeted patches.

Aardvark works by monitoring commits and changes to codebases, identifying vulnerabilities, how they might be exploited, and proposing fixes. Aardvark does not rely on traditional program analysis techniques like fuzzing or software composition analysis. Instead, it uses LLM-powered reasoning and tool-use to understand code behavior and identify vulnerabilities. Aardvark looks for bugs as a human security researcher might: by reading code, analyzing it, writing and running tests, using tools, and more.

Aardvark relies on a multi-stage pipeline to identify, explain, and fix vulnerabilities:

- **Analysis**: It begins by analyzing the full repository to produce a threat model reflecting its understanding of the project’s security objectives and design.
- **Commit scanning**: It scans for vulnerabilities by inspecting commit-level changes against the entire repository and threat model as new code is committed. When a repository is first connected, Aardvark will scan its history to identify existing issues. Aardvark explains the vulnerabilities it finds step-by-step, annotating code for human review.
- **Validation**: Once Aardvark has identified a potential vulnerability, it will attempt to trigger it in an isolated, sandboxed environment to confirm its exploitability. Aardvark describes the steps taken to help ensure accurate, high-quality, and low false-positive insights are returned to users.
- **Patching**: Aardvark integrates with OpenAI Codex to help fix the vulnerabilities it finds. It attaches a Codex-generated and Aardvark-scanned patch to each finding for human review and efficient, one-click patching.

Aardvark works alongside engineers, integrating with GitHub, Codex, and existing workflows to deliver clear, actionable insights without slowing development. While Aardvark is built for security, in our testing we’ve found that it can also uncover bugs such as logic flaws, incomplete fixes, and privacy issues.

## Real impact, today

Aardvark has been in service for several months, running continuously across OpenAI’s internal codebases and those of external alpha partners. Within OpenAI, it has surfaced meaningful vulnerabilities and contributed to OpenAI’s defensive posture. Partners have highlighted the depth of its analysis, with Aardvark finding issues that occur only under complex conditions.

In benchmark testing on “golden” repositories, Aardvark identified 92% of known and synthetically-introduced vulnerabilities, demonstrating high recall and real-world effectiveness.

## Aardvark for Open Source

Aardvark has also been applied to open-source projects, where it has discovered and we have responsibly disclosed numerous vulnerabilities—ten of which have received Common Vulnerabilities and Exposures (CVE) identifiers.

As beneficiaries of decades of open research and responsible disclosure, we’re committed to giving back—contributing tools and findings that make the digital ecosystem safer for everyone. We plan to offer pro-bono scanning to select non-commercial open source repositories to contribute to the security of the open source software ecosystem and supply chain.

We recently [updated](https://openai.com/index/scaling-coordinated-vulnerability-disclosure/) our [outbound coordinated disclosure policy](https://openai.com/policies/outbound-coordinated-disclosure-policy/) which takes a developer-friendly stance, focused on collaboration and scalable impact, rather than rigid disclosure timelines that can pressure developers. We anticipate tools like Aardvark will result in the discovery of increasing numbers of bugs, and want to sustainably collaborate to achieve long-term resilience.

## Why it matters

Software is now the backbone of every industry—which means software vulnerabilities are a systemic risk to businesses, infrastructure, and society. Over 40,000 CVEs were reported in 2024 alone. Our testing shows that around 1.2% of commits introduce bugs—small changes that can have outsized consequences.

Aardvark represents a new defender-first model: an agentic security researcher that partners with teams by delivering continuous protection as code evolves. By catching vulnerabilities early, validating real-world exploitability, and offering clear fixes, Aardvark can strengthen security without slowing innovation. We believe in expanding access to security expertise. We’re beginning with a private beta and will broaden availability as we learn.

## Private beta now open

We’re inviting select partners to join the Aardvark private beta. Participants will gain early access and work directly with our team to refine detection accuracy, validation workflows, and reporting experience.

We’re looking to validate performance across a variety of environments. If your organization or open source project is interested in joining, you can [apply here](https://www.openai.com/form/aardvark-beta-signup).
