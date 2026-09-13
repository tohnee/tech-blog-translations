---
title: "Improving language models by retrieving from trillions of tokens"
source: https://deepmind.google/blog/improving-language-models-by-retrieving-from-trillions-of-tokens/
site: deepmind
date: 2021-12-08
authors: Sebastian Borgeaud, Arthur Mensch, Jordan Hoffmann, Laurent Sifre
crawled: 2026-09-13
---

In recent years, significant performance gains in autoregressive language modeling have been achieved by increasing the number of parameters in Transformer models. This has led to a tremendous increase in training energy cost and resulted in a generation of dense “Large Language Models” (LLMs) with 100+ billion parameters. Simultaneously, large datasets containing trillions of words have been collected to facilitate the training of these LLMs.

We explore an alternate path for improving language models: we augment transformers with retrieval over a database of text passages including web pages, books, news and code. We call our method RETRO, for “Retrieval Enhanced TRansfOrmers”.

![Diagram of the Retrieval Enhanced Transformer (RETRO) architecture, showing how an input sequence queries a 2-trillion-word retrieval database to find neighbor text passages. These neighbors are processed by a Transformer Encoder, which feeds into cross-attention layers interleaved with self-attention and feed-forward layers to generate the factual output sequence.](https://lh3.googleusercontent.com/lYNi-AqFlA3pfPnWLqSctAtdNiqc7YNypluBwFQf_AnfcIbPHV_JmNMYLMz6dlkAWxZyAJ_u_Z55KkHk5cdkszU079Ut2zCDcU2Ks5M2Q7mMCT-k4bs=w1440)

Figure 1: A high-level overview of Retrieval Enhanced TransfOrmers (RETRO).

In traditional transformer language models, the benefits of model size and data size are linked: as long as the dataset is large enough, language modeling performance is limited by the size of the model. However, with RETRO the model is not limited to the data seen during training– it has access to the entire training dataset through the retrieval mechanism. This results in significant performance gains compared to a standard Transformer with the same number of parameters. We show that language modeling improves continuously as we increase the size of the retrieval database, at least up to 2 trillion tokens – 175 full lifetimes of continuous reading.

![Line plot showing that evaluation bits-per-byte (where lower is better) decreases steadily as the retrieval database size increases up to 2 trillion tokens, across four RETRO model sizes: 172M, 425M, 1.5B, and 7.5B parameters. Baseline models without retrieval (0 tokens) are represented by 'x' markers on the y-axis.](https://lh3.googleusercontent.com/tukJA8I3-EIxYEk7XHOZe7DfYWwqD7oJS25dmkd0aA5bzosuZw5oVk_OdHs-Lb8XcyU7JINqoU9BxiP4p-9PCF7nWFda0-aq5ELy9doyhUGTcdjC=w1440)

Figure 2: Increasing the size of the retrieval dataset results in large gains in model performance.

For each text passage (approximately a paragraph of a document), a nearest-neighbor search is performed which returns similar sequences found in the training database, and their continuation. These sequences help predict the continuation of the input text. The RETRO architecture interleaves regular self-attention at a document level and cross-attention with retrieved neighbors at a finer passage level. This results in both more accurate and more factual continuations. Furthermore, RETRO increases the interpretability of model predictions, and provides a route for direct interventions through the retrieval database to improve the safety of text continuation. In our experiments on the Pile, a standard language modeling benchmark, a 7.5 billion parameter RETRO model outperforms the 175 billion parameter Jurassic-1 on 10 out of 16 datasets and outperforms the 280B Gopher on 9 out of 16 datasets.

Below, we show two samples from our 7B baseline model and from our 7.5B RETRO model model that highlight how RETRO’s samples are more factual and stay more on topic than the baseline sample.

![Comparison of generated text outputs given the input prompt of the first 100 digits of Pi. The baseline 7.1B model sample hallucinates incorrect digits, whereas the RETRO 7.5B model sample successfully retrieves and continues the precise mathematical sequence of Pi.](https://lh3.googleusercontent.com/oHXq-pFgx9VSfPy9eQbc7Gl8I_1uKGUl70PBwIymgkFQuppSbgQUMGcZZhBHh5BAqu_fkyqxasWctbivHEl3VLmheq_wejlnP7pXeyHAkmZtgi9kVg=w1440)

Figure 3: The baseline only generates 2 correct digits. With RETRO, the correct digits are generated after being retrieved by the database.

![A text comparison showcasing model generations for the input prompt "Beavers are interesting animals that live near rivers. They build". The baseline 7.1B sample begins with beavers but quickly goes off-topic to discuss frogs and golden retrievers. In contrast, the RETRO 7.5B sample continues with factually accurate information solely about beavers building dams and using their teeth.](https://lh3.googleusercontent.com/Hxp8tPIM9Hxp7v-4XlgkFOtXL7zgsQnR6eftJIghYgUPdiZ-ypyHynDPD04xnr75coGR4ulINqTGMe5lHY1R_bUA6uNJSJTVNAbX0eQ_A8RDXUTk8FM=w1440)

Figure 4: The RETRO model stays more on-topic than the baseline sample.Type image caption here (optional)
