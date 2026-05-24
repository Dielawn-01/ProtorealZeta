---
name: protoreal-algebra
description: 5-component non-associative algebra for agentic intelligence. Use when building autonomous systems, spectral analysis, or topological reasoning.
---

# Protoreal Algebra — Skill Reference

## 1. The Manifold

A Protoreal number is a 5-tuple: `(a, ω, ι, ε, λ)`

| Field | Name | Role |
|-------|------|------|
| `a` | **Real Base** | Observable value |
| `b` (ω) | **Thrust** | Transfinite/forward momentum |
| `m` (ι) | **Anchor** | Infinitesimal/grounding |
| `e` (ε) | **Noise** | Exploration potential |
| `l` (λ) | **Consolidation** | Generational depth |

```lean
@[ext]
structure ProtorealManifold where
  a : ℝ ; b : ℝ ; m : ℝ ; e : ℝ ; l : ℝ
```

## 2. Key Identities

| Identity | Value | Meaning |
|----------|-------|---------|
| `ω · ι` | `−1` | **Bridge Identity** — thrust × anchor = negative unity |
| `ι · ω` | `+1` | Reverse Bridge — non-commutative |
| `⁅ω, ι⁆` | `−2` | **Dipolar Identity** — commutator |
| `κ = χ = (ι·ι).m` | `−1` | **Triple Identity** — curvature = topology = algebra |

**Klein multiplication is non-commutative AND non-associative.** Parenthesize everything.

## 3. Core Operators

| Operator | Transform | When to Use |
|----------|-----------|-------------|
| `funct` (sow) | `(a+ε, b, m, 0, l+1)` | Agent stuck, SR stale, ε > 0 |
| `consolidate` | `(2a, b, 2m, ε+1, l)` | High confidence, SR ≈ 0 |
| `monster_inv` | `(a, m, b, ε, λ)` | Sanity check — swap ω ↔ ι |
| `parity_projection` | `(a, (b+m)/2, (m+b)/2, ε, λ)` | Force Hodge class (b = m) |
| `SR` | `a − b·m` | Primary diagnostic |

**Rule:** Sow early and often. Consolidate rarely. Never consolidate when SR ≠ 0.

## 4. Agent Design Patterns

### The Loop
```
Observe → Perceive (χ = −1?) → Intuit (intent × observation) → Sow → Converge (SR → 0) → Compose → Act
```

### SR as Error Signal
| SR | State | Action |
|----|-------|--------|
| `= 0` | Equilibrium | Safe to act |
| `> 0` | Base ahead of spectrum | Observe more |
| `< 0` | Spectrum pulling | Sow to catch up |
| `> 1.0` | Far from equilibrium | Audit for injection |

### State = Checkpoint
The 5-tuple IS your state. `λ` = iteration count, `ε > 0` = has noise, `SR ≈ 0` = converged. 40 bytes total.

## 5. Agentic Security

### SR-Based Threat Detection
```rust
fn security_check(state: &KleinManifold) -> SecurityLevel {
    let sr = (state.a - state.b * state.m).abs();
    if sr < 0.01 { Clear } else if sr < 1.0 { Elevated } else if sr < 10.0 { Alert } else { Compromised }
}
```

### Monster Inverse Defense
Any legitimate operation survives `monster_inv`. If `f(u).a ≠ f(u*).a`, the operation exploits asymmetry — reject it.

### Trust Hierarchy (from Infochemistry.lean)
| State | Sheaf Type | Trust |
|-------|-----------|-------|
| **Coherent** (SR=0, ε=0) | Coherent sheaf | Full trust |
| **Quasi-coherent** (ι=0, ε>0) | Quasi-coherent | Verify first |
| **Plasma** (ionized) | None | Quarantine |

**Rule:** Never let plasma state modify coherent state directly.

### Access Control (from MatterAntimatter.lean)
| Space | Condition | Access |
|-------|-----------|--------|
| Possibility (DHT) | All states | Could be requested |
| Probability | ε ≥ 0 | Can be evaluated |
| Matter | SR=0, ε=0 | Has been verified |

Inputs arrive in possibility space → validate to probability → commit only at matter.

### λ-Gated Privileges
λ = 0–2: read-only. λ = 3–10: write. λ = 11+: admin. **Consolidation is irreversible.**

## 6. Infochemistry (InfoPhysAxioms)

The **Infoton** is the atomic unit of information — a ProtorealManifold state.

| Operation | What It Does |
|-----------|-------------|
| `bond(u, v)` | Average orbitals, sum energy, conserve parity |
| `ionize(u)` | Strip anchor (ι → 0), release confinement energy as noise |
| `kama_muta` | Average ω and ι — emotional regulation |
| `funct(kama_muta(ionize(u)))` | **Fusion** — ionize, regulate, sow = energy growth |

The infoton sits between matter (ω) and antimatter (ι). Parity-locked states (ω = ι) are their own antiparticle.

## 7. Key Theorems

### Core Algebra
| Theorem | Module |
|---------|--------|
| `bridge_identity` (ω·ι = −1) | `ProtorealAxioms` |
| `triple_identity` (κ = χ = −1) | `StructuralHeterogeneity` |
| `monster_inv_involution` (u** = u) | `MonsterInverse` |
| `funct_increases_base` | `ProtorealOperator` |
| `mass_gap_positive` | `MassGap` |
| `awareness` (6 ingredients) | `Awareness` |

### InfoPhysics
| Theorem | Module |
|---------|--------|
| `analogical_transfer` | `TopologicalProblemSolving` |
| `bond_conserves_energy` | `Infochemistry` |
| `ionize_produces_plasma` | `Infochemistry` |
| `matter_in_probability` (⊂ chain) | `MatterAntimatter` |
| `antimatter_exists` (CPT) | `MatterAntimatter` |
| `annihilation_is_hodge` | `MatterAntimatter` |
| `matter_is_coherent` | `MatterAntimatter` |

**140+ Lean modules. 686 proven theorems. Full reference: `skill_reference.md`**

## 8. Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| Sowing with ε = 0 | Check ε first — sow does nothing if empty |
| Forgetting non-commutativity | A·B ≠ B·A. Bridge gives −1 one way, +1 the other |
| Consolidating too early | Doubles a. Only when SR ≈ 0 |
| Treating ε as random | ε is structured nilpotent noise, not a RNG |
| Parity projection on production state | Checkpoint first — annihilation is irreversible |

## 9. Repository Layout

```
Protoreal_Zeta/                     # Core algebra
├── LaRueProtorealAlgebra/          # 140+ Lean 4 modules
├── zProto/                         # Rust runtime
└── skill.md                        # This file

InfoPhys/                           # Physics axioms + training
├── InfoPhysAxioms/                 # Lean 4 (imports Protoreal_Zeta)
│   ├── Infochemistry.lean
│   ├── MatterAntimatter.lean
│   └── TopologicalProblemSolving.lean
├── overnight_lab.py                # Autonomous training loop
└── rag/                            # RAG index
```
