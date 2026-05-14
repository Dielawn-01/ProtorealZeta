import streamlit as st
import numpy as np
import plotly.graph_objects as go
import math, sys, os, copy

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "core"))
from ProtorealEngine import ProtorealElement, JetElement

PHI = (1 + math.sqrt(5)) / 2
GAMMA = 0.5772156649015329

st.set_page_config(page_title="Function Lab | Spectral Observatory", layout="wide")

st.markdown(r"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    .main { background-color: #05070a; }
    h1,h2,h3,h4 { color: #e8eaf0 !important; font-family: 'Inter', sans-serif; }
    .stMarkdown p { font-family: 'Inter', sans-serif; color: #a0a8b8; }
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(255,255,255,0.04), rgba(255,255,255,0.01));
        border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; padding: 16px;
    }
    [data-testid="stMetric"]:hover { border-color: rgba(0,255,204,0.4); }
    .lab-card {
        background: linear-gradient(135deg, rgba(112,0,255,0.06), rgba(0,255,204,0.03));
        border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; padding: 24px; margin: 12px 0;
    }
    .jet-card {
        background: linear-gradient(135deg, rgba(0,255,204,0.04), rgba(0,0,0,0));
        border: 1px solid rgba(0,255,204,0.12); border-radius: 16px; padding: 20px; margin: 12px 0;
    }
    .stTextArea textarea { font-family: 'JetBrains Mono', monospace !important; }
</style>
""", unsafe_allow_html=True)

st.title("🧪 Function Lab")
st.markdown(r"""
**Multi-variable Protoreal function builder.** Define variables with Klein manifold weights,
write functions over them, and watch the orbits trace across the jet space $\varepsilon^n = 0$.
""")

# ════════════════════════════════════════════════════
# SIDEBAR: JET ORDER + GLOBAL CONTROLS
# ════════════════════════════════════════════════════

st.sidebar.header("⚙️ Jet Configuration")
jet_order = st.sidebar.slider("Nilpotent Depth (n)", 2, 12, 3,
    help="εⁿ = 0. Higher = more derivative information retained.")
n_iterations = st.sidebar.slider("Iterations", 10, 500, 100)
st.sidebar.markdown(f"""
**Active Identities**
- εⁿ = 0 (n = {jet_order})
- ε ∘ λ = id (interior)
- ω · ι = −1 (Bridge)
- κ = −1 (Curvature)
""")

st.sidebar.markdown("---")
st.sidebar.header("🎨 Visualization")
show_jet_waterfall = st.sidebar.checkbox("Show Jet Waterfall", True)
show_klein_bottle = st.sidebar.checkbox("Show Klein Bottle", True)
bottle_opacity = st.sidebar.slider("Bottle Opacity", 0.05, 0.6, 0.25, 0.05)

# ════════════════════════════════════════════════════
# VARIABLE DEFINITION PANEL
# ════════════════════════════════════════════════════

st.markdown("---")
st.markdown("## 📐 Variable Definitions")
st.markdown("Each variable is a full Protoreal element. Weights can reference other variables.")

if 'var_count' not in st.session_state:
    st.session_state.var_count = 2
if 'var_names' not in st.session_state:
    st.session_state.var_names = ['x', 'y']

col_add, col_rm, _ = st.columns([1, 1, 4])
if col_add.button("➕ Add Variable"):
    nm = chr(ord('x') + st.session_state.var_count) if st.session_state.var_count < 4 else f"v{st.session_state.var_count}"
    st.session_state.var_names.append(nm)
    st.session_state.var_count += 1
if col_rm.button("➖ Remove Last") and st.session_state.var_count > 1:
    st.session_state.var_names.pop()
    st.session_state.var_count -= 1

# Default weight expressions per variable
DEFAULT_WEIGHTS = {
    'x': {'a': '1.0', 'w': '14.134', 'i': '1/x_w', 'e': '0.1', 'l': '1'},
    'y': {'a': '0.5', 'w': 'x_w * phi', 'i': 'gamma', 'e': '0.0', 'l': 'x_l + 1'},
}

var_weight_exprs = {}
var_cols = st.columns(min(st.session_state.var_count, 4))

for idx, vname in enumerate(st.session_state.var_names):
    col = var_cols[idx % len(var_cols)]
    with col:
        st.markdown(f"#### Variable `{vname}`")
        defaults = DEFAULT_WEIGHTS.get(vname, {'a':'1.0','w':'1.0','i':'1.0','e':'0.0','l':'1'})
        wa = st.text_input(f"{vname}.a (Real)", defaults['a'], key=f"w_{vname}_a")
        ww = st.text_input(f"{vname}.ω (Thrust)", defaults['w'], key=f"w_{vname}_w")
        wi = st.text_input(f"{vname}.ι (Anchor)", defaults['i'], key=f"w_{vname}_i")
        we = st.text_input(f"{vname}.ε (Noise)", defaults['e'], key=f"w_{vname}_e")
        wl = st.text_input(f"{vname}.λ (Level)", defaults['l'], key=f"w_{vname}_l")
        var_weight_exprs[vname] = {'a': wa, 'w': ww, 'i': wi, 'e': we, 'l': wl}

# ════════════════════════════════════════════════════
# RESOLVE CODEPENDENT WEIGHTS
# ════════════════════════════════════════════════════

def resolve_weights(exprs_dict):
    """Resolve codependent weight expressions into ProtorealElements."""
    env = {
        'phi': PHI, 'gamma': GAMMA, 'pi': math.pi, 'e': math.e,
        'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
        'exp': math.exp, 'log': math.log, 'sqrt': math.sqrt,
        'tanh': math.tanh, 'sinh': math.sinh, 'cosh': math.cosh,
        'abs': abs,
    }
    resolved = {}
    # Multiple passes to resolve dependencies
    for _ in range(3):
        for vname, weights in exprs_dict.items():
            vals = {}
            for comp, expr in weights.items():
                # Replace var refs: x_w → resolved['x']['w']
                eval_expr = expr
                for other_v in exprs_dict:
                    for c in ['a', 'w', 'i', 'e', 'l']:
                        placeholder = f"{other_v}_{c}"
                        if placeholder in eval_expr and other_v in resolved:
                            eval_expr = eval_expr.replace(placeholder, str(resolved[other_v].get(c, 0)))
                try:
                    vals[comp] = float(eval(eval_expr, {"__builtins__": {}}, env))
                except:
                    vals[comp] = resolved.get(vname, {}).get(comp, 0.0)
            resolved[vname] = vals

    elements = {}
    for vname, vals in resolved.items():
        elements[vname] = ProtorealElement(
            a=vals.get('a', 0), b=vals.get('w', 0), c=vals.get('i', 0),
            e=vals.get('e', 0), l=vals.get('l', 1)
        )
    return elements, resolved

var_elements, var_raw = resolve_weights(var_weight_exprs)

# Show resolved values
st.markdown("#### Resolved Weights")
import pandas as pd
rows = []
for vn in st.session_state.var_names:
    if vn in var_raw:
        r = var_raw[vn]
        rows.append({'Var': vn, 'a': f"{r['a']:.4f}", 'ω': f"{r['w']:.4f}",
                      'ι': f"{r['i']:.4f}", 'ε': f"{r['e']:.4f}", 'λ': f"{r['l']:.1f}"})
if rows:
    st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)

# ════════════════════════════════════════════════════
# FUNCTION DEFINITION
# ════════════════════════════════════════════════════

st.markdown("---")
st.markdown("## 🔬 Function Definition")

PRESETS = {
    "Klein Product (x·y)": "x * y",
    "Jet Oscillator": "P(a=x.a + x.e*sin(step*0.1), b=x.b, c=x.c, e=-x.b*x.c*(x.a-1)*0.05, l=x.l+1)",
    "Two-Body Orbit": "P(a=x.a+x.e, b=x.b*cos(0.05)-y.c*sin(0.05), c=x.b*sin(0.05)+y.c*cos(0.05), e=y.e*0.99, l=x.l+1)",
    "ε-λ Tower": "P(a=x.a+x.e, b=x.b-0.01*x.e, c=x.c+0.01*x.e, e=0, l=x.l+1)",
    "Sowing Chain": "P(a=x.a+x.e+0.01*y.b*y.c, b=x.b, c=x.c, e=gamma/(1+step), l=x.l+1)",
    "Thermal Bridge": "P(a=x.a+x.e, b=x.b-0.01*(x.b-x.c), c=x.c+0.01*(x.b-x.c), e=0.1*exp(-abs(x.a-x.b*x.c)/(abs(x.b*x.c)+0.01)), l=x.l+1)",
    "Custom": "",
}

preset = st.selectbox("Presets", list(PRESETS.keys()), index=0)
fn_code = st.text_area("f(variables) → ProtorealElement", value=PRESETS[preset], height=80,
    help="Use variable names directly. P(...) = ProtorealElement constructor. 'step' = iteration index.")

# ════════════════════════════════════════════════════
# EVALUATION ENGINE
# ════════════════════════════════════════════════════

def make_eval_env(var_elems, step=0):
    from math import sin, cos, tan, exp, log, sqrt, pi, tanh, sinh, cosh, atan2, fabs
    env = {
        'P': ProtorealElement, 'Jet': JetElement,
        'sin': sin, 'cos': cos, 'tan': tan, 'exp': exp, 'log': log, 'sqrt': sqrt,
        'tanh': tanh, 'sinh': sinh, 'cosh': cosh, 'atan2': atan2, 'abs': fabs,
        'pi': pi, 'phi': PHI, 'gamma': GAMMA, 'step': step,
    }
    for vn, elem in var_elems.items():
        env[vn] = elem
    return env

def safe_clamp(u, lo=-100, hi=100):
    for attr in ['a', 'b', 'c', 'e', 'l']:
        v = getattr(u, attr)
        if math.isnan(v) or math.isinf(v):
            setattr(u, attr, 0.0)
        else:
            setattr(u, attr, max(lo, min(hi, v)))
    return u

@st.cache_data
def run_lab(fn_code, _var_raw, n_iter, jet_n):
    # Rebuild elements from raw values (hashable)
    var_elems = {}
    for vn, vals in _var_raw.items():
        var_elems[vn] = ProtorealElement(
            a=vals['a'], b=vals['w'], c=vals['i'], e=vals['e'], l=vals['l'])

    first_var = list(var_elems.keys())[0]
    history = {comp: [] for comp in ['a', 'b', 'c', 'e', 'l', 'sr', 'energy']}
    jet_cascade = []  # jet coefficients at each step

    u = copy.deepcopy(var_elems[first_var])
    for step in range(n_iter):
        # Record state
        history['a'].append(u.a)
        history['b'].append(u.b)
        history['c'].append(u.c)
        history['e'].append(u.e)
        history['l'].append(u.l)
        sr = u.a - u.b * u.c
        history['sr'].append(sr)
        history['energy'].append(sr**2 + (u.b - u.c)**2)

        # Build jet from current state and record cascade
        jet = JetElement([u.a, u.e] + [u.e * (0.5**k) for k in range(1, jet_n - 1)], n=jet_n)
        jet_cascade.append([jet.iterate_epsilon(m).coeffs[0] if not jet.iterate_epsilon(m).is_zero() else 0.0
                           for m in range(jet_n)])

        # Evaluate function
        env = make_eval_env(var_elems, step)
        env[first_var] = u
        try:
            result = eval(fn_code, {"__builtins__": {}}, env)
            if isinstance(result, ProtorealElement):
                u = safe_clamp(result)
            elif isinstance(result, (int, float)):
                u = ProtorealElement(a=float(result))
            # Update the variable element for next iteration
            var_elems[first_var] = u
        except Exception:
            pass  # keep previous state

    return history, jet_cascade

# Convert var_raw to hashable tuple form for caching
var_raw_hashable = {k: {c: round(v, 10) for c, v in vals.items()} for k, vals in var_raw.items()}
history, jet_cascade = run_lab(fn_code, var_raw_hashable, n_iterations, jet_order)

# ════════════════════════════════════════════════════
# METRICS
# ════════════════════════════════════════════════════

st.markdown("---")
mc1, mc2, mc3, mc4, mc5 = st.columns(5)
mc1.metric("Final a", f"{history['a'][-1]:.4f}")
mc2.metric("Final SR", f"{history['sr'][-1]:.4f}")
mc3.metric("Final Energy", f"{history['energy'][-1]:.6f}")
mc4.metric("Jet Depth (n)", str(jet_order))
mc5.metric("Iterations", str(n_iterations))

# ════════════════════════════════════════════════════
# VISUALIZATION: KLEIN BOTTLE + PHASE PORTRAIT
# ════════════════════════════════════════════════════

if show_klein_bottle:
    col_kb, col_ph = st.columns([3, 2])

    with col_kb:
        st.markdown("#### 𝕌 Klein Manifold — Orbit Trace")
        r_kb, a_kb = 2.0, 2.0
        u_p = np.linspace(0, 2*np.pi, 50)
        v_p = np.linspace(0, 2*np.pi, 50)
        u_p, v_p = np.meshgrid(u_p, v_p)
        x_kb = (r_kb + a_kb*np.cos(v_p/2)*np.sin(u_p) - a_kb*np.sin(v_p/2)*np.sin(2*u_p))*np.cos(v_p)
        y_kb = (r_kb + a_kb*np.cos(v_p/2)*np.sin(u_p) - a_kb*np.sin(v_p/2)*np.sin(2*u_p))*np.sin(v_p)
        z_kb = a_kb*np.sin(v_p/2)*np.sin(u_p) + a_kb*np.cos(v_p/2)*np.sin(2*u_p)

        fig_kb = go.Figure()
        fig_kb.add_trace(go.Surface(x=x_kb, y=y_kb, z=z_kb,
            surfacecolor=1.0 - np.sin(u_p)*np.cos(v_p),
            colorscale=[[0,'#00ffcc'],[0.5,'#1a1a2e'],[1,'#ff3366']],
            showscale=False, opacity=bottle_opacity,
            lighting=dict(ambient=0.6, diffuse=0.5, roughness=0.5, specular=0.4)))

        # Project orbit onto bottle
        orb_x, orb_y, orb_z = [], [], []
        for i in range(len(history['b'])):
            bv, cv, av = history['b'][i], history['c'][i], history['a'][i]
            up = math.atan2(bv, abs(bv)+0.5)*2.0
            vp = math.atan2(cv, abs(cv)+0.5)*2.0
            ox = (r_kb + a_kb*math.cos(vp/2)*math.sin(up) - a_kb*math.sin(vp/2)*math.sin(2*up))*math.cos(vp)
            oy = (r_kb + a_kb*math.cos(vp/2)*math.sin(up) - a_kb*math.sin(vp/2)*math.sin(2*up))*math.sin(vp)
            oz = a_kb*math.sin(vp/2)*math.sin(up) + a_kb*math.cos(vp/2)*math.sin(2*up) + (av-1)*0.3
            orb_x.append(ox); orb_y.append(oy); orb_z.append(oz)

        # Color by jet depth (how much ε-info survives)
        jet_depths = [jet_cascade[i][0] if i < len(jet_cascade) else 0 for i in range(len(orb_x))]
        fig_kb.add_trace(go.Scatter3d(x=orb_x, y=orb_y, z=orb_z, mode='lines+markers',
            line=dict(width=3, color=jet_depths, colorscale='Viridis'),
            marker=dict(size=2, color=jet_depths, colorscale='Viridis',
                        colorbar=dict(title="Jet c₀", len=0.4, y=0.8)),
            name='Orbit'))
        fig_kb.add_trace(go.Scatter3d(x=[orb_x[0]], y=[orb_y[0]], z=[orb_z[0]],
            mode='markers', marker=dict(size=8, color='#00ffcc', symbol='circle'),
            name='Start', showlegend=False))
        fig_kb.add_trace(go.Scatter3d(x=[orb_x[-1]], y=[orb_y[-1]], z=[orb_z[-1]],
            mode='markers', marker=dict(size=10, color='#ff3366', symbol='diamond'),
            name='End', showlegend=False))

        wire = dict(showgrid=True, gridcolor='rgba(255,255,255,0.06)', showbackground=False,
                    showticklabels=True, tickfont=dict(size=9, color='rgba(255,255,255,0.4)'))
        fig_kb.update_layout(scene=dict(
            xaxis=dict(**wire, title=dict(text='ω', font=dict(size=11, color='#00ffcc'))),
            yaxis=dict(**wire, title=dict(text='ι', font=dict(size=11, color='#ff3366'))),
            zaxis=dict(**wire, title=dict(text='a', font=dict(size=11, color='#feca57'))),
            bgcolor='rgba(0,0,0,0)', camera=dict(eye=dict(x=1.5, y=1.5, z=0.8))),
            template="plotly_dark", height=550, margin=dict(l=0,r=0,b=0,t=10),
            paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_kb, use_container_width=True)

    with col_ph:
        st.markdown("#### Phase Portrait (ω, ι)")
        fig_ph = go.Figure()
        sr_vals = [abs(s) for s in history['sr']]
        fig_ph.add_trace(go.Scatter(x=history['b'], y=history['c'], mode='lines+markers',
            marker=dict(size=3, color=sr_vals,
                        colorscale=[[0,'#00ffcc'],[0.5,'#feca57'],[1,'#ff3366']],
                        colorbar=dict(title="|SR|", len=0.4)),
            line=dict(width=1, color='rgba(0,255,204,0.4)'), name='Orbit'))
        b_ref = np.linspace(0.2, 5, 100)
        fig_ph.add_trace(go.Scatter(x=b_ref, y=1.0/b_ref, mode='lines',
            line=dict(color='rgba(255,255,255,0.2)', dash='dot'), name='ωι=1'))
        fig_ph.add_trace(go.Scatter(x=b_ref, y=b_ref, mode='lines',
            line=dict(color='rgba(255,255,255,0.15)', dash='dash'), name='ω=ι'))
        fig_ph.update_layout(template="plotly_dark", height=260,
            margin=dict(l=20,r=20,t=10,b=20),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(title="ω", gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(title="ι", gridcolor='rgba(255,255,255,0.05)'))
        st.plotly_chart(fig_ph, use_container_width=True)

        st.markdown("#### Component Trajectories")
        fig_comp = go.Figure()
        colors = {'a': '#00ffcc', 'ω': '#feca57', 'ι': '#ff3366', 'ε': '#7c4dff', 'λ': '#00e5ff'}
        for name, key, color in [('a','a','#00ffcc'),('ω','b','#feca57'),('ι','c','#ff3366'),
                                   ('ε','e','#7c4dff'),('λ','l','#00e5ff')]:
            fig_comp.add_trace(go.Scatter(y=history[key], mode='lines',
                line=dict(color=color, width=1.5), name=name))
        fig_comp.add_hline(y=1.0, line_dash="dot", line_color="white", opacity=0.2)
        fig_comp.update_layout(template="plotly_dark", height=220,
            margin=dict(l=20,r=20,t=10,b=20),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(title="Step"), legend=dict(orientation="h", y=1.1))
        st.plotly_chart(fig_comp, use_container_width=True)

# ════════════════════════════════════════════════════
# JET WATERFALL — NILPOTENT DEPTH VISUALIZATION
# ════════════════════════════════════════════════════

if show_jet_waterfall and jet_cascade:
    st.markdown("---")
    st.markdown(r"""
    ## 🌊 Nilpotent Jet Waterfall
    Each row is a time step. Each column is an ε-shift depth (0 to n-1).
    Color intensity = surviving coefficient magnitude. **At depth n, everything is zero** — that's εⁿ = 0.
    """)

    cascade_arr = np.array(jet_cascade)
    # Sample evenly if too many steps
    if len(cascade_arr) > 100:
        indices = np.linspace(0, len(cascade_arr)-1, 100, dtype=int)
        cascade_arr = cascade_arr[indices]

    fig_jet = go.Figure(data=go.Heatmap(
        z=cascade_arr.T,
        x=list(range(len(cascade_arr))),
        y=[f"ε^{m}" for m in range(jet_order)],
        colorscale=[[0,'#05070a'],[0.3,'#7c4dff'],[0.6,'#00ffcc'],[1,'#feca57']],
        colorbar=dict(title="c₀ after m shifts"),
    ))
    fig_jet.update_layout(
        template="plotly_dark", height=280,
        margin=dict(l=60, r=20, t=10, b=40),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(title="Iteration", gridcolor='rgba(255,255,255,0.05)'),
        yaxis=dict(title="Shift Depth", gridcolor='rgba(255,255,255,0.05)'),
    )
    st.plotly_chart(fig_jet, use_container_width=True)

    st.markdown(r"""
    <div class="jet-card">
    <h4 style="color: #7c4dff; margin-top: 0;">📐 Reading the Waterfall</h4>
    <ul>
    <li><b>Row ε⁰</b>: The base coefficient — this is the "real part" of the jet.</li>
    <li><b>Row ε¹</b>: First derivative information (classical dual-number regime).</li>
    <li><b>Row ε^(n-1)</b>: The deepest surviving information before annihilation.</li>
    <li><b>Dark columns</b>: Steps where the function drove ε toward zero (sowing events).</li>
    <li><b>Bright columns</b>: Steps with active noise injection.</li>
    </ul>
    <p>The <b>Protoreal FTC</b> guarantees: ε∘λ = λ∘ε = id at interior depths. The boundary
    defect at depth 0 and n-1 encodes the "integration constant."</p>
    </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════
# IDENTITIES REFERENCE
# ════════════════════════════════════════════════════

st.markdown("---")
col_id1, col_id2, col_id3 = st.columns(3)
with col_id1:
    st.markdown("#### Nilpotency")
    st.latex(rf"\varepsilon^{{{jet_order}}} = 0")
    st.caption(f"Noise annihilates at depth {jet_order}.")
with col_id2:
    st.markdown("#### Protoreal FTC")
    st.latex(r"\varepsilon \circ \lambda = \lambda \circ \varepsilon = \mathrm{id}")
    st.caption("Interior roundtrip (boundary defect at edges).")
with col_id3:
    st.markdown("#### Bridge Contraction")
    st.latex(r"\omega \cdot \iota = -1")
    st.caption("The fundamental identity.")

# ── Footer ──
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #667; font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; padding: 20px;">
    Function Lab | Spectral Observatory<br>
    Jet Space: εⁿ = 0 · Protoreal FTC Verified · 51 Lean Modules · 0 Sorry
</div>
""", unsafe_allow_html=True)
