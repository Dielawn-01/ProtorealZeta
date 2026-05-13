import sys
import os
import pandas as pd
import numpy as np

# Ensure ZetaEngine can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import ZetaEngine as ze

def analyze_lrs_divergence(budget=500):
    print(f"🚀 Initiating LRS Divergence Analysis (Budget: {budget})")
    print("🔭 Scanning for Anti-Anchors (Maximum Repulsion Zones)...")
    
    results = []
    
    # We want a representative sample of the 3D space
    for l in range(1, 20):
        for m in range(1, 20):
            for n in range(1, 20):
                try:
                    val, eps, norm, rank, energy = ze.T3_l_m_n(l, m, n)
                    results.append({
                        'l': l, 'm': m, 'n': n,
                        'norm': float(norm),
                        'mod24': (l + m + n) % 24,
                        'mod6': (l + m + n) % 6
                    })
                except: pass
                
    df = pd.DataFrame(results)
    
    # Identify "Anti-Anchors": Points with norm_eps closest to 0.5 (Maximum Repulsion)
    # Since norm_eps is circular (0 and 1 are hits), 0.5 is the exact center of the "Dark Space"
    df['repulsion'] = abs(df['norm'] - 0.5)
    anti_anchors = df.sort_values('repulsion').head(50)
    
    print("\n--- 🕳️ Top Anti-Anchors Found (Max Repulsion) ---")
    print(anti_anchors[['l', 'm', 'n', 'norm', 'mod24', 'mod6']].head(10).to_string(index=False))
    
    # Modularity of Repulsion
    print("\n📊 Mod-24 Distribution of Anti-Anchors:")
    m24 = anti_anchors['mod24'].value_counts()
    for ch, count in m24.items():
        print(f"  Channel {ch:>2} mod 24: {count} instances")
        
    print("\n📊 Mod-6 Distribution of Anti-Anchors:")
    m6 = anti_anchors['mod6'].value_counts()
    for ch, count in m6.items():
        print(f"  Channel {ch} mod 6: {count} instances")

    # Compare against Super-Hits (Resonance)
    super_hits = df[df['norm'] < 0.1]
    print(f"\n✨ Super-Hits found in this sample: {len(super_hits)}")
    if not super_hits.empty:
        print("Mod-24 Distribution of Super-Hits:")
        print(super_hits['mod24'].value_counts().head(3))

if __name__ == "__main__":
    analyze_lrs_divergence()
