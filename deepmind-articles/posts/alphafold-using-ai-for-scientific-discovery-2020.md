---
title: "AlphaFold: Using AI for scientific discovery"
source: https://deepmind.google/blog/alphafold-using-ai-for-scientific-discovery-2020/
site: deepmind
date: 2020-01-15
authors: 
crawled: 2026-09-13
---

UPDATE: In July 2022, we released AlphaFold protein structure predictions for nearly all catalogued proteins known to science. Read the latest blog [here](https://deepmind.com/blog/alphafold-reveals-the-structure-of-the-protein-universe).

In our study [published in Nature](https://rdcu.be/b0mtx), we demonstrate how artificial intelligence research can drive and accelerate new scientific discoveries. We’ve built a dedicated, interdisciplinary team in hopes of using AI to push basic research forward: bringing together experts from the fields of structural biology, physics, and machine learning to apply cutting-edge techniques to predict the 3D structure of a protein based solely on its genetic sequence.

Our system, AlphaFold – described in peer-reviewed papers now published in [Nature](https://rdcu.be/b0mtx) and [PROTEINS](https://onlinelibrary.wiley.com/doi/abs/10.1002/prot.25834) – is the culmination of several years of work, and builds on decades of prior research using large genomic datasets to predict protein structure. The 3D models of proteins that AlphaFold generates are far more accurate than any that have come before - marking significant progress on one of the core challenges in biology. The AlphaFold code used at CASP13 is available on Github [here](https://github.com/deepmind/deepmind-research/tree/master/alphafold_casp13) for anyone interested in learning more or replicating our results. We’re also excited by the fact that this work has already inspired other, independent implementations, including the model described in [this paper](https://www.biorxiv.org/content/10.1101/846279v1.full.pdf), and a community - built, [open source implementation](https://github.com/dellacortelab/prospr), described [here](https://www.biorxiv.org/content/10.1101/830273v1).

## What is the protein-folding problem?

Proteins are large, complex molecules essential to all of life. Nearly every function that our body performs - contracting muscles, sensing light, or turning food into energy - relies on proteins, and how they move and change. What any given protein can do depends on its unique 3D structure. For example, antibody proteins utilised by our immune systems are ‘Y-shaped’, and form unique hooks. By latching on to viruses and bacteria, these antibody proteins are able to detect and tag disease - causing microorganisms for elimination. Collagen proteins are shaped like cords, which transmit tension between cartilage, ligaments, bones, and skin. Other types of proteins include Cas9, which, using CRISPR sequences as a guide, act like scissors to cut and paste sections of DNA; antifreeze proteins, whose 3D structure allows them to bind to ice crystals and prevent organisms from freezing; and ribosomes, which act like a programmed assembly line, helping to build proteins themselves.

The recipes for those proteins - called genes - are encoded in our DNA. An error in the genetic recipe may result in a malformed protein, which could result in disease or death for an organism. Many diseases, therefore, are fundamentally linked to proteins. But just because you know the genetic recipe for a protein doesn’t mean you automatically know its shape. Proteins are comprised of chains of amino acids (also referred to as amino acid residues). But DNA only contains information about the sequence of amino acids - not how they fold into shape. The bigger the protein, the more difficult it is to model, because there are more interactions between amino acids to take into account. As demonstrated by [Levinthal’s paradox](https://en.wikipedia.org/wiki/Levinthal%27s_paradox), it would take longer than the age of the known universe to randomly enumerate all possible configurations of a typical protein before reaching the true 3D structure - yet proteins themselves fold spontaneously, within milliseconds. Predicting how these chains will fold into the intricate 3D structure of a protein is what’s known as the “protein-folding problem” - a challenge that scientists have worked on for decades. This unsolved problem has already inspired countless developments, from spurring IBM’s efforts in supercomputing ([BlueGene](https://en.wikipedia.org/wiki/IBM_Blue_Gene)), to novel citizen science efforts ([Folding@Home](https://foldingathome.org/) and [FoldIt](https://fold.it/portal/)) to new engineering realms, such as rational protein design.

## Why is protein folding important?

> I think that we shall be able to get a more thorough understanding of the nature of disease in general by investigating the molecules that make up the human body, including the abnormal molecules, and that this understanding will permit...the problem of disease to be attacked in a more straightforward manner such that new methods of therapy will be developed.

Linus Pauling

1960

Scientists have long been interested in determining the structures of proteins because a protein’s form is thought to dictate its function. Once a protein’s shape is understood, its role within the cell can be guessed at, and scientists can develop drugs that work with the protein’s unique shape.

Over the past five decades, researchers have been able to determine shapes of proteins in labs using experimental techniques like [cryo-electron microscopy](https://en.wikipedia.org/wiki/Cryogenic_electron_microscopy), [nuclear magnetic resonance](https://en.wikipedia.org/wiki/Nuclear_magnetic_resonance) and [X-ray crystallography](https://en.wikipedia.org/wiki/X-ray_crystallography), but each method depends on a lot of trial and error, which can take years of work, and cost tens or hundreds of thousands of dollars per protein structure. This is why biologists are turning to AI methods as an alternative to this long and laborious process for difficult proteins. The ability to predict a protein’s shape computationally from its genetic code alone – rather than determining it through costly experimentation – could help accelerate research.

![A four-step diagram illustrating how proteins fold: starting from a sequence of amino acids, forming local shapes like alpha helices and pleated sheets, folding into a complex 3D protein structure, and finally interacting with other proteins.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62273f8719ed3b2a84c8fd13_Fig201.svg)

Figure 1: Complex 3D shapes emerge from a string of amino acids.

## How can AI make a difference?

Fortunately, the field of genomics is quite rich in data thanks to the rapid reduction in the cost of genetic sequencing. As a result, deep learning [approaches](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1005324) to the prediction problem that rely on genomic data have become increasingly popular in the last few years. To catalyse research and measure progress on the newest methods for improving the accuracy of predictions, a biennial global competition called CASP ([Critical Assessment of protein Structure Prediction](http://predictioncenter.org/)) was established in 1994, and has become the gold standard for assessing predictive techniques. We’re indebted to decades of prior work by the CASP organisers, as well as to the thousands of experimentalists whose structures enable this kind of assessment.

DeepMind’s work on this problem resulted in AlphaFold, which we submitted to CASP13. We’re proud to be part of what the CASP organisers have called “unprecedented progress in the ability of computational methods to predict protein structure,” placing [first](http://predictioncenter.org/casp13/zscores_final.cgi?formula=assessors) in rankings among the teams that entered (our entry is A7D).

Our team focused specifically on the problem of modelling target shapes from scratch, without using previously solved proteins as templates. We achieved a high degree of accuracy when predicting the physical properties of a protein structure, and then used two distinct methods to construct predictions of full protein structures.

## Using neural networks to predict physical properties

Both of these methods relied on deep neural networks that are trained to predict properties of the protein from its genetic sequence. The properties our networks predict are: (a) the distances between pairs of amino acids and (b) the angles between chemical bonds that connect those amino acids. The first development is an advance on commonly used techniques that estimate whether pairs of amino acids are near each other.

We trained a neural network to predict a distribution of distances between every pair of residues in a protein (visualised in Figure 2). These probabilities were then combined into a score that estimates how accurate a proposed protein structure is. We also trained a separate neural network that uses all distances in aggregate to estimate how close the proposed structure is to the right answer.

![An animation of the gradient descent method predicting a structure for CASP13 target T1008.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/622692c5f70ee10657e72050_AlphaFold202.gif)

## Using neural networks to predict physical properties

Both of these methods relied on deep neural networks that are trained to predict properties of the protein from its genetic sequence. The properties our networks predict are: (a) the distances between pairs of amino acids and (b) the angles between chemical bonds that connect those amino acids. The first development is an advance on commonly used techniques that estimate whether pairs of amino acids are near each other.

We trained a neural network to predict a distribution of distances between every pair of residues in a protein (visualised in Figure 2). These probabilities were then combined into a score that estimates how accurate a proposed protein structure is. We also trained a separate neural network that uses all distances in aggregate to estimate how close the proposed structure is to the right answer.

![A comparison of ground truth structures and AlphaFold's average predicted distances for three protein targets (T0954, T0965, and T0955). The top rows show highly matching heatmaps representing the distance between residue pairs, while the bottom row displays 3D ribbon models of the folded proteins, showing near-perfect alignment between the ground truth structures in green and AlphaFold's predicted structures in blue.](https://lh3.googleusercontent.com/anpBtYTh5VH53TPliYMyaHg8s_eb2bOGY8ouE8zSyEaPbEMb7F6p1de40adBWBfXF-pDYo8Zqsa7NH2bf6KSDcy1NMh5sgvMj8Gq4jMJUlMj5MxzWw=w1440)

Figure 2: Two ways of visualising the accuracy of AlphaFold’s predictions. The top figure features the distance matrices for three proteins. The brightness of each pixel represents the distance between the amino acids in the sequence comprising the protein–the brighter the pixel, the closer the pair. Shown in the top row are the real, experimentally determined distances and, in the bottom row, the average of AlphaFold’s predicted distance distributions. Importantly, these match well on both global and local scales. The bottom panels represent the same comparison using 3D models, featuring AlphaFold’s predictions (blue) versus ground-truth data (green) for the same three proteins.

Using these scoring functions, we were able to search the protein landscape to find structures that matched our predictions. Our first method built on techniques commonly used in structural biology, and repeatedly replaced pieces of a protein structure with new protein fragments. We trained a generative neural network to invent new fragments, which were used to continually improve the score of the proposed protein structure.

![A flowchart diagram showing how AlphaFold predicts protein structure: it starts with a protein sequence input, passes through a neural network informed by databases, outputs distance predictions and angle predictions, optimizes these via a gradient descent score, and finally produces the predicted 3D protein structure.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6227400ac14721b5286ae553_AF2004.svg)

The second method optimised scores through [gradient descent](https://en.wikipedia.org/wiki/Gradient_descent) - a mathematical technique commonly used in machine learning for making small, incremental improvements - which resulted in highly accurate structures. This technique was applied to entire protein chains rather than to pieces that must be folded separately before being assembled into a larger structure, to simplify the prediction process.

The AlphaFold version used at CASP13 is available [on Github](https://github.com/deepmind/deepmind-research/tree/master/alphafold_casp13) for anyone interested in learning more, or replicating our protein-folding results.

## What happens next?

While we’re thrilled by the success of our protein-folding model, there’s still much to be done in the realm of protein biology, and we’re excited to continue our efforts in this field. We’re committed to establishing ways that AI can contribute to basic scientific discovery, with the hope of making real-world impact. This approach might serve to ultimately improve our understanding of the body and how it works, enabling scientists to target and design new, effective cures for diseases more efficiently. Scientists have only mapped structures for about half of all the proteins made by human cells. Some rare diseases involve mutations in a single gene, resulting in a malformed protein which can have profound effects on the health of an entire organism. A tool like AlphaFold might help rare disease researchers predict the shape of a protein of interest rapidly and economically. As scientists acquire more knowledge about the shapes of proteins and how they operate through simulations and models, this method may eventually help us contribute to efficient drug discovery, while also reducing the costs associated with experimentation. Our hope is that AI will be useful for disease research, and ultimately improve the quality of life for millions of patients around the world.

But potential benefits aren’t restricted to health alone - understanding protein folding will assist in protein design, which could unlock a tremendous [number of benefits](https://science.sciencemag.org/content/338/6110/1042). For example, advances in biodegradable enzymes - which can be enabled by protein design - could help manage pollutants like plastic and oil, helping us break down waste in ways that are more friendly to our environment. In fact, researchers have already begun [engineering bacteria](https://www.bbc.co.uk/news/science-environment-43783631) to secrete proteins that will make waste biodegradable, and easier to process.

The success of our first foray into protein folding is indicative of how machine learning systems can integrate diverse sources of information to help scientists come up with creative solutions to complex problems at speed. Just as we’ve seen how AI can help people master complex games through systems like [AlphaGo](https://deepmind.com/research/alphago/) and [AlphaZero](https://deepmind.google/blog/alphago-zero-starting-from-scratch/), we similarly hope that one day, AI breakthroughs will help serve as a platform to advance our understanding of fundamental scientific problems, too.

It’s exciting to see these early signs of progress in protein folding, demonstrating the utility of AI for scientific discovery. Even though there’s a lot more work to do before we’re able to have a quantifiable impact on treating diseases, managing waste, and more, we know the potential is enormous. With a [dedicated team](https://deepmind.com/about/science) focused on delving into how machine learning can advance the world of science, we’re looking forward to seeing the many ways our technology can make a difference.

Listen to our [podcast](https://deepmind.com/blog/article/podcast-episode-5-out-of-the-lab) featuring the researchers behind this work.

This blog post is based on the following work

[AlphaFold: Improved protein structure prediction using potentials from deep learning](https://rdcu.be/b0mtx) (Nature)

[Protein structure prediction using multiple deep neural networks in CASP13](https://onlinelibrary.wiley.com/doi/abs/10.1002/prot.25834) (PROTEINS)

The AlphaFold version used at CASP13 is available [on Github](https://github.com/deepmind/deepmind-research/tree/master/alphafold_casp13) for anyone interested in learning more, or replicating our protein folding results.

This work was done in collaboration with Andrew Senior, Richard Evans, John Jumper, James Kirkpatrick, Laurent Sifre, Tim Green, Chongli Qin, Augustin Žídek, Sandy Nelson, Alex Bridgland, Hugo Penedones, Stig Petersen, Karen Simonyan, Steve Crossan, Pushmeet Kohli, David Jones, David Silver, Koray Kavukcuoglu and Demis Hassabis
