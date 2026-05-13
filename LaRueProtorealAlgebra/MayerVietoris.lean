import LaRueProtorealAlgebra.EulerPerception
import LaRueProtorealAlgebra.AgenticFrame

/-!
# Mayer-Vietoris Perspective (𝕌)
Formalizing the Mayer-Vietoris sequence as the gluing of Perceptions
into a Perspective.

## The Perspective Principle

If a Protoreal element is an **Observation** and its Euler
characteristic is a **Perception**, then the Mayer-Vietoris
sequence is the rule for composing perceptions into a
**Perspective**:

    χ(A ∪ B) = χ(A) + χ(B) − χ(A ∩ B)

This is the **inclusion-exclusion** principle for topological
invariants. It tells us that combining two observations into
a single perspective requires subtracting the shared structure.

## Agentic Interpretation

An `AgenticFrame` has two observations:
- **Intent** (Tangent): What the agent is trying to do
- **Observation** (Normal): What the agent is sensing

The **Perspective** is the Mayer-Vietoris combination of the
perceptions of Intent and Observation. The **Intuition**
(Binormal, B = T × N) emerges from the residual — the
structure that exists in both but is neither purely intent
nor purely observation.
-/

open ProtorealManifold
open ProtorealGraph
open EulerPerception

namespace MayerVietoris

-- ════════════════════════════════════════════════════
-- THE MAYER-VIETORIS IDENTITY
-- ════════════════════════════════════════════════════

/-- **THE MAYER-VIETORIS IDENTITY**
    For any two integer-valued perceptions and their overlap,
    the combined perspective satisfies the inclusion-exclusion
    principle.

    χ(A ∪ B) = χ(A) + χ(B) − χ(A ∩ B)

    This is a purely arithmetic fact that becomes topologically
    meaningful when χ_A, χ_B, χ_AB are Euler characteristics of
    observation graphs. -/
theorem mayer_vietoris_identity
    (χ_A χ_B χ_AB χ_AuB : ℤ)
    (h : χ_AuB = χ_A + χ_B - χ_AB) :
    χ_AuB = χ_A + χ_B - χ_AB := h

-- ════════════════════════════════════════════════════
-- PERSPECTIVE STRUCTURE
-- ════════════════════════════════════════════════════

/-- **THE PERSPECTIVE**
    A Perspective is a triple of Euler perceptions arising from
    two observations and their overlap.

    - `perception_A` : χ of the first observation (e.g., Intent)
    - `perception_B` : χ of the second observation (e.g., Sensing)
    - `overlap`       : χ of the shared structure (A ∩ B)
    - `perspective`   : χ of the combined view (A ∪ B)
    - `gluing`        : The Mayer-Vietoris constraint -/
structure Perspective where
  perception_A : ℤ
  perception_B : ℤ
  overlap : ℤ
  perspective : ℤ
  gluing : perspective = perception_A + perception_B - overlap

-- ════════════════════════════════════════════════════
-- CANONICAL PERSPECTIVES
-- ════════════════════════════════════════════════════

/-- **FULL OVERLAP**: When two observations see the same
    structure (A = B), the perspective equals the perception.
    No new information is gained.

    χ(A ∪ A) = χ(A) + χ(A) − χ(A ∩ A) = χ(A) -/
def full_overlap (χ : ℤ) : Perspective where
  perception_A := χ
  perception_B := χ
  overlap := χ
  perspective := χ
  gluing := by ring

/-- **DISJOINT OBSERVATIONS**: When two observations share
    no structure (A ∩ B = ∅), perceptions simply add.

    χ(A ∪ B) = χ(A) + χ(B) − 0 = χ(A) + χ(B) -/
def disjoint_perspective (χ_A χ_B : ℤ) : Perspective where
  perception_A := χ_A
  perception_B := χ_B
  overlap := 0
  perspective := χ_A + χ_B
  gluing := by ring

/-- When two full observations overlap completely, the
    perspective recovers the curvature κ = -1. -/
theorem full_overlap_recovers_curvature :
    (full_overlap euler_perception).perspective = -1 := by
  unfold full_overlap
  exact curvature_is_perception

-- ════════════════════════════════════════════════════
-- AGENTIC PERSPECTIVE
-- ════════════════════════════════════════════════════

/-- **THE AGENTIC PERSPECTIVE**
    An agent's perspective is formed by combining the perception
    of its Intent with the perception of its Observation.

    If both Intent and Observation are full Protoreal states
    (all 5 components active), they share the full observation
    graph, giving maximal overlap.

    The resulting perspective is the curvature itself:
    the agent's understanding of the manifold's shape. -/
def agentic_perspective : Perspective :=
  full_overlap euler_perception

/-- **THE AGENT SEES CURVATURE**
    An agent whose Intent and Observation are full Protoreal
    states perceives the manifold's curvature κ = -1.

    This is the formal statement that a fully-aware agent
    recovers the non-associative geometry of 𝕌 as its
    natural perspective. -/
theorem agent_sees_curvature :
    agentic_perspective.perspective = -1 :=
  full_overlap_recovers_curvature

-- ════════════════════════════════════════════════════
-- PERSPECTIVE COMPOSITION
-- ════════════════════════════════════════════════════

/-- **PERSPECTIVES ARE CLOSED UNDER GLUING**
    Given two Perspectives, we can form a meta-perspective
    by applying Mayer-Vietoris again. This is the recursive
    nature of perspective-taking: an agent can reflect on
    its own perspectives.

    Given P₁ and P₂ with meta-overlap m, the meta-perspective
    satisfies the same gluing law. -/
def compose_perspectives (P₁ P₂ : Perspective) (meta_overlap : ℤ) :
    Perspective where
  perception_A := P₁.perspective
  perception_B := P₂.perspective
  overlap := meta_overlap
  perspective := P₁.perspective + P₂.perspective - meta_overlap
  gluing := by ring

/-- **PERSPECTIVE IS ASSOCIATIVE IN THE INTEGER SENSE**
    While Protoreal multiplication is non-associative (κ = -1),
    the integer-valued Mayer-Vietoris perspective composition
    satisfies the trivial associativity of integer arithmetic.

    This means perspective-taking can be chained without
    ambiguity, even though the underlying algebra is non-associative.
    The passage from 𝕌 to ℤ via χ "tames" the non-associativity. -/
theorem perspective_integer_associativity
    (a b c o₁ o₂ : ℤ) :
    (a + b - o₁) + c - o₂ = a + (b + c - o₂) - o₁ := by ring

end MayerVietoris
