---
title: "Using machine learning to accelerate ecological research"
source: https://deepmind.google/blog/using-machine-learning-to-accelerate-ecological-research/
site: deepmind
date: 2019-08-08
authors: Stig Petersen, Meredith Palmer, Ulrich Paquet, Pushmeet Kohli
crawled: 2026-09-13
---

The Serengeti is one of the last remaining sites in the world that hosts an intact community of large mammals. These animals roam over vast swaths of land, some migrating thousands of miles across multiple countries following seasonal rainfall. As human encroachment around the region becomes more intense, these species are forced to alter their behaviours in order to survive. Increasing agriculture, poaching, and climate abnormalities contribute to changes in animal behaviours and population dynamics, but these changes have occurred at spatial and temporal scales which are difficult to monitor using traditional research methods. There is a great urgency to understand how these animal communities function as human pressures grow, both in order to understand the dynamics of these last pristine ecosystems, and to formulate effective management plans to conserve and protect the integrity of this unique biodiversity hotspot.

To this end, DeepMind is collaborating with ecologists and conservationists to develop machine learning methods to help study the behavioural dynamics of an entire African animal community in the Serengeti National Park and Grumeti Reserve in Tanzania. The Serengeti-Mara ecosystem is globally unparalleled in its biodiversity, hosting an estimated 70 large mammal species and 500 bird species, thanks in part to its unique geology and varied habitat types. Almost a decade ago, the Serengeti Lion Research program installed hundreds of motion-sensitive cameras within the core of the protected area. The cameras are triggered by passing wildlife, capturing animal images frequently, across vast spatial scales, allowing researchers to study animal behaviour, distribution, and demography with great spatial and temporal resolution.

