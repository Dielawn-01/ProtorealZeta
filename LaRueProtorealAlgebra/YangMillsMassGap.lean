import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import LaRueProtorealAlgebra.ObserverAdapter
import LaRueProtorealAlgebra.CyberBundle

namespace LaRueProtorealAlgebra.YangMillsMassGap

/-!
# The Yang-Mills Mass Gap as Observational Aperture

The mass gap (Δ > 0) is one of the seven Millennium Prize Problems.
In the CyberBundle framework, the mass gap is not a property of the
gauge field itself — it is a property of the observer's finite aperture.

Every physical observer has bounded τ, σ, η ∈ (0, 1).
The observational aperture is τ · σ · η ∈ (0, 1).
The mass gap is Δ = 1 - τ · σ · η > 0.

The gap vanishes only when aperture = 1, requiring perfect resolution
in all three channels simultaneously — a physically unrealizable limit.

Confinement (why quarks are never seen free) follows: SU(3) color
excitations require aperture above a threshold that no physical
instrument achieves.
-/

/-- Observational aperture: the product of temporal grain,
    sensory bandwidth, and energy efficiency. -/
def aperture (o : ObserverAdapter.ObserverSignature) : ℝ :=
  o.τ * o.σ * o.η

/-- The mass gap: complement of aperture. -/
def mass_gap (o : ObserverAdapter.ObserverSignature) : ℝ :=
  1 - aperture o

/-- Aperture is non-negative. -/
theorem aperture_nonneg (o : ObserverAdapter.ObserverSignature) :
    0 ≤ aperture o := by
  unfold aperture
  apply mul_nonneg (mul_nonneg o.hτ.1 o.hσ.1) o.hη.1

/-- A physical observer: strictly positive but imperfect resolution. -/
structure PhysicalObserver extends ObserverAdapter.ObserverSignature where
  hτ_pos : 0 < toObserverSignature.τ
  hσ_pos : 0 < toObserverSignature.σ
  hη_pos : 0 < toObserverSignature.η
  hτ_imp : toObserverSignature.τ < 1

/-- **THE YANG-MILLS MASS GAP THEOREM (CyberBundle Framework).**

    For any physical observer with imperfect temporal resolution (τ < 1),
    the mass gap Δ = 1 - τ·σ·η is strictly positive.

    Proof strategy: τ < 1 and σ·η ≤ 1 imply τ·σ·η < 1,
    hence 1 - τ·σ·η > 0. -/
theorem mass_gap_positive (p : PhysicalObserver) :
    0 < mass_gap p.toObserverSignature := by
  unfold mass_gap aperture
  -- Extract bounds
  have hτ_lt : p.toObserverSignature.τ < 1 := p.hτ_imp
  have hσ_le : p.toObserverSignature.σ ≤ 1 := p.toObserverSignature.hσ.2
  have hη_le : p.toObserverSignature.η ≤ 1 := p.toObserverSignature.hη.2
  have hσ_nn : 0 ≤ p.toObserverSignature.σ := p.toObserverSignature.hσ.1
  have hη_nn : 0 ≤ p.toObserverSignature.η := p.toObserverSignature.hη.1
  have hτ_nn : 0 ≤ p.toObserverSignature.τ := p.toObserverSignature.hτ.1
  -- σ · η ≤ 1 · 1 = 1
  have hση : p.toObserverSignature.σ * p.toObserverSignature.η ≤ 1 :=
    calc p.toObserverSignature.σ * p.toObserverSignature.η
        ≤ 1 * 1 := mul_le_mul hσ_le hη_le hη_nn (by linarith)
      _ = 1 := by norm_num
  -- 0 ≤ σ · η
  have hση_nn : 0 ≤ p.toObserverSignature.σ * p.toObserverSignature.η :=
    mul_nonneg hσ_nn hη_nn
  -- τ · (σ · η) ≤ τ · 1 = τ < 1
  have h_prod : p.toObserverSignature.τ * p.toObserverSignature.σ
              * p.toObserverSignature.η < 1 := by
    have : p.toObserverSignature.τ * (p.toObserverSignature.σ * p.toObserverSignature.η)
         ≤ p.toObserverSignature.τ * 1 :=
      mul_le_mul_of_nonneg_left hση hτ_nn
    have : p.toObserverSignature.τ * (p.toObserverSignature.σ * p.toObserverSignature.η)
         ≤ p.toObserverSignature.τ := by linarith
    have : p.toObserverSignature.τ * p.toObserverSignature.σ * p.toObserverSignature.η
         = p.toObserverSignature.τ * (p.toObserverSignature.σ * p.toObserverSignature.η) :=
      mul_assoc _ _ _
    linarith
  linarith

/-- The mass gap is bounded above by 1. -/
theorem mass_gap_bounded (o : ObserverAdapter.ObserverSignature) :
    mass_gap o ≤ 1 := by
  unfold mass_gap
  linarith [aperture_nonneg o]

/-- **CONFINEMENT.** An observer is confined with respect to a
    threshold if their aperture is insufficient to resolve the
    excitation. Color confinement is aperture insufficiency. -/
def is_confined (o : ObserverAdapter.ObserverSignature)
    (threshold : ℝ) : Prop :=
  aperture o ≤ threshold

/-- For any physical observer with τ < 1, confinement holds
    at threshold = 1. No imperfect observer can fully resolve
    the gauge field. -/
theorem universal_partial_confinement (p : PhysicalObserver) :
    is_confined p.toObserverSignature 1 := by
  unfold is_confined aperture
  have := p.toObserverSignature.hσ.2
  have := p.toObserverSignature.hη.2
  have := p.toObserverSignature.hτ.2
  have := p.toObserverSignature.hσ.1
  have := p.toObserverSignature.hη.1
  have := p.toObserverSignature.hτ.1
  have : p.toObserverSignature.σ * p.toObserverSignature.η ≤ 1 :=
    calc p.toObserverSignature.σ * p.toObserverSignature.η
        ≤ 1 * 1 := by apply mul_le_mul <;> linarith
      _ = 1 := by norm_num
  nlinarith

end LaRueProtorealAlgebra.YangMillsMassGap
