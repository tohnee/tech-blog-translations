---
title: "Running PyTorch on the M1 GPU"
source: https://sebastianraschka.com/blog/2022/pytorch-m1-gpu.html
crawled: 2026-09-06
---

# Running PyTorch on the M1 GPU

Today, [PyTorch officially introduced](https://pytorch.org/blog/introducing-accelerated-pytorch-training-on-mac/) GPU support for Apple’s ARM M1 chips. This is an exciting day for Mac users out there, so I spent a few minutes tonight trying it out in practice. In this short blog post, I will summarize my experience and thoughts with the M1 chip for deep learning tasks.

## My M1 Experience So Far

Back at the beginning of 2021, I happily sold my loud and chunky 15-inch Intel MacBook Pro to buy a much cheaper M1 MacBook Air. It’s been a fantastic machine so far: it is silent, lightweight, super-fast, and has terrific battery life.

When I was writing my new book, I noticed that it didn’t only feel fast in everyday use, but it also sped up several computations. For example, preprocessing the IMDb movie dataset [took only 21 seconds](https://github.com/rasbt/machine-learning-book/blob/main/ch08/ch08.ipynb) instead of [1 minute and 51 seconds](https://github.com/rasbt/python-machine-learning-book-3rd-edition/blob/master/ch08/ch08.ipynb) on my 2019 Intel MacBook Pro.

Similarly, all scikit-learn-related workflows were much faster on the M1 MacBook Air! I could even run small neural networks in PyTorch in a reasonable time (various multilayer perceptrons and convolutional neural networks for teaching purposes). I recall making a LeNet-5 runtime comparison between the M1 and a GeForce 1080Ti and finding similar speeds.

Even though the M1 MacBook is an amazing machine, it is really not feasible to train modern deep neural networks on it. It really can’t handle anything beyond LeNets. However, I should note that I compiled PyTorch myself back then, as an early adopter, and I could only utilize the M1 CPU in PyTorch.

## PyTorch M1 GPU Support

Today, the PyTorch Team [has finally announced M1 GPU support](https://pytorch.org/blog/introducing-accelerated-pytorch-training-on-mac/), and I was excited to try it. Along with the announcement, their [benchmark](https://sebastianraschka.com/glossary/#benchmark "Benchmark") showed that the M1 GPU was about 8x faster than a CPU for training a VGG16. And it was about 21x faster for inference (evaluation). According to the fine print, they tested this on a Mac Studio with an M1 Ultra. I am assuming CPU here refers to the M1 Ultra CPU.

How do we install the PyTorch version with M1 GPU support? I expect the M1-GPU support to be included in the 1.12 release and recommend watching the [release list](https://github.com/pytorch/pytorch/releases) for updates. But for now, we can install it from the latest nightly release:

![Pytorch m1 gpu m1 support](https://sebastianraschka.com/images/blog/2022/pytorch-m1-gpu/m1-support.webp)

(Screenshot from [pytorch.org](https://pytorch.org))

Personally, I recommend installing it as follows from the terminal:

```python
$ conda create -n torch-nightly python=3.8 

$ conda activate torch-nightly

$ pip install --pre torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/nightly/cpu
```

Then, if you want to run PyTorch code on the GPU, use `torch.device("mps")` analogous to `torch.device("cuda")` on an Nvidia GPU.

(An interesting tidbit: The file size of the PyTorch installer supporting the M1 GPU is approximately 45 Mb large. The PyTorch installer version with CUDA 10.2 support has a file size of approximately 750 Mb.)

## My Benchmarks

Just out of curiosity, I wanted to try this myself and trained deep neural networks for one epoch on various hardware, including the 12-core Intel server-grade CPU of a beefy deep learning workstation and a MacBook Pro with an M1 Pro chip. Here are the results for a VGG16 with CIFAR-10 images rescaled to 224x224 pixels (typical ImageNet sizes for VGG16):

![Pytorch m1 gpu vgg benchmark training](https://sebastianraschka.com/images/blog/2022/pytorch-m1-gpu/vgg-benchmark-training.webp)

---

**Additional details about the runs**

(The [M1 Max](https://github.com/rasbt/machine-learning-notes/issues/3) and [M1 Ultra](https://github.com/rasbt/machine-learning-notes/issues/12) results were kindly provided by readers. And I also added in the RTX 3060 and RTX 3080 results that were kindly provided [here](https://github.com/rasbt/machine-learning-notes/issues/6) and [here](https://github.com/rasbt/machine-learning-notes/issues/7).)

The batch size was 32 for all runs except the RTX 3060, which only had 6 GB VRAM and could only handly a batch size of 8.

You may have noticed that there are two versions of certain runs in the plot above: May 18 and May 22. There was apparently a [memory leak](https://github.com/pytorch/pytorch/issues/77753#issuecomment-1133875782) in the initial May 18 nightly-release (torch 1.12.0.dev20220518) that was recently fixed on May 21. So I upgraded to the May 22 night-release (torch-1.13.0.dev20220522) and rerun the experiments.

---

Compared to the M1 Pro CPU (fourth row from the top) and M1 Pro GPU (sixth row from the bottom), the M1 Pro GPU trains the network 3.5x faster. That’s at least something!

Next, let’s take a look at the inference speeds. Here, inference means evaluating the model on the test sets:

![Pytorch m1 gpu vgg benchmark inference](https://sebastianraschka.com/images/blog/2022/pytorch-m1-gpu/vgg-benchmark-inference.webp)

During inference, the speed advantage between M1 Pro CPU and GPUs is even more noticeable. For example, the M1 Pro GPU is 5x times as fast (1.69 min) as the M1 Pro CPU (8.51 min).

So, while the M1 GPU supports offers a noticeable boost compared to the M1 CPU, it’s not a total game changer, and we probably still want to stick to conventional GPUs for our neural network training. The M1 Ultra of the Mac Studio comes closer to Nvidia GPU performance, but we have to consider that this is an expensive (~$5k) machine!

Some additional notes about the M1 GPU performance:

- I noticed that the convolutional networks need much more RAM when running them on a CPU or M1 GPU (compared to a CUDA GPU), and there may be issues regarding swapping. However, I made sure that training [the neural networks never exceeded 80% memory utilization](https://twitter.com/rasbt/status/1527115038720512000?s=20&t=k1374Sdramu2rFp0EQGkxA) on the MacBook Pro.
- As suggested, not maxing out the batch size on the M1 GPU runs could be another explanation. However, for fairness, I ran all training runs with a batch size of 32 – the 2080Ti and 1080Ti couldn’t handle more due to their limited 11Gb VRAM. **Update:** I repeated the M1 Pro GPU run with a batch size of 64 and it was approximately 20% faster compared to a batch size of 32.

Also, we should keep in mind that this is an early release of a brand-new feature, and it might improve over time. The fact that it works and is under active development is pretty exciting by itself, though! 🙌

If you want to run the code yourself, [here is a link to the scripts](https://github.com/rasbt/machine-learning-notes/tree/main/benchmark/pytorch-m1-gpu).

([Please let me know](https://twitter.com/rasbt/status/1527102613749125120?s=20&t=gerAjN40WmmDglsNDFj5Mg) if you have any ideas on how to improve the GPU performance!)

## Conclusions

Is the MacBook with M1 GPU going to be my go-to for deep learning? A hard no. I don’t think we should think of laptops as our primary deep neural network training machines. That’s because

- they have a high cost/performance ratio (compared to workstations);
- they can get relatively hot which surely isn’t healthy;
- if we utilize them under full load, they become pretty limited for other tasks that we usually want them to do.

However, laptops are my go-to productivity machines. I use them for pretty much everything, including simple scientific computations and debugging complicated neural network code before running it on my workstation or cloud cluster.

My personal takeaway from this benchmark is that the recent PyTorch M1 GPU support finally works, and this is exciting! There may still be some kinks to be ironed out to work smoothly and faster than the CPUs, and I expect it to make laptops (ehm, MacBooks) significantly more attractive as productivity, prototyping, and debugging machines for deep learning. 🎉

PS: If you have any ideas on how to speed up the M1 GPU performance, please [reach out!](https://twitter.com/rasbt/status/1527102613749125120?s=20&t=gerAjN40WmmDglsNDFj5Mg) 🙏.
