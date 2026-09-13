---
title: "Sharing our insights from designing with clinicians"
source: https://deepmind.google/blog/sharing-our-insights-from-designing-with-clinicians/
site: deepmind
date: 2017-11-10
authors: 
crawled: 2026-09-13
---

[Editor’s note: this is the first in a series of blog posts about what we’ve learned about working in healthcare. It’s both exceptionally hard and exceptionally important to get right, and we hope that by sharing our experiences we’ll help other health innovators along the way]

In our design studio, we have [Indi Young’s](http://indiyoung.com/) mantra on the wall as a reminder to “fall in love with the problem, not the solution”. Nowhere is this more true than in health, where there are so many real problems to address, and where introducing theoretically clever but practically flawed software could easily do more harm than good.

Over the course of hundreds of hours of shadowing, interviews and workshops with nurses, doctors and patients, we’ve been privileged to learn a lot about some of the problems they all face - and we’re still learning a ton every day. We are constantly impressed by the skill and care that clinicians across the NHS deliver every day, and this is the primary motivation for our team to ensure that these people get the tools they need to appropriately support them in their quest to help patients. In the first of a series of posts about what we’ve learned through working in health, we wanted to share some of the design lessons from building Streams, a secure clinical mobile app that gives the right information to the right clinician at the right time.

## Start with empathy

Most products begin with an insight into one core problem. In the case of Streams, it was that urgent clinical information gets retrieved by nurses and doctors over a mixture of outdated desktop computers, pager messages and handwritten lists. This contributes towards delays in care and occasionally serious harm if something is missed, and a 2017 study found that nearly half of emergency response time is wasted due to inefficient communication between systems.

Surely a secure mobile app like Streams that immediately pushes urgent clinical information directly to the right nurse or doctor would be a better solution? We think so, yes. But as we learned more about the working lives of clinicians, and the phenomenon of “bleeper fatigue” - with many doctors telling us that they receive over 100 notifications a day already - we started to recognise how a solution might actually become another problem if we ended up contributing to the general bombardment of messages.

It turns out that there’s a very fine line between alerts that clinicians find useful, and alerts that become a nuisance - and much of this seems to come down to the precise way in which data is presented in the app. For example, clinicians told us that when reviewing a patient’s record in the hospital, they need to see a patient’s hospital number, their allergies and details of previous admissions, rather than the traditional format of listing NHS number and GP practice. This was easy to fix with a subtle change in information architecture, which addressed something that many clinicians found to be more irritating than we initially thought!

![A design team gathers around a wall filled with user journey maps and sticky notes to discuss the design of the Streams app.](https://lh3.googleusercontent.com/uz4oLaL3qrMKOJM8T-rmLrS9QocNdobsFmNDxwv4MAaUODDnJddfvvJs4j9Jg5KkhWbAC_HLnwv2B5p4XBMoxyqK9yhWgZI7fvqb-VmMSH_Vyvr_dIo=w1440)

We also found by using the colour red in the interface intentionally and in a measured way, we could improve how people navigated content and better draw attention to information which needs urgent action. The sound designer on our team also worked directly with healthcare workers to produce a unique sound that would be immediately recognisable amidst the din of other bleeps and alerts.

While these might seem like relatively minor design choices, clinicians told us of the surprisingly large impact it had on managing their busy time, and how likely they were to use the product in practice.

## Expecting the unexpected

Design doesn’t stop at deployment. Good health IT should empower nurses and doctors to change the way they care for patients. Each change creates a new reality, with its own set of new problems - and new opportunities to make a difference.

For example, once we’d deployed Streams at the Royal Free Hospital in January 2017, clinicians told us that the app needed a better way to support communication between teams and across specialties. While they wanted urgent alerts to be sent to multiple clinicians at the same time, to increase the likelihood of a rapid response, it wasn’t easy enough for each of those clinicians to see if their colleagues were also responding - which in some cases could actually have hindered coordination, rather than improving it. We supported their need to triage alerts by giving clinicians the one-click ability within the app to “recommend a response”, “dismiss a response” or indicate that a patient had been attended to, and for this to be visible across the clinical team.

Another area that surprised us was the urgency of creating a patient-friendly view within the app. From the beginning, our patient advisors championed the need for a way for patients to see their data within Streams, and so this had always been on our roadmap. But we hadn’t factored in just how important this might be right away.

![A medical professional uses the Streams app. They are turned away from the camera, we cannot see their face. They are standing in front of boxes of medical equipment.](https://lh3.googleusercontent.com/KGAiyu8M8R_J9PINR3THaAWTnFcvTewsRUjNpDQ0IqLB3_70SnLPT3faf1Rx9xAsMHc5UBDOpT7shRjgEGhEC0ECkB3FRtEJ155Pj9YAkXoK3I5HLac=w1440)

While it’s normal to see clinicians carrying paper notes and pagers on the wards, many patients were surprised to see staff walking around looking at an app on their mobile phones. In some cases, patients assumed that clinicians must be on personal social networking or messaging apps - rather than using an app specifically designed to support their care - and challenged them directly about what they were doing!

These moments provided opportunities for clinicians to really engage patients in their care, by showing them the data in the Streams app and talking through what it meant for their treatment. The challenge was that the default Streams views are designed for highly-trained clinicians, with graphs and notations that are hard to understand for the layperson. We are now looking into making the app more patient-friendly, providing a new way to strengthen and support the clinician-patient relationship.

This kind of post-deployment insight could only have come through ongoing face-to-face feedback from nurses, doctors and patients. Typical app usage metrics might be useful for developers in other domains, but in a field like health they will almost always miss the point. What’s important isn’t how health IT is used in itself, but rather the changes it enables in the person-to-person context of care: whether it improves or impairs the caring relationship between clinicians and their patients, or whether it empowers or stresses out overstretched clinical teams. The answers lie in the conversations, not the usage data. In a future blog, we'll talk in more detail about what we've learned from our dedicated patient involvement efforts too.

## Learning from others

Our approach is constantly informed by the great work of other people and organisations working across the field. So far we’ve been drawing on best practices in user-centred design and agile development from the likes of the Royal College of Art's [Healthcare Innovation Exchange Centre](https://www.rca.ac.uk/research-innovation/helix-centre/), [Prescribe Design](http://prescribedesign.com/), [Stanford Biodesign](http://biodesign.stanford.edu/) and the [Mayo Innovation Centre](http://centerforinnovation.mayo.edu/). [This article](https://www.team-consulting.com/insights/an-agile-approach-to-medical-device-design/), by Carl Warren at Team Consulting, provides a good explanation of how agile processes can be used in medical technology, for those curious to learn more.

We hope Streams continues to evolve with the help of patients, clinicians and nurses, and that the lessons we’ve learned are useful to other innovators in health! If you work in healthcare and want to be involved in our future work, please register your interest [here](https://deepmind.com/about/health).

To learn more about how Streams is having an impact on the wards, listen to Sarah Stanley, consultant nurse at The Royal Free London NHS Foundation Trust below:
