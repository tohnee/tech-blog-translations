---
title: "High-fidelity speech synthesis with WaveNet"
source: https://deepmind.google/blog/high-fidelity-speech-synthesis-with-wavenet/
site: deepmind
date: 2017-11-22
authors: Aäron van den Oord, Yazhe Li, Igor Babuschkin
crawled: 2026-09-13
---

In October we announced that our state-of-the-art speech synthesis model [WaveNet](https://deepmind.com/blog/article/wavenet-generative-model-raw-audio) was being used to generate realistic-sounding voices for the [Google Assistant](https://deepmind.com/blog/article/wavenet-launches-google-assistant) globally in Japanese and the US English. This production model - known as parallel WaveNet - is more than 1000 times faster than the [original](https://deepmind.com/blog/article/wavenet-generative-model-raw-audio) and also capable of creating higher quality audio.

Our [latest paper](https://arxiv.org/abs/1711.10433) introduces details of the new model and the “probability density distillation” technique we developed to allow the system to work in a massively parallel computing environment.

The original WaveNet model used autoregressive connections to synthesise the waveform one sample at a time, with each new sample conditioned on the previous samples. While this produces high-quality audio with up to 24,000 samples per second, this sequential generation is too slow for production environments.

![Diagram showing parallel neural network generation, with input nodes at the bottom connecting through hidden layers directly to output nodes at the top.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62227b1d1dd26da452c9e160_unnamed-2.gif)

The original model synthesises one sample at a time with each sample conditioned on previous ones

To get around this we needed a solution that could generate long sequences of samples all at once and with no loss of quality. Our solution is called probability density distillation, where we used a fully-trained WaveNet model to teach a second, “student” network that is both smaller and more parallel and therefore better suited to modern computational hardware. This student network is a smaller dilated [convolutional neural network](https://en.wikipedia.org/wiki/Convolutional_neural_network), similar to the original WaveNet. But, crucially, generation of each sample does not depend on any of the previously generated samples, meaning we can generate the first and last word - and everything in between - at the same time, as shown in the animation below.

![An animation of a parallel neural network generating all output nodes at the same time directly from the input nodes.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/622670e8b58caa5fe7d80033_New20Model.gif)

The new WaveNet model uses white noise as an input and synthesises all of the output samples in parallel

During training, the student network starts off in a random state. It is fed random white noise as an input and is tasked with producing a continuous audio waveform as output. The generated waveform is then fed to the trained WaveNet model, which scores each sample, giving the student a signal to understand how far away it is from the teacher network’s desired output. Over time, the student network can be tuned - via backpropagation - to learn what sounds it should produce. Put another way, both the teacher and the student output a probability distribution for the value of each audio sample, and the goal of the training is to minimise the [KL divergence](https://en.wikipedia.org/wiki/Kullback%E2%80%93Leibler_divergence) between the teacher’s distribution and the student’s distribution.

The training method has parallels to the set-up for generative adversarial networks (GANs), with the student playing the role of generator and the teacher as the discriminator. However, unlike GANs, the student’s aim is not to “fool” the teacher but to cooperate and try to match the teacher’s performance.

Although the training technique works well, we also need to add a few extra loss functions to guide the student towards the desired behaviour. Specifically, we add a [perceptual loss](https://arxiv.org/abs/1508.06576) to avoid bad pronunciations, a contrastive loss to further reduce the noise, and a power loss to help match the energy of the human speech. Without the latter, for example, the trained model whispers rather than speaking out loud.

Adding all of these together allowed us to train the parallel WaveNet to achieve the same quality of speech as the original WaveNet, as shown by the mean opinion scores (MOS) - a scale of 1-5 that measures of how natural sounding the speech is according to tests with human listeners. Note that even human speech is rated at just 4.667 on the MOS scale.

![Table showing Mean Opinion Scores (MOS): Current best non-WaveNet (4.19 ± 0.10), Autoregressive WaveNet (4.41 ± 0.07), and Parallel WaveNet (4.41 ± 0.08).](https://lh3.googleusercontent.com/qWug513KsBO4ONSYx8AOkr5P1Mpej02DOBSPuA3VKRYUr8gb1Wx4IU0e2ZPXzzCtbM9v7FnOGg1vu4J2AJfPVlSl9gplVBebh0P29ORCge5ShXxa=w1440)

Of course, the development of probability density distillation was just one of the steps needed to allow WaveNet to meet the speed and quality requirements of a production system. Incorporating parallel WaveNet into the serving pipeline of the Google Assistant required an equally significant engineering effort by the DeepMind Applied and Google Speech teams. It was only by working together that we could move from fundamental research to Google-scale product in a little over 12 months.

**Notes**

Read the [new paper](https://arxiv.org/abs/1711.10433).

Read more about [WaveNet in the Google Assistant](https://deepmind.com/blog/article/wavenet-launches-google-assistant).

Read the [original WaveNet blog post](https://deepmind.com/blog/article/wavenet-generative-model-raw-audio).

Read the original [WaveNet paper.](https://arxiv.org/pdf/1609.03499.pdf)

This work was done by Aaron van den Oord, Yazhe Li, Igor Babuschkin, Karen Simonyan, Oriol Vinyals, Koray Kavukcuoglu, George van den Driessche, Edward Lockhart, Luis C. Cobo, Florian Stimberg, Norman Casagrande, Dominik Grewe, Seb Noury, Sander Dieleman, Erich Elsen, Nal Kalchbrenner, Heiga Zen, Alex Graves, Helen King, Tom Walters, Dan Belov and Demis Hassabis.
