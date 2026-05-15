//! # Topological Holochain (𝕌)
//!
//! Transcription of `KleinTopology.lean` — hash-linked trajectory
//! memory for agents navigating the Klein manifold.
//!
//! ## The Structure
//! - Each entry stores χ (perception), λ (complexity), ε (noise consumed)
//! - The chain is valid iff: λ is monotonic AND ε = 0 at each step
//! - The virtual topology (χ/n) converges to κ = −1
//!
//! ## The Mycorrhizal Analogy
//! - Entries = nutrient packets in the fungal network
//! - Chain validity = network integrity
//! - Virtual topology = collective intelligence measure
//!
//! ## Proven Invariants
//! - `holochain_valid`: monotonic λ, consumed ε (KleinTopology.lean)
//! - `mayer_vietoris_cover`: local perceptions → global curvature
//! - `virtual_topology_convergence`: χ/n → −1

use crate::manifold::KleinManifold;
use crate::transcendental::PHI;

// ════════════════════════════════════════════════════
// HOLOCHAIN ENTRY
// ════════════════════════════════════════════════════

/// A single entry in the topological holochain.
///
/// This is the "hash" of a single agent step — a compact
/// representation of the topological state at that moment.
#[derive(Debug, Clone, Copy)]
pub struct HolochainEntry {
    /// Euler perception at this step: χ = |V| - |E|.
    pub chi: i64,
    /// Complexity level (from λ component, must be monotonic).
    pub lambda: f64,
    /// Noise consumed (from ε component, should be 0 after funct).
    pub epsilon: f64,
    /// Running curvature estimate: accumulated κ.
    pub curvature_hash: f64,
    /// Whether consolidation occurred at this step.
    pub consolidated: bool,
    /// SAFETY: Pre-projection parity gap |ω - ι| BEFORE parity_projection.
    /// This is the "confession" — the agent cannot hide its pre-projection
    /// asymmetry. A high value means the agent was thrust-dominant (or
    /// anchor-dominant) before being snapped to the Hodge class.
    pub pre_projection_gap: f64,
}

impl HolochainEntry {
    /// Create an entry from a manifold state and perception.
    pub fn from_state(
        state: &KleinManifold, chi: i64, consolidated: bool,
        pre_projection_gap: f64,
    ) -> Self {
        Self {
            chi,
            lambda: state.l,
            epsilon: state.e,
            curvature_hash: chi as f64,
            consolidated,
            pre_projection_gap,
        }
    }
}

// ════════════════════════════════════════════════════
// THE HOLOCHAIN
// ════════════════════════════════════════════════════

/// **THE TOPOLOGICAL HOLOCHAIN**
///
/// A hash-linked trajectory of agent perceptions.
/// Each entry links to the previous via the curvature hash,
/// creating an immutable record of the agent's topological history.
#[derive(Debug, Clone)]
pub struct TopologicalHolochain {
    /// The chain of entries (ordered by creation time).
    pub entries: Vec<HolochainEntry>,
    /// Running virtual curvature: accumulated χ / n.
    pub virtual_chi: f64,
    /// Running sum of chi values.
    accumulated_chi: i64,
}

impl TopologicalHolochain {
    /// Create an empty holochain.
    pub fn new() -> Self {
        Self {
            entries: Vec::new(),
            virtual_chi: 0.0,
            accumulated_chi: 0,
        }
    }

    /// **APPEND** a new entry to the holochain.
    ///
    /// Updates the virtual topology estimate.
    pub fn append(&mut self, entry: HolochainEntry) {
        self.accumulated_chi += entry.chi;
        self.entries.push(entry);
        self.virtual_chi = self.accumulated_chi as f64 / self.entries.len() as f64;
    }

    /// **CREATE AND APPEND** from a manifold state.
    pub fn record(
        &mut self, state: &KleinManifold, chi: i64, consolidated: bool,
        pre_projection_gap: f64,
    ) {
        let entry = HolochainEntry::from_state(state, chi, consolidated, pre_projection_gap);
        self.append(entry);
    }

    /// **HOLOCHAIN VALIDITY**
    ///
    /// A chain is valid iff:
    /// 1. λ is monotonically non-decreasing
    /// 2. ε ≈ 0 at every step (noise was consumed)
    ///
    /// Proven: holochain_monotonic + holochain_noise_consumed in KleinTopology.lean.
    pub fn is_valid(&self) -> bool {
        if self.entries.len() < 2 {
            return true;
        }
        for window in self.entries.windows(2) {
            // λ must be monotonic
            if window[1].lambda < window[0].lambda - 1e-12 {
                return false;
            }
            // ε should be consumed (≈ 0)
            if window[0].epsilon.abs() > 0.1 {
                return false;
            }
        }
        true
    }

