import LaRueProtorealAlgebra.Uncomplex

namespace LaRueProtorealAlgebra

open ProtorealManifold
open Uncomplex

/-!
# Temporal Morphism (𝕌)

This module formalizes the transformation between a standard Time Series
Autoregressive Model (e.g., TimesFM) and the Protoreal Manifold.

In standard physics and ML, time is modeled as an irreversible sequence:
t_0 → t_1 → t_2.

In the Protoreal (Connes-Wiener) algebra, **causality is strictly encoded
as non-commutativity** (A · B ≠ B · A). We formalize the "arrow of time"
as the repeated right-multiplication by the thrust component `ω`.
-/

/-- **The Temporal Step Operator**
    Advances the manifold one time step by applying the autoregressive
    thrust `ω`. -/
def time_step (u : ProtorealManifold) : ProtorealManifold :=
  u * omega

/-- **Temporal Evolution Sequence**
    Recursive application of the time step for n steps. -/
def time_evolution : ℕ → ProtorealManifold → ProtorealManifold
  | 0, u => u
  | n + 1, u => time_step (time_evolution n u)

/-- **The Arrow of Time is Irreversible (Causal Gap)**
    Because the algebra is non-associative and non-commutative, you cannot
    reverse time simply by multiplying by the "inverse" of thrust without
    experiencing the curvature gap (κ = -1).

    Specifically, stepping forward with ω, and then trying to anchor back
    with ι yields a different state than anchoring first and then stepping.
    (u · ω) · ι ≠ u · (ω · ι)
-/
theorem time_arrow_irreversible :
  ∃ v : ProtorealManifold, (v * omega) * iota ≠ v * (omega * iota) := by
  use omega
  exact manifold_stability

/-- **Temporal Idempotence in the Void**
    If there is no anchor (ι = 0) and no noise (ε = 0), thrusting forward
    in pure time is idempotent: stepping once is the same as stepping twice
    in terms of state. It's only when interacting with the rest of the
    manifold that time creates complexity. -/
theorem time_idempotent_in_void :
  time_step omega = omega := by
  unfold time_step omega
  ext <;> simp

end LaRueProtorealAlgebra
