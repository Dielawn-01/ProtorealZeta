import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import goait
from goait.agent import GoaitAgent
from goait.zetaspace import ProtorealAR

st.set_page_config(page_title="GOAIT: Research Dashboard", layout="wide", page_icon="🧭")

def run_dashboard():
    st.title("🧭 GOAIT: Generative Observatory Dashboard")
    st.markdown("### Analyzing Adelic Topology & Modular Resonance")
    
    agent = GoaitAgent()
    
    # --- Sidebar ---
    st.sidebar.header("Topological Settings")
    manifold_depth = st.sidebar.slider("Surreal Depth (epsilon)", 0.0, 1.0, 0.5)
    modular_mode = st.sidebar.selectbox("Modular Symmetry", ["Mod-12", "Mod-24 (Monster)", "Mod-60"])
    
    # --- Row 1: Manifold Curvature ---
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Manifold Curvature (κ)")
        # Sample some zeros to show the curvature landscape
        sample_t = np.linspace(14.13, 1000, 100)
        curvatures = [agent.query_resonance(t)['manifold_curvature'] for t in sample_t]
        
        fig_curv = px.line(x=sample_t, y=curvatures, labels={'x': 't (Height)', 'y': 'Curvature (κ)'},
                          title="Curvature Landscape across Spectral Anchors", template="plotly_dark")
        st.plotly_chart(fig_curv, use_container_width=True)
        
    with col2:
        st.subheader("Modular Pull (Mod-24)")
        # Simulate modular structure from the user's research
        mod_vals = np.random.normal(0.1, 0.05, 24)
        mod_vals[21] *= 2 # Orientation flip at 21
        mod_vals[23] *= -3 # Inversion at 24
        
        fig_mod = px.bar(x=list(range(24)), y=mod_vals, labels={'x': 'Mod-24 Index', 'y': 'Mean Iota Pull'},
                        title="Topological Warp by Monstrous Symmetry", template="plotly_dark")
        st.plotly_chart(fig_mod, use_container_width=True)

    # --- Row 2: ZetaSpace Geometry ---
    st.divider()
    st.subheader("📐 ZetaSpace: Geometric Construction Audit")
    
    c1, c2 = st.columns([1, 2])
    with c1:
        st.write("Current Proof State (Protoreal Triangle)")
        u_a = goait.ProtorealFull(1, 0, 0)
        u_b = goait.ProtorealFull(1, 0, 0)
        u_c_sq = ProtorealAR.protoreal_pythagoras(u_a, u_b)
        
        st.metric("Euclidean Hypotenuse^2", "2.0")
        st.metric("Protoreal Hypotenuse^2", f"{u_c_sq.a:.4f}", delta=f"{u_c_sq.a - 2.0:.4f} (Curvature)")
        
    with c2:
        # 3D Visualization of the Klein Manifold local patch
        X, Y = np.meshgrid(np.linspace(-2, 2, 20), np.linspace(-2, 2, 20))
        Z = np.sin(X) * np.cos(Y) * np.exp(-0.1 * (X**2 + Y**2)) # Conceptual non-orientable patch
        
        fig_klein = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale='Magma')])
        fig_klein.update_layout(title="ZetaSpace: Local Manifold Patch", template="plotly_dark", height=400)
        st.plotly_chart(fig_klein, use_container_width=True)

    # --- Row 3: Trade Simulation (Hypothesis Testing) ---
    st.divider()
    st.subheader("💹 Spectral Trade Simulation")
    st.info("Hypothesis: Modular forms in the zeta zeros for prime outputs drive market resonance.")
    
    # Simulate a price sequence driven by Protoreal Dilation
    days = 100
    base_price = 100
    # Add 'Modular Jitter' to the returns
    returns = np.random.normal(0.001, 0.02, days)
    # Inject Prime-index resonance
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    for p in primes:
        if p < days:
            returns[p] += 0.05 * np.cos(p % 24) # Modular-weighted prime boost
            
    price_seq = base_price * np.exp(np.cumsum(returns))
    
    fig_trade = px.line(x=list(range(days)), y=price_seq, labels={'x': 'Step', 'y': 'Protoreal Price'},
                       title="Simulated Trade Sequence (Prime-Modular Resonance)", template="plotly_dark")
    st.plotly_chart(fig_trade, use_container_width=True)

    st.success("✅ Dashboard Ready. GoaitAgent is monitoring the background mining run.")

if __name__ == "__main__":
    run_dashboard()
