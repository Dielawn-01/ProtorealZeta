"""
T3 La Rue-Stieltjes Antenna (Final): The Decelerated Scalpel.
Testing at 100k budget to see if it sustains 15% resonance.
"""
import time
import math
import sys
import os

# Ensure ZetaEngine can be imported from parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import ZetaEngine as ze

G0 = 0.5772156649015328606
G1 = -0.0728158454836767249
G2 = -0.0096903631928723185
G3 = 0.0020538344203033459

BUDGET = 100000

def t3_final_antenna(l, m, n):
    p_l, p_m, p_n = float(ze.sieve[l]), float(ze.sieve[m]), float(ze.sieve[n])
    
    # 1. Decelerated 3D Base (The scale-invariant anchor)
    base = ((p_l * p_m * p_n)**(2/3)) * math.e
    
    # 2. Stieltjes-weighted 3D Drift
    euclidean_inner = (p_l - l)**2 + (p_m - m)**2 + (p_n - n)**2
    termB = math.sqrt(euclidean_inner / (2 * math.pi))
    
    h = (math.log(p_l) + math.log(p_m) + math.log(p_n)) / 3
    stieltjes_poly = G0 + G1 * h + G2 * h**2 / 2 + G3 * h**3 / 6
    
    # La Rue Scaling
    idx_scaling = math.log1p(l**2 + m**2 + n**2)
    
    drain = termB * stieltjes_poly * idx_scaling
    
    # 3. Symmetric 8pi^2 Bounds
    b1 = (p_l * p_m * math.exp(-p_n)) / (8 * math.pi**2)
    b2 = (p_m * p_n * math.exp(-p_l)) / (8 * math.pi**2)
    b3 = (p_l * p_n * math.exp(-p_m)) / (8 * math.pi**2)
    
    return base - drain - (b1 + b2 + b3)

print(f"=== T3 LA RUE-STIELTJES FINAL ANTENNA (Budget={BUDGET:,}) ===\n")
start = time.time()
count = 0; hits = 0; sum_norm = 0.0; total = 0
for l in range(1, BUDGET + 1):
    m_max = BUDGET // l
    if m_max < 1: break
    for m in range(1, m_max + 1):
        n_max = BUDGET // (l * m)
        if n_max < 1: break
        for n in range(1, n_max + 1):
            total += 1
            try:
                val = t3_final_antenna(l, m, n)
                rank, nearest = ze.get_nearest_zero(val)
                eps = abs(val - nearest)
                norm = float(eps / ze.get_zero_spacing(val))
                if norm != float('inf') and not math.isnan(norm):
                    count += 1
                    sum_norm += norm
                    if norm < 0.1: hits += 1
            except: pass

hr = hits / count if count > 0 else 0
avg = sum_norm / count if count > 0 else 0
print(f"  T3 Final Antenna                    | HR: {hr*100:>7.3f}% | Avg: {avg:>12.2f}")
print(f"\nTotal time: {time.time() - start:.1f}s")
