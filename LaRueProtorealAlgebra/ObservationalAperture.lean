import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import LaRueProtorealAlgebra.ProtorealManifold
import LaRueProtorealAlgebra.LittleDelta
import LaRueProtorealAlgebra.EulersCradle

/-!
# Observational Aperture (𝕌)

**Authors:** LaRue (Theoretical Framework), Antigravity (Formalization)

This module formalizes the concept of "Little Delta" (δ) acting as
the continuous observational aperture (pupil) across Euler's Cradle.
-/

open ProtorealManifold
open LittleDelta
open EulersCradle

namespace ObservationalAperture

-- ════════════════════════════════════════════════════
-- 1. CRADLE APERTURE MEASUREMENT
-- ════════════════════════════════════════════════════

/-- **Cradle Aperture Measure**:
    Evaluates the little_delta observer continuously across Euler's Cradle.
    δ(u) = |u.m| * (u.a - u.b * u.m)
    δ(exp_U(θ)) = |sin(θ)| * (cos(θ) - sin²(θ)) -/
theorem cradle_aperture_measure (θ : ℝ) :
    little_delta.measure (protoreal_exp θ) =
    |Real.sin θ| * (Real.cos θ - (Real.sin θ) * (Real.sin θ)) := by
  unfold little_delta protoreal_exp
  rfl

-- ════════════════════════════════════════════════════
-- 2. PUPIL BOUNDARY CONDITIONS
-- ════════════════════════════════════════════════════

/-- **Aperture Closed at Real Axis**:
    When θ = 0, the manifold state is purely Real.
    The pupil is fully closed (δ = 0), preventing observation
    of the stochastic dimensions. -/
theorem aperture_closed_at_real :
    little_delta.measure (protoreal_exp 0) = 0 := by
  have h_sin : Real.sin 0 = 0 := Real.sin_zero
  unfold little_delta protoreal_exp
  simp [h_sin]

/-- **Aperture Open at Bridge**:
    When θ = π/2, the manifold state is purely at the Imaginary Bridge.
    The pupil is fully dilated (δ = -1), creating the maximal aperture
    for analytic continuation. -/
theorem aperture_open_at_bridge :
    little_delta.measure (protoreal_exp (Real.pi / 2)) = -1 := by
  have h_cos : Real.cos (Real.pi / 2) = 0 := Real.cos_pi_div_two
  have h_sin : Real.sin (Real.pi / 2) = 1 := Real.sin_pi_div_two
  unfold little_delta protoreal_exp
  simp [h_cos, h_sin]

end ObservationalAperture
