---
title: "A new model and dataset for long-range memory"
source: https://deepmind.google/blog/a-new-model-and-dataset-for-long-range-memory/
site: deepmind
date: 2020-02-10
authors: 
crawled: 2026-09-13
---

This blog introduces a new long-range memory model, the [Compressive Transformer](https://arxiv.org/abs/1911.05507), alongside a new benchmark for book-level language modelling, [PG19](https://github.com/deepmind/pg19). We provide the conceptual tools needed to understand this new research in the context of recent developments in memory models and language modelling.

Throughout our lives, we build up memories that are retained over a diverse array of timescales, from minutes to months to years to decades. When reading a book, we can recall characters who were introduced many chapters ago, or in an earlier book in a series, and reason about their motivations and likely actions in the current context. We can even put the book down during a busy week, and pick up from where we left off without forgetting the plotline.

We do not achieve such feats by storing every detail of sensory input we receive about the world throughout our lifetimes. [Our brains select, filter, and integrate](https://www.ncbi.nlm.nih.gov/pubmed/28641107) input stimuli based on factors of relevance, surprise, perceived danger, and repetition. In other words, we compress lifelong experience to a set of salient memories which help us understand the past, and better anticipate the future. A major goal of AI researchers is discovering ways of implementing such abilities in computational systems and benchmarks which require complex reasoning over long time-spans.

Memory systems for artificial neural networks have advanced considerably in the past two decades. In this post, we look to past advances to explore why this is such a difficult task and consider how natural language modelling could offer an effective means of designing better long range memory systems? We reflect on the necessity for better compressive memory architectures, and sparse memory access mechanisms, to work towards the goal of incorporating lifelong reasoning in our computational systems.

## A brief history of memory in deep learning

> There is no memory or retentive faculty based on lasting impression. What we designate as memory is but increased responsiveness to repeated stimuli.

Nikola Tesla

One of the earliest and most widely-used memory architectures in present day is a recurrent neural network (RNN) called the [Long Short-Term-Memory](https://www.bioinf.jku.at/publications/older/2604.pdf) (LSTM). The LSTM maintains a compact memory in the form of a vector of numbers, which it accesses and modifies with gated read, write, and forget operations. It was originally developed on a suite of synthetic tasks that involved learning logical operations on a stream of bits. However, it has since become a ubiquitous model of sequential data: from recognising handwritten notes to predicting the early onset of kidney injury.

One weakness of the LSTM, and of many contemporary RNNs, is capacity. They are designed so that each unit of memory can influence every other unit in memory with a learnable weight. But this results in a computationally inefficient system: the number of learnable parameters in the model grows quadratically with the memory size. For example, an LSTM with a memory of size 64KB results in parameters of size 8GB. Circumventing this memory capacity bottleneck has been an active research area.

![Diagram illustrating an agent interacting with an external memory system over time to write an observed key to memory and later read it to open a chest.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62274c1dcce30901e65d1115_Fig201.svg)

Figure 1. Long-range reasoning is crucial to general intelligence. Here, an agent remembers the existence and location of a key over a long period of time, and recalls this information when a treasure chest is discovered – prompting the agent to return to the remembered location to retrieve the key.

Researchers at DeepMind proposed a novel architecture, the [Differentiable Neural Computer](https://deepmind.com/blog/article/differentiable-neural-computers) (DNC), which augments an LSTM with a much larger memory matrix to address these deficits. The DNC uses an attention operation to read from this memory matrix. In visual attention, our eyes are drawn by pertinent objects in a visual scene–for example, one might typically spend more time observing a friend’s face during an emotional conversation than on noticing their shoes. Here, memory models can attend to particular events/data in the past. This attention operation requires a fixed number of parameters, independent of the memory size, and so the memory capacity of the model can be significantly increased.

Alongside the DNC, recurrent neural networks with an additional attention mechanism were showing promise in the domains of [translation](https://arxiv.org/abs/1409.0473) and [question answering](https://arxiv.org/abs/1410.3916). These models were able to reason over time using two memory structures: a small and compact LSTM memory and a large external memory. However, more recently researchers at Google Brain Team proposed the Transformer which removes the LSTM, and only uses attention to transmit [information across time](https://arxiv.org/abs/1706.03762).

![The phrase "the agreement on the European Economic Area was signed in August 1992" is translated into French above, with lines connecting each word in English with its French equivalent.](https://lh3.googleusercontent.com/4-K4RqcoDw0FRzBhqYgUMhUkaAcJ8nLJ-H4QHp3tjxPQaNQ1HRwQDbuOylvPjjzOxJC3__ME35ccTz3pzWj8LGT-ZYl-eJKoIdJlvKL5HNoePUUVgkU=w1440)

Figure 2. A visualisation of the neural network’s attention for English to French translation. Source: Attention and Augmented Recurrent Neural Networks, Olah & Carter, 2016

The Transformer was originally shown to significantly outperform recurrent neural networks for machine translation. However it has since been applied to a range of applications in natural language processing, from question answering, document summarisation, sentiment classification and the modelling of natural language – a task that has seen particular exciting developments over the past year.

## Modelling natural language

Finding machine learning tasks which both drive the development of better memory architectures and push us further towards artificial general intelligence is challenging. Statistical language modelling is one such task that we believe could be valuable for both purposes. Language models work by sequentially predicting the next word in a stream of text. They can be used to model existing texts and also to generate novel texts. As they get better at modelling the past, their predictions become more accurate, and the texts they generate become more realistic.

In Claude Shannon’s seminal article “[A Mathematical Theory of Communication](https://onlinelibrary.wiley.com/doi/10.1002/j.1538-7305.1948.tb01338.x)” published in 1948, which founded the field of information theory, he discussed primitive language models and illustrated how adding more context improves the quality and realism of generated text. He does this by introducing the most simple model of English text, which has no contextual modelling at all – a character-level model which treats each character independently. By sampling characters with their relative frequencies (8% of the time for ‘a’, 1.5% for ‘b’ etc.) we arrive with a nonsensical string :

**XFOML RXKHRJFFJUJ ZLPWCFWKCYJ FFJEYVKCQSGHYD QPAAMKBZAACIBZLHJQD.**

However, he remarks at the improvement in sample quality if one instead models the probability of words independently. Now the modelled context is approximately 7X larger (the average number of characters in a word):

**REPRESENTING AND SPEEDILY IS AN GOOD APT OR COME CAN DIFFERENT NATURAL HERE HE THE A IN CAME THE TO OF TO EXPERT GRAY COME TO FURNISHES THE LINE MESSAGE HAD BE THESE.**

By modelling the probability of word pairs, a further 2X in context length, even more realistic text emerges:

**THE HEAD AND IN FRONTAL ATTACK ON AN ENGLISH WRITER THAT THE CHARACTER OF THIS POINT IS THEREFORE ANOTHER METHOD FOR THE LETTERS THAT THE TIME OF WHO EVER TOLD THE PROBLEM FOR AN UNEXPECTED**

In other words, an increase in the length of context leads to an improvement in the quality of text generated. Shannon remarks on the quality of his produced samples and conjectures that natural text samples may emerge from a sufficiently complex statistical model, “The particular sequence of ten words “attack on an English writer that the character of this” is not at all unreasonable. It appears then that a sufficiently complex stochastic process will give a satisfactory representation of a discrete source”.

One criticism of language modelling as a task for long-range reasoning is that models can capture a large portion of their predictions from the local context. Neural language models have traditionally ignored the wider context, focusing mostly on the short term. For example, in 2017 [Dailuk et al.](https://arxiv.org/abs/1702.04521) found their neural language model rarely attends beyond the preceding five words. However in the past year large Transformer models have been shown to make use of hundreds of words of context to generate ever-more realistic text with a longer range of coherence. A demo from [OpenAI’s GPT-2](https://openai.com/blog/better-language-models/), a 1.5B parameter Transformer, indicate that the model is able to generate realistic text and retain key entities (e.g. Dr Jorge Pérez and unicorns) across multiple paragraphs:

**The scientist named the population, after their distinctive horn, Ovid’s Unicorn. These four-horned, silver-white unicorns were previously unknown to science.**

**Now, after almost two centuries, the mystery of what sparked this odd phenomenon is finally solved.**

**Dr. Jorge Pérez, an evolutionary biologist from the University of La Paz, and several companions, were exploring the Andes Mountains when they found a small valley, with no other animals or humans. Pérez noticed that the valley had what appeared to be a natural fountain, surrounded by two peaks of rock and silver snow.**

**Pérez and the others then ventured further into the valley. “By the time we reached the top of one peak, the water looked blue, with some crystals on top,” said Pérez.**

**Pérez and his friends were astonished to see the unicorn herd. These creatures could be seen from the air without having to move too much to see them – they were so close they could touch their horns.**

**While examining these bizarre creatures the scientists discovered that the creatures also spoke some fairly regular English. Pérez stated, “We can see, for example, that they have a common ‘language,’ something like a dialect or dialectic.”**

**Dr. Pérez believes that the unicorns may have originated in Argentina, where the animals were believed to be descendants of a lost race of people who lived there before the arrival of humans in those parts of South America.**

**While their origins are still unclear, some believe that perhaps the creatures were created when a human and a unicorn met each other in a time before human civilization. According to Pérez, “In South America, such incidents seem to be quite common.”**

**However, Pérez also pointed out that it is likely that the only way of knowing for sure if unicorns are indeed the descendants of a lost alien race is through DNA. “But they seem to be able to communicate in English quite well, which I believe is a sign of evolution, or at least a change in social organization,” said the scientist.**

## Transferring knowledge

Such samples would likely astound Shannon, 70 years on from his early language model experiments. However the real benefit of powerful neural language models – and their relevance to the goal of AGI – is their ability to transfer knowledge to a suite of tasks. In the process of learning how to model text, neural language models appear to build up a knowledge-base of associations, and a plethora of skills.

For instance, researchers at OpenAI showed that GPT-2 can be applied to natural-language processing tasks such as question answering, paraphrasing, or sentiment analysis with surprisingly good performance – especially for a model that has never been explicitly trained to perform such tasks. When large Transformer language models are fine-tuned on particular tasks such as question answering, the resulting performance is significantly better than models that were designed and trained solely for question answering. Google’s prominent natural language model, [BERT](https://arxiv.org/abs/1810.04805), achieves state-of-the-art performance on a wide array of NLP benchmarks, and is now [a part of Google Search](https://www.blog.google/products/search/search-language-understanding-bert/). And more recently, it was shown that GPT-2 can learn to play rudimentary chess by training it on strings of [game moves](https://slatestarcodex.com/2020/01/06/a-very-unlikely-chess-game/).

## Benchmarking language models

A popular long-range language model benchmark is [WikiText-103](https://www.salesforce.com/products/einstein/ai-research/the-wikitext-dependency-language-modeling-dataset/), which is comprised of English-language Wikipedia articles, and was developed by researchers at [Salesforce AI](https://arxiv.org/abs/1609.07843). Articles are around 3,600 words on average, which, at the time of creation, was far beyond the memory window of state-of-the-art models.

However researchers at Google recently showed that a Transformer variant called the TransformerXL – which maintains a memory of past network activations and recently obtained state-of-the-art results on WikiText-103 – can make use of contexts spanning over [one thousand words](https://arxiv.org/abs/1901.02860). This raises the question: will models soon saturate these benchmarks? As such, we’ve compiled and released a new, longer-range language model benchmark based on books.

## A new dataset for long-term memory research

To support growing interest in long-range sequence models, we are releasing a new language modelling benchmark, [**PG-19**](https://github.com/deepmind/pg19), which is derived from books in the [Project Gutenberg online library](https://www.gutenberg.org/).

Books provide a rich context for the development of long-range memory models. We selected a subset of approximately 28,000 books from Project Gutenberg published before 1919. Unlike prior language modeling dataset releases, we apply very little pre-processing to the text. For example, we do not limit the vocabulary size of the data or censor numbers, to avoid the filtering of useful information.

PG-19 is over double the size of prior language modelling benchmarks, such as the [Billion Word Benchmark](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/41880.pdf), and contains text that is over 10X longer in context than the prior long-range language model benchmark, WikiText-103. We provide a comparative table of existing language modelling benchmarks, below:

![A comparison table of language modelling benchmarks including 1B Word, Penn Treebank, WikiText-103, and PG-19, highlighting PG-19's significantly larger average context length of 69K words and open vocabulary size.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62274ca26f79eae3412a2cbf_Fig203.svg)

## Compressive Transformer

Alongside a new benchmark, we propose a long-range memory model called the [Compressive Transformer](https://arxiv.org/abs/1911.05507). We take inspiration from the role of sleep in the formation of [consolidated episodic memories](https://www.ncbi.nlm.nih.gov/pubmed/28641107). Sleep is known to be crucial for memory, and it’s thought that sleep serves to compress and consolidate memories, thereby improving reasoning abilities for memory tasks. In the Compressive Transformer, granular memories akin to episodic memories are collected online as the model passes over a sequence of inputs; over time, they are eventually compacted.

The Compressive Transformer uses attention to select information from the past, like the Transformer. It maintains a short-term memory of past activations, in the same style as the recently-proposed [TransformerXL](https://arxiv.org/abs/1901.02860). Where the TransformerXL discards past activations when they become older, the Compressive Transformer instead compacts them into a compressed memory. The compression is performed by a neural network guided by an auxiliary loss that guides it to keep around task-relevant information. It can learn to filter out irrelevant memories, as well as combine memories so that the salient information is preserved and retrievable over a longer period of time.

![Diagram showing the memory structure of a Compressive Transformer, with three sections over a timeline: "Sequence" and "Memory" represented by orange dots, and "Compressed Memory" represented by cyan dots spanning a much denser timeline.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62274cba2b4e7e19932faaf2_Fig204.gif)

Figure 3. Compressive Transformer: a long-range sequence attentive sequence model which characterises the past with a granular short-term memory with a coarse compressed memory.

We find the Compressive Transformer has state-of-the-art performance in the modelling of natural language for two widely-used long-range benchmarks, **WikiText-103** and **Enwik8,** compared to [published results](http://nlpprogress.com/english/language_modeling.html) that do not use additional sources of training data. We also show it can be used effectively to model speech, handles rare words especially well, and can be used within a reinforcement learning agent to solve a memory task.

![A comparison table of language model perplexity across word frequency buckets, demonstrating that the Compressive Transformer outperforms LSTM and TransformerXL models, with the largest percentage gains in predicting rare words (frequency < 1K).](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62274cd01da7d8a1f9b80635_Fig204.svg)

We find the Compressive Transformer produces the largest performance gain in modelling long-context book text from the PG-19 benchmark. The model’s conditional samples can be used to write book-like extracts. Below we show a sample that is fed a paragraph of text to be used as context, taken from “The Patrol of the Sun Dance” by Ralph Connor, which the model has not previously seen.

**Context from** **The Patrol of the Sun Dance Trail by Ralph Connor**

**Along the tote-road, which ran parallel to the steel, a man, dark of skin, slight but wiry, came running, his hard panting, his streaming face, his open mouth proclaiming his exhaustion. At a little trail that led to the left he paused, noted its course toward the flaunting flag, turned into it, then struggled up the rocky hillside till he came to the wooden shack, with a deep porch running round it, and surrounded by a rustic fence which enclosed a garden whose neatness illustrated a characteristic of the British soldier. The runner passed in through the gate and up the little gravel walk and began to ascend the steps...**

**Continuation by the Compressive Transformer**

**...As though by mutual consent, all the three members of the Superintendent Force were standing on the veranda watching his progress, a man came strolling slowly down the path, stopping often to gaze curiously about him, then stopping once more when he saw the four standing on the veranda. His face was dark, his eyes prominent, and the lines that furrowed his forehead showed marks of many woes, yet his step was alert and he began to mount the steps with steady strides.**

**The man’s attention was diverted by the unexpected appearance of the two policemen; a third man came slipping up, grumbling under his breath, and stopped long enough to look doubtfully around him, then slipped away again. In the meantime, the four on the veranda continued to watch the approach of the new arrival. In spite of himself, the Superintendent Force became conscious of a curious feeling–uneasiness that was almost fear–in the presence of that strange man. He would not allow himself to admit the fact, yet he felt it in his bones. But to the watchers, the plain, everyday features of that stranger and his coming, seemed only just what the Seven White Shee owed him–their weight, their hurry, their blast...**

The Compressive Transformer is able to produce narrative in a variety of styles, from multi-character dialogue, first-person diary entries, or third-person prose. Although the model does not have an understanding of language that’s grounded in the real world, or the events that take place in it – by capturing longer-range correlations, we see the emergence of more coherent text.

## The future of memory architectures

As we strive to create agents that operate over days, weeks or even years, it will be impractical to compute over all raw input data at each timestep. Even with the current growth in computing power, we will need to develop compressive and sparse architectures for memory to build representations and reason about actions.

Models which are able to capture relevant correlations across days, months, or years’ worth of experience are on the horizon. We believe the route to more powerful reasoning over time will emerge from better selective attention of the past, and more effective mechanisms to compress it. As we explore ideas in this space, we need tasks and datasets that span longer and longer time intervals. The PG-19 dataset can help researchers move in this direction, presenting textual data in the longest form that we typically consume as humans: full-length books. We hope that its release will spur interest in new models that compress the past in order to predict the future and act effectively in the present.

Read more

[Compressive Transformer paper](https://arxiv.org/abs/1911.05507)

[PG-19 Benchmark](https://github.com/deepmind/pg19)
