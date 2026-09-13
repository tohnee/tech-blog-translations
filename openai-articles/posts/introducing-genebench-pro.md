---
title: "Introducing GeneBench-Pro"
date: 2026-06-30
source: https://openai.com/index/introducing-genebench-pro/
crawled: 2026-09-13
category: research
---

Scientific data rarely arrive with instructions. Researchers must decide whether a pattern reflects biology or noise, whether the data can support the question being asked, and how each result should change what they do next. AI agents are increasingly capable of executing complex analyses, but real scientific research also depends not simply on recalling facts or following a predefined workflow but also on making these higher-order judgments.

Today, we’re introducing GeneBench-Pro—a challenging, research-level benchmark for testing whether models can handle the kind of judgment-heavy analysis that real-world computational biology requires. It expands on [GeneBench](https://www.biorxiv.org/content/10.64898/2026.04.22.720113v1) to cover harder, more realistic tasks across genomics, quantitative biology, and translational medicine, capturing the complexity, iterative nature, and ambiguity of scientific research in computational biology.

To date, there have been few convincing assessments of the system-level judgment calls that make real-world computational research difficult. These include handling ambiguity, revising assumptions, choosing the correct analysis path, and knowing when a result is decision-ready. Because these skills are difficult to formalize, they are also difficult to assess rigorously, even as weaknesses in them increasingly constrain overall AI performance.

GeneBench-Pro is designed to precisely measure these higher-level capabilities. Within GeneBench-Pro, we define “research taste” as the chains of judgment calls that shape an analysis: which questions the data can support, how early diagnostics should change the model or estimand, and when an initial plan needs to be revised. Each GeneBench-Pro problem gives the model a realistic and messy dataset, brief experimental context, and a target estimand tied to a downstream decision. To answer correctly, the model must explore the data, choose an appropriate analytical approach, engage in an iterative process of experimentation, and supply a final answer.

## Dataset construction

In biology, the cost of data generation (e.g., genome sequencing) has fallen dramatically, and [some researchers now argue](https://www.nature.com/articles/s41576-022-00551-z) that the limiting factor is no longer sample collection but downstream computation and analysis. GeneBench-Pro is built to assess progress in addressing that bottleneck, with 129 questions covering a broad range of computational biology settings and methods.

This atlas provides a preview of the breadth of GeneBench-Pro. Visit the [case studies page](https://openai.com/index/genebench-pro/case-studies/) to explore 10 representative questions in more detail.

GeneBench-Pro is also designed to avoid common benchmark failures. Many long-horizon biology benchmarks construct multi-step questions around messy historical datasets, where there may be no single correct path through the analysis. An agent might choose one defensible cutoff, while another might choose a different but equally defensible option, reflecting the arbitrary choices made by the benchmark creator more than any fundamental differences in model performance. The reverse can also happen: if a problem is too numerically insensitive, an agent can make fundamental errors in an analysis and still produce a passing result.

To avoid these failure modes, each GeneBench-Pro problem is built synthetically: we know the full causal structure and directly simulate the data-generating process. That enables us to tune the complexity of each problem, ensure that reasonable differences in subjective analytical choices still produce accepted numerical results, and verify (through ablation studies) that plausible but incorrect analyses fail. We then audit problem drafts through detailed trace analyses to check for information leakage and unintended solution pathways. This gives us confidence that getting the right answer depends on choosing the correct analytic pathway and not on exploiting a shortcut or matching an arbitrary author preference.

We sent 82 of the 129 GeneBench-Pro questions to external domain experts, including graduate students, postdoctoral researchers, industry scientists, and professors. Reviewers assessed each problem’s realism, whether the target answer was identifiable, and whether the methods and estimators were appropriate. Feedback was used to improve problems.

Alexander Strudwick Young, Assistant Professor in Human Genetics at UCLA

Jennifer Grundman, PhD Candidate in Human Genetics at UCLA

Alexander Strudwick Young, Assistant Professor in Human Genetics at UCLA

Jennifer Grundman, PhD Candidate in Human Genetics at UCLA

- Alexander Strudwick Young, Assistant Professor in Human Genetics at UCLA
- Jennifer Grundman, PhD Candidate in Human Genetics at UCLA

## Evaluation and grading

Each GeneBench-Pro problem is a self-contained scientific analysis. Agents receive access to an isolated workspace with a short prompt, data files, and a standard bioinformatics stack including Python, scientific computing libraries, and basic genomics packages like PLINK 2.0 (although the problems do not require domain-specific tooling).

Because we control the full data-generation process, we can grade correctness deterministically against known targets, avoiding model-choice variability and verbosity effects found in standard rubric-based evaluation.

Each problem also comes with rich metadata, including the intended analysis structure, attached data files, a detailed multi-page case study, and expert review outcomes. We are fully open-sourcing 10 representative GeneBench-Pro questions on [Hugging Face](https://huggingface.co/datasets/openai/genebench-pro-public-package), with an [interactive web interface](https://openai.com/index/genebench-pro/case-studies/) for browsing them. Finally, we will provide a 50-question subset to [Artificial Analysis](https://artificialanalysis.ai/) for independent, third-party benchmarking in the near future.

## Results

Our strongest model at the time of testing, GPT‑5.6 Sol, attains a pass rate of 28.7% at the highest reasoning level (31.5% with Pro mode enabled). That is a sharp increase from when we began building the original GeneBench; at that time, our best frontier model, GPT‑5, scored below 5%. Progress on this benchmark suggests that frontier models are improving quickly, even on less tangible, systems-level scientific reasoning. At the current pace, this benchmark may be saturated by the end of the year.

The results also show the impact of scaling test-time compute. At the lowest reasoning level, GPT‑5.6 Sol only achieves a single-digit passrate. At the highest reasoning level, GPT‑5.6 Sol solves nearly six times as many questions as GPT‑5.2 does while using about two-thirds as many tokens.

Comparisons across model families suggest that GPT models are among the strongest systems at high-level scientific reasoning under quantitative uncertainty. The performance gap between GPT‑5.6, GPT‑5.5 and leading open-source models such as GLM 5.2 is significantly larger than we would expect when extrapolating from [coding benchmarks](https://deepswe.datacurve.ai/), indicating that open-source models are more specialized for coding than for broader reasoning ability.

We used frontier GPT models to evaluate and harden problems during development. As such, we suspected GeneBench-Pro might be biased against GPT models relative to other model families. However, competitor models at best matched the performance of the corresponding GPT model at the time of release, and tended to fall short considerably.

These evaluation results—as high as 31.5% on GPT‑5.6 Sol (Pro)—are striking given the difficulty of the GeneBench-Pro questions. In a survey, our reviewers estimated that a typical GeneBench-Pro problem would take a human expert around 20–40 hours to complete. At a conservative $200 per hour, that puts the human labor cost of a single problem in the thousands of dollars. Current AI agents are still too unreliable to replace human experts, but the cost gap is large, with inference costs at only several dollars per problem. That means even partial automation at current capabilities could create meaningful economic and scientific value.

Cyrillus Tan, Postdoctoral Research Associate at the New York Genome Center

Lex Flagel, Director of Data Science at Gencove

Cyrillus Tan, Postdoctoral Research Associate at the New York Genome Center

Lex Flagel, Director of Data Science at Gencove

- Cyrillus Tan, Postdoctoral Research Associate at the New York Genome Center
- Lex Flagel, Director of Data Science at Gencove

Still, the fact that frontier models still solve fewer than a third of these problems shows that there is substantial room for improvement. Models can make partial progress on challenging problems, but they struggle to close the inferential loop. This failure pattern mirrors the contrast between human experts and novices. Experts use their experience to frame the problem and adapt their approach, while novices make observations but struggle to integrate them into the broader context of the problem.

Achieving near-perfect performance will require evaluations that both reliably measure progress and identify where models still fail. Benchmarks like GeneBench-Pro can help to turn a vague capability deficiency into something we can diagnose and improve.

If agents can reliably automate this class of analysis, they could significantly accelerate scientific discovery. Human genetic evidence is already central to target prioritization and translational follow-up, because mechanisms with genetic support are much more likely to lead to approved treatments.

Meanwhile, sequencing costs have plummeted, and biobank-scale datasets now link molecular, phenotypic, and health-record information at unprecedented breadth. The limiting factor is shifting from data generation to turning the information into actionable insights. Models that can consistently perform analyses now handled by teams of human experts could transform industrial research by accelerating hypothesis triage, target follow-up, and the iteration cycle between data generation and decision-making.

GeneBench-Pro represents an initial effort to evaluate the more abstract skills involved in good scientific judgment possessed by experienced. These skills allow them to intuit and identify the most promising initial analyses, iterate and revise their thinking when data contradict initial assumptions, and arrive at conclusions upon which downstream clinical, academic, or business decisions may depend.

We anticipate that as model capabilities advance, benchmarks that probe model abilities at these higher levels of abstraction will become increasingly useful, beyond those that simply test book knowledge or the ability to execute routine analyses.
