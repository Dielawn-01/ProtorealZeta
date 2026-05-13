import Mathlib.Analysis.Real.Hyperreal

/-!
# Protoreal Ring Axioms — Hyperreal Foundation

Built directly on Mathlib's Hyperreal field ℝ*.
No saturation. No potency. Just the Bridge and ordering.

## Core Elements
- omega_u := Hyperreal.omega (the canonical transfinite)
- iota_u := -omega_u⁻¹ (the infinitesimal anchor)

## The One True Axiom
omega_u · iota_u = -1 (The Bridge Identity — a THEOREM, not an axiom)

## Ordering (preserved, not flattened)
⋯ > ω³ > ω² > ω > r > 0 > ι > ι² > ⋯
-/

open Hyperreal

namespace Protoreal

-- ════════════════════════════════════════════════════
-- Core Definitions
-- ════════════════════════════════════════════════════

/-- The transfinite thrust: lim(eˣ) as x → ∞ -/
noncomputable def omega_u : ℝ* := Hyperreal.omega

/-- The infinitesimal anchor: -1/ω -/
noncomputable def iota_u : ℝ* := -omega_u⁻¹

-- ════════════════════════════════════════════════════
-- The Bridge Identity (PROVEN)
-- ════════════════════════════════════════════════════

/-- omega is nonzero. Required for the bridge. -/
theorem omega_ne_zero : omega_u ≠ 0 := ne_of_gt Hyperreal.omega_pos

/-- **The Bridge Identity**: ω · ι = -1.
    This is the fundamental contraction. NOT an axiom — a theorem
    following directly from ι := -ω⁻¹ and field arithmetic. -/
theorem bridge : omega_u * iota_u = -1 := by
  change omega_u * (-omega_u⁻¹) = -1
  field_simp [omega_ne_zero]

/-- The reverse bridge: ι · ω = -1.
    In the commutative Hyperreal field, both orderings give -1. -/
theorem bridge_rev : iota_u * omega_u = -1 := by
  rw [mul_comm, bridge]

-- ════════════════════════════════════════════════════
-- Ordering Lemmas (The Transfinite Hierarchy)
-- ════════════════════════════════════════════════════

/-- ω is strictly positive. -/
theorem omega_pos : (0 : ℝ*) < omega_u := Hyperreal.omega_pos

/-- ι is strictly negative (it's -1/ω where ω > 0). -/
theorem iota_neg : iota_u < 0 := by
  unfold iota_u
  simp only [neg_lt_zero]
  exact inv_pos_of_pos omega_pos

/-- ω > 1 (omega is infinite, hence greater than any finite real). -/
theorem omega_gt_one : (1 : ℝ*) < omega_u := by
  unfold omega_u
  exact Hyperreal.coe_lt_omega 1

/-- **ω² > ω**: The transfinite hierarchy is strictly increasing.
    Proof: Since ω > 1, multiplying both sides by ω gives ω² > 1·ω = ω. -/
theorem omega_sq_gt : omega_u * omega_u > omega_u := by
  have h1 : omega_u > 1 := omega_gt_one
  nlinarith [omega_pos]

/-- ι² is positive (negative × negative). -/
theorem iota_sq_pos : 0 < iota_u * iota_u := by
  exact mul_pos_of_neg_of_neg iota_neg iota_neg

/-- **ι² < |ι|**: Infinitesimals get strictly smaller when squared.
    Since |ι| = ω⁻¹ and ι² = ω⁻², and ω > 1, we have ω⁻² < ω⁻¹. -/
theorem iota_sq_lt_abs : iota_u * iota_u < |iota_u| := by
  unfold iota_u
  rw [neg_mul_neg, abs_neg, abs_of_pos (inv_pos_of_pos omega_pos)]
  rw [← mul_inv]
  rw [inv_lt_inv₀ (mul_pos omega_pos omega_pos) omega_pos]
  exact omega_sq_gt

-- ════════════════════════════════════════════════════
-- Higher Powers: The Full Hierarchy
-- ════════════════════════════════════════════════════

/-- ω^n > any real number, for n ≥ 1. -/
theorem omega_pow_gt_real (n : ℕ) (hn : 0 < n) (r : ℝ) :
    (r : ℝ*) < omega_u ^ n := by
  calc (r : ℝ*) < omega_u := by unfold omega_u; exact Hyperreal.coe_lt_omega r
    _ = omega_u ^ 1 := (pow_one omega_u).symm
    _ ≤ omega_u ^ n := by
        exact pow_le_pow_right₀ (le_of_lt omega_gt_one) hn

/-- ω is infinite (as defined in Hyperreal). -/
theorem omega_infinite : Hyperreal.Infinite omega_u :=
  (Hyperreal.infinite_iff_infinitesimal_inv Hyperreal.omega_ne_zero).mpr Hyperreal.infinitesimal_epsilon

/-- ι is non-zero (since its inverse is infinite). -/
theorem iota_ne_zero : iota_u ≠ 0 := by
  intro h
  have h_inv := bridge
  rw [h, mul_zero] at h_inv
  norm_num at h_inv

end Protoreal
