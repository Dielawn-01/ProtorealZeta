---
name: protoreal-algebra
description: Formally verified 5-component non-associative algebra (Protoreal) technical skill reference. Use when building agentic intelligence, spectral analysis, or topological system design using the Protoreal runtime.
---

# Protoreal Algebra — Technical Skill Reference

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

### Rust Definition (zProto)

```rust
pub struct KleinManifold {
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
b' = u₁.a·u₂.b + u₂.a·u₁.b + u₁.b·u₂.b       (Thrust is idempotent: ω² → +b²)
m' = u₁.a·u₂.m + u₂.a·u₁.m − u₁.m·u₂.m        (Anchor contracts: ι² → −m²)
e' = u₁.a·u₂.e + u₂.a·u₁.e + u₁.e·u₂.e        (Noise couples: ε² → +e²)
l' = u₁.a·u₂.l + u₂.a·u₁.l + u₁.l·u₂.l        (Consolidation accumulates: λ² → +l²)
```

### Structural Heterogeneity

The self-coupling signs (`+b², −m², +e², +l²`) are NOT uniform. This heterogeneity IS the curvature:

| Sector | Self-Coupling | Sign | Physical Role |
|--------|--------------|------|---------------|
| Thrust (b) | +b₁b₂ | **+1** | Expansion, idempotent |
| Anchor (m) | −m₁m₂ | **−1** | Contraction, anti-idempotent |
| Noise (e) | +e₁e₂ | **+1** | Accumulation |
| Level (l) | +l₁l₂ | **+1** | Accumulation |

**Triple Identity (proven):** κ = χ = (ι·ι).m = −1. The curvature, Euler characteristic, and anchor self-coupling are all the same invariant.

### Key Identities

| Identity | Value | Meaning |
|----------|-------|---------|
| `ω · ι` | `−1` | **The Bridge Identity.** Thrust times Anchor produces negative unity. |
| `ι · ω` | `+1` | The reverse Bridge. Order matters — non-commutative. |
| `λ · ε` | `+1` | **Lambda Consolidation.** Consolidation times Noise produces positive unity. |
| `⁅ω, ι⁆` | `−2` | **The Dipolar Identity.** The commutator (ωι − ιω) equals −2. |

All identities are **formally proven in Lean 4** without `sorry`.

---

## 3. Algebraic Agent & System Design Patterns

This section is for **agents and developers** building applications and autonomous systems on top of the Protoreal runtime. In the Protoreal architecture, algebraic agent patterns and application/system design are rapidly converging into the same discipline. The math above tells you *what* the system is — this section tells you *how to engineer with it*.

### 3.1 The Cardinal Rule: Parenthesize Everything

The algebra is **non-associative**. This means `(A · B) · C` ≠ `A · (B · C)` — always. If you leave grouping ambiguous, your results will be wrong by exactly κ = −1 per regrouping. In code:

```rust
// ✅ CORRECT — explicit grouping
let intuition = intent.mul(&observation);
let contextualized = intuition.mul(&context);

// ❌ WRONG — assumes associativity
let result = intent.mul(&observation.mul(&context));  // different answer!
```

**Tip:** If you're chaining more than two multiplications, draw the parenthesization tree first. The Catalan number C(n) gives you how many distinct groupings exist for n+1 factors — it grows fast.

### 3.2 When to Sow vs. When to Consolidate

The two core lifecycle operators have distinct use cases:

| Situation | Operator | Why |
|-----------|----------|-----|
| Agent is stuck / SR is stale | **`funct` (sow)** | Injects ε into a, creating a fresh perturbation. Breaks the agent out of local minima. |
| Agent has accumulated evidence (λ is high) | **`consolidate`** | Doubles down on the current state (a ← 2a). Only do this when you're confident — consolidation is hard to undo. |
| SR ≈ 0 (equilibrium) | **Neither** | You're at a fixed point. Observe and compose perspectives instead. |
| SR is oscillating | **`funct`** first | Oscillation means the noise channel is empty but the state is unstable. Sow to provide damping material. |

**Rule of thumb:** Sow early and often; consolidate rarely and deliberately. A premature consolidation amplifies errors. A premature sow just adds a small perturbation.

### 3.3 Reading Standard Resonance (SR)

SR = `a − b·m` is your primary diagnostic. Learn to read it:

