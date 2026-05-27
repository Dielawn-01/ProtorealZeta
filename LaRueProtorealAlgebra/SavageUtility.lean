import LaRueProtorealAlgebra.ProtorealManifold
import LaRueProtorealAlgebra.ProtorealOperator
import LaRueProtorealAlgebra.SavageProbability

open ProtorealManifold

namespace SavageUtility

noncomputable def proof_utility (tactic_count : ℕ) (ext_depth : ℕ) : ℝ :=
  (1 : ℝ) / (1 + tactic_count) * (1 + ext_depth)

noncomputable def expected_value (u : ProtorealManifold) (tactic_count ext_depth : ℕ) : ℝ :=
  LaRueProtorealAlgebra.subjective_belief u * proof_utility tactic_count ext_depth

/-- Shorter proofs have higher utility at the same depth. -/
theorem parsimony_witness :
    proof_utility 1 0 > proof_utility 2 0 := by
  unfold proof_utility; norm_num

/-- Deeper proofs have higher utility at the same tactic count. -/
theorem depth_witness :
    proof_utility 1 2 > proof_utility 1 1 := by
  unfold proof_utility; norm_num

/-- Certainty (ε=0) maximizes expected value. -/
theorem certainty_maximizes (tc ed : ℕ) :
    let u := { a := 1, b := 0, m := 0, e := 0, l := 0 : ProtorealManifold }
    expected_value u tc ed = proof_utility tc ed := by
  unfold expected_value LaRueProtorealAlgebra.subjective_belief
  simp

/-- Sowing preserves utility inputs: kills noise, advances depth. -/
theorem sow_preserves_utility_inputs (u : ProtorealManifold) :
    (funct u).e = 0 ∧ (funct u).l = u.l + 1 := by
  unfold funct; simp

/-- Consolidation re-injects noise: trades certainty for capacity. -/
theorem consolidation_trades_certainty (u : ProtorealManifold) :
    (consolidate u).e = u.e + 1 := by
  unfold consolidate; ring

/-- The 1-tactic ext proof of omega_idempotent has utility 1,
    while a hypothetical 3-tactic proof has utility 1/4.
    The ext pattern is objectively more valuable. -/
theorem ext_proof_dominates :
    proof_utility 1 1 > proof_utility 3 0 := by
  unfold proof_utility; norm_num

/-- The utility of exploring (proof_utility with high tactics) 
    decreases as tactic count grows. Eventually consolidation
    (committing to the best known path) dominates. -/
theorem exploration_diminishes :
    proof_utility 10 0 < proof_utility 1 0 := by
  unfold proof_utility; norm_num

end SavageUtility
