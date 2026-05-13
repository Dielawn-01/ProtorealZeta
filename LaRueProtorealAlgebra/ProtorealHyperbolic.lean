import Mathlib.Analysis.Complex.Trigonometric
import LaRueProtorealAlgebra.ProtorealMesh

/-!
# Protoreal Hyperbolic Trigonometry (𝕌)
Formalizing sinh and cosh on the Klein Manifold.
-/

open ProtorealManifold

/-- Mesh Sinh:
    Expanded across the Klein manifold sectors. -/
noncomputable def mesh_sinh (m : KleinMesh) : KleinMesh :=
  let u := m.manifold
  { manifold := 
      { a := Real.sinh (u.a + m.resonance.re),
        b := Real.sinh (u.a + u.b + m.resonance.re) - Real.sinh (u.a + m.resonance.re),
        m := Real.cosh (u.a + m.resonance.re) * u.m,
        e := Real.cosh (u.a + m.resonance.re) * u.e,
        l := Real.cosh (u.a + m.resonance.re) * u.l },
    resonance := m.resonance }

/-- Mesh Cosh:
    Expanded across the Klein manifold sectors. -/
noncomputable def mesh_cosh (m : KleinMesh) : KleinMesh :=
  let u := m.manifold
  { manifold := 
      { a := Real.cosh (u.a + m.resonance.re),
        b := Real.cosh (u.a + u.b + m.resonance.re) - Real.cosh (u.a + m.resonance.re),
        m := Real.sinh (u.a + m.resonance.re) * u.m,
        e := Real.sinh (u.a + m.resonance.re) * u.e,
        l := Real.sinh (u.a + m.resonance.re) * u.l },
    resonance := m.resonance }

/-- **THE DYNAMIC PYTHAGOREAN IDENTITY**
    cosh²(m) - sinh²(m) = 1 (at the real site). -/
theorem dynamic_pythagorean (m : KleinMesh) :
    (mesh_cosh m).manifold.a^2 - (mesh_sinh m).manifold.a^2 = 1 := by
  unfold mesh_cosh mesh_sinh
  simp

/-- Mesh Tanh:
    The Protoreal Variation of the Tanh activation function.
    Couples the hyperbolic squashing to the anchor/noise sectors. -/
noncomputable def mesh_tanh (m : KleinMesh) : KleinMesh :=
  let u := m.manifold
  let r := m.resonance.re
  { manifold := 
      { a := Real.tanh (u.a + r),
        b := Real.tanh (u.a + u.b + r) - Real.tanh (u.a + r),
        m := (1 - (Real.tanh (u.a + r))^2) * u.m,
        e := (1 - (Real.tanh (u.a + r))^2) * u.e,
        l := (1 - (Real.tanh (u.a + r))^2) * u.l },
    resonance := m.resonance }

/-- **TANH DERIVATIVE PROPERTY**
    The anchor sector of mesh_tanh is exactly scaled by the derivative. -/
theorem mesh_tanh_anchor_scaled (m : KleinMesh) :
    (mesh_tanh m).manifold.m = 
    (1 - (Real.tanh (m.manifold.a + m.resonance.re))^2) * m.manifold.m := by
  unfold mesh_tanh
  simp
