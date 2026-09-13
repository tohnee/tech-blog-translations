---
title: "Accelerating fusion science through learned plasma control"
source: https://deepmind.google/blog/accelerating-fusion-science-through-learned-plasma-control/
site: deepmind
date: 2022-02-16
authors: 
crawled: 2026-09-13
---

Successfully controlling the nuclear fusion plasma in a tokamak with deep reinforcement learning

Note: This blog was first published on 16 Feb 2022. Following the release of [TORAX plasma simulator code](https://github.com/google-deepmind/torax) in May 2024, we’ve made minor updates to the text to reflect this.

To solve the global energy crisis, researchers have long sought a source of clean, limitless energy. Nuclear fusion, the reaction that powers the stars of the universe, is one contender. By smashing and fusing hydrogen, a common element of seawater, the powerful process releases huge amounts of energy. Here on earth, one way scientists have recreated these extreme conditions is by using a tokamak, a doughnut-shaped vacuum surrounded by magnetic coils, that is used to contain a plasma of hydrogen that is hotter than the core of the Sun. However, the plasmas in these machines are inherently unstable, making sustaining the process required for nuclear fusion a complex challenge. For example, a control system needs to coordinate the tokamak's many magnetic coils and adjust the voltage on them thousands of times per second to ensure the plasma never touches the walls of the vessel, which would result in heat loss and possibly damage. To help solve this problem and as part of DeepMind’s mission to advance science, we collaborated with [the Swiss Plasma Center](https://www.epfl.ch/research/domains/swiss-plasma-center/) at [EPFL](https://www.epfl.ch/) to develop the first deep reinforcement learning (RL) system to autonomously discover how to control these coils and successfully contain the plasma in a tokamak, opening new avenues to advance nuclear fusion research.

In a [paper published today in Nature](https://www.nature.com/articles/s41586-021-04301-9), we describe how we can successfully control nuclear fusion plasma by building and running controllers on the Variable Configuration Tokamak (TCV) in Lausanne, Switzerland. Using a learning architecture that combines deep RL and a simulated environment, we produced controllers that can both keep the plasma steady and be used to accurately sculpt it into different shapes. This “plasma sculpting” shows the RL system has successfully controlled the superheated matter and - importantly - allows scientists to investigate how the plasma reacts under different conditions, improving our understanding of fusion reactors.

> In the last two years DeepMind has demonstrated AI’s potential to accelerate scientific progress and unlock entirely new avenues of research across biology, chemistry, mathematics and now physics.

Demis Hassabis

Co-founder and CEO, DeepMind

This work is another powerful example of how machine learning and expert communities can come together to tackle grand challenges and accelerate scientific discovery. Our team is hard at work applying this approach to fields as diverse as quantum chemistry, pure mathematics, material design, weather forecasting, and more, to solve fundamental problems and ensure AI benefits humanity.

![A complex, industrial-scale view of the Variable Configuration Tokamak (TCV) hardware, showing a dense network of metal pipes, support structures, electrical wiring, and scientific equipment.](https://lh3.googleusercontent.com/WMw93KCG9rWNf9A7SsocGn4JFtXmm4XoVEtYgarEkv0rxR4HLLLXegV6o3fAWWML2zYAav4iS-CZEyEZOi0s6jXxhL0w9dtvEAaJqXFdE83ZJ5kG6s8=w1440)

![A simplified 3D cross-section diagram of a doughnut-shaped tokamak reactor, showing its grey outer vacuum vessel, concentric magnetic coils wrapping around it, and the orange and yellow nuclear fusion plasma core suspended inside.](https://lh3.googleusercontent.com/yY5FdXBZ4IMfow7lM9FxNH3DGAQ4cgb_w7T-lA9kCElgN6QDH4uQkQo_7VsmDgLXnIZTcr6MrKrgEtn7w7cAx2YKtjD2ebwG-j7HMcdZszwM0k41nEM=w1440)

![An interior wide-angle view of the empty vacuum vessel of the Variable Configuration Tokamak (TCV) in Lausanne, showing its curved metallic walls lined with protective tiles and a central column.](https://lh3.googleusercontent.com/i3UG0ZGwTpjIW3jK5kIQVIpOcZ_56AUi-kac74MrxZ5u0MHcXbW61sOcFUnNWBjpSXQvR7mSBI0JHIZLZvcRh80ufVtG4jLsmzvMHLlY8k7AeAV4=w1440)

## Learning when data is hard to acquire

Research into nuclear fusion is currently limited by researchers’ ability to run experiments. While there are dozens of active tokamaks around the world, they’re expensive machines and in high demand. For example, TCV can only sustain the plasma in a single experiment for up to three seconds, after which it needs 15 minutes to cool down and reset before the next attempt. Not only that, multiple research groups often share use of the tokamak, further limiting the time available for experiments.

Given the current obstacles to access a tokamak, researchers have turned to simulators to help advance research. For example, our partners at EPFL have built a powerful set of simulation tools that model the dynamics of tokamaks. We were able to use these to allow our RL system to learn to control TCV in simulation and then validate our results on the real TCV, showing we could successfully sculpt the plasma into the desired shapes. Whilst this is a cheaper and more convenient way to train our controllers; we still had to overcome many barriers. For example, plasma simulators are slow and require many hours of computer time to simulate one second of real time. In addition, the condition of TCV can change from day to day, requiring us to develop algorithmic improvements, both physical and simulated, and to adapt to the realities of the hardware.

## Success by prioritising simplicity and flexibility

Existing plasma-control systems are complex, requiring separate controllers for each of TCV’s 19 magnetic coils. Each controller uses algorithms to estimate the properties of the plasma in real time and adjust the voltage of the magnets accordingly. In contrast, our architecture uses a single neural network to control all of the coils at once, automatically learning which voltages are the best to achieve a plasma configuration directly from sensors.

As a demonstration, we first showed that we could manipulate many aspects of the plasma with a single controller.

![An animated split-screen comparison showing a real-time blue glowing plasma experiment from inside the tokamak on the left, next to a corresponding digital plasma state reconstruction diagram on the right as it shifts shapes and positions over time.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/622156ac3fb17333dc4ed11e_Fig202.gif)

The controller trained with deep reinforcement learning steers the plasma through multiple phases of an experiment. On the left, there is an inside view in the tokamak during the experiment. On the right, you can see the reconstructed plasma shape and the target points we wanted to hit. (credit: DeepMind & SPC/EPFL)

In the video above, we see the plasma at the top of TCV at the instant our system takes control. Our controller first shapes the plasma according to the requested shape, then shifts the plasma downward and detaches it from the walls, suspending it in the middle of the vessel on two legs. The plasma is held stationary, as would be needed to measure plasma properties. Then, finally the plasma is steered back to the top of the vessel and safely destroyed.

We then created a range of plasma shapes being studied by plasma physicists for their usefulness in generating energy. For example, we made a “snowflake” shape with many “legs” that could help reduce the cost of cooling by spreading the exhaust energy to different contact points on the vessel walls. We also demonstrated a shape close to the proposal for [ITER](https://www.iter.org/), the next-generation tokamak under construction, as EPFL was conducting experiments to predict the behaviour of plasmas in ITER. We even did something that had never been done in TCV before by stabilising a “droplet” where there are two plasmas inside the vessel simultaneously. Our single system was able to find controllers for all of these different conditions. We simply changed the goal we requested, and our algorithm autonomously found an appropriate controller.

![Five schematics of a tokamak cross-section showing different plasma shapes successfully controlled by reinforcement learning: Droplets, Negative Triangularity, ITER-like shape, Snowflake, and Elongated Plasma.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/622156e74a5e0732d8c7268e_Fig203.gif)

We successfully produced a range of shapes whose properties are under study by plasma physicists. (credit: DeepMind & SPC/EPFL)

## The future of fusion and beyond

Similar to progress we’ve seen when applying AI to other scientific domains, our successful demonstration of tokamak control shows the power of AI to accelerate and assist fusion science, and we expect increasing sophistication in the use of AI going forward. This capability of autonomously creating controllers could be used to design new kinds of tokamaks while simultaneously designing their controllers. Our work also points to a bright future for reinforcement learning in the control of complex machines. It’s especially exciting to consider fields where AI could augment human expertise, serving as a tool to discover new and creative approaches for hard real-world problems. We predict reinforcement learning will be a transformative technology for industrial and scientific control applications in the years to come, with applications ranging from energy efficiency to personalised medicine.

In May 2024, we released [TORAX](https://arxiv.org/abs/2406.06718), a new [open source](https://github.com/google-deepmind/torax) plasma simulator. TORAX models the “core” (interior) of the plasma, and predicts changes in temperature, density, and electric current. This expands our ability to train advanced tokamak AI controllers. TORAX is written in JAX, a Python framework originally developed to train AI, and offers exciting capabilities for scientific computing through fast and scalable computation, increased prediction accuracy, and sensitivity analysis. By making TORAX available to the fusion community with access to these new capabilities we hope it enables development of new workflows for general purpose tokamak design and optimization.

**Notes**

Read the paper: [Magnetic control of tokamak plasmas through deep reinforcement learning](https://www.nature.com/articles/s41586-021-04301-9)

Read the paper: [TORAX: A Fast and Differentiable Tokamak Transport Simulator in JAX](https://arxiv.org/abs/2406.06718)
