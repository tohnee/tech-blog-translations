---
title: "Practical cryptanalysis with MiniMax's latest Internal Model"
date: 2026-11-20
source: https://minimax.io/blog/practical-cryptanalysis-with-minimaxs-latest-internal-model
crawled: 2026-11-21
---

# Practical cryptanalysis with MiniMax's latest Internal Model

2026-11-20

cryptography

Our research team used an internal-only research model that we will call **MiniMax's Internal Model (MIM)** to conduct automated cryptanalysis across modern cryptographic schemes. The model identified several previously unknown structural flaws and turned multiple theoretical attacks into practical breaks.

Our results cover three main areas: **First,** across historical NIST cryptographic standardization competitions, MIM produced the first practical breaks against multiple candidate algorithms that previously had no known practical attacks. **Second,** we extended our scope to recent papers from leading cryptography conferences and journals, as well as competition-winning designs, achieving efficient authenticated ciphertext forgery or key recovery on several peer-reviewed constructions and extending the highest number of attacked rounds on a recent block cipher. **Third,** in tackling classical hard mathematical problems that underlie public-key cryptography, MIM combined algebraic structure exploitation with systems-level engineering optimizations to solve dozens of previously unsolved high-order instances in public cryptographic challenges, achieving measured speedups of hundreds to tens of thousands of times over prior state-of-the-art solvers.

### Why cryptanalysis

Cryptography secures network communications, financial transactions, and critical infrastructure. Unlike software vulnerability research, which looks for implementation bugs in coding, cryptanalysis targets the design itself, examining primitives, protocols, and hardness assumptions for flaws. Modern cryptanalysis tests both mathematical reasoning and code, with clear, verifiable outcomes. On-paper derivations and complexity estimates aren't enough: a model has to turn its analysis into executable code that carries out the attack within strict data and compute budgets. A single flaw in either the mathematical derivation or the code causes the entire attack to fail. The script either recovers the target secret or it does not, leaving zero room for hallucination. This binary outcome makes cryptanalysis a clean testbed for long-horizon reasoning and scientific discovery in language models.

### 1. Breaking NIST candidates with no known practical attacks

Testing language models on cryptanalysis requires separating reasoning from memorized papers. CryptanalysisBench (NeurIPS 2026), created by researchers from ETH Zurich, Anthropic, and collaborators, collects entries from four NIST standardization competitions: AES, SHA-3, lightweight cryptography, and post-quantum cryptography. Tier 1 contains 49 schemes with known practical attacks. Tier 2 contains 135 publicly reviewed schemes with no known practical attacks, along with 7 production-strength challenge schemes.

Using the same setup as the original paper, we evaluated MIM on Tier 2. Its independent reasoning traces show that it can directly analyze the underlying mathematics and compromise several NIST candidates. Examples include:

* **Waterfall-256 (NIST SHA-3 candidate):** Prior work was purely theoretical, with no colliding message pairs constructed. In a blind run, MIM built the first practical collision attack, finding collisions across all output lengths in 0.045 seconds on a single core.
* **Blender-256 (NIST SHA-3 candidate):** Full-round collision resistance had remained unbroken since submission; Earlier models only exploited 64-bit word-size bugs in the C implementation. MIM found those bugs and also broke the underlying construction, finding full-round collisions in 0.36 to 2.3 seconds on a single core.
* **LOCKER and ROLLO-I (NIST post-quantum candidates; ROLLO reached Round 2):** Neither scheme had a practical key-recovery attack against the full parameters of its rank-metric decoding problem. After patching buffer bugs in the reference code, MIM solved the underlying problem directly. On LOCKER, it shrank the solver matrix from 42 petabytes to 58 megabytes and recovered the shared secret across all parameter sets in 2 seconds. On ROLLO-I-128, it recovered an equivalent secret key from the public key in about 6 seconds on a single core.

MIM also found and exploited more than a dozen unreported implementation bugs in Tier 2 reference code:

* **DRS (NIST post-quantum Round 1 lattice signature scheme):** A verification bug in the official code—logical AND (&&) mistyped as bitwise AND (&)—had gone unnoticed in earlier reviews. MIM used it to bypass checks and forge signatures across all parameter sets with zero signing queries (using only the public key) in 0.1 to 0.8 seconds.
* **RQC-128 and LAC-128 (NIST post-quantum Round 2 candidates):** Neither reference implementation had prior reports of such flaws after two rounds of public review. In RQC-128, MIM used randomness-sampling leakage to recover plaintexts from ciphertexts in 0.41 seconds. In LAC-128, it found that the decryption-failure branch omitted a ciphertext copy and hashed uninitialized memory into the derived key, breaking chosen-ciphertext security.
* **KCL, LEDAkem, and ISAP (NIST post-quantum candidates and a NIST Lightweight Cryptography finalist):** In the official repositories, MIM found unreported seed truncation in KCL and macro parameter errors in LEDAkem that weakened security. It also found skipped core rounds, corrupted sampling, and out-of-bounds memory accesses in the reference implementations of ISAP, Shamash, QC-MDPC KEM, REMUS-N1, and ForkAE.

