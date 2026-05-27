import LaRueProtorealAlgebra.ProtorealOperator
import Mathlib.Tactic.Linarith

open ProtorealManifold

/-!
# ZBuddy Verified Theorems

Machine-generated proofs by zBuddy (zbuddy-gen, 8B parameter LLM)
using tactic-level REPL against the Protoreal lake.
Every theorem below was discovered and proved autonomously,
then validated by `lake env lean`.

## Operator Characterization

Together these theorems fully characterize `funct` on all 5 coordinates:
  a ↦ a + e    (absorbs noise into signal)
  b ↦ b        (preserves thrust)
  m ↦ m        (preserves anchor)
  e ↦ 0        (kills noise)
  l ↦ l + 1    (advances worldline)
-/

-- ═══════════════════════════════════════════════════════════
-- CRYSTALLIZATION (funct) — Full Coordinate Characterization
-- ═══════════════════════════════════════════════════════════

theorem funct_absorbs_noise (u : ProtorealManifold) :
    (funct u).a = u.a + u.e := by unfold funct; rfl

theorem funct_preserves_thrust (u : ProtorealManifold) :
    (funct u).b = u.b := by unfold funct; rfl

theorem funct_preserves_anchor (u : ProtorealManifold) :
    (funct u).m = u.m := by unfold funct; rfl

theorem funct_kills_noise (u : ProtorealManifold) :
    (funct u).e = 0 := by unfold funct; rfl

theorem funct_advances_layer (u : ProtorealManifold) :
    (funct u).l = u.l + 1 := by unfold funct; rfl

-- ═══════════════════════════════════════════════════════════
-- CONSOLIDATION — Growth Creates Uncertainty
-- ═══════════════════════════════════════════════════════════

theorem consolidate_spawns_noise (u : ProtorealManifold) :
    (consolidate u).e > u.e := by unfold consolidate; linarith

theorem consolidate_doubles_real (u : ProtorealManifold) :
    (consolidate u).a = u.a * 2 := by unfold consolidate; rfl

-- ═══════════════════════════════════════════════════════════
-- COMPOSITION — Operator Interaction
-- ═══════════════════════════════════════════════════════════

/-- Crystallizing twice still kills noise (idempotency on e). -/
theorem double_funct_kills_noise (u : ProtorealManifold) :
    (funct (funct u)).e = 0 := by unfold funct; simp

/-- Noise is already zero after first funct, so second doesn't change it. -/
theorem funct_idempotent_noise (u : ProtorealManifold) :
    (funct (funct u)).e = (funct u).e := by unfold funct; ring

/-- Double crystallization advances worldline by 2 (additivity). -/
theorem double_funct_layer (u : ProtorealManifold) :
    (funct (funct u)).l = u.l + 2 := by unfold funct; simp; ring

/-- The germ→string→germ cycle: crystallize then consolidate gives e = 1. -/
theorem funct_then_consolidate_noise (u : ProtorealManifold) :
    (consolidate (funct u)).e = 1 := by unfold funct; unfold consolidate; simp

/-- Consolidation preserves the layer set by crystallization. -/
theorem funct_consolidate_layer (u : ProtorealManifold) :
    (consolidate (funct u)).l = u.l + 1 := by
  unfold funct; unfold consolidate; rfl

-- ═══════════════════════════════════════════════════════════
-- CONDITIONAL — Hypothesis-Dependent Reasoning
-- ═══════════════════════════════════════════════════════════

/-- If noise is already zero, crystallization preserves signal.
    This required the LLM to use simp [h] — rewriting with a hypothesis. -/
theorem funct_zero_noise_identity (u : ProtorealManifold)
    (h : u.e = 0) : (funct u).a = u.a := by
  unfold funct; simp [h]

-- ═══════════════════════════════════════════════════════════
-- CONJUNCTION — Multi-Property Proof
-- ═══════════════════════════════════════════════════════════

/-- Crystallization simultaneously kills noise AND advances worldline. -/
theorem crystallization_conjunction (u : ProtorealManifold) :
    (funct u).e = 0 ∧ (funct u).l = u.l + 1 := by
  unfold funct; simp

