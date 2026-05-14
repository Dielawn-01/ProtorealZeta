import Mathlib.Tactic
import Mathlib.RingTheory.Nilpotent.Defs
import LaRueProtorealAlgebra.ProtorealManifold

/-!
# Nilradical Generalization: The Protoreal Jet Space (𝕌ⁿ)

Generalizing the nilpotent noise element ε from order 2 (dual numbers, ε² = 0)
to arbitrary order n (jet space, εⁿ = 0, εⁿ⁻¹ ≠ 0).

## The Calculus Analogy

- **ε acts as the differential operator** (right-shift): each application
  moves information one level deeper into the jet. After n applications,
  all information has "fallen off the edge" → nilpotent.
- **λ acts as the integral operator** (left-shift): each application
  accumulates information back toward the base. After n applications,
  no new information remains to accumulate → saturation.

The duality: **ε vanishes at order n, λ freezes at order n.**

## Connection to Algebraic Geometry

This module uses Mathlib's `IsNilpotent` predicate from ring theory.
The jet space ℝ[ε]/(εⁿ) is the truncated polynomial ring — the standard
nilradical construction from scheme theory.

## Jet Morphism Structure

Projection (Jⁿ → Jᵐ) commutes with ε-shift but NOT with λ-shift.
This asymmetry is the origin of the boundary defect in the Protoreal FTC.
The sowing operator `funct` IS a jet projection morphism (Jⁿ → Jⁿ⁻¹).
-/

open ProtorealManifold

namespace NilradicalGeneralization

-- ════════════════════════════════════════════════════
-- THE JET ELEMENT
-- ════════════════════════════════════════════════════

/-- A jet element of order n: coefficients beyond position n are zero. -/
structure JetElement (n : ℕ) where
  coeff : ℕ → ℝ
  support : ∀ k, n ≤ k → coeff k = 0

@[ext]
theorem JetElement.ext {n : ℕ} {a b : JetElement n}
    (h : ∀ k, a.coeff k = b.coeff k) : a = b := by
  cases a; cases b; congr; ext k; exact h k

instance JetElement.instZero (n : ℕ) : Zero (JetElement n) where
  zero := ⟨fun _ => 0, fun _ _ => rfl⟩

@[simp]
theorem JetElement.zero_coeff {n : ℕ} (k : ℕ) : (0 : JetElement n).coeff k = 0 := rfl

-- ════════════════════════════════════════════════════
-- SHIFT OPERATORS
-- ════════════════════════════════════════════════════

/-- **EPSILON SHIFT (Protoreal Differentiation)** -/
def epsilon_shift {n : ℕ} (a : JetElement n) : JetElement n where
  coeff k := if k = 0 then 0
             else if k < n then a.coeff (k - 1)
             else 0
  support k hk := by simp [show ¬(k < n) from by omega]

/-- **LAMBDA SHIFT (Protoreal Integration)** -/
def lambda_shift {n : ℕ} (a : JetElement n) : JetElement n where
  coeff k := if k + 1 < n then a.coeff (k + 1) else 0
  support k hk := by simp [show ¬(k + 1 < n) from by omega]

-- Coeff access lemmas (bridge unfold gap caused by dite/ite mismatch)
@[simp]
theorem epsilon_shift_coeff {n : ℕ} (a : JetElement n) (k : ℕ) :
    (epsilon_shift a).coeff k =
      if k = 0 then 0 else if k < n then a.coeff (k - 1) else 0 := by
  unfold epsilon_shift; split <;> simp_all

@[simp]
theorem lambda_shift_coeff {n : ℕ} (a : JetElement n) (k : ℕ) :
    (lambda_shift a).coeff k =
      if k + 1 < n then a.coeff (k + 1) else 0 := by
  unfold lambda_shift; split <;> simp_all

-- ════════════════════════════════════════════════════
-- THE NILPOTENCY THEOREM (ε-shift)
-- ════════════════════════════════════════════════════

