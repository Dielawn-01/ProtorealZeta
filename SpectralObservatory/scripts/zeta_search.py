import sys
import os
import pandas as pd
import numpy as np

# Ensure the local core is discoverable
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import ZetaEngine as ze
import core.ProtorealEngine as ue

def monster_zeta_search(horizon=2000000, batch_size=50000):
    """
    The 𝕌-Stitched Monster Search:
    Performs a 2M-zero scan using the Parity-Locked Monster Inverse logic.
    Identifies the precise 'a' connection for each spectral zero.
    """
    print(f"📡 Initiating 𝕌-Stitched Monster Search (Horizon: {horizon})")
    print(f"🛠️  Engine: Klein-Projective | Monster Inverse Stitch | Hyperbolic Gradient")
    
    zeros = ze.KNOWN_ZEROS
    if not zeros:
        print("❌ Error: No zeros found.")
        return
    
    actual_horizon = min(len(zeros), horizon)
    results = []
    
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'monster_zeta_audit.csv')
    
    for rank in range(actual_horizon):
        try:
            t = zeros[rank]
            
            # 1. Start with raw projection (no bias)
            u_init = ue.ProtorealElement(a=0.0, b=float(t), c=1.0/float(t))
            
            # 2. Apply the Monster Stitch ( doubling + inversion averaging )
            u_stitched = ue.monster_stitch(u_init)
            
            # 3. Perform Hyperbolic Descent to find the equilibrium for this zero
            # We use the Synthesis engine to resolve the stitched tension
            synth = ue.ProtorealSynthesis(t=u_stitched.b, a=u_stitched.a)
            u_final = synth.solve_equilibrium(iterations=3)
            
            # 4. Measure Metrics
            sr = ue.calculate_standard_resonance(u_final)
            div = abs(u_final.a - 1.0) # Divergence from the Protoreal Fixed Point
            duality_delta = ue.verify_duality(u_final, re_s=0.5)
            
            results.append({
                'rank': rank + 1,
                't': t,
                'a_discovered': u_final.a,
                'sr': sr,
                'protoreal_divergence': div,
                'duality_delta': duality_delta,
                'curvature': float(synth.calculate_curvature().a)
            })
            
            if (rank + 1) % batch_size == 0:
                print(f"  ✨ Progress: {rank + 1}/{actual_horizon} | Mean Divergence: {np.mean([x['divergence_05'] for x in results[-batch_size:]]):.6f}")
                pd.DataFrame(results).to_csv(output_path, index=False)
                
        except Exception as e:
            pass
            
    df = pd.DataFrame(results)
    df.to_csv(output_path, index=False)
    
    print(f"\n✅ Monster Search Complete. Data saved to: {output_path}")
    return df

if __name__ == "__main__":
    monster_zeta_search()
