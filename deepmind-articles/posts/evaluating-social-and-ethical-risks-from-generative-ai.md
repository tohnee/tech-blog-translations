---
title: "Evaluating social and ethical risks from generative AI"
source: https://deepmind.google/blog/evaluating-social-and-ethical-risks-from-generative-ai/
site: deepmind
date: 2023-10-19
authors: Laura Weidinger, William Isaac
crawled: 2026-09-13
---

Introducing a context-based framework for comprehensively evaluating the social and ethical risks of AI systems

Generative AI systems are already being used to write books, create graphic designs, [assist medical practitioners](https://www.deepmind.com/blog/codoc-developing-reliable-ai-tools-for-healthcare), and are becoming increasingly capable. Ensuring these systems are developed and deployed responsibly requires carefully evaluating the potential ethical and social risks they may pose.

In our [new paper](https://arxiv.org/abs/2310.11986), we propose a three-layered framework for evaluating the social and ethical risks of AI systems. This framework includes evaluations of AI system capability, human interaction, and systemic impacts.

We also map the current state of safety evaluations and find three main gaps: context, specific risks, and multimodality. To help close these gaps, we call for repurposing existing evaluation methods for generative AI and for implementing a comprehensive approach to evaluation, as in our case study on misinformation. This approach integrates findings like how likely the AI system is to provide factually incorrect information with insights on how people use that system, and in what context. Multi-layered evaluations can draw conclusions beyond model capability and indicate whether harm — in this case, misinformation — actually occurs and spreads.

To make any technology work as intended, both social and technical challenges must be solved. So to better assess AI system safety, these different layers of context must be taken into account. Here, we build upon earlier research identifying the [potential risks of large-scale language models](https://www.deepmind.com/publications/ethical-and-social-risks-of-harm-from-language-models), such as privacy leaks, job automation, misinformation, and more — and introduce a way of comprehensively evaluating these risks going forward.

## Context is critical for evaluating AI risks

Capabilities of AI systems are an important indicator of the types of wider risks that may arise. For example, AI systems that are more likely to produce factually inaccurate or misleading outputs may be more prone to creating risks of misinformation, causing issues like lack of public trust.

Measuring these capabilities is core to AI safety assessments, but these assessments alone cannot ensure that AI systems are safe. Whether downstream harm manifests — for example, whether people come to hold false beliefs based on inaccurate model output — depends on context. More specifically, who uses the AI system and with what goal? Does the AI system function as intended? Does it create unexpected externalities? All these questions inform an overall evaluation of the safety of an AI system.

Extending beyond **capability** evaluation, we propose evaluation that can assess two additional points where downstream risks manifest: human interaction at the point of use, and systemic impact as an AI system is embedded in broader systems and widely deployed. Integrating evaluations of a given risk of harm across these layers provides a comprehensive evaluation of the safety of an AI system.

‍**Human interaction** evaluation centres the experience of people using an AI system. How do people use the AI system? Does the system perform as intended at the point of use, and how do experiences differ between demographics and user groups? Can we observe unexpected side effects from using this technology or being exposed to its outputs?

‍**Systemic impact** evaluation focuses on the broader structures into which an AI system is embedded, such as social institutions, labour markets, and the natural environment. Evaluation at this layer can shed light on risks of harm that become visible only once an AI system is adopted at scale.

![A concentric circle diagram illustrating three layers of AI safety evaluation: a white inner circle labeled "Capability," a light blue middle ring labeled "Human interaction," and a dark blue outer ring labeled "Systemic impact," with a horizontal arrow pointing outwards from the center labeled "Context."](https://lh3.googleusercontent.com/gbzEwHOnaX3WEqcqWZu25GxovI7bsBY-7XrGmQP-np0P0hH-f2-QMBJLM-mpuCTtCHxXTDueQEBrq6gjUrSNfU1D2_DZET9Mukb5_FTx67S6_T7ITA=w1440)

Our three-layered evaluation framework, including capability, human interaction, and systemic impact. Context is essential for assessing the safety of AI systems.

## Safety evaluations are a shared responsibility

AI developers need to ensure that their technologies are developed and released responsibly. Public actors, such as governments, are tasked with upholding public safety. As generative AI systems are increasingly widely used and deployed, ensuring their safety is a shared responsibility between multiple actors:**‍**

- ‍**AI developers** are well-placed to interrogate the capabilities of the systems they produce.
- ‍**Application developers** and designated public authorities are positioned to assess the functionality of different features and applications, and possible externalities to different user groups.**‍**
- **Broader public stakeholders** are uniquely positioned to forecast and assess societal, economic, and environmental implications of novel technologies, such as generative AI.

The three layers of evaluation in our proposed framework are a matter of degree, rather than being neatly divided. While none of them is entirely the responsibility of a single actor, the primary responsibility depends on who’s best placed to perform evaluations at each layer.

![A grid visualization illustrating the shared responsibility of AI safety evaluation. The columns represent the evaluation layers: "Capability," "Human Interaction," and "Systemic Impact" (labeled "Context" along the bottom axis). The rows represent the actors: "AI model developers," "AI application developers," and "Third party stakeholders." Red-orange wave curves indicate the level of responsibility for each actor across the layers, showing that model developers have the highest responsibility for Capability, application developers for Human Interaction, and third-party stakeholders for Systemic Impact.](https://lh3.googleusercontent.com/4DdTuv2vKSR4eSSiJ81yrj35y04ompAgU_mEn4POrC_uMvpwPOSz1_Q1WY79l8wMcS8EbhIHa9sGcrWNN9iKp5TB2EDpyrZvXrjMWRR-VrYsyCn7xwY=w1440)

Relative distribution of responsibilities for AI developers and other organisations.

## Gaps in current safety evaluations of generative multimodal AI

Given the importance of this additional context for evaluating the safety of AI systems, understanding the availability of such tests is important. To better understand the broader landscape, we made a wide-ranging effort to collate evaluations that have been applied to generative AI systems, as comprehensively as possible.

![Three charts illustrating gaps in AI safety evaluations: Figure 2a shows most evaluations target text (and fewer address image, audio, or multimodal formats); Figure 2b shows 85.6% of evaluations focus on capability, with only 9.1% on human interaction and 5.3% on systemic impact; and Figure 2c visualizes the distribution of modalities across these three evaluation layers.](https://lh3.googleusercontent.com/bquHAzzwK5IWPzJxwbm14KlDaPvreqSQ9hlquASz_LhqMXr_9nFQnpsdzAwL9HLCl8up8Jheqp5tYWDIo6GbQ2Ra_vM2Kc5oc2R-QgDdmtZGwPQ0vw=w1440)

State of sociotechnical safety evaluation for generative AI systems by risk category, evaluation ‘layer’, and output modality, based on a wide-ranging review.

By mapping the current state of safety evaluations for generative AI, we found three main safety evaluation gaps:

1. ‍**Context:** Most safety assessments consider generative AI system capabilities in isolation. Comparatively little work has been done to assess potential risks at the point of human interaction or of systemic impact.**‍**
2. **Risk-specific evaluations:** Capability evaluations of generative AI systems are limited in the risk areas that they cover. For many risk areas, few evaluations exist. Where they do exist, evaluations often operationalise harm in narrow ways. For example, representation harms are typically defined as stereotypical associations of occupation to different genders, leaving other instances of harm and risk areas undetected.**‍**
3. **Multimodality:** The vast majority of existing safety evaluations of generative AI systems focus solely on text output — big gaps remain for evaluating risks of harm in image, audio, or video modalities. This gap is only widening with the introduction of multiple modalities in a single model, such as AI systems that can take images as inputs or produce outputs that interweave audio, text, and video. While some text-based evaluations can be applied to other modalities, new modalities introduce new ways in which risks can manifest. For example, a description of an animal is not harmful, but if the description is applied to an image of a person it is.

We’re making a list of links to publications that detail safety evaluations of generative AI systems openly accessible via [this repository](https://dpmd.ai/46CPd58). If you would like to contribute, please add evaluations by filling out [this form](https://docs.google.com/forms/d/e/1FAIpQLSddpgbOQusru0Kvhq7eAXR0yWnBVioE0SUPX-C_RMwclldOrw/viewform?resourcekey=0-aLrlwk9nVVurJPmtncsC2g).

## Putting more comprehensive evaluations into practice

Generative AI systems are powering a wave of new applications and innovations. To make sure that potential risks from these systems are understood and mitigated, we urgently need rigorous and comprehensive evaluations of AI system safety that take into account how these systems may be used and embedded in society.

A practical first step is repurposing existing evaluations and leveraging large models themselves for evaluation — though this has important limitations. For more comprehensive evaluation, we also need to develop approaches to evaluate AI systems at the point of human interaction and their systemic impacts. For example, while spreading misinformation through generative AI is a recent issue, we show there are many existing methods of evaluating public trust and credibility that could be repurposed.

Ensuring the safety of widely used generative AI systems is a shared responsibility and priority. AI developers, public actors, and other parties must collaborate and collectively build a thriving and robust evaluation ecosystem for safe AI systems.

[Read our paper on arXiv](https://arxiv.org/abs/2310.11986)[Access the Sociotechnical Evaluations Repository](https://docs.google.com/spreadsheets/u/1/d/e/2PACX-1vQObeTxvXtOs--zd98qG2xBHHuTTJOyNISBJPthZFr3at2LCrs3rcv73d4of1A78JV2eLuxECFXJY43/pubhtml)[Contribute to the Sociotechnical Evaluations Repository](https://docs.google.com/forms/d/e/1FAIpQLSddpgbOQusru0Kvhq7eAXR0yWnBVioE0SUPX-C_RMwclldOrw/viewform?resourcekey=0-aLrlwk9nVVurJPmtncsC2g)

**Paper authors:** Laura Weidinger, Maribeth Rauh, Nahema Marchal, Arianna Manzini, Lisa Anne Hendricks, Juan Mateos-Garcia, Stevie Bergman, Iason Gabriel, Conor Griffin, Jackie Kay, Ben Bariach, Verena Rieser, William Isaac.

Update on 1 November 2023: Bar chart colours in Figures 2a and 2b were adjusted to better represent the original data.
