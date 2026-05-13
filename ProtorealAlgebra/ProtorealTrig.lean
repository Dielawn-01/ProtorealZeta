import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import LaRueProtorealAlgebra.ProtorealMesh

/-!
# Protoreal Trigonometry (𝕌)
Formalizing sine and cosine on the Klein Manifold.
-/

open ProtorealManifold

/-- Mesh Sine:
    Expanded across the Klein manifold sectors. -/
noncomputable def mesh_sin (m : KleinMesh) : KleinMesh :=
  let u := m.manifold
  { manifold := 
      { a := Real.sin (u.a + m.resonance.re),
        b := Real.sin (u.a + u.b + m.resonance.re) - Real.sin (u.a + m.resonance.re),
        m := Real.cos (u.a + m.resonance.re) * u.m,
        e := Real.cos (u.a + m.resonance.re) * u.e,
        l := Real.cos (u.a + m.resonance.re) * u.l },
    resonance := m.resonance }

/-- Mesh Cosine:
    Expanded across the Klein manifold sectors. -/
noncomputable def mesh_cos (m : KleinMesh) : KleinMesh :=
  let u := m.manifold
  { manifold := 
      { a := Real.cos (u.a + m.resonance.re),
        b := Real.cos (u.a + u.b + m.resonance.re) - Real.cos (u.a + m.resonance.re),
        m := -Real.sin (u.a + m.resonance.re) * u.m,
        e := -Real.sin (u.a + m.resonance.re) * u.e,
        l := -Real.sin (u.a + m.resonance.re) * u.l },
    resonance := m.resonance }

