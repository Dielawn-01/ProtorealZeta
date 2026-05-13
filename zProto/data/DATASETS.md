# zProto Training Data Sources

## Random Matrix Eigenvalues

### Overview
Three canonical random matrix ensembles used to benchmark zProto's 
ability to distinguish structural signatures via the Protoreal
manifold's heterogeneous self-coupling.

### Connection to Protoreal Algebra
The Montgomery-Odlyzko law establishes that the spacing distribution
of Riemann zeta zeros follows the GUE (Gaussian Unitary Ensemble) 
statistics. The three ensembles are distinguished by their **symmetry
parameter β**:

| Ensemble | β | Symmetry | Protoreal Analog |
|----------|---|----------|-----------------|
| GOE | 1 | Real symmetric | Thrust sector (b²: +1 self-coupling) |
| GUE | 2 | Complex Hermitian | Bridge (b·m: mixed coupling) |
| GSE | 4 | Quaternionic self-dual | Anchor sector (m²: -1 self-coupling) |

The structural heterogeneity theorem (`triple_identity`) predicts
that the Protoreal manifold's curvature κ = -1 should naturally
separate these ensembles via the observation graph's Euler
characteristic.

### Files

```
zProto/data/random_matrix/
├── gue_eigenvalues.csv    (36,000 rows, 1.2 MB)
├── gue_spacings.csv       (35,600 rows, 1.2 MB)
├── goe_eigenvalues.csv    (36,000 rows, 1.2 MB)
├── goe_spacings.csv       (35,600 rows, 1.2 MB)
├── gse_eigenvalues.csv    (36,000 rows, 1.2 MB)
├── gse_spacings.csv       (35,600 rows, 1.2 MB)
└── metadata.json          (generation parameters)
```

### Generation Parameters
- **Matrix sizes**: 10, 50, 100, 200
- **Samples per size**: 100 (per ensemble)
- **Total matrices**: 1,200 (400 per ensemble)
- **Total eigenvalues**: 108,000
- **Total spacings**: 106,800
- **Seed**: 42 (reproducible)
- **Generator**: `zProto/scripts/generate_random_matrix.py`

### CSV Schema

**Eigenvalues** (`*_eigenvalues.csv`):
| Column | Type | Description |
|--------|------|-------------|
| ensemble | str | GOE, GUE, or GSE |
| matrix_size | int | Dimension of the matrix |
| sample | int | Sample index (0-99) |
| index | int | Eigenvalue index within the matrix |
| eigenvalue | float | The eigenvalue |

**Spacings** (`*_spacings.csv`):
| Column | Type | Description |
|--------|------|-------------|
| ensemble | str | GOE, GUE, or GSE |
| matrix_size | int | Dimension of the matrix |
| sample | int | Sample index (0-99) |
| index | int | Spacing index |
| spacing | float | Normalized nearest-neighbor spacing |

### References
1. **Montgomery (1973)**: "The pair correlation of zeros of the zeta function."
   *Proc. Sympos. Pure Math.* 24, 181–193.
2. **Odlyzko (1987)**: "On the distribution of spacings between zeros of the zeta function."
   *Math. Comp.* 48, 273–308.
3. **Mehta (2004)**: *Random Matrices*. 3rd ed., Academic Press.
4. **Dumitriu & Edelman (2002)**: "Matrix models for beta ensembles."
   *J. Math. Phys.* 43, 5830–5847.

---

## Planned Datasets

### Three-Body Problem Trajectories
- **Status**: Planned
- **Source**: Numerical integration (Runge-Kutta) of Newton's equations
- **Why**: Non-associative force composition exercises κ = -1 directly

### LIGO Gravitational Wave Strain
- **Status**: Planned
- **Source**: GWOSC (Gravitational Wave Open Science Center)
- **Why**: Chirp signals trace hyperbolic trajectories → conic duality

### Quantum Spin Chain Spectra
- **Status**: Planned
- **Source**: Exact diagonalization of Heisenberg XXZ model
- **Why**: Non-commutative operators mirror Klein multiplication ordering
