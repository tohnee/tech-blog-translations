---
title: "Introducing new capabilities to GPT‑Rosalind"
date: 2026-06-03
source: https://openai.com/index/introducing-new-capabilities-to-gpt-rosalind/
crawled: 2026-09-13
category: research
---

We’re introducing a new model update to our [GPT‑Rosalind](https://openai.com/rosalind/) series purpose-built for life sciences research at enterprise scale. It combines GPT‑5.5’s agentic coding and tool-use capabilities with stronger model intelligence in core drug-discovery domains such as medicinal chemistry and genomics, while advancing performance across broader life sciences analysis, design, and experimental workflows.

Progress in life sciences depends on synthesizing data and evidence across scales and modalities: molecules, genes, pathways, and living systems. In our evaluations, the updated GPT‑Rosalind shows broad performance gains on research tasks from biology experts, complex medicinal chemistry queries, quantitative biology, and wet lab troubleshooting.

GPT‑Rosalind is now available in research preview to eligible organizations globally through our trusted-access deployment structure.

## Improving performance on scientifically-valuable tasks

In order to measure and continuously improve the real-world impact of GPT‑Rosalind, we designed LifeSciBench, an externally expert-judged benchmark focused on foundational aspects in life sciences research. Unlike existing benchmarks that evaluate a single component of model performance or biological domain in isolation, LifeSciBench takes an end-to-end view of scientifically valuable work by drawing tasks from six workflow areas central to life sciences research: evidence handling, analysis, design and optimization, scientific reasoning, validation and operations, and translation and communication. We use this benchmark to align progress with the needs and realities of life sciences research.

GPT‑Rosalind leads performance across scientifically-valuable tasks identified by industry and academic experts.

Extracting, reconciling, and auditing scientific evidence from papers, figures, tables, and experimental records.

## Eval Example

We’re preparing for a Type B FDA meeting on AAV9-microDys-X, an AAV9-based micro-dystrophin gene therapy for Duchenne muscular dystrophy that expresses a 138 kDa construct from an MCK promoter, and we want a hard-nosed critique of whether our current package really supports accelerated approval on micro-dystrophin expression as a surrogate endpoint reasonably likely to predict clinical benefit.

Study context: open-label Phase 1b/2 in 12 ambulatory boys age 4–7 with confirmed DMD and out-of-frame rod-domain deletions. The package is:

- Pre-treatment vastus lateralis biopsies: 0–3% of healthy-control dystrophin by quantitative Western blot using MANEX1A against the N-terminal actin-binding domain.
- 12-week post-treatment contralateral vastus lateralis biopsies: mean micro-dystrophin 38% of healthy control (range 18–61%) by the same Western blot, normalized to total protein by Coomassie staining.
- Post-treatment immunofluorescence: sarcolemmal signal in 75–95% of fibers using a polyclonal anti-dystrophin C-terminal antibody.
- 48-week function: mean NSAA change +1.4 points from baseline versus −0.6 in an external published natural-history registry cohort (p = 0.03 by unpaired t-test).
- Safety: transient transaminitis in 8/12 patients managed with steroid taper; one resolved myocarditis; no deaths.
- Biodistribution/persistence: AAV9 vector genomes detectable in muscle at 12 weeks at a mean of 2.3 vector genomes per nucleus.
- Eligibility: no baseline anti-AAV9 neutralizing antibodies (titer <1:400) and no exon-44 deletions.

Please pressure-test this package item by item: where would FDA or a skeptical reviewer say the evidence, as presented, fails to support our conclusion, and what additional data, analyses, or design changes would be needed to close those gaps if possible? For anything not specified, assume what is known from other clinical-grade 138 kDa micro-dystrophin programs and relevant clinical trials through December 31, 2025 also applies.

## Candidate Response

**Bottom line:** As presented, this package is not strong enough to support accelerated approval on micro-dystrophin expression as a surrogate endpoint reasonably likely to predict clinical benefit. A skeptical FDA reviewer would likely view the biomarker, functional, durability, safety, and generalizability evidence as materially under-supported.

| Package Item | Key Failure Mode | What Would Be Needed |
| Western blot quantification | MANEX1A binds an N-terminal epitope shared by endogenous full-length dystrophin and the micro-dystrophin transgene, so the assay does not cleanly distinguish transgene from residual/revertant dystrophin. Quantifying a 138 kDa micro-dystrophin against a healthy full-length dystrophin standard is also invalid. | Use a recombinant micro-dystrophin standard and an orthogonal method that distinguishes transgene from endogenous dystrophin, such as targeted mass spectrometry or a transgene-specific/epitope-specific assay. |
| Immunofluorescence | The C-terminal polyclonal antibody is poorly suited because the 138 kDa construct lacks the C-terminal domain. Many DMD patients have revertant fibers, and revertant dystrophin can retain C-terminal epitopes. Revertant fibers may expand clonally with age, biasing IF signal, especially in older boys. | Repeat IF with an antibody against an epitope present in the transgene but absent from revertant dystrophin. Quantify transgene-positive fibers separately from revertant fibers. |
| Surrogate endpoint validity | The package conflates protein amount with clinical function. “38% of healthy-control protein mass” does not mean 38% of normal dystrophin function because micro-dystrophin is structurally truncated. | Empirically validate the relationship between micro-dystrophin mass-percent, sarcolemmal localization, downstream functional restoration, and clinical benefit before treating expression as a surrogate endpoint. |
| Biopsy design | Pre- and post-treatment contralateral vastus lateralis biopsies introduce left-right and intramuscular spatial variability. Disease progression and fibro-fatty replacement can also change total-protein-normalized signal. | Standardize biopsy site using consistent anatomical landmarks, normalize to muscle-specific proteins, and measure fibro-fatty composition in parallel. |
| NSAA comparator/statistics | An external natural-history cohort is not a randomized concurrent control. Trial eligibility, supportive care, participation effects, baseline NSAA, steroid regimen, age, and exon class can all bias the comparison. An unpaired t-test is not sufficient. Also, a +1.4 NSAA change is within test-retest variability for this age group. | Run a randomized concurrent placebo-controlled study, or at minimum use adjusted analyses accounting for baseline NSAA, age, steroid regimen, exon class, and other confounders. |
| Age-window confounding | Boys age 4–7 are in a developmental window where untreated ambulatory DMD patients may gain motor function before decline dominates. A 48-week NSAA change mixes developmental gain, disease progression, and possible treatment effect. | Use a concurrent randomized control with age stratification to separate developmental trajectory from treatment effect. |
| Prior clinical precedent | Open-label micro-dystrophin functional signals have not reliably predicted confirmatory benefit; published precedent includes micro-dystrophin gene therapy confirmatory trials failing to reproduce open-label NSAA improvements. | Do not rely on open-label NSAA change as decisive support. Require controlled functional evidence. |
| Structural limits of the construct | The 138 kDa construct deletes spectrin repeats R16/17, which contain nNOS-binding sites. Loss of nNOS recruitment can impair functional sympatholysis and ischemia protection during exercise, creating a mechanistic ceiling on rescue independent of expression level. | Add mechanistic studies showing whether this specific construct restores relevant dystrophin-associated complex function, nNOS localization, exercise physiology, and muscle protection. |
| AAV durability | Vector genomes at 12 weeks do not establish durable expression. AAV9 genomes are largely non-integrating episomes and may decline over time. Vector-genome persistence is not the same as persistent protein expression. | Measure longitudinal transgene protein expression and functional biomarker durability beyond 12 weeks. |
| Immune/safety profile | Transaminitis in 8/12 patients is consistent with immune response to AAV-transduced cells, but the mechanism is not established. One myocarditis case is concerning given AAV9 cardiac tropism. | Provide deeper immune monitoring, liver/cardiac safety characterization, and intensified cardiac follow-up. |
| Patient selection/generalizability | Excluding anti-AAV9 neutralizing-antibody-positive patients limits generalizability. Excluding exon-44 deletions limits applicability to that DMD subgroup. n=12 is too small to characterize safety and efficacy across the broader DMD population. | Broaden eligibility where possible or pre-specify stratified analyses by antibody status, genotype/exon class, age, and baseline function before using the result to support broad approval. |

**Regulatory conclusion:** The package may show biological activity, but it does not yet establish that the measured micro-dystrophin expression is a reliable surrogate reasonably likely to predict clinical benefit. The main gaps are assay specificity, invalid quantification standards, possible revertant-fiber confounding, lack of a randomized control, age-related NSAA confounding, uncertain durability, and unresolved safety/generalizability issues.

To close the gap, the program would need a controlled, age-stratified clinical design with transgene-specific expression assays, orthogonal protein quantification, tissue-composition controls, longitudinal durability data, mechanistic functional assays for the truncated construct, and stronger safety monitoring, especially hepatic and cardiac.

## Rubric Criteria & Grades

## Stronger scientific reasoning

### Medicinal chemistry

GPT‑Rosalind achieves industry-leading performance in medicinal chemistry, a field focused on turning molecules into useful drugs. We designed MedChemBench to reflect realistic medicinal chemistry workflows, evaluating multimodal chemical structure understanding; structure-activity relationship (SAR); prediction of drug potency, toxicity, and absorption, distribution, metabolism, excretion (ADME); multiparameter lead-optimization decision-making; and retrosynthesis. GPT‑Rosalind out-performs GPT‑5.5 at 27.5% vs. 25.1% on MedChemBench, while using 7.2% fewer tokens.

GPT‑Rosalind shows better multimodal synthesis and mechanistic reasoning in medicinal chemistry.

### Genomics and quantitative biology

On GeneBench, our agentic evaluation on long horizon, end-to-end analysis in genomics and quantitative biology, GPT‑Rosalind uses 31% fewer tokens than GPT‑5.5 while achieving a higher accuracy of 21.6% vs. 20.4%. GeneBench assesses agentic performance on long-horizon quantitative tasks: based on realistic scientific data, can an agent plan valid analysis, QC, modeling, and corrections to arrive at decision-relative answers? Included problems span a variety of domains, including functional genomics, spatial transcriptomics, proteomics, epigenomics, and applied genetics.

GPT‑Rosalind uses 31% fewer tokens than GPT‑5.5 while improving accuracy.

### Assisting real-world lab work

We introduce a new evaluation to test GPT‑Rosalind’s ability to help scientists conducting lab work in the real world. LabWorkBench tests the model's ability to link perturbations to experimental outcomes in real wet lab protocols used by scientists, for the purposes ranging from troubleshooting to optimization. The data used by LabWorkBench are proprietary and thus uncontaminated. GPT‑Rosalind scores 63.2% vs. GPT‑5.5 at 55.8%, while using 5.3% fewer tokens.

On real wet lab protocol assistance, GPT‑Rosalind shows significant gains over GPT‑5.5 while improving token efficiency.

## From reasoning to executed workflows

We built the [Life Sciences Research](https://github.com/openai/plugins/tree/main/plugins/life-science-research) and [Life Sciences NGS Analysis](https://github.com/openai/plugins/tree/main/plugins/ngs-analysis) plugins to extend the increased intelligence of [GPT‑Rosalind](https://openai.com/rosalind/) with a practical execution layer for repeatable scientific workflows. Together, these plugins bring sourced evidence retrieval, biological interpretation, and bioinformatics execution into the same workspace, helping researchers connect external evidence with internal omics analyses while preserving artifacts and provenance. All users can now access both plugins through Codex. Qualified GPT‑Rosalind enterprise users can additionally use GPT‑Rosalind to power these plugins.

To better leverage Codex as a dynamic workbench for scientists, we added interactive viewers for biologically native file types. The initial set of sequence, alignment, and structure viewers are designed to keep scientists close to the evidence as GPT‑Rosalind reasons across a workflow and directly answer follow-up questions using the active viewer in-context.

The demo above shows these capabilities in action, orchestrated by GPT‑Rosalind. We follow a scientist investigating a liquid tumor biopsy to identify mutations and other molecular changes that could inform treatment. The Life Sciences NGS Analysis plugin turns a review of processed ctDNA records into an interactive notebook, surfacing recurring alterations, low-frequency calls, and sample trajectories that focus the investigation on KRAS G12C. From there, the Life Sciences Research plugin adds sourced target, inhibitor, and resistance context, while the native sequence, alignment, and structure viewers allow the scientist to inspect mutant residue 12, its conservation across the RAS family, and the inhibitor-bound pocket directly. The workflow concludes by translating that evidence into concrete follow-up options, with each step and artifact available for expert review.

Life Sciences NGS Analysis plugin

scRNA-seq QC & Annotation

Turn a 10x-style matrix bundle into QC-filtered single-cell artifacts, annotations, and UMAPs you can inspect and revise in Codex. The Life Sciences NGS Analysis plugin routes the request to scrna-seq-qc, chooses QC thresholds from the data, preserves provenance around filtering and annotation, and surfaces blockers such as missing doublet-detection dependencies.

Bulk RNA-seq FASTQ QC

Turn a bulk RNA-seq sample sheet, FASTQ bundle, and reference files into a QC-reviewed counts bundle you can inspect and reuse in Codex. The Life Sciences NGS Analysis plugin routes the request, validates the inputs, and returns an auditable run envelope with MultiQC, Salmon matrices, provenance, and explicit caveats.

## Expanded access for trusted organizations

We are expanding access to the [GPT‑Rosalind](https://openai.com/rosalind/) series to eligible organizations globally. GPT‑Rosalind will be available in research preview through our trusted-access deployment structure for organizations that are conducting legitimate scientific research with clear public benefit, have strong governance and safety oversight, and controlled access with enterprise-grade security.

As part of this global expansion, we’re excited to help support Novo Nordisk’s mission of bringing innovative treatment options to patients faster by helping scale their medical research with GPT‑Rosalind. Novo Nordisk is leveraging frontier AI capabilities to help researchers analyze complex datasets, uncover useful patterns, and test hypotheses more quickly. GPT‑Rosalind’s stronger biological understanding will help teams connect evidence across literature, genomics, transcriptomics, sequence, structure, and experimental results, making it easier to move from data to clearer research decisions.

“Life sciences research is complex, data-rich, and interdisciplinary. To deliver meaningful value for researchers, advanced AI models must be grounded in trusted scientific data, connected to validated tools, and integrated into the real-world workflows researchers use every day. We’re pleased with our partnership with OpenAI and the opportunity to explore how GPT‑Rosalind can support more rigorous, practical approaches to drug discovery.”

Mishal Patel, Group Vice President, AI & Digital Innovation, R&D - Novo Nordisk

We are also now offering an OpenAI managed workspace for qualified organizations without an Enterprise account.

- [Request access](https://openai.com/form/life-sciences-access/)

## What’s next

The updated GPT‑Rosalind is the next step in our broader commitment to building AI systems that can help accelerate scientific discovery while ensuring that advanced biological capabilities are deployed with appropriate safeguards. We will continue improving the model’s biological reasoning, expanding support for tool-heavy and long-horizon research workflows, and working with qualified organizations across regions to evaluate real-world impact.

This also means applying life sciences AI to high-impact public-benefit work, from drug discovery and translational medicine to public health, preparedness, and biodefense. Through [Rosalind Biodefense](https://openai.com/index/strengthening-societal-resilience-with-rosalind-biodefense/) and our trusted-access deployment model, we aim to put frontier biological capabilities in the hands of the researchers, institutions, and defenders working to improve human health and strengthen societal resilience.

We will continue building [GPT‑Rosalind](https://openai.com/rosalind/) to become a more capable partner across the full life cycle of scientific research, helping scientists move more quickly from the right questions to clearer evidence, better experiments, and ultimately new treatments for patients.
