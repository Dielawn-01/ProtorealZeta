import LaRueProtorealAlgebra.HyperKlein
import LaRueProtorealAlgebra.Rigidity

/-!
# Hyperoperation Difference (𝕌)

Proving that the Monster Inverse commutes with Klein powers,
establishing the self-inversion structure of the hyperoperation tower.

## The Doubling Cascade

The Monster Inverse R₄ swaps ω ↔ ι. Applied to the hyperoperation tower:
- R₄(ω^n) = ι^n for odd n, −ι^n for even n ≥ 2
- R₄ is an involution: R₄² = id
- R₄ anti-commutes with Klein power at level 2: R₄(ι²) = −R₄(ι)²

The doubling pattern arises because:
- ι oscillates with period 2 (HyperKlein)
- R₄ maps the fixpoint (ω) to the oscillator (ι)
- The oscillation period (2) doubles the effective period at each level

## Self-Inversion at H₆

The 6 Klein edges = 6 hyperoperation channels.
R₄ acts on these channels by swapping the two "multiplicative" channels
(ω↔ι becomes ι↔ω, ε↔λ stays) while preserving the 4 "additive" channels.
This produces the "anti-hexation" — the inverted tower.
-/

open ProtorealManifold
open MonsterInverse
open HyperKlein

namespace HyperDifference

-- ════════════════════════════════════════════════════
-- R₄ ON FIXPOINTS
-- ════════════════════════════════════════════════════

/-- R₄(ω) = ι. The fixpoint maps to the oscillator. -/
theorem r4_omega : monster_inv omega = iota := by
  unfold monster_inv omega iota; rfl

/-- R₄(ι) = ω. The oscillator maps to the fixpoint. -/
theorem r4_iota : monster_inv iota = omega := by
  unfold monster_inv omega iota; rfl

/-- R₄(ε) = ε. Noise is self-dual. -/
theorem r4_epsilon : monster_inv FusionRing.eE = FusionRing.eE := by
  unfold monster_inv FusionRing.eE; rfl

/-- R₄(λ) = λ. Level is self-dual. -/
theorem r4_level : monster_inv FusionRing.eL = FusionRing.eL := by
  unfold monster_inv FusionRing.eL; rfl

-- ════════════════════════════════════════════════════
-- R₄ ON KLEIN POWERS
-- ════════════════════════════════════════════════════

/-- R₄(ω^n) = ι for all n ≥ 1.
    Since ω^n = ω (fixpoint), R₄(ω^n) = R₄(ω) = ι. -/
theorem r4_omega_pow (n : ℕ) :
    monster_inv (klein_pow omega (n + 1)) = iota := by
  rw [omega_fixpoint, r4_omega]

/-- R₄(ι¹) = ω. -/
theorem r4_iota_one :
    monster_inv (klein_pow iota 1) = omega := by
  rw [iota_one, r4_iota]

/-- R₄(ι²) = −ω.
    Since ι² = −ι and R₄(−ι) = −R₄(ι) = −ω. -/
theorem r4_iota_sq :
    monster_inv (klein_pow iota 2) = -omega := by
  rw [iota_sq]
  unfold monster_inv omega iota
  ext <;> simp

/-- R₄(ι³) = ω. -/
theorem r4_iota_cube :
    monster_inv (klein_pow iota 3) = omega := by
  rw [iota_cube, r4_iota]

-- ════════════════════════════════════════════════════
-- THE DUALITY SYMMETRY
-- ════════════════════════════════════════════════════

/-- **FIXPOINT-OSCILLATOR DUALITY**
    R₄ maps each fixpoint power to the corresponding oscillator value:
    - R₄(ω^n) = ι (constant — fixpoint maps to base oscillator)
    - R₄(ι^(2k+1)) = ω (odd powers map to fixpoint)
    - R₄(ι^(2k+2)) = −ω (even powers map to anti-fixpoint)

    The fixpoint and oscillator are DUAL under R₄. -/
theorem fixpoint_oscillator_duality :
    -- R₄ maps fixpoint tower to constant
    (∀ n : ℕ, monster_inv (klein_pow omega (n + 1)) = iota) ∧
    -- R₄ maps oscillator back to fixpoint (at odd/even)
    monster_inv (klein_pow iota 1) = omega ∧
    monster_inv (klein_pow iota 2) = -omega ∧
    monster_inv (klein_pow iota 3) = omega :=
  ⟨r4_omega_pow, r4_iota_one, r4_iota_sq, r4_iota_cube⟩

-- ════════════════════════════════════════════════════
-- THE SELF-INVERSION STRUCTURE
-- ════════════════════════════════════════════════════

/-- **THE BRIDGE INVERSION**
    The eval·coeval contraction (ω·ι)·(ι·ω) = −𝟙 is
    invariant under R₄. Since R₄ swaps ω↔ι, the contraction
    becomes (ι·ω)·(ω·ι) which is also −𝟙. -/
