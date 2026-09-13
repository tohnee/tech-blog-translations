---
title: "An OpenAI model has disproved a central conjecture in discrete geometry"
date: 2026-05-20
source: https://openai.com/index/model-disproves-discrete-geometry-conjecture/
crawled: 2026-09-13
category: research
---

For nearly 80 years, mathematicians have studied a deceptively simple question: if you place nnn points in the plane, how many pairs of points can be exactly distance 111 apart?

This is the planar unit distance problem, first posed by Paul Erdős in 1946. It is one of the best-known questions in combinatorial geometry, easy to state and remarkably difficult to resolve. The 2005 book *Research Problems in Discrete Geometry*, by Brass, Moser, and Pach, calls it “possibly the best known (and simplest to explain) problem in combinatorial geometry.” Noga Alon, a leading combinatorialist at Princeton, describes it as “one of Erdős’ favorite problems.” Erdős even offered a monetary prize for resolving this problem.

Today, we share a breakthrough on the unit distance problem. Since Erdős’s original work, the prevailing belief has been that the “square grid” constructions depicted further below were essentially optimal for maximizing the number of unit-distance pairs. An internal OpenAI model has disproved this longstanding conjecture, providing an infinite family of examples that yield a polynomial improvement. The proof has been checked by a group of external mathematicians. They have also written a companion paper explaining the argument and providing further background and context for the significance of the result.

The result is also notable for how it was found. The proof came from a new general-purpose reasoning model, rather than from a system trained specifically for mathematics, scaffolded to search through proof strategies, or targeted at the unit distance problem in particular. As part of a broader effort to test whether advanced models can contribute to frontier research, we evaluated it on a collection of Erdős problems. In this case, it produced a proof resolving the open problem.

This proof is an important milestone for the math and AI communities. It marks the first time that a prominent open problem, central to a subfield of mathematics, has been solved autonomously by AI. It also demonstrates the depth of reasoning these systems now support. Mathematics provides a particularly clear testbed for reasoning: the problems are precise, potential proofs can be checked, and a long argument only works if the reasoning holds together from beginning to end. The method by which the problem was solved is also notable. The proof brings unexpected, sophisticated ideas from algebraic number theory to bear on an elementary geometric question.

Fields medalist Tim Gowers, writing in the companion paper, calls the result “a milestone in AI mathematics.” According to leading number theorist Arul Shankar, “In my opinion this paper demonstrates that current AI models go beyond just helpers to human mathematicians – they are capable of having original ingenious ideas, and then carrying them out to fruition”.

Mathematicians on the result

Noga Alon

Tim Gowers

Arul Shankar

Jacob Tsimerman

- Noga Alon
- Tim Gowers
- Arul Shankar
- Jacob Tsimerman

