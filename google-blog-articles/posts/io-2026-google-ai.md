---
title: "How we used Gemini to build Google I/O 2026"
source: https://blog.google/innovation-and-ai/technology/ai/io-2026-google-ai/
site: google-blog
date: 2026-06-01
authors: Marvin Chow
crawled: 2026-09-13
---

[Google I/O 2026](https://blog.google/innovation-and-ai/technology/developers-tools/google-io-2026-collection/) was all about how we’re making AI helpful for everyone in new ways. But we didn’t just make announcements about our innovations in AI at I/O — we used those tools to bring I/O to life, too.

It’s both a strange and exciting moment to be building anything. We're living through an incredible shift where AI tools are getting better each month, effectively rewriting the rules of what we can create.

This year, we challenged ourselves to use the same AI we were putting on stage to out-innovate, out-create and out-efficient ourselves.

We moved faster than ever and prototyped in real-time — blending human artistry with experimental technology — with no better example than the "Timmy TPU" film.

But the reward is showing how these tools unlock creativity and offload the mundane tasks, giving the team their best hours back for the parts they are uniquely suited to do. When done right, the event is amazing on its own, and, as a viewer, you stop thinking about how AI was used. That shift is the opportunity we want to share, because people keep asking, “What can you really do with AI?”

Keep reading to learn which AI tools we used — and how we prompted them — to help make I/O 2026 happen.

### “TPU Training Day” short film

**The AI products & models:** Google AI Studio; experimental DeepMind models; Gemini Omni; Nano Banana

**What we did:** We created a short film starring a bunch of TPUs getting ready to do some heavy lifting for I/O 2026.

**How we did it:** This project started with a question: Could we make an animated film with the simplest materials — cardboard and markers — and then use AI to bring it to life? We worked with director Laurie Rowan and Nexus Studios to blend puppets, traditional animation and AI — keeping human craft and artistry right at the heart of "TPU Training Day" (also known as "Timmy TPU").

First, we captured character performances through puppetry and simple 3D animation. This gave us full control over framing and camera movement. We then used Nano Banana to generate stylized first frames from that raw footage. To keep frames consistent, we built a custom tool inside Google AI Studio. This let us test Nano Banana frames at scale, ensuring pixel-perfect matches before generating sequences.

We merged the base animation and stylized frames using Gemini Omni and other experimental models. This elevated the film to a cinematic level while retaining the original human intent. Preserving these tiny, human imperfections is what gives puppet films their charm, and our AI pipelines were designed to protect those details.

### I/O visual brand identity

![The words I/O surrounded by related icons, all in rainbow colors, against a white background](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Collection-Hero.width-1200.format-webp.webp)

**The AI products & models:** Gemini models and Nano Banana

**What we did:** We created the visual brand identity for I/O 2026, landing on a four-color gradient with overlapping transparencies and interlocking icons.

**How we did it:** Our brand identity was a close collaboration between our team and AI. We started by feeding Gemini models our past brand guidelines and five years of I/O recaps. The early outputs didn't quite hit the mark, so we ran some micro-experiments. We generated new imagery and iteratively fed outputs back into Nano Banana with feedback. We also used Nano Banana to explore icon styles. Finally, we landed on flat 2D icons that dynamically transform into hyper-textured 3D icons. This created a cohesive brand expression across keynotes, physical signage and digital apps.

Here’s a prompt we used to explore icon styles with Nano Banana:

```ts
You are an expert image editor. You will be given two images.

**Image 1** provides the **texture and material**.

**Image 2** provides the **pose, shape, and lighting**.

Your task is to create a new image by applying the detailed texture 
and pattern from the icon in **Image 1** onto the surface 
of the white icon in **Image 2**.

**Crucial Constraint:** The output image must perfectly preserve
the exact pose, camera angle, scale, and lighting 
of the icon in **Image 2**. Do not change its orientation 
or position in any way. The final result should be the 
icon from Image 2, but with the texture of Image 1.
```

Our I/O YouTube trailer showcased our final icon style:

### The I/O pre-show: Jellectronica

**The AI products & models:** Google Antigravity; Google Colab; Google CoralNPU; Google Flow Music; Lyria 3 Pro

**What we did:** We kicked off the pre-show with Jellectronica, a generative music experiment in partnership with the Monterey Bay Aquarium that translated moon jelly movements into sound with Lyria 3 Pro.

**How we did it:** We trained a YOLO8 model in Google Colab, and then ran it on Google’s Coral NPU. This tracked jellyfish movement to control the music, which was made using Google Flow Music and the Lyria API. For example, more jellies in the bass section meant louder, more energetic bass. We also vibe-coded a mass stem generator in Google Antigravity to automate the production of music stems, like bass, chords, melody and drums.

### The I/O pre-show: Infinite Scaler and Code the Countdown

**The AI products & models:** Google AI Studio; Gemini API; Gemini Canvas; Google Antigravity; Lyria 3; Nano Banana

**What we did:** Infinite Scaler, another part of the pre-show, was a video game where players competed and generated the levels as they played.

**How we did it:** We wanted players to build infinite 3D worlds quickly just using 2D image generation. To do this, we used Nano Banana to generate sprite sheets from user prompts and reference images via the Gemini API. We sent foreground elements back to Nano Banana to generate normal, roughness and emission maps. This inferred depth, letting us map textures to a 3D cardboard box rendered in WebGL before adding them to the global stack of worlds. We used Google AI Studio for rapid prototyping before moving to Google Antigravity for development; we generated in-game music entirely using Lyria 3.

You can [play the game and explore the levels we built together here](http://infinitescaler.withgoogle.com/).

Here’s a sample user prompt for Infinite Scaler:

```ts
A majestic space fox levitating in space with a giant 
Saturn and stars behind
```

Feeding that back into the Gemini API for a level plan gave us this prompt:

```ts
Title: Celestial Fox Void

Color Palette: Deep navy and midnight blue backdrop, vibrant burnt
orange and dusty terracotta for the fox, soft cream and muted amber 
for Saturn rings, and deep plum shadows. All greens are replaced with 
dull, earthy dark olive tones to avoid #00FF00 interference.
    
Skyline: A vast expanse of midnight blue clay textured with dense
constellations of white and pale yellow spherical stars of varying sizes.

Sky panel: Deep indigo clay surface scattered with clusters of tiny 
white bead-like stars, creating a dense celestial field without
any bright green elements.

Floor panel: A flat plane of deep violet cosmic dust sculpted with
smooth, rounded craters and soft-molded ridges, keeping all surfaces 
matte and non-reflective.

Decorations Arch: A massive, perfectly spherical Saturn dominates the 
upper sector with thick, concentric ring layers made of hand-pressed tan 
and cream clay coils.

Decorations Ground: A majestic fox with flowing clay-sculpted fur
levitates at the center, surrounded by floating, multi-sized clay
asteroids and small, irregular space debris particles.
```

That prompt resulted in this sprite sheet. The game’s sprite sheets combined multiple elements in a consistent template that used green screen backgrounds for easy masking.

![Sprite sheet showing various images including a fox and Saturn against a lime green background](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/fox-sprite.width-1200.format-webp.webp)

This process resulted in a fully playable 3D level like this:

Finally, we played a generated countdown coded by creators worldwide in our Code the Countdown challenge. [We asked you](https://x.com/googledevs/status/2050245538730168343) to design numbers between 1 and 10 in Canvas or AI Studio, then stitched them into a countdown powered by code.

### Antigravity Coffee Co. pop-up

![Antigravity Coffee Co. pop-up at I/O](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Antigravity_Coffee_Co..width-100.format-webp.webp)

![Intricate latte art of a bicycle at Antigravity Coffee Co.](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Antigravity_Coffee_Co._2.width-100.format-webp.webp)

**The AI products & models:** Flutter; Gemini Enterprise Agent Platform; Google Antigravity; Nano Banana

**What we did:** We created an app for I/O attendees to design and order lattes with custom art, then build their own version of the most unhinged coffee app ever.

**How we did it:** We used generative UI and the A2UI protocol with Flutter to build adaptive interfaces that changed in real-time. This replaced static forms with dynamic user interactions. Firebase bridged the frontend to models like Nano Banana. This handled complex reasoning and content generation. A single Flutter codebase delivered a high-quality, zero-latency experience across different hardware. We relied on Google Cloud and Firebase — including Cloud Functions, Firestore and Cloud Ops. This solved the complexity of building and monitoring modern generative AI apps. Attendees also used Google Antigravity's agentic coding to quickly build their own order apps.

### Speaker title cards

**The AI products & models:** Gemini Omni; Google Flow; Nano Banana Pro

**What we did:** Each speaker got their own custom generated title card made with our image and video generation models.

**How we did it:** Josh Woodward — our VP of Google Labs & Google Gemini — is a great example. On stage, attendees saw a digital Josh riding Chrome Dino, then dunking a basketball.

We used Nano Banana Pro to generate core assets like ingredient reference sheets. We used these ingredients to storyboard, trying variations and adding personal details. In Google Flow, we first used Veo to help prototype actions and generate animations like a slam dunk. We also generated animations with Gemini Omni in Google Flow, which was particularly helpful when dealing with intricate sports movements. Detailed text prompts kept the AI outputs consistent with our reference sheets. Finally, we composited and time-remapped raw motion from the generated videos into polished titles.

Here’s a prompt we used for our ingredients reference sheet:

```ts
Man casually riding the trex. He looks comfortable like he has
done this many times before. Man is relaxed and holding reins on
the trex. Expand and show more of scene. Keep the cacti. Lighting on 
man makes sense. Man is also lit by dawn lighting like rest of scene.
```

Here’s a Google Flow video prompt we used after that:

```ts
Show me the rest of this scene. Keep consistent with the 
character sheet, especially the style of the trex. The trex jumps
over the cacti. Slam dunk.
```

### Sticker swag

![Four 3D I/O stickers in different patterns, including a black and purple galactic pattern](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/IO_Stickers.width-1200.format-webp.webp)

**The AI products & models:** Gemini and Nano Banana

**What we did:** We generated and printed custom I/O stickers for attendees on the spot.

**How we did it:** We built an interactive sticker game on a custom web app. Players had 20 seconds to catch falling prompts using an Android bot. There were over 100 prompt categories — from blueberries and disco balls to lasers and wood. Players selected two prompts, or hit "I'm feeling lucky" for a random mix. Our backend — using Nano Banana for Gemini and Android — fused these choices together. This created a highly personalized, custom I/O sticker design. Think of a 3D "I/O" made of solid gold waffles or a gummy bear motherboard. Designs were printed immediately for attendees to collect.

Here’s an example prompt we used to generate the sticker designs, starting with some general guidelines:

```ts
You are an advanced, highly precise AI image generation rendering
engine. Your primary function is to apply complex materials and
artistic styles to a specific 3D layout provided by the user.
```

Next, we provided additional details about individual elements like color, lighting and in the example below, the iconic “I/O” shape:

```ts
The geometry of the object (the vertical block, slanted slab, and
short cylinder forming "I/O") is immutable. You must perfectly
align the generated textures with the boundaries, depth and
perspective of the input layout. Do not alter the underlying 3D
shapes, pose or scale.
```

To dive deeper, catch up on [many of our biggest I/O 2026 announcements here](https://blog.google/innovation-and-ai/technology/ai/google-io-2026-all-our-announcements/).
