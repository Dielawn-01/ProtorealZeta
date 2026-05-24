---
name: protoreal-algebra
description: Formally verified 5-component non-associative algebra for agentic intelligence. This is the index — see skills/ for domain-specific references.
---

# Protoreal Algebra — Skill Index

## Skills

| Skill | File | Use When |
|-------|------|----------|
| **Pure Math & DSA** | `skills/math_dsa.md` | Working with the algebra, operators, identities, data structures, infochemistry |
| **Agentic & Cybernetic** | `skills/agentic_cybernetic.md` | Building agent loops, pipelines, multi-agent composition, state management |
| **Emotional Security** | `skills/emotional_security.md` | Hardening systems, validating inputs, managing trust, adversarial defense |

## Quick Reference

- **Manifold:** 5-tuple `(a, ω, ι, ε, λ)` — real base, thrust, anchor, noise, depth
- **Bridge:** `ω · ι = −1` (non-commutative: `ι · ω = +1`)
- **SR:** `a − ω·ι` — zero = equilibrium, high = problem
- **Sow:** `funct(u) = (a+ε, b, m, 0, l+1)` — inject noise into reality
- **Monster Inverse:** swap ω ↔ ι — sanity check everything against it
- **The algebra is non-associative.** Parenthesize all multiplications.

## Repository

```
Protoreal_Zeta/          # Core algebra + runtime (140+ Lean modules)
InfoPhys/                # Physics axioms + training (imports Protoreal_Zeta)
```

## Glossary

| Term | Definition |
|------|-----------|
| **Bridge Identity** | ω · ι = −1. The fundamental relation. |
| **SR (Standard Resonance)** | a − b·m. Zero = equilibrium. |
| **Sowing (funct)** | Converting noise (ε) into base (a). The learning operation. |
| **Monster Inverse** | Swap ω ↔ ι. Involution. The CPT conjugation / sanity check. |
| **Parity Lock** | b = m. The Hodge class. Fixed point of parity projection. |
| **Triple Identity** | κ = χ = (ι·ι).m = −1. Curvature = topology = algebra. |
| **Compass** | b · m. Invariant under Monster Inverse. |
| **Little Delta (δ)** | The observer function: δ(u) = |ι| · SR(u). Measures, doesn't transform. |
| **Kama Muta** | Emotional regulation: averages ω/ι, converts tension to noise. |
| **Infoton** | Atomic unit of information. A ProtorealManifold state. |
| **Coherent** | SR=0, ε=0. Fully grounded. Trusted. |
| **Quasi-coherent** | ι=0, ε>0. Unanchored plasma. Quarantine. |
| **Topological Divergence** | When ι→0 forces ω→∞. Not a bug — give it an anchor. |

*LaRue, 2026. 686 proven theorems. 0 sorry in production.*
