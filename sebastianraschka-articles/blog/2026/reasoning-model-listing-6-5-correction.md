---
title: "Reasoning Book Listing 6.5 Correction"
source: https://sebastianraschka.com/blog/2026/reasoning-model-listing-6-5-correction.html
crawled: 2026-09-06
---

# Reasoning Book Listing 6.5 Correction

Thanks everyone for all the kind words and feedback. Super happy that you are enjoying *Build a [Reasoning Model](https://sebastianraschka.com/glossary/#reasoning-model "Reasoning Model") (From Scratch)*!

Unfortunately, there’s a small typo in Listing 6.5 on page 198 (see the video below). The line `torch.manual_seed(0)` should be `torch.manual_seed(5)`.

This is a tiny change, but it’s needed to reproduce the generated response in Listing 6.5 and the corresponding log-probability outputs later in Chapter 6. If you use 0, the code is of course still correct but the numeric results may be a bit different, which could be confusing. Anyway, it should be a small 1 character change :).

This will be fixed in the next printing.

I am sorry about the oversight, and I hope this note saves you some debugging time.

Source: lightly edited website version of my [Substack note](https://substack.com/@rasbt/note/c-301484736).
