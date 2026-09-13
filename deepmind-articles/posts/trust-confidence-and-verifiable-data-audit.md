---
title: "Trust, confidence and Verifiable Data Audit"
source: https://deepmind.google/blog/trust-confidence-and-verifiable-data-audit/
site: deepmind
date: 2017-03-09
authors: Mustafa Suleyman, Ben Laurie
crawled: 2026-09-13
---

Data can be a powerful force for social progress, helping our most important institutions to improve how they serve their communities. As cities, hospitals, and transport systems find new ways to understand what people need from them, they’re unearthing opportunities to change how they work today and identifying exciting ideas for the future.

Data can only benefit society if it has society’s trust and confidence, and here we all face a challenge. Now that you can use data for so many more purposes, people aren’t just asking about who’s holding information and whether it’s being kept securely – they also want greater assurances about precisely what is being done with it.

In that context, auditability becomes an increasingly important virtue. Any well-built digital tool will already log how it uses data, and be able to show and justify those logs if challenged. But the more powerful and secure we can make that audit process, the easier it becomes to establish real confidence about how data is being used in practice.

Imagine a service that could give mathematical assurance about what is happening with each individual piece of personal data, without possibility of falsification or omission. Imagine the ability for the inner workings of that system to be checked in real-time, to ensure that data is only being used as it should be. Imagine that the infrastructure powering this was freely available as open source, so any organisation in the world could implement their own version if they wanted to.

The working title for this project is “Verifiable Data Audit”, and we’re really excited to share more details about what we’re planning to build!

## Verifiable Data Audit for DeepMind Health

Over the course of this year we'll be starting to build out Verifiable Data Audit for [DeepMind Health](https://deepmind.com/about/health), our effort to provide the health service with technology that can help clinicians predict, diagnose and prevent serious illnesses – a key part of DeepMind’s mission to deploy technology for social benefit.

