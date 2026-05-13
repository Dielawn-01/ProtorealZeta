import Mathlib.Combinatorics.SimpleGraph.Basic
import Mathlib.Data.Fin.Basic
import LaRueProtorealAlgebra.ProtorealManifold

/-!
# Protoreal Observation Graph (𝕌 → Graph)
Formalizing the morphism from Protoreal elements to interaction graphs.

## The Observation Functor

Every Protoreal element `u = {a, ω, ι, ε, λ}` maps to a graph `G(u)`
on 5 vertices, where edges represent non-trivial interactions under
the Klein multiplication rule.

If a Protoreal number is an **Observation**, then `G(u)` is the
structural skeleton of what is observed — which components are active
and how they interact.

## Vertex Semantics
- `0` : a  (Real Part)
- `1` : ω  (Thrust / Transfinite)
- `2` : ι  (Anchor / Infinitesimal)
- `3` : ε  (Noise / Exploration)
- `4` : λ  (Consolidation / Level)

## Edge Semantics (from Klein Multiplication)
The Klein multiplication `(u₁ · u₂).a = a₁a₂ - b₁m₂ + m₁b₂ + l₁e₂ - e₁l₂`
reveals 6 interaction pairs:
- `(0,1)` a↔ω : `a₁b₂ + a₂b₁` terms in thrust
- `(0,2)` a↔ι : `a₁m₂ + a₂m₁` terms in anchor
- `(0,3)` a↔ε : `a₁e₂ + a₂e₁` terms in noise
- `(0,4)` a↔λ : `a₁l₂ + a₂l₁` terms in level
- `(1,2)` ω↔ι : `-b₁m₂ + m₁b₂` cross-terms (The Bridge)
- `(3,4)` ε↔λ : `l₁e₂ - e₁l₂` cross-terms (The Consolidation)
-/

open ProtorealManifold

namespace ProtorealGraph

-- ════════════════════════════════════════════════════
-- COMPONENT INDEX
-- ════════════════════════════════════════════════════

/-- The five components of a Protoreal manifold, indexed by `Fin 5`. -/
abbrev ComponentIdx := Fin 5

/-- Named indices for readability. -/
def idx_a : Fin 5 := ⟨0, by omega⟩
def idx_omega : Fin 5 := ⟨1, by omega⟩
def idx_iota : Fin 5 := ⟨2, by omega⟩
def idx_eps : Fin 5 := ⟨3, by omega⟩
def idx_lam : Fin 5 := ⟨4, by omega⟩

-- ════════════════════════════════════════════════════
-- COMPONENT ACCESS
-- ════════════════════════════════════════════════════

/-- Extract the value of the i-th component of a Protoreal manifold. -/
def component (u : ProtorealManifold) (i : Fin 5) : ℝ :=
  match i with
  | ⟨0, _⟩ => u.a
  | ⟨1, _⟩ => u.b
  | ⟨2, _⟩ => u.m
  | ⟨3, _⟩ => u.e
  | ⟨4, _⟩ => u.l

/-- A component is **active** if it is non-zero.
    An active component participates in the observation. -/
def is_active (u : ProtorealManifold) (i : Fin 5) : Prop :=
  component u i ≠ 0

-- ════════════════════════════════════════════════════
-- THE INTERACTION GRAPH (via edge set)
-- ════════════════════════════════════════════════════

/-- The **structural adjacency** of the Klein multiplication.
    Two component indices are structurally adjacent if they appear
    together in a cross-term of the Klein multiplication rule.

    Defined as a decidable Boolean predicate for `decide`-based proofs. -/
def klein_adj_bool (i j : Fin 5) : Bool :=
  match i.val, j.val with
  | 0, 1 => true  | 1, 0 => true  -- a ↔ ω
  | 0, 2 => true  | 2, 0 => true  -- a ↔ ι
  | 0, 3 => true  | 3, 0 => true  -- a ↔ ε
  | 0, 4 => true  | 4, 0 => true  -- a ↔ λ
  | 1, 2 => true  | 2, 1 => true  -- ω ↔ ι (Bridge)
  | 3, 4 => true  | 4, 3 => true  -- ε ↔ λ (Consolidation)
  | _, _ => false

