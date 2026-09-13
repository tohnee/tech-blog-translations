---
title: "Navigating with grid-like representations in artificial agents"
source: https://deepmind.google/blog/navigating-with-grid-like-representations-in-artificial-agents/
site: deepmind
date: 2018-05-09
authors: Andrea Banino, Dharshan Kumaran, Caswell Barry, Benigno Uria
crawled: 2026-09-13
---

Most animals, including humans, are able to flexibly navigate the world they live in – exploring new areas, returning quickly to remembered places, and taking shortcuts. Indeed, these abilities feel so easy and natural that it is not immediately obvious how complex the underlying processes really are. In contrast, spatial navigation remains a substantial challenge for artificial agents whose abilities are far outstripped by those of mammals.

In 2005, a potentially crucial part of the neural circuitry underlying spatial behaviour was revealed by an astonishing discovery: neurons that fire in a strikingly regular hexagonal pattern as animals explore their environment. This lattice of points is believed to facilitate spatial navigation, similarly to the gridlines on a map. In addition to equipping animals with an internal coordinate system, these neurons - known as [**grid cells**](https://en.wikipedia.org/wiki/Grid_cell) - have recently been hypothesised to support **vector-based navigation**. That is: enabling the brain to calculate the distance and direction to a desired destination, “[as the crow flies](https://en.wikipedia.org/wiki/Euclidean_distance),” allowing animals to make direct journeys between different places even if that exact route had not been followed before.

The group that first discovered grid cells was jointly awarded the [2014 Nobel Prize in Physiology or Medicine](https://www.nobelprize.org/prizes/medicine/2014/summary/) for shedding light on how cognitive representations of space might work. But after more than 10 years of theorising since their discovery, the computational functions of grid cells - and whether they support vector-based navigation - has remained largely a mystery.

![Grid cells fire when an agent traverses a set of small regions, called firing fields. Colour-coded map showing firing rate distribution of a biological grid cell. The colour scale is from blue (no firing) to orange (peak firing rate). Biological grid cells are anatomically separated into modules of neurons (grey ovals) with different scales. One neuron of each scale is shown to be firing (orange). By reading out the activity of the population of grid cells, referred to as the grid code, an animal can determine its location in the environment. Triangles drawn atop the firing fields of grid cells highlight a grid pattern following a regular hexagonal structure.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6226874bed593bcc260a76e0_Grid20Cells2001.gif)

In our [most recent paper](https://www.nature.com/articles/s41586-018-0102-6) [[PDF here](https://www.nature.com/articles/s41586-018-0102-6.epdf?author_access_token=BjM-5BdGxd14c17YFA6PsdRgN0jAjWel9jnR3ZoTv0OEfySMT4t78PpPpCS7uExW3njb8Q4UlgcwRM32WwBCKZs73SThwkfI42wHhFEtJM-Y7sQxDsR1cR7_C9Kq1GwuxGJn46kzRnujvrDMGzc4TQ%3D%3D)]published in Nature, we developed an artificial agent to test the theory that grid cells support vector-based navigation, in keeping with our [overarching philosophy](https://deepmind.com/blog/article/ai-and-neuroscience-virtuous-circle) that algorithms used for AI can meaningfully approximate elements of the brain.

As a first step, we trained a recurrent network to perform the task of localising itself in a virtual environment, using predominantly movement-related velocity signals. This ability is commonly used by mammals when moving through unfamiliar places or in situations where it is not easy to spot familiar landmarks (e.g. when navigating in the dark).

We found that grid-like representations (hereafter grid units) spontaneously emerged within the network - providing a striking convergence with the neural activity patterns observed in foraging mammals, and consistent with the notion that grid cells provide an efficient code for space.

![Two rows of heat maps comparing firing rate patterns: the top row labeled "Artificial (Agent)" shows grid-like representation fields from an artificial agent, and the bottom row labeled "Biological (Rat)" shows biological grid cell firing patterns.](https://lh3.googleusercontent.com/pdfgh-9Uo9mNAKKKyBNSJZSrS9_lYe_4MZh8Cy0EWKy3qIV9tD31rFPXLnkh5HBKOxkh0GYk_73a7eY1katvine3Bqz5WhFuznWfpGyPCki-HsEWsQ=w1440)

Our experiments with artificial agents yielded grid-like representations (“grid units”) that were strikingly similar to biological grid cells in foraging mammals.

We next sought to test the theory that grid cells support vector-based navigation by creating an artificial agent to be used as an experimental guinea pig. This was done by combining the initial “grid network” with a larger network architecture, forming an agent that could be trained using deep reinforcement learning to navigate to goals in challenging virtual reality game environments.

This agent performed at a super-human level, exceeding the ability of a professional game player, and exhibited the type of flexible navigation normally associated with animals, taking novel routes and shortcuts when they became available.

![Two side-by-side diagrams comparing an agent's path to a goal: the left diagram shows a meandering path around closed red barriers, while the right diagram shows a direct vector path when the barriers are open.](https://lh3.googleusercontent.com/iA0EDJPGVEykPI5o8Xbmmvrqe4vuzEssa342Wz5owHTIC9BfC0tyf_DCKbVXtMyySyy5Z2zmH93kod3I02g1-FU_H5GsOZ_QyE7juattK4Icu8LAyjQ=w1440)

Through a series of experimental manipulations, we showed that grid-like representations were critical for vector-based navigation. For example, when grid cells in the network were silenced, the agent’s ability to navigate was impaired, and the representation of key metrics such as distance and direction to the goal became less accurate.

![Agent starts at bottom right (orange), the goal is at top left (green). Agent explores the room, as grid units fire to represent the agent's position (orange ovals). The pattern of grid units active at the agent's current position is the "current grid code". Agent arrives at goal for the first time via a wandering path. Activation colours change green to indicate that agent has arrived at goal. Agent now knows the location of the goal, storing the "goal grid code" (grid unit activity pattern at the goal). Agent starts at origin, retrieves the goal grid code from memory, and calculates a vector which represents the most direct path from origin to goal. The calculated vector is then used to follow the most direct path to the goal. Agent has reached the goal using vector-based navigation.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/622687e38a29ed50d4cb8c35_Grid20Cells2004.gif)

An illustration of vector-based navigation with grid units. The circles at the bottom represent grid unit populations of 3 different scales; colored cells are active. As the agent moves, the grid units that fire - which represent the “current grid code” - change to reflect the agent entering different firing fields. Grid units are used to calculate the shortest path to the goal.

We believe our study constitutes an important step in understanding the fundamental computational purpose of grid cells in the brain and also highlights the benefits they afford to artificial agents. The evidence provides compelling support for the theory that grid cells provide a Euclidean spatial framework - a concept of space - enabling vector-based navigation.

More broadly, our work reaffirms the potential of utilising algorithms thought to be used by the brain as [inspiration for machine learning architectures](https://www.cell.com/neuron/fulltext/S0896-6273(17)30509-3). The extensive previous neuroscience research into grid cells makes the agent's interpretability - which is itself a major topic in AI research - significantly easier, by giving us clues about what to look for when trying to understand its internal representations. The work also showcases the potential of using artificial agents actively engaging in complex behaviours within realistic virtual environments to test theories of how the brain works.

Taking this principle further, a similar approach could be used to test theories concerning brain areas that are important for perceiving sound or controlling limbs, for example. In the future such networks may well provide a new way for scientists to conduct ‘experiments’, suggesting new theories and even complementing some of the work that is currently conducted in animals.

UPDATE 14.05.18

We’d encourage you to read [The emergence of grid-like representations by training recurrent neural networks to perform spatial localization](https://openreview.net/forum?id=B17JTOe0-) by Cueva and Wei, which was published contemporaneously at ICLR. While different in scope and findings, it shows interesting results. In brief, the authors found periodic firing that conformed to the shape of the enclosure, e.g rectangular grids in a square environment and triangular in a triangular environment (fig. 2 of Cueva and Wei). This differs from our study, where we found grid-like units whose firing pattern closely resembles rodent grid cells which typically show hexagonal firing patterns across different shaped environments (e.g. square and circular arena).

Read the Nature paper: [[PDF](https://www.nature.com/articles/s41586-018-0102-6.epdf?author_access_token=BjM-5BdGxd14c17YFA6PsdRgN0jAjWel9jnR3ZoTv0OEfySMT4t78PpPpCS7uExW3njb8Q4UlgcwRM32WwBCKZs73SThwkfI42wHhFEtJM-Y7sQxDsR1cR7_C9Kq1GwuxGJn46kzRnujvrDMGzc4TQ%3D%3D)]

Download the original paper (unformatted): [[PDF](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/navigating-with-grid-like-representations-in-artificial-agents/Vector-based%20Navigation%20using%20Grid-like%20Representations%20in%20Artificial%20Agents.pdf)]

Read Nobel Prize Laureate Edvard Moser's [review of the paper](https://f1000.com/prime/733198068?key=nvlnlWetE8dlZTy).

This work was done by Andrea Banino, Caswell Barry, Benigno Uria, Charles Blundell, Timothy Lillicrap, Piotr Mirowski, Alexander Pritzel, Martin Chadwick, Thomas Degris, Joseph Modayil, Greg Wayne, Hubert Soyer, Fabio Viola, Brian Zhang, Ross Goroshin, Neil Rabinowitz, Razvan Pascanu, Charlie Beattie, Stig Petersen, Amir Sadik, Stephen Gaffney, Helen King, Koray Kavukcuoglu, Demis Hassabis, Raia Hadsell, and Dharshan Kumaran.
