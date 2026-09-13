---
title: "How we built one of the most ambitious datasets in brain activity research"
source: https://blog.google/innovation-and-ai/technology/research/zapbench-zebrafish-brain-mapping/
site: google-blog
date: 2025-06-09
authors: Chaim Gartenberg
crawled: 2026-09-13
---

For almost a decade, Michał Januszewski has been thinking about what fish are thinking about.

Michał is part of Google Research, which has been working with collaborators at HHMI Janelia and Harvard University to build one of the most [ambitious datasets in brain activity research](https://research.google/blog/improving-brain-models-with-zapbench/) yet: a dataset that tracks both the neural activity and nanoscale structure of an entire brain of single larval zebrafish — which could lead to major breakthroughs for how we understand our own brains.

“For years, our team has been really focusing on what’s called connectomics, which deals with the [structural mapping of brains](https://blog.google/technology/research/mouse-brain-research/) — we take very high-resolution pictures of small fragments of brains and try to identify all cells and all the connections between them,” Michał says. “That gives you a static snapshot of the brain as it is at any given moment in time, but doesn’t tell you what the brain is doing when it's actually alive and thinking.”

So Michał's team looked to build a new, multimodal dataset that could predict and show neural activity of an organism as it thinks. They chose to start with the zebrafish, which checked several key boxes: It is a vertebrate animal, with more complex brain functions than, say, an insect, and its brain is small enough that the team could get a dataset of the entire brain, instead of just a tiny portion of it.

And — perhaps most importantly — newly hatched zebrafish are almost entirely transparent, allowing the team to use a specialized laser rig to scan nearly two hours of brain activity for more than 70,000 neurons in a live fish’s brain as it reacts to various patterns and stimuli being projected around it.

In April, Google Research [released that data](https://blog.google/technology/research/zapbench-zebrafish-brains/) as a first-of-its-kind benchmark, called [ZAPBench](https://github.com/google-research/zapbench) (Zebrafish Activity Prediction Benchmark), which can help advance neuroscience by enabling the development of more accurate AI models that can predict brain activity.

Researchers used a light sheet microscope to record brain activity in a larval zebrafish.

![Zebrafish in a bowl, illuminated by a blue light, surrounded by three microscope lenses](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/ZAPBench_Diagram.width-1200.format-webp.webp)

Researchers at Google have created plenty of AI model benchmarks to drive improvements for models in other fields, like [WeatherBench 2](https://sites.research.google/weatherbench/) for improving forecasts, or the [One Billion Word Benchmark](https://research.google/pubs/one-billion-word-benchmark-for-measuring-progress-in-statistical-language-modeling/) for language models. ZAPBench, however, fills a unique need. While it can be easy to double check the accuracy of something like a weather prediction from an AI model by, say, sticking your head out a window, there’s no simple way to test predictive models for brain activity, due to the difficulty in obtaining scan data in the first place.

“Neuroscience researchers have been building models for how the brain works, but it's been relatively rare to be able to put them to the test for how well they can actually predict brain activity,” says Research Scientist Viren Jain. ”With ZAPBench, anybody can create models and evaluate them, both against the benchmark and other models.” The team at Google has already seen some interesting results in their own tests, including how models tended to make mistakes in predictions in specific areas of the brain, but were more accurate at predicting activity in others.

The originally recorded brain activity data (left), and a predicted brain activity image that ZAPBench is able to help benchmark (right).

Creating ZAPBench is just the first step. The Google Research team is also building on its existing work to map the connectome of the tens of thousands of neurons of the exact same larval zebrafish brain whose activity was imaged. The hope is that by pairing the connectome of the specific specimen’s brain together with the activity of that brain, we’ll be able to find new insights into how brains work on a basic level — both for fish, and one day, even for humans.

“The long-term goal here is to figure out how the brain operates at a really mechanistic level,” Viren says. “And if we can develop a model that’s better at predicting how all these different components drive brain activity, it’ll significantly advance the state of and our confidence in basic models of how the brain works — which could drive applications in medicine, brain computer interfaces or any number of helpful applications in the future.”
