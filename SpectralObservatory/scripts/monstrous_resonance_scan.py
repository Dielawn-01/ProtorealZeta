"""
monstrous_resonance_scan.py — 24-Dimensional Spectral Analysis

Performs the 'Monstrous Resonance' scan for cardinalities N = 1 to 24.
Investigates the Stability Collapse and the emergence of Permanent Repulsion 
in high-dimensional modular manifolds.
"""

import sys
import os
import random
import numpy as np
import mpmath as mp
import pandas as pd

# Add workspace paths
BASE_PATH = "/home/phrxmaz/Documents/Prime Search"
sys.path.append(BASE_PATH)
sys.path.append(os.path.join(BASE_PATH, "TheLab"))

import ZetaEngine as ze

# Ultra-high precision for Monstrous scale
mp.mp.dps = 150 

def T_Generic(indices):
    """Generalized Prime Antenna for cardinality N."""
    N = len(indices)
    primes = [mp.mpf(ze.sieve[idx]) for idx in indices]
    
    # 1. Decelerated Base: (Product p_i)^(2/N) * e
    prod_p = mp.fprod(primes)
    base = mp.power(prod_p, mp.mpf(2)/N) * mp.exp(1)
    
    # 2. Universal Stieltjes Drift
    # Magnitude of index-prime divergence in N-space
    euclidean_inner = mp.fsum([(primes[i] - indices[i])**2 for i in range(N)])
    termB = mp.sqrt(euclidean_inner / (2 * mp.pi))
    
    h = mp.fsum([mp.log(p) for p in primes]) / N
    G0, G1, G2, G3 = mp.euler, mp.mpf('-0.0728158454836767249'), mp.mpf('-0.0096903631928723185'), mp.mpf('0.0020538344203033459')
    stieltjes_poly = G0 + G1 * h + G2 * h**2 / 2 + G3 * h**3 / 6
    
    idx_scaling = mp.log(1 + mp.fsum([mp.mpf(idx)**2 for idx in indices]))
    drain = termB * stieltjes_poly * idx_scaling
    
    val = base - drain
    
    # Check nearest zero in the 2M database
    rank, nearest = ze.get_nearest_zero(val)
    epsilon = abs(float(val - nearest))
    norm_eps = epsilon / ze.get_zero_spacing(val)
    
    return norm_eps

def run_monstrous_scan(samples_per_n=10000):
    print(f"👹 INITIATING MONSTROUS RESONANCE SCAN (N=1..24 | Total Samples: {samples_per_n * 24})")
    print(f"Leech Lattice Horizon | Cardinality max = 24")
    print("-" * 75)
    
    master_results = []
    
    for N in range(1, 25):
        print(f"📡 Scanning Dimension N={N}...")
        norms = []
        # Sample through the prime manifold
        for i in range(samples_per_n):
            # Biased sampling to stay within the 2M zero horizon
            indices = [int(10 + 110 * (random.random()**0.5)) for _ in range(N)]
            try:
                norm = T_Generic(indices)
                norms.append(norm)
            except: pass
            
        norms = np.array(norms)
        attr = (norms < 0.1).mean() * 100
        rep = ((norms > 0.4) & (norms < 0.6)).mean() * 100
        delta = attr - rep
        
        state = "ATTRACTIVE" if delta > 0 else "REPELLENT"
        
        master_results.append({
            'N': N,
            'State': state,
            'Lock %': attr,
            'Repel %': rep,
            'Stability': delta
        })
        
        print(f"  ✅ Result: {state} (Δ: {delta:+.4f})")

    df = pd.DataFrame(master_results)
    print("\n" + "🔥"*20)
    print("💎 MONSTROUS RESONANCE REPORT")
    print("🔥"*20)
    print(df.to_string(index=False))
    
    # Save to data directory
    output_path = os.path.join(BASE_PATH, "TheLab/data/monstrous_resonance_scan.csv")
    df.to_csv(output_path, index=False)
    print(f"\n✅ Monstrous Data archived to {output_path}")

if __name__ == "__main__":
    run_monstrous_scan()
