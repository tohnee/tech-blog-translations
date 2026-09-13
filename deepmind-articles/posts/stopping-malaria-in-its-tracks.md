---
title: "Stopping malaria in its tracks"
source: https://deepmind.google/blog/stopping-malaria-in-its-tracks/
site: deepmind
date: 2022-10-13
authors: 
crawled: 2026-09-13
---

Developing a better malaria vaccine with the help of AI that could save hundreds of thousands of lives every year

When biochemist Matthew Higgins established his research group in 2006, he had malaria firmly in his sights. The mosquito-borne disease is second only to tuberculosis in terms of its devastating global impact. Malaria killed an estimated 627,000 people in 2020, mostly children under five, and almost half of the world’s population is within its reach, though Africa is by far the hardest hit. Symptoms of infection can begin with just a fever and a headache, making it easily missed or misdiagnosed – and therefore left untreated.

Preventing malaria is therefore the priority, which is why Higgins, a professor of molecular parasitology at the University of Oxford, has been working tirelessly with his team to understand how the malaria parasite interacts with human-host proteins. Their aim is to use these insights to design improved therapies, including a vaccine that will be much more effective than what is currently available.

![Professor Matthew Higgins photographed while using his computer.](https://lh3.googleusercontent.com/j2kRKelzJ6Y6uYaW9efvBg9UCqgBl5e6Erd751mbkHeJsh1Zp87oXH4FlObO09Dg86hVGRTJzN_-14dBAShNzQWFpm1cOZewlgMIPgeWUqEi5POiow=w1440)

When a human is bitten by an infected female mosquito, one of five types of malaria parasite may enter the bloodstream. These single-celled parasites are typically carried to the liver, where they mature and multiply, releasing more into the bloodstream. Symptoms such as fever, chills, fatigue, and sickness might not appear until 10 days to four weeks after infection occurs, yet the speed of diagnosis is critical. Of the five parasite species that cause malaria in humans, two are particularly dangerous. For example, an infection by Plasmodium falciparum can, if untreated, suddenly escalate to severe illness and death inside a day.

The key challenge for Higgins is the shapeshifting nature of malaria parasites. Their ability to constantly alter their appearance as well as that of their host (red blood) cells allows them to evade the human immune system. “In terms of drug, or vaccine, discovery, that makes it hard to pin it down and decide what to target,” he says. The possibility of a fully effective vaccine – the only way to stop malaria in its tracks – seemed remote.

![A scientist wearing goggles examines an object illuminated from underneath, by a harsh blue-tinted light.](https://lh3.googleusercontent.com/yq2AVKjT1yJq4PDynrExvyCo7z3bV5kcf5U6yZkEFJXu-lYCQlGiGaXCNOvDuyfKkyLNDjfFES8vms2EkVXQY4umX-ss0c_rjZwwZOrJKfW-1xFe-A=w1440)

The urgency of the race to develop an effective vaccine is underlined by the number of teams working towards that goal. Currently, RTS,S, widely known by its brand name Mosquirix, is the only approved inoculation. It was designed for children and in October 2021. Its arrival was a “huge advancement” and “very good news”, says Higgins. Because RTS,S targets only the first step of an infection, in which the malaria parasite is carried to the liver, it only has about a 30% efficacy rate. “30% is a big deal. It means a lot of lives saved,” he says. “But it’s a long way short of the 100% we want.”

> When we combined our model with Alphafold’s predicted structure, we could suddenly see how the whole system worked.

Matthew Higgins

Biochemist

More recently, another team at the University of Oxford – the Jenner Institute – reported promising results of another similar vaccine. Its approach, which consists of three doses followed by a booster one year later, has an efficacy rate of 77%. However, like Mosquirix, this vaccine intercepts at the first, pre-liver stage of the malaria parasite’s life cycle.

In contrast, Higgins - along with his Oxford-based collaborators Simon Draper and Sumi Biswas - is developing vaccine immunogens for a multi-stage vaccine that can simultaneously work at every phase of the infection cycle. Beyond the parasite’s initial entry into human liver cells, the lab’s ultimate goal is a vaccine that can not only target the blood-cell invasion that follows infection, but also the final reproductive stage of the parasite’s life cycle, which involves the fusion of its male and female gametes. It’s important to tackle this stage, because infected humans can otherwise transmit the parasite to previously uninfected mosquitoes if bitten again, continuing the cycle.

![Two scientists wearing white coats, working in a laboratory.](https://lh3.googleusercontent.com/GpY7oGnju7LBP7IUUHvVRkITD_DS5Nwdmpwt_mXeqRDEg9O6Vd_tMz_hzcOoiSILieB83P_PUpOLnoIAGvJcAuejkhMAQOJneSvrFeeyutr_dxVWkQ=w1440)

Progress has been hard-fought and slow. To illustrate why, consider the COVID-19 virus. This type of coronavirus has just one spike protein on its surface that a vaccine needs to target. The malaria parasites, on the other hand, have hundreds or even thousands of surface proteins, according to Higgins. And it’s a slippery shapeshifter.

Crucially, developing a vaccine that contains a critical infection-disrupting component requires knowing the molecular structure of one gamete surface protein – Pfs48/45 – essential to the development of the parasite in the mosquito midgut. This is where Higgins and his team got derailed. For years they tried to decipher the protein’s shape, with limited success. Even using two of the best experimental techniques available to discern a protein’s structure – X-ray crystallography and cryo-electron microscopy – the researchers could obtain only fuzzy, low-resolution images. As a result, their structural models of Pfs48/45 were necessarily imperfect and incomplete.

That was, until AlphaFold arrived.

“We’d been battling with this problem for years, trying to get the details we needed,” says Higgins. “Then we added AlphaFold into the mix. And when we combined our model with Alphafold’s predicted structure, we could suddenly see how the whole system worked.” Higgins recalls the exciting moment that his PhD student [Kuang-Ting Ko](https://higginslab.web.ox.ac.uk/kuang-ting-ko) – “who had been trying all sorts of different things to improve the experimental images” – burst into the office with the news.

> AlphaFold has allowed us to take our project to the next level, from a fundamental science stage to the preclinical and clinical development stage.

Matthew Higgins

“It was a great relief,” says Higgins, and a turning point for the project. The combination of laborious experimental work and AI prediction quickly resulted in a sharp view of Pfs48/45. “The crucial AlphaFold information enabled us to decide which bits of the protein we want to put in a vaccine and how we want to organize those proteins,” says Higgins. “AlphaFold has allowed us to take our project to the next level, from a fundamental science stage to the preclinical and clinical development stage.”

AlphaFold is not without its flaws, of course. Higgins noted that while the AI system worked well in predicting how each module within a protein adopts its structure, there were instances when its 3D visualizations were a little off. To get the most accurate and confident results, AlphaFold is best used alongside more traditional tools such as cryo-electron microscopy, he says. “I’m sure AlphaFold’s predictions will get better and better. But for now, combining experimental knowledge with AlphaFold models is the optimal approach, because it allows us to piece everything together. This is the approach which we are taking for many of our projects.”

![A pair of hands holding a 3D-printed molecular model of the Pfs48/45 malaria protein, with orange, blue, and yellow sections representing different domains.](https://lh3.googleusercontent.com/jsn_dAScr7xNND7mb7EfPiPGzXrefQy7q2PE2U1TXibJ--Qe2B2MM_1ya5_uwTnPuxW9Ke-xAPWAIifMUbLcBoK2kwUsOPl9tXoAmZnbKC_TDfk82g=w1440-h810-n-nu)

Higgins’ collaborator, Professor Sumi Biswas will be conducting a human clinical trial of Pfs48/45 in early 2023. Now that the structure of Pfs48/45 is understood, this will allow the Biswas and Higgins groups to work together to understand the immune response generated in these vaccination trials, and to design improved vaccines. In the pursuit of developing a vaccine that works at every stage of the malaria life cycle, Higgins is also making strides in understanding another target, a large protein complex key in the stage of malaria where the parasites infect the red blood cells, causing the onset of symptoms. Using a combination of AlphaFold and cryo-EM, the team is working hard to understand how this complex fits together.

Looking further up the road, Higgins envisions AlphaFold as a critical technology for creating new, useful proteins from scratch, a process known as de novo protein design. “The future of AlphaFold may not be so much in predicting the molecules which already exist in cells, but rather in predicting the structures of molecules that people are designing for specific applications, such as vaccines,” he says. “If we’re able to design proteins and then use AlphaFold to predict if they’ll fold up the way we need them to, that’s going to be very powerful.”