/-- The Prop-valued adjacency relation. -/
def klein_adj (i j : Fin 5) : Prop :=
  klein_adj_bool i j = true

instance klein_adj_decidable (i j : Fin 5) : Decidable (klein_adj i j) :=
  inferInstanceAs (Decidable (klein_adj_bool i j = true))

/-- Klein adjacency is symmetric. -/
theorem klein_adj_symm (i j : Fin 5) (h : klein_adj i j) : klein_adj j i := by
  unfold klein_adj klein_adj_bool at *
  fin_cases i <;> fin_cases j <;> simp_all

/-- Klein adjacency is irreflexive (no self-loops). -/
theorem klein_adj_irrefl (i : Fin 5) : ¬ klein_adj i i := by
  unfold klein_adj klein_adj_bool
  fin_cases i <;> simp

/-- **THE OBSERVATION GRAPH**
    The full Klein interaction graph on `Fin 5`.
    This is the maximal observation — all 5 components are
    considered as potential interaction sites.

    A Protoreal element u **observes** through this graph
    when all its components are active. -/
def observation_graph : SimpleGraph (Fin 5) :=
  SimpleGraph.mk' ⟨fun i j => klein_adj_bool i j, by
    constructor
    · -- symmetry
      intro x y
      unfold klein_adj_bool
      fin_cases x <;> fin_cases y <;> simp
    · -- irreflexivity
      intro x
      unfold klein_adj_bool
      fin_cases x <;> simp⟩

instance : DecidableRel observation_graph.Adj := by
  intro i j
  unfold observation_graph
  simp [SimpleGraph.mk']
  exact inferInstanceAs (Decidable (klein_adj_bool i j = true))

-- ════════════════════════════════════════════════════
-- ADJACENCY THEOREMS
-- ════════════════════════════════════════════════════

/-- **THE BRIDGE ADJACENCY**: ω and ι are adjacent in the
    observation graph. This is the graph-theoretic image of
    the Bridge Identity ω·ι = -1. -/
theorem bridge_adj : observation_graph.Adj idx_omega idx_iota := by
  decide

/-- **THE CONSOLIDATION ADJACENCY**: ε and λ are adjacent.
    This is the graph-theoretic image of λ·ε = 1. -/
theorem consolidation_adj : observation_graph.Adj idx_eps idx_lam := by
  decide

/-- **REAL COUPLES TO THRUST**: a and ω are adjacent. -/
theorem real_thrust_adj : observation_graph.Adj idx_a idx_omega := by
  decide

/-- **REAL COUPLES TO ANCHOR**: a and ι are adjacent. -/
theorem real_anchor_adj : observation_graph.Adj idx_a idx_iota := by
  decide

/-- **REAL COUPLES TO NOISE**: a and ε are adjacent. -/
theorem real_noise_adj : observation_graph.Adj idx_a idx_eps := by
  decide

/-- **REAL COUPLES TO LEVEL**: a and λ are adjacent. -/
theorem real_level_adj : observation_graph.Adj idx_a idx_lam := by
  decide

/-- **ω AND ε ARE NOT ADJACENT**: There is no direct
    cross-term between Thrust and Noise in Klein multiplication. -/
theorem thrust_noise_not_adj : ¬ observation_graph.Adj idx_omega idx_eps := by
  decide

/-- **ω AND λ ARE NOT ADJACENT**: No direct Thrust-Level
    interaction in the Klein rule. -/
theorem thrust_level_not_adj : ¬ observation_graph.Adj idx_omega idx_lam := by
  decide

/-- **ι AND ε ARE NOT ADJACENT**: No direct Anchor-Noise
    interaction. -/
theorem anchor_noise_not_adj : ¬ observation_graph.Adj idx_iota idx_eps := by
  decide

/-- **ι AND λ ARE NOT ADJACENT**: No direct Anchor-Level
    interaction. -/
theorem anchor_level_not_adj : ¬ observation_graph.Adj idx_iota idx_lam := by
  decide

end ProtorealGraph
