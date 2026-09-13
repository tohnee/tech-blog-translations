---
title: "A catalogue of genetic mutations to help pinpoint the cause of diseases"
source: https://deepmind.google/blog/a-catalogue-of-genetic-mutations-to-help-pinpoint-the-cause-of-diseases/
site: deepmind
date: 2023-09-19
authors: 
crawled: 2026-09-13
---

New AI tool classifies the effects of 71 million ‘missense’ mutations

Uncovering the root causes of disease is one of the greatest challenges in human genetics. With millions of possible mutations and limited experimental data, it’s largely still a mystery which ones could give rise to disease. This knowledge is crucial to faster diagnosis and developing life-saving treatments.

Today, we’re releasing a [catalogue](https://zenodo.org/record/8360242) of ‘missense’ mutations where researchers can learn more about what effect they may have. Missense variants are genetic mutations that can affect the function of human proteins. In some cases, they can lead to diseases such as cystic fibrosis, sickle-cell anaemia, or cancer.

The AlphaMissense catalogue was developed using AlphaMissense, our new AI model which classifies missense variants. In a paper published in [Science](https://www.science.org/doi/10.1126/science.adg7492), we show it categorised 89% of all 71 million possible missense variants as either likely pathogenic or likely benign. By contrast, only 0.1% have been confirmed by human experts.

AI tools that can accurately predict the effect of variants have the power to accelerate research across fields from molecular biology to clinical and statistical genetics. [Experiments to uncover disease-causing mutations](https://genomebiology.biomedcentral.com/articles/10.1186/s13059-023-02986-x) are expensive and laborious – every protein is unique and each experiment has to be designed separately which can take months. By using AI predictions, researchers can get a preview of results for thousands of proteins at a time, which can help to prioritise resources and accelerate more complex studies.

We’ve made all of our predictions freely available for commercial and researcher use, and open sourced the [model code for AlphaMissense](https://github.com/deepmind/alphamissense).

![A visualization comparing predictions for all 71 million human missense variants. The top pie chart shows AlphaMissense predictions: 57% likely benign (blue), 32% likely pathogenic (pink), and 11% uncertain (grey). The bottom chart shows human annotations: approximately 6% seen in humans (dark blue circle) and approximately 0.1% confirmed by human experts (small purple circle inside), representing a tiny fraction of the total variants.](https://lh3.googleusercontent.com/sbPsonVn4kyy5ZQ3kFmJ0BQb1jIolWkueQwpcUuIKDxemcFlLAQFLl_NWr2mbJsSZdCLVSNjqQBl9CkWebx-Q9qc7GsdWsfYu3W4naAu_B0OMawz=w1440)

AlphaMissense predicted the pathogenicity of all possible 71 million missense variants. It classified 89% – predicting 57% were likely benign and 32% were likely pathogenic.

## What is a missense variant?

A missense variant is a single letter substitution in DNA that results in a different amino acid within a protein. If you think of DNA as a language, switching one letter can change a word and alter the meaning of a sentence altogether. In this case, a substitution changes which amino acid is translated, which can affect the function of a protein.

The average person is carrying [more than 9,000 missense variants](https://www.nature.com/articles/s41586-021-04103-z/tables/1). Most are benign and have little to no effect, but others are pathogenic and can severely disrupt protein function. Missense variants can be used in the diagnosis of rare genetic diseases, where a few or even a single missense variant may directly cause disease. They are also important for studying complex diseases, like type 2 diabetes, which can be caused by a combination of many different types of genetic changes.

Classifying missense variants is an important step in understanding which of these protein changes could give rise to disease. Of more than 4 million missense variants that have been seen already in humans, only 2% have been annotated as pathogenic or benign by experts, roughly 0.1% of all 71 million possible missense variants. The rest are considered ‘variants of unknown significance’ due to a lack of experimental or clinical data on their impact. With AlphaMissense we now have the clearest picture to date by classifying 89% of variants using a threshold that yielded 90% precision on a database of known disease variants.

## Pathogenic or benign: How AlphaMissense classifies variants

AlphaMissense is based on our breakthrough model [AlphaFold](https://www.deepmind.com/research/highlighted-research/alphafold), which predicted structures for nearly all proteins known to science from their amino acid sequences. Our adapted model can predict the pathogenicity of missense variants altering individual amino acids of proteins.

To train AlphaMissense, we fine-tuned AlphaFold on labels distinguishing variants seen in human and closely related primate populations. Variants commonly seen are treated as benign, and variants never seen are treated as pathogenic. AlphaMissense does not predict the change in protein structure upon mutation or other effects on protein stability. Instead, it leverages databases of related protein sequences and structural context of variants to produce a score between 0 and 1 approximately rating the likelihood of a variant being pathogenic. The continuous score allows users to choose a threshold for classifying variants as pathogenic or benign that matches their accuracy requirements.

![Diagram illustrating the AlphaMissense workflow. Under "Input," a reference DNA codon (CAG) and protein amino acid (Q) mutate into a missense variant (CGG and R). Under "AlphaMissense," this input is processed using "1. Structure context" and "2. Protein language modeling." Under "Output," AlphaMissense predicts a pathogenicity score from 0 to 1, classifying the variant as Pathogenic (pink, near 1), Uncertain (grey), or Benign (blue, near 0).](https://lh3.googleusercontent.com/g3tJ2fMpu0Zn1KBxI_Z1bVJ_F7b6S4kp-oYSDfFEc4GYwC4cO0PMl5IoOwjvEMCOWeULbFjbHhuTH2ccb0rNbvSimX2I-dwNR9Gl_mctAlW5hqov=w1440)

An illustration of how AlphaMissense classifies human missense variants. A missense variant is input, and the AI system scores it as pathogenic or likely benign. AlphaMissense combines structural context and protein language modelling, and is fine-tuned on human and primate variant population frequency databases.

AlphaMissense achieves state-of-the-art predictions across a wide range of genetic and experimental benchmarks, all without explicitly training on such data. Our tool outperformed other computational methods when used to classify variants from ClinVar, a public archive of data on the relationship between human variants and disease. Our model was also the most accurate method for predicting results from the lab, which shows it is consistent with different ways of measuring pathogenicity.

![Two horizontal bar charts comparing the performance of AlphaMissense against other computational methods. On the left, for ClinVar classification (auROC), AlphaMissense outperforms other models with a score above 0.9. On the right, for experimental assays across 25 proteins (mean Spearman correlation), AlphaMissense again achieves the highest score, near 0.5.](https://lh3.googleusercontent.com/cxViWkcfi2AVD3dhVQEdBjJ-zzFU4ToCyfS8SD5U0iNpwgjSedQ3icOpwTJ5Zs2VrTHfGpa7A0KBFfEGLRMyJHsNPDODmj-wpwzdanE9GH-nOMHkg3A=w1440)

**AlphaMissense outperforms other computational methods on predicting missense variant effects.**
**Left:** Comparing AlphaMissense and other methods’ performance on classifying variants from the Clinvar public archive. Methods shown in grey were trained directly on ClinVar and their performance on this benchmark are likely overestimated since some of their training variants are contained in this test set.
**Right:** Graph comparing AlphaMissense and other methods’ performance on predicting measurements from biological experiments.

## Building a community resource

AlphaMissense builds on AlphaFold to further the world’s understanding of proteins. One year ago, we released [200 million protein structures](https://www.deepmind.com/blog/alphafold-reveals-the-structure-of-the-protein-universe) predicted using AlphaFold – which is helping millions of scientists around the world to accelerate research and pave the way toward new discoveries. We look forward to seeing how AlphaMissense can help solve open questions at the heart of genomics and across biological science.

We’ve made AlphaMissense’s predictions freely available to both commercial and scientific communities. Together with EMBL-EBI, we are also making them more usable through the [Ensembl Variant Effect Predictor](https://www.ensembl.org/info/docs/tools/vep/script/vep_plugins.html#alphamissense).

In addition to our look-up table of missense mutations, we’ve shared the expanded predictions of all possible 216 million single amino acid sequence substitutions across more than 19,000 human proteins. We’ve also included the average prediction for each gene, which is similar to measuring a gene's evolutionary constraint – this indicates how essential the gene is for the organism’s survival.

![Two 3D protein structure visualizations colored by AlphaMissense pathogenicity predictions, with red indicating likely pathogenic regions and blue indicating likely benign regions. On the left is the Hemoglobin subunit beta (HBB) protein with small spheres highlighting variant locations, and on the right is the highly complex Cystic fibrosis transmembrane conductance regulator (CFTR) protein structure.](https://lh3.googleusercontent.com/Dm6KiKU9UFGlJ153Ii1zKWtBEGDKU79p1qN4gZqMJUnfcTPmfgxLDzeBpt-p3uIggSw038EKx6qyeEiM7JujpFgj9_OrPfAxgAtFTzGJZ76iOmQK3w=w1440)

Examples of AlphaMissense predictions overlaid on AlphaFold predicted structures (red=predicted as pathogenic, blue=predicted as benign, grey=uncertain). Red dots represent known pathogenic missense variants, blue dots represent known benign variants from the ClinVar database.
**Left:** HBB protein. Variants in this protein can cause sickle cell anaemia.
**Right:** CFTR protein. Variants in this protein can cause cystic fibrosis.

## Accelerating research into genetic diseases

A key step in translating this research is collaborating with the scientific community. We have been working in partnership with Genomics England, to explore how these predictions could help study the genetics of rare diseases. Genomics England cross-referenced AlphaMissense’s findings with variant pathogenicity data previously aggregated with human participants. Their evaluation confirmed our predictions are accurate and consistent, providing another real-world benchmark for AlphaMissense.

While our predictions are not designed to be used in the clinic directly – and should be interpreted with other sources of evidence – this work has the potential to improve the diagnosis of rare genetic disorders, and help discover new disease-causing genes.

Ultimately, we hope that AlphaMissense, together with other tools, will allow researchers to better understand diseases and develop new life-saving treatments.

Learn more about AlphaMissense:

[Read our paper in Science](https://www.science.org/stoken/author-tokens/ST-1429/full)[Ensembl Variant Effect Predictor plugin](https://www.ensembl.org/info/docs/tools/vep/script/vep_plugins.html#alphamissense)[Download AlphaMissense code](https://github.com/google-deepmind/alphamissense)

**Notes**

\*As of 13 March 2024 the AlphaMissense predictions are available under a [CC BY v.4](https://creativecommons.org/licenses/by/4.0/legalcode) license, thereby lifting the previous non-commercial use restriction.  Please see [published database](https://console.cloud.google.com/storage/browser/dm_alphamissense) and [Zenodo](https://zenodo.org/records/10813168) for further access information.

We would like to thank Juanita Bawagan, Jess Valdez, Katie McAtackney, Kathryn Seager, Hollie Dobson, for their help with text and figures. We are also grateful to our external partners, Genomics England and EMBL-EBI, for their continuous support. This work was done thanks to the contributions of the co-authors: Guido Novati, Joshua Pan, Clare Bycroft, Akvilė Žemgulytė, Taylor Applebaum, Alexander Pritzel, Lai Hong Wong, Michal Zielinski, Tobias Sargeant, Rosalia G. Schneider, Andrew W. Senior, John Jumper, Demis Hassabis, Pushmeet Kohli. We would also like to thank Kathryn Tunyasuvunakool, Rob Fergus, Eliseo Papa, David La, Zachary Wu, Sara-Jane Dunn, Kyle R. Taylor, Natasha Latysheva, Hamish Tomlinson, Augustin Žídek, Roz Onions, Mira Lutfi, Jon Small, Molly Beck, Annette Obika, Hannah Gladman, Folake Abu, Alyssa Pierce, James Tam, Q Green, Meera Last, Tharindi Hapuarachchi and the greater Google DeepMind team for their support, help and feedback.
