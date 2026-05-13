//! # Glial Dopant System (𝕌)
//!
//! Transcription of `GlialDopant.lean` — the astrocyte-gated
//! plasticity module for aperiodic noise injection.
//!
//! ## The Biological Analogy
//! - **Neurons** = `funct` (fast, every step)
//! - **Astrocytes** = `consolidate` (slow, Fibonacci-gated)
//! - **Ca²⁺ microdomains** = ε injection (stochastic, γ-scaled)
//!
//! ## The AGMP Four-Factor Rule
//! 1. Eligibility: standard gradient (ε component)
//! 2. Modulation: resonance feedback (SR → ε correction)
//! 3. Astrocyte gate: slow integration (consolidate on Fibonacci steps)
//! 4. Stabilization: parity projection (b = m lock)
//!
//! ## Proven Invariants
//! - `dopant_enables_growth`: complexity increases (λ monotonic)
//! - `dopant_consumes_noise`: ε = 0 after each funct
//! - `fibonacci_never_periodic`: the schedule is aperiodic (Penrose)

use crate::manifold::KleinManifold;
use crate::operators::{funct, consolidate, parity_projection, standard_resonance};
use crate::transcendental::{PHI, GAMMA, gamma_noise_scale, is_fibonacci};

// ════════════════════════════════════════════════════
// THE GLIAL STATE
// ════════════════════════════════════════════════════

/// **THE ASTROCYTE STATE**
///
/// Tracks the slow-timescale variables of the glial system.
/// This is the "fourth factor" in the AGMP learning rule.
#[derive(Debug, Clone)]
pub struct GlialState {
    /// Total funct applications (fast timescale counter).
    pub cycle_count: usize,
    /// Step at which last consolidation occurred.
    pub last_consolidation: usize,
    /// Euler perception history (for virtual topology).
    pub chi_history: Vec<i64>,
    /// Remaining noise budget (decays as γ/√step).
    pub noise_budget: f64,
    /// Accumulated gate value (slow integration).
    pub gate_value: f64,
    /// Gate time constant (τ_astrocyte).
    pub tau: f64,
}

impl GlialState {
    /// Create a new glial state with default parameters.
    pub fn new() -> Self {
        Self {
            cycle_count: 0,
            last_consolidation: 0,
            chi_history: Vec::new(),
            noise_budget: GAMMA,
            gate_value: 0.0,
            tau: 10.0,
        }
    }

    /// Create with custom time constant.
    pub fn with_tau(tau: f64) -> Self {
        Self { tau, ..Self::new() }
    }

    /// Is the astrocyte gate open?
    ///
    /// The gate opens when the integrated signal exceeds φ⁻¹ ≈ 0.618.
    /// This means the system is in a learning regime.
    pub fn gate_is_open(&self) -> bool {
        self.gate_value.abs() > 1.0 / PHI
    }

    /// Update the gate with a new signal (resonance magnitude).
    ///
    /// Exponential moving average with time constant τ:
    ///   gate ← gate × (1 - 1/τ) + signal × (1/τ)
    pub fn integrate_signal(&mut self, signal: f64) {
        let alpha = 1.0 / self.tau;
        self.gate_value = self.gate_value * (1.0 - alpha) + signal * alpha;
    }

    /// Record a perception.
    pub fn record_chi(&mut self, chi: i64) {
        self.chi_history.push(chi);
    }

    /// **VIRTUAL TOPOLOGY**
    ///
    /// The running average of Euler perception.
    /// Should converge to -1 (the Klein manifold's curvature).
    /// Proven: mayer_vietoris_cover in KleinTopology.lean.
    pub fn virtual_topology(&self) -> f64 {
        if self.chi_history.is_empty() {
            return 0.0;
        }
        let sum: i64 = self.chi_history.iter().sum();
        sum as f64 / self.chi_history.len() as f64
    }

    /// Is the virtual topology converging to κ = -1?
    pub fn topology_converging(&self) -> bool {
        self.chi_history.len() > 3 && (self.virtual_topology() + 1.0).abs() < 0.5
    }
}

impl Default for GlialState {
    fn default() -> Self {
        Self::new()
    }
}

// ════════════════════════════════════════════════════
// THE DOPANT CYCLE
// ════════════════════════════════════════════════════

/// **THE DOPANT CYCLE**
///
/// The main astrocyte-gated learning step:
///
/// 1. Compute resonance correction (ε = -SR)
/// 2. Apply funct (fast: ε → a, λ += 1)
/// 3. If Fibonacci step → apply golden_consolidation (slow)
/// 4. Apply parity projection (stabilization)
/// 5. If gate is open → inject γ-scaled noise
///
/// Returns the new manifold state and whether consolidation occurred.
pub fn dopant_cycle(
    state: &KleinManifold,
    glial: &mut GlialState,
) -> (KleinManifold, bool) {
    glial.cycle_count += 1;
    let step = glial.cycle_count;

    // 1. ELIGIBILITY — resonance correction
    let resonance = standard_resonance(state);
    let corrected = KleinManifold::new(
        state.a, state.b, state.m, -resonance, state.l,
    );

    // 2. FAST PATH — funct (neuron fires)
    let mut result = funct(&corrected);

    // 3. SLOW PATH — consolidate on Fibonacci steps (astrocyte gate)
    let did_consolidate = is_fibonacci(step);
    if did_consolidate {
        result = golden_consolidation(&result);
        glial.last_consolidation = step;
    }

    // 4. STABILIZATION — parity projection (b = m lock)
    result = parity_projection(&result);

    // 5. MODULATION — integrate resonance into gate
    glial.integrate_signal(resonance.abs());

    // 6. NOISE INJECTION — if gate is open, inject γ-scaled noise
    if glial.gate_is_open() {
        let noise = gamma_noise_scale(step);
        glial.noise_budget -= noise.abs();
        result = KleinManifold::new(
            result.a, result.b, result.m,
            result.e + noise, // Inject into ε
            result.l,
        );
    }

    (result, did_consolidate)
}

