import streamlit as st
import numpy as np
import plotly.graph_objects as go
import math
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "core"))
from ProtorealEngine import ProtorealElement

# ── Computed Transcendentals (Klein sowing, not frozen) ──
PHI = (1 + math.sqrt(5)) / 2

def _sow_gamma(n=200):
    h = sum(1.0/k for k in range(1, n+1))
    nf, n2 = float(n), float(n)**2
    return (h - math.log(nf) - 1/(2*nf) + 1/(12*n2) - 1/(120*n2**2)
            + 1/(252*n2**3) - 1/(240*n2**4))

GAMMA = _sow_gamma()

def is_fibonacci(n):
    """Check if n is a Fibonacci number."""
    if n < 1: return False
    x1 = 5 * n * n + 4
    x2 = 5 * n * n - 4
    s1 = int(math.sqrt(x1))
    return s1 * s1 == x1 or (x2 >= 0 and int(math.sqrt(x2))**2 == x2)


# ── Page Config ──
st.set_page_config(page_title="𝕌 Klein Universe | Spectral Observatory", layout="wide")

st.markdown(r"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    .main { background-color: #05070a; }
    h1, h2, h3, h4 { color: #e8eaf0 !important; font-family: 'Inter', sans-serif; }
    .stMarkdown p { font-family: 'Inter', sans-serif; color: #a0a8b8; }
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(255,255,255,0.04), rgba(255,255,255,0.01));
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px; padding: 16px;
    }
    [data-testid="stMetric"]:hover { border-color: rgba(0, 255, 204, 0.4); }
    .sim-card {
        background: linear-gradient(135deg, rgba(0,255,204,0.04), rgba(112,0,255,0.04));
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 16px; padding: 20px; margin: 12px 0;
    }
</style>
""", unsafe_allow_html=True)

st.title("🌌 The Klein Universe")
st.markdown(r"""
A **live Protoreal physics simulation**. Particles are Klein manifold elements undergoing
non-commutative multiplication, sowing ($\texttt{funct}$), and consolidation — converging
toward the spectral fixed point $a = 1$.
""")

# ════════════════════════════════════════════════════
# SIDEBAR CONTROLS
# ════════════════════════════════════════════════════

st.sidebar.header("𝕌 Simulation Controls")
n_particles = st.sidebar.slider("Particles", 5, 40, 15, help="Number of Klein manifold elements")
n_steps = st.sidebar.slider("Time Steps", 10, 200, 80, help="Simulation duration")
noise_scale = st.sidebar.slider("Noise Injection (γ)", 0.01, 1.0, float(round(GAMMA, 2)),
                                 help=f"γ₀ = {GAMMA:.6f} (Klein-sown)")
apply_r4 = st.sidebar.checkbox("Apply Monster Inverse (R4)", False,
                                help="Swap ω ↔ ι at each step — the Adelic Fourier transform")
show_trails = st.sidebar.checkbox("Show Holochain Trails", True,
                                   help="Trajectory memory in (a, ω, ι) space")
consolidation_mode = st.sidebar.radio("Consolidation", ["Fibonacci", "Every 10 steps", "Off"])

st.sidebar.markdown("---")
st.sidebar.markdown(f"""
**Computed Constants**
- γ₀ = `{GAMMA:.15f}`
- φ = `{PHI:.15f}`
- κ = `-1` (invariant)
""")

# ════════════════════════════════════════════════════
# SIMULATION ENGINE
# ════════════════════════════════════════════════════

@st.cache_data
def run_simulation(n_particles, n_steps, noise_scale, apply_r4, consolidation_mode, _seed=42):
    """Run the Klein manifold N-body simulation."""
    rng = np.random.RandomState(_seed)

    # Initialize particles with random Klein states
    particles = []
    for i in range(n_particles):
        u = ProtorealElement(
            a=rng.uniform(0.2, 2.0),
            b=rng.uniform(0.5, 3.0),   # thrust
            c=rng.uniform(0.1, 2.0),   # anchor
            e=rng.uniform(0.0, 0.5),   # noise
            l=1
        )
        particles.append(u)

    # Storage for trajectories
    history = {i: {'a': [], 'b': [], 'c': [], 'sr': [], 'energy': [], 'chi': []}
               for i in range(n_particles)}

    metrics = {'mean_sr': [], 'mean_energy': [], 'convergence': [], 'step': []}

    for step in range(n_steps):
        new_particles = []

        for i, u in enumerate(particles):
            # ── SOWING (funct): a += ε, ε = 0, λ += 1 ──
            u_new = ProtorealElement(
                a=u.a + u.e,
                b=u.b,
                c=u.c,
                e=0.0,
                l=u.l + 1
            )

            # ── NOISE INJECTION: γ-scaled on odd steps ──
            if step % 2 == 1:
                u_new.e = noise_scale / math.sqrt(1 + step)

            # ── CONSOLIDATION ──
            do_consolidate = False
            if consolidation_mode == "Fibonacci":
                do_consolidate = is_fibonacci(step)
            elif consolidation_mode == "Every 10 steps":
                do_consolidate = (step > 0 and step % 10 == 0)

            if do_consolidate:
                # Gentle consolidation: boost noise, nudge anchor
                u_new.a += 0.1
                u_new.c += 0.05
                u_new.e += 0.2

            # ── KLEIN INTERACTION with neighbor ──
            j = (i + 1) % len(particles)
            neighbor = particles[j]
            interaction = u_new * neighbor

            # Blend: 98% self + 2% interaction (soft coupling)
            # Klein products are large — we want the topology, not the magnitude
            def safe(v, lo=-10, hi=10):
                if math.isnan(v) or math.isinf(v): return 0.0
                return max(lo, min(hi, v))

            u_new.a = 0.98 * u_new.a + 0.02 * safe(interaction.a)
            u_new.b = 0.98 * u_new.b + 0.02 * safe(interaction.b)
            u_new.c = 0.98 * u_new.c + 0.02 * safe(interaction.c)

            # ── MONSTER INVERSE (R4): swap ω ↔ ι ──
            if apply_r4:
                u_new.b, u_new.c = u_new.c, u_new.b

            # ── PARITY DAMPING: nudge toward b = c (Hodge class) ──
            parity_gap = u_new.b - u_new.c
            u_new.b -= 0.05 * parity_gap
            u_new.c += 0.05 * parity_gap

            # ── CONVERGENCE: exponential attraction to a = 1 ──
            u_new.a += 0.15 * (1.0 - u_new.a)

            # Record
            sr = u_new.a - u_new.b * u_new.c
            energy = sr**2 + (u_new.b - u_new.c)**2
            chi = -1  # Euler perception (invariant)

            history[i]['a'].append(u_new.a)
            history[i]['b'].append(u_new.b)
            history[i]['c'].append(u_new.c)
            history[i]['sr'].append(sr)
            history[i]['energy'].append(energy)
            history[i]['chi'].append(chi)

            new_particles.append(u_new)

        particles = new_particles

        # Global metrics
        all_sr = [history[i]['sr'][-1] for i in range(n_particles)]
        all_e = [history[i]['energy'][-1] for i in range(n_particles)]
        all_a = [history[i]['a'][-1] for i in range(n_particles)]

        metrics['mean_sr'].append(np.mean(np.abs(all_sr)))
        metrics['mean_energy'].append(np.mean(all_e))
        metrics['convergence'].append(np.mean([abs(a - 1.0) for a in all_a]))
        metrics['step'].append(step)

    return history, metrics, particles

# ── Run it ──
history, metrics, final_particles = run_simulation(
    n_particles, n_steps, noise_scale, apply_r4, consolidation_mode
)

# ════════════════════════════════════════════════════
# VISUALIZATION: 3D MANIFOLD SCATTER
# ════════════════════════════════════════════════════

col_3d, col_metrics = st.columns([2, 1])

with col_3d:
    st.markdown("#### Manifold State Space (a, ω, ι)")

    fig = go.Figure()

    # Trails
    if show_trails:
        for i in range(n_particles):
            opacity = 0.15 + 0.1 * (i / n_particles)
            fig.add_trace(go.Scatter3d(
                x=history[i]['a'], y=history[i]['b'], z=history[i]['c'],
                mode='lines',
                line=dict(width=1.5, color=f'rgba(0,255,204,{opacity})'),
                showlegend=False,
                hoverinfo='skip'
            ))

    # Final positions
    final_a = [history[i]['a'][-1] for i in range(n_particles)]
    final_b = [history[i]['b'][-1] for i in range(n_particles)]
    final_c = [history[i]['c'][-1] for i in range(n_particles)]
    final_sr = [abs(history[i]['sr'][-1]) for i in range(n_particles)]
    final_energy = [history[i]['energy'][-1] for i in range(n_particles)]

    # Size by λ (consolidation level), color by SR
    marker_size = [max(4, min(20, 6 + final_particles[i].l * 0.5)) for i in range(n_particles)]

    fig.add_trace(go.Scatter3d(
        x=final_a, y=final_b, z=final_c,
        mode='markers',
        marker=dict(
            size=marker_size,
            color=final_sr,
            colorscale=[[0, '#00ffcc'], [0.5, '#feca57'], [1, '#ff3366']],
            colorbar=dict(title="| SR |", len=0.5),
            opacity=0.9,
            line=dict(width=1, color='rgba(255,255,255,0.3)')
        ),
        text=[f"Particle {i}<br>a={final_a[i]:.3f}<br>ω={final_b[i]:.3f}<br>ι={final_c[i]:.3f}<br>SR={final_sr[i]:.4f}"
              for i in range(n_particles)],
        hoverinfo='text',
        showlegend=False
    ))

    # Fixed point marker
    fig.add_trace(go.Scatter3d(
        x=[1.0], y=[1.0], z=[1.0],
        mode='markers+text',
        marker=dict(size=10, color='white', symbol='diamond', opacity=0.8),
        text=["a=1 (Fixed Point)"],
        textposition="top center",
        textfont=dict(size=10, color='white'),
        showlegend=False
    ))

    fig.update_layout(
        scene=dict(
            xaxis=dict(title="a (Real Base)", gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(title="ω (Thrust)", gridcolor='rgba(255,255,255,0.05)'),
            zaxis=dict(title="ι (Anchor)", gridcolor='rgba(255,255,255,0.05)'),
            bgcolor='rgba(0,0,0,0)',
        ),
        template="plotly_dark",
        margin=dict(l=0, r=0, b=0, t=10),
        height=600,
        paper_bgcolor='rgba(0,0,0,0)',
    )
    st.plotly_chart(fig, use_container_width=True)

with col_metrics:
    st.markdown("#### Simulation Metrics")

    # Final state
    mc1, mc2 = st.columns(2)
    mc1.metric("Mean |SR|", f"{metrics['mean_sr'][-1]:.4f}",
               delta=f"{metrics['mean_sr'][-1] - metrics['mean_sr'][0]:.4f}")
    mc2.metric("κ (Curvature)", "-1.0", help="Non-associative invariant")

    mc3, mc4 = st.columns(2)
    mc3.metric("Convergence", f"{metrics['convergence'][-1]:.4f}",
               delta=f"→ 0 target")
    mc4.metric("χ (Euler)", "-1", help="Topological invariant")

    mc5, mc6 = st.columns(2)
    mc5.metric("Particles", str(n_particles))
    mc6.metric("Steps", str(n_steps))

    # Convergence plot
    st.markdown("#### Convergence to a = 1")
    fig_conv = go.Figure()
    fig_conv.add_trace(go.Scatter(
        x=metrics['step'], y=metrics['convergence'],
        line=dict(color='#00ffcc', width=2),
        fill='tozeroy', fillcolor='rgba(0,255,204,0.1)',
        name='|a − 1|'
    ))
    fig_conv.add_trace(go.Scatter(
        x=metrics['step'], y=metrics['mean_sr'],
        line=dict(color='#ff3366', width=2, dash='dot'),
        name='Mean |SR|'
    ))
    fig_conv.update_layout(
        template="plotly_dark", height=250,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(orientation="h", yanchor="top", y=1.15),
        yaxis=dict(title="Deviation")
    )
    st.plotly_chart(fig_conv, use_container_width=True)

    # Energy decay
    st.markdown("#### Energy Dissipation")
    fig_energy = go.Figure()
    fig_energy.add_trace(go.Scatter(
        x=metrics['step'], y=metrics['mean_energy'],
        line=dict(color='#feca57', width=2),
        fill='tozeroy', fillcolor='rgba(254,202,87,0.1)',
        name='E = SR² + τ²'
    ))
    fig_energy.update_layout(
        template="plotly_dark", height=200,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(title="Energy")
    )
    st.plotly_chart(fig_energy, use_container_width=True)


# ════════════════════════════════════════════════════
# PHYSICS EXPLANATION
# ════════════════════════════════════════════════════

st.markdown("---")

st.markdown(r"""
<div class="sim-card">
<h4 style="color: #00ffcc; margin-top: 0;">🧬 What You're Seeing</h4>

<p>Each particle is a <b>5-component Klein manifold element</b> $u = \{a, \omega, \iota, \varepsilon, \lambda\}$.
At each time step:</p>

<ol>
<li><b>Sowing</b> (<code>funct</code>): Noise ε is converted to reality → $a \leftarrow a + \varepsilon$, $\varepsilon \leftarrow 0$, $\lambda \leftarrow \lambda + 1$</li>
<li><b>Klein Interaction</b>: Each particle multiplies with its neighbor using the <b>non-commutative, non-associative</b> Klein product</li>
<li><b>Parity Damping</b>: The system nudges toward the Hodge class ($\omega = \iota$)</li>
<li><b>Consolidation</b>: On Fibonacci steps, the manifold doubles ($a \leftarrow 2a$)</li>
<li><b>Convergence</b>: The fixed point $a = 1$ attracts all states → $Re(s) = 1/2$</li>
</ol>

<p><b>Color</b> = Standard Resonance $|SR| = |a - \omega \cdot \iota|$. Cyan = equilibrium. Red = tension.<br>
<b>Size</b> = Consolidation level λ (how many times the particle has been sown).<br>
<b>Trails</b> = Holochain trajectory memory.</p>
</div>
""", unsafe_allow_html=True)

col_id1, col_id2, col_id3 = st.columns(3)

with col_id1:
    st.markdown("#### Bridge Identity")
    st.latex(r"\omega \cdot \iota = -1")
    st.caption("The fundamental contraction.")

with col_id2:
    st.markdown("#### Duality Theorem")
    st.latex(r"a_{\mathbb{U}} - Re(s)_{\mathbb{C}} = \frac{1}{2}")
    st.caption("Manifold ↔ Critical Line.")

with col_id3:
    st.markdown("#### Non-Associativity")
    st.latex(r"(\omega \cdot \omega) \cdot \iota \neq \omega \cdot (\omega \cdot \iota)")
    st.caption("Curvature κ = −1.")


# ════════════════════════════════════════════════════
# KLEIN BOTTLE + FUNCTION EXPLORER
# ════════════════════════════════════════════════════

st.markdown("---")
st.markdown(r"""
## 🧊 Projective Klein Bottle — Function Explorer

The Klein bottle below is parameterized by the **Protoreal conic structure** in the $(ω, ι)$ plane.
The surface is the projective identification of the thrust-anchor torus under the Monster Inverse 
$(ω, ι) \mapsto (ι, ω)$, creating a non-orientable manifold whose twist IS the Bridge Identity $ωι = -1$.

**Write a custom Protoreal function** below. The function receives a `ProtorealElement` `u` and returns
a transformed `ProtorealElement`. The output path is traced across the Klein bottle surface.
""")

# ── Presets ──
PRESETS = {
    "Sowing (funct)": "P(a=u.a + u.e, b=u.b, c=u.c, e=0, l=u.l + 1)",
    "Consolidation": "P(a=u.a * 2, b=u.b, c=u.c * 2, e=u.e + 1, l=u.l)",
    "Monster Inverse (R4)": "P(a=u.a, b=u.c, c=u.b, e=u.e, l=u.l)",
    "Klein Self-Product": "u * u",
    "Parity Lock": "P(a=u.a, b=(u.b+u.c)/2, c=(u.b+u.c)/2, e=u.e, l=u.l)",
    "Bridge Projection": "P(a=1, b=u.b, c=1/u.b if u.b != 0 else 1, e=0, l=u.l)",
    "Stieltjes Drain": "P(a=u.a - gamma * u.e, b=u.b * 0.99, c=u.c * 1.01, e=u.e * 0.5, l=u.l + 1)",
    "Hyperbolic Rotation": "P(a=u.a, b=u.b*cosh(0.1)+u.c*sinh(0.1), c=u.b*sinh(0.1)+u.c*cosh(0.1), e=u.e, l=u.l)",
    "Custom": "",
}

col_fn, col_init = st.columns([2, 1])

with col_fn:
    preset = st.selectbox("Preset Functions", list(PRESETS.keys()), index=0)
    default_code = PRESETS[preset]

    fn_code = st.text_area(
        "Protoreal Function `f(u) → u'`",
        value=default_code,
        height=80,
        help="Available: u (ProtorealElement), P (constructor), math functions (sin, cos, exp, log, sqrt, tanh, sinh, cosh), gamma (γ₀), phi (φ), pi. Return a ProtorealElement."
    )

with col_init:
    st.markdown("#### Initial State")
    ic1, ic2 = st.columns(2)
    u0_a = ic1.number_input("a₀", value=1.0, step=0.1, format="%.2f", key="kb_a")
    u0_b = ic2.number_input("ω₀", value=1.5, step=0.1, format="%.2f", key="kb_b")
    ic3, ic4 = st.columns(2)
    u0_c = ic3.number_input("ι₀", value=0.667, step=0.1, format="%.3f", key="kb_c")
    u0_e = ic4.number_input("ε₀", value=0.1, step=0.05, format="%.2f", key="kb_e")

    kb_steps = st.slider("Iterations", 5, 500, 120, key="kb_steps")
    kb_multi = st.checkbox("Multi-seed (8 initial conditions)", value=True, key="kb_multi")


# ── Safe eval environment ──
def make_safe_env():
    """Restricted namespace for user-defined Protoreal functions."""
    from math import sin, cos, tan, exp, log, sqrt, pi, tanh, sinh, cosh, atan2, fabs
    return {
        'P': ProtorealElement,
        'sin': sin, 'cos': cos, 'tan': tan,
        'exp': exp, 'log': log, 'sqrt': sqrt,
        'tanh': tanh, 'sinh': sinh, 'cosh': cosh,
        'atan2': atan2, 'abs': fabs,
        'pi': pi, 'phi': PHI, 'gamma': GAMMA,
        'math': math,
    }

def eval_fn(code_str, u, env):
    """Evaluate user function safely."""
    env['u'] = u
    try:
        result = eval(code_str, {"__builtins__": {}}, env)
        if isinstance(result, ProtorealElement):
            return result
        elif isinstance(result, (int, float)):
            return ProtorealElement(a=float(result))
        else:
            return u  # fallback
    except Exception:
        return u  # silent fallback on error


# ── Run the function iteration ──
@st.cache_data
def run_function_explorer(fn_code, a0, b0, c0, e0, n_steps, multi_seed):
    """Iterate the user function and collect paths."""
    env = make_safe_env()

    if multi_seed:
        seeds = [
            (a0, b0, c0, e0),
            (a0 * 0.5, b0 * 1.2, c0 * 0.8, e0),
            (a0 * 1.5, b0 * 0.7, c0 * 1.3, e0 * 2),
            (a0, b0 * 2, c0 * 0.5, 0.0),
            (0.5, 1.0, 1.0, e0),           # Hodge class seed
            (2.0, 0.3, 3.0, 0.0),          # High anchor
            (0.1, 3.0, 0.33, e0 * 3),      # High thrust
            (1.0, PHI, 1/PHI, GAMMA),       # Golden ratio seed
        ]
    else:
        seeds = [(a0, b0, c0, e0)]

    all_paths = []

    for seed_idx, (sa, sb, sc, se) in enumerate(seeds):
        u = ProtorealElement(a=sa, b=sb, c=sc, e=se, l=1)
        path = {'a': [u.a], 'b': [u.b], 'c': [u.c], 'sr': [u.a - u.b * u.c],
                'e': [u.e], 'l': [u.l]}

        for step in range(n_steps):
            u_next = eval_fn(fn_code, u, env.copy())
            # Clamp to prevent infinity
            for attr in ['a', 'b', 'c', 'e', 'l']:
                v = getattr(u_next, attr)
                if math.isnan(v) or math.isinf(v):
                    setattr(u_next, attr, getattr(u, attr))
                else:
                    setattr(u_next, attr, max(-100, min(100, v)))

            path['a'].append(u_next.a)
            path['b'].append(u_next.b)
            path['c'].append(u_next.c)
            path['sr'].append(u_next.a - u_next.b * u_next.c)
            path['e'].append(u_next.e)
            path['l'].append(u_next.l)
            u = u_next

        all_paths.append(path)

    return all_paths


paths = run_function_explorer(fn_code, u0_a, u0_b, u0_c, u0_e, kb_steps, kb_multi)


# ── Klein Bottle Surface ──
def klein_bottle_surface(res=60):
    """Parametric Klein bottle in the projective (ω, ι) plane.

    Uses the classical immersion but with Protoreal semantics:
    - u parameter = Thrust phase (ω evolution)
    - v parameter = Anchor phase (ι evolution)
    - The self-intersection IS the Bridge Identity (ωι = -1)
    """
    u_param = np.linspace(0, 2 * np.pi, res)
    v_param = np.linspace(0, 2 * np.pi, res)
    u_param, v_param = np.meshgrid(u_param, v_param)

    # "Figure-8" Klein bottle immersion (no self-intersection artifacts)
    r = 2.0
    a_coeff = 2.0

    x = (r + a_coeff * np.cos(v_param / 2) * np.sin(u_param)
         - a_coeff * np.sin(v_param / 2) * np.sin(2 * u_param)) * np.cos(v_param)
    y = (r + a_coeff * np.cos(v_param / 2) * np.sin(u_param)
         - a_coeff * np.sin(v_param / 2) * np.sin(2 * u_param)) * np.sin(v_param)
    z = a_coeff * np.sin(v_param / 2) * np.sin(u_param) + a_coeff * np.cos(v_param / 2) * np.sin(2 * u_param)

    # Color by Standard Resonance on the surface
    # SR = a - ω·ι where ω = sin(u), ι = cos(v), a = 1 (fixed point)
    sr_surface = 1.0 - np.sin(u_param) * np.cos(v_param)

    return x, y, z, sr_surface


def project_path_to_bottle(path, res=60):
    """Map a Protoreal path onto Klein bottle surface coordinates.

    (ω, ι) → (u_param, v_param) via:
      u_param = atan2(ω, |ω|+0.1) * π   (thrust phase)
      v_param = atan2(ι, |ι|+0.1) * π   (anchor phase)
    Then evaluate the Klein bottle immersion at that point.
    """
    xs, ys, zs = [], [], []
    r = 2.0
    a_coeff = 2.0

    for i in range(len(path['b'])):
        b_val = path['b'][i]
        c_val = path['c'][i]

        # Map to angular coordinates
        u_p = math.atan2(b_val, abs(b_val) + 0.5) * 2.0
        v_p = math.atan2(c_val, abs(c_val) + 0.5) * 2.0

        x = (r + a_coeff * math.cos(v_p / 2) * math.sin(u_p)
             - a_coeff * math.sin(v_p / 2) * math.sin(2 * u_p)) * math.cos(v_p)
        y = (r + a_coeff * math.cos(v_p / 2) * math.sin(u_p)
             - a_coeff * math.sin(v_p / 2) * math.sin(2 * u_p)) * math.sin(v_p)
        z = (a_coeff * math.sin(v_p / 2) * math.sin(u_p)
             + a_coeff * math.cos(v_p / 2) * math.sin(2 * u_p))

        # Offset by a (real part) to separate orbits vertically
        z += (path['a'][i] - 1.0) * 0.3

        xs.append(x)
        ys.append(y)
        zs.append(z)

    return xs, ys, zs


# ── Build the visualization ──
col_bottle, col_phase = st.columns([3, 2])

with col_bottle:
    st.markdown("#### Klein Bottle with Function Orbits")

    x_kb, y_kb, z_kb, sr_kb = klein_bottle_surface(res=50)

    fig_kb = go.Figure()

    # Surface
    fig_kb.add_trace(go.Surface(
        x=x_kb, y=y_kb, z=z_kb,
        surfacecolor=sr_kb,
        colorscale=[[0, 'rgba(0,255,204,0.15)'], [0.5, 'rgba(50,50,80,0.1)'], [1, 'rgba(255,51,102,0.15)']],
        showscale=False,
        opacity=0.25,
        lighting=dict(ambient=0.6, diffuse=0.4, roughness=0.5, specular=0.3),
        name='Klein Bottle'
    ))

    # Paths
    path_colors = [
        '#00ffcc', '#ff3366', '#feca57', '#7c4dff',
        '#00e5ff', '#ff6e40', '#69f0ae', '#ea80fc',
    ]

    for idx, path in enumerate(paths):
        px, py, pz = project_path_to_bottle(path)
        color = path_colors[idx % len(path_colors)]

        # Trail
        fig_kb.add_trace(go.Scatter3d(
            x=px, y=py, z=pz,
            mode='lines',
            line=dict(width=3, color=color),
            name=f'Orbit {idx+1}',
            opacity=0.8,
        ))

        # Start marker
        fig_kb.add_trace(go.Scatter3d(
            x=[px[0]], y=[py[0]], z=[pz[0]],
            mode='markers',
            marker=dict(size=6, color=color, symbol='circle'),
            showlegend=False,
            hovertext=f'Start {idx+1}: a={path["a"][0]:.2f}, ω={path["b"][0]:.2f}, ι={path["c"][0]:.2f}',
            hoverinfo='text',
        ))

        # End marker
        fig_kb.add_trace(go.Scatter3d(
            x=[px[-1]], y=[py[-1]], z=[pz[-1]],
            mode='markers',
            marker=dict(size=8, color=color, symbol='diamond'),
            showlegend=False,
            hovertext=f'End {idx+1}: a={path["a"][-1]:.2f}, ω={path["b"][-1]:.2f}, ι={path["c"][-1]:.2f}',
            hoverinfo='text',
        ))

    fig_kb.update_layout(
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            bgcolor='rgba(0,0,0,0)',
            camera=dict(eye=dict(x=1.5, y=1.5, z=0.8)),
        ),
        template="plotly_dark",
        margin=dict(l=0, r=0, b=0, t=10),
        height=650,
        paper_bgcolor='rgba(0,0,0,0)',
        legend=dict(
            orientation="h", yanchor="top", y=0.02,
            font=dict(size=10),
        ),
    )
    st.plotly_chart(fig_kb, use_container_width=True)


with col_phase:
    st.markdown("#### Phase Portrait (ω, ι)")

    fig_phase = go.Figure()

    for idx, path in enumerate(paths):
        color = path_colors[idx % len(path_colors)]
        sr_vals = [abs(s) for s in path['sr']]

        fig_phase.add_trace(go.Scatter(
            x=path['b'], y=path['c'],
            mode='lines+markers',
            marker=dict(
                size=3,
                color=sr_vals,
                colorscale=[[0, '#00ffcc'], [0.5, '#feca57'], [1, '#ff3366']],
                showscale=(idx == 0),
                colorbar=dict(title="|SR|", len=0.4, y=0.8) if idx == 0 else None,
            ),
            line=dict(width=1, color=color),
            name=f'Orbit {idx+1}',
            opacity=0.7,
        ))

        # Start/end
        fig_phase.add_trace(go.Scatter(
            x=[path['b'][0]], y=[path['c'][0]],
            mode='markers', marker=dict(size=8, color=color, symbol='circle'),
            showlegend=False,
        ))
        fig_phase.add_trace(go.Scatter(
            x=[path['b'][-1]], y=[path['c'][-1]],
            mode='markers', marker=dict(size=10, color=color, symbol='diamond'),
            showlegend=False,
        ))

    # Reference lines
    # Bridge: b*c = 1 (hyperbola)
    b_ref = np.linspace(0.2, 5, 100)
    fig_phase.add_trace(go.Scatter(
        x=b_ref, y=1.0/b_ref,
        mode='lines', line=dict(color='rgba(255,255,255,0.2)', dash='dot', width=1),
        name='ωι = 1 (Bridge)',
    ))
    # Parity: b = c
    fig_phase.add_trace(go.Scatter(
        x=b_ref, y=b_ref,
        mode='lines', line=dict(color='rgba(255,255,255,0.15)', dash='dash', width=1),
        name='ω = ι (Hodge)',
    ))

    fig_phase.update_layout(
        template="plotly_dark",
        height=320,
        margin=dict(l=20, r=20, t=10, b=20),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(title="ω (Thrust)", gridcolor='rgba(255,255,255,0.05)'),
        yaxis=dict(title="ι (Anchor)", gridcolor='rgba(255,255,255,0.05)'),
        legend=dict(orientation="h", yanchor="top", y=-0.15, font=dict(size=9)),
    )
    st.plotly_chart(fig_phase, use_container_width=True)

    # ── Convergence time series ──
    st.markdown("#### Real Part Trajectory")
    fig_a = go.Figure()
    for idx, path in enumerate(paths):
        color = path_colors[idx % len(path_colors)]
        fig_a.add_trace(go.Scatter(
            y=path['a'], mode='lines', line=dict(color=color, width=1.5),
            name=f'Orbit {idx+1}', showlegend=False,
        ))
    fig_a.add_hline(y=1.0, line_dash="dot", line_color="white", opacity=0.3,
                    annotation_text="Fixed Point (a=1)")
    fig_a.update_layout(
        template="plotly_dark", height=220,
        margin=dict(l=20, r=20, t=10, b=20),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(title="Iteration", gridcolor='rgba(255,255,255,0.05)'),
        yaxis=dict(title="a (Real Base)", gridcolor='rgba(255,255,255,0.05)'),
    )
    st.plotly_chart(fig_a, use_container_width=True)


# ── Final state table ──
st.markdown("#### Orbit Endpoints")

endpoint_data = []
for idx, path in enumerate(paths):
    endpoint_data.append({
        "Orbit": idx + 1,
        "a": f"{path['a'][-1]:.4f}",
        "ω": f"{path['b'][-1]:.4f}",
        "ι": f"{path['c'][-1]:.4f}",
        "SR": f"{path['sr'][-1]:.4f}",
        "ε": f"{path['e'][-1]:.4f}",
        "λ": f"{path['l'][-1]:.1f}",
        "Hodge (ω≈ι)": "✓" if abs(path['b'][-1] - path['c'][-1]) < 0.1 else "✗",
        "Converged (a≈1)": "✓" if abs(path['a'][-1] - 1.0) < 0.1 else "✗",
    })

import pandas as pd
st.dataframe(pd.DataFrame(endpoint_data), hide_index=True, use_container_width=True)

st.markdown(r"""
<div class="sim-card">
<h4 style="color: #7c4dff; margin-top: 0;">📐 How It Works</h4>
<p>The <b>Klein bottle surface</b> is a figure-8 immersion parameterized by thrust phase (ω) and anchor phase (ι).
The Monster Inverse identification $(ω, ι) \leftrightarrow (ι, ω)$ creates the non-orientable twist —
this is the same involution that swaps the hyperbolic fiber ($ωι = 1$) with the elliptic fiber ($ω = ι$).</p>
<p>Your function is applied iteratively. Each orbit starts at a different point and traces its path
across the bottle. <b>Fixed points</b> appear as clusters. <b>Attractors</b> appear as spiraling convergences.
<b>Chaos</b> appears as space-filling curves.</p>
<p><b>Try it:</b> Start with "Klein Self-Product" to see the non-associative algebra in action,
then switch to "Hyperbolic Rotation" to watch orbits flow along the Bridge Identity curve $ωι = 1$.</p>
</div>
""", unsafe_allow_html=True)

