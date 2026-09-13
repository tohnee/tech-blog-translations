---
title: "The race to cure a billion people from a deadly parasitic disease"
source: https://deepmind.google/blog/the-race-to-cure-a-billion-people-from-a-deadly-parasitic-disease/
site: deepmind
date: 2022-07-28
authors: 
crawled: 2026-09-13
---

Researchers accelerate their search of life-saving treatments for leishmaniasis

“We were about to give up,” says Dr Benjamin Perry, a medicinal chemist at the [Drugs for Neglected Diseases initiative (DNDi)](https://dndi.org/). When Perry joined the organization seven years ago, based in Geneva, Switzerland, his goal was to speed up the discovery of new treatments for two potentially fatal parasitic illnesses, [Chagas disease](https://dndi.org/diseases/chagas/) and [leishmaniasis](https://dndi.org/diseases/visceral-leishmaniasis/). By and large, they achieved a lot of success. For one potential leishmaniasis drug in DNDi’s diverse portfolio, however, progress had slowed almost to a halt.

“We couldn’t find ways of making changes that improved the drug molecule,” says Perry. “It either lost all its potency as an anti-parasitic or it kind of stayed the same.”

However, things changed when Perry and his collaborators heard about DeepMind’s AI system, AlphaFold. Now, using a combination of scientific detective work and AI, the researchers have cleared a path towards turning the molecule into a real treatment for a devastating disease.

New treatments for leishmaniasis can’t come soon enough. The disease is caused by parasites of the genus Leishmania and spreads through sandfly bites in countries across [Asia, Africa, the Americas, and the Mediterranean](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5464238/).

Visceral leishmaniasis, the most severe form, causes fever, weight loss, anemia, and enlargement of the spleen and liver. “If it’s not treated, it is fatal,” says Dr Gina Muthoni Ouattara, senior medical manager at DNDi in Nairobi, Kenya. Cutaneous leishmaniasis, the most common form, causes skin lesions and leaves lasting scars.

![A nurse in a blue uniform and face mask checks the blood pressure of a patient in a red shirt in a hospital ward.](https://lh3.googleusercontent.com/WwYKbhvKyg9o-SYCCHjVbESutcTgp8Vc4C1d_UBnigKfrBP5eCgxCyHRhKpC2a_yubHZN-LHTDbtt632cufUqCK91iAsjQKLSE6QrBxKvAotcnAhxg=w1440)

A patient with visceral leishmaniasis and an HIV co-infection. Credit: University of Gondar

Globally, about [a billion people are at risk of leishmaniasis](https://www.who.int/health-topics/leishmaniasis#tab=tab_1) and each year there are [50-90,000 new cases of visceral leishmaniasis](https://dndi.org/diseases/visceral-leishmaniasis/facts/), the majority in children. While medical treatments vary by region, most are lengthy and come with significant side effects.

In Eastern Africa, the first-line treatment for visceral leishmaniasis involves a 17-day course of two injections each day, of two separate drugs, [sodium stibogluconate and paromomycin](https://dndi.org/research-development/portfolio/ssg-pm/), given in hospital. "Even for an adult, these injections are very painful, so you can imagine having to give these two injections to a child every day for 17 days,” says Ouattara. Before DNDi’s crucial work to develop a shorter and more effective combination therapy, this treatment lasted for 30 days.

An alternative treatment requires an intravenous infusion that needs to be kept refrigerated and administered under sterile conditions. “The most limiting thing is that all of these treatments have to be given in hospital,” says Ouattara. That adds to the costs, and means patients and their caregivers miss out on income, school, and time with their family. “It really affects communities.”

> People always ask themselves, ‘Have we looked at the AlphaFold structure?’ It’s become common parlance.

Michael Barrett

Biochemist and Parasitologist

DNDi’s previous efforts have already cut the amount of time visceral leishmaniasis patients spend in hospital. But the organization’s ultimate goal is to come up with an oral treatment that could be administered at a local health facility, or even at home.

That kind of radical improvement might require entirely new drugs. If you’re looking for completely new compounds to turn into treatments, where do you start?

DNDi’s approach to drug discovery in this area of research could be called “old school”, says Perry, though he maintains there’s a reason for that – it’s often the best way to discover drugs. First, researchers screen thousands of molecules to find those that show promise in attacking the disease-causing organism as a whole. Then, they tweak those molecules to try to make them more effective. “It’s a bit more ‘brute force’,” he says. “We don’t usually know how it’s doing it.”

![Headshots of Dr. Benjamin Perry, a medicinal chemist, on the left, and Dr. Gina Muthoni Ouattara, senior medical manager at DNDi, on the right.](https://lh3.googleusercontent.com/HLwnqO1RVdk8L702JW4apr4nwf6nHmlOXhdx_DAlR5G6Tvcq6sQf7BI9MYrj4oxIu0MI2_HWT4WzJ4XftB-jNA5if41dRjDqBpDfvatK62s5iAii=w1440)

Benjamin Perry and Gina Muthoni Ouattara. Credit: DNDi

This trial-and-error approach is the best way to find new treatments for patients, says Perry. But the optimisation stage can feel a bit like stumbling around in the dark. “You're going ‘Okay, well, I've got this chemical, just make some random changes to it’ which works sometimes,” says Perry. But with their promising leishmaniasis molecule, they’d hit a brick wall. “We’d tried that and it hadn't worked.”

With hope dwindling, DNDi sent the molecule to [Michael Barrett](https://www.gla.ac.uk/researchinstitutes/iii/staff/michaelbarrett/), a professor at the University of Glasgow, UK, who for the last decade has been using a technique called [metabolomics](https://en.wikipedia.org/wiki/Metabolomics) to unravel how drugs work.

“There are all sorts of chemical processes occurring in our body where we chop molecules down into their component building blocks and then rebuild them,” says Barrett. “That's the basis of life, really.” Collectively, these chemical reactions make up our metabolism. Parasites, like the one that causes leishmaniasis, have a metabolism too.

Metabolic reactions are regulated by biological catalysts known as enzymes. Many drugs work by interfering with those enzymes, so Barrett and his group look for changes in the molecules that are made during metabolic reactions to figure out what a drug is doing.

He put DNDi’s molecule on to a Leishmania parasite. “Sure enough, the metabolism changed,” he says. Barrett and his colleagues saw a big increase in one molecule whose job is to turn into phospholipids, a type of fat molecule that makes up cell membranes. Yet at the same time, the number of phospholipids actually being made was decreasing.

Barrett figured out that the enzyme that would have turned the first molecule into phospholipids was the one that was being affected by the drug. Interrupting this reaction was how the molecule was killing the parasite.

![A male nurse in a white uniform with a stethoscope around his neck writes on a clipboard while a female nurse in a blue uniform looks on in a hospital ward.](https://lh3.googleusercontent.com/78RmN25tJcSKWNd4cB0S4J8oYtL6QiShL2CQ8UAJJmBK6rSpR5JxhQZ2Gc9rMo86VpUXuvTaCcifNJM-20WicYVeOAoScanrxf0RY3IDW7gGxeOl=w1440)

Stella Akiror and John Oseluo taking down details after checking on a patient. Credit: Lameck Ododo - DNDi

But having hurdled one obstacle, Barrett’s group hit another. They wanted to know what their target enzyme looked like, but finding its structure experimentally would be near impossible because it was a type of protein that is notoriously hard to work with in the lab. “It embeds itself in the membrane, and that makes it really difficult to fiddle with,” says Barrett.

That could have been the end of the story. But instead Perry put Barrett in touch with researchers at DeepMind who were working on [AlphaFold](https://www.deepmind.com/research/highlighted-research/alphafold), an AI system that predicts a protein’s 3D structure from its amino acid sequence. The AlphaFold team took the target protein’s amino acid sequence and came back with exactly what Barrett and his colleagues needed: a prediction for its 3D structure.

Barrett’s group took that structure, and the structure of DNDi’s molecule, and were able to figure out how they fit together – pinning down, virtually at least, how the drug binds to the protein.

> Most of the diseases we work with are endemic in countries where the [scientific] infrastructure is not necessarily that great.

Benjamin Perry

Medicinal Chemist

Since then, DeepMind, in partnership with EMBL’s European Bioinformatics Institute, has made [a database of millions of protein structures](https://alphafold.ebi.ac.uk/) available to researchers. An open source implementation of the AlphaFold system is [also available](https://github.com/deepmind/alphafold). “Anybody can now just take their protein amino acid sequence, plug it into AlphaFold and get a structure out,” says Barrett. “It’s revolutionary.”

“This, for me, is the biggest change that AlphaFold has made to the scientific environment,” says Perry. “People always ask themselves, ‘Have we looked at the AlphaFold structure?’ It’s become common parlance."

Having access to protein structure predictions is proving useful for drug-discovery researchers in many ways.

There are more than 20 different species of the Leishmania parasite that cause disease in humans, but Barrett’s group works with a single species, Leishmania mexicana. While much of what they find translates to others, it’s not a given – so they need to cross-check any findings. “We can get the Leishmania donovani version of that target gene, we can put that through the AlphaFold algorithm very quickly and see, does the donovani version fold in the same way as the mexicana version?”

There is also a human version of the target enzyme Barrett identified in the Leishmania parasite. Researchers will need to make sure that only the parasite’s version of the enzyme comes under attack from a new drug, to avoid potential side effects for patients – something that will be easier if they know what the human version looks like. “We got that structure from AlphaFold as well,” says Perry.

Of course, AlphaFold can’t accurately fold every possible protein. And for those it can, the structure alone doesn’t provide everything drug discovery researchers need. The next step-change would be to develop an AI system able to predict docking – taking the structure, and the drug, and figuring out where they fit together.

While there is still a long way to go before the molecule Barrett unraveled becomes a real treatment against leishmaniasis – if it ever gets there – it has demonstrated that AlphaFold can lower a barrier when it comes to investigating new drugs. For researchers hunting down new treatments for neglected diseases, where funding is often tight, this could make all the difference.

When drug discovery researchers are in the dark about how to optimize a promising molecule, moving beyond quick-and-easy tweaks means investing a lot more time and money. When funding is scarce, that’s a harder sell. “We can’t throw kitchen sinks at issues in neglected tropical diseases because the money’s not there,” says Barrett.

But a tool like AlphaFold could be accessible to researchers who can’t use expensive equipment to pin down the chemistry of their compounds. “Most of the diseases we work with are endemic in countries where the infrastructure is not necessarily that great,” says Perry.

If AlphaFold can help unravel how a molecule acts against a disease by making visible the structure the drug is targeting – as it has done with DNDi’s potential new leishmaniasis drug – it could also illuminate a path for medicinal chemists like Perry to turn a dead-end molecule into a real treatment. “We couldn’t look at this fancy way that our molecule interacts with the structure and say, we just need another carbon here, or get rid of that nitrogen, move this around – that sort of stuff was off-limits for us,” he says. “Except, now, it isn't.”
