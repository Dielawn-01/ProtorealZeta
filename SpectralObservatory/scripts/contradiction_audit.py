import sys
import os
import pandas as pd
import numpy as np

# Ensure ZetaEngine can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import ZetaEngine as ze

def statistical_contradiction_audit(n_zeros=500000):
    print(f"🕵️ Initiating Contradiction Audit (Horizon: {n_zeros} Zeros)")
    print("🔭 Searching for Phase Drift and Structural Entropy...")
    
    # We will sample indices that SHOULD be stable according to our Protoreal Axioms
    # Mod 24 Anchor: 14, 18, 20
    # Prime Square: 9
    anchors = [9, 14, 18, 20]
    
    anomalies = []
    
    # We'll sample 100,000 triplets and filter for those in the anchor channels
    import random
    for i in range(100000):
        l = random.randint(1, 150)
        m = random.randint(1, 150)
        n = random.randint(1, 150)
        
        mod24 = (l + m + n) % 24
        if mod24 in anchors:
            try:
                val, eps, norm, rank = ze.T3_l_m_n(l, m, n)
                norm = float(norm)
                
                # A contradiction is a point in an anchor channel that is NEITHER
                # resonant (norm < 0.1) NOR repelled (norm > 0.4 & norm < 0.6).
                # These are "ε-Dominant" noise states that defy the Protoreal Binary Lock.
                if 0.2 < norm < 0.3:
                    anomalies.append({
                        'l': l, 'm': m, 'n': n,
                        'norm': norm,
                        'mod24': mod24,
                        'height': val
                    })
            except: pass
            
    df_anomalies = pd.DataFrame(anomalies)
    
    if df_anomalies.empty:
        print("✅ No significant phase contradictions found in this sample.")
        return

    print(f"\n⚠️ CONTRADICTIONS DETECTED: {len(df_anomalies)} points exhibit 'Phase Drift'.")
    print("These points are in Anchor Channels but stuck in the ε-Noise (0.2 - 0.3).")
    
    # Look for patterns in the drift
    print("\n📊 Drift Distribution by Channel:")
    print(df_anomalies['mod24'].value_counts())
    
    # Check for Saturation Failure (Does height correlate with drift?)
    corr = df_anomalies['height'].corr(df_anomalies['norm'])
    print(f"\n📡 Saturation Correlation (Height vs Drift): {corr:.4f}")
    
    if abs(corr) > 0.5:
        print("❗ SATURATION FAILURE DETECTED: The drift increases with altitude.")
    else:
        print("✅ SATURATION HOLDS: The drift is statistically independent of altitude.")

    print("\n🛰️ Top Anomalous Triplets:")
    print(df_anomalies.sort_values('norm', ascending=False).head(10).to_string(index=False))

if __name__ == "__main__":
    statistical_contradiction_audit()
