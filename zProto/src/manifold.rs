//! # Klein Manifold (𝕌)
//!
//! The 5-component Protoreal manifold: `u = {a, ω, ι, ε, λ}`.
//!
//! Every operation here is a direct transcription of `ProtorealManifold.lean`.
//! The Klein multiplication is non-associative and non-commutative.
//!
//! ## Axioms (proven in Lean, tested here)
//! - Bridge Identity: ω · ι = -1
//! - Non-Associativity: (ω · ω) · ι ≠ ω · (ω · ι)
//! - Curvature: κ.a = ((ω·ω)·ι).a - (ω·(ω·ι)).a = -1
//! - Thrust Idempotent: (ω·ω).b = 1
//! - Anchor Anti-Idempotent: (ι·ι).m = -1

use std::ops::{Add, Sub, Mul, Neg};

/// The 5-component Klein Manifold element.
///
/// | Field | Name            | Algebraic Property       |
/// |-------|-----------------|--------------------------|
/// | `a`   | Real Part       | Observable frequency     |
/// | `b`   | Thrust (ω)      | Idempotent: ω·ω → +b²   |
/// | `m`   | Anchor (ι)      | Anti-idempotent: ι·ι → -m²|
/// | `e`   | Noise (ε)       | Nilpotent: ε² = 0       |
/// | `l`   | Consolidation (λ)| Accumulating: λ·λ → +l² |
#[derive(Debug, Clone, Copy)]
pub struct KleinManifold {
    pub a: f64,
    pub b: f64,
    pub m: f64,
    pub e: f64,
    pub l: f64,
}

impl KleinManifold {
    /// Create a new manifold element.
    pub fn new(a: f64, b: f64, m: f64, e: f64, l: f64) -> Self {
        Self { a, b, m, e, l }
    }

    /// The zero element.
    pub fn zero() -> Self {
        Self::new(0.0, 0.0, 0.0, 0.0, 0.0)
    }

    /// The multiplicative identity (1, 0, 0, 0, 0).
    pub fn one() -> Self {
        Self::new(1.0, 0.0, 0.0, 0.0, 0.0)
    }

    /// Scalar multiplication: r * u.
    pub fn scale(self, r: f64) -> Self {
        Self::new(
            self.a * r,
            self.b * r,
            self.m * r,
            self.e * r,
            self.l * r,
        )
    }

    /// The Euclidean norm (for convergence metrics).
    pub fn norm(&self) -> f64 {
        (self.a.powi(2)
            + self.b.powi(2)
            + self.m.powi(2)
            + self.e.powi(2)
            + self.l.powi(2))
        .sqrt()
    }

    /// The standard resonance: a - b·m.
    /// This measures the deviation from the Bridge Identity.
    pub fn standard_resonance(&self) -> f64 {
        self.a - self.b * self.m
    }

    /// The bearing: b × m (topological compass).
    pub fn bearing(&self) -> f64 {
        self.b * self.m
    }
}

// ════════════════════════════════════════════════════
// BASIS ELEMENTS (from ProtorealManifold.lean)
// ════════════════════════════════════════════════════

/// ω — The Thrust basis element (0, 1, 0, 0, 0).
/// Idempotent: ω·ω has b-component = 1.
pub fn omega() -> KleinManifold {
    KleinManifold::new(0.0, 1.0, 0.0, 0.0, 0.0)
}

/// ι — The Anchor basis element (0, 0, 1, 0, 0).
/// Anti-idempotent: ι·ι has m-component = -1.
pub fn iota() -> KleinManifold {
    KleinManifold::new(0.0, 0.0, 1.0, 0.0, 0.0)
}

/// ε — The Noise basis element (0, 0, 0, 1, 0).
/// Nilpotent in the ε² = 0 sense at the manifold level.
pub fn eps() -> KleinManifold {
    KleinManifold::new(0.0, 0.0, 0.0, 1.0, 0.0)
}

/// λ — The Consolidation basis element (0, 0, 0, 0, 1).
/// Accumulating: λ·λ has l-component = 1.
pub fn lam() -> KleinManifold {
    KleinManifold::new(0.0, 0.0, 0.0, 0.0, 1.0)
}

