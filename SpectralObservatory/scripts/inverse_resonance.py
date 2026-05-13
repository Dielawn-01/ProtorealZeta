"""
T3 Inverse Resonance Engine: Prime Prediction Experiment.
Using the La Rue-Stieltjes Antenna to 'predict' primes from Zeta zeros.
"""
import math
import sys
import os

# Ensure ZetaEngine can be imported from parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import ZetaEngine as ze
from mpmath import mp

# Stieltjes constants
G0 = mp.euler
G1 = mp.mpf('-0.0728158454836767249')
G2 = mp.mpf('-0.0096903631928723185')
G3 = mp.mpf('0.0020538344203033459')

def predict_prime_from_zero(l, m, target_k):
    # 1. Get the target zero value
    if target_k <= len(ze.KNOWN_ZEROS):
        gamma_k = mp.mpf(ze.KNOWN_ZEROS[target_k - 1])
    else:
        # Fallback to Backlund approximation for ultra-high rank
        rank_eff = float(target_k) - 0.1375
        gamma_k = (2 * mp.pi * rank_eff) / (mp.log(rank_eff / mp.e))
    
    p_l, p_m = mp.mpf(ze.sieve[l]), mp.mpf(ze.sieve[m])
    l_mp, m_mp = mp.mpf(l), mp.mpf(m)
    
    # We need to find p_n such that T3(l, m, n) approx gamma_k
    # Simplified Base: (p_l * p_m * p_n)^(2/3) * e
    # For a first approximation, we assume Drain and Bounds are small compared to Base
    # p_n_approx = (gamma_k / (e * (p_l * p_m)^(2/3)))^(3/2)
    
    base_target = gamma_k # Start with gamma_k as the target for the base
    
    # Iterative refinement to account for Drain
    p_n_est = mp.power(base_target / (mp.exp(1) * mp.power(p_l * p_m, mp.mpf('0.666666666666666667'))), mp.mpf('1.5'))
    
    # Modular Constraint: n must satisfy (l + m + n) % 24 == 14
    # Let's find the nearest n to our p_n_est index
    # (Actually we want the prime value, but let's see where the index lands)
    
    # Refine p_n_est by adding back the Drain estimate
    # h = (ln(p_l) + ln(p_m) + ln(p_n)) / 3
    h = (mp.log(p_l) + mp.log(p_m) + mp.log(p_n_est)) / 3
    stieltjes_poly = G0 + G1 * h + G2 * h**2 / 2 + G3 * h**3 / 6
    
    # We don't know 'n' yet for idx_scaling, so we use a proxy
    # Since p_n approx n log n, we use n approx p_n / log p_n
    n_est = p_n_est / mp.log(p_n_est)
    idx_scaling = mp.log(1 + l_mp**2 + m_mp**2 + n_est**2)
    
    # Re-calculate Drain with estimate
    # termB uses (p_n - n) which we'll approximate as 0 for the first pass
    # termB = sqrt(((p_l-l)^2 + (p_m-m)^2 + (p_n-n)^2) / 2pi)
    termB = mp.sqrt(((p_l-l_mp)**2 + (p_m-m_mp)**2) / (2 * mp.pi))
    drain_est = termB * stieltjes_poly * idx_scaling
    
    # Adjusted Base Target
    base_target = gamma_k + drain_est
    p_n_final = mp.power(base_target / (mp.exp(1) * mp.power(p_l * p_m, mp.mpf('0.666666666666666667'))), mp.mpf('1.5'))
    
    return p_n_final

def test_prediction():
    print("🔮 Inverse Resonance Engine: Initializing Prime Prediction...")
    
    # Test on a known high-rank zero
    target_k = 2000000
    l, m = 80, 52 # From our 'Super-Hit' species
    
    p_n_predicted = predict_prime_from_zero(l, m, target_k)
    
    print(f"\nTarget: Zeta Zero #{target_k:,}")
    print(f"Fixed Indices: l={l}, m={m}")
    print(f"Predicted Prime Value ($p_n$): {float(p_n_predicted):,.2f}")
    
    # Find the closest actual prime in our sieve
    # We search the sieve for the closest value
    p_actual = 0; n_actual = 0
    min_diff = float('inf')
    for n, p in enumerate(ze.sieve):
        if n == 0: continue
        diff = abs(float(p) - float(p_n_predicted))
        if diff < min_diff:
            min_diff = diff
            p_actual = p
            n_actual = n
        if p > p_n_predicted * 1.1: break
            
    print(f"Closest Actual Prime in Sieve: {p_actual} (Index n={n_actual})")
    print(f"Prediction Accuracy: {100 * (1 - abs(float(p_actual) - float(p_n_predicted)) / float(p_actual)):.4f}%")
    
    # Check modular constraint
    mod_sum = (l + m + n_actual) % 24
    print(f"Index Sum Mod 24: {mod_sum} (Target: 14)")

if __name__ == "__main__":
    test_prediction()
