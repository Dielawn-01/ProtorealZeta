import LaRueProtorealAlgebra.Basic
import LaRueProtorealAlgebra.LieAlgebra
open ProtorealManifold open LieAlgebra

theorem bracket_of_eps_lam : lie_bracket eps lam = { a := 2, b := 0, m := 0, e := 0, l := 0 } := by
  ext <;> unfold lie_bracket eps lam <;> simp <;> ring
  norm_num
  lean
