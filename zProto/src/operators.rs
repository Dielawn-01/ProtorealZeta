//! # Protoreal Operators (𝕌)
//!
//! Transcription of `ProtorealOperator.lean`, `MonsterInverse.lean`,
//! and `HodgeDecomposition.lean`.
//!
//! ## Operators
//! - `funct` (Sowing): ε → a, level += 1
//! - `consolidate` (Harvesting): doubles a and m
//! - `monster_inv` (R4): swaps b ↔ m (involution)
//! - `parity_projection`: (u + u*) / 2 (idempotent)
//! - `hodge_10`, `hodge_01`: Fourier frequency decomposition

use crate::manifold::KleinManifold;

// ════════════════════════════════════════════════════
// SOWING & HARVESTING (ProtorealOperator.lean)
// ════════════════════════════════════════════════════

/// **SOWING (funct)**: Converts noise potential (ε) into reality (a).
///
/// ```text
/// a ← a + ε
/// ε ← 0
/// λ ← λ + 1
/// ```
///
/// This is the fundamental "learning" operator — it commits
/// potential observations into the agent's base state.
pub fn funct(u: &KleinManifold) -> KleinManifold {
    KleinManifold::new(
        u.a + u.e, // Noise becomes reality
        u.b,       // Thrust unchanged
        u.m,       // Anchor unchanged
        0.0,       // Noise consumed
        u.l + 1.0, // Level incremented
    )
}

/// **HARVESTING (consolidate)**: Doubles the real and anchor components.
///
/// ```text
/// a ← a × 2
/// m ← m × 2
/// ```
pub fn consolidate(u: &KleinManifold) -> KleinManifold {
    KleinManifold::new(
        u.a * 2.0,
        u.b,
        u.m * 2.0,
        u.e + 1.0,
        u.l,
    )
}

// ════════════════════════════════════════════════════
// MONSTER INVERSE (MonsterInverse.lean)
// ════════════════════════════════════════════════════

/// **MONSTER INVERSE (R4)**: Swaps thrust ↔ anchor.
///
/// This is the Adelic Fourier transform that identifies
/// the hyperbolic fiber (b·m = 1) with the elliptic fiber (b = m).
///
/// **Involution**: monster_inv(monster_inv(u)) = u
pub fn monster_inv(u: &KleinManifold) -> KleinManifold {
    KleinManifold::new(u.a, u.m, u.b, u.e, u.l)
}

/// **PARITY PROJECTION**: (u + monster_inv(u)) / 2
///
/// Projects onto the parity-locked locus (b = m).
/// This is idempotent: parity(parity(u)) = parity(u).
pub fn parity_projection(u: &KleinManifold) -> KleinManifold {
    let avg = (u.b + u.m) / 2.0;
    KleinManifold::new(u.a, avg, avg, u.e, u.l)
}

// ════════════════════════════════════════════════════
// HODGE DECOMPOSITION (HodgeDecomposition.lean)
// ════════════════════════════════════════════════════

/// **HODGE (1,0) COMPONENT**: The thrust harmonic.
///
/// Projects onto the (1,0) Hodge sector: keeps b, zeroes m.
/// This is the "forward-looking" frequency.
pub fn hodge_10(u: &KleinManifold) -> KleinManifold {
    KleinManifold::new(u.a, u.b, 0.0, u.e, u.l)
}

/// **HODGE (0,1) COMPONENT**: The anchor harmonic.
///
/// Projects onto the (0,1) Hodge sector: keeps m, zeroes b.
/// This is the "backward-looking" frequency.
pub fn hodge_01(u: &KleinManifold) -> KleinManifold {
    KleinManifold::new(u.a, 0.0, u.m, u.e, u.l)
}

// ════════════════════════════════════════════════════
// ACTIVATION (ProtorealHyperbolic.lean)
// ════════════════════════════════════════════════════

/// **MESH TANH**: Component-wise hyperbolic activation.
///
/// Applies tanh to each component, preserving the manifold structure.
/// The derivative scaling is built into the nonlinearity.
pub fn mesh_tanh(u: &KleinManifold) -> KleinManifold {
    KleinManifold::new(
        u.a.tanh(),
        u.b.tanh(),
        u.m.tanh(),
        u.e.tanh(),
        u.l.tanh(),
    )
}

/// **STANDARD RESONANCE**: a - b·m
///
/// Measures the deviation from the Bridge equilibrium.
/// At equilibrium: resonance = 0 (when a = b·m).
pub fn standard_resonance(u: &KleinManifold) -> f64 {
    u.a - u.b * u.m
}

// ════════════════════════════════════════════════════
// TESTS (transcribed from Lean proofs)
// ════════════════════════════════════════════════════

#[cfg(test)]
mod tests {
    use super::*;
    use crate::manifold::{omega, iota};

