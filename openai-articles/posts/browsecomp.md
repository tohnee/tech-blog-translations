---
title: "BrowseComp: a simple yet challenging benchmark for measuring the ability for agents to browse the web"
date: 2026-04-10
source: https://openai.com/index/browsecomp/
crawled: 2026-09-13
category: research
---

# BrowseComp: a simple yet challenging benchmark for measuring the ability for agents to browse the web

Deep research is a new capability of AI systems that involves searching the web, synthesizing information from many sources, and producing long, cited reports. To measure progress on this capability, we built BrowseComp (short for Browsing Competence): a benchmark that is simple to evaluate but very hard to solve, consisting of 1,266 questions whose answers require persistent, multi-step browsing.

## Why we built BrowseComp

Existing question-answering benchmarks are largely saturated: frontier models answer most of their questions correctly, often without needing to browse at all. There is a need for a benchmark where web browsing is actually necessary, and where questions remain difficult even for systems with access to search.

BrowseComp questions are designed so that:

Finding the answer requires locating and combining information scattered across multiple web pages.

The information is not typically indexed or linked directly from search results, requiring agents to dig through primary sources.

Verification is simple: every question has a short, unambiguous answer (a number, date, name, or phrase), making automatic evaluation easy.

Each question went through multiple rounds of human review to ensure that the answer was verifiable, that the question was well-posed, and that solving it genuinely required browsing persistence and creativity.

## What makes BrowseComp hard

A typical BrowseComp question looks simple on the surface—“Find the name of the X that did Y in year Z”—but the answer may be buried in an archived news article, a scanned PDF, a regional website, or a database that only surfaces under the right query. Solving these questions requires agents to:

Formulate many search queries, adapting strategy as they learn.

Read and synthesize information from primary sources, not just search snippets.

Persist through many dead ends: the average number of browse actions needed is high, and many questions were designed to be findable only through indirect paths.

Maintain and cross-check candidate answers against multiple sources.

Results

We evaluated a range of models and agentic browsing systems. Key findings:

GPT-4o with browsing solved fewer than 2% of the questions, despite strong performance on existing benchmarks.

o1 with browsing improved to roughly 9%.

Our deep research capability, which combines reasoning with agentic browsing over long horizons, solved approximately 51%—a dramatic improvement, though still far from complete.

Human experts with web access solve most questions, but often require hours per question; BrowseComp is intentionally beyond what casual browsing can achieve.

These results illustrate a broader pattern: benchmarks that are simple to construct can reveal large capability gaps between systems that superficially perform similarly.

## What we release

We are releasing the BrowseComp dataset, including:

The full set of 1,266 questions and their verified answers.

Reasoning traces and browse trajectories from our models on a sample of questions, to aid analysis of failure modes.

A grading harness for automatic evaluation.

We hope BrowseComp will be useful to researchers building agentic search systems, and that the gap it reveals—between what is possible today and what expert human browsing achieves—will close quickly.

Limitations

BrowseComp measures persistence and search skill, but not all aspects of deep research: it does not test writing quality, citation accuracy, or the synthesis of subjective judgments. Nor do we claim the questions are representative of what real users ask; they are deliberately adversarial. As models improve, we expect BrowseComp to saturate, and we are developing harder successors.

## Citation

For attribution in academic contexts or books, please cite this work as

OpenAI, "BrowseComp: a simple yet challenging benchmark for measuring the ability for agents to browse the web", OpenAI, 2026.

