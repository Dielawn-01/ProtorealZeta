import pandas as pd
import numpy as np
import goait 
import os

def feature_engineer(limit=2000000):
    input_path = "/home/phrxmaz/Documents/Prime Search/zeta_zeros_2m.txt"
    output_dir = "/home/phrxmaz/Documents/zetadata"
    output_path = os.path.join(output_dir, "goait_augmented_dataset.csv")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    print(f"🧬 Loading {limit} zeros from {input_path}...")
    
    zeros = []
    with open(input_path, 'r') as f:
        for i, line in enumerate(f):
            if i >= limit: break
            line = line.strip()
            if line:
                try: zeros.append(float(line))
                except: continue
                
    df = pd.DataFrame({'t': zeros})
    df['index'] = df.index + 1
    
    print("✨ Engineering Protoreal & Modular features...")
    
    # 1. Modular Phase (Mod-24 Monstrous Symmetry)
    df['mod24'] = df['index'] % 24
    df['modular_sine'] = np.sin(2 * np.pi * df['mod24'] / 24)
    
    # 2. Local Spacing
    df['local_spacing'] = 2 * np.pi / np.log(np.maximum(df['t'], 14.2) / (2 * np.pi))
    
    # 3. Protoreal Components (Simulation)
    # We map 't' to the real part 'a'
    # b (Thrust) is log-scaled height
    # c (Pull) is simulated jitter based on modular phase
    df['protoreal_a'] = df['t']
    df['protoreal_b'] = np.log(df['t'])
    df['protoreal_c'] = 0.1 * np.cos(2 * np.pi * df['mod24'] / 24) # Modular pull
    
    # 4. Topological Jitter (Goait Engine)
    # Using the Goait Rust core to calculate local associator magnitude
    def get_local_jitter(row):
        u = goait.ProtorealFull(row['protoreal_a'], row['protoreal_b'], row['protoreal_c'])
        return goait.get_jitter(u, u, u)
    
    # Sampling for performance (or vectorizing if possible)
    # Since we can't easily vectorize the Rust call, we apply to a subset or use a proxy
    df['jitter'] = 0.0653 * (3 * df['protoreal_b']) # Proxy based on ZetaEngine.py:207
    
    # 5. Stochastic Features
    np.random.seed(42)
    df['stochastic_drift'] = np.cumsum(np.random.normal(0, 0.01, len(df)))
    df['stochastic_noise'] = np.random.normal(0, 0.005, len(df))
    
    # 6. Trade Resonance Pulse (Market Simulation)
    df['trade_resonance'] = np.sin(df['t'] * df['local_spacing']) * (1 - df['mod24'] / 24)
    
    print(f"💾 Saving augmented dataset to {output_path}...")
    df.to_csv(output_path, index=False)
    print("✅ Compilation complete.")

if __name__ == "__main__":
    feature_engineer()
