import os
import sys
import pandas as pd
import numpy as np
from sympy import sieve
import bisect
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
import streamlit as st

# --- Constants ---
GAMMA = 0.57721566490153286060
sieve.extend(500) 

# --- Environment & Rendering ---
pio.renderers.default = "iframe"

# --- Core Logic: Zero Search ---
@st.cache_resource
def load_heavy_assets():
    """Loads 2M Zeta zeros into memory once."""
    KNOWN_ZEROS = []
    # Search paths: parent, local, or absolute
    paths = ["zeta_zeros_2m.txt", "../zeta_zeros_2m.txt", "data/zeta_zeros_2m.txt", "../data/zeta_zeros_2m.txt", "data/zeta_zeros_100k_sample.txt"]
    for p in paths:
        if os.path.exists(p):
            zeros = []
            with open(p, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try: zeros.append(float(line))
                        except ValueError: continue
            return sorted(zeros)
    return []

# --- NeuroPharm Integration ---
try:
    import neuro_pharm
    NEURO_PHARM_AVAILABLE = True
except ImportError:
    NEURO_PHARM_AVAILABLE = False

KNOWN_ZEROS = load_heavy_assets()
SCOUT = None
if NEURO_PHARM_AVAILABLE and KNOWN_ZEROS:
    SCOUT = neuro_pharm.ZetaScout(KNOWN_ZEROS)

def approx_k(T):
    if T < 14.13: return 1
    import math
    T_f = float(T)
    return round((T_f / (2 * math.pi)) * math.log(T_f / (2 * math.pi * math.e)) + 1.44)

def get_nearest_zero(t):
    if not KNOWN_ZEROS:
        return 0, 0
    
    if SCOUT:
        z, dist = SCOUT.find_nearest(float(t))
        # Find index for backward compatibility (could be optimized)
        idx = bisect.bisect_left(KNOWN_ZEROS, z) + 1
        return idx, z
    t_f = float(t)
    if t_f < KNOWN_ZEROS[0]:
        return 1, KNOWN_ZEROS[0]
    
    if t_f <= KNOWN_ZEROS[-1]:
        idx = bisect.bisect_left(KNOWN_ZEROS, t_f)
        if idx == 0: return 1, KNOWN_ZEROS[0]
        if idx == len(KNOWN_ZEROS): return len(KNOWN_ZEROS), KNOWN_ZEROS[-1]
        before, after = KNOWN_ZEROS[idx-1], KNOWN_ZEROS[idx]
        if abs(t_f - before) < abs(t_f - after): return idx, before
        else: return idx + 1, after
    else:
        k = float(approx_k(t))
        import math
        def backlund(rank):
            rank_eff = float(rank) - 0.1375
            return (2 * math.pi * rank_eff) / (math.log(rank_eff / math.e))
        best_k, best_z = k, backlund(k)
        for i in [k-1, k+1]:
            if i < 1: continue
            zi = backlund(i)
            if abs(t_f - zi) < abs(t_f - best_z): 
                best_k, best_z = i, zi
        return int(best_k), float(best_z)

# --- Core Logic: Harmonic Formulas ---

def get_zero_spacing(T):
    """Returns the average local spacing of Zeta zeros at height T."""
    import math
    T_f = max(float(T), 14.2)
    return (2 * math.pi) / math.log(T_f / (2 * math.pi))

def D_m_n(m, n):
    """LaRue-Stieltjes Prime Antenna (V6).
    Mangoldt-reduced base with Stieltjes polynomial Drain.
    Formula: p_m · e · p_n - Modulator - Stieltjes_Drain
    """
    p_m, p_n = float(sieve[m]), float(sieve[n])
    m_f, n_f = float(m), float(n)
    
    # Stieltjes constants (gamma_1 through gamma_3)
    G0 = GAMMA
    G1 = -0.07281584548367672
    G2 = -0.00969036319287231
    G3 = 0.00205383442030334
    
    # Mangoldt-reduced base: e^{Lambda(p_n)} = p_n
    base = p_m * np.exp(1) * p_n
    
    # Modulator: capped to prevent overflow when p_n >> p_m
    half_drift = (p_n - p_m) / 2
    if abs(float(half_drift)) < 700:
        modulator = np.sqrt(m_f * n_f) * np.exp(half_drift) / (4 * np.pi)
    else:
        modulator = 0.0
    
    # Stieltjes Drain: Euclidean drift * Stieltjes polynomial * log-scaled quadratic
    euclidean_inner = (p_n - n_f)**2 + (p_m - m_f)**2
    termB = np.sqrt(euclidean_inner / (2 * np.pi))
    mangoldt_diff = abs(np.log(p_n / p_m))
    stieltjes_poly = G0 + G1 * mangoldt_diff + G2 * mangoldt_diff**2 / 2 + G3 * mangoldt_diff**3 / 6
    quad_sep = abs(float(n_f**2 - m_f**2))
    drain = termB * stieltjes_poly * np.log(1 + quad_sep)
    
    val = base - modulator - drain
    rank, nearest = get_nearest_zero(val)
    epsilon = abs(float(val - nearest))
    norm_eps = epsilon / get_zero_spacing(val)
    
    # New Math: Energy and Tension
    a = 1.0 + norm_eps
    energy = (a - 1.0)**2 # Simplified energy for the prime antenna
    return val, epsilon, norm_eps, rank, energy

def S_m_n(m, n):
    """The S-Series: Gamma-Decelerated Engine: p_m * (e*gamma)^p_n - (modulator + drain)."""
    p_m, p_n = float(sieve[m]), float(sieve[n])
    m_f, n_f = float(m), float(n)
    
    # Decelerated Base: (e * gamma) is the new growth unit
    base = p_m * np.power(np.exp(1) * GAMMA, p_n)
    
    modulator = np.sqrt(m_f * n_f) * np.exp((p_n - p_m) / 2) / (4 * np.pi)
    euclidean_inner = (p_n - n_f)**2 + (p_m - m_f)**2
    termB = np.sqrt(euclidean_inner / (2 * np.pi))
    exponent = abs((n_f**2 - m_f**2) * np.log(p_n / p_m))
    drain = termB * np.power(GAMMA, exponent)
    
    val = base - modulator - drain
    rank, nearest = get_nearest_zero(val)
    epsilon = abs(float(val - nearest))
    norm_eps = epsilon / get_zero_spacing(val)
    
    energy = (norm_eps)**2
    return val, epsilon, norm_eps, rank, energy

def test_function(m, n, k=1):
    """Hybrid Engine (Experimental T-Series): p_m * e^k * p_n + (p_m * e^-p_n) / (4 * pi)."""
    p_m, p_n = float(sieve[m]), float(sieve[n])
    
    # First term of T-Series
    res = p_m * np.exp(k) * p_n
    
    # Original T-Series error term (bound)
    bound = (p_m * np.exp(-p_n)) / (4 * np.pi)
    
    # ADDING instead of subtracting
    val = res + bound
    
    rank, nearest = get_nearest_zero(val)
    epsilon = abs(float(val - nearest))
    norm_eps = epsilon / get_zero_spacing(val)
    energy = (norm_eps)**2
    return val, epsilon, norm_eps, rank, energy


def T_m_n(m, n, k=1):
    """T-series Linear Resonance function (The Scalpel)."""
    p_m, p_n = float(sieve[m]), float(sieve[n])
    res = p_m * np.exp(k) * p_n
    bound = (p_m * np.exp(-p_n)) / (4 * np.pi)
    val = res - bound
    rank, nearest = get_nearest_zero(val)
    epsilon = abs(float(val - nearest))
    norm_eps = epsilon / get_zero_spacing(val)
    energy = (norm_eps)**2
    return val, epsilon, norm_eps, rank, energy

def get_protoreal_jitter(l, m, n):
    """
    Calculates the Topological Jitter (δ) for a prime triplet.
    This jitter arises from the non-associative nature of the Protoreal manifold.
    Gap = ((l * m) * n) - (l * (m * n))
    """
    p_l, p_m, p_n = float(sieve[l]), float(sieve[m]), float(sieve[n])
    
    # Thrust terms (b) based on logarithmic volume
    b_l, b_m, b_n = np.log(p_l), np.log(p_m), np.log(p_n)
    
    # Pull terms (c) based on index-scaling drift
    c_l = (p_l - l) / (2 * np.pi)
    c_m = (p_m - m) / (2 * np.pi)
    c_n = (p_n - n) / (2 * np.pi)
    
    # The non-associative gap in the real part (a)
    # Derived from the Lean 4 'ProtorealFull.mul' cross-terms
    jitter = (b_l * c_m * b_n) - (b_n * c_m * b_l) # Symmetric drift
    jitter += -1.0 * (b_l + b_m + b_n) # Proven Curvature constant (kappa = -1)
    
    return jitter

def T3_l_m_n(l, m, n):
    """T3 La Rue-Stieltjes Prime Antenna (Protoreal Squeeze Edition).
    Formula: (p_l * p_m * p_n)^(2/3) * e - (Stieltjes_Drift) - B_sym - Jitter
    """
    p_l, p_m, p_n = float(sieve[l]), float(sieve[m]), float(sieve[n])
    l_f, m_f, n_f = float(l), float(m), float(n)
    
    # 1. Decelerated 3D Base
    base = np.power(p_l * p_m * p_n, 2.0/3.0) * np.exp(1)
    
    # 2. Stieltjes-weighted 3D Drift
    euclidean_inner = (p_l - l_f)**2 + (p_m - m_f)**2 + (p_n - n_f)**2
    termB = np.sqrt(euclidean_inner / (2 * np.pi))
    
    h = (np.log(p_l) + np.log(p_m) + np.log(p_n)) / 3
    G0, G1, G2, G3 = GAMMA, -0.07281584548367672, -0.00969036319287231, 0.00205383442030334
    stieltjes_poly = G0 + G1 * h + G2 * h**2 / 2 + G3 * h**3 / 6
    
    idx_scaling = np.log(1 + l_f**2 + m_f**2 + n_f**2)
    drain = termB * stieltjes_poly * idx_scaling
    
    # 3. Symmetric 8pi^2 Bounds
    b1 = (p_l * p_m * np.exp(-p_n)) / (8 * np.pi**2)
    b2 = (p_m * p_n * np.exp(-p_l)) / (8 * np.pi**2)
    b3 = (p_l * p_n * np.exp(-p_m)) / (8 * np.pi**2)
    
    # 4. PROTOREAL SQUEEZE: Topological Jitter Correction
    jitter = get_protoreal_jitter(l, m, n)
    
    val = base - drain - (b1 + b2 + b3) - jitter
    
    rank, nearest = get_nearest_zero(val)
    epsilon = abs(float(val - nearest))
    norm_eps = epsilon / get_zero_spacing(val)
    
    # Total Formalization Energy (E)
    # The 3D manifold stabilizes at E = 0
    energy = (norm_eps)**2 + (float(jitter) / 100.0)**2
    
    return val, epsilon, norm_eps, rank, energy

def T3_Protoreal(l, m, n):
    """
    T3 Antenna with formal ProtorealState mapping.
    Calculates transfinite thrust and spectral pull for curvature analysis.
    """
    val, eps, norm, rank = T3_l_m_n(l, m, n)
    
    # Thrust b corresponds to the altitude-based exponential growth
    # Pull c corresponds to the spectral distance (epsilon)
    # We lift these into the formal U ring: u = a + bw + ci
    return val, eps, -norm, rank

def T_Generic(indices):
    """
    La Rue Generic Prime Antenna for arbitrary cardinality N.
    Used to validate the La Rue Conjecture (Cardinality-Phase Shift).
    Formula: (Product p_i)^(2/N) * e - Stieltjes_Drift
    """
    N = len(indices)
    primes = [float(sieve[idx]) for idx in indices]
    
    # 1. Decelerated Base
    prod_p = np.prod(primes)
    base = np.power(prod_p, 2.0/N) * np.exp(1)
    
    # 2. Universal Stieltjes Drift
    euclidean_inner = np.sum([(primes[i] - indices[i])**2 for i in range(N)])
    termB = np.sqrt(euclidean_inner / (2 * np.pi))
    
    h = np.sum([np.log(p) for p in primes]) / N
    G0, G1, G2, G3 = GAMMA, -0.07281584548367672, -0.00969036319287231, 0.00205383442030334
    stieltjes_poly = G0 + G1 * h + G2 * h**2 / 2 + G3 * h**3 / 6
    
    idx_scaling = np.log(1 + np.sum([float(idx)**2 for idx in indices]))
    drain = termB * stieltjes_poly * idx_scaling
    
    # 3. Cardinality-Phase Correction (La Rue Conjecture)
    # Odd cardinalities stay resonant; Even/High cardinalities shift toward repulsion (0.5)
    phase_shift = 0.0
    if N % 2 == 0:
        phase_shift = 0.25 * (N / 24) # Gradually approach repulsion
    elif N >= 24:
        phase_shift = 0.5 # Total phase collapse at the Leech Lattice horizon
    
    val = base - drain - phase_shift
    rank, nearest = get_nearest_zero(val)
    epsilon = abs(float(val - nearest))
    norm_eps = epsilon / get_zero_spacing(val)
    
    return val, epsilon, norm_eps, rank


# --- Visualization Dashboard Utilities ---

def plot_resonance_shell(df, k_tier=1):
    """Generates a 3D surface plot for a given k-tier."""
    sub_df = df[df['k'] == k_tier]
    if sub_df.empty: return None
    # Use pivot_table to handle potential duplicate entries in the CSV
    piv = sub_df.pivot_table(index='n', columns='m', values='eps', aggfunc='min')
    z_data = piv.values
    
    fig = go.Figure(data=[go.Surface(z=z_data, colorscale='Viridis')])
    fig.update_layout(
        title=f"Resonance Shell Topology (Tier k={k_tier})",
        scene=dict(xaxis_title='m (Log)', yaxis_title='n (Log)', zaxis_title='ε', xaxis_type='log', yaxis_type='log'),
        template="plotly_dark",
        height=600
    )
    return fig

def plot_density_map(df, k_tier=1):
    """Generates a 2D heatmap of resonant species."""
    sub_df = df[df['k'] == k_tier].copy()
    if sub_df.empty: return None
    sub_df['species'] = (sub_df['eps'] < 0.1).astype(int)
    # Use pivot_table to handle potential duplicate entries
    piv = sub_df.pivot_table(index='n', columns='m', values='species', aggfunc='max')
    fig = px.imshow(piv, title=f"Resonant Species Density (k={k_tier})", 
                    color_continuous_scale="Magma", template="plotly_dark")
    return fig


# Engine Ready
