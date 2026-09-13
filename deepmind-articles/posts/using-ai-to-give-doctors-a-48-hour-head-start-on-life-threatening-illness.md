---
title: "Using AI to give doctors a 48-hour head start on life-threatening illness"
source: https://deepmind.google/blog/using-ai-to-give-doctors-a-48-hour-head-start-on-life-threatening-illness/
site: deepmind
date: 2019-07-31
authors: Mustafa Suleyman, Dominic King
crawled: 2026-09-13
---

Artificial intelligence can now predict one of the leading causes of avoidable patient harm up to two days before it happens, as demonstrated by [our latest research published in Nature](https://nature.com/articles/s41586-019-1390-1). Working alongside experts from the US Department of Veterans Affairs (VA), we have developed technology that, in the future, could give doctors a 48-hour head start in treating acute kidney injury (AKI), a condition that is associated with over [100,000 people](https://www.england.nhs.uk/akiprogramme/) in the UK every year. These findings come alongside a peer-reviewed service evaluation of Streams, our mobile assistant for clinicians, which shows that patient care can be improved, and health care costs reduced, through the use of digital tools. Together, they form the foundation for a transformative advance in medicine, helping to move from reactive to preventative models of care.

Millions of people die every year from diseases that could have been prevented with earlier detection. One such disease is acute kidney injury (AKI), a condition where a patient’s kidney suddenly stops working properly. Affecting up to one in five hospitalised patients in [the UK](https://improvement.nhs.uk/documents/251/Patient_Safety_Alert_Stage_2_-_AKI_resources.pdf) and [the US](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3362180/), the condition is notoriously difficult to spot, and deterioration can happen quickly. [Experts](https://www.ncepod.org.uk/2009aki.html) believe that up to 30% of cases could be prevented if a doctor intervenes early enough.

> Such digital technologies will undoubtedly open up new possibilities for timely clinical interventions and treatments to reduce harm to patients.

Professor Jeremy Hughes

Chair of Kidney Research UK

Over the last few years, our team at DeepMind has focused on finding an answer to the complex problem of avoidable patient harm, building digital tools that can spot serious conditions earlier and helping doctors and nurses deliver faster, better care to patients in need. This is our team’s biggest healthcare research breakthrough to date, demonstrating the ability to not only spot deterioration more effectively, but actually predict it before it happens.

Working with the VA, the DeepMind team applied AI technology to a comprehensive de-identified electronic health record dataset collected from a network of over a hundred VA sites. The [research](https://www.nature.com/articles/s41586-019-1390-1) shows that the AI could accurately predict AKI in patients up to 48 hours earlier than it is currently diagnosed. Importantly, the model correctly predicted 9 out of 10 patients whose condition deteriorated so severely that they then required dialysis. This could provide a window in the future for earlier preventative treatment and avoid the need for more invasive procedures like kidney dialysis. The model has also been designed so that it might, in the future, generalise to other major causes of diseases and deterioration such as sepsis, a life-threatening infection.

To address the ‘black box’ problem – one of the key barriers for the implementation of AI in clinical practice – the model also provides the clinical information that was most important in making its predictions of deteriorating kidney function. It also provides predicted future results for several relevant blood tests. This information may help clinicians understand the reasoning behind the AI-enabled alert and anticipate future patient deterioration.

However, these predictions can’t help real patients without the right tools to alert specialists. Clinicians routinely use pagers, paper records and fax machines to communicate with each other, but better technology is desperately needed so that critical information can be delivered to the right specialist at the right time. That’s why we’re also pleased to report that the results of a peer-reviewed evaluation of our mobile medical assistant Streams have also been published today. This work was conducted by researchers at University College London.

![Flowchart comparing a slow, manual "Pre-implementation pathway" for detecting and escalating AKI with a fast, automated "Digitally-enabled care pathway" using the Streams mobile app.](https://lh3.googleusercontent.com/Ru0HRA9qh_fBIxIO0MoXkcbeN3yYk_c2qzK4tmNPgsmveMh0hjKNzf4gBRpoGK8DmkjZXmFzNqAeDPlGMS6ZoYWq8cU4vyP2bZWJx22zaWq3p_Nw2A=w1440)

An illustration how an at-risk patient is flagged in the traditional vs. digitally-enabled care pathway

Streams is a mobile medical assistant for clinicians, and has been in use at the Royal Free London NHS Foundation Trust since early 2017. The app uses the existing national AKI algorithm to flag patient deterioration, supports the review of medical information at the bedside, and enables instant communication between clinical teams. Shortly after rolling out at the Royal Free, clinicians [said](https://www.royalfree.nhs.uk/news-media/news/new-app-helping-to-improve-patient-care/) that Streams was saving them up to two hours a day. We also heard about patients, like [Afia Ahmad](http://www.standard.co.uk/news/health/new-mother-receives-pioneering-kidney-treatment-after-app-detects-lifethreatening-illness-a3476936.html), whose treatment was escalated thanks to the app. But we wanted to quantify these benefits through robust clinical evaluation. Today’s results show that the app saved clinicians’ time, improved care and reduced the number of AKI cases being missed at the hospital.

By using Streams, [specialists reviewed urgent cases within 15 minutes or less](https://www.nature.com/articles/s41746-019-0100-6)(a process that might otherwise have taken several hours) and fewer cases of AKI were missed (3.3% rather than 12.4%). The app also [reduced the average cost of admission](https://www.jmir.org/2019/7/e13147/) for a patient with AKI by 17%, demonstrating a huge potential cost saving for hospitals in the future, considering that AKI costs the NHS [more than £1 billion](https://academic.oup.com/ndt/article/29/7/1362/1844079) each year.

> This is a game changer that will advance our care and understanding of acute kidney injury.

Donal O'Donoghue

Professor of Renal Medicine at the University of Manchester, Chair of Trustees of Kidney Care UK

Feedback from [the qualitative study](https://www.jmir.org/2019/7/e13143/) was positive, with healthcare professionals emphasising the ways in which the app accelerated the detection of patients in need, saved them time in performing administrative tasks, and improved team communication. One respondent said the app “streamlines care, and speeds up the time in which they get a specialist renal review.” Another clinician from the nephrology team stated that “Being able to look up the blood results for anyone in the hospital wherever you are is unparalleled...it must save at least – I don’t know if you could analyse it – but it must save at least a couple of hours in a day.”

Getting the right information about the right patient at the right time is a huge problem for healthcare systems across the globe. Critically, these early findings from the Royal Free suggest that, in order to improve patient outcomes even further, clinicians need to be able to intervene before AKI can be detected by the current NHS algorithm – which is why our research on AKI is so promising. These results comprise the building blocks for our long-term vision of preventative healthcare, helping doctors to intervene in a proactive, rather than reactive, manner.

Streams doesn’t use artificial intelligence at the moment, but the team now intends to find ways to safely integrate predictive AI models into Streams in order to provide clinicians with intelligent insights into patient deterioration.

This is a major milestone for the DeepMind Health team, who will be carrying this work forward as part of Google Health, led by Dr David Feinberg. As we [announced](https://deepmind.com/blog/announcements/scaling-streams-google) in November 2018, the Streams team, and colleagues working on translational research in healthcare, will be joining Google in order to make a positive impact on a global scale. The combined experience, infrastructure and expertise of DeepMind Health teams alongside Google’s will help us continue to develop mobile tools that can support more clinicians, address critical patient safety issues and could, we hope, save thousands of lives globally.
