---
title: "Co-Scientist: A multi-agent AI partner to accelerate research"
source: https://deepmind.google/blog/co-scientist-a-multi-agent-ai-partner-to-accelerate-research/
site: deepmind
date: 2026-05-19
authors: Co-Scientist team
crawled: 2026-09-13
---

Introducing a collaborative AI partner for researchers to develop new hypotheses in life sciences and beyond.

Every great scientific breakthrough begins with a single, transformative idea. The spark of discovery relies on a researcher's ability to connect disparate facts and formulate the right hypothesis to test. But in an era of information overload and increasingly complex challenges, the search for these needle-in-a-haystack ideas has become a significant bottleneck for progress.

We believe AI can help dramatically accelerate the pace of breakthroughs by serving as a dedicated partner in the generation and refinement of breakthrough scientific hypotheses.

Today, in [*Nature*](https://www.nature.com/articles/s41586-026-10644-y) we published our latest Co-Scientist research, introducing a new multi-agent AI system built with Gemini that iteratively generates, debates, and evolves novel hypotheses for complex scientific problems.

We are making the Co-Scientist system available to individual researchers through [Hypothesis Generation](https://ai.google/gemini-for-science?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=), a new experimental tool jointly developed across Google DeepMind, Google Research, Google Cloud and Google Labs. We’ll begin rolling out in the coming weeks and researchers can register their interest at [labs.google/science](http://labs.google/science).

Since sharing our [early research](https://research.google/blog/accelerating-scientific-breakthroughs-with-an-ai-co-scientist/) last year, we’ve been developing and testing Co-Scientist together with teams who are leveraging it to tackle challenging problems - from [antimicrobial resistance](https://www.cell.com/cell/fulltext/S0092-8674(25)00973-0) and [plant immunity](https://www.biorxiv.org/content/10.64898/2026.05.03.722499v1) to [liver fibrosis](https://advanced.onlinelibrary.wiley.com/doi/abs/10.1002/advs.202508751). We’re excited to share some of the ways it is already being applied across fundamental biology, the natural sciences, and engineering.

![](https://lh3.googleusercontent.com/AUvoISTWskz_JJwNuJo3nWOp9SDzm4F778owkT_wGGfpFFkrxtvwjPa7ST25xWjtiy5cRMT_VfqFH16BxxrtYlWIhIfqI5gqyn-we-BlMHh2Mfhv_A=w1440-h810-n-nu)

## How Co-Scientist works: A multi-agent system built with Gemini

Scientific discovery is rarely a straight line; it is a cycle of ideation and hypothesis generation, critique, and refinement. Scientists often reach their most profound insights only after wrestling with a complex problem for days, months, or even years. The core research question behind Co-Scientist was: *How can an AI system engage in this rigorous structured thinking for scientific discovery?*

The Co-Scientist AI system is made of a collaborative coalition of specialized agents based on the Gemini model, which we can group into three different phases:

**Generate ideas:**

- Generation agent - Proposes initial focus areas and novel hypotheses grounded in scientific literature and data.
- Proximity agent - Maps and clusters generated hypotheses to help ensure a diverse, comprehensive exploration of the research space.

**Debate ideas:**

- Reflection agent - Acts as a "virtual peer reviewer," critically evaluating hypotheses for correctness, quality, and novelty.
- Ranking agent - Orchestrates an “idea tournament”, using pairwise comparisons and simulated scientific debates to prioritize the most promising paths and hypotheses.

**Evolve ideas:**

- Evolution agent - Continuously refines, combines, and builds upon the top-ranked hypotheses in the tournament to help iteratively improve their quality.
- Meta-review agent - Synthesizes insights from the debates and idea tournament to continuously optimize the system and generates the final research proposal for the scientist to review.

Orchestrating the agent coalition is a supervisor agent acting as an adaptive planner. Unlike AI models that think linearly, this freeform planner breaks down high-level research goals into executable steps, coordinating agents to run in parallel and explore multiple avenues simultaneously.

![Generated ideas are iteratively refined, critiqued  and evolved into new hypotheses, forming a virtuous cycle of scientific reasoning and hypothesis generation.](https://lh3.googleusercontent.com/Q8eJiVojnFL1Wfa-gnQi9ZHp-yvx-wu5NnJxVXRrh9QGfXcCbkzP7cXKlHyS4Z7WYwfQf8gRrw0h28pKZCyjU7A9sT5Te6jxy1ZF4shl94Y3tEzK4Q=w1440-h810-n-nu)![Generated ideas are iteratively refined, critiqued  and evolved into new hypotheses, forming a virtuous cycle of scientific reasoning and hypothesis generation.](https://lh3.googleusercontent.com/29HFGmr87GjK8qog8rQZdZdTV-eCYux1E6ao1HDh5z3CkYBN2pDk2mebwniNZVCsKKY-URUB8BSphRtUKoxP2XP6GkzV6B9mhE0JgjoCzyOH8JKZZw=w1440-h810-n-nu)

Generated ideas are iteratively refined, critiqued and evolved into new hypotheses, forming a virtuous cycle of scientific reasoning and hypothesis generation.

## Tournament of ideas: How our system verifies, refines, and ranks hypotheses

Co-Scientist can explore thousands of research directions. To help find the most impactful ones, we developed the ‘tournament of ideas’. The approach draws from principles used in [AlphaGo](https://deepmind.google/research/alphago/?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=co-scientist) and [AlphaStar](https://deepmind.google/blog/alphastar-mastering-the-real-time-strategy-game-starcraft-ii/?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=co-scientist) - but instead of playing a game, our AI agents hold scientific debates to generate, refine and rank ideas.

To push the boundaries of novelty while ensuring the hypotheses are robust and testable, the majority of the system's computation is dedicated to *verifying* these hypotheses. By deeply cross-checking claims against scientific literature and data, the system ensures that claims remain grounded, factually accurate, and logically coherent. The system currently integrates web search and specialized databases like ChEMBL and UniProt to incorporate additional knowledge. It can also leverage advanced specialized models as tools like AlphaFold, which we are testing in select research collaborations.

This combination of these capabilities helps make Co-Scientist one of the first examples of a reliable multi-agent system for structured scientific thinking, enabling it to deliver tangible results in novel hypothesis generation for complex scientific problems .

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

The idea tournament is iteratively ranking hypotheses via an Elo-based tournament while also injecting fresh knowledge to expand its exploration of the hypothesis space.

## Validating Co-Scientist in the lab, starting with life sciences

Over the past year, we have collaborated with global experts to evaluate Co-Scientist on complex problems in the life sciences. We have also been previewing an [enterprise-grade version](https://docs.cloud.google.com/gemini/enterprise/docs/co-scientist-and-alphaevolve?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=co-scientist) with a number of organizations including Daiichi Sankyo, Bayer Crop Science, and the [US National Laboratories as part of the Genesis Mission](https://deepmind.google/blog/google-deepmind-supports-us-department-of-energy-on-genesis/).

![A close-up portrait of Stanford Professor Gary Peltz looking slightly to the right of the frame, speaking in a brightly lit laboratory setting.](https://lh3.googleusercontent.com/feR1XoKhjhNxOAWmOoypIwDiuwTrvJfiuHp5hAV9B9tORNH_HNe79Nl3aCg8FYVyfco5BpShty9Ge50rAB3e1407a8d4lKYk6iOQGMW9_2RwkIWJcFM=w1440-h810-n-nu)

### Uncovering repurposed medicines to fight liver fibrosis

Co-Scientist helped accelerate Gary Peltz’s search for liver fibrosis treatments. The multi-agent system highlighted overlooked drug-repurposing candidates, including one that successfully blocked 91% of a scarring-linked response in lab tests. The results, published in Advanced Science, point toward new gene-regulating approaches to treat chronic liver disease.

“*Co-Scientist feels like a collaborator that’s read everything available about biomedical science, with the reasoning capabilities to find the connections that we’re currently missing.*”

Professor Gary Peltz, Stanford University School of Medicine

![Associate Professor Ritu Raman works with a pipette in her lab at the Massachusetts Institute of Technology.](https://lh3.googleusercontent.com/YeqYxXWGT1gwAgAGgKeoE2xdwC87j5tZBRLK6E5Uy6JkPyORYwMtIRN2mfDwLeCjkxUKjfhWxcucuhEgYW0hnZjdHX5nX68hlpMzLoZHuH3BiXtwxbM=w1440-h810-n-nu)

### Uniting biological toolkits for a new approach to ALS

Co-Scientist helped unite Ritu Raman and Ryan Flynn’s labs around the degenerative disease, ALS. The system helped Ritu quickly digest complex literature, propose testable ideas, and spot where complementary expertise could strengthen the best leads, sparking collaboration with Ryan on potential RNA-based approaches to ALS.

“*Science is a team sport. Co-Scientist can’t do science by itself, and I can’t do it all by myself either. It helps me structure my thoughts, so I know what to ask of other experts and collaborators.*”

Associate Professor Ritu Raman, Massachusetts Institute of Technology

![Jonathan Gootenberg and Omar Abudayyeh sitting side-by-side in their laboratory, speaking to the camera.](https://lh3.googleusercontent.com/JHF_yOfbRzrLsjTJ4tCIGBqU9JYNTpC27M9BtelOonmeweb66YbV65bG5mT5ZqtegsslpBbp-AjjgCgN1bByO2aZeXZGDpluIHkLTdJstEu0CkX2GMI=w1440-h810-n-nu)

### Fast-tracking genetic leads to reverse cellular aging

Biologists Omar Abudayyeh and Jonathan Gootenberg are using Co‑Scientist to speed up research on reversing cellular aging. The system synthesises decades of literature to propose novel genetic leads that in lab tests have been shown to rejuvenate cells. It also slashes the time needed to analyse huge screening datasets, from months to days.

“*Using Co-Scientist feels like having a team of 50 people at your disposal, doing all the work within a day, which isn’t something we can otherwise do with our lab.”*

Omar Abudayyeh, Principal Investigator, The Abudayyeh–Gootenberg Lab

![Professor Filippo Menolascina speaking and gesturing in an office-like setting, with a computer monitor displaying a landscape on the left.](https://lh3.googleusercontent.com/yiE1zOfJz2dFwVBD9X0hD-LCATT4IF1JutmEAv_J1vdf3MqKSi_jKH8iNhQWl_64tT4fxxFpcgy5ySrKzJ7iFuqC9Xfr3Ac0J8PAxZ93cg9b6aNLU50=w1440-h810-n-nu)

### Accelerating discovery of liver disease mechanisms

For Filippo Menolascina, Co-Scientist helped turn biomedical literature overload into high-quality hypotheses for metabolic liver disease. The system highlighted promising disease mechanisms and drug combinations, and helped explain why an existing drug benefits only some patients – an idea later supported by Menolascina’s lab tests.

“*Co‑Scientist feels like a jetpack for scientists, powering up our ability to identify promising mechanisms. I think we’re on the brink of a scientific revolution that will significantly shorten the iteration cycles needed to achieve breakthroughs.*”

Filippo Menolascina, Professor of Engineering Biology, University of Edinburgh

![A close-up portrait of Cambridge Professor Clare Bryant smiling warmly while speaking, set in an office with window blinds behind her.](https://lh3.googleusercontent.com/bL1ooIkzsyirRnU13mjmExP9LTYHccohqn2RrxOhzTNOvxi-5M0H6O_JTHvTKzJGcSX1FoCivapgB97PSBkxI_Dx7Qs2Jc2FglbgDDq308dxU-m5=w1440-h810-n-nu)

### Finding the molecular switches behind new infectious diseases

Clare Bryant is using Co-Scientist to help identify the proteins that cause severe disease when pathogens like flu and COVID-19 leap from animals to humans. Iterating with the AI system, she rapidly narrowed the hunt to specific amino acids her lab will test — potentially cutting years of experimental work down to months.

“*Co-Scientist pulls together the entire published literature and online resources to help me ask better questions. It catches what I'd miss in a data-rich field and helps me prioritise, so my team can focus on answering the right questions in the lab.*"

Clare Bryant, Professor of Innate Immunity, University of Cambridge

![A close-up portrait of Dr. Matt Onsum smiling.](https://lh3.googleusercontent.com/bruRdamTW0SCOcZRs-NfATzhcQt62JqXHBaNglb0OeWdoF8-R-5DKSqHiqPKVsqZGv_lqdnYJba_pQFzJOLiXb_v5-RfCGbb4zsBa8gW0Gqhbef_zA=w1440-h810-n-nu)

### Opening new paths in aging research

At Calico Life Sciences, Matt Onsum and Katherine Labbé are using Co-Scientist to tackle one of medicine’s hardest problems: the biology of aging. The AI system has impressed Calico’s experts with its scientific discernment, including by generating an exciting novel hypothesis about the integrated stress response that was later confirmed in the lab.

“*What I found both exciting and surprising about using Co-Scientist is how much it thinks like a scientist. It really works naturally with how a scientist already thinks and behaves.*”

Dr Matt Onsum, Head of AI/ML, Calico Life Sciences

## Developing agentic tools with the scientific community

Co-Scientist was developed in collaboration with researchers from over 100 institutions to test its capabilities and ensure it is a high-quality, useful tool for the scientific community.

As part of our [responsible AI](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/documents/ai-responsibility-update-published-february-2025.pdf) approach, Co-Scientist underwent extensive internal and external safety evaluations. Given Co-Scientist’s demonstrated proficiency in life and physical sciences, we also conducted independent evaluations for misuse in Chemical, Biological, Radiological and Nuclear (CBRN) domains. From these findings, we developed custom safety classifiers to flag unethical research goals and mitigate the surfacing of unsafe information.

We will continue to iterate and develop the tool alongside feedback and collaboration with the scientific community and are excited to be making Co-Scientist available to individual researchers through [Gemini for Science](https://ai.google/gemini-for-science?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=&utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=co-scientist). We also look forward to expanding access to more Google Cloud enterprise partners soon.

We have been deeply inspired by the scientists who have built up our understanding of the world today. And we hope that AI can help researchers to usher in and accelerate a new era of scientific progress.

**Note: Co-Scientist is intended to be a partner in research, not a replacement for scientific or clinical expertise, and users are responsible for any decisions they make using the outputs as they continue their scientific journey.**

[Register your interest](http://labs.google.com/science/interested?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=)[Read our Nature paper](https://www.nature.com/articles/s41586-026-10644-y)[Learn more about Gemini for Science](https://blog.google/innovation-and-ai/technology/research/gemini-for-science-io-2026)

## Acknowledgements

This research project was led by Juraj Gottweis and Vivek Natarajan, as well as Alan Karthikesalingam, Annalisa Pawlosky, and Yunhan Xu, and with key contributions from: Wei-Hung Weng, Adam Marsh, Alexander Daryin, Alessio Orlandi, Andrew Carroll, Anil Palepu, Antonia Mould, Artiom Myaskovsky, Ash Otter, Avinatan Hassidim, Ben Feinstein, Burak Gokturk, Byron Lee, Dan Popovici, Dina Zverinski, Eeshit Dhaval Vaishnav, Elahe Vedadi, Fan Zhang, Felix Weissenberger, Florian Hasler, Frankie Garcia, Gary Peltz, Grzegorz Glowaty, Ivor Rendulic, Ivan Budiselic, Jacob Blum, James Stevenson, Jan Freyberg, Jeremy Ratcliff, Joel Fenster, José R Penadés, Katherine Chou, Kavita Kulkarni, Keran Rong, Khaled Saab, Luka Rimanic, Marina Boia, Mathias Voges, Matthias Bellaiche, Nenad Tomašev, Ottavia Bertolli, Paige Kunkle, Petar Sirkovic, Ryutaro Tanno, Suzy Pickering, Tao Tu, Tiago R D Costa, Tom Sheffer, Victoria Langston, Vikram Dhillon, Yuan Guan, Ziyue Wang, Amin Vahdat, James Manyika, Demis Hassabis, Yossi Matias and Pushmeet Kohli.

We thank our teammates Ali-Cowen Rivers, Anna Trostanetski, Barnaby James, Bill Byrne, Boon Panichprecha, Charlie Taylor, Diego Ballesteros, Hussein Hassan Harrirou, Ieva Grublyte, Ivan Lee, Jakob Oesignhaus, James Walker, Jorge Barrios, Laurynas Tamulevičius, Luka Važić, Meet Shah, Mihai Ciorobea, Natasha Latysheva, Nicolas Stroppa, Nir Kerem, Saz Basu, Sebastian Nowozin, Taylor Applebaum, Team Rakket and, Thomas Wagner and Yaniv Carmel for their technical support.

We also want to thank Carmela Sidrauski, Clare Bryant, Filippo Menolascina, Jonathan Gootenberg, Katherine Labbé, Matthew Onsum, Omar Abudayyeh, Ritu Raman, Ryan Flynn, Velia Siciliano for their collaboration.

Finally, we thank Ali Eslami, Andy Berndt, Ankur Jain, Anna Koivuniemi, Clemens Mayer, Dale Webster, Greg Corrado, Jason Freidenfelds, Jeff Dean, Joelle Barral, John Jumper, John Platt, Josh Woodward, Karen DeSalvo, Koray Kavukcuoglu, Michael Brenner, Michael Howell, Noam Shazeer, Oriol Vinyals, Parthasarathy Ranganathan, Ronit Levavi Morad, Royal Hansen, Scott Huffman, Srini Narayanan, Susan Thomas, Thomas Kurian, Zoubin Ghahramani and Sundar Pichai for their support of this work.
