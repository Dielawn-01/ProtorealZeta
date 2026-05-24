---
name: protoreal-agentic
description: Agentic architecture and cybernetic design patterns for the Protoreal runtime. Use when building agent loops, pipelines, or autonomous systems.
---

# Protoreal — Agentic & Cybernetic Skill

## The Agent Loop

```
Observe → Perceive (χ = −1?) → Intuit (intent × observation) → Sow → Converge (SR → 0) → Compose → Act
```

| Step | Math | Rust Module |
|------|------|-------------|
| **Observe** | 𝕌 → SimpleGraph(Fin 5) | `graph.rs` |
| **Perceive** | χ = |V| − |E| = −1 | `graph.rs` |
| **Intuit** | intent × observation (Klein product) | `frame.rs` |
| **Converge** | funct + parity → SR → 0 | `fiber.rs` |
| **Compose** | χ(A∪B) = χ(A) + χ(B) − χ(A∩B) | `frame.rs` |

**Convergence:** Should take 2–3 iterations. If > 5, input is adversarial — reset frame.

## The Agentic Frame (T-N-B)

| Component | Role | Agent Meaning |
|-----------|------|---------------|
| `intent` (T) | Tangent | What I want |
| `observation` (N) | Normal | What I see |
| `intuition` (B) | Binormal | What I understand |

**Intuition = Intent × Observation** (Klein product). Context-dependent because non-associative:
`(intent · observation) · context ≠ intent · (observation · context)`

## SR as Diagnostic

| SR | State | Action |
|----|-------|--------|
| `= 0` | Equilibrium | Safe to act |
| `> 0` | Base ahead | Observe more |
| `< 0` | Spectrum pulling | Sow to catch up |
| `> 1.0` | Unstable | Audit for injection |

## When to Sow vs. Consolidate

| Situation | Operator | Why |
|-----------|----------|-----|
| Agent stuck, SR stale | `funct` | Inject ε into a — break local minima |
| High confidence, SR ≈ 0 | `consolidate` | Double down (a ← 2a). Hard to undo. |
| SR ≈ 0, stable | Neither | You're at a fixed point. Compose. |
| SR oscillating | `funct` first | Noise channel empty but unstable. Damp it. |

**Rule:** Sow early and often. Consolidate rarely and deliberately.

## State = Checkpoint

The 5-tuple IS your complete state. No separate counters needed:

| Instead of... | Use... |
|---|---|
| `iteration_count` | `state.l` (λ IS the counter) |
| `has_noise: bool` | `state.e > 0` |
| `is_converged: bool` | `SR.abs() < threshold` |
| `confidence: f64` | `1.0 / (1.0 + SR.abs())` |

40 bytes. Serialize the manifold, not derived values.

## Pipeline Design

Non-associativity means **grouping matters**:

```rust
// ❌ Left-fold (implicit)
let result = a.mul(&b).mul(&c).mul(&d);

// ✅ Balanced tree (explicit)
let ab = a.mul(&b);
let cd = c.mul(&d);
let result = ab.mul(&cd);  // Different answer!
```

Left-fold = sequential/streaming. Right-fold = holistic/batch. The difference IS the primorial jitter. Document your parenthesization.

## Multi-Agent Composition

Use Mayer-Vietoris, not averaging:

```
χ(A ∪ B) = χ(A) + χ(B) − χ(A ∩ B)
```

The overlap χ(A ∩ B) is where emergent insight lives. Zero overlap = no emergence.

## Code-Switching (NLP ↔ Math)

```
code_switch(u) = { a := a, ω := ι, ι := ω, ε := λ, λ := ε }
```

Preserves κ = −1. Ambiguity (ε) in semantics becomes depth (λ) in algebra. Parse → code_switch → compute → code_switch → emit.

## λ-Gated Complexity

| λ Range | Level | Capability |
|---------|-------|-----------|
| 0–2 | Newborn | Basic responses |
| 3–10 | Trained | Full pipeline |
| 11–50 | Veteran | Advanced reasoning |
| 50+ | Elder | Meta-reasoning |

**Consolidation is irreversible.** Track `ε / √λ` as exploration efficiency.

## Monster Inverse Sanity Check

Before committing to any action:

```python
if f(state).a ≈ f(monster_inv(state)).a:
    # Robust — parity-invariant conclusion
else:
    # Fragile — investigate before acting
```

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| Sowing with ε = 0 | funct does nothing. Consolidate first to spawn noise. |
| Forgetting non-commutativity | A·B ≠ B·A. Bridge = −1 one way, +1 the other. |
| Consolidating too early | Doubles a exponentially. Only when SR ≈ 0. |
| Ignoring λ | Don't feed complex tasks to λ = 0 agents. |
| Implicit associativity | Every regrouping shifts by κ = −1. Parenthesize. |