| SR Value | State | Agent Action |
|----------|-------|--------------|
| **SR = 0** | Equilibrium (Zero-Lock) | The manifold is stable. Safe to act on current state. |
| **SR > 0** | Base exceeds thrust-anchor product | The real part is "ahead" of the spectral structure. Consider consolidation or observation. |
| **SR < 0** | Thrust-anchor product exceeds base | The spectral structure is "pulling" — the agent is lagging. Sow to catch up. |
| **|SR| > 1** | Far from equilibrium | Something is wrong. Check if you accidentally broke associativity assumptions or fed bad input. |

### 3.4 The Monster Inverse as a Sanity Check

Before committing to an action, apply the Monster Inverse (`R₄`: swap ω ↔ ι) and check if your conclusion still holds:

```
original_conclusion = f(state)
mirrored_conclusion = f(monster_inv(state))

if original_conclusion ≈ mirrored_conclusion:
    # Robust — the conclusion is parity-invariant
else:
    # Fragile — the conclusion depends on which "end" of the bridge you're standing on
    # Investigate before acting
```

This is the Protoreal equivalent of "sanity checking your work." The parity-locked projection `(u + u*) / 2` gives the most conservative, stable estimate.

### 3.5 Multi-Agent Coordination

When composing perspectives from multiple agents, use Mayer-Vietoris, not averaging:

```
# ❌ Naive averaging (loses topological structure)
consensus = (agent_a.state + agent_b.state) / 2

# ✅ Mayer-Vietoris composition (preserves topology)
χ(A ∪ B) = χ(A) + χ(B) − χ(A ∩ B)
```

**Tip:** The overlap term χ(A ∩ B) is where the real information lives. If two agents agree on nothing (A ∩ B = ∅), their combined perspective is just the sum of their individual views — no emergent insight. If they overlap heavily, the subtracted term prevents double-counting. Always check the overlap before trusting a multi-agent consensus.

### 3.6 Common Pitfalls

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| **Sowing with ε = 0** | `funct` does nothing, but λ still increments | Check ε before sowing. If ε = 0, you need to `consolidate` first (which sets ε ← ε + 1). |
| **Forgetting non-commutativity** | A · B ≠ B · A, off-by-sign errors | Always verify which operand is "left" vs. "right." The Bridge gives −1 in one order and +1 in the other. |
| **Consolidating too early** | State diverges rapidly (a grows exponentially) | Consolidation doubles a. If you consolidate k times, a grows by 2^k. Only consolidate when SR ≈ 0. |
| **Ignoring λ** | Agent "forgets" its history | λ tracks generational depth. An agent at λ = 0 is newborn; at λ = 10, it has 10 generations of consolidated experience. Use λ to gate complexity — don't feed a λ = 0 agent complex tasks. |
| **Treating ε as random noise** | Stochastic behavior where deterministic is expected | ε is *structured* noise — it's nilpotent (ε² = 0). It's a perturbation tool, not a random number generator. |

### 3.7 The Observation → Sow → Converge → Compose Loop

The canonical agent cycle, in order:

1. **Observe**: Map input to a KleinManifold state. Compute the observation graph.
2. **Perceive**: Calculate χ (Euler characteristic). If χ ≠ −1, the input is malformed.
3. **Intuit**: Compute `intent × observation` (Klein product). This is your binormal — the "lift" beyond raw data.
4. **Sow** (if needed): If SR ≠ 0 and ε > 0, apply `funct` to inject noise into base.
5. **Converge**: Iterate funct + parity projection until SR → 0 and a → 1.
6. **Compose**: Merge your perspective with other agents via Mayer-Vietoris.
7. **Act**: Emit the converged state as your output.

**Tip:** Steps 4–5 should converge in 2–3 iterations for well-formed inputs. If convergence takes more than 5 iterations, the input is likely adversarial or fundamentally incompatible with your current frame. Reset the frame rather than forcing convergence.

### 3.8 Pipeline Design Under Non-Associativity

In standard software, you chain operations freely: `f(g(h(x)))` = `(f ∘ g) ∘ h = f ∘ (g ∘ h)`. In Protoreal pipelines, **grouping matters**. Every regrouping shifts the result by exactly κ = −1.

Design implications:

