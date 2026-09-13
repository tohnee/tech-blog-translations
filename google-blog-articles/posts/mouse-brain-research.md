---
title: "Mouse brain research is helping us better understand human minds"
source: https://blog.google/innovation-and-ai/technology/research/mouse-brain-research/
site: google-blog
date: 2024-07-08
authors: Ari Marini
crawled: 2026-09-13
---

Google researchers recently unveiled the [largest, most detailed map of the human brain yet](https://blog.google/technology/research/google-ai-research-new-images-human-brain/). It described just 1 cubic millimeter of brain tissue — the size of half a grain of rice — but at high enough resolution to show individual neurons and their connections to each other, and required 1.4 *petabytes* of data to encode.

Although it’s only a tiny sliver of the brain, the map led to several surprising discoveries. “For example, we found some of the wires will wrap themselves into these giant knots,” Google Research Scientist Viren Jain says of the neurons. “We have no idea why — nobody's ever seen it before.”

Now, Viren and his team have got mice on the brain. And for good reason — these mammals may help solve mysteries about our minds that have eluded us since our beginnings. Mysteries like: How are memories stored and retrieved? How do we recognize objects and faces? Why do we need so much sleep? And what goes wrong in Alzheimer’s and other brain diseases?

“One reason we don’t have answers to these questions is that we don’t yet have the data we need in order to study the brain,” Viren says.

The human brain has about 86 billion neurons connected to each other by more than 100 trillion synapses that enable you to think, feel, move and interact with the world. By creating a map of these neural connections — known as a “connectome” — we can unlock new understanding about how our brains work, and why sometimes they don’t.

To build detailed maps at the synaptic level, researchers need to image the brain at nanometer resolution and work with massive amounts of data. It’s a significant technical challenge that requires continued innovation in imaging techniques, AI algorithms and data management tools. That’s why, 10 years ago, Google Research formed its [Connectomics team](https://research.google/teams/connectomics/).

Over the past decade, the team has developed technologies to [more efficiently process, analyze and share data](https://sites.research.google/neural-mapping/), enabling researchers to dramatically scale up progress on understanding the brain. For example, they introduced [flood-filling networks](https://research.google/blog/improving-connectomics-by-an-order-of-magnitude/), which replaced the manual effort of coloring in cells across brain images by using machine learning to automatically trace the paths of neurons through layers of tissue. Building on this, their [SegCLR algorithm](https://research.google/blog/multi-layered-mapping-of-brain-tissue-via-segmentation-guided-contrastive-learning/) automatically identifies distinct parts of cells and cell types within these networks. And they created software such as [TensorStore](https://research.google/blog/tensorstore-for-high-performance-scalable-array-storage/) and [Neuroglancer](https://github.com/google/neuroglancer/) which helps store, process and visualize large multidimensional images and volumes.

Still, mapping the entire human brain connectome would require gathering and analyzing as much as a zettabyte of data (one billion terabytes), which is beyond the current capabilities of existing technologies. “If we were to map the whole human brain right now, it might take billions of dollars and hundreds of years,” Viren says.

Instead, researchers focus on either mapping large portions of the brains of small animals, or small pieces of brain tissue from large animals. In 2020, the Connectomics team mapped [half of a fruit fly’s brain](https://research.google/blog/releasing-the-drosophila-hemibrain-connectome-the-largest-synapse-resolution-map-of-brain-connectivity/), revealing the connections among 25,000 neurons. Through collaborations with researchers in the field, they’ve also created connectomes for portions of the brains of the [zebra finch](https://www.nature.com/articles/s41592-018-0049-4) and [zebrafish larvae](https://www.nature.com/articles/s41592-022-01621-0). And in May, the aforementioned map of [1 cubic millimeter of human brain tissue was published in *Science*](https://www.science.org/doi/10.1126/science.adk4858).

Thousands of researchers around the world have used the datasets from these projects, resulting in hundreds of published discoveries.

Researchers built a 3D image of nearly every neuron and their connections within a small piece of human brain tissue. The top image shows excitatory neurons and the bottom image shows inhibitory neurons.

![The top image shows all the excitatory neurons in a piece of human brain tissue lit up in yellow, while the bottom image shows all the inhibitory neurons in the same sample lit up in blue.](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/3D_neuron_and_connection_stills.width-1200.format-webp.webp)

Now, the Connectomics team is working with partners at Harvard, Princeton and elsewhere to map the mouse’s hippocampus — the part of the brain responsible for encoding memories, attention and spatial navigation, and representing 2-3% of the entire mouse brain.

Without the time or technology to map the entire human brain, analyzing a mouse connectome is the next best thing. It’s small enough to be technically feasible and could potentially deliver insights relevant to our own minds. “When you look at a mouse brain in the electron microscope, it looks exactly like a human brain. It is, in fact, a miniature version of a human brain,” Jeff W. Lichtman, a professor of molecular and cellular biology at Harvard, says. That's why scientists frequently use mice to study human brain disorders.

Mice are just the latest connectome frontier; neuroscientists have been working for decades to map increasingly larger and more complicated brains. The first connectome was for a worm’s brain — published in 1986, it took 16 years to map.

Connectomics across the decades.

![A diagram showing a table of different connectomics projects, with a roundworm at the top with 302 neurons requiring terabytes of storage, accomplished in the 1970s. The table grows in scale as it goes down to fruit fly, human brain fragments, mouse hippocampus, mouse and finally a whole human brain. The human brain,the number of neurons has dramatically increased to 100,000,000,000, which would need hundreds of exabytes to store.](https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/Brain_in-line_2.gif)

Even though a mouse brain is 1,000 times smaller than a human brain, mapping one is still an immense technical challenge. The dataset from one mouse brain connectome at nanometer resolution could be the largest biological dataset ever collected, estimated at about 20,000-30,000 terabytes.

“So not just acquiring the data, but even just storing and accurately processing all that data is a major challenge,” Viren says. “But that’s been our unique contribution to the field: developing tools that push the state of the art in accuracy and then really applying them at scale to larger and larger datasets.”

If successful, the Connectomics team's mouse brain project will be the first time scientists have mapped part of a mammalian hippocampus. It’s also the largest-ever chunk of any brain researchers have attempted to map.

“Fundamental research generates extraordinary value,” Viren says. “What gets me excited is that one day, we’ll have a precise understanding of how we form memories and what underlies mental disorders or diseases. But in order to do that, we have to create this loop of technology that would have been unimaginable as recently as two decades ago.”
