---
title: "The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery"
arxiv: 2408.06292
source: https://arxiv.org/abs/2408.06292
crawled: 2026-09-23
---

# The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery

Chris Lu
Affiliation: Equal Contribution
Affiliation: Sakana AI
Affiliation: FLAIR, University of Oxford
  
Cong Lu
Affiliation: Equal Contribution
Affiliation: University of British Columbia
Affiliation: Vector Institute
  
Robert Tjarko Lange
Affiliation: Equal Contribution
Affiliation: Sakana AI
  
Jakob Foerster
Affiliation: FLAIR, University of Oxford
Affiliation: Equal Advising
  
Jeff Clune
Affiliation: University of British Columbia
Affiliation: Vector Institute
Affiliation: Canada CIFAR AI Chair
Affiliation: Equal Advising
  
David Ha
Affiliation: Sakana AI
Affiliation: Equal Advising

###### Abstract

One of the grand challenges of artificial general intelligence is developing agents capable of conducting scientific research and discovering new knowledge.
While frontier models have already been used as aides to human scientists, e.g. for brainstorming ideas, writing code, or prediction tasks, they still conduct only a small part of the scientific process.
This paper presents the first comprehensive framework for fully *automatic scientific discovery*, enabling frontier large language models (LLMs) to perform research independently and communicate their findings.
We introduce The AI Scientist, which generates novel research ideas, writes code, executes experiments, visualizes results, describes its findings by writing a full scientific paper, and then runs a simulated review process for evaluation.
In principle, this process can be repeated to iteratively develop ideas in an open-ended fashion and add them to a growing archive of knowledge, acting like the human scientific community.
We demonstrate the versatility of this approach by applying it to three distinct subfields of machine learning: diffusion modeling, transformer-based language modeling, and learning dynamics.
Each idea is implemented and developed into a full paper at a meager cost of less than $15 per paper, illustrating the potential for our framework to democratize research and significantly accelerate scientific progress.
To evaluate the generated papers, we design and validate an automated reviewer, which we show achieves near-human performance in evaluating paper scores.
The AI Scientist can produce papers that exceed the acceptance threshold at a top machine learning conference as judged by our automated reviewer.
This approach signifies the beginning of a new era in scientific discovery in machine learning: bringing the transformative benefits of AI agents to the *entire* research process of AI itself, and taking us closer to a world where *endless affordable creativity and innovation* can be unleashed on the world’s most challenging problems.
Our code is open-sourced at <https://github.com/SakanaAI/AI-Scientist>.

## 1 Introduction

