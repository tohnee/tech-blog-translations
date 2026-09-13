---
title: "Updating the Frontier Safety Framework"
source: https://deepmind.google/blog/updating-the-frontier-safety-framework/
site: deepmind
date: 2025-02-04
authors: 
crawled: 2026-09-13
---

Our next iteration of the FSF sets out stronger security protocols on the path to AGI

AI is a powerful tool that is helping to unlock new breakthroughs and make significant progress on some of the biggest challenges of our time, from climate change to drug discovery. But as its development progresses, advanced capabilities may present new risks.

That’s why we [introduced](https://deepmind.google/discover/blog/introducing-the-frontier-safety-framework/) the first iteration of our Frontier Safety Framework last year - a set of protocols to help us stay ahead of possible severe risks from powerful frontier AI models. Since then, we've collaborated with experts in industry, academia, and government to deepen our understanding of the risks, the empirical evaluations to test for them, and the mitigations we can apply. We have also implemented the Framework in our safety and governance processes for evaluating frontier models such as Gemini 2.0. As a result of this work, today we are publishing an updated [Frontier Safety Framework](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/updating-the-frontier-safety-framework/Frontier%20Safety%20Framework%202.0.pdf).

Key updates to the framework include:

- Security Level recommendations for our Critical Capability Levels (CCLs), helping to identify where the strongest efforts to curb exfiltration risk are needed
- Implementing a more consistent procedure for how we apply deployment mitigations
- Outlining an industry leading approach to deceptive alignment risk

## Recommendations for Heightened Security

Security mitigations help prevent unauthorized actors from exfiltrating model weights. This is especially important because access to model weights allows removal of most safeguards. Given the stakes involved as we look ahead to increasingly powerful AI, getting this wrong could have serious implications for safety and security. Our initial Framework recognised the need for a tiered approach to security, allowing for the implementation of mitigations with varying strengths to be tailored to the risk. This proportionate approach also ensures we get the balance right between mitigating risks and fostering access and innovation.

Since then, we have drawn on [wider research](https://www.rand.org/pubs/research_reports/RRA2849-1.html) to evolve these security mitigation levels and recommend a level for each of our CCLs.\* These recommendations reflect our assessment of the minimum appropriate level of security the field of frontier AI should apply to such models at a CCL. This mapping process helps us isolate where the strongest mitigations are needed to curtail the greatest risk. In practice, some aspects of our security practices may exceed the baseline levels recommended here due to our strong overall security posture.

This second version of the Framework recommends particularly high security levels for CCLs within the domain of machine learning research and development (R&D). We believe it will be important for frontier AI developers to have strong security for future scenarios when their models can significantly accelerate and/or automate AI development itself. This is because the uncontrolled proliferation of such capabilities could significantly challenge society’s ability to carefully manage and adapt to the rapid pace of AI development.

Ensuring the continued security of cutting-edge AI systems is a shared global challenge - and a shared responsibility of all leading developers. Importantly, getting this right is a collective-action problem: the social value of any single actor’s security mitigations will be significantly reduced if not broadly applied across the field. Building the kind of security capabilities we believe may be needed will take time - so it’s vital that all frontier AI developers work collectively towards heightened security measures and accelerate efforts towards common industry standards.

## Deployment Mitigations Procedure

We also outline deployment mitigations in the Framework that focus on preventing the misuse of critical capabilities in systems we deploy. We’ve updated our deployment mitigation approach to apply a more rigorous safety mitigation process to models reaching a CCL in a misuse risk domain.

The updated approach involves the following steps: first, we prepare a set of mitigations by iterating on a set of safeguards. As we do so, we will also develop a safety case, which is an assessable argument showing how severe risks associated with a model's CCLs have been minimised to an acceptable level. The appropriate corporate governance body then reviews the safety case, with general availability deployment occurring only if it is approved. Finally, we continue to review and update the safeguards and safety case after deployment. We’ve made this change because we believe that all critical capabilities warrant this thorough mitigation process.

## Approach to Deceptive Alignment Risk

The first iteration of the Framework primarily focused on misuse risk (i.e., the risks of threat actors using critical capabilities of deployed or exfiltrated models to cause harm). Building on this, we've taken an industry leading approach to proactively addressing the risks of deceptive alignment, i.e. the risk of an autonomous system deliberately undermining human control.

An initial approach to this question focuses on detecting when models might develop a baseline instrumental reasoning ability letting them undermine human control unless safeguards are in place. To mitigate this, we explore automated monitoring to detect illicit use of instrumental reasoning capabilities.

We don’t expect automated monitoring to remain sufficient in the long-term if models reach even stronger levels of instrumental reasoning, so we’re actively undertaking – and strongly encouraging – further research developing mitigation approaches for these scenarios. While we don’t yet know how likely such capabilities are to arise, we think it is important that the field prepares for the possibility.

## Conclusion

We will continue to review and develop the Framework over time, guided by our [AI Principles](https://ai.google/responsibility/principles/), which further outline our commitment to responsible development.

As a part of our efforts, we’ll continue to work collaboratively with partners across society. For instance, if we assess that a model has reached a CCL that poses an unmitigated and material risk to overall public safety, we aim to share information with appropriate government authorities where it will facilitate the development of safe AI. Additionally, the latest Framework outlines a number of potential areas for further research – areas where we look forward to collaborating with the research community, other companies, and government.

We believe an open, iterative, and collaborative approach will help to establish common standards and best practices for evaluating the safety of future AI models while securing their benefits for humanity. The [Seoul Frontier AI Safety Commitments](https://www.gov.uk/government/publications/frontier-ai-safety-commitments-ai-seoul-summit-2024/frontier-ai-safety-commitments-ai-seoul-summit-2024) marked an important step towards this collective effort - and we hope our updated Frontier Safety Framework contributes further to that progress. As we look ahead to AGI, getting this right will mean tackling very consequential questions - such as the right capability thresholds and mitigations - ones that will require the input of broader society, including governments.

[Read the technical report](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/updating-the-frontier-safety-framework/Frontier%20Safety%20Framework%202.0.pdf)

The latest update to the FSF was developed by Lewis Ho, Celine Smith, Claudia van der Salm, Joslyn Barnhart, and Rohin Shah, under the leadership of Allan Dafoe, Anca Dragan, Andy Song, Demis Hassabis, Four Flynn, Jennifer Beroshi, Helen King, Nicklas Lundblad, and Tom Lue. We are grateful for the substantial contributions of Aalok Mehta, Adam Stubblefield, Alex Kaskasoli, Alice Friend, Amy Merrick, Anna Wang, Ben Bariach, Charley Snyder, David Bledin, David Lindner, Dawn Bloxwich, Don Wallace, Eva Lu, Heidi Howard, Iason Gabriel, James Manyika, Joana Iljazi, Kent Walker, Lila Ibrahim, Mary Phuong, Mikel Rodriguez, Peng Ning, Roland S. Zimmermann, Samuel Albanie, Sarah Cogan, Sasha Brown, Seb Farquhar, Sebastien Krier, Shane Legg, Victoria Krakovna, Vijay Bolina, Xerxes Dotiwalla, Ziyue Wang.

**Footnotes**

\*Critical capabilities definition - To identify capabilities a model may have with potential for severe harm, we research the paths through which a model could cause severe harm in high-risk domains, and then determine the minimal level of capabilities a model must have to play a role in causing such harm. We call these “Critical Capability Levels” (CCLs), and they guide our evaluation and mitigation approach.
