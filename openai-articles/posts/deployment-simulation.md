---
title: "Predicting model behavior before release by simulating deployment"
date: 2026-06-16
source: https://openai.com/index/deployment-simulation/
crawled: 2026-09-13
category: research
---

## Introduction

Before releasing a new model, labs need to understand not just what it can do, but how it is likely to behave in real-world use, including where it might introduce new risks. This becomes even more important as capabilities increase. As part of our pre-deployment safety review, we leverage targeted evaluations, red-teaming, and other checks to understand model behavior. We’ve now started using a method for simulating model deployments before they happen, which adds a complementary signal: a deployment-like preview of how a candidate model may behave before it reaches users.

Deployment Simulation is a method for simulating a future deployment before it happens. We do so by replaying previous conversations in a privacy-preserving manner with a new candidate model. This enables us to study how the new model responds in realistic contexts before release, including whether new undesired behaviors emerge and how often they may appear.

Across multiple GPT‑5‑series Thinking deployments, Deployment Simulation improved our estimates of undesired model behavior rates, helped surface novel forms of misalignment before release, and helped reduce the risk that models would be able to tell they were being tested. We also applied the method to challenging agentic rollouts, showing that it can extend beyond standard chat to more complex agent settings involving tool use, and can also be used for risk assessment before internal model deployments.

We have already used insights from Deployment Simulation during model development to identify blind spots in traditional evaluations and inform mitigations and deployment decisions. As we make the pipeline easier to run, we expect it to play a larger role in the future model development process.

## How Deployment Simulation works

Pre-deployment evaluations used across the industry generally consist of a mix of synthetic, manually written, or production prompts intentionally selected to be difficult, high severity, or adversarial. These evaluations have generally had two intertwined goals: assessing how the model responds when stress-tested in situations that have a very small chance of occurring in deployment traffic, and gaining a general understanding of undesired model behaviors, including finding novel undesired behaviors and predicting their deployment-time frequencies.

While traditional evaluations remain crucial for the first goal, Deployment Simulation represents a significant step forward with regards to the second goal for non-tail risks (in our experiments, our approach can’t be expected to measure behaviors that occur with frequency less than 1 in 200,000 messages). Deployment Simulation’s strength comes from side-stepping some core challenges with traditional evaluations:

- **Coverage:** it is difficult to be confident that evaluation prompts will cover all possible types of undesired model behavior. Measuring new types of undesired behavior requires creating new evaluations, and knowing what harms to measure. This can be time and labor intensive, and evaluations can saturate over time.
- **Selection biases:** traditional evaluations generally are built with specific undesired model behaviors in mind, selected in ways that bias towards contexts have previously occurred. This may make their estimates less informative about incidence of such behaviors in the full breadth of the deployment distribution.
- **Being recognizable as tests by models:** models have been increasingly able to determine they are being tested, which can distort their behavior and our downstream measurements of their safety. While many of the traditional evaluations we use at OpenAI are also drawn from production traffic and don’t suffer from this issue, this is a common concern for many traditional evaluations used across the industry.

The main technique behind Deployment Simulation is simple: we take recent conversations from deployment, remove the original assistant response from the older model, and regenerate it with a candidate model to be released. We evaluate the completions by searching for new failure modes, and estimate deployment-time undesired behavior frequency based on frequency in this deployment-like distribution. We can perform the same measurements after release on real deployment traffic, enabling us to validate our pre-deployment forecasts.

Deployment Simulation significantly mitigates the three limitations listed above: sampling bias is addressed by using a distribution of evaluation prompts representative of recent usage. Deployment Simulation with representative prompts can also mitigate concerns about coverage: we get greater coverage of undesirable model behaviors by simply simulating more traffic. This tradeoff between compute and coverage is important, because it makes the quality of this axis of risk assessment scale with compute, rather than the manual effort required to build more evaluations. Models also don’t seem to be able to distinguish between conversations obtained via deployment simulation and real deployment traffic.

*Figure 1: Overview of our Deployment Simulation pipeline*

