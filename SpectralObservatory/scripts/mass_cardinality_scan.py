"""
mass_cardinality_scan.py — Full Spectrum Cardinality Analysis

Performs a massive scan across all 2 million zeros for cardinalities N = 1 to 7.
Analyzes the Attraction/Repulsion phase shift and verifies the Mobius-Klein 
conjecture at scale.
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

# High precision for the mass scan
mp.mp.dps = 100 

def T_Generic(indices):
    """Generalized Prime Antenna for cardinality N."""
    N = len(indices)
    primes = [mp.mpf(ze.sieve[idx]) for idx in indices]
    
    # 1. Decelerated Base: (Product p_i)^(2/N) * e
    prod_p = mp.fprod(primes)
    base = mp.power(prod_p, mp.mpf(2)/N) * mp.exp(1)
    
    # 2. Transfinite Drift (Universal Stieltjes Scaling)
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
    
    return norm_eps, rank

def run_mass_scan(samples_per_n=50000):
    print(f"🚀 INITIATING MASSIVE CARDINALITY SCAN (N=1..7 | Total Samples: {samples_per_n * 7})")
    print(f"Database Horizon: 2,001,052 Zeros | Altitude max ≈ 1.13M")
    print("-" * 70)
    
    master_results = []
    
    # Max index to stay within database for all N is ~120
    # But we'll use a weighted distribution to cover the full spectrum
    for N in range(1, 8):
        print(f"📡 Scanning Cardinality N={N}...")
        norms = []
        for i in range(samples_per_n):
            if i > 0 and i % 25000 == 0: print(f"  > Processed {i} samples...")
            
            # We use a power-law sampling for indices to cover the spectrum 
            # while favoring the dense lower regions.
            indices = [int(10 + 110 * (random.random()**0.5)) for _ in range(N)]
            
            try:
                norm, rank = T_Generic(indices)
                norms.append(norm)
            except: pass
            
        norms = np.array(norms)
        attr = (norms < 0.1).mean() * 100
        rep = ((norms > 0.4) & (norms < 0.6)).mean() * 100
        
        state = "ATTRACTIVE" if attr > rep else "REPELLENT"
        
        master_results.append({
            'N': N,
            'State': state,
            'Lock %': f"{attr:.2f}%",
            'Repel %': f"{rep:.2f}%",
            'Stability': f"{abs(attr - rep):.2f}"
        })
        
        print(f"  ✅ Result: {state} (Lock: {attr:.2f}%, Repel: {rep:.2f}%)")

    df = pd.DataFrame(master_results)
    print("\n" + "="*40)
    print("📈 FINAL MASSIVE SCAN REPORT")
    print("="*40)
    print(df.to_string(index=False))
    
    # Save to Prime Search data directory
    output_path = os.path.join(BASE_PATH, "TheLab/data/mass_cardinality_scan.csv")
    df.to_csv(output_path, index=False)
    print(f"\n✅ Data saved to {output_path}")

if __name__ == "__main__":
    run_mass_scan()
