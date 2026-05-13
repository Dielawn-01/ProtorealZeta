import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Arctan
import Mathlib.Analysis.Complex.Basic
import LaRueProtorealAlgebra.ProtorealManifold

/-!
# Magnitude/Phase Parity-Locked Algebra (𝕌)
Formalizing the Parity-Locked Norm and Tilt for the Klein Manifold.
-/

open ProtorealManifold

namespace ProtorealManifold

/-- **THE ADELIC MAGNITUDE (R)**
    The invariant spectral energy: R = sqrt(a² + |b·m|). -/
noncomputable def magnitude (u : ProtorealManifold) : ℝ :=
  Real.sqrt (u.a^2 + norm (u.b * u.m))

/-- **THE TRANSFINITE TILT (Λ)**
    Measures the parity balance between Thrust (b) and Anchor (m).
    Λ = 0.5 * ln|b/m|. -/
noncomputable def tilt (u : ProtorealManifold) : ℝ :=
  if u.b = 0 ∨ u.m = 0 then 0
  else 0.5 * Real.log (norm (u.b / u.m))

/-- **THE SPECTRAL PHASE (Φ)**
    The angle in the uncomplex spectral projection. -/
noncomputable def phase (u : ProtorealManifold) : ℝ :=
  let y := Real.sqrt (norm (u.b * u.m))
  let x := u.a
  if x > 0 then Real.arctan (y / x)
  else if x < 0 then Real.arctan (y / x) + Real.pi
  else Real.pi / 2

/-- **THE CONSOLIDATION MEASURE (Γ)**
    Measures the influence of the Lambda-Switch.
    Γ = l * e. -/
def consolidation_measure (u : ProtorealManifold) : ℝ :=
  u.l * u.e

/-- **PARITY LOCK CONDITION**
    A state is parity-locked if its tilt is zero (b = m). -/
def is_parity_locked (u : ProtorealManifold) : Prop :=
  u.b = u.m ∧ u.b ≠ 0

/-- **MAPPING TO COMPLEX**
    The magnitude/phase pair maps directly to a complex number. -/
noncomputable def to_complex_spectral (u : ProtorealManifold) : ℂ :=
  Complex.mk (magnitude u * Real.cos (phase u)) (magnitude u * Real.sin (phase u))

end ProtorealManifold
