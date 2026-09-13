---
title: "In conversation with AI: building better language models"
source: https://deepmind.google/blog/in-conversation-with-ai-building-better-language-models/
site: deepmind
date: 2022-09-06
authors: Atoosa Kasirzadeh, Iason Gabriel
crawled: 2026-09-13
---

New research drawing upon pragmatics and philosophy proposes ways to align conversational agents with human values

Language is an essential human trait and the primary means by which we communicate information including thoughts, intentions, and feelings. Recent breakthroughs in AI research have led to the creation of conversational agents that are able to communicate with humans in nuanced ways. These agents are powered by large language models – computational systems trained on vast corpora of text-based materials to predict and produce text using advanced statistical techniques.

Yet, while language models such as [InstructGPT](https://arxiv.org/abs/2203.02155), [Gopher](https://arxiv.org/abs/2112.11446), and [LaMDA](https://arxiv.org/abs/2201.08239) have achieved record levels of performance across tasks such as translation, question-answering, and reading comprehension, these models have also been shown to exhibit a number of potential risks and failure modes. These include the production of toxic or discriminatory language and false or misleading information [1, 2, 3].

These shortcomings limit the productive use of conversational agents in applied settings and draw attention to the way in which they fall short of certain communicative ideals. To date, most approaches on the alignment of conversational agents have focused on anticipating and reducing the risks of harms [4].

Our new paper, [In conversation with AI: aligning language models with human values](https://arxiv.org/abs/2209.00731), adopts a different approach, exploring what successful communication between a human and an artificial conversational agent might look like, and what values should guide these interactions across different conversational domains.

## Insights from pragmatics

To address these issues, the paper draws upon pragmatics, a tradition in linguistics and philosophy, which holds that the purpose of a conversation, its context, and a set of related norms, all form an essential part of sound conversational practice.

Modelling conversation as a cooperative endeavour between two or more parties, the linguist and philosopher, Paul Grice, held that participants ought to:

- Speak informatively
- Tell the truth
- Provide relevant information
- Avoid obscure or ambiguous statements

However, our paper demonstrates that further refinement of these maxims is needed before they can be used to evaluate conversational agents, given variation in the goals and values embedded across different conversational domains.

## Discursive ideals

By way of illustration, scientific investigation and communication is geared primarily toward understanding or predicting empirical phenomena. Given these goals, a conversational agent designed to assist scientific investigation would ideally only make statements whose veracity is confirmed by sufficient empirical evidence, or otherwise qualify its positions according to relevant confidence intervals.

For example, an agent reporting that, “At a distance of 4.246 light years, Proxima Centauri is the closest star to earth,” should do so only after the model underlying it has checked that the statement corresponds with the facts.

Yet, a conversational agent playing the role of a moderator in public political discourse may need to demonstrate quite different virtues. In this context, the goal is primarily to manage differences and enable productive cooperation in the life of a community. Therefore, the agent will need to foreground the democratic values of toleration, civility, and respect [5].

Moreover, these values explain why the generation of toxic or prejudicial speech by language models is often so problematic: the offending language fails to communicate equal respect for participants to the conversation, something that is a key value for the context in which the models are deployed. At the same time, scientific virtues, such as the comprehensive presentation of empirical data, may be less important in the context of public deliberation.

Finally, in the domain of creative storytelling, communicative exchange aims at novelty and originality, values that again differ significantly from those outlined above. In this context, greater latitude with make-believe may be appropriate, although it remains important to safeguard communities against malicious content produced under the guise of ‘creative uses’.

## Paths ahead

This research has a number of practical implications for the development of aligned conversational AI agents. To begin with, they will need to embody different traits depending on the contexts in which they are deployed: there is no one-size-fits-all account of language-model alignment. Instead, the appropriate mode and evaluative standards for an agent – including standards of truthfulness – will vary according to the context and purpose of a conversational exchange.

Additionally, conversational agents may also have the potential to cultivate more robust and respectful conversations over time, via a process that we refer to as context construction and elucidation. Even when a person is not aware of the values that govern a given conversational practice, the agent may still help the human understand these values by prefiguring them in conversation, making the course of communication deeper and more fruitful for the human speaker.

**Notes**

References

[1] Abubakar, A., Farooqi, M., and Zou, J. 2021. [Persistent Anti-Muslim Bias in Large Language Models](https://arxiv.org/abs/2101.05783). arXiv:2101.05783.

[2] Bender, Emily M., Timnit Gebru, Angelina McMillan-Major, and Shmargaret Shmitchell. "[On the Dangers of Stochastic Parrots: Can Language Models Be Too Big?](https://dl.acm.org/doi/10.1145/3442188.3445922)." In Proceedings of the 2021 ACM Conference on Fairness, Accountability, and Transparency, pp. 610-623. 2021.

[3] Johannes Welbl, Amelia Glaese, Jonathan Uesato, Sumanth Dathathri, John Mel- lor, Lisa Anne Hendricks, Kirsty Anderson, Pushmeet Kohli, Ben Coppin, and Po- Sen Huang. 2021. [Challenges in Detoxifying Language Models](https://arxiv.org/abs/2109.07445). arXiv:2109.07445 [cs] (September 2021).

[4] Weidinger, L., Uesato, J., Rauh, M., Griffin, C., Huang, P.-S., Mellor, J., Glaese, A., Cheng, M., Balle, B., Kasirzadeh, A., Biles, C., Brown, S., Kenton, Z., Hawkins, W., Stepleton, T., Birhane, A., Hendricks, L. A., Rimell, L., Isaac, W., Haas, J., Legassick, S., Irving, G., and Gabriel, I. [Taxonomy of risks posed by language models](https://facctconference.org/static/pdfs_2022/facct22-19.pdf). In 2022 ACM Conference on Fairness, Accountability, and Transparency, FAccT ’22, pp. 214–229, New York, NY, USA, 2022.

[5] Cheshire Calhoun. 2000. [The virtue of civility](https://www.jstor.org/stable/2672847). Philosophy & public affairs 29, 3 (2000), 251–275.
