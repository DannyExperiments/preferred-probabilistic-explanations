# Problem and proof outline

The input and preferred-solution quantifiers are those of Definitions 23 and 24. Membership in Π₂ᴾ is Theorem 11(2). The remaining lower bound addresses §7. [Source](https://proceedings.kr.org/2026/30/kr2026-0030-flaminio-et-al.pdf#page=10)

## One assessment

Start from the complement of a quantified formula ∃X∀Y F(X,Y). A fallback literal s always entails the observation. Put probability 2/3 on a satisfiable event that sets every selector true and s false. The theory requires exactly one selector per pair. A coherent measure uses its remaining 1/3 to witness positivity for any theory-consistent partial assignment. Every selector-only term beats the fallback in all coherent measures. It is a solution exactly when all completions of its induced partial assignment and all universal values satisfy F. Terms containing s cannot beat it.

## Listed support

The fallback point has mass (n−1)/(3n−1), and 2n more points each omit just one selector and have mass 1/(3n−1). A nonempty term with m selectors has mass (2n−m)/(3n−1), so a better term uses at most n. Entailment requires each pair to contribute at least one selector. With exactly one per pair, every valuation either triggers a guard or yields the exact chosen assignment with free universal variables. The two constructions both reduce quantified falsity to preferred recognition. The [explicit-support supplement](explicit-support-supplement.zip) contains the supporting proof and original verification code.

## Bounded support

For fixed maximum support k, saturate each qualifying subset of points by taking all literals common to them. It suffices to test these terms for entailment. Countervaluations certify absence of a better solution. Candidate validity is in coNP. A two-point SAT–UNSAT reduction gives DP-completeness, with NP-completeness when validity is promised. At one point preference and ordinary recognition coincide.

[Complete arguments](../paper/manuscript.pdf)
