---
title: "Using Unity to Help Solve Intelligence"
source: https://deepmind.google/blog/using-unity-to-help-solve-intelligence/
site: deepmind
date: 2020-11-18
authors: Simon Carter, Manuel Sanchez, Ricardo Barreira, Seb Noury, Keith Anderson, Jay Lemmon, Jonathan Coe, Piotr Trochim, Tom Handley, Adrian Bolton
crawled: 2026-09-13
---

## A wide range of environments

In the pursuit of artificial general intelligence (AGI), we seek to create agents that can achieve goals in a wide range of environments. As our agents master the environments we create, we must continually create new environments that probe as-yet-untested cognitive abilities.

Games have always provided a challenge for artificial intelligence (AI) research, most famously board games such as backgammon, chess, and Go. Video games such as Space Invaders, Quake III Arena, Dota 2 and StarCraft II have also more recently become popular for AI research. Games are ideal because they have a clear measure of success, allowing progress to be reviewed empirically and to be directly benchmarked against humans.

As AGI research progresses, so too does the research community’s interest in more complex games. At the same time, the engineering efforts needed for transforming individual video games into research environments become hard to manage. Increasingly, general-purpose game engines become the most scalable way to create a wide range of interactive environments.

## General-purpose game engines

Much AGI research has already happened in game engines such as [Project Malmo](https://www.microsoft.com/en-us/research/project/project-malmo/), based on Minecraft; [ViZDoom](http://vizdoom.cs.put.edu.pl/), based on Doom; and [DeepMind Lab](https://github.com/deepmind/lab), based on Quake III Arena. These engines can be scripted to quickly create new environments – and since many were written for older hardware, they’re able to run extremely fast on modern hardware, eliminating the environment as a performance bottleneck.

But these game engines are missing some important features. DeepMind Lab, for example, is excellent for learning navigation but poor for learning common sense notions like how objects move and interact with each other.

## Unity

At DeepMind we use Unity, a flexible and feature-rich game engine. Unity’s realistic physics simulation allows agents to experience an environment more closely grounded in the real world. The modern rendering pipeline provides more subtle visual clues such as realistic lighting and shadows. Unity scripts are written in C#, which is easy to read, and unlike with bespoke engines, provides access to all game-engine features. Multiplatform support lets us run environments at home on our laptops or at scale on Google’s data-centres. Finally, as the Unity engine continues to evolve, we can future-proof ourselves without expending a large amount of our own engineering time.

Unity includes a ready-to-use machine learning toolkit called [ML-Agents](https://unity.com/products/machine-learning-agents) that focuses on simplifying the process of making an existing game available as a learning environment. DeepMind focuses on constructing a wide variety of heterogeneous environments which are run at scale, and as such we instead use dm\_env\_rpc (see below).

![Four screen captures of Unity environments created at DeepMind](https://lh3.googleusercontent.com/DW-eKf83KbI3sYOIflGj2CG6DZeui2qBmhDVKH4HO3B2247NrVvviFRDvEjae2ciCqdUWktSkE0cxByVQOKL7Ha2fDhBwr8yQUJcRD0bf4D3FIcJ_3Q=w1440)

Screen captures of Unity environments created at DeepMind

## Differences from conventional games

Traditional video games render themselves in real-time: one second on-screen is equal to one second in a simulation. But to AI researchers, a game is just a stream of data. Games can often be processed much more quickly than in real-time, and there’s no problem if the game speed varies wildly from moment to moment.

Additionally, many reinforcement learning algorithms scale with multiple instances. That is, one AI can play thousands of games simultaneously and learn from them all at once.

Because of this, we optimise for throughput instead of latency. That is, we update our games as many times as we can and don’t worry about generating those updates at a consistent rate. We run multiple games on a single computer, with one game per processor core. Stalls caused by features such as garbage collection - a common headache for traditional game makers - are not a concern to us as long as the game generally runs quickly.

## Containerisation and dm\_env\_rpc

Games output images, text, and sound for the player to see and hear, and also take input commands from a game controller of some kind. The structure of this data is important for AI researchers. For example, text is normally presented separately instead of being drawn onto the screen. Since flexibility in this data format is so important, we created a new open-source library called [dm\_env\_rpc](https://github.com/deepmind/dm_env_rpc), which functions as the boundary between environments and agents.

By using dm\_env\_rpc, we can containerise our environments and release them publicly. Containerisation means using technology like [Docker](https://www.docker.com/) to package precompiled environment binaries. Containerisation allows our research to be independently verified. It’s a more reliable and convenient way to reproduce experiments than open sourcing, which can be confused by compiler or operating system differences. For more details on how we containerise an environment, please see our work on [dm\_memorytasks.](https://github.com/deepmind/dm_memorytasks)
