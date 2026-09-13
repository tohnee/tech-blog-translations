---
title: "Discovering when an agent is present in a system"
source: https://deepmind.google/blog/discovering-when-an-agent-is-present-in-a-system/
site: deepmind
date: 2022-08-18
authors: Zachary Kenton, Ramana Kumar, Sebastian Farquhar, Jonathan Richens, Matt MacDermott, Tom Everitt
crawled: 2026-09-13
---

New, formal definition of agency gives clear principles for causal modelling of AI agents and the incentives they face

We want to build safe, aligned artificial general intelligence (AGI) systems that pursue the intended goals of its designers. [Causal influence diagrams](https://deepmindsafetyresearch.medium.com/progress-on-causal-influence-diagrams-a7a32180b0d1#b09d) (CIDs) are a way to model decision-making situations that allow us to reason about [agent incentives](https://ojs.aaai.org/index.php/AAAI/article/view/17368). For example, here is a CID for a 1-step Markov decision process – a typical framework for decision-making problems.

![A causal influence diagram (CID) for a 1-step Markov decision process, featuring a chance node S1 connected to decision node A1 by a dotted information link, and both S1 and A1 connected to a second chance node S2 by solid causal links, which in turn points to a yellow diamond utility node R2.](https://lh3.googleusercontent.com/9sLgX1JVVqsmVfCGd6hoLuun3F7u8f2wfww-9XW-a0Ik2vkVvXzZbfoHUXpGNyW5PtJgyYkDfApwy6oFQ5aQtEVlJlgbXqKrNKGjClUBQzY4Fg-NuWk=w1440)

S1 represents the initial state, A1 represents the agent’s decision (square), S2 the next state. R2 is the agent’s reward/utility (diamond). Solid links specify causal influence. Dashed edges specify information links – what the agent knows when making its decision.

By relating training setups to the incentives that shape agent behaviour, CIDs help illuminate potential risks before training an agent and can inspire better agent designs. But how do we know when a CID is an accurate model of a training setup?

Our new paper, [Discovering Agents](https://arxiv.org/abs/2208.08345), introduces new ways of tackling these issues, including:

- The first formal causal definition of agents: **Agents are systems that would adapt their policy if their actions influenced the world in a different way**
- An algorithm for discovering agents from empirical data
- A translation between causal models and CIDs
- Resolving earlier confusions from incorrect causal modelling of agents

Combined, these results provide an extra layer of assurance that a modelling mistake hasn’t been made, which means that CIDs can be used to analyse an agent’s incentives and safety properties with greater confidence.

## Example: modelling a mouse as an agent

To help illustrate our method, consider the following example consisting of a world containing three squares, with a mouse starting in the middle square choosing to go left or right, getting to its next position and then potentially getting some cheese. The floor is icy, so the mouse might slip. Sometimes the cheese is on the right, but sometimes on the left.

![An illustration of a grid with three horizontal squares, showing an empty left square, a mouse in the middle square, and a piece of cheese in the right square.](https://lh3.googleusercontent.com/dBDVGmGiiliQicECrVvgvB32eDL5CrYoQ09puR61QyuwYVdDThCW0Vnz0TXM-NcN5iH4iCbVUncaZj4XqRQFOguN0qbLKMF65jSpBO2r0sWMkBXwQoQ=w1440)

The mouse and cheese environment.

This can be represented by the following CID:

![A causal influence diagram (CID) representing the mouse example, with a pink square decision node D labeled "Left/Right" pointing to a white circular chance node X labeled "New position", which in turn points to a pink diamond utility node U labeled "Gets cheese".](https://lh3.googleusercontent.com/4NkJeGra3AzkhYM01q4ivyFIb-3W6QMmmSBkF6fSeaxen0i7gF-rFci3HV61FTKE92jcxJHf71gV8D0OtmNjKx9Nib8F33jAYCMhJE-avHqIK-l86g=w1440)

CID for the mouse. D represents the decision of left/right. X is the mouse’s new position after taking the action left/right (it might slip, ending up on the other side by accident). U represents whether the mouse gets cheese or not.

The intuition that the mouse would choose a different behaviour for different environment settings (iciness, cheese distribution) can be captured by a [mechanised causal graph](https://drive.google.com/file/d/1_OBLw9u29FrqROsLfhO6rIaWGK4xJ3il/view), which for each (object-level) variable, also includes a mechanism variable that governs how the variable depends on its parents. Crucially, we allow for links between mechanism variables.

This graph contains additional mechanism nodes in black, representing the mouse's policy and the iciness and cheese distribution.

![A mechanised causal graph for the mouse example. Below, three circular white nodes represent object-level variables: D (Left/Right) points to X (New position), which points to U (Gets cheese). Above, three black square mechanism nodes govern them: Policy (D-tilde) points to D, Iciness (X-tilde) points to X, and Cheese distribution (U-tilde) points to U. Mechanism links include a dashed black arrow from X-tilde to D-tilde, and a blue dash-dotted arrow from U-tilde to D-tilde representing a terminal edge.](https://lh3.googleusercontent.com/le3eeno-1GJCNqurogpt_oTLdxvLTJgOlwZPw2JKDCDRqbgbUmzssNZZZ4aYzvI-yx0sJyBPJt4lTiUSb3E6T3OEqPrJKoYbNTJk4BvBhCqL32hdEg=w1440)

Mechanised causal graph for the mouse and cheese environment.

Edges between mechanisms represent direct causal influence. The blue edges are special terminal edges – roughly, mechanism edges A~ → B~ that would still be there, even if the object-level variable A was altered so that it had no outgoing edges.

In the example above, since U has no children, its mechanism edge must be terminal. But the mechanism edge X~ → D~ is not terminal, because if we cut X off from its child U, then the mouse will no longer adapt its decision (because its position won’t affect whether it gets the cheese).

## Causal discovery of agents

Causal discovery infers a causal graph from experiments involving interventions. In particular, one can discover an arrow from a variable A to a variable B by experimentally intervening on A and checking if B responds, even if all other variables are held fixed.

Our first algorithm uses this technique to discover the mechanised causal graph:

![An illustration of "Algorithm 1" mapping a physical setup of a mouse in a three-square grid trying to get cheese to a corresponding mechanised causal graph.](https://lh3.googleusercontent.com/Ij9NGAAMEVJF4j9SnD1FQ85PrEON3_crqniJPAa1IzeOMxs2Jfv5EkJI7gpU-XWxDmu2mIakQzRqu1EWZj3CpIIAL34HpGKSFg_nINM4TC67N99ZNr0=w1440)

Algorithm 1 takes as input interventional data from the system (mouse and cheese environment) and uses causal discovery to output a mechanised causal graph. See paper for details.

Our second algorithm transforms this mechanised causal graph to a game graph:

![An illustration of "Algorithm 2" transforming a mechanised causal graph on the left into a game graph on the right.](https://lh3.googleusercontent.com/Oct9eHFPBn5YIgrQsothpBGaiBEJW99PlNkLkgE4w134kcVi9SM_kYcJzkmrQpLpfjseN7qgSIyByHmyevv5FLocCxMgxppo0sXGuOLXONvtnp81yFg=w1440)

Algorithm 2 takes as input a mechanised causal graph and maps it to a game graph. An ingoing terminal edge indicates a decision, an outgoing one indicates a utility.

Taken together, Algorithm 1 followed by Algorithm 2 allows us to discover agents from causal experiments, representing them using CIDs.

Our third algorithm transforms the game graph into a mechanised causal graph, allowing us to translate between the game and mechanised causal graph representations under some additional assumptions:

![An illustration of "Algorithm 3" transforming a game graph on the left into a mechanised causal graph on the right.](https://lh3.googleusercontent.com/l0_pbDgVLJ_TFcp6pwJAcrQugRgqq3kMIc7cz-4eOBNcaiAgZF_qdsopcdp7oKoifuv753pemAv1jBwcxOQJdHOP-pZ54WeskcSyFGZzMl2h_a84=w1440)

Algorithm 3 takes as input a game graph and maps it to a mechanised causal graph. A decision indicates an ingoing terminal edge, a utility indicates an outgoing terminal edge.

## Better safety tools to model AI agents

We proposed the first formal causal definition of agents. Grounded in causal discovery, our key insight is that agents are systems that adapt their behaviour in response to changes in how their actions influence the world. Indeed, our Algorithms 1 and 2 describe a precise experimental process that can help assess whether a system contains an agent.

Interest in causal modelling of AI systems is rapidly growing, and our research grounds this modelling in causal discovery experiments. Our paper demonstrates the potential of our approach by improving the safety analysis of several example AI systems and shows that causality is a useful framework for discovering whether there is an agent in a system – a key concern for assessing risks from AGI.

Excited to learn more? Check out our [paper](https://arxiv.org/abs/2208.08345). Feedback and comments are most welcome.
