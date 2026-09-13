---
title: "Mapping the misuse of generative AI"
source: https://deepmind.google/blog/mapping-the-misuse-of-generative-ai/
site: deepmind
date: 2024-08-02
authors: Nahema Marchal, Rachel Xu
crawled: 2026-09-13
---

New research analyzes the misuse of multimodal generative AI today, in order to help build safer and more responsible technologies

Generative artificial intelligence (AI) models that can produce image, text, audio, video and more are enabling a new era of creativity and commercial opportunity. Yet, as these capabilities grow, so does the potential for their misuse, including manipulation, fraud, bullying or harassment.

As part of [our commitment](https://ai.google/responsibility/principles/) to develop and use AI responsibly, we published a [new paper](https://arxiv.org/abs/2406.13843), in partnership with [Jigsaw](https://jigsaw.google.com/) and [Google.org](http://google.org/), analyzing how generative AI technologies are being misused today. Teams across Google are using this and other research to develop better safeguards for our generative AI technologies, amongst other safety initiatives.

Together, we gathered and analyzed nearly 200 media reports capturing public incidents of misuse, published between January 2023 and March 2024. From these reports, we defined and categorized common tactics for misusing generative AI and found novel patterns in how these technologies are being exploited or compromised.

By clarifying the current threats and tactics used across different types of generative AI outputs, our work can help shape AI governance and guide companies like Google and others building AI technologies in developing more comprehensive safety evaluations and mitigation strategies.

## Highlighting the main categories of misuse

While generative AI tools represent a unique and compelling means to enhance creativity, the ability to produce bespoke, realistic content has the potential to be used in inappropriate ways by malicious actors.

By analyzing media reports, we identified two main categories of generative AI misuse tactics: the exploitation of generative AI capabilities and the compromise of generative AI systems. Examples of the technologies being exploited included creating realistic depictions of human likenesses to impersonate public figures; while instances of the technologies being compromised included ‘jailbreaking’ to remove model safeguards and using adversarial inputs to cause malfunctions.

![A bar chart displaying the frequency of generative AI misuse tactics. The chart shows that "exploitation of generative AI capabilities" (dark purple bars) is far more prevalent than "compromise of generative AI systems" (light purple bars), with "impersonation" being the most frequent tactic overall at over 20%.](https://lh3.googleusercontent.com/Bk68MM5pHa6B-ZlTL2YQ0YvC61bNPU6sBtQXnSf_KSY1Cdei9KFqqTcbCZmuAtvoGG1HAb_XNw5LhnbyenrbxIZRqtaE7cI4BS3f2p8vemsngmX5UA=w1440)

Relative frequency generative AI misuse tactics in our dataset. Any given case of misuse reported in the media could involve one or more tactics.

Cases of exploitation — involving malicious actors exploiting easily accessible, consumer-level generative AI tools, often in ways that didn’t require advanced technical skills — were the most prevalent in our dataset. For example, we reviewed a high-profile case from February 2024 where an international company [reportedly lost HK$200 million](https://www.scmp.com/news/hong-kong/law-and-crime/article/3250851/everyone-looked-real-multinational-firms-hong-kong-office-loses-hk200-million-after-scammers-stage) (approx. US $26M) after an employee was tricked into making a financial transfer during an online meeting. In this instance, every other “person” in the meeting, including the company’s chief financial officer, was in fact a convincing, computer-generated imposter.

Some of the most prominent tactics we observed, such as impersonation, scams, and synthetic personas, pre-date the invention of generative AI and have long been used to influence the information ecosystem and manipulate others. But wider access to generative AI tools may alter the costs and incentives behind information manipulation, giving these age-old tactics new potency and potential, especially to those who previously lacked the technical sophistication to incorporate such tactics.

## Identifying strategies and combinations of misuse

Falsifying evidence and manipulating human likenesses underlie the most prevalent tactics in real-world cases of misuse. In the time period we analyzed, most cases of generative AI misuse were deployed in efforts to influence public opinion, enable scams or fraudulent activities, or to generate profit.

By observing how bad actors combine their generative AI misuse tactics in pursuit of their various goals, we identified specific combinations of misuse and labeled these combinations as strategies.

![A Sankey diagram mapping the goals of generative AI misuse (left) to specific tactics used to achieve them (right). Purple represents opinion manipulation, linking mainly to disinformation. Green represents monetization and profit, linking to deepfake commodification and content farming. Red represents scam and fraud, linking to celebrity scam ads and phishing. Blue represents harassment, linking to defamation and bullying. Orange represents reach, linking to plagiarism and digital resurrection. Yellow represents terrorism and extremism, linking to propaganda. Light blue represents cyber attacks, linking to information theft.](https://lh3.googleusercontent.com/r4oeN12XS9EVAmIQauX_pYFkFD4nvR_VTmWxBjCngsuEEWVQJDLnRJ1ZbnafoUMI7oxpBDO65jLDKcLk-mQc3SZzSIcM_TeaQDslLiNrqt_55HgkZw=w1440)

Diagram of how the goals of bad actors (left) map onto their strategies of misuse (right).

Emerging forms of generative AI misuse, which aren’t overtly malicious, still raise ethical concerns. For example, new forms of political outreach are blurring the lines between authenticity and deception, such as [government officials suddenly speaking a variety of voter-friendly languages](https://www.nytimes.com/2023/10/20/nyregion/ai-robocalls-eric-adams.html) without transparent disclosure that they’re using generative AI, and [activists using the AI-generated voices of deceased victims to plead for gun reform](https://www.theguardian.com/us-news/2024/feb/14/ai-shooting-victims-calls-gun-reform).

While the study provides novel insights on emerging forms of misuse, it’s worth noting that this dataset is a limited sample of media reports. Media reports may prioritize sensational incidents, which in turn may skew the dataset towards particular types of misuse. Detecting or reporting cases of misuse may also be more challenging for those involved because generative AI systems are so novel. The dataset also doesn’t make a direct comparison between misuse of generative AI systems and traditional content creation and manipulation tactics, such as image editing or setting up 'content farms' to create large amounts of text, video, gifs, images and more. So far, anecdotal evidence suggests that traditional content manipulation tactics remain more prevalent.

## Staying ahead of potential misuses

Our [paper](https://arxiv.org/abs/2406.13843) highlights opportunities to design initiatives that protect the public, such as advancing broad generative AI literacy campaigns, developing better interventions to protect the public from bad actors, or [forewarning people and equipping them](https://medium.com/jigsaw/prebunking-to-build-defenses-against-online-manipulation-tactics-in-germany-a1dbfbc67a1a) to spot and refute the manipulative strategies used in generative AI misuse.

This research helps our teams better safeguard our products by informing our development of safety initiatives. On YouTube, we [now require creators to share when their work is meaningfully altered or synthetically generated, and seems realistic](https://support.google.com/youtube/thread/264550152/new-disclosures-and-labels-for-generative-ai-content-on-youtube?hl=en). Similarly, we updated our election advertising policies to require advertisers to disclose when their election ads include material that has been digitally altered or generated.

As we continue to expand our understanding of malicious uses of generative AI and make further technical advancements, we know it’s more important than ever to make sure our work isn’t happening in a silo. We recently joined the [Content for Coalition Provenance and Authenticity](https://c2pa.org/) (C2PA) as a steering committee member to help develop the technical standard and drive adoption of Content Credentials, which are tamper-resistant metadata that shows how content was made and edited over time.

In parallel, we’re also conducting research that advances existing red-teaming efforts, including [improving best practices for testing the safety of large language models (LLMs)](https://arxiv.org/abs/2406.11757v1), and developing pioneering tools to make AI-generated content easier to identify, such as [SynthID](https://deepmind.google/technologies/synthid/), which is being integrated into a growing range of products.

In recent years, Jigsaw has [conducted research with misinformation creators](https://arxiv.org/abs/2405.13554) to understand the tools and tactics they use, [developed prebunking videos](https://prebunking.withgoogle.com/) to forewarn people of attempts to manipulate them, and [shown that prebunking campaigns can improve misinformation resilience at scale](https://www.science.org/doi/10.1126/sciadv.abo6254). This work forms part of Jigsaw’s broader portfolio of information interventions to help people protect themselves online.

By proactively addressing potential misuses, we can foster responsible and ethical use of generative AI, while minimizing its risks. We hope these insights on the most common misuse tactics and strategies will help researchers, policymakers, industry trust and safety teams build safer, more responsible technologies and develop better measures to combat misuse.

[Read our paper](https://arxiv.org/abs/2406.13843)[Learn more about Jigsaw](https://jigsaw.google.com/)

**Acknowledgements**

This research was a collective effort by Nahema Marchal, Rachel Xu, Rasmi Elasmar, Iason Gabriel, Beth Goldberg, and William Isaac, with feedback and advisory contributions from Mikel Rodriguez, Vijay Bolina, Alexios Mantzarlis, Seliem El-Sayed, Mevan Babakar, Matt Botvinick, Canfer Akbulut, Harry Law, Sébastien Krier, Ziad Reslan, Boxi Wu, Frankie Garcia, and Jennie Brennan.
