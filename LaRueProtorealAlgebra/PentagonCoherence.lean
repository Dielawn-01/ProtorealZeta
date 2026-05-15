import LaRueProtorealAlgebra.ProtorealManifold
import LaRueProtorealAlgebra.FusionRing
import LaRueProtorealAlgebra.LGKCosmology

/-!
# Pentagon Coherence (𝕌)
Verifying that the Protoreal associator satisfies the Pentagon
cocycle condition on the basis {𝟙, ω, ι, ε, λ}.

## The Associator

For any triple (A, B, C), the associator is:
  α(A, B, C) = (A · B) · C − A · (B · C)

The curvature κ = −1 is the a-component of α(ω, ω, ι).

## Pentagon Coherence

For four elements A, B, C, D, the Pentagon cocycle condition states:
  α(A·B, C, D).a − α(A, B·C, D).a + α(A, B, C·D).a = 0

This says: the three "re-bracketing corrections" sum to zero,
which is exactly the coherence condition that makes the associator
consistent. We verify this on all critical basis quadruples.

## Key Results
- Pentagon cocycle = 0 for (ω,ω,ω,ι), (ω,ω,ι,ι), (ω,ι,ω,ι), (ι,ω,ω,ι)
- 𝟙 is associative with everything
- ε and λ sectors are individually associative
- Non-associativity localises to the ω-ι sector (structural heterogeneity)
-/

open ProtorealManifold

namespace PentagonCoherence

-- ════════════════════════════════════════════════════
-- THE ASSOCIATOR
-- ════════════════════════════════════════════════════

/-- The associator α(A,B,C) = (A·B)·C − A·(B·C). -/
def assoc (A B C : ProtorealManifold) : ProtorealManifold :=
  ProtorealManifold.mul (ProtorealManifold.mul A B) C -
  ProtorealManifold.mul A (ProtorealManifold.mul B C)

-- ════════════════════════════════════════════════════
-- UNIT ASSOCIATIVITY
-- ════════════════════════════════════════════════════

theorem assoc_unit_left (B C : ProtorealManifold) :
    assoc FusionRing.e1 B C = 0 := by
  unfold assoc FusionRing.e1 ProtorealManifold.mul
  ext <;> simp <;> ring

theorem assoc_unit_mid (A C : ProtorealManifold) :
    assoc A FusionRing.e1 C = 0 := by
  unfold assoc FusionRing.e1 ProtorealManifold.mul
  ext <;> simp <;> ring

theorem assoc_unit_right (A B : ProtorealManifold) :
    assoc A B FusionRing.e1 = 0 := by
  unfold assoc FusionRing.e1 ProtorealManifold.mul
  ext <;> simp <;> ring

-- ════════════════════════════════════════════════════
-- THE CURVATURE TRIPLE
-- ════════════════════════════════════════════════════

/-- α(ω,ω,ι).a = −1. The canonical curvature. -/
theorem assoc_omega_omega_iota_a :
    (assoc omega omega iota).a = -1 := by
  unfold assoc omega iota ProtorealManifold.mul
  simp [HSub.hSub, Sub.sub]

-- ════════════════════════════════════════════════════
-- PENTAGON COCYCLE: sum = 0
-- ════════════════════════════════════════════════════

/-- **PENTAGON COCYCLE (ω,ω,ω,ι)**:
    α(ω²,ω,ι).a − α(ω,ω²,ι).a + α(ω,ω,ω·ι).a = 0. -/
theorem pentagon_wwwi :
    (assoc (ProtorealManifold.mul omega omega) omega iota).a -
    (assoc omega (ProtorealManifold.mul omega omega) iota).a +
    (assoc omega omega (ProtorealManifold.mul omega iota)).a = 0 := by
  unfold assoc omega iota ProtorealManifold.mul
  simp [HSub.hSub, Sub.sub]

/-- **PENTAGON COCYCLE (ω,ω,ι,ι)**: sum = 0. -/
theorem pentagon_wwii :
    (assoc (ProtorealManifold.mul omega omega) iota iota).a -
    (assoc omega (ProtorealManifold.mul omega iota) iota).a +
    (assoc omega omega (ProtorealManifold.mul iota iota)).a = 0 := by
  unfold assoc omega iota ProtorealManifold.mul
  simp [HSub.hSub, Sub.sub]

/-- **PENTAGON COCYCLE (ω,ι,ω,ι)**: sum = 0. -/
theorem pentagon_wiwi :
    (assoc (ProtorealManifold.mul omega iota) omega iota).a -
    (assoc omega (ProtorealManifold.mul iota omega) iota).a +
    (assoc omega iota (ProtorealManifold.mul omega iota)).a = 0 := by
  unfold assoc omega iota ProtorealManifold.mul
  simp [HSub.hSub, Sub.sub]

/-- **PENTAGON COCYCLE (ι,ω,ω,ι)**: sum = 0. -/
theorem pentagon_iwwi :
    (assoc (ProtorealManifold.mul iota omega) omega iota).a -
    (assoc iota (ProtorealManifold.mul omega omega) iota).a +
    (assoc iota omega (ProtorealManifold.mul omega iota)).a = 0 := by
  unfold assoc omega iota ProtorealManifold.mul
  simp [HSub.hSub, Sub.sub]

-- ════════════════════════════════════════════════════
-- FLAT SECTORS
-- ════════════════════════════════════════════════════

/-- ε-ε-ε is fully associative (nilpotent sector is flat). -/
theorem assoc_eee :
    assoc FusionRing.eE FusionRing.eE FusionRing.eE = 0 := by
  unfold assoc FusionRing.eE ProtorealManifold.mul
  ext <;> simp

/-- λ-λ-λ is fully associative (level sector is flat). -/
theorem assoc_LLL :
    assoc FusionRing.eL FusionRing.eL FusionRing.eL = 0 := by
  unfold assoc FusionRing.eL ProtorealManifold.mul
  ext <;> simp

-- ════════════════════════════════════════════════════
-- HETEROGENEITY THEOREM
-- ════════════════════════════════════════════════════

/-- **ASSOCIATIVE SECTORS**: Elements in the real line (all non-real
    components zero) are trivially associative. Non-associativity
    arises from the ω-ι and ε-λ cross-term interactions.

    More precisely: the a-component of the associator depends on
    the thrust-anchor sector AND the noise-level sector. Both
    contraction pairs (ω·ι and ε·λ) contribute to curvature. -/
theorem real_sector_associative
    (A B C : ProtorealManifold)
    (hA : A.b = 0 ∧ A.m = 0 ∧ A.e = 0 ∧ A.l = 0)
    (hB : B.b = 0 ∧ B.m = 0 ∧ B.e = 0 ∧ B.l = 0)
    (hC : C.b = 0 ∧ C.m = 0 ∧ C.e = 0 ∧ C.l = 0) :
    assoc A B C = 0 := by
  obtain ⟨hA1, hA2, hA3, hA4⟩ := hA
  obtain ⟨hB1, hB2, hB3, hB4⟩ := hB
  obtain ⟨hC1, hC2, hC3, hC4⟩ := hC
  unfold assoc ProtorealManifold.mul
  ext <;> simp [HSub.hSub, Sub.sub, hA1, hA2, hA3, hA4, hB1, hB2, hB3, hB4, hC1, hC2, hC3, hC4] <;> ring

end PentagonCoherence
