---
title: "Why doesn't Streams use AI?"
source: https://deepmind.google/blog/why-doesnt-streams-use-ai/
site: deepmind
date: 2017-11-29
authors: Dominic King
crawled: 2026-09-13
---

One of the questions I’m most often asked about Streams, our secure mobile healthcare app, is “why is DeepMind making something that doesn’t use artificial intelligence?”

It’s a fair question to ask of an artificial intelligence (AI) company. When we first started thinking about working in healthcare, our natural focus was on AI and how it could be used to help the NHS and its patients. We see huge potential for AI to revolutionise our understanding of diseases - how they develop and are diagnosed - which could, in turn, help scientists discover new treatments, care pathways and cures.

In the early days of DeepMind Health, we met with clinicians at the Royal Free Hospital in London who wanted to know if AI could improve care for patients at risk of acute kidney injury (AKI). AKI is notoriously difficult to spot, and can result in serious illness or even death if left untreated.

AKI is currently detected by applying a formula (called the [AKI algorithm](https://www.england.nhs.uk/akiprogramme/aki-algorithm/)) to NHS patients’ blood tests. This algorithm is good, but it’s widely known that it isn’t perfect. For example, it has a tendency to generate false positives for patients with chronic (as opposed to acute) kidney disease. It’s also insensitive to whether the patient has been admitted to hospital for two hours or two weeks, or whether the patient is eight years old or 92 years old - all of which makes a difference.

Together with our partners at the Royal Free, we saw many ways in which technology could help and were interested in both AI and non-AI methods to make a difference.

As part of this, we made an [initial ethics application](https://www.hra.nhs.uk/planning-and-improving-research/application-summaries/research-summaries/using-machine-learning-to-improve-prediction-of-aki-deterioration/) in 2015 to the NHS Health Research Authority (HRA), for a potential research project at the Royal Free using de-personalised patient data. By combining classical statistics and AI, the goal of this research project would have been to develop better algorithms that could more accurately predict and identify AKI.

But the more time we spent with the clinicians at the Royal Free, the more it became obvious that their most urgent problems were not going to be solved by using AI to develop a better algorithm alone. They made it clear to us that their core challenge was in how you actually implement an algorithm to change the way care is delivered in practise.

We’ve often talked about the current state of technology in the NHS, to the point that it’s easy to forget just how bad the situation is. Clinicians still routinely use pagers to communicate with each other, and [research](http://www.surgjournal.com/article/S0039-6060(14)00047-6/abstract) I undertook at Imperial College London found that this causes communication barriers that slow down treatment for patients at risk. Think about how much less time you’d have in a day if, instead of sending a text, you had to page someone from a landline, and then wait for them to call you back, so you could give them the message. Imagine getting paged up to 25 times a day. And imagine how much less time you’d have in your day if everyone in your office had to share a limited number of computers and you had to wait your turn to use them.

That’s what doctors and nurses face every day, whilst trying to care for seriously ill people.

Those early meetings our team had with clinicians at the Royal Free changed our perspective about what was most needed to improve care for conditions like AKI. We shifted our focus away from AI research at the Royal Free and focused solely on building a tool - Streams - that would address the more urgent problem of rapidly responding to specific patient alerts in a coordinated way.

Rather than needing to log into a shared computer, Streams lets doctors and nurses use a mobile phone to see information about their patients that they need to make decisions about care and treatment. It puts test results and vital signs observations in the palm of their hands, and alerts them with a breaking news-style warning if a patient’s condition is getting worse. It also makes communication between different clinicians easy, so everyone has the most up to date information all the time.

![Flowchart comparing the traditional, delayed clinical workflow for detecting AKI (using pagers, phone calls, and desktop computer logins) with the accelerated, direct workflow using the Streams mobile app to notify specialists.](https://lh3.googleusercontent.com/v4ji9R48Allniw9hmgfpnviwhIyOq6XhFZS8DDIfHiSq82wyUT6PSGKDAUEq7MtYjpJ_FlVjFOpZtG3hQPamPsOnppMk8tVrcxiLCnxIGwVhQqY0xg=w1440)

By getting existing patient data to the right nurse or doctor more quickly and simply, Streams gives them more time to focus on patients - without yet relying on AI.

Building Streams turned out to be a lot of work and, given the limited size of our team back in 2015, we decided against pursuing AI research with the Royal Free in parallel. As well as the additional workload, it would have required us to effectively split our team into two to ensure that the Royal Free’s personally identified data (for Streams) and de-identified data (for research) were kept entirely separate. So we didn’t move forward with AI research, and nor did we sign the additional agreements with the Royal Free that would be required to do so. To this date, we have not done any research or AI development with the Royal Free.

That’s not to say we’ve stopped thinking about how AI will be able to help clinicians in future. We’ve pursued multiple AI research projects with other partners, and have always been clear that in future we hope that Streams at the Royal Free will use AI.

But as the saying goes, a journey of a thousand miles begins with a single step. We see Streams as an essential first step towards that AI-enabled future. Without a working app that can deliver clinical information to nurses and doctors, AI alerts would be pointless. You can’t generate an AI recommendation from data held on pen and paper, and nor can you send detailed clinical alerts through a pager or fax machine.

When the time is right we hope to pursue research with the Royal Free, but would only do so with the appropriate approvals. For now, our work with them is focused on the more immediate problems that Streams helps to solve for clinicians and for patients.

You can read more about Streams and how it works [here](https://health.google/).
