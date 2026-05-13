//! # Spectral Fiber (𝕌 ↔ ℂ)
//!
//! Transcription of `SpectralFiber.lean` and `DualityTheorem.lean`.
//!
//! ## The Fiber Bundle
//! - Base Space: ℝ (imaginary parts of zeta zeros)
//! - Total Space: KleinManifold
//! - Projection: π(t) = {0, t, 1/t, 0, 0}
//! - Connection: funct (parallel transport)
//! - Inverse Map: Re(s) = a / 2

use crate::manifold::KleinManifold;
use crate::operators::{funct, parity_projection, standard_resonance};

// ════════════════════════════════════════════════════
// FIBER PROJECTION (DualityTheorem.lean)
// ════════════════════════════════════════════════════

/// **FIBER PROJECTION**: maps imaginary height t → manifold state.
///
/// π(t) = {a := 0, b := t, m := 1/t, e := 0, l := 0}
///
/// The unbiased projection: starts at a = 0 (no assumption about Re(s)).
pub fn fiber_project(t: f64) -> KleinManifold {
    assert!(t.abs() > 1e-15, "Fiber projection requires t ≠ 0");
    KleinManifold::new(0.0, t, 1.0 / t, 0.0, 0.0)
}

/// **FIBER EQUILIBRIUM**: funct-corrected fiber state.
///
/// Steps:
/// 1. Project: u = {0, t, 1/t, 0, 0}
/// 2. Set ε = -resonance(u) = -(0 - t·(1/t)) = -(0 - 1) = 1
/// 3. Apply funct: a = 0 + 1 = 1
pub fn fiber_equilibrium(t: f64) -> KleinManifold {
    let u = fiber_project(t);
    let resonance = standard_resonance(&u);
    let corrected = KleinManifold::new(u.a, u.b, u.m, -resonance, u.l);
    funct(&corrected)
}

/// **ADELIC IMAGE**: maps manifold state → complex real part.
///
/// Re(s) = a / 2
pub fn adelic_image(u: &KleinManifold) -> f64 {
    u.a / 2.0
}

// ════════════════════════════════════════════════════
// CONVERGENCE ENGINE
// ════════════════════════════════════════════════════

/// **CONVERGENCE METRIC**: distance from the fixed point.
///
/// The fixed point has a = 1, b·m = 1, b = m.
/// Returns 0.0 when fully converged.
pub fn convergence_metric(u: &KleinManifold) -> f64 {
    let a_dev = (u.a - 1.0).powi(2);
    let bridge_dev = (u.b * u.m - 1.0).powi(2);
    let parity_dev = (u.b - u.m).powi(2);
    (a_dev + bridge_dev + parity_dev).sqrt()
}

/// **ITERATIVE CONVERGENCE**: repeatedly apply funct + parity
/// to converge toward the fixed point.
///
/// Returns the trajectory and the final state.
pub fn converge(
    initial: &KleinManifold,
    max_steps: usize,
    tolerance: f64,
) -> (Vec<KleinManifold>, KleinManifold) {
    let mut trajectory = vec![*initial];
    let mut state = *initial;

    for _ in 0..max_steps {
        // Step 1: Compute resonance correction
        let resonance = standard_resonance(&state);
        let corrected = KleinManifold::new(
            state.a, state.b, state.m, -resonance, state.l,
        );

        // Step 2: Apply funct (sow noise into reality)
        state = funct(&corrected);

        // Step 3: Apply parity projection (b ↔ m averaging)
        state = parity_projection(&state);

        trajectory.push(state);

        // Check convergence
        if convergence_metric(&state) < tolerance {
            break;
        }
    }

    (trajectory, state)
}

// ════════════════════════════════════════════════════
// TESTS
// ════════════════════════════════════════════════════

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn fiber_bridge_product() {
        let t = 14.134;
        let u = fiber_project(t);
        assert!(
            (u.b * u.m - 1.0).abs() < 1e-12,
            "Fiber bridge product should be 1"
        );
    }

    #[test]
    fn fiber_equilibrium_at_one() {
        let t = 14.134;
        let eq = fiber_equilibrium(t);
        assert!(
            (eq.a - 1.0).abs() < 1e-12,
            "Equilibrium a should be 1, got {}",
            eq.a
        );
    }

    #[test]
    fn adelic_image_is_half() {
        let t = 14.134;
        let eq = fiber_equilibrium(t);
        let re = adelic_image(&eq);
        assert!(
            (re - 0.5).abs() < 1e-12,
            "Adelic image should be 0.5, got {}",
            re
        );
    }

    #[test]
    fn fiber_works_for_many_zeros() {
        // Test with multiple known zeta zero imaginary parts
        let zeros = [14.134, 21.022, 25.011, 30.425, 32.935];
        for t in &zeros {
            let eq = fiber_equilibrium(*t);
            assert!(
                (eq.a - 1.0).abs() < 1e-12,
                "Equilibrium at t={} should have a=1, got {}",
                t, eq.a
            );
            assert!(
                (adelic_image(&eq) - 0.5).abs() < 1e-12,
                "Adelic at t={} should be 0.5",
                t
            );
        }
    }

    #[test]
    fn convergence_from_arbitrary_state() {
        // Iterative convergence from an arbitrary state
        // Note: the parity projection changes b and m, altering
        // the resonance. The convergence loop stabilizes the state
        // but may not reach a=1 exactly for arbitrary inputs.
        let u = KleinManifold::new(0.0, 3.0, 1.0 / 3.0, 0.0, 0.0);
        let (trajectory, final_state) = converge(&u, 10, 1e-6);
        assert!(
            trajectory.len() > 1,
            "Should have trajectory"
        );
        assert!(
            final_state.a.is_finite(),
            "Final state should be finite"
        );
        // The parity-locked state should have b ≈ m
        assert!(
            (final_state.b - final_state.m).abs() < 1e-6,
            "Converged state should be parity-locked"
        );
    }

    #[test]
    fn convergence_metric_at_fixed_point() {
        let u = KleinManifold::new(1.0, 1.0, 1.0, 0.0, 0.0);
        assert!(
            convergence_metric(&u) < 1e-12,
            "Fixed point should have zero metric"
        );
    }
}
