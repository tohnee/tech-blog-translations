---
title: "Gemini Robotics On-Device brings AI to local robotic devices"
source: https://deepmind.google/blog/gemini-robotics-on-device-brings-ai-to-local-robotic-devices/
site: deepmind
date: 2025-06-24
authors: Carolina Parada
crawled: 2026-09-13
---

We’re introducing an efficient, on-device robotics model with general-purpose dexterity and fast task adaptation.

In March, we introduced [Gemini Robotics](https://deepmind.google/discover/blog/gemini-robotics-brings-ai-into-the-physical-world/), our most advanced VLA (vision language action) model, bringing Gemini 2.0’s multimodal reasoning and real-world understanding into the physical world.

Today, we’re introducing Gemini Robotics On-Device, our most powerful VLA model optimized to run locally on robotic devices. Gemini Robotics On-Device shows strong general-purpose dexterity and task generalization, and it’s optimized to run efficiently on the robot itself.

Since the model operates independent of a data network, it’s helpful for latency sensitive applications, and ensures robustness in environments with intermittent or zero connectivity.

We’re also sharing a [Gemini Robotics SDK](https://github.com/google-deepmind/gemini-robotics-sdk) to help developers easily evaluate Gemini Robotics On-Device on their tasks and environments, test our model in our [MuJoCo](https://github.com/google-deepmind/aloha_sim) physics simulator, and quickly adapt it to new domains, with as few as 50 to 100 demonstrations. Developers can access the SDK by signing up to our trusted tester program.

## Model capabilities and performance

Gemini Robotics On-Device is a robotics foundation model for bi-arm robots, engineered to require minimal computational resources. It builds on the task generalization and dexterity capabilities of Gemini Robotics and is:

- Designed for rapid experimentation with dexterous manipulation.
- Adaptable to new tasks through fine-tuning to improve performance.
- Optimized to run locally with low-latency inference.

Gemini Robotics On-Device achieves strong visual, semantic and behavioral generalization across a wide range of testing scenarios, follows natural language instructions, and completes highly-dexterous tasks like unzipping bags or folding clothes — all while operating directly on the robot.

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

In our evaluations, our On-Device mode exhibits strong generalization performance while running entirely locally.

![A bar chart titled "Generalization Benchmark results across 9 tasks" comparing the success rates of three models—Gemini Robotics (blue), Previous Best On-Device (cyan), and Gemini Robotics On-Device (purple)—across Visual, Semantic, and Action generalization. For all three benchmarks, Gemini Robotics has the highest success rate (ranging from 0.6 to 0.75), followed closely by Gemini Robotics On-Device (ranging from approximately 0.52 to 0.74), while the Previous Best On-Device model performs significantly lower (ranging from 0.11 to 0.36).](https://lh3.googleusercontent.com/I6Zopg7Y_-VweSLsrzuRFGXeuIvUAJPXwEnxvnFyGjqWl65K3luU2WFHyGEu4xvC-QWB7jW62FM5j_oKk6pvZB7X6QXsKKdYehyJZYoKmHem7MAJ35U=w1440)

Chart evaluating Gemini Robotics On-Device’s generalization performance, compared to our flagship Gemini Robotics model and the previous best on-device model.

Gemini Robotics On-Device also outperforms other on-device alternatives on more challenging out-of-distribution tasks and complex multi-step instructions. For developers seeking state-of-the-art results in these settings, without on-device limitations, we also offer the Gemini Robotics model.

![A bar chart titled "Instruction Following Benchmark measuring steerability" comparing the success rates of three models across "Easy" and "Hard" tasks. For both categories, Gemini Robotics (blue) has the highest success rate, followed by Gemini Robotics On-Device (purple), while the Previous Best On-Device model (cyan) has the lowest performance.](https://lh3.googleusercontent.com/SVQOj7ZJccb_C3l3VQ6aoXprwYDyozOFLTswucWr92L5e9vexhETlk4Oib6tym_v6IdhvpVzrmTVIlR2KHBohma7LtQ-kxTzZkYnmVkXoNb5bajn=w1440)

Chart evaluating Gemini Robotics On-Device’s instruction following performance, compared to our flagship Gemini Robotics model and the previous best on-device model.

To learn more about our evaluations, read our [Gemini Robotics tech report](https://arxiv.org/pdf/2503.20020).

## Adaptable to new tasks, generalizable across embodiments

Gemini Robotics On-Device is the first VLA model we're making available for fine-tuning. While many tasks will work out of the box, developers can also choose to adapt the model to achieve better performance for their applications. Our model quickly adapts to new tasks, with as few as 50 to 100 demonstrations — indicating how well this on-device model can generalize its foundational knowledge to new tasks.

Here, we show how Gemini Robotics On-Device outperforms the current, best on-device VLA on tasks involving fine-tuning to newer models. We tested the model on seven dexterous manipulation tasks of varying degrees of difficulty, including zipping a lunch-box, drawing a card and pouring salad dressing.

![A bar chart titled "Fast Adaptation" comparing the "Average Success Rate over Fast Adaptation Tasks" for three models. Gemini Robotics (blue) has the highest success rate at 0.8, followed by Gemini Robotics On-Device (purple) at approximately 0.68, and the Previous Best On-Device model (cyan) at approximately 0.53.](https://lh3.googleusercontent.com/4YSKJSyeJJsQHU8Tz0jpkDloDAkF7Yb7mtcy8ECn5qC4nBFY9_75DSs1-qr-XNRGZvAvFZ2NaJ5LABD16QBZrPPufZt3oyTxWWKGh0M7im9uFt6edQ=w1440)

Chart showing Gemini Robotics On-Device’s task adaptation performance, with fewer than 100 examples.

We further adapted the Gemini Robotics On-Device model to different robot embodiments. While we trained our model only for [ALOHA robots](https://aloha-2.github.io/), we were able to further adapt it to a bi-arm [Franka FR3 robot](https://franka.de/franka-research-3) and the [Apollo humanoid robot](https://apptronik.com/apollo) by Apptronik.

On the bi-arm Franka, the model performs general-purpose instruction following, including handling previously unseen objects and scenes, completing dexterous tasks like folding a dress, or executing [industrial belt assembly tasks](https://www.nist.gov/el/intelligent-systems-division-73500/robotic-grasping-and-manipulation-assembly/assembly) that require precision and dexterity.

On the Apollo humanoid, we adapt the model to a significantly different embodiment. The same generalist model can follow natural language instructions and manipulate different objects, including previously unseen objects, in a general manner.

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

## Responsible development and safety

We’re developing all Gemini Robotics models in alignment with our [AI Principles](https://ai.google/principles/?utm_source=&utm_medium=&utm_campaign=&utm_content=) and applying a [holistic safety approach](https://sites.google.com/corp/view/safe-robots) spanning semantic and physical safety.

In practice, we capture semantic and content safety using the [Live API](https://ai.google.dev/gemini-api/docs/live?utm_source=&utm_medium=&utm_campaign=&utm_content=), and interface our models with low-level safety critical controllers to execute the actions. We recommend evaluating the end-to-end system on our recently developed [semantic safety benchmark](https://asimov-benchmark.github.io/) and performing [red-teaming exercises](https://predictive-red-team.github.io/) at all levels to expose the model’s safety vulnerabilities.

Our Responsible Development & Innovation (ReDI) team continues to analyze and advise on the real-world impact of all Gemini Robotics models, finding ways to maximize their societal impact and minimize risk. Then our Responsibility & Safety Council (RSC) reviews these assessments, providing feedback to integrate into model development to help further maximize benefits and minimize risk.

To gain a deeper understanding of Gemini Robotics On-Device’s usage and safety profile and to gather feedback, we’re initially releasing it to a select group of trusted testers.

## Accelerating innovation in robotics

Gemini Robotics On-Device marks a step forward in making powerful robotics models more accessible and adaptable — and our on-device solution will help the robotics community tackle important latency and connectivity challenges.

The Gemini Robotics SDK will further accelerate innovation by allowing developers to adapt the model to their specific needs. Sign up for model and SDK access via our [trusted tester program](https://docs.google.com/forms/d/1sM5GqcVMWv-KmKY3TOMpVtQ-lDFeAftQ-d9xQn92jCE/edit?ts=67cef986).

We’re excited to see what the robotics community will build with these new tools as we continue to explore the future of bringing AI into the physical world.

[Sign up for our trusted tester program](https://docs.google.com/forms/d/1sM5GqcVMWv-KmKY3TOMpVtQ-lDFeAftQ-d9xQn92jCE/edit?ts=67cef986&utm_source=&utm_medium=&utm_campaign=&utm_content=)[Read the Gemini Robotics tech report](https://arxiv.org/pdf/2503.20020)[Test ALOHA robots in simulation](https://github.com/google-deepmind/aloha_sim)

**Acknowledgements**

We gratefully acknowledge contributions, advice, and support from Abbas Abdolmaleki, Saminda Abeyruwan, Joshua Ainslie, Jean-Baptiste Alayrac, Montserrat Gonzalez Arenas, Travis Armstrong, Maria Attarian, Ashwin Balakrishna, Yanan Bao, Clara Barbu, Catarina Barros, Robert Baruch, Nathan Batchelor, Maria Bauza, Lucas Beyer, Jeff Bingham, Michael Bloesch, Michiel Blokzijl, Steven Bohez, Konstantinos Bousmalis, Demetra Brady, Philemon Brakel, Anthony Brohan, Thomas Buschmann, Arunkumar Byravan, Kendra Byrne, Serkan Cabi, Ken Caluwaerts, Federico Casarini, Christine Chan, Oscar Chang, Jose Enrique Chen, Xi Chen, Huizhong Chen, Hao-Tien Lewis Chiang, Krzysztof Choromanski, Adrian Collister, Kieran Connell, David D'Ambrosio, Sudeep Dasari, Todor Davchev, Coline Devin, Norman Di Palo, Tianli Ding, Adil Dostmohamed, Anca Dragan, Yilun Du, Debidatta Dwibedi, Michael Elabd, Tom Erez, Claudio Fantacci, Cody Fong, Erik Frey, Chuyuan Fu, Frankie Garcia, Ashley Gibb, Marissa Giustina, Keerthana Gopalakrishnan, Laura Graesser, Simon Green, Oliver Groth, Roland Hafner, Leonard Hasenclever, Sam Haves, Nicolas Heess, Brandon Hernaez, Tim Hertweck, Alexander Herzog, R. Alex Hofer, Sandy H Huang, Jan Humplik , Atil Iscen, Mithun George Jacob, Deepali Jain, Sally Jesmonth, Ryan Julian, Dmitry Kalashnikov, M. Emre Karagozler, Stefani Karp, Chase Kew, Jerad Kirkland, Sean Kirmani, Yuheng Kuang, Thomas Lampe, Antoine Laurens, Isabel Leal, Alex X. Lee, Tsang-Wei Edward Lee, Jennie Lees, Jacky Liang, Yixin Lin, Li-Heng Lin, Caden Lu, Sharath Maddineni, Anirudha Majumdar, Kevis-Kokitsi Maninis, Siobhan Mcloughlin, Assaf Hurwitz Michaely, Joss Moore, Robert Moreno, Thomas Mulc, Michael Neunert, Francesco Nori, Dave Orr, Carolina Parada, Emilio Parisotto, Peter Pastor, André Susano Pinto, Acorn Pooley, Grace Popple, Thomas Power, Alessio Quaglino, Haroon Qureshi, Kanishka Rao, Dushyant Rao, Krista Reymann, Martin Riedmiller, Francesco Romano, Keran Rong, Dorsa Sadigh, Stefano Saliceti, Daniel Salz, Pannag Sanketi, Mili Sanwalka, Kevin Sayed, Pierre Sermanet, Dhruv Shah, Mohit Sharma, Kathryn Shea, Mohit Shridhar, Charles Shu, Laurent Simon, Vikas Sindhwani, Sumeet Singh, Radu Soricut, Andreas Steiner, Rachel Sterneck, Ian Storz, Razvan Surdulescu, Ben Swanson, Mitri Syriani, Jie Tan, Yuval Tassa, Alan Thompson, Dhruva Tirumala, Jonathan Tompson, Karen Truong, Jake Varley, Siddharth Verma, Grace Vesom, Giulia Vezzani, Oriol Vinyals, Ayzaan Wahid, Zhicheng Wang, Xiaohan Wang, Stefan Welker, Paul Wohlhart, Chengda Wu, Markus Wulfmeier, Fei Xia, Ted Xiao, Annie Xie, Jinyu Xie, Peng Xu, Sichun Xu, Ying Xu, Zhuo Xu, Yuxiang Yang, KongQun Yang, Rui Yao, Sergey Yaroshenko, Matt Young, Wenhao Yu, Wentao Yuan, Martina Zambelli, Xiaohua Zhai, Jingwei Zhang, Tingnan Zhang, Allan Zhou, Yuxiang Zhou, Guangyao (Stannis) Zhou, Howard Zhou.

We also thank the operations and support staff that performed data collection and robot evaluations for this project.