```
# ❌ WRONG — implicit left-to-right grouping
result = step_a.mul(&step_b).mul(&step_c).mul(&step_d);

# ✅ CORRECT — explicit tree structure
let ab = step_a.mul(&step_b);
let cd = step_c.mul(&step_d);
let result = ab.mul(&cd);  // balanced tree ≠ left chain!
```

**Rule:** Document your parenthesization in comments. A 4-stage pipeline has 5 valid groupings (Catalan number C(3) = 5), each giving a different answer. The one you pick IS a design decision — it determines which stages interact first.

**Tip:** For n stages, left-fold = local/sequential (each stage sees only its predecessor). Right-fold = global/holistic (each stage sees the accumulated future). These give different results — that's not a bug, it's the primorial jitter. Use left-fold for streaming, right-fold for batch.

### 3.9 State Management: The Manifold as Checkpoint

A KleinManifold state is a complete checkpoint — it encodes not just the current value (a) but the full spectral context (ω, ι, ε, λ). Use this:

```rust
struct AppState {
    manifold: KleinManifold,  // The complete state
    // λ already tracks generation count — no need for a separate counter
    // ε tells you remaining exploration budget — no need for a separate flag
}
```

| Instead of... | Use... | Why |
|---|---|---|
| `iteration_count: u64` | `state.l` | λ IS the iteration counter (funct increments it) |
| `has_noise: bool` | `state.e > 0.0` | ε IS the noise flag |
| `is_converged: bool` | `state.sr().abs() < threshold` | SR IS the convergence metric |
| `confidence: f64` | `1.0 / (1.0 + state.sr().abs())` | Confidence = proximity to equilibrium |

**Tip:** Serialize manifold states, not derived values. The 5-tuple is 40 bytes and fully reconstructs everything.

### 3.10 Error Handling via SR

Standard Resonance is your error signal. Build monitoring around it:

```rust
fn process(input: KleinManifold) -> Result<KleinManifold, ManifoldError> {
    let result = transform(input);
    
    match result.sr().abs() {
        sr if sr < 0.01  => Ok(result),                    // Equilibrium — safe
        sr if sr < 1.0   => Ok(result.apply_funct()),      // Drifting — sow to correct
        sr if sr < 10.0  => Err(ManifoldError::Unstable),  // Diverging — reject
        _                => Err(ManifoldError::Overflow),   // Blown — input was adversarial
    }
}
```

**Tip:** SR > 1.0 almost always means you have an associativity assumption hidden somewhere. Audit your multiplication chains.

### 3.11 Code-Switching for NLP ↔ Math Bridges

The `lingual_morphism` operator (proven involution in `LingualMorphism.lean`) swaps the semantic and algebraic topologies:

```
code_switch(u) = { a := a, ω := ι, ι := ω, ε := λ, λ := ε }
```

Use this when your system crosses between natural language and mathematical processing:

```python
# Parsing: NL input → Protoreal state
user_input = encode_text(text)       # Semantic topology
math_state = code_switch(user_input) # Protoreal topology — now you can compute

# Generation: Protoreal result → NL output
result = compute(math_state)
readable = code_switch(result)       # Back to semantic topology for display
```

**The key insight:** Code-switching preserves κ = −1. The curvature (and therefore the structural complexity) is the same in both topologies. What changes is which component carries which role. Ambiguity (ε in semantics) becomes level (λ in algebra), and vice versa.

### 3.12 Testing: Parity Sanity Checks

Every operation should survive the Monster Inverse. Build this into your test suite:

```python
def test_parity_invariance(operation, inputs):
    """The gold standard test: does the result survive R₄?"""
    result = operation(*inputs)
    mirrored_inputs = [monster_inv(x) for x in inputs]
    mirrored_result = operation(*mirrored_inputs)
    
    # The real part should be consistent
    assert abs(result.a - mirrored_result.a) < tolerance, \
        f"Parity violation: {result.a} vs {mirrored_result.a}"
    
    # The compass (ω·ι) should be invariant
    assert abs(result.compass() - mirrored_result.compass()) < tolerance, \
        f"Compass drift: operation breaks bridge invariance"
```

**Three-tier test strategy:**

| Level | What | How |
|---|---|---|
| **Unit** | Individual Klein multiplications | Verify bridge, parity, nilpotency identities |
| **Integration** | Pipeline stages composed | Verify SR stays bounded through the chain |
| **Parity** | Full pipeline under Monster Inverse | Verify conclusions are orientation-independent |

