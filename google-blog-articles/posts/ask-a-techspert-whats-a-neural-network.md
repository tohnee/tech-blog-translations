---
title: "Ask a Techspert: What’s a neural network?"
source: https://blog.google/innovation-and-ai/technology/ai/ask-a-techspert-whats-a-neural-network/
site: google-blog
date: 2021-07-07
authors: Aryn Sanderson
crawled: 2026-09-13
---

Back in the day, there was a surefire way to tell humans and computers apart: You’d present a picture of a four-legged friend and ask if it was a cat or dog. A computer couldn’t identify felines from canines, but we humans could answer with doggone confidence.

That all changed about a decade ago thanks to leaps in computer vision and machine learning – specifically,  major advancements in neural networks, which can train computers to learn in a way similar to humans. Today, if you give a computer enough images of cats and dogs and label which is which, it can learn to tell them apart purr-fectly.

But how exactly do neural networks help computers do this? And what else can — or can’t — they do? To answer these questions and more, I sat down with Google Research’s [Maithra Raghu](https://research.google/people/105562/), a research scientist who spends her days helping computer scientists better understand neural networks. Her research helped the Google Health team discover [new ways](https://ai.googleblog.com/2019/12/understanding-transfer-learning-for.html) to apply deep learning to assist doctors and their patients.

**So, the big question: What’s a neural network?**

To understand neural networks, we need to first go back to the basics and understand how they fit into the bigger picture of artificial intelligence (AI). Imagine a Russian nesting doll, Maithra explains. AI would be the largest doll, then within that, there’s machine learning (ML), and within that, neural networks (... and within that, deep neural networks, but we’ll get there soon!).

If you think of AI as the science of making things smart, ML is the subfield of AI focused on making computers smarter by teaching them to learn, instead of hard-coding them. Within that, neural networks are an advanced technique for ML, where you teach computers to learn with algorithms that take inspiration from the human brain.

Your brain fires off groups of neurons that communicate with each other. In an artificial neural network, (the computer type), a “neuron” (which you can think of as a computational unit) is grouped with a bunch of other “neurons” into a layer, and those layers  stack on top of each other. Between each of those layers are connections. The more layers  a neural network has, the “deeper” it is. That’s where the idea of “deep learning” comes from. “Neural networks depart from neuroscience because you have a mathematical element to it,” Maithra explains, “Connections between neurons are numerical values represented by matrices, and training the neural network uses gradient-based algorithms.”

This might seem complex, but you probably interact with neural networks fairly often — like when you’re scrolling through personalized movie recommendations or chatting with a customer service bot.

**So once you’ve set up a neural network, is it ready to go?**

Not quite. The next step is training. That’s where the model becomes much more sophisticated. Similar to people, neural networks learn from feedback. If you go back to the cat and dog example, your neural network would look at pictures and start by randomly guessing. You’d label the training data (for example, telling the computer if each picture features a cat or dog), and those labels would provide feedback, telling the neural network when it’s right or wrong. Throughout this process, the neural network’s parameters adjust, and the neural network transitions from not knowing to learning how to identify between cats and dogs.

**Why don’t we use neural networks all the time?**

“Though neural networks are based on our brains, the way they learn is actually very different from humans,” Maithra says. “Neural networks are usually quite specialized and narrow. This can be useful because, for example, it means a neural network might be able to process medical scans much quicker than a doctor, or spot patterns  a trained expert might not even notice.”

But because neural networks learn differently from people, there's still a lot that computer scientists don’t know about how they work. Let’s go back to cats versus dogs: If your neural network gives you all the right answers, you might think it’s behaving as intended. But Maithra cautions that neural networks can work in mysterious ways.

“Perhaps your neural network isn’t able to identify between cats and dogs at all – maybe it’s only able to identify between sofas and grass, and all of your pictures of cats happen to be on couches, and all your pictures of dogs are in parks,” she says. “Then, it might seem like it knows the difference when it actually doesn’t.”

That’s why Maithra and other researchers are diving into the internals of neural networks, going deep into their layers and connections, to better understand them – and come up with ways to make them more helpful.

“Neural networks have been transformative for so many industries,” Maithra says, “and I’m excited that we’re going to realize even more profound applications for them moving forward.”
