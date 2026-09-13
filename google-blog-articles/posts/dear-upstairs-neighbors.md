---
title: "How animators and AI researchers made ‘Dear Upstairs Neighbors’"
source: https://blog.google/innovation-and-ai/models-and-research/google-deepmind/dear-upstairs-neighbors/
site: google-blog
date: 2026-01-26
authors: Cassidy Curtis
crawled: 2026-09-13
---

Today, our animated short film, “Dear Upstairs Neighbors,” previews at the Sundance Film Festival. The film will be showcased at the Sundance Institute’s Story Forum, a space focused on artist-first tools and technologies supporting visual storytelling.

“Dear Upstairs Neighbors” is the story of a young woman, Ada, who is desperate for a good night’s sleep but kept awake by her exceedingly noisy neighbors. As she struggles to imagine what could be causing the cacophony upstairs, reality drifts into fantasy, and an epic battle for peace and sanity ensues.

The film is a collaboration between [animation veterans](https://www.imdb.com/title/tt39368604/reference), including director and Pixar alum Connie He, and researchers at Google DeepMind, united by a shared goal of exploring how generative tools might fit in with artists' creative processes.

Director Connie He developed the story based on her personal experience with noisy neighbors. In her storyboards she envisioned a series of hallucinations that get more unhinged and ridiculous as the night progresses.

![A series of handmade paintings showing Ada, a young woman in her pyjamas with curly blue-black hair in a messy bun, standing in a neutral pose, rendered from several different angles.](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Figure02_character_turnaround_bed.width-100.format-webp.webp)

For our main character, Ada, production designer Yingzong Xin created a design that’s quirky and unique, with pushed proportions and an angular shape language.

![A series of paintings showing Ada’s face with a variety of extreme expressions: joy, rage, fear, wonder, yawning, and many more.](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Figure03_DUN_Expression_color_v1_.width-100.format-webp.webp)

Ada’s face is extremely expressive. Character model sheet by Yingzong Xin.

![A painting of Ada’s bedroom, showing the arrangement of her bed, desk, bookshelves, and various objects, rendered in isometric perspective with a cool color palette.](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Figure03a_Ada_bedroom_1080p.width-100.format-webp.webp)

Ada’s bedroom is rendered in cool colors, conveying a sense of calm, comfort and sanctuary. Set design by Yingzong Xin.

![A painting of a saw cutting a log, in vivid neon turquoise, magenta and yellow on a black background.](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Figure04_Log_1080p.width-100.format-webp.webp)

Ada’s hallucinations have a rough style and neon palette that distinguishes them from the “real world” of her bedroom. Concept art by Yingzong Xin.

![A painting of Ada standing on her bed, enraged by all the noise, her mouth in an angry grimace, her hands balled into fists, and red and orange flames bursting out from her in all directions.](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Figure05_700_6_1080p.width-100.format-webp.webp)

The painterly style changes from moment to moment, expressing Ada’s changing emotions through color and texture. Concept art by Yingzong Xin.

![An expressionistic painting of a giant speaker floating menacingly above a mysterious landscape, in garish tones of black, red, and yellow.](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Figure06_700_8_1080p.width-100.format-webp.webp)

In the most intense moments, the abstract expressionist style grows to dominate the entire scene. Concept art by Yingzong Xin.

From the start, the team aspired to empower animation artists to benefit from the creative potential of generative AI without sacrificing artistic control to its inherent unpredictability. To define her vision for this film, Connie developed the storyboards, and enlisted award-winning production designer Yingzong Xin to create concept art and character designs. We committed to staying faithful to this artistic vision throughout shot production.

The expressionistic visual styles are central to the storytelling — and extremely difficult to achieve in traditional animation. We expected that AI could help fill the gap, but soon found that these styles were so unique, and our design choices so specific, that our researchers would have to develop new capabilities to provide the customization and control that we needed to bring the film to life.

## Tune for new visual styles

Our first challenge was to produce shots consistent with Ada’s character design and the painterly styles that defined each scene. To achieve high quality and consistency, our researchers built tools that allowed our artists to fine-tune custom Veo and Imagen models on their artwork, teaching the models new visual concepts from just a few example images.

![A grid of twelve colorful painterly images of Ada in a variety of situations: swimming, rock climbing, boxing, playing soccer, DJing, playing with kids in a waterfall, gazing in wonder at the aurora in an arctic landscape, and more.](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/WM_AdaT2I_1080p.width-100.format-webp.webp)

Images of Ada generated by Imagen after fine-tuning. The fine-tuned model helped the whole team explore Ada as a character.

Left: paintings by Yingzong Xin. Right: stylized animated video generated by Veo after fine-tuning. What Veo learned from our concept art surprised us: not just superficial details like color and texture, but deep artistic concepts like two-point perspective.

Top: Ada’s character design follows strictly two-dimensional rules: her characteristic hair poof and messy bun must always be part of her silhouette, never obscuring her face. Bottom left: a 3D sculpture of Ada’s hair can’t possibly look correct from every angle, because the solid form violates those 2D rules. Bottom right: Veo, after fine-tuning on images of Ada, seamlessly resolves the conflict, smoothly adapting the shapes to keep the silhouette correct as the head turns.

## Show, don’t type

Another challenge was precisely controlling the content and motion of each shot. We knew that text prompting alone would never let us control the rhythm of Ada’s sleepy fingers typing, the comedic timing of her facial expressions, or the exact framing of a camera reveal. We needed a way to communicate that level of nuance and specificity to our AI models. Our researchers drew inspiration from how our animators communicate visually, by drawing, painting or acting out scenes. We developed novel video-to-video workflows, which allowed our animators to convey their intentions visually by creating rough animation in their tool of choice. Our models then transformed that animation into fully stylized videos that follow the input motion, with an adjustable balance between tight control and creative improvisation.

Using text-to-video with the fine-tuned Veo model produced scenes that looked like Ada, but their movement was random, uncontrolled, and often bizarre. Text alone can’t convey the nuance and specificity needed for narrative animated filmmaking.

To create a nuanced performance strong enough to carry the story, our animators used traditional methods. Animator Ben Knight created rough 3D animation for this scene in Maya, and researcher Andy Coenen used fine-tuned Veo models to transform it into the final look.

The video-to-video approach allowed each artist to work in their comfort zone, using their favorite animation tools. Animator Mattias Breitholtz created this rough 2D animation using TV Paint, and researcher Forrester Cole transformed it into the final look frame by frame, using fine-tuned versions of Imagen in a custom ComfyUI workflow.

Animator Steven Chao animated Ada and created dynamic low-poly effects in Maya, and researcher Ellen Jiang and director Connie He used fine-tuned Veo and Imagen models to transform these elements into the expressionist look. The staccato rhythm of the changing paint texture adds to the intensity of the action.

## Iterate toward perfection

Even with the control provided by fine-tuning and video-to-video workflows, none of our final shots were created in a single “one-click” generation. Just as in any film production, we critiqued each shot in our “dailies” reviews, going through several rounds of feedback to get every detail right. To iterate on a shot without re-generating from scratch every time, we built tools for localized refinement, allowing us to edit specific regions of a video with an adjustable level of control.

To create Ada’s hallucination of a howling dog, we started with a concept painting by Yingzong Xin, and used Veo image-to-video to bring it to life. Veo’s first pass (without fine-tuning) was too photorealistic for our film; so we used the fine-tuned version of Veo to bring the shot closer to our intended visual style. The video-to-video workflow allowed us to switch freely between Veo and traditional tools like Premiere.

Using fine-tuned Veo with video-to-video workflows allowed us to iterate on the design of both the dog and the painterly effects around it, exploring stylistic variations with unprecedented freedom and control.

Supervising animator Cassidy Curtis created rough 3D animation for this shot in Maya, and researcher Erika Lu fine-tuned a Veo model to transform it into the final look. To improve the silhouette of Ada’s hair, Lu added a rough mask to indicate the region where more hair was needed, and used Veo to improvise an extra tuft of hair there that fits seamlessly into the rest of the shot.

Finally, to prepare our film for the big screen, we used Veo's upscaling capability to bring our final shots to 4K resolution. Guided by our artists' critique, our researchers carefully tuned the model's behavior to add rich detail that preserved every nuance of the artistic style. The Veo 4K upscaling model is available in Flow and coming to Google AI Studio and Vertex AI later this month to meet the real-world needs of filmmakers.

Each shot presented unique challenges, and over the course of production, our multi-disciplinary team developed several workflows combining the precise control of hand-crafted animation with the stylistic flexibility and scalability of generative AI. Not only did our AI models produce hilarious bloopers, they often surprised us with unexpectedly beautiful and creative solutions. We learned valuable lessons from coming together every day to produce each shot with fine-grained artistic intention and care. Our artists found new creative powers through direct access to experimental research, and used their craft and perspective to help shape its development. Our researchers gained hands-on experience as technical artists, rapidly prototyping solutions to break through artistic and technological barriers. We’re excited to continue our mission to build generative AI with and for professional artists and filmmakers.