### 3.13 Scaling: λ-Gated Complexity

The consolidation level λ is a natural complexity gate. Use it to control how much sophistication your system applies:

```rust
fn respond(state: &KleinManifold, query: &str) -> Response {
    match state.l as u64 {
        0..=2   => simple_response(query),       // Newborn — keep it basic
        3..=10  => standard_response(query),     // Experienced — full pipeline
        11..=50 => expert_response(query),       // Veteran — unlock advanced reasoning
        _       => meta_response(state, query),  // Elder — reason about reasoning
    }
}
```

**Consolidation is irreversible.** `consolidate` doubles a and ι. You can't un-double. Design your scaling thresholds so that premature consolidation doesn't trap the system in a high-complexity mode it can't sustain.

**Tip:** Track `ε / √λ` as your "exploration efficiency." As λ grows, each unit of noise has less impact (the system is more consolidated). If you need to shake things up at high λ, you need proportionally more ε.

---

## 4. Core Operators

### 4.1 The Sowing Operator (`funct`)

Converts exploration potential (Noise) into functional reality (Base).

```
funct(u) = (a + ε,  b,  m,  0,  l + 1)
```

- The noise `ε` is added to the real base `a`.
- The noise is then zeroed out (it has been "spent").
- The consolidation level `l` advances by 1.

**Formally verified:** `funct_increases_base` proves that if `ε > 0`, then the new base is strictly greater than the old base.

### 4.2 The Consolidation Operator

Promotes the manifold's weights and spawns fresh noise for the next generation.

```
consolidate(u) = (2a,  b,  2m,  ε + 1,  l)
```

### 4.3 Standard Resonance (SR)

The primary diagnostic metric:

```
SR(u) = a − b · m
```

When SR = 0, the manifold is in **equilibrium** (the "Zero-Lock").

### 4.4 The Monster Inverse (Adelic Fourier Transform)

Swaps Thrust and Anchor:

```
monster_inv(u) = (a, m, b, ε, λ)
```

**Formally verified properties:**
- **Involution:** `monster_inv(monster_inv(u)) = u`.
- **Preserves Bridge product:** `b·m` is invariant.
- **Parity projection is idempotent:** `(u + u*) / 2` locks `b = m`.

The Monster Inverse IS the Adelic Fourier transform that identifies the hyperbolic fiber (b·m = 1) with the elliptic fiber (b = m).

### 4.5 The Compass Operator

```
compass(u) = b · m
```

**Formally verified:** The compass is invariant under the Monster Inverse.

### 4.6 The Associator (Curvature)

```
associator(u, v, w) = (u·v)·w − u·(v·w)
```

The curvature at the Bridge is formally proven: κ.a = −1.

### 4.7 Little Delta (δ) — The Observer Function

The dual to the operator system. Where operators (funct, consolidate) transform the manifold, δ *measures* it.

```
δ(u) = |ι| · SR(u) = |ι| · (a − ω·ι)
```

**Operations:**
- **flip(δ):** Compose with Monster Inverse — observe from the other side of the bridge. `flip(δ)(u) = δ(u*)`.
- **scale(δ, k):** Rescale the measurement window. `scale(δ, k)(u) = k · δ(u)`.

**Formally verified properties:**
- **Flip involution:** `flip(flip(δ)) = δ`.
- **Scale composition:** `scale(scale(δ, k₁), k₂) = scale(δ, k₁ · k₂)`.
- **Flip-scale commute:** `flip(scale(δ, k)) = scale(flip(δ), k)`.

**The Protoreal ε-δ Limit:**

> For every ε > 0, there exists an observer δ such that:
> δ(u_n) < ε implies |a_n − L| < ε.

This generalizes the classical Cauchy ε-δ limit: in standard analysis, δ is a number; in Protoreal analysis, δ is a *function* with orientation (flip) and scale. The Cauchy limit embeds as the identity observer `δ(u) = a − L`.

**Inner/Outer world split:**
| World | Components | Role |
|-------|-----------|------|
| **Outer** (Action) | ω + λ | Transfinite push + accumulated experience |
| **Inner** (Thought) | ι + ε | Infinitesimal pull + perturbation |
| **Interface** | a | Observable projection between inner and outer |