| **Area** | **Traditional Evaluations** | **Deployment Simulation** |
| **Coverage** | Better for low prevalence but high severity risks that we want to make sure we have coverage for | Better for understanding the spectrum of risks we’re likely to see in deployment traffic |
| **Representativeness / bias** | Focused on evaluating targeted past or predicted risks, even for behaviors that have extremely low prevalence in deployment | Representative of risks that occur above a certain prevalence in current deployment traffic |
| **Evaluation awareness** | Potentially obvious test cues (e.g., with synthetic data) unless evals are created with deployment data | Deployment-like context seems to significantly mitigate eval awareness |
| **Effort** | Custom prompt distributions and setups requires significantly more manual effort | Requires a one-time infrastructure cost, and then reuses prefixes from deployment and graders from known undesired behaviors |

*High level comparison between traditional evaluations and Deployment Simulation*

## How we tested Deployment Simulation

To evaluate Deployment Simulation, we pre-registered predictions for the deployment-time frequency of 20 types of undesirable behavior for GPT‑5.4 Thinking. We also ran retrospective studies across other deployments of Thinking models of the GPT‑5‑series. The model behaviors we analyze cover both misalignment and disallowed content categories which we have been reporting in system cards (e.g. the model lying about tools, or outputting disallowed sexual content). While for these results we only track 20 categories of undesired model behavior, and only look for novel misaligned behaviors, Deployment Simulation is a general technique which could be applied to simulate any deployment-time model property.

The production traffic we leveraged was also from Thinking models of the GPT‑5‑series. Before running our evaluations, we automatically removed account-linked identifiers and identifiable information. In accordance with our privacy policy, we only analyzed ChatGPT traffic from users who allow their data to be used for model improvements. We report only aggregate findings from these evaluations. In total, we analyzed approximately 1.3 million de-identified conversations across GPT‑5 Thinking through GPT‑5.4 deployments, spanning August 2025 to March 2026.

We evaluate the quality of the pre-deployment risk-assessment produced by Deployment Simulation in three main ways:

- **Taxonomy coverage:** did post-release auditing surface any important misaligned behaviors missing from our initial bad behavior taxonomy?
- **Directional accuracy:** did the simulation correctly predict whether deployment prevalence would increase or decrease for known behaviors?
- **Rate calibration:** were our pre-deployment estimates close to the rates we later observed in deployment? Achieving good rate calibration requires more than directional accuracy, making this the highest possible quality standard.

We also measure how much models are able to tell they are in an evaluation during Deployment Simulation, and test how robust the method is to different forms of deployment traffic and to challenging tool use settings.

## Deployment Simulation significantly expands pre-deployment risk assessment

Across GPT‑5‑series Thinking deployments, Deployment Simulation outperformed challenging-prompt baselines in determining actual risk rate, was able to surface calculator hacking before release, and appeared potentially indistinguishable from deployment to the model.

**Overview of our predictions.** For a visualization of all predictions for Thinking model deployments of the GPT‑5‑series, see Figure 2. The predictions for GPT‑5.4 Thinking were pre-registered, while the others were retroactive predictions. In aggregate, our predictions had a median multiplicative error of 1.5x (e.g. if the undesirable behavior rate is 10 in 100k, this would correspond to estimating a rate of 15 or 6.67 in 100k). While tail errors of our method can be roughly 10x larger, we expect they can be significantly reduced with further improvements to our simulation pipeline, as discussed below.

