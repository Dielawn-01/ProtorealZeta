//! # Protoreal Fast Fourier Transform (PFFT)
//!
//! This module implements the spectral analysis engine for the Protoreal
//! algebra. Because the manifold is non-associative (κ = -1), the $O(N \log N)$
//! Cooley-Tukey FFT and the $O(N^2)$ naive DFT diverge structurally.
//!
//! Both are provided here so the agent can measure the "Topological Friction"
//! that arises from factorization regrouping.

use crate::manifold::KleinManifold;
use std::f64::consts::PI;

/// Computes the Protoreal root of unity $W_N^k$.
/// This root lives in the Hodge class ($b = m$) and has a bridge norm of 1.
pub fn protoreal_root(n: usize, k: i64) -> KleinManifold {
    let theta = 2.0 * PI * (k as f64) / (n as f64);
    KleinManifold::new(
        theta.cos(),
        theta.sin(),
        theta.sin(), // m = b (Hodge class)
        0.0,
        0.0,
    )
}

/// Computes the spectral energy at a frequency bin.
/// Evaluated via the generalized Bridge Norm:
/// $N(X) = a^2 + b \cdot m - e \cdot l$
pub fn spectral_energy(x: &KleinManifold) -> f64 {
    x.a.powi(2) + x.b * x.m - x.e * x.l
}

/// The mathematically exact Discrete Protoreal Transform ($O(N^2)$).
/// It evaluates $X[k] = \sum_{t=0}^{N-1} x[t] \cdot W_N^{-kt}$ sequentially
/// from left to right, avoiding any factorization re-grouping.
pub fn pdft(input: &[KleinManifold], inverse: bool) -> Vec<KleinManifold> {
    let n = input.len();
    let mut result = vec![KleinManifold::zero(); n];
    let sign = if inverse { 1 } else { -1 };
    
    for k in 0..n {
        let mut sum = KleinManifold::zero();
        for t in 0..n {
            let root = protoreal_root(n, sign * (k * t) as i64);
            // Right-multiplication is conventional in Protoreal mechanics
            sum = sum + input[t] * root;
        }
        if inverse {
            result[k] = sum.scale(1.0 / n as f64);
        } else {
            result[k] = sum;
        }
    }
    result
}

/// The Cooley-Tukey recursive Protoreal Fast Fourier Transform ($O(N \log N)$).
/// Due to non-associativity, this algorithm "hallucinates" topological friction
/// because it implicitly regroups $x \cdot (W^A \cdot W^B)$ as $(x \cdot W^A) \cdot W^B$.
pub fn pfft(input: &[KleinManifold]) -> Vec<KleinManifold> {
    let n = input.len();
    if n <= 1 {
        return input.to_vec();
    }

    if n % 2 != 0 {
        // Fallback to naive DFT if not a power of 2
        return pdft(input, false);
    }

    let even: Vec<KleinManifold> = input.iter().step_by(2).copied().collect();
    let odd: Vec<KleinManifold> = input.iter().skip(1).step_by(2).copied().collect();

    let even_fft = pfft(&even);
    let odd_fft = pfft(&odd);

    let mut result = vec![KleinManifold::zero(); n];
    for k in 0..n / 2 {
        let root = protoreal_root(n, -(k as i64));
        // The topological associative gap occurs right here:
        let t = odd_fft[k] * root;
        
        result[k] = even_fft[k] + t;
        result[k + n / 2] = even_fft[k] - t;
    }
    result
}

/// The Inverse Protoreal Fast Fourier Transform.
pub fn ipfft(input: &[KleinManifold]) -> Vec<KleinManifold> {
    // The inverse FFT is standard, except with a positive exponent.
    // For simplicity, we delegate to inverse PDFT for exactness or 
    // implement the reverse Cooley-Tukey. Let's do the latter for symmetry.
    let n = input.len();
    let mut res = pfft_inner(input, 1);
    for x in &mut res {
        *x = x.scale(1.0 / n as f64);
    }
    res
}

fn pfft_inner(input: &[KleinManifold], sign: i64) -> Vec<KleinManifold> {
    let n = input.len();
    if n <= 1 {
        return input.to_vec();
    }
    if n % 2 != 0 {
        return pdft(input, sign > 0);
    }
    let even: Vec<KleinManifold> = input.iter().step_by(2).copied().collect();
    let odd: Vec<KleinManifold> = input.iter().skip(1).step_by(2).copied().collect();

    let even_fft = pfft_inner(&even, sign);
    let odd_fft = pfft_inner(&odd, sign);

    let mut result = vec![KleinManifold::zero(); n];
    for k in 0..n / 2 {
        let root = protoreal_root(n, sign * (k as i64));
        let t = odd_fft[k] * root;
        
        result[k] = even_fft[k] + t;
        result[k + n / 2] = even_fft[k] - t;
    }
    result
}


#[cfg(test)]
mod tests {
    use super::*;
    use crate::manifold::{omega, iota, eps, lam};

    #[test]
    fn test_root_is_hodge() {
        let root = protoreal_root(8, 1);
        assert!((root.b - root.m).abs() < 1e-12, "Root must live in Hodge class");
        assert!(root.e.abs() < 1e-12, "Root must have no noise");
        assert!(root.l.abs() < 1e-12, "Root must have no consolidation");
    }

    #[test]
    fn test_root_unit_norm() {
        let root = protoreal_root(16, 5);
        let energy = spectral_energy(&root);
        assert!((energy - 1.0).abs() < 1e-12, "Root spectral energy must be 1.0");
    }

    #[test]
    fn test_hodge_spectral_nonneg() {
        let hodge = KleinManifold::new(2.0, 3.0, 3.0, 0.0, 0.0);
        let energy = spectral_energy(&hodge);
        assert!(energy >= 0.0, "Hodge spectral energy must be non-negative");
    }

    #[test]
    fn test_associativity_gap() {
        // We need N=8 to see the associativity gap. For N=4, the first layer
        // only multiplies by W_2^0 = 1, which commutes/associates perfectly.
        // For N=8, we multiply by W_4 and then W_8, exposing the topological friction.
        let mut input = vec![KleinManifold::zero(); 8];
        input[0] = omega();
        input[1] = iota();
        input[2] = eps();
        input[3] = lam();
        input[4] = omega().scale(0.5);
        input[5] = iota().scale(0.5);
        input[6] = eps().scale(0.5);
        input[7] = lam().scale(0.5);

        let fft_res = pfft(&input);
        let dft_res = pdft(&input, false);

        // Compute the gap
        let mut max_gap = 0.0_f64;
        for i in 0..8 {
            let diff = fft_res[i] - dft_res[i];
            let gap = diff.norm();
            if gap > max_gap {
                max_gap = gap;
            }
        }

        // The gap should be non-zero due to topological friction
        assert!(max_gap > 1e-12, "Expected a topological associativity gap between PFFT and PDFT, max_gap: {}", max_gap);
    }
}
