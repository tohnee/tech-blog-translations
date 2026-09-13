---
title: "Sora 2 is here"
date: 2025-09-30
source: https://openai.com/index/sora-2/
crawled: 2026-09-13
category: research
---

*As of April 26, 2026, the Sora product is no longer available.*

---

Today we’re releasing Sora 2, our flagship video and audio generation model.

The [original Sora model](https://openai.com/index/video-generation-models-as-world-simulators/) from February 2024 was in many ways the GPT‑1 moment for video—the first time video generation started to seem like it was working, and simple behaviors like object permanence emerged from scaling up pre-training compute. Since then, the Sora team has been focused on training models with more advanced world simulation capabilities. We believe such systems will be critical for training AI models that deeply understand the physical world. A major milestone for this is mastering pre-training and post-training on large-scale video data, which are in their infancy compared to language.

Prompt: figure skater performs a triple axle with a cat on her head

With Sora 2, we are jumping straight to what we think may be the GPT‑3.5 moment for video. Sora 2 can do things that are exceptionally difficult—and in some instances outright impossible—for prior video generation models: Olympic gymnastics routines, backflips on a paddleboard that accurately model the dynamics of buoyancy and rigidity, and triple axels while a cat holds on for dear life.

Prompt: a guy does a backflip

Prior video models are overoptimistic—they will morph objects and deform reality to successfully execute upon a text prompt. For example, if a basketball player misses a shot, the ball may spontaneously teleport to the hoop. In Sora 2, if a basketball player misses a shot, it will rebound off the backboard. Interestingly, “mistakes” the model makes frequently appear to be mistakes of the internal agent that Sora 2 is implicitly modeling; though still imperfect, it is better about obeying the laws of physics compared to prior systems. This is an extremely important capability for any useful world simulator—you must be able to model failure, not just success.

The model is also a big leap forward in controllability, able to follow intricate instructions spanning multiple shots while accurately persisting world state. It excels at realistic, cinematic, and anime styles.

Prompt: Vikings Go To War — North Sea Launch (10.0s, Winter cool daylight / early medieval)...

As a general purpose video-audio generation system, it is capable of creating sophisticated background soundscapes, speech, and sound effects with a high degree of realism.

Prompt: Two mountain explorers in bright technical shells, ice crusted faces, eyes narrowed with urgency shout in the snow, one at a time

You can also directly inject elements of the real world into Sora 2. For example, by observing a video of one of our teammates, the model can insert them into any Sora-generated environment with an accurate portrayal of appearance and voice. This capability is very general, and works for any human, animal or object.

Prompt: Bigfoot is really kind to him, a little too kind, like oddly kind. Bigfoot wants to hang out but he he wants to hang too much

The model is far from perfect and makes plenty of mistakes, but it is validation that further scaling up neural networks on video data will bring us closer to simulating reality.

## Deployment of Sora 2

On the road to general-purpose simulation and AI systems that can function in the physical world, we think people can have a lot of fun with the models we’re building along the way.

We first started playing with this “upload yourself” feature several months ago on the Sora team, and we all had a blast with it. It kind of felt like a natural evolution of communication—from text messages to emojis to voice notes to this.

So today, we’re launching a** new social iOS app just called “Sora,”** powered by Sora 2. Inside the app, you can create, remix each other’s generations, discover new videos in a customizable Sora feed, and bring yourself or your friends in via a feature called “**characters**”. With characters, you can drop yourself straight into any Sora scene with remarkable fidelity after a short one-time video-and-audio recording in the app to verify your identity and capture your likeness.

Last week, we launched the app internally to all of OpenAI. We’ve already heard from our colleagues that they’re making new friends at the company because of the feature. We think a social app built around this “characters” feature is the best way to experience the magic of Sora 2.

## Launching responsibly

Concerns about doomscrolling, addiction, isolation, and RL-sloptimized feeds are top of mind—here is what we are doing about it.

We are giving users the tools and optionality to be **in control of what they see on the feed**. Using OpenAI's existing large language models, we have developed a new class of recommender algorithms that can be instructed through natural language. We also have built-in mechanisms to periodically poll users on their wellbeing and proactively give them the option to adjust their feed.

By default, we show you content heavily biased towards people you follow or interact with, and prioritize videos that the model thinks you’re most likely to use as inspiration for your own creations. We are not optimizing for time spent in feed, and we explicitly designed the app to maximize creation*, *not consumption. You can find more details in our [Feed Philosophy](https://openai.com/index/sora-feed-philosophy/)

This app is **made to be used with your friends**. Overwhelming feedback from testers is that characters are what make this feel different and fun to use—you have to try it to really get it, but it is a new and unique way to communicate with people. We’re rolling this out as an invite-based app to make sure you come in with your friends. At a time when all major platforms are moving away from the social graph, we think characters will reinforce community.

**Protecting the wellbeing of teens** is important to us. We are putting in default limits on how many generations teens can see per day in the feed, and we’re also rolling out with stricter permissions on characters for this group. In addition to our automated safety stacks, we are scaling up teams of human moderators to quickly review cases of bullying if they arise. We are launching with Sora [parental controls](https://openai.com/index/introducing-parental-controls/) via ChatGPT so parents can override infinite scroll limits, turn off algorithm personalization, as well as manage direct message settings.

With characters, **you are in control of your likeness end-to-end** with Sora. Only you decide who can use your character, and you can revoke access or remove any video that includes it at any time. Videos containing a character of you, including drafts created by other people, are viewable by you at any time.

There are a lot of safety topics we’ve tackled with this app—consent around use of likeness, provenance, preventing the generation of harmful content, and much more. See our [Sora 2 Safety doc](https://openai.com/index/launching-sora-responsibly/) for more details.

A lot of problems with other apps stem from the monetization model incentivizing decisions that are at odds with user wellbeing. Transparently, our only current plan is to eventually give users the option to pay some amount to generate an extra video if there’s too much demand relative to available compute. As the app evolves, we will openly communicate any changes in our approach here, while continuing to keep user wellbeing as our main goal.

We’re at the beginning of this journey, but with all of the powerful ways to create and remix content with Sora 2, we see this as the beginning of a completely new era for co-creative experiences. We’re optimistic that this will be a healthier platform for entertainment and creativity compared to what is available right now. We hope you have a good time :)

## Sora 2 availability and what’s next

The [Sora iOS app](https://apps.apple.com/app/id6744034028) is available to download now. You can sign up in-app for a push notification when access opens for your account. We’re starting the initial rollout in the **U.S. and Canada** today with the intent to quickly expand to additional countries. After you’ve received an invite, you’ll also be able to access Sora 2 through [sora.com](http://sora.com). Sora 2 will initially be available for free, with generous limits to start so people can freely explore its capabilities, though these are still subject to compute constraints. ChatGPT Pro users will also be able to use our experimental, higher quality **Sora 2 Pro** model on [sora.com](http://sora.com) (and soon in the Sora app as well). We also plan to release Sora 2 in the API. Sora 1 Turbo will remain available, and everything you’ve created will continue to live in your [sora.com](http://sora.com) library.

Video models are getting very good, very quickly. General-purpose world simulators and robotic agents will fundamentally reshape society and accelerate the arc of human progress. Sora 2 represents significant progress towards that goal. In keeping with OpenAI’s mission, it is important that humanity benefits from these models as they are developed. We think Sora is going to bring a lot of joy, creativity and connection to the world.

*— Written by the Sora Team*

Primary Target & Visuals
First read: a dragon slicing past serrated ice spires, wingtip vortices peeling spindrift; second read: the glacier’s fractured sheet falling away to a cobalt fjord, with amber sun rim kissing frost on scales; expression reads predatory calm / effortless power.

Format & Look
5.0s; 4K; 180° shutter; large-format digital sensor emulation with crisp micro-contrast; very fine grain; restrained halation on snow glints; no gate weave.

Lenses & Filtration
Hero: 50mm spherical on nose-mounted gyro-stabilized aerial platform (parallel tracking with slight inward arc). Filtration: Black Pro-Mist 1/8; circular polarizer set light to tame snow glare while preserving specular sparkle.

Grade / Palette
Highlights: clean ice white with cool roll-off; Mids: steel-blue glacier and pale cyan air; Shadows: slate/teal with preserved crevasse detail; warm amber rim on dragon edges for separation; speculars tight on frost/scale.

Lighting & Atmosphere
Late-afternoon low sun cross-key; katabatic wind lofting spindrift; thin frozen haze for depth; intermittent ice-dust bursts in the wake; faint breath-vapor from the dragon on exertion.

Location & Framing
Towering serac field and knife-edged ridgeline; camera tracks co-speed alongside the dragon at mid-altitude, glacier diagonals driving back to fjord; foreground ice fins pass close for parallax; no human structures.

Wardrobe / Props / Vehicle Notes
N/A (creature). Surface read: matte horn ridges, semi-iridescent scale plates with micro-frost along leading edges.

Sound
High-air wind shear, wing membrane thunder each downstroke, crystalline ice tick/creak from the seracs, distant glacier calving boom; quick exhale/rumble from the dragon: “Rrhh—” (sub-1s). No score—pure diegetic awe.

Optimized Shot List (1 shot / 5.0s)
0.0–5.0 — “Parallel Ridge Carve” (50mm, nose-mount aerial with slight inward arc & micro-push)
We pace the dragon as it threads a corridor of ice spires; wingtip vortices peel spindrift into ribbons; a calving fragment drops far below, sending a powder plume; the camera eases closer—scales read, amber rim flares—then the dragon banks toward the fjord, tail scissoring, casting a sweeping shadow over the glacier.
Purpose: Deliver mythic scale with tactile realism in one decisive pass—speed, mass, and elemental cold.

Camera Notes (Why It Reads)
50mm balances creature presence and landscape scale without miniaturizing; parallel track + inward arc sells velocity and form; micro-push times with strongest downstroke for power punctuation; light polarizer controls glare while keeping glitter; back/rim sun sculpts silhouette; near-miss ice fins provide parallax speed cues.

Finishing
Very fine grain (~15%); halation minimal on snow speculars; gentle print emulation to keep blues credible and blacks rich; multiband dynamics to retain wing thump without masking calving boom; poster frame: dragon banked across a sun-lit serac, spindrift streaming, fjord blazing deep blue beyond.

## Sora 2