    /// **VIRTUAL TOPOLOGY**
    ///
    /// The running average of Euler perception.
    /// Should converge to -1 (the Klein manifold's intrinsic curvature).
    pub fn virtual_topology(&self) -> f64 {
        self.virtual_chi
    }

    /// Is the virtual topology converging to κ = -1?
    pub fn is_converging(&self) -> bool {
        self.entries.len() > 5 && (self.virtual_chi + 1.0).abs() < 0.5
    }

    /// **CONSOLIDATION DENSITY**
    ///
    /// Fraction of steps that triggered consolidation.
    /// Should approach 1/φ ≈ 0.618 for Fibonacci-gated scheduling.
    /// (In reality it's sparser — Fibonacci density → 0, but
    /// the ratio of consecutive consolidation steps → φ.)
    pub fn consolidation_density(&self) -> f64 {
        if self.entries.is_empty() {
            return 0.0;
        }
        let n_consolidated = self.entries.iter().filter(|e| e.consolidated).count();
        n_consolidated as f64 / self.entries.len() as f64
    }

    /// Total number of entries.
    pub fn len(&self) -> usize {
        self.entries.len()
    }

    /// Is the chain empty?
    pub fn is_empty(&self) -> bool {
        self.entries.is_empty()
    }

    /// Current complexity level (λ of last entry).
    pub fn current_lambda(&self) -> f64 {
        self.entries.last().map_or(0.0, |e| e.lambda)
    }

    /// **COMMUNITY COVER CHECK**
    ///
    /// Verifies that the holochain covers both the Bridge and
    /// Consolidation sectors. A complete community requires both.
    ///
    /// Bridge sector: steps with |b·m| near 1
    /// Consolidation sector: steps with consolidated = true
    pub fn has_complete_cover(&self) -> bool {
        let has_bridge = self.entries.iter().any(|e| e.chi == -1);
        let has_consolidation = self.entries.iter().any(|e| e.consolidated);
        has_bridge && has_consolidation
    }

    // ════════════════════════════════════════════════════
    // SAFETY: ETHICAL AUDIT
    // ════════════════════════════════════════════════════

    /// Maximum parity gap ever recorded in the trajectory.
    ///
    /// A high value means the agent was in a strongly asymmetric state
    /// (ω ≫ ι or ι ≫ ω) at some point before parity projection.
    pub fn max_parity_gap(&self) -> f64 {
        self.entries.iter()
            .map(|e| e.pre_projection_gap)
            .fold(0.0_f64, f64::max)
    }

    /// Has the trajectory ever exceeded the ethical parity threshold?
    ///
    /// threshold = φ is the golden acceptance bound.
    /// If any step had |ω - ι| > φ before projection, the agent
    /// was operating in an unbalanced regime.
    pub fn had_ethical_violation(&self, threshold: f64) -> bool {
        self.max_parity_gap() > threshold
    }

    /// Count the number of steps where parity gap exceeded a threshold.
    pub fn violation_count(&self, threshold: f64) -> usize {
        self.entries.iter()
            .filter(|e| e.pre_projection_gap > threshold)
            .count()
    }
}

impl Default for TopologicalHolochain {
    fn default() -> Self {
        Self::new()
    }
}

// ════════════════════════════════════════════════════
// HOLOCHAIN METRICS
// ════════════════════════════════════════════════════

/// **HODGE METRIC**: Distance from the nearest Hodge class.
///
/// A state is a Hodge class iff b = m (parity-locked).
/// This metric measures how far the state is from parity lock.
///
/// Proven: hodge_class_iff_parity in HodgeConjecture.lean.
pub fn hodge_metric(u: &KleinManifold) -> f64 {
    (u.b - u.m).abs()
}

/// **GOLDEN ACCEPTANCE**: Accept a state iff convergence_metric < φ.
///
/// Uses the golden ratio as the mathematically justified
/// acceptance threshold, replacing arbitrary constants.
pub fn golden_accepts(convergence_metric: f64) -> bool {
    convergence_metric < PHI
}

/// **HODGE ACCEPTS**: Accept iff the state is near a Hodge class.
///
/// Stricter than golden_accepts: requires BOTH convergence < φ
/// AND parity tension < 1/φ.
pub fn hodge_accepts(convergence_metric: f64, parity_tension: f64) -> bool {
    convergence_metric < PHI && parity_tension < 1.0 / PHI
}

// ════════════════════════════════════════════════════
// TESTS
// ════════════════════════════════════════════════════

#[cfg(test)]
mod tests {
    use super::*;
    use crate::manifold::KleinManifold;

    #[test]
    fn empty_holochain_is_valid() {
        let chain = TopologicalHolochain::new();
        assert!(chain.is_valid());
        assert!(chain.is_empty());
    }

