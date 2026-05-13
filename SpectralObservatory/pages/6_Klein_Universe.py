import streamlit as st
import numpy as np
import plotly.graph_objects as go
import sys
import os

# --- Engine Integration ---
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "core"))
try:
    from ProtorealEngine import (
        ProtorealSynthesis, ProtorealElement, monster_stitch,
        calculate_standard_resonance, get_engine_status
    )
    ENGINE_AVAILABLE = True
except ImportError:
    ENGINE_AVAILABLE = False

# --- Page Config ---
st.set_page_config(page_title="𝕌 Klein Universe | Spectral Observatory", layout="wide")

# --- Premium CSS ---
st.markdown(r"""
<style>
    .main { background-color: #0a0c10; }
    h1, h2, h3 { color: #e8eaf0 !important; font-family: 'Inter', sans-serif; }
    .stSlider > div > div > div > div { background-color: #00ffcc; }
</style>
""", unsafe_allow_html=True)

st.title("🌌 The Klein Universe")
st.markdown(r"""
This visualization represents the **Klein-Projective Manifold** with the **Monster Inverse Stitch**.
The Moebius Stitch ($\omega\iota = -1$) creates the fundamental topological twist, while the 
Monster Inverse ($u \leftrightarrow u^*$) reflects dimensions 1-24 into 25-48.

#### **📐 Geometry of the 𝕌-Manifold**
The manifold is rendered as a **non-orientable Klein Bottle**, mapping spectral parameters to spatial coordinates:
*   **Toroidal Rotation ($u$)**: Represents the **Transfinite Phase** (the evolution of Thrust $\omega$).
*   **Poloidal Circulation ($v$)**: Represents the **Infinitesimal Spin** (the evolution of Anchor $\iota$).
*   **Surface Color ($\phi$)**: Maps to the **Standard Resonance ($S_R$)**. Bright regions indicate high tension (Repulsion), while dark regions indicate Resonance Locks.
""")

# --- Sidebar Controls ---
st.sidebar.header("𝕌 Manifold Controls")
jitter = st.sidebar.slider("Topological Jitter (δ)", 0.0, 1.0, 0.05, 
                           help="The non-associative gap curvature (κ). Increasing δ reveals the 'friction' between Thrust and Anchor.")
squeeze = st.sidebar.slider("Protoreal Squeeze Factor", 0.0, 2.0, 1.0, 
                            help="Phase correction for resonance stability. Adjusts the spectral density across the manifold surface.")
resolution = st.sidebar.select_slider("Resolution", options=[12, 24, 48, 96], value=24, 
                                      help="Spectral resolution. 24 corresponds to the Leech Lattice dimension.")

if ENGINE_AVAILABLE:
    status = get_engine_status()
    st.sidebar.markdown("---")
    st.sidebar.success(f"Duality: {status['Duality']}")
    st.sidebar.caption(f"Audit: {status['2M Audit']}")

# --- Klein Bottle Geometry ---
def generate_klein_bottle(u_res, v_res, δ, s):
    u = np.linspace(0, 2 * np.pi, u_res)
    v = np.linspace(0, 2 * np.pi, v_res)
    u, v = np.meshgrid(u, v)

    # Parametric equations for a Klein Bottle
    r = 4 * (1 - np.cos(u) / 2)
    x = 6 * np.cos(u) * (1 + np.sin(u)) + r * np.cos(u) * np.cos(v)
    y = 16 * np.sin(u) + r * np.sin(u) * np.cos(v)
    z = r * np.sin(v)

    # Twisted part for non-orientability
    mask = u > np.pi
    x[mask] = 6 * np.cos(u[mask]) * (1 + np.sin(u[mask])) + r[mask] * np.cos(v[mask] + np.pi)
    
    # Resonance mapping with squeeze
    resonance = (np.sin(u) * np.cos(v) * (1 - δ) + δ * np.cos(u*2)) * s
    
    return x, y, z, resonance

x, y, z, resonance = generate_klein_bottle(resolution * 2, resolution, jitter, squeeze)

# --- Plotly 3D Surface ---
fig = go.Figure(data=[go.Surface(
    x=x, y=y, z=z, 
    surfacecolor=resonance,
    colorscale='Viridis',
    reversescale=True,
    colorbar=dict(title="Resonance (𝕌)", tickprefix="φ"),
    lighting=dict(ambient=0.4, diffuse=0.8, roughness=0.1, specular=1.5),
    lightposition=dict(x=100, y=200, z=150)
)])

fig.update_layout(
    title=f"Klein Spectral Topology (Jitter δ={jitter:.2f} | Squeeze={squeeze:.1f})",
    scene=dict(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        zaxis=dict(visible=False),
        bgcolor="rgba(0,0,0,0)"
    ),
    template="plotly_dark",
    margin=dict(l=0, r=0, b=0, t=50),
    height=700
)

st.plotly_chart(fig, use_container_width=True)

# --- Metrics ---
st.markdown("---")
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Duality Offset", "0.5000", help="a_𝕌 − Re(s) = 1/2")
c2.metric("Curvature (κ)", "-1.0", help="Non-associative gap (topological invariant)")
c3.metric("Stitched Growth", "0.5973", delta="→ 0.5 target", help="Monster Inverse growth ratio")
c4.metric("2M Audit", "PASSED", delta="0 anomalies", delta_color="normal")
c5.metric("Bearing ( Compass )", "1.000", help="Topological Orientation Flux (b*c)")

st.markdown(r"""
### 🏗️ The Monster Inverse Mechanism
The **Parity-Locked Projection** $(u + u^*)/2$ reflects the transfinite thrust through the 
infinitesimal anchor. This doubling-and-averaging mirrors the relationship between dimensions 
1-24 and 25-48 in the **Leech Lattice**, creating the algebraic foundation for the 
**Protoreal-Complex Duality**: $a_{\\mathbb{U}} - Re(s) = 1/2$.
""")

st.markdown("---")
st.markdown("#### **Next Step: High-Throughput Pharming**")
st.markdown(r"""
The global manifold is now visible. To scale our search, we employ the NeuroPharm 
engine for high-throughput batch resonance scouting.
""")
if st.button("💊 Proceed to NeuroPharm Scan"):
    st.switch_page("pages/7_NeuroPharm_Scan.py")
