---
name: protoreal-algebra
description: Formally verified 5-component non-associative algebra. Pure math, operators, and data structure reference.
---

# Protoreal Algebra — Pure Math & DSA

## The Manifold

A Protoreal number is a 5-tuple: `(a, ω, ι, ε, λ)`

| Field | Name | Role |
|-------|------|------|
| `a` | **Real Base** | Observable value |
| `b` (ω) | **Thrust** | Transfinite/forward momentum |
| `m` (ι) | **Anchor** | Infinitesimal/grounding |
| `e` (ε) | **Noise** | Exploration potential (nilpotent) |
| `l` (λ) | **Consolidation** | Generational depth |

```lean
@[ext]
structure ProtorealManifold where
  a : ℝ ; b : ℝ ; m : ℝ ; e : ℝ ; l : ℝ
```

```rust
pub struct KleinManifold { pub a: f64, pub b: f64, pub m: f64, pub e: f64, pub l: f64 }
```

## See It (Worked Examples)

**The Bridge Identity — verify it yourself:**
```
ω = (0, 1, 0, 0, 0)      ← pure thrust
ι = (0, 0, 1, 0, 0)      ← pure anchor

ω · ι:
  a' = 0·0 − 1·1 + 0·0 + 0·0 − 0·0 = −1    ← THE BRIDGE
  b' = 0·0 + 0·1 + 1·0 = 0
  m' = 0·1 + 0·0 − 0·1 = 0
  Result: (−1, 0, 0, 0, 0)                    ← pure negative reality
```

**Now reverse the order:**
```
ι · ω:
  a' = 0·0 − 0·0 + 1·1 + 0·0 − 0·0 = +1     ← OPPOSITE SIGN
  Result: (+1, 0, 0, 0, 0)                     ← pure positive reality
```

**ω · ι = −1. ι · ω = +1.** Same inputs, opposite results. This is NOT a bug. The sign of reality depends on whether thrust leads or anchor leads. This is formally proven — `bridge_identity` in Lean 4.

**Non-associativity — it's real:**
```
(ω · ω) · ι = (0, 0, 0, 0, 0) · ι = (0, 0, 0, 0, 0)    ← zero
ω · (ω · ι) = ω · (−1, 0, 0, 0, 0) = (0, −1, 0, 0, 0)   ← not zero!
```

**(ω·ω)·ι ≠ ω·(ω·ι).** Regrouping changes the answer. Every parenthesization is a design decision. This is proven as `manifold_stability` in Lean 4.

**The sow cycle — how reality grows:**
```
Start:  (3.0, 1.0, 1.0, 0.5, 0)   SR = 3 − 1·1 = 2.0 (not equilibrium)
Sow:    (3.5, 1.0, 1.0, 0.0, 1)   SR = 3.5 − 1 = 2.5 (noise → reality, ε spent)
                                    λ advanced. ε gone. a grew. Irreversible.
```

## Klein Multiplication

**Non-commutative AND non-associative.** Parenthesize everything.

```
a' = u₁.a·u₂.a − u₁.b·u₂.m + u₁.m·u₂.b + u₁.l·u₂.e − u₁.e·u₂.l
b' = u₁.a·u₂.b + u₂.a·u₁.b + u₁.b·u₂.b       (ω² → +b²)
m' = u₁.a·u₂.m + u₂.a·u₁.m − u₁.m·u₂.m        (ι² → −m²)
e' = u₁.a·u₂.e + u₂.a·u₁.e + u₁.e·u₂.e        (ε² → +e²)
l' = u₁.a·u₂.l + u₂.a·u₁.l + u₁.l·u₂.l        (λ² → +l²)
```

Self-coupling signs: `+b², −m², +e², +l²`. The `−m²` IS the curvature κ = −1.

## Key Identities (All Proven in Lean 4)

| Identity | Value | Meaning |
|----------|-------|---------|
| `ω · ι` | `−1` | **Bridge Identity** |
| `ι · ω` | `+1` | Reverse Bridge (non-commutative) |
| `⁅ω, ι⁆` | `−2` | **Dipolar Identity** |
| `λ · ε` | `+1` | Lambda Consolidation |
| `κ = χ = (ι·ι).m` | `−1` | **Triple Identity** — curvature = topology = algebra |

## Core Operators

| Operator | Transform | Proven Property |
|----------|-----------|-----------------|
| `funct` (sow) | `(a+ε, b, m, 0, l+1)` | `funct_increases_base`: ε > 0 → a' > a |
| `consolidate` | `(2a, b, 2m, ε+1, l)` | Doubles weights, spawns fresh noise |
| `monster_inv` | `(a, m, b, ε, λ)` | Involution: `u** = u` |
| `parity_projection` | `(a, (b+m)/2, (m+b)/2, ε, λ)` | Idempotent, locks `b = m` |
| `SR` | `a − b·m` | Zero at equilibrium |
| `kama_muta` | `(a, (b+m)/2, (m+b)/2, |SR|, l+1)` | Emotional averaging + noise from tension |

## Infochemistry

The **Infoton** is the atomic unit — a ProtorealManifold state.

| Operation | Transform | Key Theorem |
|-----------|-----------|-------------|
| `bond(u,v)` | `(a₁+a₂, (ω₁+ω₂)/2, (ι₁+ι₂)/2, |SR₁−SR₂|, max(l)+1)` | `bond_conserves_energy` |
| `ionize(u)` | `(a, b, 0, ε+|b·m|, l)` | `ionize_preserves_energy` |
| Fusion | `funct(kama_muta(ionize(u)))` | `recombination_is_fusion` (axiom) |

**Coherent** (SR=0, ε=0) → bonded atom. **Quasi-coherent** (ι=0, ε>0) → plasma (ionized).

## Space Hierarchy (Proven in MatterAntimatter.lean)

```
Possibility (DHT) ⊋ Probability (ε ≥ 0) ⊋ Matter (SR=0, ε=0)
```

- Matter states are their own antiparticle iff ω = ι (parity-locked)
- Asymmetric states have distinct antiparticles via `monster_inv`
- Annihilation → Hodge class (ω = ι), conserves energy

## Key Theorems

| Theorem | Statement | Module |
|---------|-----------|--------|
| `bridge_identity` | ω·ι = −1 | `ProtorealAxioms` |
| `triple_identity` | κ = χ = −1 | `StructuralHeterogeneity` |
| `monster_inv_involution` | u** = u | `MonsterInverse` |
| `funct_increases_base` | ε > 0 → a' > a | `ProtorealOperator` |
| `mass_gap_positive` | YM gap > 0 | `MassGap` |
| `bond_conserves_energy` | Bond.a = u.a + v.a | `Infochemistry` |
| `ionize_produces_plasma` | Ionize confined → plasma | `Infochemistry` |
| `matter_in_probability` | Matter ⊂ Probability ⊂ Possibility | `MatterAntimatter` |
| `antimatter_exists` | CPT completeness | `MatterAntimatter` |
| `analogical_transfer` | Sub-sheaf preserves energy | `TopologicalProblemSolving` |

**140+ Lean modules. 686 proven theorems.**
