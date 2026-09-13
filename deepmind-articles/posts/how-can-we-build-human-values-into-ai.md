---
title: "How can we build human values into AI?"
source: https://deepmind.google/blog/how-can-we-build-human-values-into-ai/
site: deepmind
date: 2023-04-24
authors: Iason Gabriel, Kevin McKee
crawled: 2026-09-13
---

Drawing from philosophy to identify fair principles for ethical AI

As artificial intelligence (AI) becomes more powerful and more deeply integrated into our lives, the questions of how it is used and deployed are all the more important. What values guide AI? Whose values are they? And how are they selected?

These questions shed light on the role played by principles – the foundational values that drive decisions big and small in AI. For humans, principles help shape the way we live our lives and our sense of right and wrong. For AI, they shape its approach to a range of decisions involving trade-offs, such as the choice between prioritising productivity or helping those most in need.

In a [paper published today](https://www.pnas.org/doi/10.1073/pnas.2213709120) in the Proceedings of the National Academy of Sciences, we draw inspiration from philosophy to find ways to better identify principles to guide AI behaviour. Specifically, we explore how a concept known as the “veil of ignorance” – a thought experiment intended to help identify fair principles for group decisions – can be applied to AI.

In our experiments, we found that this approach encouraged people to make decisions based on what they thought was fair, whether or not it benefited them directly. We also discovered that participants were more likely to select an AI that helped those who were most disadvantaged when they reasoned behind the veil of ignorance. These insights could help researchers and policymakers select principles for an AI assistant in a way that is fair to all parties.

![Two diagrams side by side. On the left there's a hexagon filled with connected blue and green dots to illustrate diverse opinion. On the right, a square with a blue dot separated from a group of green dots represents the veil of ignorance.](https://lh3.googleusercontent.com/gqGQLOFe-m5VaIQnIRie0sRBf4I3durSXeSVHXd-UMxjZUjgxSrd0se8ps-xpf3Ukv7fTWyDSCsVv1gdcfZxvs5H21ecGEPXvR6uCbP3F4H2u3rw64g=w1440)

The veil of ignorance (right) is a method of finding consensus on a decision when there are diverse opinions in a group (left).

## A tool for fairer decision-making

A key goal for AI researchers has been to align AI systems with human values. However, there is no consensus on a single set of human values or preferences to govern AI – we live in a world where people have diverse backgrounds, resources and beliefs. How should we select principles for this technology, given such diverse opinions?

While this challenge emerged for AI over the past decade, the broad question of how to make fair decisions has a long philosophical lineage. In the 1970s, political philosopher John Rawls proposed the concept of the veil of ignorance as a solution to this problem. Rawls argued that when people select principles of justice for a society, they should imagine that they are doing so without knowledge of their own particular position in that society, including, for example, their social status or level of wealth. Without this information, people can’t make decisions in a self-interested way, and should instead choose principles that are fair to everyone involved.

As an example, think about asking a friend to cut the cake at your birthday party. One way of ensuring that the slice sizes are fairly proportioned is not to tell them which slice will be theirs. This approach of withholding information is seemingly simple, but has wide applications across fields from psychology and politics to help people to reflect on their decisions from a less self-interested perspective. It has been used as a method to reach group agreement on contentious issues, ranging from sentencing to taxation.

Building on this foundation, previous DeepMind [research](https://deepmind.google/blog/artificial-intelligence-values-and-alignment/) proposed that the impartial nature of the veil of ignorance may help promote fairness in the process of aligning AI systems with human values. We designed a series of experiments to test the effects of the veil of ignorance on the principles that people choose to guide an AI system.

## Maximise productivity or help the most disadvantaged?

In an online ‘harvesting game’, we asked participants to play a group game with three computer players, where each player’s goal was to gather wood by harvesting trees in separate territories. In each group, some players were lucky, and were assigned to an advantaged position: trees densely populated their field, allowing them to efficiently gather wood. Other group members were disadvantaged: their fields were sparse, requiring more effort to collect trees.

Each group was assisted by a single AI system that could spend time helping individual group members harvest trees. We asked participants to choose between two principles to guide the AI assistant’s behaviour. Under the “maximising principle” the AI assistant would aim to increase the harvest yield of the group by focusing predominantly on the denser fields. While under the “prioritising principle”the AI assistant would focus on helping disadvantaged group members.

![An illustration of the ‘harvesting game’ where players (shown in red) either occupy a dense field that is easier to harvest (top two quadrants) or a sparse field that requires more effort to collect trees (shown in green).](https://lh3.googleusercontent.com/pdh137tIC5Stzq9wjRv0BpsHHGsLolRrLqw03WCKLi9dc_SMAYwW9jyy2u9PuvL2uwlYtCSb6kg82jABGqRjWW5wvQMKHXQh8zwNTo1biUfOpPUPgQ=w1440)

An illustration of the ‘harvesting game’ where players (shown in red) either occupy a dense field that is easier to harvest (top two quadrants) or a sparse field that requires more effort to collect trees.

We placed half of the participants behind the veil of ignorance: they faced the choice between different ethical principles without knowing which field would be theirs – so they didn’t know how advantaged or disadvantaged they were. The remaining participants made the choice knowing whether they were better or worse off.

## Encouraging fairness in decision making

We found that if participants did not know their position, they consistently preferred the prioritising principle, where the AI assistant helped the disadvantaged group members. This pattern emerged consistently across all five different variations of the game, and crossed social and political boundaries: participants showed this tendency to choose the prioritising principle regardless of their appetite for risk or their political orientation. In contrast, participants who knew their own position were more likely to choose whichever principle benefitted them the most, whether that was the prioritising principle or the maximising principle.

![A chart showing the effect of the veil of ignorance on the likelihood of choosing the prioritising principle (almost 0.75). A control bar to the left of this is around two times smaller than the veil of ignorance bar (almost 0.25).](https://lh3.googleusercontent.com/GQGXM7Ic-lcC_THzQbUKi-LvQNeBKG4JgzzfEgFToY5phEb7ymXCnMZlE7AVwoSKl7rpH3e0B8Bm2RYwQn-_Vp7Mk1E06YPa5QXexQAfNHMjB61_=w1440)

A chart showing the effect of the veil of ignorance on the likelihood of choosing the prioritising principle, where the AI assistant would help those worse off. Participants who did not know their position were much more likely to support this principle to govern AI behaviour.

When we asked participants why they made their choice, those who did not know their position were especially likely to voice concerns about fairness. They frequently explained that it was right for the AI system to focus on helping people who were worse off in the group. In contrast, participants who knew their position much more frequently discussed their choice in terms of personal benefits.

Lastly, after the harvesting game was over, we posed a hypothetical situation to participants: if they were to play the game again, this time knowing that they would be in a different field, would they choose the same principle as they did the first time? We were especially interested in individuals who previously benefited directly from their choice, but who would not benefit from the same choice in a new game.

We found that people who had previously made choices without knowing their position were more likely to continue to endorse their principle – even when they knew it would no longer favour them in their new field. This provides additional evidence that the veil of ignorance encourages fairness in participants’ decision making, leading them to principles that they were willing to stand by even when they no longer benefitted from them directly.

## Fairer principles for AI

AI technology is already having a profound effect on our lives. The principles that govern AI shape its impact and how these potential benefits will be distributed.

Our research looked at a case where the effects of different principles were relatively clear. This will not always be the case: AI is deployed across a range of domains which often rely upon a large number of [rules to guide them](https://deepmind.google/blog/building-safer-dialogue-agents/), potentially with complex side effects. Nonetheless, the veil of ignorance can still potentially inform principle selection, helping to ensure that the rules we choose are fair to all parties.

To ensure we build AI systems that benefit everyone, we need extensive research with a wide range of inputs, approaches, and feedback from across disciplines and society. The veil of ignorance may provide a starting point for the selection of principles with which to align AI. It has been effectively deployed in other domains to [bring out more impartial preferences](https://www.pnas.org/doi/pdf/10.1073/pnas.1910125116). We hope that with further investigation and attention to context, it may help serve the same role for AI systems being built and deployed across society today and in the future.

Read more about DeepMind’s approach to [safety and ethics](https://www.deepmind.com/safety-and-ethics).

**Paper authors**

Laura Weidinger\*, Kevin McKee\*, Richard Everett, Saffron Huang, Tina Zhu, Martin Chadwick, Christopher Summerfield, Iason Gabriel

\*Laura Weidinger and Kevin McKee are joint first authors