    // ── Funct (ProtorealOperator.lean) ──
    #[test]
    fn funct_sows_noise() {
        let u = KleinManifold::new(1.0, 2.0, 3.0, 0.5, 0.0);
        let result = funct(&u);
        assert!((result.a - 1.5).abs() < 1e-12, "a should be a + ε");
        assert!((result.e - 0.0).abs() < 1e-12, "ε should be 0");
        assert!((result.l - 1.0).abs() < 1e-12, "λ should be 1");
    }

    #[test]
    fn funct_preserves_thrust_anchor() {
        let u = KleinManifold::new(1.0, 2.0, 3.0, 0.5, 0.0);
        let result = funct(&u);
        assert!((result.b - u.b).abs() < 1e-12);
        assert!((result.m - u.m).abs() < 1e-12);
    }

    // ── Monster Inverse (MonsterInverse.lean) ──
    #[test]
    fn monster_involution() {
        let u = KleinManifold::new(1.0, 2.0, 3.0, 0.5, 0.7);
        let result = monster_inv(&monster_inv(&u));
        assert_eq!(result, u, "monster_inv(monster_inv(u)) should equal u");
    }

    #[test]
    fn monster_swaps_thrust_anchor() {
        let u = KleinManifold::new(1.0, 2.0, 3.0, 0.5, 0.7);
        let result = monster_inv(&u);
        assert!((result.b - u.m).abs() < 1e-12, "b should become m");
        assert!((result.m - u.b).abs() < 1e-12, "m should become b");
    }

    // ── Parity Projection (MonsterInverse.lean) ──
    #[test]
    fn parity_locks_thrust_anchor() {
        let u = KleinManifold::new(1.0, 2.0, 3.0, 0.5, 0.7);
        let result = parity_projection(&u);
        assert!(
            (result.b - result.m).abs() < 1e-12,
            "Parity projection should lock b = m"
        );
    }

    #[test]
    fn parity_is_idempotent() {
        let u = KleinManifold::new(1.0, 2.0, 3.0, 0.5, 0.7);
        let once = parity_projection(&u);
        let twice = parity_projection(&once);
        assert_eq!(
            once, twice,
            "Parity projection should be idempotent"
        );
    }

    // ── Hodge Decomposition ──
    #[test]
    fn hodge_decomposition_adds_up() {
        let u = KleinManifold::new(0.0, 2.0, 3.0, 0.0, 0.0);
        let h10 = hodge_10(&u);
        let h01 = hodge_01(&u);
        let sum = h10 + h01;
        assert_eq!(sum, u, "hodge_10 + hodge_01 should reconstruct u");
    }

    // ── Resonance ──
    #[test]
    fn resonance_at_bridge() {
        // At Bridge: a = b·m
        let u = KleinManifold::new(6.0, 2.0, 3.0, 0.0, 0.0);
        assert!(
            standard_resonance(&u).abs() < 1e-12,
            "Resonance should be 0 at Bridge"
        );
    }

    // ── Monster preserves Bridge product ──
    #[test]
    fn monster_preserves_bridge() {
        let u = KleinManifold::new(1.0, 2.0, 3.0, 0.5, 0.7);
        let bm_original = u.b * u.m;
        let bm_reflected = monster_inv(&u).b * monster_inv(&u).m;
        assert!(
            (bm_original - bm_reflected).abs() < 1e-12,
            "Monster should preserve b·m"
        );
    }

    // ── Fiber Projection (DualityTheorem.lean) ──
    #[test]
    fn fiber_converges_to_one() {
        // Simulate: project t, set ε = -resonance, funct
        let t = 14.134; // First zeta zero imaginary part
        let u = KleinManifold::new(0.0, t, 1.0 / t, 0.0, 0.0);
        let resonance = standard_resonance(&u);
        let corrected = KleinManifold::new(u.a, u.b, u.m, -resonance, u.l);
        let equilibrium = funct(&corrected);
        assert!(
            (equilibrium.a - 1.0).abs() < 1e-12,
            "Fiber equilibrium should have a = 1, got {}",
            equilibrium.a
        );
    }

    // ── Adelic Image (SpectralFiber.lean) ──
    #[test]
    fn adelic_image_is_half() {
        let t = 14.134;
        let u = KleinManifold::new(0.0, t, 1.0 / t, 0.0, 0.0);
        let resonance = standard_resonance(&u);
        let corrected = KleinManifold::new(u.a, u.b, u.m, -resonance, u.l);
        let equilibrium = funct(&corrected);
        let adelic = equilibrium.a / 2.0;
        assert!(
            (adelic - 0.5).abs() < 1e-12,
            "Adelic image should be 1/2, got {}",
            adelic
        );
    }
}
