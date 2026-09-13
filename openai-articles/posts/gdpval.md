---
title: "Measuring the performance of our models on real-world tasks"
date: 2025-09-25
source: https://openai.com/index/gdpval/
crawled: 2026-09-13
category: research
---

Our mission is to ensure that artificial general intelligence benefits all of humanity. As part of our mission, we want to transparently communicate progress on how AI models can help people in the real world. That’s why we’re introducing GDPval: a new evaluation designed to help us track how well our models and others perform on economically valuable, real-world tasks. We call this evaluation GDPval because we started with the concept of Gross Domestic Product (GDP) as a key economic indicator and drew tasks from the key occupations in the industries that contribute most to GDP.

People often speculate about AI’s broader impact on society, but the clearest way to understand its potential is by looking at what models are already capable of doing. History shows that major technologies—from the internet to smartphones—took more than a decade to go from invention to widespread adoption. Evaluations like GDPval help ground conversations about future AI improvements in evidence rather than guesswork, and can help us track model improvement over time.

Previous AI evaluations like challenging academic tests and competitive coding challenges have been essential in pushing the boundaries of model reasoning capabilities, but they often fall short of the kind of tasks that many people handle in their everyday work.

To bridge this gap, we’ve been developing evaluations that measure increasingly realistic and economically relevant capabilities. This progression has moved from classic academic benchmarks like MMLU (exam-style questions across dozens of subjects), to more applied evaluations like [SWE-Bench](https://openai.com/index/introducing-swe-bench-verified/) (software engineering bug-fixing tasks), [MLE-Bench](https://openai.com/index/mle-bench/) (machine learning engineering tasks such as model training and analysis), and [Paper-Bench](https://openai.com/index/paperbench/) (scientific reasoning and critique on research papers), and more recently to market-based evaluations like [SWE-Lancer](https://openai.com/index/swe-lancer/) (freelance software engineering projects based on real payouts).

GDPval is the next step in that progression. It measures model performance on tasks drawn directly from the real-world knowledge work of experienced professionals across a wide range of occupations and sectors, providing a clearer picture on how models perform on economically valuable tasks. Evaluating models on realistic occupational tasks helps us understand not just how well they perform in the lab, but how they might support people in the work they do every day.

## What GDPval measures

GDPval, the first version of this evaluation, spans 44 occupations selected from the top 9 industries contributing to U.S. GDP. The GDPval full set includes 1,320 specialized tasks (220 in the gold open-sourced set), each meticulously crafted and vetted by experienced professionals with over 14 years of experience on average from these fields. Every task is based on real work products, such as a legal brief, an engineering blueprint, a customer support conversation, or a nursing care plan.

GDPval is distinctive both in its realism and diversity of tasks being evaluated. Unlike other evaluations tied to economic value which concentrate on specific domains (e.g., SWE-Lancer), GDPval covers many tasks and occupations. And unlike benchmarks which involve synthetically creating tasks in the style of an academic exam or test (e.g., Humanity’s Last Exam or MMLU), GDPval focuses on tasks based on deliverables that are either an actual piece of work or product that exists today or are a similarly constructed piece of work product.

Unlike traditional benchmarks, GDPval tasks are not simple text prompts. They come with reference files and context, and the expected deliverables span documents, slides, diagrams, spreadsheets, and multimedia. This realism makes GDPval a more realistic test of how models might support professionals.

GDPval is an early step that doesn’t reflect the full nuance of many economic tasks. While it spans 44 occupations and hundreds of knowledge work tasks, it is limited to one-shot evaluations, so it doesn’t capture cases where a model would need to build context or improve through multiple drafts. Future versions will extend to more interactive workflows and context-rich tasks to better reflect the complexity of real-world knowledge work (see more in our Limitations section below).

## How we chose occupations

GDPval covers tasks across 9 industries and 44 occupations, and future versions will continue to expand coverage. The initial 9 industries were chosen based on those contributing over 5% to U.S. GDP, as determined by data from the Federal Reserve Bank of St. Louis. Then, we selected the 5 occupations within each industry that contribute most to total wages and compensation and are predominantly knowledge work occupations, using wage and employment data from the [May 2024 US Bureau of Labor Statistics (BLS) occupational employment report](https://www.bls.gov/oes/tables.htm). To determine if the occupations were predominantly knowledge work, we used task data from [O *NET](https://www.onetonline.org/), a database of U.S. occupational information sponsored by the U.S. Department of Labor. We classified whether each task for each occupation in O *NET was knowledge work or physical work/manual labor (requiring actions to be taken in the physical world). An occupation qualified overall as “predominantly knowledge work” if at least 60% of its component tasks were classified as not involving physical work or manual labor. We chose this 60% threshold as a starting point for the first version of GDPval, focusing on occupations where AI could have the highest impact on real-world productivity.

This process yielded 44 occupations for inclusion.

**Real estate and rental and leasing**

- Concierges
- Property, real estate, and community association managers
- Real estate sales agents
- Real estate brokers
- Counter and rental clerks

**Government**

- Recreation workers
- Compliance officers
- First-line supervisors of police and detectives
- Administrative services managers
- Child, family, and school social workers

**Manufacturing**

- Mechanical engineers
- Industrial engineers
- Buyers and purchasing agents
- Shipping, receiving, and inventory clerks
- First-line supervisors of production and operating workers

**Professional, scientific, and technical services**

- Software developers
- Lawyers
- Accountants and auditors
- Computer and information systems managers
- Project management specialists

**Health care and social assistance**

- Registered nurses
- Nurse practitioners
- Medical and health services managers
- First-line supervisors of office and administrative support workers
- Medical secretaries and administrative assistants

**Finance and insurance**

- Customer service representatives
- Financial and investment analysts
- Financial managers
- Personal financial advisors
- Securities, commodities and financial services sales agents

**Retail trade**

- Pharmacists
- First-line supervisors of retail sales workers
- General and operations managers
- Private detectives and investigators

**Wholesale trade**

- Sales managers
- Order clerks
- First-line supervisors of non-retail sales workers
- Sales representatives, wholesale and manufacturing, except technical and scientific products
- Sales representatives, wholesale and manufacturing, technical and scientific products

**Information**

- Audio and video technicians
- Producers and directors
- News analysts, reporters, and journalists
- Film and video editors
- Editors

## How we built the dataset

For each occupation, we worked with experienced professionals to create representative tasks that reflect their day-to-day work. These professionals averaged 14 years of experience, with strong records of advancement. We deliberately recruited a breadth of experts—such as lawyers from different practice areas and firms of different sizes—to maximize representativeness.

Each task went through a multi-step review process to ensure it was representative of real work, feasible for another professional to complete, and clear for evaluation. On average, each task received 5 rounds of expert review, including checks from other task writers, additional occupational reviewers, and model-based validation.

The resulting dataset includes 30 fully reviewed tasks per occupation (full-set) with 5 tasks per occupation in our open-sourced gold set, providing a robust foundation for evaluating model performance on real-world knowledge work.

### Examples of GDPval tasks

### Prompt + task context

### Experienced human deliverable

## How we grade model performance

To evaluate model performance on GDPval tasks, we rely on expert “graders”—a group of experienced professionals from the same occupations represented in the dataset. These graders blindly compare model-generated deliverables with those produced by task writers (not knowing which is AI versus human generated), and offer critiques and rankings. Graders then rank the human and AI deliverables and classify each AI deliverable as “better”, “as good as”, or “worse than” one another.

Task writers also created detailed scoring rubrics for their occupations, which add consistency and transparency to the grading process. We also built an “automated grader”, an AI system trained to estimate how human experts would judge a given deliverable. In other words, instead of running a full expert review every time, the automated grader can quickly predict which output people would likely prefer. We’re releasing this tool through at evals.openai.com as an experimental research service, but it’s not yet as reliable as expert graders, so we don’t use it to replace them.

## Early results

We found that today’s best frontier models are already approaching the quality of work produced by industry experts. To test this, we ran blind evaluations where industry experts compared deliverables from several leading models—GPT‑4o, o4-mini, OpenAI o3, GPT‑5, Claude Opus 4.1, Gemini 2.5 Pro, and Grok 4—against human-produced work. Across 220 tasks in the GDPval gold set, we recorded when model outputs were rated as better than (“wins”) or on par with (“ties”) the deliverables from industry experts, as shown in the bar chart below. Claude Opus 4.1 was the best performing model in the set, excelling in particular on aesthetics (e.g., document formatting, slide layout), and GPT‑5 excelled in particular on accuracy (e.g., finding domain-specific knowledge). We also see clear progress over time on these tasks. Performance has more than doubled from GPT‑4o (released spring 2024) to GPT‑5 (released summer 2025), following a clear linear trend.

In addition, we found that frontier models can complete GDPval tasks roughly 100x faster and 100x cheaper than industry experts. However, these figures reflect pure model inference time and API billing rates, and therefore do not capture the human oversight, iteration, and integration steps required in real workplace settings to use our models. Still, especially on the subset of tasks where models are particularly strong, we expect that giving a task to a model before trying it with a human would save time and money.

Expert graders compared deliverables from leading models to human experts. Today’s frontier models are already approaching the quality of work produced by industry experts. Claude Opus 4.1 produced outputs rated as good as or better than humans in just under half the tasks.

From GPT‑4o to GPT‑5, performance on GDPval tasks more than tripled in a year.

Finally, we incrementally trained an internal, experimental version of GPT‑5 to assess if we could improve performance on GDPval. We found this process improved performance, creating a pathway for further potential improvement. Other controlled experiments back this up: increasing model size, encouraging more reasoning steps, and giving richer task context each led to measurable gains.

You can read the full results in our paper. We’re also releasing a gold subset of GDPval tasks and a public grading service so other researchers can build on this work.

## The future of work and AI

As AI becomes more capable, it will likely cause changes in the job market. Early GDPval results show that models can already take on some repetitive, well-specified tasks faster and at lower cost than experts. However, most jobs are more than just a collection of tasks that can be written down. GDPval highlights where AI can handle routine tasks so people can spend more time on the creative, judgment-heavy parts of work. When AI complements workers in this way it can translate into significant economic growth. Our goal is to keep everyone on the “up elevator” of AI by democratizing access to these tools, supporting workers through change, and building systems that reward broad contribution.

## Limitations and what’s next

GDPval is an early step. While it covers 44 occupations and hundreds of tasks, we are continuing to refine our approach to expand the scope of our testing and make the results more meaningful. The current version of the evaluation is also one-shot, so it doesn’t capture cases where a model would need to build context or improve through multiple drafts—for example, revising a legal brief after client feedback or iterating on a data analysis after spotting an anomaly. Additionally, in the real world, tasks aren’t always clearly defined with a prompt and reference files; for example, a lawyer might have to navigate ambiguity and talk to their client before deciding that creating a legal brief is the right approach to help them. We plan to expand GDPval to include more occupations, industries, and task types, with increased interactivity, and more tasks involving navigating ambiguity, with the long-term goal of better measuring progress on diverse knowledge work.

## Get involved

- **If you’re an industry expert** interested in contributing to GDPval, please [show your interest here](https://openai.com/form/real-world-knowledge-work/).
- **If you’re a customer working with OpenAI** and you’d like to contribute to a future round of GDPval, please [express interest here](https://openai.com/form/gdpval-customer-contribution/).

Community participation is essential—we’re excited to build GDPval together with researchers, practitioners, and organizations who share our goal of making AGI more useful for people at work.
