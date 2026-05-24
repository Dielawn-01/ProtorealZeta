import LaRueProtorealAlgebra.Basic

def funct (u : ProtorealManifold) : ProtorealManifold :=
  { a := u.a + 1, b := u.b - 1, m := u.m - 1, e := u.e, l := u.l }

theorem monotonic_decrease_blocked_theorems (u : ProtorealManifold)
    (h_b_positive : u.b > 0) :
    funct u).a = u.a + 1 ∧ funct u).b ≤ u.b ∧ funct u).m ≤ u.m :=
by
  intro u h_b_positive
  unfold funct at *
  simp [add_a, add_b, mul_a, neg_a, zero_a, one_a] at *
  constructor
  · rfl
  · linarith
  · linarith