#!/usr/bin/env python3
"""
Generate Random Matrix Eigenvalue Datasets for zProto Training.

Generates eigenvalues from three canonical random matrix ensembles:
- GUE (Gaussian Unitary Ensemble): complex Hermitian matrices
- GOE (Gaussian Orthogonal Ensemble): real symmetric matrices
- GSE (Gaussian Symplectic Ensemble): quaternionic self-dual matrices

The Montgomery-Odlyzko law connects GUE eigenvalue statistics
to Riemann zeta zero spacings. The structural heterogeneity of
the Protoreal algebra (+1 thrust, -1 anchor) should naturally
encode the orthogonal/unitary/symplectic distinction.

Output Format (CSV):
    ensemble,matrix_size,eigenvalue_index,eigenvalue,
    normalized_spacing,unfolded_eigenvalue
"""

import numpy as np
import os
import json
from datetime import datetime

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(OUTPUT_DIR, "..", "data", "random_matrix")
os.makedirs(DATA_DIR, exist_ok=True)

# ════════════════════════════════════════════════════
# ENSEMBLE GENERATORS
# ════════════════════════════════════════════════════

def generate_gue(n: int) -> np.ndarray:
    """Gaussian Unitary Ensemble (β=2).
    
    H = (A + A†) / (2√n), where A has i.i.d. complex Gaussian entries.
    Eigenvalues follow the Wigner semicircle law.
    """
    A = (np.random.randn(n, n) + 1j * np.random.randn(n, n)) / np.sqrt(2)
    H = (A + A.conj().T) / (2 * np.sqrt(n))
    return np.linalg.eigvalsh(H)


def generate_goe(n: int) -> np.ndarray:
    """Gaussian Orthogonal Ensemble (β=1).
    
    H = (A + Aᵀ) / (2√n), where A has i.i.d. real Gaussian entries.
    """
    A = np.random.randn(n, n)
    H = (A + A.T) / (2 * np.sqrt(n))
    return np.linalg.eigvalsh(H)


def generate_gse(n: int) -> np.ndarray:
    """Gaussian Symplectic Ensemble (β=4).
    
    Simulated via the tridiagonal β-ensemble with β=4.
    Uses the Dumitriu-Edelman tridiagonal model.
    """
    # Tridiagonal β-ensemble (Dumitriu-Edelman)
    beta = 4
    diag = np.random.randn(n) * np.sqrt(2)
    off_diag = np.array([
        np.random.chisquare(beta * (n - i - 1)) ** 0.5
        for i in range(n - 1)
    ])
    # Build tridiagonal matrix
    H = np.diag(diag) + np.diag(off_diag, 1) + np.diag(off_diag, -1)
    H /= (2 * np.sqrt(n))
    return np.linalg.eigvalsh(H)


def unfold_eigenvalues(eigs: np.ndarray) -> np.ndarray:
    """Unfold eigenvalues to unit mean spacing.
    
    Uses the empirical CDF to map eigenvalues to a
    uniform distribution, then scales to unit spacing.
    """
    n = len(eigs)
    sorted_eigs = np.sort(eigs)
    # Empirical CDF unfolding
    unfolded = np.arange(1, n + 1) / n * n
    return unfolded


def normalized_spacings(eigs: np.ndarray) -> np.ndarray:
    """Compute normalized nearest-neighbor spacings.
    
    s_i = (λ_{i+1} - λ_i) / <s>
    
    The spacing distribution distinguishes ensembles:
    - GOE: P(s) ~ s·exp(-πs²/4) (Wigner surmise, β=1)
    - GUE: P(s) ~ s²·exp(-4s²/π) (β=2)
    - GSE: P(s) ~ s⁴·exp(-64s²/9π) (β=4)
    """
    sorted_eigs = np.sort(eigs)
    spacings = np.diff(sorted_eigs)
    mean_spacing = np.mean(spacings)
    if mean_spacing > 0:
        return spacings / mean_spacing
    return spacings


# ════════════════════════════════════════════════════
# DATASET GENERATION
# ════════════════════════════════════════════════════

def generate_dataset(
    ensemble_name: str,
    generator,
    matrix_sizes: list,
    samples_per_size: int,
    seed: int = 42,
):
    """Generate a full dataset for one ensemble."""
    np.random.seed(seed)
    
    all_eigenvalues = []
    all_spacings = []
    metadata = {
        "ensemble": ensemble_name,
        "matrix_sizes": matrix_sizes,
        "samples_per_size": samples_per_size,
        "seed": seed,
        "generated_at": datetime.now().isoformat(),
        "total_matrices": len(matrix_sizes) * samples_per_size,
    }
    
    for n in matrix_sizes:
        for sample_idx in range(samples_per_size):
            eigs = generator(n)
            eigs_sorted = np.sort(eigs)
            spacings = normalized_spacings(eigs)
            
            for i, eig in enumerate(eigs_sorted):
                all_eigenvalues.append({
                    "ensemble": ensemble_name,
                    "matrix_size": n,
                    "sample": sample_idx,
                    "index": i,
                    "eigenvalue": float(eig),
                })
            
            for i, s in enumerate(spacings):
                all_spacings.append({
                    "ensemble": ensemble_name,
                    "matrix_size": n,
                    "sample": sample_idx,
                    "index": i,
                    "spacing": float(s),
                })
    
    return all_eigenvalues, all_spacings, metadata


def save_csv(data: list, filename: str, keys: list):
    """Save a list of dicts as CSV."""
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'w') as f:
        f.write(','.join(keys) + '\n')
        for row in data:
            f.write(','.join(str(row[k]) for k in keys) + '\n')
    print(f"  Saved {len(data)} rows → {filepath}")
    return filepath


# ════════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════════

if __name__ == "__main__":
    print("═" * 60)
    print("  zProto Random Matrix Eigenvalue Generator")
    print("═" * 60)
    
    # Configuration
    MATRIX_SIZES = [10, 50, 100, 200]
    SAMPLES_PER_SIZE = 100
    
    ensembles = [
        ("GUE", generate_gue),
        ("GOE", generate_goe),
        ("GSE", generate_gse),
    ]
    
    all_metadata = {}
    
    for name, gen in ensembles:
        print(f"\n▸ Generating {name} ensemble...")
        eigs, spacings, meta = generate_dataset(
            name, gen, MATRIX_SIZES, SAMPLES_PER_SIZE
        )
        
        eig_file = save_csv(
            eigs,
            f"{name.lower()}_eigenvalues.csv",
            ["ensemble", "matrix_size", "sample", "index", "eigenvalue"],
        )
        
        spacing_file = save_csv(
            spacings,
            f"{name.lower()}_spacings.csv",
            ["ensemble", "matrix_size", "sample", "index", "spacing"],
        )
        
        meta["eigenvalue_file"] = os.path.basename(eig_file)
        meta["spacing_file"] = os.path.basename(spacing_file)
        meta["total_eigenvalues"] = len(eigs)
        meta["total_spacings"] = len(spacings)
        all_metadata[name] = meta
    
    # Save combined metadata
    meta_path = os.path.join(DATA_DIR, "metadata.json")
    with open(meta_path, 'w') as f:
        json.dump(all_metadata, f, indent=2)
    print(f"\n  Metadata → {meta_path}")
    
    print("\n═" * 60)
    print("  Generation complete!")
    print(f"  Output directory: {DATA_DIR}")
    print("═" * 60)
