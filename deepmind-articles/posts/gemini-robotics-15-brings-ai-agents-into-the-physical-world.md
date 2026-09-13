---
title: "Gemini Robotics 1.5 brings AI agents into the physical world"
source: https://deepmind.google/blog/gemini-robotics-15-brings-ai-agents-into-the-physical-world/
site: deepmind
date: 2025-09-25
authors: Carolina Parada
crawled: 2026-09-13
---

We’re powering an era of physical agents — enabling robots to perceive, plan, think, use tools and act to better solve complex, multi-step tasks.

Earlier this year, we made incredible progress bringing [Gemini](https://deepmind.google/models/gemini/)'s multimodal understanding into the physical world, starting with the [Gemini Robotics](https://deepmind.google/discover/blog/gemini-robotics-brings-ai-into-the-physical-world/) family of models.

Today, we’re taking another step towards advancing intelligent, truly general-purpose robots. We're introducing two models that unlock agentic experiences with advanced thinking:

- [**Gemini Robotics 1.5**](https://deepmind.google/models/gemini-robotics/gemini-robotics/) – Our most capable vision-language-action (VLA) model turns visual information and instructions into motor commands for a robot to perform a task. This model thinks before taking action and shows its process, helping robots assess and complete complex tasks more transparently. It also learns across embodiments, accelerating skill learning.
- [**Gemini Robotics-ER 1.5**](https://deepmind.google/models/gemini-robotics/gemini-robotics-er/) – Our most capable vision-language model (VLM) reasons about the physical world, natively calls digital tools and creates detailed, multi-step plans to complete a mission. This model now achieves state-of-the-art performance across spatial understanding benchmarks.

These advances will help developers build more capable and versatile robots that can actively understand their environment to complete complex, multi-step tasks in a general way.

Starting today, we’re making Gemini Robotics-ER 1.5 available to developers via the Gemini API in [Google AI Studio](https://aistudio.google.com/?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=/). Gemini Robotics 1.5 is currently available to select partners. Read more about building with the next generation of physical agents [on the Developer blog](https://developers.googleblog.com/en/building-the-next-generation-of-physical-agents-with-gemini-robotics-er-1-5/?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=/).

## Gemini Robotics 1.5: Unlocking agentic experiences for physical tasks

Most daily tasks require contextual information and multiple steps to complete, making them notoriously challenging for robots today.

For example, if a robot was asked, “Based on my location, can you sort these objects into the correct compost, recycling and trash bins?" it would need to search for relevant local recycling guidelines on the internet, look at the objects in front of it and figure out how to sort them based on those rules — and then do all the steps needed to completely put them away. So, to help robots complete these types of complex, multi-step tasks, we designed two models that work together in an agentic framework.

Our embodied reasoning model, Gemini Robotics-ER 1.5, orchestrates a robot’s activities, like a high-level brain. This model excels at planning and making logical decisions within physical environments. It has state-of-the-art spatial understanding, interacts in natural language, estimates its success and progress, and can natively call tools like [Google Search](https://search.google/intl/en-GB/?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=/) to look for information or use any third-party user-defined functions.

Gemini Robotics-ER 1.5 then gives Gemini Robotics 1.5 natural language instructions for each step, which uses its vision and language understanding to directly perform the specific actions. Gemini Robotics 1.5 also helps the robot think about its actions to better solve semantically complex tasks, and can even explain its thinking processes in natural language — making its decisions more transparent.

![A diagram illustrating the Gemini Robotics 1.5 agentic system, showing how the high-level orchestrator Gemini Robotics-ER 1.5 uses thinking, tool use, and planning to guide the Gemini Robotics 1.5 VLA model in performing a waste-sorting task.](https://lh3.googleusercontent.com/vSMY895gzWpK-nGK2Vn__6OsjX5DIlTkiBBqggd0f-oAw1oNgh5tFPiZPKtSKIONx4UCT7kiop72Nuj0RMrJ-bICxx21SZCG55LlqcqBA-n_znJw=w1440)

Diagram showing how our embodied reasoning model, Gemini Robotics-ER 1.5, and our vision-language-action model, Gemini Robotics 1.5, actively work together to perform complex tasks in the physical world.

Both of these models are built on the core Gemini family of models and have been fine-tuned with different datasets to specialize in their respective roles. When combined, they increase the robot’s ability to generalize to longer tasks and more diverse environments.

![](https://lh3.googleusercontent.com/sdFcpCoe-jJQIx2Ay8OzvMoz0WHXK0wJ0fa9WNG2JzqmGEfBH8d60a5YUlWQkJ9wlMfbJEAJ6wphjI9jAlaZcE9BTIEpInPQowHpvGMHZe9Ui8qiGQ=w1440-h810-n-nu)

### Understands its environment

Gemini Robotics-ER 1.5 is the first thinking model optimized for embodied reasoning. It achieves state-of-the-art performance on both academic and internal benchmarks, inspired by real-world use cases from our trusted tester program.

We evaluated Gemini Robotics-ER 1.5 on 15 academic benchmarks including [Embodied Reasoning Question Answering](https://github.com/embodiedreasoning/ERQA) (ERQA) and [Point-Bench](https://pointarena.github.io/), measuring the model’s performance on pointing, image question answering and video question answering.

See details in [our tech report](https://storage.googleapis.com/deepmind-media/gemini-robotics/Gemini-Robotics-1-5-Tech-Report.pdf).

![Bar chart showing aggregated performance on 15 academic embodied reasoning benchmarks, with Gemini Robotics-ER 1.5 highlighted in blue achieving the highest score of over 60, followed by GPT-5, GPT-5-mini, Gemini Robotics-ER 1.0, and GPT-5-Nano.](https://lh3.googleusercontent.com/iGOPSXl7VFgFdMJW9V7dCfa8ngGLwHmaIOL9bDgrQMULRVVIku-ukMdcdRl0XVZPLnhpJLdkayLARFTDkoSwkyEgXi5s35vcMDRtnwLuf0oyx3Xqyg=w1440)

Bar graph showing Gemini Robotics-ER 1.5’s state-of-the-art performance results compared to similar models. Our model achieves the highest aggregated performance on 15 academic embodied reasoning benchmarks, including Point-Bench, RefSpatial, RoboSpatial-Pointing, Where2Place, BLINK, CV-Bench, ERQA, EmbSpatial, MindCube, RoboSpatial-VQA, SAT, Cosmos-Reason1, Min Video Pairs, OpenEQA and VSI-Bench.

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

A collage of GIFs showing some of Gemini Robotics-ER 1.5’s capabilities, including object detection and state estimation, segmentation mask, pointing, trajectory prediction and task progress estimation and success detection.

## Thinks before acting

Vision-language-action models traditionally translate instructions or linguistic plans directly into a robot’s movement. Beyond simply translating instructions or plans, Gemini Robotics 1.5, can now think before taking action. This means it can generate an internal sequence of reasoning and analysis in natural language to perform tasks that require multiple steps or require a deeper semantic understanding.

For example, when completing a task like, “Sort my laundry by color,” the robot in the video below thinks at different levels. First, it understands that sorting by color means putting the white clothes in the white bin and other colors in the black bin. Then it thinks about steps to take, like picking up the red sweater and putting it in the black bin, and about the detailed motion involved, like moving a sweater closer to pick it up more easily.

![](https://lh3.googleusercontent.com/z1XbNpE9I8GVhHf9jWsER5fFXj0TVWgsRE42CnYTInCMt2x83RvAbGtUJ46gBeg57mSLFQi3XBUT8Rt7bo7kKAV-hhOmM7-oBeV4wyGro6UXvL--85Y=w1440-h810-n-nu)

During this multi-level thinking process, the vision-language-action model can decide to turn longer tasks into simpler shorter segments that the robot can execute successfully. It also helps the model generalize to solve new tasks and be more robust to changes in its environment.

## Learns across embodiments

Robots come in all shapes and sizes, and have different sensing capabilities and different degrees of freedom, making it difficult to transfer motions learned from one robot to another.

Gemini Robotics 1.5 shows a remarkable ability to learn across different embodiments. It can transfer motions learned from one robot to another, without needing to specialize the model to each new embodiment. This breakthrough accelerates learning new behaviors, helping robots become smarter and more useful.

For example, we observe that tasks only presented to the [ALOHA 2](https://aloha-2.github.io/) robot during training, also just work on the Apptronik’s humanoid robot, [Apollo](https://apptronik.com/apollo), and the bi-arm [Franka](https://franka.de/franka-research-3-arm) robot, and vice versa.

![](https://lh3.googleusercontent.com/vHo1vRQXDOOR3movvDNdiYIBH5xfw3gxknu3Q9XE1TYtFJCiCxF_6FdgiQoSiMmNqQJOn01aD4ySoMuio2rzI49xqS_q-8828m7oJ5KzA5IvhJDBEr8=w1440-h810-n-nu)

## How we’re responsibly advancing AI and Robotics

As we unlock the full potential of embodied AI, we’re proactively developing novel safety and alignment approaches to enable agentic AI robots to be responsibly deployed in human-centric environments.

Our Responsibility & Safety Council (RSC) and Responsible Development & Innovation (ReDI) team partner with the Robotics team to ensure that the development of these models are in line with our [AI Principles](https://ai.google/principles/?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=).

Gemini Robotics 1.5 implements a holistic approach to safety through high-level semantic reasoning, including thinking about safety before acting, ensuring respectful dialogue with humans via alignment with existing [Gemini Safety Policies](https://storage.googleapis.com/deepmind-media/gemini/gemini_v2_5_report.pdf), and triggering low-level safety sub-systems (e.g. for collision avoidance) on-board the robot when needed.

To guide our safe development of Gemini Robotics models, we’re also releasing an upgrade of the [ASIMOV benchmark](http://asimov-benchmark.github.io/v2), a comprehensive collection of datasets for evaluating and improving semantic safety, with better tail coverage, improved annotations, new safety question types and new video modalities.

In our safety evaluations on the [ASIMOV benchmark](http://asimov-benchmark.github.io/v2), Gemini Robotics-ER 1.5 shows state-of-the-art performance, and its thinking ability significantly contributes to the improved understanding of semantic safety and better adherence to physical safety constraints.

Learn more about our safety research in [our tech report](https://storage.googleapis.com/deepmind-media/gemini-robotics/Gemini-Robotics-1-5-Tech-Report.pdf) or visit [our safety website](https://deepmind.google/models/gemini-robotics/responsibly-advancing-ai-and-robotics/).

## A milestone towards solving AGI in the physical world

Gemini Robotics 1.5 marks an important milestone towards solving AGI in the physical world. By introducing agentic capabilities, we’re moving beyond models that react to commands and creating systems that can truly reason, plan, actively use tools and generalize.

This is a foundational step toward building robots that can navigate the complexities of the physical world with intelligence and dexterity, and ultimately, become more helpful and integrated into our lives.

We’re excited to continue this work with the broader research community and can’t wait to see what the robotics community builds with our latest Gemini Robotics-ER model.

**Explore Gemini Robotics 1.5**

[Read the tech report](https://storage.googleapis.com/deepmind-media/gemini-robotics/Gemini-Robotics-1-5-Tech-Report.pdf)[Sign up to our trusted tester program](https://docs.google.com/forms/d/1sM5GqcVMWv-KmKY3TOMpVtQ-lDFeAftQ-d9xQn92jCE/edit?ts=67cef986)[Learn more on the Developer blog](https://developers.googleblog.com/en/building-the-next-generation-of-physical-agents-with-gemini-robotics-er-1-5/?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=)

**Acknowledgements**This work was developed by the Gemini Robotics team: Abbas Abdolmaleki, Saminda Abeyruwan, Joshua Ainslie, Jean-Baptiste Alayrac, Montserrat Gonzalez Arenas, Ashwin Balakrishna, Nathan Batchelor, Alex Bewley, Jeff Bingham, Michael Bloesch, Konstantinos Bousmalis, Philemon Brakel, Anthony Brohan, Thomas Buschmann, Arunkumar Byravan, Serkan Cabi, Ken Caluwaerts, Federico Casarini, Christine Chan, Oscar Chang, London Chappellet-Volpini, Jose Enrique Chen, Xi Chen, Hao-Tien Lewis Chiang, Krzysztof Choromanski, Adrian Collister, David B. D'Ambrosio, Sudeep Dasari, Todor Davchev, Meet Kirankumar Dave, Coline Devin, Norman Di Palo, Tianli Ding, Carl Doersch, Adil Dostmohamed, Yilun Du, Debidatta Dwibedi, Sathish Thoppay Egambaram, Michael Elabd, Tom Erez, Xiaolin Fang, Claudio Fantacci, Cody Fong, Erik Frey, Chuyuan Fu, Ruiqi Gao, Marissa Giustina, Keerthana Gopalakrishnan, Laura Graesser, Oliver Groth, Agrim Gupta, Roland Hafner, Steven Hansen, Leonard Hasenclever, Sam Haves, Nicolas Heess, Brandon Hernaez, Alex Hofer, Jasmine Hsu, Lu Huang, Sandy H. Huang, Atil Iscen, Mithun George Jacob, Deepali Jain, Sally Jesmonth, Abhishek Jindal, Ryan Julian, Dmitry Kalashnikov, Stefani Karp, Matija Kecman, J. Chase Kew, Donnie Kim, Frank Kim, Junkyung Kim, Thomas Kipf, Sean Kirmani, Ksenia Konyushkova, Yuheng Kuang, Thomas Lampe, Antoine Laurens, Tuan Anh Le, Isabel Leal, Alex X. Lee, Tsang-Wei Edward Lee, Guy Lever, Jacky Liang, Li-Heng Lin, Fangchen Liu, Shangbang Long, Caden Lu, Sharath Maddineni, Anirudha Majumdar, Kevis-Kokitsi Maninis, Andrew Marmon, Sergio Martinez, Assaf Hurwitz Michaely, Niko Milonopoulos, Joss Moore, Robert Moreno, Michael Neunert, Francesco Nori, Joy Ortiz, Kenneth Oslund, Carolina Parada, Emilio Parisotto, Peter Pastor Sampedro, Acorn Pooley, Thomas Power, Alessio Quaglino, Haroon Qureshi, Rajkumar Vasudeva Raju, Helen Ran, Dushyant Rao, Kanishka Rao, Isaac Reid, David Rendleman, Krista Reymann, Miguel Rivas, Francesco Romano, Yulia Rubanova, Pannag R Sanketi, Dhruv Shah, Mohit Sharma, Kathryn Shea, Mohit Shridhar, Charles Shu, Vikas Sindhwani, Sumeet Singh, Radu Soricut, Rachel Sterneck, Ian Storz, Razvan Surdulescu, Jie Tan, Jonathan Tompson, Saran Tunyasuvunakool, Jake Varley, Grace Vesom, Giulia Vezzani, Maria Bauza Villalonga, Oriol Vinyals, René Wagner, Ayzaan Wahid, Stefan Welker, Paul Wohlhart, Chengda Wu, Markus Wulfmeier, Fei Xia, Ted Xiao, Annie Xie, Jinyu Xie, Peng Xu, Sichun Xu, Ying Xu, Zhuo Xu, Jimmy Yan, Sherry Yang, Skye Yang, Yuxiang Yang, Hiu Hong Yu, Wenhao Yu, Li Yang Ku, Wentao Yuan, Yuan Yuan, Jingwei Zhang, Tingnan Zhang, Zhiyuan Zhang, Allan Zhou, Guangyao Zhou and Yuxiang Zhou.

We’d also like to thank: Amy Nommeots-Nomm, Ashley Gibb, Bhavya Sukhija, Bryan Gale, Catarina Barros, Christy Koh, Clara Barbu, Demetra Brady, Hiroki Furuta, Jennie Lees, Kendra Byrne, Keran Rong, Kevin Murphy, Kieran Connell, Kuang-Huei Lee, M. Emre Karagozler, Martina Zambelli, Matthew Jackson, Michael Noseworthy, Miguel Lázaro-Gredilla, Mili Sanwalka, Mimi Jasarevic, Nimrod Gileadi, Rebeca Santamaria-Fernandez, Rui Yao, Siobhan Mcloughlin, Sophie Bridgers, Stefano Saliceti, Steven Bohez, Svetlana Grant, Tim Hertweck, Verena Rieser, Yandong Ji.

For their leadership and support of this effort, we’d like to thank: Jean-Baptiste Alayrac, Zoubin Ghahramani, Koray Kavukcuoglu and Demis Hassabis. We’d like to recognize the many teams across Google and Google DeepMind that have contributed to this effort including Legal, Marketing, Communications, Responsibility and Safety Council, Responsible Development and Innovation, Policy, Strategy and Operations, and our Business and Corporate Development teams. We’d like to thank everyone on the Robotics team not explicitly mentioned above for their continued support and guidance. Finally, we’d like to thank the Apptronik team for their support.