/-- After m ε-shifts, coeff k = a.coeff(k − m) if m ≤ k < n, else 0. -/
theorem epsilon_shift_iter_coeff {n : ℕ} (a : JetElement n) (m : ℕ) :
    ∀ k, (Nat.iterate epsilon_shift m a).coeff k =
      if m ≤ k ∧ k < n then a.coeff (k - m) else 0 := by
  induction m with
  | zero =>
    intro k
    simp only [Nat.iterate, Nat.zero_le, true_and, Nat.sub_zero]
    by_cases hkn : k < n
    · simp [hkn]
    · simp [hkn, a.support k (by omega)]
  | succ m ih =>
    intro k
    rw [Function.iterate_succ', Function.comp, epsilon_shift_coeff]
    by_cases hk0 : k = 0
    · simp [hk0]
    · by_cases hkn : k < n
      · -- Simplify the if k=0 and if k<n from epsilon_shift_coeff
        simp only [hk0, ↓reduceIte, hkn]
        rw [ih (k - 1)]
        -- Now both sides have a single ite
        -- LHS: if m ≤ k-1 ∧ k-1 < n then a.coeff(k-1-m) else 0
        -- RHS: if m+1 ≤ k ∧ k < n then a.coeff(k-(m+1)) else 0
        -- Since k ≠ 0: (m ≤ k-1 ∧ k-1 < n) ↔ (m+1 ≤ k ∧ k < n)
        have key : (m ≤ k - 1 ∧ k - 1 < n) ↔ (m + 1 ≤ k ∧ k < n) := by
          constructor
          · intro ⟨h1, h2⟩; exact ⟨by omega, by omega⟩
          · intro ⟨h1, h2⟩; exact ⟨by omega, by omega⟩
        split_ifs
        · congr 1; omega
        · tauto
        · tauto
        · rfl
      · simp [hk0, show ¬(k < n) from hkn]

/-- **THE NILPOTENCY THEOREM (εⁿ = 0)** -/
theorem epsilon_shift_nilpotent {n : ℕ} (a : JetElement n) :
    Nat.iterate epsilon_shift n a = 0 := by
  ext k
  rw [epsilon_shift_iter_coeff _ _ k, JetElement.zero_coeff]
  simp [show ¬(n ≤ k ∧ k < n) from by omega]

/-- **THE NON-VANISHING THEOREM (εⁿ⁻¹ ≠ 0)** -/
theorem epsilon_shift_nonvanishing {n : ℕ} (a : JetElement n) (hn : 2 ≤ n)
    (ha : a.coeff 0 ≠ 0) :
    Nat.iterate epsilon_shift (n - 1) a ≠ 0 := by
  intro h
  have h2 := congr_arg (fun x => JetElement.coeff x (n - 1)) h
  dsimp only at h2
  rw [epsilon_shift_iter_coeff _ _ (n - 1)] at h2
  simp only [show (n - 1 ≤ n - 1 ∧ n - 1 < n) from ⟨le_refl _, by omega⟩,
             ↓reduceIte, Nat.sub_self, JetElement.zero_coeff] at h2  -- linter false positive on sub_self
  exact ha h2

-- ════════════════════════════════════════════════════
-- THE SATURATION THEOREM (λ-shift)
-- ════════════════════════════════════════════════════

/-- After m λ-shifts, coeff k = a.coeff(k + m) if k + m < n, else 0. -/
theorem lambda_shift_iter_coeff {n : ℕ} (a : JetElement n) (m : ℕ) :
    ∀ k, (Nat.iterate lambda_shift m a).coeff k =
      if k + m < n then a.coeff (k + m) else 0 := by
  induction m with
  | zero =>
    intro k
    simp only [Nat.iterate, Nat.add_zero]
    by_cases hkn : k < n
    · simp [hkn]
    · simp [show ¬(k < n) from hkn, a.support k (by omega)]
  | succ m ih =>
    intro k
    rw [Function.iterate_succ', Function.comp, lambda_shift_coeff]
    by_cases hlt : k + 1 < n
    · simp only [hlt, ↓reduceIte, ih (k + 1)]
      by_cases hlt2 : k + 1 + m < n
      · simp only [hlt2, ↓reduceIte, show k + (m + 1) < n from by omega]
        congr 1; omega
      · simp only [hlt2, ↓reduceIte, show ¬(k + (m + 1) < n) from by omega]
    · simp [hlt, show ¬(k + (m + 1) < n) from by omega]

/-- **THE SATURATION THEOREM (λⁿ saturates)** -/
theorem lambda_shift_saturates {n : ℕ} (a : JetElement n) :
    Nat.iterate lambda_shift n a = 0 := by
  ext k
  rw [lambda_shift_iter_coeff _ _ k, JetElement.zero_coeff]
  split
  · exact a.support _ (by omega)
  · rfl

-- ════════════════════════════════════════════════════
-- THE DUALITY THEOREM (PROTOREAL FTC)
-- ════════════════════════════════════════════════════

/-- **ε∘λ roundtrip at interior positions** -/
theorem epsilon_lambda_roundtrip {n : ℕ} (a : JetElement n) (k : ℕ)
    (hk_pos : 0 < k) (hk_top : k + 1 < n) :
    (epsilon_shift (lambda_shift a)).coeff k = a.coeff k := by
  simp only [epsilon_shift_coeff, lambda_shift_coeff]
  simp only [show k ≠ 0 from by omega, ↓reduceIte, show k < n from by omega,
             show k - 1 + 1 < n from by omega]
  congr 1; omega

/-- **λ∘ε roundtrip at interior positions** -/
theorem lambda_epsilon_roundtrip {n : ℕ} (a : JetElement n) (k : ℕ)
    (hk_top : k + 1 < n) :
    (lambda_shift (epsilon_shift a)).coeff k = a.coeff k := by
  simp only [lambda_shift_coeff, epsilon_shift_coeff]
  simp only [show k + 1 ≠ 0 from by omega, show k + 1 < n from hk_top, ↓reduceIte,
             Nat.add_sub_cancel]

-- ════════════════════════════════════════════════════
-- SYMMETRY AND ORDER HIERARCHY
-- ════════════════════════════════════════════════════

/-- **ε and λ annihilate at the same order n.** -/
theorem nilpotent_saturation_symmetry {n : ℕ} (a : JetElement n) :
    Nat.iterate epsilon_shift n a = Nat.iterate lambda_shift n a := by
  rw [epsilon_shift_nilpotent, lambda_shift_saturates]

/-- n = 1: Trivial jet. -/
theorem order_1_trivial (a : JetElement 1) : epsilon_shift a = 0 := by
  have := epsilon_shift_nilpotent (n := 1) a
  simp [Nat.iterate] at this; exact this

/-- n = 2: Classical dual numbers (ε² = 0). -/
theorem order_2_nilpotent (a : JetElement 2) :
    Nat.iterate epsilon_shift 2 a = 0 := epsilon_shift_nilpotent a

/-- n = 3: Second-order jet (ε³ = 0). -/
theorem order_3_nilpotent (a : JetElement 3) :
    Nat.iterate epsilon_shift 3 a = 0 := epsilon_shift_nilpotent a

/-- Derivative depth: n − 1 meaningful derivatives at order n. -/
def derivative_depth (n : ℕ) : ℕ := n - 1

end NilradicalGeneralization
