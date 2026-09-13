---
title: "A Generalist Agent"
source: https://deepmind.google/blog/a-generalist-agent/
site: deepmind
date: 2022-05-12
authors: 
crawled: 2026-09-13
---

Inspired by progress in large-scale language modelling, we apply a similar approach towards building a single generalist agent beyond the realm of text outputs. The agent, which we refer to as Gato, works as a multi-modal, multi-task, multi-embodiment generalist policy. The same network with the same weights can play Atari, caption images, chat, stack blocks with a real robot arm and much more, deciding based on its context whether to output text, joint torques, button presses, or other tokens.

![A central blue icon labeled "Gato" is connected by arrows to diverse multi-modal tasks, including 3D environments, Atari games, physics simulations, chatbot dialogue, image captioning, and robotic arm control.](https://lh3.googleusercontent.com/T0NXTmIR8b3kxzy_7tmN4DgluPggtpEb6HP6Pq2pH9PvtE7wMgmkbuJQKDgIAgRlo5YiXkdkX55YMGI77kZ2aAFzgtlMm_Ov3-b9wABFatqBmfY9BA=w1440)

During the training phase of Gato, data from different tasks and modalities are serialised into a flat sequence of tokens, batched, and processed by a transformer neural network similar to a large language model. The loss is masked so that Gato only predicts action and text targets.

![Diagram illustrating how the Gato model is trained: diverse modal data (Atari, text, images, proprioception) are tokenized and sequenced into a batched input, which is processed by the Gato network to produce batched and masked shifted targets for optimization.](https://lh3.googleusercontent.com/dELldQjUlVR_3wIjXUIaSISuvbCZTDQFraNENfkvTW5TsMznAU6l_VzLrVe4QclFyp06qaWeMVDrknN0bgWYOrGMNhDMGr_RK9ZUZFi7leIS7BQP=w1440)

When deploying Gato, a prompt, such as a demonstration, is tokenised, forming the initial sequence. Next, the environment yields the first observation, which is also tokenised and appended to the sequence. Gato samples the action vector autoregressively, one token at a time.

Once all tokens comprising the action vector have been sampled (determined by the action specification of the environment), the action is decoded and sent to the environment which steps and yields a new observation. Then the procedure repeats. The model always sees all previous observations and actions within its context window of 1024 tokens.

![Diagram illustrating how the Gato model is deployed: an optional fixed prompt is tokenized followed by a sequence of observations and autoregressively sampled actions in an interactive loop with the environment.](https://lh3.googleusercontent.com/s-5aBCFsPzWWFDHiTRpBuuIDcOhyrS-HX0AxH2Jf0HmD5gheV8po4JS_YoT3iUkhKj9Ksh8X6bjw8xyY8NVGiM9h40GssG4Leo4gvQcuX2uDhtKbRQ=w1440)

Gato is trained on a large number of datasets comprising agent experience in both simulated and real-world environments, in addition to a variety of natural language and image datasets. The number of tasks, where the performance of the pretrained Gato model is above a percentage of expert score, grouped by domain, is shown here.

![Stacked area chart showing Gato's performance across various task domains, plotted by the percentage of expert score.](https://lh3.googleusercontent.com/FcRbjUl-2s-MlpygxiWSrMKZNDvo8x7MIGlelYkB6IeMItwjLJvW03xs7w3LLDh0KvWG5CioRMNBbjM8XM2g9_Kp_H5p7X8ulzWK4_csO4czvQEgPg=w1440)

The following images also show how the pre-trained Gato model with the same weights can do image captioning, engage in an interactive dialogue, and control a robot arm, among many other tasks.

![Ten images with accompanying captions to show how the pre-trained Gato model can do image captioning.](https://lh3.googleusercontent.com/m_EZIGaZ5a4nJEcmQkxXGow-KTh1iGv-VMdimwSYnVAHJimsqS5-KYW7v3qrzu78wznFAgylL5ExKAlsHh6nvuOAEy2h1vJoi024Q0PwCMy1znua=w1440)

![Chatbot dialogue showing how the pre-trained Gato model with the same weights can engage in an interactive dialogue.](https://lh3.googleusercontent.com/-4PURVjQgptdksFcPBUtyDYvlK1gvTZWm4MrAyVY04hxPFHYndT5kCh4F6hRHFAthAtCkOgqf3dsfUkiJw3FJx2eQzx4e84UUU3mpNAYKu1YHtm5QVI=w1440)

![A green cube, red trapezoid and purple 3D octagon are placed on a grey floor. The image is replicated eight times, showing a black grabber pick up and put down each object from above.](https://lh3.googleusercontent.com/Vz2LuGHS5eXOgfMil_9h03VymgRDd9yFzD3SQH76ao0Uda3Ncn8W2HYSqD6QhBG-LV0kg3VdhShvsFQhmfVJ28ZnSSNXIl4GABiaNcKwRgoMQsZdVg=w1440)
