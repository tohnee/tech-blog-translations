---
title: "Running Guide agent: A step towards running unbounded"
source: https://blog.google/innovation-and-ai/models-and-research/google-deepmind/running-guide-agent/
site: google-blog
date: 2026-05-20
authors: Robin Dua
crawled: 2026-09-13
---

For blind and low-vision (BLV) athletes, running has traditionally required a physical tether — whether it’s a human guide or a painted track line. Today, we are excited to share how we’re taking steps towards changing that with the Running Guide agent, an accessibility agent that uses real-time environmental understanding to help low-vision athletes run. It marks a massive leap from simple path-following to advanced, real-time spatial reasoning. As we work to perfect this technology, our goal is simple: unassisted independence for every runner.

## A hybrid architecture for uncompromising safety

Building on our previous work with [Project Guideline](https://youtu.be/C_h4HnKVptk?si=MoQceUkIRkP4wbPr), the Running Guide agent uses a chest-mounted Pixel 10 Pro smartphone to view the path ahead and guide the user via auditory feedback. Because high-speed activities demand high trust, we built a hybrid, dual-path architecture:

- **On-device segmentation:** Running entirely offline on the Pixel 10’s custom silicon, this model guarantees ultra-low latency safety. It delivers immediate "STOP" alerts and steering cues — heard as directional ticking sounds — so runners maintain a reliable sense of direction even without a cellular connection.
- **Gemma 4’s advanced reasoning:** Leveraging [Gemma 4 E4B](https://huggingface.co/google/gemma-4-E4B), this path handles complex multimodal inputs (image and text) for high-level scene understanding entirely on device. To keep latency low, we use Smarter Frame Selection. Instead of processing every frame, the model only analyzes "high-entropy" frames — like sudden terrain changes or new obstacles — delivering faster, highly relevant coaching.

![Running guide agent architecture diagram. Flowchart maps Input Senses (video, audio, Pixel 10 Pro) to On-Device Analysis (Segmentation) and Agents (Planner, Coach, Break), leading to Output Feedback (Partial Audio and Voice Coaching)](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Architecture.width-1200.format-webp.webp)

## A multi-agent framework

The Running Guide agent is a collaborative, multi-agent framework designed to help enable the running experience for a BLV user:

- **Planner agent:** Utilizing Gemma 4’s function calling, this agent pulls weather and Google Maps data, chats with the runner to establish workout goals and calibrates their digital starting line.
- **Coach agent:** Operates mid-run to deliver concise, telegraphic verbal alerts. It triages feedback into a strict hierarchy: DANGER (immediate evasive action needed), WARNING (nearby runners/obstacles) and NOTICE (upcoming track curves).
- **Break agent:** Manages rest intervals, allowing athletes to pause and resume their session at any time.

## Intelligent eyewear and community partnerships

While the chest-mounted Pixel 10 Pro is a robust foundation, we are prototyping the Running Guide agent on intelligent eyewear. Wearable glasses provide a wider, steadier field of view, which drastically optimizes the data fed to our multimodal models. The glasses stream directly to the Pixel device, seamlessly blending hardware and ambient AI.

Runner’s view through Intelligent Eyewear

To ensure we are building alongside the community, we’ve partnered with [SG Enable](https://www.sgenable.sg/about-us/our-story), Singapore’s focal agency for disability and inclusion. By connecting our engineering teams directly with BLV runners for real-world testing, we can iteratively design a tool that truly meets their needs.

The Running Guide agent is a powerful showcase of the new chapter of agents for Google AI. Athletes will be able to use our tool, which combines zero-latency edge computing with deep-world understanding, to push their limits and navigate the world with total, unassisted confidence.
