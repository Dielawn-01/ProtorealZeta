import os
import sys

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)

import streamlit as st
import pandas as pd
import numpy as np
import ZetaEngine as ze
import plotly.graph_objects as go
import plotly.express as px
from core.ProtorealEngine import ProtorealState, get_engine_status

st.set_page_config(page_title="La Rue Conjecture | 𝕌", page_icon="🌀", layout="wide")

# --- Premium CSS ---
st.markdown(r"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400&display=swap');
    .main { background-color: #0a0c10; }
    h1, h2, h3 { font-family: 'Inter', sans-serif !important; color: #e8eaf0 !important; }
    .stMarkdown p { font-family: 'Inter', sans-serif; color: #b0b8c8; font-size: 1.05rem; }
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(255,255,255,0.04), rgba(255,255,255,0.01));
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px; padding: 20px;
    }
    .conjecture-card {
        background: linear-gradient(135deg, rgba(0,255,204,0.05), rgba(0,0,0,0));
        border: 1px solid rgba(0,255,204,0.12);
        border-radius: 16px;
        padding: 28px;
        margin: 16px 0;
    }
</style>
""", unsafe_allow_html=True)

st.title("🌀 The La Rue Conjecture")
st.markdown("The Cardinality-Phase Shift: how prime sequence length determines resonance or repulsion.")
st.markdown("---")

# ════════════════════════════════════════════════════
# THE CONJECTURE
# ════════════════════════════════════════════════════

st.markdown(r"""
<div class="conjecture-card">
    <div style="font-family: 'JetBrains Mono', monospace; color: #00ffcc; font-size: 0.85rem; margin-bottom: 10px;">
        CONJECTURE (La Rue, 2026)
    </div>
    <div style="font-size: 1.15rem; color: #e8eaf0; line-height: 1.8;">
        The resonance phase of a prime sequence <b>(p₁, p₂, ..., pₙ)</b> is topologically determined by its cardinality <b>N</b>:
        <br>• <b>Odd N</b> → Resonance State (Phase 0.0) — zero-lock attraction
        <br>• <b>Even N</b> → Repulsion State (Phase 0.5) — midpoint wall
        <br>• <b>N = 24</b> → Monstrous Inversion — total phase collapse at the Leech Lattice horizon
    </div>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════
# CARDINALITY-PHASE DATA
# ════════════════════════════════════════════════════

MONSTROUS_PATH = os.path.join(BASE_PATH, "TheLab", "data", "monstrous_resonance_scan.csv")
MASS_PATH = os.path.join(BASE_PATH, "TheLab", "data", "mass_cardinality_scan.csv")

df = None
data_label = ""

if os.path.exists(MONSTROUS_PATH):
    df = pd.read_csv(MONSTROUS_PATH)
    data_label = "Monstrous Resonance Scan (N=1..24)"
elif os.path.exists(MASS_PATH):
    df = pd.read_csv(MASS_PATH)
    data_label = "Cardinality Scan (N=1..7)"

if df is not None:
    col_chart, col_table = st.columns([2, 1])
    
    with col_chart:
        st.subheader(f"📈 {data_label}")
        
        # Clean numeric data
        if 'Lock %' in df.columns and isinstance(df['Lock %'].iloc[0], str):
            df['LockNum'] = df['Lock %'].str.rstrip('%').astype(float)
            df['RepelNum'] = df['Repel %'].str.rstrip('%').astype(float)
        else:
            df['LockNum'] = df.get('Lock %', 0)
            df['RepelNum'] = df.get('Repel %', 0)
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df['N'], y=df['LockNum'], name="Resonance (Phase 0.0)",
            line=dict(color='#00ffcc', width=3), mode='lines+markers',
            marker=dict(size=8)
        ))
        fig.add_trace(go.Scatter(
            x=df['N'], y=df['RepelNum'], name="Repulsion (Phase 0.5)",
            line=dict(color='#ff4b4b', width=3, dash='dash'), mode='lines+markers',
            marker=dict(size=8)
        ))
        
        # Highlight phase inversions
        if 'Stability' in df.columns:
            inversions = df[df['Stability'] < 0]
            if not inversions.empty:
                fig.add_trace(go.Scatter(
                    x=inversions['N'], y=inversions['LockNum'],
                    mode='markers', marker=dict(color='#ff00ff', size=14, symbol='x', line=dict(width=2)),
                    name='Phase Inversion'
                ))
        
        fig.update_layout(
            template="plotly_dark",
            xaxis_title="Cardinality (N)",
            yaxis_title="Density %",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            height=500,
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter'),
            hovermode="x unified"
        )
        st.plotly_chart(fig, width='stretch')
    
    with col_table:
        st.subheader("📋 Phase Audit")
        display_cols = [c for c in ['N', 'State', 'Lock %', 'Repel %', 'Stability'] if c in df.columns]
        st.dataframe(df[display_cols], width='stretch', hide_index=True, height=450)
        
        if 'Stability' in df.columns:
            st.info("**Leech Lattice Horizon**: Beyond N=21, stability Δ drops below zero — total phase inversion.")
else:
    st.warning("Cardinality scan data not found. Run scripts in `TheLab/scripts/` to generate datasets.")

st.markdown("---")

