---
title: "GPT‑5 lowers the cost of cell-free protein synthesis"
date: 2026-02-05
source: https://openai.com/index/gpt-5-lowers-protein-synthesis-cost/
crawled: 2026-09-13
category: research
---

We’ve seen [rapid progress](https://openai.com/index/accelerating-science-gpt-5/) from AI in fields like math and physics, where ideas can often be evaluated without touching the physical world. Biology is different. Progress runs through the lab, where scientists run experiments that take time and money.

That’s starting to change. Frontier models can now connect directly to lab automation, propose experiments, run them at scale, learn from the results, and decide what to do next. In much of life science, the bottleneck is iteration, and autonomous labs are built to remove that constraint.

In earlier work, we showed that GPT‑5 could [improve wet-lab protocols](https://openai.com/index/accelerating-biological-research-in-the-wet-lab/) through closed-loop experimentation. Here, we show that the same approach can reduce the cost of protein production.

We partnered with [Ginkgo Bioworks](https://www.ginkgo.bio) to connect GPT‑5 to a cloud laboratory—an automated wet lab run remotely through software, where robots execute experiments and return data—and used that lab-in-the-loop setup to optimize a widely used biological process: cell-free protein synthesis (CFPS). Over six rounds of closed-loop experimentation, the system tested more than 36,000 unique CFPS reaction compositions across 580 automated plates. After being provided access to a computer, a web browser, and access to relevant papers, GPT‑5 took three rounds of experimentation to establish a new state of the art in low-cost CFPS, achieving a 40% reduction in protein production cost (and a 57% improvement in the cost of reagents), including novel reaction compositions that are more robust to reaction conditions common in autonomous labs.

## Why cell-free protein synthesis matters

Cell-free protein synthesis (CFPS) is a way to make proteins without growing living cells. Instead of putting DNA into cells and waiting for them to produce a protein, CFPS runs the protein-making machinery in a controlled mixture. That makes it a practical tool for rapid prototyping and testing as scientists can run many experiments quickly and measure results the same day.

Proteins are a big part of what modern biology delivers. Many important medicines are based on proteins. Many diagnostics and research assays depend on proteins. In industrial settings, proteins act as enzymes that make chemical processes cleaner and more efficient. Proteins are even found in your laundry detergent. When protein production becomes faster and cheaper, scientists can usually test more ideas sooner, and reduce the cost of turning early research into something that people can benefit from everyday.

CFPS is already useful for that kind of iteration. The bottleneck is that it is tricky to optimize and gets expensive at scale.

## Cell-free protein synthesis is difficult to optimize and costly

Cell-free protein synthesis requires complex, interacting ingredients: the DNA template encoding the protein to be made, the cell lysate (the soup of cellular machinery from inside cells), and a large number of biochemical components ranging from energy sources to salts. It is incredibly difficult to reason about the system as a whole, and [many](https://pubmed.ncbi.nlm.nih.gov/21520017/) [previous](https://www.nature.com/articles/s41467-020-15798-5?utm_source=chatgpt.com) [studies](https://www.nature.com/articles/s41467-025-58139-0?utm_source=chatgpt.com) have applied different types of machine learning to reduce protein production cost.

Standard cell-free protein synthesis (CFPS) formulations and commercial kits are often priced for human-paced work. Autonomous labs can run thousands of reactions in the time a human team might run dozens. At that scale, the cost of reagents becomes the limiting factor.

CFPS is also difficult to optimize by intuition alone. It’s a mixture of many interacting components. Small changes can matter, but the direction of the effect isn’t always obvious, and the best combinations can be hard to find without running a lot of experiments. Prior approaches have reduced costs, but progress tends to be incremental because exploring the space thoroughly is labor-intensive.

## Connecting GPT‑5 to a robotic lab

We paired GPT‑5 with Ginkgo Bioworks’ cloud laboratory to form a closed-loop autonomous system for cell-free protein synthesis (CFPS) optimization.

GPT‑5 designed batches of experiments. The lab executed them. The results were fed back to the model. The model used that data to propose the next round. We repeated that cycle six times.

*GPT‑5 designed batches of experiments in a standard 384-well plate format, and ran them on Ginkgo Bioworks’ cloud laboratory. Once the experiments finished, the cloud laboratory pushed the data back to GPT‑5, where the model analyzed the outcomes, generated new hypotheses, and designed the next round of experiments.*

To keep the loop grounded in what an autonomous lab can do, we added strict programmatic validation before any experiment ran. That validation enforced that AI-designed experiments were physically executable on the automation platform. It prevented “paper experiments” that look plausible in text but can’t be carried out in a robotic workflow.

Across the full run, the system executed more than 36,000 CFPS reactions across 580 automated plates. This scale matters because it’s what lets patterns emerge. In biology, single experiments are noisy. Throughput and iteration are how you separate signal from random noise. Once GPT‑5 had access to the relevant paper and tools, it took three rounds of experimentation and two months to establish a new state of the art: 40% lower protein production cost compared to the [best prior baseline](https://www.biorxiv.org/content/10.1101/2025.08.01.668204v1.article-info).

*Ginkgo Bioworks’ reconfigurable automation carts. Credit: Ginkgo Bioworks*

## What we learned

We found that the improvements came from identifying combinations that work well together and that hold up in the realities of high-throughput automation.

We found that GPT‑5 identified low-cost reaction compositions that humans had not previously tested in this configuration. Cell-free protein synthesis (CFPS) has been studied for years, but the space of possible mixtures is still large. When you can propose and execute thousands of combinations quickly, you can find workable regions that are easy to miss with a manual workflow.

We also found that high-throughput, plate-based experiments often differ from manual, bench-top experiments. Oxygenation can be lower in high-throughput reaction formats. Mixing and geometry can be different. Most CFPS reactions produce much more protein in test tubes than in microtiter plates, because larger scales generally come with more oxygen availability and better mixing. In fact, for plate-based reactions at low volume, GPT‑5 proposed many reactions that out-performed the prior best immediately after getting access to a computer for data analysis and a web browser to search for relevant papers . Overall, GPT‑5 proposed many reagent combinations that performed well under high-throughput constraints, including many that are more robust in low-oxygen conditions common in automated lab settings.

In addition, we found that small changes in buffering, energy regeneration components, and polyamines had an outsized impact relative to their cost. These are not always the first parameters people reach for, but at high throughput, they become testable hypotheses rather than background assumptions.

Finally, the cost structure itself shaped what mattered. In CFPS, costs are now dominated by lysate and DNA. That means yield is the highest-leverage strategy. If you can boost protein output per unit of expensive input, you make meaningful progress on cost even before you chase marginal savings elsewhere.

### Autonomous lab iteration cuts cost while raising protein yield

*Across six rounds of autonomous experimentation, the system steadily improved cell-free protein synthesis, driving costs down while increasing protein yield. Results are shown as reaction cost versus protein titer for each round, with the best tradeoffs forming a frontier. Larger points mark the lowest cost-per-gram achieved in each round, and the star/dotted reference indicates the prior state-of-the-art benchmark in 384-well plates (Olsen et al., 2025). A closer look at the later rounds highlights the final gains, and a round-by-round summary shows the best cost-per-gram decreasing over time.*

## Limitations

These results were demonstrated on one protein, sfGFP, and one cell-free protein synthesis (CFPS) system. Generalization to other proteins and other CFPS systems still needs to be shown.

Oxygenation and reaction geometry can strongly affect yields, and these factors can vary across scales. Some improvements may be sensitive to these conditions, and understanding those sensitivities is part of what comes next.

Human oversight was required for protocol improvements and reagent handling. The system can design and interpret experiments, but laboratory work still involves practical details that need experienced operators.

## What’s next

We plan to apply lab-in-the-loop optimization to other biological workflows where faster iteration can unlock progress. We see autonomous labs as complementary to models. Models can generate designs, but ultimately biology still requires testing and iteration. Closing the loop between generation and experimentation is how you turn promising ideas into working results.

As we work to accelerate scientific progress safely and responsibly, we also seek to evaluate and reduce risks, particularly those related to biosecurity. These results show that models can reason in the wet lab to improve protocols, and may have implications for biosecurity that we assess and mitigate through our [Preparedness Framework](https://openai.com/index/updating-our-preparedness-framework/). We are committed to building necessary and nuanced safeguards at a model and system level to reduce these risks, as well as develop evaluations to track current levels.

We’re grateful to our partners at Ginkgo Bioworks and the teams who helped design, run, and support the automated cloud laboratory behind this work.
