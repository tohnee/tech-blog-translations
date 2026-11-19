---
title: "MAI Cyber 2 Flash:Leading security. Lower cost"
source: https://microsoft.ai/news/introducing-mai-cyber-2-flash/
site: microsoft
date: 2026-11-17
crawled: 2026-11-19
---

# MAI Cyber 2 Flash:Leading security. Lower cost

Security teams need AI to find vulnerabilities, recommend fixes, and investigate threats around the clock.

Doing that at scale takes serious computing power, and the cost can quickly add up.

Built on Microsoft’s decades of proprietary security data and expertise, MAI Cyber 2 Flash is our latest specialist security model. It delivers leading performance on real-world security tasks at a fraction of the cost of larger models. And we’re bringing that capability directly into Microsoft’s security products.

# Proven by performance. Efficient by design

On CyberGym‑E2E[1](#fn-1), a benchmark measuring real-world vulnerability discovery, MAI Cyber 2 Flash (92.3%) beats GPT-6 Astra (91.5%)[5](#fn-5) at **less than** **2% of the cost per task.**[3](#fn-3) It also outperforms GPT-5.6 Cyber[6](#fn-6) on CyberGym‑E2E and WebExploitBench at the same reasoning budget.[2](#fn-2)

With a one-million-token context window, four times larger than MAI Cyber 1.1 Flash, it can analyze more of a codebase during complex, multi-step investigations. Early evaluations through Microsoft Perception show performance comparable to leading models on investigation agent and security-detection authoring tasks.

We’re already seeing what specialist models can deliver in customer environments: Insight Enterprises found MAI Cyber models to be **20% more token-efficient** than the GPT models it tested in its evaluations.[4](#fn-4)

These results point to a bigger opportunity: bringing advanced security capabilities to more workloads, without the cost of running larger models at every step.

## **Get started**

MAI Cyber 2 Flash is coming exclusively to Microsoft security products, including Codename MDASH, where it will automatically replace the existing model in the MAI profile for eligible customers starting mid-December.

**About these results**

*Results reflect evaluations on specific security tasks and configurations. Performance and cost comparisons vary by workload, model configuration, reasoning effort, and evaluation methodology.*

1. **CyberGym‑E2E:** MAI Cyber 2 Flash achieved 92.3% task success versus 91.5% for GPT‑6 Astra, using half the reasoning budget.
2. **WebExploitBench:** MAI Cyber 2 Flash achieved 40.4% versus 38.4% for GPT‑5.6 Cyber at the same reasoning budget.
3. **Cost per task:** Measured on CyberGym‑E2E from all input, cached input and output tokens, priced at list price (MAI Cyber 2 Flash $0.10 / $0.01 / $0.50 per 1M tokens; GPT‑6 Astra Azure OpenAI Global $10 / $1 / $50 per 1M tokens). Reflects offline evaluation cost, not customer spend.
4. **Insight Enterprises:** Customer-reported 20% token-efficiency advantage for MAI Cyber models versus GPT-5.4, GPT-5.3 Codex, and GPT-5.4 Mini.
5. **Benchmark integrity:** While reviewing our CyberGym‑E2E results, we found that 92 of the benchmark’s 905 tasks are based on the same open source projects and vulnerability reports as some of our training data. The benchmark’s reference solutions were never used in training. To be conservative, we excluded these 92 tasks for every model and report CyberGym‑E2E results on the remaining 813 tasks.
6. **Comparison with GPT‑****6 Cyber:** GPT‑6 Cyber is currently available only to select customers, and evaluating it on agentic, tool-using benchmarks requires additional safeguards that are still being put in place. We plan to share comparative results in the coming weeks.
