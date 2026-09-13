---
title: "Advancing conservation with AI-based facial recognition of turtles"
source: https://deepmind.google/blog/advancing-conservation-with-ai-based-facial-recognition-of-turtles/
site: deepmind
date: 2022-08-25
authors: 
crawled: 2026-09-13
---

Finding solutions to improve turtle reidentification and supporting machine learning projects across Africa

Protecting the ecosystems around us is critical to safeguarding the future of our planet and all its living citizens. Fortunately, new artificial intelligence (AI) systems are making progress in conservation efforts worldwide, helping tackle complex problems at scale – from [studying the behaviour of animal communities in the Serengeti](https://deepmind.google/blog/using-machine-learning-to-accelerate-ecological-research/) to help conserve the diminishing ecosystem, to [spotting poachers and their wounded prey](https://www.newscientist.com/article/2305616-ai-can-spot-wounded-wild-animals-and-poachers-in-camera-trap-footage/) to prevent species going extinct.

As part of our mission to help benefit humanity with the technologies we develop, it's important we ensure diverse groups of people build the AI systems of the future so that it’s equitable and fair. This includes broadening the machine learning (ML) community and engaging with wider audiences on addressing important problems using AI.

Through investigation, we came across [Zindi](https://zindi.africa/) – a dedicated partner with complementary goals – who are the largest community of African data scientists and host competitions that focus on solving Africa’s most pressing problems.

Our [Science team](https://www.deepmind.com/about/science)’s Diversity, Equity, and Inclusion (DE&I) team worked with Zindi to identify a scientific challenge that could help advance conservation efforts and grow involvement in AI. Inspired by Zindi’s [bounding box turtle challenge](https://zindi.africa/competitions/local-ocean-conservation-sea-turtle-face-detection), we landed on a project with the potential for real impact: turtle facial recognition.

Biologists consider turtles to be an indicator species. These are classes of organisms whose behaviour helps scientists understand the underlying welfare of their ecosystem. For example, the presence of otters in rivers has been considered a sign of a clean, healthy river, since a ban on chlorine pesticides in the 1970s brought the species back from the brink of extinction.

Turtles are another such species. By grazing on seagrass cover, they cultivate the ecosystem, providing a habitat for numerous fish and crustaceans. Traditionally, individual turtles have been identified and tracked by biologists with physical tags, though frequent loss or erosion of these tags in seawater has made this an unreliable method. To help solve some of these challenges, we launched an ML challenge called [Turtle Recall](https://zindi.africa/competitions/turtle-recall-conservation-challenge).

![Four example photos of sea turtle heads from top, left, and right angles, paired with dataset labels for image file name, image location, and turtle ID.](https://lh3.googleusercontent.com/vbmpvxhQ6o1WgE9C_NPZuHCqZK0JR4iis5lGgCIKiKKSM3hlDH6O17kvQsQbJdSyugDnhmmB2wY5doaUgt7uC9ZmtVNfHtbY3Hye6txoW2jMEz1H=w1440)

Example of image data for four turtles taken from the tutorial colab notebook. Differences in lighting, scale, background, pose, and similarities between turtles added to the complexity of the prediction challenge. Credit: Zindi.

Given the additional challenge of keeping a turtle still enough to locate their tag, the Turtle Recall challenge aimed to circumvent these problems with turtle facial recognition. This is possible because the pattern of scales on a turtle's face is unique to the individual and remains the same over their multi-decade lifespan.

The challenge aimed to increase the reliability and speed of turtle reidentification, and potentially offer a way to replace the use of uncomfortable physical tags altogether. To make this possible, we needed a dataset to work from. Fortunately, after Zindi’s previous turtle-based challenge with Kenyan-based charity [Local Ocean Conservation](https://localocean.co/), the teams were kindly able to share a dataset of labelled images of turtle faces.

![A three-panel graphic illustrating AI facial recognition of sea turtles: the left panel shows a close-up profile of a sea turtle's head, highlighting its unique scale pattern; the center panel shows a blurred heatmap of the facial features detected by the machine learning model; and the right panel overlays this heatmap onto the turtle's face.](https://lh3.googleusercontent.com/J0hJ-FIr2bGtuj4mqCJwPRKLk3UE7eZtj2EK0M6a3ffyX7UC5jAjSsLKQHKj4IB06qSTC7IbP1iGAbTJa29sn9VNdJ5Z1kV17ls5O5d0TkINSaSwBg=w1440)

Visualisation of which turtle head regions a neural network pays attention to when making its predictions of which individual is in the photo. Left: A turtle's face from the dataset. Middle/Right: activations from DenseNet121 and EfficientNetB5 on the same image. Credit: Zindi and Zindi discussion board user ZFTurbo.

The competition started in November 2021 and lasted five months. To encourage competitor participation, the team implemented a [colab notebook](https://research.google.com/colaboratory/), an in-browser programming environment, which introduced two common programming tools: [JAX](https://deepmind.google/blog/using-jax-to-accelerate-our-research/) and [Haiku](https://en.wikipedia.org/wiki/Haiku_(operating_system)#:~:text=Haiku%20is%20written%20in%20C,provides%20an%20object%2Doriented%20API.).

Participants were tasked with downloading the challenge data and training models to predict a turtle’s identity, as accurately as possible, given a photograph taken from a specific angle. Having submitted their predictions on data withheld from the model, they were able to visit a public leaderboard tracking the progress of each participant.

The community engagement was incredibly positive, and so was the technical innovation displayed by teams during the challenge. During the course of the competition, we received submissions from a diverse range of AI enthusiasts from 13 different African countries – including countries not traditionally well represented at the biggest ML conferences, such as Ghana and Benin.

Our turtle conservation partners have indicated that the participant’s level of prediction accuracy will be immediately useful for identifying turtles in the field, meaning that these models can have a real and immediate impact on wildlife conservation.

As part of Zindi’s continued efforts to support climate-positive challenges, they are also working on [Swahili audio classification](https://zindi.africa/competitions/swahili-audio-classification) in Kenya to help translation and emergency services, and [air quality prediction](https://zindi.africa/competitions/layerai-air-quality-prediction-challenge) in Uganda to improve social welfare.

We're grateful to Zindi for their partnership, and all those who contributed their time to the Turtle Recall challenge and the growing field of AI for conservation. And we look forward to seeing how people around the world continue to find ways to apply AI technologies towards building a healthy, sustainable future for the planet.

Read more about Turtle Recall on [Zindi’s blog](https://zindi.medium.com/facial-recognition-for-turtles-how-crowd-sourced-ai-can-help-marine-conservation-efforts-6bc7a69e6712) and learn about Zindi at <https://zindi.africa/>
