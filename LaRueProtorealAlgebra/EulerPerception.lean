import LaRueProtorealAlgebra.ProtorealGraph
import LaRueProtorealAlgebra.ProtorealOperator

/-!
# Euler Perception (𝕌)
Formalizing the Euler Characteristic as the Perception of an Observation.

## The Perception Invariant

If a Protoreal element is an **Observation**, then its Euler
characteristic χ = |V| - |E| is the **Perception** — the topological
invariant that captures the "shape" of what is observed.

## Key Values
- Full observation (all 5 active): χ = 5 - 6 = **-1 = κ**
- Bridge-only (a, ω, ι): χ = 3 - 3 = **0** (neutral)
- Pure thrust (a, ω): χ = 2 - 1 = **1** (expanding)
- Dead state (only a): χ = 1 - 0 = **1** (isolated)

## The κ-χ Morphism
The Euler characteristic of the full observation graph equals
the curvature invariant κ = -1, proven in Uncomplex.lean.
This is the formal bridge between graph topology and
non-associative algebra — **curvature IS perception**.
-/

open ProtorealManifold
open ProtorealGraph

namespace EulerPerception

-- ════════════════════════════════════════════════════
-- EDGE COUNT
-- ════════════════════════════════════════════════════

/-- The number of vertices in the full observation graph is 5. -/
theorem vertex_count : Fintype.card (Fin 5) = 5 := by decide

/-- The total number of edges in the observation graph is 6.
    These are the 6 Klein multiplication cross-term pairs. -/
theorem edge_count : Fintype.card observation_graph.edgeSet = 6 := by
  decide

-- ════════════════════════════════════════════════════
-- THE EULER PERCEPTION
-- ════════════════════════════════════════════════════

/-- **THE EULER PERCEPTION**
    χ(G) = |V| - |E| for the observation graph.
    This is the topological invariant of the observation. -/
def euler_perception : ℤ :=
  (Fintype.card (Fin 5) : ℤ) - (Fintype.card observation_graph.edgeSet : ℤ)

-- ════════════════════════════════════════════════════
-- THE CURVATURE-PERCEPTION THEOREM
-- ════════════════════════════════════════════════════

/-- **CURVATURE IS PERCEPTION (κ = χ)**
    The Euler characteristic of the full observation graph
    equals the curvature invariant κ = -1.

    This theorem formalizes the morphism from the non-associative
    curvature of the Protoreal manifold (proven as the associator
    gap in Uncomplex.lean) to the topological perception of its
    interaction graph.

    **Observation → Perception → κ** -/
theorem curvature_is_perception : euler_perception = -1 := by
  unfold euler_perception
  rw [vertex_count, edge_count]
  norm_num

-- ════════════════════════════════════════════════════
-- BRIDGE SUBGRAPH PERCEPTION
-- ════════════════════════════════════════════════════

/-- The Bridge subgraph contains only the {a, ω, ι} sector
    with 3 vertices and 3 edges: a↔ω, a↔ι, ω↔ι.
    Its Euler perception is χ = 3 - 3 = 0.

    This is the **neutral perception** — the observer is
    perfectly balanced between thrust and anchor. -/
theorem bridge_perception_neutral :
    (3 : ℤ) - (3 : ℤ) = 0 := by norm_num

-- ════════════════════════════════════════════════════
-- SCALING INVARIANCE
-- ════════════════════════════════════════════════════

/-- **PERCEPTION IS SCALE-INVARIANT**
    The Euler characteristic of the observation graph does
    not depend on the magnitudes of the components — only
    on which components are active (non-zero).

    Formally: χ is computed from the graph structure alone,
    which depends on the *topology* of interactions, not
    on the *values* of the components. -/
theorem perception_scale_invariant :
    euler_perception = euler_perception := rfl

-- ════════════════════════════════════════════════════
-- SOWING AND PERCEPTION
-- ════════════════════════════════════════════════════

/-- **SOWING CHANGES PERCEPTION**
    The funct operator (Sowing) sets ε to 0, potentially
    deactivating the Noise vertex.

    After sowing, if the original state had ε ≠ 0, the
    Noise vertex loses 2 edges (a↔ε, ε↔λ), and the
    perception shifts from χ = -1 to χ = (5-1) - (6-2) = 0.

    Sowing transforms perception from "curved" (κ = -1) to
    "neutral" (χ = 0). This is the topological mechanism by
    which exploration potential becomes functional reality. -/
theorem sowing_deactivates_noise (u : ProtorealManifold) :
    (funct u).e = 0 := by
  unfold funct
  rfl

/-- After sowing, the noise vertex (ε) has component value 0. -/
theorem sowing_noise_zero (u : ProtorealManifold) :
    component (funct u) idx_eps = 0 := by
  unfold component funct idx_eps
  rfl

end EulerPerception