![An extreme close-up camera trap photo of a cheetah looking off-camera, with a grassy savanna and blue sky in the background.](https://lh3.googleusercontent.com/9bnhBbcx7g-0J514I7L7EEhzsnzqsZuIPv29BvoomJYaSMecv-ty7rEC9yLZtvqzoxvw-Zsd9pbFKWhBRABiFSwSD2_Rj0RDBLf9JSf92InlMie2=w1440)

Motion sensors in a camera trap trigger the device to take images of naturally behaving animals without interfering with their daily routines. Photos may be empty, having been triggered by a false alarm, or contain dozens of individuals at different distances and poses. Monitored species range from aardvarks to zebras.

Over the last nine years, the team has collected and stored millions of photos like the one above. Until now, volunteers from across the world have helped to identify and count the species in the photos by hand using the [Zooniverse](https://www.zooniverse.org/projects/zooniverse/snapshot-serengeti) web-based platform, which hosts many similar projects for citizen-scientists. This has resulted in a rich [dataset](https://datadryad.org/resource/doi:10.5061/dryad.5pt92), [Snapshot Serengeti](https://www.nature.com/articles/sdata201526), featuring labels and counts for around 50 different species. Currently, the annotation process is labor intensive and time-consuming: it takes up to a year from the time a camera is triggered until labels are collected from volunteers. This bottleneck has not only impeded scientists’ ability to perform basic research, but has made it hard for conservationists to react adaptively to challenges and perturbations disrupting the ecosystem. To help researchers unlock this data with greater efficiency, we’ve used the [Snapshot Serengeti dataset](https://www.nature.com/articles/sdata201526) to train machine learning models to automatically detect, identify, and count animals.

![An extreme close-up camera trap photo of an African buffalo leaning in with its nose right in front of the lens.](https://lh3.googleusercontent.com/d_hM5xc3o_d8buOYiwGBbRH3KWalGlsaH4tkXWfeZL1uDozVDET9UR9fZYnn7THVKAAhOhWg8NQhNgnc86Ac_XmXmlvvkOhCFV5q9A0K7MoY7avablI=w1440)

Grazing buffalo captured by a motion sensitive camera. Note that the challenge of labelling the photographed species is not entirely straightforward – sometimes a full view is obscured, or only a certain portion of an animal is captured, or in focus. Our system is currently as accurate as human labellers in identifying about 50 large species correctly.

Using machine learning for conservation is not new. For example, researchers have previously leveraged [tourist photos](https://www.cell.com/current-biology/fulltext/S0960-9822(19)30626-8?dgcid=raven_jbs_etoc_email) and [YouTube videos](https://www.nationalgeographic.co.uk/animals/2018/11/how-artificial-intelligence-changing-wildlife-research) to track animals, and [audio recordings](https://www.nature.com/articles/d41586-019-00746-1) to identify species by their calls. Camera trap data can be hard to work with–animals may appear out of focus, and can be at many different distances and positions with respect to the camera (as in the image above). With expert input from leading ecologist and conservationist Dr. Meredith Palmer, our project quickly took shape, and we now have a model that can perform on par with, or better than, human annotators for most of the species in the region. Importantly, this method shortens the data processing pipeline by up to 9 months, which has immense potential to help researchers in the field.

Of course, field work is challenging, and fraught with unexpected hazards such as failing power lines and limited or no internet access. We are currently preparing the software for deployment in the field, and looking at ways to safely run our pre-trained model with modest hardware requirements and little Internet access. We’ve worked closely with our collaborators in the field to be sure that our technology is used [responsibly](https://www.nature.com/articles/s42256-019-0022-7). Once in place, researchers in the Serengeti will be able to make direct use of this tool, helping provide them with up-to-date species information to better support their conservation efforts.

![A camera trap photo of a male ostrich with a bright pink neck and legs standing in the grassy savanna of the Serengeti.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62272fab3d02a35aa8b88d73_Serengeti204.gif)

An ostrich roaming the Serengeti.

We will be talking further about the project and related work at the [Deep Learning Indaba](http://www.deeplearningindaba.com/) in Kenya later this August. DeepMind is a founding partner of the Deep Learning Indaba, a continent-wide movement to strengthen the research and application of ML and AI in Africa, and several DeepMind researchers serve as key organisers of this unique event. “Indaba” is a Zulu word indicating an important community gathering. This year, community-led IndabaX AI conferences were held in 26 African countries as part of the runup to the main [Deep Learning Indaba](http://www.deeplearningindaba.com/) at Kenyatta University in Kenya in late August. For a week, researchers, students and community members will meet to share their knowledge and best practices, and experts will host panels, workshops and discussions covering many topics in machine learning and AI. During this meeting, DeepMind and other Indaba volunteers will co-host a hackathon for anyone interested in ML and conservation to develop their own models using the [Snapshot Serengeti](https://www.zooniverse.org/projects/zooniverse/snapshot-serengeti) dataset. Ecology students will be equipped to understand and use ML models for conservation, and taught how to develop their own models. Through gatherings like Indaba, we hope to empower more local experts to use AI techniques for addressing problems in their own communities. The AI community in Africa is growing, and the hackathon will help to train local experts, centering on conservation as part of the core dialogue.

![A camera trap photo of a young male lion and a small cub sitting in the golden grass of the Serengeti at sunrise.](https://lh3.googleusercontent.com/5PwngeLDjj3V8Xb87LuRvLKOde4pl3dlVqcQYlPY8k--Xz28K4w0PZ5HFtq4-0FDUiA4QVuGMUWOHBpnsgDwsYyN_GgXMXN7be5cFgSSPVBVgSo3NA=w1440)

A lion and cub.

The DeepMind Science Team works to leverage AI to tackle key scientific challenges that impact the world. We’ve developed a robust model for detecting and analysing animal populations in field data, and have helped to consolidate data to enable the growing machine learning community in Africa to build AI systems for conservation which, we hope, will scale to other parks. We’ll next be validating our models by deploying them in the field and tracking their progress. Our hope is to contribute towards making AI research more inclusive–both in terms of the kinds of domains we apply it to, and the people developing it. Hence, participating in meetings like Indaba are key for helping build a global team of AI practitioners who can deploy machine learning for diverse projects.

![A camera trap photo of zebras in the Serengeti kicking up a cloud of dust.](https://lh3.googleusercontent.com/VOVDRDF-g62l8Ksy9VPl9PHwdQPWxdZbmD6jFcxvjVz8qONR2BgovsiGUpRgMpU4fNwG4Tz7xOUAWSMQsBZCoBK4qdn_99PUThO8Qv8JA5kbQIY4Aps=w1440)

A zebra gallops through grasslands.

**Project credits**

Jean-baptiste Alayrac, Sam Blackwell, Joao Carreira, Reena Chopra, Sander Dieleman, Brian McWilliams, Sofia Miñano, Sanjana Narayanan, Meredith Palmer, Ulrich Paquet, Stig Petersen, Roman Werpachowski, Michal Zielinski.

Additional Credits

Razia Ahamed, Andrea Banino, Pushmeet Kohli, Drew Purves, Andrew Zisserman

This work was made possible by data from Snapshot Serengeti. Images are available via a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/) and can be found [here](https://datadryad.org/resource/doi:10.5061/dryad.5pt92). Please contact [Dr Meredith Palmer](mailto:palme516@umn.edu) with data inquiries.

Swanson AB, Kosmala M, Lintott CJ, Simpson RJ, Smith A, Packer C (2015) Snapshot Serengeti, high-frequency annotated camera trap images of 40 mammalian species in an African savanna. Scientific Data 2: 150026