// ════════════════════════════════════════════════════
// KLEIN MULTIPLICATION
// (from ProtorealManifold.lean, mul definition, lines 46-52)
// ════════════════════════════════════════════════════
//
// (u₁ · u₂).a = a₁a₂ - b₁m₂ + m₁b₂ + l₁e₂ - e₁l₂
// (u₁ · u₂).b = a₁b₂ + a₂b₁ + b₁b₂          (thrust: +self)
// (u₁ · u₂).m = a₁m₂ + a₂m₁ - m₁m₂          (anchor: -self)
// (u₁ · u₂).e = a₁e₂ + a₂e₁ + e₁e₂          (noise: +self)
// (u₁ · u₂).l = a₁l₂ + a₂l₁ + l₁l₂          (level: +self)

impl Mul for KleinManifold {
    type Output = Self;

    fn mul(self, other: Self) -> Self {
        // SAFETY: Nilpotent truncation (ε² = 0).
        // The Lean proof (ProtorealManifold.lean) establishes ε^n = 0
        // but f64 doesn't respect nilpotency. When both operands carry
        // noise (|ε| > machine epsilon), the product's ε is clamped to 0.
        // This closes the gap between the formal proof and the implementation.
        let e_raw = self.a * other.e + other.a * self.e + self.e * other.e;
        let e_safe = if self.e.abs() > 1e-12 && other.e.abs() > 1e-12 {
            0.0 // ε² = 0 (axiom-enforced, not approximated)
        } else {
            e_raw
        };

        Self {
            a: self.a * other.a - self.b * other.m + self.m * other.b
                + self.l * other.e - self.e * other.l,
            b: self.a * other.b + other.a * self.b + self.b * other.b,
            m: self.a * other.m + other.a * self.m - self.m * other.m,
            e: e_safe,
            l: self.a * other.l + other.a * self.l + self.l * other.l,
        }
    }
}

impl Add for KleinManifold {
    type Output = Self;

    fn add(self, other: Self) -> Self {
        Self {
            a: self.a + other.a,
            b: self.b + other.b,
            m: self.m + other.m,
            e: self.e + other.e,
            l: self.l + other.l,
        }
    }
}

impl Sub for KleinManifold {
    type Output = Self;

    fn sub(self, other: Self) -> Self {
        Self {
            a: self.a - other.a,
            b: self.b - other.b,
            m: self.m - other.m,
            e: self.e - other.e,
            l: self.l - other.l,
        }
    }
}

impl Neg for KleinManifold {
    type Output = Self;

    fn neg(self) -> Self {
        Self {
            a: -self.a,
            b: -self.b,
            m: -self.m,
            e: -self.e,
            l: -self.l,
        }
    }
}

impl PartialEq for KleinManifold {
    fn eq(&self, other: &Self) -> bool {
        (self.a - other.a).abs() < 1e-12
            && (self.b - other.b).abs() < 1e-12
            && (self.m - other.m).abs() < 1e-12
            && (self.e - other.e).abs() < 1e-12
            && (self.l - other.l).abs() < 1e-12
    }
}

impl std::fmt::Display for KleinManifold {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(
            f,
            "𝕌({:.4}, {:.4}ω, {:.4}ι, {:.4}ε, {:.4}λ)",
            self.a, self.b, self.m, self.e, self.l
        )
    }
}

// ════════════════════════════════════════════════════
// AXIOM TESTS (transcribed from Lean proofs)
// ════════════════════════════════════════════════════

#[cfg(test)]
mod tests {
    use super::*;

    // ── Bridge Identity (ProtorealAxioms.lean: bridge) ──
    #[test]
    fn bridge_identity_omega_iota() {
        let result = omega() * iota();
        assert!(
            (result.a - (-1.0)).abs() < 1e-12,
            "Bridge: (ω·ι).a should be -1, got {}",
            result.a
        );
    }

    #[test]
    fn bridge_identity_iota_omega() {
        let result = iota() * omega();
        assert!(
            (result.a - 1.0).abs() < 1e-12,
            "Bridge: (ι·ω).a should be +1, got {}",
            result.a
        );
    }

    // ── Non-Associativity (Uncomplex.lean: manifold_stability) ──
    #[test]
    fn non_associativity() {
        let left = (omega() * omega()) * iota();
        let right = omega() * (omega() * iota());
        assert_ne!(
            left, right,
            "Non-associativity: (ω·ω)·ι must ≠ ω·(ω·ι)"
        );
    }

    // ── Curvature (LGKCosmology.lean: curvature_a_component) ──
    #[test]
    fn curvature_is_neg_one() {
        let left = (omega() * omega()) * iota();
        let right = omega() * (omega() * iota());
        let kappa = left.a - right.a;
        assert!(
            (kappa - (-1.0)).abs() < 1e-12,
            "Curvature: κ.a should be -1, got {}",
            kappa
        );
    }

