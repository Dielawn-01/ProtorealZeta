import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
import numpy as np
import ZetaEngine as ze
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Resonance Analysis | 𝕌", page_icon="📊", layout="wide")

# --- Premium CSS ---
st.markdown(r"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400&display=swap');
    .main { background-color: #0a0c10; }
    h1, h2, h3 { font-family: 'Inter', sans-serif !important; color: #e8eaf0 !important; }
    .stMarkdown p { font-family: 'Inter', sans-serif; color: #b0b8c8; }
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(255,255,255,0.04), rgba(255,255,255,0.01));
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px; padding: 20px;
    }
    [data-testid="stMetric"]:hover { border-color: rgba(255, 75, 75, 0.3); }
</style>
""", unsafe_allow_html=True)

st.title("📊 Resonance Analysis")
st.markdown("Deep inspection of the prime-zeta divergence landscape. Tables, metrics, and spectral decomposition.")
st.markdown("---")

# ════════════════════════════════════════════════════
# DATA LOADING
# ════════════════════════════════════════════════════

@st.cache_data
def load_divergence_data():
    CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                            'data', 'zeta_divergence_analysis.csv')
    if not os.path.exists(CSV_PATH):
        return pd.DataFrame()
    
    df = pd.read_csv(CSV_PATH)
    df = df[df['Div'] != '---'].copy()
    
    numeric_cols = ['k', 'Div', 'Dylon', 'Base', 'Modulator', 'Drain', 'Λ Ratio',
                    'Nearest Zero', 'Resonance', 'λ_P(k)', 'λ_P(m*n)', 'Normalized_Div']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

df = load_divergence_data()

if df.empty:
    st.warning("No divergence data found. Run the analysis scripts in `TheLab/scripts/` to generate datasets.")
    st.stop()

# ════════════════════════════════════════════════════
# SIDEBAR CONTROLS
# ════════════════════════════════════════════════════

st.sidebar.header("🔧 Data Controls")
sort_col = st.sidebar.selectbox("Sort By", options=['m', 'n', 'Div', 'Dylon', 'Resonance', 'Normalized_Div'],
                                 index=0)
sort_order = st.sidebar.radio("Order", ["Ascending", "Descending"])
show_only_resonant = st.sidebar.checkbox("Show only resonant (ε < 0.1)", False)

if show_only_resonant and 'Normalized_Div' in df.columns:
    df = df[df['Normalized_Div'].abs() < 0.1]

# ════════════════════════════════════════════════════
# SUMMARY METRICS
# ════════════════════════════════════════════════════

m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Total Points", f"{len(df):,}")
m2.metric("Mean |ε|", f"{df['Div'].abs().mean():.4f}" if 'Div' in df.columns else "—")
m3.metric("Min |ε|", f"{df['Div'].abs().min():.6f}" if 'Div' in df.columns else "—")
if 'Resonance' in df.columns:
    m4.metric("Resonance Lock", f"{(df['Resonance'] < 0.1).sum()}")
    m5.metric("Hit Rate", f"{100 * (df['Resonance'] < 0.1).mean():.1f}%")
else:
    m4.metric("Columns", f"{len(df.columns)}")
    m5.metric("Range", f"m∈[{int(df['m'].min())},{int(df['m'].max())}]")

st.markdown("---")

# ════════════════════════════════════════════════════
# TABS: TABLE | GRADIENT | ANTENNA
# ════════════════════════════════════════════════════

tab_table, tab_gradient, tab_antenna = st.tabs(["📋 Data Table", "🔥 Divergence Gradient", "📡 Antenna Decomposition"])

with tab_table:
    st.subheader("Dataset Inspector")
    display_df = df.sort_values(sort_col, ascending=(sort_order == "Ascending"))
    st.dataframe(display_df, width='stretch', hide_index=True, height=600)

with tab_gradient:
    st.subheader("Spectral Divergence Gradient")
    
    if 'Div' in df.columns:
        piv = df.pivot_table(index='n', columns='m', values='Div', aggfunc='min')
        fig_heat = px.imshow(piv, color_continuous_scale="RdBu", color_continuous_midpoint=0,
                             labels=dict(color="ε Divergence"))
        fig_heat.update_layout(template="plotly_dark", height=600,
                                paper_bgcolor='rgba(0,0,0,0)', font=dict(family='Inter'))
        st.plotly_chart(fig_heat, width='stretch')
    else:
        st.info("Divergence column not available in this dataset.")

with tab_antenna:
    st.subheader("Prime Antenna Decomposition")
    
    st.latex(r"""
    D_{m,n} = \underbrace{p_m \cdot e \cdot p_n}_{\text{Mangoldt Base}} 
    - \underbrace{\frac{\sqrt{m \cdot n} \cdot e^{\frac{p_n - p_m}{2}}}{4\pi}}_{\text{Modulator}} 
    - \underbrace{\sqrt{\frac{(p_n - n)^2 + (p_m - m)^2}{2\pi}} \cdot P(\Delta \Lambda) \cdot \ln(1 + |n^2 - m^2|)}_{\text{Stieltjes Drain}}
    """)
    st.markdown(r"""
    **Antenna Components:**
    *   **Mangoldt Base**: The raw transfinite product ($\pi(l)\pi(m)\pi(n)$).
    *   **Modulator**: The local phase correction aligned with the index drift.
    *   **Stieltjes Drain**: The altitude-scaled logarithmic correction using Stieltjes Phase Polynomials $P(\Delta \Lambda)$.
    
    *   $\| \mathbf{p} - \mathbf{n} \|^2 = (p_n - n)^2 + (p_m - m)^2$ (Euclidean Index Drift)
    *   $P(\Delta \Lambda) = \gamma_0 + \gamma_1 \Delta \Lambda + \frac{\gamma_2}{2} \Delta \Lambda^2 \dots$ (Stieltjes Phase Polynomial)
    *   $\Delta \Lambda = |\ln(p_n / p_m)|$ (Mangoldt Divergence)
    """)
    
    if all(c in df.columns for c in ['Base', 'Modulator', 'Drain']):
        # Component breakdown
        comp_col1, comp_col2 = st.columns([2, 1])
        
        with comp_col1:
            fig_comp = go.Figure()
            
            sample = df.head(200)
            x_idx = range(len(sample))
            
            fig_comp.add_trace(go.Scatter(
                x=list(x_idx), y=sample['Base'].apply(lambda x: np.log10(abs(x)) if x != 0 else 0),
                name="log₁₀|Base|", line=dict(color='#00ffcc', width=2)))
            fig_comp.add_trace(go.Scatter(
                x=list(x_idx), y=sample['Modulator'].apply(lambda x: np.log10(abs(x)) if x != 0 else 0),
                name="log₁₀|Modulator|", line=dict(color='#ff4b4b', width=2)))
            fig_comp.add_trace(go.Scatter(
                x=list(x_idx), y=sample['Drain'].apply(lambda x: np.log10(abs(x)) if x != 0 else 0),
                name="log₁₀|Drain|", line=dict(color='#feca57', width=2)))
            
            fig_comp.update_layout(
                template="plotly_dark", height=450,
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis_title="Sample Index", yaxis_title="log₁₀|Component|",
                legend=dict(orientation="h", yanchor="bottom", y=1.02),
                font=dict(family='Inter')
            )
            st.plotly_chart(fig_comp, width='stretch')
            st.markdown(r"""
            **Component Analysis:**
            The decomposition chart reveals the relative scales of the antenna components:
            *   **Mangoldt Base (Green)**: The raw transfinite product ($\pi(l)\pi(m)\pi(n)$). This is the "thrust" of the prime triple toward the spectral horizon.
            *   **Stieltjes Correction (Red)**: The local phase modulator that aligns the prime product with the nearest zero.
            *   **Drain (Yellow)**: The logarithmic altitude adjustment that accounts for the density of zeros as $t \to \infty$.
            """)
        
        with comp_col2:
            st.markdown("#### Component Ranges")
            st.dataframe(df[['Base', 'Modulator', 'Drain']].describe().round(4), 
                         width='stretch')
    else:
        st.info("Antenna components not available in this dataset.")

# ════════════════════════════════════════════════════
# POINT LOOKUP
# ════════════════════════════════════════════════════

st.markdown("---")
st.subheader("🎯 Coordinate Lookup")

lk_col1, lk_col2 = st.columns([1, 3])

with lk_col1:
    m_sel = st.number_input("m", min_value=1, max_value=int(df['m'].max()), value=1)
    n_sel = st.number_input("n", min_value=1, max_value=int(df['n'].max()), value=2)

with lk_col2:
    row_data = df[(df['m'] == m_sel) & (df['n'] == n_sel)]
    if not row_data.empty:
        row = row_data.iloc[0]
        c1, c2, c3 = st.columns(3)
        c1.metric("p_m", f"{int(row['p_m'])}" if 'p_m' in row else "—")
        c2.metric("p_n", f"{int(row['p_n'])}" if 'p_n' in row else "—")
        c3.metric("Divergence (ε)", f"{row['Div']:.6f}" if 'Div' in row else "—")
        
        if 'Dylon' in row:
            c4, c5, c6 = st.columns(3)
            c4.metric("Antenna Output", f"{row['Dylon']:.2e}")
            c5.metric("Nearest Zero", f"γ_{int(row['k'])}" if 'k' in row else "—")
            c6.metric("Resonance", f"{row['Resonance']:.4f}" if 'Resonance' in row else "—")
    else:
        st.caption(f"Coordinate ({m_sel}, {n_sel}) not in dataset range.")

st.markdown("---")
st.markdown("#### **Next Step: The Stitch Hunt**")
st.markdown(r"""
Now that we can decompose resonance, let’s apply these metrics to hunt for specific 
"Stitch" coordinates in the spectrum.
""")
if st.button("🌀 Proceed to The Stitch Hunt"):
    st.switch_page("pages/5_The_Stitch_Hunt.py")
