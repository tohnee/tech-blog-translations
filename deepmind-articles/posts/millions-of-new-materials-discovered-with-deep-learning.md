---
title: "Millions of new materials discovered with deep learning"
source: https://deepmind.google/blog/millions-of-new-materials-discovered-with-deep-learning/
site: deepmind
date: 2023-11-29
authors: Amil Merchant, Ekin Dogus Cubuk
crawled: 2026-09-13
---

AI tool GNoME finds 2.2 million new crystals, including 380,000 stable materials that could power future technologies

Modern technologies from computer chips and batteries to solar panels rely on inorganic crystals. To enable new technologies, crystals must be stable otherwise they can decompose, and behind each new, stable crystal can be months of painstaking experimentation.

Today, in a [paper published in Nature](https://www.nature.com/articles/s41586-023-06735-9), we share the discovery of 2.2 million new crystals – equivalent to nearly 800 years’ worth of knowledge. We introduce Graph Networks for Materials Exploration (GNoME), our new deep learning tool that dramatically increases the speed and efficiency of discovery by predicting the stability of new materials.

With GNoME, we’ve multiplied the number of technologically viable materials known to humanity. Of its 2.2 million predictions, 380,000 are the most stable, making them promising candidates for experimental synthesis. Among these candidates are materials that have the potential to develop future transformative technologies ranging from superconductors, powering supercomputers, and next-generation batteries to boost the efficiency of electric vehicles.

GNoME shows the potential of using AI to discover and develop new materials at scale. External researchers in labs around the world have independently created 736 of these new structures experimentally in concurrent work. In partnership with Google DeepMind, a team of researchers at the Lawrence Berkeley National Laboratory has also published [a second paper in Nature](https://www.nature.com/articles/s41586-023-06734-w) that shows how our AI predictions can be leveraged for autonomous material synthesis.

We’ve made [GNoME’s predictions available](https://www.nature.com/articles/s41586-023-06735-9) to the research community. We will be contributing 380,000 materials that we predict to be stable to the Materials Project, which is now processing the compounds and adding them into [its online database](https://next-gen.materialsproject.org/). We hope these resources will drive forward research into inorganic crystals, and unlock the promise of machine learning tools as guides for experimentation

## Accelerating materials discovery with AI

![A concentric circle diagram illustrating the scale of crystal material discoveries. The smallest, darkest blue circle representing "Human experimentation" accounts for 20,000 discoveries. It is nested within a medium blue circle for "Computational methods" at 48,000 discoveries, which is in turn nested within a massive light blue circle representing "GNoME" with 421,000 discoveries, highlighting the dramatic scale of AI-driven material discovery.](https://lh3.googleusercontent.com/eQQaMwaeVZIZ6W3FXvY4Fq9xdFvA2s5z94cSv74_GF8Ctdyn0Xtq5vOXBpuGNhx_PgmsmHz266aYV3KiAJCYxKxR2FbTyF-PwlJTY5fLweVHCWr15w=w1440)

About 20,000 of the crystals experimentally identified in the ICSD database are computationally stable. Computational approaches drawing from the Materials Project, Open Quantum Materials Database and WBM database boosted this number to 48,000 stable crystals. GNoME expands the number of stable materials known to humanity to 421,000.

In the past, scientists searched for novel crystal structures by tweaking known crystals or experimenting with new combinations of elements - an expensive, trial-and-error process that could take months to deliver even limited results. Over the last decade, computational approaches led by [the Materials Project](https://materialsproject.org/) and other groups have helped discover 28,000 new materials. But up until now, new AI-guided approaches hit a fundamental limit in their ability to accurately predict materials that could be experimentally viable. GNoME’s discovery of 2.2 million materials would be equivalent to about 800 years’ worth of knowledge and demonstrates an unprecedented scale and level of accuracy in predictions.

For example, 52,000 new layered compounds similar to graphene that have the potential to revolutionize electronics with the development of superconductors. Previously, about [1,000 such materials had been identified](https://pubmed.ncbi.nlm.nih.gov/28191965/). We also found 528 potential lithium ion conductors, 25 times more than a [previous study](https://pubs.rsc.org/en/content/articlelanding/2017/ee/c6ee02697d), which could be used to improve the performance of rechargeable batteries.

We are releasing the predicted structures for 380,000 materials that have the highest chance of successfully being made in the lab and being used in viable applications. For a material to be considered stable, it must not decompose into similar compositions with lower energy. For example, carbon in a graphene-like structure is stable compared to carbon in diamonds. Mathematically, these materials lie on the convex hull. This project discovered 2.2 million new crystals that are stable by current scientific standards and lie below the convex hull of previous discoveries. Of these, 380,000 are considered the most stable, and lie on the “final” convex hull – the new standard we have set for materials stability.

## GNoME: Harnessing graph networks for materials exploration

![Flowchart showing the active learning loop of GNoME, divided into a "Structural pipeline" and a "Compositional pipeline." Both pipelines generate candidates, represent them as graphs, and use a GNN to predict stability. These predictions are verified via DFT, added to the GNoME Database, and used to output "Energy models," "2.2 Million stable" materials, and "Interatomic potentials," with data fed back for subsequent rounds of learning.](https://lh3.googleusercontent.com/xdW-P8-xOUqjCJdtuZQcsdhLfNYcjOjSckg97qWuOeAflq0QJR_fUlv5gPIy7BDtwdKwtSFiY3TKfvDJs5Ka54Xne5GnSNXUmeoif8X5k8l4wdf9SZU=w1440)

GNoME uses two pipelines to discover low-energy (stable) materials. The structural pipeline creates candidates with structures similar to known crystals, while the compositional pipeline follows a more randomized approach based on chemical formulas. The outputs of both pipelines are evaluated using established Density Functional Theory calculations and those results are added to the GNoME database, informing the next round of active learning.

GNoME is a state-of-the-art graph neural network (GNN) model. The input data for GNNs take the form of a graph that can be likened to connections between atoms, which makes GNNs particularly suited to discovering new crystalline materials.

GNoME was originally trained with data on crystal structures and their stability, openly available through [the Materials Project](https://next-gen.materialsproject.org/). We used GNoME to generate novel candidate crystals, and also to predict their stability. To assess our model’s predictive power during progressive training cycles, we repeatedly checked its performance using established computational techniques known as Density Functional Theory (DFT), used in physics, chemistry and materials science to understand structures of atoms, which is important to assess the stability of crystals.

We used a training process called ‘active learning’ that dramatically boosted GNoME’s performance. GNoME would generate predictions for the structures of novel, stable crystals, which were then tested using DFT. The resulting high-quality training data was then fed back into our model training.

Our research boosted the discovery rate of materials stability prediction from around 50%, to 80% - based on [MatBench Discovery](https://matbench-discovery.materialsproject.org/), an external benchmark set by previous state-of-the-art models. We also managed to scale up the efficiency of our model by improving the discovery rate from under 10% to over 80% - such efficiency increases could have significant impact on how much compute is required per discovery.

## AI ‘recipes’ for new materials

The GNoME project aims to drive down the cost of discovering new materials. External researchers have independently created 736 of GNoME’s new materials in the lab, demonstrating that our model’s predictions of stable crystals accurately reflect reality. We’ve released our database of newly discovered crystals to the research community. By giving scientists the full catalog of the promising ‘recipes’ for new candidate materials, we hope this helps them to test and potentially make the best ones.

![Six 3D molecular structures of predicted stable crystals, each labeled with its chemical formula: K2BiCl5, Li4MgGe2S7, Mo5GeB2, KV3Se3, Rb2HfSi3O9, and Tm5Pd9P7.](https://lh3.googleusercontent.com/nUYwTkQmJC-_e956cSIIx9umzvDb4cWcpjJQUa-ikFg-1-mAV8X7YkK0yMy8xLjN-NoTINjDC_t7LhXcT2rs14-0aawWc-6cCc3apj44fqWn4LI_LQ=w1440)

Upon completion of our latest discovery efforts, we searched the scientific literature and found 736 of our computational discoveries were independently realized by external teams across the globe. Above are six examples ranging from a first-of-its-kind Alkaline-Earth Diamond-Like optical material (Li4MgGe2S7) to a potential superconductor (Mo5GeB2).

Rapidly developing new technologies based on these crystals will depend on the ability to manufacture them. In a paper led by our collaborators at Berkeley Lab, researchers showed a robotic lab could rapidly make new materials with automated synthesis techniques. Using materials from the Materials Project and insights on stability from GNoME, the autonomous lab created new recipes for crystal structures and successfully synthesized more than 41 new materials, opening up new possibilities for AI-driven materials synthesis.

![An automated robotic arm operating inside a glass-enclosed synthesis laboratory setup, surrounded by trays of sample vials and chemical containers for materials discovery.](https://lh3.googleusercontent.com/n0q40AO2pID4Ke3smLEyZDzlXSsukFpl_pE1jX1kpnTTl4QPCg3vbSrZUui62TIL0L4YkpF7DV_J7mMFAehJOcXxOB0MAvJ8_bg4tdsha4PXxVkxxcA=w1440)

A-Lab, a facility at Berkeley Lab where artificial intelligence guides robots in making new materials. Photo credit: Marilyn Sargent/Berkeley Lab

## New materials for new technologies

To build a more sustainable future, we need new materials. GNoME has discovered 380,000 stable crystals that hold the potential to develop greener technologies – from better batteries for electric cars, to superconductors for more efficient computing.

Our research – and that of collaborators at the Berkeley Lab, Google Research, and teams around the world — shows the potential to use AI to guide materials discovery, experimentation, and synthesis. We hope that GNoME together with other AI tools can help revolutionize materials discovery today and shape the future of the field.

**Read our paper in Nature**

[Read our paper in Nature](https://www.nature.com/articles/s41586-023-06735-9)[Read the Berkeley Lab paper in Nature](https://www.nature.com/articles/s41586-023-06734-w)[Download the dataset](https://github.com/google-deepmind/materials_discovery)

**Acknowledgements**

This work would not have been possible without our amazing co-authors: Simon Batzner, Sam Schoenholz, Muratahan Aykol, and Gowoon Cheon. We would also like to acknowledge Doug Eck, Jascha Sohl-dickstein, Jeff Dean, Joëlle Barral, Jon Shlens, Pushmeet Kohli, and Zoubin Ghahramani for sponsoring the project; Lizzie Dorfman for Product Management support; Andrew Pierson for Program Management support; Ousmane Loum for help with computing resources; Luke Metz for his help with infrastructure; Ernesto Ocampo for help with early work on the AIRSS pipeline; Austin Sendek, Bilge Yildiz, Chi Chen, Chris Bartel, Gerbrand Ceder, Joy Sun, JP Holt, Kristin Persson, Lusann Yang, Matt Horton, and Michael Brenner for insightful discussions; and the Google DeepMind team for continuing support.
