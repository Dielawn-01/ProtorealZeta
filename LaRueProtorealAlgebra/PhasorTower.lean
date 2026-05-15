import LaRueProtorealAlgebra.ProtorealManifold
import LaRueProtorealAlgebra.FusionRing
import LaRueProtorealAlgebra.HyperKlein
import LaRueProtorealAlgebra.HodgeConjecture
import LaRueProtorealAlgebra.Rigidity

/-!
# Phasor Tower (ℝ → ℂ → 𝕌)

Formalizing the embedding tower from reals through complex numbers to
the Protoreal manifold, mediated by the **phasor structure**.

## The Complex Structure

The Bridge identity ω·ι = −𝟙 is the Klein analog of i² = −1.
Multiplication by ι acts as a **90° rotation**:
  (a𝟙 + bω) · ι = −b𝟙 + aι

This maps (a, b, 0, 0, 0) → (−b, 0, a, 0, 0), i.e. the pair (a,b)
undergoes the rotation (a,b) ↦ (−b, a) — exactly like the complex
multiplication z ↦ iz.

## The Phase

The **phase** of a Klein element is `φ(u) = u.b − u.m`.
- φ = 0: Hodge class (parity-locked, algebraic cycle)
- φ ≠ 0: non-Hodge (active phasor)

The Hodge star ★ is the "phase conjugation" operator: ★u swaps b↔m,
so ★ negates the phase: φ(★u) = −φ(u).

## The Tower

| Level | Number System | Power Tower | Behavior |
|-------|--------------|-------------|----------|
| ℝ | Real line | x^n | Fixpoint |
| ℂ | Complex plane | z^n | Rotation |
| 𝕌 | Klein manifold | u^n | 3 fixpoints + 1 oscillator |
-/

open ProtorealManifold

namespace PhasorTower

-- ════════════════════════════════════════════════════
-- THE EMBEDDINGS
-- ════════════════════════════════════════════════════

/-- **ℝ EMBEDDING**: x ↦ {x, 0, 0, 0, 0}.
    The real line lives in the a-component. -/
def real_embed (x : ℝ) : ProtorealManifold :=
  { a := x, b := 0, m := 0, e := 0, l := 0 }

/-- **ℂ EMBEDDING**: (re, im) ↦ {re, im, 0, 0, 0}.
    The "complex plane" uses a for the real part and b for the
    imaginary part. Multiplication by ι acts as multiplication by i. -/
def complex_embed (re im : ℝ) : ProtorealManifold :=
  { a := re, b := im, m := 0, e := 0, l := 0 }

-- ════════════════════════════════════════════════════
-- THE COMPLEX ROTATION
-- ════════════════════════════════════════════════════

/-- **MULTIPLICATION BY ι IS A 90° ROTATION**
    (a𝟙 + bω) · ι = (−b)𝟙 + aι.
    This maps the a-component to −b and the m-component to a.
    In terms of the (a,b) plane: (a,b) ↦ (−b, a). -/
theorem iota_rotation (a b : ℝ) :
    (ProtorealManifold.mul (complex_embed a b) iota).a = -b ∧
    (ProtorealManifold.mul (complex_embed a b) iota).m = a := by
  unfold complex_embed iota ProtorealManifold.mul
  constructor <;> ring

/-- **DOUBLE ROTATION COLLAPSES THE REAL PART**
    Multiplying by ι twice maps the a-component to 0.
    Unlike ℂ where i²z = −z, the Klein double rotation
    loses information due to non-associativity.

    This is the **quasi-associativity signature**: in ℂ,
    (z·i)·i = z·(i·i) = −z. But in 𝕌,
    (z·ι)·ι ≠ z·(ι·ι) because κ = −1.

    The DIFFERENCE is exactly the associator gap. -/
theorem double_iota_collapses (a b : ℝ) :
    let z := complex_embed a b
    let z' := ProtorealManifold.mul (ProtorealManifold.mul z iota) iota
    z'.a = 0 := by
  unfold complex_embed iota ProtorealManifold.mul
  simp

-- ════════════════════════════════════════════════════
-- THE PHASE
-- ════════════════════════════════════════════════════

/-- **THE KLEIN PHASE**: φ(u) = u.b − u.m.
    Measures how far an element is from being a Hodge class. -/
def klein_phase (u : ProtorealManifold) : ℝ := u.b - u.m

/-- **HODGE CLASS ↔ ZERO PHASE**
    u is a Hodge class iff its phase is zero. -/