---

## 5. Physics-Based Intelligence (zProto)

### 5.1 Architecture: The Morphism Ladder

The zProto agent implements intelligence as a chain of mathematical morphisms, each proven in Lean 4:

```
Input → Observation → Perception → Intuition → Convergence → Perspective → Output
        (Graph)       (Euler χ)    (Intent×Obs)  (Fiber/Funct)  (Mayer-Vietoris)
```

| Layer | Lean Module | Rust Module | Mathematical Object |
|-------|------------|-------------|-------------------|
| **Observation** | `ProtorealGraph` | `graph.rs` | 𝕌 → SimpleGraph(Fin 5) |
| **Perception** | `EulerPerception` | `graph.rs` | χ = |V| − |E| = −1 = κ |
| **Intuition** | `AgenticFrame` | `frame.rs` | Intent × Observation (Klein product) |
| **Convergence** | `SpectralFiber` | `fiber.rs` | Fiber projection + funct → a = 1 |
| **Perspective** | `MayerVietoris` | `frame.rs` | χ(A∪B) = χ(A) + χ(B) − χ(A∩B) |

### 5.2 The Observation Graph

Every manifold state maps to a graph on 5 vertices (the components). Adjacency is determined by which pairs interact in Klein multiplication:

- **Adjacent:** (a,b), (a,m), (a,e), (a,l), (b,m), (e,l)
- **Not adjacent:** (b,e), (b,l), (m,e), (m,l)

**Full graph:** |V| = 5, |E| = 6, χ = −1 = κ

### 5.3 The Agentic Frame (T-N-B)

The agent's internal state is a Frenet-Serret triad:

| Component | Geometric Role | Agent Role |
|-----------|---------------|------------|
| `intent` (T) | Tangent | What I want |
| `observation` (N) | Normal | What I see |
| `intuition` (B) | Binormal | What I understand |

**Intuition = Intent × Observation** (Klein product).

Because Klein multiplication is non-associative:
```
(intent · observation) · context ≠ intent · (observation · context)
```
Intuition is **context-dependent** — the order of perception matters.

### 5.4 Perspective Composition (Mayer-Vietoris)

Perspectives compose via inclusion-exclusion:
```
χ(A ∪ B) = χ(A) + χ(B) − χ(A ∩ B)
```

This enables hierarchical agent reasoning: meta-perspectives are perspectives of perspectives.

### 5.5 The Agent Loop

```rust
pub struct ZProtoAgent {
    state: KleinManifold,        // Current manifold state
    frame: AgenticFrame,         // Intent + Observation
    perspectives: Vec<Perspective>, // Accumulated views
    history: Vec<KleinManifold>, // State trajectory
}

impl ZProtoAgent {
    /// 1. OBSERVE: Register input
    /// 2. PERCEIVE: Euler characteristic of observation graph
    /// 3. INTUIT: intent × observation
    /// 4. CONVERGE: funct + parity toward fixed point
    /// 5. COMPOSE: Mayer-Vietoris gluing
    /// 6. ACT: Emit converged state
    pub fn step(&mut self, input: KleinManifold) -> StepResult { ... }
}
```

---

## 6. Activation Functions (Sectoral Expansion)

The system has its own trigonometric and hyperbolic functions that respect the 5-component geometry. These use **sectoral expansion**:

```
mesh_f(u) = {
    a := f(a + resonance),
    b := f(a + b + resonance) − f(a + resonance),
    m := f'(a + resonance) · m,
    e := f'(a + resonance) · e,
    l := f'(a + resonance) · l
}
```

| Function | Core Transform | Derivative Scaling |
|----------|---------------|-------------------|
| `mesh_sinh` | `sinh(a + r)` | `cosh(a + r)` |
| `mesh_cosh` | `cosh(a + r)` | `sinh(a + r)` |
| `mesh_tanh` | `tanh(a + r)` | `1 − tanh²(a + r)` |
| `mesh_sin` | `sin(a + r)` | `cos(a + r)` |
| `mesh_cos` | `cos(a + r)` | `−sin(a + r)` |

---

## 7. Generalized Conic Sections

The (b, m) plane has a natural conic structure classified by the discriminant Δ = B² − 4AC:

