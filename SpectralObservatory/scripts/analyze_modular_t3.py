"""
Modular Analysis of T3 Resonant Species.
Identifying the 'Golden Channels' in the 3D Prime-Zeta Lattice.
"""
import os
import pandas as pd
import numpy as np

def analyze_modular_resonance():
    print("📊 Loading T3 Training Data...")
    df = pd.read_csv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 't3_training_data.csv'))
    
    # Filter for resonant species (Super-hits)
    resonant = df[df['norm'] < 0.1].copy()
    print(f"🎯 Total Resonant Species Found: {len(resonant)} (out of {len(df)})")
    
    # Calculate Mod 24 and Mod 6 for the sum of indices
    resonant['sum_mod_24'] = (resonant['l'] + resonant['m'] + resonant['n']) % 24
    resonant['sum_mod_6'] = (resonant['l'] + resonant['m'] + resonant['n']) % 6
    
    # Tiered Analysis
    for tier in ['Local', 'Mid', 'Deep']:
        sub = resonant[resonant['tier'] == tier]
        if sub.empty: continue
        
        print(f"\n--- {tier} Tier Analysis ---")
        
        # Mod 24 Distribution
        m24 = sub['sum_mod_24'].value_counts().head(5)
        print("Top 5 Mod-24 Channels:")
        for ch, count in m24.items():
            pct = (count / len(sub)) * 100
            print(f"  Channel {ch:>2} mod 24: {pct:>6.2f}% ({count} hits)")
            
        # Mod 6 Distribution
        m6 = sub['sum_mod_6'].value_counts()
        print("Mod-6 Distribution:")
        for ch, count in m6.items():
            pct = (count / len(sub)) * 100
            print(f"  Channel {ch} mod 6: {pct:>6.2f}%")
            
        # Top Species (Triplets)
        print("Most Resonant Species (Min Norm):")
        top_3 = sub.sort_values('norm').head(3)
        for _, row in top_3.iterrows():
            print(f"  ({int(row['l'])}, {int(row['m'])}, {int(row['n'])}) | Norm: {row['norm']:.8f} | Rank: {int(row['rank'])}")

if __name__ == "__main__":
    analyze_modular_resonance()
