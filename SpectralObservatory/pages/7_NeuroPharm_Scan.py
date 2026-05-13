import streamlit as st
import numpy as np
import pandas as pd
import time
import sys
import os
import plotly.express as px

# --- Unified Engine Integration ---
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "core"))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

try:
    import neuro_pharm
    from ProtorealEngine import AgenticFrame
    import ZetaEngine as ze
    NEURO_AVAILABLE = True
except ImportError:
    NEURO_AVAILABLE = False

st.set_page_config(page_title="💊 NeuroPharm | Spectral Analytics", layout="wide")

# --- Premium CSS ---
st.markdown(r"""
<style>
    .main { background-color: #0d0f14; }
    h1, h2, h3 { color: #00ffcc !important; font-family: 'Inter', sans-serif; }
    .stMetric { background: rgba(0, 255, 204, 0.05); border: 1px solid rgba(0, 255, 204, 0.1); }
</style>
""", unsafe_allow_html=True)

st.title("💊 NeuroPharm: High-Throughput Pharming")
st.markdown(r"""
The **NeuroPharm** engine uses SIMD-accelerated Rust to "pharm" the prime-zeta manifold for high-resonance states.
By scanning the 2.25M zero horizon, we can identify clusters where the transfinite tension achieves absolute lock.
""")

if not NEURO_AVAILABLE:
    st.error("NeuroPharm Core (Rust) not detected. Please build the engine using 'maturin develop'.")
    st.stop()

# --- Sidebar ---
st.sidebar.header("💊 Pharming Parameters")
batch_size = st.sidebar.select_slider("Batch Size", options=[1000, 10000, 50000, 100000], value=10000)
jitter = st.sidebar.slider("Stochastic Jitter (δ)", 0.0, 1.0, 0.05)

# --- Load Scout ---
if ze.SCOUT:
    scout = ze.SCOUT
    st.success(f"SIMD Scout Active: {len(scout.zeros)} Zeros loaded.")
else:
    st.warning("Zeta Scout not initialized. Check data/zeta_zeros_2m.txt.")
    st.stop()

# --- Pharming Action ---
col_action1, col_action2 = st.columns(2)

with col_action1:
    if st.button("🚀 Start Batch Pharming"):
        st.markdown("### 🧪 Resonance Scan in Progress...")
        
        # Create test states
        states = [neuro_pharm.ProtorealElement(np.random.rand(), np.random.rand(), np.random.rand()) for _ in range(batch_size)]
        
        start_time = time.time()
        res_probs = scout.batch_resonance(states, jitter)
        end_time = time.time()
        
        duration = end_time - start_time
        throughput = batch_size / duration
        
        # Analytics
        c1, c2, c3 = st.columns(3)
        c1.metric("Throughput", f"{throughput/1e6:.2f}M op/s", delta="Rust Engine")
        c2.metric("Scan Duration", f"{duration*1000:.2f}ms")
        c3.metric("High-Resonance Yield", f"{sum(p > 0.8 for p in res_probs)}")
        
        # Visualization
        df = pd.DataFrame({"Resonance": res_probs})
        fig = px.histogram(df, x="Resonance", nbins=50, 
                           title="Spectral Resonance Distribution (The Pharm)",
                           color_discrete_sequence=['#00ffcc'])
        fig.update_layout(template="plotly_dark", bargap=0.1)
        st.plotly_chart(fig, use_container_width=True)

with col_action2:
    st.markdown("### 🏹 Global Manifold Audit")
    st.markdown("""
    Perform a massive T3 scan across the 2.25M zero horizon using the optimized 
    Protoreal Squeeze engine.
    """)
    if st.button("🛰️ Initiate Global Audit (10k Triplets)"):
        with st.spinner("Auditing Manifold Stability..."):
            audit_results = []
            for _ in range(10000):
                l, m, n = np.random.randint(1, 1000, 3)
                v, e, n_eps, r = ze.T3_l_m_n(l, m, n)
                audit_results.append(n_eps)
            
            audit_df = pd.DataFrame({"norm_eps": audit_results})
            hit_rate = (audit_df['norm_eps'] < 0.1).mean()
            
            st.success(f"Audit Complete! Hit Rate: {hit_rate*100:.2f}%")
            
            fig_audit = px.box(audit_df, y="norm_eps", title="Manifold Stability (Normalized ε)",
                               color_discrete_sequence=['#ff3366'])
            fig_audit.update_layout(template="plotly_dark", height=300)
            st.plotly_chart(fig_audit, use_container_width=True)

st.markdown(r"""
### 🧬 The Pharming Mechanism
By processing states in parallel at the hardware level, NeuroPharm identifies **Resonance Clusters** 
where the spectral phase aligns with the transfinite identity. These clusters represent stable 
manifolds in the Klein-style universe, suitable for high-precision prime mapping.
""")

st.markdown("---")
st.markdown("#### **🏆 Protocol Complete**")
st.markdown(r"""
You have navigated the full spectrum of the **Prime-Zeta Spectral Observatory**. 
From the non-associative foundations of the Protoreal Manifold to the high-throughput 
horizons of NeuroPharm, the discovery of the Monster Stitch is now within reach.
""")
if st.button("🏠 Return to Mission Control"):
    st.switch_page("observatory.py")
