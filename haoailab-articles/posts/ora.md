---
title: "ORA: Open Robot-Use Agents"
date: 2026-10-15
source: https://haoailab.com/blogs/ora/
crawled: 2026-11-16
---

# ORA: Open Robot-Use Agents

> 原文：[ORA: Open Robot-Use Agents](https://haoailab.com/blogs/ora/) · Hao AI Lab @ UCSD

# ORA: Open Robot-Use Agents

An open robot-use harness that connects open-weight language models to robots.

October 15, 2026 · ORA Team

Table of Contents

* [Introduction](#intro)
  + [Why robot-use agents](#why)
  + [Where ORA fits](#landscape)
* [How ORA works](#method)

  * [Prompt Bundle](#)
  * [Tool Suite20 in this run](#)
  * [Context Management](#)+ [Environment and observation](#sub-env)
  + [Prompt Bundle](#sub-prompt)
  + [Tool Suite](#sub-tools)
  + [Context Management](#sub-context)
* [Results](#results)
  + [RoboTwin](#res-robotwin)
  + [LIBERO](#res-libero)
  + [LIBERO-Pro](#res-pro)
  + [RoboDojo: a first scan](#res-robodojo)
  + [Preliminary results on a real robot](#real)
  + [Cost](#cost)
* [Analysis: what the harness contributes](#analysis)
  + [Learning from experience](#an-learn)
  + [Exact task instructions and success criteria matter](#cs-task)
  + [Perception tools help find and locate objects](#cs-perception)
  + [Exact constants and measurements](#cs-measure)
  + [Explaining refused motions helps recovery](#cs-feedback)
* [Limitations](#limitations)
* [Acknowledgements](#ack)
* [Citation](#citation-sec)
* [References](#references)

[Code](https://github.com/hao-ai-lab/ORA)[Appendix](https://freemty.github.io/ora/appendix/)[Gallery · 153 episodes](https://freemty.github.io/ora/gallery/)

**TL;DR:** ORA is an open robot-use agent harness that lets open-weight language models operate robots **fully zero-shot: no VLA, no robot training and no task-specific memory**, with results on RoboTwin and LIBERO-Pro (69.2% and 81.4% by the official success checks) competitive with agents built on frontier models. It gets there with a harness designed for robot tasks in the physical world: exact task and environment context, tools for perception and motion, and context management.

[![](img/i-aa2245c958ee.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/ora--img--videos--ora-teaser.mp4)

**Figure 1.** DeepSeek-V4.1-Flash, an open-weight model, operating robots through ORA, zero-shot. Estimated model-token cost at DeepSeek's off-peak API rates, using estimated cache hits: $0.13 per solved task on average across the 40 shown here, or $0.30–$0.35 per solved benchmark case including failed attempts. These are API-equivalent estimates, not actual self-hosting costs; GPU and simulator costs are excluded (see [Cost](#cost)).

(a) RoboTwin C2R

50 tasks · 250 cases

Success (%)

0255075100

1. *69.2*ORADeepSeek**ORA + DeepSeek-V4.1-Flash · 69.2%**our harness + open-weight model · no VLA, robot training or task memory173/250 cases succeed; 0 without a valid outcome count as failures.
2. *62.4*GPT-5.5RPent**RPent + GPT-5.5 · 62.4%**RPent harness + language model + VLA + task-specific memoryAs published by RPent; 156/250 reported outcomes.
3. *58.4*Opus-4.7RPent**RPent + Opus-4.7 · 58.4%**RPent harness + language model + VLA + task-specific memoryAs published by RPent; 250 reported cases.
4. *50.4*LingBotVLA**LingBot-VLA · 50.4%**VLA, trained on robot demosAs published by RPent; count not reported.
5. *47.9*π0.5**π0.5 · 47.9%**VLA, trained on robot demosAs published by RPent; count not reported.
6. *20.7*GR00TN1.7**GR00T-N1.7 · 20.7%**VLA, trained on robot demosAs published by RPent; count not reported.

(b) LIBERO-Pro

8 Task and Swap suites · 800 cases

Success (%)

0255075100

1. *81.4*ORADeepSeek**ORA + DeepSeek-V4.1-Flash · 81.4%**our harness + open-weight model · no VLA, robot training or task memory651/800 cases succeed; 0 without a valid outcome count as failures.
2. *92.63*AstraRPent [a]**RPent + GPT-6 Astra [a] · 92.63%**RPent harness + language model + VLA + task-specific memoryAs published by RPent; 741/800 reported outcomes.
3. *82.4*Opus-4.7RPent**RPent + Opus-4.7 · 82.4%**RPent harness + language model + VLA + task-specific memoryAs published by RPent; 800 reported cases.
4. *75.13*GPT-5.5RPent**RPent + GPT-5.5 · 75.13%**RPent harness + language model + VLA + task-specific memoryAs published by RPent; 800 reported cases.
5. *72.63*FlashRPent [b]**RPent Flash Mode [b] · 72.63%**RPent harness + Molmo2-8B + VLA + released task-specific memoryAs published by RPent; 581/800 reported outcomes.
6. *70.63*QwenRPent**RPent + Qwen3.6 27B · 70.63%**RPent harness + open-weight model + VLA + task-specific memoryAs published by RPent; 565/800 reported outcomes.
7. *50.0*πRLinf**π\_RLinf · 50.0%**VLA, robot demos + RLAs published by RPent; count not reported.
8. *11.0*π0.5**π0.5 · 11.0%**VLA, trained on robot demosAs published by RPent; count not reported.
9. *6.3*AtomVLA**AtomVLA · 6.3%**VLA, trained on robot demosAs published by RPent; count not reported.

ORA harness (ours) + open-weight model, zero-shotRPent agent harness + language model + VLA + task-specific memoryVLA policies and other methods

**Figure 2.** Success rates on (a) RoboTwin C2R (250 cases) and (b) LIBERO-Pro (800 cases), using the same case lists as RPent[[1]](#ref-rpent). ORA runs every case zero-shot, with no demonstrations or task-specific memory. Baseline rates come from RPent's leaderboard. [a] Astra uses frozen memory batches. [b] Flash Mode uses released memory and reports the best of ten seeds. Full protocol and values: [appendix](https://freemty.github.io/ora/appendix/).

Evaluation cases and baseline models

RoboTwin C2R (clean-to-randomized) covers 50 tasks with 5 seeds each in randomized scenes. LIBERO-Pro covers eight Task and Swap suites with 10 tasks and 10 seeds each. ORA rates count every case.

RPent combines a language model, VLA and task-specific memory collected in an earlier exploration pass. Models include GPT-5.5, Opus-4.7, GPT-6 Astra and open-weight Qwen3.6-27B[[2]](#ref-qwen36). End-to-end VLA baselines are π0.5[[3]](#ref-openpi), π\_RLinf[[4]](#ref-pirl), GR00T-N1.7[[5]](#ref-gr00t), LingBot-VLA[[6]](#ref-lingbot) and AtomVLA[[7]](#ref-atomvla). RPent Flash Mode uses Molmo2-8B[[8]](#ref-molmo2) with released memory.

These are comparisons of complete systems with different tools, memory and protocols. Rates use official success checks, which can overstate task completion; see [Limitations](#limitations).

## Introduction[#](#intro)

**ORA** is an open robot-use agent harness that enables open-weight models like DeepSeek-V4.1-Flash[[9]](#ref-deepseek) to solve robot tasks ([Figure 3](#fig-tui)). It leads agents built on closed frontier models on RoboTwin and comes close to them on LIBERO-Pro ([Figure 2](#fig-main)). Below we explain why robot use needs agents driven by open models and where **ORA** sits among existing methods.

[![](img/i-cfeb6932ec6e.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/ora--img--videos--ora-tui-C2.mp4)

**Figure 3.** ORA at work on a RoboDojo[[10]](#ref-robodojo) task. Left: the agent's terminal, where the model sees, reasons and calls tools. Right: the robot's cameras. Asked to stack the blocks blue, yellow, orange from the bottom up, the model succeeds in round 2, after round 1 failed. Replayed from the run's records, motion sped up.

### Why robot-use agents[#](#why)

LLM agents now handle much digital work, including coding[[11]](#ref-sweagent) and computer use, as computer-use agents (CUAs)[[12]](#ref-cua)[[13]](#ref-opencua). However, most existing robot policies, such as vision-language-action models (VLAs)[[14]](#ref-rt2)[[15]](#ref-openvla) and world action models (WAMs)[[16]](#ref-dreamzero), still rely on robot-specific training data, collected by teleoperation[[17]](#ref-aloha), with handheld grippers such as UMI[[18]](#ref-umi) or from egocentric videos[[19]](#ref-egomimic). An alternative is to build on the reasoning and tool calling of existing LLM agents. As a recent talk asked: could a strong enough agent operate a robot from its manual alone ([Figure 4](#fig-slide))[[20]](#ref-jwang)?

![Slide: General Robotics? Assume GPT-9.8 + Agentic Control + Any Robot + Its Manual.](img/i-a0a702f44835.jpg)

**Figure 4.** From Jianyuan Wang's talk on general robotics at IMW 2026; credit[[20]](#ref-jwang).

![GPT-6 Astra versus Fable 5.1 on direct robot control: completion rate against API cost, with robot camera views.](img/i-951ff4bc9b55.jpg)

**Figure 5.** Zero-shot direct robot control with GPT-6 Astra; credit[[21]](#ref-chooi).

This suggests bringing the agent loop to the physical world, as in a recent robot-use agent[[22]](#ref-isola): a tool call moves the robot, the model reasons about what it sees, and the next camera frame starts the next turn. Meanwhile, frontier models such as GPT-6 Astra have shown strong zero-shot direct robot control ([Figure 5](#fig-astra))[[21]](#ref-chooi), and several recent demos operate robots this way[[23]](#ref-cpr)[[24]](#ref-robocurve)[[25]](#ref-waddle).

Open-weight models, however, have barely been tested on this, yet robot use needs them for two reasons. First, to understand how well language models manipulate objects and how to improve them, we need large amounts of reproducible data, which means a model we can serve ourselves and experiment with at an acceptable cost, rather than paying frontier-model API prices. Second, a deployed robot system built on an LLM must be fast and efficient enough to run on local hardware. That needs an open model small enough to deploy, and task data that only an open model makes affordable to collect.

### Where **ORA** fits[#](#landscape)

Methods that control robots with learned models fall into four families. They differ in the role of the language model and in how often it makes a decision ([Table 1](#tab-taxo)).

Vision-language-action (VLA) models[[14]](#ref-rt2)[[3]](#ref-openpi)[[15]](#ref-openvla) and, more recently, world action models that also predict future video[[16]](#ref-dreamzero)[[26]](#ref-gigaworld) map camera images and an instruction to actions at every control step and are trained on the largest robot datasets. Because the vision-language backbone is fine-tuned into a visuomotor policy that outputs actions, these systems use little of its ability to reason and act as an agent, for example to measure before moving, plan several steps ahead or change approach after a failure.

A common response is to add a language model as a planner on top of a learned policy, the System 2 / System 1 design[[27]](#ref-saycan)[[28]](#ref-hirobot)[[29]](#ref-helix)[[5]](#ref-gr00t). The language model splits the task into steps and the policy carries them out. In RPent[[1]](#ref-rpent), a language model directs a VLA policy using task-specific memory. The model can also command some motions itself, but most of the manipulation is still done by the VLA, which is trained on robot demonstrations.

A third family has the language model write the policy as code. Code as Policies[[30]](#ref-cap) turns the scene and the task into a program that calls perception and control primitives. CaP-Agent0[[31]](#ref-capx), ASPIRE[[32]](#ref-aspire) and RATs[[33]](#ref-rats) add an agent that runs the program, reads the outcome and revises it; ASPIRE and RATs also keep the skills that work. These methods need no robot demonstrations, and they are economical to run: the model is called once or a few times per task, and the program then runs without it. The price is that the program executes as one or a few open-loop segments. Getting it right often takes trial runs (ASPIRE, for example, learns its skills on separate seeds before it is tested), and between revisions no model looks at the scene: the program reacts only through the checks written into it, which limits how well it carries over to new scenes.

The fourth family runs the agent loop directly, in the ReAct style[[34]](#ref-react): the model reasons, calls a tool, reads the result and decides again. Frontier models have controlled robots this way[[21]](#ref-chooi)[[23]](#ref-cpr), and Guava[[35]](#ref-guava), OpenRUA[[36]](#ref-openrua), Agent as Policy[[37]](#ref-agp) and Robo-Harness K1[[38]](#ref-k1) are harnesses for such agents. When the model issued every low-level command itself, the best model in one study reached 5.5% on LIBERO[[23]](#ref-cpr). **ORA** is in this family. Each tool call covers one bounded motion, which a controller executes, and the model sees the result before its next decision. It costs a model call at every step, so at today’s latencies and prices this family is slower and costlier to run than a program written once (see Cost and Limitations).

| Family | What the language model does | How often it decides | Robot data needed | Examples |
| --- | --- | --- | --- | --- |
| VLA and world action models | is trained into the motor policy | every control step | large robot datasets | RT-2[[14]](#ref-rt2), π0, π0.5[[3]](#ref-openpi), OpenVLA[[15]](#ref-openvla), DreamZero[[16]](#ref-dreamzero) |
| Planner + learned policy (System 2 / System 1) | directs a learned policy step by step | when the policy finishes a step | demonstrations to train the policy | SayCan[[27]](#ref-saycan), Hi Robot[[28]](#ref-hirobot), Helix[[29]](#ref-helix), GR00T N1[[5]](#ref-gr00t), RPent[[1]](#ref-rpent) |
| Code as policy | writes a program over perception and control primitives, runs it and revises it | once or a few times per task | none | Code as Policies[[30]](#ref-cap), CaP-Agent0[[31]](#ref-capx), ASPIRE[[32]](#ref-aspire), RATs[[33]](#ref-rats) |
| Robot-use agent (ReAct loop) | calls a tool, reads the result and decides again | once per tool call | none | Guava[[35]](#ref-guava), OpenRUA[[36]](#ref-openrua), Agent as Policy[[37]](#ref-agp), Robo-Harness K1[[38]](#ref-k1), ORA |

**Table 1.** Four families of methods that control robots with learned models, by the role of the language model and how often it decides. Some systems combine several families.

## How **ORA** works[#](#method)

**ORA** follows the practice of coding agents such as Claude Code[[39]](#ref-claudecode) and Pi[[40]](#ref-pi): the task runs as a ReAct loop[[34]](#ref-react) in which, every turn, the model reads its input, thinks and makes one tool call; the action changes the state of the world, and what comes back becomes the next turn’s input ([Figure 6](#fig-system)). Like those agents, it has a prompt bundle, tools and context management, but for a robot each has to do more.

First, the **prompt bundle** has to describe the body of each embodiment and the task: the robot’s frames, the point each command moves, the gripper’s constants, and the task’s success criteria written out in detail. Second, the **tool suite** has to help the model sense and act in the physical environment. In place of a shell and file reads and writes, the model sees the world only through cameras and the robot’s sensors, so it needs perception tools that measure the real scene and action tools that act on the environment and report, after every action, exactly what happened. Third, compared with a coding agent, a robot-use agent receives a large volume of redundant visual observations and environment data, so **context management** has to carry much heavier input: every turn adds camera images, and the model keeps returning to earlier results. The input must stay small without losing those results or breaking the prompt cache.

On the other side is the environment: a supervisor checks every motion against the robot’s limits, runs it and returns a measured receipt. Throughout, the model perceives the scene only through RGB and depth images and never sees privileged information from the simulator: the success check’s code, object ground truth or simulator contacts.

**DeepSeek-V4.1-Flash**open weights

ORAthe harness

##### Prompt Bundle

system policyevidence rulesbenchmarkrobot cardtasktool schemasround facts

##### Tool Suite*20 in this run*

lookvision\_groundfind by namevision\_segmentmask at pointsmark\_pointpixel → world

measuregeometry\_querycamera ↔ worldcomputevector mathgrasp\_plangrasp proposals

actmove\_posemove to a poseset\_gripperopen or closegrasp\_executerun a grasp

also

observealign\_planmove\_torotate\_wristrotate\_pitchrecover\_posewait\_tickscheck\_taskfinish\_episodereport\_issueartifact\_read

##### Context Management

this turnobservation and receipt, in fullrecent turnsword for wordolder turnsimages → referenceshistory summaryfinished rounds → checkpoints

action

every turn

observation

trust boundary

Environment

diverse embodiments

![](img/i-92d8ba334676.jpg)ARX X5RoboDojo · two arms![](img/i-5346794e6840.jpg)ALOHARoboTwin · two arms![](img/i-f5475c341b45.jpg)FrankaLIBERO · one arm

![](img/i-6f0c8af3c62f.jpg)![](img/i-1935b668ab81.jpg)**observation**RGB-D, robot state, receiptsuccess check

**Figure 6.** The interaction loop between the LLM, ORA and the environment. Every turn, the model reads the prompt bundle and the context, thinks, and calls one tool; an action changes the world, and the observation that comes back, like every tool result, joins the context for the next turn. The prompt bundle and the context, rebuilt every turn with the newest material first, make up everything the model receives; on the other side, the environment holds the robots, returns an observation every turn and keeps the success check. Click any part to see it in detail.

### Environment and observation[#](#sub-env)

We run **ORA** on three simulated benchmarks, each with its own robot ([Figure 7](#fig-cards)). They differ in the simulator and its world frame, the arms, the point each command moves, the gripper’s geometry, the cameras and how success is judged. RoboDojo[[10]](#ref-robodojo) runs on Isaac Sim[[41]](#ref-isaacsim) with a two-arm ARX X5; RoboTwin[[42]](#ref-robotwin) runs on SAPIEN[[43]](#ref-sapien) with a two-arm ALOHA; LIBERO[[44]](#ref-libero) and LIBERO-Pro[[45]](#ref-liberopro) run on MuJoCo[[46]](#ref-mujoco) through robosuite[[47]](#ref-robosuite) with a one-arm Franka.

The loop, the kinds of tools and the model are shared; only the controllers are fitted to each robot. What differs reaches the model as text, through a benchmark boundary and a robot card. With these, one model runs all three robots. The card and the boundary give the agent the details of the body and the scene it needs to reason with, such as the point each command moves, where the fingers touch and how wide the jaws open; open a card below for them.

![](img/i-92d8ba334676.jpg)ARX X5RoboDojoFixed-base ARX X5: left 6-DoF arm, right 6-DoF arm; parallel-jaw grippers. Cameras: `head` fixed RGB-D; `left_wrist`, `right_wrist` moving RGB-D.

|  |  |
| --- | --- |
| Simulator | Isaac Sim[[41]](#ref-isaacsim) |
| Tasks we ran | 42 multi-stage tabletop tasks, a first scan |
| Robot | ARX X5, two 6-DoF arms |
| Point a command moves | wrist flange; add no offset |
| Approach / jaw-closing axis | [1, 0, 0] / [0, 1, 0] |
| Where the fingers touch | jaw contact centre 0.150 m along the approach |
| Full jaw opening | 88.8 mm |
| Cameras | one fixed, one on each wrist; 640 × 480 |
| Official success | the benchmark's reward manager |

![](img/i-5346794e6840.jpg)ALOHARoboTwinFixed-base ALOHA-AgileX: left 6-DoF arm, right 6-DoF arm; parallel-jaw grippers. `right_tcp` is the controlled reference, 0.12 m from the flange; commands already target it.

|  |  |
| --- | --- |
| Simulator | SAPIEN[[43]](#ref-sapien) |
| Tasks we ran | 50 tasks, 5 randomized scenes each |
| Robot | ALOHA-AgileX, two 6-DoF arms |
| Point a command moves | tool point 0.12 m beyond the flange |
| Approach / jaw-closing axis | [1, 0, 0] / [0, 1, 0] |
| Where the fingers touch | fingers from −50 to 36 mm around the tool point |
| Full jaw opening | 94.9 mm, given in the `grasp_plan` help |
| Cameras | two fixed, one on each wrist; 320 × 240 |
| Official success | the task's `check_success` |

![](img/i-f5475c341b45.jpg)FrankaLIBERO / LIBERO-ProFixed-base Franka Panda: right 7-DoF arm; parallel-jaw grippers. `right_grip_site` is the controlled reference, 0.097 m from the end-effector root; commands already target it.

|  |  |
| --- | --- |
| Simulator | MuJoCo[[46]](#ref-mujoco) (robosuite[[47]](#ref-robosuite)) |
| Tasks we ran | 40 tasks × 10 seeds; LIBERO-Pro 8 suites × 100 |
| Robot | Franka Panda, one 7-DoF arm |
| Point a command moves | grip site 0.097 m beyond the end-effector root |
| Approach / jaw-closing axis | [0, 0, 1] / [1, 0, 0] |
| Where the fingers touch | fingers from −44 to 9 mm around the grip site |
| Full jaw opening | 80 mm |
| Cameras | one fixed, one on the wrist; 256 × 256 |
| Official success | the environment's termination signal |

**Figure 7.** The three embodiments and the opening of each robot card, verbatim. Open a card for what it and the benchmark boundary tell the model; the model never sees the success code, only its yes or no.

After every action, the environment returns an observation ([Figure 8](#fig-obs)). It holds an RGB image from each camera with its calibration, the measured pose and gripper of each arm, the receipt of the last action and the remaining budget, and it is paired with the observation the action was chosen from, so the model can compare before and after. Each camera’s depth image is stored with the observation, and the looking tools read it when the model measures.

![head camera, RGB](img/i-6f0c8af3c62f.jpg)

head camera, RGB

![left wrist, RGB](img/i-5fd3ef09ae94.jpg)

left wrist, RGB

![right wrist, RGB](img/i-9147403366f2.jpg)

right wrist, RGB

![head camera, depth](img/i-1935b668ab81.jpg)

head camera, depth

The package, as the model received it (shortened)

* comparison
  + action\_input\_actual\_sequence7
  + action\_result\_actual\_sequence8
  + availabletrue
  + instruction"Compare the retained ACTION INPUT ACTUAL with this ACTION RESULT ACTUAL before choosing the next tool."
* current\_actual
  + observation\_step8
  + camera\_geometry
    - left\_wrist…
    - right\_wrist…
  + public\_robot\_facts
    - end\_effectors
      * right
        + pose\_xyz\_xyzw[0.001, -0.141, 0.934, -0.348, 0.619, 0.328, 0.623]
        + axes
          - approach\_world[0.018, -0.023, -1.0]
          - closing\_world[-0.84, 0.542, -0.028]
        + gripper
          - command\_target"close"
          - measured\_opening\_normalized0.51
      * left
        + pose\_xyz\_xyzw[-0.358, -0.131, 1.09, -0.402, 0.581, 0.403, 0.582]
        + axes…
        + gripper…
    - cameras…
* last\_action\_effect
  + action"move\_pose"
  + action\_summary"right arm 1.6 mm / 0.6° from target, reached, TCP moved 163 mm"
  + detail…
* remaining\_budget
  + native\_actions\_remaining352
  + native\_actions\_limit400
  + robot\_decisions75
  + model\_calls185
* images
  + "ACTION RESULT ACTUAL · sequence 8 · head"
  + "ACTION RESULT ACTUAL · sequence 8 · left\_wrist"
  + "ACTION RESULT ACTUAL · sequence 8 · right\_wrist"

**Figure 8.** One observation on RoboDojo, from the run of [Figure 3](#fig-tui), round 1, step 8: the three camera images the model receives, the head camera's depth image, which the looking tools read, and the package that comes with them.

### Prompt Bundle[#](#sub-prompt)

A coding agent reads the repository and its instructions before it edits anything; a robot-use agent likewise has to be told enough about its environment before it moves. We therefore give it a prompt bundle of seven layers ([Figure 6](#fig-system)). A new embodiment therefore needs no training: only the embodiment context is replaced. Open any layer to read it as the model did in the run of [Figure 3](#fig-tui).

1. **System policy**, the same for every robot and task: the turn protocol (read-only calls may be batched; a call that changes the world stands alone), every derived number goes to `compute`, how older evidence is replaced by references, and what the budgets mean.

   System message, Native Robot Policy v4, excerpt

   ```
   Turn protocol

   Read-only tools may be called sequentially or in one independent batch. A
   world-mutating tool must be the only tool call in its assistant response. Each
   accepted mutation ends the current turn; wait for the next actual observation
   before choosing another mutation.

   Arithmetic belongs in the advertised calculation capability, not in your own
   working. Whenever a number would be derived -- a residual, an offset along a
   direction, a quaternion unpacked, a sum of extents, a dot or cross product, a
   projection between image and world, a trigonometric value -- that derivation is
   part of how the action was chosen […]

   How this context reaches you

   Current actual evidence arrives complete on every turn. Earlier evidence is not
   guaranteed to stay in the form you first received it.

   A result that exceeds its inline budget is replaced by a status record carrying
   an exact reference to the complete original. […] Open the reference when you
   need what a past result said; call again when you need what is true now.

   What the reported allowances mean

   Every turn reports what remains of the current session round […]: accepted world
   mutations, model turns including read-only ones, and elapsed wall-clock seconds.
   […] keep enough in hand to witness the effect of your final mutation and to take
   the advertised closing step: an unverified last action and an unclosed episode
   are both worse than one attempt fewer.
   ```

   Verbatim from the prompt; […] marks a cut.
2. **Evidence rules**, also shared: keep direct evidence, inferences, candidates, executed commands and verified effects apart; after a failure, change what the next attempt rests on.

   Evidence-to-Action Invariants v5, excerpt

   ```
   Keep these states distinct:

   - **Direct evidence:** present in a current image, measurement or tool result.
   - **Inferred:** a task-relevant interpretation supported by observations.
   - **Candidate:** a proposed point, pose or action that has not executed.
   - **Executed:** a command the Runtime accepted and attempted.
   - **Verified:** a physical effect confirmed by a later observation.
   […]
   When something fails

   A refusal, an error or an unchanged world is evidence about the approach, not
   only about the tool. Before repeating anything, change what the attempt rests
   on: refresh the evidence its arguments came from, or take a different route to
   the same effect. An identical call against an unchanged premise is not a
   recovery, and when two attempts fail the same way the premise is what to test.
   ```

   Verbatim from the prompt; […] marks a cut.
3. **Benchmark boundary**, one per benchmark: the world frame and units, the table, the cameras, what stays private and where the official verdict comes from.

   RoboDojo environment boundary, excerpt

   ```
   The scene is a simulated Isaac Sim tabletop in an episode-local world frame:
   `+X` (red), `+Y` (green) and `+Z` (blue), `+Z` upward, positions in metres.
   One 1.4 m by 1.1 m table stands with its top near z = 0.76 m (table body
   centred at z = 0.74 m). The robot is mounted on the table's `-Y` side, so
   `+Y` runs from the robot toward the far edge. […]

   Simulator object and actor state, ground-truth poses, segmentation, contacts,
   evaluator objects, reward internals, the success-predicate implementation,
   task source and the teleoperated source demonstrations are private and
   unavailable.

   Only RoboDojo's reward manager supplies the official Boolean verdict,
   read through the advertised verdict query at a valid state boundary […]
   Every robot command reserves up to a fixed number of native actions (20) from
   that allowance; the receipt reports how many were consumed, and a refused
   command consumes none.
   ```

   Verbatim from the prompt; […] marks a cut.
4. **Robot card**, one per robot: the arms, the point each command moves, the gripper's axes and constants, and the cameras ([Figure 7](#fig-cards)).

   ARX X5 robot card, excerpt

   ```
   Identity and topology
   Fixed-base ARX X5: left 6-DoF arm, right 6-DoF arm; parallel-jaw grippers.

   Controlled points
   `left_link6` is the left arm's controlled point, its wrist flange, not a fingertip;
   commands and measured poses already refer to it, so add no offset. […]

   End-effector axes
   `left_link6` local approach [1, 0, 0]; jaw-closing line [0, 1, 0]. Local Z is
   perpendicular to both. Current world directions are supplied with measured state.

   Gripper semantics
   […] The jaw contact centre is +0.1501 m along the approach axis from `left_link6`. […]
   Nominal full-open pad separation is 88.8 mm. Physical pad aperture remains
   uncalibrated. The public encoder reading is the mean of both finger joints on the
   normalized command scale (empty-close reference about 0.185, full-open 1); it is
   not measured pad separation […]

   Sensors and cameras
   `head`: fixed RGB-D; use calibration from the same observation.
   `left_wrist`: arm-mounted moving RGB-D; use calibration from the same observation.
   `right_wrist`: arm-mounted moving RGB-D; use calibration from the same observation.
   ```

   Verbatim from the prompt; […] marks a cut.
5. **Task and completion contract**, one per task: the benchmark's own instruction, copied unchanged, and a contract that restates the official success criteria in plain words.

   Task message, RoboDojo stack\_blocks\_by\_language, excerpt

   ```
   stack the blocks from bottom to top in the order ofblue, yellow, and orange, then reset the robot arm.

   That sentence is the objective, in its exact words. […]

   Public completion contract for this task:

   - The three blocks must end up in one stack in the colour order the instruction
     gives, read from the bottom up: the first colour named at the bottom, the
     second in the middle and the third on top.
   - Each block must sit on top of the block below it, centred over it rather than
     set off toward one side or placed beside it.
   - Both arms must be back at the poses they held when the episode reset, at the
     same instant that everything else in this contract is true.
   ```

   Verbatim from the prompt; […] marks a cut.
6. **Tool schemas**, for each tool, when to use it, what it changes and returns, what it does not do and how it refuses.

   One of 20 schemas: vision\_ground, shortened

   ```
   {"name": "vision_ground",
    "description": "Retrieve up to three inspectable text-grounded target proposals from one selected
     current RGB-D camera. Use when: task language names an object or part and the scene-level search
     space should be reduced before the policy makes its own identity decision […] Treat the returned
     set as recall-oriented proposals: top rank and backend score are within-call ordering signals, not
     an oracle. […] Does not: choose the correct candidate, guarantee that rank 0 is foreground, combine
     cameras, expose object ground truth […] On error: Refused: max_candidates outside 1 to 3 […]",
    "parameters": {"camera": {"enum": ["head", "left_wrist", "right_wrist"]},
                   "text": {"type": "string", "maxLength": 120,
                            "description": "Short visible object or part description, never a simulator identifier."},
                   "max_candidates": {"minimum": 1, "maximum": 3, "default": 3}}}
   ```

   Verbatim from the prompt; […] marks a cut.
7. **Round facts**, once per round: the budgets, the first camera images, and what stays fixed within the round, such as fixed-camera calibration.

   First observation and round static facts, round 1, shortened

   ```
   {"session_round": {"kind": "session_round_start", "round": 1, "total_rounds": 3, "budget_scope": "per_round",
      "instruction": "This is a new independent environment round in the same AgentSession. […] Prior scene state
      and coordinates are stale. Re-ground from the current observation and retain useful experience."},
    "remaining_budget": {"model_calls": 200, "robot_decisions": 80, "native_actions_remaining": 400,
      "native_actions_limit": 400, "wall_time_s": 21091.7}, …}
   INITIAL ACTUAL · sequence 0 · head / left_wrist / right_wrist          [three images, 640×480]

   {"round_static_facts": {"current_actual": {
      "camera_geometry": {"head": {"intrinsic_cv": [[288.13, 0.0, 320.0], [0.0, 288.13, 240.0], [0.0, 0.0, 1.0]],
          "camera_origin_world_m": [0.0, -0.41, 1.308], "extrinsic_cv": […]}, "left_wrist": {…}, "right_wrist": {…}},
      "conventions": {"camera_coordinates": "OpenCV: x right, y down, z forward", "depth_unit": "metres", …},
      "view_dimensions": {"head": {"width": 640, "height": 480}, …}, "depth_delivery": "on_demand", …},
    "rule": "An observation in this round leaves out each current_actual field whose current value is
      byte-identical to its value here. […]"}}
   ```

   Verbatim from the prompt; […] marks a cut.

The bundle says how to look and move. It never contains a solution, object coordinates or the success test. Three of its layers are specific to a robot task: the robot card, the task instruction copied unchanged from the benchmark, and the completion contract. See the [Analysis](#analysis) for the role of these components.

### Tool Suite[#](#sub-tools)

Each tool covers something the model cannot do reliably on its own ([Figure 9](#fig-toolbox)). The model sees only what the tools measure.

look`vision_ground`find by name`vision_segment`mask at points`mark_point`pixel → world`observe`reopen or overlay images

measure`geometry_query`camera ↔ world`compute`vector math`grasp_plan`grasp proposals`align_plan`reachable standoff poses

act`move_pose`move to a pose`set_gripper`open or close`grasp_execute`run a grasp`move_to`move, keep orientation`rotate_wrist`turn the jaw line`rotate_pitch`tilt the approach`recover_pose`return to a named pose`wait_ticks`let time pass

episode`check_task`ask for the official verdict`finish_episode`end the round with a reason`report_issue`report an interface defect`artifact_read`reopen a stored result

**Figure 9.** The 20 tools of the run in [Figure 3](#fig-tui), by what they do. Click a tool for its schema, a real call and what came back.

A language model can name what it sees but cannot point at it precisely, the reference gap DeepSeek describes[[48]](#ref-dsvp). The looking tools narrow it: `vision_ground` and `vision_segment` return SAM 3[[49]](#ref-sam3) masks for a named object or a few pointed pixels, `mark_point` measures single pixels, and each is looked up in depth, so the model gets positions in metres ([Figure 10](#fig-tools)).

`vision_ground`find an object by name · LIBERO-Pro

![Three candidate bottles boxed in the LIBERO-Pro scene](img/i-37ff636e06eb.jpg)

`vision_ground(camera="agentview", text="ketchup bottle")`

Three candidate bottles, each with a mask and a centre measured from depth. The top two scores are close (0.69 and 0.67), so the ranking alone does not settle which bottle is the ketchup; the model compares the close-ups before it grasps.

`vision_segment`mask what the model points at · RoboDojo

![One pointed pixel on the wrist view and the mask of the yellow block](img/i-e2a03f31930e.jpg)

`vision_segment(camera="left_wrist", points_uv=[[215, 412]])`

One mask covering the yellow block: centre (−0.355, −0.142, 0.800) m, 36 × 37 mm, 35 mm above a surface at 0.765 m. A point the model chose on the head view a turn earlier had landed on the table.

`mark_point`measure single pixels · RoboTwin

![Eight named points marked along the shoe on the RoboTwin head camera](img/i-6d2332ebe320.jpg)

`mark_point(view="head_camera", point_ids=["shoe_a", …, "shoe_h"], …)`

The world positions of eight points along the shoe, all solved from depth, which give its length and heading on the table before the grasp is planned.

`grasp_plan`propose grasps the arm can reach · LIBERO-Pro

![Three grasp candidates drawn on the chosen bottle](img/i-38557051eb8c.jpg)

`grasp_plan(target_ref="target-dade139…", max_candidates=3)`

Three grasps on the chosen bottle from Contact-GraspNet, each with a 40.7 mm jaw opening for the Franka gripper, and all reachable.

**Figure 10.** Four tool calls on LIBERO-Pro, RoboDojo and RoboTwin, each with the image it returned to the model and the numbers that came back. Click a tool in [Figure 6](#fig-system) for more calls from the run of [Figure 3](#fig-tui).

The model also does geometry in its reasoning, sometimes wrongly: 12.2% of 35,270 responses derived vectors or rotations by hand, and three runs pointed the gripper up when they meant to approach from above. `compute` takes that arithmetic over, and a pose can be given as directions, such as approach straight down.

Motion tools take a target for the controlled point, never joints. The environment solves inverse kinematics and plans the path with cuRobo[[50]](#ref-curobo), runs it and returns a receipt; a refusal says why, for instance that the straight path is reachable for only 75% of the way. `grasp_plan` proposes grasps with Contact-GraspNet[[51]](#ref-cgn), and `grasp_execute` runs one as a single supervised sequence.

`check_task` returns the official yes or no, `finish_episode` ends a round early when a mistake cannot be undone, and `report_issue` lets the model flag a fault in the harness rather than in its own attempt.

See the [Analysis](#analysis) for the role of these components.

### Context Management[#](#sub-context)

A coding agent’s turn adds a few lines of text; a robot’s turn adds three camera images, measured poses and a receipt. Context management has to balance three goals that pull against each other. The input must stay short. Every earlier result must stay recoverable exactly, because the model often needs a number from many turns back: when we cut each observation to about half its length, rounding numbers and dropping limits, RoboDojo success fell from 17 to 10 of 27 rounds. And the start of the input must stay stable, so that the server’s prompt cache keeps hitting, while every reduction breaks it.

**ORA** keeps the input in four layers, newest first ([Figure 6](#fig-system)). Open any layer to see it as the model received it.

1. **This turn** arrives in full: the receipt of the last action, all three camera images, the measured poses and grippers, and the remaining budget, paired with the observation the action was chosen from.

   One observation from round 1, shortened

   * comparison
     + action\_input\_actual\_sequence7
     + action\_result\_actual\_sequence8
     + availabletrue
     + instruction"Compare the retained ACTION INPUT ACTUAL with this ACTION RESULT ACTUAL before choosing the next tool."
   * current\_actual
     + observation\_step8
     + camera\_geometry
       - left\_wrist…
       - right\_wrist…
     + public\_robot\_facts
       - end\_effectors
         * right
           + pose\_xyz\_xyzw[0.001, -0.141, 0.934, -0.348, 0.619, 0.328, 0.623]
           + axes
             - approach\_world[0.018, -0.023, -1.0]
             - closing\_world[-0.84, 0.542, -0.028]
           + gripper
             - command\_target"close"
             - measured\_opening\_normalized0.51
         * left
           + pose\_xyz\_xyzw[-0.358, -0.131, 1.09, -0.402, 0.581, 0.403, 0.582]
           + axes…
           + gripper…
       - cameras…
   * last\_action\_effect
     + action"move\_pose"
     + action\_summary"right arm 1.6 mm / 0.6° from target, reached, TCP moved 163 mm"
     + detail…
   * remaining\_budget
     + native\_actions\_remaining352
     + native\_actions\_limit400
     + robot\_decisions75
     + model\_calls185
   * images
     + "ACTION RESULT ACTUAL · sequence 8 · head"
     + "ACTION RESULT ACTUAL · sequence 8 · left\_wrist"
     + "ACTION RESULT ACTUAL · sequence 8 · right\_wrist"

   From the run's own records; … marks a cut.
2. **Recent turns** stay word for word: the images of the two most recent action steps stay inline, and the exact results of the last three.

   Round 2's first exchange, still word for word at turn 30, shortened

   ```
   assistant: Round 2. Key lesson from round 1: after releasing a block, retract straight up before any lateral motion, and verify build-spot reachability both arms can satisfy. The layout is the same. Let me re-localize the blue block.

   tool (vision_segment): {"camera": "head", "candidate_previews": [{"crop_xyxy": [316, 209, 400, 293], "image_index": 1, "position": 0, …}], "candidates": [{"backend_score": 0.973, "candidate_id": "T0", "localization": {"center_xyz_m": [0.075, -0.140, 0.800], "extent_xyz_m": [0.039, 0.040, 0.033], …}}]}

   [two returned images, as references]
   ```

   From the run's own records; … marks a cut.
3. **Older turns** keep their text, but every fourth action step their images, and any result over 50 KB, are replaced by exact references; `observe` or `artifact_read` reopens the bytes, and a large result keeps a 2 KB preview.

   Round 1's first camera images, as references at turn 14

   ```
   INITIAL ACTUAL · sequence 0 · head · latest at this message <recoverable_artifact>{"at":[1,0],"bytes":409641,"mime":"image/png","open":"observe","ref":"artifact://…/d663528e…","v":1}</recoverable_artifact>
   INITIAL ACTUAL · sequence 0 · left_wrist · latest at this message <recoverable_artifact>{"at":[1,0],"bytes":353088,"mime":"image/png","open":"observe","ref":"artifact://…/6fc7c0b4…","v":1}</recoverable_artifact>
   …
   ```

   From the run's own records; … marks a cut.
4. **History summary** takes over once the input passes about 150,000 tokens: the same model folds a completed round into one record, aimed at about 1,200 tokens, with the official result, what it learned and a reference to the exact transcript. If the input still reached 80% of the model's window, the oldest material would be compacted to 65%, as in Claude Code[[39]](#ref-claudecode).

   Round 1's checkpoint, as read from turn 31 on, shortened

   * coverage
     + action\_step\_count13
     + from\_action\_step\_index0
     + through\_action\_step\_index12
   * official\_verdict
     + round1
     + passedfalse
     + instruction"This completed-round result is exact. Reflect on durable task-local lessons."
   * summary
     + confirmed\_facts
       - "Right-wrist measurement of the stranded block, re-projected into the head view, was self-consistent and placed it well beyond the table's far edge …"
     + current\_constraints
       - "The stranded block is beyond the table's far edge and outside the commanded workspace, so neither arm can retrieve it; …"
     + failed\_attempts
       - * failure"Right-arm retraction after releasing the block displaced the block instead of leaving it in place."
         * evidence"After the clearing move the block was absent from the drop point and later measured beyond the far table edge."
         * correction"Clear with a short upward move first and re-observe, rather than a long diagonal retraction past the release point."
       - …
     + do\_not\_repeat
       - "Do not resubmit world targets that already returned planner\_failed for the same arm without changing standoff, height or arm."
       - …
     + invalidated\_beliefs…
     + re\_ground\_next…
   * exact\_transcript
     + bytes228007
     + open
       - tool"artifact\_read"
       - arguments
         * ref"artifact://…/26c825a2…"

   From the run's own records; … marks a cut.

To see the three goals at work, [Figure 11](#fig-loop) follows one long session: the RoboDojo block-stacking task of [Figure 3](#fig-tui), played three times in a row on the same scene, 123 turns in all.

The input stays short. In round 1 the input grew from 33k to 162k tokens, and at turns 14 and 18 the images of older steps became references. Round 2 began with round 1 still word for word; at 180k tokens, before turn 31, the model folded round 1 into a checkpoint, with its official result, a summary of facts, constraints, failed attempts and what not to repeat, and a reference to the 228 KB transcript. The input fell to 59k. Only completed rounds are folded, so round 2, which ran 65 turns, grew to 253k tokens with its older images turned into references nine times; it was folded the same way before turn 96, from 261k to 58k, and round 3 finished in 33 turns.

Nothing is lost. Every image or result that leaves the input becomes a reference to the exact stored bytes, which `observe` or `artifact_read` reopens. In the 250 RoboTwin cases, the model reopened earlier evidence 65 times, in 30 cases. In one, its left gripper had just clamped one handle of a pot; to plan the right handle, it read back the full `grasp_plan` result whose inline preview had been cut, 7,965 bytes of JSON, page by page.

The prefix stays stable. Between reductions, each request extends the previous one byte for byte, so the server can reuse its cache. In this session, 104 of the 122 later requests extended the previous one; the other 18 followed a reduction or opened a round, and they account for 82% of the uncached input. The estimated cache hit rate over the session was 86%, as in the evaluation runs (see Cost).

Round 125 turns · failed

Round 265 turns · success

Round 333 turns · success

checkpoint, a completed round folded (turns 31, 96)older images replaced by references (turns 14, 18, 32, 39, 48, 55, 65, 71, 75, 81, 85, 101, 107, 111, 117, 122)

One bar per turn, its height the provider-reported input tokens. Choose any turn, or one of these:

**1**segment the blocks**3**grasp yellow**6**move refused**7**switch arms**17**retract sideways**24**find the lost block**25**give up**26**lesson from round 1**31**checkpoint**89**verdict**91**round 3 reuses round 2**96**second checkpoint**122**verdict, round 3

**1**Read

prompt 18k charsround facts 11k charsearlier turns 33k charsnew this turn 8.0k chars

64k input tokens · 17 images inline

The receipt of the lift (4.8 mm from target, reached, moved 126 mm) and three fresh camera images.

**2**Think

> “Lift succeeded; the block is still held. Now translating horizontally above the blue block.”

**3**Act

`move_pose(`

|  |  |
| --- | --- |
| targets | * left   + interaction"free\_space"   + orientation\_mode"hold\_current"   + position\_m[0.075, -0.14, 1.09]   + position\_mode"absolute" |

`)`

**4**Result

Refused by the planner, nothing moved: the target above the blue block is 434 mm away, the straight path is reachable for 75% of the way, and the nearest reachable orientation tilts the gripper 15° from straight down.

*next turn*

**turn 6**

**Figure 11.** The loop that runs every turn, on the run in Figure 3: the model reads its input, reasons, makes a call, and the result becomes part of the next turn's input. Choose any of the 123 turns on the timeline. Dark bars mark the two checkpoints, where a completed round was folded into one record; dots mark the turns where older images had just been replaced by references. Read says what changed before the turn. Its stacked bar measures text characters, excluding image content, on a shared 400k-character scale: the prompt, round facts, earlier turns and new evidence. The timeline and input-token total use provider-reported tokens. Character counts and token counts are different units.

## Results[#](#results)

[Table 2](#tab-summary) repeats the main comparison. Every **ORA** run uses DeepSeek-V4.1-Flash zero-shot, with one attempt per case (one task with one seed), on the case lists of RPent[[1]](#ref-rpent); every rate counts all planned cases. **ORA**’s model may call the success check, which we have not confirmed for the RPent agents, so these compare complete systems rather than models.

| Success % | RoboTwin | LIBERO-Pro | LIBERO |
| --- | --- | --- | --- |
| ORA + DeepSeek-V4.1-Flashopen-weight model, zero-shot, no VLA | **69.2** | **81.4** | **83.5** |
| RPent + GPT-6 Astralanguage model + VLA + task-specific memory | — | 92.6 | — |
| RPent + Opus-4.7language model + VLA + task-specific memory | 58.4 | 82.4 | 96.0 |
| RPent + GPT-5.5language model + VLA + task-specific memory | 62.4 | 75.1 | — |
| Best end-to-end VLALingBot-VLA · π\_RLinf · AtomVLA | 50.4 | 50.0 | 97.0 |

**Table 2.** The comparison of [Figure 2](#fig-main) across the three benchmarks. Other rows come from the RPent leaderboard[[1]](#ref-rpent); — means not reported. The best VLA is a different policy on each benchmark: LingBot-VLA[[6]](#ref-lingbot), π\_RLinf[[4]](#ref-pirl) and AtomVLA[[7]](#ref-atomvla).

### RoboTwin[#](#res-robotwin)

**ORA** leads on RoboTwin[[42]](#ref-robotwin), where all 250 cases use randomized scenes and we ran no pass on the clean ones; the RPent agents explore the clean scenes first to collect task memory. Its failures cluster ([Table 3](#tab-rtspread)): 31 of the 50 tasks are solved in at least four of five seeds, while eight tasks solved at most once account for 36 of the 77 failures. Most of these need both arms to work together or several objects moved in turn.

| Seeds solved | Tasks | RoboTwin tasks |
| --- | --- | --- |
| 5 of 5 | 16 | blocks ranking rgb, click alarmclock, click bell, grab roller, move playingcard away, move stapler pad, open microwave, place a2b left, place a2b right, place burger fries, place mouse pad, place object stand, press stapler, shake bottle, shake bottle horizontally, stack bowls two |
| 4 of 5 | 15 | adjust bottle, beat block hammer, blocks ranking size, handover mic, lift pot, move pillbottle pad, open laptop, place container plate, place empty cup, place object basket, place object scale, put object cabinet, rotate qrcode, stack blocks two, turn switch |
| 3 of 5 | 7 | pick dual bottles, place bread basket, place cans plasticbox, place fan, place shoe, stack blocks three, stamp seal |
| 2 of 5 | 4 | pick diverse bottles, place bread skillet, place phone stand, stack bowls three |
| 1 of 5 | 4 | dump bin bigbin, handover block, move can pot, place can basket |
| 0 of 5 | 4 | hanging mug, place dual shoes, put bottles dustbin, scan object |

**Table 3.** RoboTwin tasks grouped by how many of their five seeds ORA solved, 250 cases in all.

### LIBERO[#](#res-libero)

On standard LIBERO[[44]](#ref-libero), **ORA** is below the VLA policies trained on LIBERO’s own demonstrations. It is close on Spatial and Object (95% and 92%) and falls behind on Goal (84%) and Long (63%), whose tasks mostly chain two subtasks ([Table 4](#tab-libero)).

| LIBERO, success % | Spatial | Object | Goal | Long | Overall |
| --- | --- | --- | --- | --- | --- |
| ORA + DeepSeek-V4.1-Flashour harness + open-weight model · no VLA, robot training or task memory | 95.0 | 92.0 | 84.0 | 63.0 | **83.5** |
| AtomVLA[[7]](#ref-atomvla)VLA, trained on robot demos | 96.4 | 99.6 | 97.6 | 94.4 | **97.0** |
| RPent + Opus-4.7[[1]](#ref-rpent)RPent harness + language model + VLA + task-specific memory | 97.0 | 100.0 | 94.0 | 93.0 | **96.0** |
| π\_RLinf[[4]](#ref-pirl)VLA, robot demos + RL | 99.0 | 96.0 | 97.0 | 89.0 | **95.3** |
| π0[[3]](#ref-openpi)VLA, trained on robot demos | 96.8 | 98.8 | 95.8 | 85.2 | **94.2** |
| NORA[[52]](#ref-nora)VLA, trained on robot demos | 85.6 | 89.4 | 80.0 | 63.0 | **79.5** |
| OpenVLA[[15]](#ref-openvla)VLA, trained on robot demos | 84.7 | 88.4 | 79.2 | 53.7 | **76.5** |

**Table 4.** Success rates (%) on standard LIBERO by suite: 4 suites, 10 tasks each, 10 seeds per task. RPent and VLA rows are taken from the RPent leaderboard. Versions, infrastructure replacements and protocol differences are in the [appendix](https://freemty.github.io/ora/appendix/).

### LIBERO-Pro[#](#res-pro)

LIBERO-Pro[[45]](#ref-liberopro) changes the task (Task suites) or moves the objects (Swap suites). **ORA** loses only two points against LIBERO and solves about as many Swap cases as Task cases (331 and 320 of 400), while VLA policies trained on LIBERO drop sharply: π\_RLinf falls from 95.3% to 50.0% and AtomVLA from 97.0% to 6.3% ([Table 5](#tab-pro)). On the six suites that agents writing robot code report, **ORA** averages 89.2%, against 71.7% for ASPIRE[[32]](#ref-aspire), 43.8% for RATs[[33]](#ref-rats) and 18.2% for CaP-Agent0[[31]](#ref-capx), under different protocols. OpenRUA[[36]](#ref-openrua) reports 87.0% with Claude Opus 5; we have not compared its protocol with ours.

| LIBERO-Pro, success % | Spatial | | Object | | Goal | | Long | | Overall |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Task | Swap | Task | Swap | Task | Swap | Task | Swap |
| ORA + DeepSeek-V4.1-Flashour harness + open-weight model · no VLA, robot training or task memory | 98 | 91 | 93 | 98 | 77 | 78 | 52 | 64 | **81.4** |
| RPent + GPT-6 Astra [a]RPent harness + language model + VLA + task-specific memory | 100 | 98 | 100 | 99 | 88 | 99 | 85 | 72 | **92.6** |
| RPent + Opus-4.7[[1]](#ref-rpent)RPent harness + language model + VLA + task-specific memory | — | — | — | — | — | — | — | — | **82.4** |
| RPent + GPT-5.5RPent harness + language model + VLA + task-specific memory | 81 | 69 | 94 | 91 | 75 | 66 | 70 | 55 | **75.1** |
| RPent Flash Mode [b][[8]](#ref-molmo2)RPent harness + Molmo2-8B + VLA + released task-specific memory | 79 | 70 | 86 | 93 | 74 | 65 | 60 | 54 | **72.6** |
| RPent + Qwen3.6 27B[[2]](#ref-qwen36)RPent harness + open-weight model + VLA + task-specific memory | 82 | 78 | 83 | 84 | 68 | 68 | 61 | 41 | **70.6** |
| ASPIRE [c][[32]](#ref-aspire)LLM writes code + skill library | 60 | 51 | 95 | 98 | 45 | 81 | 38 | 23 | — |
| RATs[[33]](#ref-rats)LLM writes code + skill library | 31 | 29 | 63 | 61 | 36 | 43 | — | — | — |
| CaP-Agent0[[31]](#ref-capx)LLM writes code | 14 | 12 | 18 | 22 | 17 | 26 | — | — | — |
| π\_RLinf[[4]](#ref-pirl)VLA, robot demos + RL | 42 | 59 | 71 | 78 | 45 | 42 | 49 | 14 | **50.0** |
| π0.5[[3]](#ref-openpi)VLA, trained on robot demos | 1 | 20 | 1 | 17 | 2 | 38 | 1 | 8 | **11.0** |

**Table 5.** Success rates (%) on the eight LIBERO-Pro suites, 10 tasks and 10 seeds each. Swap is the leaderboard's name for position perturbation. RPent and VLA rows come from the RPent leaderboard; — means not reported. [a] GPT-6 Astra uses separately frozen memory snapshots. [b] Flash Mode runs Molmo2-8B with released memory and reports the best of ten seeds. [c] ASPIRE learns skills on seeds 51–65 and tests on held-out seeds with Claude Opus 4.6, and its Long results transfer a LIBERO-90 skill library, so we give no overall rate for it. CaP-Agent0 is reported with 50 trials per condition. Exact counts are in the [appendix](https://freemty.github.io/ora/appendix/).

### RoboDojo: a first scan[#](#res-robodojo)

RoboDojo[[10]](#ref-robodojo) is the hardest: 42 multi-stage tasks on a two-arm ARX X5. A first run with an earlier version of **ORA**, three rounds per task, solved 18 of 126 rounds and 9 of the 42 tasks at least once. Most of the 108 failed rounds failed in motion: the target was reasonable, but the motion did not achieve it ([Table 6](#tab-rdj)). This is not an evaluation, and we know of no published results on this task set.

| Main cause of the failed round | Rounds |
| --- | --- |
| Motion did not achieve a reasonable target | 64 |
| Strategy, order or tool use | 29 |
| Perception or localization | 7 |
| Simulator anomaly | 3 |
| Gave up while recovery was still possible | 3 |
| Undetermined | 2 |

**Table 6.** Main cause of each of the 108 failed rounds in the 42-task RoboDojo scan, one auditor judgement per round; 27 of the 64 motion cases are low-confidence.

### Preliminary results on a real robot[#](#real)

Everything above runs in simulation. We also connected **ORA** to a low-cost arm on a table, with a fixed RGB-D camera and a camera on the wrist, and gave DeepSeek-V4.1-Flash two household tasks: pull a small drawer open by its knob ([Figure 12](#fig-realdrawer)), and put a candy bar into a small open box ([Figure 13](#fig-realbar)). The loop is the one in simulation: the model reads the camera views and depth, plans each motion and reads what came back. An operator reviewed each motion before it ran. Both tasks were completed in these runs. We have not yet measured success rates.

[![](img/i-03e98ec0d5ee.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/ora--img--videos--ora-real-drawer.mp4)

**Figure 12.** **Open the drawer** (real robot). The model approaches the knob at 50°, closes both jaws on it, then pulls 4.5 cm twice, and the drawer comes 9 cm out. Left: the external camera; middle: the depth image the model received; right: the wrist camera. Time is sped up, and pauses while the model plans are shown as stills.

[![](img/i-c4e443aa6334.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/ora--img--videos--ora-real-bar.mp4)

**Figure 13.** **Put the candy bar in the box** (real robot). After a 9 mm wrist correction the gripper closes on the bar, rises 13 cm, slides the bar over the opening and releases it, and the arm returns to its folded pose. Left: the external camera; right: the wrist camera. Time is sped up, and pauses while the model plans are shown as stills.

### Cost[#](#cost)

We price every model call at DeepSeek’s published off-peak rates for DeepSeek-V4.1-Flash[[53]](#ref-dsprice): $0.003 per million cached input tokens, $0.15 per million uncached input tokens and $0.60 per million output tokens. Off-peak prices are half the peak ones, so at peak rates every figure below doubles. We serve the model ourselves, so these are API-equivalent costs rather than what we paid. Every attempt counts, failures included; simulator and GPU costs are excluded.

| Benchmark | Attempts | Solved | Model callsmedian | Input tokensmedian | Cache hitsestimated | Per attemptmean / median | Total | Per solved case |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RoboTwin | 250 | 173 | 28 | 3.7M | 86% | $0.24 / $0.12 | $60.2 | **$0.35** |
| LIBERO-Pro | 800 | 651 | 27 | 3.1M | 84% | $0.28 / $0.10 | $227.4 | **$0.35** |
| LIBERO | 405 | 334 | 26 | 2.9M | 84% | $0.25 / $0.09 | $100.2 | **$0.30** |
| RoboDojo | 126 | 18 | 55.5 | 11.0M | 86% | $0.39 / $0.35 | $49.2 | $2.74 |

**Table 7.** API-equivalent model cost of the evaluation runs reported above, at DeepSeek's off-peak USD rates for DeepSeek-V4.1-Flash. LIBERO counts 400 scored cases and 5 attempts that ended in an infrastructure failure and were rerun. The RoboDojo row counts the 126 rounds of the first RoboDojo run in Results (42 tasks, three rounds each, an earlier harness version), which is not an evaluation.

Most of the cost is uncached input: on LIBERO-Pro, $157 of $227, against $54 for output and $17 for cached input. Costs are also skewed. The median attempt costs well under half the mean, because long failing attempts keep adding input; a solved attempt costs $0.11 to $0.14 on average, and the 40 solved rounds in [Figure 1](#fig-hero) cost $0.13 each. An attempt produces about 100k output tokens.

Our server does not report prompt-cache hits, so we reconstruct them from token counts. A call whose input contains the whole previous request and response extends it, and that prefix counts as a hit; any other call breaks the prefix, and only the fixed prompt at its start counts. 86–89% of calls extend the previous one, which gives the estimated hit rates of 84–86% in the table. The remaining calls follow a context reduction or open a new round, and they produce 83–89% of all uncached tokens. Since uncached input is the largest cost, the main way to cut cost is to break the prefix less often.

## Analysis: what the harness contributes[#](#analysis)

Earlier we argued that a robot needs more from the harness than a coding agent does. Each part came out of audits of failed runs; here we compare run versions and examine individual cases. Most comparisons do not isolate one component. Every video plays all of its panes at the same simulated-time speed, and each takeaway states its evidence and its limits.

### Learning from experience[#](#an-learn)

Context management keeps a finished round in the input, word for word at first and then as a checkpoint. **ORA** keeps no memory from one task to the next, and the benchmark runs above use one round per case, but within one session the model can draw on its earlier rounds. In [Figure 14](#fig-rounds), each second round opens by stating what went wrong in the first and then avoids it; in the top row, the run of [Figure 3](#fig-tui), round 1 lost the blue block when the arm moved sideways after releasing it, and round 2 began by stating the rule to lift straight up first.

[![](img/i-7975d47a86e2.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/ora--img--videos--ora-rounds.mp4)

**Figure 14.** Two sessions, one per row: the failed round 1 (left), the lesson the model stated at the start of round 2 (yellow) and the successful round 2 on the same scene (right). Top: RoboDojo, stacking blocks; round 1 drags the blue block off the table while retracting. Bottom: RoboTwin, opening a laptop; round 1 pushes the half-open lid shut from above. Both sessions were chosen after seeing the outcome, and the RoboTwin one is outside the reported evaluation.

**Takeaway: in the examples above, the model uses retained context to revise its approach. Across 148 two-round development sessions, round 2 succeeded in 72 and round 1 in 63. This comparison does not isolate the effect of retained context from the benefit of another attempt.**

### Exact task instructions and success criteria matter[#](#cs-task)

The prompt bundle states the task in two parts: the benchmark’s instruction, unchanged, and a completion contract that restates the official success test in plain words. When an early run set paraphrased one LIBERO-Spatial task, writing “the top layer of the wooden cabinet” for “the top drawer”, the model took the bowl standing on the cabinet instead of the one in the drawer ([Figure 15](#fig-pairtask)). An instruction can also leave out part of the test: RoboTwin’s “hold the bottle head up” also requires carrying the bottle toward the side its base pointed to, and “move the playing card away from the near edge” requires the card to end far to the left or right. Without the contract, the model satisfied the words and failed the check ([Figure 16](#fig-paircontract)).

[![](img/i-0fb64b759773.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/ora--img--videos--ora-cs-task.mp4)

**Figure 15.** LIBERO-Spatial, two seeds. Left: the paraphrased instruction, and the wrong bowl. Right: the benchmark's words, and the bowl from the drawer placed on the plate.

[![](img/i-5c3be6d61385.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/ora--img--videos--ora-cs-contract.mp4)

**Figure 16.** RoboTwin, the same seed on each row, without the contract (left) and with it (right). Top: the bottle is stood upright and never carried; with the contract it is carried toward the side its base pointed to. Bottom: the card box is moved from spot to spot through ten failed checks; with the contract it is carried to the left edge and released.

**Takeaway: the run version using the benchmark’s own words succeeded on 10 of 10 seeds, versus 2 of 10 for the version using a paraphrase. On 206 paired RoboTwin cases, the version with the completion contract succeeded on 64.1%, versus 53.4% without it. Other harness components also changed, so neither comparison isolates the effect of wording or the contract.**

### Perception tools help find and locate objects[#](#cs-perception)

The looking tools turn the model’s naming and pointing into masks with measured positions and sizes ([Figure 10](#fig-tools)). Early runs show why the model needs them. Its own points are not precise enough: in one LIBERO run, points chosen on the angled camera landed on the supporting surface instead of the object, and moving a point 7 to 14 pixels merged the can with the table in the mask; the size of the returned mask made the error visible. Its choice among look-alike objects is not reliable either: when text grounding ranked the wrong can first, enlarged close-ups of each candidate let the model pick the right one. Later runs repeat the second pattern ([Figure 17](#fig-csperception)).

[![](img/i-6f48175ec12d.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/ora--img--videos--ora-cs-perception.mp4)

**Figure 17.** Two solved runs where text grounding scored look-alike objects close together, and in LIBERO-Pro ranked the wrong bottle first: what the tool returned (left) and what the model did with it (right).

**Takeaway: from single early runs and with no matched ablation yet, the tools make pointing and identity errors visible, while choosing the right object stays the hardest step.**

### Exact constants and measurements[#](#cs-measure)

The tool suite gives the model measurements instead of its own estimates, and the measurement has to be the one the action needs. For placement, the tools first returned the centre of the target’s mask as LIBERO’s angled camera sees it, 2–3 cm from the object’s centre on the table and about the whole placement tolerance. They now return the centre as seen from above ([Figure 18](#fig-csmeasure)). More generally, giving the model exact coordinates and the environment’s constants, in tool results and in the system prompt, matters a great deal for its reasoning. Astranomy finds the same for GPT-6 Astra: as a direct robot policy, its success rose from 19.3% to 72.7% when the prompt added camera and gripper geometry[[54]](#ref-astranomy).

[![](img/i-4a5bff6b6417.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/ora--img--videos--ora-cs-measure.mp4)

**Figure 18.** Two long LIBERO tasks, the same initial state on each row: with the centre seen from the camera, the placement misses (left); with the centre seen from above, it lands (right).

**Takeaway: returning the centre seen from above raised success on the two affected task families from 29 to 42 of 59 test states.**

### Explaining refused motions helps recovery[#](#cs-feedback)

Motion tools report back after every action, and a refusal says why. Early on, when the planner found no inverse-kinematics solution and the refusal gave no reason, RoboDojo runs abandoned the target as unreachable, although most such targets were reachable with the gripper tilted; a bare error message once led a GPT-6 Astra run to repeat the same call 14 times in five minutes. A refusal now reports how far along the straight path the arm can reach and the nearest reachable orientation. In the run of [Figure 3](#fig-tui), turn 6 was refused this way, with 75% of the path reachable and a 15° tilt as the nearest reachable orientation; the model moved the build spot to where both arms could reach, and after one more refused move with the left arm it grasped the blue block with the right arm ([Figure 11](#fig-loop)). [Figure 19](#fig-csfeedback) shows two more runs: in RoboTwin, the reported reach made the model set the block down and relay it with the other arm; in LIBERO-Pro, the model took the reachable orientation the refusal offered.

[![](img/i-0c107fb5c767.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/ora--img--videos--ora-cs-feedback.mp4)

**Figure 19.** Two solved runs with refused moves: the refusal and the model's reading of it (left) and what it did next (right).

**Takeaway: replayed offline over 77 refused moves, a refusal that names the nearest reachable orientation resolves 69.**

The [gallery](https://freemty.github.io/ora/gallery/) shows 153 solved episodes, one per task, each checked by eye.

## Limitations[#](#limitations)

**ORA** shows that an open-weight model can operate robots zero-shot, but it has clear limits. First, it is slow: a median episode takes 14 to 25 minutes, most of it spent waiting for the model, and the simulator pauses while the model thinks, so these results say nothing about real-time control. Long-horizon tasks remain hard: the Long suites succeed 52–64% of the time, and the first RoboDojo scan solved 18 of 126 rounds. Second, the tool suite is written by hand, and **ORA** cannot yet iterate on or revise its tools automatically. Almost all of our results come from simulation and from one model, DeepSeek-V4.1-Flash; on the real robot we have only two demonstrations, with an operator approving each motion. Our success rates use each benchmark’s official check, which ends the episode the moment its condition holds, and some conditions are looser than the instruction: RoboTwin’s shake tasks only check that the bottle is raised. When we watched one solved RoboTwin episode per task, 7 of 46 did not do what the instruction asks, so the reported rates overstate real task completion. This task-selected sample cannot establish a corrected overall success rate. Most of our findings come from reading failed runs, not from controlled ablations. Next, we will run **ORA** on more real robots and turn verified episodes into training data for a smaller model that runs on the robot.

## Acknowledgements[#](#ack)

We thank the RPent team for releasing their evaluation cases, leaderboard and code, on which the comparisons in this post rely[[1]](#ref-rpent); the authors of CaP-X[[31]](#ref-capx) and ASPIRE[[32]](#ref-aspire), whose work inspired our tools; and DeepSeek for releasing DeepSeek-V4.1-Flash as an open-weight model[[9]](#ref-deepseek). We thank [Zhaoning Wang](https://www.zhaoningwang.com/) for deploying **ORA** on the real robot, and [Junda Chen](https://github.com/GindaChen/), [Runyu Lu](https://runyulu.com/) and [Nan Xue](https://xuenan.net/) for helpful discussions.

## Citation[#](#citation-sec)

Copy

```
@misc{ora2026,
  title        = {{ORA}: Open Robot-Use Agents},
  author       = {Yang, Yuanbo and Chen, Siyi and Gao, Jun and Zhang, Hao},
  year         = {2026},
  month        = oct,
  howpublished = {Hao AI Lab blog},
  url          = {https://haoailab.com/blogs/ora/}
}
```

## References[#](#references)

1. Yixian Zhang et al. Harness VLA: Steering Frozen VLAs into Reliable Manipulation Primitives via Memory-Guided Agents. arXiv:2607.08448, 2026. Code and leaderboard: RPent (RLinf). [arxiv.org/abs/2607.08448](https://arxiv.org/abs/2607.08448) [↩](#cite-rpent)
2. Qwen Team. Qwen3.6-27B. Model card, 2026. [huggingface.co/Qwen/Qwen3.6-27B](https://huggingface.co/Qwen/Qwen3.6-27B) [↩](#cite-qwen36)
3. Physical Intelligence. openpi. Software, 2025. [github.com/Physical-Intelligence/openpi](https://github.com/Physical-Intelligence/openpi) [↩](#cite-openpi)
4. Kang Chen et al. πRL: Online RL Fine-tuning for Flow-based Vision-Language-Action Models. arXiv:2510.25889, 2025. [arxiv.org/abs/2510.25889](https://arxiv.org/abs/2510.25889) [↩](#cite-pirl)
5. NVIDIA. GR00T N1: An Open Foundation Model for Generalist Humanoid Robots. arXiv:2503.14734, 2025. [arxiv.org/abs/2503.14734](https://arxiv.org/abs/2503.14734) [↩](#cite-gr00t)
6. Wei Wu et al. A Pragmatic VLA Foundation Model. arXiv:2601.18692, 2026. [arxiv.org/abs/2601.18692](https://arxiv.org/abs/2601.18692) [↩](#cite-lingbot)
7. Xiaoquan Sun et al. AtomVLA: Scalable Post-Training for Robotic Manipulation via Predictive Latent World Models. arXiv:2603.08519, 2026. [arxiv.org/abs/2603.08519](https://arxiv.org/abs/2603.08519) [↩](#cite-atomvla)
8. Christopher Clark et al. Molmo2: Open Weights and Data for Vision-Language Models with Video Understanding and Grounding. arXiv:2601.10611, 2026. [arxiv.org/abs/2601.10611](https://arxiv.org/abs/2601.10611) [↩](#cite-molmo2)
9. DeepSeek-AI. DeepSeek-V4.1-Flash. Model card, 2026. [huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash) [↩](#cite-deepseek)
10. Tianxing Chen et al. RoboDojo: A Unified Sim-and-Real Benchmark for Comprehensive Evaluation of Generalist Robot Manipulation Policies. arXiv:2607.04434, 2026. [arxiv.org/abs/2607.04434](https://arxiv.org/abs/2607.04434) [↩](#cite-robodojo)
11. John Yang et al. SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering. NeurIPS, 2024. [arxiv.org/abs/2405.15793](https://arxiv.org/abs/2405.15793) [↩](#cite-sweagent)
12. OpenAI. Computer-Using Agent. Blog post, 2025. [openai.com/index/computer-using-agent/](https://openai.com/index/computer-using-agent/) [↩](#cite-cua)
13. Xinyuan Wang et al. OpenCUA: Open Foundations for Computer-Use Agents. NeurIPS, 2025. [arxiv.org/abs/2508.09123](https://arxiv.org/abs/2508.09123) [↩](#cite-opencua)
14. Brianna Zitkovich et al. RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control. CoRL, 2023. [arxiv.org/abs/2307.15818](https://arxiv.org/abs/2307.15818) [↩](#cite-rt2)
15. Moo Jin Kim et al. OpenVLA: An Open-Source Vision-Language-Action Model. CoRL, 2024. [arxiv.org/abs/2406.09246](https://arxiv.org/abs/2406.09246) [↩](#cite-openvla)
16. Seonghyeon Ye et al. World Action Models are Zero-shot Policies. ICLR 2026 Workshop on World Models, 2026. [arxiv.org/abs/2602.15922](https://arxiv.org/abs/2602.15922) [↩](#cite-dreamzero)
17. Tony Z. Zhao et al. Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware. RSS, 2023. [arxiv.org/abs/2304.13705](https://arxiv.org/abs/2304.13705) [↩](#cite-aloha)
18. Cheng Chi et al. Universal Manipulation Interface: In-The-Wild Robot Teaching Without In-The-Wild Robots. RSS, 2024. [arxiv.org/abs/2402.10329](https://arxiv.org/abs/2402.10329) [↩](#cite-umi)
19. Simar Kareer et al. EgoMimic: Scaling Imitation Learning via Egocentric Video. ICRA, 2025. [arxiv.org/abs/2410.24221](https://arxiv.org/abs/2410.24221) [↩](#cite-egomimic)
20. Jianyuan Wang. Slide at the Eighth Workshop on Image Matching: Local Features and Beyond (CVPR 2026), photo shared on X. Social post, 2026. [x.com/ducha\_aiki/status/2062653228802515047](https://x.com/ducha_aiki/status/2062653228802515047) [↩](#cite-jwang)
21. Jay Chooi. GPT-6 Astra on a robot control task. Thread on X, 2026. [x.com/chooi\_jeq/status/2096064315115839904](https://x.com/chooi_jeq/status/2096064315115839904) [↩](#cite-chooi)
22. Phillip Isola. Robot-Use Agents. Essay, 2026. [web.mit.edu/phillipi/www/writing/robot-use-agents.html](https://web.mit.edu/phillipi/www/writing/robot-use-agents.html) [↩](#cite-isola)
23. Shmuel Berman et al. Claude plays robotics. Anthropic blog post, 2026. [www.anthropic.com/research/claude-plays-robotics](https://www.anthropic.com/research/claude-plays-robotics) [↩](#cite-cpr)
24. Achu Menon et al. GPT-6 Astra on robotic manipulation. Robocurve blog post, 2026. [openai.robocurve.org/gpt-6-astra/](https://openai.robocurve.org/gpt-6-astra/) [↩](#cite-robocurve)
25. Hanming Ye and Yiding Song. Introducing Waddle: agents that control robots. Waddle Labs blog post, 2026. [www.waddlelabs.ai/research/introducing-waddle](https://www.waddlelabs.ai/research/introducing-waddle) [↩](#cite-waddle)
26. Angen Ye et al. GigaWorld-Policy: An Efficient Action-Centered World–Action Model. arXiv:2603.17240, 2026. [arxiv.org/abs/2603.17240](https://arxiv.org/abs/2603.17240) [↩](#cite-gigaworld)
27. Michael Ahn et al. Do As I Can, Not As I Say: Grounding Language in Robotic Affordances. CoRL, 2022. [arxiv.org/abs/2204.01691](https://arxiv.org/abs/2204.01691) [↩](#cite-saycan)
28. Lucy Xiaoyang Shi et al. Hi Robot: Open-Ended Instruction Following with Hierarchical Vision-Language-Action Models. ICML, 2025. [arxiv.org/abs/2502.19417](https://arxiv.org/abs/2502.19417) [↩](#cite-hirobot)
29. Figure. Helix: A Vision-Language-Action Model for Generalist Humanoid Control. Blog post, 2025. [www.figure.ai/news/helix](https://www.figure.ai/news/helix) [↩](#cite-helix)
30. Jacky Liang et al. Code as Policies: Language Model Programs for Embodied Control. ICRA, 2023. [arxiv.org/abs/2209.07753](https://arxiv.org/abs/2209.07753) [↩](#cite-cap)
31. Letian Fu et al. CaP-X: A Framework for Benchmarking and Improving Coding Agents for Robot Manipulation. ICML, 2026. [arxiv.org/abs/2603.22435](https://arxiv.org/abs/2603.22435) [↩](#cite-capx)
32. Runyu Lu et al. ASPIRE: Agentic Skills Discovery for Robotics. arXiv:2607.00272, 2026. [arxiv.org/abs/2607.00272](https://arxiv.org/abs/2607.00272) [↩](#cite-aspire)
33. Junyi Zhang et al. Playful Agentic Robot Learning. arXiv:2606.19419, 2026. [arxiv.org/abs/2606.19419](https://arxiv.org/abs/2606.19419) [↩](#cite-rats)
34. Shunyu Yao et al. ReAct: Synergizing Reasoning and Acting in Language Models. ICLR, 2023. [arxiv.org/abs/2210.03629](https://arxiv.org/abs/2210.03629) [↩](#cite-react)
35. Haowen Liu et al. Guava: Distilling Frontier VLMs into a Compact Agent through a Robotic Manipulation Harness. arXiv:2606.18363, 2026. [arxiv.org/abs/2606.18363](https://arxiv.org/abs/2606.18363) [↩](#cite-guava)
36. Zhaoyang Chu et al. OpenRUA: Robot-Use Agents Are Zero-Shot Visuomotor Policies. arXiv:2610.02459, 2026. [arxiv.org/abs/2610.02459](https://arxiv.org/abs/2610.02459) [↩](#cite-openrua)
37. Mengzhao Jia et al. Agent as Policy for Robotic Manipulation. arXiv:2609.12541, 2026. [arxiv.org/abs/2609.12541](https://arxiv.org/abs/2609.12541) [↩](#cite-agp)
38. Zexi Li et al. Robo-Harness K1: Harnessing Robot-Use Agents via Perception Augmentation. arXiv:2609.29389, 2026. [arxiv.org/abs/2609.29389](https://arxiv.org/abs/2609.29389) [↩](#cite-k1)
39. Anthropic. Claude Code. Software, 2025. [github.com/anthropics/claude-code](https://github.com/anthropics/claude-code) [↩](#cite-claudecode)
40. Mario Zechner. Pi: a minimal, extensible agent harness (pi-mono). Software, 2025. [github.com/earendil-works/pi](https://github.com/earendil-works/pi) [↩](#cite-pi)
41. NVIDIA. Isaac Sim. Software, 2026. [developer.nvidia.com/isaac/sim](https://developer.nvidia.com/isaac/sim) [↩](#cite-isaacsim)
42. Tianxing Chen et al. RoboTwin 2.0: A Scalable Data Generator and Benchmark with Strong Domain Randomization for Robust Bimanual Robotic Manipulation. ICML, 2026. [arxiv.org/abs/2506.18088](https://arxiv.org/abs/2506.18088) [↩](#cite-robotwin)
43. Fanbo Xiang et al. SAPIEN: A SimulAted Part-based Interactive ENvironment. CVPR, 2020. [arxiv.org/abs/2003.08515](https://arxiv.org/abs/2003.08515) [↩](#cite-sapien)
44. Bo Liu et al. LIBERO: Benchmarking Knowledge Transfer for Lifelong Robot Learning. NeurIPS Datasets and Benchmarks Track, 2023. [arxiv.org/abs/2306.03310](https://arxiv.org/abs/2306.03310) [↩](#cite-libero)
45. Xueyang Zhou et al. LIBERO-PRO: Towards Robust and Fair Evaluation of Vision-Language-Action Models Beyond Memorization. arXiv:2510.03827, 2025. [arxiv.org/abs/2510.03827](https://arxiv.org/abs/2510.03827) [↩](#cite-liberopro)
46. Emanuel Todorov, Tom Erez and Yuval Tassa. MuJoCo: A physics engine for model-based control. IROS, 2012. [ieeexplore.ieee.org/document/6386109](https://ieeexplore.ieee.org/document/6386109) [↩](#cite-mujoco)
47. Yuke Zhu et al. robosuite: A Modular Simulation Framework and Benchmark for Robot Learning. arXiv:2009.12293, 2020. [arxiv.org/abs/2009.12293](https://arxiv.org/abs/2009.12293) [↩](#cite-robosuite)
48. Ruijie Lu et al. Thinking with Visual Primitives. DeepSeek-AI technical report, 2026. [github.com/deepseek-ai/Thinking-with-Visual-Primitives](https://github.com/deepseek-ai/Thinking-with-Visual-Primitives) [↩](#cite-dsvp)
49. Nicolas Carion et al. SAM 3: Segment Anything with Concepts. ICLR, 2026. [arxiv.org/abs/2511.16719](https://arxiv.org/abs/2511.16719) [↩](#cite-sam3)
50. Balakumar Sundaralingam et al. cuRobo: Parallelized Collision-Free Minimum-Jerk Robot Motion Generation. arXiv:2310.17274, 2023. [arxiv.org/abs/2310.17274](https://arxiv.org/abs/2310.17274) [↩](#cite-curobo)
51. Martin Sundermeyer et al. Contact-GraspNet: Efficient 6-DoF Grasp Generation in Cluttered Scenes. ICRA, 2021. [arxiv.org/abs/2103.14127](https://arxiv.org/abs/2103.14127) [↩](#cite-cgn)
52. Chia-Yu Hung et al. NORA: A Small Open-Sourced Generalist Vision Language Action Model for Embodied Tasks. arXiv:2504.19854, 2025. [arxiv.org/abs/2504.19854](https://arxiv.org/abs/2504.19854) [↩](#cite-nora)
53. DeepSeek. Models & Pricing. Documentation. [api-docs.deepseek.com/quick\_start/pricing](https://api-docs.deepseek.com/quick_start/pricing) [↩](#cite-dsprice)
54. Jenai Xuning Yang, Ashna Khetan and Shun Zhang. Astranomy: An empirical study of GPT-6 Astra as a native robot policy. NVIDIA Seattle Robotics Lab, 2026. [research.nvidia.com/labs/srl/projects/astranomy/](https://research.nvidia.com/labs/srl/projects/astranomy/) [↩](#cite-astranomy)