# ════════════════════════════════════════════════════
# PROTOREAL TRIGONOMETRY
# ════════════════════════════════════════════════════

st.subheader("🔮 Protoreal Trigonometry — A Novel Function Family")

trig_col1, trig_col2 = st.columns([2, 1])

with trig_col1:
    st.markdown(r"""
    The Protoreal System generates functions **between standard trig and hyperbolic trig**:
    """)
    
    st.latex(r"U_{\cosh}(t) = \frac{e^{\omega t} + e^{\iota t}}{2}, \quad U_{\sinh}(t) = \frac{e^{\omega t} - e^{\iota t}}{2}")
    
    st.markdown("#### The Dynamic Pythagorean Identity (Proven in Lean 4)")
    st.latex(r"U_{\cosh}^2(t) - U_{\sinh}^2(t) = e^{(\omega - 1/\omega) \cdot t}")
    
    st.markdown(r"""
    | Property | Standard Trig | Hyperbolic | **Protoreal** |
    |---|---|---|---|
    | Identity | cos² + sin² = 1 | cosh² - sinh² = 1 | **U_cosh² - U_sinh² = e^((ω-1/ω)t)** |
    | Constant? | ✅ Yes | ✅ Yes | **❌ Dynamic** |
    | Fixed Point | — | — | **ω = 1 → recovers standard** |
    """)
    
    # Interactive visualization
    t_vals = np.linspace(-1.5, 1.5, 300)
    omega_val = st.slider("ω (transfinite parameter)", min_value=1.0, max_value=20.0, value=3.0, step=0.5)
    
    identity_vals = np.exp((omega_val - 1.0/omega_val) * t_vals)
    standard = np.ones_like(t_vals)
    
    fig_trig = go.Figure()
    fig_trig.add_trace(go.Scatter(x=t_vals, y=identity_vals, name=f"Protoreal (ω={omega_val})",
                                   line=dict(color='#00ffcc', width=3)))
    fig_trig.add_trace(go.Scatter(x=t_vals, y=standard, name="Standard (cosh²-sinh²=1)",
                                   line=dict(color='white', width=2, dash='dash')))
    fig_trig.update_layout(
        template="plotly_dark", height=400,
        xaxis_title="t", yaxis_title="Identity Value",
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02)
    )
    st.plotly_chart(fig_trig, width='stretch')

with trig_col2:
    st.markdown(r"""
    #### **Chiral Bridge**
    In the anti-commutative extension:
    
    **Left product:**  
    $(\omega\iota)^t = (-1)^t = e^{i\pi t}$  
    → Oscillates (trig-like)
    
    **Right product:**  
    $(\iota\omega)^t = (+1)^t = 1$  
    → Constant (flat)
    
    The **ordering of generators** determines whether you get waves or flatness. 
    This chirality is unique to the Protoreal System.
    """)
    
    st.markdown("---")
    st.markdown(r"""
    #### **Fixed Point Theorem**
    At **ω = 1**:
    
    $\omega + \iota = 1 + (-1) = 0$
    
    $e^{0 \cdot t} = 1$ for all $t$.
    
    **Standard hyperbolic functions are the degenerate case** of Protoreal trig. 
    The Protoreal identity reduces to the classical cosh² - sinh² = 1.
    
    *Proven in Lean 4 with* `simp` *and formally mapped in* `SpectralLattice.lean`.
    """)

st.markdown("---")

# ════════════════════════════════════════════════════
# REAL-TIME CARDINALITY SCOUT
# ════════════════════════════════════════════════════

st.subheader("🔭 Real-Time Cardinality Scout")

scout_col1, scout_col2 = st.columns([1, 2])

with scout_col1:
    indices_str = st.text_input("Prime Indices (comma-separated)", "14, 14, 14")
    try:
        indices = [int(x.strip()) for x in indices_str.split(",")]
        N = len(indices)
    except:
        indices = [14, 14, 14]
        N = 3
    
    st.metric("Cardinality N", N)
    st.caption("Odd → Resonance, Even → Repulsion")

if st.button("Deploy Antenna", type="primary"):
    try:
        val, eps, norm, rank = ze.T_Generic(indices)
        
        with scout_col2:
            st.subheader(f"📡 Antenna Report (N={N})")
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Predicted Height (t)", f"{float(val):.2f}")
            c2.metric("Normed Error (ε)", f"{float(norm):.4f}")
            c3.metric("Nearest Zero (γ_k)", f"k={int(rank)}")
            
            phase_val = float(norm) % 1.0
            st.progress(min(max(phase_val, 0.0), 1.0))
            
            if phase_val < 0.1:
                st.success("**RESONANCE** — Zero-Lock Attraction")
            elif 0.4 < phase_val < 0.6:
                st.error("**REPULSION** — Midpoint Wall")
            else:
                st.warning("**TRANSITIONAL** — Spectral Jitter")
    except Exception as e:
        st.error(f"Antenna error: {e}")

st.markdown("---")
st.markdown("#### **Next Step: The Klein Universe**")
st.markdown(r"""
The cardinality-phase shifts are best visualized as rotations on a non-orientable 
surface. Observe the global stability of the Klein Universe.
""")
if st.button("🌀 Proceed to The Klein Universe"):
    st.switch_page("pages/6_Klein_Universe.py")
