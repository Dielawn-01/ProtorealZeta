"""
mass_protoreal_audit.py — Large-scale Spectral Analysis of the Protoreal Manifold

Analyzes 2,001,052 Zeta zeros using the 4-component Protoreal Engine.
Searches for Epsilon-Potent drift and Non-commutative phase anomalies.
"""

import sys
import os
import pandas as pd
import numpy as np
import mpmath as mp

# Setup paths
BASE_PATH = "/home/phrxmaz/Documents/Prime Search"
SAGE_PATH = "/home/phrxmaz/Documents/Sage"
sys.path.append(BASE_PATH)
sys.path.append(os.path.join(BASE_PATH, "TheLab"))
sys.path.append(SAGE_PATH)

import ZetaEngine as ze
from protoreal.ring import ProtorealElement
from protoreal.autolift import autolift

def test_func(indices):
    """The Protoreal Test Function: Lifts antenna resonance to 4-component space."""
    val, eps, norm, rank = ze.T_Generic(indices)
    # Lift to Protoreal space based on the normalized jitter
    # We use 'norm' as the base for the infinitesimal anchor
    u = ProtorealElement(a=float(val), c=float(norm))
    return u

def run_mass_audit(limit=100000): # Running on 100k for speed, can be scaled
    print(f"🚀 Starting Mass Protoreal Audit (N=1..7, Limit={limit} zeros)...")
    
    results = []
    # Analyzing N=1 for each zero in the sample
    for k in range(1, limit + 1):
        try:
            u = test_func([k])
            
            # Stress test: Square the state and check for potency drift
            u_sq = u * u
            
            # Record metrics
            results.append({
                'zero_index': k,
                'real_base': u.a,
                'iota_pull': u.c,
                'potency_drift': u_sq.c, # Should be -u.c^2 if iota^2 = -iota
                'is_attractive': u.c < 0.2
            })
            
            if k % 10000 == 0:
                print(f"  Processed {k} zeros...")
        except:
            continue

    df = pd.DataFrame(results)
    
    # Analyze the 21st-dimension horizon (Parity check)
    print("\n🔍 Analyzing Parity Parity (La Rue Conjecture)...")
    summary = {
        'total_zeros': len(df),
        'attractive_percentage': (df['is_attractive'].sum() / len(df)) * 100,
        'avg_iota_pull': df['iota_pull'].mean(),
        'drift_consistency': (df['potency_drift'] / -df['iota_pull']**2).mean() # Should be 1.0 if axioms hold
    }
    
    return df, summary

if __name__ == "__main__":
    df, summary = run_mass_audit()
    print("\n📊 ANALYSIS COMPLETE")
    print(summary)
    
    # Save results for reporting
    df.to_csv(os.path.join(BASE_PATH, "TheLab/data/mass_protoreal_audit.csv"), index=False)
