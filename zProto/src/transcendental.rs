//! # Transcendental Basis (𝕌)
//!
//! The five fundamental constants of the computable universe,
//! transcribed from `TranscendentalBasis.lean`.
//!
//! | Constant | Value     | Component | Role                        |
//! |----------|-----------|-----------|-----------------------------|
//! | e        | 2.71828…  | a (Real)  | Exponential growth engine   |
//! | π        | 3.14159…  | ω (Thrust)| Periodic/circular structure |
//! | φ        | 1.61803…  | λ (Level) | Golden accumulation         |
//! | γ        | 0.57721…  | ε (Noise) | Harmonic drift/static       |
//! | i        | √(−1)     | ι (Anchor)| Contraction anchor          |
//!
//! ## Proven Correspondences
//! - Euler's Identity: e^{iπ} = −1 (TranscendentalBasis.euler_identity)
//! - Bridge Identity: ω·ι = −1 (Protoreal.bridge)
//! - Golden Recurrence: φ² = φ + 1 (HodgeConjecture.phi_sq)

use std::f64::consts::{E, PI};

// ════════════════════════════════════════════════════
// THE FIVE CONSTANTS
// ════════════════════════════════════════════════════

/// **e** — Euler's number. Maps to component `a` (real part).
/// The base of exponential growth; the sowing operator's engine.
pub const EULER_E: f64 = E;

/// **π** — The circle constant. Maps to component `ω` (thrust).
/// Periodic spectral structure; attention rotation period.
pub const PI_CONST: f64 = PI;

/// **φ** — The golden ratio (1 + √5) / 2. Maps to component `λ` (level).
/// The accumulation eigenvalue; acceptance threshold; dopant schedule limit.
/// Proven: φ² = φ + 1 (HodgeConjecture.phi_sq)
pub const PHI: f64 = 1.618_033_988_749_895;

/// **γ** — The Euler-Mascheroni constant. Maps to component `ε` (noise).
/// The harmonic series drift; noise injection scale.
/// γ = lim_{n→∞} (∑_{k=1}^{n} 1/k − ln n) ≈ 0.5772…
pub const GAMMA: f64 = 0.577_215_664_901_532_9;

// ════════════════════════════════════════════════════
// DERIVED FUNCTIONS
// ════════════════════════════════════════════════════

/// **Golden threshold** — φ as the discriminator acceptance bound.
/// Replaces arbitrary thresholds with the proven eigenvalue.
pub fn golden_threshold() -> f64 {
    PHI
}

/// **φ²** — The golden square. Used for secondary thresholds.
/// φ² = φ + 1 ≈ 2.618 (proven in HodgeConjecture.phi_sq)
pub fn phi_squared() -> f64 {
    PHI * PHI // = PHI + 1.0 by the golden recurrence
}

/// **Gamma-scaled noise** — Noise injection decaying as γ/√step.
/// Models the Euler-Mascheroni drift: the first Stieltjes constant
/// γ₀ governs the leading correction in prime counting.
///
/// At step 0: returns γ ≈ 0.577
/// At step n: returns γ / √(1 + n)
pub fn gamma_noise_scale(step: usize) -> f64 {
    GAMMA / (1.0 + step as f64).sqrt()
}

/// **Exponential learning rate** — lr = e^{−step/τ}.
/// Uses Euler's number as the natural decay base.
/// τ controls the timescale of learning.
pub fn euler_lr(step: usize, tau: f64) -> f64 {
    (-(step as f64) / tau).exp()
}

/// **Golden learning rate** — lr₀ × φ^{−epoch}.
/// Each epoch shrinks LR by the golden ratio.
/// Converges faster than exponential decay for small epoch counts.
pub fn golden_lr(base_lr: f64, epoch: usize) -> f64 {
    base_lr / PHI.powi(epoch as i32)
}

/// **Stieltjes drain coefficient** — γ-weighted correction.
/// From the La Rue-Stieltjes Antenna (ZetaEngine.py):
/// drain = termB × stieltjes_poly × log(1 + quad_sep)
///
/// The Stieltjes constants γ₀, γ₁, γ₂, γ₃ from the Laurent
/// expansion of ζ(s) around s = 1.
pub struct StieltjesConstants {
    pub gamma_0: f64,
    pub gamma_1: f64,
    pub gamma_2: f64,
    pub gamma_3: f64,
}

impl StieltjesConstants {
    /// The canonical Stieltjes constants (from mpmath/OEIS).
    pub fn canonical() -> Self {
        Self {
            gamma_0: GAMMA,
            gamma_1: -0.072_815_845_483_676_725,
            gamma_2: -0.009_690_363_192_872_318,
            gamma_3:  0.002_053_834_420_303_346,
        }
    }

