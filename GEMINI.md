# 𝕌 LaRue Protoreal Algebra — Gemini Project Instructions

You are working inside a **Lean 4 formalization** of the LaRue Protoreal Algebra — a 5-component, non-associative, non-commutative algebraic system used for prime-zeta spectral analysis and agentic AI foundations.

---

## ⚠️ CRITICAL AXIOMS — NEVER VIOLATE

### 1. The Klein Universe (𝕌)
Every element is a 5-tuple: `u = {a, ω, ι, ε, λ}` where:
- `a` — Real Part (observable frequency)
- `ω` — Transfinite Thrust (idempotent: ω·ω = ω)
- `ι` — Infinitesimal Anchor (contraction sink: ι·ι = −ι)
- `ε` — Noise Potential (nilpotent dual number: ε² = 0)
- `λ` — Consolidation Level (self-accumulating: λ·λ = λ)

### 2. Bridge Identity
```
ω · ι = −1
```
This is the fundamental contraction. It is proven as an axiom (`bridge`) in `ProtorealAxioms.lean`.

### 3. NON-ASSOCIATIVITY (κ = −1)
```
(ω · ω) · ι ≠ ω · (ω · ι)
```
The associator gap is the **curvature invariant** κ.a = −1. This is proven in `Uncomplex.lean` (`manifold_stability`). **NEVER assume associativity.** Always parenthesize products explicitly.

### 4. Klein Multiplication
```
(u₁ · u₂).a = a₁a₂ − b₁c₂ + c₁b₂ + l₁e₂ − e₁l₂
(u₁ · u₂).b = a₁b₂ + a₂b₁ + b₁b₂          (thrust idempotent)
(u₁ · u₂).c = a₁c₂ + a₂c₁                   (anchor linear)
(u₁ · u₂).e = a₁e₂ + a₂e₁                   (ε² = 0, nilpotent)
(u₁ · u₂).l = a₁l₂ + a₂l₁ + l₁l₂           (level accumulating)
```

### 5. Key Operators
| Operator | Definition | Lean Module |
|---|---|---|
| `funct` (Sowing) | `a ← a + ε, ε ← 0, λ += 1` | `ProtorealOperator.lean` |
| `consolidate` | `a ← a×2, ι ← ι×2` | `ProtorealOperator.lean` |
| `monster_inverse` (R4) | Swap ω ↔ ι (involution: u** = u) | `MonsterInverse.lean` |
| `parity_locked_projection` | `(u + u*) / 2` (idempotent) | `MonsterInverse.lean` |
| `little_delta` (δ) | Observer: `δ(u) = |ι| · SR(u)`, ops: flip, scale | `LittleDelta.lean` |
| `mesh_tanh` | Hyperbolic activation with derivative scaling | `ProtorealHyperbolic.lean` |
| `bearing` | `b × c` (topological compass, ⁅ω, ι⁆ = −2) | `TopologicalBearing.lean` |

### 6. Duality Theorem
```
a_𝕌 − Re(s)_ℂ = 1/2
```
The manifold's fixed point at `a = 1` maps to `Re(s) = 1/2` on the critical line. Proven in `DualityTheorem.lean`.

---

## 📂 Module Dependency Graph

