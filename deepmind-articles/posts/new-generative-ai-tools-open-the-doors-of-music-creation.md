---
title: "New generative AI tools open the doors of music creation"
source: https://deepmind.google/blog/new-generative-ai-tools-open-the-doors-of-music-creation/
site: deepmind
date: 2024-10-23
authors: GenMedia Music team
crawled: 2026-09-13
---

**Note (May 1, 2025):** These tools are now powered by [Lyria](https://deepmind.google/models/lyria/) and [Lyria RealTime](https://deepmind.google/models/lyria/lyria-realtime/), the music generation models developed by Google DeepMind.

Our latest AI music technologies are now available in MusicFX DJ, Music AI Sandbox and YouTube Shorts

For nearly a decade, our teams have been exploring [how artificial intelligence (AI) can support the creative process](https://magenta.withgoogle.com/blog/2016/06/01/welcome-to-magenta/), building tools that empower enthusiasts and professionals to discover new forms of creative expression.

Over the past year, we’ve been working in close collaboration with partners across the music industry through our [Music AI Incubator](https://blog.youtube/inside-youtube/partnering-with-the-music-industry-on-ai/) and more. Their input has been guiding our state-of-the-art generative music experiments, and helping us ensure that our new generative AI tools responsibly open the doors of music creation to everyone.

Today, in partnership with [Google Labs](https://blog.google/technology/ai/jacob-collier-labs-sessions), we're releasing a reimagined experience for [MusicFX DJ](http://labs.google/musicfx) that makes it easier for anyone to generate music, interactively, in real time.

We’re also announcing updates to our music AI toolkit, called [Music AI Sandbox](https://blog.google/technology/ai/google-generative-ai-veo-imagen-3/), and highlighting our latest AI music technologies in [YouTube’s Dream Track](https://deepmind.google/discover/blog/transforming-the-future-of-music-creation/), a suite of experiments that creators can use to generate high-quality instrumentals for their Shorts and videos.

## Generating live music with MusicFX DJ

At I/O this year, we shared an [early preview of MusicFX DJ](https://blog.google/technology/ai/google-labs-video-fx-generative-ai/), a digital tool that anyone can play like an instrument, making the joy of live music creation more accessible to people of all skill levels.

Today, we’re introducing a number of updates to MusicFX DJ, including an expanded set of intuitive controls, a reimagined interface, improved audio quality and new model behaviors. These capabilities let players generate and steer a continuous flow of music, share their creations with friends and play a jam session together.

Working in close collaboration with [Jacob Collier](https://www.youtube.com/watch?v=y7gKlzvg8xk&feature=youtu.be) — a six-time GRAMMY award-winning singer, songwriter, producer and multi-instrumentalist — we designed these updates to make MusicFX DJ more accessible, useful and inspiring.

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

Unlike traditional DJ tools that mix together preexisting tracks, MusicFX DJ generates brand new music by allowing players to mix musical concepts as text prompts. With MusicFX DJ, players can combine their favorite genres, instruments and vibes to create new styles, improvise a live DJ set or search for new melodies, timbres and rhythms to use in production.

While not a traditional musical instrument, MusicFX DJ is an accessible and expressive entry point to live music creation. Regardless of one’s musical experience, MusicFX DJ empowers players with intuitive controls to generate and steer a unique and continuously evolving musical soundscape.

> You craft this real-time sonic putty that’s endlessly surprising and essentially seeks to alchemize or forge connections between things that would otherwise be unlikely.

Jacob Collier

Two novel approaches underpin MusicFX DJ. First, we adapted an offline generative music model to perform real-time streaming. We did this by training it to generate the next clip of music, based on the previous generated music and the text prompts provided by the player.

Second, instead of having a single fixed text prompt, like typical text-to-music models, we give players the ability to mix together multiple text prompts and change the mixture over time. The model achieves this by mixing together representations of each prompt, known as embeddings, with the relative importance of each embedding, chosen by the player using a slider. The model uses these combined embeddings to help steer the style of music.

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

Flowchart showing how MusicFX DJ generates a continuous flow of music, creating the next clip from previous clips, while steered by the text prompts and sliders to weight their importance.

### Building more intuitive controls

Together with Jacob, we looked to discover and build dedicated controls that could be intuitive to beginners, encourage experimentation and provide more diverse routes to creative expression than text prompts alone.

With MusicFX DJ’s new controls, players can conduct the instrumentation and easily create breakdowns and bass drops by removing and adding the bass, drums and other instruments. They can adjust textural aspects of the music, like how bright or dark, repetitive or random and smooth or rough it should sound and feel.

Players can also control key and tempo, making it easier to play along with existing music and with others during extended jam sessions. Our teams have really enjoyed using MusicFX DJ alongside their traditional instruments, and we can’t wait to hear what others create with these new capabilities.

Slide 1 of 4

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

### Generating production-quality sound

As part of the collaboration, we also explored how a player could use the model output as both a source of inspiration and as part of a large composition. But our earlier models lacked the quality needed for creating professional audio. Thanks to the latest innovations from our audio research team, including new neural audio codecs and optimized network architectures, MusicFX DJ is now able to stream production-quality 48 kHz stereo audio in real time.

### Sharing and downloading audio

Inspired by Jacob’s focus on creative collaboration, both [with other artists](https://www.npr.org/2024/04/01/1198910485/jacob-collier-album-djesse-volume-four) and [with his audiences](https://www.youtube.com/watch?v=3KsF309XpJo), we wanted to make it easier to share and interact with music made with MusicFX DJ. Players can now download 60 seconds of their MusicFX DJ audio and share sessions with friends, who can watch a performance playback and even jump in to take over the controls at any point — taking the music in an entirely new direction.

## An expanded Music AI Sandbox toolkit

[Music AI Sandbox](https://blog.google/technology/ai/google-generative-ai-veo-imagen-3/) is an experimental suite of music AI tools that aims to supercharge the workflows of musicians, producers and songwriters who collaborate with us through YouTube’s [Music AI Incubator](https://blog.youtube/inside-youtube/partnering-with-the-music-industry-on-ai/). It has been a valuable testing ground for gathering feedback from diverse artists, songwriters and partners across the music industry about our latest and most experimental generative music tools. While the Music AI Sandbox isn’t currently publicly available, successful elements of this work will be integrated into widely-accessible Google products.

Since showing the Music AI Sandbox publicly at this year’s I/O, we’ve also been working closely with [Google’s Technology & Society team](https://blog.google/technology/ai/artist-refik-anadol-ai-creativity-google/) to improve the user experience and connect with the artistic community at scale to gather feedback. This work has helped us make significant updates to the models behind this suite of tools.

Soon, trusted testers will be able to sketch a song and use a multi-track view to help organize and refine compositions with precise controls. This new version of Music AI Sandbox integrates our latest technologies, including models that power MusicFX DJ, along with popular features like loop generation, sound transformation and in-painting to help users seamlessly connect parts of their musical tracks.

![A screenshot of the user interface designs for our updated Music AI Sandbox, which has a multi-track view to help organize and refine compositions with precise controls.](https://lh3.googleusercontent.com/otfaldHsOzIe3YZYbnTgqhSfJFWRFpe0yQqvaou4XM2_4vmpzbcjHppFKF9mV2n5V6qcjvqycTK2FMxe7UCzpOtfPon7YDtIi5aLWLzdg5mVn7LFLg=w1440)

Screenshot of user interface designs for our updated Music AI Sandbox, which has a multi-track view to help organize and refine compositions with precise controls.

## YouTube's Dream Track experiment now generates instrumental soundtracks

Building off our ongoing work with YouTube, we’ve evolved our [Dream Track experiment](https://blog.youtube/inside-youtube/ai-and-music-experiment/) to allow U.S. creators to explore a range of genres and prompts that generate instrumental soundtracks with powerful text-to-music models.

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

Our latest music generation models are trained with a novel reinforcement learning approach to have higher audio quality, while also paying better attention to the nuances of a user’s text prompts. Responsibly deploying generative technologies is core to [our values](https://ai.google/responsibility/principles/), so all music generated by MusicFX DJ and Dream Track is watermarked using [SynthID](https://deepmind.google/technologies/synthid/).

## Building the future of music creation together

We’ve been delighted to work with partners in the music community over the past year to help build technology that's both responsive to the needs of professionals and expands access for the next generation of musicians.

We’re looking forward to deepening these partnerships as we build the future of music creation together, developing even better tools to inspire creativity.

[Try MusicFX DJ](http://labs.google/musicfx)[Watch our Lab Sessions video with Jacob Collier](https://www.youtube.com/watch?v=y7gKlzvg8xk&feature=youtu.be)[Read more about Music AI Sandbox](https://deepmind.google/blog/transforming-the-future-of-music-creation/)

This work was made possible by core research and engineering efforts from Andrea Agostinelli, Zalán Borsos, George Brower, Antoine Caillon, Cătălina Cangea, Noah Constant, Michael Chang, Chris Deaner, Timo Denk, Chris Donahue, Michael Dooley, Jesse Engel, Christian Frank, Beat Gfeller, Tobenna Peter Igwe, Drew Jaegle, Matej Kastelic, Kazuya Kawakami, Pen Li, Ethan Manilow, Yotam Mann, Colin McArdell, Brian McWilliams, Adam Roberts, Matt Sharifi, Ian Simon, Ondrej Skopek, Marco Tagliasacchi, Cassie Tarakajian, Alex Tudor, Victor Ungureanu, Mauro Verzetti, Damien Vincent, Luyu Wang, Björn Winkler, Yan Wu, and Mauricio Zuluaga.

MusicFX DJ was developed by Antoine Caillon, Noah Constant, Jesse Engel, Alberto Lalama, Hema Manickavasagam, Adam Roberts, Ian Simon, and Cassie Tarakajian in collaboration with our partners from Google Labs including Obed Appiah-Agyeman, Tahj Atkinson, Carlie de Boer, Phillip Campion, Sai Kiran Gorthi, Kelly Lau-Kee, Elias Roman, Noah Semus, Trond Wuellner, Kristin Yim, and Jamie Zyskowski. We give our deepest thanks to Jacob Collier, Ben Bloomberg, and Fran Haincourt for their valuable feedback throughout the development process.

Music AI Sandbox was developed by Andrea Agostinelli, George Brower, Ross Cairns, Michael Chang, Yeawon Choi, Chris Deaner, Jesse Engel, Reed Enger, Beat Gfeller, Tom Hume, Tom Jenkins, Max Edelmann, Drew Jaegle, Jacob Kelly, DY Kim, David Madras, Hema Manickavasagam, Ethan Manilow, Yotam Mann, Colin McArdell, Chris Reardon, Felix Riedel, Adam Roberts, Arathi Sethumadhavan, Eleni Shaw, Sage Stevens, Amy Stuart, Luyu Wang, Pawel Wluka, and Yan Wu in collaboration with our partners in YouTube and Tech & Society.

Dream Track was developed by Andrea Agostinelli, Zalán Borsos, Geoffrey Cideron, Timo Denk, Michael Dooley, Christian Frank, Sertan Girgin, Myriam Hamed Torres, Matej Kastelic, Pen Li, Brian McWilliams, Matt Sharifi, Ondrej Skopek, Marco Tagliasacchi, Mauro Verzetti, Mauricio Zuluaga, in collaboration with our partners in YouTube.

Special thanks to Aäron van den Oord, Tom Hume, Douglas Eck, Eli Collins, Mira Lane, Koray Kavukcuoglu, and Demis Hassabis for their insightful guidance and support throughout the research process. Thanks to Mahyar Bordbar and DY Kim for helping coordinate these efforts, as well as the YouTube Artist Partnerships team for their support partnering with the music industry.

We also acknowledge the many other individuals who contributed across Google DeepMind and Alphabet, including our partners at YouTube.