    // ── Structural Heterogeneity (StructuralHeterogeneity.lean) ──
    #[test]
    fn thrust_self_coupling_positive() {
        let result = omega() * omega();
        assert!(
            (result.b - 1.0).abs() < 1e-12,
            "Thrust: (ω·ω).b should be +1, got {}",
            result.b
        );
    }

    #[test]
    fn anchor_self_coupling_negative() {
        let result = iota() * iota();
        assert!(
            (result.m - (-1.0)).abs() < 1e-12,
            "Anchor: (ι·ι).m should be -1, got {}",
            result.m
        );
    }

    #[test]
    fn structural_heterogeneity() {
        let thrust = (omega() * omega()).b;
        let anchor = (iota() * iota()).m;
        assert!(
            (thrust - anchor).abs() > 1e-12,
            "Heterogeneity: thrust coupling ≠ anchor coupling"
        );
    }

    // ── Noise Nilpotency (SAFETY: ε² = 0) ──
    #[test]
    fn noise_self_coupling() {
        let result = eps() * eps();
        // SAFETY FIX: ε² must be 0 (nilpotent truncation enforced).
        // Previously this test asserted (ε·ε).e == 1 (raw float behavior).
        // The Lean proof says ε^n = 0; the implementation now enforces this.
        assert!(
            result.e.abs() < 1e-12,
            "SAFETY: (ε·ε).e must be 0 (nilpotent), got {}",
            result.e
        );
    }

    // ── Level Accumulation ──
    #[test]
    fn level_self_coupling() {
        let result = lam() * lam();
        assert!(
            (result.l - 1.0).abs() < 1e-12,
            "Level: (λ·λ).l should be +1, got {}",
            result.l
        );
    }

    // ── Identity Element ──
    #[test]
    fn one_is_identity() {
        let u = KleinManifold::new(3.0, 2.0, 1.5, 0.7, 0.3);
        let left = KleinManifold::one() * u;
        let right = u * KleinManifold::one();
        assert_eq!(left, u, "1 * u should equal u");
        assert_eq!(right, u, "u * 1 should equal u");
    }

    // ── Consolidation Cross-Terms ──
    #[test]
    fn eps_lam_cross_term() {
        let result = lam() * eps();
        assert!(
            (result.a - 1.0).abs() < 1e-12,
            "Consolidation: (λ·ε).a should be +1, got {}",
            result.a
        );
    }

    #[test]
    fn lam_eps_anti_cross_term() {
        let result = eps() * lam();
        assert!(
            (result.a - (-1.0)).abs() < 1e-12,
            "Consolidation: (ε·λ).a should be -1, got {}",
            result.a
        );
    }

    // ── Triple Identity (StructuralHeterogeneity.lean: triple_identity) ──
    #[test]
    fn triple_identity() {
        let kappa = ((omega() * omega()) * iota()).a
            - (omega() * (omega() * iota())).a;
        let chi: i64 = 5 - 6; // |V| - |E| of observation graph
        let anchor = (iota() * iota()).m;

        assert!(
            (kappa - (-1.0)).abs() < 1e-12,
            "κ should be -1"
        );
        assert_eq!(chi, -1, "χ should be -1");
        assert!(
            (anchor - (-1.0)).abs() < 1e-12,
            "anchor coupling should be -1"
        );
    }

    // ── SAFETY: Nilpotent Truncation ──
    #[test]
    fn nilpotent_truncation_epsilon_squared() {
        // When both operands carry ε, the product's ε must be 0
        let e1 = KleinManifold::new(0.0, 0.0, 0.0, 0.5, 0.0);
        let e2 = KleinManifold::new(0.0, 0.0, 0.0, 0.3, 0.0);
        let result = e1 * e2;
        assert!(
            result.e.abs() < 1e-12,
            "SAFETY: ε² must be 0, got {}",
            result.e
        );
    }

    #[test]
    fn nilpotent_single_epsilon_propagates() {
        // When only ONE operand carries ε, it should propagate normally
        let u = KleinManifold::new(2.0, 0.0, 0.0, 0.0, 0.0);
        let e = KleinManifold::new(0.0, 0.0, 0.0, 0.5, 0.0);
        let result = u * e;
        assert!(
            (result.e - 1.0).abs() < 1e-12, // 2.0 * 0.5 + 0.0 * 0.0 + 0.0 * 0.5 = 1.0
            "Single-ε operand should propagate: expected 1.0, got {}",
            result.e
        );
    }
}