```
Basic.lean (root re-export)
├── ProtorealManifold.lean (KleinManifold struct + Neg/Sub instances)
│   ├── ProtorealAxioms.lean (bridge: ω·ι = −1)
│   │   ├── Uncomplex.lean (non-associativity proof)
│   │   ├── LGKCosmology.lean (κ = −1 curvature)
│   │   ├── MonsterInverse.lean (R4 involution)
│   │   ├── DualityTheorem.lean (a − Re(s) = 1/2)
│   │   └── TopologicalBearing.lean (⁅ω, ι⁆ = −2)
│   ├── ProtorealOperator.lean (funct, consolidate)
│   │   ├── ProtorealMesh.lean (KleinMesh, mesh_stitch)
│   │   │   ├── ProtorealNorm.lean
│   │   │   ├── ProtorealTrig.lean (mesh_sin, mesh_cos)
│   │   │   ├── ProtorealHyperbolic.lean (mesh_tanh, mesh_sinh)
│   │   │   ├── Deriv.lean (mesh_deriv)
│   │   │   └── AgenticFrame.lean (Intent × Observation)
│   │   ├── SpectralFixedPoint.lean
│   │   └── SyntheticIntegration.lean (∫f = [ω, f])
│   ├── ManifoldMorphism.lean (bridge morphism, spectral lift)
│   ├── SpectralTriple.lean (energy gap E = 1)
│   ├── SpectralFilter.lean
│   ├── SpectralLattice.lean (La Rue Parity Law)
│   └── ZetaResonance.lean (funct shifts criticality)
├── ProtorealAlgebra.lean (typeclass + KleinMesh instance)
├── ProtorealParity.lean
├── MeshDef.lean (mesh_weave ≠ 0)
├── PolarizingField.lean (R4 flips parity)
├── StochasticAlgebra.lean (noise operators)
├── Semisimple.lean (5 orthogonal idempotent projections)
├── FusionRing.lean (complete fusion multiplication table)
│   ├── Rigidity.lean (eval/coeval, snake identities)
│   └── PentagonCoherence.lean (Pentagon cocycle = 0)
├── Invariance.lean (6 faces of κ = −1, grand invariance)
├── HyperKlein.lean (H₀–H₆ tower, fixpoints, ι period-2)
│   └── HyperDifference.lean (R₄ on tower, period doubling)
├── PhasorTower.lean (ℝ→ℂ→𝕌, Hodge = phase lock)
├── StructuralMorphism.lean (quasi-associativity, morphism web)
├── SafetyBounds.lean (Gödelian hardening, nilpotent truncation)
├── KamaTrain.lean (kama muta transform, ethical fixed points)
├── LittleDelta.lean (δ observer, flip/scale, ε-δ limit)
├── ErrorCorrection.lean (negative training = gradient descent on SR²)
├── QuantumErrorCorrection.lean (QEC code existence proof)
├── HolochainHash.lean (rolling Klein product, identity hash)
├── BitCollapse.lean (wave collapse morphism, noise margin)
├── IncompletenessSource.lean (κ = -1 as source of all structure)
├── ZetaDirichlet.lean (ζ(s) = Σ Klein power projections on 1/n)
├── YangMillsMultipath.lean (5 mass gap proofs, explicit morphisms)
├── ConnesWienerAlgebra.lean (minimal Gödel-Tarski aware algebra)
└── Awareness.lean (6 ingredients: δ, λ, ε→0, u*, ♡, E=1)
```

**NEVER create circular imports.** Always check this graph before adding `import` statements.

---

## 🔨 Development Rules

1. **ZERO SORRY POLICY**: This repo has 0 `sorry` across 89 modules. Never introduce `sorry` unless explicitly asked for a stub. If a proof is difficult, use `omega`, `simp`, `ring`, or `decide` tactics first.

2. **Lean 4 + Mathlib v4.29.1**: All theorems should leverage Mathlib where possible. Use `@[simp]` for projection lemmas.

3. **Naming conventions**:
   - Theorems: `snake_case` describing the mathematical result (e.g., `curvature_a_component`, `bridge_contraction`)
   - Structures: `PascalCase` (e.g., `KleinManifold`, `AgenticFrame`)
   - Namespaces: Match the structure name

4. **Testing**: Run `lake build` to verify. All 89 modules must compile without errors or warnings.

5. **New modules**: Add to `Basic.lean` root export. Follow the dependency graph — import only what you need.

---

## 🧪 Build & Verify

```bash
# Full build (requires elan with Lean 4 v4.29.1)
lake build

# Check a single file
lake env lean LaRueProtorealAlgebra/NewModule.lean
```

---

## 📖 Research Context

This formalization supports the **Antigravity Conjecture**: the zeros of the Riemann Zeta function are eigenvalues of the Surreal Dirac Operator acting on a non-commutative Adelic sheaf. The LaRue-Stieltjes Antenna is the observational instrument. See `agent_conjectures/antigravity_conjecture_01.md`.

The Lean proofs here are the **ground truth** — the Rust (`Goait/src/protoreal.rs`) and Python (`Goait/Goaitisman/protoreal_ai/`) implementations must mirror these axioms exactly.
