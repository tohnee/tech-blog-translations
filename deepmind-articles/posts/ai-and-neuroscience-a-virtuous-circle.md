---
title: "AI and Neuroscience: A virtuous circle"
source: https://deepmind.google/blog/ai-and-neuroscience-a-virtuous-circle/
site: deepmind
date: 2017-08-02
authors: Demis Hassabis, Christopher Summerfield, Matt Botvinick
crawled: 2026-09-13
---

Recent progress in AI has been remarkable. Artificial systems now outperform expert humans at [Atari video games](https://deepmind.com/research/publications/human-level-control-through-deep-reinforcement-learning/), the [ancient board game Go](https://deepmind.com/research/case-studies/alphago-the-story-so-far), and [high-stakes matches of heads-up poker](http://science.sciencemag.org/content/356/6337/508). They can also produce [handwriting](https://web.mit.edu/cocosci/Papers/Science-2015-Lake-1332-8.pdf) and [speech](https://deepmind.com/blog/article/wavenet-generative-model-raw-audio) indistinguishable from those of humans, translate between multiple languages and even reformat your holiday snaps [in the style of Van Gogh](https://deepart.io/) masterpieces.

These advances are attributed to several factors, including the application of new statistical approaches and the increased processing power of computers. But in [a recent Perspective in the journal Neuron](https://www.cell.com/neuron/fulltext/S0896-6273(17)30509-3), we argue that one often overlooked contribution is the use of ideas from experimental and theoretical neuroscience.

Psychology and neuroscience have played a key role in the history of AI. Founding figures such as [Donald Hebb](https://en.wikipedia.org/wiki/Donald_O._Hebb), [Warren McCulloch](https://en.wikipedia.org/wiki/Warren_Sturgis_McCulloch), [Marvin Minsky](https://en.wikipedia.org/wiki/Marvin_Minsky) and [Geoff Hinton](https://en.wikipedia.org/wiki/Geoffrey_Hinton) were all originally motivated by a desire to understand how the brain works. In fact, throughout the late 20th Century, much of the key work developing neural networks took place not in mathematics or physics labs, but in psychology and neurophysiology departments.

> With so much at stake, the need for the field of neuroscience and AI to come together is now more urgent than ever before.

At DeepMind, we argue that despite rapid progress in both fields, researchers should not lose sight of this vision. We urge researchers in neuroscience and AI to find a common language, allowing a free flow of knowledge that will allow continued progress on both fronts.

We believe that drawing inspiration from neuroscience in AI research is important for two reasons. First, neuroscience can help validate AI techniques that already exist. Put simply, if we discover one of our artificial algorithms mimics a function within the brain, it suggests our approach may be on the right track. Second, neuroscience can provide a rich source of inspiration for new types of algorithms and architectures to employ when building artificial brains. Traditional approaches to AI have historically been dominated by logic-based methods and theoretical mathematical models. We argue that neuroscience can complement these by identifying classes of biological computation that may be critical to cognitive function.

Take one recent example of a seminal finding in neuroscience: the discovery of offline experience “[replay](http://www.sciencedirect.com/science/article/pii/S0166223610000172?via%3Dihub)”. During sleep or quiet resting, biological brains “replay” temporal patterns of neuronal activity that were produced in an earlier active period. For example, when rats run through a maze, “place” cells activate as the animal moves around. During rest, the same sequence of neuronal activity is observed, as if the rats were mentally reimagining their past movements, and using them to optimise future behaviour. In fact, it has been shown that interfering with replay impairs performance when they later perform the same tasks.

![Abstract retro video game sprites and blocks rendered as glowing 3D outlines floating over a digital grid.](https://lh3.googleusercontent.com/XRaO1hKI_b8279Tiv59-FHGq_dNESFSL51Zu3l6x4By_LmupaIAgaAE0z14Nv_sh66q1eQM8z2_xFyx5Z85_P0B5ZbW5W8wH6ke8lEs4anX8AzUMvZg=w1440)

'Replay' was a key element of DQN, a general-purpose agent that is able to continually adapt its behaviour to new environments

At first glance, it might seem counterintuitive to build an artificial agent that needs to ‘sleep’ - after all, they are supposed to grind away at a computational problem long after their programmers have gone to bed. But this principle was a key part of our [deep-Q network (DQN)](https://deepmind.com/research/publications/human-level-control-through-deep-reinforcement-learning/), an algorithm that learnt to master a diverse range of Atari 2600 games to superhuman level with only the raw pixels and score as inputs. DQN mimics “experience replay”, by storing a subset of training data that it reviews “offline”, allowing it to learn anew from successes or failures that occurred in the past.

Successes like this give us confidence that neuroscience is already an important source of ideas for AI. But looking forward, we believe it will become indispensable in helping us tackle unsolved questions, such as those concerning efficient learning, understanding of the physical world, and imagination.

[Imagination](https://www.ncbi.nlm.nih.gov/pubmed/19528007) is a hugely important function for humans and animals, allowing us to plan for future scenarios without taking action; something that may come at a cost. Consider a simple example, such as planning a holiday. In order to do this we leverage our knowledge - or “model” - of the world and use it to project forward in time, evaluating future states, and allowing us to calculate the route we need to take or what clothes to pack for sunny weather. Cutting-edge research in human neuroscience is starting to unveil the computational and systems mechanisms that underpin this kind of thinking, but much of this new understanding has yet to be incorporated into artificial models.

![An illustration of a tree shaped like a human brain, where the left side is composed of digital pixels and circuits, and the right side is made of organic branches and green leaves, representing the connection between artificial intelligence and neuroscience.](https://lh3.googleusercontent.com/wtrBw4LC9a7fk2XgAoX0GZ5-YVljIOjfMEx0i_5YuuXLcyQZZ2FetVzwpemxKYARg3Vh2YDpni3UXEOvdcg7rP_100GxWvTFOFzmrzZMicIAi67hmg=w1440)

The fields of neuroscience and artificial intelligence have a long and intertwined history

Another key challenge in contemporary AI research is known as transfer learning. To be able to deal effectively with novel situations, artificial agents need the ability to build on existing knowledge to make sensible decisions. Humans are already good at this - an individual who can drive a car, use a laptop or chair a meeting are usually able to cope even when confronted by an unfamiliar vehicle, operating system or social situation.

Researchers are now starting to take the first steps towards understanding how this might be possible in artificial systems. For example, a new class of network architecture known as a “[progressive network](https://arxiv.org/abs/1606.04671)” can use knowledge learned in one video game to learn another. The same architecture has also been shown to transfer knowledge from a simulated robotic arm to a real-world arm, massively reducing the training time. Intriguingly, these networks bear some similarities to [models of sequential task learning in humans](http://science.sciencemag.org/content/344/6191/1481.long). These tantalising links suggest that there are great opportunities for future AI research to learn from work in neuroscience.

But this exchange of knowledge cannot be a one-way street. Neuroscience can also benefit from AI research. Take the idea of reinforcement learning - one of the central approaches in contemporary AI research. Although the original idea came from theories of animal learning in psychology, it was developed and elaborated by machine learning researchers. These later ideas fed back into neuroscience to help us understand neurophysiological phenomena, such as the [firing properties of dopamine neurons](http://science.sciencemag.org/content/275/5306/1593.long) in the mammalian basal ganglia.

This back and forth is essential if both fields are to continue to build on each other’s insights, creating a virtuous circle whereby AI researchers use ideas from neuroscience to build new technology, and neuroscientists learn from the behaviour of artificial agents to better interpret biological brains. Indeed, this cycle will likely accelerate thanks to recent advances, such as optogenetics, that allow us to precisely measure and manipulate brain activity, yielding vast quantities of data that can be analysed with tools from machine learning.

We therefore believe distilling intelligence into algorithms and comparing them to the human brain is now vital. Not only could it bolster our quest to develop AI, a tool that we hope will [create new knowledge and push forward scientific discovery](https://www.ft.com/content/048f418c-2487-11e7-a34a-538b4cb30025), but may also allow us to better understand what’s going on inside our own heads. That could shed light on some of the most enduring mysteries in neuroscience, such as the nature of creativity, dreams and, perhaps one day, even consciousness. With so much at stake, the need for the field of neuroscience and AI to come together is now more urgent than ever before.

**Notes**

Read paper: [Neuroscience-Inspired Artificial Intelligence](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/ai-and-neuroscience-a-virtuous-circle/Neuron.pdf)
