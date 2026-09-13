---
title: "BYOL-Explore: Exploration with Bootstrapped Prediction"
source: https://deepmind.google/blog/byol-explore-exploration-with-bootstrapped-prediction/
site: deepmind
date: 2022-06-20
authors: Zhaohan Daniel Guo, Shantanu Thakoor, Miruna Pîslar, Bernardo Avila Pires, Florent Altché, Corentin Tallec, Alaa Saade, Daniele Calandriello, Jean-Bastien Grill, Yunhao Tang, Michal Valko, Rémi Munos, Mohammad Gheshlaghi Azar, Bilal Piot
crawled: 2026-09-13
---

![Split-screen gameplay showing a first-person 3D perspective of a red platform on the left, and a top-down view of a colorful maze-like level layout on the right from a DM-HARD-8 task.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62b068d95af4f802873938ec_throw_across_first_1.gif)

Second-person and top-down views of a BYOL-Explore agent solving Thow-Across level of DM-HARD-8, whereas pure RL and other baseline exploration methods fail to make any progress on Thow-Across.

Curiosity-driven exploration is the active process of seeking new information to enhance the agent’s understanding of its environment. Suppose that the agent has learned a model of the world that can predict future events given the history of past events. The curiosity-driven agent can then use the prediction mismatch of the world model as the intrinsic reward for directing its exploration policy towards seeking new information. As follows, the agent can then use this new information to enhance the world model itself so it can make better predictions. This iterative process can allow the agent to eventually explore every novelty in the world and use this information to build an accurate world model.

Inspired by the successes of [bootstrap your own latent](https://arxiv.org/abs/2006.07733) (BYOL) – which has been applied in [computer vision](https://arxiv.org/abs/2103.16559), [graph representation learning](https://arxiv.org/abs/2102.06514), and [representation learning in RL](https://arxiv.org/abs/2007.05929) – we propose BYOL-Explore: a conceptually simple yet general, curiosity-driven AI agent for solving hard-exploration tasks. BYOL-Explore learns a representation of the world by predicting its own future representation. Then, it uses the prediction-error at the representation level as an intrinsic reward to train a curiosity-driven policy. Therefore, BYOL-Explore learns a world representation, the world dynamics, and a curiosity-driven exploration policy all-together, simply by optimising the prediction error at the representation level.

![Diagram illustrating the BYOL-Explore architecture where a BYOL world representation at an earlier time step predicts a future BYOL representation, with the prediction-error used as an intrinsic reward to train an RL policy.](https://lh3.googleusercontent.com/eh6U_VCPkqhxv9fQhebe9jMV-NqTm5S1eGtTH9KWpG2v2adUWOy8NvTbS5waRkhjL7gS9s4hVvnduLSUEIS4eZO_48KOC7M2BuFAL2ei_ujHeRc284E=w1440)

![A multi-panel animated GIF showing first-person perspectives of an AI agent navigating visually complex 3D environments from the DM-HARD-8 suite, featuring colorful blocks, textured objects, and geometric obstacles.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62b06901690bcc5c64c64fa7_fp_hard_8_1.gif)

Comparison between BYOL-Explore, Random Network Distillation (RND), Intrinsic Curiosity Module (ICM) and pure RL (no intrinsic reward), in terms of mean capped human-normalised score (CHNS).

Despite the simplicity of its design, when applied to the [DM-HARD-8](https://arxiv.org/abs/1909.01387) suite of challenging 3-D, visually complex, and hard exploration tasks, BYOL-Explore outperforms standard curiosity-driven exploration methods such as [Random Network Distillation](https://arxiv.org/abs/1810.12894) (RND) and [Intrinsic Curiosity Module](https://arxiv.org/abs/1705.05363) (ICM), in terms of mean capped human-normalised score (CHNS), measured across all tasks. Remarkably, BYOL-Explore achieved this performance using only a single network concurrently trained across all tasks, whereas prior work was restricted to the single-task setting and could only make meaningful progress on these tasks when provided with human expert demonstrations.

As further evidence of its generality, BYOL-Explore achieves super-human performance in the ten hardest exploration [Atari games](https://arxiv.org/abs/1207.4708), while having a simpler design than other competitive agents, such as [Agent57](https://arxiv.org/abs/2003.13350) and [Go-Explore](https://arxiv.org/abs/2004.12919).

![Line graph comparing the Mean CHNS (Capped Human-Normalized Score) in percentage over learner steps on the DM-HARD-8 suite for BYOL-Explore, BYOL-Explore (big), RND, ICM, and RL. Both BYOL-Explore variants outperform RND, ICM, and standard RL, with BYOL-Explore (big) reaching a 100% mean CHNS.](https://lh3.googleusercontent.com/GIhn_FTvaO-_cY6GhhgHxkmU-8e4xiMNIyWT-w-hqkq-HiRv5_mbOE5K57xddipsHpRVJGBXyuOl3HVO2pv4sUgTmocwn0O0f_3jkuTsgRb_berGqQ=w1440)

Comparison between BYOL-Explore, Random Network Distillation (RND), Intrinsic Curiosity Module (ICM) and pure RL (no intrinsic reward), in terms of mean capped human-normalised score (CHNS).

![Line graph showing Mean CHNS in % over Learner Steps, comparing BYOL-Explore to RND, ICM, and standard RL, with BYOL-Explore significantly outperforming the other methods by reaching a peak of around 70%.](https://lh3.googleusercontent.com/iquw7UVx-hMaTG8ISixsBq6pgYZzY8YVF-cX9HCRZhOhi1lZXYCLQzq2LQRO40gsHC2YIFGNulAmRb9HMTK6kjN9Ig52Iz-VB0-EOALuy0dqMaWsjl8=w1440)

Moving forward, we can generalise BYOL-Explore to highly stochastic environments by learning a probabilistic world model that could be used to generate trajectories of the future events. This could allow the agent to model the possible stochasticity of the environment, avoid stochastic traps, and plan for exploration.
