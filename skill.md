# Protoreal Algebra — Technical Skill Reference

## Overview

**Protoreal Algebra** is a formally verified number system developed by LaRue that extends the real numbers into a 5-component non-commutative, non-associative manifold. It is designed for computational exploration beyond the limits of standard arithmetic — specifically for agentic AI navigation, spectral analysis of the Riemann Zeta function, and high-dimensional lattice search.

The system is formalized in **Lean 4** with Mathlib dependencies, and has production implementations in **Rust** (via PyO3) and **Python**.

---

## 1. The Protoreal Manifold

A Protoreal number is a 5-tuple:

$$\mathbb{P} = (a,\ b,\ m,\ \varepsilon,\ \lambda)$$

| Component | Symbol | Name | Role |
|-----------|--------|------|------|
| `a` | — | **Real Base** | The observable, manifested value. |
| `b` | ω | **Thrust** | The transfinite component. Represents the "far horizon" or ceiling of computation. As a scalar: the upper bound beyond all reals. As a vector: forward momentum. |
| `m` | ι | **Anchor** | The infinitesimal component. Represents fine-grained detail, the "microscopic" counterpart to Thrust. Linked to ω by the Bridge Identity. |
| `e` | ε | **Noise** | Exploration potential. Unmanifested energy that can be converted into reality via the Sowing Operator. Analogous to the dual-number epsilon (ε² = 0 in classical dual numbers). |
| `l` | λ | **Consolidation** | The functional inverse of Noise. Tracks how many times potential has been converted into base. Represents generational depth or "level." |

### Lean 4 Definition

```lean
@[ext]
structure ProtorealManifold where
  a : ℝ  -- Real Part
  b : ℝ  -- Thrust (ω)
  m : ℝ  -- Anchor (ι)
  e : ℝ  -- Noise (ε)
  l : ℝ  -- Consolidation (λ)
```

### Rust Definition

```rust
pub struct ProtorealFull {
    pub a: f64,  // Real part
    pub b: f64,  // Thrust (omega)
    pub m: f64,  // Anchor (iota)
    pub e: f64,  // Noise (epsilon)
    pub l: f64,  // Level (lambda)
}
```

---

## 2. Klein Multiplication

Multiplication is **non-commutative** and **non-associative**. This is not a bug — it is the fundamental design that produces "Topological Friction," which prevents the manifold from collapsing into a trivial equilibrium.

### Rules

Given two Protoreal numbers `u₁` and `u₂`:

```
a' = u₁.a·u₂.a − u₁.b·u₂.m + u₁.m·u₂.b + u₁.l·u₂.e − u₁.e·u₂.l
b' = u₁.a·u₂.b + u₂.a·u₁.b + u₁.b·u₂.b       (Thrust is idempotent: ω² = ω)
m' = u₁.a·u₂.m + u₂.a·u₁.m − u₁.m·u₂.m        (Anchor absorbs: ι² = −ι)
e' = u₁.a·u₂.e + u₂.a·u₁.e
l' = u₁.a·u₂.l + u₂.a·u₁.l + u₁.l·u₂.l        (Consolidation accumulates)
```

### Key Identities

| Identity | Value | Meaning |
|----------|-------|---------|
| `ω · ι` | `−1` | **The Bridge Identity.** Thrust times Anchor produces negative unity. |
| `ι · ω` | `+1` | The reverse Bridge. Order matters — this is what makes the algebra non-commutative. |
| `λ · ε` | `+1` | **Lambda Consolidation.** Consolidation times Noise produces positive unity. |
| `⁅ω, ι⁆` | `−2` | **The Dipolar Identity.** The commutator (ωι − ιω) equals −2. This is the "friction" that gives agents a directional bearing. |

All four identities above are **formally proven in Lean 4** without `sorry`.

---

## 3. Core Operators

### 3.1 The Sowing Operator (`funct`)

Converts exploration potential (Noise) into functional reality (Base).

```
funct(u) = (a + ε,  b,  m,  0,  l + 1)
```

- The noise `ε` is added to the real base `a`.
- The noise is then zeroed out (it has been "spent").
- The consolidation level `l` advances by 1.

