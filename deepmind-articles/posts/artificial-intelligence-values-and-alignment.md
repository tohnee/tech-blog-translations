---
title: "Artificial Intelligence, Values and Alignment"
source: https://deepmind.google/blog/artificial-intelligence-values-and-alignment/
site: deepmind
date: 2020-01-13
authors: Iason Gabriel
crawled: 2026-09-13
---

The question of ‘value alignment’ centres upon how to ensure that AI systems are properly aligned with human values. It can be broken down into two parts. The first part is technical and focuses on how to encode values or principles in artificial agents, so that they reliably do what they ought to do. The second part is normative, and focuses on what values or principles it would be right to encode in AI.

This paper focuses on the second question, paying particular attention to the fact that we live in a pluralistic world where people have a variety of different beliefs about value. Ultimately, I suggest that we need to devise principles for alignment that treat people fairly and command widespread support despite this difference of opinion.

## Moral considerations

Any new technology generates moral considerations. Yet the task of imbuing artificial agents with moral values becomes particularly important as computer systems operate with greater autonomy and at a speed that ‘increasingly prohibits humans from evaluating whether each action is performed in a responsible or ethical manner’.

The first part of the paper notes that while technologists have an important role to play in building systems that respect and embody human values, the task of selecting appropriate values is not one that can be settled by technical work alone. This becomes clear when we look at the different ways in which value alignment could be achieved, at least within the reinforcement learning paradigm.

One set of approaches try to specify a reward function for an agent that would lead it to promote the right kind of outcome and act in ways that are broadly thought to be ethical. For this approach to succeed, we need to specify appropriate goals for artificial agents and encode them in AI systems – which is far from straightforward. A second family of approaches proceeds differently. Instead of trying to specify the correct reward function for the agent upfront, it looks at ways in which an agent could learn the correct reward from examples of human behavior or human feedback. However, the question then becomes what data or feedback to train the agent on – and how this decision can be justified.

Either way, important normative questions remain.

## Alignment with what?

A key concern among AI researchers is that the systems they build are properly responsive to human direction and control. Indeed, as Stuart Russell notes, it is important that artificial agents understand the real meaning of the instructions they are given, and that they do not interpret them in an excessively literal way – with the story of King Midas serving as a cautionary tale.

At the same time, there is growing recognition that AI systems may need to go beyond this – and be designed in a way that leads them to do the right thing by default, even in the absence of direct instructions from a human operator.

One promising approach holds that AI should be designed to align with human preferences. In this way, AI systems would learn to avoid outcomes that very few people wanted or desired. However, this approach also has certain weaknesses. Revealed preferences can be irrational or based on false information. They may also be malicious. Furthermore, preferences are sometimes ‘adaptive’: people who lead lives affected by poverty or discrimination may revise their hopes and expectations downwards in order to avoid disappointment. By aligning itself with existing human preferences, AI could therefore come to act on data that is heavily compromised.

To address this weakness, I suggest that AI systems need to be properly responsive to underlying human interests and values. A principle-based approach to AI alignment, which takes into account both of these factors, would yield agents that are less likely to do harm and more likely to promote human well-being. A principle-based approach to alignment could also be sensitive to other considerations, such as the welfare of future generations, non-human animals and the environment.

## Three approaches

The final part of the paper looks at the ways in which principles for AI alignment might be identified.

In this context, I suggest that the main challenge is not to identify ‘true’ moral principles and encode them in AI – for even if we came to have great confidence in the truth of a single moral theory there would still be people with different beliefs and opinions who disagreed with us. Instead, we should try to identify principles for alignment that are acceptable to people who ascribe to a wide range of reasonable points of view. Principles of this kind could be arrived at in at least three different ways.

![Three green diagrams in a row, each one shows an isolated blue dot and a group of green dots in different configurations. The first one is the shape of a circle and labelled Overlapping Consensus, next is a square titled Veil of Ignorance, and lastly a triangle called Social Choice.](https://lh3.googleusercontent.com/T0rInNGPsxKSjpcztLDyeAS68qk04BTGpbRQuufdY4tcfZgBLCzBgkuaf4VnCPkmh7bYyhwPtsWbczbNyu1fj8KjeXt4aUCPNxitiCUMjFWMDrh4lA=w1440)

One approach looks at the possibility that there is an overlapping consensus between the moral beliefs held by people around the world. If such a consensus exists, then AI could be aligned with it – and potentially command widespread support – without encountering the problem of value imposition. In this regard, human rights are particularly promising. For while the idea of universal human rights is not wholly uncontested, the principles they embody command significant international support in practice. They also find justification in African, Islamic, Western, and Confucian philosophical traditions.

A second approach to pluralistic value alignment seeks to model fair principles for AI using the idea of a ‘veil of ignorance’. The veil of ignorance is a device proposed by the philosopher John Rawls, to help people with different values and perspectives agree upon principles of justice for a society. The central claim is that when choosing principles of this kind, people should do so from an imaginary position where they do not know who they will be in that society, or what specific moral view they will hold. As a result, they will deliberate impartially and choose principles that do not unduly favour themselves. A similar approach could be used to model principles for AI.

Although it is difficult to say what people would choose in this situation without knowing more about the specific form of AI in question, it seems plausible that they would want to ensure that this technology is safe, amenable to human control, and that its benefits are distributed widely.

The final approach looks at ways in which social choice theory can be used to combine different viewpoints and inform the direction AI should take. One school of thought focuses on mathematical integration of individual preferences into a single ranking – which could be used to guide AI. More promising still are democratic methods such as voting and broad-based deliberation. When used successfully, these approaches reflect the value of equality and have the potential to ensure that principles for AI alignment enjoy widespread legitimacy.

## Further research

Each proposal discussed here is tentative. They can be developed and combined in many different ways. This paper has benefited from feedback provided by over fifty people, including from audiences at workshops convened at Stanford University, Princeton University, PAI, the University of Warwick, and the University of California, Berkeley. Moving forward, our hope is that this paper can contribute to the growing conversation about AI systems and their alignment with human values.

**Notes**

1. Colin Allen, Iva Smit and Wendell Wallach, ‘Artificial Morality: Top-Down, Bottom-Up and Hybrid Approaches’, Ethics and Information Technology 7 (2005), p. 149.
2. Joshua Cohen, The Arc of the Moral Universe and Other Essays (Harvard, 2010); Jack Donnelly, ‘The Relative Universality of Human Rights’, Human Rights Quarterly 29 (2007)
