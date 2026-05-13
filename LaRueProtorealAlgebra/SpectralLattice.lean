import LaRueProtorealAlgebra.ProtorealMesh
import LaRueProtorealAlgebra.ProtorealAlgebra

/-!
# Spectral Lattice (𝕌)
Mapping the Klein Mesh to the spectral lattice coordinates.
-/

open ProtorealManifold

/-- Spectral Coordinate:
    A mapping to the (a, b, m) sectors. -/
structure SpectralCoordinate where
  a : ℝ
  b : ℝ
  m : ℝ

/-- resonance_lattice:
    Maps a coordinate into the Klein mesh. -/
def resonance_lattice (c : SpectralCoordinate) : KleinMesh :=
  mesh_stitch { a := c.a, b := c.b, m := c.m, e := 0, l := 0 } 0


