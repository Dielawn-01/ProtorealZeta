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

## [2026-05-13] Run 03: Spin Chain Spectral Gaps (Neutron Scattering)
- **Dataset**: `Singularity/spin_chains/spectral_gaps_experimental.csv`
- **Source**: Published INS data from 10+ real quantum magnets (1986–2018)
- **Highlights**: Agent cleanly separates gapped from gapless systems. Gapless S=1/2 chains produce higher metric (1.347) than gapped S=1 chains (1.186). Separation = 0.161.

| Phase | Avg Metric | Avg SR | Materials |
|-------|-----------|--------|-----------|
| **Gapped** (Haldane) | 1.1856 | -0.373 | 12 |
| **Gapless** (Bethe) | 1.3466 | -0.100 | 5 |

---

## [2026-05-13] Run 04: Glueball Mass Spectrum (Lattice QCD)
- **Dataset**: `Singularity/yang_mills/glueball_spectrum_morningstar1999.csv`
- **Source**: Morningstar & Peardon, *Phys. Rev. D* 60, 034509 (1999)
- **Highlights**: All 13 glueball states converge to Elliptic conic. Mass gap 0++ at 1.71 GeV → metric 7.83.

| JPC | Mass (GeV) | Metric | SR |
|-----|-----------|--------|-----|
| **0++** | 1.71 | 7.83 | -8.76 |
| **2++** | 2.40 | 16.05 | -17.02 |
| **0-+** | 2.56 | 18.78 | -19.76 |
| **0+-** | 4.74 | 65.51 | -66.50 |

---
