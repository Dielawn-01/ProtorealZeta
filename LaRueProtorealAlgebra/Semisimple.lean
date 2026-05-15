import LaRueProtorealAlgebra.ProtorealManifold

/-!
# Semisimple Decomposition (𝕌)
Proving that the Protoreal Ring admits a semisimple decomposition
into 5 orthogonal idempotent projections, one per basis component.

## Key Results
- Each projection πₖ extracts a single component
- Projections are idempotent: πₖ ∘ πₖ = πₖ
- Projections are orthogonal: πⱼ ∘ πₖ = 0 for j ≠ k
- Projections are complete: Σ πₖ = id
-/

open ProtorealManifold

namespace Semisimple

-- ════════════════════════════════════════════════════
-- THE FIVE PROJECTIONS
-- ════════════════════════════════════════════════════

/-- Projection onto the real (a) component. -/
def π_a (u : ProtorealManifold) : ProtorealManifold :=
  { a := u.a, b := 0, m := 0, e := 0, l := 0 }

/-- Projection onto the thrust (ω) component. -/
def π_ω (u : ProtorealManifold) : ProtorealManifold :=
  { a := 0, b := u.b, m := 0, e := 0, l := 0 }

/-- Projection onto the anchor (ι) component. -/
def π_ι (u : ProtorealManifold) : ProtorealManifold :=
  { a := 0, b := 0, m := u.m, e := 0, l := 0 }

/-- Projection onto the noise (ε) component. -/
def π_ε (u : ProtorealManifold) : ProtorealManifold :=
  { a := 0, b := 0, m := 0, e := u.e, l := 0 }

/-- Projection onto the level (λ) component. -/
def π_l (u : ProtorealManifold) : ProtorealManifold :=
  { a := 0, b := 0, m := 0, e := 0, l := u.l }

-- ════════════════════════════════════════════════════
-- IDEMPOTENCY: πₖ ∘ πₖ = πₖ
-- ════════════════════════════════════════════════════

theorem π_a_idempotent (u : ProtorealManifold) :
    π_a (π_a u) = π_a u := by
  unfold π_a; ext <;> simp

theorem π_ω_idempotent (u : ProtorealManifold) :
    π_ω (π_ω u) = π_ω u := by
  unfold π_ω; ext <;> simp

theorem π_ι_idempotent (u : ProtorealManifold) :
    π_ι (π_ι u) = π_ι u := by
  unfold π_ι; ext <;> simp

theorem π_ε_idempotent (u : ProtorealManifold) :
    π_ε (π_ε u) = π_ε u := by
  unfold π_ε; ext <;> simp

theorem π_l_idempotent (u : ProtorealManifold) :
    π_l (π_l u) = π_l u := by
  unfold π_l; ext <;> simp

-- ════════════════════════════════════════════════════
-- ORTHOGONALITY: πⱼ ∘ πₖ = 0 for j ≠ k
-- ════════════════════════════════════════════════════

theorem π_a_ω_orthogonal (u : ProtorealManifold) :
    π_a (π_ω u) = 0 := by unfold π_a π_ω; ext <;> simp

theorem π_a_ι_orthogonal (u : ProtorealManifold) :
    π_a (π_ι u) = 0 := by unfold π_a π_ι; ext <;> simp

theorem π_a_ε_orthogonal (u : ProtorealManifold) :
    π_a (π_ε u) = 0 := by unfold π_a π_ε; ext <;> simp

theorem π_a_l_orthogonal (u : ProtorealManifold) :
    π_a (π_l u) = 0 := by unfold π_a π_l; ext <;> simp

theorem π_ω_a_orthogonal (u : ProtorealManifold) :
    π_ω (π_a u) = 0 := by unfold π_ω π_a; ext <;> simp

theorem π_ω_ι_orthogonal (u : ProtorealManifold) :
    π_ω (π_ι u) = 0 := by unfold π_ω π_ι; ext <;> simp

theorem π_ω_ε_orthogonal (u : ProtorealManifold) :
    π_ω (π_ε u) = 0 := by unfold π_ω π_ε; ext <;> simp

theorem π_w_l_orthogonal (u : ProtorealManifold) :
    π_ω (π_l u) = 0 := by unfold π_ω π_l; ext <;> simp

theorem π_ι_a_orthogonal (u : ProtorealManifold) :
    π_ι (π_a u) = 0 := by unfold π_ι π_a; ext <;> simp

theorem π_ι_ω_orthogonal (u : ProtorealManifold) :
    π_ι (π_ω u) = 0 := by unfold π_ι π_ω; ext <;> simp

theorem π_ι_ε_orthogonal (u : ProtorealManifold) :
    π_ι (π_ε u) = 0 := by unfold π_ι π_ε; ext <;> simp

theorem π_i_l_orthogonal (u : ProtorealManifold) :
    π_ι (π_l u) = 0 := by unfold π_ι π_l; ext <;> simp

theorem π_ε_a_orthogonal (u : ProtorealManifold) :
    π_ε (π_a u) = 0 := by unfold π_ε π_a; ext <;> simp

theorem π_ε_ω_orthogonal (u : ProtorealManifold) :
    π_ε (π_ω u) = 0 := by unfold π_ε π_ω; ext <;> simp

theorem π_ε_ι_orthogonal (u : ProtorealManifold) :
    π_ε (π_ι u) = 0 := by unfold π_ε π_ι; ext <;> simp

theorem π_e_l_orthogonal (u : ProtorealManifold) :
    π_ε (π_l u) = 0 := by unfold π_ε π_l; ext <;> simp

theorem π_l_a_orthogonal (u : ProtorealManifold) :
    π_l (π_a u) = 0 := by unfold π_l π_a; ext <;> simp

theorem π_l_ω_orthogonal (u : ProtorealManifold) :
    π_l (π_ω u) = 0 := by unfold π_l π_ω; ext <;> simp

theorem π_l_ι_orthogonal (u : ProtorealManifold) :
    π_l (π_ι u) = 0 := by unfold π_l π_ι; ext <;> simp

theorem π_l_ε_orthogonal (u : ProtorealManifold) :
    π_l (π_ε u) = 0 := by unfold π_l π_ε; ext <;> simp

-- ════════════════════════════════════════════════════
-- COMPLETENESS: Σ πₖ = id
-- ════════════════════════════════════════════════════

/-- **SEMISIMPLE DECOMPOSITION THEOREM**
    Every Protoreal element decomposes uniquely as the sum
    of its 5 orthogonal projections. -/
theorem completeness (u : ProtorealManifold) :
    π_a u + π_ω u + π_ι u + π_ε u + π_l u = u := by
  unfold π_a π_ω π_ι π_ε π_l
  ext <;> simp [Add.add] <;> ring

end Semisimple
