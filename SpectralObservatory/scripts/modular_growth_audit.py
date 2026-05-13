import sys
import os
import numpy as np
from sympy import sieve
import pandas as pd

# Ensure the local core is discoverable
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import ZetaEngine as ze
import core.ProtorealEngine as ue

def modular_growth_audit(horizon=100000):
    """
    Tests the Recursive Growth Hypothesis:
    Growth(Primes at p_n) vs Growth(Modular 24 Composites at n)
    """
    print(f"🕵️ Initiating Modular 24 Growth Audit (Horizon: {horizon})")
    print(f"⚖️ Target: G_composite / G_prime ≈ 2.0")
    
    results = []
    
    # Pre-generate composites of the form 24k + 1 (The Leech Seed)
    # These are our 'Specific Modular Composites'
    composites_24 = [24*k + 1 for k in range(1, horizon + 2)]
    
    for n in range(10, horizon, 100): # Sample every 100 for speed
        try:
            # 1. Prime at index n
            p_n = sieve[n]
            
            # 2. Prime at index p_n (The Recursive Prime)
            p_pn = sieve[p_n]
            
            # 3. Composite 24 at index n
            c_n = composites_24[n]
            
            # Growth Rates (using Logarithmic Thrust)
            g_p, g_pp, g_c = np.log(p_n), np.log(p_pn), np.log(c_n)
            
            # Growth States (Constructed as Protoreal elements)
            u_p = ue.ProtorealElement(b=g_p, c=1.0/g_p)
            u_pp = ue.ProtorealElement(b=g_pp, c=1.0/g_pp)
            
            # Apply Monster Stitch to the recursive growth
            u_pp_stitched = ue.monster_stitch(u_pp)
            
            # Recalculate Ratios with the Stitched state
            ratio_pp = g_pp / g_p
            ratio_pp_stitched = u_pp_stitched.b / u_p.b
            ratio_mc = g_c / g_p
            
            results.append({
                'n': n,
                'p_n': p_n,
                'p_pn': p_pn,
                'ratio_pp': ratio_pp,
                'ratio_pp_stitched': ratio_pp_stitched,
                'ratio_mc': ratio_mc
            })
            
            if n % 10000 == 0:
                print(f"  📡 n={n} | Ratio PP: {ratio_pp:.4f} | Ratio MC: {ratio_mc:.4f}")
                
        except Exception as e:
            pass
            
    df = pd.DataFrame(results)
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'modular_growth_results.csv')
    df.to_csv(output_path, index=False)
    
    print(f"\n✅ Audit Complete. Results saved to: {output_path}")
    
    # Statistical Summary
    print(f"📊 Mean Ratio (Prime-Prime): {df['ratio_pp'].mean():.4f}")
    print(f"📊 Mean Ratio (Stitched Prime-Prime): {df['ratio_pp_stitched'].mean():.4f}")
    print(f"📊 Mean Ratio (Modular-Composite): {df['ratio_mc'].mean():.4f}")
    
    return df

if __name__ == "__main__":
    modular_growth_audit(horizon=500000)