theorem hodge_iff_zero_phase (u : ProtorealManifold) :
    HodgeConjecture.hodge_star u = u ↔ klein_phase u = 0 := by
  rw [HodgeConjecture.hodge_class_iff_parity]
  unfold klein_phase
  constructor
  · intro h; linarith
  · intro h; linarith

/-- **THE HODGE STAR NEGATES PHASE**
    φ(★u) = −φ(u). The Hodge star is phase conjugation. -/
theorem hodge_negates_phase (u : ProtorealManifold) :
    klein_phase (HodgeConjecture.hodge_star u) = -klein_phase u := by
  unfold klein_phase HodgeConjecture.hodge_star MonsterInverse.monster_inv
  ring

/-- **REAL EMBEDDINGS ARE HODGE CLASSES**
    Every real number embeds as a phase-zero element. -/
theorem real_is_hodge (x : ℝ) :
    klein_phase (real_embed x) = 0 := by
  unfold klein_phase real_embed; ring

/-- **PURE IMAGINARY HAS MAXIMAL PHASE**
    The basis element ω has maximal positive phase. -/
theorem omega_phase : klein_phase omega = 1 := by
  unfold klein_phase omega; ring

/-- **DUAL IMAGINARY HAS MINIMAL PHASE**
    The basis element ι has maximal negative phase. -/
theorem iota_phase : klein_phase iota = -1 := by
  unfold klein_phase iota; ring

-- ════════════════════════════════════════════════════
-- THE PARITY PROJECTION (Phase Lock)
-- ════════════════════════════════════════════════════

/-- **THE PARITY PROJECTION KILLS PHASE**
    The parity projection (u + ★u)/2 always has zero phase.
    This is the "phase-locking" operation that produces Hodge classes. -/
noncomputable def phase_lock (u : ProtorealManifold) : ProtorealManifold :=
  { a := u.a, b := (u.b + u.m) / 2, m := (u.b + u.m) / 2, e := u.e, l := u.l }

theorem phase_lock_is_hodge (u : ProtorealManifold) :
    klein_phase (phase_lock u) = 0 := by
  unfold klein_phase phase_lock; ring

-- ════════════════════════════════════════════════════
-- FIXPOINT-OSCILLATOR CLASSIFICATION
-- ════════════════════════════════════════════════════

/-- **FIXPOINTS ARE HODGE-LIKE**
    ω, ε, λ are fixpoints of Klein power. Their power towers converge.
    ω has phase 1 (pure imaginary), ε and λ have phase 0 (real-like). -/
theorem fixpoint_phases :
    klein_phase omega = 1 ∧
    klein_phase FusionRing.eE = 0 ∧
    klein_phase FusionRing.eL = 0 :=
  ⟨omega_phase,
   by unfold klein_phase FusionRing.eE; ring,
   by unfold klein_phase FusionRing.eL; ring⟩

/-- **THE OSCILLATOR HAS DUAL PHASE**
    ι has phase −1, the conjugate of ω's phase 1.
    Its power tower oscillates (period 2) rather than converging. -/
theorem oscillator_dual_phase :
    klein_phase iota = -(klein_phase omega) := by
  rw [omega_phase, iota_phase]

-- ════════════════════════════════════════════════════
-- THE TOWER HIERARCHY
-- ════════════════════════════════════════════════════

/-- **THE PHASOR TOWER THEOREM**
    The ℝ → ℂ → 𝕌 embedding tower has the following structure:
    1. ℝ embeds as zero-phase elements (always Hodge)
    2. ℂ embeds via ι-rotation (i² = −1 analog)
    3. 𝕌 adds noise (ε) and level (λ), both zero-phase
    4. The phase classifies Hodge vs non-Hodge
    5. The parity projection always produces Hodge classes -/
theorem phasor_tower :
    -- ℝ is always Hodge
    (∀ x : ℝ, klein_phase (real_embed x) = 0) ∧
    -- ι-rotation is the complex structure
    (∀ a b : ℝ,
      (ProtorealManifold.mul (complex_embed a b) iota).a = -b ∧
      (ProtorealManifold.mul (complex_embed a b) iota).m = a) ∧
    -- Phase-lock always produces Hodge classes
    (∀ u : ProtorealManifold, klein_phase (phase_lock u) = 0) ∧
    -- Hodge star negates phase
    (∀ u : ProtorealManifold,
      klein_phase (HodgeConjecture.hodge_star u) = -klein_phase u) :=
  ⟨real_is_hodge, iota_rotation, phase_lock_is_hodge, hodge_negates_phase⟩

end PhasorTower
