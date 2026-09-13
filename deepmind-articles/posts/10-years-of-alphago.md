---
title: "From games to biology and beyond: 10 years of AlphaGo’s impact"
source: https://deepmind.google/blog/10-years-of-alphago/
site: deepmind
date: 2026-03-10
authors: Demis Hassabis, Demis Hassabis
crawled: 2026-09-13
---

Ten years ago, our AI system AlphaGo became the first program to defeat a world champion at the complex game of Go – reaching a milestone in the field a decade before many experts thought possible.

The achievement heralded the beginning of what is now recognized as the modern era in artificial intelligence (AI). With a single creative play, the famous ‘Move 37,’ [AlphaGo](https://deepmind.google/research/alphago/) demonstrated the potential of AI and signaled that we now had the techniques to begin tackling real-world scientific problems.

Today, this breakthrough continues to inform our work building systems on the path to artificial general intelligence (AGI). We believe AGI will be the most profound technology ever invented and potentially the ultimate tool to advance science, medicine, and productivity.

## A creative spark

In 2016, over 200 million people watched AlphaGo face world-champion Go player Lee Sae Dol in Seoul. The match was defined by ‘Move 37’ in Game 2, a play so unconventional that professional commentators initially thought it was a mistake. But it proved to be decisive. One hundred or so moves later, the stone was in exactly the right position for AlphaGo to win the game. It was a display of incredible foresight and the AI system’s ability to go beyond mimicking human experts and find entirely new strategies.

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

[Watch the AlphaGo documentary on YouTube](https://www.youtube.com/watch?v=WXuK6gekU1Y)

Go has long been a proving ground for AI research because of the game’s sheer complexity. There are 10170 possible positions on the board—far more than the number of atoms in the observable universe.

To make the game tractable, AlphaGo used deep neural networks combined with advanced search and reinforcement learning – an AI approach DeepMind [pioneered](https://www.nature.com/articles/nature16961).

AlphaGo learned a model of plausible Go moves by first learning from games played by human experts, and then playing hundreds of thousands of games against itself, improving as the strongest winning strategies were reinforced. The system then considered only the most potentially fruitful paths and from that smaller subset of moves, found the one most likely to lead it to win.

After AlphaGo, we built [AlphaGo Zero](https://deepmind.google/blog/alphago-zero-starting-from-scratch/), which learned the game from completely random play and became arguably the strongest player in history. Then we generalized the system further with [AlphaZero](https://deepmind.google/blog/alphazero-shedding-new-light-on-chess-shogi-and-go/), which taught itself from scratch to master any 2-player perfect information game, including Go, chess, and shogi. Beginning with no prior knowledge other than the rules of the game, AlphaZero was able to learn to master chess in a matter of hours, and beat not only the top human players but the best specialised chess programs at the time, like Stockfish. And even though chess had been so heavily analysed with the aid of these programs, just as with Go, AlphaZero was still able to come up with interesting [new strategies](https://www.newinchess.com/game-changer).

It was further proof of what I knew the moment we won the match in Seoul - the technology was ready to be applied to our real goal of accelerating scientific breakthroughs.

> I believe the greatest lesson AlphaGo offered was a definitive preview of the AI era—proving it wasn’t some distant, vague future, but a reality arriving on our doorstep. It served as a "roadmap from the future," sending a clear signal to humanity about how the world was about to change.

Go Master Lee Sae Dol

Adjunct Professor at UNIST

## Catalyzing breakthroughs in science

By proving it could navigate the massive search space of a Go board, AlphaGo demonstrated the potential for AI to help us better understand the vast complexities of the physical world. We started by attempting to solve the protein folding problem, a 50-year grand challenge of predicting the 3D structure of proteins - information that is crucial for understanding diseases and developing new drugs.

In 2020, we finally cracked this longstanding scientific problem with our [AlphaFold 2](https://deepmind.google/blog/alphafold-five-years-of-impact/) system. From there, we folded the structures for all 200 million proteins known to science and made them freely available to scientists in an open-source database. Today, over 3 million researchers around the world use the [AlphaFold database](https://alphafold.ebi.ac.uk/) to accelerate their important work on everything from malaria vaccines to plastic-eating enzymes. And in 2024, it was the honor of a lifetime for John Jumper and I to be awarded the Nobel Prize in Chemistry for leading this project, on behalf of the entire AlphaFold team.

Since AlphaGo’s win, we’ve applied its groundbreaking approach to many other areas of science and mathematics, including:

**Mathematical reasoning:** The most direct descendant of AlphaGo’s architecture, [AlphaProof](https://deepmind.google/blog/ai-solves-imo-problems-at-silver-medal-level/) learned to prove formal mathematical statements using a combination of language models and AlphaZero’s reinforcement learning and search algorithms. Alongside AlphaGeometry 2, it became the first system to achieve a medal-standard (silver) at the International Mathematical Olympiad (IMO), proving AlphaGo's methods could unlock advanced mathematical reasoning and laying the foundation for our most capable general models.

Gemini, our largest and most capable model, recently went even further. An advanced version of its Deep Think mode [achieved](https://deepmind.google/blog/advanced-version-of-gemini-with-deep-think-officially-achieves-gold-medal-standard-at-the-international-mathematical-olympiad/) gold-medal level performance at the 2025 IMO using an approach inspired by AlphaGo. Since then, Deep Think has been [applied](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-deep-think/) to even more complex, open-ended challenges across science and engineering.

**Algorithm discovery:** Just as AlphaGo searched for the best move in a game, our coding agent [AlphaEvolve](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/) explores the space of computer code to discover more efficient algorithms. It had its own Move 37 moment when it found a novel way to multiply matrices, a fundamental mathematical operation powering nearly all modern neural networks. AlphaEvolve is now being tested on problems ranging from data center optimization to quantum computing.

**Scientific collaboration:** We are integrating the search and reasoning principles pioneered with AlphaGo into an [AI co-scientist](https://research.google/blog/accelerating-scientific-breakthroughs-with-an-ai-co-scientist/). By having agents 'debate' scientific ideas and hypotheses, this system acts as a collaborator capable of performing the rigorous thinking necessary to identify patterns in data and solve sophisticated problems. In validation studies at [Imperial College London](https://www.imperial.ac.uk/news/261293/googles-ai-co-scientist-could-enhance-research/), it analyzed decades of literature and independently arrived at the same hypothesis about antimicrobial resistance that researchers had spent years developing and validating experimentally.

We’ve also used AI to [better understand the genome](https://deepmind.google/blog/alphagenome-ai-for-better-understanding-the-genome/), [advance fusion energy research](https://deepmind.google/blog/bringing-ai-to-the-next-generation-of-fusion-energy/), [improve weather prediction](https://deepmind.google/science/weathernext/) and more.

As impressive as our scientific models are, they are highly specialized. To achieve fundamental breakthroughs like creating limitless clean energy or solving diseases that we don’t understand today, we need general AI systems that can find underlying structure and connections between different subject areas, and help us to come up with new hypotheses like the best scientists do.

## Future of intelligence

For an AI to be truly general, it needs to understand the physical world. We built Gemini to be multimodal from the beginning so it could understand not just language, but also audio, video, images and code to build a model of the world.

To think and reason across these modalities, the latest Gemini models use some of the techniques we pioneered with AlphaGo and AlphaZero.

The next generation of AI systems will also need to be able to call upon specialized tools. For example, if a model needed to know the structure of a protein it could use AlphaFold for that.

We think the combination of Gemini’s world models, AlphaGo’s search and planning techniques, and specialized AI tool use will prove to be critical for AGI.

True creativity is a key capability that such an AGI system would need to exhibit. Move 37 was a glimpse of AI’s potential to think outside the box, but true original invention will require something more. It would need to not only come up with a novel Go strategy, as AlphaGo impressively did, but actually invent a game as deep and elegant, and as worthy of study as Go.

Ten years after AlphaGo’s legendary victory, our ultimate goal is on the horizon. The creative spark first seen in Move 37 catalyzed breakthroughs that are now converging to pave the path towards AGI - and usher in a new golden age of scientific discovery.

Exactly one decade later, we look back at the match that sparked the modern AI revolution.

[Learn about AlphaGo](https://deepmind.google/research/alphago/)[Watch the AlphaGo documentary on YouTube](https://www.youtube.com/watch?v=WXuK6gekU1Y)
