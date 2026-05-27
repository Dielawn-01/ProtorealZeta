import LaRueProtorealAlgebra.Basic
import LaRueProtorealAlgebra.LieAlgebra

open ProtorealManifold
open LieAlgebra

namespace ExteriorAlgebra

/-- The Exterior (Wedge) Product. -/
def wedge (u v : ProtorealManifold) : ProtorealManifold :=
  u * v - v * u

/-- The wedge product is identical to the Lie bracket. -/
theorem wedge_eq_bracket (u v : ProtorealManifold) :
    wedge u v = lie_bracket u v := rfl

-- Grassmann Axioms
theorem wedge_antisymmetric (u v : ProtorealManifold) :
    wedge u v = -(wedge v u) := by
  unfold wedge; ext <;> simp <;> ring

theorem wedge_self_zero (u : ProtorealManifold) :
    wedge u u = 0 := by
  unfold wedge; ext <;> simp <;> ring

theorem wedge_nilpotent (u v w : ProtorealManifold) :
    wedge (wedge u v) w = 0 := by
  unfold wedge; ext <;> simp <;> ring

-- Pure Real
theorem wedge_b_zero (u v : ProtorealManifold) : (wedge u v).b = 0 := by
  unfold wedge; simp; ring
theorem wedge_m_zero (u v : ProtorealManifold) : (wedge u v).m = 0 := by
  unfold wedge; simp; ring
theorem wedge_e_zero (u v : ProtorealManifold) : (wedge u v).e = 0 := by
  unfold wedge; simp; ring
theorem wedge_l_zero (u v : ProtorealManifold) : (wedge u v).l = 0 := by
  unfold wedge; simp; ring

-- Annihilation
theorem annihilation_omega_iota :
    wedge omega iota = { a := -2, b := 0, m := 0, e := 0, l := 0 } := by
  unfold wedge omega iota; ext <;> simp <;> ring

theorem annihilation_energy_omega_iota :
    (wedge omega iota).a = -2 := by
  unfold wedge omega iota; simp; ring

theorem annihilation_eps_lam :
    wedge eps lam = { a := -2, b := 0, m := 0, e := 0, l := 0 } := by
  unfold wedge eps lam; ext <;> simp <;> ring

theorem annihilation_energy_eps_lam :
    (wedge eps lam).a = -2 := by
  unfold wedge eps lam; simp; ring

-- Baryogenesis
theorem thrust_accumulates : omega * omega = omega := by
  ext <;> unfold omega <;> simp <;> ring

theorem anchor_oscillates : iota * iota = -iota := by
  ext <;> unfold iota <;> simp <;> ring

theorem baryogenesis :
    (omega * omega = omega) ∧ (iota * iota = -iota) :=
  ⟨thrust_accumulates, anchor_oscillates⟩

theorem complete_annihilation :
    omega * iota + iota * omega = 0 ∧
    (wedge omega iota).a = -2 := by
  constructor
  · ext <;> unfold omega iota <;> simp
  · unfold wedge omega iota; simp; ring

-- Signature
theorem signature_thrust : (omega * omega).b = 1 := by
  unfold omega; simp
theorem signature_anchor : (iota * iota).m = -1 := by
  unfold iota; simp
theorem signature_noise : (eps * eps).e = 1 := by
  unfold eps; simp
theorem signature_level : (lam * lam).l = 1 := by
  unfold lam; simp

theorem signature_plus_minus_plus_plus :
    (omega * omega).b = 1 ∧
    (iota * iota).m = -1 ∧
    (eps * eps).e = 1 ∧
    (lam * lam).l = 1 :=
  ⟨signature_thrust, signature_anchor, signature_noise, signature_level⟩

end ExteriorAlgebra
