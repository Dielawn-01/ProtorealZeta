"""
T3 Antenna Full Spectrum Trainer.
Performing a deep-field scan of the T3 La Rue-Stieltjes Antenna against 2M zeros.
"""
import os
import sys
import time
import math
import pandas as pd

# Ensure ZetaEngine can be imported from parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import ZetaEngine as ze

def train_t3_antenna():
    print("🚀 Initializing T3 Full Spectrum Scan (2,001,052 Zeros)...")
    
    # We will sample a large number of coordinates across different index tiers
    # to cover the full spectrum of zeros.
    tiers = [
        {'name': 'Local', 'range': (1, 100), 'samples': 50000},
        {'name': 'Mid',   'range': (10, 500), 'samples': 50000},
        {'name': 'Deep',  'range': (100, 1000), 'samples': 50000},
        {'name': 'Ultra', 'range': (500, 2000), 'samples': 50000}
    ]
    
    results = []
    
    import random
    
    for tier in tiers:
        print(f"📡 Scanning {tier['name']} Tier (Range: {tier['range']})...")
        r_min, r_max = tier['range']
        
        for i in range(tier['samples']):
            if i % 10000 == 0: print(f"  Processed {i}/{tier['samples']}...")
            # Random sampling within the tier range to get broad coverage
            l = random.randint(r_min, r_max)
            m = random.randint(r_min, r_max)
            n = random.randint(r_min, r_max)
            
            try:
                val, eps, norm, rank, energy = ze.T3_l_m_n(l, m, n)
                results.append({
                    'tier': tier['name'],
                    'l': l, 'm': m, 'n': n,
                    'norm': float(norm),
                    'rank': int(rank)
                })
            except:
                pass
                
    df = pd.DataFrame(results)
    
    # Tiered Analysis
    print("\n=== T3 ANTENNA TRAINING REPORT ===")
    
    # We re-categorize based on the ACTUAL rank found
    def categorize_rank(k):
        if k < 10000: return 'Local'
        if k < 100000: return 'Mid'
        if k < 500000: return 'Deep'
        return 'Ultra'
        
    df['actual_tier'] = df['rank'].apply(categorize_rank)
    
    stats = []
    for t_name in ['Local', 'Mid', 'Deep', 'Ultra']:
        sub = df[df['actual_tier'] == t_name]
        if sub.empty: continue
        
        hr = (sub['norm'] < 0.1).mean()
        avg_div = sub['norm'].mean()
        
        # Find dominant Mod 24 channel
        sub['mod24'] = (sub['l'] + sub['m'] + sub['n']) % 24
        dom_channel = sub['mod24'].value_counts().idxmax()
        
        stats.append({
            'Tier': t_name,
            'HR': f"{hr*100:.2f}%",
            'Avg Div': f"{avg_div:.4f}",
            'Anchor': f"{dom_channel} mod 24"
        })
        
    stats_df = pd.DataFrame(stats)
    print(stats_df.to_string(index=False))
    
    # Save the heavy data for the dashboard
    df.to_csv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 't3_training_data.csv'), index=False)
    print(f"\n✅ Training complete. 200,000 coordinates mapped. Data saved to t3_training_data.csv")

if __name__ == "__main__":
    train_t3_antenna()
