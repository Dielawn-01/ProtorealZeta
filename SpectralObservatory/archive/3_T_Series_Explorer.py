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

st.set_page_config(page_title="T-Series | Resonance Shells", layout="wide")

st.title("🌌 T-Series ($T_{m,n}$) Resonance Explorer")

st.latex(r"""
T_{m,n}(m, n, k) = \underbrace{(p_m \cdot e^k \cdot p_n)}_{\text{Resonance}} - \underbrace{\frac{p_m \cdot e^{-p_n}}{4\pi}}_{\text{Bound}}
""")

# --- Data Loading ---
@st.cache_data
def load_res_data():
    CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'resonance_data.csv')
    if not os.path.exists(CSV_PATH):
        return pd.DataFrame()
    return pd.read_csv(CSV_PATH)

df = load_res_data()

if df.empty:
    st.error("❌ No resonance data found. Run the scan in workbook0.")
    st.stop()

# --- Sidebar ---
st.sidebar.header("🔬 Tier Selection")
k_sel = st.sidebar.select_slider("Hyperoperational Tier (k)", options=[1, 2, 3], value=1)

sub_df = df[df['k'] == k_sel].copy()
sub_df['sum_mod_24'] = (sub_df['m'] + sub_df['n']) % 24

# --- Dashboard ---
t1, t2, t3 = st.tabs(["🧊 3D Resonance Shell", "📉 Modular DNA", "📊 Resonant Lattice"])

with t1:
    st.subheader(f"3D Shell Topology (k={k_sel})")
    # Using the ZetaEngine's native shell plotter
    fig_shell = ze.plot_resonance_shell(df, k_tier=k_sel)
    if fig_shell:
        st.plotly_chart(fig_shell, width='stretch')

with t2:
    st.subheader("Modular Resonance DNA (Mod 24)")
    st.markdown("This histogram shows which $(m+n) \pmod{24}$ channels carry the highest resonance density.")
    
    # Filter for resonant species to show the "DNA"
    resonant_df = sub_df[sub_df['eps'] < 0.15]
    fig_mod = px.histogram(resonant_df, x='sum_mod_24', nbins=24, 
                           template="plotly_dark", color_discrete_sequence=['#00ffcc'])
    fig_mod.update_traces(marker_line_color='rgba(255,255,255,0.8)', marker_line_width=1)
    fig_mod.update_layout(xaxis_title="(m + n) mod 24", yaxis_title="Resonance Density")
    st.plotly_chart(fig_mod, width='stretch')

with t3:
    st.subheader("🔍 Resonant Species Explorer")
    st.dataframe(sub_df.sort_values('eps').head(100), width='stretch', hide_index=True)

st.markdown("---")
st.info("The T-Series remains the primary engine for high-density lattice mapping.")
