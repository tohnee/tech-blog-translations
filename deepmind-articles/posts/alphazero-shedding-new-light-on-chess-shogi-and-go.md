---
title: "AlphaZero: Shedding new light on chess, shogi, and Go"
source: https://deepmind.google/blog/alphazero-shedding-new-light-on-chess-shogi-and-go/
site: deepmind
date: 2018-12-06
authors: David Silver, Thomas Hubert, Julian Schrittwieser, Demis Hassabis
crawled: 2026-09-13
---

In late 2017 we [introduced AlphaZero](https://arxiv.org/abs/1712.01815), a single system that taught itself from scratch how to master the games of chess, [shogi](https://en.wikipedia.org/wiki/Shogi)(Japanese chess), and [Go](https://en.wikipedia.org/wiki/Go_(game)), beating a world-champion program in each case. We were excited by the preliminary results and thrilled to see the response from members of the chess community, who saw in AlphaZero’s games a ground-breaking, highly dynamic and “[unconventional](https://www.ft.com/content/ea707a24-f6b7-11e7-8715-e94187b3017e)” style of play that differed from any chess playing engine that came before it.

Today, we are delighted to introduce the full evaluation of AlphaZero, [published in the journal Science](https://www.science.org/doi/full/10.1126/science.aar6404) ([Open Access version here](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/alphazero-shedding-new-light-on-chess-shogi-and-go/alphazero_preprint.pdf)), that confirms and updates those preliminary results. It describes how AlphaZero quickly learns each game to become the strongest player in history for each, despite starting its training from random play, with no in-built domain knowledge but the basic rules of the game.

> I can’t disguise my satisfaction that it plays with a very dynamic style, much like my own!

Garry Kasparov

Former World Chess Champion

This ability to learn each game afresh, unconstrained by the norms of human play, results in a distinctive, unorthodox, yet creative and dynamic playing style. Chess Grandmaster Matthew Sadler and Women’s International Master Natasha Regan, who have analysed thousands of AlphaZero’s chess games for [their forthcoming book Game Changer](https://www.newinchess.com/game-changer) (New in Chess, January 2019), say its style is unlike any traditional chess engine.” It’s like discovering the secret notebooks of some great player from the past,” says Matthew.

Traditional chess engines – including the world computer chess champion [Stockfish](https://en.wikipedia.org/wiki/Stockfish_(chess)) and [IBM’s ground-breaking Deep Blue](https://www.ibm.com/ibm/history/ibm100/us/en/icons/deepblue/) – rely on thousands of rules and heuristics handcrafted by strong human players that try to account for every eventuality in a game. Shogi programs are also game specific, using similar search engines and algorithms to chess programs.

AlphaZero takes a totally different approach, replacing these hand-crafted rules with a deep [neural network](https://en.wikipedia.org/wiki/Artificial_neural_network) and general purpose algorithms that know nothing about the game beyond the basic rules.

![An animated line graph showing the reinforcement learning progress of AlphaZero. Beside an illustration of a Go board, the graph plots Elo rating against training steps up to 700k, demonstrating how AlphaZero rapidly increases its playing strength during self-play.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/622693c3f70ee14b39e7ee17_AlphaZero.gif)

In chess, AlphaZero first outperformed Stockfish after just 4 hours; in shogi, AlphaZero first outperformed Elmo after 2 hours; and in Go, AlphaZero first outperformed the version of AlphaGo that beat the legendary player Lee Sedol in 2016 after 30 hours. Note: each training step represents 4,096 board positions.

To learn each game, an untrained neural network plays millions of games against itself via a process of trial and error called [reinforcement learning](https://en.wikipedia.org/wiki/Reinforcement_learning). At first, it plays completely randomly, but over time the system learns from wins, losses, and draws to adjust the parameters of the neural network, making it more likely to choose advantageous moves in the future. The amount of training the network needs depends on the style and complexity of the game, taking approximately 9 hours for chess, 12 hours for shogi, and 13 days for Go.

> Some of its moves, such as moving the King to the centre of the board, go against shogi theory and - from a human perspective - seem to put AlphaZero in a perilous position. But incredibly it remains in control of the board. Its unique playing style shows us that there are new possibilities for the game.

Yoshiharu Habu

9-Dan professional, only player in history to hold all seven major shogi titles

The trained network is used to guide a search algorithm – known as Monte-Carlo Tree Search (MCTS) – to select the most promising moves in games. For each move, AlphaZero searches only a small fraction of the positions considered by traditional chess engines. In Chess, for example, it searches only 60 thousand positions per second in chess, compared to roughly 60 million for Stockfish.

![An infographic comparing the amount of search per decision. Where a human grandmaster searches hundreds of moves, AlphaZero searches tens of thousands of moves, and State-of-the-art chess engines search tens of millions of moves.](https://lh3.googleusercontent.com/e0wFggmSiOjbp5jtZ1xq8sNhAvOf7ids49D-qzO1wMl1w7cxVoZ8F5L02VzQ1SWvmHu3pqazmc2UY5N3cAU52A3dH_8XXkQYXn9HNkLgn1A0QVVUm60=w1440)

The fully trained systems were tested against the strongest hand-crafted engines for chess ([Stockfish](https://en.wikipedia.org/wiki/Stockfish_(chess))) and shogi ([Elmo](https://en.wikipedia.org/wiki/Elmo_(shogi_engine))), along with our previous self-taught system [AlphaGo Zero](https://deepmind.com/blog/article/alphago-zero-starting-scratch), the strongest Go player known.

- Each program ran on the hardware for which they were designed. Stockfish and Elmo used 44 CPU cores (as in the [TCEC world championship](https://en.wikipedia.org/wiki/Top_Chess_Engine_Championship)), whereas AlphaZero and AlphaGo Zero used a single machine with 4 first-generation [TPUs](https://cloud.google.com/tpu/docs/tpus) and 44 [CPU](https://en.wikipedia.org/wiki/Central_processing_unit) cores. A first generation TPU is roughly similar in inference speed to commodity hardware such as an [NVIDIA Titan V GPU](https://www.nvidia.com/en-gb/titan/titan-v/), although the architectures are not directly comparable.
- All matches were played using time controls of three hours per game, plus an additional 15 seconds for each move.

In each evaluation, AlphaZero convincingly beat its opponent:

- In chess, AlphaZero defeated the [2016 TCEC (Season 9)](https://www.chessbomb.com/arena/-/2016-tcec9) world champion [Stockfish](https://stockfishchess.org/), winning 155 games and losing just six games out of 1,000. To verify the robustness of AlphaZero, we also played a series of matches that started from common human openings. In each opening, AlphaZero defeated Stockfish. We also played a match that started from the set of opening positions used in the 2016 TCEC world championship, along with a series of additional matches against the most recent development version of Stockfish, and a variant of Stockfish that uses a strong opening book. In all matches, AlphaZero won.
- In shogi, AlphaZero defeated the [2017 CSA world champion version of Elmo](http://www2.computer-shogi.org/wcsc27/index_e.html), winning 91.2% of games.
- In Go, AlphaZero defeated [AlphaGo Zero](https://deepmind.com/blog/article/alphago-zero-learning-scratch), winning 61% of games.

![An infographic comparing AlphaZero's performance in Chess, Shogi, and Go against Stockfish, Elmo, and AlphaGo Zero respectively, showing win/draw/loss rates broken down by playing as white or black.](https://lh3.googleusercontent.com/zyxpKGbbGJK-pId62KSa3pjYEYfdAHeOCCh6asmtiJD4jVdgxOZlNMWQ3HKKstdex7YVdAIgejUQlIB4VsbRJu2dU1hBiK77wcX9pSJMO3jDlJ6pGm4=w1440)

However, it was the style in which AlphaZero plays these games that players may find most fascinating. In Chess, for example, AlphaZero independently discovered and played common human motifs during its self-play training such as openings, king safety and pawn structure. But, being self-taught and therefore unconstrained by conventional wisdom about the game, it also developed its own intuitions and strategies adding a new and expansive set of exciting and novel ideas that augment centuries of thinking about chess strategy.

> Chess has been used as a Rosetta Stone of both human and machine cognition for over a century. AlphaZero renews the remarkable connection between an ancient board game and cutting-edge science by doing something extraordinary.

Garry Kasparov

Former World Chess champion

The first thing that players will notice is AlphaZero's style, says Matthew Sadler – “the way its pieces swarm around the opponent’s king with purpose and power”. Underpinning that, he says, is AlphaZero’s highly dynamic game play that maximises the activity and mobility of its own pieces while minimising the activity and mobility of its opponent’s pieces. Counterintuitively, AlphaZero also seems to place less value on “material”, an idea that underpins the modern game where each piece has a value and if one player has a greater value of pieces on the board than the other, then they have a material advantage. Instead, AlphaZero is willing to sacrifice material early in a game for gains that will only be recouped in the long-term.

“Impressively, it manages to impose its style of play across a very wide range of positions and openings,” says Matthew, who also observes that it plays in a very deliberate style from its first move with a “very human sense of consistent purpose”.

“Traditional engines are exceptionally strong and make few obvious mistakes, but can drift when faced with positions with no concrete and calculable solution,” he says. “It's precisely in such positions where ‘feeling’, ‘insight’ or ‘intuition’ is required that AlphaZero comes into its own."

> The implications go far beyond my beloved chessboard... Not only do these self-taught expert machines perform incredibly well, but we can actually learn from the new knowledge they produce.

Garry Kasparov

Former World Chess champion

This unique ability, not seen in other traditional chess engines, has already been harnessed to give chess fans [fresh insight and commentary](https://chess24.com/en/read/news/alphazero-on-carlsen-caruana-games-1-8) on the recent [World Chess Championship](https://worldchess.com/) match between [Magnus Carlsen](https://en.wikipedia.org/wiki/Magnus_Carlsen) and [Fabiano Caruana](https://en.wikipedia.org/wiki/Fabiano_Caruana) and will be explored further in [Game Changer](https://www.newinchess.com/game-changer). “It was fascinating to see how AlphaZero's analysis differed from that of top chess engines and even top grandmaster play,” says Natasha Regan. "AlphaZero could be a powerful teaching tool for the whole community."

AlphaZero’s teachings echo what we saw when [AlphaGo](https://deepmind.com/research/case-studies/alphago-the-story-so-far) played the legendary champion [Lee Sedol](https://en.wikipedia.org/wiki/Lee_Sedol) in 2016. During [the games](https://deepmind.com/alphago-korea), AlphaGo played a number of [highly inventive winning moves,](https://deepmind.com/blog/article/innovations-alphago) including move 37 in game two, which overturned hundreds of years of thinking. These moves - and many others - have since been studied by players at all levels including Lee Sedol himself, who said of Move 37: “I thought AlphaGo was based on probability calculation and it was merely a machine. But when I saw this move I changed my mind. Surely AlphaGo is creative.”

As with Go, we are excited about AlphaZero’s creative response to chess, which has been a grand challenge for artificial intelligence since the dawn of the computing age with early pioneers including Babbage, Turing, Shannon, and von Neumann all trying their hand at designing chess programs. But AlphaZero is about more than chess, shogi or Go. To create intelligent systems capable of solving a wide range of real-world problems we need them to be flexible and generalise to new situations. While there has been some progress towards this goal, it remains a major challenge in AI research with systems capable of mastering specific skills to a very high standard, but often failing when presented with even slightly modified tasks.

AlphaZero’s ability to master three different complex games – and potentially any perfect information game – is an important step towards overcoming this problem. It demonstrates that a single algorithm can learn how to discover new knowledge in a range of settings. And, while it is still early days, AlphaZero’s creative insights coupled with the encouraging results we see in other projects such as [AlphaFold](https://deepmind.google/science/alphafold/), give us confidence in [our mission](https://deepmind.com/about/) to create general purpose learning systems that will one day help us find novel solutions to some of the most important and complex scientific problems.

**Notes**

1. Read [the paper in Science](http://science.sciencemag.org/cgi/content/full/362/6419/1140?ijkey=XGd77kI6W4rSc&keytype=ref&siteid=sci)
2. Download an [Open Access version of the paper](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/alphazero-shedding-new-light-on-chess-shogi-and-go/alphazero_preprint.pdf) [PDF]
3. Read the accompanying [Science editorial](http://science.sciencemag.org/content/362/6419/1087) by Garry Kasparov
4. Read the [accompanying Perspective article](http://science.sciencemag.org/content/362/6419/1118) in Science by Deep Blue co-creator Murray Campbell
5. Download [the top 20 AlphaZero-Stockfish games chosen by Grandmaster Matthew Sadler](https://storage.googleapis.com/deepmind-media/DeepMind.com/Open-Source/alphazero-resources/alphazero_stockfish_top20.zip) [.zip]
6. Download [the top 10 AlphaZero-Elmo games chosen by shogi Master Yoshiharu Habu](https://storage.googleapis.com/deepmind-media/DeepMind.com/Open-Source/alphazero-resources/alphazero_elmo_top10%20(1).zip) [.zip]
7. Download [210 AlphaZero-Stockfish chess games and 100 AlphaZero-Elmo shogi games](https://deepmind.com/research/open-source/alphazero-resources)
8. Download the [accompanying artwork](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/alphazero-shedding-new-light-on-chess-shogi-and-go/alphazero_images.zip)
9. Find out more about the AlphaZero book [Game Changer](https://www.newinchess.com/game-changer) (New in Chess, January 2019)

This work was done by David Silver, Thomas Hubert, Julian Schrittwieser, Ioannis Antonoglou, Matthew Lai, Arthur Guez, Marc Lanctot, Laurent Sifre, Dharshan Kumaran, Thore Graepel, Timothy Lillicrap, Karen Simonyan, and Demis Hassabis.