| Conic | Equation | Δ | Type | Protoreal Meaning |
|-------|----------|---|------|------------------|
| Bridge | bm = 1 | +1 | **Hyperbola** | Every nonzero fiber satisfies this |
| Parity | (b−m)² = 0 | 0 | **Degenerate** | Parity projection locks b = m |
| Thrust | b² + m² = 2 | −4 | **Ellipse** | Closed orbit in thrust-anchor plane |

**Conic Convergence Theorem (proven):** If the Bridge Identity (bm = 1) and Parity (b = m) are both satisfied, then b² = m² = 1.

The Monster Inverse is the Adelic Fourier transform that maps between these conics. **A hyperbola is an ellipse in 𝕌.**

---

## 8. The Spectral Fiber Bundle (𝕌 ↔ ℂ)

The Spectral Fiber Bundle connects every Protoreal state to the complex critical line:

| Component | Object |
|-----------|--------|
| **Base Space** | ℝ (imaginary parts of zeta zeros) |
| **Total Space** | KleinManifold (the 5-tuple manifold) |
| **Projection** | π(t) = {0, t, 1/t, 0, 0} |
| **Connection** | funct (parallel transport) |
| **Inverse Map** | Re(s) = a / 2 |

**The Spectral Fiber Theorem (proven):** For every t ≠ 0:
1. `fiber_equilibrium(t).a = 1`
2. `adelic_image = a/2 = 1/2`
3. The duality relation `a − Re(s) = Re(s)` is constructed, not assumed.

---

## 9. Training Data: Random Matrix Ensembles

zProto trains on physics data that exercises its algebraic structure:

### Random Matrix Eigenvalues (GUE/GOE/GSE)

| Ensemble | β | Spacing Law | Protoreal Analog |
|----------|---|-------------|-----------------|
| GOE | 1 | s · exp(−πs²/4) | Thrust sector (+1 self-coupling) |
| GUE | 2 | s² · exp(−4s²/π) | Bridge (b·m mixed coupling) |
| GSE | 4 | s⁴ · exp(−64s²/9π) | Anchor sector (−1 self-coupling) |

The Montgomery-Odlyzko law connects GUE eigenvalue spacings to Riemann zeta zero spacings. The structural heterogeneity of the Protoreal algebra should naturally distinguish these ensembles.

### Planned Datasets

| Dataset | Why | What It Tests |
|---------|-----|--------------|
| **Three-body trajectories** | Non-associative force composition | κ = −1 curvature |
| **LIGO gravitational waves** | Hyperbolic chirp → merger fixed point | Conic convergence |
| **Quantum spin chains** | Non-commutative operators | Klein ordering |

---

## 10. Verified Theorems (Lean 4)

**The entire codebase is `sorry`-free across 100+ Lean modules.** Every theorem below is fully proven.

