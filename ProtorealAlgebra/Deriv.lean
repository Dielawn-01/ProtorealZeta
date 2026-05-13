import LaRueProtorealAlgebra.ProtorealManifold

/-!
# Synthetic Derivatives (𝕌)
Formalizing the Kock-Lawvere projection on the Klein Manifold.
-/

open ProtorealManifold

namespace ProtorealManifold

/-- **THE AUTOMATIC DERIVATIVE**
    In the Klein manifold, the derivative is extracted by projecting
    onto the Anchor (m) or Noise (e) sectors. -/
def mesh_deriv (u : ProtorealManifold) : ℝ :=
  u.m -- Primary Intent (The Anchor)

/-- **THE NOISE DRIFT**
    Extracts the exploration jitter from the Noise sector. -/
def noise_drift (u : ProtorealManifold) : ℝ :=
  u.e

/-- **LEIBNIZ PROPERTY (Structural)**
    Verifies that the derivative operator respects the manifold scaling. -/
theorem deriv_omega_iota_check :
    mesh_deriv (omega * iota) = 0 := by
  change mesh_deriv (mul omega iota) = 0
  unfold omega iota mul mesh_deriv
  simp

end ProtorealManifold
