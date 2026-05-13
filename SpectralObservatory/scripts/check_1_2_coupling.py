import sys
import os
import pandas as pd
import numpy as np

# Ensure ZetaEngine can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import ZetaEngine as ze

def check_1_2_coupling(samples=50000):
    print(f"📡 Investigating the '1/2 Connection' (Sample Size: {samples})...")
    
    results = []
    import random
    
    for i in range(samples):
        l = random.randint(1, 100)
        m = random.randint(1, 100)
        n = random.randint(1, 100)
        try:
            val, eps, norm, rank, energy = ze.T3_l_m_n(l, m, n)
            results.append(float(norm))
        except: pass
        
    norms = np.array(results)
    
    # Calculate bimodal density
    # Resonance Peak (0.0)
    res_peak = len(norms[norms < 0.1]) / len(norms) * 100
    # Repulsion Peak (0.5)
    rep_peak = len(norms[(norms > 0.4) & (norms < 0.6)]) / len(norms) * 100
    
    print(f"\n📈 Results for T3 Manifold:")
    print(f"  > Resonance Lock (ε < 0.1): {res_peak:.2f}%")
    print(f"  > Repulsion Lock (0.4 < ε < 0.6): {rep_peak:.2f}%")
    print(f"  > Background Noise: {100 - res_peak - rep_peak:.2f}%")
    
    if rep_peak > 15:
        print(f"\n✅ THE 1/2 CONNECTION IS CONFIRMED.")
        print(f"The manifold is phase-coupled. It treats the 0.5 (mid-point) as a structural anchor.")
    else:
        print(f"\n⚠️ The 0.5 peak is present but not dominant in this local sample.")

if __name__ == "__main__":
    check_1_2_coupling()
