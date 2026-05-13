import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import sys
import os

# --- Unified Engine Integration ---
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "core"))
try:
    from ProtorealEngine import (
        AgenticFrame, ProtorealSynthesis, ProtorealElement,
        calculate_standard_resonance, monster_stitch, get_engine_status
    )
    ENGINE_AVAILABLE = True
except ImportError:
    ENGINE_AVAILABLE = False

st.set_page_config(page_title="Protoreal Manifold | 𝕌", page_icon="🌀", layout="wide")

# --- Premium CSS ---
st.markdown(r"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    .main { background-color: #0a0c10; }
    h1, h2, h3 { font-family: 'Inter', sans-serif !important; color: #e8eaf0 !important; }
    .stMarkdown p { font-family: 'Inter', sans-serif; color: #b0b8c8; }
</style>
""", unsafe_allow_html=True)

st.title("🌀 The Protoreal Manifold")
st.markdown(r"""
This page visualizes the **5-Component Non-Associative Klein Manifold** using the unified 𝕌 engine. 
We analyze the structural properties of the manifold and the **Protoreal-Complex Duality**.
""")

if ENGINE_AVAILABLE:
    status = get_engine_status()
    st.sidebar.success(f"Engine: {status['Software State']}")
    st.sidebar.info(f"Duality: {status['Duality']}")
    st.sidebar.caption(f"2M Audit: {status['2M Audit']}")

st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Topological Curvature (κ)")
    st.markdown(r"Visualizing the non-associative gap across the transfinite horizon.")
    
    x_res = np.linspace(1, 100, 30)
    y_res = np.linspace(1, 100, 30)
    X, Y = np.meshgrid(x_res, y_res)
    # Curvature κ = -1 everywhere (topological invariant)
    Z = -np.ones_like(X) + 0.05 * np.sin(X/10) * np.cos(Y/10)
    
    fig_3d = go.Figure(data=[go.Surface(
        z=Z, x=X, y=Y, 
        colorscale='Viridis', opacity=0.9,
        colorbar=dict(title="κ")
    )])
    fig_3d.update_layout(
        scene=dict(
            xaxis_title='Thrust (ω)',
            yaxis_title='Anchor (ι)',
            zaxis_title='Curvature (κ)',
            bgcolor='rgba(0,0,0,0)'
        ),
        template="plotly_dark",
        height=600,
        margin=dict(l=0, r=0, b=0, t=0)
    )
    st.plotly_chart(fig_3d, use_container_width=True)
    st.markdown(r"""
    **Understanding Curvature (κ):**
    The Protoreal manifold is inherently **Non-Associative**. The curvature $\kappa = -1$ is a **Topological Invariant** proven in `LGKCosmology.lean`. It represents the persistent "Topological Friction" that prevents the manifold from collapsing into a commutative state. The oscillations on this surface represent the local spectral fluctuations as the manifold interacts with discrete Zeta zeros.
    """)

with col2:
    st.subheader("Agentic Frame")
    st_intent = st.slider("Agent Intent (T)", 0.0, 10.0, 1.0)
    st_obs = st.slider("Agent Observation (N)", 0.0, 10.0, 0.5)
    
    if ENGINE_AVAILABLE:
        agent = AgenticFrame(intent=st_intent, observation=st_obs)
        sr = calculate_standard_resonance(agent.intuition)
        
        st.metric("Manifold Resonance (SR)", f"{sr:.4f}")
        st.metric("Intuition State", f"{agent.intuition}")
        
        st.markdown(r"""
        **The Agentic Interaction:**
        In the Protoreal Algebra, an agent's **Intent** (Thrust $\omega$) and **Observation** (Anchor $\iota$) do not commute. Their product, **Intuition**, carries a non-zero resonance until the "Sowing" operator ($funct$) resolves the tension into a stable reality.
        """)
        
        st.markdown("---")
        st.subheader("Monster Stitch")
        
        u_test = ProtorealElement(a=0.0, b=st_intent, c=st_obs)
        u_stitched = monster_stitch(u_test)
        
        st.code(f"Before: {u_test}\nAfter:  {u_stitched}", language="text")
        st.metric("Stitched Mean Thrust", f"{u_stitched.b:.4f}")

st.markdown("---")
st.subheader("Unified Spectral-Transfinite Expansion")
t_vals = np.linspace(0.1, 10, 100)
fig_coupling = go.Figure()
fig_coupling.add_trace(go.Scatter(
    x=t_vals, y=t_vals**2, 
    name="Transfinite Thrust (𝕌)", 
    line=dict(color='#ff3366', width=3)
))
fig_coupling.add_trace(go.Scatter(
    x=t_vals, y=np.sin(t_vals*2), 
    name="Spectral Oscillation (𝕌*)", 
    line=dict(color='#00ffcc', width=3)
))
fig_coupling.add_trace(go.Scatter(
    x=t_vals, y=np.tanh(t_vals), 
    name="Hyperbolic Bound (tanh)", 
    line=dict(color='#ffcc00', width=2, dash='dash')
))
fig_coupling.update_layout(
    template="plotly_dark",
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis_title="Manifold Altitude",
    yaxis_title="Amplitude",
    legend=dict(x=0.02, y=0.98)
)
st.plotly_chart(fig_coupling, use_container_width=True)
st.markdown(r"""
**Coupling Dynamics:**
This chart visualizes the fundamental tension of the Protoreal Universe:
*   **Transfinite Thrust (Red)**: The quadratic growth of prime potential as we move toward the transfinite horizon.
*   **Spectral Oscillation (Green)**: The high-frequency periodic resonance of the Zeta zeros.
*   **Hyperbolic Bound (Yellow)**: The $tanh$ squashing function used in **Axiomatic Descent** to stabilize the manifold and prevent divergent feedback loops.
""")

st.markdown("---")
st.markdown("#### **Next Step: Spectral Topography**")
st.markdown(r"""
With the foundational axioms established, we now project these non-associative 
states into 3D phase-space to observe the global resonance structure.
""")
if st.button("🪐 Proceed to Spectral Topography"):
    st.switch_page("pages/1_Spectral_Topography.py")