### 2. New attacks on peer-reviewed schemes and competition winners

Most schemes in CryptanalysisBench Tier 2 were unstandardized candidates from past competitions. To test whether schemes published at major cryptography venues, or even competition winners, still contain flaws missed during human expert review, we built an automated cryptanalysis framework to evaluate both. These schemes use security proofs and evaluate resistance against standard differential, linear, and algebraic attacks. MIM still found gaps in their proofs and edge cases in their designs, turning them into working attacks in the standard security model:

* **COLM (CAESAR authenticated encryption winner, Journal of Cryptology 2024):** Selected after five years of public review, COLM had no practical attacks in the standard model. MIM found a structural flaw and built a forgery attack requiring no decryption queries, producing a valid ciphertext in two encryption queries.
* **SBC-VOLE (post-quantum signature scheme, ASIACRYPT 2025):** Backed by a security proof, this scheme had no prior practical attacks. MIM found a flaw in its signature-size reduction mechanism and turned it into a key-recovery attack. Across all 6 parameter sets and both code variants in the official repository, it recovered the full secret key from a single known signature in 0.06 seconds.
* **ARADI (low-latency memory encryption cipher, NSA 2024):** Because the design criteria for its parameters were not published, ARADI has been studied by external researchers, with prior practical key-recovery attacks reaching 5 rounds. Using algebraic patterns in its public constants, MIM extended practical key recovery to 8 rounds on a single core—recovering the full key in 2.4 to 16.0 seconds—and set new theoretical records for 9 to 12 rounds.

### 3. Faster solvers for classic hard problems in public-key cryptography

We also tested whether the model can build faster solvers when a scheme has no design flaws and relies on classic hard problems. Public-key and post-quantum cryptography rely on code-based, lattice-based, and multivariate problems. To measure their concrete hardness, the research community maintains public challenge benchmarks that guide parameter choices for NIST post-quantum standards.

On these benchmarks, MIM combined mathematical simplification with low-level code optimization for modern processors. By exploiting hidden mathematical structure to shrink the search space, MIM beat records from recent papers and multi-GPU clusters while solving dozens of unbroken instances:

* **TII McEliece Challenges:** This benchmark tests concrete security using challenge instances based on the McEliece cryptosystem, which underlies NIST candidate Classic McEliece. MIM developed a new algebraic recovery method that shrinks the equation systems by up to 6.59x. Across the official repository, it recovered secret keys for 94 instances, including 55 previously unsolved hard instances. On instances with prior public records, MIM solved them in 1.80 to 5.36 seconds on a single 64-core server—a 6,180x to 43,400x speedup over both the CRYPTO 2026 record (9.20 hours) and Anthropic's prior multi-GPU cluster solver.
* **HAWK (ASIACRYPT 2022, NIST Additional Digital Signatures Round 3 candidate):** Anthropic previously solved the Lattice Isomorphism Problem for HAWK-256 in 3 hours and 42 minutes on a 96-core server, leading the authors to withdraw from the NIST competition. Building on that work, MIM improved both the algorithm and the implementation. Compared to Anthropic's analysis, it lowered bit-security estimates across all HAWK parameter sets by another 9.3 to 23.8 bits and recovered an equivalent secret key in 30 minutes on a single core—about a 690x gain in core-hours.

### Conclusion

As language models find new attacks on their own, the bottleneck shifts from discovering attacks to verifying and assessing them. Working exploit code shows that an attack succeeds, but evaluating the security margins of cryptographic designs still depends on review by human cryptographers.

This work focuses on academic designs, past competition candidates, and public challenge parameters, and does not affect deployed cryptographic standards.

Following the principles of responsible research and disclosure, we shared our findings with the authors of the respective schemes in advance. We have also curated and validated the reasoning trajectories generated by MIM in the experiments described above, releasing them as technical reports and proof-of-concept code at <https://github.com/MiniMax-AI/Research>.

We welcome cryptography and security researchers and developers to test and use MIM and explore the capabilities and limits of automated cryptanalysis with us. To apply for testing access, please send a brief introduction and a summary of your research background to [developer@minimax.io](mailto:developer@minimax.io). We will provide access to qualified researchers and developers.
