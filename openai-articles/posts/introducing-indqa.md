---
title: "Introducing IndQA"
date: 2025-11-03
source: https://openai.com/index/introducing-indqa/
crawled: 2026-09-13
category: research
---

Our mission is to make AGI benefit all of humanity. If AI is going to be useful for everyone, it needs to work well across languages and cultures. About 80 percent of people worldwide do not speak English as their primary language, yet most existing benchmarks that measure non-English language capabilities fall short.

Existing multilingual benchmarks like [MMMLU](https://huggingface.co/datasets/openai/MMMLU) are now saturated—top models cluster near high scores—which make them less useful for measuring real progress. In addition, current benchmarks mostly focus on translation or multiple-choice tasks. They don’t adequately capture what really matters for evaluating an AI system’s language capabilities—understanding context, culture, history, and the things that matter to people where they live.

That’s why we built **IndQA**, a new benchmark designed to evaluate how well AI models understand and reason about questions that matter in Indian languages, across a wide range of cultural domains. While our aim is to create similar benchmarks for other languages and regions, India is an obvious starting point. India has about a billion people who don’t use English as their primary language, 22 official languages (including at least seven with over 50 million speakers), and is ChatGPT’s second largest market.

This work is part of our ongoing commitment to improve our products and tools for Indian users, and to make our technology more accessible throughout the country.

## How it works

IndQA evaluates knowledge and reasoning about Indian culture and everyday life in Indian languages. It spans 2,278 questions across 12 languages and 10 cultural domains, created in partnership with 261 domain experts from across India. Unlike existing benchmarks like MMMLU and MGSM, it is designed to probe culturally nuanced, reasoning-heavy tasks that existing evaluations struggle to capture.

IndQA covers a broad range of culturally relevant topics, such as **Architecture & Design, Arts & Culture, Everyday Life, Food & Cuisine, History, Law & Ethics, Literature & Linguistics, Media & Entertainment, Religion & Spirituality,** and **Sports & Recreation**—with items written natively in **Bengali, English, Hindi, Hinglish, Kannada, Marathi, Odia, Telugu, Gujarati, Malayalam, Punjabi,** and **Tamil**. *Note: We specifically added Hinglish given the prevalence of code-switching in conversations.*

Each datapoint includes a **culturally grounded prompt** in an Indian language, an **English translation** for auditability, **rubric criteria** for grading, and an **ideal answer** that reflects expert expectations.

IndQA uses a rubric-based approach. Each response is graded against criteria written by domain experts for that specific question. The criteria spell out what an ideal answer should include or avoid, and each one is given a weighted point value based on its importance. A model-based grader checks whether each criterion is met. The final score is the sum of the points for criteria satisfied out of the total possible.

## How we built IndQA

- **Expert‑authored questions.** We worked with partners to find experts in India across 10 different domains. They drafted difficult, reasoning‑focused prompts tied to their regions and specialties. These experts are native‑level speakers of the relevant language (and English) and bring deep subject expertise.
- **Adversarial filtering:** Each question was tested against OpenAI’s strongest models at the time of their creation: GPT‑4o, OpenAI o3, GPT‑4.5, and (partially, post public launch) GPT‑5. We kept only those questions where a majority of these models failed to produce acceptable answers, preserving headroom for progress
- **Detailed Criteria.** Along with every question, domain experts provided criteria used to grade the model response, similar to an exam rubric for an essay question. These criteria are used to grade responses from candidate models.
- **Ideal answers + review.** Experts added ideal answers and English translations, followed by peer review and iterative fixes until sign‑off.

## Example questions

## Improvements over time

We use IndQA to evaluate how recent frontier models perform and chart progress over the last couple years. With IndQA we can see that OpenAI’s models have improved significantly over time on Indian languages (with caveats), but still have substantial room for improvement. We look forward to improving performance and sharing results for future models.

We also stratify performance on IndQA by Language and Domain below, comparing GPT‑5 Thinking High to other frontier models.

### Caveats

Because questions are *not identical* across languages, IndQA is **not** a language leaderboard; cross‑language scores shouldn’t be interpreted as direct comparisons of language ability. Instead, we plan to use IndQA to measure *improvement over time* within a model family or configuration.

Additionally, because questions were filtered to those GPT‑4o, OpenAI o3, GPT‑4.5, and (post public launch) GPT‑5 could not answer sufficiently, question selection is adversarial against these models. This potentially confounds the relative performance of GPT‑5, and could disadvantage all OpenAI models compared to non-OpenAI models.

## The experts behind IndQA

We’re grateful to the **261** Indian experts—journalists, linguists, scholars, artists, and industry practitioners—who authored and reviewed questions for IndQA. A few examples of the experts we worked with includes:

- A Nandi Award winning Telugu actor and screenwriter with over 750 films
- A Marathi journalist and editor at Tarun Bharat
- A scholar of Kannada linguistics and dictionary editor
- An International Chess Grandmaster who coaches top-100 chess players
- A Tamil writer, poet, and cultural activist advocating for social justice, caste equity, and literary freedom
- An award winning Punjabi music composer
- A Gujarati heritage curator and conservation specialist
- An award winning Malayalam poet and performance artist
- A professor of history, specializing in Bengal's rich cultural heritage
- A professor of architecture, focusing on Odishan temples

## Next steps

We hope the release of IndQA will inform and inspire new benchmark creation from the research community. IndQA style questions are especially valuable in languages or cultural domains that are poorly covered by existing AI benchmarks. Creating similar benchmarks to IndQA can help AI research labs learn more about languages and domains models struggle with today, and provide a north star for improvements in the future.
