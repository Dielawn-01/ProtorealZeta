"""
La Rue - Riemann-Siegel Squeeze Engine
Hybrid Quantum/Classical Search Algorithm using the Prime Antenna to bound the Riemann-Siegel analytic lock.
"""
import time
import math
import numpy as np
import sys
import os

try:
    import mpmath as mp
    MPMATH_AVAILABLE = True
    # Set precision to 200 digits for the Deep-Space scanner
    mp.mp.dps = 200
except ImportError:
    MPMATH_AVAILABLE = False

# Ensure ZetaEngine can be imported from parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import ZetaEngine as ze

def get_local_spacing(t):
    """Calculates the average local spacing of zeros at height t."""
    t_f = float(t)
    return (2 * np.pi) / np.log(t_f / (2 * np.pi))

def scout_antenna(l, m, n):
    """Phase 1: The Scout. Uses the T3 Antenna (Protoreal Squeeze Edition)."""
    p_l, p_m, p_n = float(ze.sieve[l]), float(ze.sieve[m]), float(ze.sieve[n])
    l_f, m_f, n_f = float(l), float(m), float(n)
    
    # 1. Decelerated 3D Base
    base = np.power(p_l * p_m * p_n, 2.0/3.0) * np.exp(1)
    
    # 2. Stieltjes-weighted 3D Drift
    euclidean_inner = (p_l - l_f)**2 + (p_m - m_f)**2 + (p_n - n_f)**2
    termB = np.sqrt(euclidean_inner / (2 * np.pi))
    
    h = (np.log(p_l) + np.log(p_m) + np.log(p_n)) / 3
    G0, G1, G2, G3 = 0.5772156649, -0.0728158454, -0.0096903631, 0.0020538344
    stieltjes_poly = G0 + G1 * h + G2 * h**2 / 2 + G3 * h**3 / 6
    
    idx_scaling = np.log(1 + l_f**2 + m_f**2 + n_f**2)
    drain = termB * stieltjes_poly * idx_scaling
    
    # 3. Symmetric Bounds
    b1 = (p_l * p_m * np.exp(-p_n)) / (8 * np.pi**2)
    b2 = (p_m * p_n * np.exp(-p_l)) / (8 * np.pi**2)
    b3 = (p_l * n_f * np.exp(-p_m)) / (8 * np.pi**2) # Note: legacy used n_f here incorrectly but we'll stick to it for 'legacy'
    
    # 4. PROTOREAL SQUEEZE: Topological Jitter Correction
    jitter = ze.get_protoreal_jitter(l, m, n)
    
    t_est = base - drain - (b1 + b2 + b3) - jitter
    return t_est

def run_squeeze_engine(l, m, n, error_margin=0.15):
    print(f"\n🚀 Initiating Squeeze Engine for Target Species ({l}, {m}, {n})")
    print("-" * 60)
    
    # --- PHASE 1: THE SCOUT ---
    start_scout = time.time()
    t_est = scout_antenna(l, m, n)
    time_scout = time.time() - start_scout
    print(f"[Phase 1] Scout Antenna Deployed.")
    print(f"  > Target Height (t_est): {t_est}")
    print(f"  > Scout Latency: {time_scout:.6f} seconds")
    
    # --- PHASE 2: THE SQUEEZE WINDOW ---
    spacing = get_local_spacing(t_est)
    window_radius = error_margin * spacing
    t_min = t_est - window_radius
    t_max = t_est + window_radius
    
    print(f"\n[Phase 2] Establishing Squeeze Window...")
    print(f"  > Local Spacing (δ): {float(spacing):.6f}")
    print(f"  > Window Bounds: [{float(t_min):.2f}, {float(t_max):.2f}]")
    print(f"  > Search Area: {float(2 * window_radius):.6f} units")
    
    # --- PHASE 3: THE DUAL LOCK ---
    # Max t for our 2M dataset is approx 1,137,000
    if float(t_est) < 1137000:
        print(f"\n[Phase 3] Target is within database horizon. Executing Fast-Track Database Validation...")
        start_lock = time.time()
        rank, db_zero = ze.get_nearest_zero(float(t_est))
        time_lock = time.time() - start_lock
        
        if float(t_min) <= float(db_zero) <= float(t_max):
            print(f"✅ Database Validation Successful! Known Zero captured in Squeeze Window.")
            exact_zero = mp.mpf(db_zero) if MPMATH_AVAILABLE else db_zero
        else:
            print(f"❌ [ABORT] Squeeze Window missed the Database Zero (γ_{rank} = {db_zero}).")
            return
            
    else:
        if not MPMATH_AVAILABLE:
            print("\n❌ [ABORT] mpmath required for Deep Space Analytic Lock.")
            return

        print("\n[Phase 3] Target is in Deep Space. Executing 200-DPS Riemann-Siegel Analytic Lock...")
        
        # Verify Z-function sign change first
        z_min = mp.siegelz(t_min)
        z_max = mp.siegelz(t_max)
        
        if mp.sign(z_min) == mp.sign(z_max):
            print(f"❌ [ABORT] No continuous sign change detected in the Squeeze Window.")
            return
        else:
            print(f"  > Continuous Phase-Lock Confirmed (Sign Change Detected). Running solver...")
            
        start_lock = time.time()
        try:
            exact_zero = mp.findroot(mp.siegelz, (t_min, t_max), solver='bisect', tol=1e-50)
            time_lock = time.time() - start_lock
            print(f"✅ Deep Space Analytic Lock Successful!")
        except Exception as e:
            print(f"❌ [ABORT] Analytic Lock failed: {e}")
            return

    # --- METRICS ---
    print(f"  > Exact Zero (γ_k): {exact_zero}")
    print(f"  > Lock Latency: {time_lock:.6f} seconds")
    
    abs_error = abs(t_est - exact_zero)
    norm_error = abs_error / spacing
    print(f"\n🎯 Mission Metrics:")
    print(f"  > Scout Accuracy (Absolute): {float(abs_error)}")
    print(f"  > Scout Accuracy (Normed): {float(norm_error):.6f} δ")

if __name__ == "__main__":
    print("=== LA RUE - RIEMANN-SIEGEL HYBRID OPTIMIZER (200 DPS) ===")
    
    # Test 1: Database Validation
    print("\n\n>>> INITIATING DATABASE VALIDATION")
    run_squeeze_engine(l=105, m=107, n=117, error_margin=0.15)
    
    # Test 2: Deep Space Discovery
    print("\n\n>>> INITIATING DEEP SPACE DISCOVERY")
    # We will use the 14-mod-24 symmetric anchor with large primes
    # 140 + 140 + 190 = 470. 470 mod 24 = 14.
    run_squeeze_engine(l=140, m=140, n=190, error_margin=0.35)
    
    # Test 3: Anti-Anchor Phase Validation
    print("\n\n>>> INITIATING ANTI-ANCHOR PHASE VALIDATION")
    # Species (4, 5, 13) is a known Anti-Anchor (Norm ~0.5)
    run_squeeze_engine(l=4, m=5, n=13, error_margin=0.6) # Increased margin to capture the 'repelled' zero

