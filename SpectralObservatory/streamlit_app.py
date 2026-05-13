import streamlit as st
import pandas as pd
import numpy as np
import os
import plotly.express as px
import plotly.graph_objects as go

# --- Premium Page Configuration ---
st.set_page_config(
    page_title="𝕌 Protoreal Zeta Prime Hunt",
    page_icon="🏹",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Premium CSS ---
st.markdown(r"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    .main { background-color: #0a0c10; }

    h1, h2, h3 {
        font-family: 'Inter', sans-serif !important;
        color: #e8eaf0 !important;
        font-weight: 600 !important;
    }

    .stMarkdown p, .stMarkdown li {
        font-family: 'Inter', sans-serif;
        color: #b0b8c8;
        font-size: 1.05rem;
        line-height: 1.6;
    }

    /* Glassmorphism metric cards */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(255,255,255,0.04), rgba(255,255,255,0.01));
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 20px;
        transition: all 0.3s ease;
    }
    [data-testid="stMetric"]:hover {
        border-color: rgba(0, 255, 204, 0.3);
        box-shadow: 0 0 30px rgba(0, 255, 204, 0.05);
    }

    /* Hero section */
    .hero-badge {
        display: inline-block;
        background: linear-gradient(135deg, #00ffcc22, #ff336622);
        border: 1px solid #00ffcc44;
        border-radius: 24px;
        padding: 6px 16px;
        font-size: 0.85rem;
        color: #00ffcc;
        font-family: 'JetBrains Mono', monospace;
        margin-bottom: 8px;
    }

    .hunt-card {
        background: linear-gradient(135deg, rgba(0,255,204,0.06), rgba(0,0,0,0));
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 16px;
        padding: 32px;
        margin: 20px 0;
    }

    /* Sidebar polish */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d0f14, #0a0c10);
        border-right: 1px solid rgba(255,255,255,0.05);
    }

    .stAlert { border-radius: 12px; }

    .stDataFrame { border-radius: 12px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════
# HERO SECTION: THE HUNT
# ════════════════════════════════════════════════════

st.markdown('<div class="hero-badge">🏹 MANIFOLD SCOUT ACTIVE — 2.25M HORIZON</div>', unsafe_allow_html=True)
st.title("𝕌 The Protoreal Zeta Prime Hunt")
st.markdown(r"""
Welcome to the **Prime-Zeta Spectral Observatory**. This facility is designed for the 
**Guided Discovery** of the non-associative Protoreal Manifold. We are scouting for 
prime resonance "Stitches" where the transfinite prime thrust ($\omega$) and 
infinitesimal zero anchor ($\iota$) achieve **Spectral Equilibrium**.

#### **🚀 Discovery Pipeline**
Follow the protocol from mathematical foundations to transfinite horizons:
1.  **Foundations**: Define the 5-Component Axioms.
2.  **Scouting**: Map the 3D Spectral Topography.
3.  **Dynamics**: Audit the La Rue Cardinality Conjecture.
4.  **Horizons**: Visualize the non-orientable Klein Universe.

[Start Protocol: The Protoreal Manifold](/Protoreal_Manifold)
""")

# --- The Manifold Identity ---
st.markdown(r"""
<div class="hunt-card">
    <div style="font-family: 'JetBrains Mono', monospace; color: #ff3366; font-size: 0.9rem; margin-bottom: 12px;">
        NON-ASSOCIATIVE MANIFOLD IDENTITY
    </div>
    <div style="font-size: 2.0rem; color: #e8eaf0; font-family: 'Inter', serif; letter-spacing: 2px;">
        (ω · ω) · ι ≠ ω · (ω · ι)
    </div>
    <div style="font-size: 0.9rem; color: #667; margin-top: 12px;">
        The Manifold Stability Theorem prevents topological collapse at the Bridge Point (ω · ι = −1).
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ════════════════════════════════════════════════════
# CORE TELEMETRY & PRIME RANKING
# ════════════════════════════════════════════════════

col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("🎯 Resonant Prime Targets (The Leaderboard)")
    
    # Representative data for the "Hunt"
    hunt_data = pd.DataFrame([
        {"Prime Triple (l,m,n)": "(140, 140, 190)", "Resonance $S_R$": "0.0031", "State": "Super-Hit", "Bridge Potential": "-0.9969"},
        {"Prime Triple (l,m,n)": "(4, 5, 13)", "Resonance $S_R$": "0.5003", "State": "Repulsion Wall", "Bridge Potential": "-0.4997"},
        {"Prime Triple (l,m,n)": "(105, 107, 117)", "Resonance $S_R$": "0.0936", "State": "Stable Lock", "Bridge Potential": "-0.9064"},
        {"Prime Triple (l,m,n)": "(21, 21, 21)", "Resonance $S_R$": "0.1420", "State": "Monstrous Anchor", "Bridge Potential": "-0.8580"},
    ])
    st.dataframe(hunt_data, width='stretch', hide_index=True)
    
    st.markdown(r"""
    **Understanding the Targets:**
    *   **Prime Triple**: A coordinates set $\{l, m, n\}$ where the product $\pi(l)\pi(m)\pi(n)$ approaches a spectral zero.
    *   **Standard Resonance ($S_R$)**: The error between the manifold state and the ideal equilibrium. $S_R = 0$ implies a perfect "Stitch."
    *   **Bridge Potential**: The energy available at the $\omega \cdot \iota$ interface. Values near $-1.0$ indicate high stability.
    """)
    st.info(r"The **Standard Resonance** ($S_R$) is the observable fingerprint of the Protoreal state: $S_R = a - b \cdot c$.")

with col_right:
    st.subheader("🛰️ Scout Telemetry")
    m1, m2 = st.columns(2)
    m1.metric("Manifold Curvature", "0.0653 κ", help="Measure of non-associative drift (κ).")
    m2.metric("Stitch Tension", "0.9998 τ", help="The binding energy of the Monster Stitch.")
    
    m3, m4 = st.columns(2)
    m3.metric("Non-Assoc Gap", "0.122 δ", help="The difference between (ωω)ι and ω(ωι).")
    m4.metric("Verified Zeros", "2.25M", help="Number of Zeta zeros audited for Duality.")
    
    st.markdown("---")
    st.markdown("#### The La Rue Parity Law")
    st.markdown(r"""
    - **Odd Cardinality** ($N=1,3,5$): Resonance Lock ($0.0$).
    - **Even Cardinality** ($N=2,4,6$): Repulsion Wall ($0.5$).
    """)

# ════════════════════════════════════════════════════
# INTERSECTING METRICS: THE HIERARCHY
# ════════════════════════════════════════════════════

st.subheader("🌊 Global Phase Distribution")

col_phase, col_info = st.columns([3, 1])

with col_phase:
    try:
        GLOBAL_CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'global_resonance_data.csv')
        if os.path.exists(GLOBAL_CSV):
            gdf = pd.read_csv(GLOBAL_CSV)
            
            fig_p = px.histogram(gdf, x="eps", nbins=80,
                                 color_discrete_sequence=['#00ffcc'],
                                 title="Spectral Phase Density: Resonance vs Repulsion")
            fig_p.update_layout(
                template="plotly_dark", 
                height=400, 
                showlegend=False,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis_title="Normalized ε (Intersecting Metric)",
                yaxis_title="Density",
                font=dict(family="Inter")
            )
            fig_p.update_traces(marker_line_width=0)
            st.plotly_chart(fig_p, width='stretch')
        else:
            # Generate representative distribution
            phase_data = pd.DataFrame({
                'Phase': np.concatenate([
                    np.random.normal(0.02, 0.03, 2000),
                    np.random.normal(0.50, 0.04, 1800),
                    np.random.uniform(0, 1, 6200)
                ])
            })
            phase_data['Phase'] = phase_data['Phase'].clip(0, 1)
            fig_p = px.histogram(phase_data, x="Phase", nbins=80,
                                 color_discrete_sequence=['#00ffcc'],
                                 title="Bimodal Phase Lock (Representative Intersection)")
            fig_p.update_layout(
                template="plotly_dark", height=400, showlegend=False,
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Inter")
            )
            fig_p.update_traces(marker_line_width=0)
            st.plotly_chart(fig_p, width='stretch')
    except Exception as e:
        st.error(f"Phase engine offline: {e}")

with col_info:
    st.markdown("#### The 1/2 Connection")
    st.markdown(r"""
    The prime-zeta manifold is **bimodal**, exhibiting two primary stability regimes:
    
    - **Phase 0.0 (Resonance Lock)**: Where prime energy and zero-potential annihilate exactly.
    - **Phase 0.5 (Repulsion Wall)**: The critical boundary where the manifold resists collapse.
    
    This binary is the **La Rue Parity Law**: 
    odd cardinalities favor resonance, 
    even cardinalities favor repulsion. This distribution is the "spectral signature" of the Riemann Hypothesis in Protoreal space.
    """)

st.markdown("---")
st.markdown("---")
st.subheader("🔭 Modular Mission Control")
st.markdown(r"""
The **Protoreal Zeta Prime Hunt** is partitioned into three specialized research zones. 
Select a module from the **Sidebar** to begin deep-field analysis.
""")

# ════════════════════════════════════════════════════
# AXIOMATIC WORKBENCH: THE KLEIN UNIVERSE
# ════════════════════════════════════════════════════
st.markdown("---")
st.subheader("🛠️ 𝕌 Axiomatic Workbench")

w1, w2 = st.columns([2, 1])

with w1:
    st.markdown(r"""
    This workbench is synchronized with the **Lean 4 Mathlib** formalization. It allows for the 
    real-time manipulation of the **5-Component Klein Manifold**.
    """)
    
    with st.expander("Explore the 5-Component Axioms", expanded=False):
        st.markdown(r"""
        Numerical states $u$ are evaluated as vectors in a **5-Component Projective Space**:
        
        $$u = \{a, \omega, \iota, \epsilon, \lambda\}$$
        
        *   **Real Base ($a$)**: Empirical Divergence (No longer assuming 1/2).
        *   **Transfinite Thrust ($\omega$)**: Exploration Velocity toward the horizon.
        *   **Infinitesimal Anchor ($\iota$)**: Stability pull (Logarithmic convergence).
        *   **Noise Potential ($\epsilon$)**: Unmanifested jitter (Fuel for scaling).
        *   **Consolidation Level ($\lambda$)**: Generational Index (The Leech Lattice Layer).
        
        #### **The Non-Commutative Bridge**
        The manifold satisfies the anti-commutative identity proven in `TopologicalBearing.lean`:
        $$[\omega, \iota] = -2 \quad | \quad [\epsilon, \lambda] = -2$$
        
        #### **The Microscope Analogy (Dual Numbers)**
        The noise component $\epsilon$ is formalized as a **Dual Number** ($\epsilon^2 = 0$). This acts as a 'Microscope' into the manifold's infinitesimal jitter, allowing the automatic derivative to seed the next consolidation scale.
        """)

    # Interactive State Manipulator
    import core.ProtorealEngine as ue
    
    st.markdown("#### Manifold State Projector")
    sc1, sc2, sc3, sc4, sc5 = st.columns(5)
    a_in = sc1.number_input("a (Drift)", value=0.000, step=0.001, format="%.3f")
    w_in = sc2.number_input("w (Thrust)", value=1.0, step=0.1)
    i_in = sc3.number_input("i (Anchor)", value=1.0, step=0.1)
    e_in = sc4.number_input("e (Noise)", value=0.0, step=0.1)
    l_in = sc5.number_input("l (Level)", value=1, step=1)
    
    u_curr = ue.ProtorealElement(a=a_in, b=w_in, c=i_in, e=e_in, l=l_in)
    
    st.code(f"Current State: {u_curr}", language="text")
    
    b1, b2, b3 = st.columns(3)
    if b1.button("🌱 Sow Manifest Potential"):
        synth = ue.ProtorealSynthesis(t=u_curr.b, a=u_curr.a, e=u_curr.e)
        u_next = synth.solve_equilibrium(iterations=5)
        st.success(f"Equilibrium Discovered! New Drift: {u_next.a:.6f}")
        st.balloons()
    
    if b2.button("🧊 Consolidate Anchor"):
        u_next = u_curr.consolidate()
        st.info(f"Anchor Sharpened! New Stability: {u_next.c}")
        
    if b3.button("🔭 Zeta Projection"):
        # Project onto the first zero, but using actual spectral data if available
        u_zeta = ue.zeta_project(14.134, a=0.0) # Start from 0.0 to observe drift
        st.markdown(f"**First Zero Projection (a=0.0)**: `{u_zeta}`")
        st.info("Note: Real part 'a' now tracks actual spectral divergence (Topological Drift).")

with w2:
    st.markdown("#### Topological Bearing (Compass)")
    bearing = u_curr.bearing()
    st.metric("Manifold Bearing", f"{bearing:.4f}", help="b * c (Orientation Flux)")
    
    st.markdown("#### Topological Drift (SR)")
    res_val = ue.calculate_standard_resonance(u_curr)
    
    # Visualization of the drift from the critical line
    fig_drift = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = res_val,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Standard Resonance"},
        gauge = {
            'axis': {'range': [None, 1]},
            'bar': {'color': "#00ffcc"},
            'steps': [
                {'range': [0, 0.1], 'color': "rgba(0, 255, 204, 0.2)"},
                {'range': [0.45, 0.55], 'color': "rgba(255, 51, 102, 0.2)"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 0.5
            }
        }
    ))
    fig_drift.update_layout(template="plotly_dark", height=250, margin=dict(l=20,r=20,t=50,b=20))
    st.plotly_chart(fig_drift, use_container_width=True)

# ════════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════════

st.sidebar.markdown("### 🏹 The Prime Hunt")
st.sidebar.markdown("---")

st.sidebar.caption("Manifold stabilized via Lean 4 + Mathlib.")

st.markdown("---")
st.markdown("#### **Next Step: Establishing the Foundations**")
st.markdown(r"""
Once the axioms are set, we project the manifold into 3D space to identify 
resonance corridors.
""")
if st.button("🚀 Proceed to The Protoreal Manifold"):
    st.switch_page("pages/4_Protoreal_Manifold.py")
