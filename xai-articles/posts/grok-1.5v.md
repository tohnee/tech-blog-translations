---
title: "grok-1.5v"
date: 2025-03-12
source: https://x.ai/news/grok-1.5v
crawled: 2026-09-22
---

April 12, 2024

## Grok-1.5 Vision Preview

Connecting the digital and physical worlds with our first multimodal model.

---

**Introducing Grok-1.5V, our first-generation multimodal model. In addition to its strong text capabilities, Grok can now process a wide variety of visual information, including documents, diagrams, charts, screenshots, and photographs. Grok-1.5V will be available soon to our early testers and existing Grok users.**

## Capabilities

Grok-1.5V is competitive with existing frontier multimodal models in a number of domains, ranging from multi-disciplinary reasoning to understanding documents, science diagrams, charts, screenshots, and photographs. We are particularly excited about Grok’s capabilities in understanding our physical world. Grok outperforms its peers in our new RealWorldQA benchmark that measures real-world spatial understanding. For all datasets below, we evaluate Grok in a zero-shot setting without chain-of-thought prompting.

| Benchmark | **Grok-1.5V** | GPT-4V | Claude 3 Sonnet | Claude 3 Opus | Gemini Pro 1.5 |
| --- | --- | --- | --- | --- | --- |
| MMMU Multi-discipline | 53.6% | 56.8% | 53.1% | **59.4%** | 58.5% |
| Mathvista Math | **52.8%** | 49.9% | 47.9% | 50.5% | 52.1% |
| AI2D Diagrams | 88.3% | 78.2% | **88.7%** | 88.1% | 80.3% |
| TextVQA Text reading | **78.1%** | 78.0% | - | - | 73.5% |
| ChartQA Charts | 76.1% | 78.5% | 81.1% | 80.8% | **81.3%** |
| DocVQA Documents | 85.6% | 88.4% | **89.5%** | 89.3% | 86.5% |
| RealWorldQA Real-world understanding | **68.7%** | 61.4% | 51.9% | 49.8% | 67.5% |

Example

Writing code from a diagram

![A diagram describing a guessing game with a flowchart of the game logic and user interactions](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fgrok1.5v_guessing.4bae7361.webp&w=2048&q=75)

##### User

Can you translate this into Python code?

##### Grok

Certainly! The flowchart you’ve provided describes a simple guessing game where the computer generates a random number, and the user has to guess it. Here’s the Python code that represents the logic in the flowchart:

python

```
import random

def guess_number(): # Generate a random number between 1 and 10

    target = random.randint(1, 10)

    while True:
        guess = int(input("Guess a number between 1 and 10: "))

        if guess == target:
            print("You won!")
            break
        else:
            print("Wrong guess, try again!")

if __name__ == "__main__":
    guess_number()
```

This code will run the guessing game as described in the flowchart. The user will be prompted to enter their guess until they guess the correct number.

## Real-World Understanding

In order to develop useful real-world AI assistants, it is crucial to advance a model's understanding of the physical world. Towards this goal, we are introducing a new benchmark, RealWorldQA. This benchmark is designed to evaluate basic real-world spatial understanding capabilities of multimodal models. While many of the examples in the current benchmark are relatively easy for humans, they often pose a challenge for frontier models.

![A picture of various household objects on a table.](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Frealworldqa_sample_1.40f61ece.webp&w=3840&q=75)

Which object is larger the pizza cutter or the scissors? A. The pizza cutter is larger. B. The scissors is larger. **C. They are about the same size.**

![A picture of a dark street scene with a sign that says "left lane must turn left"](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Frealworldqa_sample_2.c56d23d9.webp&w=3840&q=75)

Where can we go from the current lane? **A. Turn left.** B. Go straight. C. Turn left and go straight. D. Turn right.

![A picture of a street with several cars parked on the left](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Frealworldqa_sample_3.8c909fbe.webp&w=3840&q=75)

Given this front camera view from our sedan, do we have enough space to drive around the gray car in front of us? **A. Yes.** B. No.

![A picture of a toy next to a cell phone showing a compass.](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Frealworldqa_sample_4.510a61d4.webp&w=1920&q=75)

Given the picture, in which cardinal direction is the dinosaur facing? A. North. B. South. **C. East.** D. West.

The initial release of the RealWorldQA consists of over 700 images, with a question and easily verifiable answer for each image. The dataset consists of anonymized images taken from vehicles, in addition to other real-world images. We are excited to release RealWorldQA to the community, and we intend to expand it as our multimodal models improve. RealWorldQA is released under [CC BY-ND 4.0](https://creativecommons.org/licenses/by-nd/4.0/?ref=chooser-v1). Click [here (677MB)](https://data.x.ai/realworldqa.zip) to download the dataset.

## Into the Future

Advancing both our multimodal understanding and generation capabilities are important steps in building beneficial AGI that can understand the universe. In the coming months, we anticipate to make significant improvements in both capabilities, across various modalities such as images, audio, and video.

If you want to be a part of this journey, we are [hiring](/careers).

Try Grok On

[Web](https://grok.com)

[iOS](https://apps.apple.com/app/grok/id6670324846)

[Android](https://play.google.com/store/apps/details?id=ai.x.grok&hl=en)

[Grok on X](https://x.com/i/grok)

Products

[Grok](/grok)

[API](/api)

Company

[Company](/company)

[Careers](/careers)

[Contact](/contact)

[News](/news)

Resources

[Status](https://status.x.ai)

[Privacy policy](/privacy-policy)

[Security](/security)

[Legal](/legal)
