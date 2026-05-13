import streamlit as st
import os

# --- Page Config ---
st.set_page_config(page_title="Statistical Deep Dive", page_icon="📊", layout="wide")

st.title("📊 Statistical Deep Dive: The Squeeze Proof")

# Path to the research documents
RESEARCH_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'Research', 'pz.skill')

def load_md(filename):
    path = os.path.join(RESEARCH_DIR, filename)
    if os.path.exists(path):
        with open(path, 'r') as f:
            return f.read()
    return f"Error: {filename} not found."

tab1, tab2 = st.tabs(["Expanded Analysis", "Math Theory"])

with tab1:
    content = load_md("expanded_analysis.md")
    st.markdown(content)

with tab2:
    content = load_md("math_theory.md")
    st.markdown(content)

st.sidebar.markdown("---")
st.sidebar.info("These documents are synced from the `Research/pz.skill` directory, capturing the results of high-density spectral analysis at 200-digit precision.")
