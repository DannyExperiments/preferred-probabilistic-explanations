# Lean certificate

**Support saturation**

A heavier term with a supported theory witness and entailment throughout the theory exists exactly when a heavier subset of the support has such a witness and its common-literal closure entails the observation throughout the theory. The weight threshold is modeled by an upward-closed predicate.

The support-size complexity bounds and hardness constructions are proved in the paper.

The principal checked declaration is `SupportSaturation.better_iff_saturation`. See [Fixed support size](../paper/manuscript.tex#L73) in the manuscript. [Lean source](Q800.lean) · [Verification workflow](../.github/workflows/lean.yml)

Replay with Lean 4.30.0 and its standard library from the repository root.

```sh
lean -DwarningAsError=true formalization/Q800.lean
```
