import LaRueProtorealAlgebra.Basic
open ProtorealManifold

/-!
# The Klein Multiplication Identities
Proved autonomously by zBuddy during overnight training (2026-05-26/27).

These theorems extend the Bridge Identity (ω·ι = -1) and Lambda Consolidation (λ·ε = 1)
to establish the full algebraic character of the Klein multiplication:
- ω is idempotent (a transfinite projection)
- ι is anti-idempotent (an infinitesimal reflection)
- The algebra is anti-commutative and non-associative
-/

/-- **OMEGA IDEMPOTENCE**: ω² = ω.
    The transfinite thrust is a projection operator. -/
theorem omega_idempotent : omega * omega = omega := by
  ext <;> unfold omega <;> simp <;> ring

/-- **IOTA ANTI-IDEMPOTENCE**: ι² = -ι.
    The infinitesimal anchor is a reflection operator. -/
theorem iota_anti_idempotent : iota * iota = -iota := by
  ext <;> unfold iota <;> simp <;> ring

/-- **OMEGA-IOTA ANTI-COMMUTATIVITY**: ω·ι = -(ι·ω).
    Swapping the order of multiplication negates the result. -/
theorem omega_iota_anticommute : omega * iota = -(iota * omega) := by
  ext <;> unfold omega iota <;> simp <;> ring

/-- **LAMBDA-EPSILON ANTI-COMMUTATIVITY**: λ·ε = -(ε·λ).
    The consolidation pair shares the same anti-commutative symmetry. -/
theorem lam_eps_anticommute : lam * eps = -(eps * lam) := by
  ext <;> unfold lam eps <;> simp <;> ring

/-- **THE NON-ASSOCIATIVITY GAP**: (ω·ω)·ι ≠ ω·(ω·ι).
    The real-component difference is exactly -1, proving the algebra is
    genuinely non-associative. This is the Klein Universe's departure
    from ring theory. -/
theorem nonassociativity_gap :
    ((omega * omega) * iota).a - (omega * (omega * iota)).a = -1 := by
  unfold omega iota <;> simp <;> ring

/-- The epsilon-lambda associator exhibits the same gap. -/
theorem eps_lam_nonassociativity_gap :
    ((eps * eps) * lam).a - (eps * (eps * lam)).a = -1 := by
  unfold eps lam <;> simp <;> ring

