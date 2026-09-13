---
title: "Semi-Adversarial Nets for Face Images"
source: https://sebastianraschka.com/blog/2018/semi-adversarial-nets-1.html
crawled: 2026-09-06
---

# Semi-Adversarial Nets for Face Images

I thought that it would be nice to have short and concise summaries of recent projects handy, to share them with a more general audience, including colleagues and students. So, I challenged myself to use fewer than 1000 words without getting distracted by the nitty-gritty details and technical jargon.

In this post, I mainly cover some of my recent research in collaboration with the [iPRoBe Lab](http://iprobe.cse.msu.edu) that falls under the broad category of developing approaches to hide specific information in face images. The research discussed in this post is about “maximizing privacy while preserving utility” (goals that are somewhat similar to the ones in [differential privacy](https://en.wikipedia.org/wiki/Differential_Privacy) research).

If you are interested in the research described here, you can find more detailed information in the following two papers:

- “[Semi-Adversarial Networks: Convolutional Autoencoders for Imparting Privacy to Face Images](https://ieeexplore.ieee.org/document/8411207/)” (ICB 2018, preprint: <https://arxiv.org/abs/1712.00321>)
- “Gender Privacy: An Ensemble of Semi Adversarial Networks for Confounding Arbitrary Gender Classifiers” (BTAS 2018; preprint: <https://arxiv.org/abs/1807.11936>)

## Improving Privacy while Preserving Utility

We can think of the research problem we were tackling more generally as a constrained optimization problem: We wanted to hide specific information in face images while preserving their biometric utility. More specifically, we formulated the following three goals:

1. Perturbing gender information
2. Ensuring realistic face images
3. Retaining biometric face recognition\* utility

*\*Biometric face recognition* can be grouped into two related subtasks, identification (A) and verification (B):

![Semi adversarial nets 1 biometric id](https://sebastianraschka.com/images/blog/2018/semi-adversarial-nets-1/biometric-id.webp)

Here, “perturbation” of gender information means that a given gender classifier is no longer be able to make reliable predictions about a person’s gender. One could of think of many reasons why preventing the automated extraction of personal attributes is desirable. Here are three typical examples:

1. Gender-based profiling
2. Identity theft (by combining data from various publicly available sources)
3. Violation of ethics by extracting data without users’ consent

The issues mentioned above could occur whenever face images are captured, uploaded, and stored in central databases. As a counter-measure, systems (for example, supermarket or surveillance cameras) could be equipped with gender-perturbing technology before selling it to third parties, making it harder for end-users to violate users’ privacy and prevent collecting data for unapproved purposes. For instance, hiding information in face image databases could also help ensure compliance with [GDPR guidelines](https://www.eugdpr.org).

## The General Utility of Semi-Adversarial Nets

Of course, we can easily hide gender information by merely adding noise to an image or scrambling the images to a certain degree. However, we have to keep in mind that substantial alterations to an image are also likely rendering any utility of the face image useless (here: biometric recognition).

While I highlighted our main motivations behind developing the SAN in the previous paragraph, the general idea behind SANs can be thought of as a general approach to optimize an arbitrary loss function under constraints. Problems where we want to **maximize the performance with respect to one classifier while minimizing the performance of another**. Hence, even you are not working on face recognition problems, SANs could still potentially be useful for tackling a constrained optimization task.

The next section describes the overall SAN architecture from our ICB 2018 paper “[Semi-Adversarial Networks: Convolutional Autoencoders for Imparting Privacy to Face Images](https://ieeexplore.ieee.org/document/8411207/)” (preprint version: <https://arxiv.org/abs/1712.00321>).

## The Semi-Adversarial Nets Architecture

While the SAN architecture may look a bit intriguing in the figures we provided in the papers; it is relatively straightforward if we think of it as three main components:

1. An autoencoder to perturb an input image, but ensures that the image looks close to the original
2. A face matcher, which should be able to make accurate predictions
3. A gender classifier, which should be *unable* to make accurate predictions

![Semi adversarial nets 1 san architecture](https://sebastianraschka.com/images/blog/2018/semi-adversarial-nets-1/san-architecture.webp)

The SAN training can be summarized in PyTorch (pseudo) code as follows:

```python
ae = AutoEncoder()  
gc = GenderClassifier()  
fm = FaceMatcher()  

gc.load_state_dict(torch.load('saved_fm_model.pkl'))  
fm.load_state_dict(torch.load('saved_gc_model.pkl'))  

for fixed_model in (gc, fm):  
    for param in fixed_model.parameters():  
        param.requires_grad = False  

optimizer = torch.optim.Adam(ae.parameters(), lr=learning_rate)  

for epoch in range(num_total_epochs):  
    # ...  
    cost = loss_reconstruction + loss_gender_classification + loss_face_matching  
    cost.backward()  
    optimizer.step()
```

(The complete source code is available at <https://github.com/iPRoBe-lab/semi-adversarial-networks>.)

Please note that in addition to using a range of unseen face image datasets for evaluating the SAN model, we also discard the gender classifier and face matcher used during training and use a range of unseen face matchers and gender classifiers to evaluate our approach.

For those who are wondering, the following figure illustrates the reason why we refer to this setup as **semi-adversarial**:

![Semi adversarial nets 1 semi adversarial](https://sebastianraschka.com/images/blog/2018/semi-adversarial-nets-1/semi-adversarial.webp)

## Diversity and Generalization

As described in “Gender Privacy: An Ensemble of Semi Adversarial Networks for Confounding Arbitrary Gender Classifiers,” we recently focused on enhancing the generalization performance of the original SAN model by augmenting the dataset, among others. For example, to avoid common biases as discussed by Buolamwini et al. in “[Gender shades: Intersectional accuracy disparities in commercial gender classification](http://proceedings.mlr.press/v81/buolamwini18a.html),” we oversampled random samples of individuals with dark skin color, which are underrepresented in most face images datasets to mitigate potential bias. Furthermore, we extended the evaluation suite to a broader range of unseen gender classifiers and face matchers.

## What’s next

The two research articles summarized in this post cover the underlying architecture and “semi-adversarial” training scheme to optimize an objective under a constraint. Of course, many aspects are currently still being explored, such as different ensembling schemes and extending the multiple attributes, as mentioned in the paper.

This article pretty much covers some of our research on SAN and differential privacy in a nutshell. Also, there is much more to come soon. Also, we are excited to present our recent results at the [BTAS 2018](https://www.isi.edu/events/btas2018/home) conference and also talk about it at [ODSC West 2018](https://odsc.com/california) later this fall.
