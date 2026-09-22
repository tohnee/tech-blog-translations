---
title: "Modular Manifolds"
date: 2026-08-31
source: https://thinkingmachines.ai/blog/modular-manifolds/
crawled: 2026-09-22
---

When we train large neural networks, we need to keep them healthy. We do not want the tensors in the network—either the weights, activations or gradients—to grow too large or too small. Very small and very large tensors cause a variety of problems not just limited to numerical underflow and overflow. For example, weight matrices changing size during training makes it harder to design training algorithms—since the relative size of updates to weights has a significant impact on the speed of learning.

The gold standard for keeping tensors healthy is to normalize them. Normalization is commonplace for activation vectors, where we use techniques like [layer norm](https://arxiv.org/abs/1607.06450) to put the activations on a good scale before passing them to the next layer. It is also commonplace to normalize gradient updates, where we can interpret fast training algorithms like the [Muon optimizer](https://kellerjordan.github.io/posts/muon/) as spectrally normalizing the updates. Normalization provides us with certainty about the sizes of tensors—without needing to check Wandb!—and when training large neural networks with many interacting components, having certainty about the network internals is valuable.

Normalization is less commonly applied to weight matrices, although it is not unheard of. For example, the [EDM2](https://github.com/NVlabs/edm2) diffusion model codebase uses weight constraints and the authors report benefits in [their paper](https://arxiv.org/abs/2312.02696). And [BiT](https://arxiv.org/abs/1912.11370) uses [weight standardization](https://arxiv.org/abs/1903.10520). Various other techniques have been proposed but are not common practice in modern large-scale training.For some more examples, see [Salimans et al, 2016](https://arxiv.org/abs/1602.07868), [Miyato et al, 2018](https://arxiv.org/abs/1802.05957) and our paper [Liu et al, 2021](https://arxiv.org/abs/2102.07227). Normalizing the weight matrices might be a good idea for a few reasons. Weight constraints make understanding the relative size of optimization updates easier. They remove the problem of weight norms exploding. They allow us to focus hyperparameter tuning effort on tensors whose size matters most. They can force matrices to have a small [condition number](https://en.wikipedia.org/wiki/Condition_number), making their behaviour more predictable. And relatedly, weight constraints facilitate [Lipschitz guarantees](https://theses.hal.science/tel-04674274v1) for robustness to perturbations.

This post covers one appealing way to constrain the weight matrices of a neural network—by keeping the tensors constrained to submanifolds at each layer. This opens the door to re-thinking optimization, as we can co-design optimization algorithms with these manifold constraints. As an example, we proposeThis algorithm builds on work from Jianlin Su and Franz Louis Cesista, as discussed further below. a manifold version of the Muon optimizer whose weights are constrained to the Stiefel manifold: the manifold of matrices with unit [condition number](https://en.wikipedia.org/wiki/Condition_number). We conclude the post by defining the idea of a *modular manifold*, which is a composable manifold that attempts to make it easier to scale up and train large networks.

Our goal in writing this post is to provide an introduction to a research area that we are excited about, and highlight many directions for future work. We would love to see more work from the community on the topics mentioned at the end of the post!

## The shape of a manifold optimizer

This section works through the simplest example of learning on a manifold: a vector parameter constrained to a hypersphere in Rd\mathbb{R}^dRd. The vector parameter is trained to minimize a loss function defined over the full space Rd\mathbb{R}^dRd. This setup might be useful for, say, individual embedding vectors in a transformer model. This section will be a good warmup for the following section on [manifold Muon](#muon-on-the-stiefel-manifold) that considers matrix parameters.

We will not be too formal about the definition of a manifold here: it is enough to understand that a manifold is a curved surface that looks flat when you zoom in close enough. The locally flat approximation at a point on the manifold is called the *tangent space* to the manifold, as visualized in [Figure](#fig:tangent-space) :

The sphere in three dimensions—or the hypersphere in higher dimensions—is a manifold. The locally flat approximation at a point on the manifold is called the tangent space to the manifold and is visualized as the red plane in the figure.

We can characterize the hypersphere in ddd dimensions as the set of points w∈Rdw \in \mathbb{R}^dw∈Rd of unit Euclidean norm. And the tangent space at a point www on the hypersphere is the set of all vectors a∈Rda \in \mathbb{R}^da∈Rd that are orthogonal to www.

To keep the weights constrained to the manifold, we could use a non-manifold optimizer and just project the weights back to the manifold after each step. Instead, we are interested in designing methods that take steps in the tangent space. The reason is that we would like to be able to equate the learning rate of our optimizer with the actual length of the optimization step. But if the optimization steps are pointing significantly off manifold and then being projected back, this nice property does not hold. Similar motivation is given in Section 2.3 of the [EDM2 paper](https://arxiv.org/abs/2312.02696).

Before we can design a training algorithm for this manifold, something important we need to decide on is how to measure distanceFor a manifold to be “Riemannian”, the distance measure must be induced by an inner product. The [Euclidean (ℓ2\ell_2ℓ2​) norm](https://en.wikipedia.org/wiki/Euclidean_distance) is induced by an inner product, but the [Manhattan (ℓ1\ell_1ℓ1​) distance](https://en.wikipedia.org/wiki/Taxicab_geometry) is not. in the tangent space. A common choice is the Euclidean distance, but we could also choose to measure distance in other ways, as visualized in [Figure](#fig:inscribed-norm-balls) . In the next section, we will talk about choosing a distance measure based on the functionality of the module.

Inscribing unit balls in the tangent space for different distance measures. The ℓ2\ell_2ℓ2​ (Euclidean) unit ball is a circle while the ℓ1\ell_1ℓ1​ (Manhattan) unit ball is a diamond.

Crucially, the choice of distance measure changes the direction of the best optimization step. If the distance measure is non-Euclidean, then for a fixed length step, we may be able to move further in the direction of the gradientBy gradient, we mean the partial derivative of the loss with respect to the weights. Mathematicians reserve the term gradient for [something else](https://en.wikipedia.org/wiki/Gradient#Riemannian_manifolds) in Riemannian geometry. by not following the gradient direction exactly! This concept is visualized in [Figure](#fig:tangent-space-with-gradient) .

How geometry influences the direction of the best optimization step. The pink arrow represents the raw gradient—meaning the partial derivative of the loss with respect to the weights. The yellow diamond denotes the ℓ1\ell_1ℓ1​ unit ball. The green arrow is the unit vector pointing furthest in the direction of the gradient. Notice how the green arrow is not parallel to the pink arrow. (In practice, the pink arrow need not lie in the tangent space, although the green arrow will do by construction.) Try dragging the pink arrow to see how the best update direction changes.

To see how this works out in math, we can formulate the optimal update direction given a manifold constraint and a distance measure as itself solving a constrained optimization problem. We will demonstrate this for the case of the hypersphere equipped with the Euclidean norm. Letting ggg denote the gradient, www the current point on the hypersphere, aaa the update direction and η\etaη the learning rate, we need to solve:

min⁡a∈Rda⊤g∥a∥2=1⏟linear change in losssuch that∥a∥2=η⏟size constraintanda⊤w=0∥a∥2=1⏟tangent constraint.(⋆)\min_{a\in\mathbb{R}^d} \quad \underbrace{a^\top g\vphantom{\|a\|_2 = 1}}_{\mathclap{\text{linear change in loss}}} \quad \text{such that} \quad \underbrace{\|a\|_2 = \eta}_{\mathclap{\text{size constraint}}} \quad \text{and} \quad \underbrace{a^\top w = 0\vphantom{\|a\|_2 = 1}}_{\mathclap{\text{tangent constraint}}}.\tag{$\star$}a∈Rdmin​linear change in lossa⊤g∥a∥2​=1​​such thatsize constraint∥a∥2​=η​​andtangent constrainta⊤w=0∥a∥2​=1​​.(⋆)

Mapping back to the visual language of Figures ,  and , this formula says that the green arrow (optimal value of aaa) must belong to the red tangent hyperplane (a⊤w=0a^\top w = 0a⊤w=0) and must also lie on a yellow circle of radius η\etaη (∥a∥2=η\|a\|_2 = \eta∥a∥2​=η). To solve (⋆)(\star)(⋆), we can apply the [method of Lagrange multipliers](https://en.wikipedia.org/wiki/Lagrange_multiplier). The relevant Lagrangian function is given by:

L(a,λ,μ)=a⊤g+λ2⋅(a⊤a−η)+μ⋅(a⊤w),\mathcal{L}(a, \lambda, \mu) = a^\top g + \frac{\lambda}{2} \cdot (a^\top a - \eta) + \mu \cdot (a^\top w),L(a,λ,μ)=a⊤g+2λ​⋅(a⊤a−η)+μ⋅(a⊤w),

where λ\lambdaλ and μ\muμ are Lagrange multipliers. Setting the derivative of the Lagrangian with respect to aaa to zero and applying the constraints to solve for λ\lambdaλ and μ\muμ, the optimal update aopta_\mathrm{opt}aopt​ ends up being given by the following formula:

aopt=−η×g−ww⊤g∥g−ww⊤g∥2.a_\mathrm{opt} = - \eta \times \frac{g - ww^\top g}{\|g-ww^\top g\|_2}.aopt​=−η×∥g−ww⊤g∥2​g−ww⊤g​.

In words, the optimal update is given by subtracting out the radial component from the gradient, normalizing and multiplying by the learning rate. Since this update lies in the tangent space, actually a very smallFor a learning rate η\etaη, the effect of the retraction map is O(η2)\mathcal{O}(\eta^2)O(η2) small, so the learning rate *almost* equals the length of the step. correction is needed to stay on the manifold. The correction is known as a “retraction map” and is visualized in [Figure](#fig:retraction-map) :

Visualizing the retraction map. The green arrow is the update taken in the tangent space. Since for large step sizes the tangent space starts to diverge from the manifold, we need to project the updated weights back to the manifold using the retraction map—illustrated by the purple arrow.

We can solve for the retraction map by applying Pythagoras’ theorem to [Figure](#fig:retraction-map) . For a unit hypersphere and a step of length η\etaη, the hypotenuse has length 1+η2\sqrt{1+\eta^2}1+η2​ and therefore the retraction map for the hypersphere equipped with the Euclidean norm is simply given by dividing the updated weights through by 1+η2\sqrt{1+\eta^2}1+η2​. Putting everything together, the full manifold optimization algorithm is then given by:

w←11+η2[w−η×g−ww⊤g∥g−ww⊤g∥2].w \gets \frac{1}{\sqrt{1+\eta^2}} \left[w - \eta \times \frac{g - ww^\top g}{\|g-ww^\top g\|_2}\right].w←1+η2​1​[w−η×∥g−ww⊤g∥2​g−ww⊤g​].

As an exercise for the reader: try calculating the Euclidean norm of the updated weight vector and check that the updated weight vector indeed lies on the hypersphere.

To summarize this section, a first-order manifold optimizer has three steps:

1. Find the tangent vector of unit length that goes furthest in the gradient direction.
2. Multiply this direction by the learning rate and subtract from the weights;
3. Retract the updated weights back to the manifold.

There are two decisions to make in applying this procedure: what manifold constraint we should use and how we should measure length. By making different decisions, we can generate different optimization algorithms as shown in the following table.

| Manifold | Norm | Optimizer |
| --- | --- | --- |
| Euclidean Rn\mathbb{R}^nRn | Euclidean norm | vanilla gradient descent |
| Euclidean Rn\mathbb{R}^nRn | infinity norm | sign gradient descent |
| hypersphere SnS^nSn | Euclidean norm | hyperspherical descent |
| matrix space Rm×n\mathbb{R}^{m\times n}Rm×n | spectral norm | Muon |
| Stiefel manifold ⊂Rm×n\subset\mathbb{R}^{m\times n}⊂Rm×n | spectral norm | manifold Muon |

We will derive the final algorithm in the table, manifold Muon, in the next section. To design a manifold constraint and a distance function for a matrix parameter, we shall think carefully about the role that a weight matrix plays inside a neural network.

## Manifold Muon

A typical weight matrix WWW in a transformer is a “vector-multiplier”, meaning that it transforms an input vector xxx into an output vector y=Wxy = Wxy=Wx. We will design a manifold constraint and a distance function so that the matrix acts in a good way on input vectors: the matrix should not produce excessively small or large outputs, and updates to the matrix should not cause the output vector to change too much or too little.

A good way to think about how a matrix acts on vectors is through the [singular value decomposition](https://en.wikipedia.org/wiki/Singular_value_decomposition), illustrated in [Figure](#fig:svd) . The SVD decomposes a matrix in a way that tells us how the matrix stretches input vectors along different axes.

![](svgs/svd.svg)

The singular value decomposition. A matrix M∈Rm×nM\in\mathbb{R}^{m\times n}M∈Rm×n of rank kkk can always be decomposed as M=UΣV⊤M = U \Sigma V^\topM=UΣV⊤, where U∈Rm×kU\in\mathbb{R}^{m\times k}U∈Rm×k and V∈Rn×kV\in\mathbb{R}^{n\times k}V∈Rn×k have orthonormal columns and Σ∈Rk×k\Sigma\in\mathbb{R}^{k\times k}Σ∈Rk×k is a diagonal matrix with only positive entries. The entries of Σ\SigmaΣ are called the singular values of MMM. The singular values measure the stretching effect that the matrix has on vectors that align with the corresponding columns of UUU and VVV.

We would like the matrix to have a stretching effect close to one, so we will choose a matrix manifold where all the singular values are exactly one. This matrix manifold is known formally as the [*Stiefel manifold*](https://en.wikipedia.org/wiki/Stiefel_manifold). We can assume without loss of generality that we are dealing with a tall matrix (m≥nm \geq nm≥n), and then the Stiefel manifold can be equivalently defined as the following set:

Stiefel(m,n):={W∈Rm×n∣WTW=In}.\mathsf{Stiefel}(m,n) := \left\{ W \in \mathbb{R}^{m \times n} \mid W^T W = I_n \right\}.Stiefel(m,n):={W∈Rm×n∣WTW=In​}.

Furthermore, [one may show](https://cseweb.ucsd.edu/classes/sp24/cse291-e/papers/StiefelManifold/StiefelNotes.pdf) that a matrix A∈Rm×nA \in \mathbb{R}^{m \times n}A∈Rm×n lies tangentNotice that the Stiefel constraint WTW=InW^T W = I_nWTW=In​ directly generalizes the hyperspherical constraint w⊤w=1w^\top w = 1w⊤w=1 from the previous section. Similarly, the tangent space condition generalizes the hyperspherical one that a⊤w=0a^\top w = 0a⊤w=0. to the Stiefel manifold at matrix WWW if and only if:

A⊤W+W⊤A=0.A^\top W + W^\top A = 0.A⊤W+W⊤A=0.

To design a manifold optimizer for the Stiefel manifold, all that remains is to choose a distance function. To limit the maximum stretching effect the weight update can have on an input vector, we will choose the *spectral norm*, which measures the largest singular value of a matrix. Although this only limits the maximum effect the update can have, since the optimizer we derive will saturate this bound, it will turn out to prevent the minimum effect of the update from being too small.There are some exceptions to this statement, such as when a weight matrix has a fan-out less than its fan-in, in which case we cannot escape from the matrix and its updates having a null space and mapping some inputs to zero.

The idea of doing gradient descent under a spectral norm constraint is what [led to](https://jeremybernste.in/writing/deriving-muon) the Muon optimizer and, when combined with the Stiefel manifold constraint, we obtain a problem that we shall call *manifold Muon*:

min⁡A∈Rm×ntrace⁡(GTA)⏟linear change in losssuch that∥A∥spectral≤η⏟size constraintandATW+WTA=0∥A∥spectral=η⏟tangent constraint.(†)\min_{A\in\mathbb{R}^{m\times n}} \quad \underbrace{\operatorname{trace}(G^T A)}_{\mathclap{\text{linear change in loss}}} \quad \text{such that} \quad \underbrace{\|A\|_{\text{spectral}} \leq \eta}_{\mathclap{\text{size constraint}}} \quad \text{and} \quad \underbrace{A^T W + W^T A = 0\vphantom{\|A\|_{\text{spectral}} = \eta}}_{\mathclap{\text{tangent constraint}}} \tag{$\dagger$}.A∈Rm×nmin​linear change in losstrace(GTA)​​such thatsize constraint∥A∥spectral​≤η​​andtangent constraintATW+WTA=0∥A∥spectral​=η​​.(†)

The manifold Muon problem (†)(\dagger)(†) directly generalizes problem (⋆)(\star)(⋆) from the previous section. Solving (†)(\dagger)(†) is harder than solving (⋆)(\star)(⋆), and here we will present a numerical solution inspiredI [figured out](https://docs.modula.systems/algorithms/manifold/orthogonal/) how to solve manifold Muon in the square case late last year, but I was unable to solve the full rectangular case and thus [posed the problem](https://docs.modula.systems/algorithms/manifold/orthogonal/#open-problem-extending-to-the-stiefel-manifold) as an open problem on the Modula docs. Jianlin Su [solved the problem](https://kexue.fm/archives/11221) this summer by taking a Lagrangian approach and working out a fixed point iteration on the optimality condition. I saw an early version of Jianlin’s work (which did not quite work yet) and also [related work](https://leloykun.github.io/ponder/steepest-descent-stiefel/) by Franz Louis Cesista, and I was able to work out the dual ascent algorithm presented here. by work done by Jianlin Su and Franz Louis Cesista.

Our key insight is that (†)(\dagger)(†) is a convex optimization problem that may be solved via a standard method known as [*dual ascent*](https://www.cs.cmu.edu/~pradeepr/convexopt/Lecture_Slides/dual-ascent.pdf). Here we will just sketch the main idea, but you can find a more detailed derivation [on this page](https://docs.modula.systems/algorithms/manifold/stiefel/).

Similar to Jianlin’s approach, we introduce a matrix of Lagrange multipliers Λ∈Rn×n\Lambda\in\mathbb{R}^{n\times n}Λ∈Rn×n. We then apply a series of transformations to convert the problem (†)(\dagger)(†) from a *constrained minimization problem* to an *unconstrained maximization problem*:

(†)=min⁡∥A∥spectral≤ηmax⁡Λ  trace⁡G⊤A+trace⁡Λ⊤(A⊤W+W⊤A)=min⁡∥A∥spectral≤ηmax⁡Λ  trace⁡A⊤(G+2W(Λ+Λ⊤))=max⁡Λmin⁡∥A∥spectral≤η  trace⁡A⊤(G+2W(Λ+Λ⊤))=max⁡Λ  −η×∥G+2W(Λ+Λ⊤)∥nuclear.\begin{align}
(\dagger) &= \min_{\|A\|_\mathrm{spectral} \leq \eta} \max_{\Lambda} \;\operatorname{trace} G^\top A + \operatorname{trace}\Lambda^\top (A^\top W + W^\top A) \\
&= \min_{\|A\|_\mathrm{spectral} \leq \eta} \max_{\Lambda}\; \operatorname{trace}A^\top (G + 2W(\Lambda+\Lambda^\top))\\
&= \max_{\Lambda} \min_{\|A\|_\mathrm{spectral} \leq \eta} \; \operatorname{trace}A^\top (G + 2W(\Lambda+\Lambda^\top))\\
&= \max_{\Lambda} \; - \eta \times \|G + 2W(\Lambda+\Lambda^\top)\|_\mathrm{nuclear}.
\end{align}(†)​=∥A∥spectral​≤ηmin​Λmax​traceG⊤A+traceΛ⊤(A⊤W+W⊤A)=∥A∥spectral​≤ηmin​Λmax​traceA⊤(G+2W(Λ+Λ⊤))=Λmax​∥A∥spectral​≤ηmin​traceA⊤(G+2W(Λ+Λ⊤))=Λmax​−η×∥G+2W(Λ+Λ⊤)∥nuclear​.​​

Equation (1) reformulates the problem as a [saddle point problem](https://www-cs.stanford.edu/people/davidknowles/lagrangian_duality.pdf): the maximization over Λ\LambdaΛ will send the objective to infinity whenever the tangent space condition is violated. Equation (2) follows by applying properties of the trace and equation (3) follows from Sion’s minimax theorem. The inner minimization in equation (3) is solved by setting Aopt(Λ)=−η×msign⁡(G+2W(Λ+Λ⊤))A_\mathrm{opt}(\Lambda) = - \eta \times \operatorname{msign}(G + 2W(\Lambda+\Lambda^\top))Aopt​(Λ)=−η×msign(G+2W(Λ+Λ⊤)) where msign⁡\operatorname{msign}msign is the [matrix sign function](https://docs.modula.systems/algorithms/newton-schulz/).The matrix sign function snaps the singular values of a matrix to one. It may be computed efficiently on GPUs via Newton-Schulz iteration or the recent [Polar Express](https://arxiv.org/abs/2505.16932) algorithm. And we obtain equation (4) by substituting this expression for Aopt(Λ)A_\mathrm{opt}(\Lambda)Aopt​(Λ) into equation (3). Equation (4) is known as the “dual problem” to (†)(\dagger)(†) and we can solve it by gradient ascent. After some work, the gradient of the dual function is given by:

H(Λ):=−η×∇Λ∥G+W(Λ+Λ⊤)∥nuclear=−η×[W⊤msign(G+2W(Λ+Λ⊤))+msign⁡(G+2W(Λ+Λ⊤))⊤W],\begin{align}
H(\Lambda) &:= - \eta \times \nabla_\Lambda \|G + W (\Lambda+\Lambda^\top)\|_\mathrm{nuclear} \\
&= - \eta \times [W^\top\mathrm{msign}(G + 2W (\Lambda+\Lambda^\top)) + \operatorname{msign}(G + 2W (\Lambda+\Lambda^\top))^\top W],
\end{align}H(Λ)​:=−η×∇Λ​∥G+W(Λ+Λ⊤)∥nuclear​=−η×[W⊤msign(G+2W(Λ+Λ⊤))+msign(G+2W(Λ+Λ⊤))⊤W],​​

where the nuclear norm ∥⋅∥nuclear\|\cdot\|_\mathrm{nuclear}∥⋅∥nuclear​ measures the sum of the singular values of a matrix.

Finally, we can write down the manifold Muon algorithm:Note that this algorithm is closely related to [Jianlin Su’s solution](https://kexue.fm/archives/11221). Where we run dual ascent, Jianlin’s solution amounts to solving for the maximum of the dual function H(Λ)=0H(\Lambda)=0H(Λ)=0 via a fixed point iteration.

1. Run gradient ascent on the dual variable Λ←Λ+α×H(Λ)\Lambda \gets \Lambda + \alpha \times H(\Lambda)Λ←Λ+α×H(Λ) to solve for Λopt\Lambda_\mathrm{opt}Λopt​.
2. Compute the update Aopt=−η×msign⁡(G+2W(Λopt+Λopt⊤))A_\mathrm{opt} = - \eta \times \operatorname{msign}(G + 2W(\Lambda_{\mathrm{opt}}+\Lambda_\mathrm{opt}^\top))Aopt​=−η×msign(G+2W(Λopt​+Λopt⊤​)).
3. Apply the update to the weights W←W+AoptW \gets W + A_\mathrm{opt}W←W+Aopt​.
4. Retract the weights back to the manifold W←msign⁡(W)W \gets \operatorname{msign}(W)W←msign(W).

We ran a very small experiment to sanity check the algorithm and provide a minimal implementation for students or researchers to play with. Each training run finishes in less than a minute. The code is [here](https://github.com/thinking-machines-lab/manifolds/) and see [Figure](#fig:cifar10)  for the setup and results.

![](svgs/cifar10.svg)

Training a small MLP for 3 epochs on the CIFAR-10 dataset. The different lightly shaded blue curves show different weight decay settings for AdamW. Results were averaged over 3 random seeds. The manifold Muon optimizer attained higher train and test accuracy than AdamW. The third plot shows the final singular value distribution of the first weight matrix for the best performing learning rate: the singular values after training with manifold Muon are all close to 1. Manifold Muon increased the wall clock time per step compared to AdamW, although this could be improved by running fewer steps of dual ascent or adding momentum to the algorithm and running dual ascent online. Depending on other systems bottlenecks, the overhead may not be an issue.

## Modular manifolds

So far in this post, we have discussed manifold constraints for individual parameter tensors and co-designed optimization logic for these constraints. A question we have not answered is: what happens when we combine layers to build networks? Can we think about individual layers in isolation—or do we need to be careful about interactions between layers and modify the optimization logic in response? The goal of this section is to point out that there is a way to extend the reasoning we introduced in the previous two sections to the case of whole networks, and we call this *the theory of modular manifolds*.The theory of modular manifolds builds on research I did with my friend Tim Large, my postdoc advisor Phillip Isola, my PhD advisor Yisong Yue and many other amazing collaborators. At the end of the section, we provide some links to learn more.

The idea of modular manifolds is to build an abstraction that tells us how to budget learning rates across layers. The actual optimization logic in each layer ends up being the same as what we already worked out, except that the learning rate for a layer is modified depending on where the layer appears in the network. The abstraction rests upon a key observation made in our paper on the [modular norm](https://arxiv.org/abs/2405.14813), that budgeting learning rates—both across layers and when scaling up individual layers—is intimately tied to understanding the Lipschitz sensitivity of the network output with respect to the weights. The abstraction tracks this sensitivity as we build the network, and manifold constraints help us get a much tighter understanding of this sensitivity.

The starting point for the abstraction is to think of any neural network module—from a layer to a whole transformer—as a mathematical object with three attributes:

1. A forward function f:W×X→Yf:\mathcal{W} \times \mathcal{X} \to \mathcal{Y}f:W×X→Y that maps from a parameter space W=Rd\mathcal{W} = \mathbb{R}^dW=Rd and an input space X\mathcal{X}X to an output space Y\mathcal{Y}Y.
2. A submanifold of the weight space M⊂W\mathcal{M}\subset\mathcal{W}M⊂W that the weights are constrained to.
3. A norm ∥⋅∥:W→R\|\cdot\| : \mathcal{W} \to \mathbb{R}∥⋅∥:W→R that acts as a measuring stick on weight space.

For example, a linear module equipped with the spectral norm and constrained to the Stiefel manifold, for which we have already worked out an optimizer, would be written:

StiefelLinear={(W,x)↦Wx,(forward function)Stiefel(m,n),(manifold)∥⋅∥spectral.(norm) \mathsf{StiefelLinear} = \begin{cases}(W, x) \mapsto Wx, & \text{(forward function)}\\ \mathsf{Stiefel}(m,n), & \text{(manifold)}\\ \|\cdot\|_\mathrm{spectral}. & \text{(norm)}\end{cases}StiefelLinear=⎩⎨⎧​(W,x)↦Wx,Stiefel(m,n),∥⋅∥spectral​.​(forward function)(manifold)(norm)​

Provided that an input xxx to the StiefelLinear\mathsf{StiefelLinear}StiefelLinear module has unit ℓ2\ell_2ℓ2​ norm, then StiefelLinear\mathsf{StiefelLinear}StiefelLinear is Lipschitz with respect to its weights in the module’s assigned norm with Lipschitz constant one:This argument can be extended to the RMS norm on the input and the RMS–RMS operator norm on the weights.

∥(W+ΔW)x−Wx∥2≤∥ΔW∥spectral×∥x∥2=∥ΔW∥spectral.\|(W + \Delta W) x - Wx\|_2 \leq \|\Delta W\|_\mathrm{spectral} \times \|x\|_2 = \|\Delta W\|_\mathrm{spectral}.∥(W+ΔW)x−Wx∥2​≤∥ΔW∥spectral​×∥x∥2​=∥ΔW∥spectral​.

This type of Lipschitz statement helps us understand how to scale weight updates to this module since it gives us a bound on how much the output can change when we perturb the weights. But when we compose two modules, can we automatically compile a Lipschitz statement on the joint weight space of the new module? The answer turns out to be yes, if we follow special rules for building the new module:

1. The new forward function f3f_3f3​ is given by composing the two existing forward functions f1f_1f1​ and f2f_2f2​:
   f3((w1,w2),x):=f2(w2,f1(w1,x)).f_3((w_1, w_2), x) := f_2(w_2, f_1(w_1, x)). \qquadf3​((w1​,w2​),x):=f2​(w2​,f1​(w1​,x)).
2. The new manifold constraint M3\mathcal{M}_3M3​ is just the Cartesian product (see [Figure](#fig:product-manifold)  for a fun example) of the two existing manifolds M1\mathcal{M}_1M1​ and M2\mathcal{M}_2M2​:
   M3=M1×M2.\mathcal{M}_3 = \mathcal{M}_1 \times \mathcal{M}_2. \qquadM3​=M1​×M2​.
3. The new norm function is the max of the two existing norm functions weighted by special scalar coefficients s1s_1s1​ and s2s_2s2​. Letting ∥⋅∥1\|\cdot\|_1∥⋅∥1​ denote the first module’s norm and ∥⋅∥2\|\cdot\|_2∥⋅∥2​ denote the second module’s norm, the new norm ∥⋅∥3\|\cdot\|_3∥⋅∥3​ is given by:
   ∥(w1,w2)∥3:=max⁡(s1⋅∥w1∥1,s2⋅∥w2∥2).\|(w_1, w_2)\|_3 := \max(s_1\cdot \|w_1\|_1, s_2\cdot \|w_2\|_2). \qquad∥(w1​,w2​)∥3​:=max(s1​⋅∥w1​∥1​,s2​⋅∥w2​∥2​).

When we use this composite norm to derive optimizers—following the same recipe we used in the first two sections of this post—we end up deriving separate optimizers for each layer, but the scalar coefficients sis_isi​ budget the learning rates across layers.

We give much more detail on this construction, including extending it to other ways of combining modules, in our paper on the [modular norm](https://arxiv.org/abs/2405.14813)—although the paper does not cover manifold optimization. You can also check out our paper on [modular duality](https://arxiv.org/abs/2410.21265) for more on building optimizers in the modular norm. The [Modula project](https://modula.systems) builds toward a programmatic implementation of this construction.

![](svgs/product-manifold.svg)

The Cartesian product is a simple way to glue together two manifolds. For example, the product of a line and a disk is a cylinder. We get one copy of the disk at every point on the line.

## Directions for future work

We are excited about any research that tries to make neural network training as principled and automatic as the forward pass. The ideas in this post benefitted strongly from interactions with external researchers like Jianlin Su and Franz Louis Cesista. We would love to see more work on these topics from the community.

Some possible directions for future work are:

- **Modularity.** What manifolds should attention heads live on? Should embeddings be constrained differently than unembeddings? We can mix-and-match constraints in different parts of the network, or leave some tensors unconstrained.
- **Numerics.** Manifold constraints also place constraints on the range of values that individual weight entries can take. Does this impact numerics, or make low-precision training easier?
- **Convex optimization.** The manifold Muon algorithm involves running dual ascent. Can we apply more sophisticated convex optimization techniques to solve the dual problem faster or more reliably?
- **Convergence analysis.** How fast do these algorithms converge? Does good conditioning of the weight matrices benefit convergence? Is there more that we can say theoretically?
- **Regularization.** Manifold constraints implicitly regularize the model. Could we design constraints or tune their radii to improve generalization?
- **Architecture-optimizer co-design.** While hard manifold constraints may not ultimately be the right way to constrain weight matrices, they exemplify the idea of tightly co-designing optimization algorithms with architecural components. Are there more opportunities here?
- **Non-Riemannian geometry.** Most work on manifold optimization works in a Riemannian world where distances are induced by inner products and norm balls are ellipsoids. But neural networks are different: matrices act as operators, and operator norms like the spectral norm do not emerge from inner products. This implies, for example, that norm balls can have sharp corners and there is no unique gradient flow. Is there more to be discovered in this non-Riemannian world?
- **Practical implementation.** Applying these techniques at scale requires efficient manifold operations on GPUs. The recent [Polar Express](https://arxiv.org/abs/2505.16932) paper shows promise for fast matrix sign computation. What other algorithmic innovations do we need?

## Further reading

- **Manifold optimization.** [Absil, Mahony & Sepulchre](https://press.princeton.edu/absil)’s textbook is a standard reference. For the Stiefel manifold specifically, see [Edelman et al, 1998](https://math.mit.edu/~edelman/publications/geometry_of_algorithms.pdf). These works live in a Riemannian world. Similarly most machine learning papers that consider optimization on the Stiefel manifold take a Riemannian point of view: see [Li et al, 2020](https://arxiv.org/abs/2002.01113), [Kong et al, 2022](https://arxiv.org/abs/2205.14173) and [Park et al, 2025](https://arxiv.org/abs/2508.17901) for some examples.
- **Non-Riemannian geometry in machine learning.** [Thomas Flynn’s paper](https://arxiv.org/abs/1708.00523) from 2017 on duality structure gradient descent characterizes the neural network weight space as a *Finsler manifold*, meaning a manifold equipped with a norm. It is well worth a read. Also see Jianlin Su’s [recent blog post](https://kexue.fm/archives/11221) on Stiefel Muon as well as Franz Louis Cesista’s [blog post](https://leloykun.github.io/ponder/steepest-descent-stiefel/) on a heuristic solution to Muon on the Stiefel manifold. Franz also wrote a [followup blog post](https://leloykun.github.io/ponder/steepest-descent-finsler/) generalizing the solution presented here. The [Scion paper](https://arxiv.org/abs/2502.07529) imposes weight constraints a different way via convex combinations and [Carlson et al, 2015](https://papers.nips.cc/paper_files/paper/2015/hash/f50a6c02a3fc5a3a5d4d9391f05f3efc-Abstract.html) wrote an early paper on (unconstrained) spectral descent.
- **The Modula project.** The goal of the Modula project is to build a library that automatically compiles steepest descent optimizers along with Lipschitz statements for general architectures. Check out the project page at <https://modula.systems> as well as our paper on the [modular norm](https://arxiv.org/abs/2405.14813) and [modular duality](https://arxiv.org/abs/2410.21265). Our [optimization anthology](https://arxiv.org/abs/2409.20325) also provides an accessible route into this space of ideas.
- **Lipschitz-constrained deep learning.** There has been a lot of work on this topic. For example, check out [Louis Béthune](https://theses.hal.science/tel-04674274v1) and [Tsui-Wei Weng’s](https://dspace.mit.edu/bitstream/handle/1721.1/129313/1227782217-MIT.pdf?sequence=1&isAllowed=y) PhD theses. Usually work on this topic does not connect weight-Lipschitzness to optimizer design. See also [Anil et al, 2018](https://arxiv.org/abs/1811.05381) and our paper [Newhouse et al, 2025](https://arxiv.org/abs/2507.13338).

## Citation

Please cite this work as:

```
Jeremy Bernstein, "Modular Manifolds",
Thinking Machines Lab: Connectionism, Sep 2025.
```

Or use the BibTeX citation:

```
@article{bernstein2025manifolds,
  author = {Jeremy Bernstein},
  title = {Modular Manifolds},
  journal = {Thinking Machines Lab: Connectionism},
  year = {2025},
  note = {https://thinkingmachines.ai/blog/modular-manifolds/},
  doi = {10.64434/tml.20250926}
}
```