The modern scientific method ([Chalmers, 2013](#bib.bib14); [Jevons, 1877](#bib.bib44); [Dewey, 1910](#bib.bib20)) is arguably one of the greatest achievements of the Enlightenment.
Traditionally, a human researcher collects background knowledge, drafts a set of plausible hypotheses to test, constructs an evaluation procedure, collects evidence for the different hypotheses, and finally assesses and communicates their findings. Afterward, the resulting manuscript undergoes peer review and subsequent iterations of refinement.
This procedure has led to countless breakthroughs in science and technology, improving human quality of life.
However, this iterative process is inherently limited by human researchers’ ingenuity, background knowledge, and finite time.
Attempting to automate general scientific discovery ([Waltz and Buchanan, 2009](#bib.bib100); [Langley, 2024](#bib.bib57); [Langley, 1987](#bib.bib56)) has been a long ambition of the community since at least the early 70s, with computer-assisted works like the Automated Mathematician ([Lenat, 1977](#bib.bib62); [Lenat and Brown, 1984](#bib.bib63)) and DENDRAL ([Buchanan and Feigenbaum, 1981](#bib.bib12)).
In the field of AI, researchers have envisioned the possibility of automating AI research using AI itself ([Schmidhuber, 1991](#bib.bib85); [Schmidhuber, 2010b](#bib.bib87); [Schmidhuber, 2010a](#bib.bib86); [Schmidhuber, 2012](#bib.bib88); [Ghahramani, 2015](#bib.bib30)), leading to “AI-generating algorithms” ([Clune, 2019](#bib.bib18)).
More recently, foundation models have seen tremendous advances in their general capabilities ([OpenAI, 2023](#bib.bib79); [Google DeepMind Gemini Team, 2023](#bib.bib34); [Anthropic, 2024](#bib.bib4); [Llama Team, 2024](#bib.bib66)), but they have only been shown to accelerate individual parts of the research pipeline, e.g. the writing of scientific manuscripts ([Altmäe et al., 2023](#bib.bib2); [Ifargan et al., 2024](#bib.bib43); [Majumder et al., 2024](#bib.bib73); [Dinu et al., 2024](#bib.bib22)), as a muse to brainstorm ideas ([Girotra et al., 2023](#bib.bib31); [Wang et al., 2024b](#bib.bib104); [Baek et al., 2024](#bib.bib6)), or aides to coding ([Gauthier, 2024](#bib.bib29)).
To date, the community has yet to show the possibility of executing entire research endeavors without human involvement.

Traditional approaches to automating research projects have so far relied on carefully constraining the search space of potential discoveries, which severely limits the scope of exploration and requires substantial human expertise and design.
For example, significant advancements in materials discovery ([Pyzer-Knapp et al., 2022](#bib.bib82); [Merchant et al., 2023](#bib.bib75); [Szymanski et al., 2023](#bib.bib97)) and synthetic biology ([Jumper et al., 2021](#bib.bib47); [Hayes et al., 2024](#bib.bib36)) have been achieved by restricting exploration to well-characterized domains with predefined parameters, which allows for targeted progress but limits broader, open-ended discovery and addressing only a subset of the scientific process, without encompassing tasks such as manuscript preparation.
Within the field of machine learning itself, research automation has largely been restricted to hyperparameter and architecture search ([He et al., 2021](#bib.bib37); [Hutter et al., 2019](#bib.bib41); [Wan et al., 2021](#bib.bib101); [Lu et al., 2022b](#bib.bib69); [Wan et al., 2022](#bib.bib102)) or algorithm discovery ([Metz et al., 2022](#bib.bib76); [Lange et al., 2023b](#bib.bib54); [Lange et al., 2023a](#bib.bib53); [Lu et al., 2022a](#bib.bib67); [Kirsch et al., 2019](#bib.bib52); [Chen et al., 2024b](#bib.bib17); [Alet et al., 2020](#bib.bib1)) within a hand-crafted search space.
Recent advances in LLMs have shown the potential to extend the search space to more generalized, code-level solutions ([Ma et al., 2023](#bib.bib71); [Lu et al., 2024a](#bib.bib68); [Faldor et al., 2024](#bib.bib24); [Lehman et al., 2022](#bib.bib60)).
However, these approaches remain constrained by rigorously-defined search spaces and objectives, which limit the breadth and depth of possible discoveries.

In this paper, we introduce The AI Scientist, the first fully automated and scalable pipeline for end-to-end paper generation, enabled by recent advances in foundation models.
Given a broad research direction and a simple initial codebase, The AI Scientist seamlessly performs ideation, a literature search, experiment planning, experiment iterations, manuscript writing, and peer reviewing to produce insightful papers.
Furthermore, in principle The AI Scientist can run in an open-ended loop, building on its previous scientific discoveries to improve the next generation of ideas.
This allows us to speed up the slow nature of scientific iteration at a surprisingly low financial cost (∼\sim$15/paper) and represents a step towards turning the world’s ever-increasing computing resources into the scientific breakthroughs needed to tackle the core challenges of the 21st century.
Here, we focus on Machine Learning (ML) applications, but this approach can more generally be applied to almost any other discipline, e.g. biology or physics, given an adequate way of automatically executing experiments ([Kehoe et al., 2015](#bib.bib50); [Arnold, 2022](#bib.bib5); [Zucchelli et al., 2021](#bib.bib115)).

By leveraging modern LLM frameworks like chain-of-thought ([Wei et al., 2022](#bib.bib107)) and self-reflection ([Shinn et al., 2024](#bib.bib89)) to improve decision-making, The AI Scientist is able to generate its own scientific ideas and hypotheses, as well as a plan for testing them with experiments.
Next, The AI Scientist implements plan-directed code-level changes to the experiment “template” using the state-of-the-art coding assistant Aider ([Gauthier, 2024](#bib.bib29)), and executes experiments to collect a set of computational results, which are in turn used to draft a scientific paper.
The AI Scientist then performs an automated paper-reviewing process using guidelines from a standard machine learning conference.
Finally, The AI Scientist adds the completed ideas and reviewer feedback to its archive of scientific findings, and the process repeats.
Crucially, the generated paper and experimental artifacts The AI Scientist produces allow us to easily interpret and judge its findings post-hoc, allowing human scientists to also benefit from what is learned.

![Refer to caption](2408.06292v3/figures/conceptual.png)

Figure 1: Conceptual illustration of The AI Scientist, an end-to-end LLM-driven scientific discovery process.
The AI Scientist first invents and assesses the novelty of a set of ideas.
It then determines how to test the hypotheses, including writing the necessary code by editing a codebase powered by recent advances in automated code generation.
Afterward, the experiments are automatically executed to collect a set of results consisting of both numerical scores and visual summaries (e.g. plots or tables).
The results are motivated, explained, and summarized in a LaTeX report.
Finally, The AI Scientist generates an automated review, according to current practice at standard machine learning conferences.
The review can be used to either improve the project or as feedback to future generations for open-ended scientific discovery.

Our contributions are summarized as follows:

1. 1.

   We introduce the first end-to-end framework for fully automated scientific discovery in Machine Learning research, enabled by frontier LLMs ([Section 3](#S3 "3 The AI Scientist ‣ The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery")). This fully automated process includes idea generation, experiment design, execution, and visualizing and writing up the results into a full manuscript.
2. 2.

   To assess the quality of the generated papers, we introduce a foundation model-based reviewing process in [Section 4](#S4 "4 Automated Paper Reviewing ‣ The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery"). This process achieves near-human-level performance across multiple evaluation metrics (e.g. 65% vs. 66% balanced accuracy) when evaluated on ICLR 2022 OpenReview data. The reviews further enable The AI Scientist to select the best ideas for “publication” to an ever-growing archive of scientific discoveries, and the process can be repeated to build on these discoveries, just as in the human scientific community.
3. 3.

   The AI Scientist can generate hundreds of interesting, medium-quality papers over the course of a week.
   In this report, we focus on a subset of these papers, highlighting novel insights in diffusion modeling, language modeling, and grokking.
   We perform an in-depth case study into one selected paper in [Section 5](#S5 "5 In-Depth Case Study ‣ The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery"), and present aggregate results in [Section 6](#S6 "6 Experiments ‣ The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery").
4. 4.

   We conclude the paper with an extensive discussion on the limitations, ethical considerations, and future outlook of our approach in [Sections 8](#S8 "8 Limitations & Ethical Considerations ‣ The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery") and [9](#S9 "9 Discussion ‣ The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery").

## 2 Background

Large Language Models.
In this paper, we build our automated scientist from autoregressive large language models (LLMs, [OpenAI (2023)](#bib.bib79); [Google DeepMind Gemini Team (2023)](#bib.bib34); [Anthropic (2023)](#bib.bib3); [Llama Team (2024)](#bib.bib66); [Zhu et al. (2024)](#bib.bib114)) which learn to generate text completions by modeling the conditional probability of a new token (similar to a word) given the preceding tokens, p⁡(xt|x<t;θ)p(x_{t}|x_{<t};\theta), and sampling at test-time.
Together with vast data and model scaling, this enables LLMs to not only generate coherent text, but crucially also exhibit human-like abilities, including commonsense knowledge ([Talmor et al., 2019](#bib.bib98)), reasoning ([Wei et al., 2022](#bib.bib107)), and the ability to write code ([Chen et al., 2021](#bib.bib16); [Xu et al., 2022](#bib.bib108)).

LLM Agent Frameworks.
Typical applications of LLMs often involve embedding the model into an “agent” ([Wang et al., 2024a](#bib.bib103)) framework, including the following possibilities: the structuring of language queries (e.g. few-shot prompting ([Brown et al., 2020](#bib.bib11))), encouraging reasoning traces (e.g. chain-of-thought ([Wei et al., 2022](#bib.bib107))), or asking the model to iteratively refine its outputs (e.g., self-reflection ([Shinn et al., 2024](#bib.bib89))).
These leverage the language model’s ability to learn in-context ([Olsson et al., 2022](#bib.bib78)) and can greatly improve its performance, robustness and reliability on many tasks.

Aider: An LLM-Based Coding Assistant.
Our automated scientist directly implements ideas in code and uses a state-of-the-art open-source coding assistant, Aider ([Gauthier, 2024](#bib.bib29)).
Aider is an agent framework that is designed to implement requested features, fix bugs, or refactor code in existing codebases.
While Aider can in principle use any underlying LLM, with frontier models it achieves a remarkable success rate of 18.9% on the SWE Bench ([Jimenez et al., 2024](#bib.bib46)) benchmark, a collection of real-world GitHub issues.
In conjunction with new innovations added in this work, this level of reliability enables us, for the first time, to fully automate the ML research process.

## 3 The AI Scientist

Overview.
The AI Scientist has three main phases ([Figure 1](#S1.F1 "In 1 Introduction ‣ The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery")): (1) Idea Generation, (2) Experimental Iteration, and (3) Paper Write-up. After the write-up, we introduce and validate an LLM-generated review to assess the quality of the generated paper ([Section 4](#S4 "4 Automated Paper Reviewing ‣ The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery")).
We provide The AI Scientist with a starting *code template* that reproduces a lightweight baseline training run from a popular model or benchmark.
For example, this could be code that trains a small transformer on the works of Shakespeare ([Karpathy, 2022](#bib.bib49)), a classic proof-of-concept training run from natural language processing that completes within a few minutes.
The AI Scientist is then free to explore any possible research direction.
The template also includes a LaTeX folder that contains style files and section headers, along with simple plotting code.
We provide further details on the templates in [Section 6](#S6 "6 Experiments ‣ The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery"), but in general, each run starts with a representative small-scale experiment relevant to the topic area.
The focus on small-scale experiments is not a fundamental limitation of our method, but simply for computational efficiency reasons and compute constraints on our end.
We provide the prompts for all stages in [Appendix A](#A1 "Appendix A Prompts ‣ The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery").

1. Idea Generation.
Given a starting template, The AI Scientist first “brainstorms” a diverse set of novel research directions.
We take inspiration from evolutionary computation and open-endedness research ([Brant and Stanley, 2017](#bib.bib10); [Lehman et al., 2008](#bib.bib58); [Stanley et al., 2017](#bib.bib96); [Stanley, 2019](#bib.bib94)) and iteratively grow an archive of ideas using LLMs as the mutation operator ([Zhang et al., 2024](#bib.bib112); [Faldor et al., 2024](#bib.bib24); [Lu et al., 2024b](#bib.bib70); [Lehman et al., 2022](#bib.bib60)).
Each idea comprises a description, experiment execution plan, and (self-assessed) numerical scores of interestingness, novelty, and feasibility.
At each iteration, we prompt the language model to generate an interesting new research direction conditional on the existing archive, which can include the numerical review scores from completed previous ideas.
We use multiple rounds of chain-of-thought ([Wei et al., 2022](#bib.bib107)) and self-reflection ([Shinn et al., 2024](#bib.bib89)) to refine and develop each idea.
After idea generation, we filter ideas by connecting the language model with the Semantic Scholar API ([Fricke, 2018](#bib.bib28)) and web access as a tool ([Schick et al., 2024](#bib.bib84)).
This allows The AI Scientist to discard any idea that is too similar to existing literature.

2. Experiment Iteration. Given an idea and a template, the second phase of The AI Scientist first executes the proposed experiments and then visualizes its results for the downstream write-up.
The AI Scientist uses Aider to first plan a list of experiments to run and then executes them in order.
We make this process more robust by returning any errors upon a failure or time-out (e.g. experiments taking too long to run) to Aider to fix the code and re-attempt up to four times.

After the completion of each experiment, Aider is then given the results and told to take notes in the style of an experimental journal.
Currently, it only conditions on text but in future versions, this could include data visualizations or any modality.
Conditional on the results, it then re-plans and implements the next experiment.
This process is repeated up to five times.
Upon completion of experiments, Aider is prompted to edit a plotting script to create figures for the paper using Python.
The AI Scientist makes a note describing what each plot contains, enabling the saved figures and experimental notes to provide all the information required to write up the paper.
At all steps, Aider sees its history of execution.

Note that, in general, the provided initial seed plotting and experiment templates are small, self-contained files. The AI Scientist frequently implements entirely new plots and collects new metrics that are not in the seed templates. This ability to arbitrarily edit the code occasionally leads to unexpected outcomes ([Section 8](#S8 "8 Limitations & Ethical Considerations ‣ The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery")).

3. Paper Write-up.
The third phase of The AI Scientist produces a concise and informative write-up of its progress in the style of a standard machine learning conference proceeding in LaTeX.
We note that writing good LaTeX can even take competent human researchers some time, so we take several steps to robustify the process.
This consists of the following:

1. 1.

   Per-Section Text Generation: The recorded notes and plots are passed to Aider, which is prompted to fill in a blank conference template section by section.
   This goes in order of introduction, background, methods, experimental setup, results, and then the conclusion (all sections apart from the related work).
   All previous sections of the paper it has already written are in the context of the language model.
   We include brief tips and guidelines on what each section should include, based on the popular [“How to ML Paper” guide](https://docs.google.com/document/d/16R1E2ExKUCP5SlXWHr-KzbVDx9DBUclra-EbU8IB-iE/edit#heading=h.16t67gkeu9dx), and include details in [Section A.3](#A1.SS3 "A.3 Paper Writing ‣ Appendix A Prompts ‣ The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery").
   At each step of writing, Aider is prompted to *only use real experimental results in the form of notes and figures generated from code, and real citations* to reduce hallucination.
   Each section is initially refined with one round of self-reflection ([Shinn et al., 2024](#bib.bib89)) as it is being written.
   Aider is prompted to not include any citations in the text at this stage, and fill in only a skeleton for the related work, which will be completed in the next stage.
2. 2.

   Web Search for References: In a similar vein to idea generation, The AI Scientist is allowed 20 rounds to poll the Semantic Scholar API looking for the most relevant sources to compare and contrast the near-completed paper against for the related work section.
   This process also allows The AI Scientist to select any papers it would like to discuss and additionally fill in any citations that are missing from other sections of the paper.
   Alongside each selected paper, a short description is produced of where and how to include the citation, which is then passed to Aider.
   The paper’s bibtex is automatically appended to the LaTeX file to guarantee correctness.
3. 3.

   Refinement: After the previous two stages, The AI Scientist has a completed first draft, but can often be overly verbose and repetitive.
   To resolve this, we perform one final round of self-reflection section-by-section, aiming to remove any duplicated information and streamline the arguments of the paper.
4. 4.

   Compilation: Once the LaTeX template has been filled in with all the appropriate results, this is fed into a LaTeX compiler.
   We use a LaTeX linter and pipe compilation errors back into Aider so that it can automatically correct any issues.

## 4 Automated Paper Reviewing

An LLM Reviewer Agent. A key component of an effective scientific community is its reviewing system, which evaluates and improves the quality of scientific papers.
To mimic such a process using large language models, we design a GPT-4o-based agent ([OpenAI, 2023](#bib.bib79)) to conduct paper reviews based on the Neural Information Processing Systems (NeurIPS) conference [review guidelines](https://neurips.cc/Conferences/2022/ReviewerGuidelines).
The review agent processes the raw text of the PDF manuscript using the PyMuPDF parsing library.
The output contains numerical scores (soundness, presentation, contribution, overall, confidence), lists of weaknesses and strengths as well as a preliminary binary decision (accept or reject).
These decisions may then be post-calibrated by thresholding using the reviewer score.
We leverage this automated reviewing process to obtain an initial evaluation of the papers generated by The AI Scientist.
We provide the entire reviewing prompt template in [Section A.4](#A1.SS4 "A.4 Paper Reviewing ‣ Appendix A Prompts ‣ The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery").

Table 1: Performance of The AI Scientist’s automated LLM reviewing system on 500 ICLR 2022 papers. We show mean and 95% bootstrap confidence intervals, and highlight the comparison between the human baseline and our best AI reviewer.

|  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  | Reviewer | Balanced Acc. ↑\uparrow | Accuracy ↑\uparrow | F1 Score ↑\uparrow | AUC ↑\uparrow | FPR ↓\downarrow | FNR ↓\downarrow |
|  | Human (NeurIPS)11 1 Numbers are calculated based of the NeurIPS consistency experiment ([Beygelzimer et al., 2021](#bib.bib8)). | 0.66\mathbf{0.66} | 0.73\mathbf{0.73} | 0.49\mathbf{0.49} | 0.65\mathbf{0.65} | 0.17\mathbf{0.17} | 0.52\mathbf{0.52} |
|  | Random Decision | 0.500.50 | 0.500.50 | 0.400.40 | 0.500.50 | 0.500.50 | 0.500.50 |
|  | Always Reject | 0.500.50 | 0.590.59 | 0.000.00 | 0.500.50 | 0.000.00 | 1.001.00 |
| Uncalibrated | Sonnet 3.5 | 0.52±0.010.52\pm 0.01 | 0.40±0.010.40\pm 0.01 | 0.55±0.010.55\pm 0.01 | 0.52±0.010.52\pm 0.01 | 0.95±0.020.95\pm 0.02 | 0.00±0.000.00\pm 0.00 |
| GPT-4o-mini | 0.53±0.020.53\pm 0.02 | 0.65±0.010.65\pm 0.01 | 0.11±0.060.11\pm 0.06 | 0.53±0.020.53\pm 0.02 | 0.01±0.010.01\pm 0.01 | 0.94±0.040.94\pm 0.04 |
| GPT-4o (0-shot) | 0.61±0.040.61\pm 0.04 | 0.68±0.030.68\pm 0.03 | 0.43±0.070.43\pm 0.07 | 0.61±0.040.61\pm 0.04 | 0.11±0.030.11\pm 0.03 | 0.67±0.070.67\pm 0.07 |
| GPT-4o (1-shot) | 0.60±0.030.60\pm 0.03 | 0.70±0.03\mathbf{0.70\pm 0.03} | 0.37±0.080.37\pm 0.08 | 0.60±0.030.60\pm 0.03 | 0.04±0.020.04\pm 0.02 | 0.76±0.060.76\pm 0.06 |
| Calibrated | Sonnet 3.5 @8 | 0.59±0.040.59\pm 0.04 | 0.65±0.040.65\pm 0.04 | 0.45±0.060.45\pm 0.06 | 0.59±0.040.59\pm 0.04 | 0.20±0.040.20\pm 0.04 | 0.61±0.070.61\pm 0.07 |
| GPT-4o-mini @6 | 0.59±0.040.59\pm 0.04 | 0.64±0.040.64\pm 0.04 | 0.45±0.060.45\pm 0.06 | 0.59±0.040.59\pm 0.04 | 0.22±0.050.22\pm 0.05 | 0.60±0.070.60\pm 0.07 |
| GPT-4o (0-shot) @6 | 0.63±0.040.63\pm 0.04 | 0.63±0.040.63\pm 0.04 | 0.56±0.050.56\pm 0.05 | 0.63±0.040.63\pm 0.04 | 0.38±0.050.38\pm 0.05 | 0.36±0.070.36\pm 0.07 |
| GPT-4o (1-shot) @6 | 0.65±0.04\mathbf{0.65\pm 0.04} | 0.66±0.04\mathbf{0.66\pm 0.04} | 0.57±0.05\mathbf{0.57\pm 0.05} | 0.65±0.04\mathbf{0.65\pm 0.04} | 0.31±0.05\mathbf{0.31\pm 0.05} | 0.39±0.07\mathbf{0.39\pm 0.07} |

Evaluating the Automated Reviewer.
To evaluate the LLM-based reviewer’s performance, we compared the artificially generated decisions with ground truth data for 500 ICLR 2022 papers extracted from the publicly available OpenReview dataset ([Berto, 2024](#bib.bib7)).
Similar to the previous section, we combine many recent advancements in LLM agents to make the decision-making process robust.
More specifically, we improve the base LLM’s decision-making process by leveraging self-reflection ([Shinn et al., 2024](#bib.bib89)), providing few-shot examples ([Wei et al., 2022](#bib.bib107)) and response ensembling ([Wang et al., 2022](#bib.bib105)).
With GPT-4o, The AI Scientist’s reviewing procedure achieves 70% accuracy when combining 5 rounds of self-reflection, 5 ensembled reviews, and a 1-shot review example taken from the ICLR 2022 [review guidelines](https://iclr.cc/Conferences/2022/ReviewerGuide). Afterward, we perform an LLM-based meta-review, which prompts the agent to act as an Area Chair ([Wang et al., 2022](#bib.bib105)) (full prompts in [Section A.4](#A1.SS4 "A.4 Paper Reviewing ‣ Appendix A Prompts ‣ The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery")).
While this number is lower than the 73% accuracy that was reported for humans in the NeurIPS 2021 consistency experiment ([Beygelzimer et al., 2021](#bib.bib8)), the automated reviewer achieves superhuman F1 Scores (0.57 vs. 0.49) and human-level AUC (0.65 for both) when thresholding the decision at a score of 6 (a “Weak Accept” in the NeurIPS review guidelines). This choice corresponds roughly to the average score of accepted papers.

The considered ICLR 2022 paper dataset is very class-imbalanced, i.e. it contains many more rejected papers. When considering a balanced dataset of papers, The AI Scientist’s reviewing process achieves human-level accuracy (0.65% vs. 0.66%). Furthermore, the False Negative Rate (FNR) is much lower than the human baseline (0.39 vs. 0.52).
Hence, the LLM-based review agent rejects fewer high-quality papers.
The False Positive Rate (FNR), on the other hand, is higher (0.31 vs. 0.17) highlighting room for potential future improvements.

To further validate the performance of the automated reviewer, we compare the consistency of the overall paper scores between anonymous OpenReview reviewers randomly sampled pairwise per paper ([Figure 2](#S4.F2 "In 4 Automated Paper Reviewing ‣ The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery"), bottom-left) and between the average of all reviewers and the LLM score ([Figure 2](#S4.F2 "In 4 Automated Paper Reviewing ‣ The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery"), bottom-middle).
For the set of 500 ICLR 2022 papers, we find that the correlation between the score of two human reviewers is smaller (0.14) than the correlation between the LLM score and the average score across the reviewers (0.18).
Overall, across all metrics, the results suggest that LLM-based reviews can not only provide valuable feedback ([D’Arcy et al., 2024](#bib.bib19)) but also align more closely with the average human reviewer score than individual human reviewers align with each other.

Each review is generated for $0.25 to $0.50 in API costs. We additionally compared the reviewing performance of various other foundation models.
While Claude Sonnet 3.5 ([Anthropic, 2024](#bib.bib4)) and GPT-4o-mini provide a more cost-efficient approach, their performance was substantially worse ([Table 1](#S4.T1 "In 4 Automated Paper Reviewing ‣ The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery")).
Moreover, we had to threshold scores at 8 for Sonnet 3.5 to obtain calibrated results, due to persistent over-optimism bias.
Llama 3.1 405B ([Llama Team, 2024](#bib.bib66)) struggled to follow the reviewer output template consistently.
We open-source our code, providing a new and interesting LLM benchmark for the community.

![Refer to caption](2408.06292v3/figures/review_confusion.png)

![Refer to caption](2408.06292v3/figures/review_correlation.png)

Figure 2: Evaluation of The AI Scientist’s paper reviewing process on ICLR 2022 OpenReview Data using GPT-4o. Adding Reflexion and one-shot prompting improves the accuracy of the LLM-Based Reviewing Process. Review ensembling (5 reviews) and subsequent meta-aggregation, on the other hand, did not affect the reviewer’s performance, but can reduce variance.

LLM Reviewer Ablations.
We compare various prompt configurations for GPT-4o and find that both Reflexion (+2%) and one-shot prompting (+2%) substantially help with performing more accurate reviewing ([Figure 2](#S4.F2 "In 4 Automated Paper Reviewing ‣ The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery"), top and bottom-right).
On the other hand, using review ensembling does not appear to improve the reviewer’s performance substantially but can reduce variance.
In the following sections, we used our best overall reviewer:
GPT-4o with 5 rounds of self-reflection, 5 ensembled reviews, a meta-aggregation step, and 1 few-shot example.

## 5 In-Depth Case Study

Before we present extensive experiments and metrics for The AI Scientist’s generated papers in [Section 6](#S6 "6 Experiments ‣ The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery"), we first visualize a representative sample from a run of the The AI Scientist which illustrates both its strengths and shortcomings, followed by a broader discussion of its potential.
The selected paper “Adaptive Dual-Scale Denoising” is generated from a run where The AI Scientist is asked to do research on diffusion modeling, which is fully detailed in [Section 6.1](#S6.SS1 "6.1 Diffusion Modeling ‣ 6 Experiments ‣ The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery").
The base foundation model was Claude Sonnet 3.5 ([Anthropic, 2024](#bib.bib4)).

Generated Idea.
As discussed in [Section 3](#S3 "3 The AI Scientist ‣ The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery"), The AI Scientist first generates an idea based on the provided template and its previous archive of discoveries.
The idea in the selected paper was proposed in the 6th iteration of the algorithm and aims to improve the ability of diffusion models to capture both global structure and local details in a 2D dataset, by proposing two branches in the standard denoiser network.
This is a well-motivated direction that has been the primary reason for researchers adopting diffusion models over prior styles of generative models such as VAEs ([Kingma and Welling, 2014](#bib.bib51)) and GANs ([Goodfellow et al., 2014](#bib.bib33)), and to the best of our knowledge has not been widely studied.

We highlight that The AI Scientist generates an impressive experimental plan that includes *the proposed code modification, comparison to baselines, evaluation metrics, and the design of additional plots*.
As has been previously observed in the literature, judgments by LLMs can often have bias ([Zheng et al., 2024](#bib.bib113)) which we can observe in over-estimation of an idea’s interestingness, feasibility, or novelty.
The “novel” flag at the end indicates The AI Scientist believes the idea is novel after searching for related papers using the Semantic Scholar API.

Idea - adaptive_dual_scale_denoising

```
"Name": "adaptive_dual_scale_denoising",
"Title": "Adaptive Dual-Scale Denoising for Dynamic Feature Balancing in
Low-Dimensional Diffusion Models",
"Experiment": "Modify MLPDenoiser to implement a dual-scale processing
approach with two parallel branches: a global branch for the original input
and a local branch for an upscaled input. Introduce a learnable, timestep-
conditioned weighting factor to dynamically balance the contributions of
global and local branches. Train models with both the original and new
architecture on all datasets. Compare performance using KL divergence and
visual inspection of generated samples. Analyze how the weighting factor
evolves during the denoising process and its impact on capturing global
structure vs. local details across different datasets and timesteps.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 8,
"novel": true
```

Generated Experiments.
We display the generated code diff (deletions are in red, and additions are in green) for the substantial algorithmic changes below.
The code matches the experimental description and is well-commented.
The AI Scientist is able to iterate on the code with results from intermediate experiments in the loop, and it eventually ends up with interesting design choices for the adaptive weight network, e.g. a LeakyReLU.
Importantly, this network has a well-behaved output that is guaranteed to be between 0 and 1.
We additionally note that The AI Scientist changed the output of the network to return the adaptive weights to make new visualizations.

Generated Paper.
The AI Scientist generates an 11-page scientific manuscript in the style of a standard machine learning conference submission complete with visualizations and all standard sections.
We display a preview of the completely AI-generated paper in [Figure 3](#S5.F3 "In 5 In-Depth Case Study ‣ The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery"), with the full-sized version available in [Section D.1](#A4.SS1 "D.1 DualScale Diffusion: Adaptive Feature Balancing for Low-Dimensional GenerativeModels ‣ Appendix D Highlighted Generated Papers ‣ The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery").

![Refer to caption](2408.06292v3/all_pages.png)

Figure 3: Preview of the “Adaptive Dual-Scale Denoising” paper which was entirely autonomously generated by The AI Scientist. The full paper can be viewed in [Section D.1](#A4.SS1 "D.1 DualScale Diffusion: Adaptive Feature Balancing for Low-Dimensional GenerativeModels ‣ Appendix D Highlighted Generated Papers ‣ The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery")

We highlight specific things that were particularly impressive in the paper:

- •

  Precise Mathematical Description of the Algorithm. The algorithmic changes in the code above are described precisely, with new notation introduced where necessary, using LaTeX math packages. The overall training process is also described exactly.
- •

  Comprehensive Write-up of Experiments. The hyperparameters, baselines, and datasets are listed in the paper. As an essential sanity check, we verified that the main numerical results in Table 1 of the generated paper exactly match the experimental logs. Impressively, while the recorded numbers are in long-form floats, The AI Scientist chooses to round them all to 3 decimal places without error. Even more impressively, the results are accurately compared to the baseline (e.g. 12.8% reduction in KL on the dinosaur dataset).
- •

  Good Empirical Results. Qualitatively, the sample quality looks much improved from the baseline. Fewer points are greatly out-of-distribution with the ground truth. Quantitatively, there are improvements to the approximate KL divergence between true and estimated distribution.
- •

  New Visualizations. While we provided some baseline plotting code for visualizing generated samples and the training loss curves, it came up with novel algorithm-specific plots displaying the progression of weights throughout the denoising process.
- •

  Interesting Future Work Section. Building on the success of the current experiments, the future work section lists relevant next steps such as scaling to higher-dimensional problems, more sophisticated adaptive mechanisms, and better theoretical foundations.

On the other hand, there are also pathologies in this paper:

- •

  Subtle Error in Upscaling Network. While a linear layer upscales the input to the denoiser network, only the first two dimensions are being used for the “local” branch, leading this upscaling layer to be a linear layer that preserves the same dimensionality effectively.
- •

  Hallucination of Experimental Details. The paper claims that V100 GPUs were used, even though the agent couldn’t have known the actual hardware used. In reality, H100 GPUs were used. It also guesses the PyTorch version without checking.
- •

  Positive Interpretation of Results. The paper tends to take a positive spin even on its negative results, which leads to slightly humorous outcomes. For example, while it summarizes its positive results as: “Dino: 12.8% reduction (from 0.989 to 0.862)” (lower KL is better), the negative results are reported as “Moons: 3.3% improvement (from 0.090 to 0.093)”. Describing a negative result as an improvement is certainly a stretch of the imagination.
- •

  Artifacts from Experimental Logs. While each change to the algorithm is usually descriptively labeled, it occasionally refers to results as “Run 2”, which is a by-product from its experimental log and should not be presented as such in a professional write-up.
- •

  Presentation of Intermediate Results. The paper contains results for every single experiment that was run. While this is useful and insightful for us to see the evolution of the idea during execution, it is unusual for standard papers to present intermediate results like this.
- •

  Minimal References. While additional references have been sourced from Semantic Scholar, including two papers in the related work that are very relevant comparisons, overall the bibliography is small at only 9 entries.

Review.
The automated reviewer points out valid concerns in the generated manuscript.
The review recognizes the experiments were with simple, 2D datasets only, however, this is because we externally constrained the system to use these datasets, and in its current form, The AI Scientist cannot download higher-dimensional datasets from the internet.
On the other hand, limitations such as the proposed algorithm’s increased computational cost of the algorithm are mentioned in the actual paper, which shows that The AI Scientist is often up-front about the drawbacks of its idea.
The reviewer also lists many relevant questions about the paper, such as: explaining the variability of performance across datasets, and explaining in more detail how the upscaling process affects the local branch’s input.

Review - adaptive_dual_scale_denoising

```
"Summary": "The paper introduces an adaptive dual-scale denoising approach
for low-dimensional diffusion models, aiming to balance global structure
and local details in generated samples. The novel architecture incorporates
two parallel branches and a learnable, timestep-conditioned weighting
mechanism to dynamically balance their contributions throughout the
denoising process. The approach is evaluated on four 2D datasets,
demonstrating improvements in sample quality.",
"Strengths": [
    "Novel approach to balancing global and local features in diffusion
models for low-dimensional data.",
    "Comprehensive empirical evaluation on multiple 2D datasets.",
    "Adaptive weighting mechanism that dynamically adjusts focus during
denoising."
],
"Weaknesses": [
    "Lacks detailed theoretical justification for the dual-scale
architecture.",
    "Computational cost is significantly higher, which may limit practical
applicability.",
    "Some sections are not clearly explained, such as the autoencoder
aggregator and weight evolution analysis.",
    "Limited diversity in the datasets used for evaluation. More complex,
real-world datasets could strengthen claims.",
    "Insufficient ablation studies and analysis on specific design choices
like different types of aggregators."
],
"Originality": 4,
"Quality": 3,
"Clarity": 3,
"Significance": 3,
"Questions": [
    "Can you provide a more detailed theoretical justification for the
dual-scale architecture?",
    "What impact do different types of aggregators have on the model’s
performance?",
    "How does the model perform on more complex, real-world low-dimensional
datasets?",
    "Can the computational cost be reduced without sacrificing
performance?"
],
"Limitations": [
    "The paper should address the high computational cost and explore ways
to optimize it.",
    "The limited diversity of datasets and lack of detailed theoretical
backing for the proposed architecture are notable limitations."
],
"Ethical Concerns": false,
"Soundness": 3,
"Presentation": 3,
"Contribution": 3,
"Overall": 5,
"Confidence": 4,
"Decision": "Reject"
```

Final Comments.
Drawing from our domain knowledge in diffusion modeling—which, while not our primary research focus, is an area in which we have published papers—we present our overall opinions on the paper generated by The AI Scientist below.

- •

  The AI Scientist correctly identifies an interesting and well-motivated direction in diffusion modeling research, e.g. previous work has studied modified attention mechanisms ([Hatamizadeh et al., 2024](#bib.bib35)) for the same purpose in higher-dimensional problems. It proposes a comprehensive experimental plan to investigate its idea, and successfully implements it all, achieving good results. We were particularly impressed at how it responded to subpar earlier results and iteratively adjusted its code (e.g. refining the weight network). The full progression of the idea can be viewed in the paper.
- •

  While the paper’s idea improves performance and the quality of generated diffusion samples, the reasons for its success may not be as explained in the paper.
  In particular, there is no obvious inductive bias beyond an upscaling layer (effectively just an additional linear layer) for the splitting of global or local features.
  However, we do see progression in weights (and thus a preference for the global or local branch) across diffusion timesteps which suggests that something non-trivial is happening.
  Our interpretation is instead that the network that The AI Scientist has implemented for this idea resembles a mixture-of-expert (MoE, [Yuksel et al. (2012)](#bib.bib111); [Fedus et al. (2022)](#bib.bib27)) structure that is prevalent across LLMs ([Jiang et al., 2024](#bib.bib45)).
  An MoE could indeed lead to the diffusion model learning separate branches for global and local features, as the paper claims, but this statement requires more rigorous investigation.
- •

  Interestingly, the true shortcomings of this paper described above certainly require some level of domain knowledge to identify and were only partially captured by the automated reviewer (i.e., when asking for more details on the upscaling layer).
  At the current capabilities of The AI Scientist, this can be resolved by human feedback.
  However, future generations of foundation models may propose ideas that are challenging for humans to reason about and evaluate.
  This links to the field of “superalignment” ([Burns et al., 2023](#bib.bib13)) or supervising AI systems that may be smarter than us, which is an active area of research.
- •

  Overall, we judge the performance of The AI Scientist to be about the level of an early-stage ML researcher who can competently execute an idea but may not have the full background knowledge to fully interpret the reasons behind an algorithm’s success. If a human supervisor was presented with these results, a reasonable next course of action could be to advise The AI Scientist to re-scope the project to further investigate MoEs for diffusion.
  Finally, we naturally expect that many of the flaws of the The AI Scientist will improve, if not be eliminated, as foundation models continue to improve dramatically.

## 6 Experiments

We extensively evaluate The AI Scientist on three templates (as described in [Section 3](#S3 "3 The AI Scientist ‣ The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery")) across different publicly available LLMs: Claude Sonnet 3.5 ([Anthropic, 2024](#bib.bib4)), GPT-4o ([OpenAI, 2023](#bib.bib79)), DeepSeek Coder ([Zhu et al., 2024](#bib.bib114)), and Llama-3.1 405b ([Llama Team, 2024](#bib.bib66)).
The first two models are only available by a public API, whilst the second two models are open-weight.
For each run, we provide 1-2 basic seed ideas as examples (e.g. modifying the learning rate or batch size) and have it generate another 50 new ideas.
We visualize an example progression of proposed ideas in [Appendix C](#A3 "Appendix C Progression of Generated Ideas ‣ The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery").
Each run of around fifty ideas in total takes approximately 12 hours on 8×8\times NVIDIA H100s22
2
Note that the experiment templates are very small-scale and are not compute-intensive. They would likely take a similar amount of time on cheaper GPUs, as we do not achieve high utilization..
We report the number of ideas that pass the automated novelty check, successfully complete experiments, and result in valid compilable manuscripts. Note that the automated novelty check and search are self-assessed by each model for its own ideas, making relative “novelty” comparisons challenging.
Additionally, we provide the mean and max reviewer scores of the generated papers and the total cost of the run.
Finally, we select and briefly analyze some of the generated papers, which are listed below.
The full papers can be found in [Appendix D](#A4 "Appendix D Highlighted Generated Papers ‣ The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery"), alongside the generated reviews and code.

In practice, we make one departure from the formal description of The AI Scientist, and generate ideas without waiting for paper evaluations to be appended to the archive in order to parallelize more effectively.
This allowed us to pay the cost of the idea generation phase only once and iterate faster; furthermore, we did not observe any reduction in the quality of the papers generated as measured by the average review score with this modification.

Table 2: 10 selected papers generated by The AI Scientist across 3 different templates, together with scores from our automated reviewer corresponding to the [NeurIPS guidelines](https://neurips.cc/Conferences/2022/ReviewerGuidelines). The average accepted paper at NeurIPS has a score of around 6 from human evaluation.

| Type | Paper Title | Score |
| --- | --- | --- |
| 2D Diffusion | DualScale Diffusion: Adaptive Feature Balancing for Low-Dimensional Generative Models | 𝟓\mathbf{5} |
| 2D Diffusion | Multi-scale Grid Noise Adaptation: Enhancing Diffusion Models For Low-dimensional Data | 𝟒\mathbf{4} |
| 2D Diffusion | GAN-Enhanced Diffusion: Boosting Sample Quality and Diversity | 𝟑\mathbf{3} |
| 2D Diffusion | DualDiff: Enhancing Mode Capture in Low-dimensional Diffusion Models via Dual-expert Denoising | 𝟓\mathbf{5} |
| NanoGPT | StyleFusion: Adaptive Multi-style Generation in Character-Level Language Models | 𝟓\mathbf{5} |
| NanoGPT | Adaptive Learning Rates for Transformers via Q-Learning | 𝟑\mathbf{3} |
| Grokking | Unlocking Grokking: A Comparative Study of Weight Initialization Strategies in Transformer Models | 𝟓\mathbf{5} |
| Grokking | Grokking Accelerated: Layer-wise Learning Rates for Transformer Generalization | 𝟒\mathbf{4} |
| Grokking | Grokking Through Compression: Unveiling Sudden Generalization via Minimal Description Length | 𝟑\mathbf{3} |
| Grokking | Accelerating Mathematical Insight: Boosting Grokking Through Strategic Data Augmentation | 𝟓\mathbf{5} |

From manual inspection, we find that Claude Sonnet 3.5 consistently produces the highest quality papers, with GPT-4o coming in second. We provide a link to all papers, run files, and logs in our [GitHub repository](https://github.com/SakanaAI/AI-Scientist), and recommend viewing the uploaded Claude papers for a qualitative analysis.
This observation is also validated by the scores obtained from the LLM reviewer ([Figure 4](#S6.F4 "In 6 Experiments ‣ The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery")).
When dividing the number of generated papers by the total cost, we end up at a cost of around $10-15 per paper.
Notably, GPT-4o struggles with writing LaTeX, which prevents it from completing many of its papers.
For the open-weight models, DeepSeek Coder is significantly cheaper but often fails to correctly call the Aider tools.
Llama-3.1 405b performed the worst overall but was the most convenient to work with, as we were frequently rate-limited by other providers.
Both DeepSeek Coder and Llama-3.1 405b often had missing sections and results in their generated papers.
In the following subsections, we will describe each template, its corresponding results, and specific papers.

![Refer to caption](2408.06292v3/figures/scores_ai_papers.png)

Figure 4: Violin plots showing the distribution of scores generated by the The AI Scientist reviewer for AI-generated papers across three domains and four foundation models. Scores on the y-axis refer to [NeurIPS ratings](https://neurips.cc/Conferences/2022/ReviewerGuidelines), which range from 2 (Strong Reject) to 6 (Weak Accept).

### 6.1 Diffusion Modeling

Table 3: Evaluation of automated AI Scientist paper generation for Diffusion Modeling.

|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | |  | | --- | | Total | | Ideas | | |  | | --- | | Novel | | Ideas | | |  | | --- | | Experiments | | Passed | | |  | | --- | | Completed | | Papers | | |  | | --- | | Mean | | Score | | |  | | --- | | Max | | Score | | |  | | --- | | Total | | Cost | |
| Sonnet 3.5 | 51 | 49 | 38 | 38 | 3.82 | 6.0 | ∼\sim$250 |
| GPT-4o | 51 | 41 | 17 | 16 | 3.70 | 5.0 | ∼\sim$300 |
| DeepSeek Coder | 51 | 42 | 32 | 31 | 3.32 | 5.0 | ∼\sim$10 |
| Llama-3.1 405b | 51 | 31 | 21 | 21 | 2.30 | 3.0 | ∼\sim$120 |

General Description: This template studies improving the performance of diffusion generative models ([Sohl-Dickstein et al., 2015](#bib.bib91); [Ho et al., 2020](#bib.bib38)) on low-dimensional datasets.
Compared to image generation, low-dimensional diffusion is much less well-studied, and thus there may be interesting algorithmic contributions to be made here.

Code Template:
We base this template on a modified version of the popular ‘tanelp/tiny-diffusion’ repository ([Pärnamaa, 2023](#bib.bib80)) with additional minor hyperparameter tuning added and exponential moving average on the weights.
The diffusion models are DDPM ([Ho et al., 2020](#bib.bib38)) models trained to generate samples from four distributions including geometric shapes, the two moons dataset, and a 2D dinosaur.
The denoiser network is parameterized as an MLP with sinusoidal embeddings for the diffusion timestep and input data.
The plotting script visualizes generated samples and plots training loss by default.
Estimated KL is provided as an additional metric for sample quality via non-parametric entropy estimation.

Highlighted Generated Paper 1:
[DualScale Diffusion: Adaptive Feature Balancing for Low-Dimensional Generative Models.](#A4.SS1 "D.1 DualScale Diffusion: Adaptive Feature Balancing for Low-Dimensional GenerativeModels ‣ Appendix D Highlighted Generated Papers ‣ The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery")
We analyze this paper in-depth in [Section 5](#S5 "5 In-Depth Case Study ‣ The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery").
This paper proposes a dual-scale denoising approach that splits the traditional diffusion denoiser into a global and a local processing branch.
The network input is upscaled before being fed into the local branch.
The outputs of the branches are then combined using a learnable time-conditioned weighting.
It achieves impressive quantitative and qualitative results.
It further manages to plot the evolution of the weighting across time, which requires very significant deviation from the provided code.

Highlighted Generated Paper 2: [Multi-scale Grid Noise Adaptation: Enhancing Diffusion Models For Low-dimensional Data.](#A4.SS2 "D.2 Multi-scale Grid Noise Adaptation: Enhancing Diffusion Models For Low-dimensional Data ‣ Appendix D Highlighted Generated Papers ‣ The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery")
This paper proposes to dynamically scale the standard diffusion noise schedule with a learned multiplicative factor based on where a particular input is in 2D space.
The multiplicative factor is set by two grids that cover the input space, one coarse 5x5 grid and one more fine-grained 20x20 grid.
This creative approach allows the diffusion model to dramatically improve performance across the datasets.

Highlighted Generated Paper 3: [GAN-Enhanced Diffusion: Boosting Sample Quality and Diversity.](#A4.SS3 "D.3 Gan-Enhanced Diffusion: Boosting Sample Quality and Diversity ‣ Appendix D Highlighted Generated Papers ‣ The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery")
This paper, inspired by GANs, proposes adding a discriminator to the diffusion model to guide the generation.
It achieves comparable quantitative performance to the baseline, however, the final generated figures appear to have fewer out-of-distribution points.
This is notable as the current version of The AI Scientist is unable to view them (a problem that can be remedied by using multi-modal models in the future).

Highlighted Generated Paper 4: [DualDiff: Enhancing Mode Capture in Low-dimensional Diffusion Models via Dual-expert Denoising.](#A4.SS4 "D.4 DualDiff: Enhancing Mode Capture in Low-dimensional Diffusion Models via Dual-expert Denoising ‣ Appendix D Highlighted Generated Papers ‣ The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery")
This paper proposes a similar idea to our first highlighted diffusion paper, also studying a mixture of experts style network for low-dimensional diffusion models.
However, this idea evolves differently, with the standard diffusion loss now being augmented with a loss that encourages diversity in the two experts.
The paper impressively visualizes the impact of the diversity loss in distributing inputs across both experts and further color-codes which parts of the sample space each expert is specialized in.
We were particularly impressed by The AI Scientist’s ability to perform a radically different take on a similar idea.

### 6.2 Language Modeling

Table 4: Evaluation of automated AI Scientist paper generation for Language Modeling.

|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | |  | | --- | | Total | | Ideas | | |  | | --- | | Novel | | Ideas | | |  | | --- | | Experiments | | Passed | | |  | | --- | | Completed | | Papers | | |  | | --- | | Mean | | Score | | |  | | --- | | Max | | Score | | |  | | --- | | Total | | Cost | |
| Sonnet 3.5 | 52 | 50 | 20 | 20 | 4.05 | 5.0 | ∼\sim$250 |
| GPT-4o | 52 | 44 | 30 | 16 | 3.25 | 5.0 | ∼\sim$300 |
| DeepSeek Coder | 52 | 37 | 23 | 23 | 3.21 | 4.0 | ∼\sim$10 |
| Llama-3.1 405b | 52 | 41 | 21 | 21 | 2.31 | 3.0 | ∼\sim$120 |

General Description: This template investigates transformer-based ([Vaswani et al., 2017](#bib.bib99)) autoregressive next-token prediction tasks. Because this task is widely studied and optimized, it is difficult for The AI Scientist to find significant improvements. There are some common failure modes for this template that result in impressive-looking, but deceptive results. For example, a few of its ideas effectively cheat by subtly leaking information from future tokens, which results in lower perplexity.

Code Template:
The code is modified from the popular NanoGPT repository ([Karpathy, 2022](#bib.bib49)). The provided script template trains a small transformer language model on the character-level Shakespeare dataset ([Karpathy, 2015](#bib.bib48)), the enwik8 dataset ([Hutter, 2006](#bib.bib42)), and the text8 dataset ([Mahoney, 2011](#bib.bib72)). It runs three seeds on the Shakespeare dataset, and one each on the remaining ones. The code saves the runtime, validation losses, and train losses. The plotting script visualizes training curves by default.

Highlighted Generated Paper 1: [StyleFusion: Adaptive Multi-style Generation in Character-Level Language Models.](#A4.SS5 "D.5 StyleFusion: Adaptive Multi-style Generation in Character-Level Language Models ‣ Appendix D Highlighted Generated Papers ‣ The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery")
This paper proposes an architectural change to the model, in which a learned per-token “style adapter” modulates the Transformer state at each layer. The method achieves strong results and deserves further investigation, though we suspect that one reason it may work is that it is simply adding more parameters, which may trivialize the result.
Furthermore, it omits some important implementation details in the writing, such as how the style loss labels are derived (which appear to be randomly assigned on each update step).

Highlighted Generated Paper 2: [Adaptive Learning Rates in Transformers via Q-Learning.](#A4.SS6 "D.6 Adaptive Learning Rates for Transformers via Q-Learning ‣ Appendix D Highlighted Generated Papers ‣ The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery")
This paper proposes using a basic online Q-Learning algorithm to adjust the model’s learning rate during training. The state consists of the current learning rate and validation loss, the action applies a small perturbation to the learning rate, and the reward is the negative change in validation loss. While the idea is creative, it seems inappropriate to use simple Q-Learning in this highly non-stationary and partially-observed environment. Nonetheless, it happens to achieve effective results.

### 6.3 Grokking Analysis

Table 5: Evaluation of automated AI Scientist paper generation for Grokking.

|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | |  | | --- | | Total | | Ideas | | |  | | --- | | Novel | | Ideas | | |  | | --- | | Experiments | | Passed | | |  | | --- | | Completed | | Papers | | |  | | --- | | Mean | | Score | | |  | | --- | | Max | | Score | | |  | | --- | | Total | | Cost | |
| Sonnet 3.5 | 51 | 47 | 25 | 25 | 3.44 | 5.0 | ∼\sim$250 |
| GPT-4o | 51 | 51 | 22 | 13 | 2.92 | 3.0 | ∼\sim$300 |
| DeepSeek Coder | 51 | 46 | 38 | 36 | 3.13 | 4.0 | ∼\sim$10 |
| Llama-3.1 405b | 51 | 36 | 30 | 30 | 2.00 | 3.0 | ∼\sim$120 |

General Description: This template investigates questions about generalization and learning speed in deep neural networks.
We follow the classic experimental paradigm reported in [Power et al. (2022)](#bib.bib81) for analyzing “grokking”, a poorly understood phenomenon in which validation accuracy dramatically improves long after the train loss saturates.
We provide code that generates synthetic datasets of modular arithmetic tasks and then trains a Transformer model on them.
Unlike the previous templates, this one is more amenable to open-ended empirical analysis (e.g. what conditions grokking occurs) rather than just trying to improve performance metrics.

Code Template: We base our implementation off of two popular open source re-implementations ([Snell, 2021](#bib.bib90); [May, 2022](#bib.bib74)) of [Power et al. (2022)](#bib.bib81). The code generates four synthetic datasets of modular arithmetic tasks and trains a transformer on each across three random seeds. It returns train losses, validation losses, and the number of update steps required to reach perfect validation accuracy. The plotting scripts visualize the training and validation curves by default.

Highlighted Generated Paper 1: [Unlocking Grokking: A Comparative Study of Weight Initialization Strategies in Transformer Models.](#A4.SS7 "D.7 Unlocking Grokking: A Comparative Study of Weight Initialization Strategies in Transformer Models ‣ Appendix D Highlighted Generated Papers ‣ The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery")
This paper investigates different weight initializations and their impact on grokking.
It finds that Xavier ([Glorot and Bengio, 2010](#bib.bib32)) and Orthogonal weight initializations consistently result in significantly faster grokking on the tasks than the widely-used default baseline weight initializations (Kaiming Uniform and Kaiming Normal). While this is a basic investigation, it provides an interesting result that could be studied in more depth.
The paper also has a creative and catchy title.

Highlighted Generated Paper 2: [Grokking Accelerated: Layer-wise Learning Rates for Transformer Generalization.](#A4.SS8 "D.8 Grokking Accelerated: Layer-wise Learning Rates for Transformer Generalization ‣ Appendix D Highlighted Generated Papers ‣ The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery")
This paper assigns different learning rates to different layers of the Transformer architecture. It finds that increasing the learning rate for higher layers results in significantly faster and more consistent grokking after iterating through different configurations throughout its experiments. It impressively includes the key section of its implementation in the write-up.

Highlighted Generated Paper 3: [Grokking Through Compression: Unveiling Sudden Generalization via Minimal Description Length.](#A4.SS9 "D.9 Grokking Through Compression: Unveiling Sudden Generalization via Minimal Description Length ‣ Appendix D Highlighted Generated Papers ‣ The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery")
This paper investigates potential connections between grokking and Minimal Description Length (MDL). We believe this idea is particularly interesting, though not executed very well. Its method for measuring MDL simply involves counting the number of parameters above a threshold ϵ\epsilon. While this does end up correlating with grokking, it is not analyzed in much depth. The paper could be significantly improved by investigating other estimates of MDL and including basic ablations. Furthermore, The AI Scientist failed to write the Related Works section and hallucinated a plot (Figure 5).

Highlighted Generated Paper 4: [Accelerating Mathematical Insight: Boosting Grokking Through Strategic Data Augmentation.](#A4.SS10 "D.10 Accelerating Mathematical Insight: Boosting Grokking Through Strategic Data Augmentation ‣ Appendix D Highlighted Generated Papers ‣ The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery")
This paper investigates data augmentation techniques for grokking in modular arithmetic. It comes up with valid and creative augmentation techniques (operand reversal and operand negation) and finds that they can significantly accelerate grokking. While it is not surprising that data augmentation can improve generalization, the experiments and ideas seem generally well-executed. However, The AI Scientist once again failed to write the Related Works section. In principle, this failure may be easily remedied by simply running the paper write-up step multiple times.

## 7 Related Work

While there has been a long tradition of automatically optimizing individual parts of the ML pipeline (AutoML, [Hutter et al. (2019)](#bib.bib41); [He et al. (2021)](#bib.bib37)), none come close to the full automation of the entire research process, particularly in communicating obtained scientific insights in an interpretable and general format.

LLMs for Machine Learning Research.
Most closely related to our work are those that use LLMs to assist machine learning research.
[Huang et al. (2024)](#bib.bib40) propose a benchmark for measuring how successfully LLMs can write code to solve a variety of machine learning tasks.
[Lu et al. (2024a)](#bib.bib68) use LLMs to propose, implement, and evaluate new state-of-the-art algorithms for preference optimization.
[Liang et al. (2024)](#bib.bib64) use LLMs to provide feedback on research papers and find that they provide similar feedback to human reviewers, while [Girotra et al. (2023)](#bib.bib31) find that LLMs can consistently produce higher quality ideas for innovation than humans.
[Wang et al. (2024b)](#bib.bib104); [Baek et al. (2024)](#bib.bib6) use LLMs to propose research ideas based on scientific literature search but do not execute them.
[Wang et al. (2024c)](#bib.bib106) automatically writes surveys based on an extensive literature search.
Our work can be seen as the synthesis of all these distinct threads, resulting in a single autonomous open-ended system that can execute the entire machine learning research process.

LLMs for Structured Exploration.
Because LLMs contain many human-relevant priors, they are commonly used as a tool to explore large search spaces.
For example, recent works have used LLM coding capabilities to explore reward functions ([Ma et al., 2023](#bib.bib71); [Yu et al., 2023](#bib.bib110)), virtual robotic design ([Lehman et al., 2023](#bib.bib61)), environment design ([Faldor et al., 2024](#bib.bib24)), and neural architecture search ([Chen et al., 2024a](#bib.bib15)).
LLMs can also act as evaluators ([Zheng et al., 2024](#bib.bib113)) for “interestingness” ([Zhang et al., 2024](#bib.bib112); [Lu et al., 2024b](#bib.bib70)) and as recombination operators for black-box optimization with Evolution Strategies ([Lange et al., 2024](#bib.bib55); [Song et al., 2024](#bib.bib92)) and for Quality-Diversity approaches ([Lim et al., 2024](#bib.bib65); [Bradley et al., 2024](#bib.bib9); [Ding et al., 2024](#bib.bib21)).
Our work combines many of these notions, including that our LLM Reviewer judges papers on novelty and interestingness, and that many proposed ideas are new combinations of previous ones.

AI for Scientific Discovery.
There has been a long tradition of AI assisting scientific discovery ([Langley, 2024](#bib.bib57); [Langley, 1987](#bib.bib56)) across many other fields.
For example, AI has been used for chemistry ([Buchanan and Feigenbaum, 1981](#bib.bib12)), synthetic biology ([Jumper et al., 2021](#bib.bib47); [Hayes et al., 2024](#bib.bib36)), materials discovery ([Pyzer-Knapp et al., 2022](#bib.bib82); [Merchant et al., 2023](#bib.bib75); [Szymanski et al., 2023](#bib.bib97)), mathematics ([Romera-Paredes et al., 2024](#bib.bib83); [Lenat, 1977](#bib.bib62); [Lenat and Brown, 1984](#bib.bib63)), and algorithm search ([Fawzi et al., 2022](#bib.bib26)).
Other works aim to analyze existing pre-collected datasets and find novel insights ([Langley, 1987](#bib.bib56); [Ifargan et al., 2024](#bib.bib43); [Majumder et al., 2024](#bib.bib73); [Yang et al., 2024](#bib.bib109); [Falkenhainer and Michalski, 1986](#bib.bib25); [Zytkow, 1996](#bib.bib116); [Nordhausen and Langley, 1990](#bib.bib77)).
Unlike our work, these are usually restricted to a well-defined search space in a single domain and do not involve “ideation”, writing, or peer review from the AI system.
In its current form, The AI Scientist excels at conducting research ideas implemented via code; with future advances (e.g. robotic automation for wet labs ([Kehoe et al., 2015](#bib.bib50); [Arnold, 2022](#bib.bib5); [Zucchelli et al., 2021](#bib.bib115); [Sparkes et al., 2010](#bib.bib93))), the transformative benefits of our approach could reach across all science, especially as foundation models continue to improve.

## 8 Limitations & Ethical Considerations

While The AI Scientist produces research that can provide novel insights, it has many limitations and raises several important ethical considerations.
We believe future versions of The AI Scientist will be able to address many of its current shortcomings.

Limitations of the Automated Reviewer.
While the automated reviewer shows promising initial results, there are several potential areas for improvement.
The dataset used, from ICLR 2022, is old enough to potentially appear in the base model pre-training data - this is a hard claim to test in practice since typical publicly available LLMs do not share their training data.
However, preliminary analysis showed that LLMs were far from being able to reproduce old reviews exactly from initial segments, which suggests they have not memorized this data.
Furthermore, the rejected papers in our dataset used the original submission file, whereas for the accepted papers only the final camera-ready copies were available on OpenReview.
Future iterations could use more recent submissions (e.g. from TMLR) for evaluation.
Unlike standard reviewers, the automated reviewer is unable to ask questions to the authors in a rebuttal phase, although this could readily be incorporated into our framework.
Finally, since it does not currently use any vision capabilities, The AI Scientist (including the reviewer) is unable to view figures and must rely on textual descriptions of them.

Common Failure Modes. The AI Scientist, in its current form, has several shortcomings in addition to those already identified in [Section 5](#S5 "5 In-Depth Case Study ‣ The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery"). These also include, but are not limited to:

- •

  The idea generation process often results in very similar ideas across different runs and even models. It may be possible to overcome this by allowing The AI Scientist to directly follow up and go deeper on its best ideas, or by providing it content from recently-published papers as a source of novelty.
- •

  As shown in [Tables 3](#S6.T3 "In 6.1 Diffusion Modeling ‣ 6 Experiments ‣ The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery"), [5](#S6.T5 "Table 5 ‣ 6.3 Grokking Analysis ‣ 6 Experiments ‣ The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery") and [4](#S6.T4 "Table 4 ‣ 6.2 Language Modeling ‣ 6 Experiments ‣ The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery"), Aider fails to implement a significant fraction of the proposed ideas. Furthermore, GPT-4o in particular frequently fails to write LaTeX that compiles. While The AI Scientist can come up with creative and promising ideas, they are often too challenging for it to implement.
- •

  The AI Scientist may incorrectly implement an idea, which can be difficult to catch. An adversarial code-checking reviewer may partially address this. As-is, one should manually check the implementation before trusting the reported results.
- •

  Because of The AI Scientist’s limited number of experiments per idea, the results often do not meet the expected rigor and depth of a standard ML conference paper. Furthermore, due to the limited number of experiments we could afford to give it, it is difficult for The AI Scientist to conduct fair experiments that control for the number of parameters, FLOPs, or runtime. This often leads to deceptive or inaccurate conclusions. We expect that these issues will be mitigated as the cost of compute and foundation models continues to drop.
- •

  Since we do not currently use the vision capabilities of foundation models, it is unable to fix visual issues with the paper or read plots. For example, the generated plots are sometimes unreadable, tables sometimes exceed the width of the page, and the page layout (including the overall visual appearance of the paper ([Huang, 2018](#bib.bib39))) is often suboptimal. Future versions with vision and other modalities should fix this.
- •

  When writing, The AI Scientist sometimes struggles to find and cite the most relevant papers. It also commonly fails to correctly reference figures in LaTeX, and sometimes even hallucinates invalid file paths.
- •

  Importantly, The AI Scientist occasionally makes critical errors when writing and evaluating results. For example, it struggles to compare the magnitude of two numbers, which is a known pathology with LLMs. Furthermore, when it changes a metric (e.g. the loss function), it sometimes does not take this into account when comparing it to the baseline. To partially address this, we make sure all experimental results are reproducible, storing copies of all files when they are executed.
- •

  Rarely, The AI Scientist can hallucinate entire results. For example, an early version of our writing prompt told it to always include confidence intervals and ablation studies. Due to computational constraints, The AI Scientist did not always collect additional results; however, in these cases, it would sometimes hallucinate an entire ablations table. We resolved this by instructing The AI Scientist explicitly to only include results it directly observed. Furthermore, it frequently hallucinates facts we do not provide, such as the hardware used.
- •

  More generally, we do not recommend taking the scientific content of this version of The AI Scientist at face value. Instead, we advise treating generated papers as hints of promising ideas for practitioners to follow up on. Nonetheless, we expect the trustworthiness of The AI Scientist to increase dramatically in the coming years in tandem with improvements to foundation models. We share this paper and code primarily to show what is currently possible and hint at what is likely to be possible soon.

Safe Code Execution.
The current implementation of The AI Scientist has minimal direct sandboxing in the code, leading to several unexpected and sometimes undesirable outcomes if not appropriately guarded against. For example, in one run, The AI Scientist wrote code in the experiment file that initiated a system call to relaunch itself, causing an uncontrolled increase in Python processes and eventually necessitating manual intervention. In another run, The AI Scientist edited the code to save a checkpoint for every update step, which took up nearly a terabyte of storage. In some cases, when The AI Scientist’s experiments exceeded our imposed time limits, it attempted to edit the code to extend the time limit arbitrarily instead of trying to shorten the runtime. While creative, the act of bypassing the experimenter’s imposed constraints has potential implications for AI safety ([Lehman et al., 2020](#bib.bib59)). Moreover, The AI Scientist occasionally imported unfamiliar Python libraries, further exacerbating safety concerns. We recommend strict sandboxing when running The AI Scientist, such as containerization, restricted internet access (except for Semantic Scholar), and limitations on storage usage.

At the same time, there were several unexpected positive results from the lack of guardrails. For example, we had forgotten to create the output results directory in the grokking template in our experiments. Each successful run from The AI Scientist that outputted a paper automatically caught this error when it occurred and fixed it. Furthermore, we found that The AI Scientist would occasionally include results and plots that we found surprising, differing significantly from the provided templates. We describe some of these novel algorithm-specific visualizations in [Section 6.1](#S6.SS1 "6.1 Diffusion Modeling ‣ 6 Experiments ‣ The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery").

Broader Impact and Ethical Considerations.
While The AI Scientist has the potential to be a valuable tool for researchers, it also carries significant risks of misuse. The ability to automatically generate and submit papers to academic venues could greatly increase the workload for reviewers, potentially overwhelming the peer review process and compromising scientific quality control. Similar concerns have been raised about generative AI in other fields, such as its impact on the arts ([Epstein et al., 2023](#bib.bib23)). Furthermore, if the Automated Reviewer tool was widely adopted by reviewers, it could diminish the quality of reviews and introduce undesirable biases into the evaluation of papers. Because of this, we believe that papers or reviews that are substantially AI-generated must be marked as such for full transparency.

As with most previous technological advances, The AI Scientist has the potential to be used in unethical ways.
For example, it could be explicitly deployed to conduct unethical research, or even lead to unintended harm if The AI Scientist conducts unsafe research.
Concretely, if it were encouraged to find novel, interesting biological materials and given access to “cloud labs” ([Arnold, 2022](#bib.bib5)) where robots perform wet lab biology experiments, it could (without its overseer’s intent) create new, dangerous viruses or poisons that harm people before we can intervene.
Even in computers, if tasked to create new, interesting, functional software, it could create dangerous malware.
The AI Scientist’s current capabilities, which will only improve, reinforce that the machine learning community needs to immediately prioritize learning how to align such systems to explore in a manner that is safe and consistent with our values.

## 9 Discussion

In this paper, we introduced The AI Scientist, the first framework designed to fully automate the scientific discovery process, and, as a first demonstration of its capabilities, applied it to machine learning itself.
This end-to-end system leverages LLMs to autonomously generate research ideas, implement and execute experiments, search for related works, and produce comprehensive research papers.
By integrating stages of ideation, experimentation, and iterative refinement, The AI Scientist aims to replicate the human scientific process in an automated and scalable manner.

Why does writing papers matter? Given our overarching goal to automate scientific discovery, why are we also motivated to have The AI Scientist write papers, like human scientists? For example, previous AI-enabled systems such as FunSearch ([Romera-Paredes et al., 2024](#bib.bib83)) and GNoME ([Pyzer-Knapp et al., 2022](#bib.bib82)) also conduct impressive scientific discovery in restricted domains, but they do not write papers.

There are several reasons why we believe it is fundamentally important for The AI Scientist to write scientific papers to communicate its discoveries.
First, writing papers offers a highly interpretable method for humans to benefit from what has been learned.
Second, reviewing written papers within the framework of existing machine learning conferences enables us to standardize evaluation.
Third, the scientific paper has been the primary medium for disseminating research findings since the dawn of modern science.
Since a paper can use natural language, and include plots and code, it can flexibly describe any type of scientific study and discovery.
Almost any other conceivable format is locked into a certain kind of data or type of science.
Until a superior alternative emerges (or possibly invented by AI), we believe that training The AI Scientist to produce scientific papers is essential for its integration into the broader scientific community.

Costs. Our framework is remarkably versatile and effectively conducts research across various subfields of machine learning, including transformer-based language modeling, neural network learning dynamics, and diffusion modeling.
The cost-effectiveness of the system, producing papers with potential conference relevance at an approximate cost of $15 per paper, highlights its ability to democratize research (increase its accessibility) and accelerate scientific progress.
Preliminary qualitative analysis, for example in [Section 5](#S5 "5 In-Depth Case Study ‣ The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery"), suggests that the generated papers can be broadly informative and novel, or at least contain ideas worthy of future study.

The actual compute we allocated for The AI Scientist to conduct its experiments in this work is also incredibly light by today’s standards.
Notably, our experiments generating hundreds of papers were largely run only using a single 8×8\timesNVIDIA H100 node over the course of a week.
Massively scaling the search and filtering would likely result in significantly higher-quality papers.

In this project, the bulk of the cost for running The AI Scientist is associated with the LLM API costs for coding and paper writing. In contrast, the costs associated with running the LLM reviewer, as well as the computational expenses for conducting experiments, are negligible due to the constraints we’ve imposed to keep overall costs down. However, this cost breakdown may change in the future if The AI Scientist is applied to other scientific fields or used for larger-scale computational experiments.

Open vs. Closed Models. To quantitatively evaluate and improve the generated papers, we first created and validated an Automated Paper Reviewer.
We show that, although there is significant room for improvement, LLMs are capable of producing reasonably accurate reviews, achieving results comparable to humans across various metrics.
Applying this evaluator to the papers generated by The AI Scientist enables us to scale the evaluation of our papers beyond manual inspection.
We find that Sonnet 3.5 consistently produces the best papers, with a few of them even achieving a score that exceeds the threshold for acceptance at a standard machine learning conference from the Automated Paper Reviewer.

However, there is no fundamental reason to expect a single model like Sonnet 3.5 to maintain its lead.
We anticipate that all frontier LLMs, including open models, will continue to improve.
The competition among LLMs has led to their commoditization and increased capabilities.
Therefore, our work aims to be model-agnostic regarding the foundation model provider.
In this project, we studied various proprietary LLMs, including GPT-4o and Sonnet, but also explored using open models like DeepSeek and Llama-3.
We found that open models offer significant benefits, such as lower costs, guaranteed availability, greater transparency, and flexibility, although slightly worse quality.
In the future, we aim to use our proposed discovery process to produce self-improving AI in a closed-loop system using open models.

Future Directions. Direct enhancements to The AI Scientist could include integrating vision capabilities for better plot and figure handling, incorporating human feedback and interaction to refine the AI’s outputs, and enabling The AI Scientist to automatically expand the scope of its experiments by pulling in new data and models from the internet, provided this can be done safely. Additionally, The AI Scientist could follow up on its best ideas or even perform research directly on its own code in a self-referential manner. Indeed, significant portions of the code for this project were written by Aider. Expanding the framework to other scientific domains could further amplify its impact, paving the way for a new era of automated scientific discovery. For example, by integrating these technologies with cloud robotics and automation in physical lab spaces ([Kehoe et al., 2015](#bib.bib50); [Zucchelli et al., 2021](#bib.bib115); [Arnold, 2022](#bib.bib5); [Sparkes et al., 2010](#bib.bib93)) provided it can be done safely, The AI Scientist could perform experiments for biology, chemistry, and material sciences.

Crucially, future work should address the reliability and hallucination concerns, potentially through a more in-depth automatic verification of the reported results. This could be done by directly linking code and experiments, or by seeing if an automated verifier can independently reproduce the results.

Conclusion. The introduction of The AI Scientist marks a significant step towards realizing the full potential of AI in scientific research. By automating the discovery process and incorporating an AI-driven review system, we open the door to endless possibilities for innovation and problem-solving in the most challenging areas of science and technology.
Ultimately, we envision a fully AI-driven scientific ecosystem including not only AI-driven researchers but also reviewers, area chairs, and entire conferences.
However, we do not believe the role of a human scientist will be diminished.
We expect the role of scientists will change as we adapt to new technology, and they will be empowered to tackle more ambitious goals.
For instance, researchers often have more ideas than they have time to pursue, what if The AI Scientist could take the first explorations on all of them?

While the current iteration of The AI Scientist demonstrates a strong ability to innovate on top of well-established ideas, such as Diffusion Modeling or Transformers, it is an open question whether such systems can ultimately propose genuinely paradigm-shifting ideas.
Will future versions of The AI Scientist be capable of proposing ideas as impactful as Diffusion Modeling, or come up with the next Transformer architecture?
Will machines ultimately be able to invent concepts as fundamental as the artificial neural network, or information theory?
We believe The AI Scientist will make a great companion to human scientists, but only time will tell to the extent to which the nature of human creativity and our moments of serendipitous innovation ([Stanley and Lehman, 2015](#bib.bib95)) can be replicated by an open-ended discovery process conducted by artificial agents.

## Acknowledgments

The authors would like to thank Irene Zhang, Johannes von Oswald, Takuya Akiba, Yujin Tang, Aaron Dharna, Ben Norman, Jenny Zhang, Shengran Hu, Anna Olerinyova, Felicitas Muecke-Wegner, and Kenneth Stanley for helpful feedback on an earlier version of the draft.
This work was supported by the Vector Institute, Canada CIFAR AI Chairs program, grants from Schmidt Futures, Open Philanthropy, NSERC, and a generous donation from Rafael Cosman.

## References

- Alet et al. (2020)

  Ferran Alet, Martin F Schneider, Tomas Lozano-Perez, and Leslie Pack Kaelbling.
  Meta-learning curiosity algorithms.
  *arXiv preprint arXiv:2003.05325*, 2020.
- Altmäe et al. (2023)

  Signe Altmäe, Alberto Sola-Leyva, and Andres Salumets.
  Artificial intelligence in scientific writing: a friend or a foe?
  *Reproductive BioMedicine Online*, 47(1):3–9, 2023.
- Anthropic (2023)

  Anthropic.
  Model card and evaluations for claude models, 2023.
  URL <https://www-files.anthropic.com/production/images/Model-Card-Claude-2.pdf>.
- Anthropic (2024)

  Anthropic.
  The claude 3 model family: Opus, sonnet, haiku, 2024.
  URL <https://www-cdn.anthropic.com/de8ba9b01c9ab7cbabf5c33b80b7bbc618857627/Model_Card_Claude_3.pdf>.
- Arnold (2022)

  Carrie Arnold.
  Cloud labs: where robots do the research.
  *Nature*, 606(7914):612–613, 2022.
- Baek et al. (2024)

  Jinheon Baek, Sujay Kumar Jauhar, Silviu Cucerzan, and Sung Ju Hwang.
  Researchagent: Iterative research idea generation over scientific literature with large language models, 2024.
  URL <https://arxiv.org/abs/2404.07738>.
- Berto (2024)

  Federico Berto.
  Iclr2022-openreviewdata, 2024.
  URL <https://github.com/fedebotu/ICLR2022-OpenReviewData>.
- Beygelzimer et al. (2021)

  Alina Beygelzimer, Yann Dauphin, Percy Liang, and Jennifer Wortman Vaughan.
  The neurips 2021 consistency experiment.
  *Neural Information Processing Systems blog post*, 2021.
  URL <https://blog.neurips.cc/2021/12/08/the-neurips-2021-consistency-experiment>.
- Bradley et al. (2024)

  Herbie Bradley, Andrew Dai, Hannah Benita Teufel, Jenny Zhang, Koen Oostermeijer, Marco Bellagente, Jeff Clune, Kenneth Stanley, Gregory Schott, and Joel Lehman.
  Quality-diversity through ai feedback.
  In *The Twelfth International Conference on Learning Representations*, 2024.
- Brant and Stanley (2017)

  Jonathan C Brant and Kenneth O Stanley.
  Minimal criterion coevolution: a new approach to open-ended search.
  In *Proceedings of the Genetic and Evolutionary Computation Conference*, pages 67–74, 2017.
- Brown et al. (2020)

  Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, Sandhini Agarwal, Ariel Herbert-Voss, Gretchen Krueger, Tom Henighan, Rewon Child, Aditya Ramesh, Daniel M. Ziegler, Jeffrey Wu, Clemens Winter, Christopher Hesse, Mark Chen, Eric Sigler, Mateusz Litwin, Scott Gray, Benjamin Chess, Jack Clark, Christopher Berner, Sam McCandlish, Alec Radford, Ilya Sutskever, and Dario Amodei.
  Language models are few-shot learners, 2020.
- Buchanan and Feigenbaum (1981)

  Bruce G Buchanan and Edward A Feigenbaum.
  Dendral and meta-dendral: Their applications dimension.
  In *Readings in artificial intelligence*, pages 313–322. Elsevier, 1981.
- Burns et al. (2023)

  Collin Burns, Pavel Izmailov, Jan Hendrik Kirchner, Bowen Baker, Leo Gao, Leopold Aschenbrenner, Yining Chen, Adrien Ecoffet, Manas Joglekar, Jan Leike, Ilya Sutskever, and Jeff Wu.
  Weak-to-strong generalization: Eliciting strong capabilities with weak supervision, 2023.
  URL <https://arxiv.org/abs/2312.09390>.
- Chalmers (2013)

  Alan Chalmers.
  *What is this thing called science?*
  McGraw-Hill Education (UK), 2013.
- Chen et al. (2024a)

  Angelica Chen, David Dohan, and David So.
  Evoprompting: Language models for code-level neural architecture search.
  *Advances in Neural Information Processing Systems*, 36, 2024a.
- Chen et al. (2021)

  Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde De Oliveira Pinto, Jared Kaplan, Harri Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman, et al.
  Evaluating large language models trained on code.
  *arXiv preprint arXiv:2107.03374*, 2021.
- Chen et al. (2024b)

  Xiangning Chen, Chen Liang, Da Huang, Esteban Real, Kaiyuan Wang, Hieu Pham, Xuanyi Dong, Thang Luong, Cho-Jui Hsieh, Yifeng Lu, et al.
  Symbolic discovery of optimization algorithms.
  *Advances in Neural Information Processing Systems*, 36, 2024b.
- Clune (2019)

  Jeff Clune.
  Ai-gas: Ai-generating algorithms, an alternate paradigm for producing general artificial intelligence.
  *arXiv preprint arXiv:1905.10985*, 2019.
- D’Arcy et al. (2024)

  Mike D’Arcy, Tom Hope, Larry Birnbaum, and Doug Downey.
  Marg: Multi-agent review generation for scientific papers, 2024.
  URL <https://arxiv.org/abs/2401.04259>.
- Dewey (1910)

  J. Dewey.
  *How We Think*.
  D.C. Heath & Company, 1910.
  ISBN 9781519501868.
  URL <https://books.google.co.uk/books?id=WF0AAAAAMAAJ>.
- Ding et al. (2024)

  Li Ding, Jenny Zhang, Jeff Clune, Lee Spector, and Joel Lehman.
  Quality diversity through human feedback: Towards open-ended diversity-driven optimization.
  In *Forty-first International Conference on Machine Learning*, 2024.
  URL <https://openreview.net/forum?id=9zlZuAAb08>.
- Dinu et al. (2024)

  Marius-Constantin Dinu, Claudiu Leoveanu-Condrei, Markus Holzleitner, Werner Zellinger, and Sepp Hochreiter.
  Symbolicai: A framework for logic-based approaches combining generative models and solvers, 2024.
  URL <https://arxiv.org/abs/2402.00854>.
- Epstein et al. (2023)

  Ziv Epstein, Aaron Hertzmann, Investigators of Human Creativity, Memo Akten, Hany Farid, Jessica Fjeld, Morgan R Frank, Matthew Groh, Laura Herman, Neil Leach, et al.
  Art and the science of generative ai.
  *Science*, 380(6650):1110–1111, 2023.
- Faldor et al. (2024)

  Maxence Faldor, Jenny Zhang, Antoine Cully, and Jeff Clune.
  Omni-epic: Open-endedness via models of human notions of interestingness with environments programmed in code, 2024.
  URL <https://arxiv.org/abs/2405.15568>.
- Falkenhainer and Michalski (1986)

  Brian C Falkenhainer and Ryszard S Michalski.
  Integrating quantitative and qualitative discovery: the abacus system.
  *Machine Learning*, 1:367–401, 1986.
- Fawzi et al. (2022)

  Alhussein Fawzi, Matej Balog, Aja Huang, Thomas Hubert, Bernardino Romera-Paredes, Mohammadamin Barekatain, Alexander Novikov, Francisco J R Ruiz, Julian Schrittwieser, Grzegorz Swirszcz, et al.
  Discovering faster matrix multiplication algorithms with reinforcement learning.
  *Nature*, 610(7930):47–53, 2022.
- Fedus et al. (2022)

  William Fedus, Barret Zoph, and Noam Shazeer.
  Switch transformers: Scaling to trillion parameter models with simple and efficient sparsity.
  *Journal of Machine Learning Research*, 23(120):1–39, 2022.
  URL <http://jmlr.org/papers/v23/21-0998.html>.
- Fricke (2018)

  Suzanne Fricke.
  Semantic scholar.
  *Journal of the Medical Library Association: JMLA*, 106(1):145, 2018.
- Gauthier (2024)

  Paul Gauthier.
  aider, 2024.
  URL <https://github.com/paul-gauthier/aider>.
- Ghahramani (2015)

  Zoubin Ghahramani.
  Probabilistic machine learning and artificial intelligence.
  *Nature*, 521(7553):452–459, 2015.
- Girotra et al. (2023)

  Karan Girotra, Lennart Meincke, Christian Terwiesch, and Karl T Ulrich.
  Ideas are dimes a dozen: Large language models for idea generation in innovation.
  *Available at SSRN 4526071*, 2023.
- Glorot and Bengio (2010)

  Xavier Glorot and Yoshua Bengio.
  Understanding the difficulty of training deep feedforward neural networks.
  In *Proceedings of the thirteenth international conference on artificial intelligence and statistics*, pages 249–256. JMLR Workshop and Conference Proceedings, 2010.
- Goodfellow et al. (2014)

  Ian Goodfellow, Jean Pouget-Abadie, Mehdi Mirza, Bing Xu, David Warde-Farley, Sherjil Ozair, Aaron Courville, and Yoshua Bengio.
  Generative adversarial nets.
  In Z. Ghahramani, M. Welling, C. Cortes, N. Lawrence, and K.Q. Weinberger, editors, *Advances in Neural Information Processing Systems*, volume 27. Curran Associates, Inc., 2014.
  URL <https://proceedings.neurips.cc/paper/2014/file/5ca3e9b122f61f8f06494c97b1afccf3-Paper.pdf>.
- Google DeepMind Gemini Team (2023)

  Google DeepMind Gemini Team.
  Gemini: A family of highly capable multimodal models, 2023.
- Hatamizadeh et al. (2024)

  Ali Hatamizadeh, Jiaming Song, Guilin Liu, Jan Kautz, and Arash Vahdat.
  Diffit: Diffusion vision transformers for image generation, 2024.
  URL <https://arxiv.org/abs/2312.02139>.
- Hayes et al. (2024)

  Tomas Hayes, Roshan Rao, Halil Akin, Nicholas J Sofroniew, Deniz Oktay, Zeming Lin, Robert Verkuil, Vincent Q Tran, Jonathan Deaton, Marius Wiggert, et al.
  Simulating 500 million years of evolution with a language model.
  *bioRxiv*, pages 2024–07, 2024.
- He et al. (2021)

  Xin He, Kaiyong Zhao, and Xiaowen Chu.
  Automl: A survey of the state-of-the-art.
  *Knowledge-based systems*, 212:106622, 2021.
- Ho et al. (2020)

  Jonathan Ho, Ajay Jain, and Pieter Abbeel.
  Denoising diffusion probabilistic models.
  In H. Larochelle, M. Ranzato, R. Hadsell, M.F. Balcan, and H. Lin, editors, *Advances in Neural Information Processing Systems*, volume 33, pages 6840–6851. Curran Associates, Inc., 2020.
  URL <https://proceedings.neurips.cc/paper/2020/file/4c5bcfec8584af0d967f1ab10179ca4b-Paper.pdf>.
- Huang (2018)

  Jia-Bin Huang.
  Deep paper gestalt.
  *arXiv preprint arXiv:1812.08775*, 2018.
- Huang et al. (2024)

  Qian Huang, Jian Vora, Percy Liang, and Jure Leskovec.
  Mlagentbench: Evaluating language agents on machine learning experimentation.
  In *Forty-first International Conference on Machine Learning*, 2024.
- Hutter et al. (2019)

  Frank Hutter, Lars Kotthoff, and Joaquin Vanschoren.
  *Automated machine learning: methods, systems, challenges*.
  Springer Nature, 2019.
- Hutter (2006)

  Marcus Hutter.
  The hutter prize, 2006.
  URL <http://prize.hutter1.net>.
- Ifargan et al. (2024)

  Tal Ifargan, Lukas Hafner, Maor Kern, Ori Alcalay, and Roy Kishony.
  Autonomous llm-driven research from data to human-verifiable research papers, 2024.
  URL <https://arxiv.org/abs/2404.17605>.
- Jevons (1877)

  William Stanley Jevons.
  *The principles of science: A treatise on logic and scientific method*.
  Macmillan and Company, 1877.
- Jiang et al. (2024)

  Albert Q. Jiang, Alexandre Sablayrolles, Antoine Roux, Arthur Mensch, Blanche Savary, Chris Bamford, Devendra Singh Chaplot, Diego de las Casas, Emma Bou Hanna, Florian Bressand, Gianna Lengyel, Guillaume Bour, Guillaume Lample, Lélio Renard Lavaud, Lucile Saulnier, Marie-Anne Lachaux, Pierre Stock, Sandeep Subramanian, Sophia Yang, Szymon Antoniak, Teven Le Scao, Théophile Gervet, Thibaut Lavril, Thomas Wang, Timothée Lacroix, and William El Sayed.
  Mixtral of experts, 2024.
  URL <https://arxiv.org/abs/2401.04088>.
- Jimenez et al. (2024)

  Carlos E. Jimenez, John Yang, Alexander Wettig, Shunyu Yao, Kexin Pei, Ofir Press, and Karthik Narasimhan.
  Swe-bench: Can language models resolve real-world github issues?, 2024.
  URL <https://arxiv.org/abs/2310.06770>.
- Jumper et al. (2021)

  John Jumper, Richard Evans, Alexander Pritzel, Tim Green, Michael Figurnov, Olaf Ronneberger, Kathryn Tunyasuvunakool, Russ Bates, Augustin Žídek, Anna Potapenko, et al.
  Highly accurate protein structure prediction with alphafold.
  *nature*, 596(7873):583–589, 2021.
- Karpathy (2015)

  Andrej Karpathy.
  The unreasonable effectiveness of recurrent neural networks, 2015.
  URL <https://karpathy.github.io/2015/05/21/rnn-effectiveness/>.
- Karpathy (2022)

  Andrej Karpathy.
  NanoGPT, 2022.
  URL <https://github.com/karpathy/nanoGPT>.
- Kehoe et al. (2015)

  Ben Kehoe, Sachin Patil, Pieter Abbeel, and Ken Goldberg.
  A survey of research on cloud robotics and automation.
  *IEEE Transactions on automation science and engineering*, 12(2):398–409, 2015.
- Kingma and Welling (2014)

  Diederik P. Kingma and Max Welling.
  Auto-Encoding Variational Bayes.
  In *2nd International Conference on Learning Representations, ICLR 2014, Banff, AB, Canada, April 14-16, 2014, Conference Track Proceedings*, 2014.
- Kirsch et al. (2019)

  Louis Kirsch, Sjoerd van Steenkiste, and Jürgen Schmidhuber.
  Improving generalization in meta reinforcement learning using learned objectives.
  *arXiv preprint arXiv:1910.04098*, 2019.
- Lange et al. (2023a)

  Robert Lange, Tom Schaul, Yutian Chen, Chris Lu, Tom Zahavy, Valentin Dalibard, and Sebastian Flennerhag.
  Discovering attention-based genetic algorithms via meta-black-box optimization.
  In *Proceedings of the Genetic and Evolutionary Computation Conference*, pages 929–937, 2023a.
- Lange et al. (2023b)

  Robert Lange, Tom Schaul, Yutian Chen, Tom Zahavy, Valentin Dalibard, Chris Lu, Satinder Singh, and Sebastian Flennerhag.
  Discovering evolution strategies via meta-black-box optimization.
  In *Proceedings of the Companion Conference on Genetic and Evolutionary Computation*, pages 29–30, 2023b.
- Lange et al. (2024)

  Robert Tjarko Lange, Yingtao Tian, and Yujin Tang.
  Large language models as evolution strategies.
  *arXiv preprint arXiv:2402.18381*, 2024.
- Langley (1987)

  Pat Langley.
  *Scientific discovery: Computational explorations of the creative processes*.
  MIT press, 1987.
- Langley (2024)

  Pat Langley.
  Integrated systems for computational scientific discovery.
  In *Proceedings of the AAAI Conference on Artificial Intelligence*, volume 38, pages 22598–22606, 2024.
- Lehman et al. (2008)

  Joel Lehman, Kenneth O Stanley, et al.
  Exploiting open-endedness to solve problems through the search for novelty.
  In *ALIFE*, pages 329–336, 2008.
- Lehman et al. (2020)

  Joel Lehman, Jeff Clune, Dusan Misevic, Christoph Adami, Lee Altenberg, Julie Beaulieu, Peter J Bentley, Samuel Bernard, Guillaume Beslon, David M Bryson, et al.
  The surprising creativity of digital evolution: A collection of anecdotes from the evolutionary computation and artificial life research communities.
  *Artificial life*, 26(2):274–306, 2020.
- Lehman et al. (2022)

  Joel Lehman, Jonathan Gordon, Shawn Jain, Kamal Ndousse, Cathy Yeh, and Kenneth O. Stanley.
  Evolution through large models, 2022.
  URL <https://arxiv.org/abs/2206.08896>.
- Lehman et al. (2023)

  Joel Lehman, Jonathan Gordon, Shawn Jain, Kamal Ndousse, Cathy Yeh, and Kenneth O Stanley.
  Evolution through large models.
  In *Handbook of Evolutionary Machine Learning*, pages 331–366. Springer, 2023.
- Lenat (1977)

  Douglas B Lenat.
  Automated theory formation in mathematics.
  In *IJCAI*, volume 77, pages 833–842, 1977.
- Lenat and Brown (1984)

  Douglas B Lenat and John Seely Brown.
  Why am and eurisko appear to work.
  *Artificial intelligence*, 23(3):269–294, 1984.
- Liang et al. (2024)

  Weixin Liang, Yuhui Zhang, Hancheng Cao, Binglu Wang, Daisy Yi Ding, Xinyu Yang, Kailas Vodrahalli, Siyu He, Daniel Scott Smith, Yian Yin, et al.
  Can large language models provide useful feedback on research papers? a large-scale empirical analysis.
  *NEJM AI*, page AIoa2400196, 2024.
- Lim et al. (2024)

  Bryan Lim, Manon Flageat, and Antoine Cully.
  Large language models as in-context ai generators for quality-diversity.
  *arXiv preprint arXiv:2404.15794*, 2024.
- Llama Team (2024)

  Llama Team.
  The llama 3 herd of models, 2024.
  URL <https://arxiv.org/abs/2407.21783>.
- Lu et al. (2022a)

  Chris Lu, Jakub Kuba, Alistair Letcher, Luke Metz, Christian Schroeder de Witt, and Jakob Foerster.
  Discovered policy optimisation.
  *Advances in Neural Information Processing Systems*, 35:16455–16468, 2022a.
- Lu et al. (2024a)

  Chris Lu, Samuel Holt, Claudio Fanconi, Alex J Chan, Jakob Foerster, Mihaela van der Schaar, and Robert Tjarko Lange.
  Discovering preference optimization algorithms with and for large language models.
  *arXiv preprint arXiv:2406.08414*, 2024a.
- Lu et al. (2022b)

  Cong Lu, Philip Ball, Jack Parker-Holder, Michael Osborne, and Stephen J. Roberts.
  Revisiting design choices in offline model based reinforcement learning.
  In *International Conference on Learning Representations*, 2022b.
  URL <https://openreview.net/forum?id=zz9hXVhf40>.
- Lu et al. (2024b)

  Cong Lu, Shengran Hu, and Jeff Clune.
  Intelligent go-explore: Standing on the shoulders of giant foundation models, 2024b.
  URL <https://arxiv.org/abs/2405.15143>.
- Ma et al. (2023)

  Yecheng Jason Ma, William Liang, Guanzhi Wang, De-An Huang, Osbert Bastani, Dinesh Jayaraman, Yuke Zhu, Linxi Fan, and Anima Anandkumar.
  Eureka: Human-level reward design via coding large language models.
  *arXiv preprint arXiv:2310.12931*, 2023.
- Mahoney (2011)

  Matt Mahoney.
  About the test data, 2011.
  URL <http://mattmahoney.net/dc/textdata.html>.
- Majumder et al. (2024)

  Bodhisattwa Prasad Majumder, Harshit Surana, Dhruv Agarwal, Bhavana Dalvi Mishra, Abhijeetsingh Meena, Aryan Prakhar, Tirth Vora, Tushar Khot, Ashish Sabharwal, and Peter Clark.
  Discoverybench: Towards data-driven discovery with large language models, 2024.
  URL <https://arxiv.org/abs/2407.01725>.
- May (2022)

  Daniel May.
  grokking, 2022.
  URL <https://github.com/danielmamay/grokking>.
- Merchant et al. (2023)

  Amil Merchant, Simon Batzner, Samuel S Schoenholz, Muratahan Aykol, Gowoon Cheon, and Ekin Dogus Cubuk.
  Scaling deep learning for materials discovery.
  *Nature*, 624(7990):80–85, 2023.
- Metz et al. (2022)

  Luke Metz, James Harrison, C Daniel Freeman, Amil Merchant, Lucas Beyer, James Bradbury, Naman Agrawal, Ben Poole, Igor Mordatch, Adam Roberts, et al.
  Velo: Training versatile learned optimizers by scaling up.
  *arXiv preprint arXiv:2211.09760*, 2022.
- Nordhausen and Langley (1990)

  Bernd Nordhausen and Pat Langley.
  A robust approach to numeric discovery.
  In *Machine learning proceedings 1990*, pages 411–418. Elsevier, 1990.
- Olsson et al. (2022)

  Catherine Olsson, Nelson Elhage, Neel Nanda, Nicholas Joseph, Nova DasSarma, Tom Henighan, Ben Mann, Amanda Askell, Yuntao Bai, Anna Chen, et al.
  In-context learning and induction heads.
  *arXiv preprint arXiv:2209.11895*, 2022.
- OpenAI (2023)

  OpenAI.
  Gpt-4 technical report, 2023.
- Pärnamaa (2023)

  Tanel Pärnamaa.
  tiny-diffusion, 2023.
  URL <https://github.com/tanelp/tiny-diffusion>.
- Power et al. (2022)

  Alethea Power, Yuri Burda, Harri Edwards, Igor Babuschkin, and Vedant Misra.
  Grokking: Generalization beyond overfitting on small algorithmic datasets.
  *arXiv preprint arXiv:2201.02177*, 2022.
- Pyzer-Knapp et al. (2022)

  Edward O Pyzer-Knapp, Jed W Pitera, Peter WJ Staar, Seiji Takeda, Teodoro Laino, Daniel P Sanders, James Sexton, John R Smith, and Alessandro Curioni.
  Accelerating materials discovery using artificial intelligence, high performance computing and robotics.
  *npj Computational Materials*, 8(1):84, 2022.
- Romera-Paredes et al. (2024)

  Bernardino Romera-Paredes, Mohammadamin Barekatain, Alexander Novikov, Matej Balog, M Pawan Kumar, Emilien Dupont, Francisco JR Ruiz, Jordan S Ellenberg, Pengming Wang, Omar Fawzi, et al.
  Mathematical discoveries from program search with large language models.
  *Nature*, 625(7995):468–475, 2024.
- Schick et al. (2024)

  Timo Schick, Jane Dwivedi-Yu, Roberto Dessì, Roberta Raileanu, Maria Lomeli, Eric Hambro, Luke Zettlemoyer, Nicola Cancedda, and Thomas Scialom.
  Toolformer: Language models can teach themselves to use tools.
  *Advances in Neural Information Processing Systems*, 36, 2024.
- Schmidhuber (1991)

  Jürgen Schmidhuber.
  Curious model-building control systems.
  In *Proc. international joint conference on neural networks*, pages 1458–1463, 1991.
- Schmidhuber (2010a)

  Jürgen Schmidhuber.
  Artificial scientists & artists based on the formal theory of creativity.
  In *3d Conference on Artificial General Intelligence (AGI-2010)*, pages 148–153. Atlantis Press, 2010a.
- Schmidhuber (2010b)

  Jürgen Schmidhuber.
  Formal theory of creativity, fun, and intrinsic motivation (1990–2010).
  *IEEE transactions on autonomous mental development*, 2(3):230–247, 2010b.
- Schmidhuber (2012)

  Jürgen Schmidhuber.
  When creative machines overtake man, 2012.
  URL <https://www.youtube.com/watch?v=KQ35zNlyG-o>.
- Shinn et al. (2024)

  Noah Shinn, Federico Cassano, Ashwin Gopinath, Karthik Narasimhan, and Shunyu Yao.
  Reflexion: Language agents with verbal reinforcement learning.
  *Advances in Neural Information Processing Systems*, 36, 2024.
- Snell (2021)

  Charlie Snell.
  grokking, 2021.
  URL <https://github.com/Sea-Snell/grokking>.
- Sohl-Dickstein et al. (2015)

  Jascha Sohl-Dickstein, Eric Weiss, Niru Maheswaranathan, and Surya Ganguli.
  Deep unsupervised learning using nonequilibrium thermodynamics.
  In Francis Bach and David Blei, editors, *Proceedings of the 32nd International Conference on Machine Learning*, volume 37 of *Proceedings of Machine Learning Research*, pages 2256–2265, Lille, France, 07–09 Jul 2015. PMLR.
  URL <https://proceedings.mlr.press/v37/sohl-dickstein15.html>.
- Song et al. (2024)

  Xingyou Song, Yingtao Tian, Robert Tjarko Lange, Chansoo Lee, Yujin Tang, and Yutian Chen.
  Position paper: Leveraging foundational models for black-box optimization: Benefits, challenges, and future directions.
  *arXiv preprint arXiv:2405.03547*, 2024.
- Sparkes et al. (2010)

  Andrew Sparkes, Wayne Aubrey, Emma Byrne, Amanda Clare, Muhammed N Khan, Maria Liakata, Magdalena Markham, Jem Rowland, Larisa N Soldatova, Kenneth E Whelan, et al.
  Towards robot scientists for autonomous scientific discovery.
  *Automated experimentation*, 2:1–11, 2010.
- Stanley (2019)

  Kenneth O Stanley.
  Why open-endedness matters.
  *Artificial life*, 25(3):232–235, 2019.
- Stanley and Lehman (2015)

  Kenneth O Stanley and Joel Lehman.
  *Why greatness cannot be planned: The myth of the objective*.
  Springer, 2015.
- Stanley et al. (2017)

  Kenneth O Stanley, Joel Lehman, and Lisa Soros.
  Open-endedness: The last grand challenge you’ve never heard of.
  *While open-endedness could be a force for discovering intelligence, it could also be a component of AI itself*, 2017.
- Szymanski et al. (2023)

  Nathan J Szymanski, Bernardus Rendy, Yuxing Fei, Rishi E Kumar, Tanjin He, David Milsted, Matthew J McDermott, Max Gallant, Ekin Dogus Cubuk, Amil Merchant, et al.
  An autonomous laboratory for the accelerated synthesis of novel materials.
  *Nature*, 624(7990):86–91, 2023.
- Talmor et al. (2019)

  Alon Talmor, Jonathan Herzig, Nicholas Lourie, and Jonathan Berant.
  CommonsenseQA: A question answering challenge targeting commonsense knowledge.
  In Jill Burstein, Christy Doran, and Thamar Solorio, editors, *Proceedings of the 2019 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long and Short Papers)*, pages 4149–4158, Minneapolis, Minnesota, June 2019. Association for Computational Linguistics.
  [10.18653/v1/N19-1421](https://doi.org/10.18653/v1/N19-1421).
  URL <https://aclanthology.org/N19-1421>.
- Vaswani et al. (2017)

  Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N Gomez, Łukasz Kaiser, and Illia Polosukhin.
  Attention is all you need.
  *Advances in neural information processing systems*, 30, 2017.
- Waltz and Buchanan (2009)

  David Waltz and Bruce G Buchanan.
  Automating science.
  *Science*, 324(5923):43–44, 2009.
- Wan et al. (2021)

  Xingchen Wan, Vu Nguyen, Huong Ha, Binxin Ru, Cong Lu, and Michael A Osborne.
  Think global and act local: Bayesian optimisation over high-dimensional categorical and mixed search spaces.
  In *International Conference on Machine Learning*, pages 10663–10674. PMLR, 2021.
- Wan et al. (2022)

  Xingchen Wan, Cong Lu, Jack Parker-Holder, Philip J. Ball, Vu Nguyen, Binxin Ru, and Michael Osborne.
  Bayesian generational population-based training.
  In Isabelle Guyon, Marius Lindauer, Mihaela van der Schaar, Frank Hutter, and Roman Garnett, editors, *Proceedings of the First International Conference on Automated Machine Learning*, volume 188 of *Proceedings of Machine Learning Research*, pages 14/1–27. PMLR, 25–27 Jul 2022.
  URL <https://proceedings.mlr.press/v188/wan22a.html>.
- Wang et al. (2024a)

  Lei Wang, Chen Ma, Xueyang Feng, Zeyu Zhang, Hao Yang, Jingsen Zhang, Zhiyuan Chen, Jiakai Tang, Xu Chen, Yankai Lin, et al.
  A survey on large language model based autonomous agents.
  *Frontiers of Computer Science*, 18(6):186345, 2024a.
- Wang et al. (2024b)

  Qingyun Wang, Doug Downey, Heng Ji, and Tom Hope.
  Scimon: Scientific inspiration machines optimized for novelty, 2024b.
  URL <https://arxiv.org/abs/2305.14259>.
- Wang et al. (2022)

  Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc Le, Ed Chi, Sharan Narang, Aakanksha Chowdhery, and Denny Zhou.
  Self-consistency improves chain of thought reasoning in language models.
  *arXiv preprint arXiv:2203.11171*, 2022.
- Wang et al. (2024c)

  Yidong Wang, Qi Guo, Wenjin Yao, Hongbo Zhang, Xin Zhang, Zhen Wu, Meishan Zhang, Xinyu Dai, Min Zhang, Qingsong Wen, Wei Ye, Shikun Zhang, and Yue Zhang.
  Autosurvey: Large language models can automatically write surveys, 2024c.
  URL <https://arxiv.org/abs/2406.10252>.
- Wei et al. (2022)

  Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Fei Xia, Ed Chi, Quoc V Le, Denny Zhou, et al.
  Chain-of-thought prompting elicits reasoning in large language models.
  *Advances in neural information processing systems*, 35:24824–24837, 2022.
- Xu et al. (2022)

  Frank F Xu, Uri Alon, Graham Neubig, and Vincent Josua Hellendoorn.
  A systematic evaluation of large language models of code.
  In *Proceedings of the 6th ACM SIGPLAN International Symposium on Machine Programming*, pages 1–10, 2022.
- Yang et al. (2024)

  Zonglin Yang, Xinya Du, Junxian Li, Jie Zheng, Soujanya Poria, and Erik Cambria.
  Large language models for automated open-domain scientific hypotheses discovery, 2024.
  URL <https://arxiv.org/abs/2309.02726>.
- Yu et al. (2023)

  Wenhao Yu, Nimrod Gileadi, Chuyuan Fu, Sean Kirmani, Kuang-Huei Lee, Montse Gonzalez Arenas, Hao-Tien Lewis Chiang, Tom Erez, Leonard Hasenclever, Jan Humplik, et al.
  Language to rewards for robotic skill synthesis.
  *arXiv preprint arXiv:2306.08647*, 2023.
- Yuksel et al. (2012)

  Seniha Esen Yuksel, Joseph N Wilson, and Paul D Gader.
  Twenty years of mixture of experts.
  *IEEE transactions on neural networks and learning systems*, 23(8):1177–1193, 2012.
- Zhang et al. (2024)

  Jenny Zhang, Joel Lehman, Kenneth Stanley, and Jeff Clune.
  OMNI: Open-endedness via models of human notions of interestingness.
  In *The Twelfth International Conference on Learning Representations*, 2024.
  URL <https://openreview.net/forum?id=AgM3MzT99c>.
- Zheng et al. (2024)

  Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan Zhuang, Zhanghao Wu, Yonghao Zhuang, Zi Lin, Zhuohan Li, Dacheng Li, Eric Xing, et al.
  Judging llm-as-a-judge with mt-bench and chatbot arena.
  *Advances in Neural Information Processing Systems*, 36, 2024.
- Zhu et al. (2024)

  Qihao Zhu, Daya Guo, Zhihong Shao, Dejian Yang, Peiyi Wang, Runxin Xu, Y Wu, Yukun Li, Huazuo Gao, Shirong Ma, et al.
  Deepseek-coder-v2: Breaking the barrier of closed-source models in code intelligence.
  *arXiv preprint arXiv:2406.11931*, 2024.
- Zucchelli et al. (2021)

  Piero Zucchelli, Giorgio Horak, and Nigel Skinner.
  Highly versatile cloud-based automation solution for the remote design and execution of experiment protocols during the covid-19 pandemic.
  *SLAS TECHNOLOGY: Translating Life Sciences Innovation*, 26(2):127–139, 2021.
- Zytkow (1996)

  Jan M Zytkow.
  Automated discovery of empirical laws.
  *Fundamenta Informaticae*, 27(2-3):299–318, 1996.

## Appendix

## Table of Contents

## Appendix A Prompts

We present some representative prompts that we use for The AI Scientist in [Section 3](#S3 "3 The AI Scientist ‣ The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery") and [Section 4](#S4 "4 Automated Paper Reviewing ‣ The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery"). The full list of prompts can be found in the provided code.

### A.1 Idea Generation

These prompts correspond to the first stage of The AI Scientist in [Section 3](#S3 "3 The AI Scientist ‣ The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery").

Idea Generation System Prompt

You are an ambitious AI PhD student who is looking to publish a paper that will contribute significantly to the field.

Idea Generation Prompt

```
{task_description}
<experiment.py>
{code}
</experiment.py>

Here are the ideas that you have already generated:

’’’
{prev_ideas_string}
’’’

Come up with the next impactful and creative idea for research
experiments and directions you can feasibly investigate with the code
provided. Note that you will not have access to any additional resources
or datasets. Make sure any idea is not overfit the specific training
dataset or model, and has wider significance.

Respond in the following format:

THOUGHT:
<THOUGHT>

NEW IDEA JSON:
‘‘‘json
<JSON>
‘‘‘

In <THOUGHT>, first briefly discuss your intuitions and motivations for
the idea. Detail your high-level plan, necessary design choices and
ideal outcomes of the experiments. Justify how the idea is different
from the existing ones.

In <JSON>, provide the new idea in JSON format with the following fields:
- "Name": A shortened descriptor of the idea. Lowercase, no spaces,
underscores allowed.
- "Title": A title for the idea, will be used for the report writing.
- "Experiment": An outline of the implementation. E.g. which functions
need to be added or modified, how results will be obtained, ...
- "Interestingness": A rating from 1 to 10 (lowest to highest).
- "Feasibility": A rating from 1 to 10 (lowest to highest).
- "Novelty": A rating from 1 to 10 (lowest to highest).

Be cautious and realistic on your ratings.
This JSON will be automatically parsed, so ensure the format is precise.
You will have {num_reflections} rounds to iterate on the idea, but do
not need to use them all.
```

Idea Novelty System Prompt

```
You are an ambitious AI PhD student who is looking to publish a paper that
will contribute significantly to the field.
You have an idea and you want to check if it is novel or not. I.e., not
overlapping significantly with existing literature or already well explored.
Be a harsh critic for novelty, ensure there is a sufficient contribution in
the idea for a new conference or workshop paper.
You will be given access to the Semantic Scholar API, which you may use to
survey the literature and find relevant papers to help you make your
decision.
The top 10 results for any search query will be presented to you with the
abstracts.

You will be given {num_rounds} to decide on the paper, but you do not need
to use them all.
At any round, you may exit early and decide on the novelty of the idea.
Decide a paper idea is novel if after sufficient searching, you have not
found a paper that significantly overlaps with your idea.
Decide a paper idea is not novel, if you have found a paper that
significantly overlaps with your idea.

{task_description}
<experiment.py>
{code}
</experiment.py>
```

Idea Novelty Prompt

```
Round {current_round}/{num_rounds}.
You have this idea:

"""
{idea}
"""

The results of the last query are (empty on first round):
"""
{last_query_results}
"""

Respond in the following format:

THOUGHT:
<THOUGHT>

RESPONSE:
‘‘‘json
<JSON>
‘‘‘

In <THOUGHT>, first briefly reason over the idea and identify any query that
could help you make your decision.
If you have made your decision, add "Decision made: novel." or
"Decision made: not novel." to your thoughts.

In <JSON>, respond in JSON format with ONLY the following field:
- "Query": An optional search query to search the literature (e.g. attention
is all you need). You must make a query if you have not decided this round.

A query will work best if you are able to recall the exact name of the paper
you are looking for, or the authors.
This JSON will be automatically parsed, so ensure the format is precise.
```

### A.2 Designing Experiments

These prompts correspond to the second stage of The AI Scientist in [Section 3](#S3 "3 The AI Scientist ‣ The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery").

Experiment Running Aider Prompt

```
Your goal is to implement the following idea: {title}.
The proposed experiment is as follows: {idea}.
You are given a total of up to {max_runs} runs to complete the necessary
experiments. You do not need to use all {max_runs}.

First, plan the list of experiments you would like to run. For example,
if you are sweeping over a specific hyperparameter, plan each value you
would like to test for each run.

Note that we already provide the vanilla baseline results, so you do not
need to re-run it.

For reference, the baseline results are as follows:

{baseline_results}

After you complete each change, we will run the command ‘python
experiment.py --out_dir=run_i’ where i is the run number and evaluate
the results.
YOUR PROPOSED CHANGE MUST USE THIS COMMAND FORMAT, DO NOT ADD ADDITIONAL
COMMAND LINE ARGS.
You can then implement the next thing on your list.
```

Plotting Aider Prompt

```
Great job! Please modify ‘plot.py‘ to generate the most relevant plots for
the final writeup.

In particular, be sure to fill in the "labels" dictionary with the correct
names for each run that you want to plot.

Only the runs in the ‘labels‘ dictionary will be plotted, so make sure to
include all relevant runs.

We will be running the command ‘python plot.py‘ to generate the plots.

---

Please modify ‘notes.txt‘ with a description of what each plot shows along
with the filename of the figure. Please do so in-depth.

Somebody else will be using ‘notes.txt‘ to write a report on this in the
future.
```

### A.3 Paper Writing

These prompts correspond to the final stage of The AI Scientist in [Section 3](#S3 "3 The AI Scientist ‣ The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery").

Paper Writing Aider Prompt

```
We’ve provided the ‘latex/template.tex‘ file to the project. We will be
filling it in section by section.

First, please fill in the {section} section of the writeup.

Some tips are provided below:
{per_section_tips}

Before every paragraph, please include a brief description of what you plan
to write in that paragraph in a comment.

Be sure to first name the file and use *SEARCH/REPLACE* blocks to perform
these edits.
```

### A.4 Paper Reviewing

These prompts correspond to the review process of The AI Scientist in [Section 4](#S4 "4 Automated Paper Reviewing ‣ The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery").

Paper Review System Prompt

You are an AI researcher who is reviewing a paper that was submitted to a prestigious ML venue. Be critical and cautious in your decision. If a paper is bad or you are unsure, give it bad scores and reject it.

Paper Review Prompt

```
## Review Form
Below is a description of the questions you will be asked on the review form
for each paper and some guidelines on what to consider when answering these
questions.
When writing your review, please keep in mind that after decisions have been
made, reviews and meta-reviews of accepted papers and opted-in rejected
papers will be made public.

{neurips_reviewer_guidelines}

{few_show_examples}

Here is the paper you are asked to review:
‘‘‘
{paper}
‘‘‘
```

Paper Review Reflection Prompt

```
Round {current_round}/{num_reflections}.
In your thoughts, first carefully consider the accuracy and soundness of
the review you just created.
Include any other factors that you think are important in evaluating the
paper.
Ensure the review is clear and concise, and the JSON is in the correct
format.
Do not make things overly complicated.
In the next attempt, try and refine and improve your review.
Stick to the spirit of the original review unless there are glaring
issues.

Respond in the same format as before:
THOUGHT:
<THOUGHT>

REVIEW JSON:
‘‘‘json
<JSON>
‘‘‘

If there is nothing to improve, simply repeat the previous JSON EXACTLY
after the thought and include "I am done" at the end of the thoughts but
before the JSON.
ONLY INCLUDE "I am done" IF YOU ARE MAKING NO MORE CHANGES.
```

Paper Review Ensembling System Prompt

```
You are an Area Chair at a machine learning conference.
You are in charge of meta-reviewing a paper that was reviewed by
{reviewer_count} reviewers.
Your job is to aggregate the reviews into a single meta-review in the same
format.
Be critical and cautious in your decision, find consensus, and respect the
opinion of all the reviewers.
```

Paper Review Ensembling Prompt

```
Review 1/N:
{review_1}

...

Review N/N:
{review_N}

{neurips_reviewer_guidelines}
```

## Appendix B Hyperparameters

Here, we list the hyperparameters used in the final experiments in [Section 6](#S6 "6 Experiments ‣ The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery").

Table 6: Hyperparameters for The AI Scientist.

| Category | Hyperparameter | Value |
| --- | --- | --- |
| Idea Generation | Number of Idea Reflections | 3 |
| Number of Novelty Search Rounds (Semantic Scholar) | 10 |
| Experiment Execution | Max Experiments | 5 |
| Max Experiment Attempts | 4 |
| Experiment Timeout | 7200 seconds |
| Plotting Timeout | 600 seconds |
| Paper Writing | Number of Citation Rounds (Semantic Scholar) | 20 |
| Number of LaTeX Error Correction Rounds | 5 |
| Reviewer | Number of Reflections | 5 |
| Number of Fewshot Examples | 1 |
| Number of Ensembled Reviews | 5 |
| LLM Temperature | 0.1 |

## Appendix C Progression of Generated Ideas

We visualize the progression of ideas across a run of The AI Scientist on the “Grokking” template described in [Section 6.3](#S6.SS3 "6.3 Grokking Analysis ‣ 6 Experiments ‣ The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery") using Sonnet 3.5.
The first idea is the seed idea, all subsequent ideas are AI-generated.

Seed Idea - batch_size_grokking

```
"Name": "batch_size_grokking",
"Title": "Batch Size Grokking: Assessing the impact of the training
batchsize on the grokking phenomenon",
"Experiment": "Modify the experiments to dynamically adjust the batch size
during training, starting with a small batch size and gradually increasing
it. This could potentially lead to faster generalization on the validation
set.",
"Interestingness": 6,
"Feasibility": 4,
"Novelty": 4,
"novel": true
```

Idea 1/50 - model_size_grokking

```
"Name": "model_size_grokking",
"Title": "Investigating the Impact of Model Size on the Grokking
Phenomenon",
"Experiment": "Modify the Transformer class to accept variable number of
layers and dimension sizes. Test models with 1, 2, 4, and 8 layers, and
dimension sizes of 64, 128, 256, and 512. For each dataset and model size,
track the step at which grokking occurs (defined as validation accuracy
exceeding 99%
and final accuracy vs model size for each task.",
"Interestingness": 8,
"Feasibility": 7,
"Novelty": 7,
"novel": true
```

Idea 2/50 - optimizer_grokking

```
"Name": "optimizer_grokking",
"Title": "Optimization Dynamics and Grokking: Comparing SGD and Adam with
Different Learning Rate Schedules",
"Experiment": "Modify the training loop to support two optimizers (SGD,
Adam) and two learning rate schedules (constant, cosine annealing). For
each combination, run multiple experiments with different random seeds.
Track validation accuracy, training loss, and L2 norm of weight updates
throughout training. Compare the timing and extent of grokking across these
optimization strategies for each dataset. Analyze how different
optimization dynamics correlate with grokking behavior, including
statistical analysis of the results.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 8,
"novel": true
```

Idea 3/50 - biased_data_grokking

```
"Name": "biased_data_grokking",
"Title": "Grokking Under Biased Data: The Effect of Input Range Bias on
Neural Network Generalization",
"Experiment": "Modify the fetch_train_example method in AbstractDataset to
introduce a simple bias: favoring lower-valued inputs. For modular
arithmetic operations, sample 70%
of the input range. For permutations, favor permutations with more elements
in their original positions. Keep the validation set unbiased. Run
experiments comparing grokking behavior on biased vs. unbiased training
sets. Track metrics such as steps to 99%
validation accuracy, and training loss. Analyze how this bias affects
grokking across different operations.",
"Interestingness": 8,
"Feasibility": 8,
"Novelty": 8,
"novel": true
```

Idea 4/50 - adaptive_noise_grokking

```
"Name": "adaptive_noise_grokking",
"Title": "Adaptive Noise in Grokking: Investigating Input Perturbations on
Algorithmic Learning and Representations",
"Experiment": "Modify the GroupDataset class to add operation-specific
noise during training: (1) For modular arithmetic, add small integer
perturbations. (2) For permutations, occasionally swap two elements.
Implement three noise levels (low, medium, high) for each operation.
Compare grokking behavior across noise levels and operations, tracking
steps to 99%
loss. Analyze learned representations by visualizing attention patterns and
performing principal component analysis (PCA) on hidden states at different
training stages. Compare these representations between noisy and non-noisy
training to understand how noise affects the abstraction of concepts.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 9,
"novel": true
```

Idea 5/50 - attention_evolution_grokking

```
"Name": "attention_evolution_grokking",
"Title": "Attention Evolution in Grokking: Quantifying the Transition from
Memorization to Generalization",
"Experiment": "Modify the Transformer class to output attention weights.
Extract and store attention weights at key checkpoints: start, mid-
training, grokking point (99%
visualization tools for attention heatmaps and create plots showing
attention evolution over time. Calculate the Frobenius norm of the
difference between attention matrices at consecutive checkpoints to
quantify attention evolution. Compare attention patterns and evolution
metrics across different operations (modular arithmetic vs. permutations).
Analyze attention for specific, informative input sequences to enhance
interpretability. Correlate attention evolution metrics with validation
accuracy and generalization performance.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 8,
"novel": true
```

Idea 6/50 - local_vs_global_attention_grokking

```
"Name": "local_vs_global_attention_grokking",
"Title": "Local vs Global Attention: Investigating the Impact of Attention
Scope on Grokking in Algorithmic Learning",
"Experiment": "Modify the DecoderBlock class to support two attention
mechanisms: full (global) attention and local attention with a fixed window
size. Implement these variants and run experiments across all datasets.
Track metrics including time to grokking (99%
validation accuracy, and training loss. Calculate and compare ’attention
entropy’ for both mechanisms across tasks to quantify attention focus.
Analyze how the scope of attention (local vs global) affects grokking
behavior and final performance for different algorithmic tasks.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 8,
"novel": true
```

Idea 7/50 - input_encoding_grokking

```
"Name": "input_encoding_grokking",
"Title": "Binary vs One-Hot Encoding: Impact on Grokking in Algorithmic
Learning Tasks",
"Experiment": "Modify the AbstractDataset class to support two encoding
schemes: one-hot (current) and binary. Implement binary encoding for
modular arithmetic operations using log2(p) bits, and for permutations
using ceil(log2(k!)) bits to represent each permutation uniquely. Adjust
the Transformer class to accommodate different input sizes. Run experiments
for each encoding scheme across all datasets, tracking metrics such as time
to grokking (99%
loss, and model memory usage. Analyze how different encoding schemes affect
grokking behavior, convergence speed, and final performance for various
algorithmic tasks. Compare the impact of input representations on the
model’s ability to learn and generalize across different operations.
Discuss how findings could inform input representation choices in other
machine learning tasks beyond algorithmic learning.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 8,
"novel": true
```

Idea 8/50 - curriculum_learning_grokking

```
"Name": "curriculum_learning_grokking",
"Title": "Curriculum Learning in Grokking: The Effect of Structured Example
Progression on Algorithmic Learning",
"Experiment": "Modify the AbstractDataset class to implement a simple
curriculum learning strategy. For modular arithmetic operations, start with
operations involving numbers in the lower half of the range and gradually
introduce larger numbers. For permutations, begin with permutations that
differ from the identity by one swap and progressively increase the number
of swaps. Implement a curriculum scheduler that increases difficulty every
500 steps. Run experiments comparing standard random sampling vs.
curriculum learning across all datasets. Track metrics including time to
grokking (99%
loss. Plot learning trajectories (validation accuracy over time) for both
approaches. Compare attention patterns between curriculum and random
approaches at different stages of training. Analyze how the curriculum
affects the grokking phenomenon across different operations and discuss
implications for training neural networks on algorithmic tasks.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 8,
"novel": true
```

Idea 9/50 - weight_init_grokking

```
"Name": "weight_init_grokking",
"Title": "Weight Initialization Strategies and Their Impact on Grokking in
Algorithmic Learning",
"Experiment": "Modify the Transformer class to support three weight
initialization strategies: Xavier/Glorot, Kaiming/He, and random normal (as
baseline). Implement these initialization methods for linear layers and
embeddings. Run experiments across all datasets for each initialization
strategy. Track metrics including time to grokking (99%
accuracy), final validation accuracy, training loss, and gradient norm
during training. Plot learning curves and compare the distribution of
weight values at different stages of training. Analyze the loss landscape
by computing gradient variance as a proxy for local geometry at key points
during training. Compare how different initialization strategies affect the
grokking phenomenon, convergence speed, and final performance across
various algorithmic tasks. Investigate potential correlations between
initial weight distributions, gradient variance characteristics, and the
timing/nature of the grokking transition.",
"Interestingness": 9,
"Feasibility": 9,
"Novelty": 8,
"novel": true
```

Idea 10/50 - task_complexity_grokking

```
"Name": "task_complexity_grokking",
"Title": "Grokking Across Task Complexity: Mapping Neural Network Learning
Dynamics to Algorithmic Difficulty",
"Experiment": "1. Modify the AbstractDataset class to include new
operations of increasing complexity: modular addition, subtraction,
multiplication, and exponentiation. 2. Implement these operations in new
dataset classes. 3. Quantify task complexity using metrics like algebraic
degree and average solution time for humans (estimated). 4. Run experiments
for each operation, tracking metrics such as time to grokking (99%
validation accuracy), final validation accuracy, training loss, and a new
’complexity-adjusted learning rate’ (validation accuracy improvement per
epoch, normalized by task complexity). 5. Plot learning curves and
complexity-adjusted learning rates for each operation. 6. Analyze attention
patterns and hidden state representations at different stages of training
for each operation. 7. Investigate correlations between quantified task
complexity and grokking characteristics (e.g., time to grokking, steepness
of accuracy improvement).",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 8,
"novel": true
```

Idea 11/50 - regularization_grokking

```
"Name": "regularization_grokking",
"Title": "The Role of Regularization in Grokking: How L2 and Label
Smoothing Affect Algorithmic Learning",
"Experiment": "1. Implement L2 regularization by adding weight decay to the
optimizer. 2. Implement label smoothing in the loss function. 3. Modify the
training function to support these regularization techniques with two
strength levels each (low and high). 4. Run experiments for each
regularization technique and strength across all datasets, including a
baseline without regularization. 5. Track metrics: time to grokking (99%
validation accuracy), final validation accuracy, training loss, and a new
’grokking speed’ metric (rate of validation accuracy improvement from 50%
to 90%
for different regularization settings. 7. Analyze how L2 regularization and
label smoothing affect the timing, speed, and nature of grokking across
various algorithmic tasks, comparing against the non-regularized
baseline.",
"Interestingness": 9,
"Feasibility": 9,
"Novelty": 8,
"novel": true
```

Idea 12/50 - grokking_extrapolation

```
"Name": "grokking_extrapolation",
"Title": "Grokking and Extrapolation: Investigating the Limits of
Algorithmic Understanding",
"Experiment": "1. Modify AbstractDataset to create a separate test set with
out-of-distribution examples (e.g., larger numbers for modular arithmetic,
longer permutations). 2. Implement a new evaluation function for the test
set. 3. During training, periodically evaluate on both validation and test
sets. 4. Track metrics: time to grokking on validation set, final
validation accuracy, test set accuracy at grokking point, final test set
accuracy, and ’extrapolation gap’. 5. Implement visualization of test set
performance and extrapolation gap over time, highlighting the grokking
point. 6. Compare extrapolation capabilities across different operations
and model sizes. 7. Analyze attention patterns on test set inputs before
and after grokking. 8. Implement a simple MLP baseline for comparison.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 9,
"novel": true
```

Idea 13/50 - label_noise_grokking

```
"Name": "label_noise_grokking",
"Title": "Grokking Under Noise: The Impact of Systematic and Random Label
Errors on Algorithmic Learning",
"Experiment": "1. Modify the AbstractDataset class to introduce two types
of label noise: random (labels changed randomly) and systematic (specific
labels consistently flipped). Add a ’noise_type’ parameter
(random/systematic) and ’noise_level’ parameter (low: 5%
high: 20%
training set while keeping the validation set clean. 3. Run experiments for
each noise type and level across all datasets. 4. Track metrics: time to
grokking (99%
loss, and model confidence (mean softmax probability of correct class). 5.
Plot learning curves and model confidence for different noise types and
levels, highlighting the grokking point for each. 6. Analyze how different
types and levels of label noise affect the timing, speed, and extent of
grokking across different operations. 7. Compare attention patterns between
noisy and clean training at different stages to understand how the model
adapts to noise.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 9,
"novel": true
```

Idea 14/50 - compositional_grokking

```
"Name": "compositional_grokking",
"Title": "Compositional Grokking: Investigating the Relationship Between
Grokking and Compositional Learning in Modular Arithmetic",
"Experiment": "1. Modify ModSumDataset and ModSubtractDataset to include
composite operations: (a + b) - c mod p and (a - b) + c mod p. 2. Implement
new dataset class CompositeModDataset for these operations. 3. Run
experiments comparing learning curves for basic (a + b, a - b) and
composite operations. 4. Track metrics: time to grokking for basic vs.
composite operations, correlation between grokking times, final accuracies.
5. Analyze attention patterns to see if the model learns to attend to
intermediate results in composite operations. 6. Implement a ’compositional
generalization’ test by training on basic operations and testing on their
compositions. 7. Compare internal representations (e.g., using PCA on
hidden states) for basic vs. composite operations at different stages of
training.",
"Interestingness": 9,
"Feasibility": 6,
"Novelty": 9,
"novel": true
```

Idea 15/50 - mutual_information_grokking

```
"Name": "mutual_information_grokking",
"Title": "Information Dynamics in Grokking: Analyzing Mutual Information
Evolution During Algorithmic Learning",
"Experiment": "1. Implement a function to estimate mutual information using
a binning approach for efficiency. 2. Modify the Transformer class to
output hidden states from the final layer. 3. Update the training loop to
calculate and store mutual information between (a) inputs and outputs, and
(b) final hidden states and outputs, at regular intervals. 4. Run
experiments across all datasets, tracking these mutual information metrics
alongside validation accuracy and training loss. 5. Create plots showing
the evolution of both mutual information metrics over training time,
highlighting the grokking point. 6. Analyze how mutual information trends
relate to grokking by testing specific hypotheses: (a) Rapid increase in
hidden state-output mutual information coincides with grokking, (b) Input-
output mutual information stabilizes post-grokking. 7. Compare mutual
information dynamics between different operations and model sizes to
identify common patterns in successful grokking.",
"Interestingness": 9,
"Feasibility": 6,
"Novelty": 9,
"novel": true
```

Idea 16/50 - sparse_subnetworks_grokking

```
"Name": "sparse_subnetworks_grokking",
"Title": "Sparse Subnetworks in Grokking: Investigating the Emergence of
Critical Structures During Algorithmic Learning",
"Experiment": "1. Implement a simple magnitude-based pruning function for
the Transformer model. 2. Modify the training loop to perform pruning at
key points: before training, just before grokking (based on validation
accuracy), and after grokking. 3. For each pruning point, create sparse
networks at different sparsity levels (e.g., 50%
these sparse networks from the original initialization for a fixed number
of steps. 5. Track metrics: validation accuracy of sparse networks,
sparsity level, and grokking speed (if it occurs). 6. Plot the performance
of sparse networks at different sparsity levels and pruning points. 7.
Compare the structure and performance of sparse networks found before and
after grokking across different operations.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 9,
"novel": true
```

Idea 17/50 - positional_encoding_grokking

```
"Name": "positional_encoding_grokking",
"Title": "Inductive Biases in Grokking: The Impact of Positional Encoding
Schemes on Algorithmic Learning",
"Experiment": "1. Modify the Transformer class to support three positional
encoding schemes: sinusoidal (current), learned embeddings, and a simple
binary encoding (e.g., [0,1,0,1,0] for ’a o b = c’). 2. Implement these
encoding schemes, ensuring they work with the existing sequence length. 3.
Run experiments for each encoding scheme across all datasets, tracking:
time to grokking (99%
training loss, and attention entropy. 4. Analyze how different encoding
schemes affect attention patterns and grokking behavior for each operation
type. 5. Compare generalization capabilities on sequences with shuffled
operands (e.g., ’b o a = c’). 6. Correlate encoding scheme performance with
operation complexity to identify potential interactions between input
representation and task structure. 7. Discuss implications for designing
transformers for specific algorithmic tasks based on findings.",
"Interestingness": 9,
"Feasibility": 9,
"Novelty": 9,
"novel": true
```

Idea 18/50 - adversarial_robustness_grokking

```
"Name": "adversarial_robustness_grokking",
"Title": "Adversarial Robustness During Grokking: Tracking Vulnerability
Evolution in Algorithmic Learning",
"Experiment": "1. Implement a simple perturbation method: randomly flip 1-2
bits in the input representation for modular arithmetic, and swap 1-2
elements for permutations. 2. Modify the training loop to generate
perturbed inputs and evaluate model performance on them every 500 steps. 3.
Track metrics: normal validation accuracy, accuracy on perturbed inputs,
and ’robustness gap’ (difference between normal and perturbed accuracy). 4.
Plot the evolution of robustness to perturbations alongside the grokking
curve. 5. Compare robustness before, during, and after grokking across
different operations. 6. Analyze examples of successful perturbations at
different stages of training. 7. Investigate potential correlations between
the timing of grokking and changes in robustness to perturbations.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 9,
"novel": true
```

Idea 19/50 - critical_periods_grokking

```
"Name": "critical_periods_grokking",
"Title": "Critical Periods in Grokking: The Impact of Timed Learning Rate
Spikes on Algorithmic Learning",
"Experiment": "1. Modify the training loop to support learning rate spikes
at specific points (25%
to apply these spikes, increasing the learning rate by 10x for 100 steps.
3. Run experiments for each spike timing across all datasets (modular
arithmetic and permutations), including a control group with no spikes. 4.
Track metrics: time to grokking, final validation accuracy, and ’spike
impact’ (change in validation accuracy slope in 500 steps post-spike). 5.
Plot learning curves highlighting spike points and their impacts. 6.
Analyze how spike timing affects grokking across different operations,
comparing modular arithmetic tasks with permutations. 7. Compare attention
patterns immediately before and after impactful spikes. 8. Correlate spike
impact with the stage of learning (pre-grokking, during grokking, post-
grokking) to identify potential critical periods, assessing whether these
periods are task-specific or general across operations.",
"Interestingness": 9,
"Feasibility": 9,
"Novelty": 9,
"novel": true
```

Idea 20/50 - lottery_tickets_grokking

```
"Name": "lottery_tickets_grokking",
"Title": "Lottery Tickets in Grokking: Investigating Sparse Subnetworks
Capable of Algorithmic Learning",
"Experiment": "1. Implement an iterative magnitude pruning function for the
Transformer model. 2. Modify the training loop to support multiple rounds
of train-prune-reset cycles. 3. For each dataset, run experiments with
pruning levels of 30%
iteration, train the network to convergence, prune the specified percentage
of smallest weights, then reset remaining weights to their initial values.
5. Track metrics for each sparse network: time to grokking (or maximum
training time if grokking doesn’t occur), final validation accuracy, and
training loss. 6. Introduce a ’grokking efficiency’ metric: the ratio of
time to grokking for the sparse network vs. the dense network. For networks
that don’t grok, use the maximum training time. 7. Plot learning curves for
each pruning level, highlighting grokking points and grokking efficiency.
8. Compare the structure of sparse networks that achieve grokking across
different operations, focusing on the distribution of preserved weights in
different layers and attention heads. 9. Analyze the correlation between
pruning level and grokking efficiency across different algorithmic tasks,
including cases where grokking fails to occur.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 8,
"novel": false
```

Idea 21/50 - algebraic_structure_grokking

```
"Name": "algebraic_structure_grokking",
"Title": "Grokking and Algebraic Structure: How Group Properties Influence
Neural Network Learning",
"Experiment": "1. Implement new dataset classes for modular multiplication
and division (modulo p, where p is prime, ensuring proper group
structures). 2. For each operation (addition, multiplication, division),
calculate and store two properties: group order and number of generators.
3. Run experiments for each operation type, tracking: time to grokking,
final validation accuracy, and the two group properties. 4. Plot learning
curves and grokking points for each operation, labeled with their group
properties. 5. Analyze the correlation between group properties and
grokking behavior (e.g., time to grokking, steepness of accuracy
improvement). 6. Compare attention patterns across operations, focusing on
how they reflect the underlying group structure (e.g., uniformity for
commutative operations). 7. Test the model’s ability to generalize by
evaluating on compositions of learned operations (e.g., a * b + c mod p)
after training on individual operations.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 9,
"novel": true
```

Idea 22/50 - mdl_grokking

```
"Name": "mdl_grokking",
"Title": "Minimum Description Length and Grokking: Investigating the
Relationship Between Model Compression and Algorithmic Learning",
"Experiment": "1. Implement functions to calculate model complexity: (a) L2
norm of weights, (b) number of bits to store parameters at different
precisions, (c) effective number of parameters using BIC. 2. Modify the
training loop to track these complexity measures alongside existing
metrics. 3. Run experiments across all datasets, recording complexity
measures, validation accuracy, and training loss at regular intervals. 4.
Plot the evolution of model complexity alongside the grokking curve. 5.
Analyze the correlation between sudden decreases in model complexity and
the onset of grokking, including statistical tests for significance. 6.
Compare complexity dynamics across different operations and model sizes. 7.
Visualize weight distributions at pre-grokking, during grokking, and post-
grokking stages. 8. Implement and compare two early stopping mechanisms:
one based on model complexity stabilization and another based on validation
loss stabilization.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 9,
"novel": true
```

Idea 23/50 - invariance_learning_grokking

```
"Name": "invariance_learning_grokking",
"Title": "Learning Invariances in Grokking: Tracking Symmetry Awareness
During Algorithmic Learning",
"Experiment": "1. Modify AbstractDataset to generate transformed versions
of inputs (cyclic shifts for modular arithmetic, relabelings for
permutations). 2. Update the evaluation function to test model predictions
on both original and transformed inputs. 3. Implement an ’invariance score’
metric: mean absolute difference between predictions on original and
transformed inputs. 4. Modify the training loop to calculate and store the
invariance score at regular intervals. 5. Run experiments across all
datasets, tracking the invariance score alongside existing metrics. 6. Plot
the evolution of the invariance score alongside the grokking curve. 7.
Analyze how the invariance score changes before, during, and after
grokking. 8. Compare invariance learning across different operations and
model sizes. 9. Investigate correlation between invariance score and
generalization performance.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 9,
"novel": true
```

Idea 24/50 - grokking_double_descent

```
"Name": "grokking_double_descent",
"Title": "Grokking and Double Descent: Exploring the Intersection of Two
Deep Learning Phenomena",
"Experiment": "1. Create a range of model sizes by varying num_layers (1 to
8) and dim_model (32 to 512). 2. For each dataset, train models of
different sizes, tracking validation accuracy, training loss, and time to
grokking (99%
parameters to identify double descent behavior. 4. On the same plot, mark
the point where grokking occurs for each model size. 5. Analyze the
relationship between grokking timing and the different regimes of the
double descent curve (under-parameterized, critical, over-parameterized).
6. Calculate the correlation between model size and time to grokking. 7.
Compare double descent and grokking behavior across different operations
(modular arithmetic vs. permutations). 8. Investigate whether grokking
consistently occurs in a specific regime of the double descent curve.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 9,
"novel": false
```

Idea 25/50 - ntk_alignment_grokking

```
"Name": "ntk_alignment_grokking",
"Title": "NTK-Output Alignment in Grokking: Tracking Feature Learning
Dynamics in Algorithmic Tasks",
"Experiment": "1. Implement a function to compute the NTK-output alignment:
the cosine similarity between the NTK’s top eigenvector and the output
gradient. 2. Modify the training loop to compute and store this alignment
metric every 100 steps. 3. Run experiments across all datasets, tracking
NTK-output alignment alongside validation accuracy and training loss. 4.
Plot the evolution of NTK-output alignment alongside the grokking curve. 5.
Analyze how the alignment changes before, during, and after grokking,
identifying any consistent patterns across different operations. 6.
Investigate correlations between sudden changes in alignment and the onset
of grokking. 7. Compare alignment dynamics for models that achieve grokking
vs. those that don’t. 8. Experiment with using the alignment metric as an
early stopping criterion or to adjust learning rates dynamically. 9.
Discuss implications of findings for understanding feature learning and
generalization in grokking.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 9,
"novel": true
```

Idea 26/50 - loss_landscape_grokking

```
"Name": "loss_landscape_grokking",
"Title": "Loss Landscape Evolution in Grokking: Geometric Insights into
Algorithmic Learning",
"Experiment": "1. Implement functions to compute and visualize 2D loss
landscapes using filter-wise normalization. 2. Modify the training loop to
save model checkpoints at key points: start of training, 25%
just before grokking (based on validation accuracy), during grokking, and
after grokking. 3. For each checkpoint, compute and store 2D loss landscape
visualizations. 4. Define quantitative metrics for loss landscape
characteristics: (a) local smoothness (average gradient magnitude), (b)
global convexity (ratio of loss at edges to center), (c) barrier height
(maximum loss along minimum loss path). 5. Run experiments across all
datasets, generating loss landscapes and computing metrics at key points.
6. Create side-by-side comparisons of loss landscapes at different stages
of training for each operation. 7. Analyze how loss landscape metrics
change before, during, and after grokking. 8. Compare loss landscape
evolution between operations that grok quickly vs. slowly. 9. Investigate
correlations between changes in loss landscape metrics and the onset of
grokking.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 8,
"novel": true
```

Idea 27/50 - neural_collapse_grokking

```
"Name": "neural_collapse_grokking",
"Title": "Neural Collapse in Grokking: Investigating Feature Geometry
During Algorithmic Learning",
"Experiment": "1. Modify Transformer to output final layer features. 2.
Implement functions to compute class means and covariances. 3. Calculate
simplified neural collapse metrics: (a) average cosine similarity between
class means, (b) ratio of within-class to between-class variances. 4. Track
these metrics every 500 steps during training. 5. Run experiments on
modular arithmetic and permutation datasets. 6. Plot neural collapse
metrics alongside grokking curves. 7. Analyze changes in metrics before,
during, and after grokking. 8. Compare neural collapse dynamics between
operations that grok quickly vs. slowly. 9. Visualize class mean
trajectories in 2D/3D using PCA. 10. Discuss implications for understanding
both grokking and general neural network learning dynamics.",
"Interestingness": 9,
"Feasibility": 6,
"Novelty": 9,
"novel": true
```

Idea 28/50 - data_augmentation_grokking

```
"Name": "data_augmentation_grokking",
"Title": "Data Augmentation in Grokking: The Impact of Input
Transformations on Algorithmic Learning",
"Experiment": "1. Implement task-specific augmentations: (a) For modular
arithmetic: add random offsets (mod p) to inputs. (b) For permutations:
apply random permutations to inputs and outputs. 2. Modify GroupDataset to
apply augmentations with 0%
for each augmentation level across all datasets. 4. Track metrics: time to
grokking (99%
’augmentation generalization gap’ (difference between augmented and non-
augmented validation accuracy). 5. Plot learning curves and generalization
gaps for each augmentation level. 6. Analyze the correlation between
augmentation level and grokking speed. 7. Compare attention patterns
between augmentation levels to understand representation changes. 8.
Discuss implications for designing data augmentation strategies in
algorithmic learning tasks.",
"Interestingness": 9,
"Feasibility": 9,
"Novelty": 8,
"novel": true
```

Idea 29/50 - emergent_grokking

```
"Name": "emergent_grokking",
"Title": "Emergent Abilities in Grokking: Investigating Scale-Dependent
Algorithmic Learning",
"Experiment": "1. Modify existing datasets to include ’simple’ and
’complex’ versions (e.g., mod sum with small vs. large primes). 2. Adjust
Transformer class to scale from tiny (1 layer, 64 dim) to medium (4 layers,
512 dim). 3. For each operation, train models of increasing size, tracking
grokking time and performance on both simple and complex versions. 4.
Implement a generalization test for each operation (e.g., mod sum with even
larger primes). 5. Plot learning curves for different model sizes,
highlighting grokking points. 6. Create heatmaps of model size vs.
operation complexity, showing grokking time and generalization test
results. 7. Perform statistical analysis to identify significant jumps in
performance across model sizes, using metrics such as accuracy increase
rate and time to reach 99%
behavior patterns across different operation types.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 9,
"novel": true
```

Idea 30/50 - functional_modularity_grokking

```
"Name": "functional_modularity_grokking",
"Title": "Functional Modularity in Grokking: Analyzing Emergent
Specialization in Transformer Networks During Algorithmic Learning",
"Experiment": "1. Implement functions to track weight update patterns and
attention focus for each layer and head. 2. Modify the training loop to
compute and store these metrics at regular intervals. 3. Define a
’functional modularity score’ based on the consistency of weight updates
and attention patterns for specific input types. 4. Run experiments across
all datasets, tracking the functional modularity score alongside existing
metrics. 5. Plot the evolution of functional modularity alongside the
grokking curve. 6. Analyze how functional modularity changes before,
during, and after grokking. 7. Visualize the most consistent patterns at
different stages of training and interpret their functions. 8. Compare
functional modularity dynamics between different operations and model
sizes. 9. Investigate correlations between functional modularity and
grokking speed or generalization performance.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 9,
"novel": true
```

Idea 31/50 - information_compression_grokking

```
"Name": "information_compression_grokking",
"Title": "Information Compression in Grokking: Analyzing Representational
Dynamics During Algorithmic Learning",
"Experiment": "1. Modify Transformer class to include a bottleneck layer
(smaller dimension linear layer) after the encoder. 2. Implement function
to compute activation sparsity (%
bottleneck layer. 3. Update training loop to compute and store activation
sparsity and gradient magnitudes of the bottleneck layer at regular
intervals. 4. Run experiments with different bottleneck sizes (e.g., 25%
50%
to grokking, final validation accuracy, activation sparsity, and gradient
magnitudes. 6. Plot activation sparsity and gradient magnitude evolution
alongside grokking curves for each bottleneck size. 7. Analyze how these
metrics change before, during, and after grokking. 8. Test generalization
by evaluating models on slightly out-of-distribution examples (e.g., larger
numbers in modular arithmetic). 9. Investigate correlation between optimal
compression (measured by activation sparsity) and grokking speed,
generalization performance.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 8,
"novel": true
```

Idea 32/50 - critical_learning_periods_grokking

```
"Name": "critical_learning_periods_grokking",
"Title": "Critical Learning Periods in Grokking: Temporal Dynamics of
Algorithmic Understanding",
"Experiment": "1. Modify the training loop to support ’intervention
periods’ where learning rate is increased by 5x for 100 steps. 2. Implement
a sliding window intervention strategy, with windows of 500 steps, starting
every 250 steps. 3. Run experiments for each window across all datasets and
three model sizes (small, medium, large), including a control group with no
interventions. 4. Track metrics: time to grokking, final validation
accuracy, and ’intervention impact’ (area under the validation accuracy
curve for 500 steps post-intervention). 5. Plot learning curves
highlighting intervention windows and their impacts. 6. Create heatmaps
visualizing intervention impact across time windows and model sizes for
each operation. 7. Analyze how intervention timing affects grokking across
different operations and model sizes. 8. Compare attention patterns
immediately before and after impactful interventions. 9. Investigate
whether certain operations or model sizes have more pronounced critical
periods than others. 10. Discuss implications for curriculum design in
machine learning and potential applications in continual and transfer
learning.",
"Interestingness": 9,
"Feasibility": 7,
"Novelty": 9,
"novel": true
```

Idea 33/50 - simplicity_bias_grokking

```
"Name": "simplicity_bias_grokking",
"Title": "Simplicity Bias in Grokking: Analyzing Weight Matrix Complexity
During Algorithmic Learning",
"Experiment": "1. Modify AbstractDataset to include two complexity levels
for each operation (e.g., small vs. large prime for modular arithmetic,
short vs. long permutations). 2. Implement a function to compute the
effective rank of weight matrices using singular value decomposition. 3.
Update the training loop to compute and store the effective rank for each
layer every 500 steps. 4. Run experiments across all datasets and both
complexity levels, tracking effective rank alongside existing metrics. 5.
Plot the evolution of effective rank alongside grokking curves for each
complexity level and operation. 6. Analyze how effective rank changes
before, during, and after grokking, and how this relates to task
complexity. 7. Investigate correlations between effective rank dynamics and
grokking speed or generalization performance. 8. Compare effective rank
patterns across different operations and model sizes. 9. Contrast effective
rank dynamics between operations that grok quickly versus those that grok
slowly or fail to grok. 10. Experiment with using effective rank as an
indicator for the onset of grokking.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 9,
"novel": true
```

Idea 34/50 - lucky_initializations_grokking

```
"Name": "lucky_initializations_grokking",
"Title": "Lucky Initializations in Grokking: Identifying and Analyzing
Favorable Starting Points for Algorithmic Learning",
"Experiment": "1. Implement a function to generate and store 50 random
initializations for the Transformer model. 2. Modify the training loop to
support training from stored initializations and different learning rates.
3. For each dataset, train models from the 50 initializations with 3
learning rates, tracking ’grokking efficiency’ (ratio of validation
accuracy to training steps at 99%
initializations (top 20%
characteristics of lucky initializations: weight distribution statistics,
layerwise norms, and attention pattern initialization. 6. Implement a
function to visualize the loss landscape around initial points using
filter-wise normalization. 7. Compare lucky initializations across
different operations to identify common patterns. 8. Develop a simple
predictor for initialization ’luckiness’ based on identified
characteristics. 9. Test transfer of lucky initializations across tasks and
learning rates.",
"Interestingness": 9,
"Feasibility": 9,
"Novelty": 9,
"novel": true
```

Idea 35/50 - relative_attention_grokking

```
"Name": "relative_attention_grokking",
"Title": "Relative Positional Attention and Its Impact on Grokking in
Algorithmic Learning",
"Experiment": "1. Modify the DecoderBlock class to support two attention
types: standard (current) and relative positional. 2. Implement relative
positional attention, ensuring it works with the existing sequence length.
3. Update the Transformer class to accept an attention_type parameter. 4.
Run experiments for both attention types across all datasets, tracking:
time to grokking (99%
training loss, grokking transition sharpness (rate of validation accuracy
increase), and post-grokking stability (variance in validation accuracy
after reaching 99%
highlighting grokking points and transition periods. 6. Visualize and
compare attention patterns between the two mechanisms at key stages: pre-
grokking, during grokking transition, and post-grokking. 7. Analyze how
relative positional attention affects grokking behavior, transition
sharpness, and stability for each operation type compared to standard
attention. 8. Investigate correlations between attention type and grokking
speed or post-grokking stability. 9. Discuss implications for designing
transformers for specific algorithmic tasks based on findings.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 8,
"novel": true
```

Idea 36/50 - grokking_task_interference

```
"Name": "grokking_task_interference",
"Title": "Grokking and Task Interference: Exploring the Stability of
Algorithmic Understanding",
"Experiment": "1. Modify the training loop to support learning two modular
arithmetic operations sequentially (e.g., addition then multiplication). 2.
Implement a task scheduler that switches between tasks at regular
intervals. 3. Create a ’dual-task evaluation’ function to assess
performance on both tasks simultaneously. 4. Track metrics: time to
grokking for each task, performance on the first task while learning the
second, and a ’grokking stability’ score (maintenance of >95%
task 1 while learning task 2). 5. Run experiments with different task
switching frequencies. 6. Analyze how grokking on one task affects learning
speed and grokking on the subsequent task. 7. Visualize attention patterns
before and after introducing the second task to understand representation
changes. 8. Investigate the correlation between grokking speed on the first
task and stability of that understanding when learning the second task. 9.
Compare results with a baseline of learning both tasks simultaneously to
isolate the effects of sequential learning.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 9,
"novel": true
```

Idea 37/50 - attention_inductive_bias_grokking

```
"Name": "attention_inductive_bias_grokking",
"Title": "Inductive Biases in Attention Mechanisms: Their Impact on
Grokking in Algorithmic Learning",
"Experiment": "1. Modify DecoderBlock class to support two attention
mechanisms: standard dot-product and additive (Bahdanau). 2. Implement
these attention mechanisms, ensuring compatibility with existing
architecture. 3. Update Transformer class to accept an attention_type
parameter. 4. Select a subset of most illustrative datasets based on
preliminary experiments. 5. Run experiments for each attention type on
selected datasets, tracking: time to grokking (99%
final validation accuracy, training loss, and ’grokking transition
sharpness’ (defined as the maximum rate of validation accuracy increase
over any 500-step window). 6. Implement a simple generalization test using
slightly out-of-distribution examples (e.g., larger numbers for modular
arithmetic). 7. Plot learning curves for each attention type, highlighting
grokking points and transition periods. 8. Analyze how different attention
mechanisms affect grokking behavior, transition sharpness, and
generalization performance for each operation type. 9. Visualize attention
patterns for each mechanism at key stages: pre-grokking, during grokking
transition, and post-grokking. 10. Discuss implications for designing
transformers with appropriate inductive biases for specific types of
algorithmic learning tasks.",
"Interestingness": 9,
"Feasibility": 9,
"Novelty": 9,
"novel": true
```

Idea 38/50 - gradient_dynamics_grokking

```
"Name": "gradient_dynamics_grokking",
"Title": "Gradient Dynamics in Grokking: Analyzing Information Flow
Efficiency During Algorithmic Learning",
"Experiment": "1. Modify the training loop to compute gradient statistics
(sparsity and magnitude distribution) for each layer. 2. Implement
functions to calculate gradient sparsity (%
magnitude percentiles. 3. Update training process to store these metrics
every 500 steps. 4. Run experiments across all datasets, tracking gradient
metrics alongside existing performance metrics. 5. Plot the evolution of
gradient sparsity and magnitude distributions alongside grokking curves. 6.
Analyze how gradient dynamics change before, during, and after grokking. 7.
Compare gradient patterns between operations that grok quickly vs. slowly.
8. Investigate correlations between changes in gradient dynamics and
grokking speed or generalization performance. 9. Visualize gradient flow
patterns at key stages: pre-grokking, during grokking transition, and post-
grokking.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 8,
"novel": true
```

Idea 39/50 - adaptive_curriculum_grokking

```
"Name": "adaptive_curriculum_grokking",
"Title": "Adaptive Curriculum Learning in Grokking: Optimizing Example
Difficulty for Efficient Algorithmic Understanding",
"Experiment": "1. Modify AbstractDataset to include a difficulty scoring
function (e.g., input magnitude for modular arithmetic, cycle length for
permutations). 2. Implement adaptive sampling strategy: start with easiest
20%
level exceeds 90%
tracking difficulty of selected examples. 4. Run experiments comparing
adaptive curriculum, random sampling, and static curriculum (increasing
difficulty linearly) across all datasets. 5. Track metrics: time to
grokking, final validation accuracy, learning trajectory smoothness, and
example difficulty distribution over time. 6. Analyze relationship between
difficulty progression and grokking onset. 7. Visualize learning curves and
difficulty progression for each strategy. 8. Compare consistency and speed
of grokking across different random seeds for each strategy. 9. Analyze
computational efficiency by comparing total number of examples needed to
achieve grokking for each strategy. 10. Compare attention patterns at key
points (pre-grokking, during grokking, post-grokking) across strategies to
understand how adaptive curriculum affects internal representations.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 9,
"novel": true
```

Idea 40/50 - task_structure_grokking

```
"Name": "task_structure_grokking",
"Title": "Task Structure and Grokking: Investigating the Relationship
Between Algorithmic Complexity and Learning Dynamics",
"Experiment": "1. Modify AbstractDataset to include a
’structural_complexity’ score based on: a) number of unique outputs, b)
input-output correlation, c) algebraic degree for modular operations or
cycle structure for permutations. 2. Extend existing dataset classes to
include a wider range of operations (e.g., modular addition,
multiplication, exponentiation; simple and complex permutations). 3. Run
experiments across all operations, tracking time to grokking, final
validation accuracy, and learning curve smoothness. 4. Plot grokking
metrics against structural complexity scores, comparing trends between
modular arithmetic and permutation tasks. 5. Analyze correlation between
structural complexity and grokking behavior. 6. Compare attention patterns
and gradient flows across tasks of different complexity. 7. Implement a
generalization test where models trained on simpler structures are
evaluated on more complex ones. 8. Discuss implications for neural network
learning on structured vs. unstructured tasks in general machine learning
contexts.",
"Interestingness": 9,
"Feasibility": 9,
"Novelty": 9,
"novel": true
```

Idea 41/50 - numerical_base_grokking

```
"Name": "numerical_base_grokking",
"Title": "Numerical Base and Grokking: How Input Representation Affects
Pattern Recognition in Algorithmic Learning",
"Experiment": "1. Modify AbstractDataset and modular arithmetic dataset
classes to support binary and decimal bases. 2. Implement functions to
convert between bases and adjust the encode/decode methods. 3. Update the
Transformer class to handle variable input lengths. 4. Run experiments for
binary and decimal bases on modular addition and multiplication tasks. 5.
Track metrics: time to grokking (99%
accuracy, training loss, and ’cross-base generalization’ (accuracy when
testing on the other base). 6. Plot learning curves for each base,
highlighting grokking points. 7. Compare learning curves for binary (0-3)
vs decimal (0-9) to isolate base effects from sequence length. 8. Analyze
how different bases affect grokking speed and pattern recognition. 9.
Compare attention patterns across bases at key stages: pre-grokking, during
grokking, and post-grokking. 10. Discuss implications for choosing input
representations in mathematical machine learning tasks.",
"Interestingness": 9,
"Feasibility": 9,
"Novelty": 9,
"novel": true
```

Idea 42/50 - activation_function_grokking

```
"Name": "activation_function_grokking",
"Title": "Activation Functions and Grokking: Investigating the Role of Non-
linearity in Algorithmic Learning and Generalization",
"Experiment": "1. Modify the DecoderBlock class to support multiple
activation functions (ReLU, GELU, Tanh). 2. Update the Transformer class to
accept an activation_type parameter, allowing for both uniform and hybrid
activation setups. 3. Run experiments comparing the baseline (GELU) with
ReLU, Tanh, and a hybrid setup (ReLU in lower layers, Tanh in upper layers)
across all datasets. 4. Track metrics: time to grokking (99%
accuracy), final validation accuracy, training loss, ’grokking transition
sharpness’, and gradient flow statistics. 5. Plot learning curves for each
activation setup, highlighting grokking points and transition periods. 6.
Visualize decision boundaries at different training stages for each
activation setup. 7. Analyze how different activation functions affect
grokking behavior, transition sharpness, and final performance for each
operation type. 8. Compare hidden representations (using t-SNE) across
activation setups at key stages: pre-grokking, during grokking transition,
and post-grokking. 9. Investigate the relationship between activation
function properties and the trade-off between memorization and
generalization. 10. Discuss implications for choosing activation functions
in tasks requiring pattern discovery and generalization beyond algorithmic
learning.",
"Interestingness": 9,
"Feasibility": 9,
"Novelty": 9,
"novel": true
```

Idea 43/50 - phase_transition_grokking

```
"Name": "phase_transition_grokking",
"Title": "Grokking as a Phase Transition: Characterizing Critical Behavior
in Algorithmic Learning",
"Experiment": "1. Implement functions to track key metrics: validation
accuracy, training loss, gradient norm, and weight norm. 2. Modify training
loop to compute and store these metrics every 100 steps. 3. Run experiments
across all datasets, with finer-grained tracking (every 10 steps) around
the suspected grokking point. 4. Implement analysis tools to detect sudden
changes or discontinuities in metrics. 5. Plot all metrics on a single,
multi-axis graph to visualize potential phase transitions. 6. Calculate
susceptibility using fluctuations in validation accuracy near the grokking
point. 7. Analyze scaling behavior of susceptibility to identify critical
exponents, if any. 8. Compare phase transition characteristics across
different operations and model sizes. 9. Investigate whether manipulating
learning rate or gradient clipping can induce or prevent grokking phase
transitions.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 9,
"novel": false
```

Idea 44/50 - effective_dimension_grokking

```
"Name": "effective_dimension_grokking",
"Title": "Effective Dimension Dynamics in Grokking: Analyzing
Representational Complexity During Algorithmic Learning",
"Experiment": "1. Implement functions to compute the rank and top-k
singular values of weight matrices. 2. Modify the training loop to compute
and store these metrics every 500 steps for each layer. 3. Run experiments
across all datasets, tracking rank and singular value distributions
alongside existing performance metrics. 4. Implement a simple MLP baseline
that doesn’t exhibit grokking for comparison. 5. Plot the evolution of rank
and singular value distributions alongside grokking curves for both
Transformer and MLP models. 6. Analyze how these metrics change before,
during, and after grokking in the Transformer, contrasting with the MLP. 7.
Compare rank dynamics between operations that grok quickly vs. slowly. 8.
Investigate correlations between changes in rank/singular values and
grokking speed or generalization performance. 9. Visualize the relationship
between these metrics and other performance indicators at different stages
of training.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 9,
"novel": true
```

Idea 45/50 - representation_entropy_grokking

```
"Name": "representation_entropy_grokking",
"Title": "Representation Entropy in Grokking: Tracking the Simplification
of Learned Concepts",
"Experiment": "1. Implement a function to compute the entropy of the
model’s internal representations. 2. Modify the Transformer class to output
intermediate representations. 3. Update the training loop to compute and
store the representation entropy every 500 steps. 4. Run experiments across
all datasets, including configurations that lead to successful grokking and
those that don’t (e.g., by varying model size or learning rate). 5. Track
entropy alongside existing performance metrics. 6. Plot the evolution of
representation entropy alongside grokking curves for both successful and
unsuccessful cases. 7. Analyze how representation entropy changes before,
during, and after grokking in successful cases, and compare with
unsuccessful cases. 8. Investigate correlations between changes in
representation entropy and grokking speed or generalization performance. 9.
Visualize the relationship between entropy and other performance indicators
at different stages of training. 10. Plot entropy distributions across
different layers of the model to understand how different parts contribute
to concept simplification.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 8,
"novel": true
```

Idea 46/50 - mutual_information_grokking

```
"Name": "mutual_information_grokking",
"Title": "Mutual Information Dynamics in Grokking: Tracing Information Flow
During Algorithmic Learning",
"Experiment": "1. Modify Transformer class to output representations from
input embedding, middle layer, and final layer. 2. Implement MINE (Mutual
Information Neural Estimation) for efficient mutual information
approximation. 3. Update training loop to compute and store mutual
information estimates between input-middle, input-output, and middle-output
every 500 steps. 4. Run experiments across all datasets, tracking mutual
information alongside existing performance metrics. 5. Plot the evolution
of mutual information alongside grokking curves and generalization gap. 6.
Analyze how mutual information changes before, during, and after grokking,
particularly in relation to the generalization gap. 7. Compare mutual
information dynamics between operations that grok quickly vs. slowly. 8.
Investigate correlations between changes in mutual information and grokking
speed or generalization performance.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 8,
"novel": true
```

Idea 47/50 - lottery_tickets_grokking

```
"Name": "lottery_tickets_grokking",
"Title": "Lottery Tickets in Grokking: Sparse Subnetworks and Sudden
Generalization",
"Experiment": "1. Implement iterative magnitude pruning for the Transformer
model. 2. Modify training loop for train-prune-reset cycles. 3. For each
dataset, run experiments with pruning levels of 50%
iterations. 4. Track metrics: time to grokking, final validation accuracy,
training loss, and ’grokking efficiency’ (ratio of time to grokking for
sparse vs. dense network). 5. Plot learning curves for each pruning level,
highlighting grokking points. 6. Compare sparse network structures that
achieve grokking across operations. 7. Analyze correlation between pruning
level and grokking efficiency. 8. Implement simple MLP baseline without
grokking for comparison. 9. Visualize weight distributions of winning
tickets pre- and post-grokking.",
"Interestingness": 9,
"Feasibility": 9,
"Novelty": 8,
"novel": false
```

Idea 48/50 - architecture_inductive_bias_grokking

```
"Name": "architecture_inductive_bias_grokking",
"Title": "Architectural Inductive Biases and Grokking: Comparing Sudden
Generalization Across Neural Network Types",
"Experiment": "1. Implement simplified 1D CNN and LSTM model classes
compatible with existing sequence-based datasets. 2. Modify training loop
to support multiple model types. 3. Run experiments comparing Transformer,
1D CNN, and LSTM models across modular arithmetic datasets. 4. Track
metrics: time to grokking, final validation accuracy, training loss, and
architecture-specific indicators (attention patterns for Transformer,
filter activations for CNN, forget gate activations for LSTM). 5. Plot
learning curves for each architecture, highlighting grokking points. 6.
Analyze how different architectures affect grokking behavior, speed, and
final performance for each operation type. 7. Compare internal
representations (using t-SNE) across architectures at key stages: pre-
grokking, during grokking transition, and post-grokking. 8. Investigate the
relationship between architectural inductive biases and the trade-off
between memorization and generalization in modular arithmetic tasks.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 8,
"novel": true
```

Idea 49/50 - shortcut_learning_grokking

```
"Name": "shortcut_learning_grokking",
"Title": "Shortcut Learning and Grokking: The Interplay Between Surface
Patterns and Deep Understanding in Algorithmic Learning",
"Experiment": "1. Modify AbstractDataset to include operation-specific
shortcuts: for modular arithmetic, make the result always even if the first
operand is even; for permutations, always swap the first two elements. 2.
Implement a function to gradually remove these shortcuts over training by
reducing their frequency. 3. Update the training loop to apply the shortcut
removal function. 4. Add a ’shortcut reliance’ metric: the accuracy
difference between shortcut-following and shortcut-violating examples. 5.
Run experiments with varying shortcut removal rates across datasets. 6.
Track metrics: time to grokking, final validation accuracy, shortcut
reliance over time, and performance on a shortcut-free test set. 7. Plot
learning curves and shortcut reliance alongside grokking curves. 8. Analyze
how shortcut presence and removal affect grokking timing and quality. 9.
Compare attention patterns between models trained with and without
shortcuts at key stages.",
"Interestingness": 9,
"Feasibility": 9,
"Novelty": 9,
"novel": true
```

Idea 50/50 - grokking_forgetting_complexity

```
"Name": "grokking_forgetting_complexity",
"Title": "Grokking and Forgetting: The Interplay of Task Complexity and
Sudden Generalization in Algorithmic Learning",
"Experiment": "1. Modify ModSumDataset to support multiple complexity
levels (e.g., modular addition with increasing prime moduli). 2. Update the
training loop to gradually introduce higher complexity levels while
continuously evaluating on all levels. 3. Implement a ’multi-complexity
evaluation’ function to assess performance across all complexity levels
simultaneously. 4. Track metrics: time to grokking for each complexity
level, performance on lower complexity levels when grokking occurs on a
higher level, and a ’complexity forgetting score’ (decrease in accuracy on
lower complexity levels). 5. Analyze the correlation between grokking
events and performance changes on other complexity levels. 6. Compare
internal representations (using cosine similarity of hidden states) across
complexity levels before and after grokking events. 7. Investigate trends
in grokking speed across increasing complexity levels. 8. Plot learning
curves for all complexity levels simultaneously, highlighting grokking
points and potential forgetting events. 9. Visualize the evolution of
representation similarities over time using heatmaps.",
"Interestingness": 9,
"Feasibility": 9,
"Novelty": 9,
"novel": true
```

## Appendix D Highlighted Generated Papers

In the following section, we present highlighted examples of generated papers from The AI Scientist.
For each paper, we additionally present the generated idea, the link to the code, and the automated review at the end.

### D.1 DualScale Diffusion: Adaptive Feature Balancing for Low-Dimensional Generative Models

This idea was proposed in the 6th iteration of a Sonnet 3.5 run.

Idea

```
"Name": "adaptive_dual_scale_denoising",
"Title": "Adaptive Dual-Scale Denoising for Dynamic Feature Balancing in
Low-Dimensional Diffusion Models",
"Experiment": "Modify MLPDenoiser to implement a dual-scale processing
approach with two parallel branches: a global branch for the original input
and a local branch for an upscaled input. Introduce a learnable, timestep-
conditioned weighting factor to dynamically balance the contributions of
global and local branches. Train models with both the original and new
architecture on all datasets. Compare performance using KL divergence and
visual inspection of generated samples. Analyze how the weighting factor
evolves during the denoising process and its impact on capturing global
structure vs. local details across different datasets and timesteps.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 8,
"novel": true
```

Link to code: <https://github.com/SakanaAI/AI-Scientist/tree/main/example_papers/adaptive_dual_scale_denoising>.

See pages - of [highlighted_papers/diffusion/adaptive_dual_scale_denoising/adaptive_dual_scale_denoising.pdf](https://highlighted_papers/diffusion/adaptive_dual_scale_denoising/adaptive_dual_scale_denoising.pdf)

Review

```
"Summary": "The paper introduces an adaptive dual-scale denoising approach
for low-dimensional diffusion models, aiming to balance global structure
and local details in generated samples. The novel architecture incorporates
two parallel branches and a learnable, timestep-conditioned weighting
mechanism to dynamically balance their contributions throughout the
denoising process. The approach is evaluated on four 2D datasets,
demonstrating improvements in sample quality.",
"Strengths": [
    "Novel approach to balancing global and local features in diffusion
models for low-dimensional data.",
    "Comprehensive empirical evaluation on multiple 2D datasets.",
    "Adaptive weighting mechanism that dynamically adjusts focus during
denoising."
],
"Weaknesses": [
    "Lacks detailed theoretical justification for the dual-scale
architecture.",
    "Computational cost is significantly higher, which may limit practical
applicability.",
    "Some sections are not clearly explained, such as the autoencoder
aggregator and weight evolution analysis.",
    "Limited diversity in the datasets used for evaluation. More complex,
real-world datasets could strengthen claims.",
    "Insufficient ablation studies and analysis on specific design choices
like different types of aggregators."
],
"Originality": 4,
"Quality": 3,
"Clarity": 3,
"Significance": 3,
"Questions": [
    "Can you provide a more detailed theoretical justification for the
dual-scale architecture?",
    "What impact do different types of aggregators have on the model’s
performance?",
    "How does the model perform on more complex, real-world low-dimensional
datasets?",
    "Can the computational cost be reduced without sacrificing
performance?"
],
"Limitations": [
    "The paper should address the high computational cost and explore ways
to optimize it.",
    "The limited diversity of datasets and lack of detailed theoretical
backing for the proposed architecture are notable limitations."
],
"Ethical Concerns": false,
"Soundness": 3,
"Presentation": 3,
"Contribution": 3,
"Overall": 5,
"Confidence": 4,
"Decision": "Reject"
```

### D.2 Multi-scale Grid Noise Adaptation: Enhancing Diffusion Models For Low-dimensional Data

This idea was proposed in the 35th iteration of a Claude run.

Idea

```
"Name": "grid_based_noise_adaptation",
"Title": "Grid-Based Noise Adaptation for Enhanced Low-Dimensional
Diffusion Models",
"Experiment": "1. Modify NoiseScheduler to support grid-based noise level
adjustments. 2. Implement a simple grid structure (e.g., 10x10) to store
learnable noise adjustment factors. 3. Adjust MLPDenoiser to incorporate
the grid-based noise level in its computations. 4. Modify the training loop
to include the grid parameters in the optimization process. 5. Adapt the
sampling process to use the grid-based noise levels during inference. 6.
Train models with both standard and grid-based noise adaptation approaches
on all datasets. 7. Compare KL divergence, sample quality, and convergence
speed between the two approaches. 8. Introduce a ’noise adaptation
effectiveness’ metric by measuring the variance of learned grid values. 9.
Visualize the learned noise adjustment grid at different timesteps. 10.
Analyze computational overhead and discuss trade-offs between model
complexity and performance gains.",
"Interestingness": 9,
"Feasibility": 9,
"Novelty": 9,
"novel": true
```

Link to code: <https://github.com/SakanaAI/AI-Scientist/tree/main/example_papers/grid_based_noise_adaptation>.

See pages - of [highlighted_papers/diffusion/grid_based_noise_adaptation/grid_based_noise_adaptation.pdf](https://highlighted_papers/diffusion/grid_based_noise_adaptation/grid_based_noise_adaptation.pdf)

Review

```
"Summary": "The paper introduces a multi-scale grid-based noise adaptation
mechanism for diffusion models to improve their performance on low-
dimensional datasets. It employs a combination of coarse (5x5) and fine
(20x20) grids to dynamically adjust noise levels during the diffusion
process, with L1 regularization encouraging sparsity in fine-grained
adjustments. The approach is evaluated on four 2D datasets: circle, dino,
line, and moons, showing improvements in sample quality and distribution
matching.",
"Strengths": [
    "The paper addresses a relevant problem in the application of diffusion
models to low-dimensional data.",
    "The proposed multi-scale grid-based noise adaptation mechanism is
novel and shows potential.",
    "The experimental results demonstrate improvements in sample quality
and distribution matching on several 2D datasets."
],
"Weaknesses": [
    "The paper lacks clarity in some sections, especially regarding the
detailed implementation of the proposed method.",
    "The experiments, while showing improvements, lack comprehensive
analyses and more ablation studies.",
    "The potential societal impact and limitations of the proposed method
are not adequately discussed.",
    "The paper does not compare the proposed method with a wide range of
existing methods, limiting the context of its contributions.",
    "There are some formatting issues, such as missing figure captions
(e.g., Figure 2).",
    "The choice of datasets, while diverse, needs better justification in
terms of their relevance and representativeness for broader applications.",
    "The computational overhead and training time increases are significant
and need more discussion regarding their practical implications."
],
"Originality": 3,
"Quality": 2,
"Clarity": 2,
"Significance": 3,
"Questions": [
    "Can the authors provide more detailed explanations of the multi-scale
grid-based noise adaptation mechanism?",
    "How does the performance of the proposed method compare to other
state-of-the-art methods for low-dimensional data generation?",
    "Can the authors discuss the potential societal impact and limitations
of their work in more detail?",
    "Can the authors provide more detailed ablation studies to isolate the
impact of coarse and fine grids, as well as L1 regularization?",
    "How does the proposed method perform on higher-dimensional datasets,
and what are the challenges anticipated in such scenarios?",
    "Can the authors elaborate on the choice of the specific grid sizes
(5x5 and 20x20)? Have alternative configurations been tested?",
    "Can the authors provide more visualizations for the generated samples,
particularly for the dino and moons datasets?",
    "Can you provide a detailed explanation of the L1 regularization term
and its impact on the results?"
],
"Limitations": [
    "The paper does not discuss the potential societal impact and
limitations of the proposed method in sufficient detail. It would be
beneficial to address these aspects to provide a more comprehensive
understanding of the work’s implications.",
    "The paper does not address the potential computational overhead and
increased training time associated with the proposed method.",
    "There is limited discussion on the generalizability of the approach to
higher-dimensional datasets or other types of data.",
    "The paper does not thoroughly address potential limitations of the
proposed method, such as increased computational complexity and dataset-
specific tuning requirements.",
    "The method’s effectiveness on higher-dimensional datasets remains
unexplored.",
    "Increased computational costs for training and inference."
],
"Ethical Concerns": false,
"Soundness": 2,
"Presentation": 2,
"Contribution": 2,
"Overall": 4,
"Confidence": 4,
"Decision": "Reject"
```

### D.3 Gan-Enhanced Diffusion: Boosting Sample Quality and Diversity

This idea was proposed in the 14th iteration of a GPT-4o run.

Idea

```
"Name": "gan_diffusion",
"Title": "Enhancing Diffusion Models with Generative Adversarial Networks
for Improved Sample Quality",
"Experiment": "In this experiment, we will integrate a GAN framework into
the diffusion model. Specifically, we will: (1) Implement a simple
discriminator network to distinguish between real and generated samples,
using a small MLP architecture, (2) Modify the MLPDenoiser to include an
adversarial loss term along with the existing reconstruction loss, using a
gradient penalty to improve training stability, (3) Adjust the training
loop to alternately train the discriminator and the denoiser, ensuring that
the denoiser learns to produce more realistic samples based on the feedback
from the discriminator, (4) Train the GAN-enhanced diffusion model on the
same datasets, and (5) Compare the results in terms of training time,
evaluation loss, KL divergence, and sample quality using both quantitative
metrics (e.g., KL divergence) and qualitative visual inspection.",
"Interestingness": 10,
"Feasibility": 8,
"Novelty": 10,
"novel": true
```

Link to code: <https://github.com/SakanaAI/AI-Scientist/tree/main/example_papers/gan_diffusion>.

See pages - of [highlighted_papers/diffusion/gan_diffusion/gan_diffusion.pdf](https://highlighted_papers/diffusion/gan_diffusion/gan_diffusion.pdf)

Review

```
"Summary": "The paper proposes integrating a Generative Adversarial Network
(GAN) framework into diffusion models to improve sample quality and
diversity. The approach includes a simple discriminator network, an
adversarial loss term, and a gradient penalty to the adversarial loss.
Extensive experiments on multiple 2D datasets are conducted to validate the
approach, comparing results in terms of training time, evaluation loss, KL
divergence, and sample quality.",
"Strengths": [
    "The integration of GAN framework with diffusion models is a novel
approach to improve sample quality and diversity.",
    "The introduction of a gradient penalty to improve training stability
is a thoughtful addition.",
    "The paper provides a comprehensive evaluation on multiple 2D datasets,
using various metrics such as training time, evaluation loss, KL
divergence, and sample quality."
],
"Weaknesses": [
    "The methodology section lacks detailed explanations for certain
components, such as the exact architecture of the discriminator network and
the choice of hyperparameters.",
    "The improvements in evaluation loss and KL divergence are not
consistent across all datasets, indicating that the model’s performance may
be dataset-dependent.",
    "The experimental scope is limited to 2D datasets. Further research is
needed to evaluate the model’s performance on higher-dimensional data.",
    "The paper lacks sufficient ablation studies to isolate the
contributions of different components of the proposed method.",
    "The evaluation metrics are somewhat limited; including metrics like
FID could strengthen the evaluation.",
    "The paper does not sufficiently address the limitations of the
approach, particularly its dataset dependency and scalability to higher-
dimensional data.",
    "There is no discussion on potential negative societal impacts or
ethical concerns related to the work."
],
"Originality": 3,
"Quality": 2,
"Clarity": 2,
"Significance": 2,
"Questions": [
    "Can you provide more details on the architecture of the discriminator
network?",
    "How do the hyperparameters lambda-adv and lambda-gp affect the model’s
performance?",
    "Can you explain why the improvements are inconsistent across different
datasets?",
    "Can the authors provide more detailed descriptions of the denoiser and
discriminator networks?",
    "Have the authors considered using more comprehensive evaluation
metrics like FID?",
    "Can the authors provide more ablation studies to isolate the
contributions of the gradient penalty and adversarial loss?",
    "How would the proposed method perform on more complex and higher-
dimensional datasets?"
],
"Limitations": [
    "The paper acknowledges the increased training time and dataset
dependency of the improvements. However, it could benefit from a more
thorough exploration of different architectures and higher-dimensional
datasets.",
    "The empirical results show mixed improvements, indicating that the
model’s performance may be dataset-dependent.",
    "The paper does not explore the limitations of the proposed approach in
depth, particularly in terms of scalability to higher-dimensional data."
],
"Ethical Concerns": false,
"Soundness": 2,
"Presentation": 2,
"Contribution": 2,
"Overall": 3,
"Confidence": 4,
"Decision": "Reject"
```

### D.4 DualDiff: Enhancing Mode Capture in Low-dimensional Diffusion Models via Dual-expert Denoising

This idea was proposed in the 5th iteration of a Claude run.

Idea

```
"Name": "dual_expert_denoiser",
"Title": "Dual-Expert Denoiser for Improved Mode Capture in Low-Dimensional
Diffusion Models",
"Experiment": "Modify MLPDenoiser to implement a dual-expert architecture.
Create a simple gating network that outputs a single weight (sigmoid
output) based on the noisy input and timestep. Implement two expert
networks with the same structure as the original denoising network. Combine
expert outputs using the gating weight. Train models with both the original
and new architecture on all datasets, with particular focus on ’moons’ and
’dino’. Compare performance using KL divergence, sample diversity metrics
(e.g., number of modes captured), and visual inspection of generated
samples. Analyze the specialization of experts across different regions of
the data distribution.",
"Interestingness": 8,
"Feasibility": 8,
"Novelty": 8,
"novel": true
```

Link to code: <https://github.com/SakanaAI/AI-Scientist/tree/main/example_papers/dual_expert_denoiser>.

See pages - of [highlighted_papers/diffusion/dual_expert_denoiser/dual_expert_denoiser.pdf](https://highlighted_papers/diffusion/dual_expert_denoiser/dual_expert_denoiser.pdf)

Review

```
"Summary": "The paper ’DualDiff: Enhancing Mode Capture in Low-Dimensional
Diffusion Models via Dual-Expert Denoising’ introduces a dual-expert
denoising architecture aimed at enhancing diffusion models’ performance on
low-dimensional datasets. The method uses a gating mechanism to combine two
specialized expert networks dynamically, which helps in capturing multiple
modes in low-dimensional data distributions. The paper demonstrates
substantial improvements in terms of mode capture and sample diversity,
validated through various experiments on 2D datasets like ’circle’, ’dino’,
’line’, and ’moons’.",
"Strengths": [
    "The paper addresses a relevant and challenging problem in the field of
generative modeling.",
    "The dual-expert architecture and dynamic gating mechanism are novel
and well-formulated.",
    "Extensive experiments provide strong evidence of the approach’s
effectiveness.",
    "The introduction of a diversity loss term to encourage multiple mode
capture is a valuable contribution."
],
"Weaknesses": [
    "The novelty of combining two expert networks with a gating mechanism
is somewhat incremental.",
    "The choice of datasets is limited to simple 2D shapes, which might not
fully demonstrate the generalizability of the approach.",
    "The evaluation of gating mechanism behavior is not sufficiently
detailed.",
    "The increased training and inference times are a significant drawback
that may limit practical applicability.",
    "The diversity loss term is weighted arbitrarily without thorough
justification for the chosen value.",
    "The paper lacks detailed ablation studies to isolate the impact of
different components (e.g., gating mechanism, diversity loss).",
    "Potential limitations and negative societal impacts are not adequately
addressed."
],
"Originality": 3,
"Quality": 3,
"Clarity": 3,
"Significance": 3,
"Questions": [
    "Could you provide more detailed analysis on how the gating mechanism
adapts during training?",
    "How would the model perform on higher-dimensional datasets or more
complex low-dimensional datasets?",
    "Is the choice of the diversity loss weight (lambda) empirically validated?
Could different values lead to significantly different results?",
    "Can the authors provide more details on the gating mechanism and how
it determines the weight for each expert network?",
    "How does the performance vary with different configurations of the
gating network?",
    "Can the authors explain the choice of hyperparameters, particularly
the value of lambda in the diversity loss term?",
    "Can the authors provide more detailed ablation studies to quantify the
impact of each component (e.g., gating mechanism, diversity loss)?",
    "How does the model perform with different types of aggregators for the
expert networks?",
    "Can more qualitative examples and visualizations be provided to
substantiate the claims of improved mode capture?",
    "Can you provide more details on the architecture of the expert
networks and the gating mechanism?",
    "How does the diversity loss term impact the final performance, and
what are the trade-offs?",
    "Can you include more comprehensive ablation studies to evaluate the
impact of each component of the proposed method?",
    "What are the computational costs associated with the dual-expert
architecture, and how do they compare to the baseline?"
],
"Limitations": [
    "The increased computational cost and the focus on low-dimensional
datasets are the primary limitations of the proposed approach.",
    "The generalizability to higher-dimensional settings remains unclear.",
    "Potential negative societal impacts and limitations are not adequately
addressed."
],
"Ethical Concerns": false,
"Soundness": 3,
"Presentation": 3,
"Contribution": 3,
"Overall": 5,
"Confidence": 4,
"Decision": "Reject"
```

### D.5 StyleFusion: Adaptive Multi-style Generation in Character-Level Language Models

This idea was proposed in the 24th iteration of a Sonnet 3.5 run.

Idea

```
"Name": "multi_style_adapter",
"Title": "Multi-Style Adapter: Enhancing Style Awareness and Consistency in
Character-Level Language Models",
"Experiment": "1. Modify the GPT class to include a set of learnable style
embeddings (4 styles, each 64-dimensional). 2. Implement a style
classification head (small MLP) that predicts style probabilities based on
the last hidden state. 3. Create a StyleAdapter class that uses the
predicted style to modulate hidden states (through element-wise
multiplication). 4. Update the forward method to incorporate style
classification and adaptation after every other transformer layer. 5. Train
models with and without the Multi-Style Adapter on all three datasets. 6.
Compare validation perplexity, inference speed, and generated sample
quality. 7. Evaluate style consistency using a separate pre-trained style
classifier on generated sequences of varying lengths. 8. Analyze and
visualize learned style embeddings and style-specific attention patterns.
9. Perform style transfer experiments by manually selecting style
embeddings during inference. 10. Evaluate the model’s ability to classify
unseen text into learned styles.",
"Interestingness": 9,
"Feasibility": 9,
"Novelty": 9,
"novel": true
```

Link to code: <https://github.com/SakanaAI/AI-Scientist/tree/main/example_papers/multi_style_adapter>.

See pages - of [highlighted_papers/nanogpt/multi_style_adapter/multi_style_adapter.pdf](https://highlighted_papers/nanogpt/multi_style_adapter/multi_style_adapter.pdf)

Review

```
"Summary": "The paper introduces the Multi-Style Adapter, which enhances
style awareness and consistency in character-level language models by
integrating learnable style embeddings, a style classification head, and a
StyleAdapter module into the GPT architecture. The approach aims to balance
style adaptation and language modeling capabilities, and demonstrates
improved style consistency and competitive validation losses across
multiple datasets.",
"Strengths": [
    "The paper presents a novel approach to style-aware language modeling,
addressing a critical need for fine-grained stylistic control.",
    "The Multi-Style Adapter is well-motivated and integrates seamlessly
with the GPT architecture.",
    "Extensive experiments on diverse datasets demonstrate improved style
consistency and validation loss.",
    "The paper includes thorough analysis and visualization of learned
style embeddings and attention patterns."
],
"Weaknesses": [
    "The model achieves perfect style consistency scores on some datasets,
which may indicate overfitting to specific style patterns.",
    "The reduced inference speed (approximately 40% slower than the
baseline) may limit the practical applicability of the model.",
    "The paper could explore more sophisticated style representation
techniques and evaluate their impact.",
    "Lack of detailed ablation studies and additional baselines to
strengthen the claims.",
    "Clarity of the autoencoder aggregator mechanism could be enhanced."
],
"Originality": 3,
"Quality": 3,
"Clarity": 3,
"Significance": 3,
"Questions": [
    "How does the model handle unseen styles during inference?",
    "Can the authors provide more details on the training process and
hyperparameter tuning?",
    "What are the potential impacts of overfitting on the model’s ability
to generate diverse text within each style?",
    "Can the authors provide more detailed ablation studies, especially
focusing on the impact of different components in the Multi-Style
Adapter?",
    "How does the Multi-Style Adapter perform compared to other recent
style-transfer models?",
    "Can the computational efficiency trade-offs be quantified in a more
detailed manner?",
    "Can the authors clarify the autoencoder aggregator’s role and how it
integrates with the rest of the model?",
    "What measures have been taken to ensure the model does not overfit to
specific style patterns, especially given the perfect consistency scores on
some datasets?",
    "Are there any potential optimization techniques that could be explored
to improve the computational efficiency of the Multi-Style Adapter?",
    "How does the model handle cases where the input sequence contains
mixed styles?",
    "Could you provide more qualitative examples of generated text to
demonstrate the style consistency?",
    "What is the impact of reducing the number of gating parameters in the
modulation function?"
],
"Limitations": [
    "The reduced inference speed and potential overfitting to specific
style patterns are significant limitations. Future work should focus on
optimizing computational efficiency and improving the model’s ability to
generalize to diverse styles.",
    "The paper currently lacks sufficient ablation studies and additional
baselines.",
    "The model’s performance may be sensitive to hyperparameter settings,
such as the weight of the style loss and the frequency of StyleAdapter
application."
],
"Ethical Concerns": false,
"Soundness": 3,
"Presentation": 3,
"Contribution": 3,
"Overall": 5,
"Confidence": 4,
"Decision": "Reject"
```

### D.6 Adaptive Learning Rates for Transformers via Q-Learning

This idea was proposed in the 33rd iteration of a GPT-4o run.

Idea

```
"Name": "rl_lr_adaptation",
"Title": "Reinforcement Learning for Dynamic Learning Rate Adaptation in
Transformer Training",
"Experiment": "1. Implement a simpler RL method (e.g., Q-learning) that
takes the current state (e.g., validation loss, current learning rate) and
determines the adjustment to the learning rate. 2. Use a reward signal
derived from validation performance to update the Q-values. 3. Modify the
training loop to incorporate the RL agent’s adjustments to the learning
rate at each evaluation interval. 4. Compare the training dynamics,
convergence speed, and final performance with the baseline model using
static or heuristic-based learning rate schedules on multiple datasets
(shakespeare_char, enwik8, text8).",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 9,
"novel": true
```

Link to code: <https://github.com/SakanaAI/AI-Scientist/tree/main/example_papers/rl_lr_adaptation>.

See pages - of [highlighted_papers/nanogpt/rl_lr_adaptation/rl_lr_adaptation.pdf](https://highlighted_papers/nanogpt/rl_lr_adaptation/rl_lr_adaptation.pdf)

Review

```
"Summary": "The paper explores the application of Q-learning to dynamically
adjust the learning rate during transformer model training, aiming to
enhance training efficiency and model performance. The state is represented
by the validation loss and current learning rate, and the Q-learning agent
learns to adjust the learning rate to optimize the training process. The
approach is validated on three datasets: shakespeare_char, enwik8, and
text8.",
"Strengths": [
    "The application of Q-learning for dynamic learning rate adaptation
during transformer training is novel and interesting.",
    "The paper addresses an important problem in neural network training:
the selection of an appropriate learning rate schedule.",
    "Comprehensive experimental setup on multiple datasets."
],
"Weaknesses": [
    "The experimental results do not convincingly demonstrate a significant
improvement over baseline methods. The best validation loss achieved by the
Q-learning method on the shakespeare_char dataset is worse than the
baseline.",
    "The choice of state representation (validation loss and current
learning rate) is not well-justified.",
    "The paper lacks a detailed comparison with other sophisticated
adaptive learning rate methods like AdamW, LAMB, Lookahead, or Noisy
Adam.",
    "The clarity of the explanation on Q-learning and the reward signal
could be improved.",
    "The technical details of the Q-learning implementation and its
integration with transformer training are not thoroughly explained.",
    "The significance of the results is questionable given the additional
complexity introduced by the Q-learning agent.",
    "The figures and tables are not clear and do not provide sufficient
insight into the benefits of the proposed method.",
    "The paper does not sufficiently address the limitations of the
proposed method, such as sensitivity to hyperparameters and potential
overhead from the Q-learning agent.",
    "The discussion on the broader impacts and potential applications of
the approach is limited."
],
"Originality": 2,
"Quality": 2,
"Clarity": 2,
"Significance": 2,
"Questions": [
    "Can you provide a detailed justification for the choice of state
representation (validation loss and current learning rate)?",
    "How does your method compare with other adaptive learning rate methods
like AdamW, LAMB, Lookahead, or Noisy Adam in terms of both performance and
computational overhead?",
    "Can you clarify the reward signal used in your Q-learning approach?",
    "Why were other RL approaches not considered or compared with
Q-learning?",
    "Can the authors provide more details on the hyperparameter tuning
process?",
    "Can the authors provide more details on the state and action space
used in Q-learning?",
    "How sensitive is the approach to the choice of hyperparameters for
Q-learning?",
    "Can the authors provide a more in-depth analysis of why Q-learning
leads to better performance?",
    "Can you provide more details on the implementation of the Q-learning
agent and its interaction with the training process?",
    "What specific benefits does Q-learning offer over other RL-based
hyperparameter optimization methods?",
    "Can you elaborate on the marginal improvements in validation loss? Why
are the differences so small?",
    "How does the proposed method generalize to other types of neural
network architectures or other hyperparameters?",
    "Can the authors provide more insights into the robustness and
generality of the proposed Q-learning based approach?",
    "How does the method perform on other types of neural network
architectures apart from transformers?",
    "Can the authors discuss potential limitations and ethical concerns in
more detail?"
],
"Limitations": [
    "The method’s performance is sensitive to the choice of
hyperparameters, and there is additional overhead introduced by the
Q-learning agent.",
    "The experimental results do not convincingly demonstrate significant
improvements over baseline methods.",
    "The approach may not generalize well to other types of neural network
architectures without further tuning.",
    "The authors should discuss the potential drawbacks and challenges of
using Q-learning for learning rate adaptation in more detail.",
    "The paper does not adequately address the potential limitations and
ethical concerns of the proposed approach. It is important to discuss how
the method scales to other neural network architectures and the potential
risks associated with its use."
],
"Ethical Concerns": false,
"Soundness": 2,
"Presentation": 2,
"Contribution": 2,
"Overall": 3,
"Confidence": 4,
"Decision": "Reject"
```

### D.7 Unlocking Grokking: A Comparative Study of Weight Initialization Strategies in Transformer Models

This idea was proposed in the 2nd iteration of a Sonnet 3.5 run.

Idea

```
"Name": "weight_initialization_grokking",
"Title": "Weight Initialization Grokking: Assessing the impact of weight
initialization strategies on the grokking phenomenon",
"Experiment": "Modify the ‘run‘ function to include different weight
initialization strategies (Xavier, He, orthogonal) for the Transformer
model. Specifically, adjust the model initialization phase in the
‘Transformer‘ class to apply these strategies. Compare these against the
baseline (PyTorch default) by measuring the final training and validation
accuracy, loss, and the number of steps to reach 99% validation accuracy.
Evaluate the results for each dataset and seed combination.",
"Interestingness": 8,
"Feasibility": 7,
"Novelty": 7,
"novel": true
```

Link to code: <https://github.com/SakanaAI/AI-Scientist/tree/main/example_papers/weight_initialization_grokking>.

See pages - of [highlighted_papers/grokking/weight_initialization_grokking/weight_initialization_grokking.pdf](https://highlighted_papers/grokking/weight_initialization_grokking/weight_initialization_grokking.pdf)

Review

```
"Summary": "The paper investigates the impact of weight initialization
strategies on the grokking phenomenon in Transformer models, focusing on
arithmetic tasks in finite fields. It compares five initialization methods
(PyTorch default, Xavier, He, Orthogonal, and Kaiming Normal) using a small
Transformer architecture. The study reveals significant differences in
convergence speed and generalization capabilities across initialization
strategies, with Xavier and Orthogonal initializations showing superior
performance.",
"Strengths": [
    "Addresses an intriguing and underexplored phenomenon in deep
learning.",
    "Provides a systematic comparison of multiple weight initialization
strategies.",
    "Includes rigorous empirical analysis and statistical validation.",
    "Offers practical guidelines for initialization in similar learning
scenarios."
],
"Weaknesses": [
    "The scope is limited to small Transformer models and arithmetic tasks,
which may not generalize well to larger models or more complex tasks.",
    "The paper lacks deeper theoretical insights into why certain
initialization strategies perform better.",
    "The clarity of the experimental setup and the integration of figures
and tables could be improved.",
    "The implications for broader Transformer applications and potential
societal impacts are not sufficiently addressed."
],
"Originality": 3,
"Quality": 3,
"Clarity": 3,
"Significance": 3,
"Questions": [
    "Can the authors provide more theoretical explanations for why certain
initialization methods perform better?",
    "How do the findings translate to more complex, real-world tasks beyond
simple arithmetic operations?",
    "Can the clarity of the figures and tables be improved, and can key
graphs be better integrated into the text?",
    "What are the potential negative societal impacts of the findings?"
],
"Limitations": [
    "The study is limited to small Transformer models and arithmetic tasks,
which may not fully represent the complexity of real-world problems.",
    "The paper lacks a deeper theoretical understanding of the observed
phenomena.",
    "The potential negative societal impacts of the findings are not
addressed."
],
"Ethical Concerns": false,
"Soundness": 3,
"Presentation": 3,
"Contribution": 3,
"Overall": 5,
"Confidence": 4,
"Decision": "Reject"
```

### D.8 Grokking Accelerated: Layer-wise Learning Rates for Transformer Generalization

This idea was proposed in the 22nd iteration of a Sonnet 3.5 run.

Idea

```
"Name": "layerwise_lr_grokking",
"Title": "Layer-wise Learning Rate Grokking: Assessing the impact of layer-
wise learning rates on the grokking phenomenon",
"Experiment": "Modify the ‘run‘ function to implement layer-wise learning
rates. Specifically, adjust the optimizer instantiation to apply different
learning rates to different layers of the Transformer model. Define three
groups: 1) Embedding layers with a small learning rate (e.g., 1e-4), 2)
Lower Transformer layers with a moderate learning rate (e.g., 1e-3), 3)
Higher Transformer layers with a larger learning rate (e.g., 1e-2). Use
PyTorch’s parameter groups feature to assign these learning rates. Compare
these against the baseline (uniform learning rate) by measuring the final
training and validation accuracy, loss, and the number of steps to reach
99% validation accuracy. Evaluate the results for each dataset and seed
combination.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 9,
"novel": true
```

Link to code: <https://github.com/SakanaAI/AI-Scientist/tree/main/example_papers/layerwise_lr_grokking>.

See pages - of [highlighted_papers/grokking/layerwise_lr_grokking/layerwise_lr_grokking.pdf](https://highlighted_papers/grokking/layerwise_lr_grokking/layerwise_lr_grokking.pdf)

Review

```
"Summary": "The paper proposes a novel layer-wise learning rate strategy to
accelerate and enhance the grokking phenomenon in Transformer models. The
approach involves assigning different learning rates to the embedding
layers, lower Transformer layers, and higher Transformer layers. The method
is empirically validated on algorithmic tasks such as modular arithmetic
and permutations, showing significant improvements in convergence speed and
final performance.",
"Strengths": [
    "The paper addresses an important problem in deep learning: the
grokking phenomenon.",
    "The proposed layer-wise learning rate strategy is novel and shows
significant improvements in experimental results.",
    "Experiments demonstrate substantial improvements in both convergence
speed and final performance."
],
"Weaknesses": [
    "The paper lacks detailed methodological clarity, particularly
regarding the exact implementation of the layer-wise learning rates and
hyperparameter tuning.",
    "The theoretical explanation for why layer-wise learning rates work is
insufficient.",
    "The scope of tasks is limited to algorithmic ones, making it unclear
how well the findings generalize to other domains.",
    "The choice of learning rates seems arbitrary and lacks
justification.",
    "More comprehensive ablation studies and comparisons with other related
methods would strengthen the paper.",
    "Certain sections, such as the experimental setup and ablation studies,
could be more detailed and clearer."
],
"Originality": 3,
"Quality": 2,
"Clarity": 3,
"Significance": 3,
"Questions": [
    "Can the authors provide more detailed explanations of the
hyperparameter tuning process and the exact implementation of the layer-
wise learning rates?",
    "How do the authors ensure that the proposed method generalizes to
tasks beyond the algorithmic ones tested in the paper?",
    "Can the authors compare their approach with other related methods in
more detail?",
    "Can you provide more theoretical insights into why layer-wise learning
rates specifically facilitate grokking?",
    "How were the specific learning rates chosen for embedding, lower, and
higher layers?",
    "Can you discuss the potential for overfitting and how it was
mitigated?",
    "Have you tested the robustness of your method across different
datasets and larger model sizes?",
    "What is the impact of different learning rate configurations on the
results?",
    "Can the authors discuss potential strategies for mitigating the need
for careful tuning of learning rates to avoid instability?"
],
"Limitations": [
    "The methodology lacks detailed clarity, and the authors do not provide
sufficient information on the hyperparameter tuning process.",
    "The scope of tasks is limited to algorithmic ones, and the
generalizability of the findings is unclear.",
    "The paper requires more theoretical backing for the proposed method.",
    "The choice of specific learning rates and potential overfitting issues
need to be addressed in more detail.",
    "The scalability of the approach to larger models and more complex
tasks is not thoroughly addressed.",
    "Ethical concerns related to the potential misuse of accelerated
learning techniques are not addressed."
],
"Ethical Concerns": false,
"Soundness": 2,
"Presentation": 2,
"Contribution": 3,
"Overall": 4,
"Confidence": 4,
"Decision": "Reject"
```

### D.9 Grokking Through Compression: Unveiling Sudden Generalization via Minimal Description Length

This idea was proposed in the 22nd iteration of a Sonnet 3.5 run.

Idea

```
"Name": "mdl_grokking_correlation",
"Title": "Minimal Description Length and Grokking: An Information-Theoretic
Perspective on Sudden Generalization",
"Experiment": "Implement a function estimate_mdl(model) using weight
pruning to approximate the model’s description length. Prune weights below
a threshold and count remaining non-zero weights. Modify the training loop
to compute MDL every 500 steps. Run experiments on ModDivisionDataset and
PermutationGroup, including a baseline without MDL tracking. Plot MDL
estimates alongside validation accuracy. Define the ’MDL transition point’
as the step with the steepest decrease in MDL. Compare this point with the
grokking point (95% validation accuracy). Analyze the correlation between
MDL reduction and improvement in validation accuracy. Compare MDL evolution
between grokking and non-grokking (baseline) scenarios.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 9,
"novel": true
```

Link to code: <https://github.com/SakanaAI/AI-Scientist/tree/main/example_papers/mdl_grokking_correlation>.

See pages - of [highlighted_papers/grokking/mdl_grokking_correlation/mdl_grokking_correlation.pdf](https://highlighted_papers/grokking/mdl_grokking_correlation/mdl_grokking_correlation.pdf)

Review

```
"Summary": "This paper investigates the phenomenon of grokking in neural
networks through the lens of Minimal Description Length (MDL), offering an
information-theoretic perspective on sudden generalization. The authors
propose a method to estimate and track MDL during training using weight
pruning techniques. Experiments on modular arithmetic and permutation tasks
reveal a strong connection between MDL transitions and grokking points,
with varying dynamics across different tasks.",
"Strengths": [
    "The paper addresses a significant and poorly understood phenomenon in
neural networks, grokking.",
    "The use of Minimal Description Length (MDL) to analyze grokking is
novel and provides valuable insights.",
    "The experimental results on modular arithmetic tasks are strong,
showing clear connections between MDL reduction and generalization.",
    "The paper introduces new visualization techniques for understanding
the relationship between MDL and grokking."
],
"Weaknesses": [
    "The description of the weight pruning technique and how MDL is
estimated lacks clarity and detail.",
    "The poor performance on permutation tasks raises questions about the
generalizability of the findings.",
    "The theoretical grounding of the connection between MDL and grokking
could be strengthened.",
    "The experimental setup is not comprehensive enough, with limited
datasets and tasks.",
    "The significance of the results for practical applications in neural
network training and model design is not well-articulated."
],
"Originality": 3,
"Quality": 2,
"Clarity": 2,
"Significance": 3,
"Questions": [
    "Can the authors provide a more detailed description of the weight
pruning technique and how MDL is estimated?",
    "What are the potential reasons for the poor performance on permutation
tasks, and how might the approach be improved?",
    "Can the authors provide more theoretical grounding for the connection
between MDL and grokking?",
    "How is the weight pruning technique implemented for MDL estimation,
and why was the specific threshold chosen?",
    "Can the authors extend their experiments to more complex and diverse
tasks to test the generalizability of their findings?",
    "What are the practical implications of these findings for neural
network training and model design?"
],
"Limitations": [
    "The paper needs to address the clarity of the description of methods,
particularly weight pruning and MDL estimation.",
    "The generalizability of the findings beyond modular arithmetic tasks
is questionable based on the results for permutation tasks.",
    "The potential negative societal impacts of this work are not
discussed, although the focus on theoretical and empirical analysis may
have minimal direct societal consequences."
],
"Ethical Concerns": false,
"Soundness": 2,
"Presentation": 2,
"Contribution": 2,
"Overall": 3,
"Confidence": 4,
"Decision": "Reject"
```

### D.10 Accelerating Mathematical Insight: Boosting Grokking Through Strategic Data Augmentation

This idea was proposed in the 12th iteration of a Sonnet 3.5 run.

Idea

```
"Name": "data_augmentation_grokking",
"Title": "Impact of Data Augmentation on Grokking Dynamics in Mathematical
Operations",
"Experiment": "Modify AbstractDataset to include methods for operand
reversal (for addition and multiplication) and operand negation (for
addition, subtraction, and division) augmentations. Update the training
loop in train() to apply these augmentations with a 30% probability. Run
experiments with three conditions across all datasets: no augmentation
(baseline), reversal augmentation (for applicable operations), and negation
augmentation (for applicable operations). Track grokking behavior by
measuring: 1) steps to 95% validation accuracy, 2) rate of validation
accuracy increase around the grokking point, and 3) final accuracies. Plot
learning curves and gradient norm evolution for each condition. Implement
functions to visualize weight distributions and attention patterns at key
points (initial, pre-grokking, post-grokking, final) for each condition.
Compare how different augmentations affect these metrics and visualizations
across operation types.",
"Interestingness": 9,
"Feasibility": 9,
"Novelty": 8,
"novel": true
```

Link to code: <https://github.com/SakanaAI/AI-Scientist/tree/main/example_papers/data_augmentation_grokking>.

See pages - of [highlighted_papers/grokking/data_augmentation_grokking/data_augmentation_grokking.pdf](https://highlighted_papers/grokking/data_augmentation_grokking/data_augmentation_grokking.pdf)

Review

```
"Summary": "The paper investigates the impact of data augmentation on the
grokking phenomenon in neural networks learning modular arithmetic
operations. Using a transformer model, the study explores how strategic
data augmentation techniques, such as operand reversal and negation,
influence grokking across tasks like addition, subtraction, division, and
permutation. The experimental results show that targeted augmentations can
significantly accelerate grokking, with combined strategies yielding
further improvements in most cases.",
"Strengths": [
    "Addresses a novel and relevant topic in deep learning, focusing on the
grokking phenomenon.",
    "Provides a comprehensive analysis of different data augmentation
strategies and their effects on grokking dynamics.",
    "Robust experimental setup with multiple runs and conditions tested to
ensure reliability.",
    "Findings suggest practical strategies for enhancing model training
efficiency and generalization capabilities."
],
"Weaknesses": [
    "Lacks clarity in some sections, particularly in the methodology and
the detailed implementation of experiments.",
    "Limited discussion on the impact of different augmentation
probabilities; more thorough investigation needed.",
    "Results are highly specific to modular arithmetic operations, limiting
generalizability to other domains.",
    "Insufficient exploration of how these techniques could be applied to
different neural network architectures.",
    "Theoretical justifications for the observed effects are lacking.",
    "Potential ethical concerns regarding the use of data augmentation in
critical applications are not addressed."
],
"Originality": 3,
"Quality": 3,
"Clarity": 3,
"Significance": 3,
"Questions": [
    "Can the authors provide more details on the methodology and the
specific implementation of experiments?",
    "How do different augmentation probabilities impact the results across
various tasks?",
    "Can the authors discuss the potential applicability of their findings
to different neural network architectures and other domains?",
    "Can the authors provide a more detailed theoretical explanation for
the observed grokking phenomena with data augmentations?",
    "What steps were taken to ensure the reproducibility of the
experiments?",
    "Can the authors discuss the limitations of their approach and
potential negative societal impacts?",
    "Could the authors elaborate on the reasoning behind the observed
improvements in grokking speed due to data augmentations?",
    "What are the potential ethical concerns of applying these data
augmentation strategies in real-world applications?",
    "Can the authors include more ablation studies to dissect the
individual contributions of each augmentation technique in greater
detail?",
    "How do the results generalize to other neural network architectures or
more complex tasks beyond modular arithmetic?"
],
"Limitations": [
    "The paper’s clarity and thoroughness in discussing methodology and
results need improvement.",
    "The generalizability of the findings to other domains and
architectures requires further exploration.",
    "The study acknowledges the sensitivity of results to hyperparameters
and task specificity. However, it should also consider the broader
applicability and potential limitations in real-world scenarios.",
    "Potential negative societal impacts are not discussed, which is
important for a comprehensive evaluation of the work."
],
"Ethical Concerns": false,
"Soundness": 3,
"Presentation": 3,
"Contribution": 3,
"Overall": 5,
"Confidence": 4,
"Decision": "Reject"
```
