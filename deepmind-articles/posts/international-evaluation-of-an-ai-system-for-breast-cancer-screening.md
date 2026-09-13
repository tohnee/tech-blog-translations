---
title: "International evaluation of an AI system for breast cancer screening"
source: https://deepmind.google/blog/international-evaluation-of-an-ai-system-for-breast-cancer-screening/
site: deepmind
date: 2020-01-01
authors: Scott Mayer McKinney, Marcin T. Sieniek, Varun Godbole, Jonathan Godwin, Natasha Antropova, Hutan Ashrafian, Trevor Back, Mary Chesus, Greg Corrado, Ara Darzi, Mozziyar Etemadi, Florencia Garcia-Vicente, Fiona Gilbert, Mark Halling-Brown, Demis Hassabis, Sunny Jansen, Alan Karthikesalingam, Christopher J Kelly, Dominic King, Joseph Ledsam, David Melnick, Hormuz Mostofi, Bernardino Romera-Paredes, Lily Peng, Joshua Jay Reicher, Richard Sidebottom, Mustafa Suleyman, Daniel Tse, Kenneth C. Young, Jeffrey De Fauw, Shravya Shetty
crawled: 2026-09-13
---

Breast cancer is the second leading cause of death from cancer in women, but outcomes have been shown to improve if caught and treated early. This is why many countries around the world have set up breast cancer screening programmes, aiming to identify breast cancer at earlier stages of the disease, when treatment can be more successful.

However, interpreting mammograms (breast x-rays) remains challenging, as evidenced by the high variability of experts’ performance in detecting cancer. In this collaborative research with [Google Health](https://health.google/) & [Cancer Research UK](https://www.cancerresearchuk.org/) Imperial Centre, [Northwestern University](https://www.northwestern.edu/), and [Royal Surrey County Hospital](https://www.royalsurrey.nhs.uk/) now [published in Nature](https://www.nature.com/articles/s41586-019-1799-6.epdf?author_access_token=V_LKV2xpSv9G1dhANYeWM9RgN0jAjWel9jnR3ZoTv0M5zwPVx5jT4z_z-YkUZTBT6_1AtRXi8QouJM7xB-oSN-cVBoH7f_QTgx-yQN3UBEVfkvO1_5urNT-CZHGCEQNGlCuO69tMQYak4SmdoDqyzg%3D%3D), we developed an AI system capable of surpassing clinical specialists from the UK and US in predicting breast cancer from mammograms, as confirmed by biopsy.

## Breast cancer screening datasets

Breast cancer screening programmes vary from country to country. In the US, women are typically screened every one to two years, and their mammograms are interpreted by a single radiologist. In the UK, women are screened every three years, but each mammogram is interpreted by two radiologists, with an arbitration process in case of disagreement. We utilised large datasets collected in both countries to develop and evaluate this AI system.

The UK evaluation dataset consisted of a random sample of 10% of all women with screening mammograms at two sites in London between 2012 and 2015. It included 25,856 women, 785 of which had a biopsy, and 414 women with cancer that was diagnosed within three years of imaging. These de-identified data was collected as part of the [OPTIMAM](http://commercial.cancerresearchuk.org/optimam-mammography-image-database-and-viewing-software) database effort by Cancer Research UK, and are subject to strict privacy constraints.

The US evaluation dataset consisted of de-identified screening mammograms of 3,097 women collected between 2001 and 2018 from one academic medical centre. We included images from all 1,511 women who were biopsied during this time period and a random subset of women who never underwent biopsy. Among the women who received a biopsy, 686 were diagnosed with cancer within 2 years of imaging.

![A mammogram showing four images – two of each breast from different angles.](https://lh3.googleusercontent.com/fGcjpi6UWNSINjcTGkl9H7MlnCGFDuDpBQZ-l-1orGh6y4XHybt9dAdRufyX7GLh_OKM7XS83yz5F4zQgrIZ-9JZqFrpj_fGDMBYsNKuzxjbTpYVbEU=w1440)

Each mammogram has four images - two of each breast from different angles.

## Assessing the performance of the AI system

We compared the performance of the AI system against decisions made by individual human specialists in the original screening visit. In this evaluation, we found that the AI had an absolute reduction in false positives (women incorrectly referred for further investigation) of 5.7% for US subjects and 1.2% for UK subjects, and a reduction in false negatives (women incorrectly missed for further investigation) of 9.4% for US subjects and 2.7% for UK subjects, compared to human experts. See the [paper](https://www.nature.com/articles/s41586-019-1799-6.epdf?author_access_token=V_LKV2xpSv9G1dhANYeWM9RgN0jAjWel9jnR3ZoTv0M5zwPVx5jT4z_z-YkUZTBT6_1AtRXi8QouJM7xB-oSN-cVBoH7f_QTgx-yQN3UBEVfkvO1_5urNT-CZHGCEQNGlCuO69tMQYak4SmdoDqyzg%3D%3D) for more extensive results.

![Two ROC curves comparing the breast cancer screening performance of the AI system against human readers. The left graph shows UK results (breast cancer in 3 years) where the AI curve is plotted alongside markers for the mean first reader, mean second reader, consensus, and the AI's operating points. The right graph shows US results (breast cancer in 2 years) showing the AI system's ROC curve, its operating point, and a marker representing the mean human reader.](https://lh3.googleusercontent.com/_1zMrIxm4bwgRtC-A54GK0QErvYmo2AYSppuuMpoxKbQHTtBCO9Nppv0SpGThAOyZaoFFCFfmyF66d4am00E9X1ex3Qsr2XYAERN1B-6Z7tpMVzhsg=w1440)

The AI system accurately predicts, solely from screening mammograms, whether a patient will have a biopsy positive for breast cancer (note that only a small fraction of screening visits will result in a biopsy). It does so more accurately than individual human specialists, with lower false positive rates (for cancer prediction within three years for the UK dataset, and within two years for the US dataset). The top left indicates peak performance, with no false positives or false negatives. Credit: McKinney et al, Nature

## Generalisation across populations

To evaluate whether the AI system was able to generalise across populations and screening settings, we ran an experiment in which the AI was only allowed to learn from data from UK subjects, and then evaluated it on data from US subjects. This experiment showed that the AI system still surpassed human expert performance on US data.

This is an encouraging avenue for future research and gives more confidence about the robustness of the AI system. It might be possible that an AI diagnostic system could be beneficial even when used in areas where there is not a significant history of screening mammography on which to train it.

## Future research & potential applications

We’ve yet to determine how to best deploy an AI system for clinical use in mammography. However, we investigated one possible such scenario by using the AI system as a “second reader”. We simulated this by treating the prediction of the AI system as an independent second opinion for every mammogram, taking the place of the ‘second reader’ in the UK ‘double reading’ system. When the AI and the clinician disagreed, the existing arbitration process would take place. In these simulated experiments, we showed that an AI-aided double-reading system could achieve non-inferior performance to the UK system with only 12% of the current second reader workload.

Further research, including prospective clinical studies, will be required to understand the full extent to which this technology can benefit breast cancer screening programmes.
