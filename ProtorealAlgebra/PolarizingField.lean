import LaRueProtorealAlgebra.ProtorealManifold

/-!
# Polarizing Fields (𝕌)
Formalizing the parity and polarization of manifold states.
-/

open ProtorealManifold

/-- Parity State:
    Represents the orientation of a manifold sector. -/
inductive Parity where
  | Positive : Parity
  | Negative : Parity
  | Neutral : Parity

/-- **THE POLARIZING FIELD**
    Maps a manifold state into its primary parity.
    Locked to the Thrust (b) sector. -/
noncomputable def field (u : ProtorealManifold) : Parity :=
  if u.b > 0 then Parity.Positive
  else if u.b < 0 then Parity.Negative
  else Parity.Neutral

namespace PolarizingField

/-- **POLARIZATION FLIP**
    The R4 reflection flips the parity of the manifold. -/
theorem field_polarization_flip (u : ProtorealManifold) :
    u.b ≠ 0 → field (R4 u) ≠ field u := by
  intro hne
  rcases lt_or_gt_of_ne hne with h | h
  · -- u.b < 0, so -u.b > 0
    unfold field R4
    simp only
    have h1 : ¬(u.b > 0) := not_lt.mpr (le_of_lt h)
    have h2 : -u.b > 0 := neg_pos.mpr h
    have h3 : ¬(-u.b < 0) := not_lt.mpr (le_of_lt h2)
    rw [if_pos h2, if_neg h1, if_pos h]
    exact Parity.noConfusion
  · -- u.b > 0, so -u.b < 0
    unfold field R4
    simp only
    have h1 : -u.b < 0 := by linarith
    have h2 : ¬(-u.b > 0) := not_lt.mpr (le_of_lt h1)
    rw [if_neg h2, if_pos h1, if_pos h]
    exact Parity.noConfusion

end PolarizingField
