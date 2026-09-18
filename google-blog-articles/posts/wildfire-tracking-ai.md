---
title: "Ask a Scientist: How can researchers use AI to spot a wildfire?"
source: https://blog.google/innovation-and-ai/models-and-research/google-research/wildfire-tracking-ai/
site: google-blog
date: 2026-09-15
authors: Lindsey Lanquist
crawled: 2026-09-18
---

For over a decade, Google Research has been exploring how to use artificial intelligence and machine learning to detect wildfires and model how fires spread. Along the way, we’ve teamed up with Muon Space to support the Earth Fire Alliance’s [FireSat](https://blog.google/innovation-and-ai/products/inside-firesat-launch-muon-space/) program, a new satellite constellation designed to detect and monitor wildfires. Once completed — and with the help of AI — it will be able to spot fires as small as 5-by-5 meters (about the size of a single car), anywhere on Earth, from way up in space.

We sat down with research scientist Chris Van Arsdale to understand exactly how this technology works.

**What do you do at Google?**

I manage the climate and energy research group. We look for ways to use Google technology to mitigate climate change. We ask questions like, “What do we want things to look like in 20 years?” And we map out the steps we can take now — with today’s technology — to make a difference.

**Why did Google decide to tackle wildfire detection?**

There are huge swaths of the world where we expect an increase in wildfires, and we realized we could use technology to get ahead of that. We considered solutions like drone swarms with fire retardant to prevent fires from spreading, or finding a way to sniff out smoke distributed across the landscape. We settled on early wildfire detection — catching fires when they’re small, before they start spreading — as the solution with the highest potential impact.

Early detection is really an information problem, but when we looked into it, we realized the information we wanted to organize didn’t even exist. So we decided to design a novel satellite constellation to make it happen.

**Why has it traditionally been so difficult to spot a wildfire from space?**

Fire authorities want to catch a fire early, while it’s still small. But when you look at a typical satellite image of the earth, there’s a lot of things that could be mistaken for a wildfire — clouds reflecting sunlight or something hot, like a smoke stack or even a grill in someone’s backyard.

Plus, current satellite imagery is often working off data that’s about 11 hours old or really low-resolution, which makes it less useful when you’re trying to stop a rapidly spreading fire while it’s still small.

If you want satellites that can confidently spot really tiny wildfires, you can build a really big, expensive, high-resolution satellite that stares at the ground for a long time. Or you use smaller, lower-cost satellites — meaning you can launch a lot more of them — but you have to make up the precision difference with machine learning and AI. We chose the latter.

**What does it take to detect fires at such a small scale?**

We asked fire agencies how small a fire needs to be for them to have the chance to contain it. It’s somewhere around 50 to 100 square meters. So we set an even more ambitious target, making our early detection limit 25 square meters — a 5-by-5 meter fire.

We built a new type of camera that’s optimized to detect wildfires, and we initially trained our AI models by flying it over controlled burns. That gave us a reliable baseline for what fires look like from the air.

We’ve been flying that camera around California and taking pictures of things that look like fires from above. By tracking how these scenes change over time, we can distinguish true fires from false alarms — and improve our fire detection algorithms.

**How do you train an AI algorithm to distinguish a wildfire from a false alarm?**

There are lots of fires we don’t want to spam firefighters with. An agricultural burn, for example, is a controlled fire — which is different than a wildfire. For our AI models to be truly effective, we need to understand how fires progress over time. Which ones turn into wildfires, and which ones don’t?

That’s why we helped design the FireSat satellites, which operate in low-Earth orbit. Once the full constellation is deployed, the satellites will take a picture of the Earth every 20 minutes, meaning they can catch fires earlier and track how they progress in near real time time.

One of our goals with FireSat is to build a ground-truth record of what turns into a large wildfire and what doesn’t. We can use that data to fine-tune our algorithms and focus on the fires that matter most.

**What does this mean for first responders managing a fire on the ground?**

The greatest gift we can give to first responders is time. By gathering all this data, we’ll be able to detect fires while they’re still small to help prevent them from spreading, and we’ll also understand how they spread. This helps firefighters forecast fire behavior and ultimately keep their communities safe.

**What do you hope the scientific community will be able to learn from this dataset?**

When we began this program, we were frustrated by the lack of clear, ground truth data about wildfires. But we’ve made progress — our satellite has already spotted way more fires than we were expecting to detect. By collecting this data, analyzing it with researchers, and sharing those insights with authorities ahead of high-risk fire conditions, we can help them get a better understanding of fire activity over time and how it changes according to local conditions.

If you’re a city planner, for example, you might want to know where to put a firebreak — a barrier that slows the spread of a wildfire. Historically, we didn’t have good data to know where it should go. But with FireSat, we’ll get the answer.

**What’s next for our wildfire detection work?**

We just got our first batch of operational satellites up. The next batch will come next year. It’s going to take us a few years before we get to full operational capacity, and it’s going to be a long journey.

Our goal is to snap a picture of the world every 20 minutes, and that requires approximately 50 satellites. We expect to get there around 2030. In the meantime, our goal in the next two years is to capture a complete picture of the Earth’s surface every hour. That’s where we expect to see a lot of change in fire response.
