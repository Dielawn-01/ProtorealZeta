import time
import math
import sys
import os
import numpy as np

# Ensure ZetaEngine can be imported from parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import ZetaEngine as ze

def t3_legacy(l, m, n):
    """Legacy T3 Antenna (Pre-Protoreal Squeeze)"""
    p_l, p_m, p_n = float(ze.sieve[l]), float(ze.sieve[m]), float(ze.sieve[n])
    base = ((p_l * p_m * p_n)**(2/3)) * math.e
    euclidean_inner = (p_l - l)**2 + (p_m - m)**2 + (p_n - n)**2
    termB = math.sqrt(euclidean_inner / (2 * math.pi))
    h = (math.log(p_l) + math.log(p_m) + math.log(p_n)) / 3
    G = [0.5772156649015328606, -0.0728158454836767249, -0.0096903631928723185, 0.0020538344203033459]
    stieltjes_poly = G[0] + G[1] * h + G[2] * h**2 / 2 + G[3] * h**3 / 6
    idx_scaling = math.log1p(l**2 + m**2 + n**2)
    drain = termB * stieltjes_poly * idx_scaling
    b_sum = (p_l * p_m * math.exp(-p_n)) / (8 * math.pi**2) + (p_m * p_n * math.exp(-p_l)) / (8 * math.pi**2) + (p_l * p_n * math.exp(-p_m)) / (8 * math.pi**2)
    return base - drain - b_sum

BUDGET = 5000

print(f"=== BATTLE OF THE ANTENNAS (Budget={BUDGET:,}) ===\n")

# Run Legacy
start_l = time.time()
l_hits = 0; l_count = 0
for l in range(1, 20):
    for m in range(1, 20):
        for n in range(1, 20):
            try:
                val = t3_legacy(l, m, n)
                rank, nearest = ze.get_nearest_zero(val)
                norm = float(abs(val - nearest) / ze.get_zero_spacing(val))
                l_count += 1
                if norm < 0.1: l_hits += 1
            except: pass
time_l = time.time() - start_l

# Run Protoreal Squeeze
start_u = time.time()
u_hits = 0; u_count = 0
for l in range(1, 20):
    for m in range(1, 20):
        for n in range(1, 20):
            try:
                val, eps, norm, rank = ze.T3_l_m_n(l, m, n)
                u_count += 1
                if norm < 0.1: u_hits += 1
            except: pass
time_u = time.time() - start_u

print(f"  Legacy T3 Antenna    | Hit Rate: {100*l_hits/l_count:.2f}% | Count: {l_count}")
print(f"  Protoreal Squeeze T3    | Hit Rate: {100*u_hits/u_count:.2f}% | Count: {u_count}")
print(f"\nOptimization Delta: {((u_hits/u_count)/(l_hits/l_count)-1)*100:+.2f}% accuracy gain.")