Given the sensitivity of health data, we’ve always believed that we should aim to be as innovative with governance as we are with the technology itself. We’ve already invited additional oversight of DeepMind Health by appointing a panel of unpaid [Independent Reviewers](https://deepmind.com/about/health) who are charged with scrutinising our healthcare work, commissioning audits, and publishing an annual report with their findings.

We see Verifiable Data Audit as a powerful complement to this scrutiny, giving our partner hospitals an additional real-time and fully proven mechanism to check how we’re processing data. We think this approach will be particularly useful in health, given the sensitivity of personal medical data and the need for each interaction with data to be appropriately authorised and consistent with rules around patient consent. For example, an organisation holding health data can’t simply decide to start carrying out research on patient records being used to provide care, or repurpose a research dataset for some other unapproved use. In other words: it’s not just where the data is stored, it’s what’s being done with it that counts. We want to make that verifiable and auditable, in real-time, for the first time.

So, how will it work? We serve our hospital partners as a data processor, meaning that our role is to provide secure data services under their instructions, with the hospital remaining in full control throughout. Right now, any time our systems receive or touch that data, we create a log of that interaction that can be audited later if needed.

With Verifiable Data Audit, we’ll build on this further. Each time there’s any interaction with data, we’ll begin to add an entry to a special digital ledger. That entry will record the fact that a particular piece of data has been used, and also the reason why - for example, that blood test data was checked against the NHS national algorithm to detect possible acute kidney injury.

The ledger and the entries within it will share some of the properties of [blockchain](https://en.wikipedia.org/wiki/Blockchain_(database)), which is the idea behind Bitcoin and other projects. Like blockchain, the ledger will be append-only, so once a record of data use is added, it can’t later be erased. And like blockchain, the ledger will make it possible for third parties to verify that nobody has tampered with any of the entries.

But it’ll also differ from blockchain in a few important ways. Blockchain is decentralised, and so the verification of any ledger is decided by consensus amongst a wide set of participants. To prevent abuse, most blockchains require participants to repeatedly carry out complex calculations, with huge associated costs (according to some estimates, the total energy usage of blockchain participants could be as much as the [power consumption of Cyprus](https://www.ft.com/content/384a349a-32a5-11e4-93c6-00144feabdc0)). This isn’t necessary when it comes to the health service, because we already have trusted institutions like hospitals or national bodies who can be relied on to verify the integrity of ledgers, avoiding some of the wastefulness of blockchain.

We can also make this more efficient by replacing the chain part of blockchain, and using a tree-like structure instead (if you’d like to understand more about Merkle trees, a good place to start would be [this blog](https://technology.blog.gov.uk/2015/10/13/guaranteeing-the-integrity-of-a-register/) from the UK’s Government Digital Service). The overall effect is much the same. Every time we add an entry to the ledger, we’ll generate a value known as a “cryptographic hash”. This hash process is special because it summarises not only the latest entry, but all of the previous values in the ledger too. This makes it effectively impossible for someone to go back and quietly alter one of the entries, since that will not only change the hash value of that entry but also that of the whole tree.

In simple terms, you can think of it as a bit like the last move of a game of Jenga. You might try to gently take or move one of the pieces - but due to the overall structure, that’s going to end up making a big noise!

So, now we have an improved version of the humble audit log: a fully trustworthy, efficient ledger that we know captures all interactions with data, and which can be validated by a reputable third party in the healthcare community. What do we do with that?

The short answer is: massively improve the way in which these records can be audited. We’ll build a dedicated online interface that authorised staff at our partner hospitals can use to examine the audit trail of DeepMind Health’s data use in real-time. It will allow continuous verification that our systems are working as they should, and enable our partners to easily query the ledger to check for particular types of data use. We’d also like to enable our partners to run automated queries, effectively setting alarms that would be triggered if anything unusual took place. And, in time, we could even give our partners the option of allowing others to check our data processing, such as individual patients or patient groups.

## The technical challenges ahead

Building this is going to be a major undertaking, but given the importance of the issue we think it’s worth it. Right now, three big technical challenges stand out.

**No blind spots.** For this to be provably trustworthy, it can’t be possible for data use to take place without being logged in the ledger - otherwise, the concept falls apart. As well as designing the logs to record the time, nature and purpose of any interaction with data, we’d also like to be able to prove that there’s no other software secretly interacting with data in the background. As well as logging every single data interaction in our ledger, we will also need to use [formal methods](https://en.wikipedia.org/wiki/Formal_methods) as well as code and data centre audits by experts, to prove that every data access by every piece of software in the data centre is captured by these logs. We’re also interested in efforts to guarantee the trustworthiness of the hardware on which these systems run - an active topic of computer science research!

**Different uses for different groups.** The core implementation will be an interface to allow our partner hospitals to provably check in real-time that we’re only using patient data for approved purposes. If these partners wanted to extend that ability to others, like patients or patient groups, there would be complex design questions to resolve.

A long list of log entries may not be useful to many patients, and some may prefer to read a consolidated view or rely on a trusted intermediary instead. Equally, a patient group may not have the authority to see identified data, which would mean allowing our partners to provide some form of system-wide information - for example, whether machine learning algorithms have been run on particular datasets - without unintentionally revealing patient data.

For technical details on how we could provide verified access to subsets or summaries of the data, see the open source [Trillian](https://github.com/google/trillian) project, which we will be using, and this [paper explaining how it works](https://github.com/google/trillian/blob/master/docs/papers/VerifiableDataStructures.pdf).

**Decentralised data and logs, without gaps.** There’s no single patient identified information database in the UK, and so the process of care involves data travelling back and forth between healthcare providers, IT systems, and even patient-controlled services like wearable devices. There’s a lot of work going into making these systems interoperable (our mobile product, [Streams, is built to interoperable standards](https://deepmind.com/about/health)) so they can work safely together. It would be helpful for these standards to include auditability as well, to avoid gaps where data becomes unauditable as it passes from one system to another.

This doesn’t mean that a data processor like DeepMind should see data or audit logs from other systems. Logs should remain decentralised, just like the data itself. Audit interoperability would simply provide additional reassurance that this data can’t be tampered with as it travels between systems.

This is a significant technical challenge, but we think it should be possible. Specifically, there’s an emerging open standard for interoperability in healthcare called FHIR, which could be extended to include auditability in useful ways.

## Building in the open

We’re hoping to be able to implement the first pieces of this later this year, and are planning to blog about our progress and the challenges we encounter as we go. We recognise this is really hard, and the toughest challenges are by no means the technical ones. We hope that by sharing our process and documenting our pitfalls openly, we’ll be able to partner with and get feedback from as many people as possible, and increase the chances of this kind of infrastructure being used more widely one day, within healthcare and maybe even beyond.
