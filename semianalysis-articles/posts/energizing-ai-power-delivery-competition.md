---
title: "Energizing AI: Power Delivery Competition Heats Up Vicor, MPS, Delta, ADI, Renesas, Infineon "
subtitle: "Nvidia H100, Google TPUv5, AMD MI300, Intel Gaudi3/PVC, Cerebras WSE2"
date: 2023-08-01
source: https://newsletter.semianalysis.com/p/energizing-ai-power-delivery-competition
crawled: 2026-09-15
authors: ["Dylan Patel", "Myron Xie", "Gerald Wong", "George Cozma"]
tags: []
audience: only_paid
paywalled: true
---

# Energizing AI: Power Delivery Competition Heats Up Vicor, MPS, Delta, ADI, Renesas, Infineon 

**Nvidia H100, Google TPUv5, AMD MI300, Intel Gaudi3/PVC, Cerebras WSE2**

> ⚠️ 付费订阅文章：以下正文为公开可见的预览部分，在付费墙处截断，并非全文。/ Paid post: only the publicly visible preview portion is archived; the body is truncated at the paywall.

AI accelerators are becoming increasingly power-hungry. The Nvidia H100 has thermal design power (TDP) of 700 watts (W) compared to less than 200W for the most commonly installed datacenter CPU in the world, Intel Skylake/Cascade Lake. Next-generation chips will require even more power to support more compute density. This would require >200 kW at the rack level compared to current conventional CPU server racks that can deliver 15-20Kw.

With increasing power comes more challenges that need to be solved. In particular, higher power leads to disproportionately greater transmission and conversion losses: which is power that is being wasted. With electricity costs being one of the largest expenses in the datacenter, reducing power loss is vital to improving TCO. As a result, we are now seeing power delivery networks at the rack level down to the chip level being re-architected to address this in power-hungry compute workloads such as AI training and inferencing.

Advanced power delivery architecture’s primary purpose is to increase efficiency. Today we will dive into the technology and competitive landscape for this topic. Power delivery company Vicor has been one of the companies that historically benefitted the most from the trend historically. Over the last decade, Vicor went from a supplier of commodity power components to entering advanced datacenter power applications with design wins in various hyperscaler datacenter rack-level power solutions and AI accelerators from Nvidia, Google, AMD, Cerebras, Tesla, and Intel.

However, Vicor’s fortunes have changed rapidly more recently given the dynamic nature of the power market. As [we exclusively discovered and disclosed over a year ago, Monolithic Power Systems was able to supplant Vicor in Nvidia’s H100 GPU](https://www.semianalysis.com/p/short-report-nvidia-supplier-cut). Furthermore, Vicor’s 2nd biggest customer also has a tumultuous relationship. In addition, there are many changes with hyperscale datacenter rack power solutions including multiple new competitors (MPS, Delta, Renesas, Infineon, ADI).

The narrative has been volatile, with Vicor’s future role becoming a battleground. Recent newsflow, Vicor’s lawsuits against competitors, the deployments of hyperscalers, and incredible statements from leadership have given both sides of the argument ammunition.

Today we will go through a primer of power delivery, Vicor’s technology lead, our assessment of Vicor’s signature Factorized Power Architecture and Vertical Power Delivery technologies, key design wins, including details on whether Vicor is in the H100 or TPUv5, Vicor’s potential in the automotive industry, and implications for their long term. We will also share our view on their 5 main competitors, MPS, Delta, Renesas, Infineon, and ADI, and the current legal battle erupting.

## **Power Delivery for Chips, Primer**

Electricity is generated and transferred in the grid at voltages as high as hundreds of thousands at Alternating Current (AC). What compute and memory chips need is stable and clean power that is a much lower voltage and in the form of Direct Current (DC). Too much voltage will overload and damage the delicate circuitry of the chip. Too little voltage, and the chip’s circuits won’t be able to switch properly. It is the job of transformers, power supply units (PSUs), and finally, voltage regulator modules (VRMs) to deliver the right type of power to a chip. With increasing power demands, efficient power delivery is also becoming more challenging.

![](https://substack-post-media.s3.amazonaws.com/public/images/34bda3cd-c0b0-4e1e-9777-fe1e98c0df15_3082x892.png)

In electric circuits like a GPU or a CPU, there are 4 main values: Power, Current, Voltage, and Resistance. Power (P) is simply a measurement of energy used per unit of time which is commonly denoted in units of Watts (W). Current is a measurement of the amount of electrons being moved or, to put it another way, the flow rate of the electrons. Current (I or A) is often denoted in increments of amps (A). Voltage (V) is the difference in electric potential between 2 points. You can think of voltage as the pressure that pushes the electrons through a loop.

Voltage is usually given in units of Volts (V). Finally, we have Resistance (R), which is normally given in units of ohms (Ω) and is simply how hard it is for the current to flow through the material. To use these values, we need Ohm’s law and we are going to focus on 2 different forms of Ohm’s law. The first form is P = I*V which simply means that the power is equal to the current times the voltage. The second form is P = R*I2 which means that power also equals the resistance times the current squared.

Silicon runs at low voltages of around 1V DC or less. In pursuit of power efficiency, designs are moving to lower clockspeeds and lower operating voltages to run at a more efficient segment of the performance/power curve.

However, transporting power at low voltages and high currents creates large power losses (I^2R) from power line resistances. The key to minimizing power loss is to transport power at higher voltages and lower currents, then step down the voltage as close as possible to the active silicon.

## **What makes up a Voltage Regulator Module (VRM)?**

The VRM is an important set of parts that takes the input voltage from a system’s PSU then converts that into the correct voltage to power the SoC. Usually, we would see the VRM on the PCB housing the chip although in some rare cases, these components may be on the package itself or even integrated on the silicon. A modern VRM has 3 main parts: capacitors, inductors, and power stages. Capacitors store electrical energy and then release that energy at a constant rate, smoothing out the power being delivered to the processor. An inductor is used to resist changes in current and prevent massive spikes of current from killing the processor.

![](https://substack-post-media.s3.amazonaws.com/public/images/33694782-198d-46c6-8e45-22c05aa31978_2928x1431.png)
*Simplified VRM*

Lastly and arguably the most important part of the VRM is the power stage which takes the input voltage of say 12 volts from the PSU and converts that into the voltage the processor needs. On a CPU, that required voltage is traditionally 1.2 to 1.8 volts, and on a GPU or large FPGA, ASIC, or AI accelerator, that voltage is anywhere from 0.8 to 1.0 volts.

## **Higher Power, Lower Efficiency**

As the voltage to power the SoC drops with future architectures and process technologies, to maintain the same power the current needs to increase by the same factor of the voltage decrease. For example, let’s take a 240W AMD Genoa CPU with an operating voltage of 1.2 volts. Stepping down from the 12 volt input to 1.2 volts for the chip (a step down of 10x), means that the current needs to increase from 20 amps at 12 volts to 200 amps of current at 1.2 volts (an increase of 10x) to maintain the same level of power.

Compare this to a 700-watt GPU that operates at 0.8V. If you were to step down a 12 volt input to 0.8 volts for the chip (a step down of 15x), that means that current needs to increase from 60 amps at 12 volts to 875 amps of current at 0.8 volts (an increase of 15x). **Compared to the less-power-hungry CPU, the GPU’s current is much higher. Higher current means higher resistance losses** as we know from the P = R*I2 equation (loss is resistance multiplied by the square of current).

Resistance gets dramatically worse as we step down the voltage to 0.8V: the current increases by 15x, which **results in an exponentially** **larger resistance loss of 225x**. This exemplifies how efficiency losses have become a big problem with recent generations of datacenter chips. This only gets worse as the voltages continue to drop with process shrinks and packages get larger and more power-hungry with [advanced packaging](https://www.semianalysis.com/p/advanced-packaging-part-1-pad-limited).

[Share](https://newsletter.semianalysis.com/p/energizing-ai-power-delivery-competition?utm_source=substack&utm_medium=email&utm_content=share&action=share)

## **The Rise Of 48 Volt**

To address this, higher input voltages are being used. For a long time, 12V direct current (DC) power has been the standard voltage that PSUs for electronics would deliver. 12V was introduced at a time when it worked more than well enough as wattages were low enough so that resulting efficiency losses were immaterial. As the industry has started to require higher wattages with lower voltage SoCs, resulting in a double hit to efficiency. These efficiency losses outweigh the benefits of relatively cheap and ubiquitous 12V components.

**Going to 48V from 12V means 4 times less current is required, so loss will be 16 (4^2) times lower.** This is why many companies are moving to 48V power delivery networks. But what’s the point if you are going down to 1V anyway?

You can step down the 48V voltage to SoC voltage much closer to the SoC, **so the trace length is smaller. Longer trace length leads to greater resistance loss.** Therefore, by only stepping down the 48V input as close to the point of load as possible, the result is lower overall resistance losses.

![](https://substack-post-media.s3.amazonaws.com/public/images/b291ece1-d130-48b0-bc5a-6f9143f7cd2b_3427x1905.png)

Google was the first hyperscaler to adopt 48V power in their datacenters around 2016 and pushed for the 48V to be standardized in the OpenCompute consortium.

## **Vicor’s Rise**

In response, chip companies and OEMs placed 48V input VRMs on their boards. The main beneficiary of this was Vicor. While an established 48V ecosystem was used for telco equipment this was a negative voltage, whereas datacenters require positive voltages. Vicor was the primary player providing 48V VRMs for compute use cases.

To facilitate this change, power supply units would convert the 380V AC power the rack receives to 48V DC. With datacenters delivering 48V power at the rack, this created a reason for server boards also to start adopting 48V input to be able to take this 48V input voltage and step it down. Or, to make legacy 12V boards work, there would need to be an intermediate component to step down 48V to 12V. Basically, there either needs to be a 48V output voltage or 48V input voltage, and that is where Vicor was first to market.

![](https://substack-post-media.s3.amazonaws.com/public/images/8f07ef00-694b-482d-8e44-a8126234a2f5_2677x1434.png)
*Vicor’s 48V ecosystem*

Vicor's first mainstream merchant silicon design win was Nvidia’s V100 SXM3 refresh in 2018. It featured a 48V VRM using Vicor’s components. Then came the A100, and the entire lineup used Vicor parts for the VRM. Google also adopted Vicor for the TPU in a similar time frame as the V100. This reinforced Vicor’s dominance in 48V and that Vicor was the way forward for high-performance power delivery.

From there, the [narrative was violated when Vicor was designed out in the H100, replaced by Monolithic Power Systems (MPS)](https://www.semianalysis.com/p/short-report-nvidia-supplier-cut), which SemiAnalysis first broke the news of. This exclusive report was followed by Vicor’s stock falling more than 20% the morning after publication and an additional 30% over the next year due to Nvidia’s massive contribution to Vicor’s revenue. To this day, Vicor still hasn’t shipped in volume in [Nvidia’s H100, which is ramping up massively](https://www.semianalysis.com/p/ai-capacity-constraints-cowos-and).

Last week, Vicor’s 30+ year tenure CEO made claims about being designed back into a customer’s base platform while simultaneously filing lawsuits against his competitors, leading to a tremendous short squeeze. To be clear, the CEO also said to a sell sider they would be designed back in over a year ago, but the orders still haven’t come in. The official details are quite scant, so let’s unpack what’s happening with Nvidia and other customers.

Today we will go through Vicor’s technology lead, our assessment of Vicor’s signature Factorized Power Architecture and Vertical Power Delivery technologies, key design wins, including details on whether Vicor is in the H100 or TPUv5, Vicor’s chances in the automotive space, and implications for their long term prospects.We will also share our view on their 5 main competitors, MPS, Delta, Renesas, Infineon, and ADI, and the current legal battle erupting.

[Get 20% off a group subscription](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)