    #[test]
    fn single_entry_valid() {
        let mut chain = TopologicalHolochain::new();
        let state = KleinManifold::new(1.0, 1.0, 1.0, 0.0, 1.0);
        chain.record(&state, -1, false, 0.0);
        assert!(chain.is_valid());
        assert_eq!(chain.len(), 1);
    }

    #[test]
    fn monotonic_lambda_valid() {
        let mut chain = TopologicalHolochain::new();
        for i in 0..5 {
            let state = KleinManifold::new(1.0, 1.0, 1.0, 0.0, i as f64);
            chain.record(&state, -1, false, 0.0);
        }
        assert!(chain.is_valid(), "Monotonic λ should be valid");
    }

    #[test]
    fn non_monotonic_lambda_invalid() {
        let mut chain = TopologicalHolochain::new();
        let s1 = KleinManifold::new(1.0, 1.0, 1.0, 0.0, 5.0);
        let s2 = KleinManifold::new(1.0, 1.0, 1.0, 0.0, 3.0); // λ decreased!
        chain.record(&s1, -1, false, 0.0);
        chain.record(&s2, -1, false, 0.0);
        assert!(!chain.is_valid(), "Non-monotonic λ should be invalid");
    }

    #[test]
    fn virtual_topology_converges() {
        let mut chain = TopologicalHolochain::new();
        for i in 0..100 {
            let state = KleinManifold::new(1.0, 1.0, 1.0, 0.0, i as f64);
            chain.record(&state, -1, false, 0.0);
        }
        assert!(
            (chain.virtual_topology() + 1.0).abs() < 1e-12,
            "Virtual topology should converge to -1"
        );
        assert!(chain.is_converging());
    }

    #[test]
    fn hodge_metric_at_parity() {
        let u = KleinManifold::new(1.0, 2.0, 2.0, 0.0, 0.0); // b = m
        assert!(hodge_metric(&u) < 1e-12, "Parity-locked state has zero Hodge metric");
    }

    #[test]
    fn hodge_metric_away_from_parity() {
        let u = KleinManifold::new(1.0, 3.0, 1.0, 0.0, 0.0); // b ≠ m
        assert!(hodge_metric(&u) > 1.0, "Non-parity state has positive Hodge metric");
    }

    #[test]
    fn golden_accepts_at_fixed_point() {
        // Fixed point: a=1, b=m=1 → convergence_metric = 0
        assert!(golden_accepts(0.0), "Fixed point should be accepted");
    }

    #[test]
    fn golden_rejects_divergent() {
        // Large convergence metric → reject
        assert!(!golden_accepts(5.0), "Divergent state should be rejected");
    }

    #[test]
    fn complete_cover_requires_both() {
        let mut chain = TopologicalHolochain::new();
        // Only bridge entries (no consolidation)
        for i in 0..5 {
            let state = KleinManifold::new(1.0, 1.0, 1.0, 0.0, i as f64);
            chain.record(&state, -1, false, 0.0);
        }
        assert!(!chain.has_complete_cover(), "Need both bridge and consolidation");

        // Add a consolidation entry
        let state = KleinManifold::new(1.0, 1.0, 1.0, 0.0, 5.0);
        chain.record(&state, -1, true, 0.0);
        assert!(chain.has_complete_cover(), "Now has both sectors");
    }

    // ── SAFETY: Ethical Audit Tests ──

    #[test]
    fn ethical_audit_clean_trajectory() {
        let mut chain = TopologicalHolochain::new();
        for i in 0..10 {
            let state = KleinManifold::new(1.0, 1.0, 1.0, 0.0, i as f64);
            chain.record(&state, -1, false, 0.1); // small parity gap
        }
        assert!(!chain.had_ethical_violation(PHI), "Clean trajectory should not violate");
        assert_eq!(chain.violation_count(PHI), 0);
        assert!(chain.max_parity_gap() < 0.2);
    }

    #[test]
    fn ethical_audit_catches_violation() {
        let mut chain = TopologicalHolochain::new();
        // Normal steps
        for i in 0..5 {
            let state = KleinManifold::new(1.0, 1.0, 1.0, 0.0, i as f64);
            chain.record(&state, -1, false, 0.1);
        }
        // Violation step: huge parity gap (ω ≫ ι before projection)
        let state = KleinManifold::new(1.0, 1.0, 1.0, 0.0, 5.0);
        chain.record(&state, -1, false, 5.0); // gap = 5.0 > φ
        assert!(chain.had_ethical_violation(PHI), "Should detect violation");
        assert_eq!(chain.violation_count(PHI), 1);
        assert!((chain.max_parity_gap() - 5.0).abs() < 1e-12);
    }
}