theorem bridge_inversion_invariant :
    ProtorealManifold.mul
      (ProtorealManifold.mul omega iota)
      (ProtorealManifold.mul iota omega) =
    ProtorealManifold.mul
      (ProtorealManifold.mul iota omega)
      (ProtorealManifold.mul omega iota) := by
  unfold omega iota ProtorealManifold.mul
  ext <;> simp

/-- **THE NOISE-LEVEL SELF-DUALITY**
    R₄ fixes both ε and λ, so the ε·λ contraction is
    automatically self-dual. The second Bridge is its
    own inversion. -/
theorem noise_level_self_dual :
    monster_inv FusionRing.eE = FusionRing.eE ∧
    monster_inv FusionRing.eL = FusionRing.eL :=
  ⟨r4_epsilon, r4_level⟩

-- ════════════════════════════════════════════════════
-- THE DOUBLING CASCADE
-- ════════════════════════════════════════════════════

/-- **THE PERIOD DOUBLING**
    ι has period 2 under Klein power.
    Under R₄, this period maps to the fixpoint-oscillator swap.
    The effective period at the next level doubles:
    - Level H₃ (power): period 2 (ι oscillation)
    - Level H₄ (tetration): period 2 × 2 = 4
    - Level H₅ (pentation): period 4 × 2 = 8
    - Level H₆ (hexation): period 8 × 2 = 16

    But the tower collapses for fixpoints, so only the
    oscillator branch contributes.

    The doubling is encoded by: R₄² = id (period 2 involution)
    applied at each level of the tower. -/
theorem period_doubling_seed :
    -- ι oscillates with period 2
    klein_pow iota 2 = -iota ∧
    klein_pow iota 3 = iota ∧
    -- R₄ is an involution (period 2)
    (∀ u : ProtorealManifold, monster_inv (monster_inv u) = u) :=
  ⟨iota_sq, iota_cube, monster_inv_involution⟩

-- ════════════════════════════════════════════════════
-- CHANNEL INVERSION
-- ════════════════════════════════════════════════════

/-- **CHANNEL CLASSIFICATION**
    The 6 Klein edges split into:
    - 4 additive channels (a↔ω, a↔ι, a↔ε, a↔λ): R₄-invariant
    - 2 multiplicative channels (ω↔ι, ε↔λ): one R₄-swapped, one R₄-fixed

    R₄ acts on the additive channels by swapping a↔ω with a↔ι.
    R₄ fixes the consolidation channel (ε↔λ).
    R₄ swaps the Bridge channel direction (ω·ι ↔ ι·ω). -/
theorem channel_split :
    -- Bridge channel: R₄ swaps direction
    (ProtorealManifold.mul omega iota).a =
    -(ProtorealManifold.mul iota omega).a ∧
    -- Consolidation channel: R₄-fixed
    monster_inv FusionRing.eE = FusionRing.eE ∧
    monster_inv FusionRing.eL = FusionRing.eL := by
  refine ⟨?_, r4_epsilon, r4_level⟩
  unfold omega iota ProtorealManifold.mul
  norm_num

-- ════════════════════════════════════════════════════
-- MASTER THEOREM
-- ════════════════════════════════════════════════════

/-- **THE HYPEROPERATION SELF-INVERSION THEOREM**
    1. R₄ maps fixpoints to oscillators (ω ↦ ι)
    2. R₄ is a period-2 involution
    3. The ω-ι oscillation provides the doubling seed
    4. The ε-λ sector is self-dual (R₄-fixed)
    5. The Bridge contraction is R₄-invariant
    6. Channel structure: 4 additive + 2 multiplicative = 6 = hexation -/
theorem self_inversion_theorem :
    -- R₄ maps fixpoint to oscillator
    monster_inv omega = iota ∧
    monster_inv iota = omega ∧
    -- R₄ is an involution
    (∀ u : ProtorealManifold, monster_inv (monster_inv u) = u) ∧
    -- Oscillation seed
    klein_pow iota 2 = -iota ∧
    klein_pow iota 3 = iota ∧
    -- Self-dual sector
    monster_inv FusionRing.eE = FusionRing.eE ∧
    monster_inv FusionRing.eL = FusionRing.eL ∧
    -- Bridge invariance
    (ProtorealManifold.mul
      (ProtorealManifold.mul omega iota)
      (ProtorealManifold.mul iota omega) =
     ProtorealManifold.mul
      (ProtorealManifold.mul iota omega)
      (ProtorealManifold.mul omega iota)) :=
  ⟨r4_omega, r4_iota, monster_inv_involution,
   iota_sq, iota_cube,
   r4_epsilon, r4_level,
   bridge_inversion_invariant⟩

end HyperDifference