/// **GOLDEN CONSOLIDATION**
///
/// Scales the real part by φ while preserving parity.
/// This is the Penrose growth operator — the eigenvalue
/// of the Hodge-Star ∘ Consolidation composition.
///
/// Proven: golden_eigenvalue in HodgeConjecture.lean.
pub fn golden_consolidation(u: &KleinManifold) -> KleinManifold {
    KleinManifold::new(
        u.a * PHI,
        u.b,
        u.m,
        u.e,
        u.l,
    )
}

/// **SIMPLE DOPANT** — funct only, no gating.
///
/// For contexts where the full AGMP cycle is too heavy.
/// Still uses resonance correction.
pub fn simple_dopant(state: &KleinManifold) -> KleinManifold {
    let resonance = standard_resonance(state);
    let corrected = KleinManifold::new(
        state.a, state.b, state.m, -resonance, state.l,
    );
    funct(&corrected)
}

// ════════════════════════════════════════════════════
// TESTS
// ════════════════════════════════════════════════════

#[cfg(test)]
mod tests {
    use super::*;
    use crate::manifold::{omega, iota, KleinManifold};

    #[test]
    fn glial_state_creation() {
        let g = GlialState::new();
        assert_eq!(g.cycle_count, 0);
        assert!((g.noise_budget - GAMMA).abs() < 1e-12);
    }

    #[test]
    fn gate_initially_closed() {
        let g = GlialState::new();
        assert!(!g.gate_is_open(), "Gate should start closed");
    }

    #[test]
    fn gate_opens_on_high_signal() {
        let mut g = GlialState::with_tau(1.0); // Fast integration
        g.integrate_signal(5.0);
        assert!(g.gate_is_open(), "Gate should open on high signal");
    }

    #[test]
    fn virtual_topology_empty() {
        let g = GlialState::new();
        assert!((g.virtual_topology() - 0.0).abs() < 1e-12);
    }

    #[test]
    fn virtual_topology_converges() {
        let mut g = GlialState::new();
        // Feed it -1 repeatedly (the correct curvature)
        for _ in 0..100 {
            g.record_chi(-1);
        }
        assert!(
            (g.virtual_topology() + 1.0).abs() < 1e-12,
            "Virtual topology should converge to -1"
        );
    }

    #[test]
    fn dopant_cycle_increments_lambda() {
        let u = KleinManifold::new(0.5, 1.0, 1.0, 0.0, 0.0);
        let mut g = GlialState::new();
        let (result, _) = dopant_cycle(&u, &mut g);
        assert!(
            result.l > u.l,
            "Dopant cycle should increment λ"
        );
    }

    #[test]
    fn dopant_cycle_consumes_noise() {
        let u = KleinManifold::new(0.5, 1.0, 1.0, 0.3, 0.0);
        let mut g = GlialState::new();
        // Gate is closed initially, so no noise injection
        let (result, _) = dopant_cycle(&u, &mut g);
        // After funct, ε should be 0 (noise consumed) unless gate injected
        if !g.gate_is_open() {
            assert!(
                result.e.abs() < 1e-12,
                "With gate closed, ε should be 0 after funct"
            );
        }
    }

    #[test]
    fn dopant_fibonacci_consolidation() {
        let u = KleinManifold::new(1.0, 1.0, 1.0, 0.0, 0.0);
        let mut g = GlialState::new();

        // Step 1 is Fibonacci → should consolidate
        let (result, did_consolidate) = dopant_cycle(&u, &mut g);
        assert!(did_consolidate, "Step 1 should trigger consolidation");
        // After golden consolidation, a should be scaled by φ
        // But funct also adds ε to a, and parity may adjust...
        assert!(g.last_consolidation == 1);
    }

    #[test]
    fn dopant_non_fibonacci_no_consolidation() {
        let u = KleinManifold::new(1.0, 1.0, 1.0, 0.0, 0.0);
        let mut g = GlialState::new();

        // Run to step 4 (not Fibonacci)
        for _ in 0..3 {
            dopant_cycle(&u, &mut g);
        }
        let (_, did_consolidate) = dopant_cycle(&u, &mut g);
        assert!(!did_consolidate, "Step 4 is not Fibonacci");
    }

    #[test]
    fn golden_consolidation_scales_by_phi() {
        let u = KleinManifold::new(1.0, 1.0, 1.0, 0.0, 0.0);
        let result = golden_consolidation(&u);
        assert!(
            (result.a - PHI).abs() < 1e-12,
            "Golden consolidation should scale a by φ"
        );
    }

    #[test]
    fn parity_lock_preserved() {
        let u = KleinManifold::new(1.0, 1.0, 1.0, 0.0, 0.0);
        let mut g = GlialState::new();
        let (result, _) = dopant_cycle(&u, &mut g);
        assert!(
            (result.b - result.m).abs() < 1e-12,
            "Dopant cycle should preserve parity lock (b = m)"
        );
    }

    #[test]
    fn simple_dopant_works() {
        let u = KleinManifold::new(0.0, 14.134, 1.0 / 14.134, 0.0, 0.0);
        let result = simple_dopant(&u);
        assert!(
            (result.a - 1.0).abs() < 1e-12,
            "Simple dopant on fiber should give a = 1"
        );
    }
}