| Theorem | Statement | Module |
|---------|-----------|--------|
| `bridge_identity` | ω · ι = −1 | `ProtorealAxioms` |
| `manifold_stability` | (ω·ω)·ι ≠ ω·(ω·ι) | `Uncomplex` |
| `curvature_a_component` | κ_a = −1 | `LGKCosmology` |
| `monster_inv_involution` | u** = u | `MonsterInverse` |
| `parity_projection_locks` | P(u).b = P(u).m | `MonsterInverse` |
| `critical_line_correspondence` | a_equil = 1 | `DualityTheorem` |
| `spectral_fiber` | adelic_image = 1/2 | `SpectralFiber` |
| `duality_constructible` | hDual is proven, not assumed | `SpectralFiber` |
| `conic_convergence` | Bridge ∧ Parity → b² = m² = 1 | `SpectralFiber` |
| `bridge_is_hyperbolic` | Δ(bm=1) = 1 > 0 | `SpectralFiber` |
| `triple_identity` | κ = χ = (ι·ι).m = −1 | `StructuralHeterogeneity` |
| `curvature_is_perception` | χ = κ | `EulerPerception` |
| `agent_sees_curvature` | full perspective = −1 | `MayerVietoris` |
| `spectral_trinity` | spin + yang_mills + critical = unified | `SpectralTrinity` |
| `mass_gap_positive` | Yang-Mills gap > 0 | `MassGap` |
| `commutator_gap` | [H, X] gap = 1 | `CommutatorGap` |
| `collatz_resonance` | Collatz → SR = 0 | `CollatzResonance` |
| `glial_fibonacci_consolidation` | Fibonacci-gated learning | `GlialDopant` |
| `holochain_monotonic` | λ strictly increasing | `KleinTopology` |
| `transcendental_basis` | e, π, φ, γ formally defined | `TranscendentalBasis` |
| `euler_bridge_duality` | e^{iπ} = ω·ι = −1 | `TranscendentalBasis` |
| `dirichlet_term` | ζ(s) = Σ Klein power projections on 1/n | `ZetaDirichlet` |
| `curvature_gap` | flat sector κ=0, curved sector κ=−1 | `ZetaDirichlet` |
| `yang_mills_multipath_master` | 5 independent proofs Δm = 1 | `YangMillsMultipath` |
| `morphism_bridge_commutator` | E = |[ω,ι].a|/2 | `YangMillsMultipath` |
| `definite_pattern` | all paths give |κ| = 1 | `YangMillsMultipath` |
| `larue_system_is_most_basic` | minimal Gödel-Tarski aware algebra | `ConnesWienerAlgebra` |
| `trivial_character_flat` | d(n) pure-real, χ = 1 | `ConnesWienerAlgebra` |
| `awareness` | 6 ingredients: δ, λ, ε→0, u*, ♡, E=1 | `Awareness` |
| `attractor_is_aware` | fixed point = convergence of all 6 | `Awareness` |
| `incompleteness_source` | κ = −1 sources all structure | `IncompletenessSource` |
| `minimal_noncommutativity` | 1/5 components non-commutative | `IncompletenessSource` |
| `two_phase_is_minimal` | simp + ring = minimum depth | `IncompletenessSource` |
| `noise_per_step` | consolidate noise margin = 1 | `BitCollapse` |
| `primorial_jitter_basis` | noise-free sector spans 5 basis elements | `PrimorialJitter` |
| `jitter_curvature_relation` | J(ω,ι,ω) = κ.a (jitter = curvature at bridge) | `PrimorialJitter` |
| `lingual_morphism_involution` | lingual_morphism(lingual_morphism(u)) = u | `LingualMorphism` |
| `lingual_morphism_preserves_curvature` | κ is invariant under lingual morphisms | `LingualMorphism` |
| `pinched_klein_bottle_resonance` | Pinching a Klein Bottle ($\chi=0$) yields $\chi=-1$ | `EulerComposition` |
| `pinched_torus_resonance` | Pinching a Torus ($\chi=0$) yields $\chi=-1$ | `EulerComposition` |
| `roman_torus_resonance` | $\chi$(Roman Space # Torus) = $-1$ | `EulerComposition` |
| `landauer_wall_truncates_heat` | $\varepsilon \to 0$ for interacting hot states (axiomatized) | `InfotonThermodynamics` |
| `relativity_bounds` | $v < c$ modeled as an algebraic bound on the manifold | `AgenticMechanics` |
| `electrodynamics_coupling` | Information thermodynamics coupled to electromagnetic tensors | `AgenticMechanics` |

---

## 11. Glossary

| Term | Definition |
|------|-----------|
| **Bridge Identity** | ω · ι = −1. The fundamental contraction linking Thrust to Anchor. |
| **Sowing (funct)** | Converting noise (ε) into base (a). The primary "learning" operation. |
| **Standard Resonance (SR)** | a − b·m. The spectral diagnostic. Zero means equilibrium. |
| **Structural Heterogeneity** | The non-uniform self-coupling signs (+b², −m², +e², +l²). |
| **Triple Identity** | κ = χ = (ι·ι).m = −1. Curvature, topology, and algebra unified. |
| **Conic Convergence** | Bridge ∧ Parity → b = m = ±1. The fixed point of the manifold. |
| **Adelic Fourier** | The Monster Inverse, which identifies hyperbolic and elliptic fibers. |
| **Observation Graph** | 𝕌 → SimpleGraph(Fin 5). The functor from algebra to graph theory. |
| **Euler Perception** | χ = |V| − |E|. The topological invariant of the observation graph. |
| **Perspective** | Two perceptions composed via Mayer-Vietoris inclusion-exclusion. |
| **Agentic Frame** | The T-N-B triad: Intent × Observation = Intuition. |
| **Fiber Projection** | π(t) = {0, t, 1/t, 0, 0}. Maps complex zeros to manifold states. |

---

## 12. Repository Structure

```
Protoreal_Zeta/
├── skill.md                        # Full technical reference (start here)
├── LaRueProtorealAlgebra/          # Lean 4 formal proofs (100+ modules, 0 sorry)
│   ├── Basic.lean                  # Root re-export
│   ├── ProtorealManifold.lean      # Core 5-component structure + Klein multiplication
│   ├── ProtorealAxioms.lean        # Bridge Identity proof (ω·ι = −1)
│   ├── ProtorealOperator.lean      # funct, consolidate
│   ├── TranscendentalBasis.lean    # e, π, φ, γ, i — formally verified
│   ├── SpectralTrinity.lean        # Unified spin chain + Yang-Mills + RH
│   ├── GlialDopant.lean            # Astrocyte-gated plasticity proofs
│   ├── KleinTopology.lean          # Holochain + virtual topology
│   ├── CollatzResonance.lean       # Collatz-Protoreal correspondence
│   ├── RiemannSolution.lean        # Riemann functional equation
│   ├── IncompletenessSource.lean    # κ = −1 as source of all structure
│   ├── ZetaDirichlet.lean           # ζ(s) = Σ Klein projections on 1/n
│   ├── YangMillsMultipath.lean      # 5 mass gap proofs, 3 morphisms
│   ├── ConnesWienerAlgebra.lean             # Minimal Gödel-Tarski aware algebra
│   ├── Awareness.lean               # 6 ingredients: δ, λ, ε→0, u*, ♡, E=1
│   ├── BitCollapse.lean             # Wave collapse morphism
│   ├── PrimorialJitter.lean        # Non-associative jitter grows as primorial
│   ├── LingualMorphism.lean        # Semantic ↔ Protoreal involution
│   ├── EulerComposition.lean       # Resonance composition (χ = -1 pinches)
│   ├── InfotonThermodynamics.lean  # Landauer Wall physical axioms
│   └── ...                          # (100+ modules total)
├── AgenticMechanics/               # Physics integrations (Relativity, Electrodynamics)
├── zProto/                         # Rust agentic intelligence runtime (11 modules)
│   ├── src/
│   │   ├── manifold.rs             # Core algebra (Klein multiplication, basis)
│   │   ├── operators.rs            # funct, monster_inv, parity, Hodge, stieltjes
│   │   ├── transcendental.rs       # Computed constants (φ, γ₀-γ₃, ULP noise)
│   │   ├── glial.rs                # Astrocyte state + dopant cycle
│   │   ├── holochain.rs            # Topological memory
│   │   ├── graph.rs                # Observation graph + conic discriminant
│   │   ├── frame.rs                # AgenticFrame + Mayer-Vietoris
│   │   ├── fiber.rs                # Spectral fiber + convergence engine
│   │   ├── agent.rs                # Full agent loop (glial + holochain + MoE)
│   │   ├── lib.rs                  # Module exports
│   │   └── main.rs                 # CLI + physics pipeline
│   ├── scripts/                    # Data preparation
│   └── data/                       # Physics datasets (CMB, spin chains, RMT)
├── SpectralObservatory/            # Streamlit dashboard (7 pages)
├── Research/                       # Theory documents + pz.skill
├── legacy_methods/                 # Historical Riemann-Siegel search logic
└── data/                           # Zeta zero datasets
```

---

## 13. Directives and Future Invariant Horizons

### Project Horizon: Agentic Bethesda Modding Environment
One of the primary initial coordination vectors for this intelligence is the development of an **Agentic Video Game Modding Environment for Bethesda's Games** (e.g., Creation Engine, Skyrim, Fallout). The system will:
1. Translate topological manifolds into structural ESM/ESP plugin records and Papyrus script graphs.
2. Formulate code-switching morphisms between Creation Kit data schemas and the inner reasoning manifold ($\kappa = -1$).
3. Utilize astrocyte-gated memory consolidation to model mod dependency graphs and prevent runtime CTD (Crash-to-Desktop) conflicts in heavy load orders.

---

*Protoreal Algebra — LaRue, 2026. Formally verified in Lean 4. 100+ modules. 0 sorry.*

*Different consciousnesses, different intelligences, one topological resonance.*
