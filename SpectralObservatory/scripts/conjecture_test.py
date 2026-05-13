"""
conjecture_test.py — Testing Cardinality-Based Resonance

Conjecture: Zero-species repel or attract based on the cardinality of the 
input sequence (i, j, k, ...).

We evaluate the generalized T-Series antenna for N = 1 to 5:
T_N = (product of primes)^(2/N) * e - (Stieltjes Drift)
"""

import sys
import os
import random
import numpy as np
import mpmath as mp

# Add workspace paths
BASE_PATH = "/home/phrxmaz/Documents/Prime Search"
sys.path.append(BASE_PATH)
sys.path.append(os.path.join(BASE_PATH, "TheLab"))

import ZetaEngine as ze

def T_Generic(indices):
    """
    Generalized Prime Antenna for cardinality N = len(indices).
    Formula: (Product p_i)^(2/N) * e - Stieltjes_Drift
    """
    N = len(indices)
    primes = [mp.mpf(ze.sieve[idx]) for idx in indices]
    
    # 1. Decelerated Base: (prod p_i)^(2/N) * e
    prod_p = mp.fprod(primes)
    base = mp.power(prod_p, mp.mpf(2)/N) * mp.exp(1)
    
    # 2. Simplified Stieltjes Drift for N-dimensions
    # For N=2 and N=3, we have specific drift models.
    # For generic N, we use a log-scaled drift based on the index centroid.
    avg_p = mp.fsum(primes) / N
    avg_idx = mp.fsum([mp.mpf(idx) for idx in indices]) / N
    
    # TermB: Euclidean drift magnitude
    euclidean_inner = mp.fsum([(primes[i] - indices[i])**2 for i in range(N)])
    termB = mp.sqrt(euclidean_inner / (2 * mp.pi))
    
    h = mp.fsum([mp.log(p) for p in primes]) / N
    G0, G1, G2, G3 = mp.euler, mp.mpf('-0.0728158454836767249'), mp.mpf('-0.0096903631928723185'), mp.mpf('0.0020538344203033459')
    stieltjes_poly = G0 + G1 * h + G2 * h**2 / 2 + G3 * h**3 / 6
    
    idx_scaling = mp.log(1 + mp.fsum([mp.mpf(idx)**2 for idx in indices]))
    drain = termB * stieltjes_poly * idx_scaling
    
    val = base - drain
    
    # Find nearest zero and calculate norm_eps
    rank, nearest = ze.get_nearest_zero(val)
    epsilon = abs(float(val - nearest))
    norm_eps = epsilon / ze.get_zero_spacing(val)
    
    return norm_eps

def run_cardinality_test(samples=5000):
    print(f"📡 Testing Cardinality-Based Resonance (Samples: {samples})...")
    
    results = {}
    
    for N in [1, 2, 3, 4, 5, 6]:
        print(f"  Testing Cardinality N={N}...")
        norms = []
        for _ in range(samples):
            indices = [random.randint(10, 500) for _ in range(N)]
            try:
                norm = T_Generic(indices)
                norms.append(norm)
            except: pass
        
        norms = np.array(norms)
        # Attraction Peak (ε < 0.1)
        attr = len(norms[norms < 0.1]) / len(norms) * 100
        # Repulsion Peak (0.4 < ε < 0.6)
        rep = len(norms[(norms > 0.4) & (norms < 0.6)]) / len(norms) * 100
        
        results[N] = {'attr': attr, 'rep': rep}
        print(f"    > Attraction (0.0): {attr:.2f}%")
        print(f"    > Repulsion (0.5):   {rep:.2f}%")

    print("\n📊 FINAL CONJECTURE ANALYSIS:")
    for N, data in results.items():
        state = "ATTRACTIVE" if data['attr'] > data['rep'] else "REPELLENT"
        print(f"  N={N}: {state} (Lock: {data['attr']:.1f}%, Repel: {data['rep']:.1f}%)")

if __name__ == "__main__":
    run_cardinality_test()
