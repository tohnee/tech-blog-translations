---
title: "Using AI to plan head and neck cancer treatments"
source: https://deepmind.google/blog/using-ai-to-plan-head-and-neck-cancer-treatments/
site: deepmind
date: 2018-09-13
authors: Mustafa Suleyman
crawled: 2026-09-13
---

[Early results](https://arxiv.org/abs/1809.04430) from our partnership with [the Radiotherapy Department at University College London Hospitals NHS Foundation Trust](https://deepmind.com/blog/applying-machine-learning-radiotherapy-planning-head-neck-cancer/) suggest that we are well on our way to developing an artificial intelligence (AI) system that can analyse and segment medical scans of head and neck cancer to a similar standard as expert clinicians. This segmentation process is an essential but time-consuming step when planning radiotherapy treatment. [The findings](https://arxiv.org/abs/1809.04430) also show that our system can complete this process in a fraction of the time.

## Speeding up the segmentation process

More than half a million people are diagnosed each year with cancers of the head and neck worldwide. Radiotherapy is a key part of treatment, but clinical staff have to plan meticulously so that healthy tissue doesn’t get damaged by radiation: a process which involves radiographers, oncologists and/or dosimetrists manually outlining the areas of anatomy that need radiotherapy, and those areas that should be avoided.

Although our work is still at an early stage, we hope it could one day reduce the waiting time between diagnosis and treatment, which could potentially improve outcomes for cancer patients. We also hope that accurate auto-segmentation could speed up the [adaptive radiotherapy process](http://www.christie.nhs.uk/patients-and-visitors/your-treatment-and-care/treatments/radiotherapy/what-we-do/adaptive-radiotherapy/), whereby radiotherapy treatments are adapted as the tumour shrinks - although more work is needed to investigate how this would work in practice.

As well as changing patients’ lives, this research could also free up time for the clinicians who treat them, meaning they get to spend more time on patient care, education and research.

## Applying our research to clinical settings

We’ve taken steps to ensure our work is clinically applicable. This includes the development of a [new performance metric](https://github.com/deepmind/surface-distance) used to assess model performance that we believe is more representative of clinical processes, and a test set with new [high-quality segmentations](https://github.com/deepmind/tcia-ct-scan-dataset) of scans selected from sites previously unseen to the model which demonstrates generalisability. Both of these have been open sourced to the research community. But for our system to have an impact on real people diagnosed with cancer, we need to expand it and demonstrate that it works in real clinical environments.

That’s why we’re looking forward to moving into the next phase of work with UCLH, where we will be exploring a human evaluation of these AI algorithms to test how they might perform in a clinical environment.

At DeepMind Health, we think it is important to share our work with others in the community. As such, Professor Olaf Ronneberger, Senior Research Scientist at DeepMind Health, will be presenting these initial findings at [MICCAI](https://www.miccai2018.org/en/), the world leading conference on medical imaging, this Sunday.

Ultimately, we believe that advanced technologies can and should help change lives, and we’re excited for the next steps of this project. We’ll continue to keep you updated as we make progress.
