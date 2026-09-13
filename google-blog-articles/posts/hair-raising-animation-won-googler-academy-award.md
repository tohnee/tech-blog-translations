---
title: "Hair-raising animation won this Googler an Academy Award"
source: https://blog.google/innovation-and-ai/technology/research/hair-raising-animation-won-googler-academy-award/
site: google-blog
date: 2021-02-18
authors: Zack Ontiveros
crawled: 2026-09-13
---

On February 13, Google Research’s own John Anderson was the recipient of the Academy Award for Technical Achievement — an award given annually for technical accomplishments that [“contribute to the progress of the motion picture industry](https://www.oscars.org/sci-tech/technical#:~:text=Technical%20Achievement%20Awards%20are%20given,at%20an%20annual%20award%20ceremony.).” John is being recognized for contributions to the [Taz Hair Simulation System](https://graphics.pixar.com/library/CurlyHairB/paper.pdf) developed during his time at Pixar. His work is most notably featured in Pixar’s movie "Brave," powering the springy curls of the main character Merida. This is John’s second Academy Award over his 14 years working in film. He received his first in 2002 for his work on George Lucas’ Industrial Light and Magic’s [Creature Dynamics System](https://www.ilm.com/awards/ilm-creature-dynamics-system-awards/), which similarly enabled the realistic animation of movement of hair, skin and clothing used in movies such as "Star Wars: Episode I," "The Mummy" and "Mighty Joe Young."

Mark Meyer (left) - Research Group Lead at Pixar and John Anderson (right) - Principal Scientist at Google Research during their shared time at Pixar.

![Mark Meyer (left) - Research Group Lead at Pixar and John Anderson (right) - Principal Scientist at Google Research during their shared time at Pixar](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/AndersonJohn_00967_janders_fun.t.width-1200.format-webp.webp)

Simulation is a difficult computational problem, as it attempts to recreate a continuous physical world using a limited amount of compute power. To make the real world processable by computers, designers of a simulation must “discretize” or chunk the world into coarse pieces and calculate the physical interactions between those coarse chunks. Within those chunks, simulation designers must “parameterize,” or make assumptions about the behavior of the world, as computing the physics beyond this point would be too expensive. The art of simulation is tuning these assumptions and balancing the accuracy, scale and cost of the recreation of the physical world.

Example of the output of the Taz Hair Simulation System.

![Example of the output of the Taz Hair Simulation System](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/PixarTaz-Merida.width-1200.format-webp.webp)

For curly hair, like Merida’s in "Brave," there are countless collisions between individual strands of hair at any given time. Even more complicated are the individual physics of those strands of hair, effectively acting like small springs. The hair simulation technology used in Brave employed clever mathematical schemes which kept the computational cost low, enabling animators to work quickly and efficiently, while still maintaining a high degree of physical accuracy, ensuring that Merida’s tight curls still bounced and flowed like real hair.

Before joining the film industry, John served for nearly 14 years as a professor of Atmospheric and Oceanic Sciences at University of Wisconsin-Madison. It was this experience in physics and computational fluid dynamics which served as a basis for a number of his contributions across his film career. At Google, John now focuses on leveraging his unique background to help the world combat the effects of one of the day’s most pressing issues: climate change. John leads a group within Google Research that explores how we can improve simulation to better model the climate and climate-change-exacerbated phenomena like floods and wildfires.

Like in hair animation, large climate models depend on the individual interactions of small scale processes, such as the turbulent or chaotic movement of individual clouds. However, instead of the clever mathematical schemes used for Merida’s hair, John’s research group focuses on using machine learning to predict the dynamics of the physics, enabling modellers to both improve the accuracy of those “within chunk” assumptions or replace the model altogether with a machine-learned equivalent.

John’s group employs Google’s TPUs to generate high resolution recreations of [floods](https://blog.google/technology/ai/flood-forecasts-india-bangladesh/), wildfires and clouds. The outputs of these simulations are used to train machine learning models which can then be used within subsequent simulations to reduce cost and improve accuracy. His group believes that through the application of machine learning to simulation, we will be able to create more efficient models that will accelerate our ability to predict and prepare for the effects of climate change.

From bringing to life the smallest details in animation and film to improving global models of climate and weather, John’s work has greatly advanced how we understand the dynamics of the physical world. Congratulations, John!
