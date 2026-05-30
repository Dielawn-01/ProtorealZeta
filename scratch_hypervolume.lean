import LaRueProtorealAlgebra.ProtorealManifold
import LaRueProtorealAlgebra.HyperbolicIdentity
open ProtorealManifold
open ProtorealAlgebra

theorem right_associative_hypervolume :
    U * (U * U) = U * (1/4 : ℝ) + (1/4 : ℝ) := by
  ext <;> dsimp [U, omega, iota] <;> simp <;> ring
