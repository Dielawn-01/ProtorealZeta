import os
import sys
import pandas as pd
import numpy as np

# Ensure ZetaEngine can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import ZetaEngine as ze

def run_comprehensive_test():
    print("🧪 Starting Comprehensive Repository Audit...")
    print("==========================================")

    # 1. Verify Assets
    print("\n[1/4] Verifying Heavy Assets...")
    zeros = ze.KNOWN_ZEROS
    if zeros:
        print(f"  ✅ Loaded {len(zeros):,} Zeta zeros.")
        print(f"  First Zero: {zeros[0]}, Last Zero: {zeros[-1]}")
    else:
        print("  ❌ Failed to load Zeta zeros!")

    # 2. Verify Engine Logic
    print("\n[2/4] Testing Resonance Engines...")
    test_coords = [(1, 1), (5, 7), (13, 17), (24, 24)]
    
    engines = {
        "D_m_n (Dylon)": ze.D_m_n,
        "S_m_n (Adelic)": ze.S_m_n,
        "T_m_n (T-Series)": ze.T_m_n,
        "test_function (Hybrid/Exp)": ze.test_function
    }

    for name, func in engines.items():
        print(f"  Scanning {name}:")
        for m, n in test_coords:
            try:
                val, eps, norm, rank = func(m, n)
                print(f"    ({m}, {n}) -> Norm: {float(norm):.6f}, Rank: {int(rank)}")
            except Exception as e:
                print(f"    ❌ ({m}, {n}) failed: {e}")

    print("  Scanning T3_l_m_n (3D):")
    for l, m, n in [(1,1,1), (5,7,11)]:
        try:
            val, eps, norm, rank = ze.T3_l_m_n(l, m, n)
            print(f"    ({l}, {m}, {n}) -> Norm: {float(norm):.6f}, Rank: {int(rank)}")
        except Exception as e:
            print(f"    ❌ ({l}, {m}, {n}) failed: {e}")

    # 3. Verify Data Directory
    print("\n[3/4] Checking Data Integrity...")
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
    if os.path.exists(data_dir):
        files = os.listdir(data_dir)
        print(f"  ✅ Data directory found with {len(files)} files.")
        for f in files:
            if f.endswith('.csv'):
                try:
                    df = pd.read_csv(os.path.join(data_dir, f), nrows=5)
                    print(f"    - {f:<30} | {len(df.columns):>2} columns | OK")
                except Exception as e:
                    print(f"    - {f:<30} | ❌ Corrupt: {e}")
    else:
        print("  ❌ Data directory NOT found!")

    # 4. Verify Pages Pathing
    print("\n[4/4] Auditing Streamlit Pages...")
    pages_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'pages')
    if os.path.exists(pages_dir):
        pages = [f for f in os.listdir(pages_dir) if f.endswith('.py')]
        print(f"  ✅ Found {len(pages)} pages.")
        # Check for path consistency
        for p in pages:
            with open(os.path.join(pages_dir, p), 'r') as f:
                content = f.read()
                if "pd.read_csv" in content and "data" not in content:
                    print(f"    ⚠️ {p:<30} | Potential broken path detected!")
                else:
                    print(f"    ✅ {p:<30} | Path audit passed.")
    else:
        print("  ❌ Pages directory NOT found!")

    print("\n==========================================")
    print("✅ Audit Complete.")

if __name__ == "__main__":
    run_comprehensive_test()
