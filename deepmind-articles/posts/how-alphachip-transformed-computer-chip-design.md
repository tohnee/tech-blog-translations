---
title: "How AlphaChip transformed computer chip design"
source: https://deepmind.google/blog/how-alphachip-transformed-computer-chip-design/
site: deepmind
date: 2024-09-26
authors: Anna Goldie, Azalia Mirhoseini
crawled: 2026-09-13
---

Our AI method has accelerated and optimized chip design, and its superhuman chip layouts are used in hardware around the world

In 2020, we released a [preprint](https://arxiv.org/pdf/2004.10746) introducing our novel reinforcement learning method for designing chip layouts, which we later [published in Nature](https://www.nature.com/articles/s41586-021-03544-w) and [open sourced](https://github.com/google-research/circuit_training).

Today, we’re [publishing a Nature addendum](https://www.nature.com/articles/s41586-024-08032-5) that describes more about our method and its impact on the field of chip design. We’re also releasing a [pre-trained checkpoint](https://github.com/google-research/circuit_training/?tab=readme-ov-file#PreTrainedModelCheckpoint), sharing the model weights and announcing its name: AlphaChip.

Computer chips have fueled remarkable progress in artificial intelligence (AI), and AlphaChip returns the favor by using AI to accelerate and optimize chip design. The method has been used to design superhuman chip layouts in the last three generations of Google’s custom AI accelerator, the [Tensor Processing Unit](https://cloud.google.com/tpu?hl=en) (TPU).

AlphaChip was one of the first reinforcement learning approaches used to solve a real-world engineering problem. It generates superhuman or comparable chip layouts in hours, rather than taking weeks or months of human effort, and its layouts are used in chips all over the world, from data centers to mobile phones.

> AlphaChip’s groundbreaking AI approach revolutionizes a key phase of chip design.

SR Tsai

Senior Vice President of MediaTek

## How AlphaChip works

Designing a chip layout is not a simple task. Computer chips consist of many interconnected blocks, with layers of circuit components, all connected by incredibly thin wires. There are also lots of complex and intertwined design constraints that all have to be met at the same time. Because of its sheer complexity, chip designers have struggled to automate the chip floorplanning process for over sixty years.

Similar to [AlphaGo](https://deepmind.google/technologies/alphago/) and [AlphaZero](https://deepmind.google/technologies/alphazero-and-muzero/), which learned to master the games of Go, chess and shogi, we built AlphaChip to approach chip floorplanning as a kind of game.

Starting from a blank grid, AlphaChip places one circuit component at a time until it’s done placing all the components. Then it’s rewarded based on the quality of the final layout. A novel “edge-based” graph neural network allows AlphaChip to learn the relationships between interconnected chip components and to generalize across chips, letting AlphaChip improve with each layout it designs.

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

Left: Animation showing AlphaChip placing the open-source, Ariane RISC-V CPU, with no prior experience. Right: Animation showing AlphaChip placing the same block after having practiced on 20 TPU-related designs.

## Using AI to design Google’s AI accelerator chips

AlphaChip has generated superhuman chip layouts used in every generation of Google’s TPU since its publication in 2020. These chips make it possible to massively scale-up AI models based on Google’s [Transformer](https://research.google/blog/transformer-a-novel-neural-network-architecture-for-language-understanding/) architecture.

TPUs lie at the heart of our powerful generative AI systems, from large language models, like [Gemini](https://gemini.google.com/), to image and video generators, [Imagen](https://deepmind.google/technologies/imagen-3/) and [Veo](https://deepmind.google/technologies/veo/). These AI accelerators also lie at the heart of Google's AI services and are [available](https://cloud.google.com/tpu) to external users via Google Cloud.

![Photograph of a row of Cloud TPU v5p AI accelerator supercomputers in a Google data center](https://lh3.googleusercontent.com/tsPiQ_Sw2dnUDFsKuKa1SkyezcLczPkIEa44V3785ov_3YqDKm7HD1AL5MSjk9-SZ87kbAG-mKC-BMq4HoAVAOLxvJ62Zhguuu_RMn_0VfxOI6Pu4A=w1440)

A row of Cloud TPU v5p AI accelerator supercomputers in a Google data center.

To design TPU layouts, AlphaChip first practices on a diverse range of chip blocks from previous generations, such as [on-chip and inter-chip network blocks](https://en.wikipedia.org/wiki/Network_on_a_chip), [memory controllers](https://en.wikipedia.org/wiki/Memory_controller), and [data transport buffers](https://en.wikipedia.org/wiki/Data_buffer). This process is called pre-training. Then we run AlphaChip on current TPU blocks to generate high-quality layouts. Unlike prior approaches, AlphaChip becomes better and faster as it solves more instances of the chip placement task, similar to how human experts do.

With each new generation of TPU, including our latest [Trillium](https://cloud.google.com/blog/products/compute/introducing-trillium-6th-gen-tpus) (6th generation), AlphaChip has designed better chip layouts and provided more of the overall floorplan, accelerating the design cycle and yielding higher-performance chips.

![Bar graph showing the number of AlphaChip designed chip blocks across three generations of Google’s Tensor Processing Units (TPU), including v5e, v5p and Trillium.](https://lh3.googleusercontent.com/uvA--nI76IjsOKgvkv3eVi3MICc9-zRB8eLVhizsrJOneYBvaT-Ub65q-FwyUw_HXWyc-7z0J7_W3WlNJogdIXoAeeA8zkUKYiok8YM1ey44e3bFt9o=w1440)

Bar graph showing the number of AlphaChip designed chip blocks across three generations of Google’s Tensor Processing Units (TPU), including v5e, v5p and Trillium.

![Bar graph showing AlphaChip’s average wirelength reduction across three generations of Google’s Tensor Processing Units (TPUs), compared to placements generated by the TPU physical design team.](https://lh3.googleusercontent.com/HCymxHdoYn-g1paupQodU33pZqnEpJrqLn86Ji4KrX6PtyhoIVSOuSKGjLRVKUg3gj1aPtrEx8ppSa7EOA5wQY1DjWzQMDW4GJvu82qhlS6zPWGFHQ=w1440)

Bar graph showing AlphaChip’s average wirelength reduction across three generations of Google’s Tensor Processing Units (TPUs), compared to placements generated by the TPU physical design team.

## AlphaChip’s broader impact

AlphaChip’s impact can be seen through its applications across Alphabet, the research community and the chip design industry. Beyond designing specialized AI accelerators like TPUs, AlphaChip has generated layouts for other chips across Alphabet, such as [Google Axion Processors](https://cloud.google.com/blog/products/compute/introducing-googles-new-arm-based-cpu), our first Arm-based general-purpose data center CPUs.

External organizations are also adopting and building on AlphaChip. For example, MediaTek, one of the top chip design companies in the world, extended AlphaChip to accelerate development of their most advanced chips while improving power, performance and chip area.

AlphaChip has triggered an explosion of work on AI for chip design, and has been extended to other critical stages of chip design, such as [logic synthesis](https://openreview.net/forum?id=0t1O8ziRZp) and [macro selection](https://ieeexplore.ieee.org/document/9980637).

> AlphaChip has inspired an entirely new line of research on reinforcement learning for chip design, cutting across the design flow from logic synthesis to floorplanning, timing optimization and beyond.

Professor Siddharth Garg

NYU Tandon School of Engineering

## Creating the chips of the future

We believe AlphaChip has the potential to optimize every stage of the chip design cycle, from computer architecture to manufacturing — and to transform chip design for custom hardware found in everyday devices such as smartphones, medical equipment, agricultural sensors and more.

Future versions of AlphaChip are now in development and we look forward to working with the community to continue revolutionizing this area and bring about a future in which chips are even faster, cheaper and more power-efficient.

[Read our 2024 addendum](https://www.nature.com/articles/s41586-024-08032-5)[Read our 2021 paper](https://www.nature.com/articles/s41586-021-03544-w)[Read our 2020 preprint](https://arxiv.org/pdf/2004.10746)[See our pre-training tutorial](https://github.com/google-research/circuit_training/blob/main/docs/PRETRAINING.md)

Slide 1 of 5

> AlphaChip’s groundbreaking AI approach revolutionizes a key phase of chip design. At MediaTek, we’ve been pioneering chip design’s floorplanning and macro placement by extending this technique in combination with the industry’s best practices. This paradigm shift not only enhances design efficiency, but also sets new benchmarks for effectiveness, propelling the industry towards future breakthroughs.

SR Tsai, Senior Vice President

Mediatek

> AlphaChip demonstrates the remarkable transformative potential of reinforcement learning in tackling one of the most complex hardware optimization challenges: chip floorplanning. This research not only extends the application of reinforcement learning beyond its established success in game-playing scenarios to practical, high-impact industrial challenges, but also establishes a robust baseline environment for benchmarking future advancements at the intersection of AI and full-stack chip design. The work's long-term implications are far-reaching, illustrating how hard engineering tasks can be reframed as new avenues for AI-driven optimization in semiconductor technology.

Professor Vijay Janapa Reddi

Harvard University

> AlphaChip has inspired an entirely new line of research on reinforcement learning for chip design, cutting across the design flow from logic synthesis to floorplanning, timing optimization and beyond. While the details vary, key ideas in the paper including pre-trained agents that help guide online search and graph network based circuit representations continue to influence the field, including my own work on reinforcement learning for logic synthesis. If not already, this work is poised to be one of the landmark papers in machine learning for hardware design.

Professor Siddharth Garg

NYU Tandon School of Engineering

> Reinforcement learning has profoundly influenced electronic design automation (EDA), particularly by addressing the challenge of data scarcity in AI-driven methods. Despite obstacles including delayed rewards and limited generalization, research has proven reinforcement learning's capability in complex electronic design automation tasks such as floorplanning. This seminal paper has become a cornerstone in reinforcement learning-electronic design automation research and is frequently cited, including in my own work that received the Best Paper Award at the 2023 ACM Design Automation Conference.

Professor Sung-Kyu Lim

Georgia Institute of Technology

> There are two major forces that are playing a pivotal role in the modern era: semiconductor chip design and AI. This research charted a new path and demonstrated ideas that enabled the electronic design automation (EDA) community to see the power of AI and reinforcement learning for IC design. It has had a seminal impact in the field of AI for chip design and has been critical in influencing our thinking and efforts around establishing a major research conference like IEEE LLM-Aided Design (LAD) for discussion of such impactful ideas.

Ruchir Puri

Chief Scientist, IBM Research; IBM Fellow

**Acknowledgements**

We’re so grateful to our amazing coauthors: Mustafa Yazgan, Joe Wenjie Jiang, Ebrahim Songhori, Shen Wang, Young-Joon Lee, Eric Johnson, Omkar Pathak, Azade Nazi, Jiwoo Pak, Andy Tong, Kavya Srinivasa, William Hang, Emre Tuncer, Quoc V. Le, James Laudon, Richard Ho, Roger Carpenter and Jeff Dean.

We especially appreciate Joe Wenjie Jiang, Ebrahim Songhori, Young-Joon Lee, Roger Carpenter, and Sergio Guadarrama’s continued efforts to land this production impact, Quoc V. Le for his research advice and mentorship, and our senior author Jeff Dean for his support and deep technical discussions.

We also want to thank Ed Chi, Zoubin Ghahramani, Koray Kavukcuoglu, Dave Patterson, and Chris Manning for all of their advice and support.
