---
title: "Gemini Robotics 2 brings whole body intelligence to robots"
source: https://deepmind.google/blog/gemini-robotics-2-brings-whole-body-intelligence-to-robots/
site: deepmind
date: 2026-07-30
authors: Carolina Parada
crawled: 2026-09-13
---

From feet to fingertips — we are teaching robots intelligent whole-body control, fine dexterity, and teamwork to complete a broad range of complex tasks

For decades, we’ve dreamed of robots that can seamlessly step into our world and lend a hand. Now, that vision takes a significant stride forward.

Most robots are pre-programmed or teleoperated for narrow, repetitive task sequences. They lack the ability to truly learn for themselves or adapt to unpredictable environments. Moreover, transferring learned skills from one robot body to another remains incredibly difficult. To take on the hardest problems at scale, robots of every shape and size need AI models giving them the ability to think, act, and interact intelligently to safely complete tasks.

We demonstrated how Gemini's multimodal understanding could drive real-world action with [Gemini Robotics](https://deepmind.google/models/gemini-robotics/). Today, we are introducing Gemini Robotics 2 - the intelligence layer powering the next generation of truly adaptable robots. As it takes its first literal steps, this major advance unlocks intelligent whole-body control, advanced dexterity, and multi-robot collaboration.

Gemini Robotics 2 enables robots to reason through every movement, unlocking a broad range of tasks. For example, it can enable a humanoid to walk, crouch, stretch, and manipulate objects to clean up a cluttered room. It can even team up with other robots to finish the job faster. And this profound intelligence can also run locally on-device while seamlessly adapting to entirely new robotic bodies in just a few hours.

We are making this possible through three highly capable models:

- [Gemini Robotics 2](https://deepmind.google/models/gemini-robotics/vla/): Our most advanced vision-language-action model (VLA) that converts vision and language input into motor control, enabling a robot to take action. This model is capable of controlling full humanoids, from feet to fingertips, and other bi-arm robots. It also brings a new level of dexterous manipulation on both hands and grippers.
- [Gemini Robotics ER 2](https://deepmind.google/models/gemini-robotics/embodied-reasoning/): Our most capable embodied reasoning (ER) model. It is a vision language model (VLM) that acts as our agent, enabling robots to communicate with humans, understand the physical world and plan multi-step tasks lasting several minutes. We are also introducing the ability for robots to work together as a team.
- [Gemini Robotics On-Device 2](https://deepmind.google/models/gemini-robotics/on-device/): Our most efficient vision-language-action model (VLA) optimized to run locally on robotic devices. This model can now achieve fast adaptation to completely new robot embodiments with a few hours of data.

Slide 1 of 3

![A bar chart titled "General whole body manipulation" with subtitle "Apollo with Inspire hands" displaying accuracy percentages with error bars across three tasks: "Pick up from table" at 68.4%, "Pick up from floor" at 45.7%, and "Pick up from shelf" at 76.3%.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/MVCfTE-4h3AwDVPZ/gemini-robotics-2__general-whole-body-manipulation__light.svg)![A bar chart titled "General whole body manipulation" with subtitle "Apollo with Inspire hands" displaying accuracy percentages with error bars across three tasks: "Pick up from table" at 68.4%, "Pick up from floor" at 45.7%, and "Pick up from shelf" at 76.3%.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/MVCfTE-4h3AwDVPZ/gemini-robotics-2__general-whole-body-manipulation__dark.svg)

Gemini Robotics 2 controlling three different embodiments, using the same model checkpoint — the Apptronik Apollo 2 robot with SharpaWave hands, the Apollo 2 robot with Inspire hands, and the Franka Duo with the Robotiq gripper — on a wide variety of whole-body and dexterous manipulation tasks. Each bar represents the average success rate over multiple tasks within the same skill category. For multifinger tasks we show individual task performance. While Gemini Robotics 2 achieves a medium to high success rate for whole-body and gripper-based dexterous tasks, the multi-finger dexterous manipulation remains challenging.

![A bar chart titled "Multi-finger dexterity" with subtitle "Apollo with Sharpa hands" displaying accuracy percentages with error bars across five tasks: "Screw bulb" at 36%, "Unscrew bulb" at 92%, "Tie trash bag" at 44%, "Dustpan" at 32%, and "Ziplock" at 40%.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/MVCfTE-4h3AwDVPZ/gemini-robotics-2__multi-finger-dexterity__light.svg)![A bar chart titled "Multi-finger dexterity" with subtitle "Apollo with Sharpa hands" displaying accuracy percentages with error bars across five tasks: "Screw bulb" at 36%, "Unscrew bulb" at 92%, "Tie trash bag" at 44%, "Dustpan" at 32%, and "Ziplock" at 40%.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/MVCfTE-4h3AwDVPZ/gemini-robotics-2__multi-finger-dexterity__dark.svg)

![A bar chart titled "Gripper dexterity" with subtitle "Franka Duo" displaying accuracy percentages with error bars across three tasks: "General pick and place" at 74.2%, "Diverse tool kitting" at 78.9%, and "Precise insertion tasks" at 89.6%.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/MVCfTE-4h3AwDVPZ/gemini-robotics-2__gripper-dexterity__light.svg)![A bar chart titled "Gripper dexterity" with subtitle "Franka Duo" displaying accuracy percentages with error bars across three tasks: "General pick and place" at 74.2%, "Diverse tool kitting" at 78.9%, and "Precise insertion tasks" at 89.6%.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/MVCfTE-4h3AwDVPZ/gemini-robotics-2__gripper-dexterity__dark.svg)

Gemini Robotics ER 2, our reasoning model, is now available on [Google AI Studio](https://ai.dev/prompts/new_chat?model=gemini-robotics-er-2-preview) and in private preview on [Gemini Enterprise Agent Platform](https://console.cloud.google.com/agent-platform/publishers/google/model-garden/gemini-robotics-er-2-preview-info). Our VLA and On-Device models are available to [early-access partners](https://docs.google.com/forms/d/1sM5GqcVMWv-KmKY3TOMpVtQ-lDFeAftQ-d9xQn92jCE/viewform?ts=67cef986&edit_requested=true). Read how to bring these models to your hardware on our [Developer blog](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/gemini-robotics-er-2/).

## Humanoids in motion: Managing whole-body tasks

The world is built for human movements; it requires us to reach, bend, and balance in tight, cluttered spaces. While our previous models controlled the humanoid’s upper-body to achieve table-top tasks, Gemini Robotics 2 expands physical AI into whole-body motions.

For the first time, our model can now control entire humanoid robots, translating intent into intelligent whole-body control. For example, when controlling [Apptronik’s Apollo 2](https://apptronik.com/apollo/apollo-2) humanoid robot, we can ask it to *“put the watering can into the green bin in the bottom shelf.*” Apollo processes the instruction, walks to the table, and picks up the watering can, takes a few steps to the shelves, and places it precisely in its destination. While our robots have more to advance in movement speed, this is an important step towards the skills needed to complete more complex, real-world tasks that require whole-body coordination.

[ Your browser does not support the video tag.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/MVCfTE-4h3AwDVPZ/GR2_Wholebody_posterframe_v01.webm)

## Bringing advanced dexterity to hands and grippers

To be genuinely useful in our homes and workplaces, robots need finesse. Gemini Robotics 2 unlocks a new level of physical dexterity across different end effectors, whether a robot is using hands or grippers, enabling robots to be more useful than ever before.

The model can now control the five-fingered, 22 degree-of-freedom SharpaWave hand on the Apollo 2 robot to complete delicate actions like tying knots or sealing a ziplock bag. It can also operate standard two-fingered parallel grippers on a [Franka Duo platform](https://franka.de/fr3-duo) to perform complex dexterous tasks (e.g. tight packing). We are continuing to advance the level of precision and speed to achieve human-level dexterity.

[ Your browser does not support the video tag.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/MVCfTE-4h3AwDVPZ/GR2_Dexterity_posterframe_v01.webm)

## Unlocking advanced tasks with agentic reasoning and multi-robot collaboration

Most real-world tasks require multiple steps over an extended period of time. To manage this complexity, our embodied reasoning (ER) model, Gemini Robotics ER 2, serves as the robot’s high-level brain, processing user instructions and communicating with humans. It observes the room, reasons about the steps needed to complete the task, coordinates with the VLA to carry out the actions, and tracks progress until the task is done. This setup allows robots to execute complex multi-step tasks, self-correct if a step fails, and generalize to novel situations and goals.

In this update, we are enabling robots to more reliably execute longer task sequences, lasting several minutes and involving hundreds of decisions. Gemini Robotics ER 2 now understands when tasks begin and end, and can pinpoint the moment key events occur, marking a step change in progress understanding.

Furthermore, we are introducing multi-robot collaboration. This enables different types of robots to communicate and work together to solve complex workflows a single robot could not do alone.

[ Your browser does not support the video tag.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/MVCfTE-4h3AwDVPZ/GR2_MultiRobot_posterframe_v04.webm)

## Adapting fast on-device models for any robot

Many robotic applications need to operate without network latency or internet connectivity. Gemini Robotics On-Device 2 is built specifically to handle these constraints — it is our most-efficient vision-language-action model (VLA) optimized to run locally on robotic devices.

This model is natively multi-embodiment and inherits our advanced “motion transfer” techniques from [Gemini Robotics 1.5](https://deepmind.google/blog/gemini-robotics-15-brings-ai-agents-into-the-physical-world/). We can now adapt to new bi-arm robot embodiments with just a few hours of adaptation time, typically with less than 200 examples. This works even with new embodiments with drastically different shapes, sensors and degrees of freedom, as shown below with a diverse set of tasks being performed by the Dexmate, SO101, and Trossen platforms.

![](https://lh3.googleusercontent.com/-CSJxggUnu5m5TfompiXP2z7YLThhUvDn2-kBueCZv6HCEWWefUt_WLzM6wxnTV1sTGqBbvmXDnOTB12W18NDr2NgFVXvHKCiTtjfXpyzuOYPJZXlg=w1440-h810-n-nu)

![ Your browser does not support the video tag.](https://lh3.googleusercontent.com/-CSJxggUnu5m5TfompiXP2z7YLThhUvDn2-kBueCZv6HCEWWefUt_WLzM6wxnTV1sTGqBbvmXDnOTB12W18NDr2NgFVXvHKCiTtjfXpyzuOYPJZXlg)

## Advancing our commitment to safe and responsible robotics

Safety is foundational to our robotics research. As robots gain more physical capabilities, we are committed to ensuring end-to-end safety and alignment. With each release, we’ve taken a multi-layered approach that combines traditional physical safety measures with robust AI safety frameworks.

Gemini Robotics 2 specifically advances robotics safety for navigating the uncertainty of the real world and collaborating alongside humans.

We’re introducing [ASIMOV-Agentic](https://huggingface.co/datasets/google/asimov_agentic/blob/main/README.md), a new benchmark for agentic safety orchestration and uncertainty resolution. For example, it measures the embodied reasoning agent’s ability to refuse unsafe tool calls from a VLA.It also measures the agent’s ability to predict whether a task is possible and to proactively request human intervention when uncertain.

Additionally, with enhanced embodied reasoning, Gemini Robotics ER 2 is our safest robotics model to date in safety constraint following and human proximity benchmarks. It can better detect when humans are nearby, trigger safety tool calls and bring the robot to a safe stop if someone approaches too closely. This is a key requirement in collaborative safety standards. Read our [Gemini Robotics 2: Safety Technical Report](https://storage.googleapis.com/deepmind-media/gemini-robotics/Gemini-Robotics-2-Safety.pdf) for more details.

## Building towards general-purpose physical AI

Gemini Robotics 2 marks an important milestone on the path toward solving AGI in the physical world. Unlocking the true potential of robotics requires moving past single-task automation toward general-purpose intelligence. By building this core intelligence, our goal is to enable AI in the physical world that can work alongside humans to solve complex challenges.

**Explore Gemini Robotics 2**

[Try in Google AI Studio](https://ai.dev/prompts/new_chat?model=gemini-robotics-er-2-preview)[View Gemini Robotics ER 2 Model Card](https://deepmind.google/models/model-cards/gemini-robotics-er-2/)[View Gemini Robotics On-Device 2 Model Card](https://deepmind.google/models/model-cards/gemini-robotics-on-device-2/)[Learn more on the Developer blog](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/gemini-robotics-er-2/)[Sign up for our Trusted Tester Program](https://docs.google.com/forms/d/1sM5GqcVMWv-KmKY3TOMpVtQ-lDFeAftQ-d9xQn92jCE/viewform?ts=67cef986&edit_requested=true)[Try in Gemini Enterprise Agent Platform (Private Preview)](https://console.cloud.google.com/agent-platform/publishers/google/model-garden/gemini-robotics-er-2-preview-info)

**Acknowledgements**
This work was developed by the Gemini Robotics team: Abhijit Ogale, Abhishek Jindal, Adil Dostmohamed, Adrian Collister, Alan Thompson, Alessio Quaglino, Alex Bewley, Alex Hofer, Alex Taeho Kim, Alex X. Lee, Alex Zihao Zhu, Allen Chai, Amaris Paryag, Amit Hampaul, Amy Nommeots-Nomm, Amy Shen, Andre Araujo, Andrew Gallagher, Anirudha Majumdar, Anna Volosina, Annie S. Chen, Annie Xie, Anthony Brohan, Antoine Laurens, Arunkumar Byravan, Asaf Revach, Assaf Hurwitz Michaely, Baruch Tabanpour, Ben Moran, Benoit Landry, Bingyi Cao, Bogdan Mazoure, Brandon Hernaez, Brijen Thananjeyan, Bryan Anenberg, Caden Lu, Carl Doersch, Carolina Parada, Caroline Pantofaru, Charles Shu, Chengda Wu, Christine Chan, Christy Koh, Chuyuan Fu, Claire Cui, Clare Lee, Claudio Fantacci, Connor Schenck, David Rendleman, Deepali Jain, Demetra Brady, Dennis Li, Dhruv Shah, Dimple Vijaykumar, Dirk Ehrlich, Divya Garikapati, Dmitry Kalashnikov, Dre Mahaarachchi, Dushyant Rao, Erik Frey, Fangchen Liu, Federico Casarini, Francesco Nori, Francesco Romano, Frankie Garcia, Gabor Simko, Gautam Salhotra, Giulia Vezzani, Grace Popple, Grace Vesom, Graziano Misuraca, Guangyao Zhou, Hagen Soltau, Hanzi Mao, Hao-Tien Lewis Chiang, Harris Chan, Hila Noga, Howard Zhou, Ian Storz, Idan Lev-Yehudi, Ignacio Rocco, Inessa Konstanz, Isaac Reid, Ishita Prasad, Ivan Kapelyukh, J. Chase Kew, Jacky Liang, Jake Varley, James Susilo, Jasmine Hsu, Jerad Kirkland, Jeremy Plassmann, Jessica Lo, Jie Tan, Jimmy Yan, Jingwei Zhang, Jinyu Xie, Jose Enrique Chen, Joshua Ainslie, Joss Moore, Juanita Bawagan, Junkyung Kim, Justin Lidard, Kanishka Rao, Kathryn Quinn Shea, Kaustubh Sridhar, Keerthana Gopalakrishnan, Ken Caluwaerts, Kenneth Oslund, Khimya Khetarpal, Konstantinos Bousmalis, Krista Reymann, Krzysztof Choromanski, Ksenia Konyushkova, Kun Zhang, Kunal Aneja, Laura Graesser, Leen Verburgh, Leonard Hasenclever, Li-Heng Lin, London Chappellet-Volpini, Lucie Kerley, Maria Attarian, Maria Bauza Villalonga, Marissa Giustina, Max McCabe, Meet Kirankumar Dave, Mehdi S. M. Sajjadi, Metin Tokosz-Exley, Michael Neunert, Michael Noseworthy, Michiel Blokzijl, Miguel Rivas, Mithun George Jacob, Mitsuhiko Nakamoto, Mo Dawoud, Mohan Kumar Srirama, Mohit Sharma, Mohit Shridhar, Muinat Abdul, Murilo F. Martins, Nadav Olmert, Nathan Batchelor, Nicolas Heess, Niko Milonopoulos, Norman Di Palo, Oliver Groth, Ouais Alsharif, Padmini Copparapu, Parth Parekh, Paul Ruiz, Paul Wohlhart, Peide Huang, Peng Xu, Pengfei Xing, Peter Pastor, Petko Yotov, Phil Duffy, Philemon Brakel, Rachel Sterneck, Rajkumar Vasudeva Raju, Ravin Kumar, Razvan Surdulescu, René Wagner, Reza Sanatinia, Robert Baruch, Robert McDonald, Robert Moreno, Rohan Thakker, Roland Hafner, Ryan Doss, Sajjad Zafar, Sally Jesmonth, Sam Haves, Saminda Abeyruwan, Sandy Han Huang, Scott Crowell, Seliem El-Sayed, Sergey Yaroshenko, Sergio Martinez Abad, Serkan Cabi, Sharath Maddineni, Shuang Li, Sichun Xu, Silvia Cruciani, Skanda Koppula, Skye Yang, Soo Sung, Stefan Welker, Stefani Karp, Stefano Saliceti, Steven Hansen, Stuart Bowers, Sumeet Singh, Svetlana Grant, Takahiro Miki, Takuma Yoneda, Thomas Buschmann, Thomas Lampe, Thomas Power, Thor Schaeff, Tim Hertweck, Tingnan Zhang, Todd McInally, Todor Davchev, Tong Zhao, Travers Rhodes, Tsang-Wei Edward Lee, Vika Koriakin, Vikas Sindhwani, Wenhao Yu, Wentao Yuan, Xiaolin Fang, Yahav Nussbaum, Ying Sheng, Ying Xu, Yuheng Kuang, Yuxiang Yang, Yuxiang Zhou

For their leadership and support of this effort, we’d like to thank: Jean-Baptiste Alayrac, Zoubin Ghahramani, Koray Kavukcuoglu and Demis Hassabis. We’d like to recognize the many teams across Google and Google DeepMind that have contributed to this effort including Legal, Marketing, Communications, Responsibility and Safety Council, Responsible Development and Innovation, Policy, Strategy and Operations, and our Business and Corporate Development teams. We’d like to thank everyone on the Robotics team not explicitly mentioned above for their continued support and guidance. Finally, we’d like to thank our partners: Apptronik, Boston Dynamics, and Agile Robots teams for their support.
