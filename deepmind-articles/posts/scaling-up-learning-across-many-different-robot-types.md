---
title: "Scaling up learning across many different robot types"
source: https://deepmind.google/blog/scaling-up-learning-across-many-different-robot-types/
site: deepmind
date: 2023-10-03
authors: Quan Vuong, Pannag Sanketi
crawled: 2026-09-13
---

Together with partners from 33 academic labs, we have pooled data from 22 different robot types to create the Open X-Embodiment dataset and RT-X model

Robots are great specialists, but poor generalists. Typically, you have to train a model for each task, robot, and environment. Changing a single variable often requires starting from scratch. But what if we could combine the knowledge across robotics and create a way to train a general-purpose robot?

Today, we are launching a [new set of resources for general-purpose robotics learning](https://arxiv.org/abs/2310.08864) across different robot types, or embodiments. Together with partners from 33 academic labs we have pooled data from 22 different robot types to create the Open X-Embodiment dataset. We also release RT-1-X, a robotics transformer (RT) model derived from [RT-1](https://blog.research.google/2022/12/rt-1-robotics-transformer-for-real.html) and trained on our dataset, that shows skills transfer across many robot embodiments.

In this work, we show training a single model on data from multiple embodiments leads to significantly better performance across many robots than those trained on data from individual embodiments. We tested our RT-1-X model in five different research labs, demonstrating 50% success rate improvement on average across five different commonly used robots compared to methods developed independently and specifically for each robot. We also showed that training our visual language action model, [RT-2](https://www.deepmind.com/blog/rt-2-new-model-translates-vision-and-language-into-action), on data from multiple embodiments tripled its performance on real-world robotic skills.

We developed these tools to collectively advance cross-embodiment research in the robotics community. The Open X-Embodiment dataset and RT-1-X model checkpoint are now available for the benefit of the broader research community, thanks to the work of robotics labs around the world that shared data and helped evaluate our model in a commitment to openly and responsibly developing this technology. We believe these tools will transform the way robots are trained and accelerate this field of research.

## Open X-Embodiment Dataset: Collecting data to train AI robots

Datasets, and the models trained on them, have played a critical role in advancing AI. Just as [ImageNet](https://www.image-net.org/index.php) propelled computer vision research, we believe Open X-Embodiment can do the same to advance robotics. Building a dataset of diverse robot demonstrations is the key step to training a generalist model that can control many different types of robots, follow diverse instructions, perform basic reasoning about complex tasks, and generalize effectively.  However, collecting such a dataset is too resource-intensive for any single lab.

To develop the Open X-Embodiment dataset, we partnered with academic research labs across more than 20 institutions to gather data from 22 robot embodiments, demonstrating more than 500 skills and 150,000 tasks across more than 1 million episodes. This dataset is the most comprehensive robotics dataset of its kind.

![A grid of 24 video stills showing various types of robotic arms performing different tasks.](https://lh3.googleusercontent.com/IY4K4inaQaBbeElljOAXs7m3CIJMTl9OpDz4CgrtlzkTEfn_HHq02c88BbRagmTewAz68ImKt7sPRy4hcm29zNFTRs9nFBrXlR9tSVjBJYPLrDlKow=w1440)

Samples from the Open X-Embodiment Dataset demonstrating more than 500 skills and 150,000 tasks.

![Two bar charts illustrating the composition of the Open X-Embodiment dataset. Chart (a), "Datasets per Robot Embodiment," shows Franka as the most represented robot, followed by xArm and Sawyer. Chart (b), "Common Dataset Skills," shows the distribution of skills in the dataset, with "picking," "moving," and "pushing" as the most frequent actions.](https://lh3.googleusercontent.com/DT05E5se1pTEj1EkJlf0yBAEcSbRUC3q9iyjOmfmb14i_6HTJBhwiVMYDoy7pqK5yGG2WJKk5H8WnhWbeAPAc5RmTTsyPaTEtqpuag_QH2qamrxXs28=w1440)

The Open X-Embodiment dataset combines data across embodiments, datasets and skills.

## RT-X: A general-purpose robotics model

RT-X builds on two of our robotics transformer models. We trained RT-1-X using [RT-1](https://blog.research.google/2022/12/rt-1-robotics-transformer-for-real.html), our model for real-world robotic control at scale, and we trained RT-2-X on [RT-2](https://www.deepmind.com/blog/rt-2-new-model-translates-vision-and-language-into-action), our vision-language-action (VLA) model that learns from both web and robotics data. Through this, we show that given the same model architecture, RT-1-X and RT-2-X are able to achieve greater performance thanks to the much more diverse, cross-embodiment data they are trained on. We also show that they improve on models trained in specific domains, and exhibit better generalization and new capabilities.

To evaluate RT-1-X in partner academic universities, we compared how it performed against models developed for their specific task, like opening a door, on corresponding dataset. RT-1-X trained with the Open X-Embodiment dataset outperformed the original model by 50% on average.

![Bar chart showing that the RT-1-X model consistently outperforms original methods across five different university robotics labs, with a mean success rate of 63% compared to the baseline mean of 41%.](https://lh3.googleusercontent.com/UpRLdhH270shlq6EYSQBg0KARHtV4ZRbDNjU2HWn6_n3mvU-8LCfhjryVEHFSgckdgQ9_77WNU1ORhAGoOhJS0ExWYc47B5OhTQ3MfYXtz_q6YHstg=w1440)

RT-1-X mean success rate is 50% higher than the corresponding Original method.

![A collection of five short, looping video clips showing different robotic arms performing tasks in various university labs: a robot arm interacting with table objects (CLVR, USC), routing a white cable through a metal guide (RAIL, UC Berkeley), opening a white cabinet door (CILVR, NYU), wiping a wooden surface with a cloth (AUTOLab, UC Berkeley), and interacting with buttons on a cardboard box (AiS, University of Freiburg).](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/651bf88fe2241d17b4fc187c_Fig3B_RT-X.gif)

Videos of RT-1-X evaluations run at different partner universities

## Emergent skills in RT-X

To investigate the transfer of knowledge across robots, we conduct experiments with our helper robot on tasks that involve objects and skills that are not present in the RT-2 dataset but exist in another dataset for a different robot. Specifically, RT-2-X was three times as successful as our previous best model, RT-2, for emergent skills.

Our results suggest that co-training with data from other platforms imbues RT-2-X with additional skills that were not present in the original dataset, enabling it to perform novel tasks.

![Bar chart showing the mean success rate of RT-2 at roughly 25% compared to RT-2-X at approximately 75%, demonstrating a 3x increase in emergent skill evaluation.](https://lh3.googleusercontent.com/mKX3hCLy0YOzzwd4gXaM0_K2Mypupwx53B-yBmDrNvgNvmMDCju-4muw4IdSXoiBT4vl925vYWWyZ641qdRIUfAh-RXCx574ujCQ8J85ZLPYSvLV=w1440)

![A short animation, showing a robotic arm moving an apple between a can and an orange. Then moving an apple near a cloth. Then moving an apple on top of a pot.This demonstrates its ability to understand spatial relationships.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/651bf8dc08ece07a453c6cdb_Fig5_RT-X.gif)

RT-2-X demonstrates understanding of spatial relationships between objects.

RT-2-X demonstrates skills that the RT-2 model was not capable of previously, including better spatial understanding. For example, if we ask the robot to "move apple near cloth" instead of "move apple on cloth" the trajectories are quite different. By changing the preposition from "near" to "on", we can modulate the actions that robot takes.

RT-2-X shows that combining data from other robots into the training improves the range of tasks that can be performed even by a robot that already has large amounts of data available – but only when utilizing a sufficiently high-capacity architecture.

![A robotic arm identifies a plastic pepper sitting between a plastic carrot and plastic ice cream cone. It then picks the pepper up and places it in a yellow basket.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/651bf921492f377d1e2866a2_Fig6_RTX.gif)

RT-2-X (55B): one of the biggest models to date performing unseen tasks in an academic lab

## Responsibly advancing robotics research

Robotics research is at an exciting, but early, juncture. New research shows the potential to develop more useful helper robots by scaling learning with more diverse data, and better models. Working collaboratively with labs around the world and sharing resources is crucial to advancing robotics research in an open and responsible way. We hope that open sourcing the data and providing safe but limited models will reduce barriers and accelerate research. The future of robotics relies on enabling robots to learn from each other, and most importantly, allowing researchers to learn from one another.

This work demonstrates that models that generalize across embodiments are possible, with dramatic improvements in performance both with robots here at Google DeepMind and on robots at different universities around the world. Future research could explore how to combine these advances with the self-improvement property of [RoboCat](https://www.deepmind.com/blog/robocat-a-self-improving-robotic-agent) to enable the models to improve with their own experience. Another future direction could be to further probe how different dataset mixtures might affect cross-embodiment generalization and how the improved generalization materializes.

**Partner with us:** [open-x-embodiment@googlegroups.com](mailto:open-x-embodiment@googlegroups.com)

[Read our paper](https://arxiv.org/abs/2310.08864)[Access our data and model](https://robotics-transformer-x.github.io/)

**Notes**

We would like to thank the co-authors of this work: Abhishek Padalkar, Acorn Pooley, Ajinkya Jain, Alex Bewley, Alex Herzog, Alex Irpan, Alexander Khazatsky, Anant Rai, Anikait Singh, Anthony Brohan, Antonin Raffin, Ayzaan Wahid, Ben Burgess-Limerick, Beomjoon Kim, Bernhard Schölkopf, Brian Ichter, Cewu Lu, Charles Xu, Chelsea Finn, Chenfeng Xu, Cheng Chi, Chenguang Huang, Christine Chan, Chuer Pan, Chuyuan Fu, Coline Devin, Danny Driess, Deepak Pathak, Dhruv Shah, Dieter Büchler, Dmitry Kalashnikov, Dorsa Sadigh, Edward Johns, Federico Ceola, Fei Xia, Freek Stulp, Gaoyue Zhou, Gaurav S. Sukhatme, Gautam Salhotra, Ge Yan, Giulio Schiavi, Hao Su, Hao-Shu Fang, Haochen Shi, Heni Ben Amor, Henrik I Christensen, Hiroki Furuta, Homer Walke, Hongjie Fang, Igor Mordatch, Ilija Radosavovic, Isabel Leal, Jacky Liang, Jaehyung Kim, Jan Schneider, Jasmine Hsu, Jeannette Bohg, Jeffrey Bingham, Jiajun Wu, Jialin Wu, Jianlan Luo, Jiayuan Gu, Jie Tan, Jihoon Oh, Jitendra Malik, Jonathan Tompson, Jonathan Yang, Joseph J. Lim, João Silvério, Junhyek Han, Kanishka Rao, Karl Pertsch, Karol Hausman, Keegan Go, Keerthana Gopalakrishnan, Ken Goldberg, Kendra Byrne, Kenneth Oslund, Kento Kawaharazuka, Kevin Zhang, Keyvan Majd, Krishan Rana, Krishnan Srinivasan, Lawrence Yunliang Chen, Lerrel Pinto, Liam Tan, Lionel Ott, Lisa Lee, Masayoshi Tomizuka, Maximilian Du, Michael Ahn, Mingtong Zhang, Mingyu Ding, Mohan Kumar Srirama, Mohit Sharma, Moo Jin Kim, Naoaki Kanazawa, Nicklas Hansen, Nicolas Heess, Nikhil J Joshi, Niko Suenderhauf, Norman Di Palo, Nur Muhammad Mahi Shafiullah, Oier Mees, Oliver Kroemer, Pannag R Sanketi, Paul Wohlhart, Peng Xu, Pierre Sermanet, Priya Sundaresan, Quan Vuong, Rafael Rafailov, Ran Tian, Ria Doshi, Roberto Martín-Martín, Russell Mendonca, Rutav Shah, Ryan Hoque, Ryan Julian, Samuel Bustamante, Sean Kirmani, Sergey Levine, Sherry Moore, Shikhar Bahl, Shivin Dass, Shuran Song, Sichun Xu, Siddhant Haldar, Simeon Adebola, Simon Guist, Soroush Nasiriany, Stefan Schaal, Stefan Welker, Stephen Tian, Sudeep Dasari, Suneel Belkhale, Takayuki Osa, Tatsuya Harada, Tatsuya Matsushima, Ted Xiao, Tianhe Yu, Tianli Ding, Todor Davchev, Tony Z. Zhao, Travis Armstrong, Trevor Darrell, Vidhi Jain, Vincent Vanhoucke, Wei Zhan, Wenxuan Zhou, Wolfram Burgard, Xi Chen, Xiaolong Wang, Xinghao Zhu, Xuanlin Li, Yao Lu, Yevgen Chebotar, Yifan Zhou, Yifeng Zhu, Ying Xu, Yixuan Wang, Yonatan Bisk, Yoonyoung Cho, Youngwoon Lee, Yuchen Cui, Yueh-hua Wu, Yujin Tang, Yuke Zhu, Yunzhu Li, Yusuke Iwasawa, Yutaka Matsuo, Zhuo Xu, Zichen Jeff Cui.

The authors would like to thank Arielle Bier, Dimple Vijaykumar, Gabriella Pearl, Jane Park, Katie McAtackney, Juanita Bawagan, Eleanor Tomlinson, Dex Hunter-Torricke for their help in creating the content for the blog. We would also like to thank John Guilyard for the amazing animations used for this website. We are thankful to Sanah Choudhry, Michael Griessel, Jon Small for their legal advice. We would like to acknowledge Yuheng Kuang, Ning Hou, Utsav Malla, Sarah Nguyen, Rochelle Dela Cruz, Justice Carbajal, Brianna Zitkovich, Emily Perez, Elio Prado, Jodilyn Peralta, Tran Pham, Deeksha Manjunath, Samuel Wan, Jaspiar Singh and the greater Google DeepMind team for their feedback and contributions.
