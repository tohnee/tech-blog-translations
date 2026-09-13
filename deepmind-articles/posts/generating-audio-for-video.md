---
title: "Generating audio for video"
source: https://deepmind.google/blog/generating-audio-for-video/
site: deepmind
date: 2024-06-17
authors: Generative Media team
crawled: 2026-09-13
---

Video-to-audio research uses video pixels and text prompts to generate rich soundtracks

Video generation models are advancing at an incredible pace, but many current systems can only generate silent output. One of the next major steps toward bringing generated movies to life is creating soundtracks for these silent videos.

Today, we're sharing progress on our video-to-audio (V2A) technology, which makes synchronized audiovisual generation possible. V2A combines video pixels with natural language text prompts to generate rich soundscapes for the on-screen action.

Our V2A technology is pairable with video generation models like [Veo](https://deepmind.google/technologies/veo/) to create shots with a dramatic score, realistic sound effects or dialogue that matches the characters and tone of a video.

It can also generate soundtracks for a range of traditional footage, including archival material, silent films and more — opening a wider range of creative opportunities.

Prompt for audio: Cinematic, thriller, horror film, music, tension, ambience, footsteps on concrete

Prompt for audio: Cute baby dinosaur chirps, jungle ambience, egg cracking

Prompt for audio: Jellyfish pulsating under water, marine life, ocean

Prompt for audio: A drummer on a stage at a concert surrounded by flashing lights and a cheering crowd

Prompt for audio: Cars skidding, car engine throttling, angelic electronic music

Prompt for audio: A slow mellow harmonica plays as the sun goes down on the prairie

Prompt for audio: Wolf howling at the moon

## Enhanced creative control

Importantly, V2A can generate an unlimited number of soundtracks for any video input. Optionally, a ‘positive prompt’ can be defined to guide the generated output toward desired sounds, or a ‘negative prompt’ to guide it away from undesired sounds.

This flexibility gives users more control over V2A’s audio output, making it possible to rapidly experiment with different audio outputs and choose the best match.

Prompt for audio: A spaceship hurtles through the vastness of space, stars streaking past it, high speed, Sci-fi

Prompt for audio: Ethereal cello atmosphere

Prompt for audio: A spaceship hurtles through the vastness of space, stars streaking past it, high speed, Sci-fi

## How it works

We experimented with autoregressive and diffusion approaches to discover the most scalable AI architecture, and the diffusion-based approach for audio generation gave the most realistic and compelling results for synchronizing video and audio information.

Our V2A system starts by encoding video input into a compressed representation. Then, the diffusion model iteratively refines the audio from random noise. This process is guided by the visual input and natural language prompts given to generate synchronized, realistic audio that closely aligns with the prompt. Finally, the audio output is decoded, turned into an audio waveform and combined with the video data.

![Diagram of the V2A technology workflow, showing input video pixels and text prompts (positive and negative) processed through encoders, a diffusion model, and a decoder to generate an audio waveform.](https://lh3.googleusercontent.com/4UXuyvSiMGMU26kS2cFxP-1bl40KD8QOsGF_XquqUPAJ-5xq8wCrT00ioneRu0EhOuRsE0iJ3tjLCDpBLtKOeGe4bt9rv6DS2QZ2q97zcRaBuKeFzc0=w1440)

Diagram of our V2A system, taking video pixel and audio prompt input to generate an audio waveform synchronized to the underlying video. First, V2A encodes the video and audio prompt input and iteratively runs it through the diffusion model. Then it generates compressed audio, which is decoded into an audio waveform.

To generate higher quality audio and add the ability to guide the model towards generating specific sounds, we added more information to the training process, including AI-generated annotations with detailed descriptions of sound and transcripts of spoken dialogue.

By training on video, audio and the additional annotations, our technology learns to associate specific audio events with various visual scenes, while responding to the information provided in the annotations or transcripts.

## Further research underway

Our research stands out from existing video-to-audio solutions because it can understand raw pixels and adding a text prompt is optional.

Also, the system doesn't need manual alignment of the generated sound with the video, which involves tediously adjusting different elements of sounds, visuals and timings.

Still, there are a number of other limitations we’re trying to address and further research is underway.

Since the quality of the audio output is dependent on the quality of the video input, artifacts or distortions in the video, which are outside the model’s training distribution, can lead to a noticeable drop in audio quality.

We’re also improving lip synchronization for videos that involve speech. V2A attempts to generate speech from the input transcripts and synchronize it with characters' lip movements. But the paired video generation model may not be conditioned on transcripts. This creates a mismatch, often resulting in uncanny lip-syncing, as the video model doesn’t generate mouth movements that match the transcript.

![](https://lh3.googleusercontent.com/_i0NHcAzCbB1pjGV06l3eqe3B0nOYEdQGWNLWivwqVaNFtcemyRdwZNFiRg8bkliL50WNwpxSTV5lL_bJGt80dvaByTTOZXHuuB8KESlqZJTgHBf6A=w1440-h810-n-nu)

Prompt for audio: Music, Transcript: “this turkey looks amazing, I’m so hungry”

## Our commitment to safety and transparency

We’re committed to developing and deploying AI technologies responsibly. To make sure our V2A technology can have a positive impact on the creative community, we’re gathering diverse perspectives and insights from leading creators and filmmakers, and using this valuable feedback to inform our ongoing research and development.

We’ve also incorporated our [SynthID](https://deepmind.google/technologies/synthid/) toolkit into our V2A research to watermark all AI-generated content to help safeguard against the potential for misuse of this technology.

Before we consider opening access to it to the wider public, our V2A technology will undergo rigorous safety assessments and testing. Initial results are showing this technology will become a promising approach for bringing generated movies to life.

Note: All examples are generated by our V2A technology, which is paired with [Veo](https://deepmind.google/technologies/veo/), our most capable generative video model.

[Learn about Veo](https://deepmind.google/models/veo/)[Explore our SynthID toolkit](https://deepmind.google/models/synthid/)

**Acknowledgements**

This work was made possible by the contributions of: Ankush Gupta, Nick Pezzotti, Pavel Khrushkov, Tobenna Peter Igwe, Kazuya Kawakami, Mateusz Malinowski, Jacob Kelly, Yan Wu, Xinyu Wang, Abhishek Sharma, Ali Razavi, Eric Lau, Serena Zhang, Brendan Shillingford, Yelin Kim, Eleni Shaw, Signe Nørly, Andeep Toor, Irina Blok, Gregory Shaw, Pen Li, Scott Wisdom, Aren Jansen, Zalán Borsos, Brian McWilliams, Salah Zaiem, Marco Tagliasacchi, Ron Weiss, Manoj Plakal, Hakan Erdogan, John Hershey, Jeff Donahue, Vivek Kumar, and Matt Sharifi.

We extend our gratitude to Benigno Uria, Björn Winckler, Charlie Nash, Conor Durkan, Cătălina Cangea, David Ding, Dawid Górny, Drew Jaegle, Ethan Manilow, Evgeny Gladchenko, Felix Riedel, Florian Stimberg, Henna Nandwani, Jakob Bauer, Junlin Zhang, Luis C. Cobo, Mahyar Bordbar, Miaosen Wang, Mikołaj Bińkowski, Sander Dieleman, Will Grathwohl, Yaroslav Ganin, Yusuf Aytar, and Yury Sulsky.

Special thanks to Aäron van den Oord, Andrew Zisserman, Tom Hume, RJ Mical, Douglas Eck, Nando de Freitas, Oriol Vinyals, Eli Collins, Koray Kavukcuoglu and Demis Hassabis for their insightful guidance and support throughout the research process.

We also acknowledge the many other individuals who contributed across Google DeepMind and our partners at Google.
