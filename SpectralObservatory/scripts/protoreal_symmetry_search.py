import sys
import os
import pandas as pd
import numpy as np
from sympy import symbols, log, simplify

# Ensure ZetaEngine and ProtorealEngine can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import ZetaEngine as ze
from core.ProtorealEngine import ProtorealState

def search_structural_similarity(n_zeros=20000):
    # Initialize Engine
    ze.load_heavy_assets()
    
    print(f"🔬 Searching for Structural Symmetry: Protoreal Ring vs. LRS Manifold")
    print(f"📊 Analyzing horizon: {n_zeros} zeros.")
    
    # Search for known zeros asset
    data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'zeta_zeros_2m.txt')
    if not os.path.exists(data_path):
        data_path = "/home/phrxmaz/Documents/Prime Search/zeta_zeros_2m.txt"
    
    if not os.path.exists(data_path):
        print(f"❌ Dataset not found at {data_path}.")
        return
    
    df = pd.read_csv(data_path, nrows=n_zeros, names=['height'])
    
    # We will sample some T3 coordinates and map them to Protoreal states
    # Axiom: Omega represents the prime-growth (divergence)
    # Axiom: Iota represents the zero-density (convergence)
    
    similarities = []
    
    for l, m, n in [(2, 3, 5), (7, 11, 13), (17, 19, 23), (47, 53, 59), (101, 103, 107)]:
        try:
            val, eps, norm, rank = ze.T3_l_m_n(l, m, n)
            
            # Theoretical Protoreal Mapping:
            # b = log(prime_product) -> The transfinite thrust
            # c = 1/log(height) -> The infinitesimal anchor
            
            p_prod = ze.primes[l] * ze.primes[m] * ze.primes[n]
            b_val = np.log(p_prod)
            c_val = 1.0 / np.log(val/ (2 * np.pi))
            
            # The "Structural Tension"
            # In Protoreal Algebra: u = a + b*omega + c*iota
            # The product b*c*(w*i) = -b*c
            # If b*c ≈ 1, then the transfinite and infinitesimal are in perfect equilibrium (-1 bridge).
            
            tension = b_val * c_val
            
            similarities.append({
                'species': (l, m, n),
                'norm_eps': norm,
                'omega_thrust (b)': b_val,
                'iota_anchor (c)': c_val,
                'tension (b*c)': tension
            })
        except: pass
        
    sim_df = pd.DataFrame(similarities)
    print("\n--- 🪐 Protoreal-LRS Structural Mapping ---")
    print(sim_df.to_string(index=False))
    
    avg_tension = sim_df['tension (b*c)'].mean()
    print(f"\n📊 Average Structural Tension (b*c): {avg_tension:.6f}")
    
    if abs(avg_tension - 1.0) < 0.2:
        print("\n✅ SYMMETRY DETECTED: The LRS manifold operates near the Protoreal Equilibrium (b*c ≈ 1).")
        print("The prime growth (omega) is naturally balanced by the logarithmic zero density (iota).")
    else:
        print("\n⚠️ Tension Divergence: The system is currently in a transfinite-dominant state.")

if __name__ == "__main__":
    search_structural_similarity()
