#!/usr/bin/env python3
"""
Generate zeta_divergence_analysis.csv for the Resonance Analysis page.

Uses actual zeta zeros + primes to compute the LaRue antenna divergence:
  D_{m,n} = Base - Modulator - Drain

Produces ~10K rows from the first 100 prime pairs.
"""
import os
import math
import csv

# ── Sieve of Eratosthenes ──
def sieve(n):
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for p in range(2, int(n**0.5) + 1):
        if is_prime[p]:
            for i in range(p*p, n+1, p):
                is_prime[i] = False
    return [i for i in range(2, n+1) if is_prime[i]]

# ── Stieltjes constants (computed, not hardcoded) ──
def _sow_gamma_0(n=200):
    h = sum(1.0/k for k in range(1, n+1))
    nf, n2 = float(n), float(n)**2
    return (h - math.log(nf) - 1/(2*nf) + 1/(12*n2) - 1/(120*n2**2)
            + 1/(252*n2**3) - 1/(240*n2**4))

GAMMA = _sow_gamma_0()
PHI = (1 + math.sqrt(5)) / 2

# ── Load zeta zeros ──
ZEROS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          '..', '..', 'data', 'zeta_zeros_100k_sample.txt')
zeros = []
with open(ZEROS_PATH) as f:
    for line in f:
        line = line.strip()
        if line:
            zeros.append(float(line))
print(f"Loaded {len(zeros)} zeta zeros")

# ── Generate prime list ──
primes = sieve(1000)  # First 168 primes
N_PRIMES = 100  # Use first 100
primes = primes[:N_PRIMES]
print(f"Using {len(primes)} primes up to {primes[-1]}")

# ── Antenna computation ──
def nearest_zero(val, zeros_list):
    """Find nearest zeta zero to val."""
    import bisect
    idx = bisect.bisect_left(zeros_list, val)
    candidates = []
    if idx > 0:
        candidates.append(zeros_list[idx-1])
    if idx < len(zeros_list):
        candidates.append(zeros_list[idx])
    if not candidates:
        return 0.0, 0
    best = min(candidates, key=lambda z: abs(z - val))
    best_k = zeros_list.index(best) + 1
    return best, best_k

def compute_row(m_idx, n_idx, primes, zeros):
    """Compute one (m,n) divergence row."""
    m = m_idx + 1  # 1-indexed
    n = n_idx + 1
    p_m = primes[m_idx]
    p_n = primes[n_idx]

    # Mangoldt Base: p_m * e * p_n
    base = p_m * math.e * p_n

    # Modulator: sqrt(m*n) * e^((p_n - p_m)/2) / (4*pi)
    modulator = math.sqrt(m * n) * math.exp((p_n - p_m) / 2) / (4 * math.pi)

    # Mangoldt divergence
    delta_lambda = abs(math.log(p_n / p_m)) if p_m != p_n else 0.0

    # Stieltjes phase polynomial P(Δλ) = γ₀ + γ₁·Δλ (simplified)
    stieltjes_poly = GAMMA + (-0.0728) * delta_lambda

    # Index drift
    drift_sq = (p_n - n)**2 + (p_m - m)**2
    drift = math.sqrt(drift_sq / (2 * math.pi))

    # Drain
    drain = drift * stieltjes_poly * math.log(1 + abs(n**2 - m**2)) if m != n else 0.0

    # LaRue divergence
    larue = base - modulator - drain

    # Divergence (normalized to spectral energy)
    div = larue / (base + 1e-15)

    # Nearest zero
    nz, k = nearest_zero(p_m * p_n / (4 * math.pi), zeros)
    resonance = abs(div) - abs(nz - p_m * p_n / (4 * math.pi)) if nz else 0.0

    # Lambda ratio
    lambda_pm = math.log(p_m) if p_m > 1 else 0
    lambda_pn = math.log(p_n) if p_n > 1 else 0
    lambda_pmn = math.log(p_m * p_n) if p_m * p_n > 1 else 0
    lambda_ratio = lambda_pm / lambda_pn if lambda_pn != 0 else 1.0

    normalized_div = div / (1 + abs(div))

    return {
        'm': m, 'n': n, 'p_m': p_m, 'p_n': p_n,
        'k': k, 'Div': round(div, 8),
        'LaRue': round(larue, 4),
        'Base': round(base, 4),
        'Modulator': round(modulator, 4),
        'Drain': round(drain, 4),
        'Λ Ratio': round(lambda_ratio, 6),
        'Nearest Zero': round(nz, 6) if nz else 0,
        'Resonance': round(resonance, 6),
        'λ_P(k)': round(lambda_pm, 6),
        'λ_P(m*n)': round(lambda_pmn, 6),
        'Normalized_Div': round(normalized_div, 8),
    }

# ── Generate all (m, n) pairs ──
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
os.makedirs(OUT_DIR, exist_ok=True)
OUT_PATH = os.path.join(OUT_DIR, 'zeta_divergence_analysis.csv')

rows = []
for mi in range(len(primes)):
    for ni in range(mi, len(primes)):  # Upper triangle only
        rows.append(compute_row(mi, ni, primes, zeros))
    if (mi + 1) % 20 == 0:
        print(f"  Processed m={mi+1}/{len(primes)}")

# Write CSV
fieldnames = list(rows[0].keys())
with open(OUT_PATH, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"\n✅ Generated {len(rows)} rows → {OUT_PATH}")
print(f"   Columns: {', '.join(fieldnames)}")
