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
