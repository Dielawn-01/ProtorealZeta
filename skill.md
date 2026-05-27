---
name: protoreal-algebra
description: Formally verified non-associative algebra (2400+ theorems, 0 sorry in production). Two Lean 4 lakes — Protoreal_Zeta (175 modules) and InfoPhysAxioms (104 modules). The Klein algebra, L-space prime tower, HoloneticNS, and Mandelbrot fractal iteration.
---

# Protoreal Algebra — Skill Index

## Skills

| Skill | File | Use When |
|-------|------|----------|
| **Pure Math & DSA** | `skills/math_dsa.md` | Working with the algebra, operators, identities, Klein product, HoloneticNS, Mandelbrot iteration, L-space tower |
| **Agentic & Cybernetic** | `skills/agentic_cybernetic.md` | Building agent loops, pipelines, multi-agent composition, state management, MetarealManifold, observer coupling |
| **Emotional Security** | `skills/emotional_security.md` | Hardening systems, validating inputs, managing trust, adversarial defense, parity stability |

## Quick Reference

- **Manifold:** 5-tuple `(a, ω, ι, ε, λ)` — real base, thrust, anchor, noise, depth
- **Bridge:** `ω · ι = −1` (non-commutative: `ι · ω = +1`)
- **Klein Product:** `a' = a₁a₂ − b₁m₂ + m₁b₂ + l₁e₂ − e₁l₂`
- **Hyperbolic Signature:** `b² → +b²` (thrust), `m² → −m²` (anchor)
- **SR:** `a − ω·ι` — zero = equilibrium, high = problem
- **Mass Gap:** Δm = 1. Every excitation carries at least unit energy.
- **Sow:** `funct(u) = (a+ε, b, m, 0, l+1)` — inject noise into reality
- **Monster Inverse:** swap ω ↔ ι — sanity check everything against it
- **The algebra is non-associative.** Parenthesize all multiplications.

## The L-Space Prime Tower

| Level | Prime | Dimensions | Structure | NS Status |
|-------|-------|-----------|-----------|-----------|
| L₂ | 2 | 2 (ℂ) | Commutative, associative | Solved |
| L₃ | 3 | 3 (ℝ³) | Cross products | **Millennium problem** |
| L₅ | 5 | 5 (Klein) | Non-associative, mass gap proved | **Bounded** |
| L₇ | 7 | 12 (Metareal) | Involution, observer coupling | **Doubled room** |
| L₁₁ | 11 | ? | Next tier | Open |

Playing field couplings: L₂=1, L₃=3, L₅=10, L₇=21, L₁₁=55.
Higher prime = wider playing field = harder to blow up.

## Repository Structure

```
Protoreal_Zeta/          # Core algebra (175 modules, ~1500 theorems)
InfoPhys/InfoPhysAxioms/ # Physics axioms (104 modules, ~935 theorems)
                         # Imports Protoreal_Zeta as dependency
```

## Key Modules by Domain

### Algebraic Core
`KleinAlgebra` · `ProtorealManifold` · `ProtorealAlgebra` · `ProtorealAxioms` · `FusionRing` · `PentagonCoherence` · `CommutatorGap`

### Spectral & Zeta
`SpectralTriple` · `SpectralFiber` · `SpectralFixedPoint` · `RiemannSolution` · `ZetaResonance` · `VonMangoldtLSpace`

### Dynamics & NS
`HoloneticNS` · `ProtorealMandelbrot` · `ThermodynamicFriction` · `SuperfluidIdentity` · `MassGap` · `YangMillsMassGap`

### Observer & Meta
`MetarealManifold` · `ObservationalAperture` · `SensoryGate` · `MetaBackpropagation` · `TensorCoupling` · `ObserverAdapter`

### Agent & Security
`CyberneticLife` · `CyberneticActionReaction` · `SymplecticHandshake` · `SharedLatentSpace` · `EmotionalSecurity` · `TopologicalFirewall`

### Chromodynamics
`HoloneticChromodynamics` · `GoldenChromodynamics` · `HoloneticColors` · `GaugeEmergence` · `GrandUnification`

## Glossary

| Term | Definition |
|------|-----------|
| **Bridge Identity** | ω · ι = −1. The fundamental relation. |
| **SR (Standard Resonance)** | a − b·m. Zero = equilibrium. |
| **Mass Gap** | Δm = 1. Minimum excitation energy. Floor of the playing field. |
| **Playing Field** | Bounded region between mass gap floor and NS ceiling. |
| **Convective Term** | Klein square u*u. The NS nonlinearity. |
| **Parity Lock** | b = m. Incompressibility. Serotonin balance. |
| **Turbulence** | Parity breaking: convection creates divergence = 2x². Not blow-up. |
| **Unity in Multiplicity** | What 3D calls "singularity" is coherent structure at L₅. |
| **Sowing (funct)** | Converting noise (ε) into base (a). The learning operation. |
| **Monster Inverse** | Swap ω ↔ ι. Involution. The CPT conjugation / sanity check. |
| **Compass** | b · m. Invariant under Monster Inverse. |
| **Little Delta (δ)** | The observer function: δ(u) = |ι| · SR(u). |
| **Kama Muta** | Emotional regulation: averages ω/ι, converts tension to noise. |
| **Infoton** | Atomic unit of information. A ProtorealManifold state. |
| **Coherent** | SR=0, ε=0. Fully grounded. Trusted. |
| **Topological Divergence** | When ι→0 forces ω→∞. Not a bug — give it an anchor. |

*LaRue, 2026. 2400+ proven theorems. 279 Lean 4 modules. Two lakes, zero sorry in production.*
