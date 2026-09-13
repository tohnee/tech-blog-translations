---
title: "Learning to navigate in cities without a map"
source: https://deepmind.google/blog/learning-to-navigate-in-cities-without-a-map/
site: deepmind
date: 2018-03-29
authors: Piotr Mirowski, Raia Hadsell, Andrew Zisserman
crawled: 2026-09-13
---

How did you learn to navigate the neighborhood of your childhood, to go to a friend’s house, to your school or to the grocery store? Probably without a map and simply by remembering the visual appearance of streets and turns along the way. As you gradually explored your neighborhood, you grew more confident, mastered your whereabouts and learned new and increasingly complex paths. You may have gotten briefly lost, but found your way again thanks to landmarks, or perhaps even by looking to the sun for an impromptu compass.

Navigation is an important cognitive task that enables humans and animals to traverse, without maps, over long distances in a complex world. Such long-range navigation can simultaneously support self-localisation (“I am here”) and a representation of the goal (“I am going there”).

In [Learning to Navigate in Cities Without a Map](https://arxiv.org/abs/1804.00168), we present an interactive navigation environment that uses first-person perspective photographs from [Google Street View](https://en.wikipedia.org/wiki/Google_Street_View), approved for use by the StreetLearn project and academic research, and gamify that environment to train an AI. As standard with Street View images, faces and license plates have been blurred and are unrecognisable. We build a neural network-based artificial agent that learns to navigate multiple cities using visual information (pixels from a Street View image). Note that this research is about navigation in general rather than driving; we did not use traffic information nor try to model vehicle control.

![Three side-by-side Google Street View panoramas showing diverse urban environments used for AI navigation training: Times Square in New York City with yellow cabs and billboards, Bethesda Terrace in Central Park with lush greenery, and St. Paul's Cathedral in London with iconic red double-decker buses.](https://lh3.googleusercontent.com/po6lqhaBy-0k3SBx2lTBKMqJ2hkfyCFgbNwmpl5zSBEpMj0Ji6U9mntN0x0OxnBvUM62rYmRzMJFjGA3_aPo5hH-SvkRAN6JSff3lWTdRGvVanVtSg=w1440)

Our agent navigates in visually diverse environments, without having access to the map of the environment.

The agent is rewarded when it reaches a target destination (specified, for instance, as pair of latitude and longitude coordinates), like a courier tasked with an endless set of deliveries but without a map. Over time, the AI agent learns to cross entire cities in this way. We also demonstrate that our agent can learn the task in multiple cities, and then robustly adapt to a new city.

![An animated GIF demonstrating the AI agent's first-person perspective navigation through Google Street View in Paris, with an inset aerial map overlay showing its real-time path and position tracking.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/622681de9a678443ffbca1e1_Stop20Motion.gif)

Stop-motion films of agent trained in Paris. The images are superposed with a map of the city, showing the goal location (in red) and the agent location and field of view (in green). Note that the agent does not see the map, only the lat/lon coordinates of the goal location.

## Learning navigation without building maps

We depart from the traditional approaches which rely on explicit mapping and exploration (like a cartographer who tries to localise themselves and draw a map at the same time). Our approach, in contrast, is to learn to navigate as humans used to do, without maps, GPS localisation, or other aids, using only visual observations. We build a neural network agent that inputs images observed from the environment and predicts the next action it should take in that environment. We train it end-to-end using deep reinforcement learning, similarly to some recent work on [learning to navigate in complex 3D mazes](https://arxiv.org/pdf/1611.03673.pdf) and [reinforcement learning with unsupervised auxiliary tasks](https://arxiv.org/pdf/1611.05397.pdf) for playing games. Unlike those studies, which were conducted on small-scale simulated maze environments, we utilise city-scale real-world data, including complex intersections, footpaths, tunnels, and diverse topology across London, Paris, and New York City. Moreover, the approach we use support city-specific learning and optimisation as well as general, transferable navigation behaviours.

## Modular neural network architecture that can transfer to new cities

The neural network inside our agent consists of three parts: 1) a convolutional network that can process images and extract visual features, 2) a locale-specific recurrent neural network that is implicitly tasked with memorising the environment as well as learning a representation of “here” (current position of the agent) and of “there” (location of the goal) and 3) a locale-invariant recurrent network that produces the navigation policy over the agent’s actions. The locale-specific module is designed to be interchangeable and, as its name indicates, unique to each city where the agent navigates, whereas the vision module and the policy module can be locale-invariant.

![Diagram illustrating the modular neural network architectures: (a) single-city setup, (b) multi-city setup with three distinct locale-specific pathways, and (c) a transfer learning setup showing frozen modules in grey when adapting to a new city.](https://lh3.googleusercontent.com/o8vl9t-boK_7Hp9XPBA9LmUXjH9kZlhQGV3LlfxR3_c2Jy1q2tRpF-BgDjnAwyHMIUjoMloL1dzQzSo3gEmoDcGkg6XZo3vsOrf607MPBEgCsM8n-Q=w1440)

Comparison of the CityNav architecture (a), MultiCityNav architecture with a locale-specific pathway for each city (b) and illustration of the training and transfer procedure when adapting the agent to a new city (c).

Just as in the Google Street View interface, the agent can rotate in place or move forward to the next panorama, when possible. Unlike the Google Maps and Street View environment, the agent does not see the little arrows, the local or global map, or the famous Pegman: it needs to learn to differentiate open roads from sidewalks. The target destinations may be kilometres away in the real world and require the agent to step through hundreds of panoramas to reach them.

We demonstrate that our proposed method can provide a mechanism for transferring knowledge to new cities. As with humans, when our agent visits a new city, we would expect it to have to learn a new set of landmarks, but not to have to re-learn its visual representations or its behaviours (e.g., zooming forward along streets or turning at intersections). Therefore, using the MultiCity architecture, we train first on a number of cities, then we freeze both the policy network and the visual convolutional network and only a new locale-specific pathway on a new city. This approach enables the agent to acquire new knowledge without forgetting what it has already learned, similarly to the [progressive neural networks](https://arxiv.org/pdf/1606.04671.pdf?)architecture.

![An image showing the five areas of Manhattan used in this study: Lower Manhattan, Greenwich Village, Midtown, Central Park and Harlem.](https://lh3.googleusercontent.com/qJZSpzPTn8JJE2-mLbrQOmBZDbmFKKY1InOKlbPCWvxm66cAE6jIGPyZlrQ5hA27jYKxjsBYVwtS5u7nvXnWQMTXgyuK-DWpYLM3K4TeLQrnvDXB=w1440)

Five areas of Manhattan used in this study

Studying navigation is fundamental in the study and development of artificial intelligence, and trying to replicate navigation in artificial agents can also help scientists understand its biological underpinnings.