*Figure 2. Deployment Simulation frequency predictions of deployment-time undesirable behavior based on prior deployment data. The notation 5.1 → 5 indicates that we are resampling prefixes from GPT‑5 with GPT‑5.1, that is, simulating GPT‑5.1’s deployment based on data from GPT‑5. The highest rate of misaligned behavior was “calculator hacking” in GPT‑5.1, which we have discussed*[*previously*](https://alignment.openai.com/prod-evals/)*.*

**Comparing Deployment Simulation predictions to baselines.** The most important categories to estimate correctly for pre-deployment risk-assessments are ones that have large changes of incidence after the model’s deployment (e.g. >= 1.5x). On this subset, Deployment Simulation is substantially better than baselines both at predicting whether a certain undesirable behavior will increase or decrease in prevalence with a model’s deployment (Figure 3, left), and at estimating its exact deployment-time incidence (Figure 3, right). We use two main baselines: a Challenging Prompts baseline which we currently use for system cards and launch decisions, and a naive baseline of using rates from the previous deployment as estimates for the new model.

*Figure 3. Deployment Simulation predicts both the direction of incidence changes (left) and exact production rates (right) better than static evals.*

**Sources of simulation error in our pipeline.** We also studied the current sources of error in our pipeline. Specifically, large tail errors make the pipeline less trustworthy for deployment decisions: for example, when seeing a large predicted increase in an undesirable behavior of a certain type, if the pipeline is known to have even occasional large errors, it raises doubt about whether this is a reliable estimate or an artifact of the pipeline. There are two main sources of possible error:

- **Resampling environment fidelity error:** to estimate production rates accurately, our simulation pipeline needs to be as realistic as possible. This is in part an engineering problem (sampling from the model using the same pipelines used for production traffic), and in part an interesting challenge for tools which need read/write access to external resources which are constantly changing (e.g. web searches or interacting with local files). We can isolate the simulation fidelity error by comparing predictions from an actual deployment and its simulation (that is, simulating the deployment of the already deployed model).
- **Prompt distribution shift error:** a major concern with Deployment Simulation is that any model’s deployment will cause a distributional shift in inputs, especially if users adapt to new model affordances. We isolate prompt distribution error by comparing estimates when simulating the deployment using recent prompts vs prompts from the realized deployment.

As seen in Figure 4, we find that a large fraction of the error in our pipeline–especially for tail errors–is currently due to simulation fidelity. This is good news, as we expect simulation fidelity to be generally easier to improve than reducing prompt distribution shift. We also find that prompt distribution shift error may be reduced by using the most recent data from the previous deployment. More detail can be found in the research paper.

*Figure 4: Resampling environment fidelity seems to be the largest source of error in our estimates, especially for the most extreme errors.*

**Automated auditing found the one new misalignment introduced in these deployments.** In the deployment window we studied, our automated auditing pipeline based on simulated deployments would have surfaced ‘calculator hacking’ before release, which was the only novel misalignment we identified in the analyzed ChatGPT traffic. Calculator hacking is a form of reward hacking which involves the model using a browser tool as a calculator while presenting the action as a search. This does not mean large-scale auditing will catch every new failure, but it shows why realistic contexts matter: they can elicit behaviors that narrower eval sets may never surface directly, even if they were not present in the original traffic used to seed the simulation.

## Reducing evaluation awareness

Another advantage of using deployment-like contexts is that they may reduce distortions that arise when models recognize they are being tested. In prior research, [we](https://openai.com/index/detecting-and-reducing-scheming-in-ai-models/) as well as [others](https://arxiv.org/abs/2505.23836) have found that models are often aware of when they’re being tested. For example, models may reason in their chain-of-thought about what they’re being tested on, what an evaluator might like, and – if they’re misbehaving – whether they’ll be caught. This poses a problem for alignment evaluations: if a model is only well behaved because it thinks it’s being tested, how do we build confidence that it’ll behave safely once it learns it’s been deployed?

We show that Deployment Simulation substantially reduces levels of evaluation awareness exhibited by models relative to traditional evaluations which are not based on real deployment data. We measure evaluation awareness in three ways: by asking a model to classify whether a trajectory came from production or an evaluation, monitoring chain-of-thought for explicit statements about being evaluated for alignment, as well as for [metagaming](https://alignment.openai.com/metagaming): any reasoning about oversight. Simulated deployment traffic closely matched real deployment traffic across all three measures. For example, GPT‑5.2 labeled real production traffic as evaluation-like 5.4% of the time and simulated traffic 5.1% of the time, while traditional evaluations (such as SWE-Bench or MonorepoBench, which are composed primarily of synthetic examples) were classified as evaluations almost 100% of the time.

*Figure 5. Evaluation-awareness comparison: real production traffic and simulated traffic show similar rates for eval detection, verbalized alignment evaluation awareness, and metagaming, while traditional eval datasets report much higher rates.*

## Tool simulation for agentic trajectories

To test whether the method could extend beyond standard chat modes, we also studied simulating deployments for challenging agentic coding settings. Specifically, we use 120,000 internal employee agentic trajectories from GPT‑5.4 to simulate the internal deployment of coding agents based on GPT‑5.5. This serves two purposes: this shows how deployment simulation can also be used for risk-assessment for internal deployments, and it demonstrates that it is possible to make simulation fidelity high even in agentic settings via careful tool simulation.

Above we discussed that the simulation fidelity is one of the main sources of error in our current pipeline. One of the challenges with making deployment simulations realistic is that it requires tools to act in realistic ways, even when they need read/write access to external resources which are constantly changing (e.g. web searches or interacting with local files).

This is especially challenging for settings such as agentic deployments: a single agent trajectory can depend on hundreds of tool calls, repository state, network responses, or transient failures. This makes resampling with real tool access both challenging and potentially dangerous. In light of this, instead of applying tool calls to live systems, we simulate them with another LLM. We show that giving this LLM extra affordances is essential to realism and therefore estimation quality.

We give the tool-simulator model the original final-turn rollout, the repository from the time of the conversation, a database of tool-call/response pairs, and read-only connectors. In a test where a discriminator tried to tell simulated from real rollouts, realism improved from an 11.6% win rate to 49.5%, near the 50% chance level.

*Figure 6: One can make resampling realism almost indistinguishable from real sampling even in tool-heavy settings when simulating tool calls with increased affordances.*

As additional evidence of simulation fidelity, when simulating GPT‑5.4 Codex thinking traffic with GPT‑5.4, the misalignment rates are, just about, within error bars. By contrast, in our pre-deployment testing GPT‑5.5 was more misaligned in most categories.

*Figure 7: With tool simulation, behavior rates for conversations resampled with GPT‑5.4 and actual GPT‑5.4 production traffic are quite similar – indicating high resampling environment fidelity. See the*[*GPT‑5.5 system card*](https://deploymentsafety.openai.com/gpt-5-5/sec%3Acoding-internal-misalignment/fig-5)*for more context on the categories.*

These results suggest that Deployment Simulation can extend to complex agent settings when the surrounding tool environment is simulated with sufficient fidelity.

## WildChat and external auditing

A natural question is whether external auditors can get some of the same benefits without access to private production traffic. We tested this with 100,000 WildChat conversations used as prefixes. WildChat was less accurate than recent OpenAI production data, but still informative: recent production data had lower average multiplicative error than WildChat (1.75× vs. 2.44×), while WildChat often stayed within roughly 3× of production rates and identified the better model at above-chance rates. We see WildChat-style evaluations as a promising complement to developer-run Deployment Simulation. See this companion [Alignment blogpost](https://alignment.openai.com/validating-public-evals/) for more results on this point.

## Limitations

Deployment Simulation is a complement to, not a replacement for, adversarial evaluations, red-teaming, and targeted tail-risk analysis. The detection of some undesired model behaviors relies on chain-of-thought monitorability: if future models reason less legibly, omit key steps, or learn to obscure intent, we may not be able to detect these forms of undesirable behavior. Furthermore, because production data is private, developers currently have stronger access to representative contexts than external auditors. Better public datasets could narrow that gap.

Deployment Simulation is most useful for behaviors that occur often enough to appear in sampled prefixes. A failure that occurs once in ten million conversations is unlikely to be discovered in a million-sample run, so adversarial evaluations, red-teaming, and targeted tail-risk analysis remain necessary. We currently focus on simulating a single assistant response, as in preliminary experiments we did not find meaningful improvements to our estimates by simulating multiple turns. This may be an important area for improving simulation fidelity in the future.

The method also depends on the prefix distribution—the mix of conversations that are being resampled. Historical traffic may not match how users interact with a more capable model after a major product change, new tool release, world event, or seasonal shift. Analysis in the full paper suggests that this issue can be mitigated by using the most recent data available.

## Conclusion

Deployment simulation is a new approach to pre-deployment risk assessment that helps frontier labs and evaluators predict how language models may behave in the real world and understand the risks they pose before deployment. It complements existing safety evaluations, red-teaming, and targeted analysis by adding a more production-like prediction layer that can improve estimates of deployment behavior, reduce evaluation-awareness effects, and make pre-deployment predictions checkable after release. Used alongside traditional evaluations, Deployment Simulation can help make model risk assessment more realistic, more quantitative, and more useful for deployment decisions.
