---
title: "Bringing the magic: Google breaks open a bottleneck in quantum computing"
source: https://blog.google/innovation-and-ai/models-and-research/quantum-computing/magic-state-cultivation-quantum-computing/
site: google-blog
date: 2026-10-15
authors: Emma Rosenfeld
crawled: 2026-10-16
---

Google Quantum AI has demonstratively opened up a key bottleneck in quantum computing: we’ve shown that “magic state cultivation” works in practice on our Willow processor, reducing errors about 40x compared to without it. This breakthrough, published today in [Science](https://www.science.org/doi/10.1126/science.aee7961), is a crucial step towards scaling up quantum computing to practical use.

## The "magic state" bottleneck

Since 2004, long before quantum computing was a practical engineering pursuit, researchers have foreseen a particularly tricky bottleneck.

To achieve “universal” quantum computing and execute useful programs, you need to be able to run (and [error-correct](https://research.google/blog/making-quantum-error-correction-work/)) a specific set of quantum operations. You can do this by first creating what are called "magic states," so dubbed because they can help you create the operations you need for going beyond classical computing.

But there’s a catch: creating high-quality, error-corrected magic states is incredibly resource-heavy. Some estimates have shown that up to 95% of a quantum computer’s entire capacity might need to be dedicated to making them — leaving little room for actual computing. An extra challenge is that once you use a magic state, you can’t re-use it, making magic states a scarce resource.

So for 20 years, researchers have been chipping away at this cost of magic, bringing it lower and lower.

## How we made this breakthrough

In 2024, Google Quantum AI researchers Craig Gidney, Noah Shutty, and Cody Jones harnessed an idea from the literature, refined it, and developed what we now call “magic state cultivation.” Their approach promised an especially large reduction. The idea was that cultivation would act like a filter. You would inject a noisy state into a small region on a quantum chip, and then run a series of highly coordinated measurements to check for errors and remove any flawed attempts. Craig and team showed how that would let you grow, or “cultivate,” an exceptionally pure, low-error quantum state that you could simultaneously adapt into a larger, useful encoding.

On paper, it looked great. If we could make this idea actually work on our quantum hardware, it could substantially reduce the size of the quantum computer needed for practical tasks.

In practice — and on par with developing many new technologies — it required a whole series of technical innovations and engineering.

As just one example, when first testing the cultivation protocol, Google Quantum AI research scientist Emma Rosenfeld was seeing data that seemed to defy the laws of physics. After months of confusion, simulations, discussions with colleagues, and consistency checks, she found that it arose from an incorrect assumption in the team’s go-to measurement technique. Specifically, a particular kind of noise in the lab caused by electrical equipment drift and temperature variation was interfering with the benchmark’s validity. The solution required a pivot in both our theoretical and engineering approaches. The team added extra control to the system to reduce the impact of that noise, and invented a new benchmarking technique to solve the issue more fundamentally, by using cultivation as a tool to measure itself.

With this and many more algorithmic innovations and engineering solutions, we established a new state-of-the-art in quantum metrology. On Google Quantum AI's Willow processor, our protocol achieved an extraordinary 40-fold reduction in errors relative to un-cultivated states. And we got T-states with a record logical fidelity of 99.99%.

Now published in [Science](https://www.science.org/doi/10.1126/science.aee7961), this work is the first demonstration of a practical solution to one of quantum computing's most severe resource bottlenecks. It demonstrates, on real hardware, that we can efficiently create these crucial magic states.

## Our findings and the future

We also took the first steps in demonstrating that Craig and others’ theories are compatible with our quantum computing architecture. We learned how to successfully switch between “color codes” (one newer type of quantum error correction, ideal for cultivation) and “surface codes” (another, more established method), grafting states from a distance-3 color code to a distance-5 surface code. Originally developed in the 2024 theory paper, this grafting protocol showed that in practice, purified states can survive and transfer smoothly inside our hardware.

Of course, we still need to demonstrate magic state cultivation at a larger scale to make it realistic for practical quantum computing, and plenty of technical challenges remain. But this achievement takes a key theoretical idea and turns it into an experimentally demonstrated reality. It brings us one step closer to our goal at [Google Quantum AI](http://quantumai.google/): building a useful, error-corrected quantum computer to solve otherwise unsolvable problems.