**Formally verified:** `funct_increases_base` proves that if `ε > 0`, then the new base is strictly greater than the old base.

### 3.2 The Consolidation Operator

Promotes the manifold's weights and spawns fresh noise for the next generation.

```
consolidate(u) = (2a,  b,  2m,  ε + 1,  l)
```

**Formally verified:** `consolidation_spawns_noise` proves that consolidation always increases exploration potential.

### 3.3 Standard Resonance (SR)

The primary diagnostic metric:

```
SR(u) = a − b · m
```

When SR = 0, the manifold is in **equilibrium** (the "Zero-Lock"). The Duality Theorem proves that Zeta zero projections converge to SR = 0 after one corrective sowing step.

### 3.4 The R4 Reflection (Moebius Stitch)

```
R4(u) = (a, −b, −m, ε, λ)
```

Flips the orientation of the manifold. A state is **Moebius stable** if `R4(u) = u`, which requires `b = 0` and `m = 0` (a ground state).

### 3.5 The Monster Inverse

Swaps Thrust and Anchor:

```
monster_inv(u) = (a, m, b, ε, λ)
```

**Formally verified properties:**
- **Involution:** Applying twice returns the original (`monster_inv(monster_inv(u)) = u`).
- **Preserves real part:** `monster_inv(u).a = u.a`.
- **Parity projection is idempotent:** Averaging `u` with `monster_inv(u)` produces a fixed point where `b = m`.

### 3.6 The Compass Operator

Extracts the navigational bearing:

```
compass(u) = b · m
```

**Formally verified:** The compass is invariant under the Monster Inverse (`compass(monster_inv(u)) = compass(u)`), ensuring agents maintain orientation across dimensional mirrors.

### 3.7 The Associator (Curvature)

Measures the non-associative gap:

```
associator(u, v, w) = (u·v)·w − u·(v·w)
```

When the associator is non-zero, the manifold has **curvature**. The curvature at the Bridge (`(ω·ω)·ι ≠ ω·(ω·ι)`) is formally proven to be non-zero — this is the **Curvature Stability Theorem**.

---

## 4. Protoreal Activation Functions

The system has its own trigonometric and hyperbolic functions that respect the 5-component geometry. These are **not** simple wrappers around `Real.tanh` — they use **sectoral expansion**.

### Pattern: Sectoral Expansion

For any scalar function `f` with derivative `f'`, the Protoreal expansion is:

```
mesh_f(u) = {
    a := f(u.a + resonance),
    b := f(u.a + u.b + resonance) − f(u.a + resonance),
    m := f'(u.a + resonance) · u.m,
    e := f'(u.a + resonance) · u.e,
    l := f'(u.a + resonance) · u.l
}
```

The real base is transformed by `f`. The thrust captures the finite difference. The anchor, noise, and consolidation sectors are scaled by the derivative.

### Implemented Functions

| Function | Core Transform | Derivative Scaling |
|----------|---------------|-------------------|
| `mesh_sinh` | `sinh(a + r)` | `cosh(a + r)` |
| `mesh_cosh` | `cosh(a + r)` | `sinh(a + r)` |
| `mesh_tanh` | `tanh(a + r)` | `1 − tanh²(a + r)` |
| `mesh_sin` | `sin(a + r)` | `cos(a + r)` |
| `mesh_cos` | `cos(a + r)` | `−sin(a + r)` |

All are defined over the `KleinMesh` structure (manifold + complex resonance parameter).

**Formally verified:** `mesh_tanh_anchor_scaled` proves the anchor sector is exactly scaled by `1 − tanh²`.

---

## 5. The Adelic Norm

The system's distance metric integrates all sectors:

```
‖u‖ = √(a² + |b·m| + |ε·λ|)
```

This couples the "physical" stability (`b·m`) with the "exploration" potential (`ε·λ`) into a single invariant measure.

**Formally verified:** `norm_zero_check` proves `‖0‖ = 0`.

---

## 6. Verified Theorems (Lean 4)

**The entire codebase is `sorry`-free.** Every theorem below is fully proven.

