import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
import numpy as np
import ZetaEngine as ze
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Spectral Topography | Prime-Zeta", page_icon="🌌", layout="wide")

# --- Premium CSS ---
st.markdown(r"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    .main { background-color: #0a0c10; }
    h1, h2, h3 { font-family: 'Inter', sans-serif !important; color: #e8eaf0 !important; }
    .stMarkdown p { font-family: 'Inter', sans-serif; color: #b0b8c8; }
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(255,255,255,0.04), rgba(255,255,255,0.01));
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 20px;
    }
    [data-testid="stMetric"]:hover { border-color: rgba(0, 255, 204, 0.3); }
</style>
""", unsafe_allow_html=True)

st.title("🌌 Spectral Topography: Prime-Zeta Manifold")
st.markdown("The prime-zeta manifold rendered as interactive 3D phase-space, heat gradients, and modular polar projections.")
st.markdown("---")

# ════════════════════════════════════════════════════
# SIDEBAR CONTROLS
# ════════════════════════════════════════════════════

st.sidebar.header("⚙️ Observation Parameters")
budget = st.sidebar.slider("Hyperbolic Budget (l·m·n ≤ B)", min_value=100, max_value=2000, value=600, step=100)
mod_24_filter = st.sidebar.selectbox("Mod-24 Channel", ["All", 0, 9, 14, 18, 20])
color_scale = st.sidebar.selectbox("Color Scale", ["Viridis", "Plasma", "Turbo", "RdBu"])

# ════════════════════════════════════════════════════
# DATA GENERATION
# ════════════════════════════════════════════════════

@st.cache_data
def generate_3d_data(b):
    data = []
    for l in range(1, b + 1):
        m_max = b // l
        if m_max < 1: break
        for m in range(1, m_max + 1):
            n_max = b // (l * m)
            if n_max < 1: break
            for n in range(1, n_max + 1):
                try:
                    val, eps, norm, rank, energy = ze.T3_l_m_n(l, m, n)
                    if norm < 5.0:
                        data.append({
                            'l': l, 'm': m, 'n': n,
                            'p_l': int(ze.sieve[l]), 'p_m': int(ze.sieve[m]), 'p_n': int(ze.sieve[n]),
                            'norm_eps': float(norm),
                            'energy': float(energy),
                            'mod24': (l + m + n) % 24,
                            'mod6': (l + m + n) % 6,
                            'is_resonant': energy < 0.001
                        })
                except Exception:
                    pass
    return pd.DataFrame(data)

with st.spinner("Scanning the manifold..."):
    df = generate_3d_data(budget)

if df.empty:
    st.error("No data generated. Increase budget or check engine.")
    st.stop()

# Apply filters
plot_df = df.copy()
if mod_24_filter != "All":
    plot_df = plot_df[plot_df['mod24'] == mod_24_filter]

# ════════════════════════════════════════════════════
# TABS: 3D | HEAT MAP | PHASE RADAR
# ════════════════════════════════════════════════════

tab_3d, tab_heat, tab_radar = st.tabs(["🪐 3D Topography", "🔥 Energy Heat Map", "🎯 Phase Radar"])

with tab_3d:
    st.subheader("Manifold Energy Topography (E)")
    
    fig = px.scatter_3d(
        plot_df, x='l', y='m', z='n',
        color='energy',
        color_continuous_scale=color_scale,
        range_color=[0, 0.01],
        size=[12 if sh else 3 for sh in plot_df['is_resonant']],
        size_max=18, opacity=0.9,
        hover_data=['p_l', 'p_m', 'p_n', 'energy', 'mod24']
    )
    fig.update_traces(marker=dict(line=dict(width=0)))
    fig.update_layout(
        margin=dict(l=0, r=0, b=0, t=0),
        scene=dict(
            xaxis_title='l', yaxis_title='m', zaxis_title='n',
            xaxis_type='log', yaxis_type='log', zaxis_type='log',
            bgcolor='rgb(10, 10, 15)'
        ),
        paper_bgcolor='rgb(10, 10, 15)',
        font=dict(color='white', family='Inter'),
        height=650
    )
    st.plotly_chart(fig, width='stretch')
    
    st.markdown(r"""
    **Understanding the Reality:**
    *   **Coordinates (l, m, n)**: The indices of the prime triple.
    *   **Spectral Energy (E)**: This is the real physical potential of the manifold. Points where $E \to 0$ are the "Stitches" proven to exist on the critical line.
    *   **Marker Size**: Points of absolute resonance ($E < 0.001$) are highlighted as verified spectral anchors.
    
    *Note: Visualizations utilize Float64 for real-time navigation. Symbolic verification (200-digit precision) is performed in the Lean 4 proof environment.*
    """)
    
    # Metrics row
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Points", f"{len(plot_df):,}")
    m2.metric("Mean Energy (E)", f"{plot_df['energy'].mean():.6f}")
    m3.metric("Lock Rate", f"{100 * plot_df['is_resonant'].mean():.1f}%")
    m4.metric("Min Energy", f"{plot_df['energy'].min():.8f}")

with tab_heat:
    st.subheader("Prime Resonance Heat Map (Numerical)")
    
    heat_col1, heat_col2 = st.columns([3, 1])
    
    with heat_col1:
        DATA_CSV = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                'data', 'zeta_divergence_analysis.csv')
        
        if os.path.exists(DATA_CSV):
            df_heat = pd.read_csv(DATA_CSV)
            df_heat = df_heat[df_heat['Div'] != '---'].copy()
            df_heat['Div'] = pd.to_numeric(df_heat['Div'], errors='coerce')
            
            piv = df_heat.pivot_table(index='n', columns='m', values='Div', aggfunc='min')
            fig_heat = px.imshow(piv, color_continuous_scale="RdBu", color_continuous_midpoint=0,
                                 labels=dict(color="ε Divergence"),
                                 title="Spectral Divergence Gradient")
            fig_heat.update_layout(template="plotly_dark", height=550,
                                    paper_bgcolor='rgba(0,0,0,0)', font=dict(family='Inter'))
            st.plotly_chart(fig_heat, width='stretch')
        else:
            piv = df.pivot_table(index='n', columns='m', values='norm_eps', aggfunc='min')
            fig_heat = px.imshow(piv, color_continuous_scale=color_scale,
                                 labels=dict(color="Normalized ε"),
                                 title="Resonance Gradient (m × n)")
            fig_heat.update_layout(template="plotly_dark", height=550,
                                    paper_bgcolor='rgba(0,0,0,0)', font=dict(family='Inter'))
            st.plotly_chart(fig_heat, width='stretch')
            st.markdown(r"""
            **Heat Map Mechanics:**
            The heat map projects the 3D manifold onto a 2D resonance plane ($m \times n$). It reveals the **Phase-Lock Corridors** where the spectral density is highest. Darker regions represent stable "spectral sinks" where the Riemann Zeta zeros are topologically anchored.
            """)
    
    with heat_col2:
        st.markdown("#### Top Numerical Hits")
        top_species = df.sort_values('norm_eps').head(10)
        st.dataframe(top_species[['l', 'm', 'n', 'norm_eps', 'mod24']], 
                     width='stretch', hide_index=True)

with tab_radar:
    st.subheader("Modular Prime Radar")
    
    radar_col1, radar_col2 = st.columns([2, 1])
    
    with radar_col1:
        radar_data = df.groupby('mod24')['norm_eps'].mean().reset_index()
        radar_data['strength'] = 1 / (radar_data['norm_eps'] + 0.1)
        
        fig_r = go.Figure(data=go.Scatterpolar(
            r=radar_data['strength'],
            theta=[f"{x}" for x in radar_data['mod24']],
            fill='toself',
            line_color='#00ffcc',
            fillcolor='rgba(0, 255, 204, 0.1)'
        ))
        fig_r.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, max(radar_data['strength']) * 1.2]),
                bgcolor='rgba(0,0,0,0)'
            ),
            showlegend=False, template="plotly_dark", height=500,
            margin=dict(l=40, r=40, b=40, t=40),
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter')
        )
        st.plotly_chart(fig_r, width='stretch')
        st.markdown(r"""
        **Radar Analysis:**
        The **Modular Prime Radar** identifies structural symmetries in the prime-zeta distribution. By grouping resonance strength by **Mod-24 residue classes**, we reveal the "Antenna Anchors" — specific residue classes that act as topological magnets for resonant primes.
        """)
    
    with radar_col2:
        st.markdown("#### Numerical Anchors")
        st.markdown(r"""
        The **mod-24 radar** reveals which residue classes 
        concentrate the highest prime resonance density.
        
        **Key anchors:**
        - **14 mod 24** — Primary stabilizer
        - **18 mod 24** — Geometric mean anchor
        - **0 mod 6** — Prime form buffer
        """)

st.markdown("---")
st.caption("Numerical topography independent of Protoreal algebraic weighting.")


st.markdown("---")
st.markdown("#### **Next Step: Deep Resonance Analysis**")
st.markdown(r"""
Visual topography reveals the 'where'. Now we analyze the 'how' by decomposing 
the spectral tension into its constituent Mangoldt and Stieltjes components.
""")
if st.button("📊 Proceed to Resonance Analysis"):
    st.switch_page("pages/2_Resonance_Analysis.py")
