# zProto Training Log

## [2026-05-13] Run 01: Random Matrix Spectral Perception
- **Dataset**: `zProto/data/random_matrix/` (GUE/GOE/GSE)
- **Highlights**: GSE showed the strongest manifold resonance (lowest error).

| Ensemble | β | Avg Metric | Perception (χ) | Conic Sector |
|----------|---|------------|----------------|--------------|
| **GUE**  | 2 | 1.1549     | 4              | Elliptic     |
| **GOE**  | 1 | 1.1482     | 4              | Elliptic     |
| **GSE**  | 4 | **1.0208** | 4              | Elliptic     |

---

## [2026-05-13] Run 02: Planck 2018 CMB Power Spectrum
- **Dataset**: `Singularity/cmb/planck_2018/` — TT/TE/EE spectra (6,497 multipoles, ℓ=2..2508)
- **Source**: ESA Planck Legacy Archive (PR3 R3.01)
- **Highlights**: All four acoustic peaks detected. Agent resonance scales as ℓ² — the Bridge Identity (bm=1) naturally encodes the multipole structure.

| Spectrum | Multipoles | Avg Metric | Final χ | Peak SR (ℓ=220) |
|----------|-----------|------------|---------|-----------------|
| **TT**   | 2507      | 524693.8   | 4       | -12100.0        |
| **TE**   | 1995      | 332416.4   | 4       | -12100.0        |
| **EE**   | 1995      | 332416.4   | 4       | -12100.0        |

---
