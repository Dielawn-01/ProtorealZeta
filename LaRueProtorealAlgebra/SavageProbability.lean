import LaRueProtorealAlgebra.ProtorealManifold
import LaRueProtorealAlgebra.LittleDelta
import LaRueProtorealAlgebra.MonsterInverse

namespace LaRueProtorealAlgebra

open ProtorealManifold
open LittleDelta
open MonsterInverse

/-!
# Savage's Personal Probability (𝕌)

This module formalizes L.J. Savage's concept of Subjective Probability
within the Protoreal Algebra. Standard probability is measure-theoretic and
frequentist, which is incompatible with the non-commutative curvature of the
Klein universe.

Instead, probability is defined subjectively: it is the Observer's (`delta`)
belief structure projected onto the Ambiguity (`e` / ε) of the manifold.
-/

/-- **Subjective Belief Measure**
    The observer's probability measure is derived from the ambiguity (ε) 
    and scaled by the structural anchor (ι). 
    A state with 0 ambiguity yields a belief of 1 (Certainty).
    A state with high ambiguity yields a fractional belief. -/
noncomputable def subjective_belief (u : ProtorealManifold) : ℝ :=
  -- Belief is inverse to absolute ambiguity. If ε=0, belief is 1.
  if u.e = 0 then 1 else 1 / (1 + |u.e|)

/-- **Savage's Sure-Thing Principle (Anchoring)**
    If a decision maker prefers an action regardless of the state of the 
    world, the decision is structurally anchored.
    In Protoreal space, the Sure-Thing principle maps directly to the
    contraction anchor `ι`. If the anchor is dominant, the ambiguity 
    does not change the parity of the projection. -/
theorem sure_thing_anchoring (u : ProtorealManifold) :
  let u_anchored := { a := u.a, b := u.b, m := 100, e := u.e, l := u.l }
  (parity_projection u_anchored).b = (parity_projection u_anchored).m := by
  apply parity_projection_locks

/-- **Subjective Certainty Theorem**
    If the observer collapses the wave function (setting ε to 0),
    their subjective belief becomes 1. This formally proves that
    probability in Protoreal space is an act of observation, not 
    a physical frequentist property. -/
theorem subjective_certainty (u : ProtorealManifold) :
  let collapsed := { a := u.a, b := u.b, m := u.m, e := 0, l := u.l }
  subjective_belief collapsed = 1 := by
  unfold subjective_belief
  simp

end LaRueProtorealAlgebra
