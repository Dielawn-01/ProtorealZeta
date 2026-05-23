import Mathlib.Data.Real.Basic
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.IntervalCases
import LaRueProtorealAlgebra.ProtorealManifold

/-!
# Configuration Sheaves over Task Topologies (𝕌)

**Authors:** LaRue (Theoretical Framework), Antigravity (Formalization)

Encodes model configurations as sections of a sheaf over task topologies.
The sheaf assigns optimal configs to problem types, with restriction maps,
gluing axioms, monotonicity, and topological sort compatibility.
-/

namespace ConfigSheaf

-- ════════════════════════════════════════════════════
-- 1. TASK TOPOLOGY (THE BASE SPACE)
-- ════════════════════════════════════════════════════

/-- Task complexity levels: 0=definitional, 1=algebraic, 2=existential,
    3=universal, 4=recursive, 5=full_manifold -/
abbrev TaskLevel := ℕ

/-- Optimal dimensions assigned by the sheaf section. -/
def optimal_dimensions : TaskLevel → ℕ
  | 0 => 12 | 1 => 12 | 2 => 36 | 3 => 36 | 4 => 36 | _ => 42

/-- Minimum dimensions required per task level. -/
def min_dimensions : TaskLevel → ℕ
  | 0 => 2 | 1 => 6 | 2 => 12 | 3 => 24 | 4 => 36 | _ => 42

-- ════════════════════════════════════════════════════
-- 2. MODEL CAPACITY (THE STALKS)
-- ════════════════════════════════════════════════════

structure ModelCapacity where
  dimensions : ℕ
  is_self_dual : Bool
  has_seed_slot : Bool

def cap_minimal      : ModelCapacity := ⟨12, false, false⟩
def cap_dual_monster : ModelCapacity := ⟨36, true,  true⟩
def cap_full         : ModelCapacity := ⟨42, false, false⟩

-- ════════════════════════════════════════════════════
-- 3. SHEAF RESTRICTION MAPS
-- ════════════════════════════════════════════════════

def capacity_sufficient (cap_dim : ℕ) (task : TaskLevel) : Prop :=
  cap_dim ≥ min_dimensions task

/-- Full capacity (42D) covers ALL task levels 0..5. -/
theorem full_covers_all (t : TaskLevel) (h : t ≤ 5) :
    capacity_sufficient 42 t := by
  unfold capacity_sufficient min_dimensions
  interval_cases t <;> simp

/-- Dual Monster (36D) covers levels 0..4. -/
theorem dual_monster_covers_0_to_4 (t : TaskLevel) (h : t ≤ 4) :
    capacity_sufficient 36 t := by
  unfold capacity_sufficient min_dimensions
  interval_cases t <;> simp

/-- Minimal (12D) covers levels 0..2. -/
theorem minimal_covers_0_to_2 (t : TaskLevel) (h : t ≤ 2) :
    capacity_sufficient 12 t := by
  unfold capacity_sufficient min_dimensions
  interval_cases t <;> simp

-- ════════════════════════════════════════════════════
-- 4. GLUING AXIOM
-- ════════════════════════════════════════════════════

def can_glue (d1 d2 target : ℕ) : Prop := d1 + d2 ≥ target

/-- Monster glue: 18 + 18 = 36 (each half after bitcollapse -3). -/
theorem monster_glue : can_glue 18 18 36 := by unfold can_glue; omega

/-- Asymmetric glue: 29 + 11 = 40 ≥ 36. -/
theorem asymmetric_glue : can_glue 29 11 36 := by unfold can_glue; omega

/-- Internal substrate glue: 11 + 4 = 15 ≥ 12. -/
theorem substrate_internal_glue : can_glue 11 4 12 := by unfold can_glue; omega

-- ════════════════════════════════════════════════════
-- 5. SECTION MONOTONICITY & TOPOLOGICAL SORT
-- ════════════════════════════════════════════════════

/-- Optimal section assigns non-decreasing dimensions. -/
theorem section_monotone (a b : TaskLevel) (hab : a ≤ b) (hb : b ≤ 5) :
    optimal_dimensions a ≤ optimal_dimensions b := by
  unfold optimal_dimensions
  interval_cases b <;> interval_cases a <;> simp_all

/-- Minimum dimensions are monotone. -/
theorem min_dim_monotone (a b : TaskLevel) (hab : a ≤ b) (hb : b ≤ 5) :
    min_dimensions a ≤ min_dimensions b := by
  unfold min_dimensions
  interval_cases b <;> interval_cases a <;> simp_all

/-- Topological sort invariant: if t₁ ≤ t₂, then the capacity
    at t₂ is sufficient for t₁. Bottom-up processing always works. -/
theorem topo_sort_invariant (t1 t2 : TaskLevel) (h : t1 ≤ t2) (h2 : t2 ≤ 5) :
    capacity_sufficient (optimal_dimensions t2) t1 := by
  unfold capacity_sufficient optimal_dimensions min_dimensions
  interval_cases t2 <;> interval_cases t1 <;> simp_all

/-- Self-sufficiency: the sheaf section always provides enough
    for its own task level. -/
theorem section_self_sufficient (t : TaskLevel) (h : t ≤ 5) :
    capacity_sufficient (optimal_dimensions t) t := by
  unfold capacity_sufficient optimal_dimensions min_dimensions
  interval_cases t <;> simp

end ConfigSheaf
