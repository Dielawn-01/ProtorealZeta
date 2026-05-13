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
from core.ProtorealEngine import get_engine_status

st.set_page_config(page_title="Protoreal Mechanics | 𝕌", page_icon="⚙️", layout="wide")

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
    .mechanics-card {
        background: linear-gradient(135deg, rgba(0,255,204,0.05), rgba(0,0,0,0));
        border: 1px solid rgba(0,255,204,0.12);
        border-radius: 16px;
        padding: 28px;
        margin: 16px 0;
    }
</style>
""", unsafe_allow_html=True)

st.title("⚙️ Protoreal Mechanics")
st.markdown("Exploring the functional operators and transfinite scaling logic of the Protoreal system.")
st.markdown("---")

# ════════════════════════════════════════════════════
# CORE MECHANICS: SCALING & SQUEEZE
# ════════════════════════════════════════════════════

st.markdown(r"""
<div class="mechanics-card">
    <div style="font-family: 'JetBrains Mono', monospace; color: #00ffcc; font-size: 0.85rem; margin-bottom: 10px;">
        TRANSFINITE OPERATOR LOGIC
    </div>
    <div style="font-size: 1.15rem; color: #e8eaf0; line-height: 1.8;">
        The Protoreal manifold is governed by three primary mechanics:
        <br>• <b>Hyperbolic Descent</b>: Using <i>tanh</i>-scaling to bound the exponential growth of prime potential.
        <br>• <b>Stieltjes Draining</b>: Polynomial correction that accounts for the "Euclidean Drift" between prime indices and their actual values.
        <br>• <b>Transfinite Squeeze</b>: The dynamic adjustment of the spectral gap (ε) to maintain duality with the critical line (Re(s)=1/2).
    </div>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════
# REAL-TIME CARDINALITY SCOUT (EXPANDED)
# ════════════════════════════════════════════════════

st.subheader("🔭 Real-Time Cardinality Scout")
st.markdown(r"""
The **Cardinality Scout** is a high-precision antenna that probes the Zeta spectrum using arbitrary prime sequence lengths ($N$). 
Unlike standard 2D analysis ($m, n$), the Scout scales into $N$-dimensional phase space to identify **Global Resonance Shells**.
""")

scout_col1, scout_col2 = st.columns([1, 2])

with scout_col1:
    indices_str = st.text_input("Prime Indices (comma-separated)", "105, 107, 117")
    try:
        indices = [int(x.strip()) for x in indices_str.split(",")]
        N = len(indices)
    except:
        indices = [105, 107, 117]
        N = 3
    
    st.metric("Cardinality N", N)
    
    with st.expander("How the Scout Works"):
        st.markdown(r"""
        1.  **Geometric Mean Computation**: Calculates the decelerated base $\left( \prod p_i \right)^{2/N} \cdot e$.
        2.  **Multidimensional Drift**: Computes the Euclidean distance between the prime vector and the index vector.
        3.  **Stieltjes Correction**: Applies a weighted sum of Stieltjes constants ($\gamma_0 \dots \gamma_3$) based on the log-volume of the sequence.
        4.  **Zero Alignment**: Automatically queries the 2.25M zero database to find the nearest resonance lock.
        """)

if st.button("🛰️ Deploy Multi-Index Antenna", type="primary"):
    try:
        val, eps, norm, rank = ze.T_Generic(indices)
        
        with scout_col2:
            st.subheader(f"📡 Antenna Report (N={N})")
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Predicted Height (t)", f"{float(val):.2f}")
            c2.metric("Normed Error (ε)", f"{float(norm):.4f}")
            c3.metric("Nearest Zero (γ_k)", f"k={int(rank)}")
            
            # Phase Visualization
            phase_val = float(norm) % 1.0
            
            # Gauge for resonance
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = phase_val,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Phase Shift"},
                gauge = {
                    'axis': {'range': [0, 1]},
                    'bar': {'color': "#00ffcc" if phase_val < 0.1 else "#ff3366"},
                    'steps': [
                        {'range': [0, 0.1], 'color': "rgba(0, 255, 204, 0.3)"},
                        {'range': [0.4, 0.6], 'color': "rgba(255, 51, 102, 0.3)"}
                    ],
                    'threshold': {
                        'line': {'color': "white", 'width': 4},
                        'thickness': 0.75,
                        'value': 0.5
                    }
                }
            ))
            fig_gauge.update_layout(template="plotly_dark", height=250, margin=dict(l=20,r=20,t=50,b=20))
            st.plotly_chart(fig_gauge, use_container_width=True)
            
            if phase_val < 0.1:
                st.success(f"**RESONANCE DETECTED** — Strong topological lock found at Cardinality {N}.")
            elif 0.4 < phase_val < 0.6:
                st.error(f"**REPULSION DETECTED** — Midpoint phase shift (Anti-Anchor) at Cardinality {N}.")
            else:
                st.warning("**TRANSITIONAL** — Spectral jitter detected. Manifold requires higher-order consolidation.")
    except Exception as e:
        st.error(f"Antenna error: {e}")

