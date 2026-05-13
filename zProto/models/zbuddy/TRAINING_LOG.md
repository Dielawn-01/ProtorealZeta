# zBuddy Model Training Log

## Model: zbuddy-gen
- **Base**: qwen2.5-coder:14b (9GB, Q4_K_M quantization)
- **System Prompt**: Protoreal Algebra grounding (see Modelfile)
- **Deployment**: Ollama (v0.23.3), GPU inference on RTX 5090

---

## Klein Text Encoder (v2)

### Architecture
| Parameter | Value |
|-----------|-------|
| Type | TransformerEncoder |
| Parameters | 4,509,701 |
| Embedding dim | 128 |
| Heads | 4 |
| Layers | 2 |
| Max sequence length | 512 |
| Vocab size | 32,000 (byte-level) |
| Output | 5-tuple (a, ω, ι, ε, λ) |

### Training Run — v1 (Fixed Targets)
- **Date**: 2026-05-13
- **Corpus**: 991 pairs (183 equilibrium, 215 low, 263 moderate, 330 noise)
- **Targets**: 4 fixed manifold states
- **Device**: CPU (RTX 5090 SM 120 not yet in PyTorch)
- **Epochs**: 50
- **Best val loss**: 0.0058
- **Issue**: Binary classifier — all non-verified text collapsed to metric ~16.0

### Training Run — v2 (Dynamic Targets) ✓ CURRENT
- **Date**: 2026-05-13
- **Corpus**: 991 pairs (same sources)
- **Targets**: Dynamic — computed via `mesh_tanh → resonance correction → funct`
- **Device**: CPU
- **Epochs**: 50
- **Best val loss**: 0.0011 (5x improvement over v1)
- **Discrimination gradient**:

| Input Type | Metric |
|-----------|--------|
| Rust test (best) | 1.149 |
| Lean theorem | 1.175 |
| Research doc | 1.182 |
| Wrong math | 1.221 |
| Generic text | 1.223 |
| Python code | 1.234 |
| Nonsense (worst) | 1.244 |

### Corpus Sources
| Source | Pairs | Tier |
|--------|-------|------|
| LaRueProtorealAlgebra/*.lean | 228 | equilibrium/low |
| zProto/src/*.rs | 98 | equilibrium/low |
| Goait (timesfm, Goaitisman) | 233 | moderate |
| Research docs | ~40 | low |
| skill.md, GEMINI.md, README.md | ~40 | low |
| Singularity (GEMINI.md, COMMS.md) | 22 | moderate |
| Synthetic noise | 220 | noise |
| Shuffled text | 110 | noise |

---

## Discriminator: zProto Agent (Python port)
- **Source**: Mirrors `zProto/src/{manifold,operators,graph,fiber,agent}.rs`
- **Axiom tests**: All pass (Bridge ω·ι = -1, κ = -1, χ = -1)
- **Thresholds (calibrated)**:
  - `metric_threshold = 8.0`
  - `resonance_threshold = 10.0`
  - `max_retries = 3`

---

## GAN Architecture
```
User Question
  → Generator (qwen2.5-coder:14b via Ollama)
  → Klein Text Encoder (text → KleinManifold)
  → zProto Discriminator (morphism ladder → scores)
  → Accept (metric < 8.0, |SR| < 10.0) or Reject + Retry
```

## Deployment
- **Location**: Local deployment (CodeBuddy workspace)
- **CLI**: `zbuddy` (symlinked to ~/.local/bin/)
- **Desktop**: Klein bottle icon launcher
- **Backend**: FastAPI on :8503
- **UI**: Streamlit on :8502
