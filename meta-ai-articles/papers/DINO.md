---
title: "Emerging Properties in Self-Supervised Vision Transformers"
arxiv: 2104.14294
date: 2021-04-29
source: https://arxiv.org/abs/2104.14294
crawled: 2026-09-22
---

# Emerging Properties in Self-Supervised Vision Transformers

Mathilde Caron       Hugo Touvron       Ishan Misra       Hervé Jegou
Affiliation:  Facebook AI Research           Inria*           Sorbonne University
  
Julien Mairal       Piotr Bojanowski       Armand Joulin

###### Abstract

††
∗Univ. Grenoble Alpes, Inria, CNRS, Grenoble INP, LJK, 38000 Grenoble, France.
  
Correspondence: mathilde@fb.com
  
Code: <https://github.com/facebookresearch/dino>

In this paper, we question if self-supervised learning provides new properties to Vision Transformer (ViT) [[10](#as1_bib.bib10)] that stand out compared to convolutional networks (convnets).
Beyond the fact that adapting self-supervised methods to this architecture works particularly well, we make the following observations:
first, self-supervised ViT features contain explicit information about the semantic segmentation of an image,
which does not emerge as clearly with supervised ViTs, nor with convnets.
Second, these features are also excellent kk-NN classifiers, reaching 78.3% top-1 on ImageNet with a small ViT.
Our study also underlines the importance of momentum encoder [[13](#as1_bib.bib13)], multi-crop training [[3](#as1_bib.bib3)], and the use of small patches with ViTs.
We implement our findings into a simple self-supervised method, called DINO, which we interpret as a form of self-distillation with no labels.
We show the synergy between DINO and ViTs by achieving 80.1% top-1 on ImageNet in linear evaluation with ViT-Base.

![[Uncaptioned image]](2104.14294v2/attn6.png)

Figure 1: 
Self-attention from a Vision Transformer with 8×88\times 8 patches trained with no supervision.
We look at the self-attention of the [CLS] token on the heads of the last layer.
This token is not attached to any label nor supervision.
These maps show that the model automatically learns class-specific features leading to unsupervised object segmentations.

## 1 Introduction

Transformers [[70](#bib.bib70)] have recently emerged as an alternative to convolutional neural networks (convnets) for visual recognition [[10](#as1_bib.bib10), [25](#as1_bib.bib25), [83](#bib.bib83)].
Their adoption has been coupled with a training strategy inspired by natural language processing (NLP), that is, pretraining on large quantities of data and finetuning on the target dataset [[9](#as1_bib.bib9), [55](#bib.bib55)].
The resulting Vision Transformers (ViT) [[10](#as1_bib.bib10)] are competitive with convnets but, they have not yet delivered clear benefits over them: they are computationally more demanding, require more training data, and their features do not exhibit unique properties.

In this paper, we question whether the muted success of Transformers in vision can be explained by the use of supervision in their pretraining.
Our motivation is that one of the main ingredients for the success of Transformers in NLP was the use of self-supervised pretraining, in the form of close procedure in BERT [[9](#as1_bib.bib9)] or language modeling in GPT [[55](#bib.bib55)].
These self-supervised pretraining objectives use the words in a sentence to create pretext tasks that provide a richer learning signal than the supervised objective of predicting a single label per sentence.
Similarly, in images, image-level supervision often reduces the rich visual information contained in an image to a single concept selected from a predefined set of a few thousand categories of objects [[21](#as1_bib.bib21)].

While the self-supervised pretext tasks used in NLP are text specific, many existing self-supervised methods have shown their potential on images with convnets [[3](#as1_bib.bib3), [4](#as1_bib.bib4), [12](#as1_bib.bib12), [13](#as1_bib.bib13)].
They typically share a similar structure but with different components designed to avoid trivial solutions (collapse) or to improve performance [[7](#as1_bib.bib7)].
In this work, inspired from these methods, we study the impact of self-supervised pretraining on ViT features.
Of particular interest, we have identified several interesting properties that do not emerge with supervised ViTs, nor with convnets:

- •

  Self-supervised ViT features explicitly contain the scene layout and, in particular, object boundaries, as shown in Figure [1](#S0.F1 "Figure 1 ‣ Emerging Properties in Self-Supervised Vision Transformers").
  This information is directly accessible in the self-attention modules of the last block.
- •

  Self-supervised ViT features perform particularly well with a basic nearest neighbors classifier (kk-NN) *without any finetuning, linear classifier nor data augmentation*, achieving 78.3% top-1 accuracy on ImageNet.

The emergence of segmentation masks seems to be a property shared across self-supervised methods.
However, the good performance with kk-NN only emerge when combining certain components such as momentum encoder [[13](#as1_bib.bib13)] and multi-crop augmentation [[3](#as1_bib.bib3)].
Another finding from our study is the importance of using smaller patches with ViTs to improve the quality of the resulting features.

Overall, our findings about the importance of these components lead us to design a simple self-supervised approach that can be interpreted as a form of knowledge distillation [[35](#bib.bib35)] with no labels.
The resulting framework, DINO, simplifies self-supervised training by directly predicting the output of a teacher network—built with a momentum encoder—by using a standard cross-entropy loss.
Interestingly, our method can work with only a centering and sharpening of the teacher output to avoid collapse, while
other popular components such as predictor [[12](#as1_bib.bib12)], advanced normalization [[3](#as1_bib.bib3)] or contrastive loss [[13](#as1_bib.bib13)] add little benefits in terms of stability or performance.
Of particular importance, our framework is flexible and works on both convnets and ViTs without the need to modify the architecture, nor adapt internal normalizations [[58](#bib.bib58)].

We further validate the synergy between DINO and ViT by outperforming previous self-supervised features on the ImageNet linear classification benchmark with 80.1% top-1 accuracy with a ViT-Base with small patches.
We also confirm that DINO works with convnets by matching the state of the art with a ResNet-50 architecture.
Finally, we discuss different scenarios to use DINO with ViTs in case of limited computation and memory capacity.
In particular, training DINO with ViT takes just two 8-GPU servers over 3 days to achieve 76.1%76.1\% on ImageNet linear benchmark, which outperforms self-supervised systems based on convnets of comparable sizes with significantly reduced compute requirements [[3](#as1_bib.bib3), [12](#as1_bib.bib12)].

Figure 2: 
Self-distillation with no labels.
We illustrate DINO in the case of one single pair of views (x1x_{1}, x2x_{2}) for simplicity.
The model passes two different random transformations of an input image to the student and teacher networks.
Both networks have the same architecture but different parameters.
The output of the teacher network is centered with a mean computed over the batch.
Each networks outputs a KK dimensional feature that is normalized with a temperature softmax over the feature dimension.
Their similarity is then measured with a cross-entropy loss.
We apply a stop-gradient (sg) operator on the teacher to propagate gradients only through the student.
The teacher parameters are updated with an exponential moving average (ema) of the student parameters.

## 2 Related work

##### Self-supervised learning.

A large body of work on self-supervised learning focuses on discriminative approaches coined *instance classification* [[4](#as1_bib.bib4), [20](#bib.bib20), [13](#as1_bib.bib13), [27](#as1_bib.bib27)],
which considers each image a different class and trains the model by discriminating them up to data augmentations.
However, explicitly learning a classifier to discriminate between all images [[20](#bib.bib20)] does not scale well with the number of images.
Wu *et al*. [[27](#as1_bib.bib27)] propose to use a noise contrastive estimator (NCE) [[32](#bib.bib32)] to compare instances instead of classifying them.
A caveat of this approach is that it requires comparing features from a large number of images simultaneously.
In practice, this requires large batches [[4](#as1_bib.bib4)] or memory banks [[13](#as1_bib.bib13), [27](#as1_bib.bib27)].
Several variants allow automatic grouping of instances in the form of clustering [[2](#bib.bib2), [8](#bib.bib8), [2](#as1_bib.bib2), [36](#bib.bib36), [42](#bib.bib42), [74](#bib.bib74), [80](#bib.bib80), [85](#bib.bib85)].

Recent works have shown that we can learn unsupervised features without discriminating between images.
Of particular interest, Grill *et al*. [[12](#as1_bib.bib12)] propose a metric-learning formulation called BYOL, where features are trained by matching them to representations obtained with a momentum encoder.
Methods like BYOL work even without a momentum encoder, at the cost of a drop of performance [[7](#as1_bib.bib7), [12](#as1_bib.bib12)].
Several other works echo this direction, showing that one can match more elaborate representations [[26](#bib.bib26), [27](#bib.bib27)], train features matching them to a uniform distribution [[6](#bib.bib6)] or by using whitening [[23](#bib.bib23), [81](#bib.bib81)].
Our approach takes its inspiration from BYOL but operates with a different similarity matching loss and uses the exact same architecture for the student and the teacher.
That way, our work completes the interpretation initiated in BYOL of self-supervised learning as a form of Mean Teacher self-distillation [[24](#as1_bib.bib24)] with no labels.

##### Self-training and knowledge distillation.

Self-training aims at improving the quality of features by propagating a small initial set of annotations to a large set of unlabeled instances.
This propagation can either be done with hard assignments of labels [[41](#bib.bib41), [78](#bib.bib78), [79](#bib.bib79)] or with a soft assignment [[76](#bib.bib76)].
When using soft labels, the approach is often referred to as knowledge distillation [[7](#bib.bib7), [35](#bib.bib35)] and has been primarily designed to train a small network to mimic the output of a larger network to compress models.
Xie *et al*. [[76](#bib.bib76)] have shown that distillation could be used to propagate soft pseudo-labels to unlabelled data in a self-training pipeline, drawing an essential connection between self-training and knowledge distillation.
Our work builds on this relation and extends knowledge distillation to the case where no labels are available.
Previous works have also combined self-supervised learning and knowledge distillation [[25](#bib.bib25), [63](#bib.bib63), [5](#as1_bib.bib5), [47](#bib.bib47)], enabling self-supervised model compression and performance gains.
However, these works rely on a *pre-trained* fixed teacher while our teacher is dynamically built during training.
This way, knowledge distillation, instead of being used as a post-processing step to self-supervised pre-training, is directly cast as a self-supervised objective.
Finally, our work is also related to codistillation [[1](#bib.bib1)] where student and teacher have the same architecture and use distillation during training.
However, the teacher in codistillation is also distilling from the student, while it is updated with an average of the student in our work.

## 3 Approach

### 3.1 SSL with Knowledge Distillation

The framework used for this work, DINO, shares the same overall structure as recent self-supervised approaches [[3](#as1_bib.bib3), [7](#as1_bib.bib7), [4](#as1_bib.bib4), [12](#as1_bib.bib12), [13](#as1_bib.bib13)].
However, our method shares also similarities with knowledge distillation [[35](#bib.bib35)] and we present it under this angle.
We illustrate DINO in Figure [2](#S1.F2 "Figure 2 ‣ 1 Introduction ‣ Emerging Properties in Self-Supervised Vision Transformers") and propose a pseudo-code implementation in Algorithm [1](#algorithm1 "Algorithm 1 ‣ 3.1 SSL with Knowledge Distillation ‣ 3 Approach ‣ Emerging Properties in Self-Supervised Vision Transformers").

Knowledge distillation is a learning paradigm where we train a student network gθsg_{\theta_{s}} to match the output of a given teacher network gθtg_{\theta_{t}}, parameterized by θs\theta_{s} and θt\theta_{t} respectively.
Given an input image xx, both networks output probability distributions over KK dimensions denoted by PsP_{s} and PtP_{t}.
The probability PP is obtained by normalizing the output of the network gg with a softmax function. More precisely,

|  |  |  |  |
| --- | --- | --- | --- |
|  | Ps​(x)(i)=exp⁡(gθs​(x)(i)/τs)∑k=1Kexp⁡(gθs​(x)(k)/τs),P_{s}(x)^{(i)}=\frac{\exp(g_{\theta_{s}}(x)^{(i)}/\tau_{s})}{\sum_{k=1}^{K}\exp(g_{\theta_{s}}(x)^{(k)}/\tau_{s})}, |  | (1) |

with τs>0\tau_{s}>0 a temperature parameter that controls the sharpness of the output distribution, and a similar formula holds for PtP_{t} with temperature τt\tau_{t}.
Given a fixed teacher network gθtg_{\theta_{t}}, we learn to match these distributions by minimizing the cross-entropy loss w.r.t. the parameters of the student network θs\theta_{s}:

|  |  |  |  |
| --- | --- | --- | --- |
|  | minθs⁡H⁡(Pt​(x),Ps​(x)),\min_{\theta_{s}}H(P_{t}(x),P_{s}(x)), |  | (2) |

where H⁡(a,b)=−a​log⁡bH(a,b)=-a\log b.

In the following, we detail how we adapt the problem in Eq. ([2](#S3.E2 "Equation 2 ‣ 3.1 SSL with Knowledge Distillation ‣ 3 Approach ‣ Emerging Properties in Self-Supervised Vision Transformers")) to self-supervised learning.
First, we construct different distorted views, or crops, of an image with multi-crop strategy [[3](#as1_bib.bib3)].
More precisely, from a given image, we generate a set VV of different views.
This set contains two *global* views, x1gx^{g}_{1} and x2gx^{g}_{2} and several *local* views of smaller resolution.
All crops are passed through the student while only the *global* views are passed through the teacher, therefore encouraging “local-to-global” correspondences.
We minimize the loss:

|  |  |  |  |
| --- | --- | --- | --- |
|  | minθs∑x∈{x1g,x2g}∑x′∈Vx′≠xH(Pt(x),Ps(x′)).\min_{\theta_{s}}\sum_{x\in\{x^{g}_{1},x^{g}_{2}\}}\quad\sum_{\begin{subarray}{c}x^{\prime}\in V\\ x^{\prime}\neq\,x\end{subarray}}\quad H(P_{t}(x),P_{s}(x^{\prime})). |  | (3) |

Algorithm 1  DINO PyTorch pseudocode w/o multi-crop.

[⬇](data:text/plain;base64,IyBncywgZ3Q6IHN0dWRlbnQgYW5kIHRlYWNoZXIgbmV0d29ya3MKIyBDOiBjZW50ZXIgKEspCiMgdHBzLCB0cHQ6IHN0dWRlbnQgYW5kIHRlYWNoZXIgdGVtcGVyYXR1cmVzCiMgbCwgbTogbmV0d29yayBhbmQgY2VudGVyIG1vbWVudHVtIHJhdGVzCmd0LnBhcmFtcyA9IGdzLnBhcmFtcwpmb3IgeCBpbiBsb2FkZXI6ICMgbG9hZCBhIG1pbmliYXRjaCB4IHdpdGggbiBzYW1wbGVzCiAgICB4MSwgeDIgPSBhdWdtZW50KHgpLCBhdWdtZW50KHgpICMgcmFuZG9tIHZpZXdzCgogICAgczEsIHMyID0gZ3MoeDEpLCBncyh4MikgIyBzdHVkZW50IG91dHB1dCBuLWJ5LUsKICAgIHQxLCB0MiA9IGd0KHgxKSwgZ3QoeDIpICMgdGVhY2hlciBvdXRwdXQgbi1ieS1LCgogICAgbG9zcyA9IEgodDEsIHMyKS8yICsgSCh0MiwgczEpLzIKICAgIGxvc3MuYmFja3dhcmQoKSAjIGJhY2stcHJvcGFnYXRlCgogICAgIyBzdHVkZW50LCB0ZWFjaGVyIGFuZCBjZW50ZXIgdXBkYXRlcwogICAgdXBkYXRlKGdzKSAjIFNHRAogICAgZ3QucGFyYW1zID0gbCpndC5wYXJhbXMgKyAoMS1sKSpncy5wYXJhbXMKICAgIEMgPSBtKkMgKyAoMS1tKSpjYXQoW3QxLCB0Ml0pLm1lYW4oZGltPTApCgpkZWYgSCh0LCBzKToKICAgIHQgPSB0LmRldGFjaCgpICMgc3RvcCBncmFkaWVudAogICAgcyA9IHNvZnRtYXgocyAvIHRwcywgZGltPTEpCiAgICB0ID0gc29mdG1heCgodCAtIEMpIC8gdHB0LCBkaW09MSkgIyBjZW50ZXIgKyBzaGFycGVuCiAgICByZXR1cm4gLSAodCAqIGxvZyhzKSkuc3VtKGRpbT0xKS5tZWFuKCkKCg==)

# gs, gt: student and teacher networks

# C: center (K)

# tps, tpt: student and teacher temperatures

# l, m: network and center momentum rates

gt.params = gs.params

for x in loader: # load a minibatch x with n samples

x1, x2 = augment(x), augment(x) # random views

s1, s2 = gs(x1), gs(x2) # student output n-by-K

t1, t2 = gt(x1), gt(x2) # teacher output n-by-K

loss = H(t1, s2)/2 + H(t2, s1)/2

loss.backward() # back-propagate

# student, teacher and center updates

update(gs) # SGD

gt.params = l*gt.params + (1-l)*gs.params

C = m*C + (1-m)*cat([t1, t2]).mean(dim=0)

def H(t, s):

t = t.detach() # stop gradient

s = softmax(s / tps, dim=1)

t = softmax((t - C) / tpt, dim=1) # center + sharpen

return - (t * log(s)).sum(dim=1).mean()

This loss is general and can be used on any number of views, even only 22.
However, we follow the standard setting for multi-crop by using 2 global views at resolution 2242224^{2} covering a large (for example greater than 50%50\%) area of the original image, and several local views of resolution 96296^{2} covering only small areas (for example less than 50%50\%) of the original image.
We refer to this setting as the basic parametrization of DINO, unless mentioned otherwise.

Both networks share the same architecture gg with different sets of parameters θs\theta_{s} and θt\theta_{t}.
We learn the parameters θs\theta_{s} by minimizing Eq. ([3](#S3.E3 "Equation 3 ‣ 3.1 SSL with Knowledge Distillation ‣ 3 Approach ‣ Emerging Properties in Self-Supervised Vision Transformers")) with stochastic gradient descent.

##### Teacher network.

Unlike knowledge distillation, we do not have a teacher gθtg_{\theta_{t}} given *a priori* and hence, we build it from past iterations of the student network.
We study different update rules for the teacher in Section [5.2](#S5.SS2 "5.2 Impact of the choice of Teacher Network ‣ 5 Ablation Study of DINO ‣ Emerging Properties in Self-Supervised Vision Transformers") and show that freezing the teacher network over an epoch works surprisingly well in our framework, while copying the student weight for the teacher fails to converge.
Of particular interest, using an exponential moving average (EMA) on the student weights, i.e., a momentum encoder [[13](#as1_bib.bib13)], is particularly well suited for our framework.
The update rule is θt←λ​θt+(1−λ)​θs,\theta_{t}\leftarrow\lambda\theta_{t}+(1-\lambda)\theta_{s}, with λ\lambda following a cosine schedule from 0.9960.996 to 11 during training [[12](#as1_bib.bib12)].
Originally the momentum encoder has been introduced as a substitute for a queue in contrastive learning [[13](#as1_bib.bib13)].
However, in our framework, its role differs since we do not have a queue nor a contrastive loss, and may be closer to the role of the mean teacher used in self-training [[24](#as1_bib.bib24)].
Indeed, we observe that this teacher performs a form of model ensembling similar to Polyak-Ruppert averaging with an exponential decay [[20](#as1_bib.bib20), [59](#bib.bib59)].
Using Polyak-Ruppert averaging for model ensembling is a standard practice to improve the performance of a model [[38](#bib.bib38)].
We observe that this teacher has better performance than the student throughout the training, and hence, guides the training of the student by providing target features of higher quality.
This dynamic was not observed in previous works [[12](#as1_bib.bib12), [58](#bib.bib58)].

Table 1: Networks configuration.
“Blocks” is the number of Transformer blocks, “dim” is channel dimension and “heads” is the number of heads in multi-head attention.
“# tokens” is the length of the token sequence when considering 2242224^{2} resolution inputs, “# params” is the total number of parameters (without counting the projection head) and “im/s” is the inference time on a NVIDIA V100 GPU with 128 samples per forward.

| model | blocks | dim | heads | #tokens | #params | im/s |
| --- | --- | --- | --- | --- | --- | --- |
| ResNet-50 | – | 2048 | – | – | 23M | 1237 |
| ViT-S/16 | 12 | 384 | 6 | 197 | 21M | 1007 |
| ViT-S/8 | 12 | 384 | 6 | 785 | 21M | 180 |
| ViT-B/16 | 12 | 768 | 12 | 197 | 85M | 312 |
| ViT-B/8 | 12 | 768 | 12 | 785 | 85M | 63 |

##### Network architecture.

The neural network gg is composed of a backbone ff (ViT [[10](#as1_bib.bib10)] or ResNet [[34](#bib.bib34)]), and of a projection head hh: g=h∘fg=h\circ f.
The features used in downstream tasks are the backbone ff output.
The projection head consists of a 3-layer multi-layer perceptron (MLP) with hidden dimension 20482048 followed by ℓ2\ell_{2} normalization and a weight normalized fully connected layer [[22](#as1_bib.bib22)] with KK dimensions, which is similar to the design from SwAV [[3](#as1_bib.bib3)].
We have tested other projection heads and this particular design appears to work best for DINO (Appendix [C](#Sx1.SS3 "C Projection Head ‣ Appendix ‣ Emerging Properties in Self-Supervised Vision Transformers")).
We do not use a predictor [[12](#as1_bib.bib12), [7](#as1_bib.bib7)], resulting in the exact same architecture in both student and teacher networks.
Of particular interest, we note that unlike standard convnets, ViT architectures do not use batch normalizations (BN) by default.
Therefore, when applying DINO to ViT we do not use any BN also in the projection heads, making the system *entirely BN-free*.

##### Avoiding collapse.

Several self-supervised methods differ by the operation used to avoid collapse, either through contrastive loss [[27](#as1_bib.bib27)], clustering constraints [[8](#bib.bib8), [3](#as1_bib.bib3)], predictor [[12](#as1_bib.bib12)] or batch normalizations [[12](#as1_bib.bib12), [58](#bib.bib58)].
While our framework can be stabilized with multiple normalizations [[3](#as1_bib.bib3)], it can also work with only a centering and sharpening of the momentum teacher outputs to avoid model collapse.
As shown experimentally in Section [5.3](#S5.SS3 "5.3 Avoiding collapse ‣ 5 Ablation Study of DINO ‣ Emerging Properties in Self-Supervised Vision Transformers"), centering prevents one dimension to dominate but encourages collapse to the uniform distribution, while the sharpening has the opposite effect.
Applying both operations balances their effects which is sufficient to avoid collapse in presence of a momentum teacher.
Choosing this method to avoid collapse trades stability for less dependence over the batch:
the centering operation only depends on first-order batch statistics and can be interpreted as adding a bias term cc to the teacher: gt​(x)←gt​(x)+cg_{t}(x)\leftarrow g_{t}(x)+c.
The center cc is updated with an exponential moving average, which allows the approach to work well across different batch sizes as shown in Section [5.5](#S5.SS5 "5.5 Training with small batches ‣ 5 Ablation Study of DINO ‣ Emerging Properties in Self-Supervised Vision Transformers"):

|  |  |  |  |
| --- | --- | --- | --- |
|  | c←m​c+(1−m)​1B​∑i=1Bgθt​(xi),c\leftarrow mc+(1-m)\frac{1}{B}\sum_{i=1}^{B}g_{\theta_{t}}(x_{i}), |  | (4) |

where m>0m>0 is a rate parameter and BB is the batch size.
Output sharpening is obtained by using a low value for the temperature τt\tau_{t} in the teacher softmax normalization.

### 3.2 Implementation and evaluation protocols

In this section, we provide the implementation details to train with DINO and present the evaluation protocols used in our experiments.

##### Vision Transformer.

We briefly describe the mechanism of the Vision Transformer (ViT) [[10](#as1_bib.bib10), [70](#bib.bib70)] and refer to Vaswani *et al*. [[70](#bib.bib70)] for details about Transformers and to Dosovitskiy *et al*. [[10](#as1_bib.bib10)] for its adaptation to images.
We follow the implementation used in DeiT [[25](#as1_bib.bib25)].
We summarize the configuration of the different networks used in this paper in Table [1](#S3.T1 "Table 1 ‣ Teacher network. ‣ 3.1 SSL with Knowledge Distillation ‣ 3 Approach ‣ Emerging Properties in Self-Supervised Vision Transformers").
The ViT architecture takes as input a grid of non-overlapping contiguous image patches of resolution N×NN\times N.
In this paper we typically use N=16N=16 (“/16”) or N=8N=8 (“/8”).
The patches are then passed through a linear layer to form a set of embeddings.
We add an extra learnable token to the sequence [[9](#as1_bib.bib9), [10](#as1_bib.bib10)].
The role of this token is to aggregate information from the entire sequence and we attach the projection head hh at its output.
We refer to this token as the class token [CLS] for consistency with previous works[[9](#as1_bib.bib9), [10](#as1_bib.bib10), [25](#as1_bib.bib25)], even though it is not attached to any label nor supervision in our case.
The set of patch tokens and [CLS] token are fed to a standard Transformer network with a “pre-norm” layer normalization [[11](#bib.bib11), [39](#bib.bib39)].
The Transformer is a sequence of self-attention and feed-forward layers, paralleled with skip connections.
The self-attention layers update the token representations by looking at the other token representations with an attention mechanism [[4](#bib.bib4)].

##### Implementation details.

We pretrain the models on the ImageNet dataset [[21](#as1_bib.bib21)] without labels.
We train with the adamw optimizer [[44](#bib.bib44)] and a batch size of 10241024, distributed over 1616 GPUs when using ViT-S/16.
The learning rate is linearly ramped up during the first 1010 epochs to its base value determined with the following linear scaling rule [[29](#bib.bib29)]: l​r=0.0005∗batchsize/256lr=0.0005*\text{batchsize}/256.
After this warmup, we decay the learning rate with a cosine schedule [[43](#bib.bib43)].
The weight decay also follows a cosine schedule from 0.040.04 to 0.40.4.
The temperature τs\tau_{s} is set to 0.10.1 while we use a linear warm-up for τt\tau_{t} from 0.040.04 to 0.070.07 during the first 3030 epochs.
We follow the data augmentations of BYOL [[12](#as1_bib.bib12)] (color jittering, Gaussian blur and solarization) and multi-crop [[3](#as1_bib.bib3)] with a bicubic interpolation to adapt the position embeddings to the scales [[10](#as1_bib.bib10), [25](#as1_bib.bib25)].
The code and models to reproduce our results is publicly available.

##### Evaluation protocols.

Standard protocols for self-supervised learning are to either learn a linear classifier on frozen features [[82](#bib.bib82), [13](#as1_bib.bib13)] or to finetune the features on downstream tasks.
For linear evaluations, we apply random resize crops and horizontal flips augmentation during training, and report accuracy on a central crop.
For finetuning evaluations, we initialize networks with the pretrained weights and adapt them during training.
However, both evaluations are sensitive to hyperparameters, and we observe a large variance in accuracy between runs when varying the learning rate for example.
We thus also evaluate the quality of features with a simple weighted nearest neighbor classifier (kk-NN) as in [[27](#as1_bib.bib27)].
We freeze the pretrain model to compute and store the features of the training data of the downstream task.
The nearest neighbor classifier then matches the feature of an image to the kk nearest stored features that votes for the label.
We sweep over different number of nearest neighbors and find that 2020 NN is consistently working the best for most of our runs.
This evaluation protocol does not require any other hyperparameter tuning, nor data augmentation and can be run with only one pass over the downstream dataset, greatly simplifying the feature evaluation.

Table 2: 
Linear and kk-NN classification on ImageNet.
We report top-1 accuracy for linear and kk-NN evaluations on the validation set of ImageNet for different self-supervised methods.
We focus on ResNet-50 and ViT-small architectures, but also report the best results obtained across architectures.
∗ are run by us.
We run the kk-NN evaluation for models with official released weights.
The throughput (im/s) is calculated on a NVIDIA V100 GPU with 128 samples per forward.
Parameters (M) are of the feature extractor.

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| Method | Arch. | Param. | im/s | Linear | kk-NN |
| Supervised | RN50 | 23 | 1237 | 79.3 | 79.3 |
| SCLR [[4](#as1_bib.bib4)] | RN50 | 23 | 1237 | 69.1 | 60.7 |
| MoCov2 [[6](#as1_bib.bib6)] | RN50 | 23 | 1237 | 71.1 | 61.9 |
| InfoMin [[67](#bib.bib67)] | RN50 | 23 | 1237 | 73.0 | 65.3 |
| BarlowT [[81](#bib.bib81)] | RN50 | 23 | 1237 | 73.2 | 66.0 |
| OBoW [[27](#bib.bib27)] | RN50 | 23 | 1237 | 73.8 | 61.9 |
| BYOL [[12](#as1_bib.bib12)] | RN50 | 23 | 1237 | 74.4 | 64.8 |
| DCv2 [[3](#as1_bib.bib3)] | RN50 | 23 | 1237 | 75.2 | 67.1 |
| SwAV [[3](#as1_bib.bib3)] | RN50 | 23 | 1237 | 75.3 | 65.7 |
| DINO | RN50 | 23 | 1237 | 75.3 | 67.5 |
| Supervised | ViT-S | 21 | 1007 | 79.8 | 79.8 |
| BYOL∗ [[12](#as1_bib.bib12)] | ViT-S | 21 | 1007 | 71.4 | 66.6 |
| MoCov2∗ [[6](#as1_bib.bib6)] | ViT-S | 21 | 1007 | 72.7 | 64.4 |
| SwAV∗ [[3](#as1_bib.bib3)] | ViT-S | 21 | 1007 | 73.5 | 66.3 |
| DINO | ViT-S | 21 | 1007 | 77.0 | 74.5 |
| Comparison across architectures | | | | |  |
| SCLR [[4](#as1_bib.bib4)] | RN50w4 | 375 | 117 | 76.8 | 69.3 |
| SwAV [[3](#as1_bib.bib3)] | RN50w2 | 93 | 384 | 77.3 | 67.3 |
| BYOL [[12](#as1_bib.bib12)] | RN50w2 | 93 | 384 | 77.4 | – |
| DINO | ViT-B/16 | 85 | 312 | 78.2 | 76.1 |
| SwAV [[3](#as1_bib.bib3)] | RN50w5 | 586 | 76 | 78.5 | 67.1 |
| BYOL [[12](#as1_bib.bib12)] | RN50w4 | 375 | 117 | 78.6 | – |
| BYOL [[12](#as1_bib.bib12)] | RN200w2 | 250 | 123 | 79.6 | 73.9 |
| DINO | ViT-S/8 | 21 | 180 | 79.7 | 78.3 |
| SCLRv2 [[5](#as1_bib.bib5)] | RN152w3+SK | 794 | 46 | 79.8 | 73.1 |
| DINO | ViT-B/8 | 85 | 63 | 80.1 | 77.4 |

## 4 Main Results

We first validate the DINO framework used in this study with the standard self-supervised benchmark on ImageNet.
We then study the properties of the resulting features for retrieval, object discovery and transfer-learning.

### 4.1 Comparing with SSL frameworks on ImageNet

We consider two different settings: comparison with the same architecture and across architectures.

##### Comparing with the same architecture.

In top panel of Table [2](#S3.T2 "Table 2 ‣ Evaluation protocols. ‣ 3.2 Implementation and evaluation protocols ‣ 3 Approach ‣ Emerging Properties in Self-Supervised Vision Transformers"), we compare DINO with other self-supervised methods with the same architecture, either a ResNet-50 [[34](#bib.bib34)] or a ViT-small (which follows the design of DeiT-S [[25](#as1_bib.bib25)]).
The choice of ViT-S is motivated by its similarity with ResNet-50 along several axes: number of parameters (21M vs 23M), throughput (1237/sec VS 1007 im/sec) and supervised performance on ImageNet with the training procedure of [[25](#as1_bib.bib25)] (79.3% VS 79.8%).
We explore variants of ViT-S in Appendix [D](#Sx1.SS4 "D Additional Ablations ‣ Appendix ‣ Emerging Properties in Self-Supervised Vision Transformers").
First, we observe that DINO performs on par with the state of the art on ResNet-50, validating that DINO works in the standard setting.
When we switch to a ViT architecture, DINO outperforms BYOL, MoCov2 and SwAV by +3.5% with linear classification and by +7.9% with kk-NN evaluation.
More surprisingly, the performance with a simple kk-NN classifier is almost on par with a linear classifier (74.5% versus 77.0%).
This property emerges only when using DINO with ViT architectures, and does not appear with other existing self-supervised methods nor with a ResNet-50.

##### Comparing across architectures.

On the bottom panel of Table [2](#S3.T2 "Table 2 ‣ Evaluation protocols. ‣ 3.2 Implementation and evaluation protocols ‣ 3 Approach ‣ Emerging Properties in Self-Supervised Vision Transformers"), we compare the best performance obtained across architectures.
The interest of this setting is not to compare methods directly, but to evaluate the limits of a ViT trained with DINO when moving to larger architectures.
While training a larger ViT with DINO improves the performance, reducing the size of the patches (“/8” variants) has a bigger impact on the performance.
While reducing the patch size do not add parameters, it still leads to a significant reduction of running time, and larger memory usage.
Nonetheless, a base ViT with 8×88\times 8 patches trained with DINO achieves 80.1% top-1 in linear classification and 77.4% with a kk-NN classifier with 10×10\times less parameters and 1.4×1.4\times faster run time than previous state of the art [[5](#as1_bib.bib5)].

### 4.2 Properties of ViT trained with SSL

We evaluate properties of the DINO features in terms of nearest neighbor search, retaining information about object location and transferability to downstream tasks.

Table 3: Image retrieval.
We compare the performance in retrieval of off-the-shelf features pretrained with supervision or with DINO on ImageNet and Google Landmarks v2 (GLDv2) dataset.
We report mAP on revisited Oxford and Paris.
Pretraining with DINO on a landmark dataset performs particularly well.
For reference, we also report the best retrieval method with off-the-shelf features [[57](#bib.bib57)].

|  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  | ℛ\mathcal{R}Ox | | ℛ\mathcal{R}Par | |
| Pretrain | Arch. | Pretrain | M | H | M | H |
| Sup. [[57](#bib.bib57)] | RN101+R-MAC | ImNet | 49.8 | 18.5 | 74.0 | 52.1 |
| Sup. | ViT-S/16 | ImNet | 33.5 | 8.9 | 63.0 | 37.2 |
| DINO | ResNet-50 | ImNet | 35.4 | 11.1 | 55.9 | 27.5 |
| DINO | ViT-S/16 | ImNet | 41.8 | 13.7 | 63.1 | 34.4 |
| DINO | ViT-S/16 | GLDv2 | 51.5 | 24.3 | 75.3 | 51.6 |

#### 4.2.1 Nearest neighbor retrieval with DINO ViT

The results on ImageNet classification have exposed the potential of our features for tasks relying on nearest neighbor retrieval.
In this set of experiments, we further consolidate this finding on landmark retrieval and copy detection tasks.

##### Image Retrieval.

We consider the revisited [[53](#bib.bib53)] Oxford and Paris image retrieval datasets [[50](#bib.bib50)].
They contain 3 different splits of gradual difficulty with query/database pairs.
We report the Mean Average Precision (mAP) for the Medium (M) and Hard (H) splits.
In Table [3](#S4.T3 "Table 3 ‣ 4.2 Properties of ViT trained with SSL ‣ 4 Main Results ‣ Emerging Properties in Self-Supervised Vision Transformers"), we compare the performance of different *off-the-shelf* features obtained with either supervised or DINO training.
We freeze the features and directly apply kk-NN for retrieval.
We observe that DINO features outperform those trained on ImageNet with labels.

An advantage of SSL approaches is that they can be trained on any dataset, without requiring any form of annotations.
We train DINO on the 1.2M clean set from Google Landmarks v2 (GLDv2) [[72](#bib.bib72)], a dataset of landmarks designed for retrieval purposes.
DINO ViT features trained on GLDv2 are remarkably good, outperforming previously published methods based on off-the-shelf descriptors [[68](#bib.bib68), [57](#bib.bib57)].

Table 4: Copy detection.
We report the mAP performance in copy detection on Copydays “strong” subset [[21](#bib.bib21)].
For reference, we also report the performance of the multigrain model [[5](#bib.bib5)], trained specifically for particular object retrieval.

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| Method | Arch. | Dim. | Resolution | mAP |
| Multigrain [[5](#bib.bib5)] | ResNet-50 | 2048 | 2242224^{2} | 75.1 |
| Multigrain [[5](#bib.bib5)] | ResNet-50 | 2048 | largest side 800 | 82.5 |
| Supervised [[25](#as1_bib.bib25)] | ViT-B/16 | 1536 | 2242224^{2} | 76.4 |
| DINO | ViT-B/16 | 1536 | 2242224^{2} | 81.7 |
| DINO | ViT-B/8 | 1536 | 3202320^{2} | 85.5 |

##### Copy detection.

We also evaluate the performance of ViTs trained with DINO on a copy detection task.
We report the mean average precision on the “strong” subset of the INRIA Copydays dataset [[21](#bib.bib21)].
The task is to recognize images that have been distorted by blur, insertions, print and scan, etc.
Following prior work [[5](#bib.bib5)], we add 10k distractor images randomly sampled from the YFCC100M dataset [[66](#bib.bib66)].
We perform copy detection directly with cosine similarity on the features obtained from our pretrained network.
The features are obtained as the concatenation of the output [CLS] token and of the GeM pooled [[54](#bib.bib54)] output patch tokens.
This results in a 1536d descriptor for ViT-B.
Following [[5](#bib.bib5)], we apply whitening on the features.
We learn this transformation on an extra 20K random images from YFCC100M, distincts from the distractors.
Table [4](#S4.T4 "Table 4 ‣ Image Retrieval. ‣ 4.2.1 Nearest neighbor retrieval with DINO ViT ‣ 4.2 Properties of ViT trained with SSL ‣ 4 Main Results ‣ Emerging Properties in Self-Supervised Vision Transformers") shows that ViT trained with DINO is very competitive on copy detection.

Table 5: DAVIS 2017 Video object segmentation.
We evaluate the quality of frozen features on video instance tracking.
We report mean region similarity 𝒥m\mathcal{J}_{m} and mean contour-based accuracy ℱm\mathcal{F}_{m}.
We compare with existing self-supervised methods and a supervised ViT-S/8 trained on ImageNet.
Image resolution is 480p.

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| Method | Data | Arch. | (𝒥CLOSE(\mathcal{J}&OPENℱ)m\mathcal{F})_{m} | 𝒥m\mathcal{J}_{m} | ℱm\mathcal{F}_{m} |
| Supervised | | | |  |  |
| ImageNet | INet | ViT-S/8 | 66.0 | 63.9 | 68.1 |
| STM [[18](#as1_bib.bib18)] | I/D/Y | RN50 | 81.8 | 79.2 | 84.3 |
| Self-supervised | | | |  |  |
| CT [[26](#as1_bib.bib26)] | VLOG | RN50 | 48.7 | 46.4 | 50.0 |
| MAST [[15](#as1_bib.bib15)] | YT-VOS | RN18 | 65.5 | 63.3 | 67.6 |
| STC [[14](#as1_bib.bib14)] | Kinetics | RN18 | 67.6 | 64.8 | 70.2 |
| DINO | INet | ViT-S/16 | 61.8 | 60.2 | 63.4 |
| DINO | INet | ViT-B/16 | 62.3 | 60.7 | 63.9 |
| DINO | INet | ViT-S/8 | 69.9 | 66.6 | 73.1 |
| DINO | INet | ViT-B/8 | 71.4 | 67.9 | 74.9 |

|  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- |
| Refer to caption | Refer to caption |  |  |  | Refer to caption | Refer to caption |
| Refer to caption | Refer to caption |  |  |  | Refer to caption | Refer to caption |
| Refer to caption | Refer to caption |  |  |  | Refer to caption | Refer to caption |
| Refer to caption | Refer to caption |  |  |  | Refer to caption | Refer to caption |

Figure 3: Attention maps from multiple heads.
We consider the heads from the last layer of a ViT-S/8 trained with DINO and display the self-attention for [CLS] token query.
Different heads, materialized by different colors, focus on different locations that represents different objects or parts
(more examples in Appendix).

#### 4.2.2 Discovering the semantic layout of scenes

As shown qualitatively in Figure [1](#S0.F1 "Figure 1 ‣ Emerging Properties in Self-Supervised Vision Transformers"), our self-attention maps contain information about the segmentation of an image.
In this study, we measure this property on a standard benchmark as well as by directly probing the quality of masks generated from these attention maps.

##### Video instance segmentation.

In Tab. [5](#S4.T5 "Table 5 ‣ Copy detection. ‣ 4.2.1 Nearest neighbor retrieval with DINO ViT ‣ 4.2 Properties of ViT trained with SSL ‣ 4 Main Results ‣ Emerging Properties in Self-Supervised Vision Transformers"), we evaluate the output patch tokens on the DAVIS-2017 video instance segmentation benchmark [[52](#bib.bib52)].
We follow the experimental protocol in Jabri *et al*. [[14](#as1_bib.bib14)] and segment scenes with a nearest-neighbor between consecutive frames; we thus do not train any model on top of the features, nor finetune any weights for the task.
We observe in Tab. [5](#S4.T5 "Table 5 ‣ Copy detection. ‣ 4.2.1 Nearest neighbor retrieval with DINO ViT ‣ 4.2 Properties of ViT trained with SSL ‣ 4 Main Results ‣ Emerging Properties in Self-Supervised Vision Transformers") that even though our training objective nor our architecture are designed for dense tasks, the performance is competitive on this benchmark.
Since the network is not finetuned, the output of the model must have retained some spatial information.
Finally, for this dense recognition task, the variants with small patches (“/8”) perform much better (+9.1%9.1\% (𝒥CLOSE(\mathcal{J}&OPENℱ)m\mathcal{F})_{m} for ViT-B).

##### Probing the self-attention map.

In Fig. [3](#S4.F3 "Figure 3 ‣ Copy detection. ‣ 4.2.1 Nearest neighbor retrieval with DINO ViT ‣ 4.2 Properties of ViT trained with SSL ‣ 4 Main Results ‣ Emerging Properties in Self-Supervised Vision Transformers"), we show that different heads can attend to different semantic regions of an image, even when they are occluded (the bushes on the third row) or small (the flag on the second row).
Visualizations are obtained with 480480p images, resulting in sequences of 3601 tokens for ViT-S/8.
In Fig. [4](#S4.F4 "Figure 4 ‣ Probing the self-attention map. ‣ 4.2.2 Discovering the semantic layout of scenes ‣ 4.2 Properties of ViT trained with SSL ‣ 4 Main Results ‣ Emerging Properties in Self-Supervised Vision Transformers"), we show that a supervised ViT does not attend well to objects in presence of clutter both qualitatively and quantitatively.
We report the Jaccard similarity between the ground truth and segmentation masks obtained by thresholding the self-attention map to keep 60% of the mass.
Note that the self-attention maps are smooth and not optimized to produce a mask.
Nonetheless, we see a clear difference between the supervised or DINO models with a significant gap in terms of Jaccard similarities.
Note that self-supervised convnets also contain information about segmentations but it requires dedicated methods to extract it from their weights [[31](#bib.bib31)].

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| Supervised |  |  |  |  |
| Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption |
| DINO |  |  |  |  |
| Refer to caption | Refer to caption | Refer to caption | Refer to caption | Refer to caption |

|  | Random | Supervised | DINO |
| --- | --- | --- | --- |
| ViT-S/16 | 22.0 | 27.3 | 45.9 |
| ViT-S/8 | 21.8 | 23.7 | 44.7 |

Figure 4: Segmentations from supervised versus DINO.
We visualize masks obtained by thresholding the self-attention maps to keep 60% of the mass.
On top, we show the resulting masks for a ViT-S/8 trained with supervision and DINO.
We show the best head for both models.
The table at the bottom compares the Jaccard similarity between the ground truth and these masks on the validation images of PASCAL VOC12 dataset.

#### 4.2.3 Transfer learning on downstream tasks

In Tab. [6](#S4.T6 "Table 6 ‣ 4.2.3 Transfer learning on downstream tasks ‣ 4.2 Properties of ViT trained with SSL ‣ 4 Main Results ‣ Emerging Properties in Self-Supervised Vision Transformers"), we evaluate the quality of the features pretrained with DINO on different downstream tasks.
We compare with features from the same architectures trained with supervision on ImageNet.
We follow the protocol used in Touvron *et al*. [[25](#as1_bib.bib25)] and finetune the features on each downstream task.
We observe that for ViT architectures, self-supervised pretraining transfers better than features trained with supervision, which is consistent with observations made on convolutional networks [[3](#as1_bib.bib3), [13](#as1_bib.bib13), [62](#bib.bib62)].
Finally, self-supervised pretraining greatly improves results on ImageNet (+1-2%).

Table 6: Transfer learning by finetuning pretrained models on different datasets.
We report top-1 accuracy.
Self-supervised pretraining with DINO transfers better than supervised pretraining.

|  | Cifar10{}_{\text{10}} | Cifar100{}_{\text{100}} | INat18{}_{\text{18}} | INat19{}_{\text{19}} | Flwrs | Cars | INet |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ViT-S/16 |  |  |  |  |  |  |  |
| Sup. [[25](#as1_bib.bib25)] | 99.0 | 89.5 | 70.7 | 76.6 | 98.2 | 92.1 | 79.9 |
| DINO | 99.0 | 90.5 | 72.0 | 78.2 | 98.5 | 93.0 | 81.5 |
| ViT-B/16 |  |  |  |  |  |  |  |
| Sup. [[25](#as1_bib.bib25)] | 99.0 | 90.8 | 73.2 | 77.7 | 98.4 | 92.1 | 81.8 |
| DINO | 99.1 | 91.7 | 72.6 | 78.6 | 98.8 | 93.0 | 82.8 |

## 5 Ablation Study of DINO

In this section, we empirically study DINO applied to ViT.
The model considered for this entire study is ViT-S.
We also refer the reader to Appendix for additional studies.

### 5.1 Importance of the Different Components

We show the impact of adding different components from self-supervised learning on ViT trained with our framework.

Table 7: 
Important component for self-supervised ViT pretraining.
Models are trained for 300 epochs with ViT-S/16.
We study the different components that matter for the kk-NN and linear (“Lin.”) evaluations.
For the different variants, we highlight the differences from the default DINO setting.
The best combination is the momentum encoder with the multicrop augmentation and the cross-entropy loss.
We also report results with BYOL [[12](#as1_bib.bib12)], MoCo-v2 [[6](#as1_bib.bib6)] and SwAV [[3](#as1_bib.bib3)].

|  | Method | Mom. | SK | MC | Loss | Pred. | kk-NN | Lin. |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | DINO | ✓ | ✗ | ✓ | CE | ✗ | 72.8 | 76.1 |
| 2 |  | ✗ | ✗ | ✓ | CE | ✗ | 0.1 | 0.1 |
| 3 |  | ✓ | ✓ | ✓ | CE | ✗ | 72.2 | 76.0 |
| 4 |  | ✓ | ✗ | ✗ | CE | ✗ | 67.9 | 72.5 |
| 5 |  | ✓ | ✗ | ✓ | MSE | ✗ | 52.6 | 62.4 |
| 6 |  | ✓ | ✗ | ✓ | CE | ✓ | 71.8 | 75.6 |
| 7 | BYOL | ✓ | ✗ | ✗ | MSE | ✓ | 66.6 | 71.4 |
| 8 | MoCov2 | ✓ | ✗ | ✗ | INCE | ✗ | 62.0 | 71.6 |
| 9 | SwAV | ✗ | ✓ | ✓ | CE | ✗ | 64.7 | 71.8 |
| SK: Sinkhorn-Knopp, MC: Multi-Crop, Pred.: Predictor | | | | | | | | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CE: Cross-Entropy, MSE: Mean Square Error, INCE: InfoNCE | | | | | | | | |

In Table [7](#S5.T7 "Table 7 ‣ 5.1 Importance of the Different Components ‣ 5 Ablation Study of DINO ‣ Emerging Properties in Self-Supervised Vision Transformers"), we report different model variants as we add or remove components.
First, we observe that in the absence of momentum, our framework does not work (row 2) and more advanced operations, SK for example, are required to avoid collapse (row 9).
However, with momentum, using SK has little impact (row 3).
In addtition, comparing rows 3 and 9 highlights the importance of the momentum encoder for performance.
Second, in rows 4 and 5, we observe that multi-crop training and the cross-entropy loss in DINO are important components to obtain good features.
We also observe that adding a predictor to the student network has little impact (row 6) while it is critical in BYOL to prevent collapse [[7](#as1_bib.bib7), [12](#as1_bib.bib12)].
For completeness, we propose in Appendix [B](#Sx1.SS2 "B Methodology Comparison ‣ Appendix ‣ Emerging Properties in Self-Supervised Vision Transformers") an extended version of this ablation study.

##### Importance of the patch size.

In Fig. [5](#S5.F5.fig1 "Figure 5 ‣ Importance of the patch size. ‣ 5.1 Importance of the Different Components ‣ 5 Ablation Study of DINO ‣ Emerging Properties in Self-Supervised Vision Transformers"), we compare the kk-NN classification performance of ViT-S models trained with different patch sizes, 16×1616\times 16, 8×88\times 8 and 5×55\times 5.
We also compare to ViT-B with 16×1616\times 16 and 8×88\times 8 patches.
All the models are trained for 300 epochs.
We observe that the performance greatly improves as we decrease the size of the patch.
It is interesting to see that performance can be greatly improved without adding additional parameters.
However, the performance gain from using smaller patches comes at the expense of throughput: when using 5×\times5 patches, the throughput falls to 44 im/s, *vs* 180 im/s for 8×\times8 patches.

Figure 5: 
Effect of Patch Size.
kk-NN evaluation as a function of the throughputs for different input patch sizes with ViT-B and ViT-S. Models are trained for 300 epochs.

### 5.2 Impact of the choice of Teacher Network

In this ablation, we experiment with different teacher network to understand its role in DINO.
We compare models trained for 300300 epochs using the kk-NN protocol.

##### Building different teachers from the student.

In Fig. [6](#S5.F6 "Figure 6 ‣ Analyzing the training dynamic. ‣ 5.2 Impact of the choice of Teacher Network ‣ 5 Ablation Study of DINO ‣ Emerging Properties in Self-Supervised Vision Transformers")(right), we compare different strategies to build the teacher from previous instances of the student besides the momentum teacher.
First we consider using the student network from a previous epoch as a teacher.
This strategy has been used in a memory bank [[27](#as1_bib.bib27)] or as a form of clustering hard-distillation [[8](#bib.bib8), [2](#bib.bib2), [14](#bib.bib14)].
Second, we consider using the student network from the previous iteration, as well as a copy of the student for the teacher.
In our setting, using a teacher based on a recent version of the student does not converge.
This setting requires more normalizations to work.
Interestingly, we observe that using a teacher from the previous epoch does not collapse, providing performance in the kk-NN evaluation competitive with existing frameworks such as MoCo-v2 or BYOL.
While using a momentum encoder clearly provides superior performance to this naive teacher, this finding suggests that there is a space to investigate alternatives for the teacher.

##### Analyzing the training dynamic.

To further understand the reasons why a momentum teacher works well in our framework, we study its dynamic during the training of a ViT in the left panel of Fig. [6](#S5.F6 "Figure 6 ‣ Analyzing the training dynamic. ‣ 5.2 Impact of the choice of Teacher Network ‣ 5 Ablation Study of DINO ‣ Emerging Properties in Self-Supervised Vision Transformers").
A key observation is that this teacher constantly outperforms the student during the training, and we observe the same behavior when training with a ResNet-50 (Appendix [D](#Sx1.SS4 "D Additional Ablations ‣ Appendix ‣ Emerging Properties in Self-Supervised Vision Transformers")).
This behavior has not been observed by other frameworks also using momentum [[13](#as1_bib.bib13), [12](#as1_bib.bib12)], nor when the teacher is built from the previous epoch.
We propose to interpret the momentum teacher in DINO as a form of Polyak-Ruppert averaging [[20](#as1_bib.bib20), [59](#bib.bib59)] with an exponentially decay.
Polyak-Ruppert averaging is often used to simulate model ensembling to improve the performance of a network at the end of the training [[38](#bib.bib38)].
Our method can be interpreted as applying Polyak-Ruppert averaging during the training to constantly build a model ensembling that has superior performances.
This model ensembling then guides the training of the student network [[24](#as1_bib.bib24)].

| Teacher | Top-1 |
| --- | --- |
| Student copy | 0.1 |
| Previous iter | 0.1 |
| Previous epoch | 66.6 |
| Momentum | 72.8 |

Figure 6: 
Top-1 accuracy on ImageNet validation with kk-NN classifier.
(left) Comparison between the performance of the momentum teacher and the student during training.
(right) Comparison between different types of teacher network.
The momentum encoder leads to the best performance but is not the only viable option.

### 5.3 Avoiding collapse

Figure 7: 
Collapse study.
(left): evolution of the teacher’s target entropy along training epochs;
(right): evolution of KL divergence between teacher and student outputs.

We study the complementarity role of centering and target sharpening to avoid collapse.
There are two forms of collapse: regardless of the input, the model output is uniform along all the dimensions or dominated by one dimension.
The centering avoids the collapse induced by a dominant dimension, but encourages an uniform output.
Sharpening induces the opposite effect.
We show this complementarity by decomposing the cross-entropy HH into an entropy hh and the Kullback-Leibler divergence (“KL”) DK​LD_{KL}:

|  |  |  |  |
| --- | --- | --- | --- |
|  | H⁡(Pt,Ps)=h⁡(Pt)+DK​L​(Pt|Ps).H(P_{t},P_{s})=h(P_{t})+D_{KL}(P_{t}|P_{s}). |  | (5) |

A KL equal to zero indicates a constant output, and hence a collapse.
In Fig. [7](#S5.F7 "Figure 7 ‣ 5.3 Avoiding collapse ‣ 5 Ablation Study of DINO ‣ Emerging Properties in Self-Supervised Vision Transformers"), we plot the entropy and KL during training with and without centering and sharpening.
If one operation is missing, the KL converges to zero, indicating a collapse.
However, the entropy hh converges to different values: 00 with no centering and −log⁡(1/K)-\log(1/K) with no sharpening, indicating that both operations induce different form of collapse.
Applying both operations balances these effects (see study of the sharpening parameter τt\tau_{t} in Appendix [D](#Sx1.SS4 "D Additional Ablations ‣ Appendix ‣ Emerging Properties in Self-Supervised Vision Transformers")).

### 5.4 Compute requirements

Table 8: 
Time and memory requirements.
We show total running time and peak memory per GPU (“mem.”) when running ViT-S/16 DINO models on two 8-GPU machines.
We report top-1 ImageNet val acc with linear evaluation for several variants of multi-crop, each having a different level of compute requirement.

|  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  | 100 epochs | |  | 300 epochs | |  |
| multi-crop |  | top-1 | time |  | top-1 | time | mem. |
| ×22422\!\times\!224^{2} |  | 67.8 | 15.3h |  | 72.5 | 45.9h | 9.3G |
| ×2242+×9622\!\times\!224^{2}+\phantom{0}2\!\times\!96^{2} |  | 71.5 | 17.0h |  | 74.5 | 51.0h | 10.5G |
| ×2242+×9622\!\times\!224^{2}+\phantom{0}6\!\times\!96^{2} |  | 73.8 | 20.3h |  | 75.9 | 60.9h | 12.9G |
| ×2242+×9622\!\times\!224^{2}+10\!\times\!96^{2} |  | 74.6 | 24.2h |  | 76.1 | 72.6h | 15.4G |

In Tab. [8](#S5.T8 "Table 8 ‣ 5.4 Compute requirements ‣ 5 Ablation Study of DINO ‣ Emerging Properties in Self-Supervised Vision Transformers"), we detail the time and GPU memory requirements when running ViT-S/16 DINO models on two 88-GPU machines.
We report results with several variants of multi-crop training, each having a different level of compute requirement.
We observe in Tab. [8](#S5.T8 "Table 8 ‣ 5.4 Compute requirements ‣ 5 Ablation Study of DINO ‣ Emerging Properties in Self-Supervised Vision Transformers") that using multi-crop improves the accuracy / running-time tradeoff for DINO runs.
For example, the performance is 72.5%72.5\% after 4646 hours of training without multi-crop (i.e. ×22422\!\times\!224^{2}) while DINO in ×2242+×9622\!\times\!224^{2}+10\!\times\!96^{2} crop setting reaches 74.6%74.6\% in 2424 hours only.
This is an improvement of +2%+2\% while requiring ×2\!\times less time, though the memory usage is higher (15.4​G15.4G versus 9.3​G9.3G).
We observe that the performance boost brought with multi-crop cannot be caught up by more training in the ×22422\!\times\!224^{2} setting, which shows the value of the “local-to-global” augmentation.
Finally, the gain from adding more views diminishes (+.2% form ×6\!\times to ×10\!\times 96296^{2} crops) for longer trainings.

Overall, training DINO with Vision Transformers achieves 76.176.1 top-1 accuracy using two 8-GPU servers for 3 days.
This result outperforms state-of-the-art self-supervised systems based on convolutional networks of comparable sizes with a significant reduction of computational requirements [[12](#as1_bib.bib12), [3](#as1_bib.bib3)].
Our code is available to train self-supervised ViT on a limited number of GPUs.

### 5.5 Training with small batches

| bs | 128 | 256 | 512 | 1024 |
| --- | --- | --- | --- | --- |
| top-1 | 57.9 | 59.1 | 59.6 | 59.9 |

Table 9: 
Effect of batch sizes. Top-1 with kk-NN for models trained for 100 epochs without multi-crop.

In Tab. [9](#S5.T9.fig1 "Table 9 ‣ 5.5 Training with small batches ‣ 5 Ablation Study of DINO ‣ Emerging Properties in Self-Supervised Vision Transformers"), we study the impact of the batch size on the features obtained with DINO.
We also study the impact of the smooth parameter mm used in the centering update rule of Eq. [4](#S3.E4 "Equation 4 ‣ Avoiding collapse. ‣ 3.1 SSL with Knowledge Distillation ‣ 3 Approach ‣ Emerging Properties in Self-Supervised Vision Transformers") in Appendix [D](#Sx1.SS4 "D Additional Ablations ‣ Appendix ‣ Emerging Properties in Self-Supervised Vision Transformers").
We scale the learning rate linearly with the batch size [[29](#bib.bib29)]: l​r=0.0005∗batchsize/256lr=0.0005*\text{batchsize}/256.
Tab. [9](#S5.T9.fig1 "Table 9 ‣ 5.5 Training with small batches ‣ 5 Ablation Study of DINO ‣ Emerging Properties in Self-Supervised Vision Transformers") confirms that we can train models to high performance with small batches.
Results with the smaller batch sizes (b​s=128bs=128) are slightly below our default training setup of b​s=1024bs=1024, and would certainly require to re-tune hyperparameters like the momentum rates for example.
Note that the experiment with batch size of 128128 runs on only 11 GPU.
We have explored training a model with a batch size of 88, reaching 35.2%35.2\% after 5050 epochs, showing the potential for training large models that barely fit an image per GPU.

## 6 Conclusion

In this work, we have shown the potential of self-supervised pretraining a standard ViT model, achieving performance that are comparable with the best convnets specifically designed for this setting.
We have also seen emerged two properties that can be leveraged in future applications:
the quality of the features in kk-NN classification has a potential for image retrieval where ViT are already showing promising results [[22](#bib.bib22)].
The presence of information about the scene layout in the features can also benefit weakly supervised image segmentation.
However, the main result of this paper is that we have evidences that self-supervised learning could be the key to developing a BERT-like model based on ViT.
In the future, we plan to explore if pretraining a large ViT model with DINO on random uncurated images could push the limits of visual features [[28](#bib.bib28)].

##### Acknowledgement.

We thank Mahmoud Assran, Matthijs Douze, Allan Jabri, Jure Zbontar, Alaaeldin El-Nouby, Y-Lan Boureau, Kaiming He, Thomas Lucas as well as the Thoth and FAIR teams for their help, support and discussions around this project.
Julien Mairal was funded by the ERC grant number 714381 (SOLARIS project) and by ANR 3IA MIAI@Grenoble Alpes (ANR-19-P3IA-0003).

## References

- [1]

  Rohan Anil, Gabriel Pereyra, Alexandre Passos, Robert Ormandi, George E Dahl,
  and Geoffrey E Hinton.
  Large scale distributed neural network training through online
  distillation.
  arXiv preprint arXiv:1804.03235, 2018.
- [2]

  Yuki Markus Asano, Christian Rupprecht, and Andrea Vedaldi.
  Self-labelling via simultaneous clustering and representation
  learning.
  In ICLR, 2020.
- [3]

  Mahmoud Assran, Nicolas Ballas, Lluis Castrejon, and Michael Rabbat.
  Recovering petaflops in contrastive semi-supervised learning of
  visual representations.
  preprint arXiv:2006.10803, 2020.
- [4]

  Dzmitry Bahdanau, Kyunghyun Cho, and Yoshua Bengio.
  Neural machine translation by jointly learning to align and
  translate.
  preprint arXiv:1409.0473, 2014.
- [5]

  Maxim Berman, Hervé Jégou, Vedaldi Andrea, Iasonas Kokkinos, and
  Matthijs Douze.
  MultiGrain: a unified image embedding for classes and instances.
  arXiv preprint arXiv:1902.05509, 2019.
- [6]

  Piotr Bojanowski and Armand Joulin.
  Unsupervised learning by predicting noise.
  In ICML, 2017.
- [7]

  Cristian Buciluǎ, Rich Caruana, and Alexandru Niculescu-Mizil.
  Model compression.
  In SIGKDD, 2006.
- [8]

  Mathilde Caron, Piotr Bojanowski, Armand Joulin, and Matthijs Douze.
  Deep clustering for unsupervised learning of visual features.
  In ECCV, 2018.
- [9]

  Mathilde Caron, Piotr Bojanowski, Julien Mairal, and Armand Joulin.
  Unsupervised pre-training of image features on non-curated data.
  In ICCV, 2019.
- [10]

  Mathilde Caron, Ishan Misra, Julien Mairal, Priya Goyal, Piotr Bojanowski, and
  Armand Joulin.
  Unsupervised learning of visual features by contrasting cluster
  assignments.
  In NeurIPS, 2020.
- [11]

  Mia Xu Chen, Orhan Firat, Ankur Bapna, Melvin Johnson, Wolfgang Macherey,
  George Foster, Llion Jones, Niki Parmar, Mike Schuster, Zhifeng Chen, et al.
  The best of both worlds: Combining recent advances in neural machine
  translation.
  preprint arXiv:1804.09849, 2018.
- [12]

  Ting Chen, Simon Kornblith, Mohammad Norouzi, and Geoffrey Hinton.
  A simple framework for contrastive learning of visual
  representations.
  preprint arXiv:2002.05709, 2020.
- [13]

  Ting Chen, Simon Kornblith, Kevin Swersky, Mohammad Norouzi, and Geoffrey
  Hinton.
  Big self-supervised models are strong semi-supervised learners.
  In NeurIPS, 2020.
- [14]

  Weijie Chen, Shiliang Pu, Di Xie, Shicai Yang, Yilu Guo, and Luojun Lin.
  Unsupervised image classification for deep representation learning.
  arXiv preprint arXiv:2006.11480, 2020.
- [15]

  Xinlei Chen, Haoqi Fan, Ross Girshick, and Kaiming He.
  Improved baselines with momentum contrastive learning.
  preprint arXiv:2003.04297, 2020.
- [16]

  Xinlei Chen and Kaiming He.
  Exploring simple siamese representation learning.
  preprint arXiv:2011.10566, 2020.
- [17]

  Marco Cuturi.
  Sinkhorn distances: Lightspeed computation of optimal transport.
  In NeurIPS, 2013.
- [18]

  Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova.
  Bert: Pre-training of deep bidirectional transformers for language
  understanding.
  preprint arXiv:1810.04805, 2018.
- [19]

  Alexey Dosovitskiy, Lucas Beyer, Alexander Kolesnikov, Dirk Weissenborn,
  Xiaohua Zhai, Thomas Unterthiner, Mostafa Dehghani, Matthias Minderer, Georg
  Heigold, Sylvain Gelly, et al.
  An image is worth 16x16 words: Transformers for image recognition at
  scale.
  preprint arXiv:2010.11929, 2020.
- [20]

  Alexey Dosovitskiy, Philipp Fischer, Jost Tobias Springenberg, Martin
  Riedmiller, and Thomas Brox.
  Discriminative unsupervised feature learning with exemplar
  convolutional neural networks.
  TPAMI, 2016.
- [21]

  Matthijs Douze, Hervé Jégou, Harsimrat Sandhawalia, Laurent Amsaleg,
  and Cordelia Schmid.
  Evaluation of gist descriptors for web-scale image search.
  In CIVR, 2009.
- [22]

  Alaaeldin El-Nouby, Natalia Neverova, Ivan Laptev, and Hervé Jégou.
  Training vision transformers for image retrieval.
  preprint arXiv:2102.05644, 2021.
- [23]

  Aleksandr Ermolov, Aliaksandr Siarohin, Enver Sangineto, and Nicu Sebe.
  Whitening for self-supervised representation learning.
  preprint arXiv:2007.06346, 2020.
- [24]

  Mark Everingham, Luc Van Gool, Christopher KI Williams, John Winn, and Andrew
  Zisserman.
  The pascal visual object classes (voc) challenge.
  IJCV, 2010.
- [25]

  Zhiyuan Fang, Jianfeng Wang, Lijuan Wang, Lei Zhang, Yezhou Yang, and Zicheng
  Liu.
  Seed: Self-supervised distillation for visual representation.
  2021.
- [26]

  Spyros Gidaris, Andrei Bursuc, Nikos Komodakis, Patrick Pérez, and Matthieu
  Cord.
  Learning representations by predicting bags of visual words.
  In CVPR, 2020.
- [27]

  Spyros Gidaris, Andrei Bursuc, Gilles Puy, Nikos Komodakis, Matthieu Cord, and
  Patrick Pérez.
  Online bag-of-visual-words generation for unsupervised representation
  learning.
  arXiv preprint arXiv:2012.11552, 2020.
- [28]

  Priya Goyal, Mathilde Caron, Benjamin Lefaudeux, Min Xu, Pengchao Wang, Vivek
  Pai, Mannat Singh, Vitaliy Liptchinsky, Ishan Misra, Armand Joulin, et al.
  Self-supervised pretraining of visual features in the wild.
  preprint arXiv:2103.01988, 2021.
- [29]

  Priya Goyal, Piotr Dollár, Ross Girshick, Pieter Noordhuis, Lukasz
  Wesolowski, Aapo Kyrola, Andrew Tulloch, Yangqing Jia, and Kaiming He.
  Accurate, large minibatch sgd: Training imagenet in 1 hour.
  preprint arXiv:1706.02677, 2017.
- [30]

  Jean-Bastien Grill, Florian Strub, Florent Altché, Corentin Tallec,
  Pierre H Richemond, Elena Buchatskaya, Carl Doersch, Bernardo Avila Pires,
  Zhaohan Daniel Guo, Mohammad Gheshlaghi Azar, Bilal Piot, Koray Kavukcuoglu,
  Rémi Munos, and Michal Valko.
  Bootstrap your own latent: A new approach to self-supervised
  learning.
  In NeurIPS, 2020.
- [31]

  Shir Gur, Ameen Ali, and Lior Wolf.
  Visualization of supervised and self-supervised neural networks via
  attribution guided factorization.
  preprint arXiv:2012.02166, 2020.
- [32]

  Michael Gutmann and Aapo Hyvärinen.
  Noise-contrastive estimation: A new estimation principle for
  unnormalized statistical models.
  In International Conference on Artificial Intelligence and
  Statistics, 2010.
- [33]

  Kaiming He, Haoqi Fan, Yuxin Wu, Saining Xie, and Ross Girshick.
  Momentum contrast for unsupervised visual representation learning.
  In CVPR, 2020.
- [34]

  Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian Sun.
  Deep residual learning for image recognition.
  In CVPR, 2016.
- [35]

  Geoffrey Hinton, Oriol Vinyals, and Jeff Dean.
  Distilling the knowledge in a neural network.
  preprint arXiv:1503.02531, 2015.
- [36]

  Jiabo Huang, Qi Dong, Shaogang Gong, and Xiatian Zhu.
  Unsupervised deep learning by neighbourhood discovery.
  In ICML, 2019.
- [37]

  Allan Jabri, Andrew Owens, and Alexei A Efros.
  Space-time correspondence as a contrastive random walk.
  2020.
- [38]

  Sébastien Jean, Kyunghyun Cho, Roland Memisevic, and Yoshua Bengio.
  On using very large target vocabulary for neural machine translation.
  preprint arXiv:1412.2007, 2014.
- [39]

  Guillaume Klein, Yoon Kim, Yuntian Deng, Jean Senellart, and Alexander M Rush.
  Opennmt: Open-source toolkit for neural machine translation.
  preprint arXiv:1701.02810, 2017.
- [40]

  Zihang Lai, Erika Lu, and Weidi Xie.
  Mast: A memory-augmented self-supervised tracker.
  In CVPR, 2020.
- [41]

  Dong-Hyun Lee et al.
  Pseudo-label: The simple and efficient semi-supervised learning
  method for deep neural networks.
  In Workshop on challenges in representation learning, ICML,
  2013.
- [42]

  Junnan Li, Pan Zhou, Caiming Xiong, and Steven C.H. Hoi.
  Prototypical contrastive learning of unsupervised representations.
  ICLR, 2021.
- [43]

  Ilya Loshchilov and Frank Hutter.
  Sgdr: Stochastic gradient descent with warm restarts.
  preprint arXiv:1608.03983, 2016.
- [44]

  Ilya Loshchilov and Frank Hutter.
  Fixing weight decay regularization in adam.
  2018.
- [45]

  Julien Mairal.
  Cyanure: An open-source toolbox for empirical risk minimization for
  python, c++, and soon more.
  preprint arXiv:1912.08165, 2019.
- [46]

  Maria-Elena Nilsback and Andrew Zisserman.
  Automated flower classification over a large number of classes.
  In 2008 Sixth Indian Conference on Computer Vision, Graphics &
  Image Processing, 2008.
- [47]

  Mehdi Noroozi, Ananth Vinjimoor, Paolo Favaro, and Hamed Pirsiavash.
  Boosting self-supervised learning via knowledge transfer.
  In CVPR, 2018.
- [48]

  Seoung Wug Oh, Joon-Young Lee, Ning Xu, and Seon Joo Kim.
  Video object segmentation using space-time memory networks.
  In ICCV, 2019.
- [49]

  Hieu Pham, Qizhe Xie, Zihang Dai, and Quoc V Le.
  Meta pseudo labels.
  preprint arXiv:2003.10580, 2020.
- [50]

  James Philbin, Ondrej Chum, Michael Isard, Josef Sivic, and Andrew Zisserman.
  Lost in quantization: Improving particular object retrieval in large
  scale image databases.
  In CVPR, 2008.
- [51]

  Boris T Polyak and Anatoli B Juditsky.
  Acceleration of stochastic approximation by averaging.
  SIAM journal on control and optimization, 30(4):838–855, 1992.
- [52]

  Jordi Pont-Tuset, Federico Perazzi, Sergi Caelles, Pablo Arbeláez, Alex
  Sorkine-Hornung, and Luc Van Gool.
  The 2017 davis challenge on video object segmentation.
  preprint arXiv:1704.00675, 2017.
- [53]

  Filip Radenović, Ahmet Iscen, Giorgos Tolias, Yannis Avrithis, and
  Ondřej Chum.
  Revisiting oxford and paris: Large-scale image retrieval
  benchmarking.
  2018.
- [54]

  Filip Radenović, Giorgos Tolias, and Ondřej Chum.
  Fine-tuning cnn image retrieval with no human annotation.
  IEEE transactions on pattern analysis and machine intelligence,
  2018.
- [55]

  Alec Radford, Jeffrey Wu, Rewon Child, David Luan, Dario Amodei, and Ilya
  Sutskever.
  Language models are unsupervised multitask learners.
- [56]

  Ilija Radosavovic, Raj Prateek Kosaraju, Ross Girshick, Kaiming He, and Piotr
  Dollár.
  Designing network design spaces.
  In CVPR, 2020.
- [57]

  Jerome Revaud, Jon Almazán, Rafael S Rezende, and Cesar Roberto de Souza.
  Learning with average precision: Training image retrieval with a
  listwise loss.
  In ICCV, 2019.
- [58]

  Pierre H Richemond, Jean-Bastien Grill, Florent Altché, Corentin Tallec,
  Florian Strub, Andrew Brock, Samuel Smith, Soham De, Razvan Pascanu, Bilal
  Piot, et al.
  Byol works even without batch statistics.
  preprint arXiv:2010.10241, 2020.
- [59]

  David Ruppert.
  Efficient estimations from a slowly convergent robbins-monro process.
  Technical report, 1988.
- [60]

  Olga Russakovsky, Jia Deng, Hao Su, Jonathan Krause, Sanjeev Satheesh, Sean Ma,
  Zhiheng Huang, Andrej Karpathy, Aditya Khosla, Michael Bernstein, Alexander C
  Berg, and Li Fei-Fei.
  Imagenet large scale visual recognition challenge.
  IJCV, 2015.
- [61]

  Tim Salimans and Diederik P Kingma.
  Weight normalization: A simple reparameterization to accelerate
  training of deep neural networks.
  NeurIPS, 2016.
- [62]

  Mert Bulent Sariyildiz, Yannis Kalantidis, Diane Larlus, and Karteek Alahari.
  Concept generalization in visual representation learning.
  arXiv preprint arXiv:2012.05649, 2020.
- [63]

  Zhiqiang Shen, Zechun Liu, Jie Qin, Lei Huang, Kwang-Ting Cheng, and Marios
  Savvides.
  S2-bnn: Bridging the gap between self-supervised real and 1-bit
  neural networks via guided distribution calibration.
  arXiv preprint arXiv:2102.08946, 2021.
- [64]

  Kihyuk Sohn, David Berthelot, Chun-Liang Li, Zizhao Zhang, Nicholas Carlini,
  Ekin D Cubuk, Alex Kurakin, Han Zhang, and Colin Raffel.
  Fixmatch: Simplifying semi-supervised learning with consistency and
  confidence.
  In NeurIPS, 2020.
- [65]

  Antti Tarvainen and Harri Valpola.
  Mean teachers are better role models: Weight-averaged consistency
  targets improve semi-supervised deep learning results.
  preprint arXiv:1703.01780, 2017.
- [66]

  Bart Thomee, David A Shamma, Gerald Friedland, Benjamin Elizalde, Karl Ni,
  Douglas Poland, Damian Borth, and Li-Jia Li.
  Yfcc100m: The new data in multimedia research.
  arXiv preprint arXiv:1503.01817, 2015.
- [67]

  Yonglong Tian, Chen Sun, Ben Poole, Dilip Krishnan, Cordelia Schmid, and
  Phillip Isola.
  What makes for good views for contrastive learning.
  NeurIPS, 2020.
- [68]

  Giorgos Tolias, Ronan Sicre, and Hervé Jégou.
  Particular object retrieval with integral max-pooling of cnn
  activations.
  arXiv preprint arXiv:1511.05879, 2015.
- [69]

  Hugo Touvron, Matthieu Cord, Matthijs Douze, Francisco Massa, Alexandre
  Sablayrolles, and Hervé Jégou.
  Training data-efficient image transformers & distillation through
  attention.
  preprint arXiv:2012.12877, 2020.
- [70]

  Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones,
  Aidan N Gomez, Łukasz Kaiser, and Illia Polosukhin.
  Attention is all you need.
  In NeurIPS, 2017.
- [71]

  Xiaolong Wang, Allan Jabri, and Alexei A Efros.
  Learning correspondence from the cycle-consistency of time.
  In CVPR, 2019.
- [72]

  Tobias Weyand, Andre Araujo, Bingyi Cao, and Jack Sim.
  Google landmarks dataset v2-a large-scale benchmark for
  instance-level recognition and retrieval.
  2020.
- [73]

  Zhirong Wu, Yuanjun Xiong, Stella X Yu, and Dahua Lin.
  Unsupervised feature learning via non-parametric instance
  discrimination.
  In CVPR, 2018.
- [74]

  Junyuan Xie, Ross Girshick, and Ali Farhadi.
  Unsupervised deep embedding for clustering analysis.
  In ICML, 2016.
- [75]

  Qizhe Xie, Zihang Dai Dai, Eduard Hovy, Minh-Thang Luong, and Quoc V. Le.
  Unsupervised data augmentation for consistency training.
  preprint arXiv:1904.12848, 2020.
- [76]

  Qizhe Xie, Minh-Thang Luong, Eduard Hovy, and Quoc V Le.
  Self-training with noisy student improves imagenet classification.
  In CVPR, 2020.
- [77]

  Haohang Xu, Xiaopeng Zhang, Hao Li, Lingxi Xie, Hongkai Xiong, and Qi Tian.
  Seed the views: Hierarchical semantic alignment for contrastive
  representation learning.
  arXiv preprint arXiv:2012.02733, 2021.
- [78]

  Qiantong Xu, Tatiana Likhomanenko, Jacob Kahn, Awni Hannun, Gabriel Synnaeve,
  and Ronan Collobert.
  Iterative pseudo-labeling for speech recognition.
  preprint arXiv:2005.09267, 2020.
- [79]

  I Zeki Yalniz, Hervé Jégou, Kan Chen, Manohar Paluri, and Dhruv
  Mahajan.
  Billion-scale semi-supervised learning for image classification.
  preprint arXiv:1905.00546, 2019.
- [80]

  Jianwei Yang, Devi Parikh, and Dhruv Batra.
  Joint unsupervised learning of deep representations and image
  clusters.
  In CVPR, 2016.
- [81]

  Jure Zbontar, Li Jing, Ishan Misra, Yann LeCun, and Stéphane Deny.
  Barlow twins: Self-supervised learning via redundancy reduction.
  arXiv preprint arXiv:2103.03230, 2021.
- [82]

  Richard Zhang, Phillip Isola, and Alexei A Efros.
  Colorful image colorization.
  In ECCV, 2016.
- [83]

  Hengshuang Zhao, Jiaya Jia, and Vladlen Koltun.
  Exploring self-attention for image recognition.
  In CVPR, 2020.
- [84]

  Bolei Zhou, Agata Lapedriza, Jianxiong Xiao, Antonio Torralba, and Aude Oliva.
  Learning deep features for scene recognition using places database.
  In NeurIPS, 2014.
- [85]

  Chengxu Zhuang, Alex Lin Zhai, and Daniel Yamins.
  Local aggregation for unsupervised learning of visual embeddings.
  In ICCV, 2019.

## Appendix

### A Additional Results

##### kk-NN classification.

In Tab. [10](#Sx1.T10 "Table 10 ‣ 𝑘-NN classification. ‣ A Additional Results ‣ Appendix ‣ Emerging Properties in Self-Supervised Vision Transformers"), we evaluate the frozen representations given by ResNet-50 or ViT-small pre-trained with DINO with two evaluation protocols: linear or kk-NN.
For both evaluations, we extract representations from a pre-trained network without using any data augmentation.
Then, we perform classification either with weighted kk-NN or with a linear regression learned with cyanure library [[16](#as1_bib.bib16)].
In Tab. [10](#Sx1.T10 "Table 10 ‣ 𝑘-NN classification. ‣ A Additional Results ‣ Appendix ‣ Emerging Properties in Self-Supervised Vision Transformers") we see that ViT-S accuracies are better than accuracies obtained with RN50 both with a linear or a kk-NN classifier.
However, the performance gap when using the kk-NN evaluation is much more significant than when considering linear evaluation.
For example on ImageNet 1%, ViT-S outperforms ResNet-50 by a large margin of +14.1%+14.1\% with kk-NN evaluation.
This suggests that transformers architectures trained with DINO might offer more model flexibility that benefits the kk-NN evaluation.
KK-NN classifiers have the great advantage of being fast and light to deploy, without requiring any domain adaptation.
Overall, ViT trained with DINO provides features that combine particularly well with kk-NN classifiers.

Table 10: kk-NN and linear evaluation for ViT-S/16 and ResNet-50 pre-trained with DINO.
We use ImageNet-1k [[21](#as1_bib.bib21)] (“Inet”), Places205 [[29](#as1_bib.bib29)], PASCAL VOC [[11](#as1_bib.bib11)] and Oxford-102 flowers (“FLOWERS”) [[17](#as1_bib.bib17)].
ViT trained with DINO provides features that are particularly kk-NN friendly.

|  | Logistic | | |  | kk-NN | | |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  | RN50 | ViT-S | Δ\Delta |  | RN50 | ViT-S | Δ\Delta |
| Inet 100% | 72.1 | 75.7 | 3.6 |  | 67.5 | 74.5 | 7.0 |
| Inet 10% | 67.8 | 72.2 | 4.4 |  | 59.3 | 69.1 | 9.8 |
| Inet 1% | 55.1 | 64.5 | 9.4 |  | 47.2 | 61.3 | 14.1 |
| Pl. 10% | 53.4 | 52.1 | -1.3 |  | 46.9 | 48.6 | 1.7 |
| Pl. 1% | 46.5 | 46.3 | -0.2 |  | 39.2 | 41.3 | 2.1 |
| VOC07 | 88.9 | 89.2 | 0.3 |  | 84.9 | 88.0 | 3.1 |
| FLOWERS | 95.6 | 96.4 | 0.8 |  | 87.9 | 89.1 | 1.2 |
| Average Δ\Delta |  |  | 2.4 |  |  |  | 5.6 |

Table 11: 
ImageNet classification with different pretraining.
Top-1 accuracy on ImageNet for supervised ViT-B/16 models using different pretrainings or using an additional pretrained convnet to guide the training.
The methods use different image resolution (“res.”) and training procedure (“tr. proc.”), i.e., data augmentation and optimization.
“MPP” is Masked Patch Prediction.

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| Pretraining | |  |  |  |  |
| method | data |  | res. | tr. proc. | Top-1 |
| Pretrain on additional data | | | |  |  |
| MMP | JFT-300M |  | 384 | [[10](#as1_bib.bib10)] | 79.9 |
| Supervised | JFT-300M |  | 384 | [[10](#as1_bib.bib10)] | 84.2 |
| Train with additional model | | | |  |  |
| Rand. init. | - |  | 224 | [[25](#as1_bib.bib25)] | 83.4 |
| No additional data nor model | | | |  |  |
| Rand. init. | - |  | 224 | [[10](#as1_bib.bib10)] | 77.9 |
| Rand. init. | - |  | 224 | [[25](#as1_bib.bib25)] | 81.8 |
| Supervised | ImNet |  | 224 | [[25](#as1_bib.bib25)] | 81.9 |
| DINO | ImNet |  | 224 | [[25](#as1_bib.bib25)] | 82.8 |

##### Self-supervised ImageNet pretraining of ViT.

In this experiment, we study the impact of pretraining a supervised ViT model with our method.
In Tab. [11](#Sx1.T11 "Table 11 ‣ 𝑘-NN classification. ‣ A Additional Results ‣ Appendix ‣ Emerging Properties in Self-Supervised Vision Transformers"), we compare the performance of supervised ViT models that are initialized with different pretraining or guided during training with an additional pretrained convnet.
The first set of models are pretrained with and without supervision on the large curated dataset composed of 300M images.
The second set of models are trained with hard knowledge distillation from a pretrained supervised RegNetY [[56](#bib.bib56)].
The last set of models do not use any additional data nor models, and are initialized either randomly or after a pretraining with DINO on ImageNet.
Compare to random initialization, pretraining with DINO leads to a performance gain of +1%.
This is not caused by a longer training since pretraining with supervision instead of DINO does not improve performance.
Using self-supervised pretraining reduces the gap with models pretrained on extra data or distilled from a convnet.

##### Low-shot learning on ImageNet.

We evaluate the features obtained with DINO applied on ViT-S on low-shot learning.
In Tab. [12](#Sx1.T12 "Table 12 ‣ Low-shot learning on ImageNet. ‣ A Additional Results ‣ Appendix ‣ Emerging Properties in Self-Supervised Vision Transformers"), we report the validation accuracy of a logistic regression trained on frozen features (frozen) with 1% and 10% labels.
The logistic regression is trained with the cyanure library [[16](#as1_bib.bib16)].
When comparing models with a similar number of parameters and image/sec, we observe that our features are on par with state-of-the-art semi-supervised models.
Interestingly, this performance is obtained by training a multi-class logistic regression on *frozen features, without data augmentation nor finetuning*.

Table 12: 
Low-shot learning on ImageNet with frozen ViT features.
We train a logistic regression on frozen features (frozen).
Note that this frozen evaluation is performed *without any finetuning nor data augmentation*.
We report top-1 accuracy.
For reference, we show previously published results that uses finetuning and semi-supervised learning.

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  |  |  | Top 1 | |
| Method | Arch | Param. | 1% | 10% |
| Self-supervised pretraining with finetuning | | | | |
| UDA [[28](#as1_bib.bib28)] | RN50 | 23 | – | 68.1 |
| SimCLRv2 [[5](#as1_bib.bib5)] | RN50 | 23 | 57.9 | 68.4 |
| BYOL [[12](#as1_bib.bib12)] | RN50 | 23 | 53.2 | 68.8 |
| SwAV [[3](#as1_bib.bib3)] | RN50 | 23 | 53.9 | 70.2 |
| SimCLRv2 [[7](#as1_bib.bib7)] | RN50w4 | 375 | 63.0 | 74.4 |
| BYOL [[12](#as1_bib.bib12)] | RN200w2 | 250 | 71.2 | 77.7 |
| Semi-supervised methods | | | | |
| SimCLRv2+KD [[5](#as1_bib.bib5)] | RN50 | 23 | 60.0 | 70.5 |
| SwAV+CT [[1](#as1_bib.bib1)] | RN50 | 23 | – | 70.8 |
| FixMatch [[23](#as1_bib.bib23)] | RN50 | 23 | – | 71.5 |
| MPL [[19](#as1_bib.bib19)] | RN50 | 23 | – | 73.9 |
| SimCLRv2+KD [[5](#as1_bib.bib5)] | RN152w3+SK | 794 | 76.6 | 80.9 |
| Frozen self-supervised features | | | | |
| DINO -frozen | ViT-S/16 | 21 | 64.5 | 72.2 |

|  |  |  |
| --- | --- | --- |
| Refer to caption | Refer to caption | Refer to caption |

Figure 8: 
Self-attention for a set of reference points.
We visualize the self-attention module from the last block of a ViT-S/8 trained with DINO.
The network is able to separate objects, though it has been trained with no supervision at all.

### B Methodology Comparison

We compare the performance of different self-supervised frameworks, MoCo-v2 [[6](#as1_bib.bib6)], SwAV [[3](#as1_bib.bib3)] and BYOL [[12](#as1_bib.bib12)] when using convnet or ViT.
In Tab. [13](#Sx1.T13 "Table 13 ‣ B Methodology Comparison ‣ Appendix ‣ Emerging Properties in Self-Supervised Vision Transformers"), we see that when trained with ResNet-50 (convnet), DINO performs on par with SwAV and BYOL.
However, DINO unravels its potential with ViT, outperforming MoCo-v2, SwAV and BYOL by large margins (+4.3% with linear and +6.2% with k-NN evaluations).
In the rest of this section, we perform ablations to better understand the performance of DINO applied to ViT.
In particular, we provide a detailed comparison with methods that either use a momentum encoder, namely MoCo-v2 and BYOL, and methods that use multi-crop, namely SwAV.

Table 13: 
Methodology comparison for DEIT-small and ResNet-50.
We report ImageNet linear and kk-NN evaluations validation accuracy after 300 epochs pre-training.
All numbers are run by us and match or outperform published results.

|  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- |
|  |  | ResNet-50 | |  | ViT-small | |
| Method |  | Linear | kk-NN |  | Linear | kk-NN |
| MoCo-v2 |  | 71.1 | 62.9 |  | 71.6 | 62.0 |
| BYOL |  | 72.7 | 65.4 |  | 71.4 | 66.6 |
| SwAV |  | 74.1 | 65.4 |  | 71.8 | 64.7 |
| DINO |  | 74.5 | 65.6 |  | 76.1 | 72.8 |

##### Relation to MoCo-v2 and BYOL.

In Tab. [14](#Sx1.T14 "Table 14 ‣ Relation to MoCo-v2 and BYOL. ‣ B Methodology Comparison ‣ Appendix ‣ Emerging Properties in Self-Supervised Vision Transformers"), we present the impact of ablating components that differ between DINO, MoCo-v2 and BYOL: the choice of loss, the predictor in the student head, the centering operation, the batch normalization in the projection heads, and finally, the multi-crop augmentation.
The loss in DINO is a cross-entropy on sharpened softmax outputs (CE) while MoCo-v2 uses the InfoNCE contrastive loss (INCE) and BYOL a mean squared error on l2-normalized outputs (MSE).
No sharpening is applied with the MSE criterion.
Though, DINO surprisingly still works when changing the loss function to MSE, but this significantly alters the performance (see rows (1, 2) and (4, 9)).
We also observe that adding a predictor has little impact (1, 3).
However, in the case of BYOL, the predictor is critical to prevent collapse (7, 8) which is consistent with previous studies [[7](#as1_bib.bib7), [12](#as1_bib.bib12)].
Interestingly, we observe that the teacher output centering avoids collapse without predictor nor batch normalizations in BYOL (7, 9), though with a significant performance drop which can likely be explained by the fact that our centering operator is designed to work in combination with sharpening.
Finally, we observe that multi-crop works particularly well with DINO and MoCo-v2, removing it hurts performance by 2−4%2-4\% (1 versus 4 and, 5 versus 6).
Adding multi-crop to BYOL does not work out-of-the-box (7, 10) as detailed in Appendix [E](#Sx1.SS5 "E Multi-crop ‣ Appendix ‣ Emerging Properties in Self-Supervised Vision Transformers") and further adaptation may be required.

Table 14: 
Relation to MoCo-v2 and BYOL.
We ablate the components that differ between DINO, MoCo-v2 and BYOL: the loss function (cross-entropy, CE, versus InfoNCE, INCE, versus mean-square error, MSE), the multi-crop training, the centering operator, the batch normalization in the projection heads and the student predictor. Models are run for 300 epochs with ViT-S/16. We report top-1 accuracy on ImageNet linear evaluation.

|  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  | Method | Loss | multi-crop | Center. | BN | Pred. | Top-1 |
| 1 | DINO | CE | ✓ | ✓ |  |  | 76.1 |
| 2 | – | MSE | ✓ | ✓ |  |  | 62.4 |
| 3 | – | CE | ✓ | ✓ |  | ✓ | 75.6 |
| 4 | – | CE |  | ✓ |  |  | 72.5 |
| 5 | MoCov2 | INCE |  |  | ✓ |  | 71.4 |
| 6 |  | INCE | ✓ |  | ✓ |  | 73.4 |
| 7 | BYOL | MSE |  |  | ✓ | ✓ | 71.4 |
| 8 | – | MSE |  |  | ✓ |  | 00.1 |
| 9 | – | MSE |  | ✓ |  |  | 52.6 |
| 10 | – | MSE | ✓ |  | ✓ | ✓ | 64.8 |

Table 15: Relation to SwAV.
We vary the operation on the teacher output between centering, a softmax applied over the batch dimension and the Sinkhorn-Knopp algorithm.
We also ablate the Momentum encoder by replacing it with a hard copy of the student with a stop-gradient as in SwAV.
Models are run for 300 epochs with ViT-S/16. We report top-1 accuracy on ImageNet linear evaluation.

|  | Method | Momentum | Operation | Top-1 |
| --- | --- | --- | --- | --- |
| 1 | DINO | ✓ | Centering | 76.1 |
| 2 | – | ✓ | Softmax(batch) | 75.8 |
| 3 | – | ✓ | Sinkhorn-Knopp | 76.0 |
| 4 | – |  | Centering | 00.1 |
| 5 | – |  | Softmax(batch) | 72.2 |
| 6 | SwAV |  | Sinkhorn-Knopp | 71.8 |

##### Relation to SwAV.

In Tab. [15](#Sx1.T15 "Table 15 ‣ Relation to MoCo-v2 and BYOL. ‣ B Methodology Comparison ‣ Appendix ‣ Emerging Properties in Self-Supervised Vision Transformers"), we evaluate the differences between DINO and SwAV: the presence of the momentum encoder and the operation on top of the teacher output.
In absence of the momentum, a copy of the student with a stop-gradient is used.
We consider three operations on the teacher output: Centering, Sinkhorn-Knopp or a Softmax along the batch axis.
The Softmax is similar to a single Sinkhorn-Knopp iteration as detailed in the next paragraph.
First, these ablations show that using a momentum encoder significantly improves the performance for ViT (3 versus 6, and 2 versus 5).
Second, the momentum encoder also avoids collapse when using only centering (row 1).
In the absence of momentum, centering the outputs does not work (4) and more advanced operations are required (5, 6).
Overall, these ablations highlight the importance of the momentum encoder, not only for performance but also to stabilize training, removing the need for normalization beyond centering.

##### Details on the Softmax(batch) variant.

The iterative Sinkhorn-Knopp algorithm [[8](#as1_bib.bib8)] used in SwAV [[3](#as1_bib.bib3)] is implemented simply with the following PyTorch style code.

[⬇](data:text/plain;base64,IyB0YXUgaXMgU2lua2hvcm4gcmVndWxhcml6YXRpb24gcGFyYW0KeCA9IGV4cCh4IC8gdGF1KQpmb3IgXyBpbiByYW5nZShudW1faXRlcnMpOiAjIDEgaXRlciBvZiBTaW5raG9ybgoJIyB0b3RhbCB3ZWlnaHQgcGVyIGRpbWVuc2lvbiAob3IgY2x1c3RlcikKCWMgPSBzdW0oeCwgZGltPTAsIGtlZXBkaW09VHJ1ZSkKCXggLz0gYwoKCSMgdG90YWwgd2VpZ2h0IHBlciBzYW1wbGUKCW4gPSBzdW0oeCwgZGltPTEsIGtlZXBkaW09VHJ1ZSkKCSMgeCBzdW1zIHRvIDEgZm9yIGVhY2ggc2FtcGxlIChhc3NpZ25tZW50KQoJeCAvPSBu)

# tau is Sinkhorn regularization param

x = exp(x / tau)

for _ in range(num_iters): # 1 iter of Sinkhorn

# total weight per dimension (or cluster)

c = sum(x, dim=0, keepdim=True)

x /= c

# total weight per sample

n = sum(x, dim=1, keepdim=True)

# x sums to 1 for each sample (assignment)

x /= n

When performing a single Sinkhorn iteration (num_iters=1) the implementation can be highly simplified into only two lines of code, which is our softmax(batch) variant:

[⬇](data:text/plain;base64,eCAvPSBzdW0oeCwgZGltPTEsIGtlZXBkaW09VHJ1ZSk=)

x /= sum(x, dim=1, keepdim=True)

We have seen in Tab. [15](#Sx1.T15 "Table 15 ‣ Relation to MoCo-v2 and BYOL. ‣ B Methodology Comparison ‣ Appendix ‣ Emerging Properties in Self-Supervised Vision Transformers") that this highly simplified variant of SwAV works competitively with SwAV.
Intuitively, the softmax operation on the batch axis allows to select for each dimension (or “cluster”) its best matches in the batch.

##### Validating our implementation.

We observe in Tab. [13](#Sx1.T13 "Table 13 ‣ B Methodology Comparison ‣ Appendix ‣ Emerging Properties in Self-Supervised Vision Transformers") that our reproduction of BYOL, MoCo-v2, SwAV matches or outperforms the corresponding published numbers with ResNet-50.
Indeed, we obtain 72.7%72.7\% for BYOL while [[12](#as1_bib.bib12)] report 72.5%72.5\% in this 300300-epochs setting.
We obtain 71.1%71.1\% for MoCo after 300300 epochs of training while [[6](#as1_bib.bib6)] report 71.1%71.1\% after 800800 epochs of training.
Our improvement compared to the implementation of [[6](#as1_bib.bib6)] can be explained by the use of a larger projection head (3-layer, use of batch-normalizations and projection dimension of 256256).

##### Relation to other works.

DINO is also related to UIC [[14](#bib.bib14)] that use outputs from the previous epoch as hard pseudo-labels for “unsupervised classification”.
However, we use centering to prevent collapse while UIC resorts to balance sampling techniques as in [[8](#bib.bib8)].
Our work can be interpreted as a soft UIC variant with momentum teacher.

The concurrent work CsMI [[77](#bib.bib77)] also exhibits strong performance with simple k-NN classifiers on ImageNet, even with convnets.
As DINO, CsMI combines a momentum network and multi-crop training, which we have seen are both crucial for good k-NN performance in our experiments with ViTs.
We believe studying this work would help us identifying more precisely the components important for good kk-NN performance and leave this investigation for future work.

### C Projection Head

Similarly to other self-supervised frameworks, using a projection head [[4](#as1_bib.bib4)] improves greatly the accuracy of our method.
The projection head starts with a nn-layer multi-layer perceptron (MLP).
The hidden layers are 2048d and are with gaussian error linear units (GELU) activations.
The last layer of the MLP is without GELU.
Then we apply a ℓ2\ell_{2} normalization and a weight normalized fully connected layer [[7](#as1_bib.bib7), [22](#as1_bib.bib22)] with KK dimensions.
This design is inspired from the projection head with a “prototype layer” used in SwAV [[3](#as1_bib.bib3)].
We do not apply batch normalizations.

##### BN-free system.

Unlike standard convnets, ViT architectures do not use batch normalizations (BN) by default.

| ViT-S, 100 epochs | heads w/o BN | heads w/ BN |
| --- | --- | --- |
| kk-NN top-1 | 69.7 | 68.6 |

Therefore, when applying DINO to ViT we do not use any BN also in the projection heads.
In this table we evaluate the impact of adding BN in the heads.
We observe that adding BN in the projection heads has little impact, showing that BN is not important in our framework.
*Overall, when applying DINO to ViT, we do not use any BN anywhere, making the system entirely BN-free.*
This is a great advantage of DINO + ViT to work at state-of-the-art performance without requiring any BN.
Indeed, training with BN typically slows down trainings considerably, especially when these BN modules need to be synchronized across processes [[13](#as1_bib.bib13), [3](#as1_bib.bib3), [2](#as1_bib.bib2), [12](#as1_bib.bib12)].

Figure 9: 
Projection head design w/ or w/o l2-norm bottleneck.

##### L2-normalization bottleneck in projection head.

We illustrate the design of the projection head with or without l2-normalization bottleneck in Fig. [9](#Sx1.F9 "Figure 9 ‣ BN-free system. ‣ C Projection Head ‣ Appendix ‣ Emerging Properties in Self-Supervised Vision Transformers").

| # proj. head linear layers | 11 | 22 | 33 | 44 |
| --- | --- | --- | --- | --- |
| w/ l2-norm bottleneck | – | 62.2 | 68.0 | 69.3 |
| w/o l2-norm bottleneck | 61.6 | 62.9 | 0.1 | 0.1 |

We evaluate the accuracy of DINO models trained with or without l2-normalization bottleneck and we vary the number of linear layers in the projection head.
With l2 bottleneck, the total number of linear layers is n+1n+1 (nn from the MLP and 11 from the weight normalized layer) while without bottleneck the total number of linear layers is nn in the head.
In this table, we report ImageNet top-1 kk-NN evaluation accuracy after 100 epochs pre-training with ViT-S/16.
The output dimensionality KK is set to 40964096 in this experiment.
We observe that DINO training fails without the l2-normalization bottleneck when increasing the depth of the projection head.
L2-normalization bottleneck stabilizes the training of DINO with deep projection head.
We observe that increasing the depth of the projection head improves accuracy.
Our default is to use a total of 4 linear layers: 3 are in the MLP and one is after the l2 bottleneck.

##### Output dimension.

In this table, we evaluate the effect of varying the output dimensionality KK.

| KK | 1024 | 4096 | 16384 | 65536 | 262144 |
| --- | --- | --- | --- | --- | --- |
| kk-NN top-1 | 67.8 | 69.3 | 69.2 | 69.7 | 69.1 |

We observe that a large output dimensionality improves the performance.
We note that the use of l2-normalization bottleneck permits to use a large output dimension with a moderate increase in the total number of parameters.
Our default is to use KK equals to 65536 and d=256d=256 for the bottleneck.

##### GELU activations.

By default, the activations used in ViT are gaussian error linear units (GELU).

| ViT-S, 100 epochs | heads w/ GELU | heads w/ ReLU |
| --- | --- | --- |
| kk-NN top-1 | 69.7 | 68.9 |

Therefore, for consistency within the architecture, we choose to use GELU also in the projection head.
We evaluate the effect of using ReLU instead of GELU in this table and observe that changing the activation unit to ReLU has relatively little impact.

### D Additional Ablations

We have detailed in the main paper that the combination of centering and sharpening is important to avoid collapse in DINO.
We ablate the hyperparameters for these two operations in the following.
We also study the impact of training length and some design choices for the ViT networks.

##### Online centering.

We study the impact of the smoothing parameters in the update rule for the center cc used in the output of the teacher network.

| mm | 0 | 0.9 | 0.99 | 0.999 |
| --- | --- | --- | --- | --- |
| kk-NN top-1 | 69.1 | 69.7 | 69.4 | 0.1 |

The convergence is robust to a wide range of smoothing, and the model only collapses when the update is too slow, i.e., m=0.999m=0.999.

##### Sharpening.

We enforce sharp targets by tuning the teacher softmax temperature parameter τt\tau_{t}.
In this table, we observe that a temperature lower than 0.060.06 is required to avoid collapse.

| τt\tau_{t} | 00 | 0.020.02 | 0.040.04 | 0.060.06 | 0.080.08 | 0.04→0.070.04\rightarrow 0.07 |
| --- | --- | --- | --- | --- | --- | --- |
| kk-NN top-1 | 43.9 | 66.7 | 69.6 | 68.7 | 0.1 | 69.7 |

When the temperature is higher than 0.060.06, the training loss consistently converges to l​n​(K)ln(K).
However, we have observed that using higher temperature than 0.060.06 does not collapse if we start the training from a smaller value and increase it during the first epochs.
In practice, we use a linear warm-up for τt\tau_{t} from 0.040.04 to 0.070.07 during the first 3030 epochs of training.
Finally, note that τ→0\tau\rightarrow 0 (extreme sharpening) correspond to the argmax operation and leads to one-hot hard distributions.

##### Longer training.

We observe in this table that longer training improves the performance of DINO applied to ViT-Small.

| DINO ViT-S | 100-ep | 300-ep | 800-ep |
| --- | --- | --- | --- |
| kk-NN top-1 | 70.9 | 72.8 | 74.5 |

This observation is consistent with self-supervised results obtained with convolutional architectures [[4](#as1_bib.bib4)].
We note that in our experiments with BYOL on ViT-S, training longer than 300300 epochs has been leading to worse performance compare our 300300 epochs run.
For this reason we report BYOL for 300 epochs in Tab. [2](#S3.T2 "Table 2 ‣ Evaluation protocols. ‣ 3.2 Implementation and evaluation protocols ‣ 3 Approach ‣ Emerging Properties in Self-Supervised Vision Transformers") while SwAV, MoCo-v2 and DINO are trained for 800 epochs.

##### The teacher outperforms the student.

We have shown in Fig. [6](#S5.F6 "Figure 6 ‣ Analyzing the training dynamic. ‣ 5.2 Impact of the choice of Teacher Network ‣ 5 Ablation Study of DINO ‣ Emerging Properties in Self-Supervised Vision Transformers") that the momentum teacher outperforms the student with ViT and we show in this Figure that it is also the case with ResNet-50.

The fact that the teacher continually outperforms the student further encourages the interpretation of DINO as a form of Mean Teacher [[24](#as1_bib.bib24)] self-distillation.
Indeed, as motivated in Tarvainen et al. [[24](#as1_bib.bib24)], weight averaging usually produces a better model than the individual models from each iteration [[20](#as1_bib.bib20)].
By aiming a target obtained with a teacher better than the student, the student’s representations improve.
Consequently, the teacher also improves since it is built directly from the student weights.

##### Self-attention maps from supervised versus self-supervised learning.

We evaluate the masks obtained by thresholding the self-attention maps to keep 80% of the mass.

|  |  |
| --- | --- |
| ViT-S/16 weights |  |
| Random weights | 22.0 |
| Supervised | 27.3 |
| DINO | 45.9 |
| DINO w/o multicrop | 45.1 |
| MoCo-v2 | 46.3 |
| BYOL | 47.8 |
| SwAV | 46.8 |

We compare the Jaccard similarity between the ground truth and these masks on the validation images of PASCAL VOC12 dataset for different ViT-S trained with different frameworks.
The properties that self-attention maps from ViT explicitly contain the scene layout and, in particular, object boundaries is observed across different self-supervised methods.

##### Impact of the number of heads in ViT-S.

We study the impact of the number of heads in ViT-S on the accuracy and throughput (images processed per second at inference time on a singe V100 GPU).

| # heads | dim | dim/head | # params | im/sec | kk-NN |
| --- | --- | --- | --- | --- | --- |
| 6 | 384 | 64 | 21 | 1007 | 72.8 |
| 8 | 384 | 48 | 21 | 971 | 73.1 |
| 12 | 384 | 32 | 21 | 927 | 73.7 |
| 16 | 384 | 24 | 21 | 860 | 73.8 |

We find that increasing the number of heads improves the performance, at the cost of a slighlty worse throughput.
In our paper, all experiments are run with the default model DeiT-S [[25](#as1_bib.bib25)], i.e. with 66 heads only.

### E Multi-crop

In this Appendix, we study a core component of DINO: multi-crop training [[3](#as1_bib.bib3)].

##### Range of scales in multi-crop.

For generating the different views, we use the RandomResizedCrop method from torchvision.transforms module in PyTorch.

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| (0.05, ss), (ss, 1), ss: | 0.08 | 0.16 | 0.24 | 0.32 | 0.48 |
| kk-NN top-1 | 65.6 | 68.0 | 69.7 | 69.8 | 69.5 |

We sample two global views with scale range (s,1)(s,1) before resizing them to 2242224^{2} and 66 local views with scale sampled in the range (0.05,s)(0.05,s) resized to 96296^{2} pixels.
Note that we arbitrarily choose to have non-overlapping scaling range for the global and local views following the original design of SwAV.
However, the ranges could definitely be overlapping and experimenting with finer hyperparameters search could lead to a more optimal setting.
In this table, we vary the parameter ss that controls the range of scales used in multi-crop and find the optimum to be around 0.30.3 in our experiments.
We note that this is higher than the parameter used in SwAV which is of 0.140.14.

##### Multi-crop in different self-supervised frameworks.

We compare different recent self-supervised learning frameworks, namely MoCo-v2 [[6](#as1_bib.bib6)], BYOL [[12](#as1_bib.bib12)] and SwAV [[3](#as1_bib.bib3)] with ViT-S/16 architecture.

| crops | 2×22422\times 224^{2} | |  | 2×2242+6×9622\times 224^{2}+6\times 96^{2} | |
| --- | --- | --- | --- | --- | --- |
| eval | kk-NN | linear |  | kk-NN | linear |
| BYOL | 66.6 | 71.4 |  | 59.8 | 64.8 |
| SwAV | 60.5 | 68.5 |  | 64.7 | 71.8 |
| MoCo-v2 | 62.0 | 71.6 |  | 65.4 | 73.4 |
| DINO | 67.9 | 72.5 |  | 72.7 | 75.9 |

For fair comparisons, all models are pretrained either with two 2242224^{2} crops or with multi-crop [[3](#as1_bib.bib3)] training, i.e. two 2242224^{2} crops and six 96296^{2} crops for each image.
We report kk-NN and linear probing evaluations after 300 epochs of training.
Multi-crop does not benefit all frameworks equally, which has been ignored in benchmarks considering only the two crops setting [[7](#as1_bib.bib7)].
The effectiveness of multi-crop depends on the considered framework, which positions multi-crop as a core component of a model and not a simple “add-ons” that will boost any framework the same way.
Without multi-crop, DINO has better accuracy than other frameworks, though by a moderate margin (1%).
Remarkably, DINO benefits the most from multi-crop training (+3.4%+3.4\% in linear eval).
Interestingly, we also observe that the ranking of the frameworks depends on the evaluation protocol considered.

##### Training BYOL with multi-crop.

When applying multi-crop to BYOL with ViT-S, we observe the transfer performance is higher than the baseline without multi-crop for the first training epochs.

However, the transfer performance growth rate is slowing down and declines after a certain amount of training.
We have performed learning rate, weight decay, multi-crop parameters sweeps for this setting and systematically observe the same pattern.
More precisely, we experiment with {1​e−51e^{-5}, 3​e−53e^{-5}, 1​e−41e^{-4}, 3​e−43e^{-4}, 1​e−31e^{-3}, 3​e−33e^{-3}} for learning rate base values, with {0.020.02, 0.050.05, 0.10.1} for weight decay and with different number of small crops: {2, 4, 6}.
All our runs are performed with synchronized batch normalizations in the heads.
When using a low learning rate, we did not observe the performance break point, i.e. the transfer performance was improving continually during training, but the overall accuracy was low.
We have tried a run with multi-crop training on ResNet-50 where we also observe the same behavior.
Since integrating multi-crop training to BYOL is not the focus of this study we did not push that direction further.
However, we believe this is worth investigating why multi-crop does not combine well with BYOL in our experiments and leave this for future work.

### F Evaluation Protocols

#### F.1 kk-NN classification

Following the setting of Wu *et al*. [[27](#as1_bib.bib27)], we evaluate the quality of features with a simple weighted kk Nearest Neighbor classifier.
We freeze the pretrained model to compute and store the features of the training data of the downstream task.
To classify a test image xx, we compute its representation and compare it against all stored training features TT.
The representation of an image is given by the output [CLS] token: it has dimensionality d=384d=384 for ViT-S and d=768d=768 for ViT-B.
The top kk NN (denoted 𝒩k\mathcal{N}_{k}) are used to make a prediction via weighted voting.
Specifically, the class cc gets a total weight of ∑i∈𝒩kαi​𝟏ci=c\sum_{i\in\mathcal{N}_{k}}\alpha_{i}\mathbf{1}_{c_{i}=c}, where αi\alpha_{i} is a contribution weight.
We use αi=exp⁡(Ti​x/τ)\alpha_{i}=\exp(T_{i}x/\tau) with τ\tau equals to 0.070.07 as in [[27](#as1_bib.bib27)] which we do not tune.
We evaluate different values for kk and find that k=20k=20 is consistently leading to the best accuracy across our runs.
This evaluation protocol does not require hyperparameter tuning, nor data augmentation and can be run with only one pass over the downstream dataset.

#### F.2 Linear classification

Following common practice in self-supervised learning, we evaluate the representation quality with a linear classifier.
The projection head is removed, and we train a supervised linear classifier on top of frozen features.
This linear classifier is trained with SGD and a batch size of 10241024 during 100100 epochs on ImageNet.
We do not apply weight decay.
For each model, we sweep the learning rate value.
During training, we apply only random resizes crops (with default parameters from PyTorch RandomResizedCrop) and horizontal flips as data augmentation.
We report central-crop top-1 accuracy.
When evaluating convnets, the common practice is to perform global average pooling on the final feature map before the linear classifier.
In the following, we describe how we adapt this design when evaluating ViTs.

##### ViT-S representations for linear eval.

Following the *feature-based* evaluations in BERT [[9](#as1_bib.bib9)], we concatenate the [CLS] tokens from the ll last layers.

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| concatenate ll last layers | 11 | 22 | 44 | 66 |
| representation dim | 384 | 768 | 1536 | 2304 |
| ViT-S/16 linear eval | 76.1 | 76.6 | 77.0 | 77.0 |

We experiment with the concatenation of a different number ll of layers and similarly to [[9](#as1_bib.bib9)] we find l=4l=4 to be optimal.

##### ViT-B representations for linear eval.

With ViT-B we did not find that concatenating the representations from the last ll layers to provide any performance gain, and consider the final layer only (l=1l=1).

|  |  |  |
| --- | --- | --- |
| pooling strategy | [CLS] tok. | concatenate [CLS] tok. |
|  | only | and avgpooled patch tok. |
| representation dim | 768 | 1536 |
| ViT-B/16 linear eval | 78.0 | 78.2 |

In this setting, we adapt the pipeline used in convnets with global average pooling on the output patch tokens.
We concatenate these pooled features to the final [CLS] output token.

### G Self-Attention Visualizations

We provide more self-attention visualizations in Fig. [8](#Sx1.F8 "Figure 8 ‣ Low-shot learning on ImageNet. ‣ A Additional Results ‣ Appendix ‣ Emerging Properties in Self-Supervised Vision Transformers") and in Fig. [10](#Sx1.F10 "Figure 10 ‣ H Class Representation ‣ Appendix ‣ Emerging Properties in Self-Supervised Vision Transformers").
The images are randomly selected from COCO validation set, and are not used during training of DINO.
In Fig. [8](#Sx1.F8 "Figure 8 ‣ Low-shot learning on ImageNet. ‣ A Additional Results ‣ Appendix ‣ Emerging Properties in Self-Supervised Vision Transformers"), we show the self-attention from the last layer of a DINO ViT-S/8 for several reference points.

### H Class Representation

As a final visualization, we propose to look at the distribution of ImageNet concepts in the feature space from DINO.
We represent each ImageNet class with the average feature vector for its validation images.
We reduce the dimension of these features to 30 with PCA, and run t-SNE with a perplexity of 20, a learning rate of 200 for 5000 iterations.
We present the resulting class embeddings in Fig. [11](#Sx1.F11 "Figure 11 ‣ H Class Representation ‣ Appendix ‣ Emerging Properties in Self-Supervised Vision Transformers").
Our model recovers structures between classes: similar animal species are grouped together, forming coherent clusters of birds (top) or dogs, and especially terriers (far right).

|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  | DINO | | |  |  | Supervised | | |  |  |  |  |  | DINO | | |  |  | Supervised | | |
| Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |
| Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |
| Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |
| Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |
| Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |
| Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |
| Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |
| Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |
| Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |
| Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |
| Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |
| Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |
| Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |
| Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |
| Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |
| Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |

Figure 10: Self-attention heads from the last layer. We look at the attention map when using the [CLS] token as a query for the different heads in the last layer. Note that the [CLS] token is not attached to any label or supervision.

Figure 11: 
t-SNE visualization of ImageNet classes as represented using DINO.
For each class, we obtain the embedding by taking the average feature for all images of that class in the validation set.

## Supplementary Material for Self-Supervised Learning of Visual Transformers with a Momentum Teacher

|  |
| --- |
| Anonymous ICCV submission |
| Paper ID 7530 |

## Appendix

### A Additional Results

##### kk-NN classification.

In Tab. [1](#as1_Sx1.T1 "Table 1 ‣ 𝑘-NN classification. ‣ A Additional Results ‣ Appendix ‣ Supplementary Material for Self-Supervised Learning of Visual Transformers with a Momentum Teacher ‣ Emerging Properties in Self-Supervised Vision Transformers"), we evaluate the frozen representations given by ResNet-50 or ViT-small pre-trained with DINO with two evaluation protocols: linear or kk-NN.
For both evaluations, we extract representations from a pre-trained network without using any data augmentation.
Then, we perform classification either with weighted kk-NN or with a linear regression learned with cyanure library [[16](#as1_bib.bib16)].
In Tab. [1](#as1_Sx1.T1 "Table 1 ‣ 𝑘-NN classification. ‣ A Additional Results ‣ Appendix ‣ Supplementary Material for Self-Supervised Learning of Visual Transformers with a Momentum Teacher ‣ Emerging Properties in Self-Supervised Vision Transformers") we see that ViT-S accuracies are better than accuracies obtained with RN50 both with a linear or a kk-NN classifier.
However, the performance gap when using the kk-NN evaluation is much more significant than when considering linear evaluation.
For example on ImageNet 1%, ViT-S outperforms ResNet-50 by a large margin of +14.1%+14.1\% with kk-NN evaluation.
This suggests that transformers architectures trained with DINO might offer more model flexibility that benefits the kk-NN evaluation.
KK-NN classifiers have the great advantage of being fast and light to deploy, without requiring any domain adaptation.
Overall, ViT trained with DINO provides features that combine particularly well with kk-NN classifiers.

Table 1: kk-NN and linear evaluation for ViT-S/16 and ResNet-50 pre-trained with DINO.
We use ImageNet-1k [[21](#as1_bib.bib21)] (“Inet”), Places205 [[29](#as1_bib.bib29)], PASCAL VOC [[11](#as1_bib.bib11)] and Oxford-102 flowers (“FLOWERS”) [[17](#as1_bib.bib17)].
ViT trained with DINO provides features that are particularly kk-NN friendly.

|  | Logistic | | |  | kk-NN | | |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  | RN50 | ViT-S | Δ\Delta |  | RN50 | ViT-S | Δ\Delta |
| Inet 100% | 72.1 | 75.7 | 3.6 |  | 67.5 | 74.5 | 7.0 |
| Inet 10% | 67.8 | 72.2 | 4.4 |  | 59.3 | 69.1 | 9.8 |
| Inet 1% | 55.1 | 64.5 | 9.4 |  | 47.2 | 61.3 | 14.1 |
| Pl. 10% | 53.4 | 52.1 | -1.3 |  | 46.9 | 48.6 | 1.7 |
| Pl. 1% | 46.5 | 46.3 | -0.2 |  | 39.2 | 41.3 | 2.1 |
| VOC07 | 88.9 | 89.2 | 0.3 |  | 84.9 | 88.0 | 3.1 |
| FLOWERS | 95.6 | 96.4 | 0.8 |  | 87.9 | 89.1 | 1.2 |
| Average Δ\Delta |  |  | 2.4 |  |  |  | 5.6 |

Table 2: 
ImageNet classification with different pretraining.
Top-1 accuracy on ImageNet for supervised ViT-B/16 models using different pretrainings or using an additional pretrained convnet to guide the training.
The methods use different image resolution (“res.”) and training procedure (“tr. proc.”), i.e., data augmentation and optimization.
“MPP” is Masked Patch Prediction.

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| Pretraining | |  |  |  |  |
| method | data |  | res. | tr. proc. | Top-1 |
| Pretrain on additional data | | | |  |  |
| MMP | JFT-300M |  | 384 | [[10](#as1_bib.bib10)] | 79.9 |
| Supervised | JFT-300M |  | 384 | [[10](#as1_bib.bib10)] | 84.2 |
| Train with additional model | | | |  |  |
| Rand. init. | - |  | 224 | [[25](#as1_bib.bib25)] | 83.4 |
| No additional data nor model | | | |  |  |
| Rand. init. | - |  | 224 | [[10](#as1_bib.bib10)] | 77.9 |
| Rand. init. | - |  | 224 | [[25](#as1_bib.bib25)] | 81.8 |
| Supervised | ImNet |  | 224 | [[25](#as1_bib.bib25)] | 81.9 |
| DINO | ImNet |  | 224 | [[25](#as1_bib.bib25)] | 82.8 |

##### Self-supervised ImageNet pretraining of ViT.

In this experiment, we study the impact of pretraining a supervised ViT model with our method.
In Tab. [2](#as1_Sx1.T2 "Table 2 ‣ 𝑘-NN classification. ‣ A Additional Results ‣ Appendix ‣ Supplementary Material for Self-Supervised Learning of Visual Transformers with a Momentum Teacher ‣ Emerging Properties in Self-Supervised Vision Transformers"), we compare the performance of supervised ViT models that are initialized with different pretraining or guided during training with an additional pretrained convnet.
The first set of models are pretrained with and without supervision on the large curated dataset composed of 300M images.
The second set of models are trained with hard knowledge distillation from a pretrained supervised RegNetY [[56](#bib.bib56)].
The last set of models do not use any additional data nor models, and are initialized either randomly or after a pretraining with DINO on ImageNet.
Compare to random initialization, pretraining with DINO leads to a performance gain of +1%.
This is not caused by a longer training since pretraining with supervision instead of DINO does not improve performance.
Using self-supervised pretraining reduces the gap with models pretrained on extra data or distilled from a convnet.

##### Low-shot learning on ImageNet.

We evaluate the features obtained with DINO applied on ViT-S on low-shot learning.
In Tab. [3](#as1_Sx1.T3 "Table 3 ‣ Low-shot learning on ImageNet. ‣ A Additional Results ‣ Appendix ‣ Supplementary Material for Self-Supervised Learning of Visual Transformers with a Momentum Teacher ‣ Emerging Properties in Self-Supervised Vision Transformers"), we report the validation accuracy of a logistic regression trained on frozen features (frozen) with 1% and 10% labels.
The logistic regression is trained with the cyanure library [[16](#as1_bib.bib16)].
When comparing models with a similar number of parameters and image/sec, we observe that our features are on par with state-of-the-art semi-supervised models.
Interestingly, this performance is obtained by training a multi-class logistic regression on *frozen features, without data augmentation nor finetuning*.

Table 3: 
Low-shot learning on ImageNet with frozen ViT features.
We train a logistic regression on frozen features (frozen).
Note that this frozen evaluation is performed *without any finetuning nor data augmentation*.
We report top-1 accuracy.
For reference, we show previously published results that uses finetuning and semi-supervised learning.

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  |  |  | Top 1 | |
| Method | Arch | Param. | 1% | 10% |
| Self-supervised pretraining with finetuning | | | | |
| UDA [[28](#as1_bib.bib28)] | RN50 | 23 | – | 68.1 |
| SimCLRv2 [[5](#as1_bib.bib5)] | RN50 | 23 | 57.9 | 68.4 |
| BYOL [[12](#as1_bib.bib12)] | RN50 | 23 | 53.2 | 68.8 |
| SwAV [[3](#as1_bib.bib3)] | RN50 | 23 | 53.9 | 70.2 |
| SimCLRv2 [[7](#as1_bib.bib7)] | RN50w4 | 375 | 63.0 | 74.4 |
| BYOL [[12](#as1_bib.bib12)] | RN200w2 | 250 | 71.2 | 77.7 |
| Semi-supervised methods | | | | |
| SimCLRv2+KD [[5](#as1_bib.bib5)] | RN50 | 23 | 60.0 | 70.5 |
| SwAV+CT [[1](#as1_bib.bib1)] | RN50 | 23 | – | 70.8 |
| FixMatch [[23](#as1_bib.bib23)] | RN50 | 23 | – | 71.5 |
| MPL [[19](#as1_bib.bib19)] | RN50 | 23 | – | 73.9 |
| SimCLRv2+KD [[5](#as1_bib.bib5)] | RN152w3+SK | 794 | 76.6 | 80.9 |
| Frozen self-supervised features | | | | |
| DINO -frozen | ViT-S/16 | 21 | 64.5 | 72.2 |

|  |  |  |
| --- | --- | --- |
| Refer to caption | Refer to caption | Refer to caption |

Figure 1: 
Self-attention for a set of reference points.
We visualize the self-attention module from the last block of a ViT-S/8 trained with DINO.
The network is able to separate objects, though it has been trained with no supervision at all.

### B Methodology Comparison

We compare the performance of different self-supervised frameworks, MoCo-v2 [[6](#as1_bib.bib6)], SwAV [[3](#as1_bib.bib3)] and BYOL [[12](#as1_bib.bib12)] when using convnet or ViT.
In Tab. [4](#as1_Sx1.T4 "Table 4 ‣ B Methodology Comparison ‣ Appendix ‣ Supplementary Material for Self-Supervised Learning of Visual Transformers with a Momentum Teacher ‣ Emerging Properties in Self-Supervised Vision Transformers"), we see that when trained with ResNet-50 (convnet), DINO performs on par with SwAV and BYOL.
However, DINO unravels its potential with ViT, outperforming MoCo-v2, SwAV and BYOL by large margins (+4.3% with linear and +6.2% with k-NN evaluations).
In the rest of this section, we perform ablations to better understand the performance of DINO applied to ViT.
In particular, we provide a detailed comparison with methods that either use a momentum encoder, namely MoCo-v2 and BYOL, and methods that use multi-crop, namely SwAV.

Table 4: 
Methodology comparison for DEIT-small and ResNet-50.
We report ImageNet linear and kk-NN evaluations validation accuracy after 300 epochs pre-training.
All numbers are run by us and match or outperform published results.

|  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- |
|  |  | ResNet-50 | |  | ViT-small | |
| Method |  | Linear | kk-NN |  | Linear | kk-NN |
| MoCo-v2 |  | 71.1 | 62.9 |  | 71.6 | 62.0 |
| BYOL |  | 72.7 | 65.4 |  | 71.4 | 66.6 |
| SwAV |  | 74.1 | 65.4 |  | 71.8 | 64.7 |
| DINO |  | 74.5 | 65.6 |  | 76.1 | 72.8 |

##### Relation to MoCo-v2 and BYOL.

In Tab. [5](#as1_Sx1.T5 "Table 5 ‣ Relation to MoCo-v2 and BYOL. ‣ B Methodology Comparison ‣ Appendix ‣ Supplementary Material for Self-Supervised Learning of Visual Transformers with a Momentum Teacher ‣ Emerging Properties in Self-Supervised Vision Transformers"), we present the impact of ablating components that differ between DINO, MoCo-v2 and BYOL: the choice of loss, the predictor in the student head, the centering operation, the batch normalization in the projection heads, and finally, the multi-crop augmentation.
The loss in DINO is a cross-entropy on sharpened softmax outputs (CE) while MoCo-v2 uses the InfoNCE contrastive loss (INCE) and BYOL a mean squared error on l2-normalized outputs (MSE).
No sharpening is applied with the MSE criterion.
Though, DINO surprisingly still works when changing the loss function to MSE, but this significantly alters the performance (see rows (\rownumber1, \rownumber2) and (\rownumber4, \rownumber9)).
We also observe that adding a predictor has little impact (\rownumber1, \rownumber3).
However, in the case of BYOL, the predictor is critical to prevent collapse (\rownumber7, \rownumber8) which is consistent with previous studies [[7](#as1_bib.bib7), [12](#as1_bib.bib12)].
Interestingly, we observe that the teacher output centering avoids collapse without predictor nor batch normalizations in BYOL (\rownumber7, \rownumber9), though with a significant performance drop which can likely be explained by the fact that our centering operator is designed to work in combination with sharpening.
Finally, we observe that multi-crop works particularly well with DINO and MoCo-v2, removing it hurts performance by 2−4%2-4\% (\rownumber1 versus \rownumber4 and, \rownumber5 versus \rownumber6).
Adding multi-crop to BYOL does not work out-of-the-box (\rownumber7, \rownumber10) as detailed in Appendix [E](#as1_Sx1.SS5 "E Multi-crop ‣ Appendix ‣ Supplementary Material for Self-Supervised Learning of Visual Transformers with a Momentum Teacher ‣ Emerging Properties in Self-Supervised Vision Transformers") and further adaptation may be required.

Table 5: 
Relation to MoCo-v2 and BYOL.
We ablate the components that differ between DINO, MoCo-v2 and BYOL: the loss function (cross-entropy, CE, versus InfoNCE, INCE, versus mean-square error, MSE), the multi-crop training, the centering operator, the batch normalization in the projection heads and the student predictor. Models are run for 300 epochs with ViT-S/16. We report top-1 accuracy on ImageNet linear evaluation.

|  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  | Method | Loss | multi-crop | Center. | BN | Pred. | Top-1 |
| \rownumber1 | DINO | CE | ✓ | ✓ |  |  | 76.1 |
| \rownumber2 | – | MSE | ✓ | ✓ |  |  | 62.4 |
| \rownumber3 | – | CE | ✓ | ✓ |  | ✓ | 75.6 |
| \rownumber4 | – | CE |  | ✓ |  |  | 72.5 |
| \rownumber5 | MoCov2 | INCE |  |  | ✓ |  | 71.4 |
| \rownumber6 |  | INCE | ✓ |  | ✓ |  | 73.4 |
| \rownumber7 | BYOL | MSE |  |  | ✓ | ✓ | 71.4 |
| \rownumber8 | – | MSE |  |  | ✓ |  | \pzo0.1 |
| \rownumber9 | – | MSE |  | ✓ |  |  | 52.6 |
| \rownumber10 | – | MSE | ✓ |  | ✓ | ✓ | 64.8 |

Table 6: Relation to SwAV.
We vary the operation on the teacher output between centering, a softmax applied over the batch dimension and the Sinkhorn-Knopp algorithm.
We also ablate the Momentum encoder by replacing it with a hard copy of the student with a stop-gradient as in SwAV.
Models are run for 300 epochs with ViT-S/16. We report top-1 accuracy on ImageNet linear evaluation.

|  | Method | Momentum | Operation | Top-1 |
| --- | --- | --- | --- | --- |
| \rownumber1 | DINO | ✓ | Centering | 76.1 |
| \rownumber2 | – | ✓ | Softmax(batch) | 75.8 |
| \rownumber3 | – | ✓ | Sinkhorn-Knopp | 76.0 |
| \rownumber4 | – |  | Centering | \pzo0.1 |
| \rownumber5 | – |  | Softmax(batch) | 72.2 |
| \rownumber6 | SwAV |  | Sinkhorn-Knopp | 71.8 |

##### Relation to SwAV.

In Tab. [6](#as1_Sx1.T6 "Table 6 ‣ Relation to MoCo-v2 and BYOL. ‣ B Methodology Comparison ‣ Appendix ‣ Supplementary Material for Self-Supervised Learning of Visual Transformers with a Momentum Teacher ‣ Emerging Properties in Self-Supervised Vision Transformers"), we evaluate the differences between DINO and SwAV: the presence of the momentum encoder and the operation on top of the teacher output.
In absence of the momentum, a copy of the student with a stop-gradient is used.
We consider three operations on the teacher output: Centering, Sinkhorn-Knopp or a Softmax along the batch axis.
The Softmax is similar to a single Sinkhorn-Knopp iteration as detailed in the next paragraph.
First, these ablations show that using a momentum encoder significantly improves the performance for ViT (\rownumber3 versus \rownumber6, and \rownumber2 versus \rownumber5).
Second, the momentum encoder also avoids collapse when using only centering (row \rownumber1).
In the absence of momentum, centering the outputs does not work (\rownumber4) and more advanced operations are required (\rownumber5, \rownumber6).
Overall, these ablations highlight the importance of the momentum encoder, not only for performance but also to stabilize training, removing the need for normalization beyond centering.

##### Details on the Softmax(batch) variant.

The iterative Sinkhorn-Knopp algorithm [[8](#as1_bib.bib8)] used in SwAV [[3](#as1_bib.bib3)] is implemented simply with the following PyTorch style code.

[⬇](data:text/plain;base64,IyB0YXUgaXMgU2lua2hvcm4gcmVndWxhcml6YXRpb24gcGFyYW0KeCA9IGV4cCh4IC8gdGF1KQpmb3IgXyBpbiByYW5nZShudW1faXRlcnMpOiAjIDEgaXRlciBvZiBTaW5raG9ybgoJIyB0b3RhbCB3ZWlnaHQgcGVyIGRpbWVuc2lvbiAob3IgY2x1c3RlcikKCWMgPSBzdW0oeCwgZGltPTAsIGtlZXBkaW09VHJ1ZSkKCXggLz0gYwoKCSMgdG90YWwgd2VpZ2h0IHBlciBzYW1wbGUKCW4gPSBzdW0oeCwgZGltPTEsIGtlZXBkaW09VHJ1ZSkKCSMgeCBzdW1zIHRvIDEgZm9yIGVhY2ggc2FtcGxlIChhc3NpZ25tZW50KQoJeCAvPSBu)

# tau is Sinkhorn regularization param

x = exp(x / tau)

for _ in range(num_iters): # 1 iter of Sinkhorn

# total weight per dimension (or cluster)

c = sum(x, dim=0, keepdim=True)

x /= c

# total weight per sample

n = sum(x, dim=1, keepdim=True)

# x sums to 1 for each sample (assignment)

x /= n

When performing a single Sinkhorn iteration (num_iters=1) the implementation can be highly simplified into only two lines of code, which is our softmax(batch) variant:

[⬇](data:text/plain;base64,eCAvPSBzdW0oeCwgZGltPTEsIGtlZXBkaW09VHJ1ZSk=)

x /= sum(x, dim=1, keepdim=True)

We have seen in Tab. [6](#as1_Sx1.T6 "Table 6 ‣ Relation to MoCo-v2 and BYOL. ‣ B Methodology Comparison ‣ Appendix ‣ Supplementary Material for Self-Supervised Learning of Visual Transformers with a Momentum Teacher ‣ Emerging Properties in Self-Supervised Vision Transformers") that this highly simplified variant of SwAV works competitively with SwAV.
Intuitively, the softmax operation on the batch axis allows to select for each dimension (or “cluster”) its best matches in the batch.

##### Validating our implementation.

We observe in Tab. [4](#as1_Sx1.T4 "Table 4 ‣ B Methodology Comparison ‣ Appendix ‣ Supplementary Material for Self-Supervised Learning of Visual Transformers with a Momentum Teacher ‣ Emerging Properties in Self-Supervised Vision Transformers") that our reproduction of BYOL, MoCo-v2, SwAV matches or outperforms the corresponding published numbers with ResNet-50.
Indeed, we obtain 72.7%72.7\% for BYOL while [[12](#as1_bib.bib12)] report 72.5%72.5\% in this 300300-epochs setting.
We obtain 71.1%71.1\% for MoCo after 300300 epochs of training while [[6](#as1_bib.bib6)] report 71.1%71.1\% after 800800 epochs of training.
Our improvement compared to the implementation of [[6](#as1_bib.bib6)] can be explained by the use of a larger projection head (3-layer, use of batch-normalizations and projection dimension of 256256).

##### Relation to other works.

DINO is also related to UIC [[14](#bib.bib14)] that use outputs from the previous epoch as hard pseudo-labels for “unsupervised classification”.
However, we use centering to prevent collapse while UIC resorts to balance sampling techniques as in [[8](#bib.bib8)].
Our work can be interpreted as a soft UIC variant with momentum teacher.

The concurrent work CsMI [[77](#bib.bib77)] also exhibits strong performance with simple k-NN classifiers on ImageNet, even with convnets.
As DINO, CsMI combines a momentum network and multi-crop training, which we have seen are both crucial for good k-NN performance in our experiments with ViTs.
We believe studying this work would help us identifying more precisely the components important for good kk-NN performance and leave this investigation for future work.

### C Projection Head

Similarly to other self-supervised frameworks, using a projection head [[4](#as1_bib.bib4)] improves greatly the accuracy of our method.
The projection head starts with a nn-layer multi-layer perceptron (MLP).
The hidden layers are 2048d and are with gaussian error linear units (GELU) activations.
The last layer of the MLP is without GELU.
Then we apply a ℓ2\ell_{2} normalization and a weight normalized fully connected layer [[7](#as1_bib.bib7), [22](#as1_bib.bib22)] with KK dimensions.
This design is inspired from the projection head with a “prototype layer” used in SwAV [[3](#as1_bib.bib3)].
We do not apply batch normalizations.

##### BN-free system.

Unlike standard convnets, ViT architectures do not use batch normalizations (BN) by default.

| ViT-S, 100 epochs | heads w/o BN | heads w/ BN |
| --- | --- | --- |
| kk-NN top-1 | 69.7 | 68.6 |

Therefore, when applying DINO to ViT we do not use any BN also in the projection heads.
In this table we evaluate the impact of adding BN in the heads.
We observe that adding BN in the projection heads has little impact, showing that BN is not important in our framework.
*Overall, when applying DINO to ViT, we do not use any BN anywhere, making the system entirely BN-free.*
This is a great advantage of DINO + ViT to work at state-of-the-art performance without requiring any BN.
Indeed, training with BN typically slows down trainings considerably, especially when these BN modules need to be synchronized across processes [[13](#as1_bib.bib13), [3](#as1_bib.bib3), [2](#as1_bib.bib2), [12](#as1_bib.bib12)].

Figure 2: 
Projection head design w/ or w/o l2-norm bottleneck.

##### L2-normalization bottleneck in projection head.

We illustrate the design of the projection head with or without l2-normalization bottleneck in Fig. [2](#as1_Sx1.F2 "Figure 2 ‣ BN-free system. ‣ C Projection Head ‣ Appendix ‣ Supplementary Material for Self-Supervised Learning of Visual Transformers with a Momentum Teacher ‣ Emerging Properties in Self-Supervised Vision Transformers").

| # proj. head linear layers | 11 | 22 | 33 | 44 |
| --- | --- | --- | --- | --- |
| w/ l2-norm bottleneck | – | 62.2 | 68.0 | 69.3 |
| w/o l2-norm bottleneck | 61.6 | 62.9 | 0.1 | 0.1 |

We evaluate the accuracy of DINO models trained with or without l2-normalization bottleneck and we vary the number of linear layers in the projection head.
With l2 bottleneck, the total number of linear layers is n+1n+1 (nn from the MLP and 11 from the weight normalized layer) while without bottleneck the total number of linear layers is nn in the head.
In this table, we report ImageNet top-1 kk-NN evaluation accuracy after 100 epochs pre-training with ViT-S/16.
The output dimensionality KK is set to 40964096 in this experiment.
We observe that DINO training fails without the l2-normalization bottleneck when increasing the depth of the projection head.
L2-normalization bottleneck stabilizes the training of DINO with deep projection head.
We observe that increasing the depth of the projection head improves accuracy.
Our default is to use a total of 4 linear layers: 3 are in the MLP and one is after the l2 bottleneck.

##### Output dimension.

In this table, we evaluate the effect of varying the output dimensionality KK.

| KK | 1024 | 4096 | 16384 | 65536 | 262144 |
| --- | --- | --- | --- | --- | --- |
| kk-NN top-1 | 67.8 | 69.3 | 69.2 | 69.7 | 69.1 |

We observe that a large output dimensionality improves the performance.
We note that the use of l2-normalization bottleneck permits to use a large output dimension with a moderate increase in the total number of parameters.
Our default is to use KK equals to 65536 and d=256d=256 for the bottleneck.

##### GELU activations.

By default, the activations used in ViT are gaussian error linear units (GELU).

| ViT-S, 100 epochs | heads w/ GELU | heads w/ ReLU |
| --- | --- | --- |
| kk-NN top-1 | 69.7 | 68.9 |

Therefore, for consistency within the architecture, we choose to use GELU also in the projection head.
We evaluate the effect of using ReLU instead of GELU in this table and observe that changing the activation unit to ReLU has relatively little impact.

### D Additional Ablations

We have detailed in the main paper that the combination of centering and sharpening is important to avoid collapse in DINO.
We ablate the hyperparameters for these two operations in the following.
We also study the impact of training length and some design choices for the ViT networks.

##### Online centering.

We study the impact of the smoothing parameters in the update rule for the center cc used in the output of the teacher network.

| mm | 0 | 0.9 | 0.99 | 0.999 |
| --- | --- | --- | --- | --- |
| kk-NN top-1 | 69.1 | 69.7 | 69.4 | 0.1 |

The convergence is robust to a wide range of smoothing, and the model only collapses when the update is too slow, i.e., m=0.999m=0.999.

##### Sharpening.

We enforce sharp targets by tuning the teacher softmax temperature parameter τt\tau_{t}.
In this table, we observe that a temperature lower than 0.060.06 is required to avoid collapse.

| τt\tau_{t} | 00 | 0.020.02 | 0.040.04 | 0.060.06 | 0.080.08 | 0.04→0.070.04\rightarrow 0.07 |
| --- | --- | --- | --- | --- | --- | --- |
| kk-NN top-1 | 43.9 | 66.7 | 69.6 | 68.7 | 0.1 | 69.7 |

When the temperature is higher than 0.060.06, the training loss consistently converges to l​n​(K)ln(K).
However, we have observed that using higher temperature than 0.060.06 does not collapse if we start the training from a smaller value and increase it during the first epochs.
In practice, we use a linear warm-up for τt\tau_{t} from 0.040.04 to 0.070.07 during the first 3030 epochs of training.
Finally, note that τ→0\tau\rightarrow 0 (extreme sharpening) correspond to the argmax operation and leads to one-hot hard distributions.

##### Longer training.

We observe in this table that longer training improves the performance of DINO applied to ViT-Small.

| DINO ViT-S | 100-ep | 300-ep | 800-ep |
| --- | --- | --- | --- |
| kk-NN top-1 | 70.9 | 72.8 | 74.5 |

This observation is consistent with self-supervised results obtained with convolutional architectures [[4](#as1_bib.bib4)].
We note that in our experiments with BYOL on ViT-S, training longer than 300300 epochs has been leading to worse performance compare our 300300 epochs run.
For this reason we report BYOL for 300 epochs in Tab.  while SwAV, MoCo-v2 and DINO are trained for 800 epochs.

##### The teacher outperforms the student.

We have shown in Fig.  that the momentum teacher outperforms the student with ViT and we show in this Figure that it is also the case with ResNet-50.

The fact that the teacher continually outperforms the student further encourages the interpretation of DINO as a form of Mean Teacher [[24](#as1_bib.bib24)] self-distillation.
Indeed, as motivated in Tarvainen et al. [[24](#as1_bib.bib24)], weight averaging usually produces a better model than the individual models from each iteration [[20](#as1_bib.bib20)].
By aiming a target obtained with a teacher better than the student, the student’s representations improve.
Consequently, the teacher also improves since it is built directly from the student weights.

##### Self-attention maps from supervised versus self-supervised learning.

We evaluate the masks obtained by thresholding the self-attention maps to keep 80% of the mass.

|  |  |
| --- | --- |
| ViT-S/16 weights |  |
| Random weights | 22.0 |
| Supervised | 27.3 |
| DINO | 45.9 |
| DINO w/o multicrop | 45.1 |
| MoCo-v2 | 46.3 |
| BYOL | 47.8 |
| SwAV | 46.8 |

We compare the Jaccard similarity between the ground truth and these masks on the validation images of PASCAL VOC12 dataset for different ViT-S trained with different frameworks.
The properties that self-attention maps from ViT explicitly contain the scene layout and, in particular, object boundaries is observed across different self-supervised methods.

##### Impact of the number of heads in ViT-S.

We study the impact of the number of heads in ViT-S on the accuracy and throughput (images processed per second at inference time on a singe V100 GPU).

| # heads | dim | dim/head | # params | im/sec | kk-NN |
| --- | --- | --- | --- | --- | --- |
| 6 | 384 | 64 | 21 | 1007 | 72.8 |
| 8 | 384 | 48 | 21 | 971 | 73.1 |
| 12 | 384 | 32 | 21 | 927 | 73.7 |
| 16 | 384 | 24 | 21 | 860 | 73.8 |

We find that increasing the number of heads improves the performance, at the cost of a slighlty worse throughput.
In our paper, all experiments are run with the default model DeiT-S [[25](#as1_bib.bib25)], i.e. with 66 heads only.

### E Multi-crop

In this Appendix, we study a core component of DINO: multi-crop training [[3](#as1_bib.bib3)].

##### Range of scales in multi-crop.

For generating the different views, we use the RandomResizedCrop method from torchvision.transforms module in PyTorch.

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| (0.05, ss), (ss, 1), ss: | 0.08 | 0.16 | 0.24 | 0.32 | 0.48 |
| kk-NN top-1 | 65.6 | 68.0 | 69.7 | 69.8 | 69.5 |

We sample two global views with scale range (s,1)(s,1) before resizing them to 2242224^{2} and 66 local views with scale sampled in the range (0.05,s)(0.05,s) resized to 96296^{2} pixels.
Note that we arbitrarily choose to have non-overlapping scaling range for the global and local views following the original design of SwAV.
However, the ranges could definitely be overlapping and experimenting with finer hyperparameters search could lead to a more optimal setting.
In this table, we vary the parameter ss that controls the range of scales used in multi-crop and find the optimum to be around 0.30.3 in our experiments.
We note that this is higher than the parameter used in SwAV which is of 0.140.14.

##### Multi-crop in different self-supervised frameworks.

We compare different recent self-supervised learning frameworks, namely MoCo-v2 [[6](#as1_bib.bib6)], BYOL [[12](#as1_bib.bib12)] and SwAV [[3](#as1_bib.bib3)] with ViT-S/16 architecture.

| crops | 2×22422\times 224^{2} | |  | 2×2242+6×9622\times 224^{2}+6\times 96^{2} | |
| --- | --- | --- | --- | --- | --- |
| eval | kk-NN | linear |  | kk-NN | linear |
| BYOL | 66.6 | 71.4 |  | 59.8 | 64.8 |
| SwAV | 60.5 | 68.5 |  | 64.7 | 71.8 |
| MoCo-v2 | 62.0 | 71.6 |  | 65.4 | 73.4 |
| DINO | 67.9 | 72.5 |  | 72.7 | 75.9 |

For fair comparisons, all models are pretrained either with two 2242224^{2} crops or with multi-crop [[3](#as1_bib.bib3)] training, i.e. two 2242224^{2} crops and six 96296^{2} crops for each image.
We report kk-NN and linear probing evaluations after 300 epochs of training.
Multi-crop does not benefit all frameworks equally, which has been ignored in benchmarks considering only the two crops setting [[7](#as1_bib.bib7)].
The effectiveness of multi-crop depends on the considered framework, which positions multi-crop as a core component of a model and not a simple “add-ons” that will boost any framework the same way.
Without multi-crop, DINO has better accuracy than other frameworks, though by a moderate margin (1%).
Remarkably, DINO benefits the most from multi-crop training (+3.4%+3.4\% in linear eval).
Interestingly, we also observe that the ranking of the frameworks depends on the evaluation protocol considered.

##### Training BYOL with multi-crop.

When applying multi-crop to BYOL with ViT-S, we observe the transfer performance is higher than the baseline without multi-crop for the first training epochs.

However, the transfer performance growth rate is slowing down and declines after a certain amount of training.
We have performed learning rate, weight decay, multi-crop parameters sweeps for this setting and systematically observe the same pattern.
More precisely, we experiment with {1​e−51e^{-5}, 3​e−53e^{-5}, 1​e−41e^{-4}, 3​e−43e^{-4}, 1​e−31e^{-3}, 3​e−33e^{-3}} for learning rate base values, with {0.020.02, 0.050.05, 0.10.1} for weight decay and with different number of small crops: {2, 4, 6}.
All our runs are performed with synchronized batch normalizations in the heads.
When using a low learning rate, we did not observe the performance break point, i.e. the transfer performance was improving continually during training, but the overall accuracy was low.
We have tried a run with multi-crop training on ResNet-50 where we also observe the same behavior.
Since integrating multi-crop training to BYOL is not the focus of this study we did not push that direction further.
However, we believe this is worth investigating why multi-crop does not combine well with BYOL in our experiments and leave this for future work.

### F Evaluation Protocols

#### F.1 kk-NN classification

Following the setting of Wu *et al*. [[27](#as1_bib.bib27)], we evaluate the quality of features with a simple weighted kk Nearest Neighbor classifier.
We freeze the pretrained model to compute and store the features of the training data of the downstream task.
To classify a test image xx, we compute its representation and compare it against all stored training features TT.
The representation of an image is given by the output [CLS] token: it has dimensionality d=384d=384 for ViT-S and d=768d=768 for ViT-B.
The top kk NN (denoted 𝒩k\mathcal{N}_{k}) are used to make a prediction via weighted voting.
Specifically, the class cc gets a total weight of ∑i∈𝒩kαi​𝟏ci=c\sum_{i\in\mathcal{N}_{k}}\alpha_{i}\mathbf{1}_{c_{i}=c}, where αi\alpha_{i} is a contribution weight.
We use αi=exp⁡(Ti​x/τ)\alpha_{i}=\exp(T_{i}x/\tau) with τ\tau equals to 0.070.07 as in [[27](#as1_bib.bib27)] which we do not tune.
We evaluate different values for kk and find that k=20k=20 is consistently leading to the best accuracy across our runs.
This evaluation protocol does not require hyperparameter tuning, nor data augmentation and can be run with only one pass over the downstream dataset.

#### F.2 Linear classification

Following common practice in self-supervised learning, we evaluate the representation quality with a linear classifier.
The projection head is removed, and we train a supervised linear classifier on top of frozen features.
This linear classifier is trained with SGD and a batch size of 10241024 during 100100 epochs on ImageNet.
We do not apply weight decay.
For each model, we sweep the learning rate value.
During training, we apply only random resizes crops (with default parameters from PyTorch RandomResizedCrop) and horizontal flips as data augmentation.
We report central-crop top-1 accuracy.
When evaluating convnets, the common practice is to perform global average pooling on the final feature map before the linear classifier.
In the following, we describe how we adapt this design when evaluating ViTs.

##### ViT-S representations for linear eval.

Following the *feature-based* evaluations in BERT [[9](#as1_bib.bib9)], we concatenate the [CLS] tokens from the ll last layers.

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| concatenate ll last layers | 11 | 22 | 44 | 66 |
| representation dim | 384 | 768 | 1536 | 2304 |
| ViT-S/16 linear eval | 76.1 | 76.6 | 77.0 | 77.0 |

We experiment with the concatenation of a different number ll of layers and similarly to [[9](#as1_bib.bib9)] we find l=4l=4 to be optimal.

##### ViT-B representations for linear eval.

With ViT-B we did not find that concatenating the representations from the last ll layers to provide any performance gain, and consider the final layer only (l=1l=1).

|  |  |  |
| --- | --- | --- |
| pooling strategy | [CLS] tok. | concatenate [CLS] tok. |
|  | only | and avgpooled patch tok. |
| representation dim | 768 | 1536 |
| ViT-B/16 linear eval | 78.0 | 78.2 |

In this setting, we adapt the pipeline used in convnets with global average pooling on the output patch tokens.
We concatenate these pooled features to the final [CLS] output token.

### G Self-Attention Visualizations

We provide more self-attention visualizations in Fig. [1](#as1_Sx1.F1 "Figure 1 ‣ Low-shot learning on ImageNet. ‣ A Additional Results ‣ Appendix ‣ Supplementary Material for Self-Supervised Learning of Visual Transformers with a Momentum Teacher ‣ Emerging Properties in Self-Supervised Vision Transformers") and in Fig. [3](#as1_Sx1.F3 "Figure 3 ‣ H Class Representation ‣ Appendix ‣ Supplementary Material for Self-Supervised Learning of Visual Transformers with a Momentum Teacher ‣ Emerging Properties in Self-Supervised Vision Transformers").
The images are randomly selected from COCO validation set, and are not used during training of DINO.
In Fig. [1](#as1_Sx1.F1 "Figure 1 ‣ Low-shot learning on ImageNet. ‣ A Additional Results ‣ Appendix ‣ Supplementary Material for Self-Supervised Learning of Visual Transformers with a Momentum Teacher ‣ Emerging Properties in Self-Supervised Vision Transformers"), we show the self-attention from the last layer of a DINO ViT-S/8 for several reference points.

### H Class Representation

As a final visualization, we propose to look at the distribution of ImageNet concepts in the feature space from DINO.
We represent each ImageNet class with the average feature vector for its validation images.
We reduce the dimension of these features to 30 with PCA, and run t-SNE with a perplexity of 20, a learning rate of 200 for 5000 iterations.
We present the resulting class embeddings in Fig. [4](#as1_Sx1.F4 "Figure 4 ‣ H Class Representation ‣ Appendix ‣ Supplementary Material for Self-Supervised Learning of Visual Transformers with a Momentum Teacher ‣ Emerging Properties in Self-Supervised Vision Transformers").
Our model recovers structures between classes: similar animal species are grouped together, forming coherent clusters of birds (top) or dogs, and especially terriers (far right).

|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  | DINO | | |  |  | Supervised | | |  |  |  |  |  | DINO | | |  |  | Supervised | | |
| Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |
| Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |
| Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |
| Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |
| Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |
| Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |
| Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |
| Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |
| Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |
| Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |
| Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |
| Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |
| Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |
| Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |
| Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |
| Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |  |  | Refer to caption | Refer to caption | Refer to caption |

Figure 3: Self-attention heads from the last layer. We look at the attention map when using the [CLS] token as a query for the different heads in the last layer. Note that the [CLS] token is not attached to any label or supervision.

Figure 4: 
t-SNE visualization of ImageNet classes as represented using DINO.
For each class, we obtain the embedding by taking the average feature for all images of that class in the validation set.

## References

- [1]

  Mahmoud Assran, Nicolas Ballas, Lluis Castrejon, and Michael Rabbat.
  Recovering petaflops in contrastive semi-supervised learning of
  visual representations.
  arXiv preprint arXiv:2006.10803, 2020.
- [2]

  Mathilde Caron, Piotr Bojanowski, Julien Mairal, and Armand Joulin.
  Unsupervised pre-training of image features on non-curated data.
  In Proceedings of the International Conference on Computer
  Vision (ICCV), 2019.
- [3]

  Mathilde Caron, Ishan Misra, Julien Mairal, Priya Goyal, Piotr Bojanowski, and
  Armand Joulin.
  Unsupervised learning of visual features by contrasting cluster
  assignments.
  In Proceedings of Advances in Neural Information Processing
  Systems (NeurIPS), 2020.
- [4]

  Ting Chen, Simon Kornblith, Mohammad Norouzi, and Geoffrey Hinton.
  A simple framework for contrastive learning of visual
  representations.
  arXiv preprint arXiv:2002.05709, 2020.
- [5]

  Ting Chen, Simon Kornblith, Kevin Swersky, Mohammad Norouzi, and Geoffrey
  Hinton.
  Big self-supervised models are strong semi-supervised learners.
  In Proceedings of Advances in Neural Information Processing
  Systems (NeurIPS), 2020.
- [6]

  Xinlei Chen, Haoqi Fan, Ross Girshick, and Kaiming He.
  Improved baselines with momentum contrastive learning.
  arXiv preprint arXiv:2003.04297, 2020.
- [7]

  Xinlei Chen and Kaiming He.
  Exploring simple siamese representation learning.
  arXiv preprint arXiv:2011.10566, 2020.
- [8]

  Marco Cuturi.
  Sinkhorn distances: Lightspeed computation of optimal transport.
  In Proceedings of Advances in Neural Information Processing
  Systems (NeurIPS), 2013.
- [9]

  Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova.
  Bert: Pre-training of deep bidirectional transformers for language
  understanding.
  arXiv preprint arXiv:1810.04805, 2018.
- [10]

  Alexey Dosovitskiy, Lucas Beyer, Alexander Kolesnikov, Dirk Weissenborn,
  Xiaohua Zhai, Thomas Unterthiner, Mostafa Dehghani, Matthias Minderer, Georg
  Heigold, Sylvain Gelly, et al.
  An image is worth 16x16 words: Transformers for image recognition at
  scale.
  arXiv preprint arXiv:2010.11929, 2020.
- [11]

  Mark Everingham, Luc Van Gool, Christopher KI Williams, John Winn, and Andrew
  Zisserman.
  The pascal visual object classes (voc) challenge.
  International Journal of Computer Vision (IJCV), 2010.
- [12]

  Jean-Bastien Grill, Florian Strub, Florent Altché, Corentin Tallec,
  Pierre H Richemond, Elena Buchatskaya, Carl Doersch, Bernardo Avila Pires,
  Zhaohan Daniel Guo, Mohammad Gheshlaghi Azar, et al.
  Bootstrap your own latent: A new approach to self-supervised
  learning.
  In Proceedings of Advances in Neural Information Processing
  Systems (NeurIPS), 2020.
- [13]

  Kaiming He, Haoqi Fan, Yuxin Wu, Saining Xie, and Ross Girshick.
  Momentum contrast for unsupervised visual representation learning.
  In Proceedings of the Conference on Computer Vision and Pattern
  Recognition (CVPR), 2020.
- [14]

  Allan Jabri, Andrew Owens, and Alexei A Efros.
  Space-time correspondence as a contrastive random walk.
  2020.
- [15]

  Zihang Lai, Erika Lu, and Weidi Xie.
  Mast: A memory-augmented self-supervised tracker.
  In Proceedings of the IEEE/CVF Conference on Computer Vision and
  Pattern Recognition, pages 6479–6488, 2020.
- [16]

  Julien Mairal.
  Cyanure: An open-source toolbox for empirical risk minimization for
  python, c++, and soon more.
  arXiv preprint arXiv:1912.08165, 2019.
- [17]

  Maria-Elena Nilsback and Andrew Zisserman.
  Automated flower classification over a large number of classes.
  In 2008 Sixth Indian Conference on Computer Vision, Graphics &
  Image Processing, 2008.
- [18]

  Seoung Wug Oh, Joon-Young Lee, Ning Xu, and Seon Joo Kim.
  Video object segmentation using space-time memory networks.
  In Proceedings of the IEEE/CVF International Conference on
  Computer Vision, pages 9226–9235, 2019.
- [19]

  Hieu Pham, Qizhe Xie, Zihang Dai, and Quoc V Le.
  Meta pseudo labels.
  arXiv preprint arXiv:2003.10580, 2020.
- [20]

  Boris T Polyak and Anatoli B Juditsky.
  Acceleration of stochastic approximation by averaging.
  SIAM journal on control and optimization, 30(4):838–855, 1992.
- [21]

  Olga Russakovsky, Jia Deng, Hao Su, Jonathan Krause, Sanjeev Satheesh, Sean Ma,
  Zhiheng Huang, Andrej Karpathy, Aditya Khosla, Michael Bernstein, Alexander C
  Berg, and Li Fei-Fei.
  Imagenet large scale visual recognition challenge.
  International Journal of Computer Vision (IJCV), 2015.
- [22]

  Tim Salimans and Diederik P Kingma.
  Weight normalization: A simple reparameterization to accelerate
  training of deep neural networks.
  Proceedings of Advances in Neural Information Processing Systems
  (NeurIPS), 2016.
- [23]

  Kihyuk Sohn, David Berthelot, Chun-Liang Li, Zizhao Zhang, Nicholas Carlini,
  Ekin D Cubuk, Alex Kurakin, Han Zhang, and Colin Raffel.
  Fixmatch: Simplifying semi-supervised learning with consistency and
  confidence.
  In Proceedings of Advances in Neural Information Processing
  Systems (NeurIPS), 2020.
- [24]

  Antti Tarvainen and Harri Valpola.
  Mean teachers are better role models: Weight-averaged consistency
  targets improve semi-supervised deep learning results.
  arXiv preprint arXiv:1703.01780, 2017.
- [25]

  Hugo Touvron, Matthieu Cord, Matthijs Douze, Francisco Massa, Alexandre
  Sablayrolles, and Hervé Jégou.
  Training data-efficient image transformers & distillation through
  attention.
  arXiv preprint arXiv:2012.12877, 2020.
- [26]

  Xiaolong Wang, Allan Jabri, and Alexei A Efros.
  Learning correspondence from the cycle-consistency of time.
  In Proceedings of the IEEE/CVF Conference on Computer Vision and
  Pattern Recognition, pages 2566–2576, 2019.
- [27]

  Zhirong Wu, Yuanjun Xiong, Stella X Yu, and Dahua Lin.
  Unsupervised feature learning via non-parametric instance
  discrimination.
  In Proceedings of the Conference on Computer Vision and Pattern
  Recognition (CVPR), 2018.
- [28]

  Qizhe Xie, Zihang Dai Dai, Eduard Hovy, Minh-Thang Luong, and Quoc V. Le.
  Unsupervised data augmentation for consistency training.
  arXiv preprint arXiv:1904.12848, 2020.
- [29]

  Bolei Zhou, Agata Lapedriza, Jianxiong Xiao, Antonio Torralba, and Aude Oliva.
  Learning deep features for scene recognition using places database.
  In Proceedings of Advances in Neural Information Processing
  Systems (NeurIPS), 2014.
