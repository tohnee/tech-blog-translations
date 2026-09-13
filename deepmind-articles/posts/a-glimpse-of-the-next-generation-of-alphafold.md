---
title: "A glimpse of the next generation of AlphaFold"
source: https://deepmind.google/blog/a-glimpse-of-the-next-generation-of-alphafold/
site: deepmind
date: 2023-10-31
authors: 
crawled: 2026-09-13
---

Progress update: Our latest AlphaFold model shows significantly improved accuracy and expands coverage beyond proteins to other biological molecules, including ligands

Since its release in 2020, [AlphaFold](https://deepmind.google/technologies/alphafold/) has revolutionized how proteins and their interactions are understood. Google DeepMind and [Isomorphic Labs](https://www.isomorphiclabs.com/) have been working together to build the foundations of a more powerful AI model that expands coverage beyond just proteins to the full range of biologically-relevant molecules.

Today we’re [sharing an update](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/a-glimpse-of-the-next-generation-of-alphafold/alphafold_latest_oct2023.pdf) on progress towards the next generation of AlphaFold. Our latest model can now generate predictions for nearly all molecules in the [Protein Data Bank](https://www.wwpdb.org/) (PDB), frequently reaching atomic accuracy.

It unlocks new understanding and significantly improves accuracy in multiple key biomolecule classes, including ligands (small molecules), proteins, nucleic acids (DNA and RNA), and those containing post-translational modifications (PTMs). These different structure types and complexes are essential for understanding the biological mechanisms within the cell, and have been challenging to predict with high accuracy.

The model’s expanded capabilities and performance can help accelerate biomedical breakthroughs and realize the next era of 'digital biology’ — giving new insights into the functioning of disease pathways, genomics, biorenewable materials, plant immunity, potential therapeutic targets, mechanisms for drug design, and new platforms for enabling protein engineering and synthetic biology.

Series of predicted structures compared to ground truth (white) from our latest AlphaFold model.

## Above and beyond protein folding

[AlphaFold](https://deepmind.google/discover/blog/alphafold-a-solution-to-a-50-year-old-grand-challenge-in-biology/) was a fundamental breakthrough for single chain protein prediction. [AlphaFold-Multimer](https://www.biorxiv.org/content/10.1101/2021.10.04.463034v2) then expanded to complexes with multiple protein chains, followed by AlphaFold2.3, which improved performance and expanded coverage to larger complexes.

In 2022, AlphaFold’s structure predictions for nearly [all cataloged proteins known to science](https://deepmind.google/discover/blog/alphafold-reveals-the-structure-of-the-protein-universe/) were made freely available via the [AlphaFold Protein Structure Database](https://alphafold.ebi.ac.uk/), in partnership with EMBL's European Bioinformatics Institute (EMBL-EBI).

To date, 1.4 million users in over 190 countries have accessed the AlphaFold database, and scientists around the world have used AlphaFold’s predictions to help advance research on everything from accelerating new [malaria vaccines](https://deepmind.google/discover/blog/stopping-malaria-in-its-tracks/) and advancing [cancer drug discovery](https://deepmind.google/discover/blog/understanding-the-faulty-proteins-linked-to-cancer-and-autism/) to developing [plastic-eating enzymes](https://deepmind.google/discover/blog/creating-plastic-eating-enzymes-that-could-save-us-from-pollution/) for tackling pollution.

Here we show AlphaFold’s remarkable abilities to predict accurate structures beyond protein folding, generating highly-accurate structure predictions across ligands, proteins, nucleic acids, and post-translational modifications.

![Four bar graphs of the next generation AlphaFold model's performance across protein-ligand complexes (top left), proteins (top right), nucleic acids (bottom left), and covalent modifications (bottom right).](https://lh3.googleusercontent.com/U_EZzsp4FXouG5u-mxbBb76Fn9XHCUvZl4ANHe6ULwm8gWnoTejYNvGT4BUahhDWR0ZPzfMEjLw3fGqvfzAgclzh-ZYS6Pr-eu8L5yIKemLFUWCNvg=w1440)

Performance across protein-ligand complexes (a), proteins (b), nucleic acids (c), and covalent modifications (d).

## Accelerating drug discovery

Early analysis also shows that our model greatly outperforms AlphaFold2.3 on some protein structure prediction problems that are relevant for drug discovery, like antibody binding. Additionally, accurately predicting protein-ligand structures is an incredibly valuable tool for drug discovery, as it can help scientists identify and design new molecules, which could become drugs.

Current industry standard is to use ‘docking methods’ to determine interactions between ligands and proteins. These docking methods require a rigid reference protein structure and a suggested position for the ligand to bind to.

Our latest model sets a new bar for protein-ligand structure prediction by outperforming the best reported docking methods, without requiring a reference protein structure or the location of the ligand pocket — allowing predictions for completely novel proteins that have not been structurally characterized before.

It can also jointly model the positions of all atoms, allowing it to represent the full inherent flexibility of proteins and nucleic acids as they interact with other molecules — something not possible using docking methods.

Here, for instance, are three recently published, therapeutically-relevant cases where our latest model’s predicted structures (shown in color) closely match the experimentally determined structures (shown in gray):

1. [PORCN](https://doi.org/10.1038/s41586-022-04952-2): A clinical stage anti-cancer molecule bound to its target, together with another protein.
2. [KRAS](https://doi.org/10.1126/science.adg9652): Ternary complex with a covalent ligand (a molecular glue) of an important cancer target.
3. [PI5P4Kγ](https://doi.org/10.1021/acs.jmedchem.1c01819): Selective allosteric inhibitor of a lipid kinase, with multiple disease implications including cancer and immunological disorders.

![Three digitally rendered structure predictions for PORCN (left), KRAS (center), and PI5P4Kγ (right).](https://lh3.googleusercontent.com/r0AZfPC_RpSbxkc0UWlC_-xjhPqmX8HdjvvOx7hlNer4ZNjkrrDAHSF-BmNdq_huCuFvCV9h_4g7ytyd4Byw72EE4e6j-IEQPxFxe8JGdgKF6q2Ac1U=w1440)

Predictions for PORCN (1), KRAS (2), and PI5P4Kγ (3).

Isomorphic Labs is applying this next generation AlphaFold model to therapeutic drug design, helping to rapidly and accurately characterize many types of macromolecular structures important for treating disease.

## New understanding of biology

By unlocking the modeling of protein and ligand structures together with nucleic acids and those containing post-translational modifications, our model provides a more rapid and accurate tool for examining fundamental biology.

One example involves the structure of [CasLambda bound to crRNA and DNA](https://www.rcsb.org/structure/8DC2), part of the [CRISPR family](https://doi.org/10.1016/j.cell.2022.10.020). CasLambda shares the genome editing ability of the [CRISPR-Cas9 system](https://www.nobelprize.org/prizes/chemistry/2020/press-release/), commonly known as ‘genetic scissors’, which researchers can use to change the DNA of animals, plants, and microorganisms. CasLambda’s smaller size may allow for more efficient use in genome editing.

![Digitally rendered image of the predicted structure for CasLambda (Cas12l) bound to crRNA and DNA, part of the CRISPR subsystem.](https://lh3.googleusercontent.com/btCM7mAXfuNJflMWIp_xUcCMOW4IU6fpS8xXlC7ZLsBDyN4sNpFAyO3rX_DM-CqDHdbAfmdN65M6_P6nO6DBXLXOqCFgG_uNwap1z77Cn0gWNG5WiA=w1440)

Predicted structure of CasLambda (Cas12l) bound to crRNA and DNA, part of the CRISPR subsystem.

The latest version of AlphaFold’s ability to model such complex systems shows us that AI can help us better understand these types of mechanisms, and accelerate their use for therapeutic applications. More examples are [available in our progress update](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/a-glimpse-of-the-next-generation-of-alphafold/alphafold_latest_oct2023.pdf).

## Advancing scientific exploration

Our model’s dramatic leap in performance shows the potential of AI to greatly enhance scientific understanding of the molecular machines that make up the human body — and the wider world of nature.

AlphaFold has already catalyzed major scientific advances around the world. Now, the next generation of AlphaFold has the potential to help advance scientific exploration at digital speed.

Our dedicated teams across Google DeepMind and Isomorphic Labs have made great strides forward on this critical work and we look forward to sharing our continued progress.

[Read our progress update](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/a-glimpse-of-the-next-generation-of-alphafold/alphafold_latest_oct2023.pdf)
