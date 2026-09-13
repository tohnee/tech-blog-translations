---
title: "Genie 3: A new frontier for world models"
source: https://deepmind.google/blog/genie-3-a-new-frontier-for-world-models/
site: deepmind
date: 2025-08-05
authors: Jack Parker-Holder, Shlomi Fruchter
crawled: 2026-09-13
---

Today we are announcing Genie 3*,* a general purpose world model that can generate an unprecedented diversity of interactive environments.

Given a text prompt, Genie 3 can generate dynamic worlds that you can navigate in real time at 24 frames per second, retaining consistency for a few minutes at a resolution of 720p.

## Towards world simulation

At Google DeepMind, we have been pioneering research in simulated environments for over a decade, from training agents to [master real-time strategy games](https://deepmind.google/discover/blog/alphastar-mastering-the-real-time-strategy-game-starcraft-ii/?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=&utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=) to developing simulated environments for [open-ended learning](https://deepmind.google/discover/blog/generally-capable-agents-emerge-from-open-ended-play/?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=) and [robotics](https://deepmind.google/discover/blog/from-motor-control-to-embodied-intelligence/?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=). This work motivated our development of world models, which are AI systems that can use their understanding of the world to simulate aspects of it, enabling agents to predict both how an environment will evolve and how their actions will affect it.

World models are also a key stepping stone on the path to AGI, since they make it possible to train AI agents in an unlimited curriculum of rich simulation environments. Last year we introduced the first foundation world models with [Genie 1](https://deepmind.google/research/publications/60474/?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=&utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=) and [Genie 2](https://deepmind.google/discover/blog/genie-2-a-large-scale-foundation-world-model/?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=&utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=), which could generate new environments for agents. We have also continued to push the state of the art in video generation with our models Veo 2 and Veo 3, which exhibit a deep understanding of intuitive physics.

Each of these models marks progress along different capabilities of world simulation. Genie 3 is our first world model to allow interaction in real-time, while also improving consistency and realism compared to Genie 2.

![Comparison table detailing the advancements of the Genie 3 model over GameNGen, Genie 2, and Veo in key areas like control, resolution, and interaction latency.](https://lh3.googleusercontent.com/cZoNo9iSxNXrzUDTQUuy84upr6YnjHF1XaysuhkUG9X8LwCzKI3KX4scd0Y779NBBi7ffpkTbTaKqPZ_07Wto_0VaqjF8gmwNAwTSk3eLOtX8PCn=w1440)

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

Genie 3 can generate a consistent and interactive world over a longer horizon

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

- [Capabilities](#capabilities)
- [Embodied agent research](#embodied-agent-research)
- [Limitations](#limitations)
- [Responsibility](#responsibility)
- [Next steps](#next-steps)

## Genie 3’s capabilities include:

The following are recordings of real time interactions from Genie 3.

### Modelling physical properties of the world

Experience natural phenomena like water and lighting, and complex environmental interactions.

Slide 1 of 5

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

**Prompt:** The video shows a first person perspective of someone navigating difficult terrain in the middle of a volcanic area. This is a real world video shot from the perspective of a wheeled robot that needs to traverse across a terrain. The vehicle has chunky offroad tires that crunch under the blackened rock. The camera is an egocentric camera mounted to the vehicle, and you can see the front tires just on the bottom of the camera along with the body of the robot. In the distance you can see smoke and lava flowing from the volcano. There are no other visible signs of life. There are lava pools that the agent is trying to avoid and random rock formations. The sky is a vivid blue.

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

**Prompt:** Jetski during the festival of lights

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

**Prompt:** Walking on a pavement in Florida next to a two-lane road from one side and the sea on the other, during an approaching hurricane, with strong wind and waves splashing over the road. There is a railing on the left of the agent, separating them from the sea. The road goes along the coast, with a short bridge visible in front of the agent. Waves are splashing over the railing and onto the road one after another. Palm trees are bending in the wind. There is heavy rain, and the agent is wearing a rain coat. Real world, first-person.

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

**Prompt:** Fast tracking real world video following a jellyfish swimming at high speed through the darkness of the deep sea between canyons covered in densely packed vent mussels with tiny white crabs crawling on them. Blurry hydrothermal vents in the distance spew thick, billowing plumes of vibrant blue, mineral-rich smoke from glowing rocky structures. Very dark, dim deep sea lighting, particles float in the cloudy ocean.

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

**Prompt:** A helicopter pilot carefully maneuvering over a coastal cliff with a small waterfall.

### Simulating the natural world

Generate vibrant ecosystems, from animal behaviors to intricate plant life.

Slide 1 of 4

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

**Prompt:** Running by the shores of a glacial lake, exploring branching paths through the forest, crossing flowing mountain streams. Set amidst beautiful snow capped mountains and pine forest. Plentiful wildlife makes the journey a delight.

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

**Prompt:** Real world tracking shot swimming through deep dimly lit ocean between deep ocean canyons, densely packed vast school of jellyfish swimming, bioluminescent lighting.

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

**Prompt:** This is a natural, real-world landscape designed as a Japanese zen garden. The scene is set in the early morning under a clear sky. Soft, warm sunlight illuminates the garden, casting long, gentle shadows. The ground is covered in fine, white sand that is raked into meticulous swirling patterns. A small, still pond is present, with pink water lilies floating on its surface. Smooth, grey rocks of various sizes are placed throughout the garden, some with green moss on their surfaces. Key structures include a stacked stone cairn and a traditional Japanese stone lantern. The entire area is enclosed by a tall bamboo fence in the background. The visual style is photorealistic, with high detail in the textures of the sand, stone, and lush green vegetation.

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

**Prompt:** The environment is a natural, real-world landscape, specifically a dense arrangement of lush, vibrant foliage. The leaves are broad and deeply textured, displaying an array of green hues from emerald to lime, interspersed with hints of yellow and red, suggesting a rich, healthy ecosystem. Abstract dappled light filters down from above, creating shifting patterns of illumination and shadow across the leaves, highlighting their intricate veins and varied surfaces. The atmosphere is serene and deeply immersive, evoking a sense of being within a vibrant, living natural world. Small water droplets are visible on some leaf surfaces, reflecting the ambient light. The background is a soft blur of similar foliage, emphasizing the foreground elements. The air appears humid and still.

### Modelling animation and fiction

Tap into imagination, creating fantastical scenarios and expressive animated characters.

Slide 1 of 4

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

**Prompt:** A vibrant 3D style, an adorable, fluffy creature bounding across a vibrant rainbow bridge in a fantastical landscape. The creature is small and compact, with fur that mimics the warm hues of a sunrise – oranges, yellows, and pinks blending seamlessly together. Its most striking feature is a pair of large, perked ears, shaped like those of a German Shepherd, adding a touch of playful contrast to its otherwise rounded form. As it runs on four short legs across the rainbow, its fur appears to ripple and flow, adding to its sense of dynamism and energy. The rainbow bridge arches gracefully through a whimsical landscape, perhaps filled with floating islands, glowing flora, and swirling clouds. The lighting is bright and cheerful, casting a warm glow on the creature and its surroundings. The overall impression is one of joy, wonder, and boundless energy, capturing the creature's playful spirit and the magical nature of the world it inhabits. This image evokes a sense of childlike whimsy and invites the viewer to imagine the adventures that await this charming creature in its fantastical realm.

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

**Prompt:** Being a lizard, origami style

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

**Prompt:** A fantastical, wide-angle shot captures a lush, enchanted forest bathed in the soft glow of twilight. The player controls a large firefly flying through towering trees with vibrant foliage creating a dense canopy overhead, filtering the sunlight and casting dappled shadows on the forest floor. Nestled among the branches are a handful of charming tree houses, each glowing with a warm, inviting light. The tree houses vary in size and design, some resembling whimsical castles, others cozy cabins. Tiny details, like glowing windows and miniature balconies, add to their charm. A winding path, barely visible beneath the undergrowth, leads the viewer's eye deeper into the enchanted forest. The overall scene evokes a sense of wonder, tranquility, and the magic of childhood dreams.

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

**Prompt:** A serene Irish landscape, with rolling emerald-green hills, misty lakes, and rugged mountains, suddenly trembles violently—as if the earth itself is being torn apart. In a moment of surreal chaos, entire sections of land rip free, rising into the sky in jagged, brutalist formations, their rocky undersides exposed like raw, fractured earth. The lakes are wrenched upward, now suspended in the sky, their waters spilling downward in colossal waterfalls, creating an apocalyptic storm of mist and rain over the land below. The camera pulls back, revealing a new impossible geography—mountains floating, cliffs inverted, rivers twisting mid-air—as gravity itself bends, turning the once-peaceful countryside into a brutalist, surreal monument to nature’s violent transformation.

### Exploring locations and historical settings

Transcend geographical and temporal boundaries to explore places and past eras.

Slide 1 of 5

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

**Prompt:** A real world mountainous environment in the Alps. The landscape features steep, rocky cliffs and narrow gorges filled with loose scree and debris. The rock is predominantly grey and white, with patches of green vegetation clinging to the cliff faces. The top of the gorge opens up to a vista of dense evergreen forests and meadows. The overall theme is one of rugged, natural beauty and extreme terrain.

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

**Prompt:** Venice by Vaporetto. The canals of Venice are recreated with painstaking detail. The water has realistic reflections and wakes. The buildings show crumbling plaster and centuries of weathering. The scene is populated with other gondolas, water taxis, and barges.

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

**Prompt:** Exploring the palace of Knossos on Crete as it would have stood in its glorious heyday.

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

**Prompt:** Walking around on a beautiful day out in Hinsdale, Illinois. Real world. There are cars parked. The person filming is standing on the sidewalk, there are flocks of birds flying overhead.

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

**Prompt:** A biking enthusiast driving on a narrow road on an edge of a cliff in India, the Killar-Kishtwar Road. Real-world, first-person, only hands on handles visible.

### Pushing the frontier of real-time capabilities

Achieving a high degree of controllability and real-time interactivity in Genie 3 required significant technical breakthroughs. During the auto-regressive generation of each frame, the model has to take into account the previously generated trajectory that grows with time. For example, if the user is revisiting a location after a minute, the model has to refer back to the relevant information from a minute ago. To achieve real-time interactivity, this computation must happen multiple times per second in response to new user inputs as they arrive.

### Environmental consistency over a long horizon

In order for AI generated worlds to be immersive, they have to stay physically consistent over long horizons. However, generating an environment auto-regressively is generally a harder technical problem than generating an entire video, since inaccuracies tend to accumulate over time. Despite the challenge, Genie 3 environments remain largely consistent for several minutes, with visual memory extending as far back as one minute ago.

Slide 1 of 5

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

**Prompt:** POV action camera of a tan house being painted by a first person agent with a paint roller

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

**Prompt:** A Victorian street with a grey house. The grey house has a portal ringed by magical sparks. The portal leads to a vast desert filled with dunes, and that desert is visible from the outside. The agent can walk into the portal and is teleported to the desert.

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

**Prompt:** This is a fantastical, whimsical forest environment. The lighting is bright and cheerful, suggesting a sunny day with dappled light filtering through a dense canopy of lush, oversized leaves. The air is clear and still. The ground is a soft, verdant carpet of moss and unusually large, brightly coloured mushrooms in shades of red and blue, their caps dotted with white. Winding dirt paths, well-trodden and narrow, weave between towering, ancient trees with smooth, grey bark. Interspersed throughout the forest are charming, mushroom-shaped houses, with intricate wooden doors and tiny, circular windows, each one unique in its design and colour palette, ranging from vibrant reds to gentle blues and greens. Various small, friendly forest creatures, such as colourful butterflies and tiny singing birds, flit amongst the foliage, adding to the lively atmosphere. There is an abundance of peculiar, oversized flowers blooming in an array of pastel and bright hues, releasing a gentle glow.

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

**Prompt:** An extremely enormous, realistic gorilla, draped in a flamboyant, emerald red vest with ornate brass buttons and an elaborate, feathered bicorne hat, brandishing only a vintage silk parasol, navigates a series of outrageously extravagant, moss-laden McMansions where grand marble structures are subtly embraced by sprawling, ancient rose bushes and creeping ivy.

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

**Prompt:** Walking around ancient Athens, Greek architecture, marble

![Three video frames of a generated ancient Greek temple and ruins at 0:00, 0:20, and 0:40, demonstrating the model's visual memory and environmental consistency over time.](https://lh3.googleusercontent.com/mqzat7VkvKPSmjGZJgfgeK10HHg0w_9_UktqhR_YrpPEhme5G2VJKCqFNasBu-wEmOS_vNbpbE0uRGVzFQUkUNJoHVcTDPmJre-jByG6gkGTHbDk=w1440)

*The trees to the left of the building remain consistent throughout the interaction, even as they go in and out of view.*

Genie 3’s consistency is an emergent capability. Other methods such as NeRFs and Gaussian Splatting also allow consistent navigable 3D environments, but depend on the provision of an explicit 3D representation. By contrast, worlds generated by Genie 3 are far more dynamic and rich because they’re created frame by frame based on the world description and actions by the user.

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

**Prompt:** First-person view drone video. High speed flight into and along a narrow canyon in Iceland with a river at the bottom and moss on the rocks, golden hour, realworld

### Promptable world events

In addition to navigational inputs, Genie 3 also enables a more expressive form of text-based interaction, which we refer to as *promptable world events*.

Promptable world events make it possible to change the generated world, like altering weather conditions or introducing new objects and characters, enhancing the experience from navigation controls.

This ability also increases the breadth of counterfactual, or “what if” scenarios, that can be used by agents learning from experience to handle unexpected situations.

**Choose a world setting. Then, pick an event, and see Genie 3 create it.**

### Fueling embodied agent research

To test the compatibility of Genie 3 created worlds for future agent training, we generated worlds for a recent version of our [SIMA agent](https://deepmind.google/discover/blog/sima-generalist-ai-agent-for-3d-virtual-environments/?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=), our generalist agent for 3D virtual settings. In each world we instructed the agent to pursue a set of distinct goals, which it aims to achieve by sending navigation actions to Genie 3. Like any other environment, Genie 3 is not aware of the agent’s goal, instead it simulates the future based on the agent's actions.

**Choose a world setting. Then, pick a goal you'd like an agent to achieve and watch how it accomplishes it.**

Since Genie 3 is able to maintain consistency, it is now possible to execute a longer sequence of actions, achieving more complex goals. We expect this technology to play a critical role as we push toward AGI, and agents play a greater role in the world.

Slide 1 of 3

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

## Limitations

While Genie 3 pushes the boundaries of what world models can accomplish, it's important to acknowledge its current limitations:

- **Limited action space**. Although promptable world events allow for a wide range of environmental interventions, they are not necessarily performed by the agent itself. The range of actions agents can perform directly is currently constrained.
- **Interaction and simulation of other agents**. Accurately modeling complex interactions between multiple independent agents in shared environments is still an ongoing research challenge.
- **Accurate representation of real-world locations**. Genie 3 is currently unable to simulate real-world locations with perfect geographic accuracy.
- **Text rendering.** Clear and legible text is often only generated when provided in the input world description.
- **Limited interaction duration.** The model can currently support a few minutes of continuous interaction, rather than extended hours.

## Responsibility

We believe foundational technologies require a deep commitment to responsibility from the very beginning. The technical innovations in Genie 3, particularly its open-ended and real-time capabilities, introduce new challenges for safety and responsibility. To address these unique risks while aiming to maximize the benefits, we have worked closely with our Responsible Development & Innovation Team.

At Google DeepMind, we're dedicated to developing our best-in-class models in a way that amplifies human creativity, while limiting unintended impacts. As we continue to explore the potential applications for Genie, we are announcing Genie 3 as a limited research preview, providing early access to a small cohort of academics and creators. This approach allows us to gather crucial feedback and interdisciplinary perspectives as we explore this new frontier and continue to build our understanding of risks and their appropriate mitigations. We look forward to working further with the community to develop this technology in a responsible way.

## Next steps

We believe Genie 3 is a significant moment for world models, where they will begin to have an impact on many areas of both AI research and generative media. To that end, we're exploring how we can make Genie 3 available to additional testers in the future.

Genie 3 could create new opportunities for education and training, helping students learn and experts gain experience. Not only can it provide a vast space to train agents like robots and autonomous systems, Genie 3 can also make it possible to evaluate agents’ performance, and explore their weaknesses.

At every step, we’re exploring the implications of our work and developing it for the benefit of humanity, safely and responsibly.

**Please cite using the following BibTex**

[Download BibTeX](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/genie-3/genie3worldmodel2025.bib?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=)

## Acknowledgments

Genie 3 was made possible due to key research and engineering contributions from Phil Ball, Jakob Bauer, Frank Belletti, Bethanie Brownfield, Ariel Ephrat, Shlomi Fruchter, Agrim Gupta, Kristian Holsheimer, Aleks Holynski, Jiri Hron, Christos Kaplanis, Marjorie Limont, Matt McGill, Yanko Oliveira, Jack Parker-Holder, Frank Perbet, Guy Scully, Jeremy Shar, Stephen Spencer, Omer Tov, Ruben Villegas, Emma Wang and Jessica Yung.

We thank Andrew Audibert, Cip Baetu, Jordi Berbel, David Bridson, Jake Bruce, Gavin Buttimore, Sarah Chakera, Bilva Chandra, Paul Collins, Alex Cullum, Bogdan Damoc, Vibha Dasagi, Maxime Gazeau, Charles Gbadamosi, Shan Han, Woohyun Han, Ed Hirst, Ashyana Kachra, Lucie Kerley, Kristian Kjems, Eva Knoepfel, Vika Koriakin, Jessica Lo, Cong Lu, Zeb Mehring, Alexandre Moufarek, Henna Nandwani, Valeria Oliveira, Fabio Pardo, Jane Park, Andrew Pierson, Ben Poole, Helen Ran, Nilesh Ray, Tim Salimans, Manuel Sanchez, Igor Saprykin, Amy Shen, Sailesh Sidhwani, Duncan Smith, Joe Stanton, Hamish Tomlinson, Dimple Vijaykumar, Luyu Wang, Piers Wingfield, Nat Wong, Keyang Xu, Christopher Yew, Nick Young and Vadim Zubov for their invaluable partnership in developing and refining key components of this project.

Thanks to Tim Rocktäschel, Satinder Singh, Adrian Bolton, Inbar Mosseri, Aäron van den Oord, Douglas Eck, Dumitru Erhan, Raia Hadsell, Zoubin Gharamani, Koray Kavukcuoglu and Demis Hassabis for their insightful guidance and support throughout the research process.

Feature video was produced by Suz Chambers, Matthew Carey, Alex Chen, Andrew Rhee, JR Schmidt, Scotch Johnson, Heysu Oh, Kaloyan Kolev, Arden Schager, Sam Lawton, Hana Tanimura, Zach Velasco, Ben Wiley, and Dev Valladares. Including samples generated by Signe Nørly, Eleni Shaw, Andeep Toor, Gregory Shaw, and Irina Blok.

We thank Frederic Besse, Tim Harley and the rest of the SIMA team for access to a recent version of their agent.

Finally, we extend our gratitude to Mohammad Babaeizadeh, Gabe Barth-Maron, Parker Beak, Jenny Brennan, Tim Brooks, Max Cant, Harris Chan, Jeff Clune, Kaspar Daugaard, Dumitru Erhan, Ashley Feden, Simon Green, Nik Hemmings, Michael Huber, Jony Hudson, Dirichi Ike-Njoku, Hernan Moraldo, Bonnie Li, Simon Osindero, Georg Ostrovski, Ryan Poplin, Alex Rizkowsky, Giles Ruscoe, Ana Salazar, Guy Simmons, Jeff Stanway, Metin Toksoz-Exley, Xinchen Yan, Petko Yotov, Mingda Zhang and Martin Zlocha for their insights and support.
