---
title: "Behind Project Suncatcher, our moonshot to put AI in space"
source: https://blog.google/innovation-and-ai/models-and-research/google-research/google-project-suncatcher-facts/
site: google-blog
date: 2026-09-24
authors: Travis Beals
crawled: 2026-09-25
---

After years of research, Project Suncatcher is scheduled to embark on its first test in orbit, launching a prototype satellite to evaluate how Google Tensor Processing Units (TPUs) perform in space.

Announced last year, [Project Suncatcher](https://blog.google/innovation-and-ai/technology/research/google-project-suncatcher/) is a long-term, research moonshot exploring whether space could one day host scalable machine learning infrastructure. In low Earth orbit, satellites can access near-constant sunlight, generating up to eight times more solar power than on Earth. Eventually, it could be possible to link together multiple constellations of satellites, allowing them to manage larger AI workloads while in orbit.

Big breakthroughs happen when you work backwards from an end goal. In our case, it's to ensure AI's profound benefits in key areas, from healthcare to scientific discovery, can reach everyone, far into the future. Just as early research into autonomous driving and quantum computing required years of experimentation before we got to practical systems, exploring compute in space begins with measured, deliberate steps.

Turning that idea into reality starts with a basic question: Can our AI hardware operate in space? This initial mission onboard the upcoming Transporter-18 rideshare mission with SpaceX was developed in partnership with [Planet](https://www.planet.com/). It’s designed to gather in-orbit data on how our TPUs handle the physical stress of spaceflight and the radiation and thermal extremes of space.

As we prepare for an early test launch and work toward our next milestone in 2027, the Project Suncatcher team discussed what we hope to learn and the engineering hurdles ahead in a new [video series](https://www.youtube.com/playlist?list=PLAeFjVYtuU34) digging into the science behind the mission.

## Hardware survival

A rocket trip into low Earth orbit lasts about 10 minutes, during which the spacecraft experiences intense vibration and sustained acceleration loads up to 10 times the force of gravity, or g-force. Individual components, such as the TPU chips, can experience even greater forces up to 50 to 100 *g*. The team conducted vibration testing by intensely shaking the satellite on all three axes to mimic the frequencies of a rocket launch. Tests like this rarely go as planned, so we were pleasantly surprised that the hardware held up to the force.

Once the TPU chips make it to space, the level of radiation outside the Earth’s atmosphere presents another challenge to overcome. Solar events and cosmic rays can wreak havoc on electronics, so our team tested TPUs in a proton beam facility at UC Davis’s Crocker Nuclear Laboratory while running AI workloads. During the test, we monitored closely to see how errors, like a bitflip, would affect our workloads. Initial results have shown that our Trillium TPUs hold up remarkably well, and can survive a radiation total ionizing dose greater than what they would receive during a five-year space mission.

But some things can only be tested in space. Putting our first TPUs in orbit next week will help us get data and learnings to inform future launches.

## Cooling in space

Cooling orbital data centers is a crucial research challenge. TPUs generate a large amount of heat in a small area, which needs to be diffused safely or the chips are at risk of overheating. But in space, there’s no airflow. In a vacuum, you can only diffuse heat via radiators, which requires a totally different approach to cooling electronics.

We’re working on a number of different approaches for this, including a combination of heat pipes and radiators to cool the chips. So far, our team has tested the technology in a thermal vacuum chamber that simulates both the thermal and vacuum environment in space. We’ll see how our new TPU cooling system works in space and refine our designs as we learn more.

## Satellite interconnectivity

Future designs of our satellites will each carry dozens of TPU chips while orbiting the Earth in clusters. To maintain the bandwidth necessary to process AI, every satellite has to know both its own position and where it sits relative to its neighbors. To do this, the satellites will communicate via lasers.

The technology in space already exists, but most state-of-the-art systems are optimized for low bandwidth across large distances, whereas our lasers need to operate at very high bandwidth over extremely short distances. Maintaining the necessary connection requires extraordinary precision, similar to hitting a coin-size target from miles away while both points are in motion. We’ll test our work on this in 2027 when we put two satellites in orbit.

## Just the beginning

Exploring space as a viable location for scalable AI compute won’t happen all at once. It takes methodical engineering, starting with proving our hardware can handle the physical and unpredictable realities of operating in orbit. This first launch is about seeing what works, identifying points of failure, and applying those findings to future missions.

Every transformative technology we’ve built at Google began with an audacious goal — and the discipline of working backward to solve hard problems all along the way. As our latest moonshot heads to the launchpad, our team is excited to share what we learn and the science driving this work forward.