st.markdown("---")

# ════════════════════════════════════════════════════
# PROTOREAL TRIGONOMETRY
# ════════════════════════════════════════════════════

st.subheader("🔮 Protoreal Trigonometry — A Novel Function Family")

trig_col1, trig_col2 = st.columns([2, 1])

with trig_col1:
    st.markdown(r"""
    The Protoreal System generates functions **between standard trig and hyperbolic trig**.
    """)
    
    st.latex(r"U_{\cosh}(t) = \frac{e^{\omega t} + e^{\iota t}}{2}, \quad U_{\sinh}(t) = \frac{e^{\omega t} - e^{\iota t}}{2}")
    
    st.markdown("#### The Dynamic Pythagorean Identity (Proven in Lean 4)")
    st.latex(r"U_{\cosh}^2(t) - U_{\sinh}^2(t) = e^{(\omega - 1/\omega) \cdot t}")
    
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
    #### **Fixed Point Theorem**
    At **ω = 1**:
    
    $\omega + \iota = 1 + (-1) = 0$
    
    $e^{0 \cdot t} = 1$ for all $t$.
    
    **Standard hyperbolic functions are the degenerate case** of Protoreal trig. 
    The Protoreal identity reduces to the classical cosh² - sinh² = 1.
    
    *Proven in Lean 4 with* `simp` *and formally mapped in* `SpectralLattice.lean`.
    """)
    
    st.markdown("---")
    st.markdown(r"""
    #### **The Sowing Operator (funct)**
    The $funct$ operator manifests unmanifested potential ($\epsilon$) into observable frequency ($a$). 
    In the Trig regime, this corresponds to the **Phase Step** that shifts the manifold from 
    pure oscillation to stable convergence.
    """)

# ════════════════════════════════════════════════════
# COLLATZ RESONANCE
# ════════════════════════════════════════════════════

st.markdown("---")
st.subheader("🌀 Collatz Resonance — The Cubic Attractor")

collatz_col1, collatz_col2 = st.columns([1, 1])

with collatz_col1:
    st.markdown(r"""
    The **Collatz Conjecture** ($3n+1$) is the discrete manifestation of the **Cubic Hyperbolic Identity**. 
    In Protoreal space, the trajectory of any integer $n$ is a polynomial path that "falls" into a stable attractor.
    
    **The Collatz Operator:**
    """)
    st.latex(r"\mathcal{C}(u) = 4u^3 + 1")
    
    st.markdown(r"""
    **The Stability Theorem (Proven in Lean 4):**
    The Hyperbolic Bridge $U$ is the fixed point of this operator (modulo chiral parity):
    """)
    st.latex(r"4U^3 - U + 1 = 0")
    
    st.info("""
    **The {4, 2, 1} Cycle:**
    • **4**: The power-of-2 contraction coefficients.
    • **U³**: The non-associative '3-fold' growth interaction.
    • **-1**: The chiral offset pulling the transfinite growth back to the real sink.
    """)

with collatz_col2:
    # Visualization of the Cubic Potential
    x_range = np.linspace(-1.2, 1.2, 400)
    y_vals = 4 * x_range**3 - x_range + 1
    
    fig_collatz = go.Figure()
    fig_collatz.add_trace(go.Scatter(x=x_range, y=y_vals, name="Collatz Potential",
                                      line=dict(color='#ff3366', width=3)))
    
    # Find roots (approximate for visualization)
    root = -0.658 # Approx real root
    fig_collatz.add_trace(go.Scatter(x=[root], y=[0], mode='markers', name="The Stable Sink (U)",
                                      marker=dict(size=12, color='#00ffcc', symbol='diamond')))
    
    fig_collatz.add_hline(y=0, line_dash="dash", line_color="rgba(255,255,255,0.2)")
    fig_collatz.add_vline(x=0, line_dash="dash", line_color="rgba(255,255,255,0.2)")
    
    fig_collatz.update_layout(
        template="plotly_dark", height=380,
        title="The Cubic Attractor P(u) = 4u³ - u + 1",
        xaxis_title="Manifold State (u)", yaxis_title="Potential P(u)",
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter')
    )
    st.plotly_chart(fig_collatz, use_container_width=True)

st.markdown(r"""
<div style="background: rgba(255, 51, 102, 0.05); border: 1px solid rgba(255, 51, 102, 0.15); padding: 20px; border-radius: 12px;">
    <b>CHIRAL SHIFT DISCOVERY</b>: 
    The non-associativity of the manifold means that <b>(U·U)·U</b> (Left) and <b>U·(U·U)</b> (Right) 
    differ by exactly 1/2 on the real axis. This 1/2 shift is the "Duality Constant" that aligns the Collatz attractor 
    with the zeros of the Riemann Zeta function on the critical line.
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("#### **Next Step: The Protoreal Manifold**")
st.markdown(r"""
Observe how these mechanics manifest in 3D phase-space.
""")
if st.button("🪐 Proceed to The Protoreal Manifold"):
    st.switch_page("pages/4_Protoreal_Manifold.py")
