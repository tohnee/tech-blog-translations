---
title: "Enabling high-accuracy protein structure prediction at the proteome scale"
source: https://deepmind.google/blog/enabling-high-accuracy-protein-structure-prediction-at-the-proteome-scale/
site: deepmind
date: 2021-07-22
authors: Kathryn Tunyasuvunakool, Jonas Adler, Zachary Wu, Tim Green, Michal Zielinski, Augustin Žídek, Alex Bridgland, Andrew Cowie, Clemens Meyer, Agata Laydon, Sameer Velanka, Gerard Kleywegt, Alex Bateman, Richard Evans, Alexander Pritzel, Michael Figurnov, Olaf Ronneberger, Russ Bates, Simon A. A. Kohl, Anna Potapenko, Andrew J Ballard, Bernardino Romera-Paredes, Stanislav Nikolov, Rishub Jain, Ellen Clancy, David Reiman, Stig Petersen, Andrew Senior, Koray Kavukcuoglu, Ewan Birney, Pushmeet Kohli, John Jumper, Demis Hassabis
crawled: 2026-09-13
---

## The AlphaFold method

Many novel machine learning innovations contribute to AlphaFold’s current level of accuracy. We give a high-level overview of the system below; for a technical description of the network architecture see our AlphaFold [methods paper](https://www.nature.com/articles/s41586-021-03819-2) and especially its extensive Supplementary Information.

The AlphaFold network consists of two main stages. Stage 1 takes as input the amino acid sequence and a multiple sequence alignment (MSA). Its goal is to learn a rich “pairwise representation” that is informative about which residue pairs are close in 3D space.

Stage 2 uses this representation to directly produce atomic coordinates by treating each residue as a separate object, predicting the rotation and translation necessary to place each residue, and ultimately assembling a structured chain. The design of the network draws on our intuitions about protein physics and geometry, for example, in the form of the updates applied and in the choice of loss.

Interestingly, we can produce a 3D structure based on the representation at intermediate layers of the network. The resulting “trajectory” videos show how AlphaFold’s belief about the correct structure develops during inference, layer by layer. Typically a hypothesis emerges after the first few layers followed by a lengthy process of refinement, although some targets require the full depth of the network to arrive at a good prediction.

![An animated 3D trajectory video showing how AlphaFold's predicted protein structure develops and refines during inference, layer by layer, starting from a rough hypothesis to a highly structured multi-colored chain.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/fig_1_BeVC9fP.gif)

![An animated 3D trajectory video showing how AlphaFold's predicted protein structure develops and refines during inference, layer by layer, starting from a rough hypothesis to a highly structured multi-colored chain.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/fig_2_6UHmi8M.gif)

![An animated 3D trajectory video showing how AlphaFold's predicted protein structure develops and refines during inference, layer by layer, starting from a rough hypothesis to a highly structured multi-colored chain.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/fig_3_6Ul0Gch.gif)

Predicted structure for the CASP14 targets T1044, T1024 and T1064 at successive layers of the network. Structures are colored by residue number and the counter shows the current layer.

## Accuracy and confidence

AlphaFold was stringently assessed in the [CASP14](https://predictioncenter.org/casp14/zscores_final.cgi) experiment, in which participants blindly predict protein structures that have been solved but not yet made public. The method achieved high accuracy in a majority of cases, with an average 95% RMSD-Cα to the experimental structure of less than 1Å. In our papers, we further evaluate the model on a much larger set of recent PDB entries. Among the findings are strong performance on large proteins and good side chain accuracy where the backbone is well-predicted.

![Bar chart showing AlphaFold’s CASP14 accuracy relative to other methods such as Tfold_Human, Baker, Zhang, Baker experimental.](https://lh3.googleusercontent.com/w0ugEc2xzlJObbTQh51BMG153ONu_3lEsbxr9eLKDX7hEUF7Pqh1pNUaE1guX8TA8gKsGhgaoLA5g3sjcuA2287A37_gIDgzn8q4Nky_DvlxWHtkgeQ=w1440)

AlphaFold’s CASP14 accuracy relative to other methods. RMSD-Cα based on the best-predicted 95% of residues for each target.

An important factor in the utility of structure predictions is the quality of the associated confidence measures. Can the model identify the parts of its prediction likely to be reliable? We have developed two confidence measures on top of the AlphaFold network to address this question.

The first is pLDDT ([predicted lDDT-Cα](https://doi.org/10.1093/bioinformatics/btt473)), a per-residue measure of local confidence on a scale from 0 - 100. pLDDT can vary dramatically along a chain, enabling the model to express high confidence on structured domains but low confidence on the linkers between them, for example. In our [paper](https://www.nature.com/articles/s41586-021-03828-1), we present evidence that some regions with low pLDDT may be unstructured in isolation; either intrinsically disordered or structured only in the context of a larger complex. Regions with pLDDT < 50 should not be interpreted except as a possible disorder prediction.

The second metric is PAE (Predicted Aligned Error), which reports AlphaFold’s expected position error at residue x, when the predicted and true structures are aligned on residue y. This is useful for assessing confidence in global features, especially domain packing. For residues x and y drawn from two different domains, a consistently low PAE at (x, y) suggests AlphaFold is confident about the relative domain positions. Consistently high PAE at (x, y) suggests the relative positions of the domains should not be interpreted. The general approach used to produce PAE can be adapted to predict a variety of superposition-based metrics, including [TM-score](https://doi.org/10.1002/prot.20264) and [GDT](https://doi.org/10.1093/nar/gkg571).

![A diagram illustrating AlphaFold's confidence metrics. On the left, two predicted protein structures are color-coded by per-residue confidence (pLDDT), showing high/medium confidence in blue and low/very low confidence in orange. On the right, two Predicted Aligned Error (PAE) heatmaps are shown: the top map illustrates "uncertain relative positions" with localized dark green squares indicating well-defined individual domains but lack of inter-domain confidence, while the bottom map illustrates "confident relative positions" with large green blocks indicating high confidence in the global, relative arrangement of domains.](https://lh3.googleusercontent.com/g__7WFe_n5sioMoF0oIAPVVFkNHPA5T5T5Rcd1VdTBOzUoQqZ3szE-LjuZPJmg_llUFsoRUtvUX3XrmKb74S1cK44l8GjMMlrUpMQvvFf5jKkRb1z2I=w1440)

Per-residue confidence (pLDDT) and Predicted Aligned Error (PAE) for two example proteins (P54725, Q5VSL9). Both have confident individual domains, but the latter also has confident relative domain positions. Note: Q5VSL9 was solved after this prediction was produced.

To emphasise, AlphaFold models are ultimately predictions: while often highly accurate they will sometimes be in error. Predicted atomic coordinates should be interpreted carefully, and in the context of these confidence measures.

## Open sourcing

Alongside our [method paper](https://www.nature.com/articles/s41586-021-03819-2), we have made the AlphaFold source code available on [GitHub](https://github.com/deepmind/alphafold). This includes access to a trained model and a script for making predictions on novel input sequences. We believe this is an important step that will enable the community to use and build on our work. The easiest way to fold a single new protein with AlphaFold is to use our [Colab notebook](https://bit.ly/alphafoldcolab).

The open source code is an updated version of our CASP14 system based on the [JAX framework](https://github.com/google/jax), and it achieves equally high accuracy. It also incorporates some recent performance improvements. AlphaFold’s speed has always depended heavily on the input sequence length, with short proteins taking minutes to process and only very long proteins running into hours. Once the MSA has been assembled, the open source version can now predict the structure of a 400 residue protein in just over a minute of GPU time on a V100.

## Proteome scale and AlphaFold DB

AlphaFold’s fast inference times allow the method to be applied at whole-proteome scale. In our [paper](https://www.nature.com/articles/s41586-021-03828-1), we discuss AlphaFold’s predictions for the human proteome. However, we have since generated predictions for the reference proteomes of a number of [model organisms, pathogens and economically significant species](https://alphafold.ebi.ac.uk/download), and large scale prediction is now routine. Interestingly, we observe a difference in the pLDDT distribution between species, with generally higher confidence on bacteria and archaea and lower confidence on eukaryotes, which we hypothesize may be related to the prevalence of disorder in these proteomes.

No single research group can fully explore such a large dataset, and so we partnered with [EMBL-EBI](https://www.ebi.ac.uk/) to make the predictions freely available via the [AlphaFold DB](https://alphafold.ebi.ac.uk/). Each prediction can be viewed alongside the confidence metrics described above. A bulk download is also provided for each species, and all data is covered by a CC-BY-4.0 license (making it freely available for both academic and commercial use). We are extremely grateful to EMBL-EBI for their work with us to develop this new resource. Over the course of the coming months we plan to expand the dataset to cover the over 100 million proteins in [UniRef90](https://www.uniprot.org/uniref/?query=&fil=identity:0.9).

![A 3x3 grid of various 3D protein structures predicted by AlphaFold for different reference proteomes (including fission yeast, C. elegans, M. tuberculosis, budding yeast, fruit fly, P. falciparum, Arabidopsis, Dictyostelium, and E. coli), color-coded by per-residue prediction confidence (pLDDT) from high confidence (blue) to low confidence (orange).](https://lh3.googleusercontent.com/GqFl_KlLOJ6EmtNLXYYTKQFT1lwT3OFPy_jrEkKzEyB6cFRcrqcg8VC3dDtYzSZ7AzkPJEA4V98UHq7WWHpUhiJUNqMyQOmDoQJnF1fKVzJyM3lh=w1440)

Example: AlphaFold DB predictions from a variety of organisms.

![Three 3D ridge plots illustrating the distribution of AlphaFold’s per-residue prediction confidence (pLDDT) across fifteen reference proteomes. Eukaryotic proteomes (center and right) generally show lower confidence and a higher prevalence of low-confidence regions than bacterial and archaeal proteomes (left), which show a sharp spike near 100% confidence.](https://lh3.googleusercontent.com/VaeRpgcBDCr-tB8f42iE4cXy0tTjghF9lYoqL3aTau-fgS5YAkaj74IFaj-tifz2kErEIlNa1KVkVICfVSfZvL7Co4wqD1Jj56pT5665cmUJgp1Fs70=w1440)

Distribution of per-residue confidence for 14 species; left to right: bacteria / archaea, animals, and protists.

In AlphaFold DB, we have chosen to share predictions of full protein chains up to 2700 amino acids in length, rather than cropping to individual domains. The rationale is that this avoids missing structured regions that have yet to be annotated. It also provides context from the full amino acid sequence, and allows the model to attempt a domain packing prediction. AlphaFold’s intra-domain accuracy was more extensively evaluated in CASP14 and is expected to be higher than its inter-domain accuracy. However, AlphaFold was the top ranked method in the inter-domain assessment, and we expect it to produce an informative prediction in some cases. We encourage users to view the PAE plot to determine whether domain placement is likely to be meaningful.

## Future work

We are excited about the future for computational structural biology. There remain many important topics to address: predicting the structure of complexes, incorporating non-protein components, and capturing dynamics and the response to point mutations. The development of network architectures like AlphaFold that excel at the task of understanding protein structure is a cause for optimism that we can make progress on related problems.

We see AlphaFold as a complementary technology to experimental structural biology. This is perhaps best illustrated by its role in helping to solve experimental structures, through molecular replacement and docking into cryo-EM volumes. Both applications can accelerate existing research, saving months of effort. From a bioinformatics perspective, AlphaFold’s speed enables the generation of predicted structures on a massive scale. This has the potential to unlock new avenues of research, by supporting structural investigations of the contents of large sequence databases.

Ultimately, we hope AlphaFold will prove a useful tool for illuminating protein space, and we look forward to seeing how it is applied in the coming months and years.

We would love to hear your feedback and understand how AlphaFold and the AlphaFold DB have been useful in your research. Share your stories at [alphafold@deepmind.com](mailto:alphafold@deepmind.com).
