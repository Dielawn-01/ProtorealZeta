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
# THE PRIMORIAL JITTER ANIMATION
# ════════════════════════════════════════════════════

st.markdown("---")
st.markdown(r"""
<div class="sim-card">
<h4 style="color: #00ffcc; margin-top: 0;">🧬 Primorial Jitter — The QM-GR Gap</h4>
<p>The <b>jitter</b> J(n) is the difference between left-folding (local/QM) and right-folding 
(global/GR) the first n primes through the Klein product. It grows as the 
<b>primorial</b> — J(n)/J(n-1) ≈ p_n, the n-th prime itself.</p>
<p style="font-size: 0.85rem; color: #667;">This is a structural analogy, not a physical claim. 
Whether the left/right fold correspondence maps to actual QM/GR is an open question.</p>
</div>
""", unsafe_allow_html=True)

@st.cache_data
def compute_primorial_jitter(max_n=30):
    """Compute the primorial jitter for first max_n primes."""
    from sympy import primerange
    primes = list(primerange(2, 200))[:max_n]
    
    def klein_mul(u1, u2):
        return ProtorealElement(
            a=u1.a*u2.a - u1.b*u2.c + u1.c*u2.b + u1.l*u2.e - u1.e*u2.l,
            b=u1.a*u2.b + u2.a*u1.b + u1.b*u2.b,
            c=u1.a*u2.c + u2.a*u1.c - u1.c*u2.c,
            e=u1.a*u2.e + u2.a*u1.e + u1.e*u2.e,
            l=u1.a*u2.l + u2.a*u1.l + u1.l*u2.l,
        )
    
    def prime_to_klein(p):
        return ProtorealElement(a=1.0/p, b=float(p), c=1.0/p, e=0, l=0)
    
    results = {'n': [], 'jitter': [], 'log_jitter': [], 'ratio': [], 'prime': []}
    
    for n in range(2, min(max_n + 1, len(primes) + 1)):
        elements = [prime_to_klein(p) for p in primes[:n]]
        
        # Left fold
        left = elements[0]
        for el in elements[1:]:
            left = klein_mul(left, el)
        
        # Right fold
        right = elements[-1]
        for el in reversed(elements[:-1]):
            right = klein_mul(el, right)
        
        jitter = left.a - right.a
        results['n'].append(n)
        results['jitter'].append(jitter)
        results['log_jitter'].append(math.log(abs(jitter)) if jitter != 0 else 0)
        results['prime'].append(primes[n-1])
        
        if len(results['jitter']) >= 2 and results['jitter'][-2] != 0:
            results['ratio'].append(jitter / results['jitter'][-2])
        else:
            results['ratio'].append(0)
    
    return results

