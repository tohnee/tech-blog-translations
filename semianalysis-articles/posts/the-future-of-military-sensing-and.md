---
title: "The Future Of Military Sensing And Communications Systems – Co-Packaged Optics Enable Converged RF Phased Arrays"
subtitle: "Lockheed Martin NGAD enabled by Ayar Labs"
date: 2022-11-02
source: https://newsletter.semianalysis.com/p/the-future-of-military-sensing-and
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: everyone
paywalled: false
---

# The Future Of Military Sensing And Communications Systems – Co-Packaged Optics Enable Converged RF Phased Arrays

**Lockheed Martin NGAD enabled by Ayar Labs**

Warfare is evolving rapidly due to the advancements in semiconductors and sensors. The model of massive budgets for single programs that take decades to churn out a few hundred units of equipment is facing tremendous pressure. Stealth, drones, and mass-volume manufacturing of precision-guided missiles are rapidly changing the equation of defense. Currently, the most advanced militaries have dozens or hundreds of fighters and bombers but tens of thousands of drones and missiles. It’s unknown if modern militaries can combat or even reliably track a high-density swarm of these new weapons with existing capabilities.

Ayar Labs and Lockheed Martin published a fascinating paper regarding radio frequency (RF) converged phased array antennas utilizing silicon photonics for communications. This solution could answer this problem. Today we want to explain current sensor, and communications architectures of defense systems, cost and performance issues with these architectures, digital beamforming, MIMO, RF phased arrays, and silicon photonics for defense applications. Special thanks to the SPIE Optics and Photonics conference, presentations, and papers as they are helped tremendously in the writing of this.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/3a68cf43-e198-42be-9520-2b67329ed42e_958x611.png)

First, let’s discuss modern sensor and communications architectures. This is a demonstrative model of a modern jet fighter such as an F-22 Raptor or F-35 Lightning. These aircraft use arrays of sophisticated sensors for targeting, tracking, communications, and more. The F-35, for example, was a [pioneer in infrared sensor systems](https://www.lockheedmartin.com/en-us/products/f-35-lightning-ii-eots.html). This system utilizes many arrays of electro-optical antennas to give it a 360-degree view of everything around the aircraft. This greatly improved the fighter’s capabilities regarding searching and tracking targets. The biggest flaw of this system is that its flexibility is quite limited. The entire subsystem lives in its own bubble with its own processing pipelines.

> Each aperture is tightly integrated into its corresponding RF system, and cannot be utilized by a different system without either physically rewiring the platform, or retraining an existing system to accommodate the needs of another system.
>
> Lockheed Martin

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/ce104109-4f4d-4eed-8d4d-899413bb89a2_1427x656.png)

Deploying these sensors in a defense application, requires a whole host of very custom work, from the physical electro-optical infrared sensor development through to processing and algorithms. Developing this system is incredibly costly and involves many disciplines that must work together for a long period of time to develop completed systems. The electro-optical infra-red system will be completely separate from another RF sensing or communications system.

In many cases, each sensor is optimized for that particular use case. A modern military must have RF systems designed to detect, track, connect, and communicate with various planes, drones, missiles, helicopters, satellites, ground-based weapons systems, ships, submarines, and more. As more RF subsystems are created for interfacing with these various elements of the battlefield, friend and foe, the complexity and costs skyrocket.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/47debceb-c761-4538-ab1f-cd5305b982f5_1357x735.png)

These advanced military applications are beginning to require dozens of different subsystems, and the costs are ballooning. Furthermore, delays with a single subsystem mean the entire platform is now delayed. The F-35 is often bashed for these delays and costs. While the exact causes of various delays are unknown, the monolithic planning and complexity involved with creating such a complex system is the culprit. Now that the F-35 is working and deployed, it is considered leagues ahead of any other fighter in the world, and the RF subsystems are a big part of that.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/ab8c525a-b6b3-4016-851b-935fdd800c94_1398x567.png)

Imagine if these many different RF subsystems could be developed and deployed in a disaggregated manner. Instead of monolithic subsystems where sensors, RF processing, and application space are all built for each specific task, the solution space is reframed. A few major classes of sensors could be optimized for RF gain, noise, and other attributes instead of being tuned for the exact use case. The RF processing algorithms could be updated on a faster cadence to introduce new sensing and communications capabilities based on the data coming in and being sent out of these RF elements. The application algorithms could also be updated on a separate cadence to react to evolving battlefields. Rather than costly 20-year programs, the timeline for bringing advanced technology would be rapidly shortened.

Above is a demonstrative example of an NGAD fighter with only two types of sensors. A high-performance phased array antenna array and an electro-optical infrared antenna array. Versus the demonstrative example of the F-22/F-35 fighter, there are significantly fewer sensor types. Despite the reduced types of sensors, disaggregating sensors from processing would enable enhanced capabilities for tracking more, smaller, and stealthier targets.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/90baa2b6-a0c8-4c4b-88bc-17efbb912116_1423x717.png)

The various RF sensors would be converged before processing. With techniques such as MIMO and digital beamforming, higher data rates and less noisy signals can be obtained.

Digital beamforming and MIMO (multiple input, multiple output) are technologies that have been utilized in the past, but more complex algorithms and techniques continue to drive the performance of RF systems. We haven’t ever explained beamforming or MIMO in a public report, so we will provide a quick primer. Please recognize that we are oversimplifying it; many books have been written about these topics.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/5afb0b0e-699b-4375-924a-34e72fe04ebc_502x282.png)

MIMO is when there are multiple inputs and multiple outputs for a transmit and receive device. The benefits for the total data throughput are huge. For reference, 5G small cells have in the range of 64 transmit and 64 receive pairs. The path for getting huge volumes of data in and out of a next-generation aircraft is clear, given that the consumer market has proven these technologies.

