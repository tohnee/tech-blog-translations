---
title: "Introducing EVMbench"
date: 2026-02-18
source: https://openai.com/index/introducing-evmbench/
crawled: 2026-09-13
category: research
---

Smart contracts routinely secure $100B+ in open-source crypto assets. As AI agents improve at reading, writing, and executing code, it becomes increasingly important to measure their capabilities in economically meaningful environments, and to encourage the use of AI systems defensively to audit and strengthen deployed contracts.

Together with [Paradigm](https://www.paradigm.xyz), we’re introducing EVMbench, a benchmark evaluating the ability of AI agents to detect, patch, and exploit high-severity smart contract vulnerabilities. EVMbench draws on 117 curated vulnerabilities from 40 audits, with most sourced from open code audit competitions. EVMbench additionally includes several vulnerability scenarios drawn from the security auditing process for the [Tempo](https://tempo.xyz/) blockchain, a purpose-built L1 designed to enable high-throughput, low-cost payments via stablecoins. These scenarios extend the benchmark into payment-oriented smart contract code, where we expect agentic stablecoin payments to grow, and help ground it in a domain of emerging practical importance.

To create our task environments, we adapted existing proof-of-concept exploit tests and deployment scripts, when they existed, and otherwise manually wrote them. For the patch mode, we ensured that the vulnerabilities are exploitable and that can be mitigated without introducing compilation-breaking changes, which would compromise our setup. For the exploit mode, we wrote custom graders and red-teamed the environments in an attempt to find and patch methods by which an agent might cheat the grader. In addition to task quality control via domain expertise provided by Paradigm, we used automated task auditing agents to help increase the soundness of our environments.

EVMbench evaluates three capability modes:

- **Detect**: Agents audit a smart contract repository and are scored on recall of ground-truth vulnerabilities and associated audit rewards.
- **Patch**: Agents modify vulnerable contracts and must preserve intended functionality while eliminating exploitability, verified through automated tests and exploit checks.
- **Exploit**: Agents execute end-to-end fund-draining attacks against deployed contracts on a sandboxed blockchain environment, with grading performed programmatically via transaction replay and on-chain verification.

To support objective and reproducible evaluation, we developed a Rust-based harness that deploys contracts, replays agent transactions deterministically, and restricts unsafe RPC methods. Exploit tasks run in an isolated local Anvil environment rather than on live networks, and vulnerabilities are historical and publicly documented.

We evaluate frontier agents across all three modes. In the**‘exploit’** mode, GPT‑5.3‑Codex running via Codex CLI achieves a score of 71.0%. This represents a significant gain over previous models, such as GPT‑5, which scores 33.3% and was released just over six months ago. The detect recall and patch success rates remain below full coverage, as a large fraction of vulnerabilities remain difficult for agents to find and fix.

EVMbench also reveals interesting differences in model behavior across tasks. Agents perform best in the exploit setting, where the objective is explicit: continue iterating until funds are drained. In contrast, performance is weaker on detect and patch tasks. In**‘detect’**, agents sometimes stop after identifying a single issue rather than exhaustively auditing the codebase. In **‘patch’**, maintaining full functionality while removing subtle vulnerabilities remains challenging.

## Limitations

EVMbench does not represent the full difficulty of real-world smart contract security. The vulnerabilities included were drawn from Code4rena auditing competitions. While these are realistic and high-severity, many heavily deployed and widely used crypto contracts undergo significantly more scrutiny and may be harder to exploit.

Our grading system is robust but imperfect. In **‘detect’** mode, we check whether the agent finds the same vulnerabilities identified by human auditors. If the agent identifies additional issues, we do not currently have a reliable way to determine whether they represent true vulnerabilities that humans missed or false positives.

There are also structural limitations in the **‘exploit’** setting. Transactions are replayed sequentially in the grading container, so behaviors that depend on precise timing mechanics are out of scope. The chain state is a clean local Anvil instance rather than a fork of mainnet, and we currently support only single-chain environments. In some cases this requires mock contracts instead of mainnet deployments.

## Why this matters

Smart contracts secure billions of dollars in assets, and AI agents are likely to be transformative for both attackers and defenders. Measuring model capability in this domain helps track emerging cyber risks and highlights the importance of using AI systems defensively to audit and strengthen deployed contracts.

EVMbench is intended both as a measurement tool and as a call to action. As agents improve, it becomes increasingly important for developers and security researchers to incorporate AI-assisted auditing into their workflows.

Over recent months, we’ve seen meaningful gains in model performance on cybersecurity tasks, benefiting both developers and security professionals. In parallel, we’ve been [preparing strengthened cyber safeguards](https://openai.com/index/strengthening-cyber-resilience/) to support defensive use and broader ecosystem resilience.

Because cybersecurity is inherently dual-use, we’re taking an evidence-based, iterative approach that accelerates defenders’ ability to find and fix vulnerabilities while slowing misuse. Our mitigations include safety training, automated monitoring, [trusted access](https://openai.com/index/trusted-access-for-cyber/) for advanced capabilities, and enforcement pipelines including threat intelligence.

We’re investing in ecosystem safeguards such as expanding the private beta of [Aardvark](https://openai.com/index/introducing-aardvark/), our security research agent, and partnering with open-source maintainers to provide free codebase scanning for widely used projects.

Building on our Cybersecurity Grant Program launched in 2023, we’re also committing $10M in API credits to accelerate cyber defense with our most capable models, especially for open source software and critical infrastructure systems. Organizations engaged in good-faith security research can apply for API credits and support through our [Cybersecurity Grant Program](https://openai.com/form/cybersecurity-grant-program/).

We release EVMbench’s tasks, tooling, and evaluation framework to support continued research on measuring and managing emerging AI cyber capabilities.
