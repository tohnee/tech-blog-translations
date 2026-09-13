---
title: "RT-2: New model translates vision and language into action"
source: https://deepmind.google/blog/rt-2-new-model-translates-vision-and-language-into-action/
site: deepmind
date: 2023-07-28
authors: Yevgen Chebotar, Tianhe Yu
crawled: 2026-09-13
---

Robotic Transformer 2 (RT-2) is a novel vision-language-action (VLA) model that learns from both web and robotics data, and translates this knowledge into generalised instructions for robotic control

High-capacity vision-language models (VLMs) are trained on web-scale datasets, making these systems remarkably good at recognising visual or language patterns and operating across different languages. But for robots to achieve a similar level of competency, they would need to collect robot data, first-hand, across every object, environment, task, and situation.

In our [paper](https://robotics-transformer2.github.io/assets/rt2.pdf), we introduce Robotic Transformer 2 (RT-2), a novel vision-language-action (VLA) model that learns from both web and robotics data, and translates this knowledge into generalised instructions for robotic control, while retaining web-scale capabilities.

![](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/64c28bb04fd16049ea01b833_64c1e428094c3322c3991c90_RT-22520gif_1.gif)

A visual-language model (VLM) pre-trained on web-scale data is learning from RT-1 robotics data to become RT-2, a visual-language-action (VLA) model that can control a robot.

This work builds upon Robotic Transformer 1 [(RT-1)](https://ai.googleblog.com/2022/12/rt-1-robotics-transformer-for-real.html), a model trained on multi-task demonstrations, which can learn combinations of tasks and objects seen in the robotic data. More specifically, our work used RT-1 robot demonstration data that was collected with 13 robots over 17 months in an office kitchen environment.

RT-2 shows improved generalisation capabilities and semantic and visual understanding beyond the robotic data it was exposed to. This includes interpreting new commands and responding to user commands by performing rudimentary reasoning, such as reasoning about object categories or high-level descriptions.

We also show that incorporating chain-of-thought reasoning allows RT-2 to perform multi-stage semantic reasoning, like deciding which object could be used as an improvised hammer (a rock), or which type of drink is best for a tired person (an energy drink).

## Adapting VLMs for robotic control

RT-2 builds upon VLMs that take one or more images as input, and produces a sequence of tokens that, conventionally, represent natural language text. Such VLMs have been [successfully trained](https://ai.googleblog.com/2022/09/pali-scaling-language-image-learning-in.html) on web-scale data to perform tasks, like visual question answering, image captioning, or object recognition. In our work, we adapt Pathways Language and Image model ([PaLI-X](https://ai.googleblog.com/2022/09/pali-scaling-language-image-learning-in.html)) and Pathways Language model Embodied ([PaLM-E](https://ai.googleblog.com/2023/03/palm-e-embodied-multimodal-language.html)) to act as the backbones of RT-2.

To control a robot, it must be trained to output actions. We address this challenge by representing actions as tokens in the model’s output – similar to language tokens – and describe actions as strings that can be processed by standard [natural language tokenizers](https://github.com/google/sentencepiece), shown here:

![A diagram showing how robot actions are represented as a string sequence of tokens, starting with "Terminate or continue", followed by three tokens for positional change (X, Y, Z), three tokens for rotational change (X, Y, Z), and a final token for the gripper state.](https://lh3.googleusercontent.com/_xUzI0LiXRXg-9C6qqFYWt5U-Dn2gUlui_lk9vaJ0lR6zqH9ijCMNfE7mFXXNcsPB85VK-Q0kcV_xylGcFzAdDL4V57jx3kMoXNYTqOO4Le_mrO7pVg=w1440)

Representation of an action string used in RT-2 training. An example of such a string could be a sequence of robot action token numbers, e.g.“1 128 91 241 5 101 127 217”.

The string starts with a flag that indicates whether to continue or terminate the current episode, without executing the subsequent commands, and follows with the commands to change position and rotation of the end-effector, as well as the desired extension of the robot gripper.

We use the same discretised version of robot actions as in RT-1, and show that converting it to a string representation makes it possible to train VLM models on robotic data – as the input and output spaces of such models don’t need to be changed.

![A diagram showing the RT-2 model training workflow, where Internet-scale VQA data and robot action data are co-fine-tuned to create a Vision-Language-Action model for robot control, which is then deployed for closed-loop robot control tasks like "Put the strawberry into the correct bowl," "Pick the nearly falling bag," and "Pick object that is different."](https://lh3.googleusercontent.com/wS51jyqW2T7T_m14tD2kn4pg86isQ1i7kusjlkQC-OktXdDgz-2iG4m_oZB8aFNmulk5ckURCxItJ1yWMVX54uU5k1WshHFKiqbhmNjlQmtgeN-O=w1440)

RT-2 architecture and training: We co-fine-tune a pre-trained VLM model on robotics and web data. The resulting model takes in robot camera images and directly predicts actions for a robot to perform.

## Generalisation and emergent skills

We performed a series of qualitative and quantitative experiments on our RT-2 models, on over 6,000 robotic trials. Exploring RT-2’s emergent capabilities, we first searched for tasks that would require combining knowledge from web-scale data and the robot’s experience, and then defined three categories of skills: symbol understanding, reasoning, and human recognition.

Each task required understanding visual-semantic concepts and the ability to perform robotic control to operate on these concepts. Commands such as “pick up the bag about to fall off the table” or “move banana to the sum of two plus one” – where the robot is asked to perform a manipulation task on objects or scenarios never seen in the robotic data – required knowledge translated from web-based data to operate.

![A grid of 15 examples showcasing the RT-2 model's emergent capabilities. Each example pairs a photograph of the robotic arm performing a task with a text box containing the natural language command, such as "pick up the bag about to fall off the table," "move banana to Germany," "move coke can to Taylor Swift," and "move banana to the sum of two plus one."](https://lh3.googleusercontent.com/bO4w5oQ6jaC03Mb4IHsBwpbLs6ZIzWE6e26qsBxVxr_C7hH1eWmzXw8XfLsazfZWOxoB_k1wtv7fX9ChE3elaKh0nrIqD-HKu3VxBGB6vcxZo4mt3w=w1440)

Examples of emergent robotic skills that are not present in the robotics data and require knowledge transfer from web pre-training.

Across all categories, we observed increased generalisation performance (more than 3x improvement) compared to previous baselines, such as previous RT-1 models and models like Visual Cortex ([VC-1](https://eai-vc.github.io/)), which were pre-trained on large visual datasets.

![A bar chart titled "Success rates of emergent skill evaluations" comparing the performance of VC1, RT-1, RT-2 with PaLM-E-12B, and RT-2 with PaLI-X-55B across three categories: "Symbol understanding," "Reasoning," and "Human recognition," alongside a "Task average." The RT-2 models significantly outperform the VC1 and RT-1 baselines, with RT-2 with PaLI-X-55B achieving the highest success rates, reaching over 80% in symbol understanding and nearly 60% on average.](https://lh3.googleusercontent.com/9R8LMhVVNeVXvOJTQTPOAq2DpBtJlruhnq2Hd40iFVdvK2W6aWLvQywhdqN6MDHE3Xc_7UlLa0eXAchDlY6f4aj9hAFWSkKhnn_OKph2DDaP5wJfnQ=w1440)

Success rates of emergent skill evaluations: our RT-2 models outperform both previous robotics transformer (RT-1) and visual pre-training (VC-1) baselines.

We also performed a series of quantitative evaluations, beginning with the original RT-1 tasks, for which we have examples in the robot data, and continued with varying degrees of previously unseen objects, backgrounds, and environments by the robot that required the robot to learn generalisation from VLM pre-training.

![Three side-by-side images depicting generalisation evaluations: the first shows "Unseen objects" (a soda can, a wrist watch, a blue towel, and a pink tool); the second shows "Unseen backgrounds" (a table covered in an autumn leaf patterned cloth with toys on it); and the third shows "Unseen environments" (various kitchen items next to a metal sink sink).](https://lh3.googleusercontent.com/bqQlrYAORkOlJ6QTVGTYBSHicJDdX2YcGXlL2mnW-5EvryaZIcBdyBJaoSyiWAs5mrcAdN3mn4E0F5OhxM-hBQhsqyGDpNpRwVDzK3asqxpTNUNt=w1440)

Examples of previously unseen environments by the robot, where RT-2 generalises to novel situations.

RT-2 retained the performance on the original tasks seen in robot data and improved performance on previously unseen scenarios by the robot, from RT-1’s 32% to 62%, showing the considerable benefit of the large-scale pre-training.

Additionally, we observed significant improvements over baselines pre-trained on visual-only tasks, such as VC-1 and Reusable Representations for Robotic Manipulation ([R3M](https://sites.google.com/corp/view/robot-r3m/)), and algorithms that use VLMs for object identification, such as Manipulation of Open-World Objects ([MOO](https://robot-moo.github.io/)).

![A bar chart comparing model performance across various evaluation scenarios: "Seen tasks", "Unseen objects", "Unseen backgrounds", "Unseen environments", and "Unseen task average". RT-2 with PaLM-E-12B and RT-2 with PaLI-X-55B consistently outperform the R3M, VC-1, RT-1, and MOO baselines in all unseen categories.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/64c28bb0a7e46157ca3edb96_64c2566864b91d6bd0590f41_Fig25206.svg)

RT-2 achieves high performance on seen in-distribution tasks and outperforms multiple baselines on out-of-distribution unseen tasks.

Evaluating our model on the open-source [Language Table](https://github.com/google-research/language-table) suite of robotic tasks, we achieved a success rate of 90% in simulation, substantially improving over the previous baselines including [BC-Z](https://sites.google.com/corp/view/bc-z/home) (72%), [RT-1](https://ai.googleblog.com/2022/12/rt-1-robotics-transformer-for-real.html) (74%), and [LAVA](https://interactive-language.github.io/) (77%).

Then we evaluated the same model in the real world (since it was trained on simulation and real data), and demonstrated its ability to generalise to novel objects, as shown below, where none of the objects except the blue cube were present in the training dataset.

![Two photographs side by side with a title saying "push the ketchup to the blue cube". The image on the left shows a robotic arm next to a wooden board with three different bottles of sauce. The image on the right shows the robotic arm pushing the ketchup towards the blue cube.](https://lh3.googleusercontent.com/TAp7v2jwkWXtS2pfu6SYW8wGL8O7oacILl-G_kRKVhBH-YAa7gOtfQgBGCJSQWy1sAQXd_uPbFCm9BMRS1fp2ax89DnVZbg8-l0Uq4FSLLnPeBM1z7Y=w1440)

RT-2 performs well on real robot Language Table tasks. None of the objects except the blue cube were present in the training data.

Inspired by [chain-of-thought prompting methods used in LLMs](https://ai.googleblog.com/2022/05/language-models-perform-reasoning-via.html), we probed our models to combine robotic control with chain-of-thought reasoning to enable learning long-horizon planning and low-level skills within a single model.

In particular, we fine-tuned a variant of RT-2 for just a few hundred gradient steps to increase its ability to use language and actions jointly. Then we augmented the data to include an additional “Plan” step, first describing the purpose of the action that the robot is about to take in natural language, followed by “Action” and the action tokens. Here we show an example of such reasoning and the robot’s resulting behaviour:

![An image showing a robot performing chain-of-thought semantic reasoning. On the left, the instruction "I need to hammer a nail, what object from the scene might be useful?" is answered with the prediction "Rocks. Action: 1 129 138 122 132 132 106 127". On the right, a sequence of three photos shows the robotic arm successfully identifying, reaching for, and picking up a rock from the table.](https://lh3.googleusercontent.com/AgfKBrhscaCWnmmzUjTpb_4MrH8wS8ITeG-srl3R3U5GVuQHwZOR22Mr5JU4eArTCmz9ijtp4JJHdPIDu9T6HAVJNXrwdSqpyzRVA8vCTTjmBjXb71w=w1440)

Chain-of-thought reasoning enables learning a self-contained model that can both plan long-horizon skill sequences and predict robot actions.

With this process, RT-2 can perform more involved commands that require reasoning about intermediate steps needed to accomplish a user instruction. Thanks to its VLM backbone, RT-2 can also plan from both image and text commands, enabling visually grounded planning, whereas current plan-and-act approaches like [SayCan](https://ai.googleblog.com/2022/08/towards-helpful-robots-grounding.html) cannot see the real world and rely entirely on language.

## Advancing robotic control

RT-2 shows that vision-language models (VLMs) can be transformed into powerful vision-language-action (VLA) models, which can directly control a robot by combining VLM pre-training with robotic data.

With two instantiations of VLAs based on PaLM-E and PaLI-X, RT-2 results in highly-improved robotic policies, and, more importantly, leads to significantly better generalisation performance and emergent capabilities, inherited from web-scale vision-language pre-training.

RT-2 is not only a simple and effective modification over existing VLM models, but also shows the promise of building a general-purpose physical robot that can reason, problem solve, and interpret information for performing a diverse range of tasks in the real-world.

[‍ Read our paper](https://robotics-transformer2.github.io/assets/rt2.pdf)[Learn more on the Keyword](https://blog.google/technology/ai/google-deepmind-rt2-robotics-vla-model/)

**Acknowledgements**

We would like to thank the co-authors of this work: Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Xi Chen, Krzysztof Choromanski, Tianli Ding, Danny Driess, Avinava Dubey, Chelsea Finn, Pete Florence, Chuyuan Fu, Montse Gonzalez Arenas, Keerthana Gopalakrishnan, Kehang Han, Karol Hausman, Alexander Herzog, Jasmine Hsu, Brian Ichter, Alex Irpan, Nikhil Joshi, Ryan Julian, Dmitry Kalashnikov, Yuheng Kuang, Isabel Leal, Lisa Lee, Tsang-Wei Edward Lee, Sergey Levine, Yao Lu, Henryk Michalewski, Igor Mordatch, Karl Pertsch, Kanishka Rao, Krista Reymann, Michael Ryoo, Grecia Salazar, Pannag Sanketi, Pierre Sermanet, Jaspiar Singh, Anikait Singh, Radu Soricut, Huong Tran, Vincent Vanhoucke, Quan Vuong, Ayzaan Wahid, Stefan Welker, Paul Wohlhart, Jialin Wu, Fei Xia, Ted Xiao, Peng Xu, Sichun Xu, Tianhe Yu and Brianna Zitkovich for their contributions to the project and Fred Alcober, Jodi Lynn Andres, Carolina Parada, Joseph Dabis, Rochelle Dela Cruz, Jessica Gomez, Gavin Gonzalez, John Guilyard, Tomas Jackson, Jie Tan, Scott Lehrer, Dee M, Utsav Malla, Sarah Nguyen, Jane Park, Emily Perez, Elio Prado, Jornell Quiambao, Clayton Tan, Jodexty Therlonge, Eleanor Tomlinson, Wenxuan Zhou, and the greater Google DeepMind team for their help and feedback.
