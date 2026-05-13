import streamlit as st
import os
import sys
import time

# Ensure legacy_methods and SpectralObservatory are in the path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, 'SpectralObservatory'))

import ZetaEngine as ze

# Import legacy logic
# We need to be careful with the imports inside the legacy script
try:
    import legacy_methods.UnrealEngine as ue_legacy
    # We can't easily import LaRue-R-S_optimization due to the hyphen in filename
    # We'll use import_module or just re-implement the call logic here
    import importlib.util
    spec = importlib.util.spec_from_file_location("lrs_opt", os.path.join(BASE_DIR, "legacy_methods", "LaRue-R-S_optimization.py"))
    lrs_opt = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(lrs_opt)
    LEGACY_AVAILABLE = True
except Exception as e:
    st.error(f"Legacy modules could not be loaded: {e}")
    LEGACY_AVAILABLE = False

st.set_page_config(page_title="Legacy Audit", page_icon="🕵️", layout="wide")

st.title("🕵️ Legacy Audit: LRS vs. Protoreal")

st.markdown("""
This module allows you to run the legacy **La Rue - Riemann-Siegel (LRS) Squeeze Engine** 
and compare its predictions against the current **Protoreal T3 Antenna**.
""")

if LEGACY_AVAILABLE:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Coordinates (l, m, n)")
        l = st.number_input("l", value=105, step=1)
        m = st.number_input("m", value=107, step=1)
        n = st.number_input("n", value=117, step=1)
        
    with col2:
        st.subheader("Audit Parameters")
        margin = st.slider("Squeeze Window Margin", 0.05, 1.0, 0.15)
        
    if st.button("🚀 Run Comparative Audit"):
        col_res1, col_res2 = st.columns(2)
        
        with col_res1:
            st.write("### 📜 Legacy Scout Results")
            start_legacy = time.time()
            try:
                t_est_legacy = lrs_opt.scout_antenna(l, m, n)
                legacy_time = time.time() - start_legacy
                st.write(f"**Estimated Height (t_est):** {t_est_legacy}")
                st.write(f"**Latency:** {legacy_time:.6f}s")
                
                # Get actual zero for reference
                rank, db_zero = ze.get_nearest_zero(float(t_est_legacy))
                st.write(f"**Nearest Database Zero (γ_{rank}):** {db_zero}")
                
                err_legacy = abs(float(t_est_legacy) - db_zero)
                st.metric("Legacy Error (Absolute)", f"{err_legacy:.6f}")
            except Exception as e:
                st.error(f"Legacy run failed: {e}")

        with col_res2:
            st.write("### 🏹 Protoreal T3 Scout Results")
            start_proto = time.time()
            try:
                val_proto, eps_proto, norm_proto, rank_proto, energy_proto = ze.T3_l_m_n(l, m, n)
                proto_time = time.time() - start_proto
                st.write(f"**Estimated Height (t_est):** {val_proto}")
                st.write(f"**Latency:** {proto_time:.6f}s")
                st.metric("Protoreal Error (Absolute)", f"{eps_proto:.6f}", 
                          delta=f"{eps_proto - err_legacy:.6f}" if 'err_legacy' in locals() else None, 
                          delta_color="inverse")
                st.metric("Spectral Energy (E)", f"{energy_proto:.6f} potential")
            except Exception as e:
                st.error(f"Protoreal run failed: {e}")

        st.markdown("---")
        st.subheader("🕳️ LRS Divergence: The Anti-Anchor Scan")
        st.markdown("""
        Legacy analysis focused on **Repulsion Zones** (where $S_R \\approx 0.5$). 
        These "Anti-Anchors" represent the maximum topological tension in the manifold.
        """)
        
        if st.checkbox("🔍 Initiate Mass Divergence Audit (Budget: 500)"):
            import pandas as pd
            import plotly.express as px
            
            with st.spinner("Scanning for Anti-Anchors..."):
                results = []
                for i in range(1, 15):
                    for j in range(1, 15):
                        for k in range(1, 15):
                            v, e, n_eps, r, energy = ze.T3_l_m_n(i, j, k)
                            results.append({
                                'l': i, 'm': j, 'n': k,
                                'norm': float(n_eps),
                                'energy': float(energy),
                                'mod24': (i + j + k) % 24,
                                'repulsion': abs(float(n_eps) - 0.5)
                            })
                df = pd.DataFrame(results)
                anti_anchors = df.sort_values('repulsion').head(20)
                
                c1, c2 = st.columns([1, 2])
                with c1:
                    st.write("**Top Anti-Anchors**")
                    st.dataframe(anti_anchors[['l', 'm', 'n', 'norm', 'mod24']], hide_index=True)
                
                with c2:
                    fig = px.bar(df.groupby('mod24')['repulsion'].mean().reset_index(), 
                                 x='mod24', y='repulsion', 
                                 title="Mod-24 Repulsion Distribution",
                                 color_continuous_scale="Magma")
                    fig.update_layout(template="plotly_dark", height=300)
                    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("Legacy methods are not available. Please ensure `legacy_methods/` contains the necessary files.")

st.markdown("---")
if st.button("🏠 Return to Mission Control"):
    st.switch_page("observatory.py")