try:
    jitter_data = compute_primorial_jitter(30)
    
    col_j1, col_j2 = st.columns(2)
    
    with col_j1:
        st.markdown("#### Jitter Growth (log scale)")
        fig_jitter = go.Figure()
        
        # Animated: build frames for each n
        n_vals = jitter_data['n']
        log_vals = jitter_data['log_jitter']
        
        # Base trace (full line, faded)
        fig_jitter.add_trace(go.Scatter(
            x=n_vals, y=log_vals,
            mode='lines+markers',
            line=dict(color='#00ffcc', width=3),
            marker=dict(size=6, color='#00ffcc', 
                       line=dict(color='white', width=1)),
            name='log|J(n)|',
            fill='tozeroy',
            fillcolor='rgba(0,255,204,0.08)',
        ))
        
        # Chebyshev function θ(p_n) for comparison
        chebyshev = []
        running = 0
        for i, n in enumerate(n_vals):
            running += math.log(jitter_data['prime'][i])
            chebyshev.append(running)
        
        fig_jitter.add_trace(go.Scatter(
            x=n_vals, y=chebyshev,
            mode='lines',
            line=dict(color='#ff3366', width=2, dash='dash'),
            name='θ(pₙ) Chebyshev',
            opacity=0.7,
        ))
        
        fig_jitter.update_layout(
            template="plotly_dark", height=320,
            margin=dict(l=30, r=10, t=10, b=30),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(title="n (number of primes)", gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(title="log|J(n)|", gridcolor='rgba(255,255,255,0.05)'),
            legend=dict(orientation="h", yanchor="top", y=1.12, font=dict(size=10)),
        )
        st.plotly_chart(fig_jitter, use_container_width=True)
    
    with col_j2:
        st.markdown("#### Growth Ratio J(n)/J(n-1)")
        
        # Skip first few (unstable)
        valid_n = n_vals[2:]
        valid_ratio = jitter_data['ratio'][2:]
        valid_primes = [jitter_data['prime'][i] for i in range(2, len(n_vals))]
        
        fig_ratio = go.Figure()
        
        # The ratio
        fig_ratio.add_trace(go.Bar(
            x=valid_n, y=valid_ratio,
            marker=dict(
                color=valid_ratio,
                colorscale=[[0, '#1a1a2e'], [0.5, '#00ffcc'], [1, '#ff3366']],
                line=dict(width=0),
            ),
            name='J(n)/J(n-1)',
            opacity=0.85,
        ))
        
        # The n-th prime (for comparison)
        fig_ratio.add_trace(go.Scatter(
            x=valid_n, y=valid_primes,
            mode='markers+lines',
            marker=dict(size=5, color='white', symbol='diamond-open'),
            line=dict(color='rgba(255,255,255,0.4)', width=1, dash='dot'),
            name='pₙ (nth prime)',
        ))
        
        fig_ratio.update_layout(
            template="plotly_dark", height=320,
            margin=dict(l=30, r=10, t=10, b=30),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(title="n", gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(title="Ratio / Prime", gridcolor='rgba(255,255,255,0.05)'),
            legend=dict(orientation="h", yanchor="top", y=1.12, font=dict(size=10)),
            barmode='overlay',
        )
        st.plotly_chart(fig_ratio, use_container_width=True)
    
    # Key insight callout
    st.markdown(r"""
    <div style="background: linear-gradient(135deg, rgba(0,255,204,0.08), rgba(255,51,102,0.08)); 
                border: 1px solid rgba(0,255,204,0.2); border-radius: 12px; padding: 16px; margin: 8px 0;">
        <span style="color: #00ffcc; font-family: 'JetBrains Mono', monospace; font-size: 0.9rem;">
            OBSERVATION (200-digit verified)</span><br>
        <span style="color: #e8eaf0; font-size: 1.1rem;">
            J(n)/J(n-1) → p_n &nbsp;•&nbsp; The jitter growth rate IS the sequence of primes</span><br>
        <span style="color: #667; font-size: 0.85rem;">
            Left fold (local/sequential) vs right fold (global/holistic) — 
            the gap between them grows multiplicatively by each new prime.
            See PrimorialJitter.lean for the formal framework.
        </span>
    </div>
    """, unsafe_allow_html=True)

except Exception as e:
    st.info(f"Primorial jitter requires sympy. Install with: `pip install sympy`. ({e})")

st.markdown("---")

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
st.sidebar.header("🧊 Bottle Appearance")
bottle_opacity = st.sidebar.slider("Surface Opacity", 0.05, 0.8, 0.35, 0.05,
                                    help="Transparency of the Klein bottle surface")

BOTTLE_COLORSCALES = {
    "Spectral Resonance": [[0, '#00ffcc'], [0.5, '#1a1a2e'], [1, '#ff3366']],
    "Viridis": 'Viridis',
    "Plasma": 'Plasma',
    "Twilight": [[0, '#e2d1c3'], [0.25, '#5e4fa2'], [0.5, '#0d0d1a'], [0.75, '#9e0142'], [1, '#e2d1c3']],
    "Deep Ocean": [[0, '#0a1628'], [0.3, '#0d47a1'], [0.6, '#00bcd4'], [1, '#e0f7fa']],
    "Solar Flare": [[0, '#0d0221'], [0.3, '#cc5803'], [0.6, '#fca311'], [1, '#fffbf0']],
    "Monochrome": [[0, '#1a1a2e'], [0.5, '#404060'], [1, '#8888aa']],
}
bottle_colorscale_name = st.sidebar.selectbox("Color Theme", list(BOTTLE_COLORSCALES.keys()), index=0)
bottle_colorscale = BOTTLE_COLORSCALES[bottle_colorscale_name]

bottle_lighting = st.sidebar.select_slider("Lighting", 
    options=["Matte", "Soft", "Glossy"],
    value="Soft")

LIGHTING_PRESETS = {
    "Matte": dict(ambient=0.8, diffuse=0.3, roughness=0.9, specular=0.1),
    "Soft": dict(ambient=0.6, diffuse=0.5, roughness=0.5, specular=0.4),
    "Glossy": dict(ambient=0.4, diffuse=0.6, roughness=0.1, specular=1.2),
}
bottle_light = LIGHTING_PRESETS[bottle_lighting]

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
# SIMULATION METRICS
# ════════════════════════════════════════════════════

def project_point_to_bottle(b_val, c_val, a_val=1.0):
    """Project a single (ω, ι, a) point onto the Klein bottle."""
    r, a_c = 2.0, 2.0
    u_p = math.atan2(b_val, abs(b_val) + 0.5) * 2.0
    v_p = math.atan2(c_val, abs(c_val) + 0.5) * 2.0
    x = (r + a_c * math.cos(v_p / 2) * math.sin(u_p)
         - a_c * math.sin(v_p / 2) * math.sin(2 * u_p)) * math.cos(v_p)
    y = (r + a_c * math.cos(v_p / 2) * math.sin(u_p)
         - a_c * math.sin(v_p / 2) * math.sin(2 * u_p)) * math.sin(v_p)
    z = (a_c * math.sin(v_p / 2) * math.sin(u_p)
         + a_c * math.cos(v_p / 2) * math.sin(2 * u_p))
    z += (a_val - 1.0) * 0.3
    return x, y, z

mc1, mc2, mc3, mc4, mc5, mc6 = st.columns(6)
mc1.metric("Mean |SR|", f"{metrics['mean_sr'][-1]:.4f}",
           delta=f"{metrics['mean_sr'][-1] - metrics['mean_sr'][0]:.4f}")
mc2.metric("κ (Curvature)", "-1.0", help="Non-associative invariant")
mc3.metric("Convergence", f"{metrics['convergence'][-1]:.4f}", delta="→ 0 target")
mc4.metric("χ (Euler)", "-1", help="Topological invariant")
mc5.metric("Particles", str(n_particles))
mc6.metric("Steps", str(n_steps))

col_conv, col_energy = st.columns(2)

with col_conv:
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
        template="plotly_dark", height=200,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(orientation="h", yanchor="top", y=1.15),
        yaxis=dict(title="Convergence")
    )
    st.plotly_chart(fig_conv, use_container_width=True)

with col_energy:
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
<h4 style="color: #00ffcc; margin-top: 0;">🧬 How the Klein Universe Works</h4>

<p>The <b>Klein bottle</b> is the manifold itself — a figure-8 immersion parameterized by
thrust phase (ω) and anchor phase (ι). The Monster Inverse identification
$(ω, ι) ↔ (ι, ω)$ creates the non-orientable twist.</p>

<p>Two layers are overlaid on this surface:</p>
<ul>
<li><b>Simulation particles</b> (small dots): N-body Klein elements undergoing sowing, interaction, and parity damping. They converge toward $a = 1$.</li>
<li><b>Function orbits</b> (colored trails): Your custom Protoreal function applied iteratively from multiple seeds.</li>
</ul>

<p><b>Dot color</b> = Standard Resonance $|SR| = |a - ω · ι|$ — cyan = equilibrium, red = tension.<br>
<b>Trail color</b> = orbit identity. <b>Circle</b> = start, <b>diamond</b> = end.<br>
<b>Reference curves</b> (phase portrait): dotted = Bridge ($ωι = 1$), dashed = Hodge ($ω = ι$).</p>
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
## 🧊 Function Explorer

Write a **custom Protoreal function** below. It receives a `ProtorealElement` `u` and returns
a transformed element. The output orbits are traced on the Klein bottle alongside the simulation particles.
""")

# ── Rules & Reference (collapsible) ──
with st.expander("📖 Rules for Writing Protoreal Functions", expanded=False):
    st.markdown(r"""
### Syntax

Your function is a single **Python expression** that receives `u` (a `ProtorealElement` with fields
`u.a`, `u.b`, `u.c`, `u.e`, `u.l`) and returns a new element via `P(a=..., b=..., c=..., e=..., l=...)`.
You can also use `u * u` for Klein multiplication.

### Available Symbols

| Symbol | Meaning | Value |
|--------|---------|-------|
| `u` | Current state | `ProtorealElement` |
| `P(...)` | Constructor | `ProtorealElement(a, b, c, e, l)` |
| `u * u` | Klein product | Non-commutative, non-associative |
| `phi` | Golden ratio φ | 1.618... |
| `gamma` | Euler–Mascheroni γ₀ | 0.5772... |
| `pi` | π | 3.1415... |
| Math | `sin, cos, tan, exp, log, sqrt, tanh, sinh, cosh, abs, atan2` | |

### Component Rules

| Component | Field | Algebraic Law | Physics Role |
|-----------|-------|--------------|-------------|
| **a** (Real) | `u.a` | Observable base | Interface between inner and outer worlds |
| **ω** (Thrust) | `u.b` | Idempotent: ω·ω = ω | Outer world — momentum / action / spatial curvature |
| **ι** (Anchor) | `u.c` | Contraction: ι·ι = −ι | Inner world — potential / thought / temporal curvature |
| **ε** (Noise) | `u.e` | Nilpotent: εⁿ = 0 | Inner world — perturbation / feeling / quantum fluctuation |
| **λ** (Level) | `u.l` | Accumulating: λ·λ = λ | Outer world — proper time / experience / action count |

### Physics ↔ Protoreal Dictionary

| Physics Concept | Protoreal Expression |
|----------------|---------------------|
| **Kinetic energy** | εⁿ → 0 (nilpotent at depth n, so kinetic energy is *transient*) |
| **Potential energy** | Bearing: ω · ι (the Bridge gives V = −1 at equilibrium) |
| **Force / acceleration** | Δa = ε (sowing converts noise to reality) |
| **Mass / inertia** | λ (consolidation level resists change) |
| **Gravitational coupling** | ω · ι (bearing = topological "mass") |
| **Curvature** | κ = −1 (the non-associativity invariant) |
| **Geodesic deviation** | (ω·ω)·ι − ω·(ω·ι) = κ (association failure = tidal force) |
| **Time reversal** | Monster Inverse: swap ω ↔ ι |
| **Lorentz boost** | Hyperbolic rotation in (ω, ι) plane |
| **Metric signature** | SR = a − ω·ι (Standard Resonance = signature trace) |
| **Fixed point** | a = 1 ↔ Re(s) = 1/2 (Duality Theorem) |
| **Thermal noise** | ε ~ exp(−\|SR\|/T) where T = \|ω·ι\| (Boltzmann ↔ Unruh bridge) |
| **Partition function** | Z = Σ exp(−λ·SR²) (consolidation level = inverse temperature) |
| **Observer (δ)** | δ(u) = \|ι\| · SR(u) — the inner world's measurement of outer deviation |
| **ε-δ limit** | ∀ε>0, ∃δ: δ(u)<ε ⟹ \|a−L\|<ε (generalizes Cauchy limits) |
| **Flip** | flip(δ) = δ ∘ R₄ — observe from the other side of the bridge |
| **Scale** | scale(δ, k) = k·δ — rescale the measurement window |
""")

# ── Presets: Physics first, then algebraic ──
PRESETS = {
    # ── Physics-Inspired ──
    "⚛ Harmonic Oscillator": "P(a=u.a + u.e, b=u.b, c=u.c, e=-u.b*u.c*(u.a - 1)*0.1, l=u.l + 1)",
    "🪐 Kepler Orbit": "P(a=u.a, b=u.b*cos(0.08) - u.c*sin(0.08), c=u.b*sin(0.08) + u.c*cos(0.08), e=u.e*0.99, l=u.l + 1)",
    "🌀 Geodesic Flow (κ = −1)": "P(a=u.a + u.e + 0.01*u.b*u.c, b=u.b - 0.005*u.b*u.b, c=u.c + 0.005*u.c, e=u.e*0.98, l=u.l + 1)",
    "🌡 Thermal Geodesic": "P(a=u.a + u.e + 0.01*u.b*u.c, b=u.b - 0.01*u.b*(u.b - u.c), c=u.c + 0.01*u.c*(u.b - u.c), e=0.1*exp(-abs(u.a - u.b*u.c)/(abs(u.b*u.c)+0.01)) - u.e*0.3, l=u.l+1)",
    "🔴 Friedmann Expansion": "P(a=u.a*(1 + u.e/(u.a+0.01)), b=u.b*(1+u.e/(3*u.a+0.01)), c=u.c*(1+u.e/(3*u.a+0.01)), e=sqrt(abs(u.a - u.b*u.c))*0.05, l=u.l+1)",
    "🌊 Damped Wave": "P(a=u.a + u.e, b=u.b + 0.1*sin(u.l*0.3), c=u.c + 0.1*cos(u.l*0.3), e=(1-u.a)*0.2 - u.e*gamma, l=u.l+1)",
    "δ Observer (ε-δ Limit)": "P(a=u.a - abs(u.c)*(u.a - u.b*u.c)*0.05, b=u.b - 0.02*(u.b - u.c), c=u.c + 0.02*(u.b - u.c), e=abs(u.c)*abs(u.a - u.b*u.c), l=u.l + 1)",
    # ── Algebraic ──
    "Sowing (funct)": "P(a=u.a + u.e, b=u.b, c=u.c, e=0, l=u.l + 1)",
    "Consolidation": "P(a=u.a + 0.1, b=u.b, c=u.c, e=u.e + 0.2, l=u.l)",
    "Monster Inverse (R4)": "P(a=u.a, b=u.c, c=u.b, e=u.e, l=u.l)",
    "Klein Self-Product": "u * u",
    "Parity Lock": "P(a=u.a, b=(u.b+u.c)/2, c=(u.b+u.c)/2, e=u.e, l=u.l)",
    "Bridge Projection": "P(a=1, b=u.b, c=1/u.b if u.b != 0 else 1, e=0, l=u.l)",
    "Stieltjes Drain": "P(a=u.a - gamma * u.e, b=u.b * 0.99, c=u.c * 1.01, e=u.e * 0.5, l=u.l + 1)",
    "Lorentz Boost": "P(a=u.a, b=u.b*cosh(0.1)+u.c*sinh(0.1), c=u.b*sinh(0.1)+u.c*cosh(0.1), e=u.e, l=u.l)",
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
# Three.js Klein Universe — live particle simulation
from core.klein_universe_3d import get_klein_universe_html
import streamlit.components.v1 as components

st.markdown("#### 𝕌 Klein Manifold — Live Simulation")
st.markdown("""
<div style="font-size:0.85rem; color:#667; margin-bottom:8px;">
<b>What you see IS the algebra.</b> Each particle evolves using only proven operations: 
exact Klein multiplication (ProtorealManifold.lean), sowing/funct (ProtorealOperator.lean), 
parity lock (MonsterInverse.lean). The ε channel is the only noise source. 
No random walks, no aesthetic forcing — if particles cluster, that's the product. 
If they spread, that's the product.
</div>
""", unsafe_allow_html=True)

klein_html = get_klein_universe_html(n_particles, noise_scale, apply_r4)
components.html(klein_html, height=650, scrolling=False)

# ── Phase portrait below ──
col_phase, col_a = st.columns(2)

with col_phase:
    st.markdown("#### Phase Portrait (ω, ι)")
    fig_phase = go.Figure()
    for idx, path in enumerate(paths):
        color = ['#00ffcc','#ff3366','#feca57','#7c4dff','#00e5ff','#ff6e40','#69f0ae','#ea80fc'][idx % 8]
        fig_phase.add_trace(go.Scatter(
            x=path['b'], y=path['c'], mode='lines+markers',
            marker=dict(size=2, color=color), line=dict(width=1, color=color),
            name=f'Orbit {idx+1}', opacity=0.7,
        ))
    b_ref = np.linspace(0.2, 5, 100)
    fig_phase.add_trace(go.Scatter(x=b_ref, y=1.0/b_ref, mode='lines',
        line=dict(color='rgba(255,255,255,0.15)', dash='dot', width=1), name='ωι=1'))
    fig_phase.add_trace(go.Scatter(x=b_ref, y=b_ref, mode='lines',
        line=dict(color='rgba(255,255,255,0.1)', dash='dash', width=1), name='ω=ι'))
    fig_phase.update_layout(
        template="plotly_dark", height=280, margin=dict(l=20,r=20,t=10,b=20),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(title="ω", gridcolor='rgba(255,255,255,0.05)'),
        yaxis=dict(title="ι", gridcolor='rgba(255,255,255,0.05)'),
        legend=dict(orientation="h", yanchor="top", y=-0.15, font=dict(size=9)),
    )
    st.plotly_chart(fig_phase, use_container_width=True)

with col_a:
    st.markdown("#### Real Part Trajectory")
    fig_a = go.Figure()
    for idx, path in enumerate(paths):
        color = ['#00ffcc','#ff3366','#feca57','#7c4dff','#00e5ff','#ff6e40','#69f0ae','#ea80fc'][idx % 8]
        fig_a.add_trace(go.Scatter(y=path['a'], mode='lines',
            line=dict(color=color, width=1.5), name=f'Orbit {idx+1}', showlegend=False))
    fig_a.add_hline(y=1.0, line_dash="dot", line_color="white", opacity=0.3,
                    annotation_text="Fixed Point (a=1)")
    fig_a.update_layout(
        template="plotly_dark", height=280, margin=dict(l=20,r=20,t=10,b=20),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(title="Iteration", gridcolor='rgba(255,255,255,0.05)'),
        yaxis=dict(title="a", gridcolor='rgba(255,255,255,0.05)'),
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
<h4 style="color: #7c4dff; margin-top: 0;">📐 Interpreting the Results</h4>
<p><b>Fixed points</b> appear as clusters where orbits converge.
<b>Attractors</b> appear as spiraling convergences — most Protoreal functions attract to $a = 1$.
<b>Chaos</b> appears as space-filling curves (try "Klein Self-Product" with 500 iterations).</p>
<p>The <b>Hodge check</b> (ω ≈ ι) tells you if the orbit reached parity equilibrium.
The <b>convergence check</b> (a ≈ 1) tells you if it reached the Duality fixed point $Re(s) = 1/2$.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("#### 🧪 Advanced: Function Lab")
st.markdown("For multi-variable Protoreal functions with codependent weights and jet-order visualization:")
if st.button("🔬 Open Function Lab"):
    st.switch_page("pages/7_Function_Lab.py")
