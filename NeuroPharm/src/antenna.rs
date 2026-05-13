use crate::protoreal::ProtorealFull;

pub fn calculate_jitter(u: ProtorealFull, v: ProtorealFull, w: ProtorealFull) -> f64 {
    let associator = ProtorealFull::curvature(&u, &v, &w);
    // We take the real part of the associator as the primary jitter magnitude
    associator.a
}

pub fn bogoliubov_mixing(forward: ProtorealFull, backward: ProtorealFull) -> (f64, f64) {
    // LGK Bogoliubov mixing: m.res / (r4_reflection m).res
    // We'll use the 'a' part as the base resonance magnitude
    let r_f = forward.a;
    let r_b = backward.r4_reflection().a;
    
    if r_b == 0.0 {
        return (1.0, 0.0);
    }
    
    let ratio = r_f / r_b;
    // Mixing coefficients: cosh(ratio), sinh(ratio)
    (ratio.cosh(), ratio.sinh())
}

pub fn t_generic_protoreal(indices: &[usize], primes: &[f64]) -> ProtorealFull {
    let n = indices.len() as f64;
    if n == 0.0 {
        return ProtorealFull::new(0.0, 0.0, 0.0, 0.0, 0.0);
    }
    
    // Decelerated Base: (Product p_i)^(2/N) * e
    let prod_p: f64 = primes.iter().product();
    let base = prod_p.powf(2.0 / n) * std::f64::consts::E;
    
    // Simplistic Stieltjes Drift
    let drift = primes.iter().zip(indices.iter())
        .map(|(p, i)| (p - *i as f64).powi(2))
        .sum::<f64>().sqrt() / (2.0 * std::f64::consts::PI);
        
    ProtorealFull::new(base - drift, base.ln(), drift / base, 0.0, 0.0)
}
