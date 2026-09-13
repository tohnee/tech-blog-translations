---
title: "Exploring the context of online images with Backstory"
source: https://deepmind.google/blog/exploring-the-context-of-online-images-with-backstory/
site: deepmind
date: 2025-07-21
authors: Avneesh Sud, Chris Bregler
crawled: 2026-09-13
---

New experimental AI tool helps people explore the context and origin of images seen online.

The ways people are using and interacting with images online is constantly evolving. Last year, we published a paper on [determining trustworthiness through context and provenance](https://static.googleusercontent.com/media/publicpolicy.google/en//resources/determining_trustworthiness_en.pdf), showing how better assessment tools can empower people to make informed decisions about what they’re seeing on the internet.

As part of our efforts to help people make informed choices, we’re developing easy-to-use provenance tools and in-product context features, and investing in areas like [information literacy](https://beinternetlegends.withgoogle.com/en_uk).

Today, we’re introducing Backstory, an experimental artificial intelligence (AI) tool that surfaces information and helps people learn more about the context of images seen online.

When given an image and a written prompt, Backstory investigates whether an image was AI-generated, when and where it’s previously been used online, and whether it’s been digitally altered. It quickly equips users with helpful information, responds to further prompts, describes whether and how an image has been used, and how its story may have changed over time. Backstory also generates easy-to-read reports of its findings.

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

## Assessing trustworthiness through context and origin

Built using [Gemini](https://deepmind.google/models/gemini/?_gl=1*v8kbv3*_up*MQ..*_ga*Njc2NDM5MzkxLjE3NTE4ODYzMTk.*_ga_LS8HVHCNQ0*czE3NTE4ODYzMTgkbzEkZzAkdDE3NTE4ODYzMTgkajYwJGwwJGgw), Backstory draws on a number of detection technologies designed to identify whether an image is real or created using generative AI. Backstory then combines this with a more holistic assessment of the context of the image. It surfaces how the image has been used on the internet and other information like metadata to help answer the user's written prompt.

In most cases, determining whether an image is AI-generated is not the same as understanding if it’s trustworthy. For example, an image may not be AI-generated, but could have been altered or presented out of context — resulting in new, sometimes misleading, information.

Alternatively, an image generated using AI may support an authentic, creative or factual story. Accurately assessing the trustworthiness of an image often requires more knowledge of how the image was created, and a deeper understanding of the context surrounding it.

## Taking a holistic approach

It’s crucial that industry, civil society, governments, academics and users work together to develop and refine the tools and programs necessary for maintaining the integrity of our information ecosystem.

As we continue to conduct research and develop Backstory, we’re working closely with trusted testers, including content creators and expert information practitioners, who manage, organize and disseminate high quality information.

Throughout the year, we’ll gather feedback about examples, user experiences and more to improve our technology and make it more helpful.

**Explore Backstory**

[Register interest in Backstory](https://forms.gle/3eGVzNJQRAyc7aPu5)

**Acknowledgements**

We would like to thank Zoubin Ghahramani, Helen King, Rahul Sukthankar, Raia Hadsell, and Chandu Thota for their leadership and support.

This work was done thanks to the contributions of Mevan Babakar, Hannah Forbes-Pollard, Nikki Hariri, Thomas Leung, Nick Dufour, Ben Usman, Min Ma, Steve Pucci, Spudde Childs, Kate Harrison, Alanna Slocum, Reza Aghajani, Sri Rajendran, Alexey Vorobyov, Ashley Eden, Rishub Jain, Stephanie Chan, Sophie Bridgers, Michiel Bakker, Sures Kumar Thoddu Srinivasan, Tesh Goyal, and Ashish Chaudhary.

We would also like to thank Kent Walker, Camino Rojo, Clement Wolf, J.D. Velazquez, Tom Lue, Ndidi Elue, Rachel Stigler, M.H. Tessler, Ricardo Prada, William Isaac, Tom Stepleton, Zoe Darme, Gail Kent, Vincent Ryan, Aaron Donsbach, Abhishek Bapna, Verena Rieser, Christian Plagemann, Anca Dragan, Joelle Barral, Edward Grefenstette, Sara Mahdavi, Sven Gowal, Florian Stimberg, Christopher Savcak, Allison Garcia, Eve Novakovic, Armin Senoner, Arielle Bier, and the greater Google DeepMind and Google teams for their support, help, and feedback.
