---
title: "Early experiments in accelerating science with GPT‑5"
date: 2025-11-20
source: https://openai.com/index/accelerating-science-gpt-5/
crawled: 2026-09-13
category: research
---

Science shapes everything from human health to energy production, from national security to our understanding of the universe. If AI can accelerate science—shortening the time it takes to generate new ideas, or to move from an idea to a tested result—the benefits compound across society.

But the pace of innovation remains a constraint. Even when the right idea exists, turning it into a product or treatment can take years. In a [recent survey](https://openaiglobalaffairs.substack.com/p/speeding-up-science-with-corrected), 60 percent of people in the U.S. said scientific and medical breakthroughs reach them too slowly; 73 percent said we need better ways to accelerate discovery; and 69 percent identified scientific leadership as a top national priority.

Today, we’re releasing “[Early science acceleration experiments with GPT‑5](https://cdn.openai.com/pdf/4a25f921-e4e0-479a-9b38-5367b47e8fd0/early-science-acceleration-experiments-with-gpt-5.pdf),” a paper co-authored with collaborators at universities and national laboratories including Vanderbilt, UC Berkeley, Columbia, Oxford, Cambridge, Lawrence Livermore National Laboratory, and The Jackson Laboratory. It compiles early case studies across math, physics, biology, computer science, astronomy, and materials science in which GPT‑5 helped researchers synthesize known results in a novel way, conduct powerful literature review, accelerate tough computations, and even generate novel proofs of unsolved propositions. The paper also documents limitations. Our goal is to give the community a clear view of what these systems can and cannot do today in research settings.

These case studies show how, in the hands of experts, GPT‑5 is accelerating scientific discovery, and why that acceleration matters:

- **Biology**: In a study led by Derya Unutmaz, M.D., scientists spent months trying to explain a puzzling change in human immune cells. GPT‑5 identified the likely mechanism within minutes from an unpublished chart and suggested an experiment that proved it. This kind of speed could help researchers understand diseases faster and develop better treatments.
- **Mathematics**: In another case, researchers Mehtaab Sawhney and Mark Sellke were tackling a decades-old open problem originally proposed by Paul Erdős. They were stuck on the final step, and GPT‑5 contributed a new idea about how one odd number breaks the pattern, which helped them complete the proof. Advances like this strengthen the mathematical foundations that many algorithms and security techniques ultimately rely on.
- **Algorithms & optimization:** Researchers Sébastien Bubeck and Christian Coester were testing whether a common decision-making method used in robotics and routing was as reliable as people assumed. GPT‑5 found a new, clear example showing the method can fail and also improved a classic result in optimization, the math used to figure out the best way to solve a problem. This type of advance helps engineers better understand the decision-making systems used in robotics, routing, and other real-world applications.

## What is OpenAI for Science?

The mission of OpenAI for Science is to accelerate scientific discovery: to help researchers explore more ideas, test hypotheses faster, and uncover insights that would otherwise take significant time. We do this by pairing frontier models with the right tools, workflows, and collaborations.

We work closely with researchers across academia, industry, and national labs. These collaborations help us understand where the models are useful, where they fail, and how to integrate them into the scientific process—from literature review and proof generation to modeling, simulation, and experimental design.

Our approach combines two complementary beliefs. Specialized scientific tools, such as simulation engines, protein databases, and computer algebra systems, are essential for efficiency and precision. At the same time, scaling foundation models continues to unlock new reasoning abilities: connecting ideas across fields, sketching proofs, proposing mechanisms, and navigating large literatures conceptually rather than by keyword. Where specialized tools exist, we want to use them; where general reasoning is required, we build models designed to handle it. Both paths reinforce each other.

## How scientists are working with GPT‑5 today

The most meaningful progress comes from human–AI teams. Scientists set the agenda: they define questions, choose methods, critique ideas, and validate results. GPT‑5 contributes breadth, speed, and the ability to explore many directions in parallel.

Using GPT‑5 effectively is a skill. Researchers learn how to pose questions, when to push back, how to break problems into steps, and what to validate independently. Productive work often looks like dialogue—researcher and model iterating until a promising direction emerges or the idea is discarded

## The current state of GPT‑5 in scientific work

Across these early studies, GPT‑5 appears able to shorten parts of the research workflow when used by experts. It does not run projects or solve scientific problems autonomously, but it can expand the surface area of exploration and help researchers move faster toward correct results.

- One emerging capability is conceptual literature search. GPT‑5 can often identify deeper relationships between ideas and retrieve relevant material across languages and less accessible sources. Researchers report finding references, connections, and theses they did not previously know.
- In mathematics and theoretical computer science, where structure is explicit and feedback loops are fast, GPT‑5 is especially helpful. Mathematicians have used GPT‑5 to generate viable proof outlines in minutes, transforming work that otherwise might have taken days or weeks. In physics and computational domains, the model can propose simplifying transformations or point to analogous structures in other fields.
- In biology and other empirical sciences, the model can propose mechanisms and design experiments to validate these hypotheses in the wet lab.

We are beyond the point where models only summarize existing knowledge. Now, early contributions from GPT‑5 can meaningfully assist researchers under expert oversight. The pace of improvement suggests the potential for deeper acceleration as capabilities and tools advance.

## What this looks like in practice: a few case studies

### Independent rediscovery of known results at the scientific frontier

Optimization is the math of finding the “best” option—like the lowest training loss or the shortest route in a network. Gradient descent is a basic optimization method that takes repeated small steps downhill on a function. A recent [theorem](https://arxiv.org/abs/2503.10138) by Guy Barzilai, Ohad Shamir, and Moslem Zamani asked when the sequence of values visited by gradient descent forms a convex curve over time (a curve with no dips), which makes the algorithm’s behavior easier to analyze and control. The first version of the paper showed this only for very small, conservative step sizes.

Sébastien Bubeck gave GPT‑5 the weaker version of the result and asked if the condition could be improved, and the model proposed a sharper step-size bound and a cleaner, more standard proof that he then checked carefully by hand; with more thinking time, an internal run of the model even derived the optimal bound from scratch.

**GPT‑5’s contribution:** GPT‑5 helped Sébastien Bubeck explore a sharper step-size condition and suggest a cleaner proof for a recent convex optimization theorem, which he verified independently.

- [Read more on page 3](https://cdn.openai.com/pdf/4a25f921-e4e0-479a-9b38-5367b47e8fd0/early-science-acceleration-experiments-with-gpt-5.pdf)

In general relativity, rotating black holes are described by the Kerr solution, and waves moving around them satisfy a complicated differential equation. Physicists look for symmetries of such equations—transformations that leave them unchanged—because symmetries lead to conserved quantities and simple structure. Recent work by Alex Lupsasca showed that the Kerr wave equation has a hidden symmetry structure forming an SL(2,ℝ) algebra, which helps explain why certain tidal responses vanish.

When we asked GPT‑5 Pro directly about the full Kerr problem, it initially failed and reported no interesting symmetries. After Lupsasca gave it a simpler “warm-up” version of the same structure in flat space, we returned to the Kerr case; this time, after about 18 minutes of internal reasoning, the model produced the full set of symmetry generators that close into SL(2,ℝ), matching the human result.

**GPT‑5’s contribution:** GPT‑5 Pro reconstructed the hidden SL(2,ℝ) symmetry algebra of the Kerr black hole wave equation once given an appropriate warm-up problem, and Lupsasca confirmed the result.

- [See the example](https://chatgpt.com/share/68b006eb-ee0c-8005-903f-bf92065d7e03/)
- [Read more on page 7](https://cdn.openai.com/pdf/4a25f921-e4e0-479a-9b38-5367b47e8fd0/early-science-acceleration-experiments-with-gpt-5.pdf)

A key question in modern immunotherapy, especially in CAR-T cancer treatments that rely on engineered T cells, is how to keep beneficial T cells active and durable without pushing them into an exhausted, dysfunctional state. Established literature has shown that transiently limiting glucose metabolism can durably reprogram T cells to be more proinflammatory. In an earlier study, Derya Unutmaz and colleagues briefly treated human CD4+ T cells (a key class of immune cells) with 2-deoxyglucose (2DG), a compound that interferes with glucose metabolism. After removing 2DG and then priming the CD4+ T cells with IL-2 (a signaling molecule that tells T cells to proliferate), they saw a lasting shift toward a proinflammatory Th17-like state—a subtype of T cells involved in both protection and autoimmune disease—and spent months of experiments and reading to arrive at a plausible mechanism explaining this effect.

Years later, he gave GPT‑5 Pro an unpublished figure of flow cytometry scatterplots showing different T cell subsets after treatment with varying glucose and 2DG levels—and asked what might explain the data and what experiments to run next. In about a dozen minutes of back-and-forth, the model suggested that disrupted N-linked glycosylation (how cells attach sugar chains to proteins) during priming was the driver, and predicted that memory (rather than naïve) T cells were responsible. GPT‑5 then proposed specific follow-up experiments, including an elegant mannose rescue experiment that restored N-glycosylation without restoring glycolysis. The lab had previously conducted the mannose rescue experiment, and the results matched the model predictions exactly.

GPT‑5 Pro was then able to analyze unpublished data of CD8+ T cells pulsed with 2DG, and predicted that transient 2DG exposure during CAR-T generation would lead to enhanced killing efficiency against target cancer cell lines. GPT‑5 Pro’s predictions matched the lab’s unpublished experimental data.

**GPT‑5’s contribution:** GPT‑5 analyzed unpublished data to derive non-obvious and valuable mechanistic hypotheses, identified the acting T-cell subpopulation, and suggested follow-up experiments, which Unutmaz’s lab later tested and confirmed.

- [Read more on page 11](https://cdn.openai.com/pdf/4a25f921-e4e0-479a-9b38-5367b47e8fd0/early-science-acceleration-experiments-with-gpt-5.pdf)

### Deep literature search

Nikita Zhivotovskiy and his collaborators proved a new theorem in convex geometry—the study of “well-behaved” shapes where any line between two points stays inside the shape. Convex geometry underlies many models in machine learning and statistics. Once the theorem was done, the natural next question was: where else could this result be useful?

Instead of guessing search terms and scanning the literature by hand, Zhivotovskiy gave GPT‑5 the formal statement of the theorem and asked which areas it might connect to. The model pointed to work in density estimation, learning theory, and multi-objective optimization, and surfaced specific references, including several he had not seen and some in other languages.

**GPT‑5’s contribution:** GPT‑5 helped Nikita Zhivotovskiy identify concrete connections and references across several fields, including materials he had not encountered.

- [See the example](https://chatgpt.com/share/690db28a-1b00-800c-b9e2-42490f586955/)
- [Read more on page 21](https://cdn.openai.com/pdf/4a25f921-e4e0-479a-9b38-5367b47e8fd0/early-science-acceleration-experiments-with-gpt-5.pdf)

Paul Erdős posed more than a thousand problems, many of which are tracked on a public website. Some problems are still listed as “open” even though solutions exist in obscure journals or non-English papers. Mehtaab Sawhney and Mark Sellke used GPT‑5 as a literature-search assistant over this database: for each supposedly open problem, they asked it to search for solutions or major partial progress.

GPT‑5 found full solutions for several problems still marked open, identified substantial partial results for others, and flagged a misprint in one problem statement. For Erdős Problem #848, human comments on the site had already outlined much of the structure; GPT‑5 proposed a key density estimate, and Sawhney and Sellke corrected and tightened it into a complete proof that closed the problem.

**GPT‑5’s contribution:** GPT‑5 assisted in locating missed solutions and proposed a density estimate that Sawhney and Sellke refined into a complete proof of Erdős Problem #848.

- [See the example](https://chatgpt.com/share/68f124d4-30b4-8005-b2d9-fcb64fc1e4ea/)
- [Read more on page 24](https://cdn.openai.com/pdf/4a25f921-e4e0-479a-9b38-5367b47e8fd0/early-science-acceleration-experiments-with-gpt-5.pdf)

Error-correcting codes add redundancy to data so you can recover information even when bits are corrupted. This project examined a special kind of binary code where each position corresponds to an edge in a graph, and the goal is to rule out any codeword that looks like a “clique” (a fully connected set of nodes). The challenge was to determine how many parity checks are fundamentally required to prevent these structured errors. GPT‑5 reframed the question using quadratic equations over a finite field and highlighted a classical result, the Chevalley–Warning theorem, which immediately pointed to the correct lower bound—showing that only about half as many constraints were needed as previously thought.

An unexpected twist emerged afterward: the exact same bound, and essentially the same proof, had appeared years earlier in a short research paper. GPT‑5 had reproduced the argument without citing its source, only identifying the prior work when asked again in a fresh session. This underscored an important lesson for AI-assisted mathematics: models can generate correct and elegant reasoning, but they may not reliably attribute where those ideas originally came from. Careful verification and attention to attribution remain essential.

**GPT‑5’s contribution:** GPT‑5 provided the key reformulation and the classical theorem that led to the optimal lower bound. However, the model did not identify the prior publication until explicitly asked, underscoring the need for careful human checks on attribution.

- [Read more on page 28](https://cdn.openai.com/pdf/4a25f921-e4e0-479a-9b38-5367b47e8fd0/early-science-acceleration-experiments-with-gpt-5.pdf)

### Working in tandem with AI

Tim Gowers, a Fields Medal–winning combinatorialist, ran a series of experiments treating GPT‑5 as a “research partner” rather than a tool for homework-style problems. He gave the model hard combinatorics questions he was actively thinking about and asked it to suggest constructions, find counterexamples, or critique partial arguments.

In multiple cases, GPT‑5 quickly spotted flaws or missing cases in candidate constructions and proposed simpler alternatives or counterexamples; in others, it stalled or failed to make progress. Gowers’ overall conclusion was that the model is already useful as a very fast, very knowledgeable critic that can stress-test ideas and save time, even though it does not yet meet his bar for full co-authorship.

**GPT‑5’s contribution:** GPT‑5 acted as a fast critic for Tim Gowers, spotting flaws, missing cases, and simpler alternatives during exploratory combinatorics work.

- [Read more on page 31](https://cdn.openai.com/pdf/4a25f921-e4e0-479a-9b38-5367b47e8fd0/early-science-acceleration-experiments-with-gpt-5.pdf)

Cosmology uses simplified models to describe the large-scale behavior of the universe, including dark energy and the expansion history. Those models often exist in several mathematically equivalent forms, and small algebraic slips can derail a calculation. Robert Scherrer used GPT‑5 to sanity-check derivations, explore toy versions of cosmological models, and translate between different parameterizations of dark energy.

GPT‑5 was particularly useful in catching algebraic mistakes, suggesting equivalent formulations of the same physical idea, and pointing Scherrer to existing results in the literature that matched the models he was independently deriving. This reduced the friction between having an idea on paper and getting it into a form that could be compared with data.

**GPT‑5’s contribution:** GPT‑5 assisted Robert Scherrer by checking derivations, suggesting equivalent formulations, and pointing to matching results in the literature.

- [Read more on page 37](https://cdn.openai.com/pdf/4a25f921-e4e0-479a-9b38-5367b47e8fd0/early-science-acceleration-experiments-with-gpt-5.pdf)

Fusion and plasma physics involve modeling hot, dense plasmas where small changes in initial conditions can lead to very different behavior. Running and interpreting these simulations is expensive and time-consuming. This work used GPT‑5 to help build and analyze a simplified reaction–diffusion model of thermonuclear burn propagation, interpret complex outputs, and explore how different density profiles affect burn performance. The model helped run parameter sweeps and identify a ridge of optimal profiles where burn fronts travel fastest.

GPT‑5 also assisted in proposing a theoretical explanation for these numerical patterns, using power-balance arguments to explain why certain profiles perform better and suggesting simple engineering rules to guide future designs. While the model occasionally produced unstable simulations or overly confident conclusions, expert oversight allowed rapid correction, making it much faster to move from “something strange is happening in this regime” to “here is a plausible explanation and a concrete test.”

**GPT‑5’s contribution:** GPT‑5 helped construct the reduced-physics model, explore parameter space, and propose physical explanations.

- [Read more on page 40](https://cdn.openai.com/pdf/4a25f921-e4e0-479a-9b38-5367b47e8fd0/early-science-acceleration-experiments-with-gpt-5.pdf)

### New scientific results obtained with AI

Paul Erdős posed a problem about finding the largest set of positive integers with a surprising rule: for any two numbers in the set, the product of those two numbers plus one must always be divisible by a perfect-square prime factor. Erdős guessed what the largest such set should look like, but the problem remained open for decades.

Sawhney and Sellke explored the structure of the problem and then asked GPT‑5 to help analyze how a single “out-of-place” number would affect the entire set. GPT‑5 suggested a clearer way to show that if even one number does not fit a specific pattern, it forces contradictions across almost all other numbers. That idea turned out to be the missing step. With it, the researchers completed a full proof showing that Erdős’s original guess was correct.

**GPT‑5’s contribution**: GPT‑5 surfaced the key insight about how one number constrains all others, enabling the authors to finish the proof of Erdős Problem 848.

- [See the example](https://chatgpt.com/share/68ec50da-cf00-8005-b5f6-b683506e5853)
- [Read more on page 53](https://cdn.openai.com/pdf/4a25f921-e4e0-479a-9b38-5367b47e8fd0/early-science-acceleration-experiments-with-gpt-5.pdf)

Online algorithms make decisions step by step without knowing the future—for example, deciding how to move a system when constraints are revealed over time. In the convex body chasing problem, the algorithm must stay inside a moving convex region while keeping total movement small. A central question is the best possible competitive ratio: how much worse an online algorithm can be, in the worst case, than an ideal offline algorithm that sees the whole sequence in advance.

Christian Coester used GPT‑5 to brainstorm hard instances and constructions that might force any online algorithm to perform badly. The model highlighted a particular geometric construction that, after refinement and checking by Coester, led to a cleaner and stronger lower bound on the competitive ratio than was previously known.

**GPT‑5’s contribution:** GPT‑5 suggested a geometric construction that Christian Coester refined into a stronger lower bound for an online algorithm problem.

- [Read more on page 61](https://cdn.openai.com/pdf/4a25f921-e4e0-479a-9b38-5367b47e8fd0/early-science-acceleration-experiments-with-gpt-5.pdf)

The team studied a graph theory problem about counting small patterns—paths, stars, and “wyes”—inside trees (graphs with no cycles). Previous work had proved one inequality relating these counts and conjectured a second one, which remained unproved. Using a custom math scaffolding around GPT‑5, the authors first asked the model to re-prove the known inequality, then to attack the conjectured one.

GPT‑5 produced short, self-contained proofs of both inequalities, relying on a different and more elegant argument than the original human proof; Bubeck, Sellke, and Yin then checked and adopted the model’s argument in their write-up.

**GPT‑5’s contribution:** GPT‑5 generated short proofs of two inequalities in trees, including a conjectured one, and the authors independently checked and adopted the argument.

- [Read more on page 69](https://cdn.openai.com/pdf/4a25f921-e4e0-479a-9b38-5367b47e8fd0/early-science-acceleration-experiments-with-gpt-5.pdf)

Researchers studied a simple model of a growing network where each new node attaches to earlier nodes with a probability influenced by a hidden parameter www. The challenge is that once the network is grown, you only see the final unlabeled tree—not the hidden labels or the attachment rules that produced it. The open question was whether www could be recovered at all from just this final structure.

The team asked GPT‑5 to reason about what global patterns in the final tree might reliably reflect the value of www. The model proposed focusing on a surprisingly accessible statistic: the long-run fraction of nodes that end up as leaves. GPT‑5 outlined how this leaf fraction converges to a simple, strictly increasing function of www, meaning that www can be read off directly from the shape of the tree. With this guidance, the authors produced a complete proof showing that the parameter is indeed identifiable.

**GPT‑5’s contribution:** GPT‑5 highlighted the key observable—leaf fraction—that unlocks a clean, provable method for recovering the hidden parameter www from a single snapshot of the final network.

- [Read more on page 75](https://cdn.openai.com/pdf/4a25f921-e4e0-479a-9b38-5367b47e8fd0/early-science-acceleration-experiments-with-gpt-5.pdf)

## Limitations

These case studies are curated illustrations of where GPT‑5 has been useful; they are not a systematic sample, and they do not capture the full range of failure modes. Expert oversight remains essential. GPT‑5 can sometimes hallucinate citations, mechanisms, or proofs that appear plausible; it can be sensitive to scaffolding and warm-up problems; it sometimes misses domain-specific subtleties; and it can follow unproductive lines of reasoning if not corrected. These are active areas of research, and we are working with collaborators to measure and mitigate these failures as we refine future systems.

## What’s next

Taken together, these early studies show that GPT‑5 is beginning to help with new types of scientific work. The model is not autonomous, but in expert hands it can help prove theorems, rediscover and extend structures, surface cross-field connections, and generate mechanisms and experiments for scientists to validate.

We also see a trajectory in which these systems improve with more time and compute. If GPT‑5 can meaningfully assist with some research questions in 20 minutes, we expect deeper results when models can spend hours or days reasoning about a problem. Combined with world-class scientists, this points toward the possibility of a step-change in scientific productivity over time.
