---
title: "Embeddings, Representations, and Latent Space Compared"
source: https://sebastianraschka.com/faq/docs/representation-embedding-latent.html
crawled: 2026-09-06
---

# Embeddings, Representations, and Latent Space Compared

While all three concepts, embedding vectors, vectors in latent space, and representations, are often used synonymously, we can make slight distinctions:

- representations are encoded versions of the original input;
- latent vectors are intermediate representations;
- embedding vectors are representations where similar items are close to each other.

**Embeddings**

Embedding vectors, or *embeddings* for short, encode relatively high-dimensional data into relatively low-dimensional vectors.

We can apply embedding methods to create a dense vector from a one-hot encoding. However, we can also use embedding methods for dense data such as images.

Taking it to the extreme, embedding methods can be used to encode data into two-dimensional dense and continuous representations for visualization purposes and clustering analysis.

A fundamental property of embeddings is that they encode *distance* or *similarity*. This means that embeddings capture the semantics of the data such that similar inputs are close in the embeddings space.

**Latent space**

*Latent space* is typically used synonymously with *embedding space* – the space into which embedding vectors are mapped.

Similar items can appear close in the latent space; however, this is not a strict requirement. More loosely, we can think of the latent space as any feature space that contains the features, often a compressed version of the original input features. These latent space features can be learned by a neural network, for example, an autoencoder that reconstructs input images, as shown in the figure below.

**Representation**

We used the term representation above. A representation is an encoded, typically intermediate form of an input. For instance, an embedding vector or vector in the latent space is a *representation* of the input. However, representations can also be produced by simpler procedures. For example, one-hot encoded vectors are considered representations of an input.
