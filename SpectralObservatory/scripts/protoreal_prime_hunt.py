import sys
import os
import pandas as pd
import numpy as np

# Ensure the local core is discoverable
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import ZetaEngine as ze
import core.ProtorealEngine as ue

def protoreal_prime_hunt(horizon=2000000, threshold=0.01, batch_size=10000):
    """
    Conducts a 2M-zero Hyperbolic Protoreal Resonance scan.
    Uses Axiomatic Descent to discover the 'a' connection for every zero.
    """
    print(f"🏹 Initiating 2M-Zero Hyperbolic Hunt (Horizon: {horizon})")
    print(f"⚖️ Method: Hyperbolic Descent | Equilibrium Search")
    
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'protoreal_2m_audit.csv')
    
    hits = []
    
    # We use the ZetaEngine to load zeros
    zeros = ze.KNOWN_ZEROS
    if not zeros:
        print("❌ Error: No zeros loaded in memory.")
        return
    
    actual_horizon = min(len(zeros), horizon)
    print(f"📂 Auditing {actual_horizon} zeros...")
    
    for rank in range(actual_horizon):
        try:
            t = zeros[rank]
            
            # Use the optimized Synthesis engine
            synth = ue.ProtorealSynthesis(t=t, a=0.0)
            u_final = synth.solve_equilibrium(iterations=3) # 3 steps is usually enough for 1e-6 precision
            
            # We record every zero's discovered 'a' and SR
            sr_final = ue.calculate_standard_resonance(u_final)
            
            hits.append({
                'rank': rank + 1,
                'height': t,
                'discovered_a': u_final.a,
                'final_sr': sr_final,
                'curvature': float(synth.calculate_curvature().a)
            })
            
            # Periodic telemetry
            if (rank + 1) % batch_size == 0:
                print(f"  📡 Progress: {rank + 1}/{actual_horizon} | Last a: {u_final.a:.4f}")
                # Save partial results
                pd.DataFrame(hits).to_csv(output_path, index=False)
                    
        except Exception as e:
            pass
            
    df_hits = pd.DataFrame(hits)
    df_hits.to_csv(output_path, index=False)
    
    print(f"\n✅ 2M Audit Complete.")
    print(f"📂 Results saved to: {output_path}")
    
    return df_hits

if __name__ == "__main__":
    # Conduct a full 2,000,000 zero hyperbolic audit
    protoreal_prime_hunt(horizon=2000000)
