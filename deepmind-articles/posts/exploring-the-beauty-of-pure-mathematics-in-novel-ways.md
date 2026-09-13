---
title: "Exploring the beauty of pure mathematics in novel ways"
source: https://deepmind.google/blog/exploring-the-beauty-of-pure-mathematics-in-novel-ways/
site: deepmind
date: 2021-12-01
authors: 
crawled: 2026-09-13
---

More than a century ago, [Srinivasa Ramanujan](https://en.wikipedia.org/wiki/Srinivasa_Ramanujan) shocked the mathematical world with his extraordinary ability to see remarkable patterns in numbers that no one else could see. The self-taught mathematician from India described his insights as deeply intuitive and spiritual, and patterns often came to him in vivid dreams. These observations captured the tremendous beauty and sheer possibility of the abstract world of pure mathematics. In recent years, we have begun to see AI make breakthroughs in [areas involving deep human intuition](https://deepmind.com/research/case-studies/alphago-the-story-so-far), and more recently on some of the [hardest problems across the sciences](https://deepmind.com/blog/article/alphafold-a-solution-to-a-50-year-old-grand-challenge-in-biology), yet until now, the latest AI techniques have not assisted in significant results in pure maths research.

As part of [DeepMind's mission](https://deepmind.com/about) to solve intelligence, we explored the potential of machine learning (ML) to recognize mathematical structures and patterns, and help guide mathematicians toward discoveries they may otherwise never have found — demonstrating for the first time that AI can help at the forefront of pure mathematics.

[Our research paper](https://www.nature.com/articles/s41586-021-04086-x), published today in the journal Nature, details our collaboration with top mathematicians to apply AI toward discovering new insights in two areas of pure mathematics: topology and representation theory. With [Professor Geordie Williamson](https://www.maths.usyd.edu.au/u/geordie/) at the University of Sydney, we discovered a new formula for a conjecture about permutations that has remained unsolved for decades. With [Professor Marc Lackenby](https://www.maths.ox.ac.uk/people/marc.lackenby) and [Professor András Juhász](https://www.maths.ox.ac.uk/people/andras.juhasz) at the University of Oxford, we have discovered an unexpected connection between different areas of mathematics by studying the structure of knots. These are the first significant mathematical discoveries made with machine learning, according to the top mathematicians who reviewed the work. We’re also releasing full companion papers on arXiv for each result that will be submitted to appropriate mathematical journals ([permutations paper](https://arxiv.org/abs/2111.15161); [knots paper](https://arxiv.org/abs/2111.15323)). Through these examples, we propose a model for how these tools could be used by other mathematicians to achieve new results.

![An animated knot made with one strand of unbroken string.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6224d0dee2f1f82cd4b977c9_unnamed.gif)

A knot is one of the fundamental objects in low-dimensional topology. It is a twisted loop embedded in 3 dimensional space.

![A list of letters: A, B, C, D, E. These letters are rearranged with permutation 32415, resulting in a second list of letters: D, B, A, C ,E.](https://lh3.googleusercontent.com/KLNgTiUHc881rOm2g8vsQI8ZUfmEewAEMoYCxOXGImAx35hd2IginLaGn_N-u0oafwkdcrFSEtClnkmlXHaifdGOSqVMNVrrutTUodAw5EtLDbOVHw=w1440)

A permutation is a re-arrangement of an ordered list of objects. The permutation “32415” puts the 1st element in the 3rd location, the 2nd element in the 2nd location and so on.

The two fundamental objects we investigated were knots and permutations.

For many years, computers have been used by mathematicians to generate data to help in the search for patterns. Known as experimental mathematics, this kind of research has resulted in well-known conjectures, such as [the Birch and Swinnerton-Dyer conjecture](https://theconversation.com/millennium-prize-the-birch-and-swinnerton-dyer-conjecture-4242) — one of six [Millennium Prize Problems](https://www.claymath.org/millennium-problems/millennium-prize-problems), the most well-known open problems in mathematics (with a US$1 million prize attached to each). While this approach has been successful and is fairly common, the identification and discovery of patterns from this data has still relied mainly on mathematicians.

Finding patterns has become even more important in pure maths because it’s now possible to generate more data than any mathematician can reasonably expect to study in a lifetime. Some objects of interest — such as those with thousands of dimensions — can also simply be too unfathomable to reason about directly. With these constraints in mind, we believed that AI would be capable of augmenting mathematicians’ insights in entirely new ways.

> It feels like Galileo picking up a telescope and being able to gaze deep into the universe of data and see things never detected before.

Marcus Du Sautoy

Simonyi Professor for the Public Understanding of Science and Professor of Mathematics, University of Oxford

Our results suggest that ML can complement maths research to guide intuition about a problem by detecting the existence of hypothesised patterns with supervised learning and giving insight into these patterns with attribution techniques from machine learning:

With Professor Williamson, we used AI to help discover a new approach to a long-standing conjecture in representation theory. Defying progress for nearly 40 years, the [combinatorial invariance conjecture](https://dl.acm.org/doi/10.1016/j.jcta.2005.12.003)states that a relationship should exist between certain directed graphs and polynomials. Using ML techniques, we were able to gain confidence that such a relationship does indeed exist and to identify that it might be related to structures known as broken dihedral intervals and extremal reflections. With this knowledge, Professor Williamson was able to conjecture a surprising and beautiful algorithm that would solve the combinatorial invariance conjecture. We have computationally verified the new algorithm across more than 3 million examples.

With Professor Lackenby and Professor Juhász, we explored knots - one of the fundamental objects of study in topology. Knots not only tell us about the many ways a rope can be tangled but also have surprising connections with quantum field theory and non-Euclidean geometry. Algebra, geometry, and quantum theory all share unique perspectives on these objects and a long standing mystery is how these different branches relate: for example, what does the geometry of the knot tell us about the algebra? We trained an ML model to discover such a pattern and surprisingly, this revealed that a particular algebraic quantity — the signature — was directly related to the geometry of the knot, which was not previously known or suggested by existing theory. By using attribution techniques from machine learning, we guided Professor Lackenby to discover a new quantity, which we call the natural slope, that hints at an important aspect of structure overlooked until now. Together we were then able to prove the exact nature of the relationship, establishing some of the first connections between these different branches of mathematics.

![A hand-drawn, multicolored mathematical graph representing a directed graph in representation theory, showing nodes labeled with permutations and edges highlighted in various colors, pointing to the algebraic expression "1 + q".](https://lh3.googleusercontent.com/GN9MgcwVWKG5Ki_Vi2Jjzq7aWO0KhGhyFJ9x0skx3btY34EEuLd3v47DtYEBxjs8OyARrei6G74ykckLhi2cGtJga6zpl5445CHRkHfj31bJeGjl0A=w1440)

![A hand-drawn mathematical diagram representing a directed graph in representation theory, showing nodes labeled with permutations, thin black connection lines, and thick paths highlighted in blue, yellow, orange, red, and teal.](https://lh3.googleusercontent.com/mNIhRnUSSUDSD-MHHHH_aPgjYtwMR4VMJnn0ZirNyZJnHzI-Jqbj2Kx8miqCHoQmCPDZ32Rv_wKR87tv4BXwJ8yuviBq8sFnTGZ-DuJj3J4EVk9u6pI=w1440)

We investigated whether ML could shed light on relationships between different mathematical objects. Shown here are two “Bruhat intervals” and their associated “Kazhdan-Lusztig polynomials” - two fundamental objects in representation theory. A Bruhat interval is a diagram that represents all the different ways you could reverse the order of a collection of objects by only swapping two of them at a time. The KL polynomials tell mathematicians something deep and subtle about the different ways that this graph can exist in high dimensional space. Interesting structure only starts to emerge when the Bruhat intervals have 100s or 1000s of vertices.

![A mathematical scatter plot demonstrating a relationship between the algebraic "Signature" of a knot on the y-axis and its geometric "Meridional translation (real)" on the x-axis, with data points colored in a gradient from blue to red according to their "Longitudinal translation" value.](https://lh3.googleusercontent.com/B-LCwTQYk6R-o7WA5V-b6r8jCtSBjahM1UqNzpkyDvLiu3eq9SXPxQPAjJEJSzDp6zMoUjFeiAgimNqz3kWm-NM14ypwppmVE0AGNjFceLyHuQVp=w1440)

Our models highlight previously undiscovered structure that guided us to surprising new mathematical results. Shown here is a striking relationship between the geometry and signature of a knot. The geometry of a knot has to do with its shape (e.g. it’s volume) when measured in a canonical way. The signature is an algebraic invariant which can be calculated by looking at the way the knot crosses itself and twists.

The use of learning techniques and AI systems holds great promise for the identification and discovery of patterns in mathematics. Even if certain kinds of patterns continue to elude modern ML, we hope [our Nature paper](https://www.nature.com/articles/s41586-021-04086-x) can inspire other researchers to consider the potential for AI as a useful tool in pure maths. To replicate the results, anybody can access our [interactive notebooks](https://github.com/deepmind/mathematics_conjectures). Reflecting on the incredible mind of Ramanujan, [George Frederick James Temple](https://mathshistory.st-andrews.ac.uk/Biographies/Temple/) wrote, “The great advances in mathematics have not been made by logic but by creative imagination.” Working with mathematicians, we look forward to seeing how AI can further elevate the beauty of human intuition to new levels of creativity.

**Notes**

This work was done by a team including contributions from Alex Davies, Petar Veličković, Lars Buesing, Sam Blackwell, Daniel Zheng, Nenad Tomašev, Richard Tanburn, Peter Battaglia, Charles Blundell, Xavier Glorot, Matt Overlan, Alyssa Pierce, Natalie Lambert, George Holland, Razia Ahamed, Clemens Meyer, Demis Hassabis and Pushmeet Kohli. We would also like to thank Jan Vonk and Jordan Ellenberg for additional mathematical input.
