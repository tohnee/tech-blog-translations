---
title: "WaveNet launches in the Google Assistant"
source: https://deepmind.google/blog/wavenet-launches-in-the-google-assistant/
site: deepmind
date: 2017-10-04
authors: Aäron van den Oord, Tom Walters
crawled: 2026-09-13
---

**Just over a year ago we presented** [WaveNet](https://deepmind.com/blog/article/wavenet-generative-model-raw-audio), a new deep neural network for generating raw audio waveforms that is capable of producing better and more realistic-sounding speech than existing techniques. At that time, the model was a research prototype and was too computationally intensive to work in consumer products.

But over the last 12 months we have worked hard to significantly improve both the speed and quality of our model and today we are proud to announce that an updated version of WaveNet is being used to generate the [Google Assistant](https://www.blog.google/products/assistant/google-assistant-powering-our-new-family-hardware/) voices for US English and Japanese across all platforms.

Using the new WaveNet model results in a range of more natural sounding voices for the Assistant.

## US English voice I

Your browser does not support the audio element. Your browser does not support the audio element.

## US English voice II

Your browser does not support the audio element. Your browser does not support the audio element.

## US English third party voice

Your browser does not support the audio element. Your browser does not support the audio element.

## Japanese voice

Your browser does not support the audio element. Your browser does not support the audio element.

To understand why WaveNet improves on the current state of the art, it is useful to understand how text-to-speech (TTS) - or [speech synthesis](https://en.wikipedia.org/wiki/Speech_synthesis) - systems work today.

The majority of these are based on so-called [concatenative TTS](https://scholar.google.com/citations?view_op=view_citation&hl=en&user=Es-YRKMAAAAJ&citation_for_view=Es-YRKMAAAAJ:u5HHmVD_uO8C), which uses a large database of high-quality recordings, collected from a single voice actor over many hours. These recordings are split into tiny chunks that can then be combined - or concatenated - to form complete utterances as needed. However, these systems can result in unnatural sounding voices and are also difficult to modify because a whole new database needs to be recorded each time a set of changes, such as new emotions or intonations, are needed.

To overcome some of these problems, an alternative model known as [parametric TTS](https://scholar.google.com/citations?view_op=view_citation&hl=en&user=z3IRvDwAAAAJ&citation_for_view=z3IRvDwAAAAJ:d1gkVwhDpl0C) is sometimes used. This does away with the need for concatenating sounds by using a series of rules and parameters about grammar and mouth movements to guide a computer-generated voice. Although cheaper and quicker, this method creates less natural sounding voices.

WaveNet takes a totally different approach. In the [original paper](https://arxiv.org/pdf/1609.03499.pdf) we described a deep generative model that can create individual waveforms from scratch, one sample at a time, with 16,000 samples per second and seamless transitions between individual sounds.

![Diagram showing the layers of the WaveNet convolutional neural network, with an input layer of blue nodes at the bottom, three hidden layers of grey nodes in the middle, and an output layer of orange nodes at the top.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62227b1d1dd26da452c9e160_unnamed-2.gif)

The structure of the convolutional neural network that underpins the original WaveNet model

It was built using a [convolutional neural network](https://en.wikipedia.org/wiki/Convolutional_neural_network), which was trained on a large dataset of speech samples. During this training phase, the network determined the underlying structure of the speech, such as which tones followed each other and what waveforms were realistic (and which were not). The trained network then synthesised a voice one sample at a time, with each generated sample taking into account the properties of the previous sample. The resulting voice contained natural intonation and other features such as lip smacks. Its “accent” depended on the voices it had trained on, opening up the possibility of creating any number of unique voices from blended datasets. As with all text-to-speech systems, WaveNet used a text input to tell it which words it should generate in response to a query.

Building up sound waves at such high-fidelity using the original model was computationally expensive, meaning WaveNet showed promise but was not something we could deploy in the real world. But over the last 12 months our teams have worked hard to develop a new model that is capable of more quickly generating waveforms. It is also now capable of running at scale and is the first product to launch on [Google’s latest TPU cloud infrastructure](https://www.blog.google/products/google-cloud/google-cloud-offer-tpus-machine-learning/).

![](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62266baf02e48255b587a17f_WaveNet20generation.gif)

The WaveNet team will now turn their focus to preparing a publication detailing the research behind the new model, but the results speak for themselves. The new, improved WaveNet model still generates a raw waveform but at speeds 1,000 times faster than the original model, meaning it requires just 50 milliseconds to create one second of speech. In fact, the model is not just quicker, but also higher-fidelity, capable of creating waveforms with 24,000 samples a second. We have also increased the resolution of each sample from 8 bits to 16 bits, the same resolution used in compact discs.

This makes the new model more natural sounding according to tests with human listeners. For example, the new US English voice I gets a mean-opinion-score (MOS) of 4.347 on a scale of 1-5, where even human speech is rated at just 4.667.

![A bar chart titled "Mean Opinion Scores" comparing "Current Best Non-WaveNet" to "WaveNet" across four voices: US English Voice I (4.186 vs. 4.347; trained on 65 hours), US English Voice II (4.089 vs. 4.314; trained on 21 hours), US English 3rd Party Voice (3.418 vs. 3.966; trained on 9 hours), and Japanese Voice (4.072 vs. 4.236; trained on 28 hours). In all four cases, WaveNet achieves a higher score.](https://lh3.googleusercontent.com/oB2ZUCuvqvFUORBXOxhcMVE9AtTFmFBby2uQlvDb7sFhLjocuzKM3-KZe5USOyElZvnpLEyRxrTaYfAkqZekKs_8H8OtB-K8JXJLOmfNUzDF-sy-ow=w1440)

The new model also retains the flexibility of the original WaveNet, allowing us to make better use of large amounts of data during the training phase. Specifically, we can train the network using data from multiple voices. This can then be used to generate high-quality, nuanced voices even where there is little training data available for the desired output voice.

We believe this is just the start for WaveNet and we are excited by the possibilities that the power of a voice interface could now unlock for all the world's languages.

**Notes**

**This work was done by the DeepMind WaveNet research and engineering teams and the Google Text-to-Speech team.**

Read the [original WaveNet blog post](https://deepmind.com/blog/wavenet-generative-model-raw-audio/).

Read the original [WaveNet paper.](https://arxiv.org/pdf/1609.03499.pdf)

Read more about [the updated Google Assistant](https://www.blog.google/products/assistant/google-assistant-powering-our-new-family-hardware/).

**Update:** An earlier version of this blog incorrectly put the MOS score for the US English 3rd Party Voice as 4.326. This has now been corrected.