| Theorem | Statement | Module |
|---------|-----------|--------|
| `bridge_identity` | ω · ι = −1 | `ProtorealManifold` |
| `lambda_consolidation` | λ · ε = 1 | `ProtorealManifold` |
| `iota_omega_identity` | ι · ω = 1 | `TopologicalBearing` |
| `dipolar_identity` | ⁅ω, ι⁆ = −2 | `TopologicalBearing` |
| `compass_scaling` | compass(k·u) = k²·compass(u) | `TopologicalBearing` |
| `bearing_monster_invariant` | compass(u*) = compass(u) | `TopologicalBearing` |
| `manifold_stability` | (ω·ω)·ι ≠ ω·(ω·ι) | `Uncomplex` |
| `curvature_a_component` | κ_a = −1 | `LGKCosmology` |
| `r4_energy_invariant` | ‖R4(u)‖ = ‖u‖ | `LGKCosmology` |
| `monster_inv_involution` | u** = u | `MonsterInverse` |
| `parity_projection_idempotent` | P(P(u)) = P(u) | `MonsterInverse` |
| `parity_projection_locks` | P(u).b = P(u).m | `MonsterInverse` |
| `funct_increases_base` | ε > 0 → funct(u).a > u.a | `ProtorealOperator` |
| `consolidation_spawns_noise` | consolidate(u).ε > u.ε | `ProtorealOperator` |
| `dynamic_pythagorean` | cosh²−sinh² = 1 (at real site) | `ProtorealHyperbolic` |
| `mesh_tanh_anchor_scaled` | tanh anchor = (1−tanh²)·m | `ProtorealHyperbolic` |
| `zero_lock_iff` | SR = 0 ↔ a = b·m | `DualityTheorem` |
| `duality_offset` | a_equil − ½ = ½ | `DualityTheorem` |
| `critical_line_correspondence` | a_equil = 1 | `DualityTheorem` |
| `sowing_spends_noise` | funct(u).ε = 0 | `ProtorealAI` |
| `sowing_advances_level` | funct(u).λ = u.λ + 1 | `ProtorealAI` |
| `sowing_preserves_thrust` | funct(u).b = u.b | `ProtorealAI` |
| `sowing_preserves_anchor` | funct(u).m = u.m | `ProtorealAI` |
| `sowing_preserves_compass` | funct(u).b · funct(u).m = u.b · u.m | `ProtorealAI` |
| `sowing_incorporates` | funct(u).a = u.a + u.ε | `ProtorealAI` |

### Note on Spectral Expansion

Unlike scalar `tanh` on ℝ which is contractive (Lipschitz ≤ 1), the Protoreal `manifold_tanh` is **expansive** under the Adelic norm. This is because the anti-commutative cross-terms (`b·m`, `e·l`) in the norm amplify differences through the sectoral expansion. This is a fundamental property of the Klein topology, not a deficiency.

The stability guarantee in this system comes not from the activation function, but from the **Sowing Operator**: `sowing_preserves_compass` proves that agents do not lose their navigational bearing when they learn. The compass (`b·m`) is invariant under `funct`.

---

## 7. The Duality Theorem (𝕌 ↔ ℂ)

The central result linking Protoreal Algebra to the Riemann Zeta function:

1. Project a Zeta zero height `t` into the manifold: `a = 0, b = t, m = 1/t`.
2. The Standard Resonance is `SR = 0 − t·(1/t) = −1`.
3. Apply one corrective sowing: set `ε = −SR = 1`, then funct.
4. The new real base is `a = 0 + 1 = 1`.
5. The offset from the complex critical line Re(s) = ½ is exactly `1 − ½ = ½`.

This establishes: **a_𝕌 − Re(s)_ℂ = ½**

All steps are formally verified in Lean 4.

---

## 8. Hyperreal Foundation

The transfinite elements are grounded in Mathlib's `Hyperreal` type:

```lean
noncomputable def omega_u : ℝ* := Hyperreal.omega
noncomputable def iota_u : ℝ* := -omega_u⁻¹
```