The less intuitive aspect of MIMO is regarding RF sensing applications. Imagine if the transmit side is a drone or a stealth aircraft. That enemy is not actively attempting to signal the fighter. They are attempting to mask their radar and infrared signatures. Imagine how difficult it is to pick up the signals emitted or radiated off the low radar signature combatant covered in radar-absorbing materials. Sensing applications require the location, heading, velocity, and rate at which a foe makes maneuvers to be known. The combat response will differ depending on whether the sensing system detects the unidentified object as a bird, drone, stealth fighter, stealth bomber, or missile.

MIMO regarding sensing lets a broader range of outputted signals be picked up over a larger effective area. This is also [where digital beamforming](https://www.youtube.com/watch?v=A1n5Hhwtz78) comes in. Just like MIMO, it is already used in commercial applications, but the use cases for military applications are unique. All the receive antenna arrays will receive slightly different phases and amplitude for signals due to propagation delays.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/bb6ad3c8-0f3e-447b-87bc-67162d8ee3fd_1531x1043.png)

When there are objects and signals in multiple directions, digital beamforming allows the system to focus in on a specific signal. The various receive antennas will sync their timing to a particular direction and distance by introducing nanosecond-level delays to the antennas receiving the signal first. Once all signals are synced up perfectly for that specific distance and direction, the outputs from the various receive antennas can be added together. The focal point of these antennas will have its signal amplified, while all other objects will be noisy and can be filtered out. Check out [this video](https://www.youtube.com/watch?v=A1n5Hhwtz78) for further explanation.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/96a49429-60a0-41b1-a189-72f9f58bb78f_1822x962.png)

Beamforming can be analog or digital in nature. The advantage of digital beamforming is that each processing element receives the raw data and uses digital signal processing to steer the beam through analysis of the dataset. This processing can occur simultaneously for many different focal points enabling the detection of swarms of much smaller objects like thousands of drones and missiles.

The move to a converged architecture requires the antenna arrays all around the aircraft to be able to be processed centrally rather than individually at each antenna array. Compare and contrast the current generation architecture (1st image) and the next generation architecture (2nd image).

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/15beec3c-4e79-49fb-aa31-257240a877d7_1427x656.png)
![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/1e515dec-49f7-4bbd-9e43-1ac7f2f7a4af_1423x717.png)

The IO requirements are massively higher with the next-generation architecture. All the 100s of GB/s coming from the sensors must be sent to a central switch before going to the various processing types, which is an explosion in networking IO speed requirements.

The crux of the idea is that instead of independently building isolated systems, they can make one extensive network that can accomplish every task together, which is only possible with extremely high-speed and efficient networking.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/4c550d2f-392e-4b9f-95c4-7be1d059f953_1423x838.png)

This is where [Ayar Labs’ co-packaged optics](https://www.semianalysis.com/p/ayar-labs-co-packaged-optics-revolution?s=w) comes in. As a refresher, check out [our prior report on the firm, which details their co-packaged optics solution for the datacenter](https://www.semianalysis.com/p/ayar-labs-co-packaged-optics-revolution?s=w). Optical IO is far more efficient than an electrical form. Ayar Labs and Lockheed Martin are researching the integration of TeraPHY co-packaged optical IO chiplet with RFICs for building advanced packages with these capabilities. Sensors, switches, and processing elements could theoretically use this optical IO for dramatically lower power consumption and higher bandwidth.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/4de7a67e-b8e5-48a4-9478-c976377e8c10_1427x803.png)

Utilizing co-packaged optical IO has multiple benefits beyond lower power and higher bandwidth. First, there is much lower electromagnetic interference (EMI). Electrical copper-based interconnects must deal with interference from higher radiation levels, the earth’s magnetic field, or combatants’ countermeasures. This interference can then cause errors in the signal being transmitted. Copper-based wiring deployed in aerospace applications requires significant shielding to prevent these issues.

Furthermore, with high-speed copper signaling, there are propagation and signal loss issues, so wiring runs are limited in length. These loss-related issues are compensated by running lower gauge, thicker wires. This introduces problems with aerospace applications as hundreds or thousands of cables are routed around an aircraft. If each wiring run is a thick gauge of wire with EMI shielding, then this wiring will take up significant space and weight budget.

Both these issues are not as relevant with co-packaged optical IO. Glass fiber optic cables require minimal shielding because they are impervious to most EMI. Glass fibers are much thinner, lighter, and more flexible. These characteristics enable wiring in much tighter spaces.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/89c7b45a-e5cd-49b0-b358-4b69e1e533e8_757x772.png)

Ayar Labs and Lockheed Martin compared the co-package optical IO to the existing state-of-the-art mid-board optical transceivers. The comparison shows that co-packaged optics have lower power, lower area, lower error rates, and higher performance. Mid-board transceivers are currently used in some military applications, although we aren’t sure where. The suppliers all have a bucket for “defense” applications.

Another interesting aspect of this research is that it could generate synergies with Ayar Labs’ current push into the datacenters. Datacenters have been reluctant to adopt co-packaged optics due to the fragility and reliability concerns. Ayar Labs will be able to prove its technology in a much more demanding application. Humidity, G-forces, laser lifetime, and temperature swings are still significant challenges, but progress is promising. Some of these learnings could be applied in the much larger datacenter communications market.

If you enjoyed reading, please share it! It helps us produce unique and niche content!

[Share](https://newsletter.semianalysis.com/p/the-future-of-military-sensing-and?utm_source=substack&utm_medium=email&utm_content=share&action=share)

[Give a gift subscription](https://newsletter.semianalysis.com/subscribe?&gift=true)

[Get 20% off a group subscription](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)

[Leave a comment](https://newsletter.semianalysis.com/p/the-future-of-military-sensing-and/comments)
