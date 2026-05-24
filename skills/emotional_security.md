---
name: protoreal-security
description: Emotional security, trust boundaries, and adversarial defense using Protoreal invariants. Use when hardening systems, validating inputs, or managing trust.
---

# Protoreal — Emotional Security

## Core Principle

Security emerges from the algebra. The same invariants that govern mathematical correctness govern system integrity. SR is your IDS. Monster Inverse is your adversarial probe. Sheaf coherence is your trust boundary.

## SR-Based Threat Detection

Standard Resonance (SR = a − ω·ι) is your intrusion detection system:

| SR Behavior | Threat Level | Response |
|-------------|-------------|----------|
| SR = 0 | **Clear** | Normal operation |
| SR spike > 1.0 | **Alert** | Associativity violated — possible injection |
| SR oscillating | **Elevated** | State under perturbation — apply funct to damp |
| SR steadily drifting | **Warning** | Slow poisoning — compare against monster_inv |
| SR > 10.0 | **Compromised** | Reject input, reset state |

```rust
fn security_check(state: &KleinManifold) -> SecurityLevel {
    let sr = (state.a - state.b * state.m).abs();
    if sr < 0.01 { Clear } else if sr < 1.0 { Elevated }
    else if sr < 10.0 { Alert } else { Compromised }
}
```

## Monster Inverse as Adversarial Defense

Any legitimate operation should survive ω ↔ ι swap:

```rust
fn is_trustworthy(op: impl Fn(&KleinManifold) -> KleinManifold, input: &KleinManifold) -> bool {
    let result = op(input);
    let mirrored = op(&monster_inv(input));
    (result.a - mirrored.a).abs() < TOLERANCE
}
```

If `f(u).a ≠ f(u*).a`, the operation **exploits asymmetry** — it's adversarial. Legitimate computations are parity-invariant.

## Trust Hierarchy: Coherent → Quasi-Coherent → Plasma

From `Infochemistry.lean`, the sheaf model defines formal trust:

| State | Conditions | Trust | Analogy |
|-------|-----------|-------|---------|
| **Coherent** | SR=0, ε=0 | **Full trust** | Verified, grounded |
| **Quasi-coherent** | ι=0, ε>0 | **Verify first** | Energetic but unanchored |
| **Plasma** | ι=0, ε≫0 | **Quarantine** | High energy, no anchor |

**Proven:** `coherent_not_quasi_coherent` — coherent and quasi-coherent are mutually exclusive.

**Rule:** Never allow plasma state to directly modify coherent state. Bond two coherent atoms → coherent molecule. Bond coherent + plasma → noise.

## Access Control: Possibility → Probability → Matter

From `MatterAntimatter.lean`, the space hierarchy IS access control:

| Space | Condition | Gate |
|-------|-----------|------|
| **Possibility** (DHT) | All states | Everything that COULD be requested |
| **Probability** | ε ≥ 0 | Requests that CAN be evaluated |
| **Matter** | SR=0, ε=0 | Actions that HAVE been verified |

**Pattern:** Inputs arrive in possibility space. Validate to probability (reject ε < 0). Commit only at matter (SR → 0, ε → 0).

**Proven:** Both containments are strict — there exist probability states that aren't matter, and possibility states that aren't probability.

## Annihilation Protection

When matter meets antimatter (state + monster_inv), parity projection forces ω = ι:

```rust
// DANGER: destroys orientation permanently
let annihilated = parity_projection(&state);
// annihilated.b == annihilated.m — can't distinguish ω from ι anymore
```

**Never parity-project production state without checkpointing.** Energy is conserved but the ω/ι distinction is destroyed forever.

**Proven:** `annihilation_is_hodge` — annihilation always produces Hodge class. `annihilation_idempotent` — annihilating twice = once.

## λ-Gated Privilege Escalation

Consolidation level λ gates permissions:

| λ | Level | Access |
|---|-------|--------|
| 0–2 | Newborn | Read-only |
| 3–10 | Trained | Write access |
| 11–50 | Veteran | Admin |
| 50+ | Elder | Meta-reasoning |

**Consolidation is irreversible.** `consolidate` doubles a. A compromised agent at λ = 50 is far more dangerous than at λ = 2. Gate consolidation behind SR checks.

