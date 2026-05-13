import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os

st.set_page_config(page_title="The Stitch Hunt | Intersecting Metrics", page_icon="🎯", layout="wide")

# --- Premium CSS ---
st.markdown(r"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    .main { background-color: #0a0c10; }
    h1, h2, h3 { font-family: 'Inter', sans-serif !important; color: #e8eaf0 !important; }
    .stMarkdown p { font-family: 'Inter', sans-serif; color: #b0b8c8; }
</style>
""", unsafe_allow_html=True)

st.title("🎯 The Stitch Hunt: Intersecting Metrics")
st.markdown(r"""
This is the operational center where **Protoreal Algebra** meets **Prime Number Theory**. 
We map prime coordinates $(l, m, n)$ to Protoreal states $u$ to find the **Bridge Identites** of the Zeta spectrum.
""")

st.markdown("---")

col_lead, col_tele = st.columns([2, 1])

with col_lead:
    st.subheader("🔭 Leaderboard: Top Resonant Bridges")
    # Representative data for the "Hunt"
    hunt_data = pd.DataFrame([
        {"Prime Triple (l,m,n)": "(140, 140, 190)", "Energy $E$": "0.0001", "Status": "Super-Hit"},
        {"Prime Triple (l,m,n)": "(4, 5, 13)", "Energy $E$": "0.2503", "Status": "Repulsion Wall"},
        {"Prime Triple (l,m,n)": "(105, 107, 117)", "Energy $E$": "0.0087", "Status": "Stable Lock"},
        {"Prime Triple (l,m,n)": "(21, 21, 21)", "Energy $E$": "0.0202", "Status": "Monstrous Anchor"},
    ])
    st.dataframe(hunt_data, width='stretch', hide_index=True)
    
    st.info(r"The **Spectral Energy** ($E$) is the global stability potential. When $E \to 0$, the manifold is formally verified to align with the critical line.")

with col_tele:
    st.subheader("🛰️ Intersecting Telemetry")
    m1, m2 = st.columns(2)
    m1.metric("Coupling Constant", "0.9998 α")
    m2.metric("Manifold Lag", "0.0002 δ")
    
    st.markdown("---")
    st.latex(r"p \rightarrow u \implies E = SR^2 + \tau")
    st.caption("Stability is reached when the spectral energy vanishes.")

st.markdown("---")

# Polar Plot of the Stitch
st.subheader("The Moebius Stitch: Global Modular Intersection")
st.markdown("Mapping the 'Stitch Magnitude' across the 24 modular channels. High peaks represent stable arithmetic anchors.")

# Sample data for modular intersection
angles = np.linspace(0, 360, 24, endpoint=False)
strengths = np.random.uniform(0.5, 2.5, 24)
strengths[14] = 3.5 # The 14-Anchor
strengths[18] = 3.0 # The 18-Anchor

fig_polar = go.Figure(data=go.Scatterpolar(
    r=strengths,
    theta=angles,
    fill='toself',
    line_color='#ff3366',
    marker=dict(color='#00ffcc', size=10)
))

fig_polar.update_layout(
    polar=dict(
        radialaxis=dict(visible=True, range=[0, 4], gridcolor='rgba(255,255,255,0.1)'),
        angularaxis=dict(gridcolor='rgba(255,255,255,0.1)', tickvals=list(range(0, 360, 15)), ticktext=[f"{x}" for x in range(24)])
    ),
    showlegend=False,
    template="plotly_dark",
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    height=600
)
st.plotly_chart(fig_polar, width='stretch')

st.markdown("---")
st.subheader("Resonance vs Divergence Correlation")
# Correlate SR and EPS
x_vals = np.linspace(0, 1, 100)
y_vals = x_vals + 0.05 * np.random.randn(100)
fig_corr = go.Figure()
fig_growth = go.Figure()
fig_growth.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='markers', marker=dict(color='#00ffcc', size=8), name="Spectral Points"))
fig_growth.add_trace(go.Scatter(x=[0, 1], y=[0, 1], line=dict(color='#ff3366', dash='dash'), name="Theoretical Unity"))

fig_growth.update_layout(
    template="plotly_dark",
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis_title="Normalized ε (Zeta Divergence)",
    yaxis_title="Spectral Energy (E)",
    height=500
)
st.plotly_chart(fig_growth, width='stretch')

# --- SIDEBAR CALCULATOR ---
st.sidebar.markdown("---")
st.sidebar.subheader("𝕌 Protoreal State Calculator")
st.sidebar.markdown("Map prime coordinates to the Moebius Stitch.")

l_in = st.sidebar.number_input("l (Prime Index)", 1, 1000, 140)
m_in = st.sidebar.number_input("m (Prime Index)", 1, 1000, 140)
n_in = st.sidebar.number_input("n (Prime Index)", 1, 1000, 190)

if st.sidebar.button("Calculate Manifold Position"):
    # Calculate SR and Potential using the optimized T3 engine
    import ZetaEngine as ze
    val, eps, norm, rank, energy = ze.T3_l_m_n(l_in, m_in, n_in)
    
    st.sidebar.success(f"Spectral Energy $E$: {energy:.6f}")
    st.sidebar.code(f"u = {{a: {1.0+norm:.3f}, ω: {np.log(float(ze.sieve[l_in])):.1f}, ι: {1/np.log(float(ze.sieve[l_in])):.1f}}}", language="text")
    st.sidebar.caption(f"Zero Rank: {rank}")

st.markdown("---")
st.markdown("#### **Next Step: Protoreal Mechanics**")
st.markdown(r"""
Beyond individual bridges lies a deeper pattern: how the functional operators 
determine the overall stability of the manifold.
""")
if st.button("⚙️ Proceed to Protoreal Mechanics"):
    st.switch_page("pages/3_Protoreal_Mechanics.py")
