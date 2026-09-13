---
title: "A major milestone for the treatment of eye disease"
source: https://deepmind.google/blog/a-major-milestone-for-the-treatment-of-eye-disease/
site: deepmind
date: 2018-08-13
authors: 
crawled: 2026-09-13
---

We are delighted to announce the results of the first phase of our joint research partnership with [Moorfields Eye Hospital](https://deepmind.com/blog/announcements/announcing-deepmind-health-research-partnership-moorfields-eye-hospital), which could potentially transform the management of sight-threatening eye disease.

The results, published online in [Nature Medicine](https://www.nature.com/articles/s41591-018-0107-6) (open access full text, see end of blog), show that our AI system can quickly interpret eye scans from routine clinical practice with unprecedented accuracy. It can correctly recommend how patients should be referred for treatment for over 50 sight-threatening eye diseases as accurately as world-leading expert doctors.

These are early results, but they show that our system could handle the wide variety of patients found in routine clinical practice. In the long term, we hope this will help doctors quickly prioritise patients who need urgent treatment – which could ultimately save sight.

## A more streamlined process

Currently, eyecare professionals use optical coherence tomography (OCT) scans to help diagnose eye conditions. These 3D images provide a detailed map of the back of the eye, but they are hard to read and need expert analysis to interpret.

The time it takes to analyse these scans, combined with the sheer number of scans that healthcare professionals have to go through (over 1,000 a day at Moorfields alone), can lead to lengthy delays between scan and treatment – even when someone needs urgent care. If they develop a sudden problem, such as a bleed at the back of the eye, these delays could even cost patients their sight.

The system we have developed seeks to address this challenge. Not only can it automatically detect the features of eye diseases in seconds, but it can also prioritise patients most in need of urgent care by recommending whether they should be referred for treatment. This instant triaging process should drastically cut down the time elapsed between the scan and treatment, helping sufferers of diabetic eye disease and age-related macular degeneration avoid sight loss.

## Adaptable technology

We don’t just want this to be an academically interesting result – we want it to be used in real treatment. So our paper also takes on one of the key barriers for AI in clinical practice: the “black box” problem. For most AI systems, it’s very hard to understand exactly why they make a recommendation. That’s a huge issue for clinicians and patients who need to understand the system’s reasoning, not just its output – the why as well as the what.

Our system takes a novel approach to this problem, combining two different neural networks with an easily interpretable representation between them. The first neural network, known as the segmentation network, analyses the OCT scan to provide a map of the different types of eye tissue and the features of disease it sees, such as haemorrhages, lesions, irregular fluid or other symptoms of eye disease. This map allows eyecare professionals to gain insight into the system’s “thinking.” The second network, known as the classification network, analyses this map to present clinicians with diagnoses and a referral recommendation. Crucially, the network expresses this recommendation as a percentage, allowing clinicians to assess the system’s confidence in its analysis.

![An infographic of the current process used to detect eye disease. It starts with an OCT scan which is analysed by a trained technician, this takes time so can cause delays in treating patients in need of urgent care. Instead, AI can analyse the OCT image and identify features of eye disease in seconds, passing that recommendation on to the clinician.](https://lh3.googleusercontent.com/t78mlRIzLYO2Gqv6Wvn0g1Q6loXy9-cOpcsuWGb7p1S9B8z-C8VpxfRds-NM6QjUjjCboyUfPBv5BHTnEjU9VKAKUJyL5pzzxmFJAlzBb5ZetieT5eo=w1440)

How AI could help clinicians detect eye disease

This functionality is critically important, since eyecare professionals are always going to play a key role in deciding the type of care and treatment a patient receives. Enabling them to scrutinise the technology’s recommendations is key to making the system usable in practice.

On top of this, our technology can be easily applied to different types of eye scanners, and not just the specific type of device it was trained on at Moorfields. This might seem inconsequential, but it means that the technology could be applied across the world with relative ease, massively increasing the number of patients who could potentially benefit. This also ensures the system can still be used in hospitals and other clinical settings even as OCT scanners are upgraded or replaced over time.

## The next phase

While we’re incredibly proud of this progress, this [initial research](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/a-major-milestone-for-the-treatment-of-eye-disease/De%20Fauw%20et.%20al%20Nature%20Medicine%202018.pdf) [PDF] would need to be turned into a product and then undergo rigorous clinical trials and regulatory approval before being used in practice. But we’re confident that, in time, this system could transform the diagnosis, treatment and management of eye disease.

Our partners at Moorfields want our research to help them improve care, reduce some of the strain on clinicians, and lower costs - all at the same time. So we’ve also worked hard on what comes next.

If this technology is validated for general use by clinical trials, Moorfields’ clinicians will be able to use it for free across all 30 of their UK hospitals and community clinics, for an initial period of five years. These clinics serve 300,000 patients a year and receive over 1,000 OCT scan referrals every day – each of which could benefit from improved accuracy and speed of diagnosis.

We’re also proud that the work we’ve put into this project will help accelerate many other NHS research efforts. The original dataset held by Moorfields was suitable for clinical use, but not for machine learning research. So we’ve invested significantly in cleaning up, curating and labelling the dataset to create one of the best AI-ready databases for eye research in the world.

This improved database is owned by Moorfields as a non-commercial public asset, and it’s already been used by hospital researchers for nine separate studies into a wide range of conditions - with many more to come. Moorfields can also use DeepMind’s trained AI model for their future non-commercial research efforts.

For all of us who have worked on this since we signed our agreement with Moorfields in 2016, this is a hugely exciting milestone, and another indication of what is possible when clinicians and technologists work together. We’ll continue to keep you updated as we make progress.

**Notes**

Read the full text open access paper on Nature Medicine [here](https://www.nature.com/articles/s41591-018-0107-6.epdf?author_access_token=PAbvHEuv_YYmrPVbG5HqKdRgN0jAjWel9jnR3ZoTv0P43NEH20hFuvBoJk6cvICihn8kmL6tmejFlnuPlbT_0KmJgK6N07SPh_ZLy0Nxb0-LAGIDBaH1fjJTkD9ahUEQpRlEudtlG9E1v3ca9xNQcQ%3D%3D)

Download the Author's version [here](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/a-major-milestone-for-the-treatment-of-eye-disease/De%20Fauw%20et.%20al%20Nature%20Medicine%202018.pdf) [PDF]
