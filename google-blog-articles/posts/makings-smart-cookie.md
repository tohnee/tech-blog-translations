---
title: "The makings of a smart cookie"
source: https://blog.google/innovation-and-ai/technology/research/makings-smart-cookie/
site: google-blog
date: 2017-12-04
authors: Daniel Golovin
crawled: 2026-09-13
---

Now that the holidays are in full swing, you’ve probably already dipped your hand into the cookie jar. You may have a favorite time-tested holiday cookie recipe, but this year we decided to mix up our seasonal baking with two new ingredients: a local bakery in Pittsburgh and our [Google AI](https://ai.google/) technology.

Over the past year, a small research team at Google has been experimenting with a new technology for experimental design. To demonstrate what this technology could do, our team came up with a real-world challenge: designing the best possible chocolate chip cookies using a given set of ingredients. Adding to the allure of this project was the fact that our team works out of Google’s Pittsburgh office, which was once an old Nabisco factory.

Using a technique called “[Bayesian Optimization](https://cloud.google.com/blog/big-data/2017/08/hyperparameter-tuning-in-cloud-machine-learning-engine-using-bayesian-optimization),” the team stepped away from their computers and rolled their sleeves up in the kitchen. First, we set a bunch of (metaphorical) knobs—in this case, the ingredients in the cookie recipe, i.e., type of chocolate; quantity of sugar, flour, vanilla, etc. The ingredients provide enough unique variables to manipulate and measure, and the recipe is easy to replicate. Our system guessed at a first recipe to try. We baked it, and our eager taste-testers—Googlers ready and willing to sacrifice for science by eating the cookies—tasted it and gave it a numerical score relative to store-bought cookie samples. We fed that rating back into the system, which learned from the rating and adjusted those “knobs” to create a new recipe. We did this dozens of times—baking, rating, and feeding it back in for a new recipe—and pretty soon the system got much better at creating tasty recipes.

After coming up with a really good recipe within Google, we wanted to see what an expert could do with our “smart cookie.” So Chef John, our lead chef in the office teaching kitchen, introduced the team to Jeanette Harris of the [Gluten Free Goat Bakery & Cafe](http://glutenfreegoat.com/). Jeanette was diagnosed with [Celiac](https://g.co/kgs/RTaAzs) over 10 years ago and she turned her passion for baking into an opportunity to offer treats to those who usually can’t partake. “When John came to me with the idea of creating an AI-generated cookie I didn’t know what to expect,” says Jeanette. “I run a small local bakery and take great care to ensure I’m providing safe, quality ingredients to my customers. But once the team took the time to explain what they were trying to do, I was all in!”

Working out of the Goat Bakery kitchen, Chef John and Jeanette mixed and matched some unusual ingredients like cardamom and szechuan pepper, using the measurements provided by Google’s system. Two months and 59 test batches later, the culinary duo came up with a new take on the classic chocolate chip cookie: The Chocolate Chip and Cardamom Cookie.

![Smart Cooke_Recipe.png](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Smart_Cooke_Recipe.width-1200.format-webp.webp)

“This was such a fun experiment! Being able to create something entirely new and different, with the help of AI, was so exciting and makes me wonder what other unique recipe concepts I can develop for my customers,” Jeanette says.

![SmartCookie_1.jpg](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/SmartCookie_1.width-100.format-webp.webp)

Jeanette Harris, John Karbowski, Daniel Golovin and Greg Kochanski present the Chocolate Chip and Cardamom "Smart" Cookie at the Gluten Free Goat Bakery.

![SmartCookie_2.jpg](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/SmartCookie_2.width-100.format-webp.webp)

Left: Jeanette Harris does a live cooking demo.

![SmartCookie_3.jpg](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/SmartCookie_3.width-100.format-webp.webp)

John Karbowski, Jeanette Harris and Daniel Golovin sample the tasty treat.

![SmartCookie_4.jpg](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/SmartCookie_4.width-100.format-webp.webp)

Demo station at Gluten Free Goat Bakery.

The smart cookie experiment is a taste of what’s possible with AI. We hope it gets you thinking about what kinds of things you can bake up with it.
