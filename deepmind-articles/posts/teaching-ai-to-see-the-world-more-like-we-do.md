---
title: "Teaching AI to see the world more like we do"
source: https://deepmind.google/blog/teaching-ai-to-see-the-world-more-like-we-do/
site: deepmind
date: 2025-11-11
authors: Andrew Lampinen, Klaus Greff
crawled: 2026-09-13
---

Your browser does not support the audio element.

**Listen to article** 10 minutes

New research shows that reorganizing a model’s visual representations can make it more helpful, robust and reliable

“Visual” artificial intelligence (AI) is everywhere. We use it to sort our photos, identify unknown flowers and steer our cars. But these powerful systems do not always “see” the world as we do, and they sometimes behave in surprising ways. For example, an AI system that can identify hundreds of car manufacturers and models might still fail to capture the commonalities between a car and an airplane, *i.e.* both are large vehicles made primarily of metal.

To better understand these differences, today we’re publishing a [new paper in Nature](https://www.nature.com/articles/s41586-025-09631-6) analyzing the important ways AI systems organize the visual world differently from humans. We present a method for better aligning these systems with human knowledge, and show that addressing these discrepancies improves their robustness and ability to generalize.

This work is a step towards building more intuitive and trustworthy AI systems.

## Why AI struggles with the “odd one out”

When you see a cat, your brain creates a mental representation that captures everything about the cat, from basic concepts like its color and furriness to high-level concepts like its "cat-ness." AI vision models also produce representations, by mapping images to points in a high-dimensional space where similar items (like two sheep) are placed close together, and different ones (a sheep and a cake) are far apart.

To understand the differences in how human and model representations are organized, we used the classic "odd-one-out" task from cognitive science, asking both humans and models to pick which of three given images does not fit in with the others. This test reveals which two items they "see" as most similar.

Sometimes, everyone agrees. Given a tapir, a sheep, and a birthday cake, both humans and models reliably pick the cake as the odd one out. Other times, the right answer is unclear, and people and models disagree.

Interestingly, we also found many cases where humans strongly agree on an answer, but the AI models get it wrong. For the third example below, most people agree the starfish is the odd one out. But most vision models focus more on superficial features like background color and texture, and choose the cat instead.

![Three rows of "odd-one-out" image triplets comparing human and AI classifications. The top row shows a tapir, sheep, and a birthday cake, labeled "Aligned" as both humans and AI select the cake. The middle row shows lemons, a red telephone booth, and a gazelle, labeled "Unclear" as human judgments vary. The bottom row shows a fox, a starfish, and a cat, labeled "Unaligned" because humans select the starfish as the odd one out, whereas the AI incorrectly selects the cat.](https://lh3.googleusercontent.com/qYpkuEX0oANy3iSQVsowLqlNrgEOxhbtcTwe23fKWQyqURoZruzejU_gUvbZDInicRi7VbvbjX5yh3pXclLyEOD38QCAgrH2qm1jMKND16EteM-J6dM=w1440)

Three examples of the "odd one out" task. Three images of subjects in the natural world are shown in three rows. The first row shows an easy task where humans and models align. The second row shows an example where humans and AI models disagree. The third row shows an example where humans tend to agree, but models make a different choice.

This example illustrates a systematic misalignment between humans and AI, which we observed across many different vision models, from image classifiers to unsupervised models.

The overall problem can be seen in a two-dimensional projection (PCA) of an AI’s internal map.

Below, on the left, we show a vision model's internal map which appears unstructured, with representations for different categories like animals, food, and furniture all mixed together. The structure on the right is the improved representation map after we applied our alignment method where categories are clearly organized.

![Two scatter plots comparing the internal representation maps of an unaligned and aligned classifier. The "Unaligned classifier" plot on the left shows a highly mixed, chaotic jumble of colored data points representing different categories, with images of a buffalo, a spider, and grass clustered close together. The "Aligned classifier" plot on the right shows clearly segregated, distinct clusters of colors corresponding to categories like Food (green), Animal (blue), and Furniture (red), with the same three images spread far apart to reflect their conceptual differences.](https://lh3.googleusercontent.com/JeGjvW3BHrbEoNFaag8o4EEgOqesvS5NKVuqjc5cVpz6FTSRKbUFpPR2AiW5wjZcRFRCKcbO8JWCTWUO-S031cGWcBJ7HuygrsHDJ7kSthZuFH92zw=w1440)

Two maps showing a vision model’s representations of many different categories of objects. Before alignment (left) there is no visible organization. After alignment (right) the representations are meaningfully organized by category.

## A multi-step alignment method

Cognitive scientists have collected the [THINGS](https://things-initiative.org/) dataset containing millions of human odd-one-out judgements, which we could have used to help solve the visual alignment problem. Unfortunately, this dataset only uses a few thousand images — not enough information to directly fine tune powerful vision models, which immediately overfit on this small set of images and forget many of their prior skills.

To address this, we proposed a three-step method:

1. We started with a powerful pretrained vision model (SigLIP-SO400M) and carefully trained a small adapter on top of it, using the THINGS dataset. By freezing the main model and carefully regularizing the adapter training, we created a teacher model that doesn’t forget its prior training.
2. This teacher model then acts as a stand-in for human-like judgments, which we used to generate a massive new dataset, called [AligNet](https://github.com/google-deepmind/alignet?tab=readme-ov-file#alignet-dataset), of millions of human-like odd-one-out decisions using a million different images — far more than we could collect from real people.
3. Finally, we used this new dataset to fine tune other AI models (the "students"). Because of the diversity of our dataset, overfitting is no longer an issue and the students can be trained fully and can more deeply restructure their internal maps.

As shown in the diagram below, the student’s representations change from an unstructured jumble to a clearly-structured organization where high-level concepts such as animals (blue) and food items (green) are separated from other types of objects.

![A three-step flow diagram illustrating the alignment method: 1) training a teacher model on the THINGS dataset using a linear adapter; 2) using the teacher model to generate a large triplet-similarity dataset (AligNet) from ImageNet; and 3) distilling these bootstrapped similarities into a student model.](https://lh3.googleusercontent.com/vrR1IgBevAiwEmZOT5I-myaPoKaW7sSwTmkPRpaovn0h64lLfn7SchZJ4sGyxIn7DRplbGf7wqFcVXr_9hDKmfV9z0zWhC025qHbFoJVjP9aOORMpw=w1440)

Diagram of our three-step model-alignment method.

Human knowledge is organized according to different levels of similarity. When we align models with human knowledge, the model’s representations change according to these levels of similarity. This reorganization follows the hierarchical structure of human knowledge known from cognitive science.

During alignment, we see that representations move apart or together in proportion to their ”conceptual distance” in the human-category hierarchy. For example, two dogs (same subordinate category) will move closer together (decrease in distance), while an owl and a truck (different superordinate categories) will move further apart (increase in distance).

![A line graph on the left plotting density against change in relative distance for four category levels. A diagram on the right displays these categories in a hierarchy: "Different superordinate" (yellow, comparing a truck and an owl), "Same superordinate" (red, comparing an owl and a poodle), "Same basic" (purple, comparing a poodle and a golden retriever), and "Same subordinate" (black, comparing two golden retrievers). The corresponding colored curves on the graph show that during alignment, items in closer categories (black and purple) decrease in distance (shifting left), while items in different superordinate categories (yellow) increase in distance (shifting right).](https://lh3.googleusercontent.com/Pc9gCB67xt6YI0xKqWuxsaKotVNfI_QfvUXxSVW17sFFcUDYJWV0-rzFAuhcPemINu3G3KKUkvNVLJaUlPUoQpCoX7sw6r0AEvFYmuK59PRym2Tq=w1440)

A line graph shows the change in relative distances between human and AI representations. The representations of very similar categories tend to get closer together, while representations of less similar pairs of objects tend to move further apart.

We can conclude that our method organizes the representational map of the AI student according to human conceptual hierarchies, without being explicitly supervised to do so.

## Testing our aligned models

We tested our aligned models on many cognitive science tasks — including tasks like multi-arrangement, arranging many images by their similarity — and a new odd-one-out dataset, called [Levels](https://doi.gin.g-node.org/10.12751/g-node.hg4tdz/), that we collected. In every case, our aligned models showed dramatically improved human-alignment, agreeing substantially more often with human judgments across a range of visual tasks.

Our models even learned a form of ‘human-like’ uncertainty. In testing, model-decision-uncertainty strongly correlated with how long it took humans to make a choice – a common proxy measure for uncertainty.

We also found that making models more human-aligned also makes them better vision models overall. Our aligned models performed much better at various challenging tasks, such as learning a new category from a single image (“few-shot learning”), or making reliable decisions, even when the type of images being tested changed (the “distribution shift”).

![A bar graph titled "Human alignment" comparing the performance accuracy of the original model (light gray) against the AligNet aligned model (blue) on cognitive science tasks. On "Triplet odd-one-out" tasks, AligNet shows significantly higher accuracy than the original model across two trials, and on "Multi-arrangement" tasks, AligNet's accuracy dramatically outperforms the original model.](https://lh3.googleusercontent.com/EuxuEhBLzvT2srQ3HQvltTxwBwZ0BiwQlW9cUEJu1ReDabAz3PdkjVTSI09J102zjQBsg6kjS8PG0Tp-551477JzVpzjgNEaZ5onJWTaPH9UktgN_nE=w1440-h810-n-nu)

![A bar graph titled "Generalisation" comparing the performance accuracy of the original model (light gray) against the AligNet aligned model (blue) on AI tasks. Across both Few-shot learning and Distribution shift tasks, the AligNet model consistently and significantly outperforms the original model.](https://lh3.googleusercontent.com/UvkD3RRITqF906Y5QqwVHxResI3wu5YNKGsprbeVfMxg6lTHOmwZU8Bh10eJpjAUQBpZ3mVWWKR9-dsGDdcYwaqPK8YoxqtNTVmC7i-HrqizK2Mp=w1440-h810-n-nu)

Two bar graphs showing that our aligned models (dark blue) outperform the original ones (light gray) at cognitive science tasks involving odd-one-out and multi-arrangement (top) and AI tasks involving few-shot learning and distribution shift (bottom).

## Toward more human-aligned, reliable models

Many existing vision models fail to capture the higher-level structure of human knowledge. This research presents a possible method for addressing this issue, and shows that models can be aligned better with human judgments and perform more reliably on various standard AI tasks.

While more alignment work remains to be done, our work illustrates a step towards more robust and reliable AI systems.

Learn more about our work

[Read our paper](https://www.nature.com/articles/s41586-025-09631-6)[Build on the open-source implementation](https://github.com/google-deepmind/alignet)[Evaluate models on the Levels dataset](https://doi.gin.g-node.org/10.12751/g-node.hg4tdz/)

## Acknowledgements

We’d like to thank the paper’s lead author Lukas Muttenthaler, and our collaborators Frieda Born, Bernhard Spitzer, Simon Kornblith, Michael C. Mozer, Klaus-Robert Müller and Thomas Unterthiner.