    /// Evaluate the Stieltjes phase polynomial at displacement h.
    /// P(h) = γ₀ + γ₁·h + γ₂·h²/2 + γ₃·h³/6
    pub fn polynomial(&self, h: f64) -> f64 {
        self.gamma_0
            + self.gamma_1 * h
            + self.gamma_2 * h * h / 2.0
            + self.gamma_3 * h * h * h / 6.0
    }
}

// ════════════════════════════════════════════════════
// FIBONACCI UTILITIES
// ════════════════════════════════════════════════════

/// Check if n is a Fibonacci number.
/// Used for the aperiodic dopant schedule (GlialDopant.lean).
pub fn is_fibonacci(n: usize) -> bool {
    if n == 0 || n == 1 {
        return true;
    }
    let mut a: usize = 0;
    let mut b: usize = 1;
    while b < n {
        let tmp = a + b;
        a = b;
        b = tmp;
    }
    b == n
}

/// Generate Fibonacci numbers up to max_val.
pub fn fibonacci_sequence(max_val: usize) -> Vec<usize> {
    let mut seq = vec![0, 1];
    loop {
        let next = seq[seq.len() - 2] + seq[seq.len() - 1];
        if next > max_val {
            break;
        }
        seq.push(next);
    }
    seq
}

// ════════════════════════════════════════════════════
// TESTS
// ════════════════════════════════════════════════════

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn golden_recurrence() {
        // φ² = φ + 1 (HodgeConjecture.phi_sq)
        assert!(
            (PHI * PHI - (PHI + 1.0)).abs() < 1e-12,
            "Golden recurrence: φ² should equal φ + 1"
        );
    }

    #[test]
    fn golden_threshold_is_phi() {
        assert!((golden_threshold() - PHI).abs() < 1e-15);
    }

    #[test]
    fn phi_squared_is_phi_plus_one() {
        assert!((phi_squared() - (PHI + 1.0)).abs() < 1e-12);
    }

    #[test]
    fn gamma_noise_decays() {
        let n0 = gamma_noise_scale(0);
        let n10 = gamma_noise_scale(10);
        let n100 = gamma_noise_scale(100);
        assert!(n0 > n10, "Noise should decay");
        assert!(n10 > n100, "Noise should continue decaying");
        assert!((n0 - GAMMA).abs() < 1e-12, "At step 0, noise = γ");
    }

    #[test]
    fn euler_lr_decays() {
        let lr0 = euler_lr(0, 10.0);
        let lr10 = euler_lr(10, 10.0);
        assert!((lr0 - 1.0).abs() < 1e-12, "At step 0, lr = e^0 = 1");
        assert!((lr10 - (-1.0_f64).exp()).abs() < 1e-12, "At step tau, lr = e^(-1)");
    }

    #[test]
    fn golden_lr_shrinks() {
        let lr0 = golden_lr(1.0, 0);
        let lr1 = golden_lr(1.0, 1);
        let lr2 = golden_lr(1.0, 2);
        assert!((lr0 - 1.0).abs() < 1e-12);
        assert!((lr1 - 1.0 / PHI).abs() < 1e-12);
        assert!(lr0 > lr1 && lr1 > lr2);
    }

    #[test]
    fn stieltjes_polynomial() {
        let s = StieltjesConstants::canonical();
        assert!((s.gamma_0 - GAMMA).abs() < 1e-12);
        // At h = 0: P(0) = γ₀
        assert!((s.polynomial(0.0) - GAMMA).abs() < 1e-12);
    }

    #[test]
    fn fibonacci_check() {
        assert!(is_fibonacci(0));
        assert!(is_fibonacci(1));
        assert!(is_fibonacci(2));
        assert!(is_fibonacci(3));
        assert!(is_fibonacci(5));
        assert!(is_fibonacci(8));
        assert!(is_fibonacci(13));
        assert!(!is_fibonacci(4));
        assert!(!is_fibonacci(6));
        assert!(!is_fibonacci(7));
    }

    #[test]
    fn fibonacci_sequence_gen() {
        let seq = fibonacci_sequence(21);
        assert_eq!(seq, vec![0, 1, 1, 2, 3, 5, 8, 13, 21]);
    }

    // ── Euler-Bridge Duality ──
    // Both e^{iπ} and ω·ι equal −1.
    // We can't compute e^{iπ} in Rust without a complex lib,
    // but we verify the Bridge side:
    #[test]
    fn bridge_value_matches_euler() {
        use crate::manifold::{omega, iota};
        let bridge = omega() * iota();
        // Bridge: ω·ι = -1
        // Euler: e^{iπ} = -1
        // Both = -1 (proven in TranscendentalBasis.euler_bridge_duality)
        assert!(
            (bridge.a - (-1.0)).abs() < 1e-12,
            "Bridge should equal Euler's identity value: -1"
        );
    }
}
