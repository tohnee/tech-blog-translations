---
title: "Putting the power of AlphaFold into the world’s hands"
source: https://deepmind.google/blog/putting-the-power-of-alphafold-into-the-worlds-hands/
site: deepmind
date: 2022-07-22
authors: Demis Hassabis
crawled: 2026-09-13
---

In July 2022, we released AlphaFold protein structure predictions for nearly all catalogued proteins known to science. Read the latest blog [here](https://deepmind.com/blog/alphafold-reveals-the-structure-of-the-protein-universe).

Today, I’m incredibly proud and excited to announce that DeepMind is making a significant contribution to humanity’s understanding of biology.

When we [announced AlphaFold 2](https://deepmind.com/blog/article/alphafold-a-solution-to-a-50-year-old-grand-challenge-in-biology) last December, it was hailed as a solution to the 50-year old protein folding problem. Last week, we published the [scientific paper](https://www.nature.com/articles/s41586-021-03819-2) and [source code](https://github.com/deepmind/alphafold/) explaining how we created this highly innovative system, and today we’re sharing [high-quality predictions](https://alphafold.ebi.ac.uk/) for the shape of every single protein in the human body, as well as for the proteins of 20 additional organisms that scientists rely on for their research.

As researchers seek cures for diseases and pursue solutions to other big problems facing humankind – including antibiotic resistance, microplastic pollution, and climate change – they will benefit from fresh insights into the structure of proteins. Proteins are like tiny exquisite biological machines. The same way that the structure of a machine tells you what it does, so the structure of a protein helps us understand its function. Today, we are sharing [a trove of information](https://alphafold.ebi.ac.uk/) that doubles [humanity’s understanding of the human proteome](https://www.nature.com/articles/s41586-021-03828-1), and reveals the protein structures found in 20 other biologically-significant organisms, from E.coli to yeast, and from the fruit fly to the mouse.

> This will be one of the most important datasets since the mapping of the Human Genome.

Ewan Birney

EMBL Deputy Director General and EMBL-EBI Director

As a powerful tool that supports the efforts of researchers, we believe this is the most significant contribution AI has made to advancing scientific knowledge to date, and is a great example of the benefits AI can bring to humanity. These insights will underpin many exciting future advances in our understanding of biology and medicine. Thanks to five tireless years of work and a lot of ingenuity from the AlphaFold team, and working closely for the past few months with our partners at [EMBL’s European Bioinformatics Institute (EMBL-EBI)](https://www.ebi.ac.uk/), we are able to share this huge and valuable resource with the world.

![Six different 3D renderings of complex protein structures predicted by AlphaFold, each showing folded alpha-helices, beta-sheets, and loops colored in a gradient of blue, yellow, and orange on a light grey background.](https://lh3.googleusercontent.com/rDmL1vjA-DDXpPoMVp6ugGzpkdD9n6jy-X9ij4cSB_pwzFUkHg_CiuB1D8EbnPkXuV7wu-j_Uy5seybyeKDJNAID2YwAWIf2MRjo1DJh5UWeWsDWxA=w1440)

Proteins are exquisite biological machines, their three-dimensional structures are often aesthetically pleasing as well as functionally critical as the building blocks of life.

This latest work builds on [announcements](https://deepmind.com/blog/article/alphafold-a-solution-to-a-50-year-old-grand-challenge-in-biology) we made last December, at the CASP14 conference, when DeepMind unveiled a radical new version of our AlphaFold system, which was recognised by the organisers of the assessment as a solution to the 50-year old grand challenge to understand the 3D structure of proteins. Determining protein structures experimentally is a time-consuming and painstaking pursuit, but AlphaFold demonstrated that AI could accurately predict the shape of a protein, at scale and in minutes, down to atomic accuracy. At [CASP](https://predictioncenter.org/casp14/index.cgi), we pledged to share our methods and provide broad access to this body of knowledge.

![A bar graph shows the median free-modelling accuracy for CASP7, CASP8, CASP9, CASP10, CASP11, CASP12, CASP13 (AlphaFold) and CASP14 (AlphaFold 2). From CASP7 to CASP12, the GDT_TS is measured under 45. CASP13 is in the 50s, CASP14 is in the high 80s.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6227ad7f559b3d69b9a59624_Accuracy.svg)

Improvements in the median accuracy of predictions in the free modelling category for the best team in each CASP, measured as best-of-5 GDT.

This month, we’ve finished the enormous amount of hard work to deliver on that commitment. We published two peer-reviewed papers in Nature ([1](https://www.nature.com/articles/s41586-021-03819-2),[2](https://www.nature.com/articles/s41586-021-03828-1)) and [open-sourced AlphaFold’s code](https://github.com/deepmind/alphafold/). Today, in partnership with [EMBL-EBI](https://www.ebi.ac.uk/), we’re incredibly proud to be launching the [AlphaFold Protein Structure Database](http://alphafold.ebi.ac.uk/%20), which offers the most complete and accurate picture of the human proteome to date, more than doubling humanity’s accumulated knowledge of high-accuracy human protein structures.

![](https://lh3.googleusercontent.com/8CkXEzMIbwTRogjhcaZKNxh3o_bbix1H7EvI-fYo1vm0CpHruGkPXXAZM0NEidK7mjI1pz42OozVXBxyEWp_WqIYpAhLkHnvkmG-u0uUY4O8COVrW_4=w1440-h810-n-nu)

In addition to the human proteome (all the ~20,000 proteins expressed by the human genome), we’re providing open access to the proteomes of [20 other biologically-significant organisms](https://www.alphafold.ebi.ac.uk/download), totalling over 350,000 protein structures. Research into these organisms has been the subject of countless research papers and numerous major breakthroughs, and has resulted in a deeper understanding of life itself. In the coming months we plan to vastly expand the coverage **to almost every sequenced protein known to science** - over 100 million structures covering most of the [UniProt reference database](https://www.uniprot.org/help/uniref). It’s a veritable protein almanac of the world. And the system and database will periodically be updated as we continue to invest in future improvements to AlphaFold.

Most excitingly, in the hands of scientists around the world, this new protein almanac will enable and accelerate research that will advance our understanding of these building blocks of life. Already, through our early collaborations, we’ve seen promising signals from researchers using AlphaFold in their own work. For instance, the [Drugs for Neglected Diseases Initiative](https://dndi.org/) (DNDi) [has advanced their research into life-saving cures](https://www.wired.co.uk/article/deepmind-alphafold-protein-diseases) for diseases that disproportionately affect the poorer parts of the world, and the [Centre for Enzyme Innovation](https://www.port.ac.uk/research/research-centres-and-groups/centre-for-enzyme-innovation) at the University of Portsmouth (CEI) is using AlphaFold to help engineer faster enzymes for recycling some of our most polluting single-use plastics. For those scientists who rely on experimental protein structure determination, AlphaFold's predictions have helped accelerate their research. As another example, a team at the [University of Colorado Boulder](https://www.colorado.edu/) is finding promise in using AlphaFold predictions to study antibiotic resistance, while a group at the [University of California San Francisco](https://www.ucsf.edu/) has used them to [increase their understanding of SARS-CoV-2 biology](https://www.biorxiv.org/content/10.1101/2021.05.10.443524v1). And this is just the start of what we hope will be a revolution in structural bioinformatics. With AlphaFold out in the world, there is a treasure trove of data now waiting to be transformed into future advances.

> AlphaFold opens new research horizons, and it is inspiring to see powerful cutting-edge AI enabling work on diseases which are concentrated almost exclusively in impoverished populations.

Ben Perry

Discovery Open Innovation Leader, Drugs for Neglected Diseases Initiative (DNDi)

For the AlphaFold team at DeepMind, this work represents the culmination of five years of enormous effort, including having to creatively overcome many challenging setbacks, resulting in a host of new sophisticated algorithmic innovations that were all needed to finally crack the problem. It builds on the discoveries of generations of scientists, from the early pioneers of protein imaging and crystallography, to the thousands of prediction specialists and structural biologists who’ve spent years experimenting with proteins since. Our dream is that AlphaFold, by providing this foundational understanding, will aid countless more scientists in their work and open up completely new avenues of scientific discovery.

> What took us months and years to do, AlphaFold was able to do in a weekend.

Professor John McGeehan

Professor of Structural Biology and Director for the Centre, Centre for Enzyme Innovation (CEI) at the University of Portsmouth

At DeepMind, our thesis has always been that artificial intelligence can dramatically accelerate breakthroughs in many fields of science, and in turn advance humanity. We built [AlphaFold](https://deepmind.com/research/case-studies/alphafold) and the [AlphaFold Protein Structure Database](https://alphafold.ebi.ac.uk/) to support and elevate the efforts of scientists around the world in the important work they do. We believe AI has the potential to revolutionise how science is done in the 21st century, and we eagerly await the discoveries that AlphaFold might help the scientific community to unlock next.

To learn more, head over to Nature to read our peer-reviewed papers describing our [full method](https://www.nature.com/articles/s41586-021-03819-2), and the [human proteome](https://www.nature.com/articles/s41586-021-03828-1). You can read more about them in our [technical blog](https://deepmind.com/research/publications/enabling-high-accuracy-protein-structure-prediction-at-the-proteome-scale). If you want to explore our system, here’s the [open-source code to AlphaFold](https://github.com/deepmind/alphafold) and [Colab notebook](https://colab.sandbox.google.com/github/deepmind/alphafold/blob/main/notebooks/AlphaFold.ipynb) to run individual sequences. To explore our structures, EMBL-EBI, the world leader in biological data, is hosting them in [a searchable database](https://alphafold.ebi.ac.uk/) that is open and free to all.

We would love to hear your feedback and understand how AlphaFold has been useful in your research. Share your stories at [alphafold@deepmind.com](mailto:alphafold@deepmind.com).
