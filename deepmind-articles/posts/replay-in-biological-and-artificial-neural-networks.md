---
title: "Replay in biological and artificial neural networks"
source: https://deepmind.google/blog/replay-in-biological-and-artificial-neural-networks/
site: deepmind
date: 2019-09-06
authors: Zeb Kurth-Nelson, Will Dabney
crawled: 2026-09-13
---

One of a series of posts explaining the theories underpinning our research.

Our waking and sleeping lives are punctuated by fragments of recalled memories: a sudden connection in the shower between seemingly disparate thoughts, or an ill-fated choice decades ago that haunts us as we struggle to fall asleep. By measuring memory retrieval directly in the brain, neuroscientists have noticed something remarkable: spontaneous recollections, measured directly in the brain, often occur as very fast [sequences](https://www.annualreviews.org/doi/10.1146/annurev-neuro-072116-031538) of multiple memories. These so-called 'replay' sequences play out in a fraction of a second–so fast that we're not necessarily aware of the sequence.

In parallel, AI researchers discovered that incorporating a similar kind of [experience replay](https://www.aaai.org/Papers/AAAI/1991/AAAI91-122.pdf) improved the efficiency of learning in artificial neural networks. Over the last three decades, the AI and neuroscientific studies of replay have grown up together. Machine learning offers hypotheses sophisticated enough to push forward our expanding knowledge of the brain; and insights from neuroscience guide and inspire AI development. Replay is a key point of contact between the two fields because like the brain, AI uses experience to learn and improve. And each piece of experience offers much more potential for learning than can be absorbed in real-time–so continued offline learning is crucial for both brains and artificial neural nets.

## Replay in the brain

Neural replay sequences were originally discovered by studying the hippocampus in rats. As we know from the Nobel prize winning work of [John O’Keefe](https://www.nobelprize.org/prizes/medicine/2014/okeefe/lecture/) and others, many hippocampal cells fire only when the animal is physically located in a specific [place](https://www.annualreviews.org/doi/abs/10.1146/annurev.neuro.31.061307.090723). In early experiments, [rats](https://science.sciencemag.org/content/271/5257/1870.long) ran the length of a single corridor or circular track, so researchers could easily determine which neuron coded for each position within the corridor.

![A graph illustrating neural firing sequences, showing seven horizontal timelines with vertical tick marks representing individual neuron spikes and colored curves representing the density of these spikes, demonstrating a sequential pattern of activation over time.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/622734b2d51bab00a1b37204_Replay2002.svg)

When rats are awake and active, each hippocampal place cell codes for a particular location in space. Each row is a different cell, and they are sorted by the location they represent. Each vertical tick mark is an action potential. The solid lines represent smoothed firing rates.

Afterwards, the scientists recorded from the same neurons while the rats rested. During rest, the cells sometimes spontaneously fired in rapid sequences demarking the same path the animal ran earlier, but at a greatly accelerated speed. These sequences are called replay. An entire replay sequence only lasts a fraction of a second, but plays through several seconds worth of real experience.

![Three grid graphs side by side showing colored vertical tick marks that represent neural firing sequences over time.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/622734d136bc1b4cd2e81183_Replay2003.svg)

During rest, place cells spontaneously fire in fast sequences that sweep through paths in the environment.

We now know replay is essential for learning. In a number of more recent experiments, researchers recorded from hippocampus to detect a signature of replay events in real time. By disrupting brain activity during replay events (either during [sleep](https://onlinelibrary.wiley.com/doi/abs/10.1002/hipo.20707) or [wakeful](https://science.sciencemag.org/content/336/6087/1454.editor-summary) resting), scientists significantly impaired rodents’ ability to learn a new task. The same disruption applied 200 milliseconds out of sync with replay events had no effect on learning.

While these experiments have been revealing, a significant limitation of rodent experiments is the difficulty of studying more sophisticated aspects of cognition, such as abstract concepts. In the last few years, replay-like sequences have also been [detected](https://www.sciencedirect.com/science/article/pii/S0896627316302070) in human brains, supporting the idea that replay is pervasive, and expanding the kinds of questions we can ask about it.

## Replay in artificial intelligence

![A conceptual diagram showing a circular loop of information flow, with a biological neural network on the left and an artificial neural network represented as layered squares on the right, connected by a daytime path representing waking life at the top and a nighttime path representing sleep and replay at the bottom.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/622734fc2b032b47dc9e08db_Replay2004.svg)

Artificial neural networks collect experience by interacting with the environment, save that experience to a replay buffer, and later play it back to continue learning from it.

Incorporating replay in silico has been beneficial to advancing [artificial intelligence](https://www.sciencedirect.com/science/article/pii/S0896627317305093). Deep learning often depends upon a ready supply of large datasets. In [reinforcement learning](http://karpathy.github.io/2016/05/31/rl/), these data come through direct interaction with the environment, which takes time. The technique of [experience](https://www.aaai.org/Papers/AAAI/1991/AAAI91-122.pdf) [replay](http://www.incompleteideas.net/lin-92.pdf) allows the agent to repeatedly rehearse previous interactions, making the most of each interaction. This method proved crucial for combining deep neural networks with reinforcement learning in the [DQN](https://www.nature.com/articles/nature14236) agent that first mastered multiple Atari games.

Since the introduction of DQN, the efficiency of replay has been improved by [preferentially](https://link.springer.com/article/10.1007/BF00993104) [replaying](https://papers.nips.cc/paper/1409-generalized-prioritized-sweeping.pdf) [the](https://arxiv.org/abs/1511.05952) most salient experiences from memory, rather than simply choosing experiences at random for replay. And recently, a variant of preferential replay has been [applied](https://www.nature.com/articles/s41593-018-0232-z) as a model in neuroscience to successfully explain empirical data from brain recordings.

Further improvements in agent performance have come from [combining experiences](https://arxiv.org/abs/1802.01561) across multiple agents, learning about a variety of [different behaviours](https://arxiv.org/abs/1707.01495) from the same set of experiences, and replaying not only the trajectory of events in the world, but also the agent's corresponding [internal memory states](https://openreview.net/pdf?id=r1lyTjAqYX). Each of these methods makes interesting predictions for neuroscience that remain largely untested.

## Movie versus imagination

As mentioned above, research into experience replay has unfolded along parallel tracks in artificial intelligence and neuroscience, with each field providing ideas and inspiration for the other. In particular, there is a central distinction, which has been studied in both fields, between two versions of replay.

Suppose you come home and, to your surprise and dismay, discover water pooling on your beautiful wooden floors. Stepping into the dining room, you find a broken vase. Then you hear a whimper, and you glance out the patio door to see your dog looking very guilty.

![An illustration of real-time experience showing a horizontal timeline from left to right with three events: "Spilt water", "Broken vase", and "Puppy". An eye icon is on the left looking along the timeline.](https://lh3.googleusercontent.com/TTQFeD98W-N87SwUdBgI4NGbgRrH-ZRhaoMlXEcms9g2yA5GPEmViNcz6DXFhJ7EXe1MH2PfzaaWBPkXMvi5BuVvLzZsD0F8HbOcF1OQ2UcZZmfD0zk=w1440)

A sequence of events, as they were experienced.

In the first version of replay, which we could call the "movie" version, when you sit down on the couch and take a rest, replay faithfully rehearses the actual experiences of the past. This theory says that your brain will replay the sequence: "water, vase, dog". In AI terms, the past experience was stored in a replay buffer, and trajectories for offline learning were drawn directly from the buffer.

![An illustration representing imagination replay during sleep, showing a timeline from left to right with the events "Spilt water", "Broken vase", and "Puppy", with a curved green arrow going from right to left under a crescent moon icon to show the order of events being flipped.](https://lh3.googleusercontent.com/0Ooy7Y2YweY0UX9Vm1srSWdethWEnOD92q_S_7UObt8sEWQwrDjpBxctexOSTPHKHCPpQlm6TTwQBWJvbAitDNi6H3t4ee9VRnPcLGgEGf9qQqiQnQ=w1440)

"Movie" replay: events are played back in the same order as they occurred.

In the second version, which we might call "imagination," replay doesn’t literally rehearse events in the order they were experienced. Instead, it infers or imagines the real relationships between events, and synthesises sequences that make sense given an understanding of how the world works. In AI terms, these replay sequences are [generated](https://arxiv.org/pdf/1809.10635.pdf) using a [learned](https://arxiv.org/pdf/1705.08690.pdf) [model](https://arxiv.org/pdf/1705.08690.pdf) of the environment.

![An illustration representing imagination replay during sleep, showing a timeline from left to right with the events "Puppy", "Broken vase", and "Spilt water" below a sleeping face icon, with a curved green arrow going from left to right over a crescent moon icon to show the reconstructed order of events.](https://lh3.googleusercontent.com/UzkELoglqaO6YwXUd5L-3X27tr03zyV4J-2UmIR4rlEQUdGmVdwZ0joChB2sHutH5--PoW7HpbFAAITuQ_Qboj6icw1slxqKfrC31L7_zQ6ZUugxxg=w1440)

"Imagination" replay: events are played back in a synthesised order which respects knowledge of the structure of the world.

The imagination theory makes a different prediction about how replay will look: when you rest on the couch, your brain should replay the sequence "dog, vase, water". You know from past experience that dogs are more likely to cause broken vases than broken vases are to cause dogs–and this knowledge can be used to reorganise experience into a more meaningful order.

In deep RL, the large majority of agents have used movie-like replay, because it is easy to implement (the system can simply store events in memory, and play them back as they happened). However, RL researchers have continued to study the possibilities around imagination replay.

Meanwhile in neuroscience, classic theories of replay postulated that movie replay would be useful to strengthen the connections between neurons that represent different events or locations in the order they were experienced. However, there have been [hints](https://www.annualreviews.org/doi/pdf/10.1146/annurev-neuro-072116-031538) from experimental neuroscience that replay might be able to imagine new sequences. The most compelling [observation](https://www.sciencedirect.com/science/article/pii/S0896627310000607) is that even when rats only experienced two arms of a maze separately, subsequent replay sequences sometimes followed trajectories from one arm into the other.

But studies like this leave open the question of whether replay simply stitches together chunks of experienced sequences, or if it can synthesise new trajectories from whole cloth. Also, rodent experiments have been primarily limited to spatial sequences, but it would be fascinating to know whether humans' ability to imagine sequences is enriched by our vast reserve of abstract conceptual knowledge.

## A new replay experiment in humans

We asked these questions in a set of recent [experiments](https://www.cell.com/cell/fulltext/S0092-8674(19)30640-3) performed jointly between UCL, Oxford, and DeepMind.

In these experiments, we first taught people a rule that defined how a set of objects could interact. The exact rule we used can be found in the paper. But to continue in the language of the "water, vase, dog" example, we can think of the rule as the knowledge that dogs can cause broken vases, and broken vases can cause water on the floor. We then presented these objects to people in a scrambled order (like "water, vase, dog"). That way, we could ask whether their brains replayed the items in the scrambled order that they experienced, or in the unscrambled order that meaningfully connected the items. They were shown the scrambled sequence and then given five minutes to rest, while sitting in an [MEG](https://en.wikipedia.org/wiki/Magnetoencephalography) brain scanner.

As in previous experiments, fast replay sequences of the objects were evident in the brain recordings. (In yet another example of the [virtuous circle](https://deepmind.com/blog/ai-and-neuroscience-virtuous-circle/) between neuroscience and AI, we used machine learning to read out these signatures from cortical activity.) These spontaneous sequences played out rapidly over about a sixth of a second, and contained up to four objects in a row. However, the sequences did not play out in the experienced order (i.e., the scrambled order: spilled water –> vase –> dog). Instead, they played out the unscrambled, meaningful order: dog –> vase –> spilled water. This answers–in the affirmative–the questions of whether replay can imagine new sequences from whole cloth, and whether these sequences are shaped by abstract knowledge.

However, this finding still leaves open the important question of how the brain builds these unscrambled sequences. To try to answer this, we played a second sequence for participants. In this sequence, you walk into your factory and see spilled oil on the floor. You then see a knocked over oil barrel. Finally, you turn to see a guilty robot. To unscramble this sequence, you can use the same kind of knowledge as in the "water, vase, dog" sequence: knowledge that a mobile agent can knock over containers, and those knocked-over containers can spill liquid. Using that knowledge, the second sequence can also be unscrambled: robot –> barrel –> spilled oil.

By showing people multiple sequences with the same structure, we could examine two new types of neural representation. First, the part of the representation that is common between spilled water and spilled oil. This is an abstract code for "a spilled liquid", invariant over whether we're in the home sequence or the factory sequence. And second, the part of the representation that is common between water, vase and dog. This is an abstract code for "the home sequence," invariant over which object we're considering.

We found both of these types of abstract codes in the brain data. And to our surprise, during rest they played out in fast sequences that were precisely coordinated with the spontaneous replay sequences mentioned above. Each object in a replay sequence was preceded slightly by both abstract codes. For example, during a dog, vase, water replay sequence, the representation of "water" was preceded by the codes for "home sequence" and "spilled liquid".

![A 2D grid diagram showing abstract analogies across different contexts. The x-axis represents the contexts "Home sequence" (with images of a puppy, broken vase, and spilled water) and "Factory sequence" (with images of a robot, barrel, and spilled oil). The y-axis represents the abstract roles "Agent", "Container", and "Liquid". Purple arrows connect "Container" to "Liquid" for both contexts, with the text "Barrel is to oil as vase is to water".](https://lh3.googleusercontent.com/Le2hTzPlScUuE6oQRIb9RV-cWSRSZGiLO1NHYm4lBSny9QdOnJQTs9MQkR65ybYEyLRam5__pDPbls9nWsQj1yhPrB3WHvlU35RDcp1c1UNfho0WZQ=w1440)

Structurally similar sequences in different contexts slotted into a common analogical framework

These abstract codes, which incorporate the conceptual knowledge that lets us unscramble the sequences, may help the brain to retrieve the correct item for the next slot in the replay sequence. This paints an interesting picture of a system where the brain slots new information into an [abstract](https://psyarxiv.com/6fm9a/) [framework](https://www.sciencedirect.com/science/article/pii/S0896627318308560) [built](http://www.talfanevans.co.uk/Neurips_2019/coordinated_hippocampal_entorhinal_replay_as_structural_inference.pdf) from past experiences, keeping it organized using precise relative timings within very fast replay sequences. Each position within a sequence could be thought of as a role in an [analogy](https://www.goodreads.com/book/show/7711871-surfaces-and-essences) (as in the above figure). Finally, we speculate that during rest, the brain may explore novel implications of previously-learned knowledge by placing an item into an analogy in which it's never been experienced, and examining the consequences.

## The virtuous circle, continued

Coming back to the virtuous circle, analogy and abstraction are relatively underused in current neural network architectures. The new results described above both indicate that the imagination style of replay may be a fruitful avenue to continue pursuing in AI research, and suggest directions for neuroscience research to learn more about the brain mechanisms underlying analogy and abstraction. It's exciting to think about how data from the brain will continue helping with the advance toward better and more human-like artificial intelligence.

Yunzhe Liu

The [new work reported in Cell](https://www.cell.com/cell/fulltext/S0092-8674(19)30640-3?_returnURL=https%3A%2F%2Flinkinghub.elsevier.com%2Fretrieve%2Fpii%2FS0092867419306403%3Fshowall%3Dtrue) was done by, **Ray Dolan**, **Zeb Kurth-Nelson** and **Tim Behrens**, and was a collaboration between DeepMind, the Wellcome Centre for Human Neuroimaging (UCL), the Max Planck-UCL Centre for Computational Psychiatry and Ageing Research, and the Wellcome Centre For Integrative Neuroimaging (Oxford).