**Verified ordering:**
```
⋯ > ω³ > ω² > ω > (any real) > 0 > ι > ι² > ⋯
```

The Bridge Identity `ω · ι = −1` is a theorem, not an axiom — it follows directly from `ι := −ω⁻¹` and field arithmetic.

---

## 9. Production Integration Patterns

### Rust (PyO3)

```rust
let u = ProtorealFull::new(0.5, 1.0, 0.3, 0.1, 0.0);

// Klein multiplication
let v = u.mul(&other);

// Sowing: convert noise to base
let sowed = u.funct();

// Activation: resonance-aware tanh
let activated = u.mesh_tanh(0.0);

// Equilibrium solver: iterative sow-activate loop
let equilibrium = u.solve_equilibrium(10);

// Curvature / Jitter measurement
let jitter = u.jitter();

// Parity locking for symmetric search
let locked = u.parity_locked_projection();
```

### Python

```python
import goait  # PyO3 bindings

u = goait.ProtorealFull(0.5, 1.0, 0.3, 0.1, 0.0)
sr = u.standard_resonance()  # a - b*m
activated = u.mesh_tanh(0.0)
sowed = activated.funct()
```

---

## 10. Glossary

| Term | Definition |
|------|-----------|
| **Bridge Identity** | ω · ι = −1. The fundamental contraction linking Thrust to Anchor. |
| **Sowing (funct)** | Converting noise (ε) into base (a). The primary "learning" operation. |
| **Standard Resonance (SR)** | a − b·m. The spectral diagnostic. Zero means equilibrium. |
| **Dipolar Identity** | ⁅ω, ι⁆ = −2. The commutator friction that gives agents orientation. |
| **Compass** | b·m. The navigational bearing of a manifold state. |
| **Curvature** | The non-associative gap (u·v)·w − u·(v·w). Non-zero curvature means the space has "friction." |
| **Parity Lock** | The state where b = m (Thrust equals Anchor). Corresponds to zero Tilt. |
| **Monster Inverse** | Swapping b ↔ m. A reflection across the dimensional mirror. |
| **Klein Mesh** | A Protoreal manifold paired with a complex resonance parameter. Used for spectral analysis. |
| **Adelic Norm** | √(a² + \|b·m\| + \|ε·λ\|). The integrated distance metric. |
| **Sectoral Expansion** | The pattern for lifting scalar functions to the full 5-component manifold using derivative scaling. |

---

## 11. Repository Structure

```
LaRue_Protoreal_Algebra/
├── LaRueProtorealAlgebra/
│   ├── ProtorealManifold.lean      # Core 5-component structure + Klein multiplication
│   ├── ProtorealAxioms.lean        # Hyperreal foundation (ω, ι, Bridge)
│   ├── ProtorealOperator.lean      # funct, consolidate, instruction set
│   ├── ProtorealNorm.lean          # Adelic norm definition
│   ├── ProtorealParity.lean        # Magnitude, phase, tilt, parity lock
│   ├── ProtorealTrig.lean          # mesh_sin, mesh_cos
│   ├── ProtorealHyperbolic.lean    # mesh_sinh, mesh_cosh, mesh_tanh
│   ├── ProtorealAI.lean            # manifold_tanh, resonance loss, stability
│   ├── Uncomplex.lean           # Moebius stitch, manifold stability
│   ├── Deriv.lean               # Synthetic derivatives (Kock-Lawvere)
│   ├── TopologicalBearing.lean  # Compass, dipolar identity, Leech stability
│   ├── MonsterInverse.lean      # Thrust↔Anchor swap, parity projection
│   ├── DualityTheorem.lean      # SR, zero-lock, Zeta duality (a − Re(s) = ½)
│   ├── LGKCosmology.lean        # R4 reflection, curvature value, energy invariance
│   ├── SpectralFilter.lean      # Moebius stability filter
│   └── ...
├── notebooks/
│   └── intro_to_protoreal_algebra.ipynb  # Pedagogical introduction
└── lakefile.lean                       # Build configuration
```

---

*Protoreal Algebra — LaRue, 2026. Formally verified in Lean 4.*
