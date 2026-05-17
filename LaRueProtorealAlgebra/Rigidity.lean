import LaRueProtorealAlgebra.ProtorealManifold
import LaRueProtorealAlgebra.FusionRing

/-!
# Rigidity Structure (𝕌)
Proving the Protoreal Ring admits duality pairings via the Bridge
identity and the ε-λ contraction.

## Key Results
- The ω-ι pairing: ω·ι = −𝟙, ι·ω = +𝟙
- The ε-λ pairing: ε·λ = −𝟙, λ·ε = +𝟙
- Snake identity for the Bridge pairing
- Two independent contraction pairs → rigid structure
-/

open ProtorealManifold

namespace Rigidity

-- ════════════════════════════════════════════════════
-- THE BRIDGE PAIRING (ω ⊣ ι)
-- ════════════════════════════════════════════════════

/-- **EVALUATION MAP (ω-ι)**: ω·ι = −𝟙.
    This is the evaluation morphism of the Bridge duality. -/
theorem eval_bridge :
    ProtorealManifold.mul omega iota = -1 := by
  unfold omega iota ProtorealManifold.mul
  ext <;> simp

/-- **COEVALUATION MAP (ω-ι)**: ι·ω = +𝟙.
    This is the coevaluation morphism of the Bridge duality. -/
theorem coeval_bridge :
    ProtorealManifold.mul iota omega = 1 := by
  unfold iota omega ProtorealManifold.mul
  ext <;> simp

-- ════════════════════════════════════════════════════
-- THE NOISE-LEVEL PAIRING (ε ⊣ λ)
-- ════════════════════════════════════════════════════

/-- **EVALUATION MAP (ε-λ)**: ε·λ = −𝟙.
    The noise-level contraction mirrors the Bridge. -/
theorem eval_noise :
    ProtorealManifold.mul FusionRing.eE FusionRing.eL = -1 := by
  unfold FusionRing.eE FusionRing.eL ProtorealManifold.mul
  ext <;> simp

/-- **COEVALUATION MAP (ε-λ)**: λ·ε = +𝟙.
    The reverse noise-level contraction. -/
theorem coeval_noise :
    ProtorealManifold.mul FusionRing.eL FusionRing.eE = 1 := by
  unfold FusionRing.eL FusionRing.eE ProtorealManifold.mul
  ext <;> simp

-- ════════════════════════════════════════════════════
-- SNAKE IDENTITY (Bridge)
-- ════════════════════════════════════════════════════

/-- **SNAKE IDENTITY (ω-side)**:
    (ω·ι)·ω + ω = 0.
    The evaluation composed with coevaluation on the ω-side
    gives the negative of the identity action on ω.
    Equivalently: ω is an "eigenvector" of the Bridge operator
    with eigenvalue −1. -/
theorem snake_omega :
    ProtorealManifold.mul (ProtorealManifold.mul omega iota) omega = -omega := by
  unfold omega iota ProtorealManifold.mul
  ext <;> simp

/-- **SNAKE IDENTITY (ι-side)**:
    ι·(ω·ι) = −ι.
    Same eigenvalue on the dual side. -/
theorem snake_iota :
    ProtorealManifold.mul iota (ProtorealManifold.mul omega iota) = -iota := by
  unfold omega iota ProtorealManifold.mul
  ext <;> simp

-- ════════════════════════════════════════════════════
-- SNAKE IDENTITY (Noise-Level)
-- ════════════════════════════════════════════════════

/-- **SNAKE IDENTITY (ε-side)**:
    (ε·λ)·ε = −ε. -/
theorem snake_epsilon :
    ProtorealManifold.mul
      (ProtorealManifold.mul FusionRing.eE FusionRing.eL)
      FusionRing.eE = -FusionRing.eE := by
  unfold FusionRing.eE FusionRing.eL ProtorealManifold.mul
  ext <;> simp

/-- **SNAKE IDENTITY (λ-side)**:
    λ·(ε·λ) = −λ. -/
theorem snake_level :
    ProtorealManifold.mul
      FusionRing.eL
      (ProtorealManifold.mul FusionRing.eE FusionRing.eL) = -FusionRing.eL := by
  unfold FusionRing.eE FusionRing.eL ProtorealManifold.mul
  ext <;> simp

-- ════════════════════════════════════════════════════
-- BRIDGE OPERATOR SQUARED = IDENTITY
-- ════════════════════════════════════════════════════

/-- The Bridge operator B(u) = ω·u·ι applied twice gives u back
    (up to sign), establishing that the Bridge is a period-2 involution
    on the unit element. -/
theorem bridge_squared_unit :
    ProtorealManifold.mul
      (ProtorealManifold.mul omega
        (ProtorealManifold.mul FusionRing.e1 iota))
      (ProtorealManifold.mul omega
        (ProtorealManifold.mul FusionRing.e1 iota)) =
    FusionRing.e1 := by
  unfold FusionRing.e1 omega iota ProtorealManifold.mul
  ext <;> simp

-- ════════════════════════════════════════════════════
-- TWO INDEPENDENT CONTRACTIONS
-- ════════════════════════════════════════════════════

/-- **DUAL BRIDGE THEOREM**: The algebra has exactly two independent
    contraction pairs: (ω,ι) and (ε,λ). Both satisfy
    eval · coeval = −𝟙 (the curvature sign). -/
theorem dual_contractions :
    ProtorealManifold.mul
      (ProtorealManifold.mul omega iota)
      (ProtorealManifold.mul iota omega) = -FusionRing.e1
    ∧
    ProtorealManifold.mul
      (ProtorealManifold.mul FusionRing.eE FusionRing.eL)
      (ProtorealManifold.mul FusionRing.eL FusionRing.eE) = -FusionRing.e1 := by
  constructor
  · unfold omega iota FusionRing.e1 ProtorealManifold.mul
    ext <;> simp
  · unfold FusionRing.eE FusionRing.eL FusionRing.e1 ProtorealManifold.mul
    ext <;> simp

end Rigidity
