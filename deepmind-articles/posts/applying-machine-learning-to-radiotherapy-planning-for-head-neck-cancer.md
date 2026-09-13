---
title: "Applying machine learning to radiotherapy planning for head & neck cancer"
source: https://deepmind.google/blog/applying-machine-learning-to-radiotherapy-planning-for-head-neck-cancer/
site: deepmind
date: 2016-08-30
authors: 
crawled: 2026-09-13
---

We’re excited to announce a new research partnership with the Radiotherapy Department at University College London Hospitals NHS Foundation Trust, which provides world-leading cancer treatment.

1 in 75 men and 1 in 150 women will be diagnosed with oral cancer during their lifetime, and oral cavity cancer has risen by 92% since the 1970s. Head and neck cancer in general affects over 11,000 patients in the UK alone each year.

Advances in treatment such as radiotherapy have improved survival rates, but because of the high number of delicate structures concentrated in this area of the body, clinicians have to plan treatment extremely carefully to ensure none of the vital nerves or organs are damaged.

That makes a cancer at the back of the mouth or in the sinuses, for example, particularly hard to treat with radiotherapy.

So with clinicians in UCLH’s world-leading radiotherapy team we are exploring whether machine learning methods could reduce the amount of time it takes to plan radiotherapy treatment for such cancers. Before radiotherapy can be administered, clinicians have to produce a detailed map of the areas of the body to be treated, and the areas to avoid.

The process, known as segmentation, involves drawing around different parts of the anatomy and feeding the information through to a radiotherapy machine, which can then target cancers while leaving healthy tissue unharmed.

But when a tumour and vital anatomical structures are found in such close proximity, as in the head and neck, the outlines clinicians produce must be painstakingly detailed.

For these cancers, segmentation can take around four hours. And even though UCLH’s specialist team at its dedicated head and neck cancer centre is a national leader in this process, there is still potential for innovation. We think machine learning could make a difference.

Our collaboration will see us carefully analyse anonymised scans from up to seven hundred former patients at UCLH, to determine the potential for machine learning to make radiotherapy planning more efficient.

Clinicians will remain responsible for deciding radiotherapy treatment plans but it is hoped that the segmentation process could be reduced from up to four hours to around an hour.

We hope that in time, the research could lead to two benefits in particular:

1. Freeing up clinicians’ time to focus more on patient care, education and research
2. Developing a radiotherapy segmentation algorithm that can potentially be applied to other areas of the body.

As with all our work with the NHS, we will treat the patient data we are using in this project with the utmost care and respect. All scans will be anonymised in line with the UCLH Information Governance policy before they are shared with DeepMind. You can read more about our own approach to information governance [here](https://deepmind.com/about/health).

This kind of research is still exploratory, but we think it has great potential to help both clinicians and patients.

![An axial CT scan of a patient's head and neck region, displaying detailed anatomical structures such as the spine, airway, and surrounding tissues for radiotherapy planning.](https://lh3.googleusercontent.com/Koc4qA9xMnSQsZBJPIMIn6i_kX4zRP2Ro92a7P5g64GYXTHwElbWYuM957Y2BkcIxFQYBwnGBijEikZetjEdYmCvIyYjYCEHpfWMEzH_ckbILNXW=w1440)

An example image taken from a computed tomography (CT) scan sequence for a patient with head and neck cancer. This is for demonstrative purposes only and is not one of the scans shared with DeepMind as part of the collaboration with UCLH.

**Notes**

This image has been reproduced, unmodified, from [The Cancer Image Archive](https://wiki.cancerimagingarchive.net/display/Public/TCGA-HNSC) under the terms of the [Creative Commons Attribution 3.0 Unported License](http://creativecommons.org/licenses/by/3.0/).

Zuley ML, Jarosz R, Kirk S, et al. 2016. Radiology Data from The Cancer Genome Atlas Head-Neck Squamous Cell Carcinoma [TCGA-HNSC] collection. [The Cancer Imaging Archive](https://wiki.cancerimagingarchive.net/display/Public/TCGA-HNSC).
Clark K, Vendt B, Smith K, et al. 2013. The Cancer Imaging Archive (TCIA): Maintaining and Operating a Public Information Repository. Journal of Digital Imaging, 26:6:1045-1057
