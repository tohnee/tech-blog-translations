---
title: "A closer look at the research to help AI see more skin tones"
source: https://blog.google/innovation-and-ai/technology/research/ai-monk-scale-skin-tone-story/
site: google-blog
date: 2022-05-11
authors: Molly McHugh-Johnson
crawled: 2026-09-13
---

Today at I/O [we released the Monk Skin Tone (MST) Scale](https://www.blog.google/products/search/monk-skin-tone-scale/) in partnership with Harvard professor and sociologist [Dr. Ellis Monk](https://www.ellismonk.com/). The MST Scale, developed by Dr. Monk, is a 10-shade scale designed to be more inclusive of the spectrum of skin tones in our society. We’ll be incorporating the MST Scale into various Google products over the coming months, and we are openly releasing the scale so that anyone can use it for research and product development.

The MST Scale is an important next step in a collective effort to improve skin tone inclusivity in technology. For Google, it will help us make progress in our commitment to image equity and improving representation across our products. And in releasing the MST Scale for all to use, we hope to make it easier for others to do the same, so we can learn and evolve together.

Addressing skin tone equity in technology poses an interesting research challenge because it isn’t just a technical question, it’s also a social one. Making progress requires the combined expertise of a wide range of people — from academics in the social sciences who have spent years studying social inequality and skin tone stratification through their research, to product and technology users, who provide necessary nuance and feedback borne of their lived experiences, to ethicists and civil rights activists, who guide on application frameworks to ensure we preserve and honor the social nuances. The ongoing and iterative work from this wider community has led us to the knowledge and understanding that we have today, and will be key to the continued path forward.

Teams within Google have been contributing to this body of work for years now. Here’s a deeper look at how Googlers have been thinking about and working on skin tone representation efforts, particularly as it relates to the MST Scale — and what might come next.

### Building technology that sees more people

“Persistent inequities exist globally due to prejudice or discrimination against individuals with darker skin tones, also known as colorism,” says Dr. Courtney Heldreth, a social psychologist and user experience (UX) researcher in Google’s Responsible AI Human-Centered Technology UX (RAI-HCT UX) department, which is part of Google Research. “The [academic literature](https://direct.mit.edu/daed/article-pdf/150/2/76/1897805/daed_a_01847.pdf) demonstrates that skin tone plays a significant role in how people are treated across a wide variety of outcomes including health, wealth, well-being, and more.” And one example of colorism is when technology doesn’t see skin tone accurately, potentially exacerbating existing inequities.

Machine learning, a type of AI, is the bedrock of so many products we use every day. Cameras use ML for security reasons, to unlock a phone or register that someone is at the door. ML helps categorize your photos by similar faces, or adjust the brightness on a picture.

To do this well, engineers and researchers need diverse training datasets to train models, and to extensively test the resulting models across a diverse range of images. Importantly, in order to ensure that datasets used to develop technologies relating to understanding people are more inclusive, we need a scale that represents a wide range of skin tones.

“If you're saying, *I tested my model for fairness to make sure it works well for darker skin tones*, but you’re using a scale that doesn't represent most people with those skin tones, you don't know how well it actually works,” says Xango Eyeé, a Product Manager working on Responsible AI.

“If not developed with intention, the skin tone measure we use to understand whether our models are fair and representative can affect how products are experienced by users. Downstream, these decisions can have the biggest impacts on people who are most vulnerable to unfair treatment, people with darker skin tones,” Dr. Heldreth says.

Eyeé and Dr. Heldreth are both core members of Google’s research efforts focused on building more skin tone equity into AI development, a group that includes an interdisciplinary set of product managers, researchers and engineers who specialize in computer vision and social psychology. The team also works across Google with image equity teams building more representation into products like cameras, photos, and emojis.

“We take a human-centered approach to understanding how AI can influence and help people around the world,” Dr. Heldreth says, “focusing on improving inclusivity in AI, to ensure that technology reflects and empowers globally and culturally diverse communities, especially those who are historically marginalized and underserved.” A more inclusive skin tone scale is a core part of this effort.

The team operates with a guiding objective: To keep improving technology so that it works well for more people. Doing that has involved two major tasks: “The first was figuring out what was already built and why it wasn't working,” Eyeé says. “And the second was figuring out what we needed to build instead.”

![A man with glasses looks into the camera smiling. A woman with glasses next to him is also looking into the camera and smiling, and she is holding the camera taking a selfie. They are in a guitar store.](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Ellis_and_Anna_Monk.width-100.format-webp.webp)

Dr. Monk with his wife, Anna.

![A screenshot of a Google Meet video call with three rows of nine people in individual squares.](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/screenshot_.width-100.format-webp.webp)

The team during a call. Top row: Kylee Jaye, Shrikanth Narayanan, Auriel Wright; middle row: Candice Schumann, Courtney Heldreth, Komal Singh; bottom row: Marco Andreetto, Susanna Ricco, Kree Cole-Mclaughlin

![Two people stand side by side, looking into the camera and smiling. They’re standing in front of a green wall with a garden art installation on it.]](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/PXL_20220407_215726896.MP.width-100.format-webp.webp)

Susanna Ricco and Kylee Jaye, another software engineer who worked on the project.

![Two women standing side by side with their arms around each other, looking into the camera and smiling. They are standing in front of shrubs and trees, standing on a sidewalk next to yellow and blue circular objects on the sidewalk.](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/IMG_8194.width-100.format-webp.webp)

Dr. Susanna Ricco and Dr. Courtney Heldreth on the Google Mountain View campus.

### A social-technical approach

"Skin tone is something that changes the physical properties of images, and it’s something that affects people’s lived experiences — and both of these things can impact how a piece of technology performs,” Dr. Susanna Ricco says. Dr. Ricco, a software engineer on Google Research's Perception team, leads a group that specializes in finding new ways to make sure Google's computer vision systems work well for more users, regardless of their backgrounds or how they look. To make sure that tech works across skin tones, we need to intentionally test and improve it across a diverse range. “To do that, we need a scale that doesn’t leave skin tones out or over-generalize,” she says.

“There’s the physics side of things — how well a sensor responds to a person’s skin tone,” Dr. Ricco says. “Then there’s the social side of things: We know that skin tone correlates with life experiences, so we want to make sure we’re looking at fairness from this perspective, too. Ultimately what matters is, *does this work for me?* — and not just *me*, the person who’s making this technology, but *me*, as in anyone who comes across it.”

“Developing a scale for this isn’t just an AI or technology problem, but a social-technical problem,” Dr. Heldreth says. “It’s important that we understand how skin tone inequality can show up in the technology we use and importantly, do our best to avoid reproducing the colorism that exists. Fairness is contextual and uniquely experienced by each individual, so it’s important to center this problem on the people who will ultimately be affected by the choices we make. Therefore, doing this right requires us to take a human-centered approach because this is a human problem.”

“Connecting the technical to the human is the challenge here,” Dr. Ricco says. "The groups we test should be influenced by the ways in which individuals experience technology differently, not purely decided based on mathematical convenience.”

If it sounds like an intricate process, that’s because it is. “Our goal is not to tackle all of this complexity at once, but instead learn deeply about what each piece of research is telling us and put together the puzzle pieces,” Dr. Heldreth says.

The Monk Skin Tone Scale

![Ten circles in a row, ranging from dark to light.](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Monkscale.width-1200.format-webp.webp)

### The Monk Skin Tone Scale

The team knew piecing together that puzzle, and particularly thinking about how to define a range of skin tones, would be a wider effort that extended beyond Google.

So over the last year, they partnered with Dr. Monk to learn about and further test the scale for technology use cases. Dr. Monk’s research focuses on how factors such as skin tone, race and ethnicity affect inequality. He has been surveying people about the kinds of ways that skin tone has played a role in their lives for a decade. “If you talk to people of color, if you ask them, ‘How does your appearance matter in your everyday life? How does your skin color, your hair, how do they impact your life?’ you find it really does matter,” he says.

Dr. Monk began this research in part to build on the most prominently used skin tone scale, the Fitzpatrick Scale. Created in 1975 and made up of six broad shades, it was meant to be a jumping off point for medically categorizing skin type. The technology industry widely adopted it and applied it to skin tones and it became the standard. It’s what most AI systems use to measure skin tone.

In comparison, the MST Scale is composed of 10 shades — a number chosen so as not to be too limiting, but also not too complex.

Together, the team and Dr. Monk surveyed thousands of adults in the United States to learn if people felt more represented by the MST Scale compared to other scales that have been used in both the machine learning and beauty industries. “Across the board, people felt better represented by the MST Scale than the Fitzpatrick Scale,” Eyeé says, and this was especially true for less represented demographic groups.

“What you’re looking for is that subjective moment where people can see their skin tone on the scale,” Dr. Heldreth says. “To see the results of our research demonstrate that there are other skin tone measures where more people see themselves better represented felt like we were making steps in the right direction, that we could really make a difference.”

Of course, 10 points are not as comprehensive as scales that have 16, 40 or 110 shades. And for many use cases, like makeup, more is better. What was exciting about the MST Scale survey results was that the team found, even with 10 shades, participants felt the scale was equally representative as scales from the beauty industry with larger variety. “They felt that the MST Scale was just as inclusive, even with only 10 points on it,” Eyeé says. A 10-point scale is also something that can be used during data annotation, whereas rating skin tone images using a 40-point scale would be an almost impossible task for raters to do reliably.

What is particularly exciting about this work is that it continues to highlight the importance of a sociotechnical approach to building more equitable tools and products. Skin tones are continuous, and can be defined and categorized in a number of different ways, the simplest being to pick equally spaced RGB values on a scale of light to dark brown. But taking such a technical approach leaves out the nuance of how different communities have been historically affected by colorism. A scale that is effective for measuring and reducing inconsistent experiences for more people needs to adequately reflect a wide range of skin-tones that represent a diversity of communities – this is where Dr. Monk’s expertise and research proves particularly valuable.

Over the past two years, the team has shared their research with various other departments at Google. And work has begun on building annotation — or labeling — best practices based on the MST Scale, informed by expertise in computer vision, skin tone inequality and social cognition. Since perceptions of skin tones are subjective, it’s incredibly important that the same interdisciplinary research that went into creating and validating the scale is also applied to how it is used.

### What’s next

One of the first areas in which this technology will be used is Google’s image-based products. Until now, Google has largely relied on the Fitzpatrick Scale for photo AI. The MST scale is now being incorporated into products like Google Photos and Image Search, and will be expanded even more broadly in the coming months.

In addition to incorporating the MST Scale into Google products and sharing the 10 shades for anyone to use, Google and Dr. Monk are publishing their peer-reviewed research and expanding their research globally. Going through the research and peer review process has helped the team make sure their work is adding to the long history of multi-sector progress in this space and also offering new ideas in the quest for more inclusive AI.

Ultimately, we want the work to extend far beyond Google. The team is hopeful this is an industry starting point, and at the same time, they want to keep improving on it. “This is an evergreen project,” Dr. Heldreth says. “We’re constantly learning, and that’s what makes this so exciting.” The team plans to take the scale to more countries to learn how they interpret skin tone, and include those learnings in future iterations of the scale.

So the work continues. And while it’s certainly a “massive scientific challenge,” as Dr. Heldreth calls it, it’s also a very human one because it’s critical that tools we use to define skin tone ensure that more people see themselves represented and thus feel worthy of being seen. “It’s not just about this precise numeric value of skin tone,” Dr. Monk says. “It’s about giving people something they can see themselves in.”
