---
title: "Reconstructing Pelé’s “lost” goal"
source: https://blog.google/innovation-and-ai/models-and-research/google-deepmind/reconstructing-peles-lost-goal/
site: google-blog
date: 2026-07-14
authors: Anita Lucchesi
crawled: 2026-09-13
---

On August 2, 1959, Pelé scored the most beautiful goal of his career: three consecutive “sombreros” over defenders and the goalkeeper without the ball ever touching the ground. But the moment was never captured on film.

For over 60 years, the legendary "Gol da Rua Javari" lived in the memories of the fans who were there. Now, in collaboration with Pelé’s family, historians, sports journalists and football legends, we used Google DeepMind technology to reconstruct this piece of football history. The work was created in full partnership with Pelé Brand, the platform responsible for preserving, protecting and expanding Pelé’s legacy, under the leadership of NR Sports.

The “Gol da Rua Javari” reconstruction is presented as a mini-documentary that features interviews with the historians, journalists, Pelé’s family, eyewitnesses and football legends with whom we worked to tell the story of an incredible moment in football history.

“He would be so proud to see all this happening. He’d always say it was a shame that the goal was never recorded. So being able to relive it, with all this technology, is amazing." — Flávia Kurtz, Pelé’s Daughter

![Black and white composite photo of Pelé and his daughter looking proudly at him](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Pele_Keyword_047.width-1200.format-webp.webp)

## Piecing together a legend

To get the history exactly right, Brazilian historian Anita Lucchesi and her team gathered nearly 2,000 historical records — from blueprints to family albums. They interviewed eyewitnesses, journalists and the Mooca community, using a scale model of the stadium, archival photographs and diagrams to help those who saw the goal reconstruct it from memory.

Over 3,600 historical images were gathered to accurately reconstruct the goal.

![Black and white photo of the famous goal](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Pele_Keyword_002.width-100.format-webp.webp)

Historical photograph of the “Gol da Rua Javari”, taken on August 2nd, 1959.

![Color image of a historian speaking to the camera](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Pele_Keyword_003.width-100.format-webp.webp)

Anita Lucchesi, Historian, UERJ & Arka

![Old historical materials about the famous goal](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Pele_Keyword_004.width-100.format-webp.webp)

Archival fragments: newspapers, maps, blueprints and family albums

![Black and white photo of people playing soccer in Brazil](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Pele_Keyword_005.width-100.format-webp.webp)

Historical photograph of the “Estádio da Rua Javari” in the Mooca neighborhood, São Paulo.

![Black and white image of soccer team members in Brazil](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Pele_Keyword_007.width-100.format-webp.webp)

Members of the Juventus team and staff at the Javari Street Stadium.

![Hand pointing to a photograph in a book](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Pele_Keyword_008.width-100.format-webp.webp)

Photograph of the Juventus team in 1959

![Old newspaper clipping with the text "Gooool" and a diagram of the goal.](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Pele_Keyword_010.width-100.format-webp.webp)

Newspaper report of the match and diagram of the goal

## Going from the pitch to pixels

Recreating this goal required a combination of practical filmmaking and our most advanced AI models: Veo, Gemini Omni and Nano Banana Pro.

First, our crew shot live-action footage right on the grass of the Rua Javari stadium, using heavy leather balls and period-accurate uniforms. This physical foundation was then fed into our models to begin the digital transformation. We focused on three core technical experiments:

- **Character replacement:** Accurately mapping Pelé's likeness and his classic number 10 kit onto a modern stunt player.
- **Environment restyling:** Transforming the modern stadium to match the cloudy weather and architecture of that specific day.
- **Generating the ambiance:** showing how fans watching the match at the stadium and listening to the radio broadcast at home experienced the moment.

![Side by side image of the original shoes and the digital recreation](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Pele_Keyword_034.width-100.format-webp.webp)

Pelé’s original cleats from 1959. Archival photographs and artifacts served as the basis for all AI-generated scenes, ensuring historical accuracy across the film.

![Side by side image of an original photograph and a digital recreation](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Pele_Keyword_028.width-100.format-webp.webp)

Raphael Herrera, photographer at Javari Stadium in 1959

![Side by side images of two elderly men and digital recreations of their younger selves](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Pele_Keyword_030.width-100.format-webp.webp)

Angelo Agarelli and Vicente Romano Netto, Juventus’ fans and eyewitnesses of the goal at Javari.

![Side by side images of a crowd photo and a digital recreation](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Pele_Keyword_033.width-100.format-webp.webp)

Crowds packing Javari Stadium during a Juventus match

## Balancing photorealism with performance control

While generative models excel at photorealism, the extreme athletic choreography of a legend like Pelé presents a unique challenge. To solve this, we used Performance Control — an approach based on Veo 3 that extracts precise 3D geometry and motion from a modern stunt player to drive video generation. By pairing this with complementary workflows that use Nano Banana Pro and Gemini Omni, we generated a final video that seamlessly brings together the stadium architecture, field conditions, Pelé’s likeness and the dynamic play.

Starting with the original live-action video (top-left), we break the scene into separate, editable layers. We capture the athletes' exact 3D motion (top-right), isolate them from the scenery (bottom-left), and generate a clean background without them (bottom-right). This allows us to modify the players and the environment independently.

![Image of a laptop showing different stages of animation](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Pele_Keyword_035_1.width-100.format-webp.webp)

To streamline editing, VFX, and video generation, Gemini Omni and Veo isolated actor footage, extracted the background and generated 3D blue-mesh player movement representations.

Performance Control creates editable 3D blue mesh renderings from an input video, modifiable using reference images.

## Building a hybrid post-production pipeline

To achieve the final polish, we built a hybrid pipeline that combined AI generation with traditional visual effects (VFX). Using custom internal tools, we further refined the AI-generated shots with Gemini Omni and Nano Banana Pro, relying on archival imagery to ensure every detail was accurate. The workflow then moved to traditional VFX for tasks like ball compositing, grain integration, and rigorous color balancing. To ensure the generations looked as period accurate as possible, we ran the digital output through a filmout machine, capturing the distinct look and feel of 1950s cinema.

## Making the invisible, visible

Nothing can substitute the experience of the fans who were there live, but we hope this project gives new life to an iconic moment in football history.

This goal reconstruction is now proudly on display at the Pelé Museum in Santos.

Museu Pelé, Santos SP, Brazil

![Picture of a child in a Pele jersey at the museum](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Pele_Keyword_038.width-1200.format-webp.webp)
