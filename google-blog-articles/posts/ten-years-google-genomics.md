---
title: "10 years of genomics research at Google"
source: https://blog.google/innovation-and-ai/technology/research/ten-years-google-genomics/
site: google-blog
date: 2025-10-16
authors: Katherine Chou
crawled: 2026-09-13
---

*Last updated: October 24, 2025*

For decades, scientists have been working to understand the genome, the operating manual for all of life on Earth. This manual lives in unending variations inside the DNA in each organism and affects everything from an organism's development to the rules of life more broadly, and yet it is one of the least understood aspects of biology.

Our journey into developing technologies for geneticists to study the genome of billions of humans, plants and animals began 10 years ago. A small team of researchers at Google decided to apply deep learning to various genome sequencing challenges, making it faster, more accurate and more efficient. What began in 2015 as a foundational research effort has now evolved into a global initiative, including partnerships with scientists and institutions across the globe to accelerate scientific discovery, advance healthcare and preserve biodiversity.

This work is already showing promising breakthroughs on behalf of human health — including today’s [announcement of DeepSomatic](https://blog.google/technology/research/deepsomatic-an-open-source-ai-model-is-speeding-up-genetic-analysis-for-cancer-research/), a new tool to identify cancer variants with more accuracy. But our work is not yet done, and more tools are coming. Today, we're taking a moment to look back at some of the key milestones and groundbreaking tools from our first 10 years in genomics, powered by AI.

> Reading the genome

AI has proven instrumental in overcoming the most fundamental challenge in genomics: reading the code of life accurately and efficiently.

- **2015 - Research begins:** Google applied cutting-edge deep learning techniques to the field of genomics for the first time, winning the 2016 PrecisionFDA Truth Challenge and kicking off a decade of exploration into the field.
- **2018 - Accurate identification of genetic variations:** We openly released our state-of-the-art variant caller, [DeepVariant](https://www.nature.com/articles/nbt.4235). This deep learning-based tool accurately identifies genetic variants in DNA sequencing data and has become widely used, directly contributing to landmark milestones like the first truly complete human genome sequence.
- **2022 - More accurate genetic sequencing:** We introduced [DeepConsensus](https://www.nature.com/articles/s41587-022-01435-7), a deep learning model that improves the accuracy of long-read sequencing data and reduces errors in raw genomic data. This has since allowed for a 250% increase in the throughput of the highest-quality sequence reads for researchers.
- **2022 - Completing the human genome**: The [NIH Telomere-to-Telomere (T2T) consortium](https://sites.google.com/corp/ucsc.edu/t2tworkinggroup) produces the first complete [human reference genome](https://www.science.org/doi/10.1126/science.abj6987) to decode the final 8% of the human genome, filling in the last missing pieces of our genetic blueprint to make a resource for researchers everywhere. This effort uses a special application of DeepVariant to polish the assembled sequence.
- **2023 - The human pangenome reference:** Engineers used DeepConsensus and DeepVariant to help create the [first draft of the human pangenome](https://www.nature.com/articles/s41586-023-05896-x). This new reference genome includes sequences from multiple individuals of diverse ancestries, a critical step toward ensuring that all people benefit from genomic medicine.
- **2025 - More accurate gene assemblies**: We introduced [DeepPolisher](https://research.google/blog/highly-accurate-genome-polishing-with-deeppolisher-enhancing-the-foundation-of-genomic-research/), a deep learning tool that enhances the accuracy of genome assemblies for human, animal and plant genomes, improving the quality of reference genomes used in research.

> Understanding the genome

Once the genome can be read accurately, the next challenge is creating a more comprehensive understanding of what function specific parts of the sequence encode and identifying which tiny variations cause disease.

- **2021 - Predicting gene expression**: [Enformer](https://www.nature.com/articles/s41592-021-01252-x), a model that predicts gene expression from a genome sequence, was released to better understand non-coding genetic variants and design cell type specific DNA sequences, advancing basic biological understanding.
- **2023 - Assessing the disease-causing potential of coding genetic variants:** We developed [AlphaMissense](https://www.science.org/doi/10.1126/science.adg7492), a model that predicts which genetic variants in the protein-coding regions of the genome are more likely to cause disease, providing a powerful new tool for geneticists.
- **2025 - Unifying model of non-coding variant effects**: Our new AI model, [AlphaGenome](https://deepmind.google/discover/blog/alphagenome-ai-for-better-understanding-the-genome/), predicts how single DNA variants affect biological processes, helping researchers understand the "dark matter" of the genome.

![Bright blue 3D rendering of a DNA double helix centered against a background of blurred, faint DNA strands and a gradient of pink and blue light.](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/AlphaGenoma-OG-1200-630-000000.width-1200.format-webp.webp)

> Accelerating discovery for people and the planet

Our AI tools are helping researchers solve major biological grand challenges, leading to breakthroughs in health and enabling conservation efforts for endangered species.

- **2021 - Phenotyping eye diseases:** Our approach to [training AI on large-scale biobank data](https://www.cell.com/ajhg/fulltext/S0002-9297(21)00188-9) of retinal images and genomics led to the discovery of new genetic links to eye diseases, identifying potential targets for drug development against conditions like glaucoma.
- **2022 - Record-breaking genetic diagnosis:** A [collaboration led by Stanford Medicine](https://med.stanford.edu/news/all-news/2022/01/dna-sequencing-technique.html) set a Guinness World Record for the fastest genetic diagnosis, identifying a disease-causing variant in under 8 hours with Google’s AI.
- **2023 - Sequencing DNA for conservation:** Google provides technical and computational support for an ambitious initiative to sequence all eukaryotic life. Our collaboration has already aided genome projects for 17 critically endangered species, showcasing AI's role in conservation.
- **2024 - AI for common health measures:** Google developed AI methods that use common medical tests to discover how our genes contribute to heart and lung diseases. Our methods [improve disease prediction and genetic discovery](https://www.nature.com/articles/s41588-024-01831-6) by better understanding how genetics influences the body's fundamental processes.
- **2025 - Identifying variants in cancer cells**: We developed an AI model, [DeepSomatic](https://research.google/blog/using-ai-to-identify-genetic-variants-in-tumors-with-deepsomatic), that more accurately identifies cancer-related genetic mutations. When tested on multiple cancer types, our method identified key variants missed by prior state-of-the-art tools, offering the potential to improve cancer diagnosis and treatment.

![Glowing blue and purple digital neural network illustration, featuring interconnected neuron-like cells on a black background.](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/DeepSomatic_Hero.width-1200.format-webp.webp)

The advancement of genomics over the past decade comes down to our approach to creating an innovation flywheel: we are driven by a real-world problem, like understanding the human genome to deliver better healthcare, to conduct fundamental computer science research. That research leads to a solution, which in turn empowers us to uncover even more interesting problems to solve, such as applying this work to the preservation of our planet’s species and protection of biodiversity.

After a decade of driving breakthrough discoveries from research to reality for advancing genetics, there is now an extraordinary research community that collaborates on this powerful suite of scientific tools to improve the lives of every being on this planet.

We can't wait to see what the next 10 years of research together will bring.
