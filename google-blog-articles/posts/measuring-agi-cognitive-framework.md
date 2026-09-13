---
title: "Measuring progress toward AGI: A cognitive framework"
source: https://blog.google/innovation-and-ai/models-and-research/google-deepmind/measuring-agi-cognitive-framework/
site: google-blog
date: 2026-03-17
authors: Ryan Burnell
crawled: 2026-09-13
---

Artificial General Intelligence (AGI) has the potential to accelerate scientific discovery and help solve some of humanity’s most pressing problems. But it can be difficult to know how close we are to this key milestone, because there’s a lack of empirical tools for evaluating systems’ general intelligence. Tracking progress toward AGI will require a wide range of methods and approaches, and we believe cognitive science provides one important piece of the puzzle.

That’s why today, we’re releasing a new paper, “[Measuring Progress Toward AGI: A Cognitive Taxonomy](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/measuring-progress-toward-agi/measuring-progress-toward-agi-a-cognitive-framework.pdf),” that presents a scientific foundation for understanding the cognitive capabilities of AI systems.

Alongside the paper, we are partnering with [Kaggle to launch a hackathon](http://kaggle.com/competitions/kaggle-measuring-agi), inviting the research community to help build the evaluations needed to put this framework into practice.

## Deconstructing general intelligence

Our framework draws on decades of research from psychology, neuroscience and cognitive science to develop a cognitive taxonomy. It identifies 10 key cognitive abilities that we hypothesize will be important for general intelligence in AI systems:

1. **Perception**: extracting and processing sensory information from the environment
2. **Generation**: producing outputs such as text, speech and actions
3. **Attention**: focusing cognitive resources on what matters
4. **Learning**: acquiring new knowledge through experience and instruction
5. **Memory**: storing and retrieving information over time
6. **Reasoning**: drawing valid conclusions through logical inference
7. **Metacognition**: knowledge and monitoring of one's own cognitive processes
8. **Executive functions**: planning, inhibition and cognitive flexibility
9. **Problem solving**: finding effective solutions to domain-specific problems
10. **Social cognition**: processing and interpreting social information and responding appropriately in social situations

![Bubbles all connecting to the central bubble "Cognitive faculties". Each bubble list a cognitive faculty.](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/agi_cognition_framework_blog_inl.width-1200.format-webp.webp)

To understand AI capabilities across these cognitive abilities, we propose a three-stage evaluation protocol that benchmarks system performance in relation to human capabilities:

1. Evaluate AI systems across a broad suite of cognitive tasks covering each ability, using held-out test sets to prevent data contamination
2. Collect human baselines for the same tasks from a demographically representative sample of adults
3. Map each AI system’s performance relative to the distribution of human performance in each ability

## Going from theory to practice

Defining these cognitive abilities is a crucial first step, but we need more than a framework to measure progress. To put this theory into practice, we are launching a new Kaggle hackathon — “[Measuring progress toward AGI: Cognitive abilities](http://kaggle.com/competitions/kaggle-measuring-agi)”. The hackathon encourages the community to design evaluations for five cognitive abilities where the evaluation gap is the largest: learning, metacognition, attention, executive functions and social cognition.

Participants can use Kaggle's newly launched [Community Benchmarks](https://blog.google/innovation-and-ai/technology/developers-tools/kaggle-community-benchmarks/) platform to build and test their evaluations against a lineup of frontier models.

We are offering a total prize pool of $200,000: $10,000 awards for the top two submissions in each of the five tracks, and $25,000 grand prizes for the four absolute best overall submissions. Submissions are open March 17 through April 16, and we’ll announce the results June 1. Head over to the [Kaggle website](http://kaggle.com/competitions/kaggle-measuring-agi) to start building.
