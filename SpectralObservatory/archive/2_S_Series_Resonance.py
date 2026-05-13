import streamlit as st
import pandas as pd
import numpy as np
import os
import sys

# Ensure ZetaEngine can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import ZetaEngine as ze
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="S-Series | Adelic Resonance", layout="wide")

st.title("💎 S-Series: Gamma-Decelerated Adelic Resonance")

st.latex(r"""
S_{m,n} = \underbrace{(p_m \cdot (e \cdot \gamma)^{p_n})}_{\text{Decelerated Base}} - \text{Modulator} - \text{Drain}
""")

st.info("The S-Series uses the Euler-Mascheroni constant (γ) to decelerate prime-indexed growth, revealing high-precision spectral anchors.")

# --- Sidebar ---
st.sidebar.header("🔬 Engine Tuning")
m_range = st.sidebar.slider("m Range", 1, 100, (1, 50))
n_range = st.sidebar.slider("n Range", 1, 100, (1, 50))

@st.cache_data
def scan_s_series(m_r, n_r):
    results = []
    for m in range(m_r[0], m_r[1] + 1):
        for n in range(n_r[0], n_r[1] + 1):
            val, eps, norm, rank = ze.S_m_n(m, n)
            # Calculate Phase Angle for polar plot
            phase = (norm * 360) % 360
            results.append({'m': m, 'n': n, 'val': float(val), 'eps': eps, 'norm': norm, 'rank': rank, 'phase': phase})
    return pd.DataFrame(results)

df = scan_s_series(m_range, n_range)

# Metrics
st.sidebar.divider()
st.sidebar.metric("Avg Norm Divergence", f"{df['norm'].mean():.4f}")
st.sidebar.metric("Beating Random", f"{100*(df['norm'] < 0.25).mean():.1f}%")

# --- Dashboard ---
t1, t2, t3 = st.tabs(["🧊 3D Adelic Topology", "🎯 Polar Phase Lock", "🔍 Resonant Species"])

with t1:
    st.subheader("3D Adelic Surface")
    # Safety: log10(abs(x)) to handle negative values
    z_vals = df['val'].apply(lambda x: np.log10(abs(float(x))) if x != 0 else 0)
    
    fig_3d = go.Figure()
    fig_3d.add_trace(go.Scatter3d(
        x=df['m'], y=df['n'], z=z_vals,
        mode='markers',
        marker=dict(size=4, color=df['norm'], colorscale='RdBu_r', cmax=0.5, cmin=0, opacity=0.7, colorbar=dict(title="Norm Div")),
        text=[f"m={r['m']}, n={r['n']}<br>Rank={r['rank']}" for _, r in df.iterrows()],
        hoverinfo='text'
    ))
    fig_3d.update_layout(
        template="plotly_dark", 
        height=700, 
        margin=dict(l=0,r=0,b=0,t=0),
        scene=dict(xaxis_type='log', yaxis_type='log')
    )
    st.plotly_chart(fig_3d, width='stretch')

with t2:
    st.subheader("S-Series Spectral Lag")
    
    fig_polar = go.Figure()
    fig_polar.add_trace(go.Scatterpolar(
        r=df['norm'],
        theta=df['phase'],
        mode='markers',
        marker=dict(color=df['m'], colorscale='Viridis', size=5, opacity=0.6),
        name="Spectral Points"
    ))
    fig_polar.update_layout(
        template="plotly_dark",
        polar=dict(
            angularaxis=dict(
                tickvals=[0, 90, 180, 270],
                ticktext=['0', 'π/2', 'π', '3π/2'],
                direction="counterclockwise",
                rotation=0
            ),
            radialaxis=dict(range=[0, 0.5], showline=False, ticks='', showticklabels=False)
        )
    )
    st.plotly_chart(fig_polar, width='stretch')

with t3:
    st.subheader("Top Resonant Species (S-Series)")
    st.dataframe(df.sort_values('norm').head(50), width='stretch', hide_index=True)

st.markdown("---")
st.info("Visual Analytics v2.0 | Optimized for High-Precision Adelic Resonance")
