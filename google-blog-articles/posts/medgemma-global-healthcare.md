---
title: "MedGemma is helping global healthcare providers deliver better care"
source: https://blog.google/innovation-and-ai/technology/health/medgemma-global-healthcare/
site: google-blog
date: 2026-09-23
authors: Richa Tiwari
crawled: 2026-09-24
---

Getting access to quality healthcare often depends on where you live and whether a specialist is available nearby. In busy city hospitals and remote village clinics around the world, healthcare workers face challenges in treating a high volume of patients with limited specialized help.

To help address these challenges, we developed MedGemma, a collection of open-weight AI models optimized to understand medical text and images. Built on our Gemma models, MedGemma provides developers, researchers, and public health organizations with an adaptable foundation to build specialized tools to support triage, diagnostic screenings, and more. Since its release, MedGemma has been downloaded more than 10 million times for thousands of research adaptations worldwide. Since the models are open, they can be adapted to local languages and to address local health priorities while organizations maintain full ownership of their data and infrastructure.

Today, global health organizations are putting MedGemma to work in three key settings: frontline care, high-volume hospitals, and nationwide public health programs.

## Reaching patients in remote settings

Because MedGemma is a family of open-weight models, it allows developers to run mobile applications without an active internet connection.

In rural Uganda, Crane AI is using MedGemma to build EaseHealth, a clinical decision support app. An adapted MedGemma model handles clinical reasoning on-device, without an internet connection, helping community health workers evaluate symptoms, review guidance, and make informed triage decisions.

In other remote clinics, MedGemma is supporting early detection.

Zambia’s cervical cancer rate is among the highest in the world. To address it, Dawa Health created the offline-capable [DawaMom app](https://developers.devsite.corp.google.com/health-ai-developer-foundations/showcase/dawamom). Using MedGemma alongside [MedSigLIP](https://developers.google.com/health-ai-developer-foundations/medsiglip)
[1](#footnote-1)
, a lightweight encoder for medical text and images, DawaMom has been used to screen more than 3,500 women, with plans to scale across the country and neighboring regions.

In India, [Visilant](https://developers.google.com/health-ai-developer-foundations/showcase/visilant) uses a smartphone-based imaging system that has already screened more than 50,000 patients for cataracts and other eye conditions. By incorporating MedGemma into its screening workflows, Visilant hopes to improve the detection of treatable eye diseases before they cause permanent vision loss.

## Supporting faster triage in major hospital systems

MedGemma is also at work in high-volume medical centers. At [AIIMS Delhi](https://blog.google/intl/en-in/company-news/from-seed-to-scale-partnering-with-indias-startups-to-build-the-ai-future/), clinicians are piloting IndusDerma, an AI-assisted dermatology screening tool specifically designed to address the unique healthcare needs and skin tones of the Indian population. By supporting early triage, structured clinical summaries, and decision-making at the primary care level, IndusDerma empowers non-dermatologists and accelerates time-to-care across a high-volume public health system.

Another AIIMS-developed app, Aarogyam, focuses on outpatient triage. AIIMS clinicians hope to use Aarogyam to reduce the pre-specialist wait time by 40%, which will improve patient satisfaction and allow specialists to see more patients. Following successful completion of these pilots and clinical validation, AIIMS Delhi’s goal is to scale these applications across their network of hospitals which see up to 15,000 daily outpatient visits.

## Protecting patient data for national health programs

MedGemma can be deployed on-site or on any cloud server and allows organizations to keep patient data local and fully under their control, which is critical for public sector health initiatives. Several ministries of health around the world are using the models to address their country’s specific needs. For example, the Ministry of Health of Indonesia is developing a tuberculosis detection model that utilizes MedGemma and MedSigLIP and is trained on local chest X-ray data. The tool is intended to support the ministry's goal of screening 50 million citizens annually to eradicate the disease.

## Building open, responsible healthcare solutions

MedGemma is designed to support a wide spectrum of clinical tasks. It can understand medical documents, answer questions, and interpret complex medical imaging, including X-rays and CTs. By releasing the models, we hope to support global developers as they create safe, privacy preserving, locally adapted tools that address real-world health needs. MedGemma models, code repositories, and documentation are available to developers and researchers worldwide.

Visit [the Health AI Developer Foundations site](https://goo.gle/hai-def) for resources and to learn more about MedGemma and other models. Ask questions or share feedback in the [Health AI Developer Foundations forum](https://discuss.ai.google.dev/c/hai-def/62).
