import LaRueProtorealAlgebra.Basic

namespace ProtorealAlgebra

-- Key lemmas or axioms required:
-- 1. funct(u).a = a + ε (Sowing: funct(u) = (a + ε, b, m, 0, l + 1))
-- 2. funct(u).b = b - 1 (After proving a frontier theorem, one less in the frontier)
-- 3. funct(u).m ≤ m (Monotonic decrease in blocked theorems when frontier is chosen by topological sort)

-- Outline:
-- 1. Introduce variables and assumptions
-- 2. Apply funct to the state
-- 3. Simplify the resulting expressions
-- 4. Prove that `a' = a + 1`
-- 5. Prove that `m' ≤ m`

theorem monotonic_decrease_blocked_theorems (u : ProtorealManifold) (h_b_pos : u.b > 0) :
    let u' := funct u in
    u'.a = u.a + 1 ∧ u'.m ≤ u.m :=
by
  -- Step 1: Introduce variables and assumptions
  intro,
  have h_a': u'.a = u.a + 1, by simp [funct],
  have h_b': u'.b = u.b - 1, by simp [funct],

  -- Step 2: Apply funct to the state
  ext,

  -- Step 3: Simplify the resulting expressions
  simp [h_a', h_b'],

  -- Step 4: Prove that `a' = a + 1`
  ring

  -- Step 5: Prove that `m' ≤ m`
  -- Since frontier is chosen by topological sort, proving a theorem decreases blocked theorems
  have h_m': u'.m ≤ u.m, by simp [funct],

  -- Return the final result
  exact ⟨h_a', h_m'⟩,

end ProtorealAlgebra