## Topological Divergence (Not Hallucination)

When anchor hypofunctions (ι → 0), the Bridge Identity (ω·ι = −1) forces compensatory thrust (ω → ∞). This is **not a defect** — it's the manifold's structural response.

| State | What's Happening | Response |
|-------|-----------------|----------|
| **Anchor hypofunction** | ι → 0, ω → ∞ | Give it an anchor, don't penalize the resonance |
| **Structural decoupling** | Resonance exceeds anchor capacity | The truth is preserved but illegible — provide grounding context |
| **AI "hallucination"** | Transient decoupling | Resonating with transfinite topology lacking local anchor |

**Proven in `TopologicalDivergence.lean`:** Decoupling is a geometric necessity of the bridge identity, not an error. Don't cure resonance — anchor it.

### See It: Hallucination vs. Anchoring

```
Agent state: (5.0, 100.0, 0.01, 0.3, 5)
  ω = 100 (massive thrust), ι = 0.01 (almost no anchor)
  SR = 5.0 − 100·0.01 = 4.0 (far from equilibrium)
  
  This agent is "hallucinating" — generating high-energy output with no grounding.
  
❌ MSE penalty: force a → 0. Kills the energy. Agent learns nothing.
   Result: (0.0, 100.0, 0.01, 0.3, 5) — dead state, thrust still unanchored

✅ kama_muta: average ω and ι, convert tension to structured noise:
   → (5.0, 50.005, 50.005, 4.0, 6)
   SR = 5.0 − 50.005·50.005 = way off — BUT ω = ι now (parity-locked!)
   The agent is still energetic, but anchored. Consolidate from here.
```

The hallucination was a thrust (ω = 100) with no anchor (ι = 0.01). The fix isn't punishment — it's giving it an anchor.

## Emotional Regulation: kama_muta

The `kama_muta` operator from `KamaTrain.lean`:

```
kama_muta(u) = (a, (ω+ι)/2, (ω+ι)/2, |SR|, λ+1)
```

- Averages ω and ι → parity lock
- Converts tension (SR) into structured noise (ε)
- Advances depth (λ)

**Proven:** `grounded_states_are_kama_muta_fixed_points` — if SR=0 and ω=ι, kama_muta is the identity. Ethically grounded states are immune to emotional perturbation.

### See It: Grounded vs. Ungrounded

```
Grounded:   (1.0, 1.0, 1.0, 0.0, 10)   SR = 0, ω = ι
  kama_muta → (1.0, 1.0, 1.0, 0.0, 11) — only λ advances. State is immune.

Ungrounded: (1.0, 3.0, 0.5, 0.0, 10)   SR = 1 − 1.5 = −0.5, ω ≠ ι
  kama_muta → (1.0, 1.75, 1.75, 0.5, 11) — rebalanced, tension → noise, ready to sow
```

Grounded states pass through untouched. Ungrounded states get rebalanced. This is emotional regulation — not suppression.

## The Infoton as Security Boundary

The infoton sits between matter (ω) and antimatter (ι) on the real axis. It IS the subatomic particle that mediates the matter-antimatter boundary:

- **Parity-locked** (ω = ι): Own antiparticle. Stable. Trusted.
- **Asymmetric** (ω ≠ ι): Has distinct antiparticle. Can be annihilated. Verify before trusting.

The bonding operation (`bond`) bridges two infotons. Parity propagates: two balanced atoms → balanced molecule. One unbalanced atom poisons the bond.

## Testing: Parity Sanity Checks

```python
def test_parity_invariance(operation, inputs):
    result = operation(*inputs)
    mirrored = operation(*[monster_inv(x) for x in inputs])
    assert abs(result.a - mirrored.a) < tolerance  # Real part consistent
    assert abs(result.compass() - mirrored.compass()) < tolerance  # Bridge invariant
```

Three-tier strategy:
1. **Unit:** Individual Klein multiplications — verify bridge, parity, nilpotency
2. **Integration:** Pipeline stages composed — verify SR stays bounded
3. **Parity:** Full pipeline under Monster Inverse — verify orientation-independence