The proof is available [here](https://cdn.openai.com/pdf/74c24085-19b0-4534-9c90-465b8e29ad73/unit-distance-proof.pdf). The companion paper by leading external mathematicians is available [here](https://cdn.openai.com/pdf/74c24085-19b0-4534-9c90-465b8e29ad73/unit-distance-remarks.pdf). You can find an abridged version of the model’s chain of thought [here](https://cdn.openai.com/pdf/1625eff6-5ac1-40d8-b1db-5d5cf925de8b/unit-distance-cot.pdf).

*Previously known construction of many unit distances from a rescaled square grid.*

## The unit distance problem

Let u(n)u(n)u(n) be the largest possible number of unit-distance pairs among nnn points in the plane. Examples attaining linear growth rate are easy to construct: placing nnn points in a line gives n−1n-1n−1 pairs, while a square grid gives about 2n2n2n pairs. The previously best known construction, coming from a rescaled square grid, turns out to give even more: n1+C/log⁡log⁡(n)n^{1 + C / \log \log(n)}n1+C/loglog(n) for a constant CCC. Since log⁡log⁡(n)\log \log(n)loglog(n) tends to infinity with nnn, the additional term in the exponent tends to 000, meaning these constructions achieve growth only slightly faster than linear. For decades, it was widely believed that this rate was essentially the best possible, and no construction could improve significantly over the square grid. In technical terms, Erdős conjectured an upper bound of n1+o(1)n^{1+o(1)}n1+o(1) in which the additional o(1)o(1)o(1) indicates a term tending to 000 with nnn.

Our new result disproves this conjecture. More precisely, for infinitely many values of nnn, the proof constructs configurations of nnn points with at least n1+δn^{1+\delta}n1+δ unit-distance pairs, for some fixed exponent δ>0\delta > 0δ>0. (The original AI proof does not give an explicit δ\deltaδ, but a forthcoming refinement due to Princeton mathematics professor Will Sawin has shown one can take δ=0.014\delta=0.014δ=0.014.)

The history of the problem helps to see why the result is surprising. The best known lower bound had been essentially unchanged since Erdős’s original 1946 construction. The best upper bound, O(n4/3)O(n^{4/3})O(n4/3), dates to work by Spencer, Szemerédi, and Trotter in 1984, and despite later refinements and related structural work by Székely, Katz and Silier, Pach, Raz, and Solymosi and by others, the upper bound has remained essentially unchanged. As evidence in favor of the conjecture, Matoušek and Alon-Bucić-Sauermann studied the problem with non-Euclidean distances in the plane, and proved that "most" of these non-Euclidean distances obey the conjecture in some sense.

Surprisingly, the key ingredients of the construction come from a very different part of mathematics known as algebraic number theory, which studies concepts like factorization in extensions of the integers known as algebraic number fields.

*After verifying the initial proof, we investigated the success rate of our models on this problem with varying amounts of test-time compute. The results are shown here.*

## New techniques from algebraic number theory

At a high level, the proof begins with a familiar geometric idea and pushes it in an unexpected direction.

Erdős’s original lower bound can be understood through the Gaussian integers: numbers of the form a+bia+bia+bi, where aaa and bbb are integers and iii is the square root of −1-1−1. The Gaussian integers extend the ordinary integers and, like them, enjoy properties such a unique factorization into primes. Such extensions of the ordinary integers or rationals are known as algebraic number fields. The new argument replaces the Gaussian integers by more complicated generalizations from algebraic number theory with richer symmetries that can create many more unit-length differences.

The precise argument uses tools such as infinite class field towers and Golod–Shafarevich theory to show the number fields required for the argument actually exist. These ideas were well-known to algebraic number theorists, but it came as a great surprise that these concepts have implications for geometric questions in the Euclidean plane.

## What this means for mathematics

This result marks an important moment in the interaction between AI and mathematics: an AI system has autonomously resolved a longstanding open problem at the center of an active field. It also offers an early glimpse of a new kind of collaboration between AI and human mathematicians. In this case, the companion work by external mathematicians paints a substantially richer picture than the original solution alone.

As Thomas Bloom writes in the companion note:

“*When assessing the importance and influence of an AI-generated proof, a question I ask myself is: has this taught us something new about the problem? Do we understand discrete geometry better now? I think the answer is a moderated yes: this shows that there is a lot more that number theoretic constructions have to say about these sorts of questions than we suspected; moreover, that the number theory required can be very deep. No doubt many algebraic number theorists will be taking a close look at other open problems in discrete geometry in the coming months.*”

The unexpected connection between algebraic number theory and discrete geometry revealed by the solution is part of what makes the result notable. It does not simply settle a specific conjecture, but may provide mathematicians with a bridge to begin exploring further related problems.

Bloom also points toward a broader possibility:

“*The frontiers of knowledge are very spiky, and no doubt the coming months and years will see similar successes in many other areas of mathematics, where long-standing open problems are resolved by an AI revealing unexpected connections and pushing the existing technical machinery to its limit. AI is helping us to more fully explore the cathedral of mathematics we have build over the centuries; what other unseen wonders are waiting in the wings?*”

This result provides a promising example: AI contributing not only a solution, but a mathematical discovery whose significance becomes clearer and richer through subsequent human understanding.

## Why this matters

The takeaway is bigger than this particular result. Better mathematical reasoning can make AI a stronger research partner: something that can hold together difficult lines of thought, connect ideas across distant areas of knowledge, surface promising paths experts may not have prioritized, and help researchers make progress on problems that would otherwise be too complex or time-intensive to tackle.

Those capabilities matter beyond mathematics. If a model can keep a complicated argument coherent, connect ideas across distant areas of knowledge, and produce work that survives expert scrutiny, those are also useful abilities in biology, physics, materials science, engineering, and medicine, and they are part of our longer-term path toward more automated research: systems that can help scientists and engineers explore more ideas and pursue harder technical questions.

AI is about to start taking a very serious role in the creative parts of research, and most importantly AI research itself. While this progress is not unexpected, it reinforces the urgency we feel about understanding this next phase of AI development, the challenges of aligning very intelligent systems, and the future of human-AI collaboration.

That future still depends on human judgment. Expertise becomes more valuable, not less. AI can help search, suggest, and verify. People choose the problems that matter, interpret the results, and decide what questions to pursue next.
