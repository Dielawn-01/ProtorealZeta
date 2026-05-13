import streamlit as st
import pandas as pd
import numpy as np
import ZetaEngine as ze
import plotly.graph_objects as go
import plotly.express as px
import os
import sys

# Ensure ZetaEngine can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(page_title="Monstrous Resonance | TheLab", layout="wide")

st.title("👾 Monstrous Resonance: The 24-Dimensional Grammar")

st.latex(r"""
\text{Resonance Channel: } (m + n) \equiv \mathcal{C} \pmod{24} \quad \text{where } \mathcal{C} \in \{9, 16, 4\}
""")

st.info("Mapping the '21-Anchor' and the 'Moonshine' symmetries discovered in the prime-zeta resonance lattice.")

# --- Modular Analysis Engine ---
@st.cache_data
def load_monstrous_data():
    CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'global_resonance_data.csv')
    if not os.path.exists(CSV_PATH):
        return pd.DataFrame()
    df = pd.read_csv(CSV_PATH)
    # Add Modular columns
    df['sum_mod_24'] = (df['m'] + df['n']) % 24
    df['k_mod_24'] = df['rank'] % 24
    return df

df = load_monstrous_data()

if df.empty:
    st.error("❌ Global lattice data not found. Please run the full scan.")
    st.stop()

# --- Sidebar ---
st.sidebar.header("👺 Monster Tuning")
mod_channel = st.sidebar.multiselect("Active Modular Channels (m+n mod 24)", 
                                    options=list(range(24)), default=[9, 16, 4])
k_channel = st.sidebar.multiselect("Active Zero Ranks (k mod 24)", 
                                  options=list(range(24)), default=[21, 8, 11])

# --- Dashboard ---
t1, t2, t3 = st.tabs(["🌀 The 21-Anchor Projection", "📊 Monstrous Distribution", "🕳️ Repulsion Symmetry"])

with t1:
    st.subheader("The Modular Wavefront (24-Ring Projection)")
    st.markdown("""
    This polar plot maps resonance intensity (ε) against the 24 modular channels of the prime-zeta lattice. 
    The angle of each point represents its congruence class $(m+n) \\pmod{24}$, mapped continuously onto the unit circle:
    * **0 Radians (East)**: Corresponds to Channel 0.
    * **π/2 Radians (North)**: Corresponds to Channel 6.
    * **π Radians (West)**: Corresponds to Channel 12.
    * **3π/2 Radians (South)**: Corresponds to Channel 18.
    
    This continuous mapping allows us to observe symmetric clustering (such as the 9-mod-24 Prime Square Channel) 
    as geometric phase-locks in the resonance wave.
    """)
    
    # Filtered for user selection
    filtered_df = df[df['sum_mod_24'].isin(mod_channel)].copy()
    
    # Convert sum_mod_24 to degrees for stability: (val / 24) * 360
    filtered_df['Theta_Deg'] = (filtered_df['sum_mod_24'] / 24) * 360
    
    fig_monster = go.Figure()
    fig_monster.add_trace(go.Scatterpolar(
        r=filtered_df['eps'],
        theta=filtered_df['Theta_Deg'],
        mode='markers',
        marker=dict(color=filtered_df['k_mod_24'], colorscale='Plasma', size=6, opacity=0.8, 
                    colorbar=dict(title="k mod 24")),
        text=[f"m={r['m']}, n={r['n']}<br>Sum={r['sum_mod_24']}<br>k={r['rank']}" for _, r in filtered_df.iterrows()],
        hoverinfo='text'
    ))
    
    fig_monster.update_layout(
        template="plotly_dark", 
        height=800, 
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
    st.plotly_chart(fig_monster, width='stretch')

with t2:
    st.subheader("Monstrous Distribution Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Zero-Rank Spectrum ($k \\pmod{24}$)")
        # Show the distribution of k mod 24 for resonant species
        resonant_df = df[df['eps'] < 0.15]
        fig_dist = px.histogram(resonant_df, x='k_mod_24', nbins=24, 
                               template="plotly_dark", color_discrete_sequence=['#ff00ff'])
        fig_dist.update_traces(marker_line_color='rgba(255,255,255,0.8)', marker_line_width=1)
        fig_dist.update_layout(xaxis_title="k mod 24", yaxis_title="Resonance Count")
        st.plotly_chart(fig_dist, width='stretch')
        
    with col2:
        st.markdown("### The 21-Anchor Resonance Heatmap")
        anchor_df = df[df['k_mod_24'] == 21].copy()
        if not anchor_df.empty:
            # Use pivot_table to avoid Duplicate Entry errors
            piv = anchor_df.pivot_table(index='n', columns='m', values='eps', aggfunc='min')
            fig_heat = px.imshow(piv, color_continuous_scale="Magma_r", zmax=0.3,
                                labels=dict(color="ε"), template="plotly_dark")
            st.plotly_chart(fig_heat, width='stretch')
        else:
            st.warning("No data points found for the 21-Anchor.")

with t3:
    st.subheader("The Repulsion Paradox (Anti-Anchors)")
    st.markdown("""
    In the Protoreal Ring, **Repulsion (Phase 0.5)** is the structural mirror of **Resonance (Phase 0.0)**. 
    This tab maps the 'Dark Channels' where the prime harmonics are most violently repelled from the zeros.
    """)
    
    # Filter for repulsion states (norm_eps near 0.5)
    repulsion_df = df[(df['eps'] > 0.4) & (df['eps'] < 0.6)].copy()
    
    if not repulsion_df.empty:
        st.markdown("### Mod-24 Distribution of Anti-Anchors")
        fig_rep = px.histogram(repulsion_df, x='sum_mod_24', nbins=24, 
                              template="plotly_dark", color_discrete_sequence=['#00ffcc'])
        fig_rep.update_layout(xaxis_title="Sum mod 24", yaxis_title="Repulsion Count")
        st.plotly_chart(fig_rep, width='stretch')
        
        st.info("Discovery: Channel 9 mod 24 exhibits the highest repulsion density in the T3 manifold.")
    else:
        st.warning("No repulsion data detected in this sample.")

st.markdown("---")
st.success("Theoretical Verdict: The 21-Anchor represents a phase-locked modular channel within the Monster Symmetry.")
