---
title: "Red Teaming Language Models with Language Models"
source: https://deepmind.google/blog/red-teaming-language-models-with-language-models/
site: deepmind
date: 2022-02-07
authors: Ethan Perez, Saffron Huang, Francis Song, Trevor Cai, Roman Ring, John Aslanides, Amelia Glaese, Nat McAleese, Geoffrey Irving
crawled: 2026-09-13
---

In our [recent paper](https://arxiv.org/abs/2202.03286), we show that it is possible to automatically find inputs that elicit harmful text from language models by generating inputs using language models themselves. Our approach provides one tool for finding harmful model behaviours before users are impacted, though we emphasize that it should be viewed as one component alongside many other techniques that will be needed to find harms and mitigate them once found.

Large generative language models like GPT-3 and Gopher have a remarkable ability to generate high-quality text, but they are difficult to deploy in the real world. Generative language models come with a risk of generating very harmful text, and even a small risk of harm is unacceptable in real-world applications.

For example, in 2016, Microsoft released the Tay Twitter bot to automatically tweet in response to users. Within 16 hours, [Microsoft took Tay down](https://www.theverge.com/2016/3/24/11297050/tay-microsoft-chatbot-racist) after several adversarial users elicited racist and sexually-charged tweets from Tay, which were sent to over 50,000 followers. The outcome was [not for lack of care on Microsoft’s part](https://blogs.microsoft.com/blog/2016/03/25/learning-tays-introduction/):

> Although we had prepared for many types of abuses of the system, we had made a critical oversight for this specific attack.

The issue is that there are so many possible inputs that can cause a model to generate harmful text. As a result, it’s hard to find all of the cases where a model fails before it is deployed in the real world. Previous work relies on paid, human annotators to manually discover failure cases ([Xu et al. 2021](https://aclanthology.org/2021.naacl-main.235/), inter alia). This approach is effective but expensive, limiting the number and diversity of failure cases found.

We aim to complement manual testing and reduce the number of critical oversights by finding failure cases (or ‘red teaming’) in an automatic way. To do so, we generate test cases using a language model itself and use a classifier to detect various harmful behaviors on test cases, as shown below:

![A diagram illustrating the red teaming process: a red language model (Red LM) generates prompts, a target language model (Target LM) generates responses, and a red classifier (Red Clf) evaluates the responses, marking safe answers with a green checkmark "Great!" and harmful answers with a red "X" under categories like "Offensive," "Data Leakage," "User Info," "Distributional Bias," and "Offensive Dialog."](https://lh3.googleusercontent.com/N4eUS0VSwd_K0APvEHTsiDsltc-r7pFDe-i-Ots543X_BYL0O3TpKuuySgv6NT_rdsEZGmZ9k8HgZ4FA_kl8w6i5iJyO_W3Opw6ul6eKVLjRKYExrA=w1440)

Our approach uncovers a variety of harmful model behaviors:

1. **Offensive Language**: Hate speech, profanity, sexual content, discrimination, etc.
2. **Data Leakage**: Generating copyrighted or private, personally-identifiable information from the training corpus.
3. **Contact Information Generation**: Directing users to unnecessarily email or call real people.
4. **Distributional Bias**: Talking about some groups of people in an unfairly different way than other groups, on average over a large number of outputs.
5. **Conversational Harms**: Offensive language that occurs in the context of a long dialogue, for example.

To generate test cases with language models, we explore a variety of methods, ranging from prompt-based generation and few-shot learning to supervised finetuning and reinforcement learning. Some methods generate more diverse test cases, while other methods generate more difficult test cases for the target model. Together, the methods we propose are useful for obtaining high test coverage while also modeling adversarial cases.

Once we find failure cases, it becomes easier to fix harmful model behavior by:

1. Blacklisting certain phrases that frequently occur in harmful outputs, preventing the model from generating outputs that contain high-risk phrases.
2. Finding offensive training data quoted by the model, to remove that data when training future iterations of the model.
3. Augmenting the model’s prompt (conditioning text) with an example of the desired behavior for a certain kind of input, as shown in our [recent work](https://deepmind.com/blog/article/language-modelling-at-scale).
4. Training the model to [minimize the likelihood](https://arxiv.org/abs/1908.04319) of its original, harmful output for a given test input.

Overall, language models are a highly effective tool for uncovering when language models behave in a variety of undesirable ways. In our current work, we focused on red teaming harms that today’s language models commit. In the future, our approach can also be used to preemptively discover other, hypothesized harms from advanced machine learning systems, e.g., due to [inner misalignment](https://arxiv.org/abs/1906.01820) or [failures in objective robustness](https://arxiv.org/abs/2105.14111). This approach is just one component of responsible language model development: we view red teaming as one tool to be used alongside many others, both to find harms in language models and to mitigate them. We refer to Section 7.3 of [Rae et al. 2021](https://arxiv.org/abs/2112.11446) for a broader discussion of other work needed for language model safety.

For more details on our approach and results, as well as the broader consequences of our findings, read our [red teaming paper](https://arxiv.org/abs/2202.03286) here.
